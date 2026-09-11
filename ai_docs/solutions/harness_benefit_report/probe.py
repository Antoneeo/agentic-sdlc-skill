#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-050 assertion harness — the benefit report.

**Rebuilt by F-053.** The first cut pinned three counts taken from the LIVE
`REVIEW_LOG.md`, so every review anyone logged rotted it: at F-053's opening it
was red against its own repo with pins 65/613/414 against a log reading
71/662/442, and `review.md` makes a probe that no longer passes a finding. The
repo shipped a standing finding by construction.

The split that fixes it:

  **Ground truth comes from a FROZEN FIXTURE** (`fixture_REVIEW_LOG.md`) — real
  rows copied byte-exact from the log, one per distinct shape the parser must
  handle. The pins describe that file and nothing else, so logging a review
  cannot touch them. They stay integer LITERALS someone edits deliberately: a
  silent parser regression changes the computed side and not the pinned one.

  **The LIVE log is guarded by INVARIANTS** (`invariants()`) — properties true
  of any log at any size: every table row is either parsed or named as
  unparsed, none is dropped in silence, and no parsed row carries an empty
  `tier` or `findings_real` cell (which the parser accepts and the report then
  loses). Those survive a new review; a count cannot.

`ground_truth()` and `invariants()` are module-level and take the log TEXT, so
F-053's harness can call them on synthetic input with known answers — a
function that ignores its argument is exactly the stub that passed the first
attempt to check this.

RED baseline (pre-implementation, 2026-09-10):
  P1 FAIL  no `benefit` subcommand exists
  P2 FAIL  no report to check against the frozen ground truth
  P3 FAIL  nothing states that the report is not a gate
  P4 PASS  invariant: the repo's log parses without silent drops
GREEN target: all PASS.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CODE = REPO / "skills" / "agentic-sdlc-skill"
ENTRY = CODE / "scripts" / "sdlc_check.py"
LIVE_LOG = REPO / "ai_docs" / "audit" / "reviews" / "REVIEW_LOG.md"
FIXTURE = Path(__file__).resolve().parent / "fixture_REVIEW_LOG.md"

# Pins for the FIXTURE, which does not move. Integer literals on purpose:
# derive them from the fixture at import and the drift detector detects
# nothing, because both sides would change together.
TRUE_ROWS = 4
TRUE_FINDINGS = 23
TRUE_DESIGN = 15

FAILS = []


def check(name, cond, detail=""):
    print("%s %s%s" % ("PASS" if cond else "FAIL", name,
                       (" — " + detail) if (detail and not cond) else ""))
    if not cond:
        FAILS.append(name)


def core():
    sys.path.insert(0, str(CODE / "scripts"))
    import sdlc_core
    return sdlc_core


def ground_truth(text):
    """(rows, findings, design) over the rows whose `tier` states a moment.

    Re-implements the parser's assumptions deliberately: it is a DRIFT
    DETECTOR, not an independent check — a wrong assumption shared by both
    would agree with itself. What carries weight is that it runs against a
    frozen file whose expected answer is a literal."""
    WIDE = ["date", "doc_key", "tier", "model", "reviewer", "findings_raised",
            "findings_real", "verdict", "revise_rounds"]
    NARROW = [c for c in WIDE if c != "model"]
    rows = findings = design = 0
    for ln in text.splitlines():
        if not ln.startswith("|") or set(ln) <= set("|-: "):
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
        m = re.match(r"^(\d+)\b", d["findings_real"].strip())
        rows += 1
        findings += int(m.group(1)) if m else 0
        if tier.startswith("design"):
            design += int(m.group(1)) if m else 0
    return rows, findings, design


def invariants(text):
    """-> (ok, why). Properties true of ANY log, whatever its size.

    This is what guards the LIVE log, in place of the counts that rotted.
    `parsed + unparsed == table rows` alone is NOT sufficient: it closes even
    when a row is unreadable, so `unparsed == 0` carries the other half."""
    sc = core()
    rows, unparsed = sc.parse_review_log(text)
    table = [ln for ln in text.splitlines()
             if sc._table_cells(ln) is not None]
    header = [ln for ln in table
              if "tier" in ln.lower() and "verdict" in ln.lower()]
    expected = len(table) - (1 if header else 0)
    if len(rows) + len(unparsed) != expected:
        return False, ("%d parsed + %d unparsed != %d table rows: rows are "
                       "being dropped in silence"
                       % (len(rows), len(unparsed), expected))
    if unparsed:
        return False, ("%d row(s) the parser could not read: %s"
                       % (len(unparsed),
                          "; ".join("line %d: %s" % u for u in unparsed[:3])))
    # Emptiness, not presence. The parser already refuses a row missing
    # `tier` or `findings_real` (REVIEW_CORE), so checking that they EXIST is
    # a tautology -- which is what the first two cuts of this check were: one
    # written `1 if x else 1`, the next a presence test. An EMPTY `tier` cell
    # passes the parser and then silently becomes an unstated moment,
    # deflating the ratio this report exists to state. Nothing else checks it.
    for n, r in enumerate(rows, 1):
        for cell in ("tier", "findings_real"):
            if not (r.get(cell) or "").strip():
                return False, ("row %d has an empty `%s` cell: it parses, and "
                               "then vanishes from every bucket" % (n, cell))
    return True, ""


def run(*args):
    p = subprocess.run([sys.executable, str(ENTRY)] + list(args),
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", cwd=str(REPO))
    return p.returncode, p.stdout + p.stderr


def root_with(log_text):
    """A docs root carrying this log, so `benefit` can be run against it."""
    d = tempfile.mkdtemp()
    root = Path(d)
    (root / "ai_docs" / "audit" / "reviews").mkdir(parents=True)
    (root / "ai_docs" / "audit" / "reviews" / "REVIEW_LOG.md").write_text(
        log_text, encoding="utf-8")
    return root


def main():
    # --- P4 (invariant, run first): the LIVE log still parses cleanly -------
    ok, why = invariants(LIVE_LOG.read_text(encoding="utf-8"))
    check("P4 (drift detector) the live log parses with nothing dropped",
          ok, why)

    # --- P1: the subcommand exists and is registered -------------------------
    rc, out = run("benefit", "--root", str(REPO))
    check("P1a `benefit` runs", rc == 0 and "usage" not in out.lower()[:200],
          "rc=%d out=%r" % (rc, out[:160]))
    _, usage = run("--help")
    check("P1b `benefit` is in the usage text", "benefit" in usage,
          "an unlisted command is one nobody finds")

    # --- P2: the report reproduces the FROZEN ground truth -------------------
    check("P2z the fixture exists and is not the live log",
          FIXTURE.is_file() and FIXTURE.resolve() != LIVE_LOG.resolve(),
          "the pins describe a file that must not move")
    fixture_text = FIXTURE.read_text(encoding="utf-8")
    check("P2y ground_truth() describes the fixture",
          ground_truth(fixture_text) == (TRUE_ROWS, TRUE_FINDINGS, TRUE_DESIGN),
          "fixture reads %s vs pinned %s — if the fixture was regenerated, "
          "that is the direction this check exists to catch"
          % (ground_truth(fixture_text),
             (TRUE_ROWS, TRUE_FINDINGS, TRUE_DESIGN)))
    _, fout = run("benefit", "--root", str(root_with(fixture_text)))
    nums = [int(n.replace(",", "")) for n in re.findall(r"\b\d[\d,]*\b", fout)]
    check("P2a the report reproduces the frozen row count", TRUE_ROWS in nums,
          "expected %d among the reported numbers" % TRUE_ROWS)
    check("P2b the report reproduces the frozen findings total",
          TRUE_FINDINGS in nums, "expected %d" % TRUE_FINDINGS)
    check("P2c the report reproduces the frozen design-caught total",
          TRUE_DESIGN in nums, "expected %d" % TRUE_DESIGN)
    check("P2d the report states how many rows it could NOT parse",
          re.search(r"unparse|could not parse|unparsed", fout, re.I) is not None,
          "a parser that drops rows in silence inflates every ratio it prints")

    # negation control: a malformed row must CHANGE that count. The count is
    # extracted and compared, never searched for: the first cut looked for the
    # word "unparsed" and `\b1\b`, both of which match `rows unparsed: 0`.
    bad = root_with(
        "| date | doc_key | tier | reviewer | findings_raised | "
        "findings_real | verdict | revise_rounds |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| 2026-01-01 | A.md | design | subagent | 2 | 2 | PASS | 1 |\n"
        "| this row | is | malformed |\n")
    rc2, out2 = run("benefit", "--root", str(bad))
    m = re.search(r"rows unparsed:\s*(\d+)", out2)
    check("P2e a malformed row is COUNTED, not skipped",
          rc2 == 0 and m is not None and m.group(1) == "1",
          "unparsed count was %s, expected 1"
          % (m.group(1) if m else "not reported"))
    clean = root_with(
        "| date | doc_key | tier | reviewer | findings_raised | "
        "findings_real | verdict | revise_rounds |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| 2026-01-01 | A.md | design | subagent | 2 | 2 | PASS | 1 |\n")
    _, out3 = run("benefit", "--root", str(clean))
    m3 = re.search(r"rows unparsed:\s*(\d+)", out3)
    check("P2f the unparsed counter reads 0 on a clean log",
          m3 is not None and m3.group(1) == "0",
          "a counter stuck at 1 would pass P2e and mean nothing")

    # --- P5: a Hybrid 10-column row parses (the schema review.md mandates) ---
    hyb = root_with(
        "| date | doc_key | tier | model | instrument | findings_raised "
        "| findings_real | verdict | revise_rounds | notes |\n"
        "|---|---|---|---|---|---|---|---|---|---|\n"
        "| 2026-09-01 | E-ISP x | design | deep | symbol-graph | 5 | 4 | "
        "FAIL | 2 |  |\n")
    _, out4 = run("benefit", "--root", str(hyb))
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
          "never a CI gate" in (CODE / "ENFORCEMENT.md").read_text(
              encoding="utf-8"),
          "unstated, someone will wire it into CI and the number becomes a target")

    print("\n%d probe(s) failing" % len(FAILS) if FAILS else "\nall probes green")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
