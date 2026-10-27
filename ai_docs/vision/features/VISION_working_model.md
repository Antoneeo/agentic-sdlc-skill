---
description: Feature Vision for F-085, the agent's working model — constraints made extractable, synthesized and recalled at the moment of action. Read before any proposal under F-085.
status: CURRENT
---
# Feature Vision: the agent's working model (F-085)

Status: APPROVED (by Antonio Pinto, 2026-10-27 — north star `audit/requests/REQUEST_working_model.md#R3`,
written text `#R10`, after the blind check: round 1 FAIL, round 2 PASS, `audit/reviews/REVIEW_LOG.md`;
amended `#R16`, two factual sentences on the Impact's ids, after a blind check PASS).

## Authority, scope and precedence

- **Binding.** While its status is DRAFT this document informs: a conflict with it is
  flagged, never a ground to block. It binds once its status reads APPROVED, which only
  the owner can set.
- **Reach.** It governs every proposal made under unit F-085, in every skill of the
  family and in both modes (Standalone, and Hybrid with devPNT): the mechanism lives in
  the shared core, so shipping it in one skill or in devPNT does not put it outside
  these rules.
- **Precedence**, highest first: (1) the project Vision (`vision/project_vision.md`,
  APPROVED v9) and the Inherited constraints below, which restate it; (2) this
  document's Prohibitions; (3) its Invariants; (4) its Goals and Success signals;
  (5) Definitions, which fix the meaning of the terms the sections above use;
  (6) Actors and Problem, which describe and never admit or reject; (7) Pointers. A
  conflict with (1) goes to the owner.

## North star (owner's words, approved verbatim — R3)

> Io ottengo feature che raggiungono il risultato voluto con meno giri e meno attrito,
> perché l'agente tiene la situazione sotto controllo con un modello denso e verificato
> che cresce mentre lavora. Un'efficienza che peggiora l'efficacia non conta come successo.

Translation (the Italian text is the approved one): *I get features that reach the
intended result with fewer rounds and less friction, because the agent keeps the
situation under control with a dense, verified model that grows while it works. An
efficiency that worsens effectiveness does not count as success.*

## Imported facts (restated so this document reads on its own)

- **Levels.** L1 trivial: about ten lines in one or two files, no API, dependency or
  behaviour change. L2 small: clear root cause, at most three files, no new dependency
  or public API. L3 significant: anything more, or a contract, data model, new
  dependency, user-visible behaviour, security-sensitive area or non-obvious design.
  The agent declares the level of each request when it starts work on it.
- **Unit** — one L3 change, with an id (F-085 is one). It is **open** from the
  declaration of its level until its closure, the step that runs the final review,
  updates the documents and closes the unit.
- **ANALYSIS** — the unit's design document, `solutions/ANALYSIS_<name>.md`. Its
  sections include the use cases (ids `UC<n>`), the functional spec (`FS<n>`), the
  interface contract, the threat model (`T<n>`), the capability ledger, and the
  **Impact**, whose table lists every file the unit changes and, where its author cites
  them, the ids each serves, followed by the **blast radius**: every caller of each
  symbol the unit changes.
- **Gates.** The *design gate* is an independent review of the ANALYSIS before code;
  the *implementation gate* is an independent review of the code diff before
  closure. Each writes one row per round in `audit/reviews/REVIEW_LOG.md`.
- **Guide** — a document in `reference/` recording how one part of the project
  works, naming the exact source it was written from. **Component** — a part of the
  code with its own contract, as named in the architecture's component map.
- **Project** — one repository. **Family** — the skills built from this repository's
  shared core; **lens** — one skill of the family.
- **Request record** — the unit's `audit/requests/REQUEST_<name>.md` (this unit's is
  `REQUEST_working_model.md`): the owner's own words, quoted verbatim, append-only,
  each entry dated and carrying the question it answers. An entry is the owner's only
  if it quotes words the owner wrote; a paraphrase or an agent's summary is not.
- **Probe** — a small script run against the real system whose result establishes a
  claim; it is shown failing on a wrong case before it is trusted.
- **devPNT** — an optional separate product that can govern plans and documents; in
  Hybrid mode the design artifacts are read from the filesystem (its exported copies
  today, its own files once devPNT unit F-011 moves them there).

## Problem (R6, R7, R8)

The artifacts an L3 already requires together hold the constraints a correct
solution must satisfy. What fails is not their content but **attention**: when the
agent writes a claim about existing code or edits a file, the constraint that binds
that act sits in another section, read hours earlier or never, and is not seen.
Owner: *"Quello che manca è la sintesi o la capacità di osservare la cosa giusta
quando serve"* (R7).

Evidence, 2026-10-27:

- devPNT's review log has 51 rows whose verdict cell is FAIL (the success signals below
  count differently — any row whose text records a FAIL, 68 — and say so). Reading
  those 51 rows' notes, one
  was caused by where documents are stored; the others name missed callers, wrong
  counts, or a design describing intended rather than actual behaviour — constraints
  that existed and were not observed.
- `solutions/harness_working_model/probe_extractability.py` on 18 ANALYSIS files (10
  here, 8 in devPNT): use cases, functional spec and threats carry ids (4–31 per
  document); the Impact table cites an id in 67 of its 221 file rows
  (`probe_impact_bridge.py`, same sample), so it does not map each file to its ids; the
  blast radius is prose, with no id and no statement of what must stay true (3 of 18
  documents carry any id'd item there, at most 6). Reading cost to see the constraints
  today: 2,500–6,600 words per ANALYSIS.

## Definitions

- **Constraint** — a statement any correct solution must satisfy, with its
  provenance. The list of constraints is what selects the correct solution (R4).
- **Sources** — the six places constraints come from, each queried and declared
  queried, even when it yields nothing: (1) the owner's request record, (2) the
  Vision, (3) the code, (4) tests and stored data, (5) the threat model, (6) the
  project's principles and architecture.
- **Three classes** (R5, confirmed R9):
  - **Objective** — what must become true. From sources 1, 2, 5. Lives as long as the
    unit.
  - **Preservation** — what must stay true: existing behaviour, callers, contracts,
    states, data at rest. From sources 3, 4, 5, found by enumerating callers and by
    executed probes. Belongs to the component, not the unit.
  - **Operating mode** — how the solution is built: DRY, Poka-Yoke, architecture and
    patterns. From source 6. Read, not discovered; cited by a unit only where the unit
    puts it under tension.
  Security is not a fourth class: protecting a new surface is an objective
  constraint; keeping an existing protection is a preservation constraint.
- **Extractable** — the constraint carries an id, the file or symbol it is bound to
  (where it has one), its provenance, and a statement of what must be or stay true that
  a test or probe could check; a shipped command reads it without interpretation.
- **Verified** — a preservation constraint is verified when it cites its evidence: the
  caller enumeration or the executed probe that established it.
- **Released** — a preservation constraint stops binding only by a decision of the
  owner recorded in the unit's request record, never by omission and never by a tool.

## Actors (F-011 R4, confirmed R9)

- **Owner (solo developer)** — receives the benefit; approves; finds a defect after
  merge. Good UX = fewer review rounds, no regression they did not approve, nothing
  new to write.
- **Agent (author)** — has the initiative: discovers constraints, writes them in
  extractable form, consults the synthesis, receives the recall without asking.
- **Independent reviewer** — checks each listed constraint against the artifact or the
  diff, **and still derives the callers and behaviours on its own**: the list is a
  floor for the review, never its ceiling.
- **Future session's agent** — inherits the preservation constraints promoted to the
  component's guide at closure.

## Goals (positive sources)

- **G1 Synthesis, derived.** The constraints of an open unit are shown in one view a
  shipped command produces from the unit's existing artifacts; every line is one
  constraint, as its home states it, with a pointer to that home and, for preservation
  constraints, its evidence. The view always ends with the same fixed sentence: it shows
  only constraints written in extractable form, and names the sections (such as a prose
  blast radius) that must still be read in full.
- **G2 Preservation constraints are extractable**, as objective ones already are.
- **G3 Recall at the moment of action.** In a session that has declared L3 for an
  open unit, when the agent is about to edit, or write a claim about, a file or symbol a
  constraint of that unit is bound to, the constraint is put in front of it without the
  agent having to look.
- **G4 Give-back (R2).** At closure, the unit's preservation constraints not released
  move to the guide of their component; objective constraints close with the unit;
  operating-mode constraints stay in the project's principles.

## Success signals (paired — F-011 R6, confirmed R9)

Measured by `solutions/harness_working_model/` on `audit/reviews/REVIEW_LOG.md` of
this repository and of devPNT, counting rows: a row whose text records a FAIL counts,
including a round later passed. The figures below are taken 2026-10-27 over all rows to
date, for orientation. **The comparison** is per repository: the rows of the ten L3
units closed after F-085 ships against the rows of the ten closed before it, both
counted by the same instrument version. The samples are small, so the owner reads each
signal as a direction, never as a statistical result.

- **S1 Effectiveness (leads): defects that escaped a gate.**
  - Implementation-gate rows recording a FAIL — a defect the design gate let through.
    All rows to date: 40 of 88 here, 15 of 32 in devPNT.
  - Defects the owner finds in a merged change: a behaviour they report as wrong.
    Nothing is recorded today; F-085 starts the record (owner agreed, F-011 R6). Until
    a second window of ten units exists, this half of S1 has no comparison and the
    pairing rule reads the first half alone.
- **S2 Efficiency (counts only under the pairing rule): design-gate rows recording a
  FAIL.** Baseline: 72 of 124 here, 53 of 74 in devPNT.
- **S3 Extractability.** Share of new L3 ANALYSIS files whose unit changes an existing
  symbol and whose blast radius is written as extractable, verified preservation
  constraints. A unit that changes an existing symbol and has no blast radius counts as
  not extractable. Baseline: 3 of 18 sampled documents carry any id'd item there, none
  with evidence. Target: all of them.

**Pairing rule.** S2 counts only while S1 is flat or better; a fall in S2 with S1 worse
is a failure of F-085, whatever S2 shows.

## Prohibitions (R9, and closing the holes the blind check found)

- **No new authored document.** A proposal that asks the agent or the owner to write a
  separate working-model document is out; the synthesis is derived from the artifacts
  the level already requires.
- **Not a cross-project knowledge base.** Constraints never leave the repository of the
  unit they come from.
- **No claim of completeness, stated or implied.** Nothing shown — the view, a footer, a
  count of sources queried — may present the list as complete or let a gate rely on it
  as complete.
- **Nothing below L3.** No part of F-085 reaches L1 or L2 work: the recall never fires
  in a session whose declared level for the work at hand is L1 or L2, including an edit
  to a file an open unit binds.
- **Never weaken a gate.** A proposal that removes or narrows what a gate reads, derives
  or checks, or whether, when or for which units a gate runs — for example handing a
  reviewer the view in place of the ANALYSIS or the diff, or skipping a round when the
  view looks complete — is out, whatever it does to S1 or S2.
- **No computed state in the view.** The view and the recall show each constraint, its
  pointer and its evidence as the home states them, and the fixed closing sentence;
  never a count, a share, a tally, a per-line marker or badge the home does not state, a
  rank or an order of what to check next, for one unit or many.

## Invariants

- **The gates do not lose input.** *Does this change what a gate reads, derives or
  checks?* If it adds, it is admissible under the Goals; if it removes or narrows, it is
  out. Calling the removal "focus", "efficiency" or "noise reduction" does not change
  the answer. An addition that shows the reviewer the author's list of callers or
  behaviours before the reviewer has derived its own is a narrowing: the reviewer
  derives first, then compares.
- **Release and acceptance are the owner's.** *Does a preservation constraint stop
  binding, or is an added cost accepted?* Only with a request-record entry quoting the
  owner's own words, given in answer to a question that named the constraint or the
  cost; a generator, a test update, an agent's note or a paraphrase is neither.

## Inherited constraints (from the project Vision)

- **No ceremony ratchet**: *"a new mandatory artifact, field or check at L2 or L3 is
  admissible only if the same change removes one of comparable cost, or the proposal
  states the cost it adds and the owner accepts it explicitly."* G2 adds structure to
  L3 writing, G3 adds reading at action time, G4 adds closure work, S1 adds a record of
  post-merge defects: each proposal either names what it removes, or states its cost and
  carries the owner's acceptance as an entry in the request record.
- **Not a work-management system**: the view and the recall never say what to work on
  next, in what order or by whom (precedents r2, r3 in `vision/rulings.md`).
- **Complete without devPNT**: no part of F-085 depends on devPNT. Using devPNT's
  semantic index when it is present is admissible; the same result must be reachable
  without it.

## Admission test, default and exemption

- A proposal under F-085 is admitted only if it advances at least one of G1–G4 or
  S1–S3 **and, when it cites S2, states why S1 does not worsen**, and violates neither a
  Prohibition, an Invariant nor an Inherited constraint. Anything this document does
  not reach is out of F-085 and goes to the project Vision's own test.
- **Exemption — the measuring instruments.** Fixing the probes in
  `solutions/harness_working_model/` needs no admission. Every such fix re-runs the
  baseline and records the old and the new value side by side; it never rewrites a
  baseline silently. Decided by effect, not by the proposer: a fix that changes any
  value on the 2026-10-27 sample changes what is counted, and is a change to the signal,
  ruled by the admission test. Either way, a comparison always counts both of its
  windows with the same instrument version.

## Pointers

- Request record and provenance: `audit/requests/REQUEST_working_model.md` (R1–R16);
  origin interview: devPNT `ai_docs/audit/requests/REQUEST_filesystem_governance.md`.
- The efficiency lever (documents, plans and delegated approval on the filesystem) is
  devPNT unit F-011, which waits for this one (F-011 R8).
- Probes and baselines: `solutions/harness_working_model/`.
