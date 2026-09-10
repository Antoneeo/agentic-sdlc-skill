---
workstream: F-047 kb row atomicity (bundled claim rows - atomicity doctrine, split move, citation-scope rail, de-trapped collision remedy, plurality note)
level: L3
branch: main
status: DONE, UNRELEASED
since: 2026-09-08
next: kb release (bump + CHANGELOG per GUIDE_release) on the owner's call — the spine delta is kb-only, so a single-package release
details: ANALYSIS_kb_row_atomicity.md (unit record + Diary); harness_kb_row_atomicity/probe.py (all probes green)
updated: 2026-09-08
---

## Resume logistics

All edits are kb-local (6 files under `distributions/kb-agentic-skill/`), uncommitted
on `main`, plus the ANALYSIS + harness in this repo's `ai_docs/solutions/`. Evidence:
harness P1-P4 all green; kb battery 376 OK; mkt battery OK; code battery green except
the two repo-index tests this registration + `sdlc_check.py index` clears. Design
review: FAIL → PASS in 2 rounds (1 BLOCK: state grammar documented singular in three
sites — folded). Reporting project's ledger stays bundled by design: the split move
is now doctrine, their rows move per reconciliation.md when they choose.
