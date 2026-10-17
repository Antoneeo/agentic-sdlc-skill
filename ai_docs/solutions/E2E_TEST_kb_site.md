---
feature: F-072
analysis: ANALYSIS_kb_site.md
---
# E2E test: docs site

## What changed, in user terms

Every package of the family now has one more command, `docs_site.py`. It writes a
small website from a project's documents. You open it from disk with no network. It
shows what the agent reads to orient itself: what the project is, what is open with
its next step, the project's features or courses, its rules and documents, and, when
the project has a knowledge base, a map of topics and every fact with the exact
passage it comes from. The site changes nothing in the project.

## Environment and preconditions

- The packages installed from the release under test, or this branch checked out.
  `<skill_dir>` is the installed skill folder, e.g. `~/.claude/skills/agentic-sdlc`.
- Python 3.9 or later. A desktop browser: Chrome or Edge, and Firefox for S12.
- Three projects:
  1. this repository (code project, `ai_docs/`);
  2. a knowledge-lens project with `topics/` and `corpus/`. The owner's field KB is
     on the owner's work machine and never leaves it, so run that pass there;
  3. a marketing project with `mkt_docs/`, e.g. a copy of
     `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/fixtures/`.
- For every scenario, open the generated `index.html` by double-click (`file://`),
  **with the network disconnected** (Wi-Fi off or cable out).

## New-behavior scenarios

### S1 — Generate (acceptance 7, command)
Steps: 1. In each of the three projects run
`python <skill_dir>/scripts/docs_site.py --root <project>`. 2. Run `git status` in each.
Expected: one `[ok] docs site written: …` line, exit 0. `git status` shows no change
under the docs root. When the output folder `.docs-site/` is not git-ignored, a
`[note]` line says so.
Result:

### S2 — Refusals (Interface Contract)
Steps: 1. `--out <project>/ai_docs/site`. 2. `--out` pointing at a folder that holds
one file of yours. 3. In a folder holding both `ai_docs/` and `mkt_docs/`, run without
`--docs-dir`. 4. In an empty folder, run with `--root` pointing at it.
Expected: each prints one `[ERROR]` line and exits 2. Nothing is written: your file
is still there and alone.
Result:

### S3 — Home answers four questions (acceptance 1, 2)
Steps: open each project's site.
Expected: four blocks: **This project** (the README's title and opening paragraph, the
Vision's status and first section as written), **Lately**, **Open now** (each open
piece of work with its status and next step) and **What is known** (areas and their
topics, or one line saying none yet). From the home page one click reaches the
reading guide, the list of main documents, the guide router, the project notes and
the open-work register.
Result:

### S4 — Open work (acceptance 10–13)
Steps: 1. Open **Open work**. 2. Edit one `audit/HANDOFF_*.md` `next:` value, re-run
the command, reload.
Expected: blocked work first, then planned, in progress, paused, completed; within a
status, the most recently updated first. Each card shows the next step in full. No
number, score, assignee, owner, due date or team anywhere. After step 2 the card
shows the new text.
Result:

### S5 — Features / Courses (acceptance 11)
Steps: open the units page in the code project, and in a course project if available.
Then switch between **Columns by status** and **Single list**.
Expected: code and knowledge projects call it **Features**, course projects
**Courses**. Entries are sorted by id. The marketing project has no such page.
Result:

### S6 — Rules and documents (UC4)
Steps: open **Rules**, then **Documents**, then any document.
Expected: Rules lists the Vision with its declared status, the guides with their
"Read when" line, and the decision records. Documents lists the folders in plain
names. A document page shows its header fields as labels and the body formatted.
Relative links open inside the site, and a fact id in backticks is a link.
Result:

### S7 — Map (UC5, knowledge project)
Steps: open **Map**; switch **Topics**, **One topic up close** (click a topic first),
**Everything**; drag, scroll, click a node; untick an origin in the legend.
Expected: the map appears laid out and framed, with no animation settling. Clicking
opens the topic, fact or source. The legend hides only origins and node kinds. On
the owner's field KB, **Everything** (≈6,240 nodes) stays responsive.
Result:

### S8 — A fact and its passage (acceptance 5, 6)
Steps: open a fact from a document, an inferred fact, a fact stated by a person, a
replaced fact and a fact in conflict.
Expected: the exact passage is highlighted with its page or lines. An inferred fact
lists what it rests on, or says which part could not be traced. A fact resting on a
person's statement shows the **statement** mark wherever it appears: in lists, in
search results, in map labels and tooltips (a dashed ring on the map), and in the
panel with the notice "Not found in a document. Treat it as a statement, not as documented
evidence." A replaced fact shows the current fact at the end of each chain, or a
stated stop. Holds when / value / also concerns appear exactly as written.
Result:

### S9 — Search (acceptance 9)
Steps: press `Ctrl+K`; search a word in a document; a word written in a document
with a non-breaking hyphen; a word that is nowhere.
Expected: results grouped as facts, topics, documents; Enter opens the selected one.
The hyphenated word is found when typed with a normal hyphen. With no result, the
knowledge project shows the sentence that begins "Nothing found among facts, topics
and documents. The full text of source documents is not searched here"; the other
projects show "Nothing found in the documents."
Result:

### S10 — Words (acceptance 8)
Steps: read every label, button and empty-page line on all pages.
Expected: plain English only. None of: claim, ledger, provenance, elicited, given,
derived, ruling, imported, superseded, contested, corpus, sidecar, locator, slug,
frontmatter, workstream, handoff, L1, L2, L3. Content (titles, facts, next steps) is
as written in the documents.
Result:

### S11 — Freshness and addresses
Steps: 1. Read the bottom-left line. 2. Bookmark a topic page, regenerate after
deleting that topic, open the bookmark. 3. Use Back and Forward.
Expected: "Generated <date time> from commit <hash>, plus N changed files not yet
committed" (or "not a git repository"). The removed item shows "Not found — it may
have changed since this site was generated" with a link home. Back and Forward walk
the pages.
Result:

### S12 — Offline in another browser (acceptance 7)
Steps: open the knowledge project's site from disk in Firefox, network off; open
the browser's developer tools on the Network tab and walk every page.
Expected: every page works; the Network tab lists only local files.
Result:

### S14 — A feature read as its chain (acceptance 15)
Steps: open **Features**, then an analysis that has a merge brief and an E2E script (in this
repository, F-066 "Merge review brief and E2E test script"); click each step's links.
Expected: above the document, eight numbered steps — Vision, Use cases, Flows and interfaces,
Risks, Solution study, Design and tests, Merge and tests, Diary — each with a one-line
meaning. Each link scrolls to that section as written; "Merge and tests" opens the merge brief
and the E2E script; the Vision step opens the project's North Star and the request record
when there is one. A step with no section says "Not in this analysis"; no number, score or
completeness mark appears.
Result:

### S15 — The North Star in view
Steps: open the home page of a project whose Vision has a "North Star" section, then one
whose Vision has none.
Expected: the first shows the North Star in full, highlighted above the four blocks, with the
Vision's status and a link to it. The second shows no North Star banner; the Vision's first
section appears inside **This project**.
Result:

### S16 — Guides
Steps: open **Guides** from the navigation; then **Rules**.
Expected: Guides shows first the link "Which guide to read before which task" (the guide
router), then "How work is done" — each operative guide with its "Read when" line and its
status as declared — then "How it works", the code-comprehension guides. A project with no
guide says in one line when they appear. Rules shows the Vision, principles and decisions,
and links to Guides; it no longer lists guides.
Result:

### S13 — Chronology (acceptance 3) — after F-073
Steps: once the dated-entry rules of F-073 are merged and the reader is in, open
**Chronology** and the home's **Lately** block.
Expected now (before F-073): the page says in one line that dated events appear as
the documents record them, and lists none. Expected after: dated events, most recent
first, each linking to its document; no analysis start or end, no state filter, no
commit history.
Result:

## Regression scenarios

### R1 — Validator unchanged
Steps: in each project run `python <skill_dir>/scripts/sdlc_check.py check --root <project>`
(marketing: `mkt_check.py`), before and after installing this release.
Expected: same findings, same exit code.
Result:

### R2 — Install and uninstall
Steps: `npm i -g` the four packages; look in each client's skills folder; uninstall.
Expected: each installed skill folder now also holds `scripts/docs_site.py` and
`docs_site/`; no `test_*.py`; uninstall removes them with the rest.
Result:

### R3 — Session start
Steps: start an agent session in each project.
Expected: the orientation printed at session start is unchanged.
Result:

## Already covered by automated tests

`scripts/test_docs_site.py` (in every package's battery): one test per acceptance
criterion except 3, on a code-built knowledge, code and marketing project. It covers
the refusals, injection and path traversal, counts against the validator's own
parse, passages, chains, inferred grounds, search folding (with Node when present),
identical output across two runs (every file byte for byte, `core.js` apart from its generation time), unreadable files named whichever reader meets them, and the four packages' file lists.
`test_drift.py` checks the four copies are one file. Do not retest these by hand.
Rendering in a real browser, Firefox, the field KB's size and the network-off check
are not automated.
