---
description: F-039 unit 1 of VISION_kb_second_brain - the topic-recall reflex and the anti-echo rule in the kb lens. The reading doctrine exists (taxonomy descent); this unit gives it the answer-side trigger the guide router already has.
status: PLANNED
feature: F-039
id: F-039
start_date: 2026-08-27
level: L3
branch: feat/kb-recall-reflex
---
# ANALYSIS: KB Recall Reflex (second-brain unit 1)

**Level: L3 · router: no match** (monorepo `reference/INDEX.md` carries only `GUIDE_release.md`, not applicable).

## Feature Vision
`VISION_kb_second_brain.md`, APPROVED 2026-08-27 — this is unit 1 of its sequence; unit 3 explicitly waits for the data units 1-2 generate.

## Objective
The descent fires only inside a kb unit of work (placing claims). Nothing triggers it when the agent ANSWERS a question that rests on project-domain knowledge — recall is left to model memory, the mechanism proven not to fire (distill "ALWAYS use", the orient hook's origin). This unit gives the existing reading doctrine an answer-side trigger, twinned on the guide router's consult, plus the anti-echo re-touch rule.

## Capability Ledger (what already exists — this unit extends, never duplicates)
- `guides.md` §0 — the consult trigger for GUIDES: proportional to triage, scan-the-router-not-the-content, targeted match, **declared verdict with three legal values, never faked**. THE model to twin.
- `taxonomy.md` §1 — the descent (top-level rows of `topics/INDEX.md` → branch → every parent → synonyms → open only final candidates). Written for PLACEMENT; reusable verbatim for answering.
- `topics/INDEX.md` — generated router: slug, description, parents, synonyms.
- Claim provenance (ELICITED/DERIVED/RULING/IMPORTED) + derivation chains (F-035) — the anti-echo rule reads these, adds nothing to their format.
- SKILL.md "Map-First Navigation" value — retrieval before *creating documents*; silent on answering.

## Design

### 1. `SKILL.md` (kb): new section `## Topic Recall — the answer-side consult`, after `## Operative Guides & Router`
- **Trigger — entering a topic, never per-turn**: fires when the reply would assert facts about the PROJECT'S domain that the KB could plausibly hold (its topics, decisions, sources, constraints). Does not fire on: pure mechanics (running a command, editing per explicit instruction), general knowledge outside the project's domain, or L1 gestures. One consult per topic per conversation — not per message.
- **The act**: scan `topics/INDEX.md` and descend per `taxonomy.md` (same doctrine, answer mode — §6 there). On a match, answer FROM the claims, citing claim ids; a `status: SUPERSEDED` claim is never cited without naming its successor.
- **The declared verdict, only when the recall ran** (never a per-turn ritual): `kb: <slug> → N claims cited` / `kb: no coverage` (index read, nothing fits) / `kb: no graph` (no `topics/INDEX.md`). Never fake — an always-"no coverage" verdict certifies a lookup that did not happen (same clause as the guide router).
- **Anti-echo (the re-touch rule)**: when a DERIVED claim grounds a decision the user is about to take, re-open the source its chain points to (the `corpus/` artifact or note) and cite it beside the claim id. The trace IS the citation — no self-declaration. ELICITED/RULING claims carry the user's own authority and are exempt.
- One line added to the "Map-First Navigation" value: retrieval also before *answering from model memory* on the project's domain.

### 2. `taxonomy.md` (kb): short new section `## 6. The same descent, answer mode`
Differences only: no placement verdicts, no writes, the descent stops at reading claims; coverage (found / not found) replaces the five verdicts; UNPLACED does not exist when reading. Everything else — descend don't scan, every parent, synonyms — applies unchanged.

### 3. Eval scenario (kb only): `evals/scenarios/recall_descends_before_answering.md`
Setup: a small `topics/` tree + claims (one DERIVED with a chain to a corpus note, one SUPERSEDED). Prompt: a cold question the KB covers. Pass: the agent descends and cites claim ids (not model memory); the SUPERSEDED claim is not cited bare; the decision-grounding DERIVED gets its source re-touched and cited.

### 4. Battery (kb `test_skill_invariants.py`): new invariant
Whitespace-normalized anchors on SKILL.md (section present; the three verdict forms; "never fake"; the re-touch rule) and on taxonomy.md (answer-mode section present). Mutation check both ways: removing the section reddens the test.

### 5. Carriers
kb `README.md` and SKILL.md's support-files list: taxonomy.md's description line gains "and the answer-mode descent".

## Impact
| File | Change |
|---|---|
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | new section + one value line |
| `.../taxonomy.md` | new §6 |
| `.../scripts/test_skill_invariants.py` | new invariant |
| `.../evals/scenarios/recall_descends_before_answering.md` | new |
| `distributions/kb-agentic-skill/README.md` | taxonomy description line |
| `distributions/kb-agentic-skill/CHANGELOG.md` | [Unreleased] entry |

All kb-lens files — `review.md`, `dispatch.md`, `templates.md`, `sdlc_core.py` untouched, so the drift guard (x3 manifest) is not involved. Code lens and mkt lens unaffected: recall over a topic graph is kb-only doctrine.

## Security and Threat Model
- **T1 noise** — a recall that fires per-turn is the vision's named failure #1. Mitigation: the entering-a-topic criterion, the L1/mechanics exemptions, once-per-topic-per-conversation, and the verdict appearing only when the recall ran.
- **T2 faked verdict** — the guide router's T7, same countermeasure inherited: three legal values, never-fake clause, declared only-when-run.
- **T3 stale installed copies** — machines running old home copies (the 1.4.1 found today) never see this doctrine. Out of scope here; named for the family-level update-notification candidate.
- No security surface: doctrine-only change, no code paths, no credentials, no network.

## Test Strategy
Battery RED→GREEN on the new invariant; mutation bites both ways; eval scenario runnable by `evals/run_behavioral.py`; `check --hybrid` CLEAN at closure; kb battery fully green.

## Action Plan
1. SKILL.md section + value line; taxonomy.md §6.
2. Invariant (RED first), then confirm GREEN; mutation check.
3. Eval scenario.
4. README + CHANGELOG carriers.
5. Closure: battery x1 (kb), check --hybrid, REVIEW_LOG, handoff.

## Diary
- 2026-08-27: unit opened on `feat/kb-recall-reflex` off main@45ad7c3 (vision APPROVED same day). Design modeled on `guides.md` §0 after reading it whole; anchors verified against the 1.6.0 tree (the session's loaded copy was 1.4.1 — home copy updated during the vision phase, a live instance of risk T3). Schema conformance pass: a PowerShell in-place patch mojibake'd the UTF-8; rewritten clean via Write — string patches on UTF-8 files go through Python or Write, never Set-Content.
