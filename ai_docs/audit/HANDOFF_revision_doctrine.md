---
workstream: F-043 Revision doctrine (delta-append is the failure; full re-read is the gesture)
level: L3
branch: feat/revision-doctrine
status: DONE, MERGED
since: 2026-08-28
next: publish kb 1.10.0 (owner's act, publish_all.bat) -> polling verify
details: ANALYSIS_revision_doctrine.md (+ this file: post-mortem verbatim)
updated: 2026-08-28
---

## The field post-mortem (verbatim, external session, 2026-08-28)

An agent realigning 12 knowledge documents after a stakeholder call, on a
kb-governed project. Reported to the owner, pasted here as product input:

> **Revisione per delta invece che per riscrittura.** Per riallineare le analisi
> alla 1.2 ho aggiunto — sezioni «Estensioni dalla call», banner «SUPERATO»,
> barrati — senza rileggere il corpo esistente. Ogni frase pre-call non toccata
> è rimasta in piedi come verità stampata [...]
> **Nuova conoscenza messa in quarantena invece che fusa.» I requisiti della
> call vivevano in una sezione a parte con la loro cronaca: il progettista
> doveva fare archeologia per ricostruire lo stato [...]
> **Premessa falsa sopravvissuta.** Il punto aperto 3 era sbagliato da luglio:
> nessuna revisione lo ha mai riletto contro le regole di dominio [...]
>
> Il meccanismo che li produce non è distrazione: è che lo strumento di edit
> spinge verso modifiche ancorate e locali — cerchi una stringa, la sostituisci,
> non rileggi mai il file intero. Ogni edit è corretto; l'invariante globale
> «il corpo legge lo stato attuale» non viene mai riverificato. La compattazione
> l'ha amplificato [...] la passata «12 documenti in un giro» ha ottimizzato la
> copertura del delta, non l'integrità di ciascun documento.
>
> **Doctrina di revisione (manca oggi).** La skill disciplina la scrittura
> (distillation) e il conflitto tra fonti (reconciliation), ma non ha un
> protocollo di revisione: «recepire nuova conoscenza in un documento esistente
> = rilettura integrale, corpo riscritto allo stato attuale, storia nel Diario —
> mai delta-append». È il triage L2 («propagation of settled knowledge,
> correcting a stale copy») che nomina il problema senza prescrivere il gesto.
> [...] La riga del remind potrebbe portarne l'eco.
>
> **Il controllo meccanico esiste già nel tuo disegno: è l'opzione C.** [...]
> col claim ledger [la staleness semantica] lo diventa: la decisione della call
> supera un claim → ogni documento che cita quel claim id risulta meccanicamente
> stale finché non è rivisto. Gli errori di oggi sono esattamente il failure
> mode per cui quella macchina è progettata.
>
> Quello che la skill non potrà mai fare: [la premessa falsa] richiedeva il
> giudizio di dominio. Lì la rilettura integrale non garantisce la cattura —
> ne alza solo la probabilità.

## The unit (when opened)

**The gesture, as doctrine (kb lens first):** incorporating new knowledge into
an existing document = full re-read + body rewritten to CURRENT state + history
in the Diary/notes — never delta-append; a SUPERATO banner is a tombstone, not
a revision. Wire it where the trigger already fires without prescribing the
gesture: the L2 triage row and the L3 distillation phase. Candidate carriers:
three lines in SKILL.md (or a small revision.md), and possibly an echo in the
`remind` line.

## Watch out

- **remind budget:** the line is a CONSTANT under a 500-char cap with a jargon
  blacklist and its own battery; an echo (~"revisions = full re-read, never
  append") must fit and stay self-contained. Adding costs every prompt — weigh.
- **Lens scope:** the report speaks kb vocabulary (distillation/reconciliation),
  but the code lens shares the failure mode on ANALYSIS updates. Decide in the
  ANALYSIS whether the doctrine is kb-only or a spine-worthy sentence ×3.
- **The claim-ledger half is NOT this unit:** it is the vision's unit 3 (staleness
  per claim, supersede, invalidation cascade) — this report is its third and
  strongest field datum, recorded in project_notes. Unit 3 stays deferred until
  the owner calls it; this unit ships only the discipline half.
- **The domain-judgment limit is real:** the doctrine raises capture probability,
  never guarantees it — say so in the doctrine text itself, no overclaiming.
