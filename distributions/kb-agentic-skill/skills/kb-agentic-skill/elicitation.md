# Spec Elicitation

`## The question discipline` below governs EVERY question to the practitioner —
any phase, any level, inside or outside the round. The rest of the file is the
spec elicitation round: it applies when an L3 request enters phase 3 (Request
Analysis), BEFORE drafting the ANALYSIS document (Standalone) or the D-UC/E-ISP
(Hybrid).

Skip path: if the spec is already complete — an approved Vision or explicit
user requirements already answer goal, scope, and constraints — skip the
round and add a one-line note in the analysis stating why it was skipped.
Do not run the round as a formality when the answers are already on record.

Unattended path: when the user is not reachable (a scheduled or autonomous run,
and a bootstrap Vision is `DRAFT` by mandate, so the skip path above cannot
apply on a project's first L3), do not stall and do not invent consensus. Write
the six answers as **declared assumptions** in `## Objective`, mark the ANALYSIS
`BLOCKED on the user`, and stop before implementation. An assumption on the
record is reviewable; a guess folded silently into a design is not.

## The question discipline

A question to the practitioner spends their attention and stalls the work; the
round below is the only place the process *plans* that cost. Everywhere, a
question is legal only when BOTH hold:

1. **Searched first, and the search is named — with its result.** The answer is
   not on record and not derivable from the corpus, the topic graph, `ai_docs/`,
   the Vision or the conversation — and the question states the terms, tools and
   areas you searched **and what they returned**. Same standard as a router
   verdict or a taxonomy-pass MISSING, and it carries their floors: a search
   whose scope does not cover the question is not a search; a hit you did not
   open narrows nothing; and **never fake the search** — "I looked and found
   nothing" that names no terms and no areas is a search not run. A question the
   corpus can answer is a search outsourced to the practitioner.
2. **It names what is blocked.** The question states the specific decision or
   fact that cannot be resolved without the reply — what you will do differently
   depending on the answer. If nothing downstream changes, there is no question.

Never legal:

- **Generic confirmation** — "shall I proceed?", "is this OK?". The process
  authorizes proceeding; if a real risk motivates the ask, name the risk and the
  fork — that is a blocking question and carries the form below.
- **Preference-fishing** — asking the practitioner to pick among options that
  are equivalent in their effect on the benefit and already decided by the
  project's conventions. Cheapness to undo is NOT the test.
- **Re-asking the record** — goal, scope or constraints that an APPROVED
  Vision, an earlier reply, or the request itself already states; or a fact a
  claim row already carries with its source.

What questions are FOR — what the practitioner uniquely owns: the benefit,
priorities between conflicting goods, non-goals, acceptance, the approvals
doctrine reserves to them, and **rulings on contested claims — where their
answer counts only as a fact they know (`basis:`), never as a preference**
(`reconciliation.md` §2). Facts about intent come from the practitioner; facts
about the documents come from the corpus. **Precedence:** a choice the
practitioner uniquely owns is never preference-fishing; the list above reaches
choices that are *not* theirs.

**Default non-blocking.** An unknown on which no fork of the work depends:
write it as a **declared assumption** in the artifact it touches, proceed, and
present the open points **batched**, answered by exception. This branch carries
the SAME evidence duty as a question: each assumption states **what it is taken
from** and **the alternative it excludes**, and every declared assumption
reaches the batch — an assumption nobody is shown is a silent decision. This is
the same structure as the claim ledger's own escalation rule — keep BOTH sides
with their sources and surface them, never silently pick one — and it is this
branch, not the blocking one, where that rule structurally lives: an open
`CONTESTED` set never stops an ingest (`reconciliation.md` §4).

**Blocking is reserved** for three cases: proceeding under ANY assumption would
waste the work (the forks diverge at once); the doctrine reserves the decision
to the practitioner; or the doctrine itself mandates the stop. **Exactly two
mandating files prescribe their own hand-over, and there the general form does
not apply**: `reconciliation.md` §4's escalation form (the claims in the set,
each source, date and provenance, and why the machine cannot decide) — the
mandated form for claim conflicts; and `review.md`'s round cap (the artifact
plus the open findings). That list is closed. Every other blocking question
carries the general form:

- the fork: the concrete options and what each implies for the work;
- the evidence: what you searched, read or tried, and what it leaves undecided;
- why no assumption survives — what work is discarded if you assume and are
  wrong;
- why it is the practitioner's call;
- what stays blocked until answered.

## The round

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
- **Asking what the approved vision already answers**: re-asking goal or
  non-goals that a `Status: APPROVED` Vision or M-VISION already states.
- **Collecting answers without folding them in**: getting replies in chat
  and proceeding to design without writing them into the analysis document —
  the next reader has no record of why the scope is what it is.
