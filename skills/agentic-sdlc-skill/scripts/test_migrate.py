#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TS18 — relocating a project's documentation root, reversibly.

A migration tool is the most dangerous thing in this package: it is the only
command that writes outside a single file, and it runs on somebody's real corpus.
Every assertion here is about what it REFUSES to do.

    python scripts/test_migrate.py
"""
import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_core  # noqa: E402


def seed(root, docs="mkt_docs"):
    d = Path(root) / docs
    (d / "vision").mkdir(parents=True, exist_ok=True)
    (d / "vision" / "V.md").write_text(
        f"# V\n\nSee `{docs}/strategy/O.md` for the objectives.\n", encoding="utf-8")
    (d / "strategy").mkdir(parents=True, exist_ok=True)
    (d / "strategy" / "O.md").write_text("# O\n\nNo reference here.\n", encoding="utf-8")
    return d


def run(root, *argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = sdlc_core.main(["migrate", "--root", str(root), *argv])
    return rc, buf.getvalue()


class MigrateRefusals(unittest.TestCase):

    def test_dry_run_is_the_default_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d)
            rc, out = run(d, "--from", "mkt_docs")
            self.assertEqual(rc, 0)
            self.assertIn("[dry-run]", out)
            self.assertFalse((Path(d) / "ai_docs").exists(),
                             "a dry run that writes is not a dry run")

    def test_missing_source_refuses(self):
        with tempfile.TemporaryDirectory() as d:
            rc, out = run(d, "--from", "mkt_docs")
            self.assertEqual(rc, 1)
            self.assertIn("not found", out)

    def test_same_name_refuses(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d, "ai_docs")
            rc, out = run(d, "--from", "ai_docs", "--to", "ai_docs")
            self.assertEqual(rc, 1)
            self.assertIn("nothing to do", out)

    def test_an_existing_target_file_refuses_rather_than_overwriting(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d)
            target = Path(d) / "ai_docs" / "vision"
            target.mkdir(parents=True)
            (target / "V.md").write_text("# somebody else's file\n", encoding="utf-8")
            rc, out = run(d, "--from", "mkt_docs", "--apply")
            self.assertEqual(rc, 1)
            self.assertIn("Refusing to overwrite", out)
            self.assertIn("somebody else's file",
                          (target / "V.md").read_text(encoding="utf-8"),
                          "the existing file must be exactly as it was")

    def test_a_dirty_git_tree_refuses(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d)
            try:
                subprocess.run(["git", "init", "-q"], cwd=d, check=True,
                               capture_output=True, timeout=30)
                subprocess.run(["git", "add", "-A"], cwd=d, check=True,
                               capture_output=True, timeout=30)
            except Exception:  # pragma: no cover - git absent in this environment
                self.skipTest("git not available")
            # staged but never committed: the tree has changes
            rc, out = run(d, "--from", "mkt_docs", "--apply")
            self.assertEqual(rc, 1)
            self.assertIn("uncommitted changes", out)
            self.assertFalse((Path(d) / "ai_docs").exists())


class MigrateApply(unittest.TestCase):

    def test_it_copies_and_never_deletes(self):
        with tempfile.TemporaryDirectory() as d:
            src = seed(d)
            rc, out = run(d, "--from", "mkt_docs", "--apply")
            self.assertEqual(rc, 0, out)
            self.assertTrue((Path(d) / "ai_docs" / "vision" / "V.md").is_file())
            self.assertTrue((src / "vision" / "V.md").is_file(),
                            "the old root is what makes this reversible: it stays")

    def test_references_are_rewritten_in_the_copy_only(self):
        with tempfile.TemporaryDirectory() as d:
            src = seed(d)
            run(d, "--from", "mkt_docs", "--apply")
            new = (Path(d) / "ai_docs" / "vision" / "V.md").read_text(encoding="utf-8")
            old = (src / "vision" / "V.md").read_text(encoding="utf-8")
            self.assertIn("ai_docs/strategy/O.md", new)
            self.assertNotIn("mkt_docs/", new)
            self.assertIn("mkt_docs/strategy/O.md", old,
                          "the source is left exactly as it was, or the move is not undoable")

    def test_files_outside_the_docs_roots_are_reported_and_never_touched(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d)
            pointer = Path(d) / "CLAUDE.md"
            body = "# protocol\n\nMust-reads: `mkt_docs/README.md`.\n"
            pointer.write_text(body, encoding="utf-8")
            rc, out = run(d, "--from", "mkt_docs", "--apply")
            self.assertEqual(rc, 0, out)
            self.assertIn("CLAUDE.md", out)
            self.assertIn("NOT touched", out)
            self.assertEqual(pointer.read_text(encoding="utf-8"), body,
                             "protocol pointers are user-authored: a tool that rewrites "
                             "them is the one thing init has always refused to do")

    def test_both_roots_validate_the_same_after_the_move(self):
        """The point of keeping the old root: you can compare, not just hope."""
        with tempfile.TemporaryDirectory() as d:
            docs = seed(d, "mkt_docs")
            (docs / "README.md").write_text("# reading guide\n", encoding="utf-8")
            run(d, "--from", "mkt_docs", "--apply")
            outs = []
            for name in ("mkt_docs", "ai_docs"):
                buf = io.StringIO()
                with redirect_stdout(buf):
                    sdlc_core.main(["validate", "--root", str(d), "--docs-dir", name])
                outs.append(buf.getvalue().replace(name, "<ROOT>"))
            self.assertEqual(outs[0], outs[1],
                             "same corpus, two roots, one verdict -- otherwise the move "
                             "changed the project instead of relocating it")


if __name__ == "__main__":
    unittest.main(verbosity=1)
