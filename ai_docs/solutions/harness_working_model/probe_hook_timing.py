"""F-085 probe (T5): what the recall hook costs per edit.

Claim probed (ANALYSIS_working_model.md, T5 and the Ceremony cost row on latency): the
hook, run as Claude Code runs it (a new Python process per edit, payload on stdin),
answers within a fraction of a second on the paths an edit actually takes:
  silent-outside   a file outside any docs project (every edit in an ungoverned repo)
  silent-unbound   a file of a governed project that no open constraint binds
  recall           a bound file, session declared L3 and read the unit (context emitted)
Each path runs 5 times; the probe prints the best and the median, in seconds.

Usage (repository root): python -I probe_hook_timing.py
       python -I probe_hook_timing.py --red
"""
import json
import pathlib
import statistics
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parents[3]
ENTRY = ROOT / "skills" / "agentic-sdlc-skill" / "scripts" / "sdlc_check.py"
ANALYSIS = """---
id: F-901
feature: Fixture
status: IN_PROGRESS
level: L3
domain: code
start_date: 2026-10-27
---
# Feature Analysis: fixture

## Use Cases / User Needs

- **UC1 (Agent)** — edits `src/app/core.py`.

## Impact

### Preservation constraints

| id | bound to | callers | must stay true | evidence |
|---|---|---|---|---|
| P1 | `src/app/core.py` | none outside the file | save keeps writing one row | grep |

## Security and Threat Model

- **T1 X.** y.
"""


def say(text):
    return json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}})


def read(path):
    return json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Read", "input": {"file_path": str(path)}}]}})


def build(base, level="L3"):
    proj = base / "proj"
    (proj / "ai_docs" / "solutions").mkdir(parents=True)
    analysis = proj / "ai_docs" / "solutions" / "ANALYSIS_fixture.md"
    analysis.write_text(ANALYSIS, encoding="utf-8")
    transcript = base / "t.jsonl"
    transcript.write_text(say(f"Level: {level} · router: no match") + "\n" + read(analysis) + "\n",
                          encoding="utf-8")
    return proj, transcript


def run(target, transcript):
    payload = json.dumps({"tool_name": "Edit", "hook_event_name": "PreToolUse",
                          "transcript_path": str(transcript),
                          "tool_input": {"file_path": str(target), "new_string": "x"}})
    t0 = time.perf_counter()
    r = subprocess.run([sys.executable, str(ENTRY), "constraints", "--hook"], input=payload,
                       capture_output=True, text=True, encoding="utf-8", cwd=str(target.anchor))
    return time.perf_counter() - t0, r.returncode, r.stdout.strip()


def paths(base, proj):
    return {"silent-outside": base / "elsewhere" / "x.py",
            "silent-unbound": proj / "src" / "app" / "free.py",
            "recall": proj / "src" / "app" / "core.py"}


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as d:
        base = pathlib.Path(d)
        if sys.argv[1:] == ["--red"]:
            proj, t = build(base / "l3")
            p = paths(base / "l3", proj)
            assert run(p["recall"], t)[2], "a bound edit at L3 must emit context"
            assert not run(p["silent-unbound"], t)[2]
            assert not run(p["silent-outside"], t)[2]
            proj1, t1 = build(base / "l1", "L1")          # negate the level: must go silent
            assert not run(paths(base / "l1", proj1)["recall"], t1)[2]
            print("red/green OK")
            sys.exit(0)
        proj, t = build(base)
        for name, target in paths(base, proj).items():
            runs = [run(target, t) for _ in range(5)]
            secs = [s for s, _, _ in runs]
            assert all(rc == 0 for _, rc, _ in runs)
            print(f"{name}: best {min(secs):.2f} s, median {statistics.median(secs):.2f} s, "
                  f"context {'yes' if runs[0][2] else 'no'}")
