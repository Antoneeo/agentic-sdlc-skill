// Shared helpers for the Marketing Agentic SDLC npm scripts (init / postinstall / preuninstall).
// Single source for client detection and skill-target paths: init and postinstall
// must never disagree on what "Claude Code is installed" means.

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

const PACKAGE_ROOT = path.resolve(__dirname, '..');
const SKILL_SOURCE = path.join(PACKAGE_ROOT, 'skills', 'mkt-agentic-sdlc');
const TEMPLATES_PATH = path.join(SKILL_SOURCE, 'templates.md');
const SKILL_DIR_NAME = 'mkt-agentic-sdlc';

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
    reload: 'Restart Claude Code to load it. Invoke via Skill tool as "mkt-agentic-sdlc".',
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
    reload: 'Restart Codex to load it. Invoke it as "$mkt-agentic-sdlc" or by asking for the Marketing SDLC skill.',
  },
  {
    // Google Antigravity 2.0 discovers global agent skills under
    // ~/.gemini/config/skills/ -- the SAME home the legacy Gemini CLI claims.
    // To avoid a shared-home double-install, this entry sets:
    //  - skillsSubdir 'config/skills': distinct target from gemini's ~/.gemini/skills
    //  - homeMarker on ~/.gemini/config/skills: detection never fires on bare
    //    ~/.gemini (which every Antigravity user has); only the Antigravity skills
    //    dir, the `agy` CLI, or ANTIGRAVITY_HOME count as "Antigravity installed".
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
    reload: 'Restart Antigravity, or run "agy skills reload", to load it. Invoke by asking for the Marketing SDLC skill.',
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
  // An entry may override the fs-existence probe with a `homeMarker` (a more
  // specific path than the bare home) so two clients sharing a home dir do not
  // both fire on its mere existence. Entries without a marker check `home`
  // exactly as before (backward-compatible).
  const homePathToCheck = client.homeMarker || client.home;
  return commandExists(client.cmd)
    || Boolean(process.env[client.envVar])
    || fs.existsSync(homePathToCheck);
}

function skillTarget(client) {
  // An entry may override the default `skills` sub-path with `skillsSubdir`
  // (split on '/' to keep cross-platform path.join correctness). Entries
  // without it resolve to <home>/skills/mkt-agentic-sdlc exactly as before.
  const subdir = client.skillsSubdir ? client.skillsSubdir.split('/') : ['skills'];
  return path.join(client.home, ...subdir, SKILL_DIR_NAME);
}

function copyRecursive(src, dest) {
  if (typeof fs.cpSync === 'function') {
    fs.cpSync(src, dest, { recursive: true, force: true });
    return;
  }
  // Fallback for Node < 16.7
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) copyRecursive(s, d);
    else fs.copyFileSync(s, d);
  }
}

/**
 * Parse templates.md into { headingText: [fencedBlock, ...] }.
 * Templates are single-sourced there: the init script must extract them
 * instead of carrying its own inline copies (which historically drifted).
 */
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

/**
 * Return the Nth fenced block of the section whose heading contains `needle`.
 * Throws with a clear message when missing: writing a wrong or empty
 * boilerplate silently would be worse than failing the init.
 */
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
  TEMPLATES_PATH,
  SKILL_DIR_NAME,
  CLIENTS,
  commandExists,
  clientDetected,
  skillTarget,
  copyRecursive,
  loadTemplates,
  templateFor,
};
