---
description: How to release a new version of the skill package (npm + git tag + main merge). Consult before any version bump, tag or publish.
status: CURRENT
source: Release runbook approved by Antonio Pinto (v1.8.0 release session, 2026-07-02; amended same day — commit+tag+push via git_push_tag.bat, plus the script's observed re-run behavior; amended 2026-07-03 (M4) — eval battery added to the verification battery + dev-only eval-harness packaging note; amended 2026-08-01 — README alignment covers all three distributions plus the family document, and `mark` closes the step instead of opening it).
distilled_from: ai_docs/reference/.sources/release-runbook-2792f160.md
source_hash: 49b46d13ee390bb4aa047e58e42f9ac6a0b3cf56f7f28875da870832f07c3e81
---
# Guide: Release

## When this applies
[source: release-runbook-2792f160.md#preconditions]
Shipping a version of `@antoneeo/agentic-sdlc-skill`. Enter only when: the unit
is DONE (review PASS, battery green, ADR accepted), `CHANGELOG.md` carries an
`## [Unreleased - X.Y.Z]` section, the repo's `check --hybrid` is CLEAN, and
`npm view @antoneeo/agentic-sdlc-skill version` shows the target version is not
already published.

## How to do a release
[source: release-runbook-2792f160.md#git-sequence]
Order: bump → verify → script (commit+tag+push) → verify tag → merge → publish.
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
[source: release-runbook-2792f160.md#verification-battery]
Before any commit/tag/publish, four checks:
1. `npm pack --dry-run --json` — expected files in; `__pycache__`, `.sources/`
   snapshots, and the dev-only eval harness (`test_*.py`, `evals/`) NOT listed.
2. init.js smoke: `node <repo>/scripts/init.js` in an empty scratch dir → all
   templates extracted; fresh `sdlc_check.py check` on the scratch dir CLEAN
   (3 boilerplate DRAFT warnings expected).
3. `sdlc_check.py check --hybrid --root <repo>` CLEAN.
4. Skill eval battery (deterministic release gate, ENFORCEMENT §5):
   `python -m unittest discover -s skills/agentic-sdlc-skill/scripts -p "test_*.py"`
   all green (aggregates plan + orient + skill-invariants). A failing eval blocks
   the release; if `test_indexes_idempotent` fails, run `sdlc_check.py index` and re-run.
After publish: `npm view @antoneeo/agentic-sdlc-skill version` returns the new
version.

## What to watch out for
[source: release-runbook-2792f160.md#known-traps]
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
- **PowerShell 5.1**: no `&&`; `npm pack --dry-run` lists files on stderr —
  use `--json`.

## Post-release
[source: release-runbook-2792f160.md#post-release]
Record version + date + next step in `ai_docs/audit/handoff.md` (in the release
commit when possible); update devPNT milestone/Action Plan state if the release
closes a unit; regenerate indexes (`sdlc_check.py index`) if canonical docs
were added.
