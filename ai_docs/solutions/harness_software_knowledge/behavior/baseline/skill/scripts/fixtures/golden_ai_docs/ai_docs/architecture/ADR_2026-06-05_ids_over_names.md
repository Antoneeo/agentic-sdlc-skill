---
description: Why every machine-consumed surface carries widget ids rather than display names.
status: CURRENT
---
# ADR: Ids over display names on machine-consumed surfaces

**Status:** Accepted
**Date:** 2026-06-05
**Task ref:** F-001 (`ai_docs/solutions/ANALYSIS_order_intake.md`)

## Context
Two widgets share the display name "Bracket, small". The operator picked the
wrong one twice in one week.

## Decision
Every machine-consumed surface — pick list, callback payload, log line — carries
the widget id. Display names appear only next to an id, never alone.

## Alternatives considered
- **Make display names unique** — rejected: the names come from the supplier
  catalogue and are not ours to change.
- **Disambiguate in the UI only** — rejected: the pick list is printed.

## Consequences
- **Pro:** the ambiguity cannot reach the operator.
- **Con / risk:** ids are unreadable, so every surface must carry both.
