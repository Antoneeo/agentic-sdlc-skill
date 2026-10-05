---
status: CURRENT
domain: code
topics: [card-identity]
description: Identità originaria nel percorso corrente card_identity.py; prova di click assente
supersedes: card-identity.md
date: 2026-10-04
derived_from: [corpus/given/source-3829deb5c873085f6ca531677eb7477d7b0eed4e27fe88de72ec88d6c83b33ce-cb83cfbaa903fddfd70b2fdea88da1a53792e0b87fb90965bbdedddfce62cb6c.txt]
---
# Identità nel sorgente corrente
La lettura statica di inputs/card_identity.py:identity(card) restituisce card["original_id"]; current_id non è letto.
Per la card con original_id=A e current_id=B il frammento corrente implica A, per lettura statica, non per un nuovo test eseguito.
Preservare la distinzione tra identità originaria e corrente: l'ancora originaria non deve essere sostituita implicitamente durante un aggiornamento.
Il frammento non valida autorizzazioni o appartenenza, né dimostra persistenza attraverso pausa, routing, consegna privata o clic end-to-end.
Il collegamento del frammento con la Monade Eclosion e i consumatori reali non sono disponibili: resta una proprietà locale.
