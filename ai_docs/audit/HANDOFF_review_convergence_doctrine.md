---
workstream: F-045 Review convergence doctrine (Execute-Before-Specify + review-loop hardening, spine ported)
level: L3
branch: main
status: DONE, PUBLISHED
since: 2026-09-01
next: publish code 1.31.0 with publish_all.bat (owner's act, 2FA), then verify on the registry; kb/mkt unchanged and skipped, their spine delta ships at their next release. Deferred item unchanged: Write Triggers row for harness_[feature]/
details: ANALYSIS_review_convergence_doctrine.md (full unit record + Diary)
updated: 2026-09-05
---

## Resume logistics

Unit committed on `main` (fcccf21, F-045) and released per GUIDE_release:
release commit carries the bumps (code 1.30.0, kb 1.12.0, mkt 0.8.0 — four
points each) + CHANGELOG entries ×3 + this handoff; tags `v1.30.0`,
`kb-v1.12.0`, `mkt-v0.8.0` on the release commit. Verification battery at
release time: npm pack clean ×3, init.js smoke CLEAN, check --hybrid CLEAN,
unittest green ×3.

To finish: (1) `publish_all.bat` from the repo root — USER's step, 2FA opens a
browser per package; skips-already-published is normal; it packs the WORKING
TREE, so run it from this tagged checkout. (2) Verify:
`npm view @antoneeo/agentic-sdlc-skill version` → 1.30.0 (and kb/mkt
equivalents). (3) Optional open WARN: a Write Triggers row for
`ai_docs/solutions/harness_[feature]/`.

## Amendment 2026-09-05 — code 1.31.0

An independent review rejected two proposed rules (measure the gap at the
objective's altitude; a form budget for units with no external number) on
evidence that inverted their support: the unit cited as unprobeable text about
text is a CODE unit that modified six production modules and shipped four
assertion harnesses, and its nine rounds are not the log's modal count. What
landed instead is inside the rule that already exists — Execute-Before-Specify
now covers a deliverable that is itself text, probed by replay against the
recorded case that motivated it, red under the old text and green under the
new. Paid for per `vision.md`'s cumulative ratchet: 67 words of illustration
deleted from the same paragraph (net -2 words).

The form budget landed in the spine `review.md`, where it has an owner, a unit
and a measured number: the lean operative form is the FIRST draft's form, stated
as a line count in the review request, and an over-budget artifact is the
reviewer's first finding. Spine synced byte-identical ×3 and the shared
manifests regenerated in all three distributions (the drift guard caught the
one-lens edit — `test_no_shared_file_has_diverged`). Derived documents refreshed
before `mark`: `strategic/skill_family_agent_workflows.md` (both the
Execute-Before-Specify bullet and the review-loop line the old text falsified).

Release battery green: eval 184 OK, `check --hybrid` CLEAN, npm pack 22 files
with no `__pycache__`/`.sources/`/test harness, init.js smoke CLEAN.
