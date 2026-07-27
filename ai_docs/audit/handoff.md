# Handoff — workstream registry
Date: 2026-07-27 (UTC)

| Workstream | Level | Branch | Status | Since | Next step | Details |
|---|---|---|---|---|---|---|
| F-015 Code-Comprehension Guides | L3 | main | PAUSED | 2026-07-19 | dogfood #8: write one real `source_kind: code` guide | ANALYSIS_comprehension_guides.md (Diary; no volatile state) |
| Release 1.17.0 | — | feat/parallel-handoff (tag v1.17.0) | AWAITING OWNER | merge to main + `npm publish` (2FA); verify `npm view` → 1.17.0 | CHANGELOG `[1.17.0]` |

## Project-wide notes
Repo is CRLF (edit as content-delta). devPNT off — Standalone. Standing Vision battery:
`audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md` (re-run on every Vision edit).
**npm is at 1.15.0**: v1.16.0 was tagged (`d5664c5`, parent of this branch) but never
published, so 1.17.0 supersedes it on npm with all its content included — publishing
1.16.0 separately is unnecessary. Both tags are pushed; `v1.16.0` stays as history.
