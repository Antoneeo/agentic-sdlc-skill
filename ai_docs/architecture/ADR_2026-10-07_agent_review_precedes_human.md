---
description: ADR - devPNT performs no review; in both modes the agent review is review.md, carried to the reviewer by a verbatim REVIEW MANDATE block, and in Hybrid its PASS precedes every proposal to devPNT, where the human reviews. Rejected - "run ONE of them, never both", a paraphrased mandate, and a strict no-escape block after the round cap.
status: CURRENT
---
# ADR: the agent review precedes the human's, and the mandate travels whole

**Status:** Accepted
**Date:** 2026-10-07
**Task ref:** F-065 (ANALYSIS_review_mandate_contract.md)
**Digest:** F-065 — a Hybrid E-ISP (devPNT M52 v1.1) passed an agent review whose prompt carried devPNT's checklist but not `review.md`, so the mandatory Functional Spec was never checked; the skill itself said devPNT's gate "owns the slot" ("run ONE of them, never both"). Decision: devPNT performs no review — it hosts artifacts and is the human's review surface; every agent review, both modes, runs under `review.md`, opened by a verbatim REVIEW MANDATE block; in Hybrid a logged PASS precedes every proposal, and after the round cap only the user's explicit decision sends an artifact on, findings attached. Replay: paraphrase 0/2 flagged the gap, block 4/4. Rejected: alternative review slots, free-form requests, a strict block with no user escape. Residual: an author can still omit the block; devPNT doctrine and reviewer definitions do not yet cite `review.md`.

## Context

`hybrid.md`'s ownership matrix gave the design review two owners: `review.md` on the ANALYSIS in Standalone, "devPNT §4.5 gate" on the `E-ISP`/`E-TDD` in Hybrid, "run ONE of them, never both". `review.md` itself named devPNT's gates as consumers; `dispatch.md` had per-task review "reuse the devPNT code-review gate". devPNT, however, has no review agent: its doctrine instructs the client to run reviewers, and the reviewer definitions it ships carry their own checklists without `review.md`. In practice a Hybrid agent built a prompt from devPNT's checklist, the reviewer never saw `review.md`, and clauses that live only there (Functional Spec, probes, Component Map) never ran. The M52 v1.1 E-ISP passed with no Functional Spec.

Replay on that artifact (`ai_docs/solutions/harness_review_mandate/`): the same model, given a §4.5-style prompt, flagged the missing section 0 times in 2; given the REVIEW MANDATE block, 4 times in 4 (once only as a warning, because the Hybrid home of the section was stated in `SKILL.md`, not in `review.md`).

## Decision

1. devPNT performs no review. It hosts governed artifacts and is where the human reviews and approves them.
2. Every agent review, Standalone or Hybrid, runs under `review.md`. Where a client follows devPNT doctrine §4.5/§4.6, that invocation is this review: one review, one REVIEW_LOG row.
3. Every request opens with the REVIEW MANDATE block copied verbatim; only fields vary, and nothing after it can narrow it. §Requesting lists every input a §Reviewing clause checks, and each clause states its Hybrid locations itself.
4. In Hybrid, no governed artifact is proposed to devPNT before an agent review of it has a final PASS, cited in the proposal. After the round cap with findings standing, the artifact returns to the user; only the user's explicit decision sends it on, with the open findings attached (owner ruling, 2026-10-07).
5. The `hybrid.md` conservation digests (code and marketing lens) were re-stamped for this amendment, after verifying that each pre-edit block matched its previous digest and that the diff touched only the declared rows (owner ruling, 2026-10-07; method per `ADR_2026-09-11_conservation_reference.md`).

## Alternatives considered

- **Keep "run ONE, never both"** — rejected: it presents the human surface as a review slot and lets the agent review be replaced by a checklist the mandate never reaches.
- **List the inputs, leave the request free-form** — rejected: the list already existed; the failure was that the reviewer never received the mandate.
- **No escape after the round cap** — rejected by the owner: a gate that can block forever gets removed; the user's explicit, recorded decision keeps the rule that no agent proposes on FAIL.
- **Move the review rows out of the hashed block** — rejected by the owner: it splits the ownership matrix, and the old row has to leave the block anyway.

## Consequences

- **Pro:** one review definition in both modes; the reviewer receives the whole mandate; the human in devPNT sees which review each proposal passed.
- **Con / risk:** the block adds a fixed form at L2/L3, replacing the free-form request at comparable cost. An author can still omit it: the invariants guard the doctrine, not each session.
- **Residual:** devPNT doctrine §4.5/§4.6 and its client reviewer definitions do not cite `review.md` yet; that is devPNT-side work.
