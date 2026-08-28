#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test battery for the `orient` subcommand (M4 Unit 1, SessionStart hook) in
sdlc_check.py.

Standard library only (unittest). Windows and POSIX compatible. Every fixture
is written to a fresh temp dir per test -- no shared mutable state, no real
filesystem side effects outside tempfile.TemporaryDirectory().

Covers the P-TM consolidation Unit-1 [MILESTONE] requirements:
  T1 zero-execution  -> test_zero_execution_side_effect
  T2 size bound      -> test_total_size_cap
  T3 confinement     -> test_path_confinement_applied
  T8 fail-open       -> test_missing_ai_docs_silent_exit0 / test_unreadable_doc_skipped
  no-dup (M-VISION)  -> test_hybrid_pointer_no_dup
"""
import json
import os
import sys
import tempfile
import unittest
from io import StringIO
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_core as sc  # noqa: E402  the SHARED core: these assert spine behaviour,
# not whichever overlay is installed -- an overlay may replace part of the document model
import sdlc_core  # noqa: E402  the module that OWNS the behaviour under test


def orient_args(root=None, hybrid=False):
    return SimpleNamespace(root=str(root) if root else None, hybrid=hybrid)


def run_orient(root=None, hybrid=False):
    """Run cmd_orient capturing stdout. Returns (rc, stdout)."""
    buf = StringIO()
    with redirect_stdout(buf):
        rc = sc.cmd_orient(orient_args(root=root, hybrid=hybrid))
    return rc, buf.getvalue()


def seed(root, rel, text):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def setUpModule():
    """Pin the docs root for this battery's fixtures.

    The marketing overlay defaults to `mkt_docs`, so a shared battery that builds
    `ai_docs` fixtures must say which root it means instead of inheriting whichever
    distribution happens to be installed."""
    global _SAVED_DOCS_DIR
    _SAVED_DOCS_DIR = sdlc_core.docs_dir()
    sdlc_core.set_docs_dir("ai_docs")


def tearDownModule():
    sdlc_core.set_docs_dir(_SAVED_DOCS_DIR)


class OrientTests(unittest.TestCase):

    def test_missing_ai_docs_silent_exit0(self):
        # Fresh project, no ai_docs/ at all -> emit nothing, exit 0 (fail-open T8).
        with tempfile.TemporaryDirectory() as d:
            rc, out = run_orient(root=d)
            self.assertEqual(rc, 0)
            self.assertEqual(out.strip(), "")

    def test_all_sections_emitted(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d, "ai_docs/README.md", "README-BODY")
            seed(d, "ai_docs/INDEX.md", "INDEX-BODY")
            seed(d, "ai_docs/reference/INDEX.md", "ROUTER-BODY")
            seed(d, "ai_docs/audit/handoff.md", "HANDOFF-BODY")
            rc, out = run_orient(root=d)
            self.assertEqual(rc, 0)
            for label in ("Reading guide (README)", "Canonical manifest (INDEX)",
                          "Guide router (when-to-consult)", "Last session handoff"):
                self.assertIn(label, out)
            for body in ("README-BODY", "INDEX-BODY", "ROUTER-BODY", "HANDOFF-BODY"):
                self.assertIn(body, out)
            self.assertIn("Rule Zero", out)

    def test_partial_present_skips_missing(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d, "ai_docs/audit/handoff.md", "ONLY-HANDOFF")
            rc, out = run_orient(root=d)
            self.assertEqual(rc, 0)
            self.assertIn("ONLY-HANDOFF", out)
            self.assertNotIn("README-BODY", out)
            self.assertIn("Last session handoff", out)
            self.assertNotIn("Reading guide (README)", out)

    def test_total_size_cap(self):
        with tempfile.TemporaryDirectory() as d:
            # Four docs each at the per-doc cap -> total (24000) exceeds
            # ORIENT_MAX_TOTAL_CHARS. Fill with digits 4-7, which never appear
            # in the header/labels/notes/triage line (those use 1/2/3 only), so
            # counting them isolates the emitted DOC-BODY chars exactly.
            seed(d, "ai_docs/README.md", "4" * sc.ORIENT_PER_DOC_CHARS)
            seed(d, "ai_docs/INDEX.md", "5" * sc.ORIENT_PER_DOC_CHARS)
            seed(d, "ai_docs/reference/INDEX.md", "6" * sc.ORIENT_PER_DOC_CHARS)
            seed(d, "ai_docs/audit/handoff.md", "7" * sc.ORIENT_PER_DOC_CHARS)
            rc, out = run_orient(root=d)
            self.assertEqual(rc, 0)
            body_chars = sum(out.count(c) for c in "4567")
            self.assertLessEqual(body_chars, sc.ORIENT_MAX_TOTAL_CHARS)
            self.assertIn("truncated", out)

    def test_unreadable_doc_skipped(self):
        # A directory where a file path is expected -> read/stat path is not a
        # file -> skipped, no traceback, exit 0.
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "ai_docs").mkdir()
            (Path(d) / "ai_docs" / "README.md").mkdir()  # dir, not a file
            seed(d, "ai_docs/audit/handoff.md", "HANDOFF-OK")
            rc, out = run_orient(root=d)
            self.assertEqual(rc, 0)
            self.assertIn("HANDOFF-OK", out)
            self.assertNotIn("Reading guide (README)", out)

    def test_zero_execution_side_effect(self):
        # A doc containing shell-like payloads must be emitted as inert TEXT,
        # never executed (P-TM T1). Assert the sentinel file is not created.
        with tempfile.TemporaryDirectory() as d:
            sentinel = Path(d) / "PWNED"
            payload = "$(touch '%s'); `touch '%s'`; rm -rf /" % (sentinel, sentinel)
            seed(d, "ai_docs/README.md", payload)
            rc, out = run_orient(root=d)
            self.assertEqual(rc, 0)
            self.assertFalse(sentinel.exists(), "orient executed doc content -- T1 violated")
            self.assertIn("touch", out)  # payload surfaced as literal text

    def test_hybrid_pointer_no_dup(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d, "ai_docs/README.md", "README-BODY")
            rc, out = run_orient(root=d, hybrid=True)
            self.assertEqual(rc, 0)
            self.assertIn("devpnt_mcp_get_bootstrap", out)
            self.assertIn("devPNT active", out)
            # Must not attempt to replicate plan/KL content itself.
            self.assertNotIn("Master Plan\n", out)

    def test_no_hybrid_pointer_when_flag_off(self):
        with tempfile.TemporaryDirectory() as d:
            seed(d, "ai_docs/README.md", "README-BODY")
            rc, out = run_orient(root=d, hybrid=False)
            self.assertEqual(rc, 0)
            self.assertNotIn("devpnt_mcp_get_bootstrap", out)

    def test_path_confinement_applied(self):
        # Every doc path must be routed through confine_under (T3). Monkeypatch
        # it to record the calls, then restore.
        with tempfile.TemporaryDirectory() as d:
            seed(d, "ai_docs/README.md", "README-BODY")
            calls = []
            # Patched on the CORE, not on the entry point: cmd_orient resolves
            # confine_under in the module that defines it, so patching the thin
            # re-export would spy on nothing and the test would pass on broken code.
            real = sdlc_core.confine_under

            def spy(base, rel):
                calls.append(rel)
                return real(base, rel)

            sdlc_core.confine_under = spy
            try:
                rc, _ = run_orient(root=d)
            finally:
                sdlc_core.confine_under = real
            self.assertEqual(rc, 0)
            self.assertEqual(calls, [rel for _, rel in sc.orient_docs()])


def run_check(root, user_settings=None, config_dir=None):
    """Run cmd_check capturing stdout. Returns (rc, stdout).

    Hermetic by default: the user-level detection (F-042) is pointed through
    the AGENTIC_SDLC_USER_SETTINGS seam at a nonexistent fixture path, so a
    real global hook on the developer's machine can never decide a verdict.
    Pass user_settings to exercise the global states, or config_dir to pin the
    real CLAUDE_CONFIG_DIR derivation (the seam is then left unset)."""
    buf = StringIO()
    saved = {k: os.environ.pop(k, None)
             for k in ("AGENTIC_SDLC_USER_SETTINGS", "CLAUDE_CONFIG_DIR")}
    if config_dir is not None:
        os.environ["CLAUDE_CONFIG_DIR"] = str(config_dir)
    else:
        os.environ["AGENTIC_SDLC_USER_SETTINGS"] = str(
            user_settings if user_settings is not None
            else Path(root) / "no-user-settings.json")
    try:
        with redirect_stdout(buf):
            rc = sc.cmd_check(Path(root))
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    return rc, buf.getvalue()


def grouped_hook(cmd):
    # The documented shape: SessionStart groups carrying a hooks: [] array.
    return {"hooks": {"SessionStart": [{"hooks": [{"type": "command", "command": cmd}]}]}}


def direct_hook(cmd):
    # The in-the-wild shape: hook objects placed directly in the SessionStart array.
    return {"hooks": {"SessionStart": [{"type": "command", "command": cmd}]}}


# Output fragments of the two notes (F-041 mechanics, F-042 wording).
# Fragments, not full lines: the goldens freeze the exact wording; these tests
# pin the behavioral contract. The two fragments are disjoint by design.
UNWIRED_NOTE = "without automatic orientation"
DEAD_NOTE = "validator that no longer exists"


class HookDetectionTests(unittest.TestCase):
    """F-041 FS-A: `check` notes the unwired and the dead orientation-hook
    states. The notes never move the exit code and never leak into validate."""

    def _docs(self, d):
        seed(d, "ai_docs/README.md", "x")  # a docs root, so check has a tree to walk

    def _live_cmd(self, d, name="sdlc_check.py"):
        vp = Path(d) / "hookbin" / name
        vp.parent.mkdir(parents=True, exist_ok=True)
        vp.write_text("# validator stub", encoding="utf-8")
        return 'python "%s" orient' % vp

    def _wire(self, d, rel, payload):
        seed(d, rel, payload if isinstance(payload, str) else json.dumps(payload))

    def test_no_config_notes_unwired_and_rc_unchanged(self):
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            rc_bare, out_bare = run_check(d)
            self.assertIn(UNWIRED_NOTE, out_bare)
            self.assertNotIn(DEAD_NOTE, out_bare)
            self._wire(d, ".claude/settings.json", grouped_hook(self._live_cmd(d)))
            rc_wired, out_wired = run_check(d)
            self.assertNotIn(UNWIRED_NOTE, out_wired)
            self.assertEqual(rc_bare, rc_wired)  # the note is informational only

    def test_wired_direct_shape_in_local_settings_silent(self):
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            self._wire(d, ".claude/settings.local.json", direct_hook(self._live_cmd(d)))
            _, out = run_check(d)
            self.assertNotIn(UNWIRED_NOTE, out)
            self.assertNotIn(DEAD_NOTE, out)

    def test_wired_codex_hooks_silent(self):
        # .codex/hooks.json documents SessionStart at top level (ENFORCEMENT par.4).
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            self._wire(d, ".codex/hooks.json",
                       {"SessionStart": [{"type": "command", "command": self._live_cmd(d)}]})
            _, out = run_check(d)
            self.assertNotIn(UNWIRED_NOTE, out)

    def test_wired_bom_settings_silent(self):
        # PowerShell/Notepad write BOM'd JSON: a wired project must not read as
        # unwired (utf-8-sig; declared divergence from Node's JSON.parse).
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            body = "\ufeff" + json.dumps(grouped_hook(self._live_cmd(d)))
            self._wire(d, ".claude/settings.json", body)
            _, out = run_check(d)
            self.assertNotIn(UNWIRED_NOTE, out)

    def test_dead_hook_notes_distinctly(self):
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            rc_bare, _ = run_check(d)
            missing = str(Path(d) / "gone" / "sdlc_check.py")
            self._wire(d, ".claude/settings.json",
                       grouped_hook('python "%s" orient' % missing))
            rc, out = run_check(d)
            self.assertIn(DEAD_NOTE, out)
            self.assertNotIn(UNWIRED_NOTE, out)
            self.assertEqual(rc, rc_bare)  # the dead note never moves rc

    def test_dead_beside_live_is_silent(self):
        # Any-resolves aggregation: the client runs ALL SessionStart hooks, so a
        # live entry beside a dead one means sessions ARE oriented.
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            missing = str(Path(d) / "gone" / "sdlc_check.py")
            self._wire(d, ".claude/settings.json",
                       grouped_hook('python "%s" orient' % missing))
            self._wire(d, ".claude/settings.local.json", direct_hook(self._live_cmd(d)))
            _, out = run_check(d)
            self.assertNotIn(DEAD_NOTE, out)
            self.assertNotIn(UNWIRED_NOTE, out)

    def test_cannot_tell_is_silent_never_dead(self):
        # Matching command whose tokens name no validator: the lib.js contract --
        # say nothing, never "broken".
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            self._wire(d, ".claude/settings.json",
                       grouped_hook("run --mode=sdlc_check.py:legacy orient"))
            _, out = run_check(d)
            self.assertNotIn(DEAD_NOTE, out)
            self.assertNotIn(UNWIRED_NOTE, out)

    def test_session_start_without_orient_notes_unwired(self):
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            self._wire(d, ".claude/settings.json", grouped_hook("python other.py lint"))
            _, out = run_check(d)
            self.assertIn(UNWIRED_NOTE, out)

    def test_malformed_settings_notes_unwired_no_crash(self):
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            self._wire(d, ".claude/settings.json", "{not json")
            rc, out = run_check(d)
            self.assertIn(UNWIRED_NOTE, out)

    def test_settings_path_is_directory_no_crash(self):
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            (Path(d) / ".claude" / "settings.json").mkdir(parents=True)
            rc, out = run_check(d)
            self.assertIn(UNWIRED_NOTE, out)

    def test_oversized_settings_counts_as_unwired(self):
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            pad = json.dumps(grouped_hook(self._live_cmd(d)))
            self._wire(d, ".claude/settings.json",
                       pad + " " * (2 * 1024 * 1024))  # past the read cap
            _, out = run_check(d)
            self.assertIn(UNWIRED_NOTE, out)

    def test_vendored_relative_command_silent(self):
        # ENFORCEMENT par.2/par.4: a vendored validator is named root-relative.
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            seed(d, "tools/sdlc_check.py", "# vendored stub")
            self._wire(d, ".claude/settings.json",
                       grouped_hook('python "tools/sdlc_check.py" orient'))
            _, out = run_check(d)
            self.assertNotIn(UNWIRED_NOTE, out)
            self.assertNotIn(DEAD_NOTE, out)

    def test_mkt_entry_point_name_matches(self):
        # Family predicate: the marketing lens ships mkt_check.py.
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            self._wire(d, ".claude/settings.json",
                       grouped_hook(self._live_cmd(d, name="mkt_check.py")))
            _, out = run_check(d)
            self.assertNotIn(UNWIRED_NOTE, out)

    def test_global_hook_silences_the_note(self):
        # F-042: the machine-global user settings are part of the detection --
        # without this, every project on a fixed machine reads unwired forever.
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            us = Path(d) / "userworld" / "settings.json"
            us.parent.mkdir(parents=True)
            us.write_text(json.dumps(grouped_hook(self._live_cmd(d))),
                          encoding="utf-8")
            _, out = run_check(d, user_settings=us)
            self.assertNotIn(UNWIRED_NOTE, out)
            self.assertNotIn(DEAD_NOTE, out)

    def test_global_dead_alone_notes_dead(self):
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            us = Path(d) / "userworld" / "settings.json"
            us.parent.mkdir(parents=True)
            missing = str(Path(d) / "gone" / "sdlc_check.py")
            us.write_text(json.dumps(grouped_hook('python "%s" orient' % missing)),
                          encoding="utf-8")
            _, out = run_check(d, user_settings=us)
            self.assertIn(DEAD_NOTE, out)
            self.assertNotIn(UNWIRED_NOTE, out)

    def test_global_dead_beside_live_project_silent(self):
        # Any-resolves aggregation ACROSS levels: project + user hooks merge.
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            us = Path(d) / "userworld" / "settings.json"
            us.parent.mkdir(parents=True)
            missing = str(Path(d) / "gone" / "sdlc_check.py")
            us.write_text(json.dumps(grouped_hook('python "%s" orient' % missing)),
                          encoding="utf-8")
            self._wire(d, ".claude/settings.json", grouped_hook(self._live_cmd(d)))
            _, out = run_check(d, user_settings=us)
            self.assertNotIn(DEAD_NOTE, out)
            self.assertNotIn(UNWIRED_NOTE, out)

    def test_user_level_relative_token_is_cannot_tell(self):
        # No cwd exists at user level: a relative token can never be judged
        # dead (the lib.js contract, re-instantiated across the level split).
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            us = Path(d) / "userworld" / "settings.json"
            us.parent.mkdir(parents=True)
            us.write_text(json.dumps(
                grouped_hook('python "tools/sdlc_check.py" orient')),
                encoding="utf-8")
            _, out = run_check(d, user_settings=us)
            self.assertNotIn(DEAD_NOTE, out)
            self.assertNotIn(UNWIRED_NOTE, out)

    def test_claude_config_dir_derivation(self):
        # With the seam unset, the production path rule must apply:
        # CLAUDE_CONFIG_DIR when set, else ~/.claude.
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            cfg = Path(d) / "cfgworld"
            cfg.mkdir(parents=True)
            (cfg / "settings.json").write_text(
                json.dumps(grouped_hook(self._live_cmd(d))), encoding="utf-8")
            _, out = run_check(d, config_dir=cfg)
            self.assertNotIn(UNWIRED_NOTE, out)
            self.assertNotIn(DEAD_NOTE, out)

    def test_validate_never_prints_the_notes(self):
        # The CI path (validate, incl. --strict) must stay silent on wiring.
        with tempfile.TemporaryDirectory() as d:
            self._docs(d)
            buf = StringIO()
            with redirect_stdout(buf):
                sc.cmd_validate(Path(d), strict=True)
            out = buf.getvalue()
            self.assertNotIn(UNWIRED_NOTE, out)
            self.assertNotIn(DEAD_NOTE, out)


if __name__ == "__main__":
    unittest.main()
