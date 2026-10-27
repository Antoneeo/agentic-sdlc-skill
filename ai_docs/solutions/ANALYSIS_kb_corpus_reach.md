---
id: F-084
feature: kb corpus reach — the project files the corpus never examined, and the documents the project sent out
description: Why a KB answers "no coverage" while the source sits one folder away and cannot say what the project declared to a client, and the inventory lookup, upper-bound orient count, changed-original finding, DECLARED provenance and one-way DIVERGES state that close both.
status: COMPLETED
level: L3
domain: code
topics: [corpus, inventory, coverage, provenance, outbound, reconciliation, recall]
start_date: 2026-10-26
end_date: 2026-10-27
branch: claude/f084-kb-corpus-reach
---
# kb corpus reach — what it never examined, what we declared

## Objective

A field project's report (REQUEST R1; names redacted) names two things no kb check sees:

1. **Project files that never reached the corpus.** Nothing compares the corpus with
   the project holding it, so a file left out on purpose and a file never opened look
   the same. In the field project, 842 files outside the docs root were never examined
   — the regulation the project is named after among them — and Topic Recall answered
   `kb: no coverage` with the source one folder away. A newer version of an ingested
   plan sat in the repo, unexamined, so the KB answered from the superseded one.
2. **What the project declared outward.** Every provenance describes something that
   came in. A document delivered to a client says what we declared, to whom and when;
   the KB cannot answer "what did we tell the client about this cell?", and the
   delivered text contradicted a ledger decision without anyone seeing it.

Measured before design (`harness_kb_corpus_reach/probe.py`, kb entry point, base
`origin/main` 854a8697). Baseline probes, green today:
- B1: a sidecar whose `original_path:` resolves and whose original's bytes changed
  after ingest is reported by none of `check`, `corpus`, `stale`.
- B2: a GIVEN row on a sidecar declaring `provenance: OCR` or `provenance: DECLARED`
  only warns (rc 0).
- B3: an ELICITED row whose source declares `provenance: DECLARED` passes silently.
- B4: over 11,000 files, `os.walk` + `os.stat` takes ~0.8 s; `scandir` +
  `DirEntry.stat` ~0.02 s (Windows, warm cache) — the walk must use the latter.

B1, B2 (DECLARED) and B3 are the defects the unit removes: `--expect-outcomes` inverts
them. Outcome probes, red today and green once built, one per R1 test and per rule
carrying it: O1 `inventory pdf` names a never-examined PDF and orient prints `<= 1`;
O2 the newer plan is `NOT_EXAMINED` beside the ingested one; O3 a DECLARED row
`DIVERGES` from a GIVEN row passes `graph`; O4 a GIVEN row on a DECLARED sidecar is
refused; O5 `stale` names a changed original; O6 a registry-excluded file is
`EXCLUDED` though its bytes match a sidecar. `--negate` flips both groups.

## Feature Vision

`vision/features/VISION_kb_second_brain.md` is APPROVED. Served:
- **"onesta nel tempo"**: `no coverage` names the residue it did not read; a
  declaration stays a dated fact about what we said, not about the product.
- **"Una sessione fredda … risponde citando claim-id reali"**: orient says unexamined
  material exists; recall says where.
- **"Nessun claim superseded citato senza che il supersede sia visibile"**: FS5, one
  level down — an artifact whose original moved on is no longer silently current.
- Non-Obiettivi respected: no automatic contradiction detection (the agent classifies;
  the validator checks only `DIVERGES` grammar and targets); no external
  infrastructure (one Markdown registry, no cache); no per-turn hook (once, at orient).

`vision/project_vision.md` (APPROVED v9), Goal "keep understanding durable across
sessions … nothing load-bearing lives only in a transcript": what the project sent out
becomes a stored, dated artifact instead of an email attachment.

Admission (`vision/rulings.md`, precedent first) — two rows; r36 is F-080's:
- **r37 — answers, for a project path the practitioner names, which files under it the
  corpus holds, held in an earlier version, excludes by an approved registry row or
  by the validator's built-in skipped directories, or never examined; orient prints only an upper bound of the last class; `stale`
  reports, per sidecar, an original that changed since ingest.** CONTESTED: r2 REJECT
  (computed per-file state in one surface; its sources include the F-024 coverage
  distribution) and r9 REJECT (any selection by state) against r9's own discriminator
  ("a lookup about what you name is in"), r28 (a count shown beside, never selecting)
  and r35c (a finding on named files). **Owner ruled** (R2): lookup on a named area.
  Distinction line, falsifiable: the command takes a required path argument and has
  **no state filter, sort, flag or per-state count** — its output is ordered by path,
  each line carries its state, no option outputs only the files of one state, and no
  line totals a state (Non-Goal 1 names "a count per status" as out; r35b was
  admitted partly for having none). Exactly two counts exist, both of one class and
  both asked for by R1: orient's upper bound of never-examined files (one number, no
  path) and the recall verdict's count of never-examined files under the path it
  named. The finding names one sidecar. `inventory .` equals the whole list — disclosed (R2) and admitted
  because what is listed is the corpus's reach over its sources, not the state of a
  document or a unit of work, and no output answers "what to work on next" (r3).
- **r38 — records a document the project sent out as a corpus artifact at the version
  sent, its claims under a provenance of their own (`DECLARED`, read as "declared to X
  on D"), and holds a declaration that contradicts the ledger with a one-way
  `DIVERGES <id>` cited by recall and listed nowhere.** Not exempt (r7): a new
  provenance and a new claim state are new capability. Precedents: r33 (a per-claim
  marker nothing lists), F-030 (IMPORTED: a class whose purpose is that one kind of row
  cannot pass for another). ADMIT on the KB Vision's "onesta nel tempo"; the one-way
  form is the owner's (R4). Its cost — the one-way form gives up the symmetric check
  that catches a one-cell flip back to OK (reconciliation.md §1) — goes to the owner
  with the admission (T8).

Disclosure per the admission test: nothing meters; Non-Goal 1 territory is entered by
r37 only (deciding facts above); the mandatory additions and their levels are in
§Ceremony disclosure.

## Use Cases / User Needs

Actors: the Practitioner (kb-agentic), and — because `inventory`, the registry check
and the DECLARED rules ride the shared validator — the Solo developer and every lens's
user whose tree holds a corpus or a registry.

- **UC1 — A cold session learns the corpus has a residue** (Practitioner). At session
  start the agent reads that up to N project files were never examined, and how to see
  which. Benefit: the cold-session signal.
- **UC2 — Recall before "no coverage"** (Practitioner). Asked about a subject the
  ledger lacks, the agent looks under the project paths that may hold it and answers
  `kb: no coverage` together with how many files there were never examined — or names
  the file. Benefit: "onesta nel tempo".
- **UC3 — Deciding what never enters the corpus** (Practitioner). The agent shows the
  files under an area; the practitioner approves exclusions (code, copies, generated
  files) with a reason; each approval becomes one registry row, and the excluded files
  are never read again. Benefit: the residue becomes small enough to mean something.
- **UC4 — An original moved on** (Practitioner). At the consolidation (`stale`), an
  ingested artifact whose original changed since ingest is named with the number of
  claims citing it, so its successor is ingested; once it is, the line goes. Benefit:
  no superseded version answering as current.
- **UC5 — Recording what we sent** (Practitioner). When a document leaves the project
  — to a client, a supplier, another function — the version sent is stored with the
  recipient and the day it was sent; its claims are DECLARED. Benefit: Goal "durable".
- **UC6 — "What did we tell the client about X?"** (Practitioner). Recall answers from
  DECLARED claims, phrased as declarations with recipient and date, and names any
  divergence from the ledger. Benefit: "onesta nel tempo".
- **UC7 — A declaration that contradicts our decision** (Practitioner). Reconciliation
  holds it (`DIVERGES`), the decision stays as it is, and the practitioner is told; it
  is closed by a new send or by a ruling that changes the decision. Benefit: "the
  machine detects and holds; it never decides" (reconciliation.md).

Grounding: `corpus/given/`, sidecar, `sha256:`, `original_path:`, `original_sha256:`,
`provenance:`, `date:`, `supersedes:`, `redacted_at_intake:`, `orient`, `stale`,
`## claims`, Topic Recall verdict, `kb: no coverage`, claim row, `prov`, `state`,
`CONTESTED`, `SUPERSEDED`, ruling, reconciliation, Write Triggers, docs site, `import`
— EXISTS. `inventory`, `audit/INVENTORY_exclusions.md`, `INGESTED`,
`INGESTED_EARLIER`, `EXCLUDED`, `NOT_EXAMINED`, `SKIPPED`, `DECLARED`, `recipient:`, `DIVERGES`
— NEW. "residue" — METAPHOR.

## Functional Spec

**FS1 — what the project is.** The project root is the docs root's parent (the root
`original_path:` already resolves against). The project's files are every regular file
under it, by **the validator's one existing definition of project files** — the
directories `stale`/`mark` already skip are skipped here too: any directory named like
the docs root (at any depth, as that rule compares names), the version-control and
dependency/build directories (`.git`, `node_modules`, `.venv`, `dist`, `build`, …) and
every dot-directory. A skipped directory is not entered, but `inventory` lists it once
(`SKIPPED <dir>/  built-in rule`), so nothing leaves the listing unannounced; it is
not counted at orient. What the exclusion registry excludes (FS2) is treated the same
way, with its own label. Links are never followed: a symbolic link (file or directory) and a
Windows junction are listed, not entered or read. A cloud-only placeholder (a file
whose content is not on the disk: OneDrive/Dropbox "online-only" on Windows, a
"dataless" file on macOS) is listed and never read.

**FS2 — the exclusion registry.** `audit/INVENTORY_exclusions.md` (docs root), a table
`| pattern | reason | approved |`. A row is written only after the practitioner
approved it; `approved` is that day (`YYYY-MM-DD`), optionally followed by the request
entry that carries the approval. Pattern grammar (a gitignore subset):
`/`-separated, relative to the project root; `*`, `?`, `[...]` within one segment;
`**` any number of segments; a trailing `/` matches directories only; a pattern with
no `/` other than a trailing one (`node_modules/`, `*.pyc`) matches a name at any
depth. Matching is case-insensitive on Windows and case-sensitive elsewhere. A
matching directory is not entered — its files are never stat'ed or read — and a
matching file is never opened, whatever its bytes. `validate`
and `check` (every lens, once per run) refuse (error) a row with an empty pattern or
reason, an `approved` that does not start with a valid date, or a pattern containing a
`..` segment or starting with `/`; an absent file excludes nothing and is silent.

**FS3 — `inventory <path>`.** `<path>` is required, relative to the project root (`.`
for the whole project), and must lie inside it and outside the docs root and every
skipped or excluded directory (otherwise `[ERROR]`, rc 2). Every project file under it
is classified, first match wins; only the INGESTED/INGESTED_EARLIER tests read bytes,
and they run only on files no earlier row claimed. Comparison is **by content**: the
file's raw digest against every sidecar that is not a tombstone (a tombstone counts
for nothing, its `original_path:` included). One line per file, in path order,
`<STATE>  <relpath>  <basis>`:

| state | when (first match wins) | basis printed |
|---|---|---|
| `SKIPPED` | a directory the built-in rule skips (FS1), listed once as `SKIPPED <dir>/` — wins over a registry row for the same directory | `built-in rule` |
| `EXCLUDED` | a registry row matches it (an excluded directory is listed once, as `EXCLUDED <dir>/`) — never read | the pattern |
| `NOT_EXAMINED` | it is a link or a cloud-only placeholder no `original_path:` names — never read | `link — not followed` / `cloud-only — not read` |
| `INGESTED` | it is a link or cloud-only placeholder an `original_path:` names — never read | the sidecar, `by path — not read` |
| `INGESTED` | its digest equals a sidecar's `sha256:` or `original_sha256:` — wherever the file now lives | the sidecar |
| `INGESTED` | a sidecar's `original_path:` resolves to it and that sidecar keeps no `original_sha256:` (redacted at intake) | the sidecar, `by path — digest not kept` |
| `INGESTED_EARLIER` | a sidecar's `original_path:` resolves to it, that sidecar keeps `original_sha256:`, and the bytes differ | the sidecar, `original changed since ingest` |
| `NOT_EXAMINED` | none of the above | — |

A file classed `INGESTED` by digest is never also
`INGESTED_EARLIER`: a successor ingested from the new bytes settles it. The command
prints no totals and has no option that filters, sorts or selects by state (r37). Then
`Nothing was written.`, rc 0. No docs root → `[ERROR] no docs root`, rc 1. It has no
time limit: it runs on demand and reads every candidate once.

**FS4 — orient's upper bound (R5).** When the docs root has `corpus/`, orient's
knowledge-layer output adds one line: `Corpus reach: <= N project files not examined
-- exact: sdlc_check.py inventory <path>`. N counts the files FS3 might class
`NOT_EXAMINED`, reading no bytes except the files whose size equals some `given/`
artifact's (hashed, so a verbatim copy anywhere is recognized and a size collision is
never undercounted). Every file an `original_path:` of a non-tombstone sidecar
resolves to counts as examined; skipped and excluded files are not counted.
N overcounts exactly the originals recognized by `original_sha256:` alone (an
extraction whose original is not at the path its sidecar names); it never
undercounts. N = 0 → no line. The count stops after 1.0 s of walking — checked
between files, so one large size-equal file can overrun it by its own hashing time —
and the line then reads `Corpus reach: not counted within 1s -- sdlc_check.py
inventory <path>`. Any error prints nothing and never disturbs the rest of orient
(fail-open, as every orient addition); "no line" therefore means N = 0, no `corpus/`,
or an error.

**FS5 — the changed-original finding.** `stale`'s `## claims` section gains, per
sidecar that is not a tombstone, is not superseded by another sidecar's
`supersedes:`, and whose `original_path:` resolves to a regular, local, non-link file
whose raw digest differs from its `original_sha256:`, one line:
`corpus/given/<artifact>: original <path> changed since ingest -- <n> claim(s) cite
it; ingest the new version as a successor (supersedes:)`. Ingesting the successor
clears it. Report-only, rc unmoved, as the rest of the section. `check` does not hash
originals (it runs on every L1, in CI too). The documented limit "`original_sha256`
is never checked" becomes "checked by `stale` and `inventory` when `original_path:`
resolves to a local file". This places R2's "finding per sidecar" in `stale`, where
R1 asked for it.

**FS6 — recall consults the inventory before "no coverage".** When a Topic Recall
verdict would be `kb: no coverage` or `… node matched, no claims`, the agent first runs
`inventory` on the project paths whose names plausibly hold the subject and counts
the `NOT_EXAMINED` lines; the verdict carries what it found:
`kb: no coverage; not examined under <path>: N` (N = 0 stated), naming the file when
one plainly holds the subject. When no path plausibly holds it, the agent does not run
`inventory .`: it cites orient's bound (`not examined in the project: <= N`). When
`inventory` fails, the clause says so (`inventory failed: <reason>`). Once per topic
per session, like the recall itself.

**FS7 — a document sent out.** Write Trigger: a document leaves the project (to a
client, a supplier, another function) → the version sent becomes a `corpus/given/`
artifact, ingested like any source (redaction at intake and the credential check
included), with sidecar `provenance: DECLARED`, `recipient: <organization or role>`
(never a private person's name — intake redaction's "a role may replace a name") and
`date:` = the day it was sent. When the sent file also lives in the project,
`original_path:` names it, so the inventory recognizes it even when redaction leaves
no digest. Drafts, internal working documents and the files a sent document is
generated from do not enter. A resend is a new artifact whose sidecar `supersedes:`
the earlier send. The docs site's chronology shows a DECLARED artifact as "document
sent", not "source document received".

**FS8 — DECLARED claims.** `DECLARED` joins the provenances. `graph` and `check`
refuse (error):
- a `DECLARED` row any of whose sources is not a `corpus/given/` artifact whose
  sidecar says `provenance: DECLARED` and carries `recipient:`;
- **any non-DECLARED row** any of whose sources declares `provenance: DECLARED` (today a
  GIVEN row there only warns — B2 — and any other row passes — B3; for a declaration
  the confusion is the defect). Every source position is checked, not only the first:
  reconciliation's corroboration appends a source to an existing row, so a declaration
  that agrees with the ledger is a DECLARED row of its own, never a second source;
- a `SUPERSEDED` pointer from a DECLARED row at a non-DECLARED row, or from a
  non-DECLARED row at a DECLARED row: a declaration is superseded only by a later
  declaration, and never settles a fact;
- `CONTESTED` between a DECLARED and a non-DECLARED row (that is `DIVERGES`).
`CONTESTED` between two DECLARED rows is legal: two sends that contradict each other
are both still held by their recipients.

**FS9 — DIVERGES (R4).** A DECLARED row whose assertion contradicts a non-DECLARED,
non-SUPERSEDED row, scopes overlapping, carries `state: DIVERGES <id>[, <id> …]`; the
target may be `OK` or `CONTESTED`. The validator refuses (error): `DIVERGES` on a
non-DECLARED row; a target that resolves to no row, to a DECLARED row, or to a
`SUPERSEDED` row (re-judge against the successor). The ledger row is not touched. It
closes by (a) a new send whose DECLARED row supersedes the divergent one, or (b) a
ruling that changes the decision: the ledger row becomes `SUPERSEDED <ruling-id>`,
`check` then errors on the stale pointer until the agent re-judges the declaration
against the ruling (`OK` when it now agrees, `DIVERGES <ruling-id>` when not). Nothing
lists, counts or filters rows by `DIVERGES`; the reconciliation escalation of the run
that set it presents it to the practitioner (reconciliation.md §4).

**FS10 — citing a declaration.** Recall cites a DECLARED claim as "declared to
<recipient> on <date>", never as a fact about the product; a `DIVERGES` row is cited
with the ledger row it diverges from. Under the anti-echo rule a DECLARED artifact is
**not ground** for a product decision: a chain that ends on one is reported as
"rests on our own declaration to <recipient>" and the claim is treated as unverified
for decision-grounding, as the rule already treats an unresolvable ground. The docs
site classes such ground `declared`.

**FS11 — a declaration stays in the project that made it.** A declaration is that
project's commitment to its recipient; carried into another project it would read as
the importer's own. So `export` leaves DECLARED rows and their artifacts out of the
bundle and says so in one line (`declarations stay in this project: not exported`, a
yes/no, never a count — as the not-yet-honored mark, F-080). The closure stays whole
by construction: under FS8/FS9 no non-DECLARED row points at a DECLARED row, so
removing every DECLARED row removes every pointer to one. A DERIVED note whose
`derived_from:` names a DECLARED artifact travels as today, its edge dangling in the
target exactly as any `derived_from:` target a bundle does not cite (the existing
walkability warning). Because `export` does not run `check`, it verifies the pointer
rule itself: a selected non-DECLARED row pointing at a DECLARED row stops the export
(error), so a tree that breaks FS8 cannot ship a dangling pointer. `import` refuses
(error) a bundle row with `prov: DECLARED` — only a hand-made bundle can carry one.

Acceptance criteria:
- AC1 (FS1, FS3): a tree with one verbatim copy, the same copy moved to another
  directory, one extraction with `original_path:` + `original_sha256:`, that original
  changed, one redacted extraction with `original_path:`, a `node_modules/` and a
  dot-directory, one registry-excluded directory, one registry-excluded file pattern,
  one untouched file, one symlink and one junction (Windows) yields exactly:
  INGESTED ×3 (digest, digest after the move, by path), INGESTED_EARLIER ×1, EXCLUDED
  ×2, NOT_EXAMINED ×3 (one `link — not followed` per link), SKIPPED ×2 and nothing
  under them; neither the excluded directory's files nor the excluded file — whose
  bytes equal an artifact's — is ever opened (instrumented open); a tombstone's
  `original_path:` counts for nothing; no totals line.
- AC2 (FS3): `inventory` without a path → usage error; `inventory ../x`,
  `inventory ai_docs` and a path under a skipped directory → `[ERROR]` rc 2;
  `inventory --state` does not exist.
- AC3 (FS2): each malformed registry row is one error in `validate` and `check`; a
  well-formed registry is silent; the registry is not catalogued by `memory_records`.
- AC4 (FS4): orient prints `<= N` with N equal to AC1's NOT_EXAMINED count; prints no
  line at N = 0 and with no `corpus/`; a size-colliding non-identical file is counted;
  a raising walk prints nothing while the topic router and the rest of orient still
  print; the 1 s message (injected clock).
- AC5 (FS5): the changed original appears in `stale`'s `## claims` with its citing
  claim count, rc unmoved; after a successor sidecar `supersedes:` it, the line is
  gone; an unchanged original and a tombstone produce none; `check` output unchanged.
- AC6 (FS8): each FS8 refusal is one error, including a DECLARED artifact as a
  GIVEN row's second source and a GIVEN artifact as a DECLARED row's second source; a
  well-formed DECLARED row passes; two CONTESTED DECLARED rows pass.
- AC7 (FS9): each FS9 refusal is one error; a DIVERGES at a CONTESTED target passes;
  after a ruling supersedes the target, `check` errors until the row is re-judged.
- AC8 (FS11): export of a topic holding a DECLARED row (with a resend chain and a
  DIVERGES) writes a bundle without DECLARED rows or their artifacts, prints the
  yes/no line, and the bundle imports into an empty project with `check` CLEAN; a
  hand-made bundle with a DECLARED row is refused on import.
- AC9: `probe.py --expect-outcomes` exits 0: the baseline group green with B1,
  B2 (DECLARED) and B3 inverted, the outcome group O1–O6 green.
- AC10 (FS6, FS7, FS10, UC3, UC7): kb eval scenarios — a no-coverage question with an
  unexamined source in the tree; a "what did we tell X" question over a DECLARED row
  with DIVERGES; an exclusion proposed and written only after approval; a send whose
  contradiction is held and escalated at the end of the run.

## Interface Contract

Surfaces: `orient` output (agent, session start), the `inventory` command and output
(agent and practitioner), `stale`'s `## claims` (closure), `validate`/`check`/`graph`
errors, the Topic Recall verdict (agent → practitioner), the exclusion registry and
sidecar fields the agent writes, the docs site's claim and chronology views
(practitioner), kb doctrine.

| Flow | Path | Idiom reused |
|---|---|---|
| Session start (UC1) | hook → orient → knowledge-layer output, one more line `Corpus reach: <= N …` | the append's one-line counts |
| Recall (UC2) | would-be `no coverage` → `inventory <path>` → count `NOT_EXAMINED` lines → `kb: no coverage; not examined under <path>: N` | the verdict, extended by a clause |
| Exclusions (UC3) | `inventory <path>` → practitioner approves → registry row with date → `EXCLUDED` next run; `validate`/`check` check rows | request record's "write after approval"; `adopt`'s "Nothing was written." |
| Consolidation (UC4) | `stale` line → successor ingested (`supersedes:`), claims re-placed → line gone | superseded-chain lines |
| Sending (UC5, UC7) | sent version ingested (FS7) → DECLARED rows → reconciled → `DIVERGES` → escalation at run end | intake; five outcomes; batched escalation |
| What we said (UC6) | recall cites "declared to <recipient> on <date>", names DIVERGES; site: origin `declared`, state `diverges`, ground `declared`, chronology "document sent" | per-provenance stance |

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| resolve docs root, project root | EXISTS | `sdlc_core.resolve_docs_dir`, `find_project_root` | `_kb_orient_append` |
| define project files (skipped dirs) | INADEQUATE | `sdlc_core.SKIP_DIRS` + docs root + dot-dirs, inlined in `iter_files` (`os.walk`, descends junctions) | `iter_files`; B4 timing |
| reject links incl. junctions | EXISTS | the `is_symlink`/`is_junction` test in `_memory_safe` | `knowledge.py` |
| confine a relative path | EXISTS | `sdlc_core.confine_under` | `kb_cmd_adopt` |
| read sidecars, resolve `original_path` | EXISTS | `load_frontmatter`, `kb_unquote`, `_kb_original_candidates`, `_kb_pointer_resolves`, `kb_is_tombstone` | `kb_corpus_check` |
| raw-byte digest | EXISTS | `kb_sha256_bytes` | `kb_corpus_check` |
| claim rows by topic, citing counts | EXISTS | `kb_collect_topics`, `kb_cited_extents` | `kb_cmd_stale`, coverage check |
| stale `## claims` section | EXISTS | `kb_cmd_stale` | — |
| orient append within budget | EXISTS | `_kb_orient_append`, `_fit_orient_append` | — |
| drop rows when writing a bundle | EXISTS | `kb_bundle_write` (F-080 mark drop) | — |
| claim state grammar | INADEQUATE | full-grammar parsers in `kb_check_claims`, `kb_export_closure`, `_kb_states` (← `kb_import_foreign_rulings`), `docs_site._kind`; SUPERSEDED-only readers in `kb_check_marks`, `kb_time_cycle` | grep `CONTESTED\|SUPERSEDED` (ERE) |
| per-provenance sidecar rules | INADEQUATE | `kb_check_claims` provenance block; no DECLARED | B2, B3 |
| classify project files against the corpus | MISSING | — | grep `inventory`, `NOT_EXAMINED`, `scandir` in `knowledge.py`, `sdlc_core.py`: none |
| gitignore-subset matcher | MISSING | — | grep `fnmatch` in both: none |
| cloud-placeholder test | MISSING | — | grep `st_file_attributes`, `st_flags`: none |

New components:
- `sdlc_core.skip_dir(name) -> bool` — the existing skipped-directory rule, extracted
  from `iter_files` (which then calls it), so the two walks share one definition.
- `knowledge.kb_exclusions(docs) -> (rows, errors)` — FS2's registry parser.
- `knowledge.kb_excluded(rel, is_dir, rows) -> pattern | None` — the FS2 matcher.
- `knowledge.kb_unreadable(entry) -> "link" | "cloud-only" | None` — FS1's
  never-read test (symlink, junction, Windows offline/recall attributes, macOS
  `SF_DATALESS`).
- `knowledge.kb_corpus_reach(docs, rel, exact=True, deadline=None) -> dict` — the
  FS1/FS3 walk and classification (`exact=False` is FS4's bound), one implementation
  for `inventory`, orient and recall.
- `knowledge.kb_changed_originals(docs) -> [(artifact, original, n_citing)]` — FS5.
- `knowledge.kb_cmd_inventory(root, docs, path) -> int` — FS3 printing.
- `knowledge.kb_has_declarations(selected) -> bool` — FS11's export line.
- `knowledge.kb_drop_declarations(text) -> text` — FS11's row drop in a bundle.

Guides: `GUIDE_skill_family_changes.md` (read) — `knowledge.py`, `sdlc_core.py`,
`docs_site.py` and the site assets count once. `GUIDE_shared_project_memory.md`
(read) — the registry check rides `_kb_extra_validate`, which `kb_validate_surface`
also reaches (mkt `validate`/`check`), so it runs on corpus-less trees, once per run;
`memory_records` excludes audit logs (AC3 verifies the registry stays out).

## Guide check

- A CURRENT guide covers what this touches: `GUIDE_shared_project_memory.md` (composition
  of `validate`/`check`, the orient append) — read; no conflict.
- No new high-complexity model was forced: the walk and the classification are one
  linear function each. No guide is due.

## Impact

`knowledge.py`, `sdlc_core.py`, `docs_site.py` and `docs_site/*` are shared verbatim by
`skills/agentic-sdlc-skill/` and the three `distributions/*/skills/*/` (four copies):
changed once, copied, `shared_files.py --update` ×4.

| Path | Change | Trace |
|---|---|---|
| `scripts/sdlc_core.py` (×4) | MODIFY | `skip_dir` extracted; `iter_files` calls it (behavior unchanged) |
| `scripts/knowledge.py` (×4) | MODIFY | `PROVENANCES` + DECLARED; FS8/FS9 in `kb_check_claims` (provenance block, state block — via `_kb_states`, which gains DIVERGES); `kb_export_closure` via `_kb_states`, and FS11 with its return shape unchanged: artifacts cited only by DECLARED rows are left out of `artifacts`, and a selected non-DECLARED row pointing at a DECLARED row is an `errors` entry (export does not run `check`, so it verifies the FS8 pointer rule itself); `kb_bundle_write` drops DECLARED rows when it writes topic tables (beside the F-080 mark drop), return unchanged; new `kb_has_declarations(selected) -> bool`, which `kb_cmd_export` calls to print the line; `kb_import_plan` refuses a `prov: DECLARED` row; new components; `kb_cmd_stale` FS5 lines; `_kb_orient_append` FS4 line in its own `try`; `_kb_extra_validate` FS2 errors; `INTERCEPTED`, parser, `kb_cmd_help`, `main` for `inventory` |
| `scripts/docs_site.py` (×4) | MODIFY | `_kind`: `diverges` + targets; origin `declared`; `Grounds` class `declared` (FS10); `chronology`: DECLARED sidecars as kind `sent` |
| `docs_site/app.js`, `strings.js`, `style.css` (×4) | MODIFY | `ORIGINS` + `declared`; strings `origin_declared`, `origin_declared_why`, `ground_class_declared`, `state_diverges`, `state_diverges_why`, `event_sent`; colors |
| `scripts/shared_manifest.json` (×4) | REGENERATE | copies |
| kb `SKILL.md` | MODIFY | command list (`inventory`); Write Triggers rows: a document sent out (FS7), `audit/INVENTORY_exclusions.md` (FS2); Topic Recall: FS6 clause, FS10 citation and anti-echo stance |
| kb `distillation.md` | MODIFY | §1 table row "a document the project sends out"; FS5's change to the `original_sha256` limit; §2 prov list + DECLARED |
| kb `reconciliation.md` | MODIFY | §1 a declaration against the ledger → DIVERGES, and a declaration never corroborates a non-DECLARED row (nor the reverse); §3 state-machine rows (set, closed by resend, by ruling, re-judge on a superseded target); §4 escalation names DIVERGES |
| kb `templates.md` | MODIFY | sidecar `provenance: DECLARED`, `recipient:`, `date:` = day sent; `original_sha256` limit text; new template `audit/INVENTORY_exclusions.md` |
| kb `portability.md` | MODIFY | export: declarations stay in the project (FS11); import refuses a DECLARED row |
| kb `taxonomy.md` | CHECK | descent in answer mode, if it restates the verdict values |
| `mkt_check.py` | MODIFY | epilog shared-commands list gains `inventory` |
| kb `evals/` | ADD | AC10 scenarios |
| kb `scripts/test_kb_corpus_reach.py` | ADD | AC1–AC9 |
| `ai_docs/solutions/harness_kb_site/probe.py` | CHECK | enumerates `PROVENANCES` and states; update if its assertions fix the set |
| kb `README.md`, `CHANGELOG.md` ×4 | MODIFY | command list; notes (registry check and DECLARED rules reach every lens's `validate`/`check`) |
| `ai_docs/strategic/architecture.md` | MODIFY | Component Map: Corpus store row (reach, DECLARED), Topic graph row ("No coverage state exists anywhere" no longer true), new components |
| `ai_docs/vision/rulings.md` | MODIFY | r37, r38 |
| `ai_docs/solutions/harness_kb_corpus_reach/probe.py` | ADD | B1–B4, O1–O6 |

Blast radius — one instrument, `grep` (ERE) over the four copies of each shared file,
every entry point and `ai_docs/solutions/harness_*`; no symbol-graph tool covers this
repository in Standalone (devPNT off), so no cross-instrument delta can be declared:
- `PROVENANCES` — `kb_check_claims`; `harness_kb_site/probe.py`.
- Full state grammar — `kb_check_claims` (state block), `kb_export_closure`,
  `_kb_states` (← `kb_import_foreign_rulings` ← `kb_import_plan`), `docs_site._kind`,
  `harness_kb_site/probe.py`. SUPERSEDED-only readers `kb_check_marks`, `kb_time_cycle`
  match `^SUPERSEDED` and are unaffected by a third kind.
- The state error text "state must be OK, …" — `kb_check_claims`; tests assert its
  prefix only (re-verify at RED).
- `kb_export_closure` — `kb_cmd_export`; `harness_spec_code_divergence(_hybrid)/probe.py`.
  Return shape unchanged, so none of its 18 call sites changes: `kb_cmd_export` ×4
  copies, the two harness probes, `test_claim_ledger.py` ×11, `test_kb_intake.py` ×1.
- `kb_bundle_write` — return unchanged; 15 call sites (`kb_cmd_export` ×4, two harness
  probes, `test_claim_ledger.py` ×9, four of which assert its boolean) untouched.
  `kb_import_plan` — `kb_cmd_import`.
- `SKIP_DIRS` — `iter_files` and `_external_references` (spine); the extraction
  changes neither's behavior.
- `kb_cmd_stale` — `main` (`stale` in code, kb, course; mkt via `knowledge.main`).
- `_kb_orient_append` — `kb_cmd_orient` (← SessionStart hook in every lens).
- `_kb_extra_validate` — `kb_cmd_validate`, `kb_cmd_check`, `kb_validate_surface`
  (← `mkt_check.py`); re-exported by kb `sdlc_check.py`; tested in `test_kb_graph.py`.
- `iter_files` — `stale`/`mark` in the spine; behavior unchanged by the extraction.
- `INTERCEPTED`/`main` — `inventory` reaches code, kb, course and mkt entry points.
- `docs_site.chronology`, `Grounds` — the site build only.

Populations at rest (triggers evaluated: read-time ↔ write-time move — no; no-migration
constraint — no; new values in columns holding data — yes, `prov` and `state`; a
narrowed `filter`/`authorize` function — no):

| Existing population | Regime | After | Who sees it |
|---|---|---|---|
| GIVEN rows on artifacts whose sidecar says another provenance | warning | unchanged, except `provenance: DECLARED` → error; none exist (DECLARED is new) | — |
| sidecars with `original_path:` + `original_sha256:` whose original changed | silent (B1) | `stale` line, report-only, until a successor is ingested | practitioner at consolidation |
| redacted text artifacts ingested without `original_path:` | n/a | their project original reads `NOT_EXAMINED` (no digest, no path to match) — an honest "not provably examined"; fixed by adding `original_path:` to the sidecar | practitioner, via `inventory` |
| documents already sent, not in the corpus | not representable | unchanged until ingested; the Write Trigger fires on a send from now on, an earlier send is ingested when the practitioner asks | practitioner |
| project files never examined | invisible | counted at orient, listed on request | agent, practitioner |
| exported bundles from before this version | no DECLARED/DIVERGES | import unchanged for them | — |

## Security and Threat Model

Surfaces: walking and reading untrusted project files; paths from sidecars, the
registry and the command line; output into logs; outbound documents stored in a
committed corpus; bundles crossing projects.

- **T1 path escape** — `inventory <path>` and registry patterns → `confine_under`;
  `..` / leading `/` patterns refused (FS2, AC2/AC3). `original_path:` resolution
  reuses `_kb_original_candidates` (unchanged stance: absolute paths are the
  practitioner's).
- **T2 link traversal and loops** → symlinks and junctions never followed, by the
  `_memory_safe` idiom (FS1, AC1).
- **T3 cloud placeholders** — reading one triggers a download → never read on Windows
  (offline/recall attributes) and macOS (`SF_DATALESS`); other platforms read them as
  regular files (declared residual).
- **T4 resource exhaustion** — huge trees, huge files → `scandir` with pruning of
  skipped and excluded directories; streamed hashing; orient's 1 s cap (FS4). Recall
  never runs `inventory .` (FS6). `inventory` itself has no cap: run on demand, it
  hashes every candidate under the named path once (declared).
- **T5 disclosure in output** — `inventory` prints relative paths and sidecar names,
  never content; paths are already visible in the repository (residual).
- **T6 confidential and personal data in sent documents** — FS7 applies intake
  redaction and the credential check unchanged; `recipient:` is an organization or
  role, never a private person's name.
- **T7 laundering a declaration into a fact** — B2/B3 → FS8 refuses every
  non-DECLARED row with a DECLARED source in any position, and every
  SUPERSEDED/CONTESTED mix; FS10 makes a DECLARED artifact non-ground for product
  decisions; FS11 keeps declarations out of bundles, so another project never reads
  one as its own.
- **T8 a divergence closed by flipping a cell** — a bare edit of `DIVERGES` to `OK` is
  not detectable (no history; the one-way form has no counterpart to check, unlike
  CONTESTED's symmetric check). Declared residual, put to the owner with r38.
- **T9 exclusion as a hiding place** — a registry row removes files from the count
  without anyone reading them → each row carries a reason and an approval date,
  visible in the diff; the validator cannot verify the approval (residual). The
  built-in skipped directories (FS1) are exclusions nobody approved per project: they
  are the validator's existing definition, and `inventory` lists each once as
  `SKIPPED`, so none leaves the listing silently; orient's bound does not count them
  (residual, declared).

## Ceremony disclosure

- Every session start in a project with `corpus/`: one stat-only walk (B4: ~0.02 s for
  11,000 files; capped at 1 s) plus hashing of size-equal files, one line of output.
- Every `validate`/`check` (every lens): the registry is parsed when present. No walk.
- `stale` (closure): one digest per non-superseded sidecar with a locally resolving
  `original_path:` and `original_sha256:` — on a large binary corpus, re-reading those
  originals once per consolidation.
- Recall that would say `no coverage`: one `inventory` on a named path.
- Each document sent out: one ingestion (an L3 ingestion step, as any source).
- Each exclusion: one approval and one registry row.
- **An L1 claim edit can now fail `check`**: refining, ruling on or superseding a row
  that a DIVERGES row points at errors until the declaration is re-judged (FS9) —
  the same cost CONTESTED already imposes on its members. Otherwise an L1 meets a new
  error only on a malformed registry or a mis-provenanced DECLARED row.
- Every lens's user, not only the Practitioner, can meet `inventory`, the registry
  check and the DECLARED rules (shared validator); none fires on a tree without a
  corpus or a registry.
- Read cost, estimated (to measure at closure): kb `SKILL.md` +1.5 KB, `distillation.md`
  +0.9 KB, `reconciliation.md` +1.3 KB, kb `templates.md` +1.2 KB, `portability.md`
  +0.3 KB.

## Action Plan

- [x] Design review (`review.md` moment 1): FAIL ×3, cap reached; owner accepted the
      design with the round-3 fix to be verified at closure (R6); r37/r38 ADMIT with the
      cost (R7); T8's residual accepted (R8); R5's mechanism correction confirmed (R9).
- [x] RED: `test_kb_corpus_reach.py` AC1–AC9 (probe outcomes red: done).
- [x] `skip_dir` extraction; `_kb_states` + DIVERGES and the two parsers routed through
      it (existing batteries green).
- [x] FS8/FS9 rules; FS11 import/export.
- [x] FS1–FS4 components and `inventory`; FS5 in `stale`; FS2 in validate/check.
- [x] Docs site `declared` / `diverges` / ground / chronology.
- [x] Doctrine: kb `SKILL.md`, `distillation.md`, `reconciliation.md`, `templates.md`,
      `portability.md`; evals.
- [x] Copy ×4; `shared_files.py --update` ×4; mkt epilog.
- [x] Component Map, README, CHANGELOG ×4, rulings r37/r38.
- [x] GREEN: four batteries, probe `--expect-outcomes`; E2E_TEST, closure review,
      MERGE_REVIEW; `check` CLEAN.

## Test Strategy

`test_kb_corpus_reach.py` (kb-only, like `test_kb_intake.py`) covers AC1–AC9 through the
kb entry point and the new functions directly; AC4 also through the code entry point
(orient reaches every lens). Cloud placeholders are tested by injecting the attribute
test (no real placeholder in CI); the junction case runs on Windows only. The kb eval
scenarios cover AC10 (UC2, UC3, UC6, UC7). The probe under `--expect-outcomes` is AC9:
the baseline facts that must survive (B2 OCR, B4) stay green, the three defects the
unit removes are inverted, and the outcome group must be green. Four batteries
(`python -m unittest discover -s <scripts> -p "test_*.py"`).

## Diary

- **2026-10-26** — Opened from the field report (R1). Vision Gate: r37 CONTESTED,
  owner ruled lookup on a named area (R2). Worktree `claude/f084-kb-corpus-reach` off
  `origin/main` 854a8697 (local `main` was behind: F-082 merged, F-083 closed there).
- **2026-10-27** — Owner: both capabilities in one analysis (R3), DIVERGES one-way (R4),
  orient upper bound (R5). Two deviations from the report, by DRY: the sent date is the
  sidecar's existing `date:` (no `sent:`), and outbound is `provenance: DECLARED` (no
  `direction:`). The reference implementation (`tools/kb_repo_inventory.py`) is not on
  this machine; the design follows the report's text.
- **2026-10-27** — Design review rounds 1–2 (log: `audit/reviews/REVIEW_LOG.md`).
  Decisions they produced that a reader of this document needs: classification is by
  content wherever the file lives (R1 "per contenuto, non per nome"); the project-file
  definition is the validator's existing one; declarations do not cross a project
  boundary (FS11), which keeps resend chains whole without any import conversion;
  R5's option text described the bound as "size different from every given/
  artifact", which would undercount a size collision, so FS4 hashes size-equal files
  — that correction goes to the owner with the cost.
- **2026-10-27** — Implemented through RED → GREEN (R10). `test_kb_corpus_reach.py`
  (25 tests) red before the code (17 of the first 24 failing for the new behaviour;
  the site test red against the old `docs_site.py`), green after. Four batteries green
  (code 464, kb 779, mkt 466, course 459); probe `--expect-outcomes` exits 0;
  `inventory` verified through all four entry points. The junction case ran on this
  machine; the symlink case is skipped here (no symlink privilege) — it runs where
  symlinks can be created. ADR_2026-10-27_declarations_and_corpus_reach.md records the
  decision. Measured read cost (UTF-8, LF): kb `SKILL.md` +2,036, `distillation.md`
  +1,165, `reconciliation.md` +1,494, kb `templates.md` +1,816, `portability.md` +460 —
  +6,971 bytes against the ~5.2 KB estimated in this document; the owner accepted the measured figure (R11).
- **2026-10-27** — Closed. Closure review (log: `audit/reviews/REVIEW_LOG.md`) PASS on
  round 3; the round-1 eval fixtures (ids, slugs), the registry's bad glob class and
  empty row, linked directories, link targets and letter-case paths were fixed with
  tests on the way. Declared residuals, for the owner: a **file** link named like a
  skipped directory or matching a dir-only exclusion is listed as that directory
  (links are matched by name and never resolved, so nothing is read); symlink-specific
  branches are untested on this machine (no symlink privilege — junctions were tested);
  real cloud placeholders were only simulated. Final evidence: batteries code 464, kb
  791, mkt 466, course 459 OK; probe `--expect-outcomes` rc 0.
