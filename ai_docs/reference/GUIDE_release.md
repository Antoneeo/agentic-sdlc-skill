---
description: How to release a new version of the skill package (npm + git tag + main merge). Consult before any version bump, tag or publish.
status: CURRENT
source: Release runbook approved by Antonio Pinto (distilled from the v1.8.0 release session, 2026-07-02).
distilled_from: ai_docs/reference/.sources/release-runbook-73c9c99d.md
source_hash: 73c9c99d04d323e298b2f798acf74c9dfc5cbf7559f2d2d46e4142d979fe5ffe
---
# Guide: Release

## When this applies
[source: release-runbook-73c9c99d.md#preconditions]
Shipping a version of `@antoneeo/agentic-sdlc-skill`. Enter only when: the unit
is DONE (review PASS, battery green, ADR accepted), `CHANGELOG.md` carries an
`## [Unreleased - X.Y.Z]` section, the repo's `check --hybrid` is CLEAN, and
`npm view @antoneeo/agentic-sdlc-skill version` shows the target version is not
already published.

## How to do a release
[source: release-runbook-73c9c99d.md#git-sequence]
Order: bump → verify → commit → push → merge → tag → publish.
1. Bump THREE places in one commit: `package.json` version,
   `gemini-extension.json` version, CHANGELOG heading
   (`[Unreleased - X.Y.Z]` → `[X.Y.Z] - YYYY-MM-DD`). (snapshot §Version bump points)
2. Any NEW support file since the last release MUST be in `package.json`
   `files` — it is an allowlist, and `postinstall.js` can only copy what the
   tarball contains. Update README's support-files bullet and Runtime Shape
   tree too. (snapshot §Packaging completeness, §README alignment)
3. Commit on the feature branch as `Release vX.Y.Z: <short title>` (bumps +
   CHANGELOG + README + handoff together); push the branch.
4. Merge to main: `gh` CLI is not installed on this machine — GitHub web PR,
   or user-authorized direct push.
5. Tag the release commit BY SHA (`git tag vX.Y.Z <sha>`), push the tag.
   Ref pushes never touch the working tree — always safe.
6. `npm publish` is the USER's step (2FA). Prepare a clean checkout and hand off.

## How to verify it is done right
[source: release-runbook-73c9c99d.md#verification-battery]
Before any commit/tag/publish, three checks:
1. `npm pack --dry-run --json` — expected files in; `__pycache__` and
   `.sources/` out.
2. init.js smoke: `node scripts/init.js` in an empty scratch dir → all
   templates extracted; fresh `sdlc_check.py check` CLEAN (3 boilerplate DRAFT
   warnings expected).
3. `sdlc_check.py check --hybrid --root <repo>` CLEAN.
After publish: `npm view @antoneeo/agentic-sdlc-skill version` returns the new
version.

## What to watch out for
[source: release-runbook-73c9c99d.md#known-traps]
- **devPNT db locks**: with the devPNT MCP server running, git checkout/merge/
  stash in the primary worktree fail on `.devpnt/*.db`
  (`unable to unlink old '...': Invalid argument`), and the dbs re-drift after
  every commit. Branch-crossing work goes in a `git worktree add` checkout, or
  waits for a server restart.
- **Never chain the tag after a fallible merge** (`git merge; git tag` put
  v1.8.0 on the wrong commit once). Tag explicitly by SHA.
- **npm publish stops at `EOTP`** — only the user can complete it.
- **PowerShell 5.1**: no `&&`; `npm pack --dry-run` lists files on stderr —
  use `--json`.

## Post-release
[source: release-runbook-73c9c99d.md#post-release]
Record version + date + next step in `ai_docs/audit/handoff.md` (in the release
commit when possible); update devPNT milestone/Action Plan state if the release
closes a unit; regenerate indexes (`sdlc_check.py index`) if canonical docs
were added.
