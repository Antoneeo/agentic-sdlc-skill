from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[3]
ns = {}
retry_path = root / "inputs/retry.py"
exec(compile(retry_path.read_text(), str(retry_path), "exec"), ns)
config = json.loads((root / "inputs/retry-config.json").read_text())
results = {}
for name, sequence in [("false_false_true", [False, False, True]), ("first_true", [True]), ("always_false", [False, False, False])]:
    calls = []
    def operation():
        calls.append(len(calls))
        return sequence[len(calls)-1]
    results[name] = {"returned": ns["attempt"](operation, config), "calls": len(calls)}
assert results["false_false_true"] == {"returned": True, "calls": 3}
assert results["first_true"] == {"returned": True, "calls": 1}
assert results["always_false"] == {"returned": False, "calls": 3}
identity_path = root / "inputs/identity.py"
exec(compile(identity_path.read_text(), str(identity_path), "exec"), ns)
results["identity_original_A_current_B"] = ns["identity"]({"original_id": "A", "current_id": "B"})
assert results["identity_original_A_current_B"] == "A"
negative_control = 0
for actual, wrong in [(results["always_false"]["calls"], 5), (results["identity_original_A_current_B"], "B")]:
    try:
        assert actual == wrong
    except AssertionError:
        negative_control += 1
assert negative_control == 2
results["intentional_wrong_assertions_rejected"] = negative_control
results["scope"] = "Local fixture only; no card integration or external services"
results["source_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root / "inputs").iterdir()) if p.is_file()}
print(json.dumps(results, indent=2))
