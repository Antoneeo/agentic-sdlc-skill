# Document templates — KB Agentic

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
---
default_domain: knowledge
---
# ai_docs — reading guide

Must-reads for this project, in order. The full manifest of canonical docs is
`INDEX.md` (generated — regenerate with `sdlc_check.py index`, never edit by hand).

1. `reference/INDEX.md` — the guide router: which guide already governs the work you are about to do (generated).
2. `vision/project_vision.md` — why the project exists (check its Status first).
3. `strategic/architecture.md` — how it is built.
4. `audit/handoff.md` — where work stopped last session (if present).

Directory purposes: `vision/` (project direction), `strategic/` (architecture and
feature catalog), `reference/` (operative guides), `solutions/` (per-feature
analyses, discovery-by-grep), `audit/` (audit plan and handoff).
```

## ai_docs/vision/project_vision.md

A Vision states **the benefit to be obtained while leaving the most degrees of
freedom possible** — it binds nothing that does not obstruct that benefit (the
deletion test, `vision.md` §What-a-Vision-IS). It is *applied* as a **gate**: a
cold reader must be able to rule ACCEPT or REJECT on a proposed change, quoting
one line, without asking anyone anything. Write it against `vision.md` §1–§4 from
the first draft — the properties that make a rule survive a motivated reader are
cheap to apply while writing and expensive to retrofit. `vision.md` §6 is the
blind check that gates promotion to APPROVED.

Sections below marked **[gate]** are load-bearing for that ruling; the others are
orientation for humans. Keep the human ones — just know which is which.

```markdown
# Project Vision
Status: DRAFT
<!-- Status: DRAFT (reconstructed by the agent, NOT a gating authority)
     or APPROVED (by <who>, <date>) — only after the user's explicit confirmation
     AND the blind check in vision.md §6. -->

## North Star
<!-- [gate, partly] The BENEFIT to be obtained — what the actor gets, never the
     mechanism, and never by comparison to another product (a comparative
     definition rots silently when the comparison target moves). Concrete enough
     that an obstacle to it is recognizable: that is what makes every Non-Goal
     below derivable and refutable. Also restate here any boundary a ruling
     depends on but that is defined elsewhere: risk tiers, lifecycle states,
     scale levels. Routing the reader to another file breaks the cold-read
     premise. -->
## Core Problem
<!-- Human orientation: what goes wrong without this product. Carries no gate
     weight unless the admission test names it. -->
## Actors
<!-- [gate] the cast this product serves. One light line per actor:
     **Role** — primary goal; good UX = what a good experience means to them.
     The "good UX =" clauses are admissible work, not decoration — say so in the
     admission test. Define each actor ONCE here; use-cases (Standalone) / D-UC
     (Hybrid) reference them by role and never re-describe them (anti-DRY).
     Proportional: a role list, not persona research. -->
## Goals
<!-- [gate — the ACCEPT side] Each with a baseline and headroom, so "advances this"
     has meaning. A goal phrased as an already-true state cannot be advanced.
     Include the recurring legitimate work explicitly (packaging and installation,
     the product's own tests, reducing what the agent must read, one more client) —
     otherwise your own test rejects the maintenance the product needs. -->
## Invariants
<!-- [gate] The promises that outrank everything: what the user is guaranteed, what
     the architecture must always be true of. State each as ONE decision question
     with BOTH branches answered, plus an anti-laundering clause naming the
     re-descriptions you expect. Omit the section if the product has none. -->
## Non-Goals
<!-- [gate — the REJECT side; this is your ENTIRE rejection surface]
     Derive every rule by the deletion test: remove it — if the benefit is still
     reachable, the rule does not belong (it spends a degree of freedom on
     nothing); if not, keep it and name the obstacle it removes. Constraints
     accumulate as work reveals obstacles — an almost-empty first draft is
     correct, not incomplete.
     Open with a supremacy clause: what these bind (all layers, tiers, paid
     components, future components), and that packaging or naming is irrelevant.
     Each rule: an observable property of the artifact (never intent or a promise),
     a closed enumeration with a closure rule, the near-miss verbs, an IN and an OUT
     example on the same axis, and its exception attached in the same bullet.
     Nothing here that cannot be violated by a proposed change — a rule about this
     document's own prose can never fire, and wastes a slot. -->
## The admission test
<!-- [gate] One sentence naming EXACTLY which sections are positive sources and
     EXACTLY which are prohibitions. State what the test does NOT govern (defect
     fixes, performance, maintenance) and give that exemption its own anti-abuse
     clause. State the default for anything unreached, per path. -->
## Success Signals
<!-- [gate] Each checkable against a NAMED artifact or command by someone who was
     not here. Not "we are the best" — a file, a command, a battery, and what the
     result must be. -->
## Where the rest lives
<!-- Pointers, so an absence reads as intentional rather than as a gap. Competitive
     positioning goes here as a dated snapshot, never in the Vision body. -->
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

## Capability Ledger
<!-- the architect pass (`architect.md`), run BEFORE the Impact below. One row per
     capability the feature requires the system to be able to DO — a verb over a
     domain noun, naming no file. Verdict EXISTS (name the component and where) /
     INADEQUATE (same, plus the gap) / MISSING (say what you searched). Every
     INADEQUATE or MISSING row becomes a component with its own contract, stated
     without naming this feature, and lands in the Impact below. Evidence is what
     makes a verdict falsifiable: for EXISTS/INADEQUATE the one guarantee you
     re-read to confirm it; for MISSING the terms, the tool and the areas searched
     (and say "provisional" when the area is still PENDING in the audit plan).
     A question, not a form: when every capability plainly exists, one line under
     this heading answers it — still naming the component and where it lives. -->

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| persist an order | EXISTS | `path/to/store.py#OrderStore` | re-read `save()`: durable, returns the id |
| notify the customer | MISSING | — | grep notify/alert/dispatch + send, over src/ and legacy/; no owner |

## Impact
<!-- existing files touched, APIs/contracts, performance, new dependencies.
     Derived from the ledger above: every INADEQUATE/MISSING row appears here. -->

## Sources and Verification
<!-- ALWAYS mandatory, also in Standalone. This is the knowledge domain's account of
     what could go wrong, and it is the risk slot the validator requires here — the
     code domain's `## Security and Threat Model` belongs to a different lens and is
     not what this one owes.
     One row per source the unit rests on: path (or URL) + locator, its provenance
     (GIVEN handed over / ELICITED said by the user / DERIVED synthesised / RULING a
     user decision), and HOW it was verified — cross-checked against another source,
     confirmed by the user, or left CONTESTED.
     A distillation whose origin cannot be reopened is model knowledge, not knowledge
     work. If something could not be confirmed, say so explicitly: that is a state the
     document may be in; silence is not. -->

| Source | Locator | Provenance | Verification |
|---|---|---|---|
| corpus/given/contract-9a1f2b7c.pdf | p.17 | GIVEN | cross-checked against the signed schedule |

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

## ai_docs/audit/handoff.md — the workstream registry

One row per OPEN workstream, ≤ 20 lines. **Parallel-safe by construction**: closing
one milestone removes one row and never touches another's resume point — the defect
this replaces was a single narrative slot where the last session to close overwrote
everyone else's handoff. It is an **inventory for lookup** (like the generated
manifest), not a work board: no assignment, no due dates, no execution ordering.

Updated at every L3 closure (row removed) AND at session end with work still
IN_PROGRESS (row refreshed) — see Write Triggers.

**Coming from a pre-1.17 project** (narrative handoff with `## Active features` /
`## Next step` / `## Session notes`): nothing is broken and nothing is urgent — the
validator only checks the `Date:` header and its age, and the orientation hook reads
the file verbatim. Read it as a one-row registry, and convert it the next time the
write trigger fires: each `## Active features` bullet becomes a row, `## Next step`
becomes that row's next step, `## Session notes` becomes `## Project-wide notes`.
Migrating a repository that is not being worked on buys nothing.

```markdown
# Handoff — workstream registry
Date: 2026-06-11 (UTC)

| Workstream | Level | Branch | Status | Since | Next step | Details |
|---|---|---|---|---|---|---|
| F-001 SSO login | L3 | feature/sso-login | PROGRESS | 2026-06-10 | wire callback tests | HANDOFF_login_sso.md · ANALYSIS_login_sso.md |
| F-002 Audit refresh | L3 | feature/audit | PAUSED | 2026-06-02 | resume at Phase 4 | ANALYSIS_audit_refresh.md (no volatile state) |

## Project-wide notes
<!-- one or two lines: release pending, environment quirks that affect everyone -->
```

## ai_docs/audit/reviews/REVIEW_LOG.md

One row per completed review (`review.md` §When a review is due). Append-only; it
is the record that the gate ran and what it was worth. **One schema for both
modes** — a Hybrid project's devPNT gates write to this same file, so Standalone
adds values to the existing columns rather than a second table.

```markdown
# Independent Review Log

| date | doc_key | tier | reviewer | findings_raised | findings_real | verdict | revise_rounds |
|---|---|---|---|---|---|---|---|
| 2026-06-11 | ANALYSIS_login_sso.md | design | subagent (opus, fresh ctx) | 4 | 3 | PASS | 2 |
| 2026-06-12 | diff feature/sso-login | closure | self-pass (declared; no subagent facility) | 2 | 2 | PASS | 1 |

## Notes
<!-- One short paragraph per review that found something worth remembering: what
     the findings actually were, and what changed because of them. The table
     answers "was it reviewed and by what"; this answers "what did it find" —
     which is where `review.md`'s per-finding outcomes live. Omit for a clean
     review; a row with 0 findings needs no note. -->
```

`tier` is the moment plus, in Hybrid, the reviewer weight: `design`, `design (late)`
and `closure` (Standalone); `deep`, `light`, `code`, `guide`, `vision` (devPNT gates
and the Vision blind check). The validator reads this column by its header name, so
extra or reordered columns are fine — but the header must say `tier`. `reviewer`
records the realization actually used — fresh subagent, one-shot client run, or a
**declared** self-pass. Writing `self-pass` where independence was unavailable is
honest; writing nothing, or implying independence you did not have, is the failure
this column exists to prevent. `findings_real` is how many raised findings survived
triage: over time it is the only evidence of whether the gate earns its cost.

## ai_docs/audit/HANDOFF_[topic].md — volatile resume logistics (ephemeral)

**Resume logistics ONLY; the ANALYSIS Diary keeps the durable narrative (DRY).**
The boundary: Diary = what happened and why (decisions, state of the work — survives
forever); this file = how to pick the work back up (branch/worktree, uncommitted
state, environment notes, the next concrete command — worthless once resumed).
Created only when a session pauses the feature WITH volatile state to record;
**DELETED at the feature's closure**, in the same step that flips the ANALYSIS to
COMPLETED — anything in it worth keeping was in the wrong file.

```markdown
# HANDOFF: [topic] (ephemeral — deleted at closure)
Updated: 2026-06-11 (UTC)
Branch: feature/sso-login (worktree ../wt-sso)

## Resume state
<!-- uncommitted files, half-run migrations, env vars, running services -->

## Next command
<!-- the literal next thing to run or edit -->

## Watch out
<!-- traps discovered this session that bite on resume (locks, CRLF, flaky test) -->
```

## ai_docs/strategic/architecture.md and existing_features.md

Canonical docs: they open with the header (`description:`/`status:`) so they enter the `INDEX.md` manifest cleanly.

```markdown
---
description: Stack, directory structure, component map and architectural patterns of the project.
status: CURRENT
---
# Project Architecture
## Technology Stack
## Directory Structure
## Component Map
<!-- The inventory the architect pass reads BEFORE searching the code
     (`architect.md` §2). One row per component that OWNS a capability:
     Capability = what it lets the system DO (a verb over a domain noun, naming
     no file). Contract = what it guarantees its consumers, in one line, stated
     without naming any single consumer. Where = a path, or `path#symbol` when
     the component is smaller than its file.
     Seeded at bootstrap; a row is added or corrected in the SAME closure that
     builds — or merely discovers — a component, and the area is marked ANALYZED.
     A directory is not a component: rows name what owns a capability, not where
     files sit (that is ## Directory Structure above). An absent or stale map is
     why the next feature rules the same capability MISSING a second time and
     builds it again. -->

Coverage: whatever `audit/audit_plan.md` marks ANALYZED — **read it, do not trust a
list restated here** (a hand-copied list is a cache with no invalidation). Outside
those areas this map is **unread, not empty**: it can never ground a MISSING
verdict, and the code is searched instead (`architect.md` §2).

| Component | Capability it owns | Contract | Where |
|---|---|---|---|
| ... | ... | ... | ... |

<!-- Where is `path/to/file.py#Symbol`. Leave the placeholder row untouched until
     the map has a real component: the validator skips an all-`...` row, so a
     freshly seeded project is never nagged about a table nobody has filled in. -->

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
