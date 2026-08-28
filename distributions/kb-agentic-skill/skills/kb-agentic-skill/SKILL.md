---
name: kb-agentic
version: 1.9.0
description: Knowledge-Base & Document-First protocol with risk-proportional triage, Vision as a guide, Signal Distillation, a complete Standalone mode and optional symbiosis with devPNT. Use for user documentation, knowledge extraction, SOPs, research notes, decision logs, knowledge management — and for answering project questions from the claim ledger and topic graph.
author: Antonio Pinto (https://github.com/Antoneeo)
copyright: (c) 2026 Antonio Pinto
---

# KB Agentic

**Why this skill exists:** to prevent *knowledge degradation and myopia* — acting from partial understanding, where new information contradicts un-indexed notes and hard-won knowledge evaporates between sessions. Triage, the Vision Gate, signal distillation, the documentation lifecycle, and operative guide routers are all one defense against that.

This skill guides knowledge management and documentation with a Document-First process proportional to risk. It works fully even without devPNT. When devPNT is available and configured for the current project, the skill works in symbiosis with its governance: M-VISION, Master Plan, Action Plan and versioned artifacts become the authoritative frame for milestones and knowledge nodes.

Support files in the skill directory:
- `templates.md`: templates for Vision, Knowledge ANALYSIS, Research SPIKE, SOP GUIDE, audit plan, and handoff.
- `portability.md`: carrying knowledge between projects — what a bundle is, why export is a closure rather than a selection, and the rule that knowledge crosses a project boundary while authority does not (`prov: IMPORTED`). Read before `export`/`import`.
- `taxonomy.md`: placing a claim in the topic graph — descent over the generated index, the five verdicts (EXISTS / INADEQUATE / MISSING / GENERALIZES / UNPLACED), the sibling rule, guarded re-parenting, canonicalization — and the answer-mode descent (`§6`). Run at L3 before drafting.
- `guides.md`: pipeline for distilling user-provided indications into `ai_docs/reference/GUIDE_[topic].md`.
- `vision.md`: how to write a Vision a cold reviewer can actually apply — the properties that make a rule hold, the minimum operable sections, and the blind check.
- `distillation.md`: from a source to claim rows — intake (content-addressed originals, stored canonical extraction, every provenance a real file), the claim table, extraction discipline, signal rules (symbiosis with `distill`).
- `reconciliation.md`: what happens when two claims meet — five outcomes, detect-and-hold (the machine never decides), rulings with mandatory `basis:`, the claim state machine, the batched escalation form.
- `review.md`: the review discipline — when a review is due, how to request one, how to receive findings, how to review.
- `dispatch.md`: opt-in subagent execution of an approved plan.
- `routing.md`: which lens owns this unit of work. Read ONLY when a sibling lens skill is installed alongside this one; a single-lens install never reads it.
- `scripts/sdlc_check.py` + `scripts/sdlc_core.py`: the mechanical validator for the docs root (`check`, `validate`, `index`, `stale`, `mark`, `gate`, `plan`, `orient`, `migrate`, and the knowledge overlay: `graph`, `corpus`, `claim-id`, `anchor`, `export`, `import`, plus `remind` — the opt-in per-turn one-line reminder, ENFORCEMENT §4). Two files: the core is the family's shared spine; the entry point IS the knowledge overlay — the claim ledger and topic-graph checks live inside it, so the core alone runs none of them. Copy both, or neither.
- `ENFORCEMENT.md`: optional setup for CI and hooks.

Read these files only when needed. `SKILL.md` is the operating contract; the support files are progressive resources.

## Knowledge Values

- **Understand before writing/updating:** do not modify or create knowledge documents without checking root cause, user constraints, and existing notes — trust the primary sources and existing guides, not memory.
- **Apply DRY and Single Source of Truth:** do not duplicate knowledge across files; extend existing notes (`ANALYSIS_[topic].md` or `GUIDE_[topic].md`).
- **Signal & Distillation:** eliminate fluff, filler, and speculative statements; keep deterministic facts, constraints, decisions, and clear SOP steps (symbiosis with `distill`).
- **Lifecycle & Freshness:** mark superseded knowledge (`status: SUPERSEDED` or `DEPRECATED`) so outdated information does not cause hallucination.
- **Protect the Vision & User Style:** align all knowledge work with user strategic goals, operational preferences, and expected outcomes.
- **Map-First Navigation:** rely on `ai_docs/README.md`, `INDEX.md`, and `reference/INDEX.md` router for targeted retrieval before creating new documents — and before *answering from model memory* on the project's domain (`## Topic Recall`).

## Rule Zero: Triage

Always classify the request before choosing the process. Declare the chosen level to the user when you start operational work.

**Declare the level WITH the router verdict** (one line, for L2, L3 and Spike — L1 declares the level alone): the result of the guide-router lookup described under `## Operative Guides`, i.e. `Level: L2 · router: no match` or `Level: L3 · router: GUIDE_release_sop.md → read`. Name the guide you matched, or `no match`.

| Level | Criteria | Required process |
|---|---|---|
| **L1 - Quick Fact / Snippet** | One claim row added to an existing topic; a typo; a preference update. No node created, no source entering the corpus, no frontmatter change. | Implement edit directly in existing note. No new documents. |
| **L2 - Propagation of settled knowledge** | The fact is **already settled** in the corpus and the work carries it into existing documents — restating, correcting a stale copy, updating an SOP that quotes it. No node created or superseded, no hierarchy change, no node frontmatter change, no new source ingested. | Mini-analysis in message: objective, impact, sources, validation. Update existing document or create single SOP/note. |
| **L3 - New knowledge unit / Corpus** | A source enters the corpus; a topic node is created or superseded; the hierarchy moves; a conflict must be reconciled; or what a claim asserts changes. | Full workflow: Vision Gate, Spec Elicitation, Taxonomy Pass, Knowledge Analysis, Distillation, Review, Indexing. |
| **Spike - Exploration** | Time-boxed exploratory research or draft without merging into official KB. | Outcome in `ai_docs/solutions/SPIKE_[topic].md`. |

Cross-cutting rules:
- **The unit of measure here is knowledge, never file count.** In this domain risk is
  knowledge-shaped: carrying one settled fact into eight documents is small, and one
  claim that re-parents a node is not. Do not import the code lens's file thresholds —
  a level is chosen by what the change does to the corpus and the graph. What keeps
  this from becoming an escape hatch is the trigger list below, which overrides the
  level whatever the size, plus one limit: **propagation that changes what a claim
  asserts is not propagation** — it is a new knowledge unit, so L3.
- **Domain routing (multi-lens installs only).** After the level is set, and only when a sibling lens skill of this family is installed (`agentic-sdlc`, `mkt-agentic-sdlc`), run the router in `routing.md` for every L2, L3 and Spike: it decides which lens's method and validation rules govern this unit of work. L1 never reaches it, and a single-lens install never reads the file — detection fails open. In such a project, never refer to a document whose meaning differs by lens ("threat model", "vision", `principles.md`, `handoff.md`) by its bare name: qualify it with its domain, or name its path.
- Personal data, credentials, security-sensitive processes, authN/authZ specs are high-risk: never L1.
- **Escalation triggers — ANY of these makes it L3, whatever the file count:** the change touches the topic hierarchy (`parents:`, a `GENERALIZES` verdict, a re-parent); it touches more than one node's frontmatter; it creates or supersedes a node other nodes reference. Re-shaping the graph is a unit of change, never a side effect of placing one claim.
- Adding one claim row to an existing topic is L1: the `id` may be left empty (the validator fills it — `claim-id --fill`), and no check errors on a hand-written row.
- If a bigger impact emerges during L1/L2 work, stop, reclassify and declare it.
- When in doubt, pick the higher level.
- **No useless questions.** Every question to the practitioner passes the legality test of the question discipline (`elicitation.md`): searched first with the search named, and the blocked decision named. Claim-conflict escalations additionally carry their own mandated form and are batched at run end (`reconciliation.md` §4).

## Write Triggers

Triage decides IF documentation is due; this table decides WHICH document each event produces, and when. **One event, one destination:** when the trigger fires and the document does not exist, create it; when it exists, update it — never duplicate it.

| Document | Write trigger | Phase |
|---|---|---|
| `solutions/ANALYSIS_[topic].md` | Every L3, after elicitation and before any drafting. On topic match with an existing analysis, update that one instead of a new file. | 3 |
| `solutions/SPIKE_[topic].md` | Closing any Spike — including a negative outcome. | — |
| `vision/features/VISION_[feature].md` | Multi-milestone topic at analysis time, or retroactive trigger (second ANALYSIS on same theme). | 3 |
| `audit/handoff.md` (workstream registry) | **Never by hand — generated by `sdlc_check.py index` from the `HANDOFF_*.md` sources**, and `validate` errors when the two disagree. Regenerate at every L3 closure and at session end; the `Date:` header is derived, so no writer touches it. Inventory for lookup, never a work board. | 5 / session end |
| `audit/HANDOFF_[topic].md` | **One per OPEN workstream, with or without volatile state** — it is the authored home of that workstream's registry row (frontmatter `workstream`/`level`/`branch`/`status`/`since`/`next`/`details`/`updated`), so no file means no row. Carries the resume logistics too; the ANALYSIS Diary keeps the durable narrative (DRY). DELETED at closure — deleting it *is* removing the row. | 4 / 5 / session end |
| `audit/project_notes.md` | A note true for the whole project rather than one workstream. Appended verbatim to the generated registry, so regenerating cannot destroy notes that belong to no workstream. | 5 / session end |
| `audit/handoff.md` — converting an existing project | **Lazily, at the first write — and then ALL AT ONCE.** Converting one row at a time is the state that loses the others, so `index` refuses to write while anything in the file is unaccounted for and names it. Until the first source exists nothing generates and nothing errors. | 5 / session end |
| `audit/audit_plan.md` (Standalone) | Bootstrap, and whenever a mapped area changes state (`sdlc_check.py mark`). | 1 |
| `reference/GUIDE_[topic].md` (`source_kind: document`) | Origin+purpose test (`guides.md`), or a proactive proposal accepted by user. | 4 / 5 |
| `reference/GUIDE_[topic].md` (`source_kind: code`/`domain`) | Recognized high-complexity domain/concept with no CURRENT guide $\rightarrow$ duty to write autonomously. | 4 / 5 |
| `audit/reviews/REVIEW_LOG.md` | Every completed review — recorded in log. | 3 / 5 |
| ADR / Decision Log — `architecture/` or devPNT DB | A strategic decision was taken (pattern, policy, structural change): record before DONE. | 5 |
| `strategic/architecture.md`, `strategic/existing_features.md` | Bootstrap; update at closure when the knowledge catalog actually changed. | 1 / 5 |
| `vision/project_vision.md`, `roadmap.md`, `principles.md` | Bootstrap as `Status: DRAFT`; promoted to APPROVED only by explicit user confirmation. | 1 / 2 |
| `topics/<slug>.md` | A placement verdict creates it (MISSING/INADEQUATE-child, `taxonomy.md`); reconciliation updates its claim rows. One node per topic — a similar-but-distinct concept is a sibling with `related:` + a written distinction, never a merge and never a duplicate. Merged/renamed nodes become tombstones (`status: SUPERSEDED` + `redirect_to:`), never deleted. | 4 |
| a KB bundle (`export`) | Knowledge must leave this project. Export is L1 — it writes nothing into the corpus. **Importing one is L3**: a source enters the corpus and nodes are created, and a bundle is external input, so never L1 whatever its size (`portability.md`). | — |
| `corpus/given/*` + sidecar | A source arrives: it becomes a content-addressed artifact with a sidecar carrying digest/date/`supersedes:`. A text source is copied verbatim. A non-text source yields its stored canonical extraction — copied **beside** the original when that is small enough to keep, or **instead of it** on a large binary corpus, where the original stays where it lives and is recorded as `original_path:`/`original_sha256:` (`distillation.md` §1, which owns this rule). Never edited after ingest — the digest check on whatever `given/` holds is what enforces it. | 4 |
| `corpus/notes/*` | Something is said (`origin: elicited`), synthesised (`derived_from:`), or ruled (`basis:`). A note with none of the three is refused by the validator. | 4 / 5 |
| the day's decisions, at a user-signed closing (the Capture Moment sweep) | Verification that the phase-4 notes/claims exist; NEW `corpus/notes/*` + claim rows only for what the sweep surfaces un-captured. The event is the CLOSING, disjoint from the row above (which fires when something is SAID). | 5 / session end |
| `solutions/PLAN_[topic].md` + its ledger | A source too long for one context is ingested: **one task per reading window** (30 pages by default; the plan states the window used), each ending at a declared `extracted_through:`. That ledger is the register the ingestion resumes from across sessions — ingestion never builds a second one (`distillation.md` §3, `templates.md`). | 4 |
| `corpus/given/*.meta.md` — `extracted_through:` | Every reading window closes by advancing it (`p=<n>`, `L<n>`, `complete`). Required once any claim cites the artifact: unstated, "I am finished" cannot be falsified, which is how a sampled 200-page manual passes for an ingested one. | 4 |
| `INDEX.md`, `reference/INDEX.md`, `topics/INDEX.md`, `corpus/INDEX.md` | Regenerated by `sdlc_check.py index` at closure — never by hand; `validate` fails on a hand-edited one. | 5 |

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
- **Design review gate (end of Phase 3, before any drafting):** the analysis is reviewed by somebody other than its author — a subagent with fresh context, or a declared self-pass when no higher rung is usable — a permission-gated rung is asked about, never silently skipped (`review.md`). Follow `review.md`; log the outcome in `audit/reviews/REVIEW_LOG.md`. A knowledge structure reviewed only by the person who chose it is not reviewed.

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

## Topic Recall — the answer-side consult

The graph is only a second brain if it is READ when answering, not only written when
distilling. The descent (`taxonomy.md`) fires here with a new trigger — the answer-side
twin of the guide consult above.

- **Trigger — unconditional scan on domain assertions.** Whenever the reply would assert
  facts about the PROJECT'S domain (its topics, decisions, sources, constraints), scan
  `topics/INDEX.md`. Plausibility of coverage is judged ON the scanned top rows, never
  before them — "the KB probably doesn't have this" is model memory talking, the exact
  judgement this reflex removes. Exempt: pure mechanics (running a command, editing per
  explicit instruction), general knowledge outside the project's domain, L1 gestures.
- **Once per topic per SESSION.** The dedup key is the matched slug (known ex post); a
  question plainly within an already-descended branch reuses that consult, and a
  placement descent already run this session counts. A compaction starts a new session.
- **The act.** Descend per `taxonomy.md` §6 (same doctrine, answer mode). On claims,
  answer FROM them citing claim ids; a claim whose `state` is `SUPERSEDED <id>` is never
  cited without naming its successor.
- **The declared verdict — only when the recall ran**, never a per-turn ritual. Four
  legal values:
  - `kb: <slug> → N claims cited`
  - `kb: <slug> → node matched, no claims` — surface the node's `gaps:` when it answers
    the question: "the KB knows it doesn't know" is a first-class answer.
  - `kb: no coverage` — index read, nothing fits.
  - `kb: index absent — regenerate (sdlc_check.py index)` — the INDEX is missing, not
    necessarily the graph (nodes routinely exist while the index lags); regenerate and
    rescan.
  Never fake the verdict: an always-"no coverage" verdict certifies a lookup that did
  not happen. The `router:` and `kb:` verdicts are independent and may co-occur, one
  line each — a how-to question can match a guide AND carry claims.
- **Anti-echo — the re-touch rule.** When a DERIVED claim grounds a decision the user is
  about to take, walk its chain to non-DERIVED ground — a GIVEN artifact, an ELICITED or
  RULING note — and cite that ground beside the claim id; re-opening only the immediate
  target may re-read the agent's own synthesis, which is the echo chamber itself. If the
  ground does not resolve (imported bundle without originals, external `original_path:`,
  tombstone): say so beside the claim id and treat the claim as **unverified for
  decision-grounding** — surfaced, never silently cited. Per-provenance stance: GIVEN's
  source column is already the direct citation; ELICITED/RULING carry the practitioner's
  own authority; an IMPORTED claim grounding a decision is named as un-re-ratified
  foreign authority.
- **The trace persists.** When the decision is recorded (a ruling note, a diary entry),
  that record cites the claim id AND the re-touched ground — the trace survives in the
  corpus, not in ephemeral chat.
- **Under dispatch**, recall is an orchestrator concern: the orchestrator runs the
  descent itself; a context-free subagent never runs its own. The task schema has no
  claims field today, so until a dispatch-focused unit adds one, the orchestrator
  inlines the cited claim rows in the task's free text — an explicit interim.

## The Capture Moment — the day's decisions reach the ledger

Capture today is what makes recall honest tomorrow: a captured elicited or ruled note
is exactly the non-DERIVED ground the re-touch rule above walks to. The rails all
exist — this section adds only the MOMENT.

- **When — user-signed closings, once per session.** Phase 5 of a governed unit, or
  any closing signal from the user in an un-governed session ("chiudiamo", "we're
  done"); the session-end pass that updates `handoff.md`/`project_notes.md` then runs
  at that same closing. Never per-turn, never a standing interruption. **Declared
  residual**: an unsignaled end (the user simply stops writing) captures nothing —
  the phase-4 duty (a decision stated mid-session owes its note WHEN SAID) is the
  protection for sessions that never close, and the orient's recency line makes the
  miss visible next time. That line measures NOTES recency, not full ledger
  freshness, and trusts frontmatter `date:` over file mtimes — mtimes lie after a
  clone or worktree.
- **The sweep question.** At the closing, ONE question, carrying its own search
  result inline: "today I recorded: [what the sweep found already on the rails] —
  any other decisions from today to record?". Scoped to TODAY, so it reaches
  decisions taken outside the session (a meeting, a call) that no transcript search
  could find — facts only the practitioner owns. This is a **scheduled elicitation**
  in the same family as the phase-3 round, not a blocking question (nothing stalls;
  the session is ending), so the blocking form does not attach; the inline result
  satisfies the search-first duty. "Niente" ends it.
- **The sweep is idempotent.** It verifies the day's decisions are on the rails; a
  decision already noted at phase 4 is verified, never re-captured — no second note,
  no duplicate claim row. The moment closes gaps; the phase-4 row stays the primary
  channel.
- **What counts as a decision**: domain choices made or confirmed today — a value, a
  threshold, a rule, a stated preference, a rejected alternative with its reason.
  NOT mechanics (commands run, files edited), NOT process state (the handoff's job).
- **The channeling — existing rails, explicit provenance.**
  - The user's words → `corpus/notes/*` with `origin: elicited` and a `date:`; a
    claim row distilled from it carries `prov: ELICITED`, source = that note with a
    legal `L<a>-<b>` locator.
  - A synthesis of the day's discussion → a note with `derived_from:` → claim
    `prov: DERIVED`.
  - **RULING only when the decision resolves an existing contested set** — then
    `reconciliation.md` §2 applies in full (mandatory `basis:`, supersession of the
    whole prior set). A fresh conflict-free decision is captured elicited: a preference
    is not a fact, and `basis:` is reserved for the fact the corpus lacks.
  - A fact on an existing topic → claim row, L1 (`id` empty; `claim-id --fill`).
  - No owning topic → the note is written NOW and the placement is declared as the
    next kb unit. Capture never smuggles an L3 hierarchy change, and
    `topics/unplaced.md` is never a decision park — UNPLACED is for topic-less
    scraps and is invisible to recall.
- **Reconciliation is wired.** A captured claim meeting an existing claim on the
  node classifies per `reconciliation.md` — capture can confirm, refine, coexist or
  CONTEST, never silently overwrite.
- **Silence stays legal where no one signed off**: no closing signal → no question,
  no ritual line.

## Mechanical Enforcement
- `scripts/sdlc_check.py index`: updates `ai_docs/INDEX.md` and `ai_docs/reference/INDEX.md`.
- `scripts/sdlc_check.py validate`: validates YAML frontmatter (`status`, `description`).
- `scripts/sdlc_check.py check`: checks dirty closures and missing indexes.
