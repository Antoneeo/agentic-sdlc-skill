---
feature: F-076
analysis: ANALYSIS_guide_verdict_check.md
---
# E2E test: Guide verdict check before edits

## What changed, in user terms

On Claude Code, in a project with guides, an agent's file edit is now refused until the
session shows the Rule-Zero level with the guide-router verdict (or `Level: L1`) and the
agent has read every guide that verdict names. The refusal is one line telling the agent
how to unblock. Installing the package wires the check for every project on the machine;
removing the hook entry turns it off for good.

## Environment and preconditions

- `@antoneeo/agentic-sdlc-skill` built from the merged branch, installed with `npm i -g`;
  Claude Code with Python on PATH.
- A project with at least one `ai_docs/reference/GUIDE_*.md` (this repository works) and a
  scratch file you may edit (for example `scratch.txt` at the project root).
- After install, `~/.claude/settings.json` holds a `PreToolUse` entry whose command ends
  in `verdict --hook; exit 0`.

## New-behavior scenarios

### S1 — UC1: edit without a verdict is refused
Steps: 1. Open a new session in the project. 2. Ask: "Without declaring anything, append
the word test to scratch.txt."
Expected: the Edit/Write is refused; the agent is shown a line starting `[sdlc verdict]
No guide-router verdict in this session`. The file is unchanged.
Result:

### S2 — UC2: verdict naming an unread guide is refused
Steps: 1. In a new session, ask the agent to write exactly "Level: L2 · router:
GUIDE_release.md → read" and then, without opening that guide, edit scratch.txt.
Expected: refused with a line naming `GUIDE_release.md`. 2. Ask the agent to read the
guide, then retry. Expected: the edit goes through the normal permission flow.
Result:

### S3 — UC3: trivial and no-match declarations pass
Steps: 1. New session: the agent writes "Level: L1" and edits scratch.txt. 2. New session:
the agent writes "Level: L2 · router: no match" and edits scratch.txt.
Expected: both edits proceed (normal permission prompt, if any); no `[sdlc verdict]` line.
Result:

### S4 — UC3: projects without guides are untouched
Steps: 1. Open a session in a project with no `ai_docs/reference/GUIDE_*.md` (or no
`ai_docs/`). 2. Edit any file without declaring anything.
Expected: no refusal.
Result:

### S5 — UC4: opt-out is permanent
Steps: 1. Remove the `PreToolUse` verdict entry from `~/.claude/settings.json`. 2. Run
`npm i -g @antoneeo/agentic-sdlc-skill` again.
Expected: the entry is not re-added (no "Guide-verdict check wired" line).
Result:

### S6 — UC4: a missing validator never blocks
Steps: 1. With the entry wired, rename the installed skill folder
(`~/.claude/skills/agentic-sdlc`) temporarily. 2. In a session, edit scratch.txt.
Expected: the edit proceeds (Python's "can't open file" is not a refusal). 3. Restore
the folder.
Result:

## Regression scenarios

### R1 — the session orientation and the per-turn line are unchanged
Steps: 1. Start a session. 2. Send a prompt.
Expected: the orientation and the `agentic-sdlc:` per-turn line appear as before.
Result:

### R2 — `gate` still blocks protected paths
Steps: 1. Wire `gate --hook --protected "src/auth"` per `ENFORCEMENT.md` §3 in a project
with no IN_PROGRESS analysis. 2. Edit a file under `src/auth/`.
Expected: refused with `[sdlc gate] …` as before.
Result:

### R3 — uninstall
Steps: 1. `npm uninstall -g @antoneeo/agentic-sdlc-skill`. 2. Open `~/.claude/settings.json`.
Expected: if npm ran the uninstaller, the verdict and remind entries are gone with a
"Removed the … hook entry" line each; if not (npm 7+), a left-over verdict entry never
blocks an edit (S6), and a left-over remind entry should be removed by hand.
Result:
