# Changelog

## 0.2.0 — 2026-07-09 (v1.0 hardening)

- **Deterministic doctrine gate**: `scripts/test_skill_invariants.py` asserts the load-bearing invariants (three guarantees, review red-flags R1/R11b/R15, elicitation rules, research URL rule, parseable template tokens, sales-led funnel guidance, support-file wiring). Fails on a real regression.
- **Opt-in behavioral eval layer**: `evals/run_behavioral.py` (zero-LLM driver) + 6 scenarios (triage/escalation, owned-facts elicitation, no-number-without-ledger, swap-test enforced, low-cost-trap flagged, no-guaranteed-success). Mirrors the sibling skill.
- **Contrast validation (B2B sales-led)**: second synthetic eval on a business unlike the first — the Vision Alignment / amendment discipline caught and held a deliberate vision-divergence (self-serve tier) instead of absorbing it.
- **Calibration from the contrast run**: sales-led/B2B funnel guidance (funnel output = qualified demos not closed customers; separate pipeline build-up table; closed-won lag) in `frameworks.md` + `templates.md`; B2B firmographic-ICP + buying-committee variant in `templates.md`.
- ENFORCEMENT.md §5/§6 updated to run both deterministic batteries + the behavioral layer.

## 0.1.0 — 2026-07-09

Initial release.

- Operating contract `SKILL.md`: Marketing Values, Rule Zero engagement triage (E1/E2/E3/Spike), dual operating modes (Standalone `mkt_docs/`, Hybrid devPNT), E3 nine-phase SOSTAC workflow with user gates, adversarial review gates and mechanical validation.
- Support files: `frameworks.md` (framework selection guide), `elicitation.md` (question waves, only-facts-you-own rule), `research.md` (research playbook + evidence ledger discipline), `templates.md` (all artifact templates), `review.md` (CMO review discipline + marketing red flags), `ENFORCEMENT.md`.
- Mechanical validator `scripts/mkt_check.py`: `check`, `validate`, `ledger`, `budget`, `funnel`, `trace`, `index`.
- npm packaging: `mkt-sdlc-init` (project scaffold), `mkt-sdlc-install-skill` (multi-client skill install: Claude Code, Gemini CLI, Codex, Google Antigravity).
