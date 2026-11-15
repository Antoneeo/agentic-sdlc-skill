"""F-097 probe, question 2: does `validate` name an ANALYSIS that declares itself
open while no workstream source carries it?

Measurements, all through the real CLI:

1. a throwaway docs tree with a generated registry (one HANDOFF source) and
   five analyses: IN_PROGRESS and carried, IN_PROGRESS and not carried, PLANNED
   and not carried, COMPLETED and not carried, IN_PROGRESS of the course domain
   and not carried;
2. the same tree after its only workstream closed (source deleted, `index`
   run): the registry is generated and empty, and two analyses still say
   IN_PROGRESS -- the state where the registry reads "none";
3. two trees that never generated a registry (an analysis IN_PROGRESS; one with
   no handoff at all, one with a hand-written audit/handoff.md): not converted,
   nothing may be named;
4. optionally, a real project root (this repository): which of its open
   analyses no source carries, and whether `validate` names them.

"Carried" is measured here independently of the validator: the unit id of the
ANALYSIS appears in a source's `workstream:`, or the ANALYSIS file name appears
in a source's frontmatter.

Exit 0 = every IN_PROGRESS analysis nobody carries is named exactly once in
trees 1 and 2 (and, with a project root, there too), the carried, the PLANNED,
the COMPLETED and the course-domain ones never are, and the trees of 3 name
nothing; exit 1 otherwise.

Usage: python probe_uncarried_analysis.py <path to sdlc_check.py> [<project root>]
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

NL = chr(10)
MARK = "no workstream file"      # the words the advisory must carry


def analysis(uid, status):
    return NL.join(["---", f"id: {uid}", f"feature: Fixture {uid}", f"status: {status}",
                    "level: L3", "start_date: 2026-11-01", "end_date:", "---",
                    f"# Feature Analysis: fixture {uid}", ""])


def handoff(uid, name):
    return NL.join(["---", f"workstream: {uid} fixture", "level: L3", "branch: main",
                    "status: IN_PROGRESS", "since: 2026-11-01", "next: next step",
                    f"details: {name}", "updated: 2026-11-01", "---", "# HANDOFF", ""])


def run(checker, cmd, root):
    res = subprocess.run([sys.executable, str(checker), cmd, "--root", str(root)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (res.stdout + res.stderr).splitlines()


def named_once(lines, name):
    return sum(name in line and MARK in line for line in lines) == 1


def named_at_all(lines, name):
    return any(name in line and MARK in line for line in lines)


def fixture(checker):
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / "ai_docs"
        (docs / "audit").mkdir(parents=True)
        (docs / "solutions").mkdir()
        cases = {"ANALYSIS_course_x.md": ("C-001", "IN_PROGRESS"),
                 "ANALYSIS_carried.md": ("F-001", "IN_PROGRESS"),
                 "ANALYSIS_uncarried.md": ("F-002", "IN_PROGRESS"),
                 "ANALYSIS_planned.md": ("F-003", "PLANNED"),
                 "ANALYSIS_closed.md": ("F-004", "COMPLETED")}
        for name, (uid, status) in cases.items():
            body = analysis(uid, status)
            if uid.startswith("C-"):
                body = body.replace("level: L3", "domain: course" + NL + "level: L3")
            (docs / "solutions" / name).write_text(body, encoding="utf-8")
        (docs / "audit" / "HANDOFF_carried.md").write_text(
            handoff("F-001", "ANALYSIS_carried.md"), encoding="utf-8")
        run(checker, "index", tmp)
        lines = run(checker, "validate", tmp)
        (docs / "audit" / "HANDOFF_carried.md").unlink()
        run(checker, "index", tmp)
        emptied = run(checker, "validate", tmp)
    with tempfile.TemporaryDirectory() as tmp:
        sol = Path(tmp) / "ai_docs" / "solutions"
        sol.mkdir(parents=True)
        (sol / "ANALYSIS_uncarried.md").write_text(analysis("F-002", "IN_PROGRESS"),
                                                   encoding="utf-8")
        run(checker, "index", tmp)
        never = run(checker, "validate", tmp)
        aud = Path(tmp) / "ai_docs" / "audit"
        aud.mkdir()
        (aud / "handoff.md").write_text(
            "# Handoff" + NL + "Date: 2026-11-01" + NL + NL + "- F-002 by hand" + NL,
            encoding="utf-8")
        by_hand = run(checker, "validate", tmp)
    ok = (named_once(lines, "ANALYSIS_uncarried.md")
          and not named_at_all(lines, "ANALYSIS_carried.md")
          and not named_at_all(lines, "ANALYSIS_closed.md")
          and not named_at_all(lines, "ANALYSIS_planned.md")
          and named_once(emptied, "ANALYSIS_uncarried.md")
          and named_once(emptied, "ANALYSIS_carried.md")
          and not named_at_all(emptied, "ANALYSIS_planned.md")
          and not named_at_all(emptied, "ANALYSIS_closed.md")
          and not named_at_all(lines, "ANALYSIS_course_x.md")
          and not named_at_all(emptied, "ANALYSIS_course_x.md")
          and not named_at_all(never, "ANALYSIS_uncarried.md")
          and not named_at_all(by_hand, "ANALYSIS_uncarried.md"))
    print("fixture: IN_PROGRESS, no source -> named once: "
          f"{named_once(lines, 'ANALYSIS_uncarried.md')}")
    print("fixture: IN_PROGRESS, carried   -> named: "
          f"{named_at_all(lines, 'ANALYSIS_carried.md')}")
    print("fixture: COMPLETED              -> named: "
          f"{named_at_all(lines, 'ANALYSIS_closed.md')}")
    print("fixture: PLANNED, no source     -> named: "
          f"{named_at_all(lines, 'ANALYSIS_planned.md')}")
    print("emptied registry: both IN_PROGRESS analyses named once: "
          f"{named_once(emptied, 'ANALYSIS_uncarried.md') and named_once(emptied, 'ANALYSIS_carried.md')}")
    print("never generated: IN_PROGRESS    -> named: "
          f"{named_at_all(never, 'ANALYSIS_uncarried.md')}")
    print("hand-written handoff: IN_PROGRESS -> named: "
          f"{named_at_all(by_hand, 'ANALYSIS_uncarried.md')}")
    print("course domain, IN_PROGRESS, no source -> named: "
          f"{named_at_all(lines, 'ANALYSIS_course_x.md') or named_at_all(emptied, 'ANALYSIS_course_x.md')}")
    return ok


def frontmatter(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---", text, re.S)
    return m.group(1) if m else ""


def field(block, key):
    m = re.search(rf"^{key}:[ \t]*(.*)$", block, re.M)
    return m.group(1).strip().strip("'\"") if m else ""


def project(checker, root):
    root = Path(root)
    sources = []
    for p in sorted((root / "ai_docs" / "audit").glob("HANDOFF_*.md")):
        block = frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        if field(block, "workstream"):
            sources.append(block)
    uncarried, open_count = [], 0
    for p in sorted((root / "ai_docs" / "solutions").glob("ANALYSIS_*.md")):
        block = frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        status = field(block, "status")
        if status not in ("IN_PROGRESS", "PLANNED"):
            continue
        open_count += 1
        uid = field(block, "id")
        carried = any(p.name in s or (uid and re.search(
            rf"^workstream:.*\b{re.escape(uid)}\b", s, re.M)) for s in sources)
        if not carried:
            uncarried.append((p.name, status))
    lines = run(checker, "validate", root)
    print(f"project: workstream sources {len(sources)}; analyses declaring "
          f"IN_PROGRESS or PLANNED {open_count}")
    ok = True
    for name, status in uncarried:
        once = named_once(lines, name)
        print(f"project: {name} ({status}) carried by no source -> named once: {once}")
        if status == "IN_PROGRESS" and not once:
            ok = False
    if not uncarried:
        print("project: every open analysis is carried by a source")
    return ok


def main():
    checker = Path(sys.argv[1]).resolve()
    ok = fixture(checker)
    if len(sys.argv) > 2:
        ok = project(checker, sys.argv[2]) and ok
    print("PROBE", "GREEN" if ok else "RED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
