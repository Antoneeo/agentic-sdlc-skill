#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-046 battery — the per-turn `remind` line, shared spine contract.

The carrier was kb's (F-041 item B) and is now every lens's, so the MECHANICAL
half of its contract is guarded here, once, for all three: one constant line,
under the cap, zero reads, and it can never break a prompt. What stays
lens-local is what only that lens can assert — kb keeps its own anchors and its
own banned-jargon list in `test_kb_remind.py`.

Why a cap and why constant: this line is injected on EVERY user prompt, so its
cost is paid on trivial turns too. That is admissible only because the owner
accepted it explicitly (`vision/rulings.md` r19, the "no ceremony ratchet"
Non-Goal's second door) — and the acceptance was for a FLAT cost. A line that
reads the repo, the session or the clock spends an unbounded amount of someone
else's context every turn and silently widens what was accepted.

    python scripts/test_remind.py
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

import sdlc_core  # noqa: E402

HERE = Path(__file__).resolve().parent
ENTRY = HERE / sdlc_core.entry_script()
REMIND_CAP = 500


def run(argv):
    """Run the lens CLI in-process, capturing stdout; SystemExit never escapes."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            mod = __import__(ENTRY.stem)
            rc = mod.main(argv)
        except SystemExit as e:
            rc = e.code if isinstance(e.code, int) else 1
    return rc, buf.getvalue()


class RemindContract(unittest.TestCase):

    def test_one_line_exit_zero(self):
        rc, out = run(["remind"])
        self.assertEqual(rc, 0)
        body = out.strip()
        self.assertTrue(body, "remind printed nothing")
        self.assertNotIn("\n", body, "the reminder must be exactly one line")

    def test_under_the_cap(self):
        _, out = run(["remind"])
        self.assertLessEqual(
            len(out.strip()), REMIND_CAP,
            "the per-turn line is paid on every prompt: the owner accepted a flat "
            "cost, and this cap is what keeps it flat")

    def test_it_names_the_load_duty(self):
        # The line exists because an unread protocol cannot be applied (F-046,
        # measured: a release ran against a guide the session never consulted).
        # A lens payload that drops this duty removes the reason for the hook.
        _, out = run(["remind"])
        low = out.strip().lower()
        self.assertIn("load", low)
        self.assertIn("skill", low + sdlc_core.profile()["skill_name"])

    def test_it_carries_the_lens_name(self):
        _, out = run(["remind"])
        self.assertIn(sdlc_core.profile()["skill_name"], out)

    def test_byte_stable_across_garbage_argv(self):
        # Constant by contract: a hook must never break a prompt, and a stray
        # flag must cost nothing.
        _, base = run(["remind"])
        for argv in (["remind", "--bogus", "x"],
                     ["remind", "--root", str(HERE / "no-such-dir-anywhere")],
                     ["remind", "extra", "junk", "--", "-q"]):
            rc, out = run(argv)
            self.assertEqual(rc, 0, argv)
            self.assertEqual(out, base, argv)

    def test_byte_stable_across_cwd(self):
        # Zero reads, proved from outside: two different working directories
        # cannot change one byte of the line.
        _, base = run(["remind"])
        outs = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as cwd:
                r = subprocess.run([sys.executable, str(ENTRY), "remind"],
                                   capture_output=True, text=True, cwd=cwd)
                self.assertEqual(r.returncode, 0, r.stderr)
                outs.append(r.stdout)
        self.assertEqual(outs[0], outs[1])
        self.assertEqual(outs[0].strip(), base.strip())

    def test_cli_intercepts_before_argparse(self):
        r = subprocess.run([sys.executable, str(ENTRY), "remind", "--bogus"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(r.stdout.strip())
        self.assertNotIn("usage:", r.stderr.lower())


if __name__ == "__main__":
    unittest.main()
