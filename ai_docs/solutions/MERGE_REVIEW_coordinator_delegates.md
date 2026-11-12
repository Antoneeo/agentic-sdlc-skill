---
feature: F-095
analysis: ANALYSIS_coordinator_delegates.md
base: main
---
# Merge review: the coordinator does not do a part's work

## Purpose

The named coordinator cleaned the skill repository and integrated F-094 itself, outside the
skill (REQUEST_coordinator_delegates.md R1). `coordination.md` now says what the coordinator
does not execute: every unit, cleanup included, goes to a part; the part that made a branch
integrates it in its own worktree; the coordinator's one git write in the shared checkout is
an `--ff-only` fast-forward at the part's request; removing any branch or worktree needs
your yes in the session that removes it.

## What only a human can judge

1. The friction: "integrate it and push" said to the coordinator now becomes a hop to the
   part, which asks you again for the push in its own session. Is that the cost you want?
2. This unit itself was done by the coordinator, on your explicit order (R2) — which the new
   rule allows ("for that unit it is a part").
3. No design-approval entry before the doctrine was written: the rule was drafted in the same
   pass as the analysis. Approving the merge approves the design.

## What was verified, by which gate

- `test_coordinator_delegates_units_and_parts_integrate`: fails by assertion on the old
  `coordination.md`, passes on the new one.
- Cold replay of the field case (`harness_coordinator_delegates/replay.md`, pinned by
  sha256): old text 3 SILENT + 1 PERMITTED, new text 4 FORBIDDEN.
- Full batteries in the four distributions OK; drift guard identical; `sdlc_check.py check`.
- Independent review: round 1 FAIL (1 BLOCK, 8 WARN), round 2 FAIL (1 BLOCK, 4 WARN),
  round 3 PASS with 3 WARN fixed after the cap (test + pinned replay, not re-reviewed — read those three sentences yourself); row in REVIEW_LOG.

## Not done

No CHANGELOG/What's new, no version bump, no tag, no push, no publish. The F-094 HANDOFF on
main still says "decide whether to merge" though F-094 is merged: its closure belongs to the
F-094 part, under this very rule.

## What to review

`coordination.md` §Trigger and roles (two new paragraphs) and the §2 coordinator bullet;
the eval scenario; the new test. Everything else is records.
