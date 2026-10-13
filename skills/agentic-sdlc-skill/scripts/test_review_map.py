#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-066 -- `review-map` tells an integrator which files of a change to review.

The question it answers came from integrators: "do we also review every change
under ai_docs?". On the F-065 merge 53% of the ai_docs lines were generated
indexes nobody needs to read, and nothing in the diff said so. These tests pin
the four classes (REVIEW / DESIGN / EVIDENCE / GENERATED), the rule that
GENERATED means "rewritten by this project's own `index`" (never a name or a
marker), and the failure cases of a command that takes a ref from the user.

Standard library only. Every test builds its own git repository and skips
where git is absent.
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENTRY = HERE / "sdlc_check.py"
HAS_GIT = shutil.which("git") is not None


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True)


def write(repo, rel, text="x\n"):
    p = Path(repo) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def run_entry(repo, *args):
    return subprocess.run([sys.executable, str(ENTRY), *args, "--root", str(repo)],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", cwd=str(repo))


def review_map(repo, *args):
    return run_entry(repo, "review-map", *args)


def rows(output):
    """{path: (status, class)} from the markdown table."""
    out = {}
    for line in output.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 5 and cells[3] in ("REVIEW", "DESIGN", "EVIDENCE", "GENERATED"):
            out[cells[0].strip("`")] = (cells[1], cells[3])
    return out


ANALYSIS = """---
id: F-001
feature: Demo
status: IN_PROGRESS
level: L3
start_date: 2026-10-12
end_date:
---
# Feature Analysis: Demo
"""

ADR = """---
description: why the demo exists
status: CURRENT
---
# ADR: demo
"""


def new_repo():
    d = Path(tempfile.mkdtemp(prefix="rmap_"))
    git(d, "init", "-q", "-b", "main")
    git(d, "config", "user.email", "t@example.invalid")
    git(d, "config", "user.name", "t")
    git(d, "config", "core.autocrlf", "false")
    return d


def commit(repo, msg="c"):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", msg)


@unittest.skipUnless(HAS_GIT, "git not available")
class ReviewMapTests(unittest.TestCase):

    def setUp(self):
        self.repo = new_repo()
        self.addCleanup(shutil.rmtree, self.repo, True)
        write(self.repo, "ai_docs/README.md", "# docs\n")
        write(self.repo, "ai_docs/architecture/ADR_base.md", ADR)
        write(self.repo, "src/app.py", "print(1)\n")
        self.assertEqual(run_entry(self.repo, "index").returncode, 0)
        commit(self.repo, "base")
        git(self.repo, "checkout", "-q", "-b", "feat")

    # AC1 -- the F-065 shape: code, design, evidence and regenerated indexes.
    def test_classes_on_a_realistic_change(self):
        write(self.repo, "ai_docs/solutions/ANALYSIS_demo.md", ANALYSIS)
        write(self.repo, "ai_docs/architecture/ADR_demo.md", ADR)
        write(self.repo, "ai_docs/audit/reviews/REVIEW_LOG.md", "| row |\n")
        write(self.repo, "ai_docs/solutions/harness_demo/probe.py", "pass\n")
        write(self.repo, "ai_docs/solutions/SHADOW_e_tdd_demo_v1.0.md", "mirror\n")
        write(self.repo, "src/app.py", "print(2)\n")
        write(self.repo, "distributions/x/app.py", "print(3)\n")
        self.assertEqual(run_entry(self.repo, "index").returncode, 0)
        commit(self.repo, "change")
        r = review_map(self.repo)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        got = {p: c for p, (_s, c) in rows(r.stdout).items()}
        self.assertEqual(got["src/app.py"], "REVIEW")
        self.assertEqual(got["distributions/x/app.py"], "REVIEW")
        self.assertEqual(got["ai_docs/solutions/ANALYSIS_demo.md"], "DESIGN")
        self.assertEqual(got["ai_docs/architecture/ADR_demo.md"], "DESIGN")
        self.assertEqual(got["ai_docs/audit/reviews/REVIEW_LOG.md"], "EVIDENCE")
        self.assertEqual(got["ai_docs/solutions/harness_demo/probe.py"], "EVIDENCE")
        self.assertEqual(got["ai_docs/solutions/SHADOW_e_tdd_demo_v1.0.md"], "GENERATED")
        for gen in ("ai_docs/INDEX.md", "ai_docs/strategic/features_history.md",
                    "ai_docs/memory/INDEX.md"):
            self.assertEqual(got[gen], "GENERATED", gen)
        order = [c for c in got.values()]
        self.assertEqual(order, sorted(order, key=["REVIEW", "DESIGN", "EVIDENCE",
                                                   "GENERATED"].index))

    # AC2 -- GENERATED is exactly what this project's `index` writes.
    def test_generated_equals_what_index_writes(self):
        write(self.repo, "ai_docs/audit/HANDOFF_demo.md",
              "---\nworkstream: F-001 Demo\nlevel: L3\nbranch: feat\nstatus: PROGRESS\n"
              "since: 2026-10-12\nnext: go\nupdated: 2026-10-12\n---\n\nbody\n")
        write(self.repo, "ai_docs/reference/GUIDE_demo.md",
              "---\ndescription: demo guide\nstatus: CURRENT\nsource_kind: document\n---\n# G\n")
        write(self.repo, "ai_docs/topics/demo.md", "---\ndescription: a topic\n---\n# T\n")
        write(self.repo, "ai_docs/corpus/doc.md", "# a corpus document\n")
        before = {p.relative_to(self.repo).as_posix()
                  for p in self.repo.rglob("*") if p.is_file() and ".git" not in p.parts}
        self.assertEqual(run_entry(self.repo, "index").returncode, 0)
        written = {p.relative_to(self.repo).as_posix()
                   for p in self.repo.rglob("*") if p.is_file() and ".git" not in p.parts}
        r = review_map(self.repo)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        got = rows(r.stdout)
        generated = {p for p, (_s, c) in got.items() if c == "GENERATED"}
        # the seven outputs `index` can write; those present in the change set
        # must be GENERATED and nothing else may be
        expected = {"ai_docs/audit/handoff.md", "ai_docs/INDEX.md",
                    "ai_docs/reference/INDEX.md", "ai_docs/strategic/features_history.md",
                    "ai_docs/memory/INDEX.md", "ai_docs/topics/INDEX.md",
                    "ai_docs/corpus/INDEX.md"}
        self.assertEqual(generated, expected & set(got))
        # the conditional writers really ran: three outputs are new in this
        # change, and the guide router changed from its empty stub
        for new in ("ai_docs/audit/handoff.md", "ai_docs/topics/INDEX.md",
                    "ai_docs/corpus/INDEX.md"):
            self.assertIn(new, written - before)
            self.assertIn(new, generated)
        self.assertIn("ai_docs/reference/INDEX.md", generated)

    def test_hand_written_handoff_is_not_generated(self):
        write(self.repo, "ai_docs/audit/handoff.md", "# Handoff\n\nfree prose\n")
        r = review_map(self.repo)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(rows(r.stdout)["ai_docs/audit/handoff.md"][1], "DESIGN")

    # AC3 -- committed, staged, unstaged and untracked all appear.
    def test_every_git_state_appears(self):
        write(self.repo, "src/committed.py")
        commit(self.repo)
        write(self.repo, "src/staged.py")
        git(self.repo, "add", "src/staged.py")
        write(self.repo, "src/app.py", "print('unstaged')\n")
        write(self.repo, "src/untracked.py", "a\nb\n")
        got = rows(review_map(self.repo).stdout)
        for p in ("src/committed.py", "src/staged.py", "src/app.py", "src/untracked.py"):
            self.assertIn(p, got)
        self.assertEqual(got["src/untracked.py"][0], "A")

    # AC4 -- inputs the command must refuse.
    def test_option_like_base_is_refused(self):
        r = review_map(self.repo, "--base=-x")
        self.assertEqual(r.returncode, 1)
        self.assertIn("[ERROR]", r.stdout + r.stderr)
        # the space form never reaches git either: argparse refuses it
        self.assertNotEqual(review_map(self.repo, "--base", "-x").returncode, 0)

    def test_unknown_base_is_refused(self):
        r = review_map(self.repo, "--base", "no-such-branch")
        self.assertEqual(r.returncode, 1)
        self.assertIn("--base", r.stdout + r.stderr)

    def test_not_a_git_repository(self):
        d = Path(tempfile.mkdtemp(prefix="rmap_nogit_"))
        self.addCleanup(shutil.rmtree, d, True)
        write(d, "ai_docs/README.md", "# docs\n")
        r = review_map(d)
        self.assertEqual(r.returncode, 1)
        self.assertIn("[ERROR]", r.stdout + r.stderr)

    def test_failing_index_fails_closed(self):
        # a hand-written registry with a row no HANDOFF source accounts for,
        # plus one source: `index` refuses to overwrite it and exits 1
        write(self.repo, "ai_docs/audit/handoff.md",
              "# Handoff\n\n| Workstream | Level |\n|---|---|\n| F-999 Orphan | L3 |\n")
        write(self.repo, "ai_docs/audit/HANDOFF_demo.md",
              "---\nworkstream: F-001 Demo\nlevel: L3\nbranch: feat\nstatus: PROGRESS\n"
              "since: 2026-10-12\nnext: go\nupdated: 2026-10-12\n---\n")
        r = review_map(self.repo)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("[ERROR]", r.stdout + r.stderr)
        self.assertNotIn("| GENERATED |", r.stdout)

    # AC5 -- rename, binary, no change.
    def test_rename_binary_and_no_change(self):
        r = review_map(self.repo)
        self.assertEqual(r.returncode, 0)
        self.assertIn("no changes against", r.stdout)
        write(self.repo, "src/big.py", "".join(f"line {i}\n" for i in range(50)))
        commit(self.repo)
        git(self.repo, "checkout", "-q", "main")
        git(self.repo, "merge", "-q", "feat")
        git(self.repo, "checkout", "-q", "feat")
        git(self.repo, "mv", "src/big.py", "src/renamed.py")
        (self.repo / "src" / "blob.bin").write_bytes(b"\x00\x01\x02binary")
        commit(self.repo)
        out = review_map(self.repo).stdout
        got = rows(out)
        self.assertEqual(got["src/renamed.py"][0], "R")
        self.assertNotIn("src/big.py", got)
        blob = next(l for l in out.splitlines() if "src/blob.bin" in l)
        self.assertEqual(blob.split("|")[3].strip(), "bin")

    # AC8 -- the command is visible.
    def test_help_lists_review_map(self):
        r = subprocess.run([sys.executable, str(ENTRY), "--help"],
                           capture_output=True, text=True)
        self.assertIn("review-map", r.stdout)


class EscapeTests(unittest.TestCase):
    # AC6 -- a hostile file name stays one table row.
    def test_pipe_and_control_characters_are_escaped(self):
        spec = importlib.util.spec_from_file_location("sdlc_check_rmap", ENTRY)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        cell = mod.table_cell("a|b\nc\td")
        self.assertNotIn("\n", cell)
        self.assertNotIn("\t", cell)
        self.assertNotIn("|", cell.replace("\\|", ""))


if __name__ == "__main__":
    unittest.main()
