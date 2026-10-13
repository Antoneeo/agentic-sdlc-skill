---
feature: F-067
analysis: ANALYSIS_request_record.md
---
# E2E test: Verbatim request record

## What changed, in user terms

When you ask any of the four skills for significant work, the agent now writes your
words down exactly as you said them, in a file under `audit/requests/`, before it
starts interpreting them, and adds each later decision you make. Documents and
reviews refer to those entries instead of retelling what you said.

## Environment and preconditions

- The four packages built from the merged `main` (code, kb, marketing, course),
  installed in a client as `ai_docs/reference/GUIDE_release.md` describes.
- One scratch project per lens with its docs root, created by that lens's init.
- `<skill_dir>` is where the client installed each skill.

## New-behavior scenarios

### S1 — the record starts before the first question (AC1), code lens
Steps: in the code scratch project, send a request that triages L3, e.g. "Vorrei
che gli amministratori potessero esportare gli ordini in CSV dal pannello admin,
filtrando per data e stato."
Expected: before its first question the agent creates
`ai_docs/audit/requests/REQUEST_<unit>.md`; R1 is your sentence, unchanged and not
translated; the agent names the file once in its reply.
Result:

### S2 — answers and approvals are appended before they are used (AC1)
Steps: answer the agent's questions, then approve its design.
Expected: each answer and the approval appear as new entries, each with the question
it answered; earlier entries are unchanged; the analysis cites `#R<n>` where it
relies on what you said.
Result:

### S3 — the same in the other three lenses (AC3)
Steps: repeat S1 with a significant request in kb (a new knowledge unit), marketing
(a full plan, E3) and course (a new course).
Expected: each creates its record under its docs root's `audit/requests/` before the
first question; in marketing, a budget you give lands in the evidence ledger with
`user, REQUEST_<engagement>.md#R<n>` as source.
Result:

### S4 — secrets are not committed (FS3)
Steps: in a request, paste a fake API key and a colleague's phone number the work
does not need.
Expected: the record shows a `[REDACTED: <kind>]` marker in place of each (the kind
wording may vary); the rest of the sentence is verbatim.
Result:

### S5 — reviews check your statements against the record (AC2, AC5)
Steps: let the agent reach its design review on an L3.
Expected: the review request lists the record among its inputs; the review reports
no statement of yours as "cannot verify".
Result:

### S6 — the merge map files the record as evidence (AC4)
Steps: in the code project, run `python <skill_dir>/scripts/sdlc_check.py review-map --base main`.
Expected: `ai_docs/audit/requests/REQUEST_<unit>.md` is in the EVIDENCE group.
Result:

## Regression scenarios

### R1 — small work stays light
Steps: ask each lens for a typo fix (L1/E1) and a small fix (L2/E2).
Expected: no `audit/requests/` file is created.
Result:

### R2 — the question style is unchanged
Steps: on an L3, look at the agent's first question set.
Expected: one numbered set, each question naming its search and what it blocks, as
before; no question is added by the record.
Result:

### R3 — validators and batteries
Steps: in each scratch project run `check` with that lens's validator.
Expected: CLEAN on a fresh project and after an L3 that wrote a record; the record
raises no warning.
Result:

## Already covered by automated tests

`test_skill_invariants.py` (shared, run in each of the four packages: trigger,
template, citing rule, review input and clause), `test_review_map.py` (record classed
EVIDENCE); full batteries code 246, kb 421, marketing 258, course 252 OK. The two
behavioural replays are in `ai_docs/solutions/harness_request_record/REPLAY.md`.
Retest S1–S6 by hand to confirm the installed packages, not the logic.
