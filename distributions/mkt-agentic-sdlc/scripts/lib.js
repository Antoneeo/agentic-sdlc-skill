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
// Kept for backward compatibility with this package's own scripts; the
// authoritative value is INSTALLED_SKILL_NAME, derived from SKILL.md below.
// The directory name each client loads the skill from. Derived from the manifest,
// never hard-coded by a consumer: three distributions share these scripts, and a
// literal here is how a copy-fork starts installing under its sibling's name.
const INSTALLED_SKILL_NAME = (() => {
  const m = fs.readFileSync(path.join(SKILL_SOURCE, 'SKILL.md'), 'utf8').match(/^name:\s*(\S+)/m);
  if (!m) throw new Error(`SKILL.md carries no 'name:' field: ${SKILL_SOURCE}`);
  return m[1];
})();

// The family's lens table, read from the shared `routing.md` rather than restated
// here. Same reason as INSTALLED_SKILL_NAME above, and the same failure it prevents:
// BOTH the row for this lens and the rows for its siblings used to be literals copied
// between distributions, so kb and mkt wrote a multi-lens note announcing themselves
// as the code lens. routing.md is one of the byte-identical shared files, so this
// lookup cannot drift between distributions.
// Lazy on purpose: preuninstall.js needs INSTALLED_SKILL_NAME and nothing else, and
// must keep working on an installation damaged badly enough to have lost routing.md.
function lensTable() {
  const routing = path.join(SKILL_SOURCE, 'routing.md');
  if (!fs.existsSync(routing)) throw new Error(`routing.md missing from the skill: ${SKILL_SOURCE}`);
  // Parsed as a table, not matched with a regex: a mis-escaped pattern matches the
  // empty string and yields undefined instead of throwing, which is how this lookup
  // failed the first time it was written.
  const table = new Map();
  for (const line of fs.readFileSync(routing, 'utf8').split(/\r?\n/)) {
    const cells = line.split('|').map((cell) => cell.trim());
    if (cells.length < 4) continue;
    const [, lens, skill] = cells;
    if (!/^[a-z]+$/.test(lens) || !/^`[a-z0-9-]+`$/.test(skill)) continue;
    const name = skill.slice(1, -1);
    // A duplicate row would otherwise be won silently by whichever came first, and a
    // wrong routing.md propagates byte-identically to every distribution.
    if (table.has(name)) throw new Error(`routing.md lists '${name}' more than once`);
    table.set(name, lens);
  }
  if (!table.size) throw new Error(`routing.md carries no lens table: ${routing}`);
  return table;
}

function selfLens() {
  const lens = lensTable().get(INSTALLED_SKILL_NAME);
  if (!lens) throw new Error(`routing.md has no lens row for '${INSTALLED_SKILL_NAME}'`);
  return lens;
}

// Sibling lenses of the same family: one shared core, one docs tree, a different
// fidelity discipline each. Keyed by the installed skill directory name.
function siblingLenses() {
  const table = lensTable();
  selfLens();                       // this lens must be in the table too
  table.delete(INSTALLED_SKILL_NAME);
  return Object.fromEntries(table);
}

// One entry per supported AI client. `home` may be overridden by an env var
// (Claude Desktop / portable installs); presence of the home dir counts as
// detection even when the CLI is not on PATH.

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
  return path.join(client.home, ...subdir, INSTALLED_SKILL_NAME);
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
  INSTALLED_SKILL_NAME,
  PACKAGE_ROOT,
  SKILL_SOURCE,
  TEMPLATES_PATH,
  CLIENTS,
  commandExists,
  clientDetected,
  skillTarget,
  copyRecursive,
  loadTemplates,
  templateFor,
};

// Lazy: reading routing.md is deferred to the consumer that actually asks.
Object.defineProperty(module.exports, 'SELF_LENS', { enumerable: true, get: selfLens });
Object.defineProperty(module.exports, 'SIBLING_LENSES', { enumerable: true, get: siblingLenses });

