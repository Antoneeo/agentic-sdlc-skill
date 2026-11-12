#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-094 probe: does the verdict hook accept a guide that was read only in part?

Replays the field shapes found in real transcripts (field_scan.txt) against the
verdict hook of the checkout this file sits in:

  F1  Read offset=1 limit=130 of a 225-line guide (GUIDE_release.md, field case)
  F2  Bash `head -30 GUIDE_x.md`
  F3  Grep with path=GUIDE_x.md
  F4  Read without limit of a 2500-line guide (the client stops at 2000 lines)
  F5  Read offset=30 (the first 29 lines skipped)

Each must be REFUSED (a reason returned). Controls that must PASS (None):

  C1  Read without offset/limit of the 225-line guide
  C2  Read of the 2500-line guide in chunks 1-2000, 2001-2500
  C3  Bash `cat GUIDE_x.md`
  C4  Codex Get-Content -TotalCount 225 of the 225-line guide

Exit 0 when every expectation holds, 1 otherwise.

    python ai_docs/solutions/harness_whole_guide_read/probe.py
"""
import json
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "skills" / "agentic-sdlc-skill" / "scripts"))
import sdlc_core  # noqa: E402

SHORT, LONG = "GUIDE_release.md", "GUIDE_long.md"


def say(text):
    return json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}})


def call(name, **inp):
    return json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "id": "t", "name": name, "input": inp}]}})


def codex(cmd, root):
    meta = json.dumps({"type": "session_meta", "payload": {"cwd": str(root)}})
    item = json.dumps({"type": "response_item", "payload": {
        "type": "function_call", "name": "exec_command", "arguments": json.dumps({"cmd": cmd})}})
    return [meta, item]


def verdict(root, lines, guide):
    t = root / "t.jsonl"
    t.write_text("\n".join([say("Level: L2 · router: %s -> read" % guide)] + lines) + "\n",
                 encoding="utf-8")
    return sdlc_core.verdict_reason({"tool_name": "Edit", "transcript_path": str(t),
                                     "tool_input": {"file_path": str(root / "src" / "a.py")}},
                                    root)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        ref = root / "ai_docs" / "reference"
        ref.mkdir(parents=True)
        (root / "src").mkdir()
        (ref / SHORT).write_text("".join("line %d\n" % i for i in range(1, 226)), encoding="utf-8")
        (ref / LONG).write_text("".join("line %d\n" % i for i in range(1, 2501)), encoding="utf-8")
        s, l = str(ref / SHORT), str(ref / LONG)
        cases = [
            ("F1 Read 1-130 of 225", [call("Read", file_path=s, offset=1, limit=130)], SHORT, True),
            ("F2 head -30", [call("Bash", command="head -30 " + s)], SHORT, True),
            ("F3 Grep on the guide", [call("Grep", pattern="x", path=s)], SHORT, True),
            ("F4 Read 2500 lines, no limit", [call("Read", file_path=l)], LONG, True),
            ("F5 Read offset=30", [call("Read", file_path=s, offset=30)], SHORT, True),
            ("C1 Read whole", [call("Read", file_path=s)], SHORT, False),
            ("C2 Read chunks to the end", [call("Read", file_path=l, offset=1, limit=2000),
                                           call("Read", file_path=l, offset=2001, limit=2000)], LONG, False),
            ("C3 cat", [call("Bash", command="cat " + s)], SHORT, False),
            ("C4 Codex -TotalCount 225", codex("Get-Content -TotalCount 225 '%s'" % s, root), SHORT, False),
        ]
        ok = True
        for name, lines, guide, refused in cases:
            reason = verdict(root, lines, guide)
            good = (reason is not None) == refused
            ok &= good
            print("%-4s %-32s expected %-7s got %s" % ("ok" if good else "FAIL", name,
                  "refuse" if refused else "pass", "refuse" if reason else "pass"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
