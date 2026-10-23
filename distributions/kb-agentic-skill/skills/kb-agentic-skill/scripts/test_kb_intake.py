#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-077 battery — intake hygiene: credentials in given/, one home per source
text, the adoption inventory, original_ref. Stdlib, no LLM, no net.

    python scripts/test_kb_intake.py
"""
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import knowledge  # noqa: E402

ENTRY = HERE / "sdlc_check.py"
SECRET = "hunter2-fake-value"
DOC = ("db.url=jdbc:postgresql://db.example.test/app\n"
       "db.user=app\n"
       "db.password=%s\n" % SECRET)
REDACTED = DOC.replace(SECRET, "[REDACTED: password]")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(*args):
    p = subprocess.run([sys.executable, str(ENTRY), *args], capture_output=True,
                       text=True, encoding="utf-8")
    return p.returncode, p.stdout + p.stderr


def tree(tmp, text, sidecar=(), snapshot=False, guide=True):
    """A minimal project: one given/ artifact + sidecar, optionally a guide whose
    snapshot (or the artifact itself) is its source. Returns (docs, name)."""
    tmp = Path(tmp)
    docs = tmp / "ai_docs"
    for sub in ("vision", "strategic", "reference", "corpus/given", "audit"):
        (docs / sub).mkdir(parents=True, exist_ok=True)
    (docs / "README.md").write_text("# ai_docs\n", encoding="utf-8")
    raw = text.encode("utf-8")
    name = "app-%s.properties" % sha(raw)[:8]
    (docs / "corpus/given" / name).write_bytes(raw)
    meta = ["---", "sha256: %s" % sha(raw), "date: 2026-10-23",
            "provenance: GIVEN"] + list(sidecar) + ["---", ""]
    (docs / "corpus/given" / (name + ".meta.md")).write_text(
        "\n".join(meta), encoding="utf-8")
    if guide:
        df = "ai_docs/corpus/given/" + name
        if snapshot:
            (docs / "reference/.sources").mkdir(parents=True, exist_ok=True)
            (docs / "reference/.sources" / name).write_bytes(raw)
            df = "ai_docs/reference/.sources/" + name
        (docs / "reference/GUIDE_app_config.md").write_text(
            "---\ndescription: Consult before changing the app configuration.\n"
            "status: CURRENT\nsource_kind: document\nsource: team config\n"
            "distilled_from: %s\nsource_hash: %s\n---\n# Guide\n\n## Rule\n"
            "[source: %s#L1-3]\nThe app reads its database from db.url.\n"
            % (df, sha(raw), name), encoding="utf-8")
    run("index", "--root", str(tmp))
    return docs, name


def snapshot_of(tmp):
    return {str(p.relative_to(tmp)): p.read_bytes()
            for p in Path(tmp).rglob("*") if p.is_file()}


class CredentialShapes(unittest.TestCase):
    """AC4: the scanner's two lists, in one table each."""

    FLAGGED = [
        ("db.password=s3cr3t", "password"),
        ("DB_PASSWORD: s3cr3t", "password"),
        ('  "password": "s3cr3t",', "password"),
        ("dbPassword = s3cr3t", "password"),
        ("spring.datasource.passphrase=abc", "password"),
        ("api_key: abcd1234", "api-key"),
        ("apiKey=abcd1234", "api-key"),
        ("aws.access-key = AKIAABCDEFGHIJKLMNOP", "access-key"),
        ("client_secret=xyz", "client-secret"),
        ("jwt.secret=xyz", "secret"),
        ("auth.token=xyz", "token"),
        ("credentials = user:pw", "credentials"),
        ("-----BEGIN RSA PRIVATE KEY-----", "private-key"),
        ("-----BEGIN OPENSSH PRIVATE KEY-----", "private-key"),
        ("url=postgresql://app:s3cr3t@db.example.test/app", "connection-string"),
        ("Authorization: Bearer abcdefghijklmnopqrstuvwxyz0123", "bearer-token"),
        ("export API_TOKEN=abc", "token"),
        ("secret_key=xyz", "secret"),
        ("jdbc:postgresql://h/db?user=a&password=s3cr3t", "connection-string"),
        ("Password: required", "password"),
        ("csrf_token: abc", "token"),
    ]
    NOT_FLAGGED = [
        "db.password=",
        "db.password=[REDACTED: password]",
        "db.password=<your password>",
        "db.password=${DB_PASSWORD}",
        "db.password={{ vault.db }}",
        "db.password=%(password)s",
        "db.password=********",
        "tokenizer: whitespace",
        "keyboard_layout=it",
        "Enter your password: it is asked at first login.",
        "The secret: there is none.",
        "url=postgresql://db.example.test/app",
        "url=postgresql://app:${PW}@db.example.test/app",
        "db.user=app",
        "password.min.length=8",
        "max_tokens: 4096",
        "password: |",
        "password: >-",
        "passphrase=correct horse battery",
        "| password | s3cr3t |",
        "secret_key_base: abc",
        "db.password=true",
        "db.password=ENC(abc)",
        "Authorization: Bearer short",
    ]

    def scan(self, line):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "f.txt"
            p.write_text(line + "\n", encoding="utf-8")
            return knowledge.kb_credential_findings(p)

    def test_flagged(self):
        for line, kind in self.FLAGGED:
            with self.subTest(line=line):
                self.assertEqual(self.scan(line), [(1, kind)])

    def test_not_flagged(self):
        for line in self.NOT_FLAGGED:
            with self.subTest(line=line):
                self.assertEqual(self.scan(line), [])

    def test_binary_not_read(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "f.bin"
            p.write_bytes(b"\x00\x01password=s3cr3t\n")
            self.assertEqual(knowledge.kb_credential_findings(p), [])

    def test_utf16_with_bom_is_read(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "f.txt"
            p.write_bytes("db.password=s3cr3t\n".encode("utf-16"))
            self.assertEqual(knowledge.kb_credential_findings(p), [(1, "password")])

    def test_long_line_inspected_on_its_head(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "f.txt"
            p.write_text("password=s3cr3t" + "x" * 10000 + "\n", encoding="utf-8")
            self.assertEqual(knowledge.kb_credential_findings(p), [(1, "password")])


class CredentialCheck(unittest.TestCase):

    def test_ac1_flagged_without_the_value(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, DOC)
            rc, out = run("check", "--root", t)
            self.assertNotEqual(rc, 0, out)
            self.assertIn("credential", out)
            self.assertIn("line 3", out)
            self.assertIn("password", out)
            self.assertNotIn(SECRET, out)

    def test_corpus_command_flags_too(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, DOC)
            rc, out = run("corpus", "--root", t)
            self.assertEqual(rc, 1, out)
            self.assertNotIn(SECRET, out)

    def test_ac2_redacted_and_declared_passes(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, REDACTED, sidecar=["redacted_at_intake: [password]"])
            rc, out = run("check", "--root", t)
            self.assertEqual(rc, 0, out)
            self.assertNotIn("credential", out)

    def test_redaction_declaration_does_not_silence(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, DOC, sidecar=["redacted_at_intake: [password]"])
            rc, out = run("check", "--root", t)
            self.assertNotEqual(rc, 0, out)

    def test_ac3_reviewed_false_positive_passes(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, DOC, sidecar=[
                "credential_scan: reviewed - a vendor manual's sample value"])
            rc, out = run("check", "--root", t)
            self.assertEqual(rc, 0, out)

    def test_review_needs_a_reason_word(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, DOC, sidecar=["credential_scan: skip"])
            rc, out = run("check", "--root", t)
            self.assertNotEqual(rc, 0, out)


class Carriers(unittest.TestCase):

    def test_check_prints_each_error_once_validate_none(self):
        with tempfile.TemporaryDirectory() as t:
            _, name = tree(t, DOC)
            rc, out = run("check", "--root", t)
            self.assertEqual(out.count("look like a credential"), 1, out)
            rc, out = run("validate", "--root", t)
            self.assertNotIn("look like a credential", out)

    def test_code_entry_point_flags_too(self):
        code = HERE.parents[4] / "skills/agentic-sdlc-skill/scripts/sdlc_check.py"
        if not code.is_file():
            self.skipTest("code lens not beside this distribution")
        with tempfile.TemporaryDirectory() as t:
            tree(t, DOC)
            p = subprocess.run([sys.executable, str(code), "check", "--root", t],
                               capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(p.returncode, 0)
            self.assertNotIn(SECRET, p.stdout + p.stderr)


class Snapshots(unittest.TestCase):
    """AC5: document-guide snapshots are scanned in every lens; code ones are not."""

    def _snap(self, t, kind="document", extra=""):
        docs, name = tree(t, REDACTED, guide=False)
        (docs / "reference/.sources").mkdir(parents=True, exist_ok=True)
        (docs / "reference/.sources/cfg-1.md").write_text(DOC, encoding="utf-8")
        (docs / "reference/GUIDE_cfg.md").write_text(
            "---\ndescription: d\nstatus: CURRENT\nsource_kind: %s\nsource: s\n"
            "distilled_from: ai_docs/reference/.sources/cfg-1.md\nsource_hash: %s\n%s"
            "---\n# G\n\n## R\n[source: cfg-1.md#L1]\nx\n"
            % (kind, sha(DOC.encode()), extra), encoding="utf-8")
        run("index", "--root", t)
        return docs

    def test_document_snapshot_flagged(self):
        with tempfile.TemporaryDirectory() as t:
            self._snap(t)
            rc, out = run("check", "--root", t)
            self.assertNotEqual(rc, 0, out)
            self.assertIn("reference/.sources/cfg-1.md", out)
            self.assertNotIn(SECRET, out)

    def test_code_snapshot_not_scanned(self):
        with tempfile.TemporaryDirectory() as t:
            self._snap(t, kind="code")
            rc, out = run("check", "--root", t)
            self.assertNotIn("look like a credential", out)

    def test_guide_escape(self):
        with tempfile.TemporaryDirectory() as t:
            self._snap(t, extra="credential_scan: reviewed - sample config\n")
            rc, out = run("check", "--root", t)
            self.assertNotIn("look like a credential", out)

    def test_no_corpus_still_scanned(self):
        with tempfile.TemporaryDirectory() as t:
            docs = self._snap(t)
            import shutil
            shutil.rmtree(docs / "corpus")
            run("index", "--root", t)
            rc, out = run("check", "--root", t)
            self.assertIn("look like a credential", out)


class Withdrawal(unittest.TestCase):
    """AC6: a tombstone holds no bytes and no digest."""

    def _withdrawn(self, t, with_sha=False):
        docs, old = tree(t, REDACTED, guide=False)
        g = docs / "corpus/given"
        (g / old).unlink()
        (g / (old + ".meta.md")).unlink()
        tomb = "app-withdrawn-20261023.properties"
        lines = ["---", "date: 2026-10-23", "provenance: GIVEN",
                 "withdrawn: credential - redacted successor stored"]
        if with_sha:
            lines.append("sha256: %s" % ("0" * 64))
        (g / (tomb + ".meta.md")).write_text("\n".join(lines + ["---", ""]),
                                             encoding="utf-8")
        raw = REDACTED.encode()
        new = "app-%s.properties" % sha(raw)[:8]
        (g / new).write_bytes(raw)
        (g / (new + ".meta.md")).write_text(
            "---\nsha256: %s\ndate: 2026-10-23\nprovenance: GIVEN\n"
            "supersedes: %s\nredacted_at_intake: [password]\n---\n" % (sha(raw), tomb),
            encoding="utf-8")
        run("index", "--root", t)
        return docs, tomb

    def test_tombstone_passes(self):
        with tempfile.TemporaryDirectory() as t:
            docs, tomb = self._withdrawn(t)
            rc, out = run("check", "--root", t)
            self.assertEqual(rc, 0, out)
            self.assertNotIn("not in given/", out)
            self.assertIn("withdrawn", (docs / "corpus/INDEX.md").read_text(encoding="utf-8"))

    def test_tombstone_with_digest_errors(self):
        with tempfile.TemporaryDirectory() as t:
            self._withdrawn(t, with_sha=True)
            rc, out = run("corpus", "--root", t)
            self.assertEqual(rc, 1, out)
            self.assertIn("withdrawn", out)

    def test_export_and_site_skip_tombstone(self):
        with tempfile.TemporaryDirectory() as t:
            docs, tomb = self._withdrawn(t)
            import docs_site
            self.assertNotIn(tomb, docs_site.build_sources(docs, {}))

    def test_sidecar_less_file_warns(self):
        with tempfile.TemporaryDirectory() as t:
            docs, _ = tree(t, REDACTED, guide=False)
            (docs / "corpus/given/leftover.properties").write_text("a=b\n", encoding="utf-8")
            rc, out = run("corpus", "--root", t)
            self.assertIn("leftover.properties: no sidecar", out)


class OneHome(unittest.TestCase):

    def test_ac5_same_text_in_two_homes_warns_once(self):
        with tempfile.TemporaryDirectory() as t:
            _, name = tree(t, REDACTED, snapshot=True,
                           sidecar=["redacted_at_intake: [password]"])
            rc, out = run("check", "--root", t)
            self.assertEqual(out.count("same text"), 1, out)
            self.assertIn("reference/.sources/" + name, out)
            self.assertIn("corpus/given/" + name, out)

    def test_line_endings_do_not_hide_the_duplicate(self):
        with tempfile.TemporaryDirectory() as t:
            docs, name = tree(t, REDACTED, snapshot=True)
            snap = docs / "reference/.sources" / name
            snap.write_bytes(snap.read_bytes().replace(b"\n", b"\r\n"))
            rc, out = run("corpus", "--root", t)
            self.assertIn("same text", out)

    def test_different_text_is_silent(self):
        with tempfile.TemporaryDirectory() as t:
            docs, name = tree(t, REDACTED, snapshot=True)
            (docs / "reference/.sources" / name).write_text("other\n", encoding="utf-8")
            rc, out = run("corpus", "--root", t)
            self.assertNotIn("same text", out)


class Adopt(unittest.TestCase):

    def test_ac6_lists_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, DOC, snapshot=True, sidecar=[
                "credential_scan: reviewed - fixture"])
            before = snapshot_of(t)
            rc, out = run("adopt", "--root", t)
            self.assertEqual(rc, 0, out)
            self.assertIn("GUIDE_app_config.md", out)
            self.assertIn("reference/.sources/", out)
            self.assertIn("line 3", out)
            self.assertNotIn(SECRET, out)
            self.assertIn("Nothing was written", out)
            self.assertIn("portability.md", out)
            self.assertEqual(snapshot_of(t), before)

    def test_guide_already_on_corpus(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, REDACTED)
            rc, out = run("adopt", "--root", t)
            self.assertEqual(rc, 0, out)
            self.assertIn("already in corpus/given/", out)

    def test_code_guides_counted_not_listed(self):
        with tempfile.TemporaryDirectory() as t:
            docs, _ = tree(t, REDACTED, guide=False)
            (docs / "reference/GUIDE_engine.md").write_text(
                "---\ndescription: d\nstatus: CURRENT\nsource_kind: code\n"
                "source: s\ndistilled_from: ai_docs/reference/.sources/e.md\n"
                "source_hash: x\n---\n# G\n", encoding="utf-8")
            rc, out = run("adopt", "--root", t)
            self.assertEqual(rc, 0, out)
            self.assertNotIn("GUIDE_engine.md", out)
            self.assertIn("1 code guide", out)

    def test_pointer_outside_the_root_is_not_read(self):
        with tempfile.TemporaryDirectory() as t:
            docs, _ = tree(t, REDACTED, guide=False)
            (docs / "reference/GUIDE_x.md").write_text(
                "---\ndescription: d\nstatus: CURRENT\nsource_kind: document\n"
                "source: s\ndistilled_from: ../outside.txt\nsource_hash: x\n---\n"
                "# G\n", encoding="utf-8")
            rc, out = run("adopt", "--root", t)
            self.assertEqual(rc, 0, out)
            self.assertIn("outside the project root", out)

    def test_no_docs_root(self):
        with tempfile.TemporaryDirectory() as t:
            rc, out = run("adopt", "--root", t)
            self.assertEqual(rc, 1, out)


class OriginalRef(unittest.TestCase):

    def test_ac7_original_ref_is_silent(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, REDACTED, sidecar=["original_ref: wiki://team-space/app-config"])
            rc, out = run("check", "--root", t)
            self.assertEqual(rc, 0, out)
            self.assertNotIn("does not resolve", out)

    def test_uri_in_original_path_names_original_ref(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, REDACTED, sidecar=["original_path: https://wiki.example.test/x"])
            rc, out = run("corpus", "--root", t)
            self.assertIn("does not resolve", out)
            self.assertIn("original_ref:", out)


class GuideOnCorpus(unittest.TestCase):
    """AC8: unchanged behaviour, guarded."""

    def test_check_and_stale_follow_the_artifact(self):
        with tempfile.TemporaryDirectory() as t:
            docs, name = tree(t, REDACTED)
            rc, out = run("check", "--root", t)
            self.assertEqual(rc, 0, out)
            rc, out = run("stale", "--root", t)
            self.assertNotIn("[stale]", out)
            p = docs / "corpus/given" / name
            p.write_bytes(p.read_bytes() + b"x")
            rc, out = run("stale", "--root", t)
            self.assertIn("[stale] reference/GUIDE_app_config.md", out)


if __name__ == "__main__":
    unittest.main()
