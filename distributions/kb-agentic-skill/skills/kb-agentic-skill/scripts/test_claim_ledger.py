#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-025 battery — the claim ledger. Pure functions, stdlib, no LLM, no net.

    python scripts/test_claim_ledger.py
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_check as kc  # noqa: E402  the kb overlay under test


def make_tree(tmp, topic_files, notes=None, given=None):
    """Materialize a minimal docs tree; returns its docs root."""
    docs = Path(tmp) / "ai_docs"
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
    return docs


def claims_md(rows):
    head = ("---\ntopic: t\ndescription: d\nparents: []\nstatus: CURRENT\n---\n\n"
            "## Claims\n\n"
            "| id | claim | valid | qty | about | source | prov | state |\n"
            "|---|---|---|---|---|---|---|---|\n")
    return head + "\n".join("| %s |" % " | ".join(r) for r in rows) + "\n"


GIVEN_TXT = {"c.txt": "page one text here\fpage two, longer text 0123456789"}
SRC1 = "corpus/given/c.txt#p=1@0-8"
SRC2 = "corpus/given/c.txt#p=2@0-10"


class TL_T1_Identity(unittest.TestCase):
    def test_text_excluded_locator_and_qty_included(self):
        a = kc.kb_claim_id("p.pdf", "p=1@0-9", "")
        self.assertEqual(a, kc.kb_claim_id("p.pdf", "p=1@0-9", ""))  # text-free
        self.assertNotEqual(a, kc.kb_claim_id("p.pdf", "p=1@0-10", ""))
        self.assertNotEqual(kc.kb_claim_id("p.pdf", "p=1@0-9", "cost:12000:EUR"),
                            kc.kb_claim_id("p.pdf", "p=1@0-9", "effort:30:d"))


class TL_T2_Scopes(unittest.TestCase):
    def test_half_open_boundary_is_disjoint(self):
        self.assertFalse(kc.kb_scopes_overlap("until 2026-03-01", "from 2026-03-01"))

    def test_unbounded_and_if_overlap_everything(self):
        self.assertTrue(kc.kb_scopes_overlap("-", "from 2026-03-01"))
        self.assertTrue(kc.kb_scopes_overlap("if tier 2", "until 2020-01-01"))

    def test_windows(self):
        self.assertTrue(kc.kb_scopes_overlap("from 2026-01-01 until 2026-06-01",
                                             "from 2026-05-01"))
        self.assertFalse(kc.kb_scopes_overlap("until 2026-01-01", "from 2026-02-01"))


class TL_T3_Symmetry(unittest.TestCase):
    def three_way(self, flip_one=False):
        ids = [kc.kb_claim_id("corpus/given/c.txt", "p=1@0-8", ""),
               kc.kb_claim_id("corpus/given/c.txt", "p=2@0-10", ""),
               kc.kb_claim_id("corpus/given/c.txt", "p=2@2-9", "")]
        rows = [
            (ids[0], "A", "-", "-", "-", SRC1, "GIVEN",
             "OK" if flip_one else "CONTESTED %s,%s" % (ids[1], ids[2])),
            (ids[1], "B", "-", "-", "-", SRC2, "GIVEN",
             "CONTESTED %s,%s" % (ids[0], ids[2])),
            (ids[2], "C", "-", "-", "-", "corpus/given/c.txt#p=2@2-9", "GIVEN",
             "CONTESTED %s,%s" % (ids[0], ids[1])),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT)
            return kc.kb_check_claims(docs)

    def test_symmetric_set_passes(self):
        errors, _, _ = self.three_way()
        self.assertEqual(errors, [], errors)

    def test_one_flipped_cell_fails(self):
        """The cheapest laundering: no deletion, one state cell edited to OK."""
        errors, _, _ = self.three_way(flip_one=True)
        self.assertTrue(any("not symmetric" in e for e in errors), errors)


class TL_T6_Fill(unittest.TestCase):
    def test_fill_confined_and_idempotent(self):
        rows = [("", "A claim", "-", "-", "-", SRC1, "GIVEN", "OK")]
        text = claims_md(rows)
        filled = kc.kb_fill_ids(text)
        want = kc.kb_claim_id("corpus/given/c.txt", "p=1@0-8", "")
        self.assertIn(want, filled)
        # confined: the only differing lines differ only in the id cell
        for a, b in zip(text.split("\n"), filled.split("\n")):
            if a != b:
                ca = [c.strip() for c in a.strip("|").split("|")]
                cb = [c.strip() for c in b.strip("|").split("|")]
                self.assertEqual(ca[1:], cb[1:], "fill touched a non-id cell")
        self.assertEqual(filled, kc.kb_fill_ids(filled))  # idempotent

    def test_empty_id_is_a_note_never_an_error(self):
        rows = [("", "A claim", "-", "-", "-", SRC1, "GIVEN", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT)
            errors, _, notes = kc.kb_check_claims(docs)
        self.assertEqual(errors, [], errors)
        self.assertTrue(any("fill-pending" in n for n in notes))


class TL_T7_Traversal(unittest.TestCase):
    def test_traversing_source_refused(self):
        rows = [("x" * 12, "A", "-", "-", "-", "../../secrets.txt#L1-2", "GIVEN", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT)
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertTrue(any("escapes the docs root" in e for e in errors), errors)

    def test_moved_source_breaks_the_id(self):
        good = kc.kb_claim_id("corpus/given/c.txt", "p=1@0-8", "")
        rows = [(good, "A", "-", "-", "-", SRC2, "GIVEN", "OK")]  # moved to p=2
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT)
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertTrue(any("does not recompute" in e for e in errors), errors)

    def test_span_past_extraction_end_errors(self):
        rows = [("", "A", "-", "-", "-", "corpus/given/c.txt#p=1@0-99999",
                 "GIVEN", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT)
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertTrue(any("spans past" in e for e in errors), errors)


class TL_T8_Provenance(unittest.TestCase):
    def test_derived_without_derived_from_errors(self):
        rows = [("", "A", "-", "-", "-", "corpus/notes/n.md#L1-2", "DERIVED", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)},
                             notes={"n.md": "---\nstatus: CURRENT\n---\nbody\n"})
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertTrue(any("derived_from" in e for e in errors), errors)

    def test_ruling_without_basis_errors(self):
        rows = [("", "A", "-", "-", "-", "corpus/notes/r.md#L1-2", "RULING", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)},
                             notes={"r.md": "---\nstatus: CURRENT\n---\nruled\n"})
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertTrue(any("no basis, no ruling" in e for e in errors), errors)

    def test_dangling_and_superseded_pointers_error(self):
        i1 = kc.kb_claim_id("corpus/given/c.txt", "p=1@0-8", "")
        i2 = kc.kb_claim_id("corpus/given/c.txt", "p=2@0-10", "")
        rows = [(i1, "A", "-", "-", "-", SRC1, "GIVEN", "CONTESTED ffffffffffff"),
                (i2, "B", "-", "-", "-", SRC2, "GIVEN", "SUPERSEDED " + i1)]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT)
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertTrue(any("resolves to no row" in e for e in errors), errors)
        # now a CONTESTED pointing at a SUPERSEDED row
        rows = [(i1, "A", "-", "-", "-", SRC1, "GIVEN", "CONTESTED " + i2),
                (i2, "B", "-", "-", "-", SRC2, "GIVEN", "SUPERSEDED " + i1)]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT)
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertTrue(any("points at SUPERSEDED" in e for e in errors), errors)

    def test_duplicate_id_across_nodes_errors(self):
        i1 = kc.kb_claim_id("corpus/given/c.txt", "p=1@0-8", "")
        row = (i1, "A", "-", "-", "-", SRC1, "GIVEN", "OK")
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md([row]),
                                   "u.md": claims_md([row])}, given=GIVEN_TXT)
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertTrue(any("duplicate id" in e for e in errors), errors)


class TL_T9_Arity(unittest.TestCase):
    def test_short_and_long_rows_both_error(self):
        base = claims_md([("", "ok row", "-", "-", "-", SRC1, "GIVEN", "OK")])
        short = base + "| a | b | c |\n"
        long_ = base + "| a | b|c | d | e | f | g | h | i |\n"
        for bad in (short, long_):
            rows, errs = kc.kb_parse_claims(bad)
            self.assertEqual(len(rows), 1)
            self.assertTrue(any("cells, expected" in m for _, m in errs), errs)


class TL_T10_Quantities(unittest.TestCase):
    def test_normalise_and_sum(self):
        total, unit = kc.kb_qty_sum(["2 w effort", "5 d effort", "8 h effort"])
        self.assertEqual((total, unit), (16.0, "d"))

    def test_mixed_currency_refuses(self):
        with self.assertRaises(ValueError):
            kc.kb_qty_sum(["100 EUR cost", "100 USD cost"])

    def test_mixed_kinds_refuse(self):
        with self.assertRaises(ValueError):
            kc.kb_qty_sum(["1 d effort", "1 d duration"])


class TL_Corpus(unittest.TestCase):
    def test_superseded_source_is_reported(self):
        i1 = kc.kb_claim_id("corpus/given/old.txt", "p=1@0-4", "")
        rows = [(i1, "A", "-", "-", "-", "corpus/given/old.txt#p=1@0-4",
                 "GIVEN", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)},
                             given={"old.txt": "old text",
                                    "new.txt": "new text",
                                    "new.txt.meta.md":
                                        "---\ndate: 2026-08-01\nsupersedes: old.txt\n---\n"})
            _, warnings = kc.kb_corpus_check(docs)
        self.assertTrue(any("supersedes" in w or "newer version" in w
                            for w in warnings), warnings)

    def test_raw_digest_detects_edit_and_differs_from_lf_normalized(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "b.bin"
            p.write_bytes(b"one\r\ntwo\r\n")
            q = Path(tmp) / "c.bin"
            q.write_bytes(b"one\ntwo\n")
            self.assertNotEqual(kc.kb_sha256_bytes(p), kc.kb_sha256_bytes(q))

    def test_note_with_no_provenance_keys_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {}, notes={"n.md": "---\nstatus: CURRENT\n---\nx\n"})
            errors, _ = kc.kb_corpus_check(docs)
        self.assertTrue(any("disguised as a source" in e for e in errors), errors)


PAGED = ("Introduction\nThe multi-company feature is disabled by\n"
         "default and must be enabled in the site\nwizard before use.\n"
         "\fAppendix\nOperator groups must also be multi-company.\n")


class TL_F029_Anchor(unittest.TestCase):
    """F-029 D: prose citation -> verified span. One test per branch, because a
    single test tripping two branches lets either be deleted with the suite
    green (the F-027 lesson)."""

    def _paged(self, tmp):
        p = Path(tmp) / "m-ab12cd34.txt"
        p.write_text(PAGED, encoding="utf-8", newline="")
        return p

    def test_resolves_a_phrase_broken_across_a_line_wrap(self):
        """The field defect: 'disabled by default' is split by the extraction's
        line wrap, so a literal-space anchor finds nothing."""
        with tempfile.TemporaryDirectory() as tmp:
            p = self._paged(tmp)
            self.assertNotIn("disabled by default", p.read_text(encoding="utf-8"))
            hits = kc.kb_resolve_anchor(p, "disabled by default", page=1)
        self.assertEqual(len(hits), 1, hits)
        self.assertTrue(hits[0][0].startswith("p=1@"), hits)

    def test_every_emitted_locator_survives_the_checker(self):
        """The round-trip: this tool may never emit a span its own validator
        would reject."""
        with tempfile.TemporaryDirectory() as tmp:
            p = self._paged(tmp)
            for loc, _ in kc.kb_resolve_anchor(p, "multi-company"):
                errs = []
                kc.kb_check_locator(p, loc, "t", errs)
                self.assertEqual(errs, [], f"{loc} emitted but rejected: {errs}")

    def test_absent_phrase_resolves_to_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self._paged(tmp)
            self.assertEqual(kc.kb_resolve_anchor(p, "biometric login"), [])

    def test_page_filter_separates_two_occurrences(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self._paged(tmp)
            self.assertEqual(len(kc.kb_resolve_anchor(p, "multi-company", page=2)), 1)
            self.assertGreater(len(kc.kb_resolve_anchor(p, "multi-company")), 1)

    def test_line_files_get_a_line_locator(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "n.md"
            p.write_text("alpha\nbeta gamma\ndelta\n", encoding="utf-8", newline="")
            hits = kc.kb_resolve_anchor(p, "beta gamma")
        self.assertEqual([h[0] for h in hits], ["L2-2"], hits)


class TL_F029_CorpusLetter(unittest.TestCase):
    """F-029 C: the extraction may BE the artifact — the original never enters
    the docs root. What the digest protects is the bytes a locator addresses."""

    def test_extraction_is_a_legal_artifact_with_no_original_present(self):
        data = PAGED.encode("utf-8")
        import hashlib
        meta = ("---\nsha256: %s\ndate: 2026-08-02\nprovenance: GIVEN\n"
                "original_path: /vault/m.pdf\noriginal_sha256: %s\n---\n"
                % (hashlib.sha256(data).hexdigest(), "0" * 64))
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {}, given={"m-ab12cd34.txt": data,
                                             "m-ab12cd34.txt.meta.md": meta})
            errors, warnings = kc.kb_corpus_check(docs)
        self.assertEqual(errors, [], errors)

    def test_a_tampered_extraction_is_still_caught(self):
        """The relaxation must not cost the guarantee: the enforced digest moved
        onto the extraction, it did not disappear."""
        import hashlib
        meta = ("---\nsha256: %s\ndate: 2026-08-02\nprovenance: GIVEN\n---\n"
                % hashlib.sha256(b"the original bytes").hexdigest())
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {}, given={"m-ab12cd34.txt": b"tampered",
                                             "m-ab12cd34.txt.meta.md": meta})
            errors, _ = kc.kb_corpus_check(docs)
        self.assertTrue(any("digest changed" in e for e in errors), errors)


class TL_F029_Dispatch(unittest.TestCase):
    """F-029 E: `--help` must show the overlay, WITHOUT costing
    forward-by-default — the property that keeps a future spine command from
    being silently dropped."""

    def _run(self, argv):
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = kc.main(argv)
        return rc, buf.getvalue()

    def test_help_lists_the_overlay_commands(self):
        rc, out = self._run(["--help"])
        self.assertEqual(rc, 0)
        for cmd in ("graph", "corpus", "claim-id", "anchor"):
            self.assertIn(cmd, out, f"--help hides '{cmd}': a reader concludes "
                                    "the knowledge overlay is not installed")

    def test_help_still_shows_the_spine_commands(self):
        _, out = self._run(["--help"])
        for cmd in ("stale", "mark", "orient"):
            self.assertIn(cmd, out, "the overlay's help replaced the spine's "
                                    "instead of extending it")

    def test_forward_by_default_survives(self):
        """A command the overlay does not intercept still reaches the spine."""
        with tempfile.TemporaryDirectory() as tmp:
            rc, out = self._run(["orient", "--root", tmp])
        self.assertEqual(rc, 0)
        self.assertNotIn("knowledge overlay", out)

    def test_skill_md_names_every_intercepted_command(self):
        """F-029 follow-up: `anchor` shipped working, listed in `--help`, and
        absent from SKILL.md -- so an agent reading only the doctrine never
        learned it exists. Derived from INTERCEPTED, never from a second hand-
        maintained list: that duplication is the defect, not the omission."""
        skill = Path(__file__).resolve().parents[1] / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        for cmd in sorted(kc.INTERCEPTED):
            self.assertIn(f"`{cmd}`", text,
                          f"SKILL.md never names `{cmd}`, which the entry point "
                          f"intercepts: the doctrine and the machinery disagree "
                          f"about what this skill can do")


class TL_F029_AnchorPath(unittest.TestCase):
    """F-029 follow-up: reported from the field as an asymmetry -- `anchor`
    had to be run from inside the docs root while its siblings take `--root`."""

    def test_path_resolves_under_the_docs_root_from_outside_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {}, given={"m-ab12cd34.txt": PAGED})
            args = type("A", (), {"path": "corpus/given/m-ab12cd34.txt",
                                  "phrase": "Operator groups", "root": tmp,
                                  "docs_dir": docs.name, "page": None,
                                  "ignore_case": False, "all": False})()
            import contextlib, io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = kc.kb_cmd_anchor(args)
        self.assertEqual(rc, 0, buf.getvalue())
        self.assertIn("p=2@", buf.getvalue())


def _portable_tree(tmp, name="A"):
    """A project holding one topic whose two claims cite one artifact."""
    import hashlib
    data = PAGED.encode("utf-8")
    root = Path(tmp) / name
    docs = root / "ai_docs"
    (docs / "corpus" / "given").mkdir(parents=True)
    (docs / "topics").mkdir(parents=True)
    art = docs / "corpus" / "given" / "m-ab12cd34.txt"
    art.write_bytes(data)
    (docs / "corpus" / "given" / "m-ab12cd34.txt.meta.md").write_text(
        "---\nsha256: %s\ndate: 2026-08-03\nprovenance: GIVEN\n"
        "extracted_through: complete\n---\n"
        % hashlib.sha256(data).hexdigest(), encoding="utf-8")
    src = "corpus/given/m-ab12cd34.txt"
    rows = [(kc.kb_claim_id(src, "p=1@42-61", ""), "disabled by default",
             "-", "-", "-", src + "#p=1@42-61", "GIVEN", "OK"),
            (kc.kb_claim_id(src, "p=2@9-51", ""), "operator groups too",
             "-", "-", "-", src + "#p=2@9-51", "GIVEN", "OK")]
    (docs / "topics" / "t.md").write_text(claims_md(rows), encoding="utf-8")
    return root, docs


class TL_F030_Portability(unittest.TestCase):
    """F-030. The load-bearing property is id stability: kb_claim_id hashes
    path#locator#qty with the TEXT EXCLUDED, so the same artifact cited at the
    same span mints the same id in every project. Dedup is therefore mechanical,
    and that is why this feature is small."""

    def test_round_trip_preserves_claim_ids_across_projects(self):
        with tempfile.TemporaryDirectory() as tmp:
            _rootA, docsA = _portable_tree(tmp, "A")
            selected, artifacts, added, errors = kc.kb_export_closure(docsA, ["t"])
            self.assertEqual(errors, [], errors)
            bundle = Path(tmp) / "bundle"
            kc.kb_bundle_write(docsA, bundle, selected, artifacts, "A")
            docsB = Path(tmp) / "B" / "ai_docs"
            docsB.mkdir(parents=True)
            writes, skipped, dedup, errors = kc.kb_import_plan(bundle, docsB)
            self.assertEqual(errors, [], errors)
            for _rel, src, dst in writes:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(src.read_bytes())
            ida = {r["id"] for r in kc.kb_collect_topics(docsA)["t"][2]}
            idb = {r["id"] for r in kc.kb_collect_topics(docsB)["t"][2]}
        self.assertEqual(ida, idb, "claim ids must survive the project boundary")

    def test_export_carries_the_bytes_its_claims_cite(self):
        """Closure, not selection: a claim whose source cannot be reopened is
        model knowledge arriving by another route."""
        with tempfile.TemporaryDirectory() as tmp:
            _root, docs = _portable_tree(tmp)
            _sel, artifacts, _added, _errs = kc.kb_export_closure(docs, ["t"])
        self.assertIn("corpus/given/m-ab12cd34.txt", artifacts)
        self.assertIn("corpus/given/m-ab12cd34.txt.meta.md", artifacts)

    def test_second_import_is_a_no_op_by_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            _rootA, docsA = _portable_tree(tmp, "A")
            selected, artifacts, _a, _e = kc.kb_export_closure(docsA, ["t"])
            bundle = Path(tmp) / "bundle"
            kc.kb_bundle_write(docsA, bundle, selected, artifacts, "A")
            writes, _s, _d, _e = kc.kb_import_plan(bundle, docsA)
        self.assertEqual(writes, [], "re-importing into its own source must write nothing")

    def test_import_never_overwrites_an_existing_topic(self):
        with tempfile.TemporaryDirectory() as tmp:
            _rootA, docsA = _portable_tree(tmp, "A")
            selected, artifacts, _a, _e = kc.kb_export_closure(docsA, ["t"])
            bundle = Path(tmp) / "bundle"
            kc.kb_bundle_write(docsA, bundle, selected, artifacts, "A")
            _rootB, docsB = _portable_tree(tmp, "B")
            (docsB / "topics" / "t.md").write_text(
                claims_md([]) + "\nLOCAL BODY\n", encoding="utf-8")
            writes, skipped, _d, errors = kc.kb_import_plan(bundle, docsB)
        self.assertEqual(errors, [], errors)
        self.assertIn("topics/t.md", skipped)
        self.assertNotIn("topics/t.md", [r for r, _p, _d in writes])

    def test_refuses_a_directory_that_is_not_a_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            _root, docs = _portable_tree(tmp)
            _w, _s, _d, errors = kc.kb_import_plan(Path(tmp), docs)
        self.assertTrue(any("not a kb bundle" in e for e in errors), errors)

    def test_refuses_a_same_named_artifact_with_different_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            _rootA, docsA = _portable_tree(tmp, "A")
            selected, artifacts, _a, _e = kc.kb_export_closure(docsA, ["t"])
            bundle = Path(tmp) / "bundle"
            kc.kb_bundle_write(docsA, bundle, selected, artifacts, "A")
            _rootB, docsB = _portable_tree(tmp, "B")
            (docsB / "corpus" / "given" / "m-ab12cd34.txt").write_bytes(b"other")
            _w, _s, _d, errors = kc.kb_import_plan(bundle, docsB)
        self.assertTrue(any("different bytes" in e for e in errors), errors)

    def test_a_path_escaping_the_docs_root_is_refused(self):
        """Belt and braces: rglob cannot currently produce a `..` entry, but the
        write path is confined anyway, so a future bundle form (archive,
        manifest-driven paths) cannot open the hole."""
        with tempfile.TemporaryDirectory() as tmp:
            _root, docs = _portable_tree(tmp)
            self.assertIsNone(kc.sdlc_core.confine_under(docs, "../../out.md"))
            self.assertIsNone(kc.sdlc_core.confine_under(docs, "topics/../../out.md"))

    def test_export_pulls_in_the_other_half_of_a_conflict_set(self):
        """A partial export ships a tree the symmetry check refuses."""
        with tempfile.TemporaryDirectory() as tmp:
            _root, docs = _portable_tree(tmp)
            src = "corpus/given/m-ab12cd34.txt"
            i1 = kc.kb_claim_id(src, "p=1@42-61", "")
            i2 = kc.kb_claim_id(src, "p=2@9-51", "")
            (docs / "topics" / "t.md").write_text(claims_md([
                (i1, "a", "-", "-", "-", src + "#p=1@42-61", "GIVEN",
                 "CONTESTED " + i2)]), encoding="utf-8")
            (docs / "topics" / "u.md").write_text(claims_md([
                (i2, "b", "-", "-", "-", src + "#p=2@9-51", "GIVEN",
                 "CONTESTED " + i1)]).replace("topic: t", "topic: u"),
                encoding="utf-8")
            selected, _art, added, errors = kc.kb_export_closure(docs, ["t"])
        self.assertEqual(errors, [], errors)
        self.assertIn("u", selected, "the conflict partner must travel too")
        self.assertEqual(added, ["u"], "and the growth must be reported, not silent")


class TL_F030_DocumentedInvocation(unittest.TestCase):
    """The commands `portability.md` §0 tells the agent to run, driven through
    `main()` exactly as written there. An executable spec beats a string match:
    it fails when the doctrine and the CLI drift apart, which is the defect class
    this skill keeps re-finding in its own field reports."""

    def _run(self, argv):
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = kc.main(argv)
        return rc, buf.getvalue()

    def test_the_documented_export_import_sequence_works(self):
        with tempfile.TemporaryDirectory() as tmp:
            rootA, _docsA = _portable_tree(tmp, "A")
            rootB = Path(tmp) / "B"
            (rootB / "ai_docs" / "topics").mkdir(parents=True)
            out = Path(tmp) / "kb-bundle"

            rc, o = self._run(["export", "--root", str(rootA), "--out", str(out)])
            self.assertEqual(rc, 0, o)
            self.assertTrue((out / "MANIFEST.md").is_file(), o)

            rc, o = self._run(["import", str(out), "--root", str(rootB), "--dry-run"])
            self.assertEqual(rc, 0, o)
            self.assertIn("dry run", o)
            self.assertFalse((rootB / "ai_docs" / "topics" / "t.md").is_file(),
                             "--dry-run must write nothing")

            rc, o = self._run(["import", str(out), "--root", str(rootB)])
            self.assertEqual(rc, 0, o)
            self.assertTrue((rootB / "ai_docs" / "topics" / "t.md").is_file(), o)

            rc, o = self._run(["check", "--root", str(rootB)])
            self.assertEqual(rc, 0, "check must be CLEAN right after an import:\n" + o)

    def test_export_of_named_topics_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            rootA, _docsA = _portable_tree(tmp, "A")
            out = Path(tmp) / "kb-bundle"
            rc, o = self._run(["export", "--root", str(rootA), "--out", str(out),
                               "--topics", "t"])
            self.assertEqual(rc, 0, o)
            self.assertEqual([p.name for p in (out / "topics").glob("*.md")], ["t.md"])


class TL_F030_ImportedAuthority(unittest.TestCase):
    """Owner ruling 2026-08-03: knowledge crosses a project boundary, authority
    does not."""

    def test_imported_row_may_not_supersede_a_local_one(self):
        src = "corpus/notes/n.md"
        i_imp = kc.kb_claim_id(src, "L1-1", "")
        i_loc = kc.kb_claim_id(src, "L2-2", "")
        rows = [(i_imp, "foreign ruling", "-", "-", "-", src + "#L1-1",
                 "IMPORTED", "OK"),
                (i_loc, "local fact", "-", "-", "-", src + "#L2-2",
                 "GIVEN", "SUPERSEDED " + i_imp)]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)},
                             notes={"n.md": "---\nimported_from: project-A\n"
                                            "basis: their owner said so\n---\nx\n"})
            errors, _w, _n = kc.kb_check_claims(docs)
        self.assertTrue(any("foreign decision cannot settle" in e for e in errors),
                        errors)

    def test_imported_without_its_origin_is_a_ruling_in_disguise(self):
        src = "corpus/notes/n.md"
        rows = [(kc.kb_claim_id(src, "L1-1", ""), "foreign ruling", "-", "-",
                 "-", src + "#L1-1", "IMPORTED", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)},
                             notes={"n.md": "---\nbasis: their owner said so\n---\nx\n"})
            errors, _w, _n = kc.kb_check_claims(docs)
        self.assertTrue(any("imported_from" in e for e in errors), errors)

    def test_a_reratified_row_settles_normally(self):
        """The escape is one honest act, not a workaround: own note, own basis,
        prov RULING."""
        src = "corpus/notes/n.md"
        i_rul = kc.kb_claim_id(src, "L1-1", "")
        i_loc = kc.kb_claim_id(src, "L2-2", "")
        rows = [(i_rul, "re-ratified here", "-", "-", "-", src + "#L1-1",
                 "RULING", "OK"),
                (i_loc, "local fact", "-", "-", "-", src + "#L2-2",
                 "GIVEN", "SUPERSEDED " + i_rul)]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)},
                             notes={"n.md": "---\nbasis: I decided, here is why\n---\nx\n"})
            errors, _w, _n = kc.kb_check_claims(docs)
        self.assertEqual([e for e in errors if "foreign decision" in e], [])


# F-031. Page 3 is furniture: it asserts nothing, and must therefore yield
# nothing. "Exhaustive" is read, never a row per page.
THREE_PAGES = ("Introduction\nThe feature is disabled by default.\n"
               "\fLimits\nThe cap is 20 operators.\n"
               "\f\n   \n")


def _cov_tree(tmp, through, spans=((1, 0, 12),), text=THREE_PAGES,
              name="m-ab12cd34.txt"):
    """A one-artifact corpus: the sidecar declares `through`, the topic cites
    `spans`. `through=None` writes no field at all."""
    docs = Path(tmp) / "ai_docs"
    (docs / "corpus" / "given").mkdir(parents=True)
    (docs / "topics").mkdir(parents=True)
    art = docs / "corpus" / "given" / name
    art.write_text(text, encoding="utf-8", newline="")
    meta = ("---\nsha256: %s\ndate: 2026-08-03\nprovenance: GIVEN\n"
            % kc.kb_sha256_bytes(art))
    if through is not None:
        meta += "extracted_through: %s\n" % through
    (docs / "corpus" / "given" / (name + ".meta.md")).write_text(
        meta + "---\nhanded over\n", encoding="utf-8")
    src = "corpus/given/" + name
    rows = []
    for pg, a, b in spans:
        loc = "p=%d@%d-%d" % (pg, a, b)
        rows.append((kc.kb_claim_id(src, loc, ""), "fact from page %d" % pg,
                     "-", "-", "-", src + "#" + loc, "GIVEN", "OK"))
    (docs / "topics" / "t.md").write_text(claims_md(rows), encoding="utf-8")
    return docs


class TL_F031_Coverage(unittest.TestCase):
    """F-031: a completion claim must be falsifiable. One test per branch —
    a single test tripping two branches lets either be deleted with the suite
    green (the F-027 lesson)."""

    def _check(self, through, **kw):
        with tempfile.TemporaryDirectory() as tmp:
            return kc.kb_corpus_check(_cov_tree(tmp, through, **kw))

    def test_claims_with_no_coverage_field_error(self):
        errors, _w = self._check(None)
        self.assertTrue(any("extracted_through" in e for e in errors), errors)

    def test_an_artifact_nobody_extracted_from_owes_nothing(self):
        errors, warnings = self._check(None, spans=())
        self.assertEqual((errors, warnings), ([], []))

    def test_short_of_the_end_warns_and_never_errors(self):
        errors, warnings = self._check("p=1")
        self.assertEqual(errors, [])
        self.assertTrue(any("incomplete" in w for w in warnings), warnings)

    def test_the_last_page_by_number_is_not_short(self):
        errors, warnings = self._check("p=3", spans=((1, 0, 12), (2, 0, 6)))
        self.assertEqual((errors, warnings), ([], []))

    def test_complete_ends_the_matter(self):
        errors, warnings = self._check("complete")
        self.assertEqual((errors, warnings), ([], []))

    def test_a_claim_past_the_declared_coverage_is_a_contradiction(self):
        errors, _w = self._check("p=1", spans=((1, 0, 12), (2, 0, 6)))
        self.assertTrue(any("contradict" in e for e in errors), errors)

    def test_coverage_past_the_stored_end_errors(self):
        errors, _w = self._check("p=9")
        self.assertTrue(any("past the end" in e for e in errors), errors)

    def test_an_unreadable_value_errors_rather_than_passing_silently(self):
        """Fail-closed: a field whose whole job is to be checkable must be
        checkable, or it is decoration that reads like a guarantee."""
        errors, _w = self._check("most of it")
        self.assertTrue(any("not a coverage statement" in e for e in errors), errors)

    def test_the_wrong_unit_compares_with_nothing_and_errors(self):
        errors, _w = self._check("L40")
        self.assertTrue(any("wrong unit" in e for e in errors), errors)

    def test_a_page_that_asserts_nothing_yields_no_rows_and_still_completes(self):
        """T3, the counterweight: 'exhaust the source' must never become
        'manufacture a row per page'. Page 3 is furniture and stays unrowed,
        and the artifact is still legitimately complete."""
        errors, warnings = self._check("complete", spans=((1, 0, 12), (2, 0, 6)))
        self.assertEqual((errors, warnings), ([], []))

    def test_a_note_sharing_a_name_is_not_attributed_to_the_artifact(self):
        """Extents are keyed by file name (as the supersession check already is),
        so a same-named note elsewhere in the corpus would otherwise inflate the
        artifact's reach and manufacture a contradiction that is not there."""
        with tempfile.TemporaryDirectory() as tmp:
            docs = _cov_tree(tmp, "p=1")
            note = docs / "corpus" / "notes" / "m-ab12cd34.txt"
            note.parent.mkdir(parents=True)
            note.write_text(THREE_PAGES, encoding="utf-8", newline="")
            src = "corpus/notes/m-ab12cd34.txt"
            rows = [(kc.kb_claim_id("corpus/given/m-ab12cd34.txt", "p=1@0-12", ""),
                     "fact from page 1", "-", "-", "-",
                     "corpus/given/m-ab12cd34.txt#p=1@0-12", "GIVEN", "OK"),
                    (kc.kb_claim_id(src, "p=2@0-6", ""), "said elsewhere",
                     "-", "-", "-", src + "#p=2@0-6", "ELICITED", "OK")]
            (docs / "topics" / "t.md").write_text(claims_md(rows), encoding="utf-8")
            errors, _w = kc.kb_corpus_check(docs)
        self.assertEqual([e for e in errors if "contradict" in e], [], errors)

    def test_the_index_names_every_artifact_including_the_finished_ones(self):
        """r9 guard: the coverage report is a fact on each row, never the
        filtered set of what is not current. Deleting the finished rows here
        would pass a naive 'shows incomplete work' test and break the Vision."""
        with tempfile.TemporaryDirectory() as tmp:
            docs = _cov_tree(tmp, "complete")
            given = docs / "corpus" / "given"
            for name, through in (("b-11112222.txt", "p=1"),
                                  ("c-33334444.txt", None)):
                art = given / name
                art.write_text(THREE_PAGES, encoding="utf-8", newline="")
                meta = ("---\nsha256: %s\ndate: 2026-08-03\nprovenance: GIVEN\n"
                        % kc.kb_sha256_bytes(art))
                if through:
                    meta += "extracted_through: %s\n" % through
                (given / (name + ".meta.md")).write_text(meta + "---\nx\n",
                                                         encoding="utf-8")
            index = kc.kb_build_corpus_index(docs)
        for name in ("m-ab12cd34.txt", "b-11112222.txt", "c-33334444.txt"):
            self.assertIn(name, index, index)
        self.assertIn("extracted through complete", index)
        self.assertIn("extracted through p=1 of 3", index)
        self.assertIn("extraction not recorded", index)


class TL_F031_WindowPlan(unittest.TestCase):
    """The register an ingestion resumes from is the PLAN_ ledger that already
    exists: one task per reading window, no second surface. What could break is
    the documented task shape, so it is driven through the real validator."""

    PLAN = """---
status: DRAFT
derived-from: ANALYSIS_manual.md
---
# Plan: Ingest the manual

```json
{
  "tasks": [
    {"id": "T1", "title": "Extract m-ab12cd34.txt, pages 1-30",
     "paths": ["ai_docs/topics/t.md",
               "ai_docs/corpus/given/m-ab12cd34.txt.meta.md"],
     "produces": ["ai_docs/corpus/given/m-ab12cd34.txt.meta.md#extracted_through=p=30"],
     "verify": "sdlc_check.py check"},
    {"id": "T2", "title": "Extract m-ab12cd34.txt, pages 31-60",
     "paths": ["ai_docs/topics/t.md",
               "ai_docs/corpus/given/m-ab12cd34.txt.meta.md"],
     "produces": ["ai_docs/corpus/given/m-ab12cd34.txt.meta.md#extracted_through=p=60"],
     "verify": "sdlc_check.py check"},
    {"id": "T3", "title": "Extract m-ab12cd34.txt, pages 61-72",
     "paths": ["ai_docs/topics/t.md",
               "ai_docs/corpus/given/m-ab12cd34.txt.meta.md"],
     "produces": ["ai_docs/corpus/given/m-ab12cd34.txt.meta.md#extracted_through=complete"],
     "verify": "sdlc_check.py check"}
  ]
}
```
"""

    def test_a_window_plan_validates_through_the_existing_command(self):
        import contextlib, io, json as _json
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sol = root / "ai_docs" / "solutions"
            sol.mkdir(parents=True)
            plan = sol / "PLAN_manual.md"
            plan.write_text(self.PLAN, encoding="utf-8")
            (sol / "PLAN_manual.ledger.json").write_text(
                _json.dumps({"T1": {"status": "done", "verify_result": "pass",
                                    "timestamp": "2026-08-03T00:00:00Z"}}),
                encoding="utf-8")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = kc.main(["plan", "--root", str(root), "validate", str(plan)])
            self.assertEqual(rc, 0, buf.getvalue())
            self.assertIn("3 task(s)", buf.getvalue())
            ledger, reason = kc.sdlc_core.load_ledger(
                sol / "PLAN_manual.ledger.json")
            self.assertEqual(reason, "")
            # The sentinel dispatch.md defines: only `status: done` is skipped,
            # so the window to resume at is T2. No new machinery computes this.
            pending = [t for t in ("T1", "T2", "T3")
                       if (ledger.get(t) or {}).get("status") != "done"]
            self.assertEqual(pending[0], "T2")


# ------------------------------------------------------------------ F-035
# The corpus letter promises every provenance is a real file. Two of the three
# mechanisms that should enforce it did not run, and one explained itself wrong.

SIDE_GIVEN = "---\nsha256: x\ndate: 2026-08-25\nprovenance: GIVEN\n---\n"


def given_and_sidecar(meta_body):
    """A given/ artifact plus the sidecar that declares it."""
    return {"c.txt": GIVEN_TXT["c.txt"], "c.txt.meta.md": meta_body}


class TL_F035_SidecarIsTheArtifactsFrontmatter(unittest.TestCase):
    """A -- the four non-GIVEN provenances must be REACHABLE on a given/
    artifact. Their declaration lives in the sidecar; the claim checker read the
    artifact itself, got {} rather than None, and errored unconditionally."""

    def _findings(self, prov, meta_body, src=None):
        rows = [("", "A", "-", "-", "-", src or SRC1, prov, "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)},
                             given=given_and_sidecar(meta_body))
            return kc.kb_check_claims(docs)

    def test_derived_with_derived_from_in_sidecar_passes(self):
        errors, _, _ = self._findings(
            "DERIVED", "---\nprovenance: DERIVED\n"
                       "derived_from: corpus/given/scan.png\n---\n")
        self.assertFalse([e for e in errors if "derived_from" in e], errors)

    def test_derived_without_derived_from_still_errors(self):
        # The gate must keep biting: a DERIVED claim on an artifact that
        # declares no derivation IS model knowledge disguised as a source.
        errors, _, _ = self._findings("DERIVED", SIDE_GIVEN)
        self.assertTrue([e for e in errors if "derived_from" in e], errors)

    def test_ruling_with_basis_in_sidecar_passes(self):
        errors, _, _ = self._findings(
            "RULING", "---\nprovenance: RULING\nbasis: measured on site\n---\n")
        self.assertFalse([e for e in errors if "basis" in e], errors)

    def test_imported_with_imported_from_in_sidecar_passes(self):
        errors, _, _ = self._findings(
            "IMPORTED", "---\nprovenance: IMPORTED\n"
                        "imported_from: other-project\n---\n")
        self.assertFalse([e for e in errors if "imported_from" in e], errors)

    def test_artifact_with_no_sidecar_at_all_still_errors(self):
        rows = [("", "A", "-", "-", "-", SRC1, "DERIVED", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT)
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertTrue([e for e in errors if "derived_from" in e], errors)

    def test_the_error_names_the_file_it_actually_read(self):
        # Bug C's lesson applied here: a finding that does not say WHERE it
        # looked sends the reader hunting in the wrong file.
        errors, _, _ = self._findings("DERIVED", SIDE_GIVEN)
        self.assertTrue([e for e in errors if ".meta.md" in e], errors)

    def test_a_markdown_artifact_in_given_resolves_its_sidecar(self):
        # The rule is sidecar-first, not "non-.md": a verbatim markdown source
        # stored in given/ declares itself in x.md.meta.md exactly like a .txt
        # extraction does, and reading its own frontmatter would read the
        # SOURCE's, which says nothing about how it was extracted.
        rows = [("", "A", "-", "-", "-", "corpus/given/d.md#L1-1",
                 "DERIVED", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)},
                             given={"d.md": "a line\n",
                                    "d.md.meta.md":
                                        "---\nprovenance: DERIVED\n"
                                        "derived_from: scan.png\n---\n"})
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertFalse([e for e in errors if "derived_from" in e], errors)

    def test_a_note_source_is_unaffected(self):
        # The .md path must keep resolving to its own frontmatter, not to a
        # sidecar that does not exist.
        rows = [("", "A", "-", "-", "-", "corpus/notes/n.md#L1-2",
                 "DERIVED", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)},
                             notes={"n.md": "---\nderived_from: x\n---\nbody\n"})
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertFalse([e for e in errors if "derived_from" in e], errors)


class TL_F035_WeakChainIsVisible(unittest.TestCase):
    """A' -- a GIVEN row resting on an artifact whose own sidecar declares a
    weaker provenance is the laundering the overlay exists to prevent. It was
    declarable only in prose, and prose is not a check."""

    def _warnings(self, sidecar_prov):
        rows = [("", "A", "-", "-", "-", SRC1, "GIVEN", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)},
                             given=given_and_sidecar(
                                 "---\nprovenance: %s\n"
                                 "derived_from: scan.png\n---\n" % sidecar_prov))
            _, warnings, _ = kc.kb_check_claims(docs)
        return warnings

    def test_given_row_on_derived_artifact_warns(self):
        self.assertTrue([w for w in self._warnings("DERIVED")
                         if "DERIVED" in w], self._warnings("DERIVED"))

    def test_given_row_on_given_artifact_is_silent(self):
        rows = [("", "A", "-", "-", "-", SRC1, "GIVEN", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)},
                             given=given_and_sidecar(SIDE_GIVEN))
            _, warnings, _ = kc.kb_check_claims(docs)
        self.assertFalse([w for w in warnings if "provenance" in w], warnings)

    def test_artifact_with_no_sidecar_is_silent(self):
        # Nothing declared, nothing to contradict: silence, not a warning.
        rows = [("", "A", "-", "-", "-", SRC1, "GIVEN", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT)
            _, warnings, _ = kc.kb_check_claims(docs)
        self.assertFalse([w for w in warnings if "provenance" in w], warnings)


class TL_F035_OriginalPathResolves(unittest.TestCase):
    """B -- `original_sha256` is not checked because we do not hold the bytes.
    That reason does not extend to the path, which costs one exists()."""

    def _run(self, meta_extra, make_original=None):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {}, given={
                "c.txt": GIVEN_TXT["c.txt"],
                "c.txt.meta.md": "---\nsha256: \ndate: 2026-08-25\n"
                                 "provenance: GIVEN\n%s---\n" % meta_extra})
            if make_original:
                p = Path(tmp) / make_original
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("original", encoding="utf-8")
            return kc.kb_corpus_check(docs)

    def test_dangling_original_path_warns(self):
        errors, warnings = self._run("original_path: vault/gone.pdf\n")
        self.assertTrue([w for w in warnings if "original_path" in w], warnings)

    def test_dangling_original_path_is_never_an_error(self):
        # T3: export never carries originals out of the docs root and import
        # copies sidecars verbatim, so an imported bundle legitimately dangles.
        errors, _ = self._run("original_path: vault/gone.pdf\n")
        self.assertFalse([e for e in errors if "original_path" in e], errors)

    def test_relative_path_resolves_against_the_project_root(self):
        errors, warnings = self._run("original_path: vault/here.pdf\n",
                                     make_original="vault/here.pdf")
        self.assertFalse([w for w in warnings if "original_path" in w], warnings)

    def test_absent_original_path_is_silent(self):
        errors, warnings = self._run("")
        self.assertFalse([w for w in warnings if "original_path" in w], warnings)


class TL_F035_DuplicateIdNamesItsCause(unittest.TestCase):
    """C -- one message served two causes. A copied row and a hash collision
    are different defects with different fixes, and the reader was sent after
    the wrong one."""

    def test_two_distinct_rows_on_one_span_report_the_collision(self):
        i1 = kc.kb_claim_id("corpus/given/c.txt", "p=1@0-8", "")
        rows = [(i1, "delivery slips to Q3", "-", "-", "-", SRC1, "GIVEN", "OK"),
                (i1, "the module ships enabled", "-", "-", "-", SRC1,
                 "GIVEN", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT)
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertTrue([e for e in errors if "cannot separate" in e], errors)

    def test_a_genuinely_copied_row_still_reports_uniqueness(self):
        i1 = kc.kb_claim_id("corpus/given/c.txt", "p=1@0-8", "")
        row = (i1, "delivery slips to Q3", "-", "-", "-", SRC1, "GIVEN", "OK")
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md([row]),
                                   "u.md": claims_md([row])}, given=GIVEN_TXT)
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertTrue([e for e in errors if "uniqueness" in e], errors)
        self.assertFalse([e for e in errors if "cannot separate" in e], errors)

    def test_the_id_function_itself_does_not_move(self):
        # C changes a string, never a hash. portability.md's de-duplication
        # rests on this value being IDENTICAL in two projects, so the constants
        # are pinned: a change here breaks every already-exported bundle.
        self.assertEqual(kc.kb_claim_id("corpus/given/c.txt", "p=1@0-8", ""),
                         "fa53fcf18ccb")
        self.assertEqual(kc.kb_claim_id("corpus/given/c.txt", "p=1@0-8",
                                        "cost:12000:EUR"), "5ddfab538bf6")


class TL_F035_R2_PathClassification(unittest.TestCase):
    """Round 2 -- the independent review found `Path.is_absolute()` was the
    wrong test: on Windows `/vault/manuals/xyz.pdf` (the form this project's
    OWN templates print) is not absolute, so it was joined under the docs root
    and rewritten onto its drive."""

    def test_rooted_driveless_path_is_taken_as_written(self):
        cands = [str(c) for c in
                 kc._kb_original_candidates("/vault/manuals/xyz.pdf",
                                            Path("D:/proj/ai_docs"))]
        self.assertEqual(len(cands), 1, cands)
        for c in cands:
            self.assertNotIn("proj", c, cands)      # never joined under the root
            self.assertNotIn("ai_docs", c, cands)

    def test_relative_path_offers_project_root_then_docs_root(self):
        cands = [str(c) for c in
                 kc._kb_original_candidates("vault/x.pdf",
                                            Path("D:/proj/ai_docs"))]
        self.assertEqual(len(cands), 2, cands)
        self.assertEqual(len(set(cands)), 2, cands)  # never the same path twice

    def test_a_posix_filename_containing_a_backslash_keeps_its_raw_form(self):
        # The raw string is tried FIRST; the slash-normalised form is only an
        # additional candidate, because a backslash is legal in a POSIX name.
        cands = [str(c) for c in
                 kc._kb_original_candidates(chr(92).join(["/vault/my", "file.pdf"]),
                                            Path("/proj/ai_docs"))]
        self.assertTrue(any(chr(92) in c for c in cands), cands)


class TL_F035_R2_PointerProbe(unittest.TestCase):
    def _warnings(self, op, make=None, as_dir=False):
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {}, given={
                "c.txt": GIVEN_TXT["c.txt"],
                "c.txt.meta.md": "---\ndate: 2026-08-25\nprovenance: GIVEN\n"
                                 "original_path: %s\n---\n" % op})
            if make:
                p = Path(tmp) / make
                p.parent.mkdir(parents=True, exist_ok=True)
                if as_dir:
                    p.mkdir(exist_ok=True)
                else:
                    p.write_text("x", encoding="utf-8")
            return kc.kb_corpus_check(docs)[1]

    def test_absolute_path_that_resolves_is_silent(self):
        with tempfile.TemporaryDirectory() as tmp:
            orig = Path(tmp) / "vault" / "x.pdf"
            orig.parent.mkdir(parents=True)
            orig.write_text("x", encoding="utf-8")
            docs = make_tree(tmp, {}, given={
                "c.txt": GIVEN_TXT["c.txt"],
                "c.txt.meta.md": "---\ndate: 2026-08-25\n"
                                 "original_path: %s\n---\n" % str(orig)})
            warnings = kc.kb_corpus_check(docs)[1]
        self.assertFalse([w for w in warnings if "original_path" in w], warnings)

    def test_relative_path_under_the_docs_root_also_resolves(self):
        # The second candidate: --root and migrate both allow a docs root that
        # does not sit directly under the project root.
        w = self._warnings("held/x.pdf", make="ai_docs/held/x.pdf")
        self.assertFalse([x for x in w if "original_path" in x], w)

    def test_a_directory_is_not_a_resolved_pointer(self):
        # original_path names a document; a directory sitting there is not it.
        w = self._warnings("vault/x.pdf", make="vault/x.pdf", as_dir=True)
        self.assertTrue([x for x in w if "original_path" in x], w)

    def test_the_warning_never_lists_the_same_path_twice(self):
        w = [x for x in self._warnings("/vault/gone.pdf") if "original_path" in x]
        self.assertTrue(w, w)
        tried = w[0].split("tried ", 1)[1].rstrip(")").split(", ")
        self.assertEqual(len(tried), len(set(tried)), w[0])


class TL_F035_R2_WeakChainEdges(unittest.TestCase):
    def _warnings(self, prov_cell, sidecar_body, given=None):
        rows = [("", "A", "-", "-", "-", SRC1, prov_cell, "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)},
                             given=given if given is not None else {
                                 "c.txt": GIVEN_TXT["c.txt"],
                                 "c.txt.meta.md": sidecar_body})
            return kc.kb_check_claims(docs)[1]

    def test_lowercase_given_in_the_sidecar_is_silent(self):
        w = self._warnings("GIVEN", "---\nprovenance: given\n---\n")
        self.assertFalse([x for x in w if "provenance" in x], w)

    def test_empty_provenance_value_is_silent(self):
        w = self._warnings("GIVEN", "---\nprovenance: \ndate: 2026-08-25\n---\n")
        self.assertFalse([x for x in w if "provenance" in x], w)

    def test_a_non_given_row_gets_no_weak_chain_warning(self):
        # The warning is about a row CLAIMING first-hand evidence. A row that
        # already declares DERIVED is not laundering anything.
        w = self._warnings("DERIVED", "---\nprovenance: DERIVED\n"
                                      "derived_from: scan.png\n---\n")
        self.assertFalse([x for x in w if "prov GIVEN" in x], w)

    def test_an_orphan_sidecar_says_nothing_about_a_missing_artifact(self):
        # The artifact is gone and the source loop already errors on it; an
        # answer read from the surviving sidecar would be a second finding
        # about a file that is not there.
        rows = [("", "A", "-", "-", "-", "corpus/given/gone.txt#L1-2",
                 "GIVEN", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given={
                "gone.txt.meta.md": "---\nprovenance: DERIVED\n"
                                    "derived_from: scan.png\n---\n"})
            errors, warnings, _ = kc.kb_check_claims(docs)
        self.assertFalse([w for w in warnings if "provenance" in w], warnings)
        self.assertTrue([e for e in errors if "does not resolve" in e], errors)


class TL_F035_R2_NoReadOutsideTheRoot(unittest.TestCase):
    def test_an_empty_source_path_never_reads_beside_the_docs_root(self):
        # `#L1-2` with no file before the locator made confine_under return the
        # docs root itself, and the sidecar name was then formed from
        # base.parent -- i.e. <docs-root>.meta.md, outside the tree.
        rows = [("", "A", "-", "-", "-", "#L1-2", "DERIVED", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT)
            trap = Path(tmp) / "ai_docs.meta.md"
            trap.write_text("---\nderived_from: planted\n"
                            "provenance: DERIVED\n---\n", encoding="utf-8")
            errors, warnings, _ = kc.kb_check_claims(docs)
        # The planted file must not be read, satisfy any gate, or be echoed.
        self.assertFalse([w for w in warnings if "planted" in w or "DERIVED" in w],
                         warnings)
        self.assertFalse([e for e in errors if "planted" in e], errors)
        # The unresolvable source is the finding this row deserves, and the one
        # it gets -- a second complaint about a missing 'derived_from:' would
        # be noise about a file that was never there.
        self.assertTrue([e for e in errors if "does not resolve" in e], errors)


class TL_F035_R2_StaleIdIsNotACollision(unittest.TestCase):
    def test_same_id_different_text_different_span_names_the_stale_id(self):
        # Two rows sharing a hand-typed id while citing DIFFERENT spans. The
        # collision wording would assert "they cite the same span", which is
        # provably false here.
        i1 = kc.kb_claim_id("corpus/given/c.txt", "p=1@0-8", "")
        rows = [(i1, "delivery slips to Q3", "-", "-", "-", SRC1, "GIVEN", "OK"),
                (i1, "the module ships enabled", "-", "-", "-", SRC2,
                 "GIVEN", "OK")]
        with tempfile.TemporaryDirectory() as tmp:
            docs = make_tree(tmp, {"t.md": claims_md(rows)}, given=GIVEN_TXT)
            errors, _, _ = kc.kb_check_claims(docs)
        self.assertTrue([e for e in errors if "was not computed from this row" in e],
                        errors)
        self.assertFalse([e for e in errors if "cannot separate" in e], errors)


if __name__ == "__main__":
    unittest.main(verbosity=1)
