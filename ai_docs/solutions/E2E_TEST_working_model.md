---
feature: F-085
analysis: ANALYSIS_working_model.md
---
# E2E test: constraints at the moment of action

## What changed, in user terms

An L3 analysis can now be read as a short list of its constraints, by unit or by file.
On Claude Code, just before the agent edits a file those constraints bind, the agent is
shown them; it is never stopped or asked anything because of it. A defect you report
after a merge has its own entry in the review log and in the docs site.

## Environment and preconditions

- The package built from this branch, installed with `npm i -g` from the checkout (or
  the published version that carries this change), on a machine with Claude Code and
  Python 3.
- A git project with `ai_docs/` and one open L3 analysis whose `## Impact` has a
  `### Preservation constraints` row bound to a real file of the project. The repository's
  own `ai_docs/solutions/ANALYSIS_working_model.md` is a ready example (status
  IN_PROGRESS while the branch is open).

## New-behavior scenarios

### S1 — FS4: the view of a unit
Steps: 1. In the project, run `python <skill>/scripts/sdlc_check.py constraints --unit <id>`.
Expected: one line per use case, spec item, threat and preservation row, each ending
with `solutions/ANALYSIS_<name>.md:<line>`; each preservation row followed by its
evidence; the last line says the view never replaces the analysis and names the
sections to read in full. No count, percentage or ranking anywhere.
Result:

### S2 — FS5: the constraints of one file
Steps: 1. Run `constraints --file <a file a preservation row binds>`. 2. Run it on a
file no constraint names.
Expected: 1. the unit's id and file, then only the constraints bound to that file, then
the closing sentence. 2. nothing at all.
Result:

### S3 — FS6: the recall before an edit
Steps: 1. Open a Claude Code session in the project. 2. Declare `Level: L3 · router:
no match` and have the agent read the open analysis. 3. Ask it to edit a file a
preservation row binds.
Expected: before the edit, the agent's context shows `[sdlc constraints]` with the bound
constraints; the edit then proceeds exactly as it would without the hook, permission
prompt included.
Result:

### S4 — FS6: silence where it does not belong
Steps: 1. In a new session, declare `Level: L1` and edit the same file. 2. In another,
declare L3 but never open the analysis, then edit it. 3. Edit a file outside any
`ai_docs` project.
Expected: no recall in any of the three, and no refusal or delay you can notice.
Result:

### S5 — FS7: the note on a missing table
Steps: 1. In an open L3 analysis of the code domain, remove the
`### Preservation constraints` table and run `sdlc_check.py validate`. 2. Add the line
`No existing symbol changed.` under `## Impact` and run it again.
Expected: 1. one `[note]` naming that analysis; the exit code is the same as before
the removal, `--strict` included. 2. no note.
Result:

### S6 — FS10: a defect reported after merge
Steps: 1. Append to `ai_docs/audit/reviews/REVIEW_LOG.md` a row with tier `post-merge`,
model `none (owner report)`, reviewer `owner`. 2. Run `sdlc_check.py benefit`.
3. Run `docs_site.py --root . --open` and look at the chronology.
Expected: 2. every review figure is the same as before the row; one extra line counts
the defect reports. 3. the row appears as "defect reported after merge".
Result:

## Regression scenarios

### R1 — the guide-verdict check still refuses as before
Steps: In a project with guides, start a session, write no router verdict, ask for an edit.
Expected: the edit is refused with the same one-line message as before this change.
Result:

### R2 — install and uninstall
Steps: 1. Install the package. 2. Read `~/.claude/settings.json`. 3. Uninstall.
Expected: 2. two `PreToolUse` entries, the verdict check and the recall, each ending in
`; exit 0`. 3. the uninstall prints "Removed the guide-verdict check hook entry" and
"Removed the constraint recall hook entry" and both entries are gone.
Result:

### R3 — a removed recall hook stays removed
Steps: Delete the recall entry from `~/.claude/settings.json`, then reinstall.
Expected: the recall entry is not added back; the verdict check is untouched.
Result:

### R4 — the other lenses see no change
Steps: With the kb, marketing or course package installed, run `validate` on a project
with an open L3 code-domain analysis without the table.
Expected: no `[note]` about preservation constraints; the output is the one you had
before upgrading.
Result:

### R5 — an older package with the new hook entry
Steps: With the recall entry in settings, install a package version without
`constraints` and edit a file.
Expected: the edit proceeds; nothing is shown.
Result:

## Already covered by automated tests

`test_constraints.py` (view, recall query, hook silence cases and JSON shape, FS7
note and lens gate, `benefit`), `test_skill_invariants.py` (doctrine anchors),
`test_docs_site.py` (the `defect` kind and its label), `test_golden_regression.py`
(code and kb transcripts), `scripts/test_clients.js` (wiring, opt-out, uninstall
names), each distribution's full battery. The live hook probe of 2026-10-27
(`harness_working_model/LIVE_PROBE_2026-10-27.md`) covered S3's context delivery and
R5 once, by hand.
