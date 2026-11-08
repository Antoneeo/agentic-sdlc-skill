---
feature: F-093
analysis: ANALYSIS_family_hook_wiring.md
base: 7842dfa3
---
# Merge review: per-turn reminder from the kb and marketing packages

## Purpose

Installing kb-agentic or mkt-agentic-sdlc now wires the per-turn reminder their
ENFORCEMENT.md promised; before, only the code lens's installer did, so a single
non-code lens never got it. A multi-lens machine keeps one reminder line per prompt.
Serves r19's benefit (the protocol reaches every turn). Option A, approved by the
owner (REQUEST R2). Option B (a lens-aware line) is not in this branch.

## What to review

# Review map -- 18 files against 7842dfa3 (merge-base 7842dfa3535c)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +4/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/scripts/lib.js` | M | +125/-7 | REVIEW | review |
| `distributions/kb-agentic-skill/scripts/postinstall.js` | M | +13/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/scripts/preuninstall.js` | M | +7/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/scripts/test_clients.js` | M | +91/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +4/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/scripts/lib.js` | M | +125/-7 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/scripts/postinstall.js` | M | +13/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/scripts/preuninstall.js` | M | +7/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/scripts/test_clients.js` | M | +91/-0 | REVIEW | review |
| `scripts/test_clients.js` | M | +29/-0 | REVIEW | review |
| `ai_docs/solutions/ANALYSIS_family_hook_wiring.md` | A | +209/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_family_hook_wiring.md` | A | +54/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/requests/REQUEST_family_hook_wiring.md` | A | +35/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +1/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_family_hooks/probe_family_install.js` | A | +37/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/memory/INDEX.md` | M | +2/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 11 files (+509/-18); DESIGN 2 files (+263/-0); EVIDENCE 3 files (+73/-0); GENERATED 2 files (+3/-0)

The kb and marketing deltas are identical apart from names (GUIDE_skill_family_changes:
counts once). `removeGlobalOrientHooks` was refactored onto a shared prune loop; the
closure review checked it is behaviour-identical.

## What was verified, and by which gate

- Behaviour AC1–AC5 (ANALYSIS Functional Spec): `test_clients.js` F-093 tests; batteries
  green after the last edit: code 76, kb 52, marketing 52, course 4.
- Install order effects: `harness_family_hooks/probe_family_install.js` (kb-only and
  marketing-only now wired; one entry per kind in every order).
- Closure review (REVIEW_LOG 2026-11-08): 4 WARN, 0 BLOCK; three fixed, two named as
  residuals in the ANALYSIS.
- No design-review round: the owner approved the option from the ANALYSIS directly.

## What only a human can judge

- The two residuals (dead family entry blocks wiring; uninstalling the owning lens leaves
  survivors unwired) are accepted as family-wide behaviour for now.
- course-creator still does not wire its reminder: its ENFORCEMENT.md does not promise it.
- Merge target and release timing: the CHANGELOG entries sit under Unreleased.
