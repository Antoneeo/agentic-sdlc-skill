---
feature: F-094
analysis: ANALYSIS_whole_guide_read.md
base: main
---
# Merge review: a matched guide is read whole and applied whole

## Purpose

Agents read the guide that governs their work only in part and applied only that part
(REQUEST_whole_guide_read.md R1). The verdict hook now credits a guide as read only when the
session's reads cover every line, and the doctrine of the four lenses says the guide is read
whole and applied whole, with a proposed amendment as the only way to depart from a rule.

## What only a human can judge

1. The tightening is felt at the first edit: a session whose only "read" was Grep, `head`,
   a partial Read or a subagent brief is now refused until it reads the guide whole. Is that
   the friction you want? (It is the rule as you stated it.)
2. The agentic per-turn line was compressed to stay under the 600/700 caps (rulings
   r19/r32): "first defect you can measure" became "fixing", and two clauses were merged.
   Check the wording still carries what you meant.
3. No design-approval entry exists in the request record: the rule came prescribed in R1.

## What was verified, by which gate

- `test_verdict.py` (+7 tests): 5 fail on the old `sdlc_core.py`, all pass on the new one.
- `harness_whole_guide_read/probe.py`: five field read shapes refused, four whole reads pass;
  all five passed before.
- Full batteries: agentic, kb, mkt, course; `node scripts/test_clients.js`; drift guard
  (33 shared files identical); `sdlc_check.py check` CLEAN.
- Independent review (fresh subagent): FAIL then fixed; row in REVIEW_LOG.

## Not done

No CHANGELOG/What's new, no version bump, no tag, no push, no publish: release follows
GUIDE_release.md when you decide to merge.

## What to review

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `distributions/course-creator/skills/course-creator/ENFORCEMENT.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/SKILL.md` | M | +2/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/dispatch.md` | M | +2/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/guides.md` | M | +33/-9 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_check.py` | M | +2/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_core.py` | M | +101/-14 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +4/-4 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_verdict.py` | M | +68/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/ENFORCEMENT.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +2/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/dispatch.md` | M | +2/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/evals/scenarios/consult_fires_on_match.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/guides.md` | M | +33/-9 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/fixtures/golden_baseline.txt` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_check.py` | M | +2/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_core.py` | M | +101/-14 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +4/-4 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_verdict.py` | M | +68/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/ENFORCEMENT.md` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/dispatch.md` | M | +2/-2 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/guides.md` | M | +33/-9 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py` | M | +2/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/sdlc_core.py` | M | +101/-14 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +4/-4 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_verdict.py` | M | +68/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/ENFORCEMENT.md` | M | +6/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +3/-3 | REVIEW | review |
| `skills/agentic-sdlc-skill/dispatch.md` | M | +2/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/evals/scenarios/consult_fires_on_match.md` | M | +1/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/guides.md` | M | +33/-9 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/fixtures/golden_baseline.txt` | M | +1/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` | M | +4/-5 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | M | +101/-14 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +4/-4 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_verdict.py` | M | +68/-0 | REVIEW | review |
| `ai_docs/audit/audit_plan.md` | M | +3/-3 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_whole_guide_read.md` | A | +207/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_whole_guide_read.md` | A | +70/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/MERGE_REVIEW_whole_guide_read.md` | A | +40/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +3/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_whole_guide_read.md` | A | +15/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_whole_guide_read.md` | A | +27/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +1/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_whole_guide_read/field_scan.txt` | A | +19/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_whole_guide_read/probe.py` | A | +94/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +2/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +3/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 36 files (+863/-141); DESIGN 5 files (+323/-4); EVIDENCE 5 files (+156/-0); GENERATED 3 files (+6/-2)
