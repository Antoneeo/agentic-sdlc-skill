---
description: Dated, evidence-based comparison of agentic-sdlc 1.26.1 and Superpowers 6.2.0: advantages, parity, remaining gaps and deliberate non-adoptions.
status: CURRENT
---
# Capabilities & Positioning

**Snapshot:** 2026-08-06 · Agentic SDLC 1.26.1 · Superpowers 6.2.0.

**Reader/action:** this report lets the product owner decide what Agentic SDLC should absorb, retain as a deliberate difference, or leave to Superpowers. It compares the two methodologies; it does not authorize roadmap work. Product intent remains owned by `ai_docs/vision/project_vision.md`, admission precedents by `ai_docs/vision/rulings.md`, and implementation decisions by the relevant ANALYSIS/ADR.

Evidence comes from the repository at tag `v1.26.1` and the installed Superpowers 6.2.0 skill set (14 skills). Concepts are summarized; no Superpowers text or format is copied.

## Executive finding

The old comparison described Agentic SDLC as governance-rich but execution-light. That is no longer accurate. Agentic SDLC now includes explicit TDD, systematic debugging, executable plans, durable task ledgers, fresh-context subagent execution, independent design/closure review, worktree isolation, branch-finishing discipline, and fresh evidence before completion claims.

The products nevertheless remain different:

- **Superpowers is execution-first.** Its strongest asset is a set of focused, aggressively worded techniques that activate close to the coding action.
- **Agentic SDLC is governance-first.** Its distinguishing asset is one risk-proportional process spine connecting durable intent, grounded requirements, architecture, implementation, evidence, review and cross-session knowledge.

Neither framing makes the other redundant. Agentic SDLC should absorb mechanisms only when they close an observed failure or prevent irreversible damage; wholesale process fusion would duplicate authorities and violate proportionality.

## Comparison matrix

| Dimension | Agentic SDLC 1.26.1 | Superpowers 6.2.0 | Assessment |
|---|---|---|---|
| Process activation | Rule Zero selects L1/L2/L3/Spike and scales ceremony to risk | Skill triggers select focused workflows; `using-superpowers` requires invocation whenever a skill may apply | **Agentic advantage:** proportionality. Superpowers is more forceful, but its universal trigger carries higher reading/process cost |
| Persistent intent | APPROVED/DRAFT Vision, Actors, benefits, Non-Goals, Success Signals and precedent ledger | Feature-level brainstorming and approved design | **Agentic advantage:** durable, cross-feature authority; Superpowers is lighter for a single change |
| Requirements chain | Grounded Use Cases → Functional Spec → Interface Contract → Threat Model → Capability Ledger → Impact | Brainstorming turns intent into an approved design before implementation | **Agentic advantage:** stronger traceability and anti-invention gates; Superpowers has the simpler interaction |
| Documentation lifecycle | Canonical status, supersession, curated/generated indexes, feature history, handoff registry | Plans/designs and SDD workspace artifacts support execution but do not form an equivalent project-wide lifecycle | **Agentic advantage:** durable project memory |
| Mechanical enforcement | `sdlc_check.py` validates structure, freshness, gates, plans, indexes and domain rules | Mostly instruction-level enforcement plus workflow helper scripts | **Agentic advantage:** more guarantees survive long context and model drift |
| TDD | `tdd.md`: RED/GREEN/REFACTOR for L2/L3, with an explicit exception record | Dedicated TDD skill with test-first iron law, failure observation, rationalization table and restart red flags | **Core parity; Superpowers stronger in enforcement writing.** Tranche B may strengthen test-honesty evidence without adding a gate |
| Debugging | `debugging.md`: root cause, hypothesis, evidence, circuit breaker and chronic-fragility escalation | Dedicated four-phase systematic-debugging workflow with pattern comparison, boundary evidence and extensive stop conditions | **Core parity; Superpowers more operationally prescriptive.** Pattern/boundary evidence remains a selective Tranche B candidate |
| Planning | Executable `PLAN_*` derived from approved design; exact paths, inputs/outputs, verification and confinement | Bite-sized implementation plans with exact files, code, tests, constraints and self-review | **Parity in executable specificity.** Agentic additionally binds the plan to governed design and validates its schema |
| Delegated execution | Optional L3 dispatch; fresh task agents, mechanical task briefs, model tier, durable single-writer ledger and resume-after-compaction | Fresh subagent per task, spec/quality reviews, fix loop, broad final review; separate batch-plan execution | **Parity with different emphasis:** Agentic favors recoverability and governed derivation; Superpowers favors a tightly packaged coding loop |
| Parallel work | Plan tasks execute in order; parallelism is not a first-class general workflow | Dedicated parallel-agent workflow for independent problem domains | **Superpowers advantage:** clearer general-purpose parallel dispatch |
| Review | Independent design and closure moments, conformance mapping, `CANNOT VERIFY`, one append-only log, scoped re-review of corrections | Request/receive-review disciplines plus per-task spec and quality reviews and broad final review | **Agentic advantage in governance/audit; Superpowers advantage in immediate task-loop ergonomics** |
| Completion evidence | Claim-to-evidence: fresh proof after the final relevant edit, claim breadth matched to proof, delegated work verified on the diff | Verification-before-completion: evidence before any success claim | **Parity after Tranche A.** Agentic additionally ties “requirements complete” to Functional Spec acceptance criteria |
| Worktrees and branch finish | L3 isolation, explicit merge decision, destructive actions require exact human authorization; repository commands live in project guides | Detailed environment detection, worktree creation/setup/baseline, four finish choices and cleanup workflow | **Parity in outcome.** Superpowers is more command-operational; Agentic separates universal safety from repository-specific commands |
| Security | Security-sensitive work cannot be L1; L3 carries threat analysis and review traceability | No equivalent methodology-wide security triage or mandatory threat-model slot | **Agentic advantage** |
| Multi-domain governance | One shared spine across code, knowledge and marketing lenses, each with its own fidelity discipline | Software-delivery skill suite | **Agentic advantage for governed non-code work** |
| Skill authoring | Operative guides are source-faithful project/agent knowledge, not a general skill-authoring method | `writing-skills` applies TDD, discovery optimization and rationalization testing to skill creation | **Superpowers advantage:** Agentic has no equivalent general skill-authoring workflow |
| Optional governed backend | Standalone-complete; devPNT can add governed storage, proposals, semantic impact and team review without becoming the methodology | No comparable optional governance backend | **Agentic differentiator** |

## A — Agentic SDLC advantages to preserve

1. **Risk-proportional governance.** L1 remains one step; higher ceremony must earn its cost.
2. **One durable intent chain.** Vision, requirements, design, plan, implementation and evidence are traceable without relying on conversation history.
3. **Anti-myopia design.** Grounded names, capability-first architecture, exhaustive blast-radius enumeration and file-level impact precede implementation.
4. **Mechanical lifecycle and drift detection.** The validator checks facts that prompt discipline alone cannot reliably preserve.
5. **Security and human authority.** Security triage, threat analysis, proposal ownership and destructive-action guards are explicit.
6. **Standalone completeness with optional amplification.** devPNT strengthens the same process without becoming a second process spine.
7. **Reusable knowledge rather than plan-local copies.** Operative guides and the agent KB keep project rules source-faithful, versioned and referenced by pointer.

## B — Capabilities now at parity or absorbed

- RED/GREEN/REFACTOR and systematic root-cause debugging.
- Design-before-code and executable, file-specific implementation plans.
- Worktree isolation and explicit branch-finishing decisions.
- Fresh-context subagent implementation with independent review.
- Durable progress evidence and recovery after context compaction.
- Disciplined requesting and receiving of review findings.
- Fresh verification before completion claims.
- Rationalization tables and red-flag wording on the highest-drift rules.

These are Agentic SDLC mechanisms now. Their owners are its existing triage, phase, review and documentation contracts; Superpowers is inspiration, not a runtime dependency or a second authority.

## C — Superpowers strengths still worth selective study

1. **Test-honesty enforcement.** Its TDD discipline makes “watched the right failure” harder to evade. Adopt only the missing evidence rule, not another TDD gate.
2. **Debugging boundary evidence.** Pattern comparison and instrumentation across component boundaries can strengthen difficult investigations. Keep it conditional and privacy-safe.
3. **General parallel dispatch.** A dedicated test for task independence is useful beyond plan-driven feature implementation. Admission requires a concrete concurrency failure, not theoretical speed.
4. **Skill-authoring TDD.** Baseline agent failure → minimal instruction → adversarial re-test is a real capability absent from Agentic SDLC. It should remain separate from operative-guide distillation, which answers a different question.
5. **Operational finish ergonomics.** Superpowers gives a complete generic branch workflow. Agentic should keep universal safety in the skill and concrete commands in repository guides; improvements belong at that seam.

## Deliberate non-adoptions

- **Universal brainstorming before every creative action:** rejected because it overrides risk-proportional triage and makes trivial work pay L3-style design cost.
- **“Any chance a skill applies” as a second classifier:** rejected because Agentic SDLC permits one triage authority per kind of work.
- **Wholesale Superpowers pipeline adoption:** rejected because the mechanisms already absorbed have Agentic-native owners; importing the pipeline would create a competing process spine.
- **Competitor-defined artifacts or formats:** rejected by the product’s anti-coupling Non-Goal. Ideas may be studied; shipped formats may not depend on Superpowers.

## D — Agentic-specific frontier in this comparison

- Source-faithful operative guides with provenance, snapshots and drift detection.
- Agent-global knowledge base with project-over-agent precedence.
- One process spine shared across code, knowledge and marketing fidelity disciplines.
- Persistent Vision authority and precedent-based capability admission.
- Standalone-to-devPNT upgrade/downgrade without losing local documents or capability.

## Positioning

Superpowers 6.2.0 is the stronger focused execution toolkit: direct, modular and highly resistant to rationalization at the coding step. Agentic SDLC 1.26.1 is the broader governance system: proportional, documentation-first and mechanically checked, now with most core execution disciplines integrated under one durable process spine.

The product direction is therefore not “become Superpowers.” It is: retain Agentic SDLC’s governance and proportionality, adopt only execution mechanisms supported by observed evidence, and express them in Agentic-native owners so the objective and process authority do not change.
