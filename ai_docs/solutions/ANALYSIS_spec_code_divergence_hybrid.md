---
id: F-081
feature: Spec/code divergence marker in Hybrid projects
status: IN_PROGRESS
level: L3
start_date: 2026-10-23
domain: code
---
# Feature Analysis: Spec/code divergence marker in Hybrid projects

## Objective

F-080 gave a specification claim in `topics/` a checked pointer,
`not-yet-honored-by -> ANALYSIS_<name>`, to the Standalone ANALYSIS that records a
deferred fix. In a Hybrid project the deferral lives in a devPNT E-ISP or E-TDD and
there is no `ANALYSIS_*` file, so the duty could not be met and the owner scoped it
out ("Standalone now, Hybrid later", `REQUEST_spec_code_divergence.md` R7). This unit
closes that gap. The marker may name `SHADOW_<doc_key>`, and `check` resolves the
newest `solutions/SHADOW_<doc_key>_vX.Y.md` and requires the claim id in it. Request:
`audit/requests/REQUEST_spec_code_divergence_hybrid.md` R1. Admission: `vision/rulings.md`
r35 (R2).

## Feature Vision

- **Benefit** — the same as F-080 (Vision v9 APPROVED, Goal "keep understanding
  durable … nothing load-bearing lives only in a transcript"; Team-lead "one source of
  truth"), now reaching the projects that run devPNT.
- **Actors** — from the project Vision: *Adopter evaluating the paid layer* (adding
  devPNT no longer drops the marker duty F-080 owed them), *Team lead needing
  governance* and *Solo developer using an AI agent*.
- **Non-goals** — the r33 conditions bind unchanged and are not restated (rulings r33,
  carried by r35). This unit adds three of its own:
  - No call to devPNT: `check` reads files only, and devPNT's own doctrine (generated
    outside this repository) is not edited here.
  - No mode flag. `check` accepts both target kinds with or without `--hybrid`, because
    the mode belongs to the unit of change, not to the project (`hybrid.md` ownership
    matrix, "mode is per unit of change").
  - No change to export, supersession or recall semantics: a SHADOW target is one more
    spelling of the same marker.
- **Success signals** — `harness_spec_code_divergence_hybrid/probe.py` B1–B7 green and
  baseline A1/A3 red after the change (FS1–FS6 below; FS7–FS8 by invariants and B7).

## Use Cases / User Needs

- **UC1 (Adopter / Team lead)** — a Hybrid L3 finds code contradicting a KB spec claim
  and defers the fix in its E-ISP or E-TDD. It marks the claim
  `not-yet-honored-by -> SHADOW_<doc_key>` and the governed artifact cites the claim id;
  the regenerated shadow carries it. *Benefit: one source of truth.*
- **UC2 (Team lead)** — `check` refuses the marker when no shadow of that doc_key exists
  or the newest one does not cite the claim. *Benefit: one source of truth, mechanically
  held.*
- **UC3 (Solo developer)** — asks the agent about the behavior; the answer says the spec
  requires it and the code does not yet do it, naming the marker's target. *Benefit:
  durable understanding.*
- **UC4 (Team lead)** — a later design version drops the deferral (the fix landed or
  the deferral moved): the newest shadow no longer cites the id and `check` says so,
  until the marker is removed or retargeted. *Benefit: one source of truth over time.*

Grounding: EXISTS — claim, claim id, `about` cell, the reserved predicate, `check`,
export, Topic Recall, shadow `SHADOW_[doc_key]_vX.Y.md`, E-ISP, E-TDD, doc_key
(`hybrid.md` §Shadow discipline, kb `distillation.md` §2). NEW — the target form
`SHADOW_<doc_key>` (unversioned). No METAPHOR names.

## Functional Spec

- **FS1 Target forms.** The reserved predicate takes `ANALYSIS_<name>` (unchanged) or
  `SHADOW_<doc_key>`, where `<doc_key>` uses letters, digits, `_` and `-`. Any other
  target, including a versioned `SHADOW_<doc_key>_vX.Y`, is an error, as a malformed
  `about` part is today. An ordinary relation pointing at a `SHADOW_` name stays an
  error. A target ending in `_v<N>` with no dot is a legal key of its own, so it is not
  refused here; it meets FS3 unless that key has shadows.
- **FS2 Resolution.** A `SHADOW_<doc_key>` target resolves to the file
  `solutions/SHADOW_<doc_key>_v<N>[.<N>…].md` with the highest version, compared
  number by number: v1.10 is above v1.9, and v1.0 above v1. Only an exact `<doc_key>`
  matches: `SHADOW_<doc_key>_extra_v1.0.md` is another key. A file of that key whose
  name does not end in such a version (`SHADOW_<doc_key>.md`, `…_v1.2a.md`) is not a
  shadow under `hybrid.md`'s name rule and is not read.
- **FS3 Dangling marker.** No matching shadow is an error naming
  `solutions/SHADOW_<doc_key>_v<X.Y>.md` and telling the user to export the shadow from
  the accepted devPNT version, or to remove the marker if it did not come from this
  project. When files of that key exist under another name, the error names one, so
  the user sees why it was not read. A stray is a file of the same exact key with a
  non-version suffix, never a longer key.
- **FS4 One-sided marker.** The resolved shadow must cite the claim id, or the id of a
  row this claim succeeds (F-080 FS8). Otherwise the error names the claim id and that
  exact file. Older versions are not read: the current design is what must still record
  the deferral (UC4).
- **FS5 Mode independence.** `check` applies FS1–FS4 with and without `--hybrid`.
- **FS6 Unchanged.** Export drops `SHADOW_` markers exactly as `ANALYSIS_` ones
  (F-080 FS9); supersession, removal (L2/L3, L1 exempt), coexistence in one cell and the
  no-selection rule (F-080 FS5–FS8) apply to both target forms.
- **FS7 Recall.** An answer citing a marked claim names the marker's target, whichever
  form it has; a marked claim is never cited as current behavior (F-080 FS1, widened).
- **FS8 Marking on deferral (Hybrid).** A Hybrid L3 that defers fixing code which
  contradicts a KB claim writes `not-yet-honored-by -> SHADOW_<doc_key>` on the claim,
  cites the claim id in that E-ISP or E-TDD, and exports its shadow. The duty is
  doctrinal: a doc_key carries no type, so `check` cannot tell an E-TDD shadow from a
  D-UC or ADR one (residual, stated).

Acceptance: FS1–FS4 and FS6's export drop are checked by the battery and the probe
(B1–B6); FS5 by the Test Strategy's `check --hybrid` case; FS7 and FS8 by doctrine
invariants and B7.

## Interface Contract

Fires: the change modifies surfaces an actor acts on or perceives — the claim's `about`
cell, the `check` messages, and the doctrine the agent reads (code Write Triggers row,
kb grammar). Export output and recall answers keep their F-080 form.

- **Actors and surfaces.** The agent edits the `about` cell (idiom: F-080's
  `<predicate> -> <target>` parts joined by `; `). The agent or a person runs
  `sdlc_check.py check` (idiom: one finding line per defect, exit 1 on error). The
  shadow is written by the Hybrid shadow discipline (`hybrid.md`), never by hand.
- **Flow (UC1/UC2).** The agent writes the marker and puts the claim id in the governed
  E-ISP/E-TDD → the accepted version is exported as a shadow → `check` → the claim
  checks (reached from every lens's `check` exactly as in F-080) resolve the target to
  the newest shadow of its key and look for the id. One error per defect, or nothing.
- **Flow (UC3).** Topic Recall cites the claim as required and not yet done, naming the
  target the marker carries.
- **Feedback.** Silence when clean; one error line naming the claim location, the
  expected or resolved file and the remedy (FS3/FS4).
- **New idiom.** None: the target is a second spelling inside F-080's grammar, and the
  file it names is `hybrid.md`'s existing shadow name.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| parse the reserved predicate's target | INADEQUATE | `knowledge.KB_NOT_HONORED_RE` | probe A1: `SHADOW_` target refused |
| resolve a target to a file under the docs root | INADEQUATE | `knowledge.kb_check_marks` resolves `solutions/<target>.md` only | re-read; no version selection exists |
| pick the newest shadow of a doc_key | MISSING | — | grep `SHADOW_` over `scripts/*.py`: only `sdlc_core` `gate --hybrid` checks presence of any E-TDD shadow, no version ordering |
| drop the marker on export | EXISTS | `knowledge.kb_drop_marks` keys on `KB_NOT_HONORED_RE` | widening the regex widens the drop (probe B6) |
| run claim checks from every lens's `check` | EXISTS | F-080 path, unchanged | F-080 probe A3 |
| tell an L3 where to cite in Hybrid | INADEQUATE | code SKILL.md Write Triggers row says "(Standalone)" | probe A3 |

The MISSING capability is "the newest shadow of a doc_key", a Hybrid capability with
no tie to claims. It goes where shadow recognition already lives, `sdlc_core`
(`is_shadow`, `has_etdd_shadow`): `newest_shadow(solutions_dir, doc_key) -> Path |
None`. Its contract: exact key, highest numeric version, names outside `hybrid.md`'s
rule ignored (FS2). It never names the mark, so the F-080 invariant that `sdlc_core`
never mentions it holds, and a later consumer (the Hybrid gate choosing the newest
E-TDD, a merge brief citing it) reuses it. `kb_check_marks` is its first caller.

## Impact

Blast radius (symbol identity, `grep` over `skills/` and `distributions/`, the
symbol-graph tool being devPNT's and devPNT off):
- `knowledge.KB_NOT_HONORED_RE` — readers: `kb_check_claims` (grammar), `kb_drop_marks`
  (export), both in `knowledge.py`; tests read the predicate string, not the regex.
- `knowledge.kb_check_marks` — one caller, `kb_check_claims`.
- `KB_NOT_HONORED` / `not-yet-honored` users in `knowledge.py`:
  `kb_bundle_write`, `kb_check_claims`, `kb_check_marks`, `kb_cmd_export`,
  `kb_drop_marks` — the FS7 invariant list, unchanged (the new resolver reads no
  predicate).
- `sdlc_core.newest_shadow` is new; its sibling `has_etdd_shadow` keeps its one caller
  (`gate --hybrid`) and is not changed.
- No other code parses `about`; `docs_site.py` copies it as text (F-080 Impact).

| File | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/scripts/knowledge.py` (shared ×4) | `KB_NOT_HONORED_RE` accepts `(ANALYSIS\|SHADOW)_[A-Za-z0-9_-]+`; the grammar error names both forms; `kb_check_marks` resolves a `SHADOW_` target through `sdlc_core.newest_shadow` and words FS3 per form, naming a stray file of the key | FS1–FS5 |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` (shared ×4) | new `newest_shadow(solutions_dir, doc_key)` and `stray_shadow(solutions_dir, doc_key)`, one name rule (`_shadow_version`) | FS2, FS3, Ledger |
| `distributions/*/scripts/knowledge.py`, `sdlc_core.py` (×3 each) | verbatim copy | drift guard |
| `scripts/shared_manifest.json` (×4) | `shared_files.py --update` | drift guard |
| `skills/agentic-sdlc-skill/SKILL.md` | D1: Write Triggers row | UC1 |
| `distributions/kb-agentic-skill/.../distillation.md` | D2: §2 reserved-predicate sentence | FS1–FS4 |
| `distributions/kb-agentic-skill/.../templates.md` | D3: claim-table `about` line | FS1 |
| `distributions/kb-agentic-skill/.../SKILL.md` | D4: Topic Recall sentence names the target, not one form | FS7 |
| `memory.md` (shared ×4) | D5: "naming its analysis" becomes "naming its target" | FS7 |
| `distributions/kb-agentic-skill/.../reconciliation.md` | D6: "the analysis or shadow citing" | FS6 |
| `distributions/kb-agentic-skill/README.md` | Extraction step (line 29) names the Hybrid target; Recall step (line 39) "naming the analysis" becomes "naming its target" | audit-plan duty; FS7 |
| `ai_docs/strategic/skill_family_agent_workflows.md` | the two F-080 paragraphs lose "solo Standalone" and name the Hybrid target | audit-plan duty |
| `ai_docs/strategic/architecture.md` | Component Map "Claim ledger" row: the second target form and the resolver | contract changed |
| `kb .../test_claim_ledger.py` | new test class (FS1–FS5) | RED |
| (same kb `test_claim_ledger.py`) | `newest_shadow` cases: `sdlc_core` is byte-identical ×4 under the drift guard, so one battery covers it, as for the F-080 claim checks | RED |
| `kb .../test_kb_recall.py` | FS1 anchor follows D4 | invariant |
| `skills/.../test_skill_invariants.py` (shared ×4) | row anchors: `SHADOW_<doc_key>` replaces "(Standalone)" | invariant |
| `ai_docs/vision/rulings.md` | r35 row; r33 basis gains "widened to Hybrid by r35" | ledger |
| `CHANGELOG.md` + three distribution CHANGELOGs | `[Unreleased]` entry | release notes |
| `hybrid.md` | none (R5 estimated one line; dropped — the Write Triggers row is read in every mode, and `hybrid.md` carries a moved-block digest a one-line edit would re-stamp) | lower cost than accepted |
| `portability.md`, code `templates.md` | none: `portability.md` names the marker only; code `templates.md` speaks of the ANALYSIS Diary, which Hybrid does not have | checked |
| request record, this ANALYSIS, harness, E2E, MERGE_REVIEW, HANDOFF, indexes | records | closure |

**Ceremony cost (r35, R5; confirmed by the owner, R6).** The deltas are
written verbatim as (old, new) pairs in `harness_spec_code_divergence_hybrid/deltas.py`,
which prints the UTF-8 byte change of each:

| Delta | Where | Bytes | Read |
|---|---|---|---|
| D1 | code `SKILL.md` Write Triggers row | +70 | every code session |
| D2 | kb `distillation.md` §2 | +116 | when distilling |
| D3 | kb `templates.md` | +29 | on trigger |
| D4 | kb `SKILL.md` §Topic Recall | −22 | every kb session |
| D5 | shared `memory.md` (×4 identical) | −2 | every session, all lenses (orientation) |
| D6 | kb `reconciliation.md` §3 | +10 | on trigger |

Net +201 B against the ≈ +300 B estimated in R5. The `hybrid.md` line R5 priced is
dropped (its duty, export the shadow, now rides in D1), and D4 shrinks. Read in every
session: +68 B in the code lens, −24 B in kb, −2 B in mkt and course. READMEs, the workflows doc and CHANGELOGs are not loaded by agents.

Steps: L1/L2 unchanged from F-080. Per deferring Hybrid L3: one claim cell, the claim
id in the governed artifact, which the shadow carries once regenerated (the E-TDD
shadow is already due before implementation, `hybrid.md`; an E-ISP-only deferral
exports one more shadow). Per later design version: none while it still records the
deferral.

## Security and Threat Model

Surfaces: filesystem (the validator lists `solutions/` and opens a file chosen from a
cell) and external input (an imported or hand-copied topic).

- **T1 Path traversal through the target.** The key grammar has no `/`, `\` or `.`;
  the resolver lists only `solutions/` (itself through `sdlc_core.confine_under`) and
  matches names against an anchored regex built from the escaped key, then confines
  the chosen file again. Mitigated, with a test.
- **T2 Foreign marker.** Unchanged from F-080: export drops both forms; a marker that
  arrives another way names a shadow absent here and FS3 refuses it. Residual as in
  F-080 (a stub shadow citing the id silences FS3; a closure review sees it).
- **T3 Laundering into a work queue.** The resolver returns one file for one target and
  is called only from the claim checks; it reads no predicate and builds no index of
  shadows by mark. The F-080 FS7 invariant stays green. Mitigated.
- **T4 Version spoofing.** A hand-made `SHADOW_<key>_v99.0.md` would become the newest
  and decide FS4. Shadows are generated and "do not edit by hand" (`hybrid.md`); the
  DB wins on divergence. Residual, stated; not prevented mechanically.
- **T5 Cost.** One directory listing per distinct SHADOW target per `check`, memoised.
- **T6 Stale shadow.** `check` reads the newest *exported* shadow, never the DB. If the
  DB holds a newer version without the deferral and the shadow was not refreshed,
  `check` passes on the old one until the refresh `hybrid.md` requires at closure.
  Follows from the "no call to devPNT" Non-goal. Residual, stated.
- **T7 Type of the shadowed document.** Any doc_key's shadow satisfies `check`, so a
  marker could name a D-UC or ADR shadow that cites the id. FS8 binds the E-ISP/E-TDD
  doctrinally; a closure review sees a wrong target. Residual, stated.

## Action Plan

- [x] Design review gate (`review.md` moment 1): PASS (8 WARN) → PASS.
- [x] Owner confirms the ceremony figures: R6 «Accept 201 B».
- [x] RED: kb `test_claim_ledger.py` class; invariant anchors.
- [x] GREEN: `sdlc_core.newest_shadow`; `knowledge.py` regex and `kb_check_marks`; both copied ×3; manifest.
- [x] D1–D6; kb README; workflows doc; Component Map; rulings r35; CHANGELOG ×4.
- [ ] Probe B1–B7 green, baseline A1/A3 red; four batteries; E2E_TEST; closure
      review; MERGE_REVIEW; `index`; `check` CLEAN; `mark`.

## Test Strategy

- **Unit (kb `test_claim_ledger.py`, new class):** cited newest shadow clean; no shadow
  is an error naming the pattern; v1.10 beats v1.9 numerically and its silence is an
  error naming it; a longer key's shadow does not resolve; a versioned target and a
  traversal-shaped key are refused by grammar; a relation to a `SHADOW_` name is
  refused; a relation and a `SHADOW_` marker in one cell are accepted by `check`; a
  successor satisfied by the predecessor's id in the shadow; FS3's remedy names the
  export and a stray file of the key; export drops a `SHADOW_` marker; `sdlc_check.py
  check --hybrid` reports the same finding as without the flag (FS5).
- **Unit (`sdlc_core.newest_shadow`):** numeric order (v1.10 > v1.9, v1.0 > v1); exact
  key; non-version names ignored; missing directory returns None.
- **Invariants:** code row anchors (`SHADOW_<doc_key>`, "export", no "(Standalone)");
  kb FS1 anchor follows D4; `memory.md` anchor follows D5; F-080 FS7 list unchanged.
- **Probe:** B1–B7 green; `--baseline` A1/A3 red, A2 green.
- **Batteries:** code, kb, mkt, course; drift guard.

## Diary / Current State

**2026-10-23 — admission and design.** F-080 merged to local main (b7c4795); branch
fast-forwarded. Router: `GUIDE_skill_family_changes.md` (shared copies count once;
L3). Guide check: no CURRENT guide covers the claim grammar beyond kb `distillation.md`,
and the change forces no new comprehension model. Elicitation: four questions asked
together (admission, target grammar, shadow presence, cost), answered R2–R5. Probe
written red-first: baseline A1–A3 green; target B1–B4, B6, B7 red, B5 green today (the
grammar already refuses a dotted target; kept as a regression guard).

**2026-10-23 — design review round 1: PASS with 8 WARN, 2 CANNOT VERIFY, answered.**
Independent subagent (rung 1, deep). PASS is provisional until a scoped re-review of
these corrections passes.
- W1: the newest-shadow resolver moves to `sdlc_core.newest_shadow`, beside
  `is_shadow` and `has_etdd_shadow`; `kb_check_marks` calls it.
- W2: D1 now says to export the shadow (+70 B instead of +80), so an E-ISP-only
  deferral is told; the dropped `hybrid.md` line is named for the owner's confirmation.
- W3: FS7 (recall names the target) and FS8 (the Hybrid L3 duty) added.
- W4: component and mechanism removed from the FS acceptance line and the contract
  flow.
- W5: FS1–FS3 state the `_v<N>` key, the v1 / v1.0 order and stray names; FS3 names a
  stray file of the key.
- W6: T6 stale-shadow residual.
- W7: `memory.md` (D5), `reconciliation.md` (D6) and the kb README Recall step are now
  in the Impact; net +201 B.
- W8: FS8 and T7 state the doctrinal-only restriction to E-ISP/E-TDD.
- Minor: the cost heading reads as pending; tests for the remedy wording and the
  check-side coexistence added.
- CV1 resolved by observation: the shadow names under the local projects (about 50,
  devPNT-generated) use letters, digits, `_` and `-` only; a node prefix appears as
  `M153_`, never with a dot. Several legacy files lack the `_vX.Y` suffix, which is
  why FS3 names a stray file.
- CV2 does not limit the design (FS4 reads the newest whether or not older ones stay).

**2026-10-23 — scoped re-review round 2: PASS.** All round-1 findings ADDRESSED. New:
N1 Action Plan behind the Impact (fixed), N2 Success-signals FS count (fixed), N3 the
stray hint is exact-key only (stated in FS3), N4 `memory.md` is read every session in
every lens (cost table corrected: +68 B code, −24 B kb, −2 B mkt and course).

**2026-10-23 — implemented.** Owner accepted 201 B (R6); status IN_PROGRESS. RED: 16
tests in kb `test_claim_ledger.py`, 10 red, 6 green regression guards. GREEN:
`sdlc_core.newest_shadow`, `knowledge.KB_NOT_HONORED_RE` and `kb_check_marks` (with a
private `_kb_mark_target` that reads no predicate), copied ×3, manifest updated. D1–D6
applied verbatim from `deltas.py`; kb README, workflows doc, Component Map, CHANGELOG ×4.
Probe B1–B7 green; baseline A1/A3 red, A2 green (the flip). Batteries after `index`:
code 458, kb 669, mkt 460, course 453, all OK. Next: E2E (written), closure review.

**2026-10-23 — closure review round 1: PASS with 5 WARN, answered.** Fresh subagent
(rung 1, deep) re-ran probe, batteries ×4, drift guard and the delta comparison.
- W1: `check` was also NOT CLEAN on `memory/INDEX.md`; closure runs `index` before
  `mark` and `check`.
- W2: the r35 row records R6 and the confirmed figures.
- W3: the handoff is removed at closure.
- W4: any part whose predicate is `not-yet-honored-by` now gets the marker message, which
  names `SHADOW_<doc_key>, unversioned`; the FS4 message says "analysis or design". Tests.
- W5: stray detection moves to `sdlc_core.stray_shadow`, sharing the one name rule with
  `newest_shadow`, so a correctly versioned file is never reported as a stray. Test.
- CV1: the E2E Result fields are the tester's, after merge (S6 needs a live agent).
  CV2: symlink escape untestable on this host; `confine_under` still guards it.
