---
description: Studio della composizione di KB autonome A/B/C; comportamento attuale, proposta e verifiche necessarie.
status: DRAFT
domain: code
---
# Spike: composizione di conoscenze kb-agentic

## Question to answer
Come consentire a un agente di consultare insieme KB autonome e produrre conoscenza di integrazione senza perdere provenienza, contesto e autorità?

## Time-box
2026-09-08: una sessione di lettura statica; nessuna implementazione o prova su progetti reali A/B/C.

## What was tried
Letti la skill installata, la dottrina e il codice della distribuzione nel repository, `taxonomy.md`, `portability.md`, l'analisi F-030 e la Vision KB Second Brain. Router: no match; metodo code, perché lo studio valuta una capacità della distribuzione. devPNT restituisce Eclosion: non pertinente a questo repository. Il working tree contiene modifiche preesistenti, lasciate intatte.

## Answer / Outcome
La skill organizza ogni KB in topic con claim e fonti riapribili; il recall scende nell'indice e consulta i claim. Export/import trasferisce copie, non istituisce una consultazione federata. `kb_import_plan` salta topic con percorso già presente; non li integra semanticamente. `kb_claim_id` dipende da percorso, locator e quantità, non dall'identità del progetto: un riferimento federato deve qualificare il claim anche con il modulo.

Proposta da discutere: **una composizione esplicita sopra KB autonome**, consultate in sola lettura. Un unico artefatto iniziale dichiara:

- Scopo della composizione, identità stabile e posizione di A/B/C, argomenti offerti e confini di applicabilità.
- Come selezionare le KB pertinenti, poi riusare il recall locale; assenza di accesso distinta da assenza di conoscenza.
- Riferimenti qualificati per modulo e claim, con revisione o impronta delle fonti effettivamente utilizzate.
- Collegamenti tra concetti, differenze di significato e conflitti aperti; nessuna fusione dedotta dall'uguaglianza del nome.
- Sede delle conclusioni trasversali, ciascuna con dipendenze esplicite e autorità locale. Una decisione di A resta una decisione di A.

Le conclusioni trasversali possono crescere in una KB di integrazione con proprie note e claim. Il primo artefatto serve a orientare e collegare: non copia i tre corpus. Percorsi e Markdown permettono un primo uso manuale; risoluzione e validazione automatica dei riferimenti esterni sono capacità da progettare, non già disponibili. Anche la rilevazione di derivati da rivedere deve attraversare i confini: oggi non è dimostrata tra KB indipendenti.

Alternative: importare tutto in una quarta KB riusa strumenti esistenti ma produce copie e collisioni; un servizio di ricerca centralizzato aggiunge infrastruttura non necessaria per il primo caso locale.

## Consequences
Prima dell'implementazione, classificare L3 e definire la Vision della nuova capacità. Verificare con tre piccoli progetti: stesso slug con significati diversi; stesso claim-id in moduli diversi; decisioni locali divergenti; fonte aggiornata dopo una sintesi; modulo non accessibile. Il risultato deve citare le origini, circoscrivere le conclusioni e rendere visibili le parti non verificate.

Decisione di prodotto ancora aperta: consultazione delle KB aggiornate in loco oppure composizione di versioni esportate e fissate. La prima privilegia attualità, la seconda riproducibilità. L'esigenza espressa orienta verso la prima, ma non la conferma.

Fonti: `distributions/kb-agentic-skill/skills/kb-agentic-skill/{SKILL.md,taxonomy.md,portability.md,scripts/sdlc_check.py}`; `ai_docs/solutions/ANALYSIS_kb_portable_knowledge.md`; `ai_docs/vision/features/VISION_kb_second_brain.md`.
