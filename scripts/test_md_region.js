#!/usr/bin/env node
// Dev-only battery for md_region.js (F-070). NOT shipped: absent from every
// package.json `files`, like test_clients.js. Run it with:
//   node scripts/test_md_region.js

const { test } = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const region = require('./md_region');

const LOG = [
  '# Changelog',
  '',
  '## [Unreleased]',
  '',
  "### What's new",
  'unreleased notes',
  '',
  '## [1.2.0] - 2026-10-01',
  '',
  "### What's new",
  '',
  '| File | Skill | Who reads it |',
  '|---|---|---|',
  '| `a.md` | code | the agent |',
  '',
  '### Added',
  '- internal detail',
  '',
  '## [1.1.0-beta.3] - 2026-09-01',
  '',
  "### What's new",
  'beta notes',
  '',
  '## [1.1.0] - 2026-08-01',
  '',
  '### Fixed',
  '- something',
  '',
].join('\n');

const TITLE = "What's new";

test('extract: the subsection of the matching version, up to the next heading', () => {
  const r = region.extractSubsection(LOG, '1.2.0', TITLE);
  assert.strictEqual(r.status, 'found');
  assert.strictEqual(r.body, '| File | Skill | Who reads it |\n|---|---|---|\n| `a.md` | code | the agent |');
});

test('extract: a version without the subsection is absent', () => {
  assert.strictEqual(region.extractSubsection(LOG, '1.1.0', TITLE).status, 'absent');
});

test('extract: an empty subsection is absent', () => {
  const log = '## [2.0.0]\n\n### What\'s new\n\n### Added\n- x\n';
  assert.strictEqual(region.extractSubsection(log, '2.0.0', TITLE).status, 'absent');
});

test('extract: a version with no section is an error', () => {
  const r = region.extractSubsection(LOG, '9.9.9', TITLE);
  assert.strictEqual(r.status, 'error');
  assert.match(r.reason, /no section/);
});

test('extract: [Unreleased] never answers for a version', () => {
  assert.strictEqual(region.extractSubsection(LOG, 'Unreleased', TITLE).status, 'error');
});

test('extract: a -beta.N version is matched literally, not as a pattern', () => {
  const r = region.extractSubsection(LOG, '1.1.0-beta.3', TITLE);
  assert.strictEqual(r.status, 'found');
  assert.strictEqual(r.body, 'beta notes');
  assert.strictEqual(region.extractSubsection(LOG, '1.1.0-beta', TITLE).status, 'error');
});

test('extract: a duplicated version heading is ambiguous', () => {
  const log = '## [1.0.0]\n### What\'s new\na\n## [1.0.0] - again\n### What\'s new\nb\n';
  const r = region.extractSubsection(log, '1.0.0', TITLE);
  assert.strictEqual(r.status, 'error');
  assert.match(r.reason, /ambiguous/);
});

test('extract: two subsections with the title in one section are ambiguous', () => {
  const log = '## [1.0.0]\n### What\'s new\na\n### What\'s new\nb\n';
  const r = region.extractSubsection(log, '1.0.0', TITLE);
  assert.strictEqual(r.status, 'error');
  assert.match(r.reason, /ambiguous/);
});

test('extract: headings inside a code fence do not end the subsection', () => {
  const log = '## [1.0.0]\n### What\'s new\nrun:\n```\n## [0.0.1] not a heading\n```\nend\n### Added\n';
  const r = region.extractSubsection(log, '1.0.0', TITLE);
  assert.strictEqual(r.body, 'run:\n```\n## [0.0.1] not a heading\n```\nend');
});

test('extract: a ``` line inside a ~~~ fence does not close it', () => {
  const log = '## [1.0.0]\n### What\'s new\n~~~\n```\n~~~\nafter\n### Added\nx\n';
  const r = region.extractSubsection(log, '1.0.0', TITLE);
  assert.strictEqual(r.body, '~~~\n```\n~~~\nafter');
});

test('extract: a shorter fence does not close a longer one', () => {
  const log = '## [1.0.0]\n### What\'s new\n````\n```\n### not a heading\n````\nend\n### Added\nx\n';
  assert.strictEqual(region.extractSubsection(log, '1.0.0', TITLE).body,
    '````\n```\n### not a heading\n````\nend');
});

test('extract: CRLF input gives the same body as LF', () => {
  const r = region.extractSubsection(LOG.replace(/\n/g, '\r\n'), '1.2.0', TITLE);
  assert.strictEqual(r.body, region.extractSubsection(LOG, '1.2.0', TITLE).body);
});

const DOC = '# Title\n\nIntro.\n\n<!-- notes:begin -->\nold\n<!-- notes:end -->\n\n## Next\n';

test('sync: replaces only what lies between the bounds', () => {
  const r = region.syncRegion(DOC, 'notes', 'new\nlines');
  assert.strictEqual(r.status, 'differs');
  assert.strictEqual(r.text, '# Title\n\nIntro.\n\n<!-- notes:begin -->\nnew\nlines\n<!-- notes:end -->\n\n## Next\n');
});

test('sync: empty content leaves the two bounds on consecutive lines', () => {
  const r = region.syncRegion(DOC, 'notes', '');
  assert.strictEqual(r.text, '# Title\n\nIntro.\n\n<!-- notes:begin -->\n<!-- notes:end -->\n\n## Next\n');
});

test('sync: identical content agrees and the text is unchanged', () => {
  const r = region.syncRegion(DOC, 'notes', 'old');
  assert.strictEqual(r.status, 'agrees');
  assert.strictEqual(r.text, DOC);
});

test('sync: CRLF document keeps CRLF, and agrees with the same content in LF', () => {
  const crlf = DOC.replace(/\n/g, '\r\n');
  assert.strictEqual(region.syncRegion(crlf, 'notes', 'old').status, 'agrees');
  const r = region.syncRegion(crlf, 'notes', 'new');
  assert.strictEqual(r.text, crlf.replace('\r\nold\r\n', '\r\nnew\r\n'));
});

test('sync: a mixed-ending document keeps every line outside the region as it was', () => {
  const doc = 'a\r\nb\n<!-- notes:begin -->\r\n<!-- notes:end -->\r\nc\n';
  const r = region.syncRegion(doc, 'notes', 'x\ny');
  assert.strictEqual(r.text, 'a\r\nb\n<!-- notes:begin -->\r\nx\r\ny\r\n<!-- notes:end -->\r\nc\n');
});

test('sync: a region holding a blank line does not agree with empty content', () => {
  const doc = '<!-- notes:begin -->\n\n<!-- notes:end -->\n';
  const r = region.syncRegion(doc, 'notes', '');
  assert.strictEqual(r.status, 'differs');
  assert.strictEqual(r.text, '<!-- notes:begin -->\n<!-- notes:end -->\n');
});

for (const [label, doc] of [
  ['missing', '# Title\n'],
  ['missing end', '<!-- notes:begin -->\nx\n'],
  ['duplicated', '<!-- notes:begin -->\n<!-- notes:end -->\n<!-- notes:begin -->\n<!-- notes:end -->\n'],
  ['reversed', '<!-- notes:end -->\nx\n<!-- notes:begin -->\n'],
]) {
  test(`sync: ${label} bounds are an error`, () => {
    const r = region.syncRegion(doc, 'notes', 'x');
    assert.strictEqual(r.status, 'error');
    assert.match(r.reason, /bounds/);
  });
}

test('sync: a bound must be a whole line, not text that quotes it', () => {
  const doc = 'see `<!-- notes:begin -->` in prose\n<!-- notes:begin -->\n<!-- notes:end -->\n';
  assert.strictEqual(region.syncRegion(doc, 'notes', 'x').status, 'differs');
});

function scratch(text) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'md-region-'));
  const file = path.join(dir, 'README.md');
  fs.writeFileSync(file, text);
  return { dir, file };
}

test('write: writes the file, then a second write changes nothing', () => {
  const { dir, file } = scratch(DOC);
  assert.strictEqual(region.writeRegion(file, 'notes', 'new').status, 'written');
  const after = fs.readFileSync(file, 'utf8');
  assert.match(after, /notes:begin -->\nnew\n<!-- notes:end/);
  assert.strictEqual(region.writeRegion(file, 'notes', 'new').status, 'agrees');
  assert.strictEqual(fs.readFileSync(file, 'utf8'), after);
  assert.deepStrictEqual(fs.readdirSync(dir), ['README.md']);
});

test('write: refuses on bad bounds and leaves the file byte-identical', () => {
  const bad = '# Title\n<!-- notes:end -->\n<!-- notes:begin -->\n';
  const { dir, file } = scratch(bad);
  assert.strictEqual(region.writeRegion(file, 'notes', 'x').status, 'error');
  assert.strictEqual(fs.readFileSync(file, 'utf8'), bad);
  assert.deepStrictEqual(fs.readdirSync(dir), ['README.md']);
});

for (const failing of ['writeFileSync', 'renameSync']) {
  test(`write: a failing ${failing} leaves the file unchanged and no temporary file`, () => {
    const { dir, file } = scratch(DOC);
    const removed = [];
    const fsImpl = Object.assign({}, fs, {
      [failing]: (...args) => {
        if (failing === 'writeFileSync') fs.writeFileSync(args[0], 'partial');
        throw Object.assign(new Error('simulated'), { code: 'EPERM' });
      },
      unlinkSync: (p) => { removed.push(p); fs.unlinkSync(p); },
    });
    const r = region.writeRegion(file, 'notes', 'new', fsImpl);
    assert.strictEqual(r.status, 'error');
    assert.strictEqual(fs.readFileSync(file, 'utf8'), DOC);
    assert.deepStrictEqual(fs.readdirSync(dir), ['README.md']);
    if (failing === 'renameSync') assert.strictEqual(removed.length, 1, 'cleanup goes through the given fs');
  });
}
