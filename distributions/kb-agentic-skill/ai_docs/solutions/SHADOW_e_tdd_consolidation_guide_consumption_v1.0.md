<!-- SHADOW generated from devPNT (e_tdd_consolidation_guide_consumption v1.0) - do not edit by hand -->

# E-TDD: Unit 2 — Guide-Layer Consumption Discipline

**Type:** Technical Design
**Milestone:** M4 — Consolidation & Proactive Activation (Unit 2)
**Frames:** milestone_vision_consolidation v2.1 (APPROVED)
**Derived from:** e_isp_consolidation_guide_consumption v1.0
**Governed by:** p_tm_consolidation T6 (no silent creation) & T7 (no blanket reading)
**Status:** DRAFT

## Summary
Doctrine unit (prose, no code). Two triggers close the write-only guide layer, mechanics single-sourced in `guides.md`, hooked from `SKILL.md` + reconciled with dispatch in `dispatch.md`.

## Module Change Plan
- **guides.md**: new `## 0. Consuming a guide (consult before acting)` before `## 1` — triage-proportional (L1 exempt), scan project + agent-KB router descriptions, read matching synthesis whole, targeted match never blanket (T7), dispatch note pointer. New `### Proactive trigger (after reusable success)` under `## 1` — after reusable user-indication-governed work, PROPOSE into the existing pipeline; never silent, never model-knowledge, distilled_from absolute (T6).
- **SKILL.md**: `## Operative Guides` gains a 3-moment lead (consult/create/propose) pointing to guides.md; `### 4. Development` gains a consult bullet (before implementing, L1 exempt); `### 5. Closure` gains a proactive-propose bullet.
- **dispatch.md**: reconciling note — consult under dispatch = populating the task `guides` field at plan-authoring time (orchestrator runs router lookup); context-free subagent reads handed pointers, does NOT self-consult; proactive stays at closure (no separate hook).

## State Model
N/A — stateless decision points (consult before act; propose after success); no lifecycle field.

## Developer testing strategy
No code test (prose). Verified by §4.6 review vs this E-TDD + `check --hybrid`. Presence becomes a mechanically-asserted release gate in Unit 4 (eval harness); Fable finding #1 ("demonstrably") carried into U4. TDD exempt (no code under test), recorded per SKILL.md:197.
