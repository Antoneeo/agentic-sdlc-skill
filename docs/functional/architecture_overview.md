<!-- devpnt:generated
  date: 2026-06-13T05:23:50
  generator: functional_docs_generator v1.0
  sources: agentic-sdlc-v2, agentic-sdlc-v2/agentic-sdlc-v2, ai_docs, ai_docs/audit, ai_docs/solutions, ai_docs/strategic
  model: GoogleGemini/gemini-flash-lite-latest
  summary_hash: 066ff8bf7cdfbd07
-->

## Subsystems

| Subsystem | Role | Key Responsibilities |
| :--- | :--- | :--- |
| agentic-sdlc-v2 | Root Architectural Framework | Defines meta-level governance, schema constraints, and behavioral policies. |
| ai_docs | Architectural Registry | Centralizes audit, solutions, strategy, and vision domains for ecosystem governance. |
| ai_docs/audit | Administrative Control Plane | Manages Vision Governance compliance. |
| ai_docs/solutions | Architectural Knowledge Base | Acts as the governance repository for project solutions. |
| ai_docs/strategic | Architectural Registry | Functions as the central registry for governance and history. |
| ai_docs/vision | Foundational Governance Layer | Provides the base layer for AI-driven software development. |
| examples | Pedagogical Resource | Contains project-specific documentation artifacts and reference implementation patterns. |
| references | Template Library | Provides standardized Markdown templates for project governance and lifecycle management. |
| scripts | Lifecycle Management | Automates provisioning, installation, and removal of AI-assisted development protocols. |
| sdlc-test-project | Meta-governance Layer | Enforces development state machine (Audit → Analysis → Dev/Test → Closing). |
| sdlc-test-project/ai_docs | Documentation Layer | Centralizes documentation for project governance. |
| skills | Agentic Capability Namespace | Aggregates modular, domain-specific logic in a plugin-based design. |
| skills/agentic-sdlc-skill | Contract-first Framework | Defines behavioral contracts for development lifecycle. |

## Dependency Map

(none)

## Boundaries

- agentic-sdlc-v2: does not implement low-level application business logic.
- ai_docs: does not execute automated deployment pipelines.
- ai_docs/audit: does not perform direct software development or coding.
- ai_docs/solutions: does not provide generic document storage.
- ai_docs/strategic: does not manage real-time project operational data.
- ai_docs/vision: does not define specific implementation details.
- examples: does not function as an active production environment.
- references: does not enforce project-specific business rules.
- scripts: does not host architectural documentation.
- sdlc-test-project: does not handle core library dependencies.
- sdlc-test-project/ai_docs: does not perform automated code testing.
- skills: does not act as a primary interface for end-users.
- skills/agentic-sdlc-skill: does not manage external cloud infrastructure.