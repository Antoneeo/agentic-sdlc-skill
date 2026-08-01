#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-024 battery — the topic graph, its indexes, and the overlay's command
surface. Stdlib, no LLM, no network; the overlay commands are exercised
through main(), because the shared batteries bind sdlc_core and structurally
cannot cover them (TS-K10).

    python scripts/test_kb_graph.py
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


def node(slug, parents=(), status="CURRENT", redirect=None, owns=(),
         synonyms=(), related=None, description="d"):
    lines = ["---", "topic: " + slug, "description: " + description,
             "parents: [%s]" % ", ".join(parents), "status: " + status]
    if redirect:
        lines.append("redirect_to: " + redirect)
    if owns:
        lines.append("owns: [%s]" % ", ".join(owns))
    if synonyms:
        lines.append("synonyms: [%s]" % ", ".join(synonyms))
    if related:
        lines.append("related: " + related)
    lines += ["---", "", "body", ""]
    return "\n".join(lines)


def make_topics(tmp, files):
    docs = Path(tmp) / "ai_docs"
    (docs / "topics").mkdir(parents=True)
    for name, text in files.items():
        (docs / "topics" / name).write_text(text, encoding="utf-8")
    return docs


class TS_K1_Polyhierarchy(unittest.TestCase):
    def test_two_parents_both_resolve_and_node_is_reachable(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {
                "a.md": node("a"), "b.md": node("b"),
                "c.md": node("c", parents=("a", "b"))})
            errors, _ = kc.kb_graph_check(docs)
        self.assertEqual(errors, [], errors)


class TS_K5_CyclesAndReachability(unittest.TestCase):
    def test_cycle_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {
                "a.md": node("a", parents=("b",)),
                "b.md": node("b", parents=("a",))})
            errors, _ = kc.kb_graph_check(docs)
        self.assertTrue(any("cycle" in e for e in errors), errors)

    def test_unreachable_node_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {
                "root.md": node("root"),
                "a.md": node("a", parents=("b",)),   # a->b->a ring, detached
                "b.md": node("b", parents=("a",))})
            errors, _ = kc.kb_graph_check(docs)
        self.assertTrue(any("unreachable" in e for e in errors), errors)

    def test_unplaced_is_exempt_from_reachability(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {
                "root.md": node("root"), "unplaced.md": node("unplaced")})
            errors, _ = kc.kb_graph_check(docs)
        self.assertEqual(errors, [], errors)


class TS_K6_Grammar(unittest.TestCase):
    def test_bad_slug_and_bad_owns_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {
                "Bad_Slug.md": node("Bad_Slug"),
                "a.md": node("a", owns=("no-slash-concept",))})
            errors, _ = kc.kb_graph_check(docs)
        self.assertTrue(any("fails the grammar" in e for e in errors), errors)
        self.assertTrue(any("owns entry" in e for e in errors), errors)

    def test_double_owner_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {
                "a.md": node("a", owns=("a/x",)),
                "b.md": node("b", owns=("a/x",))})
            errors, _ = kc.kb_graph_check(docs)
        self.assertTrue(any("owned twice" in e for e in errors), errors)


class TS_K8_Tombstones(unittest.TestCase):
    def test_parent_through_tombstone_resolves(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {
                "old.md": node("old", status="SUPERSEDED", redirect="new"),
                "new.md": node("new"),
                "child.md": node("child", parents=("old",))})
            errors, _ = kc.kb_graph_check(docs)
        self.assertEqual(errors, [], errors)

    def test_tombstone_to_nowhere_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {
                "old.md": node("old", status="SUPERSEDED", redirect="ghost")})
            errors, _ = kc.kb_graph_check(docs)
        self.assertTrue(any("redirect_to" in e for e in errors), errors)


class TS_K3_NoCoverageSurface(unittest.TestCase):
    def test_index_carries_no_coverage_token_and_no_per_node_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {"a.md": node("a", synonyms=("alpha",))})
            idx = kc.kb_build_topic_index(docs)
        for token in ("STUB", "PARTIAL", "FULL", "coverage"):
            self.assertNotIn(token, idx)
        self.assertIn("alpha", idx)  # synonyms ARE in the router (naming, not state)

    def test_graph_output_is_findings_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {"a.md": node("a"), "b.md": node("b")})
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = kc.kb_cmd_graph(docs)
        self.assertEqual(rc, 0)
        out = buf.getvalue()
        # one [ok] line; never one line per node
        self.assertNotIn("a:", out)
        self.assertNotIn("STUB", out)


class TS_K11_GeneratedIndexes(unittest.TestCase):
    def test_hand_edited_index_fails_validate_extra(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {"a.md": node("a")})
            (docs / "topics" / "INDEX.md").write_text(
                kc.kb_build_topic_index(docs) + "\nhand edit\n", encoding="utf-8")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = kc._kb_extra_validate(docs)
        self.assertEqual(rc, 1)
        self.assertIn("not aligned", buf.getvalue())


class TS_K12_CandidateSetFromDisk(unittest.TestCase):
    def test_reload_equals_pre_crash_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = {"a.md": node("a"), "b.md": node("b", parents=("a",))}
            docs = make_topics(tmp, files)
            before = set(kc.kb_load_topics(docs))
            # simulate crash: nothing persisted but the files
            after = set(kc.kb_load_topics(docs))
        self.assertEqual(before, after)
        self.assertEqual(before, {"a", "b"})


class TS_K10_CommandSurface(unittest.TestCase):
    def run_main(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            try:
                rc = kc.main(argv)
            except SystemExit as e:  # argparse exits on usage errors
                rc = e.code
        return rc, buf.getvalue()

    def test_overlay_reaches_kb_and_spine_stays_importable(self):
        self.assertTrue(callable(kc.kb_cmd_check))
        import sdlc_core
        self.assertIsNot(kc.main, sdlc_core.main)
        self.assertTrue(callable(sdlc_core.cmd_validate))

    def test_every_documented_subcommand_exits_non_2(self):
        """SKILL.md's command list must be real — mkt ships a documented
        command that dies in argparse; kb must not."""
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {"a.md": node("a")})
            root = str(docs.parent)
            for argv in (["validate", "--root", root],
                         ["check", "--root", root],
                         ["index", "--root", root],
                         ["graph", "--root", root],
                         ["corpus", "--root", root],
                         ["stale", "--root", root],
                         ["orient", "--root", root]):
                rc, _ = self.run_main(argv)
                self.assertNotEqual(rc, 2, "usage error on %r" % argv)

    def test_migrate_is_forwarded_not_dropped(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {"a.md": node("a")})
            rc, out = self.run_main(["migrate", "--from", "ai_docs",
                                     "--to", "kb_docs", "--root",
                                     str(docs.parent)])
        self.assertNotEqual(rc, 2, out)

    def test_docs_dir_works_on_an_intercepted_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "kb_docs"
            (docs / "topics").mkdir(parents=True)
            (docs / "topics" / "a.md").write_text(node("a"), encoding="utf-8")
            rc, out = self.run_main(["graph", "--root", tmp,
                                     "--docs-dir", "kb_docs"])
        self.assertEqual(rc, 0, out)
        self.assertIn("consistent", out)


class TS_K9_SelectionNotRollup(unittest.TestCase):
    def test_parent_selection_returns_only_its_own_rows(self):
        """UC2 is a selection over claim rows, never a walk over parents."""
        claims = ("## Claims\n\n"
                  "| id | claim | valid | qty | about | source | prov | state |\n"
                  "|---|---|---|---|---|---|---|---|\n"
                  "| aaaaaaaaaaaa | child effort | - | 5 d effort | - | "
                  "corpus/notes/n.md#L1-1 | ELICITED | OK |\n")
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_topics(tmp, {
                "parent.md": node("parent"),
                "child.md": node("child", parents=("parent",))})
            # child carries the qty row; parent carries none
            p = docs / "topics" / "child.md"
            p.write_text(p.read_text(encoding="utf-8") + claims, encoding="utf-8")
            parent_rows, _ = kc.kb_parse_claims(
                (docs / "topics" / "parent.md").read_text(encoding="utf-8"))
        self.assertEqual(parent_rows, [])  # nothing rolls up


if __name__ == "__main__":
    unittest.main(verbosity=1)
