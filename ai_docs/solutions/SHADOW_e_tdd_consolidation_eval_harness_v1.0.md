<!-- SHADOW generated from devPNT (e_tdd_consolidation_eval_harness v1.0) - do not edit by hand -->

# E-TDD: Unit 4 — Eval Harness

**Type:** Technical Design
**Milestone:** M4 — Consolidation & Proactive Activation (Unit 4)
**Frames:** milestone_vision_consolidation v2.1 (APPROVED)
**Derived from:** e_isp_consolidation_eval_harness v1.0
**Governed by:** p_tm_consolidation T4/T5/T9/T10
**Status:** DRAFT

## Summary
Two layers over one scenario corpus, all stdlib, all dev-only. Static battery = deterministic release gate (`unittest discover` aggregating plan+orient+skill-invariants); behavioral corpus = opt-in, non-CI.

## Module Change Plan (8 files)
- **scripts/test_skill_invariants.py** (ADD): static battery. `SKILL_DIR=parents[1]`, `REPO=parents[3]`. Asserts every M4 output — U1 (orient registered + ENFORCEMENT §4 hook), U2 (consult/proactive in SKILL.md/guides.md/dispatch.md), U3 (worktree Phase 4/5) — on stable anchors; support-files wired (explicit expected set + orphan glob); indexes idempotent (build_index/build_manifest/build_guide_index == on-disk, no write); driver-no-llm (T4). 10 tests.
- **evals/run_behavioral.py** (ADD): opt-in driver. load_scenario (fail-fast T5, exit 2), seed (confined), main (mkdtemp + seed + print prompt/criteria). No LLM/network/subprocess (T4).
- **evals/scenarios/{README,consult_fires_on_match,proactive_proposes_on_reusable,hook_orients_session}.md** (ADD): format spec + 3 scenarios (consult = "demonstrably" artifact; proactive; hook).
- **ENFORCEMENT.md** (MODIFY): new §5 — static battery = release gate + behavioral opt-in + optional CI snippet + T10 note.
- **SKILL.md** (MODIFY): §Mechanical Enforcement ladder line → self-eval battery.

## State Model
N/A — stateless assertion set + seed-and-print driver.

## Developer testing strategy
Battery self-tests (`unittest discover` = plan 32 + orient 9 + skill-invariants 10 = 51 green). Driver smoke: valid rc0, malformed rc2. check --hybrid CLEAN. "demonstrably" (Fable #1) = consult_fires_on_match scenario + static presence assertion.
