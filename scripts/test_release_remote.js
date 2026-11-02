#!/usr/bin/env node
// Dev-only battery for release_remote.js. NOT shipped: absent from every
// package.json `files`. Run it with:
//   node scripts/test_release_remote.js

const { test } = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const rr = require('./release_remote');

function git(cwd, ...args) {
  return execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
}

// A bare origin and a clone with one commit pushed to main.
function fixture() {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'release-remote-'));
  const origin = path.join(base, 'origin.git');
  const work = path.join(base, 'work');
  git(base, 'init', '-q', '--bare', '-b', 'main', origin);
  git(base, 'clone', '-q', origin, work);
  git(work, 'config', 'user.email', 't@example.invalid');
  git(work, 'config', 'user.name', 'T');
  git(work, 'checkout', '-q', '-b', 'main');
  commit(work, 'first');
  git(work, 'push', '-q', 'origin', 'main');
  return work;
}

function commit(work, msg) {
  fs.writeFileSync(path.join(work, 'f.txt'), msg);
  git(work, 'add', 'f.txt');
  git(work, 'commit', '-q', '-m', msg);
}

function run(cwd, tag) {
  const lines = [];
  const code = rr.run({ cwd, tag, log: (l) => lines.push(l) });
  return { code, out: lines.join('\n') };
}

test('ok: HEAD on origin/main and its tag on the remote at HEAD', () => {
  const w = fixture();
  git(w, 'tag', 'v1.0.0');
  git(w, 'push', '-q', 'origin', 'v1.0.0');
  const r = run(w, 'v1.0.0');
  assert.strictEqual(r.code, 0, r.out);
  assert.match(r.out, /\[ok\]/);
});

test('ok: an annotated tag is compared by the commit it names', () => {
  const w = fixture();
  git(w, 'tag', '-a', '-m', 'release', 'v1.0.0');
  git(w, 'push', '-q', 'origin', 'v1.0.0');
  assert.strictEqual(run(w, 'v1.0.0').code, 0);
});

test('fail: HEAD committed but main not pushed (the 1.50.0 case)', () => {
  const w = fixture();
  commit(w, 'release');
  git(w, 'tag', 'v1.0.0');
  git(w, 'push', '-q', 'origin', 'v1.0.0');
  const r = run(w, 'v1.0.0');
  assert.strictEqual(r.code, 1);
  assert.match(r.out, /origin\/main/);
});

test('fail: HEAD on a branch pushed but never merged into main', () => {
  const w = fixture();
  git(w, 'checkout', '-q', '-b', 'feat');
  commit(w, 'release');
  git(w, 'push', '-q', 'origin', 'feat');
  git(w, 'tag', 'v1.0.0');
  git(w, 'push', '-q', 'origin', 'v1.0.0');
  const r = run(w, 'v1.0.0');
  assert.strictEqual(r.code, 1);
  assert.match(r.out, /origin\/main/);
});

test('fail: the tag exists only locally', () => {
  const w = fixture();
  git(w, 'tag', 'v1.0.0');
  const r = run(w, 'v1.0.0');
  assert.strictEqual(r.code, 1);
  assert.match(r.out, /v1\.0\.0/);
  assert.match(r.out, /not on origin/);
});

test('fail: the remote tag names another commit', () => {
  const w = fixture();
  git(w, 'tag', 'v1.0.0');
  git(w, 'push', '-q', 'origin', 'v1.0.0');
  commit(w, 'later');
  git(w, 'push', '-q', 'origin', 'main');
  const r = run(w, 'v1.0.0');
  assert.strictEqual(r.code, 1);
  assert.match(r.out, /names .* not HEAD/);
});

test('fail: a tag name that is not a plain ref is refused before git sees it', () => {
  const w = fixture();
  const r = run(w, '--upload-pack=x');
  assert.strictEqual(r.code, 1);
});
