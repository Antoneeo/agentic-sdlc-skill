# Changelog

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
