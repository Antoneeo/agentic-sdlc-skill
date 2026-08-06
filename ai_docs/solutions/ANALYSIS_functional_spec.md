---
id: F-033
feature: Functional Spec — the readable WHAT + the strategic pass as one search with four open buffers
status: COMPLETED
level: L3
start_date: 2026-08-06
end_date: 2026-08-06
---
# Feature Analysis: Functional Spec + strategic-pass loop (F-033)

## Objective
Close the last unowned governance slot: nothing in the chain produced a single readable
statement of the complete observable behavior — the object a person validates ("is this
what we want?") and the AI conforms to. And encode the owner's model of the strategic
pass: one search, four open buffers, finalization-ordered — not four sequential phases.

## Feature Vision
Advances the Vision's "divergence visible before implementation" and the Actors' good-UX
clauses (same family as r16/Interface Contract — that admitted the interaction GEOMETRY;
this admits the behavior SEMANTICS). Actors: the owner (validates the WHAT as one object
instead of implicitly across four documents) and the agent (designs against a behavior
contract instead of re-deriving intent). Non-goal: no new file kind — the spec is an
ANALYSIS section; the extract-to-file escape stays the `VISION_[feature]` pattern, unused
until observed need. Admission: rulings r17, owner acceptance 2026-08-06.

## Use Cases / User Needs
- The owner reads one component-free section and answers "is this what I want built?"
  before any design exists. (Grounding: "ANALYSIS section" EXISTS; "Functional Spec" NEW,
  declared by this change.)
- The agent, mid-design and at closure review, checks the design/diff against stated
  behavior instead of arguing over what was meant — the observed root of second review
  rounds. Traces to "divergence visible before implementation".

## Functional Spec
Behavior of the feature itself (dogfood):
- When an L3 change adds or alters observable behavior, the ANALYSIS carries a
  `## Functional Spec`; when the trigger does not fire, the section holds one line saying
  why. An L3 artifact with behavior change and no such section fails its closure review.
- A component, file or mechanism named inside the section is reported by the review as
  Solution-leakage; the author moves it (component → Interface Contract, mechanism →
  Impact).
- Acceptance criteria: (1) review.md ×3 carries the Functional Spec clause and fires only
  in a lens whose template defines the section; (2) the batteries pass unchanged in kb/mkt
  (inert there); (3) templates.md owns the trigger definition, SKILL.md and review.md cite
  it without restating.

## Interface Contract
Not fired — the change alters authored doctrine text; it creates no runtime surface an
actor acts on or perceives.

## Capability Ledger
- Conditional-section machinery — EXISTS (`templates.md` section comments as owning
  definitions; the Interface Contract established the pattern).
- Lens-conditional review clause — EXISTS (`review.md` "fires only in the lens whose
  template defines the section", shared spine).
- Spine propagation — EXISTS (`shared_files.py` manifest + drift guard).

## Impact
- `skills/agentic-sdlc-skill/templates.md` — new `## Functional Spec` section (owning
  definition); Interface Contract authority split now cedes behavior semantics to it.
- `skills/agentic-sdlc-skill/SKILL.md` — strategic-pass loop frame (fixed/free/constraints
  /objective, four open buffers, finalization order, Vision-frame halt); Functional Spec
  paragraph; minimum-sections list; Hybrid: stale "IC lives in the E-ISP" corrected to
  governed `D-IC`, strategic-bundle pointer added, FS rides in the E-ISP until a `D-FS`
  exists.
- `review.md` ×3 (spine) — Functional Spec clause (absence finding, Solution-leakage,
  case coverage, acceptance↔Test Strategy, UC↔FS↔IC cross-checks).
- `ai_docs/`: this ANALYSIS, `ADR_2026-08-06_functional_spec_layer.md`, rulings r17.
- Version bumps ×4 points ×3 distributions; CHANGELOG ×3; shared manifests ×3.

## Security and Threat Model
Doc-only change; no runtime surface, no dependency, no execution path. Supply-chain
unchanged (same files, same packaging).

## Action Plan
All done in one pass: templates → SKILL → review ×3 → ai_docs → bumps → batteries →
independent review → release.

## Test Strategy
`test_skill_invariants.py` ×3 (template tokens still parseable, version points agree),
`test_drift.py` ×3 (spine identical), `sdlc_check.py validate` clean (0 errors; `stale`
rc=1 is pre-existing audit-mark debt from 1.22.0, not this change), golden regression
untouched (no validator change). Independent closure-style review on the full diff before
commit (logged in REVIEW_LOG; outcome in Diary).

## Diary / Current State
2026-08-06 — Designed in conversation with the owner (his formulation: the agent searches
how actors obtain from components what the VISION prescribes, risks mitigated in-loop,
architecture respected, quality/maintainability optimized; capture immediate, order only
at finalization). Independent closure review R1 FAIL (1 BLOCK: SKILL.md's IC paragraph
still claimed "observable behavior" after templates.md ceded it to the FS — fixed to
"observable interaction (behavior semantics are the Functional Spec's)"; 1 WARN: this
file's check-clean claim corrected, review logged) → R2 PASS on the fixes. Released as
code 1.25.0 / kb 1.4.5 / mkt 0.4.5.
