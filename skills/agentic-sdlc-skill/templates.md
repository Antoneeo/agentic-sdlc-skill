# Document templates — Agentic SDLC

General rules:
- Concise documents: ≤ ~80 lines each (handoff ≤ 20). If a document grows beyond that, split it, do not inflate it.
- Template conformance is not the goal: if a section has no real content, state explicitly why it does not apply. Never filler text.
- Dates always absolute, UTC where indicated.

## Canonical document header (vision/ reference/ architecture/ functional/ strategic/)

Every durable canonical document opens with this frontmatter: it feeds the generated manifest `ai_docs/INDEX.md` and gives an agent the freshness signal before it trusts the content.

```markdown
---
description: One line — what the document is and when to read it.
status: CURRENT              # CURRENT | SUPERSEDED | DRAFT | DEPRECATED
supersedes: old_doc.md       # only if it replaces another canonical doc
---
# Document Title
```

When a doc replaces another: the new one declares `supersedes:`, the old one switches to `status: SUPERSEDED` (it stays as history, do not delete it). `sdlc_check.py validate` warns if `status` is missing or if a superseded doc is still `CURRENT`.

## ai_docs/reference/GUIDE_[topic].md

Operative guide distilled from USER-PROVIDED indications (never from model knowledge).
The verbatim source snapshot lives in `ai_docs/reference/.sources/<slug>-<hash8>.md`;
`source_hash` is the snapshot's SHA-256. Every `##` section carries a fidelity marker:
`[source: <snapshot-file>#<anchor-or-line>]` for covered content, or a literal
`[not covered by source]` for gaps. Sections are CHOSEN from the repertoire below —
only those the source actually supports; never force empty ones.

```markdown
---
description: One line, ≤160 chars — when to consult this guide.
status: CURRENT
source: Human-readable name of what the user provided.
source_version: v1.2          # optional — only when the origin is versioned
distilled_from: ai_docs/reference/.sources/topic-a1b2c3d4.md
source_hash: <sha256 of the snapshot file>
---
# Guide: [Topic]

## How to do [X]
[source: topic-a1b2c3d4.md#setup]
<!-- operative steps, imperative voice -->

## How to verify it is done right
[source: topic-a1b2c3d4.md#checks]

## What NOT to do
[not covered by source]
<!-- the user's material does not address this: do not invent. -->
```

Section repertoire (pick what the source supports): How to do X / How to verify /
What NOT to do / What to watch out for / Core principles / When this applies.

## ai_docs/README.md

Curated must-read index, by hand (it is NOT the generated manifest). Created at init, updated rarely, only for real must-reads.

```markdown
# ai_docs — reading guide

Must-reads for this project, in order. The full manifest of canonical docs is
`INDEX.md` (generated — regenerate with `sdlc_check.py index`, never edit by hand).

1. `vision/project_vision.md` — why the project exists (check its Status first).
2. `strategic/architecture.md` — how it is built.
3. `audit/handoff.md` — where work stopped last session (if present).

Directory purposes: `vision/` (project direction), `strategic/` (architecture and
feature catalog), `reference/` (operative guides), `solutions/` (per-feature
analyses, discovery-by-grep), `audit/` (audit plan and handoff).
```

## ai_docs/vision/project_vision.md

```markdown
# Project Vision
Status: DRAFT
<!-- Status: DRAFT (reconstructed by the agent, NOT a gating authority)
     or APPROVED (by <who>, <date>) — only after the user's explicit confirmation -->

## North Star
## Target Users
## Core Problem
## Goals
## Non-Goals
## Success Signals
```

## ai_docs/vision/roadmap.md

```markdown
# Roadmap
Status: DRAFT

## Milestones
<!-- for each: expected benefit, priority, progress indicator -->
```

## ai_docs/vision/principles.md

```markdown
# Decision Principles
Status: DRAFT

<!-- bullet list of the stable principles guiding trade-offs and scope, most critical first -->
```

## ai_docs/vision/features/VISION_[feature_name].md

Only for features spanning multiple ANALYSIS documents or multiple milestones: otherwise the feature vision lives in the `## Feature Vision` section of the ANALYSIS.

```markdown
# Feature Vision: [Name]

## Problem
## Expected Benefit
## Users or Stakeholders
## Success Signals
## Non-Goals / Out of Scope
## Related Constraints and Principles
```

## ai_docs/solutions/ANALYSIS_[feature_name].md

The frontmatter is the source of truth for the feature state (the `features_history.md` index is generated from it).

```markdown
---
id: F-001
feature: Feature Name
status: PLANNED
level: L3
start_date: 2026-06-11
end_date:
---
# Feature Analysis: [Name]

## Objective
<!-- what we want to achieve and which problems it solves -->

## Feature Vision
<!-- expected benefit and problem solved; alignment with the project vision
     (cite the document and its DRAFT/APPROVED state); non-goals/out-of-scope
     for this feature; success signals; stakeholders only if not obvious.
     This is the single home of the feature vision: the separate file
     VISION_[feature].md is created only if the feature spans multiple
     ANALYSIS documents or multiple milestones. -->

## Impact
<!-- existing files touched, APIs/contracts, performance, new dependencies -->

## Security and Threat Model
<!-- ALWAYS mandatory, also in Standalone.
     Surfaces touched: external input, authN/authZ, cryptography, network, personal data, filesystem.
     Main threats and mitigations. "No security impact" must be justified, not declared. -->

## Action Plan
- [ ] ...

## Test Strategy
<!-- AAA unit tests, integration, examples. If the environment is not executable (firmware/HIL):
     explicit alternative verification and reason. -->

## Diary / Current State
<!-- updated at every milestone: where I am, last problem, next step.
     It is the handoff source for this feature. -->
```

Allowed frontmatter states: `PLANNED` | `IN_PROGRESS` | `COMPLETED` | `CANCELLED`. `COMPLETED` requires `end_date`. (The validator also accepts the deprecated Italian keys `stato`/`livello`/`data_inizio`/`data_fine` in existing projects.)

## ai_docs/solutions/SPIKE_[topic].md

```markdown
# Spike: [topic]

## Question to answer
## Time-box
## What was tried
## Answer / Outcome
## Consequences
<!-- max 1 page. Spike code is NOT mergeable: for production reclassify L2/L3. -->
```

## ai_docs/audit/audit_plan.md (Standalone mode only)

The `Reference` field (git hash or ISO UTC timestamp) is managed by `sdlc_check.py mark` — do not fill it by hand. Freshness is verified with `sdlc_check.py stale`.

```markdown
# Audit Plan

States: PENDING (to analyze) | ANALYZED (analyzed, with reference) | SKIPPED (with reason).

| Path | Status | Reference | Notes |
|---|---|---|---|
| src/core/ | PENDING | - | |
| vendor/ | SKIPPED | - | vendored code |
```

## ai_docs/audit/handoff.md

Just a pointer, ≤ 20 lines. The detail lives in the Diary of each ANALYSIS.

```markdown
# Handoff
Date: 2026-06-11 (UTC)
Branch: feature/sso-login
Agent: Claude

## Active features
- F-001 — see solutions/ANALYSIS_login_sso.md (Diary section)

## Next step
<!-- one line -->

## Session notes
<!-- visions read this session? drafts to have validated? -->
```

## ai_docs/strategic/architecture.md and existing_features.md

Canonical docs: they open with the header (`description:`/`status:`) so they enter the `INDEX.md` manifest cleanly.

```markdown
---
description: Stack, directory structure and architectural patterns of the project.
status: CURRENT
---
# Project Architecture
## Technology Stack
## Directory Structure
## Architectural Patterns
```

```markdown
---
description: Concise catalog of the project's existing features.
status: CURRENT
---
# Existing Features
- [ID] **Feature Name**: Description
```

`ai_docs/strategic/features_history.md` and `ai_docs/INDEX.md` have NO template: they are generated by `sdlc_check.py index`.
