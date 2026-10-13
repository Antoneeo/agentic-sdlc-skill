---
id: F-066
feature: Merge review brief and human E2E test script at every L3
status: COMPLETED
level: L3
start_date: 2026-10-12
end_date: 2026-10-12
domain: code
---
# Feature Analysis: Merge review brief and human E2E test script

## Objective

Integrators reviewing an L3 pull request ask (owner, 2026-10-12) whether to review
every change under `ai_docs`: they get an ANALYSIS, a REVIEW_LOG row and a raw diff,
and nothing says which part is theirs to judge.

Measured on the real F-065 merge (`git diff --numstat 1b156b5^ 1b156b5`): 45 files,
1,478 changed lines; 13 files / 698 lines under `ai_docs/`, of which **370 lines
(53%) are generated** (`memory/INDEX.md` 368, `INDEX.md` 1, `features_history.md` 1)
and need no human reading. Nothing in the diff says so.

Deliver, **mandatory at every L3 closure, no opt-out** (owner: "Solo L3"; cost
accepted, §Feature Vision):

1. `MERGE_REVIEW_[feature].md` — integrator, before merge: what to review, what
   was verified by which gate, what only a human can judge.
2. `E2E_TEST_[feature].md` — human testers, after merge in staging (owner: "Dopo il
   merge (staging)"); **always** regression scenarios (owner: "serve anche nel caso
   in cui non sia osservabile per verificare che non ci siano regressioni").
3. `sdlc_check.py review-map` — classes every changed file, so the map is produced.

## Feature Vision

**Precedent first** (`vision/rulings.md`). No row answers "prepares, per change,
what an integrator must judge before merge and what a tester must verify after it".
Distinction lines against the nearest rows:
- r3 (what to work on next / order / by whom, REJECT): the map orders reading
  *inside one approved change*, which Non-Goal 1 carves out ("Sequencing the steps
  inside one approved change is not this"); the E2E script names no tester, assigns
  nothing, orders no units of work.
- r2 / r9 (per-document state aggregated; selection by state): the map classifies
  the files of one diff by *kind*, never by document state.
- r22 (aggregate over closed review events): the brief cites this change's rows only.

→ **MISSING → proposed r25: ADMIT**, ruled by the owner at closure, on two bases:
- `MERGE_REVIEW` + `review-map` → Goal "make divergence visible … **again before
  merge**" and the Team-lead UX "divergence … surfaced before the change is merged".
- `E2E_TEST` → Goal "keep understanding durable — Vision, design, plans, **tests**
  … stay synchronized … so nothing load-bearing lives only in a transcript": the
  human verification of a change is derived from its design and committed with it,
  instead of living in a tester's head. It does not claim the before-merge Goal.

Vision `project_vision.md` is APPROVED (v8); no amendment. Actor: the **Team lead
needing governance** — as integrator (UC1) and as owner of post-merge verification
(UC2). Human testers are readers the Team lead hands the script to, not a Vision
actor; naming them one is a Vision amendment, not proposed here.

**Ceremony budget** (Non-Goal "No ceremony ratchet"): two mandatory L3 artifacts
and one closure step, nothing removed, L1/L2 untouched. Recurring per L3: the agent
writes ~1–2 pages per document from material it has and runs one ~3 s command;
the integrator reads one page and skips GENERATED/EVIDENCE (53% of `ai_docs/` lines
on F-065). Doctrine bytes go in the Diary; the owner accepted the cost (2026-10-12,
"Accetto, costo dichiarato") and confirms the figures before closure (r18, r24).

Non-goals: no record of who tested what or when (Non-Goal 1); no PR-platform format
or attribute (Non-Goal "no coupling" — the PR description only links the brief);
nothing at L1/L2; code lens only.

Success signals: the F-065 replay classifies its 370 generated lines GENERATED; this
feature's own closure ships both documents (AC7); an integrator using the brief does
not need to ask whether to review `ai_docs/`.

## Use Cases / User Needs

- **UC1 — Integrator decides a merge** (Team lead). Opens `MERGE_REVIEW_[feature].md`
  and learns from one page what the change is for, which files to review, which
  claims were verified by which gate, and which judgements remain theirs; decides
  the merge. Traces to: "divergence visible … again before merge".
- **UC2 — Team lead hands post-merge verification to testers** (Team lead). Gives
  `E2E_TEST_[feature].md` to human testers, who run it in staging with no design
  document open, each scenario carrying its observable expectation; regressions are
  covered even when the change has no visible behavior. Traces to: "keep
  understanding durable … tests … nothing load-bearing lives only in a transcript".
- **UC3 — Agent closes an L3** (Solo developer using an AI agent; Team lead). Writes
  both documents from the ANALYSIS, the REVIEW_LOG and the test evidence, runs
  `review-map` last, commits all with the change. Traces to: the same durability Goal.

Grounding: EXISTS — ANALYSIS, REVIEW_LOG, `sdlc_check.py`, `index`, `check`, `mark`,
the ANALYSIS sections, design/closure review. NEW — the two documents, `review-map`,
its four classes. METAPHOR — none ("pull request", "staging": the user's process words).

## Functional Spec

**`review-map`**
1. Lists every path that differs between the merge-base of the base ref (default
   `main`) and the working tree — committed, staged, unstaged, untracked — so a map
   taken as the last closure step matches what the PR will contain.
2. Each path gets one class and its instruction:
   - GENERATED — a file the project's `index` rewrites in this project (not
     judged by name or marker), plus `solutions/SHADOW_*` mirrors. "Skip; a CLEAN
     `check` proves it matches its sources." A hand-written file at a generated
     name, in a project where `index` does not write it, is not GENERATED.
   - EVIDENCE — `audit/reviews/**`, `audit/HANDOFF_*`, `solutions/harness_*/**`.
     "Spot-check that the verdicts the brief cites exist; do not re-review."
   - DESIGN — every other path under the docs root. "The reference the code is
     checked against. Read the changed parts; whether each was design-reviewed is
     stated in the brief's verification section."
   - REVIEW — every path outside the docs root. "Review."
3. Output: one markdown table (path, status, +/− lines, class, instruction), rows
   ordered REVIEW, DESIGN, EVIDENCE, GENERATED, then per-class file and line totals.
   Paths are relative to the repository top level.
4. Cases: no change → "no changes against <base>", success. Not a git repository, or
   base unresolvable → one error line naming `--base`, failure. A base starting with
   `-` → refused, failure. A rename shows the new path with status R. A binary file
   shows `bin` for lines. If the project's `index`
   fails, `review-map` prints its error and fails — never a map without GENERATED. A file name containing `|` or control characters is
   escaped so the table stays one row per file.
5. Writes nothing in the project.

**The documents**
6. `MERGE_REVIEW` contains: purpose and the Vision benefit it serves (cited, not
   copied); the review map; **already verified** — each gate with its REVIEW_LOG row,
   verdict and tier, which docs-root parts that review covered, and each test command
   with result and the commit it ran on; **your judgement** — deviations from the
   approved design, accepted residual risks, open CANNOT VERIFY items, declared
   assumptions, each "none" stated explicitly; **merge notes** — generated files
   regenerated never hand-merged, migrations/config, post-merge steps.
7. `E2E_TEST` contains: what changed in user terms; environment and preconditions
   **by reference only** — never a credential, token or secret URL; new-behavior
   scenarios, one per acceptance criterion a human can observe (none → one line
   saying the change has no observable behavior change); regression scenarios,
   always, derived from the consumers and existing surfaces the change touches;
   what automated tests already cover. Each scenario: steps, expected observable
   result, an empty result cell for the tester's copy — the skill neither requires
   nor reads results back. No tester names, no assignment, no ordering across changes.
8. Order at closure: `E2E_TEST` before the closure review (in the reviewed diff);
   `MERGE_REVIEW` after it, carrying only citations; then `index`, `review-map`, the
   table pasted into the brief, and `index` again (the brief's catalog hash changed;
   the file set does not; counts are as of the run).

**Acceptance criteria**
- AC1 — on the F-065 change set, `INDEX.md`, `memory/INDEX.md` and
  `strategic/features_history.md` are GENERATED; `REVIEW_LOG.md` and
  `harness_review_mandate/*` EVIDENCE; the ANALYSIS and the ADR DESIGN; `skills/**`
  and `distributions/**` REVIEW.
- AC2 — GENERATED equals the set `index` writes in that project: a project with
  `topics/`, `corpus/` and a HANDOFF source yields all seven outputs; one with a
  hand-written `handoff.md` and no HANDOFF source does not class it GENERATED.
- AC3 — committed, staged, unstaged and untracked changes all appear.
- AC4 — `--base -x`, an unknown base and a non-git directory each fail with the
  error line.
- AC5 — rename, binary and no-change cases behave as FS4.
- AC6 — a file name with `|` and a newline yields one escaped row.
- AC7 — this feature's closure ships both documents, written to the templates.
- AC8 — `--help` lists `review-map`.

## Interface Contract

Surfaces: (a) CLI `sdlc_check.py review-map [--base REF] [--root DIR] [--docs-dir NAME]`
(agent at closure, or integrator); (b) `MERGE_REVIEW` (integrator); (c) `E2E_TEST`
(testers the Team lead hands it to). Idioms reused: `--root`/`--docs-dir` like `stale`;
`[ERROR]` line + non-zero exit; markdown tables like the generated indexes;
`solutions/[KIND]_[feature].md` naming like ANALYSIS/SPIKE/PLAN.

Flow (UC3 → UC1 → UC2): order of FS8; inside `review-map` the code-lens entry point
asks git for the change set, runs its own `index` on a throwaway docs-root copy to
learn the generated set, classifies and prints; the agent pastes the table and
commits; the integrator reads the brief and merges; the Team lead hands `E2E_TEST`
to testers in staging.

Feedback: the table and totals; the "no changes" line; or an `[ERROR]` line with a
non-zero exit.

Constraints touched: `--help` is answered by the knowledge overlay, which lists only
its own commands — the entry point must answer `review-map` before forwarding and add
its line to the help output, or the command is invisible. The project root may sit
below the git top level (this repo contains `sdlc-test-project/ai_docs`): the docs
root is resolved from `--root`, paths from git are made relative to the top level,
and only paths under the resolved docs root take docs classes.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| know which docs-root files are generated | INADEQUATE | `sdlc_core.GENERATED_DOCS` (name filter `{features_history.md, INDEX.md}` used to exclude names from the manifest) and the marker regex (`registry_conversion_blockers`, `knowledge.KB_GENERATED_RE`). Gap: a name filter matches any `INDEX.md`, including hand-written ones, and misses `audit/handoff.md`; the marker misses `memory/INDEX.md` | probe `harness_merge_review/probe_generated.py`: `index` wrote 5 files; marker detection missed `memory/INDEX.md` (A HOLDS; `--negate` red run FAILS) |
| list a change set with status and line counts | INADEQUATE | `sdlc_core.git_changed_since(root, ref, rel)` returns names only | re-read: `git diff --name-only` + `ls-files --others`; no status, numstat, renames |
| resolve the docs root | EXISTS | `sdlc_core.find_project_root` / `docs_dir()` | used by every command |
| classify a change set for review | MISSING | — | grep -i `review-map\|merge review\|reviewer brief\|classify` over `skills/`: 7 hits, read — all triage (`classify the request`, `reclassify`), none about a change set |
| brief and E2E documents | MISSING | — | grep `MERGE_REVIEW\|E2E\|end-to-end\|tester` over `skills/`, `ai_docs/solutions/ANALYSIS_*`: 4 hits, read — dogfood trials and review notes, no document for integrators or testers |

Generated detection, weighed: extending `GENERATED_DOCS` keeps one core list but
changes manifest exclusion in four distributions and stays a list every new writer
must remember; the marker is already wrong (`memory/INDEX.md`); **running the
project's own `index` on a throwaway copy** costs ~1.4 s (measured: 4.7 MB, 436
files) and is the only answer that cannot drift from the writers. It wins.

New component **review map** (code-lens entry point), contract: "given a base ref,
list every changed path with one class and its instruction". It names no feature.

## Impact

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` | MODIFY | `main` answers `review-map` and appends its help line before `knowledge.main`; adds `_changes`, `_generated_set`, `classify_path`, `table_cell`, `cmd_review_map` |
| `skills/agentic-sdlc-skill/scripts/test_review_map.py` | ADD | AC1–AC6, AC8 on temp git repos |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | two template sections |
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | Write Triggers: two rows; Phase 5: one bullet (order of FS8) |
| `skills/agentic-sdlc-skill/hybrid.md` | MODIFY | ownership matrix row: always filesystem |
| `README.md` | MODIFY | the closure description names the two documents (audit-plan row 9 duty) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | MODIFY | derived document for code-lens closure (audit-plan row 9) |
| `CHANGELOG.md` | MODIFY | Unreleased entry |
| `ai_docs/vision/rulings.md` | MODIFY at closure | r25 on the owner's ruling |
| `ai_docs/strategic/architecture.md` (`## Component Map`), `existing_features.md` | MODIFY at closure | new component; feature catalog |
| `ai_docs/audit/audit_plan.md` | `mark` at closure, last step | audit-plan row 9 |

Blast radius of `sdlc_check.main`: in-process — `__main__`, `test_remind.py`
(`sdlc_core.entry_script()` + `mod.main`), `entry_point.load()` in
`test_skill_invariants`; subprocess — grep `sdlc_check` over `scripts/test_*.py`:
golden 5, session_start 10, invariants 5, project_memory 1, drift 1, plan 1, plus
the SessionStart/remind hooks. Only `argv[0]` in `review-map`/`-h`/`--help` changes
path; no test asserts `--help` output (grep). Shared files are untouched: no
distribution sync. Noted, out of scope: this repo's byte-identical `distributions/`
copies (540 of F-065's lines) class REVIEW.

Populations at rest: triggers evaluated — read-time→write-time: no; no-migration
constraint: yes — the COMPLETED analyses get no retroactive brief (already merged,
nothing to review); new wire format: no; redact/mask/filter: no. Residual: none
visible to any actor.

## Security and Threat Model

Surfaces: command-line input (`--base`), subprocess (git, the entry's own `index`),
filesystem read and a temp-dir write.
- T1 option injection via `--base`: refuse a leading `-`; resolve with `git rev-parse
  --verify --quiet <ref>^{commit}`; list-form `subprocess.run`, no shell (AC4).
- T2 table injection by hostile file names: escape `|`, replace control characters (AC6).
- T3 writes: only a `tempfile` directory removed on exit (FS5).
- T4 a brief misstating verification: every "already verified" line cites its
  REVIEW_LOG row and command; the claim-to-evidence rule (SKILL §5) applies; the brief
  is written after the closure review and carries no unreviewed claim of its own.
- T5 secrets in committed documents: E2E preconditions by reference only (FS7);
  the template says so.

## Action Plan

- [ ] Scoped re-review; owner approves the design.
- [ ] RED `test_review_map.py`; GREEN `review-map`; doctrine files; bytes → Diary.
- [ ] Battery + `check`; closure in the FS8 order; r25, Component Map,
      existing_features; `mark` last.

## Test Strategy

`test_review_map.py` (AAA, a temp git repo per test) covers AC1–AC6 and AC8; the full
battery `python -m unittest discover -s scripts -p "test_*.py"` and `check` CLEAN cover
regressions; AC7 by the closure review; probes: `harness_merge_review/`.

## Diary / Current State

- 2026-10-12 — elicitation (4 questions); probes; design review FAIL → PASS (rounds).
- 2026-10-12 — owner approved the design. RED 11/11 → GREEN; battery 245 OK.
  Doctrine cost (UTF-8 LF bytes): SKILL.md +1184 (always read), templates.md +3258
  (read on trigger), hybrid.md +370 (after the closure-review fixes, owner re-confirmed); the hybrid moved-block digest re-stamped as
  F-065 did. AC4 extended to a failing `index` (test_failing_index_fails_closed).
  Owner confirmed this cost and ruled r25 ADMIT (2026-10-12). Closure review next.
