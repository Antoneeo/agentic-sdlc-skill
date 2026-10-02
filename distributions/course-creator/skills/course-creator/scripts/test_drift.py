#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TS5 — the drift guard, as a gating test.

Three distributions ship one spine. This is what makes forgetting a copy loud
instead of silent: it already happened three times, and each time a user found it.

    python scripts/test_drift.py

It runs in every distribution and needs no access to the others: the manifest's
CONTENT is identical everywhere, so a shared file edited in one repo and not the
rest shows up as a manifest that no longer matches its siblings.
"""
import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import shared_files  # noqa: E402


class DriftGuard(unittest.TestCase):

    def test_manifest_exists(self):
        self.assertTrue(
            shared_files.MANIFEST.is_file(),
            "no shared manifest: generate it with `python scripts/shared_files.py --update`")

    def test_no_shared_file_is_missing(self):
        missing, _ = shared_files.report()
        self.assertEqual(missing, (),
                         "a distribution is missing part of the spine: copy it in, or "
                         "remove it from SHARED_FILES as a reviewable change")

    def test_no_shared_file_has_diverged(self):
        _, changed = shared_files.report()
        self.assertEqual(
            changed, (),
            "shared files no longer match the manifest. If the change is intended, apply "
            "it to EVERY distribution and run `shared_files.py --update` in each; if it is "
            "not, restore them. This is the check that the three copies stayed one file.")

    def test_the_manifest_covers_every_declared_shared_file(self):
        recorded = json.loads(shared_files.MANIFEST.read_text(encoding="utf-8"))["files"]
        self.assertEqual(sorted(recorded), sorted(shared_files.SHARED_FILES),
                         "the manifest and SHARED_FILES disagree: regenerate the manifest")

    def test_the_entry_point_is_never_shared(self):
        """The overlay IS the domain: sharing it would erase the distinction."""
        for rel in ("scripts/sdlc_check.py", "scripts/mkt_check.py"):
            self.assertNotIn(rel, shared_files.SHARED_FILES)

    def test_the_copies_are_identical_to_each_other(self):
        """The strong form, available in the consolidated checkout.

        The manifest catches a local edit. THIS catches the case the manifest
        cannot: a change applied and recorded in one distribution and never carried
        to the others. It found exactly that on its first run."""
        diverged, root = shared_files.cross_distribution_report()
        if root is None:
            self.skipTest("not the consolidated checkout: only the manifest check applies")
        self.assertEqual(diverged, {},
                         "the spine is one file, and these copies are not the same file")

    def test_hashing_ignores_line_endings(self):
        """A CRLF checkout is not divergence, and must never be reported as one."""
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            lf = Path(d) / "lf.txt"
            crlf = Path(d) / "crlf.txt"
            lf.write_bytes(b"one\ntwo\n")
            crlf.write_bytes(b"one\r\ntwo\r\n")
            self.assertEqual(shared_files.digest(lf), shared_files.digest(crlf))


if __name__ == "__main__":
    unittest.main(verbosity=1)
