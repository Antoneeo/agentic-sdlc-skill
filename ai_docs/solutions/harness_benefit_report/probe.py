#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-050 assertion harness — the benefit report.

The strong probe here is P2: the report is checked against THIS repo's own
REVIEW_LOG, whose true numbers were derived independently before the command
existed. A parser that silently drops rows fails against that ground truth
instead of against its own expectations — which is exactly the defect the
motivating one-off analysis hit (it dropped 61 of 63 rows on its first run,
because the log legally carries two row widths).

RED baseline (pre-implementation, 2026-09-10):
  P1 FAIL  no `benefit` subcommand exists
  P2 FAIL  no report to check against the known ground truth
  P3 FAIL  nothing states that the report is not a gate
  P4 PASS  invariant: the repo's log still holds the ground truth this pins to
GREEN target: all four PASS.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CODE = REPO / "skills" / "agentic-sdlc-skill"
ENTRY = CODE / "scripts" / "sdlc_check.py"

# Pinned figures for this repo's log. Honest about what they are, because the
# closure review made the distinction: `ground_truth()` below re-implements the
# parser's assumptions, so it is a DRIFT DETECTOR, not an independent check --
# a wrong assumption shared by both would agree with itself. What carries real
# weight is that these constants are literals someone updates deliberately: a
# silent parser regression changes the computed side and not the pinned one.
#
# Updated 2026-09-11: 63 -> 65 rows, when this unit logged its own two reviews.
TRUE_ROWS = 65
TRUE_FINDINGS = 613
TRUE_DESIGN = 414

FAILS = []


def check(name, cond, detail=""):
    print("%s %s%s" % ("PASS" if cond else "FAIL", name,
                       (" — " + detail) if (detail and not cond) else ""))
    if not cond:
        FAILS.append(name)


def sc_log(root):
    """The log path the validator uses, relative to a docs root."""
    return Path("ai_docs") / "audit" / "reviews" / "REVIEW_LOG.md"


def run(*args):
    p = subprocess.run([sys.executable, str(ENTRY)] + list(args),
                       capture_output=True, text=True, cwd=str(REPO))
    return p.returncode, p.stdout + p.stderr


def ground_truth():
    """Re-derive the numbers from the log, independently of the command."""
    log = (REPO / "ai_docs" / "audit" / "reviews" / "REVIEW_LOG.md").read_text(
        encoding="utf-8")
    WIDE = ["date", "doc_key", "tier", "model", "reviewer", "findings_raised",
            "findings_real", "verdict", "revise_rounds"]
    NARROW = [c for c in WIDE if c != "model"]
    rows, findings, design = 0, 0, 0
    for ln in log.splitlines():
        if not ln.startswith("|") or ln.startswith("|---"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        names = WIDE if len(cells) == 9 else NARROW if len(cells) == 8 else None
        if not names:
            continue
        d = dict(zip(names, cells))
        if not re.match(r"\d{4}-\d{2}-\d{2}$", d["date"]):
            continue
        tier = d["tier"].lower()
        if not tier.startswith(("design", "closure")):
            continue
        m = re.search(r"\d+", d["findings_real"])
        n = int(m.group()) if m else 0
        rows += 1
        findings += n
        if tier.startswith("design"):
            design += n
    return rows, findings, design


def main():
    # --- P4 (invariant, run first): the ground truth still holds -------------
    rows, findings, design = ground_truth()
    check("P4 (drift detector) the log still matches the pinned figures",
          (rows, findings, design) == (TRUE_ROWS, TRUE_FINDINGS, TRUE_DESIGN),
          "log now reads %d/%d/%d vs pinned %d/%d/%d — if reviews were added, "
          "update the constants deliberately; do not loosen the check"
          % (rows, findings, design, TRUE_ROWS, TRUE_FINDINGS, TRUE_DESIGN))

    # --- P1: the subcommand exists and is registered -------------------------
    rc, out = run("benefit", "--root", str(REPO))
    check("P1a `benefit` runs", rc == 0 and "usage" not in out.lower()[:200],
          "rc=%d out=%r" % (rc, out[:160]))
    _, usage = run("--help")
    check("P1b `benefit` is in the usage text", "benefit" in usage,
          "an unlisted command is one nobody finds")

    # --- P2: the report reproduces the independently derived numbers ---------
    nums = [int(n.replace(",", "")) for n in re.findall(r"\b\d[\d,]*\b", out)]
    check("P2a the report reproduces the true row count", TRUE_ROWS in nums,
          "expected %d among the reported numbers" % TRUE_ROWS)
    check("P2b the report reproduces the true findings total",
          TRUE_FINDINGS in nums, "expected %d" % TRUE_FINDINGS)
    check("P2c the report reproduces the design-caught total",
          TRUE_DESIGN in nums, "expected %d" % TRUE_DESIGN)
    check("P2d the report states how many rows it could NOT parse",
          re.search(r"unparse|could not parse|unparsed", out, re.I) is not None,
          "a parser that drops rows in silence inflates every ratio it prints")
    # negation control: a log with one malformed row must change that count
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "ai_docs" / "audit" / "reviews").mkdir(parents=True)
        (root / "ai_docs" / "audit" / "reviews" / "REVIEW_LOG.md").write_text(
            "| date | doc_key | tier | reviewer | findings_raised | "
            "findings_real | verdict | revise_rounds |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| 2026-01-01 | A.md | design | subagent | 2 | 2 | PASS | 1 |\n"
            "| this row | is | malformed |\n", encoding="utf-8")
        rc2, out2 = run("benefit", "--root", str(root))
        # The count is EXTRACTED and compared, not merely looked for: the first
        # cut of this probe searched for `\b1\b` and the word "unparsed", and
        # both match a report that says `rows unparsed: 0` -- so a parser that
        # dropped the row in silence passed the probe written to catch it.
        m = re.search(r"rows unparsed:\s*(\d+)", out2)
        check("P2e a malformed row is COUNTED, not skipped",
              rc2 == 0 and m is not None and m.group(1) == "1",
              "unparsed count was %s, expected 1"
              % (m.group(1) if m else "not reported"))
        # and the counter must be able to read 0: a probe that only ever sees
        # a non-zero count cannot tell a working counter from a stuck one.
        (root / sc_log(root)).write_text(
            "| date | doc_key | tier | reviewer | findings_raised | "
            "findings_real | verdict | revise_rounds |\n"
            "|---|---|---|---|---|---|---|---|\n"
            "| 2026-01-01 | A.md | design | subagent | 2 | 2 | PASS | 1 |\n",
            encoding="utf-8")
        _, out3 = run("benefit", "--root", str(root))
        m3 = re.search(r"rows unparsed:\s*(\d+)", out3)
        check("P2f the unparsed counter reads 0 on a clean log",
              m3 is not None and m3.group(1) == "0",
              "a counter stuck at 1 would pass P2e and mean nothing")

    # --- P5: a Hybrid 10-column row parses (the schema review.md mandates) ---
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "ai_docs" / "audit" / "reviews").mkdir(parents=True)
        (root / sc_log(root)).write_text(
            "| date | doc_key | tier | model | instrument | findings_raised "
            "| findings_real | verdict | revise_rounds | notes |\n"
            "|---|---|---|---|---|---|---|---|---|---|\n"
            "| 2026-09-01 | E-ISP x | design | deep | symbol-graph | 5 | 4 | "
            "FAIL | 2 |  |\n", encoding="utf-8")
        _, out4 = run("benefit", "--root", str(root))
        m4 = re.search(r"rows parsed:\s*(\d+)\s+rows unparsed:\s*(\d+)", out4)
        check("P5 a doctrine-conformant Hybrid row parses",
              m4 is not None and (m4.group(1), m4.group(2)) == ("1", "0"),
              "a devPNT row carries `instrument`/`notes` and NO `reviewer` -- "
              "reading by width reports the whole log as unparsed")

    # --- P6: the cost side is never silently absent -------------------------
    _, out5 = run("benefit", "--root", str(REPO))
    check("P6 the read-cost line is printed with the benefit",
          re.search(r"Read cost", out5) is not None,
          "a catch rate quoted without its cost is what this report exists "
          "to prevent")

    # --- P3: it is a report, never a gate ------------------------------------
    check("P3a exit code is 0 even with no log at all",
          run("benefit", "--root", tempfile.mkdtemp())[0] == 0,
          "a measurement that can fail a build becomes a target")
    check("P3b the doctrine says it is not a gate",
          "never a CI gate" in (CODE / "ENFORCEMENT.md").read_text(encoding="utf-8"),
          "unstated, someone will wire it into CI and the number becomes a target")

    print("\n%d probe(s) failing" % len(FAILS) if FAILS else "\nall probes green")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
