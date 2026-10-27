---
description: Why a document the project sent is its own claim provenance (DECLARED) that never crosses a project boundary, why its contradiction with the ledger is a one-way DIVERGES, and why the corpus's reach is a lookup by path sharing the validator's one definition of project files.
status: CURRENT
---
# ADR: Declarations as a provenance; the corpus's reach as a lookup

**Status:** Accepted
**Date:** 2026-10-27
**Task ref:** F-084, ANALYSIS_kb_corpus_reach.md

## Context

A field report (REQUEST_kb_corpus_reach.md R1) showed two blind spots. Every
provenance described something that came into the project, so a document delivered
to a client had no home: the KB could not say what had been declared, and a
delivered cell contradicted a ledger decision unseen. And nothing compared the corpus
with the project holding it: 842 files were never examined, and recall answered
`kb: no coverage` with the source one folder away. The Vision's Non-Goal 1 forbids
collecting computed per-document state into one surface (rulings r2, r9).

## Decision

1. A sent document is a `corpus/given/` artifact with `provenance: DECLARED` and a
   `recipient:`; its claims are `DECLARED`. No other provenance may cite one, in any
   source position, and supersession or contest never crosses a declaration: a
   declaration is our statement, not evidence.
2. A declaration contradicting the ledger is held one-way: `DIVERGES <id>` on the
   DECLARED row only. The ledger row is untouched.
3. Declarations never leave the project: `export` drops DECLARED rows and the
   artifacts only they cite (closed by construction, since no other row may point at
   one); `import` refuses them.
4. The corpus's reach is `inventory <path>`, a lookup on a named path with no
   per-state count or filter, plus one upper bound at orient. It walks by
   `sdlc_core.skip_dir`, extracted from `iter_files`, so the validator has one
   definition of project files; classification is by content.

## Alternatives considered

- **GIVEN plus a `direction: outbound` sidecar field** — the row would still read as
  evidence wherever only the row is seen (the probe showed a GIVEN row on such a
  sidecar passing); a provenance of its own makes the confusion a check failure.
- **Reuse `CONTESTED` for a divergence** — symmetric, so our own wrong statement
  would put the decision in doubt, and a ruling would supersede the declaration the
  client still holds. One-way loses CONTESTED's flip-back check (residual accepted,
  R8).
- **Import declarations as `IMPORTED`** — a resend chain then trips the existing
  "settled by an IMPORTED row" refusals, and the converted artifact becomes ground
  again; keeping declarations local removes both.
- **A full listing of files by state** — r2/r9 territory; the owner ruled a lookup
  on a named area (R2).
- **A walker of its own** — would give the validator two definitions of project
  files, and `node_modules` would inflate the count.

## Consequences

- **Pro:** "what did we tell X" is answerable with recipient and date; a divergence
  is held, never silently resolved; `no coverage` names the residue.
- **Con / risk:** a hand edit of `DIVERGES` back to `OK` is undetectable; orient
  pays a stat walk per session (capped at 1 s); an L1 claim edit can fail `check`
  when a DIVERGES row points at the row it changes.
