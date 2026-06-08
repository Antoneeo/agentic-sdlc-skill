# Vision della Feature: Vision Governance

## Problema
- La skill impone documentazione tecnica, ma non obbliga gli agenti a ripristinare l'obiettivo finale del progetto prima di proporre o implementare una feature.

## Beneficio Atteso
- Ogni nuova feature viene valutata rispetto a obiettivi, non-obiettivi, utenti target e segnali di successo, riducendo deriva strategica e scope creep.

## Utenti o Stakeholder
- Sviluppatori che usano agenti AI per sviluppo software.
- Team che vogliono mantenere coerenza tra richieste operative e direzione di prodotto.

## Segnali di Successo
- I nuovi progetti inizializzati dalla skill contengono `ai_docs/vision/`.
- Le analisi di feature includono `## Allineamento alla Vision`.
- Le istruzioni operative fermano l'agente quando una richiesta confligge con la Vision.

## Non-Obiettivi / Fuori Scope
- Non introdurre un sistema completo di product management.
- Non rendere obbligatoria una mini-vision per modifiche banali, typo o manutenzione locale senza impatto di prodotto.

## Vincoli e Principi Collegati
- Collegato a `ai_docs/vision/principles.md`: Vision before solution, Alignment over local optimization, Explicit conflict handling.
