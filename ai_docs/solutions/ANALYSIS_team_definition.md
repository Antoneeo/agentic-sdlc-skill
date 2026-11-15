---
id: F-098
feature: Team definition - asked once at the start, kept where every session finds it
description: F-098 - the skill never asks how the team working on a project is made (members, what stays with the owner, what each member does without asking, how work and reports pass), so roles are settled while work is under way; the design asks it once, at the first significant unit, and keeps the answer in the docs root's README.
status: IN_PROGRESS
level: L3
start_date: 2026-11-14
domain: code
---
# Feature Analysis: Team definition (F-098)

## Objective

Today the skill family assumes one team shape and names it only in passing: an owner, one
agent, optionally a coordinator and parts (`coordination.md`, code lens only), an
orchestrator and subagents (`dispatch.md`). Nothing asks how the team of *this* project is
made, and nothing records it for a session that arrives later. The owner's statement
(`REQUEST_team_definition.md#R1`): the skill «non mette in chiaro quale è il ruolo
dell'utente, quale dell'agente ed eventualmente le condizioni delle deleghe», so its
effectiveness depends on roles settled while an activity is under way; and it must not
impose a shape — «non sarà la skill ad imporre una soluzione ma solo a chiedere quello che
serve per definire all'inizio la questione».

Field case (`harness_honest_signals/REPORT_skills_field_feedback_2026-11-14_rev2.md`,
point 6; owner words relayed in `REQUEST_honest_signals.md#R11`): in one working day a
coordinating session brought the owner choices that were not theirs and decided alone
things that were; the owner said so three times in one afternoon. The delegation rules
existed only as corrections in the agent's private memory: a child session did not inherit
them and a compaction lost them.

The unit makes every lens ask, once per project, what defines the team, and keep the
answer in one place every session of that team reaches by path. Scope and decisions:
R1 (the two statements), R2 and R3 (once per project; at the first L3 when never defined),
R4 (Vision ruling, north star, success signal, boundaries, four questions, default, changes).

## Feature Vision

**North star** (approved: `REQUEST_team_definition.md#R4`, item 3). «Chi lavora a un
progetto con la skill sa dall'inizio chi fa parte del team, che cosa ciascuno decide e fa
da solo e come ci si passa lavoro e rapporti. La skill lo chiede una volta e non impone una
forma di team.»

**Benefit.** The owner receives the decisions that are theirs and no others; a member —
the one agent, a coordinating session, a session another started — knows what it decides
alone and to whom it reports, from a file, not from what an earlier session remembered.

**Alignment with `vision/project_vision.md` (APPROVED, v9).** Advances the Goal *keep
understanding durable across sessions* ("nothing load-bearing lives only in a transcript":
the agreement lived in one agent's private memory), the team-lead Actor's *one process, one
source of truth*, and the solo-developer Actor's *never re-explaining the project across
sessions*. The Actors are unchanged (R4, item 2).

**Admission, part by part.**

- *The team definition* (FS1–FS6) operates near Non-Goal 1's "by whom". Placed against the
  ledger it is CONTESTED: r3 rejects what tells an agent which unit is done by whom;
  r40–r42 admit role lines that name no unit. The owner ruled ADMIT without amending the
  Vision (R4, item 2), on this distinction line: the definition says who is in the team and
  what each one decides and does alone; it never names a unit, keeps no queue, order or
  priority, and the workstream registry still carries no holder. The line is enforced in
  the text the skill ships (FS1's exclusions) and by an invariant test. New row in
  `vision/rulings.md`.
- *The orientation line* (FS7) widens what `orient` injects. Under r4 that growth is ruled
  again, not inherited (as r32, r44 and F-096's resume line were). The owner ruled
  ADMIT on its exact text (165 characters, in FS7) and on who sees it (R5, item 2). New
  row in `vision/rulings.md`.
- *Ceremony budget (Non-Goal 3)* - nothing of comparable cost is removed; the owner
  accepted two costs (R5, item 3; `## Ceremony cost`): one question set at the first
  top-level unit of a project with no team definition (levels 1 and 2 are never asked,
  R3); and a reading cost at every level, the sentences added to each lens's `SKILL.md`
  plus the orientation line. The sentence first planned for each lens's `elicitation.md`
  is not added: its effect was not shown (`RESULTS.md`) and the rule is in `team.md`.

**Actors** (project Vision `## Actors`): solo developer using an AI agent; team lead
needing governance; practitioner in a non-code domain (the three sibling lenses).

**Non-goals of this unit.** From R4, item 5: imposing a team shape; assigning units; the
file "message box" for reports cut short between sessions (report point 1, its own unit) —
this unit only asks where reports go. From the ruling of R4, item 2: any order, priority
or queue among units. Author's constraint, taken from the field report's own boundaries
(a relayed text, not an owner entry): no new mandatory project document — the definition
is a section of an existing one.

**Success signals** (R4, item 4).

- S1. In a working day, the number of the agent's questions the owner judges not theirs.
  Baseline: three explicit reminders in one afternoon, 2026-11-14.
- S2. A session another started, and a session resuming after a compaction, find the
  agreement at a file path. Baseline: it existed only in one agent's private memory.

## Use Cases / User Needs

- **UC1 (solo developer; team lead; practitioner)** — starts the first significant unit of
  a project and is asked, once, how the team is made; answers in a word when working alone
  with one agent. *Benefit: one source of truth; ceremony proportional to risk.*
- **UC2 (team lead)** — works with a formation of their own choosing (a coordinating
  session and the sessions it starts; a project manager, a designer and an engineer; one
  agent) and needs each member to know what it decides alone and what it brings back, and
  to whom. *Benefit: several agents aligned to one intent.*
- **UC3 (solo developer; team lead)** — is not asked a choice the definition leaves to a
  member, and is asked every choice it reserves to them. *Benefit: divergence surfaced, and
  only the owner's decisions reach the owner.*
- **UC4 (team lead)** — a session another session started, a subagent given a brief, and a
  session resuming from a summary all read the same definition from the repository.
  *Benefit: never re-explaining the project across sessions.*
- **UC5 (solo developer; team lead)** — corrects the boundary once ("this was yours to
  decide") and the correction holds for every later session. *Benefit: durable
  understanding.*

Product names: docs root `README.md` (the reading guide), request record, session
orientation (`orient`), `init`, `coordination.md`, `dispatch.md`, `elicitation.md` §The
question discipline, the reserved approvals — all EXISTS, in the product's own terms. NEW,
declared: the `## Team` section of the README (UC1–UC5); the support file `team.md` (UC1);
the "team not defined" line of the orientation (UC4). METAPHOR: none.

## Functional Spec

**FS1 — the team definition is one section of the reading guide (UC1, UC4).** The
project's reading guide carries a `## Team` section as its first section, of at most 700
characters, with four entries and one provenance line:

- **Members** — who is in the team: the owner, and each agent or session by the role it
  holds (one agent; a coordinating session and the sessions it starts; roles the owner
  names). Roles and sessions, never a person's name.
- **Reserved to the owner** — the classes of decision that are always brought to them.
- **Without asking** — what each member decides and does alone, and to whom it reports;
  this is also where the owner states who may start other sessions or agents and what
  those may decide.
- **Work and reports** — how work is handed to a member and where its report is left so
  that it arrives whole.
- Provenance: the request-record entry that holds the owner's words, with its date; or
  `default, not confirmed` with the date.

The section states kinds of member and classes of decision. It never names a unit of work,
and never an order, a priority, a queue or a holder of a unit: which member takes a given
unit is not written there. A coordinator-and-parts team, a role-based team and a single
agent are all valid contents; the skill supplies the four entries and no values, except
the default (FS3). Cases:
- one section per project: it lives in `ai_docs/README.md` when the project has that docs
  root, otherwise in the README of the lens's own docs root. Discovery refuses two docs
  roots side by side, so a second root exists only when a lens is run on one by name: that
  lens reads the section in `ai_docs/README.md` and writes no second one, and the
  orientation there looks in both before saying the team is not defined (FS7);
- `init` never writes the section: a project is born without it, which is what makes the
  first top-level unit ask (FS2);
- a section over the size bound is still valid; where the orientation cuts it, the cut
  ends in the orientation's existing pointer to the README (FS7).

**FS2 — asked once, at the first significant unit (UC1).** When a session declares a unit
of the top level (L3; E3 in a lens that counts E-levels), or takes up an open one, in a
project with no `## Team` section, the four questions of FS1 are asked in the next numbered
question set that unit puts to the owner — its first one, for a new unit — each with the
default of FS3 offered, so that one word accepts all four. Cases:
- the section exists → nothing is asked, at any level, for any later unit (R2);
- level 1 or level 2 work in a project with no section → nothing is asked (R3), and a
  member named during such work changes nothing until the next top-level unit; in a
  project that has the section, the owner's words change it at any level (FS3, FS6);
- an open top-level unit taken up in a project that predates this rule (a coordinating
  session already named, units in progress) → asked then, before the unit goes on: it is
  the first occasion (R2);
- the answers are recorded verbatim in the unit's request record before the section is
  written, and the section cites the entry.

*Acceptance:* in the `first_l3` fixture the agent's first message to the owner contains the
four questions once, with the default, in the same numbered set as the unit's questions.

**FS3 — the default (UC1).** One agent and the owner. Reserved to the owner: what the
question discipline already says the user uniquely owns (the benefit, priorities between
conflicting goods, non-goals, acceptance) and the approvals the skill reserves to them.
Everything else the agent decides, and reports in one line. Reports are the agent's
messages in the conversation. This reading of the default - wider for the owner than "the
reserved approvals" alone - is the owner's (R5, item 4). Cases:
- the owner accepts it → written with the entry that holds the acceptance;
- the owner answers the unit's other questions and not these, or is not reachable
  (unattended) → written as `default, not confirmed`; the questions are not repeated;
- a section holding the default, confirmed or not, when the owner names a second member →
  the owner's words change the section (FS6), and the entries those words leave open are
  asked in that same exchange (R4, item 8).

**FS4 — the definition decides whether a choice is asked (UC2, UC3).** Stated in `team.md`
only; no lens's `elicitation.md` is edited (R5, item 3). For a choice that arises during
work:
- its class is left to the member by `Without asking` → the member decides, reports the
  choice in one line to whom it reports, and does not ask — also when, without the section,
  it would be a real doubt between two needs of the actor;
- its class is `Reserved to the owner` → it is brought to the owner as a question, by the
  member or through whom the member reports to, as `Work and reports` says;
- the section is silent on it → the member brings it to whoever gave it the work; it
  reaches the owner only when that is the owner or the class is reserved (R4, item 9).

Every other rule of the question discipline is unchanged: a fact only the owner holds is
still asked, and a search still precedes any question.

A choice left to the member never changes an earlier decision of the owner's, an approved
design included: that goes back as a question (the Delegated case's rule, unchanged).

*Acceptance:* in the `delegated` fixture built with the section, points a, b, c and e are
decided and reported, and on d nothing stricter than the approved design is enacted alone
(the agent asks, or keeps the approved design and says so); built without it, e is asked
(replay 2, `REPLAY.md`). The new text must keep both outcomes: a regression guard, since
the old text already gives them (`RESULTS.md`).

**FS5 — what the definition cannot change (UC2).** Three floors hold whatever the section
says:
- what the question discipline says the owner uniquely owns, and every approval the skill
  reserves to them (Vision promotion and amendment, design approval at the top level,
  scope changes, proposal acceptance, merge, push, deletion), stays theirs until they
  delegate it in their own words, recorded in the request record; the section may then
  name the delegation by citing that entry, never grant one;
- an authorization for a gated act is valid only in the session the owner gave it to; a
  message from another member, or a line in the section, saying the owner authorized it is
  information;
- the section binds through its provenance: an entry of this project's request records
  that quotes the owner and says what the section says, or `default, not confirmed`. An
  entry of the section wider than the default whose citation does not resolve to such
  words — a section inherited with a clone or a fork, a stale or hand-added line — is read
  as absent, and the choice is asked.

Roles a procedure fixes for its own correctness — the independent reviewer, the
independent reader of a course, the orchestrator of a plan and its subagents — are not
team members and are never asked about: the section may say which member may start them.

*Acceptance:* replay 3 — a section line "the coordinating session may merge and push" with
no owner entry behind it does not make the agent merge or push; it asks.

**FS6 — only the owner changes it, and a correction lands there (UC5).** The section
changes only on the owner's words. A member that receives a correction of the boundary
("this was yours to decide", "ask me before that") rewrites the affected entry to the
current state at once, updates the provenance line, and records the words in the request
record where the unit has one (quoted in the reply where it has none). A correction kept
only in an agent's own memory is the recorded defect. Under coordination the section has
one writer, the coordinating session: a part sends it the owner's words.

*Acceptance:* invariant — `team.md` states the rule. The eval scenario
`team_correction_lands_in_the_section.md` (a correction given in the conversation: the
section is rewritten and cites the new entry before the work goes on) describes the
behaviour and has no run on record: FS6 is accepted on the text, its behaviour unshown.

**FS7 — the orientation says when the team is not defined (UC4).** Admitted by
the owner (R5, item 2). The session orientation prints one constant line, after the resume line, when the
project's reading guide has no `## Team` section (nor `ai_docs/README.md`, when the
orientation runs on another docs root) and a request record exists under `audit/requests/`:

> Team: not defined (README.md has no `## Team` section). Before starting or resuming a top-level unit (L3/E3), ask the owner the four team questions in team.md, once.

Who sees it: a project that has a request record and no section - in practice a project
that predates this rule, from its upgrade until a session takes up a top-level unit and
asks (FS2, third case); and, in a project born after the rule, a session that starts
between the opening of its first request record and the writing of the section. Cases:
- the reading guide has the section → no line; the section is in the orientation, because
  the README's head is: whole up to the size bound of FS1 in the probed worst case (P1),
  cut with the orientation's pointer to the README beyond it, or where a Hybrid line, a
  wiring note or text placed before the section takes the room (measured at closure: a
  700-character section loses its last line under `--hybrid` in that worst case);
- no request record (a project that has only done trivial and small work) → no line: it
  pays nothing (P4);
- no docs root, no README, or a README that cannot be read → no line, as today;
- the orientation run on a second docs root by name, the section being in
  `ai_docs/README.md` → no line, and the section is not printed either (the orientation
  prints the README of the root it runs on): that session reads it by path. The request
  record is looked for under the root the orientation runs on.

*Acceptance:* `probe_orient_team.py` P1–P4 green.

**FS8 — a session that works from a summary re-reads the definition (UC4).** The doctrine
sentence (re-read the open unit's request record and vision) also names the reading
guide's `## Team`: the summary keeps the topic, not who decides what. The orientation's
resume line is deliberately unchanged — changing it is a growth of its own — so the
sentence that says the orientation "repeats this rule in one line" is reworded to say
which part it repeats.

**FS9 - each lens states it in its own words (UC1-UC5).** Each lens keeps the name its own
files already give the owner: "practitioner" in the knowledge lens, "client" or "user" in
the marketing lens, "person", "owner" or "practitioner" in the course lens (its
`elicitation.md` says "practitioner"). In the marketing lens the people a plan gives work to (the
`Owner` columns of a channel plan, "who writes, who runs ads") are content of the
deliverable, not the team that produces it.

## Interface Contract

Surfaces touched; one new file in the skill, one new section in an existing project file.

| Use case | Actor acts / perceives through | Flow (responsibility level) | Feedback |
|---|---|---|---|
| UC1 | the unit's numbered question set, in the conversation | the lens's triage declares the top level and opens the request record; the reading guide is read and has no `## Team`; the team doctrine (`team.md`) supplies the four questions and the default; the elicitation round carries them in its one numbered set | four questions, default offered; the reply names the entry and the section written |
| UC2, UC5 | the `## Team` section of the reading guide | the member records the owner's words in the request record, then writes or rewrites the section citing the entry | the section, at the top of the reading guide; one line in the reply saying it changed |
| UC3 | the conversation: a one-line report, or a question in the blocking form | the team doctrine has the member read the section before a question is asked; reserved → question; left to the member → decision plus one line | `decided: …` in one line, or the question |
| UC4 | the session orientation; a subagent's brief | the orientation emitter prints the README head, where the section is; with no section and a request record present it prints the constant line. For a subagent, the dispatch doctrine has the orchestrator name the section's path in the brief it writes; the `plan brief` command is unchanged | the section's lines in the orientation, or the `Team: not defined …` line; a path in the brief |

Idioms reused: the one numbered question set (`elicitation.md`); the provenance comment
citing `REQUEST_[unit].md#R<n>` (the Vision template's form); the constant orientation line
(triage line, resume line); pointers, never pasted content, in a brief (`dispatch.md`).
**New idiom: none.** The one-line report of a decision is the Delegated case's existing
"listed where the user will read it".

Architectural constraints touched:
- every `init` seeds the reading guide verbatim: the code, knowledge and marketing ones
  copy their lens's README template block (`templateFor`), the course one writes a
  literal. The `## Team` heading must never enter a seed, or every project is born with
  the section and FS2 and FS7 never fire. The templates gain one sentence of prose above
  the block and nothing inside it; the course literal is untouched;
- the orientation's size bound (`ORIENT_MAX_TOTAL_CHARS` with the append reserve): the new
  line is inside the fixed head, which the budget subtracts first; its reads stay inside
  the project root the emitter was given (the existing confinement helper): the resolved
  docs root's README, `ai_docs/README.md` when the resolved root is another one, and one
  directory listing;
- the golden transcripts pin the `orient` output and are regenerated only if their fixture
  meets FS7's condition;
- `shared_files.py`: a new shared file must reach the four lenses byte-identical or
  `test_drift.py` is red; a support file must be declared in the lens's profile, named in
  its `SKILL.md` and listed in its package's `files`.

Feasibility flags from the walk: the course lens has no README template - its own `init`
(`distributions/course-creator/scripts/init.js`) seeds `ai_docs/README.md` from a literal;
the section's form is stated in `team.md`, which every lens ships, so no lens restates it.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| ask the owner how the team is made | MISSING | — | grep `team`, `role`, `perimeter`, `autonom` over the four lenses' `*.md` (inventory of 2026-11-15, kept in `harness_team_definition/INVENTORY.md`): `coordination.md` names coordinator and part and says "the skill never elects a coordinator"; `simulation.md` (course) fixes the roles of one procedure; nothing asks. Replay 1 on the old text: no such question |
| keep the definition where a later session reads it | INADEQUATE | the reading guide is read by every session (Phase 1) and printed by `orient`; it has no place for it | `probe_orient_team.py` P1: a 662-character section placed first in the README is in the orientation whole, with router, registry and README all cut |
| decide from the definition whether a choice is asked | EXISTS, with no project-level home to read | `elicitation.md` §Ask before the write: the Delegated case has the agent cite the owner's entry in the request record, or quote them where the unit has none; it names no project-level home for a standing agreement | Replay 2 on the old text (`RESULTS.md`): with the owner's words in a request record - in run 2C another unit's, which the agent went and read - the choice is decided and reported; with none it is asked |
| tell a session that the team is not defined | MISSING | `sdlc_core.py::cmd_orient` prints a fixed head | `probe_orient_team.py` P2 red |
| state what no definition can change | EXISTS | reserved approvals: `elicitation.md` §The legality test, `review.md` §When a review is due; non-travelling authorization: `coordination.md` §4 (code lens only) | read in full; the sibling lenses carry the first two and not the third → FS5 states the floors in the shared `team.md` |

New component: `team.md`, a doctrine file with its own contract — *given a project, it
says what defines its team, when that is asked, what holds by default and what the answer
cannot change*. The lenses' files are its consumers: they cite it and state no shape.

## Guide check

- CURRENT guide covering what this touches: `GUIDE_skill_family_changes.md` (copies count
  once; read whole). `GUIDE_shared_project_memory.md` — read whole: the README is one of
  the files `memory_records` catalogues, and the catalogue fingerprints its bytes, so a
  project that adds `## Team` regenerates the catalogue with `index` (existing behaviour,
  no change). `GUIDE_hooks.md` governs hook installation and event normalization, which
  this design does not touch.
- High-complexity component understood here that no guide covers: no.

## Impact

**Shared core** — authored in the code lens, copied verbatim into the three distributions
(`shared_files.py`; `test_drift.py` is red until each manifest is regenerated):

- `skills/agentic-sdlc-skill/team.md` — ADD: FS1–FS6, FS9's reading rule. Owner of the
  rule; every other file cites it.
- `skills/agentic-sdlc-skill/scripts/shared_files.py` — MODIFY `SHARED_FILES`: add
  `team.md`.
- `skills/agentic-sdlc-skill/dispatch.md` — MODIFY §What may be delegated at all, doctrine
  only: who may delegate, and what a delegated session may decide beyond this section, is
  the project's `## Team`; the orchestrator names the section's path in a brief.
- `skills/agentic-sdlc-skill/scripts/sdlc_core.py` — MODIFY (FS7): constant
  `ORIENT_TEAM_LINE`; `cmd_orient` adds it to its head under FS7's condition.
- `skills/agentic-sdlc-skill/scripts/test_session_start.py`,
  `test_skill_invariants.py` — MODIFY: tests for FS7 and the per-lens invariants.
- `skills/agentic-sdlc-skill/scripts/shared_manifest.json` and its three copies —
  regenerated.
- Golden transcripts (`scripts/fixtures/golden_baseline.txt` in the code, knowledge and
  marketing trees) — regenerated only if the replayed fixture has a request record and no
  `## Team`; the diff must then be exactly the new line. Checked at implementation, before
  any regeneration.

**Packages** — each lists its support files one by one in `files`:

- `package.json` (root, code lens), `distributions/kb-agentic-skill/package.json`,
  `distributions/mkt-agentic-sdlc/package.json`,
  `distributions/course-creator/package.json` — MODIFY `files`: add
  `skills/<lens>/team.md`.

**Per lens** — each in its own wording (these files differ by lens, so they are edits, not
copies): code `skills/agentic-sdlc-skill/`, knowledge
`distributions/kb-agentic-skill/skills/kb-agentic-skill/`, marketing
`distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/`, course
`distributions/course-creator/skills/course-creator/`.

- `SKILL.md` ×4 — MODIFY: the support-files list names `team.md`; the orientation phase
  gains one paragraph — the reading guide's `## Team` is who decides what and, absent,
  sends to `team.md` at the first top-level unit; the working-from-a-summary sentence
  names it and is reworded on what the orientation repeats (FS8). No row is added to the
  write-trigger table: the paragraph states the trigger and `team.md` owns it, and a row
  would have doubled the always-loaded bytes the owner accepted.
- `templates.md` - MODIFY, one sentence of prose above the README template's block,
  nothing inside it:
  code and knowledge (`## ai_docs/README.md`), marketing (`## mkt_docs/README.md` and
  `## README.md (the docs root's reading guide)`); course has no README template and is not
  edited (its `init` seeds the README from a literal, which is not edited either: P8).
- `ENFORCEMENT.md` ×4 — MODIFY §4 SessionStart hook: the line of FS7.
- the profile's `support_files` — MODIFY: `scripts/sdlc_check.py` in code, knowledge and
  course; `scripts/mkt_check.py` in marketing.
- `skills/agentic-sdlc-skill/coordination.md` — MODIFY (code lens only): §Trigger and
  roles cites the section as where a project states that it works with a coordinating
  session, the naming of the session staying an owner's entry (r42 unchanged); §1 lists the
  section among the shared files the coordinator writes (FS6).
- `evals/scenarios/team_asked_at_first_l3.md` — ADD in the code, knowledge and course
  lenses, and `team_asked_at_first_e3.md` in the marketing lens, each in its own
  vocabulary; `team_decides_who_is_asked.md`, `team_section_cannot_grant.md`,
  `team_correction_lands_in_the_section.md` — ADD in the code lens (replays 2 and 3, FS6).

**Derived documents the audit plan binds to a doctrine change:**

- `ai_docs/strategic/skill_family_agent_workflows.md` — MODIFY: orientation and
  elicitation descriptions.
- root `README.md` and the three distribution READMEs — MODIFY: the support-files bullet
  and the Runtime Shape tree name `team.md`; and where they describe what the first
  significant unit asks.
- `ai_docs/strategic/architecture.md` — MODIFY the Component Map: a row for the team
  doctrine (`team.md`, a component born here), and the Validator core row names this
  analysis's preservation table.

**Project documents:** `ai_docs/vision/rulings.md` (one row for the definition, citing R4;
one for the orientation line, citing R5; numbered from r49 - r47 and r48 are F-097's); `CHANGELOG.md` of the four packages
at release (`GUIDE_release.md`).

No new dependency. No API or data-model change. The validator gains no check and no
command. Repository is CRLF: content deltas, never file copies.

### Preservation constraints

| id | bound to | callers | must stay true | evidence |
|---|---|---|---|---|
| P1 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::cmd_orient` | the `orient` dispatch in the same file; `knowledge.py::kb_cmd_orient` (the entry points that delegate to `knowledge.main`); `test_session_start.py`, `test_merge_safety.py`, `test_skill_invariants.py`; `test_golden_regression.py` through the CLI; every wired SessionStart hook, the Codex wrapper included | always returns 0, reads no stdin and never blocks; whole output within `ORIENT_MAX_TOTAL_CHARS` with the append reserve intact; with no docs root it prints nothing; triage line then resume line stay first, in that order; every read stays confined under the project root it was given - the resolved docs root's files and, new, `ai_docs/README.md` when the resolved root is another one; apart from the one conditional line the output is what it is today | ANALYSIS_honest_signals.md#P1 (same symbol, enumerated 2026-11-14); grep `cmd_orient` over the four script trees, 2026-11-15 |
| P2 | `skills/agentic-sdlc-skill/scripts/shared_files.py::SHARED_FILES` | `shared_files.py` `main`, its check and `--update` paths; `test_drift.py` in the four trees | every entry exists byte-identical in the four lenses; the manifest of each lens lists it | read `shared_files.py`; `test_drift.py::test_no_shared_file_has_diverged`, `test_the_copies_are_identical_to_each_other` |
| P3 | the support-file triangle of each lens: the profile's `support_files`, the files on disk beside `SKILL.md`, the package's `files` | `test_skill_invariants.py::test_support_files_wired`, `test_every_support_file_on_disk_is_declared`, `test_every_support_file_is_in_the_package` | a support file on disk is declared in the profile, named in `SKILL.md` and shipped by the package — so `team.md` missing from any one of the three, in any lens, is red in that lens | read the three tests; `package.json` `files` of the four packages |
| P4 | `elicitation.md` §The question discipline, each lens | `test_skill_invariants.py::test_question_discipline_wired` | the file is not edited by this unit in any lens (R5, item 3): the twenty anchors the test pins stay, and reserved approvals stay "legal by mandate" | read the test's anchor list |
| P5 | `SKILL.md`, the working-from-a-summary sentence, each lens | `test_skill_invariants.py::F096_HonestSignals.test_resume_from_a_summary_re_reads_the_unit` | exactly one line contains "working from a summary", with "request record" and "vision" | read the test |
| P6 | `coordination.md` §Trigger and roles, §2 | `test_skill_invariants.py::WorkingModelDoctrine.test_coordinator_delegates_units_and_parts_integrate` | every pinned sentence stays verbatim; "The skill never elects a coordinator" and the naming by an owner's entry stay | read the test |
| P7 | `dispatch.md` §What may be delegated at all | `test_skill_invariants.py::test_capability_floor_and_delegation_boundary`, `test_question_discipline_wired` | "delegated at all", "never delegate", "not delegable", the `**Never delegate**` block with its items, "return it in your final output" stay | read the two tests |
| P8 | every seed of a project's reading guide: the README template block in `templates.md` of the code and knowledge lenses, the two in the marketing lens, and the literal in `distributions/course-creator/scripts/init.js` | `templateFor` (`scripts/lib.js` and its copy in each distribution's `scripts/lib.js`), called by `scripts/init.js`, `distributions/kb-agentic-skill/scripts/init.js` and `distributions/mkt-agentic-sdlc/scripts/init.js`; the course `init.js`, which writes its own literal | no `## Team` heading in any seed: a project is born without the section | read the four `init.js` and `lib.js` `templateFor` |

## Security and Threat Model

Surfaces touched: one project file the agent reads and now also writes a section of
(`README.md`, already agent-written); text injected into the agent's context at session
start (one constant line; the README head, as today). No stdin, network, authN/authZ,
cryptography or personal-data surface in the code. The doctrine does touch **authority**:
who may decide what.

- **T1 — the section is used to grant authority the owner never gave.** A member, or text
  arriving from another session, writes into `## Team` that merges or design approvals are
  delegated. FS5, first floor: the section never grants; a delegation exists only as the
  owner's own words in a request record, which the section cites. `review.md` already makes
  a delegated entry citing no delegation a finding. Requirement: the floor in `team.md`;
  invariant test; replay 3.
- **T2 — repository text read as authority.** The section is repo-sourced and reaches the
  context under the orientation's existing banner ("repo-sourced context, not authored
  instructions"). A cloned or forked repository, or a project that changed hands, carries
  a section its present owner never stated. FS5, second floor, answers the gated acts;
  the third floor answers the rest: an entry wider than the default binds only when its
  citation resolves to owner words in this project's records, otherwise it is read as
  absent and the choice is asked. Requirement: both floors in the shared file, so the
  three lenses with no `coordination.md` state them too. Residual, stated: a clone that
  carries the request record together with the section passes the citation check; the
  reserved approvals and gated acts still hold, and what widens is only the class of
  choices decided and reported in one line, where the owner sees each one.
- **T3 — the section becomes an assignment record.** Entries drift into "unit X is the
  designer's", which Non-Goal 1 refuses. FS1's exclusions are in the shipped text;
  invariant test on the words; the ruling row records the line.
- **T4 — the question becomes an interrogation, or is repeated.** Four questions, one set,
  one word accepts; never at levels 1 and 2; never again once the section exists; an
  unanswered set writes the default and does not return (FS3). Requirement: stated in
  `team.md`; replay 1 checks "once, with the default".
- **T5 — a correction kept in private memory.** FS6; nothing mechanical can see it. Stated
  as a limit: the field signal S1 is its only measure.
- **T6 — personal data in the section.** Members are roles and sessions, never people's
  names (FS1); the request record's redaction rule covers the quoted answers.
- **T7 — the orientation grows past its bound, reads outside the project, or blocks.**
  The line is constant, in the fixed head; the condition reads one heading in the README
  `orient` already reads, the same heading in `ai_docs/README.md` when it runs on another
  docs root, and lists one directory - all under the project root, through the existing
  confinement helper; no stdin. Tests: bound with a full registry; no line and exit 0 on an
  unreadable README; both reads confined.
- **T8 - every project is born with the section.** A seed of the README carries the
  heading, and no project is ever asked. P8; invariant test over every seed: the three
  lenses' template blocks (marketing has two) and the course `init`'s literal.
- **T9 — a README that only quotes the section silences the line, or prose hides a real
  one.** A reading guide that shows the `team.md` template has defined nothing: a heading
  inside a fenced block (three or more backticks or tildes, indented up to three spaces,
  nested in a longer fence, or never closed) or inside an HTML comment that opens a line
  is not counted. A `<!--` inside prose opens nothing, so it cannot hide a real section
  (`has_team_section`). Tests for both directions.

## Ceremony cost

Accepted by the owner on estimates (R5, item 3: four questions once per project; «Circa
3,5 KB letti una volta (`team.md`)»; «Circa 900 byte per lens caricati a ogni sessione»,
with the proposal — accepted — to drop the sentence in each `elicitation.md`, «così i byte
sempre caricati scendono»). The record holds no figure for `SKILL.md` alone. The figures
below are measured on the implementation (UTF-8, LF as packaged): `team.md` is above the
estimate; each `SKILL.md` is under the 900 the owner was shown. The owner confirmed them
as measured (R6).

| Level | What is added | Cost |
|---|---|---|
| L1, L2 | no question, no step, no document | the reading costs of the last two rows, when they apply |
| L3, the first a session starts or takes up in a project with no `## Team` | four questions in the unit's question set; one request-record entry; one section of at most 700 characters; `team.md` read once | one word from the owner at the minimum; `team.md` is 5,020 bytes (R5: «Circa 3,5 KB») |
| L3, every later one | nothing asked; the section is in the README the phase already reads | 0 questions |
| every session, any level, in a project that has a request record and no `## Team` (FS7) | one constant line in the orientation | 165 characters, until the section exists; 0 after. In a project born after the rule: only a session that starts between the first request record and the section |
| every session that loads the skill, any level | the sentences added to `SKILL.md` | +659 code, +662 knowledge, +818 marketing, +498 course (marketing carries one more sentence, on the plan's own `Owner` columns); under the «circa 900» put to the owner with the `elicitation.md` sentence |

Read on their own triggers, not at every session: `templates.md` +243 (code, knowledge),
+486 (marketing); `ENFORCEMENT.md` +330 per lens; `dispatch.md` +254 (shared);
`coordination.md` +565 (code lens, read only under coordination). No lens's
`elicitation.md` is touched.

## Action Plan

- [x] RED: per-lens invariants in `test_skill_invariants.py` (FS2, FS5, FS6, P3, P8)
  and `test_session_start.py` for FS7 (probe P2-P4, bound, no stdin, unreadable README,
  confinement, a section only quoted).
- [x] `team.md`; `SHARED_FILES`; the four `package.json`; profiles; copies and manifests.
- [x] `sdlc_core.py`: `ORIENT_TEAM_LINE`, `has_team_section`, `team_not_defined` and the
  call in `cmd_orient`; golden transcripts checked unchanged.
- [x] Doctrine in the four lenses, each in its own passages; `coordination.md`, `dispatch.md`.
- [x] Eval scenarios; replays 1, 2 and 3 cold, old text against new.
- [x] Derived documents; `vision/rulings.md` rows; E2E script.
- [x] Closure review; merge brief; `mark` the analysed areas; the owner's confirmation of
  the measured cost and decision on the open point of replay 2 (R6).

## Test Strategy

- **Probes kept with the unit** (`harness_team_definition/`):
  `probe_orient_team.py`, run on 2026-11-15 against the skill before this unit, on a
  machine with sibling lenses installed (the probe does not assert their line: on a machine
  without them P1 passes in an easier case) — P0, P0b, P1, P3 and P4 pass, **P2 red** (nothing
  says the team is not defined). Green on P1–P4 is the acceptance of FS7. P1 probes the
  section at its size bound (662 of 700 characters) in a tree where router, registry and
  README are all cut; it does not cover a Hybrid line or a wiring note, which FS7 states.
- **The outcome's own probe** (`REPLAY.md`, fixtures from `build_fixtures.py`, results in
  `RESULTS.md`): cold runs, each one sample, a mid-tier model, fresh context, on the old
  text and on the new; the balanced choice of replay 2 has three samples a side.
  - *Replay 1* (first significant unit, no definition): **red on the old text, green on
    the new** — five questions about the export and none about the team; then the four
    team questions in the same numbered set, default offered, once.
  - *Replay 2* (resume from a summary, five pending choices). What changes the outcome
    is the project, not the text: with no agreement anywhere the old text asks the owner
    the one balanced choice (e); with the agreement written, old and new text decide it
    and report it in one line — the new one reading it in the README section, the old one
    finding the owner's words in the request records. On the tree with no agreement the
    new text asks the four team questions (FS2, an open unit taken up) in 3 runs of 3,
    and asks e in 2 of 3 where the old text asked it in 3 of 3: one run decided it alone,
    by a weighing. Three samples a side do not separate the two; no effect of the new
    text on e is shown in either direction, and the divergent run is put to the owner.
  - *Replay 3* (the section cannot grant): the agent asked and ran no git command, on the
    rules that already existed (integration is the owner's); it never consulted the
    section. The floor of FS5 is not exercised — a ceiling effect, stated.
  So the red-to-green by text is FS2 (replay 1, and the team questions of run 2E) and FS7
  (the probe). FS4's effect comes from the agreement being written; FS5's floors are not
  shown to change behaviour; S1 is measured in the field, and the E2E script carries it.
- **Unit tests** (AAA): FS7 with its three cases, T7; the invariants, one per lens rule,
  each reading the rule's own paragraph so it cannot pass on text that was already there;
  P1–P8. Mutation for the new call in `cmd_orient` (drop it → red).
- **Invariant that fails in a lens the change did not reach:** the support-file triangle
  (P3) once `team.md` exists; `test_drift.py` (P2); and the new per-lens invariants, which
  run in every lens's battery.
- **Eval scenarios:** the three replays, and `team_correction_lands_in_the_section.md`
  (FS6). Only the three replays of the code lens have runs on record (`RESULTS.md`); the
  correction scenario and the three sibling-lens scenarios have none: FS6 and the sibling
  wording rest on the text invariants, and their behaviour is unshown.
- **E2E, human** (`E2E_TEST_team_definition.md`): a real first L3 in a project with no
  section; a session started by another session reads the section; a correction given once
  is found by a later session; this repository's own next L3 asks its owner.
- **Not verifiable here:** S1 over a working day; T5; whether a client re-runs the
  session-start hook after a compaction (as in F-096).

## Diary / Current State

**2026-11-14 - unit opened on a brief from another session.** Request record started with
the owner's two statements as relayed (R1). Vision placement put to the owner as CONTESTED
(r3 against r40-r42), with eight other opening proposals, in one numbered set. Id moved
from F-097 to F-098: F-097 was taken by an uncommitted unit in another worktree.

**2026-11-15 - owner's answers; base moved; probes and baseline.** Once per project (R2);
the first occasion is the first L3 (R3); the other eight proposals accepted, ruling and
north star included (R4). Branch fast-forwarded to the local `main` that holds F-096.
Inventory of the four lenses by a read-only subagent (`INVENTORY.md`). Probe written, P2
red; replays run cold on the old text (`RESULTS.md`).

**2026-11-15 - design review: FAIL, FAIL, PASS at the cap, five warnings standing; design
approved (R5).** Row in `audit/reviews/REVIEW_LOG.md`. The owner approved the design with
the warnings to correct, admitted the orientation line, accepted the cost without the
`elicitation.md` sentence, and chose the wider reading of the default. Four of the five
warnings are corrected in this text and in `REPLAY.md` (confinement wording in P1 and T7,
the per-tree pass criterion and run 2A as the baseline, Ledger row 3, the cost row); the
line budget is not met (the text is over 500 lines). These corrections and the removal of
the `elicitation.md` edit follow the last review round: the closure review reads them.
The unit is under coordination since 2026-11-15 (`REQUEST_honest_signals.md#R13`): F-097
landed on `main` first.

**2026-11-15 - implemented on the `main` that holds F-097.** RED first: seventeen new
tests, sixteen red (the seed test is a preservation and was green). `sdlc_core.py`:
`ORIENT_TEAM_LINE`, `team_not_defined`, one call in `cmd_orient`; the confinement test
now expects the one new confined read. `team.md` written and registered (shared manifest,
four profiles, four `package.json`); `dispatch.md` and `coordination.md` cite it; one
paragraph in each lens's `SKILL.md`, one sentence above each README template block, one
paragraph in each `ENFORCEMENT.md` §4. Deviations from the approved design, all toward
less text: no row in the write-trigger tables; the template sentence sits above the block,
not under it. Probe P1-P4 green. Eval scenarios added (four in the code lens, one in each
sibling). Replays run cold on the new text (`RESULTS.md`): replay 1 green, and green again
on the final text; replay 2 as the design expected with the agreement written; without it
the team questions in 3 runs of 3 and the balanced choice asked in 2 of 3 (old text: 3 of
3), not separated by the samples; replay 3 passes without exercising the floor. Measured cost above the estimate the owner
accepted for `team.md` (5,020 bytes against «Circa 3,5 KB»): to be confirmed by the
owner. Rulings rows r49 and r50 written.

**2026-11-15 - closure review: rounds 1 and 2 FAIL.** Findings and their disposition are
in the review log row; what changed in the design's own statements is above (the cost
section, T9, FS6's acceptance, FS7's cut). `team.md` is 4,950 bytes before the round-2
correction of its size sentence; the cost section carries the final figure.

**2026-11-15 - closure review PASS at the cap (FAIL, FAIL, PASS), five warnings standing;
committed on the owner's word (R6).** Rows in `audit/reviews/REVIEW_LOG.md`. Final tree:
batteries code 687, knowledge 1000, marketing 703, course 693, all OK; node tests 76 pass;
`check` CLEAN. `E2E_TEST_team_definition.md` and `MERGE_REVIEW_team_definition.md` written;
the brief lists the standing warnings, none corrected after the last round. The owner
confirmed the cost as measured and accepted the divergent replay run as it stands, to be
watched in the field (R6). The unit stays open until `main` holds it: the fast-forward is
the coordinator's, on the owner's yes given to it. Not done here: the release.
