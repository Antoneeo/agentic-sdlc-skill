---
status: CURRENT
domain: code
topics: [card-continuity]
description: Continuità Eclosion: baseline RED e PASS del nucleo hanno scope diversi
date: 2026-10-04
derived_from: [corpus/given/source-8d2e82955248f265d8551c7a29c698984748f45d705a2c680597ed4e93cf2a59-516aebfbb5d32fc8883135d13c5c6739fa9a39f111ec1872c54ca4f6772dd2ee.txt, corpus/given/source-6d29099a0334b41c2532c017de7d2f8e41331d7a0957b650a2e66d57580cc0be-bcccab54641d42ddb6e7f68d5445cede3e928108e25cc756982d58de81ae668f.txt]
---
# Continuità della card Eclosion: modello utile alla ripresa
La proprietà cercata è conservare note accettate e fonte isolata attraverso la pausa della card, mantenendo identità originaria e autorizzazioni correnti. La baseline e il nucleo rivisto coprono stadi diversi di questa catena.
Nel percorso documentato il buffer viene popolato, il builder/adapter assemblano l'input SDK, slot_selector crea la riga pending associata alla Monade, _resume_agent salva ACK e prepara _bg_ai_response_task, poi il loop riparte.
La baseline riporta 30/30 note prima e 0/30 nella ripresa per Responses e Legacy; coda e fonte mancano. La fixture forza la Monade originaria per separare perdita della memoria e rischio di routing.
La review riporta PASS statico del nucleo servizio/adapter/finalizzazione e una suite autore di 370 PASS; i due laboratori reali card restano esclusi. Questi esiti coesistono con la baseline RED: non sono un conflitto e non dimostrano risolto il percorso utente.
La suite finale copre il producer reale a due richieste attraverso cifratura/claim/load, ma non tutta l'integrazione worker/produzione; precede inoltre il successivo guard seed/cattura nativa.
Proprietà da preservare nel nucleo: autorità iniziale completa, ordine causale input/richiesta/risultato, identità e associazione univoca, span realmente ammessi, frame stabili nelle riproiezioni, storia non rimessa in esecuzione e conservazione del passato.
Proprietà richieste alla continuità: snapshot dopo eventuali tool in coda, cifratura chat esistente, provenienza/accessi correnti e lifecycle. SensitiveJSON maschera ma non cifra: il report esclude resume_parameters/result_payload come deposito degli appunti; M139/SR16 resta invariato.
Restano aperti provenienza di tutti gli input, registrazione/freeze produttivo, worker/claim/load, legacy completa, routing/privacy, seed/cattura nativa e laboratori card. Autorizzazioni, revoche, reset, scadenza, concorrenza, effetti HTTP e consegna privata non sono provati dalla baseline.
Non inferire idempotenza HTTP da un solo tool osservato, scomparsa di ogni upload dalla fonte anonima, cambio effettivo di Monade dopo ARS dal routing preparato, né hit/costi provider dai prefissi simulati.
Le fonti sono report ricevuti; non sono disponibili runtime Eclosion, patch, harness o log citati. I loro risultati non sono stati rieseguiti qui. I bindings attestano soltanto i file dei report del fixture, non i sorgenti Eclosion sottostanti.
