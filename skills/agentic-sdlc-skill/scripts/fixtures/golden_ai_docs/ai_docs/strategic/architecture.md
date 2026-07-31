---
description: How the Widget Service is built and which component owns what.
status: CURRENT
---
# Project Architecture

## Technology Stack
Python 3.11, stdlib only. No framework, no database: orders are files.

## Directory Structure
- `src/intake/` — parsers, one per accepted format.
- `src/picking/` — pick-list construction.
- `tests/` — one test module per component.

## Component Map

| Component | Responsibility | Contract | Where |
|---|---|---|---|
| Order parser | Turn a supplied order file into an internal order, or refuse it with a reason | One parser per format, selected by content, never by file extension | `src/intake/parser.py` |
| Pick list builder | Turn an accepted order into an unambiguous pick list | Every line names a widget by id, never by display name | `src/picking/builder.py` |

## Architectural Patterns
- Refuse-with-a-reason over best-effort parsing.
- Ids over display names on every machine-consumed surface.
