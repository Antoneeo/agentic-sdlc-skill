#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-047 assertion harness — kb row atomicity.

Probes the behavioural claims ANALYSIS_kb_row_atomicity.md rests on, against the
real kb lens in this repo. Re-runnable; each probe prints PASS/FAIL and the run
exits non-zero on any FAIL.

RED baseline (pre-implementation, recorded 2026-09-08):
  P1 FAIL (both remedy sites still say "merge the two rows")
  P2 PASS (collision error fires — invariant)
  P3 FAIL (no plurality note on the motivating bundled row)
  P4 PASS (SUPERSEDED accepts a multi-id list — split is representable)
GREEN target (post-implementation): all four PASS.
"""
import re
import sys
import tempfile
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
KB = REPO / "distributions" / "kb-agentic-skill" / "skills" / "kb-agentic-skill"
sys.path.insert(0, str(KB / "scripts"))
import sdlc_check  # noqa: E402  (the kb entry point)

FAILS = []


def check(name, cond, detail=""):
    print("%s %s%s" % ("PASS" if cond else "FAIL", name,
                       (" — " + detail) if (detail and not cond) else ""))
    if not cond:
        FAILS.append(name)


def make_corpus(tmp, claim_rows):
    """Minimal docs root: one source artifact + sidecar + one topic file."""
    docs = Path(tmp) / "ai_docs"
    (docs / "corpus" / "given").mkdir(parents=True)
    (docs / "topics").mkdir(parents=True)
    src = docs / "corpus" / "given" / "review-notes-00000000.txt"
    # 12 lines so L-locators up to 12 resolve; line 5 carries the bundled comment.
    lines = ["line %d filler" % i for i in range(1, 13)]
    lines[4] = ("The reviewer states the system already allows biometric login, "
                "that account creation requires email verification, and that the "
                "calling station already offers two-factor authentication")
    src.write_text("\n".join(lines), encoding="utf-8")
    digest = sdlc_check.kb_sha256_bytes(src)
    (docs / "corpus" / "given" / "review-notes-00000000.txt.meta.md").write_text(
        "---\nsha256: %s\ndate: 2026-09-08\nprovenance: given\n"
        "extracted_through: complete\n---\n" % digest, encoding="utf-8")
    table = ["# identity", "", "## Claims", "",
             "| id | claim | valid | qty | about | source | prov | state |",
             "|---|---|---|---|---|---|---|---|"] + claim_rows + [""]
    (docs / "topics" / "identity.md").write_text("\n".join(table),
                                                 encoding="utf-8")
    return docs


SRC = "corpus/given/review-notes-00000000.txt"
BUNDLED = ("The reviewer states the system already allows biometric login, "
           "that account creation requires email verification, and that the "
           "calling station already offers two-factor authentication")


def main():
    # --- P1: the widen-or-merge trap is gone from BOTH remedy sites -----------
    dist = (KB / "distillation.md").read_text(encoding="utf-8")
    code = (KB / "scripts" / "sdlc_check.py").read_text(encoding="utf-8")
    trap = "merge the two rows"
    check("P1a distillation.md remedy no longer recommends merging distinct "
          "assertions", trap not in dist, "trap phrase still present")
    # NB: the code literal wraps mid-phrase ("merge the two " + "rows"), so the
    # probe matches the prefix that lives inside one literal — the contiguous
    # phrase would pass vacuously against source text it cannot occur in.
    check("P1b collision message no longer recommends merging distinct "
          "assertions", "or merge the two" not in code,
          "trap phrase still present")
    check("P1c collision message carries narrowing guidance",
          "narrow" in _collision_message(code).lower(),
          "no 'narrow' in the same-span collision message")

    # --- P2 (invariant): same span + same qty, different text => collision ---
    id_a = sdlc_check.kb_claim_id(SRC, "L5-5", "")
    rows = [
        "| %s | assertion one about the span | - | - | - | %s#L5-5 | GIVEN | OK |" % (id_a, SRC),
        "| %s | a different assertion, same span | - | - | - | %s#L5-5 | GIVEN | OK |" % (id_a, SRC),
    ]
    tmp = tempfile.mkdtemp()
    try:
        docs = make_corpus(tmp, rows)
        errs, _w, _n = sdlc_check.kb_check_claims(docs)
        check("P2 collision error fires on two assertions sharing span+qty",
              any("collides" in e for e in errs), "no collision error: %r" % errs)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # --- P3: the motivating bundled row draws a plurality [note] -------------
    id_b = sdlc_check.kb_claim_id(SRC, "L5-5", "")
    rows = ["| %s | %s | - | - | - | %s#L5-5 | GIVEN | OK |" % (id_b, BUNDLED, SRC)]
    tmp = tempfile.mkdtemp()
    try:
        docs = make_corpus(tmp, rows)
        errs, warns, notes = sdlc_check.kb_check_claims(docs)
        check("P3a plurality note fires on the motivating bundled row",
              any("assertion" in n and id_b in n for n in notes),
              "notes: %r" % notes)
        check("P3b plurality is never an error or warning",
              not any(id_b in x for x in errs + warns),
              "escalated beyond note: %r" % (errs + warns))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # --- P4 (invariant): SUPERSEDED accepts a multi-id list => split 1->N ----
    id_c = sdlc_check.kb_claim_id(SRC, "L5-5", "")
    id_d = sdlc_check.kb_claim_id(SRC, "L6-6", "")
    id_e = sdlc_check.kb_claim_id(SRC, "L7-7", "")
    rows = [
        "| %s | the bundle | - | - | - | %s#L5-5 | GIVEN | SUPERSEDED %s, %s |" % (id_c, SRC, id_d, id_e),
        "| %s | atomic part one | - | - | - | %s#L6-6 | GIVEN | OK |" % (id_d, SRC),
        "| %s | atomic part two | - | - | - | %s#L7-7 | GIVEN | OK |" % (id_e, SRC),
    ]
    tmp = tempfile.mkdtemp()
    try:
        docs = make_corpus(tmp, rows)
        errs, _w, _n = sdlc_check.kb_check_claims(docs)
        state_errs = [e for e in errs
                      if "state must be" in e or "resolves to no row" in e]
        check("P4 SUPERSEDED with two successors is legal (split representable)",
              not state_errs, "state errors: %r" % state_errs)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n%d probe(s) failing" % len(FAILS) if FAILS else "\nall probes green")
    return 1 if FAILS else 0


def _collision_message(code_text):
    """The same-span collision message literal, extracted from the source."""
    # End anchor chosen to sit inside ONE source literal ("break the tie");
    # phrases spanning a literal wrap are not findable in raw source text.
    m = re.search(r"collides with the row at.*?break the tie", code_text, re.S)
    return m.group(0) if m else ""


if __name__ == "__main__":
    sys.exit(main())
