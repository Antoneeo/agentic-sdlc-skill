---
workstream: F-022 Multi-Domain Core
level: L3
branch: feat/multi-domain-core
status: DONE, HELD
since: 2026-07-31
next: nothing outstanding — the release hold is lifted by the owner
details: ANALYSIS_multi_domain_core.md
updated: 2026-08-01
---

## Resume state

Complete and consolidated: one repository, the code distribution at the root, kb and
mkt under `distributions/` grafted with `git subtree` (history preserved). Batteries
green, three golden transcripts intact, drift guard comparing the copies to each
other, `npm pack` correct for all three.

## Watch out

mkt's TAGS did not transfer with the subtree and still live only in the old clone
and on GitHub. Release was HELD by the owner (2026-08-01) until kb was effective —
kb is now published through 1.3.0.

