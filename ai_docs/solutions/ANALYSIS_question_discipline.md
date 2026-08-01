---
id: F-026
feature: Question discipline (when a question to the user is legal)
status: IN_PROGRESS
level: L3
start_date: 2026-08-01
end_date:
---
# Feature Analysis: Question Discipline

## Objective

Field defect, reported by the owner: agents following the skill ask useless questions —
generic confirmations ("shall I proceed?"), questions the repo already answers, questions
that never say what is blocked without the reply ("spesso l'agente fa domande inutili
all'utente e non si capisce per quale ragione").

Where the doctrine invites it today:

- `elicitation.md` mandates a six-question round for every L3 whose skip path fires only
  when "an approved Vision or explicit user requirements already answer" — it never asks
  the agent to *derive* answers from the repo or the conversation first, so four of the
  six get asked even when the record answers them.
- The declared-assumption mechanism (proceed under a written assumption) exists only on
  the Unattended path. When the user IS reachable, the doctrine offers no alternative to
  asking, so agents interrupt for facts that could have been assumed and reviewed.
- No text anywhere states what makes a question legal. `SKILL.md` says "stop and ask" at
  several gates (Vision conflict, circuit breaker) with no form: nothing requires naming
  the blocked decision, so "ask for instructions" degenerates to "shall I proceed?".
- Contrast: the mkt sibling's `elicitation.md` already carries the cardinal rule ("ask
  only what the user uniquely owns; everything derivable from research comes from
  research") — the code skill never received its equivalent. And F-025's conflict ladder
  (kb) makes escalation non-blocking, batched, and formed (both claims, their sources,
  dates, why the machine cannot decide) — the same shape, never generalized.

**The fix**: a question-legality discipline in `elicitation.md`, governing every question
at every phase, discoverable via one cross-cutting line in `SKILL.md`.

## Feature Vision (alignment)

- **Success Signal 1** (cold-start operability: rule on a change "without asking the user
  for background") — this widens the signal from cold start to the whole session: the
  agent asks only what no artifact can answer. Baseline: the signal today binds only the
  Vision reviewer scenario.
- **Actor 1** ("never re-explaining the project across sessions") — a useless question is
  a forced re-explanation.
- **Ceremony budget disclosure** (Non-Goal 3 requires it; "omission resolves against the
  proposal", so the figures are measured, not estimated): `elicitation.md` goes from 60
  to 129 lines — **+84 / −14, net +69** — of which the discipline section is ~50; one
  existing anti-pattern bullet ("Asking what the approved vision already answers") is
  absorbed, the other two are kept verbatim. `SKILL.md` gains **one** bullet under Rule
  Zero — the only always-read cost; `elicitation.md` itself is read at L3 phase 3, or
  when an agent is about to ask. **L1 pays nothing**: no step, no field, no check — an
  L1 that asks nothing never reaches the rule, and one that would ask now asks better.
  What it removes is user-side: the interruption cost of illegal questions. The added
  ceremony sits above L1, so Non-Goal 3's budget branch applies — the cost is stated
  here and the owner accepts it explicitly by merging.

## Use Cases / User Needs

Actor: the solo developer / team lead running the skill (project_vision.md `## Actors`).

- **UC1 — repo-answerable ambiguity.** Mid-L3 the agent is unsure of a constraint. It
  searches the repo/corpus and proceeds; no question reaches the user.
- **UC2 — genuine fork.** Two viable designs, the choice turns on a priority only the
  user owns, and building on the wrong one is rework of the unit. The agent asks ONE
  blocking question carrying the mandatory form (fork, evidence, why it is the user's
  call, what is blocked).
- **UC3 — minor unknowns.** Unknowns that no fork of the work depends on: declared
  assumptions in the artifact, presented batched with the round or the deliverable —
  answered by exception, never a drip.
- **UC4 — the confirmation impulse.** The agent wants reassurance ("is this ok?"). Not
  legal: either the process already authorizes proceeding, or there is a real risk — in
  which case it is named and becomes UC2.

## Capability Ledger

| Capability | Verdict | Where / gap | Evidence |
|---|---|---|---|
| Rule a candidate question legal/illegal | **MISSING** | no owner; this feature adds it to `elicitation.md` | searched `elicitation.md` (round + anti-patterns, no legality test), `SKILL.md` (gates say "stop and ask", no form), `review.md` (escalation surfaces findings, no question form), `vision.md` (anti-question in spirit, no rule) |
| Proceed under a written assumption | **EXISTS — reach extended** | `elicitation.md` Unattended path | mechanism kept; the discipline extends it to attended sessions as the non-blocking default |
| Escalation form (both sides + evidence + why undecidable) | **EXISTS in the family, INADEQUATE here** | F-025 ladder escalation (kb, in flight); `review.md` round-cap escalation surfaces artifact+findings but prescribes no question form | generalized into the blocking-question form; `review.md` (shared) untouched — the form binds at the point of asking, which the discipline owns |
| Validate a question's legality at runtime | **not buildable** | the validator never sees the conversation | honest limit: no check can rule on a question that was asked in chat |
| Assert the doctrine is WIRED | **EXISTS** | `test_skill_invariants.py` `@requires(...)` / `OPTIONAL_CAPABILITIES` (`sdlc_core.py:242`) | the family convention — every doctrine feature ships one (F-016 `test_rule_zero_declares_router_verdict`, F-018 `test_vision_discipline_wired`, F-020 `test_architect_pass_wired`). Used here: `question_discipline` capability + `test_question_discipline_wired`. An unconditional assertion would fail mkt (its `elicitation.md` differs); the gate is what makes it shippable in the shared battery |

## Impact

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/elicitation.md` | MODIFY | new `## The question discipline` section; skip path extended with "or derivable (name the sources)"; `## The round` gains "Derive before asking"; two anti-pattern bullets absorbed into the section |
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | one cross-cutting bullet under Rule Zero pointing at the discipline (questions happen at all levels; a rule only L3-phase-3 readers see never reaches them) |
| `scripts/sdlc_core.py` ×3 | MODIFY | `question_discipline` added to `OPTIONAL_CAPABILITIES` — shared spine, so the capability name exists in every distribution and "kb does not claim it" is a visible decision, not a silent absence |
| `scripts/test_skill_invariants.py` ×3 | MODIFY | `test_question_discipline_wired`, `@requires("question_discipline")`: asserts the section in `elicitation.md` AND the bullet on `SKILL.md`'s always-read path. Skips in kb/mkt until they adopt it |
| `scripts/sdlc_check.py` (sdlc only) | MODIFY | this distribution claims the capability |
| `scripts/shared_files.py` ×3 distributions | MODIFY | boundary record: `elicitation.md` is today in NEITHER `SHARED_FILES` nor `NOT_SHARED_ON_PURPOSE`, and the mkt copy has already silently diverged — exactly the "absence nobody notices" the manifest exists to prevent. Added to `NOT_SHARED_ON_PURPOSE` with the reason |
| `scripts/shared_manifest.json` ×3 | REGENERATE | `shared_files.py`, `sdlc_core.py` and `test_skill_invariants.py` are all in `SHARED_FILES`; copied verbatim + `--update` in each distribution |

**Why the discipline is not split into the shared spine (the alternative, argued).**
`review.md` and `vision.md` are shared because each is a whole file of domain-neutral
doctrine. The discipline is a *section inside* a file whose remainder is domain-specific
— mkt runs question waves, not the six-question spec round, and its copy already
diverges. Splitting it into a fourth shared file would add a file to every distribution's
support-file list (ceremony in two domains to fix a defect reported in one) and would
still need per-domain wiring. Chosen instead: the capability name lives in the shared
spine, the text lives per-domain, and the gated test makes each sibling's non-adoption a
visible decision. **Named follow-up, not silently dropped:** kb's `elicitation.md` is
byte-identical to sdlc's today and is being reshaped by F-024 on its own branch — it
adopts the section there; mkt carries the cardinal rule already (`elicitation.md:5`) and
owes the non-blocking default, the search-naming duty and the blocking form. Both are
handoff rows, not this unit's scope.

Blast radius of `elicitation.md` (all consumers enumerated by grep over the skill dir):
`architect.md:3` (sequencing — unchanged), `vision.md:50` (benefit-first — unchanged),
`templates.md:250` (actors from round — unchanged), `SKILL.md:63,216` (trigger — 216
untouched, discipline referenced from Rule Zero instead), `sdlc_check.py:52` (filename
list — unchanged), `test_skill_invariants.py:187` (asserts "benefit" present — preserved).
kb's and mkt's `elicitation.md` are NOT touched: kb's is being reshaped by F-024 on its
own branch; mkt's already has its domain form of the rule.

## Security and Threat Model

No code, no parsing, no network, no filesystem surface beyond doctrine text. Process
risks instead:

| Risk | Mitigation |
|---|---|
| Over-suppression: agent silently guesses a genuinely user-owned call | the "what the user uniquely owns" list keeps intent/priority/approval askable; the waste test makes those blocking; declared assumptions are written in the artifact, so a wrong guess is visible to the design/closure review, never silent |
| Under-suppression: agent games "I searched" | the question must NAME what was searched — the family's falsifiability pattern (router verdict, EXISTS row): a search not named is indistinguishable from a search not run, and is treated as such |
| Discipline read as "never ask" | the section opens by naming the round as the planned question cost, and doctrine-reserved approvals stay blocking by design |

## Action Plan

1. Draft this ANALYSIS; design review (moment 1, independent subagent) before any edit.
2. Apply the `elicitation.md` and `SKILL.md` edits.
3. Record the boundary in `shared_files.py` ×3; regenerate the three manifests.
4. Run the three distributions' test batteries + `sdlc_check.py check` + `index`.
5. Closure: REVIEW_LOG row, handoff row (AWAITING OWNER — merge), flip COMPLETED.

## Test Strategy

Two layers, and the boundary between them is stated because the second cannot exist:

- **Wiring is tested.** `test_question_discipline_wired` (capability-gated) fails if the
  discipline section leaves `elicitation.md` or the bullet leaves `SKILL.md`'s always-read
  path — the regression this feature is most exposed to, since doctrine text has no
  compiler. Plus the standing batteries: drift guard (the spine propagated to three
  distributions), `test_vision_discipline_wired` (the round still asks for the benefit),
  `sdlc_check.py check`.
- **Behavior is not testable here.** No check sees a conversation, so "the agent asked a
  legal question" is out of reach of the validator. Its home is the eval harness
  (`evals/scenarios/`), cold-run: a repo-answerable unknown must produce no user question,
  and a genuine fork must produce one carrying the four form elements. Left as owner-run
  field verification, in the shape the existing `consult_fires_on_match.md` scenario uses.

## Diary

- 2026-08-01 — opened from the owner's field report; investigation, design, implementation.
  Design review round 1: **FAIL** — 1 BLOCK, 5 WARN, all real, all fixed before implementing.
  The BLOCK was the always-read `SKILL.md` paraphrase dropping the reserved-approvals
  branch, which would have outlawed the doctrine's own mandated waits (devPNT proposal
  confirmation, Vision conflict, merge decision) for any agent that never opens
  `elicitation.md` — the "restated facts diverge" defect `review.md` already names. Also
  fixed: the reserved list did not cover the doctrine's own mandated STOPS (circuit
  breaker, review round-cap), so the discipline could be read as outlawing them; a stale
  unattended-path justification; understated cost figures; a wrongly-rejected test
  alternative (the `@requires` gate makes the assertion shippable); and the unargued
  shared/per-domain placement.
- Design review round 2 (same reviewer, on the implemented state): **INCOMPLETE — the
  reviewer process died on an API session limit before writing a verdict.** Not a PASS,
  and recorded as such. Two findings it did reach are salvaged from its partial output
  and both are fixed: (a) the ANALYSIS frontmatter still said `PLANNED` while the code
  was implemented — SKILL.md phase 4 mandates the `PLANNED → IN_PROGRESS` flip and the
  handoff row already said IN_PROGRESS, so the two states had diverged; (b) the
  reserved-blocking clause imposed the four-element form on the doctrine's own mandated
  stops, where `debugging.md` (minimal reproduction / what was ruled out / best
  hypothesis) and `review.md` (artifact + open findings) already prescribe a hand-over —
  two forms over one moment, the duplicate `review.md` §Reviewing forbids, and a stuck
  agent has no "fork" to name. Fixed by citing the owning file instead of restating it.
  **Open**: the rest of round 2 never ran. The gate's rule is to surface open state to
  the human rather than block (`review.md`: a gate that can block forever gets removed),
  so this is the owner's call at merge — re-run the round after the limit resets.
- Repo-level `sdlc_check.py check` reports NOT CLEAN on `stale` — **pre-existing**,
  identical at the parent commit before any edit here (areas `skills/`, `scripts/`,
  `distributions/` unmarked since the consolidation). Not laundered with a `mark` this
  change did not earn: marking 153 distribution files as re-analyzed would be the
  unfalsifiable claim the family's own rules forbid. `validate` is 0 errors.
