# Design della revisione 4.0-content

Stato: proposta di revisione richiesta da Antonio il 2026-10-04; produzione dopo review indipendente.
Autorità: VISION_course_agentic-sdlc-kb-agentic.md APPROVED, ANALYSIS C-001 e REPORT_indicazioni_revisione_2026-10-04.md. La Vision non viene emendata: confronto e accumulo sono già benefici espliciti; distill è spiegato come supporto alla comunicazione, non come terzo corso completo. Il pubblico rimane P1 e le prove valutano atti della persona, non operazioni dell'agente.

## Problema e risultato richiesto

Il Course Value privilegia il giudizio su risposte, mentre il lettore deve prima poter motivare l'adozione. Il timeout permette di ricordare facilmente tutta la storia; il rischio di cancellare un vincolo precedente rimane poco evidente. Il valore temporale arriva tardi. I timori di regressione, costo, rigidità e conoscenza obsoleta devono trovare risposte verificabili e limiti. Il nuovo percorso parte dal lavoro ordinario e segue un software che cambia: mostra il valore, poi i meccanismi, poi la decisione sul loro uso.

## Caso e confronto

Orione diventa un software fittizio che inoltra ordini a un fornitore. Tutti i fatti, i numeri e gli esiti del caso sono narrativi, non evidenza empirica. La storia introduce quattro eventi: blocco del doppio clic; conferma persa anche quando l'ordine è creato; chiave stabile per i ritentativi dello stesso ordine; separazione delle notifiche dall'invio al fornitore. Il fornitore riconosce la chiave: stesso ordine con stessa chiave restituisce l'esito precedente; una chiave nuova è un nuovo ordine. Orione deve mantenere la chiave su ogni ritentativo. Un nuovo baco impedisce il ritentativo quando la conferma è incerta. La proposta sbagliata rimuove il blocco e crea una chiave nuova a ogni invio: sblocca il gesto ma può creare un secondo ordine. Togliere solo il blocco UI mantenendo la chiave non basta a causare la duplicazione. La soluzione coerente conserva la chiave e distingue stato incerto da fallimento certo, verificando conferma e notifica separatamente.

Nessuna conoscenza di protocolli è presunta: chiave, ritentativo, stato incerto e superfici vengono spiegati prima dell'uso. Il caso mostra che la storia informa l'indagine, non che una decisione vecchia sia sempre giusta. Il confronto dà identici fatti e fonti alla disciplina delle skill e a note curate equivalenti: cambia l'esplicitazione di consultazione, provenienza, aggiornamento e verifiche, non l'intelligenza dell'agente. Note mantenute possono ottenere gli stessi risultati.

## Percorso e verifiche

| Modulo | Obiettivo della persona | Spiegazione | Evidenza e risposta insufficiente |
|---|---|---|---|
| M1/O1 | Motivare quando adottare le skill | Difetti di chat e appunti; evoluzione Orione; patrimonio e contesto distinti; skill come istruzioni | S07 richiesta su un fix proposto: respingere il sintomo come prova, chiedere ragioni/protezioni e spiegare quale ricostruzione evitano tracce consultate. Insufficiente: più documenti quindi più sicurezza. S08 soluzione; S40–41 coprono cumulativamente O1 con scelta e alternativa sufficiente. |
| M2/O2 | Giudicare una risposta con fonti | Acquisizione, claim, ambito, argomenti e recupero pertinente | S12 risposta del tool su nuovi ordini: chiedere fonte/ambito prima del riuso. Non estrarre claim manualmente. S13 soluzione. |
| M3/O3 | Contestare il riuso di conoscenza incompatibile | Storia vs validità; fonti contestate; fatto nuovo vs preferenza; aggiornamento dei derivati | S17 risposta che sceglie per recenza: contestarla e chiedere chiarimento del servizio cui si riferisce. S18 soluzione. |
| M4/O4 | Giudicare livello, beneficio e confini | Costi proporzionati; Vision; decisioni della persona | S21 agente dichiara L2 per una riga che altera retry e duplicazione: contestare motivando l'effetto e rifiutare ampliamenti non richiesti. S22 soluzione. |
| M5/O5 | Giudicare indagine, soluzione e chiusura | Log disponibili, ipotesi; attori, comportamento, flussi e rischi; riuso; design e review; prove e correzione pulita | S29 proposta di chiusura con solo test sul pulsante: chiedere evidenze su invio, stato incerto, duplicazione e notifica; non scrivere il design. S30 soluzione. |
| M6/O6 | Collaborare con l'agente e preparare la ripresa | Responsabilità kb/SDLC/distill; folder; contesto selezionato; risultato concreto e handoff prima della compattazione; Standalone completo | S35 agente propone compattazione con scelta ancora solo in chat: chiedere salvataggio verificabile e prossimo passo prima di procedere. S36 soluzione. |
| M7/O7 | Scegliere adozione e manutenzione su un caso nuovo | Settimana/mese/anni; costo e limiti; confronto equo e alternativa sufficiente | S40 due progetti diversi, agente propone lettura totale e livelli uniformi: formulare correzione proporzionata e motivare scelta, senza rendimenti garantiti. S41 soluzione; S42 applicazione facoltativa UC5/IC4 sul proprio documento in sola lettura: richiesta di risposta con fonte e modifica solo ipotizzata, criteri per giudicarle, esempio fittizio alternativo e chiusura. |

## Impatto e capacità

Capacità esistenti: schema slide-content-v1, validator distributions/course-creator/skills/course-creator/scripts/course_check.py, grafo didattico e reader/reviewer indipendenti. simulation_3_1/packet/ conserva precedenti packet; nessun builder riusabile è certificato. I nuovi packet saranno derivati dal sorgente canonico con estrazione ispezionata. Nessun nuovo runtime o metodo della skill viene implementato.

| File | Cambiamento e ragione |
|---|---|
| ANALYSIS_course_agentic-sdlc-kb-agentic.md | Aggiornare obiettivo, UC/IC canonici, rischi, impatto, piano e diario per la revisione; archiviare i byte precedenti. |
| COURSE_PLAN.md | Aggiornare O1–O7, sequenza, alignment, locatori e valore; versione 4.0-content. |
| SLIDE_CONTENT.md | Riscrivere 42 unità complete con ragionamento visibile, fonti e soluzioni; fonte primaria. |
| D-UC.md, D-IC.md, P-TM.md | Dettagli dei medesimi UC1–UC5/IC1 e rischi C-001: nessun nuovo pubblico o canale. |
| CONCEPT_GRAPH.md | Aggiornare dipendenze e traccia spiegazione/primo uso per gli stessi concetti; aggiungere continuità dopo compattazione. |
| sources.md, source_snapshot_2026-10-04.zip | Congelare fonti riaperte delle skill stabili attuali, Vision e distill; dichiarare il caso inventato e il consiglio dell'autore. |
| modules/M1.md–M7.md | Sostituire testi obsoleti con puntatori alla fonte primaria, senza seconda versione concorrente. |
| SIMULATION_REPORT.md e simulation_4_0/ | Conservare prompt, packet versionati, due tentativi e controllo, limiti di isolamento. |
| FEEDBACK_REPORT.md | Tracciare indicazioni dell'autore e correzioni, senza dichiarare apprendimento umano. |
| history_3_2/ | Conservare versione precedente e artefatti relativi senza sovrascrivere storia precedente. |
| revise_4_0.py, align_4_0.py | Record riproducibili della produzione locale: contenuto esplicito e allineamento dei documenti; nessuna modifica al runtime della skill. |
| DIAGNOSIS_metodo_2026-10-04.md | Distinguere difetti del corso da lacune dimostrate del metodo, prima di proporre guide o cambiamenti della skill. |
| audit/HANDOFF_course_agentic_sdlc_kb_agentic.md, reviews/REVIEW_LOG.md | Stato riprendibile e evidenze dei gate. |
| INDEX.md, memory/INDEX.md, audit/handoff.md, audit/audit_plan.md | Rigenerazione e riferimento di freshness dopo il solo lavoro verificato. |

Report delle indicazioni e Vision approvata restano invariati. PPTX precedente resta storico; nessun rendering richiesto in questa fase.

## Rischi, mitigazioni e limiti

C-1 fedeltà: reopen e snapshot; ogni unità cita il registro di fonti. Nessuna fonte narrativa spacciata per osservazione.
C-2 sovraccarico: spiegare progressivamente pochi vincoli della storia, senza chiedere di memorizzare cronologie o nomi di artefatti.
C-3 spiegazione mancante/catalogo: ragionamento visibile prima delle sigle, prove che richiedono una ragione causale e non solo nomi.
C-4 confronto sleale: medesime informazioni, note curate come alternativa legittima, nessuna garanzia di risparmio o obbedienza.
C-5 simulazione contaminata/falso successo: sessioni separate, accesso simmetrico dichiarato, efficacia non verificata; review, struttura e simulazione sono evidenze distinte.
C-6 governance opzionale: spiegare Standalone completo e aggiunta eventuale di devPNT senza invocarlo; nessun requisito esterno.
C-7 feedback assente: D-IC conserva not available e percorso di correzione, nessun servizio inventato.
C-8 ruolo sbagliato: ogni prova parte da un'uscita dell'agente o da una richiesta umana; nessun punteggio per artefatti prodotti al posto del tool.
C-9 perdita da compattazione: consiglio condizionato al salvataggio e controllo dello stato; contesto piccolo non presentato come legge universale.
C-10 manutenzione: distinguere ragione storica da validità attuale, fonti superate e derivati da rivedere.

## Verifiche e sequenza

Pre-audit locatori e source hash; review indipendente del design. Produzione canonica e allineamento. Gate strutturale. Diagnostic reader P1 con reveal progressivo e due compiti nuovi congelati; controllo senza corso con pari materiale/task/accesso. Reviewer distinto con criteri congelati, soluzioni, risposte e fonti. Correggere eventuali blocker e retest del prefisso coinvolto. Rigenerare indici e gate repository; nessuna dichiarazione di efficacia umana. Le restrizioni dei reader basate su istruzioni vengono dichiarate, non spacciate per isolamento tecnico.
