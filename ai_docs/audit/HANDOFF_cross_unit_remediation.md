---
workstream: F-053 cross-unit remediation (defects a cross-lens review on a DIFFERENT model found after six units shipped)
level: L3
branch: main
status: PLANNED
since: 2026-09-11
next: open the ANALYSIS and work the four items below, in the stated order (1 and 3 are correctness, not optimization)
details: this file is the spec until ANALYSIS_cross_unit_remediation.md exists; findings verified in-repo, numbers reproduced
updated: 2026-09-11
---

## Why this unit exists

Six units (F-047 … F-052) shipped in one session, each reviewed in isolation and
each by the same model family as the author. A seventh review was then run **on a
different model**, asked a question no per-unit review can ask: does the sequence,
taken together, make the product less effective or less efficient? It found
defects none of the six could see. **Every number below was re-derived in-repo
before being written here** — do not trust them, re-run them.

## State at the time of writing

Six commits on `main`, **none pushed, no release cut**: `75ccdc5` F-047, `4e9e554`
F-048, `8238d4c` F-050, `b14f266` F-051, `8d4d41b` F-052, `902c36a` F-049. The
published packages (1.32.1 / 1.14.1 / 0.10.1) contain none of this. The three
CHANGELOGs are untouched and a version bump is owed at release.

## The four remediation items

### 1. kb has no human-approval rule (CORRECTNESS)

`grep -rci "auto-accept" distributions/kb-agentic-skill/skills/kb-agentic-skill/*.md`
returns **zero in every file**. The rule "never auto-accept a devPNT proposal:
present the preview and wait for explicit confirmation" exists in the code lens
(now in its `hybrid.md`) and in mkt, and is missing from kb entirely. The code
lens's pointer even asserts the rule "exists nowhere else in this package", which
is true of that package and was never checked against the siblings.

This also **falsifies F-052's premise**: "kb's block is 299 B, not worth moving"
measured the block's SIZE and never its CONTENT. The right question was not
whether to move kb's seam but whether kb's seam says what the others say.

*Fix:* add the rule to kb's Hybrid block. Two lines.

### 2. The F-049 authoring pointer exists in one lens of three (CORRECTNESS-ADJACENT)

`grep -c "Before authoring, know which tier"` → **1 / 0 / 0** (code / kb / mkt).
In kb and mkt the authoring-floor duty lives only in `review.md`, which is loaded
at the design-review gate — i.e. AFTER the artifact is drafted. That is the exact
load-order defect the F-049 design review raised and which was fixed in the code
lens only.

*Fix:* either port the pointer to the two missing lenses, or delete the
agent-facing half everywhere and keep only the README guidance. The reviewer's
judgement, which I share: the agent-facing half is close to inert anyway (a
session cannot map its model name to a tier), so deleting it is defensible and
cheaper than propagating it. **Decide deliberately and record the decision.**

### 3. `benefit`'s bias sentence is inverted, and it reports only the cost that fell (CORRECTNESS)

Two separate defects in `sdlc_core.py` `cmd_benefit`:

- It prints "the share above is a floor, not a ceiling" because 8 `code` rows are
  post-implementation. Folding those rows in **lowers** the design share
  (442/674 = 65.6%), so on the tool's own reasoning it is a **ceiling**. The
  sentence is backwards.
- It excludes 46 of 117 rows — every Hybrid row — because `tier` carries the
  moment in Standalone and the gate weight in Hybrid. Re-derived with the devPNT
  vocabulary mapped (deep/light→design, code→closure) the share is 68.6%: the
  headline survives, its explanation does not.
- The read-cost line prints `SKILL.md` ("every session") plus an undifferentiated
  support-file total. **The number that went down is the one it prints; the
  number that went up is the one it lumps.**

*Fix:* correct the bias sentence; map the Hybrid tier vocabulary to a moment (or
add a `moment` column); print the read cost so the total is visible, not only the
term that shrank.

### 4. The harness pins rot by construction (EFFICIENCY / MAINTENANCE)

`harness_benefit_report/probe.py` is **red at HEAD right now** (4 probes): it pins
65/613/414 and the log holds 71/662/442, because later units in the same session
logged reviews. By design this rots on **every** review anyone ever logs.
`review.md` makes "a probe that no longer passes against the current tree" a
finding, so the repo ships a standing finding.

*Fix:* pin INVARIANTS, not counts — e.g. `parsed + unparsed == table rows` and
`design + closure + unstated == parsed`. Same for the `moved-block-sha256` stamps
(F-051/F-052), which make the Hybrid seam permanently immutable: adding one row to
an ownership matrix requires recomputing a SHA by hand. Consider dropping the
stamp after the release that carries the move.

## The efficiency finding, which is the uncomfortable one

I reported a −9.4% cut. The **total read surface grew in all three lenses**,
measured on git blob sizes at `2199a6d` → `HEAD`:

| Lens | `SKILL.md` | all `.md` |
|---|---|---|
| code | 49,413 → 45,542 (**−7.8%**) | 214,414 → 226,512 (**+5.6%**) |
| kb | 27,516 → 28,667 (**+4.2%**) | 204,273 → 218,702 (**+7.1%**) |
| mkt | 22,648 → 20,995 (**−7.3%**) | 157,112 → 168,312 (**+7.1%**) |

kb's mandatory contract GREW, because it received F-047's citation-scope rule and
no diet. A Hybrid L3 session on the code lens reads roughly **+11%** more than
before; F-051 disclosed +3.9% and F-052 +6.6%, and nobody summed them. The cost
did not fall — it **moved** out of the file the report prints.

## The structural finding, worth more than the four items

Six reviews by the same model family, six rows reading "all findings folded",
five of six FAIL→folded. That is **one loop, not two eyes**. The only point in the
whole session where a claim met a genuinely external criterion was
`SPIKE_citation_scope_benefit.md`, and it came back **NULL**. Whatever this unit
does, it should not be reviewed the same way: use a different model for at least
one gate, as this cross-unit review was.

## Unknowns the reviewer could not settle

- Whether `benefit`'s share means anything for a CODE project: every "design" row
  in this log reviewed Markdown, never source. Settle by running `benefit` on a
  downstream code project's log.
- How noisy `KB_BUNDLE_HINTS` is on a real claim ledger — no kb corpus exists
  here. Settle by running `check` on a populated kb project.
- Why `harness_capability_tiers/probe.py` exits 1 on a pristine `git archive`
  copy while passing in-repo (not console encoding — it passes under
  `PYTHONIOENCODING=cp1252`). Likely reads a path outside `skills/` +
  `distributions/`. Settle by running it in a scratch copy with stderr captured.
- Whether the Hybrid L3 path is the owner's common case. If most sessions are
  Standalone L2, the efficiency verdict softens to neutral. Only the owner knows.
