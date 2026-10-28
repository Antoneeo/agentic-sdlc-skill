#!/usr/bin/env node
// Dev-only battery for whats_new.js (F-070). NOT shipped: absent from every
// package.json `files`. Run it with:
//   node scripts/test_whats_new.js

const { test } = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const wn = require('./whats_new');

const SCRIPT = path.join(__dirname, 'whats_new.js');
const BOUNDS = '<!-- whats-new:begin -->\n<!-- whats-new:end -->';

function pkg(dir, name, version, changelog) {
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'package.json'), JSON.stringify({ name, version }));
  fs.writeFileSync(path.join(dir, 'CHANGELOG.md'), changelog);
  fs.writeFileSync(path.join(dir, 'README.md'), `# ${name}\n\nIntro.\n\n${BOUNDS}\n\n## Install\n`);
}

// Two packages at different versions: the root one with notes, the other without.
function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'whats-new-'));
  pkg(root, '@x/code', '2.0.0',
    "# Changelog\n\n## [2.0.0] - 2026-10-28\n\n### What's new\nCode notes.\n\n### Added\n- detail\n\n## [1.0.0]\n");
  pkg(path.join(root, 'distributions', 'kb'), '@x/kb', '1.5.0',
    "# Changelog\n\n## [1.5.0] - 2026-10-01\n\n### Added\n- detail\n");
  return root;
}

function run(root, opts = {}) {
  const lines = [];
  const code = wn.run(Object.assign({ root, log: (l) => lines.push(l) }, opts));
  return { code, out: lines.join('\n') };
}

test('discover: the root package and every distributions/* package, nothing else', () => {
  const root = fixture();
  fs.mkdirSync(path.join(root, 'distributions', 'not-a-package'));
  assert.deepStrictEqual(wn.discover(root).map((d) => path.relative(root, d)),
    ['', path.join('distributions', 'kb')]);
});

test('render: comment, ## heading with the version, the body, an absolute link per package', () => {
  const text = wn.render('2.0.0', 'Body.', 'distributions/kb');
  const lines = text.split('\n');
  assert.match(lines[0], /^<!-- .*CHANGELOG\.md.* -->$/);
  assert.strictEqual(lines[1], "## What's new in 2.0.0");
  assert.ok(text.includes('\n\nBody.\n\n'));
  assert.match(lines[lines.length - 1],
    /\(https:\/\/github\.com\/Antoneeo\/agentic-sdlc-skill\/blob\/main\/distributions\/kb\/CHANGELOG\.md\)/);
  assert.match(wn.render('1.0.0', 'B.', ''), /blob\/main\/CHANGELOG\.md\)/);
});

test('check: a README not yet written differs for the package with notes, agrees for the one without', () => {
  const root = fixture();
  const r = run(root);
  assert.strictEqual(r.code, 1);
  assert.match(r.out, /\[FAIL\] @x\/code 2\.0\.0/);
  assert.match(r.out, /\[ok\] @x\/kb 1\.5\.0/);
});

test('write: each package gets its own version and text, then the check agrees', () => {
  const root = fixture();
  assert.strictEqual(run(root, { write: true }).code, 0);
  const code = fs.readFileSync(path.join(root, 'README.md'), 'utf8');
  assert.ok(code.includes("## What's new in 2.0.0\n\nCode notes."));
  assert.ok(!code.includes('detail'));
  const kb = fs.readFileSync(path.join(root, 'distributions', 'kb', 'README.md'), 'utf8');
  assert.ok(kb.includes(BOUNDS), 'a version without notes keeps an empty region');
  assert.strictEqual(run(root).code, 0);
});

test('check: a hand edit inside the region fails naming the package', () => {
  const root = fixture();
  run(root, { write: true });
  const f = path.join(root, 'README.md');
  fs.writeFileSync(f, fs.readFileSync(f, 'utf8').replace('Code notes.', 'Edited.'));
  const r = run(root);
  assert.strictEqual(r.code, 1);
  assert.match(r.out, /\[FAIL\] @x\/code 2\.0\.0: .*--write/);
});

test('--require: a package whose version has no notes fails, one with notes passes', () => {
  const root = fixture();
  run(root, { write: true });
  const kb = run(root, { require: true, dirs: [path.join(root, 'distributions', 'kb')] });
  assert.strictEqual(kb.code, 1);
  assert.match(kb.out, /\[FAIL\] @x\/kb 1\.5\.0: .*no "What's new"/);
  assert.strictEqual(run(root, { require: true, dirs: [root] }).code, 0);
});

test('a package whose version has no CHANGELOG section fails', () => {
  const root = fixture();
  fs.writeFileSync(path.join(root, 'package.json'), JSON.stringify({ name: '@x/code', version: '3.0.0' }));
  const r = run(root, { dirs: [root] });
  assert.strictEqual(r.code, 1);
  assert.match(r.out, /no section/);
});

test('write: a distributions/* package links its own CHANGELOG', () => {
  const root = fixture();
  const kb = path.join(root, 'distributions', 'kb');
  fs.writeFileSync(path.join(kb, 'CHANGELOG.md'),
    "# Changelog\n\n## [1.5.0] - 2026-10-01\n\n### What's new\nKB notes.\n");
  assert.strictEqual(run(root, { write: true, dirs: [kb] }).code, 0);
  assert.ok(fs.readFileSync(path.join(kb, 'README.md'), 'utf8').includes(
    '(https://github.com/Antoneeo/agentic-sdlc-skill/blob/main/distributions/kb/CHANGELOG.md)'));
});

test('write: a version with no CHANGELOG section leaves the README byte-identical', () => {
  const root = fixture();
  // A filled region first: an empty one would stay identical even if the error path wrote.
  assert.strictEqual(run(root, { write: true, dirs: [root] }).code, 0);
  assert.ok(fs.readFileSync(path.join(root, 'README.md'), 'utf8').includes('Code notes.'));
  fs.writeFileSync(path.join(root, 'package.json'), JSON.stringify({ name: '@x/code', version: '3.0.0' }));
  const before = fs.readFileSync(path.join(root, 'README.md'));
  assert.strictEqual(run(root, { write: true, dirs: [root] }).code, 1);
  assert.ok(fs.readFileSync(path.join(root, 'README.md')).equals(before));
});

test('an unreadable package is one [FAIL] line, and the other packages are still checked', () => {
  const root = fixture();
  fs.unlinkSync(path.join(root, 'CHANGELOG.md'));
  const r = run(root);
  assert.strictEqual(r.code, 1);
  assert.match(r.out, /^\[FAIL\] .*CHANGELOG\.md/m);
  assert.match(r.out, /\[ok\] @x\/kb 1\.5\.0/);
});

test('command line: an unknown option or a --root without value is refused with usage', () => {
  for (const args of [['--requre'], ['--root']]) {
    assert.throws(() => execFileSync(process.execPath, [SCRIPT, ...args], { stdio: 'pipe' }),
      (e) => e.status === 2 && /usage/i.test(String(e.stderr)) && !/at .*whats_new\.js/.test(String(e.stderr)));
  }
});

test('command line: exit status and named directories', () => {
  const root = fixture();
  const kbDir = path.join(root, 'distributions', 'kb');
  execFileSync(process.execPath, [SCRIPT, '--root', root, kbDir]);
  assert.throws(() => execFileSync(process.execPath, [SCRIPT, '--root', root, '--require', kbDir],
    { stdio: 'pipe' }), (e) => e.status === 1);
});

test('this repository: every package README agrees with its CHANGELOG', () => {
  const root = path.resolve(__dirname, '..');
  const r = run(root);
  assert.strictEqual(r.code, 0, r.out);
  assert.strictEqual(wn.discover(root).length, 4);
});
