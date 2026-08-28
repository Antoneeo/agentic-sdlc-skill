#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-039 battery — the topic-recall reflex (second-brain unit 1).

kb-ONLY module, deliberately outside the shared manifest: recall over a topic
graph is kb-only doctrine, so its guard must not ride a drift-guarded x3 file
(the round-2 review finding that created this module). Two halves:

  1. Doctrine invariants — SKILL.md's Topic Recall section and taxonomy.md's
     answer-mode section exist and carry the load-bearing clauses, anchored
     whitespace-normalized so line wrapping never decides a verdict.
  2. The orient interception — kb `orient` appends the topic router by
     construction, and never breaks orient when the graph is absent or broken.

    python scripts/test_kb_recall.py
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


ORIENT_MARKER = "ORIENT-CORE-RAN-9f3a"


def seed_project(tmp):
    """Minimal valid-enough docs root for orient to run against. The README
    carries a marker so tests can assert the SPINE's orient actually ran —
    the forward is load-bearing (a mutation deleting it must redden)."""
    docs = Path(tmp) / "ai_docs"
    docs.mkdir(parents=True)
    (docs / "README.md").write_text("# ai_docs\n%s\n" % ORIENT_MARKER,
                                    encoding="utf-8")
    return docs


def run_main(argv, cwd):
    """Run the overlay main() capturing stdout; never let SystemExit escape."""
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


class TestRecallDoctrine(unittest.TestCase):
    """The wording the reflex depends on cannot silently leave the files."""

    def test_skill_md_carries_the_recall_section(self):
        text = normalized(SKILL_DIR / "SKILL.md")
        for anchor in (
            "## Topic Recall — the answer-side consult",
            "unconditional scan on domain assertions",
            "judged ON the scanned top rows, never before them",
            "Once per topic per SESSION",
            "N claims cited",
            "node matched, no claims",
            "kb: no coverage",
            "index absent — regenerate",
            "Never fake the verdict",
            "walk its chain to non-DERIVED ground",
            "unverified for decision-grounding",
            "un-re-ratified foreign authority",
            "`SUPERSEDED <id>` is never cited without naming its successor",
            "may co-occur",
            "Exempt: pure mechanics",
            "cites the claim id AND the re-touched ground",
            "inlines the cited claim rows",
        ):
            self.assertIn(anchor, text,
                          "SKILL.md lost a recall clause: %r" % anchor)

    def test_taxonomy_carries_the_answer_mode_descent(self):
        text = normalized(SKILL_DIR / "taxonomy.md")
        for anchor in (
            "## 6. The same descent, answer mode",
            "descend before answering from model memory",
            "coverage (found / not found) replaces the five verdicts",
        ):
            self.assertIn(anchor, text,
                          "taxonomy.md lost the answer-mode section: %r" % anchor)

    def test_the_skill_description_names_the_answering_surface(self):
        head = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")[:1200]
        self.assertIn("answering project questions", head,
                      "the activation surface lost the recall trigger")


class TestOrientTopicRouter(unittest.TestCase):
    """The by-construction limb: orient surfaces the graph, and fails open."""

    def test_orient_appends_the_index_when_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = seed_project(tmp)
            topics = docs / "topics"
            topics.mkdir()
            (topics / "pricing.md").write_text(
                "---\ntopic: pricing\ndescription: d\nparents: []\n"
                "status: CURRENT\n---\n\nbody\n", encoding="utf-8")
            (topics / "INDEX.md").write_text(
                "| slug | description |\n|---|---|\n| pricing | d |\n",
                encoding="utf-8")
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertIn(ORIENT_MARKER, out,
                          "the spine's orient did not run: the forward is gone")
            self.assertIn("## Topic router", out)
            self.assertIn("pricing", out)
            self.assertLess(out.index(ORIENT_MARKER), out.index("## Topic router"),
                            "the router must be APPENDED after the spine's output")

    def test_orient_reports_a_lagging_index_with_node_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = seed_project(tmp)
            topics = docs / "topics"
            topics.mkdir()
            (topics / "pricing.md").write_text(
                "---\ntopic: pricing\ndescription: d\nparents: []\n"
                "status: CURRENT\n---\n\nbody\n", encoding="utf-8")
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertIn("index absent (1 node files)", out)
            self.assertIn("sdlc_check.py index", out)

    def test_orient_stays_silent_with_no_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            seed_project(tmp)
            rc, out = run_main(["orient", "--root", tmp], tmp)
            self.assertNotIn("## Topic router", out,
                             "a project with no graph must get no router noise")

    def test_orient_survives_an_unreadable_graph(self):
        # Fail-open: the append may find garbage; orient itself must not break.
        with tempfile.TemporaryDirectory() as tmp:
            docs = seed_project(tmp)
            (docs / "topics").mkdir()
            (docs / "topics" / "INDEX.md").mkdir()   # a DIRECTORY named INDEX.md
            rc, out = run_main(["orient", "--root", tmp], tmp)
            # no assertion on rc value: orient's own semantics own it; the test
            # is that we got here without an exception escaping main().


if __name__ == "__main__":
    unittest.main(verbosity=1)
