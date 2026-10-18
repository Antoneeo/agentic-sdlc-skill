---
feature: F-071
analysis: ANALYSIS_intent_focus.md
base: main
---
# Merge review: Intent focus

## Purpose
A review weighs effort against the owner's outcome and runs only where something is
left to judge. Serves the Vision Goals "Scale process cost to risk, in both directions"
and "divergence visible before implementation" (`ANALYSIS_intent_focus.md` §Feature Vision).

## What to review
| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +8/-0 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +7/-0 | REVIEW | review |
| `distributions/course-creator/gemini-extension.json` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/package.json` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/SKILL.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/review.md` | M | +28/-3 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_core.py` | M | +12/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/templates.md` | M | +2/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +7/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/gemini-extension.json` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/package.json` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/review.md` | M | +28/-3 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_core.py` | M | +12/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` | M | +3/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +7/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/gemini-extension.json` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/package.json` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/review.md` | M | +28/-3 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/sdlc_core.py` | M | +12/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/templates.md` | M | +3/-1 | REVIEW | review |
| `gemini-extension.json` | M | +1/-1 | REVIEW | review |
| `package.json` | M | +1/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +2/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/review.md` | M | +28/-3 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | M | +12/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_intent_focus.py` | A | +109/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/templates.md` | M | +3/-1 | REVIEW | review |
| `ai_docs/reference/.sources/skill-family-copy-count.md` | A | +10/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/reference/GUIDE_skill_family_changes.md` | A | +21/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_intent_focus.md` | M | +235/-127 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_intent_focus.md` | A | +68/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +3/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_intent_focus.md` | D | +0/-18 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_intent_focus.md` | M | +28/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +7/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_intent_focus/BEHAVIOR_CASES.md` | A | +81/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_intent_focus/probe_benefit.py` | A | +32/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_intent_focus/proposed.patch` | A | +69/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_intent_focus/replay.py` | A | +199/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/INDEX.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/audit/handoff.md` | M | +1/-2 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +5/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/reference/INDEX.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

## Already verified
- Design: REVIEW_LOG 2026-10-18 `ANALYSIS_intent_focus.md (F-071) + proposed.patch`, design, FAIL -> PASS, 2 rounds; covered the ANALYSIS and the doctrine diff.
- Implementation: REVIEW_LOG 2026-10-18 `F-071 implementation diff 8ea116b..52723c2`, closure, FAIL -> PASS, 2 rounds (corrections 52723c2..a7f98fa); the applied `review.md`/`SKILL.md` are byte-identical to the reviewed patch (blob ids, reviewer check 1).
- Release delta: REVIEW_LOG 2026-10-18 NOT DUE row (bump, CHANGELOG ×4, indexes, marks).
- Tests on the release tree: code 398, kb 579, mkt 400, course 395 OK; `test_clients.js` 53/53 and course 4/4; `test_intent_focus.py` red on 8ea116b, green after; `replay.py` RED -> GREEN; `probe_benefit.py` exit 0.
- Owner decisions: design and cost R5, copy count R6, implement and release R7, r31 ADMIT + guide + direct push R8 (`audit/requests/REQUEST_intent_focus.md`).
- Not covered by any review: `GUIDE_skill_family_changes.md` and its source snapshot, the r31 row in `vision/rulings.md`, this brief, the last Diary entry — records written after the closure PASS from owner entries R6 and R8.

## Your judgement
- Deviation from the approved design: the cold-agent replay was not re-run on the applied text (one clause differs from the replayed one; recorded in the Diary and `BEHAVIOR_CASES.md`).
- Accepted residual (T4): a CHANGELOG line that misstates, without adding a claim, a reviewed change is no longer reviewed.
- Open: the field signal (R4) over the next three L3 units.
- CANNOT VERIFY: the cold agents' raw answers live only in the F-071 session transcript.

## Merge notes
Generated files (`INDEX.md`, `handoff.md`, `memory/INDEX.md`, `reference/INDEX.md`, `features_history.md`): regenerate with `index`, never resolve by hand. Hand `E2E_TEST_intent_focus.md` to the tester after publish.
