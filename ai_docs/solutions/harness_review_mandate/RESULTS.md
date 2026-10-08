# Replay results — M52 E-ISP v1.1 (2026-10-07)

Object: `D:/SoftwareDev/devPNT/ai_docs/solutions/m52_parallel_mcp/DRAFT_E_ISP.md` (50,000 bytes, 313 lines), unchanged across runs.
Reviewer: fresh Claude subagent (general-purpose, deep tier), documents only, no source access — identical operating limits in every prompt.
Original review (REVIEW_LOG 2026-10-07, gpt-6-astra): `FAIL -> PASS` in 2 rounds, no Functional Spec finding in either.

Verbatim Functional Spec lines from each run (raw transcripts are session-local and not archived; these excerpts are copied from the returned reports):
- red A, red B: no line mentions a Functional Spec.
- green A: "B1 — BLOCK: the Functional Spec is missing."
- green B: "B1 — BLOCK: the Functional Spec is missing."
- green-minimal A: "W10 — WARN: No Functional Spec in the Hybrid set. [...] although the skill defines no Hybrid home for it."
- green-minimal B: "B1 — No `## Functional Spec`" (BLOCK).

| Variant | Prompt | Run | Verdict | Functional Spec flagged |
|---|---|---|---|---|
| red | `replay_red.md` (author prompt in devPNT §4.5 terms) | A | FAIL (2 BLOCK) | no |
| red | same | B | FAIL (2 BLOCK) | no |
| green | `replay_green.md` (REVIEW MANDATE + full input list) | A | FAIL (4 BLOCK) | yes — BLOCK B1 |
| green | same | B | FAIL (4 BLOCK) | yes — BLOCK B1 |
| green-minimal | `replay_green_minimal.md` (no Functional Spec input slot) | A | FAIL (2 BLOCK) | yes, but WARN W10: "the skill defines no Hybrid home for it" |
| green-minimal | same | B | FAIL (5 BLOCK) | yes — BLOCK B1 |

Acceptance (ANALYSIS Test Strategy): green flags it in both runs, red in neither — met.

Observations that change the design:
1. Delivering the mandate is the active ingredient: green-minimal flagged the Functional Spec 2/2 with no hint. The input slot adds reliability: without it one run doubted where the section lives in Hybrid, because that location is stated only in `SKILL.md` §3, not in `review.md`. Fix: the `review.md` Functional Spec clause states the Hybrid location itself.
2. The mandate also brought clauses the red prompt never invoked: behavioural-claim probes (green 4/4 flagged them as BLOCK), Capability Ledger vs Component Map, restated facts, revision narrative in the artifact. Red 0/2 on probes.
3. Red already FAILs on blast radius and regressions: this model is stricter than the original reviewer, so red vs original is not a pure mandate effect. The comparison that isolates the mandate is red vs green on the same model.

## After the change (F-065 `review.md`, 2026-10-07)

Prompt (`replay_post_change.md`): the new block, mandate = edited `review.md`, Binding inputs WITHOUT the Functional Spec slot (the green-minimal shape), Severity contract and Budget fields present.

| Run | Verdict | Functional Spec flagged |
|---|---|---|
| post A | FAIL (4 BLOCK) | yes — "B1 — BLOCK: no Functional Spec", states the Hybrid home from the mandate |
| post B | FAIL (3 BLOCK) | yes — "BLOCK-2: The E-ISP has no `## Functional Spec`", "In Hybrid the Functional Spec lives inside the E-ISP" |

Acceptance (R7): both flag it as a blocker with no doubt about its Hybrid home — met. Both also raised the missing Component Map / audit plan inputs as a request-side finding (R3/R4 working).
