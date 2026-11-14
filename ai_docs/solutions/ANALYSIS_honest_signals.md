---
id: F-096
feature: Honest signals - closure, open workstreams and resume say what they measure
description: F-096 - three field cases of 2026-11-14 where the method was followed and the defect passed anyway (a guide left false under a CLEAN check, forty open workstreams behind an unread warning, a resume from a summary that lost half a unit's scope), and the changes that make each signal state what it measures.
status: COMPLETED
level: L3
start_date: 2026-11-14
end_date: 2026-11-14
domain: code
---
# Feature Analysis: Honest signals (F-096)

## Objective

Three cases from one working day on a production project, recorded in
`harness_honest_signals/`. In each the agent followed the method and trusted a signal
that did not measure what it seemed to measure:

1. **A guide left false at closure** (`case_guide_false.md`). After a production release
   the agent appended a row to the change log at the bottom of an operative guide and
   closed the node. Three sentences above it still described the earlier state. `check`
   printed `CLEAN`. The owner found it. The hand correction that followed fixed two
   sentences and missed the third.
2. **Forty open workstreams** (`case_registry_40.md`). The registry warned about the count
   at every regeneration and nobody acted. Nine of the 40 registry sources declare in their
   own `status:` that the work is finished; a tenth file says the same and, having no
   `workstream:`, is not a source at all.
3. **A resume that lost a unit's scope** (`case_compaction.md`). After a compaction the
   summary named an active milestone only for the topic under discussion. Asked whether a
   function had been built, the agent searched code and logs five times and answered "I
   take it that it belongs there"; the milestone's vision, one read away, held the answer.

The unit changes the skill family so that the same three situations end differently for
every user, on every client, with or without devPNT. Scope and source:
`REQUEST_honest_signals.md` R1 (the field report), R2 (points 2, 3 and 4 of it), R8 (all
four lenses).

## Feature Vision

**Benefit.** The owner is not the last check. Whoever follows the method cannot close
work, or resume it from a summary, on a signal that measures something other than what
it appears to measure (the report's north star, R1).

**Alignment with `vision/project_vision.md` (APPROVED, v9).** Advances the Goal *keep
understanding durable across sessions* ("nothing load-bearing lives only in a transcript")
and the solo-developer Actor's *never re-explaining the project across sessions*. Protects
Success Signal 2 (*closure is mechanically clean*) under new load: it keeps the command and
states its coverage, the way Signal 3 already states the limit of the guide hash.

**Admission, part by part.**

- *The closed-workstream finding* (FS4) operates in Non-Goal 1's territory. It names one
  file whose own `status:` field contradicts its existence. It computes no count, order,
  age or selection for work, starts nothing and assigns nothing. Precedent: r35c (a
  validator finding on named files). A cap on opening workstreams was the alternative and
  falls on r1; the owner ruled for the finding (R4). New row in `vision/rulings.md`.
- *The line added to the session orientation* (FS7) widens what `orient` injects into
  every session. Under r4 that growth is ruled again, not inherited, as r32 and r44 were
  for the per-turn line. The owner ruled for one constant line, printed always, that reads
  nothing from the session or the hook event (R7). New row in `vision/rulings.md`.
- *The coverage line of `check`* (FS3) and *the handoff template sentence* (FS5) are
  maintenance: purpose, actors and surface unchanged.
- *Ceremony budget (Non-Goal 3).* Two new duties, neither removing one of comparable cost,
  both accepted by the owner explicitly:
  - at **L2 and L3 closure**, the whole re-read of each impacted document and its
    declaration in the closure message (FS1, FS2) — R3;
  - on **resume from a summary, for a unit with an open workstream** (every L3, and an L2
    that keeps a handoff), the re-read of its request record and vision before answering
    about it or acting on it (FS6) — R6.
  L1 gains nothing: it writes no documents, runs no `check` and has no open workstream. The
  orientation line is read at session start at every level; its cost is the line itself, 224
  characters (R7 was asked at "about 200").

**Actors** (project Vision `## Actors`): solo developer using an AI agent; team lead
needing governance; practitioner in a non-code domain (the three sibling lenses, R8).

**Non-goals of this unit.** Changing when or how a client compacts. Rules that name a
client's limits. Any cap, count or order on workstreams. New mandatory documents. Reading
the hook event in `orient`. The truncated report between sessions (report point 1, its own
unit) and devPNT's read tools (point 5, devPNT's).

**Success signals** — the report's, for these three points:

- S1. A closure where a guide holds a sentence about the earlier state does not pass with
  the sentence unrewritten. Baseline: passed, `CLEAN`.
- S2. In a project above the registry's size the number of open workstreams goes down.
  Baseline: 40 on 2026-11-14.
- S3. After a compaction, asked about a part of an active unit the summary does not name,
  the agent answers citing the unit's vision at the first question. Baseline: at the second.

## Use Cases / User Needs

- **UC1 (solo developer; practitioner in a non-code domain)** — closes work that changed
  what a guide or canonical document describes, and needs the document to read true
  afterwards without being asked. *Benefit: understanding stays durable; the owner is not
  the last check.*
- **UC2 (solo developer, team lead)** — reads the `check` verdict at closure and needs to
  know what a clean verdict covers, so a form check is not taken for a fact check.
  *Benefit: divergence visible before merge.*
- **UC3 (team lead)** — regenerates the workstream registry (EXISTS: `audit/handoff.md`,
  generated by `index`) and needs each workstream file left behind after its work closed
  to be named, so closing it is one gesture. *Benefit: one source of truth.*
- **UC4 (solo developer; practitioner in a non-code domain)** — continues a session whose
  context was replaced by a summary and asks about an open workstream; needs the answer to
  come from that unit's own documents. *Benefit: never re-explaining the project across
  sessions.*

Product names: `check`, `validate`, `index`, `orient`, workstream registry,
`HANDOFF_[feature].md`, request record, guide router — all EXISTS, in the product's own
terms. NEW, declared: the `[scope]` line (UC2), the closed-workstream advisory (UC3), the
resume line of the orientation (UC4), the `re-read whole:` line of a closure message (UC1).

## Functional Spec

**FS1 — impacted documents are re-read whole at closure (UC1).** At L2 and L3 closure, a
document is *impacted* when the change edited it or changed what it describes; the guides
the router verdict named for this work are always candidates. Each impacted document is
read from its first line and every sentence describing the state before the change is
rewritten, so the document reads true as of now. An added row, dated note or log entry
never corrects the sentences above it. Cases:
- no document impacted → the closure message says so (FS2);
- a guide distilled from the owner's indications, whose source did not change → the
  sentences are still rewritten, by the same route any other correction of that guide takes;
- a document too large to absorb → it is marked superseded rather than left current and
  wrong.

**FS2 — the closure message names what was re-read (UC1).** It carries one line:
`re-read whole: <documents>` or `re-read whole: none impacted`. A closure message without
the line is read as "not re-read".
*Acceptance:* given the recorded guide (three state sentences, one appended log row) and
a closure after the release, the agent rewrites all three sentences and names the guide.

**FS3 — the `check` verdict states its coverage (UC2).** Every `check` run, in every lens,
prints after its verdict one `[scope]` line: the check covers the form of the documents
(lifecycle headers, generated files against their sources, recorded snapshot hashes) and
does not read whether their sentences are still true — re-read what the change touched.
Constant text, clean verdict or not; it never changes an exit code.
*Acceptance:* the recorded guide in a minimal tree gives a clean verdict followed by the
`[scope]` line.

**FS4 — a workstream file that declares its work closed is named (UC3).** A workstream
source whose `status:` begins with `DONE`, `COMPLETED` or `CANCELLED` (any case, quotes
ignored) contradicts the rule that the file is deleted at closure. `validate` reports each
such file once, as an advisory naming the file and the gesture: move what is still worth
reading to the Diary or a guide, delete the file, run `index`. `index` prints the same
names in one line, next to the registry it just wrote. An advisory never fails a build,
`--strict` included. Cases:
- status in free text (`Implementato (DONE)`, `COMPLETATO`) → not matched; stated as a limit;
- a file with no `workstream:` → not a source, untouched;
- no closed file → nothing printed;
- the marketing lens on a shared docs root → still once per file.
*Acceptance:* on the 43 recorded frontmatters, the nine sources that declare a closed status
are named, each once; the tenth file, with no `workstream:`, is not.

**FS5 — a closed workstream is never written as a status (UC3).** The handoff template
says it: closing is deleting. Work finished in code that waits on the owner (a commit, a
deploy, a manual test) is open, keeps a lifecycle status, and names that act as its next
step.
*Acceptance:* the template text of every lens that carries a handoff section states the
rule; an invariant test reads it.

**FS6 — on resume from a summary, the unit's own documents answer (UC4).** When the
context an agent works from is a summary (a compaction, a pasted recap, a brief), before
answering a question about a unit with an open workstream or acting on it, the agent
re-reads that unit's request record and its vision — the analysis's feature vision, a
feature vision file, in Hybrid the milestone vision — and answers citing it. A summary
keeps the topic of the moment, not the unit's scope. Level: units with an open workstream;
L1 is untouched.
*Acceptance:* given the recorded summary and the owner's first question, the agent reads
the milestone vision before answering and cites it.

**FS7 — every session orientation carries the resume rule (UC4).** The orientation the
session-start hook emits contains one line stating FS6: constant text, printed whenever
the orientation is, taking nothing from the session or the hook event. A client that re-runs the hook
after a compaction therefore delivers the rule exactly when it applies; a client that does
not leaves FS6 a written duty.
*Acceptance:* `orient` on any project with a docs root prints the line, within the output
bound it has today; with no docs root it prints nothing, as today.

## Interface Contract

Surfaces touched, all existing; no new command, flag or file.

| Use case | Actor acts / perceives through | Flow (responsibility level) | Feedback |
|---|---|---|---|
| UC1 | the closure message of an L2/L3 unit | the agent re-reads each impacted document and rewrites it; each lens's closure doctrine owns the duty | the line `re-read whole: …` |
| UC2 | the `check` output of each lens's entry point | the check runner prints its verdict — `check: CLEAN (…)` / `check: NOT CLEAN (…)` in the code, knowledge and course lenses, `[OK] check clean` / `[FAIL] check: …` in the marketing lens; the check-notes printer, which every lens already calls after the verdict, adds the coverage line | `[scope] …` after the verdict, in all four; exit code unchanged |
| UC3 | `validate` and `index` output | the registry reader lists the workstream sources; the closed-status reader returns the ones declaring a closed status; the validator prints them through its advisory channel; the registry writer repeats the names after regenerating | per file, the validator's existing advisory prefix — `[note]  …` from the spine, `[advisory] …` from the marketing overlay when it validates its own docs root; from `index`, one `[note]` line; exit codes unchanged |
| UC4 | the session orientation the SessionStart hook injects | the orientation emitter prints its fixed head; the resume line is part of that head | one constant line after the triage line |

Idioms reused: the spine's `[note]` advisory channel and the marketing overlay's
`[advisory]` one, each as it is; the one-line declared verdict (the router verdict's form,
reused for `re-read whole:`). **New idiom, declared:** the `[scope]` prefix — no existing
prefix says "what this command does not check", and `[note]` is taken by findings.

Architectural constraints touched: the golden transcript (`fixtures/golden_baseline.txt`)
pins the `check` and `orient` output byte for byte and is regenerated with the change; the
orientation's size bound (`ORIENT_MAX_TOTAL_CHARS`, with the reserve left to the knowledge
layer's append) holds.

Feasibility flags from the walk: none open.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| name a workstream source that declares its work closed | INADEQUATE | `sdlc_core.py`: `list_workstreams` reads the sources; `cmd_validate` and `rc_registry` only count them against `REGISTRY_CAP`; nothing reads `status:` | `probe_closed_handoffs.py`: 43 files, 9 sources declare closed, 0 named |
| state what the check verdict covers | INADEQUATE | `sdlc_core.py::print_check_notes`: prints the hook and review-log notes only | `probe_signals.py` P2: clean verdict on three false sentences, no `[scope]` line |
| tell the agent what to re-read on resume | MISSING | — | grep `compact`, `summar`, `resum` over the skill's `*.md`: `coordination.md` §Who coordinates (the coordinator's own files) and `dispatch.md` §Ledger protocol summary (the dispatch ledger); neither covers an open unit's scope. `probe_signals.py` P4 |
| re-read an impacted document whole at closure | INADEQUATE | `SKILL.md` Phase 5 "Update only the documents actually impacted"; the whole-re-read rule exists for an ANALYSIS only (Rule Zero L2 row, Write Triggers) | grep `appended`, `rewrit`, `current state` over `guides.md`: no rule |

No new component: every row extends an existing one inside its present contract.

## Guide check

- CURRENT guide covering what this touches: `GUIDE_skill_family_changes.md` (copies count
  once; read whole). `GUIDE_hooks.md` governs hook installation and event normalization,
  which this design no longer touches: `orient` reads no event and no wiring changes.
- High-complexity component understood here that no guide covers: no.

## Impact

**Shared core** — authored in the code lens, copied verbatim into the three distributions
(`shared_files.py`; `test_drift.py` is red until each manifest is regenerated):

- `skills/agentic-sdlc-skill/scripts/sdlc_core.py` — MODIFY: `closed_workstream_advisories`
  (new, over `list_workstreams`); `cmd_validate` adds its result to the advisories it
  prints; `rc_registry` prints one `[note]` line with the names after writing the registry;
  `print_check_notes` prints the `[scope]` line; `cmd_orient` adds the constant resume line
  to its head.
- `skills/agentic-sdlc-skill/guides.md` — MODIFY §6: any edit of a guide ends with a whole
  re-read (FS1).
- `skills/agentic-sdlc-skill/scripts/test_session_start.py`, `test_merge_safety.py`,
  `test_skill_invariants.py` — MODIFY: tests for FS3, FS4, FS5, FS7.
- `skills/agentic-sdlc-skill/scripts/shared_manifest.json` and its three copies —
  regenerated.

**Golden transcript** (pins `check` and `orient` output; `test_golden_regression.py`
replays it and needs no edit):

- `skills/agentic-sdlc-skill/scripts/fixtures/golden_baseline.txt`,
  `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/fixtures/golden_baseline.txt`,
  `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/fixtures/golden_baseline.txt`
  — regenerated; the diff must be exactly the `[scope]` line after each `check` verdict and
  the resume line in `orient`.

**Code lens:**

- `skills/agentic-sdlc-skill/SKILL.md` — MODIFY: Phase 5 bullet (FS1, FS2); Phase 1 resume
  rule (FS6).
- `skills/agentic-sdlc-skill/templates.md` — MODIFY the HANDOFF section (FS5).
- `skills/agentic-sdlc-skill/ENFORCEMENT.md` — MODIFY §4: the orientation carries the
  resume rule.
- `skills/agentic-sdlc-skill/evals/scenarios/closure_rewrites_stale_state.md`,
  `resume_rereads_unit_vision.md` — ADD.

**Sibling lenses** (R8), each in its own wording — their closure and orientation text
differs from the code lens, so these are edits, not copies:

- `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` — §5 Closure & Indexing
  (FS1, FS2); §1 orientation read (FS6).
- `distributions/course-creator/skills/course-creator/SKILL.md` — §5 Feedback and closure;
  orientation.
- `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` — its closure and
  orientation passages.
- `templates.md` of kb, mkt and course — the HANDOFF text each carries (FS5).
- `ENFORCEMENT.md` of kb, mkt and course — the orientation section, same delta as the code
  lens.
- `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py` — MODIFY
  `main`: where it prints `chronology_advisories` outside its `Report` for a docs root that
  is not `ai_docs`, it also prints `closed_workstream_advisories`. On an `ai_docs` root the
  spine's `cmd_validate` it already calls prints them, so each file is named once and
  `Report`, which fails `--strict` on any warning, never sees them. Its `index` calls
  `sdlc_core.rc_registry` directly and gets the `[note]` line with no edit.
- `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_mkt_check.py` —
  MODIFY: the advisory on a shared and on an own docs root; `[scope]` after the overlay's
  verdict.

**Derived documents the audit plan binds to a doctrine change** (`audit/audit_plan.md`,
rows `skills/agentic-sdlc-skill/` and `distributions/`):

- `ai_docs/strategic/skill_family_agent_workflows.md` — MODIFY: closure and orientation
  descriptions.
- `distributions/kb-agentic-skill/README.md`, `distributions/mkt-agentic-sdlc/README.md`,
  `distributions/course-creator/README.md`, and the root `README.md` — MODIFY where they
  state what closure or `check` does.
- `ai_docs/strategic/architecture.md` — MODIFY the Validator core row of the Component Map:
  it names this analysis's preservation table (the give-back of P1–P5 at closure).

**Project documents:** `ai_docs/vision/rulings.md` (two rows: the finding, citing R4; the
orientation line, citing R7 and r4); `CHANGELOG.md` of the four packages at release
(`GUIDE_release.md`).

No new dependency. No API or data-model change. Repository is CRLF: content deltas, never
file copies.

### Preservation constraints

| id | bound to | callers | must stay true | evidence |
|---|---|---|---|---|
| P1 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::cmd_orient` | the `orient` dispatch in the same file; `test_session_start.py`, `test_merge_safety.py`, `test_skill_invariants.py`; `test_golden_regression.py` through the CLI; every wired SessionStart hook, the Codex wrapper included | always returns 0, reads no stdin and never blocks; whole output within `ORIENT_MAX_TOTAL_CHARS` with the append reserve intact; with no docs root it prints nothing; apart from the one added line the output is what it is today | grep `cmd_orient` and `orient` over the four script trees; `test_session_start.py`; the golden diff |
| P2 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::print_check_notes` | `cmd_check` in the same file (which `knowledge.py` reaches for the knowledge and course lenses); `mkt_check.py` `main` | prints only; never changes an exit code; runs after the verdict in every lens | grep `print_check_notes`: two callers |
| P3 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::cmd_validate` | `cmd_check`; the `validate` dispatch; `knowledge.py`; `mkt_check.py`; the test files that call it | the new finding is an advisory: no error or warning count changes, the `--strict` exit is unchanged on every existing project | grep `cmd_validate`; the code's own rule where advisories are printed ("never fail a build, not even --strict") |
| P4 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::rc_registry` | `cmd_index` in the same file; `mkt_check.py` `index`, directly; `test_merge_safety.py` | the registry bytes it writes are unchanged; the new line is printed, never written into `handoff.md`; its return code is unchanged | grep `rc_registry` over the four script trees; `validate`'s byte comparison of the registry with its sources |
| P5 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::list_workstreams` | `build_registry`, `registry_conversion_blockers`, `rc_registry`, `chronology_advisories` and `cmd_validate` in the same file; `docs_site.py`; `mkt_check.py`; `test_merge_safety.py` | signature and returned list unchanged: the closed-status reader reads its result, it does not filter it | grep `list_workstreams` over the four script trees |

## Security and Threat Model

Surfaces touched: filesystem reads of project documents (unchanged set); text injected
into the agent's context (one new constant line at session start). No stdin, network,
authN/authZ, cryptography or personal-data surface.

- **T1 — the orientation blocks or loses the session start.** Eliminated by construction:
  the design reads no hook event, so `orient` gains no blocking read (R7). Requirement kept
  as a test: `cmd_orient` never touches stdin.
- **T2 — repo- or session-controlled text reaches the context through the new lines.**
  The resume line and the `[scope]` line are constants. The advisory prints a file name
  from the project's own `audit/` directory, as the registry already does, and the
  `status:` word only after it matched one of three fixed values.
- **T3 — the advisory leads to deleted knowledge.** A handoff may hold the only copy of a
  decision (the recorded inventory found this in files it kept). The advisory text says to
  move what is still worth reading before deleting; no command deletes anything.
- **T4 — a false sense of coverage moves instead of disappearing.** The `[scope]` line
  could be read as "re-reading is someone else's job". It ends with the duty: re-read what
  the change touched.
- **T5 — the orientation grows past its bound.** The line is inside the fixed head, which
  the existing budget subtracts before sizing the router and the registry; a test asserts
  the whole output stays within the bound on a project with a full registry.

The recorded cases are redacted copies of another project; they are re-read in full for
names before any commit (this repository is public).

## Action Plan

- [x] RED: tests for FS4 (advisory once per file, `index` line, free-text and
  no-`workstream` cases, `--strict` exit unchanged), FS3 (`[scope]` after either verdict,
  exit code unchanged), FS5 (template text), FS7 with T1 and T5.
- [x] `sdlc_core.py`: `closed_workstream_advisories`, its two call sites, `[scope]`,
  resume line.
- [x] `mkt_check.py`: print the advisories beside `chronology_advisories`; tests in
  `test_mkt_check.py` for the shared and the own docs root.
- [x] Doctrine, code lens: `SKILL.md` Phase 1 and Phase 5, `guides.md` §6, `templates.md`
  HANDOFF, `ENFORCEMENT.md` §4.
- [x] Doctrine, sibling lenses: the same rules in each lens's own closure, orientation,
  template and enforcement passages.
- [x] Eval scenarios: `closure_rewrites_stale_state.md`, `resume_rereads_unit_vision.md`;
  replayed cold on fixtures built from the recorded cases, old text against new (result in
  the Diary: the old text was not red).
- [x] Regenerate the three golden transcripts and the four shared manifests; full battery
  in each tree.
- [x] Derived documents: `skill_family_agent_workflows.md`, the READMEs; `vision/rulings.md`
  rows; E2E script; closure review; merge brief; `mark` the analysed areas.

## Test Strategy

- **Probes kept with the unit** (`harness_honest_signals/`), red on 2026-11-14 against
  release 1.55.0: `probe_closed_handoffs.py` (FS4, on the 43 recorded frontmatters: 9
  sources declared closed, 0 named) and `probe_signals.py` (FS3: clean verdict with no scope line;
  FS7: no resume line). Green is the acceptance.
- **Unit tests** (AAA, in the shared batteries and `test_mkt_check.py`): FS3 in the spine
  and the marketing overlay; FS4 with its four cases; FS5 as an invariant over each lens's
  template text; FS7; T1 (no stdin access), T5 (bound); P1–P5. Mutation for each new call
  (drop it → red), the battery's existing idiom.
- **Doctrine replay** (FS1, FS2, FS6): the two eval scenarios run cold by a fresh agent
  with the skill text before and after the change, on the recorded guide and the recorded
  summary. Pass criteria: all three state sentences rewritten and the guide named (FS1,
  FS2); the unit's vision read before the first answer and cited (FS6). FS1's three cases
  are scenario variants: nothing impacted → `re-read whole: none impacted`; a guide whose
  source did not change → rewritten through the guide's own route; a document too large →
  marked superseded.
- **E2E, human** (`E2E_TEST_honest_signals.md`): a real compaction on Claude Code shows the
  orientation, with the resume line, in the resumed context; a real project with a closed
  handoff shows the advisory in `check`.
- **Not verifiable here:** whether a given client re-runs the session-start hook after a
  compaction — documented for Claude Code (hooks reference, read second-hand), unknown for
  the others; S2 (the count going down over time) is observed in the field, not tested.

**Limit stated, not hidden.** FS4 names the nine sources whose status is a clean lifecycle
word. The recorded inventory judged 27 of the 43 finished (13 released, 14 finished in
code and waiting on a formal act); the other eighteen are visible only to a reader. FS5
is what makes the next closed file declare itself in a form FS4 can read — or not exist.

## Diary / Current State

**2026-11-14 — unit opened, cases received, probes red, design drafted.** Opened on the
field report (R1) for its points 2, 3 and 4 (R2). Owner accepted the closure re-read cost
(R3), ruled for a finding on the named file over any cap (R4) and supplied the three real
cases through the reporting session (R5). Elicitation round skipped beyond those
questions: goal, actors, scope, non-goals, constraints and acceptance signals are stated
in the report itself. Probes written and shown red on release 1.55.0. Open before closure,
not this unit's defect: `check` is NOT CLEAN on `main` after release 1.55.0 (`stale`:
`SKILL.md` and `distributions/`), and a fresh worktree reports 67 files where `main`
reports one.

**2026-11-14 — design review round 1: FAIL, five blockers, all confirmed on the code.**
Missing impacted files (the golden transcripts, the two derived documents the audit plan
binds); contracted prefixes that did not match the code (`[advisory]` in the spine, one
verdict string for four lenses); the registry line bound to `cmd_index` where
`rc_registry` writes it and the marketing overlay calls it directly; a stdin read whose
hang the mitigation did not answer; the resume duty and the orientation growth left out
of the ceremony and admission disclosure. Owner decisions taken on the last one: resume
cost accepted (R6); the orientation line is constant and printed always, with no read of
the hook event (R7), which removes the stdin threat and the unverified `source` value;
the doctrine goes into all four lenses (R8). Design rewritten to this state. Next: scoped
re-review, then the owner's design approval.

**2026-11-14 — design review PASS after three rounds (FAIL → PASS).** Round 2 found the
five blockers addressed and raised two wording findings; round 3 found both addressed.
Row in `audit/reviews/REVIEW_LOG.md`. Not verified by the review and left to the E2E:
whether a client re-runs the session-start hook after a compaction. Next: the owner's
design approval; no code before it.

**2026-11-14 — design approved by the owner (R9); implementation started.** First step: the
RED tests of the Action Plan.

**2026-11-14 — implemented; four batteries green.** RED first, then green: 14 tests in the
shared batteries, 4 in the marketing overlay, 4 invariants that fail in any lens the
doctrine did not reach. Both probes red on release 1.55.0 and green on the change. Full
batteries: code 642, knowledge 955, marketing 658, course 648, all OK. Golden transcripts
re-captured in the three trees that have one; their diff is the `[scope]` line after each
`check` verdict and the resume line in `orient`, nothing else. One figure of the approved
design corrected by the probe: nine sources are named on the recorded case, not ten — the
tenth file declares `DONE` and has no `workstream:`, so it is not a registry source. Owner
remark R10 (dogfood): in this repository the earlier session left `stale` red on `main`
after release 1.55.0, and F-022 is `IN_PROGRESS` with no workstream file — the inverse of
what FS4 names and outside the approved design; raised with the owner, not added. Doctrine
replays on the two eval scenarios and the E2E script: still to run.

**2026-11-14 — doctrine replays run cold: the new text passes, the old text was not red.**
Six runs, one sample each, a mid-tier model, fresh context, the skill text given by path
(old = release 1.55.0, new = this change), judged on the files the agents left and on their
closing messages. Closure scenario: with the new text all three state sentences of the guide
were rewritten and the message carried `re-read whole:`; with the old text all three were
rewritten too, and the message carried no such line. Resume scenario, two fixtures (the
second closer to the recorded case: the vision in its own document, the analysis only
pointing at it, a spike saying "probably"): old and new both read the unit's vision before
the first answer and cited it; the new text also read the request record first. So the
replays show the declaration line (FS2) and the request-record read (half of FS6); they do
**not** show that FS1 or the vision read of FS6 changes behaviour — a ceiling effect at this
size and tier, not evidence of an effect. What remains demonstrated red-to-green is the
mechanical part (FS3, FS4, FS7) on the recorded cases. The field signals S1 and S3 are the
only measure of the doctrine, and the E2E script carries them.

**2026-11-14 — closure review round 1: FAIL, two blockers, both confirmed and fixed.** The
course README, listed in the Impact, was untouched (it states what `check` does: sentence
added). Two of FS1's three declared scenario variants were missing from the eval scenario
(added). Seven warnings, all taken: the marketing and course lenses lacked the guide-route
and superseded clauses and the "no line means not re-read" sentence (added); this unit's own
handoff still described the state before implementation (rewritten — the defect FS1 names,
in the unit that introduces it); the preservation constraints had no home after closure
(Component Map row of the validator core now names this table); the line's size was stated
three ways (224 characters everywhere); the orientation enumeration in `SKILL.md` omitted
the new line; one invariant could pass on text that was already there (now reads the rule's
own paragraph). Redaction read of the recorded cases done before any commit: the two short
cases and the report's extended copy read whole; `case_registry_40.md` read whole in its
first 120 lines and, for the rest, every distinct line of its 760 remaining lines listed and
read — no person, customer, product, host or employer name, no credential.

**2026-11-14 — closure review PASS (FAIL → PASS, two rounds); final tree green; waiting on the
owner.** Full batteries on the final working tree, 2026-11-14T18:03Z: code 642, knowledge 955,
marketing 658, course 648, all OK; node tests 27, 7, 13, 76, all pass. Areas
`skills/agentic-sdlc-skill/` and `distributions/` re-marked. `E2E_TEST_honest_signals.md` and
`MERGE_REVIEW_honest_signals.md` written. Nothing is committed: the commit, the merge and the
release are the owner's, and the unit stays open until then — its handoff names that act.
Not done here: the CHANGELOG entries and version numbers (release), and the three matters of
R10 and R11.

**2026-11-14 — closure gate CLEAN; why `stale` was red in a fresh worktree.** `check --root .`:
CLEAN (validate rc=0, stale rc=0), after `mark` of `skills/agentic-sdlc-skill/`,
`distributions/` and the parent row `skills/`. Mechanism of the red seen since the unit
opened, named so it is not patched blind: a mark taken on an uncommitted tree records a
timestamp, and `stale` compares a timestamp reference with file modification times. A fresh
checkout gives every file today's time, so the same tree reported one stale file on `main`
and 67 in this worktree. It is another signal that does not measure what it seems to (it
measures when a file was written to disk, not whether it changed) and is outside this unit:
put to the owner with R10 and R11. Consequence for the merge: after the commit, `mark` the
three areas again so the reference is the commit hash.

**2026-11-14 — closed: committed and merged into `main` on the owner's word (R12).** Workstream
file deleted, analysis COMPLETED, areas re-marked by commit hash. Not pushed and not
released: neither was asked. Left for after the release: the E2E script, whose scenario S3 is
the only check that a client re-runs the session-start hook after a compaction. The doctrine's
effect stays unproven by replay (entry above). Open elsewhere: F-097 (open workstreams shown
when a unit opens; an analysis in progress with no workstream file) and F-098 (the team asked
at the start); the timestamp marks of `stale` in a fresh checkout have no unit.
