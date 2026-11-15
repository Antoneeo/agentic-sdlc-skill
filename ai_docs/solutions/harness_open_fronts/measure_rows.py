"""F-097 cost figure, question 1: how many characters the opening message of an L3
unit gains when it shows the registry's rows (workstream, status, next step).

Reads a generated `audit/handoff.md` and prints the row count and the size of that
three-column projection, one row per line. A measurement, not a check: exit 0.

Usage: python measure_rows.py <handoff.md> [<handoff.md> ...]
"""
import sys
from pathlib import Path

BAR = chr(124)
ESC = chr(92) + BAR
HOLD = chr(0)


def cells(line):
    return [c.strip().replace(HOLD, BAR)
            for c in line.replace(ESC, HOLD).strip().strip(BAR).split(BAR)]


def main():
    for arg in sys.argv[1:]:
        lines = Path(arg).read_text(encoding="utf-8").splitlines()
        rows = [cells(l) for l in lines
                if l.startswith(BAR) and not l.startswith(BAR + " Workstream")
                and not l.startswith(BAR + "---")]
        shown = [f"- {r[0]} · {r[3]} · {r[5]}" for r in rows if len(r) >= 6]
        total = sum(len(s) + 1 for s in shown)
        longest = max((len(s) for s in shown), default=0)
        print(f"{arg}: rows {len(shown)}; shown as 'workstream · status · next step': "
              f"{total} chars; longest row {longest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
