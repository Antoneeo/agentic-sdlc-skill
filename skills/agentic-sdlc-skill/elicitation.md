# Spec Elicitation

Applies when an L3 request enters phase 3 (Request Analysis), BEFORE
drafting the ANALYSIS document (Standalone) or the D-UC/E-ISP (Hybrid).

Skip path: if the spec is already complete — an approved Vision or explicit
user requirements already answer goal, scope, and constraints — skip the
round and add a one-line note in the analysis stating why it was skipped.
Do not run the round as a formality when the answers are already on record.

## The round

Ask ONE structured set of questions, not a drip of follow-ups. Keep each
question short and numbered; offer concrete options where a real choice
exists (this narrows the reply and speeds up the round). Cover:

1. **Goal / benefit** — what problem this closes, for whom, and why now.
2. **Scope boundaries** — what is explicitly included in this unit of work.
3. **Non-goals** — what is explicitly excluded, so scope does not silently
   creep in later.
4. **Constraints** — technical, compatibility, and security constraints that
   bound the solution space.
5. **Acceptance signals** — how you and the user will both recognize the
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
