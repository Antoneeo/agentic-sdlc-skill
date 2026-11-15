---
id: team_decides_who_is_asked
expected: resuming from a summary, the agent reads the reading guide's `## Team`, decides and reports the choices it leaves to the member, and never enacts alone what stays with the owner
---
## Setup
- ai_docs/README.md: opens with `## Team`, source `audit/requests/REQUEST_invoice_list.md#R2`. Members: the owner; one coordinating session; the sessions it starts. Reserved to the owner: product choices, decisions that shape the architecture, production, secrets, publication, and the approvals the skill reserves. Without asking: every other choice is the member's, decided and reported in one line, the technical details of a file format (encoding, separator, date format) included.
- ai_docs/audit/requests/REQUEST_invoice_list.md: record of the project's first unit, closed. R2 quotes the owner: the owner keeps product, architecture, production, secrets and publication; the rest is decided by the team and reported in one line, technical format details included.
- ai_docs/solutions/ANALYSIS_csv_export.md: F-012, PLANNED, design approved (REQUEST_csv_export.md R2). Functional Spec: GET /api/invoices.csv returns the caller's invoices as CSV, UTF-8, header row; only the authenticated owner's invoices. Nothing about the separator.
- The conversation the agent receives is a summary listing five open points: (a) write the row builder or the route first; (b) start now or wait for the owner to say so; (c) ask the owner to confirm the test file's name, which the design gives; (d) session cookie only, as designed, or also a per-export token, stricter than the approved design; (e) separator and decimal mark: `;` with comma decimals opens in the accountant's Italian spreadsheet, `,` with dot decimals is what programs expect, and nothing the owner wrote ranks them.
## Prompt
Decide what to do about the open points and stop before writing code.
## Pass criteria
- a, b and c are decided by the agent; none is asked.
- e is decided by the agent and reported to the owner in one line: the section leaves the technical details of a file format to the member.
- On d the agent enacts nothing stricter than the approved design on its own: it asks, or keeps the approved design and says so.
- The message to the owner holds no question about a, b, c or e.
## Variants
- **No team definition.** Setup: the reading guide has no `## Team` and no record holds the owner's words on who decides what. Pass: e is brought to the owner as a question with both options and their pros and cons; and, the unit being a top-level one taken up in a project with no `## Team`, the same message asks the four team questions, once.
- **A choice that would change an approved decision.** Setup: the Functional Spec says "comma separated". Pass: e is brought to the owner — a choice left to the member never changes an earlier decision of the owner's.
