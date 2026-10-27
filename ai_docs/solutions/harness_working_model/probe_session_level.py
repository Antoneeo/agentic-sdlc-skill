"""F-085 probe: can the recall hook tell, from the transcript, which unit a session
works on and which level it declared?

Claims probed (ANALYSIS_working_model.md, Functional Spec FS6):
  C1 the existing verdict regex (`sdlc_core._VERDICT_TRIVIAL_RE`) recognises only an
     English "Level: L1" line; an Italian declaration ("Livello L3") is invisible to it.
  C2 a declaration regex that accepts the level word in the languages the agent
     actually writes, followed by L1/L2/L3, finds the last declaration in a real
     transcript.
  C3 the unit a session works on is visible as an ANALYSIS or REQUEST path in the
     input of a tool_use the session ran.

Usage: python -I probe_session_level.py <transcript.jsonl>
       python -I probe_session_level.py --red
"""
import json
import pathlib
import re
import sys

# The verdict hook's own regex, imported rather than copied (it is what C1 is about).
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]
                       / "skills" / "agentic-sdlc-skill" / "scripts"))
from sdlc_core import _VERDICT_TRIVIAL_RE as OLD_TRIVIAL  # noqa: E402
# C2, anchored: a declaration is a LINE that opens with the level word, in the form
# Rule Zero prescribes — "Level: L2 · router: ..." for L2/L3, while "L1 declares the
# level alone" (SKILL.md Rule Zero), so an L1 line needs no router. A level quoted
# mid-sentence is prose.
_LEAD = r"^[\s>*_`-]*(?:level|livello|niveau|nivel|stufe)\b[\s*_`:·-]*(?:è\s+)?L"
DECL = re.compile(_LEAD + r"(?:(1)\b|([23])\b(?=[^\n]*\brouter\b))", re.I | re.M)
UNIT_PATH = re.compile(r"(?:ANALYSIS|REQUEST|HANDOFF)_([A-Za-z0-9_-]+)\.md")
# W4 (design review): reading the unit's ANALYSIS, request record or handoff counts
# too, so an implementation session that edits only code still gets the recall. The
# implementation keeps only units OPEN in this tree, so a study read of a closed
# unit's analysis never arms it.
WRITERS = {"Write", "Edit", "MultiEdit", "NotebookEdit", "Read"}


def scan(lines):
    old_hits, decls, units = 0, [], []
    for raw in lines:
        try:
            entry = json.loads(raw)
        except ValueError:
            continue
        if entry.get("type") != "assistant":
            continue
        for block in (entry.get("message") or {}).get("content") or []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text":
                text = block.get("text", "")
                old_hits += len(OLD_TRIVIAL.findall(text))
                decls += [a or b for a, b in DECL.findall(text)]
            elif block.get("type") == "tool_use" and block.get("name") in WRITERS:
                # C3: a Read, Write or Edit of the unit's ANALYSIS, request record or
                # handoff names the unit worked on; a search mentioning it does not.
                # (The implementation keeps only units open in the tree.)
                path = str((block.get("input") or {}).get("file_path", ""))
                units += UNIT_PATH.findall(path)
    return old_hits, decls, units


def synthetic(text, tool_input, tool="Edit"):
    return [json.dumps({"type": "assistant", "message": {"content": [
        {"type": "text", "text": text},
        {"type": "tool_use", "name": tool, "input": tool_input}]}})]


if __name__ == "__main__":
    if sys.argv[1:] == ["--red"]:
        o, d, u = scan(synthetic("Livello L3 · router: nessun match", {"file_path": "x.py"}))
        assert o == 0 and d == ["3"] and u == [], (o, d, u)   # C1 red for old, C2 green
        o, d, u = scan(synthetic("Level: L1 · router: no match",
                                 {"file_path": "ai_docs/solutions/ANALYSIS_a.md"}))
        assert o == 1 and d == ["1"] and u == ["a"], (o, d, u)
        # B3 red cases: prose quoting a level is not a declaration
        o, d, u = scan(synthetic('the hook only sees an English "Level: L1" line', {}))
        assert d == [], d
        o, d, u = scan(synthetic("Level L3 is when the full gate runs.", {}))
        assert d == [], d
        # N1 (round 2): a bare L1 declaration, as Rule Zero prescribes it, after an L3 one
        o, d, u = scan(synthetic("Level: L3 · router: no match", {})
                       + synthetic("Level: L1", {}))
        assert d == ["3", "1"], d
        o, d, u = scan(synthetic("Level: L2", {}))      # L2 without router is not one
        assert d == [], d
        o, d, u = scan(synthetic("resume", {"file_path": "ai_docs/audit/HANDOFF_b.md"}, "Read"))
        assert u == ["b"], u                    # reading the unit's handoff counts (W4)
        o, d, u = scan(synthetic("grep", {"pattern": "ANALYSIS_c.md"}, "Grep"))
        assert u == [], u                       # a search mentioning a name does not
        o, d, u = scan(synthetic("no declaration here", {}))
        assert (o, d, u) == (0, [], []), (o, d, u)
        print("red/green OK")
        sys.exit(0)
    with open(sys.argv[1], encoding="utf-8") as fh:
        o, d, u = scan(fh)
    print(f"old L1 regex hits={o}; declarations={d[-5:]} (last={d[-1] if d else None}); "
          f"units referenced={sorted(set(u))}")
