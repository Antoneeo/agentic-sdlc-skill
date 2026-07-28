# The Architect Pass

Applies at L3, in phase 3, AFTER the spec elicitation and BEFORE the Impact is
drafted. It answers the one question the Impact cannot ask: *does the system
already have the components and services this feature needs?*

Why it exists: **a feature is not a unit of construction.** Left alone, an agent
designs the feature and builds whatever it lacks inside the feature's own code
path — so no component owns the capability, the next feature that needs it
rebuilds it differently, and the platform accretes feature-shaped code nobody can
reuse. That is myopia one level above the file: the change is complete, the tests
pass, and the architecture is worse.

## 1. State the feature as capabilities, not as files

Write what the system must be able to DO for this feature to exist — "persist a
draft across sessions", "notify a third party asynchronously", "authorize per
tenant". A capability is a verb over a domain noun. It names no file, no class and
no library: **that** is the decoupling. Files come later, in the Impact.

Two or three capabilities is a normal feature. When the list has one obvious entry
and it plainly exists, say so in one line and move on — this pass is a question to
answer, not a form to fill.

## 2. Rule each capability against the platform

One verdict per capability:

| Verdict | Meaning | What the row must carry |
|---|---|---|
| **EXISTS** | a component already owns this capability and covers the need | the component and where it lives (path / symbol) |
| **INADEQUATE** | a component owns it but does not cover the need | the same, plus the gap in one line |
| **MISSING** | no component owns it | what you searched to conclude that |

Read the **`## Component Map`** in `strategic/architecture.md` first — the project's
inventory of what owns which capability, kept so this pass does not re-derive the
platform from source every session.

**The map is a cache of evidence somebody already paid for. It lowers the COST of a
verdict, never the STANDARD of one.** Every verdict carries the same evidence
whether the map answered it or not; a hit means the search is already written down,
a miss means you pay full price. Reading a row does not excuse you from checking
that it is still true — the map is the index, the code is the evidence.

**Its silence is unread, not empty.** The map covers only the areas `audit/
audit_plan.md` marks ANALYZED. In an area still PENDING — or SKIPPED, or absent from
the plan entirely — **the map can never ground a MISSING verdict.** Nothing there
has been looked at yet, and "the inventory does not mention it" is the reasoning
that builds a second copy of a component that already exists. Search it with the
symbol-graph tool (`grep` as a fallback), and a MISSING you reach that way carries
what you searched: the terms, the tool, the areas covered. An unfalsifiable MISSING
is the same defect as an EXISTS with no symbol named.

**Understanding is never deferred; only WRITING the map is.** You may leave the rest
of the repository unmapped and grow the inventory feature by feature — you may not
leave unexamined anything this change touches or depends on. That blast zone is
understood now, at full standard, mapped or not. The incremental licence is about
the artifact, never about the comprehension.

Ground every verdict. An EXISTS with no named symbol is an assumption wearing a
verdict's clothes, and it is the row that breaks in implementation. A MISSING
declared without a real search is how duplication enters — the component may be
there under a name you did not guess. This is the DRY check at architecture level.

## 3. Design what is missing as a component, not as feature internals

INADEQUATE and MISSING produce design work of their own, governed by one rule:

**The component's contract is stated in the component's own vocabulary. The feature
is one consumer, never the owner.**

The test is mechanical: write the contract — what it does, what it takes, what it
guarantees — *without naming the feature*. If you cannot, the contract is
feature-shaped, and the second consumer will force it open.

The opposite error is equally real: this is not a licence to build a framework.
Build for the need you have, at the size you need. What the rule constrains is the
contract's **vocabulary and ownership**, not its scope — a five-line component with
a clean contract satisfies it in full.

## 4. Decide the unit of change

A capability that needs building becomes **its own ANALYSIS, its own branch and its
own closure** when ANY of these holds:

- it will have more than one consumer, now or in the declared roadmap;
- it is independently mergeable and testable without the feature;
- it carries its own risk surface: security, a public contract, a data model, or a
  new dependency.

Otherwise it is a **phase inside this feature's plan** — the first phase, before the
feature consumes it — and it is still a component: own contract, own tests, never
inlined into the feature's code path. **The split rule decides the paperwork; it
never decides whether the component exists.**

When it does become its own unit, each document names the other: the feature's
ANALYSIS points at the component's, and the component's lists its consumers.

## 5. Order

The component is designed before the feature that consumes it, and normally built
and tested before it too. A feature blocked on a capability it does not have is not
"in progress" — it is a component task wearing a feature's name.

## Anti-patterns

- **Inlining** — the capability is implemented inside the feature's code path and no
  component owns it. Symptom: the next feature that needs it must copy it or
  refactor yours. This is the failure the pass exists to prevent.
- **Feature-shaped platform** — the component exists, but its contract speaks the
  feature's vocabulary. Symptom: the second consumer forces a contract change.
- **Silent degradation** — a capability comes out MISSING, nobody wants to build it,
  so the feature is quietly reshaped around what exists and ships as less than what
  was asked. The reduced benefit must be surfaced to the user as a scope change and
  recorded in the ANALYSIS; absorbing it silently is the Vision-divergence rule
  broken one level down.
- **Speculative platform** — a general framework built for a single known need.
- **Paper ledger** — every row EXISTS, nothing named. Unfalsifiable, exactly like a
  review that reports "I checked".
- **Empty-map MISSING** — ruling a capability MISSING because the Component Map is
  silent about it, in an area nobody has analyzed yet. The map's silence is
  *unread*, not *empty*. On a project the methodology has just arrived in, the map
  is nearly all silence, and this is the anti-pattern that duplicates the existing
  codebase one component at a time.

## Where the output is recorded

Standalone: the `## Capability Ledger` section of the ANALYSIS (`templates.md`),
immediately before `## Impact`, which it feeds — every INADEQUATE or MISSING row
lands there as files to create or change. The closure review maps the ledger row by
row (`review.md`).

**A component that gets built lands in the `## Component Map`** of
`strategic/architecture.md`, in the same closure — capability owned, contract,
where it lives. This is the loop that makes the pass repeatable instead of
per-session: the ledger asks the map what exists, so a component the map never
learned about is one the next feature rules MISSING and builds a second time. The
trigger is the component's birth, not a stack change (Write Triggers).

**So does a component you merely discovered.** When the pass searches an unmapped
area and finds an existing owner, write that row too, and `sdlc_check.py mark` the
area you covered. The map then grows by the feature that needed the knowledge
instead of by an up-front sweep — the understanding was paid for either way, and
this is the step that stops the next session paying for it again.

Hybrid: the ledger goes in the `E-ISP`, above its Impacted Components map. A
capability split out as its own unit of change gets its own `E-ISP`/`E-TDD`, and the
feature's `E-ISP` names it as a dependency.

## Mechanical backstops

Prose is not enforcement; these are the checks that notice when the pass did not
run or its output rotted (`sdlc_check.py`, warnings — never a gate):

- **Skipped pass**: `validate` warns when an ACTIVE (PLANNED/IN_PROGRESS) L3
  ANALYSIS started on/after 2026-07-28 lacks `## Capability Ledger`. Closed
  history and analyses born before the pass existed never nag — the same
  lazy-convert doctrine as the pre-1.17 handoff.
- **Rotting map**: `validate` resolves every path-shaped ref in the Component
  Map's `Where` column — a path that no longer exists, or a `#symbol` no longer
  present in the file, is flagged. This is the map's equivalent of the guides'
  `source_hash`: freshness detected, not trusted.
- **Adherence** (non-gating, `evals/`): `architect_rules_before_impact.md` runs
  the pass cold; `unmapped_never_grounds_missing.md` sets the brownfield trap —
  an existing component in a PENDING area, where ruling MISSING from the map's
  silence is the failure.

## Below L3

L1 and L2 do not run this pass. A capability discovered MISSING during L2 work is
itself an escalation trigger: stop, reclassify to L3, declare it (Rule Zero). "The
component was not there" is never a reason to build it inside an L2.
