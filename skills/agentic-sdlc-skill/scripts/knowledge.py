#!/usr/bin/env python3
"""Shared project memory and knowledge integrity. No entry-point profile side effects.

Extracted from the KB overlay; the kb_* API and stored formats remain compatible.
Every distribution ships this module alongside its entry point and sdlc_core.py.
"""
import argparse
import codecs
import contextlib
import io
import os
import hashlib
import ntpath
import posixpath
import re
import sys
import time
from pathlib import Path
import sdlc_core
from sdlc_core import *  # compatibility with the existing KB implementation
from sdlc_core import _map_refs

# --------------------------------------------------------------- claim ledger
# F-025. The machine detects and holds; it never decides. Every function below
# is pure and stdlib — the battery calls them directly.

CLAIM_COLUMNS = ("id", "claim", "valid", "qty", "about", "source", "prov", "state")
CLAIM_HEADING = "## Claims"
PROVENANCES = ("GIVEN", "ELICITED", "DERIVED", "RULING", "IMPORTED", "DECLARED")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
OWNS_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}/[a-z0-9][a-z0-9-]{0,63}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LOC_PAGE_RE = re.compile(r"^p=(\d+)@(\d+)-(\d+)$")
LOC_LINE_RE = re.compile(r"^L(\d+)-(\d+)$")
LOC_CELL_RE = re.compile(r"^Sheet[^!]+![A-Z]+\d+$")
# F-031. How far a source has been read, in the unit its locators address.
EXTRACTED_THROUGH_RE = re.compile(r"^(?:complete|p=(\d+)|L(\d+))$")

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


# F-047: bundling tells for the atomicity note in kb_check_claims. Literal
# substrings, deliberately few and conservative: the note is a hint, and a
# noisy hint trains readers to skip notes. Field-calibrated on the motivating
# reviewer-comment shape ("states X, that Y, and that Z").
KB_BUNDLE_HINTS = (", and that ", "; ", ", while ", " and also ")

# F-080: `about` holds relations joined by ';', and one reserved predicate whose
# target is the Standalone ANALYSIS recording a deferred fix of code that does
# not yet honor the claim. The mark has no reverse direction: nothing lists,
# counts or selects claims by it -- only the claim checks and export read it.
KB_NOT_HONORED = "not-yet-honored-by"
KB_ABOUT_RE = re.compile(r"^([a-z0-9-]+) -> ([a-z0-9-]+)$")
KB_NOT_HONORED_RE = re.compile(r"^%s -> ((?:ANALYSIS|SHADOW)_[A-Za-z0-9_-]+)$"
                               % KB_NOT_HONORED)


def kb_about_parts(cell):
    """The ';'-joined parts of an `about` cell; [] for '-' or empty."""
    if cell.strip() in ("", "-"):
        return []
    return [part.strip() for part in cell.split(";")]


def kb_unquote(value):
    """Strip ONE pair of wrapping YAML quotes (then re-strip whitespace).
    load_frontmatter keeps values verbatim by design; paths with spaces force
    quoting, so value-consuming readers unquote at the point of use. Field
    defect 2026-08-28: 102 false dangling original_path warns on one real
    corpus, and a quoted supersedes: would silently MISS the supersession."""
    v = (value or "").strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
        return v[1:-1].strip()
    return v


def frontmatter_date(meta):
    """A note's or a sidecar's `date:` as `YYYY-MM-DD`, or None (F-073).
    Quotes stripped, a datetime suffix tolerated, an impossible date refused --
    the one parser behind orient's recency probe and any chronology reader."""
    m = re.match(r"(\d{4}-\d{2}-\d{2})", kb_unquote((meta or {}).get("date")))
    if not m:
        return None
    try:
        import datetime as _dt
        _dt.date.fromisoformat(m.group(1))
    except ValueError:
        return None
    return m.group(1)


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
    """The frontmatter that DECLARES the cited file, and the path it came from.

    A corpus artifact carries none of its own: `given/x.txt` is bytes, and what
    says how those bytes were obtained is the `x.txt.meta.md` sidecar beside it.
    Resolving the cited path alone returned `{}` for such a file -- which the
    caller cannot tell apart from "resolved, field absent" -- and that made
    DERIVED, RULING and IMPORTED impossible for every claim citing `given/`.

    Sidecar FIRST when one exists, the cited file otherwise. Not "non-.md ->
    sidecar": a verbatim `.md` source stored in `given/` is declared by its
    sidecar exactly like a `.txt` extraction, and reading its own frontmatter
    would read the SOURCE's, which says nothing about how it was extracted. A
    `corpus/notes/*.md` note has no sidecar and still resolves to its own.

    Returns `(meta, label)`. The label names the file actually read, so a
    finding can say where it looked instead of sending the reader to the wrong
    file -- the same defect this release fixes in the duplicate-id message.
    """
    base = sdlc_core.confine_under(root, rel)
    if base is None or base == root.resolve():
        # None: the path escapes the docs root, and the source loop said so.
        # Equal to the root: an empty or dot-only path cell (a source written
        # `#L1-2`, with no file before the locator). Forming a sidecar name
        # from that would step back OUT of the root through `base.parent` and
        # read `<docs-root>.meta.md` -- outside the tree this helper confines.
        return None, rel
    if not base.is_file():
        # The cited file is gone. Its sidecar may still be lying there, but a
        # claim on a missing artifact is already an error from the source loop,
        # and answering from an orphan sidecar would add a second finding about
        # a file that is not there.
        return None, rel
    side = base.parent / (base.name + ".meta.md")
    if side.is_file():
        return (sdlc_core.load_frontmatter(
            sdlc_core.read_text(side).splitlines()) or {}, rel + ".meta.md")
    return (sdlc_core.load_frontmatter(
        sdlc_core.read_text(base).splitlines()) or {}, rel)


def _kb_pointer_resolves(p):
    """A recorded pointer resolves when it names a FILE we can stat.

    `is_file()` and not `exists()`: `original_path` names a document, so a
    directory that happens to sit at that path is not the original. Any OSError
    is "does not resolve" and never a traceback -- the field points OUTSIDE the
    docs root by design, so the validator has to survive whatever lives there
    (an unreadable parent on a network vault, a name too long, a reparse point).
    """
    try:
        return p.is_file()
    except OSError:
        return False


def _kb_original_candidates(op, root):
    """Every place a recorded `original_path` could legitimately be, in order.

    `Path.is_absolute()` is NOT the test, and using it was a real defect: on
    Windows a rooted-but-driveless path -- `/vault/manuals/xyz.pdf`, the exact
    form this project's own templates print -- is not absolute, so it was
    joined under the docs root and silently rewritten onto the docs root's
    DRIVE. That produced a warning quoting a path nobody wrote, and could hide
    a genuinely dangling pointer behind a file that happened to exist there.
    Anything EITHER platform calls rooted is now taken as written; only a
    genuinely relative pointer is joined.

    A relative pointer is tried against the docs root's parent (the project
    root in the standard layout) and against the docs root itself, because
    `--root` and `migrate` both allow a docs root that does not sit directly
    under the project root.
    """
    raw = (op or "").strip()
    forms = [raw]
    if "\\" in raw:
        # A path authored on Windows and read anywhere. Tried as a SECOND form,
        # never instead of the first: a backslash is a legal character in a
        # POSIX filename, and rewriting it unconditionally invented a path.
        forms.append(raw.replace("\\", "/"))
    out, seen = [], set()
    for f in forms:
        cands = ([Path(f)] if (ntpath.isabs(f) or posixpath.isabs(f))
                 else [root.parent / f, root / f])
        for c in cands:
            if str(c) not in seen:
                seen.add(str(c))
                out.append(c)
    return out


def kb_check_claims(root):
    """All mechanical claim checks over topics/*.md. Returns (errors, warnings,
    notes) as message lists. Findings only — never per-node status lines."""
    errors, warnings, notes = [], [], []
    topics = root / "topics"
    if not topics.is_dir():
        return errors, warnings, notes
    all_ids = {}     # id -> "file:line"
    all_rows = {}    # id -> (row, rel)
    # Frontmatter is now resolved for every row, GIVEN included, so a ledger
    # citing one artifact from 80 rows would otherwise stat and decode that
    # artifact's sidecar 80 times. Keyed by the cited path, per run.
    fm_cache = {}

    def _declaring_frontmatter(rel):
        if rel not in fm_cache:
            fm_cache[rel] = _note_frontmatter(root, rel)
        return fm_cache[rel]
    # F-069: the same per-run memo for the source paths themselves -- each
    # distinct path is resolved and stat'ed once, and each cited extraction
    # read once (loc_cache, owned here, dropped when this call returns).
    src_cache = {}
    loc_cache = {}

    def _resolved(path_s):
        if path_s not in src_cache:
            t = sdlc_core.confine_under(root, path_s)
            src_cache[path_s] = (t, t is not None and t.is_file())
        return src_cache[path_s]
    per_file_rows = []
    marked = []      # (where, row, [ANALYSIS_ targets]) -- F-080
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
                target, is_file = _resolved(path_s)
                if target is None:
                    errors.append("%s: source %r escapes the docs root" % (where, src))
                    continue
                if not is_file:
                    errors.append("%s: source %r does not resolve — a claim whose "
                                  "origin cannot be reopened is model knowledge"
                                  % (where, src))
                    continue
                kb_check_locator(target, loc, where, errors, loc_cache)
            # --- provenance ---
            prov = row["prov"]
            # Resolved ONCE, for every provenance: the non-GIVEN classes read it
            # for their required field, and GIVEN reads it to notice that the
            # artifact declares a weaker chain than the row claims.
            meta, meta_where = (None, "")
            if "#" in first:
                meta, meta_where = _declaring_frontmatter(first.rsplit("#", 1)[0])
            # F-084: a declaration (a document this project SENT) can never pass
            # for evidence, nor evidence for a declaration -- checked on EVERY
            # source position, because corroboration appends sources to a row.
            declared_srcs = []
            for src in sources:
                if "#" not in src:
                    continue
                path_s = src.rsplit("#", 1)[0]
                if _resolved(path_s)[1]:
                    smeta, swhere = _declaring_frontmatter(path_s)
                    if ((smeta or {}).get("provenance") or "").strip().upper() == "DECLARED":
                        declared_srcs.append((path_s, smeta, swhere))
            if prov == "DECLARED":
                decl_paths = set(d[0] for d in declared_srcs)
                for src in sources:
                    path_s = src.rsplit("#", 1)[0] if "#" in src else src
                    if not _resolved(path_s)[1]:
                        continue  # unresolvable source already reported
                    if not path_s.startswith("corpus/given/") or path_s not in decl_paths:
                        errors.append("%s: DECLARED row cites %s, which is not a "
                                      "corpus/given/ artifact whose sidecar says "
                                      "'provenance: DECLARED' -- a declaration rests "
                                      "only on the document that was sent" % (where, path_s))
                for path_s, smeta, swhere in declared_srcs:
                    if not (smeta.get("recipient") or "").strip():
                        errors.append("%s: DECLARED source (%s) carries no "
                                      "'recipient:' -- a declaration names to whom it "
                                      "was made" % (where, swhere))
            elif declared_srcs:
                errors.append("%s: prov %s, but %s declares 'provenance: DECLARED' -- "
                              "a document this project sent is a declaration, not "
                              "evidence: file the row as DECLARED on that artifact "
                              "alone (a declaration never corroborates another row)"
                              % (where, prov, declared_srcs[0][2]))
            if prov not in PROVENANCES:
                errors.append("%s: prov %r not in %s" % (where, prov, "/".join(PROVENANCES)))
            elif prov in ("DERIVED", "RULING", "ELICITED", "IMPORTED"):
                if meta is None:
                    pass  # unresolvable source already reported
                elif prov == "DERIVED" and not meta.get("derived_from"):
                    errors.append("%s: DERIVED claim's source (%s) carries no "
                                  "'derived_from:' — model knowledge disguised as "
                                  "a source" % (where, meta_where))
                elif prov == "RULING" and meta.get("imported_from"):
                    # F-083: relabelling an imported row RULING would make another
                    # owner's note carry a decision here. Ratifying is deciding:
                    # a note of your own, with your own basis.
                    errors.append("%s: RULING source (%s) names a foreign origin "
                                  "(imported_from: %s) — another project's note "
                                  "cannot carry your ruling. Write your own note "
                                  "with your own 'basis:' and put the RULING on it "
                                  "(portability.md §4)"
                                  % (where, meta_where, meta.get("imported_from")))
                elif prov == "RULING" and not meta.get("basis"):
                    errors.append("%s: RULING source (%s) carries no 'basis:' — a "
                                  "preference is not a fact; no basis, no ruling"
                                  % (where, meta_where))
                elif prov == "IMPORTED" and not meta.get("imported_from"):
                    # F-030: IMPORTED exists so a foreign decision cannot pass for
                    # a local one. Without the origin the class says nothing and
                    # the row is a RULING with the label filed off.
                    errors.append("%s: IMPORTED source (%s) carries no "
                                  "'imported_from:' — the class exists to name "
                                  "whose decision this was; unnamed, it is a "
                                  "RULING in disguise" % (where, meta_where))
            elif prov == "GIVEN":
                # F-035: a row resting on an OCR, a transcription or a
                # translation is not the same evidence as one resting on a
                # deterministic text layer. The sidecar could say so only in
                # prose, and prose is not a check -- which is how three rows
                # whose evidence was a reading of an image passed as GIVEN.
                declared = ((meta or {}).get("provenance") or "").strip()
                if declared and declared.upper() not in ("GIVEN", "DECLARED"):
                    warnings.append(
                        "%s: prov GIVEN, but %s declares 'provenance: %s' — the "
                        "row reads as first-hand evidence and its artifact does "
                        "not. File the row at the provenance the chain actually "
                        "has, or correct the sidecar" % (where, meta_where, declared))
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
            marks = []
            for part in kb_about_parts(row["about"]):
                mark = KB_NOT_HONORED_RE.match(part)
                rel_m = KB_ABOUT_RE.match(part)
                if mark:
                    marks.append(mark.group(1))
                elif part.split(" -> ")[0].strip() == KB_NOT_HONORED:
                    errors.append("%s: about %r: '%s' needs an ANALYSIS_<name> "
                                  "target (Hybrid: SHADOW_<doc_key>, unversioned) -- the "
                                  "analysis or design that records the deferred "
                                  "fix" % (where, part, KB_NOT_HONORED))
                elif not rel_m:
                    errors.append("%s: about must be '<predicate> -> <slug>' "
                                  "parts joined by ';', or '-': %r" % (where, part))
            if marks:
                marked.append((where, row, marks))
            # --- atomicity hint (F-047): a row atomic as provenance can be
            # plural as meaning. Text cannot PROVE plurality, so this is a
            # note — never a warning or an error, never the exit code.
            hints = [h for h in KB_BUNDLE_HINTS if h in row["claim"]]
            if hints:
                notes.append("%s: claim text of %s reads like more than one "
                             "assertion (matched %s) — one row asserts one "
                             "thing; if it is a bundle, split it "
                             "(distillation.md section 3, reconciliation.md "
                             "section 'Splitting a bundled row'). Heuristic "
                             "only: a genuinely "
                             "single assertion needs no change"
                             % (where, row["id"] or "(id pending)",
                                ", ".join(repr(h) for h in hints)))
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
                    # F-035: one message served two different defects. Same id
                    # with the SAME text is a copied row. Same id with DIFFERENT
                    # text is a collision: kb_claim_id hashes path#locator#qty
                    # and excludes the text on purpose, so two distinct
                    # assertions about one span cannot be told apart. The source
                    # and qty do NOT discriminate -- the id already implies them.
                    prev_row = all_rows[row["id"]][0]

                    def _cell(r, k):
                        return (r[k] or "").strip()

                    def _first_src(r):
                        return (r["source"] or "").split(";")[0].strip()

                    same_text = _cell(prev_row, "claim") == _cell(row, "claim")
                    same_span = (_first_src(prev_row) == _first_src(row)
                                 and _cell(prev_row, "qty") == _cell(row, "qty"))
                    if same_text:
                        errors.append("%s: duplicate id %s (also at %s) — uniqueness "
                                      "is global across topics/" % (where, row["id"],
                                                                    all_ids[row["id"]]))
                    elif same_span:
                        # F-047: recommending a merge here was a trap — merging
                        # distinct assertions manufactures a bundled row, trading
                        # this mechanical error for a semantic one no check sees.
                        errors.append(
                            "%s: id %s collides with the row at %s — two "
                            "DIFFERENT rows cite the same span with the same "
                            "qty, and the id function cannot separate them (it "
                            "hashes path#locator#qty and excludes the text on "
                            "purpose). Narrow each locator to the sub-span that "
                            "carries its own assertion — narrow spans make "
                            "atomic rows id-distinct (on a stored .txt, "
                            "p=<page>@<a>-<b> reaches below a line). Merge ONLY "
                            "if the two rows state the same single assertion; "
                            "merging distinct assertions trades this mechanical "
                            "error for a semantic one no check can see — do not "
                            "edit the qty to break the tie"
                            % (where, row["id"], all_ids[row["id"]]))
                    else:
                        # Same id, different text AND different span: the id
                        # cannot have been computed from both rows, so it was
                        # hand-typed or left stale after a source was repointed.
                        # Saying "they cite the same span" here would name a
                        # cause that is provably not this one.
                        errors.append(
                            "%s: id %s is also on the row at %s, which cites a "
                            "different span — the id was not computed from this "
                            "row (hand-typed, or left stale after its source "
                            "moved). Run 'sdlc_check.py claim-id --fill %s'"
                            % (where, row["id"], all_ids[row["id"]], rel))
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
            kind, targets = _kb_states(state)
            if not kind:
                errors.append("%s: state must be OK, 'CONTESTED <id>[,..]', "
                              "'SUPERSEDED <id>[,..]' or 'DIVERGES <id>[,..]': %r"
                              % (where, state))
                continue
            row_decl = _kb_is_declared(row)
            if kind == "DIVERGES" and not row_decl:
                errors.append("%s: DIVERGES on a %s row -- only a DECLARED row "
                              "diverges; two sources that disagree are CONTESTED"
                              % (where, row["prov"].strip() or "?"))
                continue
            for t in targets:
                other = all_rows.get(t)
                if other is None:
                    errors.append("%s: %s points at id %s which resolves to no row "
                                  "— deleting one side of a disagreement breaks "
                                  "the check, it does not clean up" % (where, kind, t))
                    continue
                orow, _ = other
                if kind == "DIVERGES":
                    if _kb_is_declared(orow):
                        errors.append("%s: DIVERGES points at %s, a DECLARED row -- a "
                                      "declaration diverges from the ledger, never from "
                                      "another declaration (two sends that disagree "
                                      "are CONTESTED)" % (where, t))
                    elif orow["state"].startswith("SUPERSEDED"):
                        errors.append("%s: DIVERGES points at SUPERSEDED row %s -- "
                                      "re-judge the declaration against its successor"
                                      " (OK if it now agrees)" % (where, t))
                    continue
                if kind in ("SUPERSEDED", "CONTESTED") and row_decl != _kb_is_declared(orow):
                    errors.append("%s: %s %s across a declaration -- a declaration is "
                                  "superseded only by a later declaration and never "
                                  "settles or contests a fact; a declaration that "
                                  "contradicts the ledger is DIVERGES"
                                  % (where, kind, t))
                    continue
                if kind == "SUPERSEDED" and orow["prov"] == "IMPORTED":
                    # F-030, owner ruling 2026-08-03: knowledge crosses a project
                    # boundary, authority does not. An IMPORTED row carries another
                    # owner's decision; letting it supersede a local row would make
                    # that decision binding here without anyone here granting it.
                    # Ratify first (F-083): a note of your own with your own basis,
                    # a RULING row on it, and every row contested with the imported
                    # one SUPERSEDED by that row.
                    errors.append("%s: SUPERSEDED by %s, which is IMPORTED — a "
                                  "foreign decision cannot settle a local row. "
                                  "Ratify it: your own note with your own "
                                  "'basis:', a RULING row on it, and every row "
                                  "CONTESTED with %s SUPERSEDED by that row"
                                  % (where, t, t))
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
    kb_check_marks(root, marked, per_file_rows, errors)
    return errors, warnings, notes


def kb_check_marks(root, marked, per_file_rows, errors):
    """F-080: each not-yet-honored mark names an ANALYSIS that exists in this
    project and cites the claim id -- or the id of a row this claim succeeds,
    since supersession copies the mark and edits no analysis. F-081: a Hybrid
    mark names SHADOW_<doc_key>, and the newest shadow of that key is read."""
    if not marked:
        return
    preds = {}       # successor id -> ids it supersedes
    for _, rows in per_file_rows:
        for row in rows:
            m = re.match(r"^SUPERSEDED ([0-9a-f, ]+)$", row["state"])
            if row["id"] and m:
                for t in [x.strip() for x in m.group(1).split(",") if x.strip()]:
                    preds.setdefault(t, set()).add(row["id"])
    texts = {}
    for where, row, targets in marked:
        ids, todo = set(), [row["id"]] if row["id"] else []
        while todo:
            cid = todo.pop()
            if cid not in ids:
                ids.add(cid)
                todo.extend(preds.get(cid, ()))
        for target in targets:
            if target not in texts:
                texts[target] = _kb_mark_target(root, target)
            rel, text, stray = texts[target]
            if text is None and target.startswith("SHADOW_"):
                errors.append("%s: %s -> %s: no %s in this project%s. Export the "
                              "shadow from the accepted devPNT version, or remove "
                              "the marker if it did not come from this project -- "
                              "it describes its origin's code"
                              % (where, KB_NOT_HONORED, target, rel,
                                 " (%s is not named _vX.Y)" % stray if stray else ""))
            elif text is None:
                errors.append("%s: %s -> %s: no %s in this project. Remove the "
                              "marker if it did not come from this project -- it "
                              "describes its origin's code" % (where, KB_NOT_HONORED,
                                                              target, rel))
            elif ids and not any(re.search(r"(?<![0-9a-f])%s(?![0-9a-f])" % cid, text)
                                 for cid in ids):
                errors.append("%s: %s does not cite claim %s -- the analysis or "
                              "design that records a deferred fix cites the id it "
                              "defers"
                              % (where, rel, row["id"]))


def _kb_mark_target(root, target):
    """(rel, text or None, stray name or None) for a marker target. ANALYSIS_x
    is solutions/x.md; SHADOW_k is the newest solutions/SHADOW_k_vX.Y.md, and
    when none exists a file of the same exact key with another suffix is
    reported as the stray that was not read (F-081)."""
    if not target.startswith("SHADOW_"):
        rel = "solutions/%s.md" % target
        path = sdlc_core.confine_under(root, rel)
        return rel, (sdlc_core.read_text(path)
                     if path is not None and path.is_file() else None), None
    key = target[len("SHADOW_"):]
    sol = sdlc_core.confine_under(root, "solutions")
    path = sdlc_core.newest_shadow(sol, key) if sol is not None else None
    if path is not None and sdlc_core.confine_under(root, "solutions/" + path.name):
        return "solutions/" + path.name, sdlc_core.read_text(path), None
    stray = sdlc_core.stray_shadow(sol, key) if sol is not None else None
    return "solutions/SHADOW_%s_v<X.Y>.md" % key, None, stray


def kb_drop_marks(text):
    """(text, dropped): the topic text with every not-yet-honored part removed
    from claim rows' `about` cells. Every other byte is kept -- other cells keep
    their spacing, other lines are untouched (F-080: a bundle describes no code)."""
    rows, _ = kb_parse_claims(text)
    lines = text.split("\n")
    col = 1 + CLAIM_COLUMNS.index("about")
    dropped = False
    for row in rows:
        parts = kb_about_parts(row["about"])
        keep = [p for p in parts if not KB_NOT_HONORED_RE.match(p)]
        if len(keep) == len(parts):
            continue
        # The parser strips the pipes at both ends, so a row with no trailing
        # pipe is legal: counted from the left, the about cell sits at `col`
        # either way.
        segs = lines[row["_line"] - 1].split("|")
        if len(segs) not in (len(CLAIM_COLUMNS) + 1, len(CLAIM_COLUMNS) + 2):
            continue
        segs[col] = " %s " % ("; ".join(keep) or "-")
        lines[row["_line"] - 1] = "|".join(segs)
        dropped = True
    return "\n".join(lines), dropped


def _kb_is_declared(row):
    return (row.get("prov") or "").strip().upper() == "DECLARED"


def kb_has_declarations(selected):
    """Whether any selected topic holds a DECLARED row -- a yes/no for export's
    line, never a count (the same rule as F-080's dropped-marker line)."""
    return any(_kb_is_declared(r) for _p, _t, rows in selected.values() for r in rows)


def kb_drop_declarations(text):
    """The topic text without its DECLARED rows (F-084: a declaration is this
    project's commitment to its recipient and stays here). Every other line is
    kept byte for byte. Closed by construction: check refuses any pointer from
    a non-DECLARED row at a DECLARED one, so nothing left behind points at a
    dropped row."""
    rows, _ = kb_parse_claims(text)
    gone = set(r["_line"] for r in rows if _kb_is_declared(r))
    if not gone:
        return text
    return "\n".join(ln for i, ln in enumerate(text.split("\n"), 1) if i not in gone)


def kb_check_locator(target, loc, where, errors, cache=None):
    """A locator must address an existing span of the stored bytes.

    `cache` is an optional dict the CALLER owns for one run (F-069): keyed by
    the path actually read, it holds only what the checks compare against --
    page lengths, a line count, or False for a missing extraction -- never the
    text. Findings are still appended per call, so per row. Without it, every
    call reads the file, as before."""
    m = LOC_PAGE_RE.match(loc)
    if m:
        page, a, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if a >= b:
            errors.append("%s: locator %r has an empty span" % (where, loc))
            return
        # offsets address the stored extraction (<stem>.txt beside the original)
        ext = target if target.suffix == ".txt" else target.with_suffix(".txt")
        key = ("p", ext)
        if cache is None or key not in cache:
            lengths = ([len(pg) for pg in sdlc_core.read_text(ext).split("\f")]
                       if ext.is_file() else False)
            if cache is not None:
                cache[key] = lengths
        else:
            lengths = cache[key]
        if lengths is False:
            errors.append("%s: no stored extraction %s for locator %r — offsets "
                          "must address kept bytes" % (where, ext.name, loc))
            return
        if page < 1 or page > len(lengths):
            errors.append("%s: locator %r addresses page %d of %d" %
                          (where, loc, page, len(lengths)))
        elif b > lengths[page - 1]:
            errors.append("%s: locator %r spans past the end of page %d "
                          "(%d chars)" % (where, loc, page, lengths[page - 1]))
        return
    m = LOC_LINE_RE.match(loc)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if a > b or a < 1:
            errors.append("%s: locator %r has an invalid line range" % (where, loc))
            return
        key = ("L", target)
        if cache is None or key not in cache:
            n = sdlc_core.read_text(target).count("\n") + 1
            if cache is not None:
                cache[key] = n
        else:
            n = cache[key]
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


def kb_parse_extracted_through(value):
    """('complete', None) | ('p', n) | ('L', n), or None when the value is not a
    coverage statement.

    Fail-closed on purpose: a field whose whole job is to be checkable must be
    checkable, so an unreadable value is an error rather than a silent pass."""
    m = EXTRACTED_THROUGH_RE.match((value or "").strip())
    if not m:
        return None
    if m.group(1):
        return "p", int(m.group(1))
    if m.group(2):
        return "L", int(m.group(2))
    return "complete", None


def kb_extraction_extent(artifact, kind):
    """How far the stored bytes go, in the unit `kind` — or None when nothing
    measurable is stored.

    Opens exactly the file `kb_check_locator` opens for that locator form: pages
    live in the stored extraction beside the original, lines in the artifact
    itself. Coverage is therefore measured against the same bytes a locator
    addresses, and a binary is never read as text (a .pdf with no extraction
    beside it is simply unmeasurable — the p= branch needs the .txt)."""
    if kind == "p":
        ext = artifact if artifact.suffix == ".txt" else artifact.with_suffix(".txt")
        if not ext.is_file():
            return None
        return len(sdlc_core.read_text(ext).split("\f"))
    if kind == "L":
        if not artifact.is_file():
            return None
        return sdlc_core.read_text(artifact).count("\n") + 1
    return None


def kb_coverage_cell(artifact, through):
    """The coverage fact for one corpus row.

    EVERY artifact gets one, including the finished ones: printing only the
    incomplete ones would turn this index into 'the set that is not current',
    which the Vision refuses (r9). It is a fact on an existing row, never a
    filter and never a sort key."""
    if not (through or "").strip():
        return "extraction not recorded"
    parsed = kb_parse_extracted_through(through)
    if parsed is None:
        return "extracted through %s (unreadable)" % through.strip()
    kind, n = parsed
    if kind == "complete":
        return "extracted through complete"
    total = kb_extraction_extent(artifact, kind)
    stated = ("p=%d" % n) if kind == "p" else ("L%d" % n)
    return "extracted through %s of %d" % (stated, total) if total \
        else "extracted through %s" % stated


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
            if kb_is_tombstone(meta):
                lines.append("- `%s` — %s — withdrawn" % (
                    orig, (meta.get("date") or "undated")))
                continue
            sup = kb_unquote(meta.get("supersedes"))
            lines.append("- `%s` — %s%s — %s" % (
                orig, (meta.get("date") or "undated"),
                (" — supersedes `%s`" % sup) if sup else "",
                kb_coverage_cell(given / orig, meta.get("extracted_through"))))
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


def kb_cited_extents(root):
    """Per artifact file name, what the claim rows say about it: the highest page
    and the highest line any locator addresses (with the row that says so), and
    every row citing it. One walk of topics/, shared by the supersession and the
    coverage checks — two walks of the same tree for two questions is how the
    answers start disagreeing."""
    cited = {}
    topics = root / "topics"
    if not topics.is_dir():
        return cited
    for p in sorted(topics.glob("*.md")):
        for row in kb_parse_claims(sdlc_core.read_text(p))[0]:
            where = "topics/%s:%d" % (p.name, row["_line"])
            for src in row["source"].split(";"):
                src = src.strip()
                if not src:
                    continue
                path_s, loc = src.rsplit("#", 1) if "#" in src else (src, "")
                parts = Path(path_s.strip().replace("\\", "/")).parts
                if parts[-3:-1] != ("corpus", "given"):
                    # Keyed by file name, so a note sharing a name with an
                    # artifact would otherwise be attributed to it and inflate
                    # its extents. Both consumers here ask only about given/.
                    continue
                name = parts[-1]
                e = cited.setdefault(name, {"p": 0, "p_where": None,
                                            "L": 0, "L_where": None, "rows": []})
                e["rows"].append(where)
                m = LOC_PAGE_RE.match(loc.strip())
                if m and int(m.group(1)) > e["p"]:
                    e["p"], e["p_where"] = int(m.group(1)), where
                    continue
                m = LOC_LINE_RE.match(loc.strip())
                if m and int(m.group(2)) > e["L"]:
                    e["L"], e["L_where"] = int(m.group(2)), where
    return cited


def _kb_cited_for(cited, artifact_name):
    """Claims may cite the original or its stored extraction — both address the
    same bytes, so both count as citing this artifact."""
    names = [artifact_name]
    if not artifact_name.endswith(".txt"):
        names.append(Path(artifact_name).with_suffix(".txt").name)
    found = [cited[n] for n in names if n in cited]
    if not found:
        return None
    merged = dict(found[0])
    for e in found[1:]:
        for kind in ("p", "L"):
            if e[kind] > merged[kind]:
                merged[kind], merged[kind + "_where"] = e[kind], e[kind + "_where"]
        merged["rows"] = merged["rows"] + e["rows"]
    return merged


def kb_check_coverage(rel, artifact, through, facts, errors, warnings):
    """`extracted_through:` against the rows and against the stored bytes (F-031).

    Four outcomes, and the boundary between them is the whole point: claims with
    no field errors (an unfalsifiable 'done'); a field that contradicts the bytes
    or the rows errors; a field short of the end warns, because partial work is
    legal mid-ingestion; an artifact nobody extracted from stays silent.

    The limit, stated where the code is: nothing here proves a page was READ. A
    field advanced without extracting is invisible to any checker, since a page
    that asserts nothing legitimately yields no rows — that direction belongs to
    the ingestion review. What this buys is that the shortcut must be written
    down to pass."""
    if not through:
        if facts:
            errors.append("%s: claims cite this artifact and the sidecar has no "
                          "'extracted_through:' — how far a source was read is an "
                          "assertion like any other, and unstated 'I am finished' "
                          "cannot be falsified. Record it: 'p=<n>', 'L<n>', or "
                          "'complete' (first row at %s)" % (rel, facts["rows"][0]))
        return
    parsed = kb_parse_extracted_through(through)
    if parsed is None:
        errors.append("%s: extracted_through: %r is not a coverage statement — use "
                      "'complete', 'p=<n>' or 'L<n>'" % (rel, through))
        return
    kind, n = parsed
    if kind == "complete":
        return
    other = "L" if kind == "p" else "p"
    unit = "pages" if kind == "p" else "lines"
    total = kb_extraction_extent(artifact, kind)
    if facts and facts[other] and not facts[kind]:
        errors.append("%s: coverage is stated in %s while every claim addresses %s "
                      "(%s) — stated in the wrong unit it compares with nothing, "
                      "and nothing here is checkable"
                      % (rel, unit, "lines" if kind == "p" else "pages",
                         facts[other + "_where"]))
        return
    if total and n > total:
        errors.append("%s: extracted_through: %s, past the end of the stored bytes "
                      "(%d %s) — coverage cannot exceed what was stored"
                      % (rel, through, total, unit))
    elif total and n < total:
        warnings.append("%s: extracted through %s of %d %s — ingestion is incomplete "
                        "(legal mid-work: a source is finished when every page has "
                        "been read, not when enough rows exist)"
                        % (rel, through, total, unit))
    if facts and facts[kind] > n:
        reached = ("p=%d" % facts[kind]) if kind == "p" else ("L%d" % facts[kind])
        errors.append("%s: a claim addresses %s, past the declared coverage %s (%s) — "
                      "the sidecar and the rows contradict each other; one of the two "
                      "is wrong" % (rel, reached, through, facts[kind + "_where"]))


def kb_corpus_check(root):
    """Corpus integrity: digests, supersession, coverage, laundered notes.
    Findings only."""
    errors, warnings = [], []
    corpus = root / "corpus"
    if not corpus.is_dir():
        return errors, warnings
    cited = kb_cited_extents(root)
    superseded = set()
    given = corpus / "given"
    if given.is_dir():
        for meta_p in sorted(given.glob("*.meta.md")):
            meta = sdlc_core.load_frontmatter(sdlc_core.read_text(meta_p).splitlines()) or {}
            orig = given / meta_p.name[:-len(".meta.md")]
            rel = "corpus/given/" + orig.name
            if kb_is_tombstone(meta):
                # F-077: a withdrawn artifact keeps its record, never its bytes
                # nor a digest of them -- a digest of the secret-bearing bytes
                # beside a redacted successor tests password guesses offline.
                kept = [k for k in ("sha256", "original_sha256")
                        if (meta.get(k) or "").strip()]
                if kept:
                    errors.append("%s: withdrawn, yet its sidecar keeps %s -- "
                                  "a tombstone keeps no digest of the withdrawn "
                                  "bytes (distillation.md par.1)"
                                  % (rel, ", ".join(k + ":" for k in kept)))
                if orig.is_file():
                    errors.append("%s: withdrawn, yet its bytes are still here -- "
                                  "delete them" % rel)
                continue
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
            # F-035: `original_sha256` is not verified because we do not hold
            # the bytes -- a limit stated out loud in distillation.md. That
            # reason does not extend to the PATH, which costs one exists(). A
            # corpus whose premise is "every provenance is a real file" cannot
            # let 16 sidecars go dangling behind a green run.
            op = kb_unquote(meta.get("original_path"))
            if op:
                cands = _kb_original_candidates(op, root)
                tried = [str(c) for c in cands]
                resolved = any(_kb_pointer_resolves(c) for c in cands)
                if not resolved:
                    warnings.append(
                        "%s: original_path %r does not resolve (tried %s) — the "
                        "extraction is intact, the pointer to the original is "
                        "not. A warning and not an error: a bundle carries "
                        "artifacts and sidecars, never the originals, so after "
                        "an import this dangles legitimately%s"
                        % (rel, _kb_mask_userinfo(op),
                           _kb_mask_userinfo(", ".join(tried)),
                           " -- a non-local identifier belongs in original_ref:, "
                           "which is recorded and never resolved"
                           if re.match(r"^[A-Za-z][A-Za-z0-9+.\-]+://", op) else ""))
            sup = kb_unquote(meta.get("supersedes"))
            if sup:
                superseded.add(sup)
                sup_side = given / (sup + ".meta.md")
                tomb = sup_side.is_file() and kb_is_tombstone(
                    sdlc_core.load_frontmatter(sdlc_core.read_text(sup_side).splitlines()))
                if not (given / sup).is_file() and not tomb:
                    warnings.append("%s: supersedes %r which is not in given/"
                                    % (rel, sup))
            kb_check_coverage(rel, orig,
                              (meta.get("extracted_through") or "").strip(),
                              _kb_cited_for(cited, orig.name), errors, warnings)
        # F-077: a file nobody declared -- or bytes a withdrawal left behind. A
        # stored extraction `<stem>.txt` beside a declared `<stem>.<ext>` is the
        # declared artifact's own (distillation.md par.1), not a stray.
        declared_stems = set(Path(m.name[:-len(".meta.md")]).stem
                             for m in given.glob("*.meta.md"))
        for p in sorted(given.iterdir()):
            if (p.is_file() and not p.name.endswith(".meta.md")
                    and not (given / (p.name + ".meta.md")).is_file()
                    and not (p.suffix == ".txt" and p.stem in declared_stems)):
                warnings.append("corpus/given/%s: no sidecar -- an artifact nobody "
                                "declared, or bytes a withdrawal left behind" % p.name)
        warnings.extend(_kb_same_text_warnings(root))
    notes = corpus / "notes"
    if notes.is_dir():
        for p in sorted(notes.glob("*.md")):
            meta = sdlc_core.load_frontmatter(sdlc_core.read_text(p).splitlines()) or {}
            if not (meta.get("derived_from") or meta.get("origin")
                    or meta.get("basis")):
                errors.append("corpus/notes/%s: neither 'derived_from:' nor "
                              "'origin:' nor 'basis:' — model knowledge disguised "
                              "as a source" % p.name)
    # claims resting on superseded originals (UC4), from the same single walk
    for name in sorted(superseded):
        for where in (cited.get(name) or {}).get("rows", []):
            warnings.append("%s: claim rests on %s, which a newer version "
                            "supersedes — re-verify or re-place" % (where, name))
    return errors, warnings


# ------------------------------------------------- credentials (F-077)
# A credential stored in given/ cannot be fixed in place: the digest check
# refuses the edit and git keeps the bytes. These shapes are written from the
# formats' own syntax (key=value lines, PEM headers, URL userinfo, bearer
# headers); no vendor key format is matched (distillation.md par.1 lists the
# declared false positives and false negatives). Findings carry line numbers
# and kinds, NEVER the value: the validator's output lands in logs and CI.

KB_CRED_PAIRS = {("api", "key"): "api-key", ("access", "key"): "access-key",
                 ("private", "key"): "private-key",
                 ("client", "secret"): "client-secret", ("secret", "key"): "secret"}
KB_CRED_LAST = {"password": "password", "passwd": "password",
                "passphrase": "password", "secret": "secret", "token": "token",
                "credential": "credentials", "credentials": "credentials",
                "apikey": "api-key", "accesskey": "access-key"}
KB_CRED_ASSIGN_RE = re.compile(
    r"""^\s*(?:export\s+)?(["']?)([A-Za-z0-9_.\-]+)\1\s*[=:]\s*(.*)$""")
KB_CRED_SEGMENT_RE = re.compile(r"[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])")
KB_CRED_PEM_RE = re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")
KB_CRED_URL_RE = re.compile(r"[A-Za-z][A-Za-z0-9+.\-]*://[^/\s:@]*:([^@\s/]+)@")
KB_CRED_QUERY_RE = re.compile(r"[?&;](?:password|pwd|passwd)=([^&\s;#]+)", re.I)
KB_CRED_BEARER_RE = re.compile(r"\bBearer\s+[A-Za-z0-9\-._~+/]{16,}")
KB_CRED_PLACEHOLDER_RE = re.compile(
    r"<.*>|\$\{.*\}|\{\{.*\}\}|%\(.*\)s|ENC\(.*\)|[*xX]+|[|>][-+]?\d*")
KB_CRED_LINE_MAX = 4096
KB_REVIEWED_RE = re.compile(r"^reviewed\s*[-—–:]\s*\S")


def _kb_cred_real(value):
    """True when a value looks like an actual secret, not a placeholder."""
    v = re.split(r"\s+(?:#|//)", value.strip(), maxsplit=1)[0].strip()
    if v.endswith(","):
        v = v[:-1].rstrip()
    if len(v) >= 2 and v[0] in "\"'" and v[-1] == v[0]:
        v = v[1:-1]
    if not v or re.search(r"\s", v):
        return False
    if v.lower() in ("true", "false", "null", "none", "yes", "no"):
        return False
    if v.startswith("[REDACTED") or KB_CRED_PLACEHOLDER_RE.fullmatch(v):
        return False
    return True


def _kb_cred_key_kind(key):
    segs = [s.lower() for part in re.split(r"[_.\-]", key)
            for s in KB_CRED_SEGMENT_RE.findall(part)]
    if len(segs) >= 2 and tuple(segs[-2:]) in KB_CRED_PAIRS:
        return KB_CRED_PAIRS[tuple(segs[-2:])]
    return KB_CRED_LAST.get(segs[-1]) if segs else None


def kb_credential_line_kind(line):
    """The credential kind one line carries, or None. Never returns the value."""
    line = line[:KB_CRED_LINE_MAX]
    if KB_CRED_PEM_RE.search(line):
        return "private-key"
    m = KB_CRED_ASSIGN_RE.match(line)
    if m:
        kind = _kb_cred_key_kind(m.group(2))
        if kind and _kb_cred_real(m.group(3)):
            return kind
    m = KB_CRED_URL_RE.search(line)
    if m and _kb_cred_real(m.group(1)):
        return "connection-string"
    m = KB_CRED_QUERY_RE.search(line)
    if m and _kb_cred_real(m.group(1)):
        return "connection-string"
    if KB_CRED_BEARER_RE.search(line):
        return "bearer-token"
    return None


def kb_credential_findings(path):
    """[(line_no, kind)] for one file; [] for a binary or unreadable one.

    A NUL in the first 8 KB means binary, unless the file opens with a UTF-16
    byte-order mark (then it is decoded whole). Text is streamed line by line,
    each inspected on its first KB_CRED_LINE_MAX characters."""
    out = []
    try:
        with open(path, "rb") as f:
            head = f.read(8192)
        if head[:2] in (b"\xff\xfe", b"\xfe\xff"):
            lines = Path(path).read_bytes().decode("utf-16", errors="replace").splitlines()
            for n, line in enumerate(lines, 1):
                kind = kb_credential_line_kind(line)
                if kind:
                    out.append((n, kind))
            return out
        if b"\x00" in head:
            return []
        with open(path, encoding="utf-8-sig", errors="replace") as f:
            for n, line in enumerate(f, 1):
                kind = kb_credential_line_kind(line.rstrip("\r\n"))
                if kind:
                    out.append((n, kind))
    except OSError:
        return []
    return out


def _kb_mask_userinfo(text):
    """A password inside a URL never reaches the validator's output -- also once
    a candidate path has turned its `//` into `\\` (Windows join)."""
    return re.sub(r"([/\\][^/\\\s:@]*:)\S*@", r"\1***@", text)


def _kb_reviewed(meta):
    return bool(KB_REVIEWED_RE.match(kb_unquote((meta or {}).get("credential_scan"))))


def _kb_cred_message(rel, found, fix):
    nums = [str(n) for n, _ in found[:10]] + (["..."] if len(found) > 10 else [])
    kinds = sorted(set(k for _, k in found))
    return "%s: %s %s look like a credential (%s) -- %s" % (
        rel, "line" if len(found) == 1 else "lines", ", ".join(nums),
        ", ".join(kinds), fix)


def kb_is_tombstone(meta):
    return bool(kb_unquote((meta or {}).get("withdrawn")))


def kb_credential_errors(root, docs):
    """FS2 errors over given/ artifacts and document-guide snapshots, escapes
    applied. One carrier per command calls this (check, corpus); validate never."""
    errors = []
    given = docs / "corpus" / "given"
    if given.is_dir():
        # A stored extraction `<stem>.txt` has no sidecar of its own: it is the
        # declared `<stem>.<ext>`'s (distillation.md par.1), so its escape lives there.
        by_stem = {}
        for m in sorted(given.glob("*.meta.md")):
            by_stem.setdefault(Path(m.name[:-len(".meta.md")]).stem, m)
        for p in sorted(given.iterdir()):
            if not p.is_file() or p.name.endswith(".meta.md"):
                continue
            side = given / (p.name + ".meta.md")
            if not side.is_file() and p.suffix == ".txt" and p.stem in by_stem:
                side = by_stem[p.stem]
            meta = (sdlc_core.load_frontmatter(sdlc_core.read_text(side).splitlines())
                    or {}) if side.is_file() else {}
            if _kb_reviewed(meta):
                continue
            found = kb_credential_findings(p)
            if found:
                errors.append(_kb_cred_message(
                    "corpus/given/" + p.name, found,
                    "given/ is never edited: redact into a successor and withdraw "
                    "this one (distillation.md par.1), or declare "
                    "`credential_scan: reviewed -- <reason>` in its sidecar"))
    for rel, _p, meta, _t in sdlc_core.list_guides(root):
        if (meta.get("source_kind") or "document").strip() != "document":
            continue
        df = (meta.get("distilled_from") or "").strip()
        src = sdlc_core.confine_under(root, df) if df else None
        if src is None or not src.is_file() or _kb_reviewed(meta):
            continue
        try:
            src.resolve().relative_to(given.resolve())
            continue  # scanned above, once
        except (OSError, ValueError):
            pass
        found = kb_credential_findings(src)
        if found:
            errors.append(_kb_cred_message(
                df, found,
                "redact into a new snapshot (its name changes) and update %s's "
                "distilled_from, source_hash and markers, or declare "
                "`credential_scan: reviewed -- <reason>` in the guide" % rel))
    return errors


def _kb_print_credentials(root, docs):
    errs = kb_credential_errors(root, docs)
    for e in errs:
        print("[ERROR] %s" % e)
    return 1 if errs else 0


def _kb_same_text_warnings(docs):
    """FS6: a .sources/ file and a given/ artifact holding the same text after
    line-ending normalization. Snapshots are hashed once; a given/ artifact is
    hashed only when its size is within a factor of two of some snapshot's (CRLF
    at most doubles a text), so a large extraction corpus is not read for this."""
    src = docs / "reference" / ".sources"
    given = docs / "corpus" / "given"
    if not (src.is_dir() and given.is_dir()):
        return []
    snaps = {}
    sizes = []
    for p in sorted(src.rglob("*")):
        if p.is_file():
            try:
                snaps.setdefault(sdlc_core.sha256_file(p), []).append(p)
                sizes.append(p.stat().st_size)
            except OSError:
                continue
    if not snaps:
        return []
    lo, hi = min(sizes) // 2, max(sizes) * 2
    out = []
    for g in sorted(given.iterdir()):
        if not g.is_file() or g.name.endswith(".meta.md"):
            continue
        try:
            if not lo <= g.stat().st_size <= hi:
                continue
            h = sdlc_core.sha256_file(g)
        except OSError:
            continue
        for s in snaps.get(h, []):
            out.append("reference/.sources/%s and corpus/given/%s hold the same text "
                       "-- one home per source text: re-point the guide to "
                       "corpus/given/ (portability.md par.6, kb-agentic)"
                       % (s.relative_to(src).as_posix(), g.name))
    return out


def kb_sha256_bytes(path):
    """RAW-byte digest for binaries. The spine's sha256_file normalizes CRLF->LF
    (right for text snapshots, wrong for binaries, where a hostile 0D0A/0A pair
    would collide)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# -------------------------------------------------------- time cycle (F-044)
# The three lists of the kb time cycle, computed ONCE per invocation and fed to
# every surface (check/graph/corpus warn streams, `stale`, orient) -- never a
# leaner re-implementation per surface, which is how under-counting is born.

KB_GENERATED_RE = re.compile(r"GENERATED by \S+ index - do not edit by hand")
KB_HEX12_RE = re.compile(r"^[0-9a-f]{12}$")


# A citation of a claim id is a run of exactly its 12 lowercase hex characters
# NOT embedded in a longer hex run: a git hash sharing a substring must never
# count as a citation (either side, either case). Two such bounded runs cannot
# overlap, so findall returns every one of them.
KB_HEX_TOKEN_RE = re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{12}(?![0-9a-fA-F])")


def _kb_hex_tokens(text):
    """The ids a text cites, extracted in one pass (F-069). Callers test
    membership instead of scanning the text once per id: that per-(document,
    id) scan made the time cycle grow with superseded ids x living documents."""
    return frozenset(KB_HEX_TOKEN_RE.findall(text))


def _kb_df_entries(value):
    """A derived_from cell -> its entries: a single value or the inline list
    `[a, b]`, each kb_unquote'd (quoted paths with spaces are legal YAML)."""
    v = (value or "").strip()
    if not v:
        return []
    if v.startswith("[") and v.endswith("]"):
        return [kb_unquote(e) for e in v[1:-1].split(",") if kb_unquote(e)]
    return [kb_unquote(v)]


def kb_time_cycle(docs):
    """-> {"cited":    [(doc_rel, old_id, missing_ids, succ_ids)],
          "expired":  [(topic_rel, id, until, cited_by)],
          "chain":    [(node_rel, ground_rel, via)],
          "dangling": [(owner_rel, raw_entry)]}      -- each list sorted.

    Read-only, tolerant per file: a malformed table or frontmatter drops that
    file's contribution (the syntax finding belongs to the claims/corpus
    checks). cited: a LIVING document containing a SUPERSEDED id without every
    successor id visible in the same document -- the self-clearing condition,
    so an append-only Diary correction naming the successors is a legal fix.
    Living excludes corpus/given/ (+ sidecars: remedy-free), generated files
    (header marker, ANY lens's entry point), and SUPERSEDED tombstones; the
    OWNING topic self-clears by construction (its state cell carries every
    successor id). expired: `valid` windows whose half-open `until` has
    passed -- computed here, NEVER written back (state writes belong to
    reconciliation). chain: transitive reverse derived_from closure from
    superseded given/ artifacts, edges from BOTH carriers (note frontmatter
    and given/*.meta.md sidecars). dangling: any derived_from entry that
    resolves to nothing -- standing, supersession or not: a chain must be
    walkable BEFORE anything falls."""
    import datetime as _dt
    import posixpath
    cited, expired, chain, dangling = [], [], [], []
    superseded = {}
    windows = []
    topics = docs / "topics"
    if topics.is_dir():
        for p in sorted(topics.glob("*.md")):
            if p.name == "INDEX.md":
                continue
            try:
                rows, _ = kb_parse_claims(sdlc_core.read_text(p))
            except Exception:
                continue
            rel = "topics/" + p.name
            for row in rows:
                rid = (row.get("id") or "").strip()
                if not KB_HEX12_RE.match(rid):
                    continue
                m = re.match(r"^SUPERSEDED ([0-9a-f, ]+)$",
                             (row.get("state") or "").strip())
                if m:
                    succs = tuple(x.strip() for x in m.group(1).split(",")
                                  if KB_HEX12_RE.match(x.strip()))
                    if succs:
                        superseded[rid] = succs
                try:
                    scope = kb_parse_scope(row.get("valid") or "-")
                except Exception:
                    continue
                if scope[0] == "window" and scope[2]:
                    windows.append((rel, rid, scope[2]))
    living = []
    for p in sorted(docs.rglob("*.md")):
        rel = p.relative_to(docs).as_posix()
        if rel.startswith("corpus/given/"):
            continue
        try:
            text = sdlc_core.read_text(p)
        except Exception:
            continue
        if KB_GENERATED_RE.search(text[:512]):
            continue
        meta = sdlc_core.load_frontmatter(text.splitlines()) or {}
        if (meta.get("status") or "").strip() == "SUPERSEDED":
            continue
        living.append((rel, text))
    # One token pass per living document, and none at all on a KB with no
    # supersession and no validity window (the orient line runs this at every
    # session start).
    tokens = ({rel: _kb_hex_tokens(text) for rel, text in living}
              if superseded or windows else {})
    for rel, _text in living:
        cites = tokens[rel] if tokens else frozenset()
        for old in cites.intersection(superseded):
            succs = superseded[old]
            missing = tuple(x for x in succs if x not in cites)
            if missing:
                cited.append((rel, old, missing, succs))
    today = _dt.date.today().isoformat()
    for topic_rel, rid, until in sorted(windows):
        if until <= today:
            by = tuple(rel for rel, _text in living
                       if rel != topic_rel and rid in tokens[rel])
            expired.append((topic_rel, rid, until, by))
    rev = {}
    node_meta = {}
    sup_arts = set()
    notes_dir = docs / "corpus" / "notes"
    given_dir = docs / "corpus" / "given"

    def _resolve(entry):
        # Normalize BEFORE resolving: `./x`, `a//b`, `a/../b` resolve on the
        # filesystem but would never match the canonical node keys, so the
        # walk would silently stop with neither a chain entry nor a dangling
        # warn (closure-review WARN-1). Backslashed spellings stay loud: no
        # `/` means the bare-name ladder, which dangles them visibly.
        entry = posixpath.normpath(entry)
        if "/" in entry:
            return entry if (docs / entry).is_file() else None
        for base in ("corpus/notes/", "corpus/given/"):
            if (docs / (base + entry)).is_file():
                return base + entry
        return None

    def _edges_of(owner_rel, meta):
        for e in _kb_df_entries(meta.get("derived_from")):
            target = _resolve(e)
            if target is None:
                dangling.append((owner_rel, e))
            else:
                rev.setdefault(target, set()).add(owner_rel)

    if notes_dir.is_dir():
        for p in sorted(notes_dir.glob("*.md")):
            rel = "corpus/notes/" + p.name
            try:
                meta = sdlc_core.load_frontmatter(
                    sdlc_core.read_text(p).splitlines()) or {}
            except Exception:
                continue
            node_meta[rel] = meta
            _edges_of(rel, meta)
    if given_dir.is_dir():
        for mp in sorted(given_dir.glob("*.meta.md")):
            orig_rel = "corpus/given/" + mp.name[:-len(".meta.md")]
            try:
                meta = sdlc_core.load_frontmatter(
                    sdlc_core.read_text(mp).splitlines()) or {}
            except Exception:
                continue
            node_meta[orig_rel] = meta
            _edges_of(orig_rel, meta)
            sup = kb_unquote(meta.get("supersedes"))
            if sup:
                sup_arts.add("corpus/given/" + sup)
    for ground in sorted(sup_arts):
        seen = {ground}
        frontier = [(ground, ())]
        while frontier:
            node, via = frontier.pop()
            for owner in sorted(rev.get(node, ())):
                if owner in seen:
                    continue
                seen.add(owner)
                owner_via = via + (node,)
                tomb = (node_meta.get(owner, {}).get("status")
                        or "").strip() == "SUPERSEDED"
                if owner not in sup_arts and not tomb:
                    chain.append((owner, ground, owner_via))
                frontier.append((owner, owner_via))
    cited.sort()
    expired.sort()
    chain.sort()
    dangling.sort()
    return {"cited": cited, "expired": expired,
            "chain": chain, "dangling": dangling}


def kb_time_cycle_warns(cycle):
    """-> (cited_lines, chain_lines, dangling_lines). ASCII only."""
    cited = ["%s: cites %s, superseded by %s -- successor(s) %s not named; "
             "revise per the Revision doctrine"
             % (rel, old, ", ".join(succs), ", ".join(missing))
             for rel, old, missing, succs in cycle["cited"]]
    chain = []
    for node, ground, via in cycle["chain"]:
        tail = ("supersede the note" if node.startswith("corpus/notes/")
                else "supersede the derivation")
        chain.append("%s: derives (via %s) from %s, which a newer version "
                     "supersedes -- re-derive from the successor or %s"
                     % (node, " -> ".join(via), ground, tail))
    dang = ["%s: derived_from %s resolves to nothing -- the chain is not "
            "walkable" % (o, e) for o, e in cycle["dangling"]]
    return cited, chain, dang


# ------------------------------------------------------- portability (F-030)
# Export a subgraph WITH the bytes its claims cite; import it additively.
#
# The bundle mirrors the docs-root layout on purpose: claim `source` cells are
# docs-root-relative, so nothing is rewritten on import and `kb_claim_id` --
# sha256(path#locator#qty), text excluded -- mints the SAME id in both projects.
# That is what makes de-duplication mechanical instead of a judgement call, and
# it is why this feature is small.

BUNDLE_MANIFEST = "MANIFEST.md"


def kb_claim_sources(row):
    """The docs-root-relative artifact paths a claim row cites (no locators)."""
    out = []
    for src in row["source"].split(";"):
        src = src.strip()
        if src and "#" in src:
            out.append(src.rsplit("#", 1)[0])
        elif src:
            out.append(src)
    return out


def kb_collect_topics(docs):
    """{slug: (path, text, rows)} for every topic node that parses."""
    out = {}
    tdir = docs / "topics"
    if not tdir.is_dir():
        return out
    for p in sorted(tdir.glob("*.md")):
        if p.name == "INDEX.md":
            continue
        text = sdlc_core.read_text(p)
        meta = sdlc_core.load_frontmatter(text.splitlines()) or {}
        rows, _ = kb_parse_claims(text)
        out[(meta.get("topic") or p.stem).strip()] = (p, text, rows)
    return out


def kb_export_closure(docs, slugs):
    """(topics, artifacts, added_for_conflicts, errors).

    Closure in two directions, because a partial export produces a target whose
    own checks fail:
      * every artifact a selected claim cites travels with it -- a claim whose
        source cannot be reopened is model knowledge arriving by another route;
      * every row a CONTESTED row points at travels too, since the symmetry
        check refuses a set that lost half its members. When such a row lives in
        an unselected topic, that topic is ADDED and reported, never dropped.
    """
    all_topics = kb_collect_topics(docs)
    errors = []
    for s in slugs:
        if s not in all_topics:
            errors.append("no such topic: %s" % s)
    if errors:
        return {}, [], [], errors
    selected = dict((s, all_topics[s]) for s in slugs)
    # id -> slug, over the WHOLE graph, so a conflict partner is findable
    owner_of = {}
    declared_ids = set()
    for slug, (_p, _t, rows) in all_topics.items():
        for r in rows:
            if r["id"]:
                owner_of[r["id"]] = slug
                if _kb_is_declared(r):
                    declared_ids.add(r["id"])
    added = []
    pending = list(selected)
    while pending:
        slug = pending.pop()
        for r in selected[slug][2]:
            if _kb_is_declared(r):
                continue  # F-084: a declaration stays in this project
            _kind, refs = _kb_states(r["state"])
            for ref in refs:
                other = owner_of.get(ref)
                if ref in declared_ids:
                    errors.append("claim %s in topic '%s' points at %s, a DECLARED row: "
                                  "declarations are not exported and a fact never "
                                  "points at one -- run check" % (r["id"] or "(no id)",
                                                                   slug, ref))
                elif other is None:
                    errors.append("claim %s in topic '%s' points at id %s, which "
                                  "no topic owns: export would carry a broken set"
                                  % (r["id"] or "(no id)", slug, ref))
                elif other not in selected:
                    selected[other] = all_topics[other]
                    added.append(other)
                    pending.append(other)
    artifacts = []
    seen = set()
    for slug, (_p, _t, rows) in sorted(selected.items()):
        for r in rows:
            if _kb_is_declared(r):
                continue  # its artifact stays with the declaration
            for rel in kb_claim_sources(r):
                for cand in (rel, rel + ".meta.md",
                             rel[:-len(Path(rel).suffix)] + ".txt" if Path(rel).suffix else rel):
                    if cand in seen:
                        continue
                    if cand.endswith(".meta.md") and (docs / cand).is_file() and \
                            kb_is_tombstone(sdlc_core.load_frontmatter(
                                sdlc_core.read_text(docs / cand).splitlines())):
                        continue  # F-077: a tombstone never travels
                    if (docs / cand).is_file():
                        seen.add(cand)
                        artifacts.append(cand)
    return selected, artifacts, added, errors


def kb_bundle_write(docs, out, selected, artifacts, project):
    """Write the bundle. Mirrors the docs-root layout; no path is rewritten.
    Returns whether a not-yet-honored mark was dropped (F-080) -- a yes/no,
    never a count: a count of dropped marks is a count of claims by the mark."""
    out.mkdir(parents=True, exist_ok=True)
    (out / "topics").mkdir(exist_ok=True)
    dropped = False
    for slug, (p, text, _rows) in sorted(selected.items()):
        text, d = kb_drop_marks(text)
        dropped = dropped or d
        text = kb_drop_declarations(text)
        (out / "topics" / p.name).write_text(text, encoding="utf-8")
    for rel in artifacts:
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((docs / rel).read_bytes())
    lines = ["---", "kb_bundle: 1", "source_project: %s" % project,
             "topics: [%s]" % ", ".join(sorted(selected)),
             "artifacts: %d" % len(artifacts), "---",
             "# KB bundle", "",
             "Import with `sdlc_check.py import <this directory>`. Additive: it "
             "never overwrites a node and never deletes anything.", ""]
    for rel in artifacts:
        lines.append("- `%s` sha256:%s" % (rel, kb_sha256_bytes(docs / rel)))
    (out / BUNDLE_MANIFEST).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return dropped


def _kb_replace_cells(line, updates):
    """One claim-table row with the cells at the given column indexes replaced;
    everything else -- indentation, outer pipes, a CRLF tail -- verbatim."""
    end = "\r" if line.endswith("\r") else ""
    body = line[:-1] if end else line
    lead = body[:len(body) - len(body.lstrip())]
    s = body.strip()
    opens, closes = s.startswith("|"), len(s) > 1 and s.endswith("|")
    cells = s[1 if opens else 0:len(s) - 1 if closes else len(s)].split("|")
    for i, v in updates.items():
        cells[i] = " %s " % v
    return "%s%s%s%s%s" % (lead, "|" if opens else "", "|".join(cells),
                           "|" if closes else "", end)


def _kb_states(state):
    """'CONTESTED a, b' / 'SUPERSEDED a' / 'DIVERGES a' -> (kind, [ids]);
    OK/other -> (None, []). The one parser of the full state grammar."""
    m = re.match(r"^(CONTESTED|SUPERSEDED|DIVERGES) ([0-9a-f, ]+)$", (state or "").strip())
    if not m:
        return None, []
    return m.group(1), [t.strip() for t in m.group(2).split(",") if t.strip()]


def _kb_bom_text(data):
    """(bom, text): a UTF-8 BOM (Windows authoring) is kept apart and given back
    on write, as sdlc_core.read_text reads past it."""
    bom = codecs.BOM_UTF8 if data.startswith(codecs.BOM_UTF8) else b""
    return bom, data[len(bom):].decode("utf-8")


def _kb_foreign_note(data, project, rel):
    """F-083: the bytes of a ruling note as it lands in another project, and the
    number of lines inserted. Lines go right after the opening '---' with the
    note's own line ending; an existing origin line is rewritten in place, so it
    moves nothing. None when the note opens no frontmatter."""
    bom, text = _kb_bom_text(data)
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(nl)
    if not lines or lines[0].strip() != "---":
        return None
    end = next((i for i in range(1, min(len(lines), 60)) if lines[i].strip() == "---"),
               None)
    if end is None:
        return None
    inserted = ["imported_from: %s — %s" % (project, rel)]
    origin = [i for i in range(1, end) if re.match(r"^origin:", lines[i], re.I)]
    for i in origin:
        lines[i] = "origin: imported"
    if not origin:
        inserted.append("origin: imported")
    lines[1:1] = inserted
    return bom + nl.join(lines).encode("utf-8"), len(inserted)


def _kb_shift_loc(loc, k):
    a, b = (int(x) for x in LOC_LINE_RE.match(loc).groups())
    if a >= 2:
        return "L%d-%d" % (a + k, b + k)
    return "L1-%d" % (b + k if b >= 2 else 1)


def _kb_span(data, loc):
    """The lines a line locator addresses, minus the two lines an import may
    insert or rewrite -- what a moved locator must still cite."""
    a, b = (int(x) for x in LOC_LINE_RE.match(loc).groups())
    return [x for x in _kb_bom_text(data)[1].splitlines()[a - 1:b]
            if not re.match(r"^(imported_from|origin):", x, re.I)]


def _kb_rewrite_derived_from(data, renames):
    """A note whose derived_from names a renamed ruling note names the copy. The
    edit stays on the derived_from line, so no line moves."""
    bom, text = _kb_bom_text(data)
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(nl)
    if not lines or lines[0].strip() != "---":
        return data
    for i in range(1, min(len(lines), 60)):
        if lines[i].strip() == "---":
            break
        m = re.match(r"^(derived_from:\s*)(.*)$", lines[i], re.I)
        if not m:
            continue
        val = m.group(2).strip()
        listed = val.startswith("[") and val.endswith("]")
        toks = val[1:-1].split(",") if listed else [val]
        out = []
        for tok in toks:
            e = kb_unquote(tok)
            hit = next((new for old, new in renames.items()
                        if e in (old, old[len("corpus/notes/"):])), None)
            out.append((" " if listed and out else "") + hit if hit else tok)
        new = ("[%s]" % ",".join(out)) if listed else out[0]
        lines[i] = m.group(1) + new
    return bom + nl.join(lines).encode("utf-8")


def kb_import_foreign_rulings(bundle, docs, topic_rels, written, project):
    """F-083 -- knowledge crosses a project boundary, authority does not
    (portability.md §4, owner rulings 2026-08-03 and R3 of F-083).

    -> (content, drop, report, errors). content: {rel: bytes} to write instead of
    the bundle's bytes; drop: rels never to write (a ruling note under its own
    name); report: {"converted": n, "notes": [renamed notes of skipped topics]}.

    A RULING row arrives IMPORTED, resting on a renamed copy of its note that
    names the origin; the rows it superseded and the ruling form one CONTESTED
    set again. The note is never edited in place: a line inserted into it moves
    the line every locator cites, and check verifies line bounds, not text."""
    errors, content, drop = [], {}, set()
    report = {"converted": 0, "notes": []}
    slug = re.sub(r"[^a-z0-9]", "-", (project or "unknown").lower())
    parsed = {}
    for rel in topic_rels:
        text = (bundle / rel).read_bytes().decode("utf-8")
        parsed[rel] = (text, kb_parse_claims(text)[0])
    rulings = [(rel, r) for rel in topic_rels for r in parsed[rel][1]
               if r["prov"].strip().upper() == "RULING"]
    # Which notes land foreign. A note cited by a RULING row is a ruling note;
    # so is any bundle note declaring a basis: (reconciliation.md) -- one can
    # travel without its row, cited by another row, and land first under its
    # own name, ready to carry a local-looking RULING later (closure review B1).
    users = {}                        # note -> [(topic rel, row)] RULING rows on it
    for rel, r in rulings:
        src = r["source"].split(";")[0].strip()
        path, _, loc = src.rpartition("#")
        if not (re.match(r"^corpus/notes/[^/]+\.md$", path) and LOC_LINE_RE.match(loc)
                and (bundle / path).is_file()):
            if rel in written:
                errors.append("claim %s in %s is a RULING resting on %r, not on a "
                              "note in corpus/notes/ cited by line (a ruling is a "
                              "note, reconciliation.md) -- carry it by hand"
                              % (r["id"] or "(no id)", rel, src))
            continue
        users.setdefault(path, []).append((rel, r))
    ndir = bundle / "corpus" / "notes"
    for p in (sorted(ndir.glob("*.md")) if ndir.is_dir() else []):
        meta = sdlc_core.load_frontmatter(_kb_bom_text(p.read_bytes())[1].splitlines()) or {}
        if meta.get("basis") and not meta.get("imported_from"):
            users.setdefault("corpus/notes/" + p.name, [])
    renames = {}                      # original note -> (copy, bytes, k)
    for path in sorted(users):
        data = (bundle / path).read_bytes()
        meta = sdlc_core.load_frontmatter(_kb_bom_text(data)[1].splitlines()) or {}
        ruled = [(rel, r) for rel, r in users[path] if rel in written]
        where = ("claim %s in %s" % (ruled[0][1]["id"] or "(no id)", ruled[0][0])
                 if ruled else path)
        if meta.get("imported_from"):
            if ruled:
                errors.append("%s is a RULING on %s, which already names a foreign "
                              "origin -- the source project relabelled an imported "
                              "decision; fix it there" % (where, path))
            continue                  # already foreign: it travels as it is
        home = docs / path
        if not ruled and home.is_file() and                 kb_sha256_bytes(home) == hashlib.sha256(data).hexdigest():
            continue                  # this project holds the note, no topic here rules on it
        foreign = _kb_foreign_note(data, project, path)
        if foreign is None:
            if ruled:
                errors.append("%s rests on %s, which opens no frontmatter"
                              % (where, path))
            continue
        copy = "corpus/notes/imported_%s_%s" % (slug, path[len("corpus/notes/"):])
        if sdlc_core.confine_under(docs, copy) is None:
            errors.append("renamed note %r escapes the docs root" % copy)
            continue
        renames[path] = (copy, foreign[0], foreign[1])
    if errors:
        return content, drop, report, errors
    for old, (copy, data, _k) in renames.items():
        drop.add(old)
        content[copy] = data
    for p in sorted((bundle / "corpus" / "notes").glob("*.md")) \
            if (bundle / "corpus" / "notes").is_dir() else []:
        rel = "corpus/notes/" + p.name
        if rel in drop:
            continue
        new = _kb_rewrite_derived_from(p.read_bytes(),
                                       dict((o, c) for o, (c, _d, _k) in renames.items()))
        if new != p.read_bytes():
            content[rel] = new
    for copy in [c for c in list(content) if c in [v[0] for v in renames.values()]]:
        content[copy] = _kb_rewrite_derived_from(
            content[copy], dict((o, c) for o, (c, _d, _k) in renames.items()))

    # rows of the topics this import writes: move sources, re-mint ids
    ren, rows_w, prov_of = {}, [], {}
    for rel in topic_rels:
        if rel not in written:
            continue
        for r in parsed[rel][1]:
            rows_w.append((rel, r))
    for rel, r in rows_w:
        cells = [s.strip() for s in r["source"].split(";") if s.strip()]
        moved = []
        for n, s in enumerate(cells):
            path, _, loc = s.rpartition("#")
            if path in renames and LOC_LINE_RE.match(loc):
                copy, data, k = renames[path]
                nloc = _kb_shift_loc(loc, k)
                if _kb_span((bundle / path).read_bytes(), loc) != _kb_span(data, nloc):
                    errors.append("claim %s in %s: %s#%s would not cite the same text "
                                  "in %s#%s -- nothing was converted"
                                  % (r["id"], rel, path, loc, copy, nloc))
                cells[n] = "%s#%s" % (copy, nloc)
                moved.append(n)
            elif path in renames:
                errors.append("claim %s in %s cites %s by %r, not by line: the "
                              "renamed copy would move it" % (r["id"], rel, path, loc))
        r["_source"] = "; ".join(cells) if moved else r["source"]
        r["_id"] = r["id"]
        if 0 in moved and r["id"]:
            path, _, loc = cells[0].rpartition("#")
            try:
                r["_id"] = kb_claim_id(path, loc, kb_qty_key(r["qty"]))
            except ValueError:
                pass
            ren[r["id"]] = r["_id"]
        conv = r["prov"].strip().upper() == "RULING" and \
            r["source"].split(";")[0].strip().rpartition("#")[0] in renames
        r["_prov"] = "IMPORTED" if conv else r["prov"]
        r["_conv"] = conv
    if errors:
        return content, drop, report, errors
    converted = set(r["id"] for _rel, r in rows_w if r["_conv"])
    report["converted"] = len(converted)
    members = {}
    for rel, r in rows_w:
        kind, targets = _kb_states(r["state"])
        hit = [t for t in targets if t in converted]
        if kind != "SUPERSEDED" or not hit:
            continue
        if len(hit) != len(targets):
            errors.append("claim %s in %s is SUPERSEDED by the ruling %s and by %s, "
                          "which is not a ruling: its set cannot reopen without "
                          "deciding which successor stands -- re-rule it in the "
                          "source project" % (r["id"], rel, ", ".join(hit),
                                              ", ".join(t for t in targets if t not in hit)))
            continue
        for t in hit:
            members.setdefault(t, set()).add(r["id"])
    partners = {}
    for rel, r in rows_w:
        if r["_conv"] and members.get(r["id"]):
            kind, targets = _kb_states(r["state"])
            if kind == "SUPERSEDED" and any(t not in converted for t in targets):
                errors.append("ruling %s in %s settled rows but was itself superseded "
                              "by %s, which is not a ruling: its set cannot reopen "
                              "cleanly -- re-rule it in the source project"
                              % (r["id"], rel, ", ".join(targets)))
            group = members[r["id"]] | {r["id"]}
            for x in group:
                partners.setdefault(x, set()).update(group - {x})
    if errors:
        return content, drop, report, errors
    for rel, r in rows_w:
        kind, targets = _kb_states(r["state"])
        if r["id"] in partners:
            own = set(targets) if kind == "CONTESTED" else set()
            r["_state"] = "CONTESTED " + ", ".join(
                sorted(ren.get(t, t) for t in own | partners[r["id"]]))
        elif kind:
            r["_state"] = "%s %s" % (kind, ", ".join(ren.get(t, t) for t in targets))
        else:
            r["_state"] = r["state"]
        prov_of[r["_id"]] = r["_prov"].strip().upper()

    # boundary: every pointer must resolve after the import, never onto a foreign row
    held = {}
    for _slug, (_p, _t, trows) in kb_collect_topics(docs).items():
        for t in trows:
            if t["id"]:
                held[t["id"]] = (t["prov"].strip().upper(), t["state"])
    for rel, r in rows_w:
        kind, targets = _kb_states(r["_state"])
        for t in targets:
            prov = prov_of.get(t) or (held.get(t) or (None,))[0]
            if t not in prov_of and t in held and kind == "CONTESTED":
                hkind, hts = _kb_states(held[t][1])
                if hkind != "CONTESTED" or r["_id"] not in hts:
                    errors.append("claim %s in %s is CONTESTED with %s, which this "
                                  "project holds without naming it back: the import "
                                  "never edits an existing topic -- add the pointer "
                                  "there first, or carry the row by hand"
                                  % (r["_id"], rel, t))
                    continue
            if prov is None:
                errors.append("claim %s in %s points at %s, which this import does not "
                              "write and this project does not hold: its set would "
                              "arrive incomplete -- import the topics together"
                              % (r["_id"], rel, t))
            elif kind == "SUPERSEDED" and prov == "IMPORTED":
                errors.append("claim %s in %s is SUPERSEDED by %s, which is IMPORTED "
                              "here: a foreign decision cannot settle it -- import the "
                              "topics together, or reopen the set by hand"
                              % (r["_id"], rel, t))
    if errors:
        return content, drop, report, errors

    for rel in topic_rels:
        if rel not in written:
            continue
        text, rows = parsed[rel]
        lines = text.split("\n")
        for r in rows:
            up = {}
            for col, key in (("id", "_id"), ("source", "_source"), ("prov", "_prov"),
                             ("state", "_state")):
                if r[key] != r[col]:
                    up[CLAIM_COLUMNS.index(col)] = r[key]
            if up:
                lines[r["_line"] - 1] = _kb_replace_cells(lines[r["_line"] - 1], up)
        new = "\n".join(lines).encode("utf-8")
        if new != (bundle / rel).read_bytes():
            content[rel] = new
    for rel, r in rulings:
        path = r["source"].split(";")[0].strip().rpartition("#")[0]
        if rel not in written and path in renames:
            note = renames[path][0]
            if note not in report["notes"]:
                report["notes"].append(note)
    return content, drop, report, errors


def kb_import_plan(bundle, docs, report=None):
    """(writes, skipped_topics, dedup, errors) -- computed BEFORE anything is
    written, because an import that half-applies leaves a tree whose checks fail
    and whose owner cannot tell what landed. Each write is (rel, bytes, dst):
    the bytes are the bundle's, except where F-083 makes a foreign ruling land
    foreign (kb_import_foreign_rulings). `report`, when a dict, receives what
    that conversion did."""
    errors, writes, skipped, dedup = [], [], [], []
    man = bundle / BUNDLE_MANIFEST
    if not man.is_file():
        return [], [], [], ["not a kb bundle: no %s in %s" % (BUNDLE_MANIFEST, bundle)]
    meta = sdlc_core.load_frontmatter(sdlc_core.read_text(man).splitlines()) or {}
    if str(meta.get("kb_bundle", "")).strip() != "1":
        return [], [], [], ["%s carries no 'kb_bundle: 1'" % BUNDLE_MANIFEST]

    known_ids = set()
    target = kb_collect_topics(docs)
    for _slug, (_p, _t, rows) in target.items():
        for r in rows:
            if r["id"]:
                known_ids.add(r["id"])

    entries, topic_rels, written = [], [], set()
    for p in sorted(bundle.rglob("*")):
        if not p.is_file() or p.name == BUNDLE_MANIFEST:
            continue
        rel = p.relative_to(bundle).as_posix()
        dst = sdlc_core.confine_under(docs, rel)
        if dst is None:
            errors.append("bundle entry %r escapes the docs root — refusing the "
                          "whole import, not just this file" % rel)
            continue
        if rel.startswith("topics/"):
            topic_rels.append(rel)
            if dst.is_file():
                skipped.append(rel)
                continue
            written.add(rel)
        entries.append((rel, p, dst))
    for rel, p, _dst in entries:
        if rel.startswith("topics/"):
            for r in kb_parse_claims(sdlc_core.read_text(p))[0]:
                if _kb_is_declared(r):
                    errors.append("%s: claim %s is DECLARED -- a declaration stays in "
                                  "the project that made it; export never ships one, "
                                  "so this bundle was edited by hand"
                                  % (rel, r["id"] or "(no id)"))
    if errors:
        return [], skipped, [], errors

    content, drop, rep, errors = kb_import_foreign_rulings(
        bundle, docs, topic_rels, written, str(meta.get("source_project", "")).strip())
    if report is not None:
        report.update(rep)
    if errors:
        return [], skipped, [], errors
    planned = [(rel, p, dst) for rel, p, dst in entries if rel not in drop]
    for rel in sorted(set(content) - set(rel for rel, _p, _d in entries)):
        planned.append((rel, None, sdlc_core.confine_under(docs, rel)))
    for rel, p, dst in planned:
        data = content[rel] if rel in content else p.read_bytes()
        if dst.is_file() and not rel.startswith("topics/"):
            if kb_sha256_bytes(dst) != hashlib.sha256(data).hexdigest():
                errors.append("%s exists with different bytes (target %s… vs "
                              "bundle %s…): content-addressed names must mean "
                              "equal content" % (rel, kb_sha256_bytes(dst)[:8],
                                                 hashlib.sha256(data).hexdigest()[:8]))
            continue
        writes.append((rel, data, dst))

    for rel, data, _dst in writes:
        if not rel.startswith("topics/"):
            continue
        rows, _ = kb_parse_claims(data.decode("utf-8"))
        for r in rows:
            if r["id"] and r["id"] in known_ids:
                dedup.append(r["id"])
    return writes, skipped, dedup, errors


# ------------------------------------------------------------------ commands

MEMORY_DIRS = ("vision", "reference", "architecture", "functional", "strategic",
               "solutions", "research", "strategy", "tactics", "deliverables",
               "spikes", "topics", "corpus/notes")


def _memory_safe(docs, path):
    """Reject links (including Windows junctions) and paths outside the docs root."""
    try:
        path.resolve().relative_to(docs.resolve())
        for p in (path, *path.parents):
            if p == docs.parent:
                break
            if p.is_symlink() or (hasattr(p, "is_junction") and p.is_junction()):
                return False
        return True
    except (OSError, ValueError, RuntimeError):
        return False


def memory_records(docs):
    """Live metadata, not claims or work states. Never traverse raw corpus or logs."""
    paths = []
    readme = docs / "README.md"
    default = "code"
    if readme.is_file() and _memory_safe(docs, readme):
        paths.append(readme)
        meta = sdlc_core.load_frontmatter(sdlc_core.read_text(readme).splitlines())
        default = kb_unquote(meta.get("default_domain")) or default
    for dirname in MEMORY_DIRS:
        folder = docs / dirname
        if not folder.is_dir() or not _memory_safe(docs, folder):
            continue
        for base, dirs, files in os.walk(folder, followlinks=False):
            dirs[:] = sorted(d for d in dirs if not d.startswith((".", "harness_"))
                             and _memory_safe(docs, Path(base) / d))
            for name in files:
                p = Path(base) / name
                if (p.suffix.lower() == ".md" and name not in ("INDEX.md", "features_history.md")
                        and _memory_safe(docs, p)):
                    paths.append(p)
    records = []
    for p in sorted(set(paths), key=lambda p: p.relative_to(docs).as_posix()):
        text = p.read_bytes().decode("utf-8", errors="replace")
        meta = sdlc_core.load_frontmatter(text.splitlines())
        title = next((line[2:].strip() for line in text.splitlines()
                      if line.startswith("# ")), p.stem)
        # LF-normalized like the guides' source_hash: an autocrlf checkout must
        # regenerate the same catalog as an LF one.
        records.append((p.relative_to(docs).as_posix(),
                        kb_unquote(meta.get("domain")) or default,
                        ", ".join(_as_list(meta.get("topics", ""))),
                        kb_unquote(meta.get("description")) or title,
                        sdlc_core.sha256_file(p)))
    return records


def _memory_table(records):
    def cell(value):
        return " ".join(value.split()).replace("|", "&#124;").replace("<", "&lt;")
    lines = ["| Path | Domain | Topics | Description | SHA256 |", "|---|---|---|---|---|"]
    lines += ["| " + " | ".join(cell(v) for v in row) + " |" for row in records]
    return "\n".join(lines) + "\n"


def memory_build_index(docs):
    return ("# Project memory (generated discovery catalog)\n\n"
            "Regenerate with the installed validator's index command. Paths are relative "
            "to the docs root. Read each source for authority, validity and status; "
            "a catalog entry is not a verified fact.\n\n" + _memory_table(memory_records(docs)))


def memory_index(docs):
    out = docs / "memory" / "INDEX.md"
    if not _memory_safe(docs, out):
        print("[ERROR] unsafe memory/INDEX.md output path; nothing written there")
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(memory_build_index(docs))
    print("[ok] project memory regenerated: %s" % out)
    return 0


def memory_validate(docs):
    out = docs / "memory" / "INDEX.md"
    if not _memory_safe(docs, out):
        print("[ERROR] unsafe memory/INDEX.md path")
        return 1
    if out.is_file() and sdlc_core.norm_text(sdlc_core.read_text(out)) != \
            sdlc_core.norm_text(memory_build_index(docs)):
        print("[ERROR] memory/INDEX.md not aligned: run the validator's index command")
        return 1
    return 0


def memory_recall(docs, query):
    words = query.casefold().split()
    rows = [r for r in memory_records(docs)
            if all(w in " ".join(r[:4]).casefold() for w in words)]
    print("# Project memory: live metadata lookup (read sources before deciding)")
    print(_memory_table(rows) if rows else "No metadata match; this is not proof of no knowledge.")
    return 0


def kb_refresh_indexes(docs):
    """Derived indexes without invoking any domain's main index command."""
    for dirname, builder in (("topics", kb_build_topic_index), ("corpus", kb_build_corpus_index)):
        out = docs / dirname / "INDEX.md"
        if not _memory_safe(docs, out):
            print("[ERROR] unsafe %s/INDEX.md output path" % dirname)
            return 1
        if (docs / dirname).is_dir():
            out.write_text(builder(docs), encoding="utf-8")
            print("[ok] %s index regenerated: %s" % (dirname, out))
    return memory_index(docs)


def kb_validate_surface(docs, full=False):
    """Additive seam for marketing: preserve its own validator and report.
    `full` is marketing's check: the credential scan (F-077) runs there outside
    the topics/corpus guard, since document-guide snapshots need no corpus."""
    rc = max(memory_validate(docs), _kb_extra_validate(docs))
    if full:
        rc = max(rc, _kb_print_credentials(docs.parent, docs))
    if full and ((docs / "topics").is_dir() or (docs / "corpus").is_dir()):
        cycle = kb_time_cycle(docs)
        rc = max(rc, kb_cmd_graph(docs, cycle), kb_cmd_corpus(docs, cycle))
    return rc

INTERCEPTED = {"index", "validate", "check", "graph", "corpus", "claim-id",
               "anchor", "export", "import", "stale", "recall", "adopt",
               "inventory"}


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


def kb_cmd_graph(docs, cycle=None):
    errors, warnings = kb_graph_check(docs)
    ce, cw, cn = kb_check_claims(docs)
    if cycle is None:
        cycle = kb_time_cycle(docs)
    tc_cited, _tc_chain, _tc_dang = kb_time_cycle_warns(cycle)
    total_w = len(warnings) + len(cw) + len(tc_cited)
    for w in warnings + cw + tc_cited:
        print("[warn]  %s" % w)
    for n in cn:
        print("[note]  %s" % n)
    for e in errors + ce:
        print("[ERROR] %s" % e)
    total_e = len(errors) + len(ce)
    if total_e:
        print("Graph: %d errors, %d warnings." % (total_e, total_w))
        return 1
    if not (docs / "topics").is_dir():
        print("[ok] no topics/ - nothing to check")
    else:
        print("[ok] topic graph and claim ledger consistent "
              "(%d warnings)" % total_w)
    return 0


def kb_cmd_corpus(docs, cycle=None, extra_errors=()):
    errors, warnings = kb_corpus_check(docs)
    errors = list(extra_errors) + errors
    if cycle is None:
        cycle = kb_time_cycle(docs)
    _tc_cited, tc_chain, tc_dang = kb_time_cycle_warns(cycle)
    warnings = warnings + tc_chain + tc_dang
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
    return max(rc, kb_refresh_indexes(docs)) if rc == 0 else rc


def _kb_extra_validate(docs):
    """The kb additions to validate: generated-index freshness for the overlay's
    two indexes. Prints nothing on a tree without them (TS-K7)."""
    rc = 0
    for e in kb_exclusions(docs)[1]:
        print("[ERROR] %s" % e)
        rc = 1
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
    return max(rc, kb_validate_surface(docs))


def kb_cmd_check(root, docs, strict=False, hybrid=False):
    # The spine's check owns its banners and summary line: reuse it whole, so a
    # tree with no kb surface gets byte-identical output. The kb checks ride its
    # hooks -- index freshness in the validate stage, graph/corpus as sections
    # only when the surface exists -- so the summary is printed after all of them.
    sections = ()
    if (docs / "topics").is_dir() or (docs / "corpus").is_dir():
        cycle = kb_time_cycle(docs)
        sections = (("graph", lambda: kb_cmd_graph(docs, cycle)),
                    ("corpus", lambda: kb_cmd_corpus(docs, cycle)))
    return sdlc_core.cmd_check(
        root, strict=strict, hybrid=hybrid,
        extra_validate=lambda: max(_kb_extra_validate(docs), memory_validate(docs),
                                   _kb_print_credentials(root, docs)),
        extra_sections=sections)


def kb_cmd_adopt(root, docs):
    """F-077: the dry-run plan of adopting kb-agentic on an existing docs root --
    which document guides rest on a snapshot, and what moving each into
    corpus/given/ involves. Reads only; there is no --apply (portability.md
    par.6: the choice of source and the redaction are judgements)."""
    if not docs.is_dir():
        print("[ERROR] no docs root at %s" % docs)
        return 1
    given = docs / "corpus" / "given"
    twins = {}
    if given.is_dir():
        for g in sorted(given.iterdir()):
            if g.is_file() and not g.name.endswith(".meta.md"):
                try:
                    twins.setdefault(sdlc_core.sha256_file(g), g.name)
                except OSError:
                    pass
    print("=== adopt: document guides -> corpus/given/ (dry run) ===")
    code_n = 0
    for rel, _p, meta, _t in sdlc_core.list_guides(root):
        if (meta.get("source_kind") or "document").strip() != "document":
            code_n += 1
            continue
        df = (meta.get("distilled_from") or "").strip()
        print("%s" % rel)
        print("  distilled_from: %s" % (df or "(none)"))
        src = sdlc_core.confine_under(root, df) if df else None
        if df and src is None:
            print("  source: outside the project root -- not read")
            continue
        if src is None or not src.is_file():
            print("  source: missing")
            continue
        try:
            where = "/" + src.relative_to(root.resolve()).as_posix()
        except ValueError:
            where = ""
        if "/corpus/given/" in where:
            print("  source: already in corpus/given/")
            continue
        print("  source: %s" % (".sources/ snapshot" if "/reference/.sources/" in where
                                 else "elsewhere"))
        try:
            twin = twins.get(sdlc_core.sha256_file(src))
        except OSError:
            twin = None
        if twin:
            print("  same text already in corpus/given/%s" % twin)
        found = kb_credential_findings(src)
        if found:
            print("  " + _kb_cred_message("credential-shaped", found,
                                         "redact before storing (distillation.md par.1)")
                  .split(": ", 1)[1])
    print("%d code guide(s) stay on .sources/." % code_n)
    print("Nothing was written. Procedure: portability.md par.6 (kb-agentic).")
    return 0


# --------------------------------------------------------------------------
# F-084: the corpus's reach over the project that holds it. A file left out on
# purpose and a file nobody opened used to look the same; these classify every
# project file against the sidecars, by content, and name the residue.

KB_REGISTRY = "audit/INVENTORY_exclusions.md"
KB_REACH_DEADLINE = 1.0          # orient's walk; inventory has none (on demand)
_kb_clock = time.monotonic       # injectable for the deadline test
_KB_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\b")
# Windows: FILE_ATTRIBUTE_OFFLINE, RECALL_ON_OPEN, RECALL_ON_DATA_ACCESS;
# macOS: SF_DATALESS. A file whose bytes are not on the disk is never read --
# reading it would download it.
_KB_CLOUD_ATTRS = 0x1000 | 0x40000 | 0x400000
_KB_SF_DATALESS = 0x40000000
_KB_REPARSE_POINT = 0x400


class _KbDeadline(Exception):
    pass


def _kb_glob_regex(pattern):
    """FS2's gitignore subset -> (compiled regex, dir_only)."""
    dir_only = pattern.endswith("/")
    pat = pattern.rstrip("/")
    out, i = [], 0
    while i < len(pat):
        c = pat[i]
        if pat.startswith("**/", i):
            out.append("(?:[^/]+/)*")
            i += 3
        elif pat.startswith("**", i):
            out.append(".*")
            i += 2
        elif c == "*":
            out.append("[^/]*")
            i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        elif c == "[":
            j = pat.find("]", i + 1)
            if j < 0:
                out.append(re.escape(c))
                i += 1
            else:
                body = pat[i + 1:j]
                if body.startswith("!"):
                    body = "^" + body[1:]
                out.append("[%s]" % body.replace("\\", "\\\\"))
                i = j + 1
        else:
            out.append(re.escape(c))
            i += 1
    rx = "".join(out)
    rx = ("^" + rx + "$") if "/" in pat else ("^(?:.*/)?" + rx + "$")
    return re.compile(rx, re.IGNORECASE if os.name == "nt" else 0), dir_only


def kb_exclusions(docs):
    """(rows, errors) of the exclusion registry. rows: (pattern, regex,
    dir_only). An absent registry excludes nothing and is silent."""
    p = docs / KB_REGISTRY
    rows, errors = [], []
    if not p.is_file():
        return rows, errors
    import datetime as _dt
    for n, line in enumerate(sdlc_core.read_text(p).splitlines(), 1):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        joined = "".join(cells)
        if "-" in joined and set(joined) <= set("-: "):
            continue  # separator
        if cells and cells[0].lower() == "pattern":
            continue  # header
        where = "%s:%d" % (KB_REGISTRY, n)
        if len(cells) != 3:
            errors.append("%s: a row has three cells: pattern | reason | approved" % where)
            continue
        pattern, reason, approved = cells
        bad = []
        if not pattern:
            bad.append("empty pattern")
        elif pattern.startswith("/") or ".." in pattern.split("/"):
            bad.append("pattern %r leaves the project root" % pattern)
        if not reason:
            bad.append("empty reason -- say why it never enters the corpus")
        m = _KB_DATE_RE.match(approved)
        ok_date = False
        if m:
            try:
                _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                ok_date = True
            except ValueError:
                pass
        if not ok_date:
            bad.append("approved %r is not the day of the practitioner's approval "
                       "(YYYY-MM-DD)" % approved)
        rx = dir_only = None
        if not bad:
            try:
                rx, dir_only = _kb_glob_regex(pattern)
            except re.error as e:
                bad.append("pattern %r is not a valid glob (%s)" % (pattern, e))
        if bad:
            errors.append("%s: %s" % (where, "; ".join(bad)))
            continue
        rows.append((pattern, rx, dir_only))
    return rows, errors


def kb_excluded(rel, is_dir, rows):
    """The registry pattern matching project-relative `rel`, or None."""
    for pattern, rx, dir_only in rows:
        if dir_only and not is_dir:
            continue
        if rx.match(rel):
            return pattern
    return None


def kb_unreadable(entry):
    """'link' / 'cloud-only' for a DirEntry whose bytes are never read; None
    otherwise. Links include Windows junctions (the `_memory_safe` idiom)."""
    try:
        if entry.is_symlink():
            return "link"
        is_junction = getattr(entry, "is_junction", None)
        if is_junction is not None and is_junction():
            return "link"
        st = entry.stat(follow_symlinks=False)
    except OSError:
        return "unreadable"
    attrs = getattr(st, "st_file_attributes", 0) or 0
    if attrs & _KB_REPARSE_POINT and entry.is_dir(follow_symlinks=False):
        return "link"  # a junction on a runtime without is_junction
    if attrs & _KB_CLOUD_ATTRS or (getattr(st, "st_flags", 0) or 0) & _KB_SF_DATALESS:
        return "cloud-only"
    return None


def _kb_path_key(p):
    return os.path.normcase(os.path.abspath(str(p)))


def _kb_reach_index(docs):
    """What the sidecars say about originals: digest -> sidecar, named path ->
    (sidecar, original_sha256 or None), the artifacts' sizes. Tombstones count
    for nothing, their `original_path:` included."""
    by_digest, by_path, sizes = {}, {}, set()
    given = docs / "corpus" / "given"
    if not given.is_dir():
        return by_digest, by_path, sizes
    for meta_p in sorted(given.glob("*.meta.md")):
        meta = sdlc_core.load_frontmatter(sdlc_core.read_text(meta_p).splitlines()) or {}
        if kb_is_tombstone(meta):
            continue
        rel = "corpus/given/" + meta_p.name
        try:
            sizes.add((given / meta_p.name[:-len(".meta.md")]).stat().st_size)
        except OSError:
            pass
        for k in ("sha256", "original_sha256"):
            v = (meta.get(k) or "").strip().lower()
            if v:
                by_digest.setdefault(v, rel)
        op = kb_unquote(meta.get("original_path"))
        if op:
            osha = (meta.get("original_sha256") or "").strip().lower() or None
            for c in _kb_original_candidates(op, docs):
                try:
                    present = c.is_symlink() or c.exists()
                except OSError:
                    present = False
                if present:
                    by_path.setdefault(_kb_path_key(c), (rel, osha))
                    break
    return by_digest, by_path, sizes


def kb_corpus_reach(docs, rel=".", exact=True, deadline=None):
    """FS1/FS3: classify the project files under `rel` (project-relative).

    exact=True (inventory): every candidate is hashed -- comparison by content,
    wherever the file now lives. exact=False (orient's bound): only files whose
    size equals some given/ artifact's are hashed, and every file an
    original_path names counts as examined, so the NOT_EXAMINED count never
    undercounts. Returns {"entries": [(rel, STATE, basis)], "not_examined": n}.
    Raises _KbDeadline when `deadline` seconds of walking pass.
    """
    project = docs.parent
    rows, _errors = kb_exclusions(docs)
    by_digest, by_path, sizes = _kb_reach_index(docs)
    docs_key = _kb_path_key(docs)
    entries, counter = [], [0]
    start = _kb_clock()

    def add(r, state, basis=""):
        entries.append((r, state, basis))
        if state == "NOT_EXAMINED":
            counter[0] += 1

    def visit(e, erel):
        if deadline is not None and _kb_clock() - start > deadline:
            raise _KbDeadline()
        kind = kb_unreadable(e)
        try:
            # A link's target is never looked up (a dead network target would
            # stall orient): a link is matched by its NAME, as if it were a
            # directory, for the skip rule and dir-only exclusions.
            dir_like = kind == "link" or e.is_dir(follow_symlinks=False)
        except OSError:
            dir_like = False
        if dir_like and _kb_path_key(e.path) == docs_key:
            return
        if dir_like and sdlc_core.skip_dir(e.name):
            add(erel + "/", "SKIPPED", "built-in rule")
            return
        pat = kb_excluded(erel, dir_like, rows)
        if pat:
            add(erel + "/" if dir_like else erel, "EXCLUDED", pat)
            return
        if kind is None and dir_like:
            walk(e.path, erel)
            return
        if kind == "link":
            dir_like = False
        named = by_path.get(_kb_path_key(e.path))
        if kind:
            if named:
                add(erel, "INGESTED", "%s, by path — not read" % named[0])
            else:
                add(erel, "NOT_EXAMINED", {"link": "link — not followed",
                                           "cloud-only": "cloud-only — not read"}
                    .get(kind, "unreadable — not read"))
            return
        if not e.is_file(follow_symlinks=False):
            return
        digest = None
        try:
            if exact or e.stat(follow_symlinks=False).st_size in sizes:
                digest = kb_sha256_bytes(Path(e.path))
        except OSError:
            digest = None
        if digest and digest in by_digest:
            add(erel, "INGESTED", by_digest[digest])
        elif named:
            srel, osha = named
            if osha is None:
                add(erel, "INGESTED", "%s, by path — digest not kept" % srel)
            elif not exact:
                add(erel, "INGESTED", srel)       # examined; exactness is inventory's
            else:
                add(erel, "INGESTED_EARLIER", "%s, original changed since ingest" % srel)
        else:
            add(erel, "NOT_EXAMINED")

    def walk(d, drel):
        try:
            with os.scandir(d) as it:
                items = sorted(it, key=lambda x: x.name)
        except OSError:
            add((drel + "/") if drel else "./", "NOT_EXAMINED", "unreadable — not read")
            return
        for e in items:
            visit(e, (drel + "/" + e.name) if drel else e.name)

    rel = (rel or ".").replace("\\", "/").strip("/")
    if rel in ("", "."):
        walk(str(project), "")
    else:
        target = project / rel
        with os.scandir(str(target.parent)) as it:
            for e in it:
                if os.path.normcase(e.name) == os.path.normcase(target.name):
                    visit(e, rel)
    entries.sort(key=lambda t: t[0])
    return {"entries": entries, "not_examined": counter[0]}


def kb_cmd_inventory(root, docs, path):
    """FS3: one line per project file under `path`, in path order, with its
    state. No totals, no filter, no sort by state (r37). Writes nothing."""
    if not docs.is_dir():
        print("[ERROR] no docs root")
        return 1
    project = docs.parent
    rel = (path or "").replace("\\", "/").strip()
    parts = [x for x in rel.split("/") if x not in ("", ".")]
    if rel.startswith("/") or ntpath.isabs(rel) or ".." in parts:
        print("[ERROR] %s is outside the project root" % path)
        return 2
    # Lexical, never resolved: a link on the way is not followed (FS1). Each
    # component is matched to the name on disk, case-insensitively where the
    # filesystem is, so a differently-cased path is never an empty listing.
    real = []
    for name in parts:
        here = project.joinpath(*real)
        try:
            with os.scandir(str(here)) as it:
                found = [e.name for e in it
                         if os.path.normcase(e.name) == os.path.normcase(name)]
        except OSError:
            found = []
        if not found:
            print("[ERROR] %s does not exist" % path)
            return 2
        real.append(name if name in found else found[0])
        if len(real) < len(parts) and (
                os.path.islink(project.joinpath(*real))
                or getattr(os.path, "isjunction", lambda _p: False)(project.joinpath(*real))):
            print("[ERROR] %s lies behind %s, a link the inventory never follows"
                  % (path, "/".join(real)))
            return 2
    parts = real
    rows, _e = kb_exclusions(docs)
    for i, name in enumerate(parts):
        prefix = "/".join(parts[:i + 1])
        here = project.joinpath(*parts[:i + 1])
        if _kb_path_key(here) == _kb_path_key(docs):
            print("[ERROR] %s is the docs root: the corpus is not a project-file area" % path)
            return 2
        dir_like = os.path.islink(here) or os.path.isdir(here)
        if dir_like and sdlc_core.skip_dir(name):
            print("[ERROR] %s lies in %s/, which the validator never treats as "
                  "project files (built-in rule)" % (path, prefix))
            return 2
        if dir_like and kb_excluded(prefix, True, rows):
            print("[ERROR] %s lies in %s/, excluded by %s" % (path, prefix, KB_REGISTRY))
            return 2
    reach = kb_corpus_reach(docs, "/".join(parts) or ".", exact=True)
    for r, state, basis in reach["entries"]:
        print(("%-16s  %s  %s" % (state, r, basis)).rstrip())
    print("Nothing was written.")
    return 0


def kb_changed_originals(docs):
    """FS5: [(artifact rel, original_path, n citing claims)] for every live,
    non-superseded sidecar whose local original's bytes differ from the
    `original_sha256:` it recorded at ingest."""
    given = docs / "corpus" / "given"
    if not given.is_dir():
        return []
    metas = []
    superseded = set()
    for meta_p in sorted(given.glob("*.meta.md")):
        meta = sdlc_core.load_frontmatter(sdlc_core.read_text(meta_p).splitlines()) or {}
        metas.append((meta_p, meta))
        sup = kb_unquote(meta.get("supersedes"))
        if sup:
            superseded.add(sup)
    cites = {}
    for _slug, (_p, _t, rows) in kb_collect_topics(docs).items():
        for r in rows:
            for src in set(kb_claim_sources(r)):
                cites[src] = cites.get(src, 0) + 1
    out = []
    for meta_p, meta in metas:
        art = meta_p.name[:-len(".meta.md")]
        if kb_is_tombstone(meta) or art in superseded:
            continue
        op = kb_unquote(meta.get("original_path"))
        osha = (meta.get("original_sha256") or "").strip().lower()
        if not (op and osha):
            continue
        for c in _kb_original_candidates(op, docs):
            try:
                if c.is_symlink() or not c.is_file():
                    continue
                st = os.lstat(str(c))  # attributes without opening the file
                if (getattr(st, "st_file_attributes", 0) or 0) & _KB_CLOUD_ATTRS or \
                        (getattr(st, "st_flags", 0) or 0) & _KB_SF_DATALESS:
                    break
                if kb_sha256_bytes(c) != osha:
                    rel = "corpus/given/" + art
                    out.append((rel, op, cites.get(rel, 0)))
            except OSError:
                pass
            break
    return out


def kb_cmd_stale(root, docs, hybrid=False):
    """F-044: the consolidation view. The spine's output and exit semantics
    come first (--hybrid passed through untouched), then the `## claims`
    section -- superseded-cited docs, expired windows, superseded chains.
    Nothing is appended on a clean corpus, and the section NEVER moves the
    spine's rc: the time cycle reports, the spine rules."""
    rc = sdlc_core.cmd_stale(root, hybrid=hybrid)
    cycle = kb_time_cycle(docs)
    cited_w, chain_w, _dang = kb_time_cycle_warns(cycle)
    lines = list(cited_w)
    for topic_rel, rid, until, by in cycle["expired"]:
        lines.append("%s: %s expired %s (%s)"
                     % (topic_rel, rid, until,
                        ("cited by: " + ", ".join(by)) if by else "uncited"))
    lines += chain_w
    for rel, op, n in kb_changed_originals(docs):
        lines.append("%s: original %s changed since ingest -- %d claim(s) cite it; "
                     "ingest the new version as a successor (supersedes:)"
                     % (rel, op, n))
    if lines:
        print("")
        print("## claims")
        for ln in lines:
            print(ln)
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
    """Prose citation -> a verified span. The half `claim-id` never had.

    The path may be given as it appears in a claim's `source` cell
    (`corpus/given/x-ab12cd34.txt`): when it does not resolve from the current
    directory it is retried under the docs root, so the command works from
    anywhere in the project instead of only from inside `ai_docs/`. Reported
    from the field as an asymmetry with `graph`/`corpus`/`check`, which take
    `--root`; those scan a tree, this one takes a path, and the fix is to make
    the path resolve rather than to document where to stand."""
    p = Path(args.path)
    if not p.is_file():
        try:
            _, docs = _kb_root(args)
            if (docs / args.path).is_file():
                p = docs / args.path
        except sdlc_core.AmbiguousDocsRoot:
            pass
    if not p.is_file():
        print("[ERROR] no such file: %s" % args.path)
        print("        looked from the current directory and under the docs "
              "root; give the path as the claim's `source` cell carries it.")
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


def kb_cmd_export(args):
    root, docs = _kb_root(args)
    slugs = ([s.strip() for s in args.topics.split(",") if s.strip()]
             if args.topics else sorted(kb_collect_topics(docs)))
    if not slugs:
        print("[ERROR] no topics to export")
        return 2
    selected, artifacts, added, errors = kb_export_closure(docs, slugs)
    for e in errors:
        print("[ERROR] %s" % e)
    if errors:
        return 1
    out = Path(args.out)
    dropped = kb_bundle_write(docs, out, selected, artifacts, root.name)
    print("[ok] bundle written: %s" % out)
    print("     topics: %d, artifacts: %d" % (len(selected), len(artifacts)))
    if dropped:
        print("     not-yet-honored markers dropped: they describe this "
              "project's code")
    if kb_has_declarations(selected):
        print("     declarations stay in this project: not exported")
    if added:
        # never silent: a set that grew is a fact about the export, and the
        # alternative -- dropping the partner rows -- ships a broken tree.
        print("     +%d topic(s) added to keep conflict sets whole: %s"
              % (len(added), ", ".join(sorted(added))))
    return 0


def kb_cmd_import(args):
    _root, docs = _kb_root(args)
    bundle = Path(args.bundle)
    if not bundle.is_dir():
        print("[ERROR] no such bundle directory: %s" % bundle)
        return 2
    report = {}
    writes, skipped, dedup, errors = kb_import_plan(bundle, docs, report)
    for e in errors:
        print("[ERROR] %s" % e)
    if errors:
        print("[ERROR] nothing was written: an import that half-applies leaves a "
              "tree whose checks fail and whose owner cannot tell what landed.")
        return 1
    if args.dry_run:
        print("[ok] dry run: %d file(s) would be written" % len(writes))
    else:
        for _rel, data, dst in writes:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
        print("[ok] imported %d file(s) into %s" % (len(writes), docs))
    if report.get("converted"):
        # portability.md §0 point 4: the agent must be able to tell the user
        print("     %d ruling(s) arrive as IMPORTED: each rests on a renamed copy of "
              "its note (imported_<project>_...) and settles nothing until you "
              "ratify it (portability.md §4)" % report["converted"])
    for note in report.get("notes", []):
        print("[note] %s: a ruling of a skipped topic lands only as this foreign "
              "copy -- a row merged by hand cites it as IMPORTED" % note)
    if dedup:
        print("     %d claim(s) already present, by id — the same artifact cited "
              "at the same span mints the same id in any project" % len(dedup))
    for rel in skipped:
        print("[note] %s already exists: NOT overwritten. Run the placement pass "
              "(taxonomy.md) and merge by hand — an import never decides that."
              % rel)
    print("[note] re-run 'sdlc_check.py check' now: the import is additive, and "
          "an imported ruling stays IMPORTED until you ratify it with a note of "
          "your own.")
    return 0


def kb_cmd_orient(argv):
    """Forward `orient` to the spine untouched, then append the topic router.

    The recall reflex (SKILL.md section "Topic Recall") needs the graph in
    sight at session start -- by construction, not exhortation (F-039). The
    spine's orient is never re-implemented here: the raw argv goes through
    (the --help pattern below), and orient's flags are never mirrored into an
    overlay argparse -- the drift class the forward-by-default comment warns
    about. parse_known_args reads ONLY the two root flags the overlay itself
    needs to locate topics/, and ignores everything else.

    The append fails open: a broken graph read must never break orient itself.
    It is also bounded (F-075): the spine leaves ORIENT_APPEND_RESERVE of the
    client's hook cap free, and the append is cut to it -- the topic router
    first, since it is the part that grows -- so the whole output stays under
    the cap.
    """
    try:
        rc = sdlc_core.main(argv)
    except SystemExit as e:
        rc = e.code if isinstance(e.code, int) else 1
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            _kb_orient_append(argv)
    except (Exception, SystemExit):
        pass
    text = buf.getvalue()
    if text:
        print(_fit_orient_append(text, sdlc_core.ORIENT_APPEND_RESERVE), end="")
    return rc


def _fit_orient_append(text, budget):
    """`text` within `budget` characters: shrink the topic-router block first,
    then, if the rest alone is too wide, cut the whole append. Never raises."""
    if len(text) <= budget:
        return text
    lines = text.rstrip("\n").split("\n")
    try:
        i = lines.index("## Topic router")
        j = next((k for k in range(i + 1, len(lines)) if not lines[k].strip()), len(lines))
        block, others = lines[i + 1:j], lines[:i + 1] + lines[j:]
        room = budget - len("\n".join(others)) - 2
        if room > 0:
            fitted = sdlc_core.orient_fit(block, room, "topics/INDEX.md")
            out = "\n".join(lines[:i + 1] + fitted + lines[j:]) + "\n"
            if len(out) <= budget:
                return out
    except ValueError:
        pass
    return "\n".join(sdlc_core.orient_fit(lines, budget - 1, "the knowledge layer's files")) + "\n"


def _kb_orient_append(argv):
    """The lines kb_cmd_orient appends after the spine's orientation."""
    # Pre-bind so a throw INSIDE the router print (after root was validly
    # bound) does not erase it -- the recency block below must survive a
    # router failure with the bound root intact (closure R2 finding).
    root = name = None
    try:
        probe = argparse.ArgumentParser(add_help=False)
        probe.add_argument("--root")
        probe.add_argument("--docs-dir")
        known, _ = probe.parse_known_args(argv[1:])
        try:
            discovered, name = sdlc_core.resolve_docs_dir(known, known.root)
        except sdlc_core.AmbiguousDocsRoot:
            # Mirror the spine's degraded orient: fall back to the default
            # docs dir rather than losing the router on a half-migrated tree.
            discovered, name = None, sdlc_core.DEFAULT_DOCS_DIR
        root = (Path(known.root).resolve() if known.root
                else (discovered or sdlc_core.find_project_root()))
        topics = root / name / "topics"
        if (root / name).is_dir():
            print("\nProject memory: memory/INDEX.md; use recall QUERY for live metadata. "
                  "Read sources for authority and status.")
        index = topics / "INDEX.md"
        if index.is_file():
            lines = sdlc_core.read_text(index).splitlines()
            print("\n## Topic router")
            cap = 30
            for line in lines[:cap]:
                print(line)
            if len(lines) > cap:
                print("(+%d more lines -- read topics/INDEX.md)" % (len(lines) - cap))
        elif topics.is_dir():
            nodes = [p for p in topics.glob("*.md") if p.name != "INDEX.md"]
            if nodes:
                print("\n## Topic router")
                print("index absent (%d node files) -- regenerate: sdlc_check.py index"
                      % len(nodes))
        # no topics/ at all: the project has no graph; print nothing.
    except (Exception, SystemExit):
        # SystemExit included: the probe parser raises it on a dangling flag
        # value -- the spine already reported that usage error; the append must
        # never turn it into an escape. root/name keep whatever binding they
        # reached: pre-binding throws leave them None (recency skips), a throw
        # inside the router print leaves them valid (recency still runs).
        pass
    try:
        # Notes recency (F-040) -- its OWN try, genuinely independent of the
        # router: a router throw must not kill this line. It measures NOTES
        # recency, not full ledger freshness (an ingest feeding claims from
        # given/ leaves it unmoved). Date source: frontmatter `date:` first;
        # per-note mtime as fallback -- mtime LIES after clone/worktree (the
        # skill's own worktree hygiene makes that routine), which is why the
        # frontmatter date is primary.
        if root is None:
            return
        notes_dir = root / name / "corpus" / "notes"
        if notes_dir.is_dir():
            import datetime as _dt
            newest = None
            newest_mtime = False
            for p in notes_dir.glob("*.md"):
                stamp = None
                from_mtime = False
                try:
                    # Field datum 7 (on 1.11.0): the old 600-byte head window
                    # silently skipped the WHOLE probe when a real frontmatter
                    # (edge lists, basis lines) pushed the closing fence past
                    # it -- the file was already fully read, so the cap bought
                    # only failure. load_frontmatter is the authoritative
                    # reader (fence-bounded, so a column-0 date: in the body
                    # still cannot misdate the note); frontmatter_date covers
                    # quoted dates and tolerates a datetime suffix.
                    meta = sdlc_core.load_frontmatter(
                        sdlc_core.read_text(p).splitlines()) or {}
                    day = frontmatter_date(meta)
                    if day:
                        stamp = _dt.date.fromisoformat(day)
                except Exception:
                    pass
                if stamp is None:
                    try:
                        stamp = _dt.date.fromtimestamp(p.stat().st_mtime)
                        from_mtime = True
                    except Exception:
                        continue
                # Strict newer wins; on a tie a DATED stamp beats an mtime one,
                # so the disclosure below never fires beside a validated date
                # proving the same day.
                if (newest is None or stamp > newest
                        or (stamp == newest and newest_mtime
                            and not from_mtime)):
                    newest = stamp
                    newest_mtime = from_mtime
            if newest is None:
                print("\nno notes yet (corpus/notes)")
            else:
                days = (_dt.date.today() - newest).days
                # The basis is disclosed when mtime decided the winner: the
                # field-reported lie was a rewritten note reading "0 days old"
                # against SKILL.md's date-first promise -- degraded, and mute.
                basis = "; mtime -- date: not parsed" if newest_mtime else ""
                print("\nnewest note: %d days old (corpus/notes%s)"
                      % (max(days, 0), basis))
    except (Exception, SystemExit):
        # Fail-open: nothing in the recency append may break orient. (The
        # probe parser lives in the router try above; this guard covers the
        # date/mtime walk and the print itself.)
        pass
    try:
        # F-044: the time-cycle count line -- once per session at orient,
        # fail-open, SILENT when clean (noise is failure one). It runs the
        # shared collector, never a leaner walk: the counts must match what
        # `stale` lists, or the line under-counts its way to false calm.
        if root is not None:
            docs = root / name
            if (docs / "topics").is_dir() or (docs / "corpus").is_dir():
                cycle = kb_time_cycle(docs)
                n_docs = len({c[0] for c in cycle["cited"]})
                m_exp = len(cycle["expired"])
                k_chain = len(cycle["chain"])
                if n_docs or m_exp or k_chain:
                    print("\nkb time: %d docs cite superseded claims; "
                          "%d claims expired; %d derivations on superseded "
                          "sources -- run sdlc_check.py stale"
                          % (n_docs, m_exp, k_chain))
    except (Exception, SystemExit):
        pass
    try:
        # F-084: the corpus's reach, an upper bound of the project files never
        # examined (R5). Its own try: a failing walk prints nothing and takes
        # nothing else with it.
        if root is not None and (root / name / "corpus").is_dir():
            try:
                n = kb_corpus_reach(root / name, ".", exact=False,
                                    deadline=KB_REACH_DEADLINE)["not_examined"]
            except _KbDeadline:
                print("\nCorpus reach: not counted within 1s -- "
                      "sdlc_check.py inventory <path>")
            else:
                if n:
                    print("\nCorpus reach: <= %d project files not examined -- "
                          "exact: sdlc_check.py inventory <path>" % n)
    except (Exception, SystemExit):
        pass


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
shared project memory -- also available:
  recall QUERY                live cross-domain document metadata lookup
  graph                       topic-graph integrity: placement, edges, cycles
  corpus                      corpus integrity: digests, supersession, notes
  stale                       spine staleness PLUS `## claims`: superseded-cited
                              docs, expired windows, superseded chains
  claim-id <path> <locator>   compute a claim id (--fill to fill a whole table)
  anchor <path> <phrase>      resolve a phrase to a verified locator span
  export --out <dir>          bundle a subgraph WITH the bytes its claims cite
  import <dir>                merge a bundle in additively (never overwrites)
  adopt                       dry run: document guides resting on .sources/
                              snapshots, and what moving them into corpus/given/
                              involves (writes nothing; portability.md par.6)
  inventory <path>            the project files under <path> (. = all), each with
                              its state against the corpus: INGESTED,
                              INGESTED_EARLIER, EXCLUDED, NOT_EXAMINED (or
                              SKIPPED); no totals, writes nothing
  remind                      one-line per-turn reminder (UserPromptSubmit hook,
                              opt-in -- ENFORCEMENT par.4; constant, zero-read)

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
    # `orient` is special-cased BEFORE the overlay argparse, like --help: the
    # spine runs it on the raw argv, the overlay only appends the topic router.
    if argv and argv[0] == "orient":
        return kb_cmd_orient(argv)
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
    p = sub.add_parser("stale")
    p.add_argument("--root")
    p.add_argument("--docs-dir")
    p.add_argument("--hybrid", action="store_true")
    p = sub.add_parser("recall")
    p.add_argument("query")
    p.add_argument("--root")
    p.add_argument("--docs-dir")
    p = sub.add_parser("claim-id")
    p.add_argument("path")
    p.add_argument("locator", nargs="?")
    p.add_argument("--qty")
    p.add_argument("--fill", action="store_true")
    p = sub.add_parser("anchor")
    p.add_argument("path")
    p.add_argument("phrase")
    p.add_argument("--root")
    p.add_argument("--docs-dir")
    p.add_argument("--page", type=int)
    p.add_argument("--ignore-case", action="store_true")
    p.add_argument("--all", action="store_true")
    p = sub.add_parser("export")
    p.add_argument("--out", required=True)
    p.add_argument("--topics")
    p.add_argument("--root")
    p.add_argument("--docs-dir")
    p = sub.add_parser("import")
    p.add_argument("bundle")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--root")
    p.add_argument("--docs-dir")
    p = sub.add_parser("adopt")
    p.add_argument("--root")
    p.add_argument("--docs-dir")
    p = sub.add_parser("inventory")
    p.add_argument("path")
    p.add_argument("--root")
    p.add_argument("--docs-dir")
    args = ap.parse_args(argv)
    if args.cmd == "claim-id":
        return kb_cmd_claim_id(args)
    if args.cmd == "anchor":
        return kb_cmd_anchor(args)
    if args.cmd == "export":
        return kb_cmd_export(args)
    if args.cmd == "import":
        return kb_cmd_import(args)
    try:
        root, docs = _kb_root(args)
    except sdlc_core.AmbiguousDocsRoot as e:
        # same behaviour as the spine for non-exempt commands
        print("[ERROR] %s" % e)
        return 1
    if args.cmd == "index":
        return kb_cmd_index(root, docs)
    if args.cmd == "recall":
        return memory_recall(docs, args.query)
    if args.cmd == "stale":
        return kb_cmd_stale(root, docs, hybrid=args.hybrid)
    if args.cmd == "graph":
        return kb_cmd_graph(docs)
    if args.cmd == "corpus":
        return kb_cmd_corpus(docs, extra_errors=kb_credential_errors(root, docs))
    if args.cmd == "adopt":
        return kb_cmd_adopt(root, docs)
    if args.cmd == "inventory":
        return kb_cmd_inventory(root, docs, args.path)
    if args.cmd == "validate":
        return kb_cmd_validate(root, docs, strict=args.strict, hybrid=args.hybrid)
    return kb_cmd_check(root, docs, strict=args.strict, hybrid=args.hybrid)


if __name__ == "__main__":
    sys.exit(main())
