---
id: F-002
feature: Pick List
status: IN_PROGRESS
level: L3
start_date: 2026-07-29
end_date:
---
# Feature Analysis: Pick List

## Objective
Turn an accepted order into a pick list the operator can execute without asking
the clerk which widget is meant.

## Feature Vision
Feature vision: `ai_docs/vision/features/VISION_pick_list.md`. Advances Goal 1 of
the project Vision; Actor: warehouse operator.

## Use Cases / User Needs
- The operator picks a widget whose display name is shared with another (warehouse operator).

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| read an accepted order | EXISTS | `src/intake/parser.py#load_accepted` | re-read `load_accepted()`: returns the internal order or raises |
| render a pick line | MISSING | — | grep pick/line/render over src/ and tests/; no owner |

## Impact
`src/picking/builder.py` (new), `src/intake/parser.py` (one exported helper), `tests/test_builder.py` (new).

## Security and Threat Model
No new external input: the builder consumes an already-parsed order. Filesystem
write is confined to the output directory passed by the caller.

## Action Plan
- [x] Builder skeleton and its test.
- [ ] Id-and-name rendering per the ADR.

## Test Strategy
Two widgets sharing a display name must produce two distinguishable lines.

## Diary / Current State
- **2026-07-30 — in progress.** Builder skeleton green; rendering next.
