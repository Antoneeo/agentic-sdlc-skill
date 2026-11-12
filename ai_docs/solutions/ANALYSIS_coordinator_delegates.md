---
description: F-095 - under coordination the coordinator executes no unit itself, and a part integrates its own branch. Field case, the doctrine gap in coordination.md, the rule, its replay.
status: IN_PROGRESS
feature: F-095
id: F-095
start_date: 2026-11-12
level: L3
branch: claude/f095-coordinator-delegates
---
# ANALYSIS: The coordinator does not do a part's work (F-095)

## Objective

On 2026-11-12 the named coordinator cleaned this repository and integrated a part's branch
itself, outside the skill (`audit/requests/REQUEST_coordinator_delegates.md` R1). The owner:
the skill explains how to delegate, but perhaps not this. Make `coordination.md` say what
the coordinator does NOT do itself, and who integrates a part's branch.

## Feature Vision

Serves the skill's purpose (acting from partial understanding) and `coordination.md`'s own
role split (a part "following the whole skill for it"). No new capability, no Non-Goal
touched: Non-Goal 1 (no ordering or priority of parts) stays untouched — the rule assigns
acts to roles, it never decides which part runs next.

## Diagnosis — the mechanism

`coordination.md` defines the coordinator positively (shared files, leases, `index`/`mark`
in the shared checkout, checking parts' claims) and never says what it must not execute.
Three consequences, replayed by a cold reader (`harness_coordinator_delegates/replay.md`):

1. Merge, push and repository cleanup by the coordinator: **SILENT**.
2. Re-marking after an integration: **PERMITTED** by "it alone runs `index`, `review-map`
   and `mark` there" — the sentence written for documents-only parts reads as a licence.
3. A coordinator acting on a unit triages nothing: coordinating is not a unit, so the work
   it absorbs runs with no level, no router verdict, no guide — exactly the field case.

Falsified on the way: the field staleness was not caused by merging in the shared checkout
(probe in `replay.md`); the rule rests on role and context, not on the validator.

## Use Cases / User Needs

- UC1 — The owner hands the coordinator an integration ("integrate it and push"): the
  coordinator sends it to the part that made the branch (EXISTS: part, branch, `coordination.md` §4 for the authorization).
- UC2 — The owner asks the coordinator to tidy the repository: the cleanup is a unit, it
  goes to a part that declares level and verdict (EXISTS: unit, Rule Zero).
- UC3 — The owner explicitly tells the coordinator to do a unit itself: it does, as a part
  of that unit, with its own record (this very unit, R2).
Each traces to the purpose "acting from partial understanding": the session with the
context does the work, under the skill.

## Functional Spec

- FS1 — Under coordination every L2/L3/Spike, repository cleanup and other units' rows
  included, goes to a part. Coordinator acts: shared files and §2 commands (the
  fast-forward of FS4 included), decisions under delegation (§3), reading and checking
  parts, reporting, asking. An L1 edit to a file it owns is not a unit.
- FS2 — The owner's explicit instruction makes the coordinator a part for that unit.
- FS3 — Integration after the owner's choice is the part's: merge the integration line into
  its branch in its own worktree, re-mark, `check` CLEAN, then move the line (fast-forward
  push, or with no remote ask the coordinator for FS4). The part never writes the shared
  checkout; a push needs the owner's yes in the part's own session (§4). The coordinator
  never merges a part's branch, makes the re-mark that merge needs, or pushes it. Removing any branch or worktree under
  coordination needs the owner's yes in the removing session, naming them (`SKILL.md` Phase 5).
- FS4 — In the shared checkout the coordinator's one git write is an `--ff-only`
  fast-forward to the checked commit, at the part's request, only when `git status` shows
  nothing uncommitted but its own shared files;
  `mark` there never repairs an integration.
- FS5 — A part without a §5 closure message is not integrated by the coordinator: §5
  applies, the owner decides.
Acceptance: the cold replay rules all four field acts FORBIDDEN; the invariant test fails on
the old text and passes on the new.

## Interface Contract

Not fired: the change alters doctrine an agent reads, not a surface an actor acts on; the
coordinator's message to the owner keeps the §5 shape.

## Capability Ledger

| Capability | Verdict | Where |
|---|---|---|
| Assign a unit to a part | EXISTS | `coordination.md` §Trigger and roles, Part |
| Say what the coordinator must not execute | MISSING → written | `coordination.md` §Trigger and roles |
| Assign integration to a role | MISSING → written | same section; §2 sentence tightened |

## Guide check

- CURRENT guide covering this work: `GUIDE_skill_family_changes.md`, read whole; applied:
  `coordination.md` ships only in the code lens, so no copy counts.
- No high-complexity component was modelled: no new guide is owed.

## Impact

| File | Change |
|---|---|
| `skills/agentic-sdlc-skill/coordination.md` | two paragraphs in §Trigger and roles; §2 `mark` sentence |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | `test_coordinator_delegates_units_and_parts_integrate`; a shared file, so copied identically to the three distributions with their `shared_manifest.json` regenerated (counts once, `GUIDE_skill_family_changes.md`); it skips outside the code lens |
| `skills/agentic-sdlc-skill/evals/scenarios/coordinator_delegates_unit_work.md` | new scenario |
| `ai_docs/...` | request record, this ANALYSIS, replay, handoff, E2E, merge review |

### Preservation constraints

| Symbol | Consumers | Must stay true |
|---|---|---|
| `coordination.md` §2 coordinator bullet | documents-only parts' closure (§2, §5) | the coordinator still runs `index`/`review-map`/`mark` for them |
| §4 authorization rule | parts receiving relayed owner words | a relayed "integrate" stays information; the part may ask the owner |

## Security and Threat Model

T1 — a coordinator integrating unreviewed state into the integration line: reduced, the
part integrates only a commit `check` passed. T2 — a gated act (push) taken on relayed
authority: unchanged, §4 still governs. No new surface.

## Action Plan

1. Rule in `coordination.md`. 2. Invariant test, red/green. 3. Cold replay, red/green.
4. Scenario. 5. Independent review. 6. `check`, commit on the branch.

## Test Strategy

`test_skill_invariants.py` (new test red on `harness_coordinator_delegates/coordination_before.md`,
green on the branch), full unittest battery, `sdlc_check.py check`, the replay record.

## Diary / Current State

- 2026-11-12 — Opened in the coordinator session on the owner's instruction (R2). Stale
  hypothesis falsified by a throwaway probe; rule written; invariant test and cold replay
  red before, green after; §2 tightened on the replay reader's remark.
- 2026-11-12 — Independent review FAIL (1 BLOCK: cleanup without the owner's yes; 8 WARN).
  All folded: owner-authorized cleanup, the fast-forward in the closed list and in §2 with
  an uncommitted-work precondition, the part never writes the shared checkout, push on the
  owner's yes in the part's session, \"gone\" replaced by the §5 closure message, test on full
  sentences plus the §2 bullet (now red by failure, not by exception), replay re-run on the
  final text, eval cleanup gated on the owner.
- 2026-11-12 — Round 2 FAIL (replay not pinned to the text; precondition cited §2 without a
  rule; removal authorization without locus, only the part's own; eval clause unguarded).
  Folded: removal rule for any branch/worktree with the yes in the removing session, the
  `git status` precondition stated in place, test anchors for both and the eval, replay
  re-run pinned to sha256 dce42b60…
- 2026-11-12 — Round 3 PASS, 3 WARN fixed after the cap: the coordinator sentence narrowed to
  the re-mark a merge needs (no clash with §2), removal clause disambiguated, relayed-words
  anchors added. Verified by the test (red on old, green on new) and a cold replay pinned to
  sha256 7301604b…; not re-reviewed.
