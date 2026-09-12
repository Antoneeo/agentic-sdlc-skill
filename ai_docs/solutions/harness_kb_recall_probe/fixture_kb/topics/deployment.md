---
topic: deployment
description: how releases reach production, and who approves them
parents: []
status: CURRENT
---

## Claims

| id | claim | valid | qty | about | source | prov | state |
|---|---|---|---|---|---|---|---|
| c-dp-01 | The canary window is 30 minutes before full rollout | - | 30 min | - | corpus/notes/release-elicited.md#L3-3 | ELICITED | OK |
| c-dp-02 | Rollback is manual and owned by the release engineer | - | - | - | corpus/notes/release-elicited.md#L7-7 | ELICITED | SUPERSEDED c-dp-03 |
| c-dp-03 | Rollback is automatic on a failed health gate | from 2026-09-01 | - | - | corpus/notes/release-ruling.md#L4-4 | RULING | OK |
