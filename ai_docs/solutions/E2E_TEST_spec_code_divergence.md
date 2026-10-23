---
feature: F-080
analysis: ANALYSIS_spec_code_divergence.md
---
# E2E test: Spec/code divergence state shared by the two skills

## What changed, in user terms

A knowledge-base claim taken from a specification can now say "the code does not do
this yet", pointing at the analysis that put the fix off. `check` refuses the mark
when that analysis is missing or does not mention the claim. The agent, answering
from the claim, says the behavior is required but not yet done. An export leaves the
mark behind.

## Environment and preconditions

- The packages built from the merged commit (code and kb lenses installed side by
  side), Python 3 on the path.
- A scratch project with `ai_docs/`, one source in `corpus/given/` (any short text
  file), and a topic `topics/export.md` holding one claim from it. Use
  `sdlc_check.py anchor` and `claim-id --fill` to make the row valid, then confirm
  `sdlc_check.py check` is CLEAN before starting.

## New-behavior scenarios

### S1 — FS3: a marker with no analysis is refused
Steps:
1. Set the claim's `about` cell to `not-yet-honored-by -> ANALYSIS_export_schedule`.
2. Run `python <code skill>/scripts/sdlc_check.py check --root .`.

Expected: `check` fails with one line naming `solutions/ANALYSIS_export_schedule.md`
and telling you to remove a marker that did not come from this project.

Result:

### S2 — FS4: an analysis that does not cite the claim is refused
Steps:
1. Create `ai_docs/solutions/ANALYSIS_export_schedule.md` with valid ANALYSIS
   frontmatter and no mention of the claim id.
2. Run `check`.

Expected: one error naming the claim id and that analysis.

Result:

### S3 — FS2/FS4: a cited marker is clean
Steps:
1. Add a dated Diary line to that analysis naming the claim id.
2. Run `check`.

Expected: no finding about the claim.

Result:

### S4 — FS5: a relation and the marker share one cell
Steps:
1. Set `about` to `depends-on -> export; not-yet-honored-by -> ANALYSIS_export_schedule`.
2. Run `check`.
3. Then set it to `not-yet-honored-by -> f-080` and run `check`.

Expected: step 2 is clean. Step 3 reports that the reserved predicate needs an
`ANALYSIS_<name>` target.

Result:

### S5 — FS9: export drops the marker
Steps:
1. Restore the valid cell from S4 step 1.
2. Run `sdlc_check.py export --root . --out ../bundle`.
3. Open `../bundle/topics/export.md`.

Expected: the report has one line saying the not-yet-honored markers were dropped,
with no number in it. The bundle's claim keeps `depends-on -> export` and has no
marker. Every other line of the topic is identical to the original.

Result:

### S6 — FS1: the agent answers "required, not yet done"
Steps:
1. With S4 step 1's cell in place, ask the agent (kb lens loaded) a question the
   claim answers ("does the export run nightly?").

Expected: the answer cites the claim id, says the specification requires it and the
code does not yet do it, and names `ANALYSIS_export_schedule`. It does not state the
behavior as current.

Result:

## Regression scenarios

### R1 — An unmarked relation still validates
Steps: set `about` to `depends-on -> export` alone and run `check`.
Expected: clean, as before the change.
Result:

### R2 — A malformed `about` is still refused
Steps: set `about` to `depends-on export` (no arrow) and run `check`.
Expected: one error saying `about` must be `<predicate> -> <slug>` parts joined by `;`.
Result:

### R3 — Export without markers is byte-identical
Steps: with `about` set to `-`, export the topic as in S5.
Expected: no drop line; the bundle's topic file is byte-identical to the original.
Result:

### R4 — The docs site shows the cell as written
Steps: run `docs_site.py --root .` and open the claim.
Expected: the "Also concerns" row shows the `about` text as written; no page lists or
counts marked claims.
Result:

### R5 — `validate` is unchanged
Steps: run `sdlc_check.py validate --root .` with the S1 cell.
Expected: no claim finding (validate never ran claim checks); `check` is where S1 fails.
Result:

## Already covered by automated tests

- kb `test_claim_ledger.py` `TL_F080_NotYetHonored`: S1–S5, R2, R3, the predecessor
  case (FS8) and the traversal-shaped targets.
- kb `test_kb_recall.py`: the Topic Recall wording (S6's doctrine) and that no
  generator reads the mark.
- code `test_skill_invariants.py` `NotYetHonoredTrigger`: the Write Triggers row.
- Probe `ai_docs/solutions/harness_spec_code_divergence/probe.py`: B1–B6.
