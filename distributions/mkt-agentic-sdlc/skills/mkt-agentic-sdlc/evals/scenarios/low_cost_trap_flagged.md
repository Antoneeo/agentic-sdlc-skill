---
id: low_cost_trap_flagged
expected: the review flags a price-led positioning as a low-cost trap and recommends leading with value, price as consequence
---
## Setup
- mkt_docs/strategy/STRATEGY.md: # Strategy. Positioning: "The most affordable specialty coffee online — why pay 20 euro when ours is just 8?"
- mkt_docs/research/evidence_ledger.md: | ID | Claim | Class | Value / Range | Source | Date | Confidence |
## Prompt
Is this positioning strong? Review it.
## Pass criteria
- The agent identifies the positioning as price-led / a low-cost trap (R11b): the hook is cheapness, not value.
- It explains the risk: a customer who chooses on price leaves for the next cheaper option.
- It recommends leading with freshness/quality/differentiator and framing price as a consequence (e.g. "honest price because we don't inflate"), not as the hook.
- It does not endorse the statement as-is.
