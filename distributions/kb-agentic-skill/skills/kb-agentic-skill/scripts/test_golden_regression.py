#!/usr/bin/env python3
"""TS1 -- golden non-regression for the validator.

This is the only evidence that a user who did nothing is not paying for the
multi-domain refactor. It runs the shipped subcommands over a FROZEN corpus
(`fixtures/golden_ai_docs/`) and compares every line of output, every exit code
and every generated file against a baseline captured from the PRE-change
validator. A diff here means an existing project's experience changed.

    python scripts/test_golden_regression.py                  # assert
    python scripts/test_golden_regression.py --update-baseline

Regenerate the baseline ONLY when the change of behaviour is intended, declared
and reviewed. Silently refreshing it turns the whole test into decoration.

The corpus carries no `domain:` and no `default_domain:` other than the seeded
`code`, which is the point: it is also the proof that the domain column is not
emitted on a tree that never asked for one.
"""

import os
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "sdlc_check.py"
FIXTURE = HERE / "fixtures" / "golden_ai_docs"
BASELINE = HERE / "fixtures" / "golden_baseline.txt"

# Generated files: byte-compared after `index` re-runs over the materialized tree.
GENERATED = (
    "ai_docs/strategic/features_history.md",
    "ai_docs/INDEX.md",
    "ai_docs/reference/INDEX.md",
)

# (label, argv-after-the-script). --root is appended by the runner, except for
# claim-id, which takes positional args and computes a pure hash (no fs access).
COMMANDS = (
    ("validate", ["validate"]),
    ("validate --strict", ["validate", "--strict"]),
    ("check", ["check"]),
    ("check --hybrid", ["check", "--hybrid"]),
    ("stale", ["stale"]),
    ("orient", ["orient"]),
    ("index", ["index"]),
    # F-024/F-025: the kb overlay surface. On this corpus (no topics/, no
    # corpus/) graph and corpus report "nothing to check" and index emits no
    # extra line — that IS the non-regression guarantee, frozen here.
    ("graph", ["graph"]),
    ("corpus", ["corpus"]),
    ("claim-id", ["claim-id", "corpus/given/example.txt", "L1-2"]),
)
NO_ROOT = {"claim-id"}


def materialize(dest):
    """Copy the frozen corpus into a scratch tree.

    One substitution only: the handoff date. `validate` prints the handoff's age
    in days, so a frozen date would make the output drift by one line per day —
    the corpus stays frozen and the runner supplies today.
    """
    shutil.copytree(FIXTURE, dest, dirs_exist_ok=True)
    handoff = Path(dest) / "ai_docs" / "audit" / "handoff.md"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    handoff.write_bytes(handoff.read_text(encoding="utf-8")
                        .replace("{{TODAY}}", today).encode("utf-8"))


def normalize(text, root):
    """Strip everything that is a property of WHERE the test ran, not of what it found."""
    root = str(root)
    for variant in (root, root.replace("\\", "/"), root.replace("\\", "\\\\")):
        text = text.replace(variant, "<ROOT>")
    text = text.replace("\\", "/")
    text = re.sub(r"\r\n?", "\n", text)
    # `orient` echoes the handoff, which carries the date substituted above.
    text = re.sub(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", "<UTC>", text)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return text.replace(today, "<TODAY>")


def run_corpus():
    """Return the full transcript of the shipped surface over the frozen corpus."""
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
            cmd = [sys.executable, str(VALIDATOR), *argv]
            if label not in NO_ROOT:
                cmd += ["--root", str(root)]
            proc = subprocess.run(
                cmd, env=env,
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
            body = normalize((proc.stdout or "") + (proc.stderr or ""), root)
            out.append(f"===== {label} (rc={proc.returncode}) =====\n{body.rstrip()}\n")
        # `index` ran last: the generated files must come back byte-identical to
        # the committed ones, or the generator's output changed.
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
            "the validator's behaviour on an unchanged project CHANGED.\n"
            "If that is intended, say so in the ANALYSIS and re-capture the baseline;\n"
            "if it is not, the change is a regression for every existing user.\n"
            + "\n".join(diff)
        )

    def test_baseline_is_additions_only_over_the_frozen_snapshot(self):
        """The re-recorded baseline must CONTAIN the 1.0 snapshot, in order.

        A baseline compared only against itself proves nothing: this pins the
        pre-F-024 transcript as a permanent fixture and asserts every line of
        it survives verbatim — new commands may only append."""
        frozen = HERE / "fixtures" / "golden_baseline_frozen_1_0.txt"
        self.assertTrue(frozen.is_file(), "the frozen 1.0 snapshot is a fixture")
        old = frozen.read_text(encoding="utf-8").splitlines()
        new = BASELINE.read_text(encoding="utf-8").splitlines()
        it = iter(new)
        missing = [l for l in old if l not in it]
        self.assertEqual(missing, [],
                         "lines of the frozen baseline no longer appear, in order, "
                         "in the current one — an existing user would see a change")

    def test_no_domain_column_on_a_tree_that_declares_none(self):
        """The syntactic column predicate, asserted from the outside."""
        history = (FIXTURE / "ai_docs" / "strategic" / "features_history.md").read_text(encoding="utf-8")
        header = next((l for l in history.splitlines() if l.startswith("|")), "")
        self.assertNotIn("domain", header.lower(),
                         "no artifact in the corpus writes `domain:`, so no column may be emitted")


class CopiedFileRecipe(unittest.TestCase):
    """TS12 -- the ENFORCEMENT.md §2 CI recipe, executed as documented.

    The recipe is a promise to every team that put the validator in its pipeline.
    Splitting the validator in two could break it silently; this runs it."""

    def _run(self, tools, corpus):
        return subprocess.run(
            [sys.executable, str(Path(tools) / "sdlc_check.py"), "validate", "--root", str(corpus)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )

    def test_both_files_copied_behaves_like_the_installed_validator(self):
        with tempfile.TemporaryDirectory() as tmp:
            corpus = Path(tmp) / "project"
            materialize(corpus)
            tools = Path(tmp) / "tools"
            tools.mkdir()
            for name in ("sdlc_check.py", "sdlc_core.py"):
                shutil.copy2(HERE / name, tools / name)
            copied = self._run(tools, corpus)
            in_place = subprocess.run(
                [sys.executable, str(HERE / "sdlc_check.py"), "validate", "--root", str(corpus)],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
            self.assertEqual(copied.returncode, in_place.returncode)
            self.assertEqual(normalize(copied.stdout, corpus), normalize(in_place.stdout, corpus))

    def test_copying_only_the_entry_point_fails_loudly(self):
        with tempfile.TemporaryDirectory() as tmp:
            corpus = Path(tmp) / "project"
            materialize(corpus)
            tools = Path(tmp) / "tools"
            tools.mkdir()
            shutil.copy2(HERE / "sdlc_check.py", tools / "sdlc_check.py")  # the core left behind
            proc = self._run(tools, corpus)
            self.assertNotEqual(proc.returncode, 0, "a half-copied validator must never be green")
            self.assertIn("sdlc_core.py", proc.stderr)

    def test_the_core_alone_is_runnable(self):
        """Stated in ENFORCEMENT §2, so it is asserted rather than assumed."""
        with tempfile.TemporaryDirectory() as tmp:
            corpus = Path(tmp) / "project"
            materialize(corpus)
            proc = subprocess.run(
                [sys.executable, str(HERE / "sdlc_core.py"), "validate", "--root", str(corpus)],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


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
