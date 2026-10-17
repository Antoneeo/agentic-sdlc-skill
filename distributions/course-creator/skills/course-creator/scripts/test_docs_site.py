#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-072 -- the docs site: what the agent reads, made visible to the user.

One test per acceptance criterion of `ANALYSIS_kb_site.md`, run on three projects
built here in code: a knowledge-lens project (topics, claims, corpus), a code
project and a marketing project. Shared battery: it runs in every distribution,
so it never names one.

    python scripts/test_docs_site.py
"""
import contextlib
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import docs_site  # noqa: E402
import knowledge  # noqa: E402
import sdlc_core  # noqa: E402

PAGE_DIR = HERE.parent / "docs_site"
NBH = "‑"  # non-breaking hyphen


# ------------------------------------------------------------------ fixtures

def write(root, rel, text):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
    return p


CLAIM_HEAD = ("## Claims\n\n| id | claim | valid | qty | about | source | prov | state |\n"
              "|---|---|---|---|---|---|---|---|\n")


def row(cid, text, source, prov, state="OK", valid="-", qty="-", about="-"):
    return "| %s | %s | %s | %s | %s | %s | %s | %s |\n" % (
        cid, text, valid, qty, about, source, prov, state)


def build_kb(root, outside):
    """A knowledge-lens project exercising every shape the spec names."""
    d = "ai_docs/"
    write(root, d + "README.md", "---\ndescription: Reading guide.\nstatus: CURRENT\n"
          "default_domain: knowledge\n---\n# Pump field KB\n\nWhat we know about the "
          "pumps in the field.\n\nSecond paragraph.\n")
    write(root, d + "INDEX.md", "# Canonical manifest\n\n- `vision/project_vision.md`\n")
    write(root, d + "reference/INDEX.md", "# Guide router\n\n- GUIDE_ingest.md\n")
    write(root, d + "reference/GUIDE_ingest.md", "---\ndescription: Read before "
          "ingesting a mail.\nstatus: CURRENT\nsource_kind: document\n---\n# Guide: ingest\n\nSteps.\n")
    write(root, d + "reference/GUIDE_parser.md", "---\ndescription: How the parser "
          "is built.\nstatus: CURRENT\nsource_kind: code\n---\n# Guide: parser\n\nMap.\n")
    write(root, d + "vision/project_vision.md", "# Project Vision\nStatus: APPROVED (v2)\n\n"
          "## North Star\n\nServe the field technicians.\n\n## Non-Goals\n\nNone.\n")
    write(root, d + "vision/principles.md", "---\nstatus: CURRENT\n---\n# Principles\n\nBe exact.\n")
    write(root, d + "architecture/ADR_2026-03-01_pick_store.md", "---\nstatus: CURRENT\n---\n"
          "# ADR: pick the store\n\nDecided.\n")
    write(root, d + "audit/HANDOFF_ingest.md", "---\nworkstream: K-001 mail ingestion\nlevel: L3\n"
          "branch: feat/ingest\nstatus: IN_PROGRESS\nsince: 2026-03-01\nnext: read the March "
          "mails, then the April ones; keep the order as received\nupdated: 2026-03-10\n---\n"
          "## Resume logistics\n\nStart from mail 12.\n")
    write(root, d + "audit/HANDOFF_blocked.md", "---\nworkstream: K-002 waiting for the supplier\n"
          "level: L2\nstatus: BLOCKED\nsince: 2026-03-02\nnext: wait\nupdated: 2026-03-04\n---\n")
    write(root, d + "audit/HANDOFF_undated.md", "---\nworkstream: K-003 undated\nlevel: Spike\n"
          "status: READY\nsince: 2026-03-02\nnext: look\n---\n")
    write(root, d + "audit/project_notes.md", "- 2026-03-05 — Release pending.\n")
    write(root, d + "audit/requests/REQUEST_ingest.md", "---\nunit: K-001\n---\n# Request record\n\n"
          "### R1 — 2026-03-02 — opening request\n> ingest the mails\n")
    write(root, d + "audit/reviews/REVIEW_LOG.md", "# Review log\n\n| date | doc_key | tier | model "
          "| findings_raised | findings_real | verdict | revise_rounds |\n|---|---|---|---|---|---|---|---|\n"
          "| 2026-03-06 | K-001 design | design | m | 2 | 2 | PASS | 1 |\n")
    write(root, d + "solutions/ANALYSIS_ingest.md", "---\ndescription: Mail ingestion.\n"
          "status: IN_PROGRESS\nid: K-001\nlevel: L3\ndomain: knowledge\nstart_date: 2026-03-01\n---\n"
          "# ANALYSIS: ingest\n\nSee fact `a00000000001` and token `deadbeefcafe`.\n\n"
          "The pre" + NBH + "commit hook.\n\n<img src=x onerror=alert(1)> and </script>\n\n"
          "[bad](javascript:alert(1)) [ok](../vision/project_vision.md) [web](https://example.org)\n\n"
          "## Objective\n\nRead the mails.\n\n## Feature Vision\n\nServes the field.\n\n"
          "## Use Cases / User Needs\n\n- UC1 read a mail.\n\n## Functional Spec\n\nNot triggered: "
          "no behavior change.\n\n## Sources and Verification\n\nEvery fact cites its mail.\n\n"
          "## Capability Ledger\n\n| Capability | Verdict |\n|---|---|\n| read | EXISTS |\n\n"
          "## Impact\n\nOne parser.\n\n## Action Plan\n\n1. Parse.\n\n## Test Strategy\n\nFixtures.\n\n"
          "## Notes on naming\n\nOutside the chain.\n\n"
          "## Diary\n\n- **2026-03-01** — Opened.\n- **2026-03-08** — Mails 1-11 read.\n")
    write(root, d + "solutions/MERGE_REVIEW_ingest.md", "---\nfeature: K-001\n---\n# Merge review: ingest\n")
    write(root, d + "solutions/E2E_TEST_ingest.md", "---\nfeature: K-001\n---\n# E2E test: ingest\n")
    write(root, d + "solutions/ANALYSIS_old.md", "---\nstatus: COMPLETED\nid: K-000\nlevel: L2\n"
          "start_date: 2026-01-01\nend_date: 2026-01-09\n---\n# ANALYSIS: old\n")
    # topics
    write(root, d + "topics/pumps.md", "---\ntopic: pumps\ndescription: Every pump.\n"
          "synonyms: [pump, impeller unit]\ngaps: no data on 2019 models\n---\n# Pumps\n")
    write(root, d + "topics/valves.md", "---\ntopic: valves\nparents: [pumps]\n---\n")
    seals = ("---\ntopic: seals\nparents: [pumps]\nrelated: valves\n---\n# Seals\n\n" + CLAIM_HEAD
             + row("a00000000001", "The seal lasts two years.", "corpus/given/manual.txt#L2-3", "GIVEN",
                   valid="from 2026-01-01", qty="2 y duration", about="pumps")
             + row("a00000000002", "Spec says 40 bar.", "corpus/given/spec.pdf#p=2@5-15", "GIVEN")
             + row("a00000000003", "Mario said it leaks.", "corpus/notes/call.md", "ELICITED")
             + row("a00000000004", "So it leaks after two years.", "corpus/notes/reasoned.md", "DERIVED")
             + row("a00000000005", "Use the manual figure.", "corpus/notes/decided.md", "DERIVED")
             + row("a00000000006", "Untraceable.", "corpus/notes/lost.md", "DERIVED")
             + row("a00000000007", "Escapes.", "corpus/notes/escape.md", "DERIVED")
             + row("a00000000008", "Gone source.", "corpus/given/gone.txt#L1-1", "GIVEN")
             + row("b00000000001", "Old figure.", "corpus/given/manual.txt#L1-1", "GIVEN",
                   state="SUPERSEDED b00000000002, b00000000003")
             + row("b00000000002", "Mid figure.", "corpus/given/manual.txt#L1-1", "GIVEN",
                   state="SUPERSEDED b00000000004")
             + row("b00000000003", "Lost branch.", "corpus/given/manual.txt#L1-1", "GIVEN",
                   state="SUPERSEDED b0000000dead9")
             + row("b00000000004", "Current figure.", "corpus/given/manual.txt#L1-1", "GIVEN")
             + row("c00000000001", "Loop one.", "corpus/given/manual.txt#L1-1", "GIVEN",
                   state="SUPERSEDED c00000000002")
             + row("c00000000002", "Loop two.", "corpus/given/manual.txt#L1-1", "GIVEN",
                   state="SUPERSEDED c00000000001")
             + row("d00000000001", "Pressure 40.", "corpus/given/spec.pdf#p=1@0-4", "GIVEN",
                   state="CONTESTED d00000000002")
             + row("d00000000002", "<script>alert(1)</script> pressure 50 </script>",
                   "corpus/given/manual.txt#L3-3", "GIVEN", state="CONTESTED d00000000001"))
    write(root, d + "topics/seals.md", seals)
    write(root, d + "topics/old-seals.md", "---\ntopic: old-seals\nstatus: SUPERSEDED\n"
          "redirect_to: seals\n---\n")
    write(root, d + "topics/loop-a.md", "---\ntopic: loop-a\nparents: [loop-b]\n---\n")
    write(root, d + "topics/loop-b.md", "---\ntopic: loop-b\nparents: [loop-a]\n---\n")
    write(root, d + "topics/orphan.md", "---\ntopic: orphan\nparents: [missing-x]\n---\n")
    write(root, d + "topics/under-merged.md", "---\ntopic: under-merged\nparents: [old-seals]\n---\n"
          + CLAIM_HEAD + row("e00000000001", "Valves close.", "corpus/given/manual.txt#L1-2", "GIVEN"))
    # corpus
    write(root, d + "corpus/given/manual.txt", "line one\nline two\nline three\x0c still three\n")
    write(root, d + "corpus/given/manual.txt.meta.md", "---\ndate: 2026-02-01\n"
          "extracted_through: complete\n---\n")
    write(root, d + "corpus/given/spec.txt", "p1 text 40 bar\x0cpage two: rated 40 bar max")
    write(root, d + "corpus/given/spec.pdf", "%PDF fake")
    write(root, d + "corpus/given/spec.pdf.meta.md", "---\ndate: 2026-02-03\nextracted_through: p=2\n"
          "supersedes: spec-old.pdf\n---\n")
    write(root, d + "corpus/given/spec-old.pdf", "%PDF old")
    write(root, d + "corpus/given/spec-old.pdf.meta.md", "---\ndate: 2025-12-01\n---\n")
    write(root, d + "corpus/notes/call.md", "---\norigin: elicited\ndate: 2026-03-03\n---\nMario, phone.\n")
    write(root, d + "corpus/notes/reasoned.md", "---\nderived_from: [call.md, manual.txt]\n---\nWhy.\n")
    write(root, d + "corpus/notes/decided.md", "---\nderived_from: manual.txt\n---\nUse it.\n")
    write(root, d + "corpus/notes/old-based.md", "---\nderived_from: spec-old.pdf\n---\nFrom the old spec.\n")
    write(root, d + "corpus/notes/lost.md", "---\nderived_from: nothing.md\n---\nLost.\n")
    write(root, d + "corpus/notes/escape.md", "---\nderived_from: %s\n---\nOut.\n"
          % Path(outside).resolve().as_posix())
    return Path(root)


def build_code(root):
    d = "ai_docs/"
    write(root, d + "README.md", "# Widget app docs\n\nThe widget service.\n")
    write(root, d + "INDEX.md", "# Manifest\n")
    write(root, d + "reference/INDEX.md", "# Guide router\n\nNo guides yet.\n")
    write(root, d + "vision/project_vision.md", "---\nstatus: DRAFT\n---\n# Vision\n\n## Context\n\nA shop.\n\n"
          "## North Star\n\nShip widgets.\n")
    write(root, d + "audit/HANDOFF_api.md", "---\nworkstream: F-001 api\nlevel: L3\nstatus: PLANNED\n"
          "since: 2026-04-01\nnext: write the contract\nupdated: 2026-04-02\n---\n")
    write(root, d + "solutions/ANALYSIS_api.md", "---\nstatus: PLANNED\nid: F-001\nlevel: L3\n"
          "start_date: 2026-04-01\n---\n# ANALYSIS: api\n\n## Diary\n\n- **2026-04-01** — Opened.\n")
    write(root, d + "solutions/ANALYSIS_a_first.md", "---\nstatus: DONE\nid: F-010\nlevel: L1\n---\n# ANALYSIS: z\n")
    return Path(root)


def build_mkt(root):
    d = "mkt_docs/"
    write(root, d + "README.md", "---\ndefault_domain: marketing\n---\n# Launch plan\n\nGo to market.\n")
    write(root, d + "INDEX.md", "# Manifest\n")
    write(root, d + "reference/INDEX.md", "# Guide router\n")
    write(root, d + "vision/project_vision.md", "# Vision\nStatus: DRAFT\n\n## Goals\n\nSell.\n")
    return Path(root)


def tree_digest(path):
    h = hashlib.sha256()
    for p in sorted(Path(path).rglob("*")):
        h.update(p.relative_to(path).as_posix().encode())
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()


def load_js(path):
    """A data file is `window.X = <json>;` -- read it back as the page would."""
    text = Path(path).read_text(encoding="utf-8")
    body = text.split("=", 1)[1].strip()
    assert body.endswith(";"), path
    return json.loads(body[:-1])


def run(project, *extra):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = docs_site.main(["--root", str(project)] + list(extra))
    return code, out.getvalue()


class SiteCase(unittest.TestCase):
    """Builds the three projects once and generates each site once."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="docs_site_")
        base = Path(cls.tmp)
        cls.outside = write(base, "outside/secret.md", "---\norigin: elicited\n---\nTOPSECRET-BODY\n")
        cls.kb = build_kb(base / "kb", cls.outside)
        cls.code = build_code(base / "code")
        cls.mkt = build_mkt(base / "mkt")
        cls.digests = {p: tree_digest(p / d) for p, d in
                       ((cls.kb, "ai_docs"), (cls.code, "ai_docs"), (cls.mkt, "mkt_docs"))}
        cls.results = {p: run(p) for p in (cls.kb, cls.code, cls.mkt)}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def out(self, project):
        return project / ".docs-site"

    def data(self, project, name):
        return load_js(self.out(project) / "data" / (name + ".js"))


# ---------------------------------------------------------------- the command

class Command(SiteCase):

    def test_generates_with_one_summary_line_and_exit_0(self):
        for project, (code, text) in self.results.items():
            self.assertEqual(code, 0, text)
            self.assertTrue((self.out(project) / "index.html").is_file())
            self.assertIn("[ok]", text)

    def test_reads_the_legacy_marketing_root(self):
        core = self.data(self.mkt, "core")
        self.assertEqual(core["meta"]["docs_dir"], "mkt_docs")

    def test_missing_root_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            code, text = run(Path(d))
            self.assertEqual(code, 2, text)

    def test_ambiguous_root_exits_2_with_the_resolvers_message(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "ai_docs").mkdir()
            (Path(d) / "mkt_docs").mkdir()
            code, text = run(Path(d))
            self.assertEqual(code, 2)
            self.assertIn("more than one documentation root", text)

    def test_out_inside_the_docs_root_is_refused(self):
        code, text = run(self.code, "--out", str(self.code / "ai_docs" / "site"))
        self.assertEqual(code, 2, text)
        self.assertFalse((self.code / "ai_docs" / "site").exists())

    def test_out_over_a_folder_it_did_not_write_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "mine.txt", "user file")
            code, text = run(self.code, "--out", d)
            self.assertEqual(code, 2, text)
            self.assertEqual(sorted(os.listdir(d)), ["mine.txt"])

    def test_out_over_its_own_earlier_run_is_accepted(self):
        code, text = run(self.code)
        self.assertEqual(code, 0, text)

    def test_identical_output_across_two_runs(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a", Path(d) / "b"
            self.assertEqual(run(self.kb, "--out", str(a))[0], 0)
            self.assertEqual(run(self.kb, "--out", str(b))[0], 0)
            files = sorted(p.relative_to(a).as_posix() for p in a.rglob("*") if p.is_file())
            self.assertEqual(files, sorted(p.relative_to(b).as_posix() for p in b.rglob("*") if p.is_file()))
            for rel in files:
                ta, tb = (a / rel).read_text(encoding="utf-8"), (b / rel).read_text(encoding="utf-8")
                if rel == "data/core.js":
                    ja, jb = load_js(a / rel), load_js(b / rel)
                    ja["meta"].pop("generated"), jb["meta"].pop("generated")
                    self.assertEqual(ja, jb)
                else:
                    self.assertEqual(ta, tb, rel)

    def test_an_unreadable_file_is_named_and_exits_1(self):
        """Whichever reader meets it -- the generator's own or a shared one -- an
        unreadable file is named on its own line, the run exits 1, and the site is
        still written from the rest."""
        cases = ((build_code, "ai_docs/solutions/ANALYSIS_api.md"),
                 (build_code, "ai_docs/audit/HANDOFF_api.md"),
                 (build_code, "ai_docs/README.md"),
                 (lambda r: build_kb(r, self.outside), "ai_docs/topics/seals.md"))
        for builder, rel in cases:
            with self.subTest(rel), tempfile.TemporaryDirectory() as d:
                project = builder(Path(d) / "p")
                target = project / rel
                real = sdlc_core.read_text

                def flaky(path, real=real, target=target):
                    if Path(path) == target:
                        raise PermissionError(13, "denied", str(path))
                    return real(path)
                sdlc_core.read_text = flaky
                try:
                    code, text = run(project)
                finally:
                    sdlc_core.read_text = real
                self.assertEqual(code, 1, text)
                self.assertIn("[ERROR] unreadable: " + rel.split("/", 1)[1] + " (", text)
                self.assertTrue((project / ".docs-site" / "index.html").is_file())
                self.assertIs(sdlc_core.read_text, real, "the guard restores the shared reader")

    def test_a_raw_read_that_fails_is_named_and_exits_1(self):
        with tempfile.TemporaryDirectory() as d:
            project = build_code(Path(d) / "p")
            target = project / "ai_docs" / "vision" / "project_vision.md"
            real = Path.read_bytes

            def flaky(self_path):
                if self_path == target:
                    raise PermissionError(13, "denied", str(self_path))
                return real(self_path)
            Path.read_bytes = flaky
            try:
                code, text = run(project)
            finally:
                Path.read_bytes = real
            self.assertEqual(code, 1, text)
            self.assertIn("[ERROR] unreadable: vision/project_vision.md (", text)

    def test_the_command_runs_as_a_script(self):
        r = subprocess.run([sys.executable, str(HERE / "docs_site.py"), "--root", str(self.code),
                            "--out", str(Path(self.tmp) / "script_out")],
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(len([l for l in r.stdout.splitlines() if l.startswith("[ok]")]), 1)

    def test_it_is_not_named_site(self):
        self.assertFalse((HERE / "site.py").exists())


# ------------------------------------------------------ acceptance criteria

class Criterion01CheckRule(SiteCase):
    """Every source the orientation reads is on the home page or one click from it."""

    def test_orientation_sources_reach_the_home(self):
        for project in (self.kb, self.code, self.mkt):
            core = self.data(project, "core")
            docs = self.data(project, "docs")
            links = core["home"]["links"]
            for key in ("readme", "manifest", "router"):
                self.assertIn(links[key], docs, (project, key))
            self.assertIn("work", links)
        core = self.data(self.kb, "core")
        self.assertEqual(core["home"]["links"]["notes"], "audit/project_notes.md")
        self.assertEqual(core["home"]["links"]["topics"], "map")

    def test_the_orientation_list_is_the_validators_own(self):
        """The home links come from sdlc_core.orient_docs, not from a copy of it."""
        links = self.data(self.kb, "core")["home"]["links"]
        for _label, rel in sdlc_core.orient_docs():
            rel = rel.split("/", 1)[1]
            if (self.kb / "ai_docs" / rel).is_file():
                self.assertIn(rel, links.values(), rel)

    def test_every_page_is_built_from_the_docs_root_only(self):
        docs = self.data(self.kb, "docs")
        for path in docs:
            self.assertFalse(path.startswith(("/", "..")), path)
            self.assertTrue((self.kb / "ai_docs" / path).is_file(), path)
        self.assertNotIn("TOPSECRET-BODY", json.dumps(self.data(self.kb, "kb")))


class Criterion02FourQuestions(SiteCase):

    def test_home_answers_the_four_questions_on_each_lens(self):
        for project in (self.kb, self.code, self.mkt):
            home = self.data(project, "core")["home"]
            self.assertTrue(home["title"])
            self.assertIn("lately", home)
            self.assertIn("open", home)
            self.assertIn("known", home)
        home = self.data(self.kb, "core")["home"]
        self.assertEqual(home["title"], "Pump field KB")
        self.assertIn("What we know about the pumps", home["intro_html"])
        self.assertEqual(home["vision"]["status"], "APPROVED (v2)")
        self.assertEqual(home["vision"]["section_title"], "North Star")
        self.assertTrue(home["vision"]["north_star"])
        self.assertEqual([a["slug"] for a in home["known"]], ["pumps"])
        self.assertEqual(self.data(self.code, "core")["home"]["vision"]["status"], "DRAFT")

    def test_the_north_star_is_found_by_name_and_shown_first(self):
        """R25: the Vision's North Star, wherever it sits; the first section only when
        the Vision has none -- and then it is not called a North Star."""
        code = self.data(self.code, "core")["home"]["vision"]
        self.assertEqual((code["section_title"], code["north_star"]), ("North Star", True))
        self.assertIn("Ship widgets.", code["section_html"])
        mkt = self.data(self.mkt, "core")["home"]["vision"]
        self.assertEqual((mkt["section_title"], mkt["north_star"]), ("Goals", False))
        app = (PAGE_DIR / "app.js").read_text(encoding="utf-8")
        self.assertIn("h.vision && h.vision.north_star", app)

    def test_open_now_names_each_workstream_with_its_next_step(self):
        home = self.data(self.kb, "core")["home"]
        names = [c["name"] for c in home["open"]]
        self.assertIn("K-001 mail ingestion", names)


class Criterion04Counts(SiteCase):
    """Per-item counts equal the probe's; nothing sorted or filtered by them."""

    def test_counts_equal_the_validators_parse(self):
        kb = self.data(self.kb, "kb")
        docs = self.kb / "ai_docs"
        per_source, topics_of = {}, {}
        for slug, node in knowledge.kb_load_topics(docs).items():
            rows, _ = knowledge.kb_parse_claims(sdlc_core.read_text(docs / node["file"]))
            if slug in kb["topics"] and not kb["topics"][slug].get("merged_into"):
                self.assertEqual(kb["topics"][slug]["count"], len(rows), slug)
            for r in rows:
                for src in sorted(set(knowledge.kb_claim_sources(r))):
                    if src.startswith("corpus/given/"):
                        name = src[len("corpus/given/"):]
                        per_source[name] = per_source.get(name, 0) + 1
                        topics_of.setdefault(name, set()).add(slug)
        for name, src in kb["sources"].items():
            self.assertEqual(src["facts"], per_source.get(name, 0), name)
            self.assertEqual(src["topics"], sorted(topics_of.get(name, ())), name)

    def test_topics_are_listed_by_slug_not_by_count(self):
        kb = self.data(self.kb, "kb")
        self.assertEqual(kb["order"], sorted(kb["order"]))


class Criterion05Passages(SiteCase):

    def test_each_passage_equals_the_span_its_locator_addresses(self):
        facts = self.data(self.kb, "kb")["facts"]
        p = facts["a00000000001"]["sources"][0]
        self.assertEqual(p["passage"], "line two\nline three\x0c still three")
        self.assertEqual(p["where"], {"lines": [2, 3]})
        p = facts["a00000000002"]["sources"][0]
        self.assertEqual(p["passage"], "two: rated")
        self.assertEqual(p["where"], {"page": 2})

    def test_a_missing_source_gives_its_reason(self):
        p = self.data(self.kb, "kb")["facts"]["a00000000008"]["sources"][0]
        self.assertNotIn("passage", p)
        self.assertEqual(p["reason"], "no_file")

    def test_every_branch_of_a_replacement_chain_ends_or_stops(self):
        facts = self.data(self.kb, "kb")["facts"]
        ends = facts["b00000000001"]["chain_ends"]
        self.assertIn({"id": "b00000000004"}, ends)
        self.assertIn({"stop": "missing", "id": "b0000000dead9"}, ends)
        loop = facts["c00000000001"]["chain_ends"]
        self.assertEqual(loop, [{"stop": "loop", "id": "c00000000001"}])

    def test_inferred_classes(self):
        facts = self.data(self.kb, "kb")["facts"]
        self.assertEqual(facts["a00000000004"]["ground_class"], "statement")
        self.assertEqual(facts["a00000000005"]["ground_class"], "documents")
        self.assertEqual(facts["a00000000006"]["ground_class"], "untraceable")
        self.assertEqual(facts["a00000000007"]["ground_class"], "untraceable",
                         "a path leaving the docs root is never followed")

    def test_the_walk_agrees_with_the_time_cycle_edges(self):
        docs = self.kb / "ai_docs"
        dangling = {(o, e) for o, e in knowledge.kb_time_cycle(docs)["dangling"]}
        for p in sorted((docs / "corpus" / "notes").glob("*.md")):
            meta = sdlc_core.load_frontmatter(sdlc_core.read_text(p).splitlines())
            for e in knowledge._kb_df_entries(meta.get("derived_from")):
                owner = "corpus/notes/" + p.name
                mine = docs_site.resolve_derived(docs, e, inside_only=False)
                self.assertEqual(mine is None, (owner, e) in dangling, (owner, e))

    def test_the_walk_reaches_the_same_file_as_the_time_cycle(self):
        """Not only whether an entry resolves: WHICH file. The time cycle's chain
        names the file a note's derived_from reached; the site must reach it too."""
        docs = self.kb / "ai_docs"
        chain = knowledge.kb_time_cycle(docs)["chain"]
        self.assertTrue(chain, "the fixture must give the time cycle a chain to walk")
        for owner, ground, via in chain:
            meta = sdlc_core.load_frontmatter(sdlc_core.read_text(docs / owner).splitlines())
            reached = [docs_site.resolve_derived(docs, e)
                       for e in knowledge._kb_df_entries(meta.get("derived_from"))]
            self.assertIn(via[-1], reached, owner)

    def test_inferred_grounds_name_what_they_rest_on(self):
        grounds = self.data(self.kb, "kb")["facts"]["a00000000004"]["grounds"]
        kinds = sorted(g["kind"] for g in grounds)
        self.assertEqual(kinds, ["document", "statement"])


class Criterion06StatementMark(SiteCase):

    def test_facts_resting_on_a_statement_carry_the_mark(self):
        facts = self.data(self.kb, "kb")["facts"]
        self.assertTrue(facts["a00000000003"]["statement"])
        self.assertTrue(facts["a00000000004"]["statement"])
        self.assertFalse(facts["a00000000001"]["statement"])

    def test_holds_when_value_and_also_concerns_are_as_written(self):
        f = self.data(self.kb, "kb")["facts"]["a00000000001"]
        self.assertEqual((f["valid"], f["qty"], f["about"]), ("from 2026-01-01", "2 y duration", "pumps"))

    def test_every_place_a_fact_text_is_shown_carries_the_mark(self):
        """Enumerate every read of a fact's text in the page and require each one to
        sit where the mark is applied: the list line, the panel (with its notice),
        the one title function the map labels and tooltips use, or the filter that
        only matches words. A new view that shows `f.text` raw fails here."""
        app = (PAGE_DIR / "app.js").read_text(encoding="utf-8")
        allowed = {"factTitle", "factLine", "factPanel"}
        reads = [m.start() for m in re.finditer(r"\bf0?\.text\b", app)
                 if not app[:m.start()].endswith("normalize(")]   # matching words, not showing
        self.assertTrue(reads)
        for pos in reads:
            owner = re.findall(r"\n  function (\w+)\(", app[:pos])[-1]   # the page's own functions
            self.assertIn(owner, allowed, "a fact's text is shown raw in %s()" % owner)
        self.assertRegex(app, r"function factTitle\(f\) \{ return f\.statement \?")
        self.assertRegex(app, r"function factLine\([^)]*\) \{[\s\S]*?if \(f\.statement\)")
        self.assertRegex(app, r"function factPanel\([^)]*\) \{[\s\S]*?f\.statement \? el\(\"div\", \{ \"class\": \"statement-notice\"")
        self.assertIn("e.statement ?", app, "search hits show the mark")

    def test_search_entries_carry_the_mark(self):
        facts = self.data(self.kb, "kb")["facts"]
        for e in self.data(self.kb, "kb")["search"]:
            if e["k"] == "fact":
                self.assertEqual(e["statement"], facts[e["id"]]["statement"], e["id"])


class Criterion07NoChangeNoNetwork(SiteCase):

    def test_the_docs_root_is_unchanged(self):
        for (project, d) in ((self.kb, "ai_docs"), (self.code, "ai_docs"), (self.mkt, "mkt_docs")):
            self.assertEqual(tree_digest(project / d), self.digests[project])

    def test_the_page_makes_no_network_request(self):
        for p in sorted(self.out(self.kb).rglob("*")):
            if p.suffix not in (".html", ".js", ".css"):
                continue
            text = p.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"(?i)<(script|link|img|iframe)[^>]+(src|href)\s*=\s*[\"']?(https?:)?//")
            self.assertNotRegex(text, r"(?i)@import|url\(\s*[\"']?(https?:)?//")
            for api in ("fetch(", "XMLHttpRequest", "WebSocket", "sendBeacon", "EventSource"):
                self.assertNotIn(api, text, p.name)

    def test_page_files_are_classic_scripts(self):
        html = (self.out(self.kb) / "index.html").read_text(encoding="utf-8")
        self.assertNotIn('type="module"', html)


FORBIDDEN = ("claim", "ledger", "provenance", "elicited", "given", "derived", "ruling",
             "imported", "superseded", "contested", "corpus", "sidecar", "locator", "slug",
             "frontmatter", "workstream", "handoff", "L1", "L2", "L3")


def strings_table():
    text = (PAGE_DIR / "strings.js").read_text(encoding="utf-8")
    return re.findall(r'"((?:[^"\\]|\\.)*)"\s*[,}\n]', text.split("=", 1)[1])


class Criterion08Words(unittest.TestCase):

    def test_no_interface_string_uses_the_skills_vocabulary(self):
        values = strings_table()
        self.assertGreater(len(values), 50)
        for v in values:
            for w in FORBIDDEN:
                self.assertNotRegex(v, r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(w)
                                    if w[0] == "L" else r"(?i)\b%s\b" % w, v)

    def test_the_static_page_has_no_wording_of_its_own(self):
        html = (PAGE_DIR / "index.html").read_text(encoding="utf-8")
        text = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", html, flags=re.S)
        self.assertEqual(text.split(), ["Loading…"] if "Loading…" in text else [])

    def test_every_classifying_label_carries_its_explanation(self):
        text = (PAGE_DIR / "strings.js").read_text(encoding="utf-8")
        for key in ("origin_given", "origin_elicited", "origin_derived", "origin_ruling",
                    "origin_imported", "state_superseded", "state_contested"):
            self.assertIn(key + "_why", text)


class Criterion09Search(SiteCase):

    def test_the_empty_search_sentences(self):
        text = (PAGE_DIR / "strings.js").read_text(encoding="utf-8")
        self.assertIn("Nothing found among facts, topics and documents. The full text of source "
                      "documents is not searched here — not finding something does not mean the "
                      "sources are silent on it.", text)
        self.assertIn("Nothing found in the documents.", text)

    def test_normalization_folds_case_accents_dashes_and_invisibles(self):
        n = docs_site.normalize
        self.assertEqual(n("Pre" + NBH + "Commit"), "pre-commit")
        self.assertEqual(n("Café​"), "cafe")
        self.assertEqual(n("a—b–c"), "a-b-c")

    def test_a_word_with_a_non_breaking_hyphen_is_indexed_findably(self):
        entries = self.data(self.kb, "core")["search"]
        hit = [e for e in entries if e["path"] == "solutions/ANALYSIS_ingest.md"]
        self.assertTrue(hit and "pre-commit" in hit[0]["n"])

    def test_the_page_normalizes_the_query_the_same_way(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("node not available: the browser-side half is checked by the E2E script")
        app = (PAGE_DIR / "app.js").read_text(encoding="utf-8")
        m = re.search(r"function normalize\(s\) \{.*?\n[ \t]*\}[ \t]*\n", app, re.S)
        self.assertIsNotNone(m)
        cases = ["Pre" + NBH + "Commit", "Café​", "a—b–c", "  A b  "]
        script = m.group(0) + "\nconsole.log(JSON.stringify(%s.map(normalize)));" % json.dumps(cases)
        r = subprocess.run([node], input=script, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(json.loads(r.stdout), [docs_site.normalize(c) for c in cases])


class Criterion10to13WorkViews(SiteCase):

    def test_rebuilt_from_the_documents_on_every_run(self):
        with tempfile.TemporaryDirectory() as d:
            project = build_code(Path(d) / "p")
            run(project)
            write(project, "ai_docs/audit/HANDOFF_api.md", "---\nworkstream: F-001 api\nstatus: DONE\n"
                  "since: 2026-04-01\nnext: nothing\n---\n")
            run(project)
            card = self.data(project, "core")["work"]["cards"][0]
            self.assertEqual((card["status"], card["next"]), ("DONE", "nothing"))

    def test_open_work_order_is_group_then_updated_then_name(self):
        cards = self.data(self.kb, "core")["work"]["cards"]
        self.assertEqual([c["name"] for c in cards],
                         ["K-002 waiting for the supplier", "K-001 mail ingestion", "K-003 undated"])
        self.assertEqual([c["group"] for c in cards], [1, 3, 8], "READY is not a group")

    def test_next_steps_are_verbatim_and_complete(self):
        cards = {c["name"]: c for c in self.data(self.kb, "core")["work"]["cards"]}
        self.assertEqual(cards["K-001 mail ingestion"]["next"],
                         "read the March mails, then the April ones; keep the order as received")

    def test_cards_carry_only_declared_values(self):
        allowed = {"name", "status", "group", "level", "since", "updated", "branch", "next", "path"}
        for c in self.data(self.kb, "core")["work"]["cards"]:
            self.assertLessEqual(set(c), allowed)
        for u in self.data(self.kb, "core")["units"]:
            self.assertLessEqual(set(u), {"name", "id", "status", "group", "level", "lens",
                                          "start", "end", "path"})

    def test_units_sorted_by_id_as_text(self):
        units = self.data(self.code, "core")["units"]
        self.assertEqual([u["id"] for u in units], ["F-001", "F-010"])

    def test_project_notes_below_the_cards(self):
        notes = self.data(self.kb, "core")["work"]["notes"]
        self.assertEqual(notes["path"], "audit/project_notes.md")
        self.assertIn("Release pending.", notes["html"])

    def test_no_units_page_on_a_marketing_project(self):
        meta = self.data(self.mkt, "core")["meta"]
        self.assertIsNone(meta["units_page"])
        self.assertIsNone(self.data(self.mkt, "core")["units"])
        self.assertEqual(self.data(self.kb, "core")["meta"]["units_page"], "features")

    def test_the_only_action_is_opening_a_document(self):
        app = (PAGE_DIR / "app.js").read_text(encoding="utf-8")
        for verb in ("localStorage", "sessionStorage", "indexedDB", "<form", "download=",
                     "document.cookie", "window.open("):
            self.assertNotIn(verb, app)

    def test_no_people_or_schedule_fields(self):
        app = (PAGE_DIR / "app.js").read_text(encoding="utf-8")
        strings = (PAGE_DIR / "strings.js").read_text(encoding="utf-8")
        for word in ("assignee", "owner", "due", "iteration", "sprint", "team", "role"):
            self.assertNotRegex(app + strings, r"(?i)\b%s\b" % word)


class Criterion14Announcements(unittest.TestCase):

    def test_skill_md_names_the_command_and_tells_no_agent_to_choose(self):
        skill = (HERE.parent / "SKILL.md").read_text(encoding="utf-8")
        lines = [l for l in skill.splitlines() if "docs_site.py" in l]
        self.assertEqual(len(lines), 1, "one line announces the site")
        self.assertLessEqual(len(lines[0].encode("utf-8")), 160, "the owner accepted about 160 bytes (R13, R15)")
        self.assertNotRegex(lines[0], r"(?i)\b(choose|prefer|avoid|skip|pick|order)\b")

    def test_the_package_ships_the_page_and_no_test(self):
        pkg = HERE.parent.parent.parent / "package.json"
        if not pkg.is_file():
            self.skipTest("installed skill: no package.json")
        files = json.loads(pkg.read_text(encoding="utf-8"))["files"]
        skill = HERE.parent.name
        for rel in ("scripts/docs_site.py", "docs_site/index.html", "docs_site/app.js",
                    "docs_site/style.css", "docs_site/strings.js"):
            self.assertIn("skills/%s/%s" % (skill, rel), files)
        self.assertFalse([f for f in files if "test_" in f])


class Criterion15FeatureChain(SiteCase):
    """An analysis page shows the chain the agent works through (R24)."""

    STEPS = ["vision", "use_cases", "flows", "risks", "solution", "design", "merge_tests", "diary"]

    def chain(self, project, rel):
        return self.data(project, "docs")[rel]["chain"]

    def test_steps_in_order_with_their_sections_as_written(self):
        chain = self.chain(self.kb, "solutions/ANALYSIS_ingest.md")
        self.assertEqual([s["step"] for s in chain["steps"]], self.STEPS)
        titles = {s["step"]: [x["title"] for x in s["sections"]] for s in chain["steps"]}
        self.assertEqual(titles, {
            "vision": ["Objective", "Feature Vision"],
            "use_cases": ["Use Cases / User Needs"],
            "flows": ["Functional Spec"],
            "risks": ["Sources and Verification"],
            "solution": ["Capability Ledger", "Impact"],
            "design": ["Action Plan", "Test Strategy"],
            "merge_tests": [],
            "diary": ["Diary"]})

    def test_each_section_link_lands_on_its_heading(self):
        page = self.data(self.kb, "docs")["solutions/ANALYSIS_ingest.md"]
        for step in page["chain"]["steps"]:
            for sec in step["sections"]:
                self.assertIn('id="%s"' % sec["id"], page["html"], sec)

    def test_sections_outside_the_chain_stay_in_the_document(self):
        page = self.data(self.kb, "docs")["solutions/ANALYSIS_ingest.md"]
        listed = [x["title"] for s in page["chain"]["steps"] for x in s["sections"]]
        self.assertNotIn("Notes on naming", listed)
        self.assertIn("Outside the chain.", page["html"])

    def test_merge_brief_e2e_script_and_request_record_are_linked(self):
        docs = self.data(self.kb, "docs")
        comp = docs["solutions/ANALYSIS_ingest.md"]["chain"]["companions"]
        self.assertEqual(comp, {"merge": "solutions/MERGE_REVIEW_ingest.md",
                                "e2e": "solutions/E2E_TEST_ingest.md",
                                "request": "audit/requests/REQUEST_ingest.md"})
        for rel in comp.values():
            self.assertIn(rel, docs)

    def test_the_vision_step_reaches_the_north_star(self):
        """R25: the project's North Star is one click from every analysis."""
        ns = self.data(self.kb, "docs")["solutions/ANALYSIS_ingest.md"]["chain"]["north_star"]
        self.assertEqual(ns, {"path": "vision/project_vision.md", "id": "north-star"})
        vision = self.data(self.kb, "docs")["vision/project_vision.md"]["html"]
        self.assertIn('id="north-star"', vision)
        self.assertIsNone(self.data(self.mkt, "docs")["vision/project_vision.md"].get("chain"))

    def test_a_missing_step_is_empty_never_scored(self):
        chain = self.chain(self.code, "solutions/ANALYSIS_api.md")
        self.assertEqual({s["step"]: len(s["sections"]) for s in chain["steps"]},
                         {k: 1 if k == "diary" else 0 for k in self.STEPS})
        self.assertEqual(chain["companions"], {"merge": None, "e2e": None, "request": None})
        for s in chain["steps"]:
            self.assertEqual(set(s), {"step", "sections"})
            for sec in s["sections"]:
                self.assertEqual(set(sec), {"title", "id"})

    def test_every_lens_risk_section_is_the_risk_step(self):
        """The risk headings are the validator's own, for every lens."""
        headings = list(sdlc_core.SECURITY_SECTION)
        for d in sdlc_core.DOMAINS.values():
            headings += list(d["risk_section"])
        for h in headings:
            self.assertEqual(docs_site.chain_step(h + " and more"), "risks", h)
        for pair in sdlc_core.ANALYSIS_SECTIONS:
            for h in pair:
                self.assertIsNotNone(docs_site.chain_step(h), h)

    def test_only_analyses_carry_a_chain(self):
        for rel, page in self.data(self.kb, "docs").items():
            self.assertEqual("chain" in page, rel.startswith("solutions/ANALYSIS_"), rel)

    def run_chain_strip(self, chain):
        """Run the page's own chainStrip in Node, with a stub DOM: [(class, text)] per step."""
        node = shutil.which("node")
        if not node:
            self.skipTest("node not available: the E2E script covers the page in a browser")
        app = (PAGE_DIR / "app.js").read_text(encoding="utf-8")
        m = re.search(r"  function chainStrip\(chain\) \{.*?\n  \}\n", app, re.S)
        self.assertIsNotNone(m, "chainStrip not found in app.js")
        stubs = """
var document = { getElementById: function () { return null; } };
function t(k) { return k; }
function add(n, c) {
  if (c === null || c === undefined || c === false) return;
  if (Array.isArray(c)) { c.forEach(function (x) { add(n, x); }); return; }
  n.kids.push(c);
}
function el(tag, attrs) {
  var n = { tag: tag, attrs: attrs || {}, kids: [] };
  if (attrs && attrs.text) n.kids.push(attrs.text);
  for (var i = 2; i < arguments.length; i++) add(n, arguments[i]);
  return n;
}
function link(href, text) { return el("a", { href: href }, text); }
function docHref(p) { return "#/doc/" + p; }
function docLink(p, text) { return link(docHref(p), text); }
function docAt(p, id) { return docHref(p) + "?at=" + id; }
function text(n) { return typeof n === "string" ? n : n.kids.map(text).join(" "); }
"""
        script = (stubs + m.group(0) + "\nvar out = chainStrip(%s);\n" % json.dumps(chain)
                  + "console.log(JSON.stringify(out.kids[1].kids.map(function (li) {"
                  + " return [li.attrs['class'], text(li)]; })));\n")
        r = subprocess.run([node], input=script, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        return dict(zip(self.STEPS, json.loads(r.stdout)))

    def test_a_step_with_no_section_says_so_whatever_sits_beside_it(self):
        """The North Star and the request record are linked beside the Vision step; they
        never make an analysis with no Vision section look as if it had one (round-3 B1)."""
        chain = {"steps": [{"step": s, "sections": []} for s in self.STEPS],
                 "companions": {"merge": None, "e2e": None, "request": "audit/requests/REQUEST_x.md"},
                 "north_star": {"path": "vision/project_vision.md", "id": "north-star"}}
        rows = self.run_chain_strip(chain)
        cls, text = rows["vision"]
        self.assertEqual(cls, "absent")
        self.assertIn("chain_absent", text)
        self.assertIn("chain_north_star", text)
        self.assertIn("chain_request", text)
        self.assertEqual(rows["merge_tests"][0], "absent")

    def test_a_step_with_its_own_content_is_not_absent(self):
        chain = {"steps": [{"step": s, "sections": [{"title": "T", "id": "t"}] if s == "vision" else []}
                           for s in self.STEPS],
                 "companions": {"merge": "solutions/MERGE_REVIEW_x.md", "e2e": None, "request": None},
                 "north_star": None}
        rows = self.run_chain_strip(chain)
        self.assertEqual(rows["vision"][0], "")
        self.assertNotIn("chain_absent", rows["vision"][1])
        self.assertEqual(rows["merge_tests"][0], "", "a merge brief is the step's own content")
        self.assertEqual(rows["diary"][0], "absent")

    def test_the_page_draws_the_chain_from_strings(self):
        app = (PAGE_DIR / "app.js").read_text(encoding="utf-8")
        strings = (PAGE_DIR / "strings.js").read_text(encoding="utf-8")
        self.assertIn("function chainStrip(", app)
        for step in self.STEPS:
            self.assertIn("chain_step_%s:" % step, strings)
        for key in ("chain_absent", "chain_merge", "chain_e2e", "chain_request"):
            self.assertIn(key + ":", strings)


# ------------------------------------------------------------ further cases

class KnowledgeShapes(SiteCase):

    def test_area_is_the_root_reached_by_first_parents(self):
        topics = self.data(self.kb, "kb")["topics"]
        self.assertEqual(topics["seals"]["area"], "pumps")
        self.assertEqual(topics["pumps"]["area"], "pumps")
        for slug in ("loop-a", "loop-b", "orphan", "under-merged"):
            self.assertIsNone(topics[slug]["area"], slug)

    def test_name_is_the_first_heading_else_the_slug(self):
        topics = self.data(self.kb, "kb")["topics"]
        self.assertEqual(topics["seals"]["name"], "Seals")
        self.assertEqual(topics["valves"]["name"], "valves")

    def test_a_merged_topic_forwards_and_is_neither_counted_nor_drawn(self):
        kb = self.data(self.kb, "kb")
        self.assertEqual(kb["topics"]["old-seals"]["merged_into"], "seals")
        self.assertNotIn("old-seals", kb["order"])
        self.assertNotIn("old-seals", [n["id"] for n in kb["map"]["nodes"]])

    def test_topic_fields(self):
        t = self.data(self.kb, "kb")["topics"]["pumps"]
        self.assertEqual(t["aka"], ["pump", "impeller unit"])
        self.assertEqual(t["gaps"], ["no data on 2019 models"])
        self.assertEqual(sorted(t["children"]), ["seals", "valves"])
        self.assertEqual(self.data(self.kb, "kb")["topics"]["seals"]["related"], ["valves"])

    def test_facts_in_row_order(self):
        facts = self.data(self.kb, "kb")["topics"]["seals"]["facts"]
        self.assertEqual(facts[:3], ["a00000000001", "a00000000002", "a00000000003"])

    def test_contested_names_the_other_facts(self):
        f = self.data(self.kb, "kb")["facts"]["d00000000001"]
        self.assertEqual((f["state"], f["with"]), ("contested", ["d00000000002"]))

    def test_source_reading_state_and_versions(self):
        src = self.data(self.kb, "kb")["sources"]
        self.assertEqual(src["manual.txt"]["read"], {"kind": "complete"})
        self.assertEqual(src["spec.pdf"]["read"], {"kind": "page", "n": 2, "of": 2})
        self.assertEqual(src["spec.pdf"]["newer_of"], "spec-old.pdf")
        self.assertEqual(src["spec-old.pdf"]["older_of"], "spec.pdf")
        self.assertEqual(src["spec-old.pdf"]["read"], {"kind": "unrecorded"})

    def test_map_is_laid_out_at_generation_and_deterministic(self):
        m = self.data(self.kb, "kb")["map"]
        for n in m["nodes"]:
            self.assertIsInstance(n["x"], (int, float))
            self.assertIsInstance(n["y"], (int, float))
        kinds = {e["kind"] for e in m["edges"]}
        self.assertLessEqual({"part_of", "related"}, kinds)
        shared = [e for e in m["edges"] if e["kind"] == "shared"]
        self.assertTrue(all(e["computed"] for e in shared))

    def test_fact_ids_in_documents_link_and_others_are_marked(self):
        html = self.data(self.kb, "docs")["solutions/ANALYSIS_ingest.md"]["html"]
        self.assertIn('href="#/fact/a00000000001"', html)
        self.assertIn('class="notfact"', html)


class Sanitizer(SiteCase):

    def test_markup_from_content_is_text(self):
        html = self.data(self.kb, "docs")["solutions/ANALYSIS_ingest.md"]["html"]
        self.assertNotIn("<img", html)
        self.assertNotIn("onerror=alert", html.replace("onerror=alert(1)&gt;", ""))
        self.assertNotIn("javascript:", html.replace("javascript:alert(1)", "", 0)
                         if 'href="javascript' not in html else html)
        self.assertNotIn('href="javascript', html)
        self.assertIn('href="#/doc/vision/project_vision.md"', html)
        self.assertIn('href="https://example.org"', html)

    def test_data_files_cannot_close_their_script(self):
        for p in (self.out(self.kb) / "data").glob("*.js"):
            self.assertNotIn("</", p.read_text(encoding="utf-8"), p.name)

    def test_content_cannot_address_held_markup(self):
        nul = chr(0)   # a NUL inside content: it must never reach a held placeholder
        self.assertIn("a 0 b", docs_site.markdown("a " + nul + "0" + nul + " b"))
        self.assertIn("<p>", docs_site.markdown("[x](https://e.org) " + nul + "0" + nul))

    def test_a_malformed_address_shows_not_found(self):
        app = (PAGE_DIR / "app.js").read_text(encoding="utf-8")
        self.assertRegex(app, r"try \{ rest = decodeURIComponent\(.*\); \}\s*catch \(e\) \{[^}]*notFound\(\)")

    def test_markdown_subset(self):
        f = docs_site.markdown
        self.assertIn("<h2 ", f("## Head"))
        self.assertIn("<table>", f("| a | b |\n|---|---|\n| 1 | 2 |"))
        self.assertIn("<code>x &lt;y&gt;</code>", f("`x <y>`"))
        self.assertIn("<strong>b</strong>", f("**b**"))
        self.assertIn("<blockquote>", f("> q"))
        self.assertIn("<pre><code>", f("```\n<b>\n```"))
        self.assertNotIn("<b>", f("```\n<b>\n```"))
        self.assertNotIn("<img", f("![alt](http://x/y.png)"))
        self.assertNotIn("<style", f("<style>body{}</style>"))
        self.assertIn('<a href="#top">', f("[t](#top)"))
        self.assertNotIn("<a", f("[t](data:text/html,x)"))


class Traversal(unittest.TestCase):

    def test_a_cited_path_outside_the_docs_root_is_never_followed(self):
        with tempfile.TemporaryDirectory() as d:
            docs = Path(d) / "ai_docs"
            docs.mkdir()
            outside = write(d, "x.md", "x")
            self.assertIsNone(docs_site.resolve_derived(docs, outside.as_posix()))
            self.assertIsNone(docs_site.resolve_derived(docs, "../x.md"))


class Documents(SiteCase):

    def test_the_tree_is_the_catalogs_list(self):
        tree = self.data(self.kb, "core")["tree"]
        listed = sorted(e["path"] for folder in tree for e in folder["docs"])
        catalog = sorted(r[0] for r in knowledge.memory_records(self.kb / "ai_docs"))
        self.assertEqual(listed, catalog)

    def test_audit_documents_have_pages_but_are_not_in_the_tree(self):
        docs = self.data(self.kb, "docs")
        for rel in ("audit/requests/REQUEST_ingest.md", "audit/reviews/REVIEW_LOG.md",
                    "audit/project_notes.md", "audit/HANDOFF_ingest.md"):
            self.assertIn(rel, docs)

    def test_frontmatter_shown_as_labels_and_body_formatted(self):
        page = self.data(self.kb, "docs")["solutions/ANALYSIS_ingest.md"]
        self.assertIn(["status", "IN_PROGRESS"], page["meta"])
        self.assertNotIn("status: IN_PROGRESS", page["html"])

    def test_rules_page(self):
        rules = self.data(self.kb, "core")["rules"]
        self.assertEqual(sorted(rules), ["decisions", "manifest", "vision"])
        self.assertEqual([g["path"] for g in rules["decisions"]],
                         ["architecture/ADR_2026-03-01_pick_store.md"])

    def test_guides_page(self):
        """R26: the guides have a page of their own -- router first, operative guides with
        when to read each and their declared status, then code-comprehension guides."""
        guides = self.data(self.kb, "core")["guides"]
        self.assertEqual(guides["router"], "reference/INDEX.md")
        op = guides["operative"]
        self.assertEqual([g["path"] for g in op], ["reference/GUIDE_ingest.md"])
        self.assertEqual((op[0]["when"], op[0]["status"]), ("Read before ingesting a mail.", "CURRENT"))
        self.assertEqual([g["path"] for g in guides["comprehension"]], ["reference/GUIDE_parser.md"])
        self.assertEqual(self.data(self.code, "core")["guides"],
                         {"router": "reference/INDEX.md", "operative": [], "comprehension": []})

    def test_guides_are_in_the_navigation(self):
        app = (PAGE_DIR / "app.js").read_text(encoding="utf-8")
        strings = (PAGE_DIR / "strings.js").read_text(encoding="utf-8")
        self.assertIn('["guides", "#/guides", "nav_guides"]', app)
        for key in ("nav_guides:", "guides_title:", "guides_empty:", "guides_router:",
                    "guides_operative:", "guides_comprehension:"):
            self.assertIn(key, strings)

    def test_every_page_dates_itself(self):
        meta = self.data(self.kb, "core")["meta"]
        self.assertTrue(meta["generated"])
        self.assertFalse(meta["git"])



def build_dated(root):
    """Every dated-event kind the chronology lists, plus the dated lines it must not."""
    d = "ai_docs/"
    write(root, d + "README.md", "# Dated project\n\nWhat happened.\n")
    write(root, d + "INDEX.md", "# Manifest\n")
    write(root, d + "solutions/ANALYSIS_api.md",
          "---\nstatus: IN_PROGRESS\nid: F-001\nlevel: L3\nstart_date: 2026-01-01\n"
          "end_date: 2026-12-31\n---\n# ANALYSIS: api\n\n## Objective\n\nThe 2026-02-02 plan.\n\n"
          "## Diary / Current State\n\n<!-- template comment\n     two lines -->\n"
          "**2026-03-01 — opened.** Standalone.\n\nAn undated paragraph of the same entry.\n\n"
          "- 2026-03-05: review round 1 FAIL. Fixed.\n")
    write(root, d + "solutions/SPIKE_cache.md",
          "# Spike: cache\n\n## Question to answer\n\nIs it fast?\n\n## Answer / Outcome\n\n"
          "**2026-03-03 — yes, under 1 ms.** Measured.\n\n## Consequences\n\nNone.\n")
    write(root, d + "audit/requests/REQUEST_api.md",
          "---\nunit: F-001 — api\nanalysis: ANALYSIS_api.md\n---\n# Request record: api\n\n"
          "### R1 — 2026-02-28 — opening request\n> build the api\n")
    write(root, d + "audit/reviews/REVIEW_LOG.md",
          "# Review log\n\n| date | doc_key | tier | model | instrument | findings_raised | "
          "findings_real | verdict | revise_rounds |\n|---|---|---|---|---|---|---|---|---|\n"
          "| 2026-03-04 | ANALYSIS_api.md | design | deep | subagent | 2 | 2 | PASS | 1 |\n")
    write(root, d + "audit/project_notes.md",
          "Standing note: the repo is CRLF.\n\n**2026-03-06 — release completed.** 1.0 out.\n")
    write(root, d + "architecture/ADR_2026-03-02_pick_store.md",
          "# ADR: pick the store\n\n**Status:** Accepted\n**Date:** 2026-03-02\n")
    write(root, d + "corpus/notes/decided.md",
          "---\ndate: '2026-03-07'\n---\n# Use the manual\n\nUse it.\n")
    write(root, d + "corpus/given/manual.txt.meta.md",
          "---\nsha256: x\ndate: 2026-03-08\nprovenance: GIVEN\n---\nHanded over.\n")
    return Path(root)


class Criterion03Chronology(unittest.TestCase):
    """Criterion 3 with F-073's readers: every dated event kind, most recent first, no
    analysis start or end, nothing from git -- and the page reads the same openers as
    `validate` (an entry under the template comment is an event)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="docs_site_dated_")
        cls.project = build_dated(Path(cls.tmp) / "p")
        cls.code, cls.text = run(cls.project)
        cls.core = load_js(cls.project / ".docs-site" / "data" / "core.js")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_every_kind_most_recent_first(self):
        self.assertEqual(self.code, 0, self.text)
        got = [(e["date"], e["kind"]) for e in self.core["chronology"]]
        self.assertEqual(got, [
            ("2026-03-08", "source"), ("2026-03-07", "note"), ("2026-03-06", "project_note"),
            ("2026-03-05", "diary"), ("2026-03-04", "review"), ("2026-03-03", "spike"),
            ("2026-03-02", "decision"), ("2026-03-01", "diary"), ("2026-02-28", "request")])

    def test_labels_and_links(self):
        by = {(e["date"], e["kind"]): e for e in self.core["chronology"]}
        self.assertEqual(by[("2026-03-01", "diary")]["label"], "opened")
        self.assertEqual(by[("2026-03-01", "diary")]["path"], "solutions/ANALYSIS_api.md")
        self.assertEqual(by[("2026-03-05", "diary")]["label"], "review round 1 FAIL")
        self.assertEqual(by[("2026-02-28", "request")]["label"], "R1 — opening request")
        self.assertEqual(by[("2026-03-02", "decision")]["label"], "ADR: pick the store")
        self.assertEqual(by[("2026-03-06", "project_note")]["label"], "release completed")
        self.assertEqual(by[("2026-03-07", "note")]["label"], "Use the manual")
        self.assertIn("ANALYSIS_api.md", by[("2026-03-04", "review")]["label"])
        for e in self.core["chronology"]:
            if e.get("path") is not None:
                self.assertIn(e["path"], load_js(self.project / ".docs-site" / "data"
                                                 / "docs.js"))

    def test_no_start_end_or_body_dates(self):
        dates = {e["date"] for e in self.core["chronology"]}
        for d in ("2026-01-01", "2026-12-31", "2026-02-02"):
            self.assertNotIn(d, dates)

    def test_within_a_day_the_later_entry_comes_first(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "ai_docs/solutions/ANALYSIS_x.md", "---\nid: F-1\n---\n# X\n\n## Diary\n\n"
                  "**2026-05-01 — first.** a\n\n**2026-05-01 — second.** b\n")
            got = docs_site.chronology(Path(d) / "ai_docs", {})
            self.assertEqual([e["label"] for e in got], ["second", "first"])

    def test_lately_is_the_ten_most_recent(self):
        self.assertEqual(self.core["home"]["lately"], self.core["chronology"][:10])

    def test_the_reader_is_the_validators(self):
        """UC5: the page calls the validator's reader, so changing it changes the page."""
        import unittest.mock as um
        docs = self.project / "ai_docs"
        with um.patch.object(docs_site.sdlc_core, "entry_openers",
                             lambda body: [("2099-01-01", "patched", 1)]):
            got = docs_site.chronology(docs, {})
        self.assertIn(("2099-01-01", "patched"), [(e["date"], e["label"]) for e in got])

    def test_a_source_event_opens_the_source_page(self):
        src = [e for e in self.core["chronology"] if e["kind"] == "source"]
        self.assertEqual([e["source"] for e in src], ["manual.txt"])
        app = (PAGE_DIR / "app.js").read_text(encoding="utf-8")
        # the source page exists only with a knowledge base; without one the label is text
        self.assertIn('e.source && C.meta.has_kb ? link("#/source/"', app)

    def test_a_shadow_mirror_is_not_read(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "ai_docs/solutions/ANALYSIS_old.md", "<!-- SHADOW generated from devPNT -->\n"
                  "---\nid: F-9\n---\n# Old\n\n## Diary\n\n**2026-04-04 — shadow entry.** x\n")
            self.assertEqual(docs_site.chronology(Path(d) / "ai_docs", {}), [])

    def test_marketing_research_spikes_are_read(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "mkt_docs/spikes/RESEARCH_demand.md", "# Research Spike: demand\n\n"
                  "## Answer / Outcome\n\n**2026-04-02 — demand exists.** x\n")
            got = docs_site.chronology(Path(d) / "mkt_docs", {})
            self.assertEqual([(e["date"], e["kind"], e["label"]) for e in got],
                             [("2026-04-02", "spike", "demand exists")])

    def test_a_label_with_markup_is_data_never_markup(self):          # T5
        with tempfile.TemporaryDirectory() as d:
            write(d, "ai_docs/README.md", "# X\n")
            write(d, "ai_docs/audit/project_notes.md",
                  "**2026-04-05 — <img src=x onerror=alert(1)></script>.** x\n")
            code, text = run(Path(d))
            self.assertEqual(code, 0, text)
            raw = (Path(d) / ".docs-site" / "data" / "core.js").read_text(encoding="utf-8")
            self.assertNotIn("</script", raw)
            self.assertNotIn("<img", raw)
            app = (PAGE_DIR / "app.js").read_text(encoding="utf-8")
            body = app[app.index("function eventList"):app.index("function pageHome")]
            self.assertNotIn("innerHTML", body)
            self.assertNotIn("html(", body)

    def test_every_event_kind_has_a_label_string(self):
        strings = (PAGE_DIR / "strings.js").read_text(encoding="utf-8")
        for e in self.core["chronology"]:
            self.assertIn("event_%s:" % e["kind"], strings)

    def test_an_empty_project_has_an_empty_chronology(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, "ai_docs/README.md", "# Empty\n")
            docs = Path(d) / "ai_docs"
            self.assertEqual(docs_site.chronology(docs, {}), [])


if __name__ == "__main__":
    unittest.main(verbosity=1)
