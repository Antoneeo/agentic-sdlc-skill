---
workstream: F-062 Stable family release and course beta
level: L3
branch: codex/release-1.38.0
status: IN_PROGRESS
since: 2026-10-02
next: Commit and tag after final gates, push main, publish the exact tagged export, then set Course latest to beta.2 and verify registry hashes/channels.
details: ANALYSIS_release_stable_course_beta.md; harness_release_stable_beta/release_2026-10-08.md
updated: 2026-10-08
---
# Release resume

Antonio requested execution of GUIDE_release.md on 2026-10-08, authorizing
commit, tags, push and publication. Targets: code 1.38.0, KB 1.21.0,
marketing 0.16.0 on latest, course 0.1.0-beta.2 on beta.

The release branch starts at origin/main 9970e66. It adds version metadata
and release notes for F-065 and the shared LF-hash/check-verdict fixes.
Existing F-065 closure review passed; its README scope WARN remains recorded.
Four fresh Python suites and four package/init/scratch checks pass.
Evidence and commands: solutions/harness_release_stable_beta/release_2026-10-08.md.

npm web authentication completed on 2026-10-08; whoami confirms antoneeo.
Independent release review PASS; the packed-file-count WARN was corrected.
The 2026-10-02 release remains published at 1.37.0 / 1.20.0 / 0.15.0 /
0.1.0-beta.1. Course latest still points to beta.1 after the registry rejected
its removal with E400. The owner now requires default installation to receive the newest Course:
publish beta.2 on beta, then explicitly set latest to beta.2 and verify both.
Do not remove latest or unpublish; the guide records this superseding ruling. Verify exact public tarball hashes and channels.
C-001 course content remains open; do not include presentation work.
