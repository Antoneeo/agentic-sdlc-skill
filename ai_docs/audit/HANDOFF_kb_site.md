---
workstream: F-072 docs site (static site generated from ai_docs, shared by the family)
level: L3
branch: feat/kb-site-spec
status: PLANNED
since: 2026-10-16
next: owner decision on the round-4 rewrite; then merge origin/main into this branch (main moved to 1.40.0 and holds SPIKE_kb_viewer.md), commit and push for implementation on the owner's other machine
details: ANALYSIS_kb_site.md · PROPOSAL_vision_v9_state_view.md · REQUEST_kb_site.md · harness_kb_site/probe.py
updated: 2026-10-17
---

## Resume logistics

Specification only on this branch, no code (R9). The implementer works from
`solutions/ANALYSIS_kb_site.md` alone (the generator is `docs_site.py`, a shared spine file); `harness_kb_site/probe.py --root <project>` prints
the counts acceptance criterion 1 compares against. A field KB for the end-to-end run
lives on the owner's work machine, not in this repository.
