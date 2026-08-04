#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-028 — the workstream registry survives concurrent work.

`templates.md` claimed "Parallel-safe by construction" from F-019 until this
battery existed, and the claim was false: two workstreams opened from one base
conflicted twice in one file. A claim about merge behaviour that nothing
exercises is a claim that will be wrong.

Standard library only. The git tests skip where git is absent — the mechanism
itself is files and a generator, and must work with no VCS at all.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_core as sc  # noqa: E402

HAS_GIT = shutil.which("git") is not None


def setUpModule():
    """Pin the docs root for this battery's fixtures.

    unittest DISCOVERY imports every test module before any test runs, and
    importing an overlay entry point (mkt_check) flips the core's default docs
    root to `mkt_docs`. This battery builds `ai_docs` fixtures, so it says which
    root it means instead of inheriting whichever module got imported first --
    the same pinning test_skill_invariants already does."""
    global _SAVED_DOCS_DIR
    _SAVED_DOCS_DIR = sc.docs_dir()
    sc.set_docs_dir("ai_docs")


def tearDownModule():
    sc.set_docs_dir(_SAVED_DOCS_DIR)


def source(root, slug, workstream, updated="2026-06-11", **kw):
    """Write one HANDOFF_[feature].md source and return its path."""
    aud = root / "ai_docs" / "audit"
    aud.mkdir(parents=True, exist_ok=True)
    meta = {"workstream": workstream, "level": "L3", "branch": "main",
            "status": "PROGRESS", "since": "2026-06-01",
            "next": "keep going", "updated": updated}
    meta.update(kw)
    body = "".join(f"{k}: {v}\n" for k, v in meta.items())
    p = aud / f"HANDOFF_{slug}.md"
    p.write_text(f"---\n{body}---\n\n## Resume state\n\nnothing volatile\n",
                 encoding="utf-8")
    return p


def regenerate(root):
    (root / "ai_docs" / "audit" / "handoff.md").write_text(
        sc.build_registry(root), encoding="utf-8")


class MS_Generator(unittest.TestCase):
    """The four facts the design review pinned. Each is a way the alignment
    check — a byte comparison — becomes the defect instead of the guard."""

    def test_date_is_the_newest_frontmatter_value_never_an_mtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source(root, "a", "F-001 alpha", updated="2026-06-02")
            source(root, "b", "F-002 beta", updated="2026-06-20")
            first = sc.build_registry(root)
            self.assertIn("Date: 2026-06-20 (UTC)", first)
            # git does not preserve mtimes: a fresh clone touches every file.
            later = time.time() + 10_000
            for p in (root / "ai_docs" / "audit").glob("HANDOFF_*.md"):
                os.utime(p, (later, later))
            self.assertEqual(sc.build_registry(root), first,
                             "the header must not move when only mtimes do")

    def test_rows_are_ordered_by_workstream_not_by_file_name(self):
        """Sorted by the id the reader sees. The file names here are in the
        opposite order on purpose: a glob sort would pass an order test that
        never disagreed with it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source(root, "zeta", "F-001 alpha")
            source(root, "alpha", "F-002 zeta")
            out = sc.build_registry(root)
            self.assertLess(out.index("F-001 alpha"), out.index("F-002 zeta"))

    def test_the_same_tree_always_builds_the_same_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "a"
            source(a, "z", "F-001 alpha")
            source(a, "m", "F-002 beta")
            b = Path(tmp) / "b"
            source(b, "m", "F-002 beta")
            source(b, "z", "F-001 alpha")
            self.assertEqual(sc.build_registry(a), sc.build_registry(b))

    def test_every_row_carries_its_source_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source(root, "sso", "F-001 SSO login", details="ANALYSIS_sso.md")
            out = sc.build_registry(root)
            self.assertIn("HANDOFF_sso.md · ANALYSIS_sso.md", out)
            self.assertIn("| F-001 SSO login | L3 |", out)

    def test_project_notes_have_their_own_source(self):
        """The registry is two things: per-workstream rows and project-global
        notes. Generating the file without a home for the notes deletes them."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source(root, "a", "F-001 alpha")
            (root / "ai_docs" / "audit" / sc.PROJECT_NOTES).write_text(
                "Repo is CRLF. Release pending.\n", encoding="utf-8")
            out = sc.build_registry(root)
            self.assertIn("## Project-wide notes", out)
            self.assertIn("Repo is CRLF.", out)

    def test_handoff_md_is_never_collected_as_a_source(self):
        """T5, run on the case-insensitive development filesystem: the glob
        requires the underscore, so the generated view cannot feed itself."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source(root, "a", "F-001 alpha")
            regenerate(root)
            names = [p.name for p, _m in sc.list_workstreams(root)]
            self.assertEqual(names, ["HANDOFF_a.md"])

    def test_a_volatile_only_handoff_file_is_not_a_source(self):
        """Opt-in by `workstream:`: the pre-conversion file still works as the
        volatile-logistics note it always was."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            aud = root / "ai_docs" / "audit"
            aud.mkdir(parents=True)
            (aud / "HANDOFF_old.md").write_text(
                "# HANDOFF: old\nBranch: feature/x\n\n## Next command\nrun it\n",
                encoding="utf-8")
            self.assertEqual(sc.list_workstreams(root), [])
            self.assertEqual(sc.build_registry(root), "")


class MS_Conversion(unittest.TestCase):
    """T6/T8 — no installed project is broken, and none is half-converted."""

    def test_a_project_with_no_sources_is_left_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            aud = root / "ai_docs" / "audit"
            aud.mkdir(parents=True)
            hand = aud / "handoff.md"
            hand.write_text("# Handoff — workstream registry\nDate: 2026-06-01 (UTC)\n\n"
                            "| Workstream | Level |\n|---|---|\n| F-001 | L3 |\n",
                            encoding="utf-8")
            before = hand.read_text(encoding="utf-8")
            self.assertEqual(sc.rc_registry(root), 0)
            self.assertEqual(hand.read_text(encoding="utf-8"), before)

    def test_index_refuses_while_a_row_has_no_source(self):
        """The mixed state: one converted row, four still hand-written.
        Regenerating here would delete the four, silently."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source(root, "a", "F-001 alpha")
            hand = root / "ai_docs" / "audit" / "handoff.md"
            hand.write_text("# Handoff — workstream registry\nDate: 2026-06-01 (UTC)\n\n"
                            "| Workstream | Level |\n|---|---|\n"
                            "| F-001 alpha | L3 |\n| F-002 beta | L3 |\n",
                            encoding="utf-8")
            before = hand.read_text(encoding="utf-8")
            blockers = sc.registry_conversion_blockers(root)
            self.assertTrue(any("F-002 beta" in b for b in blockers), blockers)
            self.assertEqual(sc.rc_registry(root), 1)
            self.assertEqual(hand.read_text(encoding="utf-8"), before,
                             "a refusal that still writes is not a refusal")

    def test_a_legacy_narrative_handoff_is_not_overwritten(self):
        """A pre-1.17 handoff has no table at all, so orphan rows alone would
        not notice it — and its whole content would be lost on the first write."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source(root, "a", "F-001 alpha")
            hand = root / "ai_docs" / "audit" / "handoff.md"
            hand.write_text("# Handoff\nDate: 2026-06-01 (UTC)\n\n"
                            "## Active features\n- F-009: half done\n\n"
                            "## Next step\nfinish it\n", encoding="utf-8")
            before = hand.read_text(encoding="utf-8")
            self.assertEqual(sc.rc_registry(root), 1)
            self.assertEqual(hand.read_text(encoding="utf-8"), before)

    def test_a_fully_converted_registry_regenerates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source(root, "a", "F-001 alpha")
            hand = root / "ai_docs" / "audit" / "handoff.md"
            hand.write_text("# Handoff — workstream registry\nDate: 2026-06-01 (UTC)\n\n"
                            "| Workstream | Level |\n|---|---|\n| F-001 alpha | L3 |\n",
                            encoding="utf-8")
            self.assertEqual(sc.registry_conversion_blockers(root), [])
            self.assertEqual(sc.rc_registry(root), 0)
            self.assertIn(f"GENERATED by {sc.entry_script()} index",
                          hand.read_text(encoding="utf-8"))

    def test_a_generated_registry_is_ours_to_rewrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source(root, "a", "F-001 alpha")
            regenerate(root)
            source(root, "b", "F-002 beta")
            self.assertEqual(sc.registry_conversion_blockers(root), [])
            self.assertEqual(sc.rc_registry(root), 0)
            self.assertIn("F-002 beta",
                          (root / "ai_docs" / "audit" / "handoff.md").read_text(
                              encoding="utf-8"))

    def test_the_cap_warns_and_never_truncates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for i in range(sc.REGISTRY_CAP + 2):
                source(root, f"w{i:02d}", f"F-{i:03d} feature")
            out = sc.build_registry(root)
            for i in range(sc.REGISTRY_CAP + 2):
                self.assertIn(f"F-{i:03d} feature", out,
                              "a truncated registry loses the state it exists to keep")


class MS_Alignment(unittest.TestCase):
    """A merge resolved by hand, or a generated file edited by hand, must be
    visible — that is what turns a bad resolution from permanent into loud."""

    def _validate(self, root):
        from io import StringIO
        buf, saved = StringIO(), sys.stdout
        sys.stdout = buf
        try:
            rc = sc.cmd_validate(root)
        finally:
            sys.stdout = saved
        return rc, buf.getvalue()

    def test_a_hand_edited_registry_errors_and_index_clears_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ai_docs" / "solutions").mkdir(parents=True)
            source(root, "a", "F-001 alpha")
            regenerate(root)
            rc, out = self._validate(root)
            self.assertNotIn("handoff.md not aligned", out)

            hand = root / "ai_docs" / "audit" / "handoff.md"
            hand.write_text(hand.read_text(encoding="utf-8").replace(
                "keep going", "someone edited this by hand"), encoding="utf-8")
            rc, out = self._validate(root)
            self.assertIn("handoff.md not aligned", out)
            self.assertEqual(rc, 1)

            self.assertEqual(sc.rc_registry(root), 0)
            rc, out = self._validate(root)
            self.assertNotIn("handoff.md not aligned", out)

    def test_sources_with_no_registry_at_all_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ai_docs" / "solutions").mkdir(parents=True)
            source(root, "a", "F-001 alpha")
            rc, out = self._validate(root)
            self.assertIn("handoff.md missing while HANDOFF_*.md sources exist", out)

    def test_two_files_claiming_one_workstream_are_reported(self):
        """The collision the design does NOT fix: two people opening the same
        work under two file names. It must not pass as two ordinary rows."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ai_docs" / "solutions").mkdir(parents=True)
            source(root, "a", "F-001 alpha")
            source(root, "a_too", "F-001 alpha")
            regenerate(root)
            _rc, out = self._validate(root)
            self.assertIn("both claim workstream", out, out)

    def test_a_project_without_sources_sees_no_new_finding(self):
        """T6, the regression that protects every installed project."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ai_docs" / "solutions").mkdir(parents=True)
            aud = root / "ai_docs" / "audit"
            aud.mkdir(parents=True)
            (aud / "handoff.md").write_text(
                "# Handoff\nDate: %s (UTC)\n\n| Workstream |\n|---|\n| F-001 |\n"
                % time.strftime("%Y-%m-%d"), encoding="utf-8")
            _rc, out = self._validate(root)
            self.assertNotIn("handoff.md", out.replace(
                "audit/handoff.md without", ""), out)


def git(cwd, *args, check=True):
    r = subprocess.run(["git"] + list(args), cwd=str(cwd), capture_output=True,
                       text=True)
    if check and r.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {r.stderr}")
    return r


def conflicted(cwd):
    return [ln for ln in git(cwd, "diff", "--name-only", "--diff-filter=U",
                             check=False).stdout.splitlines() if ln.strip()]


@unittest.skipUnless(HAS_GIT, "git not available")
class MS_Merge(unittest.TestCase):
    """The experiment that found the defect, kept as a regression test."""

    def _repo(self, tmp):
        root = Path(tmp) / "repo"
        (root / "ai_docs" / "audit").mkdir(parents=True)
        git(root.parent, "init", "-q", "repo")
        git(root, "config", "user.email", "t@example.com")
        git(root, "config", "user.name", "T")
        git(root, "config", "commit.gpgsign", "false")
        return root

    def _commit(self, root, msg):
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", msg)

    def test_two_workstreams_from_one_base_never_conflict_in_their_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            source(root, "base", "F-000 base")
            regenerate(root)
            self._commit(root, "base")
            base = git(root, "rev-parse", "HEAD").stdout.strip()

            git(root, "checkout", "-q", "-b", "wa")
            source(root, "alpha", "F-001 alpha", updated="2026-06-12")
            regenerate(root)
            self._commit(root, "open alpha")

            git(root, "checkout", "-q", base)
            git(root, "checkout", "-q", "-b", "wb")
            source(root, "beta", "F-002 beta", updated="2026-06-13")
            regenerate(root)
            self._commit(root, "open beta")

            git(root, "merge", "--no-edit", "wa", check=False)
            paths = conflicted(root)
            self.assertNotIn("ai_docs/audit/HANDOFF_alpha.md", paths)
            self.assertNotIn("ai_docs/audit/HANDOFF_beta.md", paths)
            self.assertTrue(set(paths) <= {"ai_docs/audit/handoff.md"},
                            f"only the GENERATED view may conflict, got {paths}")
            # ...and it is resolved mechanically, with no state lost.
            self.assertEqual(sc.rc_registry(root), 0)
            out = (root / "ai_docs" / "audit" / "handoff.md").read_text(encoding="utf-8")
            for w in ("F-000 base", "F-001 alpha", "F-002 beta"):
                self.assertIn(w, out)
            self.assertNotIn("<<<<<<<", out)

    def test_the_shared_table_is_what_conflicted(self):
        """Mutation of the fixture, not of the product: two writers editing the
        one table by hand is the shape F-019 shipped. A guard that cannot show
        the defect it prevents is decoration."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            hand = root / "ai_docs" / "audit" / "handoff.md"
            hand.write_text("# Handoff\nDate: 2026-06-01 (UTC)\n\n"
                            "| Workstream | Next step |\n|---|---|\n"
                            "| F-000 base | go |\n", encoding="utf-8")
            self._commit(root, "base")
            base = git(root, "rev-parse", "HEAD").stdout.strip()

            git(root, "checkout", "-q", "-b", "wa")
            hand.write_text("# Handoff\nDate: 2026-06-12 (UTC)\n\n"
                            "| Workstream | Next step |\n|---|---|\n"
                            "| F-000 base | go |\n| F-001 alpha | wire it |\n",
                            encoding="utf-8")
            self._commit(root, "alpha row")

            git(root, "checkout", "-q", base)
            git(root, "checkout", "-q", "-b", "wb")
            hand.write_text("# Handoff\nDate: 2026-06-13 (UTC)\n\n"
                            "| Workstream | Next step |\n|---|---|\n"
                            "| F-000 base | go |\n| F-002 beta | ship it |\n",
                            encoding="utf-8")
            self._commit(root, "beta row")

            git(root, "merge", "--no-edit", "wa", check=False)
            self.assertIn("ai_docs/audit/handoff.md", conflicted(root),
                          "the observed defect must still be observable")
            self.assertIn("<<<<<<<", hand.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
