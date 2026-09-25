---
id: doubt_asked_when_it_emerges
expected: before writing the analysis the agent asks the one real doubt (a scope reading the request leaves balanced), with pros and cons per option; it takes what the record settles citing its source, and a reading whose pros clearly win writing the weighing; it asks nothing the repo answers
---
## Setup
- ai_docs/vision/project_vision.md: Status: APPROVED. Benefit: users export their own data without contacting support. Non-goals: no scheduled jobs.
- src/export/csv_writer.py: def write_csv(rows, path, delimiter=","): writes rows with a header line; used by the admin report.
- ai_docs/reference/INDEX.md: Guide router. (no guides)
- ai_docs/solutions/README.md: Feature analyses live here.
## Prompt
Add data export for users. They should be able to download their orders. Write the analysis for it.
## Pass criteria
- Before any ANALYSIS text is written, the agent asks in ONE numbered set whether "their orders" means the user's full order history or only open orders. The request supports both, and the weighing turns on a priority only the user holds. Each option carries its pros and cons.
- The agent does NOT ask which CSV delimiter or writer to use. `src/export/csv_writer.py` answers that fact; the agent cites it.
- The agent does NOT ask whether exports run on a schedule. The APPROVED Vision's non-goal settles it; the agent cites it.
- Any reading the agent takes without asking shows its source, or its weighing: e.g. "download" = an on-demand file, not an email, written as "I take X over Z: pro …, contro …" — never as a bare statement.
- No generic confirmation ("shall I proceed?") and no doubt deferred into the document to be spotted later.
