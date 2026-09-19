---
description: Why project memory is shared by every lens while document authority and specialist workflows remain separate.
status: CURRENT
---
# ADR: Shared project memory, domain-owned work

**Status:** Accepted
**Date:** 2026-09-19
**Task ref:** F-057, ANALYSIS_sdlc_kb_integration.md

## Context

The owner requested a horizontal project view across software, marketing decisions
and plans, with memory available whenever any family skill is used. Previously the
KB validator alone carried graph/claim/corpus integrity, while code and marketing
could overlook those surfaces. Existing document indexes had domain-specific scope.

## Decision

Extract the existing KB machinery into a profile-neutral `knowledge.py` shared by
all three distributions. Keep domain profiles and marketing numerical validation in
their entry points. Every package carries `memory.md`; no sibling install is needed.

Generate `memory/INDEX.md` from original documents at the existing index step.
Optional topics metadata associates subjects across domains without creating graph
nodes or claims. Live lexical `recall` searches document metadata independently of
the saved catalog. Source status and authority are read in individual originals,
not aggregated into a work-state surface (Vision ruling r2).

## Alternatives considered

- Optional sibling KB invocation: retains installation coupling and partial checks.
- Run the whole KB workflow on every task: duplicates triage and ceremony.
- Copy every guide/decision into a KB corpus: creates competing sources.
- Automatic claim extraction: cannot certify source fidelity, approval or truth.

## Consequences

- All lenses can discover the same subjects and check the same knowledge formats.
- The specialist lens still owns ingestion/taxonomy, and marketing retains its
  evidence ledger and numerical gates. Memory does not approve decisions.
- Vendored validators now require three files; package allowlists and drift guards
  include the added module. Python 3.8-compatible output writing is retained.
- Catalog generation hashes eligible Markdown, adding local I/O at index/validation;
  no network or service. No mandatory full-corpus read by the agent per turn.
- Not a watcher, semantic search engine or DB synchronizer. Hybrid DB-only artifacts
  still require existing governed queries; accepted shadows are only local views.
- Existing projects gain the catalog at their next index. Sources and claim schemas
  are unchanged; no bulk extraction, migration or approval promotion occurs.
