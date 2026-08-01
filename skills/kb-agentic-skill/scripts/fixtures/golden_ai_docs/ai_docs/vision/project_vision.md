---
description: Why the Widget Service exists and what it refuses to become.
status: CURRENT
---
# Project Vision

Status: APPROVED (by the owner — 2026-06-01)

## North Star
One service turns a customer order into a shipped widget without a human
retyping anything.

## Core Problem
Orders arrive in four formats and are re-keyed by hand into the shipping tool.
Every re-key is a chance to ship the wrong widget to the wrong address.

## Actors
- **Order clerk** — receives orders, wants to stop re-typing them.
- **Warehouse operator** — picks and ships, wants an unambiguous pick list.

## Goals
1. An order accepted by the service is shipped without manual re-entry.
2. A rejected order tells the clerk what to fix, in the clerk's words.

## Invariants
- An order is never shipped twice.
- A rejected order is never silently dropped.

## Non-Goals
- **Not an inventory system.** Stock levels belong to the warehouse tool; this
  service reads them and never owns them.
- **Not a CRM.** Customer records are read by id; nothing here edits them.

## The admission test
A change is admitted when it moves an Actor above closer to a Goal without
breaking an Invariant or entering a Non-Goal. Quote the clause you relied on.

## Success Signals
- Re-keyed orders per week reaches zero.
- A rejected order is corrected and resubmitted without asking support.

## Where the rest lives
Milestones: `roadmap.md`. Decision rules: `principles.md`.
