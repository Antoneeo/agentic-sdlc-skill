---
description: Static save return behavior with the required original_id condition.
domain: code
topics: [save-identity]
derived_from: [corpus/given/source-b1c4e9b45e869661b1c9c0a3118542fa843225e0700280eb5773042891219d26-73904fd937e207b454df6ea823a3d4fd2ad9cf7395b8c3275af0182e9ca0a4fb.txt, corpus/notes/save-identity-finding.md]
date: 2026-10-04
status: CURRENT
---
For an ordinary dictionary containing original_id, save(record) returns that entry's value.
The direct subscript in inputs/save.py line 1 supports the presence condition; no fallback is supplied.
For the next agent: use the current save-identity claim and its captured ground when explaining save identity. This note answers the returned-value question; it does not establish persistence, callers, custom mapping behavior, or undo behavior.
Evidence is static code inspection and the supplied refinement; no implementation runtime test was executed.
