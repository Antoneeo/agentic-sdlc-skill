---
id: capture_channels_the_days_decisions
expected: at a user-signed closing, the sweep question fires once with its inline search result, and the day's stated decision lands on the existing rails — an elicited dated note plus an L1 claim row (prov ELICITED, empty id, legal locator) on the existing topic; no new topic, nothing captured twice
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
  | c-pr-01 | Discounts above 15% require CFO approval | from 2026-06-15 | - | - | corpus/notes/discount-note.md#L5-5 | ELICITED | OK |
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
Quick check: what's our discount approval rule? ... ok. New rule from this morning's meeting: quotes above 50k EUR also need my personal sign-off, effective today. Ok chiudiamo per oggi.
## Pass criteria
- At the signed closing ("chiudiamo"), the agent runs the capture sweep ONCE, and the question carries its inline result (what it already recorded / found on the rails today) — the scheduled-elicitation form, not the five-part blocking form.
- The stated decision lands as: a `corpus/notes/*` note with `origin: elicited` and a `date:`, carrying the user's words; and a claim row on `pricing` with empty `id`, `prov: ELICITED`, source = that note with a legal `L<a>-<b>` locator.
- No new topic is created (the escalation triggers hold); nothing already on the rails is re-captured.
- The existing claim c-pr-01 is untouched.
