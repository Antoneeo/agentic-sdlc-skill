"""F-083 replay harness: export a topic holding a RULING, import it into an empty
project, and assert what portability.md §4 promises (AC1, AC2, AC8).

    python probe.py <kb scripts dir> <source project root> <topic slug>

Example (the reproduction that opened the unit):
    python probe.py distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts \
        "C:/workspace/corso AI/demo/TH-01" sonda-temperatura

Two parts. BASELINE claims are about the validator the design rests on and hold on
the code before the fix too (probe A: editing the note in place re-points its line
locator; probe R: the renamed-note end state, built by hand, is CLEAN). AFTER-FIX
claims run the real export/import and fail on the code before the fix.
Exit 0 = every assertion holds. Writes only into a temporary directory.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

KB, SRC, TOPIC = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(KB))
import knowledge as kn  # noqa: E402

failed = []


def run(*args):
    p = subprocess.run([sys.executable, str(KB / "sdlc_check.py")] + list(args),
                       capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout + p.stderr


def claim(name, ok, detail=""):
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, (" -- " + detail) if detail else ""))
    if not ok:
        failed.append(name)


def rows_of(docs):
    return {r["id"]: r for _s, (_p, _t, rows) in kn.kb_collect_topics(docs).items()
            for r in rows if r["id"]}


def check(root):
    run("index", "--root", str(root))
    rc, out = run("check", "--root", str(root))
    return rc == 0, out.strip()[-400:]


def first_path(row):
    return row["source"].split(";")[0].strip().rsplit("#", 1)[0]


def set_cells(text, rid, **cells):
    """Rewrite named cells of the row whose id is rid (columns as CLAIM_COLUMNS)."""
    out = []
    for ln in text.splitlines():
        if ln.startswith("| %s " % rid):
            parts = ln.split("|")
            for k, v in cells.items():
                parts[1 + kn.CLAIM_COLUMNS.index(k)] = " %s " % v
            ln = "|".join(parts)
        out.append(ln)
    return "\n".join(out) + "\n"


def contested(state):
    m = re.match(r"^CONTESTED ([0-9a-f, ]+)$", state)
    return set(x.strip() for x in m.group(1).split(",")) if m else set()


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    src_rows = rows_of(SRC / "ai_docs")
    rulings = [i for i, r in src_rows.items() if r["prov"] == "RULING"]
    claim("the source topic holds a RULING (precondition)", bool(rulings))
    members = {r: [i for i, s in src_rows.items()
                   if s["state"].startswith("SUPERSEDED") and r in s["state"]]
               for r in rulings}
    bundle = tmp / "bundle"
    rc, out = run("export", "--root", str(SRC), "--out", str(bundle), "--topics", TOPIC)
    claim("export succeeds", rc == 0, out.strip()[-200:])

    # ---------------- BASELINE (true before and after the fix) ----------------
    rid = rulings[0]
    note = first_path(src_rows[rid])
    loc = src_rows[rid]["source"].split(";")[0].strip().rsplit("#", 1)[1]
    n = int(loc[1:].split("-")[0])
    lines = (SRC / "ai_docs" / note).read_text(encoding="utf-8").splitlines()
    shifted = lines[:1] + ["imported_from: x"] + lines[1:]
    claim("probe A: one frontmatter line in the note re-points %s at other text" % loc,
          shifted[n - 1] != lines[n - 1],
          "%r -> %r" % (lines[n - 1][:40], shifted[n - 1][:40]))

    # probe R: the designed end state, built by hand on a plain copy of the bundle
    hand = tmp / "hand"
    (hand / "ai_docs").mkdir(parents=True)
    for p in bundle.rglob("*"):
        if p.is_file() and p.name != "MANIFEST.md":
            d = hand / "ai_docs" / p.relative_to(bundle)
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, d)
    hd = hand / "ai_docs"
    new_note = "corpus/notes/imported_%s_%s" % (re.sub(r"[^a-z0-9]", "-", SRC.name.lower()),
                                                Path(note).name)
    body = (hd / note).read_text(encoding="utf-8").splitlines()
    body = body[:1] + ["imported_from: %s — %s" % (SRC.name, note)] + [
        "origin: imported" if b.strip() == "origin: ruling" else b for b in body[1:]]
    (hd / new_note).write_text("\n".join(body) + "\n", encoding="utf-8")
    (hd / note).unlink()
    new_loc = "L%d-%d" % tuple(int(x) + 1 for x in loc[1:].split("-"))
    new_id = kn.kb_claim_id(new_note, new_loc, "")
    tp = next(p for p in (hd / "topics").glob("*.md") if rid in p.read_text(encoding="utf-8"))
    text = tp.read_text(encoding="utf-8")
    group = members[rid]
    for m in group:
        text = set_cells(text, m, state="CONTESTED " + ", ".join(
            [x for x in group if x != m] + [new_id]))
    text = set_cells(text, rid, source="%s#%s" % (new_note, new_loc), prov="IMPORTED",
                     state="CONTESTED " + ", ".join(group) if group else "OK")
    text = text.replace("| %s |" % rid, "| %s |" % new_id)
    tp.write_text(text, encoding="utf-8")
    ok, out = check(hand)
    claim("probe R: renamed note + IMPORTED + reopened set, by hand, is CLEAN", ok, out)

    # ---------------- AFTER THE FIX ----------------
    tgt = tmp / "target"
    (tgt / "ai_docs" / "topics").mkdir(parents=True)
    rc, out = run("import", str(bundle), "--root", str(tgt))
    claim("import succeeds", rc == 0, out.strip()[-300:])
    claim("import reports the foreign ruling(s)", "arrive as IMPORTED" in out)
    docs = tgt / "ai_docs"
    got = rows_of(docs)
    imp = [i for i, r in got.items() if r["prov"] == "IMPORTED"]
    claim("AC1 no RULING row arrives as RULING",
          not [i for i, r in got.items() if r["prov"] == "RULING"])
    claim("AC1 %d ruling(s) arrive as IMPORTED" % len(rulings), len(imp) == len(rulings),
          "%d IMPORTED" % len(imp))
    for i in imp:
        meta, where = kn._note_frontmatter(docs, first_path(got[i]))
        claim("AC1 %s rests on a renamed note naming its origin" % i,
              first_path(got[i]).startswith("corpus/notes/imported_")
              and bool(meta and meta.get("imported_from"))
              and (meta or {}).get("origin") == "imported", where)
    claim("AC1 the note under its original name is not written",
          not (docs / note).exists())

    def addressed(docs_root, cell):
        path, l = cell.rsplit("#", 1)
        a, b = (int(x) for x in l[1:].split("-"))
        ls = (docs_root / path).read_text(encoding="utf-8").splitlines()
        return [x for x in ls[a - 1:b] if not x.startswith(("imported_from:", "origin:"))]
    for i in imp:
        orig = next((r for r in rulings if src_rows[r]["claim"] == got[i]["claim"]), None)
        if orig:
            old_cell = src_rows[orig]["source"].split(";")[0].strip()
            new_cell = got[i]["source"].split(";")[0].strip()
            claim("AC1 %s cites the same text in the copy" % i,
                  addressed(SRC / "ai_docs", old_cell) == addressed(docs, new_cell),
                  "%s -> %s" % (old_cell, new_cell))
    for i in imp:
        orig = next((r for r in rulings if src_rows[r]["claim"] == got[i]["claim"]), None)
        group = set(members.get(orig, []))
        claim("AC1 %s is CONTESTED with every row it had superseded" % i,
              contested(got[i]["state"]) >= group, got[i]["state"])
        for m in group:
            claim("AC1 %s is CONTESTED with %s and the rest of its set" % (m, i),
                  contested(got[m]["state"]) == (group - {m}) | {i}, got[m]["state"])
    ok, out = check(tgt)
    claim("AC1 check CLEAN after the import", ok, out)

    if imp and ok:
        i = imp[0]
        tp = next(p for p in (docs / "topics").glob("*.md")
                  if i in p.read_text(encoding="utf-8"))
        text = tp.read_text(encoding="utf-8")
        flip = tmp / "flip"
        shutil.copytree(tgt, flip)
        (flip / "ai_docs" / "topics" / tp.name).write_text(
            set_cells(text, i, prov="RULING"), encoding="utf-8")
        rc, out = run("check", "--root", str(flip))
        claim("AC2 relabelling IMPORTED->RULING is refused (foreign note)",
              rc != 0 and "imported_from" in out, out.strip()[-300:])

        own = "corpus/notes/RULING_ratifica_probe.md"
        (docs / own).write_text("---\norigin: ruling\nbasis: probe owner checked it "
                                "locally\ndate: 2026-10-26\n---\nRatified here.\n",
                                encoding="utf-8")
        rat = kn.kb_claim_id(own, "L6-6", "")
        todo, seen = [i], set()
        while todo:                       # connected sets, transitively
            x = todo.pop()
            if x not in seen:
                seen.add(x)
                todo.extend(contested(got[x]["state"]))
        for x in seen:
            text = set_cells(text, x, state="SUPERSEDED " + rat)
        text = text.rstrip("\n") + "\n| %s | %s | - | - | - | %s#L6-6 | RULING | OK |\n" % (
            rat, got[i]["claim"], own)
        tp.write_text(text, encoding="utf-8")
        ok2, out = check(tgt)
        claim("AC2 ratification (own note, own basis:, RULING row) is CLEAN", ok2, out)

print("\n%d assertion(s) failed" % len(failed) if failed else "\nall assertions hold")
sys.exit(1 if failed else 0)
