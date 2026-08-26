---
workstream: F-038 Gated-Rung Vocabulary
level: L3
branch: feat/gated-rung-vocabulary
status: DONE
since: 2026-08-25
next: nothing outstanding -- published and verified 2026-08-26 (1.28.0 / 1.6.0 / 0.6.0)
details: ANALYSIS_gated_rung_vocabulary.md
updated: 2026-08-26

---

## Resume state

Branch `feat/gated-rung-vocabulary` off `main`@dda8d3a. Successor to F-037 (CANCELLED
at the cap). Design went to the cap too — FAIL x3 but CONVERGING, and round 3's own
judgement was "fix BLOCK 1 + BLOCK 2 and this is implementable"; both folded, owner
chose implementation at the cap.

Implemented: the gated-rung block + reason words in `review.md` x3; `templates.md` x3
schema comment + example row; `dispatch.md` x3 degradation clause; invariant x3
(RED->GREEN, mutation bites); eval scenario spine+kb (mkt excluded — different gate);
README / kb+mkt SKILL.md / strategic doc wording; rulings r18+r19; F-035 row annotated.

## Watch out

- The retired forms: the one-time grep cleared every carrier, and the invariant now
  guards the ladder both ways (positive vocabulary anchors AND a negative assertion on
  the retired reason string). `templates.md` is per-lens (outside the drift guard), so
  the invariant's vocabulary check is the only x3 guard there.
- The devPNT doctrine's own copy of the ladder (outside this repo) now lags — known
  divergence, named in the ANALYSIS blast radius.
- Post-cap folds were unreviewed by design review (cap rule); the closure review on the
  diff is where they get independent eyes.
