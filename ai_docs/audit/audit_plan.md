# Audit Plan

States: PENDING (to analyze) | ANALYZED (analyzed, with reference) | SKIPPED (with reason).

| Path | Status | Reference | Notes |
|---|---|---|---|
| examples/ | PENDING | - | legacy docs/ layout examples, predate the ai_docs structure |
| sdlc-test-project/ | SKIPPED | - | manual test fixture, not product code |
| skills/agentic-sdlc-skill/ | ANALYZED | 35c27a392bff | re-analysis here is not complete until the two DERIVED documents say the same thing: `strategic/skill_family_agent_workflows.md` (what an agent does differently under each lens) and the distribution's `README.md` (the npm front page — support-files bullet, Runtime Shape tree, validator commands). `mark` is the last step, not the first |
| scripts/ | ANALYZED | df494cebfede |  |
| distributions/ | ANALYZED | 35c27a392bff | same duty as the row above, per distribution: doctrine changed here means `strategic/skill_family_agent_workflows.md` and that distribution's `README.md` are stale until refreshed. `stale` fires on this row at the first doctrine edit — that is the prompt |
| ai_docs/ | SKIPPED | - | the docs root is governance, not an analyzable area: `validate` checks it, and since 2026-10-19 `stale` ignores it and `mark` refuses it. |
| skills/ | ANALYZED | 35c27a392bff |  |
