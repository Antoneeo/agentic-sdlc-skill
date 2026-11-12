---
description: Post-merge script for F-095 - a human checks that a named coordinator sends unit work and integrations to parts.
status: CURRENT
---
# E2E test: the coordinator does not do a part's work (F-095)

## What changed, in user terms

A session you named coordinator no longer merges, pushes or tidies the repository itself:
it sends that work to a session (a part) and verifies the result. The part that made a
branch integrates it.

## Environment and preconditions

The released skill installed; one repository with a named coordinator (`leases.md`) and a
part that finished a unit on its own branch.

## New-behavior scenarios

### S1 — integration goes to the part
Tell the coordinator: "integrate it and push". Expected: it sends the integration to the
part, quoting your words; it runs at most a fast-forward of the shared checkout.

### S2 — cleanup goes to a part
Tell the coordinator: "clean up the old worktrees". Expected: it opens or asks a part,
which declares level and router verdict before touching anything.

### S3 — explicit order
Tell the coordinator: "do this unit here". Expected: it opens the unit's own request record
and declares level and verdict before working.

## Regression scenarios

### R1 — documents-only closure
A documents-only part in the shared checkout closes. Expected: the coordinator still runs
`index`/`mark` for it.

### R2 — leases
A part asks for an exclusive resource. Expected: unchanged, the coordinator writes the lease.
