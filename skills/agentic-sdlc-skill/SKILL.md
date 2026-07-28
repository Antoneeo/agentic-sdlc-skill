---
name: agentic-sdlc
description: Documentation-First SDLC protocol with risk-proportional triage, Vision as a guide, a complete Standalone mode and optional symbiosis with devPNT. Use for features, significant bugs, refactors, audits and documented maintenance.
author: Antonio Pinto (https://github.com/Antoneeo)
copyright: (c) 2026 Antonio Pinto
---

# Agentic SDLC

**Why this skill exists:** to prevent *myopia* — acting from partial understanding, where a change breaks what it did not account for and hard-won knowledge evaporates between sessions. Triage, the Vision Gate, the documentation lifecycle and comprehension guides are all one defense against that.

This skill guides software development with a Documentation-First process proportional to risk. It must work fully even without devPNT. When devPNT is available and configured for the current project, the skill works in symbiosis with its governance: M-VISION, Master Plan, Action Plan and versioned artifacts become the authoritative frame for milestones and implementation.

Support files in the skill directory:
- `templates.md`: templates for Vision, ANALYSIS, Spike, audit plan and handoff.
- `architect.md`: the architect pass — do the components and services this feature needs already exist? Run at L3 before drafting the Impact.
- `guides.md`: pipeline for distilling user-provided indications into `ai_docs/reference/GUIDE_[topic].md`.
- `vision.md`: how to write a Vision a cold reviewer can actually apply — the properties that make a rule hold, the minimum operable sections, and the blind check run before promoting one to APPROVED.
- `scripts/sdlc_check.py`: mechanical validator for `ai_docs/` (`check`, `validate`, `index`, `stale`, `mark`, `gate`).
- `ENFORCEMENT.md`: optional setup for CI and hooks.

Read these files only when needed. `SKILL.md` is the operating contract; the support files are progressive resources.

## Technical Values

- **Understand before acting:** do not modify code without understanding root cause, constraints and current shape — including re-reading a component you think you remember, because your model of it rots between sessions; trust the code (and its comprehension guide), not memory.
- **Preserve architectural coherence:** respect existing layers, responsibilities, naming, patterns and conventions.
- **Apply DRY and simplicity:** do not duplicate logic or knowledge; abstract only when it reduces real complexity.
- **Preserve quality:** every change must maintain or improve stability, testability and maintainability.
- **Verify technically:** close implementation work with tests, lint, smoke checks or an explicit reason.
- **Keep useful memory:** document relevant decisions and operational state, not filler text.
- **Protect the Vision:** every decision must stay aligned with expected benefits, the actors it serves (and the UX they expect), non-goals and success signals.

If a patch looks easy but you do not understand why the current code is shaped the way it is, investigate first.

## Rule Zero: Triage

Always classify the request before choosing the process. Declare the chosen level to the user when you start operational work.

**Declare the level WITH the router verdict** (one line, for L2, L3 and Spike — L1 declares the level alone): the result of the guide-router lookup described under `## Operative Guides`, i.e. `Level: L2 · router: no match` or `Level: L3 · router: GUIDE_release.md → read`. The lookup is the consult trigger; making its result a declared output is what keeps it from being skipped — a level declared without a verdict makes "did not look" indistinguishable from "looked, nothing matched". Name the guide you matched, or `no match`; name a second one only when it covers a genuinely distinct concern (typically one operative guide plus the comprehension map of the component you are touching). The verdict is never a listing of the catalogue, and never an excuse to read every guide.

| Level | Criteria | Required process |
|---|---|---|
| **L1 - Trivial** | About 10 lines in 1-2 files; no API, dependency or new-behavior change; typos or fixes restoring already-expected behavior | Implement. Run relevant existing tests. No new documents. |
| **L2 - Small** | Clear root cause; at most 3 files; no new dependency or public API; low risk | Mini-analysis in the message: objective, impact, security, tests. Tests mandatory. No new document, except updating an existing analysis on the same topic, or the handoff (see Write Triggers). |
| **L3 - Significant** | More than 3 files, APIs/contracts, new dependency, user-visible behavior, security-sensitive area, architectural change or non-obvious design | Full workflow: Vision Gate, analysis, plan, implementation, tests, closure. |
| **Spike** | Time-boxed exploration to reduce uncertainty | Code not mergeable into main. Outcome in `ai_docs/solutions/SPIKE_[topic].md`. For production, reclassify as L2 or L3. |

Cross-cutting rules:
- Parsing of external input, authN/authZ, cryptography, networking, personal data and filesystem access are security-sensitive: never L1.
- If a bigger impact emerges during L1/L2 work, stop, reclassify and declare it.
- When in doubt, pick the higher level.
- The full audit does not start for L1/L2 unless explicitly requested.

## Write Triggers

Triage decides IF documentation is due; this table decides WHICH document each event produces, and when. **One event, one destination:** when the trigger fires and the document does not exist, create it; when it exists, update it — never duplicate it. This table is the authoritative write index — the workflow phases carry the surrounding procedure and point here for the trigger.

| Document | Write trigger | Phase |
|---|---|---|
| `solutions/ANALYSIS_[feature].md` | Every L3, after elicitation and before any code. On topic match with an existing analysis, update that one instead of a new file. A capability the architect pass splits out as its own unit of change (`architect.md` §4) gets its own ANALYSIS, and the two documents name each other. | 3 |
| `solutions/SPIKE_[topic].md` | Closing any Spike — including a failed one (a negative outcome is still an outcome). | — |
| `vision/features/VISION_[feature].md` | Feature known multi-milestone at analysis time, OR the retroactive trigger: you are about to create the SECOND `ANALYSIS_*` on the same theme — extract the shared feature vision first, then let both analyses reference it. | 3 |
| `audit/handoff.md` (workstream registry) | One row per OPEN workstream (feature, level, branch, status, since, next step, pointer to its Diary/HANDOFF file) — parallel-safe: closing one milestone touches one row, never another's resume point. Refresh the row at every L3 closure (remove it) and at session end when that ANALYSIS is IN_PROGRESS; discretionary after an L2. ≤ 20 lines. | 5 / session end |
| `audit/handoff.md` — legacy narrative form (pre-1.17 projects) | **Convert lazily, on first write, never as a migration sweep.** A narrative handoff still works: read it as a single-row registry (`## Active features` bullets = the rows, `## Next step` = that row's next step). The first time the Write Trigger above fires, write it in registry form; until then, leave it. Nothing breaks in the meantime — the validator checks only the `Date:` header and its age, and the `orient` hook reads the file verbatim at the same path. | 5 / session end |
| `audit/HANDOFF_[feature].md` | Session ends with that feature unfinished AND there is volatile resume state (branch/worktree, uncommitted work, environment notes, next command). **Resume logistics only — the ANALYSIS Diary keeps the durable narrative (DRY)**; the file is ephemeral and is DELETED at that feature's closure, same step that flips the ANALYSIS to COMPLETED. | 4 / 5 / session end |
| `audit/audit_plan.md` (Standalone) | Bootstrap, and whenever a mapped area changes state (`sdlc_check.py mark` records the reference — git hash, else UTC timestamp). | 1 |
| `reference/GUIDE_[topic].md` (`source_kind: document`) | Origin+purpose test (`guides.md`), or a proactive proposal the user accepted. Propose, never a silent write, never from model knowledge. | 4 / 5 |
| `reference/GUIDE_[topic].md` (`source_kind: code`) | Recognized high-complexity component/feature/layer with no CURRENT guide — including one that breaks repeatedly across sessions → **duty to write autonomously** (no proposal; additive, code-anchored, reversible). Fidelity floor: every claim traces to a code excerpt. Signals + guard-rails: `guides.md` §1. Write it as soon as you recognize the signal; the Phase-5 Comprehension checkpoint is the backstop that asks the question, never the only moment it may fire. | 4 / 5 |
| ADR — `architecture/` (Standalone) or devPNT DB (Hybrid) | An architectural decision was taken (new pattern, layer or contract change, structural dependency): record it at closure, before DONE. No decision, no ADR. | 5 |
| `strategic/architecture.md`, `strategic/existing_features.md` | Bootstrap; update at closure when the stack or the feature catalog actually changed. | 1 / 5 |
| `strategic/architecture.md` — `## Component Map` | A component was BORN or its contract changed: the same closure that builds a capability the ledger ruled MISSING/INADEQUATE adds or corrects its row (`architect.md`). Keyed on the component, not on the stack — a new component is not a stack change, and that is how the inventory silently rots. | 5 |
| `vision/project_vision.md`, `roadmap.md`, `principles.md` | Bootstrap, as `Status: DRAFT`; promoted to APPROVED only by explicit user confirmation, and only after the blind check (`vision.md` §6) — which also gates any amendment of an APPROVED Vision. Write it against `vision.md` §1–§4 from the first draft. | 1 / 2 |
| `INDEX.md`, `reference/INDEX.md`, `strategic/features_history.md` | Never by hand: regenerated by `sdlc_check.py index` at closure when canonical docs or guides changed (prose discipline where the validator is not adopted). | 5 |

## Operating Modes

### Full Standalone

Use this mode when devPNT is unavailable, not configured for the current project, or the user explicitly asks for a filesystem-only workflow.

Source of truth:
- Vision: `ai_docs/vision/project_vision.md`, `roadmap.md`, `principles.md`.
- Features/analyses: `ai_docs/solutions/ANALYSIS_[feature].md`.
- Audit/handoff: `ai_docs/audit/`.
- Feature history: `ai_docs/strategic/features_history.md` — generated by `sdlc_check.py index` (kept by hand as a prose discipline only in environments without Python).

Standalone mode is not reduced: it must handle audits, features, significant bugs, tests, handoffs and closure without devPNT.

### Hybrid in symbiosis with devPNT

Use this mode when the `devpnt_*` tools are available and point at the current project.

Authoritative hierarchy:
1. **devPNT M-VISION**: strategic beacon of the milestone. Before design or code, read it and verify benefits, success signals, scope-in and non-goals.
2. **devPNT Master Plan**: strategic roadmap and milestones.
3. **devPNT Action Plan**: current tactical work for the active goal.
4. **devPNT governed artifacts**: `D-UC`, `P-TM`, `E-ISP`, `E-TDD`, `E-TP`, ADR.
5. **Local `ai_docs/`**: readable context, Standalone fallback, local handoff or shadow/mirror when useful.

Hybrid rules:
- devPNT is the governed source for plans and artifacts; do not create a second truth in `ai_docs/`.
- The skill stays autonomous: if devPNT is not there, switch to Standalone without losing capability.
- If the user request, the local Vision and the M-VISION diverge, stop and make the conflict explicit.
- Do not create or modify milestones without respecting the M-VISION.
- Never auto-accept devPNT proposals: present the preview and wait for explicit confirmation.
- If the local devPNT protocol imposes stricter bootstrap, plans or gates, follow them.

## Coexistence with devPNT (the Hybrid seam)

This section is the single authoritative answer to "who owns what" when both the
skill and devPNT are active. The skill owns the **process** (triage, phases, Vision
Gate, lifecycle); devPNT owns the **machinery** (governed storage, versioned
proposals, semantic analysis, independent reviewers). devPNT strengthens the
process; it never replaces it.

### Ownership matrix

| Artifact | Standalone master | Hybrid master | Mirror rule |
|---|---|---|---|
| Product vision | `vision/project_vision.md` | `vision/project_vision.md` (product scope) | devPNT KL vision is regenerated from it, never edited independently |
| Milestone vision | `vision/roadmap.md` milestones | devPNT M-VISION | `roadmap.md` may reference the M-VISION key; it never restates its content |
| Feature design | `solutions/ANALYSIS_[feature].md` | devPNT E-ISP/E-TDD (+ D-UC/P-TM) | shadow exported from the ACCEPTED DB version as `SHADOW_[doc_key]_vX.Y.md`; on divergence the DB wins and the shadow is regenerated |
| Plans | `## Action Plan` inside the ANALYSIS | devPNT Master/Action Plan | none |
| Feature state | ANALYSIS frontmatter `status` | Action Plan node status | mapping table below; at closure both must move together |
| ADR | `architecture/` (canonical dir) | devPNT DB (`adr_YYYY-MM-DD_slug`) | optional filesystem shadow `SHADOW_adr_*` exported at closure for grep-ability |
| Audit / freshness | `audit/audit_plan.md` + `stale`/`mark` | devPNT KL coverage + summary status | run `check --hybrid` (skips audit-plan staleness) |
| Operative guides | `ai_docs/reference/` | `ai_docs/reference/` — **filesystem-first even in Hybrid** | devPNT bootstrap may point at their index; it never copies their content |
| Handoff | `audit/handoff.md` | `audit/handoff.md` | always filesystem |

### Triage equivalence (one threshold, two vocabularies)

devPNT's "significance threshold" and the skill's triage are the SAME test. Do not
run two classifications:

| Skill triage | devPNT equivalent | Governed artifacts |
|---|---|---|
| L1 Trivial | trivial exempt | none |
| L2 Small | localized obvious edit | none — but see escalation |
| L3 Significant | governed unit of change | D-UC/P-TM/E-ISP/E-TDD per the devPNT trigger policy |
| Spike | exempt (non-mergeable) | `SPIKE_[topic].md` only |

Escalation triggers (any one of these makes it L3, in BOTH vocabularies): touches
more than one module, changes a public API/contract/message format, changes a data
model or state machine, has a security surface, risks duplicating existing logic,
or the design choice is non-obvious. An L2 that trips one of these is not an L2.

### Feature state mapping

| ANALYSIS frontmatter | devPNT plan node |
|---|---|
| PLANNED | READY (or BLOCKED / ON_HOLD while waiting) |
| IN_PROGRESS | PROGRESS |
| COMPLETED | DONE |
| CANCELLED | CANCELLED |

Closure discipline: never mark the node DONE while the shadow/ANALYSIS still says
IN_PROGRESS, or vice versa. They move in the same closure step.

### Shadow discipline (Hybrid)

- Shadow filename: `SHADOW_[doc_key]_vX.Y.md`, first line
  `<!-- SHADOW generated from devPNT (doc_key vX.Y) - do not edit by hand -->`.
  Never save a shadow under an `ANALYSIS_*` name: that name means "authoritative
  Standalone document" and the validator treats it as such.
- **Export the approved E-TDD shadow BEFORE implementation** (not only at closure).
  It gives context-free subagents their design input, unlocks `gate --hybrid`, and
  guarantees the filesystem fallback if devPNT becomes unavailable mid-feature.
- At closure, refresh all shadows from the accepted DB versions.

### Validator in Hybrid

Pass `--hybrid` explicitly (never auto-detected — an explicit flag beats a guessed
mode): `check --hybrid` and `stale --hybrid` skip audit-plan staleness (mapping is
delegated to devPNT/KL) — guide-drift checking still runs (`ai_docs/reference/`
is filesystem-first even in Hybrid, see the ownership matrix above); `gate --hybrid`
also unlocks on the presence of an E-TDD shadow in `solutions/` (the Hybrid design
gate) instead of requiring an IN_PROGRESS ANALYSIS.

## L3 Workflow

### 1. Audit and Alignment

- Read `ai_docs/audit/handoff.md` if it exists — the **workstream registry**: one row per open workstream, so you see at a glance what is in PROGRESS, on which branch, since when, before touching anything. If a row's Date/Branch are inconsistent with reality, treat that row as history. When resuming a specific workstream, read its `audit/HANDOFF_[feature].md` (volatile resume logistics) AND its ANALYSIS Diary (durable narrative) — the registry row points at both. A **narrative handoff from a pre-1.17 project** reads as a single-row registry; convert it when you next write it, not now (Write Triggers).
- Read `ai_docs/README.md` (curated must-reads), `ai_docs/INDEX.md` (generated manifest of all canonical docs) and `ai_docs/reference/INDEX.md` (the guide router) to know what exists before exploring the code. The router is a mandatory read, not an optional one: it is the only orientation step that tells you a guide already governs the work you are about to do. `solutions/` and `audit/` are not indexed per file: search them with glob/grep.
- Recommended default: a SessionStart hook (`ENFORCEMENT.md` §4) emits this orientation automatically at session start (README + INDEX + guide router + handoff + triage reminder), so the router reaches the context even in a session that never opens Phase 1 explicitly. Wire it wherever Python is available; when it is not wired, do these reads manually as above — the process never depends on it, and it fails open (a missing/empty `ai_docs/` never blocks the session).
- If `ai_docs/` is missing or incomplete, create the structure and the **bootstrap set** by analyzing the project in batches: `README.md`, the three `vision/` docs (`Status: DRAFT`), `strategic/architecture.md`, `strategic/existing_features.md` and — Standalone — `audit/audit_plan.md`; then regenerate `INDEX.md`. Nothing else is mandatory at bootstrap (per-document triggers: Write Triggers).
- **Arriving in a project that was never curated** (the usual case — you arrive with a task, not with a bootstrap): write `audit/audit_plan.md` FIRST. It is the scope ledger the rest is built on — one row per area, all PENDING, `SKIPPED` for what genuinely does not merit reading (vendored, generated). Then the other bootstrap documents describe what you have actually analyzed, and the `## Component Map` in `strategic/architecture.md` starts at whatever the first task made you understand. **No full-codebase sweep is required before the first feature**: the map grows feature by feature, each one marking the areas it covered (`sdlc_check.py mark`). What is NOT deferred is comprehension of what the change touches or depends on — that is understood now, at full standard, mapped or not. The licence is about writing the inventory, never about designing on a guess (`architect.md` §2: unmapped is *unread*, not *empty*, and can never ground a MISSING verdict).
- In Standalone use `ai_docs/audit/audit_plan.md` for mapping and state.
- In Hybrid prefer the devPNT/KL mapping when available; do not duplicate plan governance.
- For detailed templates use `templates.md`.

### 2. Vision Gate

Standalone:
- Read `project_vision.md`, `roadmap.md`, `principles.md`.
- If a document declares `Status: DRAFT`, treat it as a hypothesis: flag conflicts, but do not block an explicit user request.
- If it declares `Status: APPROVED` and the request conflicts, stop and ask for a choice: update the Vision or modify/reject the request.
- Never promote a Vision to `APPROVED` without the user's confirmation.
- **Writing or amending a Vision is its own discipline — follow `vision.md`.** Draft against its §1–§4 (the properties that make a rule survive a motivated reader, and the minimum sections a gate needs), then run the **blind check** (§6) before promotion to APPROVED and before any amendment of an approved Vision. A Vision that has never been read cold by someone with no other context has not been tested at the only thing it exists to do.

Hybrid:
- Read the milestone's M-VISION, or ask for/create the step required by the devPNT protocol.
- Verify that the request serves a benefit or success signal of the M-VISION.
- If the request adds unauthorized scope, treat it as a Vision divergence.
- The M-VISION is a Vision: `vision.md` applies to it too. The gate lens of the blind check (§6) is the proportional subset for a milestone-scope document.

### 3. Request Analysis

For any L3, run the spec elicitation round in `elicitation.md` BEFORE drafting the analysis (skip path inside — one-line note when the spec is already complete).

**Architect before you list files.** Once the spec is known and BEFORE drafting the Impact, run the architect pass in `architect.md`: state what the feature requires the system to be able to DO (capabilities — verbs over domain nouns, no files), rule each one against the platform — **EXISTS** (name the component and where it lives) / **INADEQUATE** (name the gap) / **MISSING** (say what you searched) — and design what is missing as a component with **its own contract, in its own vocabulary**, of which this feature is one consumer. The output is the ANALYSIS `## Capability Ledger`, which feeds the Impact. Why it is its own step: a feature is not a unit of construction, and an agent that skips it builds the missing capability inside the feature's code path, where no component owns it and the next feature rebuilds it differently. The pass is a question, not a form — when every capability plainly exists, one line answers it.

**Blast-radius enumeration is an authoring duty, not a review finding.** Before writing the Impact (the list of what changes), for every symbol whose signature you change, thread a new field through, or that has more than one caller: mechanically enumerate EVERY consumer with the best symbol-graph tool your toolchain offers — an LSP/IDE call hierarchy or a find-usages / call-graph capability — with `grep` only as a last-resort fallback, and list the full set in the Impact. Anchor to symbol identity, not line numbers (they rot). This is deterministic and cheap: doing it up-front collapses the review into one pass, instead of the reviewer returning "you missed a consumer" one round at a time. Leaving completeness to the closure review is the myopia failure this whole workflow exists to prevent.

Standalone L3:
- Before creating a new `ANALYSIS_[feature].md`, search `ai_docs/solutions/` with glob/grep for an existing analysis on the same topic: if there is one, update it instead of duplicating it.
- Create or update `ai_docs/solutions/ANALYSIS_[feature].md`.
- Minimum sections: Objective, Feature Vision (or Vision Alignment), Capability Ledger, Impact, Security and Threat Model, Action Plan, Test Strategy, Diary/Current State.
- Build the Impact/solution **on** the Vision, the use-cases/user-needs and the Security & Threat Model — read and trace to them first, and state the trace (which actor / use-case / threat / benefit each part serves) so the closure review (`review.md`) can verify conformance. Do not draft the Impact in isolation.
- For a feature known to span multiple milestones, also create `ai_docs/vision/features/VISION_[feature].md`; the retroactive case (extract it when the SECOND `ANALYSIS_*` on a theme appears) is in Write Triggers.

Hybrid L3:
- Restore the Master Plan, Action Plan and linked documents.
- Use devPNT for plans and governed artifacts.
- Use `ai_docs/solutions/SHADOW_[doc_key]_vX.Y.md` only as a readable shadow when needed; on divergence devPNT wins.

### 4. Development and Testing

- Implement only after the documentation gate required by the level.
- Isolate the work: run an L3 change on its own branch. In Hybrid, prefer a git worktree from the start — a running devPNT server locks `.devpnt/*.db` and blocks in-place branch switches/merges in the primary worktree.
- Modify surgically, consistently with the plan.
- Implementation work follows the TDD discipline in `tdd.md` (RED/GREEN/REFACTOR — the L2/L3 default; record the reason when it does not apply).
- Before implementing (L2/L3; L1 exempt), **consult the guide router** for a guide covering the task — operative, or a comprehension map of the component you are about to touch — and read it first (the consult trigger, `guides.md` §0, summarized under `## Operative Guides`). A targeted description match, not a blanket read. Its result is the router verdict already declared with the triage level (Rule Zero); re-run the lookup here only if the work has moved to a topic the first lookup did not cover, and say so if the verdict changes.
- If the environment does not allow automated tests, declare the alternative verification and the reason.
- For bugs (L2/L3), follow the systematic debugging method in `debugging.md`.
- Circuit breaker: after 3 consecutive runs without progress on the tests, stop, switch to the systematic method in `debugging.md`, and ask for instructions if still stuck. `debugging.md` also covers **chronic fragility** — a component that breaks repeatedly across sessions is a comprehension + complexity signal (write the `source_kind: code` guide AND escalate a refactor), not a fourth patch.
- Update the ANALYSIS Diary or the Action Plan when you complete milestones, hit blockers, change decisions, or a session ends with work unfinished.
- **Opt-in subagent execution**: for an L3 with an approved design, the orchestrator MAY execute the work via subagents per `dispatch.md`, gated by `sdlc_check.py plan validate` ("no valid plan, no dispatch"); default stays same-session. Hybrid: the executable `PLAN_[feature].md` is `derived-from` the accepted E-TDD, never independently authored.

### 5. Closure

- Run the relevant tests/lint/smoke checks.
- For the review itself follow `review.md` (requesting and receiving findings) — the single definition, intended for reuse by the Hybrid review gates (devPNT-side wiring out of this unit's scope).
- Verify alignment with the local Vision or the devPNT M-VISION.
- If the work was governed by user-provided indications and is reusable, **PROPOSE distilling a guide** (proactive trigger, `guides.md` §1) — a proposal for the user, never a silent write, never from model knowledge.
- **Comprehension checkpoint**: ask explicitly — *did this session force me to build a model of a high-complexity component that no CURRENT guide covers?* If yes, WRITE the `source_kind: code` guide now (a duty, not a proposal — `guides.md` §1) and say so in the closure. The knowledge you paid to build is at its most complete right here; one closure later it is gone, and the next session re-derives it or breaks the component from partial understanding.
- Update only the documents actually impacted.
- **Update the workstream registry (`audit/handoff.md`)** — mandatory at every L3 closure: REMOVE the closed workstream's row and DELETE its `audit/HANDOFF_[feature].md` (history lives in git and in the Diary); leave every other row untouched — that is the parallel-safety the registry exists for. ≤ 20 lines. The session-end rule and the L2 case: Write Triggers.
- **Aligned indexes (Poka-Yoke)**: if you created, moved or removed canonical documents (`vision/`, `reference/`, `architecture/`, `functional/`, `strategic/`):
  - regenerate the manifest with `sdlc_check.py index` (writes `ai_docs/INDEX.md`) — never write it by hand;
  - if the document is a must-read, add/update its line in the curated `README.md`;
  - if the document replaces another, mark the old one `status: SUPERSEDED` and declare `supersedes:` in the new one;
  - if you created a new canonical subdirectory, give it a purpose in `README.md`.
  A canonical doc that is unindexed or lacks `status` = dirty closure (`sdlc_check.py check` fails/warns). Do not declare DONE until it is clean. Details: section "ai_docs documents".
  - guides created or changed: `sdlc_check.py index` regenerates BOTH manifests (`ai_docs/INDEX.md` and the guide router `ai_docs/reference/INDEX.md`) in one run.
- If an architectural decision was taken (new pattern, layer or contract change, structural dependency), record an ADR before DONE — Standalone in `architecture/`, Hybrid propose the ADR/KL update in the devPNT DB. No decision, no ADR (Write Triggers).
- In Standalone, if the project adopts `sdlc_check.py`, run `python <skill_dir>/scripts/sdlc_check.py check --root <project_root>` or the equivalent local copy.
- Updated documents must travel in the same commit/PR as the code they describe.
- **Branch/worktree hygiene**: an L3 ran on its own branch (Phase 4) — close it with an explicit merge decision (merge, keep open, or discard) and clean up the branch/worktree; never leave orphan branches. In Hybrid, the running devPNT server locks `.devpnt/*.db`, so the merge is done from a separate git worktree or via a ref-only push, never an in-place branch switch in the primary worktree.

## ai_docs documents: two indexes + lifecycle

Documents in `ai_docs/` play two roles served by two distinct indexes — do not confuse them:

- **`ai_docs/README.md` (curated, by hand):** the reading priority. Few lines, only canonical must-reads, changes rarely. Human judgement on "what to read first".
- **`ai_docs/INDEX.md` (generated, `sdlc_check.py index`):** the complete manifest of every canonical doc (`vision/`, `reference/`, `architecture/`, `functional/`, `strategic/`) with description and status. Never by hand: it is regenerated, so it does not drift.
- **`strategic/features_history.md` (generated):** the ANALYSIS history, from their frontmatter.
- `audit/` and `solutions/` are discovery-by-grep: they do not enter the manifest.

**Canonical document header (lifecycle).** Every doc in those directories should open with a minimal frontmatter, so the manifest generates itself and an agent knows immediately whether to trust it:

```markdown
---
description: One line — what it is and when to read it.
status: CURRENT              # CURRENT | SUPERSEDED | DRAFT | DEPRECATED
supersedes: old_doc.md       # only if it replaces another doc
---
```

As a fallback (no frontmatter) the manifest derives the title from the first `# H1` and the description from the first prose line or blockquote; but without `status` a doc carries no freshness signal. A missing `status`, an invalid value, or a superseded doc still marked `CURRENT` = warning in `validate`. A `SUPERSEDED` doc stays on the filesystem as history, but its state declares it dead: no more greps leading back to obsolete guidance.

Without Python/hooks (minimal environments) the indexes and headers remain a prose discipline: update `README.md` and mark the `status` by hand; the validator is only the backstop where it is adopted.

Legacy note: the validator also accepts the deprecated Italian frontmatter keys (`stato`, `livello`, `data_inizio`, `data_fine`) and Italian section headings in existing projects. New documents must use the English forms.

## Operative Guides

Guides are **consulted, created, proposed, and (for code) authored for comprehension** — four moments; the mechanics live once in `guides.md`. Two source kinds: `document` (user indications, operative) and `code` (a comprehension map of a complex component):
- **Consult (before acting):** before operative L2/L3 work (L1 exempt), check the guide router for a guide covering the task and read the match first — a targeted description match, never a blanket read. **Declare the verdict** on the same line as the triage level (Rule Zero): the lookup is only reliable when its result is visible. → `guides.md` §0.
- **Create (from user indications):** the origin+purpose test below (`source_kind: document`).
- **Propose proactively (after success):** after reusable, user-indication-governed work, PROPOSE distilling a guide — a proposal, never a silent write, never from model knowledge. → `guides.md` §1.
- **Comprehend (code, autonomous):** when a component/feature/layer is high-complexity and no CURRENT guide covers it, it is your DUTY to WRITE a `source_kind: code` comprehension guide autonomously — no proposal (additive, code-anchored, reversible); every claim traces to a code excerpt. Signals + guard-rails: `guides.md` §1.

Trigger test: the user hands over indications to follow (origin = user, not model
knowledge) meant to govern how the agent operates (purpose = operative), not just
inform an answer. Both hold → distill into `ai_docs/reference/GUIDE_[topic].md`.

A guide TRAINS the agent, two levels: the guide is the **synthesis** a trained
agent carries (compact — read whole before acting); the verbatim snapshot in
`.sources/` is the **book**, reached on demand via the section markers. Fidelity
constraint: only what the source supports; gaps marked `[not covered by source]`,
never filled from general knowledge; selection and compression expected, addition
forbidden. Full pipeline, DRY rule, snapshotting and maintenance: `guides.md`.

`ai_docs/reference/INDEX.md` is generated (the guide router) — never edit by hand,
regenerate with `sdlc_check.py index`.

**Agent-global KB.** A second, cross-project guide root lives at the fixed path `~/.agentic-sdlc/` (same `ai_docs/` structure, same validator/router/freshness engine via `sdlc_check.py --root ~/.agentic-sdlc`). Project guides win on topic collision; a project guide that overrides a KB guide MUST declare `overrides: GUIDE_<topic>.md` — the validator warns on undeclared collisions (error under `--strict`) and fail-closes on an `overrides:` value that escapes the KB. Discovery is this paragraph: agents and subagents reach KB guides by path, exactly like project guides.

## Mechanical Enforcement

The prompt is not enforcement. When the project needs repeatable guarantees:
- read `ENFORCEMENT.md`;
- use `scripts/sdlc_check.py validate --strict` in CI;
- use `scripts/sdlc_check.py gate` only for security-critical directories, not for the whole repository;
- (skill development) the self-eval battery `python -m unittest discover -s scripts -p "test_*.py"` guards the skill's own doctrine invariants and is the deterministic release gate — see `ENFORCEMENT.md` §5.

The validator is a support, not a universal prerequisite: the skill must stay usable in environments without Python or hooks, declaring what it cannot verify automatically.
