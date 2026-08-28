---
workstream: F-040 KB Capture Moment (second-brain unit 2)
level: L3
branch: feat/kb-capture-moment
status: DONE, AWAITING MERGE
since: 2026-08-28
next: the owner's merge call (closure FAIL->FAIL->PASS at round 3, zero open findings)
details: ANALYSIS_kb_capture_moment.md
updated: 2026-08-28
---

## Resume state

Branch `feat/kb-capture-moment` off `main`@43dbea1. Design review FAIL(10) -> PASS in 2
rounds; the lead BLOCK was vision-level (the draft had silently reinterpreted the
mandated sweep ask) and went to the owner, who ruled to honor the vision's wording.
Implemented: SKILL.md §The Capture Moment + Write Triggers sweep row; notes-recency
line in kb_cmd_orient (date: frontmatter first, mtime fallback, limits named);
test_kb_capture.py (8 tests, mutation bites); two eval scenarios (positive + negative
branch); README point 7; CHANGELOG F-040 entry. Battery 289 OK.

## Watch out

- The sweep is a SCHEDULED elicitation (phase-3 round's family), not a blocking
  question — the R2 WARN's classification, anchored in the battery. Do not attach the
  five-part blocking form to it.
- The recency line trusts `date:` frontmatter over mtime BY DESIGN (clone/worktree
  reset mtimes); do not "simplify" to mtime-only.
- Unit 3 (the time cycle) waits for usage data from units 1-2 per the vision.
