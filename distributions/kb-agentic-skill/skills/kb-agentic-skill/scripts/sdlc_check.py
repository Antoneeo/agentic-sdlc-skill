#!/usr/bin/env python3
"""Knowledge lens entry point. Ship with sdlc_core.py and knowledge.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import sdlc_core
except ImportError as exc:
    sys.stderr.write("[ERROR] missing sdlc_core.py: %s\n"
                     "Copy entry point, sdlc_core.py and knowledge.py together.\n" % exc)
    sys.exit(1)
from sdlc_core import *
from sdlc_core import _map_refs
import knowledge
from knowledge import *
from knowledge import _kb_extra_validate, _kb_original_candidates

DOMAIN = "knowledge"

sdlc_core.set_entry_point(DOMAIN, provides=("code", "knowledge"))

sdlc_core.set_profile(
    skill_name="kb-agentic",
    unit_noun="topic",
    support_files=("templates.md", "taxonomy.md", "guides.md", "vision.md",
                   "distillation.md", "reconciliation.md", "elicitation.md",
                   "review.md", "dispatch.md", "routing.md", "portability.md",
                   "ENFORCEMENT.md", "memory.md"),
    capabilities=(
        # spine
        "triage", "write_triggers", "workstream_registry", "vision_gate",
        "design_review_gate", "guide_router", "worktree_hygiene",
        # knowledge overlay
        # `knowledge_portability` (F-030) is deliberately NOT declared: the
        # capability vocabulary lives in the shared spine, and no shared test
        # guards on portability, so adding a label there would mean editing
        # sdlc_core.py in three distributions to buy nothing.
        "taxonomy_pass", "subagent_dispatch", "question_discipline",
    ),
    # F-046: the per-turn line moved from this file's own `remind` command into
    # the shared spine, which now carries the machine for all three lenses. The
    # kb duties below are unchanged; what is new is the first one -- an unread
    # protocol cannot be applied, and until now nothing said so.
    remind_line=(
        "first decide if this skill governs the work; if yes, LOAD it once -- an "
        "unread protocol cannot be applied. Triage: L1 quick fact, L2 propagation, "
        "L3 new knowledge unit, Spike; declare the level. On this project's "
        "domain, read topics/INDEX.md first and cite claim ids, or state no "
        "coverage. Decisions today get recorded in the KB at close. Revising a "
        "document? Re-read it whole and rewrite to current state -- never append "
        "a delta."
    ),
    design_gate_between=("### 3. Request Analysis & Taxonomy Pass",
                         "### 4. Knowledge Processing & Distillation"),
)


def main(argv=None):
    return knowledge.main(argv)

if __name__ == "__main__":
    sys.exit(main())
