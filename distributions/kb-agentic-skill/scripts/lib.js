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

// --- SessionStart orientation hook (F-036) ---------------------------------
// ENFORCEMENT.md §4 says to wire this on every project that has a docs root and
// a Python interpreter. Until F-036 nothing did: it was a manual step, so it was
// skipped, and the guide router reached no agent that did not already know to
// look for it. The hook only INJECTS orientation -- it cannot force a skill
// invocation, and the mechanism that could (a blocking PreToolUse gate) is
// refused by the Vision's no-ceremony-ratchet Non-Goal.

const ORIENT_HOOK_TIMEOUT = 10;

// The validator's filename is DERIVED, never written here: the marketing lens
// ships `mkt_check.py` where the others ship `sdlc_check.py`, and this block is
// copied verbatim into all three distributions. A literal would make two of the
// three look for an entry point that does not exist.
const ORIENT_ENTRY_POINTS = ['sdlc_check.py', 'mkt_check.py'];
const ORIENT_ENTRY_POINT = (() => {
  for (const name of ORIENT_ENTRY_POINTS) {
    if (fs.existsSync(path.join(SKILL_SOURCE, 'scripts', name))) return name;
  }
  return ORIENT_ENTRY_POINTS[0];
})();

// Both settings layers are ALWAYS inspected for an existing hook, whichever one
// we would write to. Scanning only the target file left two holes: a project
// that starts un-vendored and later vendors flips the target from the local file
// to the shared one, finds nothing there, and appends a second hook; and a dead
// hook in the layer we are not writing stays invisible.
const ORIENT_SETTINGS_FILES = ['settings.json', 'settings.local.json'];

// A vendored path is built from a directory name read out of the TARGET
// repository, and the result is executed by the client as a shell command. That
// is repo-controlled input reaching a command line, so each segment must match
// this exactly -- `$(...)`, backticks and newlines are not "unusual names", they
// are the payload. The absolute branch cannot reach this input (it is built from
// os.homedir() and the client roster) but is filtered too, below.
const ORIENT_SAFE_SEGMENT = /^[A-Za-z0-9._-]+$/;
// Refused anywhere in a command path. NOT backslash: a Windows path is full of
// them and the shape this project already commits uses them.
const ORIENT_UNSAFE_IN_PATH = /["$`\r\n]/;

// Where a repo may legitimately vendor the validator. ENFORCEMENT §2 tells users
// to copy it next to their CI config (`tools/`), and a skill-authoring repo
// carries it under `skills/<lens>/scripts/`. Both are checked; the lens matching
// this distribution wins, so a monorepo vendoring several lenses cannot wire a
// sibling's validator against this lens's docs root.
function vendoredValidator(cwd) {
  const direct = [];
  for (const dir of ['tools', 'scripts']) {
    direct.push([dir, ORIENT_ENTRY_POINT].join('/'));
  }
  const skillDirs = (() => {
    let entries;
    try {
      entries = fs.readdirSync(path.join(cwd, 'skills'), { withFileTypes: true });
    } catch (e) {
      return [];                        // no skills/ here, or it is not a directory
    }
    const names = entries.filter((e) => e.isDirectory()).map((e) => e.name)
      .filter((n) => ORIENT_SAFE_SEGMENT.test(n));
    // This lens first: readdir order must not decide which lens we orient.
    names.sort((a, b) => (a === INSTALLED_SKILL_NAME ? -1 : 0)
      - (b === INSTALLED_SKILL_NAME ? -1 : 0));
    return names.map((n) => ['skills', n, 'scripts', ORIENT_ENTRY_POINT].join('/'));
  })();
  for (const rel of direct.concat(skillDirs)) {
    if (fs.existsSync(path.join(cwd, rel))) return rel;
  }
  return null;
}

function orientHookCommand(python, validator, hybrid) {
  return python + ' "' + validator + '" orient' + (hybrid ? ' --hybrid' : '');
}

// The token in an EXISTING command that names a validator -- quoted or bare, and
// NOT simply "the first quoted thing". That naive rule failed both ways: a
// command that quotes the interpreter (`"C:\Py\python.exe" "...sdlc_check.py"`)
// returned the interpreter, which exists, so a DEAD hook reported as healthy;
// and a command with no quotes at all returned nothing, so a WORKING hook was
// reported broken. Returns null when no token names a validator: the caller must
// then say it cannot tell, never that the hook is broken.
function orientHookValidator(command) {
  const cmd = String(command || '');
  const re = /"([^"]*)"|(\S+)/g;
  let m;
  while ((m = re.exec(cmd)) !== null) {
    const token = m[1] !== undefined ? m[1] : m[2];
    if (ORIENT_ENTRY_POINTS.some((n) => token.endsWith(n))) return token;
  }
  return null;
}

// Accepts both shapes seen in the wild: the documented groups
// (`SessionStart: [{ hooks: [...] }]`) and hook objects placed directly in the
// array. Anything else is reported by the caller rather than silently replaced.
function findOrientHook(settings) {
  const groups = settings && settings.hooks && settings.hooks.SessionStart;
  if (!Array.isArray(groups)) return null;
  for (const group of groups) {
    if (!group || typeof group !== 'object') continue;
    const inner = Array.isArray(group.hooks) ? group.hooks : [group];
    for (const h of inner) {
      const cmd = h && typeof h.command === 'string' ? h.command : '';
      if (ORIENT_ENTRY_POINTS.some((n) => cmd.includes(n)) && / orient(\s|$)/.test(cmd)) {
        return cmd;
      }
    }
  }
  return null;
}

// A settings object we can safely merge into: absent, or carrying the shapes we
// know. "I do not recognise this" must mean "write nothing", never "treat it as
// empty" -- the second is how a hand-written hook disappears.
function orientSettingsState(target) {
  if (!fs.existsSync(target)) return { ok: true, settings: {} };
  let settings;
  try {
    settings = JSON.parse(fs.readFileSync(target, 'utf8'));
  } catch (e) {
    return { ok: false, why: 'unreadable' };
  }
  if (!settings || typeof settings !== 'object' || Array.isArray(settings)) {
    return { ok: false, why: 'not-an-object' };
  }
  const hooks = settings.hooks;
  if (hooks !== undefined
      && (!hooks || typeof hooks !== 'object' || Array.isArray(hooks))) {
    return { ok: false, why: 'unexpected-hooks' };
  }
  if (hooks && hooks.SessionStart !== undefined && !Array.isArray(hooks.SessionStart)) {
    return { ok: false, why: 'unexpected-hooks' };
  }
  return { ok: true, settings };
}

// Returns a RESULT CODE, never printed text: the caller owns the wording and the
// battery asserts on the code. Codes:
//   wired | already | broken | unverifiable | malformed
//   no-validator | no-python | unsafe-path | write-failed
function wireOrientHook(options) {
  const cwd = options.cwd;
  const client = options.client;
  const python = options.python;
  const hybrid = !!options.hybrid;
  const docsLabel = options.docsLabel || 'project';

  const vendored = vendoredValidator(cwd);
  const absolute = path.join(skillTarget(client), 'scripts', ORIENT_ENTRY_POINT);
  const validator = vendored || absolute;
  if (!vendored && !fs.existsSync(absolute)) return { code: 'no-validator', validator };
  if (!python) return { code: 'no-python', validator };
  if (ORIENT_UNSAFE_IN_PATH.test(validator)) return { code: 'unsafe-path', validator };

  const command = orientHookCommand(python, validator, hybrid);

  // Inspect BOTH layers before deciding to write anything.
  for (const name of ORIENT_SETTINGS_FILES) {
    const p = path.join(cwd, '.claude', name);
    const state = orientSettingsState(p);
    if (!state.ok) {
      if (fs.existsSync(p)) return { code: 'malformed', file: name, target: p, why: state.why, command };
      continue;
    }
    const existing = findOrientHook(state.settings);
    if (!existing) continue;
    const found = orientHookValidator(existing);
    if (found === null) {
      return { code: 'unverifiable', file: name, target: p, existing, command };
    }
    const resolves = fs.existsSync(path.isAbsolute(found) ? found : path.join(cwd, found));
    return resolves
      ? { code: 'already', file: name, target: p, command: existing }
      : { code: 'broken', file: name, target: p, existing, command };
  }

  // F-042: a resolving MACHINE-GLOBAL hook (user-level settings) already
  // orients every project. Checked AFTER the project scan on purpose: a
  // project-level broken/malformed/unverifiable must be reported first — a
  // pre-check would mask a dead project hook behind "covered globally", the
  // wired-and-DEAD state F-041 calls the worst of the three. A dead or
  // unverifiable global hook falls through to the project write (the wrapper
  // may be emitting nothing) and the caller gets `globalNote` to print the
  // correction. A user-level token that is not absolute has no cwd to resolve
  // against, so it is treated as unverifiable.
  let globalNote;
  {
    const userTarget = path.join(client.home, 'settings.json');
    const ustate = orientSettingsState(userTarget);
    if (ustate.ok) {
      const uexisting = findOrientHook(ustate.settings);
      if (uexisting) {
        const ufound = orientHookValidator(uexisting);
        if (ufound !== null && path.isAbsolute(ufound) && fs.existsSync(ufound)) {
          return { code: 'global', target: userTarget, command: uexisting };
        }
        globalNote = (ufound === null || !path.isAbsolute(ufound)) ? 'unverifiable' : 'dead';
      }
    }
  }

  // A machine-specific command must not reach the shared, committed file.
  const file = vendored ? 'settings.json' : 'settings.local.json';
  const target = path.join(cwd, '.claude', file);
  const state = orientSettingsState(target);
  if (!state.ok) return { code: 'malformed', file, target, why: state.why, command };
  const settings = state.settings;

  if (!settings.hooks) settings.hooks = {};
  if (!Array.isArray(settings.hooks.SessionStart)) settings.hooks.SessionStart = [];
  settings.hooks.SessionStart.push({
    hooks: [{
      type: 'command',
      command,
      timeout: ORIENT_HOOK_TIMEOUT,
      statusMessage: 'Loading ' + docsLabel + ' orientation...',
    }],
  });

  // The installer has already written seed files by this point; an unwritable
  // settings file must not take the whole run down with a stack trace.
  try {
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, JSON.stringify(settings, null, 2) + String.fromCharCode(10), 'utf8');
  } catch (e) {
    return { code: 'write-failed', file, target, command, error: e.message };
  }
  return { code: 'wired', file, target, command, local: !vendored, globalNote };
}

// --- F-042: the machine-global hook (install-time wiring) -------------------
// The F-041 field lesson: the check note asked a question a normal user cannot
// evaluate. The owner's ruling: the hook is wired by the act the user already
// performs — installing/updating the package — at the USER level, which the
// installer knows exactly. `orient` is fail-open (no docs root ⇒ silent), so a
// global hook is safe by construction on unmanaged projects. Removal is a
// STANDING opt-out: a per-target marker remembers every settings file ever
// wired, and no install or update ever re-adds a removed hook. Deleting the
// marker file is the documented re-enable gesture (ENFORCEMENT §4).

// Python detection, shared by init (project wiring + index) and postinstall
// (global wiring). One list, one probe.
const PYTHON_CANDIDATES = ['python', 'python3', 'py'];
function detectPython() {
  for (const py of PYTHON_CANDIDATES) {
    try {
      execSync(`${py} --version`, { stdio: 'ignore' });
      return py;
    } catch (e) { /* try the next interpreter */ }
  }
  return null;
}

// Case/separator normalization uses the PLATFORM'S OWN path.relative: win32
// folds case and separators; forcing win32 semantics on POSIX would fold
// genuinely distinct paths (a false positive). One helper guards BOTH the
// uninstall attribution and the marker lookup — a naive prefix/string match
// misses `c:\` vs `C:\`, which on attribution re-manufactures the dead hook
// and on the marker re-wires against a standing opt-out.
function pathsEqual(a, b) {
  try {
    return path.relative(String(a), String(b)) === '';
  } catch (e) {
    return false;
  }
}
function pathInside(child, parent) {
  try {
    const rel = path.relative(String(parent), String(child));
    return rel !== '' && !rel.startsWith('..') && !path.isAbsolute(rel);
  } catch (e) {
    return false;
  }
}

// The marker lives under the family's agent-global root (the same root the
// validator's AGENTIC_SDLC_KB_ROOT seam names), read at call time so the test
// battery's stubbed env applies. Every helper is fail-open: a broken marker
// must never break an install, and a failed marker write never undoes a wire.
function orientMarkerPath() {
  const root = process.env.AGENTIC_SDLC_KB_ROOT
    || path.join(os.homedir(), '.agentic-sdlc');
  return path.join(root, 'orient-hook-wired');
}
function orientMarkerTargets() {
  try {
    return fs.readFileSync(orientMarkerPath(), 'utf8')
      .split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
  } catch (e) {
    return [];
  }
}
function orientMarkerHas(target) {
  return orientMarkerTargets().some((t) => pathsEqual(t, target));
}
function orientMarkerAdd(target) {
  try {
    if (orientMarkerHas(target)) return;
    fs.mkdirSync(path.dirname(orientMarkerPath()), { recursive: true });
    fs.appendFileSync(orientMarkerPath(), target + String.fromCharCode(10), 'utf8');
  } catch (e) { /* fail-open */ }
}
function orientMarkerRemove(target) {
  try {
    const rest = orientMarkerTargets().filter((t) => !pathsEqual(t, target));
    if (rest.length) {
      fs.writeFileSync(orientMarkerPath(), rest.join(String.fromCharCode(10)) + String.fromCharCode(10), 'utf8');
    } else {
      fs.rmSync(orientMarkerPath(), { force: true });
    }
  } catch (e) { /* fail-open */ }
}

// Wire the machine-global hook into client.home/settings.json — exactly ONE
// file (user level has no local split; the path is machine-local by nature).
// Codes follow the wireOrientHook contract, plus `opted-out`.
function wireGlobalOrientHook(options) {
  const client = options.client;
  const python = options.python;

  const validator = path.join(skillTarget(client), 'scripts', ORIENT_ENTRY_POINT);
  if (!fs.existsSync(validator)) return { code: 'no-validator', validator };
  if (!python) return { code: 'no-python', validator };
  if (ORIENT_UNSAFE_IN_PATH.test(validator)) return { code: 'unsafe-path', validator };
  const command = orientHookCommand(python, validator, false);

  const target = path.join(client.home, 'settings.json');
  const state = orientSettingsState(target);
  if (!state.ok) return { code: 'malformed', target, why: state.why, command };

  const existing = findOrientHook(state.settings);
  if (existing) {
    const found = orientHookValidator(existing);
    if (found === null || !path.isAbsolute(found)) {
      // No cwd exists at user level, so an unresolvable token is "cannot
      // tell" — left alone, never remembered as ours.
      return { code: 'unverifiable', target, existing, command };
    }
    if (fs.existsSync(found)) {
      // A hand-wired live hook, once removed, deserves the same respect as
      // one this installer wrote: remember the target.
      orientMarkerAdd(target);
      return { code: 'already', target, command: existing };
    }
    return { code: 'broken', target, existing, command };
  }

  if (orientMarkerHas(target)) return { code: 'opted-out', target };

  const settings = state.settings;
  if (!settings.hooks) settings.hooks = {};
  if (!Array.isArray(settings.hooks.SessionStart)) settings.hooks.SessionStart = [];
  settings.hooks.SessionStart.push({
    hooks: [{
      type: 'command',
      command,
      timeout: ORIENT_HOOK_TIMEOUT,
      statusMessage: 'Loading docs orientation...',
    }],
  });
  try {
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, JSON.stringify(settings, null, 2) + String.fromCharCode(10), 'utf8');
  } catch (e) {
    return { code: 'write-failed', target, command, error: e.message };
  }
  orientMarkerAdd(target);
  return { code: 'wired', target, command };
}

// Uninstall symmetry: removing the skill dirs would leave any global hook
// naming them wired-and-DEAD. So, across EVERY settings target the marker
// remembers (a hook wired under CLAUDE_CONFIG_DIR=/x must be cleaned from a
// shell without that env) unioned with the current client.home, remove ONLY
// the SessionStart entries whose validator token resolves INTO a root being
// removed. Foreign or unverifiable entries are never touched. The marker line
// is cleared ONLY when an entry was actually removed — when the user had
// already removed the hook, the line stays and the opt-out survives uninstall,
// reinstall, and sibling-lens uninstalls.
function removeGlobalOrientHooks(removedRoots) {
  const targets = [];
  const claude = CLIENTS.find((c) => c.key === 'claude');
  if (claude) targets.push(path.join(claude.home, 'settings.json'));
  for (const t of orientMarkerTargets()) {
    if (!targets.some((x) => pathsEqual(x, t))) targets.push(t);
  }
  const removedFrom = [];
  for (const target of targets) {
    try {
      const state = orientSettingsState(target);
      if (!state.ok || !fs.existsSync(target)) continue;
      const hooks = state.settings.hooks;
      if (!hooks || !Array.isArray(hooks.SessionStart)) continue;
      let removedHere = false;
      const ours = (h) => {
        const cmd = h && typeof h.command === 'string' ? h.command : '';
        if (!(ORIENT_ENTRY_POINTS.some((n) => cmd.includes(n)) && / orient(\s|$)/.test(cmd))) return false;
        const tok = orientHookValidator(cmd);
        if (tok === null || !path.isAbsolute(tok)) return false;   // cannot attribute: keep
        return removedRoots.some((root) => pathInside(tok, root));
      };
      const kept = [];
      for (const group of hooks.SessionStart) {
        if (!group || typeof group !== 'object') { kept.push(group); continue; }
        if (Array.isArray(group.hooks)) {
          const inner = group.hooks.filter((h) => {
            if (ours(h)) { removedHere = true; return false; }
            return true;
          });
          if (inner.length) kept.push({ ...group, hooks: inner });
          else if (inner.length !== group.hooks.length) { /* emptied: prune */ }
          else kept.push(group);
        } else if (ours(group)) {
          removedHere = true;                      // direct-object shape: prune
        } else {
          kept.push(group);
        }
      }
      if (!removedHere) continue;
      state.settings.hooks.SessionStart = kept;
      if (!kept.length) delete state.settings.hooks.SessionStart;
      if (state.settings.hooks && !Object.keys(state.settings.hooks).length) {
        delete state.settings.hooks;
      }
      fs.writeFileSync(target, JSON.stringify(state.settings, null, 2) + String.fromCharCode(10), 'utf8');
      orientMarkerRemove(target);
      removedFrom.push(target);
    } catch (e) { /* fail-open per target: never abort an uninstall */ }
  }
  return removedFrom;
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
  wireOrientHook,
  wireGlobalOrientHook,
  removeGlobalOrientHooks,
  detectPython,
  pathsEqual,
  orientHookCommand,
  copyRecursive,
  loadTemplates,
  templateFor,
};

// Lazy: reading routing.md is deferred to the consumer that actually asks.
Object.defineProperty(module.exports, 'SELF_LENS', { enumerable: true, get: selfLens });
Object.defineProperty(module.exports, 'SIBLING_LENSES', { enumerable: true, get: siblingLenses });

