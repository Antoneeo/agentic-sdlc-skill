---
workstream: Release 1.19.0 (Architect Pass + Design Review Gate)
level: —
branch: feat/architect-pass (tag v1.19.0)
status: AWAITING OWNER
since: 2026-07-28
next: `npm publish` (2FA, owner's act), then verify `npm view` → 1.19.0
details: CHANGELOG `[1.19.0]`/`[1.18.0]` · ANALYSIS_architect_pass.md · ANALYSIS_design_review_gate.md
updated: 2026-07-28
---

## Resume state

Merged to main. The tag carries 1.18.0 as well, which was never published.

## Watch out

After publishing, field-test on large brownfield projects:
`evals/scenarios/placement_rules_before_impact.md` and `unmapped_never_grounds_missing.md`
are the cold-run harness.

