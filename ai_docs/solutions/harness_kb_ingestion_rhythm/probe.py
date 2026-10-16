#!/usr/bin/env python3
"""Execute-before-specify harness for ANALYSIS_kb_ingestion_rhythm.

Each probe runs the real kb validator CLI on a throwaway KB and asserts the
behaviour the design rests on. Eleven assertions; P1, P2 and P5 carry a RED twin, P7 was RED before F1
(the same check against a negated state), and P6 pins a LIMIT of the tools:
what they do not verify.

    python -I ai_docs/solutions/harness_kb_ingestion_rhythm/probe.py
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[3]
CLI = REPO / "distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_check.py"
sys.path.insert(0, str(CLI.parent))
import sdlc_check as kc  # noqa: E402

TEXT = "Gate opens at 07:00.\nThe badge reader is model X2.\nPower is 24 V.\n"
HEAD = ("---\ntopic: t\ndescription: d\nparents: []\nstatus: CURRENT\n---\n\n"
        "## Claims\n\n| id | claim | valid | qty | about | source | prov | state |\n"
        "|---|---|---|---|---|---|---|---|\n")


def cli(root, *args):
    rooted = [] if args[0] == "claim-id" else ["--root", str(root)]
    r = subprocess.run([sys.executable, "-I", str(CLI), *args, *rooted], cwd=str(root),
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout + r.stderr


def anchor(root, phrase):
    rc, out = cli(root, "anchor", "corpus/given/s.txt", phrase)
    assert rc == 0, out
    loc = out.strip().splitlines()[0].strip()
    return loc


def topic(rows):
    return HEAD + "".join("| %s |\n" % " | ".join(r) for r in rows)


def build(tmp):
    docs = Path(tmp) / "ai_docs"
    (docs / "topics").mkdir(parents=True)
    (docs / "corpus/given").mkdir(parents=True)
    (docs / "corpus/given/s.txt").write_text(TEXT, encoding="utf-8", newline="\n")
    return docs


results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print("%s  %s %s" % ("GREEN" if cond else "RED  ", name, detail))


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    docs = build(tmp)

    # P2 -- `anchor` yields a locator that `graph` accepts (no hand counting).
    loc_a = anchor(root, "Gate opens at 07:00.")
    loc_b = anchor(root, "Power is 24 V.")
    print("anchor ->", loc_a, "|", loc_b)
    src = lambda loc: loc if loc.startswith("corpus/") else "corpus/given/s.txt#" + loc
    # P3 -- ids left empty, filled in one pass by `claim-id --fill`.
    t = docs / "topics/t.md"
    t.write_text(topic([("", "gate opens 07:00", "-", "-", "-", src(loc_a), "GIVEN", "OK")]),
                 encoding="utf-8")
    rc, out = cli(root, "claim-id", "ai_docs/topics/t.md", "--fill")
    filled = t.read_text(encoding="utf-8")
    id_a = [c.strip() for c in filled.splitlines()[-1].strip("|").split("|")][0]
    check("P3 claim-id --fill writes the id", rc == 0 and len(id_a) >= 8, out.strip()[-120:])
    rc, out = cli(root, "graph")
    check("P2 graph accepts the anchor-produced row", rc == 0, out.strip()[-200:])

    # P2-RED -- a hand-counted locator off by one is caught by graph.
    bad = t.read_text(encoding="utf-8").replace(src(loc_a).split("#")[1],
                                                 "L2@0-20", 1)
    t.write_text(bad, encoding="utf-8")
    rc_bad, out_bad = cli(root, "graph")
    check("P2-RED graph rejects a locator moved after its id was minted", rc_bad != 0, out_bad.strip()[-160:])
    t.write_text(filled, encoding="utf-8")

    # P6 -- LIMIT: a hand-counted, in-range, wrong span whose id is filled AFTER
    # passes graph and check. graph verifies span existence + id consistency,
    # never that the span carries the claim -- so FS4 must not call it verified.
    t.write_text(topic([("", "gate opens 07:00", "-", "-", "-",
                         "corpus/given/s.txt#L2-2", "GIVEN", "OK")]), encoding="utf-8")
    cli(root, "claim-id", "ai_docs/topics/t.md", "--fill")
    rc_g, _ = cli(root, "graph")
    rc_c, out_c = cli(root, "check")
    check("P6 LIMIT wrong span + late --fill passes graph and check", rc_g == 0 and rc_c == 0, out_c.strip()[-60:])
    t.write_text(filled, encoding="utf-8")

    # A living document cites claim A.
    rep = docs / "solutions/REPORT_k.md"
    rep.parent.mkdir(parents=True)
    rep.write_text("---\ndescription: r\nstatus: CURRENT\n---\nGate time per %s.\n" % id_a,
                   encoding="utf-8")

    # Ingestion step 2: claim B supersedes A. The cascade (`stale`) is NOT run.
    id_b = kc.kb_claim_id("corpus/given/s.txt", src(loc_b).split("#")[1], "")
    t.write_text(topic([(id_a, "gate opens 07:00", "-", "-", "-", src(loc_a), "GIVEN",
                         "SUPERSEDED " + id_b),
                        (id_b, "power 24 V", "-", "-", "-", src(loc_b), "GIVEN", "OK")]),
                 encoding="utf-8")
    rc, out = cli(root, "graph")
    check("P4 graph stays fast-check clean after a supersession", rc == 0, out.strip()[-160:])
    # Ingestion step 3: more rows arrive later (an unrelated note).
    (docs / "corpus/notes").mkdir(parents=True)
    (docs / "corpus/notes/n1.md").write_text(
        "---\norigin: elicited\ndate: 2026-10-16\nstatus: CURRENT\n---\nUnrelated remark.\n",
        encoding="utf-8")

    # P1 -- at closure, `stale` still lists the citing document: state-derived.
    rc, out = cli(root, "stale")
    check("P1 deferred stale still lists the citing doc", "REPORT_k.md" in out,
          "(rc=%s)" % rc)
    rc, out = cli(root, "check")
    check("P1b check carries the citation warn meanwhile", "REPORT_k.md" in out)
    # P1-RED -- once the document names the successor, the worklist clears.
    rep.write_text(rep.read_text(encoding="utf-8") + "Superseded by %s.\n" % id_b,
                   encoding="utf-8")
    rc, out = cli(root, "stale")
    check("P1-RED revised doc leaves the worklist", "REPORT_k.md" not in out)

    # P5 -- registry: HANDOFF file -> row via index; delete -> row gone.
    audit = docs / "audit"
    audit.mkdir()
    ho = ("---\nworkstream: %s\nlevel: L3\nbranch: main\nstatus: IN_PROGRESS\n"
          "since: 2026-10-15\nnext: ingest\ndetails: A.md\nupdated: 2026-10-16\n---\nx\n")
    (audit / "HANDOFF_k02.md").write_text(ho % "K-02 front", encoding="utf-8")
    (audit / "HANDOFF_k03.md").write_text(ho % "K-03 other", encoding="utf-8")
    rc, out = cli(root, "index")
    reg = (audit / "handoff.md").read_text(encoding="utf-8") if (audit / "handoff.md").exists() else ""
    check("P5 index generates the registry row", "K-02 front" in reg, out.strip()[-160:])
    (audit / "HANDOFF_k02.md").unlink()
    cli(root, "index")
    reg = (audit / "handoff.md").read_text(encoding="utf-8")
    check("P5-RED deleting the HANDOFF removes the row", "K-02 front" not in reg)
    # P7 -- F1 (fixed on main 28a565d): deleting the LAST HANDOFF empties the
    # generated registry. Before the fix the closed row survived (RED observed
    # 2026-10-16 on 282cd39), which is why SKILL.md once carried an interim.
    (audit / "HANDOFF_k03.md").unlink()
    cli(root, "index")
    reg = (audit / "handoff.md").read_text(encoding="utf-8")
    check("P7 last HANDOFF deleted -> registry row gone", "K-03 other" not in reg)

fails = [n for n, ok in results if not ok]
print("\n%d/%d green" % (len(results) - len(fails), len(results)))
sys.exit(1 if fails else 0)
