---
description: Vision approvata per una skill della famiglia Agentic SDLC che progetta corsi fondati sulle fonti e verificabili rispetto ai compiti dei destinatari.
status: SUPERSEDED
---

<!-- Historical version: approved by Antonio Pinto, 2026-09-26; superseded by ai_docs/vision/features/VISION_course_creator.md after the 2026-09-27 owner approval. Blind gate review PASS in round 3. -->

# Vision Feature: course_creator

## Problema

Trasformare documenti o conoscenze in slide può produrre un materiale accurato ma inadatto a chi dovrà usarlo. Se non sono espliciti il destinatario, ciò che sa già, il compito che dovrà svolgere e le condizioni in cui agirà, il corso può introdurre concetti prima dei loro prerequisiti, dedicare spazio a nozioni già note e omettere quelle necessarie. Una presentazione scorrevole può quindi lasciare il partecipante incapace di agire, senza che l'autore se ne accorga.

## Beneficio atteso

Una persona che prepara formazione a partire da fonti può costruire, per destinatari identificati, un percorso che li mette in condizione di svolgere compiti definiti nel loro contesto reale. Le spiegazioni importanti restano verificabili nelle fonti; per le capacità che il corso dichiara di insegnare sono previste attività pratiche e prove pertinenti ai compiti. Il materiale può essere consegnato come corso progettato prima di una prova con i destinatari, ma porta la dicitura «efficacia non verificata» finché quella prova non sostiene una conclusione diversa.

## Attori

- **Autore della formazione** — vuole trasformare fonti e obiettivi in un corso utilizzabile; una buona esperienza gli permette di vedere prima della produzione dei materiali quali capacità insegnerà, a chi, con quali fonti e come ne verificherà l'acquisizione.
- **Destinatario della formazione** — vuole svolgere un compito che oggi non sa svolgere con sufficiente autonomia o correttezza; una buona esperienza parte da ciò che sa davvero, introduce i prerequisiti necessari e gli fa praticare il compito nelle condizioni in cui dovrà applicarlo.
- **Responsabile del contenuto** — vuole poter verificare che il corso non attribuisca alle fonti fatti, condizioni o decisioni che non contengono; una buona esperienza rende rintracciabili le affermazioni sostanziali e visibili lacune e contraddizioni.

## Segnali di successo

- Un revisore che non ha seguito la preparazione può collegare ogni capacità promessa a un compito del destinatario, ai concetti necessari, alle fonti che sostengono le spiegazioni e a una prova che richiede di esercitare quella capacità. Un collegamento mancante resta visibile come lacuna, non viene riempito per supposizione.
- Un prerequisito necessario che il destinatario non dimostra di possedere viene insegnato o dichiarato esplicitamente come limite del corso. Il ruolo professionale o l'autovalutazione da soli non valgono come prova di padronanza.
- Prima di chiamare il corso efficace, una prova con destinatari il cui ruolo, conoscenze iniziali e contesto operativo corrispondono al pubblico dichiarato verifica il compito finale nelle condizioni previste. Il profilo dei partecipanti e la soglia di riuscita sono definiti prima della prova; senza questa evidenza lo stato resta «efficacia non verificata».
- Le affermazioni sostanziali del corso possono essere ricondotte a fonti identificabili e al loro stato di validità; un contrasto fra fonti che cambia ciò che si insegna viene esposto al responsabile del contenuto.

## Non-obiettivi e confini

- Un insieme di slide, un riassunto di fonti o un indice di argomenti non è di per sé un corso completato: manca il collegamento verificabile fra destinatario, compito e prova. Il formato di consegna resta libero quando quel collegamento esiste.
- La skill non presume competenze dei destinatari né inventa affermazioni per colmare lacune delle fonti. Un'incertezza che incide sul percorso o sulla correttezza del contenuto viene dichiarata.
- Una review del materiale può stabilire coerenza e fedeltà alle fonti; non dimostra da sola che i destinatari abbiano imparato. La skill non presenta una previsione di efficacia come risultato osservato.
- La skill progetta la formazione; non gestisce iscrizioni, assegnazioni, calendari o avanzamento delle persone. Può conservare gli esiti di una prova del corso per rivederne il progetto, ma non crea registri individuali continuativi di tentativi, punteggi o completamenti.

## Definizioni operative

- **Fonte**: contenuto riapribile con origine identificata. Può essere un documento, codice, una registrazione o una nota datata di un'intervista che attribuisce le affermazioni alla persona ascoltata. Una conversazione non fissata in un artefatto riapribile non è una fonte citabile; l'attribuzione di una testimonianza non ne prova da sola la correttezza.
- **Corso progettato**: percorso con destinatari, compiti, spiegazioni fondate, pratica e prove coerenti, pronto alla consegna come materiale. **Corso di efficacia verificata**: corso progettato per il quale una prova con destinatari corrispondenti al pubblico dichiarato ha raggiunto la soglia di riuscita prestabilita. Un corso progettato non è per questo di efficacia verificata; ogni corso di efficacia verificata è anche un corso progettato.

## Vincoli e principi collegati

- Questa è una proposta di nuova skill della famiglia, sviluppata con `agentic_sdlc` in modalità Standalone. La Vision di progetto approvata in `ai_docs/vision/project_vision.md` resta superiore a questa bozza; la nuova skill non richiede devPNT, servizi remoti o un account per funzionare.
- La disciplina di fedeltà proposta ha due verifiche distinte: **fedeltà alle fonti** per ciò che il corso afferma e **fedeltà al compito del destinatario** per ciò che il corso insegna ed esamina. `kb_agentic` governa l'ingestione e il recupero della conoscenza quando sono necessari; `course_creator` governerebbe la trasformazione didattica, senza diventare una seconda autorità sul corpus.
- Le dipendenze fra concetti e le conoscenze iniziali del destinatario devono essere esplicite prima di ordinare le spiegazioni. Il grafo dei prerequisiti è la direzione di design proposta per rendere controllabile questa proprietà; struttura, granularità e verifiche appartengono all'analisi successiva.
- L'ordine riguarda concetti e attività formative all'interno di un corso. Non stabilisce priorità di lavoro nel repository né assegna attività alle persone.
- La Vision non stabilisce ancora il numero, il nome o lo schema degli artefatti di lavoro. Use case, interfacce operative dopo il corso, rischi, strategia didattica e materiali saranno progettati in unità successive, ciascuna tracciata al beneficio atteso.
