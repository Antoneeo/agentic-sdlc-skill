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

Non-goals: no new document type — the ledger is a section, and a split-out component
reuses the ANALYSIS that already exists. **Amended 2026-07-28**: the elicitation
round also chose "no validator rule on consumer projects"; the owner later
instructed the opposite (4th increment). What shipped keeps that non-goal's *spirit*
and drops its letter — the checks are **advisories** (`[note]`, never counted as
warnings, inert under `--strict`, so they cannot redden a pipeline) and are
grandfathered by `start_date`, so no pre-existing ANALYSIS is ever nagged.

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
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` | MODIFY | 4th increment: `ledger_due()`, `check_component_map()`, `_map_refs()`, the `advisories` bucket in `cmd_validate` |
| `skills/agentic-sdlc-skill/evals/scenarios/architect_rules_before_impact.md` | ADD | adherence: the pass run cold |
| `skills/agentic-sdlc-skill/evals/scenarios/unmapped_never_grounds_missing.md` | ADD | adherence: the brownfield trap |
| `README.md`, `gemini-extension.json` | MODIFY | support-file bullet + Runtime Shape tree; release version point |
| `ai_docs/audit/audit_plan.md` | MODIFY | `mark` reference for the re-analyzed skill dir |
| `CHANGELOG.md`, `ai_docs/strategic/existing_features.md`, `ai_docs/audit/handoff.md` | MODIFY | closure |

Second increment (Component Map) touches the same five skill files plus
`strategic/architecture.md`: template section, Write-Triggers row keyed on the
component's birth **and on discovery**, `architect.md` §2 read-first + the closure
loop, the `review.md` finding, and `test_component_map_wired`. Third and fourth add
the brownfield rules and the mechanical backstops in the table above.

Blast radius: `architect.md` is a new leaf with no consumers but the three pointers
above. The only signature-shaped change is the `expected` list inside
`test_support_files_wired` (single caller, same file). No public API, no dependency.

## Security and Threat Model

Surfaces touched: **filesystem** and **parsing of document-supplied paths**. No
authN/authZ, no crypto, no network, no personal data.

The 4th increment puts new path handling into `sdlc_check.py`, so the surface is
real: `check_component_map()` reads refs out of `strategic/architecture.md` — a file
any contributor edits — then resolves them, may expand them with `root.glob()`, and
reads every matched file. Threats and mitigations:

- **T1 traversal via a crafted ref** (`../../etc/passwd`, absolute, drive-relative):
  `confine_under(root, ...)` fail-closed before any filesystem touch; glob
  metacharacters are neutralized for the confinement test so a pattern cannot slip
  past it. Covered by `test_component_map_rot_detected`.
- **T2 resource exhaustion via a wide glob** (`**/*`): bounded in practice — the
  check only reads files when the ref carries a `#symbol`, and `read_text` is the
  same bounded reader the validator already uses everywhere. Accepted risk: a
  deliberately pathological ref in your own repository's own architecture doc is
  self-inflicted, and the check is advisory (it cannot fail a build).
- **T3 false confidence**: the check proves a ref resolves, never that the row
  describes the component correctly — stated in `architect.md` beside the check,
  the same honest limit the guides' `source_hash` carries.

The two eval scenarios add no runtime surface: `run_behavioral.py` seeds a temp
fixture, makes no model call, no network request, and spawns no process.

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
      owner: attack now): `ledger_due()` + validate advisory (skipped pass,
      epoch-grandfathered); `check_component_map()` (map anti-rot, the
      `source_hash` equivalent); 2 behavioral scenarios; `architect.md`
      §Mechanical backstops; 3 new invariants. Battery 64/64
- [x] **5th increment — independent review dispositions** (2 reviewers, fresh
      context, read-only; both returned FAIL): 5 blockers and the substantive
      warnings fixed — discovered-component trigger, status filter dropped,
      advisory bucket, glob/header/word-boundary/Windows/URL fixes in the rot
      check, `parse_iso` gating, split-rule bullet 2, contract re-description
      clause, MISSING search floor, one-line licence, Hybrid home, Coverage as
      pointer, ANALYSIS Impact/Security/Test-Strategy corrected, 4 weak tests
      repaired. Battery 65/65
- [x] **6th increment — 2nd review round** (verifier: all 5 blockers confirmed
      fixed by execution; cold adversary: 2 new blockers): audit-plan path
      confinement in `stale`/`mark` + seeder writes `.`; review.md ledger clause
      made unconditional at L3; closed suffix list (no false rot on prose);
      day-zero advisory removed; heading match case-insensitive; header-required
      + ragged-row reporting; two backstop bypasses closed; `mark`-counter-check
      advisory; split bullet 2 and the MISSING floor rewritten. Battery 69/69
- [x] **7th increment — 3rd review round** (code-delta reviewer + a COLD
      end-to-end usage trial on a 25-file brownfield fixture, a lens never run
      before): `map_where_refs()` scopes the harvest to the map's Where column
      (the convergent BLOCK); `level`-missing and DRAFT-vision demoted to
      advisories (`--strict` CI was red on bootstrap); router stub written with
      zero guides + a third legal verdict; `Use Cases / User Needs` added to the
      L3 minimum sections; multi-line HTML comments no longer leak into the
      manifest; CamelCase prose no longer reported as rot; `mark` validates all
      paths before printing; gate message names the real remedy; unattended
      elicitation path. Battery 73/73
- [x] **8th increment — 4th round (narrow verification)**: 1 BLOCK (my own F4 fix
      had downgraded a real error to an advisory), the documented `owns no
      component` opt-out that was never implemented, a heading-strip that nuked
      to EOF, a CamelCase exclusion far wider than its defect, and an invariant
      of mine that was green on broken code. All fixed. Battery 73/73

## Test Strategy

The deterministic gate is the existing static battery
(`python -m unittest discover -s scripts -p "test_*.py"`, run from the skill dir).
`test_architect_pass_wired` asserts the doctrine is present and reachable from every
consumer: `architect.md` carries its anchors, `SKILL.md` invokes it in phase 3 and
lists it, `templates.md` carries the section, `review.md` carries the clause. The
orphan check in `test_support_files_wired` already fails a support file that exists
without a pointer.

**Amended (4th increment)**: the static battery proves the doctrine is *wired*, never
that an agent *executes* it, so two behavioral scenarios join the non-gating eval
layer — `architect_rules_before_impact` and `unmapped_never_grounds_missing` (the
latter seeds a real trap: an existing `RateLimiter` in a PENDING area). They are
parsed and their criteria checked for substance by `test_architect_scenarios_present`;
they never gate, because model adherence is nondeterministic.

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
- **2026-07-28 — 5th increment: independent review, both reviewers FAIL.** Owner
  asked for an independent review before publishing. Two read-only reviewers, fresh
  context, separate lenses (conformance+correctness; adversarial Vision+doctrine).
  Five blockers, all real, all fixed:
  1. **The backstop could never fire.** `ledger_due` required PLANNED/IN_PROGRESS,
     but closure flips the ANALYSIS to COMPLETED *before* `check` runs — the check
     was silent at the only moment the process mandates the validator. Status filter
     dropped; `start_date` is the sole guard, which is what grandfathering needed
     anyway. The old invariant had locked the defect in, so it was inverted.
  2. **A DISCOVERED component had no write trigger.** `architect.md` mandated
     writing the row; `SKILL.md` (the authoritative write index) and `review.md`
     fired on *birth* only. Following the shipped rules: mark the area ANALYZED,
     leave the map silent, and the next feature lawfully rules MISSING and builds a
     duplicate — the exact failure the 3rd increment exists to prevent, reachable
     by obedience. Trigger and finding both extended; `architect.md` now forbids
     the mark without the rows and states what a mark asserts.
  3. **"Never a gate" was false.** `--strict` escalates warnings to exit 1 and
     `ENFORCEMENT.md` recommends it in CI, so the ledger check was a blocking gate
     on consumer pipelines — a cost the ceremony-budget acceptance never named
     (`project_vision.md`: "Omission resolves against the proposal"). Fixed by
     honoring the accepted budget rather than expanding it: a third severity,
     **advisories**, printed as `[note]`, never counted as warnings, inert under
     `--strict`. New invariant asserts a missing ledger cannot fail `--strict`.
  4. **Literal brackets read as globs** — `app/[id]/page.tsx` (Next.js) reported as
     rot on any consumer project. Literal existence is now tried first.
  5. **The rot check was inert in silence** — `Where` taken as the last column
     (any extra column disarmed it), refs without `/` skipped (9 of this repo's own
     18 refs unchecked), Windows separators skipped, substring symbol match passing
     `#Notif` against `Notifier`. All fixed, plus a notice when a map has rows but
     no checkable ref: an inert check reported as a clean one is the same defect as
     an unread map reported as empty.
  Doctrine hardening from the adversarial lens: §4's split bullet 2 was unreachable
  (§3 mandates the property it used as a trigger, so every component earned its own
  L3) — resharpened to "delivers value merged alone" with an IN/OUT pair; the
  contract test gained its re-description clause (paraphrase defeated it); the
  MISSING search gained a floor and a stopping rule; the one-line licence now says
  the answer still lives under the heading, naming the component; `SKILL.md` phase 3
  no longer states the Standalone home unconditionally, and declares the Hybrid
  coverage asymmetry; the duplicated `Coverage:` list became a pointer to
  `audit_plan.md` (a cache with no invalidation is a defect, not a convenience).
  Dogfood failures the reviewers caught in this very document, now fixed: the Impact
  table omitted six touched files while the doctrine it ships requires every ledger
  row to land there; `## Security and Threat Model` still claimed "the validator is
  untouched" after 65 lines of new path handling; `## Test Strategy` still claimed
  "no behavioral eval scenario"; the superseded elicitation non-goal was left
  standing with the reversal only in the Diary. Battery 65/65.
- **2026-07-28 — 6th increment: second review round.** Asked for before publishing,
  scoped differently on purpose: a **verifier** (given the round-1 findings, told to
  prove each fix by execution and hunt regressions in the never-reviewed new code)
  and a **cold adversary** (no knowledge of round 1, so it could not inherit the
  anchoring). Verifier: PASS — all five blockers genuinely fixed, every behavioral
  claim reproduced on fixtures. Cold adversary: FAIL, two new blockers, both real:
  1. **The closure gate crashed and walked the whole drive.** `cmd_stale`/`cmd_mark`
     never ran audit-plan paths through `confine_under` — the one place that walks
     the filesystem was the one place without the guard every other path input has.
     `init.js` seeded `| / | PENDING |`; mark it and `root / "/"` is the drive, so
     `check` scanned `C:\` and died on `relative_to`. A `../escape` row walked
     outside the project. Pre-existing, but this release is what made
     `audit_plan.md` load-bearing (it is now what converts map silence into a
     groundable MISSING), so it became a blocker. Fixed on both commands + the
     seeder + a `relative_to` guard, with a regression test using both hostile rows.
  2. **A check that could not fire.** `SKILL.md` declared the review clause the sole
     Hybrid check that the pass ran, while the clause read "when the artifact
     carries one" — precisely what a skipped pass does not produce. Now
     unconditional at L3: an artifact with NO ledger is itself a finding.
  Round-2 warnings also fixed: false rot on prose (`app.core`, `OrderStore.save`,
  `1.18.0` — a generic `\.\w{1,5}$` was too greedy; now a closed suffix list),
  the day-zero advisory on a freshly seeded project (worst kind: it trains readers
  to ignore the channel), a case-sensitive heading match that silently disabled both
  the check and its own inertness notice, headerless/ragged tables reported as
  clean, and two zero-cost bypasses of the ledger backstop (delete `level:`; hide
  the heading in an HTML comment). Added the counter-check the brownfield rule was
  missing: an area marked ANALYZED that owns no Component Map row — `mark` is one
  cheap command and it is what makes the map's silence groundable, so the claim
  needed a check. Doctrine: split bullet 2 was still a restatement of bullet 1
  (now: ships on its own cadence, before the feature); the MISSING floor was
  unexecutable — it prescribed a symbol-graph tool for a query that tool cannot
  take, and quantified over "areas the audit plan lists", which is one row on a
  fresh project (now: text-search first, symbol-graph to confirm, triage as the
  stopping rule, provisional MISSING in PENDING areas). Battery 69/69.
- **2026-07-28 — 7th increment: third round, and the lens that had never been
  used.** Two reviewers again, but one of them did something nobody had done:
  **actually used the methodology**, cold, on a 25-file brownfield fixture with
  two components deliberately hidden behind unhelpful names. Static review had
  run three times; usage had run zero times, and it found a different class of
  defect entirely.
  **The convergent BLOCK** (both reviewers, independently): the "mark nobody paid
  for" check harvested backticked refs from the WHOLE `architecture.md`, and the
  canonical template puts `## Directory Structure` — full of backticked paths —
  directly above the Component Map. So the only automated guard that a mark
  asserted something real was **inert on every project that filled in the shipped
  template**. `map_where_refs()` now parses the map's `Where` column only.
  **The other BLOCKs, all from the usage trial:** the guide router is a mandatory
  Rule Zero read whose verdict may not be faked, but `index` refused to write it
  with zero guides and `init.js` never created it — so the required declaration
  was **unsatisfiable on every project's first day** (now: an empty stub is
  written, plus a third legal verdict `router: absent`); `SKILL.md`'s L3 minimum
  sections omitted `## Use Cases / User Needs`, which `review.md` makes a finding
  — an ANALYSIS could pass `check` CLEAN and fail its own closure review; and the
  `level`-missing guard I added in the 6th increment shipped as a **warning**,
  which `--strict` escalates to exit 1 — the exact defect the advisories bucket
  was invented for, reintroduced by me one round later, this time reddening CI on
  every pre-1.18 analysis. Demoted to an advisory and epoch-gated. The same fix
  applies to bootstrap DRAFT visions: the skill *mandates* DRAFT, so `--strict`
  was red on every freshly bootstrapped project until a human ran the blind check
  — teams delete the CI step rather than block on it.
  Also fixed: multi-line HTML comments leaked into the generated manifest (the
  vision row read `... -->`, and the manifest is what every future agent reads to
  orient); `Next.js`/`Node.js`/`OrderStore.save` were reported as rotting paths;
  `mark` printed `[ok] ... ANALYZED` for paths it then discarded; the gate message
  told the author to do what they had just done instead of naming the one-line
  remedy; and `elicitation.md` gained the unattended path the trial had to
  improvise (declared assumptions + BLOCKED, never a silent guess).
  **What the trial says worked** (recorded so it is not refactored away): the
  "noun + at least TWO synonyms + verb" clause is load-bearing — the domain noun
  alone returned **zero hits** for both hidden components, and the synonym clause
  found both; "silence is unread, not empty" made a confident MISSING
  *doctrinally unavailable* on a virgin repo; and the ledger's Evidence column
  turned a lookup into comprehension — re-reading the found component surfaced a
  4×-per-worker defect that no file-level impact analysis would have asked about,
  which the Silent-degradation rule then routed to the user as a scope decision.
  **The honest negative**: the trial ruled ceremony proportional at the feature
  level and **not** proportional at the arrival level — the first L3 in any repo
  pays a full product-Vision authoring round (~1,000 words) regardless of the
  task's size, because the incremental licence covers the audit map and pointedly
  not the Vision. Not fixed here: it is a Vision-level scope decision for the
  owner, recorded as the top open item. Battery 73/73.
- **2026-07-28 — 8th increment: fourth round, narrow by design.** Scope declared
  up front: verify the 3rd round's dispositions and hunt regressions in the code
  it introduced — no re-reading of doctrine, no new philosophy. Nine fixes
  verified by execution; eight landed. **The BLOCK was mine**: the router-stub fix
  replaced `if guides and not router: ERROR` with an unconditional advisory, so a
  project that HAS guides but lost its router (gitignored, dropped by a merge)
  reported CLEAN — the agent's mandatory lookup finds nothing, legally declares
  `router: absent`, and the guide governing the work is never consulted. An absent
  router was graded *below* a merely stale one. Restored as an error when guides
  exist; the advisory now covers only the zero-guide case.
  Three more of my own defects, all the same shape — **a fix whose blast radius I
  did not measure**: (a) the advisory told users to write `owns no component` in
  the audit-plan Notes column, and nothing read that column — a documented escape
  hatch that was fiction, which is exactly the "trains readers to ignore the
  channel" failure the surrounding code exists to avoid; now implemented. (b) The
  unterminated-comment strip nuked to end-of-file, so an ANALYSIS that merely
  *mentions* `<!--` inline, or shows an unclosed example in a fenced block, was
  told it had no Capability Ledger when it plainly did; heading detection moved
  into `has_ledger_heading()` which strips fences first and only opens an
  unterminated comment at line start. (c) The CamelCase exclusion I added to stop
  `Next.js` being reported as rot silenced 22 of 39 probed filenames — `App.tsx`,
  `Program.cs`, `Main.java`, `Cargo.toml`: precisely what React/C#/Java projects
  put in a `Where` cell. Narrowed to the one real class, a CamelCase stem with a
  `.js` tail.
  **And an invariant of mine was theater**: `test_ledger_backstop_bypasses_closed`
  asserted `cmd_validate(...) == 0`, but advisories never move the exit code — the
  reviewer replayed the fixture against the PRE-fix module and it passed. The test
  now asserts on `has_ledger_heading()` directly, including the two false-positive
  cases. Also: the manifest description fallback emitted markdown table rows
  (`| Milestone | Expected Benefit |`) as descriptions; table rows and bare
  bullets are skipped now. Battery 73/73, fresh project `--strict` rc=0.
  Deferred, recorded not silently dropped: `functional/*` docs lack `status:` so
  this repo cannot pass its own `--strict` recipe (pre-existing, devPNT-generated);
  an escaped `|` in a Where cell still shifts columns in `map_where_refs`; and the
  two `vision/` docs would read better in the manifest with real `description:`
  frontmatter — but one of them is the APPROVED Vision, and editing it to improve
  a manifest row is not proportionate to the gain.
