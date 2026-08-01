#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TS14/TS15/TS16/TS17 — the documentation root as a parameter.

`ai_docs/` stays the one surviving root and the default; the parameter exists so the
tools can READ a legacy root long enough to validate and migrate it. These tests hold
that line: the default path is untouched (TS1's job), an explicit answer always beats a
guessed one, an ambiguous tree gets no verdict at all, and the agent-global KB never
moves because a project renamed its docs directory.

    python scripts/test_docs_root.py
"""
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_check as sc  # noqa: E402
import sdlc_core  # noqa: E402


class DocsRootTestCase(unittest.TestCase):
    """The resolved name is per-invocation global state: always put it back."""

    def setUp(self):
        self.addCleanup(sdlc_core.set_docs_dir, sdlc_core.docs_dir())
        self._saved_env = os.environ.get(sdlc_core.DOCS_DIR_ENV)
        self.addCleanup(self._restore_env)

    def _restore_env(self):
        if self._saved_env is None:
            os.environ.pop(sdlc_core.DOCS_DIR_ENV, None)
        else:
            os.environ[sdlc_core.DOCS_DIR_ENV] = self._saved_env

    def seed(self, root, docs="ai_docs"):
        (Path(root) / docs / "solutions").mkdir(parents=True, exist_ok=True)
        (Path(root) / docs / "README.md").write_text("# reading guide\n", encoding="utf-8")
        return Path(root) / docs


class Args:
    def __init__(self, docs_dir=None, root=None):
        self.docs_dir = docs_dir
        self.root = root


class TS14ResolutionOrder(DocsRootTestCase):

    def test_default_is_ai_docs(self):
        with tempfile.TemporaryDirectory() as d:
            _, name = sdlc_core.resolve_docs_dir(Args(), d)
            self.assertEqual(name, "ai_docs", "a tree with no docs root at all is still ai_docs")

    def test_discovery_finds_a_legacy_root_without_a_flag(self):
        with tempfile.TemporaryDirectory() as d:
            self.seed(d, "mkt_docs")
            root, name = sdlc_core.resolve_docs_dir(Args(), d)
            self.assertEqual(name, "mkt_docs")
            self.assertEqual(Path(root), Path(d).resolve())

    def test_env_beats_discovery(self):
        with tempfile.TemporaryDirectory() as d:
            self.seed(d, "mkt_docs")
            os.environ[sdlc_core.DOCS_DIR_ENV] = "ai_docs"
            _, name = sdlc_core.resolve_docs_dir(Args(), d)
            self.assertEqual(name, "ai_docs")

    def test_flag_beats_env(self):
        with tempfile.TemporaryDirectory() as d:
            self.seed(d, "mkt_docs")
            os.environ[sdlc_core.DOCS_DIR_ENV] = "mkt_docs"
            _, name = sdlc_core.resolve_docs_dir(Args(docs_dir="ai_docs"), d)
            self.assertEqual(name, "ai_docs", "explicit beats guessed, like --hybrid")

    def test_the_env_is_read_now_not_at_import(self):
        """Or TS14 could not be written honestly, and CI could not vary it."""
        with tempfile.TemporaryDirectory() as d:
            os.environ[sdlc_core.DOCS_DIR_ENV] = "mkt_docs"
            _, first = sdlc_core.resolve_docs_dir(Args(), d)
            os.environ[sdlc_core.DOCS_DIR_ENV] = "ai_docs"
            _, second = sdlc_core.resolve_docs_dir(Args(), d)
            self.assertEqual((first, second), ("mkt_docs", "ai_docs"))

    def test_the_nearer_root_wins(self):
        with tempfile.TemporaryDirectory() as d:
            self.seed(d, "ai_docs")
            inner = Path(d) / "sub" / "project"
            self.seed(inner, "mkt_docs")
            _, name = sdlc_core.resolve_docs_dir(Args(), inner)
            self.assertEqual(name, "mkt_docs",
                             "levels are evaluated one at a time: the root you stand in wins")


class TS15AmbiguousRoot(DocsRootTestCase):

    def test_two_roots_at_one_level_refuse(self):
        with tempfile.TemporaryDirectory() as d:
            self.seed(d, "ai_docs")
            self.seed(d, "mkt_docs")
            with self.assertRaises(sdlc_core.AmbiguousDocsRoot) as ctx:
                sdlc_core.resolve_docs_dir(Args(), d)
            self.assertIn("ai_docs", str(ctx.exception))
            self.assertIn("mkt_docs", str(ctx.exception))

    def test_the_command_exits_without_printing_a_verdict(self):
        with tempfile.TemporaryDirectory() as d:
            self.seed(d, "ai_docs")
            self.seed(d, "mkt_docs")
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = sc.main(["validate", "--root", d])
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("refusing to guess", out)
            self.assertNotIn("Validation:", out,
                             "a half-migrated tree must get no verdict at all -- "
                             "a partial one reads as a whole one")

    def test_the_flag_resolves_the_ambiguity(self):
        with tempfile.TemporaryDirectory() as d:
            self.seed(d, "ai_docs")
            self.seed(d, "mkt_docs")
            buf = io.StringIO()
            with redirect_stdout(buf):
                sc.main(["validate", "--root", d, "--docs-dir", "mkt_docs"])
            self.assertIn("Validation:", buf.getvalue())

    def test_orient_stays_fail_open_on_an_ambiguous_tree(self):
        """The SessionStart hook must never block a session, not even here."""
        with tempfile.TemporaryDirectory() as d:
            self.seed(d, "ai_docs")
            self.seed(d, "mkt_docs")
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = sc.main(["orient", "--root", d])
            self.assertEqual(rc, 0)
            self.assertIn("[note]", buf.getvalue())


class TS16KbIsolation(DocsRootTestCase):

    def test_the_agent_global_kb_never_follows_the_project(self):
        """It is shared across lenses and clients: one project's rename cannot move it."""
        src = sc.read_text(Path(__file__).resolve().parent / "sdlc_core.py")
        self.assertIn('kb_root / "ai_docs" / "reference"', src)
        self.assertIn('DEFAULT_KB_ROOT / "ai_docs" / "reference"', src)
        sdlc_core.set_docs_dir("mkt_docs")
        self.assertEqual(sdlc_core.docs_dir(), "mkt_docs")
        # The KB paths above are literals precisely so this cannot drift; assert the
        # project helper does move, so the test is not vacuously true.
        self.assertTrue(str(sdlc_core.ai_path("/tmp")).endswith("mkt_docs"))


class TS17DerivedSurfaces(DocsRootTestCase):
    """Every surface that named the root by hand now names the resolved one."""

    def test_all_surfaces_follow_the_resolved_root(self):
        sdlc_core.set_docs_dir("mkt_docs")
        self.assertIn("mkt_docs/", sdlc_core.review_log_rel())
        self.assertTrue(all(rel.startswith("mkt_docs/") for _, rel in sdlc_core.orient_docs()))
        self.assertIn("mkt_docs/", sdlc_core.manifest_header())
        self.assertIn("mkt_docs/reference/", sdlc_core.guide_index_header())
        self.assertNotIn("ai_docs", sdlc_core.SKIP_DIRS,
                         "the docs root is excluded by resolved name, not by a frozen literal")

    def test_the_gate_exempts_the_resolved_root(self):
        """cmd_gate never blocks writes inside the docs tree -- whatever it is called."""
        with tempfile.TemporaryDirectory() as d:
            self.seed(d, "mkt_docs")
            target = Path(d) / "mkt_docs" / "solutions" / "ANALYSIS_x.md"
            target.write_text("# x\n", encoding="utf-8")
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = sc.main(["gate", "--root", d, "--file", str(target),
                              "--protected", "mkt_docs"])
            self.assertEqual(rc, 0, "the docs root must stay exempt after a rename")

    def test_generated_output_names_the_resolved_root(self):
        with tempfile.TemporaryDirectory() as d:
            docs = self.seed(d, "mkt_docs")
            (docs / "vision").mkdir(parents=True, exist_ok=True)
            (docs / "vision" / "project_vision.md").write_text(
                "---\ndescription: One line.\nstatus: CURRENT\n---\n# V\n\nStatus: APPROVED (owner)\n",
                encoding="utf-8")
            buf = io.StringIO()
            with redirect_stdout(buf):
                sc.main(["index", "--root", d, "--docs-dir", "mkt_docs"])
            manifest = (docs / "INDEX.md").read_text(encoding="utf-8")
            self.assertIn("mkt_docs/", manifest)
            self.assertNotIn("ai_docs/", manifest,
                             "a generated file that names the wrong root is a wrong instruction")


if __name__ == "__main__":
    unittest.main(verbosity=1)
