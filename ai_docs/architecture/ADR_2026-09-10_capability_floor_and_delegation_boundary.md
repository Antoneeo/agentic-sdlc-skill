---
description: ADR - the capability dimension gets an owner. review.md owns a capability floor (independence wins when it conflicts), dispatch.md owns the delegation boundary, and REVIEW_LOG gains `model` so both are falsifiable. Rejected - the floor in dispatch.md, routing by triage level, a third tier now, abstention when the only rung is below the floor.
status: CURRENT
---
# ADR: The capability floor and the delegation boundary

**Status:** Accepted
**Date:** 2026-09-10
**Task ref:** F-048 (ANALYSIS_capability_tiers.md)
**Digest:** F-048 — the model-capability dimension was unowned in Standalone (only devPNT had a tier table), so a gate could run below the capability its judgement needs and still report as independent; decision: review.md owns a role→floor table with the threshold-signal rule and the "independence wins" arbitration, dispatch.md owns the family-wide delegation boundary, REVIEW_LOG gains `model`; rejected the floor in dispatch.md (surfaced everywhere as opt-in-L3-only), abstention when the only rung is below the floor, routing by triage level, a third tier before measurement, a second log table for Hybrid; residual — the operational search-delegation trigger stays deferred.

## Context

Assessment against external research (2026-09-10) found the capability dimension
unowned in Standalone. `dispatch.md` tiered implementer subagents (economy, deep
after two `verify_result: fail`); `review.md` asked only for "a different model
from the author's". Nothing named a minimum capability for any role, so a client
could bind both reviewer roles to a cheap model and no rule would notice — and a
gate that cannot do its job still returns a verdict, which is worse than no gate
because it certifies. Two further gaps followed from the same absence: the
boundary of what may be delegated at all lived only in one machine's agent
memory, and the review log recorded rounds and findings but never what produced
them, so neither policy could be falsified.

Two external findings shaped the design. Cascade routing (FrugalGPT, RouteLLM)
cuts cost substantially but only where a **threshold signal** can score the cheap
answer and escalate. And multi-agent delegation costs 3-15× more tokens than a
single agent: it buys context isolation and independence, never savings.

## Decision

1. **`review.md` owns the capability floor** — it owns the gates the floor binds.
   A role→minimum-tier table, tiers as client-relative capability levels, never
   provider names. The rule underneath: **a tier may be lowered only where a
   threshold signal exists** (`task.verify`, a test, a diff against a spec, an
   assertion harness). Where the output is judgement and nothing scores it, the
   floor is the whole policy. `dispatch.md` cites the floor for the implementer
   case rather than restating it.
2. **When independence and capability conflict, independence wins.** A below-floor
   *independent* reviewer catches the class the author is structurally blind to;
   a self-pass catches none of it. The floor then requires **disclosure, not
   abstention**: the row records `below floor: <reason>`. A permission-gated
   higher rung is already r18's case; a client with no capability choice records
   `single (client exposes no choice)`.
3. **`dispatch.md` owns the delegation boundary**, declared family-wide and not
   gated by the opt-in dispatch trigger: two axes (output falsifiable cheaply ×
   reads ≫ report), a never-delegate list, and the delegability condition — a
   task whose brief cannot be expressed as **pointers** is not delegable, because
   a brief carrying content pays those tokens twice.
4. **`REVIEW_LOG` gains `model`**, and "one schema for both modes" is redefined as
   one required CORE plus each mode's own realization columns — a devPNT row
   carries no `reviewer` column, so one identical column list was never true.

## Alternatives considered

- **The floor in `dispatch.md`** (the first draft) — rejected at design review:
  all three `SKILL.md` surface `dispatch.md` as opt-in L3 dispatch, and its own
  Trigger says "Never for L1/L2", so the readers who most need the floor — anyone
  running a review gate without dispatch — would never arrive. A scope note does
  not repair a container whose title and trigger contradict it.
  **Why the boundary then stays in `dispatch.md` while the floor did not**: they
  fail differently when a reader does not arrive. An agent that never reads the
  floor still runs the gate, and runs it wrong while reporting it as independent —
  a silent false certification. An agent that never reads the boundary simply does
  not delegate, which is the safe default the skill already has (same-session is
  the default everywhere). The floor's non-arrival is a defect; the boundary's is
  a no-op. That asymmetry is why one moved and the other did not, and why the
  three `SKILL.md` pointers are a sufficient mitigation for the boundary alone.
- **Routing by triage level** (L1→cheap, L3→strong) — rejected: an L3 is mostly
  mechanical tasks with a few judgement ones, so routing by level sends the whole
  unit to the strongest model and saves nothing where the volume is.
- **A third tier now** — deferred: the research warns reported routing gains may
  be evaluation artifacts, and adding a tier to a machine that does not yet
  measure is belief, not policy. `model` is what makes measurement possible.
- **Abstention when the only rung is below the floor** — rejected: it would make
  the floor delete reviews on exactly the clients least able to afford losing
  them, trading a disclosed weak review for no review at all.
- **Text in the id of the tier vocabulary / a second log table for Hybrid** —
  rejected: readers locate columns by header, which `templates.md` already owns.

## Consequences

- **Pro:** the gate the method rests on can no longer be silently degraded; the
  delegation boundary travels with the skill instead of living in one machine's
  memory; both policies become measurable against `revise_rounds` and
  `findings_real`.
- **Con / risk:** one mandatory cell per review row (ceremony cost disclosed and
  accepted by the owner, 2026-09-10, per the Vision's "no ceremony ratchet"); the
  floor's value depends on clients exposing a capability choice at all, and where
  they do not it degrades to disclosure; and the boundary settles classification
  only — *when* to reach for a delegated search pass is a deferred unit, so the
  read-side context win the research points at is named but not yet operational.
