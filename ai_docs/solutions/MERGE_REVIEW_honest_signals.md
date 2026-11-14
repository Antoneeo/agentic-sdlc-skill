---
description: Merge review brief for F-096 - what the integrator reviews, what each gate already verified, and what only a person can judge.
status: CURRENT
feature: F-096
analysis: ANALYSIS_honest_signals.md
base: main
---
# Merge review: Honest signals (F-096)

## Purpose

Three field cases where the method was followed and the defect passed anyway. The change
makes each signal say what it measures: `check` states its coverage, a workstream file that
declares its work closed is named, and a session working from a summary is told what to
re-read (`ANALYSIS_honest_signals.md` §Feature Vision; Vision Goal "keep understanding
durable across sessions").

## What to review

# Review map -- 67 files against main (merge-base 1e7941e81a74)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `README.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/README.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/ENFORCEMENT.md` | M | +2/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/SKILL.md` | M | +4/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/guides.md` | M | +5/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_core.py` | M | +50/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +5/-5 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_merge_safety.py` | M | +99/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_session_start.py` | M | +72/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_skill_invariants.py` | M | +24/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/templates.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/ENFORCEMENT.md` | M | +2/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +2/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/guides.md` | M | +5/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/fixtures/golden_baseline.txt` | M | +3/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_core.py` | M | +50/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +5/-5 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_merge_safety.py` | M | +99/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_session_start.py` | M | +72/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_skill_invariants.py` | M | +24/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` | M | +5/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/README.md` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/ENFORCEMENT.md` | M | +2/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` | M | +2/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/guides.md` | M | +5/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/fixtures/golden_baseline.txt` | M | +2/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py` | M | +4/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/sdlc_core.py` | M | +50/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +5/-5 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_merge_safety.py` | M | +99/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_mkt_check.py` | M | +59/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_session_start.py` | M | +72/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_skill_invariants.py` | M | +24/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/templates.md` | M | +5/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/ENFORCEMENT.md` | M | +2/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +3/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/evals/scenarios/closure_rewrites_stale_state.md` | A | +20/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/evals/scenarios/resume_rereads_unit_vision.md` | A | +18/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/guides.md` | M | +5/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/fixtures/golden_baseline.txt` | M | +3/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | M | +50/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +5/-5 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_merge_safety.py` | M | +99/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_session_start.py` | M | +72/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | M | +24/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/templates.md` | M | +5/-0 | REVIEW | review |
| `ai_docs/audit/audit_plan.md` | M | +3/-3 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/project_notes.md` | M | +2/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_honest_signals.md` | A | +485/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_honest_signals.md` | A | +83/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/MERGE_REVIEW_honest_signals.md` | A | +173/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +1/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +10/-2 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +2/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/requests/REQUEST_honest_signals.md` | A | +106/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +2/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_honest_signals/REPORT_skills_field_feedback_2026-11-14.md` | A | +115/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_honest_signals/REPORT_skills_field_feedback_2026-11-14_rev2.md` | A | +136/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_honest_signals/case_compaction.md` | A | +97/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_honest_signals/case_guide_false.md` | A | +139/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_honest_signals/case_registry_40.md` | A | +880/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_honest_signals/probe_closed_handoffs.py` | A | +72/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_honest_signals/probe_signals.py` | A | +84/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +2/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +6/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 47 files (+1168/-32); DESIGN 8 files (+759/-6); EVIDENCE 9 files (+1631/-0); GENERATED 3 files (+9/-3)

The REVIEW files reduce to these, the rest being verified copies:

- `skills/agentic-sdlc-skill/scripts/sdlc_core.py` (+50/-1) — the whole code change. Its three
  copies under `distributions/` are byte-identical (`test_drift` in each tree).
- `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py` (+4/-1).
- Doctrine, read as prose: `SKILL.md` of the four lenses (2 to 4 lines each), `guides.md` §6
  (one bullet, identical in four), `templates.md` and `ENFORCEMENT.md` of the four lenses.
- The four READMEs: one sentence each.
- Tests: `test_merge_safety.py`, `test_session_start.py`, `test_skill_invariants.py` (shared,
  identical in four) and `test_mkt_check.py`.
- `golden_baseline.txt` in three trees: only added lines, the `[scope]` line after each
  `check` verdict and the resume line in `orient`.

## Already verified

- **Design review** — REVIEW_LOG 2026-11-14, `ANALYSIS_honest_signals.md (F-096 design)`,
  tier design, deep, fresh subagent: FAIL → PASS in 3 rounds. Covered the ANALYSIS against the
  Vision, the rulings ledger, the request record and the code.
- **Owner's design approval** — `REQUEST_honest_signals.md` R9.
- **Closure review** — REVIEW_LOG 2026-11-14, `diff feat/f096-honest-signals vs 1e7941e8`,
  tier closure, deep, fresh subagent: FAIL → PASS in 2 rounds. Covered the diff against the
  approved design, P1–P5, T1–T5, the doctrine in the four lenses, the two eval scenarios,
  `rulings.md` r45 and r46, `architecture.md`, `skill_family_agent_workflows.md`, the READMEs,
  the E2E script and the handoff. It did not cover this brief, written after it.
- **Tests, on the final working tree (uncommitted, base 1e7941e8), 2026-11-14T18:03Z** —
  `python -m unittest discover -s . -p "test_*.py"` in each lens's `scripts/`: code 642 OK
  (4 skipped), knowledge 955 OK (33 skipped), marketing 658 OK (29 skipped), course 648 OK
  (39 skipped). `node --test` on `scripts/test_md_region.js` 27, `test_release_remote.js` 7,
  `test_whats_new.js` 13, `test_clients.js` 76: all pass.
- **Probes on the recorded cases** — `harness_honest_signals/probe_closed_handoffs.py`: on
  release 1.55.0 nine sources declare a closed status and none is named; on this tree all
  nine are named once. `probe_signals.py`: red on 1.55.0, green on this tree. Re-run by the
  closure reviewer on a HEAD export and on the tree.
- **Owner decisions** — commit and merge into `main` (R12); closure re-read cost accepted (R3); finding on the named file, no cap
  (R4, ledger row r45); resume re-read cost accepted (R6); orientation line constant, printed
  always, no read of the hook event (R7, ledger row r46); all four lenses (R8).
- **Redaction** of the recorded cases, by the author: ANALYSIS Diary, closure-review entry.
  Not repeated by a reviewer.

## Your judgement

- **Deviations from the approved design:** one figure. The design said ten files are named
  on the recorded case; the probe shows nine — the tenth declares `DONE` and has no
  `workstream:`, so it is not a registry source. The ANALYSIS is corrected and says so.
- **The doctrine's effect is not demonstrated.** Six cold replays (one sample each, mid-tier
  model) passed with the new text and also with the old one for the whole re-read (FS1) and
  the vision read (FS6). Only the `re-read whole:` line and the request-record read differ.
  Whether the two rules change behaviour is left to the field signals S1 and S3.
- **CANNOT VERIFY:** whether a client re-runs the session-start hook after a compaction. It
  is documented for Claude Code, read second-hand. E2E scenario S3 is its only check; the
  line itself is printed at every start regardless.
- **Stated limit:** the advisory matches a status that *begins* with DONE, COMPLETED or
  CANCELLED. On the recorded case that is 9 files of 27 a person judged finished.
- **Accepted costs:** one closure duty at L2/L3 and one resume duty for units with an open
  workstream; 224 characters added to every session orientation.
- **Raised and not in this change** (`REQUEST_honest_signals.md` R10, R11): looking at the open
  workstreams before accepting new work; an analysis left in progress with no workstream file
  (F-022 in this repository); a written agreement on who decides what. Each needs its own
  ruling.
- **Decisions still owed:** the push, the release and its version numbers
  (`GUIDE_release.md`); CHANGELOG entries are not written.
- **Declared assumptions:** none.

## Merge notes

- Merged into `main` by fast-forward on the owner's word (`REQUEST_honest_signals.md` R12): two
  commits, the change and the re-mark of `skills/`, `skills/agentic-sdlc-skill/` and
  `distributions/` by commit hash. Not pushed, not released.
- The unit is closed in the same change: `ai_docs/audit/HANDOFF_honest_signals.md` deleted,
  the ANALYSIS COMPLETED.
- Before this change `check` was NOT CLEAN on `main` (`stale` after release 1.55.0); the
  re-mark clears it.
- Generated files (`ai_docs/audit/handoff.md`, `ai_docs/memory/INDEX.md`,
  `ai_docs/strategic/features_history.md`, `ai_docs/INDEX.md`) and `shared_manifest.json` in the
  four trees: on a later conflict regenerate (`index`; `shared_files.py --update`), never
  resolve by hand.
- Release: CHANGELOG entries and version numbers are not written (`GUIDE_release.md`).
- Hand `ai_docs/solutions/E2E_TEST_honest_signals.md` to the tester after the release; S3
  needs a real compaction on Claude Code.
