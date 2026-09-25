# Spec Elicitation

`## The question discipline` below governs EVERY doubt and EVERY question to the
user — any phase, any level, inside or outside the round. The rest of the file is
the spec elicitation round: it applies when an L3 request enters phase 3 (Request
Analysis), BEFORE drafting the ANALYSIS document (Standalone) or the D-UC/E-ISP
(Hybrid).

Skip path: if the spec is already complete — an approved Vision, explicit user
requirements or an earlier reply already answer goal, scope, and constraints, and
any remainder is settled as §When a doubt emerges allows — skip the round and add
a one-line note in the analysis stating why it was skipped and naming the
sources. Do not run the round as a formality when the answers are already on
record.

Unattended path: when the user is not reachable (a scheduled or autonomous run)
and a real doubt remains, do not stall and do not invent consensus. Write it as a
**declared assumption** (§Ask before the write) in the artifact it touches. At L3,
mark the ANALYSIS `BLOCKED on the user` and stop before implementation; below L3,
proceed and list the assumption in the reply. An assumption on the record is
reviewable; a guess folded silently into a design is not.

## The question discipline

A doubt kept silent is decided by the agent alone and reaches the documents
looking settled; a useless question wastes the user's attention. This section
rules on both.

### When a doubt emerges

A **candidate doubt** is an open point whose answer changes what you build or
write. The usual signals — they illustrate, they do not close the definition:

| Thought | What it means |
|---|---|
| "They probably mean…", "I'll assume…" | you are choosing between readings of the request |
| "The request doesn't say, so I'll fill it in" | a gap in scope, a non-goal, an acceptance criterion or a priority |
| "Either would work, I'll pick one" | equivalent in effect: yours, pick and do not ask; different in effect: weigh them below |
| "I'll note it as an assumption and move on" | with the user reachable, that note is where doubts go to be forgotten |
| "It's reversible, it can be fixed later" | later is after the documents built on it exist |

Settle it by kind:

- **A fact, or information only the user holds** (a deadline, a price, a
  constraint): settled only by evidence, cited — never settled by a weighing. Left
  open by the search and changing the work, it is a real doubt.
- **A choice** — a reading of intent, a design trade-off: cite the user's statement
  that settles it (the request, an APPROVED Vision, an earlier reply); failing one,
  weigh the pros and cons of each option, stating each rejected option
  at its strongest — the need it serves best; a weighing won against a weak version of the
  alternative is not a weighing. One clearly outweighs: take it and write the
  weighing with the choice — "I take X over Z: pro …, contro …". Balanced, or
  turning on a user priority not on record: a **real doubt** — and it does whenever
  the options serve different needs of the actor, each better at one the actor would
  notice in using the result (reading in a spreadsheet against processing by a
  program, a quick answer against a complete one) and none good enough at both, and
  nothing the user wrote ranks those needs — however clear your own ranking feels.
  "The more natural reading" with no pros and cons written is not a weighing. Design is yours until it
  trades off something the user owns. Reserved approvals never enter this test
  (§The form of a question).

### Ask before the write

A real doubt that passes the legality test below is **owed**, not merely allowed:
the test separates a doubt from a search not yet run, it never licenses silence.
Ask it before the first write that would embed its answer — in an analysis, plan,
guide or code — grouped with every doubt open at that point, in one numbered set,
with the client's structured-question facility where it has one. Never defer a
doubt to the deliverable, where the user must find it inside the document; never
drip one question per turn. The round below is this rule's planned occasion. Fold
every answer into the artifact, citing the reply (§Reflect); an intent choice with
neither a source nor a weighing is a finding (`review.md` §Reviewing).

**Declared assumptions exist only where no question can be asked:**

- **Unattended** — the user is not reachable (the Unattended path above).
- **Delegated** — the user's own words handed you this choice ("your call"); quote
  them. A general "go ahead" is not a delegation.

Each states **what it is taken from** and **the alternative it excludes**, and is
listed where the user will read it: an assumption recorded alone is a decision
wearing an assumption's clothes, and one nobody is shown is a silent decision. A
dispatched subagent returns its open points in its final output (`dispatch.md`);
the orchestrator treats them as its own candidate doubts (§When a doubt emerges).

### The legality test

Everywhere, a question is legal only when BOTH hold:

1. **Searched first, and the search is named — with its result.** The answer is
   not on record and not derivable from the repo, `ai_docs/`, the Vision or the
   conversation — and the question states the terms, tools and areas you searched
   **and what they returned**. Same standard as a router verdict or an
   architect-pass MISSING, and it carries their floors, not only their vocabulary
   (`architect.md`, `guides.md`): a search whose scope does not cover the question
   is not a search; a hit you did not open does not narrow anything; and **never
   fake the search** — "I looked and found nothing" that names no terms and no
   areas is a search not run. A question the repo can answer is a search
   outsourced to the user.
2. **It names what is blocked.** The question states the specific decision or
   fact that cannot be resolved without the reply — what you will do differently
   depending on the answer. If nothing downstream changes with the answer, there
   is no question.

Never legal:

- **Generic confirmation** — "shall I proceed?", "is this OK?". The process
  authorizes proceeding; if a real risk motivates the ask, name the risk and the
  fork — that is a blocking question and carries the form below.
- **Preference-fishing** — asking the user to pick among options that are
  equivalent **in their effect on the benefit** and already decided by the
  project's conventions. Cheapness to undo is NOT the test.
- **Re-asking the record** — goal, scope or constraints that an APPROVED Vision,
  an earlier reply, or the request itself already states.

What questions are FOR — what the user uniquely owns: the benefit, priorities
between conflicting goods, non-goals, acceptance, and the approvals doctrine
reserves to them (Vision promotion and amendment, scope changes, proposal
acceptance, merge decisions). Facts about intent come from the user; facts about
the system come from search.

**Precedence, because both halves can fire at once:** this paragraph wins over
the "never legal" list above it. A choice the user uniquely owns is never
preference-fishing, however cheap it is to undo; the list reaches choices that
are *not* theirs.

### The form of a question

The approvals reserved above and every stop the doctrine mandates are asked
whatever you expect the answer: **legal by mandate**, never weighed, never
re-argued here. Unattended, they are never assumed: the work holds, unless the
mandating rule prescribes its own unattended handling (`review.md`'s gated rung
does).

**Exactly two mandating files prescribe their own hand-over, and there the form
below does not apply** (two forms over one moment is the duplicate `review.md`
§Reviewing forbids): `debugging.md`'s circuit breaker — the minimal reproduction,
what was ruled out, the current best hypothesis; and `review.md`'s round cap —
the artifact plus the open findings. That list is closed. **Every other mandated
stop carries the form**, including one that names only its options and not its
evidence (`SKILL.md`'s Vision-Gate conflict names the two choices — the evidence
is still owed, and for a Vision conflict the quoted line IS the substance) and
one that prescribes nothing (`guides.md`'s guide proposal and its ingestion
bound). "The file mentions the moment" is not a prescription; only a stated
hand-over is.

A question outside the planned occasions carries the **blocking form**, one line
per element — surface both sides with their evidence, never silently pick one:

- the fork: the options, each with its pros and cons, and what each implies for
  the work;
- the evidence: what you searched, read or tried, and what it leaves undecided;
- why no assumption survives — why the weighing does not settle it, and what a
  wrong pick costs; a reserved approval or a mandated stop cites the approval or
  the mandate instead;
- why it is the user's call — what makes the remainder intent, priority or
  approval rather than a derivable fact;
- what stays blocked until answered.

## The round

**Derive before asking.** Answer each of the six from the record first — the
Vision, `ai_docs/`, the conversation; the code answers facts and constraints,
never the goal, scope or acceptance. Ask only the real doubts, and carry the
derived answers into the round with their source or weighing ("I take X from Y;
the questions below are what no source settles"), not re-confirmed one by one.

Ask ONE structured set of questions, not a drip of follow-ups. Keep each
question short and numbered; offer concrete options where a real choice
exists, each with its pros and cons (this narrows the reply and speeds up the
round). Cover:

1. **Goal / benefit** — what problem this closes and why now. The answer must
   name what the actor *obtains*, not a mechanism: "a dashboard" is not an
   answer to "never lose the thread" — ask again until it is a benefit
   (`vision.md`: the Vision is the distilled benefit; solutions and preferences
   are what gets filtered out).
2. **Actors** — who interacts with this: their role, primary goal, what
   "good UX" means to them, and the surfaces they use today for this job
   (the screens, commands or endpoints they operate — the Interface
   Contract's as-is starts here; skip the surface half when no actor-facing
   surface is in scope) and, at responsibility level, what happens when they
   act (which components respond) — the Interface Contract's flow starts here. These become the Vision's `## Actors`; each
   use-case below attaches to one (actor = who they are, use-case = what
   they do). Skip only when an approved Vision already names them.
3. **Scope boundaries** — what is explicitly included in this unit of work.
4. **Non-goals** — what is explicitly excluded, so scope does not silently
   creep in later.
5. **Constraints** — technical, compatibility, and security constraints that
   bound the solution space.
6. **Acceptance signals** — how you and the user will both recognize the
   work is done and correct.

## Reflect

Fold the answers into the ANALYSIS `## Objective` / `## Vision-Alignment`
sections (Standalone) or into the D-UC/E-ISP (Hybrid) — do not leave them
sitting only in the chat transcript. The written document, not the
conversation, is what the next session and the next reviewer will read.

Run a second round only when an answer opens a real fork in the design (a
genuinely new question the first round could not have anticipated). Do not
run a second round to double-check answers that were already clear.

## Anti-patterns

- **Interrogation**: an endless list of questions, or drip-feeding one
  question at a time across many turns instead of one structured round.
- **Deferring a doubt into the document**: writing a guess into the artifact
  and leaving the user to find it there.
- **Collecting answers without folding them in**: getting replies in chat
  and proceeding to design without writing them into the analysis document —
  the next reader has no record of why the scope is what it is.

(The illegal question forms — generic confirmation, preference-fishing,
re-asking the record — are defined once, in `## The question discipline`.)
