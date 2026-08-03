#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KB Agentic — the KNOWLEDGE domain entry point, and its overlay.

The family's shared spine lives in `sdlc_core.py`, byte-identical in every
distribution; this file is the knowledge OVERLAY on top of it. Since F-024/F-025
it is deliberately not thin: the claim ledger (assertions with provenance, held
conflicts) and the topic graph (placement, edges, integrity) are genuinely this
domain's own and stay here. What converges is the spine, not the knowledge.

From the overlay:
  claim-id <path> <locator> [--qty "..."]   compute a claim id
  claim-id --fill <file>                    fill missing ids in a claim table
  graph    [--root R]                       topic-graph integrity checks
  corpus   [--root R]                       corpus checks (supersession, digests)
  index / validate / check                  spine behaviour PLUS the kb surface
                                            (byte-identical output on a tree
                                            with no topics/ or corpus/)

Every other spine subcommand (stale, mark, gate, orient, plan, migrate, and any
future one) is FORWARDED to the spine untouched: dispatch is "not intercepted ->
forward", never a hand-copied command tuple, so a new spine command cannot be
silently dropped here.

Both files must sit in the same directory. Copying this one alone fails at
import, loudly, which is the intended failure. The core alone stays runnable,
but for kb it no longer behaves identically: it runs none of the claim or graph
checks (ENFORCEMENT.md says so).

Pure stdlib. ASCII output only (Windows-console safe).
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import sdlc_core
except ImportError as exc:  # pragma: no cover - exercised by TS12, not by unit tests
    sys.stderr.write(
        "[ERROR] sdlc_check.py cannot find sdlc_core.py next to it: " + str(exc) + "\n"
        "        The validator ships as TWO files since the multi-domain core.\n"
        "        Copy both, or run sdlc_core.py directly.\n")
    sys.exit(1)

# Re-export the core's surface: existing importers (`import sdlc_check as sc`)
# and the test batteries reach for these names on this module. The shared
# batteries bind `sdlc_core` directly, so nothing defined below can shadow what
# they test; overlay names carry a kb_ prefix for readability, not as a guard.
from sdlc_core import *            # noqa: F401,F403
from sdlc_core import _map_refs    # noqa: F401  underscore helper used by the batteries

DOMAIN = "knowledge"

sdlc_core.set_entry_point(DOMAIN, provides=("code", "knowledge"))

sdlc_core.set_profile(
    skill_name="kb-agentic",
    unit_noun="topic",
    support_files=("templates.md", "taxonomy.md", "guides.md", "vision.md",
                   "distillation.md", "reconciliation.md", "elicitation.md",
                   "review.md", "dispatch.md", "routing.md", "ENFORCEMENT.md"),
    capabilities=(
        # spine
        "triage", "write_triggers", "workstream_registry", "vision_gate",
        "design_review_gate", "guide_router", "worktree_hygiene",
        # knowledge overlay
        "taxonomy_pass", "subagent_dispatch", "question_discipline",
    ),
    design_gate_between=("### 3. Request Analysis & Taxonomy Pass",
                         "### 4. Knowledge Processing & Distillation"),
)

# --------------------------------------------------------------- claim ledger
# F-025. The machine detects and holds; it never decides. Every function below
# is pure and stdlib — the battery calls them directly.

CLAIM_COLUMNS = ("id", "claim", "valid", "qty", "about", "source", "prov", "state")
CLAIM_HEADING = "## Claims"
PROVENANCES = ("GIVEN", "ELICITED", "DERIVED", "RULING")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
OWNS_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}/[a-z0-9][a-z0-9-]{0,63}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LOC_PAGE_RE = re.compile(r"^p=(\d+)@(\d+)-(\d+)$")
LOC_LINE_RE = re.compile(r"^L(\d+)-(\d+)$")
LOC_CELL_RE = re.compile(r"^Sheet[^!]+![A-Z]+\d+$")

# Unit conventions, documented in templates.md. effort in person-days
# (8h day, 5d week, 21d month); duration in calendar days; cost within ONE
# currency (no exchange rates offline); count unit-matched.
QTY_UNITS = {
    "effort":   {"h": 0.125, "d": 1.0, "w": 5.0, "mo": 21.0, "fte-mo": 21.0},
    "duration": {"h": 1.0 / 24, "d": 1.0, "w": 7.0, "mo": 30.0},
}


def kb_qty_norm(text):
    """'12000 EUR cost' -> ('cost', 12000.0, 'EUR') or None for '-'.

    Raises ValueError on anything else: a malformed quantity must be a finding,
    never a silently-ignored cell.
    """
    text = (text or "").strip()
    if text in ("", "-"):
        return None
    parts = text.split()
    if len(parts) != 3:
        raise ValueError("qty must be '<value> <unit> <kind>' or '-': %r" % text)
    value, unit, kind = parts
    try:
        value = float(value)
    except ValueError:
        raise ValueError("qty value is not a number: %r" % text)
    if kind not in ("effort", "cost", "duration", "count"):
        raise ValueError("qty kind must be effort/cost/duration/count: %r" % text)
    if kind in QTY_UNITS and unit not in QTY_UNITS[kind]:
        raise ValueError("unknown %s unit %r (known: %s)"
                         % (kind, unit, "/".join(sorted(QTY_UNITS[kind]))))
    return kind, value, unit


def kb_qty_key(text):
    """The id component: 'cost:12000:EUR', or '' when the row carries no qty."""
    q = kb_qty_norm(text)
    if q is None:
        return ""
    kind, value, unit = q
    return "%s:%s:%s" % (kind, ("%g" % value), unit)


def kb_qty_sum(rows_qty):
    """Sum ('kind', value, unit) triples of ONE kind. Returns (total, unit).

    effort/duration normalise to days; cost sums within one currency and
    REFUSES a mixed-currency set; count requires one unit. Mixed kinds refuse.
    """
    triples = [kb_qty_norm(q) for q in rows_qty]
    triples = [t for t in triples if t]
    if not triples:
        return None
    kinds = {t[0] for t in triples}
    if len(kinds) > 1:
        raise ValueError("mixed qty kinds cannot sum: %s" % "/".join(sorted(kinds)))
    kind = triples[0][0]
    if kind in QTY_UNITS:
        total = sum(v * QTY_UNITS[kind][u] for _, v, u in triples)
        return total, "d"
    units = {t[2] for t in triples}
    if len(units) > 1:
        raise ValueError("mixed %s units cannot sum offline: %s"
                         % (kind, "/".join(sorted(units))))
    return sum(v for _, v, _ in triples), triples[0][2]


def kb_claim_id(source_path, locator, qty_key=""):
    """First 12 hex of sha256(path#locator#qty). Text excluded on purpose:
    an LLM re-extraction paraphrases; the location and the figure do not move."""
    payload = "%s#%s#%s" % (source_path, locator, qty_key)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def kb_parse_scope(text):
    """'-' | 'from X' | 'until X' | 'from X until Y' | 'if <cond>' ->
    ('always',) | ('window', from, until) | ('if', cond). Raises on junk."""
    text = (text or "").strip()
    if text in ("", "-"):
        return ("always",)
    if text.startswith("if "):
        return ("if", text[3:].strip())
    m = re.match(r"^(?:from (\S+))?\s*(?:until (\S+))?$", text)
    if not m or (m.group(1) is None and m.group(2) is None):
        raise ValueError("valid must be '-', 'from X', 'until X', "
                         "'from X until Y' or 'if <cond>': %r" % text)
    lo, hi = m.group(1), m.group(2)
    for d in (lo, hi):
        if d is not None and not DATE_RE.match(d):
            raise ValueError("scope dates are YYYY-MM-DD: %r" % text)
    return ("window", lo, hi)


def kb_scopes_overlap(a, b):
    """Half-open windows: `from` inclusive, `until` exclusive — so
    'until 2026-03-01' and 'from 2026-03-01' are DISJOINT. 'if' conditions are
    free text, undecidable, therefore treated as overlapping everything."""
    sa, sb = kb_parse_scope(a), kb_parse_scope(b)
    if sa[0] == "if" or sb[0] == "if" or sa[0] == "always" or sb[0] == "always":
        return True
    _, alo, ahi = sa
    _, blo, bhi = sb
    lo = max(alo or "0000-00-00", blo or "0000-00-00")
    hi = min(ahi or "9999-99-99", bhi or "9999-99-99")
    return lo < hi


def kb_parse_claims(text):
    """Rows of the `## Claims` table -> (rows, errors).

    Exact arity in BOTH directions: a short row and a long row both error —
    never padded, never truncated. (The mkt find_table pattern this copies
    tolerates a ragged tail; here a stray `|` in a hostile cell must be loud.)
    Each row: dict with CLAIM_COLUMNS keys + '_line' (1-based, for findings).
    """
    rows, errors = [], []
    lines = text.split("\n")
    try:
        start = next(i for i, ln in enumerate(lines)
                     if ln.strip() == CLAIM_HEADING)
    except StopIteration:
        return [], []
    header_seen = False
    for i in range(start + 1, len(lines)):
        ln = lines[i].strip()
        if ln.startswith("## "):
            break
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if not header_seen:
            header_seen = True          # header row
            if [c.lower() for c in cells] != list(CLAIM_COLUMNS):
                errors.append((i + 1, "claim table header must be exactly: "
                               + " | ".join(CLAIM_COLUMNS)))
                return [], errors
            continue
        if set(ln) <= {"|", "-", " ", ":"}:
            continue                    # separator row
        if len(cells) != len(CLAIM_COLUMNS):
            errors.append((i + 1, "claim row has %d cells, expected %d "
                           "(a '|' inside a cell must be escaped)"
                           % (len(cells), len(CLAIM_COLUMNS))))
            continue
        row = dict(zip(CLAIM_COLUMNS, cells))
        row["_line"] = i + 1
        rows.append(row)
    return rows, errors


def kb_fill_ids(text):
    """Fill empty id cells from source#locator#qty. The byte diff is confined
    to id cells: everything else comes back verbatim (TL-T6)."""
    lines = text.split("\n")
    rows, _ = kb_parse_claims(text)
    for row in rows:
        if row["id"]:
            continue
        src = row["source"].split(";")[0].strip()
        if "#" not in src:
            continue
        path, loc = src.rsplit("#", 1)
        try:
            qk = kb_qty_key(row["qty"])
        except ValueError:
            continue
        new_id = kb_claim_id(path, loc, qk)
        ln = lines[row["_line"] - 1]
        head, rest = ln.split("|", 2)[0], ln.split("|", 2)[2]
        first_cell = ln.split("|", 2)[1]
        lines[row["_line"] - 1] = "%s|%s|%s" % (
            head, first_cell.replace(first_cell.strip() or "\x00", new_id)
            if first_cell.strip() else " " + new_id + " ", rest)
    return "\n".join(lines)


def _note_frontmatter(root, rel):
    p = root / rel
    if not p.is_file():
        return None
    return sdlc_core.load_frontmatter(sdlc_core.read_text(p).splitlines()) or {}


def kb_check_claims(root):
    """All mechanical claim checks over topics/*.md. Returns (errors, warnings,
    notes) as message lists. Findings only — never per-node status lines."""
    errors, warnings, notes = [], [], []
    topics = root / "topics"
    if not topics.is_dir():
        return errors, warnings, notes
    all_ids = {}     # id -> "file:line"
    all_rows = {}    # id -> (row, rel)
    per_file_rows = []
    for p in sorted(topics.glob("*.md")):
        rel = "topics/" + p.name
        text = sdlc_core.read_text(p)
        rows, perrs = kb_parse_claims(text)
        for line, msg in perrs:
            errors.append("%s:%d: %s" % (rel, line, msg))
        per_file_rows.append((rel, rows))
        for row in rows:
            where = "%s:%d" % (rel, row["_line"])
            # --- source: resolve, confine, span-check ---
            sources = [s.strip() for s in row["source"].split(";") if s.strip()]
            if not sources:
                errors.append("%s: claim has no source" % where)
                continue
            first = sources[0]
            for src in sources:
                if "#" not in src:
                    errors.append("%s: source %r has no locator" % (where, src))
                    continue
                path_s, loc = src.rsplit("#", 1)
                target = sdlc_core.confine_under(root, path_s)
                if target is None:
                    errors.append("%s: source %r escapes the docs root" % (where, src))
                    continue
                if not target.is_file():
                    errors.append("%s: source %r does not resolve — a claim whose "
                                  "origin cannot be reopened is model knowledge"
                                  % (where, src))
                    continue
                kb_check_locator(target, loc, where, errors)
            # --- provenance ---
            prov = row["prov"]
            if prov not in PROVENANCES:
                errors.append("%s: prov %r not in %s" % (where, prov, "/".join(PROVENANCES)))
            elif prov in ("DERIVED", "RULING", "ELICITED"):
                meta = _note_frontmatter(root, first.rsplit("#", 1)[0])
                if meta is None:
                    pass  # unresolvable source already reported
                elif prov == "DERIVED" and not meta.get("derived_from"):
                    errors.append("%s: DERIVED claim's note carries no 'derived_from:' "
                                  "— model knowledge disguised as a source" % where)
                elif prov == "RULING" and not meta.get("basis"):
                    errors.append("%s: RULING note carries no 'basis:' — a preference "
                                  "is not a fact; no basis, no ruling" % where)
            # --- grammar cells ---
            try:
                kb_parse_scope(row["valid"])
            except ValueError as e:
                errors.append("%s: %s" % (where, e))
            try:
                qk = kb_qty_key(row["qty"])
            except ValueError as e:
                errors.append("%s: %s" % (where, e))
                qk = None
            if row["about"] not in ("", "-"):
                m = re.match(r"^([a-z0-9-]+) -> ([a-z0-9-]+)$", row["about"])
                if not m:
                    errors.append("%s: about must be '<predicate> -> <slug>' or '-'"
                                  % where)
            # --- id: recompute, or note fill-pending ---
            if not row["id"]:
                notes.append("%s: id missing — fill-pending, run "
                             "'sdlc_check.py claim-id --fill %s'" % (where, rel))
            elif qk is not None and "#" in first:
                path_s, loc = first.rsplit("#", 1)
                expect = kb_claim_id(path_s, loc, qk)
                if row["id"] != expect:
                    errors.append("%s: id %s does not recompute from its first "
                                  "source (+qty) — expected %s; the text may be "
                                  "corrected freely, the provenance may not be "
                                  "moved silently" % (where, row["id"], expect))
            if row["id"]:
                if row["id"] in all_ids:
                    errors.append("%s: duplicate id %s (also at %s) — uniqueness "
                                  "is global across topics/" % (where, row["id"],
                                                                all_ids[row["id"]]))
                else:
                    all_ids[row["id"]] = where
                    all_rows[row["id"]] = (row, rel)
    # --- state machine integrity, global ---
    for _, rows in per_file_rows:
        for row in rows:
            if not row["id"]:
                continue
            where = all_ids.get(row["id"], row["id"])
            state = row["state"]
            if state == "OK":
                continue
            m = re.match(r"^(CONTESTED|SUPERSEDED) ([0-9a-f, ]+)$", state)
            if not m:
                errors.append("%s: state must be OK, 'CONTESTED <id>[,..]' or "
                              "'SUPERSEDED <id>': %r" % (where, state))
                continue
            kind = m.group(1)
            targets = [t.strip() for t in m.group(2).split(",") if t.strip()]
            for t in targets:
                other = all_rows.get(t)
                if other is None:
                    errors.append("%s: %s points at id %s which resolves to no row "
                                  "— deleting one side of a disagreement breaks "
                                  "the check, it does not clean up" % (where, kind, t))
                    continue
                orow, _ = other
                if kind == "CONTESTED":
                    if orow["state"].startswith("SUPERSEDED"):
                        errors.append("%s: CONTESTED points at SUPERSEDED row %s — "
                                      "the set must be rewritten when a member is "
                                      "superseded" % (where, t))
                    elif not (orow["state"].startswith("CONTESTED")
                              and row["id"] in orow["state"]):
                        errors.append("%s: CONTESTED is not symmetric — %s does not "
                                      "name %s back; one flipped cell must never "
                                      "silently end a disagreement"
                                      % (where, t, row["id"]))
    return errors, warnings, notes


def kb_check_locator(target, loc, where, errors):
    """A locator must address an existing span of the stored bytes."""
    m = LOC_PAGE_RE.match(loc)
    if m:
        page, a, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if a >= b:
            errors.append("%s: locator %r has an empty span" % (where, loc))
            return
        # offsets address the stored extraction (<stem>.txt beside the original)
        ext = target if target.suffix == ".txt" else target.with_suffix(".txt")
        if not ext.is_file():
            errors.append("%s: no stored extraction %s for locator %r — offsets "
                          "must address kept bytes" % (where, ext.name, loc))
            return
        pages = sdlc_core.read_text(ext).split("\f")
        if page < 1 or page > len(pages):
            errors.append("%s: locator %r addresses page %d of %d" %
                          (where, loc, page, len(pages)))
        elif b > len(pages[page - 1]):
            errors.append("%s: locator %r spans past the end of page %d "
                          "(%d chars)" % (where, loc, page, len(pages[page - 1])))
        return
    m = LOC_LINE_RE.match(loc)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if a > b or a < 1:
            errors.append("%s: locator %r has an invalid line range" % (where, loc))
            return
        n = sdlc_core.read_text(target).count("\n") + 1
        if b > n:
            errors.append("%s: locator %r spans past line %d" % (where, loc, n))
        return
    if not LOC_CELL_RE.match(loc):
        errors.append("%s: locator %r matches no known form "
                      "(p=<n>@<a>-<b> / L<a>-<b> / Sheet<s>!<cell>)" % (where, loc))


def kb_anchor_pattern(phrase, ignore_case=False):
    """A phrase, compiled so it survives the line wraps an extraction introduces.

    Every run of whitespace in the phrase becomes `\\s+`: a PDF extraction breaks
    phrases mid-line, so a literal space matches nothing while a probe that
    pretty-prints collapsed whitespace shows the phrase intact. That gap cost a
    field user two full generation rounds."""
    tokens = [t for t in re.split(r"\s+", phrase.strip()) if t]
    if not tokens:
        return None
    body = r"\s+".join(re.escape(t) for t in tokens)
    return re.compile(body, re.IGNORECASE if ignore_case else 0)


def kb_resolve_anchor(target, phrase, ignore_case=False, page=None):
    """Locate a phrase in stored bytes and return [(locator, context), ...].

    The stored form decides the locator form: form-feeds mean paged bytes and
    offsets are counted inside the page, exactly as `kb_check_locator` reads
    them; otherwise line numbers. Every locator produced here is re-verified with
    that same checker before it is returned, so this can never emit a span its
    own validator would reject."""
    rx = kb_anchor_pattern(phrase, ignore_case)
    if rx is None:
        return []
    # Read what the checker will read: for a non-text original the stored
    # extraction beside it holds the bytes offsets address. `target` stays as
    # given, because that is the path the claim's `source` cell will carry and
    # therefore the path the round-trip below must verify.
    ext = target if target.suffix == ".txt" else target.with_suffix(".txt")
    text = sdlc_core.read_text(ext if ext.is_file() else target)
    hits = []
    if "\f" in text:
        for idx, body in enumerate(text.split("\f"), start=1):
            if page is not None and idx != page:
                continue
            for m in rx.finditer(body):
                hits.append(("p=%d@%d-%d" % (idx, m.start(), m.end()),
                             body[max(0, m.start() - 40):m.end() + 40]))
    else:
        lines = text.splitlines()
        starts, pos = [], 0
        for ln in lines:
            starts.append(pos)
            pos += len(ln) + 1
        for m in rx.finditer(text):
            a = sum(1 for s in starts if s <= m.start())
            b = sum(1 for s in starts if s <= m.end() - 1)
            hits.append(("L%d-%d" % (a, b),
                         text[max(0, m.start() - 40):m.end() + 40]))
    verified = []
    for loc, ctx in hits:
        errs = []
        kb_check_locator(target, loc, "anchor", errs)
        if not errs:
            verified.append((loc, ctx))
    return verified


# ---------------------------------------------------------------- topic graph
# F-024. Findings only; the graph is held in memory, rebuilt per run.

def kb_load_topics(root):
    """topics/*.md -> {slug: meta+body info}. The files ARE the state."""
    nodes = {}
    topics = root / "topics"
    if not topics.is_dir():
        return nodes
    for p in sorted(topics.glob("*.md")):
        if p.name == "INDEX.md":
            continue
        meta = sdlc_core.load_frontmatter(sdlc_core.read_text(p).splitlines()) or {}
        slug = (meta.get("topic") or p.stem).strip()
        nodes[slug] = {"meta": meta, "file": "topics/" + p.name}
    return nodes


def _as_list(v):
    if v is None:
        return []
    if isinstance(v, str):
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            return [x.strip() for x in v[1:-1].split(",") if x.strip()]
        return [v] if v else []
    return list(v)


def kb_graph_check(root):
    """Integrity of the topic graph. Errors/warnings only — never a per-node
    status line (the work-management Non-Goal forbids the collected surface)."""
    errors, warnings = [], []
    nodes = kb_load_topics(root)
    if not nodes:
        return errors, warnings
    import difflib
    live = {s: n for s, n in nodes.items()
            if (n["meta"].get("status") or "").strip() != "SUPERSEDED"}

    def resolve(slug):
        """Follow tombstone redirects to a live slug, or None."""
        seen = set()
        while slug in nodes and slug not in seen:
            seen.add(slug)
            n = nodes[slug]
            if (n["meta"].get("status") or "").strip() == "SUPERSEDED":
                slug = (n["meta"].get("redirect_to") or "").strip()
                continue
            return slug
        return None

    owns_seen = {}
    for slug, n in nodes.items():
        rel = n["file"]
        if not SLUG_RE.match(slug):
            errors.append("%s: slug %r fails the grammar ^[a-z0-9][a-z0-9-]{0,63}$"
                          % (rel, slug))
        if (n["meta"].get("status") or "").strip() == "SUPERSEDED":
            tgt = (n["meta"].get("redirect_to") or "").strip()
            if not tgt or resolve(tgt) is None:
                errors.append("%s: tombstone redirect_to %r resolves to no live node"
                              % (rel, tgt))
            continue
        for parent in _as_list(n["meta"].get("parents")):
            if not SLUG_RE.match(parent):
                errors.append("%s: parent %r fails the slug grammar" % (rel, parent))
            elif resolve(parent) is None:
                errors.append("%s: parent %r resolves to no live node" % (rel, parent))
        for c in _as_list(n["meta"].get("owns")):
            if not OWNS_RE.match(c):
                errors.append("%s: owns entry %r fails the grammar "
                              "<slug>/<concept>" % (rel, c))
            elif c in owns_seen:
                errors.append("%s: concept %r owned twice (also by %s) — one owner "
                              "per concept" % (rel, c, owns_seen[c]))
            else:
                owns_seen[c] = rel
        rl = (n["meta"].get("related") or "").strip()
        if rl and resolve(rl) is None:
            errors.append("%s: related %r resolves to no live node" % (rel, rl))
    # cycles + reachability on primary parents, live nodes only
    roots = [s for s, n in live.items() if not _as_list(n["meta"].get("parents"))]
    for slug, n in live.items():
        seen = set()
        cur = slug
        while cur is not None:
            if cur in seen:
                errors.append("%s: cycle through %r — a detached ring is invisible "
                              "to descent forever" % (n["file"], cur))
                break
            seen.add(cur)
            parents = _as_list(live.get(cur, {}).get("meta", {}).get("parents")) \
                if cur in live else []
            cur = resolve(parents[0]) if parents else None
    if roots:
        reachable = set()
        frontier = list(roots)
        children = {}
        for s, n in live.items():
            for parent in _as_list(n["meta"].get("parents")):
                rp = resolve(parent)
                if rp:
                    children.setdefault(rp, []).append(s)
        while frontier:
            cur = frontier.pop()
            if cur in reachable:
                continue
            reachable.add(cur)
            frontier.extend(children.get(cur, []))
        for slug, n in live.items():
            if slug not in reachable and slug != "unplaced":
                errors.append("%s: unreachable from any root — descent is the only "
                              "retrieval path, so this node is lost, not odd"
                              % n["file"])
    # near-duplicate warning: catches listino/listini, not listino/pricing
    slugs = sorted(live)
    for i, a in enumerate(slugs):
        for b in slugs[i + 1:]:
            pa = _as_list(live[a]["meta"].get("parents"))
            pb = _as_list(live[b]["meta"].get("parents"))
            if pa and pa == pb and difflib.SequenceMatcher(None, a, b).ratio() > 0.85:
                warnings.append("%s and %s: same parents and >0.85 name similarity — "
                                "possible duplicate; the semantic case belongs to "
                                "the router evals" % (a, b))
    return errors, warnings


def kb_build_topic_index(root):
    """slug | description | parents | synonyms — a router, not a status board."""
    nodes = kb_load_topics(root)
    lines = ["# Topic Index", "",
             "<!-- GENERATED by sdlc_check.py index - do not edit by hand -->", "",
             "| topic | description | parents | synonyms |",
             "|---|---|---|---|"]
    for slug in sorted(nodes):
        n = nodes[slug]
        if (n["meta"].get("status") or "").strip() == "SUPERSEDED":
            continue
        lines.append("| %s | %s | %s | %s |" % (
            slug, (n["meta"].get("description") or "").strip(),
            ", ".join(_as_list(n["meta"].get("parents"))),
            ", ".join(_as_list(n["meta"].get("synonyms")))))
    return "\n".join(lines) + "\n"


def kb_build_corpus_index(root):
    """One row per corpus artifact, from sidecars and note frontmatter."""
    corpus = root / "corpus"
    lines = ["# Corpus Index", "",
             "<!-- GENERATED by sdlc_check.py index - do not edit by hand -->", ""]
    given = corpus / "given"
    if given.is_dir():
        lines.append("## given/")
        for meta_p in sorted(given.glob("*.meta.md")):
            meta = sdlc_core.load_frontmatter(sdlc_core.read_text(meta_p).splitlines()) or {}
            orig = meta_p.name[:-len(".meta.md")]
            sup = (meta.get("supersedes") or "").strip()
            lines.append("- `%s` — %s%s" % (
                orig, (meta.get("date") or "undated"),
                (" — supersedes `%s`" % sup) if sup else ""))
    notes = corpus / "notes"
    if notes.is_dir():
        lines.append("")
        lines.append("## notes/")
        for p in sorted(notes.glob("*.md")):
            meta = sdlc_core.load_frontmatter(sdlc_core.read_text(p).splitlines()) or {}
            origin = (meta.get("origin") or
                      ("derived" if meta.get("derived_from") else
                       ("ruling" if meta.get("basis") else "unknown")))
            lines.append("- `%s` — %s" % (p.name, origin))
    return "\n".join(lines) + "\n"


def kb_corpus_check(root):
    """Corpus integrity: digests, supersession, laundered notes. Findings only."""
    errors, warnings = [], []
    corpus = root / "corpus"
    if not corpus.is_dir():
        return errors, warnings
    superseded = set()
    given = corpus / "given"
    if given.is_dir():
        for meta_p in sorted(given.glob("*.meta.md")):
            meta = sdlc_core.load_frontmatter(sdlc_core.read_text(meta_p).splitlines()) or {}
            orig = given / meta_p.name[:-len(".meta.md")]
            rel = "corpus/given/" + orig.name
            if not orig.is_file():
                errors.append("%s: sidecar exists but the original is gone" % rel)
                continue
            recorded = (meta.get("sha256") or "").strip()
            if recorded:
                actual = kb_sha256_bytes(orig)
                if actual != recorded:
                    errors.append("%s: raw-byte digest changed since ingest — "
                                  "given/ is never edited; this is the check, "
                                  "not a convention" % rel)
            sup = (meta.get("supersedes") or "").strip()
            if sup:
                superseded.add(sup)
                if not (given / sup).is_file():
                    warnings.append("%s: supersedes %r which is not in given/"
                                    % (rel, sup))
    notes = corpus / "notes"
    if notes.is_dir():
        for p in sorted(notes.glob("*.md")):
            meta = sdlc_core.load_frontmatter(sdlc_core.read_text(p).splitlines()) or {}
            if not (meta.get("derived_from") or meta.get("origin")
                    or meta.get("basis")):
                errors.append("corpus/notes/%s: neither 'derived_from:' nor "
                              "'origin:' nor 'basis:' — model knowledge disguised "
                              "as a source" % p.name)
    # claims resting on superseded originals (UC4)
    if superseded:
        topics = root / "topics"
        if topics.is_dir():
            for p in sorted(topics.glob("*.md")):
                rows, _ = kb_parse_claims(sdlc_core.read_text(p))
                for row in rows:
                    for src in row["source"].split(";"):
                        name = Path(src.split("#")[0].strip()).name
                        if name in superseded:
                            warnings.append(
                                "topics/%s:%d: claim rests on %s, which a newer "
                                "version supersedes — re-verify or re-place"
                                % (p.name, row["_line"], name))
    return errors, warnings


def kb_sha256_bytes(path):
    """RAW-byte digest for binaries. The spine's sha256_file normalizes CRLF->LF
    (right for text snapshots, wrong for binaries, where a hostile 0D0A/0A pair
    would collide)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------ commands

INTERCEPTED = {"index", "validate", "check", "graph", "corpus", "claim-id",
               "anchor"}


def _kb_root(args):
    """Resolve the PROJECT root exactly as the spine's main does, so --docs-dir,
    the env seam and the two-roots-refuse behaviour hold on intercepted commands.
    Same call, same order: resolve_docs_dir(args, root) -> (discovered, name).
    Spine cmd_* take the project root; kb helpers take the docs root under it."""
    discovered, name = sdlc_core.resolve_docs_dir(args, getattr(args, "root", None))
    sdlc_core.set_docs_dir(name)
    root = (Path(args.root).resolve() if args.root
            else (discovered or sdlc_core.find_project_root()))
    return root, root / name


def kb_cmd_graph(docs):
    errors, warnings = kb_graph_check(docs)
    ce, cw, cn = kb_check_claims(docs)
    for w in warnings + cw:
        print("[warn]  %s" % w)
    for n in cn:
        print("[note]  %s" % n)
    for e in errors + ce:
        print("[ERROR] %s" % e)
    total_e = len(errors) + len(ce)
    if total_e:
        print("Graph: %d errors, %d warnings." % (total_e, len(warnings) + len(cw)))
        return 1
    if not (docs / "topics").is_dir():
        print("[ok] no topics/ - nothing to check")
    else:
        print("[ok] topic graph and claim ledger consistent "
              "(%d warnings)" % (len(warnings) + len(cw)))
    return 0


def kb_cmd_corpus(docs):
    errors, warnings = kb_corpus_check(docs)
    for w in warnings:
        print("[warn]  %s" % w)
    for e in errors:
        print("[ERROR] %s" % e)
    if errors:
        print("Corpus: %d errors, %d warnings." % (len(errors), len(warnings)))
        return 1
    if not (docs / "corpus").is_dir():
        print("[ok] no corpus/ - nothing to check")
    else:
        print("[ok] corpus consistent (%d warnings)" % len(warnings))
    return 0


def kb_cmd_index(root, docs):
    rc = sdlc_core.cmd_index(root)
    if (docs / "topics").is_dir():
        out = docs / "topics" / "INDEX.md"
        out.write_text(kb_build_topic_index(docs), encoding="utf-8")
        print("[ok] topic index regenerated: %s" % out)
    if (docs / "corpus").is_dir():
        out = docs / "corpus" / "INDEX.md"
        out.write_text(kb_build_corpus_index(docs), encoding="utf-8")
        print("[ok] corpus index regenerated: %s" % out)
    return rc


def _kb_extra_validate(docs):
    """The kb additions to validate: generated-index freshness for the overlay's
    two indexes. Prints nothing on a tree without them (TS-K7)."""
    rc = 0
    checks = (("topics", kb_build_topic_index), ("corpus", kb_build_corpus_index))
    for dirname, builder in checks:
        idx = docs / dirname / "INDEX.md"
        if (docs / dirname).is_dir() and idx.is_file():
            if sdlc_core.norm_text(sdlc_core.read_text(idx)) != \
               sdlc_core.norm_text(builder(docs)):
                print("[ERROR] %s/INDEX.md not aligned: run 'sdlc_check.py index'"
                      % dirname)
                rc = 1
    return rc


def kb_cmd_validate(root, docs, strict=False, hybrid=False):
    rc = sdlc_core.cmd_validate(root, strict=strict, hybrid=hybrid)
    return max(rc, _kb_extra_validate(docs))


def kb_cmd_check(root, docs, strict=False, hybrid=False):
    # The spine's check owns its banners and summary line: reuse it whole, so a
    # tree with no kb surface gets byte-identical output. The kb checks run
    # after, and only when the surface exists.
    rc = sdlc_core.cmd_check(root, strict=strict, hybrid=hybrid)
    rc = max(rc, _kb_extra_validate(docs))
    if (docs / "topics").is_dir() or (docs / "corpus").is_dir():
        print("===== graph =====")
        rc = max(rc, kb_cmd_graph(docs))
        print("===== corpus =====")
        rc = max(rc, kb_cmd_corpus(docs))
    return rc


def kb_cmd_claim_id(args):
    if args.fill:
        p = Path(args.path)
        if not p.is_file():
            print("[ERROR] no such file: %s" % p)
            return 2
        before = sdlc_core.read_text(p)
        after = kb_fill_ids(before)
        if after != before:
            p.write_text(after, encoding="utf-8")
            print("[ok] ids filled in %s" % p)
        else:
            print("[ok] nothing to fill in %s" % p)
        return 0
    if not args.locator:
        print("[ERROR] claim-id needs <path> <locator>, or --fill <file>")
        return 2
    print(kb_claim_id(args.path, args.locator, kb_qty_key(args.qty or "-")))
    return 0


def kb_cmd_anchor(args):
    """Prose citation -> a verified span. The half `claim-id` never had."""
    p = Path(args.path)
    if not p.is_file():
        print("[ERROR] no such file: %s" % p)
        return 2
    hits = kb_resolve_anchor(p, args.phrase, ignore_case=args.ignore_case,
                             page=args.page)
    if not hits:
        print("[ERROR] phrase not found in the stored bytes of %s" % p)
        print("        nothing written: a locator you cannot verify is worse "
              "than no locator.")
        return 2
    if len(hits) > 1 and not args.all:
        print("[ERROR] %d matches -- ambiguous, so nothing is emitted. Narrow "
              "the phrase, add --page, or pass --all to see them:" % len(hits))
        for loc, ctx in hits:
            print("        %s" % loc)
        return 2
    for loc, ctx in hits:
        print(loc)
        print("    ...%s..." % " ".join(ctx.split()))
    return 0


def kb_cmd_help():
    """The spine's usage, then the overlay's own commands.

    Forward-by-default sends everything the overlay does not intercept to the
    spine -- including `--help`, whose usage line then lists the spine's nine
    commands and nothing else. A reader concludes the knowledge overlay is not
    installed; it is, and every command below works. Only `-h/--help` AT argv[0]
    lands here, so dispatch is otherwise untouched and a future spine command
    still reaches the spine."""
    try:
        sdlc_core.main(["--help"])
    except SystemExit:
        pass
    print("""
knowledge overlay (kb-agentic) -- also available:
  graph                       topic-graph integrity: placement, edges, cycles
  corpus                      corpus integrity: digests, supersession, notes
  claim-id <path> <locator>   compute a claim id (--fill to fill a whole table)
  anchor <path> <phrase>      resolve a phrase to a verified locator span

  index / validate / check    the spine's behaviour PLUS the claim ledger and
                              the topic graph""")
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    # `--help` is the one flag the overlay must answer for itself: forwarded, it
    # renders the spine's usage and hides every command above (field report,
    # 2026-08-02). Intercepted at argv[0] ONLY.
    if argv and argv[0] in ("-h", "--help"):
        return kb_cmd_help()
    # Forward-by-default: anything not intercepted goes to the spine untouched.
    # Never a hand-copied command tuple - that is how a spine command gets
    # silently dropped (mkt_check.py ships that exact defect with `migrate`).
    if not argv or argv[0] not in INTERCEPTED:
        return sdlc_core.main(argv)
    ap = argparse.ArgumentParser(prog="sdlc_check.py (kb overlay)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("index", "graph", "corpus"):
        p = sub.add_parser(name)
        p.add_argument("--root")
        p.add_argument("--docs-dir")
    for name in ("validate", "check"):
        p = sub.add_parser(name)
        p.add_argument("--root")
        p.add_argument("--docs-dir")
        p.add_argument("--strict", action="store_true")
        p.add_argument("--hybrid", action="store_true")
    p = sub.add_parser("claim-id")
    p.add_argument("path")
    p.add_argument("locator", nargs="?")
    p.add_argument("--qty")
    p.add_argument("--fill", action="store_true")
    p = sub.add_parser("anchor")
    p.add_argument("path")
    p.add_argument("phrase")
    p.add_argument("--page", type=int)
    p.add_argument("--ignore-case", action="store_true")
    p.add_argument("--all", action="store_true")
    args = ap.parse_args(argv)
    if args.cmd == "claim-id":
        return kb_cmd_claim_id(args)
    if args.cmd == "anchor":
        return kb_cmd_anchor(args)
    try:
        root, docs = _kb_root(args)
    except sdlc_core.AmbiguousDocsRoot as e:
        # same behaviour as the spine for non-exempt commands
        print("[ERROR] %s" % e)
        return 1
    if args.cmd == "index":
        return kb_cmd_index(root, docs)
    if args.cmd == "graph":
        return kb_cmd_graph(docs)
    if args.cmd == "corpus":
        return kb_cmd_corpus(docs)
    if args.cmd == "validate":
        return kb_cmd_validate(root, docs, strict=args.strict, hybrid=args.hybrid)
    return kb_cmd_check(root, docs, strict=args.strict, hybrid=args.hybrid)


if __name__ == "__main__":
    sys.exit(main())
