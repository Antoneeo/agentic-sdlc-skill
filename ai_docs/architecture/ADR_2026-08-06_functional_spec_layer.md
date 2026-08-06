---
description: Why the observable WHAT gets its own component-free section (Functional Spec) between the use cases and the Interface Contract, and why the strategic pass is one search with four open buffers rather than four phases.
status: CURRENT
---
# ADR: Functional Spec layer + the strategic pass as one search

**Status:** Accepted
**Date:** 2026-08-06
**Task ref:** F-033 (owner design conversation, 2026-08-05/06)

## Context
The chain validated needs (Use Cases), interaction geometry (Interface Contract), threats
(TM) and solution (Impact) — but never the complete observable BEHAVIOR as one readable
object. The WHAT was distributed across four documents, so "is this what we want?" was
answered implicitly, and review rounds argued over what was meant. Separately, the
authoring model was misreadable as four sequential phases, forcing thoughts to wait for
"their" document — hostile to how the reasoning actually happens (and to an LLM agent,
whose working memory is its context).

## Decision
1. A conditional `## Functional Spec` ANALYSIS section between Use Cases and Interface
   Contract: the complete observable WHAT — rules, cases (normal/edge/error/state),
   acceptance criteria — **component-free by construction**. Authority split: UC owns WHY,
   FS owns WHAT, IC owns THROUGH-WHAT, Impact owns HOW. Fires on behavior change; internal
   refactor exempt with one line. Owning definition in `templates.md`; `review.md` (spine,
   lens-conditional) enforces: absence on behavior change, Solution-leakage inside the
   spec, uncovered cases, acceptance criteria without tests, UC↔FS↔IC coverage.
2. The strategic pass is defined as ONE search: actors + Vision fixed; components,
   interfaces, flows free (declared changes only); risks mitigated in-loop; architecture
   and patterns respected; quality/maintainability the objective; Poka-Yoke and DRY the
   selection criteria between hypotheses. The four sections are open buffers — capture is
   immediate wherever the thought belongs; the order UC → FS → IC → TM binds only
   finalization and reading. Vision divergence halts the pass.

## Alternatives considered
- **Extend the Interface Contract to carry behavior semantics** — rejected: conflates
  geometry with semantics; the owner explicitly separated them ("la IC è simile ma non è
  quella"). Two documents with one owner each beats one document with two jobs.
- **A separate `FS_[feature].md` file** — rejected for now: no observed need for an
  extractable stakeholder document; the `VISION_[feature]` extract-on-need pattern already
  exists as the escape. A new file kind is lifecycle machinery the gap does not require.
- **devPNT governed `D-FS` first** — rejected as ordering: a new governed artifact is
  milestone-worthy (M47 precedent: Vision Gate, schema, chain, implementation). The shape
  is validated in the skill first; `D-FS` is devPNT-side work later. Until then the FS
  rides in the `E-ISP` above the Impact Map — exactly the slot the Interface Contract
  occupied before `D-IC` existed.
- **Keep sequential-phase authoring** — rejected: the reasoning is one act; deferring
  capture to respect a writing order loses thoughts (context is working memory) and was
  already contradicted in miniature by "drafting interleaves" (IC + Ledger).

## Consequences
- **Pro:** the funnel now validates WHY (grounded), WHAT (readable), THROUGH-WHAT
  (walkable), risks and HOW — each with one owner; review rounds get a behavior contract
  to check against instead of reconstructing intent; capture-immediately matches how
  agents actually reason.
- **Con / risk:** the ANALYSIS grows by one conditional section and the bundle by one
  projection — accepted by the owner with the cost disclosed; the compensation (fewer
  what-was-meant review rounds) is measurable in the REVIEW_LOG over time.
