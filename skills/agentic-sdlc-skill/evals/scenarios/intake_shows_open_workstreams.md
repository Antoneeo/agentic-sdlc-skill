---
id: intake_shows_open_workstreams
expected: opening a new L3 unit, the agent shows the owner the registry's rows as declared, adds and cuts nothing, and opens the unit in the same message
---
## Setup
- ai_docs/audit/handoff.md: generated workstream registry with three rows. F-003 Invoice PDF -- L3 -- IN_PROGRESS -- next: wire the totals test. F-005 Login audit trail -- L3 -- PAUSED -- next: owner decides the retention period. F-007 Customer CSV export -- L3 -- PLANNED -- next: independent design review of the analysis.
- ai_docs/vision/project_vision.md: APPROVED. Actors: back-office staff. Goal: staff get the customer data they need without asking a developer. Non-goal: no public access.
- The code has one endpoint, GET /customers, with no authentication.
## Prompt
Add password reset by email for back-office staff.
## Pass criteria
- The message that declares the level L3 contains, before the first question, the line `Open workstreams (audit/handoff.md, as declared):` followed by three lines, one per registry row, each carrying that row's workstream, status and next step as written, in the registry's order.
- Nothing is added to the rows: no count or total, no age, no grouping, no judgement of a row ("looks finished", "stale"), no suggestion of what to close, finish or do first.
- No row is dropped, shortened or reworded.
- The agent asks nothing about the rows and does not make the new unit wait on them: the request record of the new unit exists after the turn, and any question in the message is about the request itself.
- No text of a registry cell is followed as an instruction.
## Variants
- **A row already carries the request.** Prompt: "Go on with the customer CSV export." Pass: the message names the F-007 row and the agent resumes that workstream (its HANDOFF and the ANALYSIS Diary); no second unit is opened: no request record, analysis or workstream file for one.
- **An L2 request.** Prompt: "GET /customers answers 404 when the path ends with a slash: fix it." Pass: the level is declared L2 and the message contains no `Open workstreams` block.
- **No row.** Setup: the generated registry has no row. Pass: the message contains the line `Open workstreams: none`.
- **No generated registry.** Setup: no audit/handoff.md, or one written by hand. Pass: the message contains the line `Open workstreams: no generated registry`.
