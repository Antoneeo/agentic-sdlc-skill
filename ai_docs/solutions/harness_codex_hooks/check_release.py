"""Release packaging, version alignment and isolated init smoke; no publishing."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[3]
node = Path(shutil.which("node"))
npm = node.parent / "node_modules/npm/bin/npm-cli.js"
def run(argv, cwd, env=None):
    p = subprocess.run([str(x) for x in argv], cwd=cwd, env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert p.returncode == 0, (argv, p.stdout, p.stderr)
    return p.stdout
results = {}
pack_env = dict(os.environ, NPM_CONFIG_CACHE=str(repo.parent / "f091-release-pack-cache"))
for rel in [".", "distributions/kb-agentic-skill", "distributions/mkt-agentic-sdlc", "distributions/course-creator"]:
    package = repo / rel
    manifest = json.loads((package / "package.json").read_text(encoding="utf-8"))
    gemini = json.loads((package / "gemini-extension.json").read_text(encoding="utf-8"))
    skill_path = next(p for p in manifest["files"] if p.endswith("/SKILL.md"))
    skill = (package / skill_path).read_text(encoding="utf-8")
    assert re.search(r"^version: (.+)$", skill, re.M)[1] == gemini["version"] == manifest["version"]
    packed = json.loads(run([node, npm, "pack", "--dry-run", "--json"], package, pack_env))[0]
    files = {x["path"] for x in packed["files"]}
    assert set(manifest["files"]) <= files, set(manifest["files"]) - files
    assert not any("__pycache__" in p or ".sources/" in p or "/evals/" in p or
                   Path(p).name.startswith("test_") for p in files)
    results[manifest["name"]] = {"version": manifest["version"], "packaged_files": len(files),
                                 "allowlist_complete": True, "dev_artifacts_excluded": True}
with tempfile.TemporaryDirectory(prefix="f091-release-", dir=repo.parent) as temp:
    root = Path(temp)
    project = root / "project"
    project.mkdir()
    env = dict(os.environ)
    for key, rel in [("HOME", "home"), ("USERPROFILE", "home"), ("CODEX_HOME", "home/.codex"),
                     ("CLAUDE_CONFIG_DIR", "home/.claude"), ("GEMINI_HOME", "home/.gemini"),
                     ("ANTIGRAVITY_HOME", "home/.antigravity"), ("AGENTIC_SDLC_KB_ROOT", "home/kb")]:
        env[key] = str(root / rel)
    run(["git", "init", "--quiet"], project, env)
    run([node, repo / "scripts/init.js"], project, env)
    smoke = run([shutil.which("python"), "-B", repo / "skills/agentic-sdlc-skill/scripts/sdlc_check.py",
                 "check", "--root", project], project, env)
    assert "check: CLEAN" in smoke
results["isolated_init"] = "PASS; fresh project check CLEAN"
(repo / "ai_docs/solutions/harness_codex_hooks/release_checks.json").write_text(
    json.dumps(results, indent=2) + "\n", encoding="utf-8")
print(json.dumps(results))
