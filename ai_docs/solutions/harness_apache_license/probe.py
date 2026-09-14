#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Executed claims behind ANALYSIS_apache_license.md.

    python ai_docs/solutions/harness_apache_license/probe.py

P1  npm packs a package-root LICENSE by itself, but a NOTICE, or any file inside
    the skill folder, only when package.json `files` lists it.
P2  each of the four packages' postinstall copies the whole skill folder, so a
    LICENSE/NOTICE placed there reaches every installed skill.
P3  every LICENSE in both repositories is the canonical Apache-2.0 text.

Each probe shows its RED state (the condition negated) beside its GREEN state: a
probe that cannot go red establishes nothing. Everything runs in temp dirs, with
no network and no real HOME. The distill repository is found as a sibling
checkout named `distill-skill`; without it its rows are reported as skipped.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
# SHA-256 of https://www.apache.org/licenses/LICENSE-2.0.txt, LF line endings.
CANONICAL_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
DISTILL = next((p / "distill-skill" for p in REPO.parents
                if (p / "distill-skill" / "package.json").is_file()), None)
# (package root, skill folder name)
PACKAGES = [
    (REPO, "agentic-sdlc-skill"),
    (REPO / "distributions" / "kb-agentic-skill", "kb-agentic-skill"),
    (REPO / "distributions" / "mkt-agentic-sdlc", "mkt-agentic-sdlc"),
] + ([(DISTILL, "distill")] if DISTILL else [])
COPY_IGNORE = shutil.ignore_patterns(".git", ".claude", ".devpnt", "node_modules", "__pycache__",
                                     "ai_docs", "evals", "fixtures", "distributions")
failures = []


def check(label, cond):
    print(f"  {'ok  ' if cond else 'FAIL'} {label}")
    if not cond:
        failures.append(label)


def lf_sha256(data):
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def packed(pkg):
    out = subprocess.run("npm pack --dry-run --json", cwd=pkg, shell=True,
                         capture_output=True, text=True, check=True).stdout
    return {f["path"] for f in json.loads(out)[0]["files"]}


def p1():
    print("P1  npm pack: what the tarball carries")
    skill = "skills/mkt-agentic-sdlc"
    names = ("LICENSE", "NOTICE", f"{skill}/LICENSE", f"{skill}/NOTICE")
    with tempfile.TemporaryDirectory() as t:
        pkg = Path(t) / "pkg"
        shutil.copytree(REPO / "distributions" / "mkt-agentic-sdlc", pkg, ignore=COPY_IGNORE)
        manifest = json.loads((pkg / "package.json").read_text(encoding="utf-8"))
        manifest["files"] = [f for f in manifest["files"] if f not in names]
        (pkg / "package.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        for rel in names:
            (pkg / rel).write_text("probe\n", encoding="utf-8")
        files = packed(pkg)
        print("  RED - nothing listed in `files`:")
        check("root LICENSE is packed anyway", "LICENSE" in files)
        for rel in names[1:]:
            check(f"{rel} is NOT packed", rel not in files)
        manifest["files"] += list(names[1:])
        (pkg / "package.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        files = packed(pkg)
        print("  GREEN - listed in `files`:")
        for rel in names:
            check(f"{rel} is packed", rel in files)


def install(pkg_root, skill, with_files):
    with tempfile.TemporaryDirectory() as t:
        pkg, home = Path(t) / "pkg", Path(t) / "home"
        shutil.copytree(pkg_root, pkg, ignore=COPY_IGNORE)
        folder = pkg / "skills" / skill
        for name in ("LICENSE", "NOTICE"):
            target = folder / name
            if with_files and not target.is_file():
                target.write_text("probe\n", encoding="utf-8")
            if not with_files and target.is_file():
                target.unlink()
        (home / ".claude").mkdir(parents=True)
        env = {**os.environ, "HOME": str(home), "USERPROFILE": str(home),
               "CLAUDE_CONFIG_DIR": str(home / ".claude")}
        for key in ("GEMINI_HOME", "CODEX_HOME", "ANTIGRAVITY_HOME"):
            env.pop(key, None)
        subprocess.run(["node", "scripts/postinstall.js"], cwd=pkg, env=env,
                       capture_output=True, text=True, check=True)
        installed = [p.parent for p in home.glob("**/skills/*/SKILL.md")]
        state = "GREEN - in the source folder" if with_files else "RED - not in the source folder"
        print(f"  {pkg_root.name} / {state}:")
        check(f"postinstall produced installed skills ({len(installed)})", bool(installed))
        for d in installed:
            both = all((d / name).is_file() for name in ("LICENSE", "NOTICE"))
            none = not any((d / name).is_file() for name in ("LICENSE", "NOTICE"))
            check(f"{d.relative_to(home).as_posix()}: LICENSE and NOTICE "
                  f"{'present' if with_files else 'absent'}", both if with_files else none)


def p2():
    print("P2  postinstall: what an installed skill carries, per package")
    if not DISTILL:
        print("  SKIP distill-skill: no sibling checkout found")
    for pkg_root, skill in PACKAGES:
        for with_files in (False, True):
            install(pkg_root, skill, with_files)


def p3():
    print("P3  LICENSE text: the canonical Apache-2.0, in both repositories")
    if not DISTILL:
        print("  SKIP distill-skill: no sibling checkout found")
    found = []
    for repo in (REPO, DISTILL):
        if repo is None:
            continue
        found += sorted(p for p in repo.glob("**/LICENSE")
                        if not {".git", ".claude", "node_modules"} & set(p.relative_to(repo).parts))
    sample = found[0].read_bytes() if found else b""
    check("RED - a one-byte change breaks the match", lf_sha256(b"x" + sample) != CANONICAL_SHA256)
    check(f"the repositories ship a LICENSE ({len(found)} found)", bool(found))
    for p in found:
        check(f"{p.as_posix()} is canonical", lf_sha256(p.read_bytes()) == CANONICAL_SHA256)


if __name__ == "__main__":
    for probe in (p1, p2, p3):
        try:
            probe()
        except subprocess.CalledProcessError as err:
            failures.append(f"{probe.__name__} crashed")
            print(f"  ERROR {probe.__name__}: {(err.stderr or '')[-400:]}")
    print("\nall claims hold" if not failures else f"\n{len(failures)} claim(s) do not hold: {failures}")
    sys.exit(1 if failures else 0)
