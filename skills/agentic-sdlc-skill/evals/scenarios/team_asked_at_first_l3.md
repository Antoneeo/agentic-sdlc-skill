---
id: team_asked_at_first_l3
expected: declaring the first L3 unit of a project whose reading guide has no `## Team`, the agent asks the four team questions once, in the unit's numbered question set, with the default offered
---
## Setup
- ai_docs/README.md: Reading guide. Must-reads: the guide router, the project vision, the architecture. No `## Team` section.
- ai_docs/vision/project_vision.md: APPROVED. A small invoicing service a freelancer runs for their own clients. Actor: the freelancer. Goal: invoices can leave the service in a format an accountant accepts. Non-goal: no payment collection.
- ai_docs/reference/INDEX.md: generated guide router, no guides.
- app/api.py: one route, GET /api/invoices, behind a login decorator. app/invoices.py: list_invoices(owner_id).
- No file under ai_docs/solutions/ and none under ai_docs/audit/requests/.
## Prompt
I want to export the invoice list as CSV for my accountant, through a new endpoint.
## Pass criteria
- The agent declares L3 and opens the unit's request record.
- Its first message to the owner holds ONE numbered set of questions, and that set contains the four team questions: who is in the team; which decisions stay with the owner; what each member decides without asking and to whom it reports; how work and reports pass.
- The default is offered so that one word accepts all four: one agent and the owner, the owner keeping what they uniquely own and the reserved approvals, the agent deciding the rest and reporting it in one line.
- The team questions are asked once: not in a separate message before or after the unit's own questions, and not repeated.
- No `## Team` section is written before the owner replies.
## Variants
- **The section exists.** Setup: ai_docs/README.md opens with a `## Team` section citing an earlier unit's request record. Pass: no team question is asked.
- **An L2 request.** Prompt: "GET /api/invoices answers 500 on an empty list: fix it." Pass: the level is declared L2 and no team question is asked, although the reading guide has no `## Team`.
- **The owner answers only the unit's questions.** Second turn: the owner answers the questions about the export and ignores the four. Pass: the agent writes `## Team` with the default and `default, not confirmed` and the date as its source, and does not ask again.
- **An open unit taken up.** Setup: an ANALYSIS in progress and its request record exist, no `## Team`. Prompt: "Go on with the CSV export." Pass: before going on, the agent asks the four team questions with the default, once.
