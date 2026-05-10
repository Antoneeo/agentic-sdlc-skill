<!-- devpnt:generated
  date: 2026-05-10T06:55:37
  generator: functional_docs_generator v1.0
  sources: examples, references, scripts, skills, skills/agentic-sdlc-skill
  model: GoogleGemini/gemini-3.1-flash-lite-preview
  summary_hash: 3d3bff1727b4fcba
-->

## Subsystems

| Subsystem | Role | Key Responsibilities |
| :--- | :--- | :--- |
| examples | Root container | Project-level demonstration, governance, and reference documentation. |
| references | Documentation library | Enforcing architectural rigor, consistency, and standard communication schemas. |
| scripts | Bootstrapping layer | Workspace environment setup, enforcing documentation structures, and idempotent filesystem operations. |
| skills | Capability registry | Organizing domain-specific workflows into modular, reusable packages. |
| skills/agentic-sdlc-skill | Architectural backbone | Providing core development lifecycle capabilities for agents. |

## Dependency Map

(none)

## Boundaries

- examples: does not implement core agentic logic
- references: does not execute system-level automation scripts
- scripts: does not define domain-specific agentic skills
- skills: does not handle project-level governance documentation
- skills/agentic-sdlc-skill: does not manage repository-wide environment bootstrapping