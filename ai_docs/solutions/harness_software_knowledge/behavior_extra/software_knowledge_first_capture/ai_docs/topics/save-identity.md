---
topic: save-identity
description: Identity returned by save(record) and its input condition.
parents: [record-identity]
owns: [record-identity/save-result]
synonyms: [save identity, original_id, returned identity]
gaps:
  - No runtime execution has verified the return behavior.
  - Undo behavior was not examined and cannot be inferred from save.
claim_schema: 2
status: CURRENT
---

## Claims

| id | claim | valid | qty | about | source | prov | state | kind |
|---|---|---|---|---|---|---|---|---|
| 781c4075ad2c | save(record) returns the value at record['original_id']. | - | - | - | corpus/notes/save-identity-initial.md#L9-9 | DERIVED | SUPERSEDED 16896b330b2b | OBSERVATION |
| 16896b330b2b | For an ordinary dictionary containing original_id, save(record) returns that entry's value. | if record is an ordinary dictionary containing original_id | - | - | corpus/notes/save-identity-current.md#L9-9 | DERIVED | OK | OBSERVATION |
