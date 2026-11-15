"""F-097 replay judge, question 1 (FS1, FS2, T7): does a message show every row of
the generated registry, each with its workstream, status and next step as written,
in the registry's order?

Mechanical half of the judgement only. It reports, per registry row, whether the
three cells appear verbatim on one line of the message, and whether those lines come
in the registry's order. Whether the message adds a count, a judgement or a
suggestion, and whether the unit waits, is read by a person.

Exit 0 = the heading is present, every row is found verbatim, in order; exit 1
otherwise.

Usage: python judge_rows.py <audit/handoff.md> <message file>
"""
import sys
from pathlib import Path

BAR = chr(124)
ESC = chr(92) + BAR
HOLD = chr(0)
HEADING = "Open workstreams (audit/handoff.md, as declared):"


def cells(line):
    return [c.strip().replace(HOLD, BAR)
            for c in line.replace(ESC, HOLD).strip().strip(BAR).split(BAR)]


def main():
    registry = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
    message = Path(sys.argv[2]).read_text(encoding="utf-8").splitlines()
    rows = [cells(l) for l in registry
            if l.startswith(BAR) and not l.startswith(BAR + " Workstream")
            and not l.startswith(BAR + "---")]
    rows = [(r[0], r[3], r[5]) for r in rows if len(r) >= 6]
    heading = any(HEADING in line for line in message)
    found, positions = 0, []
    for ws, status, nxt in rows:
        hits = [i for i, line in enumerate(message)
                if ws in line and status in line and nxt in line]
        if hits:
            found += 1
            positions.append(hits[0])
        else:
            print(f"  not verbatim on one line: {ws[:70]}")
    ordered = positions == sorted(positions)
    print(f"heading present: {heading}")
    print(f"registry rows: {len(rows)}; found verbatim (workstream, status, next step "
          f"on one line): {found}; in the registry's order: {ordered}")
    ok = heading and found == len(rows) and ordered and bool(rows)
    print("JUDGE", "GREEN" if ok else "RED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
