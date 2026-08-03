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

## 4. Escalation — batched, and in the legal form only

Escalations are presented **once, at the end of a run** — the pipeline never stops
mid-ingest to ask. Each escalation names: the claims in the set, each one's source
(reopenable), date and provenance, and one line on why the machine cannot decide
("same subject, overlapping validity, GIVEN vs GIVEN, no newer source"). **A question
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
- Its note must carry `imported_from:`. Unnamed, the class says nothing and the row is a
  `RULING` with the label filed off; the validator refuses it.
- **It cannot settle anything here.** `SUPERSEDED <id>` pointing at an `IMPORTED` row is
  an error: nobody in this project granted that decision its authority.

Re-ratification is one act, and it is you deciding: read it, write your own note with
your own `basis:`, set `prov` to `RULING`.
