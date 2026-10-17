"""Probe for F-072 (kb site): the data shapes a site generator must handle, measured
with the validator's own parsers so the numbers mean what the validator means.

Usage:  python probe.py --root <project root whose docs root holds topics/ and corpus/>
Prints counts only - no claim text, no names - so its output can be quoted in a
public repository whatever KB it runs on.
"""
import argparse
import collections
import posixpath
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[3] / "skills" / "agentic-sdlc-skill" / "scripts"))
import knowledge  # noqa: E402
import sdlc_core  # noqa: E402

HEX12 = re.compile(r"`([0-9a-f]{12})`")


def docs_root(root):
    """The docs root; a project without topics/ is valid (the site generates without them)."""
    for cand in (root / "ai_docs", root / "mkt_docs", root / "docs" / "ai_docs"):
        if cand.is_dir():
            return cand
    if (root / "topics").is_dir() or (root / "solutions").is_dir():
        return root
    sys.exit("no ai_docs/ under %s" % root)


def frontmatter(path):
    return sdlc_core.load_frontmatter(sdlc_core.read_text(path).splitlines()) or {}


RED = False


def main():
    global RED
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--red", action="store_true",
                    help="read line ranges with splitlines(): must FAIL on a KB whose extractions carry form-feeds")
    args = ap.parse_args()
    RED = args.red
    docs = docs_root(Path(args.root).resolve())
    out = collections.OrderedDict()

    # topics and their display name
    all_nodes = knowledge.kb_load_topics(docs)
    tomb = {s for s, n in all_nodes.items()
            if str(n["meta"].get("status") or "").strip() == "SUPERSEDED"}
    nodes = {s: n for s, n in all_nodes.items() if s not in tomb}
    out["topic_tombstones"] = len(tomb)
    out["topics"] = len(nodes)
    out["topics_root"] = sum(1 for n in nodes.values() if not knowledge._as_list(n["meta"].get("parents")))
    areas = {s for s, n in nodes.items() if not knowledge._as_list(n["meta"].get("parents"))}
    out["topics_first_parent_not_an_area"] = sum(
        1 for n in nodes.values()
        if knowledge._as_list(n["meta"].get("parents"))
        and knowledge._as_list(n["meta"].get("parents"))[0] not in areas)
    h1 = 0
    for n in nodes.values():
        body = sdlc_core.read_text(docs / n["file"]).split("\n")
        if any(ln.startswith("# ") for ln in body):
            h1 += 1
    out["topics_with_h1"] = h1
    out["topics_with_related"] = sum(1 for n in nodes.values() if n["meta"].get("related"))
    out["topics_with_owns"] = sum(1 for n in nodes.values() if n["meta"].get("owns"))
    out["topics_with_gaps"] = sum(1 for n in nodes.values() if n["meta"].get("gaps"))

    # claims
    rows = []
    out["claim_parse_errors"] = 0
    for slug, n in nodes.items():
        r, errs = knowledge.kb_parse_claims(sdlc_core.read_text(docs / n["file"]))
        out["claim_parse_errors"] += len(errs)
        for row in r:
            row["_topic"] = slug
        rows += r
    by_id = {r["id"]: r for r in rows}
    out["claims"] = len(rows)
    for p in knowledge.PROVENANCES:
        out["prov_" + p] = sum(1 for r in rows if r["prov"] == p)
    kind = lambda r: r["state"].split()[0]  # noqa: E731
    for s in ("OK", "SUPERSEDED", "CONTESTED"):
        out["state_" + s] = sum(1 for r in rows if kind(r) == s)
    out["claims_with_about"] = sum(1 for r in rows if r["about"] not in ("", "-"))
    out["claims_multi_source"] = sum(1 for r in rows if len(knowledge.kb_claim_sources(r)) > 1)

    # supersession: does the named successor need following further?
    succ_ok = succ_sup = succ_con = multi = 0
    longest = 0
    for r in rows:
        if kind(r) != "SUPERSEDED":
            continue
        targets = [t.strip() for t in r["state"].split(None, 1)[1].split(",") if t.strip()]
        multi += len(targets) > 1
        for t in targets:
            k = kind(by_id[t]) if t in by_id else "MISSING"
            succ_ok += k == "OK"
            succ_sup += k == "SUPERSEDED"
            succ_con += k == "CONTESTED"
        depth, cur, seen = 0, r, set()
        while kind(cur) == "SUPERSEDED" and cur["id"] not in seen:
            seen.add(cur["id"])
            nxt = cur["state"].split(None, 1)[1].split(",")[0].strip()
            if nxt not in by_id:
                break
            cur, depth = by_id[nxt], depth + 1
        longest = max(longest, depth)
    out.update(superseded_successor_ok=succ_ok, superseded_successor_superseded=succ_sup,
               superseded_successor_contested=succ_con, superseded_multi_successor=multi,
               superseded_longest_chain=longest)
    contested_sets = [len(r["state"].split(None, 1)[1].split(",")) for r in rows if kind(r) == "CONTESTED"]
    out["contested_naming_more_than_one"] = sum(1 for n in contested_sets if n > 1)

    # locator forms
    forms = collections.Counter()
    for r in rows:
        for src in r["source"].split(";"):
            src = src.strip()
            if "#" not in src:
                forms["no_locator"] += 1
                continue
            loc = src.rsplit("#", 1)[1]
            forms["page_offset" if knowledge.LOC_PAGE_RE.match(loc) else
                  "line_range" if knowledge.LOC_LINE_RE.match(loc) else
                  "sheet_cell" if knowledge.LOC_CELL_RE.match(loc) else "other"] += 1
    for k, v in sorted(forms.items()):
        out["locator_" + k] = v

    # DERIVED: walk each chain to its ground, as SKILL.md's anti-echo rule does
    note_meta = {}

    def ground(path, seen):
        """'given' | 'elicited' | 'ruling' | 'imported' | 'unresolved' for one cited path."""
        if path in seen:
            return {"unresolved"}
        seen = seen | {path}
        if path.startswith("corpus/given/"):
            return {"given"}
        p = docs / path
        if not p.is_file():
            return {"unresolved"}
        meta = note_meta.setdefault(path, frontmatter(p))
        origin = str(meta.get("origin") or "").strip().lower()
        if origin in ("elicited", "ruling", "imported"):
            return {origin}
        df = knowledge._kb_df_entries(meta.get("derived_from"))
        if not df:
            return {"ruling"} if meta.get("basis") else {"unresolved"}
        res = set()
        for d in df:
            rel = site_resolve(str(d).strip())
            res |= ground(rel, seen) if rel else {"unresolved"}
        return res

    docs_abs = docs.resolve()

    def site_resolve(entry):
        """The site's rule (spec, Fact panel): the validator's ladder, but a path is
        followed only if it ends inside the docs root; one that leaves it is untraceable."""
        rel = resolve_entry(entry)
        if rel is None:
            return None
        target = (docs / rel).resolve()
        try:
            return target.relative_to(docs_abs).as_posix()
        except ValueError:
            return None

    def resolve_entry(entry):
        """The resolution ladder kb_time_cycle uses (knowledge.py, _resolve)."""
        entry = posixpath.normpath(entry)
        if "/" in entry:
            return entry if (docs / entry).is_file() else None
        for base in ("corpus/notes/", "corpus/given/"):
            if (docs / (base + entry)).is_file():
                return base + entry
        return None

    grounds = collections.Counter()
    for r in rows:
        if r["prov"] != "DERIVED":
            continue
        g = set()
        for s in knowledge.kb_claim_sources(r):
            g |= ground(s, frozenset())
        grounds["derived_reaches_elicited" if "elicited" in g else
                "derived_untraceable" if "unresolved" in g else
                "derived_reaches_imported" if "imported" in g else
                "derived_documents_or_decisions_only"] += 1
    out.update(sorted(grounds.items()))

    # corpus: one source document per sidecar; stored extractions are counted apart
    given = docs / "corpus" / "given"
    sidecars = sorted(given.glob("*.meta.md")) if given.is_dir() else []
    files = [p for p in given.iterdir() if not p.name.endswith(".meta.md")] if given.is_dir() else []
    described = {p.name[: -len(".meta.md")] for p in sidecars}
    out["source_documents"] = len(sidecars)
    out["source_documents_superseding_another"] = sum(1 for p in sidecars if frontmatter(p).get("supersedes"))
    out["stored_extractions_without_own_sidecar"] = sum(1 for p in files if p.name not in described)

    # passages: read every locator the way kb_check_locator does, with a per-file cache;
    # --red reads lines with splitlines() instead, which must disagree on form-feed files
    cache = {}

    def text_of(path):
        if path not in cache:
            cache[path] = sdlc_core.read_text(path)
        return cache[path]

    def passage(target, loc, red):
        m = knowledge.LOC_PAGE_RE.match(loc)
        if m:
            page, a, b = map(int, m.groups())
            ext = target if target.suffix == ".txt" else target.with_suffix(".txt")
            return text_of(ext).split("\f")[page - 1][a:b]
        m = knowledge.LOC_LINE_RE.match(loc)
        if m:
            a, b = map(int, m.groups())
            t = text_of(target)
            lines = t.splitlines() if red else t.split("\n")
            return "\n".join(lines[a - 1:b])
        return None

    t0 = time.time()
    agree = disagree = 0
    for r in rows:
        for src in r["source"].split(";"):
            src = src.strip()
            if "#" not in src:
                continue
            rel, loc = src.rsplit("#", 1)
            target = docs / rel
            errs = []
            knowledge.kb_check_locator(target, loc, "probe", errs)
            if errs:
                disagree += 1
                continue
            got = passage(target, loc, RED)
            if got is None:
                continue
            m = knowledge.LOC_LINE_RE.match(loc)
            if m:
                a, b = map(int, m.groups())
                ref = "\n".join(text_of(target).split("\n")[a - 1:b])
                ok = got == ref
            else:
                a, b = map(int, knowledge.LOC_PAGE_RE.match(loc).groups()[1:])
                ok = len(got) == b - a
            agree += ok
            disagree += not ok
    out["passages_agreeing_with_validator"] = agree
    out["passages_disagreeing"] = disagree
    out["passages_seconds_with_cache"] = round(time.time() - t0, 1)
    notes = docs / "corpus" / "notes"
    out["notes"] = len(list(notes.glob("*.md"))) if notes.is_dir() else 0

    # claim ids cited in backticks across the docs root
    hits = miss = 0
    for p in docs.rglob("*.md"):
        if "corpus" in p.parts and "given" in p.parts:
            continue
        for m in HEX12.finditer(sdlc_core.read_text(p)):
            if m.group(1) in by_id:
                hits += 1
            else:
                miss += 1
    out["backtick_ids_resolving"] = hits
    out["backtick_ids_not_resolving"] = miss
    out["markdown_documents"] = sum(1 for p in docs.rglob("*.md")
                                    if not ("corpus" in p.parts and "given" in p.parts))
    # the working-documents tree: the shared memory catalog's set (R17) plus the resume notes
    catalog = knowledge.memory_records(docs)
    project = docs.parent
    resume = sdlc_core.list_workstreams(project) if docs.name in ("ai_docs", "mkt_docs") else []
    out["working_documents"] = len(catalog) + len(resume)
    df_abs = [e for p in (docs / "corpus" / "notes").glob("*.md") for e in
              knowledge._kb_df_entries(frontmatter(p).get("derived_from"))
              if re.match(r"^([A-Za-z]:)?[/\\]", str(e))] if (docs / "corpus" / "notes").is_dir() else []
    out["derived_from_absolute_entries"] = len(df_abs)
    out["derived_from_absolute_inside_docs"] = sum(1 for e in df_abs if site_resolve(str(e).strip()))
    # frontmatter values spanning several lines (load_frontmatter drops them)
    multi = 0
    for p in docs.rglob("*.md"):
        if "corpus" in p.parts and "given" in p.parts:
            continue
        ls = sdlc_core.read_text(p).split("\n")
        if not ls or ls[0].strip() != "---":
            continue
        try:
            end = next(i for i in range(1, len(ls)) if ls[i].strip() == "---")
        except StopIteration:
            continue
        if any(l.startswith((" ", "\t", "- ")) for l in ls[1:end]):
            multi += 1
    out["documents_with_multiline_frontmatter"] = multi
    # analyses and open workstreams, as the validator lists them
    analyses = sdlc_core.list_analyses(docs.parent if docs.name == "ai_docs" else docs)
    out["analyses"] = len(analyses)
    out["analyses_declaring_updated"] = sum(1 for a in analyses if (a[1] if isinstance(a, tuple) else {}).get("updated"))
    ws = sdlc_core.list_workstreams(docs.parent if docs.name in ("ai_docs", "mkt_docs") else docs)
    out["open_workstreams"] = len(ws)
    out["open_workstreams_declaring_updated"] = sum(1 for _, m in ws if str(m.get("updated") or "").strip())
    groups = {"BLOCKED", "PLANNED", "TODO", "IN_PROGRESS", "PROGRESS", "PAUSED", "ON_HOLD",
              "COMPLETED", "DONE", "CANCELLED", "ARCHIVED"}
    out["open_workstreams_status_in_groups"] = sum(
        1 for _, m in ws if str(m.get("status") or "").strip().upper() in groups)
    out["analyses_status_in_groups"] = sum(
        1 for a in analyses if str(a[1].get("status") or "").strip().upper() in groups)

    # behaviours of existing code the specification rests on, executed, not read
    failures = []
    sample = next(iter(sorted((docs / "corpus" / "notes").glob("*.md"))), None) \
        if (docs / "corpus" / "notes").is_dir() else None
    if sample is not None:
        followed = resolve_entry(sample.resolve().as_posix()) is not None
        out["validator_ladder_follows_absolute_path"] = followed
        if not followed:
            failures.append("the ladder no longer follows absolute paths: the spec's stated difference is moot")
    fm = sdlc_core.load_frontmatter(["---", "title: x", "derived_from:", "  - a.md", "  - b.md", "---"]) or {}
    dropped = fm.get("derived_from") in (None, "", [])
    out["load_frontmatter_drops_multiline_values"] = dropped
    if not dropped:
        failures.append("load_frontmatter now parses multi-line values: the spec's raw-block rule is moot")

    width = max(len(k) for k in out)
    for k, v in out.items():
        print("%-*s %s" % (width, k, v))

    # assertions the specification rests on; exit 1 when any fails
    if out["passages_disagreeing"]:
        failures.append("%d passages read differently from kb_check_locator" % out["passages_disagreeing"])
    if out["claim_parse_errors"]:
        failures.append("%d claim rows do not parse" % out["claim_parse_errors"])
    derived = sum(out.get(k, 0) for k in ("derived_reaches_elicited", "derived_untraceable",
                                          "derived_reaches_imported", "derived_documents_or_decisions_only"))
    if derived != out["prov_DERIVED"]:
        failures.append("derived grounds %d != DERIVED rows %d" % (derived, out["prov_DERIVED"]))
    for f in failures:
        print("FAIL", f)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
