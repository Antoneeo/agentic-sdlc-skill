#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-068 battery -- the ingestion rhythm on an open front. Doctrine invariants
only: the wording the rhythm depends on cannot silently leave the kb texts.

    python scripts/test_kb_ingestion_rhythm.py
"""
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
COURSE_DIR = SKILL_DIR.parents[2] / "course-creator" / "skills" / "course-creator"


def normalized(path):
    return " ".join(path.read_text(encoding="utf-8").split())


class TestIngestionStep(unittest.TestCase):
    """AC1/AC3/AC4: an open unit absorbs; two things never wait; rows by anchor."""

    def setUp(self):
        self.skill = normalized(SKILL_DIR / "SKILL.md")

    def test_rule_zero_carries_absorption(self):
        for anchor in (
            "**An open unit absorbs.**",
            "ingestion step of <unit>",
            "the `scope:` field of that HANDOFF's frontmatter",
            "a save commit once `graph` and `corpus` are clean, its message marked `ingestion step`",
            "Without isolation the residual risk is higher",
            "A step does not rewrite dependent documents",
            "an escalation trigger the approved ANALYSIS did not plan",
            "ask one question before ingesting",
            "(from another checkout, its row in the registry says so)",
            "frontmatter untouched. The step reply states what landed on the ledger",
            "and that alignment is pending",
        ):
            self.assertIn(anchor, self.skill, "Rule Zero lost: %r" % anchor)

    def test_two_immediate_exceptions(self):
        for anchor in (
            "a communication draft in progress",
            "already delivered to the practitioner in this session",
        ):
            self.assertIn(anchor, self.skill, anchor)

    def test_rows_by_anchor_and_single_fill(self):
        for anchor in (
            "`anchor <path> <phrase>`",
            "`claim-id --fill` once",
            "never that the span says what the claim says",
        ):
            self.assertIn(anchor, self.skill, anchor)


class TestClosureEvent(unittest.TestCase):
    """AC2/AC5: closure is an event with two exits; the registry is never hand-edited."""

    def setUp(self):
        self.skill = normalized(SKILL_DIR / "SKILL.md")

    def test_phase5_trigger_and_exits(self):
        for anchor in (
            "Phase 5 fires only on the practitioner's request",
            "**Alignment closure**",
            "**Unit closure**",
            "When the closure gate is red",
            "When it was the last one, `index` empties the generated registry.",
            "enumerated from the request-record entries since then and the uncommitted changes",
            "The closure reply states the closure-gate result",
            "A unit that absorbed no ingestion step closes as before",
            "the only gate command",
            "does not print the kb `## claims` worklist",
            "which is why the `stale` step above stays",
            "the save commit lands on the shared line itself",
            "that is a departure from this rule, not a second mode",
        ):
            self.assertIn(anchor, self.skill, anchor)

    def test_write_triggers_say_never_at_a_step(self):
        self.assertGreaterEqual(self.skill.count("never at an ingestion step"), 2)

    def test_capture_sweep_runs_again_after_an_alignment(self):
        self.assertIn("user-signed closings, once per session", self.skill)
        self.assertIn("and at every Phase 5", self.skill)

    def test_no_hand_edit_of_the_registry_anywhere_in_kb_doctrine(self):
        for doc in sorted(SKILL_DIR.glob("*.md")):
            text = normalized(doc)
            self.assertNotIn("delete the generated `audit/handoff.md`", self.skill)
        for banned in ("Update `audit/handoff.md`", "updates `handoff.md`",
                           "Update `handoff.md`"):
                self.assertNotIn(banned, text, "%s: %s" % (doc.name, banned))

    def test_templates_carry_scope_lag_and_unit_closure(self):
        tpl = normalized(SKILL_DIR / "templates.md")
        for anchor in ("an ingestion step's body resume line excepted",
                       "`scope:` is what an ingestion step is tested against",
                       "(ephemeral — deleted at unit closure)"):
            self.assertIn(anchor, tpl, anchor)


class TestCascadeAtClosure(unittest.TestCase):
    """AC6: the supersession is recorded at once, the cascade runs at closure."""

    def test_reconciliation(self):
        rec = normalized(SKILL_DIR / "reconciliation.md")
        self.assertIn("runs at the unit's next closure", rec)
        self.assertNotIn("Recording a supersession ends by running", rec)
        self.assertIn("named once, in `SKILL.md` Phase 4", rec)

    def test_enforcement_kb_and_course(self):
        for root in (SKILL_DIR, COURSE_DIR):
            enf = normalized(root / "ENFORCEMENT.md")
            self.assertIn("runs `stale` at the unit's closure", enf, root)
            self.assertNotIn("after recording a supersession", enf, root)


if __name__ == "__main__":
    unittest.main()
