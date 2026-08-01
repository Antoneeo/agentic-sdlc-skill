#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Opt-in, NON-GATING behavioral eval driver for the mkt-agentic-sdlc skill.

Seeds a scenario's fixture into a temp dir and prints the prompt + pass
criteria for a human/agent to run and self-assess. Stdlib only. It makes NO
model call, NO network request, and spawns NO process -- the deterministic
release gate is the static battery (scripts/test_skill_invariants.py); this
driver is the opt-in behavioral layer that never gates (LLM nondeterminism).

Usage: python run_behavioral.py scenarios/<scenario>.md
"""
import sys
import tempfile
from pathlib import Path

REQUIRED_SECTIONS = ("Setup", "Prompt", "Pass criteria")


def _fail(msg):
    # Fail-fast, bounded message, non-zero exit -- never hang.
    print(f"[eval-error] {msg}")
    sys.exit(2)


def load_scenario(path):
    """Parse a scenario .md into {id, expected, setup, prompt, pass_criteria}.
    Fail-fast on malformed input."""
    p = Path(path)
    if not p.is_file():
        _fail(f"scenario not found: {path}")
    text = p.read_text(encoding="utf-8-sig", errors="replace")
    if not text.startswith("---"):
        _fail(f"missing '---' frontmatter in {path}")
    parts = text.split("---", 2)
    if len(parts) < 3:
        _fail(f"unterminated frontmatter in {path}")
    front_raw, body = parts[1], parts[2]
    front = {}
    for line in front_raw.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            front[k.strip()] = v.strip()
    if "id" not in front:
        _fail(f"frontmatter missing 'id' in {path}")
    sections = {}
    cur, buf = None, []
    for line in body.splitlines():
        if line.startswith("## "):
            if cur is not None:
                sections[cur] = "\n".join(buf).strip()
            cur, buf = line[3:].strip(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        sections[cur] = "\n".join(buf).strip()
    for req in REQUIRED_SECTIONS:
        if req not in sections or not sections[req]:
            _fail(f"scenario {path} missing required '## {req}' section")
    return {
        "id": front["id"],
        "expected": front.get("expected", ""),
        "setup": sections["Setup"],
        "prompt": sections["Prompt"],
        "pass_criteria": sections["Pass criteria"],
    }


def _confined(rel):
    """Reject absolute, drive-relative (Windows `C:foo`), or '..'-escaping
    relpaths (fail-closed)."""
    p = Path(rel)
    return not (p.is_absolute() or bool(p.drive) or ".." in p.parts)


def seed(scenario, dest):
    """Write each '## Setup' '- <relpath>: <content>' entry under dest."""
    dest = Path(dest)
    for line in scenario["setup"].splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        rel, _, content = line[2:].partition(":")
        rel = rel.strip()
        if not rel:
            continue
        if not _confined(rel):
            _fail(f"unsafe setup path (absolute or '..'): {rel}")
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.strip(), encoding="utf-8")


def main(argv):
    if len(argv) != 1:
        _fail("usage: run_behavioral.py scenarios/<scenario>.md")
    scenario = load_scenario(argv[0])
    fixture = Path(tempfile.mkdtemp(prefix="mkt_eval_"))
    seed(scenario, fixture)
    print(f"=== Behavioral eval: {scenario['id']} (NON-GATING) ===")
    print(f"Expected: {scenario['expected']}")
    print(f"Seeded fixture: {fixture}")
    print("\n--- Prompt (run this against your agent, cwd = the fixture) ---")
    print(scenario["prompt"])
    print("\n--- Pass criteria (self-assess) ---")
    print(scenario["pass_criteria"])
    print("\n[note] Opt-in behavioral layer; the deterministic release gate is "
          "the static battery (test_skill_invariants.py). Model nondeterminism "
          "is why this never gates.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
