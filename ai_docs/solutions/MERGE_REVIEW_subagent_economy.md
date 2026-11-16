---
description: Merge review brief for F-100 - what the integrator reviews, what each gate already verified, and what only a person can judge.
status: CURRENT
feature: F-100
analysis: ANALYSIS_subagent_economy.md
base: main
---
# Merge review: Subagent economy (F-100)

## Purpose

A field report from another project measured most subagent tokens lost on guides read in
part, which `task.verify` cannot see, and on fresh contexts rereading guides another context
held (`REQUEST_subagent_economy.md` R1). Now a brief that names guides asks for each guide's
total lines and last line read and the orchestrator checks it before `verify`; two failed
rounds move a task to a higher tier or a split by guide set; a correction goes back to the
subagent that holds the guides; and the team question says what several sessions cost and
buy (`ANALYSIS_subagent_economy.md` §Objective; scope R2).

## What to review

# Review map -- 50 files against c67e5792 (merge-base c67e5792dbce)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +6/-0 | REVIEW | review |
| `README.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +6/-0 | REVIEW | review |
| `distributions/course-creator/README.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/dispatch.md` | M | +59/-11 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_core.py` | M | +8/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +5/-5 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_plan.py` | M | +27/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_skill_invariants.py` | M | +50/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/team.md` | M | +6/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +6/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/dispatch.md` | M | +59/-11 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_core.py` | M | +8/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +5/-5 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_plan.py` | M | +27/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_skill_invariants.py` | M | +50/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/team.md` | M | +6/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +6/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/README.md` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/dispatch.md` | M | +59/-11 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/sdlc_core.py` | M | +8/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +5/-5 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_plan.py` | M | +27/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_skill_invariants.py` | M | +50/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/team.md` | M | +6/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/dispatch.md` | M | +59/-11 | REVIEW | review |
| `skills/agentic-sdlc-skill/evals/scenarios/subagent_guides_read_whole.md` | A | +16/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | M | +8/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +5/-5 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_plan.py` | M | +27/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | M | +50/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/team.md` | M | +6/-0 | REVIEW | review |
| `ai_docs/solutions/ANALYSIS_subagent_economy.md` | A | +354/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_subagent_economy.md` | A | +74/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +12/-3 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +4/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/requests/REQUEST_subagent_economy.md` | A | +56/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +4/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_subagent_economy/CRITERIA.md` | A | +62/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_subagent_economy/RESULTS.md` | A | +31/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_subagent_economy/build_replay.py` | A | +70/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_subagent_economy/prompt_new.md` | A | +340/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_subagent_economy/prompt_old.md` | A | +287/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_subagent_economy/raw_answers_v1.md` | A | +21/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_subagent_economy/raw_answers_v2.md` | A | +21/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_subagent_economy/raw_answers_v3.md` | A | +34/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_subagent_economy/raw_answers_v4.md` | A | +50/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/memory/INDEX.md` | M | +4/-2 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 33 files (+664/-68); DESIGN 4 files (+444/-3); EVIDENCE 11 files (+976/-0); GENERATED 2 files (+5/-2)

The REVIEW files reduce to: the block `### Guides a subagent must read` in
`skills/agentic-sdlc-skill/dispatch.md` with four pointers from the loop, the tiers and the
review slots; four lines in `team.md` §When it is asked; `PLAN_BRIEF_READ_BACK` and its print
in `scripts/sdlc_core.py` `cmd_plan`; tests in `test_plan.py` and class `F100_SubagentEconomy`
— all shared, byte-identical in four trees; one eval scenario; the team sentence and the
`[Unreleased]` entry in each package's README and CHANGELOG.

## Already verified

- **Design review** — REVIEW_LOG 2026-11-16, three F-100 design rows: deep FAIL (round 1, 2
  BLOCK), deep FAIL → PASS (round 2), deep PASS (round 3, cap reached, three WARNs taken).
- **Closure review** — REVIEW_LOG 2026-11-16, one row: deep FAIL → PASS in two rounds (a byte
  figure measured before a rewrap; five WARNs taken).
- **Owner decisions** — scope R2; ceremony estimate R3. Design approved by the agent under the
  reading guide's `## Team` (R4).
- **Tests** — `unittest discover` in each lens's `scripts/` after the last edit: code 697,
  knowledge 1010, marketing 713, course 703, all OK; RED first (7 tests); `check` CLEAN after
  the mark.
- **Replay** — `harness_subagent_economy/`: criteria written first; old text red on C1, C3,
  C5 and new text green on all five, two readers each (`RESULTS.md`, raw answers kept).

## Your judgement

- **The measured cost is above the estimate you accepted** (R3): `dispatch.md` +3,496 bytes
  against about +2.5 KB, `team.md` +538 against +0.4 KB; read only when delegating or when the
  team is asked; `SKILL.md` unchanged. Confirm or ask for a cut.
- **Evidence weight:** C2 and C4 were green on the old text (`RESULTS.md`); FS3 and FS4 rest on
  the field report's measurement, which is the owner's word. Two readers per text, scored by
  the author and re-scored by the closure reviewer.
- **Declared residuals:** a false or gapped "N of N" read is not detected without the
  transcript (T1); a forgotten line discards finished work where the client cannot message a
  subagent again (T5).
- **Out of scope:** proposal 5 (reports in files) and any change to `coordination.md` (R2).
- **Decisions still owed:** the merge into `main`, the push and the release.

## Merge notes

- Branch `claude/f100-subagent-economy`, cut from the release commit `c67e5792`; `main` has
  not moved since.
- Generated files (`ai_docs/audit/handoff.md`, `ai_docs/memory/INDEX.md`,
  `ai_docs/strategic/features_history.md`, `ai_docs/INDEX.md`) and `shared_manifest.json`:
  on a later conflict regenerate, never resolve by hand.
