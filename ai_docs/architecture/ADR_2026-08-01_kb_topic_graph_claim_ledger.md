---
description: Why kb's knowledge method is a claim ledger under a topic graph, detect-and-hold, inside the entry point.
status: CURRENT
---
# ADR: kb knowledge method — claim ledger + topic graph, detect-and-hold

**Status:** Accepted
**Date:** 2026-08-01
**Task ref:** F-024 / F-025 (`solutions/ANALYSIS_kb_knowledge_method.md`, `solutions/ANALYSIS_claim_ledger.md`)

## Context

kb shipped three method files that stated verdicts (EXISTS/INADEQUATE/MISSING,
"determine the source of truth") with no method behind them; the owner held the release
of all three family packages until kb could do its job. Designing the method surfaced
four load-bearing decisions, each forced by a review finding or an owner ruling.

## Decisions

1. **The unit of knowledge is the claim, not the document.** One falsifiable assertion
   per row, with its own source locator, provenance and conflict state. Documents cannot
   be reconciled; assertions can.
2. **The machine detects and holds; it never decides** (owner ruling). Conflicts become
   symmetric CONTESTED sets; resolution comes only from new information — a newer source,
   or a practitioner ruling whose mandatory `basis:` states the fact they know. A
   preference is not a fact; a basis-less ruling is refused exactly as a `derived_from`-less
   synthesis. Rulings are challengeable: later contradicting evidence re-opens the set
   carrying the ruling's basis.
3. **Identity is location, never wording.** `id = sha256(source#locator#qty)`, with
   locators addressing a STORED canonical extraction (content-addressed beside the
   original), so ids survive LLM re-extraction and a human can reopen the exact span.
   The qty component keeps two figures asserted by one sentence distinct.
4. **Everything lives inside the kb entry point** (`sdlc_check.py`), which forwards any
   spine subcommand it does not intercept by delegating to the spine's own parser. The
   npm `files` allowlist, the CI recipe and the golden copied-file test all pin the
   validator at exactly two files; a third module would never reach an installed user.

## Alternatives considered

- **Automatic precedence ladder** (GIVEN beats DERIVED, newer beats older, ten cells) —
  rejected: it needed columns the rows do not carry, produced order-dependent outcomes on
  three-way conflicts, and in one cell destroyed evidence. Deciding was the defect.
- **GraphRAG / RAPTOR-style clustered hierarchies** — rejected: both re-cluster the
  corpus on each run, so node identity does not survive re-ingestion; a curated second
  brain needs stable, referencable topics.
- **Text-keyed claim ids** — rejected: an LLM re-extraction paraphrases and every id
  moves; dedup then re-inserts everything.
- **A persisted sqlite graph artifact** — rejected: the one derived artifact that cannot
  be verified by regenerate-and-compare, and a torn one reports green. The graph is
  rebuilt in memory on every run — and as implemented that is plain Python structures,
  not in-memory sqlite: `sdlc_check.py` imports no `sqlite3` at all.
- **Computed per-node coverage (STUB/PARTIAL/FULL)** — rejected: derived-on-demand
  collection of per-document state is the work-management Non-Goal's own named case.

## Consequences

- **Pro:** conflicts cannot be resolved silently (symmetry is machine-checked; flipping
  one cell fails); every figure traces to a reopenable span; existing kb projects see
  byte-identical validator output (golden baseline +9/−0 with a frozen containment
  fixture); acceptance proven on the Eclosion corpus — 26 claims, a real GIVEN-vs-GIVEN
  capacity conflict held and resolved by an owner ruling with basis.
- **Con / risk:** line-granular locators cannot split two qty-less claims on one line
  (they must be authored as one compound claim); ingestion is serial in v1 (dispatch.md
  offers no per-path guarantee — parallel extraction needs a disjoint-`paths` check, a
  SHARED change); the entry point grew from ~80 to ~850 lines, the price of the two-file
  constraint.
