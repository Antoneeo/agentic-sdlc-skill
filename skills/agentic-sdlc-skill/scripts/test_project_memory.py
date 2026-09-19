"""Shared-memory acceptance tests: real distribution CLI, no sibling install."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ENTRY = next(HERE / n for n in ("sdlc_check.py", "mkt_check.py")
             if (HERE / n).is_file())


class ProjectMemory(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.docs = self.root / "ai_docs"
        self.put("README.md", "---\ndefault_domain: code\n---\n# Docs\n")

    def put(self, rel, text):
        p = self.docs / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    def cli(self, *args):
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        env.pop("AGENTIC_SDLC_DOCS_DIR", None)
        return subprocess.run([sys.executable, str(ENTRY), *args,
                               "--root", str(self.root), "--docs-dir", "ai_docs"],
                              capture_output=True, text=True, encoding="utf-8", env=env)

    def seed(self):
        for rel, domain, state in (("reference/GUIDE_onboarding.md", "code", "CURRENT"),
                                   ("architecture/ADR_signup.md", "code", "APPROVED"),
                                   ("strategy/PROMISE.md", "marketing", "DRAFT")):
            self.put(rel, f"---\ndescription: Onboarding constraints\ndomain: {domain}\n"
                          f"status: {state}\ntopics: [onboarding]\n---\n# Source\n")

    def test_single_install_indexes_and_recalls_all_domains_without_claims(self):
        self.seed()
        result = self.cli("index")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        idx = self.docs / "memory/INDEX.md"
        self.assertTrue(idx.is_file(), "index must register documents in common memory")
        text = idx.read_text(encoding="utf-8")
        for rel in ("reference/GUIDE_onboarding.md", "architecture/ADR_signup.md", "strategy/PROMISE.md"):
            self.assertIn(rel, text)
        self.assertIn("marketing", text)
        self.assertNotIn("APPROVED", text)  # r2: no aggregated document state
        self.assertFalse((self.docs / "topics").exists())
        self.assertFalse((self.docs / "corpus").exists())
        before = idx.read_bytes()
        self.cli("index")
        self.assertEqual(before, idx.read_bytes())
        result = self.cli("recall", "onboarding")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("strategy/PROMISE.md", result.stdout)
        self.assertIn("architecture/ADR_signup.md", result.stdout)

    def test_recall_uses_live_metadata_and_does_not_write(self):
        self.seed()
        self.cli("index")
        idx = self.docs / "memory/INDEX.md"
        before = {p.relative_to(self.docs): p.read_bytes() for p in self.docs.rglob("*") if p.is_file()}
        self.put("strategy/NEW.md", "---\ndescription: Zephyr rollout\n---\n# Original\n")
        result = self.cli("recall", "zephyr")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("strategy/NEW.md", result.stdout)
        self.assertEqual(before.get(Path("memory/INDEX.md")), idx.read_bytes())
        result = self.cli("validate")
        self.assertIn("memory/INDEX.md", result.stdout)
        self.assertNotEqual(result.returncode, 0)

    def test_body_change_and_deletion_are_detected_by_catalog_fingerprint(self):
        self.seed()
        self.cli("index")
        p = self.docs / "strategy/PROMISE.md"
        p.write_text(p.read_text(encoding="utf-8") + "Changed evidence.\n", encoding="utf-8")
        self.assertIn("memory/INDEX.md", self.cli("validate").stdout)
        self.cli("index")
        p.unlink()
        self.assertIn("memory/INDEX.md", self.cli("validate").stdout)
        self.cli("index")
        self.assertNotIn("PROMISE.md", (self.docs / "memory/INDEX.md").read_text(encoding="utf-8"))

    def test_graph_command_and_full_check_reject_cycle_in_every_distribution(self):
        self.put("topics/loop.md", "---\ndescription: Loop\nparents: [loop]\n---\n# Loop\n")
        self.cli("index")
        for command in ("graph", "check"):
            result = self.cli(command)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("cycle", result.stdout.lower())

    def test_raw_corpus_and_harness_are_not_catalogued(self):
        self.put("corpus/given/private.md", "SECRET")
        self.put("solutions/harness_probe/fixture.md", "SECRET")
        self.cli("index")
        idx = self.docs / "memory/INDEX.md"
        self.assertTrue(idx.is_file())
        text = idx.read_text(encoding="utf-8")
        self.assertNotIn("private.md", text)
        self.assertNotIn("fixture.md", text)
        self.assertNotIn("SECRET", text)

    def test_discovery_and_ambiguity_are_the_same_for_index_and_recall(self):
        def run(command):
            env = dict(os.environ, PYTHONIOENCODING="utf-8")
            env.pop("AGENTIC_SDLC_DOCS_DIR", None)
            return subprocess.run([sys.executable, str(ENTRY), command,
                                   *(["onboarding"] if command == "recall" else []),
                                   "--root", str(self.root)], capture_output=True,
                                  text=True, encoding="utf-8", env=env)
        self.assertEqual(run("index").returncode, 0)
        (self.root / "mkt_docs").mkdir()
        for command in ("index", "recall", "validate", "check"):
            result = run(command)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("refusing to guess", result.stdout)

    def test_external_symlinks_are_not_read_or_written(self):
        target = self.root / "outside.md"
        target.write_text("UNCHANGED", encoding="utf-8")
        self.put("reference/normal.md", "# Normal")
        try:
            (self.docs / "reference/leak.md").symlink_to(target)
        except OSError:
            self.skipTest("symlink creation unavailable")
        self.cli("index")
        idx = self.docs / "memory/INDEX.md"
        self.assertNotIn("leak.md", idx.read_text(encoding="utf-8"))
        idx.unlink()
        idx.symlink_to(target)
        result = self.cli("index")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(target.read_text(encoding="utf-8"), "UNCHANGED")

    def test_environment_docs_root_and_profile_survive_shared_import(self):
        self.docs.rename(self.root / "custom_docs")
        env = dict(os.environ, AGENTIC_SDLC_DOCS_DIR="custom_docs", PYTHONIOENCODING="utf-8")
        result = subprocess.run([sys.executable, str(ENTRY), "index", "--root", str(self.root)],
                                capture_output=True, text=True, encoding="utf-8", env=env)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.root / "custom_docs/memory/INDEX.md").is_file())
        result = subprocess.run([sys.executable, "-c",
            "import sdlc_core; sdlc_core.set_entry_point('marketing', script='mkt_check.py'); "
            "before=sdlc_core.profile(); import knowledge; "
            "assert sdlc_core.profile()==before; assert sdlc_core.entry_script()=='mkt_check.py'"],
            cwd=HERE, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
