---
feature: F-083
analysis: ANALYSIS_kb_import_ruling.md
---
# E2E test: an imported ruling decides nothing until ratified

## What changed, in user terms

When you import a topic from another project and it contains a decision (a ruling), the
decision now arrives marked as that project's, not yours. Its note is copied under a new
name, `imported_<project>_<name>`, that says where it came from. The question the
decision had closed is open again in your project: the sources it settled and the
decision itself are shown as disputed (`CONTESTED`). Nothing is settled until you
confirm it with a decision of your own. Imports without decisions behave as before.

## Environment and preconditions

- The kb lens installed from the merged commit, Python 3 on the path.
- A source project holding a ruling that settled a disagreement. The demo
  `C:\workspace\corso AI\demo\TH-01` (topic `sonda-temperatura`) is one; any project
  works if one topic has two rows `SUPERSEDED` by a `RULING` row on a
  `corpus/notes/` note.
- An empty receiving project: a folder with `ai_docs/topics/` only.
- Below, `kb` stands for `python <kb skill>/scripts/sdlc_check.py`.

## New-behavior scenarios

### S1 — AC1: the ruling arrives foreign and the question reopens
Steps:
1. In the source: `kb export --root <source> --out ../bundle --topics sonda-temperatura`.
2. In the receiver: `kb import ../bundle --root <receiver> --dry-run`, then without
   `--dry-run`.
3. `kb index --root <receiver>`, then `kb check --root <receiver>`.

Expected:
- both imports print `1 ruling(s) arrive as IMPORTED: …`;
- `corpus/notes/imported_<source folder>_RULING_…md` exists, its frontmatter has
  `imported_from:` and `origin: imported`, and its basis and text are those of the
  source note;
- the note under its original name does not exist;
- in the topic, the ruling row is `IMPORTED`, and it and the two rows it had superseded
  are `CONTESTED` with each other;
- `check` is CLEAN.

Result:

### S2 — AC2: relabelling is refused
Steps: in a copy of the S1 receiver, change the `IMPORTED` row's `prov` to `RULING` and
run `check`.

Expected: `check` fails with a line saying the note names a foreign origin and that
another project's note cannot carry your ruling.

Result:

### S3 — AC2: ratification settles it
Steps:
1. In the S1 receiver, write `corpus/notes/RULING_ratifica.md` with a frontmatter holding
   your own `basis:` and one line of text.
2. Add a `RULING` row on that note (`kb claim-id --fill` mints its id).
3. Set the three `CONTESTED` rows to `SUPERSEDED <your id>`.
4. `kb index`, `kb check`.

Expected: `check` is CLEAN.

Result:

### S4 — AC6: an incomplete set is refused
Steps: export a topic whose row is `CONTESTED` with a row of another topic. In the
receiver, create an empty topic with the other topic's slug first, then import.

Expected: `[ERROR]` naming the row and the missing partner, then "nothing was written".

Result:

### S5 — AC7: a skipped topic's ruling note lands only renamed
Steps: in a receiver that already has a topic `sonda-temperatura`, import the S1 bundle.

Expected: the topic is reported as skipped; a `[note]` names
`corpus/notes/imported_…`; that file exists, and the original-named note does not.

Result:

## Regression scenarios

### R1 — import without rulings is unchanged
Steps: export a topic with only `GIVEN` rows; import into an empty receiver; compare
the written files with the bundle (`fc /b` or `cmp`).

Expected: byte-identical; `check` CLEAN.

Result:

### R2 — importing twice writes nothing
Steps: run the S1 import a second time.

Expected: `[ok] imported 0 file(s)`, and the topic is reported as skipped.

Result:

### R3 — importing a project's own bundle into it writes nothing
Steps: import the S1 bundle into the source project itself, with `--dry-run`.

Expected: `0 file(s) would be written`.

Result:
