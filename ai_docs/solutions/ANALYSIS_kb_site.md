---
description: F-072 - docs site. A stdlib-only generator shared by the whole skill family turns a project's ai_docs into a static, offline, read-only website - open work and the lens's units of work (read-only state view, Vision v9), working documents, search, and where the project has a knowledge base its topic map, facts with provenance and exact passages, and source documents - in plain English.
status: PLANNED
feature: F-072
id: F-072
start_date: 2026-10-16
end_date:
level: L3
domain: code
branch: feat/kb-site-spec
---
# ANALYSIS: docs site — a static website generated from a project's ai_docs (F-072)

## Objective

Every project governed by a skill of this family accumulates documents in its docs root —
analyses, resume notes, guides, visions — and a knowledge-lens project adds thousands of
claims, dozens of topics, hundreds of source extractions and notes. Today all of it is
read by opening Markdown files, and a knowledge base's graph — topic parents and related
topics, claim rows and their sources, replacement and conflict states, `derived_from:`
chains, sidecar `supersedes:` — is invisible to the person it serves, who does not know
the skills' vocabulary.

This unit adds to **every distribution of the family** one shared generator that turns a
project's docs root into a **static website**, opened from disk, offline, read-only, in
plain English ([REQUEST_kb_site.md#R1](../audit/requests/REQUEST_kb_site.md), R7, R8,
R14). Every project gets open work and its units of work as their documents declare them,
the working documents and a search; a project with a knowledge base also gets the topic
map, every fact with its origin and the exact passage behind it, and the source
documents. It is the full specification for an implementer working from it alone on
another machine (R9). Every figure about real data comes from `harness_kb_site/probe.py`,
run on a production knowledge-lens project and on this repository; the probe prints
counts only and exits 1 when an assertion fails (`--red` demonstrates a failure).

**Prior work.** `solutions/SPIKE_kb_viewer.md` (DRAFT, on `main` since 2026-10-17) showed
on a 7-topic corpus that a static page generated from the shared parsers works in any
browser and every client, with no dependency. This unit is the production design it
called for, with three differences, each settled here: passages for every locator form
(the spike excerpted `#L` only); a precomputed layout for thousands of nodes (the spike's
level layout held tens); per-item counts, which the spike excluded under the v8 reading
of Non-Goal 1 and the owner has since admitted (r28, after v9). Like the spike, the page
is written inside the project folder, because the desktop app's browser pane shows files
outside it as static snapshots.

**Vision v9.** The open-work and units-of-work pages rest on the Vision v9 amendment (the
read-only state view), decided by the owner (R11), ruled apart from this unit in
`solutions/PROPOSAL_vision_v9_state_view.md`, approved and applied 2026-10-17 (R12).

## Feature Vision

**Alignment.** `vision/project_vision.md` (APPROVED, v9). The site advances the Goal
"keep understanding durable across sessions — … nothing load-bearing lives only in a
transcript". It serves every Actor that reads its own project — the **solo developer**,
the **team lead** ("one source of truth"), the **practitioner in a non-code domain**. It
is a family capability authored once in the shared spine (R14), as the North Star
requires of what the family shares. It needs nothing external — stdlib Python, no
network. It is optional: nothing becomes mandatory at any level (Non-Goal 3). Its
standing cost is a line of about 160 bytes in each lens's `SKILL.md`, read every session
(Goal 4), accepted for all four (R13, R15). `VISION_kb_second_brain.md` (APPROVED)
excludes external infrastructure; static files are none.

**Admission and precedent placement** (`vision/rulings.md`):

| Surface | Placement | Verdict |
|---|---|---|
| The site as a family capability, every lens | r4 (a widened capability is re-ruled as new): ruled by the owner (R14); new row **r29** | ADMIT |
| Open work, units of work | r27 (read-only state view, v9); r2 and r9 cover computed state only | ADMIT under the six v9 conditions — criteria 11–16 |
| Fact count per topic; facts taken from and topics using each source; shared-source edge thickness | **r28**, owner ruled (R10, R13) | ADMIT: beside each item, never used to select, order, filter or flag |
| Whole-project totals on the Overview | an inventory of the docs root, about no unit's state | not r2; no total of open work or units |
| How far a source document was read | on that document's own detail only (R10) | a document describing its own state |
| Map legend | origins and node kinds only (R10) | not a selection by state |
| Replaced / in-conflict marks on facts | the claim row's own declared state | facts are content, not work |
| "Could not be read" box | the generator's own error report for the run | reports the tool's run, as `validate` does |
| Recent-changes feed | not in this unit | git history is not a document's declared state |

r29, written with this unit's closure: "generates, in every lens, a static read-only site
of the project's own documents and knowledge base, under r27 and r28" — ADMIT; basis
R14.

**Actors' view.** They know their domain and must not need the skills' vocabulary (R4).

**Non-goals.** No editing from the site; no server, hosting or sharing (R2); no
translation (R6); no full-text search inside source extractions; no change to the
existing spine modules.

**Success signals.** From any fact id cited in a document the reader reaches the fact,
its origin in plain words and the highlighted passage in one click; the reader of any
project sees open work, units of work and documents without opening a file; the
production knowledge-lens project generates in under 60 seconds (the probe reads and
checks its 5,759 passages in 4–21 s across runs).

## Use Cases / User Needs

All serve the Actors above and the Goal of durable understanding.

- **UC0 — See open work and units of work** (v9; every project).
- **UC1 — See what the project's docs hold** (every project; with a knowledge base, its
  areas, topics and how much each holds).
- **UC2 — Explore the knowledge graph**; **UC3 — Check a fact**; **UC5 — Look at a
  source document** (knowledge base present).
- **UC4 — Read the working documents**; **UC6 — Search** (every project).

Names: *fact*, *topic*, *area*, *source document*, *note*, *working document*, *open
work*, and the lens's own name for its units — *features* (code, knowledge: the owner's
word, R1), *engagements* (marketing), *courses* (course) (R17) — EXISTS under the skills'
terms (claim, topic, root topic, corpus artifact, note, docs-root document, workstream,
ANALYSIS, each lens's unit noun). *Site* is NEW.

## Functional Spec

### Pages

| Page | Present |
|---|---|
| Open work | always; first page when any open work exists (R2) |
| Units of work (named per lens) | always |
| Overview | always; first page when no open work exists |
| Working documents, Search | always |
| Map, topic pages, fact panel | when the docs root has at least one topic |
| Source documents | when the docs root has at least one source-document sidecar |

An always-present page with nothing to show says in one line what will appear and when
(R17): "Open work appears here when a piece of work has resume notes." / "Features appear
here when an analysis is written." A conditional page that does not apply is absent from
the navigation.

**The units-of-work page is named by the project's default domain**: code and knowledge
→ "Features", marketing → "Engagements", course → "Courses" (R17).

### Words the site uses (R4, R7)

Every interface label is plain English understood without the skills; every label that
classifies something carries its explanation in the legend and on hover. All interface
wording — labels, explanations, messages, and the reasons the generator reports — comes
from one strings table; the generator emits a fixed reason code with parameters.

| In the skills | Label | Explanation shown |
|---|---|---|
| claim | fact | — |
| `GIVEN` | from a document | Written in a source document; the passage can be opened and re-read. |
| `ELICITED` | stated by a person | Said by a person and recorded on the day. It has not been found in a document and may never be: treat it as that person's statement. |
| `DERIVED` | inferred | Reasoned from other facts; always shown with what it rests on. |
| `RULING` | decision | A decision taken to settle a conflict between facts. |
| `IMPORTED` | from another knowledge base | Brought in from another project's knowledge base and not re-checked here. |
| claim `SUPERSEDED` | replaced | No longer valid: a newer fact takes its place. |
| `CONTESTED` | in conflict | Facts that say different things, not yet settled by a decision. |
| sidecar `supersedes:` | newer version of | This source document replaces an older one. |
| topic / root topic | topic / area | — |
| `synonyms:` · `gaps:` · `related:` · `owns:` | also known as · known gaps · related topics · covers | known gaps: what the knowledge base declares it does not know yet |
| claim `about` (`verb -> topic`) · `valid` · `qty` | also concerns · holds when · value | — |
| corpus artifact · note | source document · note | Source documents are received and never edited; a note records what was said, decided or synthesised on a day. |
| reading frontier | read in full · read up to page N of M · read up to line N of M · read up to page N · read up to line N · reading not recorded · reading not readable ("<value>") | Facts are taken only from the part that was read. (The two forms without "of M" appear when the document's length is not stored.) |
| locator · claim id | page N (or lines a–b), passage highlighted · fact id | — |
| workstream · `HANDOFF_*.md` | open work · resume notes | — |
| level `L1`/`L2`/`L3`/`Spike`, other | trivial change / small change / significant change / time-boxed exploration; other values as written | — |

**Status words** (case-insensitive):

| Raw value | Label | Group order |
|---|---|---|
| `BLOCKED` | blocked | 1 |
| `PLANNED`, `TODO` | planned | 2 |
| `IN_PROGRESS`, `PROGRESS` | in progress | 3 |
| `PAUSED`, `ON_HOLD` | paused | 4 |
| `COMPLETED`, `DONE` | completed | 5 |
| `CANCELLED` | cancelled | 6 |
| `ARCHIVED` | archived | 7 |
| anything else | the value as written | 8, "other status" |

A value that marks a unit as available or next to take (`READY`, `NEXT`, `UP NEXT` and the
like) is not a group: under v9 it is priority by another name, so it falls into "other
status", shown as written, with no position of its own. (Field: 26 of 26 open workstreams
and 45 of 45 analyses fall in groups 1–7; this repository: 5 of 6 workstreams — one
declares a compound status, shown under "other status".)

Content — titles, descriptions, fact text, document bodies, frontmatter values, next
steps — is shown exactly as written, in its own language, never translated, re-cased or
truncated (R6). Frontmatter keys are humanised (`start_date` → "start date").

### Topic names, order, areas (R6)

A topic is shown by the first `# ` heading of its node, as written, else its slug, as
written (45 of 74 field nodes have a heading). Topics are always listed **by slug as
text**, the order of the generated topic index. A merged topic (`status: SUPERSEDED`) is
neither counted nor drawn; its address forwards to its `redirect_to:` target with "This
topic was merged into <name>".

A topic's **area** is reached by following first parents upward to a node with no
parents. The walk stops at a node already visited (a cycle), a parent that does not
exist, or a merged parent; such a topic has **no area**: it is listed under "Topics
without an area" and drawn in a neutral colour. (Field: 8 of 74 topics have a first
parent that is not an area.)

### Open work (v9)

- One card per open workstream: name, status label, level label, since, last updated,
  branch, and its next step **in full, verbatim** — never cut, parsed or highlighted; a
  long step wraps. "Read the resume notes" opens the file.
- Order: status group, then the workstream's own `updated:` date, most recent first; a
  missing date last; ties by name. (Field: 26 of 26 declare `updated:`.)
- Nothing is computed, counted, scored or recommended.

### Units of work (v9)

One entry per analysis (shadow mirrors excluded): name (`feature:`, else the file name
without `ANALYSIS_` and `.md`), id as written, status label, level label, lens, start and
end dates; it opens the analysis. Two layouts: columns by status group, with no count on
any column, and a single list. **Entries are always sorted by id as text** — inside each
column and in the list, whether or not an analysis declares `updated:` — the lookup order
of the generated feature history, which v9 admits as an alternative to the date order.
Lens: `domain:`, else the project's default domain; filter by lens only, never by status.
A missing field shows "—".

### Overview

Project name (first heading of the docs root's `README.md`, else the folder name); one
line per figure, each saying what it counts — working documents and, with a knowledge
base, topics and areas, facts with a bar by origin, source documents, notes; no total of
open work or units. With a knowledge base: the areas in topic order, each with its direct
child topics and their fact counts (r28), a topic with several parents listed under each,
then "Topics without an area", and "Open the map". Always: search.

### Map

Three views; each states in two lines how to read it; legend items for **origin** and
**node kind** can be switched off; replaced and in-conflict marks cannot.

1. **Topics** (opens first): topics sized by fact count (r28), coloured by area; edges
   *part of*, *related* (declared, drawn undirected), and *share source documents
   (computed)*, dashed, thickness by the number of shared sources (r28).
2. **One topic up close**: its facts, their source documents and notes, *based on* edges
   from notes and sidecars that declare `derived_from:`, *newer version of* edges between
   source documents, other topics sharing those sources, replaced and in-conflict links.
3. **Everything**: all topics, facts, source documents and notes (6,240 nodes in the
   field); labels on topics only at low zoom; fact-to-source edges fade until zoomed in.

Edge legend: belongs to · taken from · based on · newer version of · replaced by (arrow
to the newer fact) · in conflict with (red) · also concerns (with the verb) · part of ·
related. Hover lights a node and its neighbours and fills the side panel; click pins it.
The map appears already laid out and framed, and re-frames on window resize until the
reader pans or zooms. Area colours: one hue per area, evenly spaced in topic order at
fixed saturation and lightness, for any number of areas; "no area" is neutral.

### Topic page

Name, area path, description, also known as, known gaps, covers, related topics in both
directions (one named in another's `related:` shows as "related (named by <topic>)"),
sub-topics, and its facts in row order: text, origin, marks, source (document and page or
lines, or note). Filters: words and origin only. Replaced facts are dimmed and link to
the current fact.

### Fact panel

Address `#/fact/<id>`; a row without an id: `#/fact/<topic>:<row number>`.

- Text, origin with its explanation, marks.
- **Statement notice** — on a stated fact, and on an inferred fact any of whose grounds is
  a statement: "Not found in a document. Treat it as a statement, not as documented
  evidence." Wherever such a fact is listed (topic table, search results, map hover, id
  hovers in documents) it carries a short "statement" mark.
- **Inferred**: "Rests on:" every ground reached — documents, a statement by a person, a
  decision, another knowledge base — and, when any branch cannot be followed, a separate
  line "Part of it could not be traced: <reason>". The walk: a cited source document is
  ground *documents*; a cited note is *statement* if its `origin:` is `elicited`,
  *decision* if `ruling`, *another knowledge base* if `imported`; otherwise its
  `derived_from:` entries are resolved and walked; a note with neither but with `basis:`
  is *decision*; anything else is untraceable. An entry resolves as the validator's
  cascade resolves it — a normalised path, else a bare name under `corpus/notes/` then
  `corpus/given/` — and is followed **only if it ends inside the docs root**, absolute or
  not; one that leaves the docs root is untraceable, never opened. (Field: 7 absolute
  entries, 4 inside the docs root; inferred facts by exclusive class — statement 25,
  untraceable 8, documents or decisions 157.)
- **Replaced**: "No longer valid. Replaced by:" the end of each replacement chain — every
  branch of a fork followed; a loop or a missing id stops and says so (field: 218 of 369
  links point at a fact itself replaced; longest chain 8; 11 facts name several).
- **In conflict**: the text of every other fact in the set.
- Holds when, value, also concerns.
- **Where it comes from**, for each cited source (106 field facts cite several): document
  name, page or lines, the exact passage highlighted with up to 300 characters before and
  after (pages) or 3 lines before and after (lines); a note cited with a locator shows
  that passage of the note, without one it links to the note. A cited source with a newer
  version: "A newer version of this document exists: <name>". An unresolvable citation:
  "This passage could not be found: <reason>". A spreadsheet cell: the cell reference and
  "open the file to see it".
- Other facts taken from the same document — the first 10 in topic order, then row order
  — with "and N more" linking to the source's detail. Open topic · show on map · fact id.

### Working documents

The tree holds **the documents the shared project-memory catalog lists** (R17) — the docs
root's `README.md` and the Markdown under the catalog's folders, leaving out hidden and
harness folders, the raw corpus and the generated indexes — **plus the resume notes**,
which Open work opens (field: 443 documents; this repository: 303). Folders carry plain
names (vision → "Vision and rules", strategic → "Architecture and catalog", architecture
→ "Decisions", reference → "Guides", solutions → "Analyses and specifications", topics →
"Topics", corpus/notes → "Notes", resume notes → "Resume notes"), others their path;
entries show the title (first heading, else file name), sorted by path; no status or date
in the tree. A document page shows its frontmatter as labels and, below, the frontmatter
block as written (multi-line values do not become labels: 46 field documents have them),
then the body formatted. With a knowledge base, a 12-hex token in backticks that is a fact
id becomes a link (text on hover, statement mark when it applies), and one that is not is
marked "Not a fact id in this knowledge base — a replaced or removed fact, or another
identifier such as a file digest" (50 of 6,014 in the field); without one, such tokens
are left as written. Relative links between listed documents open inside the site.

### Source documents

A table, one row per sidecar (304 in the field; stored extractions are not rows): name,
kind (the sidecar `description:` as written, else the extension), date, facts taken,
topics using it (r28); sortable by name and date only. A row opens its detail: the
sidecar fields, how far it was read, "Newer version of: <name>" / "Replaced by a newer
version: <name>", and its facts.

### Search

Button and `Ctrl+K`. Working-document titles and bodies and, with a knowledge base, fact
text and ids and topic names, slugs, synonyms and descriptions. Case-, accent- and
dash-insensitive (U+2010–U+2014, U+2212 as `-`; U+200B, U+00AD, U+FEFF ignored). Results
grouped topics / facts (origin, marks) / documents; arrows and Enter. No result, with a
knowledge base: "Nothing found among facts, topics and working documents. The full text
of source documents is not searched here — not finding something does not mean the
sources are silent on it."; without one: "Nothing found in the working documents."

### Freshness, language, look

Every page: "Generated <date time> from commit <hash>, plus N changed files not yet
committed (included)", or "not a git repository". All interface text English (R7). Dark
theme (R2): background `#0f1419`, surfaces `#161d26`/`#1d2632`, borders `#2a3441`, text
`#e6edf3`, muted `#8b98a5`; origins cyan `#22d3ee`, amber `#f59e0b`, violet `#a78bfa`,
green `#34d399`, slate `#94a3b8`; in conflict `#f43f5e`; replaced at 45% opacity. Usable
from 1024 px; below 700 px the map panel hides.

### Cases

Malformed topic or unreadable file: generation continues; the Overview lists the file and
the reason in plain words, with the validator's own message under "technical details",
verbatim. Missing source file: the fact appears; its passage gives the reason. Passage
over 2,000 characters: shown in full, scrollable. A cycle in `parents:`: the walk stops;
generation never loops.

### Acceptance criteria

1. Overview figures equal the probe's for the same docs root — on a knowledge-lens
   project and on a project without a knowledge base.
2. Every view listing a fact shows its origin and marks; a fact with a statement ground
   carries the statement mark in every view.
3. Each passage equals the span its locator addresses, read as the validator reads it.
4. A replaced fact shows the end of every branch of its chain.
5. Each inferred fact's grounds follow the walk above; per exclusive class (statement,
   then untraceable, then another knowledge base, else documents or decisions) the counts
   equal the probe's, which applies the same rule.
6. The docs root is unchanged after generation.
7. The site makes no network request and works opened from disk.
8. Searching `tamper-proof` finds a fact written with U+2011.
9. Every interface string, including every generator reason, comes from the strings
   table, and none contains, as a whole word, case-insensitively: claim, ledger,
   provenance, elicited, given, derived, ruling, imported, superseded, contested, corpus,
   sidecar, locator, slug, frontmatter, extracted_through, derived_from, workstream,
   handoff, L1, L2, L3. Verbatim validator messages appear only under "technical details".
10. Outside Open work and units of work, nothing lists, orders or filters documents or
    work by a state value; per-item counts appear only as r28 allows.
11. Open work and units of work are rebuilt in full from the documents on every run — no
    data from a previous run is read — and the freshness line dates them.
12. They show only declared values: no count, total, percentage, score or readiness.
13. They order exactly as stated (open work: status group, then declared update date;
    units: status group, then id).
14. No page offers an action on a unit other than opening its document; navigation,
    search, filters, sorting and view switches change nothing in any document and
    nothing outside the page.
15. No assignee, owner, due, target or review-by date, iteration, team or role field is
    shown; next steps appear verbatim and complete.
16. The lines this unit adds to any `SKILL.md`, README or CHANGELOG name the command and
    what the site shows, and none tells an agent to choose, prefer, avoid, skip or order
    units of work from it.
17. A source document's detail shows its reading state, its newer or older version, and
    its facts.
18. On a project without topics or source documents, the pages that need them are absent;
    on a project without open work or units, those pages show their empty-state line.

**Why the output satisfies v9's first condition.** The condition admits a collection
"derived mechanically from the documents' own fields, each time it is produced". The
generator rebuilds every data file from the documents on each run and reads nothing it
wrote before (criterion 11); the output is never edited by hand, lives outside the docs
root where no document cites it, and carries the commit it was derived from.

## Interface Contract

**Idioms.** Skill tools run as
`python <skill_dir>/scripts/<tool>.py … --root <project> [--docs-dir <name>]`, plain-text output, non-zero exit on failure; the docs root by
`sdlc_core.resolve_docs_dir`, which discovers `ai_docs` or the legacy `mkt_docs`. The
page's idioms — dark dashboard (owner, R2), side panel, `Ctrl+K` search — are new; the
panel and the shortcut are this design's choice.

**Command** (identical in every distribution):


```
python <skill_dir>/scripts/docs_site.py [--root <project>] [--docs-dir <name>] [--out <folder>] [--open]
```

- Docs root as every entry point resolves it; an ambiguous root exits 2 with the
  resolver's message (it names `--docs-dir`); a resolved root that does not exist exits 2
  with "No documentation root at <path>".
- `--out` default `<project>/.docs-site/`, inside the project folder. Exit 2 when it is
  inside the docs root ("Output folder must be outside the docs root: <path>"), and when
  it exists, is not empty and holds no `.docs-site-manifest` ("Output folder is not empty
  and was not written by docs_site: <path>").
- Success: one line,
  `docs site: <t> topics, <f> facts, <s> sources, <d> documents -> <out>/index.html (<n>s)`,
  exit 0; one more line per unreadable file and exit 1 when any; "Note: <out> is not
  git-ignored; it holds a full copy of the project's docs" when `git check-ignore` does not
  ignore it. `--open` opens the page in the default browser.

**Flows.** UC0: open `index.html` → data loads → Open work renders the cards (or its
empty line) → the units page renders columns from the same data → a card opens its
document. UC1/UC2: Overview or "Open the map" → the map draws from positions computed at
generation → hover/click fill the panel. UC3: a fact clicked anywhere → `#/fact/<id>` →
the panel renders precomputed passages, chain ends and grounds. UC4: Working documents →
document data loads on first use ("Loading documents…") → the document is formatted and
sanitized → fact ids become links. UC5: Source documents → table → a row opens its
detail. UC6: `Ctrl+K` → the precomputed index filters → Enter opens.

**Addresses.** `#/work`, `#/units`, `#/`, `#/map`, `#/map/<slug>`, `#/topic/<slug>`,
`#/fact/<id>`, `#/doc/<path>`, `#/sources`, `#/source/<name>`; back and forward work. An
address for an absent page or unknown item: "Not found" with a link home. Missing data:
"This site's data is incomplete — run the generator again."

**Constraints.** The generator and its page are shared spine files, byte-identical in the
four distributions, listed in `shared_files.py`, guarded by `test_drift.py`. They import
`sdlc_core` and `knowledge` and change neither. The generator is not named `site.py`,
which would shadow Python's standard `site` module when run from its own folder. The core
`index` is not called.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| resolve the docs root (`ai_docs`, `mkt_docs`) | EXISTS | `sdlc_core.resolve_docs_dir`, `DOCS_DIR_CANDIDATES` | re-read |
| read topics, claim rows, cited paths | EXISTS | `knowledge.kb_load_topics`, `kb_parse_claims`, `kb_claim_sources` | probe: 74 topics, 5,626 rows, 0 parse errors; 0 topics here |
| list the working documents | EXISTS | `knowledge.memory_records` (the catalog) + `sdlc_core.list_workstreams` | probe: 443 field, 303 here |
| read frontmatter, text | EXISTS | `sdlc_core.load_frontmatter`, `read_text` | probe executes the multi-line drop |
| list analyses; id order; default domain | EXISTS | `sdlc_core.list_analyses`; the sort in `sdlc_core.build_index`; `sdlc_core.project_default_domain` | probe: 45 field, 59 here |
| one row per source with reading state | EXISTS | `knowledge.kb_build_corpus_index`, `kb_coverage_cell` | re-read: seven outcomes as labelled above |
| commit, changed files | EXISTS | `sdlc_core.git_head`, `git_changed_since` | re-read |
| parse `derived_from` entries | EXISTS | `knowledge._kb_df_entries` | used by `kb_time_cycle` |
| distribute one file to four packages, detect drift | EXISTS | `shared_files.py` (`SHARED_FILES`, `--update`), `test_drift.py` | re-read |
| extract the passage a locator addresses | INADEQUATE | `kb_check_locator` validates only | probe: 5,759 of 5,759 agree; `--red` disagrees on 82 |
| resolve a `derived_from` entry | INADEQUATE | the ladder is a closure inside `kb_time_cycle` | probe copies it line for line; the implementation's test compares its walk with `kb_time_cycle`'s edges on the fixture |
| walk replacement chains; walk inferred grounds | MISSING | — | searched `SUPERSEDED`, `derived_from`, `ground`, `chain` in `knowledge.py`, `sdlc_core.py`: validation and cascade only |
| lay out a graph; format Markdown; render a page | MISSING | — | `git grep` for `markdown`, `html.escape`, `canvas`, `layout`, `force` outside `ai_docs/`: none; stdlib has no Markdown renderer |

New components, contracts in the skills' vocabulary:

- **Passage extractor** — `(docs, artifact, locator)` → `(text, before, after, where)` or a
  reason code; reads exactly as `kb_check_locator` (`read_text`, the `.txt` sibling, pages
  by `"\f"`, lines by `"\n"`), with a per-file cache.
- **Chain walker** — `replacement_ends(rows_by_id, id)` → ids and stop code;
  `derived_grounds(docs, row)` → set of {documents, statement, decision, imported} plus
  untraceable reason codes, by the walk in the Functional Spec.
- **Graph layout** — deterministic positions at generation: areas on a circle; topics by
  a force layout over topics only; facts on rings around their topic; source documents
  and notes at the centroid of what cites them; bounded relaxation over a grid so the
  cost stays near-linear. Same input, same output. (A 460-node prototype left to browser
  animation stayed tangled in a background window, where browsers throttle animation
  frames; starting each fact beside its topic made areas readable.)
- **Markdown formatter + sanitizer** — headings, paragraphs, lists, tables, emphasis,
  inline and fenced code, links, blockquotes, rules; anything else as text. Allow-list:
  those tags; `href` only, relative, `#` or `http(s)`.

## Impact

**No third-party JavaScript.** Sigma.js and Graphology ship UMD builds that would run
from disk and draw more nodes on WebGL. Rejected because the packages are Apache-2.0 with
a NOTICE and would carry third-party code and licences into every install, and the
family's contract is stdlib-only, no network; canvas 2D with a precomputed layout and
level-of-detail draws 6,240 nodes per redraw.

**New shared files**, authored in `skills/agentic-sdlc-skill/` and copied byte-identical
to the three other skill folders: `scripts/docs_site.py`; `docs_site/index.html`,
`docs_site/app.js` (classic script; all text from the strings table), `docs_site/style.css`,
`docs_site/strings.js` (the strings table); `scripts/test_docs_site.py`, which builds its
fixtures in a temporary folder from code: a knowledge-lens project (topics with and without
heading, a merged topic, a first parent that is not an area, a `parents:` cycle, a missing
parent, every origin, a 3-step replacement chain with a fork and a loop, a 3-fact conflict,
inferred facts reaching each ground, one mixed and one untraceable, an absolute
`derived_from` inside and one outside the docs root, page/line/sheet and a broken locator,
a superseding sidecar, a sidecar with `derived_from:`, a note with a locator, an empty
claim id, a multi-line frontmatter, a document citing a valid id, a missing id and a
digest, three resume notes — one `READY`, one without `updated:` — and three analyses — one
without `domain:`, one declaring `updated:`); a code project with no topics, corpus,
resume notes or analyses; a marketing project on `mkt_docs`; an ambiguous root; a missing
root; a `--docs-dir` run.

**Output** (outside the docs root, inside the project): the four `docs_site/` files;
`data/site.js` (topics, facts, sources, notes, edges, layout, work and units, freshness,
and the search index including the normalised text of working documents),
`data/passages.js`, `data/docs.js` (formatted documents, loaded on first use);
`.docs-site-manifest` (files written; every entry must resolve under `--out`). Data files
are classic scripts assigning one global each, written with
`json.dumps(…, ensure_ascii=False)`, then `</` → `<\/` and U+2028/U+2029 escaped (pages from disk cannot
fetch JSON; the escaping keeps content from closing the script).

**Existing files touched** (`reference/GUIDE_release.md` step 2; one release across the
four packages, R14):
- `skills/agentic-sdlc-skill/scripts/shared_files.py`: `SHARED_FILES` gains the six files
  above; then `shared_files.py --update` and the copies; `shared_manifest.json` follows.
- `package.json` `files` of the four packages: the five runtime files only —
  `test_docs_site.py` stays out of every package, as every shared test does (the guide's
  verification battery: no `test_*.py` in the tarball).
- READMEs: root (support-files bullet, line 37; Runtime Shape tree, line 88), kb (support
  files, line 58), marketing (validator, line 26), course (a usage line).
- `SKILL.md` of the four lenses: one line where validator commands are listed (~160
  bytes each, R15), naming the command and what it shows.
- CHANGELOGs of the four packages.
- `ai_docs/strategic/skill_family_agent_workflows.md`: every column of the validator
  commands row (line 53), and the shared-file count (line 444: 22 becomes 28, or the
  count `shared_files.py` reports after the merge with `main`).
- `ai_docs/strategic/architecture.md`: Component Map rows for the generator and the four
  components; `ai_docs/strategic/existing_features.md`: the feature;
  `ai_docs/vision/rulings.md`: r29.
- Closure: `audit/HANDOFF_kb_site.md` deleted; `sdlc_check.py index`;
  `E2E_TEST_kb_site.md`, `MERGE_REVIEW_kb_site.md`; `mark` on `skills/` and
  `distributions/` last.
- Not touched: `sdlc_core.py`, `knowledge.py`, `entry_point.py`.

**Trace.** Open work, units → UC0, v9/r27, R17; Overview → UC1, r28; map, layout → UC2,
r28; fact panel, extractor, chain walker → UC3; documents → UC4, R17; sources → UC5, r28;
search → UC6; strings table → R4/R7; naming → R6; legend, reading state → R10; shared
distribution → R14, r29; SKILL.md lines → R13, R15.

## Security and Threat Model

Surfaces: filesystem (reads the docs root, writes one folder); outside content shown in a
page (mail and documents inside extractions and notes); confidential data (the docs root
lands in the output folder).

| Threat | Requirement |
|---|---|
| Script injection from content | Text inserted as text; Markdown through the allow-list sanitizer; data files escaped. Tests: `<script>`, `onerror=`, `javascript:`, `</script>` inside a fact. |
| Content leaves the machine | No network request (no CDN, fonts, analytics); external links from content open only on click; output scanned in tests; the not-ignored note. |
| Writing into the docs | `--out` inside the docs root refused; read-only opens (criterion 6). |
| Overwriting the user's files | A non-empty `--out` without the manifest is refused; only manifest-listed files under `--out` are replaced. |
| Path traversal via sources, links or `derived_from` | A path is followed only if it ends inside the docs root; one leaving it is untraceable, never opened; `original_path` never followed. |
| Shadowing a standard module | The generator is not named `site.py`. |
| A statement read as evidence | Statement notice and mark everywhere (criterion 2); grounds behind absolute paths inside the docs root are followed, so their statements are not lost. |
| Absence read as evidence | The empty-search sentence. |
| A stale site read as current | Freshness line. |
| The state pages drift into work management | Criteria 10–16. |

## Action Plan

1. `test_docs_site.py` with its code-built fixtures, red.
2. Data model, page presence, naming, area walk, counts equal to the probe.
3. Passage extractor; chain walker; comparison with `kb_time_cycle`'s edges.
4. Formatter and sanitizer; data escaping.
5. Layout; search index.
6. Pages and strings table with reason codes.
7. Map: three views, legend, hover/pin, framing, level of detail.
8. Shared-file list, `--update`, copies; packages, READMEs, CHANGELOGs, `SKILL.md` lines;
   workflows table and count; Component Map; existing features; r29.
9. Runs on a real knowledge-lens project and on this repository; E2E script; closure
   review; merge brief; `mark`; one release.

## Test Strategy

`test_docs_site.py` (`unittest`, shared, runs in every distribution) on its fixtures,
generating into a temporary folder: counts equal to the probe's on every fixture (1);
statement mark in topic table, search index, map data, id hovers (2); passages equal to
the validator's reading, form-feed page, line range, broken locator (3); chain ends with
fork, loop, missing id (4); grounds equal to the expected sets, absolute paths inside and
outside the docs root, and the walk's resolutions equal to `kb_time_cycle`'s edges where
both follow (5); docs root unchanged (6); no `http(s)://` outside content links in the
output (7); search normalisation (8); `app.js` holds no user-facing literal, every reason
code has a string, `strings.js` passes the denylist (9); data for Overview, Map and
Sources carries no state-ordered or state-filtered collection (10); a second run over a
deliberately edited previous output rebuilds every data file (11); no count or score keys
in work and unit data (12); the stated orders, `READY` under "other status", missing
`updated:` last, an analysis declaring `updated:` still in id order (13); the page model
offers no unit action other than opening (14); next steps byte-equal to the source and no
assignee/owner/due/target/review/iteration/team keys (15); the lines this unit adds to
`SKILL.md`, READMEs and CHANGELOGs, read from a fixture copy of each, contain none of
choose / prefer / avoid / skip / order (16); source detail (17); page presence and
empty-state lines on the code fixture (18); the page name per lens; `mkt_docs`, ambiguous
and missing roots, `--docs-dir`; a `parents:` cycle terminates; sanitizer and
script-closing escape; `--out` refusals exit 2; unreadable topic exit 1; identical layout
across two runs. `test_drift.py` confirms the four copies; `npm pack --dry-run` lists no
`test_*.py`. The probe runs green on a real knowledge-lens project and on this repository,
and `--red` fails, before closure.

In a browser: every view on the fixtures and on a real project, console clean, opened
from disk with the network off; listed in the owner's E2E script.

**Guides.** Router: `GUIDE_release.md` → read (step 2 and the verification battery,
applied above); `GUIDE_shared_project_memory.md` → read (every lens discovers the root
with the core resolver and ambiguous roots fail rather than merge — the generator does the
same; the working-documents tree takes the catalog's own list). If the layout or chain
walker needs a model to maintain, a `source_kind: code` guide is written at closure.

## Diary

- **2026-10-16** — Opened in a field project; moved into the skill (R7, R8); spec only (R9).
  Work views via Vision v9 (R11).
- **2026-10-17** — v9 approved and applied (R12); r28 (R10, R13); shared family file (R14,
  R15); page names per lens, empty-state pages, catalog tree (R17). Renumbered F-072:
  F-069 to F-071 are taken on `main`, where `SPIKE_kb_viewer.md` explored the same ground
  (R18). Review verdicts and findings: `REVIEW_LOG.md` and
  `audit/reviews/REVIEW_kb_site_design.md`. Next: owner decision, then merge `main`,
  commit and push for implementation elsewhere.
