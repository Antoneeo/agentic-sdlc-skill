---
description: F-050 - `sdlc_check.py benefit`, the standing measure of what the process actually buys. Reads REVIEW_LOG and reports findings caught before code existed against the read-cost of the doctrine, so every future unit is judged on whether it moves the catch rate or only the byte count.
status: COMPLETED
end_date: 2026-09-10
feature: F-050
id: F-050
start_date: 2026-09-10
level: L3
branch: main
---
# ANALYSIS: The Benefit Report (F-050)

**Level: L3 · router: no match** (catalogue: `GUIDE_release.md` only).
Elicitation: skip path — the spec is the owner's directive of 2026-09-10 ("cercare il beneficio finale e raccoglierne il più possibile") plus the one-off analysis that answered it. Probes: `harness_benefit_report/probe.py`.

## Precedent placement

- **Near-miss on r2** (REJECT: *collects per-document or per-work state into one
  surface — stored, generated or derived on demand*), disclosed here because r8
  resolves omission against the proposal. Distinction line, falsifiable: *r2 forbids a
  surface reporting the state of WORK — open items, their readiness, what needs
  attention (its own examples are a readiness board and a coverage distribution).
  `benefit` reports the outcome of CLOSED events — reviews that already happened —
  aggregates no work item, names no document as needing anything, and its output does
  not change when work is added or finished, only when a review is logged.* If the
  owner reads that line as too fine, the correct verdict is CONTESTED and the ruling
  is theirs, not mine.
- **The r15 adjacency is dropped** (it was over-claimed in the first draft): r15 covers
  the product's own *tests*, which carry a verdict, and `benefit` is defined by never
  having one. The procedure does not need it — MISSING against r2 means the prose rules
  once and the verdict becomes a new row.
- **Non-Goal 3's second clause engaged**, since the proposal lands in its territory:
  *"Ceremony relocated from L1 to a higher level, or from a step to a report, is the same
  cost moved — count it."* Counted: nothing was relocated. No step was removed anywhere
  and turned into this report; the report reads a row `review.md` already required. What
  the unit adds is an instruction in `ENFORCEMENT.md` addressed to the owner's admission
  decision, not to the L1/L2/L3 ladder, and `SKILL.md`'s mandatory read is byte-unchanged
  except for one command name.
- Verdict proposed: MISSING against r2 → new row.

## Ceremony budget

**Nothing becomes mandatory.** No new artifact, no new field, no new check, no
addition to any gate; `benefit` is a command run when someone wants the number, and
the data it reads already exists because `review.md` already requires the row. L1, L2
and L3 all pay zero. The "no ceremony ratchet" Non-Goal is therefore satisfied without
needing the owner's acceptance door — the first unit in this sequence of which that is
true, and worth saying out loud.

## Objective

The process has produced 590 verified findings across 63 reviews with a stated moment (of 109 logged) in six
weeks, 68% of them at design review — before any code existed. That number is the
product's central claim and it had never been computed. Meanwhile `SKILL.md`, the one
file every session must read, has grown from 4.8 KB to 50 KB. This unit makes both
sides standing and cheap to recompute, so the question "does this new rule move the
catch rate or only the byte count?" has an answer instead of an opinion.

## Vision Alignment

Two Goals, and the unit exists at their intersection. **"Make divergence from the
declared intent visible before implementation"** is what the design-review share
measures directly. **"Scale process cost to risk … cost includes what the agent must
read, and lowering that price without losing the process is real work"** is what the
byte side measures. Reporting them together is the only way either is actionable: a
catch rate with no cost term justifies unbounded doctrine, and a cost term with no
catch rate justifies deleting the process.

## Use Cases / User Needs

- **UC1 — the owner deciding whether a proposed unit is worth its ceremony.** Today the ceremony budget is disclosed and accepted on judgement alone. After: the disclosure sits beside a measured baseline of what the process currently catches.
- **UC2 — the agent closing a doctrine unit.** After: one command tells it whether the corpus it just added to is catching more, the same, or less.
- **UC3 — the practitioner asked to justify the methodology.** After: a number with its provenance (109 rows logged, 63 with a stated moment, 590 findings on those) instead of an anecdote.

## Functional Spec

`sdlc_check.py benefit [--root <project>]` reads `audit/reviews/REVIEW_LOG.md` and prints:

1. **Coverage, in THREE buckets** — the distinction the unit's honesty rests on, and
   the one the first draft of this spec omitted: rows **parsed**, rows **unparsed**
   (counted and named), and among the parsed, those whose `tier` **states a moment**
   versus those where it carries the Hybrid reviewer weight instead. Cell-level too: a
   `findings_real` cell stating no number (`all`, `VOID — instrument error`) is reported
   as unknown and never summed as zero. A silent drop at either level inflates every
   ratio — the one-off analysis that motivated this unit lost 61 of 63 rows that way.
2. **The catch split**: findings verified at `design` versus `closure`, and the design
   share as a percentage — the Goal-3 number.
3. **Gate yield**: what fraction of reviews FAILed their first round, and findings per
   review by moment.
4. **Read cost**: the byte size of `SKILL.md` and of the top-level support files, so the
   two sides are printed together and neither can be quoted alone.
5. Exit code **always 0**, and no advisory, warning or error is emitted: this is a
   report, never a gate. A number that can fail a build becomes a target.

**Columns are resolved by HEADER NAME, never by width** — `templates.md` promises that
contract ("extra or reordered columns are fine — but the header must say `tier`") and
THREE widths are legal: the original 8, Standalone's 9, and Hybrid's 10 (`instrument` +
`notes`, and no `reviewer` at all). A row whose width differs from the header falls back
to the positional map for its own width, because a log legitimately carries mixed widths;
only a width no map knows is unparsed, and it is counted and named.

## Capability Ledger

All capabilities EXIST: the log and its schema (`review.md`, `templates.md`), the
column-by-header reader (`sdlc_core.review_logged` shows the idiom), the subcommand
dispatch and `--root` resolution in the spine, the three entry points' command lists.
One line: this reads a file the family already writes, with a parser shaped like one
that already exists.

## Impact

| Path | Change | What |
|---|---|---|
| `scripts/sdlc_core.py` **(spine, port ×3)** | MODIFY | header-keyed parser + the report; all three legal widths; unparsed rows AND uncounted findings cells named |
| `scripts/sdlc_check.py` + `mkt_check.py` **(per-lens entry points)** | MODIFY | the docstring command surfaces only — dispatch needs NO change (the spine registers it; verified by running `benefit` from all three lenses unmodified). kb's entry forwards by design and has no command tuple |
| `SKILL.md` ×3 **(per-lens)** | MODIFY | `benefit` on each lens's command surface — the F-029 class this repo has ruled BLOCK before |
| `scripts/shared_manifest.json` ×3 | MODIFY | `shared_files.py --update` after the port |
| `scripts/test_skill_invariants.py` **(shared battery)** | MODIFY | pin: both widths parse, the unparsed count is reported, exit code is 0 on every input including an absent log |
| `ENFORCEMENT.md` ×3 | MODIFY | one line: `benefit` is a report, never a CI gate |
| `vision/rulings.md` | MODIFY | the row from the placement above |
| `harness_benefit_report/probe.py` | ADD | P1-P6 |
| closure artifacts | ADD/MODIFY | ADR, HANDOFF, REVIEW_LOG rows, generated manifests |

Blast radius: a new subcommand adds no consumer to anything existing; the risk is the
opposite direction — the parser must not silently drop rows, which is the defect the
motivating analysis hit, and which P2e/P2f pin by extracting the unparsed COUNT rather than searching for the word (the first cut of that probe matched a dishonest report and could not fail).

## Security and Threat Model

Reads one Markdown file inside the docs root and prints aggregates; writes nothing,
executes nothing, and the docs-root confinement the spine already applies covers the
path. No new surface.

## Action Plan

1. Harness RED against the repo's real log.
2. Implement the parser and report in the spine; register in the three entry points.
3. Battery pins; port ×3; `shared_files.py --update` ×3.
4. Harness GREEN, three batteries, drift guard.
5. Design review, closure review.
6. Closure: rulings row, ADR, REVIEW_LOG rows, registration.

## Test Strategy

The strong assertion, and the reason this unit is testable where the last three were
not: **the report is checked against constants a person updates deliberately** — at the time of
writing 65 rows with a stated moment, 613 findings on those, 414 at design (they were
63/590/402 before this unit logged its own two reviews; `probe.py` dates every change). Stated
precisely, because the first draft called 63 the "parseable" count when it is the
*classified* count. The harness re-derivation is NOT independent of the code (it shares
its assumptions); the constants are what carry the check, plus P5 (a Hybrid 10-column row
parses), P2e/P2f (the unparsed counter reads 1 and 0 when it should) and P6 (the cost line
is never silently absent). A parser that drops
rows fails against that ground truth rather than against its own expectations. Plus:
both row widths parse, an absent log exits 0 with an honest "no data", and a
deliberately malformed row is counted as unparsed rather than skipped. Wording anchors
are labelled as spelling pins.

## Diary

- **2026-09-10 — opened.** Driver: the owner's redirection from measuring a proxy (does an agent avoid one citation error) to measuring the end benefit. Grounding it in the Vision's own Goals produced the first real numbers the project has: 63 reviews, 590 findings, 68% caught before code existed, against a mandatory read cost that went 4.8 KB → 50 KB. The pruning pass on `SKILL.md` is the unit AFTER this one, deliberately: pruning without the instrument would repeat the mistake this sequence just diagnosed.
