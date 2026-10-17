# Changelog

## [Unreleased - 0.1.0-beta.5]

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
