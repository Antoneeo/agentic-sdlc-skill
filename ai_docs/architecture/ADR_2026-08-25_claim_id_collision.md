---
description: Why two distinct assertions about one span are refused rather than disambiguated — the claim id stays a pure function of (path, locator, qty), and the collision is named instead of engineered away.
status: CURRENT
---
# ADR: the claim id collision is named, not disambiguated

**Status:** Accepted
**Date:** 2026-08-25
**Task ref:** F-035 (field report 2, item C — the reporter delegated this call explicitly)

## Context

`kb_claim_id` is `sha256(path#locator#qty)[:12]`, with the claim text **excluded on
purpose**: a paraphrase must not mint a new identity, and — the load-bearing
consequence — the same assertion cited at the same span mints the **same id in every
project**. `portability.md` rests on exactly that: `import` recognises an
already-present claim by id rather than by comparing text, which is what makes
de-duplication mechanical instead of a judgement call.

The price surfaced in the field. A single sentence can assert two things. Two rows
written by hand, saying different things, citing the same span with the same qty, mint
the same id — and the validator refuses the pair. The design forbids the case by
construction, and the only escapes available to the practitioner are to widen a
locator, merge the rows, or **distort the evidence until the hash differs**.

Worse, the message accused the wrong defect: *"duplicate id … uniqueness is global
across topics/"* describes a copy-pasted row. The reporter's rows were neither copied
nor duplicated, so the message sent them hunting for something that was not there.

## Decision

1. **The id function does not change.** No disambiguating ordinal, no text in the hash,
   no per-project counter. Cross-project id stability outranks the ability to express
   two assertions on one span, and the tests now pin two id values as constants so a
   future edit cannot move them quietly.
2. **The collision is diagnosed correctly.** The duplicate-id check branches on the
   **claim text**: same id with the same text is a copied row (the existing uniqueness
   message stands); same id with different text is the collision, and the message says
   so, names the other row, explains that the id excludes the text on purpose, and
   prescribes the two legitimate repairs — widen a locator, or merge the rows —
   while explicitly ruling out editing the qty to break the tie.
3. **The limit is written down** in `distillation.md` §2 beside the `id` column, in the
   same form the file already uses for `original_sha256`: a constraint the design
   accepts, stated out loud, rather than a surprise met at the validator.

The discriminator is the text, not the source: same first source and same qty are
shared by a copied row *and* by a collision — they are implied by the id itself, so
they separate nothing. The first draft of this design got that wrong and the design
review caught it.

## Alternatives considered

- **A disambiguating ordinal at equal `path#locator#qty`** (the reporter's "full fix")
  — rejected. It makes the id depend on how many rows a project happens to have written
  about that span, which is per-project state by construction. Two projects holding the
  same claim would then mint different ids, and `import`'s recognition-by-id degrades to
  text comparison — the judgement call the id was designed to remove.
- **Include the claim text in the hash** — rejected for the reason the exclusion exists:
  a re-extraction that paraphrases would mint a new identity for the same fact, and the
  ledger would accumulate duplicates that no check can relate.
- **A `TRANSCRIBED`-style extra key in the payload** (some discriminator that is not an
  ordinal) — rejected: any component that is not derivable from (path, locator, qty) in
  another project reintroduces the same divergence as the ordinal.
- **Leave the message generic and document the case only** — rejected. The message is
  where the practitioner meets the constraint; documentation they have already read
  does not help at the moment the check fires.

## Consequences

- **Pro:** `portability.md`'s mechanical de-duplication keeps its guarantee, and it is
  now pinned by tests rather than by convention.
- **Pro:** the practitioner meeting a collision is told what actually happened and which
  two repairs are legitimate — including which one is not.
- **Con / risk:** one span still cannot carry two assertions at the same qty. The
  workaround costs a locator revision, which is real work on a large corpus. The limit
  is now declared, so it is a known constraint rather than a trap; if it proves common
  in practice, the decision to revisit is the ordinal's cost against portability, and
  this ADR is what that revision supersedes.
- **Con / risk:** the collision branch reads the previously-seen row's text. That row is
  already held in `all_rows`, so the cost is a dictionary lookup and nothing else.
