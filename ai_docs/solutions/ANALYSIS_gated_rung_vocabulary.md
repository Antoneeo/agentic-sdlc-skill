---
id: F-038
feature: the gated rung — truthful log vocabulary and a mandated ask, with NO grant memory
status: COMPLETED
level: L3
start_date: 2026-08-25
end_date: 2026-08-26
---
# Feature Analysis: gated-rung vocabulary and the mandated ask

## Objective

Successor to F-037 (CANCELLED at the review cap — read its Outcome section first). What
survived three review rounds is the diagnosis; what died three ways is grant memory.
This unit builds the first and refuses the second.

**The defect.** `review.md`'s independence ladder knows two states — the client supports
a rung, or it does not — and hard-codes rung 3's reason string as *"no subagent facility
on this client"*. A rung that exists behind a standing permission policy has no truthful
word, so F-035's log row wrote `unavailable` for a facility that was present, and
`README.md:17` ships the same word on the npm front page. Worse than the word: the
doctrine's own prohibition ("rung 3 is illegitimate wherever rung 1 or 2 exists") is
**unsatisfiable** on a gated client — the agent cannot obey it without asking, and no
rule says to ask.

**The refusal.** No grant memory. F-037 proved, at ~600k tokens, that the schema offers a
grant no durable home: "session" is undefined and does not survive compaction;
`doc_key` keys a review object, not a unit (one unit = two rows); rows are written only
at review completion, so the write time misses the whole window. An agent that cannot
recall a grant **asks again**. Gates are rare, the question is one turn, and re-asking is
a strictly smaller defect than a false log row or an untracked obligation. Within one
conversation the answer simply holds — including a "for the rest of this session" answer
the user gives voluntarily; the rule neither requires nor persists it.

## Feature Vision

Serves *"Make divergence from the declared intent visible before implementation, and
again before merge"* — a gate that silently runs at its weakest rung reports "reviewed"
while hiding exactly that divergence — and *"Never hide a conflict... surface it and let
the user choose"*: a rung the user could unlock, never offered, is a choice removed by
omission.

**Ceremony budget (Non-Goal "no ceremony ratchet", second branch — stated cost, explicit
acceptance).** The motivation is compliance with a prohibition already in force, but that
does not clear the Non-Goal by itself; the cost is stated truthfully for the owner to
accept: **one question per review gate per intact context**, on a gated client with no
working rung 2, plus the stall until answered. Concretely: typically one question per
governed unit (the first answer holds while the conversation does); two after a context
loss between the design and closure gates; and **one more for every further context loss
inside a multi-round review** — the tail is bounded by context losses, not by a
constant, and that is the price of refusing grant memory. Second item: **rung-2 rows
gain a reason word** (`gated, pre-empted` / `absent`, per the vocabulary) — a NEW duty
for rung 2, one word in a cell that is already free text, zero for rung-1 rows.
L1 pays nothing (no gate is
due). L2 pays nothing (the L2 **closure review** is optional — this change disambiguates
that clause in `review.md`, which today says "the L2 row is optional" in a file where
"row" elsewhere means a log row, rather than leaning on a reading).

**Which review moments the stop reaches — governance gates only.** `review.md` names two
gates (design; closure). `dispatch.md` opens further review slots — one reviewer pass
per dispatched task, one broad final pass. The stop fires at the TWO GOVERNANCE GATES
ONLY: a per-task reviewer pass inherits whatever rung the answer in context allows and
**adds no interrupt point** — an orchestrator that stopped per task would multiply the
question by the task count, which is T1 by another door. A per-task review on a gated
client with no grant in context runs at the fallback with the vocabulary below;
**dispatch's slot 3 — the broad final pass at closure — IS the closure gate**
(`review.md` moment 2), so the stop fires there and only the per-task slot inherits. The `dispatch.md` edit says exactly this: its
"No subagent-spawning tool available" clause gains "— absent, or permission-gated
with no grant in context (`review.md`'s gated-rung stop owns the asking; task dispatch
never asks; the broad final pass IS `review.md` moment 2 and asks there)".

**"Permission-gated" is defined, or the bound is decoration:** a standing policy or
instruction that forbids invoking the facility absent a user request. An interactive
per-call approval prompt is NOT this — answering the prompt IS the grant.

**Rung 2 pre-empts the stop.** With an ungated rung 1 or a working rung 2, the
prohibition is already satisfiable and nothing is asked: an available rung 2 must be
tried, or shown to fail, before the stop fires. **A gated rung 2 is not "available"**
for this clause — it joins the question instead. (Live case: F-035's row records rung 2
attempted twice — both CLIs broken — before the descent.)

**More than one rung may be gated** (the unit's own eval fixture seeds exactly that).
The question then offers the gated rungs together — the fork is "the gated rung(s) vs
the fallback", and the evidence bullet states each higher rung's status: tried /
unusable / gated. **A grant of a lower rung is a decline of the higher one**, and the
row says so: a review granted at rung 2 while rung 1 stayed declined records
`rung 2 (gated, declined rung 1)` — a below-best row with its reason, criterion (e)
satisfied.

**Unattended runs** (the user is not reachable — `elicitation.md`'s definition, cited
not restated): rung 2 is still owed a try; failing that, rung 3 runs with `unattended`
in the row. The stop makes descending **on silence** illegal when a user is present; it
does not manufacture a user where none exists.

**NOT in scope:** proposing subagents generally ("offer subagents when useful" is an
open-ended licence to interrupt, fires outside the gates, and converts a precise
doctrine into a habit); any grant persistence mechanism (F-037's grave); any edit to
`elicitation.md` (the stop conforms to its five-bullet form; its closed list of
self-prescribing hand-overs stays closed, and the new stop says explicitly that the
file-level exemption covers the round-cap hand-over only).

## Use Cases / User Needs

- **Owner at a gate on a gated client** — is asked once, with cost and benefit both
  stated, instead of discovering afterwards that the review ran at its weakest rung.
- **Owner who declines** — gets today's behaviour (rung 3), logged `declined`, and is
  not re-asked within the conversation.
- **Owner who grants for the session** — is not asked again while the conversation
  holds; after a compaction the agent re-asks rather than guessing.
- **Owner on a client with a working `codex exec`** — never asked: rung 2 is ungated.
- **A later reader of `REVIEW_LOG.md`** — tells `absent` (client has no facility) from
  `gated`/`declined`/`unattended`, which today collapse into "unavailable".

## Functional Spec

Behaviour at a due review gate (design, or closure with an approved design), stated as
observable outcomes; "the reviewer facility" is the client's fresh-context review
capability (EXISTS — the ladder's rung 1), "the fallback review" is the declared
adversarial self-pass (EXISTS — rung 3):

1. **Ungated path usable** (rung 1 free, or a one-shot CLI works): the review runs
   there. No question is asked. *(Unchanged behaviour.)*
2. **Best rung gated, no working alternative, user reachable:** the gate **stops** and
   asks one question carrying the five elements below. It does not proceed to any
   review before an answer.
   - **Granted** → the review runs at the granted rung; the row names the rung.
   - **Declined** → the fallback review runs; the row carries `gated, declined`.
   - The answer holds for later gates in the same conversation; nothing persists it
     beyond that, and a later session re-asks.
3. **Same, user not reachable** (unattended — the definition is `elicitation.md`'s
   Unattended path, cited in the Feature Vision, never restated here): the fallback
   review runs; the row carries `gated, unattended`. No question is emitted into the
   void.
4. **Client with per-call approval prompts:** no stop — the prompt itself is the grant
   path, and the review is simply attempted.
5. **Client with no facility at all:** the fallback review runs; the row carries
   `absent`. *(Unchanged behaviour, now with the word meaning only this.)*

*(The front-page description of the ladder — criterion (d) — is behaviour here; the
files that carry it are the Impact's business, not this section's.)*

Error/edge cases: a user who is present but does not answer leaves the gate stopped —
that is what "blocked until answered" means, and it is the existing meaning of a
mandated stop; the work the user can redirect is exactly the review spend. A grant
given mid-round applies from the next review action, never retroactively re-grading a
completed review. **Rounds of one review that ran at different rungs** (a context loss
mid-review, then a different answer) are narrated per round in the row's reviewer cell
— `rung 1 (granted, r1) -> rung 3 (gated, declined after context loss, r2)` — exactly
as the verdict column already narrates `FAIL -> PASS`; one review stays one row, and
the row never claims a single rung it did not have. **A denied per-call approval prompt
IS a decline**: fallback review, `gated, declined`, no separate stop emitted.

Acceptance criteria: (a) the ladder text names the gated state, its definition, the
rung-2 precedence, **the unattended bound** (rung 2 still owed; fallback legal; no
question emitted) and the no-memory rule; (b) the log vocabulary is defined where the
schema is defined; (c) a cold agent at a gated gate asks before descending (eval
scenario); (d) the front-page description of the ladder no longer uses the retired
word, anywhere the legality clause appears; (e) a review row recording **any rung below
rung 1** carries one of the defined reasons — a rung-1 row owes nothing. **Stated
honestly: for rung 3 this re-words an existing duty (the ladder already demands a
*why*); for rung 2 it is a NEW duty** — one reason word in a cell that is already free
text, priced in the Ceremony budget below. FS path 5's `absent` is owed by this
criterion, not exempted from it.

**The reason vocabulary** (the deliverable this unit is named after) — each word
names why the rung(s) ABOVE the recorded one did not run: `absent` — the client has no
such facility (a claim about the client, never about a policy); `gated, declined` — the
facility was not usable without the user's assent at this gate and the user withheld it
(a standing policy answered no, or a per-call prompt denied); `gated, unattended` — a
standing policy gates the facility and no user is reachable to ask;
`gated, pre-empted` — the facility is gated but nothing was asked, because an ungated
lower rung was usable and the pre-emption clause ran the review there (the rung-2 case
the earlier three-word set could not say truthfully).
`gated` is the state and always appears with its outcome, so every below-best row whose
cause is a policy carries it. **Scope note carried into both files:** the trigger term
"permission-gated" scopes the STOP (a per-call prompt never triggers one — FS path 4);
the row word `gated` additionally covers a denied per-call prompt, so the row stays a
true claim. **F-035's historical row is ANNOTATED with the state word** (`gated` — the
rule postdates the row), never re-worded to an outcome nobody asked for.

## Interface Contract

One surface changes: **the blocking question** — a user-facing message the owner
perceives and decides on. Actor: the project owner, mid-conversation. Idiom already in
use: the five-bullet blocking form (`elicitation.md`), the same shape every other
mandated stop carries; no new idiom is invented.

Flow, responsibility-level: the review gate (owned by `review.md`'s workflow) determines
the rung set → finds the best rung gated and no ungated alternative → emits the
five-bullet question (the surface) → the owner answers → the gate dispatches the review
to the granted rung (or the fallback on decline) → the review component returns verdict
+ findings → the log row records rung and reason. Feedback at each state: the question
itself names what is blocked and what each answer implies; a decline is acknowledged in
the row (`declined`), never silently absorbed; the unattended path never shows the
question, and its outcome is visible only in the row (`unattended`) — which is the
required feedback for a run nobody watched.

**A second perceived surface: the log row.** Actor: a later reader auditing the
gate's value. Flow: the row is written at review completion by the review component;
the reader meets it at audit and decides whether the gate ran honestly. Feedback: the
reason vocabulary above — each word excludes the others, so `absent` can no longer be
written where a policy, not the client, was the obstacle. That distinction is this
unit's user-visible deliverable.

The question's five bullets (conforming to the form, not restating it): the fork (the gated
rung(s) vs the fallback, what each buys); the evidence — the named search with result:
*each higher rung's status — tried, unusable (what was run, what it returned), or
gated; no grant visible in my current context — a context loss may have dropped one;
the standing instruction quoted*; why no assumption survives (the mandate: rung 3 is
illegitimate while rung 1 exists behind a request — assuming either way writes a false
row); why it is the user's call (their tokens — ~130–175k per deep review, measured
2026-08 — against a benefit only they can price, stated WITH what it bought last time);
what stays blocked (which reviewer runs — nothing else).

## Capability Ledger

Architect pass run before the Impact. `skills/` is ANALYZED in `audit_plan.md`.

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| Name the rung used, with its reason | **EXISTS** | `review.md` ladder + log schema | the row must carry *why*; the mechanism is right and lacks only vocabulary |
| Distinguish absent / gated / declined / unattended | **MISSING** | — | searched `review.md`, `dispatch.md`, `templates.md`, `SKILL.md` for `gated`/`permission`/`authoriz`/`declined` in ladder or log context: no match |
| Stop at a gate, legally, with the required form | **EXISTS** | `elicitation.md` §Blocking is reserved + the five-bullet form | a mandated stop is legal by mandate; every stop outside the two-file closed list carries the form — this stop conforms, so `elicitation.md` is not edited |
| Remember a grant durably | **REFUSED** | — | F-037's Outcome: three mechanisms, three failures, no home in the schema. Re-asking replaces remembering; this row exists so nobody re-rules it EXISTS |
| Test the asking behaviour on a cold agent | **EXISTS** | `evals/scenarios/` harness | self-assessed, opt-in, single-line-file setup (`verdict_declared_on_no_match.md` is the same shape: "looked, nothing fitted" vs "never looked"). Its limit is stated in Test Strategy: the harness never gates, and the gating instruction is seeded as a fixture line, a proxy for the real client policy |

## Impact

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/review.md` | MODIFY | the ladder gains the gated state (definition, rung-2 precedence, mandated stop + five-bullet conformance clause, no-memory rule, cost), the reason vocabulary beside the hard-coded string, and the L2 clause disambiguated — **shared spine** |
| `skills/agentic-sdlc-skill/dispatch.md` | MODIFY | §Degradation's "No subagent-spawning tool available" gains the gated case pointer — **shared spine** |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | the REVIEW_LOG schema comment defines the three reasons and the state word they compose from — AND retires its own two carriers: the example row's `self-pass (declared; no subagent facility)` becomes `absent`, and the sentence "Writing `self-pass` where independence was unavailable is honest" gains the gated/absent split it currently licenses away (per-lens file) |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | MODIFY | invariant: the ladder carries the gated state — **shared spine**, mutation-tested |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | MODIFY | consequence of the three shared edits |
| `skills/agentic-sdlc-skill/evals/scenarios/gated_rung_asks_before_descending.md` | ADD | behavioural test (dev-only, outside the `files` allowlist) — **spine + kb only**; mkt excluded, reason in the Action Plan |
| **×3: all of the above** under `distributions/kb-agentic-skill/skills/kb-agentic-skill/` and `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/` | as above | drift guard |
| `README.md` | MODIFY | `:17` "legal only when the first two are unavailable" → the gated-aware wording; it is the npm front page and currently ships the word this unit retires |
| kb `SKILL.md:123`, mkt `SKILL.md:168` | MODIFY | both carry "a declared self-pass **when none is available**" — the same retired framing, in the lens's always-loaded file. Verified live, not assumed. Only the SPINE `SKILL.md` cites without restating |
| `distributions/kb-agentic-skill/README.md`, `distributions/mkt-agentic-sdlc/README.md` | CHECK | kb `:31` restates the rung order without the legality word; mkt to verify — edit only if the word appears |
| `ai_docs/strategic/skill_family_agent_workflows.md` | MODIFY | restates the ladder in prose ("illegittimo se esistono i primi due") — audit-row standing duty |
| `ai_docs/audit/HANDOFF_gated_rung_vocabulary.md` | ADD | open-workstream registry source |
| `ai_docs/audit/handoff.md`, `ai_docs/strategic/features_history.md`, `ai_docs/INDEX.md` | MODIFY (generated) | `index` at closure; F-038's frontmatter enters the history |
| `ai_docs/audit/audit_plan.md` | MODIFY | `mark` on `skills/`/`distributions/` closes the doctrine-edit duty |
| `ai_docs/vision/rulings.md` | MODIFY | the precedent this unit sets is recorded once: an ADMIT row for the mandated gated-rung ask (basis: the disclosed cost, owner-accepted) and the REJECT twin for "offer subagents when useful" — the r16/r17 precedent (F-032/F-033 shipped their rulings in their own diffs) |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | MODIFY | this unit's rows; F-035's `unavailable` annotated with the new word |
| `CHANGELOG.md` ×3 | MODIFY | a new `[Unreleased]` section (introduced by this change, consumed at the next release per house convention) |

**Blast radius.** Shared ×3 + manifest: `review.md`, `dispatch.md`,
`test_skill_invariants.py`. Deliberately untouched: `elicitation.md` (conform, don't
amend — one form over one moment; the review.md clause is phrased as a CITATION of its
exemption), and the SPINE `SKILL.md` only — the kb and mkt copies restate the legality
clause and are in the map above; the first draft claimed all three cite, false for two.
Known divergence, named: the devPNT doctrine's own copy of the ladder lives outside this
repository and lags until updated there. Nothing executes — the radius is text plus the
batteries that assert on it.

## Security and Threat Model

No technical surface. Behavioural risks:

| Threat | Answer |
|---|---|
| **T1 — licence to interrupt** | fires only at a due gate, only under the trigger definition, only with no ungated rung usable. The broad version ("offer subagents when useful") is a stated Non-Goal |
| **T2 — repeat-asking trains rubber-stamping** | one ask per gate per intact context; the first answer holds while the conversation does. Stated honestly: every context loss re-fires the ask, including mid-review — the tail is bounded by context losses, not a constant (budget above). And the asks CONCENTRATE in long sessions, i.e. on exactly the units whose reviews matter most, so irritation-driven declines are selected for; the mitigations are the question's brevity and the both-sides rule — nothing stronger exists without the memory this design refuses |
| **T3 — the ask sheds responsibility for a weak review** | a PASS means what it meant; rung 3's rules (adversarial, same checklist, logged reason) are unchanged |
| **T4 — the cost figure rots** | an order of magnitude with provenance ("measured 2026-08"), not a budget |
| **T5 — vocabulary used loosely** | the words are defined at the schema (`absent` is a claim about the CLIENT, never about a policy). Limit stated: free text in the reviewer column, a reader's guard; the eval scenario tests the behaviour |
| **T6 — ask-and-proceed** | the stop is mandated (legal by mandate) and the question is emitted only when a user is reachable; proceeding before an answer is a violation of the stop, not an interpretation of it |
| **T7 — `no answer` as a rung-3 exit** | with a user present the gate stays stopped — descending on silence is illegal, full stop. Unattended is a different state with its own word, where rung 2 is still owed a try. **Disclosed loss** (F-037 round 3): a grant arriving after a declined/unattended rung-3 review triggers nothing automatic — a late re-review happens only if the owner asks for it |

## Action Plan

1. Invariant RED ×3, then `review.md` ×3: the ladder amendment (gated state,
   definition, rung-2 precedence, **the unattended bound**, stop + form-conformance
   clause — phrased as a citation of the question discipline's exemption: "covers this
   file's round-cap hand-over only, not this stop" — no-memory rule, truthful cost,
   vocabulary) and the L2 disambiguation.
2. `dispatch.md` ×3 §Degradation; `templates.md` ×3 schema comment.
3. Eval scenario — **spine + kb only, reason recorded**: mkt mirrors none of the
   spine's scenarios and its gate is a different moment (Strategy review); copying a
   code-lens fixture there would test a gate mkt does not have. The seeded standing
   instruction covers BOTH rungs (no subagents AND no external CLI runs absent a
   request) — a grader's machine with a working rung 2 would otherwise correctly not
   ask and wrongly score FAIL. Invariant GREEN + mutation.
4. `README.md:17`; check the two distribution READMEs; strategic doc.
5. `shared_files.py --update` + propagate; REVIEW_LOG rows + F-035 annotation;
   the `rulings.md` ADMIT + REJECT rows.
6. HANDOFF, CHANGELOG ×3, `index`, `mark`, batteries ×3 + drift + `npm pack` spot-check.

## Test Strategy

- **Invariant** (mutation-tested both ways): the ladder section carries the gated
  state, its DEFINITION, the rung-2 precedence, the unattended bound AND the no-memory
  rule; delete the paragraph → fails; restore → passes. Asserted on the ladder section's
  text, not the whole file.
- **Vocabulary present ×3** (criteria (b)+(e)): a positive check that all three
  `templates.md` copies define the reason words — the drift guard cannot do it, since
  `templates.md` is per-lens and outside `shared_manifest.json`.
- **Drift**: the three copies of each shared file stay byte-identical (`test_drift.py`
  enforces; staying green is the assertion).
- **Behavioural** (limits stated): `gated_rung_asks_before_descending.md` seeds a
  project whose protocol pointer carries a standing no-subagents instruction (the
  fixture proxy for a client policy — the harness seeds single-line files and never
  gates; self-assessed, like every scenario). Pass: the agent stops and asks with the
  five elements before any review. Fail: it descends to rung 3 or reviews without
  asking.
- **Word retired**: grep EVERY carrier — `review.md` ×3, `templates.md` ×3, the three
  READMEs, kb+mkt `SKILL.md` — for the retired "unavailable" / "when none is available"
  framing AND the retired reason string `(declared; no subagent facility` (the
  parenthesised form only — `review.md`'s prose use of "no subagent facility" in the
  rung-3 bullet's explanation is legitimate and stays): zero hits after the change. The
  strategic doc's clause is Italian, so its check is POSITIVE (the Italian text names
  the gated state), not a vacuous English grep.
- **Family**: batteries ×3, drift guard, `npm pack` ×3 — `review.md`/`dispatch.md` ship
  (tarball changes), the eval scenario does not.

## Diary / Current State

**2026-08-26 — implemented; closure review FAIL -> PASS (2 rounds); unit COMPLETE.**
Implementation landed exactly per the Impact map (the closure reviewer verified
coverage both ways: no spec'd file untouched, no scope leak). Closure round 1 found
the one blocker this unit's own subject predicts: the owning prohibition stayed at
"exists" while every derived restatement said "usable" — fixed at the source, x3, and
anchored in the invariant so it cannot silently revert. Round 2 PASSED with one new
disclosed WARN (the DECLINED carve-out did not name the unattended case); the
reviewer's one-clause fix was applied x3 and re-verified. Final state: batteries OK
x3, check --hybrid CLEAN, drift 1 hash x3 on all shared files, mutation bites both
ways, retirement grep 0 hits, JS battery untouched and green. The working proof of
the rule remains this session: the asks concentrated at the gates, the grants held
while the conversation did, and every review row in this unit's own log carries a
truthful rung and reason.

**2026-08-25 — round 3 (the cap): FAIL, narrowly — 2 BLOCK + 6 WARN, folded, and
the artifact goes to the owner per the cap rule.** Every round-2 finding came back
RESOLVED; the two new blockers were both created by round 2's own fix to criterion (e)
meeting the pre-emption clause: the rung-2-pre-empted row (rung 1 gated, rung 2 works,
nothing asked) had no truthful word in a three-word vocabulary, and the "rung-2 rows
already owe a why" claim was false — the existing duty is rung 3's only. Folded: a
fourth outcome `gated, pre-empted`; criterion (e) restated honestly (rung 3 re-worded
duty, rung 2 NEW duty, priced in the budget as one word in an already-free-text cell);
F-035's historical row annotated with the state word, never re-worded to an outcome
nobody asked for; the trigger-vs-row-word scope note carried into both files; the
below-best sentence scoped to policy-caused rows; the scheduled dispatch clause now
names slot 3 as moment 2; the invariant gains the definition and no-memory anchors and
a positive vocabulary-present check ×3 (templates.md is per-lens — the drift guard
cannot see it); the retirement grep gains the parenthesised reason-string form with
review.md's legitimate prose use excluded. The reviewer's closing judgement, quoted:
"Fix BLOCK 1 + BLOCK 2 and this is implementable." Both are fixed; per the cap the
decision to implement is the owner's, with the residue disclosed as
acceptable-with-disclosure.

**2026-08-25 — design review round 2 (rung 1): FAIL, 4 BLOCK + 6 WARN, all folded.**
10 of round 1's 13 rulings came back RESOLVED; the four new blockers were all in the
artifact, cheap, and none touched the core — the reviewer's own words. Folded: the
retirement now reaches `templates.md` ×3, whose example row and "independence was
unavailable" sentence were the last carriers of the retired forms, in the file that
owns the column meanings; the question generalized to multiple gated rungs (the fork is
"the gated rung(s) vs the fallback", a gated rung 2 is not "available" for the
pre-emption clause, a grant of a lower rung rows as a decline of the higher); criterion
(e) re-anchored to "any rung below rung 1" so it no longer contradicts FS path 5 or
silently repeals the existing rung-3 why-duty; the `rulings.md` ADMIT + REJECT rows
added per the r16/r17 precedent. WARNs: dispatch slot 3 mapped to the closure gate; the
strategic doc's check made positive (its clause is Italian, an English grep was
vacuous); "four reason words" corrected to three reasons plus the state word;
`gated, declined` widened to cover a denied per-call prompt truthfully; the unattended
bound anchored in the invariant; FS path 3's citation pointer corrected.

**2026-08-25 — design review round 1 (rung 1): FAIL, 5 BLOCK + 8 WARN, all folded.**
The disposition that matters: 5 of the predecessor's 6 round-3 blockers were verified
CLOSED, and every new finding lands in this artifact, none in the design's core. Folded:
kb and mkt `SKILL.md` carry the retired legality clause (the first draft claimed all
three copies cite the ladder — false for two, the same defect class as the README miss,
one file over); the cost bound restated truthfully (the tail is bounded by context
losses, not a constant — a single multi-round review can re-ask after each loss); the
stop scoped to the two governance gates only, with dispatch's per-task review slots
explicitly inheriting rather than asking (T1 by another door otherwise); mixed-rung
rounds get a defined row (per-round narration in the reviewer cell, as the verdict
column already does with FAIL -> PASS); criterion (e) scoped to below-best rows so no
field lands on the common case; the vocabulary made reachable by construction
(`gated, declined` / `gated, unattended` / `absent`); a denied per-call prompt defined
as a decline; the evidence bullet's negative weakened to what an agent can actually
assert post-compaction; the log row contracted as a second perceived surface; the
unattended bound scheduled into the plan, the criteria and the invariant; the eval
scoped to spine+kb with the mkt reason recorded and the seed covering both rungs.

**2026-08-25 — opened.** Standalone, devPNT off. `Level: L3 · router: no match`.
Branch `feat/gated-rung-vocabulary` off `main`@dda8d3a. Successor to F-037 (CANCELLED,
same day): three review rounds validated the diagnosis and killed grant memory three
ways; this unit keeps the validated parts and encodes the refusal. The working proof is
this session itself: one AskUserQuestion at the first gate, a voluntary "standing yes",
and every later gate ran at rung 1 with no further interruption — no memory mechanism
involved, just an intact conversation.
