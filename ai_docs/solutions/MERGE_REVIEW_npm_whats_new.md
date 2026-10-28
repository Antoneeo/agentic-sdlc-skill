---
feature: F-070
analysis: ANALYSIS_npm_whats_new.md
base: main
---
# Merge review: "What's new" on the npm pages

## Purpose

Each package's npm page shows what changed in its published version, written for the
people who install it — the Vision's Goal "installable, upgradable and maintainable by the
people who use it" (`ANALYSIS_npm_whats_new.md` §Feature Vision). Nothing a user sees
changes until each package's next release carries notes.

## What to review

`sdlc_check.py review-map --base HEAD` on the uncommitted tree (2026-10-28), pasted
verbatim except for two rows removed: `docs-site.zip` and `npm` at the repository root are
untracked files that predate this unit and are not part of it — do not stage them.

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +5/-0 | REVIEW | review |
| `README.md` | M | +18/-16 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +5/-0 | REVIEW | review |
| `distributions/course-creator/README.md` | M | +3/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +5/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +18/-16 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +5/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/README.md` | M | +18/-16 | REVIEW | review |
| `publish_all.bat` | M | +10/-0 | REVIEW | review |
| `scripts/md_region.js` | A | +126/-0 | REVIEW | review |
| `scripts/test_md_region.js` | A | +214/-0 | REVIEW | review |
| `scripts/test_whats_new.js` | A | +154/-0 | REVIEW | review |
| `scripts/whats_new.js` | A | +101/-0 | REVIEW | review |
| `ai_docs/audit/audit_plan.md` | M | +2/-2 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/project_notes.md` | M | +6/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/reference/.sources/release-runbook-course-creator.md` | M | +18/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/reference/GUIDE_release.md` | M | +39/-5 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_npm_whats_new.md` | A | +378/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_npm_whats_new.md` | A | +91/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +2/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_npm_whats_new.md` | D | +0/-22 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_npm_whats_new.md` | M | +42/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +2/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_npm_whats_new/` (14 files: PROBES.md, stub, runner, probes, outputs) | A | +374/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +6/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) |
| `ai_docs/memory/INDEX.md` | M | +4/-2 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) |
| `ai_docs/reference/INDEX.md` | M | +1/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) |

The harness rows are folded into one line here; `review-map` lists them one by one.

## Already verified

- **Design review** — REVIEW_LOG 2026-10-27, `solutions/ANALYSIS_npm_whats_new.md`, tier
  design (deep), PASS → PASS → PASS in three rounds. Covered the ANALYSIS, the REQUEST
  record and the probes then in the harness. The round-3 NITs were applied after the cap,
  unreviewed.
- **Closure review** — REVIEW_LOG 2026-10-28, F-070 implementation, tier closure (deep),
  PASS → FAIL → PASS in three rounds. Covered every REVIEW and DESIGN row above. The
  ANALYSIS's closing Diary entry, the deletion of the HANDOFF and this brief came after
  round 3 and were not reviewed.
- **Tests on this tree (2026-10-28):** `node scripts/test_md_region.js` 27/27,
  `node scripts/test_whats_new.js` 13/13, `node scripts/test_clients.js` 63/63; Python
  batteries code 555, kb 882, mkt 557, course 550 OK (run before the round-1 fixes, which
  touch no Python or shared file). `node scripts/whats_new.js`: four `[ok] … README agrees`.
  `npm pack --dry-run --json` in all four packages: no new script shipped.
- **Probes** (`harness_npm_whats_new/PROBES.md`, npm replaced by a stub, nothing sent):
  re-running a publish skips all four packages with 0 publishes; a package without notes is
  refused with 0 publishes (RED before the change: 4 publishes); a package with notes
  reaches publish and the next one without is refused; every moved README block is
  identical and nothing else moved. npm drops HTML comments from a rendered README
  (checked on a live third-party page).
- **`sdlc_check.py check` and `check --hybrid`:** CLEAN after `mark scripts/ distributions/`.
- **Owner decisions:** REQUEST R6–R8 (latest release only with a link; the 1.49.0-wave
  summary in the first notes; approval before the tag; the F-057 block moved; an agent
  review of the notes only when they add content), R10 (go-ahead to implement).

## Your judgement

- **Deviations from the approved design:** none. The fixes during closure tightened the
  design's own promises (FS3: every byte outside the region unchanged, fences paired).
- **Residuals accepted** (ANALYSIS Diary, 2026-10-28): an unclosed fence, or a ```` ``` ````
  opener whose info string holds a backtick, in a `### What's new` carries the rest of the
  CHANGELOG into the notes — your approval of each release's notes is the control; an
  invalid `package.json` is reported against its folder, not the file. T3's residual: a
  publish run refused mid-way has already published the packages before it — the pre-tag
  check in the guide exists to prevent reaching that.
- **CANNOT VERIFY:** how npm renders a filled section (comment line directly above the
  `## What's new` heading) — expected correct, proven only by the first publish (E2E S5).
  Checking the README rendering on GitHub before the first tag is a cheap preview.
- **Decisions still yours:** commit and branch; at each package's next release, the notes
  themselves (the pending first-notes entry in `audit/project_notes.md` lists the four
  packages).

## Merge notes

- No migration and no configuration. Nothing changes for users until a package is
  released with notes.
- Generated files (`handoff.md`, `memory/INDEX.md`, `reference/INDEX.md`,
  `features_history.md`) may conflict on merge: regenerate with `sdlc_check.py index`,
  never resolve by hand. After a squash merge, re-run `mark scripts/ distributions/`.
- Stage explicitly: the untracked `docs-site.zip` and `npm` at the root are not part of
  this unit.
- Hand `E2E_TEST_npm_whats_new.md` to the tester; S4 and S5 belong to each package's next
  release.
