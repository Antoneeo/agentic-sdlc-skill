---
id: F-001
feature: Order Intake
status: COMPLETED
level: L3
start_date: 2026-06-01
end_date: 2026-06-20
---
# Feature Analysis: Order Intake

## Objective
Accept the four order formats the customers actually send, and refuse everything
else with a reason the clerk can act on.

## Feature Vision
Serves the project Vision's Goal 1 (no manual re-entry) and Goal 2 (a rejection
the clerk can fix). Actors: order clerk (`vision/project_vision.md` `## Actors`).
Non-goal for this feature: guessing at a malformed order.

## Use Cases / User Needs
- The clerk submits a supplier CSV and it is accepted (order clerk).
- The clerk submits a truncated file and is told which line failed (order clerk).

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| parse a supplied order | MISSING | — | grep parse/read/load over src/; no owner |
| refuse with a reason | MISSING | — | grep refuse/reject/error over src/; no owner |

## Impact
`src/intake/parser.py` (new), `src/intake/reasons.py` (new), `tests/test_parser.py` (new).

## Security and Threat Model
Surface: parsing external input. A malformed file must never crash the service or
read outside `inbox/`. Mitigation: size cap before parse, no path from file content.

## Action Plan
- [x] Parser per format, selected by content.
- [x] Reason catalogue, one entry per refusal.

## Test Strategy
One accepted and one refused fixture per format; the refusal test asserts the
reason text, not only the exit code.

## Diary / Current State
- **2026-06-20 — closed.** Four formats accepted, refusal reasons reviewed by the clerk.
