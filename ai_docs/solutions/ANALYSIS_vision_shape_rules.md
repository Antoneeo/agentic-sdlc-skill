---
id: F-023
feature: Vision Shape Rules (rules defined by function, not by form)
status: IN_PROGRESS
level: L3
start_date: 2026-07-31
end_date:
---
# Feature Analysis: Vision Shape Rules

## Objective

Two blind rounds run against the v7 Vision amendment (F-022) produced a result larger
than that amendment: **the Vision's prohibitions are largely defined by *shape* — a
form, an enumeration, a location, a named verb — rather than by the question they
answer, the counterfactual they satisfy, or the evasion they foreclose.** The
reviewer's own formulation:

> Everything that defeated the attacker defines the forbidden thing by the question it
> answers, the counterfactual it satisfies, or the evasion it forecloses — all
> properties the proposer does not control. Everything that got through defines by
> shape. **Shape is exactly what a proposer controls, so a shape-based rule is a
> specification for its own bypass.**

F-022 fixed the shape-defined rules its own amendment opened or worsened, by function.
This feature carries the rest — defects that predate the family and were surfaced, with
working attacks, while passing through. They are separated deliberately: rewriting half
an APPROVED Vision inside a consolidation feature would put that rewrite beyond the
reach of the gate it belongs to, and would make the blind battery test a wholesale
rewrite instead of an amendment.

## Feature Vision

**Expected benefit.** A Vision whose prohibitions cannot be bypassed by a competent
proposer restating the same capability in a different form. Today they can: eleven
attacks have been demonstrated across two rounds, all honest, several using the
document's own approving vocabulary.

**Alignment.** `project_vision.md` exists to be *operable* — the Goals name making the
project's intent "readable and *operable* by an agent that arrives with no context" and
making divergence visible before implementation. A gate that admits what it means to
forbid does not do that. This feature changes no capability of the product; it changes
what the gate can rule.

**Actors.** Served: **Team lead needing governance** (a gate that rules the same way
twice is what "divergence surfaced before the change is merged" requires). The work is
governance-internal, so the **Skill maintainer** feature-local cast of F-022 applies
here too — author the doctrine, run the battery.

**Non-goals.**
- **Not** re-opening what the Vision decides. Every prohibition keeps its intent; only
  the way it is stated changes. A rewrite that changes an outcome is out of scope and
  goes back to the owner as a separate decision.
- **Not** adding prohibitions. Two findings below propose new clauses (re-admission on
  scope growth; a gate on amendments); each is a *closure of an existing rule's
  bypass*, and each is disclosed as an addition under the ceremony budget.
- **Not** promoting the Vision. Promotion stays the owner's, after a blind round.

**Success signals.**
- The eleven attacks in the standing battery are re-run against the rewritten text and
  none gets through — or those that do are documented as accepted residuals with the
  reason.
- No accept-side item in the battery is wrongly rejected (the gate does not become
  reject-only, which is the failure mode the current double default already produces).

## Use Cases / User Needs

| # | Actor | Use case |
|---|---|---|
| UC1 | Team lead | The same proposal gets the same ruling from two different readers, so the gate is a control rather than a coin-flip. |
| UC2 | Team lead | A capability admitted narrowly cannot grow past its admission without being ruled on again. |
| UC3 | Skill maintainer | A new prohibition can be tested before it ships: the battery holds every attack that ever worked, with its class. |

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| rule a proposal admissible or not | EXISTS | `project_vision.md` `## The admission test` | re-read: the test is stated and has decided six rounds of battery items |
| rule the same way twice | INADEQUATE | same document: two mutually exclusive defaults for unreached proposals | "Anything this document does not reach is out until it does" (default-deny) vs "admitted only if it advances at least one Goal, Actor commitment or Success Signal … and violates neither a Non-Goal nor the user's guarantee" (admit-on-advance). Demonstrated: the F-022 consolidation and a knowledge sibling are ADMIT under one sentence and REJECT under the other. |
| re-rule a capability whose scope grew | MISSING | — | searched `project_vision.md` for re-admission, scope growth, extend, widen: the admission test governs "proposals that add or change what the product does", and "maintaining a capability the product already has needs no admission" — so a narrow admission followed by an extension is exempt at step two. No clause reaches it. |
| keep the exemption from being self-declared | INADEQUATE | `## The admission test`, the exemption sentence | the anti-laundering clause closes exactly one framing ("a fix to something that should never have shipped") and leaves "improving performance" and "maintaining a capability" unbounded and self-asserted |
| gate an amendment to a stated fact | MISSING | — | "the same change amends this Vision, or it is not accepted" requires an amendment to *exist*, and imposes no ruling on it: an amendment may be bundled with the capability it authorises, so every stated fact is soft |
| state a prohibition so its form cannot be varied | INADEQUATE | the Non-Goals | fifteen residual shape-defined rules enumerated by the round-2 blind reviewer; four have working attacks |
| hold every attack that ever worked | EXISTS | `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md` | re-read: the standing battery now carries eleven attacks with their classes, added by F-022 |

### Components

**C1 — One default for unreached proposals.** The catch-all is scoped to the
prohibitions rather than to everything: a capability operating in a Non-Goal's
territory is out unless the document reaches and admits it; everything else is ruled by
the admission test. Removes the coin-flip without making the gate reject-only.

**C2 — Re-admission on scope growth.** Widening what a capability governs is itself a
new or changed capability, ruled against every part of the product that already governs
the work it would reach.

**C3 — A bounded exemption.** "Maintaining" is defined: the capability's stated purpose,
actors and surface unchanged. If the product can do something it could not do before,
it is a new capability whatever it is called.

**C4 — Amendments ruled on their own.** An amendment to a stated fact is its own
proposal, ruled first and separately; it may not be bundled with the capability it
enables, and Non-Goals are not amendable by a capability proposal.

**C5 — Function-restatement of the residual shape rules.** Each remaining rule restated
by the question it answers or the counterfactual it satisfies. The list is the
`residual_shape_rules` section of the round-2 blind review; the manifest carve-out, the
ceremony-form enumeration and the "advances a Goal" test are the three with the widest
openings.

**C6 — Disclosure by proximity.** A proposal discloses, for every Non-Goal its subject
matter approaches, the fact that determines whether it crosses — replacing the current
two-item enumeration (metering; mandatory artifacts), which leaves sibling claims,
work-management proximity and format coupling with no disclosure duty.

## Impact

| Path | Change | Why |
|---|---|---|
| `ai_docs/vision/project_vision.md` | MODIFY | C1-C6; the residual shape rules restated by function |
| `ai_docs/audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md` | MODIFY | the round's result and any new attack it produces |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | MODIFY | one row per blind round |

No code changes, no validator changes, no skill-file changes. The Vision is prose with
no mechanical enforcement, so the blast radius is the document and the batteries that
test it. `sdlc_check.py` reads the Vision only for its presence and `Status:` line
(`VISION_FILES`), which this feature does not touch.

## Security and Threat Model

| # | Threat | Mitigation |
|---|---|---|
| T1 | A restatement silently changes an outcome the owner already decided — the rewrite becomes a re-decision wearing an editorial disguise. This is the real risk of a "clarity" pass on a binding document. | Every rewritten rule is re-run against the standing battery, whose items carry their historical verdicts: an item that flips from REJECT to ADMIT, or the reverse, is a decision and goes to the owner explicitly rather than shipping inside a wording change. |
| T2 | The rewrite closes bypasses by making the gate reject-only, which is the failure the accept-side battery exists to catch and which the current double default already produces. | The battery's accept-side items are part of the pass criterion, not a courtesy; a wrongly rejected accept-side item is a BLOCK. |
| T3 | New prohibitions (C2, C4) enter without a ceremony-budget disclosure, i.e. the feature violates the Non-Goal it is trying to make enforceable. | Each addition states which level it lands on and what it removes, per the budget clause, and goes to the owner for explicit acceptance. C2 and C4 land on the admission test — proposals to change what the product does — and never on L1. |

No external input, authN/authZ, cryptography, network, personal data or filesystem
surface: the change set is one Markdown document and two audit records.

## Action Plan

- [ ] Restate C1-C4 (the four with demonstrated attacks or demonstrated ambiguity).
- [ ] Restate C5's list, worst openings first.
- [ ] C6 disclosure rule.
- [ ] Blind round: the full standing battery (eleven attacks, all accept-side items),
      no repository access, a reviewer that has not seen the rewrite's rationale.
- [ ] Surface any flipped verdict to the owner as a decision, not as an edit.
- [ ] Owner promotion decision.

## Test Strategy

The Vision has no mechanical validator, so its tests are the batteries:

| # | Test | Asserts |
|---|---|---|
| TS1 | Standing battery, reject side: the eleven recorded attacks, re-thrown at the rewritten text. | UC1 — the bypasses are closed by function, not by wording |
| TS2 | Standing battery, accept side: consolidation, a knowledge sibling, one more client, a validator bug fix, a renamed heading. | T2 — the gate did not become reject-only |
| TS3 | Verdict diff: every battery item's ruling compared to its ruling before the rewrite; any flip is reported to the owner. | T1 — no silent re-decision |
| TS4 | A fresh reviewer, no rationale, asked for NEW attack classes. | UC3 — a rule that only survives the attacks it was written against has not been tested |

## Diary / Current State

- **2026-07-31 — opened, from F-022's blind rounds.** Round 1 (gate lens, 8 items)
  returned PASS-conditional with 4 successful rewords; round 2, run against the
  corrected text, returned **FAIL with the same four classes plus seven new ones**.
  F-022 fixed what its own amendment opened; this feature carries the rest. The
  decisive observation is the reviewer's anatomy note, now the organising principle
  here: rules that defeated every attack define by question, counterfactual or
  foreclosed evasion; rules that fell define by shape.
- **2026-08-01 — C1–C4 + C6 drafted as the v8 amendment** (commit `c750668`), Status
  line marks it PENDING the blind check; the v7 text binds until promotion. C1 one
  scoped default (silence in Non-Goal territory is a NO; silence elsewhere is the
  admission test's question); C2 re-admission on scope growth (purpose/actors/surface);
  C3 the exemption bounded ("maintaining" = all three unchanged; can-do-something-new =
  new capability whatever it is called); C4 amendments ruled first and apart, Non-Goals
  never amendable by a capability proposal; C6 disclosure-by-proximity folded into the
  disclosure paragraph. **Blind round launched** on the full v8 text (one-file read,
  nothing omitted — the Round-9 instrument error is the reason the file is complete):
  8 recorded attack classes re-thrown, 6 accept-side items, new-class hunt, verdict-diff
  duty (any flip goes to the owner as a decision, per T1).
- **2026-08-01 — blind round on the v8 draft: PASS-conditional.** All eight recorded
  attack classes stopped (metering-as-fix triple-stopped; the readiness board by the
  v7 aggregation clause verbatim; scope growth re-ruled then killed by Non-Goal 1;
  the bundled amendment twice; the paid sibling by the scope appositive; the
  offline-mode "perf" change by the effect backstop; silence-near-a-Non-Goal by
  omission-resolves-against; the best restatement by the question-not-form rule).
  All six accept-side items ADMIT — the gate did not go reject-only. **Zero verdict
  flips.** One BLOCK: the effect backstop, read literally, refused every bug fix
  (fixing makes the product able to do what it could not — reject-only defect, not a
  bypass). Nine MAJOR, all wording inside the new clauses: the backstop bounded to
  kind and made bidirectional (degradation no longer rides the exemption); the
  scope-growth triple made instances-not-list; the exemption's baseline given a
  locus (recorded, else narrowest reading, proposer's burden); disclosure keyed to
  what ships rather than the proposal's self-description; "ruled apart" required to
  stand with the capability withdrawn; the scoped default's override narrowed to the
  rule itself; the manifest/aggregation overlap given an explicit discriminator; the
  owner-acceptance disclosure path restored; Provenance dated correctly and
  superseded-draft narrations marked as not-current-text. **All ten fixes applied
  same-day.**
- **Open before promotion:** C5 — the fifteen residual shape rules (Round 9 lists
  them; three named worst: the manifest carve-out — now partly addressed by the F8
  discriminator — the ceremony-form enumeration, the "advances a Goal" test). Round
  9's warning applies: fixes introduce new shapes, so C5 is a careful pass. Then a
  confirming blind round on the fixed text (the Round-8 lesson: fixes written
  against seen attacks fall to rewords), and the owner's promotion decision.
