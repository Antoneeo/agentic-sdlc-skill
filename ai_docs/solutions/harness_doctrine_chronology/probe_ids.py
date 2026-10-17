"""F-073 probe (a): would a cross-ref id check have seen the recorded collisions?

Usage:  python -I probe_ids.py <repo> [--red]

Read-only: one `git grep` over every ref (heads, remotes, tags), never a checkout.

Identity of a unit = its ANALYSIS file name: declared by the ANALYSIS itself, or
announced by a request record's `analysis:` field before the ANALYSIS exists. (Round 1
of this probe keyed on the file slug and raised a false collision on `main`: F-069's
request record is `REQUEST_kb_graph_only.md`, its analysis `ANALYSIS_kb_graph_speed.md`.)
A collision = an id an OPEN unit of the tree declares, used on another ref by a
different ANALYSIS name.

Replays. The three collisions recorded on 2026-10-17 (F-065, F-068, F-069) are not in
any ref today: their branches were renamed or deleted, and F-069 was never committed
under that id. So the F-069 case is replayed by taking `feat/kb-site-spec`'s own
records and setting their id back to F-069, as R18 of REQUEST_kb_site records it was.
With --red the other refs are not consulted, and the collision must disappear.
"""
import re
import subprocess
import sys
import time

RED = "--red" in sys.argv
REPO = [a for a in sys.argv[1:] if not a.startswith("--")][0]
ID = re.compile(r"\b([A-Z]-\d{3,})\b")
PATHS = ["ai_docs/solutions/ANALYSIS_*.md", "ai_docs/audit/requests/REQUEST_*.md"]


def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout


def units(grep_out):
    """{ref: {id: {analysis_name}}}, open-ness per ANALYSIS as a second map."""
    per = {}
    for line in grep_out.splitlines():
        try:
            ref, path, rest = line.split(":", 2)
        except ValueError:
            continue
        key, _, val = rest.partition(":")
        per.setdefault((ref, path), {})[key] = val.strip()
    out, status = {}, {}
    for (ref, path), kv in per.items():
        name = path.rsplit("/", 1)[-1]
        analysis = name if name.startswith("ANALYSIS_") else kv.get("analysis", "")
        m = ID.search(kv.get("id") or kv.get("unit") or "")
        if m and analysis:
            out.setdefault(ref, {}).setdefault(m.group(1), set()).add(analysis)
            if name.startswith("ANALYSIS_"):
                status[(ref, analysis)] = kv.get("status", "")
    return out, status


def collisions(tree_ref, override=None):
    refs = [r for r in git("for-each-ref", "--format=%(refname)", "refs/heads",
                           "refs/remotes", "refs/tags").split() if not r.endswith("/HEAD")]
    if tree_ref not in refs:
        refs.append(tree_ref)
    grep = git("grep", "-E", "^(id|unit|analysis|status):", *refs, "--", *PATHS)
    by_ref, status = units(grep)
    mine = {}
    for fid, names in by_ref.get(tree_ref, {}).items():
        for n in names:
            if status.get((tree_ref, n), "PLANNED") in ("PLANNED", "IN_PROGRESS"):
                mine.setdefault(fid, set()).add(n)
    for n, fid in (override or {}).items():       # the replay: same files, old id
        for k in list(mine):
            mine[k].discard(n)
        mine.setdefault(fid, set()).add(n)
    tree_sha = git("rev-parse", tree_ref).strip()
    found = set()
    for ref, ids in ([] if RED else by_ref.items()):
        if ref == tree_ref or git("rev-parse", ref).strip() == tree_sha:
            continue
        for fid, names in ids.items():
            for n in names - mine.get(fid, set()):
                if fid in mine:
                    found.add((fid, tuple(sorted(mine[fid])), n, ref))
    return sorted(found)


t0 = time.time()
ok = True
replay = collisions("refs/remotes/origin/feat/kb-site-spec",
                    override={"ANALYSIS_kb_site.md": "F-069"})
for h in replay[:3]:
    print("  replay:", h)
seen = any(f == "F-069" and n == "ANALYSIS_kb_graph_speed.md" for f, _m, n, _r in replay)
print(("PASS" if seen else "FAIL") + " F-069 (kb_site) seen against kb_graph_speed on another ref")
ok &= seen
clean = collisions("refs/heads/main")
for h in clean:
    print("  on main:", h)
print(("PASS" if not clean else "FAIL") + " main today: no open unit's id used by another analysis")
ok &= not clean
print(f"elapsed {time.time() - t0:.1f}s for two full scans")
sys.exit(0 if ok else 1)
