#!/usr/bin/env python3
"""F-075 probe: replay this repository's session start and measure what reaches
the agent under Claude Code's hook-output limits.

Claude Code caps hook output at HOOK_CAP characters; above it, only the first
PREVIEW characters are injected. The probe runs both orient entry points wired
on the owner's machine for this repo (project: the code lens; user: kb-agentic)
and asserts, per entry point:
  A1  total output <= HOOK_CAP (nothing is saved to a file);
  A2  the guide router's first row lands inside the first PREVIEW characters;
  A3  the workstream registry section lands inside the first PREVIEW characters;
  A4  with sibling lenses installed on this machine, orient and remind name routing.md.
Exit 0 = all green; exit 1 = some assertion red (printed).

    python ai_docs/solutions/harness_session_orientation_reach/probe.py [--root .]
"""
import subprocess, sys
from pathlib import Path

HOOK_CAP, PREVIEW = 10_000, 2_000
ROOT = Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else Path.cwd()
ENTRIES = {
    "code (project hook)": ROOT / "skills/agentic-sdlc-skill/scripts/sdlc_check.py",
    "kb (user hook)": ROOT / "distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_check.py",
}
ROUTER_ROW = "`GUIDE_release.md`"   # first router row in this repo
HANDOFF = "## workstream registry"   # FS2 section heading (lowercased)

red = 0
for name, entry in ENTRIES.items():
    out = subprocess.run([sys.executable, str(entry), "orient", "--root", str(ROOT)],
                         capture_output=True, text=True, encoding="utf-8").stdout
    r, h = out.find(ROUTER_ROW), out.lower().find(HANDOFF)
    checks = [("A1 total <= %d" % HOOK_CAP, len(out) <= HOOK_CAP, len(out)),
              ("A2 router row in preview", 0 <= r < PREVIEW, r),
              ("A3 handoff in preview", 0 <= h < PREVIEW, h)]
    for label, ok, val in checks:
        red += not ok
        print("%-20s %-26s %s (%s)" % (name, label, "GREEN" if ok else "RED", val))
    rem = subprocess.run([sys.executable, str(entry), "remind"],
                         capture_output=True, text=True, encoding="utf-8").stdout
    ok = "routing.md" in out and "routing.md" in rem
    red += not ok
    print("%-20s %-26s %s" % (name, "A4 lens choice named", "GREEN" if ok else "RED"))
sys.exit(1 if red else 0)
