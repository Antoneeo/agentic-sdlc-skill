---
workstream: F-076 Guide verdict check before edits
level: L3
branch: main
status: PLANNED
since: 2026-10-22
next: Starts after F-075; elicitation first, with two owner decisions (warn or block; per-edit ceremony cost).
details: audit/requests/REQUEST_guide_verdict_check.md
updated: 2026-10-22
---

## Resume state

A `PreToolUse` hook on Edit/Write that reads `transcript_path` and checks a router
verdict was declared and the guides it names were read. Known risk: the transcript is
written asynchronously and may lag the current turn. Owner decisions pending: warn or
block; acceptance of the per-edit cost under the "no ceremony ratchet" Non-Goal (as r19).
Probe: replay the other session's case, unflagged today, flagged after.

## Next command

After F-075 closes: elicitation round, then ANALYSIS_guide_verdict_check.md.
