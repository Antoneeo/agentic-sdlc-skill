# Audit Plan

States: PENDING (to analyze) | ANALYZED (analyzed, with reference) | SKIPPED (with reason).

| Path | Status | Reference | Notes |
|---|---|---|---|
| examples/ | PENDING | - | legacy docs/ layout examples, predate the ai_docs structure |
| sdlc-test-project/ | SKIPPED | - | manual test fixture, not product code |
| skills/agentic-sdlc-skill/ | ANALYZED | 2026-08-01T17:29:35Z |  |
| scripts/ | ANALYZED | 4dc4a3e395eb |  |
| distributions/ | ANALYZED | 2026-08-01T17:29:35Z |  |
| ai_docs/ | ANALYZED | 2026-08-01T17:34:38Z | the governance tree itself, not an analyzable area: marking it rewrites this file, which sits inside it, so a hash-based row chases its own tail forever. Its freshness is what `check` already verifies directly |
