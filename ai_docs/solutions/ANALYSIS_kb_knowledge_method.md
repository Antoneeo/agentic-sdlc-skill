---
id: F-024
feature: kb Knowledge Method (the topic graph over a governed corpus)
status: IN_PROGRESS
level: L3
start_date: 2026-08-01
end_date:
---
# Feature Analysis: kb Knowledge Method

## Objective

`kb-agentic` ships three method files that state verdicts and rules and contain no
method:

- `taxonomy.md` rules every concept EXISTS / INADEQUATE / MISSING without saying how
  concepts are derived from a corpus, or what is searched to earn a MISSING.
- `distillation.md` lists four rules and no procedure.
- `reconciliation.md` says "determine which document represents the most recent or
  user-confirmed source of truth" without saying how, which is the instruction to guess
  in silence.

The distribution is therefore well-formed and cannot do its job. The owner has held the
release of all three packages until it can: F-022 is `DONE, HELD` for this reason.

**What kb is for**, from the owner's own account: ingest commercial and technical
specifications and act as a second brain over them — catalogue, summarise, answer.
Explicitly **not** necessarily upstream of software: it may stop at planning figures
(effort, duration, resources), at producing a presentation, or at evaluating a newly
arrived specification against what is already known.

This feature supplies the missing method: a **governed corpus**, a **topic graph oriented
by abstraction** over it, and the mechanical checks that keep the two aligned. The
assertions themselves — their schema, their provenance and what happens when two of them
disagree — are a component with two consumers and are specified in
`ANALYSIS_claim_ledger.md` (F-025); this analysis is that component's first consumer and
does not restate it.

## Feature Vision

**Expected benefit.** kb stops being a renamed copy of the code skill and answers the
question it exists for: *what do we already know about this, how sure are we, and where
did it come from?* The success signal is the acceptance bar the owner set — a real corpus
ingested end to end, and the planning and evaluation questions answered from the graph
rather than by re-reading the documents.

**Alignment.** `project_vision.md` v7 admits a knowledge sibling on its merits (Goal 7,
Actor 4 *Practitioner in a non-code domain*) on the condition that it adds **no capability
the family lacks**. The Capability Ledger below honours that literally: of six
capabilities, two already exist and are used as they are, three are INADEQUATE and are
extended rather than rebuilt, and the one genuinely new thing was extracted into F-025
because a second lens already half-owns it.

**Non-Goals — all four run.**

| Non-Goal | Verdict |
|---|---|
| *Not a work-management system* | **Ran, and it removed features.** See the four consequences below |
| *No ceremony ratchet* | **Cost declared, owner acceptance open.** See the budget below |
| *One triage authority per kind of work* | **Satisfied.** The five placement verdicts classify *concepts*, not units of work; kb's Rule Zero remains the only triage of what to do about them, and `architect.md`'s ledger verdicts govern components, a different subject |
| *No coupling to another tool's formats* | **Satisfied.** SKOS/ISO 25964 (polyhierarchy), truth discovery (evidence-weighted provenance) and nanopublications (the atomic assertion) are cited as convergences; no external schema, vocabulary or file format is emitted or parsed. If any of them changed tomorrow, nothing here changes |

The work-management clause defines a record of work by *the question answered*, adds that
it makes no difference whether the answer is stored or **derived on demand**, and states
that a view **collecting each document's own state into one surface is itself the
forbidden capability**. Four consequences:

1. The design carried a `mentions:` field whose stated purpose was a work queue
   ("concepts named by 3 nodes and never described"). **Removed**, field and framing both.
2. `topics/INDEX.md` carries **slug, description and parents only**. It is a router, not
   a status board.
3. No command aggregates `gaps` across nodes.
4. **No command aggregates `coverage` either, and `coverage` is not stored.** An earlier
   draft reported a subtree distribution (`3 FULL / 2 PARTIAL / 1 STUB`); that is exactly
   the readiness board the clause's own amendment record names as forbidden. `coverage` is
   now computed for **one** node when that node is checked, and never collected.

**Ceremony budget — declared; `## The admission test` makes omission resolve against the
proposal.** This lands on **L3 only** for adopting the graph. What an **L2** knowledge
edit pays once it exists, stated honestly rather than claimed to be zero: adding one claim
row requires an id, which is a hash over the source path and locator — supplied by
`sdlc_check.py claim-id`, so it is a command, not arithmetic by hand.

| Added | Cost | Paid by |
|---|---|---|
| `topics/<slug>.md` (6 frontmatter keys + one claim table) | one file per topic | replaces free-form notes, which cost more to reconcile than to write |
| `corpus/` with content-addressed originals | one copy per source | it *is* the fidelity discipline this lens answers to; without it kb has nothing to be faithful to |
| `graph` check | one command at closure | **removes** re-reading the corpus to learn whether the base is self-consistent |
| the three method files | rewritten, not added — read cost roughly unchanged | — |

Removed in exchange: the `mentions:` field, a second dispatch mechanism, a persisted
`.kb/graph.sqlite`, and subtree aggregation — **all of which are removals of unshipped
design, not of shipped ceremony**. The removal column is therefore empty of real cost, so
this proposal rests on the explicit-owner-acceptance branch of the clause. **That
acceptance is the open item and is the owner's to give.**

## Use Cases

- **UC1 — Ingest.** I hand over a set of specifications and get a graph in which each fact
  is attributable to the page it came from, so any answer can be defended later.
- **UC2 — Plan.** I ask what effort, duration and resources the corpus implies and get
  figures that aggregate, each with its source.
- **UC3 — Evaluate.** I hand over a *new* specification and am told what it confirms, what
  it refines, and what it contradicts — the contradiction surfaced, never silently
  resolved.
- **UC4 — Trust.** I hand over a newer version of a document I already gave, and the base
  tells me which claims are still bound to the version it superseded.

UC4 is stated in terms of **supersession, not byte drift**: `corpus/given/` is
content-addressed, so an original's bytes never change and a hash-drift detector could
never fire on it. What changes is which version is current, and that is what the check
must see.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| hold assertions with provenance and reconcile two that disagree | **INADEQUATE**, and extracted | `mkt_check.py#load_ledger/run_ledger` (portable check `marketing.ledger`) owns the row shape; F-025 `ANALYSIS_claim_ledger.md` covers the gap | re-read `run_ledger`: ids, classes, sources, duplicate and dangling-reference detection. **Gap:** no locator, no validity scope, no typed quantity, no relationship form, no reconciliation. Extracted rather than built here because a second consumer exists today |
| address a source by content and detect that it has been superseded | **INADEQUATE** | `sdlc_core.py#sha256_file` + the `.sources/<slug>-<hash8>` convention in `guides.md`; the **detector is new** and lives in the kb overlay | re-read `cmd_stale`: it iterates `list_guides`, which globs `reference/GUIDE_*.md` only, so nothing shipped looks at any other location. What is reusable is the helper and the naming convention — not the engine |
| **extend the validator with a domain command without touching the shared spine** | **INADEQUATE** | `mkt_check.py` is the pattern; there is no extension seam in the core | re-read `sdlc_core.py`: `add_subparsers(dest="cmd", required=True)` and a hard-coded dispatch table, and the regenerate-and-compare checks name three files literally. So an overlay cannot *hook* `index`/`validate`/`check` — it must **intercept and reimplement** them, exactly as `mkt_check.py` does while forwarding only `stale/mark/gate/orient/plan` |
| generate an index and prove mechanically it was not hand-edited | EXISTS (pattern) | `cmd_index` + the `norm_text(read) != norm_text(build)` checks in `cmd_validate` | re-read all three occurrences. The pattern is the poka-yoke and is reused verbatim; only the emitter for `topics/` is new, and it belongs to the overlay per the row above |
| run parallel subagents over a work set, resumably, with one writer per artifact | EXISTS | `dispatch.md` + `PLAN_[topic].ledger.json`; kb already claims `subagent_dispatch` | re-read `dispatch.md`: orchestrator loop, skip-if-done, single-writer ownership, resumable. **Its ownership is per PATH**, which constrains the design below (no two agents in one node file) and is why re-parenting is a phase, not an interleaved edit |
| parse a markdown table, stdlib only | EXISTS | `mkt_check.py#find_table` | re-read: header-matched table extraction, already load-bearing for three marketing checks |

## Design

### The two axes

| Axis | What it is | Where it lives |
|---|---|---|
| **abstraction** | topic A is composed of B; B is named here, described there | an **edge** (`parents:`, and a claim's `about`) |
| **coverage** | how much of this topic the corpus actually supports | **computed** for one node, on demand |

### Storage

```
ai_docs/
  corpus/
    given/                          # originals, verbatim, content-addressed
      contract-9a1f2b7c.pdf
      contract-9a1f2b7c.pdf.meta.md # sidecar: the only place a binary carries metadata
    notes/                          # agent-authored markdown, carries frontmatter
    INDEX.md                        # GENERATED from sidecars + note frontmatter
  topics/
    INDEX.md                        # GENERATED: slug | description | parents
    unplaced.md                     # holding pen; nothing ranks it
    pricing.md
```

`corpus/`, not `sources/`: `ai_docs/reference/.sources/` already exists and means *guide
provenance snapshots*. Two directories called sources under one tree is the naming
collision the family's domain-qualification rule forbids.

**Content-addressed originals.** A newer version is an **append**, never an overwrite —
which is what makes "the older claim is recorded as superseded, not deleted" implementable
at all. The link between versions is explicit: the newer sidecar carries
`supersedes: contract-<oldhash>.pdf`. Without that field nothing connects the two files
and UC4 is unanswerable; with it, "which claims still rest on a superseded version" is a
join, and that join is the check.

**`given/` versus `notes/` is a path-level distinction** because a PDF cannot carry
frontmatter. But "`given/` is never edited" is **a check, not a convention**: `cmd_gate`
returns early for everything under the docs root and `cmd_migrate` rewrites `.md` files
inside it, so no shipped tool blocks the write. The sidecar's recorded hash versus the
file is what detects it, and that detector is new code in the overlay — see the ledger row
above, which is why this is not claimed as reuse.

### The node

`topics/<slug>.md`, in a **flat** directory. Hierarchy lives in frontmatter because the
graph grows upward as well as downward: a document arriving next month can reveal a topic
above ten existing nodes, and if the parent were in the path that insertion would move
files and break every reference.

```markdown
---
topic: pricing
description: How the offer is priced — list prices and negotiated exceptions.
parents: [offerta-commerciale, esercizio-operativo]
owns: [pricing/list-price, pricing/negotiated-price]
synonyms: [listino, price list]
gaps:
  - volume tiers above 500 units
status: CURRENT
---

## Claims

<!-- the claim table defined by F-025; this document does not restate its columns -->
```

- **`parents` is a list.** With a single parent, a topic that is legitimately both a
  commercial term and an operations spec sits under one of them, the router descends the
  other branch, finds nothing, and rules MISSING — **satisfying** the "query before
  MISSING" rule while being wrong. Descent follows every parent; cycle and reachability
  checks use the first entry as primary, so the tree properties the checks need survive.
- **No `coverage:` key.** It would be a declared copy of a derived fact, which is the
  same defect that removed hand-written links. It is computed when a node is checked:
  `STUB` no claims; `PARTIAL` claims but `gaps` non-empty or a `CONTESTED` row; `FULL`
  otherwise. Never stored, never in the index, never aggregated (Non-Goal consequence 4).
- **No `refs`/`mentions` keys.** Every edge is derived from the claim rows — the target in
  a claim's `about`, and any `[[slug]]` in claim text. Hand-written links are two copies of
  one fact, and writing the reverse side means editing another agent's file.
- **`status:` keeps the family's document-lifecycle meaning.** Conflict state is per claim
  row, per F-025. The reason is naming, not enforcement: nothing in the spine validates
  `topics/` at all, since `MANIFEST_DIRS` does not contain it — so overloading `status:`
  would not trip a check, it would simply make one key mean two things.
- **Tombstones, never unlink.** Merging or deleting rewrites the node as
  `status: SUPERSEDED` + `redirect_to: <slug>`, body emptied. Dangling edges resolve
  through it, a later re-placed claim lands on the survivor instead of resurrecting a dead
  slug, and the graph keeps a rename history.

### Placement — five verdicts

The router judges semantically; the index narrows candidates and the checks verify
afterwards. No query decides that "listino" and "pricing" are the same concept.

| Verdict | When | Action |
|---|---|---|
| `EXISTS` | a node owns that concept | reconcile into it (F-025) |
| `INADEQUATE` | the node covers the area, the claim is finer-grained | deepen it, or create a child |
| `MISSING` | no node covers it | create under the nearest more-general node |
| `GENERALIZES` | the concept is **more general** than existing nodes | create it and re-parent them under it |
| `UNPLACED` | about no topic — document metadata, a procurement window, a signature | `topics/unplaced.md`. A holding pen: nothing ranks it, nothing counts it |

**`MISSING` may only be declared after querying the graph** — the port of `architect.md`'s
"the map's silence is unread, not empty". Two guards make it mean something:

1. **The router's view of the graph includes what it created earlier in the same batch.**
   Otherwise every node created mid-batch is invisible for the rest of it and the router
   dutifully creates the duplicate the rule exists to prevent. The mechanism is a candidate
   set **held in memory by the router for the batch**; `topics/INDEX.md` is still written
   **once, by the emitter, at the end**. Hand-appending rows to a generated file to keep it
   current mid-batch would invert the family's generated-never-hand-edited invariant, and
   is not done.
2. **Descent follows every parent**, per the polyhierarchy rule above.

**Similar but perhaps not the same → sibling, never a merge.** Same level, `related:` plus
one line stating the distinction; if that line cannot be written they are the same concept
and it is reconciliation instead. Over-merging is the harmful direction — transitive
closure compounds matcher errors and one false link chains unrelated records into a single
cluster. Deferring a merge is only correct if merging happens later, so a
**canonicalization pass** over `related:` pairs is part of this design.

**`GENERALIZES` is an escalation trigger** — re-parenting N nodes changes the data model,
which the triage table makes unconditionally L3, and one that would create a **new root**
reframes the whole base and stops for the practitioner. Before any `parents:` write the
router walks the target's ancestor chain and rejects the verdict if the node appears:
cycles are cheap to prevent and, once created, invisible, because descent is the only
retrieval path.

### Ingestion

Extraction is parallel and read-only; placement is serial. It runs on `dispatch.md`'s
orchestrator and its ledger rather than on a second mechanism: directory-as-state has no
plan validation and no verify step, and its `pending → done` transition is two non-atomic
operations that Windows makes fail where POSIX does not.

`dispatch.md` is a SHARED file and its declared trigger is an L3 with an approved design;
routine corpus ingestion is not that. **Legalising it is not done by editing the spine.**
The kb overlay states the local rule: an ingestion plan is authored by the orchestrator
from the corpus manifest (not independently), one task per source, and each task's
mandatory `verify` is *"the claim rows produced parse, and every `source` resolves under
the docs root"*. If that proves insufficient, amending `dispatch.md` is a separate change
with a three-distribution propagation cost, and is not smuggled in here.

Three roles, and the file-ownership rule that makes them safe — `dispatch.md`'s single
writer is **per path**, so no two agents may hold one node file:

- **Extractors** read one source each and emit claim rows. Structurally incapable of
  writing to the graph: read-only tools, one output path.
- **The router** is the only writer of node creation and of `parents:`.
- **Writers** fill nodes and never open a foreign one, which derived edges make possible.
  A writer that discovers mid-fill that its claim belongs elsewhere emits a reopen record;
  it may neither move it itself nor drop it.
- **Re-parenting is a router-only phase with no writers running.** `GENERALIZES` writes
  `parents:` into existing nodes, and if a writer were filling one of those files at the
  time, two agents would hold one path — the exact guarantee `dispatch.md` gives and this
  design must not spend.

### The index, and why there is no database file

`topics/INDEX.md` and `corpus/INDEX.md` are generated. They are what the router descends
and the only durable derived artifacts, and each is verified by the same rebuild-and-diff
the spine applies to its own three — implemented in the overlay, because the spine's
checks name their three files literally and the spine is not touched.

The query accelerator for the checks is `sqlite3.connect(":memory:")`, rebuilt per run. A
gitignored binary would be the one derived artifact in the family that cannot be verified
by regenerating it, and a torn one reports green — a crash mid-rebuild leaves a file that
opens fine and answers "0 broken refs, 0 orphans" because the rows are not there yet. In
memory it is not an artifact at all.

### Where provenance is owned

Claim rows in `topics/` own it. A kb `ANALYSIS`'s `## Sources and Verification` section
**cites** the nodes and sidecars the unit rests on; it does not restate their rows. Two
copies of a provenance table in one project is the restated-fact finding `review.md`
already defines, and the owning document is named here so the second copy never gets
written.

## Impact

Paths relative to `distributions/kb-agentic-skill/skills/kb-agentic-skill/` unless stated.

**No file in `shared_files.py#SHARED_FILES` is touched** — not `sdlc_core.py`, not
`dispatch.md`, not the shared batteries. A knowledge-domain directory entering the
byte-identical spine would make the code and marketing distributions manifest it. The
drift guard verifies this at closure.

| Path | Change | Responsibility | Why it changes |
|---|---|---|---|
| `taxonomy.md` | MODIFY | placement: five verdicts, semantic descent, conservative sibling, guarded re-parent, canonicalization pass | today it states verdicts with no derivation |
| `distillation.md` | MODIFY | what a claim is, the locator grammar, how a source becomes rows | today it is four rules and no procedure |
| `reconciliation.md` | MODIFY | points at F-025's ladder and states the kb-specific part: which rows address one subject | today it instructs a silent guess |
| `templates.md` | MODIFY | node template, corpus sidecar template. *(The risk-section defect — the ANALYSIS template emitted the code domain's `## Security and Threat Model` while `DOMAINS["knowledge"]` requires `## Sources and Verification`, so no kb ANALYSIS from the template could pass kb's own validator — was **already repaired** on this branch; the kb battery is green.)* | authors need the exact shapes, or they invent them |
| `SKILL.md` | MODIFY | Write Triggers for `topics/` and `corpus/`; pointers; the ingestion-plan authoring rule; the `## Sources and Verification` citation rule | a destination with no trigger row gets created twice under two names |
| `scripts/sdlc_check.py` | MODIFY | **intercepts and reimplements** `index`, `validate` and `check`; adds `graph` and `corpus`; forwards `stale/mark/gate/orient/plan` unchanged. Overlay functions are named `kb_*`, never `cmd_index`/`cmd_validate` | there is no subparser hook in the core; and `from sdlc_core import *` means a same-named function would silently rebind what the SHARED battery calls as `sc.cmd_index` / `sc.cmd_validate`, producing per-distribution divergence from an unchanged file |
| `scripts/kb_graph.py` | ADD | node parsing, derived edges, in-memory graph, the six checks | keeps the entry point thin enough to read |
| `scripts/test_kb_graph.py` | ADD | the battery | a check with no test is a claim |
| `scripts/test_golden_regression.py` | MODIFY | add `graph` and `corpus` to `COMMANDS` | this harness is deliberately not shared *because* its job is to freeze the subcommands **this** distribution ships; a new command outside `COMMANDS` is a command the harness stopped freezing |
| `scripts/fixtures/golden_baseline.txt` | MODIFY | re-record, with the two new commands appended | the transcript is the baseline; the existing lines must come back byte-identical |
| `ENFORCEMENT.md` | MODIFY | CI recipe gains the `graph` step | closure must be verifiable in CI |
| `ai_docs/solutions/ANALYSIS_claim_ledger.md` *(repo root)* | ADD | the component this consumes | `architect.md`: the two analyses name each other |
| `ai_docs/strategic/architecture.md` *(repo root)* | MODIFY | Component Map rows: topic graph, corpus store, claim ledger | components were born |

Already applied on this branch, recorded so the map matches HEAD rather than the state at
drafting: the `templates.md` risk-section repair, the F-024 registry row in
`ai_docs/audit/handoff.md`, and this document. `ai_docs/vision/roadmap.md` is deliberately
**not** touched — its Write Trigger is bootstrap, not one row per feature, and editing a
Vision document requires re-running the standing blind battery; its staleness is tracked
separately.

**Blast radius — the real consumer set of `sdlc_check.py`.** `index` is the one existing
subcommand whose implementation changes, so every caller of it is enumerated:

| Consumer | Effect |
|---|---|
| `distributions/kb-agentic-skill/scripts/init.js` — runs `sdlc_check.py index --root <cwd>` on **every install** | must stay byte-identical on a tree with no `topics/`; asserted by TS-K7 |
| `scripts/test_golden_regression.py` + `fixtures/golden_baseline.txt` | the frozen transcript; existing lines byte-identical, new commands appended |
| `test_skill_invariants.py`, `test_docs_root.py`, `test_domain_rules.py` (SHARED) | call `sc.cmd_index` / `sc.cmd_validate` off the module — which is why overlay functions are `kb_*` and interception happens only in `main` |
| `ENFORCEMENT.md` CI recipe, and any project running `sdlc_check.py check` | unchanged command names and exit codes |

The extra `topics/INDEX.md` line is emitted **only when `topics/` exists**, so a tree
without one produces identical output.

## Security and Threat Model

Surfaces: **filesystem** (new directories, path-valued fields) and **external input
parsing** (the corpus is untrusted third-party documents). No network, no authN/authZ, no
cryptography beyond content hashing. The validator stays stdlib-only and offline.
Claim-row threats (traversal via `source`, laundered `DERIVED`, forged provenance,
conflict laundering, adversarial table cells) are owned by F-025 and not restated.

| # | Threat | Mitigation | Test |
|---|---|---|---|
| TK1 | **Path traversal via extracted text.** `parents`, `about`, `related` and `redirect_to` are written by an agent reading hostile documents into files a later stage opens | every path-valued field through `confine_under(root, v)`; every slug must match `^[a-z0-9][a-z0-9-]{0,63}$` **and** resolve to an existing node or tombstone. `unplaced` obeys the same grammar, which is why it is not `_unplaced` | TS-K6 |
| TK2 | **Stale corpus.** A superseded source leaves claims resting on a version no longer current, mechanically indistinguishable from correct | the newer sidecar's `supersedes:` links the versions; the `corpus` check reports every claim whose `source` names a superseded original. Not hash drift — content addressing means the old bytes never change | TS-K4 |
| TK3 | **A node that survives its sources.** Deleting a `corpus/` file leaves claims whose origin cannot be reopened, which is model knowledge by another route | a `source` path that does not resolve is an error, not a warning | TS-K4 |
| TK4 | **Silent graph partition.** A cycle or a bad re-parent detaches a subtree; since descent is the only retrieval path, every future claim about it returns MISSING and it is rebuilt in parallel | ancestor walk refuses the write; unreachable-from-root is a check error, not just "cycle" | TS-K5 |
| TK5 | **Resource exhaustion.** A flat `topics/` with thousands of files plus a graph walk | the walk is O(nodes+edges) in memory; `cmd_migrate`'s dry run gets slower, no check breaks. Bounded and stated, not eliminated; no test, and that is a deliberate limit rather than an omission | — |

"No security impact" is not claimed: TK1 is a real traversal surface this feature
introduces, which is why confinement is a check rather than a convention.

## Action Plan

- [x] Register F-024: workstream registry row
- [x] Repair the kb ANALYSIS template's risk section (pre-existing defect); battery green
- [x] Design review gate, round 1 — FAIL, 14 BLOCK; extracted F-025, revised this document
- [ ] Design review gate, round 2 on the revised pair
- [ ] Node and corpus-sidecar templates in `templates.md`
- [ ] Rewrite `taxonomy.md`, `distillation.md`, `reconciliation.md`
- [ ] Wire `SKILL.md`: Write Triggers, pointers, ingestion-plan rule, citation rule
- [ ] `kb_graph.py` + the overlay's `index`/`validate`/`check`/`graph`/`corpus`
- [ ] `test_kb_graph.py`; re-record the golden baseline; three batteries + drift guard
- [ ] Ingest a real corpus supplied by the owner; answer UC2 and UC3 from the graph
- [ ] Closure: `check` CLEAN, Component Map rows, ADR for the topic-graph decision

## Test Strategy

Every entry is a stdlib call against a fixture tree — no network, no LLM, no subprocess.
Behaviours that live in doctrine rather than in code are listed separately and honestly.

| Id | Asserts | Covers |
|---|---|---|
| TS-K1 | a node with two `parents` is reached by descending **either** branch | the polyhierarchy repair; without it MISSING is declarable while wrong |
| TS-K2 | derived edges: a claim naming `-> phase-1` puts the node in phase-1's inbound set with **no write to phase-1** | the property that makes parallel writers safe |
| TS-K3 | `coverage` is computed, absent from frontmatter and from `topics/INDEX.md`, and no command aggregates it | Non-Goal consequence 4 |
| TS-K4 | a claim on a superseded original is reported; an unresolvable `source` errors | TK2, TK3, UC4 |
| TS-K5 | a re-parent that would close a cycle is refused; an unreachable node errors | TK4 |
| TS-K6 | a traversing `parents`/`redirect_to` is refused; a malformed slug is refused; `unplaced` passes | TK1 |
| TS-K7 | on a tree with **no** `topics/`, `index`, `validate` and `check` produce byte-identical output to the golden baseline | the non-regression guarantee for every existing kb project and for `init.js` |
| TS-K8 | a tombstoned slug resolves; a re-placed old claim lands on the survivor | merge must not resurrect dead slugs |
| TS-K9 | quantities of one kind normalise and roll up; a parent contradicting its children's sum is reported | UC2, the acceptance bar |
| TS-K10 | overlay functions are named `kb_*`; `sc.cmd_index` and `sc.cmd_validate` still resolve to the core's | the shadowing hazard the shared batteries would otherwise hit |
| TS-K11 | the generated `topics/INDEX.md` and `corpus/INDEX.md` fail the check when hand-edited | the generated-never-hand-edited invariant, in the overlay |

**Not covered by a test, and named rather than implied:** the placement verdicts and the
similarity judgement are semantic, so they are exercised by behavioural evals under
`evals/scenarios/`, not by the battery; TK5 is a stated bound with no test. F-025 carries
the tests for the claim schema, the ladder and scope arithmetic.

## Sources and Verification

Owning domain is `code` (this project declares no `default_domain`), so the mandatory risk
slot is `## Security and Threat Model` above. Recorded here because the distinction is the
point of the multi-domain rule: the documents this feature teaches kb to write owe
`## Sources and Verification`, and they satisfy it by **citing** claim rows rather than
restating them.

Verification of the claims made about other files: `taxonomy.md`, `distillation.md`,
`reconciliation.md` read in full; `MANIFEST_DIRS`, `CANONICAL_STATES`, `GENERATED_DOCS`,
`SHARED_FILES`, `NOT_SHARED_ON_PURPOSE`, `add_subparsers`, `cmd_stale`/`list_guides`,
`sha256_file`, `confine_under` read in source, not recalled; the `## Non-Goals` clause
quoted verbatim from `vision/project_vision.md`; `mkt_check.py`'s ledger confirmed as the
prior art the design review named. Three independent adversarial reviews preceded this
document and a fourth ruled on it; every structural decision above is a survivor of one or
a repair it forced.

## Diary / Current State

**2026-08-01 — analysis opened, reviewed, and rewritten.** Design elicited with the owner,
then attacked by three reviewers (concurrency, knowledge model, family fit) before this
document existed; the architecture survived, the schema did not, and the root defect was
declaring the claim the unit of reconciliation while storing provenance per node.

The design review gate then returned **FAIL** on the first draft with 14 BLOCK. Substantive
repairs, all applied above: the "hold a claim with provenance" MISSING row was **wrong** —
marketing's evidence ledger already owns the shape — so the component was extracted as
F-025; the claim id keyed on text defeated its own idempotency argument; `cmd_stale`
cannot see the corpus, so row 1 is INADEQUATE and the detector is new; there is no
subparser hook in the core, so the overlay must intercept `index`/`validate`/`check` like
`mkt_check.py`, and its functions must be `kb_*` or they rebind what the shared batteries
call; content-addressed originals made UC4 and TK2 unreachable as written, now restated as
supersession; the subtree coverage distribution was a forbidden readiness board;
re-parenting put two agents in one file; `init.js`, the golden harness and its baseline
were missing from the Impact.

Two review findings were **rejected as artifacts of my own concurrent edit**: the reviewer
read `templates.md` and `handoff.md` after this session had already repaired them and
reported the ANALYSIS's account of the prior state as fabricated. The process lesson is
real and is the reason both rows now record what is already applied: **do not run a review
against a tree you are still editing.**

**Next step:** round 2 of the design review on this document and F-025 together, then
Unit 1.
