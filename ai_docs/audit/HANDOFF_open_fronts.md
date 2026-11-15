---
workstream: F-097 Open fronts
level: L3
branch: claude/brave-dhawan-3f37ee (worktree .claude/worktrees/funny-chebyshev-e43e31, nothing committed)
status: IN_PROGRESS
since: 2026-11-14
next: The coordinator fast-forwards main to this branch; then close the unit on main (delete this file, ANALYSIS to COMPLETED, index).
details: ANALYSIS_open_fronts.md · audit/requests/REQUEST_open_fronts.md · harness_open_fronts/
updated: 2026-11-15
---
# HANDOFF: open fronts (ephemeral — deleted at closure)

## Resume state

Implemented and committed on this branch (owner's yes, REQUEST R7); not on `main` yet. The whole change is the working tree of
this worktree against `2f007f36` (F-096 on local `main`): `git status --short` lists it.
Evidence and state are in the ANALYSIS Diary; the tester's script is
`solutions/E2E_TEST_open_fronts.md`; the integrator's brief,
`solutions/MERGE_REVIEW_open_fronts.md`, is written after the closure review passes.
This unit is a part under coordination (`audit/leases.md` in the `main` checkout): the
commit and the merge are the owner's, given in this session.

To verify from cold: in each of the four `scripts/` directories run
`python -m unittest discover -s . -p "test_*.py"`; from the root run
`python ai_docs/solutions/harness_open_fronts/probe_uncarried_analysis.py
skills/agentic-sdlc-skill/scripts/sdlc_check.py .` and `sdlc_check.py check --root .`.
The marks of `skills/agentic-sdlc-skill/`, `distributions/` and `skills/` were taken on
an uncommitted tree, so they are timestamps: re-mark after the commit.
