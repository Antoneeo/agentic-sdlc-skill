// Shared helpers for the KB Agentic npm scripts (init / postinstall / preuninstall).
// Single source for client detection and skill-target paths.

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

const PACKAGE_ROOT = path.resolve(__dirname, '..');
const SKILL_SOURCE = path.join(PACKAGE_ROOT, 'skills', 'kb-agentic-skill');
const TEMPLATES_PATH = path.join(SKILL_SOURCE, 'templates.md');
// The directory name each client loads the skill from. Derived from the manifest,
// never hard-coded by a consumer: three distributions share these scripts, and a
// literal here is how a copy-fork starts installing under its sibling's name.
const INSTALLED_SKILL_NAME = (() => {
  const m = fs.readFileSync(path.join(SKILL_SOURCE, 'SKILL.md'), 'utf8').match(/^name:\s*(\S+)/m);
  if (!m) throw new Error(`SKILL.md carries no 'name:' field: ${SKILL_SOURCE}`);
  return m[1];
})();

// One entry per supported AI client. `home` may be overridden by an env var
// (Claude Desktop / portable installs); presence of the home dir counts as
// detection even when the CLI is not on PATH.

const CLIENTS = [
  {
    key: 'claude',
    label: 'Claude Code',
    cmd: 'claude',
    home: process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude'),
    envVar: 'CLAUDE_CONFIG_DIR',
    reload: 'Restart Claude Code to load it. Invoke via Skill tool as "kb-agentic".',
  },
  {
    key: 'gemini',
    label: 'Gemini CLI',
    cmd: 'gemini',
    home: process.env.GEMINI_HOME || path.join(os.homedir(), '.gemini'),
    envVar: 'GEMINI_HOME',
    reload: 'Run "gemini skills reload" or restart Gemini CLI to load it.',
  },
  {
    key: 'codex',
    label: 'Codex AI',
    cmd: 'codex',
    home: process.env.CODEX_HOME || path.join(os.homedir(), '.codex'),
    envVar: 'CODEX_HOME',
    reload: 'Restart Codex to load it. Invoke it as "$kb-agentic" or by asking for KB Agentic.',
  },
  {
    key: 'antigravity',
    label: 'Google Antigravity',
    cmd: 'agy',
    home: process.env.ANTIGRAVITY_HOME || path.join(os.homedir(), '.gemini'),
    envVar: 'ANTIGRAVITY_HOME',
    skillsSubdir: 'config/skills',
    homeMarker: path.join(
      process.env.ANTIGRAVITY_HOME || path.join(os.homedir(), '.gemini'),
      'config',
      'skills',
    ),
    reload: 'Restart Antigravity, or run "agy skills reload", to load it. Invoke by asking for KB Agentic.',
  },
];

function commandExists(cmd) {
  try {
    execSync(`${cmd} --version`, { stdio: 'ignore' });
    return true;
  } catch (e) {
    return false;
  }
}

function clientDetected(client) {
  const homePathToCheck = client.homeMarker || client.home;
  return commandExists(client.cmd)
    || Boolean(process.env[client.envVar])
    || fs.existsSync(homePathToCheck);
}

function skillTarget(client) {
  const subdir = client.skillsSubdir ? client.skillsSubdir.split('/') : ['skills'];
  return path.join(client.home, ...subdir, INSTALLED_SKILL_NAME);
}

function copyRecursive(src, dest) {
  if (typeof fs.cpSync === 'function') {
    fs.cpSync(src, dest, { recursive: true, force: true });
    return;
  }
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) copyRecursive(s, d);
    else fs.copyFileSync(s, d);
  }
}

function loadTemplates() {
  const text = fs.readFileSync(TEMPLATES_PATH, 'utf8');
  const lines = text.split(/\r?\n/);
  const sections = {};
  let heading = null;
  let block = null;
  for (const line of lines) {
    const h = line.match(/^##\s+(.*)$/);
    if (h && block === null) {
      heading = h[1].trim();
      sections[heading] = sections[heading] || [];
      continue;
    }
    if (/^```/.test(line)) {
      if (block === null) {
        block = [];
      } else {
        if (heading) sections[heading].push(block.join('\n') + '\n');
        block = null;
      }
      continue;
    }
    if (block !== null) block.push(line);
  }
  return sections;
}

function templateFor(sections, needle, index = 0) {
  const heading = Object.keys(sections).find((h) => h.includes(needle));
  const blocks = heading ? sections[heading] : undefined;
  if (!blocks || !blocks[index]) {
    throw new Error(
      `Template section containing "${needle}" (block ${index}) not found in ${TEMPLATES_PATH}. ` +
      'The package is corrupted or templates.md was restructured: fix templates.md, do not improvise content.'
    );
  }
  return blocks[index];
}

module.exports = {
  PACKAGE_ROOT,
  SKILL_SOURCE,
  INSTALLED_SKILL_NAME,
  TEMPLATES_PATH,
  CLIENTS,
  commandExists,
  clientDetected,
  skillTarget,
  copyRecursive,
  loadTemplates,
  templateFor,
};
