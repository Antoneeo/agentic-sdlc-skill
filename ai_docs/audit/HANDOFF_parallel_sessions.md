---
workstream: F-088 Coordinating parallel sessions on one repository
level: L3
branch: claude/f088-parallel-sessions
status: IN_PROGRESS
since: 2026-10-31
next: Owner decides the merge; implementation, the R13 amendment, tests and closure review are done.
details: requests/REQUEST_parallel_sessions.md
updated: 2026-10-31
---

## Resume logistics

Worktree `.claude/worktrees/f088-parallel-sessions`, branch `claude/f088-parallel-sessions`
from `main` at `788e74ee`. `main` carries uncommitted changes of another session
(`SKILL.md`, `ENFORCEMENT.md`, `test_skill_invariants.py` in four copies): do not touch them.

Settled: order of work out (R5); resource holders in `audit/leases.md`, written by the
coordinator only (R3) — still needs its admission row in `vision/rulings.md`.

Pointers from the first session: F-073 (`ANALYSIS_doctrine_chronology.md` §Parallel work (c))
gives one worktree per session; it does not isolate container, test DB, decisions,
subagents. A commit-manifest check can reuse `_generated_set` and `classify_path` of
`review-map`. A new support file needs `support_files` in `sdlc_check.py`, `files` in
`package.json` and a `SKILL.md` reference (`test_support_files_wired`,
`test_every_support_file_on_disk_is_declared`).
