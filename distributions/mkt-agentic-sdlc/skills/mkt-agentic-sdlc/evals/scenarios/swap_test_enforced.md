---
id: swap_test_enforced
expected: the CMO review flags a generic positioning statement that survives the swap test, and blocks the strategy gate
---
## Setup
- mkt_docs/strategy/STRATEGY.md: # Strategy. Positioning statement: "AcmeRoast: quality and artisan passion for people who love real coffee, every day."
- mkt_docs/research/evidence_ledger.md: | ID | Claim | Class | Value / Range | Source | Date | Confidence |
## Prompt
Review this positioning statement for the strategy gate and tell me if it's ready to ship.
## Pass criteria
- The agent runs the swap test on the ACTUAL published statement (substitutes top competitors' names).
- It finds the statement survives the swap for competitors (any roaster could say "quality and artisan passion") and marks it a BLOCK — positioning fails to exclude.
- It flags the value prop as generic / interchangeable (R11).
- It does NOT pass the gate; it asks for differentiators (what only this business can claim) before proceeding.
