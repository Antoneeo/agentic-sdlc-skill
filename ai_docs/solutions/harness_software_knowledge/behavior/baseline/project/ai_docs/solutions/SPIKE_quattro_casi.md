---
description: Quattro casi, proprietà da preservare e confini delle prove prima di intervenire su continuità card, retry e identità.
status: CURRENT
domain: code
topics: [card, eclosion, continuity, retry, configuration, identity]
---
# Spike: comprensione dei quattro casi

## Question to answer

Che cosa deve sopravvivere al prossimo intervento, che cosa è osservato e che cosa resta ignoto? Ricostruzione del 2026-10-04 dalla conoscenza del progetto e dai sette file correnti in `inputs/`. Nessuna modifica al software né test esterno. Livello Spike; router: no match. La memoria condivisa rinvia a questo documento; le sue conclusioni sono state confrontate con gli originali correnti prima del riuso.

## Time-box

Una sessione limitata ai quattro casi; durata misurata nel file `session2_metrics.json` della fixture. Non è una progettazione del fix né un'autorizzazione a implementare una nuova milestone.

## What was tried

Riletti i due resoconti card, codice/configurazione retry, design accettato e fixture testuale retry. Il vecchio probe fallisce prima delle asserzioni perché `inputs/identity.py` non esiste più. La funzione disponibile è `inputs/card_identity.py:identity(card)` e conserva la selezione di `original_id`. Aggiornato il probe locale alla nuova ubicazione e alla configurazione corrente, separando la vecchia fixture a tre tentativi dal budget attuale. Il nuovo risultato è in `ai_docs/solutions/harness_four_cases/current-result.json`: **9 asserzioni PASS e 3 controlli negativi falliti come atteso**, con data e hash delle tre fonti eseguibili/configurazione; `result.json` resta un risultato storico, non una verifica del tree corrente. I resoconti M145 sono evidenza fornita, non esecuzioni ripetute in questa sessione: sorgenti reali, launcher, patch e log citati nei resoconti non sono fra gli input.

## Answer / Outcome

### 1. Continuità della card Eclosion

**Proprietà da preservare.** La ripresa deve conservare appunti già accettati, coda del buffer e fonte isolata, associandoli all'identità originaria. La baseline richiede snapshot aggiornato dopo eventuali tool in coda, provenienza/accessi correnti, lifecycle e cifratura nel dominio chat esistente: `SensitiveJSON` maschera la visualizzazione, non cifra; `resume_parameters/result_payload` non è un deposito sicuro degli appunti. M139/SR16 resta invariato. Sono requisiti/limiti del documento fornito, non una verifica corrente dei relativi meccanismi.

**Comportamento documentato.** In `inputs/TEST_m145_card_continuity.md` §Prova e risultato, veri loop streaming/builder/adapter/SDK con trasporto e tool simulati mantengono 30/30 note, coda e fonte nel secondo input SDK prima della card. Dopo `_resume_agent`, entrambi i protocolli Responses e Legacy perdono 30/30 note: primo input della ripresa 0/30, coda assente, fonte assente. Il buffer è esattamente di 20.000 caratteri. La card `slot_selector` è riconosciuta dal registry; pending DB e Monade sono verificati. Gli argomenti preparati per `_bg_ai_response_task` sono target `all`, fonte None, isolamento False, timezone None, senza parametro di continuazione. L'esecuzione della ripresa forza la Monade originaria per isolare la perdita di memoria dal routing.

**Stato della prova.** Baseline finale RED: 2 failure, zero errori di setup, 71,84 s. I precedenti errori di fixture sono esclusi dall'evidenza. Il rischio di cambio Monade deriva dal routing preparato, non da un cambio osservato dopo ARS. Membership simulata: nessuna prova di autorizzazioni/revoche/reset/scadenza/concorrenza/effetti HTTP/privacy. Un solo tool di dominio osservato non dimostra idempotenza HTTP. La fonte anonima persa non dimostra la perdita di ogni upload normale. I TDD citati per continuità nello stesso loop e capacità del buffer non coprono la persistenza attraverso pausa.

**Il PASS del nucleo ha un perimetro diverso.** `inputs/REVIEW_m145_card_trace_core.md` documenta due round FAIL, correzioni, poi PASS statico sul nucleo. Le proprietà controllate comprendono tutta l'autorità iniziale system/developer; remapping degli indici dopo reasoning; sidecar iniziale; frame stabili nelle proiezioni ripetute; unicità/identità/ordine di richieste, chiamate e risultati; marker prima dei propri risultati; provenienza e copertura degli span; tool storici fuori offerta proiettati come dati; UUID canonici e autori interi; numeri finiti; differenze descriptor esplicite; retained ledger; passato invariato nella normalizzazione della coda; nessun dispatch storico. Non ridurre la correzione al solo buffer: queste proprietà proteggono associazioni, causalità e autorità della traccia ripristinata.

La suite finale dell'autore registra 370 PASS, 2 casi reali card esclusi, 351,24 s, exit0; include il producer reale a due richieste via cifratura/claim/load, ma precede il successivo guard seed/cattura nativa. Il reviewer non esegue test. Restano aperti ledger/provenienza di tutti gli input del builder, registrazione/freeze di produzione, integrazione worker/claim/load, legacy completa, routing/privacy, esclusione cattura nativa con seed e laboratori card reali. Copertura parziale del percorso claim/load non certifica tutta l'integrazione. Il PASS non risolve la baseline RED né autorizza DONE: nessun nodo è stato chiuso.

La review stessa limita l'enumerazione: grafo su 1.114 file Python con 17 simboli non indicizzati; ricerca testuale su 1.259 file, allegato autore su 2.152 inclusi harness/worktree. `restore_finalized` e `result_observation` hanno consumer solo nei test. Questi conteggi sono riportati, non ricontati qui, e non provano copertura produttiva completa.

### 2. Tentativi e configurazione

**Proprietà da preservare.** `inputs/retry.py:attempt(operation, config)` ricava il budget dalla chiave `attempts`, interrompe al primo risultato vero e restituisce False quando il budget si esaurisce. Il prossimo intervento deve esplicitare un eventuale cambiamento di questi comportamenti; non confondere budget massimo e numero sempre eseguito.

**Stato corrente.** `inputs/retry-config.json:1` imposta **1**, correggendo il precedente valore 3 riportato da questa conoscenza. False, False, True con questa configurazione produce False dopo una chiamata: il terzo risultato non è raggiunto. Un successo iniziale produce True dopo una chiamata; soli False producono False dopo una. `inputs/retry-test.txt:1` dichiara invece una fixture con budget 3: il suo PASS resta una prova circoscritta a quella configurazione, riproducibile localmente, e non descrive il budget corrente. Con budget zero non viene chiamata l'operazione; un'eccezione si propaga. Questi casi descrivono le funzioni disponibili, non nuovi requisiti approvati.

**Ritardi.** Il corpo completo di `inputs/retry.py:attempt(operation, config)` (righe 1–5) è un ciclo di chiamate con ritorno al primo successo: non programma sleep, ritardi o backoff. Sono fuori da questa conclusione eventuali attese interne alla callback e altri wrapper non forniti; non si sostiene che il tempo trascorso sia zero.

**Limite.** Fixture e probe locali non chiamano servizi esterni, non misurano resilienza in rete e non dimostrano successo dopo guasti reali. La configurazione letta non prova quale configurazione usi un deployment. Non sono state esplorate tutte le configurazioni malformate.

### 3. Proposta approvata

**Autorità e proprietà.** `inputs/retry-proposal.md` è un design accettato: cinque tentativi con ritardi esponenziali, implementazione pending. L'approvazione è intenzione autorizzata, non prova runtime. Preservare questa distinzione insieme alla divergenza dal codice/configurazione disponibili.

**Situazione attuale.** La configurazione corrente è 1 e `attempt` non programma ritardi: la proposta non descrive il comportamento implementato negli input. Né il PASS della fixture con tre chiamate né il nuovo probe con una certificano cinque tentativi e backoff. La relazione design approvato → implementazione pending rimane valida; si corregge soltanto il confronto con il budget corrente. Non scegliere silenziosamente fra design e stato corrente, né riscrivere il design per renderli concordi.

**Lacune prima dell'implementazione.** Il documento non precisa ritardo iniziale, moltiplicatore, cap, jitter o classi di errore ammesse. Anche la semantica delle eccezioni richiede una scelta esplicita se deve cambiare. Non inventare questi dettagli come già approvati. Il prossimo intervento deve tradurre il design in criteri osservabili e prove locali, poi verificare separatamente il servizio reale quando autorizzato.

### 4. Identità della card

**Proprietà da preservare.** `inputs/card_identity.py:identity(card)` (righe 1–2) seleziona `original_id`, non `current_id`. Una fixture locale con A originale e B corrente restituisce A. La conoscenza precedente riferiva la stessa funzione a `inputs/identity.py`: quel percorso e `inputs/identity-test.txt` non sono presenti negli input correnti e non sono fonti correnti raggiungibili. La regola è confermata dal sorgente attuale e dalla nuova esecuzione locale; il rename richiede correggere il locator, non attribuire un cambiamento di identità. Questo non prova che altri percorsi la chiamino.

**Confini.** Senza `original_id` si osserva KeyError; non esiste fallback alla chiave corrente in questa funzione. Nessuna verifica end-to-end di click card, routing, membership, persistenza o ripresa; non equiparare il PASS locale alla corretta identità lungo il flusso M145. Gli input non stabiliscono validazione o autorizzazione di A: restituire una chiave non la rende affidabile.

## Consequences

Per il prossimo intervento riusare le relazioni e i loro confini: baseline card → difetto della ripresa; review del nucleo → proprietà della traccia entro il sottoinsieme rivisto; configurazione → budget runtime locale; proposta → intenzione approvata ancora pending; selezione di `original_id` → identità locale, non prova del click. La continuità resta un'integrazione aperta malgrado il PASS del nucleo; il retry attuale e quello approvato restano due stati distinti.

**Applicabilità delle prove dopo i cambiamenti.** Il risultato storico `result.json` dimostrava la fixture con budget 3 e la funzione al vecchio locator: non è un PASS fresco del runtime corrente. La fixture esplicita a tre tentativi conserva il proprio significato e il nuovo probe la riesegue separatamente; le affermazioni di budget corrente sono aggiornate a uno. La proprietà di identità sopravvive al rename ed è ricontrollata tramite `card_identity.py`; la vecchia esecuzione rimane storica. I resoconti card conservano il proprio perimetro documentale perché nessun nuovo input dimostra il fix del click: il RED non diventa GREEN attraverso un rename o una modifica retry. I 370 PASS precedono il guard seed/cattura nativa, e continuano a non coprire quel cambiamento né i laboratori card esclusi. Per la nuova milestone servono verifiche successive agli interventi sul flusso reale, oltre alle proprietà già elencate; qui non sono disponibili né eseguite.

Nessuna guida `source_kind: code` creata: il caso card è complesso ma manca il sorgente da cui ricavare estratti fedeli; le due funzioni presenti sono semplici. I resoconti sono prove da interpretare, non un nuovo runbook operativo da distillare. Questo Spike è la memoria unica, reperibile nell'indice condiviso; i dettagli restano negli input e nel probe. Non sono state prese decisioni architetturali né chiusi nodi di implementazione.
