---
feature: F-076
analysis: ANALYSIS_guide_verdict_check.md
base: main
---
# Merge review: Guide verdict check before edits

## Purpose

On Claude Code, an agent's file edit in a project with guides is now refused until the
session shows the Rule-Zero level with the guide-router verdict (or `Level: L1`) and the
agent has read every guide that verdict names. A field agent had edited without doing
either and said nothing stopped it (REQUEST R1). This serves the anti-myopia North Star
and the Goal "operable by an agent that arrives with no context" (ANALYSIS §Feature
Vision). The installer wires the check machine-wide; uninstall also removes the per-turn
`remind` entry, which used to be left pointing at a deleted file.

## What to review

# Review map -- 40 files against main (merge-base 6015848cb250)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +4/-0 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/ENFORCEMENT.md` | M | +12/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_core.py` | M | +156/-5 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +3/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_verdict.py` | A | +240/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/ENFORCEMENT.md` | M | +12/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_core.py` | M | +156/-5 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +3/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_verdict.py` | A | +240/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/ENFORCEMENT.md` | M | +12/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/sdlc_core.py` | M | +156/-5 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +3/-2 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_verdict.py` | A | +240/-0 | REVIEW | review |
| `scripts/lib.js` | M | +109/-46 | REVIEW | review |
| `scripts/postinstall.js` | M | +11/-1 | REVIEW | review |
| `scripts/preuninstall.js` | M | +17/-1 | REVIEW | review |
| `scripts/test_clients.js` | M | +91/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/ENFORCEMENT.md` | M | +51/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +1/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | M | +156/-5 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +3/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_verdict.py` | A | +240/-0 | REVIEW | review |
| `ai_docs/solutions/ANALYSIS_guide_verdict_check.md` | A | +353/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_guide_verdict_check.md` | A | +83/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +2/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_guide_verdict_check.md` | D | +0/-22 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_guide_verdict_check.md` | M | +20/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +3/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_guide_verdict_check/probe.py` | A | +113/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +0/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +4/-2 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 29 files (+1923/-77); DESIGN 4 files (+439/-1); EVIDENCE 4 files (+136/-22); GENERATED 3 files (+5/-3)

Where to look first: `sdlc_core.py` (`transcript_facts`, `verdict_reason`, `cmd_verdict`,
the ambiguous-root branch in `main`), `scripts/lib.js` (the remind wiring and the orient
removal now go through `wireCommandHookInto` / `removeGlobalHookEntries`), the wired
command's `; exit 0`, and r34 in `vision/rulings.md`. The three distribution copies of
`sdlc_core.py`, `test_verdict.py` and `shared_files.py` are identical to the code copy
(`shared_files.py --check`).

## Already verified

- Design review: REVIEW_LOG 2026-10-23, `ANALYSIS_guide_verdict_check.md (F-076)`,
  design, deep. Round 1 FAIL (B1: a missing or older validator exits 2 and would block
  every edit), round 2 PASS (scoped).
- Closure review: REVIEW_LOG 2026-10-23, `F-076 diff 6015848..010737a (+ fixes a63dbfe)`,
  closure, deep. PASS → PASS in two rounds. It covered the code, tests, shared copies,
  installer, CHANGELOG ×4, ENFORCEMENT ×4, SKILL.md, rulings, architecture, the probe and
  the E2E script. The reviewer re-ran every battery and the probe itself.
- Batteries after the last code change (a63dbfe), `python -m unittest discover -s . -p
  "test_*.py"` in each scripts folder: code 449 OK, course 444 OK, kb 630 OK, mkt 451 OK;
  `node scripts/test_clients.js` 58 pass, 0 fail.
- Probe `ai_docs/solutions/harness_guide_verdict_check/probe.py`: 10/10 green — the field
  case refused (red before), compliant and L1 cases silent, `gate` unchanged, the wired
  form exits 0 in Git Bash and PowerShell while the bare form fails (2 / 1), and P6 on the
  author's real session transcript not refused.
- `check` CLEAN after `index` and `mark`, on the closing commit.
- Owner decisions in `audit/requests/REQUEST_guide_verdict_check.md`: R3 block, R4 accept
  the per-edit cost and wire by default. The ledger row r34 records both.

## Your judgement

- Deviations from the approved design: one addition — a subagent's own transcript
  (`isSidechain`) is also silent, besides `agent_id` (closure CV1, probed). Recorded in
  the ANALYSIS Interface Contract and ENFORCEMENT §3.
- Accepted residuals: Bash-made writes are not checked; a verdict anywhere earlier in the
  session counts; a subagent edit the client does not mark is judged on the orchestrator's
  verdict; a transcript mixing a sidechain entry into the main one would silence the check
  (none among 355 local transcripts).
- CANNOT VERIFY: whether Claude Code puts `agent_id` in a subagent's PreToolUse input
  (documented, not probed — covered by the sidechain path); whether npm 7+ runs
  `preuninstall` (covered by `; exit 0`); whether a refusal applies in bypass-permissions
  mode.
- **R1's quotation** ("Nothing stops me from acting when I haven't declared a verdict…")
  is not in the excerpt REQUEST_session_orientation_reach.md R3 records; R5 notes it.
  Confirm or correct its source.
- Decisions still owed: the merge of `claude/f076-guide-verdict-check-eaaba8`; the release
  of F-075 + F-076 per `GUIDE_release.md` (CHANGELOG sections stay `[Unreleased]`, versions
  provisional).

## Merge notes

- Generated files (`audit/handoff.md`, `memory/INDEX.md`, `strategic/features_history.md`,
  `INDEX.md`) may conflict with main or the parallel F-077..F-080 branches. Regenerate them
  with `sdlc_check.py index`; never resolve them by hand.
- `vision/rulings.md`: F-080's branch adds r33, this branch r34 — keep both rows.
- `sdlc_core.py` (×4): parallel branches may touch the subparser block in `main`; keep
  every subcommand, then copy the file to the distributions and run
  `shared_files.py --update` ×4.
- `mark` recorded the branch commit. After a squash or rebase merge, re-run `mark` on
  main for `skills/`, `scripts/` and `distributions/`.
- Hand `E2E_TEST_guide_verdict_check.md` to the tester after the merge.
