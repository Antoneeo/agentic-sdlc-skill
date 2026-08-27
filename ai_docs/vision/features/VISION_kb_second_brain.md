---
description: Feature vision for the kb-agentic "second brain" milestone - the recall reflex, the daily gesture, and the time cycle that keep a project KB honest over months of daily use with an agent colleague.
status: DRAFT
---
# Vision Feature: KB Second Brain

## Problema
- La skill sa gia' NAVIGARE il grafo (`taxonomy.md`: descend-don't-scan, ogni parent, sinonimi) - ma solo per PIAZZARE claim dentro un'unita' kb. Nessuna regola fa scattare la stessa discesa quando l'agente deve RISPONDERE su un tema: la lettura esiste come metodo, non come riflesso, e la consultazione resta affidata alla memoria del modello - il meccanismo che non scatta (provato con distill e con l'orient hook).
- I claim non invecchiano ne' cadono: staleness misurata per aree e non per claim, nessun supersede per i claim (i rulings ce l'hanno), catene di derivazione tracciabili ma senza invalidazione - se un claim a monte cade, i DERIVED costruiti sopra restano in piedi.
- Manca il gesto quotidiano: la cerimonia e' proporzionata alle unita' governate, non al giorno. Se scrivere costa, la KB si aggiorna solo nei giorni di cerimonia e i buchi sono il posto dove l'agente inventa.

Le tre derive conseguenti, su mesi d'uso: verita' morte citate con piena fiducia; propagazione senza richiamo; eco-camera (l'agente rilegge le proprie interpretazioni come fatti).

## Beneficio Atteso
Un agente-collega quotidiano su un progetto: KB consultata per riflesso, alimentata ogni giorno a costo ~zero, onesta nel tempo - i claim invecchiano, vengono sostituiti, e la caduta di un claim raggiunge meccanicamente chi ne deriva.

## Sequenza - tre unita', in quest'ordine
1. **Il riflesso di recall + regola anti-eco.** Estendere il consult (oggi solo guide router) ai topic: all'ingresso in un tema, la discesa di `taxonomy.md` gira in modalita' risposta - stessa dottrina, nuovo trigger. Un DERIVED che fonda una decisione richiede il re-touch della fonte (l'anti-eco E' una regola di recall).
2. **Il momento di cattura quotidiano.** I binari esistono gia' (un claim su topic esistente e' L1; `corpus/notes/*` accetta elicited/derived/ruling): manca il MOMENTO - un trigger di fine sessione che chiede "decisioni di oggi da registrare?" e le incanala sui binari esistenti. Nessun formato nuovo.
3. **Il ciclo del tempo.** Staleness per claim, supersede esplicito, invalidation cascade sulle catene, consolidamento periodico. Progettato per ultimo, sui DATI che le prime due unita' generano - come cresce il ledger, cosa invecchia, con che ritmo.

## Segnali di Successo
- Una sessione fredda, su un tema coperto dalla KB, risponde citando claim-id reali senza che l'utente indichi dove guardare.
- Le decisioni del giorno sono nel ledger entro il giorno, con provenance.
- Nessun claim superseded citato senza che il supersede sia visibile.
- Alla caduta di un claim, l'elenco dei derivati da rivedere e' prodotto meccanicamente.
- Il re-touch dei DERIVED decisionali e' tracciato nel log, non dichiarato a parole.

## Non-Obiettivi / Fuori Scope
- Nessuna rilevazione automatica delle contraddizioni semantiche: si parte da supersede esplicito + cascade meccanica.
- Nessuna infrastruttura esterna (RAG, embedding, database): file-based, greppabile, client-agnostica.
- Non e' la memoria personale dell'agente (quella e' del client): questa e' la KB del PROGETTO.
- Nessun hook che interroga il grafo a ogni turno: il recall vuole un criterio di ingresso-nel-tema, non un riflesso incondizionato (lezione distill: il rumore e' il fallimento numero uno).
- Nessun mega-rilascio: tre unita' separate, la terza disegnata sui dati delle prime due.

## Vincoli e Principi Collegati
- Poka-Yoke: recall per costruzione, non per esortazione (stesso ceppo di orient hook e hook distill).
- La provenance esistente (ELICITED/DERIVED/RULING/IMPORTED, catene F-035) e la navigazione di `taxonomy.md` sono il fondamento: queste unita' le riusano, non le sostituiscono.
