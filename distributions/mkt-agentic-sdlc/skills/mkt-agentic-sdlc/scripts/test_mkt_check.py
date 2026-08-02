#!/usr/bin/env python3
"""Deterministic tests for mkt_check.py — fixture project built in a tempdir."""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mkt_check  # noqa: E402


LEDGER = """# Evidence Ledger

| ID | Claim | Class | Value / Range | Source | Date | Confidence |
|---|---|---|---|---|---|---|
| EV-01 | monthly marketing budget | FACT | 15000 EUR | user, Wave 1 | 2026-01-01 | HIGH |
| EV-02 | industry close rate | BENCHMARK | 20% | https://example.com/report | 2025-11-01 | MED |
| EV-03 | organic reach growth | ASSUMPTION | 5-10% monthly | reasoning: early-stage account | 2026-01-01 | MED |
| EV-04 | search CPC for niche | BENCHMARK | 1.50 EUR | https://example.com/cpc | 2026-02-01 | HIGH |
| EV-05 | landing CVR | BENCHMARK | 3% | https://example.com/cvr | 2026-02-01 | MED |
"""

VISION = """---
description: Marketing vision for the fixture business.
status: CURRENT
---
# Marketing Vision
Status: APPROVED (by user, 2026-01-01)

## Business Goal
Grow with budget [EV-01].
"""

OBJECTIVES = """---
description: SMART objectives.
status: CURRENT
---
# Objectives
Status: APPROVED (by user, 2026-01-02)

### O1 — Lead generation
- **Target:** 24 customers by 2026-06-30 [EV-01]

### O2 — Organic presence
- **Target:** grow reach [EV-03]
"""

TACTICAL = """---
description: Channel plan, budget, funnel.
status: CURRENT
---
# Tactical Plan

Total budget: 15000

## Channel Plan
| Channel | Objective | KPI | Budget | Owner |
|---|---|---|---|---|
| Google Ads | O1 | CPL <= 30 [EV-04] | 6000 | founder |
| Content | O2 | posts/week | 9000 | founder |

## Budget Allocation
| Channel | Budget | Share |
|---|---|---|
| Google Ads | 6000 | 40% |
| Content | 9000 | 60% |

## Funnel Model
| Channel | Budget | CPC | Clicks | CVR % | Leads | Close % | Customers | CAC |
|---|---|---|---|---|---|---|---|---|
| Google Ads | 6000 | 1.50 [EV-04] | 4000 | 3 [EV-05] | 120 | 20 [EV-02] | 24 | 250 |
"""

MEASUREMENT = """---
description: KPI tree and kill/scale criteria.
status: CURRENT
---
# Measurement Plan

## KPI table
| Objective | KPI | Target | Benchmark | Cadence |
|---|---|---|---|---|
| O1 | CPL | <= 30 | [EV-04] | weekly |
| O2 | reach | +5%/month | [EV-03] | monthly |

## Kill / scale criteria
| Channel | Kill if | Scale if |
|---|---|---|
| Google Ads | CAC > 400 after 3000 spent | CAC < 200 at 2x volume |
"""


class MktCheckTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.docs = self.root / "mkt_docs"
        self.write("research/evidence_ledger.md", LEDGER)
        self.write("vision/MKT_VISION.md", VISION)
        self.write("strategy/OBJECTIVES.md", OBJECTIVES)
        self.write("tactics/TACTICAL_PLAN.md", TACTICAL)
        self.write("tactics/MEASUREMENT_PLAN.md", MEASUREMENT)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, content):
        p = self.docs / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def run_cmd(self, *argv):
        return mkt_check.main(list(argv) + ["--root", str(self.root)])

    # ---------------- clean fixture

    def test_clean_project_check_passes(self):
        self.assertEqual(self.run_cmd("index"), 0)
        self.assertEqual(self.run_cmd("check"), 0)

    def test_index_lists_canonical_docs(self):
        self.run_cmd("index")
        index = (self.docs / "INDEX.md").read_text(encoding="utf-8")
        self.assertIn("vision/MKT_VISION.md", index)
        self.assertIn("tactics/TACTICAL_PLAN.md", index)
        self.assertNotIn("evidence_ledger", index)  # research/ not canonical

    # ---------------- budget

    def test_budget_mismatch_fails(self):
        self.write("tactics/TACTICAL_PLAN.md", TACTICAL.replace("| Google Ads | 6000 | 40% |",
                                                                "| Google Ads | 5000 | 40% |"))
        self.assertEqual(self.run_cmd("budget"), 1)

    def test_budget_total_line_missing_fails(self):
        self.write("tactics/TACTICAL_PLAN.md", TACTICAL.replace("Total budget: 15000", ""))
        self.assertEqual(self.run_cmd("budget"), 1)

    # ---------------- funnel

    def test_funnel_broken_customers_fails(self):
        broken = TACTICAL.replace("| 20 [EV-02] | 24 | 250 |", "| 20 [EV-02] | 50 | 250 |")
        self.write("tactics/TACTICAL_PLAN.md", broken)
        self.assertEqual(self.run_cmd("funnel"), 1)

    def test_funnel_clean_passes(self):
        self.assertEqual(self.run_cmd("funnel"), 0)

    # ---------------- ledger

    def test_unresolved_ev_reference_fails(self):
        self.write("strategy/OBJECTIVES.md", OBJECTIVES + "\nGhost number [EV-99].\n")
        self.assertEqual(self.run_cmd("ledger"), 1)

    def test_benchmark_without_url_fails(self):
        bad = LEDGER.replace("https://example.com/report", "some analyst said so")
        self.write("research/evidence_ledger.md", bad)
        self.assertEqual(self.run_cmd("ledger"), 1)

    def test_fact_sourced_to_our_own_document_fails(self):
        # The laundering path a cold-agent field test walked (2026-08-02): a researched
        # observation classed FACT, pointed at one of our own documents. BENCHMARK would
        # have owed a URL; FACT is the one class the URL rule never reached.
        # One branch per test: the field-test row tripped both at once, so either branch
        # could have been deleted with the suite still green.
        bad = LEDGER.replace("| user, Wave 1 |", "| VoC sweep, research/VOC.md |")
        self.write("research/evidence_ledger.md", bad)
        self.assertEqual(self.run_cmd("ledger"), 1)

    def test_fact_sourced_by_pointing_elsewhere_fails(self):
        bad = LEDGER.replace("| user, Wave 1 |", "| see the VoC sweep |")
        self.write("research/evidence_ledger.md", bad)
        self.assertEqual(self.run_cmd("ledger"), 1)

    def test_fact_without_a_source_fails(self):
        bad = LEDGER.replace("| user, Wave 1 |", "|  |")
        self.write("research/evidence_ledger.md", bad)
        self.assertEqual(self.run_cmd("ledger"), 1)

    def test_fact_from_the_client_still_passes(self):
        # The rule must not make FACT unusable: it is the one class with no URL,
        # precisely because the client is the origin — including when what they handed
        # over is a Markdown file.
        for src in ("user, Wave 1: Stripe export",
                    "client, onboarding_brief.md",
                    "owner, see their CRM export"):
            with self.subTest(source=src):
                self.write("research/evidence_ledger.md",
                           LEDGER.replace("| user, Wave 1 |", f"| {src} |"))
                self.assertEqual(self.run_cmd("ledger"), 0)

    def test_assumption_without_confidence_fails(self):
        bad = LEDGER.replace(
            "| EV-03 | organic reach growth | ASSUMPTION | 5-10% monthly | reasoning: early-stage account | 2026-01-01 | MED |",
            "| EV-03 | organic reach growth | ASSUMPTION | 5-10% monthly | reasoning: early-stage account | 2026-01-01 | |")
        self.write("research/evidence_ledger.md", bad)
        self.assertEqual(self.run_cmd("ledger"), 1)

    # ---------------- trace

    def test_orphan_tactic_fails(self):
        self.write("tactics/TACTICAL_PLAN.md", TACTICAL.replace("| Google Ads | O1 |",
                                                                "| Google Ads | O9 |"))
        self.assertEqual(self.run_cmd("trace"), 1)

    def test_objective_without_kpi_row_fails(self):
        trimmed = MEASUREMENT.replace("| O2 | reach | +5%/month | [EV-03] | monthly |\n", "")
        self.write("tactics/MEASUREMENT_PLAN.md", trimmed)
        self.assertEqual(self.run_cmd("trace"), 1)

    def test_tactic_without_objective_token_fails(self):
        self.write("tactics/TACTICAL_PLAN.md", TACTICAL.replace("| Content | O2 |",
                                                                "| Content | tbd |"))
        self.assertEqual(self.run_cmd("trace"), 1)

    # ---------------- validate

    def test_missing_status_warns_strict_fails(self):
        no_fm = VISION.replace("status: CURRENT\n", "")
        self.write("vision/MKT_VISION.md", no_fm)
        self.run_cmd("index")
        self.assertEqual(self.run_cmd("validate"), 0)              # warning only
        self.assertEqual(self.run_cmd("validate", "--strict"), 1)  # strict fails

    def test_stale_index_warns(self):
        self.run_cmd("index")
        self.write("deliverables/ONE_PAGER.md",
                   "---\ndescription: x\nstatus: DRAFT\n---\n# One pager\n")
        self.assertEqual(self.run_cmd("validate", "--strict"), 1)

    # ---------------- helpers

    def test_parse_num(self):
        self.assertEqual(mkt_check.parse_num("6000"), 6000)
        self.assertEqual(mkt_check.parse_num("1.50 [EV-04]"), 1.5)
        self.assertEqual(mkt_check.parse_num("15k"), 15000)
        self.assertEqual(mkt_check.parse_num("1.2M"), 1200000)
        self.assertEqual(mkt_check.parse_num("40%"), 40)
        self.assertEqual(mkt_check.parse_num("EUR 6,000"), 6000)
        self.assertIsNone(mkt_check.parse_num(""))
        self.assertIsNone(mkt_check.parse_num("n/a"))


class CommandSurfaceTests(unittest.TestCase):
    """Every subcommand SKILL.md advertises must be recognized by mkt_check.py.

    Regression net for the dropped-`migrate` bug: SKILL.md documented the command
    while the entry point's hand-copied spine list rejected it with an argparse
    usage error (exit 2). `--help` on a recognized subcommand exits 0; an unknown
    one fails choice validation and exits 2.
    """

    SKILL_MD = Path(__file__).resolve().parents[1] / "SKILL.md"
    VALIDATOR = Path(__file__).resolve().parent / "mkt_check.py"

    def documented_commands(self):
        text = self.SKILL_MD.read_text(encoding="utf-8")
        line = next(l for l in text.splitlines()
                    if "mkt_check.py" in l and "validator" in l)
        return sorted(set(re.findall(r"`([a-z]+)`", line)))

    def test_skill_md_names_the_command_surface(self):
        cmds = self.documented_commands()
        self.assertIn("check", cmds, "SKILL.md validator line lost its command list")
        self.assertIn("migrate", cmds, "SKILL.md validator line lost the spine commands")

    def test_every_documented_subcommand_is_recognized(self):
        for cmd in self.documented_commands():
            proc = subprocess.run(
                [sys.executable, str(self.VALIDATOR), cmd, "--help"],
                capture_output=True, text=True)
            self.assertEqual(
                proc.returncode, 0,
                f"`mkt_check.py {cmd}` is documented in SKILL.md but the entry "
                f"point does not recognize it:\n{proc.stderr}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
