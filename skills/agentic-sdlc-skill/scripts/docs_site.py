#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The docs site (F-072): what the agent reads, made visible to the user.

    python <skill_dir>/scripts/docs_site.py [--root <project>] [--docs-dir <name>]
                                            [--out <folder>] [--open]

Turns a project's docs root into a static website opened from disk: what the
project is, what was done and when, what is open with its next step, and what is
known -- the same sources the agent reads to orient itself and resume work, no
more and no less. Read-only on the docs root, stdlib only, no network.

Shared spine file: byte-identical in every distribution of the family. It imports
sdlc_core and knowledge and changes neither. Listing documents, workstreams,
analyses, topics, claims, locators and the catalog goes through their readers; the
site adds what they do not offer -- a frontmatter split that keeps continuation
lines for display, the Vision's status line, and the `derived_from` ladder of
`kb_time_cycle` (a closure there), restated here with the inside-the-root rule. It is not named `site.py` -- that would shadow
Python's `site` module.

What it writes, outside the docs root: the page files (index.html, app.js,
style.css, strings.js) copied from `../docs_site/`, and `data/*.js` -- classic
scripts, because a page opened from disk cannot fetch JSON. All wording lives in
strings.js; this file emits codes, never interface text.
"""
import argparse
import html
import json
import math
import os
import posixpath
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.parse
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sdlc_core  # noqa: E402
import knowledge  # noqa: E402

PAGE_DIR = HERE.parent / "docs_site"
PAGE_FILES = ("index.html", "app.js", "style.css", "strings.js")
MARKER = ".docs-site-generated"
DEFAULT_OUT = ".docs-site"

# Status words -> group (Vision v9). A value marking a unit as available or next to
# take (READY, NEXT) is NOT a group: it falls under "other status", as written.
STATUS_GROUPS = {"BLOCKED": 1, "PLANNED": 2, "TODO": 2, "IN_PROGRESS": 3, "PROGRESS": 3,
                 "PAUSED": 4, "ON_HOLD": 4, "COMPLETED": 5, "DONE": 5, "CANCELLED": 6,
                 "ARCHIVED": 7}
OTHER_STATUS = 8

HEX12 = re.compile(r"^[0-9a-f]{12}$")
DASHES = re.compile("[‐-―−﹘﹣－]")
INVISIBLE = re.compile("[­​-‏⁠-⁤﻿]")


class SiteError(Exception):
    """A refusal: printed as one line, exit 2."""


# ------------------------------------------------------------------ reading

_UNREADABLE = []


def _text(path):
    """The file's text, or None when it cannot be read (recorded, reported, exit 1)."""
    try:
        text = sdlc_core.read_text(path)
    except OSError as exc:
        _note_unreadable(path, exc)
        return None
    if any(Path(p) == Path(path) for p, _e in _UNREADABLE):
        return None                    # the guard already read it as empty
    return text


def _note_unreadable(path, exc):
    if all(Path(p) != Path(path) for p, _e in _UNREADABLE):
        _UNREADABLE.append((Path(path), exc))


class _GuardedReads:
    """For one run, every read the shared readers make goes through one guard: an
    unreadable file is recorded and read as empty, so the run reports it by name
    and still writes the site. The shared modules' code is untouched; only the
    function their callers look up is wrapped, and restored on exit."""

    def __enter__(self):
        self.original = sdlc_core.read_text
        original = self.original

        def guarded(path):
            try:
                return original(path)
            except OSError as exc:
                _note_unreadable(path, exc)
                return ""
        sdlc_core.read_text = guarded
        return self

    def __exit__(self, *exc):
        sdlc_core.read_text = self.original
        return False


def split_frontmatter(text):
    """(meta pairs as written, body). Pairs keep continuation lines, joined."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return [], text
    end = next((i for i in range(1, min(len(lines), 200)) if lines[i].strip() == "---"), None)
    if end is None:
        return [], text
    pairs = []
    for ln in lines[1:end]:
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", ln)
        if m:
            pairs.append([m.group(1), m.group(2).strip()])
        elif pairs and ln.strip():
            item = ln.strip()
            item = item[2:].strip() if item.startswith("- ") else item
            pairs[-1][1] = (pairs[-1][1] + ", " + item) if pairs[-1][1] else item
    return pairs, "\n".join(lines[end + 1:])


def first_heading(body):
    for ln in body.split("\n"):
        if ln.startswith("# "):
            return ln[2:].strip()
    return None


def normalize(s):
    """Search folding: case, accents, dash variants, invisible characters, spaces.
    app.js carries the same function; the battery runs both on the same inputs."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower()
    s = DASHES.sub("-", s)
    s = INVISIBLE.sub("", s)
    return re.sub(r"\s+", " ", s).strip()


def status_group(value):
    return STATUS_GROUPS.get(str(value or "").strip().upper(), OTHER_STATUS)


def _v(meta, key):
    return str(meta.get(key) or "").strip()


# ---------------------------------------------------------------- markdown
# A formatter with its sanitizer built in: every byte of content is escaped, and
# the only markup in the output is the markup emitted here -- headings,
# paragraphs, lists, tables, emphasis, code, blockquotes, rules and links. A link
# survives only when relative, `#` or http(s); images become their alt text.

_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_LINK = re.compile(r"(!?)\[([^\]]*)\]\(\s*<?([^)\s>]*)>?(?:\s+\"[^\"]*\")?\s*\)")
_CODE = re.compile(r"(`+)(.+?)\1", re.S)
_AUTO = re.compile(r"&lt;(https?://[^\s&]+)&gt;")


class _Ctx:
    def __init__(self, base="", facts=None, docs=None):
        self.base = base           # folder of the document, docs-root relative
        self.facts = facts         # set of fact ids, or None without a knowledge base


def _esc(s):
    return html.escape(s, quote=True)


def _href(target, ctx):
    """(href, external) for a link target, or None when it must not be a link."""
    if target.startswith("#"):
        return _esc(target), False
    if re.match(r"^https?://", target, re.I):
        return _esc(target), True
    if _SCHEME.match(target) or target.startswith(("/", "\\")):
        return None
    path, _, _frag = target.partition("#")
    if not path:
        return None
    rel = posixpath.normpath(posixpath.join(ctx.base, urllib.parse.unquote(path)))
    if rel.startswith("..") or rel.startswith("/"):
        return None
    return "#/doc/" + urllib.parse.quote(rel, safe="/._-~"), False


def _inline(text, ctx, links=True):
    out, pos = [], 0
    for m in _CODE.finditer(text):
        out.append(_inline_plain(text[pos:m.start()], ctx, links))
        code = m.group(2).strip() if m.group(2).strip() else m.group(2)
        if ctx.facts is not None and HEX12.match(code):
            if code in ctx.facts:
                out.append('<a class="factid" href="#/fact/%s"><code>%s</code></a>' % (code, code))
            else:
                out.append('<code class="notfact">%s</code>' % code)
        else:
            out.append("<code>%s</code>" % _esc(code))
        pos = m.end()
    out.append(_inline_plain(text[pos:], ctx, links))
    return "".join(out)


def _emphasis(s):
    s = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w])__(?=\S)(.+?)(?<=\S)__(?![\w])", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\*\w])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![\*\w])", r"<em>\1</em>", s)
    s = re.sub(r"(?<![\w])_(?=\S)(.+?)(?<=\S)_(?![\w])", r"<em>\1</em>", s)
    return s


def _inline_plain(text, ctx, links):
    if not text:
        return ""
    text = text.replace("\x00", "")   # content can never address a held piece of markup
    held = []

    def hold(markup):
        held.append(markup)
        return "\x00%d\x00" % (len(held) - 1)

    def link(m):
        image, label, target = m.group(1), m.group(2), m.group(3)
        if image:
            return hold(_esc(label))
        inner = _emphasis(_esc(label))
        h = _href(target, ctx) if links else None
        if h is None:
            return hold(inner)
        href, external = h
        extra = ' target="_blank" rel="noopener noreferrer"' if external else ""
        return hold('<a href="%s"%s>%s</a>' % (href, extra, inner))

    text = _LINK.sub(link, text)
    s = _emphasis(_esc(text))
    s = _AUTO.sub(lambda m: '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
                  % (m.group(1), m.group(1)), s)
    return re.sub("\x00(\\d+)\x00", lambda m: held[int(m.group(1))], s)


def _slugify(text):
    s = re.sub(r"[^\w\- ]", "", text.lower()).strip()
    return re.sub(r"\s+", "-", s)


_LIST = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
_HR = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
_HEAD = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def _cells(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", s)]


def _is_sep(line):
    s = line.strip()
    return s.startswith("|") and set(s) <= set("|-: ") and "-" in s


def _starts_block(lines, i):
    ln = lines[i]
    return (ln.strip().startswith("```") or _HEAD.match(ln) or _HR.match(ln)
            or ln.lstrip().startswith(">") or _LIST.match(ln)
            or (ln.strip().startswith("|") and i + 1 < len(lines) and _is_sep(lines[i + 1])))


def _blocks(lines, ctx):
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.strip().startswith("```"):
            fence = ln.strip()[:3]
            body, i = [], i + 1
            while i < len(lines) and not lines[i].strip().startswith(fence):
                body.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % _esc("\n".join(body)))
            continue
        m = _HEAD.match(ln)
        if m:
            n = len(m.group(1))
            title = m.group(2)
            out.append('<h%d id="%s">%s</h%d>' % (n, _esc(_slugify(title)), _inline(title, ctx), n))
            i += 1
            continue
        if _HR.match(ln):
            out.append("<hr>")
            i += 1
            continue
        if ln.lstrip().startswith(">"):
            quoted = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                q = lines[i].lstrip()[1:]
                quoted.append(q[1:] if q.startswith(" ") else q)
                i += 1
            out.append("<blockquote>%s</blockquote>" % _blocks(quoted, ctx))
            continue
        if ln.strip().startswith("|") and i + 1 < len(lines) and _is_sep(lines[i + 1]):
            head = _cells(ln)
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(_cells(lines[i]))
                i += 1
            th = "".join("<th>%s</th>" % _inline(c, ctx) for c in head)
            body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % _inline(c, ctx) for c in r)
                           for r in rows)
            out.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (th, body))
            continue
        if _LIST.match(ln):
            i = _list(lines, i, ctx, out)
            continue
        para = [ln.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not _starts_block(lines, i):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % _inline(" ".join(para), ctx))
    return "".join(out)


def _list(lines, i, ctx, out):
    first = _LIST.match(lines[i])
    indent = len(first.group(1))
    ordered = first.group(2)[0].isdigit()
    items = []
    while i < len(lines):
        m = _LIST.match(lines[i])
        if m and len(m.group(1)) == indent:
            items.append([m.group(3)])
            i += 1
            continue
        if not lines[i].strip():
            nxt = i + 1
            if nxt < len(lines) and lines[nxt].strip() and (
                    len(lines[nxt]) - len(lines[nxt].lstrip()) > indent):
                items[-1].append("")
                i += 1
                continue
            break
        lead = len(lines[i]) - len(lines[i].lstrip())
        if lead > indent or (not m and not _starts_block(lines, i)):
            items[-1].append(lines[i][min(lead, indent + 2):] if lead > indent else lines[i].strip())
            i += 1
            continue
        break
    tag = "ol" if ordered else "ul"
    parts = []
    for item in items:
        head, rest = item[0], item[1:]
        if any(_LIST.match(r) or not r.strip() for r in rest) or any(
                r.strip().startswith(("```", ">", "|")) for r in rest):
            cont = [head] + rest
            k = 1
            while k < len(cont) and cont[k].strip() and not _LIST.match(cont[k]):
                k += 1
            inner = "<span>%s</span>" % _inline(" ".join(c.strip() for c in cont[:k]), ctx)
            inner += _blocks(cont[k:], ctx)
        else:
            inner = _inline(" ".join([head] + [r.strip() for r in rest]), ctx)
        parts.append("<li>%s</li>" % inner)
    out.append("<%s>%s</%s>" % (tag, "".join(parts), tag))
    return i


def markdown(text, base="", facts=None):
    """Markdown -> sanitized HTML. `base`: the document's folder, for relative links;
    `facts`: the fact ids, when a knowledge base is present (12-hex tokens link)."""
    return _blocks((text or "").replace("\r\n", "\n").split("\n"), _Ctx(base, facts))


# ------------------------------------------------------------ project facts

def resolve_root(args):
    """(project, docs, name) as every entry point resolves them; SiteError otherwise."""
    try:
        discovered, name = sdlc_core.resolve_docs_dir(args, args.root)
    except sdlc_core.AmbiguousDocsRoot as exc:
        raise SiteError(str(exc))
    sdlc_core.set_docs_dir(name)
    project = Path(args.root).resolve() if args.root else (
        discovered or sdlc_core.find_project_root())
    docs = project / name
    if not docs.is_dir():
        raise SiteError("%s not found: refusing to generate a site here. Run the skill's "
                        "init first, or pass --root <project_root>." % docs)
    return project, docs, name


def project_lens(project, name):
    if name == "mkt_docs":
        return "marketing"
    return sdlc_core.project_default_domain(project)


def units_page(lens):
    return {"marketing": None, "course": "courses"}.get(lens, "features")


def vision_status(pairs, body):
    for k, v in pairs:
        if k.lower() == "status":
            return v
    for ln in body.split("\n")[:20]:
        m = re.match(r"^\**\s*status\s*:?\s*\**\s*:?\s*(.+?)\s*$", ln, re.I)
        if m:
            return m.group(1).strip()
    return None


def first_section(body, named=None):
    """(title, body) of the first `## ` section -- or of the first one whose title
    starts with `named`, when given (None when there is no such section)."""
    lines = body.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("## ") and (named is None or ln[3:].strip().lower().startswith(named)):
            rest = []
            for nxt in lines[i + 1:]:
                if nxt.startswith("## "):
                    break
                rest.append(nxt)
            return ln[3:].strip(), "\n".join(rest).strip()
    return None, None


NORTH_STAR = "north star"


def vision_lead(body):
    """(title, body, is_north_star): the Vision's North Star wherever it sits (R25),
    else its first section, which is then not called a North Star."""
    title, text = first_section(body, NORTH_STAR)
    if title:
        return title, text, True
    title, text = first_section(body)
    return title, text, False


def opening_paragraph(body):
    lines = body.split("\n")
    start = next((i + 1 for i, ln in enumerate(lines) if ln.startswith("# ")), 0)
    para = []
    for ln in lines[start:]:
        if not ln.strip():
            if para:
                break
            continue
        if ln.startswith("#"):
            if para:
                break
            continue
        para.append(ln)
    return "\n".join(para)


# ------------------------------------------------------------ knowledge base

def resolve_derived(docs, entry, inside_only=True):
    """A `derived_from` entry -> docs-root-relative path, or None.

    The resolution ladder of `knowledge.kb_time_cycle` (its `_resolve` closure):
    normalize, then a path with `/` must exist as written, a bare name is looked
    up in notes/ then given/. The site adds one rule: the result is followed only
    if it ends inside the docs root."""
    entry = posixpath.normpath(str(entry).strip())
    found = None
    if "/" in entry:
        found = entry if (docs / entry).is_file() else None
    else:
        for base in ("corpus/notes/", "corpus/given/"):
            if (docs / (base + entry)).is_file():
                found = base + entry
                break
    if found is None or not inside_only:
        return found
    try:
        return (docs / found).resolve().relative_to(docs.resolve()).as_posix()
    except (ValueError, OSError):
        return None


def _inside(docs, rel):
    return sdlc_core.confine_under(docs, rel) is not None


class Passages:
    """Reads the span a locator addresses exactly as `kb_check_locator` reads it,
    one text per file (cached). Returns (where, before, passage, after) or a reason."""

    CONTEXT = 160

    def __init__(self, docs):
        self.docs = docs
        self.texts = {}
        self.check_cache = {}

    def _t(self, path):
        if path not in self.texts:
            self.texts[path] = _text(path)
        return self.texts[path]

    def read(self, rel, loc):
        target = self.docs / rel
        m = knowledge.LOC_PAGE_RE.match(loc)
        if m:
            page, a, b = map(int, m.groups())
            ext = target if target.suffix == ".txt" else target.with_suffix(".txt")
            if not ext.is_file():
                return {"reason": "no_file" if not target.exists() else "no_extraction"}
            errs = []
            knowledge.kb_check_locator(target, loc, "site", errs, self.check_cache)
            if errs:
                return {"reason": "no_span", "where": {"page": page}}
            text = self._t(ext)
            if text is None:
                return {"reason": "unreadable"}
            body = text.split("\f")[page - 1]
            return {"where": {"page": page}, "before": body[max(0, a - self.CONTEXT):a],
                    "passage": body[a:b], "after": body[b:b + self.CONTEXT]}
        m = knowledge.LOC_LINE_RE.match(loc)
        if m:
            a, b = map(int, m.groups())
            if not target.is_file():
                return {"reason": "no_file"}
            errs = []
            knowledge.kb_check_locator(target, loc, "site", errs, self.check_cache)
            if errs:
                return {"reason": "no_span", "where": {"lines": [a, b]}}
            text = self._t(target)
            if text is None:
                return {"reason": "unreadable"}
            lines = text.split("\n")
            return {"where": {"lines": [a, b]}, "before": "\n".join(lines[max(0, a - 3):a - 1]),
                    "passage": "\n".join(lines[a - 1:b]), "after": "\n".join(lines[b:b + 2])}
        if knowledge.LOC_CELL_RE.match(loc):
            return {"reason": "cell", "where": {"cell": loc}}
        return {"reason": "unknown_form"}


def _kind(row):
    parts = (row.get("state") or "").split(None, 1)
    return (parts[0] if parts else "OK").upper(), (parts[1] if len(parts) > 1 else "")


def _ids(rest):
    return [t.strip() for t in rest.split(",") if t.strip()]


def chain_ends(start, by_id):
    """Every branch of a replacement chain, walked to its end: the current fact,
    or a stated stop -- a loop or a missing id."""
    ends = []

    def walk(fid, seen):
        if fid not in by_id:
            end = {"stop": "missing", "id": fid}
        elif fid in seen:
            end = {"stop": "loop", "id": fid}
        else:
            kind, rest = _kind(by_id[fid])
            if kind == "SUPERSEDED" and _ids(rest):
                for nxt in _ids(rest):
                    walk(nxt, seen | {fid})
                return
            end = {"id": fid}
        if end not in ends:
            ends.append(end)

    kind, rest = _kind(by_id[start])
    for nxt in _ids(rest):
        walk(nxt, frozenset({start}))
    return ends


class Grounds:
    """What an inferred fact rests on: the anti-echo walk of the probe, following a
    path only when it stays inside the docs root."""

    def __init__(self, docs):
        self.docs = docs
        self.meta = {}

    def _meta(self, rel):
        if rel not in self.meta:
            t = _text(self.docs / rel)
            self.meta[rel] = sdlc_core.load_frontmatter(t.splitlines()) if t else {}
        return self.meta[rel]

    def leaves(self, rel, seen=frozenset()):
        if rel is None:
            return [{"kind": "untraceable"}]
        if rel in seen:
            return [{"kind": "untraceable", "path": rel}]
        seen = seen | {rel}
        if rel.startswith("corpus/given/"):
            return [{"kind": "document", "path": rel}]
        if not _inside(self.docs, rel) or not (self.docs / rel).is_file():
            return [{"kind": "untraceable", "path": rel}]
        meta = self._meta(rel)
        origin = _v(meta, "origin").lower()
        kind = {"elicited": "statement", "ruling": "decision", "imported": "kb"}.get(origin)
        if kind:
            return [{"kind": kind, "path": rel}]
        entries = knowledge._kb_df_entries(meta.get("derived_from"))
        if not entries:
            return [{"kind": "decision" if meta.get("basis") else "untraceable", "path": rel}]
        out = []
        for e in entries:
            target = resolve_derived(self.docs, e)
            got = self.leaves(target, seen) if target else [{"kind": "untraceable", "path": rel,
                                                              "entry": str(e)}]
            for g in got:
                if g not in out:
                    out.append(g)
        return out


def ground_class(leaves):
    kinds = {g["kind"] for g in leaves}
    if "statement" in kinds:
        return "statement"
    if "untraceable" in kinds:
        return "untraceable"
    if "kb" in kinds:
        return "imported"
    return "documents"


def topic_area(slug, live, all_nodes):
    """The root reached by first parents; a cycle, a missing or a merged parent -> None."""
    seen, cur = set(), slug
    while True:
        if cur in seen or cur not in live:
            return None
        seen.add(cur)
        parents = knowledge._as_list(live[cur]["meta"].get("parents"))
        if not parents:
            return cur
        cur = parents[0]


def build_kb(docs):
    all_nodes = knowledge.kb_load_topics(docs)
    if not all_nodes:
        return None
    tomb = {s for s, n in all_nodes.items() if _v(n["meta"], "status") == "SUPERSEDED"}
    live = {s: n for s, n in all_nodes.items() if s not in tomb}
    topics, facts, rows_of = {}, {}, {}
    by_id = {}
    for slug in sorted(all_nodes):
        node = all_nodes[slug]
        t = _text(docs / node["file"]) or ""
        _pairs, body = split_frontmatter(t)
        rows, _errs = knowledge.kb_parse_claims(t)
        for r in rows:
            r["_topic"] = slug
            r["id"] = r["id"] or "%s:%d" % (slug, r["_line"])
            by_id.setdefault(r["id"], r)
        rows_of[slug] = rows
        meta = node["meta"]
        if slug in tomb:
            topics[slug] = {"name": slug, "merged_into": _v(meta, "redirect_to")}
            continue
        topics[slug] = {
            "name": first_heading(body) or slug,
            "description": _v(meta, "description"),
            "aka": knowledge._as_list(meta.get("synonyms")),
            "gaps": knowledge._as_list(meta.get("gaps")),
            "related": knowledge._as_list(meta.get("related")),
            "parents": knowledge._as_list(meta.get("parents")),
            "file": node["file"],
            "facts": [r["id"] for r in rows],
            "count": len(rows),
        }
    for slug, t in topics.items():
        if "merged_into" in t:
            continue
        t["area"] = topic_area(slug, live, all_nodes)
        t["children"] = sorted(s for s, o in topics.items()
                               if "merged_into" not in o and slug in o["parents"])
    passages, grounds = Passages(docs), Grounds(docs)
    sources_of_topic = {}
    for slug in sorted(rows_of):
        for r in rows_of[slug]:
            kind, rest = _kind(r)
            f = {"text": r["claim"], "valid": r["valid"], "qty": r["qty"], "about": r["about"],
                 "origin": (r["prov"] or "").strip().lower(), "topic": slug,
                 "state": {"SUPERSEDED": "superseded", "CONTESTED": "contested"}.get(kind, "ok")}
            if kind == "SUPERSEDED":
                f["successors"] = _ids(rest)
                f["chain_ends"] = chain_ends(r["id"], by_id)
            if kind == "CONTESTED":
                f["with"] = _ids(rest)
            srcs = []
            for src in r["source"].split(";"):
                src = src.strip()
                if not src:
                    continue
                rel, _, loc = src.rpartition("#") if "#" in src else (src, "", "")
                rel = rel.strip()
                entry = {"path": rel}
                if not _inside(docs, rel):
                    entry["reason"] = "outside"
                elif rel.startswith("corpus/given/"):
                    entry["source"] = rel[len("corpus/given/"):]
                    sources_of_topic.setdefault(entry["source"], set()).add(slug)
                    entry.update(passages.read(rel, loc.strip()) if loc else {"reason": "no_locator"})
                elif loc:
                    entry.update(passages.read(rel, loc.strip()))
                if loc:
                    entry["loc"] = loc.strip()
                srcs.append(entry)
            f["sources"] = srcs
            if f["origin"] == "derived":
                leaves = []
                for rel in knowledge.kb_claim_sources(r):
                    rel = rel.strip()
                    for g in grounds.leaves(rel if _inside(docs, rel) else None):
                        if g not in leaves:
                            leaves.append(g)
                f["grounds"] = leaves
                f["ground_class"] = ground_class(leaves)
            f["statement"] = f["origin"] == "elicited" or f.get("ground_class") == "statement"
            facts.setdefault(r["id"], f)
    sources = build_sources(docs, rows_of)
    order = sorted(s for s in topics if "merged_into" not in topics[s])
    return {"topics": topics, "facts": facts, "sources": sources, "order": order,
            "map": build_map(topics, order, facts, sources)}


def build_sources(docs, rows_of):
    given = docs / "corpus" / "given"
    out = {}
    if not given.is_dir():
        return out
    cited = {}
    for slug, rows in rows_of.items():
        for r in rows:
            for rel in sorted(set(knowledge.kb_claim_sources(r))):
                if rel.startswith("corpus/given/"):
                    name = rel[len("corpus/given/"):]
                    c = cited.setdefault(name, [0, set()])
                    c[0] += 1
                    c[1].add(slug)
    for mp in sorted(given.glob("*.meta.md")):
        name = mp.name[:-len(".meta.md")]
        t = _text(mp) or ""
        meta = sdlc_core.load_frontmatter(t.splitlines()) or {}
        through = _v(meta, "extracted_through")
        parsed = knowledge.kb_parse_extracted_through(through) if through else None
        if not through:
            read = {"kind": "unrecorded"}
        elif parsed is None:
            read = {"kind": "unreadable", "raw": through}
        elif parsed[0] == "complete":
            read = {"kind": "complete"}
        else:
            total = knowledge.kb_extraction_extent(given / name, parsed[0])
            read = {"kind": "page" if parsed[0] == "p" else "line", "n": parsed[1]}
            if total:
                read["of"] = total
        c = cited.get(name, [0, set()])
        entry = {"kind": Path(name).suffix.lstrip(".").lower(), "date": _v(meta, "date"),
                 "read": read, "facts": c[0], "topics": sorted(c[1]),
                 "sidecar": "corpus/given/" + mp.name}
        sup = knowledge.kb_unquote(meta.get("supersedes"))
        if sup:
            entry["newer_of"] = sup
        out[name] = entry
    for name, e in list(out.items()):
        older = e.get("newer_of")
        if older in out:
            out[older]["older_of"] = name
    return out


def build_map(topics, order, facts, sources):
    """The three views' geometry, computed here: deterministic, laid out, framed.

    Topics: a radial tree by area (first parents), unplaced topics on an outer
    ring. Everything: each topic's facts on a small spiral around it, each source
    document at the centre of the topics that use it."""
    pos = {}
    areas = [s for s in order if topics[s].get("area") == s]
    kids = {s: [] for s in order}
    for s in order:
        area = topics[s].get("area")
        if area and area != s:
            parent = topics[s]["parents"][0]
            if parent in kids:
                kids[parent].append(s)
    weight = {}

    def w(s):
        if s not in weight:
            weight[s] = max(1, sum(w(k) for k in kids[s]))
        return weight[s]

    total = sum(w(a) for a in areas) or 1
    ring = 260.0

    def place(s, depth, a0, a1):
        ang = (a0 + a1) / 2
        r = depth * ring
        pos[s] = (round(r * math.cos(ang), 1), round(r * math.sin(ang), 1))
        cur = a0
        for k in kids[s]:
            span = (a1 - a0) * w(k) / w(s)
            place(k, depth + 1, cur, cur + span)
            cur += span

    cur = 0.0
    for a in areas:
        span = 2 * math.pi * w(a) / total
        place(a, 1 if len(areas) > 1 else 0, cur, cur + span)
        cur += span
    rest = [s for s in order if s not in pos]
    if rest:
        depth = max([0] + [math.hypot(*p) for p in pos.values()]) + ring
        for i, s in enumerate(rest):
            ang = 2 * math.pi * i / len(rest)
            pos[s] = (round(depth * math.cos(ang), 1), round(depth * math.sin(ang), 1))
    nodes = [{"id": s, "x": pos[s][0], "y": pos[s][1], "area": topics[s].get("area"),
              "count": topics[s]["count"]} for s in order]
    edges = []
    for s in order:
        for p in topics[s]["parents"]:
            if p in pos:
                edges.append({"a": s, "b": p, "kind": "part_of"})
        for r in topics[s]["related"]:
            if r in pos:
                edges.append({"a": s, "b": r, "kind": "related"})
    shared = {}
    for name in sorted(sources):
        ts = [t for t in sources[name]["topics"] if t in pos]
        for i, a in enumerate(ts):
            for b in ts[i + 1:]:
                shared[(a, b)] = shared.get((a, b), 0) + 1
    for (a, b), n in sorted(shared.items()):
        edges.append({"a": a, "b": b, "kind": "shared", "n": n, "computed": True})
    # everything: facts spiral around their topic; sources at their topics' centre
    every = []
    golden = math.pi * (3 - math.sqrt(5))
    for s in order:
        cx, cy = pos[s]
        for i, fid in enumerate(topics[s]["facts"]):
            r = 18 + 7 * math.sqrt(i + 1)
            every.append({"id": fid, "kind": "fact", "x": round(cx + r * math.cos(i * golden), 1),
                          "y": round(cy + r * math.sin(i * golden), 1)})
    for i, name in enumerate(sorted(sources)):
        ts = [pos[t] for t in sources[name]["topics"] if t in pos]
        if ts:
            x, y = sum(p[0] for p in ts) / len(ts), sum(p[1] for p in ts) / len(ts)
        else:
            x, y = 0.0, 0.0
        r = 40 + 4 * (i % 7)
        every.append({"id": name, "kind": "source", "x": round(x + r * math.cos(i * golden), 1),
                      "y": round(y + r * math.sin(i * golden), 1)})
    return {"nodes": nodes, "edges": edges, "every": every}


# ------------------------------------------------------------ the documents

def doc_page(docs, rel, facts):
    t = _text(docs / rel)
    if t is None:
        return None
    pairs, body = split_frontmatter(t)
    base = posixpath.dirname(rel)
    page = {"title": first_heading(body) or posixpath.basename(rel),
            "meta": pairs, "html": markdown(body, base, facts),
            "_n": normalize(" ".join([first_heading(body) or "", rel,
                                      " ".join(v for _k, v in pairs), body]))}
    if re.match(r"^solutions/ANALYSIS_[^/]+\.md$", rel):
        page["chain"] = {"steps": analysis_chain(body), "_stem": posixpath.basename(rel)[9:-3]}
    return page


# The chain an analysis is read through (R24): why (Vision), what (use cases, flows and
# interfaces, risks), how (solution study, design and tests), then the merge brief and
# E2E script, then the Diary. Headings are the validator's own wherever it names them --
# ANALYSIS_SECTIONS, SECURITY_SECTION and every lens's risk section in DOMAINS -- and the
# template's otherwise; a heading matches by prefix, case-insensitively.
CHAIN_STEPS = ("vision", "use_cases", "flows", "risks", "solution", "design",
               "merge_tests", "diary")


def _chain_headings():
    named = {pair[0]: pair for pair in sdlc_core.ANALYSIS_SECTIONS}
    risks = list(sdlc_core.SECURITY_SECTION)
    for lens in sdlc_core.DOMAINS.values():
        risks += [h for h in lens["risk_section"] if h not in risks]
    return (("vision", named["## Objective"] + named["## Feature Vision"] + ("## Vision Alignment",)),
            ("use_cases", ("## Use Cases",)),
            ("flows", ("## Functional Spec", "## Interface Contract")),
            ("risks", tuple(risks)),
            ("solution", ("## Capability Ledger",) + named["## Impact"]),
            ("design", named["## Action Plan"] + named["## Test Strategy"]),
            ("diary", named["## Diary"]))


def chain_step(heading):
    """The chain step a level-2 heading belongs to, or None (it stays where it is)."""
    h = heading.strip().lower()
    for step, aliases in _chain_headings():
        if any(h.startswith(a.lower()) for a in aliases):
            return step
    return None


def analysis_chain(body):
    """[{step, sections: [{title, id}]}] in chain order; sections as written, in
    document order. The id is the one the formatter gives the heading."""
    found = {s: [] for s in CHAIN_STEPS}
    fenced = False
    for ln in body.split("\n"):
        if ln.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced or not ln.startswith("## "):
            continue
        step = chain_step(ln)
        m = _HEAD.match(ln)
        if step and m:
            found[step].append({"title": m.group(2), "id": _slugify(m.group(2))})
    return [{"step": s, "sections": found[s]} for s in CHAIN_STEPS]


def link_companions(docs, pages):
    """Each analysis's merge brief, E2E script and request record, where they exist,
    and the project's North Star (R25)."""
    north_star = None
    vp = "vision/project_vision.md"
    if vp in pages:
        title, _body, is_ns = vision_lead(split_frontmatter(_text(docs / vp) or "")[1])
        if is_ns:
            north_star = {"path": vp, "id": _slugify(title)}
    for rel, page in pages.items():
        chain = page.get("chain")
        if not chain:
            continue
        stem = chain.pop("_stem")
        chain["north_star"] = north_star
        chain["companions"] = {
            key: path if path in pages else None
            for key, path in (("merge", "solutions/MERGE_REVIEW_%s.md" % stem),
                              ("e2e", "solutions/E2E_TEST_%s.md" % stem),
                              ("request", "audit/requests/REQUEST_%s.md" % stem))}


def orientation_sources(docs):
    """{role: docs-relative path} of what the agent reads at session start, from
    `sdlc_core.orient_docs` -- the one list. Roles are matched by position: a fifth
    source added there needs a role here, and the battery goes red until it has one."""
    roles = ("readme", "manifest", "router", "register")
    out = {}
    for role, (_label, rel) in zip(roles, sdlc_core.orient_docs()):
        rel = rel.split("/", 1)[1]
        out[role] = rel if (docs / rel).is_file() else None
    return out


def audit_pages(docs):
    """Documents the agent reads that have a page but no place in the tree (R23)."""
    out = []
    oriented = [r for r in orientation_sources(docs).values() if r]
    for rel in oriented + ["topics/INDEX.md", "audit/project_notes.md", "audit/reviews/REVIEW_LOG.md"]:
        if (docs / rel).is_file():
            out.append(rel)
    aud = docs / "audit"
    if aud.is_dir():
        out += ["audit/" + p.name for p in sorted(aud.glob("HANDOFF_*.md"))]
        req = aud / "requests"
        if req.is_dir():
            out += ["audit/requests/" + p.name for p in sorted(req.glob("*.md"))]
    return out


def build(project, docs, name):
    lens = project_lens(project, name)
    kb = build_kb(docs)
    fact_ids = set(kb["facts"]) if kb else None
    catalog = knowledge.memory_records(docs)
    paths = [r[0] for r in catalog]
    pages = {}
    for rel in sorted(set(paths + audit_pages(docs))):
        page = doc_page(docs, rel, fact_ids)
        if page is not None:
            pages[rel] = page
    link_companions(docs, pages)
    search = [{"k": "doc", "path": rel, "title": p["title"], "n": p.pop("_n")}
              for rel, p in sorted(pages.items())]

    tree = {}
    for rel in paths:
        if rel in pages:
            tree.setdefault(posixpath.dirname(rel), []).append(
                {"path": rel, "title": pages[rel]["title"]})
    tree = [{"folder": f, "docs": sorted(d, key=lambda e: e["path"])} for f, d in sorted(tree.items())]

    work = build_work(project, docs, fact_ids)
    units = build_units(project, lens) if units_page(lens) else None
    rules = build_rules(docs, pages)
    home = build_home(docs, pages, work, kb, fact_ids)
    head = sdlc_core.git_head(project) if sdlc_core.git_available(project) else ""
    changed = sdlc_core.git_changed_since(project, "HEAD", name) if head else None
    core = {
        "meta": {"generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
                 "git": bool(head), "commit": head, "changed": len(changed or []),
                 "docs_dir": name, "lens": lens, "units_page": units_page(lens),
                 "has_kb": bool(kb), "has_sources": bool(kb and kb["sources"])},
        "home": home, "work": work, "units": units, "rules": rules,
        "guides": build_guides(docs, pages), "tree": tree,
        "chronology": home["lately_all"], "search": search,
    }
    home.pop("lately_all")
    if kb:
        kb["search"] = ([{"k": "topic", "id": s, "title": kb["topics"][s]["name"],
                          "n": normalize(" ".join([s, kb["topics"][s]["name"],
                                                   " ".join(kb["topics"][s]["aka"]),
                                                   kb["topics"][s]["description"]]))}
                         for s in kb["order"]]
                        + [{"k": "fact", "id": fid, "title": f["text"], "n": normalize(f["text"]),
                            "statement": f["statement"]}
                           for fid, f in kb["facts"].items()])
    return core, pages, kb


def build_work(project, docs, facts):
    cards = []
    for p, meta in sdlc_core.list_workstreams(project):
        card = {"name": _v(meta, "workstream"), "group": status_group(meta.get("status")),
                "path": p.relative_to(docs).as_posix()}
        for key in ("status", "level", "since", "updated", "branch", "next"):
            if _v(meta, key):
                card[key] = _v(meta, key)
        cards.append(card)
    cards.sort(key=lambda c: c["name"].lower())
    cards.sort(key=lambda c: c.get("updated", ""), reverse=True)
    cards.sort(key=lambda c: (c["group"], not c.get("updated")))
    notes = None
    np = docs / "audit" / sdlc_core.PROJECT_NOTES
    if np.is_file():
        t = _text(np)
        if t is not None:
            notes = {"path": "audit/" + sdlc_core.PROJECT_NOTES, "html": markdown(t, "audit", facts)}
    register = "audit/handoff.md" if (docs / "audit" / "handoff.md").is_file() else None
    return {"cards": cards, "notes": notes, "register": register}


def build_units(project, lens):
    default = sdlc_core.project_default_domain(project)
    units = []
    for p, meta, text in sdlc_core.list_analyses(project):
        _pairs, body = split_frontmatter(text)
        u = {"name": first_heading(body) or p.stem, "group": status_group(meta.get("status")),
             "lens": sdlc_core.resolve_domain(meta, default)[0],
             "path": "solutions/" + p.name}
        for key, field in (("id", "id"), ("status", "status"), ("level", "level"),
                           ("start", "start_date"), ("end", "end_date")):
            if _v(meta, field):
                u[key] = _v(meta, field)
        if "id" not in u and _v(meta, "feature"):
            u["id"] = _v(meta, "feature")
        units.append(u)
    units.sort(key=lambda u: (u.get("id", ""), u["path"]))
    return units


def build_rules(docs, pages):
    def entries(folder, pattern):
        d = docs / folder
        return sorted(folder + "/" + p.name for p in d.glob(pattern)
                      if p.name != "INDEX.md") if d.is_dir() else []

    def item(rel):
        meta = dict((k.lower(), v) for k, v in pages[rel]["meta"])
        return {"path": rel, "title": pages[rel]["title"], "when": meta.get("description", "")}

    vision = [item(r) for r in entries("vision", "*.md") if r in pages]
    for v in vision:
        t = _text(docs / v["path"]) or ""
        pairs, body = split_frontmatter(t)
        v["status"] = vision_status(pairs, body) or ""
    decisions = [item(r) for r in entries("architecture", "*.md") if r in pages]
    return {"vision": vision, "decisions": decisions,
            "manifest": "INDEX.md" if "INDEX.md" in pages else None}


def build_guides(docs, pages):
    """The guides page (R26): the router, then operative guides (when to read each, status
    as declared), then code-comprehension guides (`source_kind: code`)."""
    ref = docs / "reference"
    operative, comprehension = [], []
    for p in sorted(ref.glob("GUIDE_*.md")) if ref.is_dir() else []:
        rel = "reference/" + p.name
        if rel not in pages:
            continue
        meta = dict((k.lower(), v) for k, v in pages[rel]["meta"])
        g = {"path": rel, "title": pages[rel]["title"], "when": meta.get("description", ""),
             "status": meta.get("status", "")}
        (comprehension if meta.get("source_kind", "").strip().lower() == "code"
         else operative).append(g)
    return {"router": "reference/INDEX.md" if "reference/INDEX.md" in pages else None,
            "operative": operative, "comprehension": comprehension}


def build_home(docs, pages, work, kb, facts):
    readme = pages.get("README.md")
    title, intro = None, ""
    t = _text(docs / "README.md") if readme else None
    if t is not None:
        _pairs, body = split_frontmatter(t)
        title = first_heading(body)
        intro = markdown(opening_paragraph(body), "", facts)
    vision = None
    vp = "vision/project_vision.md"
    if (docs / vp).is_file():
        vt = _text(docs / vp)
        if vt is not None:
            pairs, body = split_frontmatter(vt)
            st, sb, is_ns = vision_lead(body)
            vision = {"path": vp, "status": vision_status(pairs, body), "north_star": is_ns,
                      "section_title": st, "section_html": markdown(sb or "", "vision", facts)}
    events = chronology(docs, pages)
    known = []
    if kb:
        for s in kb["order"]:
            if kb["topics"][s].get("area") == s:
                known.append({"slug": s, "name": kb["topics"][s]["name"],
                              "topics": [o for o in kb["order"]
                                         if o != s and kb["topics"][o].get("area") == s]})
    links = {role: (rel if rel in pages else None)
             for role, rel in orientation_sources(docs).items()}
    links["work"] = "work"
    if work["notes"]:
        links["notes"] = work["notes"]["path"]
    if kb:
        links["topics"] = "map"
    return {"title": title or "", "intro_html": intro, "vision": vision, "links": links,
            "open": [{k: c[k] for k in ("name", "status", "next", "path") if k in c}
                     for c in work["cards"]],
            "lately": events[:10], "lately_all": events, "known": known}


SPIKE_OUTCOME = ("## Answer / Outcome",)


def chronology(docs, pages):
    """Dated events the documents declare, most recent first: {date, kind, label,
    path}. Which lines are events is F-073's rule (R22), read with the validator's
    own readers -- `section_lines` + `entry_openers` for Diary entries, spike
    outcomes and project notes, `request_entries`, `parse_review_log`, `adr_date`,
    `knowledge.frontmatter_date` -- so the page and `validate` cannot disagree. No
    analysis start or end date, no state, nothing from git. `path` is the page the
    event opens, or None when the site has no page for it."""
    events = []

    def add(date, kind, label, rel, source=None):
        e = {"date": date, "kind": kind, "label": label,
             "path": rel if rel in pages else None}
        if source:
            e["source"] = source        # opens the source's own page (#/source/<name>)
        events.append(e)

    def openers(rel, kind, aliases=None):
        text = _text(docs / rel) if (docs / rel).is_file() else None
        if text is None:
            return
        if aliases is not None:
            section = sdlc_core.section_lines(text, aliases)
            if section is None:
                return
            text = section[1]
        for date, label, _ in sdlc_core.entry_openers(text):
            add(date, kind, label, rel)

    def title_of(rel, text):
        return pages[rel]["title"] if rel in pages else (
            first_heading(split_frontmatter(text)[1]) or posixpath.basename(rel))

    for p in sorted(docs.glob("solutions/ANALYSIS_*.md")):
        text = _text(p)
        # a shadow mirror is not an analysis to `validate` (list_analyses): not here either
        if text is not None and not sdlc_core.is_shadow(p, (text.splitlines() or [""])[0]):
            openers("solutions/" + p.name, "diary", sdlc_core.DIARY_SECTION)
    # spike outcomes: SPIKE_* in the code/kb/course lenses, RESEARCH_* in marketing
    for rel in sorted(["solutions/" + p.name for p in docs.glob("solutions/SPIKE_*.md")]
                      + ["spikes/" + p.name for p in docs.glob("spikes/RESEARCH_*.md")]):
        openers(rel, "spike", SPIKE_OUTCOME)
    openers("audit/" + sdlc_core.PROJECT_NOTES, "project_note")
    for p in sorted(docs.glob("audit/requests/REQUEST_*.md")):
        rel = "audit/requests/" + p.name
        text = _text(p)
        for rid, date, label, _ in sdlc_core.request_entries(text or "")[0]:
            add(date, "request", "%s — %s" % (rid, label), rel)
    rel = "audit/reviews/REVIEW_LOG.md"
    text = _text(docs / rel) if (docs / rel).is_file() else None
    if text is not None:
        for row in sdlc_core.parse_review_log(text)[0]:
            add(row["date"], "review", "%s — %s: %s" % (
                row["doc_key"], row["tier"], row["verdict"]), rel)
    for p in sorted(docs.glob("architecture/ADR_*.md")):
        rel = "architecture/" + p.name
        text = _text(p)
        date = sdlc_core.adr_date(p.name, text or "")
        if date:
            add(date, "decision", title_of(rel, text or ""), rel)
    for folder, kind, suffix in (("corpus/notes", "note", ".md"),
                                 ("corpus/given", "source", ".meta.md")):
        for p in sorted(docs.glob(folder + "/*" + suffix)):
            rel = folder + "/" + p.name
            text = _text(p)
            if text is None:
                continue
            date = knowledge.frontmatter_date(
                sdlc_core.load_frontmatter(text.splitlines()))
            if not date:
                continue
            if kind == "source":
                name = p.name[:-len(suffix)]
                add(date, kind, name, rel, source=name)
            else:
                add(date, kind, title_of(rel, text), rel)
    # Most recent first. Within one day a document's later entry is the more recent
    # one, so the reading order is reversed too. Entries carry no time of day, so
    # between DIFFERENT documents on one day the order is fixed but not a time order:
    # the kinds come in the reverse of the reading order above.
    ranked = sorted(enumerate(events), key=lambda ne: (ne[1]["date"], ne[0]), reverse=True)
    return [e for _, e in ranked]


# ----------------------------------------------------------------- writing

def _js(var, obj):
    s = json.dumps(obj, ensure_ascii=True, separators=(",", ":"))
    return "window.%s = %s;\n" % (var, s.replace("<", "\\u003c"))


def check_out(out, docs):
    out = out.resolve()
    d = docs.resolve()
    if out == d or d in out.parents:
        raise SiteError("--out %s is inside the docs root %s: the site is written outside it."
                        % (out, d))
    if out.exists() and not out.is_dir():
        raise SiteError("--out %s exists and is not a folder." % out)
    if out.is_dir() and any(out.iterdir()) and not (out / MARKER).is_file():
        raise SiteError("--out %s is not empty and was not written by this generator: "
                        "refusing to write over it." % out)
    return out


def write_site(out, core, pages, kb):
    out.mkdir(parents=True, exist_ok=True)
    for rel in PAGE_FILES + ("data",):
        p = out / rel
        if p.is_dir():
            shutil.rmtree(p)
        elif p.exists():
            p.unlink()
    (out / MARKER).write_text("Written by docs_site.py; regenerated on every run.\n",
                              encoding="utf-8", newline="\n")
    for name in PAGE_FILES:
        shutil.copyfile(PAGE_DIR / name, out / name)
    data = out / "data"
    data.mkdir()
    (data / "core.js").write_text(_js("DOCS_SITE_CORE", core), encoding="utf-8", newline="\n")
    (data / "docs.js").write_text(_js("DOCS_SITE_DOCS", pages), encoding="utf-8", newline="\n")
    if kb:
        (data / "kb.js").write_text(_js("DOCS_SITE_KB", kb), encoding="utf-8", newline="\n")


def git_ignored(project, out):
    if not sdlc_core.git_available(project):
        return None
    try:
        out.relative_to(project.resolve())
    except ValueError:
        return None                    # outside the repository: nothing to commit
    try:
        r = subprocess.run(["git", "check-ignore", "-q", str(out)], cwd=str(project),
                           capture_output=True, text=True, timeout=10)
        return {0: True, 1: False}.get(r.returncode)
    except Exception:
        return None


def _shown(path, docs):
    try:
        return Path(path).relative_to(docs).as_posix()
    except ValueError:
        return str(path)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="docs_site.py",
        description="Generate a static, read-only site of what the agent reads in this project.")
    ap.add_argument("--root", help="project root (default: discovered from the current folder)")
    ap.add_argument("--docs-dir", dest="docs_dir", help="docs root name (ai_docs or mkt_docs)")
    ap.add_argument("--out", help="output folder (default: <project>/%s)" % DEFAULT_OUT)
    ap.add_argument("--open", action="store_true", help="open the site in the browser")
    args = ap.parse_args(argv)
    del _UNREADABLE[:]
    try:
        project, docs, name = resolve_root(args)
        out = check_out(Path(args.out) if args.out else project / DEFAULT_OUT, docs)
    except SiteError as exc:
        print("[ERROR] %s" % exc)
        return 2
    if not PAGE_DIR.is_dir():
        print("[ERROR] the page files are missing: %s (reinstall the skill)" % PAGE_DIR)
        return 2
    try:
        with _GuardedReads():
            core, pages, kb = build(project, docs, name)
    except OSError as exc:
        # a reader that bypasses read_text (raw bytes) met an unreadable file
        _note_unreadable(getattr(exc, "filename", None) or "?", exc)
        for path, err in _UNREADABLE:
            print("[ERROR] unreadable: %s (%s)" % (_shown(path, docs), err))
        print("[ERROR] the site was not written: fix the file's permissions and run again.")
        return 1
    write_site(out, core, pages, kb)
    print("[ok] docs site written: %s (%d documents%s, from %s)" % (
        out / "index.html", len(pages),
        ", %d topics, %d facts" % (len(kb["order"]), len(kb["facts"])) if kb else "", docs))
    for path, exc in _UNREADABLE:
        print("[ERROR] unreadable: %s (%s)" % (_shown(path, docs), exc))
    if git_ignored(project, out) is False:
        print("[note] %s is not git-ignored: add it to .gitignore so the site's copy of "
              "your documents is not committed." % out)
    if args.open:
        import webbrowser
        webbrowser.open((out / "index.html").as_uri())
    return 1 if _UNREADABLE else 0


if __name__ == "__main__":
    sys.exit(main())
