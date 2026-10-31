#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-087 — the owner approves an L3 design before the work starts.

review.md has the agent stop after the design review's final PASS, present the
design and ask the owner whether to proceed; the answer is recorded in the
request record under a label that begins `design approved`. In Standalone,
`validate` notes an L3 in implementation whose request record holds no such
entry. Each test names the mutation that turns it red.

    python scripts/test_design_approval.py

Standard library only.
"""
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_core as sc  # noqa: E402

SKILL_DIR = Path(__file__).resolve().parent.parent
EPOCH = sc.DESIGN_APPROVAL_EPOCH
BEFORE = "2026-10-30"   # the day the rule was written: grandfathered
MARK = "design approval"
APPROVED = "\n### R2 — 2026-11-02 — design approved\n> procedi\n"


def setUpModule():
    global _SAVED_DOCS_DIR
    _SAVED_DOCS_DIR = sc.docs_dir()
    sc.set_docs_dir("ai_docs")


def tearDownModule():
    sc.set_docs_dir(_SAVED_DOCS_DIR)


def seed(root, status="IN_PROGRESS", level="L3", start=EPOCH, extra="", request=True):
    ai = Path(root) / "ai_docs"
    for sub in ("solutions", "audit/requests", "audit/reviews"):
        (ai / sub).mkdir(parents=True, exist_ok=True)
    p = ai / "solutions" / "ANALYSIS_probe.md"
    p.write_text(
        f"---\ndescription: x\nstatus: {status}\nid: F-900\nstart_date: {start}\n"
        f"end_date:\nlevel: {level}\ndomain: code\n---\n# Feature Analysis: probe\n\n"
        f"## Objective\n\nx\n\n## Diary / Current State\n\n**{start} — opened.** x\n",
        encoding="utf-8")
    if request:
        (ai / "audit" / "requests" / "REQUEST_probe.md").write_text(
            "---\nunit: F-900\nanalysis: ANALYSIS_probe.md\n---\n# Request record: probe\n\n"
            f"### R1 — {start} — opening request\n> do it\n{extra}", encoding="utf-8")
    (ai / "audit" / "reviews" / "REVIEW_LOG.md").write_text(
        "| date | doc_key | tier | model | instrument | findings_raised | findings_real "
        "| verdict | revise_rounds | notes |\n|---|---|---|---|---|---|---|---|---|---|\n"
        f"| {start} | solutions/ANALYSIS_probe.md | design | deep | rung 1 | 0 | 0 | PASS | 1 | x |\n",
        encoding="utf-8")
    return p


def notes(root, **kw):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = sc.cmd_validate(Path(root), **kw)
    return rc, [l for l in buf.getvalue().splitlines()
                if "ANALYSIS_probe" in l and MARK in l]


class Advisory(unittest.TestCase):

    def test_in_progress_without_approval_is_noted(self):
        """Mutation: drop the design-approval call from cmd_validate -> red."""
        with tempfile.TemporaryDirectory() as d:
            seed(d)
            _, found = notes(d)
            self.assertEqual(len(found), 1, found)
            self.assertTrue(found[0].startswith("[note]"), found[0])

    def test_completed_without_approval_is_noted(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d, status="COMPLETED")
            self.assertEqual(len(notes(d)[1]), 1)

    def test_missing_request_record_is_noted(self):
        """Mutation: return True when no request record names the ANALYSIS -> red."""
        with tempfile.TemporaryDirectory() as d:
            seed(d, request=False)
            self.assertEqual(len(notes(d)[1]), 1)

    def test_label_must_begin_with_design_approved(self):
        """Mutation: match 'design approved' anywhere in the label -> red."""
        with tempfile.TemporaryDirectory() as d:
            seed(d, extra="\n### R2 — 2026-11-02 — question before the design approved\n> ok\n")
            self.assertEqual(len(notes(d)[1]), 1)

    def test_approval_entry_silences_it(self):
        """Mutation: design_approval_logged always False -> red."""
        with tempfile.TemporaryDirectory() as d:
            seed(d, extra=APPROVED)
            self.assertEqual(notes(d)[1], [])

    def test_label_is_matched_case_insensitively(self):
        """Mutation: a case-sensitive startswith -> red."""
        with tempfile.TemporaryDirectory() as d:
            seed(d, extra=APPROVED.replace("design approved", "Design approved by the owner"))
            self.assertEqual(notes(d)[1], [])

    def test_quotation_is_not_read(self):
        """Only the label counts: 'design approved' inside the quoted words of an
        entry labelled otherwise approves nothing (T3). Mutation: scan the body -> red."""
        with tempfile.TemporaryDirectory() as d:
            seed(d, extra="\n### R2 — 2026-11-02 — design returned\n> design approved? no\n")
            self.assertEqual(len(notes(d)[1]), 1)

    def test_planned_is_not_late(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d, status="PLANNED")
            self.assertEqual(notes(d)[1], [])

    def test_below_l3_is_quiet(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d, level="L2")
            self.assertEqual(notes(d)[1], [])

    def test_unit_started_before_the_epoch_is_quiet(self):
        """Mutation: compare with > instead of >= or move the epoch back -> red."""
        with tempfile.TemporaryDirectory() as d:
            seed(d, start=BEFORE)
            self.assertEqual(notes(d)[1], [])

    def test_hybrid_is_approved_in_devpnt(self):
        """Mutation: drop 'not hybrid' -> red."""
        with tempfile.TemporaryDirectory() as d:
            seed(d)
            self.assertEqual(notes(d, hybrid=True)[1], [])

    def test_note_never_changes_strict(self):
        """P5: an advisory, never a warning. Mutation: append it to warnings -> red."""
        with tempfile.TemporaryDirectory() as d:
            seed(d)
            rc_missing, found = notes(d, strict=True)
        with tempfile.TemporaryDirectory() as d:
            seed(d, extra=APPROVED)
            rc_approved, _ = notes(d, strict=True)
        self.assertTrue(found)
        self.assertEqual(rc_missing, rc_approved)


class Extractions(unittest.TestCase):
    """P1 and P3: the helpers this unit extracts leave their callers' results unchanged."""

    def test_design_review_due_unchanged(self):
        cases = [({"level": "L3", "status": "IN_PROGRESS", "start_date": sc.DESIGN_REVIEW_EPOCH}, True),
                 ({"level": "l3", "status": "COMPLETED", "start_date": "'2026-08-01'"}, True),
                 ({"level": "L3", "status": "PLANNED", "start_date": "2026-08-01"}, False),
                 ({"level": "L2", "status": "IN_PROGRESS", "start_date": "2026-08-01"}, False),
                 ({"level": "L3", "status": "IN_PROGRESS", "start_date": "2026-07-27"}, False),
                 ({"level": "L3", "status": "IN_PROGRESS"}, False)]
        for meta, want in cases:
            self.assertEqual(sc.design_review_due(meta), want, meta)

    def test_unit_documents_still_include_the_request_record(self):
        with tempfile.TemporaryDirectory() as d:
            p = seed(d)
            docs = sc._unit_documents(Path(d), p)
            self.assertTrue(any(x.lower().endswith("request_probe.md") for x in docs), docs)
            self.assertTrue(any(x.lower().endswith("handoff_probe.md") for x in docs), docs)

    def test_requests_naming_matches_the_analysis_field(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d)
            other = Path(d) / "ai_docs" / "audit" / "requests" / "REQUEST_other.md"
            other.write_text("---\nanalysis: `ANALYSIS_other.md`\n---\n", encoding="utf-8")
            got = [r.name for r in sc.requests_naming(Path(d), "ANALYSIS_probe.md")]
            self.assertEqual(got, ["REQUEST_probe.md"])


class Gate(unittest.TestCase):

    def test_refusal_names_the_design_approval(self):
        """FS 10: the message changes, the exit code does not (P4)."""
        with tempfile.TemporaryDirectory() as d:
            seed(d, status="PLANNED")
            target = Path(d) / "src" / "x.py"
            target.parent.mkdir()
            target.write_text("x = 1\n", encoding="utf-8")
            err = io.StringIO()
            with redirect_stderr(err), redirect_stdout(io.StringIO()):
                rc = sc.main(["gate", "--root", d, "--file", str(target), "--protected", "src"])
            self.assertEqual(rc, 2)
            self.assertIn(MARK, err.getvalue())


class Doctrine(unittest.TestCase):
    """The rule lives once, in the shared review.md; each lens's SKILL.md points at it."""

    def test_review_md_carries_the_rule(self):
        text = (SKILL_DIR / "review.md").read_text(encoding="utf-8")
        start = text.find("**The owner approves the design before the work starts (L3).**")
        self.assertNotEqual(start, -1, "the rule's paragraph is missing from review.md")
        para = text[start:text.find("\n\n", start)]
        for needle in ("`design approved`", "BLOCKED on the user", "devPNT", "USER GATE",
                       "does not approve it", sc.DESIGN_APPROVAL_EPOCH):
            self.assertIn(needle, para)

    def test_lens_skill_points_at_the_rule(self):
        lines = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").splitlines()
        hits = [l for l in lines if "§When a review is due" in l
                and ("design approval" in l or "approves the design" in l)]
        self.assertTrue(hits, "this lens's SKILL.md never points at the owner's design approval")


if __name__ == "__main__":
    unittest.main(verbosity=2)
