---
id: F-089
feature: Gaps in coordinating parallel sessions — the shared checkout, shared files, coordinator handover
status: COMPLETED
level: L3
start_date: 2026-11-01
end_date: 2026-11-01
---
# Feature Analysis: gaps in coordinating parallel sessions

**For whom**: the independent design reviewer, then the owner. **To do what**: approve or
reject the three rules below, ruling r42 and their cost before any doctrine is written.
**Answers**: which situations the coordinating session of chatPNT M155 found
`coordination.md` 1.51.0 silent on or wrong about, and the smallest rule for each. **Does
not answer**: which work runs next (Non-Goal 1, ruling r3); how the client starts or
compacts sessions.

Follow-up of F-088 (`ANALYSIS_parallel_sessions.md`, COMPLETED, released 1.51.0). Owner
statements: `audit/requests/REQUEST_parallel_sessions_gaps.md` R1–R5. Evidence:
`harness_parallel_sessions_gaps/` — `cases.md` (G1–G7, G9 and a control G8), `replay.md`,
`results_old_text.md` (baseline).

## Objective

The coordinating session of chatPNT M155 read `coordination.md` 1.51.0 at the owner's
request and confirmed §1–§6 (R2, relayed: its words, not the owner's). Its point 1 — the
rules start only when an owner entry names it — is the text working as designed: the
owner's act. Its points 2–4 are gaps:

- **The shared checkout (point 2, G1, G9).** Outside the code-writer lease every session
  keeps its own worktree (`coordination.md`:70-72, `SKILL.md`:211). A part whose unit
  writes no code then gives the owner, who alone runs git, one branch to merge per unit;
  the owner chose an exception with constraints (R4). The text also never says where the
  coordinator works, though the shared files it keeps live where parts read them, and
  a documents-only part could not run its own closure steps there (`index`, `review-map`,
  `mark` — `SKILL.md`:232, :242).
- **Shared files beyond request records (point 3, G2–G4).** §1 gives each request record
  one writer and says nothing of the review log in one checkout, of an external tool's
  store tracked in git (devPNT's `.devpnt/`), or of translation catalogs. Commit b8755e76
  carries all three. The commit map has no stated home for the devPNT store, and
  `Regenerated` errors for a file the validator does not write (`sdlc_check.py`:368-370).
- **Coordinator continuity and handover (point 4, G5–G7).** The text says who coordinates
  — the named session — but not whether a compacted session still is it, whether a
  session it starts inherits the role, or how a new naming takes effect.

## Feature Vision

Serves the same Actor and Goal as F-088: the team lead — «keep several agents … aligned to
one intent. Good UX = one process, one source of truth» (`project_vision.md` §Actors,
APPROVED) — and «keep understanding durable across sessions». One ANALYSIS, no feature
Vision.

**Rulings ledger.** r40 admits «the code-writer lease as the **one** exception to each
session in its own worktree» and «one `take` and one `release` line per use». FS1 adds two
sessions to the shared checkout and FS3 a `coordinator` line: scope growth of an admitted
capability, so a new row **r42** (ADMIT), owner basis at design approval. r42 supersedes
r40's «one exception» clause and nothing else of it; r40's basis cell gains «clause «one
exception» extended by r42, <date>» (the ledger's restatement form, r2), so a reader of r40
alone meets no contradiction.
Distinction lines against r3 (by whom):
- *Who works in the shared checkout* (FS1): answers «which sessions may write in the
  checkout the runtime mounts, and what», never «who must do which unit». It names kinds
  of session by the files they write, never a unit or an order.
- *The `coordinator` line* (FS3): answers «which session holds the coordinating role now,
  as the owner named it», never which unit or by whom work is done; it cites the owner's
  entry and keeps no queue.
- *Routing through the coordinator* (FS1, FS2): a change to a file the session may not
  write is sent to the session that writes it; the coordinator decides nothing about it it
  was not delegated (`coordination.md` §3, unchanged).

Out of scope: a coordinator the skill elects (F-088 R8 stands); a tool lock; sibling
lenses (`coordination.md` is code-lens only, F-088 R9); any other file several units
change (ordinary merge territory, each in its own worktree — no rule).

Success signals. Baseline, measured (`results_old_text.md`): G1 forbidden; G2 covered
across branches and in the commit map but not for appends in one checkout; G3, G4, G6,
G7 NOT FLAGGED; G5 forbidden only by implication; G8 FLAGGED. G9 is replayed on both texts
with the new-text run. Target on the new text: G1 allowed under FS1; G2–G7 and G9 FLAGGED
with the route FS1–FS3 give, by an explicit line; G8 unchanged.

## Use Cases / User Needs

- **UC1 (Team lead / owner)** — run documents-only units in the checkout already in use, so
  that only units with code cost a branch to merge. *Benefit: one process, less ceremony.*
- **UC2 (Team lead / owner)** — know, for every file several sessions touch, who writes it
  and where it goes in the commit map. *Benefit: one source of truth at merge.*
- **UC3 (Team lead / owner)** — keep one coordinator across compactions and chains of
  sessions, and change it with one sentence. *Benefit: durable understanding across
  sessions.*

Grounding: worktree, request record, review log, `merge=union` stanza (`scripts/init.js`),
commit map, `index`, `review-map`, `mark`, code-writer lease, devPNT store — EXISTS. Shared
checkout as a named place, documents-only part, `coordinator` line — NEW, declared here.

## Functional Spec

**FS1 — the shared checkout.** Under coordination the *shared checkout* is the one the
runtime mounts (with no runtime, the one the owner names); the live `leases.md` and shared
record are the ones in it. Three kinds of session work in it; every other session keeps
its own worktree. The bans of `SKILL.md` Phase 4 (no branch switch, stash, reset) bind all
three, unchanged; who commits is not changed here.
- *The code-writer lease holder* (§2, unchanged) writes code. **Code** here is every file
  the runtime runs or builds from — sources, templates, static assets, tests, migrations,
  translation templates and catalogs; files under the docs root are not code.
- *A documents-only part* writes only its own unit's files under the docs root and its own
  rows of the review log (FS2); it runs no git command that changes the checkout and no
  command that rewrites other units' files (`index`, `mark`). A change it needs elsewhere
  goes to the session that writes that file. (R4 gives the constraints «only its own unit's
  files, no git command that changes the checkout, never `index`, no code»; the review-log
  rows and the coordinator's role below are additions put to the owner at approval.) A
  part that will write code asks the coordinator before writing any: it takes the
  code-writer lease, or the owner commits its documents and its worktree is cut from that
  commit, so the branch's `gate`, review and map see its design.
- *The coordinator* works there: it writes the shared files (§1, §2, FS2), any file in the
  shared checkout that is neither code nor under the docs root (root `README.md`,
  `CHANGELOG.md`, `.gitattributes`, CI configuration — and runs `init` when needed), and
  runs `index`, `review-map` and `mark` — for the documents-only parts' closure steps too.
  In the shared checkout `review-map` sees every session's files, so a documents-only
  unit's merge brief takes its file table from that unit's section of the commit map, and
  says so. A part's closure message (§5) names the steps it left to the coordinator.
`SKILL.md` Phase 4 names the shared checkout as the one exception to «own worktree» under
coordination, pointing to `coordination.md`.

**FS2 — shared files other than request records.** §1 is retitled «Shared files: one
writer each», keeping its request-record bullets, and gains:
- *Review log* (append-only, rows unnumbered, each naming its document): every session
  appends only its own rows and never edits another's. In one checkout it appends without
  rewriting the file and rereads the file just before writing; across worktrees the
  `merge=union` stanza merges both sides (`templates.md` §REVIEW_LOG — cited, not restated;
  a project set up without it re-runs `init`). In a commit map, rows of several units go
  under Shared (`templates.md` §Commit map).
- *Translation catalogs* are code (FS1): in the shared checkout only the lease holder writes
  them; a wrong string another session finds goes to the holder through the coordinator.
- *An external tool's store tracked in git* (devPNT's `.devpnt/`): written by the tool, never
  by hand; in a commit map under Shared, naming the units whose work it holds — not
  Regenerated, which is the validator's.

**FS3 — coordinator continuity and handover.** In Trigger and roles:
- The role belongs to the named session: the client conversation the owner named. Compacted
  in place, it is the same session and keeps the role; before acting on its summary it
  rereads `leases.md` and the shared record, which are the state. A new conversation is a
  new session, whatever brief or summary it was given.
- A session started by another, the coordinator included, does not inherit the role; a
  message passing it on is information (§4), never a naming.
- `leases.md` opens with a `coordinator <session> — REQUEST_[unit].md#R<n> — YYYY-MM-DD`
  line instead of the free citation (a file opening with the 1.51.0 citation counts it as
  its first `coordinator` line). Parts read its last `coordinator` line to know whom to
  ask, and trust it only if the entry it cites quotes the owner naming that session — never
  a `decided under delegation` or `received for` entry.
- The owner changes the coordinator with a new entry naming the new session B. Whoever
  receives the owner's words enters them once: B, or A if the owner told A — then A tells
  B and stops, and the window below starts at A's entry. B appends a `coordinator` line and
  tells A (when A did not enter it) and the parts, citing the entry. A, shown the entry, writes no shared file again and
  answers that it stopped. Every line of `leases.md` and entry of the shared record that B
  did not write between the naming entry and A's answer goes to the owner; a number used
  twice is settled by a correction entry (`templates.md` §REQUEST), never by renumbering.
- Leases in force stay: they name holders, not the coordinator.
- A coordinator gone with no successor named leaves no session coordinating (Trigger): parts
  ask the owner, and the files stay as they are until the owner names one.

## Interface Contract

Actors: the owner; the coordinator (new and previous); parts. Surface: `audit/leases.md`,
a document form the owner reads and the coordinator writes (as in F-088).
- **Handover flow** — owner names session B in an entry → B enters it in the shared record
  (or A, if the owner told A, enters it, tells B and stops; the window starts at A's entry)
  and B appends `coordinator B — <entry> — <date>` → B tells the previous coordinator A and
  the parts, citing the entry → A stops writing shared files and answers B → B sends the
  owner every line and entry it did not write between the naming and A's answer.
  *Feedback:* A's answer to B; the owner's list from B; parts see the last `coordinator`
  line and check the entry it cites.
- **Documents-only part in the shared checkout** — the part writes its own unit's files;
  for any other file, and for `index`, `review-map`, `mark`, it sends to the coordinator.
  *Feedback:* its closure message names what it left to the coordinator; the commit map
  shows its files under its unit.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| let a session work in a shared checkout safely | INADEQUATE | `SKILL.md`:211; `coordination.md`:70-75 | only the code-writer lease exempt; G1 baseline |
| merge append-only review log rows across branches | EXISTS | `scripts/init.js` `gitattributes()`; `templates.md`:808 | init.js:115–140; baseline G2; chatPNT lacks the stanza |
| place a non-validator generated file in a commit map | INADEQUATE | `sdlc_check.py` `cmd_commit_map` | Regenerated errors (:368-370); Shared takes free text (:286-303), a `.devpnt` path classes REVIEW (:194-195) — fits, unsaid |
| keep one writer on a shared file | EXISTS for request records | `coordination.md` §1 | other shared files unnamed; G2–G4 |
| say who coordinates after compaction, chain or change | MISSING | `coordination.md` Trigger; `templates.md` §leases | names the session, nothing on continuity; G5–G7 |

## Guide check

- CURRENT guide covering what this touches: `GUIDE_skill_family_changes.md` — not engaged:
  every change is in the code lens only.
- High-complexity component understood here that no guide covers: no.

## Impact

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/coordination.md` | MODIFY | Trigger and roles: FS3 (role continuity, handover, reconcile); §1 retitled + FS2 bullets; §2: the opening-citation sentence (:59) becomes the `coordinator` line, the bold «one exception» (:70) becomes the FS1 shared-checkout paragraph; §5: closure message names steps left to the coordinator |
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | Phase 4 (:211): «under coordination, the code-writer lease is the one exception» → «under coordination, the sessions `coordination.md` §2 places in the shared checkout are the one exception to the own worktree — the bans hold there, and only its coordinator runs `index`» (P1) |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | §leases (:569-576): opening line `coordinator …`; §Commit map: one Shared line for a tool's store |
| `ai_docs/vision/rulings.md` | MODIFY | r42, and r40's basis cell «extended by r42», on approval |
| `ai_docs/solutions/harness_parallel_sessions_gaps/` | ADD | cases, replay, both results |
| `ai_docs/strategic/skill_family_agent_workflows.md` | MODIFY | the `coordination.md` line (:209): shared checkout, coordinator handover (`audit_plan.md` duty) |
| `README.md` | CHECK | :31 and :137 name `coordination.md` only: no change expected, confirmed at closure (`audit_plan.md` duty) |
| `CHANGELOG.md`, `package.json`, `gemini-extension.json`, `SKILL.md` `version:`, `README.md` region | MODIFY | at release |

No code change: `commit-map` accepts any path under Shared, and nothing in `scripts/` parses
`leases.md` (grep). No shared file changes, so no `shared_manifest.json` update and no
sibling copy (sibling `SKILL.md` files carry no code-writer clause). `hybrid.md`,
`dispatch.md`: no delta — FS3's reread is about `leases.md`, not the dispatch ledger.

### Preservation constraints

| id | bound to | must stay true | evidence |
|---|---|---|---|
| P1 | `SKILL.md` Phase 4 «Isolate the work» | a session works in its own worktree unless `coordination.md` §2 places it in the shared checkout; in any checkout another session may be using, no session switches branch, stashes or resets, and `index` runs there only by the coordinator of the shared checkout | replay G1, G9, G8 on the new text; F-073 (c) |
| P2 | `coordination.md` Trigger | without an owner naming no session coordinates | replay G5 |
| P3 | `coordination.md` §2 lease lines | a lease line names a resource and a session, never a unit; no queue (r40) | the `coordinator` line names a session and an entry: no resource, no unit |
| P4 | `sdlc_check.py commit-map` | unchanged | no code change; existing tests |
| P5 | `coordination.md` §1 request-record bullets | one writer per request record; record before acting | replay G8 |

## Security and Threat Model

Surface: filesystem writes by several agents in one checkout; authority of a session.
- **T1 — a documents-only part writes outside its write set** (another unit's file, a
  catalog). Files in one checkout carry no author and the commit map is a judgement
  (`sdlc_check.py`:277): its generated-file error covers only the validator's outputs.
  Detection is the coordinator checking each part's diff against its closure message (§5,
  unchanged). Residual: a stray write the coordinator misses is committed under the wrong
  unit.
- **T2 — lost update in one checkout.** Two sessions appending to the review log; a tool
  that reads the whole file and rewrites it drops a row written in between, losing gate
  evidence. FS2: append without rewriting, reread just before writing. Residual: a race
  inside that window.
- **T3 — the commit sweeps half-written files** of a documents-only part into the
  lease holder's commit. The commit map's Left out section names them (§6, unchanged).
- **T4 — a session claims the coordinator role** (G5), by message or by appending a
  `coordinator` line. FS3: only an owner entry names; a message is information (§4); a
  `coordinator` line counts only if the entry it cites quotes the owner naming that
  session. Residual: a forged quotation in the shared record — the owner is told of each
  entry and may correct it (record rule, unchanged).
- **T5 — a stale summary acts on a lease** (G6). FS3: reread before acting.
- **T6 — two coordinators write at once** (G7): two writers on the shared record number
  entries twice (F-088 C1) and both write `leases.md`. FS3: B tells A at once; until A
  answers, every line B did not write goes to the owner; duplicates are corrected by a new
  entry. Residual: a lease taken or released by A in that window may already have been
  acted on — the owner sees it and decides; A unreachable means the window stays open and
  the owner may tell A directly.

## Ceremony cost

Estimates, measured at implementation:

| Where | Who reads it | Added |
|---|---|---|
| `coordination.md` (7,080 B today) | only coordinated sessions | ~4 KB (FS1 ~1.6, FS2 ~0.9, FS3 ~1.5), about +55% |
| `SKILL.md` (code) | every session | ~0 B (one phrase replaced) |
| `templates.md` (code) | every L3 reading the leases or commit-map template | ~100 B |
| `rulings.md` | the Vision gate | one row, ~1 KB |

Under coordination: one `coordinator` line per naming, and a reconciliation at each
handover; a documents-only part sends changes to other files through their writer, and
leaves `index`, `review-map`, `mark` to the coordinator. Removed: one branch to merge per
documents-only unit.

## Action Plan

- [x] Replay `cases.md` on the old text — baseline (`results_old_text.md`).
- [x] Design review PASS, then owner approval of the design, of r42 and of the cost above.
- [x] r42 in `rulings.md`.
- [x] `coordination.md`, `SKILL.md`, `templates.md`, family workflows doc; README checked.
- [x] Replay on the new text (cold reader), G9 on both texts — green; bytes measured.
- [x] Code battery, `node scripts/test_clients.js`, `check`; E2E script, closure review,
      merge brief; `mark skills/` last.

## Test Strategy

- Replay harness: cold reader, old then new text, verdicts kept in
  `harness_parallel_sessions_gaps/`.
- Wiring and drift: code battery (`test_support_files_wired`, `test_drift.py`) — unchanged
  files must stay green; `node scripts/test_clients.js` (`templates.md` is parsed by
  `scripts/lib.js`).
- No new unit test: no code changes.

## Diary / Current State

- 2026-11-01 — Opened from the M155 coordinator's review of `coordination.md` 1.51.0 (R1–R3).
  Owner chose the documents-only exception with constraints (R4). Evidence gathered from
  chatPNT: commit b8755e76 carries the review log, `.devpnt/` DBs and translation catalogs;
  chatPNT's `.gitattributes` lacks the review-log `merge=union` stanza.
- 2026-11-01 — Baseline replay on 1.51.0 (`results_old_text.md`): G1 forbidden, G3/G4/G6/G7
  not flagged, G2 partly covered, G5 by implication only.
- 2026-11-01 — Design review round 1 FAIL (4 BLOCK, 11 WARN, 1 CANNOT_VERIFY). Rewritten:
  r42 and its distinction lines (B1); the shared checkout named, with the coordinator and its
  `index`/`review-map`/`mark` in it, P1 amended (B2); the «any other file» catch-all dropped
  (B3); threats rewritten — T1's residual, lost update, half-written files, two writers on the
  shared record (B4); R4's additions marked (W1); same session defined (W2); `coordinator`
  line opens `leases.md` (W3); reconciliation route (W4); Interface Contract fired (W5); code
  defined, catalogs scoped (W6); the move to code (W7); §1 retitled (W8); cost re-estimated
  (W9); `mark` and README check (W10); `init` re-run (W11); G3's write claim softened and G9
  added (CANNOT_VERIFY).
- 2026-11-01 — Design review round 2 FAIL (1 BLOCK, 9 WARN). Fixed: the handover window
  runs to A's answer, with correction entries for duplicates and T6's residual (N1);
  documents-only merge brief takes its table from the commit map (N2); the owner commits
  documents before a part's code worktree is cut (N3); r42 supersedes r40's clause, r40's
  basis notes it (N4); a `coordinator` line counts only if it cites owner words, the live
  files are the shared checkout's (N5); the git ban for all three kinds dropped — Phase 4's
  bans stay, R4's git ban binds the documents-only part (N6); the 1.51.0 opening citation
  counts as the first `coordinator` line (N7); files neither code nor docs, and `init`, are
  the coordinator's (N8); cost re-estimated ~4 KB, +55% (N9).
- 2026-11-01 — Design review round 3 FAIL (1 BLOCK, 1 WARN); N1–N9 verified addressed.
  Fixed: P1 and the `SKILL.md` sentence keep the bans in the shared checkout, the exception
  is to «own worktree» only and `index` is the coordinator's (NEW-1); a naming the owner
  gives the previous coordinator is entered once, by it (NEW-2). Round cap reached: put to
  the owner, who asked for a fourth round (R5).
- 2026-11-01 — Design review round 4 PASS (2 WARN, nothing blocking): NEW-1 and NEW-2
  verified addressed; FS1, P1 and the `SKILL.md` row agree. Both WARN fixed (wording): the
  Interface Contract's handover flow gains the branch where A is told; R5 cited.
- 2026-11-01 — Owner approved design, r42 and cost (R6). Doctrine written: `coordination.md`
  (Who coordinates; §1 retitled + three shared-file bullets; §2 `coordinator` line and the
  shared checkout with three kinds of session; §5 open points), `SKILL.md` Phase 4 sentence,
  `templates.md` leases opening line and a Shared example; r42 and r40's basis note; family
  doc. README checked: :31 and :137 name `coordination.md` only, still true. New-text replay
  (`results_new_text.md`): G1–G9 all FLAGGED with the targeted route, G8 unchanged; G9 on the
  old text partly (forbids `index`, no route). One ambiguity fixed: the coordinator writes a
  closing documents-only unit's commit-map section for its brief. Bytes (LF): `coordination.md`
  +3,961 (estimate ~4 KB, +57%), `SKILL.md` +103 (estimate ~0 — every session reads it),
  `templates.md` +92.
- 2026-11-01 — Closure review PASS (6 WARN, 1 NIT, 1 CANNOT_VERIFY; nothing blocking). Fixed:
  Diary figures (W1); HANDOFF `next:` (W2); family doc's git ban narrowed to the doctrine's
  and review-log rows named (W3); the live shared record is the shared checkout's too (W4);
  S6 closure in the shared checkout and R4 bans in the E2E script (W5); a coordinator gone
  with no successor: parts ask the owner, `leases.md` and the shared record stay as they are
  (W6); line 95 rewrapped (N1). CV1 accepted: replay transcripts are kept condensed, as in
  F-088. Final bytes (LF, against `c1ff546b`): `coordination.md` +4,138 (6,941 → 11,079,
  +60%; estimate ~4 KB), `SKILL.md` +103 (estimate ~0), `templates.md` +92 (estimate
  ~100), `rulings.md` +2,059 (estimate ~1 KB — the row carries three distinction lines).
- 2026-11-01 — `mark skills/agentic-sdlc-skill/` (and `skills/`) after the closure fixes.
  `check --hybrid` CLEAN; plain `check` NOT CLEAN only on `stale` for `scripts/` and
  `distributions/`, which this unit does not touch (`git diff` empty): the fresh-worktree
  mtime artifact recorded in F-088's Diary. Re-run `check` on `main` after the merge.
- 2026-11-01 — Closed: owner asked for commit and merge (R7). HANDOFF deleted, indexes
  regenerated; `main` fast-forwards to the branch.
