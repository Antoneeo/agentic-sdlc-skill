# Live hook probe — 2026-10-27 (Action Plan 1)

Probe: `probe_hook_live.py` (red/green offline with `--red`). Client: Claude Code desktop
app, Windows 11, session permission mode auto. Three PreToolUse entries wired in
`.claude/settings.json` (matcher `Edit|Write|MultiEdit|NotebookEdit`) for the probe only,
then removed; the file is back to its committed content.

| Case | Wiring | Observed | Verdict |
|---|---|---|---|
| C1 red | probe `--entry ctx; exit 0`, mode silent | both probe entries logged the call, printed nothing; no context reached the agent | red as expected |
| C1 green | same, mode context | the agent received `PreToolUse:Edit hook additional context: F085-LIVE-PROBE: additionalContext delivered`; the edit was applied | **FS6 output form accepted** — no PostToolUse fallback |
| C2 red | probe `--entry nosuffix`, mode block | edit refused, stderr shown to the agent as a hook error | red as expected |
| C2 green | `sdlc_check.py constraints --hook 2>>log; exit 0` (subcommand absent today) | argparse error captured in the log; the edit was applied | **T2 holds**: an older validator never blocks an edit |

Findings beyond the two claims:

- Hooks are re-read mid-session: a settings edit took effect on the next tool call.
- The hook process runs in the session's **current** working directory, which a Bash
  `cd` moves. With relative paths every entry failed to find its script; the unsuffixed
  one exited 2 and blocked an unrelated edit (an accidental C2 red). The installer
  already writes absolute validator paths, so wiring is immune; root resolution is not
  (`find_project_root` walks up from cwd). FS6 therefore resolves the project from the
  edited file's path.
- Not observable under auto mode: whether a decision-less object leaves the permission
  prompt unchanged. The JSON carries no `permissionDecision` (asserted by the probe and,
  from step 3, by `test_constraints.py`); Claude Code's documented behaviour is to keep
  the normal permission flow when no decision is given.
