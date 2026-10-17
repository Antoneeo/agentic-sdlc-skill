"""SPIKE (not mergeable): build a single-file HTML view of a kb-agentic corpus.

Usage: python export.py <docs_root> <out.html>

Parsing is delegated to the kb distribution's own checker (knowledge.py /
sdlc_core.py): this script only reshapes what they return into JSON and pours
it into template.html. Nothing here re-implements a kb format rule, except the
line-locator excerpt (`#L<a>-<b>`), which the checker validates but does not
expose as text.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KB_SCRIPTS = HERE.parents[2] / "distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts"
sys.path.insert(0, str(KB_SCRIPTS))

import knowledge  # noqa: E402
import sdlc_core  # noqa: E402

LINE_LOC = re.compile(r"^L(\d+)-(\d+)$")


def frontmatter(path):
    return sdlc_core.load_frontmatter(sdlc_core.read_text(path).splitlines()) or {}


def body_after_frontmatter(text):
    m = re.match(r"^---\r?\n.*?\r?\n---\r?\n?", text, re.S)
    return text[m.end():] if m else text


def excerpt(docs, source):
    """One cited span as text, when the locator is a line range."""
    if "#" not in source:
        return {"path": source, "loc": "", "text": None}
    path, loc = source.rsplit("#", 1)
    m = LINE_LOC.match(loc)
    target = docs / path
    if not m or not target.is_file():
        return {"path": path, "loc": loc, "text": None}
    lines = sdlc_core.read_text(target).splitlines()
    a, b = int(m.group(1)), int(m.group(2))
    lo, hi = max(1, a - 2), min(len(lines), b + 2)
    return {
        "path": path,
        "loc": loc,
        "from": lo,
        "cited": [a, b],
        "text": "\n".join(lines[lo - 1:hi]),
    }


def topics(docs):
    out = []
    for slug, (path, text, rows) in knowledge.kb_collect_topics(docs).items():
        meta = sdlc_core.load_frontmatter(text.splitlines()) or {}
        claims = []
        for row in rows:
            sources = [s.strip() for s in row["source"].split(";") if s.strip()]
            claims.append({
                "id": row["id"], "claim": row["claim"], "valid": row["valid"],
                "qty": row["qty"], "about": row["about"], "prov": row["prov"],
                "state": row["state"], "kind": row.get("kind", ""),
                "sources": [excerpt(docs, s) for s in sources],
            })
        out.append({
            "slug": slug,
            "file": "topics/" + path.name,
            "description": meta.get("description", ""),
            "parents": knowledge._as_list(meta.get("parents")),
            "synonyms": knowledge._as_list(meta.get("synonyms")),
            "owns": knowledge._as_list(meta.get("owns")),
            "gaps": knowledge._as_list(meta.get("gaps")),
            "status": meta.get("status", ""),
            "redirect_to": meta.get("redirect_to", ""),
            "claims": claims,
        })
    return out


def sources(docs):
    out = []
    given = docs / "corpus/given"
    for meta_path in sorted(given.glob("*.meta.md")) if given.is_dir() else []:
        artifact = meta_path.name[: -len(".meta.md")]
        out.append({
            "path": "corpus/given/" + artifact,
            "kind": "given",
            "meta": frontmatter(meta_path),
            "note": body_after_frontmatter(sdlc_core.read_text(meta_path)).strip(),
        })
    notes = docs / "corpus/notes"
    for p in sorted(notes.glob("*.md")) if notes.is_dir() else []:
        text = sdlc_core.read_text(p)
        out.append({
            "path": "corpus/notes/" + p.name,
            "kind": "ruling" if p.name.startswith("RULING_") else "note",
            "meta": frontmatter(p),
            "note": body_after_frontmatter(text).strip(),
        })
    return out


def main(docs_root, out_html):
    docs = Path(docs_root).resolve()
    errors, warnings = knowledge.kb_graph_check(docs)
    data = {
        "corpus": docs.parent.name,
        "docs": str(docs),
        "topics": topics(docs),
        "sources": sources(docs),
        "graph_errors": [str(f) for f in errors],
        "graph_warnings": [str(f) for f in warnings],
    }
    template = (HERE / "template.html").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = template.replace("/*__DATA__*/null", payload)
    Path(out_html).write_text(html, encoding="utf-8")
    print(Path(out_html).resolve())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
