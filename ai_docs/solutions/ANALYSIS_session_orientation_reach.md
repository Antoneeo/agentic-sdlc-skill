---
id: F-075
feature: What reaches the session — orient under the hook cap, lens choice
description: Why the guide router never reached a session that started with orient wired (16 KB output, router past Claude Code's 2,000-character preview, wired twice), and the reordered, bounded orientation, the wired-twice note and the lens-choice line that fix it.
status: IN_PROGRESS
level: L3
domain: code
topics: [orientation, session-start, guide-router, domain-routing, hooks]
start_date: 2026-10-23
end_date:
branch: feat/f075-orientation-reach
---
# What reaches the session — orient under the hook cap, lens choice

## Objective

An agent in a field project edited without reading the guide that governed the work,
and said why: the session-start orientation was saved to a file and only its preview
was seen (REQUEST R3). The orientation exists so that the guide router reaches every
session; today it does not reach a session on Claude Code once `ai_docs/` is mature.

Mechanism, measured by the probe (`harness_session_orientation_reach/probe.py`, red on
this repo, both wired entry points): Claude Code injects a hook's output up to 10,000
characters; above that it saves the output to a file and injects a 2,000-character
preview. `orient` emits up to 16,000 characters of document text
(`ORIENT_MAX_TOTAL_CHARS`, body only) and prints the router third, after README and
INDEX. In this repo it emits 16,435 characters, the first router row at character 8,366
and the registry table at 10,385 — both outside the preview. The cap is per hook: this
session's own start shows two separate "Output too large (16.2KB) … Preview (first 2KB)"
blocks, one per wired entry (the two settings files listed below).

Wired twice, measured: `.claude/settings.json:8` runs this repo's code-lens `orient`;
`~/.claude/settings.json:21` runs kb-agentic's. Every session here receives two copies.

Second finding (R1, the owner's quotation names "the router" and a single skill): with
sibling lenses installed, neither the orientation nor the per-turn line tells the agent
to choose the lens with `routing.md` — probed: `grep routing.md` over the current
`orient` output of this repo and over the four `remind` lines returns nothing (the only
"routing" in the orient output is an ADR title in the INDEX body).

This unit makes the orientation fit, puts what decides the next action first, says when
it is wired twice for one client, and names the lens choice at session start and on
every turn.

## Feature Vision

`vision/project_vision.md` is APPROVED. Served: Goal "Make the project's intent readable
and *operable* by an agent that arrives with no context" and Goal "Keep understanding
durable across sessions" — the router and the registry are what tell an arriving agent
which guide governs the work and what is open; the Solo developer's "never re-explaining
the project across sessions". Goal "Scale process cost to risk": one orientation copy
shrinks from 16,435 to at most 9,500 characters.

Admission (`vision/rulings.md`, precedent first):
- The orientation rework has no ledger row of its own (admitted before the ledger, M4 /
  F-016, `ENFORCEMENT.md` §4). It lands on **r14** (maintenance, exempt): purpose (orient an arriving agent),
  actor (the agent) and surface (the SessionStart output) unchanged; correctness and
  cost improve.
- The wired-twice note reports a defect of the orientation's own delivery (two copies of
  it) on the orientation's own surface; it orders nothing and assigns nothing (r3). It is
  the twin of F-041's unwired/dead note in `check`, which stays where it is.
- The lens line points at the existing router (`routing.md` §0, shipped with the family);
  it adds no triage or routing authority (r10: the router stays the one authority on
  lens, the level stays the lens's own).
- The per-turn line is ruled by r19 (ADMIT, line 48 — the id is shared with a REJECT twin
  on line 49; this unit means the ADMIT row). Its payload gains the lens choice (scope
  item 3 of the approved plan, R5) and its bound rises from 500 to 600 by the owner (R7).
  The ledger never rewrites a row: new row **r32** records the widened payload and the new
  bound and supersedes r19's bound; r19's row gains "bound superseded by r32".

Non-goals: no check that a verdict was declared or a guide read before an edit (F-076);
no automatic de-duplication of hook entries (the note says; the user removes); no change
to what the router, the registry, README or the topic router contain, only to how
`orient` shows them; no change to `routing.md`'s rules, only worked rows; the docs site
(R6) is out of scope — the planned units' visibility there belongs to the session that
generated the site; the kb `remind` line carries no guide-router duty (observed by the
review; not part of the approved plan — listed as a follow-up candidate, not acted on).

Elicitation: goal, actors, scope and acceptance derive from the approved plan (R5) and
the handoff scope; the owner's words that settle this unit are R5, R7, R8. Two real
doubts were asked and answered: R7 (remind cap 600) and R8 (the frozen 1.0 transcript
no longer guards orient). One choice weighed here, not asked:

- **README body kept, INDEX as a pointer.** I take "README body after the router and
  the registry, cut to the remaining share" over "README as a pointer only": pro — it
  is the curated must-read order, short by design (1,793 characters here), and the
  README template makes it the router's first pointer; contra — it costs share the
  registry could use, which matters only past ~25 workstreams, and the cut is
  line-bounded with a pointer. INDEX (9,352 characters here, a generated manifest) is a
  pointer: nothing in it decides a first action.

Success signals: the probe green on this repo for both wired entry points; a field
session's agent declares a router verdict from the orientation without opening a saved
file.

## Use Cases / User Needs

- **UC1 — Solo developer's agent, session start.** The agent starting a session in a
  project with guides learns, from what is injected, which guide governs the kind of
  work it may be asked for and which workstreams are open — without opening a file the
  harness saved. Benefit: "operable by an agent that arrives with no context".
- **UC2 — Solo developer, machine wired twice for one client.** The developer whose
  client runs `orient` from two settings entries learns it from the session's
  orientation, with the places that carry them. Benefit: "ceremony proportional to
  risk" (one copy, not two).
- **UC3 — Practitioner / developer with sibling lenses installed.** The agent is told,
  at session start and on every turn, to choose the lens with `routing.md` above L1 and
  declare it. Benefit: the Practitioner's "the same gates, restated in their own
  domain's units" — reached only if the agent works under the right lens.
- **UC4 — Agent ruling a mixed request.** The agent reading `routing.md` §2 finds a
  worked verdict for three recurring hybrid cases. Benefit: same as UC3.

Grounding: `orient`, `remind`, `routing.md`, guide router (`reference/INDEX.md`),
workstream registry (`audit/handoff.md`), project-wide notes, settings files — EXISTS.
"Wired-twice note", "lens line" — NEW. "Preview" — EXISTS in the harness (Claude Code's
own term, "Preview (first 2KB)").

## Functional Spec

**FS1 — size.** What a session receives from one `orient` run (every lens, any project)
is at most 9,500 characters, including the project-memory, topic-router and recency
lines that follow the orientation.

**FS2 — order and format.** The output reads, in this order:
1. the header line (unchanged text);
2. the triage line: `Triage every request (Rule Zero): L1 trivial - L2 small - L3
   significant - Spike. Declare the level with the guide-router verdict (a guide below,
   or "no match"). When in doubt, pick the higher level.`;
3. the lens line (FS4), when it applies;
4. `## Guide router (reference/INDEX.md) -- read the matching guide before acting`,
   then one line per guide: `` - `GUIDE_x.md` (STATUS) -- when to consult ``;
5. `## Workstream registry (audit/handoff.md)`, then one line per workstream:
   `- <workstream> · <level> · <branch> · <status> -- <next step>`, then
   `Project-wide notes:` and the notes text;
6. `## Reading guide (README)` and the README body;
7. `## Read on demand`: README, the manifest (`INDEX.md`), the full router with
   provenance, the full registry with since/details — one line each for the files that
   exist, paths under the docs root;
8. the wired-twice notes (FS3) — a cut section says so inline (FS6), with no separate
   note;
9. the devPNT line (`--hybrid`, unchanged text).
In this repo the first router line and the registry heading land inside the first 2,000
characters.

**FS3 — wired twice.** When one client's settings carry two or more distinct
session-orientation commands — Claude Code: project settings, project local settings,
user settings; Codex: project hooks — the output carries one `[note]` per such client:
how many, where (`.claude/settings.json`, `.claude/settings.local.json`, `user
settings`, `.codex/hooks.json`), that each session receives every copy, and to keep one.
Identical command strings count once. Entries for two different clients never add up.
An entry whose validator does not resolve (the `dead` case `check` already reports)
delivers no copy and is not counted; an entry that cannot be told counts.

**FS4 — lens line.** When a sibling lens of the family — the skills named in
`routing.md` §0's table, other than the one running — is installed in the running
skill's own skills directory or in the user's Claude skills directory, the output says
`Sibling lenses installed (<names>): above L1, choose the lens with routing.md and
declare it with the level.` No sibling, or a directory or `routing.md` unreadable: no
line.

**FS5 — per-turn line.** `remind` prints the lens's line followed by the constant
` Above L1, with sibling lenses installed: choose the lens with routing.md and declare
it.` — one line, at most 600 characters for every lens (code 566, kb 531, mkt 525,
course 393), still reading nothing.

**FS6 — cases.**
- A section that does not fit its share is cut at a line boundary and ends with
  `(+N more lines -- read <path>)`; the `Read on demand` block and the notes are never
  cut.
- Router stub (generated, no guides): the section says `no guides yet -- the router
  verdict is "no match"`.
- Router file that is not a generated table (hand-written): its text is shown as
  written, cut like any section.
- Hand-written registry (no generated header): its text is shown as written, cut like
  any section.
- More workstreams than fit: cut with the pointer, like any section.
- A missing or unreadable doc is skipped; with no doc at all the orientation prints
  nothing and exits 0. (The project-memory line that follows it still prints whenever a
  docs root exists — unchanged.)

**FS7 — routing examples.** `routing.md` §2 gains rows for: an interface spec written
for another team (kept and versioned with the repo → code; the requirements another team
must build, distilled from documents the user supplied → knowledge); a document guide
updated because its source spec changed (split: knowledge for re-distilling the guide,
code for the code change the new spec requires, citing the guide); a divergence between
a supplied spec and the code (split: code for changing the code, knowledge for
correcting the distillation when the spec is the one that is wrong — which one is wrong
is the owner's call, not the router's).

Acceptance: AC1 probe green (both entry points: total ≤ 10,000, router line and registry
heading inside 2,000); AC2 FS1 on the worst case (four oversized docs, 40-line topics
index, lens line, two wired-twice notes, `--hybrid`); AC3 FS3 per client; AC4 FS4
present/absent; AC5 `remind` ≤ 600, constant, carries `routing.md` (code, kb, mkt
batteries; course asserted by the code battery running the course entry point); AC6
FS6 cases; AC7 `routing.md` §2 carries the three rows; AC8 batteries ×4, golden ×3,
eval battery green, `check` CLEAN.

## Interface Contract

Actors: the agent in a session (software actor) perceives the SessionStart output
(`orient`) and the UserPromptSubmit line (`remind`); the developer perceives the same
output when running `orient` by hand; the agent reading a mixed request perceives
`routing.md` §2. Idioms reused: `## <label>` headings, `[note]` lines as `check` prints
them, the knowledge overlay's `(+N more lines -- read <path>)` pointer (its topic-router
cut today), the router file's own columns.

Flow, `orient`: the client runs the configured command → the lens entry point hands
`orient` to the knowledge layer, which forwards to the spine's orientation → the spine
reads the fixed doc set (README, INDEX, router, registry) under the docs root, the
client settings files (as today) and the skills directories (names only), and prints
FS2 within its share → the knowledge layer appends its project-memory, topic-router,
recency and time-cycle lines, cut to its reserved share → the client injects the whole
output. `remind`: the client runs it each prompt → the spine prints the lens's line plus
the constant suffix. `routing.md`: the agent reads §2 after §1 when the request is mixed.

Feedback: exit 0 always; no new flag. FS3/FS4 lines appear only when their condition
holds.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| read the fixed orientation docs, confined | EXISTS | `sdlc_core.orient_docs`, `confine_under`, `read_text` | re-read `cmd_orient`: per-doc confine + skip on error |
| split a Markdown table row into cells | INADEQUATE | `sdlc_core._table_cells` (review-log parser) splits on every `\|`; `parse_registry_rows` and four validator sites split inline | router/registry cells escape `\|` (`build_guide_index`, `_registry_cell`); `grep -F '\|'` on this repo's REVIEW_LOG: 0 lines |
| enumerate orient hook entries across configs | INADEQUATE | `sdlc_core._orient_hook_commands` | yields (command, at_user_level); does not say which file or client |
| know the family's lens table | EXISTS (install time, JS) / INADEQUATE (session time) | `scripts/lib.js` `lensTable()` parses shared `routing.md` §0; `init.js` `installedSiblingLenses()` | no Python reader; the session-time path needs one, from the same table |
| bound an overlay's append | MISSING | — | `knowledge.kb_cmd_orient` prints its topic router (30-line cap, no char cap) after the spine; grep `ORIENT_\|cap` in knowledge.py |
| print a constant per-turn line | EXISTS | `sdlc_core.cmd_remind` + profile `remind_line` | r19 contract, `test_remind.py` |

New components, each with its own contract:
- `_table_cells(line)` extended, not duplicated — the cells of one Markdown table row (or
  None for a non-row / separator), split on unescaped `|`, each stripped, `\|` unescaped
  to `|`. Its consumer `parse_review_log` (→ `benefit`, `docs_site`, invariants tests)
  reads the same cells on every log without `\|` (this repo's has none);
  `parse_registry_rows` now uses it too. The four inline splitters in the validator
  (`sdlc_core.py` ~1455/1517/1574/1904) stay as they are — out of this unit. Its orphan
  comparison (`registry_conversion_blockers`) compares the unescaped id against
  `meta["workstream"]`, which is unescaped too — so an id carrying `|` now matches where
  today it never could.
- `lens_table(skill_dir) -> {skill_name: lens}` — Python twin of `lib.js` `lensTable()`,
  same parse (rows whose lens cell is `[a-z]+` and skill cell a backticked
  `[a-z0-9-]+`), from the running skill's `routing.md`; `{}` on any failure.
- `installed_sibling_lenses() -> [skill_name]` — names from `lens_table` other than the
  running lens, found as `name:` in `SKILL.md` (≤ 64 KB) of a subdirectory of two fixed
  directories: the running skill's parent and `<CLAUDE_CONFIG_DIR or ~/.claude>/skills`.
  Test seam `AGENTIC_SDLC_SKILLS_DIRS` (os.pathsep list), like `AGENTIC_SDLC_USER_SETTINGS`.
- `orient_wiring(root) -> {client: {command: place}}` — distinct live orient commands per
  client, with the place each was first found.
- `ORIENT_APPEND_RESERVE` — the share the spine leaves for the knowledge layer's append,
  which cuts itself to it.

Guides: GUIDE_skill_family_changes.md — the shared files count once (applied below).
GUIDE_shared_project_memory.md covers validator composition across distributions (read);
it does not describe `orient`, so this unit's composition change (spine then knowledge
append, now with a shared budget) is stated here, and no guide is due: `cmd_orient` is a
short linear function, not a high-complexity component.

## Impact

Copies: `sdlc_core.py`, `knowledge.py`, `routing.md`, `test_session_start.py`,
`test_skill_invariants.py` are shared (`shared_manifest.json`) and copied identically
into the three distributions — counted once (GUIDE_skill_family_changes.md).

| Path | Change |
|---|---|
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` (+3) | `ORIENT_MAX_TOTAL_CHARS` 16000 → 9500, now the whole output; `ORIENT_APPEND_RESERVE = 2000`; `ORIENT_PER_DOC_CHARS` removed; `cmd_orient` emits FS2 within `ORIENT_MAX_TOTAL_CHARS - ORIENT_APPEND_RESERVE`, reading docs in `orient_docs()` order (unchanged list and order); `_table_cells` extended (escaped `|`), new `lens_table(skill_dir=None)`, `installed_sibling_lenses()`, `orient_wiring(root)`, `_orient_entry_live(root, cmd, at_user_level)` (factored out of `orient_hook_state`), `orient_fit(lines, budget, rel)`, `_orient_router_lines(text)`, `_orient_registry_lines(text)`, `ORIENT_TRIAGE_LINE`; `_orient_hook_commands` also yields the place; `parse_registry_rows` uses `_table_cells`; `REMIND_LENS_SUFFIX` appended by `cmd_remind` |
| `skills/agentic-sdlc-skill/scripts/knowledge.py` (+3) | `kb_cmd_orient`: the append moves into `_kb_orient_append(argv)`, is captured, and `_fit_orient_append(text, budget)` cuts it to `sdlc_core.ORIENT_APPEND_RESERVE` — the topic-router block first, then the whole append — with the pointer |
| `skills/agentic-sdlc-skill/scripts/test_session_start.py` (+3) | size test on the whole output; FS2–FS6 tests; `test_all_sections_emitted`, `test_partial_present`, `test_unreadable_doc_skipped` labels updated; `test_zero_execution_side_effect` unchanged (its README payload is still printed) |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` (+3) | AC7 (three §2 rows) |
| `skills/agentic-sdlc-skill/scripts/test_remind.py`, kb and mkt copies | `REMIND_CAP` 600; suffix asserted; the code copy also runs the course entry point |
| `test_golden_regression.py` code, kb, mkt | runners set `AGENTIC_SDLC_SKILLS_DIRS` to an empty dir (machine-independent); kb's `test_baseline_is_additions_only_over_the_frozen_snapshot` exempts the frozen `orient` section (R8), the frozen file untouched |
| `fixtures/golden_baseline.txt` code, kb | re-captured: only the `orient` section changes (declared here); mkt's corpus runs no orient, its baseline is unchanged |
| `skills/agentic-sdlc-skill/routing.md` (+3) | three rows in §2 (FS7) |
| `shared_manifest.json` (×4) | regenerated |
| `evals/scenarios/hook_orients_session.md` code, kb | pass criteria: router, registry, README sections and the triage line first; INDEX as a pointer |
| `skills/agentic-sdlc-skill/SKILL.md` | Phase-1 bullet: what the hook emits, in its new order |
| `ENFORCEMENT.md` ×4 | §4 first paragraph (order, pointers, cap); remind cost paragraph (characters, 600) |
| `README.md`, `distributions/kb-agentic-skill/README.md`, `distributions/mkt-agentic-sdlc/README.md` | the sentence listing what the hook hands over |
| `ai_docs/strategic/skill_family_agent_workflows.md` | "sotto i 500 caratteri" → 600, plus the lens choice (derived document, `audit_plan.md` refresh duty) |
| `ai_docs/vision/rulings.md` | new row r32; r19 (ADMIT) bound marked superseded |
| `ai_docs/strategic/architecture.md` | Component Map, Validator core row: session-time lens detection and the bounded orient append |
| `CHANGELOG.md` ×4 | `[Unreleased - X.Y.Z]` section (versions provisional; the release sets them, `GUIDE_release.md`) |
| `ai_docs/solutions/harness_session_orientation_reach/probe.py` | the probe |

Blast radius (grep over `skills/`, `distributions/`, `scripts/`; the devPNT symbol index
is stale since 2026-07-08, so text search is the only instrument — Python call sites are
by name, and each hit was opened):
- `cmd_orient` — `sdlc_core.main`; reached by `knowledge.kb_cmd_orient` for all four
  entry points (code, kb, course delegate to `knowledge.main`; mkt hands every
  non-overlay command to `knowledge.main`). Tests: `test_session_start.py`,
  `test_skill_invariants.py` (`main(["orient", ...])`), golden ×3 (byte compare), kb
  `test_kb_recall.py`, `test_kb_capture.py`, `test_kb_time_cycle.py`,
  `test_kb_graph.py`, `test_claim_ledger.py` (substring assertions on the overlay
  append, run on small fixture roots: the append stays far under its share and a
  machine-dependent lens line adds a line no assertion forbids — re-run at GREEN, and
  any that breaks gets the `AGENTIC_SDLC_SKILLS_DIRS` seam).
- `ORIENT_MAX_TOTAL_CHARS`, `ORIENT_PER_DOC_CHARS` — `cmd_orient`,
  `test_session_start.py:105-115`.
- `orient_docs` — unchanged: `docs_site.py:991` (roles by position),
  `test_docs_root.py:167`, `test_docs_site.py:368`, `test_session_start.py:180` (read
  order — kept).
- `_orient_hook_commands` — `orient_hook_state` (unpacks `(cmd, at_user_level)`; it
  will unpack the added place and ignore it), new `orient_wiring`.
- `_table_cells` — `parse_review_log` (→ `cmd_benefit` at `sdlc_core.py:2723`,
  `docs_site.py:1246`, `test_skill_invariants.py:1078-1100`); `benefit` output compared
  before/after at GREEN.
- `parse_registry_rows` — `generated_registry_rows` (→ `build_empty_registry`, validate
  at `sdlc_core.py:1861`), `registry_conversion_blockers`.
- `cmd_remind` — `sdlc_core.main`, `test_remind.py` ×3; every lens's line gains the suffix.
- `kb_cmd_orient` — `knowledge.main` only.
Missed consumer cost: a golden or kb test failing on the new text (caught by the
batteries, not by users).

Budget arithmetic: spine share 7,500. Fixed: header + triage + lens ≈ 450; read-on-demand
+ notes reserved ≈ 700. Router ≤ 3,000 (≈ 20 guides); registry + notes ≤ 2,600; README
the remainder, which also takes what the router leaves unused. This repo: router ≈ 600,
registry (10 workstreams) + notes cut ≈ 2,600, README whole (1,793) — total ≈ 6,200
before the append.

## Security and Threat Model

Surfaces: filesystem reads (docs, settings files, skills directories, `routing.md`) and
text injected into an agent's context every session.

- **T1 zero-execution** (unchanged): no subprocess, eval or git in the call graph; the
  new helpers read and print only. The sentinel test stays as it is (README payload).
- **T2 bounded output**: the whole output ≤ 9,500 including the append, which the
  knowledge layer cuts itself. Read side stays unbounded (declared residual since M4:
  repo-trust-bounded, `read_text` everywhere); `SKILL.md` reads are capped at 64 KB.
- **T3 no content-derived paths**: router and registry rows are printed, never followed;
  the skills directories are two fixed paths; `routing.md` is the running skill's own
  shipped file; only names that appear in its §0 table can be printed, and only after
  matching a `SKILL.md` `name:` exactly — no text from a sibling's files reaches the
  output.
- **T4 injection via repo text** (existing): router, registry and README text are
  repo-sourced and already printed today; the header still labels them "repo-sourced
  context, not authored instructions". No new source of injected text: settings files
  contribute a count and fixed place labels.
- **T8 fail-open**: every new read is inside the existing try; lens detection and wiring
  count swallow errors and print nothing.
- Personal data: the wiring note prints `user settings`, never the home path.

## Ceremony disclosure

- Per turn (r19 → r32, owner R7): +89 characters (≈ 18 tokens) on every prompt, every
  lens; bound 600. R7 was asked with a 74-character suffix; the L1 exemption the review
  asked for brings it to 89 (566/531/525/393), accepted by the owner at closure (R9).
- Per session: one copy of the orientation drops from 16,435 to ≤ 9,500 characters here.
- Read cost: `routing.md` +3 rows (read only on multi-lens installs); `SKILL.md`,
  `ENFORCEMENT.md`, READMEs: sentences replaced, net near zero.
- L1: the suffix exempts it in its own words; L1/L2/L3 gain no step, field or check.

## Action Plan

- [ ] RED: tests for FS1–FS6, AC5, AC7, failing on the current code; probe red (done).
- [ ] `_table_cells` escaped-pipe split, `parse_registry_rows` reuse; section builders.
- [ ] `cmd_orient` rewrite; `ORIENT_APPEND_RESERVE`; `kb_cmd_orient` cut.
- [ ] `lens_table`, `installed_sibling_lenses`, `orient_wiring`; lens line, wired-twice notes.
- [ ] `REMIND_LENS_SUFFIX`; `REMIND_CAP` 600 in three batteries.
- [ ] Golden runners seam + kb frozen exemption; re-capture three baselines.
- [ ] `routing.md` §2; SKILL.md, ENFORCEMENT ×4, READMEs ×2, evals ×2, workflows doc, rulings.
- [ ] Copy shared files; `shared_files.py --update` ×4.
- [ ] GREEN: four batteries, eval battery, probe; E2E_TEST, closure review, MERGE_REVIEW.

## Test Strategy

`test_session_start.py` (shared): AC2 worst-case fixture through the knowledge entry
point; FS2 order and exact line formats; FS6 cut + pointer, `Read on demand` intact,
router stub, hand-written registry, 60 workstreams; FS3 per client via
`AGENTIC_SDLC_USER_SETTINGS` + project files (two Claude entries → note "2"; identical
command twice → none; one Claude + one Codex → none); FS4 via `AGENTIC_SDLC_SKILLS_DIRS`
(sibling → line naming it; own lens only → none; unreadable → none); T1/T3/T8 kept.
`test_remind.py` ×3: cap 600, suffix present, constant. `test_skill_invariants.py`: AC7.
Golden ×3 re-captured with the seam. Probe: both entry points green. Eval battery
(`python -m unittest discover -s scripts -p "test_*.py"`) in all four skill folders.

## Diary

**2026-10-23 — analysis drafted.** Probe red on this repo (16,435 chars; router row
8,366; registry 10,385; both entry points). R7: remind cap 600.

**2026-10-23 — design review.** Round 1 FAIL, round 2 PASS with WARNs folded (details
in REVIEW_LOG); owner R8 settled the frozen golden transcript.

**2026-10-23 — implemented.** RED first (8 failures + 1 error in the session battery,
remind and routing invariants red), then GREEN: batteries code 418, kb 599, mkt 420,
course 413 OK; probe green on both wired entry points (5,751 characters; router line at
522, registry heading at 1,055); review-log parsing identical before and after the
escaped-pipe split (216 rows). Golden: only the orient section re-captured in code and kb;
mkt's baseline unchanged. Next: closure review.
