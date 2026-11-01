---
feature: F-090
analysis: ANALYSIS_review_log_union_check.md
---
# E2E test: the review log's merge line, checked instead of announced

## What changed, in user terms
When a project's review log has no merge rule, so two branches that both add review rows
would conflict when merged, `check` now says so and gives the exact line to add. Nobody has
to read the release notes: the agent sees the note when it closes a piece of work and adds
the line. Nothing else in `check`'s result changes, and session start is unchanged.

## Environment and preconditions
The published packages of this release; a scratch git repository with `ai_docs/` and a
review log (`ai_docs/audit/reviews/REVIEW_LOG.md`) and no `.gitattributes`. Python 3.

## New-behavior scenarios

### S1 — the note appears
Steps: run `python <skill_dir>/scripts/sdlc_check.py check --root .`.
Expected: after the summary line, a `[note]` naming `ai_docs/audit/reviews/REVIEW_LOG.md`
and the line `ai_docs/audit/reviews/REVIEW_LOG.md merge=union`; the summary verdict is the
same as without the note.
Result:

### S2 — the agent fixes it
Steps: in an agent session, ask it to close a small unit of work.
Expected: it runs `check`, sees the note, adds the line to `.gitattributes` at the
repository root; a second `check` prints no such note.
Result:

### S3 — every skill
Steps: repeat S1 with the KB, marketing (`mkt_check.py check --docs-dir ai_docs`) and Course
validators.
Expected: the same note in each.
Result:

### S3b — a marketing project on its own root
Steps: in a project whose docs root is `mkt_docs/` with `mkt_docs/audit/reviews/REVIEW_LOG.md`
and no `.gitattributes`, run `mkt_check.py check` with no `--docs-dir`.
Expected: the note names `mkt_docs/audit/reviews/REVIEW_LOG.md merge=union`.
Result:

### S4 — a project below the repository root
Steps: put the project in a subfolder `pkg/` of the repository; run S1 from `pkg/`.
Expected: the line names `pkg/ai_docs/audit/reviews/REVIEW_LOG.md`.
Result:

## Regression scenarios

### R1 — merge-safe project
Steps: on a project whose `.gitattributes` already has the line, run `check`.
Expected: no new note.
Result:

### R2 — session start unchanged
Steps: open a new agent session on the S1 project.
Expected: the orientation shows no note about the review log.
Result:

### R3 — CI
Steps: run `validate --strict` on the S1 project.
Expected: the same result as before this release; the note is not a warning.
Result:

## Already covered by automated tests
`test_merge_safety.py` (×4): note when unspecified; none with union, a covering pattern, a
custom driver, no review log, no git; path relative to the repository top; a path with a
space and a bracket reads back as union; git failures never break `check`; `check` exit
code unchanged; marketing's `check` prints it; orientation runs no subprocess.
