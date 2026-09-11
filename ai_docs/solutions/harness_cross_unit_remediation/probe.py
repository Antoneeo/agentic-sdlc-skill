#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-053 assertion harness — the cross-unit remediation.

Five defects found by a review run on a DIFFERENT model after six units had
shipped, each reviewed in isolation by the same model family as its author;
four more found by the overdue scoped re-review this unit finally ran.

**The mechanism this file kept failing at, named so it stops recurring.** Twice
now — R1 and R2 of its own design review — probes in this harness were
satisfiable by a LITERAL: a hardcoded `0% to 100%` band, a fixture that *was*
the live log, a `ground_truth` ignoring its argument, a printed sentence with
the wrong count, a verdict cell containing the word PASS inside the phrase
"cannot honestly read PASS". The pattern is always the same — the probe looked
for a SHAPE in the output instead of recomputing the VALUE and comparing. So:

  **every probe over a computed output recomputes the expected value here and
  compares; every probe over prose is labelled a wording anchor.**

  REAL STRUCTURE — P1a/P1b (one structural signal, `revise_rounds`, and no
  prose parsing at all); P4b/P4g (recompute and compare integers); P4c/P4d
  (arithmetic and a count); P4e/P4f (negation controls); P5b/P5c (call the
  other harness's functions on synthetic input with known answers, and drive
  its invariants to False); P2c/P3c (RUN the named battery test per lens, and
  prove it fails on a lens whose rule has been stripped); P3b (positions in
  the contract); P6 (byte identity); P7 (three sibling harnesses).

  WORDING ANCHORS — P2a, P2b, P3a, P4a. They catch deletion and drift, not
  meaning.

RED baseline (pre-implementation, 2026-09-11) — 21 probes then, **15 failing**.
The harness now carries 22: P4i was added at the closure round and so has no
baseline reading, and P3b's label below is the one that ran that day, since
narrowed deliberately. Transcribed from an actual run, because two earlier cuts
stated counts that matched neither each other nor reality (R2 N4, R3 finding 5):
  FAIL  P1a  7 row(s): ANALYSIS_authoring_floor.md (F-049: the floo; F-049 implementation diff (rev
  PASS  P1b  the SHIPPED backlog of unconverged reviews does not grow
  FAIL  P2a  missing in: kb
  FAIL  P2b  a lens naming auto-accept without saying what to do instead is a label, not a guarante
  FAIL  P3a  missing in: kb, mkt
  PASS  P3b  the pointer PRECEDES the lens's first authoring instruction, and cites review.md
  FAIL  P2c  a test that skips — or survives — the lens that was missing the rule is how this defec
  FAIL  P3c  a test that skips — or survives — the lens that was missing the rule is how this defec
  FAIL  P4a  folding the post-implementation rows LOWERS the design share, so the printed figure is
  FAIL  P4b  printed absent, recomputed 56%-71% — a band the probe does not recompute is a band the
  FAIL  P4c  the term that fell is printed and the term that grew is lumped: the total is the only 
  FAIL  P4d  found 0 itemised support files; a single total still hides WHICH file grew, which was 
  PASS  P4e  the interval is absent when no row's moment is unstated
  PASS  P4f  the interval is absent when unstated rows carry NO countable findings
  FAIL  P4g  printed nothing, recomputed 7 — unsaid or miscounted, the band reads narrower than hon
  FAIL  P4h  on a synthetic log expecting 40%-70% and 1 outside, the report printed no band and no 
  FAIL  P5a  review.md makes a probe that no longer passes a finding; this one rots on every review
  FAIL  P5b  no FIXTURE file; ground_truth() does not read its argument (synthetic log expecting (2
  FAIL  P5c  no invariants()
  ----  P4i  no baseline reading: added at the closure round. Exactly ONE band
             must be printed — reading only the first match lets a decoy under
             another branch survive every other check
  PASS  P6   review.md is byte-identical across the three distributions
  PASS  P7   the harnesses of the three remediated units stay green
GREEN target: all 22 PASS.
"""
import importlib.util
import os
import sys as _sys
_sys.dont_write_bytecode = True
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CODE = REPO / "skills" / "agentic-sdlc-skill"
KB = REPO / "distributions" / "kb-agentic-skill" / "skills" / "kb-agentic-skill"
MKT = REPO / "distributions" / "mkt-agentic-sdlc" / "skills" / "mkt-agentic-sdlc"
LENSES = (("code", CODE), ("kb", KB), ("mkt", MKT))
ENTRY = CODE / "scripts" / "sdlc_check.py"
LOG = REPO / "ai_docs" / "audit" / "reviews" / "REVIEW_LOG.md"
BENEFIT_HARNESS = REPO / "ai_docs" / "solutions" / "harness_benefit_report" / "probe.py"

# The instruction to WRITE THE UNIT'S DESIGN DOCUMENT, per lens. The pointer
# must precede it: appending it at the end of the file satisfies a presence
# check while defeating the load order it exists for (R1, mutation M3b-iii).
# Deliberately NOT "the first authoring instruction" -- the code lens's
# Phase-3 preamble and kb's bootstrap bullet both precede the pointer, and
# claiming otherwise would be a claim this probe does not check.
FIRST_AUTHORING = {
    "code": "- Create or update `ai_docs/solutions/ANALYSIS_",
    "kb": "- Create or update `ai_docs/solutions/ANALYSIS_",
    "mkt": "Draft `MKT_VISION.md`",
}
BATTERY_TESTS = {
    "approval": "SkillInvariants.test_human_approval_rule_in_every_lens",
    "pointer": "SkillInvariants.test_authoring_pointer_in_the_contract",
}
# What a copied lens must lose for the named test to go red. If stripping this
# leaves the test green, the test asserts nothing about the rule.
# Two patterns per rule, applied in SEPARATE copies: a test that asserts the
# WORD but not the DUTY stays green under the first strip and must go red
# under the second (F-053 closure review, WARN 7).
STRIP = {
    "approval": (re.compile(r"(?i)auto-accept"),
                 re.compile(r"(?i)explicit confirmation|wait for[^.]{0,24}confirm")),
    "pointer": (re.compile(r"know which tier is authoring"),
                re.compile(r"`review\.md`")),
}

RULE_SHIPPED = "2026-08-06"      # git log -S "Review-driven corrections"
RELEASE_FALLBACK = "2026-09-06"  # used only where .git is absent
# Ratchet over history, MEASURED under the predicate below (R1 F3 caught a
# typed 9; R2's predicate change moves it again -- so it is printed, compared,
# and never argued).
SHIPPED_BACKLOG_CAP = 8

CHILD_ENV = dict(os.environ, PYTHONIOENCODING="utf-8",
                 PYTHONDONTWRITEBYTECODE="1")

FAILS = []


def run(cmd, cwd=None):
    """Explicit encoding everywhere: the platform default decodes a child's
    output through the console codepage and corrupts it silently (ADR
    2026-09-11, conservation reference)."""
    return subprocess.run(cmd, cwd=str(cwd or REPO), capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          env=CHILD_ENV)


def check(name, cond, detail=""):
    print("%s %s%s" % ("PASS" if cond else "FAIL", name,
                       (" — " + detail) if (detail and not cond) else ""))
    if not cond:
        FAILS.append(name)


def read(p):
    return p.read_text(encoding="utf-8")


def core():
    sys.path.insert(0, str(CODE / "scripts"))
    import sdlc_core
    return sdlc_core


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def last_release_date():
    try:
        tag = run(["git", "tag", "--sort=-creatordate"])
        first = (tag.stdout or "").splitlines()
        if tag.returncode != 0 or not first:
            return RELEASE_FALLBACK, "fallback (no tags)"
        d = run(["git", "log", "-n", "1", "--format=%ad", "--date=short",
                 first[0].strip()])
        out = (d.stdout or "").strip()
        if d.returncode != 0 or not re.match(r"^\d{4}-\d{2}-\d{2}$", out):
            return RELEASE_FALLBACK, "fallback (tag undated)"
        return out, "tag %s" % first[0].strip()
    except Exception:
        return RELEASE_FALLBACK, "fallback (git unavailable)"


def unconverged(rows, sc, since, before=None):
    """Rows in the window that carried findings and whose record shows no
    second round.

    **One structural signal: `revise_rounds >= 2`.** The first cut also read
    the verdict cell for the words FAIL and PASS, and R2 broke it twice —
    `PASSED after FAILSAFE check` satisfied it, and so did
    `FAIL -> FAIL (cannot honestly read PASS)`, a cell whose whole point is to
    DENY convergence. A cell is prose; the round count is a number. The
    verdict's FORMAT (`FAIL -> PASS`) is a real duty, owned by review.md and
    checked by a human, not by a regex over free text.

    A row stating no finding count is not judged (None is not zero). A
    `closure (verification)` row is an author's hand-verification of a
    reproduced blocker, not a review with corrections to fold, and is excluded
    by name -- a known residual: the exemption is by LABEL, so a future row
    could evade the predicate by naming itself that."""
    out = []
    for r in rows:
        if r["date"] < since or (before and r["date"] >= before):
            continue
        if "(verification)" in r["tier"].lower():
            continue
        if not sc.review_findings(r["findings_real"]):
            continue
        if (sc.review_findings(r["revise_rounds"]) or 0) >= 2:
            continue
        out.append(r)
    return out


def bounds(rows, sc):
    """Re-derive what the report must print, from the log, independently.

    `code` rows are post-implementation BY DEFINITION (the closure gate), so
    their findings belong to the closure side of the upper bound -- the
    deleted sentence had the fact right and only the direction wrong (R1, F6a).
    Returns (lower, upper, uncountable) or None when there is nothing to bound.
    """
    design = closure = unstated = unstated_code = uncountable = 0
    for r in rows:
        tier = r["tier"].lower()
        n = sc.review_findings(r["findings_real"])
        if tier.startswith("design"):
            design += n or 0
        elif tier.startswith("closure"):
            closure += n or 0
        elif n is None:
            uncountable += 1
        else:
            unstated += n
            if tier.startswith("code"):
                unstated_code += n
    stated = design + closure
    if not stated or not unstated:
        return None
    return (100.0 * design / (stated + unstated),
            100.0 * (design + unstated - unstated_code) / (stated + unstated),
            uncountable)


HEADER = ("| date | doc_key | tier | model | reviewer | findings_raised | "
          "findings_real | verdict | revise_rounds |\n"
          "|---|---|---|---|---|---|---|---|---|\n")
STATED = ("| 2026-01-01 | A.md | design | deep | sub | 4 | 4 | "
          "FAIL -> PASS | 2 |\n"
          "| 2026-01-02 | B.md | closure | deep | sub | 2 | 2 | PASS | 1 |\n")
# A SECOND known answer, because one is satisfied by `return (2, 6, 4)`
# (R3, finding 1). No constant satisfies both.
STATED2 = STATED + ("| 2026-01-03 | C.md | design | deep | sub | 3 | 3 | "
                    "PASS | 1 |\n")
# A log with unstated rows whose bounds are known and DIFFERENT from the live
# log's, so a conditional literal equal to today's figures cannot pass
# (R3, finding 4): design 4, closure 2, unstated 3 + 1 code, one uncountable
# -> 40%..70%, 1 row outside.
MIXED = STATED + (
    "| 2026-01-04 | D.md | deep | deep | sub | 3 | 3 | PASS | 1 |\n"
    "| 2026-01-05 | E.md | code | deep | sub | 1 | 1 | PASS | 1 |\n"
    "| 2026-01-06 | F.md | vision | deep | sub | 9 | all | PASS | 1 |\n")
# Whole percentages, matching the report's existing `%.0f%%` idiom. Stated in
# the Functional Spec so the implementer reads it there, not off a red probe.
BAND = r"(\d+)%\s*(?:-|–|—|to|\.\.)\s*(\d+)%"


def lens_copy(tmp, name, d, pattern):
    """A lens in a scratch tree, with `pattern` stripped from its contract.

    Laid out so the battery's own `parents[1]`/`parents[3]` still resolve.
    __pycache__ and fixtures are skipped: the named test reads SKILL.md."""
    dest = Path(tmp) / "r" / "s" / "skills" / name
    dest.parent.mkdir(parents=True)
    # The WHOLE lens, so the stripped pattern is the ONLY difference between
    # this tree and the real one. Copying a subset makes every other missing
    # file a confound, and any unrelated failure then counts as "went red
    # without the rule" (R3, finding 3).
    # `fixtures/` is excluded: its golden trees are deep, and under a long
    # temp prefix the copy exceeds Windows MAX_PATH and the probe CRASHES
    # instead of reporting (F-053 closure review, WARN 8 -- the depth comes
    # from the temp root, not from the checkout). Not a confound for the two
    # named tests, which read SKILL.md and hybrid.md and nothing else; the
    # unstripped control below proves the copy is sound before any strip is
    # believed.
    shutil.copytree(d, dest,
                    ignore=shutil.ignore_patterns("__pycache__", "fixtures"))
    for f in ("SKILL.md", "hybrid.md"):
        src = dest / f
        if src.is_file():
            # Substitution over the whole TEXT, not a line filter: these
            # contracts are hard-wrapped, so a duty written "wait for
            # explicit\nconfirmation" survives any per-line strip while the
            # battery's own regex (which spans the wrap) still finds it. The
            # first cut stripped by line, which in the code lens applied the
            # mutation to `hybrid.md` and NOT to `SKILL.md` -- a half-applied
            # mutation reported as a surviving one.
            src.write_text(pattern.sub("", read(src)), encoding="utf-8")
    return dest / "scripts"


def battery_test(scripts_dir, dotted):
    p = run([sys.executable, "-m", "unittest", "-v",
             "test_skill_invariants." + dotted], cwd=scripts_dir)
    return p.returncode, (p.stdout + p.stderr)


def main():
    sc = core()
    rows, unparsed = sc.parse_review_log(read(LOG))
    release, how = last_release_date()

    # --- P1: the scoped-re-review debt (item 1) -----------------------------
    print("[context] rows parsed %d, unparsed %d; release cutoff %s (%s)"
          % (len(rows), len(unparsed), release, how))
    open_window = unconverged(rows, sc, release)
    check("P1a no unreleased review carries findings with no second round",
          not open_window,
          "%d row(s): %s" % (len(open_window),
                             "; ".join(r["doc_key"][:44] for r in open_window)))
    shipped = unconverged(rows, sc, RULE_SHIPPED, before=release)
    check("P1b the SHIPPED backlog of unconverged reviews does not grow",
          len(shipped) <= SHIPPED_BACKLOG_CAP,
          "%d shipped rows violate the rule, cap is %d — history is history, "
          "but it may not increase" % (len(shipped), SHIPPED_BACKLOG_CAP))

    # --- P2/P3: the two rules that must reach every lens ---------------------
    def contract(d):
        t = read(d / "SKILL.md")
        h = d / "hybrid.md"
        return t + (read(h) if h.is_file() else "")
    missing = [n for n, d in LENSES
               if not re.search(r"(?i)auto-accept", contract(d))]
    check("P2a (wording) every lens states the never-auto-accept rule",
          not missing, "missing in: %s" % ", ".join(missing))
    weak = [n for n, d in LENSES
            # `[^.]` spans a hard wrap, matching the battery's own regex: the
            # code lens writes "wait for explicit\nconfirmation".
            if not re.search(r"(?i)explicit confirmation|wait for[^.]{0,24}confirm",
                             contract(d))]
    check("P2b (wording) the rule states the duty, not only the word",
          not weak,
          "a lens naming auto-accept without saying what to do instead is a "
          "label, not a guarantee — thin in: %s" % ", ".join(weak))
    absent = [n for n, d in LENSES
              if "know which tier is authoring" not in read(d / "SKILL.md")]
    check("P3a (wording) the authoring pointer is in all three contracts",
          not absent, "missing in: %s" % ", ".join(absent))
    late, unowned = [], []
    for n, d in LENSES:
        t = read(d / "SKILL.md")
        if "know which tier is authoring" not in t:
            continue
        i = t.index("know which tier is authoring")
        if not re.search(r"know which tier is authoring[\s\S]{0,600}?`review\.md`",
                         t):
            unowned.append(n)
        anchor = FIRST_AUTHORING[n]
        if anchor not in t or t.index(anchor) < i:
            late.append(n)
    check("P3b the pointer precedes the lens's instruction to WRITE ITS "
          "DESIGN DOCUMENT, and cites review.md",
          not late and not unowned,
          "after the instruction in: %s; restating instead of citing in: %s "
          "— a rule that arrives after drafting is the load-order defect "
          "F-049's review raised" % (", ".join(late) or "-",
                                     ", ".join(unowned) or "-"))

    # --- P2c/P3c: the battery asserts both, in EVERY lens, non-vacuously ----
    # The first cut grepped the battery's source and a bare comment satisfied
    # it (R1, F4). The second RAN the test but an empty body passed (R2, N7).
    # This one runs it AND strips the rule from a copied lens: a test that
    # stays green without the rule asserts nothing about the rule.
    for key, label in (("approval", "P2c the approval rule is pinned by a "
                                    "battery test that runs, skips no lens, "
                                    "and fails without the rule"),
                       ("pointer", "P3c the authoring pointer is pinned by a "
                                   "battery test that runs, skips no lens, "
                                   "and fails without the pointer")):
        bad = []
        for n, d in LENSES:
            # The UNSTRIPPED copy first. Without it, a copy broken for any
            # unrelated reason makes every strip "go red" and the probe passes
            # vacuously -- the confound the whole-lens copy was meant to close,
            # re-opened by excluding `fixtures` (F-053 closure review).
            with tempfile.TemporaryDirectory() as tmp:
                crc, _ = battery_test(
                    lens_copy(tmp, n, d, re.compile(r"(?!x)x")),
                    BATTERY_TESTS[key])
            if crc != 0:
                bad.append("%s (the UNSTRIPPED copy already fails: every "
                           "strip below would be meaningless)" % n)
                continue
            rc, blob = battery_test(d / "scripts", BATTERY_TESTS[key])
            if "has no attribute" in blob or "Failed to import" in blob:
                bad.append("%s (test does not exist)" % n)
                continue
            if rc != 0:
                bad.append("%s (fails on the real lens)" % n)
                continue
            if re.search(r"\bskipped\b", blob, re.I):
                bad.append("%s (skipped)" % n)
                continue
            for i, pattern in enumerate(STRIP[key]):
                with tempfile.TemporaryDirectory() as tmp:
                    mrc, _ = battery_test(lens_copy(tmp, n, d, pattern),
                                          BATTERY_TESTS[key])
                if mrc == 0:
                    bad.append("%s (green with %s stripped)"
                               % (n, "the rule" if i == 0 else "its duty"))
        check(label, not bad,
              "a test that skips — or survives — the lens that was missing "
              "the rule is how this defect reached a release behind a green "
              "battery: %s" % ", ".join(bad))

    # --- P4: the benefit report (item 4) ------------------------------------
    p = run([sys.executable, str(ENTRY), "benefit", "--root", str(REPO)])
    out = p.stdout + p.stderr
    check("P4a (wording) the inverted bias sentence is gone",
          "floor, not a ceiling" not in out,
          "folding the post-implementation rows LOWERS the design share, so "
          "the printed figure is a ceiling with respect to them")
    want = bounds(rows, sc)
    bands = re.findall(BAND, out)
    band = re.search(BAND, out)
    # Reading only the FIRST match lets a decoy band printed under another
    # branch survive every other check (F-053 closure review, note on P4b).
    check("P4i exactly one interval is printed",
          len(bands) == (1 if want else 0),
          "found %d bands, expected %d" % (len(bands), 1 if want else 0))
    # EQUALITY with the recomputed bounds, and nothing else: the first cut
    # asserted containment of the headline, which a hardcoded 0%-100% band
    # satisfies (R2, M4b-i) and which is algebraically false for some honest
    # logs anyway (R2, out-of-scope note).
    ok = bool(want and band
              and (int(band.group(1)), int(band.group(2)))
              == (int(round(want[0])), int(round(want[1]))))
    check("P4b the printed interval equals the one recomputed from the log",
          ok,
          "printed %s, recomputed %s — a band the probe does not recompute is "
          "a band the report can invent"
          % (band.groups() if band else "absent",
             ("%.0f%%-%.0f%%" % want[:2]) if want else "n/a"))
    cost = re.search(r"SKILL\.md ([\d,]+) bytes.*?\+ ([\d,]+) bytes.*?"
                     r"=\s*([\d,]+) bytes", out, re.S)
    total_ok = cost and (int(cost.group(1).replace(",", ""))
                         + int(cost.group(2).replace(",", ""))
                         == int(cost.group(3).replace(",", "")))
    check("P4c the read-cost line prints the total, and it adds up",
          bool(total_ok),
          "the term that fell is printed and the term that grew is lumped: "
          "the total is the only figure neither half can be quoted without")
    itemised = len(re.findall(r"^\s+\S+\.md\s+[\d,]+\b", out, re.M))
    check("P4d the support files are itemised, not only summed",
          itemised >= 3,
          "found %d itemised support files; a single total still hides WHICH "
          "file grew, which was the original finding" % itemised)

    def benefit_on(log_text):
        d = tempfile.mkdtemp()
        root = Path(d)
        (root / "ai_docs" / "audit" / "reviews").mkdir(parents=True)
        (root / "ai_docs" / "audit" / "reviews" / "REVIEW_LOG.md").write_text(
            log_text, encoding="utf-8")
        q = run([sys.executable, str(ENTRY), "benefit", "--root", str(root)])
        return q.stdout + q.stderr

    check("P4e the interval is absent when no row's moment is unstated",
          re.search(BAND, benefit_on(HEADER + STATED)) is None,
          "an interval printed unconditionally says nothing about the data")
    check("P4f the interval is absent when unstated rows carry NO countable "
          "findings",
          re.search(BAND, benefit_on(
              HEADER + STATED
              + "| 2026-01-03 | C.md | vision | deep | sub | 3 | all | PASS "
                "| 1 |\n")) is None,
          "the uncertainty set is the FINDINGS, not the rows: unstated rows "
          "whose count is unknown widen nothing and must not fake a band")
    # RECOMPUTED, not matched: the first cut accepted any sentence of the right
    # shape, so a literal `0 unstated rows ... outside both bounds` passed it
    # while the true count was 7 (R2, N2).
    said = re.search(r"(\d+)\s+(?:unstated\s+)?rows?\b[^\n]*?no\s+(?:findings\s+)?"
                     r"(?:count|number)", out)
    check("P4g the count of rows outside both bounds is printed, and is right",
          want is not None and (want[2] == 0
                                or (said is not None
                                    and int(said.group(1)) == want[2])),
          "printed %s, recomputed %s — unsaid or miscounted, the band reads "
          "narrower than honesty allows"
          % (said.group(1) if said else "nothing",
             want[2] if want else "n/a (nothing to bound)"))
    # POSITIVE CONTROL on synthetic data whose answers differ from the live
    # log's: without it, a conditional literal equal to today's figures
    # (`56%-71%`, `7 rows`) passes P4b and P4g (R3, finding 4).
    mixed_out = benefit_on(HEADER + MIXED)
    mrows, _ = sc.parse_review_log(HEADER + MIXED)
    mwant = bounds(mrows, sc)
    mband = re.search(BAND, mixed_out)
    msaid = re.search(r"(\d+)\s+(?:unstated\s+)?rows?\b[^\n]*?no\s+"
                      r"(?:findings\s+)?(?:count|number)", mixed_out)
    check("P4h the band and the count are RECOMPUTED, not remembered",
          bool(mwant and mband and msaid
               and (int(mband.group(1)), int(mband.group(2)))
               == (int(round(mwant[0])), int(round(mwant[1])))
               and int(msaid.group(1)) == mwant[2]),
          "on a synthetic log expecting %s and %s outside, the report printed "
          "%s and %s"
          % (("%.0f%%-%.0f%%" % mwant[:2]) if mwant else "n/a",
             mwant[2] if mwant else "n/a",
             mband.groups() if mband else "no band",
             msaid.group(1) if msaid else "no count"))

    # --- P5: the benefit harness stops rotting (item 5) ---------------------
    rc = run([sys.executable, str(BENEFIT_HARNESS)]).returncode
    check("P5a harness_benefit_report is green against the current tree",
          rc == 0,
          "review.md makes a probe that no longer passes a finding; this one "
          "rots on every review anyone ever logs")
    bh = None
    try:
        bh = load(BENEFIT_HARNESS, "_f053_bh")
    except Exception as exc:                                  # pragma: no cover
        check("P5b the harness is importable without running", False, str(exc))
    if bh is not None:
        fixture = getattr(bh, "FIXTURE", None)
        gt = getattr(bh, "ground_truth", None)
        pinned = (getattr(bh, "TRUE_ROWS", None),
                  getattr(bh, "TRUE_FINDINGS", None),
                  getattr(bh, "TRUE_DESIGN", None))
        why = []
        if fixture is None or not Path(fixture).is_file():
            why.append("no FIXTURE file")
        elif Path(fixture).resolve() == LOG.resolve():
            why.append("FIXTURE *is* the live log")
        if not callable(gt):
            why.append("no ground_truth()")
        else:
            # Unconditional, on synthetic input with a known answer. The first
            # cut inferred "ignores its argument" from equal outputs on two
            # real logs, which is legitimate whenever they differ only in rows
            # it does not count -- so it missed the stub on a fresh freeze and
            # flagged an honest harness after this unit's own log edits (R2,
            # blocker 1).
            for text, expect in ((HEADER + STATED, (2, 6, 4)),
                                 (HEADER + STATED2, (3, 9, 7))):
                try:
                    got = tuple(gt(text))
                except Exception as exc:      # a probe reports, never crashes
                    got = "raised %s: %s" % (type(exc).__name__, exc)
                if got != expect:
                    why.append("ground_truth() does not read its argument "
                               "(synthetic log expecting %s returned %s)"
                               % (expect, got))
                    break
            try:
                if fixture is not None and Path(fixture).is_file() \
                        and tuple(gt(read(Path(fixture)))) != pinned:
                    why.append("pins %s do not describe the fixture" % (pinned,))
            except Exception:
                pass    # already reported above
        # ... and the pins must be LITERALS someone edits deliberately: derive
        # them from the fixture at import and the drift detector detects
        # nothing (R2, N8).
        src = read(BENEFIT_HARNESS)
        for pin in ("TRUE_ROWS", "TRUE_FINDINGS", "TRUE_DESIGN"):
            if not re.search(r"^%s\s*=\s*\d+\s*(#.*)?$" % pin, src, re.M):
                why.append("%s is not an integer literal (derive it from the "
                           "fixture at import and the drift detector detects "
                           "nothing)" % pin)
        check("P5b its pins are literals describing a frozen fixture that is "
              "NOT the live log", not why,
              "; ".join(why) + " — a constant pinned to a file that grows is a "
              "standing finding by construction")
        inv = getattr(bh, "invariants", None)
        live = read(LOG)
        grown = live.rstrip("\n") + (
            "\n| 2026-12-31 | ANALYSIS_future.md | design | deep | sub | "
            "3 | 3 | FAIL -> PASS | 2 |\n")
        # The contract, stated because the first cut's control rejected the
        # very invariant the spec recommends (R2, N3): invariants() must hold
        # on the live log and after a review is appended, and must FAIL on a
        # log carrying a row the parser cannot read. `parsed + unparsed ==
        # table rows` closes even then, so it is necessary and not sufficient.
        # TWO unreadable shapes, because one is a literal an implementation
        # can special-case: a short row, and a row whose date cell is not a
        # date (F-053 closure review, note on P5c).
        broken = HEADER + STATED + "| 2026-01-04 | D.md | design |\n"
        broken2 = (HEADER + STATED
                   + "| not-a-date | D.md | design | deep | sub | 1 | 1 | "
                     "PASS | 1 |\n")
        # A row the parser ACCEPTS with an empty `tier`: it then belongs to no
        # moment and vanishes from every bucket. Without this case the
        # emptiness check the closure round added can be deleted and all 22
        # probes stay green -- the ADR's own "checked by removal" rule, applied
        # to the check itself.
        broken3 = (HEADER + STATED
                   + "| 2026-01-05 | E.md |  | deep | sub | 1 | 1 | PASS | 1 |\n")
        why5c = []
        if not callable(inv):
            why5c.append("no invariants()")
        else:
            try:
                if not inv(live)[0]:
                    why5c.append("red on the live log")
                if not inv(grown)[0]:
                    why5c.append("red once one review is appended")
                if inv(broken)[0]:
                    why5c.append("green on a log carrying a short row")
                if inv(broken2)[0]:
                    why5c.append("green on a log whose date cell is not a "
                                 "date")
                if inv(broken3)[0]:
                    why5c.append("green on a row the parser accepts with an "
                                 "empty `tier` cell, which then belongs to no "
                                 "moment at all")
            except Exception as exc:          # a probe reports, never crashes
                why5c.append("raised %s: %s" % (type(exc).__name__, exc))
        check("P5c the LIVE log is guarded by invariants that survive a new "
              "review and still fail on an unreadable row",
              not why5c, "; ".join(why5c))

    # --- P6/P7 invariants: break nothing the six units pinned ---------------
    spines = [read(d / "review.md").replace("\r\n", "\n") for _, d in LENSES]
    check("P6 review.md is byte-identical across the three distributions",
          spines[0] == spines[1] == spines[2],
          "port it and re-run shared_files.py --update in each")
    stale = []
    for h in ("harness_authoring_floor", "harness_mandatory_read_diet",
              "harness_mkt_read_diet"):
        probe = REPO / "ai_docs" / "solutions" / h / "probe.py"
        if run([sys.executable, str(probe)]).returncode != 0:
            stale.append(h)
    check("P7 the harnesses of the three remediated units stay green",
          not stale, "regressed: %s" % ", ".join(stale))

    print("\n%d probe(s) failing" % len(FAILS) if FAILS else "\nall probes green")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
