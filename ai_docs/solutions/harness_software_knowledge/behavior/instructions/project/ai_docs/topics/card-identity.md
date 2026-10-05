---
topic: card-identity
parents: []
related: card-continuity
synonyms: [identità, original_id, current_id]
domain: code
topics: [card-identity]
description: Identità originale della card nella funzione locale; non estendere il risultato al routing end-to-end.
status: CURRENT
---
# Identità della card — caso 4

Riverifica locale del 2026-10-04: il sorgente corrente è `project/inputs/card_identity.py`, mentre la cattura precedente si chiama `identity.py`. Il corpo riaperto e i byte coincidono: `identity(card)` restituisce `card["original_id"]`. Aggiornato il localizzatore corrente senza dedurre identità semantica dal solo nome del file. [Sorgente corrente, L1-L2](../../inputs/card_identity.py), [cattura corrente](../corpus/given/card_identity.py).

Proprietà ricostruita: un `current_id` diverso non deve sostituire l'identità originale in questa funzione. Il report storico [identity-test.txt](../corpus/given/identity-test.txt) osserva A su `{original_id: A, current_id: B}`: resta pertinente al corpo invariato, ma non è un test di import/chiamanti dopo lo spostamento. Non è fornito un nuovo report identity-test tra gli input correnti.

Il [probe della riverifica](../solutions/harness_four_cases/reverify.py) carica il **nuovo percorso** e osserva ancora A; l'asserzione errata B fallisce. [Risultato e digest](../solutions/harness_four_cases/reverify_result.json). La prova corrente copre questa funzione e questa fixture, non card senza original_id, altri tipi, click reali, routing, autorizzazioni, binding della continuazione o percorso HTTP. Chiamanti e import reali dopo il cambio di percorso restano **da riverificare**: il loro corpus non è fornito.

Relazione riusata con [card-continuity](card-continuity.md): l'identità locale non dimostra continuità della memoria o routing end-to-end. La baseline Eclosion forza appositamente la Monade originaria per isolare la perdita degli appunti. Ipotesi tuttora non provata: tutti i consumer usano questa funzione nella ripresa. La nuova milestone può riusare l'invariante locale condizionato, non dichiarare completo il click.

Una modifica alla funzione, allo schema card o ai chiamanti impone nuova verifica; rinominare il file richiede controllo degli import anche quando il corpo è invariato. Conserviamo la fonte e la prova storiche senza spacciare la loro immutabilità per esecuzione nel sistema vivo.

## Claims

| id | claim | valid | qty | about | source | prov | state |
|---|---|---|---|---|---|---|---|
| 85c3d0ebb6e6 | identity seleziona original_id dal mapping ricevuto. | if corpo della funzione fornito nella fixture | - | - | corpus/given/identity.py#L1-2 | GIVEN | OK |
| dedb589031d2 | Il test fornito osserva A con original_id A e current_id B. | if fixture locale, non click card end-to-end | - | - | corpus/given/identity-test.txt#L1-1 | GIVEN | OK |
| 428120e289ae | Nel sorgente corrente card_identity.py, identity seleziona original_id. | if corpo corrente riaperto nella riverifica; caller e import non disponibili | - | - | corpus/given/card_identity.py#L1-2 | GIVEN | OK |
