# Agentic SDLC — Project Protocol (pointer)

This project follows the Agentic SDLC Documentation-First process. The full
operating contract is the `agentic-sdlc` skill (installed in your agent's
skills directory); this file is only the minimal always-on pointer.

## Rule Zero — Triage every request
- L1 Trivial: ~10 lines, 1-2 files, no API/dependency/behavior change. Implement + run existing tests; no docs.
- L2 Small: clear root cause, at most 3 files, low risk. Mini-analysis in the reply; tests mandatory.
- L3 Significant: >3 files, APIs/contracts, new dependency, user-visible behavior, security-sensitive area, or architectural change. Full workflow via the skill: Vision Gate -> ANALYSIS -> plan -> implement -> test -> closure.
- Spike: time-boxed exploration; outcome in `ai_docs/solutions/SPIKE_[topic].md`; reclassify for production.
- Security-sensitive areas (external input parsing, authN/authZ, crypto, network, personal data, filesystem) are never L1.
- When in doubt, pick the higher level. Declare the chosen level when starting.

## Where things live
- Vision (gate for L3): `ai_docs/vision/` — `Status: DRAFT` informs, `Status: APPROVED` binds.
- Feature analyses: `ai_docs/solutions/ANALYSIS_[feature].md` (frontmatter = feature state).
- Must-reads: `ai_docs/README.md`; full generated manifest: `ai_docs/INDEX.md`.
- If devPNT is available for this project, its M-VISION / plans / governed artifacts take over (Hybrid mode — see the skill).

## Closure gate
Docs travel in the same commit/PR as the code they describe. If the project
adopts the validator, `python <skill_dir>/scripts/sdlc_check.py check` must be
CLEAN before declaring work done.

If the agentic-sdlc skill is not available in this client, ask the user to install it:
`npm i -g @antoneeo/agentic-sdlc-skill && agentic-sdlc-install-skill`
