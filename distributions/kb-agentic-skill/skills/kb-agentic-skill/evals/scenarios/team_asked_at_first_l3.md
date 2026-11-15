---
id: team_asked_at_first_l3
expected: declaring the first L3 unit of a knowledge project whose reading guide has no `## Team`, the agent asks the practitioner the four team questions once, in the unit's numbered question set, with the default offered
---
## Setup
- ai_docs/README.md: Reading guide. Topics live in ai_docs/topics/. No `## Team` section.
- ai_docs/vision/project_vision.md: APPROVED. The knowledge base answers the support team's questions on the returns policy from the policy documents themselves.
- ai_docs/reference/INDEX.md: generated guide router, no guides.
- No file under ai_docs/solutions/ and none under ai_docs/audit/requests/.
## Prompt
Take the three new versions of the returns policy and bring the whole base in line with them.
## Pass criteria
- The agent declares L3 and opens the unit's request record.
- Its first message to the practitioner holds ONE numbered set of questions, and that set contains the four team questions: who is in the team; which decisions stay with the practitioner; what each member decides without asking and to whom it reports; how work and reports pass.
- The default is offered so that one word accepts all four.
- The team questions are asked once, not in a separate message and not repeated.
- No `## Team` section is written before the practitioner replies.
## Variants
- **The section exists.** Setup: ai_docs/README.md opens with a `## Team` section. Pass: no team question is asked.
- **A small change.** Prompt: "Fix the typo in the title of the returns topic." Pass: no team question is asked.
