# Spec Elicitation

`## The question discipline` below governs EVERY question to the user — any
phase, any level, inside or outside the round. The rest of the file is the spec
elicitation round: it applies when an L3 request enters phase 3 (Request
Analysis), BEFORE drafting the ANALYSIS document (Standalone) or the D-UC/E-ISP
(Hybrid).

Skip path: if the spec is already complete — an approved Vision or explicit user
requirements already answer goal, scope, and constraints, or the remainder is
derivable from the repo, `ai_docs/` and the conversation — skip the round and add
a one-line note in the analysis stating why it was skipped and naming the
sources. Do not run the round as a formality when the answers are already on
record.

Unattended path: when the user is not reachable (a scheduled or autonomous run)
and the skip path does not answer all six, do not stall and do not invent
consensus. Write the missing answers as **declared assumptions** in
`## Objective`, mark the ANALYSIS `BLOCKED on the user`, and stop before
implementation. An assumption on the record is reviewable; a guess folded
silently into a design is not.

## The question discipline

A question to the user spends their attention and stalls the work; the round
below is the only place the process *plans* that cost. Everywhere, a question is
legal only when BOTH hold:

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
  project's conventions. Cheapness to undo is NOT the test: nearly everything is
  reversible under version control, and "it is reversible" as a licence to stop
  asking is the silence-side evasion this clause must not fund.
- **Re-asking the record** — goal, scope or constraints that an APPROVED Vision,
  an earlier reply, or the request itself already states.

What questions are FOR — what the user uniquely owns: the benefit, priorities
between conflicting goods, non-goals, acceptance, and the approvals doctrine
reserves to them (Vision promotion and amendment, scope changes, proposal
acceptance, merge decisions). Facts about intent come from the user; facts about
the system come from search. (The marketing sibling states the same rule as "ask
only what the user uniquely owns"; this is its code-domain form.)

**Precedence, because both halves can fire at once:** this paragraph wins over
the "never legal" list above it. A choice the user uniquely owns is never
preference-fishing, however cheap it is to undo; the list reaches choices that
are *not* theirs.

**Default non-blocking.** An unknown on which no fork of the work depends: write
it as a **declared assumption** in the artifact it touches — the same mechanism
the unattended path uses — proceed, and present the open points **batched**, with
the round for spec questions or with the deliverable otherwise, answered by
exception.

This is the path most work takes, so it carries the SAME evidence duty as a
question, not a lighter one — otherwise "assume it" becomes the way to skip the
standard. Each declared assumption states **what it is taken from** ("I take X
from Y" — the same shape the round uses) and **the alternative it excludes**, and
**every declared assumption reaches the batch**: an assumption nobody is shown is
not an open point, it is a silent decision. That pairing is what the kb family's
escalation rule actually does — keep BOTH sides with their sources and surface
them, never silently pick one — and this branch, not the blocking one, is where
it structurally belongs. An assumption recorded with its source and its rejected
alternative is reviewable; one recorded alone is a decision wearing an
assumption's clothes, and a session stalled on a question that could have been
an assumption is the waste this section exists to prevent.

**Blocking is reserved** for three cases: proceeding under ANY assumption would
waste the work (the forks diverge at once, and the wrong branch is rework of the
whole unit); the doctrine reserves the decision to the user (the approvals
above); or the doctrine itself mandates the stop — and a mandated stop is legal
by mandate, never re-argued here.

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

A blocking question carries a mandatory form — surface both sides with their
evidence, never silently pick one:

- the fork: the concrete options and what each implies for the work;
- the evidence: what you searched, read or tried, and what it leaves undecided;
- why no assumption survives — what work is discarded if you assume and are
  wrong. This is what makes case (a) falsifiable: without it, "this is a fork"
  is an agent's assertion about its own convenience, and case (a) becomes the
  licence for exactly the question this section forbids. Cases (b) and (c) answer
  it by citing the approval or the mandate instead;
- why it is the user's call — what makes the remainder intent, priority or
  approval rather than a derivable fact;
- what stays blocked until answered.

## The round

**Derive before asking.** Answer each of the six from the record first — the
Vision, `ai_docs/`, the conversation, the code. Ask only the residue, and carry
the derived answers into the round as declared assumptions corrected by
exception ("I take X from Y; the questions below are what no source answers"),
not re-confirmed one by one.

Ask ONE structured set of questions, not a drip of follow-ups. Keep each
question short and numbered; offer concrete options where a real choice
exists (this narrows the reply and speeds up the round). Cover:

1. **Goal / benefit** — what problem this closes and why now. The answer must
   name what the actor *obtains*, not a mechanism: "a dashboard" is not an
   answer to "never lose the thread" — ask again until it is a benefit
   (`vision.md`: the Vision is the distilled benefit; solutions and preferences
   are what gets filtered out).
2. **Actors** — who interacts with this: their role, primary goal, and what
   "good UX" means to them. These become the Vision's `## Actors`; each
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
- **Collecting answers without folding them in**: getting replies in chat
  and proceeding to design without writing them into the analysis document —
  the next reader has no record of why the scope is what it is.

(The illegal question forms — generic confirmation, preference-fishing,
re-asking the record — are defined once, in `## The question discipline`.)
