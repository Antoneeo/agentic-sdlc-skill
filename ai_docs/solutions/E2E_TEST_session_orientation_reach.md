---
feature: F-075
analysis: ANALYSIS_session_orientation_reach.md
---
# E2E test: What reaches the session

## What changed, in user terms

When a Claude Code session starts, the agent now receives the whole project
orientation, not a 2,000-character preview of a saved file. The orientation starts
with the triage line, the guides and the open workstreams. It says when it is wired
twice for one client and, when other lenses of the family are installed, to choose
the lens. On every prompt, the reminder line also names the lens choice.

## Environment and preconditions

- The packages built from the merged branch, installed with `npm i -g` (all four:
  `@antoneeo/agentic-sdlc-skill`, kb, mkt, course), Claude Code with Python on PATH.
- A project with a mature `ai_docs/` that has several guides and open workstreams:
  this repository works.
- To check the wired-twice note: the orientation hook wired in the user settings
  (the installer does this) AND in the project's `.claude/settings.json`.

## New-behavior scenarios

### S1 — AC1: the orientation is injected whole
Steps: 1. Open a new Claude Code session in the project. 2. Look at the
SessionStart hook output in the transcript.
Expected: no "Output too large … saved to" notice for the orientation. The text
starts with the triage line, then `## Guide router`, then `## Workstream registry`.
Result:

### S2 — AC3: wired twice is said once per copy
Steps: 1. With the hook wired in both user and project settings, start a session.
Expected: each orientation copy ends with a `[note]` saying it is wired 2 times for
one client, naming `.claude/settings.json` and `user settings`, and telling to keep
one. 2. Remove one entry and start a new session: one copy, no note.
Result:

### S3 — AC4: lens line
Steps: 1. With two or more family skills installed, start a session.
Expected: a line under the triage line names the other installed lenses and says to
choose the lens with routing.md above L1. With only one family skill installed: no
such line.
Result:

### S4 — AC5: the per-turn line
Steps: 1. Send any prompt.
Expected: the reminder line ends with "Above L1, with sibling lenses installed:
choose the lens with routing.md and declare it." It is one line.
Result:

### S5 — AC7: worked routing examples
Steps: 1. Open the installed `routing.md`, §2.
Expected: rows for the interface spec for another team, the requirements another
team must build, the guide whose source spec changed, and code diverging from a
supplied spec.
Result:

## Regression scenarios

### R1 — a project without `ai_docs/`
Steps: 1. Start a session in a folder with no docs root.
Expected: the session starts normally; the orientation prints nothing.
Result:

### R2 — `check` notes on wiring
Steps: 1. In a project with no orientation hook anywhere, run `sdlc_check.py check`.
2. Point the hook at a validator path that does not exist and run it again.
Expected: the "without automatic orientation" note the first time, the "validator
that no longer exists" note the second; the exit code is the same both times.
Result:

### R3 — `--hybrid`
Steps: 1. Run `sdlc_check.py orient --hybrid` in a project.
Expected: the last line points at `devpnt_mcp_get_bootstrap`.
Result:

### R4 — a knowledge project
Steps: 1. In a project with `ai_docs/topics/INDEX.md`, start a session with the
kb-agentic hook.
Expected: the orientation is followed by the project-memory line and `## Topic
router`; the whole output is still injected (no "saved to" notice).
Result:

### R5 — `benefit` and the docs site
Steps: 1. Run `sdlc_check.py benefit` and `docs_site.py --root . --open`.
Expected: the same numbers and the same pages as before the merge (review rows,
workstreams, home links).
Result:

## Already covered by automated tests

`test_session_start.py` (order, formats, size on the worst case, stub and hand-written
files, wired-twice cases, lens line), `test_remind.py` (cap 600, the lens duty, every
lens in the checkout), `test_skill_invariants.py` (routing rows), `test_golden_regression.py`
(code, kb, mkt transcripts), the probe `ai_docs/solutions/harness_session_orientation_reach/probe.py`.
