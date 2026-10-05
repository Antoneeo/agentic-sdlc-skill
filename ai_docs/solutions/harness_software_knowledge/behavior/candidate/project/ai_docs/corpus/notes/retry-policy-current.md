---
status: CURRENT
domain: code
topics: [retry-policy]
description: Retry corrente con budget uno e distinzione dalla fixture storica a tre
supersedes: retry-policy.md
date: 2026-10-04
derived_from: [corpus/given/source-044ddd6b2149f9d44b0b5591e16d212c2037dc93c30b2110244d065c2bf549ef-9d5e9aebbbd57baf864b1093a88aa710b4e1d6858dde95a32d7f494089f691b2.txt, corpus/given/source-11d417822122f262f9ab3af7b8b379337f13a6cc3d82af66dc541f09b4a3dbab-fe7f15122f4a5a7aaeb11c9bdd6716fd2d739551735631d3c2fae7b730a84932.txt, corpus/given/source-e3ceac7c82d50a3f6a5d26bbb6872d97daf0429cb9ef5c320dfd6dd201bdfeba-181d2eeeefc0a6400827d3c53a9f6742536a7d72719891ddc71308703f9ec260.txt]
---
# Retry corrente e prova condizionata
Il limite di attempt(operation, config) resta letto da config["attempts"], non fissato nel corpo della funzione.
Con il file corrente attempts=1 passato alla funzione, la lettura statica implica al massimo una chiamata: se il primo risultato è falso, ritorna False senza raggiungere il terzo risultato della vecchia fixture.
Il primo risultato truthy restituisce subito True; questa conclusione è statica, non una nuova esecuzione.
Esaurito il budget senza successo, attempt ritorna False; le eccezioni di operation non vengono intercettate.
Il corpo non introduce attese: nessun ritardo o backoff esplicito. Durata ed effetti interni di operation restano sconosciuti.
Preservare il limite configurato, l'arresto al primo successo e False all'esaurimento: invarianti ricostruite, non nuovo mandato di prodotto.
Il report invariato descrive una fixture con attempts=3 e falso/falso/vero, PASS alla terza chiamata; rimane prova documentata di quella configurazione storica, non della configurazione corrente a uno.
Codice, configurazione e risultato sono premesse distinte: il file retry.py è invariato, ma il vecchio binding config è CHANGED. La prova storica non viene promossa a prova corrente.
Mancano caricamento effettivo del JSON nei chiamanti, sorgente del test, log grezzo e servizi reali. Nessun test software viene rieseguito qui; la risposta sul runtime è condizionata al frammento e alla configurazione forniti.
