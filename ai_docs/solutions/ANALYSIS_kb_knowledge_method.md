---
id: F-024
feature: kb Knowledge Method (the topic graph over a governed corpus)
status: COMPLETED
level: L3
start_date: 2026-08-01
end_date: 2026-08-01
---
# Feature Analysis: kb Knowledge Method

## Objective

`kb-agentic` ships three method files that state verdicts and rules and contain no
method: `taxonomy.md` rules concepts EXISTS/INADEQUATE/MISSING without saying how
concepts are derived from a corpus; `distillation.md` lists four rules and no procedure;
`reconciliation.md` says "determine which document represents the most recent or
user-confirmed source of truth" — the instruction to guess in silence. The distribution
is well-formed and cannot do its job; the owner holds the release of all three packages
until it can (F-022 `DONE, HELD`).

**What kb is for**, from the owner's own account: ingest commercial and technical
specifications and act as a second brain over them — catalogue, summarise, answer.
Explicitly not necessarily upstream of software: it may stop at planning figures
(effort, duration, resources), at a presentation, or at evaluating a newly arrived
specification against what is already known.

This feature supplies the missing method: a **governed corpus**, a **topic graph
oriented by abstraction** over it, and the checks that keep the two aligned. The
assertions themselves — schema, provenance, and what happens when two disagree — are the
**claim ledger**, `ANALYSIS_claim_ledger.md` (F-025): a component with two consumers,
specified there and consumed here, not restated.

**The design principle, owner-set and carried through every piece:** wherever the
earlier drafts had the machine *decide or invent* something — a sub-page label, a
conflict winner, a hierarchy-wide sum, a concurrency guarantee — this version moves that
point onto **a fact of the document or a fact the practitioner knows**. Never onto a
guess, never onto a preference.

## Feature Vision

**Expected benefit.** kb answers the question it exists for: *what do we already know
about this, how sure are we, and where did it come from?* Success signal: the owner's
acceptance bar — a real corpus ingested end to end, and the planning and evaluation
questions answered from the graph rather than by re-reading the documents.

**Alignment.** `project_vision.md` v7 admits a knowledge sibling on the condition it adds
no capability the family lacks. Of the ledgered capabilities, two are used as they stand,
three are extended, one was extracted to F-025 because marketing half-owns it. Nothing in
`SHARED_FILES` is touched.

**Non-Goals — all four run:**

| Non-Goal | Verdict |
|---|---|
| *Not a work-management system* | **Ran; it removed features.** `mentions:`-as-work-queue: removed. Subtree coverage aggregation (a readiness board from admitted fields): removed — `coverage` is computed for one node when that node is checked, never stored, never in an index, never collected. `topics/INDEX.md` carries slug, description, parents and synonyms only — a router, not a status board (synonyms are admitted: they are naming, not work state). `unplaced.md` is a holding pen nothing ranks |
| *No ceremony ratchet* | **L1 free by construction** (owner ruling 2026-08-01): a claim row's `id` is optional when writing by hand — the validator fills it; no new mandatory field, no command to run, and the graph checks never *error* on a hand-edited note (they report). The L3 adoption budget is below, resting on the explicit-owner-acceptance branch — the removals are of unshipped design, so the removal column is honestly empty. **Owner acceptance is the open item** |
| *One triage authority per kind of work* | **Satisfied.** Placement verdicts classify concepts, not work; kb's Rule Zero stays the sole triage — and this feature adds the escalation triggers kb's table was missing (below), rather than citing another skill's |
| *No coupling to another tool's formats* | **Satisfied.** SKOS/ISO 25964, truth discovery and nanopublications are cited as convergences; no external schema or format is emitted or parsed |

**Ceremony budget (L3 adoption).** Added: `topics/<slug>.md` (7 frontmatter keys, 2 more
optional — `related:` on siblings, `redirect_to:` on tombstones), `corpus/` with
content-addressed originals, the `graph`/`corpus` checks at closure, the three method
files rewritten (read cost roughly unchanged). What an L2 pays: writing a claim row —
the id is filled by the validator, so the cost is the row itself. What an L1 pays:
nothing new. Removed in exchange: nothing shipped (the removals are of this feature's
own earlier drafts), so the clause's owner-acceptance branch applies and is awaited.

## Use Cases

- **UC1 — Ingest.** I hand over specifications and get a graph in which each fact is
  attributable to the place it came from.
- **UC2 — Plan.** I ask what effort, duration, resources the corpus implies and get
  figures that aggregate, each with its source.
- **UC3 — Evaluate.** I hand over a *new* specification and am told what it confirms,
  refines, and contradicts — contradictions surfaced, never silently resolved.
- **UC4 — Trust.** I hand over a newer version of a document and the base tells me which
  claims still rest on the version it superseded. (Supersession, not byte drift:
  content-addressed originals never change bytes, so what changes is which version is
  current — and that is what the check joins on.)

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| hold assertions with provenance; keep disagreements open | **INADEQUATE**, extracted | `mkt_check.py`'s evidence ledger owns the row shape; F-025 owns the gap and is built first (same file, declared order) | re-read `run_ledger`; gap and extraction rationale in F-025 |
| address a source by content and detect supersession | **INADEQUATE** | `sha256_file` + the `.sources/<slug>-<hash8>` convention exist for guides; `cmd_stale` iterates `list_guides` (globs `reference/GUIDE_*.md` only) so the corpus detector is **new**, in the overlay | re-read `cmd_stale`/`list_guides`; what is reused is the helper and the convention, not the engine |
| extend the validator without touching the spine | **INADEQUATE** | no seam: `add_subparsers(required=True)`, hard-coded dispatch, three literally-named regenerate-and-compare checks. The overlay **intercepts and reimplements** `index`/`validate`/`check`, forwards `stale/mark/gate/orient/plan` — `mkt_check.py`'s exact pattern | re-read both entry points |
| generate an index and prove it was not hand-edited | EXISTS (pattern) | the `norm_text(read) != norm_text(build)` compare, reused verbatim in the overlay for `topics/INDEX.md` and `corpus/INDEX.md` | re-read the three spine occurrences |
| run subagents over a work set, resumably | **INADEQUATE** | `dispatch.md` + the plan ledger exist and kb claims `subagent_dispatch` — but its loop is **serial by design** ("for each task, in plan order") and its single-writer statement covers the *ledger*, not artifact paths; nothing checks two tasks for disjoint `paths`. An earlier draft called this "per-path single-writer ownership" — that guarantee was never issued | re-read `dispatch.md` in full and `_validate_plan_tasks`; consequence: **ingestion v1 is serial** (below) |
| parse a markdown table | **INADEQUATE** | `find_table` lives in mkt, not importable | F-025 declares the copy and its cost |

## Design

### Storage

```
ai_docs/
  corpus/
    given/                          # originals, verbatim, content-addressed
      contract-9a1f2b7c.pdf
      contract-9a1f2b7c.txt         # STORED canonical extraction: pages separated by
                                    # form-feed; what offset locators address (F-025)
      contract-9a1f2b7c.pdf.meta.md # sidecar: digest, date, `supersedes:` linking
                                    # versions, extractor id+version+normalization
    notes/                          # ELICITED transcriptions, DERIVED syntheses (derived_from:),
                                    # RULING notes (basis:) — every provenance resolves to a file
    INDEX.md                        # GENERATED from sidecars + note frontmatter
  topics/
    INDEX.md                        # GENERATED: slug | description | parents | synonyms
    unplaced.md                     # holding pen; nothing ranks it
    pricing.md
```

**The extraction is a stored artifact, not a runtime step.** Offsets are a property of
the *extracted* text, and extraction differs by extractor — so the extraction is written
once at ingest, content-addressed beside the original, with the extractor identity
recorded in the sidecar. Locators address the stored bytes; the stdlib validator opens
the `.txt` and asserts the span exists; a human opens it and reads the span. A different
extractor later produces a new stored artifact with a new address — a visible
supersession, never a silent re-hash of every id.

**Two digests, deliberately.** `given/` binaries are addressed by **raw-byte** sha256
(`sha256_bytes`, new in the overlay): the spine's `sha256_file` normalizes CRLF→LF —
right for text guide snapshots, wrong for binaries, where a hostile pair differing only
in `0D 0A` vs `0A` would collide. Text files (`notes/`, extractions) keep the
LF-normalized digest so Windows checkouts do not read as drift. The sidecar records
which digest it carries.

`corpus/`, not `sources/` — `reference/.sources/` already means guide snapshots, and one
tree must not hold two directories named sources meaning different things.

**Content-addressed originals; supersession is explicit.** A newer version is an append;
the newer sidecar's `supersedes:` links it to the old file. "Which claims rest on a
superseded version" is a join over that field — the `corpus` check. "`given/` is never
edited" is a **check, not a convention** (`cmd_gate` exempts the docs root and
`cmd_migrate` rewrites `.md` under it, verified — no shipped tool blocks the write; the
sidecar hash detects it). `init.js` does not seed `corpus/` or `topics/`: they are
created by the skill at first ingest, so non-kb uses of the tree never see them.

### The node

`topics/<slug>.md`, flat directory, hierarchy in frontmatter (the graph grows upward:
a later document can reveal a topic above ten existing nodes; flat + `parents:` makes
that insertion an edit, not a file move).

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
<!-- claim table per F-025 -->
```

- **`parents` is a list** (polyhierarchy). With one parent, the router can satisfy
  "query before MISSING" while descending the branch the topic is not under, and create
  the duplicate the rule exists to prevent. Descent follows every parent; cycle and
  reachability checks use the first entry as primary.
- **`owns` grammar**: `<this-slug>/<concept>`, lowercase, `[a-z0-9-]` segments joined by
  one `/`. Not slugs — concept identifiers scoped to the node, so the double-owner check
  compares them exactly. In TK1's confined-field enumeration.
- **No coverage state exists — not stored, not computed.** An earlier draft removed the
  stored key but kept a computed STUB/PARTIAL/FULL per node; the Vision's
  work-management clause closes exactly that escape ("derived on demand and never
  written down" makes no difference), and a whole-tree check printing per-node states
  IS the collected surface. What remains is what the clause admits: `gaps:` declared
  inside each node, describing that document, read when that node is read. The checks
  emit **findings only** — errors and warnings — never per-node status lines.
- **No `refs`/`mentions` keys** — every edge derives from claim rows (`about` targets,
  `[[slug]]` in claim text). `related:` (sibling distinction) is the one hand-written
  link: **one-directional by rule** — only the newer sibling carries it; the reverse
  direction is computed by the index, and the canonicalization pass reads both
  directions from the index, so no cross-file write ever occurs.
- **`status:` keeps the family lifecycle meaning.** Conflict state is per claim row
  (F-025). The reason is naming discipline: nothing in the spine validates `topics/` at
  all (`MANIFEST_DIRS` excludes it — verified), so this is about one key meaning one
  thing, not about tripping a check.
- **Tombstones, never unlink**: merge/delete rewrites the node as `status: SUPERSEDED` +
  `redirect_to: <slug>`, body empty. Dangling edges resolve through it; a re-placed old
  claim lands on the survivor.

### Placement — five verdicts, the router judges, the checks verify

| Verdict | When | Action |
|---|---|---|
| `EXISTS` | a node owns the concept | reconcile into it (F-025) |
| `INADEQUATE` | node covers the area, claim is finer | deepen, or create a child |
| `MISSING` | nothing covers it | create under the nearest more-general node |
| `GENERALIZES` | concept sits above existing nodes | **escalation trigger** (below) |
| `UNPLACED` | about no topic | `unplaced.md`, unranked |

**`MISSING` only after querying the graph** (the port of `architect.md`'s "unread, not
empty"), made real by two guards: the router's candidate set **includes what it created
this run** — held in memory, **rebuilt at start by reading `topics/*.md` frontmatter**
(the files are the state; a crash loses nothing a directory read does not restore), with
`topics/INDEX.md` written once at the end by the emitter and verified by
rebuild-and-diff; and descent follows **every** parent. The index narrows candidates —
including by `synonyms`, which is why they are in it — and the router opens only the
final few nodes.

**Similar-but-maybe-distinct → sibling, never merge** (`related:` + one line stating the
distinction; cannot write the line ⇒ same concept ⇒ reconcile). Over-merging is the
harmful direction — one false link chains unrelated records; a redundant sibling is
cheap to merge later, and the **canonicalization pass** over `related:` pairs is the
place it happens.

**`GENERALIZES` escalates.** Re-parenting N nodes rewrites the graph's shape; kb's Rule
Zero gains the escalation triggers its table was missing (this feature's `SKILL.md`
edit): *changes the topic hierarchy; touches more than one node's frontmatter; creates
or supersedes a node others reference* → L3, declared. A `GENERALIZES` that would create
a new root additionally stops for the practitioner. Before any `parents:` write the
router walks the target's ancestor chain and refuses a cycle; unreachable-from-root is a
check error (descent is the only retrieval path — a detached ring is otherwise invisible
forever).

### Ingestion — serial, on the machinery that exists

**v1 ingests serially.** The parallel topology of earlier drafts rested on a per-path
single-writer guarantee `dispatch.md` never issues (its loop is "in plan order" —
serial; its single-writer line covers the ledger). Correctness first: a serial pass that
never loses a write beats a parallel one that cannot prove it doesn't. Parallel
extraction is future work with its prerequisite named — a disjoint-`paths` check in plan
validation, which is a SHARED change.

Ingesting a corpus **is L3 by kb's own triage table** ("L3 — Major Knowledge Unit /
Corpus: ingesting large document sets"), so `dispatch.md`'s trigger is satisfied as
written: the ingestion plan is derived from this ANALYSIS's Action Plan — never
independently authored — one task per source, each task's `verify` = "claim rows parse;
every `source` resolves under the docs root". No carve-out, no local rule contradicting
a SHARED file (an earlier draft had one; it is gone).

Per run: read source → extract claim rows (locators are character offsets — facts of the
document, per F-025) → route each claim (five verdicts) → reconcile (F-025) → write
nodes → emit indexes → checks. Conflicts accumulate as CONTESTED and are presented
**once, in batch, at the end of the run**, each in the legal escalation form (F-025).
The pipeline never stops mid-run to ask anything.

### The two questions, answered from the structure

- **"What effort was estimated for module X?" (UC2):** select claim rows whose `qty`
  kind is `effort` and whose node or `about` names X; normalise units; sum; show each
  row's source. **No sum along `parents:`** — that edge means "more general than", not
  "part of", and summing along generality produces numbers that lie. An earlier draft
  did exactly that; if composition roll-ups are ever wanted, they need their own
  `part_of` edge, which is future work, named.
- **"What does this new specification contradict?" (UC3):** ingest it; the run's
  reconciliation output *is* the answer — corroborations, refinements, and the CONTESTED
  sets with both sides shown.

### Index and checks — in the overlay, spine untouched

`topics/INDEX.md` and `corpus/INDEX.md` are generated by the overlay's `index`,
verified by rebuild-and-diff in the overlay's `validate`. The in-memory graph for checks
is `sqlite3.connect(":memory:")`, rebuilt per run — a persisted binary would be the one
derived artifact that cannot be verified by regeneration, and a torn one reports green.

The overlay lives **inside `sdlc_check.py`** (two-file validator: npm allowlist, CI
recipe and the golden copied-file test all pin it — verified). It intercepts `index`,
`validate`, `check`; adds `graph`, `corpus`, `claim-id`; and **forwards every spine
subcommand it does not intercept — by iterating the spine's parser, never a hand-copied
tuple.** The tuple is how `mkt_check.py` ships broken today: its `SPINE_COMMANDS` omits
`migrate` while its SKILL.md documents it, and the command dies in argparse (found by
this review; tracked as its own fix). The intercepted commands resolve the docs root
through `sdlc_core.resolve_docs_dir` — so `--docs-dir`, the env seam and the
two-roots-refuse behaviour that `ENFORCEMENT.md` promises "on any subcommand" stay true.
One golden invocation carries `--docs-dir` to freeze that. `ENFORCEMENT.md`'s
"core-alone behaves identically" paragraph is rewritten: for kb it no longer does — the
core alone runs no claim or graph check — and the recipe says so instead of letting CI
copy one file and go silently green.

**Coverage note, stated because it is a real gap:** the shared batteries (seven; six
import `sdlc_core as sc` directly, and `test_skill_invariants` loads the entry point
only to read the profile) keep testing the spine's `cmd_*`, which the overlay cannot
shadow. The overlay's intercepted commands are covered by the new kb battery **through
`main()`** plus the golden transcript, and TS-K10 asserts exactly that path.

Graph checks — findings only, never per-node status lines: broken edge targets;
unreachable-from-root; cycles; double owner (exact compare on the `owns` grammar, plus a
`difflib` near-duplicate warning on description/title similarity — it will not catch
listino/pricing, it catches listino/listini, and the semantic case belongs to the router
evals); CONTESTED integrity incl. symmetry (F-025); claims on superseded sources
(`corpus`).

### Where provenance is owned

Claim rows own it. A kb ANALYSIS's `## Sources and Verification` **cites** the nodes and
sidecars the unit rests on — it does not restate rows (two provenance tables in one
project is `review.md`'s restated-fact finding). The `templates.md` block was converted
to this citation form on this branch (commit `0a1bbae`).

## Impact

Paths relative to `distributions/kb-agentic-skill/skills/kb-agentic-skill/` unless
stated. **No file in `SHARED_FILES` is touched; no file is added to the npm allowlist.**

| Path | Change | Responsibility | Why it changes |
|---|---|---|---|
| `taxonomy.md` | MODIFY | placement: five verdicts, descent over the index, sibling rule, guarded re-parent, canonicalization pass | verdicts exist, method does not |
| `distillation.md` | MODIFY | source → claim rows: what a claim is, offset locators, provenance-to-file rule | four rules, no procedure |
| `reconciliation.md` | MODIFY | points at F-025; adds the kb part: subject-sameness judgement, the batch escalation moment | instructs a silent guess today |
| `templates.md` | MODIFY | node template, sidecar template; **convert `## Sources and Verification` to citation form** (it currently mandates the second provenance table this design forbids) | authors need the shapes; the slot needs one owner |
| `SKILL.md` | MODIFY | Write Triggers (`topics/`, `corpus/`, unchanged-elsewhere rule); **Rule Zero escalation triggers** (hierarchy change, multi-node frontmatter, supersession of a referenced node); command list; the batch-escalation rule (questions only in the legal form, presented at run end) | the table has no escalation triggers today; a destination with no trigger row gets created twice |
| `scripts/sdlc_check.py` | MODIFY | the overlay: F-025's ledger section first, then graph/corpus/index/validate/check interception, `kb_`-prefixed internals for readability | there is no spine seam; two-file constraint |
| `scripts/test_kb_graph.py` | ADD | graph checks battery, driven through `main()` | the shared batteries cannot cover overlay commands |
| `scripts/test_golden_regression.py` + `fixtures/golden_baseline.txt` | MODIFY | `graph`, `corpus`, `claim-id` enter `COMMANDS`; baseline re-recorded, existing lines byte-identical | the harness freezes what this distribution ships |
| `ENFORCEMENT.md` | MODIFY | CI gains the `graph` step; the two-file copy recipe stays true (nothing new to copy); the "core-alone behaves identically" paragraph rewritten to name what the core alone no longer checks | closure verifiable in CI; a CI that copies one file must not go silently green |
| `evals/scenarios/` | MODIFY | placement and similarity scenarios (the semantic behaviours the battery cannot test); the two shipped scenarios for an `architect_pass` kb does not claim are replaced | the design routes semantic checks here by name |
| `CHANGELOG.md` | MODIFY | the release entry — this feature is what F-022's release is held for | release discipline |
| `ai_docs/solutions/ANALYSIS_claim_ledger.md` *(repo root)* | — | the component, named mutually | `architect.md` §4/§5 |
| `ai_docs/audit/handoff.md` *(repo root)* | MODIFY | F-025 row added (F-024's row exists) | one row per open workstream |
| `ai_docs/strategic/architecture.md` *(repo root)* | MODIFY | Component Map rows: corpus store, topic graph, claim ledger | components born |

Not touched, deliberately: `package.json` (nothing new ships), `init.js` (it seeds
neither `topics/` nor `corpus/`; it runs the validator at **project init** via
`kb-agentic-init` — not on npm install — and observes only the exit code, which stays 0
on a tree with no `topics/`), `ai_docs/vision/roadmap.md` (bootstrap-trigger document;
tracked as its own task), the mkt distribution, and every SHARED file.

**Blast radius — consumers of `sdlc_check.py`:** `init.js` (exit code only, unchanged);
the golden harness (extended, existing lines byte-identical); the shared batteries
(bind `sdlc_core`, untouched); CI recipes and user projects (command names and exit
codes unchanged). The `index` output gains lines **only when `topics/` exists**.

## Security and Threat Model

Surfaces: **filesystem** and **external input parsing** (the corpus is untrusted).
No network, no authN/authZ, no crypto beyond hashing; stdlib-only, offline. Claim-row
threats are owned by F-025 (TL1–TL6) and not restated.

| # | Threat | Mitigation | Test |
|---|---|---|---|
| TK1 | path traversal via extracted text in `parents`, `about`, `related`, `redirect_to`, `owns` | slugs match `^[a-z0-9][a-z0-9-]{0,63}$` and resolve to a node or tombstone; `owns` matches its own grammar; every path through `confine_under`, fail closed | TS-K6 |
| TK2 | claims resting on a superseded source, indistinguishable from current | sidecar `supersedes:` + the `corpus` check joins claims to superseded originals | TS-K4 |
| TK3 | a claim whose source cannot be reopened (deleted file — model knowledge by another route) | unresolvable `source` is an error — and every provenance class resolves to a file (F-025), so the check is total | TS-K4 |
| TK4 | silent graph partition (cycle / bad re-parent detaches a subtree forever) | ancestor-walk refusal at write time; unreachable-from-root is a check error | TS-K5 |
| TK5 | resource exhaustion (thousands of flat files + graph walk) | O(nodes+edges) in memory; `migrate`'s dry run slows, nothing breaks; binaries under the docs root are copied with `write_bytes` by `_migration_plan` (verified). Bounded, stated, untested by design | — |

## Action Plan

- [x] Register F-024; repair the kb template risk section; battery green
- [x] Design gate round 1 (FAIL, 14 BLOCK → F-025 extracted) and round 2 (FAIL, two
      lenses → automatic ladder dropped, serial v1, two-file constraint, owner rulings)
- [ ] Design gate round 3 on the rewritten pair — the last before the cap
- [x] F-025 first: ledger section in `sdlc_check.py` + `test_claim_ledger.py` (22 tests)
- [x] Templates: node, sidecar, claim table, ruling note; `## Sources and Verification`
      in citation form
- [x] Rewrite `taxonomy.md`, `distillation.md`, `reconciliation.md`
- [x] `SKILL.md`: triggers, escalation triggers, commands, L1-free rule, no-useless-questions rule
- [x] Overlay: `graph`, `corpus`, `claim-id`, `index`/`validate`/`check` interception;
      `test_kb_graph.py` (17 tests)
- [x] Golden: `COMMANDS` + baseline re-recorded (+9/−0, frozen 1.0 snapshot + containment
      test); three distribution batteries green; drift guard: 15 shared files identical
- [x] End-to-end smoke on a mini corpus: graph/corpus/index/validate/check rc 0; UC2 sums
      by selection; the span check and the digest check each caught a real error on the
      first attempt
- [x] Ingest the owner's real corpus; answer UC2 and UC3 from the graph — **done on
      the Eclosion corpus** (owner: "pesca dal progetto di Eclosion", 2026-08-01).
      Five specifications ingested content-addressed into
      `D:\SoftwareDev\skill_sdlc\kb_field_test_eclosion\`; 7 topics, 26 claims, every
      one bound to a line locator; `check: CLEAN`, graph and corpus consistent.
      **UC2 answered**: power-user storage = 5+150+200 = 355 MB/month, matching the
      document's own declared total, each figure with its source. **UC3 produced a
      real finding**: the scaling strategy (Phase 1 < 100 concurrent) and the
      performance report (200–300 concurrent), same in-document date, GIVEN vs GIVEN
      → CONTESTED pair, escalated to the owner in the legal form — the machine held
      it, decided nothing. During authoring the checks caught two real errors
      (duplicate id from two claims on one line without a distinguishing qty;
      CONTESTED pointers computed without the qty component) and, earlier, a wrong
      span and a fake digest — four catches, zero false positives
- [x] Closure: `check` CLEAN on this repo; Component Map rows (claim ledger, topic
      graph, corpus store); `architecture/ADR_2026-08-01_kb_topic_graph_claim_ledger.md`.
      The capacity CONTESTED was resolved by owner ruling ("alla fine tieni 200-300",
      2026-08-01) with `basis:` = the report measures post-optimization capacity; the
      ruling row supersedes both prior members, per the state machine, and the field
      test re-checks CLEAN

## Test Strategy

Stdlib fixtures, no network, no LLM, no subprocess; semantic behaviours (placement,
similarity) go to `evals/scenarios/`, named as such, not faked as unit tests.

| Id | Asserts |
|---|---|
| TS-K1 | a node with two `parents` is reached descending either branch |
| TS-K2 | after deriving edges for a claim whose `about` names node X, X's file bytes are unchanged (reconciliation's own CONTESTED writes are serial and out of scope here) |
| TS-K3 | the built `topics/INDEX.md` contains no coverage token; no node file carries or gains a `coverage:` key after a full check run |
| TS-K4 | claims on a superseded original are reported; unresolvable `source` errors; a span past the stored extraction's end errors |
| TS-K5 | a cycle-closing re-parent is refused (check half); an unreachable node errors |
| TS-K6 | traversal refused on every TK1 field; `owns` grammar enforced; `unplaced` passes |
| TS-K7 | with no `topics/`, `index`/`validate`/`check` output is byte-identical to the **pre-change** golden baseline; the re-recorded baseline is additions-only line-for-line |
| TS-K8 | tombstone resolves; re-placed claim lands on the survivor |
| TS-K9 | for a parent whose child carries a qty row, the UC2 selection for the parent returns only the parent's own rows |
| TS-K10 | the overlay's `index`/`validate`/`check` are what `main()` reaches; the spine's `cmd_*` remain importable and untouched; every subcommand named in SKILL.md (incl. `migrate`) exits non-2; `--docs-dir` works on an intercepted command |
| TS-K11 | hand-edited generated indexes fail the overlay's rebuild-and-diff |
| TS-K12 | router candidate set rebuilt from frontmatter equals the set before a simulated crash |

## Sources and Verification

Owning domain `code` (no `default_domain`), risk slot above. Verified in source for this
revision: the npm `files` allowlist (two validator files, nothing else under
`scripts/`); the golden copied-file recipe and `COMMANDS`; the seven shared batteries —
six import `sdlc_core as sc` directly, `test_drift` imports neither, and
`test_skill_invariants` additionally loads the entry point to read the profile (so the
overlay cannot shadow what they test, but one shared battery does observe the overlay's
existence); `dispatch.md` in full (serial loop, ledger-scoped single-writer);
`_validate_plan_tasks` (no disjointness check); kb's Rule Zero table (corpus ingestion
is L3; no escalation triggers today); `MANIFEST_DIRS`; `cmd_gate`'s docs-root exemption
and `cmd_migrate`'s rewrite+`write_bytes` behaviour; `init.js` (bound to
`kb-agentic-init`, `stdio: 'ignore'` — it observes only the exit code, at project init,
not npm install); `sha256_file`'s CRLF→LF normalization (why binaries get a raw digest);
`mkt_check.py`'s live `migrate` drop (why forwarding iterates the parser). The
`## Non-Goals` clauses quoted from `vision/project_vision.md`.

## Diary / Current State

**2026-08-01 — three rounds of review, then the owner reset the design's center.**
Round 1 (three lenses on the pre-ANALYSIS spec) broke the schema: provenance stored per
node destroyed per-claim attributes. Round 2 (disposition verifier + cold adversary on
the ANALYSIS pair) broke the machinery the repairs had leaned on: the automatic
precedence ladder needed columns that did not exist and misbehaved on three-way
conflicts; the parallel topology spent a `dispatch.md` guarantee never issued; the new
modules would never have shipped (two-file npm allowlist); the sub-page locator was
extractor-invented and thus unstable; quantity roll-up summed along a non-mereological
edge; the ceremony budget never priced L1.

The owner then set the principle and two rulings that this version implements: **the
machine detects and holds, only new information resolves** (a ruling carries `basis:` —
the fact the practitioner knows; no basis, no ruling, the conflict legitimately stays
open); **L1 stays free** (ids filled by the validator); and **no useless questions** —
escalations are batched at run end in a legal form that names the conflicting claims,
sources, dates and the reason the machine cannot decide.

**Round 3 (the cap) — FAIL, 6 BLOCK + 6 WARN, all disposed in v4.** The findings were
presented to the owner with proposed fixes; the owner approved proceeding ("vai",
2026-08-01) with the fixes incorporated and verified by the implementation battery
rather than a fourth review round. The six: stored canonical extraction (offsets became
facts of kept bytes — third and final form of the id-stability defect); qty in the id
hash + global uniqueness (one span, two figures); the state machine closed (ruling
supersedes the whole set, symmetry checked, CONTESTED→SUPERSEDED pointers error);
forward-by-default overlay (mkt's hand-copied tuple ships broken today — chipped as its
own fix); computed coverage deleted whole (derived-on-demand is still the forbidden
surface); the id-fill contract (empty id = advisory, fill confined to id cells).

**Next:** implement — F-025's ledger section in `sdlc_check.py` first, then the graph
overlay; batteries and golden baselines close each step.
