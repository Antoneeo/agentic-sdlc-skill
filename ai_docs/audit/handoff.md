# Handoff — workstream registry
Date: 2026-08-01 (UTC)

| Workstream | Level | Branch | Status | Since | Next step | Details |
|---|---|---|---|---|---|---|
| F-015 Code-Comprehension Guides | L3 | main | PAUSED | 2026-07-19 | dogfood #8: write one real `source_kind: code` guide | ANALYSIS_comprehension_guides.md (Diary; no volatile state) |
| Release 1.19.0 (Architect Pass + Design Review Gate) | — | feat/architect-pass (tag v1.19.0) | AWAITING OWNER | 2026-07-28 | merged to main; `npm publish` (2FA) is the remaining step — verify `npm view` → 1.19.0. It carries 1.18.0, never published. Then field-test on large brownfield projects: `evals/scenarios/architect_rules_before_impact.md` + `unmapped_never_grounds_missing.md` are the cold-run harness | CHANGELOG `[1.19.0]`/`[1.18.0]` · ANALYSIS_architect_pass.md · ANALYSIS_design_review_gate.md |

| F-022 Multi-Domain Core | L3 | feat/multi-domain-core | DONE, HELD | 2026-07-31 | Complete and consolidated: one repository, the code distribution at the root, kb and mkt under `distributions/` grafted with `git subtree` (history preserved; mkt's TAGS did not transfer and still live only in the old clone + GitHub). Batteries green, three golden transcripts intact, drift guard comparing the copies to each other, `npm pack` correct for all three. **Release HELD by the owner (2026-08-01): nothing is published until kb is effective** — see F-024. Nothing else outstanding here | ANALYSIS_multi_domain_core.md |

| F-023 Vision Shape Rules | L3 | feat/multi-domain-core | PLANNED | 2026-07-31 | split out of F-022's blind rounds: rules defined by shape rather than by function. Start with the two conflicting defaults for unreached proposals — every other ruling is operator-dependent until it is fixed | ANALYSIS_vision_shape_rules.md · battery in audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md Round 8 |

| F-024 kb Knowledge Method | L3 | feat/kb-knowledge-method | IN_PROGRESS | 2026-08-01 | **the release gate — F-022 stays HELD until this is effective.** Two design-gate rounds FAILED and reshaped it; the owner then set the center: the machine detects and holds conflicts, only new information resolves (rulings carry `basis:`), L1 stays free, escalations batched in a legal form. v3 of the pair is written. Next: design gate round 3 (the cap), then implement — F-025's ledger section first, same file | ANALYSIS_kb_knowledge_method.md (Diary) |
| F-025 Claim Ledger | L3 | feat/kb-knowledge-method | PLANNED | 2026-08-01 | the component F-024 consumes, extracted by round 1 of its design gate (mkt's evidence ledger half-owns the shape). Lives INSIDE kb's `sdlc_check.py` (two-file validator constraint); built before F-024's graph, same branch. Detect-and-hold only — the automatic precedence ladder was dropped by owner ruling | ANALYSIS_claim_ledger.md (Diary) |

## Project-wide notes
Repo is CRLF (edit as content-delta). devPNT off — Standalone. Standing Vision battery:
`audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md` (re-run on every Vision edit).
**npm is at 1.17.0** (verified 2026-07-28). Release branches are cut from the previous
release tag and not yet merged to main: `feat/architect-pass` carries 1.17.0's content
plus 1.18.0. `v1.16.0` was tagged and never published — stays as history.
