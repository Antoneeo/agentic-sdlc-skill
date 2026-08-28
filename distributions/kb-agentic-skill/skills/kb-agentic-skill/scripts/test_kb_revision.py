#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-043 battery — the revision doctrine (the full re-read).

kb-ONLY module, deliberately outside the shared manifest (the F-039 precedent:
kb-only doctrine, kb-only vehicle). Guards ANALYSIS_revision_doctrine.md's
contract: the SKILL.md section carries the load-bearing clauses; the L2 process
cell and the L3 Phase-4 bullet each carry a citation-only pointer; and the
canonical clause appears EXACTLY ONCE across the skill-dir markdown (pointers
cite, never restate — DRY by pin, not by luck).

    python scripts/test_kb_revision.py
"""
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL = SKILL_DIR / "SKILL.md"

CANONICAL = "never append a delta"
# Spelling variants normalized INTO the canonical before counting, so a split
# spelling can never make the once-only pin pass vacuously.
VARIANTS = ("never delta-append", "never appending a delta")
POINTER = "full re-read per `## Revision`"


def normalized(path):
    """Whitespace-normalized (case preserved): line wrapping never decides."""
    return " ".join(path.read_text(encoding="utf-8").split())


def canonical_count(text):
    for v in VARIANTS:
        text = text.replace(v, CANONICAL)
    return text.count(CANONICAL)


class RevisionDoctrineTests(unittest.TestCase):

    def setUp(self):
        self.skill = normalized(SKILL)

    def test_section_exists(self):
        self.assertIn("## Revision", self.skill)

    def test_seven_load_bearing_anchors(self):
        # The doctrine's clauses, anchored whitespace-normalized: deleting any
        # of them must redden. Casing is part of the contract (WHOLE, PER
        # DOCUMENT are the doctrine's own emphasis).
        for anchor in ("re-read", "WHOLE",
                       CANONICAL,
                       "Diary",
                       "a correction is a new entry",
                       "tombstone",
                       "raises the probability",
                       "PER DOCUMENT"):
            self.assertIn(anchor, self.skill, anchor)

    def test_exemption_anchors(self):
        # Without these the doctrine instructs the forbidden act: the machine
        # deciding on claim rows, or a revision smuggling an L3 re-parent.
        self.assertIn("never the ledger", self.skill)
        self.assertIn("never re-parents", self.skill)

    def test_l2_process_cell_carries_the_pointer(self):
        row = next((l for l in SKILL.read_text(encoding="utf-8").splitlines()
                    if l.startswith("| **L2")), "")
        self.assertTrue(row, "the L2 triage row exists")
        cells = [" ".join(c.split()) for c in row.split("|")]
        # cells: ['', level, criteria, process, ''] -- the pointer belongs to
        # the PROCESS cell and must never drift into the pinned criteria cell.
        self.assertIn(POINTER, cells[3])
        self.assertNotIn(POINTER, cells[2])

    def test_phase4_bullet_carries_the_pointer(self):
        # The post-mortem's own scenario is an L3 realignment through Phase 4:
        # the mid-L3 agent must meet the pointer there, not only in triage.
        bullet = next((l for l in SKILL.read_text(encoding="utf-8").splitlines()
                       if "Distillation rewrites existing notes" in l), "")
        self.assertTrue(bullet, "the Phase-4 isolation bullet exists")
        self.assertIn(POINTER, " ".join(bullet.split()))

    def test_canonical_clause_appears_exactly_once_across_the_skill_dir(self):
        # File set: kb SKILL.md + the skill-dir *.md support files (ENFORCEMENT
        # included; README is package-root and .py files are out of set — the
        # remind payload is the one deliberate second carrier, guarded by its
        # own battery).
        total = 0
        where = []
        for md in sorted(SKILL_DIR.glob("*.md")):
            n = canonical_count(normalized(md))
            total += n
            if n:
                where.append("%s:%d" % (md.name, n))
        self.assertEqual(total, 1,
                         "the canonical clause must appear exactly once "
                         "(the section's own line); found: %s" % ", ".join(where))


if __name__ == "__main__":
    unittest.main()
