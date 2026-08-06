# Review Discipline

The single definition of how to request, receive, and perform a review. Other
places that need review behavior point here instead of restating it (DRY) —
including devPNT's §4.5/§4.6 gates and any future review step.

## When a review is due

Two moments, and they review different things:

| # | Moment | Object | Level |
|---|---|---|---|
| **1. Design review** | End of Phase 3 — **before any implementation** | the ANALYSIS (Standalone) / the `E-ISP`+`E-TDD` (Hybrid) | L3 |
| **1b. Late arrival** | Work that became L3 *after* code existed — an L1/L2 reclassified mid-flight, or a design increment on a feature already implemented — runs moment 1 **now**, before any further implementation, logged `design (late)` | same | L3 |
| **2. Closure review** | Phase 5, before DONE | the actual diff, against that approved design | L2 / L3 — the L2 row is optional |

**Why the design review is its own moment, and not a nicety.** The closure review
can only tell you the code matches the design; it cannot tell you the design was
wrong. An omission in the design — an impacted file nobody listed, a threat with no
answering requirement, a capability ruled EXISTS on an assumption — is *cheapest*
to fix before code exists and most expensive after. And the author cannot catch it:
a self-review runs in the context that produced the omission and is structurally
blind to it, which is why independence, not effort, is what this gate buys.

**Independence, best realization the client supports** — declare which one you used:

1. **A fresh subagent** (Claude Code's Task tool, or the equivalent facility) with
   its own context, given the artifacts below and nothing from this conversation.
2. **A one-shot run of the client itself** (`gemini -p "…"`, `codex exec "…"`) with
   a SELF-CONTAINED prompt — the reviewer session has no other context, which is
   exactly what makes it independent.
3. **A declared self-pass** — a separate, explicitly adversarial pass by you,
   against the same checklist. **Rung 3 is illegitimate wherever rung 1 or 2
   exists**: on a client with a subagent facility or a one-shot CLI, descending to
   it is choosing zero independence, which is the one thing this gate buys. When
   you do use it, the log row must carry *why* — `self-pass (declared; no subagent
   facility on this client)` — not merely that you did. A rung named without its
   reason is indistinguishable from a rung chosen for convenience.

Rung 3 stays in the ladder deliberately: it is what keeps the methodology
completable with no network, no account and no subagent facility. It is a floor,
never a default.

Use a different model from the author's where the client allows it.

**Rounds are capped at 3.** FAIL → revise → re-review. If findings still stand
after the third, stop and surface them to the user with the artifact — a gate that
can block forever gets removed. **Log one row per completed review, PASS or FAIL**
— a FAIL surfaced to the user is the highest-value outcome the gate produces, and
logging only passes would erase exactly that evidence. The row goes in
`ai_docs/audit/reviews/REVIEW_LOG.md` (create it if absent — `templates.md`):
`| date | doc_key | tier | reviewer | findings_raised | findings_real | verdict | revise_rounds |`,
with `tier` = `design` or `closure` in Standalone. One schema for both modes: a
Hybrid project's devPNT gates write to the same file.
The log is how the gate's value is measured over time; skipping it makes the gate
unfalsifiable, the same defect as an unnamed EXISTS or a faked router verdict.

**The reviewer is read-only and advisory.** It never edits, never commits, never
marks anything DONE, and a PASS is not an approval to merge — the human owns that.

## Requesting

When you hand work to a reviewer (human or agent), give them:

- **Scope**: what changed and why, in one or two lines.
- **The authoritative design artifact**: the ANALYSIS, E-TDD, or equivalent
  the change was built against — not a paraphrase of it.
- **The actual diff**: the real changed files, not a description of them. (For a
  **design** review there is no diff yet — that is the point; hand the artifact
  plus the constraints below, and say the object under review is the design.)
- **For an impact/solution-analysis review, the constraints it derives from**:
  the **Vision**, including its `## Actors` (Hybrid: the `M-VISION`; Standalone:
  `project_vision.md`/`roadmap.md` + the ANALYSIS Vision-Alignment), the
  **use-cases / user-needs** (Hybrid: `D-UC`;
  Standalone: the ANALYSIS `## Use Cases / User Needs`), and the **threat model**
  (Hybrid: `P-TM`; Standalone: the ANALYSIS `## Security and Threat Model`). Hand these
  *in addition to* the design artifact — the reviewer checks the artifact **against**
  them, not only for internal consistency.
- **For a design review, the threat model too** (same sources as above). Why this
  one and not the whole set: file coverage crosses the impact-analysis→design hop on
  a mechanical gate (every impacted file needs a design block), so a dropped file is
  caught; **threats have no such gate** — a threat answered in the impact analysis
  can silently fail to become a security requirement in the design, and the later
  code review only verifies the requirements that are there, never the ones that
  should have been. The design reviewer checks that every threat surface the change
  touches has a matching security requirement.

**The verdict travels back as the reviewer's own final output** — the text it
returns when it finishes, nothing else. A reviewer that tries to message the
requester mid-run depends on a delivery channel it cannot verify (a subagent
addressed by agent TYPE rather than by session gets no such channel, and the
attempt fails silently); a requester that waits for such a message stalls
holding a verdict that already exists. State the return form when you request
the review, and read the verdict where it actually arrives.

Never ask a reviewer to "review my session" or "review what I just did"
without the artifacts above — that forces them to reconstruct scope from
conversation instead of reviewing the change itself. Say which finding
classes you want covered (correctness, security, conformance to the design,
test coverage) if the default scope is not obvious.

Never pre-judge findings for the reviewer: do not instruct them to ignore or
not flag a specific issue ("don't treat X as a defect", "at most minor"). If
you believe a finding would be a false positive, let the reviewer raise it and
resolve it with evidence in §Receiving — pre-judging is usually the requester
sparing themselves a round.

## Receiving

**MUST answer findings one by one — fix, or justify with evidence; why:
silent drops turn review into theater** — a review whose findings are not
tracked to a resolution gives the appearance of quality control without its
substance.

If you disagree with a finding, say so explicitly with your reasoning; never
resolve a disagreement by rewording the finding until it goes away. When the
project keeps a `REVIEW_LOG` (or equivalent), log the outcome of each
finding there.

### Review-driven corrections (scoped re-review)

A fix made in response to a finding is new, unreviewed work — stopping after
"I fixed it" ships the one version nobody reviewed. Every review-driven change
therefore gets a **scoped re-review** before the review can PASS: hand the
re-reviewer the original findings and ONLY the correction (the fix diff/range
for code, the amended sections for a document), and require a per-finding
verdict — `ADDRESSED`, `NOT ADDRESSED`, or `CONTESTED` with evidence. **A PASS
that carried findings is provisional until its corrections pass that round** —
the commonest real case is a PASS with non-blocking findings the author then
fixes, and stopping there ships precisely the unreviewed version this rule
exists to catch. The re-review also checks the correction itself for new
blocker-level breakage — and nothing else: out-of-scope observations become separately
recorded findings, never an extension of the loop. Expect two rounds as the
norm, not the exception — round 1 finds, round 2 verifies the fixes — inside
the same cap of 3 (§When a review is due). One logical review stays ONE
REVIEW_LOG row — a scoped re-review is a round, not a new review — with the
rounds narrated in the row's notes and **the verdict column carrying the
round-1 verdict and the final one (`FAIL → PASS`), never the final one alone**:
a first-round FAIL is the highest-value evidence the gate produces (§When a
review is due), and collapsing it into a bare `PASS` erases exactly that.

## Reviewing

When you are the reviewer:

- Verify claims against the real source, not against the diff's own
  description of itself.
- **Your verdict is your final output.** Deliver findings and verdict as the text
  you return when you finish — never only through a message to the requester, a
  channel you cannot verify and which fails silently when it is not there
  (see `## Requesting`).
- Cite evidence as `file:line` for every finding — a finding without a
  location is not actionable.
- **An unproven completion claim is a finding** (closure reviews, on the diff).
  When the work under review states or implies that something passes, is fixed,
  is clean or is complete, the evidence must be present and must post-date the
  final relevant change; a claim resting on a stale run, on a narrower check
  than the claim needs, or on a delegated agent's own report rather than the
  diff, is a finding — name the claim and what would prove it. This is the
  enforcement point of the author-side rule in `SKILL.md` §5 Closure, and the
  reason a requester hands it over is that the reviewer cannot cite a rule it
  was never given.
- **Say what you could NOT verify.** When a claim in the artifact cannot be
  verified from the inputs you were given (it lives in unchanged code, another
  document, or an environment you cannot reach), report it as a
  `CANNOT VERIFY` item instead of silently passing it — the requester holds
  the context to resolve it, and must do so before closing. A PASS that
  silently skipped unverifiable claims is review theater.
- Keep severity honest: do not inflate a style preference to a blocker, and
  do not soften a real correctness or security issue to a nit.
- No praise padding. A review reports problems and their fixes, not a
  summary of what looks fine.
- **Conformance statement (impact/solution-analysis & design reviews only — not a
  plain code-diff review).** When the artifact under review carries Vision / use-case
  / threat-model constraints, your output MUST map each constraint to its evidence: for
  every use-case/user-need (and the Actor it serves — a use-case with no defined Actor,
  or an Actor UX expectation the solution does not meet, is a finding), every threat, and
  every applicable Vision benefit/Non-Goal, state WHERE the artifact satisfies it (section
  or `file:line`) or raise it as a finding. A PASS/approve is **not valid on "found nothing"** — the conformance
  statement is the proof the check ran; an unfalsifiable "I checked" is the review
  theater this discipline exists to prevent (the reviewer-side twin of §Receiving's
  silent-drop rule). Plain code reviews stay findings-only.
- **Restated facts (cite, never copy).** Every governance slot has ONE owning document
  per project. A fact restated in the artifact under review when another document owns
  it is a **finding**: the fix is a citation naming the owner, not a better copy. This
  binds the conformance statement too — where a constraint is satisfied by another
  document, name that document as the evidence instead of repeating what it says. Two
  copies of one fact diverge at the first edit, and the reader then has no way to tell
  which one is current. The rule bites hardest across domains, where the same slot
  ("threat model", "vision", "handoff") carries a different meaning under each lens and
  a copy looks like an independent second source.
- **Use-case grounding (same reviews; the two-check gate whose owning definition
  is the code lens's `templates.md` `## Use Cases / User Needs` comment — cite it,
  never restate it).** On an L3 impact/solution analysis (Standalone) or `D-UC`
  (Hybrid), two findings live here and nowhere else: **a product name in no
  bucket** — the use-cases name a thing that neither EXISTS in the product (called
  by the term the product itself uses; a renamed existing thing is a phantom), nor
  is declared NEW in this change, nor is a pure METAPHOR kept out of the interface;
  it invents system reality that is not there. And **a use-case that traces to no
  Vision / M-VISION benefit** — a need the vision does not want, which is drift.
  This gate checks the use-cases are GROUNDED and runs BEFORE the owner's own
  review, never replacing it; coverage of each use-case by the Impact, and the
  Actor it serves, stay the conformance-statement clause above. A lens whose
  template defines no `## Use Cases` section never fires this clause.
- **Functional Spec (same reviews; fires only in the lens whose template defines
  the section — the code lens today).** When the change adds or alters observable
  behavior (the trigger's owning definition is the code lens's `templates.md`
  `## Functional Spec` section comment — cite it, never restate it), **an L3
  artifact carrying NO `## Functional Spec` is itself a finding** — absence is
  what a skipped spec looks like, not a reason to skip the check. When the spec
  is there, these findings live here: **a component, file or mechanism named
  inside it** — the spec is component-free by construction; that is
  Solution-leakage (component names belong to the Interface Contract, mechanism
  to the Impact); a behavior whose edge, error or state-dependent cases are
  absent with no stated reason; an acceptance criterion no `## Test Strategy`
  item covers; a behavior serving no use case, or a use case whose behavior the
  spec leaves unstated; and an Interface Contract flow realizing a behavior the
  spec does not state. A lens whose template defines no such section (knowledge,
  marketing) never fires this clause.
- **Capability Ledger (same reviews).** **An L3 impact/solution analysis or design
  that carries NO Capability Ledger is itself a finding** — the lens's capability
  pass (`architect.md` in the code lens, `taxonomy.md` in the knowledge lens) left
  no record, and "the artifact does not have one" is what a skipped pass looks like,
  not a reason to skip the check. (This half is load-bearing in Hybrid, where the
  validator backstop reads Standalone ANALYSIS files only and this clause is the
  sole check that the pass ran.) When the ledger is there, map each
  ledger row to where the design or diff realizes it. Three findings live here and
  nowhere else (the capability-pass file named above): a capability ruled MISSING but implemented inside
  the feature's code path, with no component owning it; a component whose contract
  names the feature (a second consumer would force it open); and a capability ruled
  MISSING, not built, and absorbed by quietly reshaping the feature — that is a
  scope change owed to the user, not a design detail. An EXISTS row with no named
  path or symbol is itself a finding. A capability built in this change and absent
  from the `## Component Map` (`strategic/architecture.md`, where the lens keeps one) is a finding too — and
  so is **a component the pass merely DISCOVERED and did not write**, especially
  when the change marks that area ANALYZED: the area now looks read, the map is
  still silent, and the next feature may lawfully rule the capability MISSING and
  build it twice. And a **MISSING row in an area `audit/audit_plan.md` does not
  mark ANALYZED, with no searches named**, is the finding that matters most on a
  project the methodology arrived in recently — an unread map reported as an empty
  one is how a duplicate of the existing codebase gets designed.
- **Interface Contract (same reviews; fires only in the lens whose template
  defines the section — the code lens today).** When the change creates or
  modifies an actor-facing surface (the trigger's owning definition is the code
  lens's `templates.md` section comment — cite it, never restate it), **an
  artifact carrying NO `## Interface Contract` is itself a finding** — "the
  artifact does not have one" is what a skipped contract looks like, not a reason
  to skip the check. When the contract is there, these findings live here: a
  use-case with no named interaction flow realizing it; **a flow that is not
  walkable at the responsibility level** — it jumps from the actor's action to
  the outcome without naming the components it traverses; **a *how* inside the
  contract** — a mechanism, algorithm, data structure, widget or file-level
  design — which is Solution-leakage (the flow NAMES components as
  responsibility-holders, it never designs them); **required feedback that omits
  an error or intermediate state, or a software actor's return status** (feedback
  is universal, not human-only); a design or diff element that alters a
  contracted surface, flow or feedback with no explicit renegotiation note (after
  design approval that is a scope change owed to the user, not a design detail);
  a contracted flow the `## Test Strategy` does not cover; and a new interaction
  idiom introduced where the contract's own as-is names an existing one, with no
  declared reason. (The architectural constraints the surface must live with are
  NOT checked here — architecture-awareness is the Capability Ledger / Impact
  review's job; a clause for it would duplicate that.) A lens whose template
  defines no such section (knowledge, marketing) never fires this clause.

## Anti-patterns

- **Batch-dismissal**: closing out a whole findings list with one blanket
  reply instead of addressing each finding individually.
- **Rewording instead of addressing**: editing the finding's text to look
  resolved without changing the code or providing evidence it is a
  non-issue.
- **Scope-creep findings**: raising issues unrelated to the change under
  review instead of filing them separately.
