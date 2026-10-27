"""F-085 probe: are the constraints in existing ANALYSIS files extractable today?

For each ANALYSIS it measures, per constraint-bearing section, the items that carry
an id at the start of a bullet, heading or table row (UC1, FS3, T2, AC-4, ...), and
how many of those items name a file or symbol in backticks (the anchor a recall hook
would key on). It also reports the document's size, the cost the agent pays today
to see the same constraints by reading.

Usage: python -I probe_extractability.py <ANALYSIS.md> [...]
RED check: --red feeds a synthetic document with no ids and must report 0 items.
"""
import re
import sys

SECTIONS = {
    "use cases": "objective",
    "functional spec": "objective",
    "interface contract": "objective",
    "security": "objective+preservation",
    "impact": "preservation",
    "capability ledger": "preservation",
    "test strategy": "preservation",
}
ITEM = re.compile(
    r"^\s*(?:[-*]\s+|\|\s*|#{3,4}\s+)\**`?"
    r"(?P<id>(?:UC|FS|IC|T|TM|AC|SR|S|R|C|B|P|W)-?\d+(?:\.\d+)?)\b"
)
ANCHOR = re.compile(r"`[^`\n]*(?:[\w-]+\.(?:py|md|js|ts|json|ps1|sh|toml|ini)\b|\w+\.\w+\(|\w+\(\))[^`\n]*`")


def section_kind(heading):
    h = heading.lower()
    for key, kind in SECTIONS.items():
        if key in h:
            return kind
    return None


def probe(text):
    lines = text.splitlines()
    out, current, item = {}, None, None
    for line in lines:
        if line.startswith("## "):
            current = section_kind(line[3:])
            item = None
            continue
        if current is None:
            continue
        m = ITEM.match(line)
        if m:
            item = {"id": m.group("id"), "anchored": bool(ANCHOR.search(line))}
            out.setdefault(current, []).append(item)
        elif item is not None and line.startswith("  ") and ANCHOR.search(line):
            item["anchored"] = True  # continuation line of the same bullet
        elif not line.strip() or line.lstrip()[:1] in "-*|#":
            item = None if not line.startswith("  ") else item
    return len(lines), len(text.split()), out


def report(name, text):
    n_lines, n_words, out = probe(text)
    total = sum(len(v) for v in out.values())
    anchored = sum(i["anchored"] for v in out.values() for i in v)
    by_kind = ", ".join(f"{k}={len(v)}" for k, v in sorted(out.items())) or "none"
    print(f"{name}: {n_lines} lines, {n_words} words | id'd items={total} "
          f"(anchored={anchored}) | {by_kind}")
    return total


if __name__ == "__main__":
    if sys.argv[1:] == ["--red"]:
        doc = "## Functional Spec\n\n- The tool must refuse bad input.\n- It logs errors.\n"
        assert report("RED-synthetic", doc) == 0, "probe found ids where there are none"
        doc2 = "## Functional Spec\n\n- **FS1 Refuse.** `sdlc_core.confine_under()` refuses.\n"
        assert report("GREEN-synthetic", doc2) == 1, "probe missed an id'd anchored item"
        print("red/green OK")
        sys.exit(0)
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as fh:
            report(path.replace("\\", "/").split("/")[-1], fh.read())
