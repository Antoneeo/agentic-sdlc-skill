#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test battery for the `orient` subcommand (M4 Unit 1, SessionStart hook) in
sdlc_check.py.

Standard library only (unittest). Windows and POSIX compatible. Every fixture
is written to a fresh temp dir per test -- no shared mutable state, no real
filesystem side effects outside tempfile.TemporaryDirectory().

Covers the P-TM consolidation Unit-1 [MILESTONE] requirements:
  T1 zero-execution  -> test_zero_execution_side_effect
  T2 size bound      -> test_total_size_cap
  T3 confinement     -> test_path_confinement_applied
  T8 fail-open       -> test_missing_ai_docs_silent_exit0 / test_unreadable_doc_skipped
  no-dup (M-VISION)  -> test_hybrid_pointer_no_dup
"""
import os
import sys
import tempfile
import unittest
from io import StringIO
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_check as sc  # noqa: E402


def orient_args(root=None, hybrid=False):
    return SimpleNamespace(root=str(root) if root else None, hybrid=hybrid)


def run_orient(root=None, hybrid=False):
    """Run cmd_orient capturing stdout. Returns (rc, stdout)."""
    buf = StringIO()
    with redirect_stdout(buf):
        rc = sc.cmd_orient(orient_args(root=root, hybrid=hybrid))
    return rc, buf.getvalue()


def seed(root, rel, text):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


class OrientTests(unittest.TestCase):

    def test_missing_ai_docs_silent_exit0(self):
        # Fresh project, no ai_docs/ at all -> emit nothing, exit 0 (fail-open T8).
        with tempfile.TemporaryDirectory() as d:
            rc, out = run_orient(root=d)
            self.assertEqual(rc, 0)
            self.assertEqual(out.strip(), "")

    def test_all_sections_emitted(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d, "ai_docs/README.md", "README-BODY")
            seed(d, "ai_docs/INDEX.md", "INDEX-BODY")
            seed(d, "ai_docs/reference/INDEX.md", "ROUTER-BODY")
            seed(d, "ai_docs/audit/handoff.md", "HANDOFF-BODY")
            rc, out = run_orient(root=d)
            self.assertEqual(rc, 0)
            for label in ("Reading guide (README)", "Canonical manifest (INDEX)",
                          "Guide router (when-to-consult)", "Last session handoff"):
                self.assertIn(label, out)
            for body in ("README-BODY", "INDEX-BODY", "ROUTER-BODY", "HANDOFF-BODY"):
                self.assertIn(body, out)
            self.assertIn("Rule Zero", out)

    def test_partial_present_skips_missing(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d, "ai_docs/audit/handoff.md", "ONLY-HANDOFF")
            rc, out = run_orient(root=d)
            self.assertEqual(rc, 0)
            self.assertIn("ONLY-HANDOFF", out)
            self.assertNotIn("README-BODY", out)
            self.assertIn("Last session handoff", out)
            self.assertNotIn("Reading guide (README)", out)

    def test_total_size_cap(self):
        with tempfile.TemporaryDirectory() as d:
            # Four docs each at the per-doc cap -> total (24000) exceeds
            # ORIENT_MAX_TOTAL_CHARS. Fill with digits 4-7, which never appear
            # in the header/labels/notes/triage line (those use 1/2/3 only), so
            # counting them isolates the emitted DOC-BODY chars exactly.
            seed(d, "ai_docs/README.md", "4" * sc.ORIENT_PER_DOC_CHARS)
            seed(d, "ai_docs/INDEX.md", "5" * sc.ORIENT_PER_DOC_CHARS)
            seed(d, "ai_docs/reference/INDEX.md", "6" * sc.ORIENT_PER_DOC_CHARS)
            seed(d, "ai_docs/audit/handoff.md", "7" * sc.ORIENT_PER_DOC_CHARS)
            rc, out = run_orient(root=d)
            self.assertEqual(rc, 0)
            body_chars = sum(out.count(c) for c in "4567")
            self.assertLessEqual(body_chars, sc.ORIENT_MAX_TOTAL_CHARS)
            self.assertIn("truncated", out)

    def test_unreadable_doc_skipped(self):
        # A directory where a file path is expected -> read/stat path is not a
        # file -> skipped, no traceback, exit 0.
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "ai_docs").mkdir()
            (Path(d) / "ai_docs" / "README.md").mkdir()  # dir, not a file
            seed(d, "ai_docs/audit/handoff.md", "HANDOFF-OK")
            rc, out = run_orient(root=d)
            self.assertEqual(rc, 0)
            self.assertIn("HANDOFF-OK", out)
            self.assertNotIn("Reading guide (README)", out)

    def test_zero_execution_side_effect(self):
        # A doc containing shell-like payloads must be emitted as inert TEXT,
        # never executed (P-TM T1). Assert the sentinel file is not created.
        with tempfile.TemporaryDirectory() as d:
            sentinel = Path(d) / "PWNED"
            payload = "$(touch '%s'); `touch '%s'`; rm -rf /" % (sentinel, sentinel)
            seed(d, "ai_docs/README.md", payload)
            rc, out = run_orient(root=d)
            self.assertEqual(rc, 0)
            self.assertFalse(sentinel.exists(), "orient executed doc content -- T1 violated")
            self.assertIn("touch", out)  # payload surfaced as literal text

    def test_hybrid_pointer_no_dup(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d, "ai_docs/README.md", "README-BODY")
            rc, out = run_orient(root=d, hybrid=True)
            self.assertEqual(rc, 0)
            self.assertIn("devpnt_mcp_get_bootstrap", out)
            self.assertIn("devPNT active", out)
            # Must not attempt to replicate plan/KL content itself.
            self.assertNotIn("Master Plan\n", out)

    def test_no_hybrid_pointer_when_flag_off(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d, "ai_docs/README.md", "README-BODY")
            rc, out = run_orient(root=d, hybrid=False)
            self.assertEqual(rc, 0)
            self.assertNotIn("devpnt_mcp_get_bootstrap", out)

    def test_path_confinement_applied(self):
        # Every doc path must be routed through confine_under (T3). Monkeypatch
        # it to record the calls, then restore.
        with tempfile.TemporaryDirectory() as d:
            seed(d, "ai_docs/README.md", "README-BODY")
            calls = []
            real = sc.confine_under

            def spy(base, rel):
                calls.append(rel)
                return real(base, rel)

            sc.confine_under = spy
            try:
                rc, _ = run_orient(root=d)
            finally:
                sc.confine_under = real
            self.assertEqual(rc, 0)
            self.assertEqual(calls, [rel for _, rel in sc.ORIENT_DOCS])


if __name__ == "__main__":
    unittest.main()
