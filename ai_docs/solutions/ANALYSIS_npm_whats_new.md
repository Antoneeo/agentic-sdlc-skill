---
id: F-070
feature: "What's new" for users on the npm pages
status: COMPLETED
level: L3
start_date: 2026-10-13
end_date: 2026-10-28
domain: code
---
# Feature Analysis: "What's new" for users on the npm pages

## Objective

Each of the four packages' npm page — its `README.md` — shows what changed in the
published version, written for the people who install it, not for the agent that
built it (REQUEST R1, R2). Today the page carries no change information: a user
upgrading from 1.45.0 to 1.49.0 learns what changed only by opening a CHANGELOG
written in implementer vocabulary, and the owner had to ask the agent for a
user-facing rewrite to brief the team (R1).

Elicitation (REQUEST R6–R8) settled what no source settled: the page shows the
**latest release only**, with a link to the full CHANGELOG (R7 Q1); the first edition
also summarizes the 1.49.0 wave, published without notes (R7 Q1, option text); the
user text is **approved by the owner before the tag** (R7 Q2); the F-057 "Shared
project memory" block **moves from the README top into the features** (R7 Q3); the
notes get an agent review **only when they add content** to what was already
reviewed (R8). Derived, with their weighing:

- **Source of the text** — I take one source, a user-facing `### What's new`
  subsection at the top of each CHANGELOG version, mirrored into the README between
  markers, over (a) a README section written by hand — pro: no tooling; contro: two
  texts that drift, nothing catches it — and (b) a CHANGELOG rewritten for users only
  — pro: one audience, one text; contro: it drops the implementer detail the shipped
  record carries, and released entries are immutable, so the history would be split
  in two styles. The mirror keeps one source and makes drift a failing check.
- **Language** — I take English over Italian, the owner's language and that of the
  root CHANGELOG preamble: pro Italian — the owner's team reads it natively (R1);
  contro — every README the npm pages show is English, the packages address users
  outside that team, and a page in two languages reads as unfinished. R7's context
  showed "English" to the owner.
- **Where the F-057 block lands** (R7 Q3, "tra le feature", option text recorded in
  R8) — I take its own section right after each README's features section, wording
  unchanged, over a bullet inside the features list: pro bullet — literally among the
  features; contro — the block is two paragraphs (including the three-file vendoring
  requirement) and becoming a bullet means rewriting prose F-057 reviewed. The option
  the owner chose named the benefit as the page opening with the introduction and the
  real news; both placements give that.

## Feature Vision

Traces to the APPROVED project Vision (v9, 2026-10-17), `## Goals`: "Be installable,
upgradable and maintainable by the people who use it … Packaging, distribution,
installation and the product's own tests are part of the product". Knowing what an
upgrade brings is part of being upgradable. Actors: **Team lead needing governance**
and **Solo developer using an AI agent** (project Vision `## Actors`); the owner,
releasing the family, is the second.

Non-goals:
- No history of earlier versions on the page (R7 Q1): the link covers it.
- No rewrite of released CHANGELOG entries; the 1.49.0-wave summary goes in the next
  release's notes, not into its own section.
- No GitHub Releases, website or announcement channel: the npm page only (R1).
- No `repository` field in the `package.json` files: the link is an absolute URL.
- No change to review doctrine: R8 is applied through `review.md` §When a review is
  due as it stands (FS5 states the reading).
- No change to anything an installed skill contains: the packages' READMEs and
  CHANGELOGs ship in the tarball, but the skill folder copied into a client does not
  include them.

Success signals: after the next publish of each package, its npm page shows its
introduction followed by "What's new in <published version>"; from then on a package
cannot be published with notes missing or a README that disagrees with its CHANGELOG.

## Use Cases / User Needs

- **UC1 (Team lead needing governance)** — after a new version is published, read on
  the package's npm page what changed for the people using it, and pass it to the
  team without filtering agent-only detail (R1, R2). *Benefit: upgradable by the
  people who use it.*
- **UC2 (Solo developer using an AI agent)** — before or after upgrading, see which
  files the version adds and which commands (R3, R4), and whether anything must be
  done on upgrade (the agent's addition, same benefit). *Benefit: same.*
- **UC3 (Solo developer using an AI agent, releasing the family)** — approve the
  user text of each release before it reaches a public page that stays as published
  until the next version (R7 Q2). *Benefit: same; what is upgradable must also be
  described truthfully.*

Grounding: npm page, `README.md`, `CHANGELOG.md`, `publish_all.bat`,
`GUIDE_release.md`, the "Shared project memory" README section — EXISTS, by those
names. "What's new" section and the `### What's new` CHANGELOG subsection — NEW,
introduced here.

## Functional Spec

- **FS1 — The page section.** Each README shows, after its introduction and before
  its first `##` section (code: `## Key Features`; KB and marketing: `## What it
  does`; Course: `## Install and initialize`), a `##` section headed
  `What's new in <version>`, where `<version>` is the package's own version; its body
  is the `### What's new` text of that version's CHANGELOG section, followed by one
  line linking the package's full CHANGELOG. The region holds nothing else, except a
  comment naming where the text is edited, which the page does not show.
- **FS2 — A version without notes.** When the CHANGELOG section for the package's
  version has no `### What's new`, or an empty one (every version released before
  this unit), the region is empty — its two bounds on consecutive lines — and the
  page shows no such section, never another version's notes.
- **FS3 — Check and write.** The section for version V is the `## ` heading whose
  first bracketed token is exactly `[V]`, whatever follows it (` - date`); a
  `## [Unreleased]` heading is never V's, so the check is meaningful only once the
  bump has set both `package.json` and the heading (FS5 orders them). Two `## [V]`
  headings, or two `### What's new` in V's section, are ambiguous and fail. Checking
  reports, per package, one of: agrees; differs; region bounds missing, duplicated or
  out of order; no CHANGELOG section for V; ambiguous. Any outcome but "agrees" fails.
  The comparison ignores line-ending differences (a `git archive` export and a CRLF
  checkout of the same commit agree). Writing regenerates the region only, leaves
  every other byte of the README unchanged, keeps the file's line endings, replaces
  the file whole or not at all (a failed write or rename leaves the previous file and
  no leftover file), and refuses — writing nothing — when the bounds are missing,
  duplicated or out of order, or the section is ambiguous. Writing twice changes
  nothing the second time.
- **FS4 — Publishing.** Before a package is sent to npm, the publish run refuses it
  when its version has no non-empty `### What's new` or its README disagrees, naming
  the package and the fix. A package already on the registry at its version is
  skipped first, as today, and is never refused by this check.
- **FS5 — The release step.** At the bump, for each bumped package, in this order:
  set the version in all bump points including the CHANGELOG heading; write
  `### What's new` in the users' terms — a "New files" table first when the version
  adds files (file, skill, who reads it — R3, R4), then new commands, then anything a
  user must do on upgrade; nothing only the agent reads (R2); regenerate the README
  region; check every bumped package, notes required. Then the agent-review ruling
  (R8): the README region is the same text as the CHANGELOG lines, which the check
  proves, so the two are judged as one — a text that states nothing the units'
  reviewed artifacts do not already state is NOT DUE under `review.md`'s CHANGELOG
  kind, its REVIEW_LOG row reading `NOT DUE: release metadata; CHANGELOG What's new
  and the README region mirrored from it; mirror check agrees`; a text that adds a
  claim (an upgrade instruction no reviewed artifact states, say) gets a scoped review
  of that part. Then the agent shows the owner the text with the ruling and waits for
  approval before the tag; a change to approved text is approved again (R7 Q2). The
  check before the tag is what keeps FS4's refusal a backstop.
- **FS6 — First edition.** The first release of each package after this unit also
  summarizes what that package's 1.49.0-wave version (code 1.49.0, KB 1.32.0,
  marketing 0.27.0, Course 0.1.0-beta.14) brought, marked as such (R7 Q1). Until a
  package has carried it, the duty is listed by package in a dated project-wide note,
  which the session orientation shows; each package's release removes its name, and
  the note goes when the list is empty.
- **FS7 — The F-057 block.** The "Shared project memory" section leaves the top of
  the code, KB and marketing READMEs and becomes its own section right after their
  features section (code: after `## Key Features`; KB: after `## Key features`;
  marketing: after `## What it does`), wording unchanged (R7 Q3). The Course README
  has no such block.

Acceptance:
- **A1** Given a CHANGELOG section for the package version with a non-empty
  `### What's new`, when written, the region equals comment + heading + that text +
  the link (FS1).
- **A2** Given no `### What's new`, or an empty one, for that version, the region is
  empty and checking agrees (FS2).
- **A3** Given a README region edited by hand, checking fails naming that package;
  writing restores it and touches nothing outside the region (FS3).
- **A4** Given missing, duplicated or reversed bounds, or an ambiguous section,
  writing refuses and leaves the file byte-identical (FS3).
- **A5** Given a CRLF README, writing keeps CRLF; given the same text with LF and CRLF
  endings, checking agrees; given a write that fails while writing the temporary file
  or while replacing the README, the README is unchanged and no temporary file remains
  (FS3).
- **A6** Given a package not on the registry whose version lacks notes, the publish
  run prints `[FAIL]` naming it and publishes nothing; given packages already on the
  registry, it skips them and never refuses (FS4).
- **A7** On this repository after the unit, checking all four packages agrees (FS2).
- **A8** The release guide states FS5's order, content rules, review ruling with its
  row wording, approval stop, and the notes-required check in its battery (FS5).
- **A9** The project-wide note lists the four packages for FS6; each package's first
  notes carry the 1.49.0-wave summary, at the owner's approval of that release, and
  its name leaves the note in the same release commit (FS6).
- **A10** Each moved F-057 block is byte-identical to its text before the move, and
  sits where FS7 says (FS7).

## Interface Contract

Fires: the npm page is a surface the user perceives; the mirror's command line, the
approval stop and the publish run's refusal are surfaces the agent and the owner act
on.

- **npm visitor (UC1, UC2) → npm page.** Idiom in use: the README as the page. Flow:
  the owner publishes → npm renders the published `README.md`, dropping HTML comments
  (probed, `harness_npm_whats_new/PROBES.md`) → the visitor reads the introduction,
  then "What's new in <version>", then follows the link to the full CHANGELOG on
  GitHub. Feedback: the version in the heading equals the version npm shows beside the
  package name. Constraint: a published README cannot change until the next version.
- **Releasing agent (UC3) → `scripts/whats_new.js`.** No argument checks every
  package; `--write` regenerates; `--require` also fails a package without notes; one
  or more package directories may be named. Flow: the command reads each package's
  version and hands the region mirror (`scripts/md_region.js`) the CHANGELOG, the
  version, the title `What's new`, the region name `whats-new` and the rendering; the
  mirror compares or writes. Feedback: one line per package (`[ok]` agrees / updated,
  `[FAIL]` with the reason and the command that fixes it); exit status 0 only when
  every named package agrees or was written. Idiom: the `[ok]` / `[FAIL]` lines of
  `publish_all.bat`, its consumer.
- **Releasing agent → owner (UC3): approval stop.** The agent shows the text of each
  bumped package in chat, with the review ruling (NOT DUE or the scoped review's
  verdict), and waits; nothing is tagged before the owner's approval.
- **Owner → `publish_all.bat`.** Per package, in the script's order (code, kb, mkt,
  course), after the registry skip, the run calls `whats_new.js --require` on that
  package; on failure it prints `[FAIL]` after the command's message and stops before
  that package's `npm publish`. A package earlier in the order may already be
  published by then: the check before the tag (FS5) is what prevents reaching that
  state. Feedback on success: today's lines plus the command's `[ok]` line per
  package published.
- Feasibility flag: the link must be absolute — no `repository` field exists in any
  `package.json`. Checked: the four CHANGELOG URLs under
  `https://github.com/Antoneeo/agentic-sdlc-skill/blob/main/` answer 200.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| extract one subsection of one version's section from a release record | MISSING | — | grep `changelog` (case-insensitive) over `skills/agentic-sdlc-skill/scripts/`, `scripts/`, `distributions/*/scripts/` (ANALYZED) and the root `*.bat` (in no audit area — opened in full): two hits, prose in `test_intent_focus.py` and a golden fixture document; the one Node heading parser, `scripts/lib.js` `loadTemplates`, reads fenced blocks of `templates.md` only |
| keep a named marked region of a document equal to given text | MISSING | — | grep `<!-- *(begin\|end\|generated\|start)`, `marker`, `replace_block` over the same areas: whole-file `GENERATED` headers (`sdlc_core.py::INDEX_HEADER`, `knowledge.py`) and the client-detection `homeMarker` paths in `scripts/lib.js`, none owning a region of a document |
| keep files identical across the distributions | EXISTS, not reused | `skills/agentic-sdlc-skill/scripts/shared_files.py` | re-read its docstring: whole-file SHA-256 per manifest entry; a README region differs per package by design |
| know a package's own version | EXISTS | `package.json` `version`, kept in step by `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py::test_the_installed_skill_says_which_version_it_is` | re-read: asserts `package.json`, `gemini-extension.json` and `SKILL.md` agree; the command keys off the same value |
| publish the family's packages, refusing on a failed precondition | EXISTS (unmapped) | `publish_all.bat` `:pub` | re-read, and probed (`PROBES.md` P1): with every version on the registry, four skips and no publish call. Repository-root files are in no audit area, so the Component Map's silence there is unread; this unit adds the row |
| state the release procedure | EXISTS | `ai_docs/reference/GUIDE_release.md` | amended (FS5) from a dated entry appended to its source snapshot |

The two MISSING rows are one component, **region mirror** (`scripts/md_region.js`):
given a Markdown release record, a version, a subsection title, a target Markdown
document, a region name and a rendering function, it checks or writes the region
`<!-- <name>:begin -->` … `<!-- <name>:end -->` so that it holds the rendered
subsection, or nothing when the subsection is absent or empty. "What's new" is one
consumer, `scripts/whats_new.js`, which supplies the title, the region name, the
rendering and the package discovery. A second consumer — another subsection into
another region — uses the same functions unchanged. Split rule (`architect.md` §4):
no consumer outside this unit now or in the roadmap, it cannot ship before it, no own
risk surface → the first phase of this plan, with its own tests.

## Guide check

- CURRENT guide covering what this touches: `GUIDE_release.md` (amended by this unit)
- High-complexity component understood here that no guide covers: no

## Impact

| Path | Change | Why |
|---|---|---|
| `scripts/md_region.js` | ADD | the region mirror (FS1–FS3); dev-only, in no `files` |
| `scripts/test_md_region.js` | ADD | its battery (A1–A5); dev-only |
| `scripts/whats_new.js` | ADD | the "What's new" command: discovery, rendering, `--write`, `--require` (FS1–FS4); dev-only |
| `scripts/test_whats_new.js` | ADD | its battery (discovery, A6's command half, A7); dev-only |
| `README.md` | MODIFY | region bounds before `## Key Features`; F-057 block after it (FS1, FS7) |
| `distributions/kb-agentic-skill/README.md` | MODIFY | bounds before `## What it does`; block after `## Key features` |
| `distributions/mkt-agentic-sdlc/README.md` | MODIFY | bounds before `## What it does`; block after it |
| `distributions/course-creator/README.md` | MODIFY | bounds before `## Install and initialize` |
| `publish_all.bat` | MODIFY | `:pub` calls `whats_new.js --require` after the registry skip (FS4) |
| `ai_docs/reference/.sources/release-runbook-course-creator.md` | MODIFY | dated owner-decision entry (R7, R8), with the `[Unreleased]` heading correction |
| `ai_docs/reference/GUIDE_release.md` | MODIFY | FS5 at the bump step, the notes-required check in the battery, new `source_hash`; its `[Unreleased - X.Y.Z]` wording corrected to the `## [Unreleased]` practice since 1.49.0 |
| `ai_docs/audit/project_notes.md` | MODIFY | dated note listing the four packages owing FS6's first edition |
| `CHANGELOG.md` ×4 | MODIFY | `[Unreleased]` entry for this unit |
| `ai_docs/strategic/architecture.md` | MODIFY | Component Map rows for the region mirror and the publisher (closure) |
| `ai_docs/solutions/harness_npm_whats_new/` | ADD | npm stub, probe runner, `PROBES.md` (P1, FS4 RED, comment rendering) |

The scripts use Node's standard library only; no dependency. Package directories
are discovered as the repository root plus `distributions/*/` holding a
`package.json`, so no fifth list of the packages is written. The link is
`https://github.com/Antoneeo/agentic-sdlc-skill/blob/main/<package path>/CHANGELOG.md`.
A write goes to a temporary file in the README's directory, renamed over it; a failed
write or rename deletes the temporary file before reporting (a killed process cannot,
and leaves it visible in `git status`).

Populations at rest: every version already on npm keeps its README without the
section — immutable, and FS2 makes the repository agree with that until each
package's next bump. The course README's prose "Version 0.1.0-beta.4" is stale; it is
outside this unit and the generated heading does not depend on it.

### Preservation constraints

| id | bound to | callers | must stay true | evidence |
|---|---|---|---|---|
| P1 | `publish_all.bat` | the four `call :pub` lines in the same file | a package already on the registry at its local version is reported skipped and never reaches the new check or `npm publish` | `harness_npm_whats_new/PROBES.md` P1: four skips, 0 publish calls (baseline 20a92ef8; re-run after the change) |
| P2 | `package.json`, `distributions/kb-agentic-skill/package.json`, `distributions/mkt-agentic-sdlc/package.json`, `distributions/course-creator/package.json` | `npm pack`; TS7 in `scripts/test_clients.js` of the code, KB and marketing packages (Course has no TS7) | `files` lists none of the four new scripts | `npm pack --dry-run --json` per package lists no `md_region`/`whats_new`; TS7 green |
| P3 | `README.md`, `distributions/kb-agentic-skill/README.md`, `distributions/mkt-agentic-sdlc/README.md`, `distributions/course-creator/README.md` | npm page; `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py::test_the_readme_keeps_the_permission_for_use_in_your_own_project` (×4 distributions) | every byte outside the region and the moved block is unchanged, the permission phrase included | `git diff` of the four READMEs; the four Python batteries green |
| P4 | `ai_docs/reference/GUIDE_release.md` | `sdlc_check.py stale`/`check` | the guide's `source_hash` matches its snapshot | `check` CLEAN |

## Security and Threat Model

Surfaces: filesystem (the mirror writes READMEs), and publication to a public page
that stays as published until the next version.

- **T1 — private or agent-internal text published.** An employer reference, a
  personal detail or an internal-only note in `### What's new` reaches the page.
  Mitigation: the guide's content rule (users' terms only, R2) and the owner's
  approval before the tag (FS5, R7 Q2); a text that adds claims also gets a scoped
  agent review (R8).
- **T2 — the mirror corrupts a README.** A write outside the region, or a partial
  write, ships a damaged page. Mitigation: refuse on missing/duplicated/reversed
  bounds or an ambiguous section before writing; replace only between the bounds;
  keep line endings; write a temporary file and rename it, deleting it if the rename
  fails, so a write is whole or absent and leaves nothing for a later `git add .` to
  stage; tests A3–A5.
- **T3 — a README that disagrees with its version is published.** Mitigation: the
  check before the tag (FS5) and the publish run's refusal before `npm publish` (FS4,
  A6, probed red at 20a92ef8: four publish calls with no notes); the battery check
  (A7). Residual: a package earlier in the publish order is already published if a
  later one is refused; reachable only when the tree changed after the pre-tag check,
  or that guide step was not run (`git_push_tag.bat` runs no check).
- **T4 — wrong text for the wrong package.** Each package's region is computed from
  its own `package.json` and its own `CHANGELOG.md`, in its own directory; a test
  pins a fixture with two packages at different versions.
- Not touched: authN/authZ, cryptography, network (the scripts make no request),
  personal data processing, external input (they read files of this repository).

## Action Plan

- [x] RED: `scripts/test_md_region.js` (A1–A5) and `scripts/test_whats_new.js`
      (discovery, `--require`, A7) on temporary fixtures.
- [x] GREEN: `scripts/md_region.js`, then `scripts/whats_new.js`.
- [x] READMEs ×4: bounds; F-057 block moved ×3 (A10); `node scripts/whats_new.js`
      agrees.
- [x] `publish_all.bat`: `--require` after the skip; re-run P1 and the FS4 probe
      (GREEN: `[FAIL]`, 0 publish calls).
- [x] Release guide: dated snapshot entry, FS5 and the notes-required check in the
      guide, new `source_hash`; the FS6 project-wide note.
- [x] CHANGELOG `[Unreleased]` ×4; Component Map rows; `E2E_TEST_npm_whats_new.md`.
- [x] Closure review; `MERGE_REVIEW_npm_whats_new.md`; `mark scripts/`; `index`; `check`.
- Each package's next release, not this unit: its first `### What's new`, with the
  1.49.0-wave summary (FS6, A9), through the review ruling and the approval stop.

## Test Strategy

- `node scripts/test_md_region.js` (node:test, stdlib): extraction (subsection found;
  stops at the next `###` or `##`; version absent; `[Unreleased]` never matched;
  subsection absent or empty; duplicated version heading or subsection refused; a
  `-beta.N` version matched literally), region sync (write between bounds; refusal
  leaves bytes unchanged for missing, duplicated and reversed bounds; CRLF kept;
  LF/CRLF texts agree; idempotent; a failing temporary write or final rename leaves
  the README unchanged and no temporary file).
- `node scripts/test_whats_new.js`: rendering (comment, `##` heading, body, absolute
  link per package path), discovery over a two-package fixture with different
  versions (T4), exit status with and without `--require`, and the real repository
  agreeing (A7).
- A6 and P1: `harness_npm_whats_new/run_publish_probe.cmd` with `npm` replaced by a
  stub that never reaches a registry — `none` (FS4: `[FAIL]`, 0 publish calls; RED
  recorded at 20a92ef8) and `all` (P1: four skips, 0 publish calls).
- A10: a probe compares each moved block with its text at `HEAD` before the move.
- A8, A9 and the approval stop are process steps: A8 by the closure review of the
  guide diff; A9 and the stop at the owner's approval of each package's next release,
  scripted in `E2E_TEST_npm_whats_new.md`.
- Existing batteries stay green: `scripts/test_clients.js` (TS7), the four Python
  batteries (P3's permission test), `check` and `check --hybrid` (P4).

## Diary / Current State

**2026-10-13 — opened.** Owner's request R1–R4; direction proposed, not confirmed.

**2026-10-27 — elicitation done, analysis drafted.** R6–R7 settled release count,
approval stop and the F-057 block.

**2026-10-27 — design review PASS (3 rounds, REVIEW_LOG 2026-10-27, F-070).** R8
recorded the owner's ruling on reviewing the notes; probes in `harness_npm_whats_new/`.
The round-3 NITs were applied after the cap and are unreviewed. Next: implementation,
starting from the RED tests.

**2026-10-28 — implemented, closure review next.** Owner's go-ahead R10. RED then
GREEN: `test_md_region.js` 23/23, `test_whats_new.js` 9/9 (the repository check went green
once the READMEs had their bounds). Probes GREEN (`PROBES.md`): P1 four skips and 0
publishes; FS4 refusal with 0 publishes; positive path publishes code and refuses kb;
A10/P3 identical blocks and nothing else moved. `[Unreleased]` handling needed one fix
after RED: a heading `[Unreleased]` must answer for no version. Next: closure review.

**2026-10-28 — closed: closure review PASS → FAIL → PASS (REVIEW_LOG 2026-10-28, F-070 implementation).**
Round 1 found six WARNs, the two that mattered being a mixed-ending README rewritten outside
the region and a ``` line inside a ~~~ fence that could leak the next `###` of the CHANGELOG
into the public notes; both fixed RED-first, with the other ten. Round 2 failed one test that
could not fail for its defect; fixed and confirmed by mutation in round 3. Batteries:
`test_md_region.js` 27/27, `test_whats_new.js` 13/13, `test_clients.js` 63/63, Python
555/882/557/550 OK; probes GREEN (`PROBES.md`). Residuals accepted, the owner's approval
of each release's notes being the control: an unclosed fence (or a ``` opener whose info
string holds a backtick) in a `### What's new` carries the rest of the CHANGELOG into the
notes, as CommonMark itself would render it; an invalid `package.json` is reported against
the folder, not the file. What remains is the owner's: commit and branch, then each
package's next release (FS6 note in `audit/project_notes.md`; E2E S4-S5).
