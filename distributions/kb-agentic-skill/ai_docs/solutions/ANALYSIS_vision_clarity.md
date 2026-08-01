---
id: F-017
feature: Vision Clarity (cold-readable, decidable Vision)
status: COMPLETED
level: L3
start_date: 2026-07-27
end_date: 2026-07-27
---
# Feature Analysis: Vision Clarity

## Objective

Make `vision/project_vision.md` usable by the reader it was always written for and
never tested against: someone — a later session, a reviewer, another agent — who
arrives cold, with no context and no one to ask.

Owner's framing (2026-07-27): *"vorrei che la VISION venisse rivista con un reviewer
ignaro per capire se è chiara o se vengono dubbi… nelle sessioni successive ma anche
nelle altre review, viene vista da reviewers ignari."*

Three blind reviewers were run against the APPROVED text with no repository access
(evidence: `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`). Verdict: **the Vision
was not operable as a decision instrument.** The decisive result is not stylistic — a
proposal to *cap how many operative guides a free user may create per month* was ruled
**admissible on the literal text**, because no Non-Goal covered metering and every
anti-paywall constraint was bound to the proper noun `devPNT` rather than to paywalling
as a class. The same hole was exploited in practice on M89, when internal-KB metering
entered the design artifacts with no Non-Goal to catch it; the blind reviewer
rediscovered it from the text alone, knowing nothing of that incident.

## Feature Vision

This work serves the Vision by repairing the Vision. Concretely, against the goals the
rewritten document now states:

- **Cold-start operability** — the Vision is the entry point of the whole
  Documentation-First chain. If it cannot be read cold, every downstream gate that
  claims to check alignment against it is checking against something the checker did
  not understand. That is not a weak gate; it is a gate that reports PASS by
  construction.
- **Making divergence visible before implementation** — a Non-Goal set that admits
  metering, paywalls and remote dependencies cannot make that class of divergence
  visible. The gate's rejection surface *is* the Non-Goal list.
- **Anti-myopia**, the skill's stated reason to exist — a Vision defined by comparison
  to a moving external target rots silently: it keeps reading as authoritative under a
  permanent `APPROVED` banner while becoming false.

Non-Goals for this feature:
- **Not a repositioning.** The product's intent is unchanged; only its expression, its
  self-containment and its decidability change. Where the old text implied a
  commitment, the new text keeps it.
- **Not a deletion of the competitive analysis.** The A/B/C/D layer map and the
  superpowers comparison move to their existing home,
  `strategic/capabilities_and_positioning.md`, where they are dated and revisable.
- **Not a promotion.** The rewrite ships as `Status: DRAFT`. Only the owner promotes a
  Vision to APPROVED; until then the previous APPROVED version remains binding.
- Not in scope: making the blind-clarity check a permanent step of the skill's Vision
  lifecycle. That is a doctrine change, proposed separately at the end of this document.

Success signals for this feature:
1. A blind reviewer, re-run against the new text, can state what the product is and
   rule decidably on the same five proposals — in particular REJECT the metering one by
   quoting a line.
2. No claim in the Vision becomes false through a third party's action alone.
3. `sdlc_check.py check` stays clean and the manifest regenerates without hand edits.

## Use Cases / User Needs

- **Solo developer using an AI agent** — needs a fresh session to inherit the project's
  intent instead of re-explaining it. *Today the fresh session reads a document that
  requires knowing what `superpowers`, `devPNT`, `Feature B`, `L1/L3` and `Standalone`
  mean; none is defined in it.*
- **Team lead needing governance** — needs the Vision to actually reject the things it
  should reject, across several agents nobody is watching. *Today the rejection surface
  is four Non-Goals, one of which is a behavior rule, and one of which (`"Not a **full**
  ALM"`) carries its own escape hatch — demonstrated by a reword that walks a work-item
  ledger straight through the gate.*
- **Adopter evaluating the paid layer** — needs to know what is guaranteed free and
  complete. *Today `"zero capability loss without devPNT"` has two incompatible readings
  and no Non-Goal forbids a paid tier under a different name.*
- **A reviewer, human or agent, ruling on someone else's change** — needs an admission
  test. *Today the only affirmative criterion is that a change "inherits `ai_docs/`
  frontmatter, manifest and lifecycle" — a test of form, so every ACCEPT the gate has
  ever issued was inferential.*

## Impact

| Path | Change | What |
|---|---|---|
| `ai_docs/vision/project_vision.md` | MODIFY (rewrite) | Product stated in its own terms; `## Core Problem` added; Non-Goals rewritten as rules; new `## The admission test`; Success Signals made artifact-checkable; competitive scaffolding removed; `Status: DRAFT` pending owner promotion |
| `ai_docs/strategic/capabilities_and_positioning.md` | MODIFY | Declared owner of the A/B/C/D layer map; snapshot framing made explicit (recon date + competitor version); `description` updated |
| `ai_docs/audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md` | ADD | The three blind reviews, convergence table, decisive finding |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | MODIFY | One row + a note, per the review discipline |
| `ai_docs/solutions/ANALYSIS_vision_clarity.md` | ADD | This document |
| `ai_docs/INDEX.md`, `ai_docs/strategic/features_history.md` | REGEN | `sdlc_check.py index` |
| `ai_docs/audit/handoff.md` | MODIFY | Closure state |

**Blast radius — who reads the Vision and could break on the rewrite.** The Vision is
prose consumed by agents, not code, so the enumeration is of *referencing documents*,
verified by grep, not of call sites:

- `strategic/capabilities_and_positioning.md` — called itself a "Companion to
  `project_vision.md`" and its description said it "Feeds the four-layer product
  vision". The four layers now live only there; **updated in this change** so the
  relationship is not left describing a document that no longer exists in that shape.
- `SKILL.md` Vision Gate (Phase 2) and `templates.md` — reference the Vision by
  **path and by `Status:` semantics**, never by section name, so removing the layer
  section breaks nothing mechanical. Verified: the validator checks only for the
  presence of the file and a `Status: DRAFT|APPROVED` line (`sdlc_check.py:523`).
- `sdlc_check.py` `build_manifest` — derives the manifest row from `Status:` and the
  first prose line. The new first prose line is the pending-promotion note; the row
  will read DRAFT. Intended and correct while promotion is pending.
- `vision/roadmap_evoluzione_agenti.md` and the ANALYSIS corpus use `Feature A` /
  `Feature B` — those handles were never *defined* in the Vision, only cited, so no
  reference is orphaned by removing the citation. The handles keep their meaning in the
  roadmap that owns them.
- Nothing else greps `project_vision.md` for content.

## Security and Threat Model

Surface: **governance integrity**. No code, no input parsing, no network, no
credentials, no personal data. "No security impact" is not claimed — a Vision is an
authorization boundary, and this change edits it.

| Threat | Mitigation |
|---|---|
| V1 — **Silent authority swap.** A rewritten Vision could quietly become the binding gate without the owner ever approving it, which is precisely how vision drift is laundered. | The rewrite ships `Status: DRAFT` with an explicit pointer to the still-binding APPROVED version and its git ref. Only the owner promotes. The skill's own rule ("never promote a Vision to APPROVED without the user's confirmation") is honored, not narrated. |
| V2 — **Scope smuggling under cover of a clarity edit.** A "clarity" rewrite is the ideal vehicle for inserting or dropping a commitment. | Every Non-Goal in the new text is either a restatement of an old one or a documented finding-driven addition, listed one by one in `## Findings and disposition`. Nothing was removed on style grounds. The old text stays retrievable at `b35b36e`. |
| V3 — **Weakening the rejection surface.** Rewriting Non-Goals could accidentally *widen* what is admissible. | The new Non-Goals were written against the five test proposals: all five now rule decidably, and the two previously-admissible ones (metering, cloud-tier) are explicit REJECTs. The reword attack (work-item ledger dressed in `ai_docs/` conventions) is closed twice — by dropping the `"full"` qualifier and by the affirmative admission test. |
| V4 — **Enforcement theater.** A Vision that reads better but is not actually more decidable. | The claim is falsifiable and is stated as feature success signal 1: re-run the blind reviewers against the new text. Until that re-run, the improvement is asserted, not proven — recorded as such below. |
| V5 — **Loss of the competitive record.** Moving the comparison out could destroy it. | It moves to a file that already contained it in fuller, dated form; nothing is deleted, and that file now declares itself its owner. |

## Action Plan

- [x] Run three blind reviewers (comprehension / gate operability / durability) with no
      repository access; record verbatim evidence.
- [x] Rewrite `project_vision.md` as DRAFT against the convergent findings.
- [x] Move ownership of the A/B/C/D map to `capabilities_and_positioning.md` and mark it
      a dated snapshot.
- [x] Record the review in `REVIEW_LOG.md`.
- [x] **Owner promoted the Vision to APPROVED** (2026-07-27).
- [x] Re-run the blind reviewers against the promoted text (feature success signal 1).
      **Result: FAIL — signal 1 not met.** See `## Round 2` below.
- [ ] **v2 fix round** for the four round-2 BLOCKERs (owner approval required — amending
      an APPROVED Vision is a user decision, not an author decision).
- [ ] Decide the doctrine question below.

## Test Strategy

Prose artifact; no executable test of the content itself. Verification is:
- `sdlc_check.py validate` — Vision `Status:` parses, canonical headers intact, manifest
  regenerates idempotently (`test_indexes_idempotent`).
- Skill eval battery — must stay green; it asserts skill doctrine, and this change
  touches `ai_docs/` only, so a failure here would mean unintended coupling.
- **Adversarial re-read (the real test)**: re-run the three blind lenses against the new
  text. Deferred until after promotion so the reviewers judge the binding document, not
  a draft. Until then, feature success signal 1 is unproven and is recorded as such.

## Findings and disposition

Every convergent finding, answered — no silent drops (`review.md` §Receiving).

| # | Finding | Disposition |
|---|---|---|
| 1 | `superpowers` undefined, load-bearing in 3 of 4 layers | **Fixed.** All competitive framing removed from the Vision; the product is stated in its own terms. The comparison lives in `capabilities_and_positioning.md`, dated. |
| 2 | Never says what the product *is* | **Fixed.** New North Star opens with function, plus a `## Core Problem` section naming myopia. |
| 3 | `best-in-class` unfalsifiable, North Star *and* Success Signal | **Fixed.** Removed from both. A Non-Goal now forbids unfalsifiable superiority claims in the Vision. |
| 4 | No Non-Goal on metering/paywall/quotas | **Fixed — the P0.** New Non-Goal, written as a rule over the *class*, not the proper noun: nothing is ever metered, capped, tiered, paywalled or account-gated, by devPNT or any other mechanism, name or future product. Paired with a second Non-Goal forbidding required network/remote/off-repo storage (closes the P1 cloud-tier proposal). |
| 5 | Layer taxonomy fails its own Success Signal (guides in A, C, D) | **Fixed.** The taxonomy leaves the Vision; "operative guide" is defined once in the North Star, with its two source kinds (project code, user instruction) named in the same sentence. |
| 6 | Substance delegated to unopenable files | **Partially fixed, deliberately.** The Vision is now self-contained for *ruling*; `## Where the rest lives` points to detail as detail, never as the basis of a decision. A Vision cannot carry everything, so the fix is that no *decision* depends on the pointer. |
| 7 | 3 of 4 Success Signals unmeasurable | **Fixed.** Six signals, each checkable against a named artifact or command by someone who was not present. Signal 1 is the blind-read test itself. |
| 8 | `6.0.x` pins the Vision to a competitor release | **Fixed.** Gone from the Vision; in the positioning file it is now explicitly a dated snapshot with a re-date instruction. |
| 9 | `zero capability loss without devPNT` ambiguous | **Fixed.** Replaced by two unambiguous rules: nothing is ever gated (Non-Goal 3), and nothing may require remote infrastructure (Non-Goal 4). The Actor bullet no longer carries the load. |
| 10 | `Never hide a conflict…` occupies a Non-Goal slot | **Fixed.** Moved into Goals, where a required behavior belongs; the Non-Goal slots are now all rejection surface. |
| — | Only affirmative test is a *form* test (R2 BLOCKER) | **Fixed.** New `## The admission test`: a change must advance a Success Signal and violate no Non-Goal; inheriting `ai_docs/` conventions is necessary and never sufficient. |
| — | `Status: APPROVED` with no version or expiry (R3) | **Not fixed here.** Real, but it is a lifecycle-mechanism question (does an APPROVED Vision expire? does promotion record a version?) that belongs to the doctrine decision below, not to one project's Vision. Named so it is not lost. |
| — | R3's proposed North Star replacement | **Adopted as the base**, then extended (devPNT defined inline, Standalone stated as a rule rather than a mode name). |

## Round 2 — the re-run, and what it says

Feature success signal 1 was **not met**. Same three lenses, same prompts, promoted text;
full evidence in `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md` (`# Round 2`).

What the rewrite bought, verified: all five test proposals now rule **REJECT** against a
quoted line (round 1: three of five). The metering proposal — the M89-class hole, and the
reason this work started — is closed by the Non-Goal written as a rule over the class.

What it cost, and this is the honest part: **the rewrite introduced a defective admission
test.** `"admitted only if it advances at least one Success Signal"` combined with six
signals that are all process invariants means the gate compels REJECT on work the
document plainly wants — supporting an additional agent client, or an ordinary bug fix.
Round 1 had no admission test to be wrong; round 2 has one, and it is wrong in the ACCEPT
direction. Two reviewers found this independently.

Three more BLOCKERs, all real:
- The Vision violates its own new Non-Goal in paragraph two (`"distinguishing capability"`
  is an unfalsifiable superiority claim).
- The Non-Goals never say whether they bind the devPNT layer, so a reviewer must guess to
  rule on any paid-layer proposal — and a working reword (mirror guides into devPNT's
  paid governed storage) passes on the guess that they do not.
- `L1/L2/L3` are undefined here while two Success Signals depend on them.

**Verdict: the Vision is better and not done.** Better is not a figure of speech — the
rejection surface went from leaky to sharp on the exact axis that had already caused a
real incident. Not done is equally literal: a gate that cannot admit is half a gate.

Proposed v2 (targeted edits, NOT another rewrite; requires owner approval because the
document is APPROVED):
1. Fix the admission test — admit what advances a **Goal or** a Success Signal, and make
   the Goals gate-bearing; or add value-delivery signals so the invariant signals stop
   carrying the whole ACCEPT direction.
2. State the scope in one line: this Vision binds every capability shipped under the
   methodology, including anything the devPNT layer adds.
3. `"distinguishing capability"` → `"central mechanism"` (R3's replacement text is
   drafted and quotable).
4. Define the risk levels in one line, or point to where Rule Zero defines them.
5. Fix `"provably faithful"` to claim what a hash actually proves; carve the executing
   agent runtime out of the no-network Non-Goal; move the devPNT capability-parity rule
   out of Actors into a Non-Goal.

## Round 3 — v2 verified, and the root cause

v2 was applied and re-checked with the gate lens plus a new **ACCEPT-side battery** (the
half round 2 showed was broken). Evidence: `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`
(`# Round 3`).

**Closed:** the undefined risk levels, the superiority self-violation, and the ACCEPT
direction for maintenance work — a bug fix and a performance change are now admitted with
no argument, quoting the carve-out.

**Opened by v2, and this is on the fix, not on the reviewer:**
- The scope preamble I added to close round 2's B3 over-reached: bound to *every*
  capability including devPNT's, Non-Goal 4 now forbids devPNT's `governed storage` — the
  first thing the North Star credits it with. The Vision contradicts itself on the paid
  layer.
- Non-Goal 5 (`devPNT may make a capability stronger, faster, governed or reviewable`)
  introduced an undefined `capability` / `amplification` distinction, and **the metering
  hole reopened one level up**: a "devPNT-layer guide attestation, free tier 20/month"
  clears every literal Non-Goal, because the anti-metering rule is scoped to *the skill*
  while the metered outcome lives in the amplification.

**Root cause, stated plainly.** Three Non-Goals (metering, network, paid-layer) are three
attempts to express one commercial principle that the document never writes down. Every
round patches one seam and opens the next, because the words the patches rely on —
`capability`, `the skill`, `amplification`, `user data` — have no shared definition. A
fourth patch round would repeat the pattern.

The positive control from the same review: Non-Goal 6 (fork / vendor / depend) is the one
rule the reviewer *could not* reword around, because its terms are closed and enumerated.
That is the shape the commercial rules need.

**Proposed v3 — structural, and it is a commercial decision, so it is the owner's.**
Replace Non-Goals 3–5 with one stated principle plus its enumerated consequences. Draft
of the principle:

> Everything the methodology produces stays in the user's own repository, readable and
> usable in full without paying anything. devPNT may charge for what it adds *over* that
> data — speed, governance, team sharing, review, analysis — but never for access to what
> the methodology produces, never in a way that counts or caps what a user may produce,
> and never in a way that leaves a document or a capability stranded when devPNT is
> removed.

That single sentence rules the reviewer's attestation reword REJECT (it meters an outcome
derived from the user's own guides) while leaving devPNT's governed storage legitimate
(it adds team-wide governance over data the user still holds in full). It also removes
the need for the scope preamble that caused the contradiction.

Also in v3, smaller: admit Actors into the admission test (multi-client support is
currently undecidable); soften the anti-creep clarification so it stops rejecting
documentation work; place `SKILL.md` with a real path so Signal 1's reader can reach the
triage definition.

**Owner approved the principle**; applied as v3, then corrected by rounds 4 and 5.

## Rounds 4 and 5 — convergence, and where it stands

| Round | Text | Adversarial proposals decidably rejected | Rewords that survived |
|---|---|---|---|
| 1 | 2026-07-02 original | 3 of 5 | metering admissible; work-ledger reword passes |
| 3 | v2 | 5 of 5 (reject side) | 3 rewords pass, incl. metering re-entering via the paid layer |
| 4 | v3 | 7 of 7 | 4 MAJOR rewords; reviewer could not construct a metering bypass |
| 5 | v4 | 9 of 9 | 6 MAJOR rewords; metering **and** work-management both declared unbypassable |

Each round's BLOCKERs were introduced by the previous round's fix, and each was narrower
than the last. Round 5's two — the chargeable list intersecting the never-meter list, and
the first enumerated consequence rejecting the paid layer it was meant to permit — were
both cases of the same class: an absolute stated next to a conditional, with no
precedence. v5 resolves them by scoping the absolutes to what the principle actually
covers, and adds the bundling rule the reviewer used twice to get around it
(*"ask what the user loses by not paying — if it is something they could have done alone,
the proposal is out however it is packaged"*).

**Status of the claim.** Feature success signal 1 is met on the reject side and on most
of the accept side: a cold reviewer with only this document rules decidably on 9 of 9
adversarial proposals and 5 of 6 legitimate ones. It is **not** met unconditionally —
v5's own text has not been blind-checked, and every previous version's fixes opened
something. The honest statement is: the Vision is now hard to get around on the two axes
that matter commercially, and one more round is owed before calling it settled.

## Diary / Current State

**2026-07-27 — rewrite drafted, awaiting owner promotion.** Standalone (devPNT off).
Blind reviewers were run with file/search/web access explicitly forbidden and the
document pasted inline, so a term they could not resolve is a property of the text, not
of their tooling; all three reported zero tool uses.

Level declared: **L3 · router: no match** (the router holds only `GUIDE_release.md`,
which covers publishing).

Honest limits of what is delivered:
- The improvement is **not yet proven**. The blind re-run (feature success signal 1)
  happens after promotion; today the claim rests on the fixes mapping 1:1 onto findings.
- The Vision is **DRAFT**, so this repository currently has no APPROVED Vision at HEAD.
  The previous APPROVED text stays binding via `b35b36e` until the owner promotes —
  stated in the document itself so a cold reader is not misled.
- One finding (APPROVED has no version or expiry) is deliberately left open.

**Doctrine question for the owner (proposed, not implemented).** Should the blind-clarity
check become a step in the skill's Vision lifecycle — required before promoting any
Vision or M-VISION to APPROVED, and re-run when it is amended? Evidence for: it found a
BLOCKER-class hole in an APPROVED document that had passed every existing gate, and the
hole had already caused a real incident (M89). Evidence against: it costs three
fresh-context runs per promotion, and promotion is rare enough that the owner may prefer
to invoke it by hand. My recommendation: **make it required for promotion to APPROVED
and for any amendment of an APPROVED Vision, not for DRAFT edits** — promotion is
exactly the moment authority is granted, and it is rare, so the cost lands where it buys
the most. Not implemented pending the owner's decision.
