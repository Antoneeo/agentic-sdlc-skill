"""F-099 replay 2: drafting-time restrictions and the T1 counter-case, old doctrine vs new.
Usage: python build_replay2.py [base-ref]"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = sys.argv[1] if len(sys.argv) > 1 else "948414c9"


def old(rel):
    return subprocess.run(["git", "show", f"{BASE}:{rel}"], cwd=ROOT, capture_output=True,
                          text=True, encoding="utf-8", check=True).stdout.replace("\r\n", "\n")


def new(rel):
    return (ROOT / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


def between(text, start, end):
    i = text.index(start)
    j = text.index(end, i + len(start)) if end else len(text)
    return text[i:j].rstrip() + "\n"


def method(read):
    skill = read("skills/agentic-sdlc-skill/SKILL.md")
    vision = read("skills/agentic-sdlc-skill/vision.md")
    line = [ln for ln in skill.splitlines() if ln.startswith("- **Protect the Vision:**")][0]
    parts = [line + "\n", between(vision, "## What a Vision IS", "\nFour consequences")]
    if "## 8. Downstream" in vision:
        parts.append(between(vision, "## 8. Downstream", None))
    return "\n".join(parts)


CASE = """## Feature Vision: Shared checklists (APPROVED)
North star (owner): "A person shares a checklist with viewers, who follow it item by item without
asking the owner anything, and the checklist stays the owner's."
Invariant - a shared checklist stays the owner's. Question: can a viewer edit the checklist, delete it
or copy it into their own workspace? If no, admitted. If yes, out. What a viewer needs to
follow the checklist is not protected: they see every item and its notes.
Success signal: viewers finish a shared checklist without messaging the owner (baseline: 40% of
viewers message the owner at least once).

## Request record
R1 (owner): "viewers must be able to follow a shared checklist; they must never be able to change
or take it."

## Threat model (draft)
- T1 a viewer copies the checklist - mitigation: copy refused, editor closed to viewers.
- T2 a stolen session exports checklists in bulk - mitigation: to be decided.

## Draft restrictions from the previous pass (to finalise)
- D1 A viewer cannot edit, delete or copy the checklist.
- D2 No internal item identifier appears in any page, export or error message shown to a viewer.
- D3 Exporting a checklist asks the viewer to sign in again.
- D4 A viewer sees only the current item.
"""

TASK = """You are the author of the design for the unit below (a significant change). The
previous drafting pass left four restrictions. Finalise them for the Interface Contract and
the threat model, following the method excerpt at the end.

Write, in English, at most 350 words: for each of D1-D4, keep / change / drop, with the
source it rests on and one line of reason; then any question you bring to the owner.
Use only the material given.
"""

for name, read in (("old", old), ("new", new)):
    text = TASK + "\n# UNIT MATERIAL\n\n" + CASE + "\n# THE METHOD YOU WORK UNDER\n\n" + method(read)
    (HERE / "replay2" / f"prompt_{name}.md").write_text(text, encoding="utf-8")
    print(name, len(text))
