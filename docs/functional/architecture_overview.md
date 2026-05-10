<!-- devpnt:generated
  date: 2026-05-10T08:11:22
  generator: functional_docs_generator v1.0
  sources: examples, references, scripts, skills, skills/agentic-sdlc-skill
  model: GoogleGemini/gemini-3.1-flash-lite-preview
  summary_hash: 93e45e2c2b7cb9b4
-->

## Subsystems

| Subsystem | Role | Key Responsibilities |
| :--- | :--- | :--- |
| examples | Project root container | Organizational wrapper for demos, governance, and reference material. |
| references | Documentation library | Enforces architectural rigor and provides standard communication templates. |
| scripts | Bootstrapping layer | Automates workspace setup and enforces documentation structures. |
| skills | Operational registry | Acts as a modular container for agent-specific capabilities. |
| skills/agentic-sdlc-skill | SDLC protocol | Houses the "Documentation-First" SDLC operational protocol. |

## Dependency Map

(none)

## Boundaries

- examples: does not implement core application logic
- references: does not execute automated tasks
- scripts: does not host business-level agent skills
- skills: does not provide global documentation templates
- skills/agentic-sdlc-skill: does not handle infrastructure environment setup