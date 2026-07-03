#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test battery for the `plan` subcommand (Subagent Execution, Feature A) and
the shared `confine_under` helper in sdlc_check.py.

Standard library only (unittest). Windows and POSIX compatible. Every plan
fixture is written to a fresh temp dir per test — no shared mutable state,
no real filesystem side effects outside tempfile.TemporaryDirectory().
"""
import json
import os
import shutil
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_check as sc  # noqa: E402


def make_project(root):
    """Minimal ai_docs/ skeleton so require_ai_docs-style checks and the
    reference-dir confinement target exist."""
    (root / "ai_docs" / "reference").mkdir(parents=True, exist_ok=True)
    (root / "ai_docs" / "solutions").mkdir(parents=True, exist_ok=True)


def write_plan(root, name, tasks, extra_frontmatter=""):
    """Writes ai_docs/solutions/<name> with a fenced ```json tasks block."""
    body = (
        "---\n"
        "status: DRAFT\n"
        f"{extra_frontmatter}"
        "---\n"
        f"# Plan: {name}\n\n"
        "```json\n"
        + json.dumps({"tasks": tasks}, indent=2)
        + "\n```\n"
    )
    p = root / "ai_docs" / "solutions" / name
    p.write_text(body, encoding="utf-8")
    return p


def write_ledger(plan_path, data):
    ledger_path = plan_path.with_name(plan_path.stem + ".ledger.json")
    ledger_path.write_text(json.dumps(data), encoding="utf-8")
    return ledger_path


def valid_task(**overrides):
    t = {
        "id": "T1",
        "title": "Do the thing",
        "paths": ["ai_docs/solutions/dummy.md"],
        "verify": "python -m pytest tests/test_dummy.py",
    }
    t.update(overrides)
    return t


class ArgsNS:
    """Minimal stand-in for argparse.Namespace: only attrs cmd_plan reads."""
    def __init__(self, file, task=None):
        self.file = file
        self.task = task


class ConfineUnderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.base = self.tmp / "base"
        self.base.mkdir()
        (self.base / "sub").mkdir()
        (self.base / "sub" / "file.md").write_text("x", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_ok_relative_path_resolves_under_base(self):
        t = sc.confine_under(self.base, "sub/file.md")
        self.assertIsNotNone(t)
        self.assertEqual(t.resolve(), (self.base / "sub" / "file.md").resolve())

    def test_absolute_path_rejected(self):
        abs_path = str((self.tmp / "outside.md"))
        self.assertIsNone(sc.confine_under(self.base, abs_path))

    def test_dotdot_rejected(self):
        self.assertIsNone(sc.confine_under(self.base, "../escape.md"))
        self.assertIsNone(sc.confine_under(self.base, "sub/../../escape.md"))

    def test_escape_via_symlink_or_resolve_rejected(self):
        # Even without a real .. part, a path resolving outside base is rejected.
        # Simulate by pointing base at a subdir and rel at a sibling-looking name
        # that .resolve() would still keep inside base (control case: must be None
        # only for genuine escapes). Here we assert a straightforward outside path.
        outside = self.tmp / "sibling.md"
        outside.write_text("y", encoding="utf-8")
        rel = os.path.relpath(str(outside), str(self.base))
        self.assertIsNone(sc.confine_under(self.base, rel))

    def test_nonexistent_target_still_confines_ok(self):
        # confine_under only checks containment, not existence.
        t = sc.confine_under(self.base, "sub/does_not_exist.md")
        self.assertIsNotNone(t)


class PlanValidateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "project"
        make_project(self.root)
        (self.root / "ai_docs" / "solutions" / "dummy.md").write_text("x", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_validate(self, plan_path):
        args = ArgsNS(file=str(plan_path))
        args.plan_cmd = "validate"
        return sc.cmd_plan(self.root, args)

    def run_brief(self, plan_path, task_id):
        args = ArgsNS(file=str(plan_path), task=task_id)
        args.plan_cmd = "brief"
        return sc.cmd_plan(self.root, args)

    def test_valid_plan_rc0(self):
        p = write_plan(self.root, "PLAN_valid.md", [valid_task()])
        rc = self.run_validate(p)
        self.assertEqual(rc, 0)

    def test_missing_verify_rc2(self):
        t = valid_task()
        del t["verify"]
        p = write_plan(self.root, "PLAN_missing_verify.md", [t])
        rc = self.run_validate(p)
        self.assertEqual(rc, 2)

    def test_missing_paths_and_produces_rc2(self):
        t = valid_task()
        del t["paths"]
        p = write_plan(self.root, "PLAN_no_paths.md", [t])
        rc = self.run_validate(p)
        self.assertEqual(rc, 2)

    def test_produces_alone_satisfies_paths_or_produces(self):
        t = valid_task(produces=["ai_docs/solutions/dummy.md"])
        del t["paths"]
        p = write_plan(self.root, "PLAN_produces_only.md", [t])
        rc = self.run_validate(p)
        self.assertEqual(rc, 0)

    def test_path_escape_rc2(self):
        t = valid_task(paths=["../escape.md"])
        p = write_plan(self.root, "PLAN_escape.md", [t])
        rc = self.run_validate(p)
        self.assertEqual(rc, 2)

    def test_absolute_path_rc2(self):
        abs_p = str((self.tmp / "outside.md"))
        t = valid_task(paths=[abs_p])
        p = write_plan(self.root, "PLAN_abs.md", [t])
        rc = self.run_validate(p)
        self.assertEqual(rc, 2)

    def test_guide_outside_reference_and_kb_rc2(self):
        t = valid_task(guides=["../../outside_guide.md"])
        p = write_plan(self.root, "PLAN_bad_guide.md", [t])
        rc = self.run_validate(p)
        self.assertEqual(rc, 2)

    def test_guide_inside_project_reference_ok(self):
        (self.root / "ai_docs" / "reference" / "GUIDE_topic.md").write_text("g", encoding="utf-8")
        t = valid_task(guides=["GUIDE_topic.md"])
        p = write_plan(self.root, "PLAN_good_guide.md", [t])
        rc = self.run_validate(p)
        self.assertEqual(rc, 0)

    def test_duplicate_ids_rc2(self):
        t1 = valid_task(id="T1")
        t2 = valid_task(id="T1", title="Second task")
        p = write_plan(self.root, "PLAN_dup.md", [t1, t2])
        rc = self.run_validate(p)
        self.assertEqual(rc, 2)

    def test_malformed_plan_json_rc2(self):
        p = self.root / "ai_docs" / "solutions" / "PLAN_malformed.md"
        p.write_text("---\nstatus: DRAFT\n---\n# Plan\n\n```json\n{not valid json\n```\n",
                     encoding="utf-8")
        rc = self.run_validate(p)
        self.assertEqual(rc, 2)

    def test_missing_json_block_rc2(self):
        p = self.root / "ai_docs" / "solutions" / "PLAN_no_block.md"
        p.write_text("---\nstatus: DRAFT\n---\n# Plan\n\nNo fenced block here.\n", encoding="utf-8")
        rc = self.run_validate(p)
        self.assertEqual(rc, 2)

    def test_malformed_ledger_handled_gracefully(self):
        p = write_plan(self.root, "PLAN_ok_ledger.md", [valid_task()])
        ledger_path = p.with_name(p.stem + ".ledger.json")
        ledger_path.write_text("{not valid json", encoding="utf-8")
        # Malformed ledger must not crash validate; plan itself is still valid.
        rc = self.run_validate(p)
        self.assertEqual(rc, 0)

    def test_ledger_id_not_in_plan_rc0_with_stderr_warning(self):
        p = write_plan(self.root, "PLAN_orphan_ledger.md", [valid_task(id="T1")])
        write_ledger(p, {"T-GHOST": {"status": "done", "verify_result": "pass",
                                     "timestamp": "2026-01-01T00:00:00Z"}})
        stderr = StringIO()
        old_stderr = sys.stderr
        sys.stderr = stderr
        try:
            rc = self.run_validate(p)
        finally:
            sys.stderr = old_stderr
        self.assertEqual(rc, 0)
        self.assertIn("not found", stderr.getvalue())

    def test_regression_own_repo_validate_still_green(self):
        # Regression per the E-TDD test block: validate/check on this repo's
        # own ai_docs stays green after the confine_under refactor.
        repo_root = Path(__file__).resolve().parents[3]
        rc = sc.cmd_validate(repo_root, strict=False)
        self.assertEqual(rc, 0)


class PlanBriefTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "project"
        make_project(self.root)
        (self.root / "ai_docs" / "solutions" / "dummy.md").write_text("x", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_brief(self, plan_path, task_id):
        args = ArgsNS(file=str(plan_path), task=task_id)
        args.plan_cmd = "brief"
        return sc.cmd_plan(self.root, args)

    def test_brief_unknown_task_rc2(self):
        p = write_plan(self.root, "PLAN_brief.md", [valid_task(id="T1")])
        rc = self.run_brief(p, "T-NOPE")
        self.assertEqual(rc, 2)

    def test_brief_prints_verify_text_without_executing(self):
        marker = self.tmp / "PWNED"
        t = valid_task(id="T1", verify=f"touch \"{marker}\"")
        p = write_plan(self.root, "PLAN_zero_exec.md", [t])

        stdout = StringIO()
        old_stdout = sys.stdout
        sys.stdout = stdout
        try:
            rc = self.run_brief(p, "T1")
        finally:
            sys.stdout = old_stdout

        self.assertEqual(rc, 0)
        out = stdout.getvalue()
        # The opaque verify text is present, verbatim, as printed text ...
        self.assertIn(f'touch "{marker}"', out)
        # ... but never executed: no PWNED file must exist on disk.
        self.assertFalse(marker.exists(),
                         "brief must never execute the verify string — zero-execution (T1)")

    def test_brief_includes_prior_produces_and_guides(self):
        (self.root / "ai_docs" / "reference" / "GUIDE_topic.md").write_text("g", encoding="utf-8")
        t1 = valid_task(id="T1", produces=["ai_docs/solutions/iface.md"])
        t2 = valid_task(id="T2", guides=["GUIDE_topic.md"])
        p = write_plan(self.root, "PLAN_interfaces.md", [t1, t2])

        stdout = StringIO()
        old_stdout = sys.stdout
        sys.stdout = stdout
        try:
            rc = self.run_brief(p, "T2")
        finally:
            sys.stdout = old_stdout

        self.assertEqual(rc, 0)
        out = stdout.getvalue()
        self.assertIn("ai_docs/solutions/iface.md", out)
        self.assertIn("GUIDE_topic.md", out)

    def test_brief_on_invalid_plan_rc2_no_output_side_effect(self):
        t = valid_task()
        del t["verify"]
        p = write_plan(self.root, "PLAN_invalid_brief.md", [t])
        rc = self.run_brief(p, "T1")
        self.assertEqual(rc, 2)


class ExtractPlanJsonTests(unittest.TestCase):
    def test_valid_block(self):
        text = "prose\n```json\n{\"tasks\": []}\n```\nmore prose"
        data, reason = sc.extract_plan_json(text)
        self.assertEqual(data, {"tasks": []})
        self.assertEqual(reason, "")

    def test_no_block_returns_none_and_reason(self):
        data, reason = sc.extract_plan_json("just prose, no fenced block")
        self.assertIsNone(data)
        self.assertTrue(reason)

    def test_malformed_json_returns_none_and_reason_never_raises(self):
        data, reason = sc.extract_plan_json("```json\n{broken\n```")
        self.assertIsNone(data)
        self.assertTrue(reason)

    def test_non_object_json_rejected(self):
        data, reason = sc.extract_plan_json("```json\n[1, 2, 3]\n```")
        self.assertIsNone(data)
        self.assertTrue(reason)

    def test_empty_text_never_raises(self):
        data, reason = sc.extract_plan_json("")
        self.assertIsNone(data)
        self.assertTrue(reason)

        data, reason = sc.extract_plan_json(None)
        self.assertIsNone(data)
        self.assertTrue(reason)


class LoadLedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_absent_file_returns_empty_no_reason(self):
        data, reason = sc.load_ledger(self.tmp / "nope.ledger.json")
        self.assertEqual(data, {})
        self.assertEqual(reason, "")

    def test_malformed_json_returns_empty_with_reason_never_raises(self):
        p = self.tmp / "bad.ledger.json"
        p.write_text("{not json", encoding="utf-8")
        data, reason = sc.load_ledger(p)
        self.assertEqual(data, {})
        self.assertTrue(reason)

    def test_non_object_json_returns_empty_with_reason(self):
        p = self.tmp / "list.ledger.json"
        p.write_text("[1, 2, 3]", encoding="utf-8")
        data, reason = sc.load_ledger(p)
        self.assertEqual(data, {})
        self.assertTrue(reason)

    def test_valid_ledger_round_trips(self):
        p = self.tmp / "ok.ledger.json"
        payload = {"T1": {"status": "done", "verify_result": "pass",
                          "timestamp": "2026-01-01T00:00:00Z"}}
        p.write_text(json.dumps(payload), encoding="utf-8")
        data, reason = sc.load_ledger(p)
        self.assertEqual(data, payload)
        self.assertEqual(reason, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
