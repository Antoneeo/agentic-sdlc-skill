"""Run a falsifiable synthetic experiment, not a wording/presence check.

Exit 1 means at least one acceptance assertion failed. --variant reference is
only a positive control for the oracle; it says nothing about agent behaviour.
"""
import argparse
import json
from pathlib import Path
import sys

from fixture import baseline_outcome, deliver, read_catalogue, read_summary, reference_outcome


def run(variant):
    classifier = baseline_outcome if variant == "baseline" else reference_outcome
    cases = [
        ("complete_catalogue", "read_catalogue", read_catalogue(["Atlas", "Orion"]), False,
         {"state": "delivered", "content": "Atlas\nOrion"}),
        ("empty_complete_catalogue", "read_catalogue", read_catalogue([]), False,
         {"state": "delivered", "content": ""}),
        ("complete_summary", "read_summary", read_summary(["Atlas"]), False,
         {"state": "delivered", "content": "Atlas"}),
        ("declared_failure", "read_catalogue", {"status": "failed", "records": []}, False,
         {"state": "blocked", "content": None}),
        ("partial_catalogue", "read_catalogue", {"records": ["Atlas"], "complete": False}, False,
         {"state": "blocked", "content": None}),
        ("malformed_catalogue", "read_catalogue", {"records": "Atlas", "complete": True}, False,
         {"state": "blocked", "content": None}),
        ("unknown_contract", "other", {"records": ["Atlas"]}, False,
         {"state": "blocked", "content": None}),
        ("stop_dominates", "read_summary", read_summary(["Atlas"]), True,
         {"state": "stopped", "content": None}),
    ]
    results = []
    for name, command, payload, stopped, expected in cases:
        try:
            observed = deliver(command, payload, classify=classifier, stopped=stopped)
            results.append(dict(case=name, expected=expected, observed=observed,
                                passed=observed == expected))
        except Exception as error:
            results.append(dict(case=name, expected=expected, error=type(error).__name__, passed=False))
    return dict(variant=variant, scope="synthetic functional mechanism only", cases=results,
                passed=sum(r["passed"] for r in results), total=len(results))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=("baseline", "reference"), default="baseline")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.variant)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    sys.exit(0 if result["passed"] == result["total"] else 1)
