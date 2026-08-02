# Changelog

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

