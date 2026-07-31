# Project Vision
Status: APPROVED (by Antonio Pinto — v6 2026-07-27, **v7 amendment 2026-07-31**)

*Binding authority for the Vision Gate. Provenance and revision history at the end of this document.*

## North Star

Agentic SDLC is a methodology an AI coding agent follows so that every change it
makes stays traceable to the project's declared intent, at a ceremony cost
proportional to the change's risk. It ships as a **family of skills built from one
shared core**: each skill is a bundle of Markdown instructions the agent loads plus
a Python validator, and the part they share — the process spine: triage, the Vision
Gate, the document lifecycle, the operative guides, the review discipline — is
authored once and distributed into each of them. `agentic-sdlc` governs software
delivery and is the only one that produces code; sibling skills govern other
domains of work under the same process, each adding only what its own fidelity
discipline requires — its method and its validation rules — and no capability the
family does not already have, and no ceremony its own domain's L1 must pay. A
document has exactly one **owning domain**: the domain whose fidelity discipline names
the source that document was written from. Frontmatter *records* that answer and the
project's declared default supplies it where no record exists — neither decides it, and
a declaration contradicting it is void. **Changing a document's owning domain changes
what the product does**: it passes the admission test like any other such change, and
the prior owner's rules bind until it has. A document may **import** another domain's checks where its
content calls for them; importing adds findings, never authority, and can never relax
what its owner requires.
A skill is installed where the agent keeps its skills; everything any of them
produces lives in the user's own project repository. There is nothing to run as a
service.

What distinguishes one skill in the family from another is its **fidelity
discipline**: what its claims must be faithful to. `agentic-sdlc` answers to this
repository's code; a sibling answers to something else, and if it answers to the
same thing it is a rename, not a sibling. Whether a proposed sibling is admissible
is ruled by the admission test and the Non-Goals below, exactly like any other
change to what the product does — this paragraph states what the family *is*, and
adds no gate of its own.

Cost scales on three working levels, and the boundaries are stated here so this
document can be applied on its own:

- **L1 trivial** — roughly ten lines across one or two files, no change to an API,
  a dependency or existing behavior. One step: make it, run the existing tests.
- **L2 small** — a clear root cause, at most three files, no new dependency and no
  public-API change. Carries a short written analysis and mandatory tests.
- **L3 significant** — anything more: more than three files, a contract or data
  model, a new dependency, user-visible behavior, a security-sensitive area, or a
  design with real alternatives. Passes the full gate — Vision check, written
  design, plan, tests, closure.

Security-sensitive work (external input, authentication, cryptography, network,
personal data, filesystem access) is never L1. When two levels both look right,
the higher one is correct.

The boundaries above are stated in code units because `agentic-sdlc` is the skill
that produces code. **Each sibling restates these three boundaries in its own
domain's units before it ships; the units change, the three levels and the ceremony
attached to them do not.** **The owner rules on those boundaries; a sibling does not
write its own escape.** A domain's L1 must cover the change that domain performs most
often at small scale — a sibling whose L1 excludes its own commonest small edit has
mis-drawn the line, not discovered that its domain has no trivial work. And L1's
single step may run only checks the domain already ran for its own sake before that
boundary was drawn: a check introduced by the same change that defines L1 is added
ceremony wearing L1's clothes. "A trivial change stays one step" binds in every
domain, and what it binds to is not the bound party's to shrink.

Its central mechanism is the **operative guide**: a document recording how one
part of the project actually works — a subsystem of the code, or a standing
instruction the user has given — which names the exact source it was written
from, so a later reader can check whether it still matches that source instead of
trusting it. A guide is written once and *cited* by later work rather than
restated in each task, so an agent starting with no prior context inherits the
project's model instead of rebuilding it or copying it forward by hand.

Every skill in the family delivers all of this from the filesystem alone: no
service, no account, no network of its own. **devPNT** — a separate product that adds governed
storage, versioned proposals with human approval, semantic analysis and
independent reviewers — may be layered on top to strengthen it, and must never be
required for the skill to be complete.

## Core Problem

**Myopia**: an agent acts from partial understanding. It changes what it can see
and breaks what it did not account for; the understanding it paid to build
evaporates when the session ends, so the next session re-derives it, badly. Every
element of this methodology — the triage, the Vision Gate, the document
lifecycle, the operative guides — exists to make understanding durable and to
make drift visible before it lands.

## Actors

- **Solo developer using an AI agent** — ship features, audits and refactors
  without losing the thread. Good UX = ceremony proportional to risk (a typo
  stays one step; a significant change earns the full gate) and never
  re-explaining the project across sessions.
- **Team lead needing governance** — keep several agents, on whatever clients the
  team uses, aligned to one intent. Good UX = one process, one source of truth,
  and divergence from the declared intent surfaced before the change is merged.
- **Adopter evaluating the paid layer** — start with the skills alone and adopt
  devPNT only when its governance machinery pays for itself. Good UX = every skill
  in the family is complete on its own, and dropping devPNT loses its amplification
  but never strands a capability or a document (the rule is a Non-Goal below, not a
  courtesy). A sibling that requires devPNT to be complete is not admissible.
- **Practitioner in a non-code domain** — govern knowledge, research or planning work
  with the same discipline, without a software process bolted onto it. Good UX = the
  same three levels and the same gates, restated in their own domain's units, and
  never being asked for an artifact that only makes sense for code — which is decided
  by the same fidelity test the rest of this document uses: **an artifact only makes
  sense for code when a practitioner in that domain cannot name what it would be
  faithful to.** Not "it feels like a software artifact."

## Goals

- Make the project's intent readable and *operable* by an agent that arrives with
  no context: it can state what the project is for and rule on a proposed change
  from `ai_docs/` alone.
- Keep understanding durable across sessions — Vision, design, plans, tests,
  guides and handoff stay synchronized, versioned and self-describing, so nothing
  load-bearing lives only in a transcript.
- Make divergence from the declared intent visible *before* implementation, and
  again before merge. Never hide a conflict between a user request and the
  declared Vision: surface it and let the user choose.
- Scale process cost to risk, in both directions — a trivial change must not pay
  for governance, and a significant one must not escape it. Cost includes what the
  agent must read: the instructions and documents it loads are part of the price of
  the process, and lowering that price without losing the process is real work.
- Stay whole without any external dependency, so that adding devPNT is an
  amplification and never a repair.
- Be installable, upgradable and maintainable by the people who use it — on the
  clients they already run, without hand-assembly. Packaging, distribution,
  installation and the product's own tests are part of the product, not overhead
  outside it.
- Carry the same process spine into other domains of work. A sibling that governs a
  domain the family does not yet reach — at the same ceremony-to-risk ratio, with its
  own fidelity discipline, and adding no capability the family lacks — advances the
  practitioner's ability to do their work under this discipline, and that is what
  advances this Goal. Without it the admission test could admit no member of the family
  the North Star declares. **What moves is the practitioner's work, never the family's
  size**: a proposal under this Goal names the practitioner in the sense of the Actor
  above and the work they do today without the sibling. "It would be one more
  well-formed sibling" moves nothing, and is the scope creep this test already refuses.

## The user's guarantee

Everything the methodology produces — every document under `ai_docs/`, every
operative guide, plan, analysis and handoff — stays in the user's own repository,
readable and usable in full without paying anything, and keeps working if devPNT
is removed tomorrow.

devPNT may charge for what it adds *over* that data, and only in the form that
genuinely needs more than one person or shared infrastructure: multi-person
workflow, team-wide sharing and audit, review by someone other than the author,
analysis across repositories a single user does not hold. The single-user form of
any of these — reviewing your own document, analyzing or indexing your own
repository — is never chargeable, because you could do it on your own machine.

devPNT may never charge for, count, cap, gate, degrade, delay or condition (here
and below, **"charge" is defined by effect, not by mechanism**: condition on
payment, on an account, on registration, on consent to telemetry or terms, on an
invitation or waitlist, or on anything else the user must give, accept or obtain
from us. A human approval step inside a workflow the user themselves chose is not
a charge):

- creating, reading, editing or validating any document the methodology produces;
- how many documents, guides, analyses or changes a user may produce;
- **any outcome the user could otherwise obtain locally from their own data** —
  mirroring, attesting, indexing or summarizing one's own repository is such an
  outcome, and putting it behind a counter is metering under another name;
- continued access to documents already produced, once devPNT is removed.

That third bullet is the dividing line: *could a single user get this from their
own data on their own machine?* If yes, it may never be metered, whichever layer
ships it — hosting it, attesting it, or indexing it elsewhere is the same outcome
moved, not a new one. If no — because it genuinely needs shared infrastructure,
several people, or someone else's compute — it may be charged for.

**Bundling does not launder the answer.** Wrapping a locally-obtainable outcome
inside a team-visible or hosted feature makes the *wrapper* chargeable, never the
outcome: the single-user path to it must remain, unmetered and uncounted, in the
skill. "Twenty team-published attestations a month" is a legitimate price on
publishing and an illegitimate cap on attesting; if the same cap bites a user
working alone on their own repository, it is metering under another name. Ask what
the user loses by not paying — if it is something they could have done alone, the
proposal is out however it is packaged.

Enumerated consequences, so the guarantee is applied and not interpreted:

- **No document the methodology produces, and no outcome a single user could reach
  from it on their own machine, is ever metered, capped, tiered, paywalled or
  account-gated** — not by devPNT, not under another product name, not by a
  component that does not exist yet. (Genuinely multi-person capabilities are the
  chargeable part; this bullet does not reach them.)
- **The skill itself requires no network, no account and no remote service.**
  devPNT may use all three for what it adds; the skill's own capabilities may not
  depend on them. (Which agent client the user runs is their own choice and out of
  scope for this rule.)
- **devPNT is never the only way to obtain an outcome the user's own data can give
  them**, and removing devPNT never strands a document.
- **What removing devPNT does cost is exactly what payment bought**: the genuinely
  multi-person, shared-infrastructure capabilities. Those going away is the paid
  layer working as designed, not stranding. Nothing the user could have done alone,
  on their own machine, may go away with it.

## Non-Goals

These bind **the product as a whole — every skill in the family, present or
future, and anything the devPNT layer adds**. Shipping a forbidden thing in the
paid layer does not put it out of reach of these rules, and neither does shipping
it in a sibling skill: earning a trigger admits a sibling to the admission test,
it never exempts it from a Non-Goal. The commercial rules are in `## The user's guarantee` above and
bind the same way.

- **Not a work-management system.** No issue tracker, work-item ledger, board,
  assignment, sprint, velocity or burndown — in any form, under any name, however
  well it inherits `ai_docs/` conventions.
  The line, stated so it can be applied: a **document describing its own state** is
  intent and belongs here — its lifecycle (draft → approved → superseded, fresh →
  stale) and its own progress (planned → in progress → completed) both qualify,
  because they describe the document, not an assignment.
  **A record of work** — the thing that is out — is **anything we ship, generate or
  instruct that answers, or tells an agent to answer, which documents or units of
  work should be worked on next, in what order, or by whom.** The rule is stated by
  the question answered, not by the form that answers it: artifact, field, view,
  generated output, procedure, or a standing instruction the agent follows are all
  the same thing here, and it makes no difference whether the answer is stored or
  derived on demand and never written down. Sequencing the steps inside one approved
  change is not this. Two consequences, because both have been reached in practice:
  a view assembled only from fields this rule admits, sorting and filtering nothing,
  is still out — collecting each document's own state into one surface is itself the
  capability; and a guide whose body is a procedure for producing that answer is out
  for the same reason, being an instruction we ship. In: an ANALYSIS whose
  own frontmatter says `IN_PROGRESS`. Out: a manifest view listing the ones that
  are. The generated manifest is the permitted form: an inventory of what exists and
  whether each document is current, ordered for lookup and carrying no further
  per-document state — and it crosses the line the moment it is reorganized, or
  enriched with such state, to answer what to do next.
- **One triage authority per kind of work.** Exactly one thing may classify any
  given change. A second authority over work something here already governs is out —
  whether it arrives as a sibling skill, as a mode or profile inside an existing one,
  as a second package, or as a devPNT feature; whether or not it renames anything;
  and whether or not the first authority is nominally removed, if after the change
  any path — including the shared core — still returns that work to it. The question
  the rule asks: *after this change, could two things rule the same change to
  different levels?* If yes, it is out, and lowering-only or fallback-only does not
  save it: two authorities that agree today are still two.
- **No ceremony ratchet, at any level.** A trivial change stays one step: any
  mechanism that makes trivial edits pay a governance cost is out — added as a
  step, a required field, a check, an auto-filled field someone must later read, or
  a cost that varies but is never zero — whatever its benefit higher up. **Above L1
  the rule is a budget, not an exemption**: a new mandatory artifact, field or check
  at L2 or L3 is admissible only if the same change removes one of comparable cost,
  or the proposal states the cost it adds and the owner accepts it explicitly.
  Ceremony relocated from L1 to a higher level, or from a step to a report, is the
  same cost moved — count it. A new sibling's own L2/L3 artifacts are **that domain's**
  ceremony and are ruled by the ratio above, not counted against another domain's
  budget; what this budget counts is ceremony added to a domain that already exists.
- **No coupling to another such tool's formats or artifacts.** *Such a tool* means
  any tool whose users we could serve instead — whether or not we say we compete with
  it, since a self-declared class is one the proposer decides. Stated as a property of
  what we do, because a promise is not checkable: **nothing we ship, generate or
  instruct may be copied from such a project, or depend on, reproduce or teach a
  format or interface it defines.** The test is a counterfactual — *if their release
  changes it, does anything we ship, generate or instruct produce a different result?*
  If yes, the rule is broken. Location does not save it: not a different repository we
  ship from, not an adapter generated into the user's own repository, and not a
  procedure that carries no format but tells the agent to infer one at read time —
  coupling that lives in behaviour is coupling. And a declaration
  that we "commit to nothing about their future versions" does not change what the
  code does. Ideas may be studied and absorbed freely; artifacts and formats may
  not cross. **This rule does not reach the AI clients the methodology runs on**:
  conforming to a client's skill layout is how the product reaches its users, and
  supporting one more of them is squarely wanted (see the team-lead Actor).

## The admission test

**What this test governs**: proposals that add or change *what the product does*.
Fixing a defect, improving performance, or maintaining a capability the product
already has needs no admission — it is authorized by the capability it serves.

**The exemption is from this test only.** The Non-Goals and the user's guarantee
bind everything, always. Work framed as a fix to something that should never have
shipped is not exempt — it is the removal of that thing, or it is out.

**Disclosure, and what silence means.** A proposal must state the facts its ruling
turns on: for anything that meters, the metered unit and the unmetered single-user
path; for anything that adds a mandatory artifact, field or check, which level it
lands on and what it removes. **Omission resolves against the proposal** — an
undisclosed fact is read the way that makes the proposal fail, on the exempt path
as much as the admitted one. Anything this document does not reach is out until it
does.

**An accepted change never silently falsifies this document.** If a proposal
contradicts a fact stated here — the number of levels, what the product ships, who
the actors are — the same change amends this Vision, or it is not accepted.

A new or changed capability is admitted only if it **advances at least one Goal,
Actor commitment or Success Signal above, and violates neither a Non-Goal nor the
user's guarantee**. The Actors' `Good UX =` clauses count: what this document
promises an Actor is admissible work, not merely aspiration.

Two clarifications, because both halves have been read wrong:

- Advancing a Goal or Signal means moving the thing it measures. Ask what changes
  for the reader or the user, not which file changed: writing a document that
  makes the project's intent decidable to a cold reader plainly advances
  cold-start operability; writing one that nobody's decision depends on does not.
- Inheriting the `ai_docs/` conventions — frontmatter, manifest, lifecycle — is
  *necessary and never sufficient*. A proposal that is well-formed but moves
  nothing this document commits to is scope creep, and the correct answer is no.

## Success Signals

Each one is checkable against a named artifact or command, by someone who was not
here when this was written.

Several are already met. **A met signal is advanced by protecting it under new
load or by widening what it covers** — say which, and against what baseline; "it
stays true" is not an advance. Where a signal names a command, the baseline is
that command's output today.

1. **Cold-start operability.** An agent given only `ai_docs/` and no other context
   can state what the project is for and rule ACCEPT / REJECT on a proposed change,
   without asking the user for background. Tested by handing this Vision to a
   reviewer with no project knowledge and seeing whether the rulings are decidable.
2. **Closure is mechanically clean.** `sdlc_check.py check` is CLEAN at every
   closure: every canonical document carries a lifecycle status, appears in the
   generated manifest, and no mapped area is stale.
3. **Guide drift is detected, not trusted.** Every `reference/GUIDE_*.md` names the
   source it was written from and records its hash, so `sdlc_check.py stale` flags a
   guide whose source has moved without anyone remembering to look. Note the limit
   honestly: the hash proves the source is *unchanged*, never that the guide
   described it correctly — that is what the guide-vs-source review is for.
4. **Guides actually reach the work.** Before L2 or L3 work, the agent looks up
   whether an existing guide covers the task and states the result — the guide it
   found, or that none matched — so a lookup that never happened is distinguishable
   from one that found nothing. The guide layer is consumed, not merely written.
   Checkable by running the `evals/scenarios/consult_fires_on_match.md` and
   `evals/scenarios/verdict_declared_on_no_match.md` scenarios cold.
5. **Zero-dependency completeness.** A full L1→L3 change, including closure and
   its documents, completes with no network, no account and no paid component.
6. **Positioning stays honest.** In `strategic/capabilities_and_positioning.md`,
   every row claiming an advantage cites evidence and carries the date of the
   comparison; a row that is parity is labelled parity.

## Where the rest lives

- Competitive positioning, the honest parity line, and the layer map of where each
  capability came from: `strategic/capabilities_and_positioning.md` (a dated
  snapshot — it is expected to age, and it is edited without touching this file).
- Milestones and sequencing: `vision/roadmap.md` and the evolution roadmap.
- Per-feature vision for anything spanning several milestones:
  `vision/features/VISION_[feature].md`.
- The full triage procedure and the `ai_docs/` document conventions: `SKILL.md`,
  the skill file itself, installed in the agent's skills directory — **not** under
  `ai_docs/`. This document states the level boundaries it needs (North Star) so a
  reader with only `ai_docs/` can still rule; `SKILL.md` carries the procedure.

Paths in this document are relative to `ai_docs/` unless written in full or noted
otherwise.

## A note on this document's own prose

No unfalsifiable claim of superiority belongs here. Competitive positioning lives
in `strategic/capabilities_and_positioning.md`, dated and evidenced per row, where
it can be revised without touching the Vision. This is a rule for whoever edits
this file — not a test to run against a proposed change, which is why it is not in
the Non-Goals.

## Provenance

All four versions below were produced and approved on **2026-07-27**, in one
session, each after a blind round against the previous text. The rapid succession
is the method, not instability; the text settled at v4.

- **v7 — 2026-07-31, APPROVED by Antonio Pinto.** Amends `## North Star`: the product
  ships as a **family of skills built from one shared core**, not as one skill. The
  amendment was owed, not optional — F-022 proposes consolidating three sibling
  skills (`agentic-sdlc`, `kb-agentic`, `mkt-agentic-sdlc`) into one repository
  publishing three packages, and the admission test at `## The admission test`
  requires a proposal contradicting *what the product ships* to amend this Vision in
  the same change. The prior text described the state in which only one skill
  existed; two siblings already exist. Adds the sibling-admissibility rule (a
  distinct kind of work with its own fidelity discipline) so the North Star can
  still reject a fork dressed as a sibling — the failure this consolidation exists
  to end. Owner decision recorded 2026-07-31 ("le cose sono cambiate da prima").
  **Blind check run (gate lens, 8-item battery, no repository access): PASS —
  conditional, 9 findings, 4 successful rewords.** Its central finding was that the
  amendment was *under-propagated*: it changed the document's subject from an
  instance to a class and left four operative sentences speaking of the instance, so
  it strengthened the North Star's statement while weakening the Non-Goals' grip.
  Three of the four rewords existed only in that gap. Fixed in this same version:
  the Non-Goals scope appositive now reads "every skill in the family, present or
  future" and states that earning a trigger never exempts a sibling from a Non-Goal
  (the class-vs-instance attack had survived only on the head phrase); Non-Goal 3's
  deixis — "here", "this repository" — replaced by "any repository the product ships
  from", since a family may ship from more than one and the mechanical test had lost
  its unique referent; the residual singulars promising filesystem-completeness and
  devPNT-optionality now bind every skill, closing a sibling that requires devPNT;
  the levels block gained the rule that each sibling restates the three boundaries in
  its own units, because a non-code sibling could otherwise truthfully report that
  L1 is empty in its domain and leave "a trivial change stays one step" — the only
  absolute rule here — with nothing to attach to; and the anti-fork clause now also
  catches carving out work an existing skill already governs, with an evidence
  standard ("name what they cannot do"). One pre-existing finding fixed by owner
  decision while open: the work-management closure covered keys and presentation
  transforms but not **aggregation**, so a readiness board assembled entirely from
  admitted per-document fields passed — the closure now names collection into a
  single surface as itself the forbidden capability. Refused this round, logged to
  the standing battery: the unscoped default-deny in the admission test, and the
  three incompatible senses of "plan". **Confirming blind round: FAIL — all four
  reworded attacks got through again, two of them as restatements of the very idea
  the round-1 fixes had just closed, plus seven new classes.** That is the pattern
  `vision.md` §7 names as the specific waste to avoid — the same class of defect in a
  new disguise — so the response was not a third round of patching the same clauses
  but a change of approach, on the round-1 reviewer's own diagnosis: **the round-1
  fixes were all defined by shape, and shape is what the proposer controls.** What
  changed in consequence: (a) the amendment stopped adding a gate — the sibling
  admissibility test invented in the first draft is **removed** from the North Star,
  which now states only what the family *is*, because a new gate clause in the
  document's least-tested section is where every sibling attack landed; (b) the veto
  it was trying to express became a Non-Goal stated by **function and outcome** —
  *one triage authority per kind of work*, vehicle-independent (sibling, mode,
  package or devPNT feature), removal tested for effect rather than for occurrence,
  which is what defeats both the carve-out and the devPNT-triage attacks; (c) the
  work-management prohibition was restated by **the question answered** rather than
  by the forms that answer it, closing derivation-on-demand and shipped procedures —
  the attack that used this document's own operative-guide mechanism as its vehicle;
  (d) the competitor rule became a **counterfactual over behaviour** rather than a
  test over files, since deleting the file was enough to pass the file test while
  keeping the coupling; (e) each sibling's L1 boundary is now ruled by the owner and
  must cover its domain's commonest small change, because delegating the definition
  to the bound party let a sibling keep L1 non-empty and empty of reach. All eight
  reworded attacks and the seven new classes are in
  `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`. Pre-existing defects orthogonal
  to this amendment — the two conflicting defaults for unreached proposals, the
  absence of any re-admission when a capability's scope grows, the self-declared
  maintenance exemption, and the remaining shape-defined rules — are **not** fixed
  here: they predate the family and rewriting them inside a consolidation feature
  would put half the Vision beyond the reach of its own gate. They are their own
  work, with a battery already written against them.
  **What the amendment cost, recorded because the number is the evidence: four blind
  rounds.** Round 1 PASS-conditional; round 2 FAIL (the round-1 fixes were shape-defined
  and all four attacks re-broke them); round 3 VOID — author error, the excerpt omitted
  three binding sections including half the veto limb — and its re-run on the complete
  gate returned FAIL with 7 of 9 surviving. That re-run found the defect no earlier
  round could see, because the gate had never been in the room: **the amendment had made
  the North Star declare a family the admission test could not admit**, since every
  Goal, Actor and Signal stood at software-methodology altitude. Fixed with Goal 7,
  Actor 4 (*Practitioner in a non-code domain*) and the owning-domain rule. A fourth,
  narrow round tested exactly those: **a knowledge sibling now rules ADMIT on its merits,
  and a project-management sibling is still refused three times over** — including by
  Goal 7 itself, on *"adding no capability the family lacks"*. That round also found two
  BLOCKs inside the new clauses, both fixed here: ownership was capturable because the
  frontmatter declaration outranked the criterion (now the criterion decides, frontmatter
  records, and a change of owner passes the admission test), and Goal 7 was
  self-referential — "advancing the family is advancing this Goal" made the family's
  *size* the thing moved, which is the scope creep the test already refuses; what moves
  is the practitioner's work. Promoted on that evidence, with the pre-existing defects
  routed to F-023 rather than absorbed here. Disposition:
  `solutions/ANALYSIS_multi_domain_core.md` and `solutions/ANALYSIS_vision_shape_rules.md`;
  every attack and its class: `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`.
- **v6 — 2026-07-27, APPROVED by Antonio Pinto.** The sixth blind round was asked
  not only to attack the text but to explain *why* the surviving rules survive.
  Its answer became `vision.md` in the skill — the drafting discipline that makes a
  Vision verifiable on the first draft instead of the sixth. Applied here as five
  repairs the same round named: the anti-coupling rule restated as a **property of
  the code** (it previously forbade a *promise*, and a proposer just promises the
  opposite); "a record of work" given a checkable subject definition and its key
  list closed **by intent** rather than by enumeration (a "ready" view keyed on
  dependency walked through the enumerated three); "charge" redefined **by effect**
  (the old mechanism list — payment, account — was bypassed by consent-to-telemetry);
  the ceremony ban extended above L1 as a **budget** (it protected only the rung it
  named, so ceremony relocated upward was free); and the exempt path given a
  **default plus a disclosure burden** (a metering quota could be "fixed" as a bug
  because nothing forced the proposal to name its metered unit). Also: met signals
  say how they can still be advanced, and an accepted change may no longer
  contradict a stated fact here without amending this document in the same change.
- **v5 — 2026-07-27, APPROVED by Antonio Pinto.** A fifth blind round rejected all
  nine adversarial proposals, including every reword that had defeated an earlier
  version, and could not construct a new bypass for the metering or work-management
  rules. What it did find, and this version closes: the chargeable list (`semantic
  analysis`, `independent review`) intersected the never-meter list (`indexing or
  summarizing one's own repository`, `attesting`) — the same capability blessed and
  forbidden in adjacent paragraphs; the first enumerated consequence was
  unconditional and so rejected the paid layer outright; a locally-obtainable
  outcome could be metered by wrapping it in a team-visible shell; the maintenance
  exemption could launder a forbidden capability as a bug fix; the anti-coupling
  rule forbade supporting a new AI client; and nothing committed to the product
  being installable or maintainable.
- **v4 — 2026-07-27, APPROVED by Antonio Pinto.** Closes what v3's own wording
  opened, found by a fourth blind round: `hosted copies` was listed as chargeable
  while `mirroring` was listed as never chargeable (same thing, opposite answers);
  `removing devPNT never strands a capability` was unqualified and so forbade the
  paid layer outright; the Non-Goals never named their subject, so a work tracker
  shipped inside devPNT escaped them. Also states the L1/L2/L3 boundaries in this
  document (Signal 1 requires a reader with only `ai_docs/`, so routing the
  definitions to `SKILL.md` made the signal unsatisfiable), marks the
  work-management test disjunctive, admits the agent's reading cost as real
  process cost, and moves the prose rule out of the Non-Goals where it could never
  fire.
- **v3 — 2026-07-27, APPROVED by Antonio Pinto.** Structural, after a third blind
  round showed v2's patches opening the next seam: three separate commercial
  Non-Goals were three attempts at one principle nobody had written down, so
  `capability`, `the skill` and `amplification` stayed exploitable — a "paid-layer
  guide attestation, free tier 20/month" cleared every literal rule. Replaced by
  `## The user's guarantee`, whose dividing line is a question with an answer:
  *could the user obtain this locally from their own data?* Also: the admission
  test now counts Actor commitments (multi-client support was undecidable without
  it) and no longer rejects documentation work; the work-vs-intent line and the
  `SKILL.md` location are stated instead of implied.
- **v2 — 2026-07-27, APPROVED by Antonio Pinto.** Fixes the four BLOCKERs the
  round-2 blind check raised against v1: the admission test could reject work the
  document wanted (now Goal-or-Signal, and scoped to capability changes); the
  Non-Goals did not say whether they bind the devPNT layer (now they do); the
  North Star made an unfalsifiable superiority claim, violating this document's
  own Non-Goal; and the risk levels were used but never defined.
- **v1 — 2026-07-27.** Rewrite after a blind-reviewer clarity check (F-017) found
  the previous text undecidable to a cold reader — most sharply, a proposal to
  meter a free user's operative guides was admissible on its literal text.
- **Superseded — approved 2026-07-02.** Retrievable at
  `git show b35b36e:ai_docs/vision/project_vision.md`.
- Evidence for both blind rounds: `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`.
  Finding-by-finding disposition: `solutions/ANALYSIS_vision_clarity.md`.
