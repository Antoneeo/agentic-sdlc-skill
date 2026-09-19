---
description: Concise catalog of the skill's existing features.
status: CURRENT
---
# Existing Features

- [057] **Shared Project Memory**: Every distribution includes a catalog of original project documents, live metadata `recall`, and shared topic/claim/corpus integrity. One installed skill suffices; workflow ownership remains domain-specific. No status aggregation, automatic claims, semantic search or watcher. See `reference/GUIDE_shared_project_memory.md` for implementation boundaries.

- [000] **Project Initialization**: Creates baseline `ai_docs/` governance files and agent protocol instructions for supported AI tools.
- [001] **Vision Governance**: Adds `ai_docs/vision/`, Vision templates, and a mandatory Vision Gate before feature analysis.
- [002] **Agentic SDLC vNext**: Adds risk triage, installed support files, Gemini native skill installation, mechanical validation, and devPNT M-VISION symbiosis while preserving full Standalone operation.
- [020] **Architect Pass**: At L3, between the spec elicitation and the Impact, the feature is stated as required capabilities and each is ruled against the platform (EXISTS / INADEQUATE / MISSING); what is missing is designed as a component with its own contract, of which the feature is one consumer. Recorded in the ANALYSIS `## Capability Ledger` and checked by the closure review.
- [032] **Interface Contract**: At L3, when the change touches a surface an actor acts on or perceives, the ANALYSIS carries a conditional `## Interface Contract` between the use cases and the Capability Ledger — per use case: the actors and surfaces; the information & processing flow (the heart) naming the components it traverses as responsibility-holders; the required affordances; universal feedback (error and intermediate states, and a software actor's return status); the architectural constraints touched; and surfaced feasibility flags. Existing idioms reused by default. The contract names the components in the flow, never their mechanism; the solution inherits the interaction (Hybrid: D-UC → D-IC → P-TM → E-ISP). Enforced by a lens-keyed review clause and a wiring invariant test.
