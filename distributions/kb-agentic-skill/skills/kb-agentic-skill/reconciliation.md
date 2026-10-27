# Reconciliation — what happens when two claims meet

**For whom**: the agent that placed a new claim on a node already holding claims about
the same subject.
**Answers**: "is this new, corroborating, refining, coexisting or conflicting — and who
resolves a conflict".
**Does not answer**: how claims are extracted (`distillation.md`) or placed
(`taxonomy.md`).

**The principle, owner-set: the machine detects and holds; it never decides.** A
conflict is resolved only by **new information** — a newer source, or a fact the
practitioner knows that the corpus lacks. Silence is impossible by construction:
both sides stay, marked, until information ends the disagreement.

## 1. Five outcomes — the agent classifies, the machine verifies

Subject-sameness is semantic judgement; no query performs it. Classify:

| Outcome | When | Action |
|---|---|---|
| **new** | nothing on that subject | insert the row |
| **corroboration** | same assertion, different source | append the source to the existing row (`;`-separated). **Never a second row.** The id keeps its first source |
| **refinement** | strictly more precise, not contradictory ("Q1" → "15 March") | new row; the old one becomes `SUPERSEDED <new-id>`, its text intact |
| **coexistence** | contradictory only if scopes overlapped — and by the half-open rule they do not | both rows stay `OK`. "12k until March" and "15k from March" are two truths, not a conflict |
| **conflict** | contradictory, scopes overlap | **every** row in the set becomes `CONTESTED` listing all counterparts. Nothing is picked |

**A declaration is not a source.** A `DECLARED` row (`distillation.md` §1: what this
project sent) never joins the five outcomes with a fact: it never corroborates a row,
never refines or supersedes one, never contests one. Against the ledger it is either
consistent (`OK`) or it **diverges**: its assertion contradicts a non-superseded,
non-DECLARED row, scopes overlapping → the DECLARED row alone becomes
`DIVERGES <id>[, ..]`; the ledger row is not touched, because our own wrong statement
puts nothing about the product in doubt. Two declarations that contradict each other
are `CONTESTED` — both are still held by their recipients.

The machine then verifies (the `graph` check): ids recompute, sources resolve and their
spans exist, `CONTESTED` is **symmetric** (editing one cell to `OK` fails the check —
the cheapest laundering), a `CONTESTED` pointer at a `SUPERSEDED` row is an error,
dangling ids are errors, duplicates are errors.

## 2. Resolution — only new information

1. **A newer source arrives.** Ingest it normally; re-classify the set with it in view;
   record what supersedes what.
2. **The practitioner rules.** A ruling is a note in `corpus/notes/` whose mandatory
   `basis:` states **the fact they know that the corpus lacks** ("client confirmed Q3 by
   phone on 30 Jul"; "doc B is an unsigned draft"). The ruling enters the ledger as a
   claim (`prov: RULING`, source = that note), and **every prior member of the set —
   including the one it agrees with — becomes `SUPERSEDED <ruling-id>`**: the ruling row
   is now the assertion, and no row lingers contested against rows that no longer
   contest it.

3. **The cascade runs.** The supersession is recorded in the ledger at
   once; the cascade runs at the unit's next closure (`SKILL.md` Phase 5),
   once for every supersession since the last one: `sdlc_check.py stale`,
   whose `## claims` section lists every living document still citing the
   fallen id without naming its successor(s) and every derivation resting
   on a superseded source -- the revision worklist, worked per the kb
   `## Revision` doctrine, one document at a time. The list is derived from
   the ledger's state, so running it later loses nothing; meanwhile the
   citation warn stands in `check` until each document is revised (or an
   append-only correction naming the successors lands), so the worklist
   cannot be silently forgotten. What does not wait for the closure is
   named once, in `SKILL.md` Phase 4 (the two immediate exceptions).

**No basis, no ruling.** A preference is not a fact; the validator refuses a ruling note
without `basis:` exactly as it refuses a DERIVED note without `derived_from:`. If the
practitioner knows nothing new, the set stays `CONTESTED` — a legitimate, permanent,
honest state.

**Rulings are challengeable.** A later source that contradicts a ruling opens a **new**
contested set carrying the ruling's `basis:` beside the new evidence — the practitioner
decides with both in view. Rule-once-forever would be wrong on this corpus's own
premise: signed amendments arrive later.

## 3. The state machine (claim-level, never node-level)

| Event | Effect |
|---|---|
| conflict classified | all members → `CONTESTED <all counterparts>` (symmetric by construction) |
| ruling recorded | ruling row `OK`; every prior member → `SUPERSEDED <ruling-id>` |
| newer source vs a ruling | new set {new row, ruling row}; escalation shows the `basis:` |
| member refined | the refining row inherits the member's contested relations (re-judged); counterparts rewritten to the new id |
| corroboration of a contested member | source appended; the set untouched — more evidence is not new information, and the escalation form shows source counts |
| a declaration contradicts the ledger | the DECLARED row → `DIVERGES <ledger ids>`; the ledger rows stay as they are; escalation names it |
| a new send corrects it | the new DECLARED row; the divergent one → `SUPERSEDED <new-id>` (a declaration is superseded only by a later declaration) |
| a ruling changes the decision | the ledger row → `SUPERSEDED <ruling-id>`; `check` then refuses the stale `DIVERGES` until the declaration is re-judged against the ruling: `OK` if it now agrees, `DIVERGES <ruling-id>` if not |
| bundled row split (`distillation.md` §3) | N atomic rows `OK`, each on its narrowed span; the bundle → `SUPERSEDED <id1>[, <id2> ..]`, text intact; contested relations re-judged per successor |

A superseded row keeps its `not-yet-honored-by` marker with its text. Copy the marker to each successor that still states behavior the code does not have; the analysis or shadow citing the predecessor's id satisfies the successor.

## 3-bis. Splitting a bundled row

A row carrying more than one assertion (`distillation.md` §3 — atomic as provenance,
plural as meaning) is repaired by supersession, never in place:

1. Write one atomic row per assertion, each citing the **narrowed span** that carries
   it (`p=1@<a>-<b>` reaches below a line on a stored `.txt`). Narrow spans mint
   distinct ids by construction.
2. The bundled row becomes `SUPERSEDED <id1>, <id2>, ...` — every successor named,
   its text intact, exactly as refinement keeps superseded text.
3. Contested relations of the bundle are **re-judged per successor**: a counterpart
   usually contests ONE of the assertions, not all of them.
4. The cascade runs (§2, *the cascade runs*): every living document citing the fallen
   id joins the revision worklist, and each citer is revised to the successor in ITS
   scope — the moment a borrowed-capability citation dies.

This is not new information arriving (§2): the source said N things all along; the
ledger only now says them one at a time. No ruling and no `basis:` is needed — the
split is a repair of our own extraction, and it travels with its own diary/commit
record like any claim-table edit.

## 4. Escalation — batched, and in the legal form only

Escalations are presented **once, at the end of a run** — the pipeline never stops
mid-ingest to ask. Each escalation names: the claims in the set, each one's source
(reopenable), date and provenance, and one line on why the machine cannot decide
("same subject, overlapping validity, GIVEN vs GIVEN, no newer source"). A divergence
is escalated the same way, naming the recipient and the day it was sent: the
practitioner corrects it with a new send or changes the decision. One limit stated
out loud: `DIVERGES` is one-way, so unlike `CONTESTED` a hand edit back to `OK` has
no counterpart to fail on — the diff review is what catches it. **A question
that cannot fill this form is not askable** — it is the symptom that the answer is in
the corpus and was not searched. Generic confirmations are not questions.

## 5. Document-level supersession (unchanged)

Whole documents keep the family lifecycle: a superseding note or guide marks the old one
`status: SUPERSEDED`; `supersedes:` in the new one's frontmatter links them. Claims and
documents move independently — superseding a document does not silently resolve the
claims extracted from it; the `corpus` check reports claims resting on superseded
originals for re-verification.

## Rulings that came from another project

An `IMPORTED` row is a ruling made by the owner of a different project
(`portability.md`). Knowledge crosses a project boundary; authority does not.

- It keeps its text, its span and its original `basis:` verbatim — the knowledge is not
  lost, and relabelling it `DERIVED` would make the row lie about its origin.
- It rests on a renamed copy of its note (`imported_<project>_<name>`) that carries
  `imported_from:`. Unnamed, the class says nothing and the row is a `RULING` with the
  label filed off; the validator refuses it.
- **It cannot settle anything here.** `import` reopens the set it had settled: its former
  members and the ruling arrive `CONTESTED` with each other. `SUPERSEDED <id>` pointing at
  an `IMPORTED` row is an error: nobody in this project granted that decision its
  authority.

Ratification is the ruling procedure above, and it is you deciding: your own note with
your own `basis:`, a `RULING` row on it, and every row `CONTESTED` with the imported one —
transitively, when it sits in more than one set — `SUPERSEDED <your id>`, the imported row
included. A `RULING` on a note that names a foreign origin is refused.
