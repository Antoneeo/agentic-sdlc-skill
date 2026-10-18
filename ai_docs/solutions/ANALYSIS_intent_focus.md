---
id: F-071
feature: Intent focus — effort weighed against the value and risk it serves
description: Why every gate stayed green while F-063/F-064 lost the owner's core promise, and why reviews ran where they lowered no risk; the doctrine that rules both, replayed red/green on both incidents.
status: PLANNED
level: L3
domain: code
topics: [anti-myopia, vision-gate, review, proportionality, efficiency]
start_date: 2026-10-04
branch: main
---
# Intent focus — effort weighed against the value and risk it serves

For the owner: approve this design and its ceremony cost (§Ceremony disclosure), and
answer the open question in §Open questions; the doctrine diff is
`harness_intent_focus/proposed.patch`. For the implementer: §Impact and §Action Plan.
Nothing is applied yet.

## Objective

One mechanism, two faces: **the skill does not weigh effort against the value or the
risk it serves.** Effectiveness: no gate checks that the work goes where the owner's
outcome is (F-063/F-064 passed every gate and dropped the "why"). Efficiency: reviews
fire by level and moment, so they ran where they lowered no risk. The owner: "E' molto
importante che l'uso della skill permetta anche di mantenere alta l'efficienza e non
solo l'efficacia. Altrimenti finisce per essere dannosa" (REQUEST R3). The remedy adds
two checks where drift entered and removes two reviews where nothing was left to judge.

## Feature Vision

`vision/project_vision.md` is APPROVED. Served: Goal "Scale process cost to risk, in
both directions" and Goal "Make divergence from the declared intent visible before
implementation"; the Solo developer's "ceremony proportional to risk" and the Team
lead's "divergence from the declared intent surfaced before the change is merged".
Bound by the Non-Goal "No ceremony ratchet" (costed below). M1 (the owner's words lost
at Vision drafting) is closed by F-074 (`vision.md` §The owner interview); out of scope.

Elicitation (2026-10-18), REQUEST R4: the efficiency remedy is narrow (reviews only;
closed kinds bump, CHANGELOG, indexes, shared copies); the promise probe is built and
run red on the baseline before code; acceptance is the replay plus a field signal.

## Reference incidents

**Effectiveness — F-063/F-064 (2026-10-04).** Snapshot with hashes in
`harness_intent_focus/incident/`; the original is archived under tag
`archive/software-knowledge` (commit e6e4fb9). Owner's intent, stated to Claude on
2026-10-04 (not verbatim, REQUEST R1): the agent should understand more easily and
better **how the software works and why**. Measured (`replay.py`): the design review's
conformance table has 25 rows, none naming the why; `knowledge.py` has 0 of 2,543 lines
in functions named for rationale; the behaviour rubric never asks why; the design review
defers the benefit ("beneficio ancora da misurare"). Every gate stayed green.

**Efficiency — the F-072/F-074 session (2026-10-18).** (a) The `--open` field fix
(commit 4543157: one `SKILL.md` line per lens and its test, red/green, batteries green)
got an independent review that the owner stopped (REQUEST R2). (b) A closure review ran
on the post-PASS F-074 delta (bump ×4, CHANGELOG ×4, README, the family workflow
document, ruling r30, E2E script) and raised three real findings: a kb README line, an
E2E scenario, state lag (REVIEW_LOG 2026-10-18; `MERGE_REVIEW_vision_interview.md`).
Of that delta, the bump and the CHANGELOGs carried no judgement; the README, E2E and
ruling did. The F-074 design review (late), by contrast, found two BLOCKs.

## Mechanisms (confirmed on the incidents)

| ID | Where the skill let it through | Current text |
|---|---|---|
| M2 | Nothing weighs where effort goes against the owner's outcome | the conformance statement (`review.md` §Reviewing) maps each constraint to *where* it is met, never *how much* of the design serves it |
| M3 | The promise is tested last, by a test that cannot discriminate | `SKILL.md` Execute-Before-Specify covers claims about existing code and text deliverables, not the claim the unit exists to make true |
| M4 | The owner's outcome is no input row of the review | the request-record clause (`review.md` §Requesting, §Reviewing) checks statements the artifact *relies on*; an outcome it silently drops is not one |
| M5a | An optional review has no trigger, so the agent runs it | `review.md` §When a review is due: "the L2 closure review is optional" |
| M5b | A review fires by moment, not by the judgement left to check | moment 2 is due "before DONE" on any diff, so a whole delta is reviewed when only part of it is judged work |

## Use Cases / User Needs

Names: *request record*, *conformance statement*, *closure review*, *REVIEW_LOG*,
*north star* EXIST; *NOT DUE* row and *promise probe* are NEW (declared here).

| UC | Actor | Need | Traces to |
|---|---|---|---|
| UC1 | owner (Team lead) | a design that drops or under-serves my stated outcome is stopped before code | Goal "divergence visible before implementation" |
| UC2 | owner | the benefit I asked for is shown measurable, and failing on today's system, before code is written | same Goal |
| UC3 | owner (Solo developer) | no review is spent where nothing is left to judge | Goal "scale process cost to risk" |
| UC4 | owner | a review not run is as visible as a review run, and judged work never escapes | Goal "scale process cost to risk", both directions |

## Functional Spec

1. **Outcome rows.** A design review of an L3/E3 unit has one conformance row per
   outcome the owner named — the opening request, every entry widening scope, an
   approved north star — stating where the design serves it and what share of the design
   (sections and planned changes) goes to it. No serving section, or a minor share while
   a secondary concern takes the bulk, is a finding. Every lens.
2. **Promise probe (code lens).** When the owner's words for an outcome name a
   comparative effect, the probe that would show it is built before code, asks the
   question the outcome names, and runs red on the baseline; the candidate is measured
   after. The author's framing of the unit never exempts it; the reviewer rules whether
   the words are comparative and checks the probe as that row's evidence.
3. **Level-2 review trigger.** At level 2 the closure review is due only on a
   security-sensitive area the lens's Rule Zero names, or at the owner's request;
   otherwise it does not run and logs no row.
4. **Restating delta.** After a design or closure PASS, a delta made only of version and
   release metadata, regenerated indexes and audit-mark records, mechanically verified
   copies of a shared file, and CHANGELOG lines stating nothing the reviewed artifacts do
   not, is not reviewed: its own check runs and a row records `NOT DUE` with the kinds,
   the check and its result. Content governs the list (a CHANGELOG line adding a claim is
   judged work); a change answering a review finding is never in it; a failing check makes
   the delta judged work. Everything else after the PASS is reviewed, scoped to that part.
5. **The benefit report counts NOT DUE rows apart**, as neither reviews nor findings,
   and prints their number.

Acceptance: `BEHAVIOR_CASES.md` (gating) — a cold agent rules the six cases red on the
current text and green on the patched one, with both controls due under the patched text;
`replay.py` RED → GREEN with every control silent; batteries ×4 green after
implementation; field signal (R4): over the next three L3 units the REVIEW_LOG shows
NOT DUE rows with their reasons and no defect later found in a delta ruled not due.

## Interface Contract

Two surfaces, both existing idioms. (1) The review verdict (`review.md`): the
conformance statement gains rows of the same shape, one per owner outcome. (2) The
REVIEW_LOG row, read by the owner and by the benefit report: same columns; a NOT DUE row
carries `tier` closure, `model` `none (not due)`, findings 0, rounds 0, verdict
`NOT DUE: <kinds; check; result>`. The report prints one extra line with their count.
Flow: author reaches the closure moment after a PASS → classifies each change of the
delta → runs the restating part's check and logs NOT DUE → requests a scoped review of
the judged part, if any.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| map an input constraint to its evidence in a review | EXISTS | conformance statement, `review.md` §Reviewing | rows extended |
| hand the owner's own words to the reviewer | EXISTS | request record, `review.md` §Requesting | r26 |
| probe a claim red then green before writing it | EXISTS | Execute-Before-Specify, `SKILL.md` §3 | extended to the unit's benefit claim |
| rule whether a review is due | INADEQUATE | `review.md` §When a review is due | by level and moment only |
| report review outcomes | INADEQUATE | `sdlc_core.py` `cmd_benefit` | counts a NOT DUE row as a closure review and as inconclusive (`probe_benefit.py`, exit 0 on today's code) |

## Impact

| Path | Change | Serves |
|---|---|---|
| `skills/agentic-sdlc-skill/review.md` (shared; copied ×3) | FS1, FS2 reviewer half, FS3, FS4; `model` value list gains `none (not due)` | UC1–UC4 |
| `skills/agentic-sdlc-skill/SKILL.md` | FS2 author half (Execute-Before-Specify) | UC2 |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` (shared ×3) `cmd_benefit` | FS5 | UC4 |
| `templates.md` ×4 lenses, §`REVIEW_LOG.md` | one sentence: the NOT DUE verdict and its cells, citing `review.md` | UC4 |
| `skills/agentic-sdlc-skill/scripts/test_intent_focus.py` | ADD: anchors, incident facts, `benefit` on a NOT DUE row | acceptance |
| `ai_docs/strategic/skill_family_agent_workflows.md` | line 92: closure review "before DONE" becomes conditional (derived document, audit_plan rows 9/11) | consistency |
| `ai_docs/vision/rulings.md` | r31 at closure, after the owner's ADMIT | admission test |

Blast radius (prose: `git grep` over `skills/`, `distributions/`, `scripts/`, `evals/`;
code: callers read in source). No test pins the replaced strings. `cmd_benefit`: called
only by the `benefit` subcommand; exercised by `test_skill_invariants.py` (benefit and
`review_logged` tests, ×4 lenses) — these must stay green. `parse_review_log`: shared by
`benefit` and the docs-site chronology, which shows a NOT DUE row as a review event as
data and needs no change. `review_logged` (design-gate check) reads `tier`; a NOT DUE row
is fixed to `tier` closure, so it can never satisfy the design gate.
`templates.md:529` ("written before the closure review so it is part of the reviewed
diff") stays true: an E2E script is never a restating kind.

Data at rest: existing REVIEW_LOG rows are unchanged and none carries `NOT DUE`, so past
report figures do not move. Triggers evaluated: read↔write invariant move (no);
no-migration Non-Goal (no); new value in a column holding data (yes — the verdict; FS5);
a narrowed redact/filter function (no).

Rulings ledger (step 1): FS1–FS4 answer a question no row has ruled (when a review is
due, what it must weigh); FS5 widens r22's report by one count — a scope growth of an
admitted capability, re-ruled with r31 (r4).

## Security and Threat Model

Doctrine plus one report; no input parsing, filesystem write or network surface added.

| ID | Risk | Requirement / answer |
|---|---|---|
| T1 | The new checks become ceremony | each fires only where the replay shows drift entered; L1 untouched; level 2 loses a step |
| T2 | The outcome is gamed: quoted where it is not served | rows weigh share of the design, not mentions (FS1) |
| T3 | A NOT DUE ruling hides judged work | closed list governed by content; finding corrections excluded; failing check makes it judged; `tier` fixed to closure; row names kinds and check, so the integrator can compare with `review-map` |
| T4 | **Withdrawn protection** — the level-2 review and the review of a restating delta | population no longer reviewed: non-security level-2 changes, and post-PASS bumps, indexes, verified shared copies and claim-free CHANGELOG lines. What still covers it: the batteries and `check`, the tool that verifies copies, the owner reading the CHANGELOG at release. Uncovered and accepted by design: a CHANGELOG line that misstates, without adding a claim, a reviewed change — it ships in an immutable npm version |
| T5 | A PASS on the outcome row is read as proof of benefit | the probe reports benefit separately (FS2) |

## Ceremony disclosure

Non-Goal "No ceremony ratchet": what is added is stated; what is removed is said
honestly, including that it does not fully pay.

- **Removed:** the review of a restating delta — at least the bump and CHANGELOG part of
  every release delta (~130–175k tokens when it is the whole review, `review.md` §The
  gated rung; a scoped review on the rest otherwise). The level-2 review was already
  optional, so making it not due frees no mandatory budget; it removes the default the
  agent fell into.
- **Added, every lens, per L3/E3 design review:** one conformance row per owner outcome
  (reviewer time). **Code lens, per L3 unit whose owner names a comparative effect:**
  building the promise probe and running it on the baseline before code — authoring
  time plus one run (461 s for F-063's baseline); frequency: units whose request says
  better/faster/easier, not most units. **Per skipped delta:** one NOT DUE row.
- **Read cost (UTF-8, LF):** `review.md` +2,179 bytes, shared, read at every review in
  all four lenses; `SKILL.md` +445 bytes (code lens, every session); `templates.md`
  ≈ +200 bytes ×4 (on trigger). L1 pays nothing.

Net: the remedy is not self-financing; the owner accepts the remainder or it is cut.

## Open questions

1. **How distribution copies count in Rule Zero (this repository).** The `--open` fix
   (4543157) touched 17 files: one doctrine line and its test, copied into four lenses,
   plus records. Counted per file it is L3 (more than three files), so the patched text
   would still make its review due as a judged delta; counted once per copied change it
   is L2, and FS3 rules the review not due. No guide or doctrine says which, and a guide
   cannot be written from the agent's own judgement (`guides.md`). The owner's call.

## Action Plan

1. Owner: approve design and cost; answer question 1 (verbatim in the request record).
2. Apply `proposed.patch`; copy `review.md` to the three distributions; `shared_files.py --update`.
3. `cmd_benefit` (FS5) ×4 via shared copy; `templates.md` ×4; workflow document line 92;
   `test_intent_focus.py` red on `main`, green after.
4. Batteries ×4; `index`; `check` CLEAN; re-run `BEHAVIOR_CASES.md` on the applied text.
5. Closure review of the code and doctrine diff (judged work).
6. r31 (owner ADMIT); bump and CHANGELOG — ruled by FS4 itself, CHANGELOG content-checked.

## Test Strategy

- `BEHAVIOR_CASES.md` (gating): six cases ruled by a cold agent per text; results there.
- `replay.py --doctrine DIR`: re-runnable check that the text carries each rule and the
  incident facts trigger it, with a control per rule; it does not show obedience.
- `probe_benefit.py`: the report's current treatment of a NOT DUE row (FS5's reason).
- `test_intent_focus.py` (battery, at implementation).

## Diary

- 2026-10-04: opened from the post-implementation review of F-063/F-064 by Claude
  (claude-opus-5-5); incident snapshot taken; facts measured, not inferred.
- 2026-10-05: owner answered — Vision drafted by ChatGPT, approved by the owner;
  why/what/how = Vision / UC-IC-TM / ISP-TDD. M1 located at Vision drafting.
- 2026-10-17: records moved to `main`; unit renumbered F-065 → F-071 (F-065 was taken).
  The archive tag `archive/software-knowledge` and its message still say F-065.
- 2026-10-18: M1 closed for Vision authoring by F-074. Scope widened by the owner to
  efficiency (REQUEST R2, R3) as M5.
- 2026-10-18: elicitation answered (R4). Candidate R1 kept only as its review half (the
  outcome row); R4 (thin slice) dropped; scoped re-review untouched (no incident shows
  it). Stale record corrected: the incident original is under tag
  `archive/software-knowledge`. Design review round 1 FAIL (7 BLOCK, 9 WARN): restating
  kinds narrowed to the owner's R4 list, finding corrections excluded, probe scoped to
  the code lens and triggered by the owner's words, behavioural replay made gating, the
  F-074 delta's findings stated as real, the Rule Zero copy-count question raised.
