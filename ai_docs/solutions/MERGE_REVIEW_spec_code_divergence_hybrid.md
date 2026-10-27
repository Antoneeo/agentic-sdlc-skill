---
feature: F-081
analysis: ANALYSIS_spec_code_divergence_hybrid.md
base: main
---
# Merge review: Spec/code divergence marker in Hybrid projects

## Purpose

F-080's `not-yet-honored-by` claim marker now works in projects that use devPNT: it
may name `SHADOW_<doc_key>`, and `check` reads the newest shadow of that governed
design and requires the claim id in it. This closes the scope the owner deferred in
F-080 ("Standalone now, Hybrid later") and serves Vision v9's "nothing load-bearing
lives only in a transcript" for the Adopter who adds devPNT (ANALYSIS §Feature
Vision; admission `vision/rulings.md` r36).

## What to review

Map computed against main at 807c755 (the merge-base; main is merged into the branch).

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/memory.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/knowledge.py` | M | +41/-14 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_core.py` | M | +35/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +4/-4 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_skill_invariants.py` | M | +5/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +2/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/distillation.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/memory.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/reconciliation.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/knowledge.py` | M | +41/-14 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_core.py` | M | +35/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +4/-4 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_claim_ledger.py` | M | +153/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_kb_recall.py` | M | +4/-5 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_skill_invariants.py` | M | +5/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +1/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/memory.md` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/knowledge.py` | M | +41/-14 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/sdlc_core.py` | M | +35/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +4/-4 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_skill_invariants.py` | M | +5/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +1/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/memory.md` | M | +1/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/knowledge.py` | M | +41/-14 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | M | +35/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +4/-4 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | M | +5/-2 | REVIEW | review |
| `ai_docs/solutions/ANALYSIS_spec_code_divergence_hybrid.md` | A | +329/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_spec_code_divergence_hybrid.md` | A | +119/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/MERGE_REVIEW_spec_code_divergence_hybrid.md` | A | +74/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +1/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +9/-7 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +2/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/requests/REQUEST_spec_code_divergence_hybrid.md` | A | +50/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +3/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_spec_code_divergence_hybrid/deltas.py` | A | +36/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_spec_code_divergence_hybrid/probe.py` | A | +132/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/memory/INDEX.md` | M | +6/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 32 files (+512/-96); DESIGN 6 files (+534/-9); EVIDENCE 4 files (+221/-0); GENERATED 2 files (+7/-3)

## Already verified

- Design review: REVIEW_LOG 2026-10-23, `ANALYSIS_spec_code_divergence_hybrid.md
  (F-081)`, design, deep tier, PASS (8 WARN) → PASS in 2 rounds. It covered the
  ANALYSIS and the harness (`probe.py`, `deltas.py`).
- Closure review: REVIEW_LOG 2026-10-23, `F-081 diff 19bdaac..ee6cf89 (+ fixes
  155c1b2)`, closure, deep tier, PASS → PASS in 2 rounds. It covered every REVIEW and
  DESIGN file above, the E2E script and the r36 row, and compared D1–D6 byte for byte
  with `deltas.py` (D5 in all four `memory.md` copies).
- Batteries on the merged tree (f1889c6): code 464 OK, kb 719 OK, mkt 466 OK, course
  459 OK. Probe B1–B7 GREEN; `--baseline` A1/A3 RED, A2 GREEN (the expected flip).
- Drift guard: `shared_files.py` reports the 31 shared files identical across the four
  packages.
- Owner decisions (REQUEST_spec_code_divergence_hybrid.md): R2 «ADMIT as r35», R3
  unversioned `SHADOW_<doc_key>` target, R4 shadow required (error if absent), R5 cost
  in principle, R6 «Accept 201 B».
- `sdlc_check.py check --root .`: CLEAN after `mark` (run in the closing commit).
- Not covered by any review: the main merge (f1889c6) beyond the batteries, and the
  generated files (`index` rewrites them).

## Your judgement

- Deviations from the approved design, all made after the design PASS and checked by
  the closure review: the `hybrid.md` line priced in R5 is dropped (its duty rides in
  the code Write Triggers row; R6 accepted that); the marker message now fires for any
  part whose predicate is `not-yet-honored-by`, so a versioned target is told to drop
  the version; stray detection lives in `sdlc_core.stray_shadow` beside
  `newest_shadow`.
- The ruling id: the owner admitted "r35"; F-077 had taken r35a–c on main, so the
  row is r36, with the owner's words quoted verbatim and the renumbering noted in it.
- Accepted residuals: `check` reads the newest *exported* shadow, never the devPNT DB,
  so a stale shadow passes until refreshed (T6); any doc_key's shadow satisfies
  `check`, the E-ISP/E-TDD restriction is doctrinal (T7, FS8); a hand-made higher
  version could decide the check (T4); a stub shadow citing the id silences FS3 (T2,
  as in F-080).
- CANNOT VERIFY: the agent's live answer naming a `SHADOW_` target (FS7, E2E S6),
  resting on doctrine guarded by invariants; the symlink-escape branch of T1 on a
  Windows host.
- Declared assumptions: devPNT doc_keys use letters, digits, `_` and `-` (observed on
  about 50 local shadow names, none with a dot).
- Decisions still owed: the merge; version numbers stay at the open `[Unreleased]`
  sections.

## Merge notes

- The branch already contains main up to 807c755 (merge commit f1889c6). If main
  moves again, resolve the CHANGELOGs, `rulings.md`, `architecture.md` and
  `REVIEW_LOG.md` by keeping both sides; regenerate the four `shared_manifest.json`
  with `shared_files.py --update` and copy them to the three distributions, never by
  hand; regenerate `handoff.md`, `memory/INDEX.md` and `features_history.md` with
  `index`. Check that no other branch took r36.
- After the merge: re-run the four batteries, then `check`, and re-run `mark` on the
  merged commit if `stale` reports the areas.
- Hand `E2E_TEST_spec_code_divergence_hybrid.md` to the tester.
