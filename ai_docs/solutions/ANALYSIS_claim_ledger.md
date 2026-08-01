---
id: F-025
feature: Claim Ledger (assertions with provenance, and what happens when two disagree)
status: PLANNED
level: L3
start_date: 2026-08-01
end_date:
---
# Feature Analysis: Claim Ledger

## Objective

Two lenses of the family need the same thing and neither has all of it: a table of
**individual assertions**, each bound to the source location it came from, each carrying
how much that source is worth, plus a decision procedure for what happens when two
assertions about one subject disagree.

- **Marketing has half of it.** `mkt_check.py#load_ledger/run_ledger` reads an evidence
  ledger keyed `id | claim | class | source`, classifies each row FACT / BENCHMARK /
  ASSUMPTION with a confidence, and detects duplicate ids and dangling `[EV-nn]`
  references. It is registered as the portable check `marketing.ledger` and its own
  docstring offers it "to documents owned by ANOTHER domain". What it has no notion of:
  a claim that is true only in a window, a claim about a relationship, a quantity that
  must aggregate, or two claims that contradict.
- **Knowledge needs all of it** (F-024): a second brain over supplied specifications is
  exactly a corpus of assertions whose worth differs by where they came from.

Building it twice is the duplication this family exists to end. This analysis defines the
component once; F-024 is its first full consumer, and marketing's ledger is prior art it
generalizes rather than replaces.

**Contract, stated without naming either consumer:** *hold assertions, each bound to a
reopenable source location and a provenance; decide mechanically whether two assertions
are the same, refine one another, hold in disjoint scopes, or conflict; and when they
conflict, resolve by a stated order or refuse to resolve — never silently.*

## Feature Vision

**Expected benefit.** An answer built from the ledger can be defended: every figure
traces to a page, and every contradiction is either resolved by a rule the practitioner
can read or is sitting in front of them unresolved. The alternative — a document-level
"source list" — cannot do either, because you cannot reconcile documents, only assertions.

**Alignment.** `project_vision.md` Goal 7 admits a sibling only if it adds **no capability
the family lacks**. This analysis is the other side of that coin: it prevents a *second*
implementation of a capability the family already half-has, which is the same rule
applied inward.

**Non-Goals, all four, run:**

| Non-Goal | Verdict |
|---|---|
| *Not a work-management system* | **Satisfied, and it constrains the design.** A claim describes a subject, never a unit of work. No field ranks anything, and **no command aggregates claim state across documents** — the forbidden capability is collection into one surface, so the checks report per-document findings only, exactly like every other validator finding |
| *No ceremony ratchet* | **Cost declared, acceptance owed.** See the budget below; the removal column is genuinely empty because nothing is being retired, so this falls to the explicit-owner-acceptance branch and is **open** |
| *One triage authority per kind of work* | **Satisfied.** Reconciliation outcomes classify *assertions*, not work; each consumer's Rule Zero remains the sole triage of what to do about them |
| *No coupling to another tool's formats* | **Satisfied.** The design converges with nanopublications (assertion + provenance as one atomic unit) and truth-discovery's evidence weighting, and reproduces neither: no external schema, vocabulary or file format is emitted or parsed. If either changes, nothing here changes |

**Ceremony budget.** Lands on **L3 only** for a consumer adopting the ledger. Honest
accounting of what an **L2** edit pays once the ledger exists: adding one row means
computing a 12-hex id, which is a hash over two fields the author already has — provided
by `sdlc_check.py claim-id <path> <locator>` so it is a command, not arithmetic by hand.
That is the true added cost at L2, and it is stated here rather than claimed to be zero.
Nothing shipped is removed in exchange. **Owner acceptance of this budget is the open
item; the proposal does not clear the bar without it.**

## Use Cases

- **UCL1** — As an author, I record an assertion and later reopen exactly the page it came
  from, so a challenged figure can be checked in seconds rather than re-read.
- **UCL2** — As an author, I add a source that says the same thing and the base gets
  *stronger*, not longer: one row, two sources.
- **UCL3** — As an author, two sources disagree and I am shown both with their provenance,
  rather than being handed one of them silently.
- **UCL4** — As the practitioner, I rule on a contradiction once and am not asked again.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| hold rows of claims with id, text and source, and detect duplicate ids and dangling references | **INADEQUATE** | `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py#load_ledger`, `#run_ledger`, registered as portable check `marketing.ledger` | re-read `run_ledger`: it validates class ∈ FACT/BENCHMARK/ASSUMPTION, confidence, date, duplicate ids, `[EV-nn]` resolution. **Gap:** no locator inside the source, no validity scope, no typed quantity, no relationship form, and no reconciliation at all — two rows asserting opposite things both pass |
| parse a markdown table out of a governed document, stdlib only | EXISTS | `mkt_check.py#find_table` | re-read: locates a table by its header cells and returns rows; already the mechanism three marketing checks rest on |
| address a source file by content and re-hash it | **INADEQUATE** | `sdlc_core.py#sha256_file` + the `.sources/<slug>-<hash8>` convention in `guides.md` | re-read both: the helper and the naming convention exist and are used for guides. **Gap:** `cmd_stale` iterates `list_guides`, which globs `reference/GUIDE_*.md` only, so no shipped detector looks anywhere else. What is reusable is the helper and the convention, not the detector |
| offer a check written in one lens to documents owned by another | EXISTS | `sdlc_core.py#portable_check` + `declared_checks`/`run_portable_checks` | re-read: a document opts in with `checks:`, findings are added and never authority. This is the seam through which a knowledge ledger check can also serve a marketing document |
| **decide what two disagreeing claims mean, and act on it** | **MISSING** | — | searched `mkt_check.py` (the only ledger implementation), the spine, and all three overlays for reconcile / conflict / supersede / contested: `mkt_check.py` has none, the spine has none. `templates.md` in kb mentions CONTESTED as a word in a template comment, backed by no procedure. No owner |

The MISSING row is the actual new component. Everything above it is generalization.

## Design

### The row

A claim table lives under a heading the consumer chooses, with fixed columns:

| id | claim | valid | qty | about | source | prov | state |
|---|---|---|---|---|---|---|---|
| c7f3a91b0e42 | List price of module A is 12000 EUR | until 2026-03-01 | 12000 EUR cost | - | corpus/given/contract-9a1f2b7c.pdf#p=17 | GIVEN | OK |

- **`id`** — first 12 hex of `sha256(source_path + "#" + locator)`, **computed from the
  location alone, never from the claim text**, and fixed at first insertion. Keying on the
  text would defeat the purpose: extraction is an LLM pass, so a re-run paraphrases, the
  hash changes, and the same assertion is inserted twice — which is precisely the
  duplication the id exists to prevent. Location is stable across re-extraction; wording
  is not. Consequence, stated because it is a real constraint: **one claim per source
  location.** A page asserting three things needs three locators (`#p=17a`, `#p=17b`), and
  the extractor is what makes them distinct.
- **`claim`** — one falsifiable assertion. "The system is robust" is not a claim; "the
  retry runs 3 times with backoff" is.
- **`valid`** — `-`, `from <date>`, `until <date>`, `from X until Y`, or `if <condition>`.
  **Half-open by definition: `from` is inclusive, `until` is exclusive**, so
  `until 2026-03-01` and `from 2026-03-01` do **not** overlap — without that rule the two
  most obvious rows in any corpus produce a spurious conflict on the boundary day. `-`
  means unbounded. `if <condition>` is free text, so overlap is undecidable: it is treated
  as **always overlapping**, which sends it to the conflict path rather than letting two
  conditional claims coexist on an assumption the validator cannot check.
- **`qty`** — `-`, or `<value> <unit> <kind>` with kind in `effort | cost | duration |
  count`. Without a unit, "3 weeks" versus "15 days" cannot even be classified as
  agreement or disagreement, and nothing aggregates.
- **`about`** — `-`, or `<predicate> -> <target>`. A claim about a relationship belongs to
  neither endpoint alone; it is stored once, under the document that owns the subject, and
  the reverse direction is computed.
- **`source`** — `<path>#<locator>`, locator typed by source class: `p=17` (paged),
  `L40-52` (line-addressed), `Sheet1!B7` (cell). Corroboration appends further sources
  after the first, separated by `;`; **the id keeps its originating source**, which is what
  makes recomputation well-defined on a corroborated row.
- **`prov`** — `RULING | GIVEN | ELICITED | DERIVED`.
- **`state`** — `OK`, `CONTESTED <id>`, `SUPERSEDED <id>`, or `CHALLENGED <id>` on a
  ruling. Per claim, never per document: one disputed date must not condemn a whole file.

### Provenance is a partial order

| Provenance | What it is |
|---|---|
| `RULING` | a decision the practitioner took on a contradiction. **Pins** the claim |
| `GIVEN` | an artifact the practitioner handed over |
| `ELICITED` | the practitioner said it; the agent transcribed it |
| `DERIVED` | the agent synthesised it; must declare `derived_from` |

`GIVEN` and `ELICITED` are **incomparable on purpose** — a spoken correction may postdate
a document, or the document may be newer, and only the practitioner knows which. Any
implementation storing provenance as a rank integer is therefore wrong.

`RULING` exists because without it a resolved conflict re-opens forever: the practitioner
rules, the ruling is transcribed as an elicited note, and GIVEN-versus-ELICITED escalates
again on the next run.

### Reconciliation — outcomes

Applied when a new claim addresses a subject an existing row already addresses:

| Outcome | When | Action |
|---|---|---|
| **new** | nothing on that subject | insert |
| **corroboration** | same assertion, different source | append the source to the existing row. **Never a second row** |
| **refinement** | strictly more precise, not contradictory | replace the text, keep both sources, old text preserved in a `SUPERSEDED` row |
| **coexistence** | contradictory *only if scopes overlap*, and by the half-open rule they do not | keep both, neither supersedes |
| **conflict** | contradictory with overlapping scope | the ladder |

### The ladder — total by construction

All ten unordered provenance pairs. A cell that is not listed does not exist.

| Pair | Outcome |
|---|---|
| `RULING` × `RULING` | **escalate.** The practitioner has contradicted their own earlier decision; a newer ruling does not silently revoke an older one, because the usual cause is not knowing the first was made |
| `RULING` × `GIVEN` | the ruling stands; the other row becomes `CHALLENGED`, and is **not** escalated again |
| `RULING` × `ELICITED` | as above |
| `RULING` × `DERIVED` | as above |
| `GIVEN` × `GIVEN` | different dates **and** comparable breadth → newer wins, older `SUPERSEDED` with the reason recorded. Same date, undatable, or **different breadth** → **escalate** (a narrow addendum must not silently override a broad master agreement) |
| `GIVEN` × `ELICITED` | **escalate** |
| `GIVEN` × `DERIVED` | GIVEN wins **unless** the derived claim's newest `derived_from` source is newer than the conflicting GIVEN → then **escalate**. Ranking by channel alone would let an unsigned draft from last year silently beat a synthesis of ten signed quotes from this quarter |
| `ELICITED` × `ELICITED` | different dates → newer wins, older `SUPERSEDED` with the reason. Same date → **escalate** |
| `ELICITED` × `DERIVED` | ELICITED wins; the derived row is flagged for re-derivation |
| `DERIVED` × `DERIVED` | **re-derive, do not escalate.** Two agent syntheses disagreeing is an internal inconsistency, not a question for the practitioner: both rows are dropped and derivation re-runs from sources |

Escalation marks **both** rows `CONTESTED <other-id>`, keeps both with their sources, and
surfaces them. It never picks one. Silence is what the absence of this table produces, and
making it impossible is the point.

### What is code and what is prose

The distinction matters because a rule no check can verify drifts. These are **pure
functions**, stdlib, in the consumer's entry point — so the ladder is testable rather than
merely written down:

| Function | Answers |
|---|---|
| `claim_id(source_path, locator)` | the id, and the `claim-id` command wraps it |
| `parse_claims(text, heading)` | rows out of the markdown table, on `find_table`'s pattern |
| `scopes_overlap(a, b)` | half-open date logic; `if` conditions always overlap |
| `resolve(prov_a, date_a, breadth_a, prov_b, ...)` | one of the ten cells, or `ESCALATE` |
| `check_ledger(rows)` | duplicate id, malformed locator, id not matching its source, `DERIVED` without `derived_from`, `CONTESTED` pointing at a missing id, quantity with no unit |

What stays prose: *which* rows address the same subject, and whether one refines another.
That is semantic judgement, and no query decides it. The standing pairing is the family's
usual one — **the agent judges, the machine verifies afterwards**.

## Impact

Paths relative to `distributions/kb-agentic-skill/skills/kb-agentic-skill/` unless stated.

**No file in `shared_files.py#SHARED_FILES` is touched.** The ledger is implemented in the
consumer's entry point, which is `NOT_SHARED_ON_PURPOSE`, precisely so a domain's data
model cannot enter the byte-identical spine.

| Path | Change | Responsibility | Why it changes |
|---|---|---|---|
| `scripts/claim_ledger.py` | ADD | the five pure functions above | one module, imported by the entry point; separable because a second consumer exists |
| `scripts/sdlc_check.py` | MODIFY | expose `claim-id`; run `check_ledger` inside the overlay's `check` | the command surface a consumer needs |
| `scripts/test_claim_ledger.py` | ADD | the battery | a check with no test is a claim |
| `templates.md` | MODIFY | the claim-table template | authors need the exact column set, or they invent one |
| `ai_docs/solutions/ANALYSIS_kb_knowledge_method.md` *(repo root)* | MODIFY | names this document as the component it consumes | `architect.md`: the two analyses name each other |
| `ai_docs/strategic/architecture.md` *(repo root)* | MODIFY | Component Map row for the ledger | a component was born |

**Not touched, and named so the omission reads as a decision:**
`distributions/mkt-agentic-sdlc/**` — marketing keeps its evidence ledger unchanged. This
component generalizes it; **migrating marketing onto it is its own unit of change**, with
its own golden-transcript risk, and bundling it here would put two independently
shippable increments in one branch.

**Blast radius.** `claim_ledger.py` is new, so it has no consumers to break. The one
existing symbol touched is the entry point's `main`, and the addition is a new subcommand
plus a call inside the overlay's own `check` — no existing subcommand changes behaviour on
a tree containing no claim table.

## Security and Threat Model

Surfaces: **external input parsing** (claim rows are written by an agent reading untrusted
documents) and **filesystem** (the `source` column is a path a later stage opens).

| # | Threat | Mitigation |
|---|---|---|
| TL1 | **Path traversal through the `source` column.** A hostile document yields `source: ../../../../Users/x/.ssh/id_rsa#p=1`, which the checks then open and hash | every `source` path through `confine_under(root, v)` before any open, mirroring the spine's fail-closed guard on `distilled_from`. Tested |
| TL2 | **Laundered synthesis.** A `DERIVED` row with no `derived_from` is model knowledge entering the ladder with real weight | `check_ledger` errors on it; `DERIVED` loses to `GIVEN` and `ELICITED` in every cell |
| TL3 | **Forged provenance by hand-editing.** An author edits a claim's `source` to a stronger document while keeping the id | ids are recomputed from `source_path#locator` and compared; a mismatch is an error. This works precisely because the id excludes the text: text may be corrected freely, provenance may not be moved silently |
| TL4 | **Conflict laundering.** Deleting one side of a contradiction makes the base look consistent | `CONTESTED <id>` pointing at a missing id is an error, so removing one side breaks the check rather than quietly succeeding |
| TL5 | **Table parsing on adversarial input.** A pipe inside a claim splits a row | cells are stripped and the column count is enforced; a row with the wrong arity is an error, never silently truncated |

No network, no authentication, no cryptography beyond hashing, no personal data held by
the component itself. "No security impact" is not claimed: TL1 is a genuine traversal
surface created by putting an untrusted-derived path in a governed file.

## Action Plan

- [ ] `claim_ledger.py`: the five pure functions
- [ ] `test_claim_ledger.py`: the ladder cell by cell, scope boundaries, ids, the checks
- [ ] Wire `claim-id` and `check_ledger` into the kb entry point
- [ ] Claim-table template
- [ ] Component Map row; F-024 cross-reference
- [ ] Closure: `check` CLEAN, drift guard green, three golden transcripts byte-identical

## Test Strategy

| Id | Asserts |
|---|---|
| TL-T1 | the id is unchanged when the claim text is rewritten, and changes when the locator does — the property the whole idempotency argument rests on |
| TL-T2 | `until X` and `from X` do **not** overlap; `-` overlaps everything; `if <cond>` overlaps everything |
| TL-T3 | all ten ladder cells, each with a case that returns the documented outcome |
| TL-T4 | `RULING × RULING` escalates, and `RULING × GIVEN` does **not** re-escalate — the loop that makes contested queues immortal |
| TL-T5 | corroboration appends a source and leaves the id and the row count unchanged |
| TL-T6 | `GIVEN × DERIVED` flips to escalation when the derived source is newer |
| TL-T7 | recomputation catches a moved `source` (TL3); a traversing path is refused (TL1) |
| TL-T8 | `DERIVED` without `derived_from` errors (TL2); `CONTESTED` pointing at a missing id errors (TL4) |
| TL-T9 | a row with the wrong column count errors rather than truncating (TL5) |
| TL-T10 | quantities in different units of one kind normalise and sum; mismatched kinds refuse |
| TL-T11 | on a tree with no claim table, every existing subcommand's output is byte-identical to the golden baseline |

Every one is a pure function call: stdlib, no network, no LLM, no subprocess.

## Sources and Verification

Owning domain is `code` (this project declares no `default_domain`), so the mandatory risk
slot is `## Security and Threat Model` above; this section is recorded for the claims made
about other files. `mkt_check.py#load_ledger/run_ledger/find_table` and its
`marketing.ledger` registration were read in source, as were `sdlc_core.py#sha256_file`,
`portable_check`, `cmd_stale`/`list_guides`, and `shared_files.py#SHARED_FILES` /
`NOT_SHARED_ON_PURPOSE`. The nanopublications and truth-discovery convergences were
confirmed by search and are cited, not reproduced.

## Diary / Current State

**2026-08-01 — split out of F-024 by its design review.** The reviewer ruled that F-024's
"hold a claim with its own provenance" MISSING row was wrong — marketing's evidence ledger
already owns the shape — and that a component with two consumers and its own data model
owes its own analysis under `architect.md` §4. The chosen cut in F-024 (method+storage /
index+checks) ran *across* this component rather than around it. Two further repairs the
same review forced are already in the design above: the id excludes the claim text (keying
on it defeated the idempotency it was introduced to give), and the ladder is total across
all ten provenance pairs (three cells, including `RULING × RULING`, were silent).

**Next step:** F-024's revision lands first, since it is what states how the ledger is
consumed; implementation of this component follows immediately after.
