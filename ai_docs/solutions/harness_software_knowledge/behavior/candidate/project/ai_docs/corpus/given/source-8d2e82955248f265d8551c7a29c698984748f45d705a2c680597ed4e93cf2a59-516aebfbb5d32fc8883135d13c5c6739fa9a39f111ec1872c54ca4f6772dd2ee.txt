---
description: Baseline riproducibile della perdita di appunti e fonte alla ripresa da card, M145.A2 ancora aperta.
status: CURRENT
---

# Card: difetto riprodotto prima del fix

**2026-10-04 · M145.A2 PROGRESS.** Per l'implementatore: usare questa baseline per verificare il futuro fix della card. Non è un E-ISP/E-TDD e non autorizza modifiche runtime. Il TDD già approvato `technical_design_extracted_source_continuity` riguarda lo stesso loop; esclude espressamente la persistenza attraverso pausa. Quello di A1 riguarda integrità e capacità del buffer, non la ripresa.

## Prova e risultato

Il probe esegue i veri loop streaming, builder, adapter e assemblaggio SDK, con trasporto e risultato del tool simulati. `scratchpad_replace` scrive realmente 30 note sintetiche in un buffer di esattamente 20.000 caratteri; una fonte isolata viene fornita nel parametro del run. Il secondo input SDK contiene tutti gli ID, il marcatore finale e la fonte. Il tool produce una `slot_selector` riconosciuta dal registry reale; il probe verifica la riga pending nel database e la Monade associata.

Il vero `_resume_agent` persiste l'ACK e prepara la chiamata background, intercettata dalla fixture. I suoi argomenti sono legati alla firma reale di `_bg_ai_response_task`: target `all`, fonte None, isolamento False, timezone None, nessun parametro di continuazione. Il probe richiama poi il vero loop con questi valori e con la Monade originaria selezionata esplicitamente, per isolare la perdita di memoria dal problema distinto di routing.

| Protocollo | Note prima della card | Note nel primo input della ripresa | Coda buffer | Fonte isolata |
|---|---:|---:|---|---|
| Responses | 30/30 | 0/30 | Assente | Assente |
| Legacy | 30/30 | 0/30 | Assente | Assente |

**RED finale: 2 failure, 0 errori di setup, 0 pass, 71,84 s, 15 warning.** Entrambe le failure sono `Card continuation lost accepted notes/source: notes=0/30; tail=False; source=False`. Un solo tool di dominio è eseguito nella sequenza osservata; il risultato non certifica l'idempotenza delle azioni HTTP sulla card.

## Riproduzione e limiti

Transitori: `.workdir/agent-work-continuity/test_card_as_is_probe.py`, `run_card_probe.ps1`, `card-probe-red.log`, `card-probe-red.xml`. Eseguire il launcher con `-Phase red` in PowerShell. Usa container effimero, checkout corrente, chat_db_test obbligatorio e fixture locali; nessun provider live, PDF o modifica del runtime. Il probe è fuori dalla suite mergeabile. I primi tentativi avevano errori nelle fixture (caricamento di conftest e contesto SQL separato); non costituiscono evidenza del difetto. La baseline finale li risolve.

La guardia membership è simulata: questa prova non verifica autorizzazioni, revoche, reset, scadenza, card concorrenti, effetti HTTP o consegna privata. La fonte anonima isola la perdita del parametro; non prova che qualsiasi upload normale scompaia dallo storico. Il cambio di Monade è un rischio verificato nel routing preparato, non un cambio effettivamente osservato dopo ARS.

Prima del fix servono E-ISP/E-TDD della continuazione da card e review indipendente. Il design deve trattare identità originaria, snapshot aggiornato dopo gli eventuali tool in coda, cifratura, provenienza/accessi correnti e lifecycle. `SensitiveJSON` maschera la visualizzazione ma non cifra il payload: non usare resume_parameters/result_payload come deposito degli appunti. Il nuovo contenuto privato deve usare il dominio di cifratura chat già esistente. M139/SR16 resta invariato.
