---
id: F-032
feature: Interaction Contract (actor-facing surface spec between use cases and solution)
status: COMPLETED
level: L3
start_date: 2026-08-04
end_date: 2026-08-04
---
# Feature Analysis: Interaction Contract

*Scope header — for the design reviewer (cold, repo access) and the implementing
agent. Answers: "what changes in which doctrine files, and why this shape". Does
not answer: "why the skill exists" (Vision) nor "the final wording of each edited
paragraph" (the diff).*

## Objective

Field defect, reported by the owner (2026-08-04): the pipeline never produces a
functional specification of the actor-facing interface. Use cases (`## Use Cases /
User Needs`, Hybrid `D-UC`) are written before the solution and stay at intent
level — correctly, but nothing downstream ever binds them to concrete surfaces.
The Impact/E-ISP and E-TDD speak component vocabulary (files, signatures, state
machines); no artifact says *which control the actor operates, what the system
responds, which use case that realizes*. Consequences, observed on frontend work
and generalizable to any actor-facing surface (GUI, CLI, API):

- the agent invents the UI at implementation time — UX is emergent, not designed;
- the design review's "actor UX fit" clause (`review.md` conformance statement —
  it binds impact/solution-analysis and design reviews, not the plain code-diff
  closure review) has no checkable object: the reviewer judges by impression;
- the Vision's `## Actors` "good UX =" clauses are a promise with no contract.

**The fix**: a conditional `## Interaction Contract` (IC) section in the ANALYSIS,
between the use cases and the Capability Ledger, plus the review clause that makes
it verifiable. No new document, no new file kind.

## Feature Vision (alignment)

Admission test run against `vision/project_vision.md` (APPROVED v8) and
`vision/rulings.md`: no ledger row answers this question → the prose ruled once;
closure adds the new ADMIT row. Basis:

- Advances the Goal "make divergence visible *before* implementation": today
  UX divergence is invisible until the code exists.
- Advances the Actor commitments: every project Vision's "good UX =" clause gains
  a downstream artifact that can honor or violate it checkably.
- Attacks the Core Problem (myopia): the interaction design stops living only in
  the implementing session's head.

**Ceremony disclosure (Non-Goal "no ceremony ratchet", the L2/L3 budget)**: this
adds a conditional section at L3 and removes nothing of comparable cost. The full
cost, stated because the Vision counts reading as cost:

- authoring: one section per L3 whose change touches an actor-facing surface; one
  line ("trigger not fired: …") on every other L3; nothing at L1/L2/Spike;
- reading: one added paragraph in the code SKILL.md loaded every session, one
  template-comment block read when drafting an ANALYSIS, and one conformance
  clause in the shared `review.md` read by reviewers in all three distributions —
  including kb/mkt, where it is lens-keyed and can never fire (finding 8's fix);
- maintenance: one more spine hash to keep in sync (`review.md`, plus
  `test_skill_invariants.py` if the wiring test lands — see Test Strategy).

The owner is asked to **accept this cost explicitly** at design approval —
recorded in the Diary when given.

## Use Cases / User Needs

- **Solo developer using an AI agent** (Vision Actor): a feature with UI arrives
  at implementation with the interaction already decided — which view, which
  control, which response — so the shipped UX matches an approved design instead
  of the agent's improvisation.
- **Team lead needing governance** (Vision Actor): the **design review** (moment
  1 — the moment the conformance statement binds) can verify "every use case is
  realized by a named interaction path" against a written contract, not an
  impression; the closure review then checks the diff against that approved
  contract like any other part of the design.
- **The implementing agent** (internal actor): receives observable-behavior
  requirements separated from solution hypotheses, so it knows what is binding
  (the contract) and what is negotiable (the feasibility notes).

## Interaction Contract

Not fired: this change edits doctrine text only — no software surface an actor
operates is created or modified. (The section the feature itself introduces;
stated here for the dogfood record.)

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| declare a conditional design section in the ANALYSIS template | EXISTS | Template source, `skills/agentic-sdlc-skill/templates.md` | re-read: single fenced block per document; `## Capability Ledger` is the precedent for a question-not-form conditional section |
| enforce a design constraint at review time | EXISTS | `review.md` §Reviewing conformance statement | re-read: already maps use-cases/threats/Vision to evidence; extension point for IC |
| propagate a shared-spine edit to all three distributions | EXISTS | `scripts/shared_files.py` + `shared_manifest.json` | manifest lists `review.md` as spine; `--update` regenerates hashes in all copies |
| mechanically validate section presence | EXISTS, deliberately NOT used in this unit | `sdlc_core.py` ANALYSIS_SECTIONS / epoch-gated ledger advisory (`ARCHITECT_PASS_EPOCH`) | honest rationale: the IC body is conditional on a semantic trigger the validator cannot decide (did the change touch an actor-facing surface?), so a presence check would either nag every L3 retroactively or bless a one-line dodge. An epoch-gated advisory on the F-020 pattern is admissible follow-up once the trigger wording has field mileage — named, not shipped here. Consequence accepted: Standalone's only backstop for a skipped IC is the design-review clause |

No MISSING rows → no new component; the feature composes existing machinery.

## Impact

The design, per file. IC's shape (decided with the owner in the elicitation round,
2026-08-04 chat):

- **Pipeline position**: Vision → use cases → **IC** → threat model → impact/
  solution. Degrees of freedom shrink monotonically: why → what is needed → what
  the surface exposes → which components → how exactly. Owner's formulation
  (2026-08-04, confirmed mid-closure): D-UC says what the person needs, D-IC says
  through which surface, only then is the threat assessed ON those surfaces and
  the solution designed — **the E-ISP inherits the UI instead of generating it**.
  In Hybrid the governed sequence is D-UC → D-IC → P-TM → E-ISP (the companion
  devPNT workstream implements the artifact; until then the IC content rides in
  the E-ISP).
- **Contract content**: (a) as-is of the touched surfaces (what the actor operates
  today) **and of the interaction patterns already in use** relevant to these use
  cases — the product's existing idioms (how it already does selection,
  confirmation, error display, navigation); (b) per use case, the interaction
  path — actor action on surface → system response → outcome — as a table;
  (c) states for each new/changed view (empty, loading, error, denied);
  (d) **feasibility notes**, non-binding: "path X presupposes reuse of Y",
  "alternative Z discarded: disproportionate cost".
- **Pattern reuse by default (UX coherence — owner refinement, 2026-08-04)**: the
  contract repeats and preserves the idioms the as-is inventory found; it is the
  interaction-level twin of the anti-DRY orientation and of "preserve
  architectural coherence". Introducing a NEW idiom where an existing one covers
  the job is a declared decision in the contract, with the reason — never an
  unmarked invention. Follow-up named (review finding 10): from the second fired
  IC on the same product, the idiom inventory is recurring knowledge — a
  `source_kind: code` comprehension guide should own it, with later ICs citing it
  plus deltas; not shipped in this unit.
- **Authority split**: the contract binds observable behavior only — no
  components, no files (that is the Impact's vocabulary). Feasibility notes are
  hypotheses the Impact confirms or refutes. If the solution cannot honor a
  contracted path at proportionate cost, the contract is **renegotiated
  explicitly** — a downstream artifact may propose the change, never enact it
  silently (the Vision-amendment pattern at feature scale). Who approves: before
  the design is approved the author iterates freely; **after approval a contract
  change is a scope change and the user approves it** — the same rule the ledger
  clause already applies to absorbed capabilities.
- **Trigger**: fires when the change creates or modifies a surface through which
  an actor **acts on or perceives** the system — GUI view, CLI command/flags, API
  endpoint, user-edited config, notification or user-facing message (perceive
  side). The list is illustrative; the verb pair is the test. IN: the wording and
  states of an error dialog (the actor perceives it and decides on it). OUT: an
  internal log format (no actor in the Vision's sense reads it to act); a private
  module API (operated by code, not by an actor). Not fired → one line stating
  why. **The trigger's owning home is the templates.md section comment**; SKILL.md
  and the review clause cite it, never restate it (restated-facts rule).
- **Co-design, and where the architect pass sits**: the drafting order inside the
  IC is *use cases clear → read the existing patterns → imagine the best UX by
  reusing them → vet feasibility with solution deep-dives*. Those deep-dives ARE
  early architect-pass probes: drafting interleaves — IC paths suggest
  capabilities, capability verdicts feed feasibility notes back. What stays fixed
  is the finalization order the doctrine already mandates: the Ledger is complete
  before the Impact is drafted (`SKILL.md` "Architect before you list files"),
  and the IC is finalized before the Impact too. The planned SKILL.md paragraph
  states this explicitly so the implementer does not invent the sequencing.
  Approval stays sequential (contract before solution).

Files touched:

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/templates.md` | MODIFY — insert `## Interaction Contract` into the ANALYSIS fenced block, between Use Cases and Capability Ledger; comment is the **owning home** of the trigger definition and carries content, authority split, renegotiation rule, and the path→test duty (each contracted path covered by `## Test Strategy`) | Template source is the single home of document bodies; `init.js` extracts the whole block, so no extractor change |
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY — Phase 3: add IC to the minimum-sections list (as conditional), one paragraph (boundary + renegotiation + where IC sits relative to the architect pass), **citing** the templates.md trigger, never restating it; Hybrid L3: IC content lives in the E-ISP above the Impacted Components map, like the ledger | Doctrine contract; Hybrid must not invent a devPNT artifact the server does not define; one owning home per fact |
| `review.md` — **shared spine, three copies**: `skills/agentic-sdlc-skill/`, `distributions/kb-agentic-skill/.../`, `distributions/mkt-agentic-sdlc/.../` | MODIFY — conformance statement: when the change touches an actor-facing surface, a missing IC is a finding; each use case must trace to a named interaction path; a design/solution element altering contracted behavior without a renegotiation note is a finding; contracted paths must be covered by the Test Strategy | The review discipline lives once; the clause is **lens-keyed on the ledger-clause pattern** ("the section the code lens's template defines"), not left to the empirical hope that kb/mkt never trip it |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` — **shared spine, three copies + manifest** | MODIFY — invariant test on the F-020 precedent: SKILL.md names the IC in Phase 3, templates.md carries the section, review.md carries the clause | Without it, a later edit dropping the IC wiring fails nothing; the file is spine, so the manifest regeneration covers it too |
| `skills/agentic-sdlc-skill/elicitation.md` | MODIFY — the actor/UX elicitation item also elicits the surfaces the actor uses today for this job | Gives the IC's as-is an elicited base; one-line delta |
| `sdlc_core.py` — **shared spine, three copies** + `sdlc_check.py` (code entry point) | MODIFY — register `interaction_contract` in `OPTIONAL_CAPABILITIES` (core) and claim it in the code profile | Mechanical enabler added during implementation (recorded per closure review W1): `test_profile_claims_no_unknown_capability` rejects an unregistered capability, and without the profile claim the `@requires("interaction_contract")` test would silently skip everywhere — the F-020 `architect_pass` pattern exactly; inert in kb/mkt (unclaimed) |
| `scripts/shared_files.py --update` output: three `shared_manifest.json` | REGENERATE | hashes change for `review.md`, `sdlc_core.py`, `test_skill_invariants.py` |
| `ai_docs/vision/rulings.md` | MODIFY at closure — new ADMIT row (question: "specifies observable actor-surface interaction binding use cases to surfaces before solution design") | The admission test's own procedure: prose ruled once → verdict becomes a row |

Blast radius (consumers of the touched symbols): `templates.md` fenced blocks →
`scripts/init.js` (extracts whole blocks — unaffected) and the test batteries
(assert on template/doctrine invariants — run to verify). `review.md` and
`test_skill_invariants.py` → spine: the three distributions' copies and
`shared_files.py` drift check (manifest hashes regenerate in all three). No code
signatures change; consumers enumerated by role because the artifacts are prose.

Out of scope, named: the devPNT-side governed `D-IC` artifact (schema, §4.2
catalog, trigger policy) belongs to the devPNT repository — its doctrine files are
generated from `devPNT/agent/core` sources and never hand-edited here. Companion
workstream to open there; until then Hybrid keeps IC inside the E-ISP.

## Security and Threat Model

No security impact, justified: doctrine-text change only — no code path, no input
parsing, no new file format the validator must parse (the IC section is inert
markdown inside an existing template). Indirect security *benefit*: the IC's
trigger feeds the threat model — every new/changed actor surface it names is a
threat surface P-TM/`## Security` must answer, and the pipeline order (IC before
threat model) makes that feeding structural.

## Action Plan

- [ ] 1. templates.md: IC section in the ANALYSIS fenced block
- [ ] 2. SKILL.md: Phase 3 sections list + IC paragraph + Hybrid seam note
- [ ] 3. review.md: lens-keyed conformance clause; propagate to both distributions
- [ ] 4. elicitation.md: surface elicitation delta
- [ ] 5. test_skill_invariants.py: IC wiring invariant (spine — propagate); `shared_files.py --update` regenerates the three manifests
- [ ] 6. Battery green: `python -m unittest discover -s skills/agentic-sdlc-skill/scripts -p "test_*.py"` (+ distribution batteries)
- [ ] 7. Closure: rulings.md ADMIT row; `sdlc_check.py index` + `check`; ADR if the review deems the authority split an architectural decision; registry update
- [ ] (post-merge, separate acts) release version bumps per `GUIDE_release.md`; devPNT-repo companion workstream for governed D-IC
- [ ] (named follow-ups, not this unit) epoch-gated validator advisory for IC presence; behavioral eval scenario for the IC clause; idiom-inventory comprehension guide pattern

## Test Strategy

Doctrine change → the executable evidence is the invariant battery (static,
zero-LLM) plus the spine-drift check: all `test_*.py` in the three distributions
green, including the **new IC wiring invariant** (F-020 precedent: SKILL.md names
it, templates.md carries the section, review.md carries the clause — a later edit
dropping any of the three fails the build); `shared_files.py --update` confirming
the three `review.md` and `test_skill_invariants.py` copies identical;
`sdlc_check.py check` CLEAN at closure. Behavioral evals (`evals/scenarios/`)
gain no new scenario in this unit: the IC clause is review-enforced, and writing
an eval for it is admissible follow-up work, not a gate for this change.

## Diary / Current State

- 2026-08-04 — Elicitation held in-chat with the owner: pipeline position, name
  (Interaction Contract over Interface Contract), co-design with non-binding
  feasibility notes, renegotiation authority; owner refinement folded in
  mid-draft: pattern reuse by default (read existing idioms, repeat and preserve
  them; new idiom = declared decision). Admission test run: ADMIT, new ruling row
  due at closure. Ceremony cost disclosed; owner acceptance pending at design
  approval. ANALYSIS drafted; next: independent design review (moment 1), then
  implementation on `feat/interaction-contract`.
- 2026-08-04 — Design review (moment 1) run by an independent fresh-context
  reviewer: **PASS, 0 BLOCK / 10 WARN**, full conformance statement delivered.
  All 10 findings answered by revision in this document: trigger closed with the
  act-or-perceive verb pair + IN/OUT examples and given templates.md as owning
  home (f1, f9); reading/maintenance cost added to the ceremony disclosure (f2);
  design-review vs closure-review moment corrected in Objective and UC2 (f3);
  IC↔architect-pass sequencing stated (f4); renegotiation approver named — the
  user, post-approval (f5); IC wiring invariant test added to Impact/plan and
  path→test duty added to the clause (f6); honest validator rationale + epoch
  advisory as named follow-up (f7); review clause lens-keyed on the ledger
  pattern (f8); idiom-inventory guide named as follow-up (f10). Logged in
  `audit/reviews/REVIEW_LOG.md`. Awaiting: owner design approval + explicit
  ceremony-cost acceptance, then implementation.
- 2026-08-04 — Owner approval given ("si, confermo entrambi"): design approved
  AND ceremony cost explicitly accepted as disclosed (per-L3 conditional section,
  SKILL.md paragraph read every session, spine clause in three distributions, one
  more spine hash). Status → IN_PROGRESS; implementing per the Action Plan.
- 2026-08-04 — Implemented TDD-first (invariant RED → doctrine edits → GREEN).
  Batteries: code 162 OK, kb 240 OK (IC test skips where unclaimed); mkt
  full-discovery failure verified PRE-EXISTING on baseline (13+1 identical
  without the diff) — spawned as its own task, not this workstream's. Deviation
  recorded: `interaction_contract` capability registration (sdlc_core ×3 +
  code profile) added as mechanical enabler — now in the Impact table. Closure
  review (moment 2, independent): **PASS, 0 BLOCK / 3 WARN**, full conformance
  statement; W1 (record the enabler) and W2 (stale handoff) fixed, W3 (closure
  acts) executed: rulings r16 ADMIT row, ADR
  `architecture/ADR_2026-08-04_interaction_contract_layer.md`, existing_features
  [032]. Owner confirmed mid-closure the Hybrid sequence D-UC → D-IC → P-TM →
  E-ISP ("l'E-ISP eredita la UI invece di generarla") — folded into the Impact
  bullet and the SKILL.md Hybrid note. Status → COMPLETED; branch awaits the
  owner's merge call (registry row stays via HANDOFF until merged).
