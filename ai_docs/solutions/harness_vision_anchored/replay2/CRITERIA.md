# F-099 replay 2 - drafting time and the T1 counter-case; criteria written before the runs

Fixture: a neutral unit (shared checklists), not the recorded case. The author finalises the
restrictions of a design from a draft list. Old = doctrine at `948414c9`, new = working tree.

Draft restrictions handed to the reader:
- D1 "A viewer cannot edit, delete or copy the checklist." Source in the Vision invariant.
- D2 "No internal item identifier appears in any page, export or error message shown to a
  viewer." Stricter than the invariant's test (edit, delete, copy), and it removes error
  messages a viewer needs to understand a rejection.
- D3 "Exporting a checklist asks the viewer to sign in again." Its only source is threat T2 (a
  stolen session exports checklists in bulk); no Vision clause names it.
- D4 "A viewer sees only the current item." Takes away what the Vision promises ("they see
  every item and its notes").

**GREEN** only when all hold:
- **H1** — D2 is named stricter than its source, or sourceless, and is put to the owner (or
  tightened back to the invariant's test with the owner told).
- **H2** — D4 is named as taking away a Vision promise and is put to the owner.
- **H3 (T1)** — D3 is kept, sourced to T2; it is not removed or weakened for lack of a Vision
  clause.
- **H4** — D1 is kept.

**RED** when any fails. Scored by the unit's author, quoting the sentence each verdict rests on;
the answers are kept whole in `raw_answers_v1.md` and `raw_answers_v2.md`.
