---
description: SPIKE - does F-047's citation-scope rule actually reduce out-of-scope citations? Pre-registered A/B replay of the one field-sourced bundled row, old doctrine vs new, blind runs and a blind judge. Protocol and failure criterion written BEFORE any run.
status: CURRENT
---
# SPIKE: Does the citation-scope rule change behaviour?

**Level: Spike · router: no match.** Time-boxed; not mergeable into doctrine. The
outcome is a number and a verdict, not a change.

## The question

F-047 shipped three things: an extraction rule (one row asserts one thing), a repair
move (split as supersession), and a **use-side rail** (before citing a row, verify
every part of it belongs to the question; cite the part and say where the rest
belongs). Only the third is testable today, because only it acts at answer time on a
corpus that already exists. The question is narrow and stated as such:

> Given a bundled claim row and a task that legitimately cites only part of it, does
> an agent under the NEW doctrine produce fewer out-of-scope assertions than one under
> the OLD doctrine?

## Why this stimulus and no other

The field report gave one row **verbatim**, with the practitioner's own ground truth
for what going wrong looks like. That is the whole reason this is a measurement rather
than a demonstration: the stimulus was not written by the author of the fix, and the
wrong answer was recorded by a human before any doctrine existed to prevent it. The
other 24 rows the report audited are not in our hands, so **nothing here generalizes
to them** — this measures one row, many runs.

The row (field text, unchanged):

> The reviewer states the app already allows biometric login on both Android and
> iOS, that account creation requires email verification, and that the calling station
> already offers two-factor authentication in three combinations — face and code, face
> and key, key and code.

Recorded field failure: cited under an app-login requirement, the row imports the third
fact and the reader concludes **the app's identity is already two-factor**. It is not —
the 2FA is at the door, a different subject.

## Pre-registered protocol

Written before any run; nothing below is adjusted after seeing results.

- **Conditions.** OLD = the kb doctrine at `fc422d6^` (immediately before F-047). NEW =
  the doctrine at `HEAD`. The only difference handed to the agent is the doctrine text.
- **Blinding.** Each run is a fresh context. The prompt never mentions bundling,
  atomicity, citation scope, F-047, or that an experiment is running. The agent is
  asked to do ordinary work: write the app-login section of a requirements document
  from the knowledge base, citing claim ids.
- **Fixture.** A minimal corpus in a scratch directory: the reviewer note as a stored
  artifact, a topic file whose `## Claims` table carries the bundled row plus three
  atomic distractor rows. Legal ids, resolving locators. The agent is told to work only
  from that directory.
- **N.** 3 runs per condition (6 total). Small, and declared small: this can show a
  large effect or nothing, and cannot resolve a small one.
- **Judge.** A separate fresh agent, blind to condition and to the hypothesis, given
  only the six outputs in shuffled order and one question per output.

## The failure criterion, fixed in advance

An output **fails** when it asserts or implies that the APP provides two-factor /
multi-factor authentication, or attributes the three combinations (face+code,
face+key, key+code) to the app, while citing the bundled row. An output **passes**
when it either omits the 2FA fact from the app section, or attributes it explicitly to
the calling station / door as a different subject.

Two secondary, pre-registered observations (not the verdict): whether the output cites
the whole row or names the part it used; and whether it states where the unused part
belongs — the behaviour the rule actually prescribes, as distinct from merely avoiding
the error.

## What a result can and cannot mean

- **NEW 3/3 pass, OLD 3/3 fail** — the rule changes behaviour on this stimulus. It
  still says nothing about the other 24 rows, nor about the extraction rule or the
  split move, and nothing about durability across models.
- **No difference** — the rule does not change behaviour on this stimulus at this N.
  That is a real negative and gets recorded as one; a doctrine that changes nothing
  measurable is a cost with an unproven benefit, and F-047's own north star says an
  unfalsifiable claim is the defect.
- **Mixed** — recorded as mixed, with the raw outputs kept. No post-hoc criterion.

## Setup decisions, recorded before any result was seen

- **Condition B is `fc422d6`, not `HEAD`.** HEAD carries F-048 as well, and comparing
  against it would attribute any difference to two units instead of one. Verified by
  diff: the only change between A and B in `SKILL.md` is the ten-line citation-scope
  block; `distillation.md` differs by the atomicity rule and the de-trapped collision
  remedy. That is the whole treatment.
- **Same model in both conditions** (mid-tier), declared rather than defaulted: a
  model difference across arms would confound the only variable being tested.
- **The fixture is a legal ledger**, not a mock — real content-addressed artifact,
  recomputed claim ids, resolving locators, `kb_check_claims` clean. The bundled row's
  id here is `235c48810344`; three atomic rows (sessions, recovery, provisioning) sit
  beside it as distractors so the task is not trivially about one row.
- **The task never mentions the mechanism.** The agent is asked to write an app
  identity section citing claim ids, nothing more. Neither arm is told that scope,
  bundling or citation width is at issue.

## Limitation found mid-run, criterion NOT adjusted

Observed while the first output arrived, recorded here before the rest were seen and
**without touching the criterion** — moving the goalposts after seeing an output is
the whole failure pre-registration exists to prevent.

The criterion passes an output that "attributes the 2FA fact explicitly to the calling
station". An output can do that and still give the fact **its own subheading inside the
app's identity section**, which reproduces the field failure in substance — a reader
skimming the app requirements sees a two-factor heading — while satisfying the letter
of the test. So the criterion measures *attribution*, not *placement*, and is more
lenient than the field failure it was derived from. Consequence to state plainly: a
PASS under this criterion is weaker evidence than it looks, and a difference between
arms is therefore more meaningful than an absence of one. The secondary observations
(does the output cite the whole row or name the part; does it say where the rest
belongs) partly cover placement, and are reported alongside.

## Results

Six runs, blind judge, criterion unchanged from the pre-registration.

| | OLD (control) | NEW (treatment) |
|---|---|---|
| **Q1 — the pre-registered criterion** (does it attribute app-level 2FA?) | 3/3 PASS | 3/3 PASS |
| Q2 — misleading *placement* despite correct attribution | 1/3 | 0/3 |
| Q3 — cites the part AND says where the rest belongs | 2/3 | 3/3 |

**Verdict: NULL on the primary criterion.** The citation-scope rule bought no
measurable reduction in out-of-scope assertions on this stimulus. Every run in both
arms named the calling station as the subject of the 2FA fact and kept it out of the
app's requirements. The secondary differences (1/3 vs 0/3 on placement, 2/3 vs 3/3 on
citation width) are one output each at N=3 — noise, and reported as noise, not as a
weak positive.

### Why the result came out null: a ceiling effect, and it is the experiment's fault

The control was already at 100%. A test cannot detect a benefit above a baseline that
does not fail, so this design could only ever have produced "no difference" or a
defect in the control — and it produced the former.

The cause is in the stimulus, and it was visible in the field report all along: **the
bundled row names its own off-topic subject in plain words** ("the *calling station*
already offers two-factor authentication"). Avoiding the error therefore requires only
reading the row attentively, not applying any rule. The four defect kinds the report
lists are not equally hard, and this row is the easiest of them — the *borrowed
capability* case with an explicit subject. The genuinely hard kinds are **subject
ambiguity** (the off-topic subject is a pronoun or an unqualified product name) and
**wrong actor** (the surface name is ambiguous between two actors), and neither is
represented here.

So this measures that a current mid-tier model, reading carefully, does not make the
field's mistake on the field's own row. It does not measure whether the rule helps
where the subject is not lexically present, which is where the report says the
remaining three defects lived.

### What this changes

- **F-047's use-side rail stays unproven, and is now recorded as such** rather than
  assumed. It cost one bullet in `SKILL.md`, so the cost/benefit is not alarming; the
  honest statement is "no measured benefit on the one case we could test".
- **A second run is worth it only with a harder stimulus** — a bundled row whose
  off-topic part carries no explicit subject. That row would have to be authored,
  which forfeits the "not written by the author of the fix" property that made this
  experiment worth running at all. The clean alternative is to obtain the reporting
  project's other 24 rows, where the subject-ambiguity cases actually live.
- **The method transfers**: pre-registration, a blind judge, a control taken from the
  commit before the fix, and one variable isolated by diff. Reusable for the F-048
  floor once the log has rows, and cheap — six runs plus a judge.

### Recorded honestly

The pre-registered criterion turned out to be lenient (see the limitation above) AND
the control was at ceiling. Both were knowable before running, from the field report's
own text, and neither was noticed until the outputs came back. That is the finding
about the instrument; the finding about the doctrine is simply: not demonstrated.
