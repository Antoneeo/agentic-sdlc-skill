---
feature: F-066
analysis: ANALYSIS_merge_review.md
base: main
---
# Merge review: Merge review brief and human E2E test script

## Purpose

Integrators did not know what to review in an L3 pull request, `ai_docs/` included.
Every L3 closure now ships this kind of brief plus a post-merge E2E script for human
testers, and `sdlc_check.py review-map` classes each changed file. Vision benefit:
"make divergence visible … again before merge" (brief, map) and "keep understanding
durable — … tests … stay synchronized" (E2E) — `ANALYSIS_merge_review.md`
§Feature Vision; ruled ADMIT as `vision/rulings.md` r25.

## What to review

Review map -- 20 files against main (merge-base 4680ceac601f)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `README.md` | M | +2/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +3/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/hybrid.md` | M | +9/-6 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` | M | +210/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_review_map.py` | A | +261/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/templates.md` | M | +83/-0 | REVIEW | review |
| `ai_docs/audit/audit_plan.md` | M | +5/-5 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_merge_review.md` | A | +265/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_merge_review.md` | A | +98/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/MERGE_REVIEW_merge_review.md` | A | +63/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/existing_features.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +9/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +8/-0 | EVIDENCE | spot-check that the verdicts the brief cites exist; do not re-review |
| `ai_docs/solutions/harness_merge_review/RESULTS.txt` | A | +10/-0 | EVIDENCE | spot-check that the verdicts the brief cites exist; do not re-review |
| `ai_docs/solutions/harness_merge_review/probe_generated.py` | A | +68/-0 | EVIDENCE | spot-check that the verdicts the brief cites exist; do not re-review |
| `ai_docs/memory/INDEX.md` | M | +7/-4 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 7 files (+569/-8); DESIGN 8 files (+443/-5); EVIDENCE 3 files (+86/-0); GENERATED 2 files (+8/-4)

Line counts are as of the run; the file set is final.

## Already verified

- **Design review** — REVIEW_LOG row 2026-10-12 `ANALYSIS_merge_review.md (F-066)`,
  deep tier, fresh subagent: FAIL → PASS in 3 rounds. Covered: the whole ANALYSIS and
  the probe harness `harness_merge_review/`.
- **Closure review** — REVIEW_LOG row 2026-10-12 `F-066 implementation diff`, deep
  tier, fresh subagent: FAIL → FAIL → PASS in 3 rounds. Covered: every file in the
  map except this brief and the files rewritten after it (`audit/audit_plan.md` by
  `mark`, the GENERATED indexes). It re-ran AC1 on the real F-065 change set
  (370 generated lines classed GENERATED).
- **Tests** — `python -m unittest discover -s scripts -p "test_*.py"` from
  `skills/agentic-sdlc-skill`: 245 tests OK (1 skipped), run after the last code edit
  of this branch (uncommitted on base `4680cea`). `test_review_map.py` holds AC1–AC6, AC8.
- **Validator** — `sdlc_check.py check --root .` CLEAN after `mark` (see Merge notes).
- **Owner decisions** — design approved; doctrine cost confirmed twice (final:
  SKILL.md +1184, templates.md +3258, hybrid.md +370 UTF-8 LF bytes); r25 ADMIT with
  two bases — all 2026-10-12, recorded in r25 and the ANALYSIS Diary.

## Your judgement

- **Deviations from the approved design:** AC4 extended to a failing `index`
  (fails closed, tested); GENERATED instruction for `SHADOW_` mirrors reworded to
  "exported from devPNT" (class unchanged).
- **Accepted residuals:** `--base -x` (space form) is refused by argparse with a usage
  error, not the `[ERROR]` line (the `=` form gives it; git is never reached); AC6
  escaping is unit-tested on the helper only — git on Windows refuses such names;
  the docs root is copied whole per run (~3 s on this repo, larger on a big
  `corpus/`); in this repo the byte-identical `distributions/` copies class REVIEW.
- **CANNOT VERIFY left open:** a dangling or unreadable untracked file is handled by
  code reading only (no symlink privilege on the review host).
- **Declared assumptions:** none.
- **Decisions still owed:** release/version of 1.38.0 (CHANGELOG entry under
  Unreleased); whether testers should become a Vision actor (separate amendment).

## Merge notes

- Generated files (`memory/INDEX.md`, `strategic/features_history.md`) may conflict
  with other branches: re-run `sdlc_check.py index`, never resolve by hand.
- `audit/audit_plan.md` was `mark`ed with a timestamp on this branch; after a squash
  or rebase merge, re-run `mark` on the integration branch (`templates.md` §audit_plan).
- No migration, no configuration change; shared spine files untouched, so the three
  distributions need no sync.
- Hand `E2E_TEST_merge_review.md` to testers after the merge.
