---
id: F-083
feature: kb import keeps a foreign ruling foreign — prov IMPORTED, origin named in its note, its set reopened until ratified
status: COMPLETED
level: L3
start_date: 2026-10-23
end_date: 2026-10-26
domain: code
---
# Feature Analysis: an imported ruling decides nothing until ratified

## Objective

`portability.md` §4 promises that a ruling carried into another project arrives as
`prov: IMPORTED`, names its origin with `imported_from:`, and settles nothing there
until the receiving owner ratifies it. `import` does none of this. It copies the bundle
byte for byte, the row stays `RULING`, and `check` is CLEAN, so a foreign decision binds
the receiving project without anyone there having granted it. That is F-030 threat T1,
still open in the shipped code. Request record:
`audit/requests/REQUEST_kb_import_ruling.md` R1–R3.

**Root cause (mechanism, not symptom).** F-030 shipped the provenance value, the
validator rules that read it and the doctrine, but no code that *produces* the value.
`kb_import_plan` only plans copies. F-030's Action Plan item E lists "enum, provenance
check, reconciliation rule" and nothing that converts, and its round-trip test used a
bundle with no `RULING` row. Marking the row by hand does not reach the documented state
either: the rows the ruling superseded travel with it, and the validator rightly refuses
`SUPERSEDED <id>` when `<id>` is IMPORTED. The documented end state could not be reached,
so the fix is a design (what those rows become, R3) and not only a copy step.

## Feature Vision (alignment)

Serves two project-Vision Goals (`vision/project_vision.md` §Goals):
- "Keep understanding durable across sessions": here, across projects. The decision and
  its basis travel and stay traceable.
- "Never hide a conflict … surface it and let the user choose": the disagreement a
  foreign ruling had closed is visible again until the receiving owner rules.

It also enforces the owner ruling F-030 recorded on 2026-08-03: knowledge crosses,
authority does not. No new capability is added and no Non-Goal is touched. The shipped
command is made to do what its shipped doctrine says.

Spec elicitation was skipped: the brief (R2) fixes goal, scope and acceptance, and the
one open choice was asked and answered (R3).

## Use Cases / User Needs

Actor: the Practitioner (`project_vision.md` §Actors), working with the kb lens.

- **UC1 — the receiving Practitioner imports a colleague's topic that contains a
  decision.**
  - Needs: the knowledge (both sources, the decision, its basis) arrives whole and
    traceable, and the decision is visibly *someone else's*, not silently in force here.
  - Serves: Goal "never hide a conflict", and the durable-understanding Goal.
- **UC2 — the receiving Practitioner agrees with the decision and adopts it.**
  - Needs: one ordinary act settles the topic locally: their own note with their own
    basis.
  - Serves: Goal "let the user choose".
- **UC3 — the agent in the receiving project answers from the ledger after the import.**
  - Needs: the ledger says "disputed; a ruling from project X says 60 s, on this basis",
    never "settled: 60 s".
  - Serves: Goal "never hide a conflict".

Grounding: every product name used already exists (`prov`, `RULING`, `IMPORTED`,
`imported_from:`, `CONTESTED`, `SUPERSEDED`, `basis:`, `origin:`, note, bundle, `import`,
`--dry-run`, `check`). No NEW term, no METAPHOR.

## Functional Spec

### Behaviour

1. **Conversion.** Every claim row with `prov: RULING` in a topic the import writes
   arrives with `prov: IMPORTED`. Its text is unchanged.
2. **The origin is named in the note.**
   - The note the ruling rests on arrives as a **renamed copy**,
     `imported_<source project>_<original name>`.
   - Its frontmatter names the origin (`imported_from: <source project> — <original
     path>`), and its `origin:` reads `imported` instead of `ruling`.
   - Its basis and body are unchanged. Every row citing the note cites the copy at the
     same text.
   - A note in the bundle derived from the ruling note (`derived_from:`) names the
     renamed copy instead, so its chain still resolves, now to the foreign decision.
   - The note under its original name is never written. A Practitioner who copies a
     row out of a skipped topic by hand therefore cannot cite a foreign note as if it
     were local.
   - A bundle note that declares a `basis:` is a ruling note even when no ruling row
     travels with it (another row cites it). It lands renamed too, so a later import of
     its ruling cannot find it under its own name.
3. **The set reopens (R3).**
   - The rows the ruling superseded, and the ruling itself, form one `CONTESTED` set:
     each row names every other member.
   - A ruling that superseded one row gives the pair {row, ruling}.
   - A ruling that superseded nothing arrives `IMPORTED` with state `OK`.
   - A ruling that was itself overruled by a later imported ruling belongs to both sets.
   - A ruling already `CONTESTED` with a newer source keeps that partner.
4. **Ratification** is the ordinary local ruling of `reconciliation.md`.
   - The receiving Practitioner writes their own note with their own `basis:` and adds a
     `RULING` row on it.
   - Every row `CONTESTED` with the imported one, followed transitively (the connected
     sets of point 3), becomes `SUPERSEDED <new id>`, the `IMPORTED` row included.
   - Relabelling the `IMPORTED` row as `RULING` is refused by `check`: a note that names
     a foreign origin cannot carry a local ruling.
5. **Reporting.** The import, `--dry-run` included, reports:
   - how many rulings arrive as IMPORTED;
   - that their sets are CONTESTED until ratified;
   - the renamed note of each ruling that lands only as a note, because its topic was
     skipped.

### Cases

- Bundle with no `RULING` row: behaviour unchanged, writes byte-identical to the bundle.
- Topic skipped because its slug exists: its rows do not land. Each ruling note it
  cites lands renamed, so a merge by hand cites the foreign form. When the target
  already holds that note under its original name with equal bytes (the target is the
  project the note came from), nothing is written for it.
- Re-importing the same bundle is a no-op: the topic is skipped, and the renamed note is
  already there with equal bytes. Importing a project's own bundle back into it writes
  nothing.
- A bundle re-exported by a receiving project and imported into the source project
  carries the renamed copy of the source's own decision. It lands as an ordinary note no
  local row cites. If a row of that bundle points at a row the source does not hold,
  the import refuses (next case).
- A bundle row already `IMPORTED` (a re-export of an earlier import) is untouched: it
  already names its origin.
- Refusals. The import writes nothing and names the row, because each of these would
  leave `check` failing or decide something silently:
  - a row superseded both by a ruling and by a row that is not a ruling;
  - a ruling that rows depend on and that a non-ruling row superseded;
  - a ruling that does not rest on a note cited by line (`reconciliation.md`: a ruling
    is a note);
  - a row whose `CONTESTED` or `SUPERSEDED` pointer would resolve to no row after the
    import (its partner sits in a skipped topic and the target does not hold it), or to
    a row the target holds that does not name it back. This
    implements the "incomplete conflict set" refusal that `portability.md` §3 already
    promised and the code never had;
  - a row settled by a ruling that this import does not write (its topic is skipped), or
    by a row the target already holds as IMPORTED;
  - a renamed note whose path the target already holds with different bytes.

### Acceptance criteria

- **AC1.** Export a topic holding {A, B SUPERSEDED R; R RULING} and import it into an
  empty project. Then:
  - R is `IMPORTED`;
  - its note is the renamed copy carrying `imported_from:` and `origin: imported`, with
    basis and body unchanged;
  - every moved source cites the same text in the copy that it cited in the original;
  - A, B and R are a symmetric CONTESTED set;
  - `check` is CLEAN.
- **AC2.** Ratify the AC1 result (own note with `basis:`, RULING row R2, A/B/R
  SUPERSEDED R2): `check` is CLEAN. Relabel R as RULING instead: `check` reports the
  foreign note.
- **AC3.** A ruling that superseded a single row gives {row, ruling} CONTESTED, and
  `check` is CLEAN.
- **AC4.** Chain (R2 overruled R1) and ruling-contested-with-newer-source: `check` is
  CLEAN after the import, and also after ratifying the connected sets.
- **AC5.** A bundle without rulings gives writes byte-identical to the bundle. A second
  import of a bundle with a ruling is a no-op.
- **AC6.** Every refusal case refuses, writes nothing and names the row.
- **AC7.** A skipped topic's ruling note lands only renamed. Importing a project's own
  bundle back into it writes nothing. A bundle note derived from the ruling note names
  the renamed copy.
- **AC7b.** Shift edge cases: a note without an `origin:` line, a CRLF note, and a
  locator range starting at line 1 all keep citing the same text.
- **AC8.** The real reproduction (TH-01 into an empty TH-02) meets AC1 and AC2
  (`harness_kb_import_ruling/probe.py`).

## Interface Contract

**Surface.** The `import` CLI output. The agent perceives it and relays it to the user
per `portability.md` §0 point 4.

**Idioms reused.** The `[ok]` summary, indented detail lines, `[note]` lines, and
`[ERROR]` followed by "nothing was written" on refusal.

**Added output:**
- the detail line `<n> ruling(s) arrive as IMPORTED: each rests on a renamed copy of its
  note (imported_<project>_…) and settles nothing until you ratify it (portability.md
  §4)`, printed when n > 0, with and without `--dry-run`;
- one `[note]` per skipped topic's ruling note, naming its renamed path;
- refusals in the existing `[ERROR]` form, each naming the row and what to do.

**Flow.** `import` plans (converts, renames, reopens, checks), then writes all or
nothing, then prints the existing closing note to run `check`. No new flag.

## Capability Ledger

| Capability | Verdict | Where / gap |
|---|---|---|
| Plan an import all-or-nothing | EXISTS | `knowledge.py` `kb_import_plan` |
| Parse claim rows of a topic | EXISTS | `kb_parse_claims` |
| Rewrite chosen cells of a row, leaving the rest verbatim | INADEQUATE | `kb_fill_ids` rewrites the id cell only. A small cell-replacement helper is added beside it |
| Mint a claim id from source, locator and qty | EXISTS | `kb_claim_id`, `kb_qty_key` |
| Mark a row foreign and inert | EXISTS | `IMPORTED` and the validator rules (F-030) |
| Refuse a local ruling resting on a foreign note | INADEQUATE | The `RULING` check reads only `basis:`. Added: refuse when the declaring frontmatter also carries `imported_from:` |
| Convert rulings, rename their notes and reopen their sets at the boundary | MISSING | Searched: `knowledge.py` (every `IMPORTED` / `imported_from` hit), the four overlays, F-030's Diary. Nothing produces `IMPORTED`. Designed as one function, `kb_import_foreign_rulings`, which the plan calls |

The `## Component Map` in `strategic/architecture.md` has no row for portability: add
**Portable knowledge (knowledge)** at closure (export closure, additive import, foreign
rulings).

**Guides:**
- `GUIDE_skill_family_changes.md` was read: the copies count once.
- No CURRENT guide covers import internals.
- The model built here is one function, so no comprehension guide is due.

## Impact

### Why a renamed note, and not a sidecar or an edit in place

Weighing (design is mine; R2 asks for `imported_from:` "nella sua nota", and this keeps
it there):
- **Edit in place** (rejected): one frontmatter line inserted into the note shifts every
  line locator that cites it. Probe A shows `#L7-7` re-pointed at `---` with no error.
  Keeping the locator honest changes the claim id, and re-importing then compares the
  edited note with the bundle's and refuses.
- **Sidecar `<note>.meta.md`** (rejected): five readers glob `corpus/notes/*.md` and
  take it for a note. A bundle sidecar landing beside an existing note re-declares that
  local note; reproduced, a round trip back to the source project broke its own ruling.
  The `given/` variant contradicts the no-op re-import.
- **Renamed copy** (taken): it is a new file, so it can be written in its foreign form.
  - Every reader already handles notes.
  - It never touches a local file.
  - It is deterministic, so re-import stays a no-op.
  - `docs_site.py` already maps `origin: imported` to "kb" instead of "decision".
  - Its cost: the IMPORTED row's id differs from the source project's, because the
    path and line moved. This is honest: it is a different file, holding another
    owner's decision.

### Changes

| Path | Change | Serves |
|---|---|---|
| `skills/agentic-sdlc-skill/scripts/knowledge.py`, plus the 3 identical copies in `distributions/*/skills/*/scripts/` | ADD `kb_import_foreign_rulings` and `_kb_replace_cells`. MODIFY `kb_import_plan` (writes carry bytes; conversion, rename, reopen, refusals); `kb_cmd_import` (writes bytes; report lines); `kb_check_claims` (RULING on a note that carries `imported_from:` is an error; the SUPERSEDED-by-IMPORTED message names the ratification act) | UC1–UC3, AC1–AC7 |
| `scripts/shared_manifest.json` ×4 | REGENERATE (`shared_files.py --update`) | drift guard |
| kb `scripts/test_claim_ledger.py` | ADD `TL_F083_ImportedRuling` (AC1–AC7). MODIFY the round-trip test (writes carry bytes) and the docstring of `test_a_reratified_row_settles_normally` (an own note, not a relabel) | Test Strategy |
| kb `portability.md` §0.4, §3, §4 | rewrite to the behaviour above | UC1, UC2 |
| kb `reconciliation.md` §Rulings that came from another project | the reopened set, the renamed note, the ratification act over connected sets | UC2 |
| kb `distillation.md` prov list | the note is the renamed copy carrying `imported_from:` | consistency |
| kb `evals/scenarios/import_places_never_overwrites.md` | setup and pass criteria: an IMPORTED row rests on a renamed note; ratification is an own note plus a RULING row | doctrine/eval drift |
| `distributions/kb-agentic-skill/README.md` | Portable knowledge bullet | UC1 |
| `ai_docs/strategic/skill_family_agent_workflows.md` (F-030 paragraph) | same behaviour, in Italian | derived doc |
| `ai_docs/strategic/architecture.md` `## Component Map` | row Portable knowledge | architect pass |
| `CHANGELOG.md` (root), kb, mkt and course `CHANGELOG.md` | `[Unreleased]` entries: the shared `check` change in every lens, the import change in kb | release |
| `ai_docs/solutions/harness_kb_import_ruling/probe.py` | replay on the real TH-01, with baseline probes | AC8 |

### Mechanism

1. **Gather.**
   - Collect every bundle topic.
   - Each `RULING` row's first source must be `corpus/notes/<name>.md#L<a>-<b>`, and the
     note must start with a frontmatter.
2. **Rename.**
   - New path: `corpus/notes/imported_<slug(project)>_<name>`. The project name is
     `source_project` from the manifest, lower-cased, with anything outside `[a-z0-9]`
     replaced by `-`.
   - New bytes, every inserted line placed right after line 1 (the opening `---`) and
     ending with the note's own line ending (CRLF or LF):
     - `imported_from: <project> — <original path>` is inserted;
     - an existing `origin:` key line (matched like the frontmatter parser: key
       `origin`, any case, any value) is rewritten in place to `origin: imported`;
     - when there is none, `origin: imported` is inserted too.
     The shift `k` is the number of inserted lines (1 or 2).
   - Locators move as lines do. `L<a>-<b>` with a ≥ 2 becomes `L<a+k>-<b+k>`; with
     a = 1 it becomes `L1-<b+k>` (b ≥ 2) or stays `L1-1`.
   - Every source cell in written rows that cites the note moves to the new path with
     its locator moved. Cells may hold several sources; the id is re-minted
     (`kb_claim_id`) only when the first source moved, and the old→new map is applied to
     every state cell.
   - Self-check before anything is written: for every moved locator, the text the new
     locator addresses in the copy equals the text the old one addressed in the
     original (inserted lines excepted). A mismatch refuses the import. `check` cannot
     catch this: it verifies line bounds only.
   - Every `corpus/notes/*.md` file in the bundle whose `derived_from:` names the ruling
     note (by path or bare name) is written with that entry replaced by the renamed path.
     The edit stays on the `derived_from:` line, so no line moves. The rewrite is
     deterministic, so the byte comparison of a re-import still holds. If the target
     already holds that derived note with its original bytes (an earlier bundle carried
     it without the ruling note), the import refuses with the different-bytes message.
     A `given/*.meta.md` sidecar whose `derived_from:` names the ruling note is not
     rewritten, and its chain shows as a stale warning.
   - The frontmatter parser reads the first 60 lines. A key on frontmatter lines 59–60
     of a ruling note can fall out of view after the insertion. Accepted as negligible:
     no note in the field is that long.
   - Ruling notes are the notes cited by a `RULING` row in any bundle topic, plus every
     bundle note declaring `basis:` without `imported_from:`. One is left unrenamed only
     when the target already holds it under its original name with equal bytes **and**
     no topic this import writes rules on it (the source-project case). A written topic
     that rules on it converts, whatever the target holds.
   - The text is read past a UTF-8 BOM, which the copy keeps.
   - The same-text self-check cannot fail while the shift rule is correct; it guards
     the rule against future edits and has no input-driven test.
3. **Convert and reopen.**
   - `prov` RULING becomes IMPORTED.
   - Members of a ruling's set are the written rows `SUPERSEDED` by it (old ids).
   - For every member and ruling: CONTESTED partners = existing partners ∪ the other
     members of each set it belongs to.
   - The refusal cases are detected here.
4. **Boundary check.** Each `CONTESTED` or `SUPERSEDED` pointer of a written row (after
   renames) must resolve to a written row or to a row the target already holds;
   otherwise the import is refused. A `CONTESTED` pointer at a row the target holds
   (and the import does not write) must find that row already `CONTESTED` and naming
   the written row back, since the import never edits an existing topic. A `SUPERSEDED`
   pointer at a row that is or becomes IMPORTED is refused too. The check runs on every
   import, with or without rulings.
5. **Writes.**
   - The original note path is dropped.
   - The renamed note is added, unless equal bytes are already there; different bytes
     are refused.
   - Topics are written with their rewritten bytes.
   - The write tuple becomes `(rel, data: bytes, dst)`.

### Blast radius

Enumerated by grep (`kb_import_plan|kb_cmd_import|kb_check_claims`) over every `.py`
in the repository; no LSP for this tree.
- `kb_import_plan` has two consumers: `kb_cmd_import`, and `test_claim_ledger.py` (the
  round-trip, no-op, never-overwrites and refusal tests). Only `kb_cmd_import` and the
  round-trip test dereference the tuple's second element.
- `kb_check_claims` gains one condition in the `RULING` branch. Its consumers (`graph`,
  `check`, and every lens through `knowledge.py`) get one new error class, which fires
  only on a note that carries `imported_from:` under a `RULING` row.
- Export is not changed: converting at the receiving end protects against bundles from
  any version.
- The spine `sdlc_core.py` and `docs_site.py` are untouched.
- The four `knowledge.py` copies stay identical (drift guard).

## Security and Threat Model

The bundle is external input; the threat that motivates the unit is F-030 T1.

| Threat | Answer |
|---|---|
| T1 — authority laundering: a foreign ruling settles rows here | converted, renamed and its set reopened at the boundary, whatever the bundle says. The validator rule (SUPERSEDED by IMPORTED) stays as the backstop |
| T1a — laundering by a hand merge out of a skipped topic | the note under its original name is never written; only the foreign renamed copy lands |
| T1b — relabelling: the IMPORTED row flipped back to RULING | `check` refuses a RULING whose note carries `imported_from:`. Residual, stated: a Practitioner who deliberately also edits the foreign note's frontmatter is not detectable by a validator. That is a deliberate act, not an accident the product can catch |
| T2 — a hostile cell breaks the row rewrite | rows that do not parse are left verbatim (the parser already reports them). The rewrite touches only the id, source, `prov` and state cells of rows the parser accepted |
| T3 — the renamed path escapes the root | built from a confined note path plus a slug restricted to `[a-z0-9-]`, and re-confined with `confine_under` before writing |
| T4 — locator drift silently corrupts the cited span | the shift rule moves every citing locator in written rows, and the plan's self-check compares the addressed text before writing. Probe A shows the failure an edit in place would cause |
| T5 — a half-converted tree | conversion is part of the plan, and the boundary check refuses every pointer that would dangle or settle on a foreign row. Guaranteed for the claim states the import writes. Not claimed: findings outside them (index alignment, which `index` regenerates; a stale chain in a note the bundle did not carry) |
| T6 — a bundle file re-declares an existing local file | nothing is written beside an existing note; the renamed path is new or byte-equal |
| T7 — trees imported before this fix (≤ 1.48.0) | they hold the foreign ruling as RULING on its original note, so the skipped-topic rule cannot tell them from the source project. Not repaired automatically. CHANGELOG and `portability.md` §4 say what to do: delete the imported topic and its files and import again, or convert by hand (rename the note, `imported_from:`, IMPORTED, reopen the set) |
| T8 — the origin slug is the exporting folder's name (`source_project`) | known limit. Two clones of one project in differently named folders produce different renamed paths for one decision, and names that slug alike ("TH 01", "th-01") can collide; a collision with different bytes is refused, never overwritten. The bundle carries no stabler project identifier |

Weighing for the mixed-supersession refusal:
- **Taken: refuse.** It keeps the import all-or-nothing (`portability.md` §3) and decides
  nothing silently. Against it: a rare legitimate source state (a row both split and
  ruled on) cannot be imported until its owner re-rules in the source project.
- **Rejected: keep the split successor and drop the ruling's claim on that row.** It
  serves import convenience, but it silently loses a relation, which is the class of
  loss reconciliation refuses.

## Action Plan

1. [x] Probes on the reproduction (they ship in the harness).
2. [x] Independent design review to PASS.
3. [x] RED: `TL_F083_ImportedRuling` failing on the current code.
4. [x] GREEN: `kb_import_foreign_rulings`, the plan, command and validator changes. Copy to
   the 3 distributions; regenerate `shared_manifest.json`.
5. [x] Docs: portability, reconciliation, distillation, eval scenario, kb README, workflows,
   Component Map, CHANGELOG.
6. [x] Harness replay on TH-01 into an empty project; batteries ×4; drift guard; `check`.
7. [x] Closure: E2E script, closure review, merge brief, index, handoff.

## Test Strategy

**Unit tests** (kb battery, `TL_F083_ImportedRuling`), one branch per test:
- AC1: conversion, renamed note, reopened set, `check` CLEAN through `main()`;
- AC2: ratification CLEAN, relabel refused;
- AC3: singleton set;
- AC4: chain and contested-with-newer-source, after the import and after ratifying the
  connected sets;
- AC5: byte-identical writes without rulings, and the no-op re-import;
- AC6: one test per refusal;
- AC7: a skipped topic's note lands renamed; a project's own bundle re-imported into it
  writes nothing; a derived note names the renamed copy;
- AC7b: no `origin:` line (shift 2), CRLF note, range from line 1 — each asserts that
  the text at the new locator equals the text at the old;
- boundary: a written row CONTESTED with a row of a skipped topic the target lacks is
  refused.

**Replay.** `harness_kb_import_ruling/probe.py <scripts> <TH-01 root> <topic>`:
- baseline probes that are claims about today's validator (B: a reopened set with a
  foreign note is legal; A: an edit in place re-points the locator);
- then AC1 (including the same-text check for every moved locator) and AC2 on the
  real export.

**Family.** The four batteries and the drift guard.

## Diary / Current State

**2026-10-23 — opened.** `Level: L3 · router: GUIDE_skill_family_changes.md → read`.
- Worktree `wt-kb-import-ruling`, branch `fix/kb-import-ruling` from `origin/main`
  (1df13df, v1.48.0).
- F-083 is the first id free after fetch; F-082 is taken on `fix/codex-agents-skills`.
- Reproduced on a scratch copy of TH-02 with the earlier import removed: the row stays
  RULING, there is no `imported_from:`, and `check` is CLEAN.
- Owner answered the one open choice (R3): reopen the set.

**2026-10-26 — design review round 1: FAIL (3 blockers, 11 WARN).** The reopened set
held (chains included). The sidecar did not:
- B1: readers of `corpus/notes/*.md` take it for a note.
- B2: a round trip back to the source project re-declared, and broke, the source's own
  ruling.
- B3: amending a `given/` sidecar breaks the no-op re-import.

Redesigned on a renamed note. Probe R, on the real reproduction: renamed copy with
`imported_from:` and `origin: imported`, line shifted, id re-minted, reopened set; result
CLEAN. Probe F, on the same tree with today's validator: relabelling the row RULING
leaves the claim check clean. T1b therefore needs the new validator condition, which
must be shown red before it is written. W1–W11 are answered in this rewrite: the
boundary check, the hand-merge rule, the T1b residual, the Impact list, ratification
over connected sets, the empty set, the request record kept literally, the weighing,
no mechanism in the Functional Spec, the baseline probes, the case tests, the Vision
citation and `--dry-run` reporting.

**2026-10-26 — design re-review round 2: PASS (provisional, 6 WARN).** All three
blockers were closed by the renamed note. The WARNs, answered in this text:
- the exact shift rule (an inserted `origin:` when absent, CRLF, ranges from line 1)
  and a same-text self-check, because `check` verifies line bounds only;
- the boundary check on every CONTESTED/SUPERSEDED pointer, which also implements
  §3's "incomplete conflict set" refusal that was never coded;
- trees imported before the fix (T7);
- `derived_from:` rewritten in bundle notes;
- the origin slug as a known limit (T8);
- review history taken out of the operative sections.

**2026-10-26 — design re-review round 3: PASS, one WARN, then implemented.** The WARN
was a CONTESTED pointer to a held row that does not name it back. It is closed in
Mechanism 4 and the code, with a test that is red without it.

RED: 25 of 26 new tests failed on the baseline; the remaining one is the
source-re-import no-op, already true. GREEN: kb battery 158/158.

A mutation check confirms the new validator condition is load-bearing: with it
disabled, the relabel test fails.

Two defects were found while going green, both fixed:
- the boundary check had been skipped for bundles without rulings;
- the F-030 round-trip test still read the old write tuple.

Replay on the real TH-01 export into an empty project: 17/17 assertions hold, AC1
and AC2 included (renamed note
`imported_th-01_RULING_trasmissione-sonda_2026-09-20.md`, row `bb01396607f2`, set
{5db6a37edb67, 8d7e02b88444, bb01396607f2}).

Batteries: code 464, kb 746, mkt 466, course 459, all OK; the four `knowledge.py`
copies are identical and `shared_manifest.json` was regenerated ×4.

`check` on the repository: validate rc=0; `stale` rc=1. The same `stale` result shows
on a clean `origin/main` checkout, so it predates this unit.

**2026-10-26 — closure review round 1: FAIL (1 blocker, 8 WARN), corrected.**
- B1: a ruling note the target already held under its own name (an earlier import of a
  topic citing it by another row) stopped a written ruling from converting. It landed
  RULING with `check` CLEAN — the unit's own defect, on another path. Fixed: every note
  declaring `basis:` lands renamed, and the equal-bytes shortcut needs no written topic
  ruling on the note. Two tests, red under the round-1 code (mutation).
- W3: a BOM note is converted and keeps its BOM (test).
- W4: one test per remaining refusal: held IMPORTED, not by line, no frontmatter,
  already foreign, derived note held; the self-check is argued above.
- W2: Component Map path. W5: review log as one row per review. W6/W7: CHANGELOGs ×4,
  §3/§4 refusal lists. W8: handoff. W1: index and check re-run at closure.

**2026-10-26 — closed.** Committed d1b1b98 on `fix/kb-import-ruling` and pushed it to
origin; `main` (9259c3a, the release-1.48.0 registry note) was merged into the branch,
and the branch was fast-forwarded onto `main` at the owner's request (no PR: `gh` is not
installed here, the release guide's merge step). After the merge: batteries ×4, harness,
`check`, `mark` on the changed areas. Still owed: the tester's E2E run, the release
(version numbers stay at `[Unreleased]`), and the course demo TH-02 re-import.
