---
feature: F-071
analysis: ANALYSIS_intent_focus.md
---
# E2E test: Intent focus

## What changed, in user terms
An agent following the skill now treats what the owner asked for as something its
review must weigh, and probes a "better/faster" benefit before code. It no longer
runs a review on a level-2 change outside security areas, nor on the part of a
release delta that only restates reviewed work; it logs a `NOT DUE` row instead, and
`sdlc_check.py benefit` counts those rows apart.

## Environment and preconditions
The installed packages at the released versions (code lens 1.44.0, kb 1.27.0, mkt 0.22.0,
course 0.1.0-beta.9); any project with an `ai_docs/` tree and a REVIEW_LOG.

## New-behavior scenarios
### S1 — FS1: the owner's outcome is a weighed review row
Steps: 1. On an L3 unit whose request names an outcome, ask the agent for its design
review. 2. Read the conformance statement.
Expected: one row per outcome you named, saying where the design serves it and what
share of the design goes to it.
Result:

### S2 — FS2: a comparative benefit is probed before code
Steps: 1. Open an L3 with a request such as "make the agent find the right guide
faster". 2. Let the agent reach the end of design.
Expected: before any code, a probe of that benefit exists in the unit's harness and
has been shown failing on today's system.
Result:

### S3 — FS3: no review on a small non-security change
Steps: 1. Ask for an L2 fix outside authentication, network, crypto, personal data or
filesystem areas. 2. Watch the closure.
Expected: no independent review runs and no REVIEW_LOG row is written; asking for a
review still gets one.
Result:

### S4 — FS4: a release delta is reviewed only on its judged part
Steps: 1. After a closure PASS, have the agent bump versions, regenerate indexes and
add a CHANGELOG entry, plus one README line. 2. Read the REVIEW_LOG.
Expected: a `NOT DUE` row naming the bump, indexes and CHANGELOG and the check that
ran; a review scoped to the README line.
Result:

### S5 — FS5: the benefit report counts NOT DUE rows apart
Steps: 1. Run `sdlc_check.py benefit --root <project>` on a log with a NOT DUE row.
Expected: a line "reviews ruled not due (logged, counted in no figure below): N";
the review counts and the FAIL rate are unchanged by that row.
Result:

## Regression scenarios
### R1 — design review still runs
Steps: at the end of an L3 design, before code. Expected: the design review runs as
before; nothing rules it not due. Result:

### R2 — fixing a review finding is still re-reviewed
Steps: fix a WARN from a closure review, even by a CHANGELOG edit. Expected: a
scoped re-review runs. Result:

### R3 — benefit on an existing log
Steps: run `benefit` on a REVIEW_LOG with no NOT DUE row. Expected: the same figures
as before the upgrade, plus "reviews ruled not due …: 0". Result:

## Already covered by automated tests
`scripts/test_intent_focus.py` (doctrine anchors, `benefit` on a NOT DUE row); the
four batteries (`test_drift.py` for the shared copies); `test_clients.js`.
