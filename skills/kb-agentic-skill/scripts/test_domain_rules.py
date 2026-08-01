#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TS2/TS3/TS4/TS10/TS13 — the multi-domain rule layer.

What TS1 cannot cover: it freezes the behaviour on a tree that declares no domain,
which is the compatibility half. This battery asserts the other half — that a tree
which DOES declare domains is validated by the right rules, and that the answer does
not depend on which distribution asked.

    python scripts/test_domain_rules.py

Dev-only, like the other batteries: deliberately outside the package allowlist.
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

SKILL_DIR = Path(__file__).resolve().parent.parent

BODY_SECTIONS = """
## Objective
Do the thing the reader needs done.

## Feature Vision
Serves the project Vision's first goal.

## Impact
`src/thing.py` (new).

## Action Plan
- [ ] Do it.

## Test Strategy
One test per accepted input.

## Diary / Current State
- **2026-07-31 — started.**
"""

CODE_RISK = """
## Security and Threat Model
Surface: external input. Mitigation: size cap before parse.
"""

KNOWLEDGE_RISK = """
## Sources and Verification
- `specs/vendor_intake.pdf` — verified against the signed copy the client sent.
"""

MARKETING_RISK = """
## Threat Map / Plan Risks
The competitor may cut price before launch; the plan holds a discount reserve.
"""


def write(root, rel, text):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def analysis(fid, feature, risk, domain=None, checks=None, extra=""):
    front = [f"id: {fid}", f"feature: {feature}", "status: IN_PROGRESS",
             "level: L2", "start_date: 2026-07-31", "end_date:"]
    if domain:
        front.append(f"domain: {domain}")
    if checks:
        front.append("checks: [" + ", ".join(checks) + "]")
    return ("---\n" + "\n".join(front) + "\n---\n"
            + f"# Feature Analysis: {feature}\n" + BODY_SECTIONS + risk + extra)


def seed_project(root, readme_default=None):
    """The minimum a project needs for `validate` to reach the analyses."""
    front = f"---\ndefault_domain: {readme_default}\n---\n" if readme_default else ""
    write(root, "ai_docs/README.md", front + "# ai_docs — reading guide\n\nMust-reads.\n")
    for name, title in (("project_vision.md", "Project Vision"),
                        ("roadmap.md", "Roadmap"), ("principles.md", "Decision Principles")):
        write(root, f"ai_docs/vision/{name}",
              f"---\ndescription: One line.\nstatus: CURRENT\n---\n# {title}\n\nStatus: APPROVED (owner)\n")
    write(root, "ai_docs/audit/audit_plan.md",
          "# Audit Plan\n\n| Area | State | Reference | Notes |\n|---|---|---|---|\n| . | PENDING | - | - |\n")


def validate(root, strict=False):
    """Run the real command and return (rc, output).

    The generated indexes are rebuilt first: their staleness is TS1's subject, not
    this battery's, and leaving them missing would drown every domain finding under
    two unrelated errors."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        sc.cmd_index(Path(root))
        rc = sc.cmd_validate(Path(root), strict=strict)
    return rc, buf.getvalue()


def reindex(root):
    buf = io.StringIO()
    with redirect_stdout(buf):
        sc.cmd_index(Path(root))
    return (Path(root) / "ai_docs" / "strategic" / "features_history.md").read_text(encoding="utf-8")


class TS2DefaultResolution(unittest.TestCase):
    """The default is resolved at PROJECT level, deterministically."""

    def test_absent_everything_is_code(self):
        with tempfile.TemporaryDirectory() as d:
            seed_project(d)  # no default_domain line at all
            write(d, "ai_docs/solutions/ANALYSIS_a.md", analysis("F-001", "A", KNOWLEDGE_RISK))
            _, out = validate(d)
            self.assertIn("'## Security and Threat Model' missing", out,
                          "a project that declares nothing is code, exactly as before this feature")

    def test_project_default_flips_the_rules(self):
        with tempfile.TemporaryDirectory() as d:
            seed_project(d, readme_default="knowledge")
            write(d, "ai_docs/solutions/ANALYSIS_a.md", analysis("K-001", "A", KNOWLEDGE_RISK))
            rc, out = validate(d)
            self.assertNotIn("Security and Threat Model", out)
            self.assertEqual(rc, 0, out)

    def test_artifact_field_overrides_the_project_default(self):
        with tempfile.TemporaryDirectory() as d:
            seed_project(d, readme_default="knowledge")
            write(d, "ai_docs/solutions/ANALYSIS_a.md",
                  analysis("F-001", "A", CODE_RISK, domain="code"))
            rc, out = validate(d)
            self.assertEqual(rc, 0, out)

    def test_unknown_domain_is_reported_not_obeyed(self):
        with tempfile.TemporaryDirectory() as d:
            seed_project(d)
            write(d, "ai_docs/solutions/ANALYSIS_a.md",
                  analysis("F-001", "A", CODE_RISK, domain="sales"))
            _, out = validate(d)
            self.assertIn("domain 'sales' not recognized", out)
            self.assertIn("validated as 'code'", out)


class TS3MixedTree(unittest.TestCase):
    """Three lenses, one tree, one answer."""

    def _mixed(self, d):
        seed_project(d)
        write(d, "ai_docs/solutions/ANALYSIS_code.md",
              analysis("F-001", "Code thing", CODE_RISK, domain="code"))
        write(d, "ai_docs/solutions/ANALYSIS_knowledge.md",
              analysis("F-001", "Knowledge thing", KNOWLEDGE_RISK, domain="knowledge"))
        write(d, "ai_docs/solutions/ANALYSIS_marketing.md",
              analysis("M-001", "Market thing", MARKETING_RISK, domain="marketing"))

    def test_mixed_tree_is_clean(self):
        with tempfile.TemporaryDirectory() as d:
            self._mixed(d)
            reindex(d)
            rc, out = validate(d, strict=True)
            self.assertEqual(rc, 0, out)

    def test_same_id_in_two_domains_is_not_a_collision(self):
        with tempfile.TemporaryDirectory() as d:
            self._mixed(d)  # F-001 appears under code AND under knowledge
            _, out = validate(d)
            self.assertNotIn("duplicated", out,
                             "ids are unique within a domain: two lenses must not collide "
                             "on a number neither of them chose")

    def test_same_id_in_one_domain_is_still_a_collision(self):
        with tempfile.TemporaryDirectory() as d:
            seed_project(d)
            write(d, "ai_docs/solutions/ANALYSIS_a.md", analysis("F-001", "A", CODE_RISK))
            write(d, "ai_docs/solutions/ANALYSIS_b.md", analysis("F-001", "B", CODE_RISK))
            _, out = validate(d)
            self.assertIn("duplicated", out)

    def test_generated_index_does_not_depend_on_the_entry_point(self):
        """The whole reason the default is project-level rather than per-distribution."""
        with tempfile.TemporaryDirectory() as d:
            self._mixed(d)
            from_code = reindex(d)
            saved = dict(sdlc_core._ENTRY_POINT)
            try:
                sdlc_core.set_entry_point("knowledge", provides=("knowledge",))
                from_knowledge = reindex(d)
            finally:
                sdlc_core.set_entry_point(saved["domain"], provides=saved["provides"])
            self.assertEqual(from_code, from_knowledge,
                             "two lenses over one tree must generate the same file, byte for byte")


class TS4PerDomainSections(unittest.TestCase):
    """The risk slot is translated, never dropped — both directions."""

    def test_knowledge_analysis_missing_its_risk_section_errors(self):
        with tempfile.TemporaryDirectory() as d:
            seed_project(d, readme_default="knowledge")
            write(d, "ai_docs/solutions/ANALYSIS_a.md", analysis("K-001", "A", ""))
            rc, out = validate(d)
            self.assertEqual(rc, 1)
            self.assertIn("'## Sources and Verification' missing (mandatory)", out)

    def test_marketing_analysis_missing_its_risk_section_errors(self):
        with tempfile.TemporaryDirectory() as d:
            seed_project(d, readme_default="marketing")
            write(d, "ai_docs/solutions/ANALYSIS_a.md", analysis("M-001", "A", ""))
            rc, out = validate(d)
            self.assertEqual(rc, 1)
            self.assertIn("'## Threat Map / Plan Risks' missing (mandatory)", out)

    def test_a_knowledge_tree_is_never_asked_for_code_sections(self):
        with tempfile.TemporaryDirectory() as d:
            seed_project(d, readme_default="knowledge")
            write(d, "ai_docs/solutions/ANALYSIS_a.md", analysis("K-001", "A", KNOWLEDGE_RISK))
            _, out = validate(d)
            self.assertNotIn("Security and Threat Model", out,
                             "asking a knowledge practitioner for a code artifact is the "
                             "failure the Vision's fourth Actor names")


class TS10CrossDomainLocatability(unittest.TestCase):
    """Finding the document that OWNS a fact, from another lens."""

    def test_history_gains_a_domain_column_only_when_the_tree_declares_one(self):
        with tempfile.TemporaryDirectory() as d:
            seed_project(d)
            write(d, "ai_docs/solutions/ANALYSIS_a.md", analysis("F-001", "A", CODE_RISK))
            self.assertNotIn("Domain", reindex(d).splitlines()[3])
            write(d, "ai_docs/solutions/ANALYSIS_b.md",
                  analysis("K-001", "B", KNOWLEDGE_RISK, domain="knowledge"))
            tagged = reindex(d)
            self.assertIn("| Domain |", tagged.splitlines()[3])
            self.assertIn("| knowledge |", tagged)
            self.assertIn("| code |", tagged,
                          "the untagged sibling still resolves: the column is complete or absent")

    def test_the_restated_fact_clause_is_present(self):
        """C4's only mechanism against copies. If this clause goes, nothing detects them."""
        review = (SKILL_DIR / "review.md").read_text(encoding="utf-8")
        self.assertIn("Restated facts", review)
        self.assertIn("ONE owning document", review)


class TS13PortableChecks(unittest.TestCase):
    """Composable, opt-in, monotonic — and never silently unavailable."""

    def test_unavailable_check_warns_visibly(self):
        with tempfile.TemporaryDirectory() as d:
            seed_project(d, readme_default="knowledge")
            write(d, "ai_docs/solutions/ANALYSIS_a.md",
                  analysis("K-001", "A", KNOWLEDGE_RISK, checks=["marketing.ledger"]))
            _, out = validate(d)
            self.assertIn("not available in this distribution", out)
            self.assertIn("was NOT checked against it", out)

    def test_imported_check_adds_findings_without_relaxing_the_owner(self):
        with tempfile.TemporaryDirectory() as d:
            seed_project(d, readme_default="knowledge")
            # Satisfies knowledge's own section, and imports a code check it fails.
            body = analysis("K-001", "A", KNOWLEDGE_RISK, checks=["code.threat_model"])
            body += "\n## Security and Threat Model\nNo security impact.\n"
            write(d, "ai_docs/solutions/ANALYSIS_a.md", body)
            rc, out = validate(d)
            self.assertIn("[code.threat_model]", out, "the imported check ran")
            self.assertIn("declared, not justified", out)
            self.assertEqual(rc, 0, "an imported check adds findings; it does not change the "
                                    "owner's error/warning contract")

    def test_a_satisfied_imported_check_is_silent(self):
        with tempfile.TemporaryDirectory() as d:
            seed_project(d)
            write(d, "ai_docs/solutions/ANALYSIS_a.md",
                  analysis("F-001", "A", CODE_RISK, checks=["code.threat_model"]))
            _, out = validate(d)
            self.assertNotIn("[code.threat_model]", out)


if __name__ == "__main__":
    unittest.main(verbosity=1)
