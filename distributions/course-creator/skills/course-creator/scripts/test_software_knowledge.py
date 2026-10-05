"""F-064/F-063: typed claims and reproducible software evidence, real engine."""
import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import knowledge as kb


class SoftwareEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        self.docs = self.project / "ai_docs"
        self.docs.mkdir()
        (self.docs / "README.md").write_text("# Project knowledge\n", encoding="utf-8")

    def table(self, kinds=("OBSERVATION",), schema=2, states=None, sources=None):
        columns = kb.CLAIM_COLUMNS + (("kind",) if schema == 2 else ())
        rows = ["---", "topic: behavior", "parents: []", "owns: [behavior/fact]",
                "claim_schema: %s" % schema, "---", "## Claims",
                "| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
        ids = []
        for i, kind in enumerate(kinds):
            source = (sources[i] if sources else "corpus/given/facts.txt#L%d-%d" % (i+1, i+1))
            path, loc = source.split(";")[0].strip().rsplit("#", 1)
            cid = kb.kb_claim_id(path, loc)
            ids.append(cid)
            cells = [cid, "Fact %d" % i, "-", "-", "-", source, "GIVEN", states[i] if states else "OK"]
            if schema == 2:
                cells.append(kind)
            rows.append("| " + " | ".join(cells) + " |")
        return "\n".join(rows) + "\n", ids

    def ledger(self, **kwargs):
        (self.docs / "topics").mkdir(exist_ok=True)
        (self.docs / "corpus/given").mkdir(parents=True, exist_ok=True)
        (self.docs / "corpus/given/facts.txt").write_text("fact\n" * 10, encoding="utf-8")
        text, ids = self.table(**kwargs)
        (self.docs / "topics/behavior.md").write_text(text, encoding="utf-8")
        return text, ids

    def test_e1_legacy_keys_and_ids_remain_unchanged(self):
        legacy, ids = self.table(schema=1)
        typed, typed_ids = self.table()
        rows, errors = kb.kb_parse_claims(legacy)
        self.assertEqual(errors, [])
        self.assertEqual(set(rows[0]), set(kb.CLAIM_COLUMNS) | {"_line"})
        self.assertEqual(ids, typed_ids)
        typed_rows, errors = kb.kb_parse_claims(typed)
        self.assertEqual(errors, [])
        self.assertEqual(typed_rows[0]["kind"], "OBSERVATION")
        self.assertEqual(kb.CLAIM_COLUMNS, ("id", "claim", "valid", "qty", "about", "source", "prov", "state"))

    def test_e1_all_kinds_and_strict_arity(self):
        text, _ = self.table(kinds=("OBSERVATION", "REQUIREMENT", "HYPOTHESIS", "DESIGN"))
        rows, errors = kb.kb_parse_claims(text)
        self.assertEqual(errors, [])
        self.assertEqual(len(rows), 4)
        for bad in (text.replace(" | DESIGN |", " |"), text.replace(" | DESIGN |", " | DESIGN | extra |")):
            self.assertTrue(kb.kb_parse_claims(bad)[1])
        self.ledger(kinds=("GUESS",))
        self.assertTrue(any("kind" in e for e in kb.kb_check_claims(self.docs)[0]))

    def test_e1_schema2_requires_typed_header_even_when_empty(self):
        text, _ = self.ledger(schema=1, kinds=())
        path = self.docs / "topics/behavior.md"
        path.write_text(text.replace("claim_schema: 1", "claim_schema: 2"), encoding="utf-8")
        self.assertTrue(any("schema" in e for e in kb.kb_check_claims(self.docs)[0]))
        path.write_text(text.replace("claim_schema: 1", "claim_schema: 3"), encoding="utf-8")
        self.assertTrue(any("schema" in e for e in kb.kb_check_claims(self.docs)[0]))

    def test_e1_cross_kind_relations_rejected_coexistence_allowed(self):
        _, ids = self.ledger(kinds=("REQUIREMENT", "OBSERVATION"))
        self.assertEqual(kb.kb_check_claims(self.docs)[0], [])
        for states in (("SUPERSEDED " + ids[1], "OK"),
                       ("CONTESTED " + ids[1], "CONTESTED " + ids[0])):
            self.ledger(kinds=("REQUIREMENT", "OBSERVATION"), states=states)
            self.assertTrue(any("kind" in e for e in kb.kb_check_claims(self.docs)[0]))

    def capture(self, rel="src.py", data=b"first\r\nsecond\r\nthird\r\n", start=2, end=2, role="code", derived_from=()):
        path = self.project / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return kb.kb_capture_source(self.project, self.docs, rel, start, end, role, derived_from)

    def test_e2_exact_bytes_binding_and_idempotence(self):
        rel, side, created = self.capture()
        self.assertTrue(created)
        self.assertEqual((self.docs / rel).read_bytes(), b"second\r\n")
        meta = kb.load_frontmatter((self.docs / side).read_text().splitlines())
        self.assertEqual(meta["software_sha256"], hashlib.sha256((self.project / "src.py").read_bytes()).hexdigest())
        self.assertEqual(meta["software_lines"], "2-2")
        self.assertNotIn("extracted_through", meta)
        self.assertNotIn("original_path", meta)
        self.assertEqual(kb.kb_project_id(self.docs), meta["software_project_id"])
        before = {p: p.read_bytes() for p in self.docs.rglob("*") if p.is_file()}
        self.assertEqual(self.capture(), (rel, side, False))
        self.assertEqual(before, {p: p.read_bytes() for p in self.docs.rglob("*") if p.is_file()})
        self.assertEqual(kb.kb_corpus_check(self.docs)[0], [])

    def test_e2_same_extract_other_binding_is_distinct(self):
        first = self.capture()[0]
        self.assertNotEqual(first, self.capture("other.py")[0])
        self.assertNotEqual(first, self.capture(data=b"changed\r\nsecond\r\nthird\r\n")[0])

    def test_e2_partial_meta_and_tampered_binding_rejected(self):
        with self.assertRaises(ValueError):
            kb.kb_software_meta({"software_path": "src.py"})
        _, side, _ = self.capture()
        p = self.docs / side
        p.write_text(p.read_text().replace("software_path: src.py", "software_path: other.py"))
        self.assertTrue(kb.kb_corpus_check(self.docs)[0])
        with self.assertRaises(ValueError):
            self.capture()

    def test_e2_orphan_retry_finishes_without_changing_blob(self):
        rel, side, _ = self.capture()
        (self.docs / side).unlink()
        self.assertTrue(self.capture()[2])
        self.assertEqual((self.docs / rel).read_bytes(), b"second\r\n")

    def test_e2_project_id_preserves_readme_and_refuses_duplicates(self):
        readme = self.docs / "README.md"
        original = "---\ncustom: value\n" + "# comment\n" * 70 + "---\n# Body\n"
        readme.write_text(original)
        pid = kb.kb_project_id(self.docs, create=True)
        self.assertIn("custom: value", readme.read_text())
        self.assertTrue(readme.read_text().endswith("# Body\n"))
        self.assertEqual(kb.kb_project_id(self.docs), pid)
        readme.write_text(readme.read_text().replace("custom: value", "knowledge_project_id: " + pid))
        with self.assertRaises(ValueError):
            kb.kb_project_id(self.docs, create=True)

    def test_e3_bad_input_rejected_before_uuid_or_corpus(self):
        (self.project / "src.py").write_bytes(b"one\ntwo\n")
        baseline = (self.docs / "README.md").read_bytes()
        for path in ("../outside.py", "/absolute", "C:drive.py", "C:/absolute", "//host/share/x", "src.py:stream"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                kb.kb_capture_source(self.project, self.docs, path, 1, 1, "code")
        for start, end, role in ((0, 1, "code"), (2, 1, "code"), (1, 99, "code"), (1, 1, "secret")):
            with self.subTest(span=(start, end, role)), self.assertRaises(ValueError):
                kb.kb_capture_source(self.project, self.docs, "src.py", start, end, role)
        for data in (b"\xff", b"x" * (16 * 1024 * 1024 + 1)):
            (self.project / "src.py").write_bytes(data)
            with self.assertRaises(ValueError):
                kb.kb_capture_source(self.project, self.docs, "src.py", 1, 1, "code")
        self.assertEqual((self.docs / "README.md").read_bytes(), baseline)
        self.assertFalse((self.docs / "corpus").exists())

    def test_e3_unsafe_premise_refused(self):
        (self.project / "src.py").write_text("one\n")
        for ref in ("../outside.md", "https://example.invalid/a", "corpus/notes/missing.md"):
            with self.subTest(ref=ref), self.assertRaises(ValueError):
                kb.kb_capture_source(self.project, self.docs, "src.py", 1, 1, "code", [ref])
        self.assertIsNone(kb.kb_project_id(self.docs))

    def test_e3_metadata_paths_must_round_trip_before_publication(self):
        before = (self.docs / "README.md").read_bytes()
        for rel in (" source.py", "'source.py'", "source.py "):
            with self.subTest(rel=rel):
                with mock.patch.object(kb, "_kb_read_bytes", return_value=b"one\n"):
                    with self.assertRaises(ValueError):
                        kb.kb_capture_source(self.project, self.docs, rel, 1, 1, "code")
                self.assertEqual((self.docs / "README.md").read_bytes(), before)
                self.assertFalse((self.docs / "corpus").exists())

    def test_e4_corrupted_legacy_support_cannot_hide_behind_matched_alternative(self):
        matched = self.capture()[0]
        legacy = "corpus/given/legacy.txt"
        (self.docs / legacy).write_bytes(b"old\r\n")
        digest = hashlib.sha256(b"old\r\n").hexdigest()
        (self.docs / (legacy + ".meta.md")).write_text("---\nsha256: " + digest + "\n---\n")
        derived = self.note("legacy-summary", [legacy])
        self.ledger(sources=[derived + "#L4-4; " + matched + "#L1-1"])
        self.assertEqual(self.findings()["claims"][0][4][0]["status"], "UNTRACKED")
        (self.docs / legacy).write_bytes(b"corrupted\r\n")
        rc, out = self.run_cli(["evidence"])
        self.assertEqual(rc, 1, out)
        self.assertIn("digest mismatch", out)
        self.assertEqual(self.findings()["claims"][0][4][0]["status"], "INVALID")

    def test_e7_text_evidence_names_changed_transitive_premise(self):
        code = self.capture()[0]
        first = self.note("run", [code])
        second = self.note("summary", [first])
        third = self.note("decision", [second])
        self.ledger(sources=[third + "#L4-4"])
        (self.project / "src.py").write_text("changed\n")
        rc, out = self.run_cli(["evidence"])
        self.assertEqual(rc, 1, out)
        self.assertIn("CHANGED " + code + ": declared file bytes changed", out)

    def test_e3_symlink_source_output_and_readme_refused(self):
        target = self.project / "target.py"
        target.write_text("one\n")
        link = self.project / "link.py"
        try:
            link.symlink_to(target)
        except OSError:
            self.skipTest("symlink creation unavailable; Windows junction case is separate")
        with self.assertRaises(ValueError):
            kb.kb_capture_source(self.project, self.docs, "link.py", 1, 1, "code")
        (self.docs / "README.md").unlink()
        (self.docs / "README.md").symlink_to(target)
        with self.assertRaises(ValueError):
            kb.kb_capture_source(self.project, self.docs, "target.py", 1, 1, "code")
        (self.docs / "README.md").unlink()
        (self.docs / "README.md").write_text("# Root\n")
        (self.docs / "corpus").symlink_to(self.project, target_is_directory=True)
        with self.assertRaises(ValueError):
            kb.kb_capture_source(self.project, self.docs, "target.py", 1, 1, "code")

    def note(self, name, parents):
        rel = "corpus/notes/" + name + ".md"
        path = self.docs / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\nderived_from: [" + ", ".join(parents) + "]\n---\nObserved under recorded conditions.\n", encoding="utf-8")
        return rel

    def findings(self):
        return kb.kb_software_findings(self.project, self.docs)

    def test_e4_changed_missing_and_foreign_are_distinct_read_only(self):
        rel, _, _ = self.capture()
        self.ledger(sources=[rel + "#L1-1"])
        before = {p: p.read_bytes() for p in self.docs.rglob("*") if p.is_file()}
        report = self.findings()
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["claims"][0][4][0]["status"], "MATCHED")
        (self.project / "src.py").write_text("changed\n")
        self.assertEqual(self.findings()["claims"][0][4][0]["status"], "CHANGED")
        (self.project / "src.py").unlink()
        self.assertEqual(self.findings()["claims"][0][4][0]["status"], "UNAVAILABLE")
        readme = self.docs / "README.md"
        raw = readme.read_bytes()
        readme.write_text("# No identity\n")
        self.assertEqual(self.findings()["claims"][0][4][0]["status"], "UNBOUND")
        readme.write_bytes(raw)
        self.assertEqual(before, {p: p.read_bytes() for p in self.docs.rglob("*") if p.is_file()})

    def test_e5_transitive_and_or_and_untracked(self):
        code = self.capture()[0]
        test = self.capture("test.py", role="test")[0]
        result = self.capture("result.txt", role="result")[0]
        first = self.note("run", [code, test, result])
        second = self.note("summary", [first])
        third = self.note("decision", [second])
        self.ledger(sources=[third + "#L4-4"])
        self.assertEqual(self.findings()["claims"][0][4][0]["status"], "MATCHED")
        (self.project / "test.py").write_text("new test never run\n")
        self.assertEqual(self.findings()["claims"][0][4][0]["status"], "CHANGED")
        alternate = self.capture("alternate.txt", role="result")[0]
        self.ledger(sources=[third + "#L4-4; " + alternate + "#L1-1"])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(kb.kb_cmd_evidence(self.project, self.docs), 0)
        statuses = [s["status"] for s in self.findings()["claims"][0][4]]
        self.assertEqual(statuses, ["CHANGED", "MATCHED"])
        note = self.note("partial", [code, "corpus/given/facts.txt"])
        self.ledger(sources=[note + "#L4-4"])
        self.assertEqual(self.findings()["claims"][0][4][0]["status"], "UNTRACKED")

    def test_e5_cycle_and_dangling_are_integrity_errors(self):
        a = self.note("a", ["corpus/notes/b.md"])
        b = self.note("b", [a])
        self.ledger(sources=[b + "#L4-4"])
        self.assertTrue(any("cycle" in e for e in self.findings()["errors"]))
        (self.docs / a).unlink()
        self.assertTrue(any("missing" in e or "resolve" in e for e in self.findings()["errors"]))

    def test_e5_contested_or_superseded_never_gets_green_from_bytes(self):
        first = self.capture()[0]
        second = self.capture("other.py")[0]
        sources = [first + "#L1-1", second + "#L1-1"]
        _, ids = self.ledger(kinds=("OBSERVATION", "OBSERVATION"), sources=sources)
        for states in (("SUPERSEDED " + ids[1], "OK"),
                       ("CONTESTED " + ids[1], "CONTESTED " + ids[0])):
            self.ledger(kinds=("OBSERVATION", "OBSERVATION"), sources=sources, states=states)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(kb.kb_cmd_evidence(self.project, self.docs), 1)

    def test_e6_export_closes_derivations_and_refuses_broken_closure(self):
        raw, side, _ = self.capture()
        note = self.note("derived", [raw])
        self.ledger(sources=[note + "#L4-4"])
        selected, artifacts, _, errors = kb.kb_export_closure(self.docs, ["behavior"])
        self.assertEqual(errors, [])
        self.assertTrue({raw, side, note}.issubset(artifacts))
        (self.docs / raw).unlink()
        self.assertTrue(kb.kb_export_closure(self.docs, ["behavior"])[3])

    def test_e6_import_never_adopts_project_readme_and_rejects_bad_typed_row(self):
        bundle = self.project / "bundle"
        bundle.mkdir()
        (bundle / "MANIFEST.md").write_text("---\nkb_bundle: 1\n---\n")
        (bundle / "README.md").write_text("---\nknowledge_project_id: 11111111-1111-1111-1111-111111111111\n---\n")
        writes, _, _, errors = kb.kb_import_plan(bundle, self.docs)
        self.assertEqual(errors, [])
        self.assertNotIn("README.md", [w[0] for w in writes])
        self.assertIsNone(kb.kb_project_id(self.docs))
        (bundle / "topics").mkdir()
        text, _ = self.table()
        (bundle / "topics/new.md").write_text(text.replace(" | OBSERVATION |", " | OBSERVATION | extra |"))
        self.assertTrue(kb.kb_import_plan(bundle, self.docs)[3])

    def test_e6_export_includes_extraction_of_a_transitive_premise(self):
        given = self.docs / "corpus/given"
        given.mkdir(parents=True)
        (given / "manual.pdf").write_bytes(b"%PDF fixture")
        (given / "manual.txt").write_text("one premise\n")
        note = self.note("manual-use", ["corpus/given/manual.pdf"])
        self.ledger(sources=[note + "#L4-4"])
        _, artifacts, _, errors = kb.kb_export_closure(self.docs, ["behavior"])
        self.assertEqual(errors, [])
        self.assertIn("corpus/given/manual.txt", artifacts)

    def run_cli(self, argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            try:
                rc = kb.main(argv + ["--root", str(self.project)])
            except SystemExit as exc:
                rc = exc.code
        return rc, out.getvalue()

    def test_e7_capture_and_json_cli_with_nested_docs_root(self):
        (self.project / "src.py").write_bytes(b"one\ntwo\n")
        nested = self.project / "docs/knowledge"
        nested.mkdir(parents=True)
        (nested / "README.md").write_text("# Nested\n")
        rc, out = self.run_cli(["capture-source", "src.py", "--lines", "1:1", "--role", "code", "--docs-dir", "docs/knowledge"])
        self.assertEqual(rc, 0, out)
        self.assertTrue(list((nested / "corpus/given").glob("*.txt")))
        rc, out = self.run_cli(["evidence", "--json", "--docs-dir", "docs/knowledge"])
        self.assertEqual(rc, 0, out)
        report = json.loads(out)
        self.assertEqual(report["sources"][0][1], "MATCHED")

    def test_e7_legacy_requires_review_and_design_is_not_observed(self):
        self.ledger(schema=1)
        rc, out = self.run_cli(["evidence"])
        self.assertEqual(rc, 1, out)
        self.assertIn("UNCLASSIFIED", out)
        self.ledger(kinds=("DESIGN",))
        rc, out = self.run_cli(["evidence"])
        self.assertEqual(rc, 0, out)
        self.assertIn("DESIGN", out)
        self.assertNotIn("MATCHED", out)

    def test_e4_matched_bytes_cannot_validate_a_missing_locator(self):
        rel = self.capture()[0]
        self.ledger(sources=[rel + "#L99-99"])
        rc, out = self.run_cli(["evidence"])
        self.assertEqual(rc, 1, out)
        self.assertTrue(self.findings()["errors"])

    def test_e4_growth_beyond_capture_limit_is_change_not_corruption(self):
        rel = self.capture()[0]
        self.ledger(sources=[rel + "#L1-1"])
        (self.project / "src.py").write_bytes(b"x" * (kb.SOFTWARE_MAX_BYTES + 1))
        report = self.findings()
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["claims"][0][4][0]["status"], "CHANGED")

    def test_e4_schema2_cannot_be_silently_legacy(self):
        self.ledger(schema=1)
        topic = self.docs / "topics/behavior.md"
        topic.write_text(topic.read_text().replace("claim_schema: 1", "claim_schema: 2"))
        self.assertTrue(self.findings()["errors"])

    def test_e3_mutation_during_read_refuses_publication(self):
        (self.project / "src.py").write_bytes(b"one\ntwo\n")
        original = kb.os.fstat
        calls = []
        def mutate(fd):
            info = original(fd)
            if info.st_size == 8:
                calls.append(fd)
            if info.st_size == 8 and len(calls) == 2:
                (self.project / "src.py").write_bytes(b"replaced with other bytes\n")
            return original(fd)
        with mock.patch.object(kb.os, "fstat", side_effect=mutate):
            with self.assertRaisesRegex(ValueError, "changed during"):
                kb.kb_capture_source(self.project, self.docs, "src.py", 1, 1, "code")
        self.assertIsNone(kb.kb_project_id(self.docs))
        self.assertFalse((self.docs / "corpus").exists())

    def test_e6_foreign_binding_does_not_open_live_software_path(self):
        rel = self.capture()[0]
        self.ledger(sources=[rel + "#L1-1"])
        (self.docs / "README.md").write_text("# Foreign project\n")
        original = kb._kb_read_bytes
        def guard(base, path, *args, **kwargs):
            self.assertNotEqual(Path(base), self.project, "foreign binding opened live source")
            return original(base, path, *args, **kwargs)
        with mock.patch.object(kb, "_kb_read_bytes", side_effect=guard):
            self.assertEqual(self.findings()["claims"][0][4][0]["status"], "UNBOUND")

    def test_e7_stale_and_seam_warn_on_drift_without_changing_legacy_exit(self):
        rel = self.capture()[0]
        self.ledger(sources=[rel + "#L1-1"])
        (self.project / "src.py").write_text("changed\n")
        with mock.patch.object(kb.sdlc_core, "cmd_stale", return_value=0), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(kb.kb_cmd_stale(self.project, self.docs), 0)
        self.assertIn("CHANGED", out.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as out:
            kb.kb_validate_surface(self.docs, full=True, project=self.project)
        self.assertIn("CHANGED", out.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as out:
            kb.kb_validate_surface(self.docs, full=True)
        self.assertIn("UNBOUND", out.getvalue())

    def test_e2_lock_refuses_without_mutation(self):
        (self.docs / ".software-capture.lock").write_text("active\n")
        with self.assertRaisesRegex(ValueError, "lock"):
            self.capture()
        self.assertIsNone(kb.kb_project_id(self.docs))
        self.assertFalse((self.docs / "corpus").exists())

    def test_e2_concurrent_cli_never_overwrites_or_forks_identity(self):
        (self.project / "src.py").write_text("one\ntwo\n")
        command = [sys.executable, kb.__file__, "capture-source", "src.py", "--lines", "1:1", "--role", "code", "--root", str(self.project)]
        workers = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        results = [(p.communicate(timeout=20), p.returncode) for p in workers]
        self.assertTrue(any(rc == 0 for _, rc in results), results)
        self.assertTrue(all(rc in (0, 1) for _, rc in results), results)
        self.assertEqual(len(list((self.docs / "corpus/given").glob("*.txt"))), 1)
        self.assertEqual(kb.kb_corpus_check(self.docs)[0], [])
        self.assertFalse((self.docs / ".software-capture.lock").exists())

    def test_e7_installed_entry_reaches_capture_and_evidence(self):
        scripts = Path(__file__).resolve().parent
        entry = scripts / ("mkt_check.py" if (scripts / "mkt_check.py").exists() else "sdlc_check.py")
        (self.project / "src.py").write_text("one\ntwo\n")
        for args in (["capture-source", "src.py", "--lines", "1:1", "--role", "config"], ["evidence", "--json"]):
            result = subprocess.run([sys.executable, str(entry), *args, "--root", str(self.project)], capture_output=True, text=True, encoding="utf-8", timeout=20)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["sources"][0][1], "MATCHED")

    def test_e7_common_methods_ship_in_isolated_distribution(self):
        directory = Path(__file__).resolve().parents[1]
        package = directory.parents[1] / "package.json"
        if not package.exists():
            self.skipTest("installed skill has no package manifest")
        allowlist = json.loads(package.read_text(encoding="utf-8"))["files"]
        for name in ("memory.md", "distillation.md", "taxonomy.md", "reconciliation.md", "portability.md", "knowledge-templates.md"):
            self.assertTrue((directory / name).is_file(), name)
            self.assertIn("skills/" + directory.name + "/" + name, allowlist)
        revision_homes = [p.name for p in directory.glob("*.md") if "never append a delta" in " ".join(p.read_text(encoding="utf-8").split())]
        self.assertEqual(revision_homes, ["memory.md"])
        self.assertFalse(any("test_software_knowledge" in p or "evals/" in p for p in allowlist))

    def legacy_corpus(self):
        given = self.docs / "corpus/given"
        notes = self.docs / "corpus/notes"
        given.mkdir(parents=True)
        notes.mkdir(parents=True)
        for name, data, extra in (("old.txt", b"old\n", ""), ("new.txt", b"new\n", "supersedes: old.txt\n")):
            (given / name).write_bytes(data)
            (given / (name + ".meta.md")).write_text(
                "---\nsha256: %s\nprovenance: GIVEN\n%s---\n" % (hashlib.sha256(data).hexdigest(), extra))
        (notes / "summary.md").write_text("---\nderived_from: old.txt\n---\nSummary.\n")

    def linked_root(self):
        """A second path to self.project through a directory link."""
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        link = Path(holder.name) / "linked"
        try:
            link.symlink_to(self.project, target_is_directory=True)
        except OSError:
            if os.name != "nt":
                self.skipTest("directory symlink unavailable")
            result = subprocess.run(["powershell", "-NoProfile", "-Command",
                "New-Item -ItemType Junction -Path '" + str(link) + "' -Target '" + str(self.project) + "'"],
                capture_output=True)
            if result.returncode:
                self.skipTest("junction creation unavailable: " + result.stderr.decode(errors="replace"))
        self.addCleanup(os.rmdir if os.name == "nt" else os.unlink, link)  # the link only, never its target
        return link

    def test_e3_link_above_the_chosen_root_is_trusted(self):
        # macOS /var and /tmp are symlinks; a junctioned checkout is common on
        # Windows. Confinement concerns what lies UNDER the root, not above it.
        self.legacy_corpus()
        (self.project / "src.py").write_text("one\n")
        root = self.linked_root()
        docs = root / "ai_docs"
        self.assertEqual(kb.kb_corpus_check(docs)[0], [])
        cycle = kb.kb_time_cycle(docs)
        self.assertEqual(cycle["dangling"], [])
        self.assertEqual([c[0] for c in cycle["chain"]], ["corpus/notes/summary.md"])
        rel, _, created = kb.kb_capture_source(root, docs, "src.py", 1, 1, "code")
        self.assertTrue(created)
        support = kb.kb_software_findings(root, docs)["sources"]
        self.assertIn((rel, "MATCHED", "declared file bytes match"), support)

    def test_e1_legacy_headers_keep_their_lenient_reading(self):
        # Sidecars and notes written before F-064 are read as before; only a
        # header carrying a software binding gets the strict, duplicate-aware read.
        self.legacy_corpus()
        side = self.docs / "corpus/given/old.txt.meta.md"
        side.write_text(side.read_text().replace("provenance: GIVEN\n", "provenance: GIVEN\nprovenance: GIVEN\n"))
        (self.docs / "corpus/notes/summary.md").write_text("---\nderived_from: old.txt\nSummary without a closing fence.\n")
        self.assertEqual(kb.kb_corpus_check(self.docs)[0], [])
        cycle = kb.kb_time_cycle(self.docs)
        self.assertEqual(cycle["dangling"], [])
        self.assertEqual([c[0] for c in cycle["chain"]], ["corpus/notes/summary.md"])
        (self.docs / "corpus/given/old.txt").unlink()
        self.assertIn("corpus/given/old.txt: sidecar exists but the original is gone",
                      kb.kb_corpus_check(self.docs)[0])
        _, software, _ = self.capture()
        path = self.docs / software
        path.write_text(path.read_text().replace("software_role: code\n", "software_role: code\nsoftware_role: test\n"))
        self.assertTrue(any("duplicate frontmatter field: software_role" in e
                            for e in kb.kb_corpus_check(self.docs)[0]))

    def test_e2_lines_are_lf_terminated_like_grep_and_git(self):
        # A span read from `grep -n` or a diff must select the same bytes: \f,
        # \v, a lone \r, U+0085 and U+2028 are content, not line breaks.
        data = "one\fstill one\nsecond same\rline\x85end\r\nthird".encode("utf-8")
        rel, _, _ = self.capture(data=data, start=2, end=3)
        self.assertEqual((self.docs / rel).read_bytes(),
                         "second same\rline\x85end\r\nthird".encode("utf-8"))
        with self.assertRaises(ValueError):
            self.capture(data=data, start=4, end=4)

    def test_e4_trailing_separator_is_not_an_invalid_source(self):
        # kb_check_claims and kb_claim_sources skip an empty `;` piece; evidence agrees.
        self.ledger(sources=["corpus/given/facts.txt#L1-1;"])
        self.assertEqual(kb.kb_check_claims(self.docs)[0], [])
        self.assertEqual(kb.kb_software_findings(self.project, self.docs)["errors"], [])

    @unittest.skipUnless(os.name == "nt", "Windows junction")
    def test_e3_junction_never_traversed(self):
        import subprocess
        outside = self.project / "outside"
        outside.mkdir()
        (outside / "secret.py").write_text("secret\n")
        link = self.project / "junction"
        result = subprocess.run(["powershell", "-NoProfile", "-Command",
            "New-Item -ItemType Junction -Path '" + str(link) + "' -Target '" + str(outside) + "'"], capture_output=True)
        if result.returncode:
            self.skipTest("junction creation unavailable: " + result.stderr.decode(errors="replace"))
        try:
            with self.assertRaises(ValueError):
                kb.kb_capture_source(self.project, self.docs, "junction/secret.py", 1, 1, "code")
            self.assertIsNone(kb.kb_project_id(self.docs))
        finally:
            os.rmdir(link)  # remove only the junction, never its target


if __name__ == "__main__":
    unittest.main()
