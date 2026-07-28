# Handoff — workstream registry
Date: 2026-07-28 (UTC)

| Workstream | Level | Branch | Status | Since | Next step | Details |
|---|---|---|---|---|---|---|
| F-015 Code-Comprehension Guides | L3 | main | PAUSED | 2026-07-19 | dogfood #8: write one real `source_kind: code` guide | ANALYSIS_comprehension_guides.md (Diary; no volatile state) |
| Release 1.18.0 (Architect Pass) | — | feat/architect-pass (tag v1.18.0) | AWAITING OWNER | 2026-07-28 | merge to main + `npm publish` (2FA); verify `npm view` → 1.18.0. Then field-test the pass on large brownfield projects — `evals/scenarios/architect_rules_before_impact.md` and `unmapped_never_grounds_missing.md` are the cold-run harness | CHANGELOG `[1.18.0]` · ANALYSIS_architect_pass.md |

## Project-wide notes
Repo is CRLF (edit as content-delta). devPNT off — Standalone. Standing Vision battery:
`audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md` (re-run on every Vision edit).
**npm is at 1.17.0** (verified 2026-07-28). Release branches are cut from the previous
release tag and not yet merged to main: `feat/architect-pass` carries 1.17.0's content
plus 1.18.0. `v1.16.0` was tagged and never published — stays as history.
