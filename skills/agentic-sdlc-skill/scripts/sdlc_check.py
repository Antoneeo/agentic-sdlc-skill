#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Agentic SDLC — the CODE domain entry point.

Thin by design. Every behaviour lives in `sdlc_core.py`, the spine shipped
verbatim in every distribution of the family; this file only says which domain
this distribution implements and which portable checks it exposes. Command
names, flags, output and exit codes are unchanged — an existing project sees the
same tool it always had.

Both files must sit in the same directory. If you copy the validator into a CI
image, copy BOTH (`ENFORCEMENT.md` §2 has the recipe); copying this one alone
fails at import, loudly and immediately, which is the intended failure.

Usage is `sdlc_core.py`'s: check / validate / index / stale / mark / gate /
orient / plan.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import sdlc_core
except ImportError as exc:  # pragma: no cover - exercised by TS12, not by unit tests
    sys.stderr.write(
        "[ERROR] sdlc_check.py cannot find sdlc_core.py next to it: " + str(exc) + "\n"
        "        The validator ships as TWO files since the multi-domain core.\n"
        "        Copy both, or run sdlc_core.py directly.\n")
    sys.exit(1)

# Re-export the core's surface: existing importers (`import sdlc_check as sc`)
# and the test batteries reach for these names on this module.
from sdlc_core import *            # noqa: F401,F403
from sdlc_core import _map_refs    # noqa: F401  underscore helper used by the batteries

# The domain this distribution implements. It does NOT decide any document's
# owning domain -- that is resolved per project (`default_domain:` in the docs
# root's README) and per artifact (`domain:`), so the same tree gets the same
# verdict from every installed distribution. What it decides is which portable
# checks a document may import here by name; the rest warn as unavailable.
DOMAIN = "code"

sdlc_core.set_entry_point(DOMAIN, provides=("code", "knowledge"))

# What this distribution carries. The shared battery reads it; the spine
# capabilities are not optional, and a shared test refuses a profile that drops one.
sdlc_core.set_profile(
    skill_name="agentic-sdlc",
    unit_noun="feature",
    support_files=("templates.md", "architect.md", "guides.md", "vision.md", "tdd.md",
                   "debugging.md", "elicitation.md", "review.md", "dispatch.md",
                   "routing.md", "ENFORCEMENT.md"),
    capabilities=(
        # spine
        "triage", "write_triggers", "workstream_registry", "vision_gate",
        "design_review_gate", "guide_router", "worktree_hygiene",
        # code overlay
        "architect_pass", "comprehension_guides", "tdd", "subagent_dispatch",
        "legacy_narrative_handoff",
    ),
    design_gate_between=("### 3. Request Analysis", "### 4. Development and Testing"),
)


def main(argv=None):
    return sdlc_core.main(argv)


if __name__ == "__main__":
    sys.exit(main())
