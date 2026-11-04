---
workstream: Release Codex hook parity
level: L3
branch: codex/f091-codex-hooks
status: IN_PROGRESS
since: 2026-11-04
next: Obtain concrete release-note approval and finish npm web login, then tag, integrate origin/main and publish the verified packages.
details: ANALYSIS_codex_hooks.md; MERGE_REVIEW_codex_hooks.md; harness_codex_hooks/release_notes.json
updated: 2026-11-04
---
# Release handoff: Codex hook parity

The code unit F-091 is COMPLETED: independent implementation/release reviews PASS,
121 Node tests, 611 Python tests (four skips), and packaging/consumer/native checks.
See its ANALYSIS Diary and release evidence; do not repeat broad reviews.

Prepared releases: code 1.53.0, KB 1.35.1, marketing 0.30.1, Course 0.1.0-beta.19.
All four targets are absent from npm; all target git tags are absent. Notes are
mirrored into each README and await the pending owner question before tagging.
Npm web login is running after E401; no tokens or trust-store contents are copied.

Primary source checkout has local design documents and unrelated docs-site.zip/npm;
preserve it. Clean integration worktree: chatPNT/.workdir/wt-f091-main-integration,
branch codex/f091-main-integration on origin/main 74c1833f. Feature commit 611ddb89
is pushed; release preparation is still uncommitted on codex/f091-codex-hooks.
Follow GUIDE_release: commit/tag/push exact inspected content; integrate/push main;
verify origin/main ancestry and all four remote tags; publish_all.bat from the clean
tagged content, with browser 2FA owned by the user; verify all npm versions/latest.
