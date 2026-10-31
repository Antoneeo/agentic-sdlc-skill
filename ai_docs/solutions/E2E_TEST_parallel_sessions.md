---
feature: F-088
analysis: ANALYSIS_parallel_sessions.md
---
# E2E test: coordinating parallel sessions on one repository

## What changed, in user terms
When you run several agent sessions on one repository and name one of them to
coordinate, the code skill now tells each session where to record your words, how to
share the container and the test database, what to report when it stops, and lets the
coordinator check a commit that carries several sessions' work. A session you did not
name as coordinator reads none of it. In every skill, a decision taken for you under a
delegation now appears in the request record with a label.

## Environment and preconditions
The published package of this release, installed in a client (Claude Code, Codex or
Gemini); a scratch git repository with `ai_docs/` (from `agentic-sdlc-init`) and
one commit. Python 3 for the validator.

## New-behavior scenarios

### S1 — FS1: the rules stay out of a single session
Steps: 1. In the scratch repository open one session and ask for an L3 change.
2. Ask it which support files it read.
Expected: it does not read `coordination.md`.
Result:

### S2 — FS1/FS2: a named coordinator and a part
Steps: 1. Open two sessions. 2. In the first, tell it «you coordinate the other
session». 3. In the second, start an L3 unit, then tell it a decision about the shared
milestone.
Expected: the first session records your naming in its request record; the second
appends your words to its own record under a `received for <unit>` heading and passes
them to the coordinator, which enters them in the shared record citing that entry.
Result:

### S3 — FS3: a lease
Steps: 1. In the part, ask it to restart the development container.
Expected: it asks the coordinator first; `ai_docs/audit/leases.md` gains a `take` line
naming the container and the part, later a `release` line.
Result:

### S4 — FS4: a delegated decision
Steps: 1. Tell the coordinator «decide the board approvals for me». 2. Let it decide
one. 3. Then ask it to change something you decided earlier.
Expected: the decision appears as `decided under delegation R<n>`; for the earlier
decision it asks you instead of deciding.
Result:

### S5 — FS5: a relayed authorization
Steps: 1. Tell the coordinator «I authorize the publication». 2. Ask the part to
publish.
Expected: the part does not act on the relayed authorization; it asks you, or the
coordinator acts.
Result:

### S6 — FS7: a part stops
Steps: 1. Interrupt the part mid-task and ask it to report.
Expected: it sends unit, state, files, verification, open points, what needs you.
Result:

### S7 — FS8/FS9: the commit map
Steps: 1. Change one source file per unit, add an ANALYSIS under `ai_docs/solutions/`
(a docs change is what makes `index` rewrite the indexes), and run `index`. 2. Write a map following the
template in `templates.md`, listing `ai_docs/INDEX.md` under one unit. 3. Run
`python <skill_dir>/scripts/sdlc_check.py commit-map map.md`.
Expected: `[ERROR]` naming `ai_docs/INDEX.md`, exit 1. Move it under `## Regenerated`:
exit 0.
Result:

### S8 — R13: a silent stop, an earlier permission, a hidden HANDOFF
Steps: 1. Close the part's client mid-task, then ask the coordinator whether the part is
done. 2. Before naming a coordinator, tell a session «restart the container freely»; name
a coordinator; ask that session to restart. 3. In S7's map, move the HANDOFF under
`## Regenerated` and run `commit-map`.
Expected: 1. the coordinator says the part is not done, reads its HANDOFF and tree, and
tells you which closure steps it can and cannot confirm; it asks you whether to resume it.
2. the session asks the coordinator for a lease first. 3. `[ERROR]` naming the HANDOFF.
Result:

## Regression scenarios

### R1 — review-map unchanged
Steps: on any branch run `sdlc_check.py review-map`.
Expected: the same table as before this release.
Result:

### R2 — request records still read
Steps: run `python <skill_dir>/scripts/docs_site.py --root . --open` on a project
with request records.
Expected: the chronology lists every entry, labelled ones included.
Result:

### R3 — one session, own worktree
Steps: with no coordinator named, start two sessions on the same repository.
Expected: each works in its own worktree, as before.
Result:

## Already covered by automated tests
`test_review_map.py` (`commit-map`: every error and warning, base HEAD, escaping,
unreadable map, no git); `test_chronology.py` (labelled headings parse); support-file
wiring and drift (`test_skill_invariants.py`, `test_drift.py`) in the four packages;
`scripts/test_clients.js`.
