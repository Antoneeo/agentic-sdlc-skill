#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Domain entry point with shared project memory.

Ship this file, sdlc_core.py and knowledge.py together. The core alone omits
knowledge integrity and this entry point\'s domain-specific behavior.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import sdlc_core
except ImportError as exc:  # pragma: no cover - exercised by TS12, not by unit tests
    sys.stderr.write(
        "[ERROR] sdlc_check.py cannot find sdlc_core.py next to it: " + str(exc) + "\n"
        "        The validator needs entry point, sdlc_core.py and knowledge.py.\n"
        "        Copy all three together; core alone omits memory and overlay checks.\n")
    sys.exit(1)

# Re-export the core's surface: existing importers (`import sdlc_check as sc`)
# and the test batteries reach for these names on this module.
from sdlc_core import *            # noqa: F401,F403
from sdlc_core import _map_refs    # noqa: F401  underscore helper used by the batteries
import knowledge

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
                   "routing.md", "hybrid.md", "ENFORCEMENT.md", "memory.md"),
    capabilities=(
        # spine
        "triage", "write_triggers", "workstream_registry", "vision_gate",
        "design_review_gate", "guide_router", "worktree_hygiene",
        # code overlay
        "architect_pass", "interaction_contract", "comprehension_guides", "tdd",
        "subagent_dispatch", "legacy_narrative_handoff", "question_discipline",
    ),
    design_gate_between=("### 3. Request Analysis", "### 4. Development and Testing"),
    remind_line=(
        "first decide if this skill governs the work; if yes, LOAD it once -- an "
        "unread protocol cannot be applied. Declare the level (L1/L2/L3/Spike) "
        "and the guide-router verdict before acting; an imperative is a request "
        "to triage. Name the mechanism before fixing the first defect you can "
        "measure -- symptom patches recur and stack. Replay governing text -- "
        "doctrine, a prompt, a schema -- against the case that motivated it: red "
        "under the old text, green under the new."
    ),
)


def main(argv=None):
    return knowledge.main(argv)


if __name__ == "__main__":
    sys.exit(main())
