---
feature: F-088
analysis: ANALYSIS_parallel_sessions.md
base: main
---
# Merge review: coordinating parallel sessions on one repository

## Purpose
Serves the Vision's team-lead Actor — «one process, one source of truth» — and the Goal
«keep understanding durable across sessions» (ANALYSIS §Feature Vision): several sessions on
one repository, one coordinating, without a record numbered by three writers, a delegate
overriding an owner decision, or a commit nobody can split by unit (chatPNT M155 cases).

## What to review
# Review map -- 42 files against main (merge-base 788e74ee664e)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `README.md` | M | +3/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/elicitation.md` | M | +3/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/review.md` | M | +3/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_chronology.py` | M | +12/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/templates.md` | M | +8/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/elicitation.md` | M | +3/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/review.md` | M | +3/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_chronology.py` | M | +12/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` | M | +8/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/elicitation.md` | M | +3/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/review.md` | M | +3/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_chronology.py` | M | +12/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/templates.md` | M | +8/-0 | REVIEW | review |
| `package.json` | M | +1/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +3/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/coordination.md` | A | +139/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/elicitation.md` | M | +3/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/review.md` | M | +3/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` | M | +119/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +2/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_chronology.py` | M | +12/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_review_map.py` | M | +174/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/templates.md` | M | +45/-0 | REVIEW | review |
| `ai_docs/solutions/ANALYSIS_parallel_sessions.md` | A | +396/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_parallel_sessions.md` | A | +103/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/MERGE_REVIEW_parallel_sessions.md` | A | +107/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +13/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +2/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_parallel_sessions.md` | A | +26/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_parallel_sessions.md` | A | +81/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +6/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_parallel_sessions/cases.md` | A | +70/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_parallel_sessions/replay.md` | A | +18/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_parallel_sessions/results_new_text.md` | A | +48/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_parallel_sessions/results_old_text.md` | A | +29/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +2/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +6/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 26 files (+588/-22); DESIGN 6 files (+622/-0); EVIDENCE 7 files (+278/-0); GENERATED 3 files (+9/-4)

## Already verified
- Design review: REVIEW_LOG rows 2026-10-31 «F-088 design» rounds 1–4 and «round 5»
  (rounds 5–7, FAIL → PASS, nothing open), deep tier, whole ANALYSIS.
- Closure review: REVIEW_LOG row 2026-10-31 «F-088 closure», deep tier, fresh reviewer, on
  the whole uncommitted diff — conformance file by file, FS1–FS9, T1–T5, P1–P5; it re-ran
  the code battery itself. Rounds 3–4 of the same row reviewed the owner's amendment (R13)
  in design and code: PASS, nothing open.
- Tests, worktree `claude/f088-parallel-sessions`, uncommitted on 788e74ee, 2026-10-31:
  code 569 OK (skipped 3); kb 883 OK; mkt 558 OK; course 581 OK; `node
  scripts/test_clients.js` 63/63. RED before implementation: the 13 `commit-map` tests
  failed; the labelled-heading test passed (P1 pinned). Amendment: the Regenerated test
  failed before its check existed, then `test_review_map` + `test_chronology` 65 OK; code
  battery and `test_clients.js` re-run after it (code 570 OK, skipped 3, 2026-10-31T13:09Z; clients 63/63). The amendment touched only
  code-lens files, so the kb, mkt and course runs above stand.
- Doctrine replay: `harness_parallel_sessions/results_old_text.md` (C1–C3, C5, C6, C8 NOT
  FLAGGED; C7 a violation) → `results_new_text.md` (every case FLAGGED; C5–C7 replayed again
  on the amended text, §Amendment).
- Owner decisions: `REQUEST_parallel_sessions.md` R5 (order of work out), R7 and R9
  (labelled entries, every lens), R8 (owner names the coordinator), R3 (leases file),
  R12 (design and cost approved), R13 (the replay residuals and W3 taken into the unit). Rulings r40, r41 written in `vision/rulings.md`.

## Your judgement
- Deviations from the approved design: the owner's amendment R13 (FS3, FS3b, FS7, FS9),
  reviewed in design and code. Measured cost against the estimates: the labelled-entries
  paragraph is +627 B per sibling lens (estimate ~0.3 KB); the amendment +992 B in
  `coordination.md` (priced ~0.5 KB); total doctrine +12,509 B LF (ANALYSIS Diary).
- Left to judgement on purpose: how the coordinator reads a silent part's tree, and
  whether to resume it (the owner's, Non-Goal 1); no remedy beyond the owner's yes for
  code a departed code-writer left (C7). WARNs open: none.
- CANNOT VERIFY: none open; the cost figures are shown to the owner with this brief.
- Decisions still owed: the merge; the release (CHANGELOG ×4 written at release, per the
  Impact).

## Merge notes
- Generated files (`audit/handoff.md`, `INDEX.md`, `memory/INDEX.md`,
  `strategic/features_history.md`) may conflict with `main`: regenerate with `index`, never
  resolve by hand.
- `main` carries uncommitted changes of another session (`SKILL.md`, `ENFORCEMENT.md`,
  `test_skill_invariants.py` ×4); merge only after those are committed or set aside by
  their owner.
- After the merge commit: `sdlc_check.py mark skills/` and `mark distributions/` (the
  doctrine changed; README and the family doc are refreshed), committed as a new commit.
- At closure: delete `audit/HANDOFF_parallel_sessions.md` and run `index`.
- E2E script for testers after release: `E2E_TEST_parallel_sessions.md`.
