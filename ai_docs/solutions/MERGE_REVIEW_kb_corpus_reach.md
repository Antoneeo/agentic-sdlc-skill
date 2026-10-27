---
feature: F-084
analysis: ANALYSIS_kb_corpus_reach.md
base: main
---
# Merge review: the corpus knows what it never examined, and what we declared

## Purpose

A field report showed a KB answering `kb: no coverage` while the source sat in the
project unexamined, and unable to say what the project had declared to a client.
`inventory <path>` now classifies each project file against the corpus by content
(INGESTED / INGESTED_EARLIER / EXCLUDED by an approved registry / NOT_EXAMINED, plus
SKIPPED directories), orient prints an upper bound of the never-examined files, recall
looks before saying `no coverage`, and `stale` names a changed original. A document
the project sends is stored as sent with `provenance: DECLARED`; its claims are
`DECLARED`, a contradiction with the ledger is held one-way as `DIVERGES`, and
declarations never leave the project in a bundle. Owner rulings: R2 (lookup on a
named area), R4 (one-way DIVERGES), R5/R9 (upper bound), R7 (admission r37/r38 with
the cost), R8 (T8 residual), R11 (measured read cost +6,971 B).

## What to review

Map computed against 854a8697 (origin/main). The changes are uncommitted in worktree
`wt-f084-kb-corpus-reach`, branch `claude/f084-kb-corpus-reach`. `knowledge.py`,
`sdlc_core.py`, `docs_site.py` and `docs_site/*` are four identical copies: review one
(the kb distribution's), the drift guard proves the others.

# Review map -- 54 files against 854a8697 (merge-base 854a869729a8)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +3/-0 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +3/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/docs_site/app.js` | M | +7/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/docs_site/strings.js` | M | +8/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/docs_site/style.css` | M | +2/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/docs_site.py` | M | +14/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/knowledge.py` | M | +539/-16 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_core.py` | M | +9/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +6/-6 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +6/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +16/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/distillation.md` | M | +15/-5 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/docs_site/app.js` | M | +7/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/docs_site/strings.js` | M | +8/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/docs_site/style.css` | M | +2/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/evals/scenarios/declaration_is_held_as_divergence.md` | A | +52/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/evals/scenarios/recall_names_the_unexamined_residue.md` | A | +36/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/portability.md` | M | +7/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/reconciliation.md` | M | +17/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/docs_site.py` | M | +14/-2 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/knowledge.py` | M | +539/-16 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_core.py` | M | +9/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +6/-6 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_kb_corpus_reach.py` | A | +790/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` | M | +46/-4 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +3/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/docs_site/app.js` | M | +7/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/docs_site/strings.js` | M | +8/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/docs_site/style.css` | M | +2/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/docs_site.py` | M | +14/-2 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/knowledge.py` | M | +539/-16 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py` | M | +2/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/sdlc_core.py` | M | +9/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +6/-6 | REVIEW | review |
| `skills/agentic-sdlc-skill/docs_site/app.js` | M | +7/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/docs_site/strings.js` | M | +8/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/docs_site/style.css` | M | +2/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/docs_site.py` | M | +14/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/knowledge.py` | M | +539/-16 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | M | +9/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +6/-6 | REVIEW | review |
| `ai_docs/architecture/ADR_2026-10-27_declarations_and_corpus_reach.md` | A | +60/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_kb_corpus_reach.md` | A | +594/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_kb_corpus_reach.md` | A | +126/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +2/-2 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +18/-4 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +2/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/requests/REQUEST_kb_corpus_reach.md` | A | +134/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +2/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_kb_corpus_reach/probe.py` | A | +253/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/INDEX.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +6/-3 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 42 files (+3337/-119); DESIGN 6 files (+802/-6); EVIDENCE 3 files (+389/-0); GENERATED 3 files (+8/-3)

## What the gates verified

- **Design review** (fresh deep-tier subagent, 3 rounds, FAIL → FAIL → FAIL, cap
  reached): the owner accepted the design with the round-3 fix to be verified at
  closure (R6); the closure review verified it.
- **Closure review** (fresh deep-tier subagent, 3 rounds, FAIL → FAIL → PASS):
  conformance of every FS/AC to code and test, the blast radius by grep, path
  confinement, links and junctions, mutation testing of `test_kb_corpus_reach.py`.
  Each round the reviewer re-ran the four batteries.
- **Evidence, final run**: batteries code 464, kb 791, mkt 466, course 459 OK;
  `probe.py --expect-outcomes` rc 0 (baseline green with the three removed defects
  inverted; outcomes O1–O6 green); `shared_files.py`: 31 shared files identical;
  `validate` 0 errors; `check` NOT CLEAN only on `stale` — the changed areas
  (`skills/agentic-sdlc-skill/`, `distributions/`, `skills/`) are marked with the
  commit hash in a follow-up commit, as F-083 did; `check` is CLEAN after it.

## What only a human can judge

- **Residuals the review accepted as WARN, for you to accept or send back:** a
  *file* link named like a skipped directory (`.env`, `build`) or matching a dir-only
  exclusion is listed as that directory, because links are matched by name and never
  resolved (nothing is read); the `kb_unreadable` OSError mapping has no test;
  symlink-specific branches were not exercised here (no symlink privilege; junctions
  were); real OneDrive/macOS placeholders were only simulated.
- **T8**: a hand edit of `DIVERGES` back to `OK` is undetectable (accepted, R8).
- **The E2E script** (`E2E_TEST_kb_corpus_reach.md`), S1–S7 and R1–R2, run by a
  human after the merge — ideally on the field project that reported the gap.
