---
feature: F-074
analysis: ANALYSIS_vision_interview.md
base: main
---
# Merge review: Vision born from an owner interview

## Purpose
Every Vision, in every lens and the devPNT M-VISION, is written only after an owner
interview and an owner-approved north star. This serves the project Vision's Goal 1,
"Make the project's intent readable and *operable*" (`ANALYSIS_vision_interview.md`
§Feature Vision).

## What to review
| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +11/-0 | REVIEW | review |
| `README.md` | M | +2/-2 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +11/-0 | REVIEW | review |
| `distributions/course-creator/gemini-extension.json` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/package.json` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/scripts/init.js` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/SKILL.md` | M | +2/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/elicitation.md` | M | +16/-5 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_skill_invariants.py` | M | +34/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/templates.md` | M | +8/-4 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/vision.md` | M | +69/-6 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +11/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +2/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/gemini-extension.json` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/package.json` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +4/-3 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/elicitation.md` | M | +16/-5 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_skill_invariants.py` | M | +34/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` | M | +45/-6 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/vision.md` | M | +69/-6 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +11/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/gemini-extension.json` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/package.json` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` | M | +3/-3 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/elicitation.md` | M | +6/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_skill_invariants.py` | M | +34/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/templates.md` | M | +34/-5 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/vision.md` | M | +69/-6 | REVIEW | review |
| `gemini-extension.json` | M | +1/-1 | REVIEW | review |
| `package.json` | M | +1/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +7/-7 | REVIEW | review |
| `skills/agentic-sdlc-skill/elicitation.md` | M | +10/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/evals/scenarios/vision_needs_owner_interview.md` | A | +21/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | M | +34/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_vision_interview.py` | A | +83/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/templates.md` | M | +50/-7 | REVIEW | review |
| `skills/agentic-sdlc-skill/vision.md` | M | +69/-6 | REVIEW | review |
| `ai_docs/audit/audit_plan.md` | M | +3/-3 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_intent_focus.md` | M | +7/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_vision_interview.md` | A | +228/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_vision_interview.md` | A | +95/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/MERGE_REVIEW_vision_interview.md` | A | +64/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +3/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_vision_interview.md` | A | +16/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_vision_interview.md` | A | +50/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +2/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_vision_interview/proposed.patch` | A | +596/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +2/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +6/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 41 files (+782/-94); DESIGN 7 files (+401/-4); EVIDENCE 4 files (+664/-0); GENERATED 3 files (+9/-4)

The four `vision.md` copies and the four `test_skill_invariants.py` copies are
byte-identical modulo line endings (drift guard `test_drift.py`, green in all four
batteries): read one of each.

## Already verified
- Design review (late), deep tier: REVIEW_LOG 2026-10-18, `ANALYSIS_vision_interview.md
  (F-074) + applied doctrine diff`, FAIL -> PASS, 1 revise round. Covered the ANALYSIS,
  the request record and the whole doctrine/test/installer diff.
- Closure review, deep tier: REVIEW_LOG 2026-10-18, `bump/CHANGELOG/README/r30/E2E delta`,
  PASS. Covered the version bump, CHANGELOGs, READMEs, `skill_family_agent_workflows.md`,
  `vision/rulings.md` r30 and the E2E script. Its three WARNs were folded after it
  (kb README line 92, E2E scenario S5 for FS7, ANALYSIS/HANDOFF state); no review read
  those three folds.
- Batteries on the bumped tree: code 393 OK, kb 579 OK, mkt 400 OK, course 395 OK
  (`python -m unittest discover -s scripts -p "test_*.py"` in each skill folder); JS
  `scripts/test_clients.js` 53/53, course 4/4.
- Red/green replay: `test_vision_interview.py` and `test_vision_born_from_owner_interview`
  fail on `main`'s text and pass on this branch (ANALYSIS §Test Strategy; re-run by the
  design reviewer on `git archive main`).
- Installers: all four `init.js` run in scratch projects with a stubbed HOME wrote the
  Vision stub; each seeded project validates with no errors.
- `sdlc_check.py check --root .`: CLEAN after `mark` on this commit.
- Owner decisions: structure R1, family-wide scope R2, bootstrap stub R3, diff approval
  R4, cost acceptance and r30 ADMIT R5 (`audit/requests/REQUEST_vision_interview.md`).
- Not covered by any review: `ai_docs/solutions/harness_vision_interview/proposed.patch`
  is the diff shown to the owner before apply (R4), kept as evidence; it is not the
  final diff.

## Your judgement
- Deviations from the approved diff (R4): the review rounds added changes the owner did
  not see as a patch — full template changes in kb/mkt/course, the course `init.js`
  stub, the seeding assertion, the planned-occasion lines, `REQUEST_project_vision.md`
  in `vision.md`, pointers in `SKILL.md` and `templates.md`. All are recorded in the
  ANALYSIS Diary.
- Residual: existing APPROVED Visions (this repo's `project_vision.md` included) are not
  re-interviewed; they are re-interviewed on their next amendment (ANALYSIS
  §Populations at rest).
- Residual: the behavioral scenario was never run with a model; it is non-gating.
- CANNOT VERIFY: installation from the tagged release (no tag yet).
- Decisions still owed: the release — tags `v1.43.0`, `kb-v1.26.0`, `mkt-v0.21.0`,
  `course-v0.1.0-beta.7`, the merge to main and `publish_all.bat`
  (`GUIDE_release.md` steps 5–9).

## Merge notes
- Generated files (`audit/handoff.md`, `memory/INDEX.md`, `strategic/features_history.md`,
  `INDEX.md`) may conflict: regenerate with `sdlc_check.py index`, never resolve by hand.
- After a squash merge, re-run `mark` on `skills/` and `distributions/`.
- Hand testers `ai_docs/solutions/E2E_TEST_vision_interview.md`.
