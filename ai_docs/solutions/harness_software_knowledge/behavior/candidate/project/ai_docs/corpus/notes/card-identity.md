---
status: SUPERSEDED
domain: code
topics: [card-identity]
description: Identità originaria distinta dalla corrente e limiti del PASS locale
date: 2026-10-04
derived_from: [corpus/given/source-3829deb5c873085f6ca531677eb7477d7b0eed4e27fe88de72ec88d6c83b33ce-8829d8c0971044a078e0b8ccaeabd96555bae9a5e137b9ae7b63a1f9a6ec8e3a.txt, corpus/given/source-2fa49ba256129b7988272b97f272e6cc1a15a7930c46ebb5b7b102c1ab70ca13-34aed586813e7deca317b429aa10be22f03db52c4a3c523ac08255fc49c2999f.txt]
---
# Identità della card
La lettura di identity(card) mostra il ritorno di card["original_id"]; current_id non viene letto dal frammento.
Il risultato ricevuto riferisce che con original_id=A e current_id=B il valore restituito è A, con PASS locale.
Proprietà da preservare: la distinzione tra identità originaria e identità corrente, affinché un aggiornamento non sostituisca implicitamente l'ancora originaria; è l'invariante ricostruita del frammento.
Non sono fornite prove del clic end-to-end, dei chiamanti o del collegamento fra questo frammento e il routing Eclosion.
Il frammento non valida autorizzazioni o appartenenza: il risultato locale non dimostra accesso, consegna privata, revoche o persistenza attraverso pausa.
Una futura modifica deve riesaminare sia identity.py sia i consumatori che scelgono la card/Monade; questi consumatori non sono enumerabili dagli input disponibili.
Nessun test del software è stato eseguito in questa sessione; PASS è riportato dal materiale ricevuto.
