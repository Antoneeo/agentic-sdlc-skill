<!-- devpnt:generated
  date: 2026-06-07T10:17:40
  generator: functional_docs_generator v1.0
  sources: ai_docs, ai_docs/audit, ai_docs/solutions, ai_docs/strategic, examples, references
  model: GoogleGemini/gemini-flash-lite-latest
  summary_hash: 402b28983d22f057
-->

## Subsystems

| Subsystem | Role | Key Responsibilities |
| :--- | :--- | :--- |
| ai_docs | Knowledge Hub | Centralizes documentation for administrative audit tracking, plugin standards, and strategic design. |
| ai_docs/audit | Administrative Workspace | Tracks technical debt and maintains audit-related records. |
| ai_docs/solutions | Architectural Knowledge Base | Stores architectural information for Antigravity 2.0 modules. |
| ai_docs/strategic | Documentation Hub | Acts as the central repository for high-level architectural design. |
| examples | Pedagogical Resource | Provides reference implementation patterns and architectural guidelines. |
| references | Governance Layer | Houses static Markdown templates for engineering artifacts and definitions. |
| scripts | Infrastructure Management | Automates onboarding, environment integration, and AI-agent skill synchronization. |
| sdlc-test-project | Meta-governance Layer | Enforces development state machine protocols and documents code changes. |
| sdlc-test-project/ai_docs | Documentation Layer | Centralizes documentation for project governance. |
| skills | Capabilities Container | Acts as a repository for domain-specific agentic capabilities. |
| skills/agentic-sdlc-skill | Architectural Foundation | Provides documentation-first logic for SDLC operations. |

## Dependency Map

(none)

## Boundaries

- ai_docs: does not execute application code
- ai_docs/audit: does not perform architectural design
- ai_docs/solutions: does not track administrative audits
- ai_docs/strategic: does not manage infrastructure scripts
- examples: does not enforce development state machines
- references: does not implement business logic
- scripts: does not provide architectural documentation
- sdlc-test-project: does not house pedagogical resources
- sdlc-test-project/ai_docs: does not synchronize external agent tools
- skills: does not manage environment onboarding
- skills/agentic-sdlc-skill: does not provide project-wide design templates