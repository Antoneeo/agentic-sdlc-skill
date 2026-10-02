---
workstream: F-062 Stable family release and course beta
level: L3
branch: main
status: IN_PROGRESS
since: 2026-10-02
next: Finish independent release reviews, close audit references, commit and tag, publish stable lenses and course beta from the exact release commit.
details: ANALYSIS_release_stable_course_beta.md
updated: 2026-10-02
---
# Release resume

Antonio authorized commit and publication on 2026-10-02 and explicitly requested
GUIDE_release.md. Target versions: code 1.37.0, KB 1.20.0, marketing 0.15.0;
course 0.1.0-beta.1 on beta, never latest. Current registry stable versions were
verified 1.36.0, 1.19.0, 0.14.0; course returned E404.

Work stays on main. Exclude presentations and their local dependencies from the
release commit; publish a clean git archive export so unrelated local work survives.
Do not infer human learning efficacy from simulator or validator results. C-001
content work remains open. No publication or commit has occurred yet.
