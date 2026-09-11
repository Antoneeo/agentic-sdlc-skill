#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-049 assertion harness — the floor reaches the author.

Honest about its own limits: P1c, P1d, P2a, P3a and P3b are WORDING ANCHORS --
they detect deletion and drift, not meaning. A README gutted to keep the pinned
phrases, or a disclosure duty negated around them, stays green (design review,
mutations M8/M9). P1a/P1b (table-row parse), P4 and P5 carry real structure.

RED baseline (pre-implementation, 2026-09-10):
  P1 FAIL  the floor names no authoring role and no session rule
  P2 FAIL  nothing forbids the double below-floor state
  P3 FAIL  the READMEs carry no tier-selection guidance
  P4 PASS  invariant: F-048's floor-table parse still finds >=2 role rows
  P5 PASS  invariant: review.md is byte-identical across the three distributions
GREEN target: all five PASS.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CODE = REPO / "skills" / "agentic-sdlc-skill"
KB = REPO / "distributions" / "kb-agentic-skill" / "skills" / "kb-agentic-skill"
MKT = REPO / "distributions" / "mkt-agentic-sdlc" / "skills" / "mkt-agentic-sdlc"
READMES = (REPO / "README.md",
           REPO / "distributions" / "kb-agentic-skill" / "README.md",
           REPO / "distributions" / "mkt-agentic-sdlc" / "README.md")

FAILS = []


def check(name, cond, detail=""):
    print("%s %s%s" % ("PASS" if cond else "FAIL", name,
                       (" — " + detail) if (detail and not cond) else ""))
    if not cond:
        FAILS.append(name)


def read(p):
    return p.read_text(encoding="utf-8")


def flat(text):
    """Whitespace-normalized, so a line wrap is not read as a change in
    meaning -- an earlier cut of P1d went red on a re-flowed paragraph."""
    return re.sub(r"\s+", " ", text)


def floor_rows(review):
    """The floor's role rows, parsed as TABLE rows — the same shape F-048 pins."""
    return [ln for ln in review.splitlines()
            if ln.startswith("|") and re.search(r"\*\*(deep|light|economy)\*\*", ln)]


def main():
    review = read(CODE / "review.md")
    rows = floor_rows(review)

    # --- P1: the authoring role is IN THE TABLE, and the session rule exists --
    # Parsed as a row, not merely mentioned in prose: a floor a reader cannot
    # look a role up in is guidance, not a floor.
    authoring_rows = [r for r in rows if re.search(r"author", r, re.I)]
    check("P1a the floor table carries an authoring role row",
          len(authoring_rows) == 1,
          "found %d rows naming authoring among %d role rows"
          % (len(authoring_rows), len(rows)))
    check("P1b that row's floor is deep",
          bool(authoring_rows) and "**deep**" in authoring_rows[0],
          "authoring is the purest case of judgement nothing scores")
    check("P1c the session rule is stated (highest floor among its own roles)",
          "highest floor" in review.lower(),
          "without it, a session performing several roles has no floor at all")
    check("P1d the rule fails open where the tier is undeterminable",
          "cannot determine its own tier" in flat(review).lower(),
          "an agent cannot acquire a capability; the rule may bind disclosure "
          "only, and must say so")

    # --- P2: the forbidden state, expressible as a predicate over the log ----
    check("P2a the double below-floor state is forbidden by name",
          "below floor" in review.lower()
          and re.search(r"may not ALSO|not also run a below-floor",
                        review, re.I) is not None,
          "one disclosed weakness is disclosed; two is an artifact nobody "
          "competent read")
    # NB: `model` and `below floor` both already exist from F-048, so testing
    # their presence proves nothing about THIS rule. Anchor on the rule naming
    # the row it is checkable in — a forbidden state no row can express is a
    # slogan.
    # Stronger than the first cut, which only wanted `REVIEW_LOG` near
    # `below-floor`: the rule must name the CELL the disclosure lands in, since
    # the log has no column for the authoring session's tier and saying "the log"
    # would have been an unkeepable promise (design review, BLOCK 2).
    check("P2b the disclosure names the cell it is recorded in",
          re.search(r"`reviewer` cell", flat(review)) is not None
          and re.search(r"`notes`", flat(review)) is not None,
          "the constraint must say where it is visible, or nobody can check it")
    check("P2c the arbitration exception is stated, not left contradictory",
          re.search(r"except when nothing better|The exception is the case",
                    flat(review), re.I) is not None,
          "forbidding the state outright contradicts `independence wins` and "
          "pushes the agent toward the abstention that rule rejects")

    # --- P3: the user-facing guidance, in all three npm front pages ----------
    # Anchored on the SECTION HEADING, not the word "tier": kb's README has a
    # pre-existing "licence tier", so the loose check stayed green when the
    # section was deleted from that lens alone (design review, mutation M4b).
    missing = [p.parent.name for p in READMES
               if not p.is_file()
               or "## Which model to run it on" not in read(p)]
    check("P3a every package README carries tier-selection guidance",
          not missing, "missing in: %s" % ", ".join(missing) if missing else "")
    inherit = [p.parent.name for p in READMES
               if p.is_file() and "not automatically yours" not in read(p).lower()]
    check("P3b each README says the reviewer's tier is not inherited",
          not inherit,
          "the commonest real misconfiguration: a deep session with a cheap "
          "reviewer bound in its agent definition — missing in: %s"
          % ", ".join(inherit))

    # --- P4/P5 invariants: do not break what F-048 pinned --------------------
    check("P4 F-048's floor-table parse still finds at least two role rows",
          len(rows) >= 2, "found %d" % len(rows))
    a, b, c = (read(CODE / "review.md").replace("\r\n", "\n"),
               read(KB / "review.md").replace("\r\n", "\n"),
               read(MKT / "review.md").replace("\r\n", "\n"))
    check("P5 review.md is byte-identical across the three distributions",
          a == b == c, "port it and re-run shared_files.py --update in each")

    print("\n%d probe(s) failing" % len(FAILS) if FAILS else "\nall probes green")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
