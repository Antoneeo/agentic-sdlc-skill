---
description: Why the actor-facing interaction is contracted between the use cases and the solution — a conditional ANALYSIS section whose flow names the components it traverses (never their mechanism), not a new document kind and not a validator rule.
status: CURRENT
---
# ADR: The Interface Contract layer

> **Refined 2026-08-05 (v2):** the flat action→response→outcome model + "no components" split were evolved to the responsibility-level flow that names components; see `ai_docs/solutions/ANALYSIS_interaction_contract.md` ## Evolution v2.

**Status:** Accepted
**Date:** 2026-08-04
**Task ref:** F-032 (`solutions/ANALYSIS_interaction_contract.md`)

## Context

No artifact bound use cases to the surfaces that realize them: use cases stay at
intent level (correctly — requirements must not presuppose an interface), and the
Impact/E-TDD speak component vocabulary. The interaction was therefore invented at
implementation time, the review's "actor UX fit" check had no object, and the
Vision's per-actor "good UX =" clauses had no downstream contract. The Vision
counts ceremony — including reading cost — as real cost, so any fix had to stay
proportional.

## Decision

The actor-facing interaction is contracted between the use cases and the solution, as a conditional `## Interface Contract` section in the ANALYSIS (in Hybrid, inside the E-ISP). Per use case whose surface the change touches, the contract states: the actors and surfaces; **the information & processing flow — the actor acts → the flow it triggers, naming the components it traverses as responsibility-holders → what returns** (responsibility level, never mechanism); the required affordances; the required feedback (universal — error and intermediate states, and a software actor's return status); the architectural constraints the surface must coexist with (read, not redesigned); and the surfaced feasibility flags. Authority split: the contract names the components in the flow but never their mechanism or file-level design (that is the Impact's vocabulary); after approval a contracted change is a scope change the user approves. It defines needs, never realization.

## Alternatives considered

- **A new document kind (`IC_[feature].md` / governed D-IC now)** — rejected:
  fragments the unit of change, adds a file lifecycle for what is one design
  concern; the devPNT governed artifact is companion work in the devPNT repo.
- **Extending E-TDD/Impact with UI blocks only** — rejected: keeps the interaction
  in component vocabulary and downstream of solution choices; the UX must be
  contracted before the solution so the E-ISP inherits it.
- **Validator-enforced section presence** — rejected for this unit: the trigger is
  semantic (did the change touch an actor-facing surface?), so a mechanical check
  either nags every L3 retroactively or blesses a one-line dodge. An epoch-gated
  advisory on the F-020 pattern is named follow-up.

## Consequences

- **Pro:** UX divergence becomes visible at design review, before code; use cases
  gain a named realization path; threat modeling gets its surface list handed to
  it; interaction idioms stop drifting per feature.
- **Con / risk:** one more conditional section at L3 and its doctrine reading cost
  (disclosed and explicitly accepted by the owner, rulings r16); Standalone's only
  backstop for a skipped contract is the design-review clause until the epoch-gated
  advisory ships; the trigger's verb pair will need field mileage.
