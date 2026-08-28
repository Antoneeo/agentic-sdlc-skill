#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-044 battery — the time cycle (kb second-brain unit 3).

kb-ONLY module, deliberately outside the shared manifest. Guards
ANALYSIS_kb_time_cycle.md's contract:

  FS-1 citation staleness — a living document citing a SUPERSEDED claim id
       without naming EVERY successor warns, per (document, id); the warn
       self-clears when the successors become visible in the same document.
  FS-2 EXPIRED — computed from the existing `valid` window (half-open `until`),
       report-only: never a state write, never a check warning.
  FS-3 chain cascade — a superseded given/ artifact reaches its transitive
       derivations through BOTH derived_from carriers (note frontmatter and
       given/*.meta.md sidecars); dangling edges get a standing walkability
       warn, supersession or not.
  FS-4 `stale` interception — spine output and flags preserved (--hybrid
       included), `## claims` section appended only when nonempty, rc unmoved.
  FS-5 orient count line — present when dirty, absent when clean, fail-open.

    python scripts/test_kb_time_cycle.py
"""
import contextlib
import datetime as dt
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_check as kc  # noqa: E402


def make_tree(tmp, topic_files, notes=None, given=None, docs_extra=None,
              docs_name="ai_docs"):
    """Materialize a minimal docs tree; returns its docs root."""
    docs = Path(tmp) / docs_name
    (docs / "topics").mkdir(parents=True)
    for name, text in topic_files.items():
        (docs / "topics" / name).write_text(text, encoding="utf-8")
    for rel, text in (notes or {}).items():
        p = docs / "corpus" / "notes" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    for rel, data in (given or {}).items():
        p = docs / "corpus" / "given" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, bytes):
            p.write_bytes(data)
        else:
            p.write_text(data, encoding="utf-8")
    for rel, text in (docs_extra or {}).items():
        p = docs / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return docs


def claims_md(rows, topic="t"):
    head = ("---\ntopic: %s\ndescription: d\nparents: []\nstatus: CURRENT\n"
            "---\n\n## Claims\n\n"
            "| id | claim | valid | qty | about | source | prov | state |\n"
            "|---|---|---|---|---|---|---|---|\n" % topic)
    return head + "\n".join("| %s |" % " | ".join(r) for r in rows) + "\n"


GIVEN_TXT = {"c.txt": "page one text here\fpage two, longer text 0123456789"}
SRC1 = "corpus/given/c.txt#p=1@0-8"
SRC2 = "corpus/given/c.txt#p=2@0-10"

OLD_ID = kc.kb_claim_id("corpus/given/c.txt", "p=1@0-8", "")
NEW_ID = kc.kb_claim_id("corpus/given/c.txt", "p=2@0-10", "")


def superseded_pair(extra_rows=()):
    """A legal two-row ledger: OLD_ID superseded by NEW_ID."""
    rows = [(OLD_ID, "old truth", "-", "-", "-", SRC1, "GIVEN",
             "SUPERSEDED " + NEW_ID),
            (NEW_ID, "new truth", "-", "-", "-", SRC2, "GIVEN", "OK")]
    return {"t.md": claims_md(rows + list(extra_rows))}


def run_cli(argv):
    """In-process CLI run capturing stdout+stderr; SystemExit becomes rc."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            rc = kc.main(list(argv))
        except SystemExit as e:
            rc = e.code if isinstance(e.code, int) else 1
    return rc, out.getvalue(), err.getvalue()


# --------------------------------------------------------------------- FS-1

class TC_CitedSuperseded(unittest.TestCase):

    def _cycle(self, docs):
        return kc.kb_time_cycle(docs)

    def test_cited_without_successor_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, superseded_pair(), given=GIVEN_TXT,
                             docs_extra={"solutions/a.md":
                                         "the limit is %s here\n" % OLD_ID})
            cyc = self._cycle(docs)
        self.assertEqual(len(cyc["cited"]), 1)
        doc, old, missing, succs = cyc["cited"][0]
        self.assertIn("solutions/a.md", doc)
        self.assertEqual(old, OLD_ID)
        self.assertIn(NEW_ID, missing)

    def test_successor_named_anywhere_clears(self):
        # A later Diary-style correction entry naming the successor is enough:
        # history stays append-only and the warn dies.
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, superseded_pair(), given=GIVEN_TXT,
                             docs_extra={"solutions/a.md":
                                         "cites %s\n\n## Diary\n- corrected: "
                                         "superseded by %s\n"
                                         % (OLD_ID, NEW_ID)})
            cyc = self._cycle(docs)
        self.assertEqual(cyc["cited"], [])

    def test_owning_topic_file_never_warns(self):
        # The state cell carries the successor id in the same document.
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, superseded_pair(), given=GIVEN_TXT)
            cyc = self._cycle(docs)
        self.assertEqual(cyc["cited"], [])

    def test_other_topic_prose_warns(self):
        # The other topic's ledger must NOT contain the successor id, or the
        # visibility condition legitimately clears -- an unrelated row plus
        # prose citing the fallen id is the UC-A shape.
        other = kc.kb_claim_id("corpus/given/c.txt", "p=2@21-30", "")
        with tempfile.TemporaryDirectory() as tmp:
            files = superseded_pair()
            files["u.md"] = claims_md(
                [(other, "unrelated", "-", "-", "-",
                  "corpus/given/c.txt#p=2@21-30", "GIVEN", "OK")],
                topic="u") + "\nProse grounding on %s stands.\n" % OLD_ID
            docs = make_tree(tmp, files, given=GIVEN_TXT)
            cyc = self._cycle(docs)
        self.assertEqual(len(cyc["cited"]), 1)
        self.assertIn("topics/u.md", cyc["cited"][0][0])

    def test_multi_successor_one_missing_warns_and_names_it(self):
        i3 = kc.kb_claim_id("corpus/given/c.txt", "p=2@11-20", "")
        rows = [(OLD_ID, "old", "-", "-", "-", SRC1, "GIVEN",
                 "SUPERSEDED %s, %s" % (NEW_ID, i3)),
                (NEW_ID, "half one", "-", "-", "-", SRC2, "GIVEN", "OK"),
                (i3, "half two", "-", "-", "-",
                 "corpus/given/c.txt#p=2@11-20", "GIVEN", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT,
                             docs_extra={"solutions/a.md":
                                         "on %s, now %s\n" % (OLD_ID, NEW_ID)})
            cyc = self._cycle(docs)
        self.assertEqual(len(cyc["cited"]), 1)
        _, _, missing, _ = cyc["cited"][0]
        self.assertEqual(tuple(missing), (i3,))

    def test_multi_successor_all_named_clears(self):
        i3 = kc.kb_claim_id("corpus/given/c.txt", "p=2@11-20", "")
        rows = [(OLD_ID, "old", "-", "-", "-", SRC1, "GIVEN",
                 "SUPERSEDED %s, %s" % (NEW_ID, i3)),
                (NEW_ID, "half one", "-", "-", "-", SRC2, "GIVEN", "OK"),
                (i3, "half two", "-", "-", "-",
                 "corpus/given/c.txt#p=2@11-20", "GIVEN", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT,
                             docs_extra={"solutions/a.md":
                                         "%s split into %s + %s\n"
                                         % (OLD_ID, NEW_ID, i3)})
            cyc = self._cycle(docs)
        self.assertEqual(cyc["cited"], [])

    def test_id_inside_longer_hex_run_is_no_citation(self):
        # A git hash embedding the 12 hex chars must not count -- either side,
        # either case.
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, superseded_pair(), given=GIVEN_TXT,
                             docs_extra={"solutions/a.md":
                                         "commit deadbeef%sCAFE told us\n"
                                         % OLD_ID})
            cyc = self._cycle(docs)
        self.assertEqual(cyc["cited"], [])

    def test_generated_files_exempt_by_marker_any_lens(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(
                tmp, superseded_pair(), given=GIVEN_TXT,
                docs_extra={
                    "INDEX.md": "<!-- GENERATED by sdlc_check.py index - do "
                                "not edit by hand -->\nrow %s\n" % OLD_ID,
                    "audit/handoff.md": "<!-- GENERATED by mkt_check.py index "
                                        "- do not edit by hand -->\n%s\n"
                                        % OLD_ID})
            cyc = self._cycle(docs)
        self.assertEqual(cyc["cited"], [])

    def test_tombstone_document_exempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, superseded_pair(), given=GIVEN_TXT,
                             docs_extra={"solutions/old_analysis.md":
                                         "---\nstatus: SUPERSEDED\n---\n"
                                         "grounded on %s\n" % OLD_ID})
            cyc = self._cycle(docs)
        self.assertEqual(cyc["cited"], [])

    def test_given_markdown_and_sidecars_exempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, superseded_pair(),
                             given=dict(GIVEN_TXT,
                                        **{"d.md": "verbatim %s\n" % OLD_ID,
                                           "d.md.meta.md":
                                           "---\nprovenance: GIVEN\n"
                                           "note: %s\n---\n" % OLD_ID}))
            cyc = self._cycle(docs)
        self.assertEqual(cyc["cited"], [])

    def test_note_citing_superseded_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, superseded_pair(), given=GIVEN_TXT,
                             notes={"n.md": "---\norigin: elicited\n"
                                            "date: 2026-08-01\n---\n"
                                            "decision rests on %s\n" % OLD_ID})
            cyc = self._cycle(docs)
        self.assertEqual(len(cyc["cited"]), 1)
        self.assertIn("corpus/notes/n.md", cyc["cited"][0][0])

    def test_graph_carries_the_warn_and_no_claims_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, superseded_pair(), given=GIVEN_TXT,
                             docs_extra={"solutions/a.md":
                                         "on %s\n" % OLD_ID})
            rc, out, _ = run_cli(["graph", "--root", tmp])
        self.assertIn("superseded by", out)
        self.assertNotIn("## claims", out)

    def test_check_carries_the_warn_and_no_claims_section(self):
        # The real `check` on a dirty tree: the FS-1 warn line rides the
        # claims stream, and `## claims` stays stale-only (spine cmd_check
        # calls spine cmd_stale, never the overlay's).
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, superseded_pair(), given=GIVEN_TXT,
                             docs_extra={"solutions/a.md":
                                         "on %s\n" % OLD_ID})
            rc, out, _ = run_cli(["check", "--root", tmp])
        self.assertIn("superseded by", out)
        self.assertNotIn("## claims", out)

    def test_id_at_start_and_end_of_file_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, superseded_pair(), given=GIVEN_TXT,
                             docs_extra={"solutions/s.md": "%s opens\n" % OLD_ID,
                                         "solutions/e.md": "closes %s" % OLD_ID})
            cyc = self._cycle(docs)
        self.assertEqual(len(cyc["cited"]), 2, cyc["cited"])


# --------------------------------------------------------------------- FS-2

class TC_Expired(unittest.TestCase):

    def _tree(self, valid_a, valid_b="-"):
        rows = [(OLD_ID, "windowed", valid_a, "-", "-", SRC1, "GIVEN", "OK"),
                (NEW_ID, "other", valid_b, "-", "-", SRC2, "GIVEN", "OK")]
        return {"t.md": claims_md(rows)}

    def test_until_today_expired_until_tomorrow_live(self):
        today = dt.date.today().isoformat()
        tomorrow = (dt.date.today() + dt.timedelta(days=1)).isoformat()
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, self._tree("until %s" % today,
                                             "until %s" % tomorrow),
                             given=GIVEN_TXT)
            cyc = kc.kb_time_cycle(docs)
        expired_ids = [e[1] for e in cyc["expired"]]
        self.assertIn(OLD_ID, expired_ids)
        self.assertNotIn(NEW_ID, expired_ids)

    def test_if_and_future_from_never_expire(self):
        future = (dt.date.today() + dt.timedelta(days=30)).isoformat()
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, self._tree("if tier 2", "from %s" % future),
                             given=GIVEN_TXT)
            cyc = kc.kb_time_cycle(docs)
        self.assertEqual(cyc["expired"], [])

    def test_expiry_is_never_written_back(self):
        today = dt.date.today().isoformat()
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, self._tree("until %s" % today),
                             given=GIVEN_TXT)
            before = (docs / "topics" / "t.md").read_text(encoding="utf-8")
            kc.kb_time_cycle(docs)
            run_cli(["graph", "--root", tmp])
            after = (docs / "topics" / "t.md").read_text(encoding="utf-8")
        self.assertEqual(before, after)

    def test_expiry_is_not_a_check_warning(self):
        today = dt.date.today().isoformat()
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, self._tree("until %s" % today),
                             given=GIVEN_TXT)
            rc, out, _ = run_cli(["graph", "--root", tmp])
        self.assertNotIn("expired", out.lower())

    def test_expired_reports_its_citing_documents(self):
        today = dt.date.today().isoformat()
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, self._tree("until %s" % today),
                             given=GIVEN_TXT,
                             docs_extra={"solutions/a.md":
                                         "still using %s\n" % OLD_ID})
            cyc = kc.kb_time_cycle(docs)
        self.assertEqual(len(cyc["expired"]), 1)
        cited_by = cyc["expired"][0][3]
        self.assertTrue(any("solutions/a.md" in c for c in cited_by))


# --------------------------------------------------------------------- FS-3

def chain_fixture(tmp, dangling=False, cycle=False, tombstone=False,
                  quoted=False):
    """scan.png superseded by scan2.png; extract.txt derives from scan.png
    (SIDECAR edge); note n.md derives from extract.txt (note edge)."""
    edge = '"corpus/given/extract.txt"' if quoted else "corpus/given/extract.txt"
    notes = {"n.md": "---\norigin: elicited\ndate: 2026-08-01\n"
                     "derived_from: [%s]\n---\nsynthesis\n" % edge}
    if dangling:
        notes["d.md"] = ("---\norigin: elicited\ndate: 2026-08-01\n"
                         "derived_from: gone.txt\n---\nx\n")
    if cycle:
        notes["a.md"] = ("---\nderived_from: corpus/notes/b.md\n---\nx\n")
        notes["b.md"] = ("---\nderived_from: [corpus/notes/a.md, "
                         "corpus/given/extract.txt]\n---\nx\n")
    if tombstone:
        notes["dead.md"] = ("---\nstatus: SUPERSEDED\n"
                            "derived_from: corpus/given/extract.txt\n---\nx\n")
    given = {
        "scan.png": b"\x89PNG old",
        "scan.png.meta.md": "---\nprovenance: GIVEN\ndate: 2026-07-01\n---\n",
        "scan2.png": b"\x89PNG new",
        "scan2.png.meta.md": ("---\nprovenance: GIVEN\ndate: 2026-08-01\n"
                              "supersedes: scan.png\n---\n"),
        "extract.txt": "extracted text\n",
        "extract.txt.meta.md": ("---\nprovenance: DERIVED\n"
                                "derived_from: scan.png\n---\n"),
    }
    return make_tree(tmp, {}, notes=notes, given=given)


class TC_ChainCascade(unittest.TestCase):

    def test_transitive_chain_crosses_the_sidecar_hop(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = chain_fixture(tmp)
            cyc = kc.kb_time_cycle(docs)
        paths = [c[0] for c in cyc["chain"]]
        self.assertTrue(any("corpus/notes/n.md" in p for p in paths), paths)
        self.assertTrue(any("corpus/given/extract.txt" in p for p in paths),
                        paths)

    def test_quoted_edge_resolves(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = chain_fixture(tmp, quoted=True)
            cyc = kc.kb_time_cycle(docs)
        self.assertTrue(any("corpus/notes/n.md" in c[0]
                            for c in cyc["chain"]), cyc["chain"])

    def test_bare_name_resolves_notes_first_then_given(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = chain_fixture(tmp)
            # bare "extract.txt": no corpus/notes/extract.txt, so given/ wins.
            (docs / "corpus" / "notes" / "m.md").write_text(
                "---\nderived_from: extract.txt\n---\nx\n", encoding="utf-8")
            cyc = kc.kb_time_cycle(docs)
        self.assertTrue(any("corpus/notes/m.md" in c[0]
                            for c in cyc["chain"]), cyc["chain"])

    def test_cycle_terminates_and_lists_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = chain_fixture(tmp, cycle=True)
            cyc = kc.kb_time_cycle(docs)
        a_rows = [c for c in cyc["chain"] if "corpus/notes/a.md" in c[0]]
        self.assertEqual(len(a_rows), 1, cyc["chain"])

    def test_dangling_edge_warns_with_no_supersession_anywhere(self):
        with tempfile.TemporaryDirectory() as tmp:
            notes = {"d.md": "---\norigin: elicited\ndate: 2026-08-01\n"
                             "derived_from: gone.txt\n---\nx\n"}
            docs = make_tree(tmp, {}, notes=notes)
            cyc = kc.kb_time_cycle(docs)
            rc, out, _ = run_cli(["corpus", "--root", tmp])
        self.assertEqual(len(cyc["dangling"]), 1)
        self.assertIn("not walkable", out)

    def test_tombstone_derivation_not_listed(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = chain_fixture(tmp, tombstone=True)
            cyc = kc.kb_time_cycle(docs)
        self.assertFalse(any("dead.md" in c[0] for c in cyc["chain"]),
                         cyc["chain"])

    def test_non_canonical_resolving_edge_is_normalized(self):
        # Closure-review WARN-1: `./corpus/given/extract.txt` resolves on the
        # filesystem but would never match the canonical node key -- the walk
        # silently stopped with neither a chain entry nor a dangling warn.
        with tempfile.TemporaryDirectory() as tmp:
            docs = chain_fixture(tmp)
            (docs / "corpus" / "notes" / "p.md").write_text(
                "---\nderived_from: ./corpus/given/extract.txt\n---\nx\n",
                encoding="utf-8")
            cyc = kc.kb_time_cycle(docs)
        self.assertTrue(any("corpus/notes/p.md" in c[0]
                            for c in cyc["chain"]), cyc["chain"])
        self.assertEqual(cyc["dangling"], [])


# --------------------------------------------------------------------- FS-4

class TC_StaleInterception(unittest.TestCase):

    def _dirty_tmp(self):
        tmp = tempfile.mkdtemp()
        make_tree(tmp, superseded_pair(), given=GIVEN_TXT,
                  docs_extra={"solutions/a.md": "on %s\n" % OLD_ID,
                              "solutions/b.md": "and %s\n" % OLD_ID})
        return tmp

    def test_claims_section_appended_when_dirty(self):
        tmp = self._dirty_tmp()
        rc, out, _ = run_cli(["stale", "--root", tmp])
        self.assertIn("## claims", out)
        self.assertIn("superseded by", out)

    def test_clean_corpus_adds_zero_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_tree(tmp, superseded_pair(), given=GIVEN_TXT,
                      docs_extra={"solutions/a.md":
                                  "cites %s then %s\n" % (OLD_ID, NEW_ID)})
            rc, out, _ = run_cli(["stale", "--root", tmp])
        self.assertNotIn("## claims", out)

    def test_hybrid_flag_is_forwarded_not_a_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_tree(tmp, {}, notes=None)
            rc, out, err = run_cli(["stale", "--root", tmp, "--hybrid"])
        self.assertNotEqual(rc, 2, err)
        self.assertNotIn("usage:", err.lower())

    def test_rc_unmoved_by_a_nonempty_section(self):
        tmp = self._dirty_tmp()
        rc_dirty, out, _ = run_cli(["stale", "--root", tmp])
        with tempfile.TemporaryDirectory() as tmp2:
            make_tree(tmp2, superseded_pair(), given=GIVEN_TXT)
            rc_clean, _, _ = run_cli(["stale", "--root", tmp2])
        self.assertIn("## claims", out)
        self.assertEqual(rc_dirty, rc_clean)

    def test_deterministic_order_by_path(self):
        tmp = self._dirty_tmp()
        rc, out, _ = run_cli(["stale", "--root", tmp])
        a = out.find("solutions/a.md")
        b = out.find("solutions/b.md")
        self.assertTrue(0 <= a < b, out)

    def test_section_shapes_expired_and_chain_lines(self):
        # The `## claims` section renders all three list kinds: cited lines,
        # expired lines with their (uncited)/(cited by:) tail, chain lines.
        today = dt.date.today().isoformat()
        with tempfile.TemporaryDirectory() as tmp:
            docs = chain_fixture(tmp)
            rows = [(OLD_ID, "windowed", "until %s" % today, "-", "-",
                     SRC1, "GIVEN", "OK")]
            (docs / "topics").mkdir(exist_ok=True)
            (docs / "topics" / "t.md").write_text(claims_md(rows),
                                                  encoding="utf-8")
            (docs / "corpus" / "given" / "c.txt").write_text(
                GIVEN_TXT["c.txt"], encoding="utf-8")
            rc, out, _ = run_cli(["stale", "--root", tmp])
        self.assertIn("## claims", out)
        self.assertIn("expired %s (uncited)" % today, out)
        self.assertIn("derives (via", out)

    def test_docs_dir_flag_is_mirrored(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_tree(tmp, superseded_pair(), given=GIVEN_TXT,
                      docs_extra={"solutions/a.md": "on %s\n" % OLD_ID},
                      docs_name="kb_docs")
            rc, out, err = run_cli(["stale", "--root", tmp,
                                    "--docs-dir", "kb_docs"])
        self.assertNotEqual(rc, 2, err)
        self.assertIn("## claims", out)


# --------------------------------------------------------------------- FS-5

class TC_OrientLine(unittest.TestCase):

    def test_counts_when_dirty(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_tree(tmp, superseded_pair(), given=GIVEN_TXT,
                      docs_extra={"solutions/a.md": "on %s\n" % OLD_ID})
            rc, out, _ = run_cli(["orient", "--root", tmp])
        self.assertIn("kb time:", out)
        self.assertIn("stale", out)

    def test_silent_when_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_tree(tmp, superseded_pair(), given=GIVEN_TXT)
            rc, out, _ = run_cli(["orient", "--root", tmp])
        self.assertNotIn("kb time:", out)

    def test_counts_distinct_docs_not_citations(self):
        # One document citing the fallen id twice is ONE doc in the count.
        with tempfile.TemporaryDirectory() as tmp:
            make_tree(tmp, superseded_pair(), given=GIVEN_TXT,
                      docs_extra={"solutions/a.md":
                                  "on %s and again %s\n" % (OLD_ID, OLD_ID)})
            rc, out, _ = run_cli(["orient", "--root", tmp])
        self.assertIn("kb time: 1 docs cite superseded claims", out)

    def test_fail_open_on_a_broken_ledger(self):
        # A junk `valid` cell must not break orient (the collector skips the
        # row; the syntax error stays the claims check's finding).
        rows = [(OLD_ID, "junk window", "not a scope", "-", "-", SRC1,
                 "GIVEN", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT)
            rc, out, _ = run_cli(["orient", "--root", tmp])
        self.assertNotIn("Traceback", out)


if __name__ == "__main__":
    unittest.main()
