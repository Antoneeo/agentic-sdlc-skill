#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The drift guard — the family's spine is authored once and copied verbatim.

Three distributions ship the same spine. Nothing but this guard stops the fourth
divergence: the first three happened silently, and were found by a user.

How it works, and why this shape:
  * SHARED_FILES is an explicit per-file MANIFEST, never "everything" and never a
    directory glob. A file leaving the shared set is then a reviewable change to
    this list, not an absence nobody notices.
  * `python shared_files.py --update` records each shared file's SHA-256 into
    `shared_manifest.json`. The recorded content is IDENTICAL in every
    distribution — that is the whole trick: edit a shared file in one repo and its
    manifest changes, so the three manifests no longer match and the divergence is
    visible as a diff instead of as a bug report.
  * `test_drift.py` fails when a shared file's hash does not match the manifest.
    So a local edit is caught immediately, in the repo where it happened, and the
    only way to make it green is to regenerate — which is exactly the moment to
    copy the file to its siblings.

Hashing is LF-normalized: the corpus is checked out on Windows and POSIX, and a
line-ending difference is not divergence.
"""

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
MANIFEST = HERE / "shared_manifest.json"

# Paths are relative to the SKILL directory. Every entry is a file that MUST be
# byte-identical (modulo line endings) in every distribution of the family.
SHARED_FILES = (
    # the spine itself
    "scripts/sdlc_core.py",
    "scripts/entry_point.py",
    "scripts/shared_files.py",
    # the shared batteries: a test that differs between distributions is a test
    # that stopped being shared
    "scripts/test_skill_invariants.py",
    "scripts/test_domain_rules.py",
    "scripts/test_docs_root.py",
    "scripts/test_session_start.py",
    "scripts/test_plan.py",
    "scripts/test_drift.py",
    "scripts/test_migrate.py",
    # domain-neutral doctrine
    "review.md",
    "routing.md",
    "vision.md",
    "guides.md",
    "dispatch.md",
)

# Deliberately NOT shared, and named here so the absence reads as a decision:
#   SKILL.md, templates.md, ENFORCEMENT.md  -- each domain's own wording
#   the entry point (sdlc_check.py / mkt_check.py) -- that IS the domain
#   the overlay files (architect/tdd/debugging | taxonomy/distillation |
#     frameworks/research) -- the overlays are supposed to differ
#   the golden corpus, its baseline AND its harness -- the harness is bound to the
#     corpus and to the subcommands THIS distribution ships (marketing has ledger,
#     budget, funnel, trace and no orient), and its whole job is to freeze what this
#     distribution does. Uniformity there would defeat the purpose
NOT_SHARED_ON_PURPOSE = (
    "SKILL.md", "templates.md", "ENFORCEMENT.md",
    "scripts/sdlc_check.py", "scripts/mkt_check.py",
    "scripts/test_golden_regression.py",
)



# --- the strong check, available once the distributions live in one repository ---
# Comparing each copy to a recorded hash catches a local edit. Comparing the copies
# to EACH OTHER catches the case the manifest cannot: a change applied and recorded
# in one distribution and simply never carried to the others. The first is a
# tripwire; this is the actual invariant.
DISTRIBUTION_SKILL_DIRS = (
    "skills/agentic-sdlc-skill",
    "distributions/kb-agentic-skill/skills/kb-agentic-skill",
    "distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc",
)


def repo_root():
    """The repository root, if this checkout is the consolidated one."""
    for parent in SKILL_DIR.parents:
        if all((parent / d).is_dir() for d in DISTRIBUTION_SKILL_DIRS):
            return parent
    return None


def cross_distribution_report():
    """{shared file -> {distribution -> hash}} for every file that is NOT identical.

    Returns ({}, None) when this is not the consolidated checkout: the guard then
    falls back to the manifest, and says so rather than passing silently.
    """
    root = repo_root()
    if root is None:
        return {}, None
    diverged = {}
    for rel in SHARED_FILES:
        seen = {}
        for dist in DISTRIBUTION_SKILL_DIRS:
            p = root / dist / rel
            seen[dist] = digest(p) if p.is_file() else None
        if len(set(seen.values())) > 1:
            diverged[rel] = seen
    return diverged, root


def digest(path):
    """SHA-256 of the LF-normalized bytes: a CRLF checkout is not divergence."""
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def current():
    out = {}
    for rel in SHARED_FILES:
        p = SKILL_DIR / rel
        out[rel] = digest(p) if p.is_file() else None
    return out


def recorded():
    if not MANIFEST.is_file():
        return None
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]


def update():
    MANIFEST.write_text(
        json.dumps({
            "_comment": "Generated by shared_files.py --update. IDENTICAL in every "
                        "distribution of the family: if two copies of this file differ, "
                        "the spine has diverged. Never edit by hand.",
            "files": current(),
        }, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n")
    return MANIFEST


def report():
    """(missing, changed) against the recorded manifest."""
    rec = recorded()
    if rec is None:
        return SHARED_FILES, ()
    cur = current()
    missing = tuple(rel for rel, h in cur.items() if h is None)
    changed = tuple(rel for rel, h in cur.items()
                    if h is not None and rec.get(rel) != h)
    return missing, changed


def _cli():
    if "--update" in sys.argv:
        print(f"[ok] shared manifest written: {update()}")
        print("     Now copy every changed shared file to the sibling distributions "
              "and regenerate there too, or their guard will fail.")
        return 0
    diverged, root = cross_distribution_report()
    if root is None:
        print("[note] not the consolidated checkout: comparing against the recorded "
              "manifest only. The cross-distribution check needs all three side by side.")
    else:
        for rel, seen in diverged.items():
            print(f"[ERROR] shared file differs BETWEEN distributions: {rel}")
            for dist, h in seen.items():
                print(f"          {dist}: {h or 'MISSING'}")
        if diverged:
            print("\nThe spine is one file. Reconcile the copies, then run --update.")
            return 1

    miss, chg = report()
    for rel in miss:
        print(f"[ERROR] shared file missing: {rel}")
    for rel in chg:
        print(f"[ERROR] shared file diverged from the manifest: {rel}")
    if miss or chg:
        print("\nThe spine is authored once and copied verbatim. Either restore the file,\n"
              "or -- if the change is intended -- apply it to EVERY distribution and run\n"
              "`python shared_files.py --update` in each.")
        return 1
    scope = ("are identical across all three distributions" if root
             else "match the manifest")
    print(f"[ok] {len(SHARED_FILES)} shared files {scope}")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
