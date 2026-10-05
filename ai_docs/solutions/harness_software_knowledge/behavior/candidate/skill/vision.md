# Writing a Vision that a cold reviewer can actually apply

Support file for `ai_docs/vision/project_vision.md`, `vision/features/VISION_*.md`
and (Hybrid) the devPNT M-VISION. Read it when writing or amending any of them.
The template lives in `templates.md`; this file is the *why it works*.

**The problem this solves.** A Vision's job is to be read cold — by a later
session, by a reviewer, by another agent — and to produce a ruling on a proposed
change. Most Visions cannot do that: they read as intent to whoever wrote them and
as ambiguity to everyone else, and the gap is invisible until something wrong gets
through. Writing one and then discovering the holes by adversarial rounds works,
but it costs several rewrites. The checklist below exists so a Vision is
verifiable on the **first** draft.

Everything here was derived empirically: six blind adversarial rounds against one
real Vision, reviewers with no repository access, ~25 attack proposals. Rules that
survived every attack and rules that fell were compared for structure. What
follows is that difference.

## What a Vision IS

A Vision states **what is to be obtained — the benefit — while leaving the most
degrees of freedom possible. It binds nothing that does not obstruct that
benefit.**

Four consequences, each operational:

- **State the benefit, not the mechanism.** What the actor *obtains*, never how —
  and concrete enough that an obstacle to it is *recognizable*. This is the test a
  North Star must pass: from "best-in-class" no constraint is derivable and none
  is refutable, because nothing recognizably obstructs it. From "everything the
  methodology produces stays usable in full without paying", a metering ban
  follows and can be checked.
- **The deletion test — the generative rule for every constraint.** Remove the
  rule: is the benefit still reachable? If **yes**, delete the rule — it was
  spending a degree of freedom on nothing. If **no**, keep it, and its sentence
  must name the obstacle it removes. This is also the stop rule: when nothing on
  the table would obstruct the benefit, the Vision needs no new rule.
- **Constraints accumulate as the work reveals obstacles.** The first draft is the
  benefit plus the few constraints already known — usually almost none, and that
  is correct (`DRAFT` informs, `APPROVED` binds). Each constraint added later
  *sharpens* the Vision without shrinking it more than the obstacle requires.
- **A constraint never obstructs the Vision.** A proposed rule that conflicts with
  the benefit is not a constraint to negotiate in place — it is a Vision
  **amendment**, and amending is the owner's decision, never a side effect of a
  downstream edit.

Extracting the benefit from a discussion is real work: a discourse arrives with
solutions, preferences and constraints tangled together, and the Vision is the
distilled benefit only. The elicitation round (`elicitation.md`) asks for it first
— and a mechanism ("a dashboard") is not an acceptable answer to a benefit
question ("never lose the thread"); ask again until the answer names what the
actor obtains.

The deletion test decides **which** rules exist. Everything below decides **how**
to write a rule so it holds once you know it must exist.

## 0. The one-line test

> Could a reader who has never seen this project rule ACCEPT or REJECT on a
> proposed change, quoting one line of this document, without asking anyone
> anything?

If a section cannot contribute to that, it is background — keep it if it helps a
human, but know it carries no gate weight.

## 1. The nine properties of a rule that holds

Each is stated as a drafting action, with the attack it defeats.

1. **Key the rule to a property observable in the artifact — never to intent,
   commitment, plan or purpose.** Test while drafting: *could I verify compliance
   by reading the diff, without asking the author what they meant?*
   → Defeats: the proposer simply promises the opposite. A rule that forbids
   "committing to track someone's format" is satisfied by saying "we commit to
   nothing"; a rule that forbids "code in this repo that parses a format we do
   not define" is not.
2. **Write it as one yes/no question with BOTH branches answered.**
   → Defeats: a gate that can only reject. A prohibition-only Vision rejects the
   work it wants (new client support, packaging, bug fixes) and is abandoned.
3. **Phrase the question counterfactually about capability, not about the status
   quo** — "could the user obtain this…", not "does the product currently do it".
   → Defeats: "we never shipped it, so nothing is being taken away."
4. **Enumerate the near-miss verbs, not just the headline one** — charge / count /
   cap / condition / gate / degrade / delay / require-signup.
   → Defeats: the soft form. A generous cap, a free-but-registered tier, a
   zero-cost counter — all are the same harm and none is the headline verb.
5. **Define every term the rule turns on by EFFECT, and close the list.** A
   definition that enumerates mechanisms is a list of the ways you already thought
   of; end it with "…and anything else the user must give, accept or obtain from
   us."
   → Defeats: the third mechanism. "Charge = payment or account" is walked past by
   "requires opting into telemetry".
6. **Enumerate the FORMS a violation can take, then state a closure rule** —
   "anything not named here is out unless it is X".
   → Defeats: the unnamed variant. "A step, a required field, a check, or a cost
   that varies but is never zero" kills "auto-filled, zero human input", because
   the form is still a required field.
7. **State the subject predicate of any enumerated test in checkable terms.** If
   the test applies to "a record of work", say what makes something one.
   → Defeats: denying the subject. The proposer agrees with every item on your
   list and asserts the list does not apply.
8. **Give one IN and one OUT example on the same axis, differing in a single
   variable.** The pair carries the discriminator; without it the reader invents
   one.
   → Defeats: the borderline case, which is where every real argument happens.
9. **Name the re-descriptions you expect, inside the rule's own sentence** —
   "in any presentation", "however the code got here", "not by a component that
   does not exist yet", "storing it as Markdown changes nothing".
   → Defeats: relabeling. A board called a "view" is still a board.

## 2. The five clauses a Vision needs around its rules

Rules do not hold alone. These structural clauses were the difference between a
rule that survived and the same rule leaking.

- **Supremacy clause** — on any rule a second layer, product, tier or future
  component could route around: *"these bind the product as a whole; shipping a
  forbidden thing in the paid layer does not put it out of reach."*
- **Exceptions attached to the rule they limit, in the same bullet, phrased
  affirmatively.** An exception in another section is a leak; an exception phrased
  only as a negation produces CANNOT DECIDE. *"This rule does not reach X;
  supporting one more X is squarely wanted."*
- **Anti-abuse clause on every exemption, naming the only permitted outcomes.**
  A maintenance exemption without one lets any forbidden thing that already
  shipped be maintained forever, and any new one be framed as a fix to it:
  *"work framed as a fix to something that should never have shipped is not
  exempt — it is the removal of that thing, or it is out."*
- **Stated defaults, per path including the exempt path** — "anything unreached is
  out"; "an exempt fix that preserves a forbidden thing is out". A test that says
  "admitted only if" gives new capability a default; exempt work has none unless
  you write one.
- **Precedence, when two sentences can both apply.** Two adjacent statements
  pointing opposite ways are decided by whichever the reader reaches first.

## 3. Only prohibitions can reject; only positives can admit

This is the most common structural failure and it is invisible from the inside.

- **A Goal cannot reject anything.** If the admission test says "advances a Goal
  and violates no Non-Goal", then rejection power lives *only* in the Non-Goals.
  A Goal that says "scale cost to risk in both directions" cannot stop cost
  inflation — you need a prohibition for that.
- **A prohibition scoped to one rung of your own scale protects only that rung.**
  Banning ceremony on trivial edits invites the same ceremony one level up.
- **A criterion phrased as an already-true state cannot be advanced.** "The check
  is CLEAN at every closure" is a state, so "advances this signal" is meaningless
  and any proposal citing it is undecidable. Give every positive criterion a
  **baseline with headroom**: a current value and date, or an explicit list of
  improvement categories that count.
- **Give recurring legitimate work an explicit authorization clause**, or it will
  be rejected by your own test: packaging and installation, the product's own
  tests, reducing what the agent must read, supporting one more client. Each needs
  a home in the positive sources — otherwise "moves nothing this document commits
  to" fires on exactly the maintenance the product needs.

## 4. Minimum operable sections

A Vision is a gate. These are the load-bearing parts; anything else is
orientation for humans and should be recognized as such.

| Section | Must contain | Enables |
|---|---|---|
| Authority & scope | what it binds (all layers, tiers, future components), that packaging is irrelevant, precedence among its own sections, the approval line | both |
| Defaults | the default ruling for anything unreached, stated per path | both |
| Admission test | one sentence naming *exactly which* sections are positive sources and *exactly which* are prohibitions | ACCEPT |
| Positive sources | Goals / Actor commitments / Success Signals — each with a baseline and headroom, checkable against a named artifact | ACCEPT |
| Prohibitions | property-based, closed enumerations, named re-descriptions, in/out pairs | REJECT |
| Invariants | the decision question with both branches answered, plus an anti-laundering clause | both |
| Exemptions | each with its anti-abuse clause | prevents laundering |
| Definitions & imported facts | terms defined by effect; **any fact from another document a ruling depends on, restated here** with the reason | standalone use |
| Pointers | what deliberately lives elsewhere, so an absence reads as intentional | prevents false CANNOT DECIDE |

**Imported facts matter more than they look.** If a ruling needs your triage
levels, your risk tiers or your lifecycle states, restate the boundaries in the
Vision — routing the reader to another file breaks the cold-read premise the
whole gate rests on. Keep the procedure elsewhere; bring the boundaries here.

**Keep competitive positioning OUT.** A Vision defined by comparison to another
product rots silently: the comparison target moves and no one edits your document.
Put it in a dated snapshot elsewhere and point to it.

## 5. What no wording can fix — use a mechanism instead

Five failure classes are structural. Prose cannot close them; do not try.

| Failure | Mechanism |
|---|---|
| "Advances a Goal" is a claim about the world, not the text | Measure it: run the ruling battery before and after, admit on measured improvement |
| **Cumulative ratchet** — each addition defensible, the sum is the ceremony the Vision forbids | A measured budget: steps per level, tokens the agent loads, artifacts per change; add-one-remove-one |
| Facts the proposal never states ("a quota of *what*?") | A proposal template that demands them, and a stated rule that omission resolves against the proposal |
| Structural compliance without truth — every rule satisfied, the artifact still wrong | Independent review; a Vision cannot detect this |
| An accepted change silently falsifying the Vision | Require the amendment in the same change; check cross-document facts mechanically |

And the sixth, which is why this file exists:

**Adversarial re-description is unbounded.** Every patch names the evasions seen so
far; a new one always exists. Patch-after-defeat is a treadmill. The only thing
that converts it into a ratchet is a **standing battery**: keep every attack
proposal that ever worked as a fixture and re-run the whole set against every
Vision edit. A Vision without a battery decays the moment someone motivated reads
it.

## 6. The blind check (procedure)

Run this **before promoting any Vision to APPROVED, and before any amendment of an
approved one**. Not for DRAFT edits — promotion is when authority is granted, and
it is rare, so the cost lands where it buys most.

1. **Give the reviewer the document text and nothing else.** Not a path — the
   text, pasted. Forbid opening files, searching, and web access explicitly. A
   term the reviewer cannot resolve is then a property of the document, not of
   their tooling.
2. **Fresh context, and a different model from the author where the client allows
   it.** Author self-review is structurally blind to its own omissions.
3. **Hand them a battery, not an open question.** Concrete proposals to rule on:
   - the standing fixtures (every attack that ever worked — see §5);
   - **reject-side** proposals aimed at each prohibition;
   - **accept-side** proposals the document plainly wants (a bug fix, packaging
     work, supporting one more client, a documentation improvement). *A gate that
     can only reject is half a gate, and the accept side is where most Visions
     fail without anyone noticing.*
4. **Ask for the mechanism, not just the verdict.** For each ruling: the exact
   quoted line, or precisely what the document fails to say. Then: *which rules
   could you not get around, and what structural property defeated you?* That
   answer is worth more than the findings.
5. **Ask for rewords.** "Slip a bad proposal past this document, including one
   dressed in its own approving vocabulary." A rule nobody can reword is done; a
   rule that falls to the first attempt was never a rule.
6. **Every finding is answered — fixed, or refused with reasoning** (`review.md`
   §Receiving). Add every successful reword to the standing battery, whether or
   not you fix it this round.

Three lenses are worth running for a product-level Vision: **comprehension** (what
is this, what could you not resolve), **gate operability** (the battery above),
**durability** (what rots, what is unfalsifiable, what is a time bomb). For a
feature-level Vision or an M-VISION, the gate lens alone is usually enough.

## 7. Cost, honestly

A first draft written against §1–§4 will still have findings — the checklist
removes the structural classes, not judgement errors. Expect one blind round to
find real things and a second to confirm. What it should NOT take is five rounds
of discovering the same class of defect in a new disguise; that is the specific
waste this file exists to prevent.
