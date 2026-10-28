---
description: How to release a new version of the skill package (npm + git tag + main merge). Consult before any version bump, tag or publish.
status: CURRENT
source: Release runbook approved by Antonio Pinto (v1.8.0 release session, 2026-07-02; amended same day — commit+tag+push via git_push_tag.bat, plus the script's observed re-run behavior; amended 2026-07-03 (M4) — eval battery added to the verification battery + dev-only eval-harness packaging note; amended 2026-08-01 — README alignment covers all three distributions plus the family document, and `mark` closes the step instead of opening it; amended 2026-08-25 — publish_all.bat is the publish step, with its skip semantics and its bump-commit-tag-first precondition; amended 2026-09-25 — plain `check` beside the hybrid one, `mark` inside the release commit, one tag per package, a pending 2FA is pending, not failed; amended 2026-10-08 — Course latest follows the newest published release for default installation; amended 2026-10-17 — Course publishes on latest like the stable packages, so no separate promotion; amended 2026-10-19 — `mark --note` writes each release's dated entry in project_notes.md; tags are set right before the publish; amended 2026-10-27 (F-070) — user-facing "What's new" per package, mirrored into the README, approved by the owner before the tag, required by publish_all.bat; amended 2026-10-28 — the notes lead with the benefit, and what a user must do is explained in full).
distilled_from: ai_docs/reference/.sources/release-runbook-course-creator.md
source_hash: cb125faed48766e56b2d6271ab32161a3d76ccde7c62153d8f62d0b051a3db4a
---
# Guide: Release

## When this applies
[source: release-runbook-course-creator.md#preconditions]
Shipping a version of one of the four `@antoneeo` skill packages. Enter only when: the unit
is DONE (review PASS, battery green, ADR accepted), `CHANGELOG.md` carries an
`## [Unreleased]` section, the repo's `check --hybrid` AND plain `check`
are CLEAN, and
`npm view @antoneeo/agentic-sdlc-skill version` shows the target version is not
already published.

## How to do a release
[source: release-runbook-course-creator.md#git-sequence]
Order: bump → verify → mark → script (commit+tag+push) → package tags → verify
tags → merge → publish.
1. Bump FOUR places in one commit: `package.json` version,
   `gemini-extension.json` version, **`SKILL.md` frontmatter `version:`**,
   CHANGELOG heading (`## [Unreleased]` → `## [X.Y.Z] - YYYY-MM-DD`).
   (snapshot §Version bump points; the SKILL.md point is the product's own,
   added 2026-08-03 — an installed skill carries no package.json, so its
   frontmatter is the only place a reader can see which build they have.
   Forgetting it fails the battery: `test_the_installed_skill_says_which_
   version_it_is` asserts all bump points agree.)
   **Then the users' notes, for each bumped package, in this order**
   [source: release-runbook-course-creator.md#user-facing-whats-new--2026-10-27]:
   - Open its `## [X.Y.Z]` section with `### What's new`, written for the people who
     install the package, not for the agent. **Lead with the benefit**
     [source: release-runbook-course-creator.md#notes-lead-with-the-benefit--2026-10-28]:
     what the version brings them, grouped by benefit, one or two plain sentences
     each — what it lets them do or spares them. Then the **"New files" table** when
     the version adds files (file, skill, who reads it). Commands, flags, formats and
     states appear only where a user must act on them, and **what a user must do is
     explained in full**: who it concerns and how they can tell, why (what goes wrong
     otherwise), the exact steps with the commands or files involved, and how to check
     it worked. No internals only the agent reads, no personal or
     employer references. While `audit/project_notes.md` carries a pending
     first-notes entry naming the package, its notes also cover what that entry says,
     marked as such; remove the package's name there in the same release commit.
   - `node scripts/whats_new.js --write`, then
     `node scripts/whats_new.js --require <each bumped package dir>`: every bumped
     package must report `[ok]`. This check before the tag is the real gate;
     `publish_all.bat`'s refusal is only its backstop.
   - Review ruling: the README region is the same text as the CHANGELOG lines (the
     check proves it), so they are judged together. Notes that state nothing the
     units' reviewed work does not already state are NOT DUE — one REVIEW_LOG row,
     verdict `NOT DUE: release metadata; CHANGELOG What's new and the README region
     mirrored from it; mirror check agrees`. Notes that add a claim (an upgrade
     instruction nobody reviewed, say) get a scoped review of that part first.
   - **Stop for the owner**: show the notes of each bumped package, with the ruling,
     and wait for approval before tagging. A change to approved notes is approved
     again. The npm page keeps this text until the next version.
2. Any NEW support file since the last release MUST be in `package.json`
   `files` — it is an allowlist, and `postinstall.js` can only copy what the
   tarball contains. Update README's support-files bullet and Runtime Shape
   tree too — **in all four distributions** (repo root for the code lens,
   `distributions/kb-agentic-skill/`, `distributions/mkt-agentic-sdlc/`,
   `distributions/course-creator/`): each
   `README.md` IS that package's npm page. The same duty covers
   `strategic/skill_family_agent_workflows.md`. When the doctrine changed,
   `mark` on the `skills/`/`distributions/` audit areas is the LAST step of
   closure, not the first: do not record the analysis while a derived document
   still says something else. (snapshot §Packaging completeness, §README alignment)
3. Inspect the staging scope: the script stages EVERYTHING (`git add .`).
   If unrelated presentation work remains, stage the release files explicitly and
   perform the same commit/tag/push sequence with that inspected set. Publish from
   a clean `git archive` export of the exact tagged commit, preserving the primary
   checkout. (snapshot §Stable and beta release amendment — 2026-10-02)
4. With the bump still uncommitted, `mark skills/agentic-sdlc-skill/
   distributions/ skills/ --note "release X.Y.Z: <short title>"`: the dirty tree
   records a timestamp, so `audit_plan.md` rides in the release commit under the tag,
   and `--note` writes the release's dated entry at the top of
   `audit/project_notes.md` in the same commit — the date is never copied by hand.
   Marking after the commit forces a second commit and the tag no longer points at
   `HEAD`. [source: release-runbook-course-creator.md#release-note-written-by-mark--2026-10-19-supersedes-the-entry-above]
   **Tag right before the publish, not when the release is prepared**: a commit landing
   after the tag and before the publish leaves the tag naming a tree npm never sees. If
   one did, move the tag (it was never published: delete it locally and on the remote,
   re-tag `HEAD`) or bump. [source: release-runbook-course-creator.md#tag-right-before-the-publish--2026-10-19]
5. From the feature branch run
   `git_push_tag.bat "Release vX.Y.Z: <short title>" vX.Y.Z` — one step:
   stage all, commit, tag, push branch + tag. It creates the code tag only.
6. Tag each other bumped package on the SAME commit and push:
   `git tag kb-vX.Y.Z` / `git tag mkt-vX.Y.Z` / `git tag course-vX.Y.Z`, then
   `git push origin kb-vX.Y.Z mkt-vX.Y.Z course-vX.Y.Z`.
7. VERIFY every tag: `git rev-parse <tag>` == `git rev-parse HEAD`. If wrong,
   `git tag -d <tag>`, fix, re-run (delete the remote tag too if it was
   pushed: `git push origin :refs/tags/<tag>`).
8. Merge to main: `gh` CLI is not installed on this machine — GitHub web PR,
   or user-authorized direct push.
9. Publish with `publish_all.bat` from the clean tagged content. Publication is
   authorized in this session; browser 2FA remains the USER's step. It checks all four packages in one run and
   **skips any already on the registry at that version**, so a single-package
   release is normal: the others that did not change are skipped, not failures,
   and an interrupted run is resumed by re-running. It packs the WORKING TREE,
   so run it from the clean tagged checkout — step 5 must have happened first.
   Every package publishes on `latest`: none declares `publishConfig.tag`, Course
   included (its version keeps the `-beta.N` suffix). The script passes the channel
   explicitly and verifies that dist-tag; a package that declared another channel
   would get the isolation guard below. A beta suffix alone does not select the
   channel. (snapshot §Publish, §publish_all.bat,
   §Stable and beta release amendment — 2026-10-02)

## How to verify it is done right
[source: release-runbook-course-creator.md#verification-battery]
Before any commit/tag/publish, five checks:
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
5. Users' notes [source: release-runbook-course-creator.md#user-facing-whats-new--2026-10-27]:
   `node scripts/whats_new.js --require <each bumped package dir>` reports `[ok]` for
   every bumped package, and `node scripts/test_md_region.js` and
   `node scripts/test_whats_new.js` are green (the last one also checks that every
   package README agrees with its CHANGELOG).
After publish: verify each version and its `dist-tags.latest`. Course needs no separate
promotion since 2026-10-17 (see the policy below).
On the first course publication (2026-10-02), npm also assigned latest despite
explicit beta routing, and authenticated removal returned E400. The publisher
rejects beta-only verification when the new prerelease is also latest, and rejects
failed/empty tag queries. The owner replaced the beta-only requirement on
2026-10-08 with the default-install policy below. Do not automatically unpublish
or move other channels. (snapshot §Stable and beta release amendment — 2026-10-02)

## Course default-install policy
[source: release-runbook-course-creator.md#course-default-install-amendment--2026-10-08]
[source: release-runbook-course-creator.md#course-on-the-normal-channel--2026-10-17]

The owner requires default installation to receive the newest Course version
(2026-10-08), through the normal publication (2026-10-17). Course declares no
`publishConfig.tag`, so `publish_all.bat` publishes it with `--tag latest` and
verifies latest, like the stable packages; there is no separate promotion step. The
version keeps its `-beta.N` suffix and the README its experimental statement: the
channel does not establish stability or learning efficacy. The `beta` dist-tag no
longer advances and is left on the last version it named. A version published before
this change on beta only (0.1.0-beta.4) needs one owner-run promotion,
`npm dist-tag add @antoneeo/course-creator@<version> latest` (browser 2FA), then a
registry check. Do not remove latest or move other package channels.

## What to watch out for
[source: release-runbook-course-creator.md#known-traps]
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
- **The four packages version independently**, so most releases touch one of
  them. That is the case the script is built for: it skips the others by
  comparing the local version against the registry first. (Before 2026-08-25 it
  did not, and aborted on the first already-published package instead.)
- **PowerShell 5.1**: no `&&`; `npm pack --dry-run` lists files on stderr —
  use `--json`.
- **`publish_all.bat` refuses a package without users' notes** — after the registry
  skip, it runs `whats_new.js --require` on each package it is about to publish and
  stops on `[FAIL]` before that package's `npm publish`. A package earlier in its
  order (code, kb, mkt, course) may already have been published in that run, so a
  refusal here means the pre-tag check of step 1 was skipped or the tree changed after
  it: fix the notes, move the unpublished packages' tags, re-run.
  [source: release-runbook-course-creator.md#user-facing-whats-new--2026-10-27]

## Post-release
[source: release-runbook-course-creator.md#post-release]
When the publish is verified, add the registry versions to the body of the release's
dated entry that step 4 wrote in `audit/project_notes.md` (keep its opener as written).
Record version + date + next step in `ai_docs/audit/handoff.md` (in the release
commit when possible); update devPNT milestone/Action Plan state if the release
closes a unit; regenerate indexes (`sdlc_check.py index`) if canonical docs
were added.
