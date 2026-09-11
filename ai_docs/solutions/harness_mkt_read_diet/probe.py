#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-052 assertion harness — the read diet applied per lens.

Same load-bearing pair as F-051 (byte-level conservation, executable weighing),
plus the two things this unit adds: the kb NON-decision is asserted so it cannot
be silently "finished", and the shared conservation check must be DERIVED rather
than carry one lens's headings.

RED baseline (pre-implementation, 2026-09-11):
  P1 FAIL  mkt has no hybrid.md
  P2 FAIL  mkt's SKILL.md carries no pointer
  P3 FAIL  nothing to conserve into yet
  P4 FAIL  mkt's ENFORCEMENT.md still cites a section that never existed there
  P5 FAIL  the shared conservation check still hardcodes the code lens's anchors
  P6 PASS  invariant: kb still carries its Hybrid block inline (measured, not done)
  P7 FAIL  the mandatory read has not shrunk
GREEN target: all seven PASS.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
MKT = REPO / "distributions" / "mkt-agentic-sdlc"
LENS = MKT / "skills" / "mkt-agentic-sdlc"
SKILL = LENS / "SKILL.md"
HYBRID = LENS / "hybrid.md"
KB = REPO / "distributions" / "kb-agentic-skill" / "skills" / "kb-agentic-skill"
BATTERY = REPO / "skills" / "agentic-sdlc-skill" / "scripts" / "test_skill_invariants.py"

# mkt's SKILL.md before the move, read with the SAME ruler `benefit` uses
# (st_size on this checkout, not the LF blob -- F-051's WARN-1).
BYTES_BEFORE = 23120

# sha256 of the block moved out of mkt's SKILL.md.
MOVED_BLOCK_SHA256 = "b9b19d58a104e858f38460065160a61e64a6cd6f64f92c1bbf47fbf534d25ef6"

FAILS = []


def check(name, cond, detail=""):
    print("%s %s%s" % ("PASS" if cond else "FAIL", name,
                       (" — " + detail) if (detail and not cond) else ""))
    if not cond:
        FAILS.append(name)


def main():
    skill = SKILL.read_text(encoding="utf-8")
    hybrid = HYBRID.read_text(encoding="utf-8") if HYBRID.is_file() else ""

    check("P1 mkt has a hybrid.md", HYBRID.is_file(),
          "the moved content has nowhere to live")

    # --- P2: the pointer, in MKT's own vocabulary ---------------------------
    m = re.search(r"### Hybrid in symbiosis with devPNT(?:.|\n)*?(?=\n## )", skill)
    blk = m.group(0) if m else ""
    after = blk.split("hybrid.md", 1)[-1] if "hybrid.md" in blk else ""
    check("P2a mkt's SKILL.md points at hybrid.md", "hybrid.md" in blk,
          "the moved content is unreachable")
    check("P2b the pointer names the mechanical trigger", "devpnt_" in blk,
          "a pointer with no trigger is a filename")
    check("P2c the pointer names what is lost by skipping it",
          re.search(r"second source of truth|ownership", after, re.I) is not None,
          "anchored AFTER the filename so the content inventory cannot satisfy it")

    # --- P3: CONSERVATION, byte level against a recorded digest ------------
    # Anchored on a digest rather than on `git show HEAD:` -- a moving
    # reference stops proving anything once the unit is committed, and
    # subprocess decodes git's UTF-8 through the console codepage on Windows.
    import hashlib
    i = hybrid.find("### Hybrid in symbiosis with devPNT")
    cand = hybrid[i:].split("\n", 1)[1].strip() if i >= 0 else ""
    check("P3a the moved block hashes to the block that left SKILL.md",
          hashlib.sha256(cand.encode("utf-8")).hexdigest() == MOVED_BLOCK_SHA256,
          "hybrid.md's block is not the content that was moved")
    # the ownership matrix rows are the substance; none may remain in SKILL.md
    rows = [l for l in hybrid.splitlines()
            if l.startswith("| ") and "shadow" in l.lower()]
    check("P3b the matrix rows moved with their heading", len(rows) >= 4,
          "found %d shadow rows in hybrid.md" % len(rows))
    check("P3c the moved headings left mkt's SKILL.md",
          "### Ownership matrix" not in skill,
          "the move did not happen; the reader now has two copies")

    # --- P4: the dangling citation this unit found before moving -----------
    enf = (LENS / "ENFORCEMENT.md").read_text(encoding="utf-8")
    check("P4 mkt's ENFORCEMENT.md no longer cites a section that is not there",
          "see the SKILL.md shadow discipline" not in enf,
          "pre-existing: mkt's SKILL.md never had a shadow discipline section")

    # --- P5: the shared check must be DERIVED, not one lens's headings ------
    bat = BATTERY.read_text(encoding="utf-8")
    hard = [a for a in ("### Shadow discipline (Hybrid)", "### Feature state mapping",
                        "### Triage equivalence")
            if a in bat]
    check("P5 the shared conservation check carries no lens's headings", not hard,
          "hardcoded in a SHARED file, so it fails in a lens without them: %s"
          % "; ".join(hard))

    # --- P6: the kb non-decision, asserted so nobody 'finishes the job' -----
    kb_skill = (KB / "SKILL.md").read_text(encoding="utf-8")
    check("P6 kb still carries its Hybrid block inline (measured, not done)",
          "### Hybrid in symbiosis with devPNT" in kb_skill
          and not (KB / "hybrid.md").is_file(),
          "kb's block is 299 B against a 1,282 B pointer cost: extracting it "
          "GROWS the file. That is a measured decision, not unfinished work")

    # --- P7: packaging reality, and the price actually down ----------------
    pkg = json.loads((MKT / "package.json").read_text(encoding="utf-8"))
    check("P7a hybrid.md is in mkt's package allowlist",
          any("hybrid.md" in f for f in pkg.get("files", [])),
          "postinstall copies only what the tarball carries")
    check("P7b mkt's README lists it",
          "hybrid.md" in (MKT / "README.md").read_text(encoding="utf-8"),
          "GUIDE_release.md step 2")
    now = SKILL.stat().st_size
    check("P7c mkt's mandatory read shrank", now < BYTES_BEFORE,
          "SKILL.md is %d bytes, was %d" % (now, BYTES_BEFORE))
    if now < BYTES_BEFORE:
        print("     (mkt mandatory read: %d -> %d bytes, -%.1f%%)"
              % (BYTES_BEFORE, now, 100.0 * (BYTES_BEFORE - now) / BYTES_BEFORE))

    print("\n%d probe(s) failing" % len(FAILS) if FAILS else "\nall probes green")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
