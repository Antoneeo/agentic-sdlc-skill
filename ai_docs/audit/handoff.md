# Handoff — workstream registry
Date: 2026-08-01 (UTC)

| Workstream | Level | Branch | Status | Since | Next step | Details |
|---|---|---|---|---|---|---|
| F-015 Code-Comprehension Guides | L3 | main | PAUSED | 2026-07-19 | dogfood #8: write one real `source_kind: code` guide | ANALYSIS_comprehension_guides.md (Diary; no volatile state) |
| Release 1.19.0 (Architect Pass + Design Review Gate) | — | feat/architect-pass (tag v1.19.0) | AWAITING OWNER | 2026-07-28 | merged to main; `npm publish` (2FA) is the remaining step — verify `npm view` → 1.19.0. It carries 1.18.0, never published. Then field-test on large brownfield projects: `evals/scenarios/architect_rules_before_impact.md` + `unmapped_never_grounds_missing.md` are the cold-run harness | CHANGELOG `[1.19.0]`/`[1.18.0]` · ANALYSIS_architect_pass.md · ANALYSIS_design_review_gate.md |

| F-022 Multi-Domain Core | L3 | feat/multi-domain-core | DONE, HELD | 2026-07-31 | Complete and consolidated: one repository, the code distribution at the root, kb and mkt under `distributions/` grafted with `git subtree` (history preserved; mkt's TAGS did not transfer and still live only in the old clone + GitHub). Batteries green, three golden transcripts intact, drift guard comparing the copies to each other, `npm pack` correct for all three. **Release HELD by the owner (2026-08-01): nothing is published until kb is effective** — see F-024. Nothing else outstanding here | ANALYSIS_multi_domain_core.md |

| F-023 Vision Shape Rules | L3 | feat/multi-domain-core | PLANNED | 2026-07-31 | split out of F-022's blind rounds: rules defined by shape rather than by function. Start with the two conflicting defaults for unreached proposals — every other ruling is operator-dependent until it is fixed | ANALYSIS_vision_shape_rules.md · battery in audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md Round 8 |

| Release of the three packages | — | feat/kb-knowledge-method | AWAITING OWNER | 2026-08-01 | **F-024/F-025 CLOSED** (COMPLETED 2026-08-01: method + ledger implemented, three design-gate rounds disposed, acceptance run on the Eclosion corpus CLEAN, the capacity conflict resolved by owner ruling with basis, ADR recorded). The hold on F-022's release was "until kb is effective" — kb now does its job on real documents; **publishing (npm ×3, 2FA) remains the owner's act**. mkt tags v0.2.0/v0.2.1 still live only in the old clone + GitHub | ANALYSIS_kb_knowledge_method.md · ANALYSIS_claim_ledger.md · ADR_2026-08-01_kb_topic_graph_claim_ledger.md |

## Project-wide notes
Repo is CRLF (edit as content-delta). devPNT off — Standalone. Standing Vision battery:
`audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md` (re-run on every Vision edit).
**npm is at 1.17.0** (verified 2026-07-28). Release branches are cut from the previous
release tag and not yet merged to main: `feat/architect-pass` carries 1.17.0's content
plus 1.18.0. `v1.16.0` was tagged and never published — stays as history.
