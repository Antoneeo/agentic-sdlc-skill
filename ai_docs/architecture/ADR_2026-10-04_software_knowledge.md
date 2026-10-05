---
description: Why software development captures and updates project concepts through the shared KB engine.
status: CURRENT
---
# ADR: Conoscenza software sul grafo KB condiviso

**Status:** Accepted
**Date:** 2026-10-04
**Task ref:** F-063 / F-064
**Digest:** Un solo grafo concettuale del progetto; metodi KB condivisi, kind opt-in e binding agli input dichiarati; escluse memoria parallela e migrazione totale; digest non certifica semantica o completezza.

## Context

La Vision approvata richiede comprensione riusabile fra sessioni e milestone,
con aggiunta e aggiornamento durante il lavoro. Il catalogo F-057 ritrova documenti,
ma non distingue meccanicamente proposte da osservazioni né una copia storica dal
software corrente. Eclosion ha mostrato perché un PASS del nucleo e il percorso
completo devono restare affermazioni distinte.

## Decision

Riutilizzare topics/corpus, claim ledger e riconciliazione di kb-agentic.
F-064 porta metodi e template nelle quattro distribuzioni e aggiunge il formato
tipizzato compatibile, capture-source, evidence e chiusura transitiva dell'export.
F-063 collega questi metodi ai momenti SDLC esistenti, anche nell'analisi senza
modifica al codice. Il router conserva un solo proprietario del lavoro.

I claim distinguono natura, provenienza e stato. Le derivazioni hanno premesse
congiunte; le fonti alternative di un claim sono corroborazioni indipendenti.
Il progetto conserva un UUID; il binding include percorso relativo, digest del file,
span e ruolo. La cattura conserva byte esatti senza avanzare automaticamente la lettura.
L'import conserva identità e autorità straniere, senza adottarle localmente.

## Alternatives considered

- **Solo istruzioni e natura nella prosa:** mantiene compatibilità, ma lascia
  interamente manuale il riconoscimento di fonti mutate; mantenuta come controllo
  nel confronto comportamentale, non come garanzia meccanica.
- **Archivio software separato:** duplica collocazione, riconciliazione e provenienza,
  violando il vincolo della Vision. Scartato.
- **Mappatura/migrazione completa:** costo anticipato e conoscenza inferita senza
  necessità concreta. Scartata; crescita sul lavoro e legacy non classificato esplicito.

## Consequences

Una sola installazione fornisce metodi e motore; le copie distribuite sono controllate
dal manifest condiviso. Crescono istruzioni e manutenzione delle prove, misurate nel
rapporto di verifica. L1 non acquisisce burocrazia aggiuntiva.

MATCHED significa corrispondenza degli input dichiarati: non prova esecuzione,
verità, completezza delle dipendenze o riduzione dei costi fra sessioni. Restano
necessari ragionamento sul codice, review indipendente e valutazione sui casi.
Il workspace deve avere scrittori fidati: i controlli non costituiscono un confine
contro sostituzioni concorrenti ostili delle directory o identità falsificate.
