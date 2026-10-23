---
feature: F-080
analysis: ANALYSIS_spec_code_divergence.md
base: main
---
# Merge review: Spec/code divergence state shared by the two skills

## Purpose

A specification claim the code does not yet honor now says so, pointing at the
ANALYSIS that deferred the fix, and Topic Recall cites it as "required, not yet
done". It serves Vision v9's "nothing load-bearing lives only in a transcript" and
the Team lead's "one source of truth" (ANALYSIS §Feature Vision; admission
`vision/rulings.md` r33).

## What to review

Map computed against the branch base 6015848 (main has since moved; see Merge notes).

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +2/-0 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/memory.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/knowledge.py` | M | +108/-7 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_skill_invariants.py` | M | +16/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +2/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +2/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/distillation.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/memory.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/portability.md` | M | +1/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/reconciliation.md` | M | +2/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/knowledge.py` | M | +108/-7 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_claim_ledger.py` | M | +129/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_kb_recall.py` | M | +36/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_skill_invariants.py` | M | +16/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/memory.md` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/knowledge.py` | M | +108/-7 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_skill_invariants.py` | M | +16/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +1/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/memory.md` | M | +1/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/knowledge.py` | M | +108/-7 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +3/-3 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | M | +16/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/templates.md` | M | +2/-1 | REVIEW | review |
| `ai_docs/solutions/ANALYSIS_spec_code_divergence.md` | A | +362/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_spec_code_divergence.md` | A | +124/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +1/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +14/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_spec_code_divergence.md` | D | +0/-20 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_spec_code_divergence.md` | M | +38/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +2/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_spec_code_divergence/deltas.py` | A | +24/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_spec_code_divergence/probe.py` | A | +123/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/handoff.md` | M | +0/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +5/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 30 files (+694/-50); DESIGN 5 files (+502/-2); EVIDENCE 5 files (+187/-20); GENERATED 3 files (+6/-4)

## Already verified

- Design review: REVIEW_LOG 2026-10-23, `ANALYSIS_spec_code_divergence.md (F-080)`,
  design, deep tier, FAIL → FAIL → PASS in 3 rounds. It covered the ANALYSIS and the
  harness (`probe.py`, `deltas.py`).
- Closure review: REVIEW_LOG 2026-10-23, `F-080 diff e74a208..be8bf34 (+ fixes
  f276686)`, closure, deep tier, FAIL → PASS in 2 rounds. It covered every REVIEW
  and DESIGN file above, the E2E script and the r33 amendment, and checked D1–D8
  byte for byte against `deltas.py`.
- Batteries on f276686's tree: code 421 OK, kb 618 OK, mkt 423 OK, course 416 OK.
  Probe B1–B6 GREEN; `--baseline` A1/A2/A4 RED (the expected flip).
- Drift guard: `shared_files.py` reports the 29 shared files identical across the
  four packages.
- Owner decisions (REQUEST_spec_code_divergence.md): R3 ADMIT, R4 mandatory on
  deferral, R5 cost in principle, R6 removal on L2/L3 with L1 exempt, R7 Standalone
  now and Hybrid later, R8 «Accept 1,820 B».
- `sdlc_check.py check --root .`: CLEAN after `mark` (run in the closing commit).
- Not covered by any review: the generated files (`index` rewrites them).

## Your judgement

- Deviations from the approved design: two, both made after the design PASS and
  checked by the closure review. Probe B5 no longer lists the code `templates.md`,
  because the accepted D6 text never names the marker. FS5 now states that a bare
  `;` is tolerated beside the canonical `; `, which the code already accepted.
- Accepted residuals: an L1 fix may leave a stale marker that under-claims the code
  (R6). An agent could silence FS3 with a stub ANALYSIS citing the id; doctrine
  forbids it, and nothing checks it mechanically (T2). Hybrid projects get no marker
  yet (R7).
- CANNOT VERIFY: the agent's live answer over a marked claim (FS1, E2E S6). It rests
  on doctrine text, which is guarded by invariants.
- Declared assumptions: none.
- Decisions still owed: the merge; a later unit for Hybrid (R7); version numbers
  stay at the open `[Unreleased]` sections.

## Merge notes

- main moved after the branch point (F-076, 5857a57). Both sides touched the four
  CHANGELOGs, `rulings.md` (F-076 added r34, this branch r33: no id clash, keep both
  rows in id order), `architecture.md`, `REVIEW_LOG.md`, code `SKILL.md` and the four
  `shared_manifest.json`. Resolve the prose files by keeping both sides. Regenerate the
  manifests with `shared_files.py --update` and copy them to the three distributions;
  never resolve them by hand. Regenerate `handoff.md`, `memory/INDEX.md` and
  `features_history.md` with `index`.
- After the merge: re-run the four batteries, then `check`, and re-run `mark` on the
  merged commit if `stale` reports the areas.
- Hand `E2E_TEST_spec_code_divergence.md` to the tester.
