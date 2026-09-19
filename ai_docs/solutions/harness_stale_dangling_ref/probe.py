#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Executed claims behind ANALYSIS_stale_dangling_ref.md (F-056).

    python ai_docs/solutions/harness_stale_dangling_ref/probe.py [path/to/sdlc_core.py]

P1  `mark` records HEAD; amending HEAD to include the rewritten audit_plan.md leaves
    the row pointing at a commit no branch contains (not an ancestor of HEAD).
P2  once the reflog expires and gc prunes it, `stale` cannot resolve the ref. Before
    F-056 it printed a warning and returned 0 -- the area was silently excluded.
    After F-056 it must return 1 and tell the user to re-mark the area.
P3  while the orphan is still reachable through the reflog, `stale` must say it is
    not an ancestor of HEAD (the early warning that precedes P2), without failing.
P4  control: mark then a NEW commit -- ref is an ancestor, no warning, rc 0.
P5  squash-merge seen from a fresh clone: the feature-branch ref never reaches the clone
    at all, so it is missing there with no prior warning -- `stale` must fail (rc 1).
P6  shallow clone whose reference predates the clone depth: rc 1 and the fetch hint.
P7  a hash reference evaluated where git is unavailable (no work tree): before F-056 it
    fell to the timestamp branch ("not parseable", rc 0); after, rc 1.
P8  an ANALYZED row whose reference is neither hash nor ISO, in a git tree: rc 1.
P9  `check` over P2's tree prints NOT CLEAN and returns 1.

The expected values are the F-056 contract. Run against the pre-F-056 core
(`git show e5b7bc0:skills/agentic-sdlc-skill/scripts/sdlc_core.py > old.py`) to see
P2b, P3 and P5-P9 red. Everything runs in temp dirs; git is required.
"""
import contextlib
import importlib.util
import io
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CORE = Path(sys.argv[1]) if len(sys.argv) > 1 else \
    REPO / "skills" / "agentic-sdlc-skill" / "scripts" / "sdlc_core.py"

spec = importlib.util.spec_from_file_location("sdlc_core_probe", CORE)
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)
sc.set_docs_dir("ai_docs")

failures = []


def git(cwd, *args):
    r = subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid",
                        "-c", "commit.gpgsign=false"] + list(args),
                       cwd=str(cwd), capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr}")
    return r.stdout.strip()


def run(fn, *a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fn(*a)
    return rc, buf.getvalue()


def repo(tmp):
    root = Path(tmp)
    (root / "src").mkdir()
    (root / "src" / "a.txt").write_text("one\n", encoding="utf-8")
    (root / "ai_docs" / "audit").mkdir(parents=True)
    (root / "ai_docs" / "audit" / "audit_plan.md").write_text(
        "# Audit Plan\n\n| Path | Status | Reference | Notes |\n|---|---|---|---|\n"
        "| src/ | PENDING | - | |\n", encoding="utf-8")
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    rc, _ = run(sc.cmd_mark, root, ["src"])
    assert rc == 0
    return root


def recorded_ref(root):
    _, _, rows = sc.parse_audit_plan(root)
    return next(r["ref"] for r in rows if r["path"].startswith("src"))


def check(name, cond, detail):
    print(f"[{'green' if cond else 'RED'}] {name}")
    if not cond:
        print("      " + detail.replace("\n", "\n      "))
        failures.append(name)


with tempfile.TemporaryDirectory() as t:
    root = repo(t)
    ref = recorded_ref(root)
    git(root, "commit", "-q", "-a", "--amend", "--no-edit")          # the defect's gesture
    anc = subprocess.run(["git", "merge-base", "--is-ancestor", ref, "HEAD"],
                         cwd=root, capture_output=True).returncode
    check("P1 amended mark ref is not an ancestor of HEAD", anc == 1, f"is-ancestor rc={anc}")

    rc, out = run(sc.cmd_stale, root)
    check("P3 reachable orphan: warned as not an ancestor, rc 0",
          rc == 0 and "not an ancestor" in out, f"rc={rc}\n{out}")

    git(root, "reflog", "expire", "--expire-unreachable=now", "--all")
    git(root, "gc", "-q", "--prune=now")
    gone = subprocess.run(["git", "cat-file", "-e", ref + "^{commit}"],
                          cwd=root, capture_output=True).returncode != 0
    check("P2a gc pruned the orphan", gone, "object still present")
    rc, out = run(sc.cmd_stale, root)
    check("P2b pruned ref: stale fails (rc 1) and names the re-mark",
          rc == 1 and "mark src/" in out and "[ok]" not in out, f"rc={rc}\n{out}")

with tempfile.TemporaryDirectory() as t:
    root = repo(t)
    git(root, "commit", "-q", "-a", "-m", "record analysis")          # the right gesture
    rc, out = run(sc.cmd_stale, root)
    check("P4 control: new commit, no warning, rc 0",
          rc == 0 and "[warn]" not in out and "[ok]" in out, f"rc={rc}\n{out}")

def commit_all(root, msg):
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", msg)


def set_ref(root, new):
    plan = root / "ai_docs" / "audit" / "audit_plan.md"
    plan.write_text(plan.read_text(encoding="utf-8").replace(recorded_ref(root), new),
                    encoding="utf-8")


with tempfile.TemporaryDirectory() as t:
    origin = Path(t) / "origin"
    origin.mkdir()
    root = repo(origin)
    trunk = git(root, "branch", "--show-current")
    git(root, "checkout", "-q", "-b", "feature")
    (root / "src" / "a.txt").write_text("two\n", encoding="utf-8")
    commit_all(root, "feature work")
    run(sc.cmd_mark, root, ["src"])                                  # marked on the branch
    commit_all(root, "record analysis")
    git(root, "checkout", "-q", trunk)
    git(root, "merge", "-q", "--squash", "feature")
    git(root, "commit", "-q", "-m", "squash feature")
    git(root, "branch", "-q", "-D", "feature")
    clone = Path(t) / "clone"
    # file:// transfers reachable objects only; a plain-path clone hardlinks every object
    subprocess.run(["git", "clone", "-q", "file://" + origin.as_posix(), str(clone)], check=True,
                   capture_output=True)
    rc, out = run(sc.cmd_stale, clone)
    check("P5 squash-merged ref seen from a fresh clone: rc 1",
          rc == 1 and "[ok]" not in out, f"rc={rc}\n{out}")

    depth1 = Path(t) / "depth1"
    subprocess.run(["git", "clone", "-q", "--depth", "1", "file://" + origin.as_posix(),
                    str(depth1)], check=True, capture_output=True)
    set_ref(depth1, git(origin, "rev-list", "--max-parents=0", "HEAD")[:12])
    rc, out = run(sc.cmd_stale, depth1)
    check("P6 shallow clone, ref beyond the depth: rc 1 + shallow hint",
          rc == 1 and "--unshallow" in out and "squash-merged" in out, f"rc={rc}\n{out}")

    nogit = Path(t) / "nogit"
    shutil.copytree(clone, nogit, ignore=shutil.ignore_patterns(".git"))
    rc, out = run(sc.cmd_stale, nogit)
    check("P7 hash ref where git is unavailable: rc 1, cause named as git",
          rc == 1 and "git is not usable here" in out and "[ok]" not in out,
          f"rc={rc}\n{out}")

    set_ref(clone, "unknown")
    rc, out = run(sc.cmd_stale, clone)
    check("P8 unparseable reference in a git tree: rc 1",
          rc == 1 and "[ok]" not in out, f"rc={rc}\n{out}")

    rc, out = run(sc.cmd_check, clone)
    check("P9 check over an unverifiable row: NOT CLEAN, rc 1",
          rc == 1 and "NOT CLEAN" in out, f"rc={rc}\n{out[-300:]}")

print(f"\n{len(failures)} red" if failures else "\nall green")
sys.exit(1 if failures else 0)
