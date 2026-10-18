---
id: F-074
feature: Vision born from an owner interview
description: Every Vision (every lens, the M-VISION included) is written only after a six-question owner interview and an owner-approved north star; elicitation's skip path no longer reaches a Vision; bootstrap writes a stub, never a reconstructed Vision; a Non-Goal bounds scope and is not a ban.
status: COMPLETED
level: L3
domain: code
topics: [vision-gate, elicitation, anti-myopia]
start_date: 2026-10-18
end_date: 2026-10-18
branch: feature/vision-interview
---
# Feature Analysis: Vision born from an owner interview

**For whom**: the independent design reviewer, then the owner. **To do what**: confirm
that the applied doctrine closes the field case below without adding ceremony outside
Vision authoring. **Does not answer**: how downstream artifacts weigh the owner's core
promise (F-071, `ANALYSIS_intent_focus.md`, M2–M4).

Owner statements: `audit/requests/REQUEST_vision_interview.md` R1 (request and the
interview structure, decided with the owner), R2 (family-wide scope), R3 (bootstrap
writes a stub), R4 (approval of the diff). Elicitation: not skipped — R1 carries the
structure verbatim; the two real doubts were asked (R2, R3). Proposed and applied diff:
`harness_vision_interview/proposed.patch`.

## Objective

A Vision the author writes alone passes every gate the skill has. In the field case
(R1: a Hybrid milestone, 2026-10-18) the author drafted the M-VISION from one sentence
and a spike through elicitation's skip path, imported a product-Vision constraint as a
ban, dropped the north star and the actor holding the initiative; the blind check
passed three rounds, and D-UC, D-IC, P-TM and an E-ISP were built on it until the E-ISP
review raised 6 BLOCKs, almost all from the imported constraint.

**Mechanism** (named before the fix): three texts let it through.
1. `elicitation.md` skip path: "explicit user requirements … already answer goal, scope,
   and constraints" admitted a one-line request plus a spike as a complete Vision spec.
2. `vision.md` §6: the blind check tests whether rules survive a hostile reader; nothing
   tested whether the Vision is the owner's, and no gate preceded drafting.
3. Bootstrap (`SKILL.md` Write Triggers, Phase 1) mandated an agent-reconstructed Vision,
   normalizing Vision text with no owner behind it.
A fourth, conceptual: the templates called Non-Goals "your ENTIRE rejection surface",
which invites writing a behaviour ban as a Non-Goal (R1: "un NON-GOAL non è un divieto").

## Feature Vision

`vision/project_vision.md` is APPROVED. This unit serves its first Goal — "Make the
project's intent readable and *operable*" — and the North Star's "traceable to the
project's declared intent": a Vision that is not the owner's declares no intent.

**Ceremony disclosure** (`project_vision.md` Non-Goal "No ceremony ratchet", budget
clause). Level: L3 only, and only in a unit that writes or amends a Vision (any lens,
the M-VISION included); L1/L2/E1/E2 and L3 units that cite an existing Vision gain no
step. Added per such unit: one interview (six questions in one numbered set, re-asked
only on a wrong-form answer) and one Gate-1 stop for the north star; the answers go to
the request record that every L3 already keeps (r26). Removed: the agent-reconstructed
Vision at bootstrap (now a 4-line stub). Doctrine read, UTF-8 LF bytes added: code SKILL
+992, elicitation +669, templates +2760; kb SKILL +450, elicitation +686, templates
+2513; mkt SKILL +405, elicitation +362, templates +1128; course SKILL +155,
elicitation +686, templates +595; shared `vision.md` +4792 (read only when writing a
Vision). The owner decided the step (R1); explicit acceptance of the cost and the
precedent row (`vision/rulings.md`, new r30) are asked at closure.

## Use Cases / User Needs

Actors are the project Vision's (owner = the person whose intent the Vision declares;
agent = the author). Names: *owner interview*, *Gate 1*, *Gate 2* are NEW (declared
here); *Vision*, *M-VISION*, *blind check*, *skip path*, *request record* EXIST.

| UC | Actor | Need | Traces to |
|---|---|---|---|
| UC1 | owner | the Vision states my benefit, my actors and my boundaries, not the author's inferences | Goal 1 |
| UC2 | owner | approve the north star in my words before drafting, so a wrong premise costs one sentence, not four artifacts | Goal 1; "divergence visible before implementation" |
| UC3 | agent | know, with no judgement call, that a sentence plus a spike does not license writing a Vision | Goal 1 |
| UC4 | reviewer | tell where each Vision rule came from (owner, higher Vision, confirmed inference) | Goal 1 |

## Functional Spec

1. Any unit that writes or amends a Vision — project, feature, lens, M-VISION, or an
   ANALYSIS Feature Vision stating a benefit no Vision names — runs the owner interview
   (`vision.md` §The owner interview). No skip path.
2. Six questions, in order; each repeated until its answer has the stated form
   (Problem, Benefit, Actors with initiative, Success with starting value, Boundaries,
   Known constraints with provenance). Author-derived answers are proposals for the owner.
3. Gate 1: a 1–2 sentence north star in the owner's words, explicitly approved, recorded
   verbatim in the request record. Without it no Vision text exists, not even DRAFT.
4. Gate 2: the Vision written from the answers, every rule with provenance; blind check
   (holds) + approved north star (is the owner's); the owner's confirmation promotes it.
5. Bootstrap writes `vision/` stubs awaiting the interview; observations go to `strategic/`.
6. A Non-Goal bounds scope: it rejects proposals pursuing it, bans no existing behaviour,
   creates no obligation; behaviour bans are Invariants or sourced constraints.
7. Unattended: the unit is `BLOCKED on the user`.

Acceptance: the scenario `evals/scenarios/vision_needs_owner_interview.md` passes; the
static regression (`scripts/test_vision_interview.py`, `test_vision_born_from_owner_interview`)
is red on the pre-F-074 text and green after.

## Interface Contract

Two surfaces. (1) The agent→owner question channel, governed by `elicitation.md`
§The question discipline. Reused idiom: one numbered set, structured-question facility
where present, answers verbatim in the request record; the interview is declared a
planned occasion like the round (`elicitation.md` Vision path), so the blocking form
does not apply to its questions. New idiom (declared): the interview is a mandated stop —
legal by mandate, like reserved approvals — so the "re-asking the record" ban does not
suppress it; a reply already on record is read back for confirmation. A Vision written
outside any unit records its interview in `REQUEST_project_vision.md` (`vision.md`).
(2) The installers: `agentic-sdlc-init` and the sibling `init.js` seed the project's
Vision file; after this change they seed the stub.
Flow: owner request → agent opens interview (six questions) → owner answers (recorded) →
agent proposes north star → owner approves (recorded) → agent drafts → blind check →
owner confirms (APPROVED).

## Capability Ledger

| Capability | Verdict | Where |
|---|---|---|
| Ask the owner structured questions and record answers | EXISTS | `elicitation.md` §The question discipline; `REQUEST_*` record (`templates.md`) |
| Gate Vision promotion on owner confirmation + blind check | EXISTS | `vision.md` §6; `SKILL.md` Vision Gate |
| Gate Vision *drafting* on owner-authored premise | MISSING (searched: `vision.md`, `elicitation.md`, `SKILL.md`, `templates.md`, `hybrid.md` in all four lenses) | added: `vision.md` §The owner interview (shared) |
| Distinguish scope bounds from behaviour bans | INADEQUATE | template said Non-Goals are the entire rejection surface; amended in `vision.md` §3 and templates |

Guide check: no CURRENT guide covers Vision authoring (router: two guides, release and
shared memory); no high-complexity code component was modelled — no guide owed.

## Impact

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/vision.md` (+3 sibling copies, shared) | MODIFY: §The owner interview; §3 Non-Goal bullet; §6 states what the blind check cannot see | mechanism 2 and 4; FS 1–4, 6 |
| `skills/agentic-sdlc-skill/elicitation.md`, kb, course | MODIFY: skip path never covers a Vision; Vision path paragraph; kb/course unattended parenthetical | mechanism 1; FS 1 |
| `distributions/mkt-agentic-sdlc/.../elicitation.md` | MODIFY: skip path never covers the MKT-VISION | mechanism 1 |
| `SKILL.md` ×4 | MODIFY: Write Triggers row + bootstrap → stubs; Vision Gate names the interview (code: Standalone + Hybrid); course/mkt drafting lines | mechanism 3; FS 5 |
| `skills/agentic-sdlc-skill/templates.md`, kb `templates.md` | MODIFY: stub as the first fenced Vision block; North Star in owner's words with approval cite; Core Problem as a case; Actors with initiative; Signals with starting value; Non-Goals as scope with provenance per rule; feature Vision template with North Star/Problem/provenance; code: ANALYSIS `## Feature Vision` pointer | R1 "sezioni Problema e North star, con la provenienza di ogni regola"; R3 |
| mkt `templates.md` | MODIFY: MKT_VISION stub as first block; North Star, Problem, initiative, starting value, Non-Goals as scope, Constraints with provenance | same, mkt section names |
| course `templates.md` | MODIFY: course Vision gains North Star and Problem; learners with initiative; signals with starting value; Non-Goals as scope; constraints with provenance | same, course section names |
| `scripts/init.js` (code), kb and mkt `init.js` via `scripts/lib.js` `templateFor(sections, needle, 0)` | UNCHANGED code, CHANGED output: they seed the first fenced block of the Vision section, which is now the stub | R3; consumer of `templates.md` found by the review |
| `distributions/course-creator/scripts/init.js` | MODIFY: its literal project-Vision seed becomes the stub | R3 |
| `scripts/test_skill_invariants.py` (shared ×4) | MODIFY: `test_vision_born_from_owner_interview` — wiring, and that what bootstrap seeds is the stub (templates' first Vision block, or init.js's literal) | family-wide wiring + seeding guard |
| `scripts/shared_manifest.json` ×4 | regenerated | drift guard |
| `skills/agentic-sdlc-skill/scripts/test_vision_interview.py` | ADD (code lens only) | regression of the field case + scenario teeth |
| `skills/agentic-sdlc-skill/evals/scenarios/vision_needs_owner_interview.md` | ADD | behavioral replay of the field case |

**Not changed, deliberately:** `hybrid.md` (both lenses) — no passage contradicts the
change (lines 26, 35–36, 53–54, 65 read), and the `SKILL.md` Vision Gate Hybrid bullet
carries the rule (the F-051 digest pins only the block from `### Hybrid in symbiosis
with devPNT` onward, so an edit was possible but is not owed); `sdlc_core.py` — a stub keeps `Status: DRAFT`,
so the validator's advisory path already covers it (`test_new_checks_never_redden_strict_ci`
stays green).

Blast radius (text anchors other code reads; `git grep` over the repo, no symbol graph
applies to prose): the installers read `templates.md` (`scripts/lib.js` `templateFor`,
first fenced block per section — missed in round 1, found by the design review); tests reading `vision.md`/`elicitation.md`/`SKILL.md`/`templates.md`
anchors — `test_vision_discipline_wired`, `test_question_discipline_wired` (its
"Unattended path" anchor kept), `test_new_checks_never_redden_strict_ci` (DRAFT bootstrap,
unchanged), `test_hybrid_seam_moved_not_deleted` (hybrid untouched). Prior ANALYSIS files
that took the skip path (`ANALYSIS_authoring_floor.md` and nine others) wrote no Vision —
unaffected. F-071 (`ANALYSIS_intent_focus.md`) hypothesis M1 is closed for Vision authoring
by this unit; M2–M4 stay with F-071.

Populations at rest: trigger 1 fires (the guarantee "Vision is the owner's" moves from
promotion time to drafting time). Existing APPROVED Visions were written under the old
regime and are not re-interviewed (no migration requested); they are re-interviewed on
their next amendment, for the questions the amendment changes. Existing bootstrap DRAFT
Visions stay DRAFT and keep informing only; the first L3 that needs one runs the
interview. This repo's own `project_vision.md` (APPROVED v9) is in that population.

## Security and Threat Model

No input parsing or network surface. One filesystem surface changes output, not code:
the installers write the Vision stub instead of the full template into the user's project
(new-project only — `init.js` does not overwrite an existing file).

| ID | Risk | Mitigation |
|---|---|---|
| T1 | Ceremony creep: the interview fires on work that writes no Vision | Scope sentence in §The owner interview; an ANALYSIS citing an existing Vision is alignment, not a Vision |
| T2 | The interview is faked: the agent fills answers itself | "an answer the author derived … is a proposal the owner confirms"; answers verbatim in the request record, which reviews check |
| T3 | Interrogation: six questions drip-fed | elicitation's one-numbered-set rule and anti-patterns apply unchanged |
| T4 | Unattended runs stall silently | `BLOCKED on the user`, the existing unattended path |
| T5 | Shared-file divergence across lenses | drift guard + regenerated manifest; four batteries run |
| T6 | An installer seeds a full Vision template again (template reordered, seeder changed) | `test_vision_born_from_owner_interview` asserts the seeded block or literal is the stub, in every lens |

## Action Plan

- [x] Request record R1–R4; doubts R2, R3 asked before writing
- [x] Proposed diff shown to owner; approved (R4); applied
- [x] Shared files propagated; manifest regenerated; four batteries green
- [x] Probe: new tests red on old text, green on new
- [x] Independent design review round 1 (FAIL, 2 BLOCK + 6 WARN) — all folded
- [x] Design review round 2 PASS + REVIEW_LOG row
- [x] Owner: explicit cost acceptance and ruling r30 in `vision/rulings.md` (R5)
- [x] Version bump ×4 (1.43.0, kb 1.26.0, mkt 0.21.0, course 0.1.0-beta.7), CHANGELOG entries, README and family-workflow alignment; E2E_TEST; closure review PASS; MERGE_REVIEW; `mark`; `check` CLEAN; commit
- [ ] Release (owner): tags, merge to main, `publish_all.bat` — `GUIDE_release.md` steps 5–9

## Test Strategy

Static (gating): `test_vision_born_from_owner_interview` in all four lenses;
`test_vision_interview.py` in the code lens — skip path, gates, question order, bootstrap,
Hybrid bullet, scenario teeth. Replay (2026-10-18, scratch copies): 5 + 1 tests red on the
pre-F-074 text (4 failures + 1 error, 1 failure), green on the patched text. Behavioral
(non-gating): run `evals/run_behavioral.py scenarios/vision_needs_owner_interview.md`.
Seeding (2026-10-18): `init.js` of all four packages run in scratch projects with a
stubbed HOME — each wrote the stub. The seeding assertion is red on `main`'s
templates. Batteries after the round-1 fixes and `index`: code 393 OK, kb 579 OK, mkt
400 OK, course 395 OK; JS client tests: code 53/53, course 4/4.

## Diary / Current State

- 2026-10-18 — Unit opened from the owner's request (R1). Doubts asked: placement (R2,
  family-wide via shared `vision.md`) and bootstrap (R3, stub). Diff drafted, probed
  red/green, shown; `hybrid.md` dropped from the diff because of the F-051 digest.
- 2026-10-18 — Owner approved (R4). Patch applied, `vision.md` and the shared battery
  copied to kb, mkt, course; manifest regenerated; four batteries green.
- 2026-10-18 — Design review round 1 FAIL: kb/mkt/course templates had received only
  part of the template change (kb still called Non-Goals the entire rejection surface);
  the installers seed `templates.md`'s first block, a consumer the Impact missed, and the
  threat model wrongly said no filesystem surface changed. Fixed: sibling templates
  completed, stubs made the seeded block (course: its literal seed), seeding test added,
  interview declared a planned occasion, record location for a unit-less Vision, cost
  disclosed, hybrid.md reason corrected.
- 2026-10-18 — Design review round 2 PASS; its one new WARN (kb/course elicitation
  counted two planned occasions, now three) folded. Batteries green in all four lenses;
  `validate` clean; `stale` lists this unit's files, recorded by `mark` in the release
  commit. Waiting on the owner's cost acceptance and ruling r30.
- 2026-10-18 — Owner accepted the cost and ruled r30 ADMIT (R5). Bumped the four
  packages, wrote CHANGELOGs, aligned READMEs and the family workflow document, wrote
  the E2E script. Closure review PASS with three WARNs (kb README line, FS7 scenario,
  state lag), all folded. Committed on `feature/vision-interview`; release not started.
