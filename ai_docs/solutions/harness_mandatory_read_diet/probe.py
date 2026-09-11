#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-051 assertion harness — the mandatory-read diet.

A pruning unit has exactly one catastrophic failure mode: a quiet deletion
wearing the costume of a move. So the load-bearing probe is P3, a CONSERVATION
check — every anchor that leaves SKILL.md must be findable in hybrid.md — and
its twin P4, which pins the blocks that must NOT have moved. Byte savings are
easy to fake by deleting doctrine; these two are what make that impossible.

RED baseline (pre-implementation, 2026-09-11):
  P1 FAIL  hybrid.md does not exist
  P2 FAIL  SKILL.md carries no pointer naming the trigger
  P3 FAIL  nothing to conserve into yet
  P4 PASS  invariant: the not-cut blocks are all still in SKILL.md
  P5 FAIL  hybrid.md is not in the package allowlist or the README
  P6 FAIL  the mandatory read has not shrunk
GREEN target: all six PASS.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CODE = REPO / "skills" / "agentic-sdlc-skill"
SKILL = CODE / "SKILL.md"
HYBRID = CODE / "hybrid.md"

# Measured before the move with the SAME ruler `benefit` uses -- st_size on this
# checkout, not the git blob. The first cut pinned the LF blob size (49645) and
# printed a percentage `benefit` would never show; before and after must be read
# with one ruler or the saving is an artifact of line endings.
BYTES_BEFORE = 50001

# Anchors that MUST end up in hybrid.md and leave SKILL.md's body.
MOVED = (
    "### Ownership matrix",
    "### Triage equivalence (one threshold, two vocabularies)",
    "### Feature state mapping",
    "### Shadow discipline (Hybrid)",
    "### Validator in Hybrid",
    "| Artifact | Standalone master | Hybrid master | Mirror rule |",
    "| Skill triage | devPNT equivalent | Governed artifacts |",
    "| ANALYSIS frontmatter | devPNT plan node |",
    # NB: "### Hybrid in symbiosis with devPNT" is NOT here. It is the name of
    # a MODE, and `## Operating Modes` must still declare both modes -- removing
    # the heading would remove the mode from the contract. It legitimately
    # appears in both files; what had to leave is its CONTENT, below.
    "Authoritative hierarchy:",
    "Hybrid rules:",
)

# Anchors that MUST STAY in SKILL.md. This is the weighing made executable:
# each one is a block the ANALYSIS argued earns its bytes, and a future diet
# that removes one has to delete a line of this list to go green.
KEPT = (
    "## Rule Zero: Triage",
    "Triage rationalizations",
    "## Write Triggers",
    "Execute-Before-Specify",
    "Blast-radius enumeration is an authoring duty",
    "Design review gate",
    "Claim-to-evidence",
    "Functional Spec before the Interface Contract",
    "Interface Contract before the Impact",
    "Architect before you list files",
    "Use cases are grounded before anything builds on them",
)

FAILS = []


def check(name, cond, detail=""):
    print("%s %s%s" % ("PASS" if cond else "FAIL", name,
                       (" — " + detail) if (detail and not cond) else ""))
    if not cond:
        FAILS.append(name)


def main():
    skill = SKILL.read_text(encoding="utf-8")

    check("P1 hybrid.md exists", HYBRID.is_file(),
          "the moved content has nowhere to live")
    hybrid = HYBRID.read_text(encoding="utf-8") if HYBRID.is_file() else ""

    # --- P2: the pointer, with its TRIGGER and its CONSEQUENCE --------------
    # A filename alone is not a pointer: the reader must know when to follow it
    # and what they lose by not following it.
    # The window is the whole mode subsection, not the line carrying the
    # filename: the trigger sentence PRECEDES that line, and a probe that
    # cannot see it reports "a pointer with no trigger" when there is one.
    m = re.search(r"### Hybrid in symbiosis with devPNT(?:.|\n)*?(?=\n## )", skill)
    blk = m.group(0) if m else ""
    check("P2a SKILL.md points at hybrid.md", "hybrid.md" in skill,
          "the moved content is unreachable")
    check("P2b the pointer names the mechanical trigger",
          "devpnt_" in blk, "a pointer with no trigger is a filename")
    # The first cut matched `ownership` -- a word the pointer's own CONTENT
    # INVENTORY already contains, so deleting the entire consequence paragraph
    # left it green (mutation-proved by the design review). Anchor on the
    # consequence itself, and on the part of the block that FOLLOWS the
    # filename, so the inventory cannot satisfy it.
    after = blk.split("hybrid.md", 1)[-1]
    check("P2c the pointer names what is lost by skipping it",
          re.search(r"second source of truth", after, re.I) is not None
          and re.search(r"auto-accept", after, re.I) is not None,
          "the reader must be able to price skipping it, including the "
          "human-approval rule that now lives only in the moved file")

    # --- P3: CONSERVATION -- the move must not be a deletion ---------------
    lost = [a for a in MOVED if a not in hybrid]
    check("P3a every moved anchor is present in hybrid.md", not lost,
          "NOT MOVED, deleted: %s" % "; ".join(lost[:4]))
    still = [a for a in MOVED if a in skill]
    check("P3b the moved anchors left SKILL.md's body", not still,
          "still in SKILL.md, so the move did not happen: %s"
          % "; ".join(still[:4]))

    # --- P4: the weighing, executable --------------------------------------
    gone = [a for a in KEPT if a not in skill]
    check("P4 every block the weighing kept is still in SKILL.md", not gone,
          "REMOVED, and the ANALYSIS argued each of these earns its bytes: %s"
          % "; ".join(gone))

    # --- P5: a pointer to a file the tarball omits is worse than the text ---
    pkg = json.loads((REPO / "package.json").read_text(encoding="utf-8"))
    files = pkg.get("files", [])
    covered = any(f == "hybrid.md" or f.rstrip("/") in ("skills", ".")
                  or "hybrid" in f or f.endswith("*") for f in files)
    check("P5a hybrid.md is reachable through the package allowlist", covered,
          "postinstall copies only what the tarball carries: files=%r" % files)
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    check("P5b the README lists hybrid.md among the support files",
          "hybrid.md" in readme, "GUIDE_release.md step 2")

    # --- P3c: conservation at BYTE level, not heading level -----------------
    # Headings can all be present while every row under them is gone. The
    # strong form is that the pre-move region survives as one contiguous,
    # character-identical substring.
    import subprocess
    head = subprocess.run(["git", "show", "HEAD:skills/agentic-sdlc-skill/SKILL.md"],
                          capture_output=True, text=True, cwd=str(REPO)).stdout
    ok = False
    if "### Hybrid in symbiosis with devPNT" in head and "## L3 Workflow" in head:
        block = head[head.index("### Hybrid in symbiosis with devPNT"):
                     head.index("## L3 Workflow")]
        body = block.split("\n", 1)[1].strip()      # drop the mode heading
        ok = body and body in hybrid
    check("P3c the moved region survives as one contiguous, identical block",
          bool(ok),
          "headings may be present while their content is not -- this is the "
          "check that a move is not a deletion wearing its costume")

    # --- P6: the price actually went down ----------------------------------
    now = SKILL.stat().st_size
    check("P6 the mandatory read shrank", now < BYTES_BEFORE,
          "SKILL.md is %d bytes, was %d" % (now, BYTES_BEFORE))
    if now < BYTES_BEFORE:
        print("     (mandatory read: %d -> %d bytes, -%.1f%%)"
              % (BYTES_BEFORE, now, 100.0 * (BYTES_BEFORE - now) / BYTES_BEFORE))

    print("\n%d probe(s) failing" % len(FAILS) if FAILS else "\nall probes green")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
