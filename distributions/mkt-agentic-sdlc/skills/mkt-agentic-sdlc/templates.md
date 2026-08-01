# Document templates — Marketing Agentic SDLC

General rules:
- Concise documents: ≤ ~80 lines each (handoff ≤ 20; final MARKETING_PLAN exempt). If a document grows beyond that, split it, do not inflate it.
- Template conformance is not the goal: if a section has no real content, state explicitly why it does not apply. Never filler text.
- Every number cites its ledger entry as `[EV-nn]`. Dates always absolute.
- Deliverable language: the target market's language (decided in Discovery). Structure and field names stay as templated so the validator can parse them.

## Canonical document header (vision/ strategy/ tactics/ deliverables/)

Every durable canonical document opens with this frontmatter: it feeds the generated manifest `mkt_docs/INDEX.md` and gives an agent the freshness signal before it trusts the content.

```markdown
---
description: One line — what the document is and when to read it.
status: CURRENT              # CURRENT | SUPERSEDED | DRAFT | DEPRECATED
supersedes: old_doc.md       # only if it replaces another canonical doc
---
# Document Title
```

When a doc replaces another: the new one declares `supersedes:`, the old one switches to `status: SUPERSEDED` (it stays as history, do not delete it). `mkt_check.py validate` warns if `status` is missing or if a superseded doc is still `CURRENT`.

## mkt_docs/README.md

Curated must-read index, by hand (it is NOT the generated manifest). Created at init, updated rarely.

```markdown
---
default_domain: marketing
---
# mkt_docs — reading guide

Must-reads for this marketing project, in order. The full manifest of
canonical docs is `INDEX.md` (generated — regenerate with `mkt_check.py
index`, never edit by hand).

1. `vision/MKT_VISION.md` — why this plan exists (check its Status first).
2. `research/evidence_ledger.md` — the single source for every number.
3. `strategy/STRATEGY.md` — the approved strategy (if present).
4. `audit/handoff.md` — where work stopped last session (if present).

Directory purposes: `vision/` (marketing vision and principles), `research/`
(evidence ledger and research outputs, discovery-by-grep), `strategy/`
(ICP/personas, threat map, objectives, strategy), `tactics/` (tactical plan,
90-day action, measurement, campaigns), `deliverables/` (assembled plan and
exports), `spikes/` (research spikes), `audit/` (handoff).
```

## mkt_docs/vision/MKT_VISION.md

```markdown
---
description: Marketing vision — expected benefit, market, non-goals, success signals.
status: DRAFT
---
# Marketing Vision
Status: DRAFT
<!-- Status: DRAFT (reconstructed by the agent, NOT a gating authority)
     or APPROVED (by <who>, <date>) — only after the user's explicit confirmation -->

## Business Goal
<!-- the business outcome marketing must serve, in one paragraph. Cite FACTs. -->

## Expected Benefit
<!-- what a successful plan changes for the business, stated measurably -->

## Market & Audience
<!-- target market, geography, deliverable language; who we serve (short — the
     detailed ICP lives in strategy/ICP_PERSONAS.md) -->

## Non-Goals
<!-- what this plan explicitly does NOT pursue (markets, segments, channels).
     The strategy review checks divergence against these. -->

## Success Signals
<!-- how the user recognizes the plan is working, in their words -->

## Constraints
<!-- budget range [EV-nn], team capacity [EV-nn], legal/brand limits -->
```

## mkt_docs/vision/principles.md

```markdown
---
description: Stable decision principles guiding marketing trade-offs.
status: DRAFT
---
# Marketing Decision Principles

<!-- bullet list, most critical first. Examples: "no channel we cannot staff",
     "brand voice X non-negotiable", "experiments capped at 10% of budget" -->
```

## mkt_docs/research/evidence_ledger.md

The single source for every number. `[EV-nn]` references across all documents resolve here. Classes: FACT (user input / primary data), BENCHMARK (external, Source URL + Date mandatory), ASSUMPTION (Range + Confidence mandatory, rationale in Claim).

```markdown
# Evidence Ledger

| ID | Claim | Class | Value / Range | Source | Date | Confidence |
|---|---|---|---|---|---|---|
| EV-01 | (example) monthly marketing budget | FACT | 5000 EUR/month | user, Wave 1 | 2026-01-01 | HIGH |
```

## mkt_docs/strategy/ICP_PERSONAS.md

```markdown
---
description: Ideal customer profile and evidence-based personas.
status: DRAFT
---
# ICP & Personas

## Ideal Customer Profile
| Criterion | Value | Anti-profile (who we do NOT serve) |
|---|---|---|

## Persona: [name]
<!-- max 2-3 personas. Every trait cites VoC evidence [EV-nn] or is labeled ASSUMPTION. -->
- **Job to be done:**
- **Buying trigger:**
- **Top objections:**
- **Watering holes:** <!-- where they actually are — feeds channel selection -->
- **Vocabulary:** <!-- verbatim words from VoC — feeds messaging -->

<!-- B2B variant: the unit is the ACCOUNT (firmographic ICP), and the
     "personas" are the ROLES in the buying committee (e.g. economic buyer,
     technical decider, gatekeeper/veto), not consumer JTBD segments. Replace
     Job/Trigger/Objections/Watering-holes per role; add who decides vs signs
     vs blocks. Firmographic ICP criteria (size, sector, geography, trigger)
     go in the ICP table above. -->

```

## mkt_docs/strategy/THREAT_MAP.md

```markdown
---
description: Competitive threats and plan risks with mitigations.
status: DRAFT
---
# Threat Map

## Competitive threats
| Threat | Evidence | Likelihood | Impact | Mitigation |
|---|---|---|---|---|

## Plan risks
<!-- budget concentration, single-channel dependence, seasonality, capacity,
     brand/reputation risks. Same table shape. -->
```

## mkt_docs/strategy/SITUATION_SWOT.md

Sintesi della fase Situation (dopo la ricerca, prima degli obiettivi). Ogni
cella cita il ledger: adjectives senza [EV-nn] vanno cancellati. PESTEL /
Five Forces solo quando il mercato lo merita (frameworks.md); se saltati,
dichiararlo con la ragione.

```markdown
---
description: Sintesi SWOT evidence-based della fase Situation.
status: CURRENT
---
# SWOT — [business] ([canale/scope])

<!-- PESTEL/Five Forces: usati o saltati-con-ragione (frameworks.md) -->

## Strengths
<!-- ogni bullet cita [EV-nn] -->
## Weaknesses
## Opportunities
## Threats
```

## mkt_docs/strategy/OBJECTIVES.md

Objectives are `### O1 — Title` headings — the validator reads the `O#` ids for trace checks. 3-5 objectives maximum.

```markdown
---
description: SMART marketing objectives for the plan cycle.
status: DRAFT
---
# Objectives
Status: DRAFT   <!-- APPROVED (by <who>, <date>) after the user gate -->

### O1 — [title]
- **Target:** [number] by [date] [EV-nn justifying plausibility]
- **Owner:**
- **Why this is achievable:** <!-- cite ledger entries -->

### O2 — [title]
...
```

## mkt_docs/strategy/STRATEGY.md

```markdown
---
description: Segmentation, targeting, positioning and messaging for the plan cycle.
status: DRAFT
---
# Strategy
Status: DRAFT   <!-- APPROVED (by <who>, <date>) after the user gate -->

## Segmentation
<!-- segments found in research, with evidence -->

## Targeting
<!-- the CHOICE and its rationale; segments explicitly rejected and why -->

## Positioning
- **Competitive alternatives:** <!-- incl. "do nothing" -->
- **Unique attributes:**
- **Value (evidence-backed):**
- **Best-fit segment:**
- **Market category:**

> For [segment] who [need], [name] is the [category] that [unique value],
> unlike [main alternative] which [limitation].

<!-- Swap test result: statement with top competitor's name substituted must be FALSE. State it. -->

## Messaging house
- **Roof (value proposition):**
- **Pillar 1:** ... — proof points: ...
- **Pillar 2:** ... — proof points: ...
```

## mkt_docs/tactics/TACTICAL_PLAN.md

Parsed mechanically: keep the `Total budget:` line and the three tables with these exact column headers. Budget numbers plain or with k/M suffix; the validator strips currency symbols.

```markdown
---
description: Channel plan, budget allocation and funnel model.
status: DRAFT
---
# Tactical Plan

Total budget: 15000

## Channel Plan
| Channel | Objective | KPI | Budget | Owner |
|---|---|---|---|---|
| (example) Google Ads | O1 | CPL <= 30 [EV-04] | 6000 | founder |

<!-- Enabler-row convention: an objective that is a PRECONDITION (measurement,
     tracking, tooling setup) is not a spend channel but still needs a serving
     tactic for the trace check. Give it a row with Budget 0 and Owner set;
     it is intentionally absent from Budget Allocation (which must sum). -->
<!-- Gate riders: when the client approves a plan/strategy at a gate WITH a
     condition, record the rider in the approved doc's header (Status line),
     not only in chat — the next session and the reviewer must see it. -->


## Budget Allocation
| Channel | Budget | Share |
|---|---|---|
| (example) Google Ads | 6000 | 40% |

<!-- allocations must sum to Total budget (±1%) — mkt_check.py budget -->

## Funnel Model
| Channel | Budget | CPC | Clicks | CVR % | Leads | Close % | Customers | CAC |
|---|---|---|---|---|---|---|---|---|
| (example) Google Ads | 6000 | 1.50 [EV-04] | 4000 | 3 [EV-05] | 120 | 20 [EV-02] | 24 | 250 |

<!-- each row must recompute: Clicks=Budget/CPC, Leads=Clicks*CVR%,
     Customers=Leads*Close%, CAC=Budget/Customers (±5%) — mkt_check.py funnel.
     Compare total Customers to the objective targets; declare any gap. -->
<!-- Sales-led / B2B: this table is shaped for immediate-purchase e-commerce.
     For a long-cycle B2B motion, read `Customers` as QUALIFIED DEMOS/LEADS and
     `CAC` as cost-per-qualified-demo (state the relabel), put ONLY paid click
     channels here, and represent referral/content/outbound + the multi-stage
     sales funnel (MQL→SQL→demo→POC→won) and closed-won lag in a separate
     "Pipeline build-up vs objective" section. See frameworks.md. -->

## Channel selection rationale
<!-- matrix scores or written rationale per chosen channel; rejected channels and why -->
```

## mkt_docs/tactics/ACTION_90D.md

```markdown
---
description: Sequenced 90-day action plan.
status: DRAFT
---
# 90-Day Action Plan

## Weeks 1-2 (day-level)
| Day | Action | Owner | Depends on |
|---|---|---|---|

## Weeks 3-12 (week-level)
| Week | Actions | Owner | Milestone |
|---|---|---|---|
```

## mkt_docs/tactics/MEASUREMENT_PLAN.md

The KPI table is parsed for trace: every objective id must appear.

```markdown
---
description: KPI tree, targets, review cadence and kill/scale criteria.
status: DRAFT
---
# Measurement Plan

## North star
<!-- the one metric, and why -->

## KPI table
| Objective | KPI | Target | Benchmark | Cadence |
|---|---|---|---|---|
| O1 | (example) CPL | <= 30 | [EV-04] | weekly |

## Kill / scale criteria
| Channel | Kill if | Scale if |
|---|---|---|
| (example) Google Ads | CAC > 400 after 3000 spent | CAC < 200 at 2x volume |

## Review cadence
<!-- weekly channel KPIs, monthly objectives, quarterly strategy -->
```

## mkt_docs/tactics/CAMPAIGN_[name].md (E2)

```markdown
---
description: Campaign plan for [name].
status: DRAFT
---
# Campaign: [name]

## Brief
<!-- objective (link to O# or approved strategy context), audience, offer, KPI -->

Total budget: 3000

## Budget Allocation
| Channel | Budget | Share |
|---|---|---|

## Funnel Model
| Channel | Budget | CPC | Clicks | CVR % | Leads | Close % | Customers | CAC |
|---|---|---|---|---|---|---|---|---|

## Timeline & owners
## Kill / scale criteria
```

## mkt_docs/deliverables/MARKETING_PLAN.md

Assembled from the APPROVED artifacts — assembly, not rewriting; on divergence the approved artifact wins. Exempt from the 80-line cap.

```markdown
---
description: The assembled marketing plan (SOSTAC) — the deliverable.
status: DRAFT
---
# Marketing Plan — [business], [cycle]

## Executive Summary
<!-- one page: goal, strategy in two sentences, budget, expected outcome, top 3 risks -->

## Assumptions
<!-- every material ASSUMPTION [EV-nn] with range and what changes if it is wrong -->

## 1. Situation
<!-- from research + situation analysis: market [EV], competitors, VoC, SWOT -->

## 2. Objectives
<!-- from OBJECTIVES.md -->

## 3. Strategy
<!-- from STRATEGY.md: STP, positioning, messaging -->

## 4. Tactics
<!-- from TACTICAL_PLAN.md: channels, budget, funnel -->

## 5. Action
<!-- from ACTION_90D.md -->

## 6. Control
<!-- from MEASUREMENT_PLAN.md: KPIs, cadence, kill/scale -->

## Appendix — Evidence Ledger
<!-- the ledger table, verbatim -->
```

## mkt_docs/deliverables/ONE_PAGER.md

```markdown
---
description: One-page strategy summary for stakeholders.
status: DRAFT
---
# [Business] — Marketing on a Page

**Goal:** ...  **Budget:** ... [EV-nn]  **Horizon:** ...
**Positioning:** <!-- the statement -->
**Objectives:** <!-- O1..On, one line each -->
**Core channels:** <!-- 2-3, with budget share -->
**We will know it works when:** <!-- top KPIs -->
**We stop/scale when:** <!-- headline kill/scale criteria -->
```

## mkt_docs/spikes/RESEARCH_[topic].md

```markdown
# Research Spike: [topic]

## Question to answer
## Time-box
## Method & sources
## Answer / Outcome
<!-- ledger rows created: EV-nn..EV-mm -->
## Consequences
<!-- max 1 page. For strategy decisions, feed into E2/E3. -->
```

## mkt_docs/audit/handoff.md

Just a pointer, ≤ 20 lines.

```markdown
# Handoff
Date: 2026-01-01 (UTC)
Engagement: E3 — [name]
Agent: Claude

## Phase state
- Phase reached: <!-- e.g. 6 Strategy, awaiting user gate -->

## Next step
<!-- one line -->

## Session notes
<!-- gates passed? open review findings? ledger rows pending sources? -->
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

## ai_docs/audit/HANDOFF_[engagement].md — volatile resume logistics (ephemeral)

**Resume logistics ONLY; the ANALYSIS Diary keeps the durable narrative (DRY).**
The boundary: Diary = what happened and why (decisions, state of the work — survives
forever); this file = how to pick the work back up (branch/worktree, uncommitted
state, environment notes, the next concrete command — worthless once resumed).
Created only when a session pauses the feature WITH volatile state to record;
**DELETED at the feature's closure**, in the same step that flips the ANALYSIS to
COMPLETED — anything in it worth keeping was in the wrong file.

```markdown
# HANDOFF: [engagement] (ephemeral — deleted at closure)
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

## ai_docs/README.md

Curated must-read index, by hand (it is NOT the generated manifest). Created at init, updated rarely, only for real must-reads.

```markdown
---
default_domain: marketing
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

`default_domain:` is the project's answer for every document that does not declare its own `domain:`. Whichever lens's `init` created the project seeds it; a later init never overwrites it, and an absent line resolves to `code` — so every project created before this field existed keeps behaving exactly as it did. It is written once, at project level, precisely so that the same tree gets **the same verdict from every installed lens**.

