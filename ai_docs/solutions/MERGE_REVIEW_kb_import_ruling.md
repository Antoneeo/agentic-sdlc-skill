---
feature: F-083
analysis: ANALYSIS_kb_import_ruling.md
base: main
---
# Merge review: an imported ruling decides nothing until ratified

## Purpose

`import` now does what `portability.md` §4 promised since F-030. A `RULING` from
another project arrives as `IMPORTED`, on a renamed copy of its note that names its
origin. The rows it had superseded arrive `CONTESTED` with it, so it settles nothing
until the receiving owner ratifies it with a ruling of their own. Before the fix it
arrived unchanged as `RULING` with `check` clean: another owner's decision was binding
here (F-030 threat T1). `check` also refuses, in every lens, a `RULING` on a note that
names a foreign origin.

This serves the Vision Goal "never hide a conflict … let the user choose" (ANALYSIS
§Feature Vision). The owner ruled what the superseded rows become (REQUEST R3,
«Reopen the set»).

## What to review

Map computed against 1df13df (origin/main, v1.48.0). The changes are uncommitted in
worktree `wt-kb-import-ruling`, branch `fix/kb-import-ruling`.

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +5/-0 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +5/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/knowledge.py` | M | +388/-19 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +9/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/distillation.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/evals/scenarios/import_places_never_overwrites.md` | M | +2/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/portability.md` | M | +46/-16 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/reconciliation.md` | M | +12/-7 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/knowledge.py` | M | +388/-19 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_claim_ledger.py` | M | +602/-4 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +5/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/knowledge.py` | M | +388/-19 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +1/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/knowledge.py` | M | +388/-19 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +1/-1 | REVIEW | review |
| `ai_docs/solutions/ANALYSIS_kb_import_ruling.md` | A | +462/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_kb_import_ruling.md` | A | +106/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/MERGE_REVIEW_kb_import_ruling.md` | A | +26/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +7/-4 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_kb_import_ruling.md` | A | +22/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_kb_import_ruling.md` | A | +31/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +2/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_kb_import_ruling/probe.py` | A | +208/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +2/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +4/-2 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 18 files (+2244/-111); DESIGN 5 files (+602/-4); EVIDENCE 4 files (+263/-0); GENERATED 3 files (+7/-3)

The four `knowledge.py` copies are identical. Review one of them
(`skills/agentic-sdlc-skill/scripts/knowledge.py`: `kb_import_foreign_rulings`, its
helpers, `kb_import_plan`, `kb_cmd_import`, and the two `kb_check_claims` messages).

## Already verified

- **Design review.** REVIEW_LOG 2026-10-26, `ANALYSIS_kb_import_ruling.md (F-083)`,
  design, deep tier, FAIL → PASS → PASS in 3 rounds. Round 1 rejected the sidecar design
  and the note is renamed instead. It covered the ANALYSIS and the harness.
- **Closure review.** REVIEW_LOG 2026-10-26, F-083 working-tree diff against 1df13df,
  closure, deep tier, FAIL → PASS in 2 rounds. Round 1 found B1: a ruling note already
  held under its own name stopped the conversion. It was fixed with two tests that are
  red under the old code. The review covered every REVIEW and DESIGN file above.
- **Batteries** after the final edit: code 464, course 459, kb 754, mkt 466, all OK.
  - `TL_F083_ImportedRuling`: the 27 tests of round 1 were 26 red on 1df13df. The green one, the no-op
    re-import into the source, was already true. The 8 added at closure test the round-1 fixes.
  - Three mutation checks confirm the load-bearing conditions: the relabel refusal,
    the held-partner symmetry, and both halves of B1.
- **Replay on the real reproduction.** `harness_kb_import_ruling/probe.py` on
  `C:\workspace\corso AI\demo\TH-01`, topic `sonda-temperatura`, into an empty project:
  17/17 assertions hold, AC1 and AC2 included.
  - Note `imported_th-01_RULING_trasmissione-sonda_2026-09-20.md`, row `bb01396607f2`
    IMPORTED.
  - Set {5db6a37edb67, 8d7e02b88444, bb01396607f2} CONTESTED.
  - `check` CLEAN; relabelling is refused; ratification is CLEAN.
  - Baseline probes A and R also hold on the old code. The four after-fix assertions
    were red there.
- **Drift guard.** `shared_files.py`: 31 shared files identical. `shared_manifest.json`
  was regenerated ×4.
- **Owner decisions.** REQUEST R1 (fix in a separate session), R2 (the brief and its
  acceptance), R3 «Reopen the set».
- **`sdlc_check.py check --root .`.** validate rc=0. `stale` rc=1, the same as a
  clean 1df13df checkout (verified by the author and by the closure reviewer).
- **Not covered by any review:** the generated files (`index` rewrites them).

## Your judgement

- **Design choices made by weighing, not asked.** The owner's R2 asks for
  `imported_from:` "nella sua nota", and it is there, in a renamed copy.
  - The note is not edited in place. One inserted line re-points its line locator
    silently (probe A).
  - No sidecar is used. Five readers take it for a note, and a round trip broke the
    source's own ruling.
  - Cost: the IMPORTED row's id differs from the source project's.
  - The mixed-supersession case is refused rather than resolved (ANALYSIS, weighing
    in §Security).
- **Accepted residuals** (ANALYSIS threat table):
  - T1b: someone who deliberately edits the foreign note's frontmatter as well
    evades the relabel check.
  - T7: trees imported with kb ≤ 1.31.0 (the course demo TH-02 is one) are not
    repaired automatically. Re-import or convert by hand.
  - T8: the origin slug is the exporting folder's name.
  - The same-text self-check has no input that triggers it.
- **Admission.** No `vision/rulings.md` row is added. The unit restores behaviour the
  shipped doctrine already prescribed, under the 2026-08-03 owner ruling, and the new
  refusal enforces that same ruling. F-030 said its question would become a new row,
  and no such row exists. Decide whether one is owed (follow-up, not this unit).
- **CANNOT VERIFY:**
  - the E2E script's results: no tester run yet;
  - `docs_site.py` mapping `origin: imported` to "kb": unchanged code, unprobed.
- **Decisions still owed:**
  - the merge, plus commit and push (nothing is committed);
  - version numbers, which stay at the open `[Unreleased]` sections;
  - the release itself (`GUIDE_release.md`, owner's act).

## Merge notes

- Main has moved since 1df13df only if other units landed. In that case:
  - resolve the CHANGELOGs ×4, `architecture.md` and `REVIEW_LOG.md` by keeping both
    sides;
  - copy `knowledge.py` to the three distributions and regenerate the four
    `shared_manifest.json` with `shared_files.py --update`, never by hand;
  - regenerate `handoff.md`, `memory/INDEX.md` and `features_history.md` with
    `index`.
- Check that no other branch took F-083. F-082 is on `fix/codex-agents-skills`.
- After the merge:
  - re-run the four batteries and the harness, then `check`;
  - run `mark` on the merged commit for the changed areas;
  - delete `HANDOFF_kb_import_ruling.md`, set the ANALYSIS to `COMPLETED`, and run
    `index` again.
- Hand `E2E_TEST_kb_import_ruling.md` to the tester.
- For the course: once installed, re-import TH-02 from TH-01. Empty TH-02's earlier
  import first, because it predates the fix (T7).
