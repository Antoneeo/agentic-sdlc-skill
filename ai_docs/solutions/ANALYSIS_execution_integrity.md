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
owners strengthened.

**Ceremony cost, disclosed (Non-Goal 3 requires this, and it was missing from v1 of this
document — raised by the late design review).** The change removes no existing check, so it
runs on the disclosure-and-acceptance path. What it adds, measured on the shipped diff:

| Cost | Where | Who pays it |
|---|---|---|
| +12 net lines in the always-loaded `SKILL.md` (a triage table, two Phase-5 bullets) | read every session, at every level | every project |
| +28 lines in `review.md` ×3 distributions | read by every reviewer, code/knowledge/marketing | every reviewer invocation |
| One mandatory extra review round when a review produced findings (the scoped re-review) | L2 optional review, L3 closure and design reviews | L3 mostly; L2 only when its optional review ran |
| A reporting duty on completion claims (name the claim, run the proof, report the status) | every level, including L1 | every claim — smallest at L1, where the proof is usually the test already run |

L1 gains no document, no subagent, no gate — only the duty to say what it verified.
**Explicitly accepted by the owner, 2026-08-06**, on the stated ground that the added ceremony
pays when it buys doing the work right the first time instead of discovering the defect late
(Diary). The rulings placement for each mechanism is below.

**Rulings placement (`ai_docs/vision/rulings.md` procedure, run per mechanism).** The ledger
keys identity on the question a capability answers or the effect it has in the delivered
system — not on whether that question is user-facing; v1 of this document applied the narrower
test and the late design review rejected it. Corrected placement:

| Mechanism | Question it answers | Placement | Line |
|---|---|---|---|
| Claim-to-evidence | what proof permits an agent to assert the current state? | **r14** (bounded maintenance exemption) | purpose, actors and surface unchanged: the closure phase already demanded technical evidence; this fixes a defect in that demand (an unstated freshness/breadth contract) — the F-033 false-CLEAN is the defect |
| Scoped re-review | how is a change made *because of* a review finding proven safe? | **r14** | the review gate and its cap of 3 already existed; the rounds were already run in practice (F-033 R1→R2). This writes down the round nobody had written |
| Destructive guards | what authority is required before irreversible branch/worktree action? | **r14** | Phase 5 already required an explicit merge decision; this states what "explicit" means and forbids inferring it. No new actor, no new surface |
| Rationalization tables / red flags | *(none — it is a WRITING TECHNIQUE, not a capability)* | **outside the ledger** | it adds no ability the system did not have: every rule it annotates already existed and already bound. The falsifiable distinction: delete every table and no rule changes meaning, no check appears or disappears. The Capability Ledger row calling it "NEW as a technique" meant new-to-this-repo as a style, not a new capability — reworded below |
| `CANNOT VERIFY` output | what does a reviewer owe about what it could not check? | **r14** | the reviewer contract (cite evidence, verdict as final output, conformance statement) already existed; this closes its silent-pass hole |
| No-pre-judging rule | who decides whether a finding is a false positive? | **r14** | §Receiving already owned finding resolution ("never reword until it goes away"); this binds the requester side of the same rule |

No mechanism lands on a REJECT row: none meters or caps a user's work (r1), none collects
per-work state into a surface (r2), none tells an agent what to work on next (r3), none
introduces a second triage authority (r10). The two provisions a motivated reader raises against
an r14 placement, answered on the record rather than left in the author's head:
- **r4 (scope growth is re-ruled as new).** The claim-to-evidence duty reaches every level while
  the maintained slot is Phase 5 — does it widen an admitted capability? Distinction: `SKILL.md`
  §Technical Values already bound verification at every level ("close implementation work with
  tests, lint, smoke checks or an explicit reason"); this states WHEN the evidence must have been
  produced and HOW WIDE a claim it supports. Falsifiable: name one level that owed no verification
  before this change and owes one now — there is none.
- **The effect backstop** (a capability the system *can no longer do* is a changed capability
  whatever the proposal calls it). The destructive guards do remove something: the agent can no
  longer clean up a branch unasked. Distinction: the removed ability was never admitted — Phase 5
  already required an explicit merge DECISION, so acting without it was a defect, not a
  capability. Read literally the backstop refuses every bug fix, which the Vision itself records
  as its known over-reach.

If the owner judges any placement above to be a stretch of r14 rather than a defect fix, that
mechanism needs its own ruled row before it stands — the ledger's procedure, not this document,
is the authority.

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
- Enforcement-writing technique (rationalization tables / red flags) — a WRITING STYLE new to
  this repo, not a capability: it annotates rules that already exist and already bind (delete
  every table and no rule changes meaning). Applied only to what this change touches: triage
  (Rule Zero table), verification (red-flag line). tdd.md/debugging.md untouched (Tranche B).

## Impact
- `skills/agentic-sdlc-skill/SKILL.md` — Rule Zero: triage rationalization table; Phase 5:
  claim-to-evidence bullet (fires at every completion claim, any phase/level) + destructive
  guards bullet (extends branch hygiene, cites the guide router).
- `review.md` ×3 (shared spine, byte-identical — canonical edited, siblings copied, hashes
  verified) — §Requesting: never pre-judge findings; §Receiving: new "Review-driven
  corrections (scoped re-review)" subsection; §Reviewing: CANNOT VERIFY reporting duty, and
  **the unproven-completion-claim finding class** — the enforcement point the claim-to-evidence
  rule promised (added in v1.26.1; its absence in 1.26.0 was a design-review BLOCK: an
  acceptance criterion cannot promise a check no reviewer can cite).
- `dispatch.md` ×3 (shared spine) — **missed by the v1 Impact and caught by the late design
  review**: its "exactly three review touches, never a loop" contradicted the scoped re-review
  it delegates to `review.md` to define. Reconciled in v1.26.1: the scoped re-review is a round
  INSIDE slot 2 or 3, never a fourth slot; "never a loop" bounds the slots, not the rounds.
- **Lens scoping, declared** (v1 left it silent): the `SKILL.md` rules (claim-to-evidence,
  destructive guards, triage table) land in the CODE lens only — the observed failure is
  code-lens, and the sibling lenses' closure phases are structurally different. The `review.md`
  and `dispatch.md` changes are shared spine and therefore ACTIVE in all three: a knowledge or
  marketing artifact review inherits the correction discipline unchanged. Landing the SKILL.md
  half in kb/mkt is a separate unit of change, not an omission of this one.
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
rule being landed) → release. **v1.26.1 (late design review remediation):** dispatch.md
reconciliation + SKILL.md hygiene/guard reconciliation + review.md enforcement clause, PASS-with-
findings and FAIL-visibility wording → spine propagation → this document's ceremony disclosure,
rulings placement and lens scoping → scoped re-review of the corrections.

**Named disposition for the chronic `stale` debt** (raised by the late design review; Success
Signal 2 says closure is mechanically clean, and four releases have now shipped against a red
gate). It is NOT closed here and this change does not own it: `mark` asserts a re-analysis, and
asserting one that did not happen is the exact claim-class this feature exists to forbid. It
becomes its own unit of work — re-analyze the mapped areas the last four releases touched, then
`mark` them — sized as documented maintenance, to be scheduled by the owner. Until then every
closure states the gate's real status rather than claiming clean.

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

2026-08-06 (later) — **Late moment-1 design review run (`1b. Late arrival`), and it FAILED with
4 BLOCK.** The design gate had been skipped before implementation and declared as a deviation;
running it late proved the deviation was the session's real defect, because the closure review
could not structurally have found any of these: (1) Non-Goal 3's ceremony budget entered with
no cost stated and no recorded acceptance — r16/r17 both required it, and the Vision's
"omission resolves against the proposal" voids an acceptance given without it; (2) the rulings
placement never run, the ledger's criterion silently narrowed to "user-facing"; (3) the
claim-to-evidence rule's promised enforcement point absent from `review.md`, so the rule bound
the author in a file the reviewer is never handed; (4) `dispatch.md` — shared spine, missing
from the Impact — left contradicting the scoped re-review it delegates to `review.md` to
define. Plus WARNs on the `SKILL.md` cleanup/guard conflict, the PASS-with-findings gap, the
one-row-vs-FAIL-visibility tension, undeclared lens scoping and the unowned `stale` debt.
**All fixed in v1.26.1**; the ceremony cost was put to the owner with real numbers and
**explicitly accepted** on the ground that ceremony which buys getting it right the first time
pays for itself. Durable lesson, recorded because it cost a whole extra release: the design
review is not interchangeable with the closure review — one asks whether the code matches the
design, the other whether the design was right, and only the second catches an authority
contradiction, an unrun admission or a missing enforcement point.
