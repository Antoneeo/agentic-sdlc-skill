# Marketing Agentic SDLC — Project Protocol (pointer)

This project follows the Marketing Agentic SDLC Evidence-First process. The full
operating contract is the `mkt-agentic-sdlc` skill (installed in your agent's
skills directory); this file is only the minimal always-on pointer.

## Rule Zero — Triage every request
- E1 Quick: single question or asset feedback (positioning opinion, copy critique). Answer directly; numbers still need a source.
- E2 Campaign: single-campaign or single-channel plan. Light path: mini-brief + targeted research + campaign document.
- E3 Full Plan: complete marketing plan. Full SOSTAC workflow via the skill: Discovery -> Research -> Situation -> Objectives -> Strategy -> Tactics -> Action -> Control -> Packaging.
- Research Spike: time-boxed market question; outcome in `mkt_docs/spikes/RESEARCH_[topic].md`.
- When in doubt, pick the higher level. Declare the chosen level when starting.

## The three non-negotiables
1. Evidence ledger: every market number carries an [EV-nn] reference (FACT / BENCHMARK / ASSUMPTION). No invented numbers, ever.
2. Ask only what the user owns: facts come from the user, analysis comes from research. Never ask the user to do the analysis.
3. Internal consistency: budget sums, funnel math and the objective->tactic->KPI chain are validated mechanically before delivery.

## Where things live
- Vision (gate for E3): `mkt_docs/vision/MKT_VISION.md` — `Status: DRAFT` informs, `Status: APPROVED` binds.
- Evidence: `mkt_docs/research/evidence_ledger.md` (the single source for every number).
- Strategy artifacts: `mkt_docs/strategy/`; tactical artifacts: `mkt_docs/tactics/`; final deliverables: `mkt_docs/deliverables/`.
- Must-reads: `mkt_docs/README.md`; full generated manifest: `mkt_docs/INDEX.md`.
- If devPNT is available for this project, its M-VISION / plans / governed artifacts take over (Hybrid mode — see the skill).

## Closure gate
Deliverables ship only after `python <skill_dir>/scripts/mkt_check.py check` is
CLEAN (where the validator is adopted) and the CMO review passed.

If the mkt-agentic-sdlc skill is not available in this client, ask the user to install it:
`npm i -g @antoneeo/mkt-agentic-sdlc-skill && mkt-sdlc-install-skill`
