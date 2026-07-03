# Handoff
Date: 2026-07-03 (UTC)
Branch: main
Agent: Claude (Opus, orchestrator) — same-session implementation (no subagent dispatch); all reviews via independent fresh-context subagents

## State: M4 built, NOT yet released
**M4 — Consolidation & Proactive Activation**: all 4 units DONE + closure governance done. The release (version bump + publish) is the remaining step — see "Next" below. Master Plan: M1/M2/M3/M4 all units DONE; M4.A6 (Release & closure) in PROGRESS (closure artifacts done, release pending).

## What was built (M4)
- **Unit 1 — SessionStart hook**: `sdlc_check.py orient` subcommand (reuses confine_under/read_text/find_project_root). Emits bounded repo-sourced orientation (README+INDEX+guide-router+handoff+triage) at session start. Zero-execution (T1), fail-OPEN (T8), size-capped (T2). Manual per-client wiring (ENFORCEMENT §4); `--hybrid` → devPNT-bootstrap pointer. `test_session_start.py` 9 tests.
- **Unit 2 — Guide consumption**: closes the write-only guide gap (Layer D). Consult trigger (before L2/L3 work, targeted router match, L1 exempt) + proactive-creation trigger (propose after user-indication reusable work). Mechanics in guides.md §0/§1; hooked from SKILL.md Operative Guides + Phase 4/5; dispatch.md note (consult at plan-authoring, subagent reads handed pointers).
- **Unit 3 — Worktree hygiene**: SKILL.md Phase 4 (isolate L3 on a branch; Hybrid → worktree, .db lock) + Phase 5 (merge decision + cleanup). Light path (2 bullets, review skipped by scope — recorded in REVIEW_LOG).
- **Unit 4 — Eval harness**: `test_skill_invariants.py` = deterministic static release gate (asserts all M4 doctrine anchors, support-pointers resolve, indexes idempotent-no-write, driver-no-llm). Behavioral corpus `evals/scenarios/` + opt-in `run_behavioral.py` (non-CI, never gates). All dev-only. Battery = `python -m unittest discover -s scripts -p "test_*.py"` = **51 tests green** (plan 32 + orient 9 + skill-invariants 10). ADR 2026-07-03 skill_eval_harness.

## Governance
Full chain per unit: M-VISION v2.1 (revised this session: DRAFT→APPROVED, added the guide-consumption unit) → D-UC + P-TM (milestone-wide, 10 threats) → per-unit E-ISP (deep review) + E-TDD (light review) → implement → §4.6 code review. REVIEW_LOG has all M4 rows. KL updated: architecture v1.4, principles v1.2 (Self-activation principle). ADR proposed. The independent-review gate caught real defects at design time: incomplete eval invariant set, the M3↔M4 dispatch interaction, the REPO parents off-by-one, P-TM overclaim of unbuilt guards.

## Next step — the release (M4.A6 part B)
Version **1.11.0** (minor — M4 features). Per `ai_docs/reference/GUIDE_release.md`:
1. **GUIDE_release update (deferred from Unit 4)**: add the eval battery (`unittest discover`) to the verification battery — this is guide-maintenance (re-snapshot `reference/.sources/release-runbook-*.md` + regenerate + new source_hash). Do this as part of the release.
2. Bump 3 places: package.json + gemini-extension.json + CHANGELOG (`[Unreleased - 1.11.0]` → `[1.11.0] - date`). NB: no new SHIPPED files this milestone (eval harness is dev-only) — nothing new for the package.json `files` allowlist.
3. Verification battery: npm pack --dry-run --json (evals/ + test_*.py must NOT ship — confirm they're excluded), init.js smoke, `check --hybrid` CLEAN, **the eval battery green**.
4. `git_push_tag.bat` → verify tag == HEAD → merge main → `npm publish` (USER, 2FA).
5. Update this handoff post-release; the KL/ADR/principles proposals must be ACCEPTED before/at release.

## Fable review findings carried (partly open)
Fable's Vision review (2026-07-03) — see memory `m4-fable-review-findings`:
- **#1 "demonstrably"** — CLOSED: defined in the eval E-ISP/ADR as a runnable seeded scenario (`consult_fires_on_match`) + static presence assertion.
- **#2 Layer-D honesty** — at closure, features_history / this handoff should state Layer D's success signal is delivered by **M1 + M4 jointly** (M1 built the guide-creation machinery; M4 made guides govern the work), not M1 alone.
- **#3 Adherence residual** — the consult trigger firing is prose-dependent forever (a model can ignore SKILL.md); "mechanical over prose" tops out below it (client-side enforcement = a lock-in Non-Goal). U1 mitigates (router in context), U4 samples it (behavioral scenarios), nothing gates it. Accepted residual — state it as such.

## Carried debt / ops
- **Not M4**: `ai_docs/functional/{architecture_overview,external_interfaces}.md` still lack lifecycle `status:` frontmatter (devPNT-regenerated, stripped headers) → 2 non-fatal `validate` warnings (check stays CLEAN). Restore at a devPNT functional-docs pass.
- roadmap/principles (`ai_docs/vision/`) still DRAFT.
- Working tree holds all M4 code + docs UNcommitted (no commit made this session — user's call). devPNT server locks `.devpnt/*.db`: commit on current branch is fine; branch-crossing needs a worktree or server restart (GUIDE_release trap).
