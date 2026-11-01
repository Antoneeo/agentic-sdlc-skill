---
id: F-090
feature: The review log's merge line, checked instead of announced
status: COMPLETED
level: L3
start_date: 2026-11-01
end_date: 2026-11-01
---
# Feature Analysis: the review log's merge line, checked instead of announced

**For whom**: the independent design reviewer, then the owner. **To do what**: approve or
reject the check below before code is written. **Answers**: how a project missing the
review log's `merge=union` attribute gets it without anyone reading a changelog. **Does
not answer**: any other `.gitattributes` content; how merges of other files behave.

Owner statements: `audit/requests/REQUEST_review_log_union_check.md` R1–R5.

## Objective

`init` writes `<docs>/audit/reviews/REVIEW_LOG.md merge=union` into `.gitattributes` (code
and kb for `ai_docs`, marketing for `mkt_docs`; `scripts/init.js` `gitattributes()`,
F-028), so two branches that both append review rows merge without a conflict. Projects
left without it, and nothing tells anyone:
- set up before F-028, or never through `init`;
- with a custom docs root, or migrated from `mkt_docs` to `ai_docs` (the line names the old
  path);
- whose project root sits below the repository root (`init` needs `.git` in its working
  directory, `scripts/init.js`:132);
- course projects: course `init.js` writes no `.gitattributes`, and seeds no review log —
  so the check fires only once a log exists, which is the right moment.
Measured: chatPNT, `git check-attr merge -- ai_docs/audit/reviews/REVIEW_LOG.md` →
`unspecified`; this repository → `union`.

The fix announced so far — «re-run `agentic-sdlc-init`» in the 1.52.0 notes and
`coordination.md` §1 — depends on a person reading it: the owner rejected it as not
poka-yoke (R1) and asked for the check before the release (R2).

## Feature Vision

Serves the team-lead Actor («one process, one source of truth») and the Goal «keep
understanding durable across sessions»: review evidence from parallel branches merges
without a hand-resolved conflict. One ANALYSIS, no feature Vision.

**Ruling ledger.** Placed against r15 (packaging, installation, distribution — ADMIT): the
note answers «is this project set up as `init` sets it up», the same question as an
installation step, so r15's verdict applies; no new row. Near r3 (by whom): the note names
a setup repair and its exact line, never what to work on next or who does it.

**Options weighed (R3).** The owner chose the note in `check`:
- *Note at session start too* — rejected: session orientation is zero-execution (it reads
  and prints, never runs anything: `sdlc_core.py` `cmd_orient` docstring, `ENFORCEMENT.md`
  ×4, the F-036 threat model); running git there withdraws that guarantee for sessions
  opened on an untrusted clone whose git configuration can run commands.
- *Automatic write by `index`* — rejected: the validator has never written outside the docs
  root, and `.gitattributes` is a shared root file (under coordination it is the
  coordinator's, `coordination.md` §2).
- *Note in `check`* — chosen: no new execution surface (`check` already runs git for
  `stale` and the id scan), and every closure in a project that uses the validator, and CI
  `check`, runs it, so the agent meets it at the first closure and adds the line.

Non-goals: writing `.gitattributes` from the validator; a validate warning (`--strict` CI
must not fail on it — the F-041 contract, `ENFORCEMENT.md` §4); running git in session
orientation; checking any file other than the review log.

Success signal: on chatPNT's tree `check` prints the note with the exact line; on this
repository it does not; after the line is added it is gone; `orient` output unchanged.

## Use Cases / User Needs

- **UC1 (Team lead / owner)** — have the review log made merge-safe without reading release
  notes: the agent is told at the first `check` and adds the line. *Benefit: one process,
  no hand-resolved conflicts.*

Grounding: `.gitattributes`, `merge=union`, `check`, the F-041 note — EXISTS. The
review-log union note — NEW.

## Functional Spec

**FS1 — detection.** `review_log_union_note(root)` in `sdlc_core.py` returns a note string
or `None`. Inside one `try` (any exception, `TimeoutExpired` and `OSError` included, returns
`None`; detection never breaks `check`):
1. If the docs root's `audit/reviews/REVIEW_LOG.md` does not exist → `None`.
2. `git rev-parse --show-prefix` in the root, timeout 3 s; failure → `None` (not a work
   tree — no separate `git_available` call).
3. `git -c core.attributesFile= check-attr -z merge -- <path relative to the root>` with
   `GIT_ATTR_NOSYSTEM=1`, timeout 3 s; parsed from the NUL-separated output. Both calls go
   through `_git_out`, which gains `env=None` (merged into `os.environ`, never replacing it,
   so PATH survives on Windows); its existing callers pass nothing and are unchanged.
4. Note only when the value is `unspecified`. `union`, `set`, or any custom driver
   (`merge=foo`) is a deliberate choice: no note.
Committed sources count, personal ones do not: system and user attribute files are
excluded. Residual: `.git/info/attributes` (per clone) is still read; a project relying on
it alone is silent here while teammates' merges can still conflict — stated, not handled.

**FS2 — the note.** One line with the path as the repository sees it (show-prefix joined,
POSIX separators), the consequence and the exact line to add:
`[note] <path> has no merge attribute: two branches that both add review rows conflict when merged. Fix: add this line to .gitattributes at the repository root: <pattern> merge=union`
`<pattern>` is built in this order, the only one git reads back as this file (probed):
first backslash-escape `\`, `[`, `*`, `?` and a leading `#` or `!`; then, if the result contains
whitespace, `"` or `\`, C-quote it (`"…"`, doubling `\` and escaping `"`).

**FS3 — where it prints.** Only in `check`, informational, never an exit code. One
`print_check_notes(root)` prints the F-041 orientation-hook note and this one; the spine's
`cmd_check` and `mkt_check.py` (which replaces `check`) call it instead of
`print_orient_hook_note`, so the next check-layer note cannot miss marketing. Session
orientation is unchanged.

**FS4 — doctrine and notes.**
- `coordination.md` §1 review-log bullet: «a project set up without the union stanza re-runs
  `init`» → «`check` names a missing union line and the line to add»; under coordination the
  coordinator adds it (`.gitattributes` is its file, §2).
- `ENFORCEMENT.md` ×4, where `check`'s informational notes are listed (F-041): one sentence
  for this note.
- `templates.md` (code, kb, mkt — the lenses whose §REVIEW_LOG carries the union paragraph):
  «without the stanza … one conflict you resolve by hand» gains «`check` names a missing
  line».
- 1.52.0 notes: the «re-run `agentic-sdlc-init`» step is dropped; the benefit is stated
  instead (`check` tells the agent, which adds the line).

## Interface Contract

Actor: the agent (reads the note, adds the line); the owner sees it in `check` output.
Surface: one `[note]` line in `check`. Flow: `check` → git asked → note when `unspecified` →
the agent adds the line (the coordinator, under coordination) → next `check` prints nothing.
Feedback: the note disappears.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| write the union line at setup | EXISTS (code, kb, mkt) / MISSING (course) | `scripts/init.js` `gitattributes()` | course init.js: 0 matches; left to the note (Objective) |
| tell a project its review log is not merge-safe | MISSING | — | no `check-attr` in `scripts/*.py` (grep) |
| check-layer informational note | EXISTS | `print_orient_hook_note` (F-041) | sdlc_core.py:2437; re-attached by hand in mkt_check.py:753-757 |
| run a git command with a timeout | EXISTS | `_git_out` | sdlc_core.py:1380 — lets `TimeoutExpired`/`OSError` propagate, hence FS1's `try` |

## Guide check

- `GUIDE_skill_family_changes.md` — engaged: `sdlc_core.py`, `test_merge_safety.py`,
  `ENFORCEMENT.md` copied ×4 count once.
- `GUIDE_shared_project_memory.md` — engaged: marketing replaces `check`; FS3's single
  `print_check_notes` is the composition fix.

## Impact

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` + 3 copies | MODIFY | FS1 `review_log_union_note`, FS2, `print_check_notes`; `cmd_check` calls it |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py` | MODIFY | `print_check_notes` replaces `print_orient_hook_note` |
| `skills/agentic-sdlc-skill/scripts/test_merge_safety.py` + 3 copies | MODIFY | tests |
| `skills/agentic-sdlc-skill/scripts/test_golden_regression.py`, kb's `test_golden_regression.py` | MODIFY | `run_corpus` env pins `GIT_CEILING_DIRECTORIES`, so a temp dir inside a work tree cannot add the note to the baseline |
| `*/scripts/shared_manifest.json` ×4 | REGENERATE | `shared_files.py --update` |
| `skills/agentic-sdlc-skill/ENFORCEMENT.md` + 3 copies | MODIFY | FS4 |
| `skills/agentic-sdlc-skill/templates.md`, kb and mkt `templates.md` | MODIFY | FS4 |
| `skills/agentic-sdlc-skill/coordination.md` | MODIFY | FS4 |
| `CHANGELOG.md` ×4, versions ×4, README regions ×4 | MODIFY | at release: 1.52.0 widens to all four packages, the validator ships in each |
| `ai_docs/solutions/E2E_TEST_review_log_union_check.md`, `MERGE_REVIEW_…` | ADD | closure |

Blast radius: `_git_out` gains `env=None` — its two callers per copy pass nothing,
unchanged. `cmd_check` — reached by code, kb and course through `knowledge.kb_cmd_check`
(`knowledge.py`:2587; course `sdlc_check.py`:55-62) and replaced by marketing's
`mkt_check.py`:753; no other entry replaces `check`. `print_orient_hook_note` keeps its
behaviour, called through `print_check_notes`. `cmd_orient`: untouched.

### Preservation constraints

| id | bound to | must stay true | evidence |
|---|---|---|---|
| P1 | `cmd_check`, `mkt_check` check | exit code unchanged by the note, and by a git failure | tests |
| P2 | `cmd_orient` | zero-execution: no subprocess in its call graph | new guard test (Test Strategy) |
| P3 | `cmd_validate` | unchanged (file-local, `--strict` unaffected) | existing battery |
| P4 | F-041 note | printed under the same conditions as before | existing tests |

## Security and Threat Model

Surface: two git subprocesses in `check`, which already runs git (`stale`, id scan).
- **T1 — command injection through the path**: fixed argv list, `--` before the path, no
  shell; the path comes from the docs root, never from file content.
- **T2 — a hung git**: 3 s timeout per call; `TimeoutExpired`/`OSError` caught → no note.
- **T3 — a note that misleads**: git itself evaluates the attribute; personal attribute
  files excluded so a teammate's view matches; `info/attributes` residual stated (FS1).
- **T4 — repository configuration running commands** when git runs: not new — `check`
  already runs git in the same tree; orientation, the one zero-execution path, is untouched
  (P2).

## Ceremony cost

Two git calls (~90 ms measured on Windows) per `check`, only where a review log exists.
Output: one line, only while the attribute is unspecified. Doctrine: one phrase in
`coordination.md`, one sentence in `ENFORCEMENT.md` ×4, one clause in `templates.md` ×3.

## Action Plan

- [x] Design review PASS, owner approval.
- [x] RED tests.
- [x] `sdlc_core.py` ×4, `mkt_check.py`, `test_golden_regression.py`, doctrine;
      `shared_files.py --update`.
- [ ] Batteries ×4, `test_clients.js`, `check`; chatPNT probe; E2E, closure review, merge
      brief.

## Test Strategy

In `test_merge_safety.py` (shared ×4; git tests skip without git), temp git repo with
`GIT_CEILING_DIRECTORIES` and `GIT_CONFIG_GLOBAL` pinned:
- note when the review log exists and the attribute is unspecified; none with `merge=union`;
  none with a covering pattern (`*.md merge=union`); none with a custom driver
  (`merge=foo`); none without a review log; none outside git;
- the path is relative to the git top when the project root is a subfolder;
- a path with a space and a bracket (`My [P]roj/…`): the printed line, once appended to
  `.gitattributes`, makes git report `union` (round trip);
- `_git_out` raising `TimeoutExpired` / `FileNotFoundError` (patched): no note, no
  exception;
- `cmd_check` exit code identical with and without the note;
- marketing: `mkt_check`'s `check` prints the note (`try: import mkt_check` + `skipIf`, the
  shared-file pattern of `test_chronology.py`), called with `--docs-dir ai_docs` and the
  docs root restored in `tearDown`, so later tests keep their pin;
- `orient` runs no subprocess: `subprocess.run` patched to raise, output unchanged (P2).

## Diary / Current State

- 2026-11-01 — Opened from the owner's rejection of the 1.52.0 notes' step 2 (R1, R2).
  Probe: chatPNT `unspecified`, this repository `union`; course `init.js` writes no
  `.gitattributes`.
- 2026-11-01 — Design review round 1 FAIL (1 BLOCK, 9 WARN, 2 CANNOT_VERIFY). Owner chose
  the note in `check` only (R3): orientation keeps zero-execution (B1). Rewritten:
  ENFORCEMENT ×4 and templates ×3 in FS4 (W1); one `print_check_notes` (W2); quoting,
  `-z`, POSIX path (W3); personal attribute files excluded, note only on `unspecified`,
  `info/attributes` residual (W4); tests for failure paths, space path, custom driver,
  marketing, pinned git env and the golden corpus (W5); ruling placed under r15 with an r3
  line (W6); options weighed, course decision, precise Objective (W7); coordinator adds the
  line (W8); 3 s timeout inside the `try`, no `git_available` (W9). CANNOT_VERIFY: the
  release notes are read at release in the primary checkout; fsmonitor moot with no git in
  orientation.
- 2026-11-01 — Design review round 2 PASS (6 WARN). Folded in: escaping order, glob first
  then C-quote, leading `#` (N1); kb's golden test pinned too (N2); `_git_out(env=None)`
  merged into `os.environ` (N3); marketing test docs-root restore and an orient
  no-subprocess guard (N4); `ENFORCEMENT.md` §4 (N5); reach stated as closures in projects
  using the validator, and CI (N6). Release notes CANNOT_VERIFY carried to closure.
- 2026-11-01 — Owner approved the design (R4). RED: 11 of 12 new tests failed (the orient
  guard passed, as it must before and after). Implemented: `_git_out(env=None)`,
  `_attr_pattern`, `review_log_union_note`, `print_check_notes` in `sdlc_core.py` (copied
  ×4), `mkt_check.py` through `print_check_notes`, golden runners pinned (code, kb),
  `ENFORCEMENT.md` ×4, `templates.md` ×3, `coordination.md`; manifests regenerated. GREEN:
  code 600 OK (skipped 4) after `index`, kb 913, mkt 588, course 611; clients 63, 4, 50, 50.
  Probe: chatPNT prints the note with `ai_docs/audit/reviews/REVIEW_LOG.md merge=union`;
  this repository prints none.
- 2026-11-01 — Closure review PASS after a scoped re-review (REVIEW_LOG «F-090 closure»):
  fixed a stripped leading space in the prefix, an unescaped leading `!` and backslash, a
  vacuous orient guard (now recording mocks; two mutants fail it), `ENFORCEMENT.md` naming
  the `.git/info/attributes` exception, E2E S3b on `mkt_docs`; the design rows merged into
  one (review.md §Receiving). Batteries green ×4. Open: one POSIX run of `MS_UnionNote` for
  the backslash and `*?` round trips.
- 2026-11-01 — Owner approved commit and merge (R5): COMPLETED, merged into `main`
  (fast-forward); release 1.52.0 for all four packages follows. The POSIX run stays open.
