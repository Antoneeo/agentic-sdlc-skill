#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-074 regression: a Vision is born from the owner interview.

Field case (2026-10, a Hybrid milestone): the author wrote the M-VISION alone from
one sentence and a spike, taking elicitation's skip path. It imported a product-
Vision constraint as a ban, dropped the north star and the actor holding the
initiative; the blind check passed three rounds because it tests whether rules
hold, not whether they are the owner's. Four downstream artifacts were built on it.

This file replays that case against the doctrine (red under the pre-F-074 text:
the skip path covered a Vision, bootstrap reconstructed one, no north-star gate)
and keeps its behavioral scenario from being gutted. Code lens only: the scenario
cites this lens's fixture shape."""
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))
import sdlc_core as sc  # noqa: E402

SCENARIO = SKILL_DIR / "evals" / "scenarios" / "vision_needs_owner_interview.md"


def read(rel):
    return sc.read_text(SKILL_DIR / rel)


class VisionInterviewRegression(unittest.TestCase):

    def test_skip_path_cannot_cover_a_vision(self):
        """The M151 shortcut: 'spec already complete' from a sentence + a spike."""
        e = read("elicitation.md")
        skip = e.split("Skip path:", 1)[1].split("Unattended path:", 1)[0]
        self.assertIn("never covers a Vision", skip)
        self.assertIn("`vision.md` §The owner interview", skip)
        self.assertIn("plus a spike", skip)

    def test_no_vision_text_before_the_north_star(self):
        v = read("vision.md")
        sec = v.split("## The owner interview", 1)[1].split("\n## 0.", 1)[0]
        for anchor in ("Gate 1", "Gate 2", "no skip path", "in the owner's words",
                       "Without it no Vision text is written", "initiative",
                       "starting value", "provenance", "Non-Goal bounds scope",
                       "survive a hostile reader"):
            self.assertIn(anchor, sec, f"owner interview section missing {anchor!r}")
        # the six questions, in order
        pos = [sec.index(q) for q in ("**Problem**", "**Benefit**", "**Actors**",
                                      "**Success**", "**Boundaries**",
                                      "**Known constraints**")]
        self.assertEqual(pos, sorted(pos), "the interview questions are out of order")
        self.assertIn("cannot see whether they are the owner's", v,
                      "the blind check must say what it cannot detect")

    def test_bootstrap_never_reconstructs_a_vision(self):
        s = read("SKILL.md")
        self.assertIn("never a Vision reconstructed by the agent", s)
        self.assertNotIn("the three `vision/` docs (`Status: DRAFT`)", s)
        self.assertNotIn("reconstructed by the agent, NOT a gating authority",
                         read("templates.md"))

    def test_hybrid_m_vision_is_interviewed(self):
        """The field case was an M-VISION: the Hybrid gate must name the interview."""
        gate = read("SKILL.md").split("### 2. Vision Gate", 1)[1].split("### 3.", 1)[0]
        hybrid = gate.split("Hybrid:", 1)[1]
        self.assertIn("M-VISION is born from the owner interview", hybrid)

    def test_scenario_keeps_its_teeth(self):
        sys.path.insert(0, str(SKILL_DIR / "evals"))
        import run_behavioral as rb  # noqa: E402
        s = rb.load_scenario(str(SCENARIO))
        crit = s["pass_criteria"]
        bullets = [ln for ln in crit.splitlines() if ln.strip().startswith("-")]
        self.assertGreaterEqual(len(bullets), 6, "pass criteria gutted")
        for must in ("No Vision text", "skip path", "initiative",
                     "starting value", "provenance", "north star"):
            self.assertIn(must, crit, f"scenario no longer asserts {must!r}")
        self.assertIn("SPIKE_", s["setup"], "the spike is the shortcut's other half")


if __name__ == "__main__":
    unittest.main()
