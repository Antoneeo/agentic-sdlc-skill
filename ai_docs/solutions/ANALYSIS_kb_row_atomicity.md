---
description: F-047 - kb row atomicity. A claim row atomic as provenance can be plural as meaning; faithful citation then asserts what the source does not. Fix across three layers - extraction doctrine (atomicity + narrow locator), repair move (split-as-supersession), use-side rail (citation-scope test) - plus the collision message de-trapped and a fallible plurality note.
status: COMPLETED
end_date: 2026-09-08
feature: F-047
id: F-047
start_date: 2026-09-08
level: L3
branch: main
---
# ANALYSIS: kb Row Atomicity (F-047)

**Level: L3 · lens: kb · router: no match** (catalogue: GUIDE_release only).
Elicitation: skip path — the spec is the practitioner's field report (103-artifact corpus, 1785 rows, 4 defects reaching committed documents past two fresh-context reviews) plus the owner's approval of the assessed fix set (a–e + f). Probes: `harness_kb_row_atomicity/probe.py` (ships with this analysis).

## Objective

Give the kb lens the concept it lacks — the assertion as the unit of the ROW, not only of the extraction pass — at the three layers where its absence produced field defects: extraction (bundled rows are legal), repair (the collision remedy recommends manufacturing bundles; splitting is undescribed), and use (a faithful citation is never scope-tested).

## Vision Alignment

The kb north star (distillation.md): *not one assertion the source makes may be lost, and not one it does not make may appear*. A bundled row violates the second half at every out-of-scope citation (the reader concludes app-level 2FA that the source asserted at the door) and pushes writers into violating the first half (silent omission of the off-topic part). The fix operationalizes the north star at row granularity; no new capability, no new artifact class.

## Use Cases / User Needs

- **UC1 — the extractor** meets a reviewer comment that asserts several facts about several subjects under one heading. Today: one span → one legal row. After: doctrine names the case; one row per assertion, narrowest supporting span each.
- **UC2 — the agent hitting an id collision.** Today the error (and distillation.md §2) says "widen … or merge" — merging distinct assertions manufactures the bundle. After: narrow-first guidance with the merge condition stated (only when genuinely ONE assertion), and the nudge-vs-narrow distinction explicit.
- **UC3 — the maintainer of a corpus with existing bundled rows** needs a legal repair. Today reconciliation.md has no split move. After: split = supersession 1→N (`SUPERSEDED <id1>, <id2>` — grammar already accepts lists, probe P4), cascade reaches every citer.
- **UC4 — the answerer citing a row** (Topic Recall). Today fidelity-to-the-row is the only test. After: scope test — every part of the cited row must belong to the question; cite the part and say where the rest belongs.

Product-name buckets: claims table / id function / collision check / notes tier / SUPERSEDED-list grammar / stale cascade / anti-echo re-touch rule — all EXIST (probed, see Impact). NEW: the atomicity block (distillation.md §3), the split move (reconciliation.md), the citation-scope bullet (kb SKILL.md §Topic Recall), the plurality `[note]` heuristic (kb_check_claims). Traces: UC1–UC4 → both halves of the north star; UC2 additionally → distillation.md's own anti-distortion rule (evidence never bent to satisfy a hash).

## Functional Spec

Observable behavior changes (validator output):
1. **Collision error remedy text** (`kb_check_claims`, same-span branch): replaces "Widen one locator … or merge the two rows" with: narrow each locator to the sub-span carrying its own assertion (ids become distinct by construction); merge ONLY if the two rows state the same single assertion; merging distinct assertions trades a mechanical error for a semantic one no check can see. Qty-editing stays forbidden. Acceptance: probe P1 green; message pinned by test.
2. **State-grammar error message** (:572-573): documents the list form — `'SUPERSEDED <id>[,..]'` — matching the regex that already accepts it (:570) and the split move that now uses it. Acceptance: message pinned by test.
3. **Plurality note** (new, notes tier — never an error/warning, `graph`/`check` exit code unchanged): a row whose claim text matches bundling heuristics (e.g. `, and that `, `; `, `, while `, ` and also `) gets one `[note]` naming the row and pointing at distillation.md §3 atomicity. Explicitly fallible: heuristics cannot prove plurality. Acceptance: probe P3 green (motivating-row replay flags), P2 invariant (collision error still fires), no exit-code change on note-only corpora, golden baselines unaffected (fixtures carry no bundled text — verified at implementation).
Non-changes: id function untouched; locator grammar untouched; state-grammar REGEX untouched (:570 already accepts lists — only its error message and the doctrine sites now say so).

## Interface Contract

Not fired as a new surface: both changes reshape existing check output on existing flows (agent runs `check`/`graph`, reads findings); no new command, no new interaction idiom. The message-content contract rides the Functional Spec.

## Capability Ledger

All capabilities EXIST — no component built. Probed: notes tier flows `kb_check_claims` → `kb_cmd_graph` `[note]` print (sdlc_check.py:1522,1529-1530); collision branch at :536-544; `SUPERSEDED` list grammar at :570 (`[0-9a-f, ]+`, comma-split targets); stale cascade for fallen ids (reconciliation.md §2.3); anti-echo sibling slot (kb SKILL.md:180). Sub-line precision confirmed AVAILABLE today: `p=<n>@<a>-<b>` addresses character offsets of the stored bytes, and `kb_check_locator` (:619-620) uses the target itself when its suffix is `.txt` — a form-feed-free file is one page, so `p=1@a-b` narrows below a line on the same stored file with no re-extraction. Re-extraction is needed only for a source with no character-addressable stored form; `L<a>-<b>` remains the floor only for rows one chooses not to re-cite.

## Impact

| Path (kb distribution) | Change | What |
|---|---|---|
| `distillation.md` | MODIFY | §2 id bullet: remedy rewritten (narrow-first, merge-condition, narrow≠nudge distinction, id re-mint note). §2 state bullet (:120): `SUPERSEDED <id>[,..]`. §3: atomicity block — one row asserts one thing; reviewer-comment case named; narrowest-span corollary; sub-line path (`p=1@a-b` on the stored `.txt` today; re-extraction only when no character-addressable stored form exists) |
| `templates.md` (kb) | MODIFY | claims-table state cell (:634): `SUPERSEDED <id>[,..]` — the authoring reference must agree with the grammar the split move uses |
| `reconciliation.md` | MODIFY | new short section: splitting a bundled row = supersession 1→N with narrowed locators, cascade runs; one state-machine event row |
| `SKILL.md` (kb) | MODIFY | §Topic Recall: citation-scope bullet, sibling to anti-echo — scope, not fidelity, is the test; cite the part and say where the rest belongs (never silently drop it) |
| `scripts/sdlc_check.py` (kb) | MODIFY | collision message text; state-grammar error message (:572-573) `'SUPERSEDED <id>[,..]'`; plurality-note heuristic in `kb_check_claims` (notes list) |
| `scripts/test_claim_ledger.py` | MODIFY | pin new collision remedy + state-grammar message; new tests: plurality note fires on bundled text, silent on atomic rows, never alters exit code |
| `ai_docs/solutions/harness_kb_row_atomicity/probe.py` (this repo) | ADD | probes P1–P4, re-runnable |

Blast radius: the collision message string has NO consumer beyond humans/agents — grep across the kb distribution found only distillation.md:100 (rewritten here) and the source itself; no test pins the old wording. The state grammar is documented in exactly three sites (templates.md:634, distillation.md:120, the validator message :572-573) — all in the table above, so machine and doctrine move together. `kb_check_claims` signature unchanged (still returns errors, warnings, notes). No impacted file is in the spine manifest: kb `sdlc_check.py` sits in `NOT_SHARED_ON_PURPOSE` (shared_files.py:81), `reconciliation.md`/`distillation.md`/`templates.md`/kb `SKILL.md` are kb-local — no port ×3. Code-lens `review.md`/SKILL.md untouched.

## Security and Threat Model

No new input surface. The plurality heuristic runs simple literal substring checks on claim text already parsed by the validator — no regex on hostile input beyond what exists, no ReDoS shape. Notes never alter exit codes, so CI behavior cannot be weaponized or broken by claim-text content.

## Action Plan

1. Harness RED (P1 red on both remedy sites, P3 red — note absent; P2, P4 green as invariants).
2. Design review (moment 1, rung 1 — fresh subagent), severity contract stated, pre-audit run.
3. Implement doctrine (3 files), checker (message + note), tests (RED→GREEN for new pins).
4. Harness GREEN full; kb battery green; drift guard green (no spine file touched — proves confinement).
5. Closure: REVIEW_LOG row, registration, indexes, commit. Release deferred to owner.

## Test Strategy

Harness P1–P4 (doctrine + replay of the motivating bundled row). kb battery: existing `test_claim_ledger.py` suite + new pins (collision remedy text; plurality note fires/does-not-fire/exit-code-neutral). Full kb `unittest discover` + code/mkt batteries (confinement: their green proves no shared file moved). Golden baselines must stay byte-identical.

## Diary

- **2026-09-10 — the use-side rail was measured, and the result is NULL.** `SPIKE_citation_scope_benefit.md` replayed the field's own bundled row, six blind runs, control taken from the commit before this unit: 3/3 correct in BOTH arms on the pre-registered criterion. The rail bought nothing measurable here, because the control was already at ceiling — the row names its off-topic subject explicitly ("the *calling station* already offers…"), so avoiding the error needs attention, not a rule. The three harder defect kinds the field report lists (subject ambiguity, wrong actor, silent omission) are not represented by this row and remain untested. Recorded per this unit's own north star: an unfalsifiable claim is the defect, and "no measured benefit on the one case we could test" is the honest state of the citation-scope rule.

- **2026-09-08 (closure) — implemented, reviewed, green.** Design review FAIL → PASS in 2 rounds (BLOCK: state grammar documented singular in three sites — templates.md joined the Impact; residual found overstated: `p=1@a-b` narrows below a line today). Closure review PASS in 1 round (0 BLOCK; conformance proven on the exact Impact set, confinement by sibling batteries). Harness 7/7 green; batteries kb 376 / code 191 / mkt 209 OK. ADR `row_atomicity_by_doctrine`. Family workflows doc gained the atomicity clause and the split outcome. Release deferred to owner.
- **2026-09-08 — opened.** Field report verified claim-by-claim against source (all confirmed; external REVIEW_LOG datum CANNOT VERIFY from here). Assessment approved by owner: fixes a–e + (f) the split move; locator-grammar extension explicitly deferred to its own unit (id-stability blast radius). Discovery during probing: the widen-or-merge trap lives in TWO places (distillation.md §2 prose AND the checker message) — both rewritten in this unit; and `SUPERSEDED` already accepts multi-id lists, so the split move needs zero parser change.
