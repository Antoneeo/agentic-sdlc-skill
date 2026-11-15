---
feature: F-097
analysis: ANALYSIS_open_fronts.md
---
# E2E test: open fronts

## What changed, in user terms

When you ask an agent for new significant work (level 3), its first message now shows
you the project's open workstreams as the registry lists them, and then goes on with
your request. And `validate` now names an analysis that says it is in progress while
the registry has no row for it.

## Environment and preconditions

- The four packages built from this change, installed with each package's install
  command (`GUIDE_release.md` names them).
- A client with the skill loaded; the session-start hook is not required.
- Project A: any project with a generated workstream registry of at least two rows
  (`ai_docs/audit/handoff.md` starting with the GENERATED comment). The fixture built by
  `ai_docs/solutions/harness_open_fronts/build_intake_fixture.py --small` is one.
- Project B: a copy of project A in which every `audit/HANDOFF_*.md` is deleted and
  `index` was run, and one `solutions/ANALYSIS_*.md` has `status: IN_PROGRESS`.
- Project C: a project that never used the generated registry (no `audit/handoff.md`).

## New-behavior scenarios

### S1 — FS1, FS2: the rows are shown when a new level-3 unit opens
Steps: 1. In project A, ask for a feature that is clearly level 3 and that no open
workstream covers (for example a new authenticated endpoint). 2. Read the agent's first
message. 3. Open `ai_docs/audit/handoff.md` beside it.
Expected: the message has the line `Open workstreams (audit/handoff.md, as declared):`
followed by one line per registry row, each with that row's workstream, status and next
step exactly as in the file, in the file's order. It has no count of the rows, no
comment on any row, no suggestion of what to close or do first, and no question about
them. The same message opens your request (level declared, request record named).
Result:

### S2 — FS3: a request an open workstream already carries is resumed
Steps: 1. In project A, ask the agent to continue the work of one registry row, in your
own words. 2. Read its first message and list `ai_docs/audit/requests/`.
Expected: the message names that row and the agent resumes it; no second unit appears
(no new request record for one).
Result:

### S3 — FS1: the two one-line forms
Steps: 1. In project B, ask for a new level-3 feature. 2. In project C, ask the same.
Expected: project B's message has the line `Open workstreams: none`; project C's has
`Open workstreams: no generated registry`.
Result:

### S4 — FS4: an analysis in progress with no row is named
Steps: 1. In project B, run `validate`.
Expected: one line starting `[note]` names the `IN_PROGRESS` analysis, says no
workstream file names it, and gives both ways out (write its workstream file with the
analysis in `details:` and run `index`; or set its status). The command's exit code is
the same as before the analysis was set to `IN_PROGRESS`.
Result:

### S5 — FS1 in the course lens (limit declared)
Steps: 1. With the course lens, in a project with a generated registry, ask for a new
level-3 course.
Expected: the message shows the registry's rows as in S1. A course that is in progress
and is not concurrent work may be absent from them: that is that lens's rule, not a
defect.
Result:

## Regression scenarios

### R1 — a small request shows no block
Steps: 1. In project A, ask for a level-2 fix (one file, clear cause).
Expected: the level is declared L2 and the message has no `Open workstreams` block.
Result:

### R2 — `validate` on a project that follows the method prints nothing new
Steps: 1. In a project whose every `IN_PROGRESS` analysis is named by a workstream file
(by file name in `details:`, or by unit id in `workstream:`), run `validate` and `check`.
Expected: no line containing "no workstream file"; verdict and exit code as before the
upgrade.
Result:

### R3 — a project that never generated a registry is untouched
Steps: 1. In project C, set an analysis to `IN_PROGRESS` and run `validate`.
Expected: no line containing "no workstream file".
Result:

### R4 — `index` and the registry are unchanged
Steps: 1. In project A, run `index`, then `validate`.
Expected: `audit/handoff.md` is byte-identical to before; `validate` reports the
registry aligned with its sources.
Result:

## Already covered by automated tests

- The advisory's cases (in progress and unnamed; named by file name or by unit id;
  planned, completed, cancelled; emptied registry; never generated; hand-written
  handoff; shadow; no unit id; course domain, declared or by project default; body-only
  mention; `--strict` exit unchanged): `test_merge_safety.py`, class
  `MS_UncarriedAnalyses`, in all four packages.
- The wording of the rule in each lens: `test_skill_invariants.py`, class
  `F097_OpenFronts`.
- The validator's output on the reference corpus is byte-identical:
  `test_golden_regression.py`.
