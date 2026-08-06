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
domain: code                 # optional — code | knowledge | marketing; omit in a single-domain project
---
# Document Title
```

When a doc replaces another: the new one declares `supersedes:`, the old one switches to `status: SUPERSEDED` (it stays as history, do not delete it). `sdlc_check.py validate` warns if `status` is missing or if a superseded doc is still `CURRENT`.

**`domain:` — write it only when it says something.** It names the domain whose fidelity discipline the document was written under, and it *records* an answer the work already has; it never decides one. Omit it and the project default applies (`default_domain:` in `ai_docs/README.md`, absent → `code`), so a single-domain project never writes the field at all. Documents under `vision/` sit above the split and take no `domain:`. In a mixed project, a wrong or forgotten field surfaces as a validation error on the missing mandatory risk section — never as a silent pass.

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
default_domain: code
---
# ai_docs — reading guide

Must-reads for this project, in order. The full manifest of canonical docs is
`INDEX.md` (generated — regenerate with `sdlc_check.py index`, never edit by hand).

1. `reference/INDEX.md` — the guide router: which guide already governs the work you are about to do (generated).
2. `vision/project_vision.md` — why the project exists (check its Status first).
3. `strategic/architecture.md` — how it is built.
4. `audit/handoff.md` — where work stopped last session (generated from the `HANDOFF_*.md` beside it; never edited by hand).

Directory purposes: `vision/` (project direction), `strategic/` (architecture and
feature catalog), `reference/` (operative guides), `solutions/` (per-feature
analyses, discovery-by-grep), `audit/` (audit plan and handoff).
```

`default_domain:` is the project's answer for every document that does not declare its own `domain:`. Whichever lens's `init` created the project seeds it; a later init never overwrites it, and an absent line resolves to `code` — so every project created before this field existed keeps behaving exactly as it did. It is written once, at project level, precisely so that the same tree gets **the same verdict from every installed lens**.

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

`domain:` and `checks:` are optional and only earn their place in a project where more than one lens is installed (see the canonical-header note above for how an omitted `domain:` resolves). `checks:` names **portable checks** imported from another domain — e.g. `domain: knowledge` with `checks: [marketing.funnel]`. An imported check can only ADD findings, never relax what the owning domain requires, so importing one is always safe; naming a check this installation does not carry produces a visible warning, never a silent pass. `id:` is unique **within a domain**, and its prefix says which: `F-` code, `K-` knowledge, `M-` marketing. Projects that predate the prefixes keep their `F-` ids — uniqueness was already scoped to the one domain they have.

```markdown
---
id: F-001
feature: Feature Name
status: PLANNED
level: L3
start_date: 2026-06-11
end_date:
domain: code                    # optional — code | knowledge | marketing
checks: [marketing.funnel]      # optional — extra portable checks to run on this document
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
     must cover each, and the closure review checks coverage + actor UX fit.
     GROUNDING GATE (two checks, nothing else — this comment is the OWNING
     definition of the gate; review.md and SKILL.md cite it, never restate it):
     1. Every product name the use-cases use resolves to exactly ONE bucket:
        EXISTS — real in the product, called by the term the product itself uses
        (a renamed existing thing is a phantom, not a citation); NEW — introduced
        by this change and explicitly declared new; METAPHOR — illustrative only,
        never named as an interface element an actor acts on. A name in no bucket
        invents system reality that is not there.
     2. Every use-case traces to a benefit named in the Vision (Standalone) /
        M-VISION (Hybrid). A use-case serving no stated benefit is drift, not a need.
     Both read the use-case TEXT — the author self-applies at drafting, then an
     independent design review (review.md, moment 1) verifies them BEFORE, and
     without replacing, the owner's own review. They keep the top of the funnel
     from proposing what the vision does not want or the project does not have;
     drafting is grounded in BOTH anchors first — the Vision (benefit + actors)
     and the real system (summaries / existing features / source). -->

## Functional Spec
<!-- [conditional] Fires when the change ADDS or ALTERS observable behavior —
     what the system does, decides or shows. Not fired (pure internal refactor,
     no behavior change) → one line stating why. This comment is the OWNING
     definition of the section; SKILL.md and review.md cite it, never restate it.
     THE validation object: the complete observable WHAT, readable by a person
     ("is this what we want?") and by the AI (the contract the design and the
     closure review conform to). Component-free by construction: it names NO
     components, files or mechanisms — behavior only, in the actor's and the
     domain's vocabulary. (Product names obey the Use Cases grounding buckets:
     EXISTS with the product's own term / NEW declared / METAPHOR never an
     interface element.)
     Content, per use case whose behavior the change touches (a question, not a form):
     1. Behavior — the rules and decisions, stated as observable outcomes
        ("a request with an expired token is rejected and the actor is told the
        session expired; no partial state persists").
     2. Cases — normal, edge, error and state-dependent behavior: empty, invalid,
        concurrent, limits, repeated. Each case states what the actor observes.
     3. Acceptance criteria — the "done when": checkable statements
        (given/when/then form welcome), each covered by ## Test Strategy.
     Authority split: Use Cases own WHY (the need), this section owns WHAT
     (behavior semantics), the Interface Contract owns THROUGH-WHAT (surfaces,
     flows, feedback), the Impact owns HOW. A component or mechanism named here
     is Solution-leakage — move it to the Interface Contract (component names)
     or the Impact (mechanism). -->

## Interface Contract
<!-- [conditional] Fires when the change creates or modifies a surface through
     which an actor **acts on or perceives** the system — GUI view, CLI
     command/flags, API endpoint, user-edited config, notification or
     user-facing message. The verb pair is the test; the list is illustrative.
     IN: an error dialog's wording and states (the actor perceives it and
     decides on it). OUT: an internal log format, a private module API
     (operated by code, not by an actor). Not fired → one line stating why.
     This comment is the OWNING definition of the trigger; SKILL.md and
     review.md cite it, never restate it.
     Content, per use case whose surface the change touches (a question, not a form):
     1. Actors + surfaces — who acts (human OR software, contracted the same way)
        through which surface, AND the interaction idioms already in use for this
        job (how the product already does selection, confirmation, errors,
        navigation).
     2. The information & processing flow — THE HEART. Walk it: the actor acts
        here → the flow it triggers, NAMING the components it traverses as
        responsibility-holders ("the auth component validates and responds") →
        what returns. Responsibility level only — never the mechanism inside a
        component. This walk is the proof of walkability: it surfaces realization
        problems before a line of code exists.
     3. Required affordances — what the actor needs in order to act.
     4. Required feedback — UNIVERSAL: what must come back, including error and
        intermediate states, and the return status a software actor receives
        (feedback is not human-only). Left implicit, the interface breaks.
     5. Architectural constraints touched — the existing components/flows the
        surface must coexist with, named as constraints (read, not redesigned).
     6. Surfaced feasibility flags / risks — problems the walk revealed; these
        feed the threat model (## Security) and the Impact.
     Reuse the as-is idioms by default; a NEW idiom where an existing one covers
     the job is a declared decision with its reason — never an unmarked invention.
     Authority split: behavior semantics (rules, cases, outcomes) are
     ## Functional Spec's — this contract binds the observable interaction AND
     the responsibility-level flow that deliver them; it NAMES the components in
     the flow, never their mechanism or file-level design (that is the Impact's
     vocabulary). After
     design approval, changing a contracted surface, flow or feedback is a scope
     change the USER approves: the solution may propose it, never enact it
     silently. Every contracted flow is covered by ## Test Strategy. -->

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

## ai_docs/audit/handoff.md — the workstream registry (GENERATED)

One row per OPEN workstream. **Never written by hand**: `sdlc_check.py index` builds
it from the `HANDOFF_[feature].md` files, and `validate` errors when the two disagree.
It is an **inventory for lookup** (like the generated manifest), not a work board: no
assignment, no due dates, no execution ordering, no holder.

**Why generated, and not just one row per workstream.** Row-per-workstream alone was
tried and was not enough: two workstreams opened from one base still conflicted twice
in this file, because a file-global `Date:` header defeats row-level ownership no
matter how few rows each writer touches. So the truth moved into the per-workstream
file, and the header is derived (the newest `updated:` in the sources — a value, never
a filesystem timestamp, which git does not preserve). Two writers on two workstreams
now touch two different files. The generated view can still conflict at merge; that
conflict is resolved **mechanically** by re-running `index`, never by hand, and
`validate` refuses CLEAN until the file matches its sources.

Project-wide notes have their own source, `ai_docs/audit/project_notes.md`, appended
verbatim under `## Project-wide notes`. (Not `handoff_notes.md`: the `HANDOFF_*.md`
glob is case-insensitive on Windows and would collect it as a workstream.)

**Converting an existing project** — lazily, at the first write, and **all at once**.
Converting one row at a time is the state that loses the others: the next `index`
would regenerate from the one source and drop the rest. `index` refuses to write while
anything in the file is unaccounted for, and names it. A pre-1.17 narrative handoff
(`## Active features` / `## Next step` / `## Session notes`) is the same conversion:
each bullet becomes a `HANDOFF_[feature].md`, `## Session notes` becomes
`project_notes.md`. A project with no sources yet is not touched and reports nothing —
migrating a repository nobody is working on buys nothing.

```markdown
# Handoff — workstream registry
Date: 2026-06-11 (UTC)

<!-- GENERATED by sdlc_check.py index - do not edit by hand. Source of truth: the HANDOFF_*.md files in ai_docs/audit/. -->

| Workstream | Level | Branch | Status | Since | Next step | Details |
|---|---|---|---|---|---|---|
| F-001 SSO login | L3 | feature/sso-login | PROGRESS | 2026-06-10 | wire callback tests | HANDOFF_login_sso.md · ANALYSIS_login_sso.md |
| F-002 Audit refresh | L3 | feature/audit | PAUSED | 2026-06-02 | resume at Phase 4 | HANDOFF_audit_refresh.md · ANALYSIS_audit_refresh.md |

## Project-wide notes

<!-- from audit/project_notes.md: release pending, environment quirks that affect everyone -->
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
Concurrent reviews: `init` writes a `.gitattributes` stanza giving this file
`merge=union` — a **built-in** driver (no per-clone `git config`, unlike
`merge=ours`, which silently does nothing until every clone configures it).
Rows are date-stamped and their order carries no meaning, so a union merge keeps
both sides instead of asking a human to choose. It is defence in depth: without
git, or without the stanza, the outcome is today's — one conflict you resolve by
hand, never a lost row.


## ai_docs/audit/HANDOFF_[feature].md — one open workstream, its own file

**The authored home of that workstream's registry row**, and the only one: the
registry is generated from these files. **One exists for every OPEN workstream**, with
or without volatile state — a workstream whose file is missing has no row, and a
workstream with no row is invisible to the next cold agent. **DELETED at the feature's
closure**, in the same step that flips the ANALYSIS to COMPLETED: deleting it *is*
removing the row.

**The DRY boundary, restated because the file is no longer rare.** What used to keep
narrative out of it was that it barely existed; now it always does. So: the ANALYSIS
Diary keeps **what happened and why** (decisions, state of the work — survives
forever), and this file keeps **the row plus the resume logistics** — how to pick the work back up (branch,
worktree, uncommitted state, the next concrete command — worthless once resumed).
Prose that would still be worth reading after closure is in the wrong file, because
this one is deleted.

The frontmatter IS the row. `workstream:` is what marks the file as a source: without
it the file is still a perfectly good volatile note, and nothing generates.

```markdown
---
workstream: F-001 SSO login
level: L3
branch: feature/sso-login (worktree ../wt-sso)
status: PROGRESS
since: 2026-06-10
next: wire the callback tests
details: ANALYSIS_login_sso.md
updated: 2026-06-11
---
# HANDOFF: [feature] (ephemeral — deleted at closure)

## Resume state
<!-- uncommitted files, half-run migrations, env vars, running services -->

## Next command
<!-- the literal next thing to run or edit -->

## Watch out
<!-- traps discovered this session that bite on resume (locks, CRLF, flaky test) -->
```

`updated:` is the date this file last changed, and the newest one across all sources
becomes the registry's `Date:` header — which is why no writer ever edits that header
and why two concurrent writers no longer collide on it. `details:` holds the *other*
pointers (the ANALYSIS, a review log entry); the generator prepends this file's own
name, so nothing points at itself by hand.

## ai_docs/audit/project_notes.md — the registry's project-wide notes (source)

Plain lines, no frontmatter, appended verbatim to the generated registry under
`## Project-wide notes`. Release pending, environment quirks, anything true for
everyone rather than for one workstream. It exists so that generating the registry
cannot destroy notes that belong to no workstream.

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
