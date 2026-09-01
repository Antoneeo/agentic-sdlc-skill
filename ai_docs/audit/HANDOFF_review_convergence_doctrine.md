---
workstream: F-045 Review convergence doctrine (Execute-Before-Specify + review-loop hardening, spine ported)
level: L3
branch: main (uncommitted - integration decision pending)
status: IMPLEMENTED, UNRELEASED
since: 2026-09-01
next: owner decides integration (commit/branch), then release per GUIDE_release (bump x3 + CHANGELOG); Write Triggers row for harness_[feature]/ still open (scoped out on 2026-09-01)
details: ANALYSIS_review_convergence_doctrine.md (full unit record + Diary)
updated: 2026-09-01
---

## Resume logistics

Everything implemented and verified sits UNCOMMITTED on `main`: SKILL.md
(Execute-Before-Specify + proportionality), review.md ×3 (four blocks + the
lens-gated behavioural-claim-probes reviewer clause, byte-identical across
distributions), shared_manifest.json ×3 regenerated. Battery evidence at
implementation time: 184 OK (code lens), drift OK (kb, mkt).

To resume: (1) owner's integration choice — commit on main, or move to a
feature branch first; (2) release cycle per `reference/GUIDE_release.md` —
version bump in every affected distribution + new CHANGELOG entries (released
entries are immutable); (3) optional: the open WARN — a Write Triggers row for
the new `ai_docs/solutions/harness_[feature]/` location (SKILL.md table claims
to be the authoritative write index and carries no row for it).
