"""F-087 probes: does `validate` notice an L3 unit implemented without the owner's design approval?

Run from the repository root:
    python ai_docs/solutions/harness_owner_design_approval/probe.py

Each fixture is a minimal Standalone project with one L3 ANALYSIS, its design-review
row and its request record. On the baseline (code lens 1.49.0) the RED probes fail:
`validate` says nothing when the request record holds no design-approval entry. The
guards pass on both sides: no advisory before implementation, below L3, before the
epoch, in Hybrid, or when the approval entry exists.

The doctrine half of F-087 is probed separately, by replaying the behavioral scenario
`skills/agentic-sdlc-skill/evals/scenarios/design_approved_before_code.md` against
the old and the new skill text (results in the ANALYSIS Diary).
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CHECK = REPO / "skills/agentic-sdlc-skill/scripts/sdlc_check.py"
MARK = "design approval"     # the advisory names the missing act; the probe keys on it

ANALYSIS = """---
id: F-001
feature: CSV export
status: {status}
level: {level}
start_date: {start}
---
# Analysis: CSV export

## Objective
Analysts export the open report as CSV.

## Diary / Current State
**{start} — design drafted.** Review requested.
"""

REQUEST = """---
unit: F-001
analysis: ANALYSIS_export_csv.md
---
# Request record: CSV export

### R1 — 2026-11-02 — opening request
> let analysts download the open report as CSV
{extra}"""

LOG = """| date | doc_key | tier | model | instrument | findings_raised | findings_real | verdict | revise_rounds | notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-02 | solutions/ANALYSIS_export_csv.md | design | deep (fresh subagent) | rung 1 | 1 | 1 | FAIL -> PASS | 2 | fixed |
"""


def run(status="IN_PROGRESS", level="L3", start="2026-11-02", extra="", hybrid=False,
        strict=False, request=True, raw=False):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        ai = root / "ai_docs"
        for sub in ("solutions", "audit/requests", "audit/reviews"):
            (ai / sub).mkdir(parents=True)
        (ai / "solutions/ANALYSIS_export_csv.md").write_text(
            ANALYSIS.format(status=status, level=level, start=start), encoding="utf-8")
        if request:
            (ai / "audit/requests/REQUEST_export_csv.md").write_text(
                REQUEST.format(extra=extra), encoding="utf-8")
        (ai / "audit/reviews/REVIEW_LOG.md").write_text(LOG, encoding="utf-8")
        args = [sys.executable, str(CHECK), "validate", "--root", str(root)]
        if hybrid:
            args.append("--hybrid")
        if strict:
            args.append("--strict")
        r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
        hits = [ln for ln in r.stdout.splitlines() if "ANALYSIS_export_csv" in ln and MARK in ln]
        return (r.returncode, hits) if raw else hits


APPROVED = "\n### R2 — 2026-11-02 — design approved\n> procedi\n"


class Probes(unittest.TestCase):
    def test_red_implemented_without_approval_is_noticed(self):
        self.assertTrue(run(), "an L3 in implementation with no design-approval entry must be noticed")

    def test_red_completed_without_approval_is_noticed(self):
        self.assertTrue(run(status="COMPLETED"))

    def test_guard_approval_entry_silences_it(self):
        self.assertEqual(run(extra=APPROVED), [])

    def test_guard_label_is_matched_case_insensitively_at_its_start(self):
        self.assertEqual(run(extra=APPROVED.replace("design approved", "Design approved by the owner")), [])

    def test_red_label_elsewhere_does_not_count(self):
        self.assertTrue(run(extra="\n### R2 — 2026-11-02 — question before the design approved\n> ok\n"))

    def test_red_missing_request_record_is_noticed(self):
        self.assertTrue(run(request=False))

    def test_red_note_never_fails_strict(self):
        rc_missing, hits = run(strict=True, raw=True)
        rc_approved, _ = run(strict=True, raw=True, extra=APPROVED)
        self.assertTrue(hits and all(h.startswith("[note]") for h in hits),
                        "the notice is an advisory ([note]), never a warning or an error")
        self.assertEqual(rc_missing, rc_approved,
                         "--strict must exit the same with or without the approval entry: "
                         "the advisory never changes the outcome (the fixture has unrelated findings)")

    def test_guard_started_the_day_the_rule_was_written(self):
        self.assertEqual(run(start="2026-10-30"), [],
                         "epoch is the day after: parallel units opened that day never saw the rule")

    def test_guard_planned_is_not_late(self):
        self.assertEqual(run(status="PLANNED"), [])

    def test_guard_below_l3(self):
        self.assertEqual(run(level="L2"), [])

    def test_guard_before_epoch(self):
        self.assertEqual(run(start="2026-10-01"), [])

    def test_guard_hybrid_is_approved_in_devpnt(self):
        self.assertEqual(run(hybrid=True), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
