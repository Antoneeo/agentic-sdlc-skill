"""Installed init idempotence and command latency in the isolated consumer PC."""
import json
import os
from pathlib import Path
import shutil
import statistics
import subprocess
import time

from test_install_upgrade import run

here = Path(__file__).resolve().parent
profile = json.loads((here / "consumer_results.json").read_text(encoding="utf-8"))
root, package = Path(profile["profile"]), Path(profile["package"])
assert root.name.startswith("f091-user-pc-")
home = Path(profile["codex_home"]).parent
env = dict(os.environ)
for key, rel in [("HOME", "."), ("USERPROFILE", "."), ("CODEX_HOME", "codex profile"),
                 ("CLAUDE_CONFIG_DIR", ".claude"), ("GEMINI_HOME", ".gemini"),
                 ("ANTIGRAVITY_HOME", ".antigravity"), ("AGENTIC_SDLC_KB_ROOT", ".agentic-sdlc")]:
    env[key] = str(home / rel)
codex = home / "codex profile/hooks.json"
claude = home / ".claude/settings.json"
before = [p.read_bytes() for p in [codex, claude]]
project = root / "init project"
project.mkdir(exist_ok=True)
run(["git", "init", "--quiet"], project, env)
for _ in range(2):
    out = run([shutil.which("node"), package / "scripts/init.js"], project, env)
    assert "Codex user orientation: already" in out, out
assert [p.read_bytes() for p in [codex, claude]] == before
assert not (project / ".codex/hooks.json").exists()
malformed_overrides = []
for field in ("commandWindows", "command_windows"):
    malformed = json.loads(before[0])
    malformed["hooks"]["SessionStart"][0]["hooks"][0][field] = 123
    text = json.dumps(malformed).encode("utf-8")
    try:
        codex.write_bytes(text)
        out = run([shutil.which("node"), package / "scripts/init.js"], project, env)
        assert "Codex user orientation: malformed" in out, out
        assert codex.read_bytes() == text
        assert claude.read_bytes() == before[1]
        malformed_overrides.append(field)
    finally:
        codex.write_bytes(before[0])  # restore only the synthetic test configuration
settings = json.loads(codex.read_bytes())
payload = {"cwd": str(project)}
timings = {}
for event, groups in settings["hooks"].items():
    for i, group in enumerate(groups):
        command = group["hooks"][0]["command"]
        samples = []
        for _ in range(3):
            start = time.perf_counter()
            value = subprocess.run(command, shell=True, cwd=project, env=env,
                                   input=json.dumps(payload), text=True, capture_output=True)
            assert value.returncode == 0, value.stderr
            samples.append(round((time.perf_counter() - start) * 1000, 1))
        timings[f"{event}:{i}"] = {"samples_ms": samples, "median_ms": statistics.median(samples)}
result = {"init_twice": "PASS", "codex_user_config_byte_identical": True,
          "malformed_override_diagnostics": malformed_overrides,
          "claude_user_config_byte_identical": True, "project_codex_hook_added": False,
          "latency_no_transcript": timings,
          "limit": "Direct installed commands on Windows; not native dispatch or a large transcript benchmark"}
(here / "init_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result))
