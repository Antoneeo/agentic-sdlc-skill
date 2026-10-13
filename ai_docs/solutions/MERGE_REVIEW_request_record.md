---
feature: F-067
analysis: ANALYSIS_request_record.md
base: main
---
# Merge review: Verbatim request record

## Purpose

In every lens, each L3/E3 unit now keeps the owner's own words — the opening request
and every later decision — verbatim and append-only in `audit/requests/`, before the
Vision Gate; artifacts cite entries and reviews check owner statements against them.
Vision benefit: "keep understanding durable … nothing load-bearing lives only in a
transcript" and "never hide a conflict between a user request and the declared
Vision" — `ANALYSIS_request_record.md` §Feature Vision; ruled ADMIT as r26.

## What to review

Review map -- 47 files against main (merge-base 9edaf1f7ecad)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `README.md` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/SKILL.md` | M | +2/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/elicitation.md` | M | +7/-3 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/review.md` | M | +9/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_skill_invariants.py` | M | +19/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/templates.md` | M | +39/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +6/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/elicitation.md` | M | +7/-3 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/review.md` | M | +9/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_skill_invariants.py` | M | +19/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` | M | +44/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` | M | +2/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/elicitation.md` | M | +5/-2 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/hybrid.md` | M | +3/-2 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/review.md` | M | +9/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_skill_invariants.py` | M | +19/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/templates.md` | M | +41/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +2/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/elicitation.md` | M | +8/-5 | REVIEW | review |
| `skills/agentic-sdlc-skill/hybrid.md` | M | +6/-4 | REVIEW | review |
| `skills/agentic-sdlc-skill/review.md` | M | +9/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` | M | +3/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_review_map.py` | M | +2/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | M | +19/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/templates.md` | M | +43/-1 | REVIEW | review |
| `ai_docs/audit/audit_plan.md` | M | +4/-4 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_request_record.md` | A | +227/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_request_record.md` | A | +90/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/MERGE_REVIEW_request_record.md` | A | +68/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/existing_features.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +8/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/requests/REQUEST_request_record.md` | A | +59/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +8/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_request_record/MOTIVATING_CASE.md` | A | +29/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_request_record/REPLAY.md` | A | +62/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_request_record/fixture_REQUEST_merge_review.md` | A | +59/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/memory/INDEX.md` | M | +6/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 33 files (+345/-42); DESIGN 7 files (+399/-4); EVIDENCE 5 files (+217/-0); GENERATED 2 files (+7/-3)

Line counts are as of the run; the file set is final.

## Already verified

- **Design review** — REVIEW_LOG row 2026-10-13 `ANALYSIS_request_record.md (F-067)`,
  deep tier, fresh subagent: FAIL → PASS in 2 rounds; its two folded WARNs re-reviewed
  by the closure review (both addressed). Covered: the ANALYSIS, the request record,
  `MOTIVATING_CASE.md`.
- **Closure review** — REVIEW_LOG row 2026-10-13 `F-067 implementation diff`, deep
  tier, fresh subagent: FAIL → PASS in 2 rounds. Covered: every file in the map except
  this brief and the files rewritten after it (`audit/audit_plan.md` by `mark`, the
  GENERATED indexes). It re-ran AC1 independently against the final doctrine.
- **Behaviour replays** — `harness_request_record/REPLAY.md`: AC1 RED (old doctrine:
  no record) and GREEN (record before the first question, reply names it); AC2: 13/13
  F-066 owner statements resolve against a rebuilt record.
- **Tests** — each distribution's battery after the last edit: code 246, kb 421,
  marketing 258, course 252 — all OK (skips only). Shared `review.md` and
  `test_skill_invariants.py` byte-identical in the four packages; manifests identical.
- **Validator** — `sdlc_check.py check --root .` CLEAN after `mark` (Merge notes).
- **Owner decisions** — `audit/requests/REQUEST_request_record.md`: open the unit R2;
  scope R4–R6 (decisions too; L3/E3 only; all four lenses); design and estimate R7;
  measured cost R8 and, after the review fixes, R10; r26 ADMIT R9.

## Your judgement

- **Deviations from the approved design:** the one-line reply naming the record,
  missing at first, added after closure round 1 (B1) — it was in the design; the
  added bytes re-confirmed (R10).
- **Accepted residuals:** the agent is still the transcriber of the owner's words (T2);
  append-only is enforced by doctrine and review, not by the validator (weighed in the
  ANALYSIS); open workstreams start a record only at their next owner decision; a kb
  note's entry name dangles after an export (its words travel with it).
- **CANNOT VERIFY left open:** fidelity of R1–R10, of the motivating excerpts and of
  the F-066 fixture — the transcripts are not in the repository; AC2's raw output was
  not kept.
- **Declared assumptions:** none.
- **Decisions still owed:** release/version for the four packages (CHANGELOG entries
  under Unreleased).

## Merge notes

- Generated files (`memory/INDEX.md`, `strategic/features_history.md`, `audit/handoff.md`)
  may conflict: re-run `sdlc_check.py index`, never resolve by hand.
- `audit/audit_plan.md` was `mark`ed with a timestamp; after a squash or rebase merge,
  re-run `mark` on the integration branch.
- Shared files changed (`review.md`, `scripts/test_skill_invariants.py`): the four
  copies and manifests travel together — merge all of them or none.
- Hand `E2E_TEST_request_record.md` to testers after the merge.
