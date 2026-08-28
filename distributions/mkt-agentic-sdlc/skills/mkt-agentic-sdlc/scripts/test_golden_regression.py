#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Golden non-regression for mkt_check.py -- the Poka-Yoke for this distribution.

Same instrument as the code distribution's TS1, pointed at this validator: a FROZEN
marketing project plus a transcript of what the SHIPPED validator says about it. Its
whole job is to make a regression impossible to introduce silently while the family
converges on a shared core -- an existing mkt project must keep getting the same
findings and the same exit codes, and if it does not, the diff says so before a user
does.

    python scripts/test_golden_regression.py                  # assert
    python scripts/test_golden_regression.py --update-baseline

Regenerate the baseline ONLY when the change of behaviour is intended, declared and
reviewed. Silently refreshing it turns the whole test into decoration.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "mkt_check.py"
FIXTURE = HERE / "fixtures" / "golden_mkt_docs"
BASELINE = HERE / "fixtures" / "golden_baseline.txt"

GENERATED = ("mkt_docs/INDEX.md",)

# (label, argv-before --root). Every shipped subcommand, so none can quietly change.
COMMANDS = (
    ("validate", ["validate"]),
    ("validate --strict", ["validate", "--strict"]),
    ("ledger", ["ledger"]),
    ("budget", ["budget"]),
    ("funnel", ["funnel"]),
    ("trace", ["trace"]),
    ("check", ["check"]),
    ("check --strict", ["check", "--strict"]),
    ("index", ["index"]),
)


def materialize(dest):
    shutil.copytree(FIXTURE, dest, dirs_exist_ok=True)


def normalize(text, root):
    root = str(root)
    for variant in (root, root.replace("\\", "/"), root.replace("\\", "\\\\")):
        text = text.replace(variant, "<ROOT>")
    text = text.replace("\\", "/")
    return re.sub(r"\r\n?", "\n", text)


def run_corpus():
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        materialize(root)
        # F-042: check's hook detection also reads the machine-global user
        # settings; without the seam the baseline would differ on any dev
        # machine that has a real global hook -- nondeterminism by construction.
        env = {**os.environ,
               "AGENTIC_SDLC_USER_SETTINGS": str(root / "no-user-settings.json")}
        env.pop("CLAUDE_CONFIG_DIR", None)
        for label, argv in COMMANDS:
            proc = subprocess.run(
                [sys.executable, str(VALIDATOR), *argv, "--root", str(root)],
                env=env,
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
            body = normalize((proc.stdout or "") + (proc.stderr or ""), root)
            out.append(f"===== {label} (rc={proc.returncode}) =====\n{body.rstrip()}\n")
        for rel in GENERATED:
            produced = (root / rel).read_text(encoding="utf-8")
            out.append(f"===== generated {rel} =====\n{normalize(produced, root).rstrip()}\n")
    return "\n".join(out)


class GoldenRegression(unittest.TestCase):

    def test_baseline_exists(self):
        self.assertTrue(
            BASELINE.is_file(),
            f"baseline missing: capture it from the PRE-change validator with "
            f"`python {Path(__file__).name} --update-baseline`",
        )

    def test_transcript_matches_baseline(self):
        expected = BASELINE.read_text(encoding="utf-8")
        actual = run_corpus()
        if expected == actual:
            return
        exp_lines = expected.splitlines()
        act_lines = actual.splitlines()
        diff = [f"  -{l}" for l in exp_lines if l not in act_lines][:12]
        diff += [f"  +{l}" for l in act_lines if l not in exp_lines][:12]
        self.fail(
            "the validator's behaviour on an unchanged marketing project CHANGED.\n"
            "If that is intended, say so in the ANALYSIS and re-capture the baseline;\n"
            "if it is not, the change is a regression for every existing mkt user.\n"
            + "\n".join(diff)
        )

    def test_every_shipped_subcommand_is_covered(self):
        """A subcommand missing from COMMANDS is a subcommand nothing protects."""
        src = VALIDATOR.read_text(encoding="utf-8")
        declared = re.search(r'OVERLAY_COMMANDS = \(([^)]+)\)', src)
        self.assertTrue(declared, "could not read the subcommand list from mkt_check.py")
        names = {n.strip().strip('"\'') for n in declared.group(1).split(",") if n.strip()}
        covered = {argv[0] for _, argv in COMMANDS}
        self.assertEqual(names - covered, set(),
                         "these subcommands ship but are not in the golden transcript")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--update-baseline", action="store_true",
                    help="capture the transcript as the new baseline (intended changes only)")
    args, rest = ap.parse_known_args()
    if args.update_baseline:
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(run_corpus(), encoding="utf-8", newline="\n")
        print(f"[ok] baseline captured: {BASELINE}")
        return 0
    return 0 if unittest.main(argv=[sys.argv[0], *rest], exit=False).result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
