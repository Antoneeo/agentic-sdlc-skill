---
description: Feature vision for the kb-agentic "second brain" milestone - governed recall, the daily gesture, and the time cycle that keep a project KB honest over months of daily use with an agent colleague.
status: DRAFT
---
# Vision Feature: KB Second Brain

## Problema
- kb-agentic governa la SCRITTURA della conoscenza (claim ledger con provenance, catene di derivazione, corpus con integrita' dei puntatori, distillazione) ma non la LETTURA: nessun meccanismo porta l'agente a consultare ledger e grafo al momento giusto. La consultazione e' affidata alla memoria del modello - lo stesso meccanismo che non scattava per la skill distill ("ALWAYS use" mai invocata) e per il processo (l'orient hook e' nato cosi').
- I claim non invecchiano: un ELICITED di mesi fa resta "vero" per sempre. La staleness e' misurata per aree, non per claim; non esiste supersede per i claim (i rulings ce l'hanno); le catene di derivazione rendono tracciabile chi dipende da chi, ma se un claim a monte cade nessun processo invalida chi lo cita - tracciabilita' senza invalidazione e' un'autopsia, non un'immunita'.
- La cerimonia attuale e' proporzionata alle unita' governate; manca il gesto quotidiano a basso attrito che cattura la decisione del giorno. Se scrivere costa, la KB si aggiorna solo nei giorni di cerimonia e i buchi diventano il posto dove l'agente inventa.

## Beneficio Atteso
Trasformare un agente in un collega quotidiano su un progetto: una KB che viene consultata per costruzione, alimentata ogni giorno a costo trascurabile, e che resta onesta nel tempo - i claim invecchiano, vengono sostituiti, e la caduta di un claim raggiunge chi ne deriva.

## Utenti o Stakeholder
- L'operatore che lavora ogni giorno sul progetto con l'agente (oggi: Antonio).
- L'agente stesso, su qualunque client della famiglia (Claude Code, Codex, Gemini, Antigravity): il recall deve funzionare anche dove non esistono hook per-turno.
- Le sessioni future a freddo, che ereditano la KB senza il contesto della conversazione.

## Le tre derive che questa vision presidia
1. **Verita' morte citate con piena fiducia** - claim mai piu' verificati che fondano decisioni.
2. **Propagazione senza richiamo** - un claim a monte si rivela errato e i DERIVED costruiti sopra restano in piedi.
3. **Eco-camera** - l'agente scrive la propria KB e la rilegge come autorita': le interpretazioni di ieri diventano i fatti di oggi.

## Sequenza (tre unita', in quest'ordine)
1. **Recall governato + regola anti-eco** - all'ingresso in un tema, ledger e grafo vengono interrogati per costruzione, non per buona volonta'; un DERIVED che sta per fondare una decisione richiede il re-touch della fonte. Le due regole viaggiano insieme perche' l'anti-eco E' una regola di recall.
2. **Il diario quotidiano** - il gesto da trenta secondi (decisione del giorno + perche') che alimenta il ledger senza aprire una unita' L3.
3. **Il ciclo del tempo** - staleness per claim, supersede esplicito, invalidation cascade sulle catene, consolidamento periodico. Progettato per ultimo, sui DATI che le prime due unita' generano: come cresce davvero il ledger, cosa invecchia, con che ritmo. Progettarlo prima significherebbe progettare sull'ipotesi.

## Segnali di Successo
- Una sessione fredda, interrogata su un tema coperto dalla KB, risponde citando claim-id reali - senza che l'utente indichi dove guardare.
- Le decisioni del giorno compaiono nel ledger entro il giorno, con provenance, a costo percepito ~zero.
- Nessun claim superseded viene citato senza che il supersede sia visibile nella risposta.
- Quando un claim viene invalidato, l'elenco dei claim derivati da rivedere e' prodotto meccanicamente, non ricostruito a mano.
- Il re-touch delle fonti per i DERIVED decisionali e' tracciato (visibile nel log, non dichiarato a parole).

## Non-Obiettivi / Fuori Scope
- **Nessuna rilevazione automatica delle contraddizioni semantiche**: e' un problema semantico, non sintattico; prometterla sarebbe magia. Si parte da supersede esplicito + cascade meccanica sulle catene.
- **Nessuna infrastruttura esterna** (RAG, embedding, database): la KB resta file-based, greppabile, client-agnostica - la portabilita' della famiglia non si negozia.
- **Non e' la memoria personale dell'agente** (quella appartiene al client, es. l'auto-memory di Claude Code): questa e' la KB del PROGETTO, condivisa tra client e sessioni.
- **Nessun hook pesante per-turno che interroga il grafo a ogni prompt**: il recall ha bisogno di un criterio di ingresso-nel-tema, non di un riflesso incondizionato - il rumore e' il fallimento numero uno da evitare (lezione distill).
- **Nessun mega-rilascio**: tre unita' separate, ciascuna con la propria review e il proprio numero - la terza disegnata sui dati delle prime due.

## Vincoli e Principi Collegati
- Vision before solution; una milestone, tre unita' incrementali.
- Poka-Yoke: il recall per costruzione batte il recall per esortazione (stesso principio dell'orient hook e dell'hook distill).
- Fase osservativa prima del design dove i dati non esistono ancora (il ciclo del tempo attende i dati del diario e del recall).
- La provenance esistente (ELICITED/DERIVED/RULING/IMPORTED, catene F-035) e' il fondamento: queste unita' la usano, non la sostituiscono.
