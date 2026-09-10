---
description: F-048 - the capability dimension gets an owner. A capability floor no review gate may start below (with the independence-vs-capability arbitration), the delegation boundary written down, and the REVIEW_LOG core schema widened with `model` so both policies become falsifiable.
status: COMPLETED
end_date: 2026-09-10
feature: F-048
id: F-048
start_date: 2026-09-10
level: L3
branch: main
---
# ANALYSIS: Capability Tiers and the Delegation Boundary (F-048)

**Level: L3 · router: no match** (catalogue: `GUIDE_release.md` only, applicable at release).
Elicitation: skip path — the spec is the owner-approved assessment of 2026-09-10 (gaps 1, 2, 4 here; gap 3, the operational search-delegation trigger, deferred). Probes: `harness_capability_tiers/probe.py`, shipped with this analysis.

## Precedent placement (the admission test, run first)

Two capabilities are proposed; both are placed against `vision/rulings.md`.

- **The capability floor** — MISSING. Nearest sibling is **r18** (a mandated stop at a gate when the only independent rung is permission-gated). Distinction line, falsifiable: *r18 governs whether an available rung may be USED (permission); this governs whether a usable rung is CAPABLE ENOUGH for the judgement that gate makes.* A client can satisfy r18 and still run a design review with a model that cannot do it. → new row, ADMIT, pending the owner's ceremony acceptance below.
- **The delegation boundary** — near-miss on **r3** (REJECT: *tells an agent or user what to work on next, in what order, or by whom*), disclosed here because r8 resolves omission against the proposal. Distinction line: *r3 forbids a surface that orders or assigns work; the boundary orders nothing, schedules nothing and assigns to no one — it classifies a pass the agent has ALREADY decided to run, by whether that pass's output is falsifiable.* No queue, no ordering, no "next". → new row, ADMIT.
- Ledger hygiene noted, not touched: `rulings.md` already carries **two rows numbered r19** (the per-turn reminder ADMIT and the subagent-offer REJECT). The ledger only grows and rows are never renumbered without an owner ruling, so this unit takes the next free ids and surfaces the collision rather than repairing it.

## Ceremony budget (the Non-Goal that bites)

The "no ceremony ratchet" Non-Goal admits a new mandatory field at L2/L3 only if the same change removes one of comparable cost, **or** the cost is disclosed and the owner accepts it explicitly. Nothing of comparable cost is removed, so this is the disclosure, in the form r16/r17/r18/r19 used:

| What is added | Who pays it, when | Size |
|---|---|---|
| `model` cell in each `REVIEW_LOG` row | the agent already writing that row, at closure | one cell, no read, no new step; the row exists today |
| the floor (in `review.md`) | only an agent invoking a review gate — a decision point it is already standing at | ~8 lines read, no added step |
| the boundary (in `dispatch.md`) | only an agent considering delegation — likewise | ~15 lines read, no added step |
| **L1** | — | zero |
| **L2** | only if the optional closure review runs | one cell |

No check is added, no exit code moves, no artifact becomes newly mandatory. **This unit does not proceed to the `model` column until the owner accepts that cost explicitly**; the floor and the boundary add no field and are not gated on it.

## Objective

Give the model-capability dimension an owner in Standalone. Today `dispatch.md` tiers implementer subagents (economy, deep after two `verify_result: fail`) and `review.md` asks only for "a different model from the author's": nothing states which roles may never start cheap, nothing states what may leave the authoring context at all, and the log cannot record what ran.

## Feature Vision

No multi-milestone feature vision: this is one unit, closed here. The durable
statement it leaves behind is the pair of ledger rows r20/r21 and the ADR, which
are where a later unit reads what was decided and why.

## Vision Alignment

The skill exists to prevent myopia. A gate run below the capability its judgement needs produces exactly that **while reporting as an independent review** — worse than no gate, because it certifies. This is therefore a correctness fix on the gate the method rests on, and only secondarily an efficiency enabler. Non-Goals run: the ceremony ratchet (disclosed above, owner acceptance pending), r3's work-management territory (distinction line above), and no provider name enters shared doctrine (a name would rot at the next model release and is probed, P1d).

## Use Cases / User Needs

- **UC1 — the agent invoking a review gate.** After: the floor names the minimum capability for that role, so "the gate ran" and "the gate could do its job" stop being one claim.
- **UC2 — the orchestrator deciding whether to delegate a pass.** After: three classes and a mechanical criterion, so the expensive mistake (delegating authoring) has to be argued against rather than happening by default.
- **UC3 — the owner reading the review log to ask whether the policy pays.** After: `model` makes the correlation with `revise_rounds` and `findings_real` visible instead of assumed.
- **UC4 — the agent whose best independent rung is below the floor** (single-model client, or a subagent facility bound to a cheap model in its agent definition). After: the arbitration below decides, and the row discloses what ran.

Product-name buckets — EXISTS: `dispatch.md` §Model tiers, `review.md` independence ladder + its "different model" line, `REVIEW_LOG` core schema (`review.md:91`, `templates.md` ×3), `plan brief` (pointers, never pasted content), `review_logged` header-based `tier` lookup, the shared-spine drift guard, r18's gated-rung stop. NEW: the floor + its arbitration, the boundary section, the `model` column. METAPHOR: none.

## Functional Spec

1. **The floor** (in `review.md`, which owns the gates it binds): a role→minimum-tier table, tiers named as client-relative capability levels, never provider names. A tier may be lowered only where a **threshold signal** exists to catch a wrong cheap answer — `task.verify`, a test, a diff against a spec — which is why implementer dispatch may start economy and a judgement gate may not.
2. **The arbitration (UC4), which is the unit's central rule**: when independence and capability conflict, **independence wins** — a below-floor independent reviewer still catches the class the author is structurally blind to, while a self-pass catches none of it. The row then records the sub-floor tier, and that disclosure IS the remedy. Where a higher-capability path exists but is permission-gated, r18 already governs: one question per gate, per intact context. Legal `model` values: `deep`, `light`, `economy`, `single (client exposes no choice)`, `below floor: <reason>`.
3. **`REVIEW_LOG` core widened with `model`** (gated on the owner's acceptance): `| date | doc_key | tier | model | … |`. The **core** is the columns both modes actually share — `date`, `doc_key`, `tier`, `model`, `findings_raised`, `findings_real`, `verdict`, `revise_rounds` — with `reviewer` (Standalone) and `instrument`/`notes` (Hybrid) named as mode-specific realization columns. This replaces the current claim of one identical column list, which the two modes never had. The column mechanics (readers locate columns by header; extras and reordering are fine) are **cited from `templates.md`, which already owns that fact**, never restated.
4. **The boundary** (in `dispatch.md`): three classes keyed on falsifiability and compression, a never-delegate list, and the delegability condition — *a task whose brief cannot be expressed as pointers is not delegable*, because a brief that must carry the content pays the tokens twice. Declared residual, stated so silence is not read as prohibition: the classification is settled; **when** to reach for a delegated search/orientation pass is the deferred unit.
5. Non-changes: no new check, no command, no exit code, no validator logic. `tier` stays at index 2 because `model` is inserted after it, so even the no-header fallback is unaffected.

## Interface Contract

Trigger fired, narrowly: `REVIEW_LOG.md` is a surface UC3's actor (the owner) reads. The contract: the table gains one column between `tier` and `reviewer`; every row the agent writes fills it from the legal value set above; historical rows keep their meaning and are not rewritten (a mixed log is legal, probed P3c). The owner's read gains one question it could not ask before — *which capability produced these rounds* — and loses nothing: no column is removed, renamed or reordered. No other surface changes.

## Capability Ledger

All capabilities EXIST — nothing is built. Anchors: tier vocabulary `dispatch.md:46-52`; gate model guidance `review.md:83`; core schema `review.md:91` + `templates.md:508` (code) / `:448` (kb) / `:505` (mkt); "one schema" prose also at `templates.md:501-503`; column-by-header mechanics already owned at `templates.md:523-524`; the lookup itself `sdlc_core.py:1055-1071`, pinned tolerant of extra columns at `test_skill_invariants.py:750-758`; brief-as-pointers `dispatch.md:26-28`; spine membership `shared_files.py:37-58` vs `:79-83`; r18 `rulings.md:47`. The pass is one line: this unit writes doctrine into files that already own these concepts and widens a table that already exists.

## Impact

| Path | Change | What |
|---|---|---|
| `review.md` **(spine)** | MODIFY | **owns the floor**: the table, the threshold-signal criterion, the arbitration, the single-model fail-open; the schema line gains `model`; the "one schema" sentence becomes core-plus-mode-specific, citing `templates.md` for the column mechanics |
| `dispatch.md` **(spine)** | MODIFY | §Model tiers cites the floor for the implementer case; new section **What may be delegated at all** (classes, never-list, pointers condition, residual) |
| kb + mkt copies of both | MODIFY | byte-identical port; `shared_files.py --update` ×3 |
| `SKILL.md` ×3 **(per-lens)** | MODIFY | the pointer to `dispatch.md` stops describing it as opt-in dispatch only, so a reader who runs no dispatch still reaches the boundary |
| `templates.md` ×3 **(per-lens)** | MODIFY | schema line + `model` column meaning (and the `tier` vs `model` disambiguation: `tier` = which gate ran, `model` = what capability ran it, since Hybrid `tier` also uses `deep`/`light`); the "one schema" prose at `:501-503`; example row gains a value |
| `test_skill_invariants.py` **(shared battery)** | MODIFY | pin the floor, the arbitration, the boundary, and the `model` column in **each lens's own** `templates.md` (the battery reads its own tree — there is no cross-distribution read); extend the `review_logged` fixture to the widened schema plus one un-widened historical row |
| `vision/rulings.md` | MODIFY | the two ADMIT rows from the placement above, with their distinction lines and the owner's acceptance date |
| `harness_capability_tiers/probe.py` | ADD | P1-P5 |
| **closure artifacts (registration + generated)** | ADD/MODIFY | `architecture/ADR_2026-09-10_…md`, `audit/HANDOFF_capability_tiers.md`, the two `REVIEW_LOG` rows, and the generator output `audit/handoff.md`, `strategic/features_history.md`, `INDEX.md` — named here so the conformance set is complete by construction rather than by the Action Plan alone |

Blast radius: the schema has exactly one machine consumer, `review_logged` (`grep review_log_rel` → `sdlc_core.py` and the batteries only); it locates `tier` by header and falls back to index 2 without one, and `model` goes after `tier`, so both paths are unaffected — the tolerance is already a pinned invariant. `ENFORCEMENT.md` and the READMEs state no schema (zero hits). `CHANGELOG` and `SHADOW_*` files are immutable history, excluded by design.

## Security and Threat Model

No input parsing, no new execution path, no file newly read or written by any script. One surface considered: `model` records a capability tier, and the doctrine forbids provider names in its own text, so the column cannot become where infrastructure detail leaks into a shared artifact — a project may still write its own names in its own log, which is its choice, not the doctrine's instruction. Residual: none.

## Action Plan

1. Harness RED (recorded), then strengthen it per the review: at least one non-tautological assertion per policy.
2. Author the floor (`review.md`) and the boundary (`dispatch.md`), code lens.
3. Owner's ceremony acceptance → then the `model` column in `review.md` + the three `templates.md` + the three `SKILL.md` pointers.
4. Port the two spine files ×2; `shared_files.py --update` ×3. Battery pins.
5. Harness GREEN; batteries code/kb/mkt; drift guard.
6. Scoped re-review, then closure review on the diff.
7. Closure: `rulings.md` rows, ADR, REVIEW_LOG rows **written in the new schema** (the unit's first use of its own field), registration, indexes. Release deferred to the owner.

## Test Strategy

Harness P1-P5. Honest about what each buys: **P2a** (one schema string across four files — a missed port reddens it), **P1d** (a negative invariant nobody satisfies by typing), **P3** (executable against `review_logged`, with a working negation control and a mixed old/new-row case), **P5** (byte identity across distributions) are real constraints; the wording anchors **P1a-c, P2b, P4a-c** are spelling pins that go green when the text is written, and are labelled as such rather than presented as evidence. Four added assertions carry real force; the instrument each lives in is named, because "both" was itself an overstatement the final round caught. In BOTH harness and battery: the floor's declared value set is **parsed whole** — values carrying a tail (`single (client exposes no choice)`, `below floor: <reason>`) are matched and compared on their key, the defect the closure review caught in the first cut; the per-lens `templates.md` must document every value the spine declares (P2e); and the floor must be a **parseable table of at least two role→tier rows** (P2f), never prose. Harness only, and necessarily so: every `model` value in this repo's real `REVIEW_LOG` must belong to the declared set (P2d) — a shipped battery cannot reach into a consuming project's log, so this one can only live where the corpus is. Battery only: the boundary's never-list must enumerate at least four items and name the governed-artifact authoring case, so the boundary cannot degrade into advice. Shared battery keeps its existing `review_logged` assertions. Full `unittest discover` in all three distributions — the siblings' green is the confinement proof.

## Diary

- **2026-09-10 (closure) — PASS at the final round, three reviews spent.** Design FAIL → FAIL → PASS (3 rounds), closure FAIL → PASS (2), sharing one final scoped round. The keeper, and the reason this unit believes its own evidence: **the defect was in the falsifiability instrument itself** — the value-set regex demanded a closing backtick right after the word, so it silently dropped the two legal values that carry a tail (`single (client exposes no choice)`, `below floor: <reason>`); the probe would have reddened on legal log content while the coverage check under-covered, and the template's own example row used one of the dropped values. Caught by execution, not reading; the final reviewer re-derived the value list rather than inspecting the fix, and ran two negative controls. Second keeper: the example row taught the exact axis confusion the floor exists to separate (a declared self-pass is an *independence* deficit, and its capability may well be `deep`), which no probe could have caught because the value was in the declared set. Batteries 193/378/211 OK, harness 17/17, `check --hybrid` CLEAN, spine byte-identical ×3.
- **2026-09-10 — opened; design review R1 FAIL, folded by rewrite.** Driver: the owner's "how does the skill stand against the research", answered with four gaps; this unit takes 1, 2, 4. External evidence: cascade routing pays only where a threshold signal exists (FrugalGPT, RouteLLM) — the floor's criterion; multi-agent costs 3-15× tokens and buys context hygiene, not savings — why the boundary is framed on falsifiability, not cost. R1 (4 BLOCK, 8 WARN) changed the design in four load-bearing ways: the ceremony Non-Goal and the precedent placement were never run (now the first two sections); the floor moved from `dispatch.md` to `review.md` because all three `SKILL.md` surface `dispatch.md` as opt-in-L3-only, so the readers who most need the floor would never arrive; the independence-vs-capability conflict had no arbitration and is in fact the unit's central rule; and "one schema, extras legal" was false — the Hybrid row has no `reviewer` column, so the core is the intersection, not the Standalone set.
