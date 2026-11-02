#!/usr/bin/env node
// Main holds what is published (release guide, step 9): before a package is
// published, the commit it is packed from must be on origin/main and its tag
// must be on origin naming that commit. npm versions are immutable, so a
// publish from a commit main does not have cannot be undone (1.50.0 was
// published from a branch never merged).
//
// Dev-only: absent from every package.json `files`. publish_all.bat runs it
// for each package it is about to publish, from the package's directory:
//   node scripts/release_remote.js --tag vX.Y.Z
// Exit 0 when both hold, 1 otherwise. Reads the remote; changes nothing but
// the origin/main tracking ref.

const { execFileSync } = require('child_process');

const MAIN = 'main';
const TAG_NAME = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;

function git(cwd, args) {
  return execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
}

// The commit a remote tag names: the peeled `^{}` line for an annotated tag,
// the plain line for a lightweight one; '' when the remote has no such tag.
function remoteTagCommit(cwd, tag) {
  const out = git(cwd, ['ls-remote', '--tags', 'origin', `refs/tags/${tag}`, `refs/tags/${tag}^{}`]);
  let plain = '';
  for (const line of out.split('\n').filter(Boolean)) {
    const [sha, ref] = line.split('\t');
    if (ref.endsWith('^{}')) return sha;
    plain = sha;
  }
  return plain;
}

function run({ cwd = process.cwd(), tag, log = console.log }) {
  if (!tag || !TAG_NAME.test(tag)) {
    log(`[FAIL] not a tag name: ${tag || '(none)'}`);
    return 1;
  }
  let head;
  try {
    head = git(cwd, ['rev-parse', 'HEAD']);
    git(cwd, ['fetch', '-q', 'origin', `+refs/heads/${MAIN}:refs/remotes/origin/${MAIN}`]);
  } catch (e) {
    log(`[FAIL] cannot read HEAD or fetch origin/${MAIN}: ${String(e.stderr || e.message).trim()}`);
    return 1;
  }
  let ok = true;
  try {
    git(cwd, ['merge-base', '--is-ancestor', head, `origin/${MAIN}`]);
  } catch (e) {
    log(`[FAIL] HEAD ${head.slice(0, 8)} is not on origin/${MAIN}: push or merge ${MAIN} first.`);
    ok = false;
  }
  let remote;
  try {
    remote = remoteTagCommit(cwd, tag);
  } catch (e) {
    log(`[FAIL] cannot list the tags on origin: ${String(e.stderr || e.message).trim()}`);
    return 1;
  }
  if (!remote) {
    log(`[FAIL] tag ${tag} is not on origin: push it first.`);
    ok = false;
  } else if (remote !== head) {
    log(`[FAIL] tag ${tag} on origin names ${remote.slice(0, 8)}, not HEAD ${head.slice(0, 8)}.`);
    ok = false;
  }
  if (ok) log(`  [ok] HEAD ${head.slice(0, 8)} is on origin/${MAIN} and tag ${tag} names it.`);
  return ok ? 0 : 1;
}

if (require.main === module) {
  const argv = process.argv.slice(2);
  const i = argv.indexOf('--tag');
  process.exitCode = run({ tag: i >= 0 ? argv[i + 1] : undefined });
}

module.exports = { remoteTagCommit, run };
