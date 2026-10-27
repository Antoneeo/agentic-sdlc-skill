#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-085 -- the constraint reader and `constraints --unit/--file`.

The agent's own unit already states its constraints; what was missing is the
synthesis at the moment of action. These tests pin what the reader extracts from
an ANALYSIS (id'd use cases, spec items and threats, and the rows of the
`### Preservation constraints` table), how a file is bound to them, and the two
command forms: the view of a unit (FS4) and the recall query for a file (FS5).
The view never counts, ranks or marks anything, and always ends with the one
sentence that names what it could not extract.

Standard library only.
"""
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_core  # noqa: E402

HERE = Path(__file__).resolve().parent
# the distribution's entry point, whatever it is called (entry_point.py)
ENTRY = next(HERE / (n + ".py") for n in ("sdlc_check", "mkt_check")
             if (HERE / (n + ".py")).is_file())

DOC = """\
---
id: F-901
feature: Fixture
status: IN_PROGRESS
level: L3
domain: code
---
# Feature Analysis: fixture

## Use Cases / User Needs

- **UC1 (Agent)** — edits `src/app/core.py` and sees the bound rules. A second sentence.
- UC2 plain id, no bold. Second names `templates.md`.
  continuation names `src/app/extra.py`.

Grounding: prose without an id.

## Functional Spec

- **FS1 Ids.** Each item starts with its id, as `sdlc_check.py constraints` shows.
### FS2 Heading item
The body sentence of the heading item. More.
| FS3 | a table row item. | x |
- **FS1 Duplicate.** Same id again.

## Interface Contract

- Command: prose, no ids.

## Impact

| File | Change | Why |
|---|---|---|
| `src/app/core.py` | MODIFY | FS1, T1 |
| `src/app/range.py` | ADD | FS2–FS3 |
| `src/*/glob.py` | MODIFY | FS1 |

### Preservation constraints

| id | bound to | callers | must stay true | evidence |
|---|---|---|---|---|
| P1 | `src/app/core.py::Store.save` | `api.py` | save keeps writing one row | grep save |
| P2 | `src/.../elided.py` | none outside the file | nothing bound here | grep |
| P3 | `src/app/old.py` | none outside the file | RELEASED (REQUEST_fixture.md#R4) old rule | probe |

## Security and Threat Model

- **T1 Injection.** Input reaches the shell. Mitigated.
"""


def write(root, rel, text):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def run(root, *args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = sdlc_core.main(["constraints", "--root", str(root), *args])
    return code, buf.getvalue()


def by_id(items):
    out = {}
    for c in items:
        out.setdefault(c["id"], []).append(c)
    return out


class Parse(unittest.TestCase):
    """FS1-FS3: what the reader extracts from one ANALYSIS."""

    def setUp(self):
        self.items = by_id(sdlc_core.parse_constraints(DOC))

    def test_ids_in_bullets_headings_and_table_rows(self):
        for cid in ("UC1", "UC2", "FS1", "FS2", "FS3", "T1", "P1", "P2", "P3"):
            self.assertIn(cid, self.items, cid)

    def test_statement_is_the_first_sentence_verbatim_with_bold_title(self):
        self.assertEqual(self.items["UC1"][0]["statement"],
                         "**UC1 (Agent)** — edits `src/app/core.py` and sees the bound rules.")
        self.assertEqual(self.items["UC2"][0]["statement"], "UC2 plain id, no bold.")

    def test_a_dot_inside_backticks_does_not_end_the_sentence(self):
        self.assertEqual(self.items["FS1"][0]["statement"],
                         "**FS1 Ids.** Each item starts with its id, as "
                         "`sdlc_check.py constraints` shows.")

    def test_heading_item_takes_title_and_first_body_sentence(self):
        st = self.items["FS2"][0]["statement"]
        self.assertTrue(st.startswith("FS2 Heading item"), st)
        self.assertIn("The body sentence of the heading item.", st)
        self.assertNotIn("More.", st)

    def test_duplicated_id_kept_at_each_home(self):
        homes = [c["line"] for c in self.items["FS1"]]
        self.assertEqual(len(homes), 2)
        self.assertNotEqual(homes[0], homes[1])

    def test_line_is_the_item_line_in_the_file(self):
        lines = DOC.splitlines()
        for cid, cs in self.items.items():
            for c in cs:
                self.assertIn(cid, lines[c["line"] - 1], (cid, c["line"]))

    def test_section_is_the_home_heading(self):
        self.assertEqual(self.items["UC1"][0]["section"], "## Use Cases / User Needs")
        self.assertEqual(self.items["T1"][0]["section"], "## Security and Threat Model")
        self.assertEqual(self.items["P1"][0]["section"], "## Impact")

    def test_item_binding_from_full_paths_in_its_text(self):
        self.assertIn("src/app/core.py", self.items["UC1"][0]["bindings"])
        # continuation lines belong to the item
        self.assertIn("src/app/extra.py", self.items["UC2"][0]["bindings"])

    def test_a_bare_file_name_in_prose_binds_nothing(self):
        self.assertEqual(self.items["UC2"][0]["bindings"], {"src/app/extra.py"})

    def test_impact_rows_bind_the_ids_they_cite_ranges_included(self):
        self.assertIn("src/app/core.py", self.items["FS1"][0]["bindings"])
        self.assertIn("src/app/core.py", self.items["T1"][0]["bindings"])
        self.assertIn("src/app/range.py", self.items["FS2"][0]["bindings"])
        self.assertIn("src/app/range.py", self.items["FS3"][0]["bindings"])

    def test_a_glob_path_binds_nothing(self):
        for cs in self.items.values():
            for c in cs:
                self.assertFalse(any("*" in b for b in c["bindings"]), c)

    def test_p_row_statement_binding_and_evidence(self):
        p1 = self.items["P1"][0]
        self.assertEqual(p1["kind"], "P")
        self.assertEqual(p1["statement"], "save keeps writing one row")
        self.assertEqual(p1["bindings"], {"src/app/core.py"})
        self.assertEqual(p1["evidence"], "grep save")
        self.assertIsNone(p1["released"])

    def test_elided_path_binds_nothing(self):
        self.assertEqual(self.items["P2"][0]["bindings"], set())

    def test_released_row(self):
        self.assertEqual(self.items["P3"][0]["released"], "REQUEST_fixture.md#R4")

    def test_prose_and_interface_contract_are_not_items(self):
        for cs in self.items.values():
            for c in cs:
                self.assertNotIn("Grounding", c["statement"])
                self.assertNotIn("Command: prose", c["statement"])


class ReadInFull(unittest.TestCase):
    """FS4's fixed sentence names what the view could not extract."""

    def names(self, text):
        return sdlc_core.unread_sections(text)

    def test_interface_contract_always_named(self):
        self.assertEqual(self.names(DOC), ["## Interface Contract"])

    def test_section_with_prose_and_no_item_is_named(self):
        doc = DOC.replace("- **T1 Injection.** Input reaches the shell. Mitigated.",
                          "Surfaces: none worth a threat.")
        self.assertIn("## Security and Threat Model", self.names(doc))

    def test_impact_without_table_or_no_symbol_line_is_named(self):
        doc = DOC.split("### Preservation constraints")[0] + \
            "## Security and Threat Model\n\n- **T1 X.** y.\n"
        self.assertIn("## Impact", self.names(doc))
        doc2 = doc.replace("## Security", "No existing symbol changed.\n\n## Security")
        self.assertNotIn("## Impact", self.names(doc2))

    def test_complete_document_names_nothing(self):
        doc = DOC.replace("## Interface Contract\n\n- Command: prose, no ids.\n\n", "")
        self.assertEqual(self.names(doc), [])


class Tree(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        write(self.root, "ai_docs/README.md", "# r\n")
        write(self.root, "ai_docs/solutions/ANALYSIS_fixture.md", DOC)

    def tearDown(self):
        self._tmp.cleanup()


class View(Tree):
    """FS4 -- `constraints --unit`."""

    def test_by_id_and_by_name(self):
        for unit in ("F-901", "ANALYSIS_fixture.md", "ANALYSIS_fixture"):
            code, out = run(self.root, "--unit", unit)
            self.assertEqual(code, 0, unit)
            self.assertIn("UC1", out)

    def test_line_format_home_and_document_order(self):
        code, out = run(self.root, "--unit", "F-901")
        lines = out.splitlines()
        uc1 = next(x for x in lines if x.startswith("UC1 — "))
        self.assertRegex(uc1, r" — solutions/ANALYSIS_fixture\.md:\d+$")
        order = [x.split(" — ")[0] for x in lines if re.match(r"^(UC|FS|T|P)\d+ — ", x)]
        self.assertEqual(order, ["UC1", "UC2", "FS1", "FS2", "FS3", "FS1",
                                 "P1", "P2", "P3", "T1"])

    def test_grouped_under_home_headings(self):
        _, out = run(self.root, "--unit", "F-901")
        heads = [x for x in out.splitlines() if x.startswith("## ")]
        self.assertEqual(heads, ["## Use Cases / User Needs", "## Functional Spec",
                                 "## Impact", "## Security and Threat Model"])

    def test_p_line_followed_by_evidence_and_release_shown(self):
        _, out = run(self.root, "--unit", "F-901")
        lines = out.splitlines()
        i = next(n for n, x in enumerate(lines) if x.startswith("P1 — "))
        self.assertEqual(lines[i + 1].strip(), "evidence: grep save")
        self.assertIn("RELEASED (REQUEST_fixture.md#R4)",
                      next(x for x in lines if x.startswith("P3 — ")))

    def test_ends_with_the_fixed_sentence_naming_interface_contract(self):
        _, out = run(self.root, "--unit", "F-901")
        last = out.strip().splitlines()[-1]
        self.assertTrue(last.startswith(sdlc_core.CONSTRAINTS_SENTENCE), last)
        self.assertIn("## Interface Contract", last)

    def test_no_count_share_or_rank(self):
        _, out = run(self.root, "--unit", "F-901")
        for line in out.splitlines():
            stripped = re.sub(r"\b(?:UC|FS|T|P|R)\d+\b|\.md:\d+|F-\d+", "", line)
            self.assertNotRegex(stripped, r"\d", line)

    def test_unknown_unit_one_error_line_exit_1(self):
        code, out = run(self.root, "--unit", "F-999")
        self.assertEqual(code, 1)
        self.assertEqual(len(out.strip().splitlines()), 1, out)

    def test_overlay_forwards_the_command(self):
        # P3: no lens's overlay intercepts `constraints`; each hands it to the core.
        r = subprocess.run([sys.executable, str(ENTRY), "constraints", "--root",
                            str(self.root), "--docs-dir", "ai_docs", "--unit", "F-901"],
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("UC1 — ", r.stdout)


class Recall(Tree):
    """FS5 -- `constraints --file`."""

    def test_bound_file_prints_unit_lines_and_sentence(self):
        code, out = run(self.root, "--file", str(self.root / "src/app/core.py"))
        self.assertEqual(code, 0)
        ids = [x.split(" — ")[0] for x in out.splitlines() if re.match(r"^(UC|FS|T|P)\d+ — ", x)]
        self.assertEqual(ids, ["UC1", "FS1", "FS1", "P1", "T1"])  # both FS1 homes
        self.assertIn("F-901", out.splitlines()[0])
        self.assertTrue(out.strip().splitlines()[-1].startswith(sdlc_core.CONSTRAINTS_SENTENCE))

    def test_backslash_path(self):
        _, a = run(self.root, "--file", str(self.root / "src/app/core.py"))
        _, b = run(self.root, "--file", str(self.root) + "\\src\\app\\core.py")
        self.assertEqual(a, b)

    def test_nothing_bound_prints_nothing(self):
        code, out = run(self.root, "--file", str(self.root / "src/app/unbound.py"))
        self.assertEqual((code, out), (0, ""))

    def test_released_constraint_not_recalled(self):
        _, out = run(self.root, "--file", str(self.root / "src/app/old.py"))
        self.assertEqual(out, "")

    def test_outside_the_project_prints_nothing(self):
        with tempfile.TemporaryDirectory() as other:
            _, out = run(self.root, "--file", str(Path(other) / "src/app/core.py"))
        self.assertEqual(out, "")

    def test_only_open_l3_code_units(self):
        cases = {
            "closed": DOC.replace("status: IN_PROGRESS", "status: COMPLETED"),
            "l2": DOC.replace("level: L3", "level: L2"),
            "knowledge": DOC.replace("domain: code", "domain: knowledge"),
        }
        for name, text in cases.items():
            write(self.root, "ai_docs/solutions/ANALYSIS_fixture.md", text)
            _, out = run(self.root, "--file", str(self.root / "src/app/core.py"))
            self.assertEqual(out, "", name)

    def test_planned_unit_recalled(self):
        write(self.root, "ai_docs/solutions/ANALYSIS_fixture.md",
              DOC.replace("status: IN_PROGRESS", "status: PLANNED"))
        _, out = run(self.root, "--file", str(self.root / "src/app/core.py"))
        self.assertIn("P1 — ", out)

    @unittest.skipUnless(os.name == "nt", "case-insensitive paths are a Windows rule")
    def test_case_insensitive_on_windows(self):
        _, out = run(self.root, "--file", str(self.root / "SRC/App/Core.py"))
        self.assertIn("P1 — ", out)

    def test_open_units_unchanged(self):
        # P1: the reader uses `_open_units`, never changes what it returns.
        self.assertEqual(sdlc_core._open_units(self.root), {"F-901": {"ANALYSIS_fixture.md"}})


def assistant(block, **extra):
    entry = {"type": "assistant", "message": {"role": "assistant", "content": [block]}}
    entry.update(extra)
    return json.dumps(entry)


def say(text, **extra):
    return assistant({"type": "text", "text": text}, **extra)


def call(name, **inp):
    return assistant({"type": "tool_use", "id": "toolu_x", "name": name, "input": inp})


class Hook(Tree):
    """FS6 -- `constraints --hook`: silent unless every condition holds; context
    only, never a permission decision."""

    L3 = say("Level: L3 · router: no match")

    def setUp(self):
        super().setUp()
        self.root = self.root.resolve()
        self.analysis = self.root / "ai_docs/solutions/ANALYSIS_fixture.md"
        self.transcript = self.root / "t.jsonl"
        self.target = self.root / "src/app/core.py"

    def read_unit(self, path=None):
        return call("Read", file_path=str(path or self.analysis))

    def run_hook(self, lines=None, tool="Edit", target=None, raw=None, args=(), cwd=None,
                 **extra):
        if lines is not None:
            self.transcript.write_text("\n".join(lines) + "\n", encoding="utf-8")
        tool_input = {"file_path": str(target or self.target), "old_string": "a",
                      "new_string": "b"}
        tool_input.update(extra.pop("tool_input", {}))
        payload = {"session_id": "s", "transcript_path": str(self.transcript),
                   "cwd": str(cwd or self.root), "hook_event_name": "PreToolUse",
                   "tool_name": tool, "tool_input": tool_input}
        payload.update(extra)
        data = raw if raw is not None else json.dumps(payload)
        stdin = io.TextIOWrapper(io.BytesIO(data.encode("utf-8")), encoding="utf-8")
        out = io.StringIO()
        old = os.getcwd()
        try:
            if cwd:
                os.chdir(cwd)
            with mock.patch.object(sys, "stdin", stdin), contextlib.redirect_stdout(out):
                try:
                    code = sdlc_core.main(["constraints", "--hook", *args])
                except SystemExit as e:  # pragma: no cover - argparse must never fire
                    code = e.code
        finally:
            os.chdir(old)
        self.assertEqual(code, 0, "the hook always exits 0: exit 2 blocks the edit")
        text = out.getvalue()
        if not text.strip():
            return None
        hso = json.loads(text)["hookSpecificOutput"]
        self.assertEqual(set(hso), {"hookEventName", "additionalContext"},
                         "context only: never a permission decision (T1, P6)")
        self.assertEqual(hso["hookEventName"], "PreToolUse")
        return hso["additionalContext"]

    # --- recalls ---------------------------------------------------------
    def test_all_conditions_hold_recalls_the_bound_constraints(self):
        ctx = self.run_hook([self.L3, self.read_unit()])
        self.assertIsNotNone(ctx)
        self.assertIn("P1 — save keeps writing one row", ctx)
        self.assertIn("F-901", ctx)
        self.assertTrue(ctx.strip().splitlines()[-1].startswith(sdlc_core.CONSTRAINTS_SENTENCE))

    def test_root_comes_from_the_edited_file_not_the_working_directory(self):
        # live probe 2026-10-27: the hook runs in the session's current directory
        with tempfile.TemporaryDirectory() as elsewhere:
            ctx = self.run_hook([self.L3, self.read_unit()], cwd=elsewhere)
        self.assertIsNotNone(ctx)

    def test_every_edit_tool(self):
        for tool in sdlc_core.VERDICT_EDIT_TOOLS:
            self.assertIsNotNone(self.run_hook([self.L3, self.read_unit()], tool=tool), tool)

    def test_reading_the_request_record_or_handoff_counts(self):
        write(self.root, "ai_docs/audit/requests/REQUEST_fixture.md",
              "---\nunit: F-901\nanalysis: ANALYSIS_fixture.md\n---\n# r\n")
        write(self.root, "ai_docs/audit/HANDOFF_fixture.md", "---\nworkstream: F-901\n---\n")
        for rel in ("ai_docs/audit/requests/REQUEST_fixture.md",
                    "ai_docs/audit/HANDOFF_fixture.md"):
            self.assertIsNotNone(self.run_hook([self.L3, self.read_unit(self.root / rel)]), rel)

    def test_italian_l3_declaration_counts(self):
        self.assertIsNotNone(self.run_hook([say("Livello L3 · router: nessun match"),
                                            self.read_unit()]))

    def test_uc6_editing_the_analysis_with_a_bound_path(self):
        ctx = self.run_hook([self.L3, self.read_unit()], target=self.analysis,
                            tool_input={"new_string": "now `src/app/core.py` also logs"})
        self.assertIn("P1 — ", ctx)
        self.assertIsNone(self.run_hook([self.L3, self.read_unit()], target=self.analysis,
                                        tool_input={"new_string": "names `src/app/other.py`"}))

    def test_uc6_write_and_multiedit_texts(self):
        self.assertIsNotNone(self.run_hook(
            [self.L3, self.read_unit()], tool="Write", target=self.analysis,
            tool_input={"content": "`src/app/core.py`"}))
        self.assertIsNotNone(self.run_hook(
            [self.L3, self.read_unit()], tool="MultiEdit", target=self.analysis,
            tool_input={"edits": [{"old_string": "a", "new_string": "`src/app/core.py`"}]}))

    def test_at_most_fifteen_lines_then_the_unit_command(self):
        rows = "".join(f"| P{n} | `src/app/core.py` | none | rule {chr(97 + n % 26)} | ev |\n"
                       for n in range(4, 30))
        write(self.root, "ai_docs/solutions/ANALYSIS_fixture.md",
              DOC.replace("| P3 |", rows + "| P3 |"))
        ctx = self.run_hook([self.L3, self.read_unit()])
        body = [x for x in ctx.splitlines()
                if re.match(r"^(?:(?:UC|FS|T|P)\d+ — |    evidence: )", x)]
        self.assertEqual(len(body), 15)
        self.assertIn("constraints --unit F-901", ctx)

    def test_lines_are_clipped_and_stripped_of_control_characters(self):
        long_rule = "x" * 400 + "\x07"
        write(self.root, "ai_docs/solutions/ANALYSIS_fixture.md",
              DOC.replace("save keeps writing one row", long_rule))
        ctx = self.run_hook([self.L3, self.read_unit()])
        self.assertNotIn("\x07", ctx)
        self.assertTrue(all(len(x) <= sdlc_core.CONSTRAINT_LINE_MAX for x in ctx.splitlines()))

    def test_docs_root_name_comes_from_the_edited_file(self):
        # closure review W3: the session's directory may hold another docs root, or two
        with tempfile.TemporaryDirectory() as elsewhere:
            (Path(elsewhere) / "mkt_docs").mkdir()
            self.assertIsNotNone(self.run_hook([self.L3, self.read_unit()], cwd=elsewhere))
            (Path(elsewhere) / "ai_docs").mkdir()   # now ambiguous where the session sits
            self.assertIsNotNone(self.run_hook([self.L3, self.read_unit()], cwd=elsewhere))

    def test_fifteen_lines_per_recall_across_units_and_evidence_kept(self):
        # closure review W4: the bound is per recall, and a P line keeps its evidence
        rows = "".join(f"| P{n} | `src/app/core.py` | none | rule {chr(97 + n % 26)} | ev |\n"
                       for n in range(4, 12))
        doc = DOC.replace("| P3 |", rows + "| P3 |")
        other = self.root / "ai_docs/solutions/ANALYSIS_other.md"
        write(self.root, "ai_docs/solutions/ANALYSIS_fixture.md", doc)
        write(self.root, "ai_docs/solutions/ANALYSIS_other.md", doc.replace("F-901", "F-902"))
        ctx = self.run_hook([self.L3, self.read_unit(), self.read_unit(other)])
        lines = ctx.splitlines()
        body = [x for x in lines if re.match(r"^(?:(?:UC|FS|T|P)\d+ — |    evidence: )", x)]
        self.assertLessEqual(len(body), sdlc_core.CONSTRAINTS_HOOK_LINES)
        for i, x in enumerate(lines):
            if re.match(r"^P\d+ — ", x):
                self.assertTrue(lines[i + 1].startswith("    evidence: "), x)
        self.assertIn("constraints --unit F-902", ctx)

    def test_a_level_word_alone_on_its_line_is_not_a_declaration(self):
        self.assertIsNotNone(self.run_hook([self.L3, self.read_unit(),
                                            say("Level\nL1 is the trivial tier.")]))

    def test_an_em_dash_separator_is_accepted(self):
        self.assertIsNotNone(self.run_hook([say("Level — L3 · router: no match"),
                                            self.read_unit()]))

    # --- silence ---------------------------------------------------------
    def test_silent_when_the_session_never_touched_the_unit(self):
        self.assertIsNone(self.run_hook([self.L3]))

    def test_a_search_mentioning_the_unit_does_not_count(self):
        self.assertIsNone(self.run_hook([self.L3, call("Grep", pattern="ANALYSIS_fixture.md")]))

    def test_silent_when_the_last_declaration_is_l1(self):
        self.assertIsNone(self.run_hook([self.L3, self.read_unit(), say("Level: L1")]))

    def test_silent_on_l2(self):
        self.assertIsNone(self.run_hook([say("Level: L2 · router: no match"), self.read_unit()]))

    def test_a_level_quoted_in_prose_is_not_a_declaration(self):
        self.assertIsNone(self.run_hook([say('the hook reads "Level: L3 · router: x" lines'),
                                         self.read_unit()]))
        # and does not silence an earlier L3 either
        self.assertIsNotNone(self.run_hook([self.L3, self.read_unit(),
                                            say('a quoted "Level: L1" in a sentence')]))

    def test_silent_for_a_subagent(self):
        self.assertIsNone(self.run_hook([self.L3, self.read_unit()], agent_id="a1"))
        self.assertIsNone(self.run_hook([say("Level: L3 · router: no match", isSidechain=True),
                                         self.read_unit()]))

    def test_silent_on_an_oversized_or_unreadable_transcript(self):
        self.transcript.write_text(self.L3 + "\n" + self.read_unit() + "\n", encoding="utf-8")
        with mock.patch.object(sdlc_core, "VERDICT_MAX_BYTES", 10):
            self.assertIsNone(self.run_hook())
        self.assertIsNone(self.run_hook(transcript_path=str(self.root / "missing.jsonl")))

    def test_silent_on_an_unbound_file_a_closed_unit_or_another_domain(self):
        lines = [self.L3, self.read_unit()]
        self.assertIsNone(self.run_hook(lines, target=self.root / "src/app/free.py"))
        for text in (DOC.replace("status: IN_PROGRESS", "status: COMPLETED"),
                     DOC.replace("domain: code", "domain: knowledge")):
            write(self.root, "ai_docs/solutions/ANALYSIS_fixture.md", text)
            self.assertIsNone(self.run_hook(lines))

    def test_silent_outside_a_project_and_on_a_non_edit_tool(self):
        with tempfile.TemporaryDirectory() as other:
            self.assertIsNone(self.run_hook([self.L3, self.read_unit()],
                                            target=Path(other) / "src/app/core.py"))
        self.assertIsNone(self.run_hook([self.L3, self.read_unit()], tool="Bash"))

    def test_silent_on_malformed_input(self):
        for raw in ("", "not json", "[]", '{"tool_name": "Edit"}'):
            self.assertIsNone(self.run_hook(raw=raw), raw)

    # --- the transcript reader --------------------------------------------
    def test_transcript_work_reports_level_and_touched_files(self):
        self.transcript.write_text("\n".join([self.L3, self.read_unit()]) + "\n",
                                   encoding="utf-8")
        work = sdlc_core.transcript_work(self.transcript)
        self.assertEqual(work["level"], "3")
        self.assertFalse(work["sidechain"])
        self.assertIn(sdlc_core._norm_rel(str(self.analysis)), work["touched"])

    def test_transcript_facts_is_unchanged(self):
        # P2: the verdict hook's reader keeps its keys
        self.transcript.write_text(self.L3 + "\n", encoding="utf-8")
        self.assertEqual(set(sdlc_core.transcript_facts(self.transcript)),
                         {"assistant", "sidechain", "declared", "trivial", "named", "read"})


NO_TABLE = DOC.split("### Preservation constraints")[0] + \
    "## Security and Threat Model\n\n- **T1 X.** y.\n"


class Advisory(Tree):
    """FS7 -- `validate` notes an open L3 code ANALYSIS with no preservation
    record; never an error, never a change to `--strict`, never another domain,
    and never in a lens that does not claim the capability (R12: code lens only)."""

    def setUp(self):
        super().setUp()
        import entry_point
        entry_point.load()  # registers this distribution's profile
        if not sdlc_core.has_capability("preservation_constraints"):
            self.skipTest("this lens does not claim 'preservation_constraints'")

    def validate(self, strict=False):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = sdlc_core.cmd_validate(self.root, strict=strict)
        notes = [x for x in out.getvalue().splitlines()
                 if x.startswith("[note]") and "Preservation constraints" in x]
        return code, notes, out.getvalue()

    def test_open_l3_code_without_table_gets_one_note(self):
        write(self.root, "ai_docs/solutions/ANALYSIS_fixture.md", NO_TABLE)
        _, notes, _ = self.validate()
        self.assertEqual(len(notes), 1, notes)
        self.assertIn("ANALYSIS_fixture.md", notes[0])

    def test_table_or_no_symbol_line_satisfies_it(self):
        _, notes, _ = self.validate()
        self.assertEqual(notes, [])
        write(self.root, "ai_docs/solutions/ANALYSIS_fixture.md",
              NO_TABLE.replace("## Security", "No existing symbol changed.\n\n## Security"))
        _, notes, _ = self.validate()
        self.assertEqual(notes, [])

    def test_closed_lower_level_and_other_domains_are_not_checked(self):
        for name, text in {
            "closed": NO_TABLE.replace("status: IN_PROGRESS", "status: COMPLETED\nend_date: 2026-10-27"),
            "l2": NO_TABLE.replace("level: L3", "level: L2"),
            "knowledge": NO_TABLE.replace("domain: code", "domain: knowledge"),
            "course": NO_TABLE.replace("domain: code", "domain: course"),
        }.items():
            write(self.root, "ai_docs/solutions/ANALYSIS_fixture.md", text)
            _, notes, _ = self.validate()
            self.assertEqual(notes, [], name)

    def test_a_lens_without_the_capability_sees_no_note(self):
        write(self.root, "ai_docs/solutions/ANALYSIS_fixture.md", NO_TABLE)
        caps = sdlc_core.profile()["capabilities"] - {"preservation_constraints"}
        with mock.patch.dict(sdlc_core._PROFILE, capabilities=caps):
            _, notes, _ = self.validate()
        self.assertEqual(notes, [])

    def test_never_an_error_and_strict_exit_unchanged(self):
        with_table = self.validate(strict=True)[0]
        write(self.root, "ai_docs/solutions/ANALYSIS_fixture.md", NO_TABLE)
        code, notes, out = self.validate(strict=True)
        self.assertEqual(len(notes), 1)
        self.assertEqual(code, with_table, "the note never changes --strict (P5)")
        self.assertNotIn("Preservation constraints", "\n".join(
            x for x in out.splitlines() if x.startswith(("[ERROR]", "[warn]"))))


LOG_HEAD = ("# Independent Review Log\n\n"
            "| date | doc_key | tier | model | reviewer | findings_raised | "
            "findings_real | verdict | revise_rounds |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
            "| 2026-10-18 | ANALYSIS_x.md | design | deep | subagent | 3 | 2 | FAIL | 2 |\n"
            "| 2026-10-19 | ANALYSIS_x.md | closure | deep | subagent | 1 | 1 | PASS | 1 |\n"
            "| 2026-10-20 | ANALYSIS_y.md | code | deep | subagent | 2 | 1 | PASS | 1 |\n")
POST_MERGE = ("| 2026-10-27 | ANALYSIS_x.md | post-merge | none (owner report) | owner "
              "| 1 | 1 | DEFECT: \"the list loses the last row\" | 0 |\n")


class Benefit(unittest.TestCase):
    """FS10 -- a `post-merge` row is a defect report, not a review: `benefit`
    keeps every review figure as it is (P8)."""

    def benefit(self, log):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p = root / sdlc_core.review_log_rel()
            p.parent.mkdir(parents=True)
            p.write_text(log, encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = sdlc_core.cmd_benefit(root)
        return code, out.getvalue()

    def test_post_merge_row_changes_no_review_figure(self):
        _, before = self.benefit(LOG_HEAD)
        code, after = self.benefit(LOG_HEAD + POST_MERGE)
        self.assertEqual(code, 0)
        added = [x for x in after.splitlines() if x not in before.splitlines()]
        removed = [x for x in before.splitlines() if x not in after.splitlines()]
        # only the parse count and one line naming the defect reports differ
        self.assertEqual(len(added), 2, added)
        self.assertEqual(len(removed), 1, removed)
        self.assertTrue(removed[0].startswith("rows parsed: 3"), removed)
        self.assertTrue(any(x.startswith("rows parsed: 4") for x in added), added)
        self.assertTrue(any("post-merge" in x and ": 1" in x for x in added), added)

    def test_post_merge_is_not_an_unstated_moment(self):
        _, after = self.benefit(LOG_HEAD + POST_MERGE)
        self.assertIn("moment not stated by `tier`: 1  (code x1)", after)

    def test_log_without_post_merge_prints_no_defect_line(self):
        _, before = self.benefit(LOG_HEAD)
        self.assertNotIn("post-merge", before)


if __name__ == "__main__":
    unittest.main()
