---
workstream: F-077 kb intake: secrets, adoption on an existing ai_docs, document guides on corpus/given
level: L3
branch: claude/f077-kb-intake-hygiene-cf9cd8
status: IN_PROGRESS
since: 2026-10-22
next: Implement F-077 (TDD) per the approved ANALYSIS, then closure.
details: audit/requests/REQUEST_kb_intake_hygiene.md
updated: 2026-10-23
---

## Resume state

Field-report findings 4, 2, 3 (security-sensitive). Redaction at intake with a declared
provenance kind and a credential-pattern check on `corpus/given/`; an adoption procedure
(and possibly a dry-run command) moving document guides and their snapshots to the
corpus; one home per source text. Interim: the field project does not ingest into
`corpus/given/` until this ships.

## Next command

Elicitation round, then the ANALYSIS.
