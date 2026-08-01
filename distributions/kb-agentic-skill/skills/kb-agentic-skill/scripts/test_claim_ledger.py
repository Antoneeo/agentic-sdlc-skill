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


if __name__ == "__main__":
    unittest.main(verbosity=1)
