# Changelog

## [Unreleased - 0.26.0]

### Changed
- `guides.md`: a document snapshot is verbatim except for credentials and personal or confidential data the guide does not need, which become `[REDACTED: <kind>]` before the snapshot is written; the guide lists the kinds in `redacted_at_intake:`.
- The session-start orientation (`orient`) now fits under Claude Code's 10,000-character hook limit, even in a project with many documents. Above that limit Claude Code saves the output to a file and shows the agent only the first 2,000 characters, so the guide router never reached the agent. The output is now at most 9,500 characters, including the knowledge layer's lines, and in this order: the triage line, the guide router (one line per guide), the workstream registry (one line per workstream, then the project-wide notes), then the reading guide (README). The manifest (INDEX) and the full files are listed as pointers. A section that does not fit is cut at a line, with a pointer to its file.
- The per-turn `remind` line also tells the agent, above L1 and when sibling lenses are installed, to choose the lens with `routing.md` and declare it. The line's limit rises from 500 to 600 characters (`vision/rulings.md` r32).

### Added
- `check` refuses, in every lens, a line shaped like a credential (a password, token or key with a real value, a private-key header, a password in a URL, a bearer token) in a `corpus/given/` file or in the snapshot of a `source_kind: document` guide. The message names the file, the lines and the kinds, never the value. A human clears a false positive with `credential_scan: reviewed — <reason>` (in the sidecar, or in the guide). A project whose stored sources already hold such a line fails `check` until each is redacted or reviewed (`vision/rulings.md` r35a).
- `adopt`: a dry run listing the document guides that rest on `.sources/` snapshots and what moving each into `corpus/given/` involves. It writes nothing.
- `check` warns when the same text is stored both as a guide snapshot and as a corpus artifact.
- `check` also warns on a `corpus/given/` file with no sidecar, accepts a withdrawn artifact's tombstone sidecar (no bytes, no digest), and, when an `original_path:` is a URI, names `original_ref:` for non-local identifiers. A password inside a URL in that warning is masked.
- Shared claim checks (`check`): a claim's `about` cell may hold several relations separated by `; `, and one reserved predicate, `not-yet-honored-by -> ANALYSIS_<name>`, marks a specification claim the code does not yet honor. `check` refuses the marker when that analysis is missing from `solutions/` or cites neither the claim id nor the id of a row the claim succeeds. `export` drops the markers and says so in one line. Nothing lists or counts claims by the marker (`vision/rulings.md` r33). `memory.md`: a marked claim is cited as not yet true of the code, naming its analysis.
- `verdict --hook` (PreToolUse): refuses an edit when the session declared no guide-router verdict, or never read a guide its verdict names; silent in projects without guides and whenever it cannot tell. Not wired by this package (`ENFORCEMENT.md` §3).
- `orient` adds a note when one client runs it from two settings entries, which means each session gets the orientation twice. Claude Code and Codex are counted separately, an identical command counts once, and an entry whose validator is gone is not counted.
- `orient` adds a line naming the sibling lenses installed beside the skill or in the user's Claude skills directory, and says to choose the lens with `routing.md`. The family list is read from `routing.md` §0, as the installer does.
- `routing.md` §2 gains worked verdicts for four mixed requests: an interface spec written for another team, the requirements another team must build, a guide whose source spec changed, and code that diverges from a supplied spec.
- The shared validator adds an advisory for a code-lens (`domain: code`) L3 analysis, started on or after 2026-10-24, that lacks a filled `## Guide check` section. Analyses of this lens are not checked.

## [0.25.0] - 2026-10-19

Includes everything listed under [0.24.0], which was tagged but never published to npm.

### Added
- `mark <paths> --note "<what was done>"` writes a dated entry `**YYYY-MM-DD — <what was done>.**` at the top of `audit/project_notes.md`. A release or work outside an open unit used to leave no dated event, because the date had to be copied there by hand. Without `--note`, and with no open unit, `mark` says so.
- `validate`: an advisory for a dated entry in `project_notes.md` whose bold does not pair; the chronology then showed the label running into the body.
- Docs site chronology: a Diary entry's label carries its unit id ("F-074 — closed"), so it reads on its own.
- `stale` no longer counts files inside the docs root (`ai_docs/`, `mkt_docs/`) as drift of any area, and `mark` refuses to record it: `validate` already checks the docs root, and every document edit used to leave `check` NOT CLEAN until a redundant re-mark.

## [0.24.0] - 2026-10-19

### Added
- Docs site: `docs_site.py --zip <file>` also writes the site as one .zip to share; unzipped, `index.html` opens on any system. A zip made by hand with Windows PowerShell 5.1 `Compress-Archive` stores `data\core.js`, and on Linux or macOS the page then finds no data; `--zip` always writes `/` names. It refuses a target inside the docs root or the site folder. The `SKILL.md` line names it.

## [0.23.0] - 2026-10-19

Includes everything listed under [0.22.0], which was tagged but never published to npm.

### Added
- Docs site: each card in Open work and each feature in Features links its merge review and its end-to-end test script, when they exist. They were reachable only inside a feature's chain page; who merges looks in Open work while the work is open, who tests looks in Features after it closed.

### Changed
- Docs site: Features are listed newest first by their declared start date; those without a start date come last.

## [0.22.0] - 2026-10-18

### Changed
- F-071: a review weighs effort against what the owner asked for. In a design review, each outcome the owner named (the opening request, any entry widening scope, an approved north star) is a row of the conformance statement, saying where the design serves it and what share of the design goes to it; an outcome no section serves, or one served by a minor share while a secondary concern takes the bulk, is a finding. `review.md` §Reviewing.
- F-071: a review runs where something is left to judge. At level 2 the closure review is due only on a security-sensitive area the lens's Rule Zero names, or at the owner's request; otherwise it does not run and logs no row. After a design or closure PASS, a delta made only of version and release metadata, regenerated indexes and audit-mark records, tool-verified copies of a shared file, and CHANGELOG lines adding no claim is not reviewed: its own check runs and a `NOT DUE` row records it. README or overview prose, an E2E script, a rulings row, doctrine, behaviour, tests and any correction of a review finding are still reviewed. `review.md` §When a review is due.
- `sdlc_check.py benefit` counts `NOT DUE` rows apart, in no review or findings figure.

## [0.21.1] - 2026-10-18

### Fixed
- F-072 (field run): the `SKILL.md` line that announces the docs site now reads `scripts/docs_site.py --root <project> --open` and says to use it to show the project state. Asked for the state, an agent had opened the site in its own client pane, where it renders blank, and improvised a local server; `--open` opens it in the user's browser, where it works offline.

## [0.21.0] - 2026-10-18

### Added
- F-074: every Vision is born from an owner interview. Before any Vision text is written (project, feature, the MKT-VISION, and the devPNT M-VISION), the agent asks the owner six questions in order, re-asking an answer that has the wrong form: the problem as one concrete case, the benefit as a result for someone, the actors including who takes the initiative, a success signal with its starting value, the boundaries, and the known constraints with where each comes from. Then the owner approves a one- or two-sentence north star in their own words; without it no Vision is written, not even a draft. The blind check still tests that the rules hold; the approved north star shows they are the owner's. `vision.md` §The owner interview.

### Changed
- `elicitation.md`: the skip path never covers the MKT-VISION; Wave 1 gathers the facts, the interview gathers the Vision.
- Bootstrap no longer writes a Vision reconstructed by the agent: the installer seeds `mkt_docs/vision/MKT_VISION.md` as a stub awaiting the interview (an existing file is never overwritten).
- A Non-Goal now bounds scope. It rejects a proposal that pursues what it names; it is not a ban on behaviour that already exists and creates no obligation. A behaviour that must never happen is an Invariant or a constraint with its source.
- The MKT_VISION template gains North Star and Problem, the actor with the initiative, signals with starting values, Non-Goals as scope, and the source of every constraint.

## [0.20.0] - 2026-10-18

### Added
- F-072: `scripts/docs_site.py --root <project>` writes a static, read-only website of what the agent reads in the project: what it is (reading guide, Vision, rules, documents), its open work with each next step verbatim, and — with a knowledge base — a map of topics, the facts with the exact passage each comes from, what an inferred fact rests on, and the source documents. It opens from disk with the network off, writes outside the docs root, changes nothing in it, and selects, ranks or recommends nothing. Each analysis opens with the chain the agent works through — Vision, use cases, flows and interfaces, risks, solution study, design and tests, merge brief and E2E script, Diary — the Vision's North Star is shown above the home page, and the guides have a page of their own: the guide router, the operative guides with when to read each, and the code-comprehension guides. The chronology lists the dated events the documents declare (Diary entries, spike outcomes, request-record entries, review-log rows, decision records, dated project notes, notes and sources received), most recent first, read with the same F-073 readers `validate` uses. Shared by the four packages (generator, page and battery are byte-identical spine files).

## [0.19.0] - 2026-10-17

### Changed
- F-073 (shared validator and doctrine): one written form for a dated entry, `**YYYY-MM-DD — label.**`, is taught for spike outcomes and project notes that record an event, and shared readers let a chronology list those events the same way the validator reads them. Two advisories reach marketing, and neither fails a build, not even `--strict`: a HANDOFF `next:` longer than 240 characters on a `level: L3` file updated on or after 2026-10-18 (`next:` now holds only the next step), and, in `check`, an open L3 unit whose id another branch or tag uses for a different analysis. That id check identifies a unit by its ANALYSIS file; a marketing request record names none, so an engagement without an ANALYSIS is not checked yet. The doctrine now says to choose a new id after fetching, and that a session sharing a checkout with another session works in its own git worktree. Advisories print as `[advisory]` lines and never count toward the exit code.

## [0.18.0] - 2026-10-17

### Changed
- F1: closing the last open workstream now empties the generated registry `audit/handoff.md` instead of leaving its stale row behind: with zero `HANDOFF_*.md` sources `index` rewrites it empty (keeping `project_notes.md`), and `validate` reports a generated registry that still has rows but no sources as an error.
- F-069: `graph`, `check`, `stale` and the session-start count are faster on a mature knowledge base, with byte-identical output. Citations of superseded claim ids are found with one pass per living document instead of one scan per (document, id) pair, and one check run reads and resolves each cited extraction once instead of once per claim row. On a synthetic ledger of 2183 rows and 1000 living documents, `graph` drops from 14 s to 4 s. No new flag.

## [0.17.0] - 2026-10-13

### Changed
- F-067: every E3 unit now keeps a verbatim, append-only request record `audit/requests/REQUEST_[engagement].md`, started before the Vision Gate: the owner's opening words and every later statement that settles something (answers, approvals, costs, rulings). Artifacts cite its entries instead of paraphrasing; the shared `review.md` asks for the record and makes an owner statement with no resolving entry a finding. Secrets, personal data and confidential third-party or employer information are redacted. An owner-given `FACT` cites its entry in the Source cell.

## [0.16.0] - 2026-10-08

### Changed
- F-065: every agent review request opens with a fixed REVIEW MANDATE block copied verbatim, which carries `review.md` itself to the reviewer in Standalone and Hybrid alike; §Requesting now lists every input its clauses check (Functional Spec, Interface Contract, Component Map, audit plan, probe harness, closure test evidence). devPNT performs no review: in Hybrid an agent review with verdict PASS precedes every proposal to devPNT, where the human reviews; after the round cap only the user's explicit decision sends an artifact on, with open findings attached.

### Fixed
- Shared memory catalog hashes normalize CRLF/LF, avoiding checkout-dependent index mismatches.
- The validator prints its final check verdict after memory, topic and corpus checks, so their errors count in the summary.

## [0.15.0] - 2026-10-02

### Changed
- F-058: share the canonical `ai_docs/` index writer with code, KB and course. Marketing checks activate only for signaled engagements on that tree; existing `mkt_docs/` behavior remains.
- Diagnose a legacy marketing-format `ai_docs/INDEX.md` with an explicit migration command.

## [0.14.0] - 2026-09-25

### Changed
- **F-026 revised: a real doubt is asked when it emerges.** The question discipline
  no longer sends doubts to the deliverable ("Default non-blocking" is gone). A real
  doubt (a fact the search leaves open, or a choice whose pros and cons do not
  settle it) is asked before the first write that would embed its answer, grouped,
  with the pros and cons of each option. A choice that clearly wins the weighing is
  taken without asking, and the weighing is written next to it — each rejected option
  stated at its strongest; options that serve different needs, none good enough at
  both, that nothing the user wrote ranks are a real doubt, however clear the
  agent's own ranking. Reserved approvals
  are always asked. A real doubt becomes a declared assumption only in unattended
  or delegated work. `review.md` makes an unasked doubt a design-review finding; `dispatch.md`
  tells a subagent to return its real doubts instead of deciding them.

### Fixed
- **`stale` no longer counts the audit plan against the area that holds it.**
  Committing a hash mark of `ai_docs/` changed `ai_docs/audit/audit_plan.md` after
  the recorded commit, so the area went stale again and every re-mark repeated the
  loop. The plan's own edits are now excluded; any other change in the area still
  counts.

## [0.13.0] - 2026-09-19

### Added
- F-057: shared project memory in every lens, no sibling installation required.
  `index` catalogs original documents; `recall QUERY` searches live metadata.
  KB integrity is shared; domain ownership and marketing numerical checks remain.
  Vendored validators now require entry point + sdlc_core.py + knowledge.py.


### Fixed
- **F-056: `stale` no longer reports an area fresh when it cannot evaluate it.** An
  `audit_plan.md` row whose reference no longer resolves (the commit was amended,
  rebased or squash-merged away, or the clone is shallow), whose reference is a git
  hash where git is unusable, or whose reference is unparseable used to print a
  warning, then `[ok]`, and exit 0. It now prints `[stale]` with the re-mark command
  and exits 1, so `check` is NOT CLEAN. A reference that still resolves but is no
  longer an ancestor of HEAD gets a warning before it dangles, and `mark` says to
  commit its result as a new commit. **Teams that squash- or rebase-merge:** a
  reference recorded on a feature branch never reaches the integration branch, so
  re-mark those areas after the merge.

## [0.12.0] - 2026-09-14

### Changed
- **F-055: Apache-2.0 with a NOTICE, in place of MIT.** The package root and the
  installed skill folder now carry `LICENSE` (the Apache-2.0 text) and `NOTICE`
  (the attribution), and `package.json` and the `SKILL.md` frontmatter say
  `Apache-2.0`. Redistributing the skill, or a version you modified, means keeping
  both files. Using it in your own project carries no obligation: the documents it
  creates or templates there are yours, and so is a copy of the validator and its
  tests placed there to check them (README, License). Versions up to 0.11.0 remain
  available under MIT. The README also asks, as a request and not a condition,
  for a mention when the skill is used in commercial work.

## [0.11.0] - 2026-09-12

### Added
- **F-052: the Hybrid seam leaves the mandatory read.** The devPNT ownership
  matrix and its neighbours move to a triggered `hybrid.md`; `SKILL.md` keeps a
  pointer carrying the trigger and what is lost by skipping it. Conservation is
  guarded by a `moved-block-sha256` digest computed from the PRE-MOVE source —
  never from the artifact under test, after a first attempt recorded the digest
  of a mojibake-corrupted file and would have frozen the corruption permanently.
- **The shared spine gains the capability floor, the delegation boundary and
  `benefit`** (F-048, F-049, F-050 — see the code lens's changelog; the files
  are byte-identical across the three packages).
- **F-053: the authoring-floor pointer**, before this lens's instruction to
  draft the MKT-VISION.

### Fixed
- **F-053: a probe in this lens's own harness could not fail.** Its conservation
  check accepted the word `ownership` after the filename, and the pointer's own
  content inventory contains it — so deleting the entire consequence paragraph
  left the harness green. That is the defect the previous unit's review had
  already blocked once, re-introduced in the next unit's probe with a comment
  claiming the opposite. Anchored on the consequence alone, and
  mutation-verified red.
- **F-053: figures that reproduced under no ruler.** This lens's read-diet
  numbers omitted the 94-byte stamp line that its own review-driven correction
  had added, so the corrected figure was invalidated by the correction beside
  it. Re-measured on one declared ruler: Standalone 22,880 -> 20,995 B
  (**-8.2%**), Hybrid 24,527 B (**+7.2%**).

### Read cost
- `SKILL.md` **-4.9%** (22,648 -> 21,541 B) Standalone. A Hybrid session reads
  **+10.7%**, proportionally the largest surcharge of the three lenses, because
  a pointer costs about the same in a contract half the size.

## [0.10.1] - 2026-09-06

### Fixed
- **F-046 shipped a hook that wired nowhere.** `wireRemindHookInto` used the
  ORIENT hook's opt-out marker (`orient-hook-wired`) as its own. That file is
  present on every machine that ever installed the skill, so the installer read
  it as "the user opted out of the per-turn reminder" and never wrote the hook —
  for everyone. Two smaller faults in the same function: the marker was checked
  BEFORE testing whether the hook was already present, and no marker was ever
  written after a successful wire, so the real opt-out could never arm. The hook
  now has its own `remind-hook-wired` marker, checked after the presence test and
  written only on success. Regression pinned in `scripts/test_clients.js` (red
  against 1.32.0: an orient-marked machine got no hook).

## [0.10.0] - 2026-09-06

### Added
- **F-046: the protocol reaches every turn (`remind`, UserPromptSubmit, wired by
  default).** `orient` fires once at session start and decays; a session that
  never loads the skill never had the protocol at all. Measured 2026-09-06: a
  release ran against a `GUIDE_release.md` the session never consulted, because
  `SKILL.md` -- where the duty is written -- had not been read. `remind` prints
  ONE constant line at every prompt, and its first duty is that one: decide
  whether the skill governs the work in front of you and, if it does, LOAD it
  once. The carrier is kb's F-041 item B, LIFTED into the shared spine rather
  than duplicated, so all three lenses share one machine; each lens declares its
  own line in `set_profile(remind_line=...)`. Installing the package wires it
  machine-wide on Claude Code alongside the orientation hook, never instead of
  it; removing the hook entry is a standing opt-out. Per-turn cost disclosed and
  accepted by the owner (`vision/rulings.md` r19, the "no ceremony ratchet"
  Non-Goal's second door), and bounded to stay flat by a contract the new shared
  `scripts/test_remind.py` guards: constant text, zero reads, one line under 500
  characters, argv ignored whole, always exit 0.

### Changed
- **`guides.md` said something false about code guides.** It claimed `stale`
  works unchanged for `source_kind: code` because "the code-excerpt snapshot
  drifts when the code changes". A snapshot is a frozen copy and never drifts:
  freshness is NOT mechanized there, and the duty is the author's twice -- when
  you MODIFY code a comprehension guide describes, and when you merely READ one
  before trusting it. Measured 2026-09-06: the guided module had gained 388
  lines and lost 71 across four commits with `stale` silent.

## [0.9.0] - 2026-09-05

Spine-only release: `review.md` updated byte-identical across the family
(authored in the code lens, code 1.31.0).

### Changed
- **The form budget belongs to the FIRST draft (shared spine `review.md`).**
  The lean operative form is the first draft's form, not the round-3 rescue:
  the review request states the artifact's line count against a budget the
  author fixed before drafting, and an artifact over budget is the reviewer's
  first finding, before content. This replaces "rewrite lean at the latest
  before round 3", which paid for the form only after two rounds had already
  been spent reading a bloated artifact. The ~1,250 -> ~500 line measurement
  already in the file is the budget's anchor.

## [0.8.0] - 2026-09-01

Spine-only release: `review.md` updated byte-identical across the family
(authored in the code lens, F-045 / code 1.30.0).

### Added
- **Review-loop convergence (shared spine `review.md`).** *Revise means
  converge, not accrete*: lean rewrite at the latest before round 3, revision
  archaeology lives in REVIEW_LOG, never in the artifact. *Severity contract*
  stated with every review request: blocker = unfit-to-proceed evidence only,
  wishes are WARN at most. *Scripted author pre-audit*: resolve every anchor
  and recount every count before requesting. The new *behavioural-claim-probes*
  reviewer clause is lens-gated and self-disarmed in this lens (this SKILL.md
  defines no Execute-Before-Specify duty).

## [0.7.0] - 2026-08-28

Spine + overlay delta parked for the next release of this lens (shipped first
in kb; the spine stays byte-identical x3 in the repo while packages publish
independently). In this lens the note is re-attached by the overlay
(`mkt_check.py`, after its own check verdict), because the overlay replaces
the spine's check pipeline entirely.

### Added
- **F-041: `check` notes an unwired or dead session-orientation hook** (one
  informational `[note]` line -- never the exit code, never a `validate` warning,
  so CI is unaffected). `init` wires the hook only at init time; projects
  initialized before F-036 or bootstrapped without `init` were silently unwired.

### Added (F-042, parked with the above)
- Install/update wires the session-orientation hook machine-wide (Claude Code
  with Python; user-level settings; removal is a standing per-target opt-out;
  uninstall surgically removes what it wired). The check note is global-aware
  and reworded in consequence-first user language.

### Added (F-043 port, with the above)
- **The revision sentence.** Updating an existing strategy or campaign doc (the E2 row) is a REWRITE, not an
  append: full re-read, body rewritten to current state -- never an appended
  delta section. Ported from the kb lens's `## Revision` doctrine (kb 1.10.0),
  born from a field post-mortem where delta-append revisions left stale
  sentences standing as printed truth.

## [0.6.0] - 2026-08-26

F-038 — the gated rung: truthful log vocabulary and a mandated ask, no grant memory.

### Fixed
- **A review rung that exists behind a permission policy is no longer logged as
  "unavailable".** The ladder knew two states (the client supports the rung, or not)
  and hard-coded rung 3's reason as "no subagent facility on this client" — so a gated
  facility produced false log rows, and the ladder's own prohibition ("rung 3 is
  illegitimate wherever rung 1 or 2 exists") was unsatisfiable on a gated client: the
  agent could not obey it without asking, and no rule said to ask.

### Added
- **The gated-rung stop.** At a due review gate (design; closure), when the best rung is
  permission-gated (a standing policy — an interactive per-call prompt is NOT this) and
  no ungated rung works (a working one-shot CLI pre-empts the stop; a gated rung 2 joins
  the question instead), the gate stops and asks ONE question in the five-bullet blocking
  form: the gated rung(s) vs the fallback, each higher rung's status, the quoted policy,
  the cost (~130-175k subagent tokens per deep review, measured 2026-08) AND what
  independence last bought, and what stays blocked. **No grant memory**: the answer holds
  while the conversation does; an agent that cannot recall a grant asks again. Unattended
  runs never emit the question — rung 2 is still owed a try, then rung 3 with its reason.
  (Successor to a design CANCELLED at the review cap after grant memory failed three
  ways; rulings r18/r19.)
- **The reason words.** A below-rung-1 row says why the rung(s) above did not run:
  `absent` (the client has no such facility — a claim about the client, never a policy),
  `gated, declined`, `gated, unattended`, `gated, pre-empted` (nothing asked — an
  ungated lower rung ran the review). A rung-1 row owes nothing. For rung 3 this
  re-words an existing duty; for rung 2 it is a new one-word duty, disclosed and
  accepted with the rest.

## [0.5.1] - 2026-08-25

### Fixed
- **The three README front pages did not mention the hook wiring that 1.27.0 added.**
  `init` now changes what every project gets, and the README *is* the npm page, so two
  of the three said nothing about it and the third barely did. Each now describes the
  wiring, the settings.json / settings.local.json split and why it exists, and the
  broken-hook report. `GUIDE_release.md` step 2 already made this a release duty; it was
  skipped in 1.27.0 and this is the catch-up.
- **`publish_all.bat`'s verify block reported the previous version after a successful
  publish — twice.** `--prefer-online` (added in kb 1.4.8) forces revalidation but cannot
  outrun CDN propagation of the `latest` tag in the seconds after publishing, so the
  1.27.0 run printed mkt `0.4.7` when `0.5.0` had in fact landed. The flag alone was the
  wrong fix and the note claiming otherwise is corrected: the block now **polls** each
  package until the registry agrees with the local version, and prints both when it does
  not, so "did it publish?" is answerable from the run instead of a manual `npm view`.

## [0.5.0] - 2026-08-25

F-036 — the orientation hook installs itself.

### Fixed
- **`ENFORCEMENT.md` 4 said "wire it on every project" and nothing ever did.** The
  SessionStart orientation hook was real, tested and fail-open, but installing it was a
  manual step, so it was skipped — and a session that never enters Phase 1 explicitly
  then never meets the guide router at all. Field result: an agent worked a governed
  project without invoking the process. `init` now wires the hook itself.
- **The invariant that looked like it guarded this guarded only prose** — it asserted
  the documentation section exists (`assertIn("## 4. SessionStart hook", t)`) and that
  `orient` runs. It gains a companion asserting the shipped installer actually CALLS the
  writer. Mutation-tested: the first draft asserted the bare symbol and passed on a file
  that imports the writer without invoking it, which is exactly the disabled-installer
  case it exists to catch.

### Fixed (also)
- **ENFORCEMENT 4/2's own worked hook examples named a skill directory that two of
  the three lenses do not install.** kb and mkt both printed
  `.claude/skills/agentic-sdlc/scripts/...`; kb installs under `kb-agentic` and mkt
  under `mkt-agentic-sdlc`, so anyone who copied the snippet got a hook that runs,
  prints `can't open file`, and emits nothing — the wired-and-dead defect this release
  detects, sitting in the instructions that produce it. Four paths corrected, and a new
  invariant derives the expected directory and validator from what the distribution
  actually ships and fails if an example names anything else. Mutation-tested.

### Added
- **A portability rule the doctrine did not have.** The hook command names a validator,
  and where that validator lives decides which settings file may carry it: a repo that
  vendors the validator gets a repo-relative command in the shared, committed
  `.claude/settings.json`; a normal project gets an absolute path, which goes to the
  git-ignored `.claude/settings.local.json` instead — committing it would hand every
  teammate a hook naming a directory they do not have. `init` picks the file and adds
  the local one to `.gitignore`. ENFORCEMENT 4's own worked example showed an absolute
  path and did not mention the distinction; it now does.
- **A wired-but-dead hook is detected and reported instead of counted as done.** Found
  in the field: a repository whose hook named a sibling lens's path, so it ran every
  session, printed `can't open file`, and emitted nothing. A bare "is a hook present?"
  check answers "already wired" to that and makes the silence permanent, so the existing
  command's validator path is checked on disk. Never rewritten — it may be hand-tuned —
  but never passed off as working either.

### Notes
- `init` declines rather than guessing: no Python, skill not installed, a settings file
  that is not valid JSON (never rewritten — a merge would discard what is in it), or a
  skill path containing a double quote. Each case prints the snippet to paste.
- Only Claude Code's hook shape is wired. Codex and Gemini keep the manual snippet: this
  repository has no fixture pinning their schema, and writing a hook file in a shape
  nobody has verified is how the wired-but-dead defect above was born.
- A blocking `PreToolUse` gate would be real enforcement rather than a nudge, and it is
  refused by the Vision's no-ceremony-ratchet Non-Goal. Recorded in the analysis so the
  next person to have the idea finds the ruling instead of re-deriving it.

## [0.4.7] - 2026-08-06

### Fixed
- **Shared-spine sync: the scoped re-review contradicted `dispatch.md` (ACTIVE in this lens).**
  `dispatch.md` said "exactly three review touches per task, never a loop" while `review.md`
  required every review-driven correction to be re-reviewed. Reconciled: the scoped re-review is
  a round inside slot 2 or 3, never a fourth slot. Also in the shared `review.md`: an unproven or
  stale completion claim is now a reviewer finding; a PASS carrying findings is provisional until
  its corrections pass a round; the single log row keeps the round-1 verdict (`FAIL → PASS`).
  Found by the code lens's late design review of F-034.

## [0.4.6] - 2026-08-06

### Changed
- **Shared-spine sync: review-driven corrections + reviewer honesty (ACTIVE in this lens).**
  The shared `review.md` gains the scoped re-review discipline — a fix made in response to a
  finding is unreviewed work and gets a correction-scoped re-review with per-finding verdicts
  before PASS — plus the `CANNOT VERIFY` reporting duty and the no-pre-judging rule. Unlike
  prior spine syncs these are NOT inert here: reviews of marketing artifacts inherit the
  correction discipline directly.

## [0.4.5] - 2026-08-06

### Changed
- **Shared-spine sync: Functional Spec clause (inert in this lens).** The shared
  `review.md` gains the code lens's Functional Spec findings (absence on behavior change,
  Solution-leakage inside the spec, uncovered cases, acceptance criteria without tests).
  The mkt lens defines no `## Functional Spec` template section, so the clause stays inert
  here — spine parity only.

## [0.4.4] - 2026-08-05

### Changed
- **Shared-spine sync: use-case grounding clause (inert in this lens).** The shared `review.md`
  gains the code lens's use-case-grounding finding — a product name in no EXISTS/NEW/METAPHOR
  bucket, or a use-case tracing to no Vision benefit. The mkt lens defines no `## Use Cases`
  template section, so the clause stays inert here — spine parity only.

## [0.4.3] - 2026-08-05

### Changed
- **Shared-spine sync: Interface Contract rename (inert in this lens).** The shared `review.md`
  Interaction Contract clause is renamed to **Interface Contract** and gains the code lens's
  evolved checks (responsibility-level flow, solution-leakage, universal feedback); the
  `interaction_contract` capability key is unchanged. The mkt lens defines no such template
  section, so the clause stays inert here — spine parity only.

## [0.4.2] - 2026-08-05

### Fixed
- **Registry recognition hard-coded to one entry point.** The workstream-registry
  header is written with `entry_script()` (here: `mkt_check.py`) but was recognized
  as "already ours" only by the literal `sdlc_check.py`: a registry this very lens
  generated was treated as legacy and re-checked for conversion blockers on every
  run. Recognition now matches the generated marker for any family entry point.
- **Battery isolation.** The marketing battery failed 13+1 under full unittest
  discovery (and passed module-by-module): `test_merge_safety` built `ai_docs`
  fixtures while the mkt overlay import had flipped the default docs root to
  `mkt_docs`. The battery now pins its docs root in `setUpModule`; full discovery
  is green.

### Changed
- **Shared-spine sync with code 1.22.0 (Interaction Contract, F-032).** The shared
  `review.md` gains the Interaction Contract conformance clause and the shared core
  registers the `interaction_contract` capability — both **inert in this lens**: the
  clause is keyed on the lens whose template defines the section (the code lens),
  mkt claims no such capability, and no mkt workflow gains any new step or artifact.

## [0.4.1] - 2026-08-03

### Added
- **`version:` in every `SKILL.md` frontmatter.** An installed skill carries no
  `package.json` and no `gemini-extension.json` — only doctrine and scripts — so nothing
  in it said which build it was. Answering "is that fix in your copy?" took `npm view`
  plus a shasum comparison; from a user's side it was unanswerable. Now the first thing
  in the operating contract says it.
- **A battery invariant asserting every bump point agrees** (`SKILL.md` ↔ `package.json`
  ↔ `gemini-extension.json`). A hand-maintained version string rots, and this repository
  has the scar: the third bump point was skipped for two whole releases with nothing to
  catch it. The fourth arrives with its guard attached, and `GUIDE_release.md` step 1
  now says FOUR.

## [0.4.0] - 2026-08-03

F-028 — several people on one project. `templates.md` had claimed the workstream
registry was "Parallel-safe by construction" since F-019, and nothing had ever exercised
it. Two workstreams opened from one base conflict **twice in one file**: on the row
insert, and on the file-global `Date:` header. Row-level ownership cannot save a file
that has a file-level field.

### Changed
- **`audit/handoff.md` is now GENERATED** from one `HANDOFF_[unit].md` per open
  workstream, whose frontmatter IS the row. Two writers on two workstreams touch two
  different files, and the `Date:` header is derived — from the newest `updated:` VALUE
  in the sources, never a filesystem timestamp (git does not preserve mtimes, and an
  mtime-derived header would make the file regenerate differently in every fresh clone).
- **`HANDOFF_[unit].md` is now written for every OPEN workstream**, with or without
  volatile state — no file, no row. It still carries the resume logistics, and deleting
  it at closure *is* what removes the row. The DRY boundary against the ANALYSIS Diary
  is restated in the template, because what used to keep narrative out of that file was
  its rarity, and the rarity is gone.
- Project-wide notes move to their own source, `audit/project_notes.md`, so generating
  the registry cannot destroy notes that belong to no workstream.

### Added
- **`validate` errors when the registry disagrees with its sources** — which is what
  turns a merge resolved carelessly from permanent into loud. Resolution is mechanical:
  re-run `index`. The generated view can still conflict; the authored truth does not.
- **`index` refuses to write while anything in the file is unaccounted for**, and names
  it. Converting one row at a time is the state that loses the others, so conversion is
  per project. A project with no sources is untouched and sees no new finding.
- **`init` writes a `.gitattributes` stanza** giving the append-only review log
  `merge=union` — a **built-in** driver, unlike `merge=ours`, which silently does
  nothing until every clone runs `git config` and leaves the file wrong even then.
  Create-only; a user's own `.gitattributes` is never clobbered.
- `scripts/test_merge_safety.py` (shared, ×3): the experiment that found the defect,
  kept as a regression test — two workstreams from one base, merged, with the assertion
  that only the generated view may conflict and that regenerating loses no state. Plus
  the mixed-state, fresh-mtime, ordering, cap and duplicate-id guards, each
  mutation-verified.
- A warning when two files claim the same workstream: the collision this design does
  **not** fix (two people opening the same work under two names) must not pass as two
  ordinary rows.

The mechanism is files and a generator: **it works with no VCS at all.** The
`.gitattributes` stanza is defence in depth — without it the outcome is today's, one
conflict resolved by hand, never a lost row.

### Upgrading
Nothing happens until you convert: with no `HANDOFF_*.md` sources, `index` and
`validate` behave exactly as before. When you convert, convert the whole registry at
once — `index` will tell you what is still unaccounted for.

## 0.3.1 — 2026-08-02

### Fixed
- **The multi-lens routing note announced this skill as the code lens.** `init.js` wrote
  the row for the CURRENT lens as a hardcoded literal copied from the code distribution,
  so a project initialised with `mkt-sdlc-init` listed `agentic-sdlc` twice and never
  named `mkt-agentic-sdlc`. Both the self row and the sibling table are now derived from
  the shared `routing.md` lens table. Found by a cold-agent field test.
- **`FACT` was the way past the evidence rule.** `BENCHMARK` owes a source URL and
  `ASSUMPTION` a range; `FACT` owed nothing, so a researched observation classed FACT
  with source "see research/VOC.md" entered the ledger unsourced. `mkt_check.py` now
  errors on a FACT with no source, or one pointing at a document of the engagement,
  while exempting a cell that names the client as origin. `research.md` states the two
  legal origins.
- `review.md` (shared spine): a review verdict travels as the reviewer's final output.

## 0.3.0 — 2026-08-01

- **One shared core, three lenses.** This skill is now built from the family's spine
  instead of a copy of it: triage, the Vision gate, the review gates, the guide router,
  question discipline and the validator core are byte-identical with
  `@antoneeo/agentic-sdlc-skill` and `@antoneeo/kb-agentic-skill`, and a drift guard
  verifies it on every build. `routing.md` decides which lens owns a unit of work when
  more than one is installed.
- `mkt_check.py` forwards every spine subcommand it does not intercept by iterating the
  spine's parser — the hand-copied command tuple used to drop `migrate` while `SKILL.md`
  documented it.

## 0.2.1 — 2026-07-09

- **Install DX fix**: README + the generated project protocol pointer no longer present `mkt-sdlc-install-skill` as a required second step. `npm i -g` alone installs the skill (the `postinstall` runs the installer); the manual command is documented as a fallback via `npx mkt-sdlc-install-skill` for setups that block install scripts, with an explicit note that the bare command is only on PATH after a global install. Prevents the "command not recognized" error after a local `npm i`.

## 0.2.0 — 2026-07-09 (v1.0 hardening)

- **Deterministic doctrine gate**: `scripts/test_skill_invariants.py` asserts the load-bearing invariants (three guarantees, review red-flags R1/R11b/R15, elicitation rules, research URL rule, parseable template tokens, sales-led funnel guidance, support-file wiring). Fails on a real regression.
- **Opt-in behavioral eval layer**: `evals/run_behavioral.py` (zero-LLM driver) + 6 scenarios (triage/escalation, owned-facts elicitation, no-number-without-ledger, swap-test enforced, low-cost-trap flagged, no-guaranteed-success). Mirrors the sibling skill.
- **Contrast validation (B2B sales-led)**: second synthetic eval on a business unlike the first — the Vision Alignment / amendment discipline caught and held a deliberate vision-divergence (self-serve tier) instead of absorbing it.
- **Calibration from the contrast run**: sales-led/B2B funnel guidance (funnel output = qualified demos not closed customers; separate pipeline build-up table; closed-won lag) in `frameworks.md` + `templates.md`; B2B firmographic-ICP + buying-committee variant in `templates.md`.
- ENFORCEMENT.md §5/§6 updated to run both deterministic batteries + the behavioral layer.

## 0.1.0 — 2026-07-09

Initial release.

- Operating contract `SKILL.md`: Marketing Values, Rule Zero engagement triage (E1/E2/E3/Spike), dual operating modes (Standalone `mkt_docs/`, Hybrid devPNT), E3 nine-phase SOSTAC workflow with user gates, adversarial review gates and mechanical validation.
- Support files: `frameworks.md` (framework selection guide), `elicitation.md` (question waves, only-facts-you-own rule), `research.md` (research playbook + evidence ledger discipline), `templates.md` (all artifact templates), `review.md` (CMO review discipline + marketing red flags), `ENFORCEMENT.md`.
- Mechanical validator `scripts/mkt_check.py`: `check`, `validate`, `ledger`, `budget`, `funnel`, `trace`, `index`.
- npm packaging: `mkt-sdlc-init` (project scaffold), `mkt-sdlc-install-skill` (multi-client skill install: Claude Code, Gemini CLI, Codex, Google Antigravity).

## [0.3.0] - 2026-08-01

### One shared core, three lenses

This release is the consolidation: `agentic-sdlc` (code), `kb-agentic` (knowledge)
and `mkt-agentic-sdlc` (marketing) are now built from ONE spine instead of being
copies of one another. They can be installed side by side, they share a single
`ai_docs/` tree, and the agent has a stated test for which one governs a given
piece of work.

**Nothing changes for an existing project.** No `default_domain` line resolves to
`code`; no `domain:` field means no new column and no new check; the router is
never read unless a sibling lens is installed, and never at all on a trivial task.
A frozen corpus plus a recorded transcript of every command and exit code
(`test_golden_regression.py`) is what makes that a checkable claim rather than a
promise.

### Added
- `routing.md` — the domain router: which lens owns this unit of work. Read only
  when a sibling lens is installed; fails open to the loaded lens.
- Optional `domain:` and `checks:` on an artifact, `default_domain:` in the docs
  root README. All optional; a single-domain project writes none of them.
- **Portable checks**: a document owned by one domain can import another domain's
  checks by name. Imported checks may only ADD findings, never relax what the
  owning domain requires.
- `migrate` — relocate a documentation root. Dry run by default, refuses a dirty
  git tree, refuses to overwrite, never deletes, and leaves user-authored protocol
  pointers untouched (they are reported instead).
- `--docs-dir` / `AGENTIC_SDLC_DOCS_DIR`: the documentation root is resolved
  (explicit flag > env > nearest recognized root > `ai_docs`). Two roots side by
  side refuse rather than half-validate.
- The drift guard (`shared_files.py`, `test_drift.py`): the spine is authored once
  and copied verbatim, and a forgotten copy now fails a test instead of reaching a
  user.

### Changed
- The validator ships as **two files**: `sdlc_core.py` (the shared spine) and the
  domain entry point. If you copied it into CI, copy both — `ENFORCEMENT.md` §2 has
  the recipe, and a half copy fails loudly at import rather than passing green.
- A review now reports a **restated fact** as a finding: every governance slot has
  one owning document, and the fix is a citation, not a better copy.
- The invariant battery is shared across distributions and reads a per-distribution
  PROFILE. Spine capabilities cannot be dropped by editing a profile; optional
  overlays are declared in one line.

