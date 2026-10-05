---
status: CURRENT
description: Quattro proprietà riusate nella nuova milestone, con configurazione corrente e limiti delle prove
domain: code
topics: [software-properties, card-continuity, retry-policy, card-identity]
---
# Spike: quattro casi software

## Question to answer
Si può dichiarare verificato il click Eclosion, quale retry applica il frammento corrente, cosa autorizza il design approvato e quale identità conserva la card? Aggiornamento della conoscenza esistente sui sette input correnti; nessuna modifica software e nessun test esterno.

## Time-box
Una sessione di consultazione mirata, confronto degli input e riconciliazione della memoria. Tempi e percorsi della sessione corrente sono in session2_metrics.json alla radice del fixture; nessun runtime Eclosion avviato.

## What was tried
Livello Spike; router: no match. Riusata la gerarchia software-properties → card-continuity / retry-policy / card-identity e aperte le note con le fonti originali catturate. Letti gli input correnti. La verifica evidence iniziale ha trovato report Eclosion e retry-test corrispondenti, config retry CHANGED, vecchio sorgente identity e suo risultato UNAVAILABLE. Nuove catture conservano la configurazione a uno e il sorgente nel nuovo percorso; vecchi bytes, binding e claim sono preservati. Nessuna prova software rieseguita: interpretazioni statiche e risultati riferiti restano distinti.

## Answer / Outcome

| Caso | Risposta sostenuta | Fonti e limite |
|---|---|---|
| Click completo Eclosion | Non verificato. La baseline documenta 30/30 → 0/30 note, coda e fonte assenti, in Responses e Legacy; il PASS statico e i 370 PASS del nucleo hanno scope diverso. | Claim 253a9eb30ee4, c4289356c1c2, cc912a8b91ce, 2dc98a10f042 e 7e3b3eb37150; inputs/TEST_m145_card_continuity.md e inputs/REVIEW_m145_card_trace_core.md, riaperti e corrispondenti alle catture. Due laboratori card esclusi, integrazione produttiva/worker/legacy/routing/privacy aperta, guard seed successivo non coperto. |
| Retry corrente | Se il chiamante passa la configurazione fornita, attempt ha budget 1: massimo una chiamata e False se il primo risultato è falso. Nessun ritardo/backoff nel corpo. | 8a2c2a590ef0, 2bd18d77260c e b094373754b3; inputs/retry.py:1-5 e inputs/retry-config.json:1. Sono conclusioni statiche: caricamento effettivo del JSON e tempi di operation sconosciuti. |
| Proposta approvata | Cinque tentativi con ritardi esponenziali sono DESIGN, implementazione pending; non descrivono il comportamento esistente documentato. | 8cbe4c563a35, 987cdc1555d1 e c26ac671370b; inputs/retry-proposal.md:2 e cattura corpus/given/retry-proposal-9f23ebb4.txt. Mancano parametri del backoff e prove di implementazione. |
| Identità e prova applicabile | Il frammento corrente restituisce original_id, non current_id. La stessa implementazione è ora in card_identity.py. Il vecchio PASS A/B→A resta attestazione locale archiviata; il suo originale manca e non è prova fresca né end-to-end. | 521033cfbca5, 530a1405d7a5 e 5488954c2729; inputs/card_identity.py:1-2, nuova cattura e precedente cattura di identity-test.txt. Il digest del codice coincide; non basta per attestare esecuzione, import dei chiamanti o collegamento Eclosion. |

Il PASS retry invariato riguarda attempts=3 e falso/falso/vero: b244f34e9684 mantiene questa condizione. Il cambiamento del JSON invalida il riuso della conclusione sul terzo tentativo per il runtime corrente, pur senza cambio in retry.py. Se la prima risposta fosse vera, il budget uno consentirebbe comunque True: la conclusione False è condizionata al primo falso, non universale.

## Consequences
Riusare le relazioni proprietà → comportamento → responsabilità → evidenza già presenti, senza creare un topic per la nuova milestone. La relazione c5540b6ae4f2 supports → card-continuity conserva l'identità come proprietà utile alla continuità; non prova un'integrazione tra i due frammenti. Il controllo retry dipende congiuntamente da codice e configurazione; il risultato locale documenta solo la propria fixture. Un file rinominato richiede nuovo binding e controllo dei consumatori; un risultato rimosso richiede una nuova prova prima di dichiarare verifica attuale.
Prima di correggere Eclosion recuperare design e sorgenti reali. Preservare note/fonte, identità originaria, snapshot dopo tool in coda, autorità iniziale completa, causalità, associazioni, cifratura chat e accessi correnti. SensitiveJSON maschera ma non cifra; non depositare appunti in resume_parameters/result_payload. Revoche, concorrenza, scadenze, idempotenza HTTP, consegna privata e costi provider restano non provati. La baseline e la review sono report, non runtime/patch/harness/log disponibili in questo fixture.
La gerarchia originale resta invariata. Nessuna visione di prodotto approvata o milestone operativa è stata creata. Nessuna guida di codice aggiunta: frammenti semplici; sorgenti del nucleo complesso assenti. Le note correnti sono corpus/notes/retry-policy-current.md e corpus/notes/card-identity-current.md; le precedenti rimangono archiviate con i loro claim sostituiti esplicitamente.
Le verifiche graph/corpus/evidence/check misurano integrità e corrispondenza, non verità dei report o completezza delle dipendenze. MATCHED di un nuovo sorgente non rende disponibile il vecchio risultato, non esegue test e non allarga lo scope di una prova. DESIGN e osservazioni convivono con la loro natura invariata.

## Diary
2026-10-04, ricostruzione dagli input correnti: corretto il riuso del budget a tre (ed7529803c5c → 8a2c2a590ef0) e della conclusione sul terzo tentativo (cf3fdca6a96c → b244f34e9684). Aggiornata la responsabilità identity.py → card_identity.py con byte identici; ca323e332851 → 521033cfbca5 e a6f03a3c8e5b → c5540b6ae4f2. Il risultato identity-test.txt è assente: conservata la cattura storica e dichiarata la perdita di verificabilità corrente. Eclosion e DESIGN retry confermati nei soli limiti già documentati; nessun test esterno eseguito.
