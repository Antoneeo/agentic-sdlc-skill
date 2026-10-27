"""F-071 replay: does a doctrine text rule on the two recorded incidents?

Usage: python replay.py --doctrine DIR   (DIR holds review.md and SKILL.md)

Each rule is (anchor in the doctrine) AND (fact measured on the incident). The
facts are read from the snapshot in incident/ and from git (archive tag
archive/software-knowledge, commit 4e29e16, REVIEW_LOG); the anchors from DIR.
Red = the doctrine in DIR does not rule; green = it rules where the drift entered.
Each rule also runs a CONTROL case built to make it silent: a rule that fires on
its control proves nothing. Exit 0 only when every rule fires and every control
is silent (the expected result for the proposed text); exit 1 otherwise.

This replay is the cheap, re-runnable half: it proves the text carries each rule and
the incident facts trigger it, never that a cold agent obeys the text. The gating
half is BEHAVIOR_CASES.md (a cold agent rules six cases on each text).
"""
import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INC = HERE / "incident"
REPO = HERE.parents[2]


def norm(text):
    return re.sub(r"\s+", " ", text)


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                          text=True, encoding="utf-8", check=True).stdout


WHY = re.compile(r"\b(why|perch[eé]|rationale|motivazion\w*)\b", re.I)


# ---- facts measured on the incidents ------------------------------------

def f063_conformance_rows():
    text = (INC / "ai_docs__audit__reviews__REVIEW_software_knowledge_design_2026-10-04.md"
            ).read_text(encoding="utf-8")
    sect = text.split("## Conformance statement R1", 1)[1].split("\n## ", 1)[0]
    return [l for l in sect.splitlines() if l.startswith("| ") and "---" not in l][1:]


def f063_rationale_lines():
    """Lines of knowledge.py functions whose name carries the owner's 'why'."""
    src = git("show", "archive/software-knowledge:skills/agentic-sdlc-skill/scripts/knowledge.py")
    tree = ast.parse(src)
    funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    why = [n for n in funcs if re.search(r"why|rationale|reason|purpose", n.name, re.I)]
    total = sum(n.end_lineno - n.lineno + 1 for n in funcs)
    return sum(n.end_lineno - n.lineno + 1 for n in why), total


def f063_rubric_why_questions():
    text = (INC / "ai_docs__solutions__harness_software_knowledge__BEHAVIOR_RUBRIC.md"
            ).read_text(encoding="utf-8")
    return len(WHY.findall(text))


def f063_benefit_deferred():
    text = (INC / "ai_docs__audit__reviews__REVIEW_software_knowledge_design_2026-10-04.md"
            ).read_text(encoding="utf-8")
    return "beneficio ancora da misurare" in text


SECURITY_PATH = re.compile(r"(auth|crypt|net|http|socket|secret|token)", re.I)


def open_fix_files():
    out = git("show", "--name-only", "--format=", "4e29e16")
    return [l for l in out.splitlines() if l.strip()]


def open_fix_security_sensitive(files):
    """Changed code that is not a test, or a path naming a security area."""
    code = [f for f in files if f.endswith((".py", ".js")) and "/test_" not in f]
    return bool(code) or any(SECURITY_PATH.search(f) for f in files)


CLOSED_KINDS = {"bump", "index", "mark", "shared copy", "changelog"}


def f074_closure_delta_kinds():
    """The kinds of the 2026-10-18 F-074 closure delta, from its REVIEW_LOG row
    (doc_key names them) and the ANALYSIS Diary (the family workflow document)."""
    log = (REPO / "ai_docs/audit/reviews/REVIEW_LOG.md").read_text(encoding="utf-8")
    row = next(l for l in log.splitlines()
               if "bump/CHANGELOG/README/r30/E2E delta after the design PASS" in l)
    assert "| closure |" in row and "| 3 | 3 | PASS |" in row, row
    diary = (REPO / "ai_docs/solutions/ANALYSIS_vision_interview.md").read_text(encoding="utf-8")
    assert "aligned READMEs and the family workflow document" in diary
    return {"bump", "changelog", "readme", "ruling", "e2e", "overview"}


# ---- anchors in the doctrine under test ---------------------------------

def anchors(d):
    review = norm((d / "review.md").read_text(encoding="utf-8"))
    skill = norm((d / "SKILL.md").read_text(encoding="utf-8"))
    return {
        "D1": bool(re.search(r"each outcome the owner named .{0,140}"
                             r"is a row too, weighed by effort", review))
              and "served by a minor share while a secondary concern takes the bulk" in review,
        "D1probe": "red on the baseline" in review,
        "D2": "How the author frames the unit (a new capability, a fix) does not exempt it" in skill
              and bool(re.search(r"owner's words for an outcome .{0,80}name a comparative effect.{0,200}"
                             r"built before code, asks the question the outcome names, "
                             r"and is shown red on the baseline", skill)),
        "D3": "it is due only on a security-sensitive area the lens's Rule Zero names" in review
              and "otherwise does not run and logs no row" in review,
        "D4": "A delta after a PASS reopens a review only where it changes what was judged" in review
              and "The list is closed and content governs it" in review
              and "a change answering a review finding is never in it" in review
              and "NOT DUE:" in review,
    }


# ---- the rules ----------------------------------------------------------

def rule_m4_m2(a, rows, rationale):
    """Design review: the owner's 'why' is a weighed row; none serves it -> finding."""
    served = [r for r in rows if WHY.search(r)]
    share = rationale[0] / rationale[1] if rationale[1] else 0.0
    return a["D1"] and (not served or share < 0.1)


def rule_m3(a, rubric_why, deferred):
    """Before code: the probe asks the outcome's question and is red on baseline."""
    return a["D2"] and a["D1probe"] and (rubric_why == 0 or deferred)


def rule_m5a(a, files):
    """L2 field fix: the closure review is ruled not due."""
    return a["D3"] and not open_fix_security_sensitive(files)


def rule_m5b(a, kinds, after_pass=True, answers_finding=False):
    """Post-PASS delta: its restating part (bump, CHANGELOG) is ruled not due and
    only its judged part (README, overview, E2E, ruling) stays under review."""
    not_due = kinds & CLOSED_KINDS
    return (a["D4"] and after_pass and not answers_finding and bool(not_due)
            and not_due != kinds - CLOSED_KINDS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doctrine", required=True, type=Path)
    a = anchors(ap.parse_args().doctrine)

    rows = f063_conformance_rows()
    rationale = f063_rationale_lines()
    rubric_why = f063_rubric_why_questions()
    deferred = f063_benefit_deferred()
    files = open_fix_files()
    kinds = f074_closure_delta_kinds()

    print("facts: F-063 conformance rows=%d, rows naming the why=%d; knowledge.py "
          "why-named function lines=%d of %d; rubric why-mentions=%d; benefit deferred=%s"
          % (len(rows), sum(bool(WHY.search(r)) for r in rows), rationale[0],
             rationale[1], rubric_why, deferred))
    print("facts: 4e29e16 files=%d, security-sensitive=%s; F-074 closure delta kinds=%s"
          % (len(files), open_fix_security_sensitive(files), sorted(kinds)))
    print("anchors:", {k: v for k, v in a.items()})

    results = [
        ("M4+M2 F-063 design review flags the unserved why", rule_m4_m2(a, rows, rationale), True),
        ("  control: a row serving the why, its share 50%", rule_m4_m2(
            a, rows + ["| why | rationale layer |"], (50, 100)), False),
        ("M3 F-063 promise probe owed before code", rule_m3(a, rubric_why, deferred), True),
        ("  control: rubric asks why, benefit not deferred", rule_m3(a, 3, False), False),
        ("M5a --open L2 fix: review not due", rule_m5a(a, files), True),
        ("  control: the fix changed non-test code", rule_m5a(
            a, files + ["skills/agentic-sdlc-skill/scripts/docs_site.py"]), False),
        ("M5b F-074 delta: bump+CHANGELOG not due, rest scoped", rule_m5b(a, kinds), True),
        ("  control: the delta answers a review finding", rule_m5b(
            a, kinds, answers_finding=True), False),
        ("  control: nothing restating in the delta", rule_m5b(
            a, {"readme", "doctrine"}), False),
        ("  control: F-074 design review (no prior PASS)", rule_m5b(a, kinds, after_pass=False), False),
    ]
    ok = True
    for name, got, want in results:
        mark = "FIRES " if got else "silent"
        good = got == want
        ok &= good
        print("%s  %-55s %s" % (mark, name, "" if good else "<- expected %s" %
                                ("FIRES" if want else "silent")))
    print("RESULT:", "GREEN" if ok else "RED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
