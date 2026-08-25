#!/usr/bin/env node
// Dev-only Node test battery for the CLIENTS registry (lib.js) and the
// install/uninstall lifecycle (postinstall.js / preuninstall.js).
//
// NOT shipped: this file is deliberately absent from package.json `files`
// (same precedent as the Python test_*.py batteries). Run it with:
//   node scripts/test_clients.js
//
// It guards the Antigravity 2.0 client unit against the P-TM threats:
//   T1 shared-home double-install, T2 wrong-path uninstall,
//   T3 detection false-pos/neg, T7 regression of the existing three clients.
//
// `lib.js` resolves each client's `home` from process.env / os.homedir() at
// module-load time, so the pure-function cases stub the env and re-require a
// fresh module instance; the install/uninstall round-trip runs postinstall and
// preuninstall as child processes with a stubbed HOME so the real filesystem
// side effects land inside a throwaway temp dir.

const { test } = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const LIB_PATH = require.resolve('./lib');
// Distribution-specific expectations are DERIVED, never written here: three
// distributions share this file, and a literal is how a copy-fork starts asserting
// its sibling's identity instead of its own.
const SKILL_SOURCE = require('./lib').SKILL_SOURCE;
const { INSTALLED_SKILL_NAME, SELF_LENS } = require('./lib');
const EXPECTED_DEFAULT_DOMAIN = (() => {
  const tpl = require('fs').readFileSync(require('path').join(SKILL_SOURCE, 'templates.md'), 'utf8');
  const m = tpl.match(/^default_domain:\s*(\S+)/m);
  if (!m) throw new Error('templates.md seeds no default_domain: the README template is incomplete');
  return m[1];
})();
// The docs root this distribution seeds, and the validator entry point it ships:
// both differ per distribution (mkt seeds mkt_docs and ships mkt_check.py), so a
// shared test must read them rather than name one distribution's answer.
const DOCS_DIR = (() => {
  const init = require('fs').readFileSync(require('path').join(__dirname, 'init.js'), 'utf8');
  const m = init.match(/'(\w*_?docs)\/README\.md'/);
  return m ? m[1] : 'ai_docs';
})();
const ENTRY_POINT_FILE = (() => {
  const dir = require('path').join(SKILL_SOURCE, 'scripts');
  for (const n of ['sdlc_check.py', 'mkt_check.py']) {
    if (require('fs').existsSync(require('path').join(dir, n))) return n;
  }
  throw new Error('no validator entry point in ' + dir);
})();
const A_SIBLING = (() => {
  // Derived from the shared routing.md table via lib, NOT from a literal in init.js:
  // reading the value under test out of the file under test is how a wrong lens word
  // stayed untestable.
  const names = Object.keys(require('./lib').SIBLING_LENSES);
  if (!names.length) throw new Error('the lens table names no sibling for this distribution');
  return names[0];
})();
const POSTINSTALL = path.join(__dirname, 'postinstall.js');
const PREUNINSTALL = path.join(__dirname, 'preuninstall.js');
const INIT = path.join(__dirname, 'init.js');

// --- TS11 helpers: run init.js in a throwaway project dir with a stubbed home.
// `siblingDirs` are created under <home>/.claude/skills/ so the sibling-lens probe
// sees exactly what the test intends, independent of what is installed for real.
function runInit(projectDir, { siblingDirs = [] } = {}) {
  const home = fs.mkdtempSync(path.join(os.tmpdir(), 'sdlc-init-home-'));
  const claudeHome = path.join(home, '.claude');
  fs.mkdirSync(path.join(claudeHome, 'skills'), { recursive: true });
  for (const d of siblingDirs) fs.mkdirSync(path.join(claudeHome, 'skills', d), { recursive: true });
  const env = { ...process.env, HOME: home, USERPROFILE: home, CLAUDE_CONFIG_DIR: claudeHome };
  delete env.GEMINI_HOME;
  delete env.CODEX_HOME;
  delete env.ANTIGRAVITY_HOME;
  try {
    execFileSync(process.execPath, [INIT], { cwd: projectDir, env, stdio: 'ignore' });
  } finally {
    fs.rmSync(home, { recursive: true, force: true });
  }
}

// --- TS11: init seeds default_domain once, stays create-only, sibling path additive ---
test('TS11 init seeds default_domain in the docs root README and never overwrites it', () => {
  const proj = fs.mkdtempSync(path.join(os.tmpdir(), 'sdlc-init-proj-'));
  try {
    runInit(proj);
    const readme = path.join(proj, DOCS_DIR, 'README.md');
    const first = fs.readFileSync(readme, 'utf8');
    assert.match(first, new RegExp('^---\r?\ndefault_domain: ' + EXPECTED_DEFAULT_DOMAIN + '\r?\n---'),
      `README frontmatter must open with default_domain: ${EXPECTED_DEFAULT_DOMAIN}`);

    // A project that edited its own default must survive a second init (create-only).
    fs.writeFileSync(readme, first.replace(`default_domain: ${EXPECTED_DEFAULT_DOMAIN}`,
      'default_domain: edited-by-hand'), 'utf8');
    runInit(proj);
    assert.match(fs.readFileSync(readme, 'utf8'), /default_domain: edited-by-hand/,
      'a second init must not overwrite an existing README (T1: create-only)');
  } finally {
    fs.rmSync(proj, { recursive: true, force: true });
  }
});

test('TS11 no sibling lens installed: no multi-lens note is written', () => {
  const proj = fs.mkdtempSync(path.join(os.tmpdir(), 'sdlc-init-solo-'));
  try {
    runInit(proj);
    assert.ok(!fs.existsSync(path.join(proj, 'AGENTIC_MULTI_LENS.md')),
      'single-lens install must cost nothing: no note, no ceremony');
  } finally {
    fs.rmSync(proj, { recursive: true, force: true });
  }
});

test('TS11 sibling lens installed: the note is additive and the protocol pointer is untouched', () => {
  const proj = fs.mkdtempSync(path.join(os.tmpdir(), 'sdlc-init-multi-'));
  try {
    // A protocol pointer written by the OTHER lens's init, carrying its own ladder.
    const sentinel = '# Written by the knowledge lens — do not touch\n';
    fs.writeFileSync(path.join(proj, 'CLAUDE.md'), sentinel, 'utf8');

    runInit(proj, { siblingDirs: [A_SIBLING] });

    assert.strictEqual(fs.readFileSync(path.join(proj, 'CLAUDE.md'), 'utf8'), sentinel,
      'init must never overwrite a user/sibling-authored protocol pointer (T1)');
    const note = fs.readFileSync(path.join(proj, 'AGENTIC_MULTI_LENS.md'), 'utf8');
    assert.match(note, new RegExp(A_SIBLING), 'the note names the detected sibling');
    assert.match(note, /routing\.md/, 'the note points at the domain router');
    assert.match(note, /Merge step owed/, 'a pre-existing pointer means a merge is owed');
    // The note must name THIS lens. The self row used to be the literal
    // "`agentic-sdlc` — the **code** lens", copied verbatim into every distribution:
    // kb and mkt announced themselves as their sibling and never named themselves,
    // and this test passed because it only ever checked the DETECTED sibling.
    // (Found by the cold-agent field test, 2026-08-02.)
    const LENS_ROW = /^- `([a-z0-9-]+)` — the \*\*([a-z]+)\*\* lens$/;
    const rows = note.split(/\r?\n/).map((l) => l.match(LENS_ROW)).filter(Boolean);
    assert.ok(rows.some((m) => m[1] === INSTALLED_SKILL_NAME && m[2] === SELF_LENS),
      `the note must name THIS lens (\`${INSTALLED_SKILL_NAME}\` — the **${SELF_LENS}** lens); it listed: ` +
      rows.map((m) => `${m[1]}/${m[2]}`).join(', '));
    assert.strictEqual(new Set(rows.map((m) => m[1])).size, rows.length,
      'no lens may be listed twice in the note');
  } finally {
    fs.rmSync(proj, { recursive: true, force: true });
  }
});

// Load a fresh copy of lib.js under a given env override. lib.js reads env +
// os.homedir() at require time, so we clear the require cache and (optionally)
// stub os.homedir()/env for the duration of the load.
function freshLib(env = {}) {
  const savedEnv = {};
  const managedKeys = ['CLAUDE_CONFIG_DIR', 'GEMINI_HOME', 'CODEX_HOME', 'ANTIGRAVITY_HOME', 'HOME', 'USERPROFILE'];
  for (const k of managedKeys) {
    savedEnv[k] = process.env[k];
    if (k in env) {
      if (env[k] === undefined) delete process.env[k];
      else process.env[k] = env[k];
    } else {
      // Clear per-client overrides by default so the home resolves to homedir().
      delete process.env[k];
    }
  }
  const savedHomedir = os.homedir;
  if (env.__homedir) os.homedir = () => env.__homedir;
  delete require.cache[LIB_PATH];
  let lib;
  try {
    lib = require('./lib');
  } finally {
    os.homedir = savedHomedir;
    for (const k of managedKeys) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
    delete require.cache[LIB_PATH];
  }
  return lib;
}

function clientByKey(lib, key) {
  const c = lib.CLIENTS.find((x) => x.key === key);
  assert.ok(c, `CLIENTS must contain a '${key}' entry`);
  return c;
}

// --- T4/TS7 (file-list half): what the package actually ships ---------------
// Run in EVERY phase that edits `files[]`, not only at release: an unlisted
// support file reaches no consumer, and a listed-but-absent one breaks the pack.
test('TS7 package files[] lists exactly the shipped skill files, and they all exist', () => {
  const pkgRoot = path.resolve(__dirname, '..');
  const pkg = JSON.parse(fs.readFileSync(path.join(pkgRoot, 'package.json'), 'utf8'));
  for (const rel of pkg.files) {
    assert.ok(fs.existsSync(path.join(pkgRoot, rel)), `files[] lists a missing path: ${rel}`);
  }
  // The validator ships as two files since the multi-domain core: shipping the
  // entry point without the core would fail at import on every consumer.
  const skillDir = path.relative(pkgRoot, require('./lib').SKILL_SOURCE).split(path.sep).join('/');
  for (const rel of [`${skillDir}/scripts/${ENTRY_POINT_FILE}`,
                     `${skillDir}/scripts/sdlc_core.py`,
                     `${skillDir}/routing.md`]) {
    assert.ok(pkg.files.includes(rel), `files[] must list ${rel}`);
  }
  // Dev-only assets must never reach a consumer.
  for (const rel of pkg.files) {
    assert.ok(!/scripts\/test_|\/evals\/|\/fixtures\//.test(rel),
      `files[] must not ship dev-only assets: ${rel}`);
  }
});

// --- T7: existing three clients unchanged (skill-target byte-equal) ---------
test('T7 skillTarget unchanged for claude/gemini/codex (default skills subdir)', () => {
  const fakeHome = path.join(os.tmpdir(), 'agy-test-home-fixed');
  const lib = freshLib({ __homedir: fakeHome });
  assert.strictEqual(
    lib.skillTarget(clientByKey(lib, 'claude')),
    path.join(fakeHome, '.claude', 'skills', lib.INSTALLED_SKILL_NAME),
  );
  assert.strictEqual(
    lib.skillTarget(clientByKey(lib, 'gemini')),
    path.join(fakeHome, '.gemini', 'skills', lib.INSTALLED_SKILL_NAME),
  );
  assert.strictEqual(
    lib.skillTarget(clientByKey(lib, 'codex')),
    path.join(fakeHome, '.codex', 'skills', lib.INSTALLED_SKILL_NAME),
  );
});

test('T7 existing three clients declare no skillsSubdir and no homeMarker', () => {
  const lib = freshLib({ __homedir: path.join(os.tmpdir(), 'agy-test-home-fixed') });
  for (const key of ['claude', 'gemini', 'codex']) {
    const c = clientByKey(lib, key);
    assert.strictEqual(c.skillsSubdir, undefined, `${key} must not set skillsSubdir`);
    assert.strictEqual(c.homeMarker, undefined, `${key} must not set homeMarker`);
  }
});

// --- T2: Antigravity skill-target under ~/.gemini/config/skills -------------
test('T2 skillTarget(antigravity) === ~/.gemini/config/skills/agentic-sdlc', () => {
  const fakeHome = path.join(os.tmpdir(), 'agy-test-home-fixed');
  const lib = freshLib({ __homedir: fakeHome });
  const anti = clientByKey(lib, 'antigravity');
  assert.strictEqual(anti.label, 'Google Antigravity');
  assert.strictEqual(anti.skillsSubdir, 'config/skills');
  assert.strictEqual(
    lib.skillTarget(anti),
    path.join(fakeHome, '.gemini', 'config', 'skills', lib.INSTALLED_SKILL_NAME),
  );
  // Distinct from the legacy gemini target (T2: no path overlap).
  assert.notStrictEqual(
    lib.skillTarget(anti),
    lib.skillTarget(clientByKey(lib, 'gemini')),
  );
});

// --- T1 (CRITICAL): bare ~/.gemini detects gemini but NOT antigravity -------
test('T1 bare ~/.gemini present: gemini TRUE, antigravity FALSE', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'agy-t1-'));
  try {
    fs.mkdirSync(path.join(tmp, '.gemini'), { recursive: true }); // bare home only
    // Make sure no env override leaks in and skews the fs-probe assertions.
    assert.ok(!process.env.GEMINI_HOME && !process.env.ANTIGRAVITY_HOME,
      'test env must not carry GEMINI_HOME/ANTIGRAVITY_HOME');
    const lib = freshLib({ __homedir: tmp });
    const gemini = clientByKey(lib, 'gemini');
    const anti = clientByKey(lib, 'antigravity');

    // The load-bearing collision guard, asserted UNCONDITIONALLY (never skipped):
    // the two entries diverge on the fs-existence probe. Bare ~/.gemini exists
    // (gemini's probe), but antigravity's homeMarker (~/.gemini/config/skills)
    // does NOT — so the mere existence of ~/.gemini can never install Antigravity.
    assert.ok(fs.existsSync(gemini.home), 'gemini probes bare ~/.gemini (exists)');
    assert.strictEqual(gemini.homeMarker, undefined, 'gemini has no homeMarker (probes bare home)');
    assert.ok(!fs.existsSync(anti.homeMarker),
      'antigravity homeMarker ~/.gemini/config/skills must NOT exist on bare ~/.gemini (T1)');

    // Full clientDetected() results. The cmd branch (`gemini`/`agy` on PATH) is
    // environment-dependent, so we assert the *bug case* directly: with cmd and
    // env absent, gemini must be TRUE (bare home) and antigravity FALSE (marker
    // absent). If a real binary is installed we skip only that binary's row, but
    // the fs-probe divergence above has already proven the collision is closed.
    if (!lib.commandExists(gemini.cmd)) {
      assert.strictEqual(lib.clientDetected(gemini), true, 'gemini detected on bare ~/.gemini');
    }
    if (!lib.commandExists(anti.cmd)) {
      assert.strictEqual(
        lib.clientDetected(anti), false,
        'antigravity must NOT detect on bare ~/.gemini (no config/skills, no env, no CLI)',
      );
    }
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});

// --- T3: antigravity detection matrix (marker OR env OR cmd) -----------------
test('T3 antigravity detected when ~/.gemini/config/skills exists', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'agy-t3a-'));
  try {
    fs.mkdirSync(path.join(tmp, '.gemini', 'config', 'skills'), { recursive: true });
    const lib = freshLib({ __homedir: tmp });
    assert.strictEqual(lib.clientDetected(clientByKey(lib, 'antigravity')), true);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});

test('T3 antigravity detected when ANTIGRAVITY_HOME is set', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'agy-t3b-'));
  const savedEnv = process.env.ANTIGRAVITY_HOME;
  try {
    // Case 1: ANTIGRAVITY_HOME points at a dir whose config/skills marker exists.
    const antiHome = path.join(tmp, 'custom-antigravity');
    fs.mkdirSync(path.join(antiHome, 'config', 'skills'), { recursive: true });
    const lib = freshLib({ __homedir: tmp, ANTIGRAVITY_HOME: antiHome });
    const anti = clientByKey(lib, 'antigravity');
    assert.strictEqual(anti.home, antiHome, 'ANTIGRAVITY_HOME overrides home (captured at load)');
    // clientDetected reads process.env live, so set it around the call.
    process.env.ANTIGRAVITY_HOME = antiHome;
    assert.strictEqual(lib.clientDetected(anti), true, 'detects via marker + env');

    // Case 2: env-var branch ALONE — point at a dir with no config/skills marker.
    const antiHome2 = path.join(tmp, 'env-only'); // never created on disk
    const lib2 = freshLib({ __homedir: tmp, ANTIGRAVITY_HOME: antiHome2 });
    process.env.ANTIGRAVITY_HOME = antiHome2; // freshLib restored it; re-set for the live call
    const anti2 = clientByKey(lib2, 'antigravity');
    assert.ok(!fs.existsSync(anti2.homeMarker), 'env-only case: marker dir must not exist');
    assert.strictEqual(lib2.clientDetected(anti2), true, 'detects via env-var branch alone');
  } finally {
    if (savedEnv === undefined) delete process.env.ANTIGRAVITY_HOME;
    else process.env.ANTIGRAVITY_HOME = savedEnv;
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});

test('antigravity carries an accurate reload string mentioning agy', () => {
  const lib = freshLib();
  const anti = clientByKey(lib, 'antigravity');
  assert.strictEqual(anti.cmd, 'agy');
  assert.strictEqual(anti.envVar, 'ANTIGRAVITY_HOME');
  assert.match(anti.reload, /agy/);
  // Must not be a copy of the gemini reload string (T8).
  assert.notStrictEqual(anti.reload, clientByKey(lib, 'gemini').reload);
});

// --- T2/T7: install -> uninstall round-trip in a stubbed HOME ---------------
// postinstall / preuninstall are run as child processes so their real fs side
// effects land under a throwaway temp HOME. We force detection of exactly the
// two colliding clients (gemini + antigravity) by creating both target markers.
test('T2/T7 install then uninstall: antigravity + gemini targets round-trip cleanly', () => {
  const tmpHome = fs.mkdtempSync(path.join(os.tmpdir(), 'agy-roundtrip-'));
  try {
    // Seed both markers so BOTH clients detect (env-independent):
    //  - bare ~/.gemini            -> gemini detects
    //  - ~/.gemini/config/skills   -> antigravity detects (homeMarker)
    fs.mkdirSync(path.join(tmpHome, '.gemini', 'config', 'skills'), { recursive: true });

    const childEnv = {
      ...process.env,
      HOME: tmpHome,
      USERPROFILE: tmpHome,
    };
    // Ensure no stray per-client overrides leak from the parent env.
    delete childEnv.CLAUDE_CONFIG_DIR;
    delete childEnv.GEMINI_HOME;
    delete childEnv.CODEX_HOME;
    delete childEnv.ANTIGRAVITY_HOME;

    const geminiTarget = path.join(tmpHome, '.gemini', 'skills', freshLib().INSTALLED_SKILL_NAME);
    const antiTarget = path.join(tmpHome, '.gemini', 'config', 'skills', freshLib().INSTALLED_SKILL_NAME);

    execFileSync(process.execPath, [POSTINSTALL], { env: childEnv, stdio: 'ignore' });

    assert.ok(fs.existsSync(path.join(antiTarget, 'SKILL.md')), 'antigravity target populated');
    assert.ok(fs.existsSync(path.join(geminiTarget, 'SKILL.md')), 'gemini target populated');
    // The two copies are distinct directories (T2: no overlap/aliasing).
    assert.notStrictEqual(antiTarget, geminiTarget);

    execFileSync(process.execPath, [PREUNINSTALL], { env: childEnv, stdio: 'ignore' });

    assert.ok(!fs.existsSync(antiTarget), 'antigravity target removed by preuninstall');
    assert.ok(!fs.existsSync(geminiTarget), 'gemini target removed by preuninstall');
  } finally {
    fs.rmSync(tmpHome, { recursive: true, force: true });
  }
});


// --- F-036: init wires the SessionStart orientation hook -------------------
// The unit exists because ENFORCEMENT.md §4 said "wire it on every project" and
// nothing did. Round 2 of these cases comes from an adversarial review that
// found the first round asserting too little: the cases marked (R2) each pin a
// defect that shipped past round 1.

const { wireOrientHook, orientHookCommand } = require('./lib');

function fakeSkill(home) {
  const dir = path.join(home, 'skills', INSTALLED_SKILL_NAME, 'scripts');
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, ENTRY_POINT_FILE), '# stub\n', 'utf8');
  return dir;
}

function sandbox(fn) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'f036-'));
  const cwd = path.join(tmp, 'project');
  const home = path.join(tmp, 'home');
  fs.mkdirSync(cwd, { recursive: true });
  fakeSkill(home);
  try {
    return fn({ tmp, cwd, client: { key: 'claude', home }, python: 'python' });
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

const readJson = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const localSettings = (cwd) => path.join(cwd, '.claude', 'settings.local.json');
const sharedSettings = (cwd) => path.join(cwd, '.claude', 'settings.json');
const writeSettings = (p, obj) => {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, typeof obj === 'string' ? obj : JSON.stringify(obj, null, 2), 'utf8');
};
const orientCommands = (p) => readJson(p).hooks.SessionStart
  // Mirrors findOrientHook: a hook object may sit directly in the array.
  .flatMap((g) => (Array.isArray(g.hooks) ? g.hooks : [g]).map((h) => h && h.command))
  .filter((c) => c && c.includes(' orient'));
// Vendor a validator the way a skill-authoring repo does.
const vendor = (cwd, dirName) => {
  const d = path.join(cwd, 'skills', dirName || INSTALLED_SKILL_NAME, 'scripts');
  fs.mkdirSync(d, { recursive: true });
  fs.writeFileSync(path.join(d, ENTRY_POINT_FILE), '# stub\n', 'utf8');
};

test('F-036: a fresh project gets a valid hook in the machine-specific file', () => {
  sandbox(({ cwd, client, python }) => {
    const r = wireOrientHook({ cwd, client, python });
    assert.strictEqual(r.code, 'wired');
    assert.strictEqual(r.file, 'settings.local.json');
    assert.ok(!fs.existsSync(sharedSettings(cwd)), 'shared settings untouched');
    const cmd = orientCommands(localSettings(cwd))[0];
    // (R2) the old test accepted `python "sdlc_check.py" orient`: assert the
    // command names the file we just proved exists, absolutely.
    const quoted = cmd.split('"')[1];
    assert.ok(path.isAbsolute(quoted), 'non-vendored command must be absolute');
    assert.ok(fs.existsSync(quoted), 'the command names a validator that exists');
  });
});

test('F-036: a vendored validator gets a portable command in the SHARED file', () => {
  sandbox(({ cwd, client, python }) => {
    vendor(cwd);
    const r = wireOrientHook({ cwd, client, python });
    assert.strictEqual(r.code, 'wired');
    assert.strictEqual(r.file, 'settings.json');
    const quoted = orientCommands(sharedSettings(cwd))[0].split('"')[1];
    assert.ok(!path.isAbsolute(quoted), 'repo-relative, so it survives a clone');
    assert.ok(fs.existsSync(path.join(cwd, quoted)), 'and it resolves from the repo root');
  });
});

test('F-036 (R2): this lens wins over a sibling vendored beside it', () => {
  sandbox(({ cwd, client, python }) => {
    vendor(cwd, 'aaa-someone-elses-skill');   // sorts first in readdir order
    vendor(cwd);
    const r = wireOrientHook({ cwd, client, python });
    assert.ok(r.command.includes(INSTALLED_SKILL_NAME),
      'readdir order must not decide which lens we orient: ' + r.command);
  });
});

test('F-036 (R2): the ENFORCEMENT §2 tools/ layout counts as vendored', () => {
  sandbox(({ cwd, client, python }) => {
    fs.mkdirSync(path.join(cwd, 'tools'), { recursive: true });
    fs.writeFileSync(path.join(cwd, 'tools', ENTRY_POINT_FILE), '# stub\n', 'utf8');
    const r = wireOrientHook({ cwd, client, python });
    assert.strictEqual(r.file, 'settings.json', 'a repo that followed §2 is vendored');
  });
});

test('F-036 (R2): a shell-metacharacter directory name never reaches a command', () => {
  sandbox(({ cwd, client, python }) => {
    // The name is repo-controlled and the command is shell-executed.
    vendor(cwd, '$(echo pwned)');
    const r = wireOrientHook({ cwd, client, python });
    assert.ok(!/[$`]/.test(r.command || ''),
      'injection reached the command: ' + r.command);
    // It must fall back to the absolute branch, not refuse everything.
    assert.strictEqual(r.code, 'wired');
    assert.strictEqual(r.file, 'settings.local.json');
  });
});

test('F-036: unrelated keys and foreign hooks survive the merge (T1)', () => {
  sandbox(({ cwd, client, python }) => {
    writeSettings(localSettings(cwd), {
      permissions: { allow: ['Bash(git status)'] },
      env: { FOO: 'bar' },
      hooks: { SessionStart: [{ hooks: [{ type: 'command', command: 'echo mine' }] }] },
    });
    assert.strictEqual(wireOrientHook({ cwd, client, python }).code, 'wired');
    const s = readJson(localSettings(cwd));
    assert.deepStrictEqual(s.permissions, { allow: ['Bash(git status)'] });
    assert.deepStrictEqual(s.env, { FOO: 'bar' });
    const all = s.hooks.SessionStart.flatMap((g) => g.hooks.map((h) => h.command));
    assert.ok(all.includes('echo mine'), "the user's own hook is still there");
    assert.strictEqual(orientCommands(localSettings(cwd)).length, 1);
  });
});

test('F-036 (R2): an unrecognised hooks shape is NEVER rewritten', () => {
  // Round 1 replaced these with {} and reported success: silent data loss.
  for (const shape of [
    { hooks: { SessionStart: { hooks: [{ type: 'command', command: 'echo MINE' }] } } },
    { hooks: { SessionStart: 'echo MINE' } },
    { hooks: ['echo MINE'] },
  ]) {
    sandbox(({ cwd, client, python }) => {
      writeSettings(localSettings(cwd), shape);
      const before = fs.readFileSync(localSettings(cwd), 'utf8');
      const r = wireOrientHook({ cwd, client, python });
      assert.strictEqual(r.code, 'malformed', JSON.stringify(shape));
      assert.strictEqual(fs.readFileSync(localSettings(cwd), 'utf8'), before,
        'a shape we do not understand is not a shape we may replace');
    });
  }
});

test('F-036: running twice adds exactly one hook (T2)', () => {
  sandbox(({ cwd, client, python }) => {
    assert.strictEqual(wireOrientHook({ cwd, client, python }).code, 'wired');
    assert.strictEqual(wireOrientHook({ cwd, client, python }).code, 'already');
    assert.strictEqual(orientCommands(localSettings(cwd)).length, 1);
  });
});

test('F-036 (R2): vendoring LATER does not add a second hook in the other file', () => {
  sandbox(({ cwd, client, python }) => {
    assert.strictEqual(wireOrientHook({ cwd, client, python }).code, 'wired');
    vendor(cwd);                       // the team adopts the CI gate
    const r = wireOrientHook({ cwd, client, python });
    assert.strictEqual(r.code, 'already',
      'the hook in the other settings layer must still be seen');
    assert.ok(!fs.existsSync(sharedSettings(cwd)), 'no second hook in the shared file');
  });
});

test('F-036 (R2): a hook placed directly in the array is recognised', () => {
  sandbox(({ cwd, client, python }) => {
    const abs = path.join(client.home, 'skills', INSTALLED_SKILL_NAME, 'scripts', ENTRY_POINT_FILE);
    writeSettings(localSettings(cwd), {
      hooks: { SessionStart: [{ type: 'command', command: 'python "' + abs + '" orient' }] },
    });
    assert.strictEqual(wireOrientHook({ cwd, client, python }).code, 'already');
    assert.strictEqual(orientCommands(localSettings(cwd)).length, 1);
  });
});

test('F-036: a hook that is wired but DEAD is reported, not called done (T2b)', () => {
  sandbox(({ cwd, client, python }) => {
    writeSettings(localSettings(cwd), {
      hooks: { SessionStart: [{ hooks: [{ type: 'command',
        command: 'python "skills/gone-skill/scripts/' + ENTRY_POINT_FILE + '" orient' }] }] },
    });
    const r = wireOrientHook({ cwd, client, python });
    assert.strictEqual(r.code, 'broken');
    assert.ok(r.existing.includes('gone-skill'));
  });
});

test('F-036 (R2): a DEAD hook whose interpreter is quoted is still BROKEN', () => {
  // Round 1 extracted the FIRST quoted token -- the interpreter, which exists --
  // and reported a dead hook as healthy.
  sandbox(({ cwd, client, python }) => {
    // A real interpreter path: it EXISTS but names no validator, which is what
    // made the first-quoted-token rule report a dead hook as healthy.
    const interp = path.join(client.home, 'python.exe');
    fs.writeFileSync(interp, 'stub', 'utf8');
    writeSettings(localSettings(cwd), {
      hooks: { SessionStart: [{ hooks: [{ type: 'command',
        command: '"' + interp + '" "skills/gone/scripts/' + ENTRY_POINT_FILE + '" orient' }] }] },
    });
    assert.strictEqual(wireOrientHook({ cwd, client, python }).code, 'broken');
  });
});

test('F-036 (R2): a WORKING hook with no quotes is not called broken', () => {
  sandbox(({ cwd, client, python }) => {
    vendor(cwd);
    writeSettings(localSettings(cwd), {
      hooks: { SessionStart: [{ hooks: [{ type: 'command',
        command: 'python3 skills/' + INSTALLED_SKILL_NAME + '/scripts/' + ENTRY_POINT_FILE + ' orient' }] }] },
    });
    assert.strictEqual(wireOrientHook({ cwd, client, python }).code, 'already');
  });
});

test('F-036 (R2): a hook naming no known validator is unverifiable, not broken', () => {
  sandbox(({ cwd, client, python }) => {
    writeSettings(localSettings(cwd), {
      hooks: { SessionStart: [{ hooks: [{ type: 'command',
        command: 'my-wrapper.sh ' + ENTRY_POINT_FILE.replace('.py', '') + ' orient' }] }] },
    });
    const r = wireOrientHook({ cwd, client, python });
    assert.ok(['unverifiable', 'wired'].includes(r.code), r.code);
    assert.notStrictEqual(r.code, 'broken', 'never assert breakage we cannot establish');
  });
});

test('F-036: malformed JSON is left byte-identical (T1)', () => {
  sandbox(({ cwd, client, python }) => {
    const junk = '{ "permissions": { /* a comment makes this JSONC */ } }';
    writeSettings(localSettings(cwd), junk);
    const r = wireOrientHook({ cwd, client, python });
    assert.strictEqual(r.code, 'malformed');
    assert.strictEqual(fs.readFileSync(localSettings(cwd), 'utf8'), junk);
  });
});

test('F-036: no Python and no validator both refuse to write (T3)', () => {
  sandbox(({ cwd, client }) => {
    assert.strictEqual(wireOrientHook({ cwd, client, python: null }).code, 'no-python');
    assert.ok(!fs.existsSync(localSettings(cwd)));
  });
  sandbox(({ cwd, python }) => {
    const empty = { key: 'claude', home: path.join(os.tmpdir(), 'f036-no-such-home') };
    assert.strictEqual(wireOrientHook({ cwd, client: empty, python }).code, 'no-validator');
    assert.ok(!fs.existsSync(localSettings(cwd)));
  });
});

test('F-036 (R2): docsLabel reaches the statusMessage', () => {
  sandbox(({ cwd, client, python }) => {
    wireOrientHook({ cwd, client, python, docsLabel: 'mkt_docs' });
    const h = readJson(localSettings(cwd)).hooks.SessionStart[0].hooks[0];
    assert.match(h.statusMessage, /mkt_docs/);
    assert.strictEqual(h.timeout, 10);
  });
});

test('F-036: --hybrid rides on the option', () => {
  sandbox(({ cwd, client, python }) => {
    assert.ok(!wireOrientHook({ cwd, client, python }).command.includes('--hybrid'));
  });
  sandbox(({ cwd, client, python }) => {
    assert.ok(wireOrientHook({ cwd, client, python, hybrid: true }).command.includes('--hybrid'));
  });
});

test('F-036 (R2): orientHookCommand is the single command shape', () => {
  assert.strictEqual(orientHookCommand('python', '/a/b.py', false), 'python "/a/b.py" orient');
  assert.strictEqual(orientHookCommand('py', 'x.py', true), 'py "x.py" orient --hybrid');
});
