---
workstream: F-044 KB Time Cycle (second-brain unit 3 - per-claim staleness, supersede, invalidation cascade)
level: L3
branch: feat/kb-time-cycle
status: DONE, AWAITING RELEASE
since: 2026-08-28
next: the combined release (owner order 2026-08-28, "concludi F-044 poi rilascia tutto"): kb 1.11.0 (F-044 + the quoting/recency fix), code + mkt with their parked F-041/F-042 entries plus the F-043 revision-sentence port; then publish_all.bat (owner's act) and registry verify
details: ANALYSIS_kb_time_cycle.md (design + Diary, COMPLETED); design review FAIL->PASS 2 rounds; closure review PASS 1 round, 3 WARN folded (normpath hardening, six test pins, check-test rename); batteries kb 367 / code 184 / mkt 202, goldens byte-identical
updated: 2026-08-28
---

## The charter (vision unit 3, verbatim)

> **Il ciclo del tempo.** Staleness per claim, supersede esplicito, invalidation
> cascade sulle catene, consolidamento periodico. Progettato per ultimo, sui
> DATI che le prime due unita' generano - come cresce il ledger, cosa invecchia,
> con che ritmo.

Success signals it serves (vision): "Nessun claim superseded citato senza che il
supersede sia visibile"; "Alla caduta di un claim, l'elenco dei derivati da
rivedere e' prodotto meccanicamente."

## The evidence dossier (four field data, all 2026-08-28, recorded in project_notes)

1. Orient alone does not hold doctrine through a session (the F-041 report).
2. F-042 live-verified same day (install wires; opt-in honored).
3. **The strongest:** the 12-document post-mortem named the cascade UNPROMPTED as
   the answer to its own failure: "la decisione della call supera un claim ->
   ogni documento che cita quel claim id risulta meccanicamente stale finche'
   non e' rivisto. Gli errori di oggi sono esattamente il failure mode per cui
   quella macchina e' progettata."
4. 1.10.0 validated by its own error-maker; the discipline half (F-043) shipped -
   the mechanical half is THIS unit, and F-043's L2/L3 boundary hardening
   ("propagation that changes what a claim asserts is not propagation - it is
   L3") prepared its ground.

## Design inputs (what exists)

- Canonical claim schema: 8 columns `| id | claim | valid | qty | about | source |
  prov | state |`, `state`: OK | CONTESTED <id> | SUPERSEDED <id> (templates.md
  owns it). NO per-claim date column today.
- F-035 derivation chains: `derived_from:` on notes, chains walkable to ground;
  the recall anti-echo rule already walks them (F-039).
- Claims live ONLY in `topics/<slug>.md` tables. **Open design question: the
  cascade needs a citation surface** - what does "a document cites a claim id"
  mean mechanically (ANALYSIS/GUIDE/notes referencing `c-...` ids? a new
  `cites:` field? grep-based?), and what does `check` do when a cited claim is
  SUPERSEDED (note? warn? per-document stale list?).
- Reconciliation owns supersession semantics (rulings, basis:); the cascade must
  CONSUME its state machine, never duplicate it.

## Watch out

- **Vision non-goals bind hard:** NO semantic contradiction detection (explicit
  supersede + mechanical cascade only); NO external infra (file-based,
  greppable); no per-turn graph hammering. "Consolidamento periodico" must not
  become a ceremony ratchet - event-driven or command-driven, never a standing
  ritual.
- Per-claim staleness needs a time anchor the schema lacks - adding a column is
  a schema change touching every existing fixture, the validator, claim-id
  hashing (does the id cover the new column? it must NOT, or every id rots),
  goldens, and the eval corpus. Enumerate that blast radius mechanically.
- The unit is kb-only (overlay + kb doctrine files) unless the ANALYSIS proves
  otherwise; the spine should stay untouched.
- Post-compaction session: the F-038 rule - the subagent session grant DIES at
  compaction; re-ask the five-bullet question at the first review gate.
- Backlog item parked (NOT this unit): the help-surface pointer line on the
  spine's unknown-command error path (project_notes).
