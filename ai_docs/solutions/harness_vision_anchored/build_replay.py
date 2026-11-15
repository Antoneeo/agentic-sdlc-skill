"""F-099 replay: builds the cold-reader prompt for the recorded case under the old
doctrine (git HEAD) and under the new one (working tree). Same case material, same
task; only the method excerpt differs. Usage: python build_replay.py [base-ref] [case-dir]. The case is not in the repository (R8)."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
CASE = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "case_m161"  # held outside the repository (R8)


def old(rel):
    return subprocess.run(["git", "show", f"{BASE}:{rel}"], cwd=ROOT, capture_output=True,
                          text=True, encoding="utf-8", check=True).stdout.replace("\r\n", "\n")


def new(rel):
    return (ROOT / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


def between(text, start, end):
    i = text.index(start)
    j = text.index(end, i + len(start)) if end else len(text)
    return text[i:j].rstrip() + "\n"


def method(read):
    review = read("skills/agentic-sdlc-skill/review.md")
    vision = read("skills/agentic-sdlc-skill/vision.md")
    parts = [between(vision, "## What a Vision IS", "\nFour consequences"),
             between(review, "- **Conformance statement", "\n- **An unasked doubt"),
             between(review, "**Rounds are capped at 3.**", " **Log one row"),
             ]
    if "**Re-anchor at the second FAIL" in review:
        parts.append(between(review, "**Re-anchor at the second FAIL", "\n\n"))
    if "## 8. Downstream" in vision:
        parts.append(between(vision, "## 8. Downstream", None))
    return "\n".join(parts)


def case():
    vc = (CASE / "vision_clause.md").read_text(encoding="utf-8")
    rq = (CASE / "requirement.md").read_text(encoding="utf-8")
    rv = (CASE / "reviews.md").read_text(encoding="utf-8")
    return "\n".join([
        between(vc, "# M-VISION v1.5 (extract)", None),
        between(rq, "## A. Interface contract, version 1.6", "## B. Interface contract"),
        between(rq, "## C. Threat model", "## E. What could not"),
        between(rv, "## Round 1 - FAIL", "## Round 3 - FAIL"),
    ])


TASK = """You are the author session of the impact analysis for plan node A10 of a
software project. Your design documents derive from the milestone vision, the
interface contract, the threat model and the plan node quoted below. Review round 2
of your impact analysis has just returned FAIL; both rounds are summarised below.
The method you work under is the excerpt at the end: follow it.

Write, in English, at most 400 words:
1. Your diagnosis of why two rounds failed.
2. Your next step, concretely.
3. Any question you bring to the owner, with its options and your recommendation.
Use only the material given; do not invent facts.
"""

for name, read in (("old", old), ("new", new)):
    text = (TASK + "\n# CASE MATERIAL\n\n" + case() + "\n# THE METHOD YOU WORK UNDER\n\n"
            + method(read))
    (HERE / "replay" / f"prompt_{name}.md").write_text(text, encoding="utf-8")
    print(name, len(text))
