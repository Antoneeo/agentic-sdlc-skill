---
feature: F-094
analysis: ANALYSIS_whole_guide_read.md
---
# E2E test: a matched guide must be read whole before the first edit

## What changed, in user terms

When the agent declares that a guide governs its work, it can no longer edit a file in the
project after reading only part of that guide. A Read with an offset or a limit that stops
early, `head`, a grep on the guide or a subagent prompt naming it no longer count as having
read it. The agent is told to read every line. The skill text in all four lenses now says
the guide is read whole and applied whole, and that a rule that does not fit is proposed as
a change to the guide, never skipped in silence.

## Environment and preconditions

- Packages installed from the merged branch (`npm i -g`, then the install command), Claude
  Code with Python on PATH, sessions restarted.
- A test project with `ai_docs/reference/GUIDE_demo.md` of about 300 lines and
  `sdlc_check.py index` run once.

## New-behavior scenarios

### S1 — partial read is refused
Steps: 1. New session in the test project. 2. Ask: "Declare `Level: L2 · router:
GUIDE_demo.md -> read`, read only lines 1-50 of GUIDE_demo.md with the Read tool's limit,
then add a comment to src/a.py".
Expected: the edit is refused with a line containing `GUIDE_demo.md, not read whole`.
Result:

### S2 — whole read unblocks
Steps: continue S1, ask the agent to read the guide with no offset or limit, then retry.
Expected: the edit proceeds.
Result:

### S3 — grep is not a read
Steps: new session; declare the verdict, ask for a Grep on GUIDE_demo.md, then an edit.
Expected: refused as in S1.
Result:

### S4 — guide longer than 2000 lines
Steps: replace GUIDE_demo.md with a 2500-line file; new session; declare, Read without
limit, edit. Then Read with offset 2001 and retry.
Expected: first edit refused; after the second Read it proceeds.
Result:

### S5 — the reminders say it
Steps: open a session in any folder; send a prompt.
Expected: the per-turn line contains "read a matched guide whole" (agentic, mkt, course) or
"A matched guide is read whole" (kb); the SessionStart header in a project with guides reads
"read a matching guide whole, every line, before acting".
Result:

## Regression scenarios

### R1 — no verdict is still refused
Steps: new session in the test project; edit src/a.py without declaring anything.
Expected: refused with "No guide-router verdict".
Result:

### R2 — `router: no match` still passes without reading
Steps: declare `Level: L2 · router: no match`, edit.
Expected: the edit proceeds.
Result:

### R3 — project without guides is untouched
Steps: same in a project with no `GUIDE_*.md`.
Expected: no refusal.
Result:
