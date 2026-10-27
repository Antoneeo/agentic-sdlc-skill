#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-084 battery — the corpus's reach and the documents the project sent out.

kb-ONLY module, deliberately outside the shared manifest. Guards
ANALYSIS_kb_corpus_reach.md's acceptance criteria:

  AC1/AC2 `inventory <path>`: classification by content, skipped and excluded
          directories, links, tombstones, argument errors, no totals.
  AC3     the exclusion registry's rows, in validate and check.
  AC4     orient's upper bound, its cap and its fail-open.
  AC5     the changed-original finding in `stale`.
  AC6     DECLARED provenance rules.
  AC7     the one-way DIVERGES state.
  AC8     declarations stay out of bundles; import refuses them.

    python scripts/test_kb_corpus_reach.py
"""
import contextlib
import hashlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_check as kc  # noqa: E402
import knowledge  # noqa: E402

TXT = "page one text here"
LOC = "p=1@0-8"


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode("utf-8")).hexdigest()


def run_cli(argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        try:
            rc = kc.main(list(argv))
        except SystemExit as e:
            rc = e.code if isinstance(e.code, int) else 1
    return rc, out.getvalue()


def write(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    # bytes verbatim: a sidecar digest is of raw bytes, and write_text would
    # translate newlines on Windows
    p.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
    return p


def sidecar(prov="GIVEN", digest=None, extra=""):
    return ("---\nsha256: %s\ndate: 2026-10-16\nprovenance: %s\n%s"
            "extracted_through: complete\n---\n" % (digest or sha(TXT), prov, extra))


def claims_md(rows, topic="t"):
    head = ("---\ntopic: %s\ndescription: d\nparents: []\nstatus: CURRENT\n"
            "---\n\n## Claims\n\n"
            "| id | claim | valid | qty | about | source | prov | state |\n"
            "|---|---|---|---|---|---|---|---|\n" % topic)
    return head + "\n".join("| %s |" % " | ".join(r) for r in rows) + "\n"


def row(src, prov="GIVEN", state="OK", claim="page one", extra_sources=()):
    srcs = "; ".join([src + "#" + LOC] + [s + "#" + LOC for s in extra_sources])
    return (kc.kb_claim_id(src, LOC, ""), claim, "-", "-", "-", srcs, prov, state)


def rid(src):
    return kc.kb_claim_id(src, LOC, "")


class Project:
    """A project root `tmp` with docs root `tmp/ai_docs`."""

    def __init__(self, tmp):
        self.root = Path(tmp)
        self.docs = self.root / "ai_docs"
        (self.docs / "topics").mkdir(parents=True)

    def given(self, name, data=TXT, meta=None):
        write(self.docs / "corpus" / "given" / name, data)
        write(self.docs / "corpus" / "given" / (name + ".meta.md"), meta or sidecar())
        return "corpus/given/" + name

    def topic(self, rows, slug="t"):
        write(self.docs / "topics" / (slug + ".md"), claims_md(rows, slug))

    def file(self, rel, data):
        return write(self.root / rel, data)

    def registry(self, rows):
        write(self.docs / "audit" / "INVENTORY_exclusions.md",
              "# Inventory exclusions\n\n| pattern | reason | approved |\n|---|---|---|\n"
              + "".join("| %s | %s | %s |\n" % r for r in rows))


def states(out):
    """{relpath: (STATE, basis)} from inventory output lines."""
    got = {}
    for ln in out.splitlines():
        parts = ln.split(None, 2)
        if len(parts) >= 2 and parts[0] in ("INGESTED", "INGESTED_EARLIER", "EXCLUDED",
                                            "NOT_EXAMINED", "SKIPPED"):
            got[parts[1]] = (parts[0], parts[2] if len(parts) > 2 else "")
    return got


def try_symlink(link, target):
    try:
        os.symlink(target, link)
        return True
    except (OSError, NotImplementedError, AttributeError):
        return False


def try_junction(link, target):
    if os.name != "nt":
        return False
    r = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                       capture_output=True)
    return r.returncode == 0


# ------------------------------------------------------------------ AC1/AC2

class TC_Inventory(unittest.TestCase):

    def build(self, tmp):
        p = Project(tmp)
        alpha = "alpha text\n"
        a = p.given("a.txt", alpha, sidecar(digest=sha(alpha)))
        p.file("src/a.txt", alpha)                       # verbatim copy
        p.file("moved/a_copy.txt", alpha)                # same bytes elsewhere
        p.given("m.txt", TXT, sidecar(extra="original_path: orig/m.pdf\n"
                                       "original_sha256: %s\n" % sha(b"M1")))
        p.file("orig/m.pdf", b"M2")                      # changed since ingest
        p.given("r.txt", TXT, sidecar(extra="original_path: red/r.txt\n"
                                       "redacted_at_intake: [password]\n"))
        p.file("red/r.txt", "password=hunter2\n")        # redacted: no digest kept
        write(p.docs / "corpus" / "given" / "t-withdrawn-20261001.txt.meta.md",
              "---\ndate: 2026-10-01\nprovenance: GIVEN\nwithdrawn: secret\n"
              "original_path: tomb/t.txt\n---\n")
        p.file("tomb/t.txt", "tomb\n")                   # tombstone counts for nothing
        p.file("node_modules/x.js", "x")
        p.file(".hidden/y.txt", "y")
        p.file("gen/z.txt", "z")
        p.file("notes.bak", alpha)                       # excluded, bytes = artifact
        p.file("plain.txt", "plain\n")
        p.registry([("gen/", "generated", "2026-10-27"),
                    ("*.bak", "copies", "2026-10-27 (REQUEST_x.md R2)")])
        p.topic([row(a)])
        return p

    def test_classification(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self.build(tmp)
            link_ok = try_symlink(p.root / "link.txt", p.root / "plain.txt")
            junc_ok = try_junction(p.root / "junc", p.root / "src")
            hashed = []
            real = knowledge.kb_sha256_bytes

            def spy(path):
                hashed.append(Path(path).resolve())
                return real(path)
            knowledge.kb_sha256_bytes = spy
            try:
                rc, out = run_cli(["inventory", ".", "--root", tmp])
            finally:
                knowledge.kb_sha256_bytes = real
            self.assertEqual(rc, 0, out)
            got = states(out)
            self.assertEqual(got["src/a.txt"][0], "INGESTED")
            self.assertIn("a.txt.meta.md", got["src/a.txt"][1])
            self.assertEqual(got["moved/a_copy.txt"][0], "INGESTED")
            self.assertEqual(got["orig/m.pdf"][0], "INGESTED_EARLIER")
            self.assertIn("original changed since ingest", got["orig/m.pdf"][1])
            self.assertEqual(got["red/r.txt"][0], "INGESTED")
            self.assertIn("by path", got["red/r.txt"][1])
            self.assertEqual(got["tomb/t.txt"][0], "NOT_EXAMINED")
            self.assertEqual(got["plain.txt"][0], "NOT_EXAMINED")
            self.assertEqual(got["node_modules/"][0], "SKIPPED")
            self.assertEqual(got[".hidden/"][0], "SKIPPED")
            self.assertEqual(got["gen/"][0], "EXCLUDED")
            self.assertEqual(got["notes.bak"][0], "EXCLUDED")
            self.assertNotIn("node_modules/x.js", got)
            self.assertNotIn("gen/z.txt", got)
            self.assertFalse(any(k.startswith("ai_docs") for k in got))
            if link_ok:
                self.assertEqual(got["link.txt"], ("NOT_EXAMINED", "link — not followed"))
            if junc_ok:
                self.assertEqual(got["junc"], ("NOT_EXAMINED", "link — not followed"))
                self.assertNotIn("junc/a.txt", got)
            # excluded files are never read, whatever their bytes
            never = {(p.root / "notes.bak").resolve(), (p.root / "gen" / "z.txt").resolve()}
            self.assertFalse(never & set(hashed), hashed)
            # no per-state totals (r37)
            self.assertNotRegex(out, r"(?im)^\s*(INGESTED|NOT_EXAMINED|EXCLUDED)\s*:\s*\d")
            self.assertIn("Nothing was written.", out)
            # path order
            listed = [ln.split(None, 2)[1] for ln in out.splitlines()
                      if ln.split(None, 1)[:1] and ln.split(None, 1)[0] in
                      ("INGESTED", "INGESTED_EARLIER", "EXCLUDED", "NOT_EXAMINED", "SKIPPED")]
            self.assertEqual(listed, sorted(listed))

    def test_cloud_only_never_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self.build(tmp)
            real = knowledge.kb_unreadable

            def fake(entry):
                if entry.name == "plain.txt":
                    return "cloud-only"
                return real(entry)
            knowledge.kb_unreadable = fake
            try:
                rc, out = run_cli(["inventory", ".", "--root", tmp])
            finally:
                knowledge.kb_unreadable = real
            self.assertEqual(states(out)["plain.txt"],
                             ("NOT_EXAMINED", "cloud-only — not read"))

    def test_subpath_and_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.build(tmp)
            rc, out = run_cli(["inventory", "orig", "--root", tmp])
            self.assertEqual(rc, 0, out)
            self.assertEqual(list(states(out)), ["orig/m.pdf"])
            for bad in ("../x", "ai_docs", "node_modules", "gen"):
                rc, out = run_cli(["inventory", bad, "--root", tmp])
                self.assertEqual(rc, 2, (bad, out))
                self.assertIn("[ERROR]", out)
            rc, out = run_cli(["inventory", "--root", tmp])
            self.assertNotEqual(rc, 0)
            rc, out = run_cli(["inventory", ".", "--state", "NOT_EXAMINED", "--root", tmp])
            self.assertNotEqual(rc, 0)

    def test_no_docs_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc, out = run_cli(["inventory", ".", "--root", str(Path(tmp) / "nope")])
            self.assertNotEqual(rc, 0)


# ------------------------------------------------------------------ AC3

class TC_Registry(unittest.TestCase):

    def test_malformed_rows_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            p.topic([])
            p.registry([("ok/", "fine", "2026-10-27"),
                        ("", "empty pattern", "2026-10-27"),
                        ("x/", "", "2026-10-27"),
                        ("y/", "bad date", "yesterday"),
                        ("../z", "escape", "2026-10-27"),
                        ("/abs", "rooted", "2026-10-27")])
            for cmd in ("validate", "check"):
                rc, out = run_cli([cmd, "--root", tmp])
                errs = [ln for ln in out.splitlines()
                        if "[ERROR]" in ln and "INVENTORY_exclusions" in ln]
                self.assertEqual(len(errs), 5, (cmd, out))
                self.assertNotEqual(rc, 0)

    def test_well_formed_is_silent_and_not_catalogued(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            p.topic([])
            p.registry([("gen/", "generated", "2026-10-27")])
            rc, out = run_cli(["validate", "--root", tmp])
            self.assertNotIn("INVENTORY_exclusions", out)
            paths = [r[0] if isinstance(r, tuple) else r.get("path")
                     for r in knowledge.memory_records(p.docs)]
            self.assertFalse(any("INVENTORY_exclusions" in str(x) for x in paths))


# ------------------------------------------------------------------ AC4

class TC_Orient(unittest.TestCase):

    def test_bound_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            a = p.given("a.txt", "alpha text\n", sidecar(digest=sha("alpha text\n")))
            p.topic([row(a)])
            p.file("src/a.txt", "alpha text\n")       # ingested by digest
            p.file("src/b.txt", "beta text!\n")       # same size, other bytes: counted
            p.file("pdf/reg.pdf", b"%PDF")            # counted
            rc, out = run_cli(["orient", "--root", tmp])
            self.assertIn("Corpus reach: <= 2 project files not examined", out)
            self.assertIn("inventory <path>", out)

    def test_no_line_when_zero_or_no_corpus(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            a = p.given("a.txt", "alpha text\n", sidecar(digest=sha("alpha text\n")))
            p.topic([row(a)])
            p.file("src/a.txt", "alpha text\n")
            rc, out = run_cli(["orient", "--root", tmp])
            self.assertNotIn("Corpus reach", out)
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            p.topic([])
            p.file("pdf/reg.pdf", b"%PDF")
            rc, out = run_cli(["orient", "--root", tmp])
            self.assertNotIn("Corpus reach", out)

    def test_fail_open_and_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            a = p.given("a.txt")
            p.topic([row(a)])
            write(p.docs / "topics" / "INDEX.md", "| topic | description |\n|---|---|\n")
            p.file("pdf/reg.pdf", b"%PDF")
            real = knowledge.kb_corpus_reach

            def boom(*a, **k):
                raise RuntimeError("walk failed")
            knowledge.kb_corpus_reach = boom
            try:
                rc, out = run_cli(["orient", "--root", tmp])
            finally:
                knowledge.kb_corpus_reach = real
            self.assertNotIn("Corpus reach", out)
            self.assertIn("## Topic router", out)
            ticks = iter([0.0] + [5.0] * 1000)
            real_clock = knowledge._kb_clock
            knowledge._kb_clock = lambda: next(ticks)
            try:
                rc, out = run_cli(["orient", "--root", tmp])
            finally:
                knowledge._kb_clock = real_clock
            self.assertIn("Corpus reach: not counted within 1s", out)


# ------------------------------------------------------------------ AC5

class TC_ChangedOriginal(unittest.TestCase):

    def build(self, tmp, successor=False):
        p = Project(tmp)
        p.file("plans/plan.pdf", b"v1")
        a = p.given("plan.txt", TXT, sidecar(extra="original_path: plans/plan.pdf\n"
                                          "original_sha256: %s\n" % sha(b"v1")))
        p.topic([row(a)])
        p.file("plans/plan.pdf", b"v2")
        if successor:
            p.given("plan2.txt", TXT + " v2", sidecar(
                digest=sha(TXT + " v2"),
                extra="supersedes: plan.txt\noriginal_path: plans/plan.pdf\n"
                      "original_sha256: %s\n" % sha(b"v2")))
        return p

    def test_stale_names_it_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.build(tmp)
            rc_check, out_check = run_cli(["check", "--root", tmp])
            rc, out = run_cli(["stale", "--root", tmp])
            hits = [ln for ln in out.splitlines() if "changed since ingest" in ln]
            self.assertEqual(len(hits), 1, out)
            self.assertIn("corpus/given/plan.txt", hits[0])
            self.assertIn("plans/plan.pdf", hits[0])
            self.assertIn("1 claim(s) cite it", hits[0])
            self.assertNotIn("changed since ingest", out_check)

    def test_successor_clears_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.build(tmp, successor=True)
            rc, out = run_cli(["stale", "--root", tmp])
            self.assertNotIn("changed since ingest", out)

    def test_unchanged_is_silent(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            p.file("plans/plan.pdf", b"v1")
            a = p.given("plan.txt", TXT, sidecar(extra="original_path: plans/plan.pdf\n"
                                              "original_sha256: %s\n" % sha(b"v1")))
            p.topic([row(a)])
            rc, out = run_cli(["stale", "--root", tmp])
            self.assertNotIn("changed since ingest", out)


# ------------------------------------------------------------------ AC6/AC7

DECL = sidecar("DECLARED", extra="recipient: client\n")


def graph_errors(tmp):
    rc, out = run_cli(["graph", "--root", tmp])
    return rc, [ln for ln in out.splitlines() if ln.startswith("[ERROR]")], out


class TC_Declared(unittest.TestCase):

    def test_well_formed_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            d = p.given("dpia.txt", TXT, DECL)
            p.topic([row(d, "DECLARED")])
            rc, errs, out = graph_errors(tmp)
            self.assertEqual(rc, 0, out)

    def test_refusals(self):
        cases = {
            "no recipient": lambda p: [row(p.given("d.txt", TXT, sidecar("DECLARED")),
                                           "DECLARED")],
            "sidecar not DECLARED": lambda p: [row(p.given("d.txt"), "DECLARED")],
            "GIVEN on DECLARED": lambda p: [row(p.given("d.txt", TXT, DECL))],
            "DECLARED second source of GIVEN": lambda p: [
                row(p.given("g.txt"), extra_sources=[p.given("d.txt", TXT, DECL)])],
            "GIVEN second source of DECLARED": lambda p: [
                row(p.given("d.txt", TXT, DECL), "DECLARED",
                    extra_sources=[p.given("g.txt")])],
        }
        for name, build in cases.items():
            with self.subTest(name), tempfile.TemporaryDirectory() as tmp:
                p = Project(tmp)
                p.topic(build(p))
                rc, errs, out = graph_errors(tmp)
                self.assertNotEqual(rc, 0, out)
                self.assertTrue(any("DECLARED" in e for e in errs), out)

    def test_elicited_on_declared_note_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            write(p.docs / "corpus" / "notes" / "n.md",
                  "---\norigin: elicited\ndate: 2026-10-16\nprovenance: DECLARED\n---\n"
                  "page one text here\n")
            src = "corpus/notes/n.md"
            r = (kc.kb_claim_id(src, "L6-6", ""), "x", "-", "-", "-", src + "#L6-6",
                 "ELICITED", "OK")
            p.topic([r])
            rc, errs, out = graph_errors(tmp)
            self.assertNotEqual(rc, 0, out)

    def test_supersession_and_contest_mixes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            g, d = p.given("g.txt"), p.given("d.txt", TXT, DECL)
            p.topic([row(g, state="SUPERSEDED " + rid(d)),
                     row(d, "DECLARED")])
            rc, errs, out = graph_errors(tmp)
            self.assertNotEqual(rc, 0, out)
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            g, d = p.given("g.txt"), p.given("d.txt", TXT, DECL)
            p.topic([row(g, state="CONTESTED " + rid(d)),
                     row(d, "DECLARED", state="CONTESTED " + rid(g))])
            rc, errs, out = graph_errors(tmp)
            self.assertNotEqual(rc, 0, out)

    def test_two_declarations_may_contest(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            d1, d2 = p.given("d1.txt", TXT, DECL), p.given("d2.txt", TXT, DECL)
            p.topic([row(d1, "DECLARED", state="CONTESTED " + rid(d2)),
                     row(d2, "DECLARED", state="CONTESTED " + rid(d1))])
            rc, errs, out = graph_errors(tmp)
            self.assertEqual(rc, 0, out)

    def test_resend_supersedes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            d1, d2 = p.given("d1.txt", TXT, DECL), p.given("d2.txt", TXT, DECL)
            p.topic([row(d1, "DECLARED", state="SUPERSEDED " + rid(d2)),
                     row(d2, "DECLARED")])
            rc, errs, out = graph_errors(tmp)
            self.assertEqual(rc, 0, out)


class TC_Diverges(unittest.TestCase):

    def test_legal_forms(self):
        for target_state in ("OK", "CONTESTED"):
            with self.subTest(target_state), tempfile.TemporaryDirectory() as tmp:
                p = Project(tmp)
                g, h = p.given("g.txt"), p.given("h.txt")
                d = p.given("d.txt", TXT, DECL)
                rows = [row(d, "DECLARED", state="DIVERGES " + rid(g))]
                if target_state == "OK":
                    rows.append(row(g))
                else:
                    rows += [row(g, state="CONTESTED " + rid(h)),
                             row(h, state="CONTESTED " + rid(g))]
                p.topic(rows)
                rc, errs, out = graph_errors(tmp)
                self.assertEqual(rc, 0, out)

    def test_refusals(self):
        with tempfile.TemporaryDirectory() as tmp:          # on a non-DECLARED row
            p = Project(tmp)
            g, h = p.given("g.txt"), p.given("h.txt")
            p.topic([row(g, state="DIVERGES " + rid(h)), row(h)])
            self.assertNotEqual(graph_errors(tmp)[0], 0)
        with tempfile.TemporaryDirectory() as tmp:          # dangling target
            p = Project(tmp)
            d = p.given("d.txt", TXT, DECL)
            p.topic([row(d, "DECLARED", state="DIVERGES 0123456789ab")])
            self.assertNotEqual(graph_errors(tmp)[0], 0)
        with tempfile.TemporaryDirectory() as tmp:          # target DECLARED
            p = Project(tmp)
            d1, d2 = p.given("d1.txt", TXT, DECL), p.given("d2.txt", TXT, DECL)
            p.topic([row(d1, "DECLARED", state="DIVERGES " + rid(d2)),
                     row(d2, "DECLARED")])
            self.assertNotEqual(graph_errors(tmp)[0], 0)

    def test_superseded_target_must_be_rejudged(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            g, g2 = p.given("g.txt"), p.given("g2.txt")
            d = p.given("d.txt", TXT, DECL)
            p.topic([row(g, state="SUPERSEDED " + rid(g2)), row(g2),
                     row(d, "DECLARED", state="DIVERGES " + rid(g))])
            rc, errs, out = graph_errors(tmp)
            self.assertNotEqual(rc, 0, out)
            self.assertTrue(any("DIVERGES" in e for e in errs), out)


# ------------------------------------------------------------------ AC8

class TC_Boundary(unittest.TestCase):

    def test_export_leaves_declarations_behind(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Project(Path(tmp) / "A")
            g = a.given("g.txt")
            d1, d2 = a.given("d1.txt", TXT, DECL), a.given("d2.txt", TXT, DECL)
            a.topic([row(g),
                     row(d1, "DECLARED", state="SUPERSEDED " + rid(d2)),
                     row(d2, "DECLARED", state="DIVERGES " + rid(g))])
            out_dir = Path(tmp) / "bundle"
            rc, out = run_cli(["export", "--out", str(out_dir), "--root", str(a.root)])
            self.assertEqual(rc, 0, out)
            self.assertIn("declarations stay in this project: not exported", out)
            bundle_text = "\n".join(p.read_text(encoding="utf-8", errors="replace")
                                    for p in out_dir.rglob("*") if p.is_file())
            self.assertNotIn("DECLARED", bundle_text)
            self.assertNotIn("d1.txt", bundle_text)
            b = Project(Path(tmp) / "B")
            b.topic([], slug="other")
            rc, out = run_cli(["import", str(out_dir), "--root", str(b.root)])
            self.assertEqual(rc, 0, out)
            rc, out = run_cli(["check", "--root", str(b.root)])
            self.assertNotIn("[ERROR]", out)

    def test_export_without_declarations_prints_no_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Project(Path(tmp) / "A")
            a.topic([row(a.given("g.txt"))])
            rc, out = run_cli(["export", "--out", str(Path(tmp) / "bundle"),
                               "--root", str(a.root)])
            self.assertEqual(rc, 0, out)
            self.assertNotIn("declarations stay", out)

    def test_import_refuses_a_hand_made_declaration(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Project(Path(tmp) / "A")
            g = a.given("g.txt")
            a.topic([row(g)])
            out_dir = Path(tmp) / "bundle"
            rc, out = run_cli(["export", "--out", str(out_dir), "--root", str(a.root)])
            self.assertEqual(rc, 0, out)
            t = out_dir / "topics" / "t.md"
            t.write_text(t.read_text(encoding="utf-8").replace("| GIVEN |", "| DECLARED |"),
                         encoding="utf-8")
            b = Project(Path(tmp) / "B")
            b.topic([], slug="other")
            rc, out = run_cli(["import", str(out_dir), "--root", str(b.root)])
            self.assertNotEqual(rc, 0, out)
            self.assertIn("DECLARED", out)


# ------------------------------------------------------------------ closure-review gaps

class TC_ReviewGaps(unittest.TestCase):

    def test_bad_character_class_is_a_finding_not_a_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            p.topic([])
            p.registry([("[z-a].txt", "typo", "2026-10-27"), ("[]].md", "typo", "2026-10-27")])
            for argv in (["validate", "--root", tmp], ["inventory", ".", "--root", tmp]):
                rc, out = run_cli(argv)
                self.assertNotIn("Traceback", out)
                self.assertNotIn("PatternError", out)
            rc, out = run_cli(["validate", "--root", tmp])
            errs = [ln for ln in out.splitlines() if "[ERROR]" in ln and "INVENTORY_exclusions" in ln]
            self.assertEqual(len(errs), 2, out)

    def test_all_empty_row_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            p.topic([])
            p.registry([("", "", "")])
            rc, out = run_cli(["validate", "--root", tmp])
            self.assertIn("INVENTORY_exclusions", out)
            self.assertNotEqual(rc, 0)

    def test_trailing_slash_is_directories_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            p.topic([])
            p.file("a/logs", "a file named logs\n")
            p.file("b/logs/x.txt", "x\n")
            p.registry([("logs/", "logs", "2026-10-27")])
            rc, out = run_cli(["inventory", ".", "--root", tmp])
            got = states(out)
            self.assertEqual(got["a/logs"][0], "NOT_EXAMINED")
            self.assertEqual(got["b/logs/"], ("EXCLUDED", "logs/"))

    def test_linked_directory_still_skipped_or_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            p.topic([])
            p.file("real/v.txt", "v\n")
            p.registry([("vendor/", "third party", "2026-10-27")])
            if not (try_junction(p.root / "node_modules", p.root / "real")
                    and try_junction(p.root / "vendor", p.root / "real")
                    and try_junction(p.root / "jin", p.root / "real")):
                self.skipTest("no junctions here")
            rc, out = run_cli(["inventory", ".", "--root", tmp])
            got = states(out)
            self.assertEqual(got["node_modules/"][0], "SKIPPED")
            self.assertEqual(got["vendor/"][0], "EXCLUDED")
            self.assertEqual(got["jin"], ("NOT_EXAMINED", "link — not followed"))
            rc, out = run_cli(["inventory", "jin", "--root", tmp])
            self.assertEqual(rc, 0, out)
            self.assertEqual(states(out), {"jin": ("NOT_EXAMINED", "link — not followed")})
            rc, out = run_cli(["inventory", "node_modules", "--root", tmp])
            self.assertEqual(rc, 2, out)
            rc, out = run_cli(["orient", "--root", tmp])  # no corpus: no line, no walk
            self.assertNotIn("Corpus reach", out)

    def test_exact_listing(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = TC_Inventory().build(tmp)
            rc, out = run_cli(["inventory", ".", "--root", tmp])
            expected = {"src/a.txt", "moved/a_copy.txt", "orig/m.pdf", "red/r.txt",
                        "tomb/t.txt", "plain.txt", "node_modules/", ".hidden/", "gen/",
                        "notes.bak"}
            got = set(states(out))
            got -= {"link.txt", "junc"}  # environment-dependent
            self.assertEqual(got, expected, out)
            ne = sum(1 for s, _b in states(out).values() if s == "NOT_EXAMINED")
            rc, orient = run_cli(["orient", "--root", tmp])
            self.assertIn("Corpus reach: <= %d " % ne, orient)

    def test_orient_line_through_the_code_entry_point(self):
        code = (Path(__file__).resolve().parents[5] / "skills" / "agentic-sdlc-skill"
                / "scripts" / "sdlc_check.py")
        if not code.is_file():
            self.skipTest("code lens not beside this distribution")
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            p.topic([row(p.given("a.txt"))])
            p.file("pdf/reg.pdf", b"%PDF")
            r = subprocess.run([sys.executable, "-I", str(code), "orient", "--root", tmp],
                               capture_output=True, text=True, encoding="utf-8")
            self.assertIn("Corpus reach: <= 1 ", r.stdout)

    def test_case_variant_path_lists_or_refuses_never_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            p.topic([])
            p.file("realvendor/v.txt", "v\n")
            p.file("node_modules/x.js", "x")
            if not (p.root / "REALVENDOR").exists():
                self.skipTest("case-sensitive filesystem")
            rc, out = run_cli(["inventory", "RealVendor", "--root", tmp])
            self.assertEqual(rc, 0, out)
            self.assertIn("realvendor/v.txt", states(out))
            rc, out = run_cli(["inventory", "REALVENDOR/V.TXT", "--root", tmp])
            self.assertEqual(list(states(out)), ["realvendor/v.txt"], out)
            rc, out = run_cli(["inventory", "Node_Modules", "--root", tmp])
            self.assertEqual(rc, 2, out)

    def test_link_on_the_path_is_refused_and_a_link_target_listed(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as out_dir:
            p = Project(tmp)
            p.topic([])
            p.file("real/v.txt", "v\n")
            if not (try_junction(p.root / "jin", p.root / "real")
                    and try_junction(p.root / "jout", Path(out_dir))):
                self.skipTest("no junctions here")
            rc, out = run_cli(["inventory", "jin/v.txt", "--root", tmp])
            self.assertEqual(rc, 2, out)
            self.assertIn("a link the inventory never follows", out)
            rc, out = run_cli(["inventory", "jout", "--root", tmp])
            self.assertEqual(rc, 0, out)
            self.assertEqual(states(out), {"jout": ("NOT_EXAMINED", "link — not followed")})

    def test_unreadable_entries_are_listed_not_tracebacks(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            p.topic([])
            p.file("locked/a.txt", "a\n")
            p.file("odd.txt", "o\n")
            real_unreadable, real_scandir = knowledge.kb_unreadable, knowledge.os.scandir

            def fake_unreadable(entry):
                return "unreadable" if entry.name == "odd.txt" else real_unreadable(entry)

            def fake_scandir(path):
                if Path(path).name == "locked":
                    raise PermissionError("denied")
                return real_scandir(path)
            knowledge.kb_unreadable = fake_unreadable
            knowledge.os.scandir = fake_scandir
            try:
                rc, out = run_cli(["inventory", ".", "--root", tmp])
            finally:
                knowledge.kb_unreadable = real_unreadable
                knowledge.os.scandir = real_scandir
            self.assertEqual(rc, 0, out)
            got = states(out)
            self.assertEqual(got["odd.txt"], ("NOT_EXAMINED", "unreadable — not read"))
            self.assertEqual(got["locked/"], ("NOT_EXAMINED", "unreadable — not read"))

    def test_tombstone_never_reports_a_changed_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            p.file("plans/plan.pdf", b"v2")
            write(p.docs / "corpus" / "given" / "plan-withdrawn-20261001.txt.meta.md",
                  "---\ndate: 2026-10-01\nprovenance: GIVEN\nwithdrawn: secret\n"
                  "original_path: plans/plan.pdf\noriginal_sha256: %s\n---\n" % sha(b"v1"))
            p.topic([])
            self.assertEqual(knowledge.kb_changed_originals(p.docs), [])

    def test_declared_superseded_at_a_fact_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            g, d = p.given("g.txt"), p.given("d.txt", TXT, DECL)
            p.topic([row(g), row(d, "DECLARED", state="SUPERSEDED " + rid(g))])
            rc, errs, out = graph_errors(tmp)
            self.assertNotEqual(rc, 0, out)
            self.assertTrue(any("across a declaration" in e for e in errs), out)

    def test_export_refuses_a_fact_pointing_at_a_declaration(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Project(Path(tmp) / "A")
            g, d = a.given("g.txt"), a.given("d.txt", TXT, DECL)
            a.topic([row(g, state="SUPERSEDED " + rid(d)), row(d, "DECLARED")])
            rc, out = run_cli(["export", "--out", str(Path(tmp) / "bundle"),
                               "--root", str(a.root)])
            self.assertNotEqual(rc, 0, out)
            self.assertIn("a DECLARED row", out)
            self.assertFalse((Path(tmp) / "bundle").exists())


# ------------------------------------------------------------------ docs site

class TC_Site(unittest.TestCase):

    def test_declared_and_diverges_render(self):
        import docs_site
        with tempfile.TemporaryDirectory() as tmp:
            p = Project(tmp)
            g = p.given("g.txt")
            d = p.given("d.txt", TXT, DECL)
            note = write(p.docs / "corpus" / "notes" / "syn.md",
                         "---\nderived_from: [%s]\ndate: 2026-10-17\n---\n"
                         "page one text here\n" % d)
            nsrc = "corpus/notes/syn.md"
            p.topic([row(g), row(d, "DECLARED", state="DIVERGES " + rid(g)),
                     (kc.kb_claim_id(nsrc, "L4-4", ""), "x", "-", "-", "-",
                      nsrc + "#L4-4", "DERIVED", "OK")])
            self.assertTrue(note.is_file())
            kb = docs_site.build_kb(p.docs)
            fd = kb["facts"][rid(d)]
            self.assertEqual(fd["state"], "diverges")
            self.assertEqual(fd["diverges_from"], [rid(g)])
            self.assertEqual(fd["origin"], "declared")
            fn = kb["facts"][kc.kb_claim_id(nsrc, "L4-4", "")]
            self.assertEqual(fn["ground_class"], "declared")
            kinds = {(e["kind"], e.get("source")) for e in docs_site.chronology(p.docs, {})}
            self.assertIn(("sent", "d.txt"), kinds)
            self.assertIn(("source", "g.txt"), kinds)


if __name__ == "__main__":
    unittest.main()
