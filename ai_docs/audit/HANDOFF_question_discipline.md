---
workstream: F-026 revised — a real doubt is asked when it emerges (three lenses)
level: L3
branch: feat/ask-when-doubt-emerges
status: DONE, AWAITING MERGE
since: 2026-09-25
next: after the 1.35.0 release branch is merged into main, open a PR from feat/ask-when-doubt-emerges (it is based on codex/f057-shared-project-memory); then release it as a minor bump in all three packages
details: ANALYSIS_question_discipline.md · harness_question_discipline/probe.py
updated: 2026-09-25
---

## Resume logistics

- The branch is committed but not pushed. It was cut from `codex/f057-shared-project-memory`
  (release 1.35.0, not yet in main), so a PR opened before that merge would carry the
  release commits too.
- The CHANGELOG entries sit under `[Unreleased]` in all three packages. The version
  bump happens at release time (`GUIDE_release.md`).
- Open outside this repository: devPNT's generated reviewer definitions must carry the new
  `review.md` §Reviewing clause "An unasked doubt is a finding". That is devPNT-side work.
- Delete this file when the PR is merged, then run `sdlc_check.py index`.
