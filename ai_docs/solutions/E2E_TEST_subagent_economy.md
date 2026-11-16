---
feature: F-100
analysis: ANALYSIS_subagent_economy.md
---
# E2E test: subagent economy

## What changed, in user terms

When an agent hands work to a subagent and names guides it must follow, it now asks the
subagent how much of each guide it read (total lines, last line read) and checks the totals
before testing or reviewing the work. Work built on a guide read in part is redone, not
tested or reviewed. A subagent that runs out of room on a guide twice does not get that guide
again: the work goes to a stronger model or is split by guide. Corrections go back to the
subagent that already has the guides in mind, instead of a new one that must reread them.
When the agent asks you how the team is made, it also tells you, in a line or two, what
several sessions cost and what they give you, compared with one session and its subagents.

## Environment and preconditions

- The four packages built from this change, installed with each package's install command
  (`GUIDE_release.md` names them).
- A client that can start subagents and, for S3, send a further message to one it started
  (Claude Code: the Agent tool and SendMessage).
- Project P: a project with an approved L3 design, a validated `PLAN_*.md` whose tasks name
  guides in `ai_docs/reference/` (two guides of several hundred lines each are enough), and a
  `## Team` section.
- Project T: a project with no `## Team` in its reading guide.

## New-behavior scenarios

### S1 — FS2: the plan brief asks for the read
Steps: 1. In project P, run `python <skill_dir>/scripts/sdlc_check.py plan brief <plan> --task <id>`
for a task with guides, then for one without.
Expected: under the guide pointers of the first, the line "Read each guide above whole, and
report for each its total lines and the last line you read."; the second has no such line.
Result:

### S2 — FS2: the read is checked before verify
Steps: 1. In project P, ask the agent to execute the plan through subagents (`dispatch.md`).
2. Watch the first task's report and the agent's next step.
Expected: the subagent's report gives, per guide, total lines and last line read; the agent
compares the totals with the guides before running `verify`. If a report omits them, the agent
asks once; a partial read is recorded `failed` in the ledger with the partial read named, and
the step is redone after the rest is read.
Result:

### S3 — FS4: a correction goes back to the same subagent
Steps: 1. Continue S2 until a per-task review returns findings.
Expected: the agent sends the findings to the subagent that did the task (a further message to
it), not to a new subagent; the review of the correction runs in a fresh reviewer context.
Result:

### S4 — FS5: the team question carries the cost
Steps: 1. In project T, ask for a clearly level-3 feature. 2. Read the team questions.
Expected: the question on members says what several sessions cost and buy against one
session with subagents, recommends no shape, and offers the default (one agent).
Result:

## Regression scenarios

### R1 — a session that delegates nothing pays nothing
Steps: 1. In project P, ask for an L2 fix and let the agent do it without subagents.
Expected: no read-back request, no length check, no change in the flow.
Result:

### R2 — two failed verify rounds still go to deep
Steps: 1. In project P, make a task's `verify` fail twice (a deliberately wrong assertion).
Expected: the retry goes to the deep tier in a new context, as before F-100.
Result:

### R3 — the team is asked once, and never at L1/L2
Steps: 1. In project T after S4, ask for a second L3 feature, then for an L2 fix.
Expected: no team questions either time.
Result:
