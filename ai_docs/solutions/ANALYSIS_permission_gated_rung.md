---
id: F-037
feature: a review rung that exists but needs the user's authorization is not "unavailable" — ask at the gate instead of descending
status: CANCELLED
level: L3
start_date: 2026-08-25
end_date: 2026-08-25
---
# Feature Analysis: the permission-gated rung

## Outcome — CANCELLED at the review cap, kept as the record

Three design-review rounds, three FAILs, nothing implemented. The diagnosis survived
every round (the ladder has no truthful word for a permission-gated rung); the
mechanism — a durable, readable grant memory — died three different ways, because the
schema offers it no home. The successor unit builds the vocabulary and the mandated
ask WITHOUT grant memory (re-asking is a smaller defect than a false log row):
`ANALYSIS_gated_rung_vocabulary.md` (F-038). Kept CANCELLED rather than deleted so the
next session finds the negative result instead of re-deriving it at the same cost
(~600k subagent tokens across four reviews).

## Objective

`review.md`'s independence ladder recognises exactly two states for a rung: the client
supports it, or it does not. It has no state for **present but permission-gated** — the
facility exists, and using it requires the user's request.

The doctrine's rule for that situation is unambiguous, and it is currently unsatisfiable:

> **Rung 3 is illegitimate wherever rung 1 or 2 exists**: on a client with a subagent
> facility or a one-shot CLI, descending to it is choosing zero independence, which is
> the one thing this gate buys.

F-035's design review descended to rung 3 with the facility present. Its log row reads,
verbatim:

> `**rung 3 — declared self-pass** (independence reduced; recorded because the log is
> where that must be visible). Rung 1 unavailable: subagent dispatch off by session
> policy.`

**The reason clause is accurate; the word in front of it is not.** "Off by session
policy" is exactly right. What is wrong is `unavailable` — and the agent had no better
word, because the ladder ships two states and hard-codes rung 3's reason string as
`self-pass (declared; no subagent facility on this client)`. The defect is not a
fabricated reason: **the doctrine gives no truthful word for what happened**, so the
nearest one gets used and two different facts collapse in the log.

**The cost of getting it wrong is measured, not assumed.** That rung-3 self-pass found
five real defects and missed every platform-semantics bug in the same artifact. When
rung 1 was authorized on the same feature, it returned three blockers, the worst being
`Path.is_absolute()` returning False for `/vault/manuals/xyz.pdf` on Windows — the exact
string this project's own templates print.

*Provenance note:* the client-side instruction that gates rung 1 here is real but lives
outside this repository and in a cache key that will rot, so it is not the evidence this
design rests on. The in-repo evidence is the log row above.

## Feature Vision

Serves *"Make divergence from the declared intent visible **before** implementation, and
again before merge"* — a gate that silently runs at its weakest rung still reports
"reviewed", which is a divergence made invisible.

Also serves *"Never hide a conflict... surface it and let the user choose."*

**Ceremony budget.** An earlier draft claimed this was a cost-neutral replacement and
owed no budget item. That was wrong on who pays: the action removed is an agent writing
a log clause; the action added spends the *user's* attention and stalls the turn, which
`elicitation.md` names in its opening line. Different payers, different currencies.

The motivation is that `review.md` already forbids rung 3 wherever rung 1 exists, and on
a gated client that prohibition cannot be obeyed without asking — the ask is the means of
compliance with a rule already in force. **That motivation does not by itself clear the
Non-Goal**, which offers only two dispositions: remove something of comparable cost, or
state the cost and have the owner accept it explicitly. This change takes the second.

**The cost, stated for explicit acceptance:** at most **one question per governed unit of
change** — an L3 gate that was already due — plus the stall until it is answered.
L1 pays nothing: no gate is due. L2 pays nothing: the L2 closure review is optional, so
no L2 gate is mandatory. *That last clause is ambiguous in the source today
(`review.md`'s table says "the L2 row is optional", and "row" elsewhere in the file means
a REVIEW_LOG row), so this change disambiguates it rather than leaning on a reading —
the Vision resolves an undisclosed load-bearing fact against the proposal.*

**"Permission-gated" is defined, or the bound is decoration.** It means: *a standing
policy or instruction that forbids invoking the facility absent a user request.* An
**interactive per-call approval prompt is NOT this** — there the user is already in the
loop and answering the prompt IS the grant, so the rule must not fire.

**Rung 2 pre-empts the stop.** If an ungated rung 1 or a working rung 2 exists, the
prohibition is already satisfiable and there is nothing to ask about. The stop fires only
when **no ungated rung is usable**, and an available rung 2 must be tried, or shown to
fail, before asking. This case is live in this repository: F-035's row records rung 2
attempted twice before the descent.

**Explicitly NOT in scope: proposing subagents generally.** The tempting version is "the
skill should offer subagents when useful". That is an open-ended licence to interrupt, it
fires outside the gates, and it converts a precise doctrine into a habit.

## Use Cases / User Needs

- **Owner running a governed change** — is asked once for that unit, at the moment the
  gate is due, with cost and benefit both stated, instead of reading afterwards that the
  review ran at its weakest rung.
- **Owner who declines** — gets what they get today (rung 3), logged as declined rather
  than as absent, and is not re-asked for that unit.
- **Owner on a trivial unit** — is not asked at all: no gate is due.
- **Owner on a client with a working `codex exec`** — is not asked at all: rung 2 is
  ungated, so the doctrine already has its independent path.
- **A later reader of `REVIEW_LOG.md`** — can tell "no facility existed" from "the
  facility existed and was declined", which are different facts about the same PASS and
  today collapse into one string.

## Capability Ledger

Architect pass run before the Impact. `skills/` is ANALYZED in `audit_plan.md`.

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| Name the rung actually used, with its reason | **EXISTS** | `review.md` rung 3 + the log schema | re-read: the row must carry *why*, and "a rung named without its reason is indistinguishable from a rung chosen for convenience". The mechanism is right; it has no vocabulary for the gated case |
| Distinguish "absent" from "gated" | **MISSING** | — | searched `review.md`, `dispatch.md`, `SKILL.md`, `templates.md` for `authoriz`/`permission`/`consent`/`gated`: no match in any ladder or log context |
| Block at the gate, legally | **EXISTS** | `elicitation.md` §Blocking is reserved | re-read: blocking is reserved for three cases, the third being "the doctrine itself mandates the stop — and a mandated stop is legal by mandate". **But the same file's closed list of self-prescribing hand-overs names only `debugging.md`'s circuit breaker and `review.md`'s round cap; every other mandated stop CARRIES THE FIVE-BULLET FORM.** This stop is not the round cap, so the form binds — and conforming to it is why `elicitation.md` needs no edit |
| Remember a grant, readably, after a compaction | **EXISTS — via `doc_key`** | `REVIEW_LOG.md` | two earlier drafts said "once per session" and could not say what a session is. `dispatch.md` refutes conversational memory outright ("The ledger is the only memory the loop needs across sessions or **context compaction**"), and the log cannot supply the answer either: its `date` is day-granular (this file already carries eight rows dated 2026-08-25 across separate sessions) and its row is written only when a review COMPLETES — so the window the mechanism exists for is uncovered. **`doc_key` is what the schema does carry and what the filesystem can answer.** Scoping the grant per unit of change removes the undefined term entirely |
| State what a review costs before running it | **MISSING** | — | `review.md` never mentions cost. Measured: 173k / 175k / 130k / 149k subagent tokens across four deep reviews this month. A number is what makes declining a real option |

## Impact

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/review.md` | MODIFY | the rule, the mandated stop, the grant scope, the question, the cost — **shared spine**. Also disambiguates the L2 clause this design's cost disclosure rests on |
| `skills/agentic-sdlc-skill/dispatch.md` | MODIFY | carries the same two-state framing ("No subagent-spawning tool available →…") — **shared spine**; left alone it is the same defect one file over |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | the `REVIEW_LOG` schema comment gains the reason vocabulary and the grant note — per-lens, not shared |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | MODIFY | the invariant — **shared spine** |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | MODIFY | consequence: three of the files above are drift-guarded |
| `skills/agentic-sdlc-skill/evals/scenarios/gated_rung_asks_before_descending.md` | ADD | the behavioural test, in the harness that actually exists (dev-only; not in the `files` allowlist) |
| **×3 — every path above under `distributions/kb-agentic-skill/skills/kb-agentic-skill/` and `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/`** | as above | the shared files must stay byte-identical or the drift guard fails |
| `README.md` + the two distribution `README.md` files | CHECK, edit only if stale | the `audit_plan.md` rows for `skills/`/`distributions/` name the README as a standing duty of any doctrine edit — **and F-035's review caught exactly this omission one feature ago**. The ladder is not described on any README today, so the expected outcome is no edit, recorded as checked |
| `ai_docs/strategic/skill_family_agent_workflows.md` | MODIFY | restates the ladder in prose ("scala di indipendenza a 3 pioli … illegittimo se esistono i primi due") — the clause this change refines; named by the same audit rows |
| `ai_docs/audit/HANDOFF_permission_gated_rung.md` | ADD | one per OPEN workstream, or the generated registry has no row |
| `CHANGELOG.md` ×3 | MODIFY | a new dated heading at release (`[x.y.z / kb a.b.c / mkt d.e.f]`); this repo keeps no `[Unreleased]` section — the previous release consumed them |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | MODIFY | this unit's rows, and F-035's `unavailable` corrected to the gated vocabulary |

**Blast radius (enumerated).**
- Shared, must change identically ×3 and regenerate the manifest: `review.md`,
  `dispatch.md`, `test_skill_invariants.py`. `templates.md` and the evals are per-lens.
- `elicitation.md` is **deliberately not edited**: the alternative was to amend its closed
  list of self-prescribing hand-overs to admit this one. Conforming to the five-bullet
  form instead leaves that list closed, which is the smaller change and keeps one form
  over one moment — the duplication `review.md` §Reviewing forbids.
- `SKILL.md` cites the ladder rather than restating it, so it needs no edit.
- The devPNT doctrine carries its own copy of the ladder **outside this repository**;
  this change makes the two disagree until that side is updated. Named, not silently left.
- Nothing executes: the ladder is doctrine. The radius is textual plus the batteries.

## Security and Threat Model

Surface: none technical. The risk is behavioural — a rule that changes when an agent
interrupts its user, and how a governance log records what happened.

| Threat | Answer |
|---|---|
| **T1 — the rule becomes a licence to interrupt** | it fires ONLY at a gate already due, ONLY when the trigger definition above is met, and ONLY when no ungated rung 1 or 2 is usable. Not "when subagents would be useful"; the rejected broad version is a stated Non-Goal so a later reader finds the ruling instead of re-deriving it |
| **T2 — asking repeatedly trains the user to rubber-stamp** | one ask per governed unit, and the grant is recorded in that unit's `REVIEW_LOG` row, which is keyed on `doc_key` and survives compaction. Two earlier drafts said "per session" and could not define or read back a session; this is the version the filesystem can answer |
| **T3 — the ask becomes a way to shed responsibility for a weak review** | the ask does not change what a PASS means. Rung 3's rules are unchanged: adversarial, same checklist, logged with its reason |
| **T4 — the cost figure rots** | written as an order of magnitude with its provenance ("~130–175k subagent tokens per deep review, measured 2026-08"), not a budget. A stale order of magnitude still supports the decision |
| **T5 — the log vocabulary is used loosely**, collapsing `declined` and `absent` | the schema comment defines the reasons and says `absent` is a claim about the CLIENT, never about a policy. **Stated limit:** the reason is free text inside the `reviewer` column, not a column of its own, so nothing constrains it mechanically. The guard is a reader's; the eval scenario is what tests the behaviour |
| **T6 — wait semantics: does the agent stop, or ask and carry on?** | an earlier draft answered with the non-blocking default, which guts the feature: ask-and-proceed runs the review at rung 3 before an answer can arrive, so the rule could be fully complied with while delivering nothing. The default did not even apply — `elicitation.md` scopes it to "an unknown on which **no fork of the work depends**", and this fork does. The rule **mandates the stop**, legal by mandate, and carries the five-bullet form |
| **T7 — `no answer` becomes a legitimate-looking way to skip rung 1** | the sharpest objection: it would turn an unconditional prohibition into one with an exit. With a user present the gate **stops**, so `no answer` is not reachable — it exists only on the unattended path, where there is no user to ask and rung 3 was always legitimate. **An earlier draft answered this with a "provisional, re-runs if the grant arrives" clause; that is deleted.** It created an obligation nothing tracked, collided with `review.md`'s existing meaning of *provisional* (a PASS carrying findings), and left an after-the-fact verdict change undefined against the rule that the verdict column carry both rounds. The unattended bound alone closes the exit |

## The question the rule prescribes

`elicitation.md` closes its list of self-prescribing hand-overs at two — `debugging.md`'s
circuit breaker and `review.md`'s round cap — and says every other mandated stop carries
the five-bullet form. This stop is a third moment, so it conforms rather than amending
the list:

> - **The fork:** run this review at rung 1 (a fresh subagent, its own context) or at
>   rung 3 (my own adversarial pass). Rung 1 finds what a self-pass structurally cannot;
>   rung 3 ships now and costs nothing.
> - **The evidence:** rung 2 attempted and failed (`<what was run, what it returned>`);
>   no grant recorded for this unit — `REVIEW_LOG.md` has no row for `<doc_key>` carrying
>   one, and none in this conversation; the client's standing instruction reads
>   `<quote>`. What that leaves undecided: whether you want the cost here.
> - **Why no assumption survives:** the doctrine mandates this stop — rung 3 is
>   illegitimate wherever rung 1 exists, and here rung 1 exists behind your request, so
>   assuming either way puts a false reason in the log.
> - **Why it is your call:** it spends your tokens (~130–175k per deep review, measured
>   2026-08) against a benefit only you can price. What it bought last time: three
>   blockers a self-pass had missed, one a platform-semantics bug.
> - **Blocked until answered:** which reviewer runs. Nothing else — implementation is
>   already gated behind this review.

Both legality limbs are on its face: the **named search with its result**, covering the
grant's own home (the log, keyed on `doc_key`) and not only the conversation the design
elsewhere declares unreliable; and the decision blocked. It states **both sides** — a
question carrying only the cost is leading, biased toward the answer that keeps rung 3,
by the same logic `review.md` uses to forbid pre-judging a reviewer's findings.

## Action Plan

1. `review.md` — the fourth state, the mandated stop with its form, the per-unit grant,
   the rung-2 precedence, the trigger definition, the cost; and the L2 clause
   disambiguated. RED first (invariant).
2. `dispatch.md` ×3 — the same two-state framing corrected.
3. `templates.md` ×3 — the reason vocabulary and the grant note.
4. `test_skill_invariants.py` ×3 — the invariant, mutation-tested.
5. `evals/scenarios/gated_rung_asks_before_descending.md` ×3 — the behavioural test.
6. `shared_files.py --update` + propagate; correct F-035's row; add this unit's rows.
7. `HANDOFF_`, strategic doc, README check, CHANGELOG ×3, `index`, batteries ×3 + drift.

## Test Strategy

- **Invariant**: `review.md` carries the gated state and the rung-2 precedence — asserted
  on the ladder section, so it fails when the rule is deleted rather than when the file
  is edited anywhere. Mutation: remove the paragraph → fails.
- **Invariant**: the three copies of each shared file stay byte-identical (`test_drift.py`
  already enforces it; keeping it green is the assertion).
- **Behavioural**: `gated_rung_asks_before_descending.md` puts a cold agent at an L3
  design gate on a client whose subagent facility is permission-gated, and fails if it
  descends to rung 3 without asking. The harness exists and already tests this shape —
  `verdict_declared_on_no_match.md` distinguishes "looked, nothing fitted" from "never
  looked". An earlier draft claimed no behavioural test was possible; that was wrong.
- **Log-reading guard, with its limit**: a row claiming `absent` on a client that has a
  Task tool is a detectable lie. It catches a reader's eye, not a validator's, and it
  would NOT have caught F-035's row, which said `unavailable`. That row is corrected here
  as the worked example of the word the ladder failed to provide.
- **Family**: batteries ×3, drift guard identical, `npm pack` ×3 — `review.md` and
  `dispatch.md` ship, so tarball content changes; verify both are still listed and the
  new eval scenario is NOT.

## Diary / Current State

**2026-08-25 — round 3 (the cap): FAIL. Stopped and surfaced, NOT implemented.**
`review.md` caps rounds at 3 — *"if findings still stand after the third, stop and
surface them to the user with the artifact — a gate that can block forever gets
removed."* Six blockers stand. Three were spot-verified by the author against live
source before reporting:

1. **The `doc_key` grant cannot key a unit of change.** `templates.md`'s own schema
   example shows ONE unit producing TWO rows — `ANALYSIS_login_sso.md` (design) and
   `diff feature/sso-login` (closure) — and the real F-035 pair does the same. So a
   grant recorded at the design gate is unfindable at the closure gate, and the
   disclosed cost is understated by a factor of two. Under this project's own
   precedent (F-021), a misstated ceremony cost voids the recorded acceptance.
2. **The grant is on disk nowhere in the window it exists for.** Changing the key did
   not change the write time: the row is written per *completed* review, and one
   logical review spans up to three rounds in one row. The compaction window is
   exactly the gap.
3. **`README.md:17` already describes the ladder** — *"a declared self-pass, legal only
   when the first two are **unavailable**"* — the precise word this design exists to
   retire, on the npm front page. The Impact row claimed "the ladder is not described
   on any README today". That is false, and it is the same omission this project's
   review caught one feature ago on F-035.

Also standing: two mandatory conditional sections (`## Functional Spec`,
`## Interface Contract`) missing with no waiver; three impacted files unnamed with
validator consequences (`features_history.md` — F-037 is divergent right now and
`validate` errors on it — plus `handoff.md` and `audit_plan.md`'s `mark`); and the
unattended bound, which after the re-run deletion carries the whole `no answer`
closure, left undefined and absent from the Action Plan.

**Author's read, for the owner's decision.** The direction is right and the diagnosis
holds: the ladder genuinely lacks a truthful word for a gated rung, and that is a real
defect with real consequences in this repo's own log. What failed three times is the
*mechanism* — every round, the attempt to give the grant a durable, readable home
produced a new contradiction, because no such home exists in the schema. The version
worth building may be much smaller: **add the vocabulary and the rule, and build no
grant memory at all.** An agent that cannot recall a grant asks again; gates are rare,
the question is cheap, and re-asking is a far smaller defect than the three mechanisms
that failed here. That is a different design and needs its own pass, not a fourth round
on this one.

**2026-08-25 — design review, round 2 (rung 1), FAIL again; simplified rather than
patched.** Round 2 found four blockers, one of them *created by* round 1's fix. The
findings converged on a single root: **"once per session" is not answerable from the
filesystem.** `session` is undefined across the whole spine, `dispatch.md` says
conversational memory does not survive compaction, the log's `date` is day-granular (eight
rows already share 2026-08-25), and the row is written only when a review *completes* —
so the compaction window the mechanism existed for was uncovered. Two rounds of patching
it produced a third contradiction: the prescribed question searched "this conversation"
while the design declared conversation unreliable.

So the grant is now scoped **per unit of change, keyed on `doc_key`** — the one key the
schema already carries and the filesystem can answer. The undefined term disappears, the
search has a real home, and the bound gets tighter rather than looser.

Two further simplifications, both deletions:
- **The "provisional, re-runs at rung 1" clause is gone.** It was round 1's fix for the
  `no answer` exit and it introduced an untracked obligation, a term collision with
  `review.md`'s existing *provisional*, and an undefined after-the-fact verdict change.
  With the stop mandated, `no answer` is unreachable with a user present; the unattended
  bound alone closes the exit, and nothing needs tracking.
- **"which is why it is not a ratchet" is gone.** The Non-Goal offers no such exemption;
  invoking its stated-cost branch one line later contradicted it, and told the owner
  there was no cost while asking them to accept one.

Round 2 also caught the closed list in `elicitation.md`: every mandated stop outside two
named files carries a five-bullet form this design had not reached. Conforming to it is
what keeps `elicitation.md` unedited and the list closed.

**2026-08-25 — design review, round 1 (rung 1), FAIL, five blockers, all folded.**
The rule's own gate applied to itself. The ceremony-budget "replacement" argument was
wrong on who pays; wait semantics were unspecified and would have let an agent ask and
proceed in the same turn; that gap opened a new rung-3 exit; the question was declared
legal "by construction" while discharging one of two mandatory limbs; and "once per
session" rested on a Ledger row that ruled session state MISSING off a four-keyword
search. Four WARNs folded too — the F-035 claim was overstated, the eval harness exists,
two carriers of the same framing were missing from the Impact, and the question stated
cost without benefit.

**2026-08-25 — opened.** Standalone, devPNT off. `Level: L3 · router: no match`.
Branch `feat/permission-gated-rung` off `main`@5f2edcf.

Trigger: the owner asked whether the skill should tell the agent to propose subagent use,
warning about token cost. The answer is narrower than the question. The doctrine already
forbids descending to rung 3 when a higher rung exists, so the defect is not a missing
suggestion but a missing *state*. Encoding "propose subagents when useful" would have
been the broader, worse change, and it is recorded as a Non-Goal.
