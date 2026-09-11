---
workstream: F-050 the benefit report (`sdlc_check.py benefit` - what the gates caught, beside what the doctrine costs to read)
level: L3
branch: main
status: DONE, UNRELEASED
since: 2026-09-10
next: owner's integration call - three reviews spent (design FAIL, closure FAIL, both folded, final re-review pending); the SKILL.md pruning pass is the unit AFTER this one and is measured by it
details: ANALYSIS_benefit_report.md; harness_benefit_report/probe.py
updated: 2026-09-10
---

## Resume logistics

Implemented and in the tree, uncommitted on `main`: `parse_review_log`,
`review_findings`, `_is_fail`/`_is_pass`, `_print_read_cost` and `cmd_benefit` in
`sdlc_core.py` (spine), the `benefit` subcommand, one battery test, the "never a CI
gate" section in all three `ENFORCEMENT.md`, and `benefit` added to every command
surface (three `SKILL.md`, the code-lens docstring, `mkt_check.py`'s usage). Spine
ported x3 with manifests regenerated.

**Do not hand-copy the numbers below into anything.** Run the command; that is the
whole point of the unit, and the first draft of this file carried a byte count taken
before the unit's last edit and never re-run - a stale completion claim, caught by the
closure review. What follows was produced by the shipped command at the moment of
writing:

```
=== benefit: what the process caught, and what it costs to read ===
rows parsed: 109   rows unparsed: 0
reviews with a stated moment: 63   moment not stated by `tier`: 46  (code x8, deep x13, deep (escalated from light: security design) x1, deep (escalated from light: t1 critical rce invariant) x1, guide x1, light x9, review x1, vision x12)
span of the reviews counted below: 2026-07-28 -> 2026-09-10

moment      rows   findings FAIL verdict per review
design        34        402          31       11.8
closure       29        188          18        6.5

Caught BEFORE the code existed: 402 / 590 findings = 68%
Reviews whose verdict contains FAIL: 49 / 63 = 78%   (+2 inconclusive)
(both figures are over the 63 reviews whose moment `tier` states)
(the unstated set is NOT moment-neutral -- 8 `code` rows are known post-implementation -- so the share above is a floor, not a ceiling)

Read cost of agentic-sdlc-skill: SKILL.md 50001 bytes (every session) + 159104 bytes of support files (read on trigger)
```

## What the two reviews changed

Both FAILed. The parser originally read columns BY WIDTH, accepting 8 or 9 cells -
but `templates.md` promises the opposite contract ("extra or reordered columns are
fine, but the header must say `tier`"), and THREE widths are legal: Hybrid's row is 10
cells with `instrument`/`notes` and no `reviewer`. A devPNT-governed project would
have seen every row reported unparsed. It now resolves columns by header, falling back
to the positional map for a row whose width differs, because a mixed log is legal.

Second: a `findings_real` cell stating no number (`all`, `VOID - instrument error`;
seven such rows exist) was silently summed as ZERO, which is the exact defect class
this unit exists to prevent, at cell level instead of row level. It now reports them
as unknown and never as zero.

Third, and the one worth remembering: the harness's own negation control could not
fail - it searched for the word "unparsed" and for `1`, and both match a report
saying `rows unparsed: 0`. Second unit in a row where the defect lived in the
falsifiability instrument rather than in the product.

Open, deliberately: `rulings.md` row, ADR, REVIEW_LOG rows and `mark` are the closure
steps; and whether the Hybrid `tier` vocabulary should carry the moment explicitly, so
the 46 unstated rows join the ratio instead of sitting beside it (a later unit).
