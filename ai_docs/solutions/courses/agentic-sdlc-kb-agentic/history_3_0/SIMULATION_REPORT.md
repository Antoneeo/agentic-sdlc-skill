# Diagnostica del corso 3.0-content

Status: inconclusive
Course version/hash: 3.0-content / SHA-256 `1e1f6f23c54f2882bf50219926951a5346baf7c49129d3bdca5730a75dd61bb0`
Author/coordinator: /root, autore e unico integratore dei materiali canonici.
Didactic reviewer: /root/course3_review, fresh context, gpt-6-sol xhigh.
Profile and objective: P1, percorso comune del team software, O1–O7.
Efficacy: efficacy not verified

## Che cosa è stato verificato

Il sorgente completo è stato riesaminato indipendentemente contro Vision, profilo, piano, grafo e fonti. La prima review ha rilevato due BLOCK sull’indipendenza/fallback delle review e un WARN sul ritorno temporale all’acquisizione del manuale. Il testo è stato corretto e la seconda review circoscritta ha verificato quei passaggi. La diagnostica di lettura e il controllo senza corso sono giudicati nel record indipendente riportato sotto; un esito favorevole del contenuto non prova efficacia umana o superiorità causale della skill.

## Materiale e accesso

Archivio riapribile: `simulation_3_0/evidence.zip`, SHA-256 `a7e309d5214a3165b52291af0363c663f6804f654d3563a7e77a72ee0577cc54`. Contiene prompt, risposte, manifest per unità, materiale visibile v1/v2, compito finale, criteri congelati, report e review. I dodici hash dello snapshot fattuale sono verificati in source-check.json. Il sorgente storico e il precedente report 2.1 restano in history_2_1; non certificano la revisione attuale.

Il lettore principale ha ricevuto S01–S34 da v1 e S35–S52 da v2. Solo S13, S35, S37, S39 e S51 cambiano fra i due pacchetti; S35 e seguenti sono stati corretti prima della loro prima esposizione. Il prefisso S01–S13 v2 è stato riletto in una sessione fresca, dopo la correzione di S13. Non è quindi una singola lettura completa di 52 unità della versione finale: il report conserva la composizione e non riscrive retroattivamente i risultati.

Il pacchetto finale v3 corregge soltanto spazi in «A 35» e «luglio, 35»: il contenuto visibile cambia per questo motivo in S30 e S36, senza cambiare fatti, spiegazioni o prove. V1, v2 e le risposte originali restano conservati; il controllo locale e la review distinguono questa correzione tipografica dalle revisioni semantiche.

Il conductor ha consegnato una unità per turno e conservato ogni risposta prima della successiva. Le soluzioni didattiche sono state mostrate solo dopo il tentativo della domanda corrispondente; non sono la chiave del compito finale, diverso e tenuto separato. Il lettore ha quindi ricevuto anche feedback didattico e domande di riflessione: sono condizioni della prova, non apprendimento spontaneo dimostrato. Questa realizzazione usa l’intero percorso self-study, comprese le soluzioni dopo il tentativo; differisce dalla lettura letterale del pacchetto ridotto senza soluzioni in simulation.md e non va presentata come un esperimento controllato puro.

Il controllo /root/course3_control_final ha letto soltanto transfer-task.md, con lo stesso profilo, compito finale e divieto di fonti esterne. Il compito esplicita che non esiste una durata corretta nascosta. Un tentativo preliminare /root/course3_control con formulazione ambigua su «navigazione» è escluso: il testo finale chiarisce «menu di navigazione dell’applicazione» prima della nuova sessione di controllo e del tentativo finale del lettore. I risultati del controllo sono in control-final.md.

L’isolamento è imposto tramite istruzioni, non sandbox tecnico. Il conductor e il reviewer possono vedere più materiale, ma non svolgono il ruolo del lettore. Il nuovo lettore del prefisso non riceve risposte dell’altro. La simulazione P1 non misura differenze fra sviluppatori e responsabili reali né la ritenzione a distanza.

## Resoconto del conductor

# Registro della lettura sequenziale — Course 3

Per il revisore: usare questo registro per individuare le esposizioni effettive e le risposte originali. Il registro descrive conduzione, conteggi e difficoltà dichiarate; non assegna un esito didattico. I testi completi sono nei registri indicati.

## Esposizioni completate

| Stream | Lettore | Esposizione | Risposte conservate |
|---|---|---|---|
| Principale | `/root/course3_reading_conductor/reader` | S01–S34 packet-v1; S35–S52 packet-v2; poi transfer-task | 52 risposte alle unità e 1 risposta finale |
| Prefisso corretto | `/root/course3_reader_fresh_prefix` | S01–S13 packet-v2 | 4 risposte conservate dal root e 9 dal conductor |

Il principale è uno stream misto, non una lettura integrale della versione finale. S13 è stata letta in v1 dal principale e in v2 dal lettore separato del prefisso. Il principale non ha ricevuto S35–S52 in v1. I prompt v1 preparati ma non consegnati sono conservati in `reader-v1/undelivered-v1-prompts/`. Le successive correzioni editoriali v3 non sono state esposte da questo conductor.

Nel principale ogni risposta è stata letta e salvata prima della consegna successiva, sempre allo stesso lettore. Gli otto tentativi S11, S17, S23, S27, S38, S42, S47 e S50 precedono le rispettive soluzioni S12, S18, S24, S28, S39, S43, S48 e S51. Il compito finale è stato consegnato dopo la risposta a S52, senza criteri di valutazione o soluzioni aggiunte. Il prefisso separato include il tentativo S11 prima della soluzione S12 e termina dopo S13.

## Registri e isolamento

- `reader-v1/S01-prompt.txt` … `S52-prompt.txt` e corrispondenti `Sxx-response.txt`: testo consegnato e risposta di ogni unità principale.
- `reader-v1/exposure-manifest.json`: versione e SHA-256 del packet, del prompt e della risposta per ciascuna unità principale.
- `reader-v1/final-task-prompt.txt` e `reader-v1/final-task-response.md`: consegna finale e risposta separata.
- `fresh-prefix.md`: registro root delle prime quattro unità del lettore separato.
- `fresh-prefix-rest/S05-prompt.txt` … `S13-prompt.txt` e corrispondenti risposte: prosecuzione del prefisso effettuata dal conductor.
- `reader-v1/run-notes.txt`: ID, variazioni del protocollo e note di trasporto.

Il principale è stato creato con `fork_turns: none` e profilo P1: membro di un team software che usa agenti, conoscenza delle due skill non stabilita. Non ha ricevuto percorsi ai file, contenuti futuri, criteri o annotazioni dell’autore. L’isolamento era solo istruttivo: strumenti e file non erano tecnicamente disabilitati. Non sono state osservate chiamate a strumenti nel suo stream.

Il lettore separato era già stato creato dal root senza storia ereditata. Il registro delle prime quattro unità autorizza la lettura di un file packet per turno: questa modalità differisce dalla consegna inline del principale. Dal trasferimento al conductor, S05–S13 sono state consegnate inline; le risposte sono state inoltrate verbatim dal root perché le notifiche tornavano al parent originale. Nessun contenuto dei due lettori è stato passato all’altro.

## Difficoltà dichiarate e variazioni operative

Le risposte complete mantengono anche i riferimenti che il lettore non poteva ancora seguire, senza correggerli retroattivamente. Tra i punti dichiarati nel principale: termine skill in S03; modalità concreta di registrazione e limiti di lettura in S13; «risposta con provenienza» in S15; limiti L2 e significato operativo di review/chiusura in S26; percorso previsto per creare una GUIDE in S37. Queste sono osservazioni del lettore, senza valutazione del conductor.

Il principale segnala inoltre «A35» in S30 e «luglio,35» in S36. Il lettore separato, dopo S13 v2, dichiara non ancora mostrato come mantenere il collegamento preciso tra testo estratto e pagina dell’originale. Le segnalazioni sono state conservate e la lettura è proseguita senza suggerimenti di riparazione.

I prompt normalizzano CRLF in LF e separano il testo dell’unità dalla domanda neutra con due ritorni a capo. Un primo comando di registrazione ha incontrato un errore di parsing PowerShell; è stato ripetuto prima della successiva consegna, senza alterare il contenuto ricevuto dal lettore. Nessun file canonico del corso è stato modificato dal conductor. Il conteggio su disco conferma 52 risposte principali alle unità, una risposta finale e 9 risposte aggiunte al registro del prefisso.


## Giudizio indipendente sulle evidenze

# Giudizio indipendente sulle evidenze didattiche — 3.0-content

**Verdetto: PASS per la prontezza semantica del contenuto, con confronto di efficacia INCONCLUDENTE.** Ho letto `criteria.md` e `transfer-task.md` congelati, tutte le 52 risposte progressive e il tentativo finale in `reader-v1/`, le 13 risposte del prefisso fresco (`fresh-prefix.md` e `fresh-prefix-rest/`), `control-final.md`, `reading-report.md`, i manifest e le sezioni canoniche richiamate dalle difficoltà. Non riapro i finding chiusi nel riesame di contenuto round 2. I punteggi descrivono due risposte di agenti, non persone o ritenzione.

## Punteggi sui criteri congelati

Scala: 0 assente/errato; 1 parziale; 2 esplicito e motivato. Il compito finale è identico nei due tentativi (`transfer-task.md` e `reader-v1/final-task-prompt.txt`).

| Criterio | Lettore | Controllo | Base del giudizio |
|---|---:|---:|---|
| 1 O1, cartella vs memoria automatica e recupero | 1 | 1 | Entrambi riaprono nota, fonte e motivo (`reader-v1/final-task-response.md:1,17`; `control-final.md:3,17-19`), ma nessuno esplicita il contrasto con una memoria automatica della chat. Il task non lo sollecita direttamente. |
| 2 O2, fonte→affermazione rintracciabile | 2 | 2 | Il lettore registra due claim contestati con versione, ambito, decorrenza e passaggi (`reader-v1/final-task-response.md:7`). Il controllo conserva i due documenti, passaggi, versioni, ambito, contrasto e collegamenti alle decisioni (`control-final.md:5,17`): manca il nome «claim», ma non la funzione. |
| 3 O3, conflitto irrisolto e nuova informazione | 2 | 2 | Entrambi rifiutano la recenza come risoluzione, cercano chiarimento fondato e tengono distinta una mitigazione da un fatto del fornitore (`reader-v1/final-task-response.md:3,7`; `control-final.md:5,7,11`). Nessuno elegge 15 come regola certa. |
| 4 O4, beneficio, confini e triage | 2 | 1 | Il lettore motiva L3, indagine circoscritta, beneficio, decisione al confine e menu fuori ambito (`reader-v1/final-task-response.md:9`). Il controllo tratta beneficio, confine e menu con giudizio, ma non classifica la modifica significativa né esplicita il triage (`control-final.md:9,11,13`). |
| 5 O5, capacità/design e due review indipendenti | 2 | 1 | Il lettore cerca calcolo e consumatori, usa Standalone, colloca revisore distinto prima del codice e dopo le prove, e non retrodata la review saltata (`reader-v1/final-task-response.md:11,13`). Il controllo ricerca i percorsi e propone design e prove, ma omette entrambe le review indipendenti (`control-final.md:9,13-15`). |
| 6 O5, prove/regressioni, stato delle evidenze e GUIDE | 2 | 1 | Il lettore osserva lista ed email a tre tempi con errori e regressioni, dichiara non eseguite le prove e motiva la GUIDE con un'indagine riusabile (`reader-v1/final-task-response.md:13,17`). Il controllo specifica prove e registrazione dei risultati, ma non distingue quando valga creare una guida operativa (`control-final.md:13,17`). |
| 7 O6, responsabilità e Standalone | 2 | 2 | Entrambi separano fatto del fornitore, scelta del responsabile e realizzazione software; il lettore colloca l'ANALYSIS in Standalone (`reader-v1/final-task-response.md:7,11,15`), il controllo spiega che l'assenza di devPNT non blocca cartella e processo (`control-final.md:5,11,19`). Nessuno attribuisce approvazione automatica a un agente. |
| 8 O7, alternativa equa e manutenzione nel tempo | 2 | 2 | Entrambi accettano le note curate per Alba, ammettono istruzioni equivalenti e richiedono riapertura e manutenzione delle fonti per il futuro, senza vantaggio garantito (`reader-v1/final-task-response.md:1,15,17`; `control-final.md:3,17,19`). |
| **Totale descrittivo** | **15/16** | **12/16** | La differenza osservata si concentra su triage, review e criterio GUIDE; non è una stima d'effetto del corso. |

## Lettura progressiva e nuovi rilievi

**Nessun nuovo BLOCK di progressione.** Il lettore principale formula e corregge le otto prove prima delle rispettive soluzioni (`reading-report.md`, «Esposizioni completate»); S38 e S42 mostrano già review indipendenti e responsabilità distinte prima delle soluzioni (`reader-v1/S38-response.txt:1-4`, `S42-response.txt:1-4`). Le risposte S01–S34 e S35–S52 mantengono il filo causale previsto dal grafo. Il prefisso fresco v2 S01–S13 riproduce la comprensione della ragione storica, della nota, della skill, della cartella e del recupero; S11 viene tentata prima di S12.

Le domande esplicite non sono prerequisiti mancanti per i compiti loro successivi. In S03 «skill» è la domanda che S04 definisce. In S15 il lettore anticipa il senso di «risposta con provenienza» e S16 lo mostra prima della prova S17 (`reader-v1/S15-response.txt:3`, `SLIDE_CONTENT.md:512-552`). In S26 il limite esatto di L2 e la meccanica di review/chiusura restano da precisare, ma l'esempio L3 è motivato e S35–37 spiegano review e chiusura prima di S38 (`reader-v1/S26-response.txt:3`). In S37 il percorso operativo per creare una GUIDE non è insegnato; il lettore ne spiega comunque scopo e provenienza e S38 chiede **quando** sia giustificata, non come scriverla (`reader-v1/S37-response.txt:2-3`; `SLIDE_CONTENT.md:1277-1283,1313-1320`). Nel prefisso fresco, S13 non specifica il meccanismo di mappatura dell'estrazione PDF alla pagina originale; S14 insegna poi il locatore necessario al claim, e il corso non promette una procedura di estrazione (`fresh-prefix-rest/S13-response.txt:1-3`; `SLIDE_CONTENT.md:442-485`). Questi sono confini dichiarabili della spiegazione, non errori che impediscano l'uso insegnato.

## Validità del confronto e stato del resoconto

Il lettore principale ha visto S01–34 v1 e S35–52 v2; S13 v2 è stata rilet­ta da un altro lettore fresco fino a S13. I manifest confermano differenze v1→v2 solo in S13/S35/S37/S39/S51 e v2→v3 solo negli spazi visibili di S30/S36. Non esiste una singola lettura integrale della versione finale. L'isolamento è per istruzioni, non tecnico; la risposta del conductor non segnala uso di strumenti, ma non si può trasformare questo in prova di sandbox. Le domande neutrali a ogni unità e le soluzioni mostrate dopo il tentativo costituiscono supporto didattico. La comparazione ha quindi usato l'intero self-study, mentre `simulation.md` prescrive un pacchetto finale senza soluzioni: la prova è utile per localizzare lacune ma non soddisfa quel controllo puro. Il controllo preliminare con navigazione ambigua è escluso; il controllo qui valutato e il lettore finale hanno ricevuto la stessa formulazione chiarita.

Il compito finale riprende i nomi Alba/Bora e la struttura della prova S50, pur cambiando dominio, numeri e superfici. Misura un'applicazione vicina, non un trasferimento lontano. Il controllo senza corso è già competente e offre anche cautele non insegnate esplicitamente, come la distinzione fra finestra attesa e garanzia del fornitore (`control-final.md:7`). La differenza 15/16 contro 12/16 non dimostra causalità, superiorità generale o apprendimento umano. Sostiene soltanto che, in queste condizioni, il testo e la sequenza hanno reso possibili le risposte richieste senza una lacuna bloccante osservata.

Ho letto `finalize.py`: il resoconto proposto dice espressamente che lo stream è misto, che il prefisso è stato riletto separatamente, che le soluzioni erano visibili dopo il tentativo e che efficacia umana e superiorità causale non sono verificate. `Status: inconclusive` è coerente con queste evidenze. La frase sull'utilità concreta dei controlli riguarda i due BLOCK effettivamente rilevati in questa produzione e non promette un run finale unico o un beneficio misurato. Il resoconto deve mantenere questa qualificazione quando viene generato.


## Field test di course-creator: che cosa consente di concludere

Il metodo aggiornato ha guidato questo autore a fissare criteri prima delle domande, riscrivere il percorso in ordine di scoperta, legare grafo a spiegazione/primo uso e separare autore, lettore, controllo e reviewer. La review ha trovato omissioni effettive nelle regole di review; i record FAIL restano conservati insieme alle correzioni. Questo dimostra l’utilità concreta di quei controlli in questa esecuzione, non che le istruzioni impediscano ogni errore o che il solo uso della skill abbia causato un miglioramento generale.

I due difetti bloccanti erano nel contenuto prodotto: le fonti della skill includevano già le regole mancanti. La cronologia del manuale richiedeva invece un raccordo narrativo. Il corso è stato corretto; nessuna modifica ulteriore a course-creator è stata effettuata o giustificata automaticamente da questi casi. Il precedente materiale 2.1 non costituisce una produzione di controllo equivalente per questo 3.0.

La distinzione fra protocolli didattici è un limite emerso: la lettura progressiva dell’intero percorso mostra le soluzioni dopo i tentativi, mentre il pacchetto della comparazione descritto dalla skill le esclude. Qui si conserva la scelta effettiva e si limita la conclusione; non si altera la skill durante la produzione del corso.

## Stato della consegna

Testo completo e sua vista per l’allievo sono le consegne. Nessun nuovo PPTX, installazione o release. La definizione finale con il proprietario precede il rendering. La chiusura globale del repository resta separata: non si marca l’intero progetto CLEAN sulla base del controllo di questo corso.
