# Handoff
Date: 2026-07-27 (UTC)
Branch: feat/guide-activation
Agent: Claude (orchestrator) — Standalone (devPNT off)

## State: v1.16.0 released from this branch (commit + tag), npm publish pending

Three features, one release:
1. **F-016 Guide Activation** — Rule Zero declares the router verdict with the triage
   level (L2/L3/Spike; L1 exempt); guide router in Phase 1 mandatory reads; `orient`
   hook recommended default + wired here; `source_kind: code` trigger phase `any` → `4/5`
   with Phase-5 Comprehension checkpoint. ADR:
   `architecture/ADR_2026-07-27_declared_router_verdict.md`.
2. **F-017 Vision Clarity** — six blind rounds (no repo access) took the Vision from
   undecidable (metering admissible on literal text — the M89 hole) to **v6 APPROVED**.
   Evidence + standing battery (21 fixtures): `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`.
3. **F-018 Verifiable Vision** — new skill file `vision.md`, anchored by the owner's
   definition: *the benefit to be obtained, leaving the most degrees of freedom
   possible — binds nothing that does not obstruct it*. Deletion test decides WHICH
   rules exist; nine properties decide HOW to write one that holds. Wired from Vision
   Gate, Write Triggers, template, `elicitation.md`; in the package allowlist.

Battery **57/57**, `check --hybrid` CLEAN, `validate` 0 errors / 4 baseline warnings.
`review.md` threat-model bullet merged (duplication removed, design-review rationale kept).

## Pending owner
1. **Merge to main** — GitHub web PR (no `gh` on this machine) or authorized direct push.
2. **`npm publish`** (2FA/EOTP) from a clean checkout. Verify:
   `npm view @antoneeo/agentic-sdlc-skill version` → 1.16.0.
   `npm pack --dry-run` re-check: `vision.md` in, eval harness (`test_*.py`, `evals/`) out.

## Next step
F-018's success signal is unproven until a Vision drafted from scratch under `vision.md`
survives its first blind round with judgement findings only. On any future Vision edit,
re-run the standing battery (end of round-6 section in the review evidence) — the re-run
is the ratchet.

## Session notes
Repo is CRLF; edits applied as content-delta. `scripts/` audit area re-analyzed in a
parallel session (installer roster documented in `strategic/architecture.md`).
