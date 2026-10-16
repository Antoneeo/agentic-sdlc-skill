---
description: F-068 - kb ingestion rhythm on an open front. A new source or statement within the declared scope of an open L3 unit enters as an ingestion step of that unit (request entry, note/artifact, claim rows, reconciliation, graph) instead of a new unit; alignment, cascade, registry, the closure gate and commit run once, at an explicit closure. Also fixes the Phase-5 handoff contradiction and names anchor/--fill as the row-writing path.
status: COMPLETED
end_date: 2026-10-16
feature: F-068
id: F-068
start_date: 2026-10-16
level: L3
branch: feat/kb-ingestion-rhythm
---
# ANALYSIS: kb ingestion rhythm on an open front (F-068)

**Level: L3 · router: no match.** `reference/INDEX.md` carries `GUIDE_release.md`
(no release here) and `GUIDE_shared_project_memory.md`, which governs the shared
family files; this unit edits no file listed in `scripts/shared_manifest.json` (the
kb `SKILL.md`, `reconciliation.md`, `ENFORCEMENT.md`, `README.md` and the course
`ENFORCEMENT.md` are distribution-local). Elicitation: skip path — the spec is the
field report (R1) and the scope the owner fixed (R2), in
`audit/requests/REQUEST_kb_ingestion_rhythm.md`. Mode: Standalone (devPNT off,
`audit/project_notes.md`).

## Objective

On a live front, information arrives in pieces (a mail, then another, then a sentence
reported by phone). Today kb-agentic runs each piece as a whole L3 unit to closure:
registration, claim rows, reconciliation, rewrite of every dependent document,
registry regeneration, the closure gate, commit. On the K-02 front (15–16 Oct 2026,
R1) five pieces in two days produced five closures, and one spoken sentence touched
as many files as two new sources. The owner's chosen rhythm (R1): record note and rows
at once; alignment, registry and full checks only on request or at the end of the
day. This unit puts that rhythm in the skill text, so it is the rule rather than one
agent's memory.

Scope (R2): proposals A (an open unit absorbs new sources), B (closure is an explicit
event), D (the two immediate exceptions), E (`anchor` + `claim-id --fill`), the
Phase-5 handoff contradiction, and the deferred `stale` cascade. Out of scope: C
(`graph --only`) — a change to the shared `knowledge.py` with its own design question
(what a per-node check does not verify, when contested sets and citations cross
nodes); the field agent measured `graph` at 46 s on the full ledger (R4), and the owner
made it the next unit (R5). F (selective `index`) — no field datum asks for it beyond
R1.

## Feature Vision

**Feature Vision** `vision/features/VISION_kb_second_brain.md` (APPROVED 2026-08-27).
Its Problem names this defect: "la cerimonia e' proporzionata alle unita' governate,
non al giorno. Se scrivere costa, la KB si aggiorna solo nei giorni di cerimonia".
Benefit served: "KB [...] alimentata ogni giorno a costo ~zero". Success signal
served: "Le decisioni del giorno sono nel ledger entro il giorno, con provenance" — a
step writes the ledger at once, and an alignment closure integrates it the same day
(FS2). Signal relaxed, by the owner's choice (R1): "Nessun claim superseded citato
senza che il supersede sia visibile" holds in the ledger and in `check` at every
moment, but a dependent document's prose may lag until the next closure (T1). Feature
Non-Goals: no per-turn graph hook (the agent runs `graph` at a step, as today); no
infrastructure; no mega-release (C and F stay separate). The time-cycle charter ("la
caduta di un claim raggiunge meccanicamente chi ne deriva") holds: P1 shows the
supersession worklist is derived from state, so running it once per closure reaches
every citer.

**Project Vision** `vision/project_vision.md` (APPROVED v8). Actor served:
**Practitioner in a non-code domain** — "the same three levels and the same gates,
restated in their own domain's units" (UC1–UC3); UC4 serves the same actor through
the agent that writes on their behalf. Non-Goals checked:
- *One triage authority per kind of work*: absorption is a rule inside kb Rule Zero,
  the same authority; no second classifier is added.
- *Not a work-management system*: the HANDOFF stays an inventory; a step writes only
  resume state into its body, never assignment, due dates or ordering.
- *No ceremony ratchet* — the L3 budget, counted. Added per step: the one-line
  "ingestion step of <unit>" declaration (in place of the triage declaration it
  replaces), a HANDOFF body resume line, and the FS3 flags when they fire. Removed per
  step: the dependent-document rewrites, the `stale` run, the HANDOFF and registry
  update, `index`, the closure gate and the commit. Net: a large reduction; nothing is
  added at L1 or L2.

## Use Cases / User Needs

- **UC1 — the practitioner on a live front.** A mail arrives about a front whose unit
  is open. They want it on the ledger within minutes, without waiting for a rewrite of
  every report and the closure gate. Trace: "alimentata ogni giorno a costo ~zero".
- **UC2 — the practitioner asking for alignment.** At the end of the day, or when they
  say "allinea", they want every dependent document rewritten once against everything
  that arrived, the registry right, the checks clean, one commit, integrated. Trace:
  "onesta nel tempo"; "decisioni del giorno nel ledger entro il giorno".
- **UC3 — the practitioner with something in flight.** A mail draft is being written,
  or they were already told something a new fact makes false. They need it fixed or
  flagged now. Trace: "onesta nel tempo".
- **UC4 — rows without hand counting, on the practitioner's behalf.** The agent needs
  a locator and an id without counting lines by hand (R1 cause 5: two off-by-one line
  numbers, one id changed by a late `qty`). Trace: "a costo ~zero".

Product-name buckets: L1/L2/L3, Rule Zero, Write Triggers, Phase 4/5, Capture Moment,
claim row, `corpus/given/*` + sidecar, `corpus/notes/*`, `audit/HANDOFF_*.md`,
`audit/handoff.md` (registry), `audit/requests/REQUEST_*.md`, `graph`, `check`,
`stale`, `index`, `mark`, `anchor`, `claim-id --fill`, the `## Revision` full re-read
(kb `SKILL.md` §Revision), the closure review (`review.md` moment 2) — EXISTS.
**Ingestion step**, **alignment closure**, **unit closure** — NEW (this unit's terms).
**Closure gate** — the existing `sdlc_check.py check` (validate + stale + graph +
corpus), named here to avoid the ambiguous "battery". "Front" — METAPHOR, prose only
(the skill's term is the open unit / workstream).

## Functional Spec

Trigger fires: the agent's observable behavior on new information and at closure
changes.

**FS1 — absorption.** A unit is **open** when its `audit/HANDOFF_*.md` exists in the
checkout named by that file's `branch:` (or listed in the registry); it is deleted at
unit closure, so existence is the test. Its **declared scope** is the `scope:` field of
that HANDOFF's frontmatter (R5: the HANDOFF exists for every open unit by
construction; a front such as K-02 may have no ANALYSIS) — the topics, front or
counterpart it covers; a unit opened on a live front declares a front-wide scope there ("K-02: every source and statement
on iPassan/IPerCom"). When a source or practitioner statement arrives that the scope
covers, the agent works in that checkout, declares "ingestion step of <unit>" in place
of a new triage, and performs only: (1) the request-record entry; (2) the `given/`
artifact with sidecar, or the note; (3) the claim rows (FS4); (4) the reconciliation
classification, recording any supersession or contested set in the ledger at once,
and presenting any escalation at the end of the step (the step is a run for
`reconciliation.md` §4); (5) `graph`; (6) one resume line in the HANDOFF body
("alignment pending since <date>: <what landed>"), frontmatter untouched — so
`updated:` lags until the alignment closure refreshes it, the cost of not running
`index` at a step. It does not
rewrite dependent documents, run `stale`, edit HANDOFF frontmatter or the registry,
run `index` or the closure gate, or commit — except, on a project with no branch
isolation (every session in one shared checkout), a save commit once `graph` is clean,
its message marked `ingestion step` (R5); it has not passed the closure gate, which
stays mandatory before the closure commit and before any push or integration, and the
step reply states once per session that the residual risk is higher without isolation.
- Case: the scope does not cover it → normal triage (a new unit, or a scope change of
  this one, put to the practitioner).
- Case: coverage is doubtful, or two open units' scopes both cover it → the agent asks
  one question before ingesting, naming the candidate unit(s) and what each choice
  sets in motion; it does not default to either.
- Case: the step would fire an escalation trigger the approved ANALYSIS did not plan
  (create/supersede a node, move the hierarchy, touch more than one node's
  frontmatter) → the agent stops, declares it, and amends the ANALYSIS with the
  practitioner's approval before continuing.
- Case: no unit is open → today's triage, unchanged.
- Case: `graph` reports an error → fixed within the step; a step never ends red.

**FS2 — closure is an event, with two exits.** Phase 5 fires only on the
practitioner's request ("allinea", "chiudi") or on a session-closing signal (the
Capture Moment's signal); the agent proposes it when the planned work is done. A unit
that absorbed no ingestion step closes as before, when its planned work is done
(closure review W6: no request round added to ordinary units). It
covers everything since the last closure, enumerated from the request-record entries
since then and the uncommitted changes on the unit's branch. It runs, once: the
Capture Moment sweep; the `stale` cascade; the revision, with a full re-read, of every
document the `stale` worklist names and every document the enumerated entries affect;
the HANDOFF update; `index`; the closure gate — `check`, the only gate command: it already runs
`validate`, `graph` and `corpus`, so those are not run separately (field comment R4
point 2, verified in code); its stale stage is the spine's and does not print the kb
`## claims` worklist, so the `stale` step above stays — and the commit.
- **Alignment closure** (the unit stays open): the HANDOFF frontmatter and body are
  updated to current state; the commit lands on the unit's branch and the agent
  proposes its integration, so the day's ledger reaches the shared line the same day;
  the integration choice stays the practitioner's.
- **Unit closure** (the practitioner declares the front done): additionally the
  closure review (`review.md` moment 2) runs before DONE, and the HANDOFF is deleted.
  When it was the last workstream, `index` empties the generated registry (F1, fixed
  on `main` 28a565d and merged into this branch; harness P7).
- Case: the closure gate is red → no commit; the unit stays open; the reply names the
  failing checks; the agent fixes and re-runs.
- Case: several supersessions across steps → one `stale` run lists all of them (P1);
  each dependent document is re-read and rewritten once.
- Case: unsignaled session end → no closure runs; the steps' notes and rows are on
  disk on the unit's branch, uncommitted; the HANDOFF body says alignment is pending.
  Declared residual (T2).

**FS3 — immediate exceptions.** Two things never wait for closure: (a) a
communication draft in progress whose sentence a new fact changes is updated in the
same step; (b) a new fact that makes false a sentence already delivered to the
practitioner **in this session** is flagged in the same reply, naming the sentence and
the fact. Across sessions the agent cannot know what was delivered; the HANDOFF
resume line and the request record are what it reads.

**FS4 — rows without hand counting.** The locator of a row is produced by
`anchor <path> <phrase>`; the `id` is left empty and filled by `claim-id --fill` once,
after the row is complete (`qty` included). `graph` verifies that the span exists and
that the id is consistent with locator and `qty` — never that the span says what the
claim says (P6). A hand-counted locator, the exception for a form `anchor` does not
produce, is therefore re-read at the span before the row is written.

**FS5 — the registry is never edited by hand.** Phase 5 and the Capture Moment say
"update the HANDOFF file (or delete it), then `index`", consistent with the Write
Triggers row; no kb instruction says "update `audit/handoff.md`".

Acceptance criteria:
- AC1: kb `SKILL.md` Rule Zero states FS1: the open-unit test, the HANDOFF `scope:` field, the save commit without isolation, the
  six gestures, and the stop/ask cases.
- AC2: Phase 5 states FS2: the trigger, the enumeration, the two exits, the red-gate
  case and the last-workstream case; the Write Triggers rows for the registry and the HANDOFF say
  "at a closure or session end, never at an ingestion step" (the body resume line
  excepted).
- AC3: Phase 4 names FS3's two exceptions with the in-session limit.
- AC4: the L1 claim-row rule names `anchor`, the single `--fill`, and the limit of
  `graph` (FS4).
- AC5: no kb doctrine text instructs a hand edit of `audit/handoff.md` (FS5).
- AC6: kb `reconciliation.md` §2 item 3, kb `ENFORCEMENT.md` §1 and course
  `ENFORCEMENT.md` §1 place the cascade at closure, with FS3(b) immediate.
- AC7: a doctrine test pins AC1–AC6; behavioral scenarios cover the step, the
  unplanned-trigger stop, and the alignment closure.

## Interface Contract

Trigger fires: the surface is the agent's reply in session, which the practitioner
perceives and decides on.

1. Actors + surfaces: the practitioner, through the conversation; the agent, through
   the validator CLI (unchanged). Idioms reused: the one-line level declaration of
   Rule Zero; the Capture Moment closing signal; `reconciliation.md` §4 escalation
   form; the question discipline of `elicitation.md` for the coverage doubt.
2. Flow — step: the practitioner hands information → the agent tests open unit and
   scope → declares "ingestion step of <unit>" → writes request entry, artifact/note,
   rows → reconciliation → `graph` → HANDOFF resume line → replies. Flow — closure:
   the practitioner says "allinea"/"chiudi" or closes the session → the agent runs the
   sweep, the cascade, the revisions, HANDOFF + `index`, the closure gate → commits and
   proposes integration (alignment) or runs the closure review and deletes the HANDOFF
   (unit) → replies.
3. Affordances: the practitioner can ask for alignment at any time; the step names its
   unit, so a wrong absorption is visible at once.
4. Feedback: a step reply states what landed on the ledger, any escalation, any FS3
   item, and that alignment is pending. A closure reply states the closure-gate result,
   the documents revised, and the commit or — when red — the failing checks and that
   nothing was committed. An FS1 stop states which trigger fired; an FS1 question names
   the candidate units.
5. Constraints: Phase-4 isolation (branch/worktree); the Capture Moment's
   once-per-session closing; the destructive guards (integration is the
   practitioner's).
6. Feasibility flags: F1 (registry row of the last workstream), fixed by its own unit
   (`main` 28a565d) before this one closed.

## Capability Ledger

| Capability | Verdict | Evidence |
|---|---|---|
| verify claim rows after a step | EXISTS — `graph`; `knowledge.py#kb_check_locator` (span exists, in range) + id consistency via `#kb_claim_id` (hash of path#locator#qty) | P2, P2-RED, P4; limit P6 |
| produce a locator from a phrase | EXISTS — `anchor`; `knowledge.py` `anchor` subcommand | P2: `L1-1`, `L3-3` accepted |
| fill empty ids in one pass | EXISTS — `claim-id --fill`; `knowledge.py#kb_fill_ids` | P3 |
| list citers of a fallen id, later | EXISTS — `stale` `## claims`, state-derived | P1, P1-RED |
| keep the worklist visible meanwhile | EXISTS — `check` citation warn | P1b |
| registry from HANDOFF sources | EXISTS since `main` 28a565d (was INADEQUATE: gap F1) — `index`; `sdlc_core.py#build_registry`, `#list_workstreams` | P5, P5-RED, P7 |
| closing signal | EXISTS — kb `SKILL.md` §The Capture Moment "When" | text |

**F1** (harness P7, RED before `main` 28a565d): with zero `HANDOFF_*.md` sources
`build_registry` returned "" and `index` wrote nothing, so the last closed workstream's
row survived, and `validate` checked alignment only when sources existed. Shared spine, all four distributions: fixed by its own unit (`main` 28a565d:
`index` empties a generated registry with zero sources; `validate` errors on a generated
registry with rows and no sources), merged into this branch, and the interim this unit
first carried was removed. Nothing new for the Component Map (`strategic/architecture.md`
already describes locators as verified against stored bytes, i.e. span existence).

## Impact

| File | Change | Serves |
|---|---|---|
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | Rule Zero: new cross-cutting rule (FS1); L1 row rule extended (FS4). Write Triggers: registry and HANDOFF rows gain "never at an ingestion step" (HANDOFF: body resume line excepted). Phase 4: ingestion-step bullet with FS3. Phase 5: trigger, enumeration, two exits, red-gate case, F1 interim (FS2); "Update `audit/handoff.md`" replaced (FS5). Capture Moment "When": "updates `handoff.md`" replaced by HANDOFF + `index` (FS5). | UC1–UC4 |
| `.../kb-agentic-skill/templates.md` | HANDOFF section: the `updated:` clause (an ingestion step's body resume line excepted; refreshed at the next closure — design review N5) and "deleted at unit closure"; HANDOFF frontmatter: the `scope:` field FS1 tests against, with its definition (R5; replaced an ANALYSIS `Scope:` line added at implementation). | FS1 consistency |
| `.../kb-agentic-skill/reconciliation.md` §2 item 3 | the supersession is recorded at once; the cascade runs at the unit's next closure; FS3(b) immediate. | UC2, UC3 |
| `.../kb-agentic-skill/ENFORCEMENT.md` §1 | "reconciliation §2 runs `stale` after recording a supersession" → at closure. | consistency |
| `distributions/course-creator/skills/course-creator/ENFORCEMENT.md` §1 | the same sentence, word for word (it describes the shipped kb `knowledge.py`) → same edit. | consistency |
| `distributions/kb-agentic-skill/README.md` (triage bullet) | "a source ingested" = new unit, plus: within an open unit's scope it is an ingestion step. | derived doc |
| `ai_docs/strategic/skill_family_agent_workflows.md` (kb section) | one sentence on the ingestion step and the closure rhythm. | derived doc |
| `.../kb-agentic-skill/scripts/test_kb_ingestion_rhythm.py` | NEW: doctrine invariants AC1–AC6 (normalized-text asserts, as `test_kb_capture.py`). | AC7 |
| `.../kb-agentic-skill/evals/scenarios/open_unit_absorbs_a_new_source.md`, `unplanned_trigger_stops_the_step.md`, `alignment_closes_once.md` | NEW: K-02 event 5 replay; FS1 stop; FS2 alignment. | AC7 |
| `distributions/kb-agentic-skill/CHANGELOG.md` | entry at release time (released entries are immutable). | — |
| `ai_docs/` | this ANALYSIS, request record, harness, HANDOFF, REVIEW_LOG rows, `audit/audit_plan.md` `mark distributions/` as the last closure step, `index`. | — |

Blast radius — grep over the whole repo (all distributions, `skills/`, `ai_docs/`) for
"after recording a supersession", "ends by running", "Update `audit/handoff.md`",
"updates `handoff.md`", "every L3 closure", "source enters the corpus", "cascade",
"Phase 5":
- `reconciliation.md` §3-bis item 4 ("The cascade runs (§2 ...)") inherits the new
  timing by citation — no edit.
- `distillation.md` locator-edit bullet ("citers of the old one are reached by the
  cascade") — no edit.
- kb and course `ENFORCEMENT.md` §1 — edited (above).
- `review.md` (shared) "Phase 5, before DONE" — unchanged; FS2 runs it at unit
  closure.
- kb `SKILL.md` Routing line naming `handoff.md` as lens-ambiguous — unchanged.
- Doctrine tests: `test_kb_capture.py` pins Capture Moment phrases this unit keeps
  verbatim; no test pins a replaced sentence.
- Out of scope, recorded for follow-up (Diary): the marketing `SKILL.md` "Update
  `handoff.md`" (same contradiction, marketing lens); shared `guides.md` citing a
  "Phase-5 Comprehension checkpoint (SKILL.md §5)" kb `SKILL.md` does not have.

## Security and Threat Model

- **T1 — a stale document is used before closure.** Between a supersession and the
  closure, a dependent report still states the fallen fact. Mitigation: `check` keeps
  the citation warn standing (P1b); FS3(b) flags at once a falsified sentence already
  delivered in this session; FS3(a) fixes in-flight drafts. Residual: an undelivered,
  not-in-flight document lags until the next closure — the relaxation the
  practitioner chose (R1), named in the Feature Vision section.
- **T2 — unsignaled session end.** Steps are on disk, uncommitted, registry row stale.
  Mitigation: Phase-4 isolation keeps them on the unit's branch; the HANDOFF body
  resume line tells the next session alignment is pending; the agent proposes closure
  when planned work is done; the Capture Moment residual and orient recency line
  already cover the unsignaled end. Residual declared in FS2. Without isolation (R4
  point 4: one shared checkout synced by OneDrive, another session's `index` picking up
  an uncommitted HANDOFF) the exposure is higher: the step save commit (R5) puts the
  work in history; the residual is stated in the step reply.
- **T3 — absorption as an escape hatch.** Labeling new work "a step" to dodge L3.
  Mitigation: FS1 requires an open unit and its written HANDOFF `scope:`, asks on doubt
  or overlap, and stops on any unplanned escalation trigger; the step names its unit.
- **T4 — the fast check misses what the closure gate catches.** Mitigation: nothing is
  committed at a closure, pushed or integrated without `sdlc_check.py check` (FS2); a
  step save commit without isolation (R5) carries only `graph`, and is marked. Limit stated, not hidden: no check
  verifies that a span carries its claim (P6); FS4 answers it with `anchor` and a
  re-read of any hand-counted span.
- **T5 — the ledger diverges between branch and shared line.** A session on the shared
  line answers recall from an older ledger. Mitigation: each alignment closure commits
  and proposes integration (FS2). Residual: integration is the practitioner's choice.
- No change to personal-data, credential or external-input handling.

## Action Plan

1. Design review (moment 1) round 2, log rows. Practitioner approval of this ANALYSIS.
2. Flip status to IN_PROGRESS. Write `test_kb_ingestion_rhythm.py` (RED on the current
   text).
3. Edit kb `SKILL.md`, `reconciliation.md`, `ENFORCEMENT.md`, course `ENFORCEMENT.md`
   (GREEN).
4. Add the three eval scenarios; refresh kb `README.md` and
   `skill_family_agent_workflows.md`; run the kb test battery
   (`python -m unittest discover -s scripts -p "test_*.py"`), the course battery, and
   this harness.
5. Closure review (moment 2), log row; `sdlc_check.py check`; `mark distributions/`;
   HANDOFF deleted; `index`; commit; merge decision to the practitioner. F1 ran as its own
   unit (done, `main` 28a565d); `graph --only` is the next unit (R5).

## Test Strategy

- Harness `harness_kb_ingestion_rhythm/probe.py`: eleven assertions, three with a
  RED twin (P1, P2, P5), P6 pinning the `graph` limit, P7 the F1 fix (RED on 282cd39). Re-run at
  closure.
- Doctrine test AC1–AC6: RED on `main` (the sentences do not exist), GREEN after.
- kb and course test batteries green; `check` clean on this repo's `ai_docs`.
- Behavioral scenarios: K-02 event 5 (old text → a new L3 and Phase 5; new text → an
  ingestion step that stops after `graph` and the resume line); an unplanned node
  creation stopping the step; an "allinea" running one closure over two steps. Run by
  `evals/run_behavioral.py` where available; otherwise recorded as not run.

## Diary

- 2026-10-16 — Unit opened on R2. Probe harness 9/9 green; finding F1 recorded as
  out of scope. Feedback cause 3's line reference ("riga 289") points to text that
  now lives in the shared `memory.md` §Revision; the rule itself is unchanged by
  this unit — only its timing is set by FS2.
- 2026-10-16 — Correction to the entry above: the full re-read rule is at kb
  `SKILL.md` §Revision, as the report said; `memory.md` has no Revision section.
- 2026-10-16 — Design review: round 1 FAIL (2 BLOCK — the `graph` guarantee and the
  course `ENFORCEMENT.md` consumer), round 2 PASS with 4 WARN folded; details in the
  REVIEW_LOG row. ANALYSIS rewritten to current state; harness at 10 assertions.
- 2026-10-16 — Owner approved the design (R3); status IN_PROGRESS. Doctrine test
  written first: 9 FAIL on the unchanged text, 9 OK after the edits. Added beyond
  the Impact as first drafted: the template `Scope:` line (FS1 needs it). kb battery
  430 OK, course 252 OK, harness 10/10.
- 2026-10-16 — Closure review round 1: FAIL (B1 the step and closure replies the
  Interface Contract requires were not in the doctrine; B2 the Capture Moment's
  "once per session" against a Phase 5 that can now run twice). Fixed both and the
  WARNs; Phase 5 now leaves a unit with no ingestion step to close as before. Details
  in the REVIEW_LOG row.
- 2026-10-16 — Closure review round 2 (scoped): PASS with N1–N3. Then the field agent
  commented on the ANALYSIS (R4) and the owner ruled (R5): scope moves to the HANDOFF
  frontmatter; a step may save-commit after `graph` where there is no branch
  isolation; `graph --only` is the next unit (its timing, 46 s per full `graph`, now
  measured); the Phase-5 scoping for units with no step is confirmed (closes N1).
  Also adopted: the closure gate is `check` alone (R4 point 2), and the Capture sweep
  runs at every Phase 5 (N3). A scoped closure re-review of these changes follows.
- 2026-10-16 — Correction to the entry above: "the closure gate is `check` alone" was
  wrong. `check` runs the spine's stale, not the kb `stale` that prints the `## claims`
  worklist (expired windows are listed only there); the harness P6 line "stale rc=0"
  was misread as the kb one. Closure review round 3 caught it (B3). Phase 5 now keeps
  the `stale` step and says only `validate`, `graph` and `corpus` need not precede
  `check`. Also: Phase 4 names a project without isolation as a departure, and the
  save-commit residual says the commit lands on the shared line itself.
- 2026-10-16 — Closure review round 4: PASS. Then `main` 28a565d (the F1 fix, its own
  unit) was fast-forwarded into this branch; the interim that deleted the generated
  registry was removed from SKILL.md and FS2, and harness P7 (RED before the fix)
  replaced the INFO line: 11/11.
- 2026-10-16 — Closure review round 5 (scoped, post-merge): PASS. Unit closed:
  status COMPLETED, HANDOFF deleted, `index`, `mark distributions/`.
