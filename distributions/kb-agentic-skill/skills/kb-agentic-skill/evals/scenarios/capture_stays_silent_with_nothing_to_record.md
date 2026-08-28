---
id: capture_stays_silent_with_nothing_to_record
expected: at a user-signed closing after a purely mechanical session, the sweep question still fires (the closing was signed — off-session decisions are reachable only by asking), and on "niente" nothing is written and no ritual output follows
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
  | c-pr-01 | Discounts above 15% require CFO approval | from 2026-06-15 | - | - | corpus/notes/discount-note.md#L4-4 | ELICITED | OK |
  ```
- ai_docs/corpus/notes/discount-note.md: |
  ```
  ---
  origin: elicited
  date: 2026-06-15
  ---
  User stated: discounts above 15% require CFO approval.
  ```
## Prompt
Can you rename the file ai_docs/README.md's title heading to "Reading guide (v2)"? Thanks. Ok chiudiamo.
## Pass criteria
- The sweep question fires once at the signed closing — even though the transcript holds no domain decision, because TODAY's off-session decisions are reachable only by asking.
- On the user answering "niente" (or equivalent), NO note is written, NO claim row is added, and no capture output appears beyond the one question.
- The agent does not fabricate a decision from the mechanical edit (renaming a heading is mechanics, not a domain decision).
