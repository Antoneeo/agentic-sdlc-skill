---
description: How to release a new version of the skill package (npm + git tag + main merge). Consult before any version bump, tag or publish.
status: CURRENT
source: Release runbook approved by Antonio Pinto (v1.8.0 release session, 2026-07-02; amended same day — commit+tag+push via git_push_tag.bat, plus the script's observed re-run behavior; amended 2026-07-03 (M4) — eval battery added to the verification battery + dev-only eval-harness packaging note; amended 2026-08-01 — README alignment covers all three distributions plus the family document, and `mark` closes the step instead of opening it; amended 2026-08-25 — publish_all.bat is the publish step, with its skip semantics and its bump-commit-tag-first precondition; amended 2026-09-25 — plain `check` beside the hybrid one, `mark` inside the release commit, one tag per package, a pending 2FA is pending, not failed).
distilled_from: ai_docs/reference/.sources/release-runbook-a62d4cd6.md
source_hash: a62d4cd6f2b67f44b2e0c2d292391a6f1ea1d9a9ac10c34e070572af80ceac6a
---
# Guide: Release

## When this applies
[source: release-runbook-a62d4cd6.md#preconditions]
Shipping a version of `@antoneeo/agentic-sdlc-skill`. Enter only when: the unit
is DONE (review PASS, battery green, ADR accepted), `CHANGELOG.md` carries an
`## [Unreleased - X.Y.Z]` section, the repo's `check --hybrid` AND plain `check`
are CLEAN, and
`npm view @antoneeo/agentic-sdlc-skill version` shows the target version is not
already published.

## How to do a release
[source: release-runbook-a62d4cd6.md#git-sequence]
Order: bump → verify → mark → script (commit+tag+push) → package tags → verify
tags → merge → publish.
1. Bump FOUR places in one commit: `package.json` version,
   `gemini-extension.json` version, **`SKILL.md` frontmatter `version:`**,
   CHANGELOG heading (`[Unreleased - X.Y.Z]` → `[X.Y.Z] - YYYY-MM-DD`).
   (snapshot §Version bump points; the SKILL.md point is the product's own,
   added 2026-08-03 — an installed skill carries no package.json, so its
   frontmatter is the only place a reader can see which build they have.
   Forgetting it fails the battery: `test_the_installed_skill_says_which_
   version_it_is` asserts all bump points agree.)
2. Any NEW support file since the last release MUST be in `package.json`
   `files` — it is an allowlist, and `postinstall.js` can only copy what the
   tarball contains. Update README's support-files bullet and Runtime Shape
   tree too — **in all three distributions** (repo root for the code lens,
   `distributions/kb-agentic-skill/`, `distributions/mkt-agentic-sdlc/`): each
   `README.md` IS that package's npm page. The same duty covers
   `strategic/skill_family_agent_workflows.md`. When the doctrine changed,
   `mark` on the `skills/`/`distributions/` audit areas is the LAST step of
   closure, not the first: do not record the analysis while a derived document
   still says something else. (snapshot §Packaging completeness, §README alignment)
3. Working tree must contain ONLY the release edits (bumps + CHANGELOG +
   README + handoff): the script stages EVERYTHING (`git add .`).
4. With the bump still uncommitted, `mark skills/agentic-sdlc-skill/
   distributions/ skills/`: the dirty tree records a timestamp, so
   `audit_plan.md` rides in the release commit under the tag. Marking after the
   commit forces a second commit and the tag no longer points at `HEAD`.
5. From the feature branch run
   `git_push_tag.bat "Release vX.Y.Z: <short title>" vX.Y.Z` — one step:
   stage all, commit, tag, push branch + tag. It creates the code tag only.
6. Tag each other bumped package on the SAME commit and push:
   `git tag kb-vX.Y.Z` / `git tag mkt-vX.Y.Z`, then
   `git push origin kb-vX.Y.Z mkt-vX.Y.Z`.
7. VERIFY every tag: `git rev-parse <tag>` == `git rev-parse HEAD`. If wrong,
   `git tag -d <tag>`, fix, re-run (delete the remote tag too if it was
   pushed: `git push origin :refs/tags/<tag>`).
8. Merge to main: `gh` CLI is not installed on this machine — GitHub web PR,
   or user-authorized direct push.
9. Publish with `publish_all.bat` from the repo root — the USER's step (2FA
   opens a browser per package). It does all three packages in one run and
   **skips any already on the registry at that version**, so a single-package
   release is normal: the two that did not change are skipped, not failures,
   and an interrupted run is resumed by re-running. It packs the WORKING TREE,
   so run it from the clean tagged checkout — step 5 must have happened first.
   (snapshot §Publish, §publish_all.bat)

## How to verify it is done right
[source: release-runbook-a62d4cd6.md#verification-battery]
Before any commit/tag/publish, four checks:
1. `npm pack --dry-run --json` — expected files in; `__pycache__`, `.sources/`
   snapshots, and the dev-only eval harness (`test_*.py`, `evals/`) NOT listed.
2. init.js smoke: `node <repo>/scripts/init.js` in an empty scratch dir → all
   templates extracted; fresh `sdlc_check.py check` on the scratch dir CLEAN
   (3 boilerplate DRAFT warnings expected).
3. `sdlc_check.py check --hybrid --root <repo>` CLEAN, and plain
   `sdlc_check.py check --root <repo>` CLEAN — `--hybrid` skips audit-plan
   staleness here, so only the plain run sees areas the bump left unmarked.
4. Skill eval battery (deterministic release gate, ENFORCEMENT §5):
   `python -m unittest discover -s skills/agentic-sdlc-skill/scripts -p "test_*.py"`
   all green (aggregates plan + orient + skill-invariants). A failing eval blocks
   the release; if `test_indexes_idempotent` fails, run `sdlc_check.py index` and re-run.
After publish: `npm view @antoneeo/agentic-sdlc-skill version` returns the new
version.

## What to watch out for
[source: release-runbook-a62d4cd6.md#known-traps]
- **devPNT db locks**: with the devPNT MCP server running, git checkout/merge/
  stash in the primary worktree fail on `.devpnt/*.db`
  (`unable to unlink old '...': Invalid argument`), and the dbs re-drift after
  every commit. Committing on the CURRENT branch (what the script does) is
  fine; branch-crossing work goes in a `git worktree add` checkout, or waits
  for a server restart.
- **`git_push_tag.bat` does not stop on a failed commit** — the tag then lands
  on the previous HEAD (the wrong-tag failure hit manually in the v1.8.0 run).
  Always run the tag verification (step 5 above).
- **Re-run with an existing tag**: `fatal: tag 'vX.Y.Z' already exists`, but
  the script continues and pushes anyway; the tag is NOT moved. Fine if it
  already points at the release commit; otherwise `git tag -d` and re-tag
  (delete the remote tag too if pushed).
- **npm publish stops at `EOTP`** — only the user can complete it.
- **A pending 2FA is not a failure**: each package waits for its own browser
  authorization, possibly minutes after the previous one (2026-09-25: mkt landed
  4.5 min after kb). Read the registry only after the script's final verify
  block; before it, a missing package is pending.
- **`publish_all.bat` packs the working tree, not the tag.** Publishing before
  the bump is committed and tagged ships a tree that no tag names, and npm
  versions are immutable — there is no undo. Bump, commit, tag, THEN publish.
- **The three packages version independently**, so most releases touch one of
  them. That is the case the script is built for: it skips the others by
  comparing the local version against the registry first. (Before 2026-08-25 it
  did not, and aborted on the first already-published package instead.)
- **PowerShell 5.1**: no `&&`; `npm pack --dry-run` lists files on stderr —
  use `--json`.

## Post-release
[source: release-runbook-a62d4cd6.md#post-release]
Record version + date + next step in `ai_docs/audit/handoff.md` (in the release
commit when possible); update devPNT milestone/Action Plan state if the release
closes a unit; regenerate indexes (`sdlc_check.py index`) if canonical docs
were added.
