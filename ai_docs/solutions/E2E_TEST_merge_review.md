---
feature: F-066
analysis: ANALYSIS_merge_review.md
---
# E2E test: Merge review brief and E2E script

## What changed, in user terms

The validator of the code skill has a new command, `review-map`, that tells an
integrator which files of a change to review and which to skip. At the end of
every significant (L3) change, the agent now also writes a merge review brief
and a test script like this one.

## Environment and preconditions

- The `agentic-sdlc` package built from the merged `main`, installed in a client
  as the release guide describes (`ai_docs/reference/GUIDE_release.md`).
- A scratch git project with an `ai_docs/` root, created by `agentic-sdlc-init`,
  with at least one commit on `main`. Python 3 and git on the PATH.
- `<skill_dir>` below is where the client installed the skill.

## New-behavior scenarios

### S1 — the map classes each kind of file (AC1, AC3)
Steps: 1. In the scratch project, create a branch. 2. Edit a source file, add
`ai_docs/solutions/ANALYSIS_demo.md`, add a row to
`ai_docs/audit/reviews/REVIEW_LOG.md`, and leave one new file untracked.
3. Run `python <skill_dir>/scripts/sdlc_check.py index`. 4. Run
`python <skill_dir>/scripts/sdlc_check.py review-map --base main`.
Expected: one table; the source file and the untracked file are REVIEW, the
ANALYSIS is DESIGN, the REVIEW_LOG is EVIDENCE, `memory/INDEX.md` and
`strategic/features_history.md` are GENERATED; rows grouped
in that order; a totals line follows.
Result:

### S2 — a hand-written file is never skipped (AC2)
Steps: in a project with no `audit/HANDOFF_*.md` file, edit
`ai_docs/audit/handoff.md` by hand, then run `review-map --base main`.
Expected: `ai_docs/audit/handoff.md` is DESIGN, not GENERATED.
Result:

### S3 — bad input is refused (AC4)
Steps: run `review-map --base no-such-branch`, then `review-map --base=-x`, then
`review-map` in a folder that is not a git repository.
Expected: each prints one `[ERROR]` line and exits non-zero; no table.
Result:

### S4 — nothing changed (AC5)
Steps: on a branch with no changes against `main`, run `review-map --base main`.
Expected: "no changes against main", exit 0.
Result:

### S5 — the command is discoverable (AC8)
Steps: run `sdlc_check.py --help`.
Expected: the usual commands, then a "Code lens" block naming `review-map`.
Result:

### S6 — the agent ships both documents at an L3 closure (AC7)
Steps: in the scratch project, ask the agent for a change that triages L3 and let
it run to closure.
Expected: `ai_docs/solutions/E2E_TEST_<feature>.md` and
`ai_docs/solutions/MERGE_REVIEW_<feature>.md` exist; the brief contains a
review-map table, cites REVIEW_LOG rows for what was verified, and states its
"Your judgement" items, "none" included; the E2E script names no tester.
Result:

## Regression scenarios

### R1 — every other command behaves as before
Steps: in the scratch project run `sdlc_check.py index`, `check`, `stale`,
`recall <word>`, `validate`.
Expected: same outputs and exit codes as with the previous release.
Result:

### R2 — session orientation and the per-prompt reminder still fire
Steps: open a new session of the client in the scratch project and send a prompt.
Expected: the orientation text appears at session start and the one-line
reminder on the prompt, as before.
Result:

### R3 — `--help` still lists the knowledge commands
Steps: run `sdlc_check.py --help`.
Expected: the spine's usage and the knowledge overlay's commands (`recall`,
`graph`, `corpus` …) are all still listed above the new block.
Result:

### R4 — L1 and L2 work produce no new document
Steps: ask the agent for a typo fix (L1) and a small fix (L2).
Expected: no `MERGE_REVIEW_*` or `E2E_TEST_*` file is created.
Result:

## Already covered by automated tests

`skills/agentic-sdlc-skill/scripts/test_review_map.py` (classes, the exact
generated set incl. topics/corpus/handoff, git states, refused inputs, a failing
`index`, rename/binary/empty, escaping, help) and the full battery
`python -m unittest discover -s scripts -p "test_*.py"` (245 tests). Retest S1–S5
by hand only to confirm the installed package, not the logic.
