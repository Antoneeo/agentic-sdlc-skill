---
description: Why course creation owns its teaching artifacts while the shared core owns the ai_docs index.
status: CURRENT
---
# ADR: Course overlay and one shared index writer

**Status:** Accepted
**Date:** 2026-09-27
**Task ref:** F-058, `ANALYSIS_course_creator.md`

## Context

`course_creator` needs learner profiles, a prerequisite graph, module explanations and diagnostic simulation on the family's `ai_docs/` tree. The marketing entry point previously wrote its own `ai_docs/INDEX.md` format. Installing both lenses in one project would let `index` alternate that file between incompatible formats. The approved F-058 Vision requires a standalone course skill and does not authorize a second source of governance for the same course.

## Decision

The shared core writes `ai_docs/INDEX.md`; code, KB, marketing and course entry points delegate to it on that tree. Marketing keeps its existing writer on `mkt_docs/`. Its aggregate `check` runs specialist checks on `ai_docs/` when a marketing engagement is signaled; explicit specialist commands remain available. A legacy marketing-format `ai_docs/INDEX.md` receives an explicit migration diagnostic and is never silently rewritten during validation.

The course overlay owns only teaching-specific artifacts and checks. Each course has one canonical `VISION_course_<slug>.md` and one `ANALYSIS_course_<slug>.md` with explicit `domain: course`; detail files cite the ANALYSIS IDs. The shared core owns triage, workstream state and memory. `course_check.py` checks structural links, not teaching quality, factual truth or human efficacy.

## Alternatives considered

- Keep two index writers on `ai_docs/`: the same input tree would have two incompatible generated outputs, so validation would depend on the last entry point invoked.
- Give the course an unrelated docs root: this would break cross-domain memory and duplicate project governance.
- Make course detail files another set of governed Hybrid documents: this would duplicate ownership in the initial Standalone scope.

## Consequences

- All four entry points can regenerate the same `ai_docs/INDEX.md`; the post-implementation comparison and hash are recorded in `ai_docs/solutions/harness_course_creator/FAMILY_INTEGRATION_PROBE.md`.
- A marketing-only `mkt_docs/` project retains its established format and checks. Migration of an older shared `ai_docs/` index is visible work.
- The course validator and method can evolve without changing the shared core's index schema. Independent learner simulations remain diagnostic; efficacy stays unverified without suitable evidence from people.
