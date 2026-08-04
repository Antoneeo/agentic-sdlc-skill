---
workstream: F-026 Question Discipline
level: L3
branch: claude/agitated-blackburn-62f5cf
status: DONE, AWAITING MERGE
since: 2026-08-01
next: the owner's merge call: rebase onto `feat/kb-knowledge-method`, or cherry-pick 50c5cf7+a0072cf onto main
details: ANALYSIS_question_discipline.md
updated: 2026-08-01
---

## Resume state

Worktree `romantic-pascal-8d15af`, cut from `feat/kb-knowledge-method`@ed1d65a.
Complete: legality test in `elicitation.md` reachable from Rule Zero, non-blocking
default with the same evidence duty as a question, blocking form generalized from
F-025. Two design-review rounds (6 findings, then 9 including 3 working evasions),
all fixed; three distributions green, drift guard identical, wiring invariant
mutation-tested.

## Watch out

The branch is 2 commits ahead of its base but `feat/kb-knowledge-method` has since
moved to 5e61170, so the two have diverged. Merging into the kb branch makes this
ride F-024's release hold. Afterwards: delete the worktree; kb adopts the section
inside F-024 and mkt owes it too.

