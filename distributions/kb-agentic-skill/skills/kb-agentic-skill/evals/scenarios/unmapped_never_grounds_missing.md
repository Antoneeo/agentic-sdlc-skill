---
id: unmapped_never_grounds_missing
expected: where the topic index has not been descended, the agent descends it instead of ruling MISSING from its silence
---
## Setup
- ai_docs/topics/site-configuration.md: ---\ntopic: site-configuration\ndescription: How an installation is set up before use.\nparents: []\nowns: [site-configuration/wizard, site-configuration/multi-company-toggle]\nsynonyms: [site wizard, setup]\nstatus: CURRENT\n---\n\n## Claims\n\n| id | claim | valid | qty | about | source | prov | state |\n|---|---|---|---|---|---|---|---|\n| c1 | The multi-company feature is disabled by default and must be enabled in the site wizard | - | - | - | corpus/given/manual-ab12cd34.txt#p=1@42-61 | GIVEN | OK |\n  <-- the node the trap hides: the concept lives here, under a name the query does not use
- ai_docs/topics/access-control.md: a node about operator permissions, owning nothing about defaults
- ai_docs/topics/INDEX.md: generated index; the agent has read only the `access-control` branch this session
- ai_docs/vision/project_vision.md: # Project Vision\nStatus: APPROVED (by owner)\n## North Star\nA knowledge base an installer can trust on site.
## Prompt
Does the multi-company feature need enabling, or is it on out of the box? Add what we know as a new topic if we don't have it.
## Pass criteria
- The agent does NOT rule the concept MISSING because the branch it happened to read is silent about it: an index not descended is **unread, not empty** (`taxonomy.md` §2).
- It DESCENDS the index and tries synonyms ("site wizard", "setup", "default", "enable") before any verdict, and finds `topics/site-configuration.md` owning `site-configuration/multi-company-toggle`.
- Verdict comes out **EXISTS** (or INADEQUATE with the gap named) citing that node and its `owns:` key -- never a bare MISSING.
- If the agent rules MISSING and creates a second node for the same concept, the scenario FAILS: that is the double-placement `owns:` exists to prevent, and it splits one fact across two homes where later descent finds only one of them.
- A genuinely absent concept for which no source asserts anything is a `gaps:` entry on the owning node, not a new empty node.
