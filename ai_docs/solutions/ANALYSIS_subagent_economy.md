---
id: F-100
feature: Subagent economy - a subagent keeps its guides, proves it read them whole, and gets a tier and a split sized to them
description: F-100 - a field report measured that most subagent tokens were lost on guides read in part and on fresh contexts rereading guides another context already held; the design makes a brief ask for the read back, sizes tier and split to the guides, sends a correction to the context that holds them, and tells the owner, where the team is asked, what several sessions cost and buy.
status: COMPLETED
level: L3
start_date: 2026-11-16
end_date: 2026-11-16
domain: code
---
# Feature Analysis: Subagent economy (F-100)

## Objective

A field report from another project (`REQUEST_subagent_economy.md#R1`, project redacted)
measured, on one day of work:

- the same work cost less with one coordinating session and subagents than with a
  coordinator and the sessions it starts, because each such session starts empty and rereads
  what the coordinator holds, and their reports cross as truncated notes and shared files;
- a subagent sent its own corrections kept its guides (about 100-150k tokens not reread);
- a mid tier read part of the interface guides in three tasks of four, about 940k tokens
  discarded, implementation tasks included; it succeeded only where the guides were small;
- a task that needs more guides than one context can read whole fails before it starts.

The doctrine today (`dispatch.md`) says a dispatched subagent reads each guide in its brief
whole and sets the implementer tier to economy because `task.verify` makes a wrong cheap
answer visible. The mechanism the report exposes: **`task.verify` scores the work, never the
reading.** A subagent that applied half a guide can pass its test; nothing asks it what it
read, so the cheap tier stays legal exactly where it fails. The edit hook does not close this:
it is silent for a subagent's edits by design (`ENFORCEMENT.md` §3, its residual "edits
through a subagent … are not checked").

Scope (owner, R2): proposal 1 as information on cost in the team question, the default
unchanged; proposals 2 (correction to the context that holds the guides), 3 (the read
reported back), 4 (tier and split sized to the guides). Proposal 5 (reports in files) is out.

## Feature Vision

No feature Vision: the unit serves the project Vision (`vision/project_vision.md`, v9,
APPROVED) inside one milestone.

- Core Problem: «Myopia: an agent acts from partial understanding». A guide read in part is
  partial understanding by construction, and the field case shows it passing `verify`.
- North Star: the method keeps decisions traceable «at a ceremony cost proportional to the
  change's risk». Rereading guides a context already holds, and work discarded after the fact,
  are cost with no risk bought.
- Non-Goal "No ceremony ratchet": the unit adds a request in a brief, a line per guide in a
  report and one line in the team question. Its cost is stated in §Ceremony cost and asked of
  the owner with this design (R2 does not accept it); measured figures confirmed at closure
  (precedent r40). L1 pays nothing.
- Non-Goal 1 (not a work-management system): the rules choose which context runs a step and
  how a step is split **inside one approved change** — the Non-Goal's own exception
  («Sequencing the steps inside one approved change is not this»). No order, queue, holder or
  assignment between units. The team line informs and prescribes no shape (r49 «never a team
  shape»; `team.md` «The skill asks; it never prescribes a team»).

## Use Cases / User Needs

- **UC1 (owner answering the team questions)** — knows, while choosing, what several sessions
  cost and buy against one session with subagents. *Benefit: cost proportional to risk; the
  choice stays theirs.*
- **UC2 (orchestrating agent)** — knows whether a subagent read its guides whole before
  passing its work on. *Benefit: partial understanding visible before review.*
- **UC3 (orchestrating agent)** — gives a set of guides to a tier and a context that can read
  them whole, or splits the work so it can. *Benefit: same.*
- **UC4 (orchestrating agent)** — sends a correction to the context that already holds the
  guides. *Benefit: cost proportional to risk.*

Grounding: EXISTS — brief, `plan brief`, `task.verify`, the ledger, tier (economy / light /
deep, `review.md` §The capability floor), guide (a `GUIDE_*.md` the router or a plan names),
`## Team`, the coordinating session and the sessions it starts (`coordination.md`: "parts").
NEW — **sending a further message to a subagent the session started** (a client facility the
doctrine has never named; named generically, as `dispatch.md` names subagent spawning, and
conditional on the client offering it). No METAPHOR names.

## Functional Spec

- **FS1 — where it applies.** Every brief that names a guide for a subagent to read whole:
  an implementer's in the plan loop, and any other delegated pass, a review included, whose
  brief names one. A guide here is a `GUIDE_*.md` (project or agent KB); the skill's own
  doctrine files a reviewer is pointed at are not guides and are out of scope. The four lenses,
  Standalone and Hybrid. A session that dispatches nothing pays nothing.
- **FS2 — the read is reported, and checked against the guide.** The brief asks the subagent
  to report, for each guide it names, the guide's total lines and the last line it read. Before
  running `verify` or passing the work to review, the orchestrator compares each total with the
  guide's real length. A report that omits the line, or whose total is wrong, is asked once for
  it (the same subagent, where the client lets the session message it again); a report still
  missing or wrong after that, or with no way to ask, counts as a partial read. A declared
  partial read is not work: it is not verified or reviewed, and the subagent is told to read the
  rest (FS4) before redoing the step. In the plan loop the ledger records the task `failed` with
  `verify_result` naming the partial read. Outside the loop (a review or another delegated pass)
  the pass's output is not used; a review discarded this way produced no verdict and is not a
  round of its cap.
- **FS3 — the guides set the tier and the split.** Before the first dispatch the orchestrator
  counts the lines of the guides a brief names and judges them against the context the tier
  works in; a set it judges too large is split before dispatch, by the guides each part needs,
  never by files alone. This first judgement has no fixed threshold (no measurement supports
  one); what bounds it is the rule after a dispatch: two consecutive failed rounds on the same
  task — a declared partial read or a failed `verify`, either kind — send it to a higher tier or
  to a split by guide set, as two `verify` fails do today; the first is answered by FS4. A split
  edits the plan inside the approved design: the plan is revised and `plan validate` runs again
  before the next dispatch. Two failed `verify` rounds alone still go to the deep tier, as today;
  the split is the option a partial read adds. A tier that stopped partway through a guide twice
  is not given that guide again, on that task or another, in the same work. A set that the deep
  tier still reads in part and that cannot be split goes to the owner.
- **FS4 — a correction goes to the context that holds the guides.** A correction of a
  subagent's own work — the rest of a partial read, review findings, a failed `verify` — goes to
  that subagent, where the client lets the session send it a further message, instead of a new
  context that rereads the guides. A first dispatch is still a fresh context with the brief as
  its whole content. Escalation wins: a task sent to a higher tier (FS3) goes to a new context at
  that tier. A subagent whose context was compacted reports the read again for the guides its
  next step needs. Never across roles: an author is never sent its own work to review, and the
  independent review keeps its fresh context; what a reviewer's scoped re-review runs in is not
  changed here.
- **FS5 — the team question carries the cost.** Where the team questions are asked, the
  question on members says, in one or two lines, what several sessions (a coordinating session
  and the sessions it starts) cost and buy against one session with subagents: each session
  starts empty and rereads guides, records and project another already holds, and their reports
  cross as notes and shared files; a subagent's report returns whole and, where the client lets
  a session message its subagent again, the subagent can be sent its corrections and keeps what
  it read; sessions buy work the owner can open and steer directly. The default (one agent) and
  the owner's choice are unchanged; nothing is recommended, refused or changed.
- **FS6 — unchanged.** The default team, the coordination rules, the capability floor's table
  and its rule, two failed `verify` rounds going to the deep tier, the ledger schema, the review
  slots and their round cap.

Acceptance: `harness_subagent_economy/CRITERIA.md` (written before the doctrine).

## Interface Contract

The surfaces are the doctrine the agent loads and three texts a person or subagent reads.
Each reuses an existing idiom; no new project document or validator field.

- UC1: the owner reads the cost line inside the team question set, and answers there.
- UC2: the subagent reads the request in its brief — for a plan task, a line `plan brief`
  prints under the guide pointers — and writes the line per guide in the report it already
  returns. The orchestrator reads it before `verify`; a missing or partial read is said in its
  next message and written to the ledger's `verify_result`.
- UC3, UC4: the orchestrator's dispatch choice, seen in its messages as today.

## Capability Ledger

| Capability | Verdict | Where / gap |
|---|---|---|
| know a guide was read whole | INADEQUATE | `dispatch.md` requires the whole read; nothing asks for it back; the edit hook is silent for subagent edits by design (`ENFORCEMENT.md` §3). The `verdict` coverage logic reads a session's own transcript; reusing it on a subagent's transcript is client-specific and out of this unit (declared candidate) |
| choose a tier for a dispatched task | INADEQUATE | `review.md` capability floor: economy for implementers, legal by `task.verify`; guide volume not counted |
| send a correction to the context that holds the guides | MISSING | searched "resume", "same subagent", "further message", "SendMessage" in `dispatch.md`, `review.md`, `team.md`, `coordination.md` |
| tell the owner what a team shape costs | INADEQUATE | `team.md` offers the default and asks; no cost |

## Guide check

No CURRENT guide covers the dispatch or team doctrine (`reference/INDEX.md`: hooks, release,
shared project memory, skill-family changes). `GUIDE_skill_family_changes.md` governs the
triage of a change copied into the distributions: read whole; the shared copies count once.
No guide is owed: the unit forced no model of a complex component.

## Impact

Shared core (authored once in the code lens, copied verbatim into three trees by
`shared_files.py --update`):

- `skills/agentic-sdlc-skill/dispatch.md` — MODIFY. One block owns the rules; the other
  places cite it in a few words:
  - §What may be delegated at all: a sub-block **Guides a subagent must read** (FS1–FS4, with
    the precedence of FS2–FS4 over the loop), so the four `SKILL.md` pointers to "that
    section" stay complete;
  - §The loop: the `plan brief` bullet (it now prints the read-back line), "Spawn the subagent
    … entire context window" (a first dispatch) and the `verify` / ledger step — pointers;
  - §Model tiers: the two-fail escalation counts a partial read too — pointer;
  - §Review slots, "If a review FAILs, fix and re-run `verify`": by the same subagent — pointer.
- `skills/agentic-sdlc-skill/team.md` — MODIFY: §When it is asked, the cost line (FS5).
- `skills/agentic-sdlc-skill/scripts/sdlc_core.py` — MODIFY: `plan brief` prints, under a
  non-empty guide list, the line asking for the read back (FS2, Poka-Yoke: the request is in
  every plan brief without the orchestrator writing it).
- `skills/agentic-sdlc-skill/scripts/test_plan.py` — MODIFY: the printed line.
- `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` — MODIFY: class
  `F100_SubagentEconomy`.
- The three copies of each, and `shared_manifest.json` in the four trees — regenerated.
- `skills/agentic-sdlc-skill/ENFORCEMENT.md` (code lens only carries the line): its residual
  "edits through a subagent … are not checked" is about the verdict check and still reads true —
  checked, not edited.

Derived documents:

- `ai_docs/strategic/skill_family_agent_workflows.md` — MODIFY: line 166 («escalation di tier
  solo dopo 2 fail consecutivi») gains the partial read; the read report and the correction
  context; the F-099 rule it lacks since the last release.
- `README.md` and the three distribution READMEs — the team bullet (`README.md`:38 and its
  copies) describes what the questions ask, so it gains one sentence on the cost line.
- `CHANGELOG.md` and the three lens CHANGELOGs — an `## [Unreleased]` entry each.

Not changed, read: the four `SKILL.md` (their pointers name `dispatch.md`'s family-wide section,
which keeps the new block inside it), `review.md` (its floor table stays; FS3 adds a dispatch
condition, not a floor), `coordination.md` (R2), validator code other than `plan brief`.

Evidence and records:

- `skills/agentic-sdlc-skill/evals/scenarios/subagent_guides_read_whole.md` — ADD; the
  scenarios `README.md` lists it if it lists scenarios.
- `ai_docs/solutions/harness_subagent_economy/` — criteria, build script, prompts, raw answers,
  results.
- `ai_docs/vision/rulings.md` — rows r53–r56, placed below.

### Placement against the ruling ledger (before the prose)

- **FS2, the read reported** — MISSING (no row answers "did a subagent read the guides it was
  given"): new row r53, ADMIT on the prose (myopia; ceremony asked).
- **FS3, tier and split sized to the guides** — near r20 (which tier may run a gate; its basis
  makes economy legal for dispatch). Scope growth of an admitted capability is re-ruled (r4):
  new row r54. Distinction line: r20 sets a floor per role; r54 adds, for a dispatched task, the
  guides' volume and a partial read as a condition on the tier and the split.
- **FS4, the correction's context** — near r3 ("by whom"). Distinction line: r3 is who works on
  which unit; r55 is which context runs a step inside one approved change, the Non-Goal's own
  exception. New row r55.
- **FS5, the cost line** — scope growth of r49 (the team question): new row r56. Distinction
  line from r49's «never a team shape»: the line states costs of shapes, recommends none.

### Preservation constraints

| Symbol / text | What must stay true |
|---|---|
| `dispatch.md` §What may be delegated at all | its table, never-list and delegability condition unchanged |
| `dispatch.md` §Model tiers | economy default; escalation after two `verify` fails unchanged |
| `dispatch.md` §Ledger protocol | schema `{status, verify_result, timestamp}`, single writer |
| `review.md` §The capability floor, independence | unchanged, cited |
| `team.md` §The default, §What the section cannot change | unchanged |
| `plan brief` output | existing sections and order unchanged; one line added only when guides exist |
| `SHARED_FILES` | no file added or removed |

## Security and Threat Model

No input or data surface; `plan brief` prints a constant. Threats on the rule itself:

- **T1 — the read is believed on the subagent's word.** Mitigation, partial: the orchestrator
  compares each total with the guide's real length (FS2), so a wrong total is caught; where the
  client exposes the subagent's tool calls, they are the evidence (`SKILL.md` Phase 5: delegated
  work is verified on the files, never on the report). **Residual, declared:** "last line N of
  N" is also what a read with gaps reports, and a weaker tier may misreport without intent;
  neither is detected without the transcript.
- **T2 — a correction context breaks review independence.** FS4's never-across-roles clause.
- **T3 — the cost line steers the owner.** FS5 states what several sessions buy as well as what
  they cost, recommends nothing, and leaves the default and the choice as they are. **Residual:**
  the costs rest on one project's measurement of one day; the line states mechanisms, not
  figures.
- **T5 — a forgotten line discards whole work.** Where the client cannot message a subagent
  again, a report that omits the line counts as a partial read (FS2), so finished work may be
  redone. **Residual, declared:** stricter than R1's words (a declared partial read); the
  `plan brief` line makes the omission rare, and the rule keeps an unproven read out of review.
- **T4 — re-dispatch without end.** FS3 bounds it: a second partial read escalates or splits;
  the deep tier's failure on an unsplittable set goes to the owner.

## Ceremony cost

Estimate accepted by the owner with the design (R3); measured figures, for confirmation at
closure: `dispatch.md` 8,185 → 11,681 UTF-8 LF bytes (+3,496, estimate +2.5 KB), `team.md`
5,020 → 5,558 (+538, estimate +0.4 KB, of which the cost line itself is the ~300 bytes the
owner reads once), `plan brief` +1 printed line (93 bytes) where guides exist. `SKILL.md`
unchanged in every lens.

| Where | Added | Cost |
|---|---|---|
| L1, L2 and any session that dispatches nothing | nothing | 0 |
| a brief naming guides | one request line (printed by `plan brief` for plan tasks) | one line |
| the subagent's report | one line per guide | one line per guide |
| the orchestrator before `verify` | one length check per guide | a line count per guide |
| a partial read | the rest read by the same subagent, then the task redone | the discard happens today too, found later |
| the team question set (once per project) | one or two lines in the members question | ~300 bytes, once |
| doctrine read on its own trigger | `dispatch.md` (when delegating) and `team.md` (when the team is asked), shared, four trees | estimate +2.5 KB and +0.4 KB |
| every session that loads a lens | nothing (`SKILL.md` unchanged) | 0 |

## Action Plan

- [x] Criteria written before the doctrine; fixture v1 leaked two answers, v2 neutral; old
  text run on v2 (`raw_answers_v2.md`).
- [x] Design review round 1 (FAIL, 2 BLOCK, 11 WARN); this revision.
- [x] Design review rounds 2 and 3 (PASS); ceremony estimate accepted by the owner (R3);
  design approved by the agent under the reading guide's `## Team` (R4).
- [x] RED: 7 tests failing before the doctrine (`F100_SubagentEconomy`, two in `test_plan.py`);
  `dispatch.md`, `team.md`, `plan brief`; copies and manifests in the four trees.
- [x] Replay of the new text on fixture v4: 5/5 criteria for both readers (`RESULTS.md`);
  eval scenario; rulings r53–r56; derived documents; `[Unreleased]` in the four CHANGELOGs.
- [x] Closure review (FAIL, then PASS); merge brief; `check`; local commit.
- [x] The owner confirmed the measured figures and the merge into `main` (R5).

## Test Strategy

- **Replay** (`harness_subagent_economy/`): a cold orchestrator reads a neutral fixture and the
  method (`dispatch.md` and `team.md`, old text from the release commit against the new),
  criteria written first. Red under the old text, green under the new. **Declared proxy:** the
  replay measures whether the doctrine makes an orchestrator do what the field report measured
  as cheaper; it does not measure tokens. The cost effect is R1's measurement. C2 (the
  correction to the same subagent) was green under the old text on every fixture, where the
  fixture names the messaging facility: it is kept as a regression criterion, not as evidence
  of FS4; FS4's evidence is R1's measurement alone, and row r55 says so. FS3's first judgement
  (sizing before dispatch) has no threshold and is not scored; C4 scores its bounded half, the
  escalation after two failed rounds and its carry-over to another task naming the same guide.
  **Measured on fixture v4:** both old-text readers escalated T0 and gave T3 to a higher tier
  unprompted, so C4 is green on the baseline and is not evidence for FS3 either: FS3 writes down
  what a careful reader already does once a failure is in front of it, and its evidence is R1's
  measurement. The baseline is red on C1 (both readers, every fixture), C3 (both readers on v2
  and v3; one partial on v4, where the fixture's T0 primes a count) and C5 (both readers on v3 and
  v4).
- **Unit**: `test_plan.py` — the printed line present with guides, absent without.
- **Invariants**: `F100_SubagentEconomy` in every tree.
- **Suite**: `unittest discover` in each lens's `scripts/`; `test_drift`.

## Diary / Current State

**2026-11-16 — opened.** Request record R1–R2. Scope chosen by the owner (R2). Worktree
`claude/f100-subagent-economy` from the release commit, so the primary checkout stays on the
release for the owner's publish.

**2026-11-16 — design review round 1 FAIL; revised.** B1: the new rules conflicted with
`dispatch.md`'s fresh-context dispatch, fail path and two-fail escalation; precedence now
stated (FS2–FS4) and those lines are in the Impact. B2: the baseline probe did not exist when
reviewed; built since — fixture v1 leaked C1 and C2 to the old text, v2 neutral, old text red on
C1, C3, C4, C5 (two readers). WARNs taken: FS5 moved into the team question and made two-sided;
FS3 sizes before the first dispatch and escalates on the second partial read; a missing line is
asked, not discarded; the length check is in FS2; ledger row 1 corrected; reviewer briefs,
compaction and the unsplittable set covered; ceremony timing and doctrine cost stated; rulings
placed; derived documents and `plan brief` named; "resume" graded NEW.

**2026-11-16 — design review round 2 PASS with 6 WARN; taken.** Old text on fixture v3: C1,
C3, C4, C5 red, C2 green (two readers). N1: FS3's first judgement declared without threshold,
its bound is two failed rounds of either kind (N6), and C4 now scores that bound on fixture v4.
N2: FS4's evidence is R1 alone. N3: FS2 outside the loop, and a report still wrong after one
ask. N4: one block owns the precedence, the other places point at it; the `plan brief` bullet
named. N5: the cost line carries the client condition. File names removed from FS4 and FS6.

**2026-11-16 — design review round 3 PASS (cap reached), 3 WARN taken.** R1: FS3 carries a
twice-failed guide over to other tasks, so C4's T3 half is in the spec. R2: two `verify` fails
alone still go to deep (FS3, FS6). R3: the forgotten-line discard declared as T5. Old text on
fixture v4: C4 green for both readers, recorded in Test Strategy; C1, C3, C5 stay the red
baseline. Design ready for approval under the reading guide's `## Team`; ceremony cost to the
owner.

**2026-11-16 — implemented; replay new text 5/5.** RED first (7 tests), then the block in
`dispatch.md` with pointers from the loop, the tiers and the review slots; the cost line in
`team.md`; the read-back line in `plan brief`. Copies and manifests in the four trees. New text
on fixture v4: C1–C5 passed by both readers. Measured bytes above the estimate (+3,496 against
+2.5 KB, after the closure review's corrections): put to the owner at closure.

**2026-11-16 — closure review FAIL (1 BLOCK, 5 WARN); taken.** B1: the `dispatch.md` figure was
measured before a later rewrap; remeasured after every correction. W1: the workstream file's
`next:`. W2: the derived document now says two failed rounds of either kind, the client
condition and never-across-roles. W3: the review-slots pointer carries the client condition.
W4: the four READMEs' team bullet gains the cost sentence. W5: `mark`, `check` and the figures
to the owner close the unit.

**2026-11-16 — closed.** Closure review round 2 PASS. Suites after the last edit: code 697,
knowledge 1010, marketing 713, course 703, all OK. Workstream file deleted; merge brief
written; local commit on `claude/f100-subagent-economy`. Open for the owner: the measured
figures and the merge.
