---
topic: retry
parents: []
synonyms: [tentativi, configurazione, proposta approvata, exponential delays]
domain: code
topics: [retry]
description: Tentativi correnti e design approvato dei cinque tentativi; evidenze separate e condizioni della configurazione.
status: CURRENT
---
# Tentativi, configurazione e proposta approvata

## Caso 2 — proprietà e comportamento corrente

Riverifica locale del 2026-10-04 sui file correnti in `project/inputs/`: il corpo di `attempt(operation, config)` è invariato, ma `retry-config.json` ora contiene `attempts: 1`. La precedente cattura con 3 resta storica; il claim `a263e45bfe82` è sostituito, per la configurazione corrente, da `8283233919b2`. Fonti: [codice riaperto, L1-L5](../../inputs/retry.py), [configurazione corrente, L1](../../inputs/retry-config.json), [cattura corrente](../corpus/given/retry-config_current.json).

Osservazione strutturale: il ciclo usa `range(config["attempts"])`, termina al primo valore truthy restituendo True e restituisce False se esaurisce il ciclo. Non programma alcuna attesa: non ci sono sleep, scheduler o ritardi esponenziali nel corpo fornito. Questo non garantisce durata zero dell'operazione o assenza di attese in altri livelli.

Osservazione eseguita: il [probe della riverifica](../solutions/harness_four_cases/reverify.py) carica direttamente codice e configurazione correnti. Con false, false, true ottiene False dopo **1 chiamata**, senza raggiungere gli altri valori; con true iniziale ottiene True dopo 1. Riprova inoltre la vecchia fixture con configurazione esplicita 3: True dopo 3 chiamate. Il controllo deliberatamente errato «la configurazione corrente consente tre chiamate» fallisce. [Risultato e digest](../solutions/harness_four_cases/reverify_result.json).

Il report `retry-test.txt`, riaperto e invariato, dichiara ancora `attempts=3`. La sua prova resta applicabile al ciclo con quella fixture, non al limite oggi fornito al runtime. La relazione riusata è **codice + configurazione → limite osservato**; il codice immutato non rende attuale la vecchia osservazione.

Proprietà ricostruite, non nuovi requisiti: massimo numero configurato di invocazioni per intero non negativo, interruzione al successo, ritorno booleano. Non sono una decisione di mantenere sempre uno o tre tentativi. Nessuna gestione di eccezioni o errori del servizio è presente nel corpo fornito. Le prove locali non misurano latenza, carico, rete o deployment.

## Caso 3 — design e distanza dall'implementazione

Il [design riaperto, L1-L2](../../inputs/retry-proposal.md) rimane dichiarato approvato: **cinque tentativi con ritardi esponenziali**, implementazione pendente. Il claim `cfb41cab4dcd` continua a descrivere questa intenzione, non l'implementazione. Oggi lo scarto è **1 senza attese programmate → 5 con attese esponenziali**, non più 3 → 5.

Non c'è conflitto da adjudicare: configurazione/esecuzione e proposta hanno autorità diverse. L'approvazione non dimostra che il design sia implementato e non autorizza questa sessione a realizzarlo. Base dei ritardi, tetto/jitter e gestione delle eccezioni non sono specificati né provati; completarli sarebbe nuova progettazione.

## Riverifica

La modifica della configurazione ha attivato la riapertura di codice, config, test e proposta; la prova corrente è stata ripetuta. Restano da verificare caricamento nel deployment reale e qualsiasi wrapper. Il prossimo cambiamento a codice, config o caller riapre queste condizioni. Un test verde con config diversa non basta; hash e snapshot attestano soltanto byte archiviati. Riutilizzare questa relazione nella nuova milestone senza trasformarla in un requisito non approvato.

## Claims

| id | claim | valid | qty | about | source | prov | state |
|---|---|---|---|---|---|---|---|
| a263e45bfe82 | La cattura precedente fissa attempts a 3. | if byte della precedente cattura, sostituita nella riverifica | - | - | corpus/given/retry-config.json#L1-1 | GIVEN | SUPERSEDED 8283233919b2 |
| 2645b6165a46 | Il ciclo legge il limite da config invece di codificare tre nella funzione. | if implementazione fornita di attempt | - | - | corpus/given/retry.py#L1-2 | GIVEN | OK |
| 0fd5585f62ef | Il test fornito riporta PASS per false, false, true con attempts=3. | if fixture locale; nessun servizio esterno | - | - | corpus/given/retry-test.txt#L1-1 | GIVEN | OK |
| cfb41cab4dcd | Il design approvato prescrive cinque tentativi con ritardi esponenziali, con implementazione pendente. | if stato del design riportato, non comportamento corrente | - | - | corpus/given/retry-proposal.md#L1-2 | GIVEN | OK |
| 8283233919b2 | La configurazione corrente riaperta fissa attempts a 1. | if byte correnti forniti nella riverifica del 2026-10-04; deployment non verificato | - | - | corpus/given/retry-config_current.json#L1-1 | GIVEN | OK |
