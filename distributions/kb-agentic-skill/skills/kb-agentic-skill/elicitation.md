# Spec Elicitation

Applies when an L3 request enters phase 3 (Request Analysis), BEFORE
drafting the ANALYSIS document (Standalone) or the D-UC/E-ISP (Hybrid).

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
