---
feature: F-086
analysis: ANALYSIS_instructor_guide.md
base: main
---
# Merge review: guida del docente per i corsi con docente

## Purpose
Un corso con docente esce con `INSTRUCTOR_GUIDE.md` e con l'elenco verificato del materiale da consegnare. Serve il segnale della Vision «Un corso con docente si consegna con tutto il materiale che l'erogazione richiede e con le istruzioni per usarlo» (ANALYSIS §Feature Vision). Il controllo della versione nel testo serve il segnale sul feedback.

## What to review
Tabella stampata da `sdlc_check.py review-map --base main` il 2026-10-30, dopo l'emendamento #R10 e prima della riga di questo brief in REVIEW_LOG.

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `distributions/course-creator/CHANGELOG.md` | M | +4/-0 | REVIEW | review |
| `distributions/course-creator/README.md` | M | +2/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/SKILL.md` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/learning_design.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/course_check.py` | M | +158/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_instructor_guide.py` | A | +321/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/slide_content.md` | M | +2/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/templates.md` | M | +59/-1 | REVIEW | review |
| `ai_docs/audit/audit_plan.md` | M | +1/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/vision_history/VISION_course_creator_2026-09-27.md` | A | +62/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_instructor_guide.md` | A | +148/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_instructor_guide.md` | A | +59/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/MERGE_REVIEW_instructor_guide.md` | A | +82/-0 | DESIGN | this brief |
| `ai_docs/strategic/architecture.md` | M | +1/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +8/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/features/VISION_course_creator.md` | M | +5/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_instructor_guide.md` | A | +17/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_instructor_guide.md` | A | +106/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +4/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_instructor_guide/e2e_report_2026-10-30.md` | A | +32/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_instructor_guide/probe.py` | A | +149/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +2/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +6/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 8 files (+548/-6); DESIGN 8 files (+366/-4); EVIDENCE 5 files (+308/-0); GENERATED 3 files (+9/-4)

## Already verified
- **Vision amendment.** REVIEW_LOG 2026-10-29, blind check of `VISION_course_creator.md`, gate lens: FAIL → PASS. Approved by the owner in REQUEST_instructor_guide.md#R7.
- **Design.** REVIEW_LOG 2026-10-29, `ANALYSIS_instructor_guide.md`, tier design: FAIL → PASS → PASS. It covered the ANALYSIS and the probe harness.
- **Closure.** REVIEW_LOG 2026-10-29, F-086 closure, tier closure: FAIL → PASS → PASS. It covered every REVIEW and DESIGN file, the E2E script included.
- **Owner replay on the real course** (#R6), 2026-10-30, report in `harness_instructor_guide/e2e_report_2026-10-30.md`:
  - S1 PASS on a copy of the course: the missing guide and «versione 1.0» in S38 were both flagged.
  - S2 PASS, but only after moving `demo/` inside the course folder. That move exposed findings 1–7.
- **Amendment #R10 and fixes 3–7.** REVIEW_LOG 2026-10-30, F-086 R10 amendment, tier closure: PASS with 3 WARN, all fixed test-first. One was the nested-repository walk following Windows junctions, now pruned and tested with a live junction.
- **Test runs**, on the uncommitted tree after the last code edit, base edb8d2d0:

  | Command | Result |
  |---|---|
  | `python -m unittest discover -s distributions/course-creator/skills/course-creator/scripts -p "test_*.py"` | Ran 580, OK (skipped=36) |
  | `python ai_docs/solutions/harness_instructor_guide/probe.py` | 15 OK |
  | `validate`, from both entry points | see the closing run in the Diary |

- **Owner decisions**, in REQUEST_instructor_guide.md:
  - #R4 and #R7: the Vision amendment;
  - #R5, amended by #R10: the verified list of materials, which may now point anywhere in the project;
  - #R6: a fixture here, plus a replay by the owner;
  - #R8: the shape of the version rule;
  - #R9: the side effect on project memory, which #R10 resolves.

## Your judgement
- **Deviation from #R5, chosen by the owner (#R10).** Materials are no longer confined to the course folder. The package is now the course folder plus the Materials list, and an `ai_docs/` path cited in the text must fall in one of the two. Option B, excluding nested repositories from the shared project memory, was rejected: it would change all four distributions and would not let the generated deck be listed.
- **Residuals accepted and declared** (ANALYSIS §Functional Spec and T2): the reviews see these, the checker does not.
  - material the delivery needs but the guide does not cite;
  - citations not written as `ai_docs/...`;
  - a deviation row whose Risk ID exists in P-TM but is not the right risk;
  - a Schedule whose total differs from the course duration;
  - dates or names in free text;
  - a version mention with no course name on the line.
- **Could not verify:**
  - a symlink escaping the project, tested live: the test skips here because of the missing symlink privilege. It holds by reading the code; the junction test does run.
- **Owner replay of S2 under #R10** (REQUEST_instructor_guide.md#R12), after the merge: PASS, `course: 0 error(s), 0 warning(s)`, `check: CLEAN`, no demo file in project memory.
- **ERROR, not WARN, for a missing guide or a guide off the template:** the author's decision, recorded in the Diary. Existing instructor-led courses fail `check` until they have a guide that follows the template, and CHANGELOG and README say so.
- **Decisions still owed:**
  - the merge;
  - the release, which brings course-creator to the next beta and its «What's new».

## Merge notes
- **Generated files** (`handoff.md`, `memory/INDEX.md`, `features_history.md`): on conflict, regenerate them with `sdlc_check.py index`. Never resolve them by hand.
- **`stale`:** in this worktree, `check` reports areas this branch does not touch (`skills/`, `scripts/`) as stale. The cause is the file dates of the worktree, and the 2026-10-29 closure review confirmed it. After the merge into the main checkout, `check` should come back clean.
- **Merged** to `main` on 2026-10-30 by fast-forward to 1a5db5d6 (#R11); the S2 replay closed the unit (#R12).
