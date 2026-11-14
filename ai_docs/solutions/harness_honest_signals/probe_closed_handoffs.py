"""F-096 probe, report point 3: does `validate` name a workstream source whose
own `status:` declares the work closed?

Replays the recorded case (case_registry_40.md, section B: the 43 HANDOFF
frontmatters of 2026-11-14) as a throwaway docs tree and runs the validator on
it. Exit 0 = every source that declares itself closed is named exactly once;
exit 1 = some are not.

Usage: python probe_closed_handoffs.py <path to sdlc_check.py>
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLOSED = ("COMPLETED", "DONE", "CANCELLED")
NL = chr(10)


def frontmatters(case_text):
    """[(label, yaml block text)] for every `### Filone-NN` block of section B."""
    section_b = case_text.split("## Sezione B", 1)[1]
    pattern = r"^### (Filone-\d+)[^\n]*\n+```yaml\n(---\n.*?\n---)\n```"
    return [(m.group(1), m.group(2)) for m in re.finditer(pattern, section_b, re.S | re.M)]


def declared_closed(block):
    m = re.search(r'^status:\s*"?([A-Za-z_]+)', block, re.M)
    return bool(m) and m.group(1).upper() in CLOSED


def is_source(block):
    """A file with no `workstream:` is not a registry source (FS4)."""
    return bool(re.search(r"^workstream:", block, re.M))


def main():
    checker = Path(sys.argv[1]).resolve()
    text = (HERE / "case_registry_40.md").read_text(encoding="utf-8").replace("\r\n", NL)
    blocks = frontmatters(text)
    assert len(blocks) == 43, f"expected 43 frontmatters in the case, parsed {len(blocks)}"
    with tempfile.TemporaryDirectory() as tmp:
        audit = Path(tmp) / "ai_docs" / "audit"
        audit.mkdir(parents=True)
        closed, not_sources = [], []
        for label, block in blocks:
            name = f"HANDOFF_{label.replace('-', '_')}.md"
            (audit / name).write_text(block + NL + "# HANDOFF" + NL, encoding="utf-8")
            if declared_closed(block):
                (closed if is_source(block) else not_sources).append(name)
        subprocess.run([sys.executable, str(checker), "index", "--root", tmp],
                       capture_output=True, text=True)
        res = subprocess.run([sys.executable, str(checker), "validate", "--root", tmp],
                             capture_output=True, text=True)
        lines = (res.stdout + res.stderr).splitlines()
    named = [n for n in closed
             if sum(n in line and "declares status" in line for line in lines) == 1]
    print(f"files in the case: {len(blocks)}")
    print(f"sources declaring themselves closed (status starts with {'/'.join(CLOSED)}): "
          f"{len(closed)}")
    print(f"same status but no `workstream:`, so not a source: {len(not_sources)}")
    print(f"named by validate, each exactly once: {len(named)}")
    for n in closed:
        if n not in named:
            print(f"  not named: {n}")
    return 0 if closed and len(named) == len(closed) else 1


if __name__ == "__main__":
    sys.exit(main())
