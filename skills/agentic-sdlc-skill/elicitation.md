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

1. **Searched first, and the search is named.** The answer is not on record and
   not derivable from the repo, `ai_docs/`, the Vision or the conversation — and
   the question says what you read or searched before asking. Same standard as a
   router verdict or an architect-pass MISSING: a search not named is
   indistinguishable from a search not run. A question the repo can answer is a
   search outsourced to the user.
2. **It names what is blocked.** The question states the specific decision or
   fact that cannot be resolved without the reply — what you will do differently
   depending on the answer. If nothing downstream changes with the answer, there
   is no question.

Never legal:

- **Generic confirmation** — "shall I proceed?", "is this OK?". The process
  authorizes proceeding; if a real risk motivates the ask, name the risk and the
  fork — that is a blocking question and carries the form below.
- **Preference-fishing** — asking the user to pick among options that are
  equivalent, reversible, or already decided by the project's conventions.
- **Re-asking the record** — goal, scope or constraints that an APPROVED Vision,
  an earlier reply, or the request itself already states.

What questions are FOR — what the user uniquely owns: the benefit, priorities
between conflicting goods, non-goals, acceptance, and the approvals doctrine
reserves to them (Vision promotion and amendment, scope changes, proposal
acceptance, merge decisions). Facts about intent come from the user; facts about
the system come from search. (The marketing sibling states the same rule as "ask
only what the user uniquely owns"; this is its code-domain form.)

**Default non-blocking.** An unknown on which no fork of the work depends: write
it as a **declared assumption** in the artifact it touches — the same mechanism
the unattended path uses — proceed, and present the open points **batched**, with
the round for spec questions or with the deliverable otherwise, answered by
exception. An assumption on the record is reviewable; a session stalled on a
question that could have been an assumption is the waste this section exists to
prevent.

**Blocking is reserved** for three cases: proceeding under ANY assumption would
waste the work (the forks diverge at once, and the wrong branch is rework of the
whole unit); the doctrine reserves the decision to the user (the approvals
above); or the doctrine itself mandates the stop — and a mandated stop is legal
by mandate, never re-argued here. Where the mandating file already prescribes
what to hand over, hand over THAT and do not restate this form on top of it:
`debugging.md`'s circuit breaker prescribes the minimal reproduction, what was
ruled out and the current best hypothesis; `review.md`'s round cap prescribes the
artifact plus the open findings. Two forms over one moment is the duplicate
`review.md` §Reviewing already forbids — and a stuck agent has no "fork" to name,
which is exactly why its own file, not this one, owns that hand-over.

Otherwise a blocking question carries a mandatory form — the kb family's
escalation rule, generalized: surface both sides with their evidence, never
silently pick one:

- the fork: the concrete options and what each implies for the work;
- the evidence: what you searched, read or tried, and what it leaves undecided;
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
