---
description: ADR - doctrine leaves the mandatory read by RELOCATION behind a triggered pointer, never by deletion, and a relocation must enumerate its inbound citations. Rejected - deleting the seam, compressing prose, a filename-only pointer, and extracting all three lenses blind.
status: CURRENT
---
# ADR: doctrine leaves the mandatory read by relocation, never by deletion

**Status:** Accepted
**Date:** 2026-09-11
**Task ref:** F-051 (ANALYSIS_mandatory_read_diet.md)
**Digest:** F-051 — `SKILL.md` had grown to 50 KB that every session must read while the catch rate held flat, but no per-paragraph benefit measure exists to prune by; decision: doctrine leaves the mandatory read only by RELOCATION into a triggered support file, the pointer must carry trigger AND consequence, the weighing of what stays is pinned executably in the battery, and a relocation must enumerate its INBOUND citations; rejected deletion, prose compression, a filename-only pointer, and doing all three lenses blind; residual — the Standalone saving (−9.4%) is paid for by a Hybrid surcharge (+3.9%), and kb/mkt still carry their seam inline.

## Context

`benefit` (F-050) made the cost side visible for the first time: `SKILL.md` had
grown from 4.8 KB to 50 KB in four months, read in full by every session, while
the measured catch rate (68% of findings before code exists) had not moved in
three releases. Cost was rising against a flat benefit.

The obstacle is that **no per-paragraph benefit measure exists**. The catch rate
is an aggregate; nothing says which rule caught what. So "this reads verbose" is
exactly the unmeasured judgement the preceding units learned to distrust, and
pruning on it would have been the same mistake in the opposite direction.

## Decision

1. **Doctrine leaves the mandatory read only by RELOCATION**, into a support
   file reached by a pointer — never by deletion. The decision rule is: *delete
   no rule; move only what a session provably cannot use, and only where the
   trigger that summons it back is mechanical.*
2. **The pointer carries the trigger AND the consequence**, not a filename. A
   reader must know when to follow it and what they lose by not following it,
   including any rule that now exists in exactly one place.
3. **The weighing is pinned executably.** The blocks judged to earn their bytes
   are a list in the harness and the battery; a future diet that removes one
   must delete a line of that list to go green. The cost of cutting a rule is
   explicit rather than silent.
4. **Conservation is proven at BYTE level**, not heading level: the moved region
   must survive as one contiguous, character-identical block.
5. **A relocation must enumerate its INBOUND citations** — who cites the moved
   sections — which is the blast-radius axis a move has and a normal change does
   not. This unit's first draft omitted it and shipped a stale citation.

## Alternatives considered

- **Deleting the Hybrid seam** — rejected: it is real doctrine that prevents a
  second source of truth, and it carries the only statement of the
  never-auto-accept human-approval rule.
- **Compressing prose across the file** — rejected: without a per-paragraph
  benefit measure this is guesswork, and the project's own doctrine holds that
  the *why* is what makes a rule survive a motivated reader. The bytes saved
  would come out of the part that does the work.
- **A filename-only pointer** — rejected: a reader with no trigger and no
  consequence has no reason to follow it, which converts a relocation into a
  deletion with extra steps.
- **Extracting all three lenses at once** — rejected as blind: kb and mkt have
  their own Hybrid material and their own profiles, and doing them unreviewed to
  save a round is how a move becomes a loss. Recorded as a named follow-up.

## Consequences

- **Pro:** the mandatory read falls for the first time (−4,722 B, −9.4%) with
  zero rules removed; the weighing is executable, so the next diet argues with a
  test instead of with prose; and `benefit`'s cost term is now a number that has
  been shown to go down.
- **Con / risk:** the Hybrid session's mandatory read RISES by 1,935 B (+3.9%) —
  a Standalone saving paid for by a Hybrid surcharge, disclosed rather than
  discovered. A Hybrid session that ignores the pointer loses the ownership
  matrix and the never-auto-accept rule; the mitigation is the pointer's
  consequence clause and a battery pin on it, not a guarantee. And kb and mkt
  remain un-dieted until the follow-up lands.
