---
feature: F-093
analysis: ANALYSIS_family_hook_wiring.md
---
# E2E test: per-turn reminder on single- and multi-lens installs

## What changed, in user terms

Installing kb-agentic or mkt-agentic-sdlc now wires the one-line reminder at each
prompt, as their ENFORCEMENT.md says. With several lenses installed there is still one
reminder line per prompt: the first lens that wired it keeps it, and that line now names
every installed lens with its domain, so the agent can pick the one that fits the task.

## Environment and preconditions

- Packages packed from the merged branch, installed with `npm i -g` on a machine with
  Claude Code and Python on PATH.
- To test on a clean profile without touching the real one: set `CLAUDE_CONFIG_DIR` and
  `AGENTIC_SDLC_KB_ROOT` to empty temp folders before installing.

## New-behavior scenarios

### S1 — kb alone gets the reminder
Steps: 1. Clean profile, install only kb-agentic. 2. Open `settings.json` in the profile.
Expected: `UserPromptSubmit` has one entry running `kb-agentic\scripts\sdlc_check.py" remind`;
the install printed "Per-turn protocol reminder wired". A new session shows the line
starting `kb-agentic:` at each prompt.
Result:

### S2 — marketing alone gets the reminder
Same as S1 with mkt-agentic-sdlc; the entry names `mkt_check.py" remind`.
Result:

### S3 — several lenses, one line
Steps: 1. Clean profile: install kb-agentic, then agentic-sdlc.
Expected: one `UserPromptSubmit` remind entry (kb's). Reversed order: one entry (agentic-sdlc's).
Result:

### S4 — the line names the installed lenses
Steps: 1. After S3, open a session in any folder and send a prompt.
Expected: the reminder ends with "Installed lenses: agentic-sdlc (code), kb-agentic (knowledge).
Above L1, choose the one that governs this work with routing.md, load it and declare it."
Install mkt-agentic-sdlc too: the next prompt lists three lenses, in name order. No new
install step is needed: the line reads the installed skills at each prompt.
Result:

## Regression scenarios

### R1 — removal is never undone
Steps: 1. After S1, delete the remind entry from `settings.json`. 2. Reinstall kb-agentic.
Expected: no remind entry comes back.
Result:

### R2 — uninstall removes only its own entry
Steps: 1. After S3 (kb's entry), uninstall agentic-sdlc. 2. Then uninstall kb-agentic.
Expected: step 1 leaves kb's entry; step 2 removes it. Orientation entries follow the
same rule as before.
Result:

### R4 — a single lens keeps its old line
Steps: after S1 (kb alone), send a prompt.
Expected: the line ends "Above L1, with sibling lenses installed: choose the lens with
routing.md and declare it." exactly as before; no lens list.
Result:

### R3 — the real profile is untouched by a test install
Run S1–S3 only with the two environment variables set. Expected: the real
`~/.claude/settings.json` and `~/.agentic-sdlc/` unchanged.
Result:
