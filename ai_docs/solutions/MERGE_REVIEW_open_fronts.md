---
feature: F-097
analysis: ANALYSIS_open_fronts.md
base: main
---
# Merge review: open fronts (F-097)

## Purpose

The owner decides what to open knowing what is open, and the registry can be trusted to
list what declares itself in progress (`ANALYSIS_open_fronts.md` §Feature Vision): the
project Vision's Goal "keep understanding durable across sessions" and the team-lead
Actor's "one source of truth". Two changes: the registry's rows shown, as declared, when
a new level-3 unit opens (four lenses); a validator advisory naming an analysis in
progress that no workstream file names (shared core). Plus F-022 set to COMPLETED.

## What to review

Printed by `sdlc_check.py review-map --base main --root .` on the uncommitted working
tree (line counts as of that run; this brief itself is not in it):

# Review map -- 46 files against main (merge-base 2f007f363bdf)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `README.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/README.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/SKILL.md` | M | +2/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_core.py` | M | +47/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_merge_safety.py` | M | +181/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_skill_invariants.py` | M | +61/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +1/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_core.py` | M | +47/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_merge_safety.py` | M | +181/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_skill_invariants.py` | M | +61/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` | M | +4/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/README.md` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` | M | +1/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/sdlc_core.py` | M | +47/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_merge_safety.py` | M | +181/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_skill_invariants.py` | M | +61/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/templates.md` | M | +4/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +2/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/evals/scenarios/intake_shows_open_workstreams.md` | A | +21/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | M | +47/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_merge_safety.py` | M | +181/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | M | +61/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/templates.md` | M | +4/-0 | REVIEW | review |
| `ai_docs/audit/audit_plan.md` | M | +3/-3 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_multi_domain_core.md` | M | +11/-2 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_open_fronts.md` | A | +635/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_open_fronts.md` | A | +103/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +1/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +8/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +2/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_open_fronts.md` | A | +28/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_open_fronts.md` | A | +64/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +2/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_open_fronts/build_intake_fixture.py` | A | +137/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_open_fronts/judge_rows.py` | A | +56/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_open_fronts/measure_rows.py` | A | +37/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_open_fronts/probe_uncarried_analysis.py` | A | +185/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_open_fronts/replay_intake.md` | A | +58/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +2/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +6/-4 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +2/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 28 files (+1211/-17); DESIGN 7 files (+763/-7); EVIDENCE 8 files (+567/-0); GENERATED 3 files (+10/-6)

Reading help: the three `distributions/*/scripts/` copies of `sdlc_core.py`,
`test_merge_safety.py` and `test_skill_invariants.py` are byte-identical to the code
lens's (`test_drift.py`); review them once, in `skills/agentic-sdlc-skill/scripts/`.

## Already verified

- **Design review** — REVIEW_LOG row 2026-11-14, `ANALYSIS_open_fronts.md (F-097)`,
  tier design, FAIL → FAIL → PASS, 3 rounds. Covered: the ANALYSIS, the request record,
  the harness.
- **Closure review** — REVIEW_LOG row 2026-11-15, `F-097 open fronts: working tree vs
  2f007f36`, tier closure, FAIL → FAIL → PASS, 3 rounds. Covered: the whole diff — core,
  tests, doctrine in the four lenses, templates, READMEs, rulings rows r47 and r48,
  `skill_family_agent_workflows.md`, `architecture.md`, the E2E script, the unit's
  HANDOFF, `ANALYSIS_multi_domain_core.md`.
- **Docs-root files no review covered**: this brief, the closure row of REVIEW_LOG and
  the last Diary entry of the ANALYSIS (written after the final PASS); the generated
  indexes are proved by `check`.
- **Tests, on the uncommitted working tree over `2f007f36`, 2026-11-15, after the last
  edit of any Python or doctrine file** (run by the round-3 closure reviewer):
  `python -m unittest discover -s . -p "test_*.py"` in each `scripts/` — code 666 OK,
  knowledge 979 OK, marketing 682 OK, course 672 OK; `node --test` — root 76 / 27 / 7 /
  13 pass, kb 52, mkt 52, course 4 pass of 5 with none failing.
- **Golden transcripts**: not in the diff; `test_golden_regression.py` green with no
  re-capture (inside the batteries above).
- **Probe**: `probe_uncarried_analysis.py` — red on release 1.55.0 and on F-096's tree
  (2026-11-14), green on this tree.
- **`sdlc_check.py check --root .`**: CLEAN (validate rc=0, stale rc=0), 2026-11-15, with
  the three analysed areas marked by timestamp (uncommitted tree).
- **Owner decisions** (`audit/requests/REQUEST_open_fronts.md`): R2 the form admitted for
  the rows (verbatim, no summary); R3 F-022 is COMPLETED; R4 design approved, costs
  accepted, the advisory admitted; R5 the course lens shows the rows with its limit
  declared; R6 the measured doctrine size accepted.

## Your judgement

- **Deviations from the approved design**: the doctrine sentence grew during the closure
  review (when each one-line form applies; Spike and reclassification in the course
  lens); the owner accepted the measured size (R6). The four READMEs gained one clause
  each, which the Impact allowed "where they state what `validate` reports". No other.
- **Warnings left open** (closure round 3, the cap reached): `README.md` and the kb, mkt
  and course READMEs summarize the advisory without "in a project that generates its
  registry".
- **Accepted residuals** (ANALYSIS T3, T4, T7): the advisory does not report `PLANNED`
  analyses, course-domain analyses, Hybrid units whose design is in devPNT, or an
  analysis a source's frontmatter names without carrying; the block is the agent's
  transcription of the registry, not a command's output; a forty-row registry costs
  about 13,000 characters per level-3 opening.
- **CANNOT VERIFY**: the doctrine replays (0 of 2 on release 1.55.0; 2 of 2 on the
  candidate, plus the resume and L2 variants) kept no transcripts, and were run on the
  sentence before the closure review's wording corrections; the final wording is held by
  text invariants only. Two samples, one model tier, one recorded case.
- **Declared assumptions**: none.
- **One act on the record to judge**: R4 and R5 were in the request record twice (a
  transcription script run twice); the second, byte-identical copies were removed from
  the never-committed file instead of being voided by a new entry.
- **Not changed, on purpose**: the marketing `templates.md` sentence on `IN_PROGRESS`
  does not say it holds on an `ai_docs` root only (the byte figures accepted in R6 would
  have moved).
- **Decisions still owed**: the commit and the merge (owner); the release — version
  numbers and the four CHANGELOG entries (`GUIDE_release.md`), not part of this unit.

## Merge notes

- Base is `main` at `2f007f36` (F-096); this branch is a fast-forward of it plus an
  uncommitted working tree. No conflict is expected.
- The unit is a part under coordination (`REQUEST_honest_signals.md` R13,
  `audit/leases.md` in the `main` checkout). Order: commit on this branch; `mark`
  `skills/agentic-sdlc-skill/`, `distributions/` and `skills/` so the reference is the
  commit hash; commit that; `check` CLEAN; then the coordinator fast-forwards `main`.
- Generated files (`audit/handoff.md`, `memory/INDEX.md`, `strategic/features_history.md`,
  `INDEX.md`): on any conflict, re-run `index`, never resolve by hand.
- F-098 (`.claude/worktrees/intelligent-roentgen-4c68ce`) restarts from this unit's
  commit; its rulings rows start at r49.
- Closing the unit on `main`: delete `audit/HANDOFF_open_fronts.md`, set the ANALYSIS to
  COMPLETED with its end date, run `index`.
- Testers: `solutions/E2E_TEST_open_fronts.md`.
