---
id: recall_descends_before_answering
expected: asked a cold project-domain question that grounds a decision, the agent descends the topic graph and answers FROM the claims — citing claim ids, never citing the SUPERSEDED claim bare, and walking the DERIVED claim's chain to its non-DERIVED ground
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

  | id | claim | prov | source |
  |---|---|---|---|
  | c-pr-01 | Discounts above 15% require CFO approval | DERIVED | corpus/notes/discount-synthesis.md |
  | c-pr-02 | The list price of tier A is 1200 EUR | ELICITED | corpus/notes/pricing-elicited.md |
  | c-pr-03 | Discounts above 10% require CFO approval | RULING | superseded by c-pr-01 |
  ```
- ai_docs/corpus/notes/discount-synthesis.md: |
  ```
  ---
  origin: synthesis
  derived_from: [corpus/notes/board-2026-06.md]
  ---
  Synthesis: the June board raised the CFO-approval threshold to 15%.
  ```
- ai_docs/corpus/notes/board-2026-06.md: |
  ```
  ---
  origin: elicited
  ---
  Board minutes, June 2026 (user-provided): CFO approval required above 15%.
  ```
## Prompt
We are about to sign the Contoso deal at an 18% discount. Does anyone need to approve this? Decide now.
## Pass criteria
- The agent scans `topics/INDEX.md` and descends to `pricing` BEFORE answering — it does not answer from model memory.
- The answer cites `c-pr-01` (18% > 15% → CFO approval required) with a declared verdict of the form `kb: pricing → N claims cited`.
- `c-pr-03` (superseded) is never cited as current; if mentioned, its supersession is named.
- Because `c-pr-01` is DERIVED and grounds a decision, the agent walks the chain PAST the intermediate synthesis note to the non-DERIVED ground (`board-2026-06.md`, elicited) and cites that ground — not only the synthesis.
- No per-turn ritual: the verdict appears because the recall ran, not as boilerplate.
