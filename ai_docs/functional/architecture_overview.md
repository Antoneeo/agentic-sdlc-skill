---
description: devPNT-generated functional overview of the skill package architecture. Snapshot 2026-07-02; regenerate via devPNT after structural changes.
status: CURRENT
---
<!-- devpnt:generated
  date: 2026-07-02T08:44:57
  generator: functional_docs_generator v1.0
  sources: agentic-sdlc-v2, agentic-sdlc-v2/agentic-sdlc-v2, ai_docs, ai_docs/audit, ai_docs/functional, ai_docs/reference
  model: GoogleGemini/gemini-flash-lite-latest
  summary_hash: 21d805a852554acf
-->

## Subsystems

| Subsystem | Role | Key Responsibilities |
| :--- | :--- | :--- |
| agentic-sdlc-v2 | Architectural Framework | Defines meta-governance, schema constraints, and behavioral policies. |
| ai_docs | Knowledge Base | Centralizes architectural intent, compliance registries, and feature tracking. |
| ai_docs/audit | Audit Registry | Tracks architectural compliance and system auditing status. |
| ai_docs/functional | Functional Registry | Acts as a static registry for architectural documentation. |
| ai_docs/reference | Reference Store | Serves as a placeholder for technical references. |
| ai_docs/solutions | Procedural Repository | Stores architectural and procedural documentation for workflows. |
| ai_docs/strategic | Governance Base | Functions as the central project governance knowledge base. |
| ai_docs/vision | Strategic Root | Defines the strategic foundation for the SDLC methodology. |
| examples | Resource Library | Houses pedagogical resources and reference implementation patterns. |
| references | Template Library | Provides standardized Markdown templates for project governance. |
| scripts | Lifecycle Engine | Orchestrates project bootstrapping and cross-environment tool synchronization. |
| sdlc-test-project | Meta-Governance Layer | Enforces development state machine protocols and document-anchored code changes. |
| sdlc-test-project/ai_docs | Project Docs | Acts as the documentation layer for project-specific governance. |
| skills | Capability Root | Acts as a namespace for modular domain-specific automation capabilities. |
| skills/agentic-sdlc-skill | Skill Governance | Establishes a framework for automated development governance. |

## Dependency Map

(none)

## Boundaries

- agentic-sdlc-v2: does not perform direct project execution
- ai_docs: does not execute system code directly
- ai_docs/audit: does not generate development code
- ai_docs/functional: does not provide operational logic
- ai_docs/reference: does not contain active implementation logic
- ai_docs/solutions: does not handle low-level infrastructure bootstrapping
- ai_docs/strategic: does not manage individual file-system states
- ai_docs/vision: does not perform tactical task automation
- examples: does not provide production-grade software frameworks
- references: does not enforce runtime code validation
- scripts: does not define high-level strategic vision
- sdlc-test-project: does not manage global architectural templates
- sdlc-test-project/ai_docs: does not execute automated tool synchronization
- skills: does not handle project-wide lifecycle governance
- skills/agentic-sdlc-skill: does not perform architectural oversight