"""F-071 probe: how `sdlc_check.py benefit` counts a NOT DUE row today.

Builds a temp project whose REVIEW_LOG holds one closure PASS and one NOT DUE row,
then runs `benefit`. Before F-071 the NOT DUE row was counted as a closure review
and as "inconclusive" (the reason for FS5; this probe exited 1 on that code, 2026-10-18).
After FS5 it is counted apart. Exit 0 when it is counted apart.
"""
import subprocess, sys, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CHECK = REPO / "skills/agentic-sdlc-skill/scripts/sdlc_check.py"
LOG = """# Independent Review Log

| date | doc_key | tier | model | reviewer | findings_raised | findings_real | verdict | revise_rounds |
|---|---|---|---|---|---|---|---|---|
| 2026-10-18 | ANALYSIS_x.md | closure | deep | subagent | 2 | 2 | PASS | 2 |
| 2026-10-18 | ANALYSIS_x.md release delta | closure | none (not due) | not run | 0 | 0 | NOT DUE: bump, CHANGELOG; batteries green | 0 |
"""
with tempfile.TemporaryDirectory() as d:
    log = Path(d) / "ai_docs/audit/reviews/REVIEW_LOG.md"
    log.parent.mkdir(parents=True)
    log.write_text(LOG, encoding="utf-8")
    out = subprocess.run([sys.executable, str(CHECK), "benefit", "--root", d],
                         capture_output=True, text=True, encoding="utf-8").stdout
print(out)
counted = "reviews with a stated moment: 2" in out
inconclusive = "(+1 inconclusive)" in out
print("NOT DUE counted as a review:", counted, "| as inconclusive:", inconclusive)
apart = "reviews ruled not due (logged, counted in no figure below): 1" in out
print("NOT DUE counted apart:", apart)
sys.exit(0 if apart and not counted and not inconclusive else 1)
