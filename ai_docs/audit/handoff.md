# Handoff — workstream registry
Date: 2026-08-01 (UTC)

| Workstream | Level | Branch | Status | Since | Next step | Details |
|---|---|---|---|---|---|---|
| F-015 Code-Comprehension Guides | L3 | main | PAUSED | 2026-07-19 | dogfood #8: write one real `source_kind: code` guide | ANALYSIS_comprehension_guides.md (Diary; no volatile state) |
| Release 1.19.0 (Architect Pass + Design Review Gate) | — | feat/architect-pass (tag v1.19.0) | AWAITING OWNER | 2026-07-28 | merged to main; `npm publish` (2FA) is the remaining step — verify `npm view` → 1.19.0. It carries 1.18.0, never published. Then field-test on large brownfield projects: `evals/scenarios/architect_rules_before_impact.md` + `unmapped_never_grounds_missing.md` are the cold-run harness | CHANGELOG `[1.19.0]`/`[1.18.0]` · ANALYSIS_architect_pass.md · ANALYSIS_design_review_gate.md |

| F-022 Multi-Domain Core | L3 | feat/multi-domain-core | REVIEW | 2026-07-31 | P0–P7 done. Three distributions on one shared spine, drift-guarded; kb's gate green (was 9F+4E); mkt converged with its golden transcript byte-identical; `migrate` ships. Batteries: 136 / 136 / 148 + 12 node each, three golden baselines intact. **Owner's call now:** (a) monorepo consolidation + anything on GitHub, (b) `npm publish` ×3 (2FA; 1.19.0 was already pending, npm is at 1.17.0), (c) whether to publish kb while its knowledge-method overlays are still stubs | ANALYSIS_multi_domain_core.md (Diary; no volatile state) |

| F-023 Vision Shape Rules | L3 | feat/multi-domain-core | PLANNED | 2026-07-31 | split out of F-022's blind rounds: rules defined by shape rather than by function. Start with the two conflicting defaults for unreached proposals — every other ruling is operator-dependent until it is fixed | ANALYSIS_vision_shape_rules.md · battery in audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md Round 8 |

## Project-wide notes
Repo is CRLF (edit as content-delta). devPNT off — Standalone. Standing Vision battery:
`audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md` (re-run on every Vision edit).
**npm is at 1.17.0** (verified 2026-07-28). Release branches are cut from the previous
release tag and not yet merged to main: `feat/architect-pass` carries 1.17.0's content
plus 1.18.0. `v1.16.0` was tagged and never published — stays as history.
