---
feature: F-089
analysis: ANALYSIS_parallel_sessions_gaps.md
base: main
---
# Merge review: gaps in coordinating parallel sessions

## Purpose
Serves the Vision's team-lead Actor — «one process, one source of truth» — and the Goal
«keep understanding durable across sessions» (ANALYSIS §Feature Vision): documents-only
units in the checkout already in use without a branch each, one writer for every file
several sessions touch, one coordinator across compactions and chains (chatPNT M155
coordinator's points 2–4, REQUEST R2).

## What to review
`sdlc_check.py review-map` against `main` (merge-base c1ff546b), plus this file:

| Path | Class | What to do |
|---|---|---|
| `skills/agentic-sdlc-skill/coordination.md` | REVIEW | review: Who coordinates; §1 retitled + three bullets; §2 `coordinator` line and the shared checkout; §5 one sentence |
| `skills/agentic-sdlc-skill/SKILL.md` | REVIEW | review: Phase 4 «Isolate the work», one sentence |
| `skills/agentic-sdlc-skill/templates.md` | REVIEW | review: leases opening line, one Shared example |
| `ai_docs/vision/rulings.md` | DESIGN | read r42 and the note in r40's basis |
| `ai_docs/solutions/ANALYSIS_parallel_sessions_gaps.md`, `E2E_TEST_parallel_sessions_gaps.md`, `MERGE_REVIEW_parallel_sessions_gaps.md`, `ai_docs/strategic/skill_family_agent_workflows.md` | DESIGN | reference; read the changed parts |
| `ai_docs/audit/HANDOFF_parallel_sessions_gaps.md`, `requests/REQUEST_parallel_sessions_gaps.md`, `reviews/REVIEW_LOG.md`, `harness_parallel_sessions_gaps/*` | EVIDENCE | spot-check what this brief cites |
| `ai_docs/audit/handoff.md`, `ai_docs/memory/INDEX.md`, `ai_docs/strategic/features_history.md` | GENERATED | skip; regenerate with `index` |

Totals: REVIEW 3 files (+70/-11).

## Already verified
- Design review: REVIEW_LOG rows 2026-11-01 «F-089 design» rounds 1–4 (FAIL ×3 → PASS,
  deep tier, fresh subagent); round 4 beyond the cap at the owner's request (R5).
- Owner decisions: R4 (documents-only parts in the shared checkout, with constraints),
  R6 (design, r42 and cost approved).
- Doctrine replay: `results_old_text.md` (G1 forbidden; G3, G4, G6, G7 not flagged; G2, G5,
  G9 partly) → `results_new_text.md` (G1–G9 FLAGGED with the targeted route; G8 control
  unchanged).
- Closure review: REVIEW_LOG row 2026-11-01 «F-089 closure», deep tier, fresh reviewer,
  whole diff — PASS, 6 WARN + 1 NIT fixed, CV1 (condensed replay transcripts) accepted.
- Tests, worktree `claude/f089-coordination-gaps`, uncommitted on c1ff546b, 2026-11-01:
  code battery 588 OK (skipped 3); `node scripts/test_clients.js` 63/63. No code changed;
  sibling packages untouched.

## Your judgement
- Cost: `coordination.md` +4,138 B LF (+60%, estimate ~4 KB), read only under
  coordination; `SKILL.md` +103 B (estimate ~0; every session reads it); `rulings.md`
  +2,059 B (estimate ~1 KB).
- Left to judgement on purpose: the status of a `release` the previous coordinator wrote
  during a handover (goes to the owner); which units a binary `.devpnt/` store holds (the
  coordinator names them).
- CANNOT VERIFY: none open.
- Decisions still owed: the merge; the release (CHANGELOG at release, code package only).

## Merge notes
- `main` is at the branch's base (`c1ff546b`): the merge is a fast-forward once the branch
  is committed. The primary checkout holds one uncommitted edit of the 1.51.0 release
  (`ai_docs/audit/project_notes.md`, registry verified) — commit it before or with the merge.
- Generated files may conflict: regenerate with `index`, never resolve by hand.
- At closure: `mark skills/` (in the branch, before its commit); delete
  `audit/HANDOFF_parallel_sessions_gaps.md` and run `index`.
- For chatPNT (outside this repository): its `.gitattributes` lacks the review-log
  `merge=union` stanza — re-run `init` there.
- E2E script for testers after release: `E2E_TEST_parallel_sessions_gaps.md`.
