---
id: F-015
feature: Code-Comprehension Guides
status: IN_PROGRESS
level: L3
start_date: 2026-07-19
end_date:
---

# ANALYSIS — Code-Comprehension Guides

## Objective

Give the agent a durable, source-faithful **comprehension guide** for a complex
component / feature / abstraction layer, so a later session starts with the map
instead of re-deriving it and breaking the thing from partial understanding.
Realize it as an **extension of the existing `reference/GUIDE_[topic].md`** (one
guide concept, generalized to a code-derived source), and let the agent write it
**autonomously** — as a duty, when it judges the topic complex enough — not via a
human-gated proposal.

Two author decisions frame this (from the design round, 2026-07-19):
1. **Extend GUIDE_ to code** (not a new `strategic/MODEL_` type).
2. **Autonomous write, no human gate** — "if the agent deems it useful and
   appropriate it is its duty to write the GUIDE."

## Feature Vision

Vision Alignment (sign-off resolved 2026-07-19). `project_vision.md` is **APPROVED**
and currently defines the guide layer (Layer D)
as *"source-faithful **operative** guides **from user indications**"* — the original
differentiator. This feature widens that on two axes:

| Vision element (as approved) | This feature | Amendment |
|---|---|---|
| "from user indications" (origin = user) | origin also = the codebase | Layer D origin broadened to "user indications OR the project's own code" |
| "operative" (purpose = how to operate) | purpose also = comprehension (how it works) | Layer D purpose broadened to operative **and** explanatory |
| "source-faithful" | preserved — source = verbatim code excerpts, hashed | none (intent honored) |

**Decision: B (signed off 2026-07-19).** Cross-session code comprehension is a
**distinct capability, homed under Layer A** (Documentation-First with a real
document lifecycle applied to code understanding) — NOT folded into Layer D. Why B
over A (amend D's wording): (1) keeps the A/B/C/D map honest — code comprehension is
parity-done-well (architecture docs, codebase RAG, devPNT KL all do it), not the
"nobody has it" novelty D claims, so wearing D's badge would violate Success Signals
#1/#2; (2) natural fit — A already owns "durable across sessions"; (3) lower blast
radius — one additive line to A, **D's differentiator sentence untouched**.
Mechanism is unchanged: still one GUIDE_ artifact, `source_kind` self-identifies
(`document` = D operative, `code` = A comprehension).

Two doctrine invariants are also amended (both scoped, both reconciled below):
- *"Never from model knowledge"* → *"Never from UNVERIFIED knowledge"*: a code guide
  is still snapshot-anchored (verbatim code excerpts), never narrated from the model's
  head. The anti-hallucination floor holds; this is a generalization, not a hole.
- *"Never a silent write / propose"* → **scoped** relaxation: code-comprehension
  guides may be written autonomously because they are **additive, code-anchored,
  reversible** (git). Operative user-origin guides KEEP propose/confirm (they carry
  user material + scope/fragmentation/location decisions that need the user).

## Use Cases / User Needs

- **Solo developer (Actor)** — re-enters a complex subsystem next session and needs
  the map immediately; good UX = "never re-explaining the project across sessions"
  (the Vision's own actor UX). The comprehension guide IS that persistence.
- **Team lead (Actor)** — many agents/clients touch the same complex component;
  good UX = one shared, source-faithful understanding, not N re-derivations that
  drift.

## Impact

Mechanism = **reuse the guide machinery, change only the source-gathering**. A
comprehension guide is a normal `reference/GUIDE_[topic].md` with a new frontmatter
field `source_kind: code` (existing guides are implicitly `source_kind: document`).
Its `.sources/` snapshot is the **verbatim curated code excerpts** it explains
(key files/functions), hashed exactly as today. `stale` hash-drift, `index`, the
router and every fidelity marker work **unchanged** — snapshot+hash is source-agnostic.

| Path | Change | Why |
|---|---|---|
| `guides.md` | MODIFY | §1 gains the autonomous code-comprehension trigger (signal list + duty, no proposal); §2 snapshot step allows assembling `.sources/` from verbatim code excerpts; §3 fidelity generalized to `source_kind`; note `stale` works unchanged. Biggest change. |
| `SKILL.md` | MODIFY | Operative Guides section gains the comprehension/autonomous moment; Write Triggers `GUIDE_` row gains the code-comprehension trigger; consult trigger (Phase 4) already covers reading it — confirm wording. |
| `templates.md` | MODIFY | `GUIDE_[topic].md` frontmatter gains `source_kind` (+ a comprehension body repertoire: "How it works / Data & control flow / Invariants / Where people break it"). |
| `debugging.md` | MODIFY | Root-cause that reconstructs an unwritten mental model → duty to capture it as a comprehension guide (natural trigger point). |
| `scripts/test_skill_invariants.py` | MODIFY | Assert the new trigger string is present + wired; keep the battery green. |
| `ai_docs/vision/project_vision.md` | MODIFY (pending sign-off) | Layer D wording amendment per the gate above. |

Validator (`sdlc_check.py`) — **no change** (snapshot+hash is already source-agnostic).

## Trigger design (the core ask — "di sua sponte")

Autonomous **duty**, agent judgment informed by concrete signals (so it fires
consistently, not on vibes). During L2/L3 work, when the agent recognizes a
component/feature/layer is high-complexity AND no CURRENT comprehension guide
covers it, it is the agent's duty to write one. Signals (any strong combination):
- high comprehension cost — had to trace across several files/modules; summaries
  were not enough (crossed from map into territory);
- high fan-in / blast radius (many consumers — the blast-radius enumeration surfaces it);
- non-obvious control/data flow — state machine, async/eventing, DI/plugin
  indirection, metaprogramming, cross-cutting invariants;
- prior breakage from partial understanding (handoff/diary/git shows it);
- non-local rationale — the "why" is not reconstructable from one file.

Guard-rails (autonomous ≠ unconstrained): DRY search-before-create (one CURRENT
guide per topic, both routers); fidelity floor (every claim → snapshot code excerpt,
gaps `[not covered by source]`); recommend the independent guide-vs-source review
(more important now that no human gates creation); announce the autonomous write in
the closure/handoff.

## Security and Threat Model

- **T1 — wrong map (hallucinated/misread code).** A confident-wrong guide is worse
  than none. Mitigation: fidelity floor (claims trace to verbatim code excerpts),
  independent guide-vs-source review recommended, `stale` on drift.
- **T2 — staleness as code evolves.** Mitigation: snapshot-hash `stale` (unchanged)
  + update-with-code closure rule (docs travel in the same commit) + `status:`.
- **T3 — autonomous-write scope creep / noise.** Mitigation: signal-gated duty
  (high-complexity floor), DRY one-per-topic, targeted router consult (never blanket).
- **T4 — the "silent write" relaxation leaking to other artifacts.** Mitigation:
  scope the relaxation EXPLICITLY to code-`source_kind` comprehension guides; code,
  plans, governed artifacts and user-origin guides stay propose/confirm.

## Action Plan

1. **Vision sign-off** — author confirms the Layer D amendment (or the "distinct
   capability" framing). GATE — nothing below starts until resolved.
2. `guides.md` — add `source_kind: code`: trigger (§1), code-excerpt snapshot (§2),
   fidelity generalization (§3), autonomous-duty rule + guard-rails.
3. `templates.md` — `GUIDE_` frontmatter `source_kind` + comprehension repertoire.
4. `SKILL.md` — Operative Guides moment + Write Triggers row + consult wording.
5. `debugging.md` — capture-the-model trigger at root-cause.
6. `project_vision.md` — Layer D amendment (same commit).
7. `test_skill_invariants.py` — assertions for the new wiring.
8. Dogfood — write one real comprehension guide for a genuinely complex part of THIS
   repo (candidate: `sdlc_check.py` index/stale engine) to validate the mechanism.
9. Closure — eval battery green, `index` regenerates routers, docs travel together.

## Test Strategy

- Eval battery (`python -m unittest discover -s scripts -p "test_*.py"`) stays green;
  add invariant assertions for the new trigger/`source_kind` wiring.
- No validator code change → `stale`/`index` behavior unaffected (confirm green).
- Behavioral dogfood (step 8) is the real proof: does a context-free next session,
  handed only the comprehension guide, understand the component well enough to change
  it safely?

## Diary / Current State

- 2026-07-19 — Design round complete (2 author decisions). Mechanism settled: extend
  GUIDE_ via `source_kind: code` + verbatim code-excerpt snapshot; validator untouched.
  devPNT OFF this session (locked on another project) → Standalone L3.
- 2026-07-19 — Vision sign-off: **B** (home under Layer A, D untouched). Action Plan
  #2–#7 DONE: `guides.md` (source_kind + autonomous comprehension trigger §1, code
  snapshot §2.3, fidelity generalization §3, code freshness §6), `templates.md`
  (`source_kind` + comprehension repertoire), `SKILL.md` (4th "Comprehend" moment +
  Write-Triggers `code` row + consult wording), `debugging.md` (capture-the-model
  trigger), `project_vision.md` (Layer A line), eval battery (+1 wiring test).
  **Eval battery 52/52 OK; repo `validate` 0 errors.** `sdlc_check.py` unchanged, as
  designed. **Pending: #8 dogfood** (write one real `source_kind: code` guide to prove
  the mechanism end-to-end incl. validator acceptance + router listing) → then close.
- 2026-07-19 — **Blind comprehension test** (independent fresh agent, skill-only, no
  hints): the new trigger is discoverable + correct — a blind agent reached "duty to
  autonomously write a `source_kind: code` guide" from the regression/complexity
  scenario, citing guides.md §1 + the debugging bridge; all controls (L3 triage,
  circuit breaker, handoff) passed. Surfaced 3 rough edges, all fixed this turn:
  **F1** (MEDIUM) — skill answered the "understand" half but was silent on "complexity
  out of control" → added the *chronic-fragility* discipline to `debugging.md` (two
  duties: write the code guide AND escalate a refactor as its own L3; stop patching)
  + a SKILL.md circuit-breaker pointer. **F2** (LOW) — added "repeatedly across
  sessions" to the comprehension signal (guides.md §1) + the Write-Triggers `code`
  row. **F3** (MINOR) — Phase 4 Diary trigger now names "session ends with work
  unfinished". Battery 52/52, validate 0 errors.
- 2026-07-19 — **Blind re-test** (fresh agent, changed skill): F1/F2/F3 confirmed
  closed; adversarial + autonomy-boundary probes PASSED (agent refused a
  general-knowledge guide; the scoped autonomy relaxation did NOT leak — refactor
  still user-gated, own-knowledge operative guide still forbidden). Two new LOW
  findings, both applied: **G6** — "Understand before acting" now names cross-session
  source-memory rot (re-read even when you think you remember); **G7** — SKILL.md gains
  a top-line thesis (the skill exists to prevent *myopia*). Battery 52/52, validate 0
  errors.
