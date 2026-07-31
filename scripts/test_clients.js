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
test('TS11 init seeds default_domain in ai_docs/README.md and never overwrites it', () => {
  const proj = fs.mkdtempSync(path.join(os.tmpdir(), 'sdlc-init-proj-'));
  try {
    runInit(proj);
    const readme = path.join(proj, 'ai_docs', 'README.md');
    const first = fs.readFileSync(readme, 'utf8');
    assert.match(first, /^---\r?\ndefault_domain: code\r?\n---/,
      'README frontmatter must open with default_domain: code');

    // A project that edited its own default must survive a second init (create-only).
    fs.writeFileSync(readme, first.replace('default_domain: code', 'default_domain: knowledge'), 'utf8');
    runInit(proj);
    assert.match(fs.readFileSync(readme, 'utf8'), /default_domain: knowledge/,
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

    runInit(proj, { siblingDirs: ['kb-agentic'] });

    assert.strictEqual(fs.readFileSync(path.join(proj, 'CLAUDE.md'), 'utf8'), sentinel,
      'init must never overwrite a user/sibling-authored protocol pointer (T1)');
    const note = fs.readFileSync(path.join(proj, 'AGENTIC_MULTI_LENS.md'), 'utf8');
    assert.match(note, /kb-agentic/, 'the note names the detected sibling');
    assert.match(note, /routing\.md/, 'the note points at the domain router');
    assert.match(note, /Merge step owed/, 'a pre-existing pointer means a merge is owed');
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

// --- T7: existing three clients unchanged (skill-target byte-equal) ---------
test('T7 skillTarget unchanged for claude/gemini/codex (default skills subdir)', () => {
  const fakeHome = path.join(os.tmpdir(), 'agy-test-home-fixed');
  const lib = freshLib({ __homedir: fakeHome });
  assert.strictEqual(
    lib.skillTarget(clientByKey(lib, 'claude')),
    path.join(fakeHome, '.claude', 'skills', 'agentic-sdlc'),
  );
  assert.strictEqual(
    lib.skillTarget(clientByKey(lib, 'gemini')),
    path.join(fakeHome, '.gemini', 'skills', 'agentic-sdlc'),
  );
  assert.strictEqual(
    lib.skillTarget(clientByKey(lib, 'codex')),
    path.join(fakeHome, '.codex', 'skills', 'agentic-sdlc'),
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
    path.join(fakeHome, '.gemini', 'config', 'skills', 'agentic-sdlc'),
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

    const geminiTarget = path.join(tmpHome, '.gemini', 'skills', 'agentic-sdlc');
    const antiTarget = path.join(tmpHome, '.gemini', 'config', 'skills', 'agentic-sdlc');

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
