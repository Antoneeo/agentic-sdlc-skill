#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-048 assertion harness — capability tiers and the delegation boundary.

Probes the behavioural claims ANALYSIS_capability_tiers.md rests on, against the
real skill family in this repo. Re-runnable; exits non-zero on any FAIL.

RED baseline (pre-implementation, recorded 2026-09-10):
  P1 FAIL  no capability floor is stated anywhere in the doctrine
  P2 FAIL  the Standalone core schema has no `model` column, while review.md
           claims one schema for both modes
  P3 PASS  invariant: review_logged locates `tier` by header, so a new column
           cannot move the gate's reading (replayed on this repo's REAL log)
  P4 FAIL  no delegation boundary is written down
  P5 PASS  invariant: the two spine files are identical across distributions
GREEN target: all five PASS.
"""
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CODE = REPO / "skills" / "agentic-sdlc-skill"
KB = REPO / "distributions" / "kb-agentic-skill" / "skills" / "kb-agentic-skill"
MKT = REPO / "distributions" / "mkt-agentic-sdlc" / "skills" / "mkt-agentic-sdlc"
sys.path.insert(0, str(CODE / "scripts"))
import sdlc_core as sc  # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    print("%s %s%s" % ("PASS" if cond else "FAIL", name,
                       (" — " + detail) if (detail and not cond) else ""))
    if not cond:
        FAILS.append(name)


def read(p):
    return p.read_text(encoding="utf-8")


def norm(text):
    """LF-normalized, for cross-distribution byte comparison."""
    return text.replace("\r\n", "\n")


def tier_key(value):
    """The comparable head of a `model` value: `below floor: only rung ...` and
    `single (client exposes no choice)` both carry a tail the value set does
    not enumerate, and comparing the whole cell would reject legal content."""
    return value.split(":")[0].split("(")[0].strip().strip("`*")


def real_log_lines():
    """The repo's own REVIEW_LOG rows — the corpus the policy must fit."""
    log = REPO / "ai_docs" / "audit" / "reviews" / "REVIEW_LOG.md"
    return [ln for ln in read(log).splitlines() if ln.startswith("|")]


def main():
    dispatch = read(CODE / "dispatch.md")
    review = read(CODE / "review.md")

    # --- P1: a capability FLOOR exists, and it is client-relative -------------
    # The floor must (a) name roles that may not start cheap, (b) tie the
    # lowering rule to a threshold signal, (c) fail open on a single-model
    # client. Anchored on the concepts, not on one sentence's wording.
    doctrine = dispatch + "\n" + review
    # NB: "floor" and "capability" each already occur in these files for
    # unrelated reasons (the rung-3 floor, the Capability Ledger), so the
    # anchor is the named term AND the roles it binds — otherwise the
    # assertion passes on coincidence.
    # Ownership (design-review R1, WARN-3): review.md OWNS the floor because it
    # owns the gates the floor binds; dispatch.md CITES it. Asserting both ends
    # is what makes this more than a spelling pin — a floor written in one file
    # and never reachable from the other is the defect that moved it here.
    check("P1a review.md owns the capability floor and dispatch.md cites it",
          "capability floor" in review.lower()
          and "capability floor" in dispatch.lower(),
          "floor missing, or dispatch.md does not point at it")
    check("P1b lowering a tier is tied to a threshold signal",
          "threshold signal" in doctrine.lower(),
          "nothing states WHY a cheap tier is safe where it is safe")
    check("P1c the floor fails open where the client exposes no choice",
          "no choice" in doctrine.lower() or "single-model" in doctrine.lower(),
          "a single-model client would be blocked by a rule it cannot satisfy")
    check("P1d no provider names entered the doctrine",
          not any(n in doctrine for n in ("Opus", "Sonnet", "Haiku", "GPT-")),
          "a provider name in shared doctrine rots at the next model release")

    # --- P2: the core schema records WHAT RAN --------------------------------
    schema_files = {"review.md": review,
                    "templates.md (code)": read(CODE / "templates.md"),
                    "templates.md (kb)": read(KB / "templates.md"),
                    "templates.md (mkt)": read(MKT / "templates.md")}
    missing = [k for k, v in schema_files.items()
               if "| tier | model |" not in v]
    check("P2a every schema statement carries the model column",
          not missing, "missing in: %s" % ", ".join(missing))
    check("P2b 'one schema' is defined as a core plus mode-specific columns",
          "core" in review.lower() and "mode-specific" in review.lower(),
          "the one-schema claim still reads as 'identical column list', which "
          "Standalone and Hybrid never were")

    # --- P2c/P2d: REAL cross-file constraints, not word presence -------------
    # The floor declares a value set for `model`. Two things must then hold that
    # no amount of typing in one file can fake: the set must be expressible in
    # the log (every value used in the repo's REAL log belongs to it), and the
    # per-lens templates must document the same values the spine declares.
    # Two of the five legal values carry a tail — `single (client exposes no
    # choice)` and `below floor: <reason>` — so a regex demanding a closing
    # backtick right after the word silently drops them, and P2d then FAILS on
    # perfectly legal log content. Match the whole backticked token, compare on
    # its key.
    raw = re.findall(r"`(deep|light|economy|single[^`]*|below floor[^`]*)`",
                     review)
    values = sorted({tier_key(v) for v in raw})
    check("P2c the floor declares its full value set for `model`",
          len(values) >= 5,
          "found %r — a floor whose vocabulary the log cannot express is not a "
          "policy" % values)
    # The floor must be a PARSED table, not prose: at least two role->tier rows.
    floor_rows = [ln for ln in review.splitlines()
                  if ln.startswith("|") and re.search(r"\*\*(deep|light|economy)\*\*", ln)]
    check("P2f the floor is a table naming at least two role->tier pairs",
          len(floor_rows) >= 2,
          "found %d parseable role rows — a floor stated only in prose cannot "
          "be checked against a role" % len(floor_rows))
    # Only rows written under the widened header are checked: a historical
    # 8-cell row legitimately has no `model` cell (FS: mixed logs are legal),
    # and reading index 3 on one would sample `reviewer` instead.
    rows = real_log_lines()
    hdr = next((r for r in rows if "| tier |" in r and "| verdict |" in r), None)
    hcells = [c.strip().lower() for c in hdr.strip().strip("|").split("|")] if hdr else []
    midx = hcells.index("model") if "model" in hcells else None
    unknown = []
    if midx is not None:
        for ln in rows[2:]:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) != len(hcells):
                continue                      # historical width: no model cell
            v = tier_key(cells[midx])
            if v and v not in values:
                unknown.append(v)
    check("P2d every `model` value in the real log is one the floor declares",
          midx is not None and not unknown,
          "no model column in the log header" if midx is None
          else "log uses %r, floor declares %r" % (sorted(set(unknown)), values))
    tpl_code = read(CODE / "templates.md")
    absent = [v for v in values if v not in tpl_code]
    check("P2e the per-lens template documents the values the spine declares",
          bool(values) and not absent,
          "no values declared yet" if not values else
          "declared in review.md but undocumented in templates.md: %r" % absent)

    # --- P3 (invariant): the gate reads `tier` by header ---------------------
    # Replay on this repo's REAL review log: take a genuine design row, widen it
    # with the new column, and require the gate to still find it. Then negate
    # the condition (a closure-only log) and require it to NOT fire.
    real_log = read(REPO / "ai_docs" / "audit" / "reviews" / "REVIEW_LOG.md")
    real_rows = [ln for ln in real_log.splitlines()
                 if ln.startswith("|") and "ANALYSIS_kb_row_atomicity" in ln]
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "ai_docs" / "audit" / "reviews").mkdir(parents=True)
        header = ("| date | doc_key | tier | model | reviewer | findings_raised "
                  "| findings_real | verdict | revise_rounds |")
        rule = "|---|---|---|---|---|---|---|---|---|"
        widened = []
        for ln in real_rows:
            cells = ln.strip().strip("|").split("|")
            cells.insert(3, " deep ")   # the new column, after `tier`
            widened.append("|" + "|".join(cells) + "|")
        (root / sc.review_log_rel()).write_text(
            "\n".join([header, rule] + widened) + "\n", encoding="utf-8")
        check("P3a the design gate still fires under the widened schema",
              sc.review_logged(root, "ANALYSIS_kb_row_atomicity.md"),
              "adding a column broke the gate's tier lookup")
        # negate it: same file with the design row removed -> must NOT fire
        closure_only = [r for r in widened if "| closure |" in r]
        (root / sc.review_log_rel()).write_text(
            "\n".join([header, rule] + closure_only) + "\n", encoding="utf-8")
        check("P3b the probe can fail: a closure-only log does not satisfy it",
              not sc.review_logged(root, "ANALYSIS_kb_row_atomicity.md"),
              "the assertion is vacuous — it passes with no design row present")
        # P3c: the MIXED log — a historical 8-cell row under the 9-column
        # header. This is the case the "no historical row needs rewriting"
        # claim is actually about, and it holds because `model` goes AFTER
        # `tier`, leaving `tier` at index 2 under both schemas.
        historical = [ln for ln in real_rows if "| design |" in ln]
        (root / sc.review_log_rel()).write_text(
            "\n".join([header, rule] + widened + historical) + "\n",
            encoding="utf-8")
        check("P3c a mixed log (old rows beside widened ones) still resolves",
              sc.review_logged(root, "ANALYSIS_kb_row_atomicity.md")
              and len(historical) > 0,
              "mixed-width rows broke the lookup, or the fixture had no "
              "historical design row to mix in")

    # --- P5 (invariant): the spine stayed one file ---------------------------
    for name in ("dispatch.md", "review.md"):
        a, b, c = (norm(read(CODE / name)), norm(read(KB / name)),
                   norm(read(MKT / name)))
        check("P5 %s is byte-identical across the three distributions" % name,
              a == b == c, "the spine diverged — port it and re-run "
                           "shared_files.py --update in each")

    # --- P4: the delegation boundary is written down -------------------------
    check("P4a the doctrine says what may be delegated at all",
          "delegated at all" in dispatch.lower()
          or "delegation boundary" in dispatch.lower(),
          "no boundary section in dispatch.md")
    check("P4b it names what must never leave the authoring context",
          "never delegate" in dispatch.lower(),
          "without a never-list the boundary is advice, not a rule")
    # NB: "pointers" already occurs twice for `plan brief`'s own guides field,
    # so counting it proves nothing. The anchor is the general CONDITION.
    check("P4c the brief-as-pointers rule is generalized into a condition",
          "not delegable" in dispatch.lower(),
          "a large brief pays the tokens twice; the rule must be stated as a "
          "general condition of delegability")

    print("\n%d probe(s) failing" % len(FAILS) if FAILS else "\nall probes green")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
