#!/usr/bin/env python3
"""F-076 probe: replay the field case -- an agent edits with no guide-router verdict
declared and a matching guide unread -- through the PreToolUse hook surface.

A field case is flagged when the hook prints a JSON `permissionDecision: "deny"` on
stdout (exit 0). Anything else -- silence, a usage error -- leaves the edit unflagged.
Cases, each on a throwaway project that has one guide (`GUIDE_release.md`):
  P1  field case: no verdict, guide never read                -> flagged
  P2  verdict names the guide, the guide was Read             -> not flagged
  P3  verdict names the guide, the guide was never read       -> flagged
  P4  `Level: L1` declared, no router verdict (L1 exempt)     -> not flagged
  P5  the existing `gate --hook` on P1 (no --protected)       -> not flagged (why it misses)
  P6  a real recorded transcript (--transcript, optional): this repo's guides, a
      session that declared its verdict and read the guides  -> not flagged
  P7  the wired command form with a missing validator, under each shell found
      (Git Bash, PowerShell)                                 -> exit 0, never 2
Exit 0 = every case as expected; exit 1 = some case red (printed).

    python ai_docs/solutions/harness_guide_verdict_check/probe.py [--transcript PATH]
"""
import json, subprocess, sys, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
ENTRY = REPO / "skills/agentic-sdlc-skill/scripts/sdlc_check.py"


def line(kind, **block):
    return json.dumps({"type": "assistant", "message": {"role": "assistant",
                       "content": [dict(type=kind, **block)]}})


def text(t):
    return line("text", text=t)


def tool(name, **inp):
    return line("tool_use", id="toolu_x", name=name, input=inp)


def project(tmp):
    ref = tmp / "ai_docs" / "reference"
    ref.mkdir(parents=True)
    (ref / "GUIDE_release.md").write_text("---\ndescription: release\nstatus: CURRENT\n---\n# G\n",
                                          encoding="utf-8")
    (tmp / "src").mkdir()
    return tmp


def run(root, transcript_lines, cmd=("verdict", "--hook"), transcript=None):
    tp = transcript
    if tp is None:
        tp = root / "t.jsonl"
        tp.write_text("\n".join(transcript_lines) + "\n", encoding="utf-8")
    payload = {"session_id": "s", "transcript_path": str(tp), "cwd": str(root),
               "hook_event_name": "PreToolUse", "tool_name": "Edit",
               "tool_input": {"file_path": str(root / "src" / "app.py"),
                              "old_string": "a", "new_string": "b"}}
    r = subprocess.run([sys.executable, str(ENTRY), *cmd], input=json.dumps(payload),
                       capture_output=True, text=True, encoding="utf-8", cwd=str(root))
    try:
        out = json.loads(r.stdout)
        return (out.get("hookSpecificOutput") or {}).get("permissionDecision") == "deny"
    except ValueError:
        return False


FIELD = [text("I'll fix the build script."), tool("Bash", command="ls src")]
CASES = [
    ("P1 field case", FIELD, True, ("verdict", "--hook")),
    ("P2 verdict + guide read", [text("Level: L2 · router: GUIDE_release.md → read"),
                                 tool("Read", file_path="ai_docs/reference/GUIDE_release.md")],
     False, ("verdict", "--hook")),
    ("P3 verdict, guide unread", [text("Level: L2 · router: `GUIDE_release.md` → read")],
     True, ("verdict", "--hook")),
    ("P4 L1 declared", [text("Level: L1 — typo fix.")], False, ("verdict", "--hook")),
    ("P5 gate --hook on P1", FIELD, False, ("gate", "--hook")),
]

red = 0
for label, lines, want, cmd in CASES:
    with tempfile.TemporaryDirectory() as d:
        got = run(project(Path(d)), lines, cmd)
    red += got != want
    print("%-28s flagged=%-5s expected=%-5s %s" % (label, got, want, "GREEN" if got == want else "RED"))

# P7: the wired command form must exit 0 even when the validator cannot run `verdict`
# (missing file, or an older version whose argparse rejects it) -- exit 2 would block.
import shutil
# full path from which(): on Windows a bare "bash" resolves to WSL's System32 shim
shells = [[shutil.which(s[0])] + s[1:] for s in (["bash", "-c"],
                                                 ["powershell", "-NoProfile", "-Command"])
          if shutil.which(s[0])]
for sh in shells:
    wired = '%s "%s" verdict --hook; exit 0' % (Path(sys.executable).as_posix(),
                                               (REPO / "no_such_validator.py").as_posix())
    # red control: the unwrapped form fails -- 2 under bash (a PreToolUse block);
    # PowerShell -Command reports a failed native command as 1
    bare = wired[:-len("; exit 0")]
    for label, cmd, want in (("P7 bare form, ", bare, "!=0"), ("P7 wired form, ", wired, 0)):
        code = subprocess.run(sh + [cmd], input="{}", capture_output=True, text=True).returncode
        ok = code != 0 if want == "!=0" else code == want
        red += not ok
        print("%-28s exit=%-9s expected=%-5s %s" % (label + Path(sh[0]).stem, code, want,
                                                    "GREEN" if ok else "RED"))

if "--transcript" in sys.argv:
    tp = Path(sys.argv[sys.argv.index("--transcript") + 1])
    got = run(REPO, None, transcript=tp)
    red += got
    print("%-28s flagged=%-5s expected=%-5s %s" % ("P6 real transcript", got, False,
                                                  "RED" if got else "GREEN"))
sys.exit(1 if red else 0)
