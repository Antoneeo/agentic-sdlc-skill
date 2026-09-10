---
description: ADR - kb claim-row atomicity is enforced by doctrine + a fallible note, never by changing the id function; bundled rows are repaired by split-as-supersession. Rejected - text in the id hash, error-level plurality lint, in-place row splitting, sub-line locator grammar extension.
status: CURRENT
---
# ADR: Row atomicity by doctrine, split by supersession

**Status:** Accepted
**Date:** 2026-09-08
**Task ref:** F-047 (ANALYSIS_kb_row_atomicity.md)

## Context

Field report (103-artifact corpus, 1785 rows): a claim row extracted from one
reviewer comment carried several assertions about several subjects; every
faithful citation of it then asserted what the source did not (borrowed
capability, wrong actor, subject ambiguity — or silent omission by the writer
avoiding them). No rail could see it: the row was legal, the citation textually
exact. Worse, the id-collision remedy ("widen … or merge the two rows")
actively recommended manufacturing such bundles, and no doctrine described how
to split one.

## Decision

1. **The id function stays provenance-based** (`sha256(path#locator#qty)`, text
   excluded). Atomicity is a property of MEANING, enforced where meaning is
   judged: extraction doctrine (one row asserts one thing; narrowest supporting
   span), the ingestion/answer-side reviews (citation scope test), and a
   heuristic `[note]` in the validator — never the exit code.
2. **Bundled rows are repaired by split-as-supersession**: N atomic rows on
   narrowed spans (ids distinct by construction), the bundle `SUPERSEDED
   <id1>, <id2>, ...` with text intact, cascade to every citer. The state
   grammar already accepted successor lists; the documentation now says so.
3. **Sub-line precision uses the existing `p=<page>@<a>-<b>` form** on the
   stored `.txt` (one page when form-feed-free) — no locator grammar change.

## Alternatives considered

- **Include the claim text in the id hash** — rejected: kills cross-project
  de-duplication (`portability.md`) and makes every paraphrase a new identity;
  the collision the exclusion causes is now read as a SYMPTOM of a non-atomic
  row instead of a nuisance to silence.
- **Error- or warning-level plurality lint** — rejected: text cannot prove
  plurality; a failing check on legitimate compound sentences forces evidence
  distortion, the exact repair the ledger forbids. A note hints without gating.
- **Split rows in place (edit text/locator, keep the row)** — rejected: erases
  provenance history and breaks every existing citation silently; supersession
  keeps the bundle's text and routes citers through the cascade worklist.
- **Extend the locator grammar with sub-line offsets for `L<a>-<b>`** —
  deferred, not needed: `p=1@<a>-<b>` already addresses characters of stored
  `.txt` bytes; a grammar change would touch id stability, anchor, coverage and
  goldens for no gained capability.

## Consequences

- **Pro:** the four field defect kinds each get a named owner (doctrine, split
  move, scope test, note); the collision remedy now pushes toward atomicity
  instead of away from it; zero mechanical behavior gated on an unprovable
  property.
- **Con / risk:** existing bundled rows heal only when someone splits them —
  the note surfaces candidates, but the repair stays manual; the heuristic will
  miss bundles phrased without its tell-strings (accepted: it is a hint, and
  the reviews own the property).
