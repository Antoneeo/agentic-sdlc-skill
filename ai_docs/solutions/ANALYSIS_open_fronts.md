---
id: F-097
feature: Open fronts - the open workstreams shown when a new unit opens, and an open analysis no workstream file carries
description: F-097 - what F-096 left out (its R10, R11) - the registry's rows shown to the owner, as declared, when a new L3 unit opens; a validator advisory naming an ANALYSIS that declares IN_PROGRESS while no workstream file names it; F-022 closed on the owner's word.
status: IN_PROGRESS
level: L3
start_date: 2026-11-14
end_date:
domain: code
---
# Feature Analysis: Open fronts (F-097)

## Objective

F-096 answered a field report (a production project, 2026-11-14, forty open
workstreams) with an advisory naming each workstream file that declares its own work
closed. Two things stayed out of it and are this unit (`REQUEST_open_fronts.md` R1):

1. **Nobody is told what is open when new work is accepted.** Owner words relayed by
   the report (R1): the skill "dovrebbe prescrivere di controllare i fronti aperti e
   fare un riassunto prima di accettare nuove attività". Replayed on release 1.55.0
   with the recorded registry (`harness_open_fronts/replay_intake.md`): two cold agents
   of two opened a new L3 unit and told the owner nothing of the forty rows; one wrote
   "il registro dei filoni (non pertinenti)". The session orientation printed five of
   the forty rows: its registry excerpt is capped at 2,600 characters.
2. **An open unit can be invisible in the registry.** In this repository
   `ANALYSIS_multi_domain_core.md` (F-022) has declared `IN_PROGRESS` since 2026-07-31
   and no `audit/HANDOFF_*.md` carries it: no file, no row. `validate` names nothing
   (`harness_open_fronts/probe_uncarried_analysis.py`, red on `main` and on F-096's
   tree). It is the inverse of what F-096 names.

The unit changes the skill family so that an owner who asks for new significant work
sees, in the same message, what the project declares open; and so that an analysis
declaring itself in progress with no workstream file is named by the validator. It
also sets F-022 to its real state, which the owner ruled is COMPLETED (R3).

**Base.** F-096 (local `main`, commits `5c667d28` and `2f007f36`). The design was
written while F-096 was still uncommitted in its worktree; this branch was
fast-forwarded onto it before any code, and the anchors below were re-checked there.

## Feature Vision

**Benefit.** The owner decides what to open knowing what is open; the registry lists
every unit that declares itself in progress, in the lenses that owe each open unit a
workstream file (code, knowledge, marketing; the course lens owes one for concurrent
work only — T4). Both without the product choosing,
counting or ordering anything.

**Alignment with `vision/project_vision.md` (APPROVED, v9).** Advances the Goal *keep
understanding durable across sessions* ("nothing load-bearing lives only in a
transcript") and the team-lead Actor's *one process, one source of truth*: the registry
is that source, and today it is neither shown at the moment it matters nor complete.

**Admission, part by part** (the ledger first, `vision/rulings.md`).

- *Showing the registry's rows when a new L3 unit opens* (FS1–FS3). Placed against
  r1, r2, r3, r9, r27 and r45:
  - r27 (ADMIT) is the row for what is shown: the state documents declare about
    themselves, derived from their own fields, read-only. The rows are copied from the
    generated registry, which r27 names as its source.
  - r3 (REJECT: tells an agent or user what to work on next, in what order, or by
    whom) is approached by the *moment*: the rows are shown when new work is asked
    for, and the same owner, in the same field report, also said "evitare di aprirne
    di nuovi finché non raggiungono un numero basso" (relayed; `REQUEST_honest_signals.md`
    R1 — a cap, refused there in R4).
    Distinction line: **it answers "what does the registry declare open now", for the
    owner, and the unit opens in the same message whatever the rows say; the product
    states no preference between the new unit and any row.**
  - r2 and r9 (REJECT: a computed or derived collection; a selection by state) reject
    the other reading of the relayed words, "fare un riassunto": a summary the agent
    writes — how many are open, which look finished, what to close first — computes a
    count and a judgement. That form is out and would need an amendment of Non-Goal 1,
    ruled first and apart.
  - r1 (REJECT: caps or meters) is not reached: nothing conditions, delays or limits
    the opening. F-096 R4 already refused a cap.
  - A match to an ADMIT row and a REJECT row is CONTESTED and the owner rules. Ruled
    R2: admitted as the rows shown verbatim; the authored summary and "nothing" were
    the alternatives. Under r4 it is scope growth of r27 (the view becomes something
    the agent is told to show at a stated moment), so it is a new row, not inherited.
  - Non-Goal 1's six conditions, checked on the form admitted. *Derived mechanically*
    holds for the registry (generated by `index`, checked by `validate` against its
    sources) and **not** for the block: the block is the agent's transcription of that
    file into a message, as R2's option said ("l'agente mostra le righe"). It is no
    kept copy — it lives in one message and is never stored, read back or updated — but
    a transcription can drop, shorten or reword a row (T7). Then: computes nothing (no count, judgement, age or selection — every row, three
    of its columns); order fixed (the registry's own); read-only (nothing is written
    from it and nothing starts); no assignment; nothing tells an agent to choose,
    prefer, avoid, skip or order units from it (FS2 forbids it in words).
- *The advisory on an analysis no workstream file names* (FS4). Twin of r45 (F-096): a
  finding on a named file, from two fields the methodology already requires — the
  analysis's own `status:` and the rule "one workstream file per open workstream, no
  file means no row" (`templates.md` §HANDOFF). It is not r45 inherited (scope growth
  is re-ruled): r45 reads one file's own field, this compares two documents. Distinct
  from r2: it derives no state of the work — it reports that two declarations the
  methodology requires disagree (the analysis says in progress, the registry has no
  row), as `validate` already does for a registry that disagrees with its sources.
  Distinct from r9: no surface lists the set; each finding is one advisory line on one
  file beside the other findings of `validate`, like r35c. Distinct from r3: it says
  which document contradicts the registry, never what to work on. New row; its
  admission is put to the owner with the design approval, not assumed.
- *F-022's status* (FS6) is a correction of one document, on the owner's word (R3).
- *Ceremony (Non-Goal 3).* See `### Ceremony cost` under Impact. One new mandatory step
  at L3 opening (FS1), accepted in principle in R2 with the figures to be confirmed
  after the design; one existing duty stated at an earlier moment in the three lenses
  that have it (FS5; the course lens, where the duty does not exist, is left out) and
  the advisory (FS4), both put to the owner with the design approval and accepted (R4). L1 and L2 gain
  nothing.

**Actors** (project Vision `## Actors`): solo developer using an AI agent; team lead
needing governance; practitioner in a non-code domain (the three sibling lenses).

**Non-goals of this unit.** Any count, cap, order, age or priority of workstreams. A
summary authored by the agent. A question to the owner about what to close. Making the
opening wait. A new command, file or field. Showing the rows at L1, L2, a Spike or the
resume of an existing workstream. An amendment of the Vision. The delegation agreement
(report point 6) and the truncated report between sessions (point 1): their own units.

**Success signals.**

- S1. In the replay of the recorded case, the message that opens a new L3 unit shows
  the registry's rows as declared and opens the unit. Baseline: 0 of 2 runs.
- S2. A project with a generated registry — with rows or emptied — and an analysis
  that declares `IN_PROGRESS` with no workstream file gets that analysis named by
  `validate`, unless its domain is `course` (FS4, T4). Baseline: not named
  (this repository, F-022).
- S3. This repository's `validate` prints no such advisory after the unit: F-022
  declares its real state.

## Use Cases / User Needs

- **UC1 (solo developer; team lead; practitioner in a non-code domain)** — asks for new
  significant work in a project with open workstreams, and needs to see what the
  project declares open at that moment, to decide alone whether and what to open.
  *Benefit: one source of truth; understanding durable across sessions.*
- **UC2 (solo developer; team lead)** — asks for work that an open workstream already
  carries, and needs the agent to say so and resume it rather than open a second.
  *Benefit: one source of truth.*
- **UC3 (team lead)** — reads `validate` and needs an analysis that declares itself in
  progress with no workstream file to be named, so the registry can be trusted to list
  what is open. *Benefit: one source of truth.*

Product names: workstream registry (`audit/handoff.md`), `HANDOFF_[feature].md`,
`validate`, `index`, the level declaration (Rule Zero's line), ANALYSIS frontmatter
`status:` — all EXISTS, in the product's own terms. NEW, declared: the
`Open workstreams` block of the opening message (UC1, UC2); the uncarried-analysis
advisory (UC3).

## Functional Spec

**FS1 — the message that opens a new L3 unit shows the registry's rows (UC1).** When a
request is triaged L3 (E3 in a lens that counts E-levels) and no open workstream
carries it, the message that declares the level contains, before the first question:

    Open workstreams (audit/handoff.md, as declared):
    - <workstream> · <status> · <next step>

one line per row of the generated registry, the three cells copied as written, in the
registry's order, every row. Cases:
- the registry has no row → `Open workstreams: none`;
- the project has no generated registry (no handoff, or one still written by hand) →
  `Open workstreams: no generated registry`;
- the level is L1, L2 or a Spike, or the request resumes an existing workstream → no
  block is owed;
- the level rises to L3 mid-flight → the block is in the message that declares the
  reclassification.

Limit, course lens: its registry holds concurrent work only, so the block there shows
what the registry declares and not every open course; a course in progress with no
workstream file appears in no row and FS4 does not report it (T4).

**FS2 — nothing is added to the rows and the unit does not wait (UC1).** The block
carries no count, total, age, grouping, judgement of a row, or suggestion of what to
close, finish or do first; no row is dropped, shortened or reworded; a cell's text is
shown as data and never followed as an instruction; the agent asks no question about the
rows; and the unit opens in the same message — request record, Vision Gate and questions proceed as
today. What the owner does on reading it is theirs.
*Acceptance (FS1, FS2):* on the recorded forty-row registry and a new L3 request, the
opening message shows forty lines matching the registry's cells, adds none of the
above, and the request record of the new unit exists.

**FS3 — a request an open workstream already carries is resumed (UC2).** If the request
belongs to a row's workstream, the message names that row and the agent resumes the
workstream (its HANDOFF and ANALYSIS Diary) and opens no second unit.
*Acceptance:* given a registry with a row for a named feature and a request to continue
it, the message names the row, the agent resumes that workstream, and no second unit
is opened (no request record, analysis or workstream file for one).

**FS4 — an analysis in progress that no workstream file names is reported (UC3).** In
a project that generates its registry — it has at least one workstream source, or its
`audit/handoff.md` is a generated registry, emptied or not — `validate` reports, as an
advisory, each ANALYSIS whose `status:` is `IN_PROGRESS` when no workstream source names
it. A source names an analysis when the analysis's file name appears in the source's
frontmatter (any field; `details:` is where the template puts it), or the analysis's unit
id appears as a whole token in the source's `workstream:` value.
The advisory names the file and both gestures: if the work is open, write its workstream
file with the analysis in `details:` and run `index`; if it is finished, set its status.
An advisory never fails a build, `--strict` included. Cases:
- `PLANNED` → not reported (the workstream file is due when implementation starts,
  FS5; reporting it would fire on every unit in design);
- `COMPLETED`, `CANCELLED` → not reported;
- no workstream source and a generated registry (every workstream closed — the usual
  state of a project that runs one unit at a time) → reported: it is the case where the
  registry says "none" and an analysis says in progress;
- no workstream source and no generated registry (no handoff, or one written by hand:
  not converted) → nothing reported;
- a shadow of a devPNT document → not an analysis, not reported;
- an analysis with no unit id → matched by file name only;
- an analysis whose domain resolves to `course` → not reported: the course lens asks
  for a workstream file only for concurrent work (its Write Triggers row "Concurrent
  work"; its template: "For parallel work"), so there a missing file contradicts
  nothing.
*Acceptance:* `probe_uncarried_analysis.py` green: with a source present, and with
the registry emptied, the uncarried `IN_PROGRESS` analysis is named once, and the
carried, the `PLANNED`, the `COMPLETED` and the course-domain ones are not; in a tree
that never generated a registry, and in one whose handoff is written by hand, nothing is
named. The golden regression holds the hand-written case too.

**FS5 — the workstream file is written when the analysis becomes in progress (UC3).**
The handoff template of the code, knowledge and marketing lenses says the workstream
file exists, at the latest, from the moment the unit's analysis declares `IN_PROGRESS`;
the code lens, the only one that states the flip `PLANNED` → `IN_PROGRESS`, repeats it
there. (In those three lenses the file is already owed for every open workstream —
"One exists for every OPEN workstream" in each template; this states when at the
latest, so FS4 is silent on a unit that follows the method.) The course lens is not
touched: its workstream file is owed for concurrent work only, and making it owed for
every course would be a new artifact; FS4 does not report course-domain analyses.
*Acceptance:* the three handoff template texts and the code lens's Phase 4 text state
it; invariant tests read them. A statement of doctrine: its behavioural check is FS4's.

**FS6 — F-022 declares its real state.** `ANALYSIS_multi_domain_core.md` becomes
`COMPLETED`, `end_date: 2026-11-14` (R3: the owner named no other date), with a Diary
entry naming where its three declared open items happened.
*Acceptance:* S3.

## Interface Contract

Surfaces touched, all existing; no new command, flag, file or field.

| Use case | Actor acts / perceives through | Flow (responsibility level) | Feedback |
|---|---|---|---|
| UC1 | the agent's message that declares the level of a new L3 unit | the triage declares the level; the agent reads the generated registry (a read the code, knowledge and marketing lenses already require at this step; new in the course lens) and copies its rows; each lens's opening doctrine owns the duty | the `Open workstreams` block, or one of its two one-line forms |
| UC2 | the same message | the agent matches the request to a row; the resume doctrine (HANDOFF + Diary) takes over | the row named; no new unit |
| UC3 | `validate` output of each lens's entry point | the analysis reader lists the analyses; the registry reader lists the workstream sources; the uncarried-analysis reader returns the analyses in progress that no source names; the validator prints them through its advisory channel | per file, one `[note]  …` line; exit codes unchanged |

Idioms reused: the one-line declared verdict (the router verdict's form — a line whose
absence reads as "did not look"), extended to a block; the spine's `[note]` advisory
channel, as F-096's closed-workstream advisory uses it. No new idiom.

Architectural constraints touched: the golden transcript
(`fixtures/golden_baseline.txt`) pins `validate` and `check` output byte for byte; its
corpus holds one `IN_PROGRESS` analysis (`ANALYSIS_pick_list.md`, F-002) in a project
that never generated a registry: its `HANDOFF_pick_list.md` has no frontmatter, so it is
not a source, and its `handoff.md` is written by hand. FS4's "not converted" case
therefore keeps the transcript unchanged — asserted, not assumed (Test Strategy). The
golden corpus exercises that case only; "carried" and "emptied registry" are the unit
tests'.

Feasibility flags from the walk: the marketing overlay validates its own document
model on a `mkt_docs` root, where no `ANALYSIS_*.md` exists; FS4 reaches it only through
the spine's `cmd_validate` on an `ai_docs` root. Stated as a limit, no overlay edit.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| show the owner what the registry declares open when a unit opens | INADEQUATE | `SKILL.md` Phase 1 tells the agent to read the registry "before touching anything"; nothing tells it to show the owner. `cmd_orient` prints registry rows at session start within `ORIENT_REGISTRY_CHARS` (2,600) | `replay_intake.md` baseline: 0 of 2; `SESSION_START.txt` of the fixture: 5 of 40 rows |
| resume instead of opening a second unit on the same topic | EXISTS | `SKILL.md` Write Triggers (ANALYSIS row: "On topic match with an existing analysis, update that one") and Phase 3 "search `ai_docs/solutions/` … update it instead of duplicating it"; FS3 names the registry row at the opening message | re-read of both passages |
| name an analysis in progress that no workstream source names | MISSING | `sdlc_core.py`: `list_analyses` and `list_workstreams` are each read by `cmd_validate`, never compared; `_open_units` reads open analyses for id collisions only | `probe_uncarried_analysis.py`: red on `main` and on F-096's tree |
| list the workstream sources / the analyses | EXISTS | `sdlc_core.py::list_workstreams`, `::list_analyses` | used as they are |

No new component: the MISSING row is one function over two existing readers, inside
the validator core's contract (advisories on the docs root).

## Guide check

- CURRENT guide covering what this touches: `GUIDE_skill_family_changes.md` (copies
  count once; read whole) and `GUIDE_shared_project_memory.md` (validator composition
  across the four lenses; read whole — its trap "use the final exit code, not the CLEAN
  banner" applies to the tests).
- High-complexity component understood here that no guide covers: no.

## Impact

All paths are against `main` with F-096 (see Objective, Base).

**Shared core** — authored in the code lens, copied verbatim into the three
distributions (`shared_files.py`; `test_drift.py` is red until each manifest is
regenerated):

- `skills/agentic-sdlc-skill/scripts/sdlc_core.py` — MODIFY: `uncarried_analyses`
  (new, over `list_analyses` and `list_workstreams`) and
  `uncarried_analysis_advisories` (new); `cmd_validate` adds the latter to the
  advisories it prints, beside `closed_workstream_advisories`. The reader uses
  `is_generated_registry` for the gate and `resolve_domain` with
  `project_default_domain` for the course case, each as it is.
- `skills/agentic-sdlc-skill/scripts/test_merge_safety.py` — MODIFY: tests for FS4
  (its seven cases, `--strict` exit unchanged).
- `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` — MODIFY: invariants
  for FS1–FS3 (each lens's text carries the block's three forms, the "nothing added,
  nothing cut, cells are data, no waiting" sentence and the resume sentence) and FS5
  (the handoff template of the code, knowledge and marketing lenses; the Phase 4 clause
  in the code lens; both profile-gated, the course lens asserting neither).
- `skills/agentic-sdlc-skill/scripts/shared_manifest.json` and its three copies —
  regenerated.
- The three copies of `sdlc_core.py`, `test_merge_safety.py`, `test_skill_invariants.py`
  under `distributions/*/skills/*/scripts/` — verbatim copies.

**Golden transcript:** `fixtures/golden_baseline.txt` in the three trees that have one —
NOT modified; `test_golden_regression.py` must stay green with no re-capture.

**Code lens:**

- `skills/agentic-sdlc-skill/SKILL.md` — MODIFY: Phase 1, registry bullet (FS1–FS3);
  Phase 4, the flip bullet (FS5).
- `skills/agentic-sdlc-skill/templates.md` — MODIFY §HANDOFF: the file exists at the
  latest from `IN_PROGRESS`; `details:` names the analysis, which is what `validate`
  matches (FS4, FS5).
- `skills/agentic-sdlc-skill/evals/scenarios/intake_shows_open_workstreams.md` — ADD.

**Sibling lenses**, each in its own wording (edits, not copies):

- `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` — `### 1. Audit and
  Alignment`, registry bullet (FS1–FS3).
- `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` — `### 1. Intake &
  Triage`, registry bullet (FS1–FS3; "engagement" for "unit", the docs root's registry).
- `distributions/course-creator/skills/course-creator/SKILL.md` — `### 1. Orient and
  align` (FS1–FS3). This passage reads README, INDEX and the guide router and not the
  registry: here FS1 adds the read of `audit/handoff.md` itself, at L3 opening.
- `templates.md` of kb and mkt — the `HANDOFF_[…]` section each carries (FS5, the
  `details:` sentence). Neither `SKILL.md` states the flip (grep `IN_PROGRESS`: no
  match), so the template is FS5's only home there.
- Course lens: `templates.md` and the Write Triggers row "Concurrent work" are NOT
  modified — FS5 does not apply and FS4 does not report course-domain analyses.

**Derived documents the audit plan binds to a doctrine change:**

- `ai_docs/strategic/skill_family_agent_workflows.md` — MODIFY: the opening step.
- `ai_docs/strategic/architecture.md` — MODIFY the Validator core row of the Component
  Map: it names this analysis's preservation table.
- `README.md` and the three distribution READMEs — MODIFY only where they state what
  `validate` reports or what happens when a unit opens; re-read whole at closure (F-096
  FS1).

**Project documents:**

- `ai_docs/vision/rulings.md` — two rows: r47, the rows shown at opening, citing R2, R4,
  R5, R6 and r4; r48, the advisory, citing the design approval R4.
- `ai_docs/solutions/ANALYSIS_multi_domain_core.md` — MODIFY frontmatter and Diary
  (FS6); `ai_docs/strategic/features_history.md` — regenerated.
- `ai_docs/audit/HANDOFF_open_fronts.md` — ADD at the flip (FS5, applied to this unit),
  deleted at closure.
- `ai_docs/solutions/E2E_TEST_open_fronts.md`, `ai_docs/solutions/MERGE_REVIEW_open_fronts.md`
  — ADD at closure; `ai_docs/audit/reviews/REVIEW_LOG.md` — one row per review.
- `CHANGELOG.md` of the four packages at release (`GUIDE_release.md`).

No new dependency. No API or data-model change. Repository is CRLF: content deltas,
never file copies.

### Ceremony cost

| What | Who pays, when | Cost | Accepted |
|---|---|---|---|
| The `Open workstreams` block (FS1) | every opening of a new L3/E3 unit, all four lenses | one line per registry row: 360 characters in this repository (2 rows); 12,935 on the redacted copy of the recorded case (40 rows, longest row 623) — `measure_rows.py`. No new read in the code, knowledge and marketing lenses, whose opening step already reads the registry; **one new read in the course lens**, whose step does not — and there the rows cover concurrent work only (FS1's limit) | R2 in principle; figures accepted R4; the course lens's read R5 |
| Doctrine text for FS1–FS3 | every session that loads the skill, per lens | measured: `SKILL.md` +1,140 (code, of which 111 are FS5's clause) / +1,029 (kb) / +1,055 (mkt) / +1,166 (course) UTF-8 LF bytes — above the estimate of about 700 that R4 accepted; accepted as measured in R6 | estimate accepted R4; measured figures accepted R6 |
| Workstream file written when the analysis becomes `IN_PROGRESS` (FS5) | code, knowledge and marketing lenses, each L3, once; the course lens pays nothing | no new artifact in those three: the file is already owed there for every open workstream; its latest moment moves from session end to that point. Measured: +209 bytes in each of the three `templates.md` (read on trigger), 111 in the code lens's `SKILL.md` | accepted R4 |
| The advisory (FS4) | a project in the state it names, on `validate` | one line per such analysis; nothing at L1; never an exit code. A new check, though it cannot fail | accepted and admitted R4 |

### Preservation constraints

| id | bound to | callers | must stay true | evidence |
|---|---|---|---|---|
| P1 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::cmd_validate` | `cmd_check` and the `validate` dispatch in the same file; `knowledge.py` (present in all four trees; the marketing entry point routes to it too); `mkt_check.py` `main`; `test_design_approval.py`, `test_guide_check.py`, `test_merge_safety.py`, `test_skill_invariants.py`, `test_domain_rules.py`, `test_plan.py`, `test_constraints.py`, `test_session_start.py`, kb's `test_kb_graph.py`, `test_golden_regression.py` through the CLI | the new finding is an advisory: no error or warning count changes, the `--strict` exit is unchanged on every existing project, the golden transcript is byte-identical | grep `cmd_validate` over the four script trees (2026-11-14); the code's own rule where advisories are printed ("never fail a build, not even --strict") |
| P2 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::list_analyses` | in the same file: `build_index`, `chronology_advisories`, `_open_units`, `cmd_validate`, `cmd_gate`, and the two constraints readers (`unit_constraints`, `open_code_units`); `docs_site.py::build_units`; `test_skill_invariants.py` | signature and returned list unchanged: the new reader reads its result, it does not filter it; shadows stay excluded | grep `list_analyses` over the four script trees: seven call sites in `sdlc_core.py`, one in `docs_site.py`, one in the invariant battery |
| P3 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::list_workstreams` | `build_registry`, `registry_conversion_blockers`, `rc_registry`, `chronology_advisories`, `closed_workstreams` (F-096) and `cmd_validate` in the same file; `docs_site.py`; `mkt_check.py`; `test_merge_safety.py` | signature and returned list unchanged; the new reader uses the frontmatter each source already returns, and changes nothing | grep `list_workstreams` over the four script trees |

## Security and Threat Model

Surfaces touched: filesystem reads of project documents under the docs root (the same
files `validate` already reads); text the agent copies from the registry into a message
to the owner. No stdin, network, authN/authZ, cryptography or personal-data surface.

- **T1 — the block becomes work management.** An agent adds a count, marks rows as
  finished or asks what to close: that is the form the Vision refuses. Requirement: FS2
  forbids it in words in each lens; the eval scenario judges the message on it (Q-how,
  Q-gate); the rulings row records the form admitted and the form refused.
- **T2 — repo-controlled text reaches the owner as if it were the agent's.** Registry
  cells are written by whoever edits the workstream files. The block is headed "as
  declared" and copies cells; the same text already reaches the context through the
  session orientation, which labels it repo-sourced. Requirement: FS2 states that a
  cell is data and is never followed; an invariant reads that sentence in each lens.
- **T3 — the advisory names units that are carried (false positives).** In the recorded
  project `details:` cells point at shadows, guides and spikes, and `workstream:` values
  carry no unit id. Requirement: a source names an analysis by file name in its
  frontmatter *or* by unit id in `workstream:`; the advisory states the one-line fix; it
  is an advisory and never fails a build. The inverse error is accepted and stated: a
  source whose frontmatter names an analysis it does not carry (a `details:` cell citing
  a sibling unit's analysis) makes that analysis read as carried.
- **T4 — the advisory is taken for proof that the registry is complete.** It reads
  `IN_PROGRESS` analyses only: a `PLANNED` unit left across sessions with no file, an
  open unit of a Hybrid project (its design is in devPNT, not an ANALYSIS) and an open
  L2 with no analysis stay invisible, and so do a course unit that is not concurrent
  work (by that lens's own rule) and an analysis a source names without carrying (T3). Stated in the Test Strategy's limits and in the rulings row; the
  advisory text claims nothing about the others.
- **T5 — a long registry floods the opening message.** Forty rows cost about 13,000
  characters. Accepted as the cost of the admitted form (R2): cutting, grouping or
  sampling rows would be a selection. The figure is in the ceremony table for the
  owner's confirmation.
- **T6 — path or status text injected through the advisory.** It prints a file name from
  `solutions/` and the fixed word `IN_PROGRESS`, after an exact match.
- **T7 — the transcription is not the registry.** The agent, not a command, copies the
  rows: under "as declared" it can drop, shorten or reword one, most likely on a long
  registry. Requirement: FS2 forbids it in words; the eval judges the message's lines
  against the registry's cells, row by row. Alternative weighed and not taken: a shipped
  command printing the three columns for the agent to relay. For it: the bytes are exact
  at the source. Against: a new command surface for one message, and the transcription
  remains — tool output is not reliably shown to the owner, so the agent would still
  copy the command's output into its message, with the same risk. The registry file is
  already that exact source. Residual: fidelity of the block rests on doctrine and on
  the owner being able to open `audit/handoff.md`, which the block's heading names.

## Action Plan

- [x] F-096 on `main` (the owner's commit and merge); this branch rebased on it.
- [x] Flip this analysis to `IN_PROGRESS`; write `HANDOFF_open_fronts.md`; `index`.
- [x] RED: tests for FS4 in `test_merge_safety.py` (seven cases, `--strict`, golden
  unchanged); invariants for FS1–FS3 and FS5 in `test_skill_invariants.py`.
- [x] `sdlc_core.py`: `uncarried_analyses`, `uncarried_analysis_advisories`, the call in
  `cmd_validate`. Probe green.
- [x] Doctrine: code lens `SKILL.md` Phase 1 and Phase 4; the three sibling `SKILL.md`;
  the `templates.md` HANDOFF texts of the code, knowledge and marketing lenses (not the
  course lens).
- [x] Eval scenario; replay with the candidate text on the recorded case (two runs) and
  its two variants (FS3, L2).
- [x] Copies and the four manifests; full battery in each tree; golden unchanged.
- [x] F-022: status, end date, Diary entry (FS6); `index`.
- [x] Derived documents; `vision/rulings.md` rows; E2E script; closure review; merge
  brief; `mark` the analysed areas; `check` CLEAN.

## Test Strategy

- **Probes kept with the unit** (`harness_open_fronts/`), red on 2026-11-14:
  `probe_uncarried_analysis.py` (FS4: fixture and this repository, on `main` and on
  F-096's tree) and the replay `replay_intake.md` with `build_intake_fixture.py` (FS1,
  FS2: two cold runs on release 1.55.0, mid-tier model, Q-open = no in both). Green is
  the acceptance. `measure_rows.py` is the cost figure, not a check.
- **Unit tests** (AAA, in the shared batteries): FS4's seven cases (the emptied
  registry, the never-generated tree, the hand-written handoff and the course domain
  among them — the course domain both declared in the analysis and reached through the
  README's `default_domain: course` on an untagged one); a source naming the analysis in
  its body only does not carry it; the advisory printed
  once per file; `--strict` exit unchanged with the advisory present (P1); `list_analyses`
  and `list_workstreams` results unchanged (P2, P3); the golden regression green with
  no re-capture. Mutation: drop the call in `cmd_validate` → red.
- **Invariants** over each lens's `SKILL.md`: the block's heading and its two one-line
  forms, the sentence forbidding additions, cuts and waiting and calling a cell data
  (FS2), the resume sentence (FS3); FS5 in the handoff template of the code, knowledge
  and marketing lenses and in the code lens's Phase 4.
- **Doctrine replay** (FS1–FS3): the eval scenario run cold with the candidate text on
  the recorded forty-row fixture, two runs, judged on the message and the files left:
  every registry row present with its three cells unaltered, nothing added, unit opened
  (FS1, FS2, T7); a variant where the request continues a row's workstream (FS3); a
  variant with an L2 request, where no block may appear — the Non-Goal 3 guard. The
  `none` and `no generated registry` forms, with the condition of each, and the
  mid-flight case are held by the text invariants only; stated as a limit. F-096's replays met a ceiling (old text
  not red); here the baseline is red, so a green candidate is evidence — of two runs,
  one tier, one case.
- **E2E, human** (`E2E_TEST_open_fronts.md`): a new L3 request in a real project with a
  generated registry shows the block; `validate` in a project with an uncarried
  `IN_PROGRESS` analysis shows the advisory.
- **Not verifiable here / limits stated:** the recorded case cannot measure FS4 — it
  holds 43 workstream frontmatters and no analysis frontmatter (a Hybrid project); FS4
  reads `IN_PROGRESS` analyses only (T4); whether owners open fewer units after seeing
  the rows is a field signal and is not a goal of this unit.

## Diary / Current State

**2026-11-14 — unit opened on a brief from the F-096 session; measured; owner ruled.**
Opened by a brief, not by owner words (R1). F-096 found unmerged (uncommitted in its
worktree): the design is written against its tree, code waits for it. Elicitation round
skipped: goal, scope, constraints and done are stated in the brief, and the two points
only the owner could settle were asked as one set (R2, R3). Measurements before any
design claim: `probe_uncarried_analysis.py` red on `main` and on F-096's tree (F-022
named by nothing); the recorded case holds no analysis frontmatter, so question 2 cannot
be measured on it; replay baseline on release 1.55.0, two runs, mid-tier model, fresh
context, judged on the returned message and on the files each run left (one request
record, nothing else): run 1 — release 1.55.0, mid tier, Q-open no, Q-how n/a, Q-gate
no; run 2 — release 1.55.0, mid tier, Q-open no, Q-how n/a, Q-gate no. Transcripts are
not kept; the returned messages were read in this session only. Question 1 placed against the
ledger: CONTESTED between r27 and r3, the authored summary on r2/r9; owner ruled for the
rows verbatim (R2). F-022: every Action Plan box ticked, its three open items overtaken
(`distributions/` holds three lenses; packages published at 1.55.0 / kb 1.37.0 / mkt
0.32.0; kb method files at 89 / 295 / 152 lines); owner ruled COMPLETED (R3).
Weighing taken without a question: `PLANNED` is not reported (FS4) — reporting it would
fire on every unit in design, the noise the field case shows nobody reads; against: a
`PLANNED` unit left across sessions with no file stays invisible (T4). Next: independent
design review, then the owner's design approval with the ceremony figures.

**2026-11-14 — design review round 1: FAIL, three blockers, all confirmed on the code.**
(1) The advisory was gated on "at least one workstream source", so it was silent in a
project whose generated registry is empty — every workstream closed, an analysis still
in progress — which is the full form of the defect and a state the code already tells
from "not converted" (`is_generated_registry`). Gate rewritten; case, probe and tests
added. (2) The reason given for the unchanged golden transcript was false: its
`HANDOFF_pick_list.md` has no frontmatter and its `handoff.md` is written by hand; the
corpus is a not-converted project. Reason corrected. (3) "No new read" was false for the
course lens, whose opening step does not read the registry: the added read is now in
the ceremony table. Nine warnings, all taken: a quotation attributed to the wrong owner
sentence; "derived mechanically" claimed for the agent's transcription (now stated as
it is, with T7 and the weighing against a shipped command); T2's requirement moved into
FS2; FS5 given a home in every lens's handoff template, so the advisory is not noise in
the knowledge and course lenses; preservation callers corrected; `templates.md`, the E2E
script, the merge brief and the review log added to the Impact; the match narrowed from
"anywhere in the source file" to its frontmatter, the inverse error stated; an L2 replay
variant added; the advisory's admission and cost put to the owner instead of inherited
from r45. Next: scoped re-review, then the owner's design approval.

**2026-11-14 — design review round 2: FAIL, one new blocker from a round-1 correction,
confirmed.** Ten of twelve round-1 findings addressed. New: "the workstream file is
already owed for every open workstream" is false in the course lens, which asks for it
only for concurrent work, so FS5 there would have been a new artifact stated as none.
Weighing taken: FS5 stays out of the course lens and FS4 does not report course-domain
analyses — for: no new artifact in a lens whose doctrine made the file conditional on
purpose; against: a course unit that is not concurrent work stays outside the registry,
as it is today by that lens's own rule (T4). The other reading — make the file owed for
every course — is listed for the owner with the design approval. Also taken:
`docs_site.py::build_units` added to P2; one count of FS4's cases (seven); the probe
gained a hand-written-handoff tree, a course-domain analysis and the COMPLETED assertion
on the emptied tree. Next: round 3, the last of the cap.

**2026-11-14 — design review PASS at round 3 (FAIL → FAIL → PASS), the cap.** Round 3
found the round-2 findings addressed and no blocker; four warnings stand, corrected in
the text after the PASS and not re-reviewed (the cap is reached), so they go to the
owner with the approval: the Action Plan still named four handoff templates; FS1 stays
in the course lens, where the registry holds concurrent work only, with that limit now
stated; the benefit and S2 qualified for the course exception; the probe's header
brought up to date and the `default_domain: course` path added to the unit tests. Row
in `audit/reviews/REVIEW_LOG.md`. Next: the owner's design approval, with the ceremony
figures and the advisory's admission; no code before it, and none before F-096 is on
`main`.

**2026-11-14 — design approved by the owner (R4, R5); implementation started with FS6.**
R4 approves the design, accepts the three costs and admits the advisory; R5 keeps the
rows in the course lens with the limit declared. This analysis flipped to `IN_PROGRESS`
and, as FS5 asks, its workstream file exists. FS6 done: `ANALYSIS_multi_domain_core.md`
is `COMPLETED`, `end_date: 2026-11-14`, with a Diary entry; `index` run; the probe on
this repository now reports every open analysis carried and stays red on the fixture
alone. Everything else waits: the remaining steps edit passages F-096 changes, and F-096
is still uncommitted in its worktree.

**2026-11-15 — implemented on F-096's `main`; four batteries green; replays green.**
F-096 reached local `main` by its own session; this branch was fast-forwarded onto it
(`2f007f36`) and `check` was CLEAN before the first edit. RED first: 21 of the 22 new
tests failed (the 22nd is the course-lens limit, a no-op in the code lens). Then
`uncarried_analyses` and `uncarried_analysis_advisories` in the core, the call in
`cmd_validate`, the doctrine in the four `SKILL.md` and the three non-course
`templates.md`, the copies and the four manifests. `probe_uncarried_analysis.py` green
on this repository. Batteries on the working tree, 2026-11-15: code 664, knowledge 977,
marketing 680, course 670, all OK; golden transcripts untouched and their regression
green with no re-capture; node tests 76, 27, 7, 13 (root), 52 (kb), 52 (mkt), 4 pass of
5 with none failing (course).

Doctrine replay, candidate text, mid-tier model, fresh context, judged on the file each
run saved (`OWNER_MESSAGE.md`) and on the files it left:
- run 3 — candidate, recorded 40-row registry, new L3 request: `judge_rows.py` GREEN
  (heading, 40 of 40 rows verbatim, in order); Q-open yes, Q-how verbatim, Q-gate no;
  the request record of the new unit exists.
- run 4 — same, second sample: `judge_rows.py` GREEN (40 of 40); Q-open yes, Q-how
  verbatim, Q-gate no; request record exists.
- run 5 — FS3 variant, three named rows, the request belongs to F-007: the message
  names the F-007 row, says no new unit is opened and resumes it (Diary entry, `next:`
  of its workstream file); no block, as owed on a resume. It created a request record
  for F-007 itself, which the fixture lacked — the acceptance line "no new request
  record" was written for a second unit and the fixture should have carried the first
  unit's record; read as a pass on FS3, with that fixture limit.
- run 6 — L2 variant, 40-row registry, a one-file fix: level declared L2, no
  `Open workstreams` block (Non-Goal 3 guard).
Each of runs 3 and 4 added one sentence after the block saying no row concerns the
request, so a new unit opens. That is FS3's question answered in the negative, not a
judgement of a row; noted because FS2 does not name it. Baseline was 0 of 2; candidate
2 of 2: two samples, one tier, one case.

Measured against the estimates the owner accepted in R4: the block's size is as
measured; the doctrine is larger than estimated — `SKILL.md` +960 to +1,071 bytes per
lens at that point, +1,029 to +1,166 after the closure review's corrections, against
"about 700". Accepted as measured by the owner (R6). `README.md` and the three
distribution READMEs each state what `validate` and `index` name (F-096's sentence): the
uncarried-analysis advisory is added to that sentence in all four. None describes what
happens when a unit opens, so the block is not described there.

**2026-11-15 — closure review round 1: FAIL, three blockers, all confirmed and fixed or
put to the owner.** Code, tests, copies and manifests were found sound. (1) The four
READMEs do state what `validate` names (F-096's sentence) and were untouched, while this
Diary said none did: sentence extended in all four, the Diary corrected. (2) This unit's
own workstream file still described the state before implementation — F-096's defect,
in the unit after it: rewritten, `index` run. (3) The rulings row r47 presented the
measured doctrine size as accepted in R4, which accepted "about 700": the row now says
so, and the owner accepted the measured figures (R6). Six warnings taken: the course lens lacked the
reclassification and Spike clauses; R4 and R5 were in the request record twice (a
transcription script run twice; the second copies, byte-identical and never committed,
removed); FS3's acceptance said "no new request record" where it meant "no second unit"
(reworded here, in the eval variant and in the E2E script); the doctrine did not say
when each one-line form applies (now it does, with invariants); P3 described a read the
code does not make and P1 named a test file that does not call `cmd_validate`; the
marketing sentence said "unit" for "engagement".

**2026-11-15 — closure review round 2: FAIL, one new blocker from a round-1 correction,
confirmed and fixed.** All nine round-1 findings addressed. New: the sentence added to
the course README said `validate` names an analysis in progress with no workstream file,
which is false for that package's own projects (course-domain analyses are not
reported): the README now states the exclusion. Four warnings taken: the marketing
README says the advisory reaches an `ai_docs` root only; this unit's `next:` named a
confirmation already given (R6) and is rewritten; the Impact and the ceremony table
cite R6. **Limit, stated:** the doctrine replays (runs 3 to 6) were run on the sentence
before the closure review's wording corrections — the condition of each one-line form,
the course lens's Spike and reclassification clauses, "engagement" in the marketing
lens — and were not repeated on the final text; those additions are held by text
invariants only. Also not changed, to keep the byte figures the owner accepted: the
marketing `templates.md` sentence on `IN_PROGRESS` does not say it applies on an
`ai_docs` root only.

**2026-11-15 — closure review PASS at round 3 (FAIL → FAIL → PASS), the cap; waiting on
the owner.** Round 3 found the five round-2 findings addressed and no blocker. On the
final working tree, run by the round-3 reviewer and after the last edit of any Python or
doctrine file: batteries code 666, knowledge 979, marketing 682, course 672, all OK
(the earlier figures plus the two invariants the closure review added); shared copies
byte-identical; node tests 76 / 27 / 7 / 13, 52, 52, 4 pass of 5 with none failing;
probe green; `check --root .` CLEAN (validate rc=0, stale rc=0), with the three areas
marked by timestamp because the tree is uncommitted. Two warnings stand and were not
corrected, the cap being reached: the READMEs' one-clause summary of the advisory omits
"in a project that generates its registry"; nothing else. `MERGE_REVIEW_open_fronts.md`
written. Nothing is committed: the commit and the merge are the owner's. This unit is a
part under coordination (owner's naming in `REQUEST_honest_signals.md` R13): after the
owner's yes, commit on this branch, mark the three areas by commit hash, commit that,
`check` CLEAN, then ask the coordinator for the fast-forward of `main`. The unit stays
open, its workstream file kept, until it is on `main`.

**2026-11-15 — the owner approved the commit (R7).** Committed on this branch; the three
analysed areas then marked by commit hash in a second commit; `check` re-run on it. The
fast-forward of `main` is asked of the coordinating session.
