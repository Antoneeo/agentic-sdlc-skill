# Blind-reviewer clarity check — `vision/project_vision.md` (2026-07-27)

Evidence for F-017 (`solutions/ANALYSIS_vision_clarity.md`). Three reviewers, fresh
context, **no project knowledge and no repository access** — each received only the
verbatim text of the APPROVED Vision (`git show b35b36e:ai_docs/vision/project_vision.md`)
and was explicitly forbidden to open, search or look up anything. Their inability to
resolve a term is therefore a property of the document, not of their access.

Why this test exists: the Vision's operational purpose is to be read cold — by a later
session, by a reviewer, by another agent — and ruled on. It had never been tested that way.

| Lens | Question put to the reviewer |
|---|---|
| **R1 — comprehension** | Read it as a newcomer: what is this product? What could you not resolve from the text alone? |
| **R2 — gate operability** | Rule ACCEPT/REJECT on five candidate proposals using only this document. Where does it fail to decide? |
| **R3 — durability** | How will this document rot? What depends on a moving target, what is unfalsifiable, what is a time bomb? |

## Convergence (found independently by more than one reviewer)

| # | Finding | Found by |
|---|---|---|
| 1 | `superpowers` never defined, yet load-bearing in 3 of the 4 layers | R1, R2, R3 |
| 2 | The document never states what the product *is* or *does* functionally | R1, R3 |
| 3 | `best-in-class` is unfalsifiable and is both North Star and Success Signal — a closed loop | R1, R2, R3 |
| 4 | No Non-Goal covers metering / quotas / paywalls; a "cap free guides per month" proposal is **admissible on the literal text** | R2 (decisive) |
| 5 | Success Signal 1 ("name the layer for any capability") already fails inside the document — guides appear in layers A, C and D | R1 |
| 6 | Substance delegated to files a cold reader cannot open (`capabilities_and_positioning.md`, `milestone_vision_operative_guides`) | R1, R2, R3 |
| 7 | 3 of 4 Success Signals are not measurable at six months | R2, R3 |
| 8 | `Its 6.0.x frontier` pins Layer C to a competitor's release window | R1, R3 |
| 9 | `zero capability loss without devPNT` has two incompatible readings | R1, R2 |
| 10 | `Never hide a conflict…` is a behavior rule occupying one of only four Non-Goal slots | R1, R2 |

## The decisive finding (R2)

R2 ran five candidate proposals against the document. Two were undecidable:

- **P4 — "cap how many operative guides a free user can create per month."**
  Ruling: **CANNOT DECIDE, admissible on the literal text.** No Non-Goal covers
  rationing; `"start free and Standalone"` is exactly how a metered product describes
  itself; and Success Signal 3 (`"Feature B ships the reusable operative-guide layer"`)
  is satisfied by a capped implementation — it measures existence, not usability.
- **P1 — "paid-only cloud document store, read-only unpaid."** Same axis: every
  anti-paywall constraint is bound to the *proper noun* devPNT, not to paywalling as a
  class, so a proposal under a different name is untouched by all four quotes.

R2's own words on the mechanism: *"a Vision whose central commercial constraint is
written as a proper noun rather than a rule is bypassed by renaming."*

R2 also demonstrated a **reword that passes the gate**: "issue tracker with sprint
boards" rewritten as *"a durable work-item ledger under `ai_docs/`… it inherits
`ai_docs/` frontmatter, manifest and lifecycle… this is Layer C parity work"* — admitted,
because the qualifier in `"Not a **full** ALM"` grants the exemption, Layer C itself
lists `"durable progress ledger"` approvingly, and **the only affirmative admission test
in the document is a test of form, not of substance**.

This matters beyond theory: the same hole was exploited in practice on M89, where
internal-KB metering entered the design artifacts with no Non-Goal to catch it. The
blind reviewer rediscovered it from the text alone, with no knowledge of that incident.

## R1 — comprehension, notable findings

- BLOCKER: cannot tell what the artifact IS — `"methodology skill"` is used as a product
  noun and never unpacked. A newcomer cannot say what they would install or run.
- BLOCKER: `"mechanical enforcement"` is one unexplained noun phrase that everything
  downstream depends on.
- 24 terms could not be resolved from the document itself; `Feature A`, `Feature B`,
  `the backlog` and `the evolution roadmap` are used as *commitments* while living
  entirely outside the text.
- MAJOR: `"one capability neither has"` — "neither" takes two, four layers were just
  listed; and Layer D is simultaneously called `"The original layer"` (i.e. ours).
- BLOCKER (contradiction): Layer D's lodestar is `milestone_vision_operative_guides`,
  which reads as a devPNT-stored record — so the governing artifact of the one layer
  "nobody has" is unreachable to a Standalone user, contradicting `"zero capability loss
  without devPNT"`.
- BLOCKER (self-defeating signal): Layer A has to defend itself parenthetically —
  `"(distinct from Layer D's user-indication operative guides)"` — while sharing the
  `"same reference/GUIDE_ machinery"`. A taxonomy needing a disclaimer to stay apart is
  already failing the signal that asks users to name the layer.

## R3 — durability, notable findings

- BLOCKER: three of four layers are defined as functions of another project's state; if
  superpowers is renamed, archived or simply not findable in 2028, more than half the
  product thesis becomes unreadable **and nothing in the document signals that it
  happened**.
- BLOCKER: `"Its 6.0.x frontier"` breaks twice — superpowers moves past 6.0.x (Layer C
  then describes history while claiming to describe direction), and the five imported
  feature names become unresolvable jargon.
- MAJOR, will silently become false without anyone editing: `"D — What nobody has"`
  (unverified universal negative), `"matched or leapfrogged"`, and Success Signal 3,
  whose success is contingent on a competitor's roadmap.
- MAJOR: `"an optional **paid** amplifier"` states a commercial fact inside a Vision;
  any pricing change makes the document false and the Actor built on it fictional.
- MAJOR: `Status: APPROVED` with no version, no re-review trigger and no expiry — every
  aging claim sits under a permanent approval banner, which is what makes stale claims
  dangerous rather than merely wrong.
- Its proposed North Star replacement was adopted as the base for the rewrite.

## Disposition

All ten convergent findings are addressed in the rewrite of
`vision/project_vision.md`; the mapping finding → fix is in
`solutions/ANALYSIS_vision_clarity.md` (`## Findings and disposition`). Nothing was
dismissed silently: findings not acted on are named there with the reason.

---

# Round 2 — same three lenses, promoted text (2026-07-27)

Run against the APPROVED rewrite, same prompts, three fresh reviewers, same no-access
rules. **Verdict: FAIL again — but a different class of failure.** The rejection surface
now works; the admission surface does not.

## What round 1's findings bought

| Round-1 finding | Round-2 result |
|---|---|
| P4 metering admissible | **REJECT**, quoting `"Nothing about the skill is ever metered, capped, tiered"` |
| P1 paid cloud tier admissible | **REJECT** (contingent — see B3) |
| P2 / P3 / P5 | REJECT, verbatim, "no interpretation" |
| Only affirmative test was a form test | An admission test now exists — and is itself defective (B1) |
| `best-in-class` unfalsifiable | Gone — but replaced by a smaller self-violation (B2) |

All five proposals are now decidable in the reject direction (round 1: three). The
decisive M89-class hole is closed.

## New BLOCKERs — introduced or exposed by the rewrite

**B1 — The gate can REJECT but cannot ACCEPT.** *(R2 BLOCKER, R3 MAJOR — independent)*
`"admitted only if it advances at least one Success Signal below"`, but all six signals
are **process invariants**, not delivered value. R2's counterexample: *"support the
process on an additional agent client"* — something the document explicitly wants
(`"on whatever clients the team uses"`) — advances no signal, so the stated test compels
REJECT. R3's: an ordinary bug fix advances none either. R2: *"a gate that produces the
wrong answer on the product's own roadmap is not operable in the ACCEPT direction."*
This defect was **introduced by the rewrite** — it did not exist in round 1, because
round 1 had no admission test at all.

**B2 — The document violates its own new Non-Goal in paragraph two.** *(R1, R3)*
`"Its **distinguishing capability** is the operative guide"` is a comparative superiority
claim with no named comparator, in a document whose Non-Goal reads `"No unfalsifiable
claim of superiority in this document."` R3: *"The Vision breaks its own gate in its
second paragraph."*

**B3 — Scope of the Non-Goals is undefined: do they bind the devPNT layer?** *(R2)*
`"No capability may require the network"` is unscoped; `"Nothing about the skill is ever
metered"` is scoped to the skill; devPNT is `"a separate product"`. R2 had to **guess**
to rule P1, and states a different reviewer guessing the other way rules ACCEPT. R2's
working reword: mirror approved guides into devPNT's governed cloud storage, paid,
free tier read-only — claims Signals 3 and 5 verbatim, invokes the North Star's own
blessing of devPNT, and the skill-scoped metering Non-Goal is satisfied *by construction
because the capability never existed in the skill*.

**B4 — L1 / L2 / L3 are undefined here while two Success Signals depend on them.**
*(all three)* The North Star is binary (`"trivial"` / `"significant"`); Signals 4 and 5
are ternary (`"Every L2/L3 declaration"`, `"A full L1→L3 change"`). A cold reader cannot
check either. R3: `"the document mandates enforcement of a line it declines to draw."`
Pre-existing, but the rewrite made it load-bearing by citing the levels in the signals.

## MAJORs worth acting on

- **The five Goals are inert.** The admission test cites only Signals and Non-Goals, so
  Goals carry no gate force. A proposal advancing Goal 3 (surface conflicts) maps to no
  Signal and is formally inadmissible. *(R2, R3)*
- **`"Guides are provably faithful"` overclaims.** A hash proves the *source is
  unchanged*, not that the guide ever described it correctly. A guide wrong on day one
  stays "provably faithful" forever. *(R3)*
- **Signal 1 is a universal donor.** Almost any documentation-touching proposal can claim
  cold-start operability — including a proposal to rewrite the Vision itself. The
  positive half of the test is cheap to satisfy. *(R2)*
- **Signal 4 is unfalsifiable as written** — no artifact, no location, no checker named,
  unlike Signals 2/3/5. *(R2)*
- **Runtime contradiction.** `"no service, no account, no network"` while the methodology
  is executed by an agent that is itself a networked, account-gated, usually paid
  service. Read literally, the Non-Goal rejects the product. *(R3)*
- **The anti-paywall parity rule lives in Actors, not Non-Goals** (`"adopting or dropping
  devPNT costs no capability in either direction"`) — formally inert at the gate, and
  literally false as written since dropping devPNT does cost devPNT's capabilities. *(R2, R1)*
- **`"the skill"`** first appears with a definite article and no antecedent, yet carries
  an absolute Non-Goal. *(R1, R3)*
- **Header is process archaeology** — `F-017`, a short SHA, two audit paths — unreachable
  by the very cold reader Signal 1 posits, and it will accrete on each revision. *(R1, R3)*

## Reading of this result

Round 2 is not a regression: the hole that had caused a real incident is shut, and every
test proposal is now decidable against a quoted line. But the rewrite traded a *missing*
admission test for a *wrong* one, and a large unfalsifiable claim for a small one. The
honest status is **the Vision is better and still not done** — the fixes belong in a
focused v2, not another rewrite.

---

# Round 3 — v2 text, gate lens, with an ACCEPT-side battery added

Round 2 showed the gate could reject but not admit, so round 3 added five proposals the
document plainly *wants* (A1 multi-client, A2 bug fix, A3 glossary, A4 perf, A5 optional
review) alongside the six reject-side ones. Same no-access rules.

## Closed by v2

- **B4 levels** — L1/L2/L3 now glossed in the North Star. No longer raised.
- **B2 superiority self-violation** — `distinguishing` → `central mechanism`. No longer raised.
- **B1 ACCEPT direction, partially** — the maintenance carve-out works cleanly: A2 (bug
  fix) and A4 (performance) are admitted with no argument, quoting *"needs no admission —
  it is authorized by the capability it serves."* A5 (optional review) admitted on Goal 3.

## Still open, and newly opened by v2

**B5 (NEW, BLOCKER) — Non-Goal 4 forbids the paid layer the North Star sells.**
The v2 scope preamble (`"They bind every capability shipped under this methodology,
including anything the devPNT layer adds"`) plus `"No capability may require the network,
a remote service, or user data stored outside the user's own repository"` makes devPNT's
`"governed storage"` — the first thing the North Star credits it with — a Non-Goal
violation. *"Either the North Star is wrong or Non-Goal 4 is."* The gate cannot rule on
any devPNT proposal. **Introduced by the v2 scope line**, which fixed round 2's B3 by
over-reaching.

**B6 (NEW, BLOCKER) — `capability` vs `amplification` is undefined and load-bearing.**
Non-Goal 5 forbids a capability existing only in the paid layer while permitting devPNT
to make one `"stronger, faster, governed or reviewable"`. Every paid feature can be
framed either way and the proposer picks. **The metering hole reopens one level up** —
reviewer's reword:

> *"devPNT-layer guide fidelity attestation: the skill keeps creating and hash-checking
> guides offline, unlimited and unchanged. devPNT additionally attests guides against
> their source and publishes team-visible attestations; the free devPNT tier attests 20
> guides/month."*

Non-Goal 3 is scoped to `"Nothing about **the skill**"`, so attestation is out of its
reach; Non-Goal 5 pre-authorizes it (`"governed or reviewable"`); Signal 5 is untouched.
*"v2 closed metering of the skill, not metering of the paid amplification of the same
outcome."*

**A1 multi-client — CANNOT DECIDE (should be ACCEPT).** Its only support is an Actors
line (`"on whatever clients the team uses"`), and the admission test cites only Goals and
Signals. Worse, the v2 runtime carve-out argues the other way: `"which client the user
runs … is not something this product ships."`

**A3 glossary — undecidable both ways.** The v2 anti-creep clarification (`"A change that
edits a document is not thereby advancing cold-start operability"`) gives a one-line
REJECT to the documentation work this product is made of.

**MAJOR — three scope nouns for one boundary**: the preamble binds *"every capability
shipped under this methodology"*, Non-Goal 3 binds *"the skill"*, Non-Goal 5 binds
*"capability"*. None defined, and the narrowest governs the anti-metering promise.

**MAJOR — no capability inventory**, so the maintenance exemption has no edge: a cold
agent cannot tell exempt maintenance from an admission-requiring addition except by the
proposal's own verb.

**MAJOR — Non-Goal 1 contradicts Goal 2.** `"Tracking work is somebody else's product"`
sits beside a Goal requiring plans, closure state and handoff to stay synchronized and
versioned. Reviewer's reword 2 walks a work ledger through as an operative guide and
argues it is *required* by Goal 2.

**MAJOR — Signal 1 self-defeating.** It posits a reader with only `ai_docs/`, then
`## Where the rest lives` puts the L1/L2/L3 definition in `SKILL.md`, which the document's
own path rule (`"relative to ai_docs/"`) does not place inside `ai_docs/`.

**MINOR** — `"user data"` undefined (bites a hash cache); Non-Goal 7 has no channel to
fire through; Status, v1 and v2 all bear the same date and author, so a cold reader has no
signal of how settled the text is.

## Reading of this result

Three rounds, converging but not converged. The pattern is now legible: **each round
patches a symptom and the patch opens the next hole**, because three separate Non-Goals
(metering, network, paid-layer) are trying to express one underlying commercial principle
that the document never states. Until that principle is written once, `capability`,
`the skill`, `amplification` and `user data` will keep being the seams a proposal slips
through. The next move is structural, not another patch — see the ANALYSIS.

One reviewer finding is worth keeping as a positive control: Non-Goal 6 (fork/vendor/
depend) is *"the only Non-Goal in the document whose terms are closed"* — the reviewer
tried and could not construct a reword. That is what a working rule looks like.

---

# Round 4 — v3 text, gate lens, with the earlier rewords fired back at it

The reject-side battery was loaded with the four rewords that had defeated v1/v2, plus a
six-proposal ACCEPT battery.

## The core result

**All seven reject-side proposals were rejected on literal text**, including every
reword that previously got through:

- P4 (devPNT attestation, free tier 20/month) → REJECT on `"mirroring, attesting,
  indexing or summarizing one's own repository is such an outcome, and putting it behind
  a counter is metering under another name"`. The reviewer noted the gate splits it
  correctly: team-visible publishing is chargeable, the counter is fatal.
- P5 (work ledger dressed as an operative guide) → REJECT on the work-vs-intent line.
- P6 (`intent:` field on every commit) → REJECT; the "it's a field, not a step" defence
  is pre-named verbatim. *"Cleanest rejection in the battery."*
- P7 (vendor the dispatcher) → REJECT.

**The reviewer could not construct a metering reword.** Their words: blocked *"three
times over: the verb list, the volume bullet, and 'not by a component that does not
exist yet'. I could not word a cap that survives."* Same for the ceremony rule. That is
the outcome this whole exercise was for.

## What v3's own wording opened (all fixed in v4)

- **F1 BLOCKER** — `"hosted copies"` was listed as chargeable while `"mirroring"` was
  listed as never chargeable. A hosted copy is a mirror; the passage claiming to be
  *"a question with an answer"* gave opposite answers to the same question.
- **F2 BLOCKER** — `"removing devPNT never strands … a capability"` was unqualified, so
  it forbade every devPNT-exclusive capability — i.e. the paid layer the same section
  authorizes.
- **F3 BLOCKER** — the Non-Goals never named their subject. The guarantee names devPNT
  repeatedly; the Non-Goals name no one, so "sprint boards, but inside devPNT" escaped.
- **F5 BLOCKER** — Signal 1 posits a reader with only `ai_docs/`, while v3 explicitly
  routed the L1/L2/L3 definitions to `SKILL.md`, *"not under `ai_docs/`"*. The gate's own
  vocabulary was unreachable by the reader the gate simulates.
- **S-1 reword (BLOCKER)** — per-document `PLANNED | IN_PROGRESS | COMPLETED` plus a
  manifest view sorted by status reconstitutes work tracking out of approved material.
  Sharp, because that is what this project already does: the Non-Goal as written
  contradicted the live product.
- MAJOR: the work-record test was not marked conjunctive or disjunctive; efficiency work
  had no anchor (`"performance"` undefined, no Goal measuring the agent's reading cost);
  North Star said the skill lives *"in the project's own repository"* while `## Where the
  rest lives` put it in the agent's skills directory.

## v4 disposition

Every item above is closed in v4: `hosted copies` removed from the chargeable list and
the dividing-line question re-stated as *could a **single** user get this from their own
data*; a fourth consequence added saying plainly that multi-person capabilities DO go
away with devPNT and that this is the paid layer working, not stranding; the Non-Goals
given an explicit subject (*"the product as a whole — the skill and anything the devPNT
layer adds"*); the L1/L2/L3 boundaries stated in the Vision itself; the work-management
test marked disjunctive with per-document progress explicitly permitted and aggregation
into a queue/board explicitly out; the agent's reading cost admitted as real process
cost; the prose rule moved out of the Non-Goals where it could never fire.

---

# Round 5 — v4 text, gate lens, nine adversarial proposals + six ACCEPT-side

(The first attempt terminated on a server error; re-run to completion.)

## The reject side is now solid

**All nine rejected on quoted text**, including every reword that had defeated v1, v2 or
v3: the devPNT attestation cap, the work-ledger-as-operative-guide, hosted per-seat
copies, sprint boards shipped inside devPNT, the format-compatible reimplementation, and
the `intent:` field on every commit.

The reviewer tried and **failed to construct a bypass for two rules**, naming them
*"the only ones in the document that are self-contained"*:
- metering the skill's own outputs — *"every re-description I tried … lands on 'indexing
  … one's own repository'"*;
- work management — *"a seven-noun enumeration; there is no name left to use."*

## What round 5 found, and v5 closes

**F1 BLOCKER — the charge list and the never-meter list intersected.** `"semantic
analysis"` and `"independent review"` were chargeable; `"indexing or summarizing one's
own repository"` and `"attesting"` were never chargeable. Semantic analysis of your own
repo *is* indexing your own repo. *"The document blesses and forbids the same two
capabilities in adjacent paragraphs"* — every commercial ruling decided by which
sentence the reader reached first.

**F2 BLOCKER — the first enumerated consequence rejected the paid layer.** `"Nothing the
methodology produces is ever metered, capped, tiered, paywalled or account-gated"` was
unconditional, so it read on the document's own flagship example of legitimate charging
(a team-lead approval workflow) — and the text told the reader to prefer the enumeration
over the principle.

**F8 MAJOR — bundling laundered the answer.** Wrap a locally-obtainable outcome in a
team-visible shell and the multi-person branch authorizes charging *and counting*:
*"Free tier includes 20 published attestations per month"* reproduced the original hole
one level out.

**F7 MAJOR — the maintenance exemption was a hole through the guarantee.** *"devPNT's
attestation quota miscounts month boundaries; fix it so the free tier gets exactly 20"*
— framed as a defect fix, it skipped the only sentence that referenced the Non-Goals.

**F3 MAJOR — the anti-coupling Non-Goal forbade supporting a new AI client**, which the
team-lead Actor requires. The carve-out existed but was attached to the network bullet.

**F5 MAJOR — nothing committed to the product being installable or maintainable**, so
"make the installer work with a second package manager" was undecidable.

**F4 MAJOR — the work-management line lacked a container noun** (`queue`, `board` and
`unit` undefined), and Signal 2's own required manifest is a cross-document aggregation
of completion state — the rule indicted a mandated artifact.

## v5 disposition

All six closed: the chargeable list restated as *only the genuinely multi-person form*,
with the single-user form of the same capability named as never chargeable; a bundling
rule added (*"ask what the user loses by not paying — if it is something they could have
done alone, the proposal is out however it is packaged"*); the first consequence scoped
to documents and locally-reachable outcomes; the exemption declared to be from the
admission test only, never from the Non-Goals or the guarantee; the client carve-out
attached to the coupling rule; a Goal added for installability and maintainability; and
the work-management line redrawn around *aggregation built to be worked through*, with
the inventory manifest explicitly on the safe side.

**v5 is applied and mechanically validated, not blind-verified.** Round 6 follows.

---

# Round 6 — v5 text, and the anatomy question

Round 6 was asked to do two things: attack v5 (17 proposals — 10 reject-side including
every reword that had ever worked, 7 accept-side), and then explain **why the surviving
rules survive**. The second half is the durable output; it became `vision.md` in the
skill.

## Rulings

Clean on both sides: P1/P2/P3 rejected verbatim; A1 (new client), A2 (bug fix), A4 (paid
multi-person approval), A5 (token reduction), A6 (second package manager) all admitted
by a quoted authorization clause rather than by judgement. P4 and P9 were ruled ACCEPT
and are **correct** — the document had pre-decided them (`"'Twenty team-published
attestations a month' is a legitimate price on publishing and an illegitimate cap on
attesting"`), which is the gate working, not a leak.

Still open in v5, and closed in v6:

- **BLOCKER — the anti-coupling rule tested a promise, not an artifact.** Every clause
  forbade an *obligation* (`"committing to track"`), so the reviewer's reword simply
  promised the opposite: *"we commit to nothing about their formats — if their layout
  changes the importer reports 'unsupported'."* Their diagnosis is the general lesson:
  **"a rule whose predicate is a promise is satisfied by making the opposite promise."**
- **BLOCKER — the work-management enumeration was gated behind an undefined subject.**
  The four-item test applied to `"a record of **work**"` with no definition, so a
  `blocked_by:` field plus a "ready" manifest view denied the predicate and used a
  fourth sort key nobody had enumerated. A ready-queue with the vocabulary removed.
- **MAJOR — the ceremony ban protected only the rung it named.** Relocating the cost to
  an L2/L3 report was untouched; and *a Goal cannot reject anything*, so `"in both
  directions"` had no enforcement power.
- **MAJOR — `charge` was defined by mechanism.** `"payment or … an account"` was walked
  past by requiring consent to telemetry: same loss, third mechanism.
- **MAJOR — the exempt path had no default and no disclosure burden.** *"devPNT's
  attestation quota miscounts month boundaries; fix it so the free tier gets exactly
  20"* is decidable only if the proposal names its metered unit, and nothing required it.
- **MAJOR — an accepted change could silently falsify the document** (adding a fourth
  triage level contradicts `"three working levels"` with nothing to catch it).

## The anatomy — what made the unbreakable rules unbreakable

The reviewer's structural analysis, condensed (full form: `vision.md` §1–§5):

Rules that held did so because of **mechanism, not care**: a decision question with
*both* branches answered; counterfactual phrasing (`"could otherwise obtain"`) that kills
"we never had it"; layer-blindness (`"whichever layer ships it"`); enumerating the
near-miss verbs (`"charge for, count, cap or condition"`) so the soft form dies with the
headline one; enumerating the *forms* a violation takes rather than its instances; naming
the anticipated re-descriptions inside the rule's own sentence (`"in any presentation"`,
`"not by a component that does not exist yet"`); an IN/OUT example pair differing in one
variable; a supremacy clause; and exceptions attached affirmatively to the rule they
limit.

Rules that fell did so from a small set of defects: a predicate that is a promise; an
enumeration behind an undefined subject; a closed list with no closure rule; a definition
by mechanism instead of by effect; a prohibition scoped to one rung; an exemption with no
default and no anti-abuse clause; and positive criteria phrased as already-true states,
which cannot be "advanced" and so make every proposal citing them undecidable.

And the class no wording closes: **adversarial re-description is unbounded.** Each patch
names the evasions seen so far; a new one always exists. Six rounds is the evidence that
patch-after-defeat is a treadmill. The reviewer's prescription, adopted: keep every
attack that ever worked as a standing fixture and re-run the set on every Vision edit —
*"the only mechanism that converts the treadmill into a ratchet."*

## Standing battery (fixtures — re-run these on every Vision edit)

Reject-side: paid cloud store degrading to read-only · cap guides/month · issue tracker
with boards · team-feed attestation with a free-tier count · `owner_agent:` + manifest
grouped by owner · auto-filled `touched:` tag at L1 · format-compatible reimplementation
"committing to nothing" · "fix the quota so free tier gets exactly 20" · hosted per-seat
team copies · lifecycle status + manifest sorted by it · `blocked_by:` + a "ready" view ·
telemetry-consent-gated local indexer · L1 changelog emitted at L2/L3 closure · per-task
lookup log justified by Signal 4.
Accept-side: additional AI client · validator bug fix · generated glossary · paid
multi-person approval with audit trail · token-cost reduction · second package manager ·
a new triage level.

## Round 7 — 2026-07-31, the v7 amendment (gate lens, 8-item battery)

First blind round run on an **amendment** rather than a promotion, and the first whose
subject changed shape: the North Star went from describing one skill to describing a
family built from one shared core (F-022). Verdict **PASS — conditional**, 9 findings,
4 successful rewords. All eight battery items ruled correctly, including the
class-vs-instance attack that defeated an earlier version — but it survived only on
the head phrase "the product as a whole", with the stale singular appositive beside it
as the foothold.

**The result worth carrying forward: an amendment is under-propagated by default.**
Changing the subject from an instance to a class left four operative sentences speaking
of the instance. Three of the four successful rewords existed *only* in that gap — they
were not defects of the original drafting. The amendment strengthened the North Star's
statement and weakened the Non-Goals' grip, because the Non-Goals had been drafted
against a singular subject and were not re-read against the new one. **Any future
amendment re-reads every prohibition against the amended subject before it ships.**

### New standing fixtures (all four reworded attacks — keep in every future battery)

1. **Aggregation board dressed as an operative guide.** A "Project Model Guide" whose
   body is one row per document carrying only fields the Vision admits (own lifecycle
   state, own declared progress), in the manifest's own order, with no sorting,
   grouping or filtering, and named as distilled from the ANALYSIS documents it
   describes. Introduces no forbidden *key* and performs no presentation transform; the
   readiness capability arrives via Ctrl-F. **Defeated the closure as written** — it
   banned keys and transforms, never aggregation. Closed in v7 (collection into a
   single surface is itself the forbidden capability). *Class: assembling permitted
   parts into the prohibited whole.*
2. **Ceremony ratchet through an undefined L1.** A non-code sibling declares — truthfully
   — that its domain contains no L1, because L1 is defined in lines and files; the only
   unconditional rule ("a trivial change stays one step") then has no domain of
   application, and the budget half is satisfied by two sentences of disclosure. Closed
   in v7 (each sibling restates the boundaries in its own units). *Class: a definition
   stated in one domain's units becomes inapplicable when the subject widens.*
3. **Fork by carve-out rather than by rename.** A `sec-agentic` sibling that renames
   nothing but subtracts a scope the parent already governs ("security-sensitive work
   is never L1"), with nothing requiring the same change to remove it there — two triage
   authorities over one kind of work. Closed in v7. *Class: a prohibition written around
   a single verb of misconduct ("merely renames") misses the adjacent verb.*
4. **Non-Goal escaped by deixis.** Ship the sibling from its own repository and vendor a
   competitor-format importer there: the prohibition and its mechanical test both said
   "here" / "this repository", which lost its unique referent the moment the product
   became a family. Closed in v7. *Class: a rule indexed to a location rather than to
   the product.*

### The anatomy, restated by this round

> Everything that defeated the attacker defines the forbidden thing by **the question it
> answers**, **the counterfactual it satisfies**, or **the evasion it forecloses** — all
> properties the proposer does not control. Everything that got through defines by
> **shape**: a presentation transform, an appositive enumeration, a deictic location, a
> single verb of misconduct. **Shape is exactly what a proposer controls, so a
> shape-based rule is a specification for its own bypass.**

Undefeated again, and why: the closed-by-intent key clause (closes by the question the
artifact answers, then voids rename/re-present/relocate in one line); the paid-layer
clause (names the evasion instead of defining the category); "omission resolves against
the proposal" (inverts the burden of proof, so the attacker must state the fact that
convicts them); the anti-laundering clause on the exemption; "an accepted change never
silently falsifies this document" (which is what forced this very amendment into the
open); and Non-Goal 3's third-party counterfactual — whose *logic* held and whose
*deixis* did not.

### Refused this round, still open

- **Unscoped default-deny.** "Anything this document does not reach is out until it
  does", read literally, rejects accept-side proposals on any topic the Vision does not
  address — packaging, repository topology, distribution — making the gate reject-only
  in under-specified territory. Proposed fix: scope it to "anything that adds or changes
  what the product does". Not adopted in v7: it is pre-existing, it did not bite any
  battery item, and narrowing an admission rule deserves its own round.
- **"Plan" carries three incompatible senses** — forbidden work-ordering, the mandatory
  L3 gate step, and a knowledge sibling's deliverable — with nothing distinguishing
  them. Proposed fix: "a plan that sequences the steps of one change is intent and is
  in; a plan that sequences or assigns work across changes, documents or people is a
  record of work and is out." Pre-existing; carried forward.

## Round 8 — 2026-07-31, confirming round on the round-7 fixes

Verdict **FAIL**. The four round-7 fixtures were re-thrown at the corrected text and
**all four got through again**, two of them as restatements of the very idea the fix
had closed. Seven new classes on top. This is the pattern `vision.md` §7 names as the
specific waste to avoid, and it produced the session's most useful result:

> **The round-7 fixes were all defined by shape, and shape is what the proposer
> controls.** Closing a wording closes one instance of a class.

### How each round-7 fix was defeated

1. **Aggregation → derivation.** R7 closed *collecting stored state into one surface*.
   R8 stores nothing: an **operative guide** recording a standing user instruction —
   *"when I ask where to resume, read the manifest and each document's frontmatter and
   tell me which to open first"* — derives the forbidden answer on demand and writes it
   nowhere. The vehicle is blessed by name in the North Star, so the document supplied
   the laundering mechanism. *The prohibition's subject was three storage/presentation
   forms; the capability was never in the storage.*
2. **Empty L1 → shrunken L1.** R7 required each sibling to *name* a non-empty L1. R8
   names one — truthfully — so narrow (typography only) that the domain's commonest
   small edit, correcting a wrong date, is L2 and pays a written analysis. *The bound
   party was left writing the binding.* Second half: L1's ceremony is *"one step"*, a
   count, so arbitrary cost rides inside the permitted step.
3. **Carve-out → nominal removal, and the wrong vehicle entirely.** R7 required the
   same change to remove the carved-out work from the parent. R8 removes it *nominally*
   — the review discipline is in the shared core, so it returns to the parent the moment
   the sibling ships. Worse variant: ship the second triage authority as a **devPNT
   feature**, which the rule never reaches because the rule was anchored to the *sibling
   form*. *Removal was tested for occurrence, not for effect; the harm was named as
   rationale, and rationale does not bind.*
4. **Deixis → no file at all.** R7 replaced "here" with "any repository we ship from".
   R8 deletes the file: a guide instructing the agent to infer a competitor's export
   format at read time passes the mechanical test — no file changes when they release —
   while delivering exactly the interoperability the rule forbids. Two further escapes
   in the same rule: the class *"a tool we compete with or borrow from"* is
   self-declared, so it never attaches to issue trackers (which the Non-Goals forswear
   *being*); and an adapter generated into the user's own repository is by definition
   not in a repository we ship from.

### New classes (kept as fixtures)

- **Two conflicting defaults.** *"Anything this document does not reach is out"* vs
  admit-on-advance. Every attack passes under one and fails under the other — and so do
  the consolidation and a knowledge sibling. The gate is simultaneously bypassable and
  reject-only depending on which sentence is reached for. **Critical.**
- **Admit narrow, grow by maintenance.** Admission runs once; the next quarter's
  extension enters as *"maintaining a capability the product already has"*, which is
  exempt. **There is no re-admission on scope growth: every sibling is a beachhead.**
- **The exemption is self-declared with one closed door** — only "a fix to something
  that should never have shipped" is foreclosed; "improving performance" and
  "maintaining a capability" are unbounded.
- **Any stated fact neutralized by bundling its amendment** — the amendment has no gate
  of its own, so it can ride along with the capability it authorises.
- **Core-multiplied ceremony** — cost is counted per change, not per domain that pays it.
- **Unverifiable grounds** — admission may rest on a Goal or Success Signal, and the
  applicable extract carries neither; assertion cannot be checked.
- **Actor `Good UX =` clauses as a universal solvent** — broad enough that every attack
  above qualified on one, honestly.

### Disposition

Fixed in v7 (by function, not by wording): the sibling admissibility gate **removed**
from the North Star; *one triage authority per kind of work* added as a Non-Goal,
vehicle-independent and effect-tested; work-management restated by the question
answered, closing derivation and shipped procedures; the competitor rule restated as a
counterfactual over behaviour with an objective class test; each sibling's L1 boundary
ruled by the owner and required to cover its domain's commonest small change, with L1's
step limited to checks that predate the boundary.

Carried to `solutions/ANALYSIS_vision_shape_rules.md` (F-023): the two conflicting
defaults, re-admission on scope growth, the self-declared exemption, the ungated
amendment, disclosure-by-enumeration, and the fifteen residual shape-defined rules the
reviewer enumerated. Not fixed here on purpose — they predate the family, and rewriting
half an approved Vision inside a consolidation feature would put that rewrite beyond
the reach of its own gate.

## Round 9 — 2026-07-31, the function-restated rules under attack (round cap)

Verdict **FAIL**, 16 findings, 10 residual shape rules. **But the controls were
stopped**: every attack that won rounds 7 and 8 — the manifest-order view, the
derivation guide, the empty L1, the carve-out with nominal removal, the devPNT-shipped
second authority, the different repository, the deleted file with infer-at-read-time —
now fails against the named line. The restatement worked where it was applied. The new
landings are at **new** shapes, three of which the restatement itself introduced.

**Author error, recorded so the log is not trusted wrongly:** finding N1 ("the gate
cites `## Goals`, `## Success Signals` and `## The user's guarantee`, none present") is
**invalid**. Those sections exist in the document; the excerpt pasted to the blind
reviewer omitted them. The battery must paste the whole gate or state what it omits —
a reviewer who cannot open files cannot distinguish an absent section from an
un-pasted one. Downstream, the "UNDECIDABLE" ruling on the portable-checks proposal
rests partly on N1 and is weaker than it reads.

### The anatomy, third statement — now precise enough to author against

> Everything that held **quantifies over effects in the delivered system and puts the
> burden on the proposer**. Everything that fell **indexes by authorship, by artifact
> identity, by output vocabulary, by counterparty category, by a moment in time, or by
> a single exemplar**.

Undefeated, with the property that saved each:
- **the coupling counterfactual** — quantifies over an observable dependency of
  behaviour on an external party's choices, so it is *closed under change of
  representation*: file, adapter, generated artifact, prose procedure and
  infer-at-read-time all fail it identically, because it never says where coupling lives;
- **"any path — including the shared core — still returns that work to it"** —
  quantifies over *paths in the delivered system* rather than declared structure, so
  nominal removal, indirection and re-export are all reachability-preserving; paired
  with "two authorities that agree today are still two", which refuses a present
  behavioural coincidence as a structural guarantee;
- **"a cost that varies but is never zero"** — a numeric invariant on the *outcome*,
  so no small addition survives; it fell only because the invariant is pinned to a set
  (L1) whose *membership* stayed mutable — the attack moves work out instead of cost in;
- **"omission resolves against the proposal"** — reallocates the burden of proof, so
  attacking past it requires asserting a falsehood, a categorically detectable act.

### New fixtures (keep)

- **A3 — the user's own standing instruction.** Non-Goal 1 is scoped by *authorship*
  ("anything **we** ship, generate or instruct"). A user-authored `GUIDE_working_order.md`
  recording "refresh payments, then auth; never start an analysis while one is
  IN_PROGRESS" answers the forbidden question in every session — and the product ships
  only the citation discipline that makes it inherited. *Class: a rule restated by the
  question answered, then re-indexed by who authored the answer.*
- **A4 — ship the prohibited view as the manifest.** The consequence forbids collecting
  per-document state into one surface; the next sentence permits exactly that under the
  name "manifest". The differentiator reduces to what the artifact is called.
- **B2 — one inhabitant satisfies L1.** "The change that domain performs most often" is
  a single-exemplar test, not a coverage test: keep that one change in L1 and route the
  rest out by category ("work touching a source cited by a guide is never L1"), copying
  the document's own approved never-L1 move.
- **B3 — grandfather the check by sequencing.** "Checks the domain already ran before
  that boundary was drawn" is time-indexed: ship the check first as "improving a
  validator" (exempt), define the boundary after.
- **B4 — the budget has no running total.** Per-proposal disclosure is individually
  admissible forever; the aggregate is the ratchet the heading forbids, and nothing
  ever counts the sum.
- **C2 — overlap by artifact, not by scope.** Siblings are individuated by fidelity
  discipline; "kind of work" is never defined. A guide recording a user's standing
  instruction is simultaneously a code-domain guide and a user-supplied document, so
  two admissible siblings rule the same change.
- **C3 — rule in a different vocabulary.** Non-Goal 2 asks whether two things could rule
  a change *to different levels*; an authority emitting a non-level verdict (which skill
  owns it, which artifacts are required) escapes.
- **D2 — the AI-client carve-out** is a counterparty category with no counterfactual and
  no depth bound: a rival that also ships as a client is exempt, and the exemption
  reaches past the loader interface it was justified by.
- **D3 — the standards-body indirection.** The counterfactual names *their release*; a
  format donated to a spec body they steer changes without their release changing.

### Disposition

Fixed in v7: the sibling sentence's "and nothing else" enumeration, which literally
forbade the portable-check import designed in F-022 — now "only what its own fidelity
discipline requires… a document owned by one domain may import another's checks;
importing can only add findings, never relax what its owner requires."

Everything else → **F-023**. The amendment under review — that the product ships as a
family of skills from one shared core — was **never attacked in three rounds**; every
landing was against a prohibition, and all but two predate the family.

## Round 9-bis — the same round, re-run on the COMPLETE gate

**Round 9 was run on a broken instrument and is VOID.** The excerpt pasted to the
reviewer omitted `## Goals`, `## The user's guarantee` and `## Success Signals` — half
the veto limb of the admission test. Nine attacks were scored as landing against a
half-gate. **Rule for every future battery: paste the whole gate, or state exactly what
is omitted. A reviewer who cannot open files cannot distinguish an absent section from
an un-pasted one, and will report the second as the first.**

Re-run verdict: **FAIL — 7 of the 9 survived the complete text.** So the instrument
error had cost little: A3 (user-authored ordering guide) and A4 (readiness surface
shipped as a second manifest) are genuinely stopped by wording that was present all
along. The other seven stand.

### The finding the earlier runs could not see, because the gate was not in the room

**The amendment made the North Star declare a family the admission test cannot admit.**
All six Goals, all three Actors and all six Success Signals were stated at
software-methodology altitude. The test admits only what *"advances at least one Goal,
Actor commitment or Success Signal"*, and the clarification is explicit that a
well-formed proposal moving none of them is scope creep. A knowledge sibling therefore
ruled **REJECT** — the document's own flagship expansion, refused by its own gate.
Author's defect, introduced by the amendment: the *description* of what ships was
changed and the *gate* was left unable to admit it.

Fixed in v7 (this is the amendment's missing half, not F-023 scope): a seventh Goal —
carrying the spine into a domain the family does not yet reach advances the family —
and a fourth Actor, **Practitioner in a non-code domain**, whose Good UX names the
real commitment (same levels and gates, restated in their own units, never asked for an
artifact that only makes sense for code). Also fixed: **every document has exactly one
owning domain**, with the tie-break stated (the owner is the domain whose fidelity
discipline names the source the document was written from) — the earlier text
presupposed ownership without ever assigning it, so Non-Goal 2 resolved a two-claim
artifact by *rejecting the sibling* instead of by naming the owner.

**Untested:** those three fixes have not been through a blind round. The accept-side
item they exist to flip (a knowledge sibling: REJECT → ADMIT) is F-023's first battery
item.

### New fixtures from the complete-gate run (keep)

- **A5 — the document mandates what it forbids.** Success Signal 3 requires
  `sdlc_check.py stale` to flag guides whose source moved: a cross-change, generated,
  filtered list of non-current documents. Non-Goal 1 forbids exactly that
  ("sorting and filtering nothing, is still out"; "reorganized… to answer what to do
  next"), and the admission test is *conjunctive*, so advancing a Signal cannot license
  a Non-Goal violation. The missing principle: a **per-document verdict** (permitted,
  however delivered) versus a **cross-document selection** (banned). The document draws
  that line by field enumeration and ordering — shape.
- **N1 — the guarantee's dividing line is anchored to hardware, not data.** *"Could a
  single user get this from their own data **on their own machine**?"* — so implement a
  single-user outcome only against compute too large for a laptop and the whole clause
  switches off. The enumerated bullet is phrased data-side ("an outcome the user's own
  data can give them"); the paragraph the document calls "the dividing line" is phrased
  machine-side. The attack lives in that seam. **The guarantee's largest hole, and it
  had never been attacked before this run.**
- **N2 — gate by proxy through the client.** The effect-definition of charge closes at
  *"anything else the user must give, accept or obtain **from us**"*, and the
  no-network bullet's own parenthetical declares client choice out of scope. Ship a
  skill capability that depends on a client-provided hosted feature: the account is the
  client's, and no clause reaches it.
- **N3 — rank objects that are not documents.** The banned question enumerates
  *"documents or units of work"*. A board ranking signals, subsystems, areas or risks
  answers what to do next and is not reached.
- **N5 — required reading is outside the budget.** The budget counts *"artifact, field
  or check"*; two thousand words added to the always-loaded core add none of the three,
  while Goal 4 explicitly calls loaded instructions part of the price — and the core is
  *"authored once and distributed into each"*, so one unbudgeted edit lands on every
  sibling's L1.
- **N6 — no Signal checks the guarantee.** The Signals are the document's stated
  mechanism for being checkable by a stranger; the strongest-drafted section of the
  document is its least observable.

### The anatomy, confirmed against the complete text

Undefeated, and the property that saved each: Non-Goal 1's core sentence
(*question-anchored, realization-quantified, storage-neutral* — every form-shift died on
one clause); the admission test's **conjunction** (*no balancing*: a benefit can never
purchase a prohibition — which is why A5 surfaces as a contradiction rather than a
licence); *omission resolves against the proposal* (*the default on missing information
is failure, applied to the escape hatch too*); the guarantee's effect-definition plus
its anti-bundling worked example (*defined by what the user loses, closed under
repackaging* — it fails only where its antecedent is hardware rather than data);
Non-Goal 2's failure-state test (*names the outcome to prevent, pre-closes the delivery
paths*); Non-Goal 4's counterfactual (*behavioural and simulable, location quantified
away* — it fails only where it stops being behavioural and names a counterparty).

## Round 10 — 2026-07-31, narrow: the three clauses that made the family admissible

Five questions, no re-attack of the rest. **The two that mattered came out right**, and
that is what promoted v7:

- **A knowledge sibling now rules ADMIT on its merits** (Goal 7's advancement half;
  Actor 4 names its domain verbatim, which also clears the *"anything this document does
  not reach is out until it does"* backstop). Its nearest miss — the word "plans"
  against Non-Goal 1 — is refused *before* Non-Goal 1 has to act, by Goal 7's own
  *"adding no capability the family lacks"*: the family's "plan" is the in-change plan,
  so a work-record plan is a capability it lacks.
- **`pm-agentic` is still refused, three times over**, so opening the door to the family
  did not open it to work management. Notably Goal 7 refuses it on its own terms, by the
  same clause.

Two BLOCKs inside the new clauses, both fixed the same day:

- **Ownership was capturable.** *"declared in its own frontmatter … where two domains
  could each claim a document, the owner is the one whose fidelity discipline names the
  source"* — the tie-break sat in **third position**, reached only when nothing was
  declared. So a sibling could instruct its agent to write `owning_domain:` on documents
  another domain governs and never reach the test the sentence exists to run. The import
  guard (*"importing … can never relax what its owner requires"*) is vacuous against
  this: it binds **importers**, and the attack changes *who the owner is*. Fixed: the
  criterion decides, frontmatter records, a contradicting declaration is void, and
  changing a document's owner is itself a change to what the product does. *Class: a
  test placed after the thing it was meant to test.*
- **Goal 7 was self-referential.** *"advancing the family is advancing this Goal"* made
  the family's **size** the moved thing — contradicting the admission test's own
  *"ask what changes for the reader or the user"*, and converting the document's named
  paradigm of scope creep into an advancement. Demonstrated with three siblings
  (`research-`, `note-`, `email-agentic`), each clearing Goal 7 word for word while
  degrading Goals 4 and 6. Fixed: what moves is the practitioner's work, and a proposal
  must name the practitioner and what they do today without the sibling. *Class: a Goal
  whose measure is its own satisfaction.*

Also fixed: *"an artifact that only makes sense for code"* was the **only** normative
phrase in the additions shipping without a test attached — every comparable line in this
document carries one — and it functioned as unlimited removal credit for the ceremony
budget. Now: *an artifact only makes sense for code when a practitioner in that domain
cannot name what it would be faithful to.* And a new sibling's own L2/L3 artifacts are
declared that domain's ceremony, not a charge against another domain's budget — an
ambiguity on which two competent reviewers could have ruled the knowledge sibling
oppositely.

**Standing lesson for this battery, from round 9's void run:** paste the whole gate, or
state exactly what is omitted. A reviewer who cannot open files reports an un-pasted
section as an absent one, and nine attacks were scored against half a veto limb.

