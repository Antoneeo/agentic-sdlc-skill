---
description: F-056 - `stale` fails closed on every ANALYZED audit-plan row whose reference it cannot evaluate (pruned, squash-merged away, beyond a shallow clone, git unavailable, unparseable), warns while a reference is an orphan (not an ancestor of HEAD), and `mark` names the gestures that orphan the reference it records.
status: COMPLETED
feature: F-056
id: F-056
start_date: 2026-09-14
end_date: 2026-09-14
level: L3
branch: fix/stale-dangling-ref
---
# ANALYSIS: stale fails closed on a reference it cannot evaluate (F-056)

## Precedent placement

Against `vision/rulings.md`: **r14** exempt (defect fix, purpose/actors/surface unchanged).
`stale` exists to say whether an analyzed area is still fresh; excluding an area it cannot
evaluate while printing `[ok]` is that purpose failing. **r15** also applies: the regression
test is the product's own tests. No REJECT row matches.

## Ceremony budget

No step, field, document or gate is added to a workflow in which the recorded reference
stays in the integration branch's history (mark, then a new commit, merged by merge commit
or fast-forward) — that workflow's output changes by one `[info]` line at `mark`.

Two workflows DO pay, and the cost is disclosed here rather than discovered by them:

- **Squash-merge, rebase-merge, `pull --rebase`, cherry-pick.** A reference `mark` records on
  a feature branch never enters the integration branch's history. Today such an area is
  silently unevaluated forever, on every clone. After F-056 it fails `stale`/`check` until
  re-marked on the integration branch: one `mark` per merge that touched a marked area.
- **CI running `check` or `stale` on a shallow clone, or where git refuses the checkout.**
  Today: warning, rc 0. After: rc 1 with a hint naming the cause. `ENFORCEMENT.md` §2
  prescribes `validate --strict` for CI, so only a pipeline that chose `check`/`stale` pays.

The Non-Goal "no ceremony ratchet" requires the owner's explicit acceptance of that cost;
how it was handled is recorded in the Diary. The alternative that avoids it is ruled out in the
Capability Ledger. Doctrine read cost: one sentence in each lens's audit-plan template
(code, kb).

## Objective

Observed 2026-09-13: three `audit_plan.md` rows (`skills/agentic-sdlc-skill/`,
`distributions/`, `skills/`) held a reference no branch contained — a sibling of the commit on
main, same parent and timestamp, differing only in `audit_plan.md`. Diagnosis (the owner's,
from that signature): `mark` recorded `HEAD`, then `git commit --amend` folded the rewritten
`audit_plan.md` into that same commit, leaving the recorded commit reachable only through the
reflog. After reflog expiry and `git gc`, `cmd_stale` printed
`[warn] <area>: git ref '<X>' unresolvable, cannot evaluate`, `continue`d without touching
`rc`, then printed `[ok] no analyzed area was modified` — three areas out of staleness.
Repaired by hand in 790b90c. The amend cannot be re-verified from the repository (the history
was rewritten since); P1 shows an amend produces exactly that signature, and the design does
not depend on which rewrite it was — P5 covers squash, P2 amend.

Goals: (1) a reference `stale` cannot evaluate makes it return 1 and tells the user to
re-mark; (2) the dangling reference is caught before it dangles — at `stale` time while the
orphan is still in the object store, and at `mark` time by naming the gestures that create it.

**The mechanism, named.** `cmd_stale` treats "cannot evaluate this row" as "this row is
fresh". Probed, it does so on four paths, not one: pruned reference (P2), reference that
never reached this clone (P5, P6), hash reference where git is unavailable — which falls to
the timestamp branch and is reported "not parseable" (P7), and a reference that is neither
hash nor timestamp (P8). F-056 changes the rule for all four. Two sibling `continue`s are a
different case and stay: an ANALYZED path that **no longer exists** has nothing left to be
modified (vacuously fresh, not unevaluable) — except under a sparse or partial checkout, where
the area exists in HEAD but not on disk: declared as a residual in the populations table, not
fixed here — and a row **rejected by confinement** (absolute,
`..`) is hostile document content refused before any walk — a security rejection, not an
analyzed area (`cmd_validate` skips such rows the same way).

## Feature Vision

`vision/project_vision.md` — Status APPROVED (v8).

- **Success Signal #2 "Closure is mechanically clean … no mapped area is stale"** — widened:
  today `check` reports CLEAN while mapped areas are unverified (probe P9 red), so the signal is
  met on paper only. After F-056 an unverifiable area cannot yield CLEAN.
- **Goal "keep understanding durable across sessions"** — the audit plan is the durable record
  of what was analyzed against which state; a reference that silently stops meaning anything is
  that record rotting unseen.
- **Non-Goals**: "no ceremony ratchet" — cost disclosed above, owner acceptance requested; not
  a work-management surface; no second triage authority; nothing coupled to another tool.

Actors: Solo developer, Team lead (the `check` gate at closure and in CI).

## Use Cases / User Needs

Buckets: *audit plan* (`audit/audit_plan.md`), *`mark`*, *`stale`*, *`check`*, *reference*
(the `Reference` column) EXIST · *orphan reference* NEW (a reference that resolves to a commit
HEAD's history does not contain).

- **UC1 — Solo developer or Team lead runs `check` at closure or in CI** and must not be told
  CLEAN when an analyzed area's freshness cannot be evaluated. Traces to: Success Signal #2.
- **UC2 — Solo developer rewrites the commit `mark` recorded** (amend, rebase, squash-merge)
  and needs to learn it while the reference can still be re-marked cheaply. Traces to: Goal
  *durable understanding*.
- **UC3 — Solo developer runs `mark`** and needs to know how to commit and merge the result so
  the reference stays meaningful. Traces to: Goal *durable understanding*.

## Functional Spec

Trigger fired: `stale`'s, `check`'s and `mark`'s observable output and exit status change.

Behavior, for an `ANALYZED` row that passed confinement and whose path exists:

- **B1 Missing reference.** The reference is hash-shaped, the tree is a git work tree, and the
  reference does not resolve to a commit → reported `[stale]`: the reference; that the area's
  freshness cannot be evaluated; the cause — the commit is not in this repository (amended,
  rebased or squash-merged away and pruned, or never fetched here); the re-mark command
  `<entry> mark <path>`, where `<entry>` is the running distribution's script name. When the
  clone is shallow, the message ADDS that history is truncated and full history may hold the
  commit (`git fetch --unshallow`) — added, not substituted, because a shallow clone of a
  squash-merged repository is missing the commit for the squash reason. `stale` returns 1.
- **B2 Orphan reference.** The reference resolves to a commit that is not an ancestor of HEAD →
  `[warn]`: the reference; the likely causes (amended, rebased, squash-merged, or marked on
  another branch); that it will stop resolving once git prunes it or on any fresh clone; the
  re-mark command. Freshness is still evaluated against that reference. This line alone never
  changes the exit status.
- **B3 Diff failure.** The reference resolves and the comparison against it still fails →
  reported `[stale]` as B1, cause "git could not
  compare against it". `stale` returns 1.
- **B4 Hash reference, no git.** The reference is hash-shaped and git is unavailable in this
  tree (not a work tree, git absent, or git refusing the repository) → `[stale]`: cannot be
  evaluated without git; run `stale` inside the git work tree, or re-mark. `stale` returns 1.
- **B5 Unparseable reference.** The reference is neither hash-shaped nor an ISO UTC timestamp →
  `[stale]`: the reference, that it is neither, and the re-mark command. `stale` returns 1.
- **B6** `[ok] no analyzed area was modified …` is printed only when no area is stale AND none
  is unverifiable. The existing closing hint names `<entry> mark <path>` as B1 does.
- **B7** `mark`, when it records a git reference, prints one `[info]` line: the reference is the
  current HEAD; commit the `audit_plan.md` change as a new commit; amending, rebasing or
  squash-merging that commit orphans the reference, so re-mark on the integration branch after
  such a merge. A timestamp reference prints nothing new.

Cases: reference is an ancestor → output identical to today; timestamp references, absent
paths, confinement rejections, guide freshness, `--hybrid` → unchanged; `check` reports NOT
CLEAN whenever `stale` returns 1; the kb lens's `stale` keeps its `## claims` section, which
never moves the exit status.

Acceptance criteria:

- **AC1** mark → amend → reflog expire → gc → `stale` returns 1, names `mark src/`, prints no
  `[ok]` (probe P2b; regression test).
- **AC2** mark → amend, before gc → `stale` returns 0 and warns "not an ancestor" (P3).
- **AC3** mark → new commit → `stale` returns 0, no `[warn]`, `[ok]` printed (P4).
- **AC4** marked on a branch, squash-merged, branch deleted, fresh clone → `stale` returns 1 (P5).
- **AC5** depth-1 clone with a reference beyond the depth → rc 1 and a "shallow" hint (P6).
- **AC6** hash reference in a tree without git → rc 1 (P7).
- **AC7** unparseable reference in a git tree → rc 1 (P8).
- **AC8** `check` over an unverifiable row prints NOT CLEAN and returns 1 (P9).
- **AC9** `mark` with a git reference prints the B7 line.
- **AC10** a reference that resolves but cannot be compared (the comparison reports failure) →
  rc 1, no `[ok]` (regression test, comparison failure injected).
- **AC11** the three `sdlc_core.py` copies stay byte-identical (drift guard green); golden
  baselines unchanged; the full battery passes in all three distributions.


## Interface Contract

Trigger fired: the output and exit code of `stale`, `check` and `mark` are the surface an agent
and a CI pipeline act on. Idiom reused: the existing `[stale]`/`[warn]`/`[info]` prefixes and
the closing hint's re-mark command; no new prefix, flag or command. Flow per use case: UC1
`check` → staleness evaluation → git (resolve, ancestry, compare) → `[stale]` line + rc 1 →
`check: NOT CLEAN`. UC2 `stale` → git ancestry → `[warn]` line, rc unchanged; after the rewrite
reaches a clone or is pruned → UC1. UC3 `mark` → git HEAD → audit plan written → `[ok]` + `[info]`.

## Capability Ledger

- *Evaluate whether a recorded reference still identifies analyzed state* — **INADEQUATE**:
  `git_changed_since` (sdlc_core) collapses "missing", "diff failed" and exceptions into `None`,
  and nothing asks about ancestry. Designed as
  `git_ref_state(root, ref) -> "ancestor" | "orphan" | "missing" | "unknown"`, beside it in the
  core's git section. Mapping: `git cat-file -e <ref>^{commit}` non-zero → `missing`;
  `git merge-base --is-ancestor <ref> HEAD` 0 → `ancestor`, 1 → `orphan`, any other code →
  `unknown`; an exception (timeout, OS error) at either call → `unknown`. `unknown` prints no
  ancestry line and proceeds to the comparison; a comparison failure is B3. Consumer:
  `cmd_stale` only.
- *Tell whether the clone is shallow* — **MISSING** (searched: the core's git section —
  `git_available`, `git_head`, `git_has_changes`, `git_changed_since`; no shallow query).
  `git_is_shallow(root) -> bool`: `git rev-parse --is-shallow-repository` stdout equals `true`;
  any failure → `False`.
- *Name the running distribution's command* — **EXISTS**: `entry_script()` (sdlc_core). The
  existing closing hint hard-codes `sdlc_check.py`, wrong under mkt (`mkt_check.py`); every new
  line and that hint use `entry_script()`.
- *Record analyzed state* — **EXISTS**: `git_head` + `cmd_mark`; unchanged except B7.
- *Substitute a reference that survives the rewrite* — **rejected**, two forms considered:
  (a) durable extra state (a private ref under `refs/`, a commit/tree pair) — CI clones never
  receive it; (b) derive a substitute from `audit_plan.md`'s own history (the commit that
  introduced the row's reference string, which travels with every clone). (b) was the strongest
  alternative and is rejected because the substitute's tree is not the analyzed state: an amend
  can fold edits to the marked paths made after `mark`, and a squash commit carries the whole
  branch, so changes made after the analysis would be absorbed and the area reported fresh —
  the defect's own class (a false CLEAN), made harder to see. It also contradicts goal (1).

Guide question: no CURRENT guide covers the stale/mark internals; the component is small (two
commands, four helpers) and fully described here, so no comprehension guide is owed.

## Impact

Enumeration instrument: no symbol-graph index serves this repository (devPNT's MCP index
belongs to another project), so consumers were enumerated with `git grep -w` over `*.py`,
`*.js` and `*.json` in all three distributions; the independent design review re-ran it and
found the same set plus kb's `kb_cmd_check` (via `cmd_check`).

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | MODIFY | add `git_ref_state`, `git_is_shallow`; `cmd_stale` B1–B6; `cmd_mark` B7 |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_core.py` | MODIFY | shared spine — verbatim copy (drift guard) |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/sdlc_core.py` | MODIFY | shared spine — verbatim copy |
| `skills/agentic-sdlc-skill/scripts/test_audit_refs.py` + the kb and mkt copies | ADD | AC1–AC9 regression test; it runs git, so it cannot live in the zero-subprocess invariants battery |
| `skills/agentic-sdlc-skill/scripts/shared_files.py` + the kb and mkt copies | MODIFY | `scripts/test_audit_refs.py` added to `SHARED_FILES` |
| `…/scripts/shared_manifest.json` ×3 | MODIFY | regenerated by `shared_files.py --update` |
| `skills/agentic-sdlc-skill/templates.md`, `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` | MODIFY | the audit-plan `Reference` sentence gains the new-commit / re-mark-after-squash rule (mkt's template has no such sentence) |
| `CHANGELOG.md`, `distributions/kb-agentic-skill/CHANGELOG.md`, `distributions/mkt-agentic-sdlc/CHANGELOG.md` | MODIFY | `[Unreleased]` entry |
| `ai_docs/solutions/harness_stale_dangling_ref/probe.py` | ADD | executed claims P1–P9 |

Blast radius (consumers, by symbol):

- `cmd_stale` — core `main` (`stale`); core `cmd_check` (and through it kb `kb_cmd_check`); kb
  `kb_cmd_stale`. Tests: `test_skill_invariants.test_audit_plan_paths_confined` (confinement
  rows in a non-git temp tree, timestamp references: unchanged branch, rc 0 still);
  `test_golden_regression` `stale`/`check` in code and kb (frozen corpus, timestamp reference,
  non-git temp dir: unchanged; the closing hint's command name is `sdlc_check.py` under both, so
  the baselines are byte-identical); kb `test_kb_time_cycle`, `test_kb_graph`,
  `test_claim_ledger` CLI runs (non-git temp dirs, no hash references). No caller treats rc 1
  as a crash.
- `cmd_mark` — core `main` (`mark`); `test_audit_plan_paths_confined` (refusal path returns
  before any write; B7 prints after a successful write only).
- `git_changed_since` — `cmd_stale` only; signature and return unchanged.
- `git_head`, `entry_script` — unchanged; `entry_script` gains consumers in `cmd_stale`.

`data_at_rest_populations` — trigger 1 fires: the guarantee "this area is fresh" moves from
"assumed when unevaluable" to "evaluated, or failed".

| Existing population | Which regime covered it | What happens to it after | Who sees the difference |
|---|---|---|---|
| Rows whose reference was already pruned | none — skipped, rc 0 | rc 1 until re-marked | the developer at the next closure; a CI that runs `check`/`stale` |
| Rows whose reference is a local orphan, still in the object store | none | `[warn]`, rc unchanged; the row above once pruned or cloned | the developer |
| Rows marked on a branch later squash- or rebase-merged | none — skipped on every clone, rc 0 | rc 1 on every fresh clone until re-marked on the integration branch; a recurring re-mark per such merge | teams using those merge styles — the cost disclosed in the Ceremony budget |
| Rows checked in a shallow clone, reference beyond the depth | none — skipped, rc 0 | rc 1 with the shallow hint | a pipeline that runs `check`/`stale` on a shallow checkout |
| Hash references where git is unavailable (tarball, git missing, git refusing the repository as unsafe) | none — "not parseable", rc 0 | rc 1 naming the missing git | whoever runs `stale` outside a usable work tree, CI containers included |
| Rows with a hand-edited or empty reference | none — "not parseable", rc 0 | rc 1 with the re-mark command | the developer |
| Rows whose path is absent from a sparse or partial checkout but present in HEAD | none — "path does not exist", rc 0 | unchanged — **residual, declared**: evaluating it needs a tracked-in-HEAD query on a path the working tree does not hold, and no incident has been observed | a pipeline using sparse checkout |

## Security and Threat Model

- **T1 argument injection into git from document content.** `audit_plan.md` is document
  content; the reference reaches `git cat-file`, `git merge-base` and `git diff`. Eliminated by
  construction: the existing `[0-9a-fA-F]{7,40}` fullmatch precedes every git call that takes
  the reference, so no value beginning with `-` reaches argv; list-form `subprocess.run`, no
  shell. The new calls sit inside that guard.
- **T2 hang on a pathological repository.** Every new git call carries a bounded `timeout` like
  its neighbours; an exception maps to `unknown` (no ancestry claim). A comparison that times
  out on a very large or partial clone now fails closed (B3) where it used to pass silently —
  accepted: an unevaluated area is not a clean one.
- **T3 false CLEAN** (the defect itself) — answered by B1–B6 on the four paths probed.

## Action Plan

1. Probe P1–P9 red on the pre-change core (done — Diary).
2. Design review (independent) on this ANALYSIS; revise; re-review.
3. Core: helpers, `cmd_stale`, `cmd_mark`; copy to kb and mkt.
4. `test_audit_refs.py` + `SHARED_FILES`; copy; `shared_files.py --update` ×3.
5. Templates ×2, CHANGELOG ×3.
6. Probe green; full battery in all three distributions; `sdlc_check.py index`, `check`.
7. Closure review on the diff; REVIEW_LOG rows; status COMPLETED. Owner acceptance of the
   squash/rebase re-mark cost: see Diary.

## Test Strategy

- Regression: `test_audit_refs.py` (skips without git), AC1–AC10, in temp repositories with
  identity and signing pinned through `-c` flags; clones use `file://` so only reachable
  objects transfer (a plain-path clone hardlinks every object and would hide P5).
- Probe: `harness_stale_dangling_ref/probe.py` red on e5b7bc0's core, green after.
- Non-regression: `python -m unittest discover -s scripts -p "test_*.py"` in each of the three
  skill `scripts/` directories (golden corpus unchanged, drift guard green).

## Diary

- 2026-09-14 — Triage L3 (4+ files across three distributions, CLI exit-code contract).
  Router: `GUIDE_release.md` not matched (no release in scope). Standalone: devPNT's MCP
  bootstrap points at another project. Probe on the current core: P1, P2a, P4 green; P2b, P3
  RED. Design review round 1 (fresh subagent): FAIL — BLOCK squash/rebase workflows unpriced;
  WARNs: substitute-from-history alternative unruled, `git_ref_state` mapping unspecified,
  hard-coded `sdlc_check.py` wrong under mkt, the named mechanism also lives on the
  "not parseable" path, missing ACs (shallow, `check`), code names in the Functional Spec;
  CANNOT_VERIFY the amend provenance. All folded into this revision; probe extended to P5–P9,
  all RED on the current core (P5 first ran green because a plain-path clone hardlinks
  unreachable objects — fixed with `file://`).
- 2026-09-14 — Design review round 2 (same reviewer, scoped): **PASS**, four WARNs folded:
  N1 acceptance timing (below), N2 AC10 added (comparison failure injected), N3 sparse checkout
  declared as a residual, N4 shallow hint made additive and P6 asserts the exact hint.
  **Ceremony-cost acceptance (N1).** The owner's request for this unit states goal (1) as "an
  unresolvable ref must make `stale` fail (rc=1) … never skip it silently"; the squash/rebase
  population is that rule applied to a reference that never reached the clone, so the
  implementation proceeds on it. The recurring re-mark it implies for squash-merge teams was not
  named in that request, so it is put to the owner explicitly in the closure report; declining
  it would narrow B1 for never-fetched references only (one branch of `cmd_stale`), not undo the
  unit.
- 2026-09-14 — Implemented TDD: `test_audit_refs.py` 9/10 RED on the unchanged core (AC3 the
  control), GREEN after the core change; probe P1–P9 all green. Spine copied to kb and mkt,
  manifests regenerated (identical ×3). Batteries: code 212 OK, kb 398 OK, mkt 230 OK. Closure
  review (fresh subagent): **PASS** with 2 WARNs, both fixed — AC6 now asserts B4's own cause
  (a mutation disabling B4 had passed every test; re-run of that mutation now turns P7 red) and
  a test pins the ledger's `unknown` state; the REVIEW_LOG rows moved to the top of the
  newest-first table. Repository `check` stays NOT CLEAN on pre-existing stale areas only (no
  `[stale]` unverifiable line on this repo's own rows: all three hash references are ancestors
  of HEAD). No ADR: no architectural decision (a fail-closed rule inside an existing command).
  Owner acceptance of the squash/rebase re-mark cost: put to the owner in the closure report.
