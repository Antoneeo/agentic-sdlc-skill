---
workstream: F-075 What reaches the session (orient under the hook cap, lens choice)
level: L3
branch: feat/f075-orientation-reach
status: IN_PROGRESS
since: 2026-10-22
next: TDD implementation per ANALYSIS_session_orientation_reach.md (design PASS round 2), then closure.
details: ANALYSIS_session_orientation_reach.md · audit/requests/REQUEST_session_orientation_reach.md
updated: 2026-10-23
---

## Resume state

First of the six units planned from the 2026-10-22 field report (REQUEST R5); release
after F-075 and F-076. Scope: `orient` output under Claude Code's 10,000-character hook
cap, with the triage line, the guide router and the handoff registry first and README /
INDEX as pointers; a notice when `orient` is wired twice; a "choose the lens with
routing.md" line when sibling lenses are installed; the constant per-turn reminder names
the lens choice; worked hybrid examples in routing.md section 2. Probe: replay this
session's start, router outside the 2,000-character preview today, inside after.

## Next command

RED tests in test_session_start.py / test_remind.py, then the sdlc_core.py changes.
