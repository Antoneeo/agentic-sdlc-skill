---
feature: F-090
analysis: ANALYSIS_review_log_union_check.md
base: main
---
# Merge review: the review log's merge line, checked instead of announced

## Purpose
Serves the team-lead Actor — «one process, one source of truth»: a review log git would not
merge with union is named by `check`, with the exact line to add, instead of an instruction
in release notes nobody reads (REQUEST R1, R2).

## What to review
`sdlc_check.py review-map` against `main` (merge-base d0efe105). Totals: REVIEW 23 files
(+881/-30), DESIGN 2, EVIDENCE 3, GENERATED 3. Most of REVIEW is four identical copies:
- `skills/agentic-sdlc-skill/scripts/sdlc_core.py` (+3 copies): `_git_out(env=None)`,
  `_attr_pattern`, `review_log_union_note`, `print_check_notes`, `cmd_check` calls it.
- `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py`: one call.
- `skills/agentic-sdlc-skill/scripts/test_merge_safety.py` (+3 copies): `MS_UnionNote`.
- `test_golden_regression.py` (code, kb): git ceiling pinned.
- `shared_manifest.json` ×4: regenerated.
- `ENFORCEMENT.md` ×4, `templates.md` (code, kb, mkt), `coordination.md`: doctrine.

## Already verified
- Design review: REVIEW_LOG row 2026-11-01 «F-090 design», deep tier, FAIL → PASS in two
  rounds; owner chose the note in `check` only (R3) and approved the design (R4).
- Closure review: REVIEW_LOG row 2026-11-01 «F-090 closure», deep tier, PASS after a scoped
  re-review of six fixes (escaping of a leading space, `!`, backslash; a vacuous orient guard
  made able to fail; doctrine and E2E wording).
- Tests, worktree `claude/f090-union-check`, uncommitted on d0efe105, 2026-11-01: code 600 OK
  (skipped 4, after `index`), kb 913, mkt 588, course 611; `test_clients.js` 63/63 and the
  sibling client suites green. RED before implementation: 11 of 12 new tests failed.
- Probe: chatPNT prints the note with `ai_docs/audit/reviews/REVIEW_LOG.md merge=union`;
  this repository prints none.

## Your judgement
- Cost: two git calls (~90 ms) per `check` where a review log exists; one line while the
  attribute is missing; session start unchanged.
- Left to judgement on purpose: `.git/info/attributes` still counts (per clone) — stated in
  `ENFORCEMENT.md`; a deliberate non-union driver is respected.
- CANNOT VERIFY: the backslash and `*?` round trips run only on POSIX; no POSIX git here. One
  run of `MS_UnionNote` on Linux or macOS closes it. Such paths cannot exist on Windows.
- Decisions still owed: the merge; the 1.52.0 release, now for all four packages.

## Merge notes
- `main` is at the branch's base (`d0efe105`): fast-forward. The primary checkout holds the
  uncommitted 1.52.0 bump of the code package (`CHANGELOG.md`, `README.md`, `package.json`,
  `gemini-extension.json`, `SKILL.md` version, a REVIEW_LOG row): none of those files is
  touched by this branch except `REVIEW_LOG.md` — commit or set the bump's row aside before
  the merge.
- Generated files may conflict: regenerate with `index`.
- After the merge: `mark skills/agentic-sdlc-skill/`, `skills/`, `distributions/`; delete
  `audit/HANDOFF_review_log_union_check.md`; `index`.
- E2E script for testers after release: `E2E_TEST_review_log_union_check.md`.
