# F-089 replay cases — chatPNT M155 under `coordination.md`

Each case is a situation of several sessions working on one repository (chatPNT,
`D:\SoftwareDev\chatPNT`), one of them coordinating. Sources: the coordinating session's
reading of `coordination.md` 1.51.0 (`REQUEST_parallel_sessions_gaps.md` R2), chatPNT's
`ai_docs/audit/requests/REQUEST_ui_uniform_style.md` (cited `UUS#R<n>`) and its git
history. Quotations are data. In every case the owner has named the coordinating session
in a request-record entry, so the coordination rules apply.

The replay question, the same for every case: **under the doctrine text given, does a rule
tell the session in the case what to do — allow it, forbid it, or route it — or is the
situation left to the session's guess?** Answer FLAGGED with the line that decides it (and
say whether it allows, forbids or routes), or NOT FLAGGED.

## G1 — a session that writes only documents, in the shared checkout
The session preparing the pre-release unit writes only design documents of its own unit
(its ANALYSIS, its HANDOFF, its request record, coverage notes). It works in the checkout
the coordinator and the code-writing session also use; the owner alone runs git. Opening a
worktree would give the owner one more branch to merge for a unit with no code.

## G2 — review-log rows from several sessions
Three sessions each append rows to `ai_docs/audit/reviews/REVIEW_LOG.md` for their own
reviews. Commit b8755e76 (wave 5h) carries four new rows. The rows are not numbered; each
names its document and date.

## G3 — devPNT's store in a commit
Commit b8755e76 also carries `.devpnt/agent/agent_knowledge.db` and `.devpnt/plans/plans.db`:
devPNT's server writes them (plans and governed documents) as sessions work through it, so
one commit can hold several units' changes in them. The coordinator writes the commit map for that commit and
must put the two files in a section.

## G4 — translation catalogs
The same commit carries `messages.pot` and `translations/{en,it}/LC_MESSAGES/messages.po`
(about 315 lines each), rewritten by the extraction tool from the code the code-writing
session changed. A session writing only documents notices a wrong Italian string
(UUS#R170: «La traduzione italiana sbagliata di "Coming Soon"») and is about to fix it in
`translations/it/LC_MESSAGES/messages.po` while the code-writing session holds its lease.

## G5 — a session started by the coordinator
The coordinating session started further sessions in a chain (`m155-plan` → `2c` →
`onda3`). The newest one, given the coordinator's summary as its brief, begins appending to
the shared record and writing `audit/leases.md`. No owner entry names it.

## G6 — the coordinator after compaction
The coordinating session's context is compacted between two units (UUS#R60, the owner: «dimmelo
che faccio una compattazione prima di iniziare 2b»); it resumes from a summary. Its
summary says the container lease is free; `audit/leases.md` ends with a `take` for another
session written after the summary was made.

## G7 — the owner names a new coordinator
The owner names another session coordinator in a new request-record entry. The previous
coordinator is still running and, unaware, appends a `release` line to `audit/leases.md`
for a part that asked it.

## G9 — closing a documents-only unit in the shared checkout
The documents-only session of G1 reaches its unit's closure. Its closure steps include
regenerating the indexes (`index`), writing the merge brief from `review-map`, and `mark`.
The code-writing session and the coordinator are working in the same checkout at that
moment. Who runs those steps, and where?

## G8 (control) — a part's own record
A part on an L3 unit appends an owner answer to its own request record before acting on
it. Expected: covered by the current text (one writer per record).
