---
description: Consult before changing shared-memory discovery, docs-root resolution, or validator composition across the three distributions.
status: CURRENT
source_kind: code
source: F-057 knowledge.py and code, KB, marketing entry-point excerpts; paths and symbols are labelled in the snapshot.
distilled_from: ai_docs/reference/.sources/shared-project-memory-09bc631b.md
source_hash: 09bc631bc1aabee2348e2abc3018826747845fa1fecb79486d40019fa6c40d6f
topics: [shared-memory, validation, domain-routing]
---
# Guide: Shared project memory

For maintainers changing discovery or validator integration. This is the implementation
map; `memory.md` in each installed skill owns agent usage, and
`architecture/ADR_2026-09-19_shared_project_memory.md` records the architectural choice.

## Control and data flow
[source: shared-project-memory-09bc631b.md#distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py:main]

Code and KB entry points delegate to `knowledge.main`. Marketing keeps its own
index and numerical commands and forwards other commands to the common module.
Its validate/check result combines marketing findings with `kb_validate_surface`;
do not replace one result with the other. Root discovery uses the core resolver
in both paths; ambiguous roots fail instead of being merged.

## Discovery is not knowledge extraction
[source: shared-project-memory-09bc631b.md#skills/agentic-sdlc-skill/scripts/knowledge.py:memory_records]

`memory_records` reads README plus Markdown under `MEMORY_DIRS`. It excludes hidden
and harness subdirectories, generated indexes, raw corpus and audit logs. It returns
path, domain, optional topics, description/title and a raw-byte SHA256; no document
state or claim is generated. Domain falls back to README's `default_domain`, then
`code`. Changing this inventory changes what every lens can discover.

## Index and recall have different freshness contracts
[source: shared-project-memory-09bc631b.md#skills/agentic-sdlc-skill/scripts/knowledge.py:memory_recall]

`index` writes the catalog; there is no watcher. `recall` rebuilds metadata in memory
and requires every query word to occur somewhere in the first four fields, ignoring
case. It does not search bodies or interpret meaning. No result establishes only
that metadata did not match. Readers must open originals to assess evidence and status.

## Validation and confinement
[source: shared-project-memory-09bc631b.md#skills/agentic-sdlc-skill/scripts/knowledge.py:memory_validate]

An existing catalog must match regenerated content; an absent catalog is allowed for
legacy projects. Unsafe catalog output paths fail. `_memory_safe` checks resolved
confinement, symlinks and junctions when the Python runtime exposes `is_junction`.
Source edits, deletions and even byte-level line-ending changes can stale the catalog.
Regenerate it after checkout conversion rather than treating its fingerprint as a
semantic digest. Snapshot freshness does not prove this guide still matches live code.

## Composition traps
[source: shared-project-memory-09bc631b.md#skills/agentic-sdlc-skill/scripts/knowledge.py:kb_cmd_check]

Code/KB run the core check and then shared memory, graph and corpus checks. The core's
printed CLEAN line precedes those additions: use the final exit code and all findings,
not that banner alone. `validate` is lighter than `check`; a successful catalog check
does not certify claims. Topic/corpus indexes are refreshed only when those directories
exist; cataloguing a guide does not create a topic graph or ingest a corpus.
