# F-063 / F-064 implementation review

2026-10-04. Reviewer: gpt-6-astra high, fresh context, static/read-only native
subagent `software_code_review`; invoking session Default, reviewer Default.
Inputs: approved Vision, both ANALYSIS documents, 83-path design map, scoped diff,
actual source, ADR and shared-memory guide. No reviewer test execution or writes.

**R1 FAIL: 2 BLOCK, 1 WARN. R2 PASS: all three addressed, no residual finding.**
PASS covers implementation conformance; it does not establish the F-063 FS7 benefit.

| Finding | Evidence and correction | Verification |
|---|---|---|
| BLOCK: legacy digest corruption could hide behind an independent MATCHED support | `_kb_software_integrity` now checks every recorded digest before the no-binding return. Intact legacy sources remain UNTRACKED; corruption is INVALID and fails evidence even with another support | New test covers a transitive legacy premise plus MATCHED alternative |
| BLOCK: capture accepted paths whose whitespace/quotes could not round-trip in metadata | `kb_capture_source` rejects unrepresentable source and premise paths before UUID creation or publication; legacy reading remains unchanged | New test covers leading/trailing whitespace and surrounding literal quotes, with no output mutation |
| WARN: text output hid changed inputs behind derived notes | `kb_cmd_evidence` prints each premise's path/status/reason recursively from the existing report | New test traverses three derivation levels |

Author reproduced the findings before fixing: `implementation/review-red.txt`
records five assertion failures including subtests; `review-green.txt` records
35 tests with one symlink privilege skip. R2 read these logs without executing them.
A subsequent legacy test required the phrase `digest changed`; the diagnostic now
retains that phrase as well as `digest mismatch`. No decision logic changed.

## Conformance retained from R1 and confirmed by R2

| Input constraint | Implementation evidence |
|---|---|
| Legacy header/IDs; optional kind; separate lifecycle | `kb_parse_claims`, `kb_check_claims`: exact 8/9-column schemas, unchanged IDs, cross-kind links rejected |
| Safe additive acquisition | `kb_project_id`, `kb_capture_source`, `_kb_capture_lock`, `_kb_publish`: stable UUID, bounded regular UTF-8 input, exact span, exclusive publication and sidecar-last retry |
| Stored integrity and current applicability | `_kb_software_integrity`, `kb_software_findings`: digest independent of binding, status distinctions, foreign project never opens live software |
| Transitive dependencies and alternatives | `kb_source_graph`, `kb_derivation_dependents`: shared graph, joint premises AND, independent support OR; cycles/dangling invalid, historical evidence retained |
| Existing check/stale behavior and marketing seam | `kb_validate_surface`, `kb_cmd_check`, `kb_cmd_stale`, marketing caller: integrity errors versus drift warnings, optional project parameter |
| Portability without authority promotion | `kb_export_closure` includes recursive premises/extractions; `kb_import_plan` excludes project README identity; ruling ratification stays agent-owned |
| All four installed distributions | Identical runtime, tests and common resources; package allowlists include common methods/templates; CLI dispatch exposes both commands |
| F-063 UC1 / FS1 orientation | `memory.md` descent from concepts to conditions and source; code/symbol impact still required |
| UC2 / FS2 nature | Claim kind is separate from provenance/state; approval does not make a design observed |
| UC3 / FS3-4 updates | Software phase triggers require evidence checks and indirect-input impact, not digest-only reasoning |
| UC4 / FS5-6 capture/reconciliation | Analysis-only additions and updates, reuse of concepts, retained sources, one owning workflow |
| UC5 / FS7 benefit | Comparative evaluation is required and reported separately; no effectiveness claim follows from static PASS |
| T1/T2/T4/T5 integrity and compatibility | Kind/state separation, source confinement, reparse checks, foreign isolation, shared consumers preserved |
| T3/T6 agent duties | Selection/minimization before capture; no execution of source instructions, no automatic secret detector; local gaps, no mandatory L1 capture |
| KB protections | Common memory retains recall, chain re-touch, grounded rulings, idempotent capture and full reread; KB keeps its specialist closing question/timing |
| Vision/non-goals and ADR | Reuses KB corpus/topic graph; no second storage/workflow, whole-repository sweep or claim of global coverage. No protection withdrawal identified |
| Guide | Exact implementation snapshot and declared hash checked in R2; refreshed after diagnostic wording adjustment |

The author owns final test runs, packaging, behavioral evaluation and document
closure. Results: `TEST_software_knowledge_2026-10-04.md`. Enumeration instruments:
AST/text design inventory, scoped file diff, direct source reads and four-copy
SHA256 comparison. Original design inventory limits remain recorded in its review.
