#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KB Agentic — the KNOWLEDGE domain entry point.

Thin by design. Every behaviour lives in `sdlc_core.py`, the spine shipped
verbatim in every distribution of the family; this file only says which domain
this distribution implements, which portable checks it exposes, and what this
overlay carries. Command
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
DOMAIN = "knowledge"

sdlc_core.set_entry_point(DOMAIN, provides=("code", "knowledge"))

# What this distribution carries. The shared battery reads it; the spine
# capabilities are not optional, and a shared test refuses a profile that drops one.
#
# Two overlays are deliberately NOT claimed, and saying so here is the point:
#  - `architect_pass` is the code overlay's "does this component already exist?".
#    The knowledge overlay asks the same question about categories and topics,
#    through `taxonomy.md`, so it claims `taxonomy_pass` instead.
#  - `comprehension_guides` is claimed once the `source_kind: code` wiring exists
#    for this domain; until then the gap is DECLARED, not hidden by a missing test.
sdlc_core.set_profile(
    skill_name="kb-agentic",
    unit_noun="topic",
    support_files=("templates.md", "taxonomy.md", "guides.md", "vision.md",
                   "distillation.md", "reconciliation.md", "elicitation.md",
                   "review.md", "dispatch.md", "routing.md", "ENFORCEMENT.md"),
    capabilities=(
        # spine
        "triage", "write_triggers", "workstream_registry", "vision_gate",
        "design_review_gate", "guide_router", "worktree_hygiene",
        # knowledge overlay
        "taxonomy_pass", "subagent_dispatch",
    ),
    design_gate_between=("### 3. Request Analysis & Taxonomy Pass",
                         "### 4. Knowledge Processing & Distillation"),
)


def main(argv=None):
    return sdlc_core.main(argv)


if __name__ == "__main__":
    sys.exit(main())
