"""F-070 probe, A10 and P3: undo the README change in memory and compare with git.

For each package README: the F-057 block in the working tree must equal its text at
the base ref, byte for byte (A10); taking out the whats-new bounds and putting the
block back where it was must give the base ref's file exactly (P3: nothing else
moved). Usage, from the repository root:  python <this file> [base-ref]
"""
import subprocess
import sys
from pathlib import Path

BASE = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
READMES = ["README.md", "distributions/kb-agentic-skill/README.md",
           "distributions/mkt-agentic-sdlc/README.md", "distributions/course-creator/README.md"]
BOUNDS = ["<!-- whats-new:begin -->", "<!-- whats-new:end -->"]


def block(lines):
    if "## Shared project memory" not in lines:
        return None, None
    a = lines.index("## Shared project memory")
    b = next(i for i in range(a, len(lines)) if lines[i].startswith("Vendoring requires all three files"))
    return a, lines[a:b + 1]


failed = False
for rel in READMES:
    base = subprocess.run(["git", "show", f"{BASE}:{rel}"], capture_output=True, check=True).stdout
    base = base.decode("utf-8").replace("\r\n", "\n").split("\n")
    now = Path(rel).read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n")
    a0, b0 = block(base)
    a1, b1 = block(now)
    same_block = b0 == b1
    # Undo: drop the bounds and the blank after them, put the block back at the top.
    undo = list(now)
    i = undo.index(BOUNDS[0])
    assert undo[i + 1] == BOUNDS[1] and undo[i + 2] == "", rel
    del undo[i:i + 3]
    if b1:
        a = undo.index("## Shared project memory")
        del undo[a:a + len(b1) + 1]
        undo[a0:a0] = b1 + ["", ""]
    ok = same_block and undo == base
    failed = failed or not ok
    print(f"[{'ok' if ok else 'FAIL'}] {rel}: block {'identical' if same_block else 'DIFFERS'}"
          f"{'' if b1 is None else f' (line {a0 + 1} -> {a1 + 1})'}; undone equals {BASE}: {undo == base}")
sys.exit(1 if failed else 0)
