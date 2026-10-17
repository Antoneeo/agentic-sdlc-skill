---
description: Vision della conoscenza cumulativa del software, comune ad agentic-sdlc e kb-agentic e riutilizzabile fra milestone e sessioni.
status: APPROVED
---
<!-- Testo fornito da Antonio Pinto e adottato come riferimento con «Avvia l’analisi sulla base di questa Vision», 2026-10-04. Blind check: PASS, review F-063 vision_gate. Formattazione Markdown normalizzata; contenuto invariato. -->

# M-VISION — Conoscenza cumulativa del software a supporto dello sviluppo

## Problema

Le analisi producono conoscenza che resta dispersa fra documenti, review e conversazioni. Le sessioni successive devono ricostruirla, rischiando di perdere le relazioni fra obiettivi, comportamenti e dettagli implementativi. La documentazione cresce senza un equivalente aumento della comprensione riutilizzabile.

## Beneficio atteso

Ogni intervento rende il software più comprensibile per quelli successivi. L’agente può partire dal quadro generale, approfondire soltanto ciò che serve e mantenere visibili le proprietà che le decisioni tecniche devono preservare.

## Attori

- **Agente di sviluppo e reviewer:** orientarsi, progettare e verificare usando conoscenza condivisa e fondata.
- **Responsabile del progetto:** ottenere continuità di comprensione, meno ricostruzioni e rilavorazioni, decisioni più leggibili.

## Ambito

Integrare agentic-sdlc e kb-agentic affinché analisi, progettazione e verifica consultino e alimentino **un grafo di conoscenza comune, dedicato al progetto software e riutilizzabile fra milestone e sessioni**.

Il grafo organizza concetti e relazioni a diversi livelli di astrazione, collegando il funzionamento generale alle evidenze nel codice e nei test. La copertura cresce attraverso il lavoro: le aree inesplorate restano riconoscibili.

## Garanzie essenziali

- Distinguere funzionamento osservato, requisiti, ipotesi e cambiamenti progettati.
- Fondare le affermazioni su evidenze rintracciabili, conservandone condizioni e limiti.
- Riconciliare conoscenza nuova ed esistente, evitando duplicazioni e contraddizioni silenziose.
- Verificare e aggiornare la conoscenza interessata dalle modifiche al software.
- Riutilizzare le capacità di kb-agentic senza creare un sistema parallelo di gestione della conoscenza.

## Segnali di successo

Una sessione nuova riesce a ricostruire il funzionamento interessato navigando dal generale al particolare, senza ricomporre la cronologia delle analisi precedenti. Un intervento successivo riutilizza conoscenza già acquisita e identifica ciò che deve ancora verificare. Una proposta non implementata non viene presentata come comportamento esistente; una modifica rende riconoscibili le conoscenze superate.

L’efficacia viene valutata su casi diversi, misurando correttezza, lavoro di ricostruzione e rilavorazioni.

## Non-obiettivi

Mappare preventivamente tutto il repository; riversare indiscriminatamente documenti o codice nel grafo; sostituire le evidenze con sintesi non verificabili; aggiungere burocrazia documentale; confondere il grafo concettuale con il solo grafo delle dipendenze del codice.
