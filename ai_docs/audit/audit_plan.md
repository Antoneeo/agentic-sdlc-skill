# Audit Plan

States: PENDING (to analyze) | ANALYZED (analyzed, with reference) | SKIPPED (with reason).

| Path | Status | Reference | Notes |
|---|---|---|---|
| examples/ | PENDING | - | legacy docs/ layout examples, predate the ai_docs structure |
| sdlc-test-project/ | SKIPPED | - | manual test fixture, not product code |
| skills/agentic-sdlc-skill/ | ANALYZED | 2026-08-05T03:32:48Z | re-analysis here is not complete until the two DERIVED documents say the same thing: `strategic/skill_family_agent_workflows.md` (what an agent does differently under each lens) and the distribution's `README.md` (the npm front page — support-files bullet, Runtime Shape tree, validator commands). `mark` is the last step, not the first |
| scripts/ | ANALYZED | 2026-08-04T04:43:42Z |  |
| distributions/ | ANALYZED | 2026-08-26T03:35:21Z | same duty as the row above, per distribution: doctrine changed here means `strategic/skill_family_agent_workflows.md` and that distribution's `README.md` are stale until refreshed. `stale` fires on this row at the first doctrine edit — that is the prompt |
| ai_docs/ | ANALYZED | 2026-08-05T03:33:02Z | the governance tree itself, not an analyzable area: marking it rewrites this file, which sits inside it, so a hash-based row chases its own tail forever. Its freshness is what `check` already verifies directly |
| skills/ | ANALYZED | 2026-08-26T03:35:21Z |  |
