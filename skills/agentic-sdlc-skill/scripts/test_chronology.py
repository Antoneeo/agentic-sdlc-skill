#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-073 — dated entries, a one-step `next:`, and ids checked across refs.

Each acceptance criterion of ANALYSIS_doctrine_chronology.md is a test here, and
each names the mutation that turns it red: a test that cannot fail for the defect
it hunts proves nothing.

    python scripts/test_chronology.py

Standard library only. The git tests skip where git is absent; the mkt tests
skip in a distribution that does not ship `mkt_check.py`.
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_core as sc  # noqa: E402
import knowledge  # noqa: E402

try:
    import mkt_check  # noqa: E402
except ImportError:
    mkt_check = None

HAS_GIT = shutil.which("git") is not None
HERE = Path(__file__).resolve().parent
EPOCH = sc.CHRONOLOGY_EPOCH
BEFORE = "2026-01-01"


def setUpModule():
    # importing mkt_check flips the core's default docs root; pin ours (see
    # test_merge_safety.setUpModule for why discovery makes this necessary)
    global _SAVED_DOCS_DIR
    _SAVED_DOCS_DIR = sc.docs_dir()
    sc.set_docs_dir("ai_docs")


def tearDownModule():
    sc.set_docs_dir(_SAVED_DOCS_DIR)


def analysis(root, slug, diary, level="L3", start=EPOCH, status="PLANNED",
             fid="F-900", docs="ai_docs"):
    sol = Path(root) / docs / "solutions"
    sol.mkdir(parents=True, exist_ok=True)
    p = sol / f"ANALYSIS_{slug}.md"
    p.write_text(
        f"---\ndescription: x\nstatus: {status}\nid: {fid}\nstart_date: {start}\n"
        f"end_date:\nlevel: {level}\n---\n# Feature Analysis: {slug}\n\n"
        f"## Objective\n\nx\n\n## Diary / Current State\n\n{diary}\n",
        encoding="utf-8")
    return p


def handoff(root, slug, nxt, level="L3", updated=EPOCH, docs="ai_docs"):
    aud = Path(root) / docs / "audit"
    aud.mkdir(parents=True, exist_ok=True)
    p = aud / f"HANDOFF_{slug}.md"
    p.write_text(
        f"---\nworkstream: {slug}\nlevel: {level}\nbranch: main\nstatus: PROGRESS\n"
        f"since: {updated}\nnext: {nxt}\ndetails: x\nupdated: {updated}\n---\n\nx\n",
        encoding="utf-8")
    return p


def quiet(fn, *a, **kw):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = fn(*a, **kw)
    return rc, buf.getvalue()


# ------------------------------------------------------------- criterion 1

class Openers(unittest.TestCase):
    """Mutation: drop the block rule from `entry_openers` -> the hard-wrapped
    cases read as events and `test_continuations_are_not_openers` fails."""

    FORMS = {
        "**2026-08-02 — opened.** Standalone, devPNT off.": ("2026-08-02", "opened"),
        "2026-09-26: la prima Vision ha avuto blind review PASS. Il resto.":
            ("2026-09-26", "la prima Vision ha avuto blind review PASS"),
        "- 2026-06-13: Analisi avviata. Decisione: integrare.": ("2026-06-13", "Analisi avviata"),
        "- **2026-07-28** — opened. devPNT off.": ("2026-07-28", "opened"),
        "### 2026-10-01 — round 2": ("2026-10-01", "round 2"),
        "2026-10-02 release closure: four packages": ("2026-10-02", "release closure: four packages"),
    }

    def test_every_corpus_form_is_read_with_its_date_and_label(self):
        for line, want in self.FORMS.items():
            got = sc.entry_openers(line)
            self.assertTrue(got, line)
            self.assertEqual(got[0][:2], want, line)
            self.assertEqual(got[0][2], 1)

    def test_continuations_are_not_openers(self):
        for body in (
            "**Round 3 (the cap) — FAIL; the v4 above disposes every finding.**",
            "**Owner note, 2026-08-02 — the skill is made to be used by an agent.**",
            "The release of 2026-10-17 shipped four packages.",
            "  - 2026-08-03: an indented bullet inside an entry",
            "a hard-wrapped prose line ends here and the next one begins with\n"
            "2026-08-01 — a date, mid-paragraph",
            'the owner said ("vai",\n2026-08-01) with the fixes incorporated',
            "**2026-08-01x** not a date boundary",
        ):
            self.assertEqual(sc.entry_openers(body), [], body)

    def test_line_numbers_are_one_based_within_the_body(self):
        body = "**2026-08-01 — a.** x\n\n**2026-08-02 — b.** y\n"
        self.assertEqual([o[2] for o in sc.entry_openers(body)], [1, 3])

    def test_label_is_capped(self):
        got = sc.entry_openers("**2026-08-01 — " + "w" * 300 + ".** x")
        self.assertEqual(len(got[0][1]), 120)

    def test_a_crafted_line_is_read_fast(self):          # T1
        line = "2026-08-01 " + "a" * 100_000
        t0 = time.perf_counter()
        sc.entry_openers(line)
        sc.entry_openers("- **" + "*" * 100_000)
        self.assertLess(time.perf_counter() - t0, 0.05)


# ------------------------------------------------------------- criterion 2

class NoNewFindingAtRest(unittest.TestCase):
    """Mutation: remove the epoch gate -> the pre-epoch fixture is flagged."""

    def test_golden_corpus_yields_no_chronology_advisory(self):
        corpora = sorted((HERE / "fixtures").glob("golden_*_docs"))
        if not corpora:
            self.skipTest("this distribution ships no golden corpus")
        for corpus in corpora:                    # golden_ai_docs / golden_mkt_docs
            docs = corpus.name[len("golden_"):]
            with tempfile.TemporaryDirectory() as d:
                shutil.copytree(corpus, Path(d) / docs)
                sc.set_docs_dir(docs)
                try:
                    self.assertEqual(sc.chronology_advisories(Path(d)), [], corpus.name)
                finally:
                    sc.set_docs_dir("ai_docs")

    def test_an_analysis_started_before_the_epoch_is_never_checked(self):
        with tempfile.TemporaryDirectory() as d:
            analysis(d, "old", "Current state: undated.\n\n### Stato corrente\nx",
                     start=BEFORE)
            handoff(d, "old", "x" * 400, updated=BEFORE)
            self.assertEqual(sc.chronology_advisories(Path(d)), [])


# ------------------------------------------------------------- criterion 3

class A1UndatedDiary(unittest.TestCase):
    """Mutation: drop the level gate -> the L2 fixture is flagged."""

    def test_an_undated_preface_is_named_with_its_line(self):
        with tempfile.TemporaryDirectory() as d:
            analysis(d, "x", "<!-- template comment -->\nCurrent state: half done.\n\n"
                             "**2026-10-20 — opened.** x")
            adv = sc.chronology_advisories(Path(d))
            self.assertEqual(len(adv), 1, adv)
            # the FILE line (heading 15, blank, comment, then the text) and the text
            self.assertIn("solutions/ANALYSIS_x.md: line 18: Diary text 'Current state", adv[0])
            self.assertIn("comes before the first dated entry", adv[0])

    def test_an_undated_h3_heading_is_named(self):
        with tempfile.TemporaryDirectory() as d:
            analysis(d, "x", "**2026-10-20 — opened.** x\n\n### Stato corrente\nstuff")
            adv = sc.chronology_advisories(Path(d))
            self.assertEqual(len(adv), 1, adv)
            self.assertIn("line 19: Diary heading '### Stato corrente' is not a dated entry",
                          adv[0])

    def test_h4_substructure_under_a_dated_entry_is_legal(self):
        with tempfile.TemporaryDirectory() as d:
            analysis(d, "x", "### 2026-10-20 — sub-design\n\n#### Objective\nx")
            self.assertEqual(sc.chronology_advisories(Path(d)), [])

    def test_l2_and_pre_epoch_get_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            analysis(d, "a", "undated", level="L2")
            analysis(d, "b", "undated", start="2026-10-17", fid="F-901")
            self.assertEqual(sc.chronology_advisories(Path(d)), [])

    def test_an_entry_under_the_template_comment_is_an_event_to_both_readers(self):
        # review F1: the validator and the event reader must tokenise alike
        body = "<!-- One dated entry...\n     more -->\n**2026-10-20 — opened.** x"
        self.assertEqual(sc.undated_diary_lines(body), [])
        self.assertEqual([o[:2] for o in sc.entry_openers(body)], [("2026-10-20", "opened")])

    def test_an_indented_first_diary_line_is_not_an_opener(self):
        # review F5: a stripped body moved `  - DATE` to column 0
        head, body = sc.section_lines("x\n## Diary\n  - 2026-10-20: indented\n",
                                      sc.DIARY_SECTION)
        self.assertEqual(head, 2)
        self.assertEqual(sc.entry_openers(body), [])

    def test_undated_diary_lines_is_the_shared_reader(self):
        lines = sc.undated_diary_lines("pre\n\n**2026-10-20 — a.** x\n\n### b\n#### c")
        self.assertEqual(lines, [(1, "pre"), (5, "### b")])


# ------------------------------------------------------------- criterion 4

class A2NextIsOneStep(unittest.TestCase):
    """Mutations: drop the length cap -> no finding; drop the mkt guard -> the
    advisory prints twice on an ai_docs root."""

    LONG = "y" * (sc.NEXT_MAX_CHARS + 1)

    def test_a_long_next_is_flagged_once(self):
        with tempfile.TemporaryDirectory() as d:
            handoff(d, "w", self.LONG)
            adv = sc.chronology_advisories(Path(d))
            self.assertEqual(len(adv), 1, adv)
            self.assertIn(f"audit/HANDOFF_w.md: next: is {len(self.LONG)} chars (> 240)", adv[0])

    def test_at_the_cap_and_l2_and_pre_epoch_get_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            handoff(d, "a", "y" * sc.NEXT_MAX_CHARS)
            handoff(d, "b", self.LONG, level="L2")
            handoff(d, "c", self.LONG, updated=BEFORE)
            self.assertEqual(sc.chronology_advisories(Path(d)), [])

    def _registry(self, d):
        rc, _ = quiet(sc.cmd_index, Path(d))
        return rc

    @staticmethod
    def _vision(d, docs="ai_docs"):
        # an APPROVED vision, so --strict has no unrelated warning to fail on
        v = Path(d) / docs / "vision"
        v.mkdir(parents=True, exist_ok=True)
        for name in sc.VISION_FILES:
            (v / name).write_text("# V\n\nStatus: APPROVED\n", encoding="utf-8")

    def test_spine_validate_strict_stays_green(self):    # T2
        with tempfile.TemporaryDirectory() as d:
            self._vision(d)
            handoff(d, "w", self.LONG)
            self._registry(d)
            for cmd in ("validate", "check"):
                rc, out = quiet(sc.main, [cmd, "--root", d, "--strict"])
                self.assertEqual(out.count("next: is"), 1, out)
                self.assertFalse([l for l in out.splitlines()
                                  if "next: is" in l and "warn" in l.lower()], out)
                if cmd == "validate":            # check also runs stale, no audit plan here
                    self.assertEqual(rc, 0, out)

    @unittest.skipIf(mkt_check is None, "mkt_check.py ships only with the marketing lens")
    def test_mkt_prints_it_once_on_both_roots_and_strict_stays_green(self):  # T6, T10
        for docs in ("mkt_docs", "ai_docs"):
            with tempfile.TemporaryDirectory() as d:
                if docs == "ai_docs":
                    self._vision(d)
                handoff(d, "w", self.LONG, docs=docs)
                quiet(mkt_check.main, ["index", "--root", d, "--docs-dir", docs])
                rcs = {}
                for cmd in ("validate", "check"):
                    rc, out = quiet(mkt_check.main, [cmd, "--root", d, "--docs-dir", docs,
                                                     "--strict"])
                    self.assertEqual(out.count("next: is"), 1, (docs, cmd, out))
                    self.assertFalse([l for l in out.splitlines()
                                      if "next: is" in l and "warn" in l.lower()], out)
                    rcs[cmd] = (rc, out)
                # the advisory never reaches the exit code: same rc without it
                (Path(d) / docs / "audit" / "HANDOFF_w.md").unlink()
                quiet(mkt_check.main, ["index", "--root", d, "--docs-dir", docs])
                rc0, out0 = quiet(mkt_check.main, ["validate", "--root", d, "--docs-dir",
                                                   docs, "--strict"])
                self.assertEqual(rcs["validate"][0], rc0, (docs, rcs["validate"][1], out0))
            sc.set_docs_dir("ai_docs")


# ------------------------------------------------------------- criterion 5

class RequestEntries(unittest.TestCase):
    """Mutation: drop the unparsed list -> the malformed heading vanishes."""

    def test_every_heading_of_this_repository_parses(self):
        req = HERE.parents[2] / "ai_docs" / "audit" / "requests"
        if not req.is_dir():
            self.skipTest("the repository's own request records are not packaged")
        n = 0
        for p in req.glob("REQUEST_*.md"):
            entries, unparsed = sc.request_entries(sc.read_text(p))
            self.assertEqual(unparsed, [], p.name)
            n += len(entries)
        self.assertGreater(n, 30)

    def test_a_malformed_heading_is_named_never_dropped(self):
        text = ("# Request record\n\n### R1 — 2026-10-01 — opening request\n> x\n\n"
                "### R4-nota — 2026-10-01 — x\n> y\n")
        entries, unparsed = sc.request_entries(text)
        self.assertEqual(entries, [("R1", "2026-10-01", "opening request", 3)])
        self.assertEqual(unparsed, [(6, "### R4-nota — 2026-10-01 — x")])


class OtherReaders(unittest.TestCase):

    def test_adr_date_reads_the_body_then_the_name(self):
        self.assertEqual(sc.adr_date("ADR_2026-01-02_x.md", "# ADR\n\n**Date:** 2026-03-04\n"),
                         "2026-03-04")
        self.assertEqual(sc.adr_date("ADR_2026-01-02_x.md", "# ADR\n"), "2026-01-02")
        self.assertIsNone(sc.adr_date("adr_x.md", "# ADR\n"))

    def test_frontmatter_date(self):
        self.assertEqual(knowledge.frontmatter_date({"date": "'2026-08-01'"}), "2026-08-01")
        self.assertEqual(knowledge.frontmatter_date({"date": "2026-08-01T10:00"}), "2026-08-01")
        self.assertIsNone(knowledge.frontmatter_date({"date": "2026-13-40"}))
        self.assertIsNone(knowledge.frontmatter_date({}))


# ------------------------------------------------------------- criterion 6

def git(cwd, *args):
    r = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)
    return r.stdout


def request(root, slug, fid, analysis_name):
    req = Path(root) / "ai_docs" / "audit" / "requests"
    req.mkdir(parents=True, exist_ok=True)
    (req / f"REQUEST_{slug}.md").write_text(
        f"---\nunit: {fid} — {slug}\nanalysis: {analysis_name}\n---\n# Request record\n",
        encoding="utf-8")


@unittest.skipUnless(HAS_GIT, "git not available")
class A3IdsOnOtherRefs(unittest.TestCase):
    """Mutation: do not consult the other refs -> the collision disappears."""

    def _repo(self, d):
        git(d, "init", "-q", "-b", "main")
        git(d, "config", "user.email", "t@t")
        git(d, "config", "user.name", "t")
        git(d, "config", "core.autocrlf", "false")
        (Path(d) / "README").write_text("x\n", encoding="utf-8")
        git(d, "add", "-A")
        git(d, "commit", "-qm", "base")

    def _other_branch(self, d, slug, fid="F-900"):
        git(d, "checkout", "-qb", "other")
        analysis(d, slug, "**2026-10-20 — opened.** x", fid=fid)
        git(d, "add", "-A")
        git(d, "commit", "-qm", "other")
        git(d, "checkout", "-q", "main")

    def test_one_id_for_two_analyses_is_named_once(self):
        with tempfile.TemporaryDirectory() as d:
            self._repo(d)
            self._other_branch(d, "theirs")
            analysis(d, "mine", "**2026-10-20 — opened.** x")
            hits = sc.ids_on_other_refs(Path(d))
            self.assertEqual(hits, [("F-900", "ANALYSIS_mine.md", "ANALYSIS_theirs.md", ["other"])])
            msgs = sc.id_advisories(Path(d))
            self.assertEqual(len(msgs), 1)
            self.assertIn("same unit under its old name", msgs[0])
            rc, out = quiet(sc.main, ["check", "--root", d])
            self.assertEqual(out.count("is also used by ANALYSIS_theirs.md"), 1, out)

    def test_a_rename_prints_the_clause(self):
        with tempfile.TemporaryDirectory() as d:
            self._repo(d)
            self._other_branch(d, "old_name")
            analysis(d, "new_name", "**2026-10-20 — opened.** x")
            msgs = sc.id_advisories(Path(d))
            self.assertEqual(len(msgs), 1)
            self.assertIn("ANALYSIS_old_name.md", msgs[0])
            self.assertIn("same unit under its old name", msgs[0])

    def test_silent_without_the_other_branch(self):
        with tempfile.TemporaryDirectory() as d:
            self._repo(d)
            analysis(d, "mine", "x")
            self.assertEqual(sc.ids_on_other_refs(Path(d)), [])

    def test_silent_when_the_only_open_unit_is_l2(self):
        with tempfile.TemporaryDirectory() as d:
            self._repo(d)
            self._other_branch(d, "theirs")
            analysis(d, "mine", "x", level="L2")
            self.assertEqual(sc.ids_on_other_refs(Path(d)), [])

    def test_silent_for_the_request_record_of_a_completed_unit(self):
        with tempfile.TemporaryDirectory() as d:
            self._repo(d)
            self._other_branch(d, "theirs")
            analysis(d, "mine", "x", status="COMPLETED")
            request(d, "mine", "F-900", "ANALYSIS_mine.md")
            self.assertEqual(sc.ids_on_other_refs(Path(d)), [])

    def test_an_open_request_record_counts_before_its_analysis_exists(self):
        with tempfile.TemporaryDirectory() as d:
            self._repo(d)
            self._other_branch(d, "theirs")
            request(d, "mine", "F-900", "ANALYSIS_mine.md")
            hits = sc.ids_on_other_refs(Path(d))
            self.assertEqual([h[:3] for h in hits],
                             [("F-900", "ANALYSIS_mine.md", "ANALYSIS_theirs.md")])

    def test_a_docs_root_in_a_subdirectory_is_scanned(self):
        # review F2: pathspecs are relative to the project root, not the repo top
        with tempfile.TemporaryDirectory() as d:
            self._repo(d)
            sub = Path(d) / "proj"
            git(d, "checkout", "-qb", "other")
            analysis(sub, "theirs", "x")
            git(d, "add", "-A")
            git(d, "commit", "-qm", "other")
            git(d, "checkout", "-q", "main")
            analysis(sub, "mine", "x")
            self.assertEqual([h[:3] for h in sc.ids_on_other_refs(sub)],
                             [("F-900", "ANALYSIS_mine.md", "ANALYSIS_theirs.md")])

    def test_a_non_ascii_name_is_not_its_own_collision(self):
        # review F3: git's quotePath C-quotes the name unless turned off
        with tempfile.TemporaryDirectory() as d:
            self._repo(d)
            analysis(d, "caff\u00e8", "x")
            git(d, "add", "-A")
            git(d, "commit", "-qm", "mine")
            git(d, "branch", "other")
            (Path(d) / "README").write_text("y\n", encoding="utf-8")
            git(d, "commit", "-qam", "move HEAD")
            self.assertEqual(sc.ids_on_other_refs(Path(d)), [])

    def test_an_id_line_in_the_body_is_not_a_declaration(self):
        # review F4: hits outside the frontmatter fence are ignored
        with tempfile.TemporaryDirectory() as d:
            self._repo(d)
            git(d, "checkout", "-qb", "other")
            sol = Path(d) / "ai_docs" / "solutions"
            sol.mkdir(parents=True)
            (sol / "ANALYSIS_t.md").write_text(
                "---\nstatus: PLANNED\n---\n# T\n\n```\nid: F-900\n```\n", encoding="utf-8")
            git(d, "add", "-A")
            git(d, "commit", "-qm", "other")
            git(d, "checkout", "-q", "main")
            analysis(d, "mine", "x")
            self.assertEqual(sc.ids_on_other_refs(Path(d)), [])

    def test_batches_cross_refs_and_a_blob_tag_is_skipped(self):  # round-2 N2, N3
        import unittest.mock as um
        with tempfile.TemporaryDirectory() as d:
            self._repo(d)
            self._other_branch(d, "theirs")
            git(d, "branch", "other2", "other")
            blob = git(d, "hash-object", "-w", "README").strip()
            git(d, "tag", "blobtag", blob)
            analysis(d, "mine", "x")
            with um.patch.object(sc, "ID_SCAN_REFS_PER_CALL", 1):
                hits = sc.ids_on_other_refs(Path(d))
            self.assertEqual(hits, [("F-900", "ANALYSIS_mine.md", "ANALYSIS_theirs.md",
                                     ["other", "other2"])])

    def test_above_the_ref_cap_it_says_it_did_not_run(self):     # T9
        with tempfile.TemporaryDirectory() as d:
            self._repo(d)
            self._other_branch(d, "theirs")
            analysis(d, "mine", "x")
            self.assertIsNone(sc.ids_on_other_refs(Path(d), max_refs=0))

    def test_a_failing_grep_is_a_skip_not_a_clean_result(self):   # review F8
        import unittest.mock as um
        with tempfile.TemporaryDirectory() as d:
            self._repo(d)
            self._other_branch(d, "theirs")
            analysis(d, "mine", "x")
            real = subprocess.run

            def failing(args, *a, **kw):
                if "grep" in args:
                    return subprocess.CompletedProcess(args, 128, "", "fatal")
                return real(args, *a, **kw)
            with um.patch.object(sc.subprocess, "run", failing):
                self.assertIsNone(sc.ids_on_other_refs(Path(d)))

    def test_a_skipped_scan_is_said_never_reported_clean(self):  # T9, review F8
        import unittest.mock as um
        with tempfile.TemporaryDirectory() as d:
            analysis(d, "mine", "x")
            with um.patch.object(sc, "ids_on_other_refs", lambda root: None):
                msgs = sc.id_advisories(Path(d))
            self.assertEqual(len(msgs), 1)
            self.assertIn("id check skipped", msgs[0])

    def test_git_runs_with_fixed_arguments_and_no_shell(self):   # T8
        import unittest.mock as um
        with tempfile.TemporaryDirectory() as d:
            self._repo(d)
            self._other_branch(d, "theirs")
            request(d, "mine", "F-900", "ANALYSIS_mine; rm -rf x.md")
            real = subprocess.run
            calls = []

            def spy(*a, **kw):
                calls.append((a, kw))
                return real(*a, **kw)
            with um.patch.object(sc.subprocess, "run", spy):
                hits = sc.ids_on_other_refs(Path(d))
            self.assertTrue(hits)
            self.assertTrue(calls)
            for a, kw in calls:
                self.assertIsInstance(a[0], list)
                self.assertFalse(kw.get("shell"))
                self.assertFalse(any("rm -rf" in str(x) for x in a[0]))

    @unittest.skipIf(mkt_check is None, "mkt_check.py ships only with the marketing lens")
    def test_mkt_check_names_it_once_on_both_roots(self):
        for docs in ("mkt_docs", "ai_docs"):
            with tempfile.TemporaryDirectory() as d:
                sc.set_docs_dir(docs)
                self._repo(d)
                git(d, "checkout", "-qb", "other")
                analysis(d, "theirs", "x", docs=docs)
                git(d, "add", "-A")
                git(d, "commit", "-qm", "other")
                git(d, "checkout", "-q", "main")
                analysis(d, "mine", "x", docs=docs)
                rc, out = quiet(mkt_check.main, ["check", "--root", d, "--docs-dir", docs])
                self.assertEqual(out.count("is also used by ANALYSIS_theirs.md"), 1,
                                 (docs, out))
            sc.set_docs_dir("ai_docs")


class A3WithoutGit(unittest.TestCase):

    def test_silent_outside_a_repository(self):
        with tempfile.TemporaryDirectory() as d:
            analysis(d, "mine", "x")
            self.assertEqual(sc.ids_on_other_refs(Path(d)), [])


if __name__ == "__main__":
    unittest.main()
