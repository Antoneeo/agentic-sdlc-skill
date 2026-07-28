---
id: F-021
feature: Design Review Gate (Standalone)
status: COMPLETED
level: L3
start_date: 2026-07-28
end_date: 2026-07-28
---
# Feature Analysis: Design Review Gate

## Objective

In Standalone the ANALYSIS is reviewed only as an *input* to the closure review —
that is, after the code exists. Nothing independent looks at the design before
implementation starts. In Hybrid that gate exists (devPNT §4.5 on `E-ISP`/`E-TDD`);
Standalone had no equivalent, so the skill's most expensive failure mode — a design
whose omission is discovered by the code that implements it — had no defense.

Close it: at the end of Phase 3, an L3 design goes to an independent reviewer
before any code, per `review.md`.

## Feature Vision

Serves the Vision's **Core Problem** directly ("an agent acts from partial
understanding… breaks what it did not account for") and **Goal 3** — "make
divergence from the declared intent visible *before* implementation, and again
before merge". That goal names two moments; the methodology only implemented the
second one in Standalone.

Evidence this is real, not theoretical: `audit/reviews/REVIEW_LOG.md` records seven
independent reviews run during F-020, **every one of them at closure**, and
`findings_raised == findings_real` on all seven — 72 findings, none rejected as
noise, none caught by the author's own self-review beforehand. The first two rows
were design defects found after the design had already been implemented.

**Ceremony budget (Non-Goal "no ceremony ratchet").** Adds cost at L3, removes
nothing → the rule's second branch: cost stated, owner accepts explicitly. The
first statement of this cost listed three items and the design review found it was
**six** — and the Vision says "Omission resolves against the proposal", so the
acceptance had to be re-obtained against the real number. The cost, in full, all at
L3 only:

1. **One reviewer pass** at the end of Phase 3, capped at 3 rounds.
2. **The `conformance_statement`** the reviewer must produce — every use-case and
   Actor, every threat, every applicable Vision Goal/Non-Goal, each mapped to
   evidence. This is the largest artifact the gate creates. It already existed in
   `review.md` for the Hybrid gates; F-021 is what makes it fire in Standalone,
   which the Vision calls "ceremony relocated… count it".
3. **The reviewer input packet** — the ANALYSIS plus Vision + Actors + use-cases +
   threat model, assembled self-contained for a fresh-context reviewer.
4. **Finding disposition** — every finding answered one by one, fixed or justified
   with evidence. On this feature's own evidence base that averaged ~10 findings
   per review.
5. **One log row** per completed review, PASS or FAIL.
6. **~90 words** added to the always-loaded `SKILL.md` (down from ~180 after the
   review's DRY finding) — the Vision counts what the agent must read as cost.

L1 and L2 are untouched, mechanically (`design_review_due` returns False for any
non-L3). **Accepted by Antonio Pinto, 2026-07-28**, against this complete
statement.

**Ruling against the other binding Non-Goal ("Not a work-management system"):**
`REVIEW_LOG.md` carries `date` and `reviewer`, and "who did it" is an enumerated
key of a record of work. It does not violate, by the Vision's own closed-by-intent
test: the log is append-only history describing what happened *to a document*, it
is never sorted or filtered by how far along anything is, and no key in it answers
"what should be worked on next". Reviewer is provenance for a past event, not an
assignment for a future one.

Non-goals: no second review schema (Hybrid's devPNT gates write to the same file
and the same columns); no gate that can block forever (3 rounds, then the findings
go to the user); no requirement that the client have subagents (a *declared*
self-pass is a legitimate, degraded realization).

## Use Cases / User Needs

- **Solo developer using an AI agent** (Vision `## Actors`) — the design is checked
  by something other than the mind that wrote it, at the point where fixing it is
  still cheap. Good UX = one pass, capped, and it never blocks indefinitely.
- **Team lead needing governance** — `REVIEW_LOG.md` makes "was this reviewed, by
  what, and what did it find" answerable months later, for Standalone projects too.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| Request, receive and perform a review to a stated standard | **EXISTS** | `skills/agentic-sdlc-skill/review.md` | re-read §Requesting/§Receiving/§Reviewing: the conformance-statement machinery for design reviews was already there, written for the Hybrid gates — it needed a Standalone trigger, not a new mechanism |
| Fire a review at the design→implementation boundary (Standalone) | **MISSING** | new §Design review gate (`SKILL.md` Phase 3) + `review.md` §When a review is due | grepped `review` across `SKILL.md`: every hit was Phase 5 or a Hybrid pointer — Phase 3 ended and Phase 4 began with no gate |
| Choose a reviewer with real independence, on any client | **MISSING** | three-rung ladder in `review.md`, client-agnostic, rung + reason declared | the ladder existed only in the devPNT doctrine — Hybrid-only and client-specific, so Standalone had nothing |
| Record that the review happened and what it found | **INADEQUATE** | Write-Triggers row + `templates.md` entry reusing the existing columns, plus a `## Notes` section for the findings | `REVIEW_LOG.md` exists with 40+ rows, all written by devPNT gates: no Standalone trigger, no template, and the table alone answers "was it reviewed" but not "what did it find" |
| Notice a skipped design review mechanically | **MISSING** | `design_review_due()` + `review_logged()` advisory, epoch-gated, suppressed under `--hybrid` | the validator had no notion of reviews at all; grepped `REVIEW` across `sdlc_check.py` before concluding — zero hits |

Contract of the new logic, stated without naming this feature: *`design_review_due(meta)`
answers whether an analysis owes a design-review record; `review_logged(root, name)`
answers whether one exists.* Consumers: `cmd_validate`.

## Impact

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/review.md` | MODIFY | §When a review is due (two moments, the ladder, the cap, the log); design reviews have no diff |
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | Phase 3 gate; Write-Triggers row for `REVIEW_LOG.md`; two ownership-matrix rows |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | `REVIEW_LOG.md` template on the existing schema |
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` | MODIFY | `DESIGN_REVIEW_EPOCH`, `REVIEW_LOG_REL`, `design_review_due()`, `review_logged()`, one advisory |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | MODIFY | `test_design_review_gate_wired` |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | MODIFY | dogfood: the 7 F-020 reviews recorded |
| `package.json`, `gemini-extension.json`, `CHANGELOG.md`, `ai_docs/audit/handoff.md` | MODIFY | release 1.19.0 + closure |

Blast radius: `design_review_due`/`review_logged` are new leaves with one caller
each (`cmd_validate`). No signature changes. `review.md` gains a section; its
existing consumers (Phase 5, `dispatch.md`, the devPNT gates) point at the file, not
at line numbers, so none of them breaks.

## Security and Threat Model

Surfaces: **filesystem** (reading one more Markdown file) and **parsing of
document-supplied text**. No external input, authN/authZ, crypto, network or
personal data.

- **T1 — path handling.** `REVIEW_LOG_REL` is a fixed, hard-coded relative path;
  no document content reaches the filesystem call, so there is no traversal input.
- **T2 — false "you skipped the review".** The worst outcome, since it trains
  readers to ignore the advisory channel. Mitigated by matching the filename
  loosely while reading the moment from the `tier` column, by firing only for
  IN_PROGRESS/COMPLETED (a PLANNED analysis is not late — the review is due at the
  *end* of Phase 3), by the `DESIGN_REVIEW_EPOCH` grandfathering, and — found by
  the design review — by **suppressing it under `--hybrid`**, where devPNT owns
  the slot and its log rows are keyed on `e_isp_`/`e_tdd_` doc_keys that this
  check could never match: a permanent, unfixable false positive on exactly the
  projects the ownership matrix directs away from this gate.
  **Residual, named rather than claimed away:** a deleted or rotated log, and a
  renamed ANALYSIS, both re-raise the advisory with no way to clear it except
  writing a row for a review nobody can now verify. Clear it with an explicit
  `| … | design | (log rotated YYYY-MM-DD) | …` row — honest bookkeeping beats a
  fabricated review. Related limit: `review_logged` is satisfied for the lifetime
  of a filename, so a long-lived ANALYSIS reopened for a later increment owes,
  mechanically, one review. The doctrine covers that case (`review.md` moment 1b,
  `design (late)`); the backstop does not, and is not meant to — it detects the
  never-reviewed design, not every increment of one.
- **T3 — theater.** A logged row proves a row was written, never that a review
  happened. Mitigated only by the `reviewer` column being a declaration and the
  self-pass being explicitly nameable — stated honestly in `review.md` rather than
  claimed away.

## Action Plan

- [x] Elicitation: skipped — the gap and the fix were specified in the exchange
      that requested it, and the ceremony cost was accepted explicitly
- [x] `review.md` — §When a review is due, ladder, cap, log
- [x] `SKILL.md` — Phase 3 gate, Write-Triggers row, ownership matrix
- [x] `templates.md` — REVIEW_LOG on the existing schema
- [x] `sdlc_check.py` — advisory backstop, epoch-gated
- [x] Dogfood: the 7 F-020 reviews logged
- [x] `test_design_review_gate_wired`; battery green
- [x] **Design review of THIS analysis** (the gate applied to itself) — FAIL,
      3 BLOCK + 10 WARN, all dispositioned; logged
- [x] Release 1.19.0

## Test Strategy

Static battery. `test_design_review_gate_wired` asserts: the two moments and the
three-rung ladder are in `review.md`; `SKILL.md` fires the gate in Phase 3 (before
Phase 4, asserted by ordering) and carries the Write-Triggers row; the template
exists on the existing schema; and `design_review_due`/`review_logged` behave —
PLANNED exempt, pre-epoch grandfathered, L2 exempt, a logged design row silences it.

## Diary / Current State

- **2026-07-28** — opened and implemented. Standalone (mode declared per unit of
  change: devPNT is connected to this machine but in use for another project).
  Branch `feat/architect-pass`; 1.19.0 rides on the unpublished 1.18.0.
- **2026-07-28 — the gate run on itself: FAIL, 3 BLOCK + 10 WARN.** It paid for
  itself on its first execution, and every blocker was in the design, not the code:
  1. **The independence ladder had an escape hatch.** Rung 3 (a declared self-pass)
     was selectable at the agent's sole discretion with no duty to say *why* the
     higher rungs were unavailable — so the cheapest path through the gate
     delivered exactly the independence it exists to buy: none, while satisfying
     every word of the doctrine. Now: rung 3 is illegitimate wherever rung 1 or 2
     exists, and its log row must carry the reason. It stays in the ladder because
     it is what keeps the methodology completable with no subagent facility
     (Vision Success Signal 5) — a floor, never a default.
  2. **The stated cost was 3 items of 6.** The reviewer counted the
     `conformance_statement`, the reviewer input packet and the finding-disposition
     duty — all mandatory, none disclosed. Under the Vision, "Omission resolves
     against the proposal", so the acceptance was void as recorded. Restated in
     full above and re-accepted.
  3. **Permanent false positive on Hybrid.** `cmd_check` never passed `hybrid` to
     `cmd_validate`, and devPNT's §4.5 rows are keyed on `e_isp_`/`e_tdd_`
     doc_keys — so the advisory fired forever, unfixably, on exactly the projects
     the ownership matrix directs away from this gate. That is the failure T2
     itself calls "the worst outcome". `hybrid` is now threaded through and the
     check suppressed there; `validate` gained the flag too.
  Warnings dispositioned: log on FAIL as well as PASS (`review.md` said PASS-only
  while SKILL/templates/the shipped log all said every review — and a capped-out
  FAIL is the most valuable row there is); the moment is now read from the `tier`
  column, since matching "design" anywhere in a row let a closure row saying
  "conformance to the design" satisfy the check — **and my own test asserting the
  opposite was vacuous**, its fixture simply omitted the word; `SKILL.md` restated
  `review.md` wholesale against `review.md`'s own DRY rule and the two had already
  drifted, so Phase 3 is now trigger-plus-pointer; the REVIEW_LOG template gained
  the `## Notes` section that "what did it find" needs (the table is counts-only,
  which is why this analysis could cite two design defects that its own log rows
  cannot substantiate); moment **1b** covers late arrival (an L2 reclassified
  mid-flight has code already, and "before any implementation" had no rule for it);
  mode is declared per unit of change, not per project; and the ledger's Evidence
  column, empty on 4 of 5 rows, is filled — an empty falsifiability column in the
  artifact under a falsifiability review.
  Not adopted: keying the backstop per-increment. The doctrine handles it (moment
  1b) and a per-increment mechanical rule needs state the log does not carry;
  recorded as a named limit in T2 instead of an invented mechanism.
