---
feature: F-077
analysis: ANALYSIS_kb_intake_hygiene.md
base: 6015848 (tip of feat/f075-orientation-reach, which this branch is cut from)
---
# Merge review: kb intake hygiene

## Purpose

A credential handed over in a team's documents could become an immutable,
hash-checked corpus artifact or guide snapshot, and nothing flagged it. Now intake
redacts first, `check` refuses a credential-shaped line in `corpus/given/` and in
document-guide snapshots (every lens) without printing the value, a secret-bearing
artifact can be withdrawn, `adopt` lists what moving document guides into the corpus
involves, and the same text in two homes is reported. Serves Goal 2 (what stays
durable is safe to keep) — ANALYSIS §Feature Vision, rulings r35a–c.

## What to review

The map is computed against 6015848, not main: this branch sits on the unmerged
F-075 branch, so a diff against main would show F-075's files too. Merge F-075 first.

# Review map -- 43 files against 6015848 (merge-base 6015848cb250)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +5/-0 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +5/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/guides.md` | M | +7/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/docs_site.py` | M | +6/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/knowledge.py` | M | +342/-8 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +8/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +4/-4 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/distillation.md` | M | +50/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/evals/scenarios/intake_redacts_credentials.md` | A | +40/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/evals/scenarios/open_unit_absorbs_a_new_source.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/guides.md` | M | +7/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/portability.md` | M | +33/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/docs_site.py` | M | +6/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/knowledge.py` | M | +342/-8 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_kb_ingestion_rhythm.py` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_kb_intake.py` | A | +552/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` | M | +23/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +5/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/guides.md` | M | +7/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/docs_site.py` | M | +6/-2 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/knowledge.py` | M | +342/-8 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `skills/agentic-sdlc-skill/guides.md` | M | +7/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/docs_site.py` | M | +6/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/knowledge.py` | M | +342/-8 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `ai_docs/audit/audit_plan.md` | M | +3/-3 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_kb_intake_hygiene.md` | A | +491/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_kb_intake_hygiene.md` | A | +110/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +3/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +3/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +3/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_kb_intake_hygiene.md` | D | +0/-22 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_kb_intake_hygiene.md` | M | +57/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +5/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_kb_intake_hygiene/probe.py` | A | +152/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +0/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +5/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 30 files (+2161/-65); DESIGN 6 files (+613/-5); EVIDENCE 4 files (+214/-22); GENERATED 3 files (+6/-4)

`knowledge.py`, `docs_site.py`, `guides.md` and `shared_manifest.json` under
`distributions/` are byte-identical copies of the `skills/agentic-sdlc-skill/` ones
(`shared_files.py --check`, four identical manifests): review them once. The code to
read is `skills/agentic-sdlc-skill/scripts/knowledge.py` (credential scan, tombstones,
same-text warning, `adopt`, URL masking), `docs_site.py` (two tombstone skips), and
`test_kb_intake.py`; the doctrine is kb `distillation.md` §1/§4, `portability.md` §6,
kb `templates.md`, kb `SKILL.md`, shared `guides.md` §2 step 3.

## Already verified

- Design review: REVIEW_LOG 2026-10-23, `ANALYSIS_kb_intake_hygiene.md (F-077)`,
  design, deep, rung 1. FAIL → FAIL → PASS in 3 rounds; five WARNs folded after the
  PASS were checked by the closure review.
- Closure review: REVIEW_LOG 2026-10-23, `F-077 diff 6015848..0290d97` then
  `0290d97..c94f0d6`, closure, deep. FAIL → PASS in 2 rounds (B1 extraction escape,
  B2 untested export/chronology skips; the new tests killed a mutation). The URL
  masking WARN (N1) was folded after the PASS with a test.
- Batteries after the final code change (`python -m unittest discover -s . -p
  "test_*.py"` per scripts folder): code 420, kb 642, mkt 422, course 415 OK.
- Probe `ai_docs/solutions/harness_kb_intake_hygiene/probe.py`: 12/12 GREEN. On the
  baseline P1 (credential passes `check`), P3 (two homes silent) and P4 (no `adopt`)
  were red; P6 shows the snapshot error once in the code, kb and marketing `check`
  on a tree with no corpus.
- `check` CLEAN after `mark` and `index` on the closing commit.
- Owner decisions, `audit/requests/REQUEST_kb_intake_hygiene.md`: R3 error with a
  reviewed escape; R4 language rule; R5 withdrawal; R6 document snapshots scanned in
  every lens; R7 personal and confidential data redacted by need; R8 cost and r35a/c
  ADMIT, L1 at-rest exposure ruled admissible; R9 r35b ADMIT (r34a–c in the record, renumbered at merge); R10 final read cost
  +7,780 bytes accepted.

## Your judgement

- Deviations from the approved design: none. Closure fixes changed the extraction
  escape lookup, tombstone digest rule (adds `original_sha256:`), URL masking, tests
  and wording; all recorded in the ANALYSIS.
- Accepted residuals: symlinks under `given/` and `.sources/` are followed (T11,
  names and line numbers only printed); FS2's declared false positives and negatives;
  secrets already in git history stay there (purging is the user's).
- Upgrade effect (R8): a project whose stored sources already hold a credential line
  fails `check` after the upgrade until each file is withdrawn/redacted or reviewed —
  including in CI on an L1 change.
- CANNOT VERIFY: the kb eval scenario `intake_redacts_credentials.md` needs a live
  agent session; the E2E scenarios are manual, after the merge.
- Decisions still owed: the merge of this branch (after F-075's); the release per
  `GUIDE_release.md`. CHANGELOG sections stay `[Unreleased]`, versions provisional.

## Merge notes

- Shared files (`knowledge.py`, `docs_site.py`, `guides.md`, the four manifests) are
  also touched by sibling units F-076/F-078..F-080: on conflict, merge the source in
  `skills/agentic-sdlc-skill/`, copy it to the three distributions, and run
  `shared_files.py --update` in each scripts folder — never hand-merge a manifest.
- `vision/rulings.md`: this branch adds r35a–c. The request record (R8, R9) and the
  review log call them r34a–c: they were renumbered at the merge with main, where
  F-080 had taken r33 and F-076 r34.
- Generated files (`audit/handoff.md`, `memory/INDEX.md`,
  `strategic/features_history.md`, `INDEX.md`) are regenerated with `sdlc_check.py
  index`, never resolved by hand.
- `mark` recorded the branch commit 4ad5a29; after a squash or rebase merge, re-run
  `mark` on main for `skills/agentic-sdlc-skill/`, `skills/` and `distributions/`.
- Hand `E2E_TEST_kb_intake_hygiene.md` to the tester after the merge.
