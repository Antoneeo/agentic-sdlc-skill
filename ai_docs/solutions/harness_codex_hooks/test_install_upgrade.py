"""Consumer acceptance: pack, npm global install/upgrade, installed hook execution.

Only synthetic PC homes/prefixes/configs are used. No trust grant or real user
profile mutation. --keep leaves the isolated PC for inspection with Codex.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

BASELINE_REF = "74c1833f1b08b2bff57f3ba5824465e0a4abb767"


def run(argv, cwd, env):
    result = subprocess.run([str(a) for a in argv], cwd=cwd, env=env,
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise AssertionError(f"{argv[0]} failed ({result.returncode}):\n{result.stdout}\n{result.stderr}")
    return result.stdout


def package_copy(repo, target, baseline=False):
    manifest = json.loads(subprocess.check_output(["git", "show", f"{BASELINE_REF}:package.json"], cwd=repo)
                          if baseline else (repo / "package.json").read_bytes())
    files = ["package.json", *manifest["files"]]
    for rel in files:
        if baseline:
            names = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASELINE_REF, "--", rel], cwd=repo, text=True).splitlines()
        else:
            p = repo / rel
            names = [str(x.relative_to(repo)).replace("\\", "/") for x in p.rglob("*") if x.is_file()] if p.is_dir() else [rel]
        for name in names:
            dest = target / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(subprocess.check_output(["git", "show", f"{BASELINE_REF}:{name}"], cwd=repo)
                             if baseline else (repo / name).read_bytes())
    if not baseline:
        # Before the release bump, use a distinct fixture version. A prepared
        # release is tested with its actual version and installed SKILL metadata.
        if manifest["version"] == "1.52.0":
            manifest["version"] = "1.52.1-f091-test"
        (target / "package.json").write_text(json.dumps(manifest), encoding="utf-8")


def handlers(settings):
    return [h for groups in settings.get("hooks", {}).values() for group in groups for h in group.get("hooks", [])]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep", action="store_true")
    parser.add_argument("--report", default="consumer_results.json")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[3]
    root = Path(tempfile.mkdtemp(prefix="f091-user-pc-")).resolve()
    assert root.is_relative_to(Path(tempfile.gettempdir()).resolve())
    node = Path(shutil.which("node"))
    npm = next((p for p in [node.parent / "node_modules/npm/bin/npm-cli.js",
                            Path(shutil.which("npm.cmd") or shutil.which("npm")).parent / "node_modules/npm/bin/npm-cli.js"] if p.is_file()), None)
    assert npm, "npm CLI not found beside the installed Node/npm launcher"
    npm_command = [node, npm]
    env = dict(os.environ)
    home = root / "PC User"
    for key, rel in [("HOME", "."), ("USERPROFILE", "."), ("CODEX_HOME", "codex profile"),
                     ("CLAUDE_CONFIG_DIR", ".claude"), ("GEMINI_HOME", ".gemini"),
                     ("ANTIGRAVITY_HOME", ".antigravity"), ("AGENTIC_SDLC_KB_ROOT", ".agentic-sdlc")]:
        env[key] = str(home / rel)
    home.mkdir()
    userconfig = root / "empty-npmrc"
    userconfig.write_text("", encoding="utf-8")
    env.update({"NPM_CONFIG_USERCONFIG": str(userconfig), "NPM_CONFIG_CACHE": str(root / "cache"),
                "NPM_CONFIG_AUDIT": "false", "NPM_CONFIG_FUND": "false", "NPM_CONFIG_UPDATE_NOTIFIER": "false"})
    prefix = root / "npm-prefix"
    tarballs = []
    for name, baseline in [("baseline", True), ("candidate", False)]:
        target = root / name
        package_copy(repo, target, baseline)
        output = run(npm_command + ["pack", "--json", "--pack-destination", root], target, env)
        tarballs.append(root / json.loads(output)[0]["filename"])
    install_args = npm_command + ["install", "--global", "--prefix", prefix, "--no-audit", "--no-fund"]
    run(install_args + [tarballs[0]], root, env)
    claude_file = Path(env["CLAUDE_CONFIG_DIR"]) / "settings.json"
    before_claude = claude_file.read_bytes()
    codex_file = Path(env["CODEX_HOME"]) / "hooks.json"
    assert not codex_file.exists(), "Baseline unexpectedly already wires Codex"
    output = run(install_args + [tarballs[1]], root, env)
    assert claude_file.read_bytes() == before_claude, "Upgrade changed Claude settings"
    settings = json.loads(codex_file.read_bytes())
    assert len(handlers(settings)) == 4
    before_codex = codex_file.read_bytes()
    run(install_args + [tarballs[1]], root, env)
    assert codex_file.read_bytes() == before_codex, "Repeat install rewrote hook definitions"
    assert claude_file.read_bytes() == before_claude
    project = root / "project"
    (project / "src").mkdir(parents=True)
    (project / "ai_docs/reference").mkdir(parents=True)
    (project / "ai_docs/solutions").mkdir()
    (project / "ai_docs/README.md").write_text("F091_ORIENT_MARKER\n", encoding="utf-8")
    (project / "ai_docs/reference/INDEX.md").write_text("# Guide router\n", encoding="utf-8")
    (project / "ai_docs/reference/GUIDE_sample.md").write_text("# Synthetic guide\n", encoding="utf-8")
    (project / "ai_docs/solutions/ANALYSIS_sample.md").write_text(
        "---\nid: F-901\nlevel: L3\nstatus: IN_PROGRESS\ndomain: code\n---\n"
        "# Synthetic unit\n## Impact\n### Preservation constraints\n"
        "| id | bound to | callers | must stay true | evidence |\n|---|---|---|---|---|\n"
        "| P1 | `src/a.py` | caller | preserve the synthetic invariant | fixture |\n", encoding="utf-8")
    transcript = root / "synthetic.jsonl"
    patch = "*** Begin Patch\n*** Update File: src/a.py\n@@\n-a\n+b\n*** End Patch"
    payload = {"session_id": "synthetic", "hook_event_name": "PreToolUse", "cwd": str(project),
               "tool_name": "apply_patch", "tool_input": {"command": patch}, "transcript_path": str(transcript)}

    def invoke(handler, cwd=project):
        result = subprocess.run(handler["command"], shell=True, cwd=cwd, env=env,
                                input=json.dumps(payload), capture_output=True,
                                text=True, encoding="utf-8", errors="replace")
        assert result.returncode == 0, result.stderr
        return result.stdout

    orient = settings["hooks"]["SessionStart"][0]["hooks"][0]
    assert "F091_ORIENT_MARKER" in invoke(orient)
    assert "F091_ORIENT_MARKER" in invoke(orient, project / "src")
    remind = settings["hooks"]["UserPromptSubmit"][0]["hooks"][0]
    assert invoke(remind).strip()
    verdict, recall = [g["hooks"][0] for g in settings["hooks"]["PreToolUse"]]
    def message(text):
        return {"type": "response_item", "payload": {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": text}]}}
    meta = {"type": "session_meta", "payload": {"cwd": str(project)}}
    transcript.write_text(json.dumps(message("Working.")) + "\n", encoding="utf-8")
    assert json.loads(invoke(verdict))["hookSpecificOutput"]["permissionDecision"] == "deny"
    lines = [meta, message("Level: L3 router: GUIDE_sample.md -> read")]
    for rel in ["ai_docs/reference/GUIDE_sample.md", "ai_docs/solutions/ANALYSIS_sample.md"]:
        lines.append({"type": "response_item", "payload": {"type": "function_call", "name": "exec_command",
                     "arguments": json.dumps({"cmd": f"Get-Content -LiteralPath '{rel}'"})}})
    transcript.write_text("\n".join(map(json.dumps, lines)) + "\n", encoding="utf-8")
    assert not invoke(verdict).strip()
    assert "P1" in json.loads(invoke(recall))["hookSpecificOutput"]["additionalContext"]
    # Opt out one handler; another remains. Foreign handlers survive explicit cleanup.
    settings["hooks"]["UserPromptSubmit"] = []
    settings["hooks"]["SessionStart"].append({"hooks": [{"type": "command", "command": "echo foreign"}]})
    codex_file.write_text(json.dumps(settings), encoding="utf-8")
    run(install_args + [tarballs[1]], root, env)
    assert not json.loads(codex_file.read_bytes())["hooks"]["UserPromptSubmit"]
    assert claude_file.read_bytes() == before_claude
    fresh_env = dict(env)
    fresh_home = root / "Fresh PC User"
    for key in ["HOME", "USERPROFILE", "CODEX_HOME", "CLAUDE_CONFIG_DIR", "GEMINI_HOME",
                "ANTIGRAVITY_HOME", "AGENTIC_SDLC_KB_ROOT"]:
        fresh_env[key] = str(fresh_home / Path(env[key]).relative_to(home))
    Path(fresh_env["CODEX_HOME"]).mkdir(parents=True)
    Path(fresh_env["CLAUDE_CONFIG_DIR"]).mkdir(parents=True)
    fresh_prefix = root / "fresh-prefix"
    run(npm_command + ["install", "--global", "--prefix", fresh_prefix,
                       "--no-audit", "--no-fund", tarballs[1]], root, fresh_env)
    assert len(handlers(json.loads((Path(fresh_env["CODEX_HOME"]) / "hooks.json").read_bytes()))) == 4
    assert len(handlers(json.loads((Path(fresh_env["CLAUDE_CONFIG_DIR"]) / "settings.json").read_bytes()))) == 4
    package = prefix / ("node_modules" if os.name == "nt" else "lib/node_modules") / "@antoneeo/agentic-sdlc-skill"
    # Leave an intact profile for a native Codex /hooks inspection before cleanup.
    if args.keep:
        codex_file.write_bytes(before_codex)
    result = {"status": "PASS", "profile": str(root), "codex_home": env["CODEX_HOME"], "project": str(project),
              "package": str(package), "claude_upgrade_byte_identical": True,
              "tarball_fresh_install": True, "tarball_install_upgrade": True, "installed_handler_checks": ["orient root/nested", "remind", "verdict deny/allow", "recall"],
              "repeat_install_byte_identical": True, "opt_out_preserved": True,
              "native_trust_execution": "not tested by this harness"}
    result["profile_retained"] = args.keep
    result["baseline_ref"] = BASELINE_REF
    if not args.keep:
        run([node, package / "scripts/preuninstall.js"], root, env)
        assert json.loads(codex_file.read_bytes())["hooks"]["SessionStart"] == [{"hooks": [{"type": "command", "command": "echo foreign"}]}]
        shutil.rmtree(root)  # verified owned temp root above
        result["explicit_cleanup_foreign_preserved"] = True
    report = repo / "ai_docs/solutions/harness_codex_hooks" / args.report
    report.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
