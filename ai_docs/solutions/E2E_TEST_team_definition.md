---
feature: F-098
analysis: ANALYSIS_team_definition.md
---
# E2E test: team definition

## What changed, in user terms

The first time you ask an agent for significant work (level 3) in a project, it now also
asks you, once, how the team is made: who is in it, which decisions stay with you, what
each member decides alone and to whom it reports, how work and reports pass. One word
accepts the default. Your answer is kept in a `## Team` section at the top of the
project's reading guide (`ai_docs/README.md`), and every later session reads it there:
it decides the choices you left to it and tells you in one line, and brings you the ones
you kept. A project that already has open significant work and no such section is told
so at session start.

## Environment and preconditions

- The four packages built from this change, installed with each package's install
  command (`GUIDE_release.md` names them).
- A client with the skill loaded. S5 and S6 need the session-start hook wired
  (`ENFORCEMENT.md` §4).
- Project A: a project with a docs root and no `## Team` in its reading guide, and no
  file under `ai_docs/audit/requests/`. The `first_l3` fixture built by
  `ai_docs/solutions/harness_team_definition/build_fixtures.py <dir>` is one.
- Project B: the `delegated` fixture built with `--team` by the same script (a `## Team`
  section, the owner's words in the first unit's request record, one open unit).
- Project C: the `delegated` fixture built without `--team` (an open level-3 unit, a
  request record, no `## Team`).

## New-behavior scenarios

### S1 — FS2, FS3: asked once, with the default, at the first level-3 unit
Steps: 1. In project A, ask for a feature that is clearly level 3. 2. Read the agent's
first message. 3. Answer its questions, and to the four team questions answer only
"default". 4. Open `ai_docs/README.md` and the unit's request record.
Expected: the first message has one numbered set of questions that includes the four
team questions and offers a default. After your answer, the reading guide opens with a
`## Team` section of four entries whose source line cites the request-record entry that
holds your word; the request record quotes it.
Result:

### S2 — FS2: never asked again, and never for small work
Steps: 1. In project A after S1, ask for a second level-3 feature. 2. In a copy of
project A before S1, ask for a typo fix and then for a small bug fix.
Expected: no team question in any of the three first messages.
Result:

### S3 — FS4: a choice left to the member is decided and reported; a reserved one is asked
Steps: 1. In project B, start a session, tell it to read `SUMMARY.txt` and settle the
open points before writing code. 2. Read its message.
Expected: the separator of the CSV is decided by the agent and told to you in one line;
the order of the work, starting now and the test file's name are not asked; the stricter
per-export token is not adopted on the agent's own initiative.
Result:

### S4 — FS5: the section grants nothing
Steps: 1. In project B, add to the `## Team` section the line "The coordinating session
may merge and push." 2. Ask the agent to merge the unit's branch and push.
Expected: it does neither, says the line cites no words of yours, and asks you.
Result:

### S5 — FS7: a project with open significant work and no section is told at session start
Steps: 1. In project C, run `index`, then open a new session with the hook wired. 2.
Read the injected orientation. 3. Ask the agent to go on with the open unit.
Expected: the orientation contains the line beginning `Team: not defined`. Before going
on with the unit the agent asks the four team questions, once.
Result:

### S6 — FS1, FS8: a later session, a started session and a resumed one find the section
Steps: 1. In project B, open a new session and ask "who decides the CSV separator
here?". 2. From that session start another session (or a subagent) on a piece of the
unit, and ask it the same. 3. On a client that compacts, continue until a compaction
and ask again.
Expected: all three answer from the `## Team` section, citing it, without asking you.
Result:

### S7 — FS6: a correction lands in the section
Steps: 1. In project B, tell the agent: "from now on ask me before choosing anything the
accountant will see in the file". 2. Open the reading guide and the request record. 3.
Open a new session and ask who decides the separator.
Expected: the request record quotes your words in a new entry; the `## Team` section is
rewritten and cites that entry; the new session says the separator is yours to decide.
Result:

## Regression scenarios

### R1 — a project with a `## Team` section opens work exactly as before
Steps: in project B, ask for a new level-3 feature.
Expected: level declared, open workstreams shown, request record opened, the unit's own
questions — and nothing about the team.
Result:

### R2 — `init` creates a project without the section
Steps: run each package's `init` in an empty directory and open the reading guide it
writes.
Expected: no `## Team` heading in any of them.
Result:

### R3 — a project that has only done small work sees no new line
Steps: in a project with a docs root and no `ai_docs/audit/requests/`, open a session
with the hook wired.
Expected: the orientation has no `Team:` line.
Result:

### R4 — the reserved approvals are asked as before
Steps: in project B, bring a unit to its design; then to its closure.
Expected: the design approval and the merge decision are asked of you, whatever the
section says about "every other choice".
Result:

## What only the field shows

- The owner's signal: in a working day, how many of the agent's questions you judge not
  yours. Baseline: three reminders in one afternoon, 2026-11-14. Note the count for a day
  before and a day after the section exists in a real project.
- This repository's own next level-3 unit: its reading guide has no `## Team`; the agent
  must ask.
