#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-040 battery — the capture moment (second-brain unit 2).

kb-ONLY module, outside the shared manifest (the F-039 review rule: kb-only
doctrine takes a kb-only vehicle). Two halves:

  1. Doctrine invariants — SKILL.md's Capture Moment section and its Write
     Triggers row carry the load-bearing clauses, whitespace-normalized.
  2. The notes-recency line in the kb orient append — five states.

    python scripts/test_kb_capture.py
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_check as kc  # noqa: E402

SKILL_DIR = Path(__file__).resolve().parent.parent


def normalized(path):
    return " ".join(path.read_text(encoding="utf-8").split())


def seed_project(tmp):
    docs = Path(tmp) / "ai_docs"
    docs.mkdir(parents=True)
    (docs / "README.md").write_text("# ai_docs\n", encoding="utf-8")
    return docs


def run_main(argv, cwd):
    buf = io.StringIO()
    old = os.getcwd()
    os.chdir(cwd)
    try:
        with contextlib.redirect_stdout(buf):
            try:
                rc = kc.main(argv)
            except SystemExit as e:
                rc = e.code if isinstance(e.code, int) else 1
    finally:
        os.chdir(old)
    return rc, buf.getvalue()


class TestCaptureDoctrine(unittest.TestCase):
    """The wording the moment depends on cannot silently leave SKILL.md."""

    def test_skill_md_carries_the_capture_section(self):
        text = normalized(SKILL_DIR / "SKILL.md")
        for anchor in (
            "## The Capture Moment",
            "user-signed closings, once per session",
            "any other decisions from today to record",
            "carrying its own search result inline",
            "the inline result satisfies the search-first duty",
            "scheduled elicitation",
            "`derived_from:` → claim `prov: DERIVED`",
            "The sweep is idempotent",
            "never re-captured",
            "prov: ELICITED",
            "RULING only when the decision resolves an existing contested set",
            "never a decision park",
            "Declared residual",
            "never silently overwrite",
            "Silence stays legal where no one signed off",
        ):
            self.assertIn(anchor, text,
                          "SKILL.md lost a capture clause: %r" % anchor)

    def test_write_triggers_carry_the_sweep_row(self):
        text = normalized(SKILL_DIR / "SKILL.md")
        for anchor in (
            "at a user-signed closing (the Capture Moment sweep)",
            "only for what the sweep surfaces un-captured",
            "disjoint from the row above",
        ):
            self.assertIn(anchor, text,
                          "the Write Triggers sweep row lost a clause: %r" % anchor)

    def test_the_recency_limit_is_named_where_the_line_is_defined(self):
        # Comment-marker + whitespace normalized: a re-wrapped comment line
        # must not decide this verdict (the F-038 line-wrap lesson).
        raw = (SKILL_DIR / "scripts" / "sdlc_check.py").read_text(encoding="utf-8")
        src = " ".join(raw.replace("#", " ").split())
        self.assertIn("mtime LIES after clone/worktree", src,
                      "the recency line lost its named limit")
        self.assertIn("NOTES recency, not full ledger", src,
                      "the recency line lost its honest scope")


class TestNotesRecency(unittest.TestCase):
    """The by-construction limb: five states, date-frontmatter first."""

    def _notes(self, tmp):
        docs = seed_project(tmp)
        notes = docs / "corpus" / "notes"
        notes.mkdir(parents=True)
        return notes

    def test_dated_note_wins_over_mtime(self):
        import datetime as dt
        with tempfile.TemporaryDirectory() as tmp:
            notes = self._notes(tmp)
            # frontmatter date is 20 days back; mtime is now -- the line must
            # trust date:, or it would report 0 days (the clone-reset lie).
            old = (dt.date.today() - dt.timedelta(days=20)).isoformat()
            (notes / "old.md").write_text(
                "---\norigin: elicited\ndate: %s\n---\nx\n" % old,
                encoding="utf-8")
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertIn("newest note:", out)
            self.assertIn("20 days old", out)

    def test_undated_note_falls_back_to_mtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            notes = self._notes(tmp)
            (notes / "n.md").write_text(
                "---\norigin: elicited\n---\nx\n", encoding="utf-8")
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertIn("newest note: 0 days old", out)

    def test_quoted_date_is_parsed_not_mtimed(self):
        # Field defect (2026-08-28): a YAML-quoted date fell through to the
        # mtime fallback, so a note rewritten today read "0 days old" against
        # SKILL.md's date-first promise.
        import datetime as dt
        with tempfile.TemporaryDirectory() as tmp:
            notes = self._notes(tmp)
            old = (dt.date.today() - dt.timedelta(days=20)).isoformat()
            (notes / "q.md").write_text(
                '---\norigin: elicited\ndate: "%s"\n---\nx\n' % old,
                encoding="utf-8")
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertIn("20 days old", out)
            self.assertNotIn("mtime", out)

    def test_long_frontmatter_date_is_still_parsed(self):
        # Field datum 7 (2026-08-28, on 1.11.0): a REAL note's frontmatter
        # (derived_from lists, basis lines) pushed the closing fence past the
        # probe's 600-byte head window, so the WHOLE date: probe silently
        # skipped and a note dated days back read "0 days old (mtime)". The
        # cap bought nothing -- the file was already fully read.
        import datetime as dt
        with tempfile.TemporaryDirectory() as tmp:
            notes = self._notes(tmp)
            old = (dt.date.today() - dt.timedelta(days=20)).isoformat()
            filler = "\n".join("k%03d: %s" % (i, "x" * 40) for i in range(20))
            (notes / "big.md").write_text(
                "---\norigin: elicited\n%s\ndate: %s\n---\nx\n" % (filler, old),
                encoding="utf-8")
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertIn("20 days old", out)
            self.assertNotIn("mtime", out)

    def test_datetime_suffix_still_parses_the_date(self):
        import datetime as dt
        with tempfile.TemporaryDirectory() as tmp:
            notes = self._notes(tmp)
            old = (dt.date.today() - dt.timedelta(days=20)).isoformat()
            (notes / "n.md").write_text(
                "---\norigin: elicited\ndate: %s 10:30\n---\nx\n" % old,
                encoding="utf-8")
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertIn("20 days old", out)
            self.assertNotIn("mtime", out)

    def test_mtime_fallback_discloses_itself(self):
        # When no date: decided the winner the line must SAY so -- a silently
        # fresh "0 days" after a rewrite/checkout is the lie the field report
        # caught; the degraded basis becomes visible, not mute.
        with tempfile.TemporaryDirectory() as tmp:
            notes = self._notes(tmp)
            (notes / "n.md").write_text(
                "---\norigin: elicited\n---\nx\n", encoding="utf-8")
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertIn("newest note: 0 days old", out)
            self.assertIn("mtime", out)

    def test_undated_winner_over_dated_note_discloses(self):
        # The field scenario's shape: an mtime-stamped note WINS over a dated
        # one -- the disclosure rides the stamp that actually won.
        import datetime as dt
        with tempfile.TemporaryDirectory() as tmp:
            notes = self._notes(tmp)
            old = (dt.date.today() - dt.timedelta(days=20)).isoformat()
            (notes / "dated.md").write_text(
                "---\norigin: elicited\ndate: %s\n---\nx\n" % old,
                encoding="utf-8")
            (notes / "undated.md").write_text(
                "---\norigin: elicited\n---\nx\n", encoding="utf-8")
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertIn("0 days old", out)
            self.assertIn("mtime", out)

    def test_dated_winner_carries_no_mtime_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            notes = self._notes(tmp)
            (notes / "n.md").write_text(
                "---\norigin: elicited\ndate: 2026-08-28\n---\nx\n",
                encoding="utf-8")
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertIn("newest note:", out)
            self.assertNotIn("mtime", out)

    def test_empty_notes_dir_says_no_notes_yet(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._notes(tmp)
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertIn("no notes yet", out)

    def test_no_corpus_prints_no_recency_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            seed_project(tmp)
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertNotIn("newest note", out)
            self.assertNotIn("no notes yet", out)

    def test_recency_prints_without_a_topic_graph(self):
        # notes exist, topics/ does not: the line is independent of the router.
        with tempfile.TemporaryDirectory() as tmp:
            notes = self._notes(tmp)
            (notes / "n.md").write_text(
                "---\norigin: elicited\ndate: 2026-08-28\n---\nx\n",
                encoding="utf-8")
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertIn("newest note:", out)
            self.assertNotIn("## Topic router", out)


if __name__ == "__main__":
    unittest.main(verbosity=1)
