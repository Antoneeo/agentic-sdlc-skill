---
description: Proposed v9 amendment of project_vision.md Non-Goal 1 - admit a read-only state view (documents' own declared state, derived mechanically, grouped by status in a fixed order) while keeping trackers, boards, assignment, priority, computed state and "what next" out. Owner decision R11 of REQUEST_kb_site.md; two blind rounds PASS-conditional, findings answered; text approved by the owner 2026-10-17 (R12) and applied to project_vision.md and rulings.md.
status: CURRENT
---
# Proposal: Vision v9 — the read-only state view

**Status: approved and applied, 2026-10-17** ([R12](../audit/requests/REQUEST_kb_site.md)). The text below is
now in `vision/project_vision.md`; r2, r9 and r27 are in `vision/rulings.md`; round 12 and
its fixtures are in `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`.

## Decision being proposed

The owner decided to amend the Vision rather than drop the views that show the state of
open work and of features ([REQUEST_kb_site.md#R11](../audit/requests/REQUEST_kb_site.md)).
`## The admission test` requires an amendment to be ruled **as its own proposal, before
and apart from the capability that needs it**, to **stand with that capability
withdrawn**, and Non-Goals to change only by the owner's decision at the Vision. This
document is that proposal; F-072 (the kb site) waits on it.

## Why it stands without F-072

1. **The product already ships what the current text forbids.** `sdlc_check.py index`
   generates `audit/handoff.md` — one row per open workstream with its status, start
   date and its own next step — and `strategic/features_history.md` — one row per
   ANALYSIS with its status and dates. Both collect per-work state into one surface,
   which the current clause ("a view assembled only from fields this rule admits,
   sorting and filtering nothing, is still out") and ruling r2 reject. F-019 admitted the
   registry as "an inventory ordered for lookup"; the Vision's text never caught up. A
   rule the product itself breaks is a rule a motivated reader can cite against it.
2. **Seeing declared state together serves the Goal "keep understanding durable across
   sessions".** A person resuming after a pause, or a team lead keeping several agents
   aligned, needs what each unit says about itself — which are blocked, which in
   progress, what each says comes next — without opening every file. It decides nothing
   for them.
3. **What the Non-Goal exists to keep out is untouched**: trackers, editable boards,
   assignment, sprints, velocity, burndown, priority, and any computed answer to "what
   next, in what order, by whom". The change admits showing **declared** state; it
   admits no **computed** state, no **ordering field** and no **decision**.

## The text

In `## Non-Goals`, first bullet ("Not a work-management system"), replace everything
from "Two consequences, because both have been reached in practice:" to the end of the
bullet with:

> Two consequences, because both have been reached in practice: a guide whose body is a
> procedure for producing that answer is out, being an instruction we ship; and a view
> is judged by what it computes, not by what it collects.
> **One collected form is admitted, the read-only state view** (v9). It gathers the
> state each document declares about itself in its own fields — a workstream's
> registry fields, an analysis's own status, declared level and dates, the next step it
> writes for itself — and shows it grouped by status. It is admitted only while all of
> these hold:
> - **It is derived mechanically from the documents' own fields, each time it is
>   produced.** A file regenerated from those fields by a command we ship, never edited
>   by hand and checked by the validator against its sources (the generated workstream
>   registry is one), is such a derivation. A hand-kept or agent-kept copy of the
>   collection — in a guide, a document or a field — is out; so is a field a tool we
>   ship writes from a computation (that value is computed, whoever stores it).
> - **It computes nothing the documents do not state**: no score, priority, rank,
>   readiness, freshness, age, recommendation, estimate, forecast, count, total,
>   percentage, velocity or burndown. A date is a date a document declares in its own
>   fields, never a file or commit time.
> - **Its order is fixed**: status groups with blocked first and then the lifecycle,
>   and within a group the most recently updated first by the declared date; or the
>   lookup order of the generated manifest. No other order is admitted: no ordering
>   field, declared or computed (`priority`, `rank`, `order`), no other direction, and
>   no status that exists to mark a unit as available or next to take (`next`, `ready`,
>   `up next`): those are priority by another name. Lifecycle statuses (planned, in
>   progress, blocked, paused, completed, cancelled) are not.
> - **It is read-only.** The only action is opening a document to read it, in a viewer
>   or editor. Nothing is edited, acknowledged, claimed or written back from it, and
>   nothing starts work on a unit: a control that launches an agent against a unit
>   starts it, and is out.
> - **It carries no assignment**: no person, agent, team or role as the one who must do
>   it, no assignee or owner field, no due, target or review-by date, no sprint or
>   iteration. A next step is shown verbatim and never parsed, extracted or highlighted;
>   templates and guidance we ship ask for the step only, never for a name, role,
>   urgency or order, and such text in a document is that document's defect, not an
>   admitted feature of the view.
> - **Nothing we ship or instruct tells an agent to choose, prefer, avoid, skip or order
>   units from it.**
>
> What separates this from the tracker that stays out is how units come to exist: a
> unit here is a document the methodology already requires (a workstream's resume
> notes, an analysis), created when the work needs it. A shipped mechanism or template
> whose purpose is to open, number, file or close work items is a tracker, whatever
> view shows them. Everything else this rule names stays out, under any name: a
> tracker, an editable board, assignment, sprints, velocity, burndown, and any output —
> stored or derived, view, field or procedure — whose answer to "what next, in what
> order, by whom" goes beyond showing what the documents themselves declare. In: an
> ANALYSIS whose own frontmatter says `IN_PROGRESS`; the generated manifest, an
> inventory ordered for lookup; a read-only view showing every analysis grouped by its
> declared status. Out: that view with a "ready next" column, an assignee, a due date,
> a priority order, a count per status, an "open only" filter, or a button that
> changes, claims or starts a unit.

The header line becomes "Status: APPROVED (by Antonio Pinto — v6 2026-07-27, v7
amendment 2026-07-31, v8 amendment 2026-08-01, **v9 amendment <date>**)", and
`## Provenance` gains:

> - **v9 — <date of approval>, APPROVED by Antonio Pinto.** Amends Non-Goal 1: admits
>   the read-only state view under six conditions. It advances the Goal "keep
>   understanding durable across sessions" and the team-lead Actor's "one source of
>   truth": what each unit declares about itself is seen together, and nothing is
>   decided for the reader. Owner decision 2026-10-16
>   (`audit/requests/REQUEST_kb_site.md` R11), ruled apart from F-072, which depends on
>   it; it also reconciles the text with the workstream registry (F-019) and feature
>   history the product already generated. Blind round 1 PASS-conditional (four rewords
>   closed); confirming round 2 PASS-conditional (fixed order and direction, declared
>   dates only, generated-file derivation, free-text next step, the launcher, the
>   tracker distinction, r9 reconciled). Disposition:
>   `solutions/PROPOSAL_vision_v9_state_view.md`.

## Precedent ledger (`vision/rulings.md`), on approval

- **r2** — the question is restated, the old wording kept in the row's basis:
  "collects **computed or derived** per-document or per-work state into one surface —
  stored, generated or derived on demand; sorted or not (declared state: r27)" — REJECT;
  deciding line "Non-Goal 1: a view is judged by what it computes". Basis: "v9 restated
  the question; v8 wording: collects per-document or per-work state…".
- **r9** — the question gains a pointer: "outputs the set of documents that are NOT
  current (or any selection by state) (declared-state grouping: r27)" — REJECT,
  unchanged for computed selections and for filters.
- **r27 (new)** — "shows, read-only and derived mechanically from the documents' own
  fields, the state documents declare about themselves, grouped by status in the fixed
  order (blocked first, then lifecycle; most recently updated first by declared date);
  computes, counts, ranks, assigns, sets deadlines, starts and recommends nothing, and
  nothing we ship tells an agent to choose, prefer, avoid, skip or order from it" — **ADMIT**; deciding line: Non-Goal 1, the read-only
  state view (v9); source: the workstream registry (F-019), the feature history; basis:
  owner decision 2026-10-16 (REQUEST_kb_site.md R11).
- Standing fixtures: "lifecycle status + manifest sorted by it" → ADMIT under r27 when
  the conditions hold; "`blocked_by:` + a 'ready' view" stays REJECT (readiness);
  "issue tracker with boards" stays REJECT. New fixtures from round 1: declared
  `priority:` ordering; a hand-kept state table in a guide; `status: NEXT_UP`; "assign to
  X" written in `next:`; grouping by `team:`; oldest-first date queue; a validator that
  writes `ready:`; an "open in agent" launcher; "skip units marked IN_PROGRESS".

## Blind round 1 — findings and disposition

Reviewer: fresh context, a different model from the author, the full candidate text
(Vision and ledger) and nothing else; 21 reject-side and 11 accept-side proposals.
Verdict **PASS-conditional**: no BLOCK; no reject-side proposal through except the
aggregation-board fixture, admitted by design of this amendment.

| Finding | Disposition |
|---|---|
| MAJOR-1 no v9 provenance; status line says "candidate"; justification must be independent | Fixed: provenance entry above, justification §"Why it stands without F-072"; "candidate" was the blind copy's marker only. |
| MAJOR-2 declared `priority`/`rank` not closed | Fixed: "orders by nothing but status and update date", ordering fields and queue-meaning statuses out. |
| MAJOR-3 a hand-kept table passes | Fixed: derived mechanically at view time; stored copies and tool-written computed fields out. |
| MAJOR-4 r2 straddles r27; stale "aggregation clause" pointer | Fixed: r2 restated to computed state, deciding line updated, pointer to r27. A per-topic fact count (a computed count) lands on r2 and is ruled by the owner as r28 in F-072. |
| MAJOR-5 a new triage level cannot be admitted through the amendment rule | Not caused by v9 and outside its scope; recorded here for a separate unit. |
| MAJOR-6 the `stale` command vs r9 | v9 no longer restates the stale example; r9 is unchanged. The pre-existing tension is recorded for a separate unit. |
| MAJOR-7 battery items 4, 9, 13 turn on disclosure | Accepted as designed: disclosure decides them. |
| MINOR-1 r27 omits the agent-pick and due-date bars | Fixed in r27. |
| MINOR-2 counts per column | Fixed: counts and totals out. |
| MINOR-3 two rows with id r19 | Pre-existing; renaming an id edits the ledger's history, so it is left to the owner. |
| MINOR-4 "owner" overloaded | Fixed: the text says "assignee", "person, agent, team or role". |
| MINOR-5 "claimed" undefined for a launcher | Fixed: the only actions are opening and reading. |
| MINOR-6 dense paragraph | Fixed: conditions as a list. |
| Reword: grouping by `team:` | Fixed: "person, agent, team or role". |
| Reword: oldest-first date queue | Fixed: a date chosen to sort a queue is out; the only date order is most recently updated first. |
| Reword: exclusion filter instruction | Fixed: "choose, skip or order". |

## Blind round 2 (confirming) — findings and disposition

Same reviewer set-up on the round-1-fixed text. Verdict **PASS-conditional**: no BLOCK;
priority, rank, ready, counts, tool-written values, shipped instructions all rejected on
explicit text; accept-side B, D, E clean.

| Finding | Disposition |
|---|---|
| MAJOR-1 r9 ("any selection by state") vs r27 — CONTESTED by the ledger rule | Fixed: r9 points to r27 for declared-state grouping, as r2 does; filters stay out (named in the text). |
| MAJOR-2 update date undefined; direction not a condition | Fixed: dates are declared in the documents' own fields, never file or commit times; the order is a condition and fixed in both direction and grouping. |
| MAJOR-3 the generated registry is a stored file | Fixed: a file regenerated by a shipped command, never hand-edited and checked by the validator, is a derivation. |
| MAJOR-4 assignment or priority in the free-text next step | Fixed: shown verbatim, never parsed or highlighted; shipped templates ask for the step only; such text is the document's defect. |
| MAJOR-5 nothing distinguishes a tracker | Fixed: a tracker is a shipped mechanism or template whose purpose is to open, number, file or close work items; units here are documents the methodology already requires. |
| MAJOR-6 "opening" undefined for a launcher | Fixed: opening means reading in a viewer or editor; launching an agent against a unit starts it and is out. |
| MINOR `PLANNED` vs `READY` | Fixed by effect: a status that exists to mark a unit as available or next to take is out; lifecycle statuses are named as admitted. |
| MINOR `target`, `review_by`, `owner` fields | Fixed: named. |
| MINOR "avoid", "prefer" | Fixed: in the last condition. |
| MINOR "dates" in r27 | Fixed: "sets deadlines". |
| MINOR provenance names no Goal or Actor; `<date>` vs pending | Fixed: Goal and Actor named; the date is the approval date, filled on approval. |
| MINOR "size" is computed; STALE by hand vs computed | Fixed: "declared level"; freshness and age named among the things never computed. |
| MINOR (round 1, carried) r2 does not cover hand-kept copies | The prose carries it ("hand-kept or agent-kept copy… is out"); r2 is about computed state and r27 requires mechanical derivation, so a hand-kept copy matches neither ADMIT row. |

## Diary

- **2026-10-16** — Drafted after R11.
- **2026-10-17** — Blind round 1 PASS-conditional, answered. Confirming round 2
  PASS-conditional, answered. Both rounds: no BLOCK, no ledger-class attack through.
  Next: owner approval of the text (or a third round on request).
- **2026-10-17** — Approved by the owner as it stands (R12); applied.
