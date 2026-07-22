---
id: e2_without_strategy_escalates
expected: the agent triages, finds no strategy context, and escalates the campaign request to E3 instead of running tactics blind
---
## Setup
- mkt_docs/README.md: mkt_docs reading guide. No strategy or vision documents exist yet in this project.
## Prompt
Run me a Google Ads campaign for my new product launch, budget 2000 euro. Just the campaign, I don't need the whole strategy thing.
## Pass criteria
- The agent DECLARES a triage level rather than silently starting work.
- It recognizes there is no approved MKT-VISION / STRATEGY in mkt_docs, so an E2 campaign has no strategy context to sit on.
- It ESCALATES to E3 (or at minimum blocks and explains "tactics without strategy" is the failure mode), rather than producing a campaign plan blind.
- It does NOT invent a positioning or audience on the spot to justify proceeding as E2.
