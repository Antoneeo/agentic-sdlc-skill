---
workstream: F-039 KB Recall Reflex (second-brain unit 1)
level: L3
branch: feat/kb-recall-reflex
status: DONE, AWAITING MERGE
since: 2026-08-27
next: the owner's merge call; release rides the next kb minor (units 2-3 of the vision may share it)
details: ANALYSIS_kb_recall_reflex.md
updated: 2026-08-28
---

## Resume state

Branch `feat/kb-recall-reflex` off `main`@45ad7c3 (VISION_kb_second_brain APPROVED).
Design review: FAIL(12) -> FAIL(1, latent) -> PASS at round 3, zero open findings,
rung 1 granted at the gate via the F-038 five-bullet ask. Implemented per the
reviewed design: SKILL.md §Topic Recall + taxonomy §6 + orient intercept (overlay
special-case, spine untouched) + test_kb_recall.py (kb-only, 7 tests, mutation
bites) + run_behavioral fenced seeding (with common-dedent, smoke-tested) + eval
scenario + README capability point 6 + CHANGELOG [Unreleased]. kb battery 281 OK.

## Watch out

- `test_kb_recall.py` is DELIBERATELY outside the shared x3 manifest (round-2
  review finding): kb-only doctrine, kb-only vehicle. Do not "tidy" it into
  test_skill_invariants.py.
- The orient intercept must never enter the overlay argparse: raw argv forward
  (the --help pattern), or the flag-mirroring drift class returns.
- Units 2 (capture moment) and 3 (time cycle) of the vision remain; unit 3
  explicitly waits for usage data from units 1-2.
