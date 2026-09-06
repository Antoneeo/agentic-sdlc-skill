#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-041 battery — the per-turn `remind` line (item B).

kb-ONLY module, deliberately outside the shared manifest (the F-039 precedent:
kb-only doctrine, kb-only vehicle). Since F-046 the MECHANICAL half of the
contract — one line, under the cap, zero reads, never breaks a prompt — is the
shared `test_remind.py`'s, because the carrier is now every lens's. What is left
here is what only this lens can assert: that the line names the kb referents an
agent who read nothing else can act on, and that it uses no word meaningless
without having read the skill.

    python scripts/test_kb_remind.py
"""
import contextlib
import io
import os
import sys
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

    def test_help_lists_remind(self):
        rc, out = run_remind(["--help"])
        self.assertEqual(rc, 0)
        self.assertIn("remind", out)


if __name__ == "__main__":
    unittest.main()
