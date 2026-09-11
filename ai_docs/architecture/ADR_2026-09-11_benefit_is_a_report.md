---
description: ADR - the benefit measure reads REVIEW_LOG by header name, reports three coverage buckets, and never carries a verdict. Rejected - a CI gate, width-keyed parsing, folding Hybrid tiers into a moment, counting a non-numeric findings cell as zero.
status: CURRENT
---
# ADR: `benefit` is a report, never a gate

**Status:** Accepted
**Date:** 2026-09-11
**Task ref:** F-050 (ANALYSIS_benefit_report.md)
**Digest:** F-050 — the product's central claim (divergence made visible before implementation) sat unverified in REVIEW_LOG for four months; decision: a `benefit` subcommand that resolves columns BY HEADER NAME across the three legal row widths, reports parsed / unparsed / moment-not-stated as three distinct buckets plus uncounted findings cells, prints the read-cost term beside the catch rate, and always exits 0; rejected a CI gate (a measurement that can fail a build becomes a target), width-keyed parsing (blind to Hybrid's 10-column row), folding Hybrid tiers into a moment by guesswork, and summing a non-numeric findings cell as zero; residual — 46 logged reviews sit beside the ratio because `tier` does not state their moment.

## Context

The methodology's central claim is that it makes divergence visible before
implementation. In four months nobody had computed it, while `SKILL.md` — the one
file every session must read — grew from 4.8 KB to 50 KB. Judgement about whether a
new rule was worth its ceremony was therefore being made with one side of the
ledger visible and the other side not measured at all.

A one-off script answered the question and, on its first run, silently dropped 61 of
63 rows because the log legally carries more than one row width. That failure is the
reason this unit exists in the shape it does.

## Decision

1. **Columns are resolved by header name, never by width.** `templates.md` already
   promised that contract; three widths are legal (8 original, 9 Standalone after
   F-048, 10 Hybrid with `instrument`/`notes` and no `reviewer`). A row whose width
   differs from the header falls back to the positional map for its own width,
   because a mixed log is legal by design.
2. **Three coverage buckets, plus a cell-level one.** Rows parsed; rows unparsed
   (counted and named); and among the parsed, those whose `tier` states a moment
   versus those carrying the Hybrid reviewer weight. A `findings_real` cell stating
   no number is reported as unknown and never summed as zero.
3. **The read cost prints with the benefit, always** — including a line saying so
   when it cannot be measured. Silence there is the catch rate quoted alone.
4. **Always exits 0, emits no warning, and the doctrine says never to wire it into
   CI.** This number is the criterion future units are judged by.

## Alternatives considered

- **A CI gate or a `check` advisory** — rejected: a measurement that can fail a
  build becomes a target, and a targeted measurement stops measuring.
- **Width-keyed parsing** (the first implementation) — rejected at review: it reads
  none of Hybrid's 10-column rows, so a devPNT-governed project sees an empty
  report with a large unparsed count.
- **Folding the Hybrid tiers into design/closure by their documented meaning**
  (`deep`/`light` are design gates, `code` is post-implementation) — rejected as
  inference: it would raise the headline from 68% to about 72% by guesswork. The
  output instead says the unstated set is not moment-neutral and that 68% is a
  floor.
- **Treating a non-numeric findings cell as zero** — rejected: it cannot be
  distinguished from a review that found nothing, and it deflates the one ratio the
  report exists to state.

## Consequences

- **Pro:** the claim is computable by one command in any project using the family;
  the cost term is structurally impossible to omit; every future doctrine unit can
  be asked whether it moves the catch rate or only the byte count.
- **Con / risk:** 46 of 109 logged reviews sit beside the ratio rather than in it,
  because `tier` conflates moment and weight in Hybrid — a later unit could make
  the moment explicit. And the headline invites being quoted without its
  denominator, which the output mitigates with three adjacent disclosure lines but
  cannot prevent.
