<!-- devpnt:generated
  date: 2026-07-22T06:50:08
  generator: functional_docs_generator v1.0
  sources: ai_docs, ai_docs/functional, evals, evals/e3_contrast_b2b, evals/e3_synthetic_v01, scripts
  model: GoogleGemini/gemini-flash-lite-latest
  summary_hash: 8311620e773ed785
-->

## Subsystems
| Subsystem | Role | Key Responsibilities |
| --- | --- | --- |
| `ai_docs` | Documentation root | Organizes design specifications, reference materials, and bridges high-level system design with operational execution. |
| `ai_docs/functional` | Functional markdown repository | Serves as the central repository for structural invariants and runtime modes; contains 5 functional documentation files detailing system architecture, data entities, and execution entries. |
| `evals` | Evaluation framework container | Aggregates evaluation frameworks, scenarios, and artifacts to test multi-agent architectures and workflows; houses static ground-truth dossiers, behavioral personas, and adversarial test suites. |
| `evals/e3_contrast_b2b` | Test vector container | Contains evaluation artifacts and test vectors for the E3 B2B contrast scenario within the evaluation framework. |
| `evals/e3_synthetic_v01` | Scenario evaluator | Evaluates the e3_synthetic_v01 marketing agentic SDLC for Caffè Brancaleone. |
| `scripts` | Lifecycle management infrastructure | Automates environment bootstrapping, skill deployment, and clean-up across various AI CLI clients by centralizing detection and file-system primitives in a shared library. |
| `skills` | Capability container | Acts as a container for modular agentic capabilities and domain-specific frameworks; holds the `mkt-agentic-sdlc` subdirectory. |
| `skills/mkt-agentic-sdlc` | SDLC framework implementation | Implements the marketing agentic SDLC framework, providing structured workflows, evidence-first governance, policy guides, elicitation protocols, and validation scripts. |

## Dependency Map
(none)

## Boundaries
- ai_docs: does not execute runtime code
- ai_docs/functional: does not provide operational scripts
- evals: does not handle production marketing workflows
- evals/e3_contrast_b2b: does not manage environment bootstrapping
- evals/e3_synthetic_v01: does not handle B2B contrast test vectors
- scripts: does not generate static documentation
- skills: does not execute system environment setups directly
- skills/mkt-agentic-sdlc: does not manage CLI client detection primitives