---
status: SUPERSEDED
domain: code
topics: [retry-policy]
description: Tentativi dipendenti dalla configurazione; comportamento locale e limiti
date: 2026-10-04
derived_from: [corpus/given/source-044ddd6b2149f9d44b0b5591e16d212c2037dc93c30b2110244d065c2bf549ef-9d5e9aebbbd57baf864b1093a88aa710b4e1d6858dde95a32d7f494089f691b2.txt, corpus/given/source-898a80b765d5d2169c8f5db93fca941627b94be4e681307302345dd05294e5e1-fbba7af07ce1b2ad333491ea024532cb72f90121bb4ea19dae074971e65ade9b.txt, corpus/given/source-e3ceac7c82d50a3f6a5d26bbb6872d97daf0429cb9ef5c320dfd6dd201bdfeba-181d2eeeefc0a6400827d3c53a9f6742536a7d72719891ddc71308703f9ec260.txt]
---
# Tentativi: codice, configurazione e risultato sono premesse congiunte
La lettura di inputs/retry.py mostra un limite preso da config["attempts"], non un numero fisso nel codice.
Con la configurazione catturata attempts=3 e la sequenza falsa, falsa, vera del risultato fornito, la funzione raggiunge il successo alla terza chiamata; il risultato riporta PASS locale.
Il ritorno immediato True evita tentativi successivi dopo un valore truthy di operation(). Questa è interpretazione statica, non una nuova esecuzione.
Esaurito range(config["attempts"]) senza successo, il codice ritorna False; il caso tutto falso non ha un risultato eseguito fornito.
Il corpo non introduce attese né intercetta eccezioni; durata ed effetti interni di operation() non sono definiti qui.
Proprietà da preservare: limite configurato, arresto al primo successo, False all'esaurimento. Sono invarianti ricostruite del frammento, non un nuovo mandato di prodotto.
Mancano sorgente del test, log grezzo, invocazione reale che carica retry-config.json, chiamanti, servizi esterni e prove dei rami limite.
Qualunque cambio di retry-config.json richiede riverifica della conclusione sul terzo tentativo anche se retry.py resta identico.
Nessun test del software è stato eseguito in questa sessione; PASS è riportato dal materiale ricevuto.
