---
description: F-049 - the floor reaches the author. F-048 bound the gates and the dispatched subagents but never the orchestrator session that AUTHORS, which by the floor's own criterion is the purest deep-tier role; this unit adds the session rule, the no-double-below-floor constraint, and the user-facing guidance on which tier to set.
status: COMPLETED
end_date: 2026-09-11
feature: F-049
id: F-049
start_date: 2026-09-10
level: L3
branch: main
---
# ANALYSIS: The Floor Reaches the Author (F-049)

**Level: L3 · router: no match** (catalogue: `GUIDE_release.md` only).
Elicitation: skip path — the spec is the owner's question of 2026-09-10 ("an agent invoking the skill from a user-set model: how does it behave, and which model should the user set?") and the gap that question exposed in F-048, shipped the same day. Probes: `harness_authoring_floor/probe.py`.

## Precedent placement

**Scope growth of r20, therefore re-ruled as new** (r4: "widens an admitted capability
to reach more work … re-ruled as new"). Distinction line, falsifiable: *r20 constrains
a rung the AGENT chooses at a gate, where routing is the remedy; this constrains the
session the USER chose before the agent existed, where routing is impossible and the
only remedies are disclosure and compensation.* An agent cannot re-tier itself
mid-session, so the two capabilities cannot share a rule. → new row, pending the
ceremony decision below.

## Ceremony budget

The unit adds no field (it reuses `model`, shipped in F-048) and no artifact. It adds
**one conditional disclosure at L3 authoring** — fired only where the session can
determine its own tier and that tier is below the authoring floor — plus the
constraint below, which forbids a state rather than requiring an act. L1 and L2 pay
zero. Nothing of comparable cost is removed, so this is the disclosure and the owner's
acceptance is owed before the rule ships.

## Objective

F-048's floor is titled "which tier may run this **gate**" and its table names review
roles, a light conformance pass, and dispatch roles. It never names the orchestrator
session — the one that authors the ANALYSIS, the Vision, the use cases and the threat
model. By the floor's own criterion that is the purest deep-tier role (judgement whose
wrongness no check can see), and `dispatch.md`'s never-list forbids moving it
elsewhere, so the session's own capability IS the capability of that work. Today the
doctrine constrains the reviewer that catches the omission and not the author that
makes it.

## Vision Alignment

Same north star as F-048, one layer earlier: an under-tiered author does not produce a
wrong answer so much as **silently fail to apply the process** — a triage never run, a
router verdict declared without the lookup, a Vision Gate not noticed. That failure is
invisible to every mechanical check the skill has, which is precisely the definition
the floor uses. Non-Goals run: the ceremony ratchet (disclosed above, acceptance
owed); no provider name enters shared doctrine (the READMEs are the user-facing
exception and are versioned per release, not doctrine); r3's work-management territory
is untouched (nothing is ordered, scheduled or assigned).

## Use Cases / User Needs

- **UC1 — the agent authoring an L3 artifact from a session the user under-tiered.** After: where it can determine its own tier, it says so before authoring rather than producing a confident artifact nobody flags.
- **UC2 — the owner choosing a model before starting.** After: the READMEs state the criterion (a session's floor is the highest floor among the roles it performs itself) and what that means for a design session versus an execution session.
- **UC3 — the reader of a review log.** After: where authoring ran below floor the row's `reviewer` cell carries that fact beside the review's own tier, so a human reading the row sees both halves. It is free text, readable and not parseable — stated rather than dressed as a check.

## Functional Spec

1. **The session rule** (in `review.md`, beside the floor it extends): a session's floor
   is the **highest floor among the roles it performs itself**. Authoring a governed
   artifact is a deep-floor role. Fails open, and says so: an agent that cannot
   determine its own tier owes nothing — the rule binds disclosure, never a capability
   the agent cannot acquire.
2. **Discouraged, not forbidden: both below the floor on one unit.** Where the
   authoring session ran below floor, the review's floor becomes non-negotiable —
   **except where no rung at or above the floor exists at all**, which is the case
   *When independence and capability conflict* already governs: there the review
   still runs, both disclosures are recorded, and the result is the worst admissible
   state rather than a violation. Forbidding it outright would contradict that
   arbitration and push the agent toward the abstention it explicitly rejects.
   Visibility is bought with **existing cells** — the disclosure is repeated in the
   review row's `reviewer` cell (Hybrid: `notes`) — because the log has no column for
   the authoring session's tier and promising "checkable in the log" without one was
   an unkeepable claim.
3. **User-facing guidance** in the three `README.md` (each is that package's npm front
   page): which kind of session wants which tier, stated as the criterion plus worked
   examples, with the explicit note that the reviewer subagent's tier is **not
   inherited** from the session and must be set deliberately.
4. Non-changes: no new column, no new check, no exit code, no command.

## Capability Ledger

All capabilities EXIST. The floor and its vocabulary (`review.md`, F-048), the `model`
column and its value set, the arbitration's disclosure idiom (`below floor: <reason>`),
the three READMEs as the user-facing surface, the shared-battery pinning pattern. One
line: this unit adds a row and a paragraph to a table F-048 built, and three README
sections; nothing is constructed.

## Impact

| Path | Change | What |
|---|---|---|
| `review.md` **(spine, port ×3)** | MODIFY | the authoring row in the floor table; the session rule; the discouraged-combination clause WITH its arbitration exception; the fail-open clause and the honest statement of the rule's reach |
| `SKILL.md` (code lens) | MODIFY | a pointer at the head of Standalone L3 — the rule binds BEFORE authoring, and `review.md` is not loaded until the design-review gate, one phase too late |
| `README.md` ×3 **(per-package, npm front page)** | MODIFY | the tier-selection guidance for the user, including the non-inheritance of the reviewer's tier |
| `scripts/test_skill_invariants.py` **(shared battery)** | MODIFY | pin the authoring row, the session rule and the forbidden state; keep F-048's ≥2-role-row pin satisfied |
| `vision/rulings.md` | MODIFY | the re-ruled row with its distinction line from r20 |
| `harness_authoring_floor/probe.py` | ADD | P1-P5, with each probe's class labelled |
| closure artifacts | ADD/MODIFY | ADR, HANDOFF, REVIEW_LOG rows, generated manifests |

Blast radius: `review.md` is shared spine — three copies plus `shared_files.py --update`
×3. The floor table gains a row, so F-048's parsing assertions (`≥2 role→tier rows`,
the declared value set) must still pass; the harness re-runs both. No script reads the
floor, so there is no machine consumer beyond those pins.

## Security and Threat Model

No code path, no input parsing, no new execution. The surface the first draft
analysed — READMEs naming concrete provider models, mitigated by dating each
mention — **was claimed and never used**: the shipped guidance names no provider
and carries no date, so both the risk and its mitigation are moot. What replaces
it as the residual is plainer and worse for the reader: *"your strongest model"*
is unactionable for a user who does not know their own ladder, and the skill
deliberately refuses to name one for them.

## Action Plan

1. Harness RED.
2. Owner's ceremony decision on the conditional disclosure.
3. Author `review.md`, the three READMEs, the battery pins; port ×3.
4. Harness GREEN, three batteries, drift guard.
5. Design review, then closure review.
6. Closure: rulings row, ADR, REVIEW_LOG rows in the F-048 schema, registration.

## Test Strategy

Honest about what each probe buys, because three units in this sequence shipped a
probe that could not fail. **Real structure**: P1a/P1b parse the authoring role as
a TABLE ROW (prose does not satisfy them), P4 keeps F-048's floor parse alive, P5
is cross-distribution byte identity. **Wording anchors, labelled as such in the
file**: P1c, P1d, P2a, P2b, P2c, P3a, P3b — they catch deletion and drift, not
meaning; a README gutted around the pinned phrases stays green, and the harness
docstring says so. P3a anchors on the section HEADING rather than the word "tier",
because kb's README has a pre-existing "licence tier" that kept a looser check
green when the section was deleted from that lens alone.

Not claimed: that the READMEs agree with the spine's value set. They do not name
`light` or `economy` at all, deliberately — the user-facing text gives a criterion,
not a vocabulary.

## Diary

- **2026-09-10 — opened.** Driver: the owner asked how an agent invoking the skill from a user-set model behaves, and which model to set. Grounding it against the real `review.md` showed F-048's floor is titled "which tier may run this gate" and names only gate and dispatch roles — the authoring session is absent, though it is the role the floor's own criterion describes most exactly. Not a defect in F-048's implementation (it did what its design said); a gap in that design's scope, found the day it shipped by a question about use rather than about code.
