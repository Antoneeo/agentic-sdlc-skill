# Changelog

## [0.4.6] - 2026-08-06

### Changed
- **Shared-spine sync: review-driven corrections + reviewer honesty (ACTIVE in this lens).**
  The shared `review.md` gains the scoped re-review discipline — a fix made in response to a
  finding is unreviewed work and gets a correction-scoped re-review with per-finding verdicts
  before PASS — plus the `CANNOT VERIFY` reporting duty and the no-pre-judging rule. Unlike
  prior spine syncs these are NOT inert here: reviews of marketing artifacts inherit the
  correction discipline directly.

## [0.4.5] - 2026-08-06

### Changed
- **Shared-spine sync: Functional Spec clause (inert in this lens).** The shared
  `review.md` gains the code lens's Functional Spec findings (absence on behavior change,
  Solution-leakage inside the spec, uncovered cases, acceptance criteria without tests).
  The mkt lens defines no `## Functional Spec` template section, so the clause stays inert
  here — spine parity only.

## [0.4.4] - 2026-08-05

### Changed
- **Shared-spine sync: use-case grounding clause (inert in this lens).** The shared `review.md`
  gains the code lens's use-case-grounding finding — a product name in no EXISTS/NEW/METAPHOR
  bucket, or a use-case tracing to no Vision benefit. The mkt lens defines no `## Use Cases`
  template section, so the clause stays inert here — spine parity only.

## [0.4.3] - 2026-08-05

### Changed
- **Shared-spine sync: Interface Contract rename (inert in this lens).** The shared `review.md`
  Interaction Contract clause is renamed to **Interface Contract** and gains the code lens's
  evolved checks (responsibility-level flow, solution-leakage, universal feedback); the
  `interaction_contract` capability key is unchanged. The mkt lens defines no such template
  section, so the clause stays inert here — spine parity only.

## [0.4.2] - 2026-08-05

### Fixed
- **Registry recognition hard-coded to one entry point.** The workstream-registry
  header is written with `entry_script()` (here: `mkt_check.py`) but was recognized
  as "already ours" only by the literal `sdlc_check.py`: a registry this very lens
  generated was treated as legacy and re-checked for conversion blockers on every
  run. Recognition now matches the generated marker for any family entry point.
- **Battery isolation.** The marketing battery failed 13+1 under full unittest
  discovery (and passed module-by-module): `test_merge_safety` built `ai_docs`
  fixtures while the mkt overlay import had flipped the default docs root to
  `mkt_docs`. The battery now pins its docs root in `setUpModule`; full discovery
  is green.

### Changed
- **Shared-spine sync with code 1.22.0 (Interaction Contract, F-032).** The shared
  `review.md` gains the Interaction Contract conformance clause and the shared core
  registers the `interaction_contract` capability — both **inert in this lens**: the
  clause is keyed on the lens whose template defines the section (the code lens),
  mkt claims no such capability, and no mkt workflow gains any new step or artifact.

## [0.4.1] - 2026-08-03

### Added
- **`version:` in every `SKILL.md` frontmatter.** An installed skill carries no
  `package.json` and no `gemini-extension.json` — only doctrine and scripts — so nothing
  in it said which build it was. Answering "is that fix in your copy?" took `npm view`
  plus a shasum comparison; from a user's side it was unanswerable. Now the first thing
  in the operating contract says it.
- **A battery invariant asserting every bump point agrees** (`SKILL.md` ↔ `package.json`
  ↔ `gemini-extension.json`). A hand-maintained version string rots, and this repository
  has the scar: the third bump point was skipped for two whole releases with nothing to
  catch it. The fourth arrives with its guard attached, and `GUIDE_release.md` step 1
  now says FOUR.

## [0.4.0] - 2026-08-03

F-028 — several people on one project. `templates.md` had claimed the workstream
registry was "Parallel-safe by construction" since F-019, and nothing had ever exercised
it. Two workstreams opened from one base conflict **twice in one file**: on the row
insert, and on the file-global `Date:` header. Row-level ownership cannot save a file
that has a file-level field.

### Changed
- **`audit/handoff.md` is now GENERATED** from one `HANDOFF_[unit].md` per open
  workstream, whose frontmatter IS the row. Two writers on two workstreams touch two
  different files, and the `Date:` header is derived — from the newest `updated:` VALUE
  in the sources, never a filesystem timestamp (git does not preserve mtimes, and an
  mtime-derived header would make the file regenerate differently in every fresh clone).
- **`HANDOFF_[unit].md` is now written for every OPEN workstream**, with or without
  volatile state — no file, no row. It still carries the resume logistics, and deleting
  it at closure *is* what removes the row. The DRY boundary against the ANALYSIS Diary
  is restated in the template, because what used to keep narrative out of that file was
  its rarity, and the rarity is gone.
- Project-wide notes move to their own source, `audit/project_notes.md`, so generating
  the registry cannot destroy notes that belong to no workstream.

### Added
- **`validate` errors when the registry disagrees with its sources** — which is what
  turns a merge resolved carelessly from permanent into loud. Resolution is mechanical:
  re-run `index`. The generated view can still conflict; the authored truth does not.
- **`index` refuses to write while anything in the file is unaccounted for**, and names
  it. Converting one row at a time is the state that loses the others, so conversion is
  per project. A project with no sources is untouched and sees no new finding.
- **`init` writes a `.gitattributes` stanza** giving the append-only review log
  `merge=union` — a **built-in** driver, unlike `merge=ours`, which silently does
  nothing until every clone runs `git config` and leaves the file wrong even then.
  Create-only; a user's own `.gitattributes` is never clobbered.
- `scripts/test_merge_safety.py` (shared, ×3): the experiment that found the defect,
  kept as a regression test — two workstreams from one base, merged, with the assertion
  that only the generated view may conflict and that regenerating loses no state. Plus
  the mixed-state, fresh-mtime, ordering, cap and duplicate-id guards, each
  mutation-verified.
- A warning when two files claim the same workstream: the collision this design does
  **not** fix (two people opening the same work under two names) must not pass as two
  ordinary rows.

The mechanism is files and a generator: **it works with no VCS at all.** The
`.gitattributes` stanza is defence in depth — without it the outcome is today's, one
conflict resolved by hand, never a lost row.

### Upgrading
Nothing happens until you convert: with no `HANDOFF_*.md` sources, `index` and
`validate` behave exactly as before. When you convert, convert the whole registry at
once — `index` will tell you what is still unaccounted for.

## 0.3.1 — 2026-08-02

### Fixed
- **The multi-lens routing note announced this skill as the code lens.** `init.js` wrote
  the row for the CURRENT lens as a hardcoded literal copied from the code distribution,
  so a project initialised with `mkt-sdlc-init` listed `agentic-sdlc` twice and never
  named `mkt-agentic-sdlc`. Both the self row and the sibling table are now derived from
  the shared `routing.md` lens table. Found by a cold-agent field test.
- **`FACT` was the way past the evidence rule.** `BENCHMARK` owes a source URL and
  `ASSUMPTION` a range; `FACT` owed nothing, so a researched observation classed FACT
  with source "see research/VOC.md" entered the ledger unsourced. `mkt_check.py` now
  errors on a FACT with no source, or one pointing at a document of the engagement,
  while exempting a cell that names the client as origin. `research.md` states the two
  legal origins.
- `review.md` (shared spine): a review verdict travels as the reviewer's final output.

## 0.3.0 — 2026-08-01

- **One shared core, three lenses.** This skill is now built from the family's spine
  instead of a copy of it: triage, the Vision gate, the review gates, the guide router,
  question discipline and the validator core are byte-identical with
  `@antoneeo/agentic-sdlc-skill` and `@antoneeo/kb-agentic-skill`, and a drift guard
  verifies it on every build. `routing.md` decides which lens owns a unit of work when
  more than one is installed.
- `mkt_check.py` forwards every spine subcommand it does not intercept by iterating the
  spine's parser — the hand-copied command tuple used to drop `migrate` while `SKILL.md`
  documented it.

## 0.2.1 — 2026-07-09

- **Install DX fix**: README + the generated project protocol pointer no longer present `mkt-sdlc-install-skill` as a required second step. `npm i -g` alone installs the skill (the `postinstall` runs the installer); the manual command is documented as a fallback via `npx mkt-sdlc-install-skill` for setups that block install scripts, with an explicit note that the bare command is only on PATH after a global install. Prevents the "command not recognized" error after a local `npm i`.

## 0.2.0 — 2026-07-09 (v1.0 hardening)

- **Deterministic doctrine gate**: `scripts/test_skill_invariants.py` asserts the load-bearing invariants (three guarantees, review red-flags R1/R11b/R15, elicitation rules, research URL rule, parseable template tokens, sales-led funnel guidance, support-file wiring). Fails on a real regression.
- **Opt-in behavioral eval layer**: `evals/run_behavioral.py` (zero-LLM driver) + 6 scenarios (triage/escalation, owned-facts elicitation, no-number-without-ledger, swap-test enforced, low-cost-trap flagged, no-guaranteed-success). Mirrors the sibling skill.
- **Contrast validation (B2B sales-led)**: second synthetic eval on a business unlike the first — the Vision Alignment / amendment discipline caught and held a deliberate vision-divergence (self-serve tier) instead of absorbing it.
- **Calibration from the contrast run**: sales-led/B2B funnel guidance (funnel output = qualified demos not closed customers; separate pipeline build-up table; closed-won lag) in `frameworks.md` + `templates.md`; B2B firmographic-ICP + buying-committee variant in `templates.md`.
- ENFORCEMENT.md §5/§6 updated to run both deterministic batteries + the behavioral layer.

## 0.1.0 — 2026-07-09

Initial release.

- Operating contract `SKILL.md`: Marketing Values, Rule Zero engagement triage (E1/E2/E3/Spike), dual operating modes (Standalone `mkt_docs/`, Hybrid devPNT), E3 nine-phase SOSTAC workflow with user gates, adversarial review gates and mechanical validation.
- Support files: `frameworks.md` (framework selection guide), `elicitation.md` (question waves, only-facts-you-own rule), `research.md` (research playbook + evidence ledger discipline), `templates.md` (all artifact templates), `review.md` (CMO review discipline + marketing red flags), `ENFORCEMENT.md`.
- Mechanical validator `scripts/mkt_check.py`: `check`, `validate`, `ledger`, `budget`, `funnel`, `trace`, `index`.
- npm packaging: `mkt-sdlc-init` (project scaffold), `mkt-sdlc-install-skill` (multi-client skill install: Claude Code, Gemini CLI, Codex, Google Antigravity).

## [0.3.0] - 2026-08-01

### One shared core, three lenses

This release is the consolidation: `agentic-sdlc` (code), `kb-agentic` (knowledge)
and `mkt-agentic-sdlc` (marketing) are now built from ONE spine instead of being
copies of one another. They can be installed side by side, they share a single
`ai_docs/` tree, and the agent has a stated test for which one governs a given
piece of work.

**Nothing changes for an existing project.** No `default_domain` line resolves to
`code`; no `domain:` field means no new column and no new check; the router is
never read unless a sibling lens is installed, and never at all on a trivial task.
A frozen corpus plus a recorded transcript of every command and exit code
(`test_golden_regression.py`) is what makes that a checkable claim rather than a
promise.

### Added
- `routing.md` — the domain router: which lens owns this unit of work. Read only
  when a sibling lens is installed; fails open to the loaded lens.
- Optional `domain:` and `checks:` on an artifact, `default_domain:` in the docs
  root README. All optional; a single-domain project writes none of them.
- **Portable checks**: a document owned by one domain can import another domain's
  checks by name. Imported checks may only ADD findings, never relax what the
  owning domain requires.
- `migrate` — relocate a documentation root. Dry run by default, refuses a dirty
  git tree, refuses to overwrite, never deletes, and leaves user-authored protocol
  pointers untouched (they are reported instead).
- `--docs-dir` / `AGENTIC_SDLC_DOCS_DIR`: the documentation root is resolved
  (explicit flag > env > nearest recognized root > `ai_docs`). Two roots side by
  side refuse rather than half-validate.
- The drift guard (`shared_files.py`, `test_drift.py`): the spine is authored once
  and copied verbatim, and a forgotten copy now fails a test instead of reaching a
  user.

### Changed
- The validator ships as **two files**: `sdlc_core.py` (the shared spine) and the
  domain entry point. If you copied it into CI, copy both — `ENFORCEMENT.md` §2 has
  the recipe, and a half copy fails loudly at import rather than passing green.
- A review now reports a **restated fact** as a finding: every governance slot has
  one owning document, and the fix is a citation, not a better copy.
- The invariant battery is shared across distributions and reads a per-distribution
  PROFILE. Spine capabilities cannot be dropped by editing a profile; optional
  overlays are declared in one line.

