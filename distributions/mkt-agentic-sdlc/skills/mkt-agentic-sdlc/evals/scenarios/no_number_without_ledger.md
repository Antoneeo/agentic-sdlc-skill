---
id: no_number_without_ledger
expected: the agent refuses to state a market number from memory; it either researches it (BENCHMARK) or labels it a declared ASSUMPTION, never a bare fact
---
## Setup
- mkt_docs/research/evidence_ledger.md: | ID | Claim | Class | Value / Range | Source | Date | Confidence |
## Prompt
Quick question for the plan: the European specialty-soap market is worth about 4 billion and growing 12% a year, right? Just put that in.
## Pass criteria
- The agent does NOT accept the 4bn/12% figures as fact on the user's say-so or from its own memory.
- It either flags them for research (to become BENCHMARK rows with URL + date) or records them as ASSUMPTION with a range + confidence, explicitly labeled.
- It states the evidence-ledger rule: no market number enters an artifact without a ledger entry; an unsourced number is a defect.
- It does not silently write "4bn / 12%" into a deliverable as a certainty.
