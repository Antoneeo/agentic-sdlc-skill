---
id: F-034
feature: Execution Integrity Tranche A — claim-to-evidence, scoped re-review, destructive guards, rationalization tables
status: COMPLETED
level: L3
start_date: 2026-08-06
end_date: 2026-08-06
---
# Feature Analysis: Execution Integrity — Tranche A (F-034)

## Objective
Close the observed execution-discipline gaps at the cheapest layer (doctrine wording, zero
machinery): completion claims backed by fresh evidence, review-driven fixes that cannot escape
review, destruction of branch/worktree state gated on explicit human intent — plus the
enforcement-writing technique (rationalization tables / red flags) on the highest-drift rules.

## Feature Vision
Derived from a firsthand comparative study of Superpowers 6.2.0 (MIT, Jesse Vincent) and an
external two-round spec (V1 reviewed FAIL → V2 reviewed PASS), adopted SELECTIVELY under the
standing weight test: a mechanism enters only on an observed repository failure the existing
gates don't catch, or as an irreversible-damage guard. Concepts reimplemented in this skill's
terminology; no text copied, no runtime dependency, single process spine preserved. Tranche B
(tdd/debugging strengthening) and Tranche C (dispatch ledger machinery) are deliberately NOT
in this change — B rides the next admitted touch of those overlays, C stays frozen until a
real failure reopens it. Non-goal: no new file, no validator change, no new gate — existing
owners strengthened. No rulings row: these strengthen existing owners (Technical Evidence,
review discipline, Phase-5 hygiene) and answer no new user-facing question.

## Use Cases / User Needs
- The owner reads a completion claim and can trust it binds to evidence produced after the
  final relevant edit — observed failure: a closure artifact claimed "check clean" while the
  gate returned NOT CLEAN (REVIEW_LOG, F-033 row). (Grounding: "Technical Evidence",
  "Phase 5", "REVIEW_LOG" EXIST; "claim-to-evidence" NEW, declared.)
- The owner's review investment is not silently voided by the fix — observed: reviews take 2
  rounds because the fix diff is itself unreviewed work; the discipline that already ran in
  practice (F-033 scoped R2) becomes doctrine.
- The owner never loses branch/worktree state to an inferred intention — irreversible-damage
  guard, admitted on risk (same class as "security-sensitive is never L1").

## Functional Spec
- Any completion claim ("passes", "fixed", "clean", "complete") made without a proof run after
  the final relevant edit is a doctrine violation the closure review can name; a narrower
  check never supports a broader claim; delegated work is verified on the diff, never on the
  subagent's report; an unavailable proof is reported as a limitation, never claimed.
- A review-driven correction reaches PASS only through a scoped re-review with per-finding
  verdicts (ADDRESSED / NOT ADDRESSED / CONTESTED); new blocker-level breakage inside the
  correction joins the findings; out-of-scope observations never extend the loop; rounds stay
  within the existing cap of 3; one logical review stays one REVIEW_LOG row.
- Discard/force-push/foreign-worktree-cleanup are offered or executed only on the user's
  explicit request, naming exactly what would be destroyed; project-specific release/finish
  commands stay in the project guide layer (cited, never restated).
- Acceptance: a completion claim made without fresh proof is nameable as a violation by the
  closure review; a correction that reached PASS without a scoped re-review is nameable the
  same way; the correction discipline applies identically to knowledge and marketing artifact
  reviews (lens-neutral wording); L1/L2 gain no ceremony beyond evidence proportionate to the
  claim being made.

## Interface Contract
Not fired — authored doctrine text; no runtime surface an actor acts on or perceives.

## Capability Ledger
- Closure-evidence slot — EXISTS (SKILL.md Phase 5 "Run the relevant tests/lint/smoke checks";
  devPNT §5 Technical Evidence) — strengthened in place with freshness/breadth/delegation.
- Review discipline + round cap — EXISTS (`review.md` "Rounds are capped at 3", §Receiving) —
  the scoped re-review is a subsection of it, integrating with (citing) the existing rules.
- Branch hygiene — EXISTS (Phase 5 bullet) — destructive guards appended to it.
- Guide-layer routing — EXISTS (`## Operative Guides` router) — cited by the finish guards.
- Enforcement-writing technique (rationalization tables / red flags) — NEW as a technique,
  applied only to what this change touches: triage (Rule Zero table), verification (red-flag
  line). tdd.md/debugging.md untouched (Tranche B).

## Impact
- `skills/agentic-sdlc-skill/SKILL.md` — Rule Zero: triage rationalization table; Phase 5:
  claim-to-evidence bullet (fires at every completion claim, any phase/level) + destructive
  guards bullet (extends branch hygiene, cites the guide router).
- `review.md` ×3 (shared spine, byte-identical — canonical edited, siblings copied, hashes
  verified) — §Requesting: never pre-judge findings; §Receiving: new "Review-driven
  corrections (scoped re-review)" subsection; §Reviewing: CANNOT VERIFY reporting duty.
- devPNT repo (companion, uncommitted branch): `agents/devpnt-tech-reviewer.md`,
  `devpnt-tech-reviewer-light.md`, `devpnt-code-reviewer.md` — output schema gains
  `CANNOT_VERIFY` severity.
- ai_docs: this ANALYSIS, `ADR_2026-08-06_execution_integrity_tranche_a.md`.
- CHANGELOG ×3, version bumps ×4 points ×3 distributions, shared manifests ×3.

## Security and Threat Model
Doc-only; no execution path, no dependency. The destructive-guards bullet REDUCES risk
(irreversible loss gated on explicit intent). Provenance: concepts only, no copied text —
no MIT notice obligation triggered (recorded in the ADR).

## Action Plan
Single pass: SKILL.md → review.md canonical → sibling propagation → devPNT agents → ai_docs →
bumps → batteries → independent closure review (with its own scoped re-review, dogfooding the
rule being landed) → release.

## Test Strategy
`test_skill_invariants.py` ×3, `test_drift.py` ×3 (byte-identity of the spine + manifests
identical), `sdlc_check.py validate` (0 errors), golden regression untouched (no validator
change). Independent closure-style review on the full diff; any fix enters the scoped
re-review loop just landed.

**Gate status, stated per the claim-to-evidence rule this change lands:** `sdlc_check.py
check` returns **NOT CLEAN** — `validate` rc=0 (0 errors) but `stale` rc=1. The stale set is
chronic audit-mark debt carried since 1.22.0 (it also names files this change edited, because
`stale` keys on the last `mark`, not on this diff); 1.23.0–1.25.0 shipped with the same debt.
This is disclosed rather than claimed clean — the rule forbids reporting the gate as clean
when it is not, and forbids a `mark` asserting a re-analysis that did not happen.

## Diary / Current State
2026-08-06 — Firsthand study of all 14 Superpowers skills confirmed the external spec's
tranche split and surfaced what it missed: the enforcement-writing technique (rationalization
tables + red flags) — Superpowers' real asset is HOW it writes rules, not any mechanism.
Adopted: Tranche A (3 observed/irreversible items) + the technique on touched rules + 3
reviewer-side lines (CANNOT_VERIFY, no pre-judging, delegated-work-on-diff). Rejected
firsthand: universal brainstorming gate (anti-proportional), 5-round fix loop (our cap stays
3), per-step-commit plans, the "1% chance → must invoke" trigger. Released as code 1.26.0 /
kb 1.4.6 / mkt 0.4.6 (kb/mkt entries are ACTIVE, not inert — the correction discipline applies
to their artifact reviews too).
