---
description: F-053 - the five defects a cross-lens review run on a DIFFERENT model found after six units shipped, each reviewed in isolation by the same model family as its author. Four are correctness (an unpaid re-review debt, a human-approval rule missing from one package, a rule that reached one lens of three, a report printing an inverted claim); one is a probe that rots by construction.
status: COMPLETED
feature: F-053
id: F-053
start_date: 2026-09-11
end_date: 2026-09-11
level: L3
branch: main
---
# ANALYSIS: The Cross-Unit Remediation (F-053)

**Level: L3 · router: no match** (catalogue: `GUIDE_release.md` only, and this
unit cuts no release). Elicitation: skip path — the spec is
`audit/HANDOFF_cross_unit_remediation.md`, written from a cross-lens review run
on a different model, plus that same model's second pass over the remediation
plan itself. Probes: `harness_cross_unit_remediation/probe.py`.

## Precedent placement

**r14 — the bounded maintenance exemption** ("fixes a defect with purpose,
actors and surface unchanged"). Every item repairs something the family already
decided to have: the scoped re-review is a rule shipped 2026-08-06 and not
executed; the human-approval guarantee is an old family rule absent from one
package; the authoring pointer is **r23's own capability**, admitted family-wide
on 2026-09-11 and implemented in one lens; the report is r22's tool printing a
false sentence. No new question is answered, so no new row — the placement is
recorded here and in r14's `source` cell (the ledger has `id | capability |
verdict | deciding line | source | basis`; it has no Diary column, and the first
draft named one that does not exist).

The one item that is *not* a defect fix is **5b**: **the `moved-block-sha256`
stamps stay through the release that carries the move.** Dropping them now would
remove the only guard on the moved content *before* it ships, and removing them
is not a doc edit — it means editing the shared battery in three lenses and
`shared_manifest.json`. Drop trigger, on the record: once the first release after
`v1.32.1` carrying `hybrid.md` in the code and mkt tarballs has shipped, git
history carries the move and the stamp proves nothing history does not. That is a
decision, not a capability.

## Ceremony budget

Two items grow a mandatory contract, and the growth is disclosed rather than
absorbed:

Ruler: `st_size` on this checkout — the one `benefit` prints. The LF blob gives
different figures, and two rulers in one document is itself a finding (F-051's
WARN-1, which this unit also repairs; see item 7).

| Item | Lens | Added | Contract before | Cost |
|---|---|---|---|---|
| 3 — authoring pointer | kb | 546 B | 28,951 B | +1.9% |
| 3 — authoring pointer | mkt | 548 B | 21,214 B | +2.6% |
| 2 — approval rule | kb | 262 B | 28,951 B | +0.9% |
| **kb total** | kb | **808 B** | 28,951 B | **+2.8%** |

Measured after the last edit, not estimated before it: the first cut of this
table guessed "~180 B" for the approval rule and 546 for mkt's carrier, and the
closure review measured 262 and 548. A disclosure table that rounds in its own
favour is the same defect as item 7, inside the document that discloses it.

(It is not one paragraph in three copies: the code lens's is 518 B after this
unit trimmed its parenthetical, kb's 540 and mkt's 544, because each names that
lens's own artifacts. With blank lines and line endings the carrier grows 546 in
kb and 548 in mkt. The code lens measured 45,279 → 45,825 when F-049 added it,
and 45,825 → 45,801 when this unit trimmed it.)

**What r23 did and did not buy.** r23 priced *one conditional disclosure at L3
authoring, no new field*, and `ANALYSIS_authoring_floor.md` scoped its carrier to
"`SKILL.md` (code lens)". The rule is family-wide — it lives in the shared
`review.md` — but the **bytes of its per-lens carrier were priced nowhere**. So
this table is the first statement of that cost, and item 3's basis is not r23 but
the owner's explicit port confirmation of 2026-09-11, given after being shown
that porting lands the paragraph in two more contracts. Recorded here, in the
Diary, and in the ledger's `source` cell. Item 2 is r14 maintenance: a rule the
other two packages already carry.

**Who pays.** No *act* is added at L1 or L2 — the disclosure fires only at L3
authoring. But `SKILL.md` is read every session, so **every level pays the bytes
above**, and the Vision's budget counts read cost explicitly. "L1 and L2 pay
zero" would have been false (design review R1, F8).

## Objective

Six units (F-047…F-052) shipped in one session. Each was reviewed in isolation,
and each by the same model family as its author. A seventh review, run on a
**different model**, asked what no per-unit review can ask — does the sequence,
taken together, leave the product less correct or more expensive? — and found
five defects none of the six could see. This unit closes them, and closes them
*before* the release that would make four of the five permanent.

The largest is not on the original list. It surfaced when the same external
model was asked to review the remediation plan: **the second review round the
doctrine mandates was never run** for the three most recent units. `review.md`
§Review-driven corrections says a fix made in response to a finding is new,
unreviewed work, that a review carrying findings is provisional until its
corrections pass a scoped round, and that the verdict cell must carry both
verdicts (`FAIL → PASS`). Seven unreleased rows read `FAIL, all findings folded`
or `PASS in 1 round` with `revise_rounds = 1`. The shipped text of those units is
the one version nobody reviewed — which is the exact failure the rule names, in
the doctrine those units themselves ship.

## What the overdue round added (items 6-9)

Item 1's round was run before implementation, on a different model, and it found
what a late round is actually for: defects in the **corrections** themselves.
Four enter this unit's scope by the FAIL branch below.

6. **A shipped probe that cannot fail (BLOCK).**
   `harness_mkt_read_diet/probe.py:65` asserts
   `second source of truth|ownership` *after* the filename — and mkt's own
   content-inventory sentence, which sits after the filename, contains
   "ownership". Deleting mkt's entire consequence paragraph leaves the harness
   green. This is the exact defect F-051's review raised as a BLOCK,
   re-introduced in the next unit's probe with a comment claiming the opposite.
7. **Figures that reproduce under no ruler.** `ANALYSIS_mkt_read_diet.md:41-42`
   and `HANDOFF_mkt_read_diet.md:20-21` say 21,215 B and 3,438 B (Hybrid 24,653,
   +6.6%); measured: 21,214 and 3,532 — the 94-byte stamp line that B3's own
   correction added is missing from the figure that correction produced, so the
   real Hybrid read is 24,746 B (+7.0%) on the `st_size` ruler, or 24,527 B (+7.2%) on the git blob, which is the ruler the corrected document declares. `ANALYSIS_mandatory_read_diet.md:18`
   carries 49,645 (LF blob) beside `:55`'s 50,001 (`st_size`) — the two-ruler
   WARN fixed in the probe and not in the document — and its 6,657 B for
   `hybrid.md` reproduces under neither (6,579 at `b14f266`, 6,646 at HEAD).
   `ANALYSIS_mkt_read_diet.md:106` promises mkt README surfaces that do not
   exist.
8. **Two citations that resolve to the wrong thing.** kb's
   `ENFORCEMENT.md:105` points at a `SKILL.md` section whose 263-byte body holds
   no shadow discipline — the dangling citation F-052 retired textually now
   dangles semantically. And `templates.md` (×3) documents the `reviewer` cell
   without saying it now carries the authoring-floor disclosure that
   `review.md` routes into it.
9. **The benefit harness decodes without an encoding.**
   `harness_benefit_report/probe.py:57` uses `text=True` with no `encoding=`,
   contradicting decision 3 of `ADR_2026-09-11_conservation_reference.md` — the
   ADR written *because* that exact omission corrupted a shipped file. It is
   rewritten wholesale by item 5 anyway.

**What the round could NOT do.** 35 WARN-class findings across six rows have no
per-finding record anywhere in the repo — only aggregate counts. No late round
can certify convergence on them, and the verdict cells say so rather than
implying otherwise. One row (F-052's closure) cannot honestly read PASS at all.

## Vision Alignment

North star: divergence visible before implementation, and before merge. Every
item serves it, and two serve it against this project's own conduct:

- **Goal 3** (the process's central claim is computable, r22): a report that
  prints an inverted directional claim and excludes 46 of 117 rows makes the
  claim *less* computable than silence would, because a false statement is
  quotable. Fixed by replacing the direction with a computed interval.
- **Goal 4** (the cost term is printed beside the benefit): the read-cost line
  prints the term that fell and lumps the term that grew. Fixed by printing the
  total, which neither half can be quoted without.
- **The anti-myopia north star, turned inward**: six reviews by one model family
  with six "all findings folded" rows are one loop, not two eyes. This unit's own
  gates run on a different model.

Non-Goals run. **No ceremony ratchet**: disclosed in full above; nothing becomes
mandatory that r23 and r14 do not already cover. **One triage authority**:
nothing classifies work. **No provider name in shared doctrine**: the tier
vocabulary is untouched; the model diversity is a property of how this unit is
*run*, recorded in `REVIEW_LOG`'s existing cells, not a new rule. **r3's
work-management territory**: the report gains an interval and a total, still
carries no verdict, still names no work item, still exits 0.

## Use Cases / User Needs

- **UC1 — the reader of `REVIEW_LOG`.** Today seven unreleased rows record a
  convergence that never happened. After: the round has been run — late, and
  full-text where the finding lists were never recorded — and each row states
  **both verdicts together with that limitation**, so a reader can see how much
  the second round was worth. A row that cannot honestly claim convergence says
  so in the verdict cell instead of borrowing the format of one that can.
- **UC2 — a kb session working in Hybrid.** Today nothing in its package says
  never to auto-accept a devPNT proposal; the guarantee exists in the other two.
  After: the rule is in kb's own contract, in the same words.
- **UC3 — an agent authoring an L3 artifact under the kb or mkt lens.** Today the
  authoring-floor duty is reachable only through `review.md`, loaded at the
  design-review gate — after the artifact exists. After: the pointer is at the
  head of its L3 workflow, where the rule can still change what gets written.
- **UC4 — anyone quoting the 67% figure.** Today they can quote it with a
  sentence claiming it is a floor, which is backwards, and with a cost term that
  omits what grew. After: the figure arrives bounded, beside a total.
- **UC5 — the next session that runs the harnesses.** Today one is red against
  the current tree and rots further on every review anyone logs. After: it pins a
  frozen fixture for ground truth and invariants for the live log.

Grounding (two checks): every product name resolves — `REVIEW_LOG.md`,
`review.md`, `SKILL.md`, `hybrid.md`, `sdlc_core.py`, `benefit`,
`moved-block-sha256`, `harness_benefit_report` all EXIST; `FIXTURE`/`invariants`
in the benefit harness are NEW and declared. Every use case traces to a Goal
above.

## Functional Spec

Trigger fired: `benefit`'s observable output changes.

1. **The interval replaces the direction.** When parsed rows exist whose `tier`
   does not state a moment AND those rows carry countable findings, the report
   prints the headline share and, beside it, the interval those findings admit:

   - lower = design / (stated + unstated) — every unstated finding was closure;
   - upper = (design + unstated − unstated_code) / (stated + unstated) — every
     unstated finding was design **except the `code` rows**, which are
     post-implementation *by definition* (they are the closure gate).

   The deleted sentence had that fact right and only its direction wrong;
   discarding the fact with the direction would loosen the upper bound from
   70.7% to 72.2% for nothing (design review R1, F6a). No direction is printed,
   because the unstated set pushes both ways — `code` rows lower the share,
   Hybrid `deep`/`light` rows raise it.
2. **The rows outside both bounds are named.** Seven unstated rows state no
   findings count (`all`, `VOID -- instrument error`). They are neither zero nor
   countable, so they sit outside the interval entirely and the report says so:
   unsaid, the band reads narrower than honesty allows — the silently shrunken
   denominator `parse_review_log`'s own comment forbids.
3. **Absence, in both directions.** The interval is absent when no row's moment
   is unstated, AND when unstated rows exist but carry no countable findings:
   the uncertainty set is the findings, not the rows.

   *Format, because the harness enforces it:* the band is printed as whole
   percentages (`56%-71%`, matching the report's existing `%.0f%%` idiom), and
   the uncountable-row sentence leads with its own integer — `7 unstated rows
   state no findings count …` — because a regex reading the first integer on
   that line is the only thing that can compare it to a recomputed value.
4. **The read-cost line prints its total, itemised.** `SKILL.md N bytes (every
   session) + M bytes across K support files (read on trigger) = T bytes total`,
   with `N + M == T`, followed by the support files and their sizes. The total
   alone reveals growth only to a reader holding the previous release's total,
   and a lumped M still hides *which* file grew — which was the original finding
   (design review R1, F7). The sorted glob is already computed. Unchanged when
   `SKILL.md` is absent: the line still prints, saying so.
5. **Acceptance criteria.** The printed interval **equals the one recomputed
   from the log by the harness** — not merely contains the headline, because a
   band the probe does not recompute is a band the report can invent (design
   review R1, mutation M4b-i: a hardcoded `0% to 100%` passed the first cut). It
   is absent in both absence cases; the three cost figures add up; at least three
   support files are itemised; exit code stays 0 in every case, including no log
   at all.
6. **Non-changes**: no new column, no new subcommand, no new flag, no exit code,
   no gate. The parser is untouched.

## Interface Contract

The only actor-facing surface is `benefit`'s stdout, and the actor is a human
reading it (or quoting it). The contract:

| Actor action | Flow | Feedback |
|---|---|---|
| runs `benefit` on a log with unstated-moment rows | parse → classify by moment → sum findings per moment → bound the residue | headline share, then the interval, then the FAIL rate, then the cost line with its total |
| runs `benefit` on a log where every row states its moment | same, residue empty | headline share, **no** interval line, FAIL rate, cost line |
| runs `benefit` with no log | short-circuit | the `[info]` line and the cost line; exit 0 |

The idiom is the one already in place — plain lines, no colour, no table beyond
the existing moment table. A new idiom would be a declared decision; there is
none.

## Capability Ledger

All capabilities EXIST. The log parser and `review_findings` (F-050), the
per-lens contract files, the shared battery and `shared_files.py --update`, the
harness convention, the `REVIEW_LOG` schema with `model`. One line: this unit
adds two sentences of doctrine, one paragraph ported twice, one arithmetic line
and one fixture file; nothing is constructed.

## Impact

| Path | Change | What |
|---|---|---|
| `ai_docs/audit/reviews/REVIEW_LOG.md` | MODIFY | the seven unreleased rows: the scoped re-review's real outcome, both verdicts in the cell, rounds corrected; plus this unit's own rows |
| `SKILL.md` (kb lens) | MODIFY | the never-auto-accept rule in the Hybrid block; the authoring pointer at the head of L3 |
| `SKILL.md` (mkt lens) | MODIFY | the authoring pointer at the head of L3 |
| `SKILL.md` (code lens) | MODIFY | **declared late, at the closure review's insistence**: the pointer's `(cited, never restated)` parenthetical removed (−24 B). The overdue round found that pointer restating three clauses of a rule it claimed only to cite; the two ported pointers carry no such parenthetical, so leaving it would have shipped three pointers making different claims about themselves |
| `scripts/sdlc_core.py` **(spine, port ×3)** | MODIFY | `cmd_benefit`: delete the directional sentence, print the interval; `_print_read_cost`: print the total |
| `scripts/test_skill_invariants.py` **(shared battery, ×3)** | MODIFY | pin the approval rule in EVERY lens (not only lenses with `hybrid.md`); pin the authoring pointer per lens |
| `ai_docs/solutions/harness_benefit_report/probe.py` | MODIFY | ground truth moves to a fixture; live-log checks become invariants; `ground_truth(text)` and `invariants(text)` become importable |
| `ai_docs/solutions/harness_benefit_report/fixture_REVIEW_LOG.md` | ADD | the frozen log the pins describe |
| `harness_cross_unit_remediation/probe.py` | ADD | P1–P7, each labelled by class |
| `ai_docs/audit/HANDOFF_benefit_report.md` | MODIFY | the quoted report output, which contains the deleted sentence and the read-cost line |
| `ai_docs/audit/HANDOFF_mandatory_read_diet.md` | MODIFY | the same quoted read-cost line, plus item 7's re-measured figures |
| `ai_docs/solutions/harness_mkt_read_diet/probe.py` | MODIFY | **item 6**: drop the `ownership` alternative that makes P2c unfailable |
| `ai_docs/solutions/ANALYSIS_mkt_read_diet.md` | MODIFY | item 7: the three stale figures and the README Impact row |
| `ai_docs/solutions/ANALYSIS_mandatory_read_diet.md` | MODIFY | item 7: one ruler, and the `hybrid.md` size re-measured |
| `ai_docs/audit/HANDOFF_mkt_read_diet.md` | MODIFY | item 7: the same figures |
| `ENFORCEMENT.md` (kb lens) | MODIFY | item 8: the citation that resolves to a section without the content |
| `templates.md` **(spine, port ×3)** | MODIFY | item 8: the `reviewer` cell description gains the authoring disclosure |
| `ai_docs/vision/rulings.md` | MODIFY | r14's `source` cell gains this unit; no new row |
| closure artifacts | ADD/MODIFY | ADR (the re-review debt and its mechanism), HANDOFF deletion, `REVIEW_LOG` rows, generated manifests |

**Blast radius** (enumerated by grep across all three distributions, the
harnesses and `ai_docs/`; `__pycache__` excluded):

Anchored to SYMBOLS, not line numbers — the first cut used line refs and they
rotted inside this unit's own edits, against the doctrine's own warning.

- `cmd_benefit` — **two** consumers per lens: the subcommand dispatch in
  `sdlc_core.py` and `test_skill_invariants.test_benefit_reports_and_never_gates`,
  which asserts it returns 0 twice. Both survive the change: the return stays 0.
- `_print_read_cost` — three call sites, all inside `cmd_benefit` itself; no
  external consumer in any lens.
- The `benefit` subcommand registration — `add_parser("benefit", …)` in
  `sdlc_core.py` per lens. Its help text describes no output line, so no edit;
  it belongs in the set.
- The deleted sentence and the read-cost line — the tail of `cmd_benefit` and
  `_print_read_cost` in each of the three lenses, and **two prose consumers outside the code**, both of which
  quote the report verbatim and must travel in the same commit or the repo ships
  a transcript of lines that no longer exist:
  `audit/HANDOFF_benefit_report.md` and `audit/HANDOFF_mandatory_read_diet.md`.
  One test does assert the read-cost line — `harness_benefit_report`'s P6
  requires `Read cost` to be present — and the reformat keeps that word, so it
  survives; the first draft's "no test asserts either line" was simply false.
- `SKILL.md` has machine consumers beyond the battery, and the first draft said
  it had none: `harness_mkt_read_diet` reads kb's and pins mkt's
  `st_size < BYTES_BEFORE` (item 3 spends 548 of a 1,906-byte margin), and
  `harness_mandatory_read_diet` pins the code lens's anchors and size. All
  survive the change; P7 re-runs them.
- `sdlc_core.py` and `test_skill_invariants.py` are shared spine: three copies
  each, plus `shared_files.py --update` ×3, with `test_drift.py` as the guard
  that catches a partial port. The battery pins this unit adds are themselves
  new machine consumers of `SKILL.md`, by design.

## Security and Threat Model

No new execution path, no new input parsing, no network, no filesystem write.
Two surfaces move slightly:

- **T1 — the fixture becomes a trusted input.** `harness_benefit_report` will
  read a file in the repo instead of the live log. Both are repo-controlled text
  and neither is executed; the parser is the same one already hardened against
  malformed rows (F-050's P2e/P2f). Residual: a fixture edited to match a broken
  parser would hide a regression — mitigated by the fixture being a *frozen copy
  of real history*, diffable in git, and by `invariants()` still running against
  the live log.
- **T2 — the deleted sentence.** Withdrawing text is the highest-risk edit a
  governed document can make. Population covered by the retired sentence:
  readers who would otherwise take 67% as exact. The substitute covers them
  better — an explicit interval instead of a one-word direction — and keeps the
  fact the sentence got right (`code` rows are post-implementation) in the upper
  bound. It does **not** strictly widen coverage, and the first draft's claim
  that it did was wrong: a reader who takes the band as a bound over *all* rows
  is still uncovered, because seven rows state no findings count and lie outside
  it. FS clause 2 names them for exactly that reason; that is mitigation, not
  elimination.

Eliminated by construction: the report still cannot fail a build (exit 0
unconditional), so no change here can become a gate.

## Action Plan

1. Harness RED — done; the probe's docstring carries the measured baseline, regenerated from a run rather than typed (two earlier cuts stated counts
   that matched neither each other nor reality).
2. Item 1: the **scoped re-review**, run on a different model — done, before any
   code. Its findings are items 6-9 above.
3. Design review — done, three rounds on a different model, all before any
   code: R1 FAIL (a BLOCK cluster: three probes classed real structure passed
   under stubs), R2 FAIL (two more of the same class, introduced by R1's own
   corrections), R3 **PASS at the cap**, with five non-blocking residuals folded
   rather than carried.
4. Item 2: kb's approval rule. Item 3: the pointer ×2, placed BEFORE each lens's
   instruction to write its design document. Battery pins for both, in every lens, skipping
   none.
5. Item 4: `cmd_benefit` interval + named uncountable rows + itemised total;
   port the spine ×3; `shared_files.py --update` ×3.
6. Item 5: the benefit harness's fixture and invariants (item 9 folds in here).
7. Items 6-8: the unfailable probe, the figures, the two citations.
8. `sdlc_check.py index` FIRST, then harness GREEN, three batteries, drift guard,
   all sibling harnesses — the battery asserts the indexes, so running it before
   `index` fails on this unit's own unregistered ANALYSIS (design review R1, F11).
9. Closure review — on a different model, as both gates above were.
10. Closure: r14's `source` cell, ADR, `REVIEW_LOG` rows (the seven remediated
    plus this unit's own), registration, indexes.

**The FAIL branch, and it fired.** A blocker found in already-shipped text does
not become a new workstream: the fix travels in this unit's commit, the file
enters the Impact as declared scope, the affected unit's Diary records it, and
its review row reads `FAIL → FAIL → PASS`. Item 6 is that case.

## Test Strategy

Honest about what each probe buys, because five units in this sequence shipped a
probe that could not fail, and this one then shipped five more of its own.

**The first cut of this harness failed its own test**, and the design review
proved it with mutations: P4b accepted a hardcoded `0% to 100%`, P5b accepted a
fixture that *was* the live log, P5c accepted `invariants = lambda t: (True,"")`,
and P2c/P3c were greps over the battery's source that a bare comment satisfied.
All five are rebuilt; what follows describes the rebuilt version.

**The mechanism, named once.** Three rounds found the same defect three times:
a probe matching the SHAPE of an output instead of recomputing the VALUE. The
harness now states the rule at its head — every probe over a computed output
recomputes and compares; every probe over prose is labelled a wording anchor —
and every probe that compares against the live log carries a positive control on
synthetic data whose answers differ, so a conditional literal equal to today's
figures cannot pass.

**Real structure.** P1a/P1b evaluate the rule as a predicate over the parsed log,
with `revise_rounds >= 2` as the **sole** structural signal and no prose
parsing at all — R2 broke the verdict-word test twice, once with `PASSED after
FAILSAFE check` and once with `FAIL -> FAIL (cannot honestly read PASS)`, a cell
whose entire purpose is to deny convergence — and with `closure (verification)`
rows excluded by name — those are an
author's hand-verification of a reproduced blocker, not a review with corrections
to fold. P4b **recomputes** both bounds from the log and compares them to the
printed integers. P4c asserts `N + M == T`; P4d counts itemised support files.
P4i requires exactly ONE band in the report, because a probe reading only the
first match accepts a decoy printed under another branch (added at the closure
round, so it has no RED baseline reading). P4e/P4f are negation controls in
both absence directions; P4g **recomputes**
the count of uncountable rows and compares it to the printed integer — the R2
cut merely matched a sentence of the right shape, which a literal with the
wrong number satisfied. P5b proves the fixture is not the live log, that `ground_truth` reads its
argument (by calling it on a synthetic log whose answer is known — R2 showed the
previous cut inferred this from two real logs and got it wrong in both
directions), and that the pins are integer literals rather than values derived
at import. P5c drives the invariants to False on a log carrying a row the parser
cannot read; `parsed + unparsed == table rows` closes even then, so that
invariant is necessary and not sufficient. P2c/P3c **run** the named battery
test in each lens, fail on a skip or an absence, and then **strip the rule from
a copied lens and require the test to go red** — because R2 showed an empty test
body passes a run-only check. P3b compares positions against a per-lens anchor: the pointer must precede the
instruction named in `FIRST_AUTHORING` — write the ANALYSIS, draft the
MKT-VISION — because appending it at the end of the file satisfies presence
while defeating the load order it exists for. Stated narrowly on purpose: it is
NOT a proof that nothing authorial precedes the pointer. The code lens's
Phase-3 preamble does, and kb's bootstrap bullet does; what the probe pins is
that the pointer precedes the instruction to write the unit's own design
document. P6
is byte identity; P7 runs three sibling harnesses.

**Wording anchors, labelled as such in the file.** P2a, P2b, P3a, P4a. They catch
deletion and drift, not meaning: a kb Hybrid block naming `auto-accept` while
negating the duty stays green.

**Not claimed.** That the late re-review of item 1 is as good as one run at the
time — 35 WARN-class findings have no surviving record, and no probe can fix
that; the verdict cells carry the limitation. That `P1a`'s release cutoff is
tamper-proof: it reads the newest git tag and falls back to a pinned date in a
`git archive` copy, printing which it used. And that `SHIPPED_BACKLOG_CAP` is
anything but a ratchet over history — it is measured, not argued.

## Diary

- **2026-09-11 — opened.** Driver: a cross-lens review on a different model,
  then that model's second pass over the remediation plan, which reversed the
  plan's own leaning on item 3 and found the re-review debt the plan had missed.
  The reversal is the evidence for the structural finding: the argument that the
  authoring pointer is "near-inert" was made in the same model family that wrote
  the rule, and fell to one fact from outside it — the reviewer agent definitions
  this repo ships bind `model: opus` and `model: sonnet` by name, so a session
  *can* map itself to a tier, which is exactly the premise the deletion argument
  denied — though the bindings live in `~/.claude/agents/devpnt-*.md`, deployed
  by devPNT, not in anything this repository ships; the first draft got that
  provenance wrong while the substantive point held.
- **2026-09-11 — design review R1: FAIL, folded.** One BLOCK cluster and eleven
  WARNs, from a review that mutation-tested all 17 probes in a scratch copy. The
  cluster is the unit's own subject matter turned on itself: three probes this
  ANALYSIS classed as "real structure" passed under stubs — a hardcoded band, a
  fixture that was the live log, a constant-true invariant. Also measured wrong:
  the shipped backlog is 6, not the 9 typed into the harness. The folds rebuilt
  five probes, added four, corrected the ceremony basis from r23 to the owner's
  own port confirmation, and added the three blast-radius consumers the map had
  missed.
- **2026-09-11 — item 1 run, before any code, on a different model.** The overdue
  round found what a late round is for: four defects in the *corrections*
  (items 6-9), including a shipped probe that cannot fail — the same defect class
  F-051's review had already blocked once, re-introduced in the next unit. It
  also established the limit of the exercise: 35 WARN-class findings across six
  rows have no surviving per-finding record, and one row cannot honestly read
  PASS. That is written into the verdict cells rather than around them.
- **2026-09-11 — design review R2 (scoped): FAIL, folded; round 3 is the cap.**
  Two blockers, both introduced by R1's own corrections, and both the same
  mechanism a third time: a probe satisfiable by a literal. P5b inferred "reads
  its argument" from two real logs and so missed the stub on a fresh freeze
  while flagging an honest harness after this unit's own log edits; P4g accepted
  any sentence of the right shape regardless of the number in it. The fold
  stopped patching cases and wrote the rule at the head of the harness: every
  probe over a computed output recomputes the expected value and compares, every
  probe over prose is labelled a wording anchor. `unconverged()` lost its
  verdict-word test entirely — a cell is prose, a round count is a number.
- **2026-09-11 — design review R3 (scoped): PASS at the cap.** Both R2 blockers
  closed under re-run mutation: the arg-reading control now calls
  `ground_truth` on synthetic logs with known answers, and the uncountable-row
  count is extracted and compared. The round left five non-blocking residuals,
  all of the same family — a single known answer is satisfied by a constant, a
  partial lens copy makes every missing file a confound, and a probe that only
  ever reads the live log accepts a literal equal to today's figures. All five
  are folded, not carried: the harness gained a second synthetic answer, a
  whole-lens copy, and P4h, a positive control whose expected band (40%-70%) and
  count (1) differ from the live log's (56%-71%, 7). The shipped backlog moved
  from 6 to 8 when the predicate lost its verdict-word test: two rows claiming
  `FAIL → PASS` with one round are now counted, correctly.
- **2026-09-11 — closure review R1: FAIL, folded.** One BLOCK, and it was this
  unit's own subject matter turned on it a fourth time: the corrected `benefit`
  transcripts in two handoffs reproduced under no run — one splicing F-053's new
  lines into F-050's old headline numbers beneath a footnote asserting the
  opposite, both quoting a read cost 222 bytes stale because the `templates.md`
  edit came after the capture. Item 7 exists to remove exactly that. The fix is
  not a fresher paste, which goes stale at the next logged review: the quote now
  states that it IS a dated capture whose figures move. Also folded: an
  `invariant` written `1 if x else 1`, a `lens_copy` that blew Windows MAX_PATH
  and crashed instead of reporting, an understated ceremony table, an undeclared
  edit to the code lens, and a claim about the pointer's position wider than the
  probe checks.
- **2026-09-11 — closure review R2 (scoped): FAIL, folded; round 3 is the cap.**
  The WARN-9 correction had put a FALSE ownership claim into a shipped doctrine
  file — kb's `ENFORCEMENT.md` now said the shadow discipline was `review.md`'s,
  and no `review.md` in any lens contains the word. That is item 8's own defect
  class, committed while fixing item 8. And the WARN-4 correction replaced dead
  code with dead code: the parser already refuses a row missing `tier` or
  `findings_real`, so testing their PRESENCE is a tautology; the check now tests
  EMPTINESS, which nothing else does and which silently costs the report a row.
  The most instructive finding was the reviewer's: my first WARN-7 fix reported
  the code lens as SURVIVING a mutation that had never been applied to it — the
  contract is hard-wrapped, the strip was per-line, and it hit `hybrid.md` but
  not `SKILL.md`. A probe that reports a mutation it did not apply is worse than
  one that applies none.
