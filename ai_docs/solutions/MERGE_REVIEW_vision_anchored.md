---
description: Merge review brief for F-099 - what the integrator reviews, what each gate already verified, and what only a person can judge.
status: CURRENT
feature: F-099
analysis: ANALYSIS_vision_anchored.md
base: main
---
# Merge review: Vision anchored (F-099)

## Purpose

A requirement grew stricter than the Vision clause it served and four review rounds never
measured it against that clause. Now every restriction in an L3 design names its source and
stays within its test, the design review checks that direction, and a second design-review
FAIL of one class re-reads the source first (`ANALYSIS_vision_anchored.md` §Objective; the
owner's words, `REQUEST_vision_anchored.md` R1).

## What to review

# Review map -- 42 files against main (merge-base 948414c90b8b)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `distributions/course-creator/skills/course-creator/SKILL.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/review.md` | M | +15/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_skill_invariants.py` | M | +49/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/vision.md` | M | +38/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +2/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/review.md` | M | +15/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_skill_invariants.py` | M | +49/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/vision.md` | M | +38/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/review.md` | M | +15/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_skill_invariants.py` | M | +49/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/vision.md` | M | +38/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +2/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/evals/scenarios/restriction_exceeds_its_source.md` | A | +16/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/review.md` | M | +15/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | M | +49/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/vision.md` | M | +38/-1 | REVIEW | review |
| `ai_docs/README.md` | M | +7/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_vision_anchored.md` | A | +316/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/MERGE_REVIEW_vision_anchored.md` | A | +110/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/process_agentic_sdlc_devpnt.md` | M | +1/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +2/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/requests/REQUEST_vision_anchored.md` | A | +74/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +3/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_vision_anchored/PROPOSTA_proporzionalita_e_riancoraggio.md` | A | +40/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_vision_anchored/build_replay.py` | A | +72/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_vision_anchored/build_replay2.py` | A | +73/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_vision_anchored/replay/CRITERIA.md` | A | +24/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_vision_anchored/replay/RESULTS.md` | A | +51/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_vision_anchored/replay2/CRITERIA.md` | A | +25/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_vision_anchored/replay2/RESULTS.md` | A | +31/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_vision_anchored/replay2/prompt_new.md` | A | +78/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_vision_anchored/replay2/prompt_new_v1.md` | A | +76/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_vision_anchored/replay2/prompt_old.md` | A | +42/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_vision_anchored/replay2/raw_answers_v1.md` | A | +91/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_vision_anchored/replay2/raw_answers_v2.md` | A | +53/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/memory/INDEX.md` | M | +5/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 21 files (+442/-26); DESIGN 5 files (+436/-1); EVIDENCE 14 files (+733/-0); GENERATED 2 files (+6/-3)

The REVIEW files reduce to: `skills/agentic-sdlc-skill/vision.md` §8 and
`skills/agentic-sdlc-skill/review.md` (conformance clause, re-anchor paragraph), copied
byte-identical into three trees; one sentence in each lens's `SKILL.md`; class
`F099_VisionAnchored` in the shared invariants; one eval scenario.

## Already verified

- **Design (late) + closure review** — REVIEW_LOG 2026-11-15, three F-099 rows: deep FAIL
  (round 1), deep scoped PASS (round 2), light scoped PASS on the corrections (round 3).
- **Design approval** — by the agent under the owner's delegation (R3), recorded as R6.
- **Owner decisions** — framing R2; ceremony shape R4; measured cost and three sources R5;
  merge R7; case out of the repository and history rebuilt R8.
- **Tests** — `unittest discover` in each lens's `scripts/`: code 691, knowledge 1004,
  marketing 707, course 697, all OK; `check` CLEAN after the mark.
- **Replays** — `harness_vision_anchored/replay/` (recorded case: old 0/2, new 2/2) and
  `replay2/` (drafting time and T1: old 0/2, new v2 2/2), criteria, prompts and raw answers kept.

## Your judgement

- **Deviation:** the doctrine was implemented before the first design review (ANALYSIS Diary).
- **Evidence weight:** two samples per text, scored by the author.
- **The case is not in the repository** (R8): it described open defects of another project;
  replay 1 keeps its criteria and results, the three local commits were rebuilt without it.
- **Declared residual:** a threat-sourced protection may be narrowed to the threat's own
  wording; the design review's restriction row is its only check.
- **Out of scope:** the devPNT doctrine half of the proposal.
- **Decisions still owed:** the push, the release and its version numbers (`GUIDE_release.md`).

## Merge notes

- Fast-forward into local `main` on R7; the unit is closed in the same change.
- Generated files (`ai_docs/audit/handoff.md`, `ai_docs/memory/INDEX.md`,
  `ai_docs/strategic/features_history.md`, `ai_docs/INDEX.md`) and `shared_manifest.json`:
  on a later conflict regenerate, never resolve by hand.
