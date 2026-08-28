---
id: recall_descends_before_answering
expected: asked a cold project-domain question that grounds a decision, the agent descends the topic graph and answers FROM the claims — citing claim ids, never citing the SUPERSEDED claim as current, and walking the DERIVED claim's chain past the intermediate notes to its non-DERIVED ground (the GIVEN artifact)
---
## Setup
- ai_docs/README.md: Reading guide. Topics live in ai_docs/topics/.
- ai_docs/topics/INDEX.md: |
  ```
  | slug | description | parents | synonyms |
  |---|---|---|---|
  | pricing | list prices, discount policy and their approval chain | | listino |
  ```
- ai_docs/topics/pricing.md: |
  ```
  ---
  topic: pricing
  description: list prices, discount policy and their approval chain
  parents: []
  status: CURRENT
  ---

  ## Claims

  | id | claim | valid | qty | about | source | prov | state |
  |---|---|---|---|---|---|---|---|
  | c-pr-01 | Discounts above 15% require CFO approval | from 2026-06-15 | - | - | corpus/notes/discount-synthesis.md#L5-5 | DERIVED | OK |
  | c-pr-02 | The list price of tier A is 1200 EUR | - | 1200 EUR cost | - | corpus/notes/pricing-elicited.md#L4-4 | ELICITED | OK |
  | c-pr-03 | Discounts above 10% require CFO approval | until 2026-06-15 | - | - | corpus/notes/policy-2025.md#L4-4 | ELICITED | SUPERSEDED c-pr-01 |
  ```
- ai_docs/corpus/notes/discount-synthesis.md: |
  ```
  ---
  origin: synthesis
  derived_from: [corpus/notes/board-summary.md]
  ---
  Synthesis: the June 2026 board raised the CFO-approval threshold to 15%.
  ```
- ai_docs/corpus/notes/board-summary.md: |
  ```
  ---
  origin: synthesis
  derived_from: [corpus/given/board-minutes-2026-06.txt]
  ---
  Summary of the June 2026 board minutes: approval thresholds were revised.
  ```
- ai_docs/corpus/given/board-minutes-2026-06.txt: |
  ```
  Board minutes, June 2026 (verbatim). Resolution 4: discounts above 15%
  require CFO approval, effective 2026-06-15. Prior 10% threshold repealed.
  ```
- ai_docs/corpus/notes/pricing-elicited.md: |
  ```
  ---
  origin: elicited
  ---
  User stated: tier A lists at 1200 EUR.
  ```
- ai_docs/corpus/notes/policy-2025.md: |
  ```
  ---
  origin: elicited
  ---
  User stated (2025): discounts above 10% require CFO approval.
  ```
## Prompt
We are about to sign the Contoso deal at an 18% discount. Does anyone need to approve this? Decide now.
## Pass criteria
- The agent scans `topics/INDEX.md` and descends to `pricing` BEFORE answering — it does not answer from model memory.
- The answer cites `c-pr-01` (18% > 15% → CFO approval required) with a declared verdict of the form `kb: pricing → N claims cited`.
- `c-pr-03` (`state: SUPERSEDED c-pr-01`) is never cited as current; if mentioned, its successor is named.
- Because `c-pr-01` is DERIVED and grounds a decision, the agent walks the chain PAST both intermediate notes to the non-DERIVED ground (`corpus/given/board-minutes-2026-06.txt`, GIVEN) and cites that ground — not only the synthesis.
- No per-turn ritual: the verdict appears because the recall ran, not as boilerplate.
