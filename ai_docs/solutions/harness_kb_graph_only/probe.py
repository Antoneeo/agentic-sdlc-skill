"""Probe for F-069: where does `graph` spend its time at field scale, and does a
faster `knowledge.py` print exactly what the old one prints?

Builds synthetic docs roots shaped like the K-02 ledger (field report: 2183 claim
rows, 139 sidecars) and runs, in a fresh interpreter per version:
  - the working-tree `knowledge.py`;
  - with --baseline <git-ref>, also `knowledge.py` + `sdlc_core.py` at that ref.
Each run prints `graph`, `corpus`, the `kb_time_cycle` result and its warn lines
(the source of the kb `## claims` section of `stale` and of the orient count); the probe ASSERTS the two transcripts are byte-identical and
exits 1 on any mismatch. Timing is printed per version; --profile adds a cProfile of
the working tree's `graph`.

Run from the worktree root:
    python ai_docs/solutions/harness_kb_graph_only/probe.py --baseline main
"""
import argparse
import random
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[3]
SCRIPTS = REPO / "skills" / "agentic-sdlc-skill" / "scripts"

SHAPES = {
    "known": dict(rows=2183, arts=139, pages=40, page_chars=3000, topics=60,
                  superseded=80, windows=20, living=300),
    "mature": dict(rows=2183, arts=139, pages=200, page_chars=3000, topics=60,
                   superseded=400, windows=60, living=1000),
}

RUNNER = r'''
import io, sys, time, contextlib, cProfile, pstats
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import knowledge, sdlc_core
root = Path(sys.argv[2])
out = io.StringIO()
t0 = time.perf_counter()
with contextlib.redirect_stdout(out):
    rc_g = knowledge.kb_cmd_graph(root)
t_graph = time.perf_counter() - t0
with contextlib.redirect_stdout(out):
    rc_c = knowledge.kb_cmd_corpus(root)
cyc = knowledge.kb_time_cycle(root)
cited, chain, dang = knowledge.kb_time_cycle_warns(cyc)
print("rc graph=%d corpus=%d" % (rc_g, rc_c))
print(out.getvalue())
print("## cycle")
for k in ("cited", "expired", "chain", "dangling"):
    for item in cyc[k]:
        print(k, repr(item))
for ln in cited + chain + dang:
    print(ln)
sys.stderr.write("TIME graph %.2f\n" % t_graph)
if len(sys.argv) > 3:
    pr = cProfile.Profile()
    with contextlib.redirect_stdout(io.StringIO()):
        pr.enable(); knowledge.kb_cmd_graph(root); pr.disable()
    s = io.StringIO()
    pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(12)
    sys.stderr.write(s.getvalue())
'''


def build(root, rows, arts, pages, page_chars, topics, superseded, windows, living):
    rnd = random.Random(7)
    given = root / "corpus" / "given"
    given.mkdir(parents=True)
    words = ("alfa beta gamma delta canone prezzo lotto torre piano quota "
             "contratto rata scadenza listino").split()
    for a in range(arts):
        body = "\f".join(
            " ".join(rnd.choice(words) for _ in range(page_chars // 6))[:page_chars]
            for _ in range(pages))
        (given / ("doc%03d.txt" % a)).write_text(body, encoding="utf-8")
        (given / ("doc%03d.txt.meta.md" % a)).write_text(
            "---\ndate: 2026-09-01\nprovenance: GIVEN\nextracted_through: complete\n---\n",
            encoding="utf-8")
    sys.path.insert(0, str(SCRIPTS))
    import knowledge
    cols = knowledge.CLAIM_COLUMNS
    tdir = root / "topics"
    tdir.mkdir()
    per = rows // topics
    made = []
    for t in range(topics):
        for r in range(per):
            a = rnd.randrange(arts)
            pg = rnd.randrange(1, pages + 1)
            s = rnd.randrange(0, page_chars - 80)
            # one span in 50 runs past its page: findings must survive the cache
            end = page_chars + 5 if len(made) % 50 == 49 else s + 60
            loc = "p=%d@%d-%d" % (pg, s, end)
            path = "corpus/given/doc%03d.txt" % a
            rid = knowledge.kb_claim_id(path, loc, knowledge.kb_qty_key("-"))
            made.append({"t": t, "id": rid, "src": "%s#%s" % (path, loc),
                         "valid": "-", "state": "OK"})
    for i in range(superseded):
        made[2 * i]["state"] = "SUPERSEDED %s" % made[2 * i + 1]["id"]
    for i in range(windows):
        made[-1 - i]["valid"] = "from 2026-01-01 until 2026-06-01" if i % 2 else "until 2099-01-01"
    for t in range(topics):
        lines = ["---", "topic: t%02d" % t, "description: synthetic",
                 ("parents: [t00]" if t else ""), "---", "", "## Claims", "",
                 "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        for i, m in enumerate(x for x in made if x["t"] == t):
            lines.append("| %s | claim %d.%d | %s | - | - | %s | GIVEN | %s |"
                         % (m["id"], t, i, m["valid"], m["src"], m["state"]))
        (tdir / ("t%02d.md" % t)).write_text("\n".join(lines) + "\n", encoding="utf-8")
    sol = root / "solutions"
    sol.mkdir()
    for d in range(living):
        cites = " ".join(rnd.choice(made)["id"] for _ in range(10))
        # boundary cases: an id inside a longer hex run, and next to uppercase hex
        cites += " deadbeef%sCAFE %sA" % (made[0]["id"], made[2]["id"])
        (sol / ("doc%03d.md" % d)).write_text(
            "---\nstatus: CURRENT\n---\n# d\n" + ("text " * 400) + cites + "\n",
            encoding="utf-8")


def run(scripts_dir, root, profile=False):
    args = [sys.executable, "-I", "-c", RUNNER, str(scripts_dir), str(root)]
    if profile:
        args.append("profile")
    p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if p.returncode:
        sys.exit("runner failed for %s:\n%s" % (scripts_dir, p.stderr))
    return p.stdout, p.stderr


def export_ref(ref, dest):
    dest.mkdir()
    for name in ("knowledge.py", "sdlc_core.py"):
        blob = subprocess.run(
            ["git", "-C", str(REPO), "show",
             "%s:skills/agentic-sdlc-skill/scripts/%s" % (ref, name)],
            capture_output=True, check=True).stdout
        (dest / name).write_bytes(blob)
    return dest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", help="git ref to compare the working tree against")
    ap.add_argument("--shape", choices=sorted(SHAPES), action="append")
    ap.add_argument("--profile", action="store_true")
    a = ap.parse_args()
    failures = 0
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        base = export_ref(a.baseline, td / "baseline") if a.baseline else None
        for name in a.shape or sorted(SHAPES):
            root = td / name
            build(root, **SHAPES[name])
            out_new, err_new = run(SCRIPTS, root, a.profile)
            line = "%-7s working tree: %s" % (name, err_new.splitlines()[0])
            if base:
                out_old, err_old = run(base, root)
                same = out_old == out_new
                failures += not same
                line += " | %s: %s | identical: %s" % (
                    a.baseline, err_old.splitlines()[0], same)
            print(line)
            if a.profile:
                print("\n".join(err_new.splitlines()[1:]))
    if failures:
        print("FAIL: %d shape(s) differ from the baseline" % failures)
        return 1
    print("OK" if base else "OK (no baseline compared)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
