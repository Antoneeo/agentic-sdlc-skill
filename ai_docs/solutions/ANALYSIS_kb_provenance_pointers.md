---
id: F-035
feature: kb field report 2 — provenance below GIVEN, unverified original_path, a duplicate-id message that names the wrong cause
status: COMPLETED
level: L3
start_date: 2026-08-25
end_date: 2026-08-25
---
# Feature Analysis: provenance chains and pointer integrity

## Objective

Second field report from the same practitioner who produced F-029, after further real
use of `kb-agentic` on a document corpus. Three defects, all **reproduced against the
shipped source before being accepted**; one report item (output noise) is deferred by
the reporter's own ordering and recorded here so it is not lost.

The three share one subject: **the corpus letter promises that every provenance is a
real file, and two of the three mechanisms that should enforce that promise do not
run.** One is a one-line type bug that closes three of the five provenance classes; one
is a field nothing ever reads; the third is a correct check whose message sends the
reader hunting for a defect that is not there.

- **A — `prov:` below `GIVEN` is structurally impossible for any claim citing
  `corpus/given/`.** `_note_frontmatter` (`sdlc_check.py:274-278`) reads frontmatter
  from the cited file. A `corpus/notes/x.md` carries frontmatter and resolves. A
  `corpus/given/x.txt` **is** a file — so the helper does not return `None`, the branch
  that means "unresolvable, already reported" — but it has no frontmatter, so it
  returns `{}`. At `:325-341`, `{} is not None`, so `meta.get("derived_from")` is
  `None` and the error fires unconditionally. The artifact's frontmatter lives in its
  `.meta.md` sidecar, which the helper never opens. Net effect: `DERIVED`, `RULING`
  and `IMPORTED` are unreachable on a `given/` artifact, and every such claim is
  forced to `GIVEN` whatever the real extraction chain was.
  **The reporter's count is one too high, and the correction matters.** `ELICITED` is
  named in the same `elif prov in (...)` tuple but has no required-field branch below
  it (`:328-341` runs DERIVED / RULING / IMPORTED and stops), so it falls through and
  never errors — on a `given/` artifact or anywhere else. Three classes are blocked,
  not four. `ELICITED`'s silence is a **separate** pre-existing gap: the class is
  accepted with nothing required of it. Named here, deliberately not fixed in this
  unit — it is a new gate, not a repair, and it belongs to its own ceremony budget.
- **A' — the consequence the reporter hit, which A alone does not close.** Three rows
  whose evidence was a transcription of an image were filed `GIVEN`, with the weak
  chain declared only in the sidecar's prose. Nothing distinguishes them from a row
  resting on a deterministic text layer. Prose is not a check; this is the laundering
  the overlay exists to prevent, entering through the door A jams shut.
- **B — `original_path:` is never verified.** Zero occurrences of `original_path` or
  `original_sha256` in `sdlc_check.py` and `sdlc_core.py`. `kb_corpus_check`
  (`:867-916`) verifies the extraction's `sha256:`, `supersedes:` and coverage, and
  that the `given/` artifact itself exists (`:881`) — never the pointer to the paper.
  The reporter moved a folder of 12 originals; 16 sidecars went dangling and the
  validator stayed green. `distillation.md:52` declares loudly that
  `original_sha256` is not checked, and the reason given — *we do not hold it* — is
  correct and **does not extend to the path**, which costs one `exists()`.
- **C — the duplicate-id error names the wrong cause.** `:370-373` says
  `duplicate id ... uniqueness is global across topics/`, which describes a copied
  row. The reporter's two rows were hand-written and different: `kb_claim_id`
  (`:165-169`) hashes `path#locator#qty` with the text excluded, so two distinct
  assertions about the same span with the same figure mint the same id. The reader
  goes looking for a duplicate that does not exist.
- **D — deferred, by the reporter's ordering.** 22 coverage `[warn]` lines around a
  single real `[ERROR]` forced `grep -E '^\[ERROR\]'` on every run. The reporter's
  first note (errors printed before warnings) was self-corrected: `kb_cmd_corpus`
  (`:1137-1148`) already prints warnings then errors. What is missing is a filter
  (`--errors-only`). Ranked last by the reporter ("D quando capita"); **not in this
  unit of change**, recorded so the next one can pick it up.

## Feature Vision

Serves the Goal *"make divergence from the declared intent visible"*. The corpus
letter's promise is that a claim can always be reopened at its origin; A and B are two
mechanisms that were meant to hold that promise and silently do not. C serves the same
Goal one level down: a check that fires correctly and explains itself wrongly costs the
reader the time the check was supposed to save.

**Ceremony budget, declared (Non-Goal *"no ceremony ratchet"*).** This unit adds two
validator checks above L1: the A' warning and the B warning. Both read fields the
sidecar contract **already** defines (`provenance:`, `original_path:`) — no new
required field, no new authoring step, no cost on a tree where the fields are correct
or absent. Nothing of comparable cost is removed, so the budget rule's second branch
applies: the cost is stated here and needs the owner's explicit acceptance.

**ACCEPTED by Antonio Pinto, 2026-08-25** ("accetto il costo"), after the cost was
stated in these terms: two warnings, on fields the sidecar contract already defines,
zero cost on a tree where those fields are correct or absent, nothing of comparable
cost removed. The budget rule's second branch is satisfied and this unit may merge.

## Use Cases / User Needs

- **Practitioner ingesting a source through a weak extraction chain** (Actor 4 — OCR, a
  transcription from an image, a translation) — can file the claim at its true
  provenance instead of being forced to `GIVEN` by a type bug.
- **A cold agent reading the ledger** — can tell a row backed by a deterministic text
  layer from one backed by a reading of a PNG, mechanically, without parsing prose —
  **provided the sidecar declares the chain in its `provenance:` field.** The check
  reads the field, not the prose around it, so it catches the author who declared the
  chain honestly and then filed the row too strongly. It does not catch — and cannot —
  an author who writes `provenance: GIVEN` over an OCR. That is why A (making the
  honest declaration *possible*) is the larger half of this pair.
- **Practitioner who reorganizes their filesystem** — learns from the validator that 16
  sidecars now point at nothing, instead of from a green run followed by a manual
  re-verification written twice by hand.
- **Practitioner who receives an imported bundle** — is *not* told their originals are
  missing, because a bundle legitimately never carries them.
- **Practitioner hitting an id collision** — reads what actually happened and what to
  do about it, instead of searching for a copy-paste that is not there.

## Capability Ledger

Architect pass run before the Impact. `distributions/` is ANALYZED in `audit_plan.md`.

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| Read the declared frontmatter of **whatever a claim cites**, note or artifact | **INADEQUATE** | `_note_frontmatter` (`sdlc_check.py:274-278`) | re-read: `p = root / rel; if not p.is_file(): return None; return load_frontmatter(...) or {}`. It resolves the cited path itself. For a `given/` artifact that path is a real file with no frontmatter, so the `{}`/`None` distinction the caller depends on is destroyed. The sidecar reader already exists twice — `kb_build_corpus_index:735` and `kb_corpus_check:875` both do `given.glob("*.meta.md")` + `load_frontmatter` — so the capability is present in the file and simply not reachable from the claim checker |
| Distinguish a claim resting on a strong extraction from one resting on a weak one | **MISSING** | — | searched `provenance` across `sdlc_check.py`: it is **written** into the sidecar (template `templates.md:665`) and **read** nowhere. `kb_build_corpus_index` reads `origin`/`derived_from`/`basis` for `notes/` only (`:748-752`). No consumer relates a row's `prov` cell to its artifact's declared `provenance:` |
| Verify that a recorded pointer to a non-copied original still resolves | **MISSING** | — | `grep -n "original_path\|original_sha256" sdlc_check.py sdlc_core.py` → no match, over 3617 lines. Written by the ingesting agent (`distillation.md:47`, `templates.md:666`), read by nothing. Not provisional: `corpus/` is fully covered by the pass |
| Name the real cause when two rows collide on an id | **INADEQUATE** | `:370-373` | re-read: one message serves two causes. The copied-row cause and the hash-collision cause are distinguishable **at the finding site with data already in hand** — the two rows' first source and qty are both parsed there |
| Separate errors from warnings in `corpus`/`graph` output | **EXISTS — insufficient at scale** | `kb_cmd_corpus:1137-1148`, `kb_cmd_graph:1120-1134` | re-read both: warnings print first, errors last; the reporter's ordering complaint was self-corrected. No `--errors-only`. **Out of scope here** (D) |

## Impact

| Path | Change | Why |
|---|---|---|
| kb `scripts/sdlc_check.py` | MODIFY | A: `_note_frontmatter` resolves the **sidecar when one exists**, and reports which file it read so the message can name it. A': new warning in `kb_check_claims`. B: `original_path` resolution check in `kb_corpus_check`. C: the duplicate-id message splits by cause |
| kb `scripts/test_claim_ledger.py` | MODIFY | one test per branch, both directions (F-027's lesson) |
| kb `distillation.md` | MODIFY | §1: `original_path` is checked and `original_sha256` is not — the existing honesty paragraph gains the distinction, and the path's resolution convention. §2: the id function's stated limit (C) |
| kb `templates.md` | MODIFY | sidecar template: `original_path` resolution convention, and the effect of `provenance:` on rows citing the artifact |
| `ai_docs/strategic/skill_family_agent_workflows.md` | MODIFY | derived doc: asserts the two `original_*` fields are "registrati e mai verificati", which B makes false. Named by the `distributions/` audit-plan row as a standing duty of any doctrine edit |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/evals/scenarios/corpus_letter_scales_to_binaries.md` | MODIFY | its pass criterion "`corpus` is clean with no original present" stops discriminating once B can warn on a legitimately absent original |
| `distributions/kb-agentic-skill/README.md` | MODIFY | `:11` states the two `original_*` fields "check nothing on their own". B makes that sentence false — the path is checked, the digest still is not |
| `CHANGELOG.md` | MODIFY | `[Unreleased]` |
| `ai_docs/architecture/ADR_2026-08-25_claim_id_collision.md` | ADD | the rejected ordinal, and why the id's cross-project stability outranks the collision |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | MODIFY | design row, closure row |
| `ai_docs/audit/HANDOFF_kb_provenance_pointers.md` | ADD | open workstream; deleted at closure |

**Blast radius (enumerated).**
- `_note_frontmatter` — `grep -n "_note_frontmatter"` returns exactly **two** sites:
  its definition (`:274`) and its single call (`:326`). No other consumer, in either
  script, in any distribution. The signature may change safely; the change is local by
  enumeration, not by assumption.
- `kb_claim_id` (`:165`) is **not** touched. Its consumers — `kb_fill_ids`, the
  recompute check at `:358`, the id-minting `claim-id` subcommand, and
  `portability.md`'s cross-project dedup, which rests on the id being identical in two
  projects — all keep their present behaviour. C changes a string, not a hash.
- `kb_corpus_check` returns `(errors, warnings)`; B adds to `warnings`, which
  `kb_cmd_corpus` (`:1137`) and the `check` surface already print. No new channel.
- **kb-only.** `sdlc_core.py` is the byte-identical spine and is not in this Impact;
  `shared_manifest.json` does not list `sdlc_check.py`, `test_claim_ledger.py`,
  `distillation.md` or `templates.md`. The drift guard must still find the three
  copies identical afterwards.
- `provenance:` in a sidecar is currently **write-only**; A' gives it its first
  consumer. Every existing sidecar in a live corpus declares `provenance: GIVEN`
  (`templates.md:664`), so the warning is silent on a conformant tree — verified
  against the template, not assumed.

## Security and Threat Model

Surfaces: filesystem reads, and parsing of practitioner-authored frontmatter. No
network, no new external-input parser, no privilege boundary crossed.

| Threat | Answer |
|---|---|
| **T1** — A unblocks `DERIVED`/`RULING`/`IMPORTED` on a `given/` artifact, and a weak claim now passes by writing `derived_from:` into a sidecar | that is the intended, and correct, gate: the existing checks (`derived_from:`, `basis:`, `imported_from:`) apply unchanged to the sidecar's frontmatter. What changes is that the declaration is now **possible and mechanically read**. A row still cannot claim a provenance whose required field is absent |
| **T2** — a `given/` artifact with **no** sidecar now yields `{}` and errors on `DERIVED` | correct and preserved: a `DERIVED` claim resting on an artifact that declares no derivation *is* model knowledge disguised as a source. The message must name the file it looked in, or the reader repeats bug C's hunt — hence the label returned alongside the frontmatter |
| **T3** — the B check becomes an error and every imported bundle fails | **warning, never an error.** Verified, not assumed: `kb_export_closure:1013-1021` collects only paths that resolve **inside** the docs root (`(docs / cand).is_file()`), so an original outside it never travels; `kb_cmd_import:1307` writes bundle bytes verbatim, so no sidecar acquires an import marker to test against. A plain warning is the only form that does not punish a legal import |
| **T4** — `original_path` is practitioner-authored and the check touches the filesystem outside the docs root | the check calls `exists()` and nothing else: no read, no traversal of the target, no content in the message beyond the path the practitioner themself wrote. Deliberately **not** passed through `confine_under` — the field's whole purpose is to point outside the docs root, so confining it would make it permanently unverifiable |
| **T5** — an ambiguous resolution rule makes the B warning fire on correct sidecars, and a warning that fires wrongly is a warning practitioners learn to ignore | absolute paths are tested as written. A relative path is tried against the docs root's **parent** (the project root in the standard layout, and what the reporter's corpus uses) **and** against the docs root itself; it warns only if **neither** resolves, and the message names both roots it tried. Two candidates rather than one because `--root` and `migrate` both allow a docs root that does not sit directly under the project root, and a single convention would fire falsely on every such tree. Documented in `templates.md` beside the field, since today it is implicit |
| **T6** — C's new message asserts a cause it has not established | the discriminator is the **claim text**, not the source: same first source and same qty are shared by a copied row *and* by a collision — they are implied by the id itself, so they separate nothing. Two rows with the same id and the **same** text are a copied row (the existing uniqueness message stands); the same id with **different** text is the case the hash provably cannot separate (the new message). `all_rows[id] = (row, rel)` at `:375` already holds the other row's text, so the branch costs no new lookup. Two branches, two tests |
| **T7** — the id collision stays possible after C | acknowledged and stated, not silently left: message-only is a deliberate choice (ADR), and the limit is written into `distillation.md` §2 in the same form as `original_sha256`'s. An unstated limit is worse than an absent guarantee — the file's own rule |

## Action Plan

1. **A** — `_note_frontmatter` returns `(meta, label)`; it reads `<rel>.meta.md` when
   that sidecar exists and the cited file otherwise, so a verbatim `.md` source stored
   in `given/` resolves the same way as a `.txt` extraction; the call site names the
   file it read. RED first.
2. **A'** — `GIVEN` row citing a `given/` artifact whose sidecar declares a
   `provenance:` other than `GIVEN` → warning naming both.
3. **B** — `original_path` resolution warning in `kb_corpus_check`.
4. **C** — split the duplicate-id message by cause.
5. Docs: `distillation.md` §1 + §2, `templates.md` sidecar block.
6. ADR (C's rejected ordinal), CHANGELOG, `index`, review log, handoff.
7. Full battery ×3 + drift guard.

## Test Strategy

- **A** — a `DERIVED` row citing `corpus/given/x.txt` whose sidecar carries
  `derived_from:` **passes**; the same row with a sidecar lacking it **errors**; an
  artifact with **no sidecar at all** errors too. The first test is the bug (it fails
  today); the other two prove the gate still bites. Separately: `RULING`/`basis:` and
  `IMPORTED`/`imported_from:`, because A closes three classes and one test would let
  two regress unseen. Plus a `corpus/notes/*.md` source, which must keep resolving to
  its **own** frontmatter and not to a sidecar that does not exist.
- **A'** — a `GIVEN` row citing an artifact whose sidecar says `provenance: DERIVED`
  warns; the same row with `provenance: GIVEN` is silent. Both directions.
- **B** — a sidecar whose `original_path` resolves is silent; one whose path does not
  resolve **warns and does not error** (asserted on the errors list too — the whole
  point of T3 is that it must not be an error); a sidecar with no `original_path` is
  silent. Relative-path resolution asserted against the project root.
- **C** — two rows with the same id and **different** claim text produce the
  **collision** message; two rows with the same id and the **same** text still produce
  the **uniqueness** message. Separate tests: one test tripping both branches lets
  either be deleted with the suite green.
- **Regression** — `kb_claim_id` output unchanged for a fixed input (C must not move a
  hash), and the existing `TL_T8_Provenance` / `TL_Corpus` classes stay green.
- **Family** — full battery ×3, drift guard byte-identical.

## Diary / Current State

**2026-08-25 — opened.** Standalone, devPNT off. `Level: L3 · router: no match`
(`GUIDE_release.md` is the only guide and governs publishing, not this fix).
Branch `feat/kb-field-report-2` off `main` (v1.26.1).

**Repository correction, recorded because it cost the session's first pass.** The
report was filed against `D:\SoftwareDev\skill_sdlc\kb-agentic-skill`, which does not
contain the code it describes: that tree is `@antoneeo/kb-agentic-skill` **1.0.0**, an
early derivation off an agentic-sdlc v1.19.0 seed, with no corpus machinery and no
`portability.md`, seven commits unpushed. The live source is this monorepo's
`distributions/kb-agentic-skill/`, published as kb 1.4.1. The reporter's line numbers
match it exactly. The stale tree is a hazard on its own — it is a plausible place to
"fix" a bug that would then never ship — and it is named here so the next session does
not repeat the search.

**Two of the reporter's own diagnoses were checked and one narrowed.** The claim that
A is "a lacuna di modello" (a missing vocabulary for weak extraction chains) is only
half of it: the vocabulary gap is real, but underneath it is a plain type bug that
closes four provenance classes outright, including three that have nothing to do with
extraction strength. Fixing the type bug is the larger repair, and it makes the
vocabulary question answerable without adding a `TRANSCRIBED` value — the reporter's
own preferred option, and it is the one taken.

The reporter delegated C's design choice explicitly ("valutalo tu"). **Ordinal
rejected.** `kb_claim_id` excludes the claim text so that the same assertion in two
projects mints the same id, which is what makes `portability.md`'s de-duplication
mechanical rather than a judgement call. A disambiguating ordinal is per-project state
by construction and would break exactly that. The collision stays possible; what
changes is that it is named correctly and its limit is written down.

**2026-08-25 — implemented, awaiting the owner.** All four fixes are on
`feat/kb-field-report-2`, uncommitted (no commit was requested).

*Evidence, run after the final edit.* kb battery **258 OK** (13 skipped), code lens
**162 OK**, mkt **180 OK** (13 skipped). Spine drift guard: `sdlc_core.py` is
md5-identical across all three distributions (`4a942191…`) — the change is kb-overlay
only, as the Impact said. New F-035 tests: 18, of which 8 failed before the patch and
all 18 pass after. `sdlc_check.py validate` rc=0.

*What is NOT clean, stated rather than smoothed over.* `check` reports
`NOT CLEAN (validate rc=0, stale rc=1)`. The single remaining stale area is
`skills/agentic-sdlc-skill/` (7 files) and **this change touched none of them**: they
were last modified by `61f1425` (F-034, v1.26.1) and `1af3bef` (v1.23.0), both already
on main and both after that row's recorded reference of 2026-08-05T03:32:48Z. So the
gate was already red at HEAD, before this branch existed. It is deliberately left that
way: `mark` on that row would assert a re-analysis of F-034's work that did not happen,
and that row's own note says its re-analysis is not complete until two derived documents
agree. `distributions/` WAS marked, after discharging the duty its row names — the
distribution `README.md` and `strategic/skill_family_agent_workflows.md` both asserted
that the two `original_*` fields "check nothing on their own", which item B makes false;
both were corrected in this change.

*The design review ran at rung 3 and the log row says why.* Rung 1 (fresh subagent) is
off by session policy; rung 2 was attempted twice and both clients are broken on this
machine — `gemini` exits on `IneligibleTierError` (and exits **0** while doing so, which
is its own trap for anyone trusting the exit code), `codex` refuses to load
`~/.codex/config.toml` because `service_tier = "default"` is not a valid variant. The
self-pass still found five defects in this document, three of them BLOCK, including the
provenance-class miscount that the field report itself also got wrong and the
discriminator error in item C. That is the gate paying for itself even at its weakest
rung — but the independence was reduced, and the log row says so.

*Outstanding, and it is the owner's call:* the ceremony budget declared under
`## Feature Vision`. Two new warnings, on fields the sidecar contract already defines,
with nothing of comparable cost removed — the Non-Goal's second branch requires explicit
acceptance before this merges.
