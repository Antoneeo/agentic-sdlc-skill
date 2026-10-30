# Changelog

## [Unreleased]

### Changed
- After the design review's final PASS, an L3 unit stops: the agent presents a short summary of the course design and asks the owner whether to proceed; production starts only after a yes, recorded in the request record under a label that begins `design approved`. Unattended, the unit is `BLOCKED on the user`. The L3 row of the triage table reads "design review, owner approval, production". The rule is in the shared `review.md`; `SKILL.md` and `templates.md` point at it (F-087).
- The shared validator: `validate` notes an L3 ANALYSIS in implementation, started on or after 2026-10-31, whose request record holds no entry whose label begins `design approved`. It is a `[note]`: `--strict` exits as before. The `gate` refusal message adds that at L3 the ANALYSIS goes `IN_PROGRESS` only after the owner's design approval; its exit codes are unchanged (F-087).

## [0.1.0-beta.15] - 2026-10-30

### What's new

**An instructor-led course ships with everything its instructor needs.** A course taught by an instructor now comes with `INSTRUCTOR_GUIDE.md`. It tells the instructor what to prepare, the schedule, what not to show the learners, what to do when a live step goes wrong, and what to clean up afterwards. It also lists every material the delivery needs. The course check confirms that each listed material exists, so a missing file shows up before the session instead of during it.

**Feedback is attributed to the right version.** If a slide or unit names the course with a version different from the one the course declares (say "version 1.0" in a course at 1.2), the check names the section and the version it found. Feedback that quotes the version then reaches the version it is about.

**Demo projects stay out of the course's memory.** Materials can be listed anywhere in the project, so demo projects and the generated deck are listed where they are. If a listed demo project with its own repository sits inside `ai_docs/`, the check warns you: its documents would otherwise turn up in project searches as if they were the course's.

**From 0.1.0-beta.14, published without notes:**
- **The process checks can no longer be bypassed by accident.** Quoting a work level inside a sentence no longer counts as declaring it, and protected parts of the project stay protected when the agent changes folder.
- **You know what the project memory has not read yet.** The agent can tell how much of the project it has never examined.

#### What to do

**1. Update (everyone).** The changes arrive only with the update.
1. Run `npm install -g @antoneeo/course-creator@latest`, then `course-creator-install-skill`.
2. Close and reopen your agent sessions: the new version loads only at startup.

To check: `npm ls -g @antoneeo/course-creator` shows 0.1.0-beta.15.

**2. Write the instructor guide (instructor-led courses, and courses that already have one).**
- **This concerns you if** a course's content file (`SLIDE_CONTENT.md` or `COURSE_CONTENT.md`) declares `Delivery mode: instructor-led`: after the update, `check` reports `instructor-led course needs INSTRUCTOR_GUIDE.md before delivery`. It also concerns any course with a `Content contract` that already has an `INSTRUCTOR_GUIDE.md`, which is now checked. Courses that declare no `Content contract` are not affected.
- **Why:** the check refuses an instructor-led course without the guide, and refuses a guide written by hand in another shape, so the course fails `check` until the guide follows the template.
- **Steps.** The commands below use `<skill_dir>`, the folder where `course-creator-install-skill` placed the skill; you can also ask the agent to run them.
  1. Ask the agent: "write INSTRUCTOR_GUIDE.md for this course from the template in templates.md".
  2. Make sure `## Materials` lists every file and folder the delivery needs, with paths from the project root (for example `demo/TH-01/`). A folder path ends with `/`; a file path does not.
  3. If a listed demo project with its own `.git` or `ai_docs/` is inside `ai_docs/`, the check warns you. Move it outside, for example to `demo/` at the project root. Then update its path in `## Materials`, in any fallback cell and in any `ai_docs/...` path the guide cites. Finally run `python <skill_dir>/scripts/sdlc_check.py index --root .`, which regenerates the project memory without the demo files.
  4. If `check` reports `mentions course version X; Course version is Y`, find the line in the named section that names the course with version X, and correct it.
- **To check:** `python <skill_dir>/scripts/sdlc_check.py course <course-folder> --root .` reports `0 error(s)` for that course, and no warning about the guide. `<course-folder>` is the course's folder name under `ai_docs/solutions/courses/`.

**3. Protected folders in a repository with several `ai_docs/` (only if you use them; from 0.1.0-beta.14).**
- **This concerns you if** your agent settings contain `gate --hook --protected` and the repository has more than one `ai_docs/` folder, for example a package with its own.
- **Why:** protected paths are now read from the `ai_docs/` nearest to the edited file. A path written from the repository root, such as `packages/api/src/auth`, no longer matches the files inside `packages/api`, so the agent could change them without an analysis.
- **Steps:** rewrite those paths from the package: `packages/api/src/auth` becomes `src/auth`. Note that `src/auth` then protects the folder with that name in every project that has its own `ai_docs/`.
- **To check:** in a session with no open analysis, ask the agent for a small change to a protected file. It must be refused.

### Added
- Instructor-led courses ship `INSTRUCTOR_GUIDE.md` (`templates.md`, F-086): what to prepare, the schedule, the reserved material (every solution unit by ID), what to do when a live step deviates and which fallback to use, what to clean up afterwards, and the list of every material the delivery needs with who may see it. `course_check` refuses a course whose content declares `Delivery mode: instructor-led` without the guide, and checks a guide wherever one exists in a course that declares a content contract: header equal to `COURSE_PLAN`, all six sections, every listed material present in the project, every cited `ai_docs/` path in the course folder or under a listed material, solution units reserved, deviation risks defined in `P-TM.md`, and scheduled modules present in `COURSE_PLAN` (`-` for a break or closing). A material may be anywhere in the project, so demo projects and the generated deck can be listed where they are. A listed folder inside `ai_docs/` that holds its own repository is warned, because project memory would index its documents as the course's. **An existing instructor-led course fails `check` until its guide is written to the template; a guide written by hand in another shape is refused too.** Courses without a declared content contract are unaffected.
- `course_check` refuses, in a course that declares a content contract (self-study or instructor-led), a line that names the course (the word course/corso, the folder slug or the full title) and mentions a dotted version other than the declared `Course version`, so feedback that quotes the version reaches the right one. A tool's version on a line that does not name the course, and a bare number such as `versione 2`, are not checked.

### Changed
- The package's npm page (its README) gains a "What's new in <version>" section right after the introduction, written for the people who install the package and linking the full CHANGELOG. It appears from the first version that carries one; each version's notes are the `### What's new` at the top of its CHANGELOG section (F-070).

## [0.1.0-beta.14] - 2026-10-27

### Added
- Shared knowledge layer (F-084, kb CHANGELOG): `inventory <path>` and orient's upper bound of never-examined project files reach this lens; `validate`/`check` refuse a malformed `audit/INVENTORY_exclusions.md` row and the new `DECLARED`/`DIVERGES` claim rules; the docs site renders them. `sdlc_core.skip_dir` is extracted from `iter_files`, behaviour unchanged.
- `constraints --unit <id>` and `constraints --file <path>` (shared core): the constraints an ANALYSIS states in extractable form, each with its line, ending with the sections they could not extract.
- `benefit` and the docs site recognize a REVIEW_LOG row with tier `post-merge` (written by the code lens: the owner's report of a wrong behaviour in a merged change): `benefit` keeps it out of every review figure, the docs site shows it as "defect reported after merge". `review.md`: a reviewer derives callers and behaviours before comparing with the constraint view.
- `guides.md`: a code guide may carry a `## Preservation constraints` section copied from a closed unit; it survives regeneration. Nothing else changes in this lens: `validate` adds no note.

### Fixed
- Shared claim checks (`check`): a `RULING` row on a note that names a foreign origin (`imported_from:`) is refused — relabelling an imported row is not ratifying it; the message for a row superseded by an `IMPORTED` one names the ratification act (F-083).
- Guide-verdict check (`verdict --hook`, shared core): a level quoted inside a sentence (`Level: L1` in prose) no longer counts as a declaration: only a line that opens with the level word does, the rule the constraint recall already uses (level 1 alone, `L1` or `E1`; levels 2 and 3 with `router` on the same line). The check now judges the project, and its docs-root name, that holds the edited file, not the one around the session's working directory; after a `cd` out of the project it let every edit through. A router verdict follows the same rule: only a line that opens with `router` or declares the level with it counts, never `router: no match` quoted in a sentence; `Level: Spike · router: …` and markdown openers (`##`, `1.`, `•`) count. A quote that itself opens a line (blockquote, code fence) still counts. The protected-path gate (`gate --hook`, `gate --file`) also judges the edited file's project, falls back to the session's project when no docs root sits above the file, and stays silent instead of exiting with an error when two docs roots sit side by side. Its `--protected` prefixes are relative to the nearest docs root above the edited file: with nested docs roots (a monorepo package with its own `ai_docs/`, or a docs folder inside a protected path) rewrite them relative to that root, or the path is no longer protected.

## [0.1.0-beta.13] - 2026-10-23

### Changed
- `guides.md`: a document snapshot is verbatim except for credentials and personal or confidential data the guide does not need, which become `[REDACTED: <kind>]` before the snapshot is written; the guide lists the kinds in `redacted_at_intake:`.
- The session-start orientation (`orient`) now fits under Claude Code's 10,000-character hook limit, even in a project with many documents. Above that limit Claude Code saves the output to a file and shows the agent only the first 2,000 characters, so the guide router never reached the agent. The output is now at most 9,500 characters, including the knowledge layer's lines, and in this order: the triage line, the guide router (one line per guide), the workstream registry (one line per workstream, then the project-wide notes), then the reading guide (README). The manifest (INDEX) and the full files are listed as pointers. A section that does not fit is cut at a line, with a pointer to its file.
- The per-turn `remind` line also tells the agent, above L1 and when sibling lenses are installed, to choose the lens with `routing.md` and declare it. The line's limit rises from 500 to 600 characters (`vision/rulings.md` r32).
- `docs_site.py` adds `.docs-site/` to the project's `.gitignore` on its first run in a git repository, so the site's copy of the documents is not committed. It used to print a note only. An entry already in the file is never changed; when git still does not ignore the folder, the note is printed as before.
- `SKILL.md` names the docs site in the words users use ("docs site", "minisito", "documentation site", "project site"), so a request for it runs `docs_site.py` instead of building a page by hand.

### Added
- `check` refuses, in every lens, a line shaped like a credential (a password, token or key with a real value, a private-key header, a password in a URL, a bearer token) in a `corpus/given/` file or in the snapshot of a `source_kind: document` guide. The message names the file, the lines and the kinds, never the value. A human clears a false positive with `credential_scan: reviewed — <reason>` (in the sidecar, or in the guide). A project whose stored sources already hold such a line fails `check` until each is redacted or reviewed (`vision/rulings.md` r35a).
- `adopt`: a dry run listing the document guides that rest on `.sources/` snapshots and what moving each into `corpus/given/` involves. It writes nothing.
- `check` warns when the same text is stored both as a guide snapshot and as a corpus artifact.
- `check` also warns on a `corpus/given/` file with no sidecar, accepts a withdrawn artifact's tombstone sidecar (no bytes, no digest), and, when an `original_path:` is a URI, names `original_ref:` for non-local identifiers. A password inside a URL in that warning is masked.
- Shared claim checks (`check`): a claim's `about` cell may hold several relations separated by `; `, and one reserved predicate, `not-yet-honored-by -> ANALYSIS_<name>`, marks a specification claim the code does not yet honor. `check` refuses the marker when that analysis is missing from `solutions/` or cites neither the claim id nor the id of a row the claim succeeds. `export` drops the markers and says so in one line. Nothing lists or counts claims by the marker (`vision/rulings.md` r33). `memory.md`: a marked claim is cited as not yet true of the code, naming its analysis.
- Shared claim checks (`check`): the `not-yet-honored-by` marker now works in Hybrid projects (devPNT present). It may name `SHADOW_<doc_key>`; `check` reads the newest `solutions/SHADOW_<doc_key>_vX.Y.md` (versions compared number by number), which must exist and cite the claim id or a predecessor's. A missing shadow is an error that says to export it, and names a file of that key whose name lacks the `_vX.Y` suffix. `check` behaves the same with or without `--hybrid`; export drops both target forms (`vision/rulings.md` r36). New shared helper `sdlc_core.newest_shadow`. `memory.md`: a marked claim is cited naming its target.
- `verdict --hook` (PreToolUse): refuses an edit when the session declared no guide-router verdict, or never read a guide its verdict names; silent in projects without guides and whenever it cannot tell. Not wired by this package (`ENFORCEMENT.md` §3).
- `orient` adds a note when one client runs it from two settings entries, which means each session gets the orientation twice. Claude Code and Codex are counted separately, an identical command counts once, and an entry whose validator is gone is not counted.
- `orient` adds a line naming the sibling lenses installed beside the skill or in the user's Claude skills directory, and says to choose the lens with `routing.md`. The family list is read from `routing.md` §0, as the installer does.
- `routing.md` §2 gains worked verdicts for four mixed requests: an interface spec written for another team, the requirements another team must build, a guide whose source spec changed, and code that diverges from a supplied spec.
- The shared validator adds an advisory for a code-lens (`domain: code`) L3 analysis, started on or after 2026-10-24, that lacks a filled `## Guide check` section. Analyses of this lens are not checked.

## [0.1.0-beta.12] - 2026-10-19

Includes everything listed under [0.1.0-beta.11], which was tagged but never published to npm.

### Added
- `mark <paths> --note "<what was done>"` writes a dated entry `**YYYY-MM-DD — <what was done>.**` at the top of `audit/project_notes.md`. A release or work outside an open unit used to leave no dated event, because the date had to be copied there by hand. Without `--note`, and with no open unit, `mark` says so.
- `validate`: an advisory for a dated entry in `project_notes.md` whose bold does not pair; the chronology then showed the label running into the body.
- Docs site chronology: a Diary entry's label carries its unit id ("F-074 — closed"), so it reads on its own.
- `stale` no longer counts files inside the docs root (`ai_docs/`, `mkt_docs/`) as drift of any area, and `mark` refuses to record it: `validate` already checks the docs root, and every document edit used to leave `check` NOT CLEAN until a redundant re-mark.

## [0.1.0-beta.11] - 2026-10-19

### Added
- Docs site: `docs_site.py --zip <file>` also writes the site as one .zip to share; unzipped, `index.html` opens on any system. A zip made by hand with Windows PowerShell 5.1 `Compress-Archive` stores `data\core.js`, and on Linux or macOS the page then finds no data; `--zip` always writes `/` names. It refuses a target inside the docs root or the site folder. The `SKILL.md` line names it.

## [0.1.0-beta.10] - 2026-10-19

Includes everything listed under [0.1.0-beta.9], which was tagged but never published to npm.

### Added
- Docs site: each card in Open work and each feature in Features links its merge review and its end-to-end test script, when they exist. They were reachable only inside a feature's chain page; who merges looks in Open work while the work is open, who tests looks in Features after it closed.

### Changed
- Docs site: Features are listed newest first by their declared start date; those without a start date come last.

## [0.1.0-beta.9] - 2026-10-18

### Changed
- F-071: a review weighs effort against what the owner asked for. In a design review, each outcome the owner named (the opening request, any entry widening scope, an approved north star) is a row of the conformance statement, saying where the design serves it and what share of the design goes to it; an outcome no section serves, or one served by a minor share while a secondary concern takes the bulk, is a finding. `review.md` §Reviewing.
- F-071: a review runs where something is left to judge. At level 2 the closure review is due only on a security-sensitive area the lens's Rule Zero names, or at the owner's request; otherwise it does not run and logs no row. After a design or closure PASS, a delta made only of version and release metadata, regenerated indexes and audit-mark records, tool-verified copies of a shared file, and CHANGELOG lines adding no claim is not reviewed: its own check runs and a `NOT DUE` row records it. README or overview prose, an E2E script, a rulings row, doctrine, behaviour, tests and any correction of a review finding are still reviewed. `review.md` §When a review is due.
- `sdlc_check.py benefit` counts `NOT DUE` rows apart, in no review or findings figure.

## [0.1.0-beta.8] - 2026-10-18

### Fixed
- F-072 (field run): the `SKILL.md` line that announces the docs site now reads `scripts/docs_site.py --root <project> --open` and says to use it to show the project state. Asked for the state, an agent had opened the site in its own client pane, where it renders blank, and improvised a local server; `--open` opens it in the user's browser, where it works offline.

## [0.1.0-beta.7] - 2026-10-18

### Added
- F-074: every Vision is born from an owner interview. Before any Vision text is written (project, feature, the course Vision, and the devPNT M-VISION), the agent asks the owner six questions in order, re-asking an answer that has the wrong form: the problem as one concrete case, the benefit as a result for someone, the actors including who takes the initiative, a success signal with its starting value, the boundaries, and the known constraints with where each comes from. Then the owner approves a one- or two-sentence north star in their own words; without it no Vision is written, not even a draft. The blind check still tests that the rules hold; the approved north star shows they are the owner's. `vision.md` §The owner interview.

### Changed
- `elicitation.md`: the skip path never covers a Vision; the interview is a planned occasion like the round.
- Bootstrap no longer writes a Vision reconstructed by the agent: the installer seeds `ai_docs/vision/project_vision.md` as a stub awaiting the interview (an existing file is never overwritten).
- A Non-Goal now bounds scope. It rejects a proposal that pursues what it names; it is not a ban on behaviour that already exists and creates no obligation. A behaviour that must never happen is an Invariant or a constraint with its source.
- The course Vision template gains North Star and Problem, learners with the initiative, signals with starting values, Non-Goals as scope, and the source of every constraint.

## [0.1.0-beta.6] - 2026-10-18

### Added
- F-072: `scripts/docs_site.py --root <project>` writes a static, read-only website of what the agent reads in the project: what it is (reading guide, Vision, rules, documents), its open work with each next step verbatim, its courses, and — with a knowledge base — a map of topics, the facts with the exact passage each comes from, what an inferred fact rests on, and the source documents. It opens from disk with the network off, writes outside the docs root, changes nothing in it, and selects, ranks or recommends nothing. Each analysis opens with the chain the agent works through — Vision, use cases, flows and interfaces, risks, solution study, design and tests, merge brief and E2E script, Diary — the Vision's North Star is shown above the home page, and the guides have a page of their own: the guide router, the operative guides with when to read each, and the code-comprehension guides. The chronology lists the dated events the documents declare (Diary entries, spike outcomes, request-record entries, review-log rows, decision records, dated project notes, notes and sources received), most recent first, read with the same F-073 readers `validate` uses. Shared by the four packages (generator, page and battery are byte-identical spine files).

## [0.1.0-beta.5] - 2026-10-17

### Changed
- F-073: one written form for a dated entry, `**YYYY-MM-DD — label.**`, is taught for Diary entries, spike outcomes and project notes that record an event, and shared readers (`entry_openers`, `request_entries`, `adr_date`, `frontmatter_date`) let a chronology list those events the same way the validator reads them. Three new advisories, which never fail a build, not even `--strict`: undated text in the Diary of an L3 analysis started on or after 2026-10-18; a HANDOFF `next:` longer than 240 characters on an L3 file updated on or after that date (`next:` now holds only the next step, and the state of the work goes to the Diary); and, in `check` only, an open L3 unit whose id another branch or tag uses for a different analysis (one `git grep` over local refs, silent without git). The doctrine now says to choose a new unit's id after fetching, and that a session sharing a checkout with another session works in its own git worktree.
- The package publishes on npm `latest`, like the other three: `npm i @antoneeo/course-creator` installs the newest version with no separate promotion. The version keeps its `-beta.N` suffix and the README its experimental statement; the `beta` dist-tag no longer advances.

## [0.1.0-beta.4] - 2026-10-17

### Changed
- F-068 (shared doctrine with kb-agentic): the supersession cascade runs at the unit's closure, once for every supersession since the last one, instead of at each supersession.
- F1: closing the last open workstream now empties the generated registry `audit/handoff.md` instead of leaving its stale row behind: with zero `HANDOFF_*.md` sources `index` rewrites it empty (keeping `project_notes.md`), and `validate` reports a generated registry that still has rows but no sources as an error.
- F-069: `graph`, `check`, `stale` and the session-start count are faster on a mature knowledge base, with byte-identical output. Citations of superseded claim ids are found with one pass per living document instead of one scan per (document, id) pair, and one check run reads and resolves each cited extraction once instead of once per claim row. On a synthetic ledger of 2183 rows and 1000 living documents, `graph` drops from 14 s to 4 s. No new flag.

## [0.1.0-beta.3] - 2026-10-13

### Changed
- F-067: every L3 unit now keeps a verbatim, append-only request record `audit/requests/REQUEST_course_<slug>.md`, started before the Vision Gate: the owner's opening words and every later statement that settles something (answers, approvals, costs, rulings). Artifacts cite its entries instead of paraphrasing; the shared `review.md` asks for the record and makes an owner statement with no resolving entry a finding. Secrets, personal data and confidential third-party or employer information are redacted.

## [0.1.0-beta.2] - 2026-10-08

### Changed
- F-065: every agent review request opens with a fixed REVIEW MANDATE block copied verbatim, which carries `review.md` itself to the reviewer in Standalone and Hybrid alike; §Requesting now lists every input its clauses check (Functional Spec, Interface Contract, Component Map, audit plan, probe harness, closure test evidence). devPNT performs no review: in Hybrid an agent review with verdict PASS precedes every proposal to devPNT, where the human reviews; after the round cap only the user's explicit decision sends an artifact on, with open findings attached.

### Fixed
- Shared memory catalog hashes normalize CRLF/LF, avoiding checkout-dependent index mismatches.
- The validator prints its final check verdict after memory, topic and corpus checks, so their errors count in the summary.

## [0.1.0-beta.1] - 2026-10-02

- First public beta on the beta channel. Diagnostic simulation does not establish human learning; interfaces and method may change.

- A course that teaches work with a tool or agent now trains and checks the person's acts (request, judging the tool's output, reserved decisions), not the operations the tool performs. `learning_design.md` records who performs each act, reads the split from the course Vision and adds a `Learner's act` acceptance row; simulation criteria give no credit for producing the tool's outputs.

### Initial beta contents (previously prepared as 0.1.0, never published)

- Add the course lens with learner profiles, concept prerequisites, sourced explanations, independent diagnostic simulation and real feedback workflow.
- Add course structural validation and the fourth shared spine copy.
- Share `ai_docs/` indexes with the code, knowledge and marketing lenses.
- Validate concept knowledge and prerequisite teaching separately for each declared learner profile; reject undefined profiles.
- Ship a Standalone source-conflict escalation procedure and document the complete four-file CI validator bundle.
