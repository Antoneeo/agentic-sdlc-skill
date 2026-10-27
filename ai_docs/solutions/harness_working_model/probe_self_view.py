"""F-085 probe: the view of this unit's own ANALYSIS (FS Acceptance).

Claim probed: `constraints --unit F-085` lists every id'd item (UC1-UC6, FS1-FS11,
T1-T8) and every P row (P1-P10) of ANALYSIS_working_model.md, and ends with the fixed
sentence naming only `## Interface Contract`.

Usage (repository root): python -I probe_self_view.py
       python -I probe_self_view.py --red
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
ENTRY = ROOT / "skills" / "agentic-sdlc-skill" / "scripts" / "sdlc_check.py"
EXPECTED = ([f"UC{n}" for n in range(1, 7)] + [f"FS{n}" for n in range(1, 12)]
            + [f"T{n}" for n in range(1, 9)] + [f"P{n}" for n in range(1, 11)])


def check(out):
    ids = {m.group(1) for m in re.finditer(r"^((?:UC|FS|T|P)\d+) — ", out, re.M)}
    missing = sorted(set(EXPECTED) - ids)
    last = out.strip().splitlines()[-1] if out.strip() else ""
    sentence_ok = last.endswith("read in full: `## Interface Contract`.")
    return missing, sentence_ok


if __name__ == "__main__":
    if sys.argv[1:] == ["--red"]:
        assert check("UC1 — x\nThis view ... ANALYSIS.") == (sorted(set(EXPECTED) - {"UC1"}), False)
        full = "\n".join(f"{i} — s — h:1" for i in EXPECTED)
        assert check(full + "\n... read in full: `## Interface Contract`.") == ([], True)
        print("red/green OK")
        sys.exit(0)
    r = subprocess.run([sys.executable, str(ENTRY), "constraints", "--root", str(ROOT),
                        "--unit", "F-085"], capture_output=True, text=True, encoding="utf-8")
    missing, sentence_ok = check(r.stdout)
    print(f"exit={r.returncode} missing={missing} sentence_names_only_interface_contract={sentence_ok}")
    sys.exit(0 if r.returncode == 0 and not missing and sentence_ok else 1)
