# Independent Review Log

Records each independent-review-gate pass (§4.5 tech artifacts, §4.6 code). This is how the gate's real benefit is measured over time — one row per review.

| date | doc_key | tier | reviewer | findings_raised | findings_real | verdict | revise_rounds |
|---|---|---|---|---|---|---|---|
| 2026-07-02 | p_tm_operative_guides | deep | devpnt-tech-reviewer | 7 | 7 | PASS | 2 |
| 2026-07-02 | e_isp_operative_guides_u1 | deep | devpnt-tech-reviewer | 10 | 10 | PASS | 2 |
| 2026-07-02 | e_tdd_operative_guides_u1 | light | devpnt-tech-reviewer-light | 4 | 4 | PASS | 3 |

## Notes
- **e_tdd_operative_guides_u1** (Feature B / M1, unit 1): round 1 FAIL — 1 BLOCK: the cmd_stale restructure claimed the audit-plan body could stay "unchanged" with rc OR-ed in, but its three early returns would silently discard a drifted-guide rc (e.g. drifted guide + empty audit plan ⇒ false success); fixed by showing the rewritten tail verbatim (`return rc` on both early paths). +2 WARNs (DEPRECATED scoping note; --strict is a blanket end-of-run mechanism, not per-warning escalation). Round 2 caught off-by-2 line citations in the fix itself (implementer brief precision). Round 3 verification-only PASS. Value: a real control-flow bug killed at design time, before the cheap-tier implementer could inherit it.
- **e_isp_operative_guides_u1** (Feature B / M1, unit 1): round 1 FAIL caught 2 BLOCK + 3 WARN — (1) `.sources/` "excluded (dotdir)" was FALSE (`list_canonical_docs` rglob has no dot-filter; snapshots would be swept into the manifest) → became a real Impact Map row; (2) index-model inconsistency (UC-5/F3 promise `reference/INDEX.md`, nothing generates it) → resolved by generating it and dropping the hand router. Round 2 PASS with 5 WARNs folded before proposing: GENERATED_DOCS no-op removed, T2 drift moved from validate to `stale` (honors the M-VISION "one freshness motor" — a silent lodestar deviation the reviewer caught), two-index role split declared, description≤160 constraint, lodestar status alignment (M-VISION v1.1).
- **p_tm_operative_guides** (Feature B / M1): round 1 FAIL caught 5 BLOCK + 2 WARN — 3 overclaims (T1 provenance/marker validation, T2 source_version drift, T5 overrides/collision were stated as existing enforcement but are unbuilt milestone deliverables) and 2 missing threats (T6 guide-path traversal, T8 provenance spoofing). Round 2 PASS after NOW/MILESTONE/PROCESS tagging + the two threats added. Concrete value: prevented shipping a threat model that would have let the human trust mechanical guards that do not exist yet. The [MILESTONE] tags now drive the E-ISP/E-TDD security requirements.
