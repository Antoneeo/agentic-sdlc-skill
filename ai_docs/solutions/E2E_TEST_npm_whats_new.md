---
feature: F-070
analysis: ANALYSIS_npm_whats_new.md
---
# E2E test: "What's new" on the npm pages

## What changed, in user terms

Each package's npm page gets a "What's new in <version>" section after its introduction,
taken from that version's CHANGELOG and approved by the owner before release. The
"Shared project memory" section moves from the top of the code, KB and marketing pages
to just after their features. The publish run refuses a package whose page lacks its
notes.

## Environment and preconditions

- The repository at the merged commit, on Windows with Node and Python on PATH.
- The probe folder `ai_docs/solutions/harness_npm_whats_new/` (npm stand-in; nothing is
  ever sent to the registry by these scenarios).
- S4 and S5 happen at each package's next real release, run by the owner; nothing is
  published for testing.

## New-behavior scenarios

### S1 — A7: every page agrees with its CHANGELOG today
Steps: 1. From the repository root, `node scripts/whats_new.js`.
Expected: four `[ok] … README agrees` lines, exit status 0. Each README holds
`<!-- whats-new:begin -->` and `<!-- whats-new:end -->` on consecutive lines, right
after the introduction.
Result:

### S2 — A1, A3: notes appear on the page, and a hand edit is caught
Steps: 1. In a scratch copy of the repository, add under `## [1.49.0] - 2026-10-27` of
`CHANGELOG.md` a `### What's new` with one line of text. 2. `node scripts/whats_new.js
--write`. 3. Open `README.md`. 4. Change a word inside the new section and run
`node scripts/whats_new.js` again.
Expected: after 2, the README shows "## What's new in 1.49.0", the line, and "Full
history" linking `…/blob/main/CHANGELOG.md`; nothing else in the file changed. After 4,
`[FAIL] @antoneeo/agentic-sdlc-skill 1.49.0: README.md disagrees …`, exit status 1.
Result:

### S3 — A6: the publish run refuses a package without notes
Steps: 1. From the repository root:
`ai_docs\solutions\harness_npm_whats_new\run_publish_probe.cmd none <absolute repo path> <absolute log path>`.
Expected: `[FAIL] @antoneeo/agentic-sdlc-skill 1.49.0: no "What's new" …`, then
`[FAIL] … not published`; the log has no `publish` line.
Result:

### S4 — A8, A9: the release step (at each package's next release)
Steps: 1. Bump a package per `GUIDE_release.md`. 2. Watch for the notes being shown to
the owner before any tag.
Expected: the agent shows the package's `### What's new` — "New files" table first when
files were added, the 1.49.0-wave summary in the first notes of each package — with the
review ruling, and tags nothing before the owner approves. The package leaves the
pending note in `audit/project_notes.md` in the release commit.
Result:

### S5 — FS1 on npm (after each package's next publish)
Steps: 1. Open the package's page on npmjs.com.
Expected: the introduction, then "What's new in <the version npm shows>", then the
features; no `<!--` text anywhere on the page; the "Full history" link opens the
package's CHANGELOG on GitHub.
Result:

## Regression scenarios

### R1 — re-running a publish skips what is already published
Steps: 1. `run_publish_probe.cmd all <absolute repo path> <absolute log path>`.
Expected: four "already on the registry - skipped" lines, verify `[ok]` ×4, no
`publish` line in the log.
Result:

### R2 — the pages read as before apart from the two moves
Steps: 1. `python ai_docs/solutions/harness_npm_whats_new/probe_readmes.py <base ref>`
with the commit before F-070 as base.
Expected: four `[ok]` lines: each moved block identical, and undoing the change gives
the base README exactly. The permission phrase ("use in your own project") is still in
each README.
Result:

### R3 — the packages ship the same files
Steps: 1. In each package folder, `npm pack --dry-run --json`.
Expected: no `md_region`, `whats_new` or `test_` script in any file list.
Result:

## Already covered by automated tests

`node scripts/test_md_region.js` (extraction, region bounds, line endings, whole-or-absent
writes) and `node scripts/test_whats_new.js` (discovery, rendering, `--write`,
`--require`, and this repository agreeing); the four Python batteries
(`test_skill_invariants.py` keeps the README permission phrase).
