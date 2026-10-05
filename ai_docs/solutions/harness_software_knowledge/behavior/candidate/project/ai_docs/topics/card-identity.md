---
topic: card-identity
description: Selezione identità originaria rispetto a quella corrente
parents: [software-properties]
owns: [card-identity/properties]
synonyms: [identità, original_id, current_id, card]
gaps:
  - Percorso del clic, consumatori e autorizzazioni non forniti.
  - Non dimostrato collegamento runtime con la Monade Eclosion.
  - inputs/identity.py e inputs/identity-test.txt non sono disponibili; le catture storiche restano leggibili.
  - La corrispondenza byte del sorgente rinominato non ripristina la prova eseguita mancante.
claim_schema: 2
status: CURRENT
---
# Selezione identità originaria rispetto a quella corrente

## Claims

| id | claim | valid | qty | about | source | prov | state | kind |
|---|---|---|---|---|---|---|---|---|
| ca323e332851 | La lettura statica identifica original_id come valore restituito; current_id non è letto. | if versione catturata il 2026-10-04 | - | - | corpus/notes/card-identity.md#L10-10 | DERIVED | SUPERSEDED 521033cfbca5 | OBSERVATION |
| 530a1405d7a5 | La fixture con original_id=A e current_id=B riferisce ritorno A. | if versione catturata il 2026-10-04 | - | - | corpus/given/source-2fa49ba256129b7988272b97f272e6cc1a15a7930c46ebb5b7b102c1ab70ca13-34aed586813e7deca317b429aa10be22f03db52c4a3c523ac08255fc49c2999f.txt#p=1@0-60 | GIVEN | OK | OBSERVATION |
| 5488954c2729 | Il PASS dell’identità è locale e non copre un clic end-to-end. | if versione catturata il 2026-10-04 | - | - | corpus/given/source-2fa49ba256129b7988272b97f272e6cc1a15a7930c46ebb5b7b102c1ab70ca13-34aed586813e7deca317b429aa10be22f03db52c4a3c523ac08255fc49c2999f.txt#p=1@61-102 | GIVEN | OK | OBSERVATION |
| a6f03a3c8e5b | Preservare la distinzione tra identità originaria e corrente. | if versione catturata il 2026-10-04 | - | supports -> card-continuity | corpus/notes/card-identity.md#L12-12 | DERIVED | SUPERSEDED c5540b6ae4f2 | REQUIREMENT |

| 521033cfbca5 | Il sorgente corrente inputs/card_identity.py restituisce original_id e non legge current_id. | if input correnti verificati il 2026-10-04 | - | - | corpus/notes/card-identity-current.md#L11-11 | DERIVED | OK | OBSERVATION |
| c5540b6ae4f2 | Preservare la distinzione tra identità originaria e corrente. | if input correnti verificati il 2026-10-04 | - | supports -> card-continuity | corpus/notes/card-identity-current.md#L13-13 | DERIVED | OK | REQUIREMENT |
| 80b51449ebd8 | A/B implica A per lettura del sorgente corrente; non è un nuovo risultato eseguito. | if input correnti verificati il 2026-10-04 | - | - | corpus/notes/card-identity-current.md#L12-12 | DERIVED | OK | OBSERVATION |

## Responsabilità e riverifica

`inputs/card_identity.py:identity(card)` seleziona original_id. Il digest completo 3829deb5c873085f6ca531677eb7477d7b0eed4e27fe88de72ec88d6c83b33ce coincide con la cattura precedente di inputs/identity.py: stessa implementazione, nuovo binding esplicito; il vecchio path resta assente (UNAVAILABLE nella verifica iniziale; ora fonte storica superseded nel report). Anche inputs/identity-test.txt manca: 530a1405d7a5 e 5488954c2729 rimangono risultati storici archiviati, non prove fresche del nuovo percorso. Leggere corpus/notes/card-identity-current.md. Distinto da card-continuity: selezione locale non prova persistenza, privacy o routing.
