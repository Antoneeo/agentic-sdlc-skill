---
id: F-003
feature: devPNT Seam (coexistence contract)
status: COMPLETED
level: L3
start_date: 2026-07-02
end_date: 2026-07-02
---
# Feature Analysis: devPNT Seam

## Objective
Eliminate the active coexistence conflicts between the skill and devPNT (C1-C8 of the
evolution roadmap) by making the skill the process spine and devPNT the amplifier:
one ownership matrix, one triage taxonomy, mode-aware validator commands, and a
slimmed devPNT MCP doctrine that defers process to the skill.

## Feature Vision
- Expected benefit: a user running skill+devPNT gets ONE coherent process — no double
  triage, no shadow/ANALYSIS collision, no gate blocking legitimate Hybrid work.
- Alignment: implements Phase 1 of `ai_docs/vision/roadmap_evoluzione_agenti.md`
  (status DRAFT, work explicitly requested by the user) — decisions D1, D2, D7.
- Non-goals: no devPNT server-side features (F1-F8 are specs for later); no Feature A/B
  content; no change to devPNT internal-mode prompt (`system_prompt.md`).
- Success signals: legacy and Hybrid scenarios pass the validator test battery;
  the devPNT doctrine no longer states its own triage or ai_docs layout.

## Impact
- `skills/agentic-sdlc-skill/SKILL.md` — new "Coexistence with devPNT" section
  (ownership matrix, triage equivalence, state mapping, shadow rule, --hybrid flags).
- `skills/agentic-sdlc-skill/scripts/sdlc_check.py` — `gate --hybrid`
  (E-TDD shadow unlock), `stale`/`check --hybrid` (skip audit-plan staleness).
- `skills/agentic-sdlc-skill/ENFORCEMENT.md` — hybrid hook example.
- `D:\SoftwareDev\devPNT\agent\core\mcp_system_prompt.md` — §1 contract bullet
  (methodology deference), §4.3 triage deferred to the skill, §6.1 layout aligned
  (vision/, reference/, SHADOW_* naming), shadow-before-implementation rule,
  §8 checklist updates. Separate repo, dirty tree: edited, NOT committed here.

## Security and Threat Model
- No new attack surface: validator stays stdlib, read/write only inside `ai_docs/`.
- `gate --hybrid` WEAKENS the write gate by design (unlocks on the presence of an
  E-TDD shadow instead of an IN_PROGRESS ANALYSIS). Mitigation: hybrid mode is an
  explicit flag in the hook command (never auto-detected), and the unlock still
  requires a design artifact on disk; documented in ENFORCEMENT.md.
- Prompt changes alter agent behavior, not code execution; the human proposal
  gate in devPNT is untouched.

## Action Plan
- [x] SKILL.md coexistence section (matrix C1/C2/C7/C8 + triage C6 + states C5 + shadow C3)
- [x] sdlc_check.py --hybrid on gate/stale/check (C4, C8)
- [x] ENFORCEMENT.md hybrid example
- [x] devPNT mcp_system_prompt.md slimmed (C1, C3, C6 on the devPNT side)
- [x] Test battery (legacy, standalone, hybrid gate/stale)
- [x] Closure: index, check CLEAN, CHANGELOG

## Test Strategy
Scenario tests on scratch projects via the validator CLI (AAA-style shell checks):
hybrid gate unlock with/without shadow, stale skip with --hybrid, standalone
regressions from the Phase 0 battery re-run.

## Diary / Current State
- 2026-07-02: analysis opened; Phase 0 completed on branch feature/v1.7.0-evolution.
- 2026-07-02: implemented and closed. SKILL.md gained the "Coexistence with devPNT"
  section (ownership matrix, triage equivalence, state mapping, shadow discipline);
  validator gained explicit `--hybrid` on gate/stale/check (H1-H5 battery green,
  Phase-0 regressions green). devPNT `mcp_system_prompt.md` slimmed: §1 methodology
  bullet, §4.3 triage deferred to the skill, §6.1 layout aligned (vision/, reference/,
  SHADOW_* naming, shadow-before-implementation, closure gate), §8 checklist items
  0/13/14. devPNT repo left UNCOMMITTED by design (dirty tree with user's own work).
  devPNT server-side features F1-F8 remain roadmap items, not part of this change.
