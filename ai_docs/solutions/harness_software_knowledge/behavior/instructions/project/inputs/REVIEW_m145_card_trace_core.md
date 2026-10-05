---
description: Review indipendente del nucleo schema2 e ripristino privato della traccia card; integrazione completa ancora aperta.
status: CURRENT
---

# M145 — Review del nucleo della traccia card

2026-10-04. Reviewer `card_trace_core_code_review`, gpt-6-astra high, contesto fresco, Default; invocante Default. Review statica, sola lettura, senza test, scritture o proposte. Riferimenti approvati: `impact_analysis_card_run_continuity` e `technical_design_card_run_continuity` v1.1, shadow in `ai_docs/solutions/`. La review riguarda il sottoinsieme servizio/adapter/predicato di finalizzazione del builder; non autorizza la chiusura di A2/A3.

## Round 1: FAIL

| Rilievo | Gravità | Difetto verificato e correzione implementata |
|---|---|---|
| Autorità iniziale incompleta | BLOCK | Con un messaggio iniziale per i tag, il confronto del solo primo system nascondeva un cambio del prompt principale; la proiezione perdeva il prompt corrente. Ora confronto e conservazione comprendono tutta la sequenza iniziale system/developer. |
| Indici dopo il reasoning | BLOCK | La proiezione rimuoveva reasoning lasciando invariati gli indici dei risultati. Ora le due mappe request/suffix sono ricalcolate separatamente. |
| Causalità e provenienza | BLOCK | Una richiesta poteva dichiarare un proprio risultato futuro come già osservato; identità dello storico e copertura degli span non erano vincolate. Ora ordine, ammissione dello storico e copertura integrale dei contributi sono verificati. |
| Associazione dei risultati | BLOCK | Mancavano unicità producer/request/call, tipo della posizione, ordine call/result e identità della richiesta della card. Ora questi vincoli sono controllati al restore. |
| Chiamata storica fuori offerta | BLOCK | Una chiamata rifiutata a un tool inesistente poteva essere ripresentata come item nativo. Ora richiede proiezione come dato. |
| Normalizzazione della coda | WARN | La coda veniva normalizzata senza il passato. Ora il passato determina la posizione della coda ma viene restituito identico. |
| Schema e descriptor | WARN | Numeri JSON come 1e309 non erano rifiutati; confronto opzioni e identità richiedeva ulteriore verifica. Il parser ora rifiuta float non finiti anche nei JSON annidati; il resto resta alla review round2. |
| Integrazione di produzione | CANNOT_VERIFY | Producer, worker, legacy, ledger di tutti gli input e esclusione della cattura nativa restano da integrare. I due laboratori reali card rimangono RED ed esclusi dalla suite del solo nucleo. |

Conformance round1: campi defaulted e constructor order, retained ledger, cifratura/versione, partial-trace rejection, strict load flag, copia metadata, nessun inserimento di chiamate storiche nella coda esecutiva e predicato di finalizzazione sono presenti. Completezza dell'ammissione, confronto autorità e associazioni fallivano i rilievi sopra. Le superfici non implementate del design non sono incluse nel verdetto.

Copertura consumer dichiarata dal reviewer: grafo su 1.114 file Python, cov `df3fe79aa0ab`, 17 simboli non indicizzati; non certifica zero consumer. Ricerca testuale di progetto su 1.259 file; allegato completo dell'autore su 2.152 include harness e worktree `.claude`. Le differenze sono esplicite negli allegati del design. `restore_finalized` e `result_observation` hanno ancora solo consumer nei test.

## Verifiche dell'autore e round 2

Artefatti sotto `.workdir/agent-work-continuity/`:

- `card-service-review-boundaries-red.xml/log`: tre nuovi casi, 3 FAIL; `review-boundaries-green`: 3 PASS.
- `card-service-review-associations-red2.xml/log`: 8 FAIL e 3 PASS; `review-associations-green`: 11 PASS. La prima preparazione dei test aveva una codifica tuple/list non corretta: esclusa dalle prove del difetto e sostituita da una fixture che dimostra l'ammissione del caso sano.
- `card-service-review-schema-red.xml/log`: 2 FAIL e 1 PASS per float non finito e falso collegamento input/risultato.
- `card-service-review-core-green.xml/log`: 363 PASS, 2 casi reali card esclusi, 0 failure/error; 348,02s, 176 warning; exit0. Questa versione precede i fix round2.

## Round 2: FAIL

Review dello stesso reviewer su `card-v2-core-review-r2.patch` e sorgenti correnti: i casi specifici di autorità, reasoning, associazione nativa/card, tool fuori offerta e normalizzazione della coda sono corretti. Restano tre BLOCK: sidecar assente nel producer iniziale che fa più richieste; frame del risultato ricorsivo dopo proiezioni ripetute; marker di richiesta non obbligatoriamente precedente ai propri risultati e span con event_id non legato all'input effettivo. WARN su confronto/report delle differenze lecite del descriptor e validazione stretta delle identità. Prove di integrazione produttore/worker restano CANNOT_VERIFY e aperte.

## Verifica dei fix round 2

`card-service-review-cycles-red2.xml/log`: 6 FAIL e 11 PASS, 37,60s. I fallimenti coprono sidecar nel primo producer, tre proiezioni successive, marker riordinato, span futuro, UUID backend non valido e autore booleano. `card-service-review-cycles-green.xml/log`: 17 PASS, 38,08s, exit0. I test dimostrano anche l'ammissione della fixture non danneggiata, prima della mutazione.

Le posizioni dei risultati sono ora esportate in ogni producer evidence-enabled; i risultati già proiettati, validati dalla sidecar backend, non vengono incorniciati ricorsivamente. Il marker precede gli eventi di esecuzione della propria richiesta; un risultato della stessa richiesta non è un input già osservato. Gli span con event_id devono precedere il marker ed essere dichiarati nell'input. UUID canonici backend e autore/config strettamente interi sono controllati. Il confronto del descriptor tratta esplicitamente modello effettivo, opzioni e scelta corrente dei tool; registra differenze lecite di pinning/finalizzazione senza confonderle con identità completa del descriptor.

## Round 3: PASS sul nucleo

Astra ha riletto sorgenti, patch e test: nessun BLOCK/WARN residuo sui rilievi dei tre round. Conformance esplicita per autorità completa, remapping reasoning, sidecar iniziale, frame stabili, identità/ordine risultati e card, offerta corrente, cronologia, span, UUID/autori, numeri finiti, confronto/report descriptor, normalizzazione della coda, retained ledger e assenza di dispatch storico. Il reviewer non ha eseguito test: il caso positivo a due richieste è presente, ma il suo esito runtime è riservato alla suite dell'autore.

Restano CANNOT_VERIFY e lavoro aperto: provenienza di tutti gli input del builder; registrazione e freeze di produzione; worker/claim/load; ricostruzione legacy completa; routing/privacy; esclusione cattura nativa con seed; laboratori reali card. Il PASS non copre questi elementi e non consente DONE.

La suite `card-service-review-final-green.xml/log` ha concluso con **370 PASS**, 2 casi reali card esclusi, 0 failure/error, 351,24s, 181 warning, exit0. Include il producer reale a due richieste attraverso cifratura, claim e caricamento. Queste prove precedono il successivo guard seed/cattura nativa, che richiede la propria verifica. Nessun nodo chiuso. Conservazione dei prefissi verificata su input simulati, non su hit o costo del provider.
