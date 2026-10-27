---
feature: F-085
analysis: ANALYSIS_working_model.md
base: main
---
# Merge review: constraints at the moment of action

## Purpose

An L3 unit's constraints, which today sit in prose the agent read hours earlier or
never, become extractable (ids, a `### Preservation constraints` table), viewable in one
command, and recalled to the agent just before it edits a file they bind. It serves the
feature Vision's G1–G4 and its north star, "fewer rounds and less friction because the
agent keeps the situation under control" (`vision/features/VISION_working_model.md`,
R3), measured by S1 (defects that escape a gate) leading S2 (design-review FAILs).

## What to review

Map computed against `main` 9709768e (merge-base). The change is uncommitted on branch
`feat/f085-working-model`, which sits on that commit.

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +8/-0 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +3/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/docs_site/strings.js` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/guides.md` | M | +8/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/review.md` | M | +9/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/docs_site.py` | M | +3/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_core.py` | M | +506/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +9/-8 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_constraints.py` | A | +684/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_docs_site.py` | M | +17/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_skill_invariants.py` | M | +91/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +3/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/docs_site/strings.js` | M | +1/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/guides.md` | M | +8/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/review.md` | M | +9/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/docs_site.py` | M | +3/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_core.py` | M | +506/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +9/-8 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_constraints.py` | A | +684/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_docs_site.py` | M | +17/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_skill_invariants.py` | M | +91/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +3/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/docs_site/strings.js` | M | +1/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/guides.md` | M | +8/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/review.md` | M | +9/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/docs_site.py` | M | +3/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/sdlc_core.py` | M | +506/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +9/-8 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_constraints.py` | A | +684/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_docs_site.py` | M | +17/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_skill_invariants.py` | M | +91/-0 | REVIEW | review |
| `docs-site.zip` | A | bin | REVIEW | review |
| `npm` | A | +0/-0 | REVIEW | review |
| `scripts/lib.js` | M | +19/-4 | REVIEW | review |
| `scripts/postinstall.js` | M | +13/-1 | REVIEW | review |
| `scripts/preuninstall.js` | M | +4/-7 | REVIEW | review |
| `scripts/test_clients.js` | M | +84/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/ENFORCEMENT.md` | M | +32/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +3/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/docs_site/strings.js` | M | +1/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/guides.md` | M | +8/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/review.md` | M | +9/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/docs_site.py` | M | +3/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/fixtures/golden_baseline.txt` | M | +8/-4 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` | M | +1/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | M | +506/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +9/-8 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_constraints.py` | A | +684/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_docs_site.py` | M | +17/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | M | +91/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/templates.md` | M | +24/-3 | REVIEW | review |
| `ai_docs/architecture/ADR_2026-10-27_context_only_recall_hook.md` | A | +65/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/reference/GUIDE_shared_project_memory.md` | M | +11/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_working_model.md` | A | +439/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_working_model.md` | A | +113/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +6/-5 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/existing_features.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/features/VISION_working_model.md` | A | +251/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/requests/REQUEST_working_model.md` | A | +94/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +4/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_working_model/LIVE_PROBE_2026-10-27.md` | A | +27/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_working_model/baseline_review_log.py` | A | +45/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_working_model/probe_extractability.py` | A | +80/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_working_model/probe_hook_live.py` | A | +84/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_working_model/probe_hook_timing.py` | A | +107/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_working_model/probe_impact_bridge.py` | A | +46/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_working_model/probe_self_view.py` | A | +40/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_working_model/probe_session_level.py` | A | +99/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_working_model/sample_2026-10-27.txt` | A | +18/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/INDEX.md` | M | +2/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +8/-4 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
Totals: REVIEW 55 files (+5521/-64); DESIGN 8 files (+887/-5); EVIDENCE 11 files (+644/-0); GENERATED 3 files (+11/-4)

Where to start: `skills/agentic-sdlc-skill/scripts/sdlc_core.py` §constraints (the
reader, `constraints_hook_context`, `transcript_work`) and the FS7 lines in
`cmd_validate`; `scripts/lib.js` `RECALL_HOOK`; then `test_constraints.py`. The
`distributions/` copies are byte-identical to the code lens's (four manifests, one hash).

## Already verified

- **Design review** — REVIEW_LOG 2026-10-27, `ANALYSIS_working_model.md (F-085)`, tier
  `design`, FAIL → FAIL → FAIL (cap), handed to the owner with the open findings fixed;
  the owner approved the design (REQUEST_working_model.md R14). Covered the ANALYSIS.
- **Closure review** — REVIEW_LOG 2026-10-27, `diff main 9709768e..working tree (F-085)`,
  tier `closure`, deep, FAIL → PASS after a scoped round 2; its one condition (the
  latency's acceptance) met by R15. Covered every REVIEW and DESIGN file above, the E2E
  script and the harness.
- **Vision** — blind check of the feature Vision, FAIL → PASS, approved R10; blind check
  of the amendment (two factual sentences), PASS, approved R16.
- **Tests, after the final code edit, on the integrated tree** — code 542, course 537,
  kb 869, mkt 544 tests OK; `node scripts/test_clients.js` 63/63; the seven probes of
  `solutions/harness_working_model/` red/green OK; `probe_self_view.py` green;
  `probe_hook_timing.py` about 0.25 s per edit. The closure reviewer re-ran them all.
- **Live hook probe** — `harness_working_model/LIVE_PROBE_2026-10-27.md`: Claude Code
  delivers a decision-less `additionalContext` and applies the edit; an absent
  `constraints` subcommand behind `; exit 0` never blocks an edit.
- **Owner decisions** — scope code lens only and costs (R12), unaccepted costs and the
  hook fallback (R13), design approval (R14), per-edit latency (R15), Vision amendment
  (R16). `vision/rulings.md` r39 records the admission.
- Not covered by a review: the generated files (GENERATED above), proven by `check`.

## Your judgement

- **Deviations from the approved design**, all recorded in the Diary: `validate`'s note
  gated on the code lens (capability `preservation_constraints`), not the domain alone,
  so the kb lens's frozen 1.0 transcript does not change; FS4's "prose but no id'd item"
  read as "no id'd item at all"; the hook resolves the docs root from the edited file;
  one 15-line budget per recall.
- **Accepted residuals**: a prose line opening with "Level L1" silences the recall (T8);
  the constraint text enters the agent's context (T4, clipped and stripped); the view
  never claims completeness and the reviewer still derives first (T6, T7).
- **CANNOT VERIFY**: whether a decision-less PreToolUse object leaves the interactive
  permission prompt unchanged (the live probe ran in auto mode; the JSON carries no
  decision, structurally); `; exit 0` on macOS/Linux shells (probed on Windows only).
- **Decisions still owed**: the release and its version; the two follow-ups below.

## Merge notes

- Conflicts are possible only in generated files and manifests if `main` moves again:
  regenerate with `sdlc_check.py index` and `shared_files.py --update` in each skill
  folder, never resolve by hand. CHANGELOGs and `vision/rulings.md` keep both sides.
- After the commit, `sdlc_check.py mark` on the changed areas (skills/, scripts/,
  distributions/), committed on its own, so `check` reads CLEAN; after a squash or rebase
  merge, re-mark on `main`.
- Installing the package wires a second PreToolUse hook (the recall) beside the
  guide-verdict check; removing its entry is a standing opt-out.
- E2E script for testers: `solutions/E2E_TEST_working_model.md`.
- Follow-ups proposed: the verdict hook matches a `Level: L1` quoted in prose and
  resolves its project from the working directory; the blind check's WARNs on the
  approved Vision's text (maintenance in the admission test, unranked sections, who may
  redefine a signal, optional Impact ids, neutral ordering).
