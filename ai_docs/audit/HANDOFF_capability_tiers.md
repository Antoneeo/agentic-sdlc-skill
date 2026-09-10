---
workstream: F-048 capability tiers + delegation boundary (floor no gate may start below, what may be delegated at all, REVIEW_LOG `model` column)
level: L3
branch: main
status: DONE, UNRELEASED
since: 2026-09-10
next: nothing outstanding except the owner's integration call - all three reviews PASS, everything green and uncommitted on main; release (bump + CHANGELOG per GUIDE_release, all three packages) deferred to the owner
details: ANALYSIS_capability_tiers.md (unit record, precedent placement, ceremony disclosure); harness_capability_tiers/probe.py; ADR_2026-09-10_capability_floor_and_delegation_boundary.md
updated: 2026-09-10
---

## Resume logistics

**Everything designed is implemented and in the tree, uncommitted on `main`.** The
owner accepted the ceremony cost on 2026-09-10 (recorded in `rulings.md` r20 and in
the ADR), so nothing is waiting on a decision.

In place: the capability floor in `review.md` (it owns the gates the floor binds —
moved there from `dispatch.md` at design review R1) with the threshold-signal rule
and the "independence wins" arbitration; the delegation boundary in `dispatch.md`,
declared family-wide; the `model` column in `review.md` and all three
`templates.md`, with "one schema" redefined as core plus mode-specific columns;
three `SKILL.md` pointers widened; two new tests in the shared battery; spine
ported byte-identical ×3 with the manifests regenerated; `rulings.md` r20/r21; the
ADR; both REVIEW_LOG rows written in the new schema.

**What remains is the owner's integration call only.** Reviews: design
**FAIL → FAIL → PASS** (3 rounds), closure **FAIL → PASS** (2), sharing one final
scoped round that verified every correction by execution rather than inspection.
Verified at that round: harness 17/17, batteries 193/378/211 OK, `check --hybrid`
CLEAN, spine byte-identical ×3 with matching manifests. The sharpest finding was
in the unit's own falsifiability instrument: the value-set regex could not express
two of the five legal `model` values, so the probe would have reddened on legal log
content while the coverage check silently under-covered.

Note for whoever commits: **F-047 (kb row atomicity) also sits uncommitted in this
tree** and is a separate, separately-reviewed unit — the F-048 closure review was
given a diff scoped away from it. Two commits, not one.

Known and deliberately untouched: `rulings.md` carries two rows numbered `r19`
(pre-existing); this unit took r20/r21. `ANALYSIS_capability_tiers.md` shares the
missing-`## Feature Vision` validator warning with four peer analyses — now added
here, the peers are not this unit's business.
