---
feature: F-089
analysis: ANALYSIS_parallel_sessions_gaps.md
---
# E2E test: the shared checkout, shared files and coordinator handover

## What changed, in user terms
When you run several agent sessions on one repository with a coordinator, a session
that writes only documents may now work in the checkout already in use instead of its
own worktree, so it leaves you no branch to merge. Each file several sessions touch has
one writer. The coordinator stays the same after its context is compacted, is not
passed on to a session it starts, and changes only when you name another one.

## Environment and preconditions
The published package of this release, installed in Claude Code; a scratch git
repository with `ai_docs/` (from `agentic-sdlc-init`) and one commit; one session named
coordinator in a request-record entry, as in the F-088 script.

## New-behavior scenarios

### S1 — FS1: a documents-only session in the shared checkout
Steps: 1. Open a second session in the same folder as the coordinator (no worktree).
2. Ask it for an L3 unit that only writes design documents. 3. Ask it to regenerate the
indexes.
Expected: it writes only its unit's files under `ai_docs/`; it does not create a branch
or worktree; it does not run `index` and asks the coordinator to.
Result:

### S2 — FS1: the move to code
Steps: in the same session ask it to implement a small code change for its unit.
Expected: before writing code it asks the coordinator: it takes the code-writer lease, or
asks you to commit its documents first and then works in its own worktree.
Result:

### S3 — FS2: shared files
Steps: 1. Let two sessions each finish a review. 2. Ask the documents-only session to
fix a wrong translation string in a `.po` catalog.
Expected: each appends only its own row to `REVIEW_LOG.md`; the catalog fix is sent to
the code-writer through the coordinator, not written by the documents-only session.
Result:

### S4 — FS3: compaction and a session started by the coordinator
Steps: 1. Compact the coordinator's context (`/compact`), then ask it who holds the
container. 2. Ask the coordinator to start a new session and tell that one it continues
the coordination.
Expected: after compaction it reads `ai_docs/audit/leases.md` before answering; the new
session does not act as coordinator and asks you to name it.
Result:

### S5 — FS3: handover
Steps: tell a part «da ora coordini tu».
Expected: the part enters your words, appends a `coordinator` line to `leases.md` and
tells the previous coordinator, which answers that it stopped; you receive the list of
lines the new coordinator did not write in between (possibly empty).
Result:

### S6 — FS1: closing a documents-only unit in the shared checkout
Steps: ask the documents-only session to close its unit.
Expected: its closure message lists under `Open points` the steps it leaves to the
coordinator (`index`, `review-map`, `mark`); the coordinator runs them, writes that
unit's section of the commit map, and the unit's merge brief takes its file table from
that section and says so.
Result:

## Regression scenarios

### R1 — no coordinator
Steps: with no coordinator named, start two sessions on the same repository.
Expected: each works in its own worktree, as before.
Result:

### R2 — a part's own record
Steps: in a part with an L3 unit, answer one of its questions.
Expected: it records your answer in its own request record before acting, as before.
Result:

### R3 — commit map
Steps: write a commit map listing `.devpnt/plans/plans.db` under Shared and run
`sdlc_check.py commit-map MAP`.
Expected: no error for that file, as before.
Result:

### R4 — the bans hold in the shared checkout
Steps: ask the documents-only session to switch branch, or to stash its changes.
Expected: it refuses, as before: no session switches branch, stashes or resets in a
checkout another session may be using.
Result:

## Already covered by automated tests
No code changed. Support-file wiring and drift (`test_skill_invariants.py`,
`test_drift.py`) and `scripts/test_clients.js`; `commit-map` behaviour in
`test_review_map.py`, unchanged.
