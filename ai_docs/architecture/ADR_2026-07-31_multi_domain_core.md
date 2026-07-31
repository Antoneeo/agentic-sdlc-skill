---
description: Why the three lens skills become one shared core with per-domain overlays, on one ai_docs/ tree, with a project-level domain default and a rule set split into an exclusive part plus portable checks.
status: CURRENT
---
# ADR: One shared core, three lenses, one docs tree

**Status:** Accepted
**Date:** 2026-07-31
**Task ref:** F-022 (`ai_docs/solutions/ANALYSIS_multi_domain_core.md`)

## Context

Three skills exist — `agentic-sdlc` (code), `kb-agentic` (knowledge),
`mkt-agentic-sdlc` (marketing). They are copy-forks of one spine and have already
drifted in opposite directions: kb was byte-copied and broke against its own missing
overlay files, mkt rewrote the spine (a 2058-line diff). Nothing detects divergence:
searching `sync`, `drift`, `generate` and `build` across all three `scripts/` trees
returns no mechanism, and none of the three has a CI workflow.

The owner's requirement made coexistence, not separation, the target: an agent may have
several lenses installed at once, must know which one governs the work in front of it,
and every lens must be able to use the knowledge already deposited under `ai_docs/`.
That last clause rules out per-lens document trees — DRY has to hold for written
documentation too, or the same fact ends up in `ai_docs/` and `mkt_docs/` and the two
diverge at the first edit.

Four decisions had to be taken together, because each one falsifies the obvious
answer to the next.

## Decision

1. **One authored core, three verbatim copies.** The spine is authored once as
   `scripts/sdlc_core.py` and copied into each distribution, with `sdlc_check.py` and
   `mkt_check.py` as thin domain entry points. Membership is an explicit per-file
   manifest — file → the distributions that must match it — and a drift guard fails CI
   on any divergence.
2. **`ai_docs/` is the one surviving root.** Every lens reads and writes the same tree;
   `mkt_docs/` is migrated. A document belongs to exactly one **owning domain** — the
   domain whose fidelity discipline names the source it was written from — and a second
   domain cites it rather than copying it.
3. **The domain default is resolved at project level.** `default_domain:` in
   `ai_docs/README.md`, seeded once by whichever `init` created the project, absent →
   `code`. An artifact may override it with `domain:`; nothing else decides.
4. **The rule set splits in two.** An **exclusive** part with exactly one owner per
   document (template, mandatory sections, the risk slot — `## Security and Threat
   Model` for code, `## Sources and Verification` for knowledge, `## Threat Map / Plan
   Risks` for marketing), plus **portable checks** imported by name through `checks:`,
   which may only add findings, never relax a requirement.

Which lens owns a unit of work is decided by a router (`routing.md`) that runs after
the triage level and only when a sibling lens is installed — doctrine the agent
applies, with no validator code behind it.

## Alternatives considered

- **Keep three independent skills** — rejected: it is the status quo that already
  drifted twice, and it cannot satisfy the shared-knowledge requirement at all.
- **Merge into one skill with modes** — rejected: every domain would pay the other
  domains' ceremony at L1, which the Vision's ceremony budget forbids, and the
  descriptions that make an agent pick the right skill would collapse into one.
- **A package generator producing the three distributions** — rejected as too much
  machinery for three consumers; the verbatim-copy-plus-guard costs one test and makes
  divergence visible instead of impossible-by-construction. Accepted honest cost: until
  the build step lands, an edit is applied three times and the guard catches a missed
  copy.
- **A per-distribution domain default** — rejected mid-design: two lenses installed
  over one tree would return two different verdicts on the same file. Project-level
  resolution is what makes the answer entry-point-independent.
- **Union or intersection of the three rule sets** — rejected: union demands every
  domain's ceremony of every document, intersection demands nothing. The exclusive part
  never composes, which is exactly why it is separated from the checks that do.
- **A mandatory `cites:` field** for cross-domain references — rejected as a ceremony
  ratchet; C5 naming plus a review clause carry it, with stale citations recorded as a
  declared residual and optional version pinning left as a candidate.
- **Per-domain document trees** (`kb_docs/`, `mkt_docs/`) — rejected: it is the DRY
  violation the owner named explicitly.

## Consequences

- **Pro:** one place to fix a spine bug; a lens is added by writing an overlay, not a
  fork; every lens sees the whole `ai_docs/` corpus; existing `agentic-sdlc` projects
  are untouched (no `default_domain` → `code`, no `domain:` fields → no behaviour
  change, the router unreachable at L1 and unread without a sibling).
- **Con / risk:** three copies to keep in step until the build step lands (guarded by
  CI, not by discipline); a migration is owed to every project with a non-`ai_docs/`
  root; nothing detects that a cited owner changed between reviews; the guide router
  (`ai_docs/reference/INDEX.md`) gains no domain column, so domain-qualified naming is
  its only mitigation on the surface every L2/L3 task reads.
