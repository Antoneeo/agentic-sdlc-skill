#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static skill-invariant battery (M4 Unit 4) -- the deterministic release gate.

Asserts the skill's OWN doctrine invariants: every M4 unit output is present and
wired, support-file pointers resolve, and the generated indexes are idempotent.
Stdlib only, zero-LLM, zero-network, zero-subprocess -- a failing eval is always
a real regression, never flakiness (P-TM T9). Runs as part of
`python -m unittest discover -s scripts -p "test_*.py"`.
"""
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_check as sc  # noqa: E402

# file sits at skills/agentic-sdlc-skill/scripts/ -> parents[1] = skill dir,
# parents[3] = repo root where ai_docs/ lives (matches test_plan.py:229).
SKILL_DIR = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]


def read(rel):
    return sc.read_text(SKILL_DIR / rel)


class SkillInvariants(unittest.TestCase):

    def test_orient_registered(self):
        self.assertTrue(hasattr(sc, "cmd_orient"))
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(sc.main(["orient", "--root", d]), 0)

    def test_enforcement_sections_present(self):
        t = read("ENFORCEMENT.md")
        self.assertIn("## 4. SessionStart hook", t)
        self.assertIn("## 5. Skill eval battery", t)

    def test_skill_consult_trigger(self):
        t = read("SKILL.md")
        self.assertIn("consult the guide router", t)
        self.assertIn("Consult (before acting)", t)

    def test_skill_proactive_trigger(self):
        t = read("SKILL.md")
        self.assertIn("PROPOSE distilling a guide", t)
        self.assertIn("Propose proactively", t)

    def test_guides_consume_and_proactive(self):
        t = read("guides.md")
        self.assertIn("## 0. Consuming a guide", t)
        self.assertIn("### Proactive trigger", t)

    def test_dispatch_guide_note(self):
        self.assertIn("Guide consumption under dispatch", read("dispatch.md"))

    def test_comprehension_guide_wiring(self):
        """Code-comprehension guides (source_kind: code) are wired end to end:
        the autonomous trigger in guides.md, the SKILL.md moment + Write-Triggers
        row, and the template field."""
        guides = read("guides.md")
        self.assertIn("Comprehension trigger", guides)
        self.assertIn("source_kind", guides)
        skill = read("SKILL.md")
        self.assertIn("source_kind: code", skill)
        self.assertIn("Comprehend (code, autonomous)", skill)
        self.assertIn("source_kind", read("templates.md"))

    def test_skill_worktree_hygiene(self):
        t = read("SKILL.md")
        self.assertIn("Isolate the work", t)
        self.assertIn("Branch/worktree hygiene", t)

    def test_support_files_wired(self):
        """Anti-orphan (mechanized 'orphaned discipline never fires', M2):
        every expected support file exists AND is referenced in SKILL.md, and
        any *.md added beside SKILL.md is also referenced (no silent orphan)."""
        skill_md = read("SKILL.md")
        expected = ["templates.md", "guides.md", "tdd.md", "debugging.md",
                    "elicitation.md", "review.md", "dispatch.md",
                    "ENFORCEMENT.md", "scripts/sdlc_check.py"]
        for rel in expected:
            self.assertTrue((SKILL_DIR / rel).is_file(),
                            f"expected support file missing: {rel}")
            self.assertIn(Path(rel).name, skill_md,
                          f"support file not referenced in SKILL.md (dangling): {rel}")
        for p in SKILL_DIR.glob("*.md"):
            if p.name == "SKILL.md":
                continue
            self.assertIn(p.name, skill_md,
                          f"orphan support file (exists, not referenced): {p.name}")

    def test_indexes_idempotent(self):
        """Generated indexes are current: build_* output == on-disk, computed
        WITHOUT writing (never calls cmd_index). A stale index fails here; the
        fix is `sdlc_check.py index` before release -- the intended gate."""
        hist = REPO / "ai_docs" / "strategic" / "features_history.md"
        if hist.is_file():
            self.assertEqual(sc.norm_text(sc.build_index(REPO)),
                             sc.norm_text(sc.read_text(hist)),
                             "features_history.md stale: run sdlc_check.py index")
        if sc.list_canonical_docs(REPO):
            manifest = REPO / "ai_docs" / "INDEX.md"
            self.assertEqual(sc.norm_text(sc.build_manifest(REPO)),
                             sc.norm_text(sc.read_text(manifest)),
                             "INDEX.md stale: run sdlc_check.py index")
        if sc.list_guides(REPO):
            gidx = REPO / "ai_docs" / "reference" / "INDEX.md"
            self.assertEqual(sc.norm_text(sc.build_guide_index(REPO)),
                             sc.norm_text(sc.read_text(gidx)),
                             "reference/INDEX.md stale: run sdlc_check.py index")

    def test_behavioral_driver_no_llm(self):
        """Mechanized T4: the behavioral driver must never call a model,
        the network, or a subprocess."""
        src = (SKILL_DIR / "evals" / "run_behavioral.py").read_text(encoding="utf-8")
        forbidden = ["subprocess", "os.system", "eval(", "exec(", "urllib",
                     "http", "requests", "openai", "anthropic", "socket"]
        for tok in forbidden:
            self.assertNotIn(tok, src, f"driver must not reference {tok} (T4)")


if __name__ == "__main__":
    unittest.main()
