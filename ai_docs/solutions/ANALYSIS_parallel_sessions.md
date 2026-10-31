---
id: F-088
feature: Coordinating parallel sessions on one repository
status: COMPLETED
level: L3
start_date: 2026-10-31
end_date: 2026-10-31
---
# Feature Analysis: coordinating parallel sessions on one repository

**For whom**: the independent design reviewer, then the owner. **To do what**: approve or
reject the rules below, and their cost, before any doctrine or code is written. **Answers**:
which failures of parallel sessions the current doctrine leaves open, the smallest rule that
closes each, where each rule lives, what the validator checks. **Does not answer**: which
work runs next or in what order (R5); how the client starts or stops sessions.

Owner statements: `audit/requests/REQUEST_parallel_sessions.md` R1–R11. Evidence and probes:
`harness_parallel_sessions/` — `cases.md` (eight recorded episodes and a control),
`replay.md` (cold-reader replay), `results_old_text.md` (the baseline).

## Objective

The owner runs several sessions on one repository at once — one coordinating, the others each
on a part (chatPNT M155: waves 5, 6 and 8 in parallel, 2026-10-28 → 31) — and asks that the
skill regulate it (R1, R2). F-019 made the workstream registry parallel-safe; F-073 gave each
session its own worktree. The baseline replay shows what neither covers: a shared record
numbered by three writers (C1), a delegate replacing an owner decision (C2), an authorization
that does not travel between sessions (C3), a part stopped mid-closure unseen (C5), one
container restarted under other sessions' running probes (C6), one commit carrying six units
with nothing saying which file was whose (C8). C7 is the reverse: the current text
**forbids** what the owner had to allow — code under test must sit in the checkout the
container mounts, so «each session in its own worktree» cannot hold for the session testing
code (R246 allowed it; no rule does). C0 (a generated file by hand) and C4 (a decision on a
false fact) are the controls: already covered.

## Feature Vision

Serves the Vision's team-lead Actor — «keep several agents … aligned to one intent. Good UX =
one process, one source of truth» (`project_vision.md` §Actors, APPROVED) — and the Goal «keep
understanding durable across sessions». One ANALYSIS, no feature Vision.

**Non-Goal 1 (ruling r3) — a distinction line for each surface near it:**
- *Order of work* held by the coordinator: **out** (R5). `coordination.md` says so and gives
  no procedure for choosing or ordering parts.
- *Lease* (R3, R8): answers «which session is using this resource now», never «who must do
  which unit». It names a resource and a session, never a unit; keeps no queue, no waiting
  list, no order; ends with its release. Proposed ruling **r40**.
- *Commit map*: describes ONE commit the owner asked for — which of the changed files go in
  it, grouped by the unit they belong to. It names files, never units still to do, and orders
  nothing; its `Left out` section says why a changed file is not in this commit, not when it
  will be. Same family as `review-map` (r25), hand-written because the grouping is a
  judgement.
- *Part-closure message*: a part reporting its own state — a document describing itself
  (Non-Goal 1's admitted case) — sent to the coordinator, never collected into a view.

**r26 extended, not replaced (R7).** The record keeps the owner's words. A decision the
coordinator takes under a delegation enters it only as a **labelled entry** no reader can take
for owner words. Proposed ruling **r41**, beside r26. Every lens gets the label (R9).

Out of scope: order or priority of parts (R5); a coordinator the skill elects (R8); starting,
stopping or watching sessions (the client's); a lock a tool enforces; sibling lenses'
`coordination.md` (R9).

Success signals: the replay of `cases.md` gives C1–C3, C5, C6, C8 NOT FLAGGED and C7 FLAGGED
as a violation under the old text (measured), and every case FLAGGED as handled under the new;
a session that is not coordinating never reads `coordination.md`.

## Use Cases / User Needs

- **UC1 (Team lead / owner)** — run several sessions on one repository through one
  coordinating session, without parts overwriting each other's record numbers or resources.
  *Benefit: one process, one source of truth.*
- **UC2 (Team lead / owner)** — delegate decisions to the coordinator and still see, in one
  record, which decisions are theirs and which were taken for them, with no earlier decision of
  theirs replaced. *Benefit: divergence surfaced before merge; durable understanding.*
- **UC3 (Team lead / owner)** — commit several parts' work knowing which file belongs to which
  unit, which are generated, which are shared. *Benefit: one source of truth at merge.*
- **UC4 (Team lead / owner)** — know, when a part stops, what it finished and what is left,
  without asking each session. *Benefit: durable understanding across sessions.*

Grounding: request record, workstream registry, `HANDOFF_*.md`, `index`, `review-map`,
worktree, delegation (`elicitation.md`) — EXISTS. Coordinator, part, lease, delegated entry,
part-closure message, commit map — NEW, declared here.

## Functional Spec

Fires: the unit adds behaviour an agent follows and a check a person runs.

- **FS1 — trigger and roles.** The rules apply while more than one session works on the same
  repository **and** the owner has named the coordinating session in a request-record entry.
  Without that naming no session coordinates: each works in its own worktree, asks the owner
  before using an exclusive resource, and appends to no record it does not own. A part is a
  peer session the owner can talk to and that follows the whole skill for its own unit
  (authoring its own design included); it is not a dispatched subagent, whose rules stay where
  they are. A session that is not coordinating never reads the coordination rules; what every
  session does read is counted under Ceremony cost below.
- **FS2 — every record has one writer.** C1 happened because three units wrote one record. A
  part is its own unit: when its triage gives it a request record (the existing L3 trigger; on
  the filesystem in both modes), the part is that record's only writer. The record of the
  shared unit the parts serve — the milestone, the umbrella — is written only by the
  coordinator. Owner words received by a part are recorded before the part acts on them, in
  the record of the unit they settle. Words settling the part's own unit go to its own record.
  Words settling the shared unit are appended verbatim to the part's own record, labelled as
  received for that unit, and sent to the coordinator, which enters them verbatim in the
  shared record citing the part's entry. A part with no record of its own (below L3) sends
  them and acts only once the coordinator has entered them. Every such entry follows every
  rule of the record (verbatim, redaction, the owner told). An artifact of the shared unit
  cites only the shared record: the coordinator enters the words before any such artifact
  relies on them. *Accept*: C1 cannot recur — no record has two writers; an L3 part needs no
  fallback when the coordinator is unreachable, a part below L3 waits for it.
- **FS3 — leases.** Exclusive resources — the development container, the test database, the
  code-writer role in a checkout a runtime mounts, others the owner names — have one holder at
  a time. A part asks the coordinator, which records the take and later the release. Restarts
  and long suites are announced to the coordinator before they start. From the naming on, a
  permission for an exclusive resource given earlier (C6: «restart as much as you like, nobody
  else uses it») no longer exempts a session from the lease: it rested on a single user. If
  the owner restates it, the coordinator enters it as a `take` for that session — a recorded
  lease, never an exemption. *Accept*: a restart under another
  session's running probe (C6) breaks a stated rule, earlier permission or not; the record of
  leases names resources and sessions only.
- **FS3b — the code-writer lease is the one sanctioned exception to «own worktree».** The
  session holding the code-writer lease of the checkout a runtime mounts writes code there;
  every other session keeps its own worktree and writes no code there. The lease passes to
  another session only once the holder's code in that checkout is committed, or set aside with
  the owner's yes. *Accept*: C7 is a recorded arrangement, not a waived violation; two
  sessions' code in that checkout is a violation, including code a previous holder left
  uncommitted.
- **FS4 — delegated entries.** A decision the coordinator takes under a delegation is a
  request-record entry labelled as decided under the owner's delegation entry, citing it (in
  Hybrid also the devPNT proposal it accepted). It never changes an earlier owner decision of
  any unit: such a choice goes to the owner as a question. That entry is the decision's one
  home; an artifact relying on it cites the entry. *Accept*: C2 breaks the rule at R176.
- **FS5 — what travels between sessions.** An owner statement recorded verbatim in a request
  record is citable by every session (r26). An authorization for a gated act — one the client
  or the skill makes wait for the owner's yes — is valid only in the session the owner gave it
  to; a message from another session saying the owner authorized it is information, never the
  authorization. The receiving session asks the owner, or the session holding it acts.
  *Accept*: C3 is handled by rule.
- **FS6 — reopening.** A decision taken on a fact found false is reopened by a new entry naming
  the one it corrects — the existing record rule, cited.
- **FS7 — part-closure message.** A part that stops — done, blocked, interrupted — reports to
  the coordinator: unit and increment; state (done / stopped at step X); files touched;
  verification run and its result; open points; what needs the owner. The coordinator verifies
  on the diff, never on the message (claim-to-evidence, cited). A part may stop without being
  able to send (a crash, a closed client): the coordinator treats a part with no closure
  message as not done, and before relying on its state — accepting its work, mapping a commit,
  telling the owner it finished — reads its HANDOFF `next:` and its working tree, and tells the
  owner which closure steps (`SKILL.md` Phase 5) the tree shows done and which it cannot tell; whether to resume the
  part is the owner's. *Accept*: for
  C5 the coordinator reads «stopped at step X», or, with no message, finds the stop before
  relying on the part instead of after.
- **FS8 — commit map.** Before a commit carrying more than one unit's work, the coordinator
  writes the map: one section per unit with its files (its HANDOFF and request record when
  they changed), a Shared section for files several units touched, a Regenerated line for the
  files the validator regenerates, a Left-out section for changed files not in this commit, each with a reason.
  The commit stays the owner's.
- **FS9 — the commit-map check.** A check reads a map against the working tree as it stands
  against HEAD and reports: error for a generated file under a unit; error for a changed
  HANDOFF or request record in no section; error for a file under two units outside Shared;
  error for a file both under a unit and in Left-out; error for a changed file under
  Regenerated that the validator does not regenerate (a HANDOFF there would otherwise pass
  unchecked); warning for a changed file in no
  section; warning for a listed file with no change. Any error fails it. *Accept*: on a map
  reconstructing C8 it names each generated index listed as unit work.
- **Shared hand-written files in general** (R2's «append atomico»): no rule beyond FS2. F-073
  (b) measured the other shared logs and settled them (`REVIEW_LOG.md merge=union`); the
  collision observed here is the request record's numbering, which FS2 closes.

## Interface Contract

Fires: a new CLI command, two new document forms, a new heading label in an existing document,
a fixed message form.

1. **Actors + surfaces.** Owner: reads the request record, `audit/leases.md`, commit maps;
   runs or asks for `sdlc_check.py commit-map MAP`. Coordinator (software actor, acting for the
   owner): writes record entries, `audit/leases.md`, commit maps; reads part messages. Part
   session: asks for leases, sends owner words and closure messages. Idioms reused: the
   record heading `### R<n> — date — label`, append-only, `[ERROR]`/`[WARN]` lines and exit 1
   of `check`, `review-map`'s table and path escaping.
2. **Flow.** Lease: part asks → coordinator appends `take <resource> — <session> — date` to
   `audit/leases.md` → part works → `release …` appended. Naming: the owner's words naming the
   coordinator are an entry in the record of the unit the owner was in; `audit/leases.md`
   opens by citing it. Commit: owner asks → coordinator writes the map (template in
   `templates.md`) → runs `commit-map` → the validator, reusing `review-map`'s change list
   (base HEAD) and generated-file detection, prints findings → coordinator fixes or explains →
   owner commits. Delegated decision: the owner's delegation is an entry of the shared record →
   the coordinator decides within it and appends a delegated entry citing it (in Hybrid also
   the devPNT proposal it accepted) → a choice that would change an earlier owner decision goes
   to the owner as a question instead → artifacts cite the entry → the owner reads it in the
   record, told apart from their own words by the label; a review flags one citing no
   delegation. Owner words for the shared unit received by a part: the part appends them, with
   the received label, to its own record → sends them to the coordinator → the coordinator
   appends them verbatim to the shared record citing `REQUEST_[part].md#R<n>` → artifacts of
   the shared unit cite the shared entry. A part with no record of its own sends the words; the
   coordinator's shared entry names that part and the date received, and the part acts once it
   exists. Part closure: the part stops → sends the message with
   its six fields → the coordinator checks each claim on the diff and the run output → tells
   the owner what is done, what is left and what needs them; the owner sees the coordinator's
   verified account, with the message as its source.
3. **Affordances.** Templates in `templates.md`: the lease line; the delegated-entry heading
   `### R<n> — date — decided under delegation R<m> — <what it settles>`; the received-entry
   heading `### R<n> — date — received for <unit> — <what it settles>`; the commit map.
   `commit-map --help`.
4. **Feedback.** One line per finding with path and rule, then a total; exit 0 clean, 1 on any
   error; `[ERROR]` and exit 1 on an unreadable map or a root outside git. No
   `audit/leases.md`: no lease taken, not an error.
5. **Constraints touched.** `review-map` unchanged; the registry stays without holder (P4).
6. **Flags.** The check sees one working tree, not other worktrees: said in its help.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| isolate one session's files from another's | EXISTS | SKILL.md Phase 4 «Isolate the work» (F-073 (c)) | re-read: own worktree; no branch switch/stash/reset/`index` in a shared checkout |
| keep one writer for a shared record's numbers | INADEQUATE | request record template: append-only, any session numbers | `templates.md` §REQUEST: no rule on concurrent writers; C1 |
| know which session holds a non-file resource | MISSING | — | grep lease/container/database/exclusive over the skill's `*.md`: none; F-073 isolates files only |
| record a delegated decision apart from owner words | INADEQUATE | `elicitation.md` «Delegated»; record template «never enter the record» | delegated choices live in artifacts; chatPNT recorded them in the record with «per delega» in prose, no fixed label |
| tell a relayed authorization from a given one | MISSING | — | grep «another session»/authoriz over the skill's `*.md`: SKILL.md:166, :210, :244, architect.md:17, debugging.md:46, :79, elicitation.md:119, vision.md:211 — none on an authorization relayed between sessions |
| classify a change's files as generated / evidence / design | EXISTS | `sdlc_check.py` `_changes`, `_generated_set`, `classify_path` | re-read: `index` on a throwaway copy decides GENERATED |
| check a commit map | MISSING | new `commit-map` command, a consumer of the three above | no such command; `review-map` classifies, it does not check a declared grouping |

## Guide check

- CURRENT guide covering what this touches: `GUIDE_skill_family_changes.md` (copies count once).
- High-complexity component understood here that no guide covers: no.

## Impact

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/coordination.md` | ADD | FS1–FS8; code lens only (R9) |
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | support-file line; Phase 4 «Isolate the work»: FS3b exception and pointer; Write Triggers, `REQUEST_[feature].md` row: a pointer «under coordination, see `coordination.md`». The record-before-act rule itself is unchanged — every part appends to its own record first (FS2) — so `templates.md` §REQUEST, which restates it, needs no change to it |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | §REQUEST: the delegated-entry and received-entry headings, and one sentence that a delegated entry is a coordinator's decision, never an owner statement (the «declared assumptions … never enter the record» sentence stays as it is); lease line; commit-map template |
| `distributions/{kb-agentic-skill,mkt-agentic-sdlc,course-creator}/skills/*/templates.md` | MODIFY | the same two headings and sentence (R9) |
| `skills/agentic-sdlc-skill/review.md` and its three copies | MODIFY | owner-statement clause: a finding for a delegated entry citing no delegation or replacing an owner decision, and for a shared-unit artifact citing a received entry instead of the shared record (identical ×4) |
| `skills/agentic-sdlc-skill/elicitation.md` and the three lens files (`distributions/*/skills/*/elicitation.md`, not shared: same «Delegated» paragraph in each) | MODIFY | «Delegated»: the coordinator's delegated decision lives in the labelled entry; the artifact cites it |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` and `distributions/*/skills/*/scripts/shared_manifest.json` (×4) | REGENERATE | `shared_files.py --update` after the shared edits, or `test_drift.py` fails |
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` | MODIFY | `support_files` + `coordination.md`; `cmd_commit_map` beside `cmd_review_map`; `main` routes it; help text |
| `skills/agentic-sdlc-skill/scripts/test_review_map.py` | MODIFY | `commit-map` tests (code-only file; the shared invariants file would break the sibling batteries) |
| `skills/agentic-sdlc-skill/scripts/test_chronology.py` and its three copies (shared ×4) | MODIFY | a labelled heading parses (P1) |
| `package.json` | MODIFY | `files` + `coordination.md` |
| `README.md` | MODIFY | support-files bullet and Runtime Shape tree (`audit_plan.md` duty) |
| `CHANGELOG.md` | MODIFY | at release |
| `distributions/{kb-agentic-skill,mkt-agentic-sdlc,course-creator}/CHANGELOG.md` | MODIFY | at release: the label, review and elicitation edits ship in each package. The three distribution `README.md` files need no change: no support file is added to those lenses |
| `ai_docs/strategic/skill_family_agent_workflows.md` | MODIFY | request-record paragraph: one writer per record under coordination, the delegated and received labels (all four lenses); a line for `coordination.md` in the code lens (`audit_plan.md` duty on `skills/` and `distributions/`) |
| `ai_docs/strategic/architecture.md` | MODIFY | Component Map: a Commit map row beside Review map |
| `ai_docs/vision/rulings.md` | MODIFY | r40, r41, on approval |
| `ai_docs/solutions/harness_parallel_sessions/` | ADD | cases, replay, both results |

`hybrid.md`: no delta — FS4 names the proposal id, which `hybrid.md`'s rule (an approval given
in devPNT is named by its proposal) already asks. `dispatch.md`: no delta — FS1 states a part
is not a dispatched subagent.

### Preservation constraints

| id | bound to | callers | must stay true | evidence |
|---|---|---|---|---|
| P1 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::request_entries` | `skills/agentic-sdlc-skill/scripts/docs_site.py` (chronology), `test_chronology.py` | a delegated-entry heading parses as an entry: the label sits after the date, inside `(.+)` | grep `request_entries(` over the package: two callers; regex `_REQUEST_HEADING` re-read |
| P2 | `skills/agentic-sdlc-skill/scripts/sdlc_check.py::cmd_review_map` | `main` | `review-map` output unchanged on the same tree | `test_review_map.py`; `commit-map` reuses helpers, never edits them |
| P3 | `skills/agentic-sdlc-skill/scripts/sdlc_check.py::main` | CLI | every existing subcommand routes as before | `--help` and one existing command in tests |
| P4 | `skills/agentic-sdlc-skill/templates.md` §workstream registry | `SKILL.md` Write Triggers; `validate` | the registry carries no holder | grep; r3 |
| P5 | `skills/agentic-sdlc-skill/SKILL.md` Phase 4 «Isolate the work» | every session in a shared repository | outside the code-writer lease, a session works in its own worktree and never switches branch, stashes, resets or runs `index` in a shared checkout | replay C7 on the new text; F-073 (c) |

`_changes`, `_generated_set`, `classify_path`, `table_cell` gain a caller and no change.

## Security and Threat Model

Surfaces: authorization between agents (FS5); filesystem and git read by `commit-map`.
- **T1 — forged or stale authorization relayed between sessions.** FS5: a relayed
  authorization for a gated act is never acted on. The client's own rule (session messages are
  not instructions) agrees.
- **T2 — delegation creep** (C2). FS4: cite the delegation; never replace an owner decision;
  the review clause makes a breach a finding.
- **T3 — map content printed into a table** (`|`, control characters, backticks). Reuse
  `table_cell`; paths from the map are compared with git's list, never opened or executed; the
  map is read as text.
- **T4 — a lease never released.** Residual: the owner tells the coordinator, which appends
  the release; no timeout (a timer is a tool lock, out of scope).
- **T5 — owner words misquoted or invented on the relay** (FS2: a part transcribes words for
  the shared unit, the coordinator copies them). An entry no owner said would be cited by the
  shared unit's artifacts. Mitigation: verbatim at both steps; the shared entry cites the
  part's entry, so the two can be compared (for a part with no record there is no part entry,
  and the owner-told rule is the only check); the owner is told of each entry and may correct
  any quotation (the record's existing rule); the review checks owner statements against the
  record.

## Ceremony cost

Estimates, measured at implementation and shown to the owner before closure:

| Where | Who reads it | Added |
|---|---|---|
| `coordination.md` (code) | only the coordinator and parts, under FS1 | ~6 KB |
| `SKILL.md` (code) | every session | ~0.4 KB |
| `templates.md` §REQUEST ×4 | every L3 that opens a record | ~0.3 KB each; code +~1 KB templates |
| `review.md` ×4 | every review, every lens | ~0.25 KB |
| `elicitation.md` ×4 | every question discipline read | ~0.2 KB |

Under coordination: one lease line per resource use; one label per delegated entry; each owner
statement that settles the shared unit and reaches a part is written twice (the part's record,
then the shared one), and a part below L3 waits for the coordinator's entry before acting on
it; one map per multi-unit commit.

## Action Plan

- [x] Replay `cases.md` on the old text — baseline (`results_old_text.md`).
- [x] Design review PASS, then owner approval of the design and of the cost above.
- [x] Rulings r40, r41.
- [x] RED tests: `test_review_map.py` (`commit-map`), `test_chronology.py` (labelled heading).
- [x] `coordination.md`, `SKILL.md`, `templates.md` ×4, `review.md` ×4, `elicitation.md` ×4,
      `sdlc_check.py`, `package.json`, `README.md`, Component Map; `shared_files.py --update`.
- [x] Replay on the new text (cold reader) — green; bytes measured.
- [x] Batteries ×4, `node scripts/test_clients.js`, `check`; E2E script, closure review, merge
      brief.

## Test Strategy

- Replay harness: cold reader, old then new text, verdicts kept in `harness_parallel_sessions/`;
  FS1's «never reads `coordination.md`» checked as: every naming of `coordination.md` in
  `SKILL.md` (support-file line, Phase 4, the REQUEST Write Trigger) is conditional on
  coordination.
- `commit-map` in `test_review_map.py`, on a temporary git repository: generated file under a
  unit (error), changed HANDOFF in no section (error), file under two units outside Shared
  (error), file under a unit and in Left-out (error), changed authored file under Regenerated
  (error), unlisted change (warning), listed file
  with no change (warning), clean map (exit 0), C8 reconstruction (names the indexes), hostile
  path characters escaped, base is HEAD.
- `test_chronology.py`: a delegated-entry heading and a received-entry heading parse (P1).
- Wiring: `test_support_files_wired`, `test_every_support_file_on_disk_is_declared` per lens;
  `test_drift.py` after `shared_files.py --update`; `node scripts/test_clients.js` (templates.md
  parsed by `scripts/lib.js`); full battery in all four packages.

## Diary / Current State

**2026-10-31 — opened.** Unit moved here from a session started in chatPNT (R4, R6). Order of
work out (R5); leases in `audit/leases.md` (R3), kept by the owner-named coordinator (R8);
delegated decisions in the record with a label (R7); label in every lens, `coordination.md` in
the code lens (R9). Cases located in chatPNT M155; C0 not located, kept as control.

**2026-10-31 — baseline replay.** `results_old_text.md`: C1–C3, C5, C6, C8 NOT FLAGGED; C0, C4
covered; C7 FLAGGED as a violation — the worktree rule forbids what R246 allowed, hence FS3b.

**2026-10-31 — design review.** Three rounds (REVIEW_LOG): FAIL; PASS with four WARN; FAIL on
one BLOCK — the FS2 fallback named a HANDOFF Diary the template does not define. Cap reached;
the fix the reviewer named is applied, unreviewed, and goes to the owner with the design.

**2026-10-31 — round 4 (R10).** FAIL: the Diary fallback has no home in a Hybrid-mode unit, which has no ANALYSIS. Mechanism, not the fallback, changed: C1 came from three units writing one record, so FS2 now gives every part its own record (one writer each) and the shared record to the coordinator alone; owner words for the shared unit are recorded first in the part's own record. The Diary fallback is gone. W1–W4 answered in FS2, the SKILL.md Impact row and the Test Strategy.

**2026-10-31 — round 5 (R11: no approval without a clean PASS).** Fresh reviewer, whole design.
FAIL: BLOCK — `strategic/skill_family_agent_workflows.md` missing from the Impact (the
`audit_plan.md` duty on doctrine changes). WARNs: the received label had no home and a
shared-unit artifact could rest on a part's entry; the double entry was uncounted and a part
below L3 had no record to write to; T4 had the owner writing the coordinator-only leases file;
the relay surface had no threat row; FS1/FS8 named files; UC2/UC4 had no walked flow; the
Ledger grep cell was wrong; the templates row widened a sentence about declared assumptions;
the REVIEW_LOG rows carried counts only. All taken: Impact rows added (also the three
distribution CHANGELOGs), FS2 restated, IC flows and both headings, T4 fixed, T5 added, cost
line, Ledger cell, templates row left the assumptions sentence alone, FS9 edge cases, log rows
completed. The SKILL.md row shrank to a pointer: under the new FS2 the record-before-act rule
holds unchanged, so no exception and no second copy exist.

**2026-10-31 — round 6 (scoped, same reviewer).** All 13 round-5 findings ADDRESSED; PASS with
one new WARN (W10): the below-L3 relay path was not walked in the IC, T5's comparison had no
part entry to compare there, the wait was uncounted. Taken: one clause each in IC §2, T5 and
the cost line.

**2026-10-31 — round 7 (scoped).** W10 ADDRESSED, no new finding: PASS with nothing open. The
design and its cost go to the owner for approval.

**2026-10-31 — implementation.** Approved (R12); rulings r40, r41 written. RED: the 13
`commit-map` tests failed before `cmd_commit_map` existed; the labelled-heading test in
`test_chronology.py` passed already (P1 holds, pinned). GREEN: `test_review_map.py` +
`test_chronology.py` 64 tests OK. Doctrine written as designed. Bytes added, LF as
packaged: `coordination.md` +5,949 (est. ~6 KB); `SKILL.md` +321 (~0.4 KB); `templates.md`
code +1,594 (~1.3 KB), each other lens +627 (est. ~0.3 KB: over, the labelled-entries
paragraph carries both headings); `review.md` +214 ×4 (~0.25 KB); `elicitation.md` +229 ×4
(~0.2 KB); total +11,517. New-text replay (`results_new_text.md`): every case FLAGGED; the
reader named three residuals outside the design — a part halting without sending
anything (C5), a standing delegation given before the naming (C6), uncommitted code of a
previous code-writer (C7) — for the owner.

**2026-10-31 — amendment (R13).** The new-text replay named three residuals and the closure
review one gap; the owner took all four into this unit. FS3: an earlier permission for an
exclusive resource stops exempting a session from the lease once a coordinator is named (C6).
FS3b: the code-writer lease passes only once the holder's code is committed or set aside with
the owner's yes (C7). FS7: a part with no closure message is treated as not done; the
coordinator reads its HANDOFF and working tree before relying on it (C5 — the real episode was
a silent stop). FS9: a changed authored file under Regenerated is an error (W3).

**2026-10-31 — amendment closed.** Scoped review rounds 3–4 of the closure row: W5 (a restated
permission read as an exemption) fixed — it becomes a `take`; the first C5 replay found the
amendment partial, so the coordinator now also tells the owner which Phase 5 steps the tree
shows done and which it cannot tell, resuming the part left to the owner. C5–C7 replayed cold
on the final text: FLAGGED (`results_new_text.md` §Amendment). RED → GREEN for the Regenerated
error (65 OK). Cost of the amendment: `coordination.md` 5,949 → 6,941 LF bytes (+992 against
~0.5 KB priced in R13); total doctrine +12,509.

**2026-10-31 — closed: COMPLETED, merged into main on the owner's word (R14, R15).** Committed
as bc30816c (implementation), then the closure commit: the merge note no longer claims
uncommitted changes of another session on `main` — they were committed in `788e74ee`, the
branch's base, and the note was never re-checked; `mark` on `skills/`,
`skills/agentic-sdlc-skill/`, `distributions/`; HANDOFF deleted. Fast-forward into `main`.
`check` CLEAN on `main`. (In the worktree `stale` also named `scripts/`: its reference is a
timestamp, compared with file mtimes, and a fresh checkout has new mtimes — not a real change.) No ADR: the decisions are rulings
r40 and r41, and `commit-map` reuses `review-map`'s classifiers. Left for the release:
CHANGELOG ×4.
