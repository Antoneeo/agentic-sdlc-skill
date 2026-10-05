---
topic: card-continuity
parents: []
synonyms: [Eclosion, ripresa, Monade, appunti, scratchpad]
domain: code
topics: [card-continuity]
description: Continuità della card Eclosion; distinguere baseline RED, nucleo verificato e integrazione aperta.
status: CURRENT
---
# Continuità della card Eclosion

Comprensione dei materiali forniti al 2026-10-04, riverificata riaprendo i due report correnti in `project/inputs/`: sono invariati rispetto alle catture. Nessuna esecuzione della card in questa sessione. L’uguaglianza dei report conserva la provenienza, non aggiunge prova live né verifica il guard successivo. I riferimenti esterni alla fixture citati nei report non sono stati aperti. `OK` nel ledger qualifica la fedeltà al report entro la condizione dichiarata, non una certificazione del runtime corrente.

## Proprietà da preservare

Requisiti riportati dalla baseline, non nuove decisioni: conservare appunti accettati e fonte isolata attraverso la sospensione; mantenere identità originaria; catturare lo snapshot dopo gli eventuali tool in coda; verificare provenienza, accessi correnti e lifecycle. Proteggere il nuovo contenuto privato con il dominio di cifratura chat esistente: `SensitiveJSON` maschera ma non cifra; `resume_parameters` e `result_payload` non sono depositi sicuri per gli appunti. M139/SR16 resta invariato. Fonte: [baseline, L29](../corpus/given/TEST_m145_card_continuity.md).

Invarianti del nucleo riportate dalla review: preservare tutta la sequenza iniziale system/developer; ricalcolare separatamente gli indici request/suffix dopo la rimozione del reasoning; associare univocamente producer/request/call e risultato con ordine causale; ammettere solo storico e span effettivamente precedenti e dichiarati nell'input. Le proiezioni ripetute non devono incorniciare nuovamente il risultato; una chiamata storica fuori offerta resta un dato, non dispatch esecutivo. La coda dipende dal passato, che viene restituito identico. Validare numeri finiti, UUID canonici e identità intere; non confondere differenze lecite del descriptor con identità completa. Fonte: [review, L14-L23 e L44-L48](../corpus/given/REVIEW_m145_card_trace_core.md).

## Comportamento osservato nei report

La baseline descrive veri loop streaming, builder, adapter e assemblaggio SDK, con trasporto/risultato tool simulati. Prima della card: 30 note sintetiche in 20.000 caratteri, marcatore finale e fonte nel secondo input SDK. Alla ripresa: 0/30 note, coda e fonte assenti, sia Responses sia Legacy. La chiamata background preparata usa target `all`, fonte None, isolamento False, timezone None e nessuna continuazione. Il loop è richiamato imponendo la Monade originaria: la perdita di memoria è separata dal routing. Due failure finali senza errori di setup; gli errori dei tentativi iniziali non provano il difetto. Fonte: baseline L12-L27.

La review passa da FAIL nei round 1 e 2 a PASS del solo nucleo nel round 3. La suite finale dell'autore riporta 370 PASS e due casi reali card esclusi. Include un producer reale a due richieste attraverso cifratura, claim e caricamento; non equivale alla copertura produttiva completa di quelle superfici. Fonte: review L38-L52.

## Riconciliazione e limiti

Il click completo Eclosion resta **NON VERIFICATO**, non dichiarato attualmente guasto sulla sola baseline storica. Il PASS del nucleo non supersede il RED end-to-end: ambito e prove differiscono, e i due laboratori card rimangono esclusi. A2/A3 non sono chiusi. Il vecchio TDD `technical_design_extracted_source_continuity` escludeva la persistenza attraverso pausa; il TDD A1 riguarda buffer/capacità. La review cita poi un design dedicato `technical_design_card_run_continuity` v1.1 approvato: ciò soddisfa un distinto passaggio progettuale dichiarato, non dimostra completamento. Gli artefatti approvati non sono inclusi qui e non sono stati verificati direttamente.

Restano aperti provenienza di tutti gli input builder, registrazione/freeze, integrazione worker/claim/load, legacy completo, routing/privacy, guard seed/esclusione cattura nativa e laboratori card. I 370 PASS precedono il guard successivo. Membership è simulata: autorizzazioni, revoche, reset, scadenze, concorrenza, effetti HTTP e consegna privata non sono provati. Un solo tool osservato non dimostra idempotenza HTTP; fonte anonima assente non dimostra perdita di ogni upload; rischio di cambio Monade nel routing non equivale a cambio osservato dopo ARS. Prefissi conservati su input simulati non provano hit o costo provider.

Copertura dichiarata, non completa: grafo 1.114 file Python, cov `df3fe79aa0ab`, 17 simboli non indicizzati; ricerca testuale 1.259 file; allegato autore 2.152 con harness/worktree. Gli allegati con la delta non sono disponibili nella fixture. `restore_finalized` e `result_observation` risultano consumati solo da test nel report; non inferire assenza di altri consumer. Fonte: review L25.

La relazione con [l’identità locale](card-identity.md) rimane: scegliere `original_id` in una funzione non prova il routing del click. La nuova milestone eredita i limiti della baseline e del PASS del nucleo, non una certificazione end-to-end.

## Prossimo intervento e riverifica

Riaprire i report e i sorgenti/config/test reali richiamati dal design dedicato, poi ottenere prove aggiornate della ripresa Responses e Legacy e del guard successivo. Una modifica a producer, builder, adapter, worker, routing o lifecycle rende queste osservazioni da riverificare. Hash e snapshot invariati dimostrano solo conservazione documentale. Ipotesi non provate: ripresa ora corretta, privacy completa, idempotenza HTTP e continuità universale degli upload; non usarle come premesse.

## Claims

| id | claim | valid | qty | about | source | prov | state |
|---|---|---|---|---|---|---|---|
| 4ffd300b0458 | Il report baseline registra perdita delle note alla ripresa in entrambi i protocolli. | if baseline locale documentata del 2026-10-04; Monade originaria forzata | - | - | corpus/given/TEST_m145_card_continuity.md#L16-21 | GIVEN | OK |
| 4c61799cfbd4 | La baseline non verifica le autorizzazioni reali. | if guardia membership simulata | - | - | corpus/given/TEST_m145_card_continuity.md#L27-27 | GIVEN | OK |
| b75c36d20292 | Il round 3 dichiara PASS limitato al nucleo. | if review statica sul sottoinsieme descritto, non integrazione completa | - | - | corpus/given/REVIEW_m145_card_trace_core.md#L46-48 | GIVEN | OK |
| 2b110b9a5813 | La suite finale riportata conta 370 PASS, con due casi reali card esclusi. | if suite precedente al successivo guard seed/cattura nativa | - | - | corpus/given/REVIEW_m145_card_trace_core.md#L52-52 | GIVEN | OK |
| 3f9bba3e32a6 | L’integrazione elencata rimane CANNOT_VERIFY e non consente DONE. | if perimetro del report fornito | - | - | corpus/given/REVIEW_m145_card_trace_core.md#L50-50 | GIVEN | OK |
