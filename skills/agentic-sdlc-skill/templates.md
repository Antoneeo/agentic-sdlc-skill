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

A guide is either OPERATIVE (`source_kind: document` — distilled from USER-PROVIDED
indications, "how to act") or a COMPREHENSION map (`source_kind: code` — distilled from
the project's own code, "how a complex component works"). Never from model knowledge:
every claim traces to the snapshot (a handed document, or verbatim code excerpts).
The guide is a SYNTHESIS — the compact training a reader takes in whole before acting;
the verbatim snapshot in `ai_docs/reference/.sources/<slug>-<hash8>.md` is the book,
reached on demand. `source_hash` is the snapshot's SHA-256. Every `##` section carries
a fidelity marker: `[source: <snapshot-file>#<anchor-or-line>]` for covered content
(doubling as the detail-lookup pointer into the book), or a literal
`[not covered by source]` for gaps. Sections are CHOSEN from the repertoire below —
only those the source actually supports; never force empty ones. A guide approaching
the source's own length is a paraphrase, not a synthesis.

```markdown
---
description: One line, ≤160 chars — when to consult this guide.
status: CURRENT
source_kind: document         # document (user indications, operative) | code (comprehension map)
source: Human-readable name of what the user provided (or the component, for source_kind: code).
source_version: v1.2          # optional — only when the origin is versioned
distilled_from: ai_docs/reference/.sources/topic-a1b2c3d4.md
source_hash: <sha256 of the snapshot file>
overrides: GUIDE_topic.md   # optional — only for a project guide overriding an agent-KB guide
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

Section repertoire (pick what the source supports):
- **`document` (operative):** How to do X / How to verify / What NOT to do / What to
  watch out for / Core principles / When this applies.
- **`code` (comprehension):** How it works / Control & data flow / Key invariants /
  Extension points / Where it breaks (failure modes) / Why it is shaped this way.
  Every marker points into the code-excerpt snapshot: `[source: <slug>-<hash8>.md#path:symbol]`.

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
## Actors
<!-- the cast this product serves. One light line per actor:
     **Role** — primary goal; good UX = what a good experience means to them.
     Define each actor ONCE here; use-cases (Standalone) / D-UC (Hybrid) reference
     them by role and never re-describe who they are (anti-DRY). Actors characterize
     the intended UX; keep it proportional — a role list, not persona research. -->
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
## Actors
<!-- the cast this feature serves — usually a subset/refinement of the project
     Actors, or a distinct feature-local cast for internal-tooling work. One light
     line each: **Role** — primary goal; good UX = what good feels like.
     Referenced by the use-cases, not re-described in them. -->
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
     for this feature; success signals; the Actors this feature serves (name them,
     or point to the project Vision's ## Actors — do not re-describe them here).
     This is the single home of the feature vision: the separate file
     VISION_[feature].md is created only if the feature spans multiple
     ANALYSIS documents or multiple milestones. -->

## Use Cases / User Needs
<!-- who needs this and why: the concrete use-cases / user-needs the change serves
     (the Standalone home for what Hybrid keeps in D-UC). Each use-case NAMES the
     Actor it serves (defined in the Vision's ## Actors) — actor = who they are,
     use-case = what they do. Derived from the elicitation round; the Impact below
     must cover each, and the closure review checks coverage + actor UX fit. -->

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

## ai_docs/solutions/PLAN_[feature].md

Opt-in, L3 only (see `dispatch.md`): the executable task list an orchestrator
drives through subagents. It is `derived-from` the accepted E-TDD (Hybrid) or
the ANALYSIS Action Plan (Standalone) — never independently authored. The
validator gate is `sdlc_check.py plan validate PLAN_[feature].md` ("no valid
plan, no dispatch").

````markdown
---
status: DRAFT
derived-from: e_tdd_[feature] vX.Y
---
# Plan: [Feature]

```json
{
  "tasks": [
    {
      "id": "T1",
      "title": "Add the confine_under helper",
      "paths": ["skills/agentic-sdlc-skill/scripts/sdlc_check.py"],
      "consumes": [],
      "produces": ["skills/agentic-sdlc-skill/scripts/sdlc_check.py#confine_under"],
      "verify": "python skills/agentic-sdlc-skill/scripts/test_plan.py",
      "guides": ["GUIDE_python_style.md"]
    }
  ]
}
```
````

Task fields: `id`/`title`/`verify` are required; at least one of `paths`/
`produces` is required. `paths` are files the task touches; `consumes`/
`produces` declare interfaces between tasks (what an earlier task hands to a
later one); `guides` are pointers (paths, not pasted content) into
`ai_docs/reference/` or the agent-global KB. All path-shaped fields are
confined fail-closed under the project root (or the reference/KB root for
`guides`) — an absolute path or a `..` escape is rejected. `verify` is opaque
text: the validator only prints it (`plan brief`), never runs it — the
orchestrator executes it out of band.

Sidecar ledger `ai_docs/solutions/PLAN_[feature].ledger.json` (orchestrator-
owned, validator-read-only): `{ "<task_id>": {"status": "done", "verify_result":
"pass", "timestamp": "2026-07-03T00:00:00Z"} }`. Only the exact `status: done`
sentinel skips re-dispatch; any other value (or a missing `status`) is treated
as pending. A ledger id absent from the plan is a non-fatal orphan warning.

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

Written at every L3 closure AND at session end with work still IN_PROGRESS (see SKILL.md, Write Triggers).

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
