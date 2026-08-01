---
name: kb-agentic
description: Knowledge-Base & Document-First protocol with risk-proportional triage, Vision as a guide, Signal Distillation, a complete Standalone mode and optional symbiosis with devPNT. Use for user documentation, knowledge extraction, SOPs, research notes, decision logs and knowledge management.
author: Antonio Pinto (https://github.com/Antoneeo)
copyright: (c) 2026 Antonio Pinto
---

# KB Agentic

**Why this skill exists:** to prevent *knowledge degradation and myopia* — acting from partial understanding, where new information contradicts un-indexed notes and hard-won knowledge evaporates between sessions. Triage, the Vision Gate, signal distillation, the documentation lifecycle, and operative guide routers are all one defense against that.

This skill guides knowledge management and documentation with a Document-First process proportional to risk. It works fully even without devPNT. When devPNT is available and configured for the current project, the skill works in symbiosis with its governance: M-VISION, Master Plan, Action Plan and versioned artifacts become the authoritative frame for milestones and knowledge nodes.

Support files in the skill directory:
- `templates.md`: templates for Vision, Knowledge ANALYSIS, Research SPIKE, SOP GUIDE, audit plan, and handoff.
- `taxonomy.md`: the taxonomy pass — do the categories, topics, and SOPs for this subject already exist? Run at L3 before drafting.
- `guides.md`: pipeline for distilling user-provided indications into `ai_docs/reference/GUIDE_[topic].md`.
- `vision.md`: how to write a Vision a cold reviewer can actually apply — the properties that make a rule hold, the minimum operable sections, and the blind check.
- `distillation.md`: contract-first signal distillation discipline (symbiosis with `distill`).
- `reconciliation.md`: systematic procedure for resolving conflicting notes, handling obsolete information, and marking deprecated docs.
- `review.md`: the review discipline — when a review is due, how to request one, how to receive findings, how to review.
- `dispatch.md`: opt-in subagent execution of an approved plan.
- `routing.md`: which lens owns this unit of work. Read ONLY when a sibling lens skill is installed alongside this one; a single-lens install never reads it.
- `scripts/sdlc_check.py` + `scripts/sdlc_core.py`: the mechanical validator for the docs root (`check`, `validate`, `index`, `stale`, `mark`, `gate`, `plan`, `orient`). Two files: the core is the family's shared spine, the entry point names this domain. Copy both, or neither.
- `ENFORCEMENT.md`: optional setup for CI and hooks.

Read these files only when needed. `SKILL.md` is the operating contract; the support files are progressive resources.

## Knowledge Values

- **Understand before writing/updating:** do not modify or create knowledge documents without checking root cause, user constraints, and existing notes — trust the primary sources and existing guides, not memory.
- **Apply DRY and Single Source of Truth:** do not duplicate knowledge across files; extend existing notes (`ANALYSIS_[topic].md` or `GUIDE_[topic].md`).
- **Signal & Distillation:** eliminate fluff, filler, and speculative statements; keep deterministic facts, constraints, decisions, and clear SOP steps (symbiosis with `distill`).
- **Lifecycle & Freshness:** mark superseded knowledge (`status: SUPERSEDED` or `DEPRECATED`) so outdated information does not cause hallucination.
- **Protect the Vision & User Style:** align all knowledge work with user strategic goals, operational preferences, and expected outcomes.
- **Map-First Navigation:** rely on `ai_docs/README.md`, `INDEX.md`, and `reference/INDEX.md` router for targeted retrieval before creating new documents.

## Rule Zero: Triage

Always classify the request before choosing the process. Declare the chosen level to the user when you start operational work.

**Declare the level WITH the router verdict** (one line, for L2, L3 and Spike — L1 declares the level alone): the result of the guide-router lookup described under `## Operative Guides`, i.e. `Level: L2 · router: no match` or `Level: L3 · router: GUIDE_release_sop.md → read`. Name the guide you matched, or `no match`.

| Level | Criteria | Required process |
|---|---|---|
| **L1 - Quick Fact / Snippet** | Small update to an existing note, typo fix in docs, quick preference update (at most 1-2 files). | Implement edit directly in existing note. No new documents. |
| **L2 - Local Note / SOP Update** | Specific SOP update, local research note, or small document addition (at most 1-2 files). Low risk. | Mini-analysis in message: objective, impact, sources, validation. Update existing document or create single SOP/note. |
| **L3 - Major Knowledge Unit / Corpus** | Ingesting large document sets, complex multi-topic research, multi-part guide creation, or restructuring the KB. | Full workflow: Vision Gate, Spec Elicitation, Taxonomy Pass, Knowledge Analysis, Distillation, Review, Indexing. |
| **Spike - Exploration** | Time-boxed exploratory research or draft without merging into official KB. | Outcome in `ai_docs/solutions/SPIKE_[topic].md`. |

Cross-cutting rules:
- **Domain routing (multi-lens installs only).** After the level is set, and only when a sibling lens skill of this family is installed (`agentic-sdlc`, `mkt-agentic-sdlc`), run the router in `routing.md` for every L2, L3 and Spike: it decides which lens's method and validation rules govern this unit of work. L1 never reaches it, and a single-lens install never reads the file — detection fails open. In such a project, never refer to a document whose meaning differs by lens ("threat model", "vision", `principles.md`, `handoff.md`) by its bare name: qualify it with its domain, or name its path.
- Personal data, credentials, security-sensitive processes, authN/authZ specs are high-risk: never L1.
- If a bigger impact emerges during L1/L2 work, stop, reclassify and declare it.
- When in doubt, pick the higher level.

## Write Triggers

Triage decides IF documentation is due; this table decides WHICH document each event produces, and when. **One event, one destination:** when the trigger fires and the document does not exist, create it; when it exists, update it — never duplicate it.

| Document | Write trigger | Phase |
|---|---|---|
| `solutions/ANALYSIS_[topic].md` | Every L3, after elicitation and before any drafting. On topic match with an existing analysis, update that one instead of a new file. | 3 |
| `solutions/SPIKE_[topic].md` | Closing any Spike — including a negative outcome. | — |
| `vision/features/VISION_[feature].md` | Multi-milestone topic at analysis time, or retroactive trigger (second ANALYSIS on same theme). | 3 |
| `audit/handoff.md` (workstream registry) | One row per OPEN workstream (topic, level, status, since, next step) — refresh at every L3 closure and session end. ≤ 20 lines. | 5 / session end |
| `audit/HANDOFF_[topic].md` | Session ends with that topic unfinished AND there is volatile resume state. Ephemeral, deleted at closure. | 4 / 5 / session end |
| `audit/audit_plan.md` (Standalone) | Bootstrap, and whenever a mapped area changes state (`sdlc_check.py mark`). | 1 |
| `reference/GUIDE_[topic].md` (`source_kind: document`) | Origin+purpose test (`guides.md`), or a proactive proposal accepted by user. | 4 / 5 |
| `reference/GUIDE_[topic].md` (`source_kind: code`/`domain`) | Recognized high-complexity domain/concept with no CURRENT guide $\rightarrow$ duty to write autonomously. | 4 / 5 |
| `audit/reviews/REVIEW_LOG.md` | Every completed review — recorded in log. | 3 / 5 |
| ADR / Decision Log — `architecture/` or devPNT DB | A strategic decision was taken (pattern, policy, structural change): record before DONE. | 5 |
| `strategic/architecture.md`, `strategic/existing_features.md` | Bootstrap; update at closure when the knowledge catalog actually changed. | 1 / 5 |
| `vision/project_vision.md`, `roadmap.md`, `principles.md` | Bootstrap as `Status: DRAFT`; promoted to APPROVED only by explicit user confirmation. | 1 / 2 |
| `INDEX.md`, `reference/INDEX.md` | Regenerated by `sdlc_check.py index` at closure. | 5 |

## Operating Modes

### Full Standalone
Use this mode when devPNT is unavailable, not configured for the current project, or the user explicitly asks for a filesystem-only workflow.
- Source of truth: `ai_docs/` (`vision/`, `solutions/`, `reference/`, `audit/`, `strategic/`).

### Hybrid in symbiosis with devPNT
Use this mode when `devpnt_*` tools are available and point at the current project.
- devPNT governs `M-VISION`, Master Plan, Action Plan, and versioned artifacts.
- Local `ai_docs/` serves as readable context, Standalone fallback, local handoff, or shadow copy.

## L3 Workflow

### 1. Audit and Alignment
- Read `ai_docs/audit/handoff.md` (workstream registry) to see active topics.
- Read `ai_docs/README.md`, `ai_docs/INDEX.md` and `ai_docs/reference/INDEX.md` (the guide router) before exploring notes. The router is a mandatory read, not an optional one: it is the only orientation step that tells you a guide already governs the work you are about to do.
- If `ai_docs/` is missing, create the bootstrap set: `README.md`, `vision/` docs, `strategic/` docs, and `audit/audit_plan.md`, then run `sdlc_check.py index`.

### 2. Vision Gate
- Read `project_vision.md`, `roadmap.md`, `principles.md` (or devPNT `M-VISION`).
- Verify request aligns with expected benefits, user goals, and success signals.

### 3. Request Analysis & Taxonomy Pass
- Run spec elicitation round (`elicitation.md`) before drafting analysis.
- Run taxonomy pass (`taxonomy.md`): verify whether topics, categories, or SOPs already exist in `ai_docs/`. Avoid duplication.
- Create or update `ai_docs/solutions/ANALYSIS_[topic].md`.
- **Design review gate (end of Phase 3, before any drafting):** the analysis is reviewed by somebody other than its author — a subagent with fresh context, or a declared self-pass when none is available. Follow `review.md`; log the outcome in `audit/reviews/REVIEW_LOG.md`. A knowledge structure reviewed only by the person who chose it is not reviewed.

### 4. Knowledge Processing & Distillation
- **Isolate the work (Branch/worktree hygiene).** Distillation rewrites existing notes: do it on a branch or a worktree, never directly on the shared corpus, so a half-finished reconciliation is never what the next reader finds.
- Before drafting (L2/L3; L1 exempt), **consult the guide router** for a guide covering the task and read it first (the consult trigger, `guides.md` §0). A targeted description match, not a blanket read. Its result is the router verdict already declared with the triage level (Rule Zero).
- Execute knowledge extraction using **Signal Distillation** (`distillation.md`).
- **Opt-in subagent execution**: for an L3 with an approved analysis, the work MAY be executed via subagents per `dispatch.md`; default stays same-session.
- Handle conflicting or outdated information via **Reconciliation** (`reconciliation.md`). Mark obsolete files `status: SUPERSEDED`.

### 5. Closure & Indexing
- Run verification checks (`sdlc_check.py check --root <project_root>`).
- If the work was governed by user-provided indications and is reusable, **PROPOSE distilling a guide** (proactive trigger, `guides.md` §1) — a proposal for the user, never a silent write, never from model knowledge.
- Update `audit/handoff.md`.
- Regenerate manifests: `python <skill_dir>/scripts/sdlc_check.py index --root <project_root>`.
- Mark output clean and complete.

## Operative Guides & Router
Guides are consulted, created, and distilled per `guides.md`.
- **Consult (before acting)**: check `ai_docs/reference/INDEX.md` — the guide router — and declare the verdict with the triage level.
- **Propose proactively**: when the user hands over indications that will govern future work, propose distilling them into a guide. A proposal, never a silent write, and never from model knowledge — a guide's whole value is that every claim traces to what the user actually provided.
- Distill from user instructions into `ai_docs/reference/GUIDE_[topic].md`.

## Mechanical Enforcement
- `scripts/sdlc_check.py index`: updates `ai_docs/INDEX.md` and `ai_docs/reference/INDEX.md`.
- `scripts/sdlc_check.py validate`: validates YAML frontmatter (`status`, `description`).
- `scripts/sdlc_check.py check`: checks dirty closures and missing indexes.
