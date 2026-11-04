"""Run changed shared contracts and real entry-point smoke for one distribution."""
from pathlib import Path
import subprocess
import sys

repo = Path(__file__).resolve().parents[3]
scripts = (repo / sys.argv[1]).resolve()
entry_point = sys.argv[2] if len(sys.argv) > 2 else "sdlc_check.py"
result = subprocess.run([sys.executable, "-B", "-m", "unittest", "test_verdict",
                         "test_constraints", "test_session_start", "test_drift"],
                        cwd=scripts, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
smoke = subprocess.run([sys.executable, "-B", str(scripts / entry_point),
                        "constraints", "--unit", "F-091", "--root", str(repo)],
                       cwd=repo, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
assert smoke.returncode == 0, smoke.stderr
assert "P1" in smoke.stdout and "P6" in smoke.stdout
print("Installed entry-point composition / F-091 constraints: PASS")
