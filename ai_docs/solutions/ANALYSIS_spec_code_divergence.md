---
id: F-080
feature: Spec/code divergence state shared by the two skills
status: COMPLETED
level: L3
start_date: 2026-10-23
end_date: 2026-10-23
domain: code
---
# Feature Analysis: Spec/code divergence state shared by the two skills

## Objective

When the code does not yet do what a specification claim in the knowledge base says,
and the fix is deferred, that fact today lives only in an ANALYSIS (and maybe a
roadmap line). kb-agentic's Topic Recall answers from the claim and presents the
specification as if the code honored it. This unit gives the claim a declared,
checked pointer to the ANALYSIS that records the deferral. Recall then cites the
claim as "required, not yet done". The ANALYSIS cites the claim id back, so the two
records cannot drift silently. Request: `audit/requests/REQUEST_spec_code_divergence.md`
R1. Admission: `vision/rulings.md` r33 (R3).

## Feature Vision

- **Benefit** — Vision v9 (APPROVED) Goal "keep understanding durable … nothing
  load-bearing lives only in a transcript", and the Team-lead Actor's "one source of
  truth". Two records exist (the KB claim and the ANALYSIS), and today they
  disagree with nothing showing either of them the other.
- **Actors** — from the project Vision: *Solo developer using an AI agent* and
  *Team lead needing governance*. *Adopter evaluating the paid layer* is touched by
  the Hybrid exclusion below.
- **Non-goals** — the r33 conditions bind and are not restated here (rulings.md r33).
  This unit adds two of its own. The cases "code correct, spec wrong" and "spec
  corrected in place" stay with SUPERSEDED/CONTESTED (`reconciliation.md`).
  **Hybrid is out of this unit by owner decision (R7: "Standalone now, Hybrid
  later")**: the target grammar knows Standalone `ANALYSIS_*` only, and the Write
  Trigger is scoped "(Standalone)". This narrows R4 in Hybrid projects. Until a
  later unit closes it, an Adopter who adds devPNT loses the marker duty (not any
  document). The narrowing is the owner's, recorded in R7.
- **Success signals** — the probe `harness_spec_code_divergence/probe.py` turns
  B1–B6 green. A recall over a marked claim names the ANALYSIS (FS1). `check` refuses
  a dangling or uncited marker (FS3, FS4).

## Use Cases / User Needs

- **UC1 (Solo developer)** — asks the agent "does the export run nightly?". The KB
  holds the spec claim. The agent answers that the spec requires it and the code
  does not yet do it, naming the ANALYSIS that deferred the fix. *Benefit: durable
  understanding (the answer matches what the project knows).*
- **UC2 (Solo developer / Team lead)** — a Standalone L3 finds code contradicting a
  KB spec claim and defers the fix. It records the deferral in the claim (marker)
  and in its ANALYSIS (claim id), once (R4, scoped by R7). *Benefit: one source of
  truth.*
- **UC3 (Solo developer)** — a later L2/L3 makes the code honor the claim and
  removes the marker in the same commit; an L1 fix is exempt (R6). *Benefit:
  durable understanding, without an L1 step.*
- **UC4 (Team lead)** — `check` refuses a marker whose ANALYSIS is missing or does
  not cite the claim, so neither half can exist alone. *Benefit: one source of
  truth, mechanically held.*
- **UC5 (Team lead)** — exports topics to another project. The bundle carries no
  marker, because markers describe the origin's code, and the target passes its own
  checks. *Benefit: one source of truth per project (a marker never asserts another
  project's code).*

Grounding: EXISTS — claim, claim id, `about` cell, Topic Recall, `check`, export,
reconciliation, ANALYSIS, `topics/`, `solutions/` (kb `distillation.md` §2,
SKILL.md §Topic Recall, `portability.md` §2, `reconciliation.md` §3; code
`templates.md`). NEW — the reserved predicate `not-yet-honored-by` and the `; `
separator in `about`. No METAPHOR names.

## Functional Spec

- **FS1 Recall.** When an answer cites a claim marked as not yet honored, it states
  that the specification requires the behavior and the code does not yet do it, and
  names the analysis. A marked claim is never cited as current behavior. An unmarked
  claim is cited as today.
- **FS2 Marking on deferral (Standalone).** A Standalone L3 that defers fixing code
  which contradicts a KB claim writes the marker on that claim and cites the claim
  id in its own analysis. The deferring unit does this; no knowledge unit is opened
  (the marker states the code's relation to the claim, not what the source asserts).
- **FS3 Dangling marker.** On `check`, a marker whose analysis does not exist in this
  project is an error naming the analysis and telling the user to remove the marker
  if it did not come from this project.
- **FS4 One-sided marker.** On `check`, a marker whose analysis cites neither the
  claim id nor the id of a row this claim succeeds (FS8) is an error naming the
  claim id and the analysis.
- **FS5 Coexistence.** A claim may carry relations and the marker together, in one
  cell, separated by `; `. A malformed part is an error, as a malformed `about` is
  today. The canonical separator is `; `; a bare `;` is tolerated, as in the source
  column. The reserved predicate with a non-analysis target is an error, and an
  ordinary relation pointing at an analysis is an error.
- **FS6 Removal.** The L2/L3 change that makes the code honor a marked claim removes
  the marker in the same commit. An L1 fix is exempt, so a marker may outlive an L1
  fix. That residual is stated and accepted (R6): the marker then under-claims the
  code, and never over-claims it.
- **FS7 No selection.** No command output, report, site view or orientation line
  lists, counts, filters or orders claims by the marker. The marker has no reverse
  direction. The site shows the `about` text per claim, as today.
- **FS8 Supersession.** A superseded row keeps its marker with its text (reconciliation
  keeps superseded text intact). Whoever supersedes it copies the marker to each
  successor that still states behavior the code does not have. An analysis citing
  the predecessor's id satisfies the successor's back-citation, so no analysis is
  edited. A CONTESTED row keeps its marker unchanged.
- **FS9 Export.** Export drops every marker from the bundle and, when it dropped any,
  says so in one line without a number (a count would be a count of claims by the
  mark, FS7). Import is unchanged: a marker that still arrives (a hand-copied tree)
  meets FS3.

Acceptance: FS3/FS4/FS5/FS9 are checked by the battery and the probe (B1–B4, B6),
FS8 by the battery only;
FS1/FS2/FS6 are doctrine, guarded by doctrine invariants; FS7 is checked by a test
over the generators (Test Strategy).

## Interface Contract

Fires: the change modifies surfaces an actor acts on or perceives. These are the
claim table's `about` cell (edited by the agent or the practitioner), the `check`
messages, the `export` report and the recall answer. `validate` is not a surface:
it does not run the claim checks (`kb_cmd_validate` passes `full=False`).

- **Actors and surfaces.** The agent edits a claim row in `topics/<slug>.md` (idiom
  in use: one table row per claim, cell grammars in `distillation.md` §2, and `;`
  already joins several sources). The agent or a person runs `sdlc_check.py check`
  (idiom: one finding line per defect, exit 1 on error) and `sdlc_check.py export`
  (idiom: `[ok]` line plus indented facts, e.g. "+N topic(s) added"). The person
  reads the agent's answer (idiom: claim ids cited inline; SUPERSEDED names its
  successor).
- **Flow (UC2/UC4).** The agent writes `not-yet-honored-by -> ANALYSIS_<name>` in the
  cell and the claim id in the ANALYSIS. `check` → in the code and kb lenses,
  `kb_cmd_check` runs the graph section (`kb_cmd_graph` → claim checks); marketing
  reaches it through `kb_validate_surface(full=True)` on `check`; course through
  `knowledge.main`. The claim checks parse the cell, resolve
  `solutions/ANALYSIS_<name>.md` under the docs root, and look for the claim id (or a
  predecessor's) in it. One finding returns per defect, or nothing.
- **Flow (UC1).** The person asks → Topic Recall descends to the claim → the answer
  cites the claim id with "the code does not yet do this — ANALYSIS_<name>".
- **Flow (UC5).** `export` → closure as today → bundle writer drops markers from the
  topic text it writes → one report line "not-yet-honored markers dropped: they
  describe this project's code", with no number.
- **Feedback.** Every defect returns one error line naming the claim location and
  what to do (FS3/FS4/FS5). A clean marker returns nothing; silence is the success
  state, as for every claim check. Export adds its one line only when it dropped a
  marker, never a count.
- **Constraints read.** The claim id is content-addressed and excludes `about`, so
  dropping a marker never changes an id. Both lenses resolve one docs root
  (`GUIDE_shared_project_memory.md`), so `topics/` and `solutions/` are siblings.
- **New idiom.** None: `; ` reuses the source column's separator; the export line
  reuses the indented-fact form of the "+N added" line, without its number.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| parse a claim's `about` cell | INADEQUATE | `knowledge.py#kb_check_claims` grammar block | probe A2: one relation per cell; A1: the target is never resolved |
| resolve a project ANALYSIS by name | EXISTS | docs root + `solutions/`, `sdlc_core.confine_under` (used by the same function for sources) | `kb_check_claims._resolved` resolves cited paths under the root |
| run claim checks from every lens's `check` | EXISTS | `knowledge.kb_cmd_check` → `kb_cmd_graph` → `kb_check_claims` (code, kb, course); `kb_validate_surface(full=True)` (marketing) | probe A3: the code lens's `check` reports a bad `about` |
| write an export bundle | INADEQUATE | `knowledge.py#kb_bundle_write` writes topic text verbatim | re-read: "no path is rewritten"; markers would travel |
| cite claims when answering | INADEQUATE | kb SKILL.md §Topic Recall; shared `memory.md` | probe A4: no rule for the marker; SUPERSEDED has one, the model to follow |
| tell an L3 to record a deferral | MISSING | code SKILL.md Write Triggers | grep `defer`/`not yet` over code SKILL.md, templates.md: no trigger |

## Impact

Blast radius (symbol identity):
- `knowledge.kb_check_claims` has one caller, `knowledge.kb_cmd_graph`. Every
  package's `check` reaches it: code and kb through `kb_cmd_check`, marketing
  through `kb_validate_surface(full=True)` (`mkt_check.py`), course through
  `knowledge.main`. `validate` does not reach it.
- `knowledge.kb_bundle_write` has one caller, `kb_cmd_export`.
- No other code parses the `about` cell. `docs_site.py` (`build_kb`) copies it as
  text and `app.js` shows it as the "fact_about" row; both work with `; ` unchanged.
  A grep for `["about"]` and `about` over `skills/` and `distributions/` returns only
  these sites and tests.

| File | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/scripts/knowledge.py` (shared ×4, drift-guarded) | `kb_check_claims`: split `about` on `; `; each part `<pred> -> <slug>`, or the reserved predicate with `ANALYSIS_[A-Za-z0-9_-]+`; resolve `solutions/<target>.md` (FS3) and require the claim id or a predecessor's in it (FS4, FS8). `kb_bundle_write` drops markers and returns whether it dropped any; `kb_cmd_export` prints one line without a number (FS9) | FS3–FS5, FS8, FS9 |
| `distributions/*/scripts/knowledge.py` (×3) | verbatim copy | drift guard |
| `scripts/shared_manifest.json` (×4) | regenerated (`shared_files.py --update`) | drift guard |
| `memory.md` (shared ×4) | D4 | FS1 for any lens answering from claims |
| `distributions/kb-agentic-skill/.../SKILL.md` | D3, §Topic Recall "The act." | FS1 |
| `distributions/kb-agentic-skill/.../distillation.md` | D1, §2 `about` bullet | FS2, FS5, FS7, FS9: the marker's meaning |
| `distributions/kb-agentic-skill/.../templates.md` | D2, claim-table `about` line | FS5 |
| `distributions/kb-agentic-skill/.../reconciliation.md` | D7, §3 | FS8 |
| `distributions/kb-agentic-skill/.../portability.md` | D8, §2 | FS9 |
| `skills/agentic-sdlc-skill/SKILL.md` | D5, one Write Triggers row | FS2, FS6 |
| `skills/agentic-sdlc-skill/templates.md` | D6, Diary comment | FS2 |
| `distributions/kb-agentic-skill/README.md` | Extraction (step 2) and Recall (step 6) name the marker | audit-plan duty for `distributions/`; FS1 |
| `ai_docs/strategic/skill_family_agent_workflows.md` | the kb extraction and recall paragraphs, the code-lens L3 duties (mark on deferral, remove on L2/L3) and §"Quando convivono" (the link between the two lenses) | audit-plan duty for both areas |
| `README.md` (code package) | none: it names the Write Triggers table, not its rows | checked: line 23 |
| `distributions/kb-agentic-skill/.../scripts/test_claim_ledger.py` | new test class | FS3–FS5, FS8, FS9 |
| `distributions/kb-agentic-skill/.../scripts/test_kb_recall.py` | doctrine invariants | FS1, FS7 |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | doctrine invariant (Write Triggers row) | FS2, FS6 |
| `ai_docs/strategic/architecture.md` | Component Map row "Claim ledger": the `about` grammar, the marker check, the export drop | the component's contract changed |
| `ai_docs/vision/rulings.md` | r33 ceremony and basis amended: L2 pays on fixing a marked claim (R6), Hybrid excluded (R7), and the figures the owner confirmed (R8) | the row must match what was accepted |
| `CHANGELOG.md` + distribution CHANGELOGs | entries under the open `[Unreleased]` sections | release notes |
| request record, this ANALYSIS, harness, E2E, MERGE_REVIEW, HANDOFF, indexes | records | closure |

**Ceremony cost (r33 budget door; the owner re-confirms these figures, R5).** The
doctrine deltas D1–D8 are written verbatim in
`harness_spec_code_divergence/deltas.py`, which prints their UTF-8 bytes:

| Delta | Where | Bytes | Read |
|---|---|---|---|
| D1 | kb `distillation.md` §2 | 576 | when distilling |
| D2 | kb `templates.md` | 150 | on trigger |
| D3 | kb `SKILL.md` §Topic Recall | 181 | every kb session |
| D4 | shared `memory.md` (×4 identical) | 91 | on trigger |
| D5 | code `SKILL.md` Write Triggers | 354 | every code session |
| D6 | code `templates.md` | 111 | on trigger |
| D7 | kb `reconciliation.md` | 222 | on trigger |
| D8 | kb `portability.md` | 135 | on trigger |

The total is 1,820 B, against the ≈ 850 B estimated in R5 (+970 B). The review
findings added D7 and D8 and grew D1. Read in every session, L1 included: 535 B
(D3 + D5). The READMEs and `skill_family_agent_workflows.md` are not loaded by
agents.
Steps:
- **L1:** zero steps; 535 B read cost.
- **L2:** a step only when it fixes a marked claim (one cell removed, R6).
- **Per deferring Standalone L3:** one claim cell and one id in the ANALYSIS (R4, R7).
- **Per supersession of a marked row:** one cell per successor that still states the
  unhonored behavior (FS8).
- **Per answer citing a marked claim:** one clause.

Nothing is removed in exchange: the cost is accepted, not offset.

## Security and Threat Model

Surfaces: filesystem (the validator opens a path derived from a table cell; export
writes rewritten topic text) and external input (a claim row may arrive in an
imported bundle or a hand-copied tree).

- **T1 Path traversal through the target.** The target grammar is
  `ANALYSIS_[A-Za-z0-9_-]+`, so it has no `/`, `\` or `.`. The path is
  `<docs>/solutions/<target>.md`, still resolved through `sdlc_core.confine_under`.
  That makes the guard independent of the regex (defence in depth). Mitigated, with
  a test.
- **T2 Foreign marker.** Export drops markers (FS9). A marker that arrives another
  way names an analysis of its origin, and FS3 refuses it. Residual, stated: an
  agent could silence FS3 by creating a stub ANALYSIS that cites the id. The error
  text says to remove a marker that did not come from this project. Doctrine D1
  makes writing a marker the duty of the unit that defers, so a stub is a doctrine
  violation that a closure review sees. Not prevented mechanically.
- **T3 Laundering the mark into a work queue.** A view or command listing marked
  claims, or a reverse index from analyses to claims, would become a defect register
  (r33; r2/r9; Non-Goal 1). FS7 forbids both, and a test checks that no generator
  references the predicate outside the claim checks and the export drop. Mitigated
  by construction plus a check.
- **T4 Export rewriting corrupts a topic.** The drop edits only the `about` cell of
  claim rows the parser recognised, and only the parts carrying the reserved
  predicate. Any other byte of the topic file is written unchanged, and a test
  compares the result. Mitigated.
- **T5 Read cost.** One extra file read per distinct marked target per `check`,
  memoised per run. Negligible.

No authentication, cryptography, network or personal data is involved.

## Action Plan

- [x] Design review gate (`review.md` moment 1), round 1: FAIL (2 BLOCK, 9 WARN), answered in this revision.
- [x] Scoped re-review, round 2: FAIL (1 BLOCK, 4 WARN), answered.
- [x] Scoped re-review, round 3: PASS.
- [x] Owner confirms the ceremony figures above: R8 «Accept 1,820 B».
- [x] RED: `test_claim_ledger.py` FS3–FS5/FS8/FS9 cases; doctrine invariants.
- [x] GREEN: `knowledge.py` check and export drop; copy ×3; manifest update.
- [x] Doctrine deltas D1–D8 as costed; READMEs and `skill_family_agent_workflows.md`.
- [x] Probe B1–B6 green, baseline A1/A2/A4 red (the flip).
- [x] rulings r33 amendment; Component Map row; CHANGELOG entries; E2E_TEST; closure review; MERGE_REVIEW; `index`; `check` CLEAN; four batteries.

## Test Strategy

- **Unit (kb `test_claim_ledger.py`):**
  - A cited marker is clean (FS2/FS4 green path).
  - A missing target is an error naming it (FS3).
  - An uncited target is an error naming the claim id (FS4).
  - Relations plus the marker in one cell are accepted. A malformed part, a reserved
    predicate with a slug target, and a relation pointing at an analysis are refused
    (FS5).
  - A traversal-shaped target is refused by grammar (T1).
  - A successor whose analysis cites only the predecessor's id is clean (FS8).
  - Export of a topic with a marked claim writes a bundle without the marker and
    with every other byte unchanged, prints the drop line with no digit in it, and
    the bundle passes the claim checks (FS9, T4).
- **Doctrine invariants:**
  - kb `test_kb_recall.py` asserts the Topic Recall act names `not-yet-honored-by`
    and "never as current behavior" (FS1).
  - kb `test_kb_recall.py` asserts that `docs_site.py` and `sdlc_core.py` never
    contain `not-yet-honored-by`, and `knowledge.py` contains it only inside the
    claim checks and the export drop (FS7).
  - code `test_skill_invariants.py` asserts the Write Triggers row names
    "(Standalone)" and "L1 is exempt" (FS2/FS6).
- **Probe:** `harness_spec_code_divergence/probe.py`, B1–B6 green; `--baseline`
  A1/A2/A4 go red once shipped (A3 stays green).
- **Batteries:** code, kb, mkt, course `unittest discover`, all green; drift guard green.

## Diary / Current State

**2026-10-23 — admission and design.** Owner ruled r33 ADMIT (R3), the marker is
mandatory on deferral (R4), cost accepted in principle (R5), removal on L2/L3 with L1
exempt (R6). Elicitation round skipped: goal, scope and constraints are on record
(R1, R3–R6, Vision v9, r33); the one open doubt (removal) was asked and answered
(R6). Probe written red-first: baseline A1–A4 green, target B1–B5 red. Router:
`GUIDE_skill_family_changes.md` (the shared copies count once; the level stays L3).
Guide check: no CURRENT guide covers the claim grammar beyond kb `distillation.md`,
and the change forces no new comprehension model, so no guide is due.

**2026-10-23 — design review round 1: FAIL, revised.** Independent subagent (rung 1,
deep): 2 BLOCK, 9 WARN, 3 CANNOT VERIFY.
- BLOCK 1 is fixed: `validate` does not reach the claim checks, and the path is now
  stated per lens.
- BLOCK 2 is fixed: the kb README and `skill_family_agent_workflows.md` are added,
  and the code README is checked and needs no change.
- WARN 1: export now drops markers (FS9, D8; `kb_bundle_write` impacted). I took that
  over the importer's refusal (no export code, but the closure's "passes its own
  checks" promise broken) and over a warning at export (verbatim kept, same broken
  promise). T2 is softened.
- WARN 2: asked; the owner scoped Hybrid out (R7).
- WARN 3: the r33 amendment is named in the Impact.
- WARN 4: the 535 B always-read cost is stated.
- WARN 5: "no reverse direction" is in D1 and FS7.
- WARN 6: supersession is FS8 plus D7, with the predecessor id accepted.
- WARN 7: the Practitioner is dropped, and UC5 serves the Team lead.
- WARN 8: the r33 conditions are cited, not restated.
- WARN 9: the order is fixed (re-review, then the cost confirmation).
- CANNOT VERIFY 1: the deltas are now verbatim in `deltas.py`.
- Target probe gains B6 (export drop). Next: scoped re-review.

**2026-10-23 — design review round 2: FAIL, revised.** Same reviewer, scoped: every
round-1 finding ADDRESSED; new findings from the corrections:
- N1 BLOCK, fixed: the export report counted dropped markers, a count of claims by
  the mark (r33, FS7). Export now prints one line without a number (FS9, D8 135 B,
  total 1,820 B).
- N2: the workflows-doc row now covers the code-lens duties and §"Quando convivono".
- N3: FS8 is acceptance-checked by the battery only; probe B5 now also reads
  `reconciliation.md` and `portability.md`.
- N4: the r33 amendment cites the figures as pending, not as an R8 that does not
  exist.
- N5, kept: the RED test class in `test_claim_ledger.py` was written while round 1 ran.
  It is test code only, uncommitted, and no production code exists. Three of its eight
  cases already pass (today's grammar refuses those cells); they stay as regression
  guards, and the five red ones drive the change.
Next: round 3, the last before the cap.

**2026-10-23 — design PASS, cost confirmed, implementation started.** Round 3 PASS
(REVIEW_LOG). Owner accepted 1,820 B (R8). Status IN_PROGRESS.

**2026-10-23 — implemented; closure review round 1: FAIL, fixed.** RED then GREEN in
`knowledge.py` (copied ×3, manifest updated), D1–D8 applied verbatim from
`deltas.py`, READMEs, workflows doc, Component Map, r33 amendment, CHANGELOG ×4, E2E.
Batteries ×4 green, probe B1–B6 green. Closure review (fresh subagent, deep): 1 BLOCK,
6 WARN. B1: export kept the marker on a row with no trailing pipe (legal for the
parser); fixed by locating the cell from the left, with a test. W1: probe A2 now tests
two ordinary relations, so it flips red as designed. W2: r33's deciding line names the
amended ceremony. W3: the export line reads as the Interface Contract. W4: FS5 and the
CHANGELOGs name `; ` as canonical, with a bare `;` tolerated. W5: the back-citation
matches the id as a whole hex token, with a test. W6: these records. Next: scoped
re-review, then MERGE_REVIEW, `index`, `mark`.

**2026-10-23 — closed.** Scoped closure re-review PASS (REVIEW_LOG). Batteries ×4 green
(code 421, kb 618, mkt 423, course 416), probe B1–B6 green. MERGE_REVIEW written,
handoff removed, areas marked. Hybrid follow-up stays open (R7). Awaiting the owner's
merge decision; nothing pushed, tagged or released.
