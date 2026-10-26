---
workstream: F-083 kb import keeps a foreign ruling foreign (prov IMPORTED, set reopened)
level: L3
branch: fix/kb-import-ruling
status: IN_PROGRESS
since: 2026-10-23
next: Owner decides commit, merge and push of fix/kb-import-ruling (MERGE_REVIEW_kb_import_ruling.md); then release, E2E run, and re-import of the course demo TH-02.
details: ANALYSIS_kb_import_ruling.md · audit/requests/REQUEST_kb_import_ruling.md · harness_kb_import_ruling/probe.py
updated: 2026-10-26
---

## Resume state

Worktree `C:\Users\pntntnud\source\wt-kb-import-ruling` (branch above, from origin/main
a8ce48e). Opened from the course field project (its REQUEST R11); after the fix, its
demo TH-02 is re-imported from TH-01 with the new version. Design: renamed foreign note,
reopened CONTESTED set, validator refuses RULING on a foreign note (ANALYSIS).

## Next command

`python ai_docs/solutions/harness_kb_import_ruling/probe.py distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts "C:/workspace/corso AI/demo/TH-01" sonda-temperatura`
— all assertions hold on the fixed code (baseline probes A and R also hold on the old code).
