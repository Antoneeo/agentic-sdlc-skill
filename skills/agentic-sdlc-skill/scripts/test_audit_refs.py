#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-056 -- `stale` never reports an area fresh when it cannot evaluate it.

The defect this battery keeps fixed: `mark` records HEAD, the user amends the
rewritten audit_plan.md into that very commit, and the recorded reference
survives only in the reflog. Once git pruned it, `stale` printed a warning, then
`[ok]`, and returned 0 -- three analyzed areas silently fell out of staleness.
The same "cannot evaluate = fresh" rule lived on every path a reference can fail
on: squash-merged away, beyond a shallow clone, git unavailable, unparseable.

Standard library only. The tests that need git skip where it is absent. Clones use
`file://`: a plain-path clone hardlinks every object, unreachable ones included,
and would hide the squash case.
"""
import contextlib
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_core as sc  # noqa: E402

HAS_GIT = shutil.which("git") is not None


def setUpModule():
    """Pin the docs root: importing an overlay entry point during discovery can
    flip the core's default (see test_merge_safety)."""
    global _SAVED_DOCS_DIR
    _SAVED_DOCS_DIR = sc.docs_dir()
    sc.set_docs_dir("ai_docs")


def tearDownModule():
    sc.set_docs_dir(_SAVED_DOCS_DIR)


def git(cwd, *args):
    r = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid",
                        "-c", "commit.gpgsign=false", "-c", "init.defaultBranch=main"]
                       + list(args), cwd=str(cwd), capture_output=True, text=True)
    if r.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {r.stderr}")
    return r.stdout.strip()


def run(fn, *args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fn(*args)
    return rc, buf.getvalue()


PLAN = "# Audit Plan\n\n| Path | Status | Reference | Notes |\n|---|---|---|---|\n"


def project(root):
    """A git project with one area, `src/`, marked ANALYZED at HEAD (uncommitted)."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "src").mkdir()
    (root / "src" / "a.txt").write_text("one\n", encoding="utf-8")
    (root / "ai_docs" / "audit").mkdir(parents=True)
    (root / "ai_docs" / "audit" / "audit_plan.md").write_text(
        PLAN + "| src/ | PENDING | - | |\n", encoding="utf-8")
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    rc, out = run(sc.cmd_mark, root, ["src"])
    assert rc == 0, out
    return root


def recorded_ref(root):
    _, _, rows = sc.parse_audit_plan(root)
    return next(r["ref"] for r in rows if r["path"] == "src/")


def set_ref(root, new):
    plan = root / "ai_docs" / "audit" / "audit_plan.md"
    plan.write_text(plan.read_text(encoding="utf-8").replace(recorded_ref(root), new),
                    encoding="utf-8")


def clone(src, dest, *extra):
    subprocess.run(["git", "clone", "-q", *extra, "file://" + src.as_posix(), str(dest)],
                   check=True, capture_output=True)
    return dest


@unittest.skipUnless(HAS_GIT, "git not available")
class DanglingReference(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def assertUnverifiable(self, rc, out, msg):
        self.assertEqual(rc, 1, f"{msg}: an area stale cannot evaluate is not fresh\n{out}")
        self.assertNotIn("[ok]", out, f"{msg}: [ok] printed over an unverified area\n{out}")

    def test_mark_amend_gc_fails_closed(self):
        """AC1 -- the incident, reproduced end to end."""
        root = project(self.tmp / "p")
        ref = recorded_ref(root)
        git(root, "commit", "-q", "-a", "--amend", "--no-edit")
        git(root, "reflog", "expire", "--expire-unreachable=now", "--all")
        git(root, "gc", "-q", "--prune=now")
        self.assertNotEqual(subprocess.run(["git", "cat-file", "-e", ref + "^{commit}"],
                                           cwd=root, capture_output=True).returncode, 0,
                            "fixture: gc must have pruned the amended-away commit")
        rc, out = run(sc.cmd_stale, root)
        self.assertUnverifiable(rc, out, "pruned reference")
        self.assertIn(f"{sc.entry_script()} mark src/", out,
                      "the message must hand the user the re-mark command")

    def test_orphan_warned_before_it_dangles(self):
        """AC2 -- while the amended-away commit is still in the object store."""
        root = project(self.tmp / "p")
        git(root, "commit", "-q", "-a", "--amend", "--no-edit")
        rc, out = run(sc.cmd_stale, root)
        self.assertEqual(rc, 0, f"an orphan is still evaluable: warn, never fail\n{out}")
        self.assertIn("not an ancestor of HEAD", out)
        self.assertIn("[ok]", out)

    def test_new_commit_is_silent(self):
        """AC3 -- the right gesture changes nothing."""
        root = project(self.tmp / "p")
        git(root, "commit", "-q", "-a", "-m", "record analysis")
        rc, out = run(sc.cmd_stale, root)
        self.assertEqual(rc, 0, out)
        self.assertNotIn("[warn]", out)
        self.assertNotIn("[stale]", out)
        self.assertIn("[ok]", out)

    def _squashed_origin(self):
        origin = project(self.tmp / "origin")
        git(origin, "commit", "-q", "-a", "-m", "record base analysis")
        git(origin, "checkout", "-q", "-b", "feature")
        (origin / "src" / "a.txt").write_text("two\n", encoding="utf-8")
        git(origin, "commit", "-q", "-a", "-m", "feature work")
        run(sc.cmd_mark, origin, ["src"])
        git(origin, "commit", "-q", "-a", "-m", "record feature analysis")
        git(origin, "checkout", "-q", "main")
        git(origin, "merge", "-q", "--squash", "feature")
        git(origin, "commit", "-q", "-m", "squash feature")
        git(origin, "branch", "-q", "-D", "feature")
        return origin

    def test_squash_merged_reference_fails_on_a_fresh_clone(self):
        """AC4 -- the reference never reached the clone: no warning ever preceded it."""
        c = clone(self._squashed_origin(), self.tmp / "c")
        rc, out = run(sc.cmd_stale, c)
        self.assertUnverifiable(rc, out, "squash-merged reference")
        self.assertIn("squash-merged", out)

    def test_shallow_clone_adds_the_fetch_hint(self):
        """AC5 -- additive: a shallow clone may ALSO be missing it for the squash reason."""
        origin = project(self.tmp / "origin")
        git(origin, "commit", "-q", "-a", "-m", "record analysis")
        base = git(origin, "rev-list", "--max-parents=0", "HEAD")[:12]
        (origin / "src" / "b.txt").write_text("b\n", encoding="utf-8")
        git(origin, "add", "-A")
        git(origin, "commit", "-q", "-m", "later")
        c = clone(origin, self.tmp / "c", "--depth", "1")
        set_ref(c, base)
        rc, out = run(sc.cmd_stale, c)
        self.assertUnverifiable(rc, out, "reference beyond the clone depth")
        self.assertIn("--unshallow", out)
        self.assertIn("squash-merged", out, "the fetch hint adds to the cause, never replaces it")

    def test_hash_reference_without_git_fails(self):
        """AC6 -- git unavailable (a copy with no .git) used to fall to 'not parseable', rc 0."""
        root = project(self.tmp / "p")
        git(root, "commit", "-q", "-a", "-m", "record analysis")
        copy = self.tmp / "copy"
        shutil.copytree(root, copy, ignore=shutil.ignore_patterns(".git"))
        rc, out = run(sc.cmd_stale, copy)
        self.assertUnverifiable(rc, out, "hash reference without git")
        self.assertIn("git is not usable here", out,
                      "without git the cause is git itself, not a missing commit")

    def test_unparseable_reference_fails(self):
        """AC7 -- a hand-edited reference in a git tree."""
        root = project(self.tmp / "p")
        set_ref(root, "unknown")
        git(root, "commit", "-q", "-a", "-m", "hand edit")
        rc, out = run(sc.cmd_stale, root)
        self.assertUnverifiable(rc, out, "unparseable reference")
        self.assertIn("mark src/", out)

    def test_check_is_not_clean(self):
        """AC8 -- the closure gate inherits the verdict."""
        root = project(self.tmp / "p")
        set_ref(root, "unknown")
        rc, out = run(sc.cmd_check, root)
        self.assertEqual(rc, 1, out)
        self.assertIn("NOT CLEAN", out)

    def test_mark_names_the_gestures_that_orphan_its_reference(self):
        """AC9 -- prevention where the reference is born."""
        root = self.tmp / "p"
        root.mkdir()
        (root / "src").mkdir()
        (root / "src" / "a.txt").write_text("one\n", encoding="utf-8")
        (root / "ai_docs" / "audit").mkdir(parents=True)
        git(root, "init", "-q")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "base")
        rc, out = run(sc.cmd_mark, root, ["src"])
        self.assertEqual(rc, 0, out)
        self.assertIn("[info]", out)
        for word in ("new commit", "amend", "squash"):
            self.assertIn(word, out.lower(), f"mark's hint must name '{word}'")

    def test_unknown_ancestry_still_compares(self):
        """Ledger: 'unknown' makes no ancestry claim and still evaluates freshness."""
        root = project(self.tmp / "p")
        git(root, "commit", "-q", "-a", "-m", "record analysis")
        (root / "src" / "a.txt").write_text("changed\n", encoding="utf-8")
        with mock.patch.object(sc, "git_ref_state", return_value="unknown"):
            rc, out = run(sc.cmd_stale, root)
        self.assertEqual(rc, 1, out)
        self.assertIn("src/a.txt", out, "the comparison must still run")
        self.assertNotIn("not an ancestor", out)
        self.assertNotIn("[stale] src/", out)

    def test_comparison_failure_fails_closed(self):
        """AC10 -- the reference resolves, the comparison does not: the path where a
        slip would quietly bring the defect back."""
        root = project(self.tmp / "p")
        git(root, "commit", "-q", "-a", "-m", "record analysis")
        with mock.patch.object(sc, "git_changed_since", return_value=None):
            rc, out = run(sc.cmd_stale, root)
        self.assertUnverifiable(rc, out, "comparison failure")


def docs_area_project(root):
    """A git project whose plan (written before 2026-10-19) lists the docs root itself
    as an analyzed area, recorded at a clean HEAD as a commit hash. `mark` no longer
    records the docs root, so the legacy row is written directly."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "ai_docs" / "audit").mkdir(parents=True)
    (root / "ai_docs" / "notes.md").write_text("one\n", encoding="utf-8")
    plan = root / "ai_docs" / "audit" / "audit_plan.md"
    plan.write_text(PLAN + "| ai_docs/ | PENDING | - | |\n", encoding="utf-8")
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    head = subprocess.run(["git", "rev-parse", "--short=12", "HEAD"], cwd=str(root),
                          capture_output=True, text=True).stdout.strip()
    plan.write_text(PLAN + "| ai_docs/ | ANALYZED | %s | |\n" % head, encoding="utf-8")
    return root


@unittest.skipUnless(HAS_GIT, "git not available")
class AuditPlanSelfReference(unittest.TestCase):
    """The audit plan records the marks; its own edit is not a change to the area
    that contains it. Before the fix, committing a hash mark of `ai_docs/` made that
    area stale again, and re-marking repeated the loop (2026-09-25, acd4cf0)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_committing_the_mark_leaves_the_area_fresh(self):
        root = docs_area_project(self.tmp / "p")
        _, _, rows = sc.parse_audit_plan(root)
        ref = next(r["ref"] for r in rows if r["path"] == "ai_docs/")
        self.assertRegex(ref, r"^[0-9a-f]{7,40}$", "fixture: a clean tree marks a hash")
        git(root, "commit", "-q", "-a", "-m", "record analysis")
        rc, out = run(sc.cmd_stale, root)
        self.assertEqual(rc, 0, f"the mark's own commit made its area stale\n{out}")
        self.assertIn("[ok]", out)

    def test_a_document_edit_never_makes_the_docs_root_stale(self):
        # owner, 2026-10-19: the docs root is governance that `validate` checks; `stale`
        # counted every document edit as drift (the row was re-marked 15 times in two days)
        root = docs_area_project(self.tmp / "p")
        git(root, "commit", "-q", "-a", "-m", "record analysis")
        (root / "ai_docs" / "notes.md").write_text("two\n", encoding="utf-8")
        rc, out = run(sc.cmd_stale, root)
        self.assertEqual(rc, 0, out)
        self.assertNotIn("notes.md", out)


class DocsRootIsNotAnArea(unittest.TestCase):
    """2026-10-19: an `ai_docs/` row made `stale` fire on every document edit, and was
    re-marked 15 times in two days; `validate` already checks the docs root."""

    def test_stale_ignores_docs_root_files_and_mark_skips_it(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "ai_docs" / "audit").mkdir(parents=True)
            (root / "src").mkdir()
            (root / "src" / "a.py").write_text("x = 1\n", encoding="utf-8")
            (root / "ai_docs" / "audit" / "audit_plan.md").write_text(
                PLAN + "| . | ANALYZED | 2000-01-01T00:00:00Z |  |\n", encoding="utf-8")
            os.utime(root / "src" / "a.py", (946684800, 946684800))   # 2000-01-01
            (root / "ai_docs" / "notes.md").write_text("new\n", encoding="utf-8")
            rc, out = run(sc.cmd_stale, root)
            self.assertNotIn("notes.md", out, "a docs-root edit is not code drift")
            rc, out = run(sc.cmd_mark, root, ["ai_docs/", "src"])
            self.assertEqual(rc, 0, out)
            self.assertIn("docs root is not an area", out)
            plan = (root / "ai_docs" / "audit" / "audit_plan.md").read_text(encoding="utf-8")
            self.assertNotIn("| ai_docs", plan)


class MarkNote(unittest.TestCase):
    """Field case 2026-10-19: releases 1.44.0-1.46.0 left no dated event, because the
    date had to be copied by hand into project_notes.md. `mark --note` writes it."""

    def project(self, d, notes=None):
        root = Path(d)
        (root / "ai_docs" / "audit").mkdir(parents=True)
        (root / "src").mkdir()
        (root / "src" / "a.py").write_text("x = 1\n", encoding="utf-8")
        if notes is not None:
            (root / "ai_docs" / "audit" / sc.PROJECT_NOTES).write_text(notes, encoding="utf-8")
        return root

    def test_note_becomes_the_newest_dated_entry(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.project(d, "Preface line.\n\n**2026-01-01 — older.** body\n")
            rc, out = run(lambda r, p: sc.cmd_mark(r, p, "release 1.46.0"), root, ["src"])
            self.assertEqual(rc, 0, out)
            text = (root / "ai_docs" / "audit" / sc.PROJECT_NOTES).read_text(encoding="utf-8")
            self.assertTrue(text.startswith("Preface line."), "the preface stays on top")
            openers = sc.entry_openers(text)
            self.assertEqual(openers[0][1], "release 1.46.0")
            self.assertEqual(openers[1][1], "older")
            self.assertEqual(sc.malformed_openers(text), [])

    def test_note_creates_the_file_when_absent(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.project(d)
            run(lambda r, p: sc.cmd_mark(r, p, "fix after closure"), root, ["src"])
            text = (root / "ai_docs" / "audit" / sc.PROJECT_NOTES).read_text(encoding="utf-8")
            self.assertEqual([o[1] for o in sc.entry_openers(text)], ["fix after closure"])

    def test_bad_note_is_refused_before_anything_is_written(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.project(d)
            rc, out = run(lambda r, p: sc.cmd_mark(r, p, "a **bold** note"), root, ["src"])
            self.assertEqual(rc, 1)
            self.assertFalse((root / "ai_docs" / "audit" / "audit_plan.md").exists())

    def test_without_note_and_no_open_unit_mark_reminds(self):
        with tempfile.TemporaryDirectory() as d:
            root = self.project(d)
            rc, out = run(sc.cmd_mark, root, ["src"])
            self.assertEqual(rc, 0)
            self.assertIn("--note", out)


if __name__ == "__main__":
    unittest.main()
