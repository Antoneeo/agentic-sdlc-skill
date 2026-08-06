---
description: Why execution-integrity mechanisms inspired by Superpowers enter as evidence-gated tranches (A now, B opportunistic, C frozen), and why the enforcement-writing technique (rationalization tables) was adopted alongside them.
status: CURRENT
---
# ADR: Execution Integrity — tranche adoption + enforcement-writing technique

**Status:** Accepted
**Date:** 2026-08-06
**Task ref:** F-034 (owner-directed comparative study of Superpowers 6.2.0)

## Context
A firsthand study of all 14 Superpowers skills (MIT, Jesse Vincent; installed for comparison)
plus an external two-round specification (V1 reviewed FAIL, V2 reviewed PASS) identified
execution-discipline mechanisms this skill lacked. The repository's standing weight criterion —
a new gate enters only on an observed failure the existing gates don't catch, or as an
irreversible-damage guard — forbids wholesale adoption: ~6 mechanism clusters at once is the
ceremony accumulation the criterion exists to prevent.

## Decision
1. **Tranche A only, now:** (a) claim-to-evidence freshness (observed: a closure artifact
   claimed "check clean" while the gate was NOT CLEAN — REVIEW_LOG F-033); (b) scoped
   re-review of review-driven corrections (observed: reviews take ≥2 rounds because the fix
   is unreviewed work; F-033 already practiced the scoped R2); (c) destructive branch/worktree
   guards (irreversible-damage class, admitted on risk). All as wording in existing owners —
   SKILL.md Phase 5, `review.md` — no new file, no validator change.
2. **The enforcement-writing technique** — rationalization tables (`Excuse | Reality`) and
   red-flag stop-words — adopted as a style on the rules this change touches (triage,
   verification). Superpowers' real asset is HOW it writes rules: it pre-refutes the exact
   escape thought at the moment of temptation; our own vision-battery round 11 recorded the
   same phenomenon ("every fix worded against the seen attack fell to a one-word reword").
3. **Reviewer-side:** `CANNOT VERIFY` becomes a first-class reviewer output (skill `review.md`
   + the three devPNT reviewer agents), and pre-judging findings in a review request is
   forbidden. Delegated work is verified on the diff, never on the report.
4. **Tranche B** (tdd/debugging strengthening) waits for the next admitted touch of those
   overlays. **Tranche C** (dispatch workspace/ledger state machine, BASE..HEAD packaging,
   validator extensions) stays frozen until a real failure (re-dispatch after compaction,
   truncated task review, dispatch context overload) reopens it as its own L3.

## Alternatives considered
- **Adopt the full spec at once** — rejected: violates the weight criterion; the heaviest
  cluster (dispatch machinery) models an autonomous-run pattern with no observed failure here.
- **Reject everything (we have reviews/tests already)** — rejected: the F-033 false-CLEAN and
  the 2-round observation are real failures the existing wording did not prevent.
- **New `verification.md` / `finish.md` files** — rejected: existing owners (Phase 5,
  `review.md`) hold the rules without ambiguity; new files are lifecycle machinery the gap
  does not require.
- **5-round fix loop with model escalation (Superpowers' shape)** — rejected: the existing
  cap of 3 with surface-to-human stays; escalation-at-cap can be revisited if cap-3 stalls
  are ever observed.
- **Universal process triggers ("1% chance → must invoke", design doc for every todo)** —
  rejected: anti-proportional; Rule Zero triage is this skill's spine.

## Consequences
- **Pro:** the three observed/irreversible gaps close at wording cost; the correction loop the
  repo already practices becomes doctrine (lens-neutral — kb/mkt artifact reviews inherit it);
  rationalization tables give the highest-drift rules a pre-refutation layer.
- **Con / risk:** SKILL.md grows by ~2 bullets + 1 table; the technique's value is measurable
  only over time (REVIEW_LOG). Provenance: concepts reimplemented, no text copied — no MIT
  notice obligation triggered.
