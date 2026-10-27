#!/usr/bin/env python3
"""F-084 probes, two groups.

B* -- BASELINE facts the design rests on: green on today's code. Those marked
      FLIPS are the defects the unit removes: under --expect-outcomes their
      expectation is inverted, so they guard the fix instead of the defect.
O* -- OUTCOMES the unit exists to make true (R1's three tests and the rules that
      carry them): RED on today's code, green once F-084 is built.

`--negate` flips every expectation, so each probe is shown able to fail.

    python probe.py [--kb <kb scripts dir>] [--negate] [--expect-outcomes]

Exit code: 0 when every B probe is green; the O probes are reported, and their
red is the point before implementation (use --expect-outcomes after it).
"""
import argparse
import contextlib
import hashlib
import io
import os
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve()
DEFAULT_KB = (HERE.parents[3] / "distributions" / "kb-agentic-skill" / "skills"
              / "kb-agentic-skill" / "scripts")


def run(kc, argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        try:
            rc = kc.main(list(argv))
        except SystemExit as e:
            rc = e.code if isinstance(e.code, int) else 1
    return rc, out.getvalue()


def tree(tmp, given, claims_rows, notes=None):
    """project root `tmp`, docs root `tmp/ai_docs`."""
    docs = Path(tmp) / "ai_docs"
    (docs / "topics").mkdir(parents=True)
    for rel, data in given.items():
        p = docs / "corpus" / "given" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
    for rel, text in (notes or {}).items():
        p = docs / "corpus" / "notes" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    head = ("---\ntopic: t\ndescription: d\nparents: []\nstatus: CURRENT\n---\n\n"
            "## Claims\n\n| id | claim | valid | qty | about | source | prov | state |\n"
            "|---|---|---|---|---|---|---|---|\n")
    (docs / "topics" / "t.md").write_text(
        head + "\n".join("| %s |" % " | ".join(r) for r in claims_rows) + "\n",
        encoding="utf-8")
    return docs


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", default=str(DEFAULT_KB))
    ap.add_argument("--negate", action="store_true")
    ap.add_argument("--expect-outcomes", action="store_true",
                    help="after implementation: O probes must be green too")
    a = ap.parse_args()
    sys.path.insert(0, a.kb)
    import sdlc_check as kc  # noqa: E402
    base, outc = [], []

    def expect(group, name, cond, flips=False):
        if flips and a.expect_outcomes:
            cond, name = not cond, name + " [FLIPPED]"
        ok = bool(cond) != a.negate
        group.append(ok)
        print("%s %s" % ("GREEN" if ok else "RED  ", name))

    txt = "page one text here"
    src = "corpus/given/plan-ab12cd34.txt"
    loc = "p=1@0-8"
    cid = kc.kb_claim_id(src, loc, "")

    def row(prov="GIVEN", state="OK", source=src, at=loc):
        return (kc.kb_claim_id(source, at, ""),
                "page one", "-", "-", "-", source + "#" + at, prov, state)

    def sidecar(prov, extra=""):
        return ("---\nsha256: %s\ndate: 2026-10-16\nprovenance: %s\n%s"
                "extracted_through: complete\n---\n" % (sha(txt.encode()), prov, extra))

    print("-- baseline (green today)")
    # B1 -- an original that changed after ingest is reported nowhere.
    with tempfile.TemporaryDirectory() as tmp:
        orig = Path(tmp) / "plans" / "plan.pdf"
        orig.parent.mkdir()
        orig.write_bytes(b"%PDF version of 16/09")
        meta = sidecar("GIVEN", "original_path: plans/plan.pdf\noriginal_sha256: %s\n"
                       % sha(orig.read_bytes()))
        tree(tmp, {"plan-ab12cd34.txt": txt, "plan-ab12cd34.txt.meta.md": meta}, [row()])
        orig.write_bytes(b"%PDF version of 29/09")
        outs = [run(kc, [c, "--root", tmp])[1] for c in ("check", "corpus", "stale")]
        expect(base, "B1 changed original (original_path resolves) is silent in "
               "check/corpus/stale (FLIPS: stale names it)",
               not any("plan.pdf" in o for o in outs), flips=True)

    # B2 -- a GIVEN row on a sidecar declaring another provenance only WARNS (rc 0).
    for declared in ("OCR", "DECLARED"):
        with tempfile.TemporaryDirectory() as tmp:
            tree(tmp, {"plan-ab12cd34.txt": txt,
                       "plan-ab12cd34.txt.meta.md": sidecar(declared)}, [row()])
            rc, out = run(kc, ["graph", "--root", tmp])
            expect(base, "B2 GIVEN row on 'provenance: %s' sidecar warns, rc 0 (rc=%s)%s"
                   % (declared, rc, " (FLIPS: refused)" if declared == "DECLARED" else ""),
                   rc == 0 and "warn" in out.lower(), flips=declared == "DECLARED")

    # B3 -- a non-GIVEN row on a DECLARED source passes silently.
    with tempfile.TemporaryDirectory() as tmp:
        note = ("---\norigin: elicited\ndate: 2026-10-16\nprovenance: DECLARED\n---\n"
                "page one text here\n")
        nsrc = "corpus/notes/n.md"
        tree(tmp, {}, [row("ELICITED", source=nsrc, at="L6-6")], notes={"n.md": note})
        rc, out = run(kc, ["graph", "--root", tmp])
        expect(base, "B3 ELICITED row whose source declares 'provenance: DECLARED' "
               "passes (rc=%s) (FLIPS: refused)" % rc, rc == 0, flips=True)

    # B4 -- walk cost: os.walk+os.stat vs scandir+DirEntry.stat over 11,000 files.
    with tempfile.TemporaryDirectory() as tmp:
        for d in range(110):
            sub = Path(tmp) / ("d%03d" % d)
            sub.mkdir()
            for f in range(100):
                (sub / ("f%03d.txt" % f)).write_bytes(b"x" * (d + f))
        t0 = time.perf_counter()
        for dp, _dn, fn in os.walk(tmp):
            for f in fn:
                os.stat(os.path.join(dp, f))
        slow = time.perf_counter() - t0

        def walk(path):
            n = 0
            with os.scandir(path) as it:
                for e in it:
                    if e.is_dir(follow_symlinks=False):
                        n += walk(e.path)
                    elif e.is_file(follow_symlinks=False):
                        e.stat(follow_symlinks=False)
                        n += 1
            return n
        t0 = time.perf_counter()
        n = walk(tmp)
        fast = time.perf_counter() - t0
        print("      B4 os.walk+stat %.3fs; scandir %d files %.3fs" % (slow, n, fast))
        expect(base, "B4 scandir stat-only walk of 11,000 files under 0.5s", fast < 0.5)

    print("-- outcomes (red today, green after F-084)")
    # O1 -- R1 test 1: a source in pdf/ never examined is named by the inventory.
    with tempfile.TemporaryDirectory() as tmp:
        tree(tmp, {"plan-ab12cd34.txt": txt,
                   "plan-ab12cd34.txt.meta.md": sidecar("GIVEN")}, [row()])
        (Path(tmp) / "pdf").mkdir()
        (Path(tmp) / "pdf" / "regulation.pdf").write_bytes(b"%PDF regulation text")
        rc, out = run(kc, ["inventory", "pdf", "--root", tmp])
        expect(outc, "O1 `inventory pdf` names pdf/regulation.pdf NOT_EXAMINED (rc=%s)" % rc,
               rc == 0 and "NOT_EXAMINED" in out and "pdf/regulation.pdf" in out)
        rc, out = run(kc, ["orient", "--root", tmp])
        expect(outc, "O1b orient prints the not-examined upper bound",
               "Corpus reach: <= 1 " in out)

    # O2 -- R1 test 2: the newer plan beside the ingested one.
    with tempfile.TemporaryDirectory() as tmp:
        plans = Path(tmp) / "plans"
        plans.mkdir()
        (plans / "plan_1609.pdf").write_bytes(b"%PDF version of 16/09")
        (plans / "plan_2909.pdf").write_bytes(b"%PDF version of 29/09")
        meta = sidecar("GIVEN", "original_path: plans/plan_1609.pdf\noriginal_sha256: %s\n"
                       % sha(b"%PDF version of 16/09"))
        tree(tmp, {"plan-ab12cd34.txt": txt, "plan-ab12cd34.txt.meta.md": meta}, [row()])
        rc, out = run(kc, ["inventory", "plans", "--root", tmp])
        lines = out.splitlines()
        expect(outc, "O2 inventory: plan_1609 INGESTED, plan_2909 NOT_EXAMINED (rc=%s)" % rc,
               rc == 0
               and any("INGESTED" in ln and "plan_1609" in ln for ln in lines)
               and any("NOT_EXAMINED" in ln and "plan_2909" in ln for ln in lines))

    # O3 -- R1 test 3: what we told the client is a DECLARED row with recipient
    # and date, and its divergence from the ledger is held.
    with tempfile.TemporaryDirectory() as tmp:
        dsrc = "corpus/given/dpia-11aa22bb.txt"
        did = kc.kb_claim_id(dsrc, loc, "")
        rows = [row(),
                (did, "page one", "-", "-", "-", dsrc + "#" + loc, "DECLARED",
                 "DIVERGES " + cid)]
        tree(tmp, {"plan-ab12cd34.txt": txt,
                   "plan-ab12cd34.txt.meta.md": sidecar("GIVEN"),
                   "dpia-11aa22bb.txt": txt,
                   "dpia-11aa22bb.txt.meta.md": sidecar("DECLARED", "recipient: client\n")},
             rows)
        rc, out = run(kc, ["graph", "--root", tmp])
        expect(outc, "O3 DECLARED row DIVERGES from a GIVEN row passes graph (rc=%s)" % rc,
               rc == 0)

    # O4 -- the laundering the unit forbids: a GIVEN row on a DECLARED sidecar errors.
    with tempfile.TemporaryDirectory() as tmp:
        tree(tmp, {"plan-ab12cd34.txt": txt,
                   "plan-ab12cd34.txt.meta.md": sidecar("DECLARED", "recipient: client\n")},
             [row()])
        rc, out = run(kc, ["graph", "--root", tmp])
        expect(outc, "O4 GIVEN row on a DECLARED sidecar is refused (rc=%s)" % rc, rc != 0)

    # O5 -- a changed original is reported by stale.
    with tempfile.TemporaryDirectory() as tmp:
        orig = Path(tmp) / "plans" / "plan.pdf"
        orig.parent.mkdir()
        orig.write_bytes(b"%PDF version of 16/09")
        meta = sidecar("GIVEN", "original_path: plans/plan.pdf\noriginal_sha256: %s\n"
                       % sha(orig.read_bytes()))
        tree(tmp, {"plan-ab12cd34.txt": txt, "plan-ab12cd34.txt.meta.md": meta}, [row()])
        orig.write_bytes(b"%PDF version of 29/09")
        rc, out = run(kc, ["stale", "--root", tmp])
        expect(outc, "O5 stale names the changed original", "plans/plan.pdf" in out
               and "changed since ingest" in out)

    # O6 -- a registry-excluded FILE is listed EXCLUDED, never INGESTED (never read).
    with tempfile.TemporaryDirectory() as tmp:
        docs = tree(tmp, {"plan-ab12cd34.txt": txt,
                          "plan-ab12cd34.txt.meta.md": sidecar("GIVEN")}, [row()])
        (docs / "audit").mkdir()
        (docs / "audit" / "INVENTORY_exclusions.md").write_text(
            "| pattern | reason | approved |\n|---|---|---|\n"
            "| *.txt | copies | 2026-10-27 |\n", encoding="utf-8")
        (Path(tmp) / "copy.txt").write_text(txt, encoding="utf-8")
        rc, out = run(kc, ["inventory", ".", "--root", tmp])
        expect(outc, "O6 an excluded file pattern wins over its digest (rc=%s)" % rc,
               rc == 0 and any("EXCLUDED" in ln and "copy.txt" in ln
                               for ln in out.splitlines()))

    ok_base, ok_out = all(base), all(outc)
    print("baseline: %s; outcomes: %s" % ("green" if ok_base else "RED",
                                         "green" if ok_out else "red"))
    if a.expect_outcomes:
        return 0 if ok_base and ok_out else 1
    return 0 if ok_base else 1


if __name__ == "__main__":
    sys.exit(main())
