---
feature: F-098
analysis: ANALYSIS_team_definition.md
base: main
---
# Merge review: team definition (F-098)

## Purpose

Who works on a project with the skill knows from the start who is in the team, what each
one decides and does alone and how work and reports pass; the skill asks it once and
imposes no team shape (`ANALYSIS_team_definition.md` §Feature Vision, north star approved
in `REQUEST_team_definition.md` R4). It serves the project Vision's Goal "keep
understanding durable across sessions" and the team-lead Actor's "one process, one source
of truth". Two changes: at the first level-3 unit of a project the agent asks four team
questions and keeps the answer in a `## Team` section of the reading guide (doctrine,
four lenses, one shared file `team.md`); the session orientation says when a project that
opened a level-3 unit has no such section (shared core, one conditional line).

## What to review

Printed by `sdlc_check.py review-map --base main --root .` on the uncommitted working
tree (line counts as of that run; this brief is in it as it stood before the table
was pasted):

# Review map -- 77 files against main (merge-base 1fa19a67a5d1)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `README.md` | M | +3/-1 | REVIEW | review |
| `distributions/course-creator/README.md` | M | +2/-0 | REVIEW | review |
| `distributions/course-creator/package.json` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/ENFORCEMENT.md` | M | +2/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/SKILL.md` | M | +4/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/dispatch.md` | M | +4/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/evals/scenarios/team_asked_at_first_l3.md` | A | +17/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_check.py` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_core.py` | M | +72/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +6/-5 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_session_start.py` | M | +172/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_skill_invariants.py` | M | +78/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/team.md` | A | +92/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +2/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/package.json` | M | +1/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/ENFORCEMENT.md` | M | +2/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +3/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/dispatch.md` | M | +4/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/evals/scenarios/team_asked_at_first_l3.md` | A | +20/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_check.py` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_core.py` | M | +72/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +6/-5 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_session_start.py` | M | +172/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_skill_invariants.py` | M | +78/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/team.md` | A | +92/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` | M | +2/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/README.md` | M | +2/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/package.json` | M | +1/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/ENFORCEMENT.md` | M | +2/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` | M | +4/-2 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/dispatch.md` | M | +4/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/evals/scenarios/team_asked_at_first_e3.md` | A | +18/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/sdlc_core.py` | M | +72/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +6/-5 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_session_start.py` | M | +172/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_skill_invariants.py` | M | +78/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/team.md` | A | +92/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/templates.md` | M | +4/-0 | REVIEW | review |
| `package.json` | M | +1/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/ENFORCEMENT.md` | M | +2/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +3/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/coordination.md` | M | +8/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/dispatch.md` | M | +4/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/evals/scenarios/team_asked_at_first_l3.md` | A | +23/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/evals/scenarios/team_correction_lands_in_the_section.md` | A | +16/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/evals/scenarios/team_decides_who_is_asked.md` | A | +19/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/evals/scenarios/team_section_cannot_grant.md` | A | +17/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` | M | +1/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | M | +72/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +6/-5 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_session_start.py` | M | +172/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | M | +78/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/team.md` | A | +92/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/templates.md` | M | +2/-0 | REVIEW | review |
| `ai_docs/solutions/ANALYSIS_team_definition.md` | A | +609/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_team_definition.md` | A | +119/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/MERGE_REVIEW_team_definition.md` | A | +120/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +2/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +8/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +2/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_team_definition.md` | A | +27/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_team_definition.md` | A | +74/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +2/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_team_definition/DRAFT_team.md` | A | +101/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_team_definition/INVENTORY.md` | A | +91/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_team_definition/REPLAY.md` | A | +86/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_team_definition/RESULTS.md` | A | +155/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_team_definition/build_fixtures.py` | A | +311/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_team_definition/probe_orient_team.py` | A | +128/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +2/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +6/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 59 files (+1885/-36); DESIGN 6 files (+860/-2); EVIDENCE 9 files (+975/-0); GENERATED 3 files (+9/-4)

Where to look first:

- `skills/agentic-sdlc-skill/team.md` — the whole rule (its three copies are identical;
  `test_drift.py` proves it).
- `skills/agentic-sdlc-skill/scripts/sdlc_core.py` — `ORIENT_TEAM_LINE`,
  `has_team_section`, `team_not_defined`, and the one call in `cmd_orient`.
- `skills/agentic-sdlc-skill/scripts/test_session_start.py` (`TeamLineTests`) and
  `test_skill_invariants.py` (`F098_TeamDefinition`).
- The one paragraph added to each lens's `SKILL.md`, in that lens's vocabulary.
- `ai_docs/vision/rulings.md` rows r49 and r50.

## Already verified, by which gate

- **Design review** (REVIEW_LOG row of 2026-11-15, `ANALYSIS_team_definition.md`): FAIL,
  FAIL, PASS at the cap of three rounds. Then the owner's design approval (R5).
- **Closure review** (REVIEW_LOG row of 2026-11-15, F-098 closure): FAIL, FAIL, PASS at
  the cap. Round 1 re-ran the four full batteries and re-measured every cost figure;
  rounds 2 and 3 mutated the new code (each new call dropped turns a test red) and
  executed the edge cases of `has_team_section` and of the section's size claim.
- **Batteries**, on this tree after the last change to a skill file, 2026-11-15T08:46Z:
  `python -m unittest discover -s scripts -p "test_*.py"` — code 687 OK, knowledge 1000
  OK, marketing 703 OK, course 693 OK; `node scripts/test_clients.js` 76 pass.
- **Shared copies**: `test_drift.py` green in the four trees (inside the batteries).
- **Golden transcripts**: not in the diff; `test_golden_regression.py` green with no
  re-capture.
- **Probe**: `harness_team_definition/probe_orient_team.py` — P2 red on release 1.55.0
  plus F-096, P0, P0b and P1–P4 green on this tree.
- **`sdlc_check.py check --root .`**: CLEAN (validate rc=0, stale rc=0), 2026-11-15, with the three analysed areas marked by timestamp (uncommitted tree).
- **Owner decisions** (`audit/requests/REQUEST_team_definition.md`): R2 once per project;
  R3 the first occasion is the first level-3 unit; R4 the ruling on Non-Goal 1 (ADMIT,
  no Vision amendment), the north star, the success signal, the boundaries, four
  questions, the default, who changes the section; R5 design approved, the orientation
  line admitted on its exact text, the cost accepted without the sentence planned for
  `elicitation.md`, the wider reading of the default.

## Your judgement

- **Two decisions the owner still owes, both on the record as pending.**
  - *The measured cost.* `team.md` is 5,020 bytes; R5 accepted «Circa 3,5 KB letti una
    volta». Each `SKILL.md` grows by 498 to 818 bytes, under the «circa 900 byte per
    lens» R5 was shown. `coordination.md` +565 (read only under coordination).
  - *One divergent replay run.* In a project with no written agreement, the old text
    asked the owner a balanced choice in 3 runs of 3; the new text asked it in 2 of 3
    and settled it alone, by a weighing, in one. Three samples a side do not separate
    the two (`harness_team_definition/RESULTS.md`).
- **Deviations from the approved design**, all toward less text: no row added to the
  write-trigger tables (the paragraph states the trigger); the template sentence sits
  above the README block, not under it; `has_team_section` and threat T9 were added
  during the closure review (a section only quoted does not count).
- **Warnings left open** (closure round 3, the cap reached, so nothing was changed after
  it):
  - `has_team_section` opens a fence on a line that starts with inline triple-backtick
    code, so a real `## Team` right after such a line is not seen and the orientation
    says "not defined". Rare input; it fails toward asking, never toward granting.
  - The ANALYSIS says a 700-character section loses its last line under `--hybrid` in
    the probe's worst case; the round-3 reviewer measured it whole up to 736 characters.
    The shipped sentence in `team.md` makes no numeric promise.
  - Ruling r49 restates the cost figures the ANALYSIS owns (r47 does the same).
  - The ANALYSIS is 609 lines against a 500-line budget, and its Diary gives two figures
    for `team.md` at two moments.
- **What the replays show and do not** (`RESULTS.md`): red to green by text — the team
  questions at the first level-3 unit, and at an open unit taken up; with the agreement
  written, a choice it leaves to the member is decided and reported in one line. Not
  shown: that the three floors of `team.md` §What the section cannot change alter
  behaviour (the existing rules already stop a merge), and the owner's signal — fewer
  questions that are not theirs over a working day. One model tier, few samples, no
  transcripts kept.
- **Accepted residuals** (ANALYSIS T2, T5): a clone that carries the request record
  together with the section passes the citation check; a correction kept in an agent's
  own memory cannot be seen mechanically.
- **Not run**: the eval scenario for a correction (`team_correction_lands_in_the_section.md`)
  and the three sibling-lens scenarios; the four `init.js` end to end (the seed rule is
  checked statically).
- **Declared assumptions**: none.
- **Decisions still owed**: the two above; the commit and the merge (owner); the release —
  version numbers and the four CHANGELOG entries (`GUIDE_release.md`), not part of this
  unit.

## Merge notes

- Base is `main` at `1fa19a67` (F-096, F-097 and the coordination commit); this branch is
  a fast-forward of it plus an uncommitted working tree. No conflict is expected.
- The unit is a part under coordination (`REQUEST_honest_signals.md` R13,
  `audit/leases.md` in the `main` checkout) and holds the main-integration lease. Order:
  commit on this branch; `mark` `skills/agentic-sdlc-skill/`, `distributions/` and
  `skills/` so the reference is the commit hash; commit that; `check` CLEAN; send the
  coordinator the hash; the coordinator fast-forwards `main` on the owner's yes.
- Generated files (`audit/handoff.md`, `memory/INDEX.md`, `strategic/features_history.md`,
  `INDEX.md`): on any conflict, re-run `index`, never resolve by hand.
- Closing the unit on `main`: delete `audit/HANDOFF_team_definition.md`, set the ANALYSIS
  to COMPLETED with its end date, run `index`.
- This repository's own reading guide has no `## Team`: its next level-3 unit asks the
  owner, and until then the new orientation line is printed here.
- Testers: `solutions/E2E_TEST_team_definition.md`.
