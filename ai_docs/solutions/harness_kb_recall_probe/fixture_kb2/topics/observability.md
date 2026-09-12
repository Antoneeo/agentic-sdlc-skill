---
topic: observability
description: logging, metrics, tracing and the alerting rules
parents: []
status: CURRENT
gaps:
  - no claim yet on the tracing sampling rate
---

## Claims

| id | claim | valid | qty | about | source | prov | state |
|---|---|---|---|---|---|---|---|
| c-obs-01 | Access logs are written to the append-only audit sink, never to stdout | - | - | - | corpus/notes/obs-elicited.md#L4-4 | ELICITED | OK |
| c-obs-02 | Alert fatigue budget is 5 paging alerts per engineer per week | - | 5 alerts | - | corpus/notes/obs-elicited.md#L9-9 | ELICITED | OK |
