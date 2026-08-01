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
  proposal", so every figure below is measured, and re-measured after the last edit —
  the review caught stale numbers twice, which is why the commands are named).
  `elicitation.md`: **60 → 169 lines**, `git diff --numstat HEAD~1` = **+123 / −14, net
  +109**, of which `## The question discipline` is **117 lines**. One existing
  anti-pattern bullet ("Asking what the approved vision already answers") is absorbed;
  the other two are kept. The section is that long because the review's successful
  evasions each cost a clause — the search floor, the reversibility fix, the precedence
  rule, the closed prescribes-list, the waste-test element. `SKILL.md` gains **one**
  bullet under Rule Zero: **416 characters / 76 words**, and deliberately the *shortest*
  path to the rule — it cites `elicitation.md` and states the two-condition test, and
  enumerates nothing, because a second copy of the never-legal forms is what diverged in
  round 1 (the longest existing cross-cutting bullet is 597 chars, so this one is not
  the largest thing on the always-read path).
  **What L1 pays, stated honestly** (Goal 4 counts what the agent must read as real
  cost, so "L1 pays nothing" would be false): L1 pays **no step, no field, no check, no
  artifact** — and **76 words of always-read text**. `elicitation.md` itself is read at
  L3 phase 3, or when an agent is about to ask. What it removes is user-side: the
  interruption cost of illegal questions, at every level including L1. The added
  ceremony sits above L1, so Non-Goal 3's budget branch applies — the cost is disclosed
  here in the figures above, and the owner accepts it explicitly by merging.

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
| Over-suppression: agent silently guesses a genuinely user-owned call | the "what the user uniquely owns" list keeps intent/priority/approval askable, and an explicit **precedence rule** makes it win over the never-legal list — without which "it is reversible ⇒ preference-fishing ⇒ never legal" was a one-clause licence for silence (round 2, finding 4). Reversibility is no longer a sufficient condition; equivalence is measured on the benefit |
| Under-suppression: agent games "I searched" | naming the search is not enough on its own — the question states **terms, tools, areas AND what they returned**, a search whose scope misses the question is not a search, and faking is named as such. The floors are imported from `architect.md`'s provisional-MISSING and `guides.md`'s never-fake-the-verdict, not merely their vocabulary (round 2, finding 2 — the first draft cited the pattern while shipping a weaker rule) |
| "Assume it" becomes the way to skip the standard | the non-blocking default carries the **same** evidence duty as a question: source (`I take X from Y`), the excluded alternative, and mandatory batch presentation. This is also where the F-025 keep-both-with-sources mechanism actually lands (round 2, finding 3) |
| Agent calls something a "fork" to force a question it wants to ask | the mandatory form has an element that only case (a) can answer — **why no assumption survives**: what work is discarded if you assume wrong. Without it, case (a) was the one blocking case the form could not falsify (round 2, finding 8) |
| Discipline read as "never ask" | the section opens by naming the round as the planned question cost; doctrine-reserved approvals and doctrine-mandated stops stay blocking by design, and the prescribes-your-own-hand-over exemption is a **closed two-file list** so a stop cannot escape the form by silence (round 2, finding 5) |

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
- Design review round 2, first attempt: **INCOMPLETE — the reviewer process died on an
  API session limit before writing a verdict.** Two findings it reached were salvaged and
  fixed: the ANALYSIS frontmatter still said `PLANNED` while the code was implemented
  (SKILL.md phase 4 mandates the flip; the handoff row already said IN_PROGRESS, so the
  two states had diverged), and the reserved-blocking clause imposed the form on top of
  `debugging.md`'s and `review.md`'s own prescribed hand-overs.
- Design review round 2, **re-run on the committed state (fresh reviewer, deep tier):
  FAIL — 4 BLOCK, 5 WARN, all evidenced, all fixed.** The round earned its cost: three of
  the four BLOCKs were **working evasions**, not formatting. (1) Cost figures wrong again
  after the round-2a edits — now re-measured with the commands named in the disclosure.
  (2) The search-naming duty cited `architect.md`/`guides.md` as its standard while
  shipping neither's floor, so *"I grepped for 'timeout' and it isn't there — which
  timeout do you want?"* passed both criteria. (3) The non-blocking default — where most
  traffic goes — carried **no** evidence duty at all, so "declare an assumption" was the
  way to skip the entire standard; it is also where F-025's keep-both-with-sources
  mechanism structurally belongs, and the first draft had attached its vocabulary to the
  blocking branch instead. (4) "Reversible" was a **sufficient** condition for
  preference-fishing, and nearly everything is reversible under git — a one-clause
  licence for silence, decided against the intended reading by `vision.md`'s own
  first-sentence-wins precedence rule. Fixed with a precedence clause. The WARNs closed
  the prescribes-list gap, added the element that makes the waste test falsifiable, made
  the Rule Zero bullet a citation rather than a second copy (it had already diverged —
  it dropped "re-asking the record", the exact form the owner's report named), corrected
  the L1-pays-nothing claim against Goal 4's reading-cost rule, and made the
  `shared_files.py` boundary comment true about kb.
- Repo-level `sdlc_check.py check` reports NOT CLEAN on `stale` — **pre-existing**,
  identical at the parent commit before any edit here (areas `skills/`, `scripts/`,
  `distributions/` unmarked since the consolidation). Not laundered with a `mark` this
  change did not earn: marking 153 distribution files as re-analyzed would be the
  unfalsifiable claim the family's own rules forbid. `validate` is 0 errors.
