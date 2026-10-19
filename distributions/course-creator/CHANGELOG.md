# Changelog

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
