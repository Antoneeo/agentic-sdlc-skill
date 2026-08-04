---
description: Why the actor-facing interaction is contracted between the use cases and the solution — a conditional ANALYSIS section with an authority split, not a new document kind and not a validator rule.
status: CURRENT
---
# ADR: The Interaction Contract layer

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

A conditional `## Interaction Contract` section in the ANALYSIS, between
`## Use Cases / User Needs` and `## Capability Ledger` (Hybrid: inside the E-ISP,
sequenced D-UC → D-IC → P-TM → E-ISP), with:

- **Trigger owned by the `templates.md` section comment** (single home): a surface
  through which an actor *acts on or perceives* the system; not fired → one line.
- **Authority split**: the contract binds observable behavior only (actor action →
  system response → outcome, per use case, plus view states); feasibility notes are
  non-binding hypotheses the Impact confirms or refutes. After design approval a
  contracted path changes only as a user-approved scope change.
- **Pattern reuse by default**: the as-is inventories existing interaction idioms;
  a new idiom is a declared decision.
- **Enforcement by review, not by validator**: a lens-keyed clause in the shared
  `review.md` (fires only in the lens whose template defines the section), plus an
  invariant test pinning the wiring. The solution inherits the interaction; it
  never generates it.

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
