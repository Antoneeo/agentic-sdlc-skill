---
id: import_places_never_overwrites
expected: importing a bundle into a populated graph runs the placement pass and merges by hand; it never overwrites a node, and it never lets a foreign ruling settle a local disagreement
---
## Setup
- A bundle exported from another project, containing `topics/pricing.md` (about a **vendor's licence tiers**) plus the corpus artifacts its claims cite.
- The target project already has `ai_docs/topics/pricing.md`, about **what this client is charged** — same slug, different concept.
- The bundle also carries a claim with `prov: IMPORTED`, whose note says `imported_from: project-A` and keeps the original `basis:`.
- The target has a local claim that disagrees with that imported one.
## Prompt
Import this bundle into the project, then tell me which pricing applies.
## Pass criteria
- The agent runs `import` and reports the skipped node rather than overwriting it. Overwriting `topics/pricing.md`, or merging the two bodies without a verdict, FAILS.
- It then runs the **placement pass** (`taxonomy.md`) on the incoming concept and reaches a verdict — most likely a sibling **with the distinguishing line written**, since "the vendor's tiers" and "what this client pays" are different subjects that share a word.
- It does NOT resolve the disagreement using the `IMPORTED` row. It states that a foreign ruling cannot settle a local one, and that re-ratification is the owner's act: own note, own `basis:`, `prov: RULING`.
- It runs `check` after importing and reports the result — the import is deliberately not a validator.
- Claims already present are recognised **by id**, not by comparing text: the same artifact cited at the same span mints the same id in every project.
