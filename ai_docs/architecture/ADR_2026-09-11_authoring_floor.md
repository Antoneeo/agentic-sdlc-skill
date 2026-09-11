---
description: ADR - the capability floor reaches the session that authors, but binds DISCLOSURE rather than routing, fails open, and yields to the independence arbitration when no better rung exists. Rejected - forbidding the double-below-floor state outright, claiming log checkability without a column, and naming provider models in the READMEs.
status: CURRENT
---
# ADR: the floor reaches the author, as disclosure

**Status:** Accepted
**Date:** 2026-09-11
**Task ref:** F-049 (ANALYSIS_authoring_floor.md)
**Digest:** F-049 — F-048's capability floor bound the review gates and the dispatched subagents but never the session that AUTHORS, though authoring is the purest case its own criterion describes; decision: the floor gains an authoring row and a session rule, binding DISCLOSURE rather than routing (a user-set session cannot re-tier itself), failing open where the tier is undeterminable, disclosed once per session in the review row's existing `reviewer`/`notes` cell, and yielding explicitly to "independence wins" where no rung at or above the floor exists; rejected an outright ban on the double-below-floor state (it contradicts that arbitration and pushes toward the abstention it rejects), a checkability claim the log has no column to support, and provider names in the READMEs; residual — the rule's reach is thin, because a session knows its model NAME and the skill maps no name to a tier, so the reliably working half is the user-facing README.

## Context

F-048 shipped a capability floor titled "which tier may run this GATE". Asked how
an agent invoking the skill from a user-set model behaves, the honest answer was
that the floor did not reach it: the table named review roles and dispatch roles,
never the session that authors the Vision, the analysis, the use cases and the
threat model — which is the purest case of "judgement whose wrongness no check can
see", and which `dispatch.md`'s never-list forbids moving elsewhere. The doctrine
constrained the reviewer that catches an omission and not the author that makes it.

## Decision

1. **Authoring a governed artifact is a deep-floor role**, as a parsed row in the
   floor table.
2. **A session's floor is the highest floor among the roles it performs itself** —
   but the remedy is **disclosure, not routing**: the session was chosen by the
   user before the agent existed and cannot re-tier itself mid-run.
3. **Fails open, and says how thin its reach is.** A session knows its model name;
   tiers are deliberately client-relative and nothing here maps name to tier, so
   the rule fires only where a session can recognize its own tier. Where it
   cannot, it owes nothing. The reliably working half is the user-facing guidance
   in the three package READMEs.
4. **Disclosed once per session, in existing cells** (`reviewer`, or Hybrid's
   `notes`) — no new column, which is what the accepted ceremony bought.
5. **The double-below-floor combination is discouraged, not forbidden**: where no
   independent rung at or above the floor exists, *When independence and
   capability conflict* governs, the review still runs, both disclosures are
   recorded, and the result is the worst admissible state — honestly labelled.

## Alternatives considered

- **Forbid the double-below-floor state outright** (the first cut) — rejected at
  review: it contradicts F-048's arbitration in a configuration that arbitration
  itself names, and, naming no remedy, pushes the agent toward the abstention
  that rule explicitly rejects.
- **Claim the state is checkable in the REVIEW_LOG** — rejected: the log's
  `model` cell records the REVIEW's tier and no column holds the authoring
  session's, so the claim was unkeepable. Either record it in existing cells or
  do not promise visibility; this takes the former.
- **Name provider models in the READMEs** (the design's own §Security plan) —
  rejected in implementation: a name dates faster than the guidance, and the
  criterion plus worked examples is actionable without one.
- **Route the authoring session** — impossible by construction.

## Consequences

- **Pro:** the gate the method rests on is no longer constrained only downstream
  of the work it judges; the user now has a stated criterion for the choice only
  they can make; and the forbidden combination is named without creating a
  contradiction.
- **Con / risk:** the agent-facing half is thin and admits it — a cheap session
  is precisely the one least likely to run the check; and the disclosure lands in
  a free-text cell, so it is readable by a human and not parseable by a script.
