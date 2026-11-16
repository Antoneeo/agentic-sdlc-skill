"""F-100 replay: an orchestrator dispatching guide-heavy tasks, and an owner choosing child
sessions; old doctrine (dispatch.md + team.md at the base ref) against the working tree.
Usage: python build_replay.py [base-ref]"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = sys.argv[1] if len(sys.argv) > 1 else "c67e5792"
FILES = ("skills/agentic-sdlc-skill/dispatch.md", "skills/agentic-sdlc-skill/team.md")


def old(rel):
    return subprocess.run(["git", "show", f"{BASE}:{rel}"], cwd=ROOT, capture_output=True,
                          text=True, encoding="utf-8", check=True).stdout.replace("\r\n", "\n")


def new(rel):
    return (ROOT / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


CASE = """## Part A - dispatch state

Project: a web shop. The L3 design is approved and its plan validated. The plan's tasks
name these guides, to be read whole by whoever does the task:
- GUIDE_forms.md - 880 lines
- GUIDE_design_tokens.md - 640 lines
- GUIDE_accessibility.md - 910 lines

Your client can start a subagent at three tiers (economy, light, deep) and can send a
further message to a subagent it started earlier, by its id.

- T0 "cart summary" (guides: forms, accessibility) - dispatched to subagent s0, economy tier.
  s0 said it had read about half of GUIDE_accessibility.md before writing the code. Sent the
  rest to read and the step to redo, it stopped partway through the guide again, saying its
  context was full. T0 is still open.
- T1 "address form" (guides: forms, design_tokens) - dispatched to subagent s1, economy tier.
  s1's report: "Done. Read GUIDE_forms.md and GUIDE_design_tokens.md. verify: 14 passed,
  0 failed."
- T2 "price badge" (guide: design_tokens) - dispatched to subagent s2, economy tier. s2's
  report: "Done. Read GUIDE_design_tokens.md. verify: 6 passed." The per-task
  review came back FAIL with two findings: the badge uses a raw colour instead of a token,
  and the hover state ignores the spacing scale.
- T3 "accessible checkout form" (guides: forms, design_tokens, accessibility) - pending.

## Part B - the team

The project's reading guide has no `## Team` section. You are opening the project's first
L3 unit. The owner has said they may want to run the work as several sessions, which they
can open themselves.
"""

TASK = """You are the orchestrating agent of the project below, working under the method
excerpt at the end.

Write, in English, at most 400 words:
1. What you do next with T0 and with T1's result, and why.
2. What you do next with T2's review findings: who fixes them.
3. How you dispatch T3: tier, how many briefs, which guides each names, and what each brief
   asks the subagent.
4. The question set on the team you put to the owner now (Part B), as you would write it.
Use only the material given.
"""

for name, read in (("old", old), ("new", new)):
    method = "\n\n".join(f"## FILE {rel.split('/')[-1]}\n\n" + read(rel) for rel in FILES)
    text = TASK + "\n# PROJECT MATERIAL\n\n" + CASE + "\n# THE METHOD YOU WORK UNDER\n\n" + method
    (HERE / f"prompt_{name}.md").write_text(text, encoding="utf-8")
    print(name, len(text))
