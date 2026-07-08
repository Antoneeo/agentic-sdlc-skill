<!-- devpnt:generated
  date: 2026-07-08T11:36:15
  generator: functional_docs_generator v1.0
  sources: agentic-sdlc-v2, agentic-sdlc-v2/agentic-sdlc-v2, ai_docs, ai_docs/audit, ai_docs/functional, ai_docs/reference
  model: GoogleGemini/gemini-flash-lite-latest
  summary_hash: a188f942d6fdfadc
-->

## Subsystems

| Subsystem | Role | Key Responsibilities |
| :--- | :--- | :--- |
| agentic-sdlc-v2 | Root architectural framework | Defines meta-level governance, schema constraints, and behavioral policies. |
| ai_docs | Centralized governance authority | Organizes hierarchical documentation from strategic vision to release runbooks. |
| ai_docs/audit | Governance and tracking layer | Tracks system architecture and ensures documentation-first compliance. |
| ai_docs/functional | Canonical documentation layer | Stores detailed functional specifications for the SDLC framework. |
| ai_docs/reference | Documentation hub | Centralizes reference material for the agentic-sdlc ecosystem. |
| ai_docs/solutions | Architectural repository | Houses the agentic-sdlc skill and associated implementation assets. |
| ai_docs/strategic | High-level command center | Manages high-level governance and architectural strategy. |
| ai_docs/vision | Strategic root | Orchestrates the strategic vision for the Agentic SDLC methodology. |
| examples | Pedagogical resource root | Provides implementation patterns and architectural guideline references. |
| references | Foundational library | Provides standardized Markdown templates for project governance and design. |
| scripts | Lifecycle management infrastructure | Handles workspace initialization, AI client integration, and tool deployment. |
| sdlc-test-project | Meta-governance layer | Enforces strict state-machine development protocols. |
| sdlc-test-project/ai_docs | Project documentation layer | Manages project-specific governance documentation. |
| skills | Agentic capabilities root | Encapsulates specialized agentic capabilities and documentation policies. |
| skills/agentic-sdlc-skill | SDLC framework implementation | Defines documentation-first SDLC governance for LLM-driven development. |

## Dependency Map

(none)

## Boundaries

- agentic-sdlc-v2: does not perform direct project execution
- ai_docs: does not implement low-level deployment scripts
- ai_docs/audit: does not manage functional specification authoring
- ai_docs/functional: does not provide high-level strategic oversight
- ai_docs/reference: does not house pedagogical project examples
- ai_docs/solutions: does not generate standardized governance templates
- ai_docs/strategic: does not define granular functional requirements
- ai_docs/vision: does not handle technical release runbooks
- examples: does not provide core infrastructure lifecycle management
- references: does not enforce project-specific state machine rules
- scripts: does not define architectural strategic vision
- sdlc-test-project: does not house the global agentic skill logic
- sdlc-test-project/ai_docs: does not manage environment initialization
- skills: does not handle project-specific documentation maintenance
- skills/agentic-sdlc-skill: does not perform local workspace orchestration