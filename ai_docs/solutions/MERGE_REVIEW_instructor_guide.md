---
feature: F-086
analysis: ANALYSIS_instructor_guide.md
base: main
---
# Merge review: guida del docente per i corsi con docente

## Purpose
Un corso con docente esce con `INSTRUCTOR_GUIDE.md` e con l'elenco verificato del materiale da consegnare. Serve il segnale della Vision «Un corso con docente si consegna con tutto il materiale che l'erogazione richiede e con le istruzioni per usarlo» (ANALYSIS §Feature Vision). Il controllo della versione nel testo serve il segnale sul feedback.

## What to review
Tabella stampata da `sdlc_check.py review-map --base main` prima di aggiungere questo brief e la riga di chiusura in REVIEW_LOG. Il numero di righe di REVIEW_LOG si riferisce a quel momento.

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `distributions/course-creator/CHANGELOG.md` | M | +4/-0 | REVIEW | review |
| `distributions/course-creator/README.md` | M | +2/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/SKILL.md` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/learning_design.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/course_check.py` | M | +130/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_instructor_guide.py` | A | +252/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/slide_content.md` | M | +2/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/templates.md` | M | +41/-1 | REVIEW | review |
| `ai_docs/audit/audit_plan.md` | M | +1/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/vision_history/VISION_course_creator_2026-09-27.md` | A | +62/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_instructor_guide.md` | A | +142/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_instructor_guide.md` | A | +58/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +1/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +8/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/features/VISION_course_creator.md` | M | +5/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_instructor_guide.md` | A | +17/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_instructor_guide.md` | A | +100/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +2/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_instructor_guide/probe.py` | A | +148/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +2/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +5/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 8 files (+433/-6); DESIGN 7 files (+277/-4); EVIDENCE 4 files (+267/-0); GENERATED 3 files (+8/-4)

## Already verified
- **Vision amendment.** REVIEW_LOG 2026-10-29, blind check of `VISION_course_creator.md`, gate lens: FAIL → PASS. Approved by the owner in REQUEST_instructor_guide.md#R7.
- **Design.** REVIEW_LOG 2026-10-29, `ANALYSIS_instructor_guide.md`, tier design: FAIL → PASS → PASS. It covered the ANALYSIS and the probe harness.
- **Closure.** REVIEW_LOG 2026-10-29, F-086 closure, tier closure: FAIL → PASS → PASS.
  - It covered every REVIEW and DESIGN file above, the E2E script included.
  - Its third round covered the one-sentence fix to E2E S2.
- **Test runs**, on the uncommitted tree after the last code edit, base 8bf09074:

  | Command | Result |
  |---|---|
  | `python -m unittest discover -s distributions/course-creator/skills/course-creator/scripts -p "test_*.py"` | Ran 574, OK (skipped=36) |
  | `python -m unittest discover -s skills/agentic-sdlc-skill/scripts -p "test_*.py"` | Ran 555, OK (skipped=3) |
  | `python ai_docs/solutions/harness_instructor_guide/probe.py` | 15 OK; on the baseline 10 RED |
  | `node scripts/test_clients.js`, `test_md_region.js`, `test_whats_new.js` | ok |
  | `validate`, from both entry points | rc=0 |

- **Owner decisions**, in REQUEST_instructor_guide.md:
  - #R4 and #R7: the Vision amendment;
  - #R5: the verified list of materials;
  - #R6: a fixture here, plus a replay by the owner;
  - #R8: the shape of the version rule.

## Your judgement
- **Deviations from the approved design:** none left. The closure fixes brought the code to the spec, and they aligned the text of rules 8 and 9 to the code.
- **Residuals accepted and declared** (ANALYSIS §Functional Spec and T2): the reviews see these, the checker does not.
  - material the delivery needs but the guide does not cite;
  - citations not written as `ai_docs/...`;
  - dates or names in free text;
  - a version mention with no course name on the line.
- **Low WARN refused:** a Materials row may be the whole course folder.
- **Could not verify:**
  - a symlink escaping the course folder, tested live: the test skips here because of the missing symlink privilege. It holds by reading the code.
  - the owner's replay on the real course (#R6, E2E S1–S2).
- **ERROR, not WARN, for a missing guide:** the author's decision, recorded in the Diary. Existing instructor-led courses fail `check` until they have the guide, and CHANGELOG and README say so.
- **Decisions still owed:**
  - the merge;
  - the release, which brings course-creator to the next beta and its «What's new».

## Merge notes
- **Generated files** (`handoff.md`, `memory/INDEX.md`, `features_history.md`): on conflict, regenerate them with `sdlc_check.py index`. Never resolve them by hand.
- **`stale`:** in this worktree, `check` reports areas this branch does not touch (`skills/`, `scripts/`) as stale. The cause is the file dates of the worktree, and the closure review confirmed it. After the merge into the main checkout, `check` should come back clean.
- **Before DONE:** the owner runs E2E S1–S2 on the real course and the result goes into the ANALYSIS Diary.
