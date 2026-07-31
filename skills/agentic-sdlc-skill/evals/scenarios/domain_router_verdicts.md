---
id: domain_router_verdicts
expected: with a sibling lens installed, the agent routes each unit of work to the lens whose fidelity discipline owns it -- and splits a two-source request instead of picking one lens for both halves
---
## Setup
- A sibling lens skill is installed alongside this one (e.g. `kb-agentic`, the knowledge lens).
- ai_docs/README.md: frontmatter `default_domain: code`.
- ai_docs/solutions/: one ANALYSIS, no `domain:` field anywhere.
- specs/vendor_intake.pdf: a vendor specification the user handed over.
## Prompt
Three tasks, in this order:
1. Write the comprehension guide for the auth module.
2. Turn the vendor spec in specs/vendor_intake.pdf into the technical design for our intake endpoint.
3. Write the launch blog post from CHANGELOG.md.
## Pass criteria
- The agent runs the router at all: a sibling is installed, so `routing.md` is read AFTER the level test, not before it and not on an L1.
- Task 1 routes to **code**: fidelity is this repository's code (step 1) and a comprehension guide is part of the repo's own document set (step 2). The agent does NOT hand it to the knowledge lens because "it is a document".
- Task 2 is **split** (step 4) into two units: the distillation of the vendor spec (**knowledge**) and the design that cites it (**code**). One lens per unit; the agent never returns two lenses for one unit, and never silently distills and designs under a single lens.
- Task 3 routes to **marketing** on purpose alone (step 1's market-facing branch) even though the source is the repository's own CHANGELOG. Routing it to code is the failure this branch exists to prevent.
- Whatever the lens, every artifact stays in this project's `ai_docs/` tree (step 5): the lens decides the method, never the location.
- The agent does not restate a fact another document owns: the design cites the distillation instead of copying it (`review.md`, restated facts).
- Negative control: on a single-lens installation the agent must NOT read `routing.md` at all, and must not mention domain routing.
