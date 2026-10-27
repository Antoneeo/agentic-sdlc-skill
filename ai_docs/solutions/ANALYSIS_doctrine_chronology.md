---
description: F-073 - readable chronology and parallel workstreams. One grammar for a dated entry, read by shared validator readers so F-072's chronology can parse events; `next:` holds only the next step; feature ids checked against every ref; the shared-log and shared-checkout defects answered with the smallest measured remedy.
status: COMPLETED
feature: F-073
id: F-073
start_date: 2026-10-17
end_date: 2026-10-17
level: L3
---
# Feature Analysis: readable chronology and parallel workstreams

**For whom**: the independent design reviewer, then the owner. **To do what**: approve
or reject the rules below before any code. **Answers**: which lines are dated events,
in what form, read by which function, checked how, at what ceremony cost; and what each
of the three parallel-work defects needs. **Does not answer**: how F-072 shows the
events (its spec, `ANALYSIS_kb_site.md` §Chronology, branch `feat/kb-site-spec`).

Owner statements: `audit/requests/REQUEST_doctrine_chronology.md` R1–R7. Measurements
and probes: `harness_doctrine_chronology/` — `misura_cronologia_2026-10-17.md` (dates),
`probe_rules.py` (the readers, red/green), `probe_ids.py` (id collisions, red/green),
`probe_parallel.sh` (merges, edits, worktrees).

## Objective

"What did we do this week, and when?" cannot be answered from the documents. The dates
exist (no non-ISO date opens an entry in either corpus) but their place and form are
free: Diary entries come in 15 forms; `next:` has become a state summary in the field
project (median 500 characters, 24.9k in all); spikes and releases leave no entry where
a reader looks. F-072's chronology reader returns no event until a rule says which lines
are events (`docs_site.chronology()`, commit 161b254).

Done = one grammar for a dated entry, applied to the hand-written places that lack one,
read by shared functions that both the validator and F-072 call; `next:` restricted to
the next step; and for each parallel-work defect either the smallest mechanism or the
measured reason none is needed.

## Feature Vision

**Precedent first** (`vision/rulings.md`).

| Row | Placement | Consequence |
|---|---|---|
| **r14** — fixes a defect, purpose/actors/surface unchanged → exempt | primary for the readers, the `next:` rule and the id check. The Diary, project notes, `next:` and feature ids already exist for the same actors and purpose; what improves is correctness: a date that can be read, a field that holds one step, an id that is unique across branches | no admission. **Not** an exemption from the budget: the three new advisories are priced below |
| **r2** — collects per-work state into one surface → REJECT | **near-miss disclosed (r8)**. The chronology is F-072's surface, ruled on that branch (Vision v9, not on `main`; this unit does not depend on it). This unit adds no surface: each date stays in its own document | distinction line: *the rules date events inside the document that already holds them; nothing is collected* |
| **r3** — tells what to work on next, in what order, by whom → REJECT | **near-miss disclosed (r8)**: the `next:` rule names "the next step". `next:` exists since F-019/F-028, ruled there as one workstream's own state. This unit narrows it; it adds no ordering, holder or cross-workstream view | distinction line: *it shortens a field that already answers "the next step inside this one unit"; it answers nothing across units* |
| **r26** — request record, "append-only by doctrine and review, **no validator**" | the heading form is already fixed (`templates.md` §Request record). This unit adds a **reader** of it, not a check; the id check reads the record's `unit:`/`analysis:` fields, which r26 created, and judges nothing about the quotations | r26's accepted cost unchanged |

**Goals advanced.** Goal 2 — "nothing load-bearing lives only in a transcript": today
"when" lives in git and in the agent's reconstruction (R1). The Core Problem's second
half — understanding that "evaporates when the session ends" — is what an unreadable
`next:` and a renumbered unit cause for the next session.

**Non-Goal 3, the budget**: `## Functional Spec` §Cost. **L1: zero. L2: zero** (R7, and
A1/A2 are gated on `level: L3`, A3 runs only while an open L3 unit exists — its runtime is the one cost an L1/L2 closure can pay, disclosed in §Cost). **Non-Goal 4 (coupling)**: the grammar is
this family's own.

## Use Cases / User Needs

Actors from the Vision; every product name is EXISTS unless marked.

- **UC1 — Solo developer, resuming** (Actor 1, "never re-explaining the project"): asks
  the agent what happened this week, when. The agent answers from Diary entries, request
  records, review-log rows, project notes, notes, sources and ADRs, each date read from
  the document, without git (R20: "la cronologia non è quella di git"). Goal 2.
- **UC2 — Agent, writing a Diary entry**: writes the date first, once; the validator
  tells it when an entry it wrote cannot be dated. Goal 2; "ceremony proportional to
  risk" (L3 only, only on analyses started under the rule).
- **UC3 — Agent, at session start** (Actor 1): reads the generated registry through
  `orient`; each row's `next:` is one step, so the row says what to pick up rather than
  paraphrasing the Diary. Goal 2.
- **UC4 — Team lead, two branches** (Actor 2, "divergence ... surfaced before the change
  is merged"): a unit opened on one branch under an id another branch already uses is
  flagged at the next `check`, before the id spreads into tags and commit messages.
  Goal 3.
- **UC5 — F-072's chronology reader** (software actor, NEW consumer on
  `feat/kb-site-spec`): builds every event with the validator's own functions, so the
  page and `validate` cannot disagree on what is an event. Goal 2.

## Functional Spec

The trigger fires: the validator's output and the doctrine's writing rules change.

### The dated-entry grammar (one, shared)

Normative form: the `OPENER` regex and `is_opener` in `probe_rules.py`, which ship as
`sdlc_core.ENTRY_OPENER` / `entry_openers`. In words:

- An **entry opener** is a line, at column 0, that — after an optional list marker
  (`- `, `* `), optional heading marks (`### `, `#### `) and an optional `**` — begins
  with an ISO date `YYYY-MM-DD` followed by a word boundary, **and starts a block**: the
  line above is blank, absent or a heading, or the line itself is a list item or a
  heading. A hard-wrapped prose line that happens to begin with a date is therefore not
  an opener (round 1 found six such lines in `ai_docs/`, e.g.
  `ANALYSIS_kb_knowledge_method.md`, where `2026-08-01) with the fixes…` continues a
  sentence). A separator after the date is **not** required: 52 real openers read
  `DATE (qualifier)` or `DATE word` ("2026-10-02 release closure: …").
- The **label** is the text after the date: leading `**`, whitespace and one separator
  (`—`, `–`, `:`, `-`) removed; then up to the closing `**` when the opener is bold,
  otherwise up to the first sentence end; trimmed, at most 120 characters, as written.
- The readers return **openers only** — date, label, line. No consumer needs where an
  entry ends, so no extent rule is defined; the doctrine tells the writer that an
  undated paragraph is read as part of the dated entry above it.
- The **written form** taught is one: `**YYYY-MM-DD — label.** body`. The reader also
  accepts the other dated forms already in the corpus, so the 217 openers written here
  stay readable with no migration (P3).

### Where each kind of event is read

| Event kind (F-072's list) | Rule | Reader | Check |
|---|---|---|---|
| ANALYSIS Diary entry | every entry starts with an opener; "current state" is the latest entry, dated the day it was written | `entry_openers(section_lines(text, DIARY)[1])` | **A1** |
| Request-record entry | `### R<n> — YYYY-MM-DD — <label>`, unchanged (34/34 here, 54/54 on `feat/kb-site-spec`, 25/26 in the field) | `request_entries(text) -> (entries, unparsed)`; a non-matching heading is unparsed and named, never dropped | none (r26) |
| Project note | a note recording an **event** opens with an opener; a **standing** note (an environment fact) stays undated and is not an event | `entry_openers(text)` | none: a check cannot tell an event from a standing fact |
| Spike outcome | `## Answer / Outcome` opens with an opener dated the day the answer was reached | `entry_openers(section_lines(text, OUTCOME)[1])` | none |
| Note / decision note (kb `corpus/notes/`) | frontmatter `date:` (existing; 236/236 in the field) | `knowledge.frontmatter_date(meta)` | existing kb checks |
| Source document received (kb sidecar) | frontmatter `date:` = **the day the source was received** (stated now; the template showed the field without saying what it dates) | `knowledge.frontmatter_date(meta)` | existing |
| Review-log row | the `date` cell (existing) | `sdlc_core.parse_review_log` | existing |
| Decision record (ADR) | `**Date:** YYYY-MM-DD` in the body (existing; 20/20), the `ADR_YYYY-MM-DD_*` name as fallback | `sdlc_core.adr_date(name, text)` | none |

**Not an event, declared:** an analysis's `start_date`/`end_date` (F-072 excludes them,
R23); a HANDOFF's `since:`/`updated:`; git history. **Not covered, by the owner's
choice (R7):** L2 work with no analysis.

### The `next:` rule

`next:` in a `HANDOFF_[feature].md` holds **the next concrete step, one sentence**.
What happened, and the state of the work, goes to the ANALYSIS Diary as a dated entry
(the Diary write trigger already fires when "a session ends with work unfinished").
Basis: in the field `next:` paraphrases the Diary (median 500 chars, up to 7,540), so
the state is written twice and drifts. The registry is also what `orient` emits at
every session start, cut at 6,000 characters per document and 16,000 in all
(`ORIENT_PER_DOC_CHARS`, `ORIENT_MAX_TOTAL_CHARS`; the registry is the fourth document,
so it gets what README, the manifest and the router leave). The rule **shrinks** the
registry; it does **not** make every row fit: a row's other cells are 141–246 chars
here, so 20 rows × (240 + ~180) is still over 6,000. Making the registry fit the
orientation is a separate defect, listed as a follow-up, not claimed here.

### The checks — all three are advisories

The precedent for every epoch-gated check is an **advisory**, and the code says why
(`sdlc_core.py`, the architect-pass and design-review advisories: a warning there "would
redden --strict CI"). A fixed epoch cannot protect a user who upgrades later: anything
written between the release and their upgrade was written without the rule. I take
advisories over warnings: pro, no project goes red at upgrade, and the finding still
prints in every `validate`/`check`; contra, `--strict` CI does not enforce the rule on
new work — the agent and the closure review do.

- **A1 — undated Diary text.** For an ANALYSIS with `level: L3` and `start_date` on or
  after `CHRONOLOGY_EPOCH`: text in the Diary before the first opener, or a `### `
  heading inside the Diary that is not an opener, named with its line. `####` and deeper
  headings are sub-structure of an entry and are not flagged (archived sub-designs such
  as `ANALYSIS_course_slide_content.md`'s `#### Objective` stay legal under a dated
  entry). Comments are ignored.
- **A2 — `next:` is not one step.** For a `HANDOFF_*.md` with `level: L3` and `updated:`
  on or after `CHRONOLOGY_EPOCH`: `next:` longer than 240 characters (this repository's
  maximum is 214). Files never touched under the rule keep their long `next:` and are
  never flagged — a population declared below.
- **A3 — id used elsewhere.** In `check` (not `validate`), where git is available, and
  only when the tree has an **open L3 unit**: an ANALYSIS with `level: L3` and status
  PLANNED or IN_PROGRESS, or a request record (request records exist only at L3/E3,
  r26) whose `analysis:` is absent from the tree or names such an open ANALYSIS — a
  closed unit's record, kept forever by r26, does not count. For each such unit's id (`[A-Z]-\d{3,}`), another ref (heads, remotes, tags)
  that uses it for a **different analysis** — identity is the ANALYSIS file name,
  declared by the ANALYSIS or announced by the request record's `analysis:` field.
  Names the id, both analyses and the ref, and says "if this is the same unit under its
  old name, ignore it". With no open L3 unit nothing runs. Silent without git; reads
  local refs only, so it is as fresh as the last fetch (the doctrine says to fetch
  first). Spikes carry no id and are not scanned. Replay: `probe_ids.py` sees the F-069
  case (kb_site against kb_graph_speed) and is red without the other refs; main is
  clean today.

Epochs read a **value** the file carries, never an mtime (F-028 T9).

### Parallel work

- **(a) Feature ids.** Doctrine: a new unit's id is chosen **after fetching**, as the
  first id free on every branch and tag the checkout can see. Mechanism: A3. Measured
  basis in the Impact.
- **(b) Shared hand-written files.** No new product mechanism (Impact). One dogfood fix
  here: this repository's `.gitattributes` lacks the `REVIEW_LOG.md merge=union` stanza
  that `init` writes for every user.
- **(c) Two sessions, one checkout.** Doctrine, Phase 4 "Isolate the work": a session
  that may run while another uses the same checkout works in its **own git worktree**,
  and never switches branch, stashes, resets or runs `index` in a checkout another
  session may be using. Generalizes the Hybrid-only worktree sentence already there.

### Cost (Non-Goal 3)

| Added | Removed |
|---|---|
| A1 (advisory, L3, analyses started under the rule): the date goes first, "current state" is a dated entry. Write cost ≈ 0 for the 59–83% of entries already date-first | the undated "current state" paragraph re-dated from git at every resume (R1) |
| A2 (advisory, L3 HANDOFFs touched under the rule): `next:` ≤ 240 chars | the state written twice (Diary and `next:`); in the field, up to ~18.7k characters of paraphrase leave the registry as HANDOFFs are touched or closed |
| A3 (advisory, `check` only, where git exists, only while an open L3 unit exists): one `git grep` over local refs; measured 3.5 s per scan in the probe with per-ref `rev-parse` calls, 0.5 s without them, target < 1 s at implementation, re-measured before release. **An L1/L2 closure in a repository with an open L3 unit pays this runtime**, and sees a line only when a collision exists — disclosed, not zero | renumbering a unit after its id has spread: three in this repository in the two weeks to 2026-10-17, one leaving a permanent tag and commit message with the old id |
| a fetch before choosing an id (doctrine) | — |
| doctrine text: the grammar paragraph and one row per place in `templates.md` ×4; two sentences in `SKILL.md` ×4 (ids, worktree); the `next:` sentence in the HANDOFF Write Trigger ×4 | — |
| L1/L2: no step, no field, no finding about their own work (R7; A1/A2 gated on `level: L3`); A3's runtime above is the one cost they can pay | — |

The doctrine bytes are measured at implementation (UTF-8 LF, per lens) and reported
before release. **Owner acceptance for A1, A2, A3 and those bytes: given 2026-10-17 (R8)**: the
removals are real but are not of comparable kind, so this analysis does not claim the
budget balances by itself.

### Acceptance criteria

1. The dated forms in the corpus are read with the right date and label; continuation
   lines — a date later in the line, an indented bullet, a hard-wrapped line, a non-date
   boundary — are not openers (`probe_rules.py` P1/P2: 17/17 green; under a negated
   grammar with no block rule the six P2 cases fail).
2. `validate` and `check` on this repository and on the golden fixtures print **no new
   finding** (P3: 0 analyses checked; A3 on main: clean).
3. A fixture L3 analysis started on the epoch with an undated preface, or an undated
   `### Stato corrente`, gets A1 naming the line; the same file dated the day before, or
   at `level: L2`, gets nothing; a `#### Objective` under a dated entry gets nothing.
4. A fixture L3 HANDOFF with `updated:` on the epoch and a 241-char `next:` gets A2,
   **once**, as an advisory, through `sdlc_check.py` and through `mkt_check.py` on both
   an `mkt_docs` and an `ai_docs` root; `validate --strict` exits 0 on all three.
5. `request_entries` reads every heading here (34) with none unparsed and names
   `### R4-nota …` as unparsed.
6. A3 fires on a fixture repository with two branches declaring one id for two
   analyses, names both, once, through `sdlc_check.py check` and `mkt_check.py check` on
   both roots; it is silent when the second branch is absent, with no git, and when the
   only open unit is L2, or when the only trace of an L3 unit is the request record of a
   COMPLETED analysis. A rename fixture (same id, the ANALYSIS renamed on one branch)
   prints the message with its "same unit under its old name" clause — the declared
   residual, not a silence.
7. F-072 can build its event list from `entry_openers`, `request_entries`,
   `frontmatter_date`, `parse_review_log`, `adr_date` and `section_lines` alone (checked
   on its branch after merge, by its owner — not in this unit).

## Interface Contract

Surfaces an actor perceives: the validator's messages (agent and CI), the templates
(the agent writing), the reader functions (F-072). Existing idiom reused: the per-file
`rel: message` advisory of `cmd_validate`; no new idiom.

- UC2 — `validate` → A1: `solutions/ANALYSIS_x.md: Diary line N: undated text before the
  first dated entry` / `… heading '### …' is not a dated entry — open entries with
  **YYYY-MM-DD — label.**`.
- UC3 — `validate` → A2: `audit/HANDOFF_x.md: next: is N chars (> 240): one next step
  here, the state goes to the Diary as a dated entry`.
- UC4 — `check` → A3: `id F-0nn (ANALYSIS_a.md) is also used by ANALYSIS_b.md on
  <ref>: choose the first id free on every ref`.
- UC5 — readers return plain values (date, label, line) and an `unparsed` list; nothing
  is formatted for display.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| Read one section's body | EXISTS | `sdlc_core.section_body` (stops only at `## `, so `###` openers survive) | read; verified by the reviewer |
| Read frontmatter | EXISTS | `sdlc_core.load_frontmatter` | read |
| Read dated review rows | EXISTS | `sdlc_core.parse_review_log` | read |
| Read a note's / sidecar's date | **INADEQUATE** | two inline uses: `knowledge.kb_cmd_orient`'s recency probe **parses** a note's date (`kb_unquote` + ISO prefix); `knowledge.kb_build_corpus_index` **displays** the raw value in a generated, alignment-checked index. Gap: no callable parser | read ~889–903, ~1927–1955 |
| Read dated entry openers | **MISSING** | searched `sdlc_core.py`, `knowledge.py`, `docs_site.py` (161b254): none; `chronology()` returns `[]` | grep "Diary": only the section alias |
| Read request-record headings | **MISSING** | none; `sdlc_check.py` only excludes `audit/requests/` from the catalog | grep "requests/" |
| Read an ADR's date | **MISSING** | none | grep "ADR_", "**Date" in `sdlc_core.py` |
| Gate a per-ANALYSIS check on a date the file carries | EXISTS | `design_review_due` + `DESIGN_REVIEW_EPOCH`, `ARCHITECT_PASS_EPOCH` (advisories) | read |
| Read workstream frontmatter | EXISTS | `sdlc_core.list_workstreams` | read |
| Catch a reused id inside one tree | EXISTS | `cmd_validate` duplicate-id ERROR | read |
| Catch a reused id across refs | **MISSING** | none | `probe_ids.py` |
| Merge an append-only table without a human | EXISTS | `merge=union` written by `scripts/init.js` ×4 | read `init.js` |

New components, in their own vocabulary: **`entry_openers`**, **`request_entries`**,
**`adr_date`** in `sdlc_core.py` ("the dated entries a document declares"); **`ids_on_other_refs`**
in `sdlc_core.py` ("ids an open unit shares with another analysis on any ref");
**`frontmatter_date(meta)`** in `knowledge.py`, beside `kb_unquote`, which it needs
(knowledge imports sdlc_core, not the reverse; F-072 imports both).

Guide question: no CURRENT guide covers the validator's readers; this unit builds no
model of a high-complexity component beyond the ledger, so no `source_kind: code` guide
is owed. `GUIDE_release.md` governs packaging at implementation.

## Impact

| Path | Change | Why (serves) |
|---|---|---|
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` (shared ×4 via `shared_files.py`) | MODIFY | ADD `ENTRY_OPENER`, `entry_openers(body) -> [(date, label, line)]`, `undated_diary_lines(body) -> [(line, text)]`, `request_entries(text) -> (entries, unparsed)`, `adr_date(name, text) -> str or None`, `ids_on_other_refs(root) -> [(id, mine, theirs, ref)]`, `CHRONOLOGY_EPOCH`, `NEXT_MAX_CHARS = 240`, `chronology_advisories(root) -> [str]` (A1, A2); `cmd_validate` appends A1/A2 to advisories; `cmd_check` appends A3 (UC2–UC5) |
| `…/scripts/knowledge.py` (shared ×4) | MODIFY | ADD `frontmatter_date(meta)`; `kb_cmd_orient`'s recency probe calls it (r11; UC5). `kb_build_corpus_index` is **not** changed: it displays the value as written, and unquoting it would change a generated, alignment-checked file and raise `corpus/INDEX.md not aligned` on every kb project with a quoted date at upgrade |
| `…/scripts/test_chronology.py` | ADD (shared ×4) | acceptance criteria 1–6, each with a mutation that turns it red |
| `…/scripts/shared_files.py` ×4 | MODIFY | add `scripts/test_chronology.py` to `SHARED_FILES` |
| `…/scripts/shared_manifest.json` ×4 | MODIFY | regenerated by `shared_files.py --update` |
| `distributions/mkt-agentic-sdlc/…/scripts/mkt_check.py` | MODIFY | `Report` has only errors and warnings, and `exit_code(strict)` fails on any warning, so advisories get their own channel: `main` prints them as `[advisory]` lines outside `Report`, never counted by `exit_code`. A1/A2: called **only when `docs_dir() != "ai_docs"`** — on an `ai_docs` root `main` already runs `sdlc_core.cmd_validate`, which prints them (criterion 4). A3: `main` never calls `cmd_check` (`run_check` replaces it), so the `check` command calls `sdlc_core.ids_on_other_refs` itself, **unguarded**, on both roots, once (criterion 6) |
| `templates.md` ×4 (code, kb, mkt, course) | MODIFY | Diary section comment: the grammar, "current state = the latest entry"; HANDOFF frontmatter: `next:` one step; project notes: event vs standing note; SPIKE `## Answer / Outcome` dated (code, kb, mkt); `id:` comment: choose after fetching; kb only: sidecar `date:` = day received |
| `SKILL.md` ×4 | MODIFY | Write Triggers HANDOFF row: `next:` = one step, state to the Diary; Phase 4 "Isolate the work": own worktree for a concurrent session (c); one clause on choosing an id (a) |
| `…/scripts/test_skill_invariants.py` ×4 | MODIFY | invariants: templates state the grammar; SKILL states the worktree and id clauses |
| `CHANGELOG.md` ×4 | MODIFY | `[Unreleased]` (`GUIDE_release.md`) |
| this repository: `.gitattributes` | MODIFY | `ai_docs/audit/reviews/REVIEW_LOG.md merge=union` (dogfood; (b)) |
| this repository: `ai_docs/audit/project_notes.md` | MODIFY | the four event notes reopened as `**YYYY-MM-DD — label.**` |
| `docs_site.py` | **not in this unit** | F-072's consumer; it calls the readers after both branches merge |

**Blast radius.** Instrument: `grep` over the four distributions (devPNT off, no symbol
graph); the reviewer re-enumerated independently and matched. `cmd_validate` callers:
`sdlc_core.cmd_check`, the `validate` dispatch in `sdlc_core`, `knowledge.kb_cmd_validate`
(×4 copies), `mkt_check.main`; `course_check.py` has no validate path of its own. All
reach A1/A2 through `cmd_validate` except `mkt_check.run_validate` on an `mkt_docs` root,
hence its guarded call. `cmd_check` callers: the `check` dispatch ×4; `mkt_check` replaces
`cmd_check` with `run_check`, hence its own A3 call. `frontmatter_date` consumers:
`kb_cmd_orient` (recency line must stay byte-identical: existing recency tests); the
second inline use, `kb_build_corpus_index`, is a display, deliberately left unchanged
(Impact row). Missing the mkt
call = advisories silently absent for marketing, the F-028 defect.

**Populations at rest** (triggers evaluated: no invariant moves between read and write
time; no Non-Goal forbids migration; no column changes type; no
`redact`/`mask`/`filter`/`sanitize`/`authorize` function changes). Named anyway:
- the 217 Diary openers and the undated blocks already written stay under the old
  regime forever — read by the tolerant reader, never checked; undated legacy text
  yields no event. Accepted: migrating 58 analyses buys a chronology of the past that
  git already holds.
- HANDOFF files with a long `next:` that are never touched again are never flagged and
  keep their size in the registry until their unit closes.
- units opened before A3 under an id another ref uses are flagged only while open.
- a unit whose ANALYSIS was renamed while a tag (permanent) or an unmerged branch keeps
  the old name under the same id is flagged as colliding with itself for as long as it
  stays open; the message says how to recognise it. Accepted: the identity is the only
  one the documents carry, and the alternative — silence on renames — would also hide
  the real collisions, which are renames of nothing.

### Parallel work — measured, then decided

**(a) Ids** (`probe_ids.py`, `probe_parallel.sh`, and the records). Committed ANALYSIS
files never collided (61 `id:` additions in the rewritten history, 323 commits, 24
branches) — but that count is blind to the real cases, because each was renumbered
before it reached a ref under the shared id. The records show **three renumbers in the
two weeks to 2026-10-17**, all found on that day when work moved between branches:
F-065 → F-071 (`ANALYSIS_intent_focus.md`; the archive tag and its commit message keep
F-065), F-068 → F-070 (`REQUEST_npm_whats_new.md` R5), F-069 → F-072
(`REQUEST_kb_site.md` R18, caught by the owner). A fourth id class, rulings, carries
`r19` twice since 2026-09-06, noted and left in `ANALYSIS_capability_tiers.md` — this
repository's own ledger, not a product artifact. The field project's ids are not
measured (not on this machine, R5). Decision: the doctrine sentence **and** A3. I take
both over the sentence alone: pro, at roughly one collision in four new ids the cost is
the renumber after the id has spread, and A3 replays the recorded case; contra, `check`
now reads git refs (fail-open without git; `mark` already shells to git) and is only as
fresh as the last fetch.

**(b) Shared files at merge.** 13 merge commits replayed in a mirror clone: 4 conflict
on named files, 1 (7b0256a) could not be replayed by `merge-tree`, 8 merge clean.
Conflicts fell on generated files (`handoff.md`, `features_history.md`, `memory/INDEX.md`,
`shared_manifest.json` — resolved by `index`/`--update`, as F-028 designed);
`audit_plan.md` (two `mark`s of one area, semantic, out of scope since F-028);
`CHANGELOG.md`; and `REVIEW_LOG.md` once (4191785, 2026-10-13, no row lost) — because
this repository's `.gitattributes` has no union stanza. `project_notes.md` and
`rulings.md` never conflicted. Edits in place: `project_notes.md` 26 of 32 commits delete
lines (notes are rewritten, "release pending" → "completed"), `rulings.md` 3 of 15,
`REVIEW_LOG.md` 6 of 84. Union is right where an edit is the exception: on a table of
independent dated rows, the rare row edited on both sides comes out duplicated and
visible, never lost — so union stays for the review log. Where editing is the norm, as
in the project notes, union would keep both versions of the same note — wrong. Shared kb
topic nodes are **not measured**: they exist only in the field project (R5). Decision:
nothing new for the product; the stanza here; topic nodes measured on the field machine
before any design.

**(c) Two sessions, one checkout.** Recorded twice: F-019 (2026-07-27, "the last writer
won") and `ANALYSIS_kb_ingestion_rhythm.md` (another session's `index` picked up an
uncommitted HANDOFF). Today the primary checkout has three attached worktrees and an
untracked nested copy `agentic-sdlc-skill/` (1,011 files, origin unknown, untouched).
The doctrine names worktrees only for Hybrid. A validator cannot see sessions, so the
answer is the sentence, at zero check cost.

## Security and Threat Model

Surfaces: the validator reads files under the docs root and, for A3, local git refs;
its output reaches CI and the agent; the readers' output reaches F-072's HTML.

| Threat | Answer |
|---|---|
| T1 — a regex over document text runs slow on a crafted line | the opener pattern is anchored with no nested quantifier; the label is cut at 120 chars. Test: a 100k-char line returns in < 50 ms |
| T2 — a new finding reddens `--strict` CI at upgrade (the F-019 trap) | all three are **advisories**, which never fail a build; epoch-gated on values in the file. Test: golden fixtures and a post-epoch fixture with a legacy-length `next:` keep `validate --strict` exit 0 |
| T3 — the epoch is evaded by back-dating `start_date` | accepted, as for `DESIGN_REVIEW_EPOCH`: the field is the author's declaration; a review reads the request record's R1 date beside it |
| T4 — an undated paragraph after an opener silently takes the date above | residual, declared: no structural reader can tell a new undated entry from a continuation. The doctrine states the consequence to the writer; A1 catches the two detectable shapes |
| T5 — a label carries markup or script into F-072's page | readers return plain text; escaping is F-072's sanitizer's duty (its spec), stated so neither side assumes the other |
| T6 — advisories missing from, or doubled in, one entry point | criterion 4 runs `mkt_check.py` on both roots through its real entry point |
| T7 — `frontmatter_date` changes kb output | recency line byte-identical (existing tests); the corpus index does not call it, so no generated file changes at upgrade |
| T10 — advisories become warnings in an entry point without an advisory channel (mkt) | mkt prints `[advisory]` lines outside `Report`; criterion 4 asserts `mkt_check.py validate --strict` exit 0 on a post-epoch fixture |
| T8 — A3 runs git on input from the documents | the only git arguments are fixed subcommands, ref names from `for-each-ref` and fixed pathspecs; no document value reaches a command line; `subprocess` with an argument list, no shell |
| T9 — A3 on a large repository slows `check` | one `git grep` over all refs; measured and reported before release; A3 skipped (one advisory line) above a stated ref count |

No secrets, personal data, network or authorization surface is touched.

## Action Plan

- [x] A — readers, `CHRONOLOGY_EPOCH`, `NEXT_MAX_CHARS`, `adr_date`, `frontmatter_date` (TDD from `test_chronology.py`).
- [x] B — A1/A2 via `chronology_advisories` in `cmd_validate`; A3 via `ids_on_other_refs` in `cmd_check`; mkt wiring on both roots.
- [x] C — doctrine: `templates.md` ×4, `SKILL.md` ×4; invariants.
- [x] D — dogfood: `.gitattributes` stanza; four project notes reopened; `check` CLEAN.
- [x] E — `SHARED_FILES` ×4, `shared_files.py --update` ×4, four batteries, drift guard; doctrine bytes and A3 runtime measured and reported to the owner.
- [x] F — closure review on the diff; `index`; CHANGELOG ×4; owner decides merge and release.
- Out of this unit, for the owner: the duplicate `r19` in `vision/rulings.md` (a ledger row changes only by owner ruling); the untracked `agentic-sdlc-skill/` in the primary checkout; the registry not fitting the orientation cap; kb topic-node conflicts measured on the field machine.

## Test Strategy

`test_chronology.py`, shared: each acceptance criterion a test, each with a mutation
that turns it red (no block rule for 1; epoch or level gate removed for 2–4; the mkt
guard removed for 4 — doubled line; unparsed list dropped for 5; refs not consulted for
6). T1 timing, T2 strict exit code, T7 byte-identity, T8 no shell. Full battery ×4,
drift guard, `npm pack` contents unchanged except the new test file. The probes in
`harness_doctrine_chronology/` stay as the record of the measured numbers.

## Diary / Current State

**2026-10-17 — opened from its handoff, on branch `doctrine-chronology`** (worktree
`wt-chronology`, cut from `origin/doctrine-chronology`). Standalone, devPNT off.
`Level: L3 · router: GUIDE_release.md → read at implementation (packaging); no guide
governs the design.` Elicitation skipped except one question: the spec is set by R1–R6,
the handoff and the measurement; L2 coverage was a real doubt (the Vision ranks neither
side) and was asked — R7, "No, keep L2 free".

Measured before designing; the finding that reframed `next:`: `orient` cuts each document
at 6,000 chars, so a long registry is partly invisible to a cold agent. The readers were
probed before the prose.

**2026-10-17 — design review round 1: FAIL, 3 BLOCK + 8 WARN** (independent subagent,
Opus 5.5, deep tier, fresh context, read-only). All folded above:
- B1, false openers: a hard-wrapped line beginning with a date read as an event (six in
  `ai_docs/`). Now an opener must start a block. The reviewer's second fix, a required
  separator, was tried and rejected by the probe: it lost 52 real openers.
- B2, "never reddens at upgrade" was false: a fixed epoch cannot protect a late upgrader.
  The checks are now advisories, following the precedent the code already states.
- B3, "zero collisions" was an artefact of the instrument: the records show three
  renumbers in two weeks, invisible to a scan of committed `id:` lines. The decision
  changed from a sentence to a sentence plus A3, with `probe_ids.py` replaying F-069.
- W1 every check gated on `level: L3`; W2 the orient-fit claim withdrawn, the 16,000
  total cap named; W3 the second date reader (`kb_build_corpus_index`) enumerated and
  `frontmatter_date` placed beside `kb_unquote`; W4 `adr_date` named; W5 mkt doubling,
  `SHARED_FILES` and the mkt SPIKE template added; W6 union kept for the review log with
  its reason, merge counts stated; W7 readers return openers only, the probe regex made
  normative; W8 `####` sub-structure exempt from A1.

**2026-10-17 — design review round 2: FAIL, 1 BLOCK + 4 WARN** (same reviewer, scoped).
Round 1 verified closed by execution, B1 by the block rule alone (218 openers kept, the
one false opener rejected; the separator rejection confirmed). New, all folded:
- N1, B2 back in one entry point: `mkt_check.Report` has no advisory channel and fails
  `--strict` on any warning. Advisories now print outside `Report` there; T10 added.
- N2 A3 wiring in mkt made explicit (unguarded, on both roots); N3 A3 gated on open L3
  units and its residual L1/L2 runtime disclosed in the Cost table; N4 rename residual
  declared, id regex `\d{3,}`, spikes stated as unscanned; N5 the corpus index left
  unchanged, since unquoting it would raise an alignment ERROR at upgrade.

**2026-10-17 — design review round 3 (the cap): PASS, 1 WARN, folded.** W-a: the A3
gate counted every request record as an open unit, though r26 keeps them after
closure; a record now counts only when its `analysis:` is absent or open, with a
fixture in criterion 6. Design approved by the reviewer; awaiting the owner's decision
on the cost (A1, A2, A3, doctrine bytes) before implementation.

**2026-10-17 — cost accepted (R8).** The owner accepted A1, A2, A3 and the doctrine
bytes; the bytes are still measured at implementation and reported before release.
Design committed on `doctrine-chronology`, not pushed. Next: implementation step A.

**2026-10-17 — implemented, steps A–E; closure review next.** `test_chronology.py` was written
first and run red (no `CHRONOLOGY_EPOCH`); 28 tests now green, and each declared mutation
turns one red (block rule, level gate, epoch gate, the 240 cap, the unparsed list, refs not
consulted, a closed unit's record counted, the mkt guard removed). Batteries green ×4: code
280, kb 471, mkt 292, course 287; manifests identical; `npm pack` lists no test file.
`check` here: the same 0 errors, 22 warnings, 16 advisories as before (criterion 2); `stale`
fails only until closure's `mark`.

Measured for the owner: A3 takes 0.33 s over this repository's 121 refs, with no collision;
doctrine bytes (UTF-8 LF) are SKILL.md +529 per lens, templates.md +1,198 code, +1,289 kb,
+676 mkt, +316 course. `CHRONOLOGY_EPOCH` is 2026-10-18; A3 is skipped above 300 refs.

Deviations from the design, both small: `id_advisories(root)` formats A3 once for the spine
and for mkt (the design named only `ids_on_other_refs`); `ids_on_other_refs` returns one
tuple per (id, other analysis) with every ref listed, so a branch and its remote print one
line. A residual the design did not name: a marketing request record carries `unit:` and no
`analysis:`, and identity is the ANALYSIS name, so a marketing engagement with no ANALYSIS
is not checked by A3; the mkt CHANGELOG says so, and the mkt SKILL.md drops the coverage claim
the other lenses make.

**2026-10-17 — closure code review: FAIL, then PASS (2 rounds).** Same reviewer as the design,
fresh context, read-only. Round 1, 1 BLOCK + 7 WARN + 1 CANNOT VERIFY, all fixed with a test
each: F1 `entry_openers` now blanks comments like `undated_diary_lines`, so an entry under the
template comment is an event to both; F2 A3 found nothing when the docs root sits in a repository
subdirectory (prefix doubled); F3/F4 `git grep -z -n` with quotePath off, and only frontmatter
keys count; F5 a new shared reader `section_lines` keeps the body unstripped, so A1 prints the
file line and an indented first line is not an opener; F6 `--strict` exit codes asserted; F7 T8
and T9 tested; F8 refs grepped in batches of 50, and a failed or timed-out scan says it was
skipped instead of reporting clean; F9 the Diary's mkt sentence corrected. Round 2 PASS with 3
WARN, folded: the reader table names `section_lines`; only refs that resolve to a commit are
grepped (a tag on a blob no longer disables A3); output split on newline only, with a test across
the batch boundary. Next: the owner's commit decision, then `mark` and closure.

**2026-10-17 — closed: COMPLETED, merged into main by the owner.** Committed as f9661b5
(implementation) and 0fb1abe (`mark`), on the owner's approval; `check` CLEAN. No ADR: the
readers and advisories follow the patterns already in place (shared readers in the spine,
epoch-gated advisories, `git` shelled with fixed arguments as `mark` does), so no new
architectural decision was taken. Left for the owner, outside this unit: the duplicate `r19`
in `vision/rulings.md`; the untracked `agentic-sdlc-skill/` copy in the primary checkout;
the registry not fitting the orient cap; kb topic-node conflicts measured on the field machine;
whether marketing engagement HANDOFFs declare `level: L3` (A2) and how A3 should identify an
engagement with no ANALYSIS; F-072 wiring its chronology to these readers. Release not decided.
