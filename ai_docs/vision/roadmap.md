# Vision Roadmap
Status: DRAFT

| Milestone | Expected Benefit | Priority | Success Signal | Status |
|:---|:---|:---|:---|:---|
| Vision Governance | Prevent strategic drift during agent-led development | High | `ai_docs/vision/` is created by default and consulted before feature analysis | [COMPLETED] |
| Agentic SDLC vNext | Keep the skill autonomous while adding proportional triage, mechanical checks, and devPNT milestone Vision alignment | High | Runtime skill folder includes support files and installer covers Claude, Codex, and Gemini | [COMPLETED] |
| Vision Actors | Characterize the actors in the Vision so UX is designed for named roles, not an implicit "user" | Medium | Vision templates carry `## Actors`; each use-case attaches to a defined actor; devPNT M-VISION mirrors it | [COMPLETED] |
| Agent Evolution (operative guides, subagents, devPNT seam) | An agent starting with no prior context inherits the project's model instead of rebuilding it, and the process is one and the same whether devPNT is present or not | High | The guide layer is shipped and consumed: `reference/GUIDE_*.md` with the generated router, consult verdict declared with triage; the Hybrid ownership matrix names one master per artifact | [COMPLETED] |
| Verifiable Vision | The Vision Gate becomes testable: a reviewer with no project context can rule ACCEPT/REJECT on a proposal quoting one line of the Vision, instead of trusting the author's intent | High | `project_vision.md` is APPROVED only after blind adversarial rounds; the standing battery (`audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`) is re-run on every Vision edit | [COMPLETED] |
| Architect Pass + Design Review Gate | Designs are ruled at capability level before files are named, and independently reviewed before any code — myopia caught at design time, not at closure | High | Every L3 ANALYSIS carries a Capability Ledger; the design-gate review is logged in `audit/reviews/REVIEW_LOG.md` before implementation starts | [COMPLETED] |
| Multi-Domain Core (F-022) | One authored source of process discipline, three distributions (`agentic-sdlc`, `kb-agentic`, `mkt-agentic-sdlc`): maintenance stops scaling with the number of domains, and a fourth domain is an overlay, not a fork | High | One repository publishes three packages; spine divergence between the distributed copies is caught mechanically; `npm pack` is correct for all three | [DONE — release HELD] |
| kb Knowledge Method (F-024, consuming the Claim Ledger F-025) | kb answers the question it exists for — what do we already know about this, how sure are we, and where did it come from — with conflicts detected and held open, resolved only by new information, never by a silent guess | High | The owner's acceptance bar: a real corpus ingested end to end, and the planning and evaluation questions answered from the graph rather than by re-reading the documents | [IN_PROGRESS] |

## Notes
- Vision documents sit above strategic architecture docs: they explain why the project exists and where it should not go.
- Architecture, analysis, and tests remain mandatory, but they must now be interpreted through the Vision Gate.
- Status describes each milestone itself, in delivery order; this table is the "milestones and sequencing" home `project_vision.md` points at, and it orders nothing below milestone level.
- F-numbers resolve in `strategic/features_history.md` (generated); per-feature detail lives in `solutions/ANALYSIS_*.md`. "Release HELD" on F-022 is the owner's ruling of 2026-08-01: nothing is published until the kb Knowledge Method is effective.
