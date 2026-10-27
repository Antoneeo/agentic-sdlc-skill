"""F-085 success-signal baseline: review rows per gate kind, and how many mention FAIL.

A row is classed by its tier cell: code/closure = implementation gate (a FAIL there is
a defect that passed the design gate), vision = Vision gate, post-merge = the owner's
report of a defect after merge (FS10: its own kind, never a gate row), anything else =
design gate. "Mentions FAIL" is textual: a row recording FAIL->PASS counts, which is the
intent (the round failed). Heuristic by construction; the ANALYSIS owns the exact
measure.

Usage: python -I baseline_review_log.py <REVIEW_LOG.md> [...]
RED check: --red feeds two synthetic rows and asserts the classification.
"""
import sys


def classify(text):
    counts = {}
    for line in text.splitlines():
        if not line.startswith("| 20"):
            continue
        cells = line.split("|")
        tier = cells[3].lower() if len(cells) > 3 else ""
        if tier.strip().startswith("post-merge"):
            kind = "post_merge"
        else:
            kind = "impl" if ("code" in tier or "closure" in tier) else (
                "vision" if "vision" in tier else "design")
        rows, fails = counts.get(kind, (0, 0))
        counts[kind] = (rows + 1, fails + ("FAIL" in line))
    return counts


if __name__ == "__main__":
    if sys.argv[1:] == ["--red"]:
        doc = ("| 2026-01-01 | x | code | m | 1 | 1 | FAIL | 1 |\n"
               "| 2026-01-02 | y | design | m | 0 | 0 | PASS | 0 |\n")
        assert classify(doc) == {"impl": (1, 1), "design": (1, 0)}, classify(doc)
        # FS10: a post-merge row is its own kind, not a design-gate row
        pm = "| 2026-05-02 | x | post-merge | none (owner report) | owner | 1 | 1 | DEFECT | 0 |\n"
        assert classify(pm) == {"post_merge": (1, 0)}, classify(pm)
        print("red/green OK")
        sys.exit(0)
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as fh:
            print(path, classify(fh.read()))
