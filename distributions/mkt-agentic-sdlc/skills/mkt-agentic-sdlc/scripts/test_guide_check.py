#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-078 — the Phase-3 guide question leaves a record in the L3 ANALYSIS.

SKILL.md asks, while analyzing, whether a CURRENT guide covers what the change
touches and whether understanding it forced a model of a complex component no
guide covers. Until this unit nothing checked that the answer was written. Each
test names the mutation that turns it red.

    python scripts/test_guide_check.py

Standard library only.
"""
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_core as sc  # noqa: E402

EPOCH = sc.GUIDE_CHECK_EPOCH
BEFORE = "2026-10-23"   # the day the rule was written: grandfathered
FILLED = ("## Guide check\n"
          "- CURRENT guide covering this: none (router: no match).\n"
          "- Complex component without a guide: no.\n\n")


def setUpModule():
    global _SAVED_DOCS_DIR
    _SAVED_DOCS_DIR = sc.docs_dir()
    sc.set_docs_dir("ai_docs")


def tearDownModule():
    sc.set_docs_dir(_SAVED_DOCS_DIR)


def analysis(root, extra="", level="L3", start=EPOCH, domain="code"):
    sol = Path(root) / "ai_docs" / "solutions"
    sol.mkdir(parents=True, exist_ok=True)
    p = sol / "ANALYSIS_probe.md"
    p.write_text(
        f"---\ndescription: x\nstatus: PLANNED\nid: F-900\nstart_date: {start}\n"
        f"end_date:\nlevel: {level}\ndomain: {domain}\n---\n# Feature Analysis: probe\n\n"
        f"## Objective\n\nx\n\n{extra}## Diary / Current State\n\n**{start} — opened.** x\n",
        encoding="utf-8")
    return p


def advisories(root):
    buf = io.StringIO()
    with redirect_stdout(buf):
        sc.cmd_validate(Path(root))
    return [l for l in buf.getvalue().splitlines() if "Guide check" in l]


class GuideCheck(unittest.TestCase):

    def test_missing_section_is_an_advisory(self):
        """Mutation: drop the guide-check call from cmd_validate -> red."""
        with tempfile.TemporaryDirectory() as d:
            analysis(d)
            found = advisories(d)
            self.assertEqual(len(found), 1, found)
            self.assertTrue(found[0].startswith("[note]"), found[0])

    def test_filled_section_is_quiet(self):
        """Mutation: has_guide_check always False -> red."""
        with tempfile.TemporaryDirectory() as d:
            analysis(d, FILLED)
            self.assertEqual(advisories(d), [])

    def test_template_left_unfilled_still_warns(self):
        """A heading carrying only the template comment answers nothing.
        Mutation: check the heading alone -> red."""
        with tempfile.TemporaryDirectory() as d:
            analysis(d, "## Guide check\n<!-- two lines -->\n\n")
            self.assertEqual(len(advisories(d)), 1)

    def test_commented_heading_does_not_count(self):
        with tempfile.TemporaryDirectory() as d:
            analysis(d, "<!-- ## Guide check\n- a\n- b -->\n\n")
            self.assertEqual(len(advisories(d)), 1)

    def test_grandfathered_by_start_date(self):
        """Mutation: drop the epoch comparison -> the existing corpus lights up."""
        with tempfile.TemporaryDirectory() as d:
            analysis(d, start=BEFORE)
            self.assertEqual(advisories(d), [])

    def test_only_l3(self):
        with tempfile.TemporaryDirectory() as d:
            analysis(d, level="L2")
            self.assertEqual(advisories(d), [])

    def test_only_the_code_lens(self):
        """The question is agentic-sdlc doctrine; the sibling lenses do not ask it.
        Mutation: drop the domain test -> red in a kb/mkt/course analysis."""
        for domain in sorted(set(sc.DOMAINS) - {"code"}):
            with tempfile.TemporaryDirectory() as d:
                analysis(d, domain=domain)
                self.assertEqual(advisories(d), [], domain)

    def test_never_a_warning_even_strict(self):
        """Advisory, never warning: --strict stays green on a late upgrade."""
        with tempfile.TemporaryDirectory() as d:
            analysis(d, FILLED.replace("## Guide check", "## Notes"))
            buf = io.StringIO()
            with redirect_stdout(buf):
                sc.cmd_validate(Path(d), strict=True)
            lines = [l for l in buf.getvalue().splitlines() if "Guide check" in l]
            self.assertTrue(lines)
            self.assertTrue(all(l.startswith("[note]") for l in lines), lines)


if __name__ == "__main__":
    unittest.main()
