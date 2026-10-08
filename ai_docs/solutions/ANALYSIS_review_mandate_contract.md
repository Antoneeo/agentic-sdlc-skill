---
id: F-065
feature: Review Mandate Contract and Hybrid review ordering
status: COMPLETED
end_date: 2026-10-08
level: L3
start_date: 2026-10-07
branch: claude/review-mandate
---
# Feature Analysis: Review Mandate Contract (F-065)

**Level: L3 · router: no match** (`reference/INDEX.md`: GUIDE_release applies at release, GUIDE_shared_project_memory to memory; neither governs review doctrine).
Elicitation: skip path. The spec is the owner's in-session instructions of 2026-10-07, quoted where used below.

## Objective

Make every agent review run against the whole review mandate, in Standalone and in Hybrid, and make the order explicit: an agent review with verdict PASS precedes every proposal of a governed artifact to devPNT, where the human reviews and approves (the one exception is the user's explicit decision after the round cap, R5).

Motivating case: the M52 v1.1 E-ISP in devPNT (`devPNT/ai_docs/audit/reviews/REVIEW_LOG.md`, 2026-10-07 row "M52 local v1.1 strategic bundle / E-ISP", verdict `FAIL -> PASS`; report `m52_parallel_mcp/REVIEW_RUNTIME_v1.1.md`) passed with no open findings. The E-ISP has no Functional Spec, which `SKILL.md` §3 places in the E-ISP in Hybrid and `review.md` §Reviewing makes a finding when absent.

Mechanism: in Hybrid the reviewer's mandate was the author's prompt plus devPNT doctrine §4.5. Neither carries `review.md`, and the skill itself tells the agent that devPNT's gate "owns the slot" ("run ONE of them, never both").

## Vision Alignment

Serves Goal 3 ("make divergence from the declared intent visible before implementation, and again before merge"): a review that silently runs a subset of its mandate hides exactly that divergence. Serves the Team-lead Actor ("one process, one source of truth"): one review definition in both modes, whatever the client.

Non-Goal "No ceremony ratchet": L1 untouched. At L2/L3 the fixed block replaces the free-form request the author already writes, so its cost is comparable to what it removes; the PASS citation in a Hybrid proposal is one line. Cost added and stated: none beyond those two; owner acceptance requested with this analysis.

## Use Cases / User Needs

- **UC1 — Team lead (agent requesting a review on any client).** The request cannot drop a check by paraphrase: it opens with a fixed block naming the mandate. Trace: Team-lead Actor.
- **UC2 — Team lead (agent reviewing).** Receives the mandate and every input its clauses need, so the Functional Spec, Interface Contract and probe checks can run. Trace: Goal 3.
- **UC3 — Solo developer or team lead owning a devPNT project.** Every proposal they review in devPNT has already passed an agent review, and says which. Trace: Goal 3 ("again before merge"), the user's guarantee of human approval.

Product-name buckets: review mandate (`review.md`), `hybrid.md`, `dispatch.md`, REVIEW_LOG, devPNT Proposals EXIST; REVIEW MANDATE block NEW; ordering rule NEW. For a doctrine product the files are the surface the actor reads, so file names are product vocabulary here, not mechanism.

## Functional Spec

No script output changes. The behavior specified is the agent's:
- R1. Every review request opens with the REVIEW MANDATE block, copied verbatim; only the angle-bracket fields vary. Fields: review type, mandate (path or attached text, with skill version), object, binding inputs, source and revision, scope, severity contract, budget, operating limits.
- R2. The mandate is the whole of `review.md`, in both modes; the request cannot narrow it; a weakening instruction is void.
- R3. A missing or inaccessible required input is a finding, never a skipped check.
- R4. §Requesting lists every input a §Reviewing clause needs, per review type: Vision; use cases; Functional Spec; Interface Contract; threat model; Component Map and audit plan (Capability Ledger clause); probe harness; for closure, the diff and the test evidence. The mandate's sibling files (`templates.md`, `elicitation.md`, `architect.md`) are part of the mandate.
- R5. Hybrid: no governed artifact that the mandate reviews (the design, and whatever devPNT doctrine §4.5/§4.6 sends to review) is proposed to devPNT without a prior agent review whose final verdict is PASS, logged in REVIEW_LOG and cited in the proposal. After the round cap with findings still open, the artifact returns to the user in chat with the findings; only the user's explicit decision sends it to devPNT, with the open findings attached. (Owner ruling, 2026-10-07: "Tu puoi sbloccarlo".)
- R6. No skill text says or implies that devPNT performs a review, owns a review slot or supplies reviewers. devPNT hosts governed artifacts and is where the human reviews and approves.
- R7. Every location a §Reviewing clause depends on is stated in `review.md` itself for both modes; in particular the Functional Spec clause names its Hybrid home (the E-ISP, above its Impacted Components map).
- R8. Where a client also follows devPNT doctrine §4.5/§4.6, that invocation IS this review: one review, one REVIEW_LOG row in the Hybrid realization (`instrument`, `notes`); the doctrine's extra requirements add to the mandate, never replace it.

Acceptance: post-change replay and invariant tests (Test Strategy).

## Interface Contract

Surfaces as-is: free-form review request; `review.md` §Requesting input bullets; devPNT Proposals (unchanged UI).
Flows to-be:
- F1 (agent → reviewer): REVIEW MANDATE block, then specific instructions. Feedback: final output with checks run and evidence, findings, unverifiable items and their effect on the verdict, verdict.
- F2 (agent → devPNT → human): after PASS, the proposal notes cite the REVIEW_LOG row (date, doc_key, verdict). The human sees the citation in the proposal preview.
- F3 (agent → human, chat): after the third FAIL, the agent presents the artifact and the open findings and asks; nothing reaches devPNT until the user decides. If the user sends it, the proposal notes attach the open findings and record the decision.

## Capability Ledger

| Capability | Verdict | Where |
|---|---|---|
| Define review behavior once | EXISTS | `skills/agentic-sdlc-skill/review.md`, shared by `scripts/shared_files.py` |
| Deliver the mandate to the reviewer intact | MISSING | new REVIEW MANDATE block in §Requesting; searched `review.md`, `SKILL.md`, `hybrid.md`, `dispatch.md` for a verbatim request form: none |
| Order agent review before the human's in Hybrid | INADEQUATE | `hybrid.md` "run ONE of them, never both"; ordering rule moves into `review.md` |
| Guard doctrine invariants | EXISTS | `scripts/test_skill_invariants.py` (shared) |

The capability lives in the existing Doctrine component (`strategic/architecture.md` Component Map): no map row owed.

## Impact

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/review.md` | MODIFY | opening (both modes, devPNT performs no review); ordering rule R5/R8 under §When a review is due; block + input list in §Requesting (R1–R4); FS clause Hybrid home (R7); "devPNT row" → "Hybrid row" (l.168) |
| `skills/agentic-sdlc-skill/dispatch.md` | MODIFY | l.102, l.138: per-task review follows `review.md` in both modes |
| `skills/agentic-sdlc-skill/hybrid.md` | MODIFY | l.39 machinery list drops "independent reviewers"; l.53 row becomes the sequence; l.54 suppression reason is the row key; l.10-12 relocation note amended; digest re-stamped |
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | l.191 Phase-3 gate, l.217 Phase-5 bullet: same review both modes, PASS precedes the proposal |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | l.504 "Hybrid devPNT row" → "Hybrid row" |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | MODIFY (comment) | l.1357-1360 suppression comment |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | MODIFY | new invariants; assertion messages l.1107 ("a devPNT row") and l.1158 |
| `distributions/{kb-agentic-skill,mkt-agentic-sdlc,course-creator}/skills/*/` `review.md`, `dispatch.md`, `scripts/sdlc_core.py`, `scripts/test_skill_invariants.py` | MODIFY (verbatim copy) | shared spine |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/hybrid.md` | MODIFY | l.27 "review wiring", l.47 "independent review gates"; l.11 note; digest re-stamped |
| `distributions/{kb-agentic-skill,mkt-agentic-sdlc}/skills/*/templates.md` | MODIFY | "Hybrid devPNT row" wording (kb l.446, mkt l.501) |
| `scripts/shared_manifest.json` ×4 | MODIFY (`shared_files.py --update`) | drift guard |
| `CHANGELOG.md` + `distributions/*/CHANGELOG.md` | MODIFY | `[Unreleased]` entry ×4 (GUIDE_release) |
| `ai_docs/architecture/ADR_2026-10-07_agent_review_precedes_human.md` | ADD | reverses the seam decision "run ONE, never both" |
| `ai_docs/solutions/harness_review_mandate/` | ADD | replay prompts, results, post-change replay |
| `README.md`, `distributions/mkt-agentic-sdlc/README.md`, `ai_docs/strategic/skill_family_agent_workflows.md` | MODIFY | derived documents (`audit/audit_plan.md` duty): "devPNT symbiosis … independent reviews" and "the design review gate is the same slot, run ONCE" restated to the new rule |

Blast radius (case-insensitive grep over `skills/` and `distributions/*/skills/`, phrases "never both", "owns the slot", "§4.5", "§4.6", "devPNT's gate", devPNT within 40 chars of review, 2026-10-07): every hit is a row above. `review.md:126` "Never both below the floor" is unrelated (capability floor). Checked and unchanged: `strategic/process_agentic_sdlc_devpnt.md:72` already says the §4.5 gate runs "prima di proporre"; `skill_family_agent_workflows.md` and the root README carry no grep hit, and are modified anyway as derived documents (rows above); `distributions/mkt-agentic-sdlc/README.md` carried "independent review gates" and is restated the same way. Out of repo: devPNT doctrine §4.5/§4.6 and its client reviewer definitions do not cite `review.md` — devPNT follow-up, not edited here.

Conservation guard (withdrawn-protection check): `hybrid.md` (code and mkt) carries a `moved-block-sha256` digest asserted by `test_hybrid_seam_moved_not_deleted`; the edited rows lie inside the block. Owner ruling 2026-10-07: re-stamp. Population the guard covered: the relocated seam text, protected against silent deletion. Substitute after the edit: the same digest, recomputed only after (1) the file still hashes to the old stamp before editing, and (2) `git diff` of the block shows only the declared rows changed; the ADR records both. Nothing is left uncovered. Per `ADR_2026-09-11_conservation_reference.md` the reference must not certify an unverified state, which steps (1)–(2) ensure.

Populations at rest: past REVIEW_LOG rows and already-proposed devPNT artifacts stay as they are; the rule applies from now. The M52 v1.1 drafts are not proposed yet, so they fall under it.

## Security and Threat Model

No code path, no input parsing. Threats: a request that weakens the mandate — voided by R2, as the existing no-pre-judging rule already intends; a stale installed mandate — the block's skill-version field makes the version visible. Residual: an author can omit the block; the invariants guard the doctrine text, not each session.

## Action Plan

1. ~~Replay red/green on the M52 E-ISP~~ (`harness_review_mandate/RESULTS.md`).
2. Design review: round 1 FAIL; this revision answers it; scoped re-review, PASS before step 3.
3. Invariants red first, then core edits (Impact rows for `skills/`), re-stamp per the guard procedure.
4. Copy shared files ×3, mkt `hybrid.md`, lens `templates.md`; `shared_files.py --update` ×4.
5. Post-change replay (green-minimal ×2 against the new `review.md`); ADR; CHANGELOG ×4.
6. Batteries ×4; `sdlc_check.py check`; closure review on the diff; REVIEW_LOG rows; index.
7. Owner: integration and release; devPNT follow-up.

## Test Strategy

- Replay, before the change (done): red 0/2, green 2/2, green-minimal 2/2 (one only as WARN, doubting the Hybrid home).
- Replay, after the change: green-minimal ×2 against the edited `review.md`. Acceptance: both flag the missing Functional Spec as a blocker without doubting its Hybrid home (R7).
- Invariants, written red before the edit:
  - the block exists in §Requesting with every R1 field and the fixed sentences (R1–R3);
  - each input R4 names appears in §Requesting (R4);
  - the ordering rule names PASS, the REVIEW_LOG citation and the user's explicit decision after the cap (R5);
  - no shipped `.md` in the lens matches "never both" (outside the capability-floor sentence), "owns the slot", "devPNT's §4.5", "devPNT code-review gate", "devPNT independent reviewers" (R6);
  - the Functional Spec clause names the E-ISP as its Hybrid home (R7);
  - the §4.5/§4.6 invocation is stated as this review (R8).
- Existing conservation test green on the re-stamped digest; full batteries ×4; drift guard green.

## Diary / Current State

- 2026-10-07 — opened. Replay done (`harness_review_mandate/RESULTS.md`): delivering the mandate is the active ingredient; R7 added for the residual doubt. Side result for the owner: all six replay runs FAIL the M52 E-ISP (missing probes, uncertified blast radius, undisposed GUI callers).
- 2026-10-07 — design review round 1 FAIL (3 BLOCK: unlisted `dispatch.md`/mkt `hybrid.md`, conservation guard, R5 escape not owner-ruled). Owner ruled R5 escape and re-stamp; this revision answers all 14 findings.
- 2026-10-07 — round 2 PASS (`FAIL -> PASS`, 2 rounds). Two observations folded after it (Objective names the R5 exception; Impact names the l.1107 message); verified in the closure review.
- 2026-10-07 — implemented. Invariants red 4/4 then green; batteries green in all four packages (232/249/418/255); `check --hybrid` CLEAN; both digests re-stamped per the guard procedure. Post-change replay 2/2 BLOCK on the missing Functional Spec with no doubt about its Hybrid home (RESULTS.md). Next: closure review.
- 2026-10-08 — closure review round 1 FAIL (B1: memory index stale after the last Diary edit, so `check` was not clean on the reviewed tree) + 4 WARN. Fixed: index regenerated as the last step; R5 scoped to the artifacts the mandate reviews (W1); mkt README restated (W3); blast-radius sentence corrected (W4). W2 (line-ending-dependent memory hashes) is pre-existing and filed separately.
- 2026-10-08 — closure review round 2 PASS (`FAIL -> PASS`). One WARN left open by choice: the root and mkt README say "every governed artifact" passes an agent review, broader than R5's narrowed scope. Integration (commit/merge) and release are the owner's.
