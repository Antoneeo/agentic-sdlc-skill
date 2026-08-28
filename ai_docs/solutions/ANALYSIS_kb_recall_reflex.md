---
description: F-039 unit 1 of VISION_kb_second_brain - the topic-recall reflex and the anti-echo rule in the kb lens. The reading doctrine exists (taxonomy descent); this unit gives it the answer-side trigger the guide router already has, plus a by-construction limb in the kb orient.
status: COMPLETED
end_date: 2026-08-28
feature: F-039
id: F-039
start_date: 2026-08-27
level: L3
branch: feat/kb-recall-reflex
---
# ANALYSIS: KB Recall Reflex (second-brain unit 1)

**Level: L3 · router: no match** (monorepo `reference/INDEX.md` carries only `GUIDE_release.md`, not applicable).

## Feature Vision
`VISION_kb_second_brain.md`, APPROVED 2026-08-27 — unit 1 of its sequence; unit 3 explicitly waits for the data units 1-2 generate.

## Objective
The descent fires only inside a kb unit of work (placing claims). Nothing triggers it when the agent ANSWERS a question that rests on project-domain knowledge — recall is left to model memory, the mechanism proven not to fire. This unit gives the existing reading doctrine an answer-side trigger twinned on the guide router's consult, an anti-echo re-touch rule, and one by-construction limb: the kb orient surfaces the topic router at session start.

## Capability Ledger (what already exists — this unit extends, never duplicates)
- `guides.md` §0 — the consult trigger for GUIDES: unconditional scan at L2/L3, scan-the-router-not-the-content, targeted match, declared verdict with named legal values, never faked, "regenerate when you report absent". THE model to twin.
- `taxonomy.md` §1 — the descent (top rows of `topics/INDEX.md` → branch → every parent → synonyms → open only final candidates). Written for PLACEMENT; reusable for answering. §1's batch paragraph also states mid-run truth: the FILES are the state; `topics/INDEX.md` is written at closure, so nodes routinely exist while the index lags.
- Claim provenance — **five values**: `GIVEN | ELICITED | DERIVED | RULING | IMPORTED` (`distillation.md` §claim-table), with the IMPORTED rule: foreign authority, "may not supersede a local row until re-ratified".
- Derivation chains (F-035): `derived_from:` may point at other notes — derived-on-derived is legal, so a chain's immediate target is NOT necessarily ground.
- kb overlay dispatch (`sdlc_check.py`): intercepted commands run overlay logic, everything else forwards to the spine — the pattern that lets `orient` gain kb behavior without touching `sdlc_core.py`.
- SKILL.md "Map-First Navigation" value — retrieval before *creating documents*; silent on answering.

## Design

### 1. `SKILL.md` (kb): new section `## Topic Recall — the answer-side consult`, after `## Operative Guides & Router`
- **Trigger — unconditional scan on domain assertions**: whenever the reply would assert facts about the PROJECT'S domain (its topics, decisions, sources, constraints), scan `topics/INDEX.md`. Plausibility of coverage is judged ON the scanned top rows, never before them — "the KB probably doesn't have this" is model memory talking, the exact judgement this reflex removes. Exempt: pure mechanics (running a command, editing per explicit instruction), general knowledge outside the project's domain, L1 gestures.
- **Dedup — once per topic per SESSION**: the key is the matched slug (known ex post); a question plainly within an already-descended branch reuses that consult, and a placement descent already run this session counts. Session vocabulary, aligned with SessionStart/session-end; a compaction starts a new session.
- **The act**: descend per `taxonomy.md` §6 (same doctrine, answer mode). On claims, answer FROM them citing claim ids; a claim whose `state` is `SUPERSEDED <id>` is never cited without naming its successor.
- **The declared verdict, only when the recall ran** (never a per-turn ritual) — four legal values:
  - `kb: <slug> → N claims cited`
  - `kb: <slug> → node matched, no claims` — surfacing the node's `gaps:` when it answers the question: "the KB knows it doesn't know" is a first-class answer.
  - `kb: no coverage` — index read, nothing fits.
  - `kb: index absent — regenerate (sdlc_check.py index)` — the INDEX is missing, not necessarily the graph (nodes routinely exist while the index lags, `taxonomy.md`); regenerate and rescan, mirror of the guide router's absent-verdict instruction.
  Never fake — an always-"no coverage" verdict certifies a lookup that did not happen (guide router's clause, re-instantiated for this namespace). The `router:` and `kb:` verdicts are independent and may co-occur, one line each — a how-to question can legitimately match a guide AND carry claims.
- **Anti-echo (the re-touch rule)**: when a DERIVED claim grounds a decision the user is about to take, walk its chain to non-DERIVED ground — a GIVEN artifact, an ELICITED or RULING note — and cite that ground beside the claim id; re-opening only the immediate target may re-read the agent's own synthesis, which is the echo chamber itself. If the ground does not resolve (imported bundle without originals, external `original_path:`, tombstone): say so beside the claim id and treat the claim as **unverified for decision-grounding** — surfaced, never silently cited. Per-provenance stance: GIVEN's source column is already the direct citation; ELICITED/RULING carry the practitioner's own authority (exempt); an IMPORTED claim grounding a decision is named as un-re-ratified foreign authority.
- **Persistence of the trace (vision signal 5)**: when the decision is recorded (a ruling note, a diary entry), that record cites the claim id AND the re-touched ground — the trace survives in the corpus, not in ephemeral chat.
- **Under dispatch**: recall is an orchestrator concern — the orchestrator runs the descent itself and a context-free subagent never runs its own (mirror of the guide consult's dispatch clause). Vehicle: the task schema has no claims field today, so until a dispatch-focused unit adds one, the orchestrator inlines the cited claim rows in the task's free text — an explicit interim, not a silent gap.
- One line added to the "Map-First Navigation" value: retrieval also before *answering from model memory* on the project's domain.
- **Frontmatter `description`** gains the answering surface ("...and answering project questions from the claim ledger") — vision signal 1 is a cold question session; if the skill never loads for a pure question, the doctrine is not in context when its case arrives.

### 2. `taxonomy.md` (kb): short new section `## 6. The same descent, answer mode`
Differences only: no placement verdicts, no writes, the descent stops at reading claims; coverage replaces the five verdicts; UNPLACED does not exist when reading. Everything else — descend don't scan, every parent, synonyms, tombstone redirects — applies unchanged.

### 3. By-construction limb: kb `orient` surfaces the topic router
`sdlc_check.py` (kb overlay) intercepts `orient` as a special case BEFORE its own argparse (the `--help` pattern): pass the raw argv to `sdlc_core.main` untouched — never re-parse or hand-mirror orient's flags, the exact drift class the file warns about — capture the return code, THEN append a `## Topic router` section — the top rows of `topics/INDEX.md` when present, `index absent (N node files) — regenerate` when nodes exist unindexed, nothing when the project has no graph. Recall per costruzione (vision constraint): every session opens with the graph in sight, so the reflex has its map before the first question. Spine untouched — overlay interception only.

### 4. Eval scenario (kb only): `evals/scenarios/recall_descends_before_answering.md`
Setup: small `topics/` tree + claims — one DERIVED with a two-hop chain (note → note → GIVEN artifact), one SUPERSEDED. Prompt: a cold question the KB covers, framed as grounding a decision. Pass: descent + claim ids cited; SUPERSEDED not cited bare; the DERIVED's chain walked to GROUND (not the intermediate note) and cited. **Harness prerequisite**: `run_behavioral.py` `seed()` today writes one line per file; it gains fenced-block multi-line seeding (kb-only file, in Impact).

### 5. Battery: new kb-only test module `test_kb_recall.py`
One NEW file, picked up by the battery's discover, carrying BOTH the doctrine invariant (whitespace-normalized anchors on SKILL.md — section present, the four verdict forms, "never fake", chain-to-ground, the unresolvable-ground branch — and taxonomy.md §6) AND the orient-interception test (topic router appended when INDEX exists / node-count line when unindexed). Mutation bites both ways. NOT in `test_skill_invariants.py`: that file is shared-manifest (x3, drift-guarded) — kb-only doctrine takes a kb-only vehicle, which is what keeps the Impact's isolation claim true.

### 6. Carriers
kb `README.md`: the capability narrative ("What it does") gains answer-side recall — the milestone's headline, not a per-file description line. kb SKILL.md support-files list: taxonomy row gains "and the answer-mode descent". CHANGELOG `[Unreleased]`.

## Impact
| File | Change |
|---|---|
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | new section, value line, frontmatter description |
| `.../taxonomy.md` | new §6 |
| `.../scripts/sdlc_check.py` | `orient` interception: topic-router section |
| `.../scripts/test_kb_recall.py` | NEW kb-only module: doctrine invariant + orient test |
| `.../evals/run_behavioral.py` | multi-line (fenced-block) seeding |
| `.../evals/scenarios/recall_descends_before_answering.md` | new |
| `distributions/kb-agentic-skill/README.md` | capability narrative |
| `distributions/kb-agentic-skill/CHANGELOG.md` | [Unreleased] entry |

All kb-lens files — `review.md`, `dispatch.md`, `templates.md`, `sdlc_core.py` untouched: the drift guard (x3 manifest) is not involved (verified: orient gain lives in the overlay entry point, which is kb-only). Code and mkt lenses unaffected.

## Security and Threat Model
- **T1 noise** — per-turn firing is the vision's named failure #1. Mitigations: domain-assertion criterion with named exemptions, once-per-topic-per-session, verdict only when the recall ran, orient limb runs once per session.
- **T2 faked verdict** — the guide router's T7, countermeasures inherited: four legal values (every real state has an honest one, including the lagging index), never-fake clause, regenerate instruction.
- **T3 stale installed copies** — old home copies never see this doctrine (the 1.4.1 found live). Out of scope; named for the family update-notification candidate.
- **T4 echo via intermediate notes** — countered by chain-to-ground; the unresolvable-ground branch keeps the honest output available at the highest-stakes moment (a required act with no truthful value gets faked or dropped).
- No security surface: no credentials, no network; the only code path is read-only orient output.

## Test Strategy
Battery RED→GREEN on the new invariant; mutation bites both ways; orient interception unit-tested (kb-only); eval scenario runnable after the harness gains multi-line seeding; `check --hybrid` CLEAN at closure; kb battery fully green.

## Action Plan
1. SKILL.md section + value line + description; taxonomy.md §6.
2. `orient` interception in the kb overlay + its test.
3. Invariant (RED first) → GREEN; mutation check.
4. `run_behavioral.py` multi-line seeding; eval scenario.
5. README + CHANGELOG carriers.
6. Closure: kb battery, check --hybrid, REVIEW_LOG, handoff.

## Diary
- 2026-08-28 (closure PASS): round 3 PASS, zero open findings — the residue was exactly
  the one cell disclosed as unverified (locator form), ruled by the reviewer against the
  validator's own grammar and fixed as three deterministic cells. Full arc: design
  FAIL(12)→FAIL(1)→PASS, closure FAIL(8)→FAIL(1)→PASS, 25 verified findings across six
  rounds, both reviews rung 1 with the F-038 ask at each gate. Unit DONE, awaiting merge.
- 2026-08-28 (closure R2): closure review round 1 FAIL — 1 BLOCK + 7 WARN, all real. The
  BLOCK was this unit's own disease in its own fixture: the eval scenario's claim table
  was written from model memory (4 columns, supersession in the wrong column) instead of
  the canonical 8-column `## Claims` schema with `state = SUPERSEDED <id>` —
  templates.md:621 read this time, scenario reseeded canonical with the two-hop chain
  grounding in a GIVEN artifact and every source seeded. Also folded: claim-state
  vocabulary fixed in SKILL.md (`state`, not `status:`); probe SystemExit + AmbiguousDocsRoot
  fallback in kb_cmd_orient; the forward itself now anchored by an ORIENT_MARKER assert
  (a mutation deleting the spine call reddens); five more doctrine anchors (dispatch
  interim, trace persistence, superseded-successor, co-occurrence, exemptions); fence-hunt
  fails fast on a forgotten fence. Recall tests 7/7, battery 281 OK.
- 2026-08-28 (closure): implemented per the PASS design, in plan order. test_kb_recall.py 7/7 with the mutation verified RED->GREEN on a doctrine anchor; kb battery 281 OK; the eval harness smoke found one real defect (fence bodies carried the bullet indentation and broke YAML frontmatter — common-dedent added, re-smoked clean). REVIEW_LOG row written; handoff registered DONE, AWAITING MERGE.
- 2026-08-27: unit opened on `feat/kb-recall-reflex` off main@45ad7c3 (vision APPROVED same day). Design modeled on `guides.md` §0 read whole; anchors verified against the 1.6.0 tree (the session's loaded copy was 1.4.1 — home copy updated during the vision phase, a live instance of T3). Schema pass: a PowerShell in-place patch mojibake'd the UTF-8; rewritten via Write — string patches on UTF-8 files go through Python or Write, never Set-Content.
- 2026-08-28 (R3): round 2 FAIL, narrow — 11/12 resolved, one new BLOCK the reviewer flagged as latent since round 1: `test_skill_invariants.py` is shared-manifest (x3), so the battery row contradicted the isolation claim. Folded: the invariant moves to a NEW kb-only `test_kb_recall.py` (with the orient test); the interception shape is pinned (special-case before argparse, raw argv, never re-parse flags); the dispatch vehicle is an explicit interim (claims inlined in task free text until a dispatch unit adds a schema field); the §0→§1 pointer fixed.
- 2026-08-28: design review round 1 (fresh subagent, rung 1 granted at the gate): FAIL, 6 BLOCK + 6 WARN, all verified real (provenance is five values with GIVEN — distillation.md:118 checked; orient lives in the spine but the overlay intercept pattern permits a kb-only limb — sdlc_check.py:1521-1532 checked). All 12 folded into this revision: unconditional scan (plausibility judged ON the index), four-verdict vocabulary with index-absent semantics + regenerate, chain-to-ground + unresolvable-ground branch, by-construction orient limb, harness multi-line seeding, five-value ledger with per-provenance stance, session dedup, dispatch clause, verdict composition, trace persistence, capability-narrative carrier + description surface.
