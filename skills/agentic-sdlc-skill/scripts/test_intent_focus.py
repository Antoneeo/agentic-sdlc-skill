#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-071 regression: effort is weighed against the value and risk it serves.

Two field cases. F-063/F-064 (2026-10-04) passed every gate and dropped the
owner's "why": no conformance row carried the owner's outcome, and the benefit
was measured after the code with a rubric that never asked why. The F-072/F-074
session (2026-10-18) ran reviews where nothing was left to judge: an optional L2
review the owner stopped, and a whole closure review on a delta whose bump and
CHANGELOG part only restated reviewed work.

This file pins the doctrine that rules both (red under the pre-F-071 text) and
the benefit report's treatment of a NOT DUE row. Code lens only: the promise
probe lives in this lens's Execute-Before-Specify. The cold-agent replay is
ai_docs/solutions/harness_intent_focus/BEHAVIOR_CASES.md in the source repo."""
import contextlib
import io
import re
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))
import sdlc_core as sc  # noqa: E402


def read(rel):
    return re.sub(r"\s+", " ", sc.read_text(SKILL_DIR / rel))


class IntentFocusRegression(unittest.TestCase):

    def test_owner_outcome_is_a_weighed_conformance_row(self):
        """F-063: 25 conformance rows, none naming the owner's why."""
        r = read("review.md")
        self.assertRegex(r, r"each outcome the owner named .{0,140}is a row too, "
                            r"weighed by effort")
        self.assertIn("served by a minor share while a secondary concern takes "
                      "the bulk, is a finding", r)
        self.assertIn("every entry widening scope", r)
        self.assertIn("approved north star", r)

    def test_promise_probe_before_code_from_the_owners_words(self):
        """F-063: benefit measured after code; framed as a capability."""
        s = read("SKILL.md")
        self.assertRegex(s, r"owner's words for an outcome .{0,80}name a comparative "
                            r"effect.{0,200}built before code, asks the question the "
                            r"outcome names, and is shown red on the baseline")
        self.assertIn("How the author frames the unit (a new capability, a fix) "
                      "does not exempt it", s)
        r = read("review.md")
        self.assertIn("In the lens whose `SKILL.md` defines Execute-Before-Specify", r)

    def test_level_two_review_has_a_trigger(self):
        """The --open fix: 'optional' with no criterion, so the agent ran it."""
        r = read("review.md")
        self.assertNotIn("the L2 closure review is optional", r)
        self.assertIn("it is due only on a security-sensitive area the lens's Rule "
                      "Zero names, or at the owner's request, and otherwise does not "
                      "run and logs no row", r)

    def test_restating_delta_is_not_due_and_the_list_is_closed(self):
        """The F-074 delta: bump and CHANGELOG restated reviewed work."""
        r = read("review.md")
        sec = r.split("A delta after a PASS reopens a review only where it changes "
                      "what was judged", 1)[1].split("The agent review comes first", 1)[0]
        for anchor in ("version numbers and release metadata",
                       "regenerated indexes and audit-mark records",
                       "copies of a shared file that a tool verifies identical",
                       "CHANGELOG lines that state nothing the reviewed artifacts do "
                       "not already state",
                       "The list is closed and content governs it",
                       "a change answering a review finding is never in it",
                       "a failing check makes the delta judged work",
                       "`NOT DUE:", "`none (not due)`"):
            self.assertIn(anchor, sec)
        # judged kinds stay reviewed: the F-074 delta's real findings lived there
        for judged in ("README or overview prose", "an E2E script", "a rulings row"):
            self.assertIn(judged, sec)

    def test_benefit_counts_not_due_rows_apart(self):
        log = ("# Independent Review Log\n\n"
               "| date | doc_key | tier | model | reviewer | findings_raised | "
               "findings_real | verdict | revise_rounds |\n"
               "|---|---|---|---|---|---|---|---|---|\n"
               "| 2026-10-18 | ANALYSIS_x.md | closure | deep | subagent | 2 | 2 | "
               "PASS | 2 |\n"
               "| 2026-10-18 | ANALYSIS_x.md delta | closure | none (not due) | not run "
               "| 0 | 0 | NOT DUE: bump, CHANGELOG; batteries green | 0 |\n")
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p = root / sc.review_log_rel()
            p.parent.mkdir(parents=True)
            p.write_text(log, encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rc = sc.cmd_benefit(root)
        text = out.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("reviews ruled not due (logged, counted in no figure below): 1", text)
        self.assertIn("reviews with a stated moment: 1", text)
        self.assertNotIn("inconclusive", text)


if __name__ == "__main__":
    unittest.main()
