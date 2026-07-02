# Handoff
Date: 2026-07-02 (UTC)
Branch: feature/v1.8.1-hash-line-endings
Agent: Claude (Fable)

## Active features
- **v1.8.1 (L2 hotfix, this branch)**: `sha256_file` in `sdlc_check.py` now hashes
  LF-normalized content (CRLF->LF) — a Windows `core.autocrlf=true` checkout no
  longer false-flags every guide `[stale]`. Backward compatible (recorded hashes
  were LF-based). guides.md step 3 + .gitattributes comment updated; battery
  scenario 10 (CRLF no-flag / genuine-drift still-flag) run green.
  Next step after tag: merge to main (web PR or user-authorized push), then
  user runs `npm publish` (2FA).
- M1 Feature B (devPNT-governed, PROGRESS): unit 1 (project-scope guides) DONE —
  implemented, 9/9 battery green, deep code review PASS, ADR accepted,
  **released as v1.8.0 (npm + tag, 2026-07-02)**. Release fixed a packaging gap:
  guides.md was missing from package.json `files` (would not have shipped).
  Unit 2 (agent-global KB: --root, overrides:, precedence) NOT started.
- devPNT docs: milestone_vision (v1.1), d_uc, p_tm, e_isp_u1, e_tdd_u1 (LATEST v1.2), adr accepted.
- Local: SHADOW_e_tdd_operative_guides_u1_v1.2.md is the implementation spec mirror.

## Next step
v1.8.1 merge to main + npm publish (user); then unit 2 E-ISP (agent KB).

## Session notes
- project_vision.md APPROVED (Antonio, 2026-07-02); roadmap/principles still DRAFT.
- Review-gate follow-up candidates (optional WARNs): orphaned guide router visibility
  in validate; T6 confinement reuse in cmd_stale. See REVIEW_LOG notes.
