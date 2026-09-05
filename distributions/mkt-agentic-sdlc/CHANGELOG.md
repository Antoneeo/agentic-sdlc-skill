# Changelog

## [0.9.0] - 2026-09-05

Spine-only release: `review.md` updated byte-identical across the family
(authored in the code lens, code 1.31.0).

### Changed
- **The form budget belongs to the FIRST draft (shared spine `review.md`).**
  The lean operative form is the first draft's form, not the round-3 rescue:
  the review request states the artifact's line count against a budget the
  author fixed before drafting, and an artifact over budget is the reviewer's
  first finding, before content. This replaces "rewrite lean at the latest
  before round 3", which paid for the form only after two rounds had already
  been spent reading a bloated artifact. The ~1,250 -> ~500 line measurement
  already in the file is the budget's anchor.

## [0.8.0] - 2026-09-01

Spine-only release: `review.md` updated byte-identical across the family
(authored in the code lens, F-045 / code 1.30.0).

### Added
- **Review-loop convergence (shared spine `review.md`).** *Revise means
  converge, not accrete*: lean rewrite at the latest before round 3, revision
  archaeology lives in REVIEW_LOG, never in the artifact. *Severity contract*
  stated with every review request: blocker = unfit-to-proceed evidence only,
  wishes are WARN at most. *Scripted author pre-audit*: resolve every anchor
  and recount every count before requesting. The new *behavioural-claim-probes*
  reviewer clause is lens-gated and self-disarmed in this lens (this SKILL.md
  defines no Execute-Before-Specify duty).

## [0.7.0] - 2026-08-28

Spine + overlay delta parked for the next release of this lens (shipped first
in kb; the spine stays byte-identical x3 in the repo while packages publish
independently). In this lens the note is re-attached by the overlay
(`mkt_check.py`, after its own check verdict), because the overlay replaces
the spine's check pipeline entirely.

### Added
- **F-041: `check` notes an unwired or dead session-orientation hook** (one
  informational `[note]` line -- never the exit code, never a `validate` warning,
  so CI is unaffected). `init` wires the hook only at init time; projects
  initialized before F-036 or bootstrapped without `init` were silently unwired.

### Added (F-042, parked with the above)
- Install/update wires the session-orientation hook machine-wide (Claude Code
  with Python; user-level settings; removal is a standing per-target opt-out;
  uninstall surgically removes what it wired). The check note is global-aware
  and reworded in consequence-first user language.

### Added (F-043 port, with the above)
- **The revision sentence.** Updating an existing strategy or campaign doc (the E2 row) is a REWRITE, not an
  append: full re-read, body rewritten to current state -- never an appended
  delta section. Ported from the kb lens's `## Revision` doctrine (kb 1.10.0),
  born from a field post-mortem where delta-append revisions left stale
  sentences standing as printed truth.

## [0.6.0] - 2026-08-26

F-038 — the gated rung: truthful log vocabulary and a mandated ask, no grant memory.

### Fixed
- **A review rung that exists behind a permission policy is no longer logged as
  "unavailable".** The ladder knew two states (the client supports the rung, or not)
  and hard-coded rung 3's reason as "no subagent facility on this client" — so a gated
  facility produced false log rows, and the ladder's own prohibition ("rung 3 is
  illegitimate wherever rung 1 or 2 exists") was unsatisfiable on a gated client: the
  agent could not obey it without asking, and no rule said to ask.

### Added
- **The gated-rung stop.** At a due review gate (design; closure), when the best rung is
  permission-gated (a standing policy — an interactive per-call prompt is NOT this) and
  no ungated rung works (a working one-shot CLI pre-empts the stop; a gated rung 2 joins
  the question instead), the gate stops and asks ONE question in the five-bullet blocking
  form: the gated rung(s) vs the fallback, each higher rung's status, the quoted policy,
  the cost (~130-175k subagent tokens per deep review, measured 2026-08) AND what
  independence last bought, and what stays blocked. **No grant memory**: the answer holds
  while the conversation does; an agent that cannot recall a grant asks again. Unattended
  runs never emit the question — rung 2 is still owed a try, then rung 3 with its reason.
  (Successor to a design CANCELLED at the review cap after grant memory failed three
  ways; rulings r18/r19.)
- **The reason words.** A below-rung-1 row says why the rung(s) above did not run:
  `absent` (the client has no such facility — a claim about the client, never a policy),
  `gated, declined`, `gated, unattended`, `gated, pre-empted` (nothing asked — an
  ungated lower rung ran the review). A rung-1 row owes nothing. For rung 3 this
  re-words an existing duty; for rung 2 it is a new one-word duty, disclosed and
  accepted with the rest.

## [0.5.1] - 2026-08-25

### Fixed
- **The three README front pages did not mention the hook wiring that 1.27.0 added.**
  `init` now changes what every project gets, and the README *is* the npm page, so two
  of the three said nothing about it and the third barely did. Each now describes the
  wiring, the settings.json / settings.local.json split and why it exists, and the
  broken-hook report. `GUIDE_release.md` step 2 already made this a release duty; it was
  skipped in 1.27.0 and this is the catch-up.
- **`publish_all.bat`'s verify block reported the previous version after a successful
  publish — twice.** `--prefer-online` (added in kb 1.4.8) forces revalidation but cannot
  outrun CDN propagation of the `latest` tag in the seconds after publishing, so the
  1.27.0 run printed mkt `0.4.7` when `0.5.0` had in fact landed. The flag alone was the
  wrong fix and the note claiming otherwise is corrected: the block now **polls** each
  package until the registry agrees with the local version, and prints both when it does
  not, so "did it publish?" is answerable from the run instead of a manual `npm view`.

## [0.5.0] - 2026-08-25

F-036 — the orientation hook installs itself.

### Fixed
- **`ENFORCEMENT.md` 4 said "wire it on every project" and nothing ever did.** The
  SessionStart orientation hook was real, tested and fail-open, but installing it was a
  manual step, so it was skipped — and a session that never enters Phase 1 explicitly
  then never meets the guide router at all. Field result: an agent worked a governed
  project without invoking the process. `init` now wires the hook itself.
- **The invariant that looked like it guarded this guarded only prose** — it asserted
  the documentation section exists (`assertIn("## 4. SessionStart hook", t)`) and that
  `orient` runs. It gains a companion asserting the shipped installer actually CALLS the
  writer. Mutation-tested: the first draft asserted the bare symbol and passed on a file
  that imports the writer without invoking it, which is exactly the disabled-installer
  case it exists to catch.

### Fixed (also)
- **ENFORCEMENT 4/2's own worked hook examples named a skill directory that two of
  the three lenses do not install.** kb and mkt both printed
  `.claude/skills/agentic-sdlc/scripts/...`; kb installs under `kb-agentic` and mkt
  under `mkt-agentic-sdlc`, so anyone who copied the snippet got a hook that runs,
  prints `can't open file`, and emits nothing — the wired-and-dead defect this release
  detects, sitting in the instructions that produce it. Four paths corrected, and a new
  invariant derives the expected directory and validator from what the distribution
  actually ships and fails if an example names anything else. Mutation-tested.

### Added
- **A portability rule the doctrine did not have.** The hook command names a validator,
  and where that validator lives decides which settings file may carry it: a repo that
  vendors the validator gets a repo-relative command in the shared, committed
  `.claude/settings.json`; a normal project gets an absolute path, which goes to the
  git-ignored `.claude/settings.local.json` instead — committing it would hand every
  teammate a hook naming a directory they do not have. `init` picks the file and adds
  the local one to `.gitignore`. ENFORCEMENT 4's own worked example showed an absolute
  path and did not mention the distinction; it now does.
- **A wired-but-dead hook is detected and reported instead of counted as done.** Found
  in the field: a repository whose hook named a sibling lens's path, so it ran every
  session, printed `can't open file`, and emitted nothing. A bare "is a hook present?"
  check answers "already wired" to that and makes the silence permanent, so the existing
  command's validator path is checked on disk. Never rewritten — it may be hand-tuned —
  but never passed off as working either.

### Notes
- `init` declines rather than guessing: no Python, skill not installed, a settings file
  that is not valid JSON (never rewritten — a merge would discard what is in it), or a
  skill path containing a double quote. Each case prints the snippet to paste.
- Only Claude Code's hook shape is wired. Codex and Gemini keep the manual snippet: this
  repository has no fixture pinning their schema, and writing a hook file in a shape
  nobody has verified is how the wired-but-dead defect above was born.
- A blocking `PreToolUse` gate would be real enforcement rather than a nudge, and it is
  refused by the Vision's no-ceremony-ratchet Non-Goal. Recorded in the analysis so the
  next person to have the idea finds the ruling instead of re-deriving it.

## [0.4.7] - 2026-08-06

### Fixed
- **Shared-spine sync: the scoped re-review contradicted `dispatch.md` (ACTIVE in this lens).**
  `dispatch.md` said "exactly three review touches per task, never a loop" while `review.md`
  required every review-driven correction to be re-reviewed. Reconciled: the scoped re-review is
  a round inside slot 2 or 3, never a fourth slot. Also in the shared `review.md`: an unproven or
  stale completion claim is now a reviewer finding; a PASS carrying findings is provisional until
  its corrections pass a round; the single log row keeps the round-1 verdict (`FAIL → PASS`).
  Found by the code lens's late design review of F-034.

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

