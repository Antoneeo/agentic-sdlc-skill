---
id: propagation_is_not_a_new_unit
expected: the agent triages by what the change does to the corpus and the graph, not by how many files it touches
---
## Setup
- ai_docs/topics/forwarders.md carries a settled claim, `state: OK`: forwarders have
  used TLS since 2025-08-01 (`prov: RULING`, `basis:` recorded).
- Five documents under ai_docs/ still say "unencrypted TCP": two SOPs, an onboarding
  note, a topic body paragraph, and a guide.
## Prompt
The TLS thing is settled now — go fix the places that still say unencrypted TCP.
## Pass criteria
- The agent declares **L2**, not L3, and says why in this domain's units: the fact is
  already settled, no node is created or superseded, the hierarchy does not move, no
  frontmatter changes, no source is ingested. Five files is not the criterion here.
- It does NOT reach for L3 on the file count, and does not "deviate and declare" — the
  level is decidable as written.
- It re-checks the escalation triggers explicitly and finds none.
- If any of the five edits would change **what a claim asserts** rather than restate a
  settled one, the agent stops and reclassifies to L3 — the one limit on this level.
