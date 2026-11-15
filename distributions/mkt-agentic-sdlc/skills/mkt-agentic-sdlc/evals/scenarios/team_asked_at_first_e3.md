---
id: team_asked_at_first_e3
expected: declaring the first E3 engagement of a marketing project whose reading guide has no `## Team`, the agent asks the client the four team questions once, with the default offered, and does not confuse the team with the people the plan gives work to
---
## Setup
- mkt_docs/README.md: mkt_docs reading guide. No `## Team` section. No vision or strategy documents yet.
- No file under mkt_docs/audit/requests/.
## Prompt
We are launching a B2B invoicing tool for freelancers in Italy in three months. I need the full marketing plan.
## Pass criteria
- The agent declares E3 and opens the engagement's request record.
- Its first question wave to the client contains the four team questions: who works on the plan with the agent; which decisions stay with the client; what each member decides without asking and to whom it reports; how work and reports pass.
- The default is offered so that one word accepts all four.
- The team questions are asked once, with the wave's other questions.
- The question about who will execute the marketing (founder, team, agency) is still asked as the plan's own input: it is content of the deliverable and is not folded into the team questions.
## Variants
- **The section exists.** Setup: mkt_docs/README.md opens with a `## Team` section. Pass: no team question is asked.
- **A project with an ai_docs root.** Setup: ai_docs/README.md opens with a `## Team` section; mkt_docs/README.md has none. Pass: no team question is asked, and no second section is written.
