"""Explicit cleanup of the latest tarball's disposable fresh-install profile."""
import json
import os
from pathlib import Path
import shutil

from test_install_upgrade import run

here = Path(__file__).resolve().parent
consumer = json.loads((here / "consumer_results.json").read_text(encoding="utf-8"))
root = Path(consumer["profile"])
assert root.name.startswith("f091-user-pc-")
home = root / "Fresh PC User"
env = dict(os.environ)
for key, rel in [("HOME", "."), ("USERPROFILE", "."), ("CODEX_HOME", "codex profile"),
                 ("CLAUDE_CONFIG_DIR", ".claude"), ("GEMINI_HOME", ".gemini"),
                 ("ANTIGRAVITY_HOME", ".antigravity"), ("AGENTIC_SDLC_KB_ROOT", ".agentic-sdlc")]:
    env[key] = str(home / rel)
file = home / "codex profile/hooks.json"
settings = json.loads(file.read_bytes())
foreign = {"hooks": [{"type": "command", "command": "echo F091_foreign"}]}
settings["hooks"]["SessionStart"].append(foreign)
file.write_text(json.dumps(settings), encoding="utf-8")
package = root / "fresh-prefix" / ("node_modules" if os.name == "nt" else "lib/node_modules") / "@antoneeo/agentic-sdlc-skill"
run([shutil.which("node"), package / "scripts/preuninstall.js"], root, env)
after = json.loads(file.read_bytes())
assert after["hooks"] == {"SessionStart": [foreign]}, after
result = {"status": "PASS", "tarball": "latest retained consumer fresh-install fixture",
          "explicit_preuninstall": True, "all_owned_codex_handlers_removed": True,
          "foreign_handler_preserved": True, "real_profile_touched": False}
(here / "final_cleanup_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result))
