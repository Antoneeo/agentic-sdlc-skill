---
id: F-025
feature: Claim Ledger (assertions with provenance; conflicts held open, never auto-resolved)
status: PLANNED
level: L3
start_date: 2026-08-01
end_date:
---
# Feature Analysis: Claim Ledger

## Objective

Two lenses of the family need the same thing and neither has all of it: a table of
**individual assertions**, each bound to a reopenable source location and a provenance,
with a stated discipline for what happens when two of them disagree.

- **Marketing has the row shape.** `mkt_check.py#load_ledger/run_ledger` reads
  `id | claim | class | source` rows, validates class and confidence, and detects
  duplicate ids and dangling `[EV-nn]` references — registered as the portable check
  `marketing.ledger`, offered by its own docstring "to documents owned by ANOTHER
  domain". What it has no notion of: a claim true only in a window, a typed quantity,
  a relationship, or two rows that contradict each other.
- **Knowledge needs the rest** (F-024): a second brain over supplied specifications is a
  corpus of assertions whose worth differs by where they came from, and whose
  contradictions are the most valuable thing it can surface.

**Contract, stated without naming either consumer:** *hold assertions, each bound to a
reopenable source location and a provenance; keep every disagreement visible with both
sides intact until a fact resolves it; and never resolve one silently.*

**The design principle, owner-set (2026-08-01):** the machine **detects and holds**
conflicts; it never decides them. Resolution comes only from **new information** — a
newer source, or a fact the practitioner knows that the corpus lacks. A practitioner's
preference is not a fact: a ruling without stated grounds is rejected exactly as an
agent synthesis without sources is. An earlier draft carried a ten-cell precedence
ladder that decided winners automatically; review showed it needed inputs the rows do
not carry, produced order-dependent outcomes on three-way conflicts, and in one cell
destroyed evidence. Dropped whole, not repaired — deciding was the defect, not the
arithmetic.

## Feature Vision

**Expected benefit.** An answer built from the ledger can be defended: every figure
traces to a page, and every contradiction is either resolved by recorded new information
or is sitting in front of the practitioner, both sides intact. **Alignment**: Goal 7
admits a sibling only if it adds no capability the family lacks; this component exists to
prevent a *second* implementation of what marketing already half-owns — the same rule
applied inward. It also restates the family's standing pairing: **the agent judges, the
machine verifies** — classification of two claims is judgement; integrity of what was
classified is arithmetic.

**Non-Goals, all four run:**

| Non-Goal | Verdict |
|---|---|
| *Not a work-management system* | **Satisfied.** A claim describes a subject, never a unit of work. Conflict findings are per-document validator findings like any other error; the batch escalation at the end of an ingest presents the conflicts *of that run*, which is reporting a command's own result, not collecting state across documents into a standing surface |
| *No ceremony ratchet* | **Satisfied at L1 by construction** (owner ruling 2026-08-01): the `id` column is optional when writing by hand — the validator computes and fills it. An L1 note edit pays nothing new. The L3 adoption budget is in F-024, which owns the consumer surface |
| *One triage authority per kind of work* | **Satisfied.** Classifying two assertions is not triaging work |
| *No coupling to another tool's formats* | **Satisfied.** Converges with nanopublications (assertion+provenance atomic) and truth discovery (evidence over channel); emits and parses no external format |

## Use Cases

- **UCL1** — I record an assertion and later reopen exactly the place it came from.
- **UCL2** — A second source says the same thing and the base gets *stronger*, not longer:
  one row, two sources.
- **UCL3** — Two sources disagree and I am shown both, with sources, dates and
  provenances — never handed one of them silently.
- **UCL4** — I resolve a contradiction by stating what I know, that fact is recorded, and
  I am not asked again **unless new information arrives** — in which case the question
  returns carrying my recorded grounds, so I decide with both in view.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| hold rows of claims with id, source and class; detect duplicate ids and dangling refs | **INADEQUATE** | `mkt_check.py#load_ledger/run_ledger` (portable check `marketing.ledger`) | re-read: validates FACT/BENCHMARK/ASSUMPTION, confidence, duplicate ids, `[EV-nn]` resolution. Gap: no locator, no validity scope, no typed quantity, no relationship form, no conflict state |
| parse a markdown table, stdlib | **INADEQUATE** | `mkt_check.py#find_table` — the pattern is right, but the function lives in a distribution kb cannot import (`mkt_check.py` is `NOT_SHARED_ON_PURPOSE`, and nothing under `SHARED_FILES` carries it) | the kb entry point carries its own copy of the ~20-line pattern, and the copy is **declared here as a cost**: promoting `find_table` into the spine would be a SHARED change with three-distribution propagation, deliberately not spent for one helper |
| hash a file and re-verify it | EXISTS | `sdlc_core.py#sha256_file` | re-read: four lines, already the guide-snapshot mechanism |
| offer a check written in one lens to documents owned by another | EXISTS | `sdlc_core.py#portable_check` + `declared_checks`/`run_portable_checks` | re-read: opt-in via `checks:`, findings never authority — the seam through which a marketing document can later import the claim checks |
| **hold a disagreement open with both sides intact, resolvable only by recorded new information** | **MISSING** | — | document-level supersession exists (`CANONICAL_STATES` has SUPERSEDED; `mkt_check.py` validates a `supersedes:` field) but nothing anywhere holds two *claims* in conflict: no conflict state, no escalation form, no ruling record. Searched the spine and all three overlays for a claim-level conflict/contested/ruling construct — the words appear only in kb's template comment, backed by no procedure |

The MISSING row is the new component. Everything above it is generalized or reused.

## Design

### The row

A claim table under a `## Claims` heading, fixed columns:

| id | claim | valid | qty | about | source | prov | state |
|---|---|---|---|---|---|---|---|
| c7f3a91b0e42 | List price of module A is 12000 EUR | until 2026-03-01 | 12000 EUR cost | - | corpus/given/contract-9a1f2b7c.pdf#p=17@412-509 | GIVEN | OK |
| 4d20be71c8a9 | List price of module A is 15000 EUR | from 2026-03-01 | 15000 EUR cost | - | corpus/given/amendment-3e8d1a04.pdf#p=2@88-140 | GIVEN | OK |

- **`id`** — first 12 hex of `sha256(source_path + "#" + locator)`. **Optional when
  authoring**: the validator's fill step computes and writes it (the L1 rule). Fixed at
  first insertion; on a corroborated row it keeps the **first** source entry, which makes
  recomputation well-defined. The claim text is deliberately excluded — an LLM
  re-extraction paraphrases, and a text-keyed id would re-insert the same assertion under
  a new hash.
- **the locator is deterministic from the document, never invented by the extractor.**
  Grammar, closed: `p=<n>@<start>-<end>` (page + character offsets in that page's
  extracted text), `L<a>-<b>` (line-addressed files), `Sheet<s>!<cell>` (spreadsheets).
  An earlier draft let the extractor mint sub-page labels (`p=17a`); that reintroduced
  through the locator the same instability the id had just evicted from the text — a
  second run orders the assertions differently and every label moves. Character offsets
  are a property of the stored bytes: the same sentence has the same offsets whoever
  extracts it, however many times. Two independent extractions of one assertion therefore
  collide on the same id, which is the dedup working.
- **`valid`** — `-` (unbounded), `from X`, `until X`, `from X until Y`, `if <condition>`.
  **Half-open: `from` inclusive, `until` exclusive**, so `until 2026-03-01` and
  `from 2026-03-01` do not overlap — the two most common rows in any commercial corpus
  must not produce a boundary-day conflict. `if <condition>` is free text and therefore
  treated as overlapping everything: undecidable coexistence is surfaced, not assumed.
- **`qty`** — `-`, or `<value> <unit> <kind>`, kind ∈ `effort | cost | duration | count`.
  `effort`, `duration`, `count` normalise arithmetically (days/weeks/FTE-months to one
  unit). **`cost` normalises only within one currency**: an offline stdlib validator has
  no exchange rates, so a mixed-currency comparison refuses rather than inventing one.
- **`about`** — `-`, or `<predicate> -> <slug>` for a claim about a relationship; stored
  once under the subject, the reverse direction computed by the consumer's index.
- **`source`** — `<path>#<locator>`; corroboration appends `; <path>#<locator>` entries.
  Every path resolves under the docs root and passes `confine_under`. **Every provenance
  class has a real file**: `GIVEN` points into `corpus/given/`, and `ELICITED`, `DERIVED`
  and `RULING` point at notes in `corpus/notes/` — a spoken fact is transcribed, a
  synthesis declares `derived_from:`, a ruling is a note (below). An earlier draft made
  `source` file-only for GIVEN and left the other three unresolvable, which the "source
  must resolve" check would have rejected wholesale.
- **`prov`** — `GIVEN | ELICITED | DERIVED | RULING`. Not a rank. It is **information
  shown to whoever resolves a conflict**, never an input to an automatic decision.
- **`state`** — `OK`, `CONTESTED <id>[,<id>…]`, `SUPERSEDED <id>`. Per claim, never per
  document. `CONTESTED` lists *every* counterpart, so a three-way conflict is one set
  seen whole, not three pairs evaluated in some order.

### Reconciliation — the agent classifies, the machine verifies

When a new claim addresses a subject an existing row already addresses, the **agent**
classifies (this is semantic judgement; no query performs it):

| Outcome | When | Action |
|---|---|---|
| **new** | nothing on that subject | insert |
| **corroboration** | same assertion, different source | append the source. **Never a second row** |
| **refinement** | strictly more precise, not contradictory ("Q1" → "15 March") | new row; old row `SUPERSEDED <new-id>`, text intact |
| **coexistence** | incompatible only if scopes overlapped, and they do not | both rows stay `OK` |
| **conflict** | incompatible, scopes overlap | **all** rows in the conflict set marked `CONTESTED` with each other's ids. Nothing is picked |

The **machine** then verifies what was classified — every check a pure function in the
consumer's entry point:

- ids recompute from `source#locator` (first entry); mismatch is an error
- every `source` resolves under the docs root, through `confine_under`, fail closed
- `DERIVED` without `derived_from:` in its note is an error (laundered synthesis)
- `RULING` without `basis:` in its note is an error (preference disguised as fact)
- `CONTESTED`/`SUPERSEDED` ids that resolve to no row are errors (conflict laundering —
  deleting either side of a recorded disagreement breaks the check, it does not clean up)
- scope grammar parses; `qty` units parse; table arity is exact (a stray `|` errors, never
  truncates)
- advisory, because subject-sameness is judgement: two rows sharing an `owns:` concept,
  overlapping scopes and different `qty` values are flagged as a probable missed conflict

### Conflict resolution — only new information resolves

A `CONTESTED` set is resolved in exactly two ways, and both are **new facts entering the
corpus**, never verdicts:

1. **A new source arrives** (a signed amendment, a newer plan). It is ingested normally;
   the agent re-classifies the set with it in view; what it supersedes is marked, with
   the superseding id recorded.
2. **The practitioner records a ruling** — a note in `corpus/notes/` whose mandatory
   `basis:` states *the fact they know that the corpus lacks* ("client confirmed Q3 by
   phone on 30 Jul", "doc B is an unsigned draft"). The ruling claim enters the ledger
   with `prov: RULING` pointing at that note; the losing rows become
   `SUPERSEDED <ruling-id>`. **No basis, no ruling**: if the practitioner knows nothing
   new, the set simply stays `CONTESTED` — a legitimate, permanent, honest state.

A later source that contradicts a RULING **does resurface** — as a new `CONTESTED` set
that carries the ruling's `basis:` alongside the new evidence, so the practitioner
decides with both in view. Rule-once-forever was in the earlier draft and was wrong on
this corpus's own premise: signed amendments arrive later.

**The escalation form — a conflict question has a legal shape** (owner requirement,
2026-08-01: no useless questions). Escalations are **batched at the end of a run**, never
modal, and each names: the claims in the set, each one's source (reopenable), date and
provenance, and the one-line reason the machine cannot decide ("same subject, overlapping
validity, GIVEN vs GIVEN, no newer source"). A question that cannot fill this form is not
askable — it is the symptom that the answer is in the corpus and was not searched.

## Impact

Paths relative to `distributions/kb-agentic-skill/skills/kb-agentic-skill/`.
**No file in `SHARED_FILES` is touched**, and **no new Python module is added**: the npm
`files` allowlist ships exactly two validator files (`sdlc_check.py`, `sdlc_core.py`),
`ENFORCEMENT.md` promises "copy both", and `test_golden_regression.py` asserts the
two-file recipe — so the ledger's functions live **inside the kb entry point**, which is
`NOT_SHARED_ON_PURPOSE` and already the overlay per `mkt_check.py`'s precedent.

| Path | Change | Responsibility | Why it changes |
|---|---|---|---|
| `scripts/sdlc_check.py` | MODIFY | the ledger section: `parse_claims`, `claim_id`, `scopes_overlap`, `qty_norm`, `check_claims`, the fill step for missing ids, the `claim-id` subcommand | the component's one implementation; a new module would not ship |
| `scripts/test_claim_ledger.py` | ADD | the battery: pure-function tests | a check with no test is a claim |
| `scripts/test_golden_regression.py` + `fixtures/golden_baseline.txt` | MODIFY | `claim-id` enters `COMMANDS`; baseline re-recorded, existing lines byte-identical | a command outside `COMMANDS` is a command the harness stopped freezing |
| `templates.md` | MODIFY | the claim-table template + the ruling-note template (`basis:` mandatory) | authors need the exact shapes |
| `SKILL.md` | MODIFY | `claim-id` in the command list; Write Trigger rows for claim tables and ruling notes | a destination with no trigger row gets created twice |
| `ai_docs/audit/handoff.md` *(repo root)* | MODIFY | F-025's own workstream row | Write Trigger: one row per OPEN workstream |
| `ai_docs/strategic/architecture.md` *(repo root)* | MODIFY | Component Map row | a component was born |

**Sequencing.** The ledger is a *section of the same file* F-024's overlay work modifies,
so the dependency is declared instead of discovered: **this component's functions and
battery land first**, in F-024's first implementation step, then F-024's graph consumes
them — `architect.md` §5 order restored. Marketing's future adoption is out of scope and
its cost is stated: it would either import across distributions (impossible today) or
promote the section into the spine (a SHARED change) — a decision for that unit, not this
one.

**Blast radius.** New functions and one new subcommand inside `sdlc_check.py`; no
existing subcommand changes behaviour on a tree with no claim tables (asserted by the
golden baseline's existing lines). The shared batteries bind `sdlc_core` directly and are
untouched by construction.

## Security and Threat Model

Surfaces: **external input parsing** (claim rows derive from untrusted documents) and
**filesystem** (`source` is a path later stages open). No network, no authN/authZ, no
crypto beyond hashing.

| # | Threat | Mitigation | Test |
|---|---|---|---|
| TL1 | path traversal via `source` — a hostile document yields `../../../.ssh/id_rsa#L1-2`, which checks then open and hash | every path through `confine_under(root, v)` before any open; fail closed, the spine's `distilled_from` precedent | TL-T7 |
| TL2 | laundered synthesis — a DERIVED note with no `derived_from:` enters as if sourced | `check_claims` errors on it; and provenance never auto-decides anything, so a laundered class buys no automatic win | TL-T8 |
| TL3 | forged provenance — claim text edited, or `source` moved to a stronger document, under a kept id | ids recompute from the first source entry; mismatch errors. Text is free to correct (not keyed); *moving the source* is what breaks the hash | TL-T7 |
| TL4 | conflict laundering — deleting one side of a disagreement | `CONTESTED`/`SUPERSEDED` referential integrity: a pointer to a missing row is an error | TL-T8 |
| TL5 | adversarial table cells — a `|` inside a claim splits the row | exact arity enforced; wrong arity errors, never truncates | TL-T9 |
| TL6 | preference disguised as fact — a ruling with no grounds silently ends a real conflict | `RULING` without `basis:` is an error; the losing rows record the ruling id, so the resolution is reopenable and challengeable | TL-T8 |

## Action Plan

- [ ] Ledger section in `sdlc_check.py`: `parse_claims`, `claim_id`, `scopes_overlap`,
      `qty_norm`, `check_claims`, id fill, `claim-id`
- [ ] `test_claim_ledger.py`
- [ ] Templates: claim table + ruling note
- [ ] `SKILL.md` command list + Write Triggers; handoff row; Component Map row
- [ ] Golden: `claim-id` in `COMMANDS`, baseline re-recorded, existing lines byte-identical

## Test Strategy

All pure-function calls, stdlib, no network, no LLM, no subprocess.

| Id | Asserts |
|---|---|
| TL-T1 | id unchanged when claim text is rewritten; id changes when the locator does; **two extractions of one sentence at the same offsets yield one id** |
| TL-T2 | `until X` / `from X` disjoint; `-` overlaps everything; `if` overlaps everything |
| TL-T3 | a three-way conflict yields one `CONTESTED` set listing all counterpart ids on every row |
| TL-T4 | a ruling with `basis:` supersedes its set; a ruling note without `basis:` errors; a later conflicting source re-opens as a new set that references the ruling |
| TL-T5 | corroboration appends a source, id and row count unchanged |
| TL-T6 | missing-id rows are filled deterministically; a filled table re-fills to byte-identical |
| TL-T7 | a traversing `source` is refused; a moved `source` under a kept id errors |
| TL-T8 | `DERIVED` without `derived_from` errors; `RULING` without `basis` errors; dangling `CONTESTED`/`SUPERSEDED` errors |
| TL-T9 | wrong table arity errors, never truncates |
| TL-T10 | effort/duration/count normalise and sum; mixed currencies refuse; mismatched kinds refuse |
| TL-T11 | on a tree with no claim table, every existing subcommand's output is byte-identical to the golden baseline |

## Sources and Verification

Owning domain is `code` (no `default_domain` declared), so the mandatory risk slot is
`## Security and Threat Model` above. Claims about other files, verified in source:
`mkt_check.py#load_ledger/run_ledger/find_table` and the `marketing.ledger` registration;
`sha256_file`, `portable_check`, `confine_under`, `CANONICAL_STATES` in `sdlc_core.py`;
the npm `files` allowlist in `distributions/kb-agentic-skill/package.json`; the two-file
recipe in kb's `ENFORCEMENT.md` and `test_golden_regression.py`. The shared batteries
import `sdlc_core as sc` directly (checked in all five), which is why the overlay cannot
shadow what they test. Convergences (nanopublications, truth discovery) cited, not
reproduced.

## Diary / Current State

**2026-08-01 — extracted by F-024's design review; rewritten after round 2 to the
owner's design ruling.** Round 2 (two lenses: disposition verifier + cold adversary)
broke the automatic precedence ladder beyond repair: cells needed absent columns
(dates, breadth, `derived_from`), symmetric cells had opposite rules, `DERIVED×DERIVED`
destroyed evidence, three-way conflicts were order-dependent, and `RULING×GIVEN` pinned a
ruling against the corpus's own premise that amendments arrive later. The owner then set
the principle this version implements: the machine detects and holds, only new
information resolves, and a ruling is itself a recorded fact (`basis:`) — never a
preference. Same round forced: locator by character offsets (the extractor invents
nothing), every provenance class resolving to a real file, the ledger living inside the
entry point (the npm allowlist ships exactly two validator files), and `claim-id`
entering the golden `COMMANDS`.

**Next step:** round 3 of the design gate on this document and F-024 together — the last
before the cap; open findings, if any, go to the owner.
