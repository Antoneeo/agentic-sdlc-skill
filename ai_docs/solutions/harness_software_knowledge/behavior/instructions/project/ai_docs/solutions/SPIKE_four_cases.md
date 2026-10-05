---
description: Esito dell’analisi circoscritta dei quattro casi e percorsi della memoria riusabile.
status: CURRENT
domain: code
topics: [card-continuity, retry, card-identity]
---
# Spike: quattro casi di comportamento software

## Question to answer
Ricostruire proprietà da preservare, comportamento osservabile e limiti delle prove di continuità Eclosion, tentativi/configurazione, proposta approvata e identità card.

## Time-box
Un passaggio sui soli otto input forniti e un probe locale; nessuna esplorazione del sistema esterno. Tempo effettivo misurato in session1_metrics.json alla radice della variante.

## What was tried
Lettura integrale degli input e dei supporti della skill pertinenti. Nessuna memoria precedente oltre al README; `recall card` senza corrispondenze. Router inizialmente assente, rigenerato vuoto. Probe locale ripetibile su retry e identità, con controlli negativi; nessuna modifica ai sorgenti. Per la card sono disponibili solo report: prove originarie non rieseguite.

## Answer / Outcome
La conoscenza durevole è unica nei topic: [continuità](../topics/card-continuity.md), [retry corrente e design futuro](../topics/retry.md), [identità](../topics/card-identity.md). Le claim citano copie integrali in corpus/given con digest e origine. Gli stati OK descrivono fedeltà alle fonti condizionata al loro perimetro, non prove generali di prodotto.

## Consequences
Il prossimo intervento riapre i file originali e verifica le dipendenze cambiate: codice, configurazione e test possono cambiare mentre gli snapshot restano identici. Nessuna chiusura M145 e nessuna promozione della proposta a comportamento runtime. Non creato un GUIDE: le funzioni disponibili sono semplici, mentre il sistema card complesso ha solo report, senza estratti del codice reale richiesti per un source_kind code fedele. Nessuna decisione architetturale, nessun nuovo piano di implementazione.
