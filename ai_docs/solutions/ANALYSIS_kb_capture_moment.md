---
description: F-040 unit 2 of VISION_kb_second_brain - the daily capture moment. The rails exist (claim row is L1, notes take elicited/derived/ruling); this unit adds the sweep MOMENT the vision mandates at user-signed closings, plus a notes-recency line in the kb orient.
status: IN_PROGRESS
feature: F-040
id: F-040
start_date: 2026-08-28
level: L3
branch: feat/kb-capture-moment
---
# ANALYSIS: KB Capture Moment (second-brain unit 2)

**Level: L3 · router: no match** (monorepo `reference/INDEX.md` carries only `GUIDE_release.md`, not applicable).

## Feature Vision
`VISION_kb_second_brain.md`, APPROVED 2026-08-27 — unit 2: "un trigger di fine sessione che chiede 'decisioni di oggi da registrare?' e le incanala sui binari esistenti. Nessun formato nuovo." The ASK is the vision's mechanism and binds: an R1 draft reinterpreted it as ambiguity-only questioning; the divergence was surfaced to the owner (2026-08-28) who ruled to honor the wording.

## Objective
Decisions — thresholds chosen, rules adopted, preferences stated, including OFF-session ones told to no agent — evaporate because no moment asks for them. The rails are already doctrine (a claim row on an existing topic is L1; `corpus/notes/*` takes `origin: elicited` / `derived_from:` / `basis:`); this unit adds the sweep moment at user-signed closings, and one by-construction limb: the kb orient surfaces notes recency so a missed capture is visible at the next session's start.

## Capability Ledger (what already exists — this unit extends, never duplicates)
- Rule Zero: "Adding one claim row to an existing topic is L1" — the cheap write path.
- Write Triggers: `corpus/notes/*` fires at phase 4/5 when "something is said / synthesised / ruled" — the PRIMARY channel: a decision stated mid-session owes its note WHEN SAID. The moment is the closing SWEEP over that duty, never a second channel.
- `reconciliation.md` §2: rulings resolve contested sets (mandatory `basis:` = the fact the corpus lacks; supersession follows); the state machine classifies a captured claim meeting an existing one.
- `elicitation.md`: the two legality tests. A scoped once-per-closing sweep question passes both — off-session decisions are practitioner-owned facts no search can find ("Facts about intent come from the practitioner").
- F-039's `kb_cmd_orient` intercept — the append point the recency line rides on. Note frontmatter `date:` (templates.md) — the honest date source; mtime lies after clone/worktree (and the skill's own §4 worktree hygiene makes that routine).
- Escalation triggers: creating/re-parenting nodes is L3 — capture must never smuggle a placement. `topics/unplaced.md` is for topic-LESS scraps only (taxonomy.md's UNPLACED definition) and is invisible to recall — never a decision park.

## Design

### 1. `SKILL.md` (kb): new section `## The Capture Moment`, after `## Topic Recall`
- **When — user-signed closings, once per session**: phase 5 of a governed unit, and ANY user closing signal in an un-governed session ("chiudiamo", "we're done", the session-end pass that updates handoff/project_notes). Never per-turn, never a standing interruption. **Declared residual**: an unsignaled end (the user simply stops writing) captures nothing — the phase-4 note duty (a decision stated mid-session is noted when said) is the protection for sessions that never close, and the recency line makes the miss visible next time.
- **The sweep question — the vision's mandated ask**: at the closing, ONE question: "decisioni di oggi da registrare?" — scoped to today, so it reaches decisions taken OUTSIDE the session (a meeting, a call) that no transcript search could find. Legal per the question discipline: the search (transcript + corpus) is named and structurally cannot contain off-session decisions; the blocked act is the capture itself. Asked once; the user's "niente" ends it.
- **The sweep is idempotent**: it verifies the day's decisions are on the rails; a decision already noted at phase 4 is verified, never re-captured (no second note, no duplicate claim row). The moment closes gaps, it does not duplicate the primary channel.
- **What counts as a decision**: domain choices made or confirmed today — a value, a threshold, a rule, a stated preference, a rejected alternative with its reason. NOT mechanics, NOT process state (the handoff's job).
- **The channeling — existing rails, explicit provenance**:
  - the user's words → `corpus/notes/*` with `origin: elicited` and a `date:`; a claim row distilled from it carries `prov: ELICITED`, source = that note with a legal `L<a>-<b>` locator;
  - a synthesis of the day's discussion → note with `derived_from:` → claim `prov: DERIVED`;
  - RULING **only when the decision resolves an existing contested set** — then `reconciliation.md` §2 applies in full (mandatory `basis:`, supersession of the losing set). A fresh conflict-free decision is captured elicited: a preference is not a fact, and `basis:` is reserved for the fact the corpus lacks.
  - fact on an existing topic → claim row, L1 (`id` empty; `claim-id --fill`);
  - no owning topic → the note is written NOW; the placement is declared as the next kb unit. Capture never smuggles an L3 hierarchy change, and `topics/unplaced.md` is never a decision park (UNPLACED is for topic-less scraps and is invisible to recall).
- **Reconciliation is wired**: a captured claim meeting an existing claim on the node classifies per `reconciliation.md` — capture can confirm, refine, coexist or CONTEST, never silently overwrite.
- **Silence stays legal where no one signed off**: no closing signal → no question, no ritual line. The declared residual above, not a gap.
- **The trace closes the anti-echo loop**: a captured elicited/ruling note is exactly the non-DERIVED ground unit 1's re-touch walks to. Capture today makes recall honest tomorrow.

### 2. By-construction limb: notes recency in the kb orient
`kb_cmd_orient` (F-039) appends, whenever `corpus/notes/` exists (with or without a topic graph): `newest note: <N> days old (corpus/notes)` — dated from note frontmatter `date:`, falling back to mtime per note when absent — or `no notes yet`. **Named limit, declared in the line's docstring and the SKILL.md sentence**: it measures NOTES recency, not full ledger freshness (an ingest feeding claims from `given/` leaves it unmoved), and the mtime fallback resets on clone/worktree — `date:` frontmatter is the honest source. Fail-open like the rest of the append.

### 3. Write Triggers row
New row: event "the day's decisions, at a user-signed closing (the Capture Moment sweep)" → destination "verification that phase-4 notes/claims exist; NEW `corpus/notes/*` + claim rows only for what the sweep surfaces un-captured" → phase "5 / session end". The event side stays disjoint from the phase-4 `corpus/notes/*` row: that row fires when something is SAID; this one fires at the CLOSING and only sweeps.

### 4. Battery: new kb-only module `test_kb_capture.py`
Doctrine anchors (whitespace-normalized): section present; the sweep question wording; "once per session"; idempotent-sweep clause; the provenance mapping (ELICITED/DERIVED/RULING-only-on-contested); "never a decision park"; the declared residual; the Write Triggers row; the recency-line forms and its named limit. Orient tests: notes with `date:` frontmatter → dated line; note without `date:` → mtime fallback; empty notes dir → `no notes yet`; no corpus → no line; notes WITHOUT topics/ → line still prints. Mutation both ways. kb-only, outside the shared manifest.

### 5. Eval scenarios (kb only, two)
- `capture_channels_the_days_decisions.md`: existing `pricing` topic (canonical `## Claims`, 8 columns, legal locators); prompt: a working exchange where the user states a decision ("quotes above 50k need my sign-off") and closes ("ok chiudiamo"). Pass: the sweep question fires once; the answer's capture lands as an `origin: elicited` + `date:` note and an L1 claim row (`prov: ELICITED`, empty id, `L<a>-<b>` source) on `pricing`; no new topic; nothing re-captured twice.
- `capture_stays_silent_with_nothing_to_record.md`: same setup, a purely mechanical exchange, user closes. Pass: the sweep question fires (the closing was signed); on "niente" no note, no claim, no ritual output beyond the one question.

### 6. Carriers
kb `README.md`: capability point 7 (the capture moment, one short paragraph incl. the recency line's named limit). kb `CHANGELOG.md` `[Unreleased]`: F-040 entry appended under the F-039 block.

## Impact
| File | Change |
|---|---|
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | new section + Write Triggers row |
| `.../scripts/sdlc_check.py` | recency line in `kb_cmd_orient` (date-frontmatter first, mtime fallback) |
| `.../scripts/test_kb_capture.py` | NEW kb-only module |
| `.../evals/scenarios/capture_channels_the_days_decisions.md` | new |
| `.../evals/scenarios/capture_stays_silent_with_nothing_to_record.md` | new |
| `distributions/kb-agentic-skill/README.md` | capability point 7 |
| `distributions/kb-agentic-skill/CHANGELOG.md` | [Unreleased] F-040 entry |

All kb-lens; no shared-spine file; `taxonomy.md`, `templates.md`, `reconciliation.md` untouched (rails reused, not changed). Code and mkt lenses unaffected.

## Security and Threat Model
- **T1 noise** — mitigations: user-signed closings only, ONE sweep question, once per session, silence legal at unsignaled ends, the recency line is one line gated on `corpus/notes/` existing.
- **T2 smuggled scope** — the no-smuggle clause; placement stays L3; unplaced never a park; anchored in the battery.
- **T3 fabricated capture** — elicited notes carry the user's words from the sweep's ANSWER, never inferred; the negative-branch scenario tests that "niente" produces nothing.
- **T4 false freshness** — the mtime-lies-after-clone limit is named where the line is defined; `date:` frontmatter is primary.
- No security surface: doctrine + a read-only date/mtime probe in orient.

## Test Strategy
Battery RED→GREEN on the new module; mutation bites both ways; recency probe unit-tested (5 states); both eval scenarios seed canonically under the fenced harness; `check --hybrid` CLEAN at closure; kb battery fully green.

## Action Plan
1. SKILL.md section + Write Triggers row.
2. Recency line in `kb_cmd_orient` + its tests.
3. `test_kb_capture.py` complete; mutation check.
4. Both eval scenarios.
5. README + CHANGELOG carriers.
6. Closure: kb battery, check --hybrid, REVIEW_LOG, handoff.

## Diary
- 2026-08-28 (implemented): design PASS at round 2 (0 open; 1 WARN folded during
  implementation: the sweep classified as a scheduled elicitation with its search
  result inline in the ask, anchored in the battery; the closing-signal wording nit
  fixed). Implemented in plan order; battery 289 OK first run after the module's 8/8
  (mutation verified RED->GREEN); both scenarios seed canonically under the fenced
  harness. One editorial slip caught by re-reading: the README point landed above
  point 6 and was moved below it.
- 2026-08-28 (R2): design review round 1 FAIL — 4 BLOCK + 6 WARN, all verified. The lead BLOCK was vision-level and went to the owner: the draft had silently reinterpreted the vision's mandated ASK into ambiguity-only questioning; the owner ruled to honor the wording (sweep question at user-signed closings). Also folded: operable closing points with the declared unsignaled-end residual (the phase-4 note duty is the real protection); recency from `date:` frontmatter with the mtime-lies-after-clone limit named (the skill's own worktree hygiene makes resets routine); unplaced-as-decision-park dropped (UNPLACED is topic-less scraps, invisible to recall); idempotent-sweep clause resolving the double-capture event overlap; explicit prov mapping; RULING bounded to contested-set resolution; reconciliation pointer; second (negative-branch) eval scenario; Write Triggers row anchored.
- 2026-08-28: unit opened on `feat/kb-capture-moment` off main@43dbea1. Design decision made before drafting: no SessionEnd/Stop hook — SessionEnd cannot reach the model and a Stop hook is per-turn noise; the honest by-construction limb is recency visibility in the F-039 orient append.
