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
import ntpath
import posixpath
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
                   "review.md", "dispatch.md", "routing.md", "portability.md",
                   "ENFORCEMENT.md"),
    capabilities=(
        # spine
        "triage", "write_triggers", "workstream_registry", "vision_gate",
        "design_review_gate", "guide_router", "worktree_hygiene",
        # knowledge overlay
        # `knowledge_portability` (F-030) is deliberately NOT declared: the
        # capability vocabulary lives in the shared spine, and no shared test
        # guards on portability, so adding a label there would mean editing
        # sdlc_core.py in three distributions to buy nothing.
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
PROVENANCES = ("GIVEN", "ELICITED", "DERIVED", "RULING", "IMPORTED")
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
            # Resolved ONCE, for every provenance: the non-GIVEN classes read it
            # for their required field, and GIVEN reads it to notice that the
            # artifact declares a weaker chain than the row claims.
            meta, meta_where = (None, "")
            if "#" in first:
                meta, meta_where = _declaring_frontmatter(first.rsplit("#", 1)[0])
            if prov not in PROVENANCES:
                errors.append("%s: prov %r not in %s" % (where, prov, "/".join(PROVENANCES)))
            elif prov in ("DERIVED", "RULING", "ELICITED", "IMPORTED"):
                if meta is None:
                    pass  # unresolvable source already reported
                elif prov == "DERIVED" and not meta.get("derived_from"):
                    errors.append("%s: DERIVED claim's source (%s) carries no "
                                  "'derived_from:' — model knowledge disguised as "
                                  "a source" % (where, meta_where))
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
                if declared and declared.upper() != "GIVEN":
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
                        errors.append(
                            "%s: id %s collides with the row at %s — two "
                            "DIFFERENT rows cite the same span with the same "
                            "qty, and the id function cannot separate them (it "
                            "hashes path#locator#qty and excludes the text on "
                            "purpose). Widen one locator to the span that "
                            "actually carries its assertion, or merge the two "
                            "rows — do not edit the qty to break the tie"
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
                if kind == "SUPERSEDED" and orow["prov"] == "IMPORTED":
                    # F-030, owner ruling 2026-08-03: knowledge crosses a project
                    # boundary, authority does not. An IMPORTED row carries another
                    # owner's decision; letting it supersede a local row would make
                    # that decision binding here without anyone here granting it.
                    # Re-ratify first: write your own ruling note with your own
                    # basis and flip the row to RULING.
                    errors.append("%s: SUPERSEDED by %s, which is IMPORTED — a "
                                  "foreign decision cannot settle a local row. "
                                  "Re-ratify it (own note, own 'basis:', prov "
                                  "RULING) or resolve this some other way"
                                  % (where, t))
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
            sup = (meta.get("supersedes") or "").strip()
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
            op = (meta.get("original_path") or "").strip()
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
                        "an import this dangles legitimately"
                        % (rel, op, ", ".join(tried)))
            sup = (meta.get("supersedes") or "").strip()
            if sup:
                superseded.add(sup)
                if not (given / sup).is_file():
                    warnings.append("%s: supersedes %r which is not in given/"
                                    % (rel, sup))
            kb_check_coverage(rel, orig,
                              (meta.get("extracted_through") or "").strip(),
                              _kb_cited_for(cited, orig.name), errors, warnings)
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


def kb_sha256_bytes(path):
    """RAW-byte digest for binaries. The spine's sha256_file normalizes CRLF->LF
    (right for text snapshots, wrong for binaries, where a hostile 0D0A/0A pair
    would collide)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


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
    for slug, (_p, _t, rows) in all_topics.items():
        for r in rows:
            if r["id"]:
                owner_of[r["id"]] = slug
    added = []
    pending = list(selected)
    while pending:
        slug = pending.pop()
        for r in selected[slug][2]:
            m = re.match(r"^(CONTESTED|SUPERSEDED) ([0-9a-f, ]+)$", r["state"].strip())
            if not m:
                continue
            for ref in [x.strip() for x in m.group(2).split(",") if x.strip()]:
                other = owner_of.get(ref)
                if other is None:
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
            for rel in kb_claim_sources(r):
                for cand in (rel, rel + ".meta.md",
                             rel[:-len(Path(rel).suffix)] + ".txt" if Path(rel).suffix else rel):
                    if cand in seen:
                        continue
                    if (docs / cand).is_file():
                        seen.add(cand)
                        artifacts.append(cand)
    return selected, artifacts, added, errors


def kb_bundle_write(docs, out, selected, artifacts, project):
    """Write the bundle. Mirrors the docs-root layout; no path is rewritten."""
    out.mkdir(parents=True, exist_ok=True)
    (out / "topics").mkdir(exist_ok=True)
    for slug, (p, text, _rows) in sorted(selected.items()):
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


def kb_import_plan(bundle, docs):
    """(writes, skipped_topics, dedup, errors) -- computed BEFORE anything is
    written, because an import that half-applies leaves a tree whose checks fail
    and whose owner cannot tell what landed."""
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

    for p in sorted(bundle.rglob("*")):
        if not p.is_file() or p.name == BUNDLE_MANIFEST:
            continue
        rel = p.relative_to(bundle).as_posix()
        dst = sdlc_core.confine_under(docs, rel)
        if dst is None:
            errors.append("bundle entry %r escapes the docs root — refusing the "
                          "whole import, not just this file" % rel)
            continue
        if dst.is_file() and not rel.startswith("topics/"):
            if kb_sha256_bytes(dst) != kb_sha256_bytes(p):
                errors.append("%s exists with different bytes (target %s… vs "
                              "bundle %s…): content-addressed names must mean "
                              "equal content" % (rel, kb_sha256_bytes(dst)[:8],
                                                 kb_sha256_bytes(p)[:8]))
            continue
        if rel.startswith("topics/") and dst.is_file():
            skipped.append(rel)
            continue
        writes.append((rel, p, dst))

    for rel, p, _dst in writes:
        if not rel.startswith("topics/"):
            continue
        rows, _ = kb_parse_claims(sdlc_core.read_text(p))
        for r in rows:
            if r["id"] and r["id"] in known_ids:
                dedup.append(r["id"])
    return writes, skipped, dedup, errors


# ------------------------------------------------------------------ commands

INTERCEPTED = {"index", "validate", "check", "graph", "corpus", "claim-id",
               "anchor", "export", "import"}


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
    kb_bundle_write(docs, out, selected, artifacts, root.name)
    print("[ok] bundle written: %s" % out)
    print("     topics: %d, artifacts: %d" % (len(selected), len(artifacts)))
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
    writes, skipped, dedup, errors = kb_import_plan(bundle, docs)
    for e in errors:
        print("[ERROR] %s" % e)
    if errors:
        print("[ERROR] nothing was written: an import that half-applies leaves a "
              "tree whose checks fail and whose owner cannot tell what landed.")
        return 1
    if args.dry_run:
        print("[ok] dry run: %d file(s) would be written" % len(writes))
    else:
        for _rel, src, dst in writes:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(src.read_bytes())
        print("[ok] imported %d file(s) into %s" % (len(writes), docs))
    if dedup:
        print("     %d claim(s) already present, by id — the same artifact cited "
              "at the same span mints the same id in any project" % len(dedup))
    for rel in skipped:
        print("[note] %s already exists: NOT overwritten. Run the placement pass "
              "(taxonomy.md) and merge by hand — an import never decides that."
              % rel)
    print("[note] re-run 'sdlc_check.py check' now: the import is additive, and "
          "an imported RULING stays IMPORTED until you re-ratify it.")
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
    """
    try:
        rc = sdlc_core.main(argv)
    except SystemExit as e:
        rc = e.code if isinstance(e.code, int) else 1
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
        # value ("orient --root" at end of argv) -- the spine already reported
        # that usage error; the append must never turn it into an escape.
        pass
    return rc


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
  export --out <dir>          bundle a subgraph WITH the bytes its claims cite
  import <dir>                merge a bundle in additively (never overwrites)

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
    if args.cmd == "graph":
        return kb_cmd_graph(docs)
    if args.cmd == "corpus":
        return kb_cmd_corpus(docs)
    if args.cmd == "validate":
        return kb_cmd_validate(root, docs, strict=args.strict, hybrid=args.hybrid)
    return kb_cmd_check(root, docs, strict=args.strict, hybrid=args.hybrid)


if __name__ == "__main__":
    sys.exit(main())
