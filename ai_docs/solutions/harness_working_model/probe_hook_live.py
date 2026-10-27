"""F-085 live probe (Action Plan 1): does Claude Code accept FS6's output form, and
does an absent subcommand leave edits unblocked?

Claims probed (ANALYSIS_working_model.md, FS6 and T2):
  C1 a PreToolUse hook that prints `hookSpecificOutput` holding only `hookEventName`
     and `additionalContext` (no `permissionDecision`) delivers that context to the
     agent and the edit proceeds.
  C2 a hook command ending in `; exit 0` whose program exits 2 (the shape of an older
     skill with no `constraints` subcommand) does not block the edit; without the
     suffix the same exit 2 does (red).

Wired as PreToolUse commands for the duration of the probe, one per entry:
  python -I <this file> --entry ctx; exit 0     context on the scratch file (C1)
  python -I <this file> --entry nosuffix        exit 2 on the scratch file (C2 red)
The real absent subcommand (`sdlc_check.py constraints --hook; exit 0`) is wired beside
them for C2 green. The behaviour is chosen by the first word of `probe_mode.txt` next
to this file (silent | context | block); each invocation appends one line to
`live_probe.log.jsonl` next to this file. Both files are deleted after the probe.

Usage: python -I probe_hook_live.py --entry ctx|nosuffix   (stdin: hook payload)
       python -I probe_hook_live.py --red
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
SCRATCH = "f085_probe_scratch.txt"
MARKER = "F085-LIVE-PROBE: additionalContext delivered"


def decide(entry, mode, payload):
    """Return (stdout, stderr, exit code) for one hook invocation."""
    path = str((payload.get("tool_input") or {}).get("file_path", ""))
    if not path.replace("\\", "/").endswith(SCRATCH):
        return "", "", 0
    if entry == "ctx" and mode == "context":
        out = {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                      "additionalContext": MARKER}}
        return json.dumps(out), "", 0
    if entry == "nosuffix" and mode == "block":
        return "", "F085 probe: simulated absent subcommand (exit 2)", 2
    return "", "", 0


def main(entry):
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        payload = {}
    try:
        mode = (HERE / "probe_mode.txt").read_text(encoding="utf-8").split()[0]
    except (OSError, IndexError):
        mode = "silent"
    out, err, code = decide(entry, mode, payload)
    with open(HERE / "live_probe.log.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "entry": entry, "mode": mode, "event": payload.get("hook_event_name"),
            "tool": payload.get("tool_name"),
            "file": str((payload.get("tool_input") or {}).get("file_path", "")),
            "emitted": bool(out), "exit": code}) + "\n")
    if out:
        print(out)
    if err:
        print(err, file=sys.stderr)
    return code


if __name__ == "__main__":
    if sys.argv[1:] == ["--red"]:
        hit = {"tool_input": {"file_path": "C:\\x\\" + SCRATCH}}
        miss = {"tool_input": {"file_path": "other.py"}}
        assert decide("ctx", "silent", hit) == ("", "", 0)          # red: no output
        out, _, code = decide("ctx", "context", hit)
        spec = json.loads(out)["hookSpecificOutput"]
        assert code == 0 and set(spec) == {"hookEventName", "additionalContext"}, spec
        assert "permissionDecision" not in out
        assert decide("ctx", "context", miss) == ("", "", 0)        # other files: silent
        assert decide("nosuffix", "block", hit)[2] == 2
        assert decide("nosuffix", "context", hit)[2] == 0
        assert decide("ctx", "block", hit)[2] == 0
        print("red/green OK")
        sys.exit(0)
    sys.exit(main(sys.argv[sys.argv.index("--entry") + 1]))
