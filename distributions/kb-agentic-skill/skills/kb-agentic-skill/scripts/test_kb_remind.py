#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-041 battery — the per-turn `remind` line (item B).

kb-ONLY module, deliberately outside the shared manifest (the F-039 precedent:
kb-only doctrine, kb-only vehicle). The contract under guard is FS-B of
ANALYSIS_kb_midsession_drift.md: one constant, self-contained line that re-arms
the kb minimum every prompt when a project opts in via UserPromptSubmit —
and can NEVER break a prompt (exit 0, garbage-argv-proof, zero reads).

    python scripts/test_kb_remind.py
"""
import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_check as kc  # noqa: E402

HERE = Path(__file__).resolve().parent


def run_remind(argv):
    """Run the overlay main() capturing stdout; never let SystemExit escape."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            rc = kc.main(argv)
        except SystemExit as e:
            rc = e.code if isinstance(e.code, int) else 1
    return rc, buf.getvalue()


class RemindContractTests(unittest.TestCase):

    def test_one_line_exit_zero(self):
        rc, out = run_remind(["remind"])
        self.assertEqual(rc, 0)
        body = out.strip()
        self.assertTrue(body, "remind printed nothing")
        self.assertNotIn("\n", body, "the reminder must be exactly one line")

    def test_length_cap(self):
        _, out = run_remind(["remind"])
        self.assertLessEqual(len(out.strip()), 500)

    def test_byte_stable_across_garbage_argv_and_roots(self):
        # Constant by contract: a hook must never break a prompt, and zero
        # filesystem reads means a nonexistent root cannot change the output.
        _, base = run_remind(["remind"])
        for argv in (["remind", "--bogus", "x"],
                     ["remind", "--root", str(HERE / "no-such-dir-anywhere")],
                     ["remind", "extra", "junk", "--", "-q"]):
            rc, out = run_remind(argv)
            self.assertEqual(rc, 0, argv)
            self.assertEqual(out, base, argv)

    def test_byte_stable_across_cwd(self):
        # The FS promises stability across cwd too: the real CLI from two
        # different working directories must print the identical line.
        _, base = run_remind(["remind"])
        outs = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as cwd:
                r = subprocess.run(
                    [sys.executable, str(HERE / "sdlc_check.py"), "remind"],
                    capture_output=True, text=True, cwd=cwd)
                self.assertEqual(r.returncode, 0, r.stderr)
                outs.append(r.stdout)
        self.assertEqual(outs[0], outs[1])
        self.assertEqual(outs[0].strip(), base.strip())

    def test_self_contained_anchors(self):
        # The distill lesson: the line says WHAT TO DO with real referents — an
        # agent that read nothing else must find the triage levels, the index
        # path, the claim currency and the capture moment in the line itself.
        _, out = run_remind(["remind"])
        low = out.lower()
        # F-043: the payload is the one revision-clause carrier outside the
        # DRY pin's file set, so its own battery guards BOTH halves of the
        # gesture ("re-read" and "never append").
        for anchor in ("l1", "l2", "l3", "spike", "topics/index.md", "claim",
                       "re-read", "never append"):
            self.assertIn(anchor, low)

    def test_no_skill_internal_jargon(self):
        # Words meaningless without having read the skill files are banned —
        # the distill payload battery's rule, re-instantiated for kb.
        _, out = run_remind(["remind"])
        low = out.lower()
        for banned in ("doctrine", "payload", "descend", "taxonomy",
                       "distill", "provenance", "elicitation"):
            self.assertNotIn(banned, low)

    def test_cli_wiring(self):
        # The real CLI must intercept `remind` before the overlay argparse:
        # a stray flag must not produce an argparse usage error on stderr.
        r = subprocess.run(
            [sys.executable, str(HERE / "sdlc_check.py"), "remind", "--bogus"],
            capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(r.stdout.strip())
        self.assertNotIn("usage:", r.stderr.lower())

    def test_help_lists_remind(self):
        rc, out = run_remind(["--help"])
        self.assertEqual(rc, 0)
        self.assertIn("remind", out)


if __name__ == "__main__":
    unittest.main()
