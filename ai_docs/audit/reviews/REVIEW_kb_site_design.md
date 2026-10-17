---
description: Per-finding disposition of the F-072 kb site design reviews (round 1, 22 findings; round 2, 26 findings) - each finding, what changed in ANALYSIS_kb_site.md, or why it was refused.
status: CURRENT
---
# F-072 kb site — design review dispositions

Reviews: fresh-context subagent, rung 1, deep tier, read-only, opened with the REVIEW
MANDATE block. Rows in `REVIEW_LOG.md`. Owner decisions cited by
`audit/requests/REQUEST_kb_site.md` entry.

## Round 1 — 2026-10-16, FAIL, 22 findings

| Finding | Disposition |
|---|---|
| B1 criterion 9 bans words that are also labels; no match rule | Fixed: whole-word, case-insensitive denylist of skill-only terms; "topic", "note" left out as plain words. |
| B2 impacted files missing; router verdict false | Fixed: `GUIDE_release.md` read and applied; package, README, workflows table, existing features, Component Map, `mark` listed. |
| B3 replaced source documents and `derived_from` edges missing | Fixed: "newer version of" label, edges, panel and source-detail notices; "based on" edges. |
| B4 no admission placement | Fixed: placement table; owner rulings R10 (counts kept → r28; reading state on detail only; legend by origin and kind only); work views via Vision v9 (R11, R12). |
| M (B5) false ES-module claim about Sigma/Graphology | Fixed: the weighing now says they ship UMD builds and rests on licence and stdlib-only. |
| M1 probe counted stored extractions as sources | Fixed: one source per sidecar; extractions counted apart. |
| M2 chain walker diverged from the validator's ladder | Fixed: probe uses `_kb_df_entries` and the ladder line for line; spec states it. |
| M3 harness asserted nothing | Fixed: assertions, exit 1, `--red` shown failing (82 passages). |
| M4 statement notice only in the panel | Fixed: mark in every view (criterion 2). |
| M5 tombstones, empty ids, docs-root errors, multi-line frontmatter | Fixed: each specified; probe excludes merged topics. |
| M6 UC5 flow and test gaps | Fixed: flow, criterion 17. |
| M7 ledger omissions; `entry_point.py` | Fixed: `kb_build_corpus_index`, `kb_coverage_cell`, `git_changed_since` named; `entry_point.py` not imported. |
| W1 Functional Spec named files and functions | Reduced: the remaining names identify data sources the reader needs; mechanisms moved to the Interface Contract and Impact. |
| W2 alignment quoted text not in the Vision | Fixed: rests on the Goal "keep understanding durable across sessions" and named Actors. |
| W3 R9 recorded no choice among options | Superseded: owner chose to amend the Vision (R11). |
| W4 details an implementer needs | Fixed: folder names, direct children, area colour, related both ways, line context, notes with locators. |
| W5 9.2 s naive locator reading | Fixed: per-file cache in the extractor contract; target under 60 s. |
| W6 data files not required to be JSON-encoded | Fixed: `json.dumps`, `</` and U+2028/2029 escaping. |
| W7 unmeasured figures | Fixed: figures now come from the probe; "≈12,000 edges" removed. |
| W8 528 lines | Accepted: no budget fixed; the Diary is short. |
| W9 SKILL.md cost not disclosed | Fixed: ~160 bytes disclosed; accepted by the owner (R13). |
| W10 error box not placed | Fixed: placement row. |

## Round 2 — 2026-10-17, FAIL, 26 findings

| Finding | Disposition |
|---|---|
| B1 next step cut to two sentences, against v9 "verbatim" | Fixed: shown in full, never cut, parsed or highlighted; criterion 15 and a byte-equality test. |
| B2 per-source counts and edge thickness unplaced | Owner ruled keep (R13); r28 written to the ledger covering topic counts, per-source counts and shared-source thickness. |
| M1 status map missing; queue statuses could form groups | Fixed: raw-to-label table with group order; `READY`/`NEXT` fall into "other status"; `Spike` labelled. |
| M2 no order inside Features columns | Fixed: sorted by id as text, the feature history's lookup order. |
| M3 criterion 1 vs merged topics | Fixed: probe excludes them (`topic_tombstones` reported); criterion 1 says so. |
| M4 grounds vs "all that apply" unstated | Fixed: the walk and the mixed case are specified; fixture `expected.json`; exclusive counting order stated for the probe comparison. |
| M5 "Imported" in a required string | Fixed: explanation reworded; all interface text must live in `strings.js`, tested. |
| M6 kb README has no Runtime Shape section | Fixed: the spec says so, adds to the support-files bullet only, and records the guide mismatch. |
| M7 no `--docs-dir`; "no docs root" message invented | Fixed: `--docs-dir` added; missing root has its own message and exit 2. |
| M8 area colour wrong for 8 topics; 12 colours for 13 areas | Fixed: area = root reached by first parents; hues evenly spaced for any number of areas. |
| W1 component names in the Functional Spec | Reduced as in round 1 W1. |
| W2 `list_analyses` omitted; MISSING without search terms | Fixed. |
| W3 side panel and `Ctrl+K` attributed to the owner | Fixed: only the dark dashboard is the owner's (R2). |
| W4 r28 deferred, wording the agent's | Fixed: r28 in the ledger now, basis quotes R10 and R13 and says the question's wording is the agent's. |
| W5 first run over a user's folder; manifest paths | Fixed: non-empty folder without manifest refused; manifest entries must resolve under `--out`. |
| W6 46 documents and 21 s not reproduced | Fixed: the probe counts multi-line frontmatter; timing stated as the measured range 5–21 s. |
| W7 no per-finding record for round 1 | Fixed: this document. |
| W8 criterion 16 tested on SKILL.md only | Fixed: SKILL.md, README, CHANGELOG. |
| W9 sidecar `derived_from` edges not drawn | Fixed: "based on" from notes and sidecars. |
| W10 Features flow; UC5 criterion | Fixed. |
| W11 "not yet found" wording for statements | Fixed: "has not been found in a document and may never be". |
| W12 which 10 other facts | Fixed: area order, then row order, with "and N more". |
| W13 path rules differ from the ladder silently | Fixed: the difference is named, and excluded from the agreement test. |
| W14 SKILL.md cost not accepted | Accepted by the owner (R13). |
| W15 criterion 11 "stored nowhere else" false | Fixed: the output is the derivation, dated by the freshness line. |
| W16 search over lazily loaded bodies | Fixed: normalised document text lives in the search index in `kb.js`. |

## Round 3 — 2026-10-17, PASS (provisional, round cap reached), 11 findings

The owner made the generator a shared family file the same day (REQUEST R14) and
accepted the SKILL.md line in all four lenses (R15); the rewrite answers both and the
findings below. Under the cap, it goes to the owner rather than to a fourth round.

| Finding | Disposition |
|---|---|
| M1 criterion 14 forbade the spec's own filters, search and switches | Fixed: no unit action other than opening; navigation, search, filters, sorting and view switches change nothing. |
| W1 criterion 10 vs Overview totals | Fixed: per-item counts only as r28 allows; whole-project totals placed as inventory; no open-work or feature totals. |
| W2 topic order inside an area undefined | Fixed: topics listed by slug as text everywhere (the generated index order). |
| W3 first-parent walk without edge cases | Fixed: stops on cycle, missing or merged parent; "Topics without an area"; tested. |
| W4 generated reasons outside the strings table | Fixed: reason codes rendered through the strings table; validator messages only under "technical details". |
| W5 file name in the Functional Spec | Fixed: the criterion speaks of "the strings table"; the file is named in Impact and Test Strategy. |
| W6 two wordings for reading state | Fixed: the five outcome classes of the coverage cell, the site's own wording, "of M" kept. |
| W7 Features name, lens, level fallbacks | Fixed: `feature:` else file stem; default domain as the feature history resolves it; other levels as written. |
| W8 Features order when `updated:` is declared | Fixed: always id order, the manifest alternative v9 admits; tested with an analysis declaring `updated:`. |
| W9 two claims without a probe | Fixed: the probe executes the ladder on an absolute path and the frontmatter reader on a multi-line value. |
| W10 v9 derivation condition not argued | Fixed: a paragraph after the criteria; a test that a second run never reads its previous output. |

## Round 4 — 2026-10-17, owner-requested beyond the cap (R16), FAIL, 16 findings

The owner then decided page names per lens, empty-state pages and the catalog tree (R17),
and warned that F-069 was taken on `main` (R18): the unit is renumbered F-072 and cites
`SPIKE_kb_viewer.md`. Brought back to the owner, not to a fifth round.

| Finding | Disposition |
|---|---|
| B1 `test_docs_site.py` in every `package.json` | Fixed: shared, never packaged, like every shared test; `npm pack --dry-run` check in the Test Strategy. |
| B2 criterion 5 vs the probe on absolute paths | Fixed: an entry is followed only if it ends inside the docs root, absolute or not; the probe applies the same rule (field 157 / 25 / 8). |
| M1 "Features" for every lens | Owner ruled (R17): Features for code and knowledge, Engagements, Courses; named by the project's default domain. |
| M2 workflows "22 file condivisi" stale | Fixed: listed in the Impact, with the count taken after the merge with `main`. |
| M3 tree vs the catalog's exclusions | Owner ruled (R17): the tree is the catalog's own list, plus the resume notes Open work opens. |
| M4 criterion-16 test red on existing text | Fixed: it checks only the lines this unit adds. |
| W1 pages hidden when empty | Owner ruled (R17): always present with an empty-state line. |
| W2 six outcomes of the reading frontier | Fixed: every outcome labelled, including the two without a total. |
| W3 function name and mechanism in the Functional Spec | Fixed: removed. |
| W4 the ladder check runs a copy | Fixed: the implementation's test compares the walk with `kb_time_cycle`'s edges; the probe's copy is declared. |
| W5 two field figures not from the probe | Fixed: the probe reports status groups and declared `updated:` for workstreams and analyses. |
| W6 `mkt_docs` under-specified | Fixed: discovery covers it, project name from the docs root's README, fixtures for `mkt_docs`, ambiguous and missing roots and `--docs-dir`; the probe recognises `mkt_docs`. |
| W7 knowledge-base wording without a knowledge base | Fixed: search sentence and id marks depend on the knowledge base being present. |
| W8 no ledger row for the family scope | Fixed: r29 (basis R14), written at closure. |
| W9 unnamed symbols; the "one-release rule" | Fixed: `build_index`, `project_default_domain` named; one release cited to R14. |
| W10 length; review history in the Diary | Fixed: Diary reduced to decisions; verdicts left to the log. |

## Round 5 — 2026-10-17, review of the R20 rewrite, beyond the cap (R21), FAIL, 21 findings

Brought back to the owner, who decided the chronology, the audit documents, the
marketing units page and to publish without a further round (R23); the side session's
dated-entry unit is a dependency (R22).

| Finding | Disposition |
|---|---|
| B1 project notes and manifest on no page | Fixed: project notes on Home and Open work; manifest shown as a lookup inventory from Home and Rules. |
| B2 chronology "selects nothing" false; no placement | Owner ruled (R23): dated events only, no analysis start/end, no state filter, "Lately" = most recent; r29 worded now. |
| B3 Diary and review-log readers ruled MISSING | Fixed: `section_body`, `parse_review_log` EXISTS; probe uses them (653 field, 343 here). |
| M1 holds when, value, also concerns cut | Fixed: shown as written, never evaluated; criterion 6. |
| M2 criterion 4 pointed at a removed Overview | Fixed: per-item counts against the probe. |
| M3 guard against state outside the work pages; r28 | Fixed: restored, sorting by name and date only. |
| M4 forks and loops in replacement chains | Fixed: every branch, stop message; tested. |
| M5 12-hex qualifier | Fixed. |
| M6 sanitizer and injection tests | Fixed: tags, link schemes, no images; tests named. |
| M7 Interface Contract below the template | Fixed: idioms, five flows, addresses, feedback for removed items and missing data. |
| M8 chronology links outside the site | Owner ruled (R23): request records, review log, project and resume notes have pages, not tree entries. |
| M9 marketing has no analyses | Owner ruled (R23): no units page on a marketing project. |
| M10 the check rule excluded the chronology | Fixed: the rule covers orienting and resuming, where the agent reads the Diary and what lies behind it. |
| W1 no Actors | Fixed. |
| W2 grounding of new names; guides "as rules" | Fixed: names declared NEW; comprehension guides under "How it works". |
| W3 units order justification | Fixed. |
| W4 dropped edge cases | Fixed where they change behaviour (missing source, not readable, not a git repository, missing root, merged topic, ties). |
| W5 search, absence, traversal untested | Fixed: criterion 9; traversal test. |
| W6 `derived_from` resolution hidden as EXISTS | Fixed: INADEQUATE, tested against `kb_time_cycle`'s edges. |
| W7 chronology reader under-specified | Superseded by R22: the dated-entry unit sets the rules. |
| W8 revision narrative in the Diary | Fixed. |
