---
description: F-072 - docs site. A stdlib-only generator shared by the whole skill family shows the user, simply and visually, what the agent reads to orient itself and to resume work - what the project is, what was done and when, what is open and its next step, what is known - from the project's own documents, offline and read-only.
status: IN_PROGRESS
feature: F-072
id: F-072
start_date: 2026-10-16
end_date:
level: L3
domain: code
branch: feat/kb-site-spec
---
# ANALYSIS: docs site — what the agent sees, made visible (F-072)

## Objective

The agent working on a project knows what the project is, what was done lately, what is
open and what comes next, and what is known — because it reads the project's documents
to orient itself and to resume work. The person it works with does not see any of this
unless they open the same Markdown files and know the skills' vocabulary.

This unit adds to every distribution of the family one shared generator that turns a
project's docs root into a static website, opened from disk, offline, read-only, in plain
English, that shows the user **what the skill has created and manages, so they understand
what was done, when, what is to do and what knowledge was acquired**
([REQUEST_kb_site.md#R20](../audit/requests/REQUEST_kb_site.md); R1, R7, R8, R14). It is
the full specification for an implementer working from it alone (R9). Figures about real
data come from `harness_kb_site/probe.py`, run on a production knowledge-lens project and
on this repository (counts only; exit 1 on a failed assertion; `--red` shows a failure).
`solutions/SPIKE_kb_viewer.md` showed the approach works with no dependency.

## Feature Vision

**The principle — it orders everything else.** The site shows the user **what the agent
reads to orient itself and to resume work: the same sources, simply and visually, no more
and no less** (R20). Every page answers one of four questions:

| Question (R20) | What the agent reads | What the site shows |
|---|---|---|
| What is this project? | at orientation: the docs root's README, the canonical manifest, the guide router | the project in a few lines; its rules; the manifest as a lookup inventory |
| What was done, and when? | on resuming: the analyses' Diary; the request records, notes and review log behind them | a chronology of events the documents date — **not git history** |
| What is open, and what comes next? | at orientation: the open-work register with each unit's next step, and the project-wide notes | open work, units of work and the project notes, as declared (Vision v9) |
| What is known? | the topic index, the claims and their sources | topics, facts with provenance and the exact passage, source documents |

**Check rule.** Everything the agent reads to orient itself or resume work is in the site;
the site shows nothing the agent does not have. A proposed page or field that fails this
check is out of scope.

**Alignment.** `vision/project_vision.md` (APPROVED, v9): the site advances "keep
understanding durable across sessions". It is a family capability authored once in the
shared spine (R14); stdlib Python, no network; optional, so nothing becomes mandatory at
any level. Its standing cost is one line of about 160 bytes in each lens's `SKILL.md`,
accepted (R13, R15). The work pages rest on the Vision v9 amendment (R11, R12).

**Placement** (`vision/rulings.md`):

| Surface | Placement |
|---|---|
| The site, every lens | new row **r29** (below), basis R14, R20 |
| Open work, units of work | **r27**, the read-only state view under v9's six conditions (criteria 10–14) |
| Per-item counts (facts per topic, per source; shared sources) | **r28** (R10, R13): beside each item, never used to select, order, filter or flag |
| Chronology | dated **events**, not units' states: no analysis start or end, no filter by any state; "Lately" is the most recent events (R23) — answers "what happened, when", never "what next" |
| Project-wide notes, request records, review log | documents the agent reads, shown as written, each on its own page (R23) |
| Reading state of a source; legend toggles | on the source's own page only; origins and node kinds only (R10) |

r29, written at closure: "generates, in every lens, a static read-only site of what the
agent reads to orient itself and resume work — the project's documents, its knowledge
base, the read-only state view (r27) and a chronology of dated events — selecting,
ranking and recommending nothing beyond r27 and r28" — ADMIT; basis R14, R20, R23.

**Non-goals.** No editing, no server, no hosting or sharing (R2); no translation (R6); no
git history; no full-text search of source extractions.

**Success signal.** A user opening the site understands, without opening a file or asking
the agent, what the project is, what was done lately, what is open with its next step, and
what is known — and from any fact reaches its origin and passage in one click.

## Use Cases / User Needs

For the solo developer, the team lead and the practitioner in a non-code domain (Vision
Actors), each reading their own project:

- **UC1 — Get oriented**: the home page answers the four questions.
- **UC2 — Follow what was done and when**: the chronology.
- **UC3 — See what is open and what comes next**: open work, project notes, units of work.
- **UC4 — Read the project's rules and documents.**
- **UC5 — Explore and check what is known** (knowledge base present).
- **UC6 — Search.**

Names: *fact*, *topic*, *area*, *source document*, *note*, *open work*, *features* (R1)
— EXISTS under the skills' terms; *site*, *chronology*, *lately*, *rules*, *units of
work*, *statement mark* — NEW.

## Functional Spec

### Pages

| Page | Present | Built from |
|---|---|---|
| Home | always | README, Vision, manifest, guide router, open-work register, project notes, topic index, chronology |
| Chronology | always | events the documents date |
| Open work | always | the open-work register (each workstream's resume notes) and the project notes |
| Features (code and knowledge projects) / Courses (course projects) | always in those lenses; **absent on a marketing project**, which keeps no analysis per engagement (R23) | each analysis |
| Rules | always | Vision, principles, decision records |
| Guides | always | the guide router, operative guides, code-comprehension guides (R26) |
| Documents | always | the documents the shared project-memory catalog lists (R17) |
| Map, topics, facts | when there is at least one topic | the topic index and claim rows |
| Source documents | when there is at least one source sidecar | sidecars |
| Search | always | all of the above |

Request records, the review log, the project notes and the resume notes have their own
readable page, reached from the chronology, the home page and Open work, but are not in
the Documents tree (R23). An always-present page with nothing yet says in one line what
will appear and when (R17).

### Home

**The North Star first (R25).** When the Vision has a section whose title starts with
"North Star", it is shown in full, as written, above the four blocks, with the Vision's
status and a link to it; without one, the Vision's first section stays in **This project**
and is not called a North Star.

Four blocks, one per question, each opening its page: **This project** (the README's
first heading and opening paragraph; the Vision's status, and its first section as written
when the Vision has no North Star -- with one, the North Star is shown above the blocks;
links to Rules and to the manifest); **Lately** (the ten most recent chronology events);
**Open now** (each open workstream's name, status and next step, and the project notes);
**What is known** (with a knowledge base, the areas and their topics).

### Chronology (R20, R22, R23)

Dated **events** the documents declare, most recent first, each with its date, its label
as written, the kind of document and a link to it: dated Diary entries of analyses,
request-record entries, notes, source documents received, review-log rows, decision
records, dated lines in the project notes. Field: 653 events; this repository: 343
(probe). No analysis start or end date, no filter by any state, no other ordering; git
history is never read.

**Dependency.** Which lines count as dated events, and in what form, is set by the
doctrine unit on dated entries, F-073 (branch `doctrine-chronology`, opened 2026-10-17; R22). The chronology reads them with
that unit's rules and the validator's existing readers; this document does not define the
parsing.

### Open work and units of work (Vision v9)

- **Open work**: one card per open workstream — name, status, level, since, last updated,
  branch, and its next step **in full, verbatim**; "Read the resume notes" opens them.
  Below the cards, the project-wide notes, as written. Order: status group (table below),
  then the declared `updated:` date, most recent first; a missing date last; ties by name.
- **Features / Courses**: one entry per analysis — name, id as written, status, level,
  lens, dates; columns by status group (no counts) or a single list; always sorted by id
  as text, the feature history's lookup order, which v9 admits; filter by lens only.
- The six v9 conditions hold: built from the documents on every run; nothing computed,
  counted or ranked; the fixed order above; the only action is opening a document; no
  assignee, owner, due date, iteration, team or role; nothing shipped tells an agent to
  choose, prefer, avoid, skip or order units from these pages.

**A feature's page (R24).** An analysis opens as its document with, above it, the chain
the agent works through, one step per row, each linking to its sections as written:
**Vision** (Objective, Feature Vision or Vision Alignment) · **Use cases** · **Flows and
interfaces** (Functional Spec, Interface Contract) · **Risks** (the lens's risk section:
Security and Threat Model, Sources and Verification, Threat Map / Plan Risks, Learning and
Content Risks) · **Solution study** (Capability Ledger, Impact) · **Design and tests**
(Action Plan, Test Strategy) · **Merge and tests** (the unit's merge brief
`MERGE_REVIEW_<feature>.md` and E2E script `E2E_TEST_<feature>.md`) · **Diary**. The request
record `audit/requests/REQUEST_<feature>.md` and the project's North Star (R25) are linked
beside the Vision. A step with no
section says "Not in this analysis" — a fact about the document, never a score; the order
of the document is unchanged; sections outside the chain stay where they are. Headings are
matched with the validator's own section names; Hybrid governed artifacts are not on the
filesystem and are out of scope.

**Status words** (case-insensitive): `BLOCKED` blocked (1) · `PLANNED`, `TODO` planned (2) ·
`IN_PROGRESS`, `PROGRESS` in progress (3) · `PAUSED`, `ON_HOLD` paused (4) · `COMPLETED`,
`DONE` completed (5) · `CANCELLED` cancelled (6) · `ARCHIVED` archived (7) · anything else
as written, under "other status" (8). A value marking a unit as available or next to take
(`READY`, `NEXT`) is not a group (v9).

**Outside Open work and Features / Courses, nothing lists, orders or filters documents or
work by a state value.** Per-item counts appear only as r28 allows; tables sort by name
and date only.

### Rules and documents

**Rules**: the Vision (status shown as declared), principles and decision records — what
the project has decided. **Guides** (R26), a page of its own: the guide router first (which
guide to read before which task), then the operative guides with their when-to-consult
line and declared status, then the code-comprehension guides ("How it works") — how work
is done here and how its complex parts work. The canonical
manifest is shown as written, as a lookup inventory. **Documents**: the catalog's list by
folder with plain folder names, title per entry, no status or date in the tree; a document
page shows its frontmatter as labels and the body formatted. With a knowledge base, a
**12-hex-digit** token in backticks that is a fact id becomes a link; another 12-hex token
is marked "Not a fact id in this knowledge base". Relative links open inside the site.

### What is known (knowledge base present)

- **Map**: three views — topics (sized by fact count, coloured by area; edges *part of*,
  *related*, and *share source documents*, marked as computed); one topic up close
  (`#/map/<slug>`: its facts, their sources and notes, *based on* and *newer version of*
  edges, replaced and in-conflict links); everything (≈6,240 nodes in the field). The
  legend switches off origins and node kinds only. The map appears laid out and framed.
- **Topic page**: name (first heading, else slug, as written — R6), area, description,
  also known as, known gaps, related topics, sub-topics, facts in row order with origin
  and marks; filters by words and origin. A merged topic is neither counted nor drawn;
  its address forwards to its successor.
- **Fact panel**: text; origin and its explanation; **holds when, value, also concerns,
  as written** (never evaluated); replaced — with the current fact at the end of every
  branch of its chain, a loop or a missing id stopping with a message — or in conflict,
  with the other facts; for an inferred fact, what it rests on — documents, a person's
  statement, a decision, another knowledge base — or which part could not be traced; for
  each source the exact passage, highlighted, with its page or lines, or why it could not
  be found. A fact resting on a person's statement carries a "statement" mark wherever it
  appears and the notice "Not found in a document. Treat it as a statement, not as
  documented evidence."
- **Source documents** (`#/source/<name>`): name, kind, date, facts taken, topics using
  it; the detail adds how far it was read and its newer or older version.

Topics are listed by slug as text; a topic's area is the root reached by its first
parents, and a cycle, a missing or a merged parent gives "no area". A `derived_from:`
entry is resolved as the validator resolves it and followed only if it ends inside the
docs root (field: 157 inferred facts rest on documents or decisions, 25 reach a
statement, 8 cannot be traced).

### Search

Button and `Ctrl+K`: documents, and with a knowledge base facts and topics; ignores case,
accents, dash variants and invisible characters. No result: "Nothing found among facts,
topics and documents. The full text of source documents is not searched here — not
finding something does not mean the sources are silent on it." (without a knowledge base:
"Nothing found in the documents.").

### Words (R4, R7)

Every label is plain English; every classifying label carries its explanation. All
interface wording, including the generator's reasons, comes from one strings table.

| In the skills | On the site |
|---|---|
| claim | fact |
| `GIVEN` · `ELICITED` · `DERIVED` · `RULING` · `IMPORTED` | from a document · stated by a person · inferred · decision · from another knowledge base |
| `SUPERSEDED` · `CONTESTED` | replaced · in conflict |
| `valid` · `qty` · `about` | holds when · value · also concerns |
| root topic · `synonyms:` · `gaps:` · `related:` | area · also known as · known gaps · related topics |
| corpus artifact · note · sidecar `supersedes:` | source document · note · newer version of |
| reading frontier | read in full / up to page (or line) N [of M] / reading not recorded / not readable |
| workstream · `HANDOFF_*.md` · `project_notes.md` | open work · resume notes · project notes |
| `L1` · `L2` · `L3` · `Spike` | trivial · small · significant change · time-boxed exploration |

Explanations: *from a document* — the passage can be re-read; *stated by a person* — said
and recorded on the day, not found in a document and maybe never: treat it as that
person's statement; *inferred* — reasoned from other facts, shown with what it rests on;
*decision* — taken to settle a conflict; *replaced* — a newer fact takes its place; *in
conflict* — facts that disagree, not yet settled.

Content (titles, descriptions, facts, documents, next steps, notes) is shown as written,
never translated or truncated (R6).

### Look

Dark theme (R2): five origin hues, red for in conflict, replaced dimmed. Every page dates
itself: "Generated <date time> from commit <hash>, plus N changed files not yet
committed" (or "not a git repository"). Usable from 1024 px.

### Acceptance criteria

1. **Check rule**: every source the orientation reads (README, canonical manifest, guide
   router, open-work register, project notes; with a knowledge base, the topic index) is
   on the home page or one click from it; every page is built only from documents in the
   docs root.
2. Home answers the four questions on a knowledge-lens, a code and a marketing project.
3. The chronology lists every dated event of the kinds above, most recent first; it
   carries no analysis start or end, no state filter, and reads no git history.
4. Per-item counts equal the probe's for the same docs root, and nothing is sorted or
   filtered by them.
5. Each passage equals the span its locator addresses, read as the validator reads it;
   every branch of a replacement chain ends at a current fact or a stated stop;
   inferred-fact classes equal the probe's.
6. A fact resting on a statement carries the statement mark in every view; holds-when,
   value and also-concerns appear as written wherever the fact panel shows a fact.
7. The docs root is unchanged; the site makes no network request — no remote image,
   font or script — and works opened from disk.
8. No interface string contains, as a whole word: claim, ledger, provenance, elicited,
   given, derived, ruling, imported, superseded, contested, corpus, sidecar, locator,
   slug, frontmatter, workstream, handoff, L1, L2, L3.
9. A search with no result shows the sentence above; a search for a word written with a
   non-breaking hyphen finds it.
10. Open work and units are rebuilt from the documents on every run.
11. They show only declared values — no count, score or readiness — in the stated order.
12. The only action on any page is opening a document; filters, search and view switches
    change nothing.
13. No assignee, owner, due date, iteration, team or role is shown; next steps are
    verbatim and complete.
14. The lines this unit adds to `SKILL.md`, READMEs and CHANGELOGs name the command and
    what the site shows, and tell no agent to choose or order units from it.
15. Every analysis page shows the chain above the document: each step links to the
    sections of that step as written, a step with none says so, the merge brief, the E2E
    script and the request record are linked when they exist, and no step carries a count,
    score or completeness mark (R24). The Vision's North Star, when it has one, is shown in
    full above the home page's blocks and linked from every analysis's Vision step (R25).

## Interface Contract

**Idioms in use**: skill tools are
`python <skill_dir>/scripts/<tool>.py … --root <project>` with a one-line summary and a non-zero exit on failure; the page is new (dark
dashboard, R2; side panel; `Ctrl+K`).

**Command** (identical in every distribution):

```
python <skill_dir>/scripts/docs_site.py [--root <project>] [--docs-dir <name>] [--out <folder>] [--open]
```

The docs root is resolved as every entry point resolves it (`ai_docs` or the legacy
`mkt_docs`); ambiguous or missing: exit 2 with the resolver's message. `--out` defaults to
`<project>/.docs-site/`; refused (exit 2) inside the docs root, or when non-empty and not
written by an earlier run. Output: one summary line, exit 0; one line per unreadable file
and exit 1 when any; a note when the output folder is not git-ignored.

**Flows.**
- *Orient (UC1, UC3)*: the user opens `index.html` → the page loads the data the
  generator wrote → Home shows the four blocks → a block opens its page.
- *Follow (UC2)*: Chronology → an event opens the document it comes from.
- *Check a fact (UC5)*: a fact anywhere → `#/fact/<id>` → the panel shows what the
  generator extracted: passages, chain ends, grounds.
- *Read (UC4)*: Documents or Rules → a document page; documents load on first use
  ("Loading documents…").
- *Search (UC6)*: `Ctrl+K` → results from the index built at generation → Enter opens.

**Addresses**: `#/`, `#/chronology`, `#/work`, `#/units`, `#/rules`, `#/guides`,
`#/documents`, `#/doc/<path>` (optionally `?at=<heading id>`),
`#/map`, `#/map/<slug>`, `#/topic/<slug>`, `#/fact/<id>`, `#/sources`, `#/source/<name>`;
back and bookmarks work. **Feedback**: an address for an absent page or a removed item
shows "Not found — it may have changed since this site was generated" with a link home;
missing data shows "This site's data is incomplete — run the generator again."

**Constraints.** The generator and its page are shared spine files, byte-identical in the
four distributions and guarded by `test_drift.py`; they import `sdlc_core` and `knowledge`
and change neither. The generator is not named `site.py` (it would shadow Python's `site`
module).

## Capability Ledger

| Capability | Verdict | Component |
|---|---|---|
| docs root; frontmatter and text | EXISTS | `sdlc_core.resolve_docs_dir`, `load_frontmatter`, `read_text` |
| the orientation's sources | EXISTS | `sdlc_core.orient_docs` |
| topics, claims, cited paths; the catalog | EXISTS | `knowledge.kb_load_topics`, `kb_parse_claims`, `kb_claim_sources`, `memory_records` |
| open workstreams; analyses; default domain | EXISTS | `sdlc_core.list_workstreams`, `list_analyses`, `project_default_domain` |
| Diary section; review-log rows | EXISTS | `sdlc_core.section_lines`, `parse_review_log` |
| sources and reading state; `derived_from` entries | EXISTS | `knowledge.kb_build_corpus_index`, `kb_coverage_cell`, `_kb_df_entries` |
| commit and changed files; one file in four packages | EXISTS | `sdlc_core.git_head`, `git_changed_since`; `shared_files.py`, `test_drift.py` |
| resolve a `derived_from` entry | INADEQUATE | the ladder is a closure inside `knowledge.kb_time_cycle`; the site's walk is tested against `kb_time_cycle`'s edges |
| extract the passage a locator addresses | INADEQUATE | `kb_check_locator` validates only; probe: 5,759 of 5,759 agree, `--red` 82 disagree |
| read request-record entries, dated note and project-note lines; collect events | MISSING | the dated-entry rules come from F-073 (R22) |
| walk replacement chains and inferred grounds | MISSING | `knowledge.py` validates and cascades only |
| lay out a graph; format Markdown; render a page | MISSING | none in the repository; stdlib has no Markdown renderer |

New components: a **passage extractor** (reads exactly as `kb_check_locator`, cached per
file); a **chronology reader** (the R22 rules plus `section_lines` and
`parse_review_log`); a **chain walker** (every branch of a replacement chain; inferred
grounds, following only paths inside the docs root); a **graph layout** computed at
generation (deterministic; a layout left to browser animation stays tangled in a
background window); a **Markdown formatter with a sanitizer** that keeps only headings,
paragraphs, lists, tables, emphasis, code, blockquotes, rules and links, a link only when
relative, `#` or `http(s)`, and no images, scripts, styles or event attributes.

## Impact

**No third-party JavaScript**: the packages are Apache-2.0 with a NOTICE and stdlib-only;
canvas 2D with a precomputed layout draws the field's ≈6,240 nodes.

**New shared files** (authored in `skills/agentic-sdlc-skill/`, copied to the three other
skill folders): `scripts/docs_site.py`; `docs_site/index.html`, `app.js` (classic script),
`style.css`, `strings.js`; `scripts/test_docs_site.py` (builds its fixtures in code: a
knowledge-lens, a code and a marketing project).

**Output**, outside the docs root: the page files and `data/*.js` (classic scripts —
pages opened from disk cannot fetch JSON — written with `json.dumps` and `</` escaped).

**Existing files**: `shared_files.py` (`SHARED_FILES` + `--update`); the four
`package.json` `files` (runtime files only — no `test_*.py` in a package, per
`GUIDE_release.md`); the four READMEs and CHANGELOGs; one line in each `SKILL.md` (R15);
`strategic/skill_family_agent_workflows.md` (commands row; shared-file count);
`strategic/architecture.md` (Component Map); `strategic/existing_features.md`;
`vision/rulings.md` (r29). One release across the four packages (R14), after the R22
unit. Not touched: `sdlc_core.py`, `knowledge.py`, `entry_point.py`.

## Security and Threat Model

| Threat | Requirement |
|---|---|
| Script injection from content (mail, documents) | text inserted as text; Markdown through the sanitizer above; data files escaped; tested with `<script>`, `onerror=`, `javascript:` links and `</script>` |
| Content leaves the machine | no network request: no CDN, fonts, analytics or remote images; output scanned in tests; a note when the output is not git-ignored |
| Writing into the docs or over the user's files | `--out` refused inside the docs root or over a folder the generator did not write |
| Path traversal | a cited or derived path is followed only inside the docs root; tested with an absolute path outside it |
| A statement read as evidence | statement mark and notice everywhere (criterion 6) |
| Absence read as evidence | the empty-search sentence (criterion 9) |
| A stale site read as current | every page dates itself |
| The site drifts into work management | criteria 4, 10–14; no state filter outside the work pages |

## Action Plan

1. `test_docs_site.py` with its three code-built fixtures, red.
2. Data: orientation sources, project notes, work and units, documents, knowledge base.
3. Passage extractor, chain walker; chronology reader on the R22 rules (F-073).
4. Formatter and sanitizer; layout; search index.
5. Pages, strings table, look.
6. Shared-file list and copies; packages, READMEs, CHANGELOGs, `SKILL.md` lines; workflows
   document; Component Map; existing features; r29.
7. Runs on a real knowledge-lens project and on this repository; E2E script; closure
   review; one release.

## Test Strategy

`test_docs_site.py` (shared `unittest`, runs in every distribution), one test per
acceptance criterion on the three fixtures, plus: empty-state lines and absent pages
(marketing units, conditional pages); `mkt_docs`, ambiguous and missing roots; a
`parents:` cycle and a replacement loop terminate; a merged topic forwards; a missing
source gives its reason; the walk agrees with `kb_time_cycle`'s edges; injection and
traversal inputs; `--out` refusals; identical output across two runs. `test_drift.py`
confirms the four copies; `npm pack --dry-run` lists no `test_*.py`. The probe runs green
on a real knowledge-lens project and on this repository before closure. In a browser:
each page on the fixtures and on a real project, opened from disk with the network off —
the owner's E2E script.

**Guides.** `GUIDE_release.md` → read (new support files; verification battery);
`GUIDE_shared_project_memory.md` → read (root discovery; the catalog the Documents page
reuses).

## Diary

- **2026-10-16** — Opened in a field project; moved into the skill (R7, R8); spec only (R9).
- **2026-10-17** — Vision v9 approved (R12); r28 (R10, R13); shared family file (R14, R15);
  per-lens names, empty-state pages, catalog tree (R17); renumbered F-072 (R18); purpose
  set to what the agent sees (R20); the chronology depends on the dated-entry doctrine
  unit (R22); chronology reduced to dated events, audit documents given pages, no units
  page on marketing projects (R23). Review history: `REVIEW_LOG.md`,
  `audit/reviews/REVIEW_kb_site_design.md`.
- **2026-10-17** — Implemented from this spec, TDD from `test_docs_site.py` (65 tests, three
  code-built projects): generator, page, strings table, shared-file list and copies, four
  packages, READMEs, CHANGELOGs, `SKILL.md` lines, workflows document, Component Map,
  existing features, r29. F-073 is still open (handoff only), so the chronology reader is
  not built: the page lists no event and says so (criterion 3 open). Probe green on this
  repository; the site's counts match it (6 open, 59 analyses, 298 catalog documents).
  The field-KB run stays on the owner's work machine. E2E script: `E2E_TEST_kb_site.md`.
- **2026-10-17** — Owner walked the map in a browser pane: map navigation reworked (a
  topic click opens it up close, Map always returns to the topics view, zoom buttons, a
  collapsible legend, a top bar under 1000 px, system cursors), and every node labelled
  wherever its whole label fits without colliding — fact text wrapped, never cut.
  Closure review round 1 FAIL (2 BLOCK, 9 WARN): the statement mark was missing from
  search hits and map labels and its test could not fail (now one title function, a
  test enumerating every place fact text is shown, red under the old tooltip); an
  unreadable file met by a shared reader crashed the run (now one guard over
  `sdlc_core.read_text` for the run, tests patch the shared reader); home links now come
  from `orient_docs`; the walk is checked against the file the time cycle reaches; the
  `SKILL.md` line is 130 bytes and names no chronology.
- **2026-10-17** — Owner rulings R24 (an analysis shows the chain the agent works through,
  with its merge brief and E2E script) and R25 (the Vision's North Star in view): spec,
  criterion 15 and their tests added first, then the generator (`analysis_chain`,
  `chain_step` on the validator's own section names, `link_companions`, `vision_lead`) and
  the page (`chainStrip`, the North Star banner).
- **2026-10-17** — Closure review round 3 FAIL (1 BLOCK, 3 WARN): an analysis with no Vision
  section showed its Vision step as filled because the North Star link sat in its list; now
  only the step's own sections (and, for "merge and tests", its merge brief and E2E script)
  decide "Not in this analysis", the North Star and request record sit beside it, and a test
  runs the page's own `chainStrip` in Node (red under the old code). The Home paragraph and
  the derived documents now name the chain and the North Star. Round cap reached. The
  agent's answer to R26 (the owner found the guides missing): a page of their own
  (`build_guides`, `pageGuides`); Rules keeps the Vision, principles and decisions. Round 4,
  run beyond the cap on the owner's instruction (R27): PASS.

**2026-10-17 — chronology reader built on F-073; criterion 3 met.** F-073 merged into main
and released in 1.41.0; this branch took main (879ff3b), and F-072's CHANGELOG entries moved
to the next unreleased versions. `chronology(docs, pages)` now reads, with the validator's own
readers: Diary entries and spike outcomes (`section_lines` + `entry_openers`, so an entry
under the template comment is an event to both), dated project notes, request-record
entries (`request_entries`), review-log rows (`parse_review_log`), decision records
(`adr_date`), notes and sources received (`knowledge.frontmatter_date`). Tests first
(`Criterion03Chronology`: red on the empty reader, then green); one string added,
`event_spike` ("exploration outcome"). On this repository: 525 events (230 Diary, 208
review rows, 62 request entries, 20 decisions, 5 project notes, no spike outcome yet in
dated form), every one linking to its page; the probe's earlier 343 counted before the
grammar existed. Labels are shown as written, markup included.

**2026-10-18 — closure review of the chronology reader: FAIL, fixed.** Fresh-context reviewer,
read-only; numbers reproduced (525 events on main), T5 held end to end. 1 BLOCK, 5 WARN: marketing
spike outcomes live in `spikes/RESEARCH_*.md` and were not read (now read, with a test); a
received source's event now opens its source page; shadow mirrors are skipped as
`list_analyses` skips them (UC5); the reader test now patches `entry_openers` and sees the page
change, and T5, marketing and shadow cases are tested; the tie rule is stated (between
documents on one day the order is fixed, not a time order). Declared residual, owned by F-073:
an opener with an impossible date (`2026-13-45`) is shown as written, since `entry_openers`
does not validate the date.

**2026-10-18 — round 2 PASS; its one WARN fixed.** A received source's event linked to
`#/source/<name>` even on a project with no knowledge base, where that page does not exist;
the link is now made only when `C.meta.has_kb`, otherwise the label stays text.
