---
workstream: Release of the three packages
level: —
branch: feat/kb-knowledge-method
status: AWAITING OWNER
since: 2026-08-01
next: publish code 1.21.0, kb 1.4.0 and mkt 0.4.0 (2FA, owner's act) — F-028 ships in all three
details: ANALYSIS_kb_knowledge_method.md · ANALYSIS_claim_ledger.md · ADR_2026-08-01_kb_topic_graph_claim_ledger.md
updated: 2026-08-03
---

## Resume state

F-024/F-025 CLOSED (2026-08-01): method + ledger implemented, three design-gate
rounds disposed, acceptance run on the Eclosion corpus CLEAN, the capacity conflict
resolved by owner ruling with basis, ADR recorded.

## Watch out

1.20.2 / 1.0.0 / 0.3.0 were published on 2026-08-02 and carry the F-027 defects.
The prepared-but-unpublished 1.20.3 / 0.3.1 content rides along inside 1.21.0 / 0.4.0.
code moved off 1.20.1 because that tag is already pushed at a commit whose README
was wrong — never move a pushed tag. `gemini-extension.json` is the third bump point
and had been skipped for two releases; it is aligned now.

