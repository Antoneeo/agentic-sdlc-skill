---
description: How to release a new version of the skill package (npm + git tag + main merge). Consult before any version bump, tag or publish.
status: CURRENT
source: Release runbook approved by Antonio Pinto (v1.8.0 release session, 2026-07-02; amended same day — commit+tag+push via git_push_tag.bat).
distilled_from: ai_docs/reference/.sources/release-runbook-a1044dca.md
source_hash: a1044dca22c8bae5c5f89c2e697a5328bf7514fe96177d2919a12ea0661a0749
---
# Guide: Release

## When this applies
[source: release-runbook-a1044dca.md#preconditions]
Shipping a version of `@antoneeo/agentic-sdlc-skill`. Enter only when: the unit
is DONE (review PASS, battery green, ADR accepted), `CHANGELOG.md` carries an
`## [Unreleased - X.Y.Z]` section, the repo's `check --hybrid` is CLEAN, and
`npm view @antoneeo/agentic-sdlc-skill version` shows the target version is not
already published.

## How to do a release
[source: release-runbook-a1044dca.md#git-sequence]
Order: bump → verify → script (commit+tag+push) → verify tag → merge → publish.
1. Bump THREE places in one commit: `package.json` version,
   `gemini-extension.json` version, CHANGELOG heading
   (`[Unreleased - X.Y.Z]` → `[X.Y.Z] - YYYY-MM-DD`). (snapshot §Version bump points)
2. Any NEW support file since the last release MUST be in `package.json`
   `files` — it is an allowlist, and `postinstall.js` can only copy what the
   tarball contains. Update README's support-files bullet and Runtime Shape
   tree too. (snapshot §Packaging completeness, §README alignment)
3. Working tree must contain ONLY the release edits (bumps + CHANGELOG +
   README + handoff): the script stages EVERYTHING (`git add .`).
4. From the feature branch run
   `git_push_tag.bat "Release vX.Y.Z: <short title>" vX.Y.Z` — one step:
   stage all, commit, tag, push branch + tag.
5. VERIFY the tag: `git rev-parse vX.Y.Z` == `git rev-parse HEAD`. If wrong,
   `git tag -d vX.Y.Z`, fix, re-run (delete the remote tag too if it was
   pushed: `git push origin :refs/tags/vX.Y.Z`).
6. Merge to main: `gh` CLI is not installed on this machine — GitHub web PR,
   or user-authorized direct push.
7. `npm publish` is the USER's step (2FA). Prepare a clean checkout and hand
   off. (snapshot §Publish)

## How to verify it is done right
[source: release-runbook-a1044dca.md#verification-battery]
Before any commit/tag/publish, three checks:
1. `npm pack --dry-run --json` — expected files in; `__pycache__` and
   `.sources/` out.
2. init.js smoke: `node <repo>/scripts/init.js` in an empty scratch dir → all
   templates extracted; fresh `sdlc_check.py check` on the scratch dir CLEAN
   (3 boilerplate DRAFT warnings expected).
3. `sdlc_check.py check --hybrid --root <repo>` CLEAN.
After publish: `npm view @antoneeo/agentic-sdlc-skill version` returns the new
version.

## What to watch out for
[source: release-runbook-a1044dca.md#known-traps]
- **devPNT db locks**: with the devPNT MCP server running, git checkout/merge/
  stash in the primary worktree fail on `.devpnt/*.db`
  (`unable to unlink old '...': Invalid argument`), and the dbs re-drift after
  every commit. Committing on the CURRENT branch (what the script does) is
  fine; branch-crossing work goes in a `git worktree add` checkout, or waits
  for a server restart.
- **`git_push_tag.bat` does not stop on a failed commit** — the tag then lands
  on the previous HEAD (the wrong-tag failure hit manually in the v1.8.0 run).
  Always run the tag verification (step 5 above).
- **npm publish stops at `EOTP`** — only the user can complete it.
- **PowerShell 5.1**: no `&&`; `npm pack --dry-run` lists files on stderr —
  use `--json`.

## Post-release
[source: release-runbook-a1044dca.md#post-release]
Record version + date + next step in `ai_docs/audit/handoff.md` (in the release
commit when possible); update devPNT milestone/Action Plan state if the release
closes a unit; regenerate indexes (`sdlc_check.py index`) if canonical docs
were added.
