#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Domain entry point with shared project memory.

Ship this file, sdlc_core.py and knowledge.py together. The core alone omits
knowledge integrity and this entry point\'s domain-specific behavior.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import sdlc_core
except ImportError as exc:  # pragma: no cover - exercised by TS12, not by unit tests
    sys.stderr.write(
        "[ERROR] sdlc_check.py cannot find sdlc_core.py next to it: " + str(exc) + "\n"
        "        The validator needs entry point, sdlc_core.py and knowledge.py.\n"
        "        Copy all three together; core alone omits memory and overlay checks.\n")
    sys.exit(1)

# Re-export the core's surface: existing importers (`import sdlc_check as sc`)
# and the test batteries reach for these names on this module.
from sdlc_core import *            # noqa: F401,F403
from sdlc_core import _map_refs    # noqa: F401  underscore helper used by the batteries
import knowledge

# The domain this distribution implements. It does NOT decide any document's
# owning domain -- that is resolved per project (`default_domain:` in the docs
# root's README) and per artifact (`domain:`), so the same tree gets the same
# verdict from every installed distribution. What it decides is which portable
# checks a document may import here by name; the rest warn as unavailable.
DOMAIN = "code"

sdlc_core.set_entry_point(DOMAIN, provides=("code", "knowledge"))

# What this distribution carries. The shared battery reads it; the spine
# capabilities are not optional, and a shared test refuses a profile that drops one.
sdlc_core.set_profile(
    skill_name="agentic-sdlc",
    unit_noun="feature",
    support_files=("templates.md", "architect.md", "guides.md", "vision.md", "tdd.md",
                   "debugging.md", "elicitation.md", "review.md", "dispatch.md",
                   "routing.md", "hybrid.md", "ENFORCEMENT.md", "memory.md"),
    capabilities=(
        # spine
        "triage", "write_triggers", "workstream_registry", "vision_gate",
        "design_review_gate", "guide_router", "worktree_hygiene",
        # code overlay
        "architect_pass", "interaction_contract", "comprehension_guides", "tdd",
        "subagent_dispatch", "legacy_narrative_handoff", "question_discipline",
    ),
    design_gate_between=("### 3. Request Analysis", "### 4. Development and Testing"),
    remind_line=(
        "first decide if this skill governs the work; if yes, LOAD it once -- an "
        "unread protocol cannot be applied. Declare the level (L1/L2/L3/Spike) "
        "and the guide-router verdict before acting; an imperative is a request "
        "to triage. Name the mechanism before fixing the first defect you can "
        "measure -- symptom patches recur and stack. Replay governing text -- "
        "doctrine, a prompt, a schema -- against the case that motivated it: red "
        "under the old text, green under the new."
    ),
)


# ------------------------------------------------------------- review-map (F-066)
# Which files of a change an integrator must review. GENERATED is learned by
# running this entry point's own `index` on a throwaway copy of the docs root:
# a name filter (GENERATED_DOCS) or the GENERATED marker each misread a real
# file (memory/INDEX.md carries no marker), while execution cannot drift from
# the writers. Code lens only: other lenses write other generated files.

REVIEW_CLASSES = ("REVIEW", "DESIGN", "EVIDENCE", "GENERATED")
REVIEW_INSTRUCTIONS = {
    "REVIEW": "review",
    "DESIGN": "reference the code is checked against; read the changed parts "
              "(the brief states which review covered them)",
    "EVIDENCE": "spot-check that what the brief cites exists (verdicts, owner "
                "statements); do not re-review",
    "GENERATED": "skip; rewritten by `index` (a CLEAN `check` proves it) or, for "
                 "SHADOW_ mirrors, exported from devPNT",
}
REVIEW_MAP_HELP = ("\nCode lens:\n  review-map [--base REF] [--root DIR] [--docs-dir NAME]\n"
                   "      classify every file changed since the merge-base with REF "
                   "(default main):\n      REVIEW / DESIGN / EVIDENCE / GENERATED, "
                   "as a markdown table for the merge review brief")


def table_cell(text):
    """One markdown table cell: `|` escaped, control characters made visible."""
    out = []
    for ch in str(text):
        if ch == "|":
            out.append("\\|")
        elif ch == "`":                     # would close the path's code span
            out.append("'")
        elif ord(ch) < 32 or ord(ch) == 127:
            out.append("\\x%02x" % ord(ch))
        else:
            out.append(ch)
    return "".join(out)


def _git(top, *args):
    import subprocess
    return subprocess.run(["git", "-C", str(top), *args], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def _z(text):
    return [t for t in text.split("\0")]


def _changes(top, base_sha):
    """[(status, path, plus, minus)] for everything differing from base_sha in the
    working tree -- committed, staged, unstaged -- plus untracked files."""
    stat = {}
    toks = _z(_git(top, "diff", "--numstat", "-z", "-M", base_sha).stdout)
    i = 0
    while i < len(toks) and toks[i]:
        add, dele, path = toks[i].split("\t", 2)
        if path == "":                      # rename: old and new follow
            path = toks[i + 2]
            i += 3
        else:
            i += 1
        stat[path] = (add, dele)
    out = []
    toks = _z(_git(top, "diff", "--name-status", "-z", "-M", base_sha).stdout)
    i = 0
    while i < len(toks) and toks[i]:
        code = toks[i][0]
        if code in "RC":
            path = toks[i + 2]
            i += 3
        else:
            path = toks[i + 1]
            i += 2
        add, dele = stat.get(path, ("-", "-"))
        out.append((code, path, add, dele))
    for path in _z(_git(top, "ls-files", "--others", "--exclude-standard", "-z").stdout):
        if not path:
            continue
        try:
            data = (Path(top) / path).read_bytes()
        except OSError:                     # dangling link, locked file: list it, count nothing
            out.append(("A", path, "-", "-"))
            continue
        if b"\0" in data[:8000]:
            out.append(("A", path, "-", "-"))
        else:                               # git counts "\n"; a last unterminated line too
            lines = data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)
            out.append(("A", path, str(lines), "0"))
    return out


def _generated_set(docs):
    """Docs-root-relative paths this project's `index` writes, learned by running
    it on a throwaway copy. None (and the error printed) when `index` fails."""
    import os
    import shutil
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory(prefix="review_map_") as tmp:
        copy = Path(tmp) / docs.name
        shutil.copytree(docs, copy)
        before = {}
        for p in copy.rglob("*"):
            if p.is_file():
                os.utime(p, (0, 0))
                before[p] = p.stat().st_mtime_ns
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "index",
                            "--root", tmp, "--docs-dir", docs.name],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
        if r.returncode != 0:
            print("[ERROR] the project's `index` failed on a throwaway copy of "
                  f"{docs.name}/, so generated files cannot be told apart; fix it first:")
            print("\n".join("        " + l for l in (r.stdout + r.stderr).strip().splitlines()))
            return None
        # compared per file, not against zero: a filesystem that clamps epoch 0
        # must not turn every docs file into GENERATED, whose instruction is "skip"
        return {p.relative_to(copy).as_posix() for p in copy.rglob("*")
                if p.is_file() and p.stat().st_mtime_ns != before.get(p)}


def classify_path(path, docs_prefix, generated):
    """One class for a top-level-relative path."""
    if not (path == docs_prefix or path.startswith(docs_prefix + "/")):
        return "REVIEW"
    rel = path[len(docs_prefix) + 1:]
    name = rel.rsplit("/", 1)[-1]
    if rel in generated or (rel.startswith("solutions/") and name.startswith("SHADOW_")):
        return "GENERATED"
    if (rel.startswith("audit/reviews/") or rel.startswith("audit/HANDOFF_")
            or rel.startswith("audit/requests/") or rel.startswith("solutions/harness_")):
        return "EVIDENCE"
    return "DESIGN"


def cmd_review_map(argv):
    import argparse
    ap = argparse.ArgumentParser(prog="sdlc_check.py review-map")
    ap.add_argument("--base", default="main")
    ap.add_argument("--root")
    ap.add_argument("--docs-dir", dest="docs_dir")
    args = ap.parse_args(argv)
    if args.base.startswith("-"):
        print(f"[ERROR] --base {args.base!r} looks like an option; pass a branch, tag or commit.")
        return 1
    try:
        discovered, name = sdlc_core.resolve_docs_dir(args, args.root)
    except sdlc_core.AmbiguousDocsRoot as exc:
        print(f"[ERROR] {exc}")
        return 1
    sdlc_core.set_docs_dir(name)
    root = Path(args.root).resolve() if args.root else (discovered or sdlc_core.find_project_root())
    if not sdlc_core.require_ai_docs(root, "review-map"):
        return 1
    top = _git(root, "rev-parse", "--show-toplevel")
    if top.returncode != 0:
        print(f"[ERROR] {root} is not inside a git repository: review-map compares a change with --base.")
        return 1
    top = Path(top.stdout.strip()).resolve()
    sha = _git(top, "rev-parse", "--verify", "--quiet", args.base + "^{commit}")
    if sha.returncode != 0:
        print(f"[ERROR] base {args.base!r} not found; pass --base <branch|tag|commit>.")
        return 1
    mb = _git(top, "merge-base", sha.stdout.strip(), "HEAD")
    if mb.returncode != 0:
        print(f"[ERROR] no merge-base between {args.base!r} and HEAD; pass another --base.")
        return 1
    mb = mb.stdout.strip()
    docs = sdlc_core.ai_path(root).resolve()
    try:
        docs_prefix = docs.relative_to(top).as_posix()
    except ValueError:
        print(f"[ERROR] {docs} is outside the git repository {top}.")
        return 1
    changes = _changes(top, mb)
    if not changes:
        print(f"no changes against {args.base} (merge-base {mb[:12]})")
        return 0
    generated = set()
    if any(classify_path(p, docs_prefix, set()) != "REVIEW" for _c, p, _a, _d in changes):
        generated = _generated_set(docs)
        if generated is None:
            return 1
    rows = sorted(((classify_path(p, docs_prefix, generated), c, p, a, d)
                   for c, p, a, d in changes),
                  key=lambda r: (REVIEW_CLASSES.index(r[0]), r[2]))
    print(f"# Review map -- {len(rows)} files against {args.base} (merge-base {mb[:12]})\n")
    print("| Path | Status | +/- | Class | What to do |")
    print("|---|---|---|---|---|")
    totals = {k: [0, 0, 0] for k in REVIEW_CLASSES}
    for cls, code, path, add, dele in rows:
        lines = "bin" if add == "-" else f"+{add}/-{dele}"
        print(f"| `{table_cell(path)}` | {code} | {lines} | {cls} | {REVIEW_INSTRUCTIONS[cls]} |")
        t = totals[cls]
        t[0] += 1
        if add != "-":
            t[1] += int(add)
            t[2] += int(dele)
    print()
    print("Totals: " + "; ".join(f"{k} {v[0]} files (+{v[1]}/-{v[2]})"
                                 for k, v in totals.items() if v[0]))
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["review-map"]:
        return cmd_review_map(argv[1:])
    rc = knowledge.main(argv)
    if argv[:1] in (["-h"], ["--help"]):
        print(REVIEW_MAP_HELP)
    return rc


if __name__ == "__main__":
    sys.exit(main())
