# Handoff
Date: 2026-07-02 (UTC)
Branch: main
Agent: Claude (Fable)

## Active features
- **v1.8.1 RELEASED** (npm published + verified, tag v1.8.1, merged to main
  756e8c8): `sha256_file` hashes LF-normalized content — CRLF checkouts no
  longer false-flag guides [stale]. Battery scenario 10 green.
- **GUIDE_release.md** (first field guide, v3): release procedure distilled per
  guides.md pipeline from the v1.8.0/v1.8.1 sessions — git_push_tag.bat usage,
  tag verification, re-run behavior, devPNT db locks, npm 2FA. Snapshot
  release-runbook-ba876688.md; 3 review rounds PASS (see REVIEW_LOG).
- M1 Feature B (devPNT-governed, PROGRESS): unit 1 (project-scope guides) DONE —
  implemented, 9/9 battery green, deep code review PASS, ADR accepted,
  released as v1.8.0 + hotfix v1.8.1 (npm, 2026-07-02). Release fixed a
  packaging gap: guides.md was missing from package.json `files`.
  Unit 2 (agent-global KB: --root, overrides:, precedence) NOT started.
- devPNT docs: milestone_vision (v1.1), d_uc, p_tm, e_isp_u1, e_tdd_u1 (LATEST v1.2), adr accepted.
- Local: SHADOW_e_tdd_operative_guides_u1_v1.2.md is the implementation spec mirror.

## Next step
Unit 2 E-ISP (agent-global KB).

## Session notes
- project_vision.md APPROVED (Antonio, 2026-07-02); roadmap/principles still DRAFT.
- Review-gate follow-up candidates (optional WARNs): orphaned guide router visibility
  in validate; T6 confinement reuse in cmd_stale. See REVIEW_LOG notes.
- Ops: devPNT server locks .devpnt dbs — branch switches/merges need the server
  closed or a separate git worktree (documented in GUIDE_release "watch out").
- KL INITIALIZED (2026-07-02): manifest v1.1, 4 docs (architecture, vision,
  principles, adr_digest) — injected at every bootstrap. Unblocking required
  deleting a stale empty analysis-scope doc (pre-M38 .py-only scan cached
  forever); the code-level self-heal fix for devPNT is tracked as a pending
  task chip (kl_init_scope: rescan on empty cached scope).
- Project summary CURRENT (regenerated 2026-07-02 17:23).
