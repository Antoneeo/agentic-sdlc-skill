"""F-085 probe: does the Impact table already bind files to constraint ids?

Claim probed (ANALYSIS_working_model.md, FS4): in existing ANALYSIS files, the rows of
the `## Impact` table name a file in backticks in their first cell and cite the ids
(UC/FS/T...) that file serves, so a file can be mapped to its constraints without new
writing. Counts, per document: table rows naming a path, and how many of them cite at
least one id.

Usage: python -I probe_impact_bridge.py <ANALYSIS.md> [...]
       python -I probe_impact_bridge.py --red
"""
import re
import sys

ID = re.compile(r"\b(?:UC|FS|IC|T|SR|P|AC)-?\d+\b")
PATH_CELL = re.compile(r"^\|\s*`([^`]+\.[A-Za-z0-9]+)`")


def bridge(text):
    in_impact, rows, with_ids = False, 0, 0
    for line in text.splitlines():
        if line.startswith("## "):
            in_impact = line[3:].strip().lower().startswith("impact")
            continue
        if in_impact and PATH_CELL.match(line):
            rows += 1
            cells = line.split("|")[2:]
            with_ids += bool(ID.search("|".join(cells)))
    return rows, with_ids


if __name__ == "__main__":
    if sys.argv[1:] == ["--red"]:
        doc = "## Impact\n\n| File | Change | Why |\n|---|---|---|\n| `a.py` | MODIFY | tidy |\n"
        assert bridge(doc) == (1, 0), bridge(doc)
        doc2 = doc + "| `b.py` | ADD | FS3, T1 |\n## Security\n| `c.py` | x | FS1 |\n"
        assert bridge(doc2) == (2, 1), bridge(doc2)
        print("red/green OK")
        sys.exit(0)
    total_rows = total_ids = 0
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as fh:
            r, w = bridge(fh.read())
        total_rows, total_ids = total_rows + r, total_ids + w
        print(f"{path.replace(chr(92), '/').split('/')[-1]}: path rows={r}, citing an id={w}")
    print(f"TOTAL path rows={total_rows}, citing an id={total_ids}")
