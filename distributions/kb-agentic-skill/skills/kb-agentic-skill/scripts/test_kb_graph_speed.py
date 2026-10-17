#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-069 battery — a graph check fast enough for the ingestion step.

kb-ONLY module, deliberately outside the shared manifest. Pins the mechanism
of ANALYSIS_kb_graph_speed.md, never a wall-clock budget (timing in CI is
noise):

  T1  kb_time_cycle extracts the cited ids of each living document once, and
      never scans a text once per (document, id) pair.
  T1b on a KB with no superseded id and no validity window it extracts nothing.
  T2  one kb_check_claims run reads each cited extraction once, however many
      rows cite it.
  T3  findings stay per row through the memo (page and line forms).
  T4  nothing is remembered between runs.

Output identity at scale is the probe's job:
    python ai_docs/solutions/harness_kb_graph_only/probe.py --baseline main

    python scripts/test_kb_graph_speed.py
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_check as kc  # noqa: E402
import knowledge  # noqa: E402

HEAD = ("---\ntopic: t\ndescription: d\nparents: []\nstatus: CURRENT\n---\n\n"
        "## Claims\n\n| id | claim | valid | qty | about | source | prov | state |\n"
        "|---|---|---|---|---|---|---|---|\n")
PAGE = "x" * 200
SIDECAR = "---\ndate: 2026-09-01\nprovenance: GIVEN\n---\n"


def row(art, a, b, valid="-", state="OK"):
    """One claim row citing corpus/given/<art>#p=1@a-b, id computed."""
    path, loc = "corpus/given/%s" % art, "p=1@%d-%d" % (a, b)
    rid = kc.kb_claim_id(path, loc, "")
    return rid, "| %s | c%d | %s | - | - | %s#%s | GIVEN | %s |" % (
        rid, a, valid, path, loc, state)


def make_docs(tmp, rows, living=(), given=None):
    docs = Path(tmp) / "ai_docs"
    (docs / "topics").mkdir(parents=True)
    (docs / "topics" / "t.md").write_text(HEAD + "\n".join(rows) + "\n",
                                          encoding="utf-8")
    g = docs / "corpus" / "given"
    g.mkdir(parents=True)
    for name, text in (given if given is not None else {"c.txt": PAGE}).items():
        (g / name).write_text(text, encoding="utf-8")
        (g / (name + ".meta.md")).write_text(SIDECAR, encoding="utf-8")
    sol = docs / "solutions"
    sol.mkdir()
    for i, text in enumerate(living):
        (sol / ("d%02d.md" % i)).write_text(text, encoding="utf-8")
    return docs


class _CountingPattern:
    """Stands in for a compiled pattern (whose attributes are read-only)."""

    def __init__(self, pattern):
        self.pattern, self.calls = pattern, 0

    def findall(self, text, *a):
        self.calls += 1
        return self.pattern.findall(text, *a)

    def __getattr__(self, name):
        return getattr(self.pattern, name)


class _CountingRe:
    """Stands in for the `re` module as knowledge.py sees it."""

    def __init__(self, real):
        self.real, self.searches = real, 0

    def search(self, *a, **k):
        self.searches += 1
        return self.real.search(*a, **k)

    def __getattr__(self, name):
        return getattr(self.real, name)


def counted_cycle(docs):
    """kb_time_cycle(docs) with re.search and the token pattern counted."""
    self_test = unittest.TestCase()
    self_test.assertTrue(hasattr(knowledge, "KB_HEX_TOKEN_RE"),
                         "knowledge.KB_HEX_TOKEN_RE does not exist: citations "
                         "are still scanned per (document, id)")
    fake_re = _CountingRe(knowledge.re)
    tokens = _CountingPattern(knowledge.KB_HEX_TOKEN_RE)
    with mock.patch.object(knowledge, "re", fake_re), \
         mock.patch.object(knowledge, "KB_HEX_TOKEN_RE", tokens):
        cycle = knowledge.kb_time_cycle(docs)
    return cycle, fake_re.searches, tokens.calls


class T1_TokenPassPerDocument(unittest.TestCase):

    def test_one_extraction_per_living_document(self):
        olds = [row("c.txt", i, i + 1) for i in range(20)]
        news = [row("c.txt", i, i + 1) for i in range(20, 40)]
        rows = [olds[i][1].replace("| OK |", "| SUPERSEDED %s |" % news[i][0])
                for i in range(20)]
        rows += [r[1] for r in news[:18]]
        rows += [row("c.txt", 40 + i, 41 + i, valid="until 2020-01-01")[1]
                 for i in range(2)]
        living = ["cites %s and %s\n" % (olds[i % 20][0], olds[(i + 7) % 20][0])
                  for i in range(30)]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_docs(tmp, rows, living)
            cycle, searches, extractions = counted_cycle(docs)
        self.assertEqual(len({c[0] for c in cycle["cited"]}), 30)
        self.assertEqual(len(cycle["expired"]), 2)
        self.assertLess(searches, 30,
                        "%d re.search calls: one scan per (document, id)" % searches)
        self.assertGreater(extractions, 0)
        # 30 living documents plus the topic file itself
        self.assertLessEqual(extractions, 31)

    def test_young_kb_extracts_nothing(self):
        rows = [row("c.txt", i, i + 1)[1] for i in range(5)]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_docs(tmp, rows, ["plain text\n"] * 30)
            cycle, searches, extractions = counted_cycle(docs)
        self.assertEqual(cycle["cited"], [])
        self.assertEqual(extractions, 0)
        self.assertEqual(searches, 0)


class T2_OneReadPerCitedFile(unittest.TestCase):

    def test_fifty_rows_one_read(self):
        rows = [row("c.txt", i, i + 1)[1] for i in range(50)]
        real = knowledge.sdlc_core.read_text
        seen = []

        def counting(path):
            seen.append(Path(path).name)
            return real(path)
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_docs(tmp, rows)
            with mock.patch.object(knowledge.sdlc_core, "read_text", counting):
                errors, _w, _n = knowledge.kb_check_claims(docs)
        self.assertEqual(errors, [])
        self.assertEqual(seen.count("c.txt"), 1,
                         "c.txt read %d times for 50 rows" % seen.count("c.txt"))


class T3_FindingsStayPerRow(unittest.TestCase):

    def test_missing_extraction_and_past_end_each_row(self):
        rows = [row("m.pdf", i, i + 1)[1] for i in range(3)]
        rows += [row("c.txt", 190 + i, 300 + i)[1] for i in range(3)]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_docs(tmp, rows, given={"c.txt": PAGE, "m.pdf": "%PDF"})
            errors, _w, _n = knowledge.kb_check_claims(docs)
        missing = [e for e in errors if "no stored extraction" in e]
        past = [e for e in errors if "spans past the end" in e]
        self.assertEqual(len(missing), 3)
        self.assertEqual(len(past), 3)
        self.assertEqual(len({e.split(": ")[0] for e in missing + past}), 6)

    def test_line_spans_past_end_each_row(self):
        path = "corpus/given/n.md"
        rows = []
        for i in range(3):
            loc = "L%d-99" % (i + 1)
            rid = kc.kb_claim_id(path, loc, "")
            rows.append("| %s | n%d | - | - | - | %s#%s | GIVEN | OK |"
                        % (rid, i, path, loc))
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_docs(tmp, rows, given={"n.md": "one\ntwo\nthree\n"})
            errors, _w, _n = knowledge.kb_check_claims(docs)
        past = [e for e in errors if "spans past line" in e]
        self.assertEqual(len(past), 3)
        self.assertEqual(len({e.split(": ")[0] for e in past}), 3)


class T4_NoCrossRunMemo(unittest.TestCase):

    def test_grown_file_is_seen_on_the_next_run(self):
        rows = [row("c.txt", 190, 300)[1]]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_docs(tmp, rows)
            first, _w, _n = knowledge.kb_check_claims(docs)
            (docs / "corpus" / "given" / "c.txt").write_text(
                PAGE * 2, encoding="utf-8")
            second, _w, _n = knowledge.kb_check_claims(docs)
        self.assertEqual(len(first), 1)
        self.assertEqual(second, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
