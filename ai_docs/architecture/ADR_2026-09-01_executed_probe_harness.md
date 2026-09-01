---
description: ADR - behavioural claims in L3 designs derive from executed probes kept as a repo-shipped harness (ai_docs/solutions/harness_[feature]/), with a lens-gated reviewer clause; rejected - scratchpad probes, prose-only duty, family-wide reviewer check.
status: CURRENT
---
# ADR: Executed-probe harness for behavioural design claims

**Status:** Accepted
**Date:** 2026-09-01
**Task ref:** F-045 (ANALYSIS_review_convergence_doctrine.md)

## Context

Eight consecutive design-review FAILs (2026-08 field session) shared one finding
class: the design described intent, not behaviour — claims of the form "the code
today does X" written from reading the source, stated with confidence, wrong.
Reading is structurally insufficient for behaviour: an author who only reads
cannot see that a called function does not exist, or that the exception they
reasoned about is caught two frames down. Once each behavioural claim was
executed first, the artifact passed in one round and probed claims held in every
subsequent round.

## Decision

1. **Execute-Before-Specify** (SKILL.md §3, code lens): every behavioural claim
   about existing code in an L3 design artifact derives from an executed probe,
   run against the real system in its real states, before the prose is written.
2. **The probes ship as a harness in the repo** — `ai_docs/solutions/harness_[feature]/`
   — not in a session scratchpad: the reviewer re-runs assertions instead of
   re-deriving claims, and every later revision re-verifies them for free.
3. **A probe must be able to fail**: shown red first (condition or state negated),
   then green — `tdd.md`'s RED gesture applied to the experiment. A probe that
   cannot fail establishes nothing (vacuous-assertion guard).
4. **Proportionality**: the duty covers claims the design rests on; structural
   facts (a file exists, a signature, its callers) stay with blast-radius
   enumeration.
5. **A lens-gated reviewer clause** (review.md §Reviewing, shared spine) owns
   three findings: claim without probe, harness absent with behavioural claims
   in prose, probe no longer passing. It fires only in the lens whose SKILL.md
   defines the duty — the code lens today — and self-disarms elsewhere, like the
   existing UC/FS/IC/Ledger clauses.

## Alternatives considered

- **Probes in the session scratchpad** — rejected: a scratchpad dies with the
  session; the reviewer cannot re-run what no longer exists, and every revision
  re-derives the claims from scratch.
- **Prose-only duty without the harness convention** — rejected: an unshipped
  probe is unfalsifiable after the fact; "I ran it" becomes the same
  uninspectable claim as "I read it".
- **Family-wide reviewer check (not lens-gated)** — rejected: kb and mkt
  SKILL.md define no probe duty, so the check would fail every kb/mkt artifact
  on a rule their lens never states; the established lens-gating pattern in
  review.md handles exactly this.
- **Requiring red-run evidence in the review** — rejected as weight without
  yield: the reviewer already re-runs AND reads the probe, so a vacuous
  assertion is contestable; demanding recorded red runs would add ceremony to
  every probe for the rare dishonest one.

## Consequences

- **Pro:** the claim-rot finding class leaves the review loop (field data: eight
  rounds → one); wrong probes stay possible but become inspectable and
  falsifiable objects, unlike wrong readings, which leave nothing to contest.
- **Con / risk:** harness directories accumulate in `ai_docs/solutions/` with no
  lifecycle of their own yet (no Write Triggers row — left open at closure);
  probe maintenance is a new, small cost on L3 revisions.
