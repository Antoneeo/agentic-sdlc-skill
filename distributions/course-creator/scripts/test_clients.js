#!/usr/bin/env node
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const lib = require('./lib');

test('the four supported clients install the course skill under its own name', () => {
  assert.deepEqual(lib.CLIENTS.map(c => c.key),
    ['claude', 'gemini', 'codex', 'antigravity']);
  for (const c of lib.CLIENTS) {
    assert.equal(path.basename(lib.skillTarget(c)), 'course-creator');
  }
  assert.equal(lib.SELF_LENS, 'course');
});

test('init creates a course-default project once and preserves the owner edits', () => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'course-init-'));
  const home = path.join(temp, 'home');
  const project = path.join(temp, 'project');
  fs.mkdirSync(home);
  fs.mkdirSync(project);
  const env = { ...process.env, HOME: home, USERPROFILE: home,
    CLAUDE_CONFIG_DIR: path.join(home, '.claude') };
  try {
    execFileSync(process.execPath, [path.join(__dirname, 'init.js')],
      { cwd: project, env, stdio: 'pipe' });
    const readme = path.join(project, 'ai_docs', 'README.md');
    assert.match(fs.readFileSync(readme, 'utf8'), /^---\r?\ndefault_domain: course/m);
    assert.match(fs.readFileSync(path.join(project, '.cursorrules'), 'utf8'), /@antoneeo\/course-creator@beta/);
    fs.writeFileSync(readme, 'owner edition\n');
    execFileSync(process.execPath, [path.join(__dirname, 'init.js')],
      { cwd: project, env, stdio: 'pipe' });
    assert.equal(fs.readFileSync(readme, 'utf8'), 'owner edition\n');
  } finally { fs.rmSync(temp, { recursive: true, force: true }); }
});

test('install and uninstall preserve unowned or modified files', () => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'course-install-'));
  const target = path.join(temp, 'skills', 'course-creator');
  try {
    assert.equal(lib.installOwned(target).code, 'installed');
    assert.ok(fs.existsSync(path.join(target, 'SKILL.md')));
    fs.writeFileSync(path.join(target, 'private.md'), 'keep me');
    fs.appendFileSync(path.join(target, 'SKILL.md'), '\nowner note\n');
    assert.equal(lib.uninstallOwned(target).code, 'removed');
    assert.ok(fs.existsSync(path.join(target, 'private.md')));
    assert.match(fs.readFileSync(path.join(target, 'SKILL.md'), 'utf8'), /owner note/);
  } finally { fs.rmSync(temp, { recursive: true, force: true }); }
});

test('an existing unowned skill directory is not overwritten', () => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'course-unowned-'));
  const target = path.join(temp, 'course-creator');
  fs.mkdirSync(target);
  fs.writeFileSync(path.join(target, 'SKILL.md'), 'foreign');
  try {
    assert.equal(lib.installOwned(target).code, 'unowned');
    assert.equal(fs.readFileSync(path.join(target, 'SKILL.md'), 'utf8'), 'foreign');
  } finally { fs.rmSync(temp, { recursive: true, force: true }); }
});

test('a symlinked ownership marker cannot redirect install or uninstall', (t) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'course-marker-'));
  const target = path.join(temp, 'course-creator');
  const outside = path.join(temp, 'outside.json');
  fs.mkdirSync(target);
  fs.writeFileSync(outside, JSON.stringify({ skill: 'course-creator', files: {} }));
  try {
    try { fs.symlinkSync(outside, path.join(target, '.course-creator-install.json')); }
    catch { t.skip('symlinks unavailable'); return; }
    assert.equal(lib.installOwned(target).code, 'unowned');
    assert.equal(lib.uninstallOwned(target).code, 'unowned');
    assert.equal(fs.readFileSync(outside, 'utf8'),
      JSON.stringify({ skill: 'course-creator', files: {} }));
  } finally { fs.rmSync(temp, { recursive: true, force: true }); }
});
