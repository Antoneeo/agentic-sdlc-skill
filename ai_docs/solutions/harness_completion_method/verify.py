"""Re-run the experiment and verify frozen input integrity.

Exit 0 certifies the recorded RED/control pattern, not a healthy baseline or an
improved methodology. Individual command exit codes and outputs are preserved.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
for relative, metadata in manifest.items():
    actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    if actual != metadata["sha256"]:
        raise SystemExit(f"Frozen input changed: {relative}")

commands = [
    ("existing_smoke", ["existing_smoke.py"], 0),
    ("functional_red", ["probe.py", "--variant", "baseline"], 1),
    ("functional_green", ["probe.py", "--variant", "reference"], 0),
    ("mediation", ["mediation.py"], 0),
]
results = []
for name, args, expected_exit in commands:
    result = subprocess.run([sys.executable, "-B", *args], cwd=ROOT,
                            capture_output=True, text=True, encoding="utf-8")
    record = dict(name=name, command=["python", "-B", *args], exit_code=result.returncode,
                  expected_exit=expected_exit, stdout=result.stdout, stderr=result.stderr)
    results.append(record)
    print(f"{name}: exit={result.returncode}, expected={expected_exit}")
    if result.returncode != expected_exit:
        raise SystemExit(f"Unexpected experiment result: {name}\n{result.stdout}\n{result.stderr}")
    if name in ("functional_red", "functional_green"):
        payload = json.loads(result.stdout)
        failures = {case["case"] for case in payload["cases"] if not case["passed"]}
        expected = {"complete_catalogue", "empty_complete_catalogue"} if name == "functional_red" else set()
        assert failures == expected, (failures, expected)
        assert payload["total"] == 8
(ROOT / "results" / "functional_runs.json").write_text(
    json.dumps(results, indent=2) + "\n", encoding="utf-8")
print("Frozen inputs verified; the faulty baseline remains RED, reference control is GREEN.")
