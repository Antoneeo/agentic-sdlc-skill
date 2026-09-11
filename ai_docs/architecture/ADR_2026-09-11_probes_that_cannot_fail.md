---
description: ADR - a probe over a computed output must RECOMPUTE the expected value and compare; a probe over prose must be labelled a wording anchor. Adopted after the same defect - an assertion satisfiable by a literal - shipped in five consecutive units and recurred five more times inside the unit convened to remove it, across three review rounds. Rejected - patching each case, relying on reviewer mutation-testing alone, and deleting the wording anchors.
status: CURRENT
---
# ADR: a probe that matches a shape is not a probe

**Status:** Accepted
**Date:** 2026-09-11
**Task ref:** F-053 (ANALYSIS_cross_unit_remediation.md)
**Digest:** F-053 — five consecutive units shipped an assertion satisfiable by a literal, and the unit convened to fix that shipped five more, across three review rounds (design R1 and R2, and the closure round): a hardcoded percentage band, a fixture that was the live log, a `ground_truth` ignoring its argument, a sentence with the wrong count, a verdict cell containing PASS inside "cannot honestly read PASS", an `|ownership` alternative matching the pointer's own inventory, an `invariant` written `1 if x else 1`. Decision: a probe over a computed output recomputes the expected value in the harness and compares, and carries a positive control on synthetic data whose answers differ from the live system's; a probe over prose is labelled a wording anchor in the file and in the ANALYSIS; a probe over a rule's presence strips the rule from a whole-lens copy and requires the check to go red. Rejected: patching each case as found (five units of evidence say it recurs), trusting reviewer mutation-testing alone (it is not run on every commit), and deleting the wording anchors (they catch deletion, which is the commonest real edit).

## Context

`SKILL.md` §Execute-Before-Specify already required that a probe be able to
fail: *"show it red first — negate the condition or the state it asserts — then
green against the real system; a probe you cannot make fail establishes
nothing."* The rule was in force for every unit below. It did not prevent any of
them:

| Unit | The assertion | Why it could not fail |
|---|---|---|
| F-047 | a contiguous phrase spanning two source literals | the phrase existed in neither; the search matched the rendered text |
| F-048 | a value-set regex over `deep\|light\|economy` | two legal values were tailed and unexpressible, so it under-covered silently |
| F-050 | the word "unparsed" and `\b1\b` | both match `rows unparsed: 0`, the very state it existed to catch |
| F-051 | the word `ownership` after the filename | the pointer's own content inventory contains it |
| F-052 | anchors derived from the moved file | deleting a section removes it from both sides |
| F-053 (R1) | containment of a headline in a band | a hardcoded `0%-100%` contains everything |
| F-053 (R1) | "the fixture is frozen" | a fixture that IS the live log satisfies every other clause |
| F-053 (R2) | "`ground_truth` reads its argument", inferred from two real logs | equal outputs are legitimate when the inputs differ only in rows it does not count |
| F-053 (R2) | a printed sentence naming the excluded rows | any sentence of that shape, with any number in it |
| F-053 (closure) | `buckets += 1 if tier.startswith(...) else 1` | both branches add 1 |

One shape recurs in all ten: **the probe looked for a SHAPE in the output
instead of recomputing the VALUE and comparing.** Ten instances across six units
is not ten mistakes; it is one missing rule.

## Decision

1. **Recompute, then compare.** A probe over a computed output derives the
   expected value in the harness, from the same source the system read, and
   asserts equality. Containment, presence and regex-shape are not evidence
   about a computation.
2. **Carry a positive control on synthetic data.** A probe that only ever reads
   the live system accepts a conditional literal equal to today's values. Every
   such probe also runs against synthetic input whose correct answer differs
   from the live one, computed by the same harness function.
3. **Label the anchors.** A probe over prose cannot check meaning. It is named a
   WORDING ANCHOR in the harness docstring and in the ANALYSIS `## Test
   Strategy`, so no reader and no reviewer mistakes it for a proof.
4. **Presence of a rule is checked by removal.** To assert that a check pins a
   rule, strip the rule from a whole copy of the lens and require the check to
   go red — with the strip operating on the TEXT, because these contracts are
   hard-wrapped and a per-line filter silently applies no mutation at all.
5. **A probe reports; it never crashes.** Every call into code under test is
   guarded, because a traceback hides the other twenty results.

## Alternatives considered

- **Patch each case as it is found** — rejected on evidence: five units did
  exactly that, and the sixth reproduced the defect five times while fixing it.
- **Rely on the reviewer's mutation matrix** — rejected: it found all ten, and
  it runs at a gate, not on every commit. A rule the author applies while
  writing is cheaper than a round of review that discovers it afterwards.
- **Delete the wording anchors and keep only structural probes** — rejected:
  deletion is the commonest real edit to a doctrine file, and an anchor catches
  it. The defect was never that anchors exist; it was that they were sold as
  structure.
- **Assert on the whole output byte-for-byte (a golden file)** — rejected: it
  turns every legitimate rewording into a failure, and the harness would be
  updated by copying the new output, which is the fixture-regeneration failure
  this repo already recorded once.

## Consequences

- **Pro:** the rule is one sentence, applies while writing rather than at a
  gate, and is checkable by a reviewer in a single pass — every probe either
  recomputes or is labelled. The three harnesses rebuilt under it (F-050's, this
  unit's, and mkt's) each went red under a mutation they had previously
  survived.
- **Con / risk:** recomputation duplicates the system's logic in the harness, so
  a wrong assumption shared by both agrees with itself. That is why the pins
  stay literals a person edits deliberately, and why the frozen fixture exists:
  the duplicated logic runs against an answer nobody can silently move.
- **Residual:** a positive control is still one known answer. A determined
  literal aimed at both the live and the synthetic case would pass. That is a
  cheat, not a mistake, and the doctrine does not defend against an author
  trying to deceive their own harness.
