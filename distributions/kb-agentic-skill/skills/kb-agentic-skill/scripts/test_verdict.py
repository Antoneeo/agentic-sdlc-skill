#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-076 battery — `verdict --hook`, the PreToolUse check of the guide-router verdict.

Rule Zero makes the agent declare the level with the router verdict and read the
guide it names before acting. A field agent edited without doing either and said
nothing stopped it. This hook reads the session transcript the client hands it and
refuses an edit (JSON `permissionDecision: deny`, exit 0) when no verdict was
declared, or a guide the verdict names was never read.

The contract guarded here: it refuses only on certainty and stays silent on
everything else (fail-open); it reads bounded data; it never prints `allow` (that
would skip the user's permission prompt); its reason echoes no transcript text.
Owner decisions: block, not warn (REQUEST_guide_verdict_check.md R3); wired by
default, cost accepted (R4, rulings.md r34).

    python scripts/test_verdict.py
"""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_core  # noqa: E402

GUIDE = "GUIDE_release.md"


def assistant(block):
    return json.dumps({"type": "assistant", "message": {"role": "assistant", "content": [block]}})


def say(text):
    return assistant({"type": "text", "text": text})


def call(name, **inp):
    return assistant({"type": "tool_use", "id": "toolu_x", "name": name, "input": inp})


VERDICT = say("Level: L2 · router: `%s` → read" % GUIDE)
READ = call("Read", file_path="ai_docs/reference/" + GUIDE)


class VerdictHook(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        ref = self.root / "ai_docs" / "reference"
        ref.mkdir(parents=True)
        (ref / GUIDE).write_text("---\ndescription: d\nstatus: CURRENT\n---\n# G\n",
                                 encoding="utf-8")
        (self.root / "src").mkdir()
        self.transcript = self.root / "t.jsonl"

    def tearDown(self):
        self._tmp.cleanup()

    def run_hook(self, lines=None, tool="Edit", target=None, raw=None, cwd=None, **extra):
        if lines is not None:
            self.transcript.write_text("\n".join(lines) + "\n", encoding="utf-8")
        payload = {"session_id": "s", "transcript_path": str(self.transcript),
                   "cwd": str(self.root), "hook_event_name": "PreToolUse",
                   "tool_name": tool,
                   "tool_input": {"file_path": str(target or self.root / "src" / "a.py")}}
        payload.update(extra)
        data = raw if raw is not None else json.dumps(payload)
        stdin = io.TextIOWrapper(io.BytesIO(data.encode("utf-8")), encoding="utf-8")
        out = io.StringIO()
        # cwd given: no --root, the hook runs where the session's `cd` left it
        argv = ["verdict", "--hook"] + ([] if cwd else ["--root", str(self.root)])
        here = os.getcwd()
        with mock.patch.object(sys, "stdin", stdin), contextlib.redirect_stdout(out):
            try:
                if cwd:
                    os.chdir(cwd)
                code = sdlc_core.main(argv)
            except SystemExit as e:  # pragma: no cover - argparse must never fire
                code = e.code
            finally:
                os.chdir(here)
        self.assertEqual(code, 0, "the hook always exits 0: exit 2 would block blind")
        text = out.getvalue()
        if not text.strip():
            return None
        obj = json.loads(text)
        hso = obj["hookSpecificOutput"]
        self.assertEqual(hso["hookEventName"], "PreToolUse")
        self.assertEqual(hso["permissionDecision"], "deny", "never allow, never ask")
        return hso["permissionDecisionReason"]

    # --- refusals -------------------------------------------------------
    def test_field_case_no_verdict_is_refused(self):
        reason = self.run_hook([say("I'll fix the build."), call("Bash", command="ls src")])
        self.assertIsNotNone(reason)
        self.assertIn("router", reason)
        self.assertIn("reference/INDEX.md", reason)

    def test_verdict_naming_unread_guide_is_refused_and_names_it(self):
        reason = self.run_hook([VERDICT])
        self.assertIsNotNone(reason)
        self.assertIn(GUIDE, reason)

    def test_every_edit_tool_is_checked(self):
        for tool in sdlc_core.VERDICT_EDIT_TOOLS:
            self.assertIsNotNone(self.run_hook([say("x")], tool=tool), tool)

    def test_reasons_stay_under_the_accepted_size(self):
        # R4 accepted "~250 characters"; FS3 binds it for ai_docs and two guide names
        (self.root / "ai_docs" / "reference" / "GUIDE_second_guide.md").write_text(
            "# G\n", encoding="utf-8")
        no_verdict = self.run_hook([say("x")])
        unread = self.run_hook([say("router: GUIDE_release.md, GUIDE_second_guide.md")])
        for reason in (no_verdict, unread):
            self.assertLessEqual(len(reason), 250, reason)
        self.assertIn("GUIDE_second_guide.md", unread)

    def test_notebook_edit_reads_notebook_path(self):
        payload_target = self.root / "src" / "nb.ipynb"
        self.transcript.write_text(say("x") + "\n", encoding="utf-8")
        data = json.dumps({"transcript_path": str(self.transcript), "tool_name": "NotebookEdit",
                           "tool_input": {"notebook_path": str(payload_target)}})
        self.assertIsNotNone(self.run_hook(raw=data))

    def test_level_quoted_in_prose_is_refused(self):
        # a declaration is a line that opens with the level word, never a quote in a
        # sentence (the F-085 rule): prose about Rule Zero declares nothing
        for text in ("Rule Zero says to write Level: L1 for a typo; this is bigger.",
                     "The hook accepts `Level: L1` as a declaration.",
                     "Triage level: L1 would be wrong here."):
            self.assertIsNotNone(self.run_hook([say(text)]), text)

    def test_router_quoted_in_prose_is_refused(self):
        # a verdict is a line that opens with `router` or a level declaration carrying
        # it on the same line; prose quoting the form declares nothing
        for text in ("The guide says to write router: no match before editing.",
                     "I'll add `router: no match` once I know.",
                     "Its Router verdict: GUIDE_release.md line is missing."):
            reason = self.run_hook([say(text), READ])
            self.assertIsNotNone(reason, text)
            self.assertIn("No guide-router verdict", reason, text)

    def test_router_line_forms_pass(self):
        # the two forms the refusal itself suggests stay valid
        for text in ("router: no match", "- router: `GUIDE_release.md` -> read",
                     "> **Router verdict**: no match", "Level: L2 and router: no match"):
            self.assertIsNone(self.run_hook([say(text), READ]), text)

    def test_spike_declaration_passes(self):
        # Rule Zero declares the level with the verdict "for L2, L3 and Spike"
        for text in ("Level: Spike · router: no match", "Livello: Spike · router: no match",
                     "Level: Research Spike · router: no match"):
            self.assertIsNone(self.run_hook([say(text), READ]), text)

    def test_heading_and_list_forms_pass(self):
        # a heading or a list item carrying the declaration is still one
        for text in ("## Level: L1", "1. Level: L1", "+ Level: L1", "• Level: L1",
                     "### Router verdict: no match", "• router: no match",
                     "2) Level: L2 · router: no match"):
            self.assertIsNone(self.run_hook([say(text), READ]), text)

    def test_edited_file_project_is_judged_from_another_cwd(self):
        # live probe 2026-10-27: the hook runs in the session's current directory,
        # which a `cd` moves -- the project judged is the one holding the file
        with tempfile.TemporaryDirectory() as other:
            (Path(other) / "ai_docs").mkdir()
            self.assertIsNotNone(self.run_hook([say("x")], cwd=other))
            self.assertIsNone(self.run_hook([VERDICT, READ], cwd=other))

    def test_edited_file_docs_root_name_is_its_own(self):
        # the docs root NAME is the edited project's too, not the working directory's
        (self.root / "ai_docs").rename(self.root / "mkt_docs")
        with tempfile.TemporaryDirectory() as other:
            (Path(other) / "ai_docs").mkdir()
            reason = self.run_hook([say("x")], cwd=other)
        self.assertIsNotNone(reason)
        self.assertIn("mkt_docs/reference/INDEX.md", reason)

    def test_reason_echoes_no_transcript_text(self):
        secret = "SECRET-TRANSCRIPT-TEXT-42"
        reason = self.run_hook([say("router: GUIDE_release.md " + secret)])
        self.assertIn(GUIDE, reason, "the unread-guide reason, not the no-verdict one")
        self.assertNotIn(secret, reason)

    # --- satisfied ------------------------------------------------------
    def test_verdict_and_read_passes(self):
        self.assertIsNone(self.run_hook([VERDICT, READ]))

    def test_read_through_bash_counts(self):
        self.assertIsNone(self.run_hook(
            [VERDICT, call("Bash", command="cat ai_docs/reference/" + GUIDE)]))

    def test_read_before_the_verdict_counts(self):
        self.assertIsNone(self.run_hook([READ, VERDICT]))

    def test_no_match_verdict_passes(self):
        self.assertIsNone(self.run_hook([say("Level: L3 · router: no match")]))

    def test_no_match_naming_a_ruled_out_guide_passes(self):
        # SKILL.md: the verdict is "never an excuse to read every guide"
        self.assertIsNone(self.run_hook(
            [say("Level: L2 · router: no match (GUIDE_release.md does not apply)")]))

    def test_markdown_emphasis_forms_pass(self):
        # emphasis around the documented forms is still the declaration
        self.assertIsNone(self.run_hook([say("**Level**: L1")]))
        self.assertIsNone(self.run_hook([say("**router**: no match")]))
        self.assertIsNone(self.run_hook([say("Router verdict: no match")]))
        reason = self.run_hook([say("**Router verdict**: `GUIDE_release.md` -> read")])
        self.assertIn(GUIDE, reason, "the bold form still names its guide")

    def test_trivial_declaration_passes(self):
        self.assertIsNone(self.run_hook([say("Level: L1 — typo.")]))
        self.assertIsNone(self.run_hook([say("Level: **E1**, a one-word fix.")]))

    def test_guide_not_in_project_need_not_be_read(self):
        self.assertIsNone(self.run_hook([say("Level: L2 · router: GUIDE_other.md → read")]))

    def test_an_edit_naming_the_guide_is_not_a_read(self):
        reason = self.run_hook([VERDICT, call("Edit", file_path="ai_docs/reference/" + GUIDE)])
        self.assertIsNotNone(reason)

    # --- F-094: a named guide is read WHOLE, or it is not read ----------------
    def long_guide(self, lines):
        (self.root / "ai_docs" / "reference" / GUIDE).write_text(
            "".join("line %d\n" % i for i in range(1, lines + 1)), encoding="utf-8")
        return "ai_docs/reference/" + GUIDE

    def test_field_case_partial_read_is_refused(self):
        # field: Read offset=1 limit=130 of the 225-line GUIDE_release.md, and the
        # release then ran on the 130 lines it had seen
        path = self.long_guide(225)
        reason = self.run_hook([VERDICT, call("Read", file_path=path, offset=1, limit=130)])
        self.assertIsNotNone(reason)
        self.assertIn(GUIDE, reason)
        self.assertIn("whole", reason)

    def test_an_offset_that_skips_the_start_is_refused(self):
        path = self.long_guide(225)
        self.assertIsNotNone(self.run_hook([VERDICT, call("Read", file_path=path, offset=30)]))

    def test_excerpt_and_search_tools_are_not_reads(self):
        path = self.long_guide(40)
        for block in (call("Bash", command="head -30 " + path),
                      call("Bash", command="sed -n 1,40p " + path),
                      call("Grep", pattern="release", path=path),
                      call("Agent", prompt="read " + path)):
            self.assertIsNotNone(self.run_hook([VERDICT, block]), block)

    def test_a_guide_past_the_read_cap_is_read_in_chunks_to_the_end(self):
        # Claude Code's Read stops at 2000 lines without a limit: a longer guide is
        # read in consecutive chunks, and stopping before the last line is a refusal
        path = self.long_guide(2500)
        self.assertIsNotNone(self.run_hook([VERDICT, call("Read", file_path=path)]))
        self.assertIsNotNone(self.run_hook([VERDICT, call("Read", file_path=path),
                                            call("Read", file_path=path, offset=2001, limit=400)]))
        self.assertIsNotNone(self.run_hook([VERDICT, call("Read", file_path=path),
                                            call("Read", file_path=path, offset=2101)]),
                             "a gap at lines 2001-2100 is not a whole read")
        self.assertIsNone(self.run_hook([VERDICT, call("Read", file_path=path),
                                         call("Read", file_path=path, offset=2001)]))

    def test_whole_reads_by_every_carrier_pass(self):
        path = self.long_guide(225)
        for block in (call("Read", file_path=path), call("Read", file_path=path, limit=225),
                      call("Bash", command="cat " + path),
                      call("PowerShell", command="Get-Content -Raw " + path),
                      call("mcp__devpnt__get_file_content", paths=[path])):
            self.assertIsNone(self.run_hook([VERDICT, block]), block)

    def test_a_read_span_it_cannot_tell_earns_no_credit(self):
        # a non-int offset or limit, or a limit of zero, is not a whole read
        path = self.long_guide(40)
        for inp in ({"offset": "30"}, {"offset": 30.0}, {"limit": 0}, {"limit": -5},
                    {"limit": "2000"}):
            self.assertIsNotNone(self.run_hook([VERDICT, call("Read", file_path=path, **inp)]), inp)

    def test_codex_total_count_short_of_the_end_is_refused(self):
        path = self.long_guide(225)
        meta = json.dumps({"type": "session_meta", "payload": {"cwd": str(self.root)}})

        def read(cmd):
            return json.dumps({"type": "response_item", "payload": {
                "type": "function_call", "name": "exec_command",
                "arguments": json.dumps({"cmd": cmd})}})
        self.assertIsNotNone(self.run_hook(
            [meta, VERDICT, read("Get-Content -TotalCount 100 '%s'" % path)]))
        self.assertIsNone(self.run_hook(
            [meta, VERDICT, read("Get-Content -TotalCount 225 '%s'" % path)]))

    # --- out of scope: silent -------------------------------------------
    def test_project_without_guides_is_silent(self):
        (self.root / "ai_docs" / "reference" / GUIDE).unlink()
        self.assertIsNone(self.run_hook([say("x")]))

    def test_file_outside_project_is_silent(self):
        outside = Path(tempfile.gettempdir()).resolve() / "elsewhere.py"
        self.assertIsNone(self.run_hook([say("x")], target=outside))

    def test_subagent_is_silent(self):
        self.assertIsNone(self.run_hook([say("x")], agent_id="a1"))

    def test_subagent_transcript_is_silent_without_agent_id(self):
        # probed: every assistant entry of a Claude Code subagent transcript carries
        # isSidechain: true, the main transcript none -- whichever path the hook gets
        line = json.loads(say("x"))
        line["isSidechain"] = True
        self.assertIsNone(self.run_hook([json.dumps(line)]))

    def test_non_edit_tool_is_silent(self):
        self.assertIsNone(self.run_hook([say("x")], tool="Bash"))

    # --- fail open --------------------------------------------------------
    def test_garbage_stdin_is_silent(self):
        self.assertIsNone(self.run_hook(raw="not json"))

    def test_missing_transcript_is_silent(self):
        self.assertIsNone(self.run_hook(transcript_path=str(self.root / "nope.jsonl")))

    def test_no_transcript_path_is_silent(self):
        self.assertIsNone(self.run_hook(transcript_path=None))

    def test_unrecognised_format_is_silent(self):
        self.assertIsNone(self.run_hook(['{"kind": "something-else"}', "garbage line"]))

    def test_oversized_transcript_is_silent(self):
        self.transcript.write_text(say("x") + "\n", encoding="utf-8")
        with mock.patch.object(sdlc_core, "VERDICT_MAX_BYTES", 10):
            self.assertIsNone(self.run_hook())

    def test_overlong_line_is_not_parsed(self):
        long_verdict = say("Level: L3 · router: no match" + " " * 64)
        with mock.patch.object(sdlc_core, "VERDICT_LINE_MAX", 32):
            # the only verdict sits on a line over the cap: it is skipped, and with no
            # assistant entry parsed the hook cannot tell -- silent, never a block
            self.assertIsNone(self.run_hook([long_verdict]))

    def test_no_docs_root_is_silent(self):
        import shutil
        shutil.rmtree(self.root / "ai_docs")
        self.assertIsNone(self.run_hook([say("x")]))

    def test_ambiguous_docs_root_is_silent(self):
        (self.root / "mkt_docs").mkdir()
        (self.root / "mkt_docs" / "README.md").write_text("# m\n", encoding="utf-8")
        (self.root / "ai_docs" / "README.md").write_text("# a\n", encoding="utf-8")
        self.assertIsNone(self.run_hook([say("x")]))

    # --- the existing PreToolUse surface keeps its behaviour ----------------
    def test_gate_hook_still_reads_the_shared_payload(self):
        payload = json.dumps({"tool_input": {"file_path": str(self.root / "src" / "a.py")}})
        stdin = io.TextIOWrapper(io.BytesIO(payload.encode("utf-8")), encoding="utf-8")
        err = io.StringIO()
        with mock.patch.object(sys, "stdin", stdin), contextlib.redirect_stderr(err):
            code = sdlc_core.main(["gate", "--hook", "--root", str(self.root),
                                   "--protected", "src"])
        self.assertEqual(code, 2)
        self.assertIn("[sdlc gate]", err.getvalue())

    def test_gate_hook_judges_the_edited_files_project_from_another_cwd(self):
        # the gate shares the verdict hook's resolution: the edited file's project
        payload = json.dumps({"tool_input": {"file_path": str(self.root / "src" / "a.py")}})
        stdin = io.TextIOWrapper(io.BytesIO(payload.encode("utf-8")), encoding="utf-8")
        err = io.StringIO()
        here = os.getcwd()
        with tempfile.TemporaryDirectory() as other:
            (Path(other) / "ai_docs").mkdir()
            with mock.patch.object(sys, "stdin", stdin), contextlib.redirect_stderr(err):
                try:
                    os.chdir(other)
                    code = sdlc_core.main(["gate", "--hook", "--protected", "src"])
                finally:
                    os.chdir(here)
        self.assertEqual(code, 2)
        self.assertIn("[sdlc gate]", err.getvalue())

    def run_gate(self, target, cwd, protected):
        payload = json.dumps({"tool_input": {"file_path": str(target)}})
        stdin = io.TextIOWrapper(io.BytesIO(payload.encode("utf-8")), encoding="utf-8")
        here = os.getcwd()
        with mock.patch.object(sys, "stdin", stdin), \
                contextlib.redirect_stderr(io.StringIO()):
            try:
                os.chdir(cwd)
                return sdlc_core.main(["gate", "--hook", "--protected", protected])
            finally:
                os.chdir(here)

    def test_gate_hook_without_a_docs_root_judges_the_session_project(self):
        # no docs root above the edited file: the project is the session's own, as
        # before the hook resolved from the file -- the protected path stays protected
        import shutil
        shutil.rmtree(self.root / "ai_docs")
        (self.root / "src" / "auth").mkdir()
        target = self.root / "src" / "auth" / "x.py"
        self.assertEqual(self.run_gate(target, self.root, "src/auth"), 2)

    def test_gate_hook_two_docs_roots_is_silent(self):
        # half-migrated project: which root governs cannot be told -- silent, not an error
        (self.root / "mkt_docs").mkdir()
        with tempfile.TemporaryDirectory() as other:
            self.assertEqual(self.run_gate(self.root / "src" / "a.py", other, "src"), 0)

    def test_gate_hook_prefixes_are_relative_to_the_nearest_docs_root(self):
        # ENFORCEMENT.md: with nested docs roots the prefixes are relative to the
        # nearest one above the edited file (a monorepo package with its own)
        pkg = self.root / "packages" / "api"
        (pkg / "ai_docs").mkdir(parents=True)
        (pkg / "src" / "auth").mkdir(parents=True)
        target = pkg / "src" / "auth" / "x.py"
        self.assertEqual(self.run_gate(target, self.root, "src/auth"), 2)
        self.assertEqual(self.run_gate(target, self.root, "packages/api/src/auth"), 0)

    def test_gate_hook_explicit_docs_name_walks_from_the_edited_file(self):
        # an explicit docs root name skips discovery: the project is still the one
        # holding the edited file, not the working directory's
        (self.root / "src" / "auth").mkdir()
        target = self.root / "src" / "auth" / "x.py"
        with tempfile.TemporaryDirectory() as other, \
                mock.patch.dict(os.environ, {sdlc_core.DOCS_DIR_ENV: "ai_docs"}):
            self.assertEqual(self.run_gate(target, other, "src/auth"), 2)

    def test_codex_patch_requires_router(self):
        lines = [json.dumps({"type":"response_item","payload":{"type":"message","role":"assistant","content":[{"type":"output_text","text":"Working."}]}})]
        patch = "*** Begin Patch\n*** Update File: src/a.py\n@@\n-a\n+b\n*** End Patch"

        result = self.run_hook(lines, tool="apply_patch", tool_input={"command":patch})

        self.assertIsNotNone(result)
        self.assertIn("No guide-router verdict", result)

    def test_codex_transcript_and_literal_read_satisfy_router(self):
        def message(text):
            return json.dumps({"type":"response_item","payload":{"type":"message","role":"assistant","content":[{"type":"output_text","text":text}]}})
        metadata = json.dumps({"type":"session_meta","payload":{"cwd":str(self.root)}})
        read = json.dumps({"type":"response_item","payload":{"type":"function_call","name":"exec_command","arguments":json.dumps({"cmd":"Get-Content -LiteralPath 'ai_docs/reference/GUIDE_release.md'"})}})
        patch = "*** Begin Patch\n*** Update File: src/a.py\n@@\n-a\n+b\n*** End Patch"
        lines = [metadata, message("Level: L2 · router: GUIDE_release.md -> read")]

        self.assertIsNotNone(self.run_hook(lines,tool="apply_patch",tool_input={"command":patch}))
        self.assertIsNone(self.run_hook(lines+[read],tool="apply_patch",tool_input={"command":patch}))

    def test_codex_user_text_cannot_declare_router(self):
        self.transcript.write_text(json.dumps({"type":"response_item","payload":{"type":"message","role":"user","content":[{"type":"input_text","text":"Level: L1"}]}}),encoding="utf-8")

        facts = sdlc_core.transcript_facts(self.transcript)

        self.assertFalse(facts["trivial"])


class CodexParsing(unittest.TestCase):
    def test_complete_multifile_patch_and_move_keep_every_target(self):
        with tempfile.TemporaryDirectory() as directory:
            patch = ("*** Begin Patch\n*** Add File: new.py\n+x\n"
                     "*** Update File: old.py\n*** Move to: moved.py\n@@\n-a\n+b\n"
                     "*** Delete File: deleted.py\n*** End Patch")
            edits = sdlc_core.hook_edits({"cwd": directory, "tool_input": {"command": patch}})
            self.assertEqual([Path(x["path"]).name for x in edits],
                             ["new.py", "old.py", "moved.py", "deleted.py"])

    def test_unknown_or_incomplete_patch_never_returns_partial_targets(self):
        for tail in ["*** Unknown File: b.py\n*** End Patch", "", "*** Update File: b.py\n*** End Patch"]:
            patch = "*** Begin Patch\n*** Add File: a.py\n+x\n" + tail
            self.assertIsNone(sdlc_core.hook_edits({"cwd": tempfile.gettempdir(), "tool_input": {"command": patch}}))

    def test_read_hint_preserves_unicode_and_historical_workdir(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = sdlc_core.shell_read_paths("Get-Content -LiteralPath 'GUIDE_à.md'", directory, "nested")
            self.assertEqual(paths, [str((Path(directory) / "nested/GUIDE_à.md").resolve())])
            self.assertIsNone(sdlc_core.shell_read_paths("cat GUIDE_x.md", None))

    def test_dynamic_shell_and_unknown_js_are_never_read_hints(self):
        for command in ["cat $guide", "Get-Content a.md; whoami", "cat *.md", "cat a.md | more"]:
            self.assertIsNone(sdlc_core.shell_read_paths(command, tempfile.gettempdir()))
        self.assertEqual(sdlc_core._codex_literal_calls('const p = "a"; await tools.exec_command({cmd:p});'), [])


if __name__ == "__main__":
    unittest.main()
