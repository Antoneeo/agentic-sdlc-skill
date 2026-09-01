---
description: F-045 - review convergence doctrine (code lens spine). Four field-lesson blocks from the 2026-08 eight-FAIL review session (Execute-Before-Specify, converge-not-accrete, severity contract, author pre-audit) plus the two review-hardening additions (proportionality clause, reviewer-side probe check). Spine ported to all three distributions.
status: COMPLETED
end_date: 2026-09-01
feature: F-045
id: F-045
start_date: 2026-09-01
level: L3
branch: main (uncommitted - integration decision pending)
---
# ANALYSIS: Review Convergence Doctrine (F-045)

**Level: L3 · router: no match** (`reference/INDEX.md`: only GUIDE_release, applicable at release, not to this authoring).
Elicitation: skip path — the spec is the owner's own uncommitted diff (four doctrine blocks, reviewed in-session) plus the owner's explicit instruction "procedi col porting e le due aggiunte raccomandate".

## Objective

Codify the 2026-08 field lesson — eight consecutive design-review FAILs that converged to PASS in one round once behavioural claims were executed and the artifact was rewritten lean — into the skill's doctrine, at the three points where the failure was produced: input quality (probes, pre-audit), loop dynamics (severity scale), revision behavior (converge, not accrete). Then close the two gaps the in-session review found: the probe duty had no proportionality bound and no reviewer-side check.

## Vision Alignment

The skill's north star is preventing myopia — acting from partial understanding. Execute-Before-Specify attacks its purest form: behavioural claims produced by reading, stated with confidence, wrong. The three review.md blocks protect the review gate's own value (measured via REVIEW_LOG): a loop whose rounds are burned on inflated blockers, rotted anchors and self-inflicted consistency findings converges never, and a cap that punishes honesty gets ignored. No Non-Goal touched: the additions are doctrine prose, no new tooling, no new mandatory artifact for L1/L2.

## Use Cases / User Needs

- **UC1 — the L3 author.** Gets a mechanical discipline (probe, then write; pre-audit, then request) that collapses review rounds instead of discovering claim-rot one finding at a time. Proportionality clause keeps the duty from becoming probe theater on trivial claims.
- **UC2 — the design reviewer.** Gets a re-runnable harness instead of re-deriving claims, a severity taxonomy that keeps the round cap meaningful, and a mechanical probe check (three findings, owned by the new clause) symmetric with the blast-radius check.
- **UC3 — the artifact's next reader.** Gets an artifact that states what IS, once — archaeology lives in REVIEW_LOG notes.

Product-name buckets: **Execute-Before-Specify NEW** (SKILL.md §3), **converge-not-accrete NEW**, **severity contract NEW**, **author pre-audit NEW**, **behavioural-claim-probes reviewer clause NEW** (all review.md), **`ai_docs/solutions/harness_[feature]/` NEW** (location); blast-radius enumeration EXISTS (SKILL.md §3), round cap + REVIEW_LOG EXIST (review.md), shared spine + drift guard EXIST (`scripts/shared_files.py`, `scripts/test_drift.py`), lens-conditional clause pattern EXISTS (review.md §Reviewing, "fires only in the lens…"). Traces: UC1/UC2 → the review gate's measured value (REVIEW_LOG); UC3 → the anti-myopia north star.

## Functional Spec

Trigger not fired: no script, command or observable tool output changes — doctrine prose only. (The battery's observable behavior is unchanged; drift manifests updated as data, not behavior.)

## Interface Contract

Trigger not fired: no actor-facing surface created or modified — the skill's prose is read by the agent, and no interaction flow changes shape.

## Capability Ledger

All capabilities EXIST — no component built. Carriers: SKILL.md §3 (authoring duties live there, beside blast-radius), review.md §When-a-review-is-due (round-cap discipline), §Requesting (request-side duties), §Reviewing (lens-conditional check family), `shared_files.py --update` (spine propagation). One-line verdict: pure doctrine addition on existing carriers; the architect pass has nothing to design.

## Impact

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY (owner: Execute-Before-Specify block; this unit: proportionality sentence) | authoring duty lives beside blast-radius; per-lens file, code lens only |
| `skills/agentic-sdlc-skill/review.md` | MODIFY (owner: 3 blocks; this unit: probe-check reviewer clause) | shared spine — single definition of review behavior |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/review.md` | MODIFY (byte-identical port) | spine invariant: three copies, one file |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/review.md` | MODIFY (byte-identical port) | same |
| `scripts/shared_manifest.json` ×3 | MODIFY (`shared_files.py --update`) | drift-guard hashes follow the spine |

Blast radius: review.md is consumed by the two sibling lenses verbatim — the new probe clause is lens-gated ("fires only in the lens whose SKILL.md defines Execute-Before-Specify — the code lens today"), so kb/mkt reviewers never fire it; the clause self-disarms like the existing UC/FS/IC/Ledger clauses. No script consumes the edited prose (verified: battery green with no test changes).

## Security and Threat Model

No code, no input parsing, no new execution path. One surface considered: the harness convention (`harness_[feature]/`) invites executable scripts into `ai_docs/solutions/` — they run only when an author or reviewer invokes them, same trust level as `scripts/`; no automatic execution is wired anywhere. Residual: none beyond pre-existing repo trust.

## Action Plan

1. ~~Owner authors four doctrine blocks~~ (input to this unit, uncommitted diff).
2. ~~In-session adversarial review of the diff~~ (findings: spine drift BLOCK, unregistered workstream, Write Triggers gap WARN, probe asymmetry WARN).
3. ~~Proportionality sentence in SKILL.md Execute-Before-Specify~~.
4. ~~Behavioural-claim-probes clause in review.md §Reviewing (lens-gated)~~.
5. ~~Port review.md to kb + mkt distributions; `shared_files.py --update` ×3~~.
6. ~~Battery + drift verification~~ (184 OK code lens; drift OK ×2 siblings).
7. ~~Register workstream (this ANALYSIS, HANDOFF, REVIEW_LOG row, index regen)~~.
8. OPEN — owner: integration decision (commit/branch), release cycle per GUIDE_release (bump ×3 + CHANGELOG), Write Triggers row for `harness_[feature]/` (deliberately scoped out by the owner's instruction).

## Test Strategy

No new tests: the unit is doctrine prose guarded by the existing drift battery. Evidence: `python -m unittest discover -s scripts -p "test_*.py"` → `Ran 184 tests — OK` (code lens, post-edit); `python -m unittest scripts.test_drift` → OK in both sibling distributions; the two pre-existing FAILs (`test_no_shared_file_has_diverged`, `test_the_copies_are_identical_to_each_other`) were the drift this unit repaired.

## Diary

- **2026-09-01 (later) — falsifiability guard-rail added.** Owner-approved third addition to Execute-Before-Specify: a probe must be shown RED first (negate the condition or state), then green — `tdd.md`'s RED gesture applied to the experiment. Closes the vacuous-assertion failure mode (probe passes but establishes nothing). Author-side only, one sentence; the reviewer clause is untouched — the reviewer already reads the probe and can contest a vacuous assertion. SKILL.md is per-lens: no porting, no manifest change.
- **2026-09-01 — unit opened and closed in one session.** Owner authored the four blocks (uncommitted); session agent reviewed the diff adversarially (4 findings — spine drift found by running the battery, not by reading), owner approved porting + the two hardening additions; executed, verified, registered. Review logged as FAIL → PASS, one WARN open (Write Triggers row). Integration and release are the owner's next call.
