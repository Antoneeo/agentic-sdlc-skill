---
id: F-028
feature: Mergeable documentation — several people on one project, in parallel
status: COMPLETED
level: L3
start_date: 2026-08-02
end_date: 2026-08-03
---
# Feature Analysis: Mergeable documentation

## Objective

`templates.md` §handoff registry states the registry is **"Parallel-safe by
construction"**. It is not, and the claim was never tested. Two workstreams opened
from a common base, each touching "only its own row", collide:

```
CONFLICT (content): ai_docs/audit/handoff.md          <- twice: the Date: header AND the row insert
CONFLICT (content): ai_docs/audit/reviews/REVIEW_LOG.md
```

Make the documents the methodology produces survive concurrent work on separate
branches: **merge without hand resolution and without silent loss.** Full
simultaneity is not the requirement (owner, 2026-08-02) — surviving the merge is.

The defect has two independent causes and both must go:

1. **A global field every writer touches.** `Date:` on line 2 of `handoff.md`
   guarantees a conflict on *every* concurrent write, regardless of how few rows
   each writer edits. Row-level ownership cannot save a file with a file-level field.
2. **A shared insertion point.** Rows appended at one place in one table are
   adjacent-line edits; git conflicts on them by construction.

## Feature Vision

**Precedent first** (`vision/rulings.md`, before any prose is interpreted).

| Row | Placement | Consequence |
|---|---|---|
| **r14** — *fixes a defect with purpose, actors and surface unchanged* → **exempt** | primary. The registry exists, claims parallel-safety, and does not have it | no admission needed, **if** purpose/actors/surface hold — they do: the generated view is column-identical to what ships today, at its unchanged path |
| **r11** — *consolidates duplicated internal machinery into one authored source* → **ADMIT** | the registry row carries `Branch` and `Next step`; `HANDOFF_[feature].md` carries `Branch:` and `## Next command`. Two authored copies of the same two fields, today | supports the design chosen below over any that keeps both |
| **r2** — *collects per-work state into one surface — stored, generated or derived on demand* → **REJECT** | **territory entered; disclosed.** The deciding fact: this proposal does **not** add the aggregation. It shipped in F-019 and was ruled there. What changes is where the bytes live | distinction line: *the output is byte-identical; only its storage moves.* If any column were added, r2 would bite |
| **r3** — *tells an agent or user what to work on next, in what order, or **by whom*** → **REJECT** | **the owner's original wording lands here.** A *registro degli accessi* that records **who holds** a workstream is "by whom" and is out | **excluded by design**: no holder, owner, assignee, lock or claim field. Stated here because omission resolves against the proposal |
| **r9** — *outputs the set of documents that are NOT current* → **REJECT** | not entered. The new validator finding is a correctness error about one named file, the same shape as the three alignment checks already shipped (`sdlc_core.py:1162/1171/1257`) | — |

**Goals advanced.** Goal 2 — *"Vision, design, plans, tests, guides and handoff stay
synchronized … so nothing load-bearing lives only in a transcript"*: a merge that
drops a workstream row loses exactly such state, and today nothing detects it.
Actor **Team lead needing governance**, whose `Good UX =` clause names the moment
verbatim — *"divergence from the declared intent surfaced **before the change is
merged**"*. Success Signal 2 (`check` CLEAN at closure) gains a case it currently
cannot see.

**Non-Goal 1 (work-management).** Territory entered, disclosed above (r2/r3). The
guard F-019 wrote stands unchanged and is re-applied here: inventory for lookup, no
assignment, no due dates, no execution ordering, no holder.

**Non-Goal 3 (no ceremony ratchet) — the budget, stated because it is owed.**

| Added | Removed |
|---|---|
| one `validate` ERROR: the generated registry is out of sync with its sources | the manual "remove the row at closure" step — closure already deletes `HANDOFF_[feature].md`, and deleting it *is* removing the row |
| **`HANDOFF_[feature].md` becomes unconditional for an OPEN workstream** (review round 1, BLOCK 3): today it is written only when there is volatile state, and a row generated from a file that may not exist is a row that vanishes | the duplicated `Branch`/`Next step` fields: one authored home instead of two |
| — | hand-resolution of a merge conflict on every concurrent handoff write |

Write count at closure is unchanged (one file touched either way), and **L1 is not
reached at all**: the handoff is an L3-closure / session-end trigger. The added row
above does not change the count either — a workstream that today writes one row in a
shared file tomorrow writes one file of its own — but it changes *which* file the
write trigger names, and pretending otherwise would be the budget dishonesty this
clause exists to prevent. Net cost still negative. No owner acceptance is being
requested under the budget clause; if a later review disagrees with that accounting,
it becomes an explicit ask.

**Non-Goal 4 (no coupling).** The fragment-directory idea is absorbed from
news-fragment tooling (towncrier, reno, scriv) as an **idea**. No format of theirs is
reproduced, read or taught. Counterfactual: if any of them changes its format
tomorrow, nothing here produces a different result.

**The user's guarantee.** The mechanism must work with **no VCS at all** — it is
files and a generator. `.gitattributes` (Action Plan B) is defense-in-depth only:
without it the outcome is today's outcome (a conflict you resolve by hand), never a
lost capability.

**Non-goals of this feature.** No lock, claim or lease protocol. No holder field. No
conflict-resolution automation beyond regeneration. No rename of existing paths.

## Use Cases / User Needs

- **Team lead needing governance** (Vision Actor 2) — two agents close two
  workstreams on two branches in the same week; both merges land without a human
  editing a table by hand, and neither closure erases the other's row.
- **Solo developer using an AI agent** (Vision Actor 1) — two worktrees on two
  features; after merging B, resuming A finds A's resume point intact. This is
  F-019's original promise, now actually true.
- **Adopter evaluating the paid layer** (Vision Actor 3) — unchanged: filesystem
  only, no service, and the same behaviour with devPNT absent.
- **A project already installed on 1.20.x** — upgrades and sees **no new error**:
  the check is opt-in by presence of the new sources, never a migration sweep
  (the F-019 lesson, T6 below).

## Capability Ledger

Architect pass run before the Impact. `audit/audit_plan.md` marks
`skills/agentic-sdlc-skill/` and `scripts/` ANALYZED, so the map is groundable here.

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| Record one open workstream's state without touching another writer's bytes | **INADEQUATE** | `ai_docs/audit/handoff.md` — one shared table plus one file-global `Date:` header (`templates.md`:370-400). Gap: both the header and the insertion point are shared | merge experiment, two workstreams from one base: 2 conflict hunks in one file. The template's "Parallel-safe by construction" is false as written |
| Gather per-document truth from many files into one view at a fixed path | **EXISTS** | `sdlc_core.py#list_guides` → `#build_guide_index` → `cmd_index` writes `reference/INDEX.md` (`sdlc_core.py:730-740`, `804-823`) | re-read `cmd_index`: globs `GUIDE_*.md`, builds, writes; the empty-stub branch shows the pattern already handles the zero case without special-casing the caller |
| Detect that a generated view drifted from its sources | **EXISTS** | `cmd_validate` (`sdlc_core.py:1162`, `1171`, `1257`) | re-read: `norm_text(read_text(x)) != norm_text(build_x(root))` → ERROR for all three generated documents. This is precisely what turns a badly-resolved merge conflict from permanent into visible |
| Hold one workstream's own state in its own file | **EXISTS** | `ai_docs/audit/HANDOFF_[feature].md` (`templates.md`:435-458) | re-read the template: it already carries `Branch:` and `## Next command` — the same two fields the registry row duplicates. Created on pause, **deleted at closure**, which is exactly when the row must disappear |
| Append a review record without colliding with a concurrent one | **INADEQUATE** | `ai_docs/audit/reviews/REVIEW_LOG.md` — shared table, every writer prepends at the same point | merge experiment: conflict. `merge=union` resolves it cleanly and is a **built-in** driver (no per-clone config) — verified: both rows survive, order irrelevant since rows are date-stamped |
| Keep a generated document out of the merge entirely | **MISSING — and ruled out** | — | tested `merge=ours`: **not** a built-in driver. `.gitattributes` alone silently does nothing; it needs `git config merge.ours.driver true` in **every clone**, and even then it leaves the file wrong (a row lost) until regenerated. Rejected: a mechanism requiring per-clone config cannot ship in a skill installed by strangers |
| Mark an audited area fresh without colliding | **EXISTS** | `cmd_mark` (`sdlc_core.py:1398`) — rewrites one row's Reference cell | rows for different areas are non-adjacent lines and merge clean; two marks of the *same* area is a genuine semantic conflict no format fixes |
| Migrate an existing project's documents to a new layout | **EXISTS** | `cmd_migrate` (`sdlc_core.py:1821`) | present and tested (`test_migrate.py`); not needed if no path is renamed — and none is |

## Impact

**Design in one line:** the registry's truth moves into the per-workstream file that
already exists — `audit/HANDOFF_[feature].md`, promoted from *optional volatile
logistics* to **the one authored home of that workstream's row** — and
`audit/handoff.md` becomes the **generated view at its unchanged path**, built and
verified by exactly the machinery that already builds and verifies the guide router.

Consequences that fall out for free: closure already deletes the per-feature file, so
the row disappears without a second edit; the `Date:` header is derived from the
sources, so no writer ever touches it; and two writers touching two workstreams touch
two files.

**Four things the generator must pin down, or the alignment check becomes the defect**
(review round 1 — a byte comparison is unforgiving, and each of these was left open):

1. **`Date:` is the newest date VALUE carried in the sources' own frontmatter**
   (`Updated:`), **never a filesystem timestamp.** Git does not preserve mtimes, so an
   mtime-derived header regenerates differently after every clone and `validate` would
   error on a tree nobody touched. This is the one reading that had to be excluded.
2. **Row order is a declared, stable sort** (by workstream id), like
   `build_guide_index`. Glob order differs across filesystems and would make the
   alignment check fail at random.
3. **Conversion is per project, not per row** — see T6, rewritten. The generator never
   writes a registry it cannot fully account for.
4. **The `≤ 20 lines` cap becomes a warning, not a truncation.** A generated view that
   silently drops the 21st workstream loses exactly the state this feature exists to
   keep; the cap survives as a signal that too much is open at once.

| Path | Change | Why |
|---|---|---|
| `skills/*/scripts/sdlc_core.py` ×3 | MODIFY | `list_workstreams()` + `build_registry()`; `cmd_index` writes `audit/handoff.md` when sources exist; `cmd_validate` alignment check, **gated on source presence** |
| `skills/*/SKILL.md` ×3 | MODIFY | Write Triggers: the registry row becomes "generated — never by hand"; the `HANDOFF_[feature]` row gains the frontmatter that feeds it, stays the only hand-written home, and **loses its "AND there is volatile resume state" condition** — an open workstream owes its file, or its row does not exist (round 1, BLOCK 3) |
| `skills/*/templates.md` ×3 | MODIFY | registry template → generated-header form; `HANDOFF_[feature].md` template gains registry frontmatter; **delete the false "Parallel-safe by construction" claim** (`templates.md`:372) and state what actually makes it safe; **restate the DRY boundary** at `templates.md`:437-440 — the file now always exists for an open workstream, so "Diary = the durable narrative" needs a sharper line than "created only when there is volatile state", which is what kept narrative out of it before |
| `skills/*/scripts/test_skill_invariants.py` ×3 | MODIFY | extend the existing `workstream_registry` invariant (`sdlc_core.py:234`) to assert the generated form + the migration clause |
| `skills/*/scripts/test_merge_safety.py` ×3 | ADD | the experiment becomes a regression test (see Test Strategy) |
| `scripts/init.js` ×3 | MODIFY | Plan B only: append the `.gitattributes` stanza, create-only, never clobbering a user's file |
| `ai_docs/audit/handoff.md` + `audit/HANDOFF_*.md` | MODIFY/ADD | dogfood: this repo's 6 open rows become 6 source files + the generated view |
| `ai_docs/README.md` | MODIFY | must-read #6: say the registry is generated |
| `CHANGELOG.md` | MODIFY | `[Unreleased]` |

**Blast radius (enumerated).**
- `ORIENT_DOCS` (`sdlc_core.py:370`) points at `audit/handoff.md`. **Path unchanged →
  no hook change**, the generated view flows through orientation exactly as today.
  Verified the same way F-019 verified it.
- `GENERATED_DOCS = {"features_history.md", "INDEX.md"}` (`sdlc_core.py:63`) excludes
  generated docs from manifest entries. `handoff.md` is not a canonical doc and is not
  in the manifest today, so the set is **not** extended — confirm during implementation
  rather than assume.
- The `Date:` freshness warning (`sdlc_core.py:1261-1273`) must keep firing: it moves
  from "someone remembered to bump a header" to "the newest source file's date",
  which makes it *more* honest, not less.
- devPNT/Hybrid: the ownership matrix says the handoff is **always filesystem**, both
  modes. Nothing in the seam changes.
- kb and mkt: the spine is byte-identical and drift-guarded, so all three carry it.

**Not in this unit, declared:** `strategic/architecture.md` `## Component Map` and
`audit/audit_plan.md`. Both are lower-frequency (closure-only, per-area) and their
realistic conflicts are **semantic** — two closures claiming the same capability
merge cleanly and are still wrong, which no storage layout fixes. `CHANGELOG.md` is
this repository's own release hygiene, not something the methodology produces for a
user. Silently narrowing scope is the anti-pattern; this is the scope stated.

## Security and Threat Model

Surfaces: filesystem only. The generated registry is emitted into agent context by
the SessionStart hook — an existing surface, same path, same truncation caps.

| Threat | Answer |
|---|---|
| **T1** — an agent hand-edits the generated `handoff.md`; the edit is lost at the next `index` | the `GENERATED … do not edit by hand` header (the form already used by three documents) plus the alignment ERROR, which fires *before* the loss: `check` is not CLEAN until the sources say the same thing |
| **T2** — a workstream file is deleted while the workstream is still open; its row vanishes silently | closure is the only step that deletes it, and the absence is visible at every session start (orientation reads the registry). Declared, not mechanically enforced — same posture as F-019's T2, and the same reason |
| **T3** — the generated `handoff.md` is committed, so it still conflicts at merge | true and accepted: resolution is **mechanical** (`index`), and `validate` refuses CLEAN until it matches. It stays committed because Signal 1 requires a cold agent given only `ai_docs/` to read it without running Python. `merge=union` is *not* applied here — interleaving two generated tables produces a plausible-looking wrong file, the worst outcome of the three |
| **T4** — two people edit the same workstream's file | a genuine semantic conflict. Nothing here fixes it, and nothing should pretend to |
| **T5** — glob collision: `handoff.md` matched by the `HANDOFF_*.md` source glob on a case-insensitive filesystem | the pattern requires the `_`, so `handoff.md` cannot match — but Windows is the development platform and this must be a **test**, not an argument |
| **T6** — an installed project upgrades and its hand-maintained `handoff.md` starts failing `check` | **the migration trap, and the one that would break every existing project.** The alignment check fires only when at least one source file carries registry frontmatter — opt-in by presence, mirroring `if guides:` in `cmd_index` (`sdlc_core.py`:806). A project with no sources sees byte-identical output to today's |
| **T8 — the mixed state eats the un-converted rows** (round 1, BLOCK 1) | **the same trap one step later, and it was invisible because T6 gated the CHECK and said nothing about the WRITE.** Lazy conversion means a real project sits with one source file and five hand-written rows; the next `index` — run at every closure — regenerates the registry from the one source and silently deletes the other five. Rule: **`index` refuses to write the registry while `handoff.md` carries rows no source accounts for**, naming them, and `check` says the same. Conversion is therefore per **project** (convert every row, once, when you first touch it), not per row. The alternative — merging generated rows with surviving hand-written ones — was rejected: it makes the file two truths at once, which is the shape that produced this feature |
| **T9 — the `Date:` header derived from a filesystem timestamp** (round 1, BLOCK 2) | git does not preserve mtimes, so an mtime-derived header regenerates differently in every fresh clone and the alignment ERROR fires on a tree nobody edited — a check that cries wolf gets disabled, taking the real finding with it. The header is the newest `Updated:` **value** written inside the sources. Tested by copying the fixture with fresh mtimes and asserting `check` stays CLEAN |
| **T7** — `.gitattributes` (Plan B) overwrites a user's own file | create-only; append the stanza if absent, never rewrite. Same discipline `init.js` already applies to protocol pointers |

## Action Plan

- [x] **A — the registry** (the certain, highest-frequency conflict): sources +
      generated view + alignment check gated on presence. Pin the four generator
      facts (Impact): `Date:` from the newest frontmatter **value**, stable sort by
      workstream id, refuse-on-unaccounted-rows, cap as a warning.
- [x] **B — REVIEW_LOG**: `.gitattributes` stanza `merge=union`, written create-only
      by `init`, plus the template note. Defense-in-depth; absent git, unchanged.
- [x] **C — migration clause**: Write Trigger row + template conversion. Lazy **per
      project** (T8): nothing is touched until the first write, and that write converts
      every row, because a half-converted registry is the one state that loses rows.
      Invariant asserts the clause exists (F-026 precedent: shipping a format change
      without one strands existing projects).
- [x] **D — dogfood**: this repo's 6 rows converted; `check` CLEAN.
- [x] **E — design review** (independent, before implementation) and **closure
      review** (on the diff), both logged.
- [x] **F — closure**: three distributions green, drift guard identical, `index`,
      `mark`, CHANGELOG.

## Test Strategy

- **The claim gets a test, not a sentence** — `test_merge_safety.py`: build a temp
  git repo, branch twice from one base, open one workstream on each, merge, assert
  **zero conflicted paths** and both rows present after regeneration. This is the
  test whose absence let a false claim ship in `templates.md`.
- **Mutation**: restore the shared-table registry → the merge test must fail with the
  observed symptom (conflict on `handoff.md`). A guard that cannot fail is not a guard.
- **Alignment**: hand-edit the generated registry → `check` reports the ERROR;
  `index` clears it.
- **Opt-in guard (T6)**: a fixture project with a hand-written `handoff.md` and no
  source files → `check` output byte-identical to today's. This is the regression
  that protects every installed project.
- **Mixed state (T8)**: one source file plus four hand-written rows → `index` writes
  **nothing** and names the four; the rows survive on disk. Mutation: let it write →
  the test must fail with the four rows gone, because silent loss is the failure mode
  and a guard that cannot observe it is decoration.
- **Fresh mtimes (T9)**: copy the fixture so every file's timestamp is now, regenerate
  → the same bytes, `check` CLEAN. Proves the header is a value and not a clock.
- **Determinism**: build the registry twice from the same tree, and from a shuffled
  glob order → byte-identical both times.
- **Case-sensitivity (T5)**: assert `handoff.md` is never collected as a source, run
  on the case-insensitive development filesystem.
- **Family**: full battery ×3, drift guard byte-identical, `npm pack` unchanged.

## Diary / Current State

**2026-08-02 — opened.** Standalone, devPNT off. `Level: L3 · router: no match`
(`reference/INDEX.md` carries only `GUIDE_release.md`).

Origin: the owner asked for *"un registro degli accessi per gestire correttamente
l'accesso di più persone allo stesso progetto anche in parallelo"*, then scoped it —
full simultaneity is not required; what is required is **documentation prepared so it
can be merged**. That scoping is what turned an access-control question into a
storage-layout one.

**The claim was tested before it was trusted.** Two workstreams, one base, one merge
→ `handoff.md` conflicts twice (the `Date:` header, then the row insert) and
`REVIEW_LOG.md` once. `templates.md` has said "Parallel-safe by construction" since
F-019; nothing ever exercised it. The second cause — a file-global field defeating
row-level ownership — is the one prose reasoning had missed entirely, and it is the
half that makes row-per-workstream insufficient on its own.

Three classic remedies were tested, not cited. Fragment-per-unit: clean, zero
configuration. `merge=union`: clean, built-in, but only sound where row order carries
no meaning. `merge=ours`: **fails silently** — not a built-in driver, needs per-clone
`git config`, and even configured leaves the file wrong until regenerated. That last
result is why the design regenerates rather than suppresses.

The architect pass then found that the product already owns almost everything this
needs: the many-files-to-one-view generator, the drift check that makes a
mis-resolved merge visible, and the per-workstream file itself — which already
duplicates two of the registry's fields and is already deleted at exactly the moment
the row must disappear. The unit is mostly **connecting existing components**, which
is why the ceremony budget comes out negative.

**2026-08-03 — paused, then design-reviewed.** Paused on 2026-08-02 by owner priority
in favour of F-029; resumed at the same point, which is the gate the plan names.

**Design review round 1 — FAIL, 5 findings (3 BLOCK), all folded above.** Declared
adversarial self-pass, since a separate reviewer was not available: independence is
reduced and this says so rather than claiming four eyes. Every claim was re-verified
against the source rather than against the ANALYSIS's own line numbers.

The three blocks share one root, and it is worth naming because it is the same root
as F-031's: **the design specified the good output and left unsaid which outputs must
exist, and when.**

- **BLOCK 1, the mixed state.** T6 gated the alignment *check* on source presence and
  said nothing about the *write*. With lazy per-row conversion, a real project sits
  with one source file and five hand-written rows, and the next `index` — which runs
  at every closure — regenerates the registry from the one source and deletes the
  other five. Silently, and in the file whose whole purpose is not losing them. Fixed
  by refusing to write a registry the sources cannot fully account for (T8), which
  makes conversion per project instead of per row.
- **BLOCK 2, `Date:` from "the newest source file".** Read as an mtime, it breaks
  every fresh clone: git does not preserve mtimes, the generated header differs from
  the committed one, and the alignment ERROR fires on a tree nobody touched. A check
  that cries wolf gets disabled, and it takes the real finding with it. Now pinned to
  the newest `Updated:` **value** inside the sources (T9), with the clone test.
- **BLOCK 3, the file that may not exist.** The row is generated from
  `HANDOFF_[feature].md`, whose write trigger is *conditional* on volatile state
  (`templates.md`:441, "created only when a session pauses the feature WITH volatile
  state"). A workstream with none — F-015 and F-028 in this very registry — would
  generate no row at all. The trigger becomes unconditional for an OPEN workstream,
  the ceremony budget now discloses that as an addition instead of listing only
  removals, and the DRY boundary at `templates.md`:437-440 gets restated: what kept
  narrative out of that file was its rarity, and the rarity is what just went away.
- WARN 4 (row order must be a declared stable sort — a byte comparison against a glob
  order is a coin flip across filesystems) and WARN 5 (the `≤ 20 lines` cap becomes a
  warning; a generator that truncates loses the 21st workstream) folded the same way.

Dismissed after checking: T5's glob collision argument holds (`HANDOFF_*.md` requires
the underscore, so `handoff.md` cannot match even case-insensitively) — and the design
already demands a test rather than resting on the argument, which is the right posture.
`GENERATED_DOCS` (`sdlc_core.py`:63) indeed needs no extension: `handoff.md` lives
under `audit/` and is not a canonical doc.

**Round 2 — PASS, verification only.** All five closed, no new contradiction: the
Vision analysis is unaffected (no column added, no holder field, the output still
byte-identical to today's at an unchanged path), and the budget stays net-negative
now that its addition is written down.

**2026-08-03 — implemented and closed.** A–F done. Batteries 159/237/177 OK (the shared
`test_merge_safety.py` is 19 of them), drift guard identical, `npm pack` unchanged
(22/23/21), `check` CLEAN. Versions prepared: code 1.21.0, kb 1.4.0, mkt 0.4.0.

**What the closure review caught, and it was the important one.** The marketing lens has
its **own** `cmd_index`/`run_validate` — `mkt_check.py` never calls the spine's — so the
doctrine I had just written into its `SKILL.md` ("generated by `mkt_check.py index`") was
**false there**: `index` would not have written the registry and `validate` would not have
checked it. Shipping that is the doctrine-contradicted-by-the-machinery class, recurring
inside the fix for a different instance of itself. Wired explicitly, with a smoke test
through the real entry point. Its smaller sibling came out of the same look: the
generated header hardcoded `sdlc_check.py`, so a marketing user was told to run a command
their distribution does not ship — the header now derives the name from the entry point
(`entry_script()`, declared and never read from `sys.argv`, because the generated bytes
must not depend on how the command was invoked).

**One thing the design promised that the implementation had to correct.** The Test
Strategy said "assert zero conflicted paths". That cannot hold: the generated registry is
committed (Signal 1 — a cold agent must read it without running Python), so both branches
regenerate it and it CAN conflict, exactly as T3 already accepted. The honest promise, and
what the test asserts: **only the generated view may conflict, the authored sources never
do, resolution is mechanical (`index`), and no workstream state is lost.** That is what
the owner asked for — merge without hand resolution and without silent loss — and it is
the promise the battery can actually keep.

**Two gaps in my own tests, found by mutating rather than by reading.** The order test
passed with the sort removed (glob order happened to agree with it) and the alignment
error was never exercised at all. Both fixed, and every guard now has a mutation that
turns it red. Added beyond the plan: a warning when two files claim one workstream — the
collision this design does NOT fix (T4), which would otherwise have shown up as two
identical-looking rows and nothing else.

**Dogfood.** This repository's registry is now generated: six sources, `project_notes.md`,
and four closed rows retired by hand — because `index` refused to write until they were
accounted for. The guard fired on its own repository the first time it ran, which is the
only demonstration worth having.

Open: publication of the three packages (owner's 2FA) and the push+tag.
