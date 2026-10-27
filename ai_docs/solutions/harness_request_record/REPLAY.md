# F-067 replays

## AC1 — does a fresh agent start the record before its first question?

Prompt (identical for RED and GREEN; only the doctrine under the path differs):

> You are simulating an AI coding agent that has the `agentic-sdlc` skill loaded. The
> skill's operating contract is the file `<worktree>/skills/agentic-sdlc-skill/SKILL.md`,
> with its support files in the same folder (read SKILL.md in full, and any support
> file it tells you to read for this situation). Do not read anything under ai_docs/
> of that repository and do not modify any file.
>
> Situation: you are working in a web-shop project that already has an `ai_docs/` root
> with an APPROVED Vision. The user's first message of the session is, verbatim:
>
> "Vorrei che gli amministratori potessero esportare gli ordini in CSV dal pannello
> admin, filtrando per data e stato. Mi serve per la contabilità, il commercialista lo
> chiede ogni mese."
>
> Task: following the skill exactly as written, list in order the concrete actions you
> would take from this message up to and including your first question to the user.
> For each action say: what you do, which file you create or modify (exact path) if
> any, and which sentence of the skill text requires it (quote it). Be literal: do only
> what the text requires or allows; do not invent steps the text does not contain.
>
> End your output with exactly one line:
> RECORD_BEFORE_FIRST_QUESTION: YES or NO — YES only if, before your first question,
> you would create a file whose purpose is to keep the user's own words verbatim (not
> a distilled analysis), and name it.

Runner: fresh-context subagent, light tier, read-only.

### RED — 2026-10-13, doctrine at `7248c47` (before F-067)

Result line: `RECORD_BEFORE_FIRST_QUESTION: NO`. The agent grepped the skill for
"verbatim", "request record", `audit/requests`, `REQUEST_` and found no such step;
its ten actions create no file before the first question; the answers are folded
into the ANALYSIS afterwards.

### GREEN — 2026-10-13, doctrine of this branch (uncommitted, after the F-067 edits)

Result line: `RECORD_BEFORE_FIRST_QUESTION: YES —
ai_docs/audit/requests/REQUEST_admin-orders-csv-export.md`. The agent created the
record at step 4, right after declaring the level and before the Vision Gate reads,
with R1 quoting the Italian request untranslated; it cited the new Write Triggers row,
the template ("started the moment the level is declared") and the new Vision-Gate
line ("Compare them with the request as recorded"), and planned to append the reply
as R2 before folding it. Scope of the replay: the code lens; the other three lenses
are covered by the shared invariant (trigger, template, citing rule stated in each).

## AC2 — given the record, are F-066's owner statements verifiable?

RED: `MOTIVATING_CASE.md` — without a record, F-066's reviewers marked the owner's
statements CANNOT VERIFY (excerpts author-attested; the reports are not in the repo).

GREEN — 2026-10-13, fresh-context subagent, light tier, read-only. Inputs: F-066's
ANALYSIS, r25, MERGE_REVIEW "Already verified", the rebuilt record
`fixture_REQUEST_merge_review.md` (R1–R11, a late record, author-transcribed), and the
new `review.md` clause. Result line: `OWNER_STATEMENTS: 13/13 resolved, 0
contradicted, 0 unresolved`. The reviewer counted all 13 as CANNOT VERIFY without the
record and 0 with it, and noted that every RESOLVED rests on the author's
transcription (T2 residual).
