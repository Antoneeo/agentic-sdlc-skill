---
id: F-085
feature: The agent's working model — constraints extractable, synthesized, recalled
status: COMPLETED
level: L3
start_date: 2026-10-27
end_date: 2026-10-27
domain: code
---
# Feature Analysis: the agent's working model

## Objective

Give the agent, at the moment it acts, the constraints its own unit already states —
above all the **preservation** constraints (what existing code must keep doing), which
today live as prose in the blast radius and are the class behind most review FAILs.
Three moves, no new authored document: make preservation constraints extractable (a
table), derive a short view of a unit's constraints with a command, and recall the
constraints bound to a file when the agent is about to edit it. At closure, the still
valid preservation constraints are copied into the component's guide when it has one.

Scope (R12): the code lens. The parser, the command and the hook live in the shared
core (`sdlc_core.py`, byte-identical in the four distributions); everything that writes,
reports or recalls is gated to the `code` domain, and `validate`'s note also to the code
lens (a profile capability), so the other lenses see no change.
Hybrid is out of this unit: the reader reads `ANALYSIS_*.md` only, and Hybrid design
artifacts reach it once devPNT F-011 puts them on the filesystem.

## Feature Vision

`vision/features/VISION_working_model.md` (APPROVED, R10). This unit advances G1
(FS4), G2 (FS1–FS2), G3 (FS5–FS6, FS11), G4 (FS8) and the instrument of S1 (FS10).
Inherited constraints: nothing below L3 (FS6 guard, FS7 scope); no computed state in
the view or the recall (FS4, FS6); never weaken a gate (FS4 and FS6 closing sentence,
the `review.md` delta); complete without devPNT (no devPNT call); no ceremony ratchet
— every added cost is in `### Ceremony cost` with the owner's acceptance (R12, R13).

Correction disclosed (request record, note after R13): the Vision's Problem says the
Impact table already maps each file to its ids; `probe_impact_bridge.py` on the pinned
sample (`harness_working_model/sample_2026-10-27.txt`) measures 67 of 221 file rows
doing so (115 of 639 over every analysis in both repositories). The recall therefore
keys on preservation constraints, which carry their own binding, and uses Impact
citations only where they exist. The sentence's amendment is proposed at closure.

## Use Cases / User Needs

- **UC1 (Agent)** — about to edit a file bound by a constraint of the open L3 unit it is
  working on, the agent receives those constraints in its context without asking.
  *Benefit: G3, effectiveness (S1).*
- **UC2 (Agent, Owner)** — runs one command and sees the constraints of a unit, each
  with a pointer to its home and, for preservation constraints, the evidence.
  *Benefit: G1, reading cost.*
- **UC3 (Independent reviewer)** — derives callers and behaviours first, then compares
  with the view; a constraint the design states but the diff breaks is a finding.
  *Benefit: S1, gates keep their input.*
- **UC4 (Agent at closure)** — copies the unreleased preservation constraints into the
  component's existing guide, or leaves them where the component map points.
  *Benefit: G4, the future session's agent inherits them.*
- **UC5 (Owner)** — reports a wrong behaviour in a merged change; the agent records it
  with the owner's words. *Benefit: S1's second half has a record.*
- **UC6 (Agent writing the design)** — editing the unit's ANALYSIS, the agent writes a
  sentence that names a path a preservation constraint of the same unit binds; it
  receives that constraint. *Benefit: G3 ("write a claim about").*

Grounding: EXISTS — ANALYSIS, `## Impact`, blast radius (SKILL.md, Phase 3), open L3
unit, guide and `source_kind: code` (`guides.md`), component map
(`strategic/architecture.md`), REVIEW_LOG and its `tier` column, the verdict hook.
NEW — the `### Preservation constraints` table, the `constraints` command and hook, the
`post-merge` tier. No METAPHOR names.

## Functional Spec

- **FS1 Ids.** In an L3 ANALYSIS of the code domain, every use case, functional-spec
  item and threat starts with its id — `UC<n>`, `FS<n>`, `T<n>` — at the start of a
  bullet, `###`/`####` heading or table row, bold or not. Preservation constraints use
  `P<n>` (FS2). Interface Contract items carry no mandatory id (R13). A duplicated id is
  shown at each of its homes; nothing merges or drops it.
- **FS2 Preservation table.** Under `## Impact`, a `### Preservation constraints`
  subsection holds one row per constraint: `| P<n> | bound to | callers | must stay
  true | evidence |`. *Bound to*: one or more backticked repository-relative file paths,
  each optionally `path::symbol`; an elided path (with `...`) binds nothing. *Callers*:
  the enumerated set, or "none outside the file". *Must stay true*: one statement a test
  or probe could check. *Evidence*: the enumeration instrument or the probe that
  established it — never "to be done". A unit that changes no existing symbol writes the
  single line `No existing symbol changed.` instead of the table. The table replaces the
  prose blast radius; the enumeration duty itself is unchanged.
- **FS3 Extraction.** From one ANALYSIS the reader extracts each id'd item of the Use
  Cases, Functional Spec and Security sections (statement = the item's first sentence,
  verbatim, bold title included; binding = backticked full paths in the item, plus the
  files of Impact table rows citing the id) and each P row (statement = *must stay
  true*; binding = *bound to*; evidence = *evidence*). A row whose *must stay true* cell
  starts with `RELEASED (` is extracted as released. Paths compare repository-relative,
  with forward slashes, case-insensitively on Windows.
- **FS4 The view — `sdlc_check.py constraints --unit <id or ANALYSIS name>`.** Prints
  the unit's constraints grouped by home section, in document order, one line each:
  `ID — statement — home:line`; a P line is followed by its evidence; a released row
  shows its release reference. It always ends with one fixed sentence: the view shows
  only constraints written in extractable form, and names the sections to read in full
  — `## Interface Contract` whenever the ANALYSIS has one (its items carry no id), any
  of the three extracted sections holding prose but no id'd item at all (prose beside
  id'd items, such as a closing *Grounding* line, does not name it), and `## Impact`
  when it has neither the table nor the no-symbol line. It prints no count, share, rank,
  marker or order other than the document's. Unknown unit: one error line, exit 1.
- **FS5 Recall query — `sdlc_check.py constraints --file <path>`.** Prints the
  unreleased constraints of every open L3 unit of this tree (an L3 ANALYSIS of the
  `code` domain that is PLANNED or IN_PROGRESS) bound to that path, in FS4's line format, unit by unit,
  followed by FS4's fixed sentence for each unit. Nothing bound prints nothing, exit 0.
  A binding matches when the path equals a bound path, or a bound `path::symbol` has
  that path.
- **FS6 Recall hook — `sdlc_check.py constraints --hook`** (Claude Code PreToolUse,
  matcher `Edit|Write|MultiEdit|NotebookEdit`). Silent — no output, exit 0 — unless all
  hold: (a) the edited file is inside the project, resolved by walking up from the
  edited file's path, never from the hook's working directory (it follows the
  session's `cd`, live probe); (b) FS5 finds an unreleased
  constraint of an open L3 unit U bound to it, or the file is U's own ANALYSIS and the
  new text names a path a P row of U binds (UC6); (c) the session transcript shows a
  Read, Write or Edit by this session of U's ANALYSIS, request record or handoff; (d) the
  last level **declaration** in the transcript is L3. A declaration is a line that opens
  with the level word (`level`, `livello`, `niveau`, `nivel`, `stufe`) followed by the
  level, in the form Rule Zero prescribes: `L1` alone, `L2` or `L3` with `router` on the
  same line. A level quoted inside a sentence is not one; a bare `Level: L1` after an L3
  declaration silences the recall. When all hold it emits `hookSpecificOutput` holding only `hookEventName` and
  `additionalContext`: at most 15 FS4 lines, the `--unit` command for the rest, and
  FS4's fixed sentence. It **never** emits a `permissionDecision`. Any error, an
  unreadable or oversized transcript, a sidechain or a subagent payload: silent. If the
  live probe (Action Plan 1) shows that Claude Code refuses a decision-less PreToolUse
  object, the same output moves to PostToolUse, after the edit (R13 (4a)).
- **FS7 Advisory.** `validate` notes (never errors) an open L3 ANALYSIS whose resolved
  domain is `code` and whose `## Impact` has neither the FS2 table nor the no-symbol
  line, in a lens whose profile claims `preservation_constraints` (the code lens, R12
  (a)). Closed analyses, other domains and other lenses are not checked; `--strict` exit
  codes are unchanged.
- **FS8 Give-back at closure (doctrine).** Each unreleased P row is copied into the
  existing `source_kind: code` guide of the component it binds, under `## Preservation
  constraints`, with the marker `[source: solutions/ANALYSIS_<name>.md#P<n>]`; the
  ANALYSIS keeps its table. That section is a declared exception to the guide's
  code-excerpt floor (`guides.md` §3), and a regenerated guide (§6) carries it over
  unchanged. When the component has no guide, its component-map row in
  `strategic/architecture.md` names the closed ANALYSIS's table. Objective constraints
  close with the unit.
- **FS9 Release (doctrine).** A P row stops binding only when the request record holds
  the owner's own words releasing it; the row stays and its *must stay true* cell is
  prefixed `RELEASED (REQUEST_<name>.md#R<n>)`.
- **FS10 Post-merge record.** A wrong behaviour the owner reports in a merged L3
  change is one REVIEW_LOG row: tier `post-merge`, model `none (owner report)`, reviewer
  `owner`, notes quoting the owner. L1 and L2 changes get no row (Vision: nothing below
  L3; S1 compares L3 units). It is not a review: `benefit` excludes it from review
  counts, the docs site's chronology shows it as a defect report rather than a review,
  and the S1 baseline counts it as its own kind.
- **FS11 Clients without hooks.** The doctrine tells the agent, in an L3 unit, to run
  `constraints --file <path>` before its first edit of a file in a session; the hook
  makes that automatic where wired.

Acceptance: FS1–FS7 and FS10 by the battery (`test_constraints.py`) and the harness;
FS6's output form by the live probe (Action Plan 1); FS8, FS9 and FS11 by doctrine
invariants (`test_skill_invariants.py`); the whole on this unit's own ANALYSIS, whose
view must list every id'd item and P row here and end with the fixed sentence naming
only `## Interface Contract` (`harness_working_model/probe_self_view.py`).

## Interface Contract

Fires: new and changed surfaces the agent, reviewer and owner act on or perceive — a
command, a hook's context, a template table, a log tier.

- **Command (UC2, UC3).** Idiom reused: `sdlc_check.py <subcommand>`, one line per item,
  exit 1 on error (as `verdict`, `review-map`). Flow: argv → the kb overlay forwards any
  command it does not intercept → spine → reader → stdout.
- **Hook context (UC1, UC6).** Idiom reused: the installer's constant-command hook spec
  (as the verdict hook), its own entry, marker and opt-out. Flow: Claude Code payload →
  `constraints --hook` → open-unit lookup → binding match → transcript scan → JSON
  context. Feedback: the lines appear beside the tool call; silence is the normal case.
  **New idiom, declared:** a hook that informs without deciding — the verdict hook only
  denies.
- **Template (UC4).** Idiom reused: a markdown table with backticked anchors, as the
  Capability Ledger.
- **Log tier (UC5).** Idiom reused: one REVIEW_LOG row; new value `post-merge`.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| read an ANALYSIS's frontmatter and sections | EXISTS | `sdlc_core.load_frontmatter`, `section_body`, `list_analyses` | re-read: flat frontmatter, first heading matching an alias |
| know the open L3 units | EXISTS | `sdlc_core._open_units` | re-read 1342–1364: L3 + PLANNED/IN_PROGRESS, plus request records |
| resolve an artifact's domain | EXISTS | `sdlc_core.resolve_domain`, `project_default_domain` | 334, 348 |
| read what a session declared and did | INADEQUATE | `sdlc_core.transcript_facts` | English `Level: X1` only, matches prose quotes, no unit detection (`probe_session_level.py`, C1 and the B3 red cases) |
| extract constraint items and bindings | MISSING | — | grep `UC\d`, `FS\d`, `T\d`, `Impact`, `blast` over `scripts/*.py`: comments and tests only |
| inform the agent before a tool runs | MISSING | — | the only PreToolUse hooks deny (`cmd_verdict`) or exit 2 (`cmd_gate`) |

The two MISSING rows become one component, the **constraint reader** in `sdlc_core.py`:
`parse_constraints(text) -> list[dict]`, `unit_constraints(root, unit)`,
`file_constraints(root, path)`. Its contract names no feature: it reads id'd items and
P rows from an ANALYSIS. The INADEQUATE row gets a sibling, `transcript_work(path)`,
sharing the bounds constants; `transcript_facts` is not changed (P2).

## Guide check

- CURRENT guide covering what this touches: none for hooks or the validator
  (`GUIDE_skill_family_changes.md`, covering how the copies count, read).
- High-complexity component understood here that no guide covers: no.

## Impact

| File | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` (shared ×4) | ADD constraint reader, `transcript_work`, `cmd_constraints` and its subparser; MODIFY `cmd_validate` (FS7 note, code domain), `cmd_benefit` (exclude `post-merge`) | FS3–FS7, FS10 |
| `distributions/*/scripts/sdlc_core.py` (×3) | verbatim copy | drift guard |
| `skills/agentic-sdlc-skill/scripts/test_constraints.py` (NEW, shared ×4), `shared_files.py` `SHARED_FILES`, `shared_manifest.json` (×4) | battery | FS1–FS7, FS10 |
| `skills/agentic-sdlc-skill/scripts/fixtures/golden_baseline.txt` | regenerated: the golden `ANALYSIS_pick_list.md` (L3, IN_PROGRESS, no table) gains the FS7 note | P9 |
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` (code entry point) | the profile claims `preservation_constraints`, the optional capability FS7 is gated on | FS7 |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/fixtures/golden_baseline.txt` | unchanged: the kb profile does not claim the capability, so its frozen 1.0 transcript survives (its corpus has the same open `pick_list` in the code domain) | P9 |
| `skills/agentic-sdlc-skill/templates.md` (code) | ANALYSIS template: id convention; `### Preservation constraints`; REVIEW_LOG `post-merge` | FS1, FS2, FS10 |
| `skills/agentic-sdlc-skill/SKILL.md` (code) | blast-radius paragraph writes the table; closure give-back and release lines; FS11 line | FS2, FS8, FS9, FS11 |
| `skills/agentic-sdlc-skill/guides.md` (shared ×4) | §3: the declared exception; §6: the section survives regeneration | FS8 |
| `skills/agentic-sdlc-skill/review.md` (shared ×4) | tier list gains `post-merge` and the model list `none (owner report)`; one sentence: derive first, then compare with the view | FS10, UC3 |
| `skills/agentic-sdlc-skill/scripts/docs_site.py` (shared ×4) + `test_docs_site.py` (shared ×4) | `chronology`: a `post-merge` row is added as kind `defect`, not `review` | FS10, P10 |
| `skills/agentic-sdlc-skill/docs_site/strings.js` (shared ×4) | the `event_defect` label, beside the other `event_*` strings (55–62) | FS10, P10 |
| `skills/agentic-sdlc-skill/ENFORCEMENT.md` (code) | the recall hook, its JSON snippet and opt-out | FS6 |
| `scripts/lib.js` | `RECALL_HOOK` spec (`suffix: '; exit 0'`, own marker, matcher of FS6), `wireGlobalRecallHook`, `removeGlobalCommandHooks` returns the spec's name | FS6, P4, P7 |
| `scripts/postinstall.js`, `scripts/preuninstall.js` | wire it after the verdict hook; uninstall names it by spec, not by event | FS6, P7 |
| `scripts/test_clients.js` | recall-hook cases mirroring the verdict-hook block (989–1060) | P4, P7 |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` (shared ×4) | anchors for FS8, FS9, FS11 doctrine | invariants |
| `ai_docs/solutions/harness_working_model/` | `baseline_review_log.py` counts `post-merge`; live hook probe; `probe_hook_timing.py` (T5) | FS10, FS6, T5 |
| `ai_docs/vision/rulings.md` | new row: the view and the recall | ledger |
| `ai_docs/strategic/architecture.md` | Component Map row: constraint reader; Hook wiring widened; five rows point at this unit's P rows | component born, FS8 |
| `ai_docs/reference/GUIDE_shared_project_memory.md` | `## Preservation constraints` with P3, the one P row whose component has a code guide | FS8 |
| `ai_docs/architecture/ADR_2026-10-27_context_only_recall_hook.md` (NEW) | the context-only hook, project from the file, lens-gated note | ADR trigger |
| `ai_docs/strategic/existing_features.md` | entry [085] | catalog |
| `README.md`, `ai_docs/strategic/skill_family_agent_workflows.md` | the derived documents the audit plan ties to `skills/` and `distributions/`: feature, `constraints` command, hook paragraph; the other lenses' READMEs unchanged (code lens only, R12 (a)) | audit plan |
| `CHANGELOG.md` + three distribution CHANGELOGs | `[Unreleased]` | release notes |

### Preservation constraints

| id | bound to | callers | must stay true | evidence |
|---|---|---|---|---|
| P1 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::_open_units` | `ids_on_other_refs`, `cmd_mark`, and this unit's `open_code_units`; none in tests or distributions | returns the same `{id: {analysis names}}` for the same tree; the reader calls it and never changes it | grep `_open_units` over `skills/`, `distributions/`, 2026-10-27 |
| P2 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::transcript_facts` | `verdict_reason` only | the verdict hook's decisions are unchanged: same regexes, bounds and return keys | grep `transcript_facts`; `test_verdict.py` green unmodified |
| P3 | `skills/agentic-sdlc-skill/scripts/knowledge.py::main` | `sdlc_check.main` in every lens | a subcommand not in `INTERCEPTED` reaches the spine untouched, so `constraints` needs no overlay change | re-read knowledge.py 2552–2570 |
| P4 | `scripts/lib.js::VERDICT_HOOK` | `wireGlobalVerdictHook`, `removeGlobalCommandHooks`, `postinstall.js`, `test_clients.js` (the F-076 block) | the verdict hook is wired, found, opted out and removed exactly as today; the recall hook is a separate spec whose `re` cannot match the verdict command and vice versa | grep `VERDICT_HOOK\|wireGlobalVerdictHook\|removeGlobalCommandHooks` over `scripts/*.js` |
| P5 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::cmd_validate` | `validate`, `check`, kb `kb_cmd_validate`, `mkt_check.py` validate/check, ≈15 test call sites | no new error and no change outside the code domain; `--strict` exit codes unchanged; `check` stays CLEAN on every tree it is CLEAN on today | grep `cmd_validate`; `check` on this repository and devPNT before and after |
| P6 | the user's permission prompts | every PreToolUse hook in the user's settings | the recall hook never allows, asks, defers or denies; the permission flow is the one without it | test on the JSON shape; live probe, Action Plan 1 |
| P7 | `scripts/preuninstall.js`, `scripts/lib.js::removeGlobalCommandHooks` | the uninstall loop in `preuninstall.js`; `test_clients.js` | each removed entry is named as the hook it is; two PreToolUse hooks are told apart (`COMMAND_HOOK_NAMES` gave way to each spec's `name`) | re-read preuninstall.js 36–44 |
| P8 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::cmd_benefit` | `benefit`; `test_intent_focus.py`, `test_skill_invariants.py`, `test_constraints.py` | review counts and findings totals stay as today for every existing row; a `post-merge` row adds to neither | re-read 2964–3010: a tier other than design/closure counts as a review today |
| P9 | `skills/agentic-sdlc-skill/scripts/fixtures/golden_baseline.txt` | `test_golden_regression.py` | the only change to the golden transcript is the FS7 note on `ANALYSIS_pick_list.md` and the advisory count it raises, in each command that runs `validate`; every other line and every exit code identical | diff of the regenerated baseline, 2026-10-27: 4 notes and 4 count lines |
| P10 | `skills/agentic-sdlc-skill/scripts/docs_site.py::chronology` | the home-page build; the chronology tests of `test_docs_site.py` | every existing REVIEW_LOG row keeps kind `review` and its text; only a `post-merge` row changes kind | re-read docs_site.py 1248–1252 |

### Ceremony cost

| Cost | Level | Removes | Accepted |
|---|---|---|---|
| P table per L3 that changes an existing symbol | L3 | the prose blast radius | R12 (a) |
| UC/FS/T ids mandatory | L3 | — | R12 (a) |
| recall lines on a bound edit (≤ 15 + one sentence) | L3 | — | R12 (b) |
| copy P rows into an existing guide at closure | L3 | — | R12 (c) |
| one `post-merge` row per defect the owner reports | merged L3 change | — | R12 (d) |
| `validate` note on an open L3 with no table | L3, code | — | R13 (1) |
| `constraints --file` before the first edit of a file, clients without hooks | L3 | — | R13 (2) |
| a second hook process on every edit, in every project, once installed: ~0.25 s (`probe_hook_timing.py`: best 0.24, median 0.25–0.26 on all three paths) | every level, Claude Code | — | R15 |

Doctrine bytes (SKILL.md, templates.md, guides.md, review.md) are measured on the diff
and reported in the merge brief.

## Security and Threat Model

Surfaces: filesystem (reads the transcript and analyses), the hook protocol (output
enters the model's context before a tool runs), availability and cost (runs on every
edit, in every project, when installed globally).

- **T1 Permission widening.** A PreToolUse output with `permissionDecision: "allow"`
  skips the user's prompt. FS6 never emits a decision (P6); a test asserts the JSON has
  only `hookEventName` and `additionalContext`. The live probe checks that Claude Code
  accepts it; if not, PostToolUse (R13), never a decision.
- **T2 Availability.** A validator that cannot run `constraints` (missing, or older) exits
  2, and exit 2 on PreToolUse blocks every edit. The wired command carries `; exit 0`,
  as the verdict hook's (r34), with a 10-second timeout; inside, every failure is
  silent exit 0. Tested in `test_clients.js` and by the live probe with the subcommand
  absent.
- **T3 Transcript read.** The path comes from the payload, as for `verdict`; the same
  size bounds apply, and it is read only after a binding matched. Mitigated.
- **T4 Injection into context.** Constraint text comes from the project's own ANALYSIS,
  which the agent reads anyway; each line is cut at 300 characters and stripped of
  control characters. Residual, stated.
- **T5 Cost on every edit.** Exit before any parse when the project has no docs root or
  no open L3 unit; parse analyses only then; read the transcript only after a match.
  Timed by the harness (`probe_hook_timing.py`, a temporary fixture project, the three paths an edit takes) before release.
- **T6 Implied completeness.** The view and the recall end with the fixed sentence
  naming what was not extracted; no count or marker. Mitigated.
- **T7 Weakened review.** The `review.md` sentence orders derive-then-compare; the view
  never replaces the ANALYSIS or the diff in a review request. Residual: doctrinal.
- **T8 Wrong binding or silence.** A path can miss (renamed file) or over-match; a prose
  line that opens with an L1 level ("Level L1 is the trivial tier…") reads as an L1
  declaration and silences the recall. Both err toward silence, never toward recalling
  on L1 work; the recall is advisory and the view remains. Residual, stated.

## Action Plan

1. Live probe of FS6's output form and of T2: wire the hook in this repository's
   `.claude/settings.json` for one session; red with no output, then decision-less
   `additionalContext` on a scratch file (context arrives, prompt unchanged), then the
   subcommand absent (edit not blocked). Record in the harness; on refusal, switch FS6
   to PostToolUse (R13).
2. Constraint reader + `constraints --unit/--file` (RED: `test_constraints.py` on this
   ANALYSIS and fixtures; GREEN).
3. Hook, `transcript_work`, installer spec, uninstall naming, `test_clients.js`.
4. FS7 advisory and `cmd_benefit`; P5 and P8 before/after; regenerate the golden
   baseline and diff it (P9).
5. Doctrine: templates.md, SKILL.md, guides.md, review.md, ENFORCEMENT.md; invariants.
   Also the docs site's `defect` kind and its `event_defect` string (FS10, P10), which
   no step had named.
6. Copies ×3, manifest, drift test; CHANGELOGs; rulings row; component map.
7. Closure: E2E script, closure review, merge brief, Vision sentence amendment proposal.

## Test Strategy

- `test_constraints.py` (shared): FS1–FS3 on fixtures (ids in bullets, headings, table
  rows; duplicates; P table; released row; no-symbol line; elided paths; path
  normalisation); FS4 lines, closing sentence and no digits outside ids and line
  numbers; FS5 matching; FS6 silence cases (no unit, no read or write of the unit by
  the session, last declaration L1/L2, a level quoted in prose, Italian L3 accepted,
  sidechain, oversized transcript, a bare `Level: L1` after an L3 declaration, a
  non-code L3 analysis) and the JSON shape (no `permissionDecision`); FS4's sentence
  naming `## Interface Contract`; FS7 note on open code-domain units only, none for kb
  or course analyses; FS10 `benefit` totals unchanged by a `post-merge` row.
- `test_docs_site.py`: a `post-merge` row is a `defect` in the chronology; other rows
  unchanged (P10); `test_every_event_kind_has_a_label_string` stays green with the new
  `event_defect` string.
- `test_skill_invariants.py`: FS8 (exception sentence in guides.md §3, regeneration
  sentence in §6), FS9 (release prefix in SKILL.md), FS11 (the `--file` line).
- `scripts/test_clients.js`: wire, already, opted-out, re-wire, removal and naming for
  the recall hook; the verdict-hook cases unchanged (P4, P7).
- Unchanged and green: `test_verdict.py` (P2), `test_drift.py`, `test_golden_regression.py`
  after the declared baseline change (P9), the full battery.
- Harness: the four probes re-run on the pinned sample; the live hook probe; `probe_hook_timing.py` (T5); `probe_self_view.py`.

## Diary / Current State

**2026-10-27 — design drafted.** Vision APPROVED (R10); elicitation round closed (R12:
code lens only; costs a, b, d accepted, c in the recommended option). Probes run:
extractability, Impact bridge, session level.

**2026-10-27 — design review rounds 1 and 2 FAIL; rewritten to current state.** The
findings and what answered each are in REVIEW_LOG. The owner settled the costs the
review found unaccepted (R13).

**2026-10-27 — design review round 3 FAIL at the cap, one BLOCK (a missing UI string)
fixed after it; handed to the owner** with the open findings (REVIEW_LOG).

Found in passing, out of scope: the existing verdict hook's `Level: X1` regex matches a
level quoted inside a sentence (`probe_session_level.py` counts the hits on a real
transcript), so a prose quote can satisfy it. A follow-up for the owner.

**2026-10-27 — design approved (R14); Action Plan 1 done.** Live probe
(`harness_working_model/LIVE_PROBE_2026-10-27.md`): Claude Code delivers a decision-less
PreToolUse `additionalContext` and applies the edit, so FS6 stays PreToolUse; the absent
subcommand behind `; exit 0` never blocks (T2). New fact: the hook runs in the session's
current working directory, so FS6 resolves the project from the edited file's path.
The verdict hook resolves it from the working directory: a second follow-up, with the
prose-quote one. Branch fast-forwarded onto `main` after the 2026-10-27 history rewrite.

**2026-10-27 — Action Plan 2 done: the constraint reader and `constraints --unit/--file`.**
`test_constraints.py` written first (35 RED: missing functions and subcommand; the P1
guard green), then GREEN 36/36. Full battery: 500 tests, the only failures the drift
guard on `sdlc_core.py`, expected until the copies of step 6. `probe_self_view.py`:
this ANALYSIS's view lists all UC/FS/T items and P1–P10 and names only
`## Interface Contract`. Two spec corrections, no behaviour change: the Acceptance line
said "naming no section", which FS4 contradicts for any ANALYSIS with an Interface
Contract; FS4 now states the reading implemented, a section is named only when it holds
prose and no id'd item at all.

**2026-10-27 — Action Plan 3 done: the recall hook and its installer spec.** RED
first on both sides: 19 hook tests failing on the missing `--hook` and 1 on the
missing `transcript_work` (the P2 guard on `transcript_facts` green); 5 installer
tests failing while the 58 existing passed. GREEN: `test_constraints.py` 57/57,
`test_clients.js` 63/63. The open-unit filter became one helper, `open_code_units`,
shared by the recall query and the UC6 branch. P7's `COMMAND_HOOK_NAMES` is gone:
each hook spec carries its `name`, which `removeGlobalCommandHooks` returns and the
uninstaller prints. End to end on this session's own 8 MB transcript, run from another
directory: editing `scripts/lib.js` recalls FS6 and P4 with the closing sentence, in
0.41 s (T5). Full battery: 521 tests, the only failures still the drift guard on
`sdlc_core.py`, expected until step 6.

**2026-10-27 — Action Plan 4 done: the FS7 note and `benefit` without `post-merge`.**
RED first: 4 failing (one note on an open L3 code unit with no record; `--strict`
unchanged; a `post-merge` row in no review figure, not an unstated moment); the silence
cases already green. GREEN: `test_constraints.py` 64/64; `has_preservation_record` is
the one test the note and the view's sentence share. P9: the regenerated golden
baseline differs by the note and the advisory count it raises, in the 4 commands that
run `validate` — no other line, no exit code; P9's statement now says so (it had said
"every other line identical", which the count line contradicts). P5 before/after on
this repository and devPNT: only notes on open L3 units without a table (3 here, 2 in
devPNT) and their counts; exit codes unchanged once this tree's own generated index is
regenerated. P8: `benefit` output byte-identical on both. Found for step 6: the kb
distribution's golden corpus has the same open `pick_list` in the code domain, so its
baseline changes at the copy; row added to the Impact. Full battery: 528 tests, the
only failures still the drift guard.

**2026-10-27 — Action Plan 5 done: the doctrine, its invariants, and the docs site's
defect kind.** RED first: 8 invariants in `test_skill_invariants.py`
(`WorkingModelDoctrine`) failing on the old text; two of them then failed on the new
text through my own test scoping (a `## Notes` heading inside the REVIEW_LOG template's
code block cut the section; a line read without the one before it), fixed without
weakening an anchor; GREEN 83/83. The docs site's FS10 piece was in the Impact and the
Test Strategy but in no step: done here, RED then GREEN (`test_docs_site.py` 107/107),
and the generated page data of a project with a `post-merge` row carries kind `defect`
and the label "defect reported after merge". Doctrine bytes: SKILL.md +907 (read every
session), templates.md +1400, guides.md +555, review.md +585, ENFORCEMENT.md +1658, for
the merge brief. Full battery: 537 tests, the only failures the drift guard, now
naming the seven shared files of step 6; `test_clients.js` 63/63.

**2026-10-27 — Action Plan 6 done: copies, manifests, release notes, ledger, map.** The
kb golden test also pins a frozen 1.0 transcript, every line in order; the FS7 note
raised its advisory count line, a change an existing kb user would see. The gap was in
my design, not the guard: FS7 was gated on the domain, while R12 (a) says the code
lens and the Objective promised the other lenses no change. FS7 is now gated on an
optional profile capability, `preservation_constraints`, claimed by the code entry
point alone (one test: a lens without it sees no note); the kb baseline is back to its
committed bytes, unchanged. The overlay test now reaches whichever entry point the
distribution ships (mkt has `mkt_check.py`, which forwards `constraints` like the
others). `test_constraints.py` joined `SHARED_FILES`; nine shared files copied, four
manifests identical. Batteries: code 538, course 533, kb 828, mkt 540 tests, all OK;
mkt's golden corpus unchanged. CHANGELOGs `[Unreleased]` ×4, rulings r39 (r37–r38 were taken by F-084 on `main`), Component Map
rows (Constraint reader new, Hook wiring widened).

**2026-10-27 — Action Plan 7 done: closure.** Before the review, the branch was
fast-forwarded onto `main` 9709768e (F-084 had touched the same shared files):
conflicts in four CHANGELOGs and the rulings kept both sides (this unit's ruling became
r39), generated files and manifests regenerated, all four batteries green on the
integrated tree. Give-back done on this unit itself (FS8): P3 into
`GUIDE_shared_project_memory.md`, the other rows pointed at by five Component Map
rows; ADR `ADR_2026-10-27_context_only_recall_hook.md`; catalog entry [085]; E2E
script. Closure review FAIL → PASS (REVIEW_LOG): round 1 two BLOCKs outside the
product code (a stale F-081 row the stash had re-added; the S1 instrument counting
`post-merge` as design) and seven WARNs, among them the hook resolving the docs-root
name from the working directory, the 15-line bound per unit instead of per recall,
the T5 timing unproven and the per-edit latency never put to the owner; all fixed
and re-reviewed, `probe_hook_timing.py` measures about 0.25 s per edit on every path.
The owner accepted that latency (R15). Vision amendment of the two sentences on the
Impact's ids: blind check PASS, approved (R16), applied. Proposed follow-ups: the
verdict hook's prose-quote match and working-directory root; the blind check's WARNs
on the approved Vision's text. `check` reaches CLEAN once the change is committed and
`mark` records the changed areas.
