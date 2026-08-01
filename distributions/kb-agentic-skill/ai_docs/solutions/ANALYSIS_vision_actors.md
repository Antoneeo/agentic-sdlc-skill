---
id: F-014
feature: Vision Actors
status: COMPLETED
level: L3
start_date: 2026-07-08
end_date: 2026-07-08
---
# Feature Analysis: Vision Actors

## Objective
- Make the **Actors** (the personas/roles a feature or project serves) a first-class, *characterized* element of the Vision, so the intended UX is designed for named people instead of an implicit "user".
- Upgrade the existing flat `## Target Users` / `## Users or Stakeholders` fields into a light, UX-driving `## Actors` element, consistently across Standalone (skill templates) and Hybrid (devPNT M-VISION).

## Feature Vision
- Serves the project north star ("keep every change aligned with intent") and the UX-as-decisive-factor principle: an actor names *who* the UX is for and *what good feels like* to them, so design trade-offs have a concrete referent.
- Aligned with `ai_docs/vision/project_vision.md` (Status: APPROVED) layer **A** — enriches the Vision artifact/lifecycle. No Non-Goal hit: it stays proportional (one light line per actor), not a full persona/ALM system.
- Non-goals for this feature: no heavyweight persona research framework; no retrofit of every historical doc; the Actor is a *reference*, not a duplicate of the use-case.

## Actors
<!-- feature-local cast: this is an internal-tooling change, so the actors are the
     doctrine's own roles, not the product end-users in project_vision.md ## Actors. -->
- **Skill author / doctrine maintainer** — evolve the process without drift; good UX = one edit point per rule, templates that prompt for what matters.
- **Agent running an L3** — apply the process correctly across sessions; good UX = each rule stated once, unambiguous, anti-DRY.
- **Reviewer (human or agent)** — catch omissions before merge; good UX = every constraint has a checkable home.
- **Hybrid/devPNT agent** — stay aligned with Standalone; good UX = the M-VISION mirrors the skill, nothing to reconcile.

## Use Cases / User Needs
- **[Skill author / doctrine maintainer]** needs the Vision templates to prompt for actors → so every project's Vision characterizes its cast. Served by the `templates.md` + `elicitation.md` edits.
- **[Agent running an L3]** needs to know actors are defined once and referenced by use-cases → so it does not re-describe "who" in two places (anti-DRY). Served by the Actor↔UseCase reference rule in `templates.md` + `review.md`.
- **[Reviewer]** needs actors in the conformance set → so a use-case with no defined actor, or an unmet UX expectation, is a finding. Served by `review.md`.
- **[Hybrid/devPNT agent]** needs the M-VISION to carry actors → so Hybrid stays aligned with Standalone. Served by the `mcp_system_prompt.md` §4.2 edit.

## Impact
Standalone skill doctrine (`skills/agentic-sdlc-skill/`):
- `templates.md` — MODIFY: `project_vision.md` `## Target Users`→`## Actors`; `VISION_[feature].md` `## Users or Stakeholders`→`## Actors`; add the light Actor shape + the Actor↔UseCase reference rule; ANALYSIS `## Feature Vision`/`## Use Cases` comments point to Actors.
- `elicitation.md` — MODIFY: add "Actors" to the one structured round (who interacts, role, goal, UX expectation).
- `SKILL.md` — MODIFY: "Protect the Vision" value (users→actors + the UX they expect); §3 Request-Analysis trace bullet gains "actor" (the Vision Gate already reads the whole `project_vision.md`/M-VISION, which now carries `## Actors`).
- `review.md` — MODIFY: conformance inputs — each use-case traces to a defined Actor; the Actor's UX expectation is a checkable constraint.

Dogfood (`ai_docs/`):
- `vision/project_vision.md` — MODIFY: `## Target Users`→`## Actors`, characterized (apply the new rule to ourselves).
- `vision/roadmap.md` — MODIFY: add the "Vision Actors" milestone row.
- `INDEX.md`, `strategic/features_history.md` — MODIFY (generated at closure via `sdlc_check.py index`).

devPNT source (`D:\SoftwareDev\devPNT\agent\core\`, redeploy via `setup_mcp.bat` = owner step):
- `mcp_system_prompt.md` — MODIFY: §4.2 `M-VISION` definition gains an Actors element; the Vision Alignment Gate list gains Actors. Deployed `~/.claude/CLAUDE.md` is regenerated, never hand-edited.

Release surfaces (repo root, owner publishes): `CHANGELOG.md`, `package.json`, `gemini-extension.json` (triple-bump, minor).

Blast radius: `## Target Users`/`## Users or Stakeholders` = 2 template spots + 1 dogfood doc (no `init.js`/generated-file copies). `sdlc_check.py` validates Vision *file presence + Status*, not headings (`VISION_FILES`, `ANALYSIS_SECTIONS`), so the rename does not break the eval battery. devPNT `PlanService.py`/`database_schemas.py` enforce only M-VISION *existence/linkage*, not content sections → no devPNT code change.

## Security and Threat Model
- No runtime surface. Documentation/doctrine + templates only. No external input, authN/authZ, crypto, network, personal data, or filesystem execution paths introduced.
- Only residual risk: doctrine drift between the skill's `## Actors` and the devPNT M-VISION Actors element. Mitigation: identical light shape in both; `review.md` is the single review definition both sides point at (DRY).

## Action Plan
- [ ] templates.md — Actors in the 3 Vision templates + Actor↔UseCase reference rule.
- [ ] elicitation.md — Actors in the structured round.
- [ ] SKILL.md — "Protect the Vision" + Vision Gate.
- [ ] review.md — Actors in the conformance set.
- [ ] Dogfood: project_vision.md `## Actors`; roadmap.md milestone row.
- [ ] devPNT source mcp_system_prompt.md §4.2 + Alignment Gate (owner redeploys).
- [ ] Closure: eval battery + `check`; regenerate INDEX + features_history; independent fresh-context review; stage CHANGELOG + version bump.

## Test Strategy
- `python -m unittest discover -s skills/agentic-sdlc-skill/scripts -p "test_*.py"` — full eval battery must stay green (no regression from the heading rename).
- `python skills/agentic-sdlc-skill/scripts/sdlc_check.py check` — CLEAN before DONE.
- Independent fresh-context review (`review.md`) of the diff — doctrine consistency (skill ↔ devPNT), anti-DRY vs use-cases, proportionality.
- Doc change: no unit runtime to exercise; verification is validator + eval battery + review.

## Diary / Current State
- 2026-07-08: L3 declared. Elicitation resolved 4 forks (scope=skill+devPNT M-VISION; Actor referenced by use-cases; light depth; term="Actors"). Orientation complete, Impact file-level concrete. Implementing.
- 2026-07-08: All surfaces implemented. Eval battery 51/51 OK; `check --hybrid` CLEAN. Independent fresh-context review PASS (2 WARN, both fixed): Impact map reconciled to the actual §3 SKILL.md edit; added a feature-local `## Actors` (+ loosened the `templates.md` feature-Actors comment) so this internal-tooling feature satisfies its own new rule. Pending owner: devPNT `setup_mcp.bat` redeploy; release bump + publish.
