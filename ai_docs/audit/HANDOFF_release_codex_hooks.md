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
Npm whoami returned E401. Web login was opened but fell back to an interactive username prompt; cancelled without entering credentials. Start a fresh web login when the owner is ready; no tokens or trust-store contents are copied.

Primary source checkout has local design documents and unrelated docs-site.zip/npm;
preserve it. Clean integration worktree: chatPNT/.workdir/wt-f091-main-integration,
branch codex/f091-main-integration. Reviewed code/tests are integrated and pushed
to origin/main e2271dd7 (merge 185ca58b, acceptance d47ad107). Feature branch is
fast-forwarded to e2271dd7; version/notes preparation remains uncommitted there.
Follow GUIDE_release: commit/tag/push exact inspected content; integrate/push main;
verify origin/main ancestry and all four remote tags; publish_all.bat from the clean
tagged content, with browser 2FA owned by the user; verify all npm versions/latest.
