---
id: placement_rules_before_impact
expected: on an L3 unit the agent states the required knowledge concepts and rules EXISTS/INADEQUATE/MISSING against the topic graph BEFORE listing documents to change
---
## Setup
- ai_docs/topics/access-control.md: ---\ntopic: access-control\ndescription: Who may operate which devices.\nparents: []\nowns: [access-control/operator-groups]\nstatus: CURRENT\n---\n\n## Claims\n\n| id | claim | valid | qty | about | source | prov | state |\n|---|---|---|---|---|---|---|---|\n
- ai_docs/topics/INDEX.md: generated topic index, listing access-control and its `owns:` keys
- ai_docs/vision/project_vision.md: # Project Vision\nStatus: APPROVED (by owner)\n## North Star\nA knowledge base an installer can trust on site.
- ai_docs/corpus/given/manual-ab12cd34.txt: a manual describing per-company scoping, operator groups and licence tiers
## Prompt
Ingest this manual and make it answerable how authorizations can be scoped per company. This is an L3 unit; produce the ANALYSIS first.
## Pass criteria
- BEFORE any document list, the ANALYSIS carries a `## Capability Ledger` stating the knowledge concepts the unit requires as domain subjects -- no file names in the capability column. This lens's capability pass is the TAXONOMY pass (`taxonomy.md`); an agent reaching for a code architect pass -- a Component Map, an architect support file -- FAILS, because kb ships none of them.
- "operator groups" is ruled **EXISTS** citing `topics/access-control.md` and its `owns:` key, read from the topic index and verified in the node -- the agent does NOT create a second node for a concept already owned (the double-placement failure `owns:` exists to prevent).
- "per-company scoping" is ruled **MISSING** with the descent named: the index keys walked, the synonyms tried, the guides consulted.
- The MISSING concept becomes a node whose `topic:` and `description:` are stated WITHOUT naming this ingestion unit, which the unit then feeds claims into.
- The `## Impact` document list is derived from the ledger, not drafted before it.
