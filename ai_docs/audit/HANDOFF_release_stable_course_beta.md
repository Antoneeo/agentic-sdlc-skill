---
workstream: F-062 Stable family release and course beta
level: L3
branch: main
status: IN_PROGRESS
since: 2026-10-02
next: Await owner decision on course latest alias after authenticated removal failed E400; review publisher guard and finish publication record.
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
content work remains open. Release commit 3e56773 and all four tags are on origin/main. npm accepted all four
packages and public tarballs match the publication hashes. Direct dist-tag reads
confirm stable targets but course also has latest. Browser authorization completed;
the authenticated DELETE of latest returned E400. Beta-only closure is not achieved.
Owner decision on this residual is pending. Do not repeat publication, unpublish,
or move release tags. Seven publisher isolation mock tests pass; independent guard review PASS.
