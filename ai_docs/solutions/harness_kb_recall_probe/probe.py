#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SPIKE harness — kb recall's "second instrument", a NEGATIVE result.

This harness was built to establish a defect and it refuted it. Read
`SPIKE_kb_recall_second_instrument.md` and `replay_2026-09-12.md` beside it
before reusing anything here: the claim was that a descent picking the wrong
branch yields a false `kb: no coverage`, and two agent-level replays — one on a
fixture built to be hostile — returned the right claim instead.

What is left here is the measurement, not the conclusion. P2 measures what each
instrument REACHES at the level of terms; that is a fact, and reading it as
"the descent is blind" was the error, because the descent judges semantic
coverage of concepts, never term presence. P3 is the RED gesture applied to P2:
the same measurement on a control fixture where the term IS in the description.
A harness whose P2 and P3 agree is measuring nothing.

P5 is the one live invariant and it outlived the spike: the ceremony ratchet
forbids a governance cost on a trivial edit, a claim on an existing topic is L1,
and an inventory joining the validator's freshness check would make that L1 edit
re-run `index` or go red — out, with no owner-acceptance door below L1. P5 pins
the two entries that may be in that tuple.

Assertions the abandoned remedy needed (a mandated text probe in the recall
verdict, a claims-inventory builder) are NOT here: a harness pinning what was
decided against is red by construction, which is a defect, not diligence.

Result, 2026-09-12: P2a/P2b/P3/P5 all PASS, and they do not establish the
defect. The unit that shipped instead is the multi-slug verdict form, pinned in
`scripts/test_kb_recall.py::test_the_verdict_form_admits_every_branch_the_descent_opened`.
"""
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
KB = REPO / "distributions" / "kb-agentic-skill" / "skills" / "kb-agentic-skill"

FAILS = []


def check(name, cond, detail=""):
    print("%s %s%s" % ("PASS" if cond else "FAIL", name,
                       (" -- " + detail) if (detail and not cond) else ""))
    if not cond:
        FAILS.append(name)


def read(p):
    return p.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# The fixture: one topic whose INDEX row shares no VOCABULARY with the
# question, while a claim inside answers it. Nothing about it is exotic -- a
# description summarizes a topic, it does not enumerate its claims -- and that
# is exactly why the shape does not reproduce a miss: the summary still covers
# the concept. `fixture_kb2/` (8 topics, a more plausible decoy branch) is the
# harder shape, and it did not reproduce one either.
# --------------------------------------------------------------------------
QUESTION_TERM = "canary"

TOPIC_BODY = """---
topic: deployment
description: %s
parents: []
status: CURRENT
---

## Claims

| id | claim | valid | qty | about | source | prov | state |
|---|---|---|---|---|---|---|---|
| c-dp-01 | The canary window is 30 minutes before full rollout | - | 30 min | - | corpus/notes/release-elicited.md#L3-3 | ELICITED | OK |
| c-dp-02 | Rollback is manual and owned by the release engineer | - | - | - | corpus/notes/release-elicited.md#L7-7 | ELICITED | SUPERSEDED c-dp-03 |
| c-dp-03 | Rollback is automatic on a failed health gate | from 2026-09-01 | - | - | corpus/notes/release-ruling.md#L4-4 | RULING | OK |
"""

INDEX_BODY = """# Topic Index

| topic | description | parents | synonyms |
|---|---|---|---|
| deployment | %s | | rilascio |
"""

DESC_DEFECT = "how releases reach production, and who approves them"
DESC_CONTROL = "how releases reach production, including the canary window"


def build_fixture(root, description):
    topics = root / "topics"
    topics.mkdir(parents=True, exist_ok=True)
    (topics / "deployment.md").write_text(TOPIC_BODY % description, encoding="utf-8")
    (topics / "INDEX.md").write_text(INDEX_BODY % description, encoding="utf-8")
    return topics


def index_row_carries(topics, term):
    """The index row's own text -- the four columns a descent reads."""
    return term.lower() in read(topics / "INDEX.md").lower()


def text_search_reaches(topics, term):
    """What a text search over topics/ reaches -- claim rows included."""
    return any(term.lower() in read(p).lower()
               for p in sorted(topics.glob("*.md")) if p.name != "INDEX.md")


def main():
    # `--emit <dir>` materializes the fixture so an agent-level replay runs on
    # the SAME bytes these assertions measure -- one source, never a retyped copy.
    if len(sys.argv) == 3 and sys.argv[1] == "--emit":
        print("fixture written: %s" % build_fixture(Path(sys.argv[2]), DESC_DEFECT))
        return 0

    with tempfile.TemporaryDirectory() as td:
        # --- P2: what each instrument reaches, at term level ----------------
        defect = build_fixture(Path(td) / "defect", DESC_DEFECT)
        check("P2a the index row does not carry the question's term",
              not index_row_carries(defect, QUESTION_TERM),
              "%r appears in the index row" % QUESTION_TERM)
        check("P2b a text search over topics/ reaches the claim",
              text_search_reaches(defect, QUESTION_TERM),
              "%r not found in topic bodies" % QUESTION_TERM)

        # --- P3: the RED gesture -- the measurement can come out otherwise --
        control = build_fixture(Path(td) / "control", DESC_CONTROL)
        check("P3 control fixture flips P2a (the measurement discriminates)",
              index_row_carries(control, QUESTION_TERM),
              "control description does not carry %r either -- P2a proves nothing"
              % QUESTION_TERM)

    # --- P5: no new mandatory check (the L1 prohibition, made executable) ---
    # The entries are themselves parenthesized, so the match runs to the end of
    # the assignment line rather than to the first ")".
    src = read(KB / "scripts" / "sdlc_check.py")
    m = re.search(r"^\s*checks = \(.*$", src, re.M)
    entries = re.findall(r'\("(\w+)",', m.group(0)) if m else []
    check("P5 freshness check carries exactly (topics, corpus)",
          entries == ["topics", "corpus"],
          "found %s -- an inventory in this tuple taxes an L1 claim edit" % (entries,))

    print("")
    print("FAILED: %s" % ", ".join(FAILS) if FAILS
          else "all assertions green -- and they do NOT establish the defect "
               "(see SPIKE_kb_recall_second_instrument.md)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
