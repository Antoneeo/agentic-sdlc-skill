"""Recount the diagnostic sequences; does not score causal reasoning."""
import hashlib
import json
from pathlib import Path
from probe import DATA

ROOT = Path(__file__).resolve().parent
SEQUENCES = {
    "baseline": {"A": ["reproduce", "logs", "effective_config"], "B": ["effective_config", "dns"], "C": ["reproduce", "incident_trace", "schema", "source"], "D": ["trace", "source", "consumers", "contracts"]},
    "candidate_initial": {"A": ["logs", "effective_config"], "B": ["effective_config", "dns"], "C": ["incident_trace", "schema", "source", "reproduce"], "D": ["trace", "source", "contracts", "consumers"]},
}

def main():
    hashes = json.loads((ROOT / "FROZEN.json").read_text(encoding="utf-8"))
    for name, expected in hashes.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    totals = {}
    for variant, cases in SEQUENCES.items():
        costs = {case: sum(DATA[case][check][0] for check in checks) for case, checks in cases.items()}
        totals[variant] = {"case_costs": costs, "checks": sum(map(len, cases.values())), "total_cost": sum(costs.values())}
    assert totals["baseline"]["total_cost"] == 22
    assert totals["candidate_initial"]["total_cost"] == 17
    print(json.dumps(totals, indent=2))

if __name__ == "__main__":
    main()
