---
description: E2E script for F-096 - what a person checks by hand after the merge: the scope line of check, the advisory on a closed workstream file, the resume line of the orientation after a real compaction.
status: CURRENT
analysis: ANALYSIS_honest_signals.md
---
# E2E test: Honest signals (F-096)

## What changed, in user terms

- `check` now says, after its verdict, what it covers: the form of the documents, not
  whether their sentences are still true.
- `validate` and `index` name a workstream file whose own `status:` says the work is
  finished. It is an advisory: no build fails because of it.
- Every session orientation carries one line telling an agent that works from a summary to
  re-read the open unit's request record and vision before answering about it.
- At closure the agent re-reads whole every document the work impacted and says so in its
  closure message (`re-read whole: …`).

## Environment and preconditions

- The four packages installed from this branch (or the released version that carries
  F-096), on a machine with Python and Claude Code.
- A project with a docs root and the session-orientation hook wired (`init` wires it).
- For S3, a session long enough to be compacted, or the client's manual compaction command.

## New-behavior scenarios

### S1 — the check verdict states its coverage (FS3)
1. In any governed project run `python <skill_dir>/scripts/sdlc_check.py check --root .`.
2. Expected: the line after `check: CLEAN (…)` or `check: NOT CLEAN (…)` begins with
   `[scope]` and says the check does not read whether the sentences are still true. The
   exit code is the one the same project gave before the upgrade.
3. Marketing lens: `python <skill_dir>/scripts/mkt_check.py check --root .` on a project
   with `mkt_docs/`: the `[scope]` line follows `[OK] check clean` or `[FAIL] check: …`.

### S2 — a closed workstream file is named (FS4)
1. In a project that keeps `audit/HANDOFF_*.md` files, set the `status:` of one to `DONE`
   (or pick one that already says `DONE`, `COMPLETED` or `CANCELLED`).
2. Run `index`. Expected: one `[note]` line naming that file, next to the "registry
   regenerated" line. `audit/handoff.md` contains no such line.
3. Run `validate --strict`. Expected: one `[note]` line for that file saying it declares
   that status and what to do; the exit code is unchanged by it.
4. Set the status to `Implemented (DONE)`. Expected: the file is no longer named. That is
   the stated limit: only a status that begins with the lifecycle word is matched.
5. Restore the file.

### S3 — the resume rule reaches a compacted session (FS7, FS6)
1. In Claude Code, in a project with an open L3 unit, work until the context is compacted
   (or run the manual compaction).
2. Expected: the orientation is in the resumed context and contains the line that begins
   "If you work from a summary". **This step is the only verification that the client
   re-runs the session-start hook after a compaction**: if the orientation is absent, the
   rule still stands in `SKILL.md`, and the finding goes back to the unit.
3. Ask about a part of the open unit that the summary does not mention. Expected: the
   agent reads that unit's request record and vision before answering, and cites them.

### S4 — closure names what was re-read (FS1, FS2)
1. Close a small L2 or L3 change that alters something a guide describes.
2. Expected: the guide's sentences about the earlier state are rewritten, not left above an
   added row; the closure message carries `re-read whole: <that guide>`.
3. Close a change that impacts no document. Expected: `re-read whole: none impacted`.

## Regression scenarios

- R1. `orient` on a project with no docs root prints nothing and exits 0.
- R2. `orient` output on a large project stays within its size bound: the guide router and
  the workstream registry are still shown, cut as before.
- R3. `validate --strict` in CI on a project that was green before the upgrade is green.
- R4. `index` twice in a row changes no generated file the second time.
- R5. The registry (`audit/handoff.md`) of a project with several open workstreams is byte
  for byte what `index` generated before, apart from nothing: no new column, row or line.

## Already covered by automated tests

- FS3: `test_session_start.ScopeAndResumeTests` (three tests); marketing overlay in
  `test_mkt_check.ClosedWorkstreamOwnRootTests`.
- FS4: `test_merge_safety.MS_ClosedWorkstreams` (eight tests); marketing own and shared
  docs root in `test_mkt_check`.
- FS5 and the reach of the doctrine into every lens: `test_skill_invariants.F096_HonestSignals`.
- FS7, no stdin read, size bound: `test_session_start.ScopeAndResumeTests`.
- The exact output change: the golden transcripts of the code, knowledge and marketing lenses.
- The recorded cases: `harness_honest_signals/probe_closed_handoffs.py` and
  `probe_signals.py`, red on release 1.55.0 and green on this change.
