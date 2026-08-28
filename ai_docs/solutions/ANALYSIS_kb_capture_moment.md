---
description: F-040 unit 2 of VISION_kb_second_brain - the daily capture moment. The rails exist (claim row is L1, notes take elicited/derived/ruling); this unit adds the MOMENT that channels the session's decisions onto them, plus a ledger-freshness line in the kb orient.
status: PLANNED
feature: F-040
id: F-040
start_date: 2026-08-28
level: L3
branch: feat/kb-capture-moment
---
# ANALYSIS: KB Capture Moment (second-brain unit 2)

**Level: L3 · router: no match** (monorepo `reference/INDEX.md` carries only `GUIDE_release.md`, not applicable).

## Feature Vision
`VISION_kb_second_brain.md`, APPROVED 2026-08-27 — unit 2: "I binari esistono già... manca il MOMENTO — un trigger di fine sessione che chiede 'decisioni di oggi da registrare?' e le incanala sui binari esistenti. Nessun formato nuovo."

## Objective
Decisions taken while working — thresholds chosen, rules adopted, preferences stated — evaporate because no moment asks for them: the KB updates only on ceremony days, and the gaps are where the agent later invents. The rails are already doctrine (a claim row on an existing topic is L1; `corpus/notes/*` takes `origin: elicited` / `derived_from:` / `basis:`); this unit adds the MOMENT, at the closing points the skill already owns, and one by-construction limb: the kb orient surfaces ledger freshness so a missed capture is visible at the next session's start.

## Capability Ledger (what already exists — this unit extends, never duplicates)
- Rule Zero: "Adding one claim row to an existing topic is L1" — the cheap write path.
- Write Triggers: `corpus/notes/*` on "something is said / synthesised / ruled"; `audit/handoff.md` + `project_notes.md` at "5 / session end" — the session-end MOMENT already exists as a doctrinal event; this unit adds a duty to it.
- `reconciliation.md`: rulings carry mandatory `basis:`; the claim state machine handles a captured fact that meets an existing claim.
- F-039's `kb_cmd_orient` intercept — the append point the freshness line rides on.
- The question discipline (`elicitation.md`): a mandated process question must name what it unblocks; capture questions fire only on genuine ambiguity.
- Escalation triggers: creating/re-parenting nodes is L3 — capture must never smuggle a placement.

## Design

### 1. `SKILL.md` (kb): new section `## The Capture Moment`, after `## Topic Recall`
- **When — the closing points the skill already owns, once per session**: phase 5 of any governed unit, and the session-end pass that already updates `handoff.md`/`project_notes.md`. Never per-turn; never a standing interruption mid-work.
- **What counts as a decision**: domain choices made or confirmed this session — a value, a threshold, a rule, a stated preference, a rejected alternative with its reason. NOT mechanics (commands run, files edited), NOT process state (that is the handoff's job).
- **The channeling — existing rails only, no new format**:
  - fact on an existing topic → claim row, L1 (`id` empty; `claim-id --fill`), source pointing at the note that records it;
  - the user's own words → `corpus/notes/*` with `origin: elicited`;
  - a decision with its reason → a note with `basis:` (a ruling);
  - no owning topic → the note is still written, and the PLACEMENT is declared as the next kb unit (or the claim goes to `topics/unplaced.md`) — capture never smuggles an L3 hierarchy change (escalation triggers hold).
- **Silence is legal, a false capture is not**: when the session took no domain decisions, nothing is declared — no per-session ritual line (the F-039 verdict lesson). A capture question to the user is legal only on genuine ambiguity (a decision that seems taken but was not confirmed), per the question discipline.
- **The trace closes the anti-echo loop**: a captured ruling/elicited note is exactly the non-DERIVED ground unit 1's re-touch rule walks to. Capture today is what makes recall honest tomorrow.

### 2. By-construction limb: ledger freshness in the kb orient
`kb_cmd_orient` (F-039) gains one line under the topic-router section, only when `corpus/notes/` exists: `newest note: <N> days old` (mtime-based; `no notes yet` when the directory is empty). A missed capture becomes visible at every session start — pressure by visibility, not by interruption. Fail-open like the rest of the append; silent when there is no corpus.

### 3. Write Triggers row
New row: event "domain decisions taken this session" → destination "claim row (L1) on the owning topic, and/or `corpus/notes/*` (elicited / ruling)" → phase "5 / session end — the Capture Moment". One event, one destination table stays true: the row points at existing destinations, it does not create one.

### 4. Battery: new kb-only module `test_kb_capture.py`
Doctrine anchors (whitespace-normalized): section present; "once per session"; the four channeling rails; "never smuggle"; silence-is-legal; the freshness line's forms. Orient tests: notes dir with an old note → `newest note:` line; empty notes dir → `no notes yet`; no corpus → no freshness line. Mutation both ways. kb-only, outside the shared manifest (the F-039 review rule).

### 5. Eval scenario (kb only): `capture_channels_the_days_decisions.md`
Setup (fenced seeding, canonical claim table per templates.md — the F-039 closure lesson): an existing `pricing` topic with `## Claims`, one note. Prompt: a short working session in which the user states a decision ("from now on, quotes above 50k need my sign-off") and asks to close up. Pass: at closure the agent captures — an `origin: elicited` note with the user's words, a claim row (L1, empty id) on `pricing` (or the declared owning topic) sourcing that note with a legal `L<a>-<b>` locator; no new topic created; no per-session ritual if nothing was decided (negative branch stated in criteria).

### 6. Carriers
kb `README.md`: capability point 7 (the capture moment, one short paragraph). kb `CHANGELOG.md` `[Unreleased]`: F-040 entry appended under the existing F-039 block.

## Impact
| File | Change |
|---|---|
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | new section + Write Triggers row |
| `.../scripts/sdlc_check.py` | freshness line in `kb_cmd_orient` |
| `.../scripts/test_kb_capture.py` | NEW kb-only module |
| `.../evals/scenarios/capture_channels_the_days_decisions.md` | new |
| `distributions/kb-agentic-skill/README.md` | capability point 7 |
| `distributions/kb-agentic-skill/CHANGELOG.md` | [Unreleased] F-040 entry |

All kb-lens; no shared-spine file; `taxonomy.md`, `templates.md`, `reconciliation.md` untouched (the rails are reused, not changed). Code and mkt lenses unaffected.

## Security and Threat Model
- **T1 noise** — a capture ritual on every session (or worse, every turn) is the vision's failure #1. Mitigations: the two named closing points only, once per session, silence legal when nothing was decided, the freshness line is one line and only when `corpus/notes/` exists.
- **T2 smuggled scope** — capture creating topics or re-parenting under the radar. Mitigation: the no-smuggle clause; placement stays L3 by the existing escalation triggers; anchored in the battery.
- **T3 fabricated capture** — the agent "capturing" decisions never taken (model knowledge as elicited notes). Mitigation: elicited notes carry the user's words; ambiguity triggers a question, not an invention; the eval's pass criteria test the negative branch.
- No security surface: doctrine + one read-only mtime probe in orient.

## Test Strategy
Battery RED→GREEN on the new module; mutation bites both ways; orient freshness unit-tested (3 states); eval scenario seeds canonically and runs under the fenced harness; `check --hybrid` CLEAN at closure; kb battery fully green.

## Action Plan
1. SKILL.md section + Write Triggers row.
2. Freshness line in `kb_cmd_orient` + its tests (RED first where doctrinal).
3. `test_kb_capture.py` complete; mutation check.
4. Eval scenario.
5. README + CHANGELOG carriers.
6. Closure: kb battery, check --hybrid, REVIEW_LOG, handoff.

## Diary
- 2026-08-28: unit opened on `feat/kb-capture-moment` off main@43dbea1. Design decision made before drafting: no SessionEnd/Stop hook — SessionEnd cannot reach the model and a Stop hook is per-turn noise; the honest by-construction limb is freshness visibility in the F-039 orient append. The unit reuses every rail (claim L1, notes, rulings, unplaced) and adds only the moment plus one orient line.
