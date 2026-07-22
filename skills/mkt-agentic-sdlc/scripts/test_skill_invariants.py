#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static skill-invariant battery -- the deterministic release gate.

Asserts the skill's OWN doctrine invariants: the load-bearing rules are present
in SKILL.md and the support files, every support file is wired, the parseable
template formats the validator depends on still exist, and the behavioral driver
is zero-LLM. Stdlib only, zero-LLM, zero-network, zero-subprocess -- a failing
eval is always a real regression, never flakiness. Runs via
`python -m unittest discover -s scripts -p "test_*.py"`.
"""
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# file sits at skills/mkt-agentic-sdlc/scripts/ -> parents[1] = skill dir.
SKILL_DIR = Path(__file__).resolve().parents[1]


def read(rel):
    return (SKILL_DIR / rel).read_text(encoding="utf-8", errors="replace")


class SkillInvariants(unittest.TestCase):

    # ---- the three engineered guarantees (SKILL.md) ----

    def test_three_guarantees_declared(self):
        t = read("SKILL.md")
        self.assertIn("Evidence ledger", t)
        self.assertIn("Mechanical validation", t)
        self.assertIn("Adversarial CMO review", t)
        self.assertIn("The Three Engineered Guarantees", t)

    def test_honesty_contract(self):
        """No guaranteed-success claim; the guarantee is process rigor."""
        t = read("SKILL.md")
        self.assertIn("Honesty Contract", t)
        self.assertIn("process rigor", t)

    def test_triage_levels(self):
        t = read("SKILL.md")
        for level in ("E1", "E2", "E3", "Research Spike"):
            self.assertIn(level, t)
        # E2 without strategy context escalates to E3
        self.assertIn("escalate", t.lower())

    def test_dual_mode(self):
        t = read("SKILL.md")
        self.assertIn("Full Standalone", t)
        self.assertIn("Hybrid", t)
        self.assertIn("mkt_docs", t)

    # ---- elicitation invariants ----

    def test_elicitation_only_owned_facts(self):
        t = read("elicitation.md")
        self.assertIn("only what the user uniquely owns", t)
        # analysis is the skill's job, not the user's
        self.assertIn("comes from research", read("SKILL.md"))

    def test_elicitation_preauthorize_dont_know(self):
        """M1 calibration: pre-authorize 'I don't know' on numeric asks."""
        t = read("elicitation.md")
        self.assertIn("Pre-authorize", t)
        self.assertIn("non lo so", t)

    def test_elicitation_wave_cap(self):
        self.assertIn("4 questions per round", read("elicitation.md"))

    # ---- research / ledger invariants ----

    def test_ledger_classes(self):
        t = read("research.md")
        for cls in ("FACT", "BENCHMARK", "ASSUMPTION"):
            self.assertIn(cls, t)
        self.assertIn("two-source", t.lower().replace(" ", "-")
                      if "two-source" in t else "Two-source rule")

    def test_research_url_not_docpointer(self):
        """M1 calibration: a BENCHMARK Source must be a real URL, not a pointer
        to one of the agent's own research docs."""
        t = read("research.md")
        # assert on wrap-stable tokens, not a phrase that spans a line break
        self.assertIn("is not a source", t)
        self.assertIn("has no `http`", t)

    # ---- review red-flags (incl. M1 calibrations) ----

    def test_review_swap_test_published_statement(self):
        """M1 calibration on R1: test the PUBLISHED statement, not a paraphrase."""
        t = read("review.md")
        self.assertIn("Swap test", t)
        self.assertIn("PUBLISHED", t)

    def test_review_low_cost_trap(self):
        """M1 calibration R11b."""
        t = read("review.md")
        self.assertIn("Low-cost trap", t)
        self.assertIn("price-led", t)

    def test_review_strawman_swap(self):
        """M1 calibration R15."""
        t = read("review.md")
        self.assertIn("Strawman swap-test", t)

    def test_review_conformance_statement(self):
        t = read("review.md")
        self.assertIn("not valid on \"found nothing\"", t)

    # ---- frameworks ----

    def test_frameworks_sostac_and_swap(self):
        t = read("frameworks.md")
        self.assertIn("SOSTAC", t)
        self.assertIn("Swap test", t)
        self.assertIn("Dunford", t)

    def test_frameworks_salesled_funnel(self):
        """M2 calibration: sales-led/B2B funnel guidance (funnel output = demos
        not closed customers; separate pipeline table for the sales funnel)."""
        t = read("frameworks.md")
        self.assertIn("Sales-led / B2B funnel", t)
        self.assertIn("build-up table", t)   # wrap-stable token

    # ---- parseable template formats the validator depends on ----

    def test_template_parseable_formats(self):
        """The validator parses these exact tokens; templates.md must keep them
        or mkt_check + templates drift (documented coupling)."""
        t = read("templates.md")
        self.assertIn("Total budget:", t)
        self.assertIn("Budget Allocation", t)
        self.assertIn("Funnel Model", t)
        self.assertIn("### O1", t)          # objective heading id form
        self.assertIn("| ID | Claim | Class", t)  # ledger table header

    def test_template_situation_swot(self):
        """M1 calibration: SITUATION_SWOT template exists."""
        self.assertIn("SITUATION_SWOT.md", read("templates.md"))

    def test_template_enabler_row(self):
        """M1 calibration: enabler-row (budget 0) convention documented."""
        t = read("templates.md")
        self.assertIn("Enabler-row convention", t)

    # ---- support files wired (anti-orphan) ----

    def test_support_files_wired(self):
        skill_md = read("SKILL.md")
        expected = ["frameworks.md", "elicitation.md", "research.md",
                    "templates.md", "review.md", "ENFORCEMENT.md",
                    "scripts/mkt_check.py"]
        for rel in expected:
            self.assertTrue((SKILL_DIR / rel).is_file(),
                            f"expected support file missing: {rel}")
            self.assertIn(Path(rel).name, skill_md,
                          f"support file not referenced in SKILL.md: {rel}")
        for p in SKILL_DIR.glob("*.md"):
            if p.name == "SKILL.md":
                continue
            self.assertIn(p.name, skill_md,
                          f"orphan support file (exists, not referenced): {p.name}")

    def test_enforcement_pre_delivery_gate(self):
        t = read("ENFORCEMENT.md")
        self.assertIn("mkt_check.py check", t)
        self.assertIn("Skill self-test", t)

    # ---- behavioral driver is zero-LLM ----

    def test_behavioral_driver_no_llm(self):
        p = SKILL_DIR / "evals" / "run_behavioral.py"
        if not p.is_file():
            self.skipTest("behavioral driver not present yet")
        src = p.read_text(encoding="utf-8")
        forbidden = ["subprocess", "os.system", "eval(", "exec(", "urllib",
                     "http", "requests", "openai", "anthropic", "socket"]
        for tok in forbidden:
            self.assertNotIn(tok, src, f"driver must not reference {tok}")


if __name__ == "__main__":
    unittest.main()
