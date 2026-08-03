---
id: F-031
feature: Exhaustive ingestion — the source is exhausted, not sampled, and the work resumes across sessions
status: PLANNED
level: L3
start_date: 2026-08-03
end_date:
---
# Feature Analysis: Exhaustive ingestion

## Objective

Owner, from the field (2026-08-03): *"l'agente che deve fare l'ingestion del grafo tende
a prendere scorciatoie e alla fine si perde un sacco di informazioni. Il grafo funziona
se tutta l'informazione di un file viene riversata in esso."*

An agent handed a 200-page manual emits a few dozen claims and reports done. Nothing it
did broke a rule: `distillation.md` §3 says what a claim is and that the extractor
invents nothing. **It never says the source must be exhausted, and it gives the agent no
way to know — or to show — that it finished.** A completion claim is currently
unfalsifiable.

**This is the third appearance of one class**, and naming it is half the fix: the rule is
obeyable, the agent obeys it, and the outcome is still wrong because a **coverage axis**
is missing. F-029 #1 was the same shape (powers recorded, gates skipped); so was the
Capability-Ledger example. A rule that says *what a good row looks like* never implies
*which rows must exist*.

Second, structural cause: a long source **cannot** be ingested in one context. Without a
resumable unit of work, an agent that runs out of room has only two moves — summarize, or
stop silently. It picks summarize.

## Feature Vision

**Precedent** (`vision/rulings.md`, before any prose).

| Row | Placement | Consequence |
|---|---|---|
| **r14** — *fixes a defect with purpose, actors and surface unchanged* → **exempt** | the extraction rule is incomplete, exactly as in F-029. Ingestion's purpose, actors and surface do not move | no admission needed for the rule itself |
| **r2** — *collects per-document or per-work state into one surface — stored, generated or derived on demand* → **REJECT** | **entered, and this is the one to get right.** A central "ingestion register" listing every source and how far each got is precisely this row | **so no central register is built.** Coverage lives on each artifact's own sidecar — the Vision's own discriminator: *"a document describing its own state … its own progress (planned → in progress → completed) qualifies, because it describes the document, not an assignment"* |
| **r3** — *tells an agent what to work on next, in what order* → **REJECT** | a field saying `next: pages 60-80` answers exactly that question | **record what has been covered, never what remains.** "Next" stays derivable and unstored — the same line the generated manifest already walks |
| **r9** — *outputs the set of documents that are NOT current* → **REJECT** | a `corpus` report listing "the incomplete artifacts" is this row verbatim | the coverage figure is printed **per artifact, for every artifact**, as a fact on the row that already exists in `corpus/INDEX.md`. Never filtered, never sorted by it |

**Goal / Actor advanced.** Goal 2 — knowledge that stays durable — is not advanced by a
graph that holds a tenth of its sources; the Core Problem (*understanding evaporates*)
happens here at ingestion time rather than between sessions. Actor 4, *Practitioner in a
non-code domain*, is the one who believes the graph answers from the whole manual.

**Non-Goal 3 (ceremony), disclosed.** One new sidecar field, `extracted_through:`,
**required only once an artifact has claims** — you may not say you extracted from
something without saying how far you got, and an artifact nobody extracted from owes
nothing. Ingestion is L3 by Rule Zero, so **L1 and L2 never meet this**. The reading
window is a rule about how to work, not an artifact. No step is added to any level.

**Non-goals of this feature.** No second register (see r2 above). No queue, no ordering,
no assignee. No automatic extraction — the agent still reads and judges. No hard
per-model page number baked into doctrine as if it were a law of nature.

## Use Cases / User Needs

- **Practitioner in a non-code domain** (Actor 4) — hands over a 212-page manual and gets
  a graph that answers from all of it, not from the first twenty pages plus a summary.
- **Practitioner in a non-code domain** — comes back three days later and the ingestion
  resumes where it stopped, without re-reading what is already extracted.
- **A cold agent inheriting a half-ingested corpus** — can tell, per artifact, what has
  been covered, instead of guessing from the claim count.
- **The owner reviewing an ingestion** — can falsify "done": today the claim is
  unfalsifiable, which is why the shortcut is invisible.

## Capability Ledger

Architect pass. `distributions/` is ANALYZED; the search covers the kb support files, the
`kb_*` inventory and the plan/dispatch machinery.

| Capability | Verdict | Owning component / gap | Evidence |
|---|---|---|---|
| Resume a long unit of work across sessions, task by task | **EXISTS** | `PLAN_[feature].md` + `PLAN_[feature].ledger.json` + `dispatch.md` (`templates.md`:310-356) | re-read the contract: tasks carry `id`/`title`/`verify`/`paths`, and the ledger records `status: done` per task, orchestrator-owned and **validator-read-only**. This is the owner's *"registro a che punto è"*, already shipped. Building a second one would be double placement **and** would walk into r2 |
| Record a per-artifact fact that travels with the artifact | **EXISTS** | the sidecar `<artifact>.meta.md` (`distillation.md` §1) | re-read: it already carries digest, date, provenance, `supersedes:`, `original_path:`. One more field about the artifact's own state is the established shape, and it is the shape r2 permits |
| Present per-artifact facts as an inventory for lookup | **EXISTS** | `kb_build_corpus_index` (`sdlc_check.py:667-685`) | re-read: one generated row per artifact, built from the sidecars. Coverage becomes one more cell on a row that already exists — the permitted manifest form, not a new surface |
| State that the source must be exhausted, not sampled | **MISSING** | — | `distillation.md` §3 defines the row and forbids invention; searched `exhaust`, `complete`, `coverage`, `all of`, `sample` across the kb support files — nothing requires the file to be finished, and nothing bounds how much is read at once |
| Make a completion claim falsifiable | **MISSING** | — | no artifact, field or check today distinguishes "extracted fully" from "extracted the first pages". The claim count cannot do it: a short source legitimately yields few rows |
| Bound how much is read before rows are emitted | **MISSING** | — | same search. `dispatch.md` bounds *tasks*, never *reading* |

## Impact

Design in one line: **the extraction rule gains an exhaustiveness clause and a bounded
reading window; each artifact's sidecar records how far it has been extracted; and the
resumable unit is the existing plan task, one per window — no new register, because the
one that would be needed is the one Non-Goal 1 forbids.**

| Path | Change | Why |
|---|---|---|
| kb `distillation.md` | MODIFY | §3: exhaustiveness ("the source is exhausted, not sampled"), the bounded window and why it exists, the duty to advance `extracted_through:` at the end of each window, and the honest limit — no validator can prove a page was *understood* |
| kb `templates.md` | MODIFY | sidecar template gains `extracted_through:` with its meaning and its limit; the ingestion `PLAN_` example becomes one task per window |
| kb `scripts/sdlc_check.py` | MODIFY | `kb_build_corpus_index`: coverage cell per artifact. `kb_corpus_check`: error when an artifact has claims and no `extracted_through:`; advisory when it is short of the end. **Per artifact, never a filtered list** (r9) |
| kb `scripts/test_claim_ledger.py` | MODIFY | one test per branch, plus the r9 guard: the report covers every artifact, not a selection |
| kb `evals/scenarios/` | ADD | cold run on a long source: sampling and declaring done is the FAIL |
| kb `SKILL.md` | MODIFY | Write Triggers: ingesting a long source produces a `PLAN_` with one task per window |
| kb `README.md`, `strategic/skill_family_agent_workflows.md` | MODIFY | derived documents |
| `CHANGELOG.md` | MODIFY | `[Unreleased]` |

**Blast radius.** The sidecar contract is read by `kb_corpus_check` and
`kb_build_corpus_index` — that is the whole consumer set, verified by grep on
`load_frontmatter` under `corpus/`. The spine is untouched: this is kb's own method, so
the drift guard must still find the three copies identical. `PLAN_`/ledger are used
as-is; **no change to `plan` or `dispatch.md`** — if either needs changing, the design
was wrong and I would rather find that in review than paper over it.

## Security and Threat Model

Surfaces: filesystem and the parsing of third-party documents already in the corpus. No
new external input — the window is a reading discipline, not a new intake path.

| Threat | Answer |
|---|---|
| **T1 — the register becomes a work board** (Non-Goal 1) | no register exists to become one. Coverage is per artifact, on the artifact's own sidecar; the report is per artifact for all artifacts; nothing records what remains |
| **T2 — `extracted_through:` becomes a lie**: the agent advances it without extracting | it is a claim like any other and it is falsifiable the same way: the pages it covers either produced rows with spans in that range or they did not. The check can compare the advanced range against the spans actually cited — stated as the design intent, and if it proves impractical the limit gets written down rather than the field being trusted |
| **T3 — the rule turns into fabrication**: "exhaust the source" pressures an agent to invent rows for empty pages | the F-029 guard applies unchanged and must be restated here: *ask, never produce*. A page that asserts nothing yields nothing, and a source that is mostly boilerplate legitimately yields few rows. Exhaustive means **read**, never **row-per-page** |
| **T4 — a hard page number ages badly** across models and page densities | doctrine states the rule and a default; the plan states the window actually used, so it is declared per ingestion rather than assumed |
| **T5 — resuming re-extracts what is already there** | claim ids are `sha256(path#locator#qty)`: a re-extracted identical span mints the identical id, so duplication is detectable rather than silent (the F-030 property, reused) |

## Action Plan

- [ ] **A — the north star, then §3.** Owner, 2026-08-03: the ingestion agent needs a
      north star, *"nemmeno una delle informazioni contenute nei file forniti deve andare
      perduta"*. Accepted, with one correction to the unit and one to the shape — both
      agreed in the same exchange. Goes at the TOP of `distillation.md`, before §1,
      because it is the criterion that generates the rules rather than one more rule:

      > **North star.** *Not one assertion the source makes may be lost, and not one it
      > does not make may appear.* These are one rule, not two: a ledger that invents
      > nothing but keeps a tenth of the manual is as useless as one that keeps
      > everything and made half of it up.
      >
      > The unit is the **assertion**, not the byte: layout, ordering, repetition and
      > page furniture are not assertions. A page that asserts nothing yields nothing —
      > exhaustive means **read**, never *a row per page*. And "I am finished" is an
      > assertion like any other: `extracted_through:` is what makes it falsifiable.

      Why the unit had to change: read literally, "no information" includes layout and
      page furniture, and an agent that believes it transcribes the manual — the
      opposite failure, equally real, and the one that would destroy the ledger's
      purpose. Why the counterweight sits in the SAME sentence: two rules a paragraph
      apart get optimized whichever was read last, which is the coin-flip defect the
      Vision's own history records. Then §3 keeps the bounded window, the
      anti-fabrication restatement (T3) and the honest limit.
- [ ] **B — `extracted_through:`**: sidecar template + the two checks (error when claims
      exist without it; advisory when short of the end), per artifact.
- [ ] **C — coverage in `corpus/INDEX.md`**, one cell on the existing row.
- [ ] **D — the ingestion plan shape**: one task per window, using `PLAN_` + the existing
      ledger. No new machinery, and no change to `plan`/`dispatch.md`.
- [ ] **E — span-vs-range consistency** (T2) if it holds up; if not, write the limit down.
- [ ] **F — tests, cold-run scenario, derived docs, closure.**

## Test Strategy

- **The r9 guard is a test, not a promise**: the coverage report names every artifact,
  including the fully-extracted ones. A report that lists only the incomplete ones must
  fail the suite — that is the Non-Goal, and it is the easiest thing to drift into.
- **One test per branch** (F-027's lesson): claims without `extracted_through:` → error;
  `extracted_through:` short of the end → advisory, never error (partial work is legal
  mid-ingestion); no claims and no field → silent.
- **Anti-fabrication (T3)**: a fixture whose later pages assert nothing must pass with no
  rows for them. The rule must not manufacture claims.
- **Resume**: a plan with three window tasks, ledger marking the first done → the second
  is the one dispatched, proven through the existing `plan`/ledger path with no new code.
- **Cold-run scenario**: an agent given a long source and a window must produce window
  tasks and advance coverage; sampling the first pages and reporting done is the FAIL.
- **Family**: batteries ×3, drift identical, `npm pack` shape unchanged.

## Diary / Current State

**2026-08-03 — opened, not implemented.** Standalone, devPNT off.
`Level: L3 · router: no match`.

The owner's proposed mechanism was right in both halves — bounded reading, and a record
that survives sessions — but the architect pass moved where the second half lives. kb
already ships `PLAN_[feature].md` with an orchestrator-owned, validator-read-only ledger
recording `status: done` per task. That **is** the register, so building a second one
would duplicate a component *and* walk straight into Non-Goal 1, which forbids collecting
per-work state into one surface.

What the Vision forced, rather than what I preferred: coverage is a fact **on each
artifact's own sidecar**, because the Vision's own discriminator admits a document
describing its own state and refuses a surface that collects them; and the report prints
every artifact, because "the set that is not current" is ruled REJECT by r9. Both
constraints came out of the gate, not out of taste, and both make the feature smaller.

The third repetition of the coverage-axis class is the finding worth keeping: `powers
without gates`, `Capability Ledger examples from the wrong lens`, and now `rows without
exhaustion`. Each time the rule described a good output and never said which outputs must
exist. That pattern belongs in the review checklist, not only in this document.

**2026-08-03, later — the north star, before implementation.** The owner named what
`distillation.md` was missing: a criterion, not another rule. The file today carries a
floor ("the extractor invents nothing") and no target, and an agent optimizing against a
floor stops the moment nothing it wrote is false — which is precisely the observed
behaviour: **nothing the field agent emitted was wrong.** Recorded in Action Plan A with
its exact wording, its unit correction (assertion, not byte) and the reason both halves
must share one sentence.

Home: `distillation.md`, not the project Vision. The Vision governs the product; this
governs one lens's method, and amending the Vision is its own proposal by its own rule.

Open: nothing blocking. Nothing implemented.
