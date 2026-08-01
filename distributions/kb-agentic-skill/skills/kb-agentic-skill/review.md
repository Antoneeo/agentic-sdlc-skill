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

Never ask a reviewer to "review my session" or "review what I just did"
without the artifacts above — that forces them to reconstruct scope from
conversation instead of reviewing the change itself. Say which finding
classes you want covered (correctness, security, conformance to the design,
test coverage) if the default scope is not obvious.

## Receiving

**MUST answer findings one by one — fix, or justify with evidence; why:
silent drops turn review into theater** — a review whose findings are not
tracked to a resolution gives the appearance of quality control without its
substance.

If you disagree with a finding, say so explicitly with your reasoning; never
resolve a disagreement by rewording the finding until it goes away. When the
project keeps a `REVIEW_LOG` (or equivalent), log the outcome of each
finding there.

## Reviewing

When you are the reviewer:

- Verify claims against the real source, not against the diff's own
  description of itself.
- Cite evidence as `file:line` for every finding — a finding without a
  location is not actionable.
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

## Anti-patterns

- **Batch-dismissal**: closing out a whole findings list with one blanket
  reply instead of addressing each finding individually.
- **Rewording instead of addressing**: editing the finding's text to look
  resolved without changing the code or providing evidence it is a
  non-issue.
- **Scope-creep findings**: raising issues unrelated to the change under
  review instead of filing them separately.
