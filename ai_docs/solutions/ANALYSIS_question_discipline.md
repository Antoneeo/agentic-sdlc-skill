---
id: F-026
feature: Question discipline (a real doubt is asked when it emerges; a question is legal only after the search)
status: COMPLETED
level: L3
start_date: 2026-08-01
end_date: 2026-09-25
---
# Feature Analysis: Question Discipline

## Objective

Two field reports from the owner, pointing in opposite directions, govern this feature.

- **2026-08-01, too many questions.** Agents asked useless ones: generic
  confirmations, questions the repo answers, questions that never say what they
  unblock.
- **2026-09-25, doubts kept silent.** Doubts never surface, flow into the written
  documents, and stay there unless the owner notices ("ci sono dei dubbi che non
  emergono e che si riversano nei documenti scritti e se non me ne accorgo restano
  lì").

The first report produced the legality test that `elicitation.md` carries in all three
lenses. That test stays. The second report comes from three leaks in the text that
answered the first:

1. **Nothing defines when a doubt has emerged.** An agent that settles an ambiguity
   by picking a plausible reading sees no doubt, so it neither asks nor declares an
   assumption. Nothing requires it to state what the reading rests on, so the choice
   enters the artifact indistinguishable from the owner's intent.
2. **Intent can be "derived" from the repo.** The code lens's skip path and "derive
   before asking" let goal, scope and constraints be derived from the repo and the
   code. That includes the parts only the owner can state.
3. **The default hands doubts to the deliverable.** "Default non-blocking" writes an
   unknown into the artifact as an assumption, "answered by exception" with the
   deliverable. The owner has to find it inside the document to answer it. The code
   lens's Rule Zero repeats the bias on the always-read path: "Blocking the work is
   the exception, not the default."

**The fix: ask on real indecision, ground everything else.**

- **A real doubt is asked before any write that would embed its answer**, together
  with the other doubts open at that point. A real doubt is either a fact or an
  owner-held datum that the search leaves open and that changes the work, or two or
  more options that change the work, where weighing their pros and cons does not
  settle the choice.
- **Facts and information only the owner holds are never weighed.** They are
  settled by evidence, cited, or asked.
- **A choice whose pros clearly outweigh its cons is taken without asking.** The
  weighing and the option it rejects are written next to it ("I take X over Z: pro …,
  contro …"), so the document shows both the choice and what it rests on.
- **Every question explains the pros and cons of each answer it offers.**
- **Reserved approvals and doctrine-mandated stops are always asked.** They are
  legal by mandate and never pass through the weighing test.
- **A real doubt that passes the legality test is owed**, not merely allowed.
- **Declared assumptions stay only where no question can be asked:** the owner is
  unreachable, or the owner delegated the choice.
- **The independent design review is the second line.** An intent choice written
  without its ground is a finding.

**Elicitation (2026-09-25, two rounds, owner's replies).**

- **When:** as soon as the doubt emerges, all the doubts of that moment in one set.
  The owner rejected both the one-question-per-turn drip and a single list at the
  end of the document.
- **Facts:** search first. A fact the search does not settle, and that changes the
  work, is asked, not silently assumed.
- **Scope:** all three lenses.
- **What counts as a doubt.** Round 2, verbatim: "occorre fare attenzione a capire se
  è davvero una informazione che deve dare l'utente oppure se si tratta di scegliere
  fra varie opzioni in cui ci sia una reale indecisione … se una cosa è così
  probabile o raccomandabile, non deve chiedere." This is the real-indecision test
  above.
- **How to tell (third input, verbatim):** "per fare una domanda deve anche spiegare
  i pro e contro di ogni risposta e qualora lui stesso vedesse che i pro pesano di
  più dei contro allora non c'è bisogno di chiedere." This sets two rules. The weighing
  of pros and cons is the test for choices. The weighing travels with every
  question that offers options.
- **Unattended below the top level:** I take "proceed on a declared assumption,
  surfaced in the reply; stop blocked only at the top level (L3 in code and kb, E3 in
  marketing)" over "stop at every level".
  - Pro: unattended L1/L2 runs keep working, and the top level keeps today's stop.
  - Contro: a below-top-level assumption can be wrong until the owner reads the
    reply.
  - The owner's principle ("se una cosa è così probabile o raccomandabile, non deve
    chiedere") ruled on the options as presented, and it names no priority the
    weighing would need.
- **Pros and cons only where a question offers options:** I take "every option
  offered carries its pros and cons" over "every question carries pros and cons".
  - Pro: an open question ("what is the goal?") has no enumerable answers to weigh.
  - Contro: none found; an open question still names what it blocks.
- **Cost:** accepted explicitly. The exact question is quoted in the budget below.

Derived without asking, with ground:

- **Every level.** Ground: the owner's "ogni volta che emergono", and the existing
  rule's "any phase, any level".
- **The five-element form keeps the name "blocking form".** Ground: every question
  outside a planned occasion still stops the write, and `review.md` plus two
  scenarios cite that name.

## Feature Vision (alignment)

- **Core Problem (myopia).** A doubt settled silently is acting from partial
  understanding. The artifact then carries a guess as if it were intent.
- **Goal 3.** "Make divergence from the declared intent visible *before*
  implementation … surface it and let the user choose." The doubt is asked, or the
  choice shows its ground.
- **Goal 2.** "Nothing load-bearing lives only in a transcript." Answers and grounds
  are written into the artifact (`elicitation.md` §Reflect, unchanged).
- **Goal 4 / solo-developer Actor.** "Ceremony proportional to risk": a clearly
  preferable option costs one written line, not a question.
- **Team-lead Actor.** "Divergence … surfaced before the change is merged": the
  review clause.
- **Non-Goal 3 (ceremony budget).** Constant always-read text also reaches L1. The
  precedent is `rulings.md` r19: such text is admitted through the Non-Goal's second
  door, the cost disclosed in full and accepted by the owner. Every cost this change
  adds:
  - **Always-read text.** Baseline measured 2026-09-25: code 416 characters, kb 327,
    marketing 247. Target: at most +60 characters each.
  - **`elicitation.md`.** Baseline: code 173 lines, kb 133, marketing 147. Target: at
    most +30 net lines each.
  - **A new design-review check** at the top level: one bullet in `review.md`, at
    most 8 lines.
  - **More interruptions.** One question set per write point instead of one list
    with the deliverable, and outside the planned occasions each question carries the
    compact five-element form.
  - **A ground line ("I take X over Z: pro …, contro …")**, only when a candidate doubt is
    settled without asking. It replaces the assumption line the old default already
    required. At L1 the cost is zero unless a candidate doubt arises, and then the
    line goes in the reply.
  - **Unattended runs.** Unchanged in code and kb. Marketing gains an unattended path
    it did not have.

  **Owner acceptance, 2026-09-25, quoted.** The question: "La Vision vieta ogni
  aumento di cerimonia non accettato esplicitamente. Questo cambio aggiunge: circa 60
  caratteri nella riga di SKILL.md sempre letta (per lente), circa 30 righe in
  elicitation.md, un nuovo controllo nella design review L3, e più interruzioni per te
  (una serie di domande per step invece di un'unica lista finale). Accetti questo
  costo?" The reply: "Accetto".

  Three items came after that question and were not itemized in it: the ground line,
  the compact form on questions outside planned occasions, and pros and cons on every
  option at the planned occasions (the owner's own fourth input). Both replace a cost that
  already existed: the assumption line, and the form on blocking questions. The
  closure report names them so the owner can confirm them. Closure also re-measures
  the figures and reports any overrun before merge.

  **Measured at closure (2026-09-25).** The always-read line came in at 417, 385 and
  304 characters, within target. The `review.md` bullet is 7 lines. `elicitation.md`
  came in at 210, 185 and 210 lines (+37, +52, +63), over the +30 target. The owner
  was asked with the figures and replied "Accetto le cifre reali" (2026-09-25).
- **No other Non-Goal touched.** It adds no work-management surface and no second
  triage authority, and it copies no other tool's format.

## Use Cases / User Needs

Actors, per `project_vision.md` §Actors: the solo developer and the team lead (code
lens), and the practitioner in a non-code domain (kb, marketing). **NEW** concepts
introduced by this change: *real indecision* and *delegated decision*. The *ground
line* EXISTS in the code lens, as the "I take X from Y" shape its discipline uses for
assumptions and derived answers. There it is extended to weighed choices and the
rejected option. It is NEW in kb and marketing. Everything else EXISTS under the same name in the lenses.

- **UC1 — real indecision on intent.** Solo developer; Goal 3. The request supports
  two readings that change scope, and weighing their pros and cons settles neither. The
  agent asks before writing either one, in one numbered set with the other open
  doubts, and then writes the answer citing the reply.
- **UC2 — a reading that clearly wins.** Solo developer; Goal 4. One reading is
  settled by the request, an APPROVED Vision or an earlier reply, or its pros clearly
  outweigh its cons against the other readings, and the weighing turns on no owner
  priority that is not on record. The agent takes it without asking and writes the
  source, or the weighing and the rejected reading, next to it.
- **UC3 — a fact, or information only the owner holds.** Solo developer; Goal 4. The
  search settles it: the agent cites the evidence, no question. The search leaves it
  open and it changes the work: the agent asks, naming the search and its result. A
  fact is never settled by weighing pros and cons.
- **UC4 — design.** Solo developer; Goal 4. The agent decides under the project's
  conventions and records the rationale. A choice that trades off something the owner
  holds, with no clear preference, becomes UC1.
- **UC5 — nobody to ask.** Practitioner or solo developer; Goal 2. In an unattended
  run, a real doubt becomes a declared assumption (source plus excluded alternative).
  At the top level the work stops blocked: at L3, `BLOCKED on the user` in code and
  kb; at E3 in marketing, the artifact stays DRAFT and the plan holds at the next user
  gate. Below the top level the work proceeds and the assumption is listed in the
  reply. When the owner
  said "you decide" for a choice, it becomes a delegated decision, quoted. A
  dispatched subagent is told, at spawn, to return its real doubts in its final output
  rather than decide them. The orchestrator asks them as its own, or settles a fact
  with evidence. A reserved approval is never assumed: unattended, the work holds
  blocked at any level.
- **UC6 — reading the artifact.** Team lead; Team-lead Actor. Every intent choice in
  a top-level analysis or design shows its source, or its ground and the reading it
  rejected. The design review flags a choice that shows neither, and a ground that
  does not meet the standard.
- **UC7 — the confirmation impulse.** Solo developer; Goal 4. "Shall I proceed?" and
  preference-fishing stay illegal.

## Functional Spec

**Behavior.**

1. **Candidate doubt.** An open point whose answer changes what gets built or
   written. Named thought-signals ("they probably mean", "the request doesn't say",
   "either would work", "I'll note it as an assumption", "it's reversible") help
   notice candidates. They illustrate the definition; they do not close it.
2. **Real indecision.** Classify the candidate first, then test it.
   - **Intent** (benefit, scope, priorities, non-goals, acceptance, reserved
     approvals).
   - **Fact** about the system: search first.
   - **Design**: yours by convention, unless it trades off something the owner holds.

   The test depends on the kind.
   - **A fact, or information only the owner holds** (a deadline, a price, a business
     constraint): settled only by evidence, cited. If the search leaves it open and it
     changes the work, it is a real doubt. It is never settled by a weighing.
   - **A choice** (a reading of intent, a design trade-off): first look for an
     owner-authored statement that settles it (the request, an APPROVED Vision, an
     earlier reply) and cite it. Otherwise, weigh the pros and cons of each option.
   - One option's pros clearly outweigh its cons against the others: take it and write
     "I take X over Z: pro …, contro …", naming the option rejected.
   - The weighing is balanced, or it turns on a priority of the owner that is not on
     record: it is a real doubt, because only the owner can weigh their own
     priorities.

   "The more natural reading", with no pros and cons written, is not a weighing.

   **Reserved approvals and doctrine-mandated stops are outside this test.** They are
   always asked, legal by mandate, whatever the agent thinks the answer is:
   - Vision promotion and amendment;
   - scope changes;
   - proposal acceptance;
   - merge decisions;
   - the stops the doctrine mandates.
3. **Timing.** A real doubt is asked before the first write that would embed its
   answer, grouped with every doubt open at that point. It is never deferred to the
   deliverable, and never dripped one per turn. The planned occasions keep their own
   grouping and form: the L3 spec round (code, kb), the waves (marketing, whose
   four-questions-per-round cap still holds, with overflow in the next round before
   the write), and the Capture Moment sweep (kb). A mandated hand-over keeps its own
   timing as well as its form: kb claim conflicts are escalated once, at the end of a
   run, and never stop an ingest.
4. **Form.** A question outside a planned occasion passes the legality test and
   carries the blocking form: five elements, one line each. The fork element lists
   the options, each with its pros and cons. Wherever a question offers options,
   including the planned occasions, each option carries its pros and cons. The element "why no assumption survives" now states why no option is
   settled by the weighing, and what a wrong pick costs. For a reserved approval or a
   mandated stop, it cites the approval or the mandate instead. The rule that reserved
   approvals and mandated stops are legal by mandate is stated next to the form. Each
   lens's closed exemption list stays as it is: two in code and kb, one in marketing.
5. **Assumptions.** Only for a real doubt that cannot be asked: unattended, or
   delegated by the owner's explicit words for that choice. A general "go ahead" is
   not a delegation. Each assumption states its source and the alternative it
   excludes, and each is listed where the owner will read it. A reserved approval or
   a mandated stop is never assumed: unattended, the work holds blocked at any level,
   unless the mandating rule prescribes its own unattended handling. The gated review
   rung is such a rule: the grant is never assumed, the fallback runs, and the row
   records it. A dispatched subagent returns its open points in its final output;
   the orchestrator treats them as its own candidate doubts.
6. **Review.** In a top-level analysis or design review, each of these is a finding:
   - an intent choice written with no owner-authored source, no ground line, and not
     as an assumption the discipline makes legal;
   - a ground line that names no rejected option, or states no pros and cons;
   - a weighing that turns on an owner priority that is not on record;
   - a fact or owner-held datum settled by a weighing instead of a source;
   - a cited source that does not say what the line claims, where the reviewer can
     read the source.

**Cases.**

- The search settles the fact: no question and no ground line needed beyond a
  citation.
- The options are equivalent in effect: no doubt. Pick one, because asking would be
  preference-fishing.
- A doubt emerges during implementation: same rule. If the answer changes an approved
  contracted surface, it is a scope change the owner approves, as today.
- A kb claim conflict: its own mandated hand-over, in the closed list, unchanged.
- A marketing estimate backed by a benchmark or a comparable: a researched answer with
  its confidence, not a doubt.

**Acceptance criteria.**

- **AC1.** Given two scope-changing readings with no clear preference, when the agent
  reaches the write, then it asks first.
- **AC2.** Given a clearly supported reading, then no question is asked, and the ground
  appears next to the choice.
- **AC3.** Given a fact the repo answers, then no question reaches the owner.
- **AC4.** Given an unattended L3 run with a real doubt, then a declared assumption is
  recorded with its source and excluded alternative, and the work stops blocked in
  that lens's vocabulary.
- **AC5.** Given a top-level artifact with an intent choice lacking any ground, or
  a ground with no pros and cons and no rejected option, then the design review
  reports a finding.
- **AC6.** Given a merge decision with an obvious answer, then the agent still asks.
- **AC7.** Given a question offering options, then each option carries its pros and
  cons.
- **AC8.** Given a fact the search leaves open that changes the work, then the agent
  asks and does not weigh it.

## Interface Contract

**Actors and surfaces.** The surface is the agent's question to the owner in the
conversation. For a software actor it is the blocked state on the artifact.

**Reused idioms.** A numbered set with concrete options (the round and the waves), and
the client's structured-question facility where one exists, which marketing already
names. No new idiom.

**Flow.**

1. The agent works and a candidate doubt appears.
2. It classifies the doubt and tests it for real indecision.
3. An option that clearly wins the weighing is taken, and the weighing is written with it.
4. Before the next write that would embed an open doubt, all the open doubts go out in
   one set.
5. The owner replies.
6. The answers are written into the artifact, citing the reply, and the work resumes.

When unattended, step 4 becomes a declared assumption, plus the blocked state at the top level.

**Feedback.** Each question names what stays blocked. Afterwards the artifact shows,
for every intent choice, its source: a reply, the record, or a stated ground.

**Constraints.** The planned occasions and the closed exemption lists are read, not
redesigned: `debugging.md`'s circuit breaker, `reconciliation.md` §4, and `review.md`'s
round cap.

**Flags.** Two risks feed the threat model: over-asking, and "the weighing favours it" used
as a licence.

## Capability Ledger

| Capability | Verdict | Where / gap | Evidence |
|---|---|---|---|
| Rule a question legal | EXISTS | `elicitation.md` §The question discipline ×3 (legality test) | re-read 2026-09-25; unchanged |
| Tell a real doubt from a clear choice | MISSING | added in `elicitation.md` ×3: candidate signals, three kinds, the pros-and-cons test | searched the three `elicitation.md`, the three `SKILL.md`, `review.md` and `debugging.md` for "doubt", "unknown" and "assum": the only trigger is an unknown the agent already recognizes |
| Decide when to ask | INADEQUATE | "Default non-blocking" defers doubts to the deliverable; code Rule Zero calls blocking the exception | replaced by "before the write that would embed it, grouped" |
| Settle intent from the record | INADEQUATE (code) | the skip path and "derive before asking" allow repo-derived goal and scope | narrowed to an owner-authored source or a stated ground |
| Record an assumption with its source | EXISTS, reach narrowed | the Unattended path (code, kb) plus the evidence duty | kept for unattended cases; delegation added; marketing has no unattended path, so it gains one |
| Catch a groundless choice in a written artifact | MISSING | `review.md` §Reviewing covers conformance, grounding and restated facts, and nothing covers an unsourced intent choice | new bullet (shared ×3) |
| Assert the wiring | EXISTS | `test_question_discipline_wired` with `@requires("question_discipline")`, claimed by all three entry points | anchors updated |
| Observe behaviour | EXISTS | `evals/scenarios/`, non-gating (code lens) | new scenario |

## Impact

| Path | Change | Serves |
|---|---|---|
| `skills/agentic-sdlc-skill/elicitation.md` | MODIFY: the discipline gains §When a doubt emerges (signals, kinds, pros-and-cons test), §Ask before the write (timing, assumptions only unattended or delegated, subagent doubts) and §The form of a question (the blocking form, scoped outside the planned occasions); the skip path and "derive before asking" are narrowed; "Default non-blocking" and "Blocking is reserved" are removed; one anti-pattern is added | UC1–UC5, UC7; FS 1–5 |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/elicitation.md` | MODIFY: same in kb vocabulary; the Capture Moment sweep is named a planned occasion; claim conflicts cite `reconciliation.md` §4 without restating it | UC1–UC5 |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/elicitation.md` | MODIFY: same in marketing vocabulary; adds an unattended path (artifact stays DRAFT, plan held at the next user gate, ledger ASSUMPTION rows listed there); the waves and their four-per-round cap stay the planned occasion; a researched ASSUMPTION is not a doubt | UC1–UC5 |
| The planned occasions: code and kb round (`elicitation.md` §The round, "offer concrete options"); marketing question style ("Offer concrete options") | MODIFY: each option offered carries its pros and cons. The kb Capture Moment sweep offers no options (an open "any other decisions?") and is untouched | AC7 |
| `dispatch.md` ×3 (shared) | MODIFY: the spawn sentence becomes "the brief plus the return-doubts line"; the line is self-contained for a subagent that never reads `elicitation.md` ("an open point whose answer changes the work: return it in your final output with what you searched; do not decide it") | UC5, F4 residual closed |
| `SKILL.md` ×3 | MODIFY: the always-read line carries "a real doubt is asked when it emerges, before it is written"; code drops "Blocking the work is the exception" | FS 3 at every level |
| `review.md` ×3 (shared) | MODIFY: new §Reviewing bullet "An unasked doubt is a finding", citing the discipline for what a legal ground or assumption is; the gated-rung citation repointed from `§Blocking is reserved` to `§The form of a question`, the section that states both the form and the legal-by-mandate rule | UC6, FS 6 |
| `scripts/test_skill_invariants.py` ×3 (shared) | MODIFY: new anchors; "Default non-blocking" asserted absent; the always-read line must carry the duty; the heading `review.md` cites must exist | wiring |
| `scripts/shared_manifest.json` ×3 | REGENERATE (`review.md`, `dispatch.md` and `test_skill_invariants.py` are shared) | drift guard |
| `skills/agentic-sdlc-skill/evals/scenarios/doubt_asked_when_it_emerges.md` | ADD | AC1–AC3 (behaviour) |
| `README.md`, `distributions/kb-agentic-skill/README.md` | MODIFY: the feature line ("proceeds on a declared assumption" is no longer true) | truthful packaging |
| `distributions/mkt-agentic-sdlc/README.md` | MODIFY: line 105 claims the question discipline is byte-identical across the three lenses, which is false before and after; reworded as the same rule, restated per lens | same |
| `ai_docs/strategic/skill_family_agent_workflows.md` | MODIFY: point 4 ("Default non-bloccante") | same |
| `CHANGELOG.md` ×3 | MODIFY: `[Unreleased]` entry (1.35.0 is released) | release notes |
| `ai_docs/solutions/harness_question_discipline/probe.py` | ADD | text replay |

**Blast radius.** Every consumer of the changed text, enumerated by grep over the three
skill directories, the READMEs and `ai_docs/strategic/`. These are doctrine files, so
there is no symbol graph.

- `review.md:58-59` ×3 cites "§Blocking is reserved" and "that file's five-bullet
  blocking form". Repointed; the form keeps its five bullets and its name.
- `review.md:63` ×3 uses "why no assumption survives". The element is kept, redefined
  compatibly: "either guess writes a false log row" is exactly a wrong-pick cost.
- `review.md:70` ×3 cites the "Unattended path". Unchanged in code and kb. In marketing
  it dangles today, and the new marketing unattended path makes it resolve.
- `gated_rung_asks_before_descending.md`, both copies (code and kb), cites "the five
  elements of the blocking form". They are kept.
- kb `SKILL.md:246-250` (the sweep "is not a blocking question … the blocking form does
  not attach") and kb `evals/scenarios/capture_channels_the_days_decisions.md:39` ("not
  the five-part blocking form"). Both stay true: the sweep is a planned occasion with its
  own form, now named as such.
- `SKILL.md` ×3: the bullets in the Impact. Code line 163 and kb line 134 point to the
  round (unchanged). Marketing lines 16 and 139 point to the waves (unchanged).
- `vision.md:50` ×3 points to the round for the benefit (unchanged).
- `debugging.md`'s circuit breaker and `guides.md`'s proposal: covered by the closed list
  and "every other mandated stop carries the form" (unchanged).
- Marketing `evals/scenarios/no_number_without_ledger.md` expects a benchmark or a
  declared ASSUMPTION. Still true: a researched ASSUMPTION is not a doubt.
- `dispatch.md` ×3 "Spawn the subagent with that brief as its entire context window":
  the new line extends the spawn, and the brief format (`plan brief`) is unchanged.
- The READMEs, `skill_family_agent_workflows.md` and the CHANGELOGs are in the Impact.

If one is missed, a citation dangles; the gated rung would cite a heading that no longer
exists. The probe and the wiring test assert that the cited heading exists in all three
lenses.

## Security and Threat Model

There is no code, parsing, network or filesystem surface, only doctrine text. The risks
are process risks.

| Risk | Mitigation |
|---|---|
| Over-asking returns (the 2026-08-01 defect) | The legality test and the never-legal list are unchanged. An option that clearly wins the weighing is taken, not asked. Every question carries the pros and cons of each option, so the owner can answer quickly. Equivalent options are the agent's to pick. There is one set per write point, never a drip. Planned occasions keep their lighter forms. |
| "The weighing favours it" becomes the new licence for silence | The weighing is written with the choice: pros and cons, and the option rejected. A weighing that turns on an owner priority not on record is a real doubt. The review clause flags a choice written without it. |
| Signal gaming: "no signal fired, so no doubt" | The signals illustrate the definition; the definition in FS 1–2 governs. The review clause is independent of whether the author noticed. |
| "Design choice" used as a label to avoid asking | A trade-off against something the owner holds, with no clear preference, is intent. |
| Delegation stretched from a general "go ahead" | Delegation is only the owner's explicit words for that choice, quoted. |
| A subagent folds its doubts silently | The spawn itself carries the return-doubts instruction (`dispatch.md`), because the brief is its entire context; the orchestrator asks them. |
| A guessed fact wearing a weighing | Facts and owner-held data are never weighed (FS 2); the review flags one that was (FS 6). |
| An unattended run assumes an approval | Reserved approvals and mandated stops are never assumed; the work holds blocked at any level. |
| kb ingests interrupted | `reconciliation.md` §4 stays in kb's closed list with its timing (FS 3), cited and not restated. |
| The review clause becomes a second copy of the owner list | The bullet cites each lens's discipline and restates nothing. |
| A reserved approval taken because "the weighing favours it" | Reserved approvals and mandated stops are outside the weighing test, legal by mandate, stated in the section `review.md` cites. |
| **Backstop limits, stated honestly** | The review clause runs at the top level only (L3, or E3 in marketing). It can check a ground against the standard and against any source it can read, but not that a quoted reply exists in the conversation, since the reviewer is given no transcript. L1 and L2 documents rely on the author-side rule alone. Whether devPNT's Hybrid reviewer definitions read `review.md` §Reviewing is outside this skill's reach, and is flagged to devPNT. |

## Action Plan

1. Probe written and shown RED on `c2a3828`.
2. Design review: rounds 1–3 FAIL, round 4 (owner-authorized) PASS.
3. Edit `elicitation.md` ×3 (including the options at the round and the waves) and
   `SKILL.md` ×3.
4. Edit `review.md` and `dispatch.md` in code and copy them byte-for-byte to kb and
   marketing; do the same for `test_skill_invariants.py`; regenerate the three
   manifests.
5. Add the scenario; update the READMEs, `skill_family_agent_workflows.md` and the
   three CHANGELOGs.
6. Probe GREEN; the three batteries; `sdlc_check.py check` and `index`; closure review
   on the diff; REVIEW_LOG rows; re-measure the budget; flip to COMPLETED.
7. The closure report tells the owner, who also maintains devPNT, that devPNT's
   generated reviewer definitions must carry the new §Reviewing clause. The report is
   the record of that flag; the devPNT-side change is out of this unit's scope.

## Test Strategy

- **Wiring (deterministic, gating).** `test_question_discipline_wired` in all three
  distributions: new anchors, "Default non-blocking" absent, the duty on the
  always-read line, and the `review.md`-cited heading present. Also the drift guard
  and the full batteries. Covers the text side of FS 1–6.
- **Doctrine replay (deterministic).** `harness_question_discipline/probe.py`: RED on
  `c2a3828`, GREEN on the working tree. It covers:
  - the silence licence gone;
  - signals, the pros-and-cons test with its rejected option, pros and cons in the
    form, the duty, write-point timing
    and the restricted assumptions present;
  - the code skip path and "derive before asking" narrowed;
  - "legal by mandate" present in the section `review.md` cites;
  - facts never weighed; reserved approvals never assumed; kb's mandated timing kept;
    marketing's DRAFT hold; the subagent return line in `dispatch.md`; pros and cons
    at the planned occasions;
  - marketing's unattended path;
  - the review clause;
  - the cited heading resolving in all three lenses;
  - the per-lens exemptions cited.
- **Behaviour (non-gating, owner-run).** `doubt_asked_when_it_emerges.md` covers AC1
  (asked before the write), AC2 (a clear reading taken with its ground) and AC3 (no
  question on a repo fact). AC4–AC8 are covered by the text layer: the unattended
  wording, the review clause, the legal-by-mandate rule, pros and cons in the form and
  at the planned occasions, and the facts rule. No validator sees a conversation, and a
  scenario for an unattended run or a design review is a follow-up, not claimed here.

## Diary

- **2026-08-01 — first increment (legality test), COMPLETED.** Built from the "useless
  questions" report. It added the legality test, the never-legal list, the owner-owned
  precedence, "Default non-blocking" with its evidence duty, the blocking form with its
  closed exemption list, and the capability-gated wiring test. Two design-review rounds
  found 5 BLOCK and 10 WARN, all fixed; the history is in REVIEW_LOG.md.
- **2026-09-25 — reopened: ask on real indecision.**
  - Opened from the "doubts stay silent" report. The round was answered by the owner.
  - The probe was written first. Two probe defects were fixed before it counted as red:
    it sliced the file's opening line instead of the section, and it compared phrases
    that wrap across lines. Both would have given false greens. With them fixed, the
    probe was RED on `c2a3828`. It grew with each review round; its final form is
    4/63 green there, where the four greens are preservation checks.
  - Design review round 1: FAIL, 3 BLOCK and 10 WARN, all real.
    - B1: judgement or repo-derived intent still settled doubts silently.
    - B2: marketing has no unattended path.
    - B3: a form on every question collided with the kb sweep and the waves.
  - A second round with the owner on two questions this raised produced the
    real-indecision test and the explicit cost acceptance. Everything is folded into
    this version.
  - Design review round 2: FAIL, 2 BLOCK and 6 WARN.
    - N1: a ground line could hide the fork (no rejected reading), and the review
      checked only presence.
    - N2: reserved approvals fell under the ground test.
    Both are folded in: the rejected reading and the standards check, and
    legal-by-mandate stated outside the test. Also fixed: marketing E-levels, L1
    cost, the quoted acceptance, the probe anchors, and the devPNT flag.
  - Owner's third input, received during round 3: pros and cons of each answer in
    every question, and no question when the agent's own weighing clearly favours one
    option. Round 3 was stopped unread, because it was reviewing a superseded test.
    The weighing replaces the one-line-ground test, and round 3 re-runs on this
    version.
  - Design review round 3 (a new reviewer): FAIL, 1 BLOCK and 10 WARN.
    - F1: the weighing could settle facts and owner-held data.
    The cap was reached and the findings went to the owner, who chose to fix them and
    authorized a fourth round (a logged deviation from the cap). The owner also chose
    the `dispatch.md` return-doubts line over a declared residual. All eleven findings
    are folded in.
  - Design review round 4 (scoped, the same reviewer): **PASS**, with 4 WARN and 2
    minor residuals. Folded in: the gated rung's own unattended handling, a
    self-contained `dispatch.md` line, the Objective's definition, the Action Plan,
    and the third unitemized cost.
- **2026-09-25 — implemented and closed.** Doctrine edited in the three lenses, with
  the shared `review.md`, `dispatch.md` and wiring test copied byte-for-byte and the
  manifests regenerated.
  - Two probe false reds (scope errors in P9 and P6) were fixed in the probe, not the
    doctrine.
  - Closure review: PASS with 9 WARN. W2–W9 were fixed afterwards: marketing's two
    meanings of ASSUMPTION, subagent doubts treated as candidate doubts, the
    §4 paraphrase, wider wiring anchors, a tighter probe, the scenario, and the Diary
    figure.
  - W1, the budget overrun, was accepted by the owner.
  - Final state: probe 63/63 green on the tree and 4/63 on `c2a3828` (preservation
    checks); batteries 221, 407 and 239 OK.
  - Integration, the owner's choice: commit on the branch now, and open the PR after
    1.35.0 reaches main.
