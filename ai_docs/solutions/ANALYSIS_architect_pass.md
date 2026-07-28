---
id: F-020
feature: Architect Pass (capabilities before files)
status: COMPLETED
level: L3
start_date: 2026-07-28
end_date: 2026-07-28
---
# Feature Analysis: Architect Pass

## Objective

Phase 3 goes from the spec elicitation straight to the **Impact** — the list of
files that change. Nothing between them asks *what the system must be able to do*
and *whether a component already does it*. So the agent designs the feature and
builds whatever it lacks inside the feature's own code path: no component owns the
new capability, the next feature that needs it rebuilds it differently, and the
platform accretes feature-shaped code nobody can reuse.

Close it with an **architect pass** at L3, between elicitation and Impact: state
the feature as required capabilities (verbs over domain nouns, no files), rule each
one against the platform (EXISTS / INADEQUATE / MISSING), and design what is
missing as a component with its own contract, of which this feature is one
consumer.

## Feature Vision

Serves `vision/project_vision.md` (Status: APPROVED) **Goal 2 — "keep understanding
durable across sessions … so nothing load-bearing lives only in a transcript"**:
today the decision "this capability does not exist, so I'll put it here" is taken
silently and recorded nowhere; the ledger makes it a written verdict a later reader
can check. It also serves the Core Problem directly — myopia one level above the
file: the change is complete and the architecture is worse.

**Ceremony budget (Non-Goal "no ceremony ratchet").** This adds cost at L3 and
removes nothing, so it takes the Vision's second branch: cost stated, owner accepts
explicitly. Cost = one pass before the Impact + one ANALYSIS section + one support
file read only when the trigger fires. **Accepted by Antonio Pinto, 2026-07-28**,
with the pass scoped to L3 (L1/L2 unaffected).

Non-goals: no validator rule on consumer projects (a warning on every existing
ANALYSIS is the nagging the Vision forbids); no new document type — the ledger is a
section, and a split-out component reuses the ANALYSIS that already exists.

## Use Cases / User Needs

- **Solo developer using an AI agent** (Vision `## Actors`) — asks for a feature and
  gets it built on components, not inside itself. Good UX = the missing piece is
  named before implementation starts, not discovered by the next feature.
- **Team lead needing governance** — the reason a component exists is written where
  the review can check it, so "why is this here" survives the session that decided it.

## Capability Ledger

| Capability | Verdict | Component / gap |
|---|---|---|
| State a required capability and rule it against the platform, durably | **MISSING** | searched `skills/agentic-sdlc-skill/*.md` for capability/component doctrine: only comprehension guides and blast radius, both downstream of this question → new `architect.md` + `## Capability Ledger` section |
| Route an L3 through the pass at the right moment | **EXISTS** | `SKILL.md` §3 Request Analysis — the phase sequence already orders elicitation → analysis; the pass inserts between them |
| Verify at closure that the ledger was honored | **INADEQUATE** | `review.md` `## Reviewing` conformance statement maps Vision / use-cases / threats but has no capability clause → extend with one |
| Detect doctrine drift mechanically | **EXISTS** | `scripts/test_skill_invariants.py` (battery, `test_support_files_wired` orphan check) — this feature is a consumer, not an owner |
| Record which components exist, what capability each owns, with what contract | **MISSING** | `strategic/architecture.md` carried stack + directories + patterns; `## Directory Structure` names folders, not capability owners; `source_kind: code` guides cover one component at a time on a complexity trigger, never the inventory → new `## Component Map` section (2nd increment) |
| Fire a write when a component is BORN | **INADEQUATE** | Write-Triggers row for `strategic/architecture.md` is keyed on *"when the stack or the feature catalog actually changed"* — a new component is neither → its own row, keyed on the component's birth |
| Point the pass at the inventory before it searches source | **INADEQUATE** | `architect.md` §2 sent the reader straight to the symbol-graph tool → reads the map first, verifies against code second |
| Distinguish "nothing owns this" from "nobody has looked yet" | **MISSING** | nothing anywhere separated the two: a seeded-empty map read as authoritative absence → §2 coverage rule + the `Empty-map MISSING` anti-pattern + the `audit_plan` ANALYZED link (3rd increment) |
| Onboard a project the methodology arrives in late, without an up-front sweep | **INADEQUATE** | Phase 1 had one bullet ("analyzing the project in batches"), no order and no bound → scope-ledger-first + incremental-map licence, scoped so it never covers the blast zone |
| Notice mechanically that the pass was skipped | **MISSING** | battery checks the doctrine text, nothing checked execution (own review, reserve 1) → `ledger_due()` + validate warning on active post-epoch L3 without the section; grandfathered by `start_date` (4th increment) |
| Notice mechanically that a map row rotted | **MISSING** | guides have `source_hash`; map rows had nothing (reserve 2) → `check_component_map()`: `Where` refs resolved on disk, `#symbol` greped in matched files; warnings only |
| Exercise real agent adherence to the pass | **EXISTS** (layer) / **MISSING** (scenarios) | `evals/run_behavioral.py` + scenario format existed; no scenario covered the pass → `architect_rules_before_impact.md` + `unmapped_never_grounds_missing.md` |

Contract of the new component, stated without naming this feature: *`architect.md`
defines when the architect pass runs, the three verdicts and what each must carry,
the contract-vocabulary rule, the split rule, and the anti-patterns.* Consumers:
`SKILL.md` phase 3 (invocation), `templates.md` (where the output is recorded),
`review.md` (how it is checked).

## Impact

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/architect.md` | ADD | the discipline (MISSING row above) |
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | support-file list; phase 3 invocation; L3 minimum sections; Write-Triggers ANALYSIS row (split-out component gets its own ANALYSIS) |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | `## Capability Ledger` in the ANALYSIS template, before `## Impact` |
| `skills/agentic-sdlc-skill/review.md` | MODIFY | one conformance clause (INADEQUATE row above) |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | MODIFY | `test_architect_pass_wired`; `architect.md` added to the expected support-file list |
| `package.json` | MODIFY | `files` allowlist — an unshipped support file is a dangling pointer for every installed consumer |
| `ai_docs/strategic/architecture.md` | MODIFY | dogfood: this repo's own `## Component Map`, 7 rows |
| `CHANGELOG.md`, `ai_docs/strategic/existing_features.md`, `ai_docs/audit/handoff.md` | MODIFY | closure |

Second increment (Component Map) touches the same five skill files plus
`strategic/architecture.md`: template section, Write-Triggers row keyed on the
component's birth, `architect.md` §2 read-first + the closure loop, the `review.md`
finding, and `test_component_map_wired`.

Blast radius: `architect.md` is a new leaf with no consumers but the three pointers
above. The only signature-shaped change is the `expected` list inside
`test_support_files_wired` (single caller, same file). No public API, no dependency.

## Security and Threat Model

Surfaces touched: **filesystem** only, and only the skill's own Markdown plus one
stdlib test. No external input parsing, no authN/authZ, no crypto, no network, no
personal data. The validator is untouched, so no new path handling enters
`sdlc_check.py`.

Process threat (the one that matters here): **T1 — ceremony ratchet.** A mandatory
pass at L3 that fires on trivial-shaped L3s becomes the cost the Vision forbids.
Mitigation: the pass is a question, not a form — `architect.md` §1 licenses the
one-line answer when every capability plainly exists, and the trigger is L3 only.
**T2 — paper ledger** (rows filled with unfalsifiable EXISTS): mitigated by
requiring a named path/symbol per verdict and by the review clause.

## Action Plan

- [x] Elicitation round (4 forks: cost, ledger home, split default, enforcement)
- [x] Vision Gate — admission ruling + ceremony-budget acceptance recorded above
- [x] Write `architect.md`
- [x] Wire `SKILL.md` (4 edits)
- [x] `templates.md` — `## Capability Ledger` section
- [x] `review.md` — conformance clause
- [x] `test_architect_pass_wired` + expected-list entry
- [x] `package.json` allowlist + README support-file bullet and Runtime Shape tree
- [x] Battery green (59/59); closure (CHANGELOG, existing_features, handoff row)
- [x] **2nd increment — Component Map**: template section, own Write-Triggers row,
      `architect.md` read-first + closure loop, `review.md` finding,
      `test_component_map_wired`, this repo's own map (7 rows). Battery 60/60
- [x] **3rd increment — brownfield safety**: the map's silence is *unread, not
      empty*; cost-vs-standard rule; `Empty-map MISSING` anti-pattern; coverage
      line tied to `audit_plan` ANALYZED; Phase 1 scope-ledger-first + bounded
      incremental licence; `review.md` unfalsifiable-MISSING finding;
      `test_unmapped_never_grounds_missing`. Battery 61/61
- [x] **4th increment — mechanical backstops** (the two self-review reserves,
      owner: attack now): `ledger_due()` + validate warning (skipped pass,
      epoch-grandfathered); `check_component_map()` (map anti-rot, the
      `source_hash` equivalent); 2 behavioral scenarios; `architect.md`
      §Mechanical backstops; 3 new invariants. Battery 64/64

## Test Strategy

The deterministic gate is the existing static battery
(`python -m unittest discover -s scripts -p "test_*.py"`, run from the skill dir).
`test_architect_pass_wired` asserts the doctrine is present and reachable from every
consumer: `architect.md` carries its anchors, `SKILL.md` invokes it in phase 3 and
lists it, `templates.md` carries the section, `review.md` carries the clause. The
orphan check in `test_support_files_wired` already fails a support file that exists
without a pointer. No behavioral eval scenario: the pass is authoring discipline,
not a triggered lookup like the guide router.

## Diary / Current State

- **2026-07-28** — opened. devPNT off (in use elsewhere) → Standalone. Branch
  `feat/architect-pass`, cut from `feat/parallel-handoff` (v1.17.0 tag, not yet
  merged to main — same pattern as 1.17 cut from v1.16.0). Elicitation answered
  all-recommended: cost accepted at L3, own `## Capability Ledger` section,
  phase-in-plan as the default split for a single-consumer component, prose +
  battery invariant with no consumer-project validator rule.
- **2026-07-28 — closed.** Battery 59/59 (`test_architect_pass_wired` added, which
  also asserts the phase-3 ordering: the pass precedes the blast radius).
  `sdlc_check.py check` validate 0 errors / 4 pre-existing warnings (two DRAFT
  vision docs, two `functional/` docs with no `status:` — all present before this
  change); `stale` cleared with `mark skills/agentic-sdlc-skill/`.
  **Review: self-pass, declared** — no independent reviewer was used (devPNT is in
  use for another project and no subagent was requested), so independence is
  reduced. Conformance: both use-cases land (solo dev → `SKILL.md` phase 3 +
  `architect.md` §1–2; team lead → `templates.md` section + `review.md` clause);
  T1 mitigated by the L3-only trigger and the "question, not a form" licence; T2 by
  the named-symbol requirement plus the review clause. Non-Goal "not a
  work-management system" checked: the ledger is a design section inside one
  document, carrying no key that answers what to work on next. Dogfooding note —
  the doctrine itself was built as a component (`architect.md`) with three pointer
  consumers, not inlined into `SKILL.md`, which is the rule it states.
  **Not shipped**: version bump, tag, publish (owner's step, `GUIDE_release.md`);
  CHANGELOG carries `## [Unreleased - 1.18.0]`. The installed skill copy under
  `~/.claude/skills/` stays at 1.17.0 until that release.
- **2026-07-28 — reopened and closed again (Component Map).** The first increment
  shipped a pass with nothing to consult: §2 said "rule each capability against the
  platform" and no artifact described the platform's components, so the inventory
  had to be re-derived from source every session — the myopia the skill exists to
  prevent, reproduced inside the cure for it. Audited the architecture artifacts and
  found three gaps: no component/capability inventory anywhere (`architecture.md` is
  stack + directories + patterns; `source_kind: code` guides cover one component at
  a time on a complexity trigger); no trigger firing on a component's birth (the row
  was keyed on *stack changed*); and the three architecture artifacts (ledger, map,
  ADR) never cited each other. Closed all three with one movement — a `## Component
  Map` section inside the canonical `architecture.md` rather than a new document,
  because a new file for an existing home is the **speculative platform**
  anti-pattern this feature's own doctrine names. Trigger: the component's birth,
  same closure. Gate: the `review.md` ledger clause, extended — a capability built
  and absent from the map is a finding, since the next feature reads the map, rules
  it MISSING and builds it twice. Left open deliberately: the ADR trigger stays
  prose (*no decision, no ADR* blocks useless ADRs; nothing detects a decision taken
  and not recorded, and a stdlib validator cannot read a diff and judge). Cost
  accepted by the owner, 2026-07-28, same ceremony-budget branch as the first
  increment. Battery 60/60.
- **2026-07-28 — 3rd increment: the brownfield trap.** Owner raised the risk that a
  bootstrap licence would let an agent design without really understanding what is
  in the project. The concern located a live defect the 2nd increment had just
  created: `init.js` seeds `architecture.md` with an EMPTY `## Component Map`, and
  §2 had just told the pass to read that map first — so on any existing codebase the
  pass would read an authoritative-looking empty index, rule everything MISSING, and
  design duplicates of components that are already there. Fixed with an asymmetric
  rule rather than a warning: **the map lowers the COST of a verdict, never the
  STANDARD of one** (a cache of evidence somebody already paid for, not a substitute
  for evidence), and **its silence is unread, not empty** — outside the areas
  `audit_plan.md` marks ANALYZED the map can never ground a MISSING, the code is
  searched, and the MISSING carries the terms/tool/areas covered. The deferral is
  scoped explicitly: **understanding is never deferred, only WRITING the map is** —
  the incremental licence covers the rest of the repository and never what the
  change touches or depends on. Named `Empty-map MISSING` so a review can catch it;
  the review clause now treats an unnamed-search MISSING on unmapped ground as a
  finding. Phase 1 gains the order (scope ledger first) and the bound (no
  full-codebase sweep before the first feature; the map grows per feature, each
  marking what it covered). This repo's own map declares its coverage
  (`skills/agentic-sdlc-skill/`, `scripts/`; `examples/` still PENDING).
  Battery 61/61.
- **2026-07-28 — 4th increment: mechanical backstops.** My own closure review
  named two reserves and the owner chose to attack both now (few releases, then
  field tests on big projects). **Reserve 1 — nothing noticed a skipped pass**:
  `ledger_due()` + a validate warning when an ACTIVE L3 ANALYSIS born on/after
  2026-07-28 (`ARCHITECT_PASS_EPOCH`, lexicographic ISO compare) lacks
  `## Capability Ledger`. This supersedes the elicitation-round choice "no
  validator rule on consumer projects" by explicit owner instruction; the
  grandfathering keeps its spirit — closed history and pre-pass in-flight work
  (F-015, started 07-19) never nag. Plus two behavioral scenarios (the F-016
  route: adherence exercised, never gated): `architect_rules_before_impact` and
  `unmapped_never_grounds_missing` — the latter seeds the trap, an existing
  `RateLimiter` in a PENDING `legacy/` area, and fails the run that rules
  MISSING from map silence. **Reserve 2 — map rows rot invisibly**:
  `check_component_map()` resolves every slash-containing backticked ref in
  `Where` (glob-aware, `confine_under` fail-closed) and greps the `#symbol` in
  matched files; warnings only, the map's `source_hash` equivalent. Proof it
  works: it immediately caught a rotten ref in THIS repo's own map
  (`evals/run_behavioral.py` written unqualified — resolved nowhere). Battery
  64/64; validate on this repo: same 4 pre-existing warnings, no new noise.
