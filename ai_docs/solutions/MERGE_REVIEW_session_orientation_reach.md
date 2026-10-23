---
feature: F-075
analysis: ANALYSIS_session_orientation_reach.md
base: main
---
# Merge review: What reaches the session

## Purpose

The session-start orientation now reaches the agent on Claude Code. It used to
emit 16,435 characters here, with the guide router at character 8,366, beyond the
2,000-character preview the client injects above its 10,000-character hook cap.
Now it emits at most 9,500 characters, with the router and the registry first.
This serves the Vision Goal "operable by an agent that arrives with no context"
(ANALYSIS §Feature Vision). The per-turn line and `orient` also name the lens
choice when sibling lenses are installed.

## What to review

# Review map -- 67 files against main (merge-base ee7364927f8e)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +11/-0 | REVIEW | review |
| `README.md` | M | +2/-2 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +11/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/ENFORCEMENT.md` | M | +3/-3 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/routing.md` | M | +4/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/knowledge.py` | M | +42/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_core.py` | M | +267/-59 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +5/-5 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_session_start.py` | M | +262/-18 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_skill_invariants.py` | M | +6/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +11/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +2/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/ENFORCEMENT.md` | M | +3/-3 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/evals/scenarios/hook_orients_session.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/routing.md` | M | +4/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/fixtures/golden_baseline.txt` | M | +21/-70 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/knowledge.py` | M | +42/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_core.py` | M | +267/-59 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +5/-5 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_golden_regression.py` | M | +23/-3 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_remind.py` | M | +27/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_session_start.py` | M | +262/-18 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_skill_invariants.py` | M | +6/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +11/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/README.md` | M | +2/-2 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/ENFORCEMENT.md` | M | +3/-3 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/routing.md` | M | +4/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/knowledge.py` | M | +42/-2 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/sdlc_core.py` | M | +267/-59 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +5/-5 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_golden_regression.py` | M | +4/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_remind.py` | M | +27/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_session_start.py` | M | +262/-18 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_skill_invariants.py` | M | +6/-0 | REVIEW | review |
| `docs-site.zip` | A | bin | REVIEW | review |
| `npm` | A | +0/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/ENFORCEMENT.md` | M | +3/-3 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +1/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/evals/scenarios/hook_orients_session.md` | M | +1/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/routing.md` | M | +4/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/fixtures/golden_baseline.txt` | M | +21/-70 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/knowledge.py` | M | +42/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | M | +267/-59 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +5/-5 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_golden_regression.py` | M | +4/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_remind.py` | M | +27/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_session_start.py` | M | +262/-18 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | M | +6/-0 | REVIEW | review |
| `ai_docs/solutions/ANALYSIS_session_orientation_reach.md` | A | +396/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_session_orientation_reach.md` | A | +98/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +1/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +3/-2 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +2/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_docs_site_naming.md` | A | +20/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/HANDOFF_guide_check_section.md` | A | +21/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/HANDOFF_guide_verdict_check.md` | A | +22/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/HANDOFF_kb_intake_hygiene.md` | A | +22/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/HANDOFF_spec_code_divergence.md` | A | +20/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_guide_verdict_check.md` | A | +21/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_kb_intake_hygiene.md` | A | +27/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_session_orientation_reach.md` | A | +65/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_spec_code_divergence.md` | A | +21/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +3/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_session_orientation_reach/probe.py` | A | +45/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +6/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +5/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 48 files (+2563/-505); DESIGN 5 files (+500/-4); EVIDENCE 11 files (+287/-0); GENERATED 3 files (+12/-4)

`docs-site.zip` and `npm` are untracked files in the author's working tree, not on
the branch: skip them. The 15 shared files under `distributions/` are
byte-identical copies of the `skills/agentic-sdlc-skill/` ones (`test_drift.py`,
four identical `shared_manifest.json`). Review them once.

## Already verified

- Design review: REVIEW_LOG 2026-10-23, `ANALYSIS_session_orientation_reach.md
  (F-075)`, design, deep. Round 1 FAIL, round 2 PASS (scoped). It covered the
  ANALYSIS and the probe.
- Closure review: REVIEW_LOG 2026-10-23, `F-075 diff ee73649..41d5f61 (+ fixes
  3197264)`, closure, deep. FAIL → PASS in 2 rounds. It covered the code, the
  tests, the shared copies, the CHANGELOG ×4 sections, the READMEs, ENFORCEMENT
  ×4, `routing.md`, the E2E script and the rulings row. The WARN corrections
  folded after the design PASS were re-reviewed in the same closure.
- Batteries, run on the tree committed at 3197264 (`python -m unittest discover
  -s . -p "test_*.py"`, in each scripts folder): code 420 OK, kb 601 OK, mkt 422
  OK, course 415 OK.
- Probe `ai_docs/solutions/harness_session_orientation_reach/probe.py`: exit 0.
  Code entry 5,746 characters, kb entry 5,748. The first router row is at 522
  and 524, the registry heading at 1,055 and 1,057, and the lens choice is
  named. On the baseline it was red: 16,435 / 8,366 / 10,385.
- `check` CLEAN after `mark` and `index`, run on the closing commit (the next
  section names it).
- Owner decisions in `audit/requests/REQUEST_session_orientation_reach.md`:
  - R7: the remind cap rises to 600.
  - R8: the frozen 1.0 golden transcript no longer guards orient.
  - R9: the 89-character suffix is accepted.
  - The ledger row r32 records R7 and R9.
- Docs-root files no review covered: the registry and request records of the
  planned units F-076..F-080. They were carried onto this branch unchanged from
  the planning session.

## Your judgement

- Deviations from the approved design: none. The closure fixes changed only
  wording, tests and records.
- Accepted residual (W10): `orient` looks for siblings beside the running skill
  and in the user's Claude skills directory, while `routing.md` §0 names only the
  directory the skill was loaded from. This is approved design.
- CANNOT VERIFY:
  - Claude Code's 10,000-character cap and 2,000-character preview: these rest on
    the field report (R3) and on this session's own two "Output too large
    (16.2KB) … Preview (first 2KB)" blocks.
  - Whether the client de-duplicates identical hook commands: FS3 counts an
    identical command once, so the note is safe either way.
- Follow-up candidate, not acted on: the kb per-turn line carries no
  guide-router duty.
- Decisions still owed:
  - The merge decision on `feat/f075-orientation-reach`.
  - The release, after F-076 per `GUIDE_release.md`. The CHANGELOG sections are
    `[Unreleased - 1.48.0 / kb 1.31.0 / mkt 0.26.0 / course 0.1.0-beta.13]`;
    the versions are provisional.

## Merge notes

- Generated files (`audit/handoff.md`, `memory/INDEX.md`,
  `strategic/features_history.md`, `INDEX.md`) may conflict with main. Regenerate
  them with `sdlc_check.py index` and never resolve them by hand.
- `mark` recorded the branch commit. After a squash or rebase merge, re-run
  `mark` on main for `skills/agentic-sdlc-skill/`, `skills/` and `distributions/`.
- Hand `E2E_TEST_session_orientation_reach.md` to the tester after the merge.
