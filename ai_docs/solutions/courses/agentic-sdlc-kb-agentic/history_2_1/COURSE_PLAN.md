# Piano del corso: kb-agentic e agentic-sdlc

Course version: 2.1-content
Content contract: slide-content-v1
Efficacy: efficacy not verified
Feedback flow: IC1

## Per chi segue il corso

Leggi [SLIDE_CONTENT.md](SLIDE_CONTENT.md), fonte primaria completa della versione 2.1-content. Ogni slide contiene testo esatto, spiegazione, specifica visiva, transizione e fonti; le verifiche rimandano alla soluzione successiva. Il caso Orione è inventato. I moduli 1.0-draft restano come materiale storico e non sono la fonte del nuovo rendering. Efficacia umana non verificata; il report della versione precedente non valuta questa revisione.

## Scelta del formato

Il proprietario ha richiesto un documento testuale dettagliato per ogni slide, utilizzabile direttamente senza inventare parti mancanti. La modalità è lettura autonoma; un futuro PPTX deriva dal testo e non lo sostituisce. Confronto con note curate, obblighi osservabili e prova di trasferimento rendono verificabile il valore promesso dal corso. Non viene generato un nuovo PPTX in questa revisione.

## Obiettivi progressivi

- **O1:** spiegare perché la memoria di una chat non equivale a un folder di progetto persistente e come l'agente consulta solo il materiale pertinente.
- **O2:** raccontare il percorso di una fonte dalla conservazione ai claim e al grafo degli argomenti, fino a una risposta con provenienza.
- **O3:** spiegare che cosa accade quando una fonte nuova contraddice la precedente e perché un conflitto non si risolve scegliendo in silenzio.
- **O4:** scegliere un livello di triage per un cambiamento e collegarlo al beneficio e ai confini della Vision.
- **O5:** seguire una modifica attraverso bisogni degli attori, regole osservabili, interazione, rischi, capacità esistenti, Impact, design, implementazione, verifica, review, chiusura e GUIDE, distinguendo scopo e sequenza di ciascuno.
- **O6:** decidere quale skill governa un'attività, distinguere Standalone da devPNT e applicare il percorso a un documento e a una modifica ipotetica del proprio progetto, dichiarando fonte, decisione umana e verifiche mancanti.
- **O7:** spiegare con il medesimo progetto narrativo la differenza con/senza skill dopo una settimana, un mese e anni, insieme alle condizioni che possono far perdere il beneficio.

## Piani delle spiegazioni

L’evidenza attesa per gli obiettivi guida le spiegazioni seguenti; i quesiti dettagliati e le soluzioni concretizzano quei criteri. Il testo completo è già scritto nel sorgente canonico.

### M1 — Il problema che resta dopo la chat

Partire da Orione: una persona chiede all'agente perché un timeout fu fissato a 30 secondi, ma la ragione è in una chat terminata. Spiegare la differenza fra contesto disponibile ora e conoscenza custodita nel progetto. Mostrare un folder aperto come progetto da Claude o Codex e l'uso di indici per aprire solo la decisione pertinente. Controesempio: riversare tutto il manuale nel prompt. La transizione chiede che cosa accade quando nel folder entra un manuale nuovo.

### M2 — Dal manuale alla risposta rintracciabile

Orione riceve un manuale di integrazione. Spiegare in ordine perché si conserva la fonte, si estraggono affermazioni atomiche con locatori, si collocano nel grafo degli argomenti e si scende nel grafo per rispondere. Distinguere il grafo KB, che organizza *di cosa* si sa, dal grafo di questo corso, che ordina *che cosa capire prima*. Un estratto ipotetico del Manuale 2.1, §4.3, p. 48, mostra un claim e una risposta che cita il passaggio. La transizione introduce una fonte incompatibile nello stesso ambito.

### M3 — La memoria che sa correggersi

Una seconda fonte su Orione contraddice la prima **per lo stesso periodo e le stesse condizioni**: spiegare il conflitto con due affermazioni specifiche e perché la skill le conserva contestate finché arriva una fonte o un fatto umano nuovo. A confronto, una regola valida fino a giugno e una diversa valida da luglio possono coesistere senza conflitto. Mostrare la differenza tra correggere una conoscenza e accumulare note incompatibili. Il limite: conservare senza rivedere non garantisce verità. La transizione è una modifica software motivata dalla regola valida.

### M4 — Dal beneficio al livello di lavoro

La nuova regola richiede una modifica a Orione. Iniziare dal beneficio atteso per chi usa il software, poi mostrare perché un typo, una correzione locale e un cambiamento significativo pagano costi di processo diversi. Spiegare la Vision come criterio per respingere una soluzione che risolve il file ma perde il beneficio. Non anticipare le sigle di design prima che la necessità di analizzare il cambiamento sia chiara. La transizione apre le tre domande: chi ne ha bisogno, attraverso cosa lo userà, che cosa può andare storto.

### M5 — Tre lenti e una soluzione verificabile

Sullo stesso cambiamento, spiegare bisogni degli attori, regole e casi osservabili della Functional Spec, contratto d'interazione e rischi come domande complementari. Prima dell'Impact controllare le capacità esistenti con il Capability Ledger; poi introdurre Impact e design dettagliato. Seguire il lavoro fino all'implementazione, ai test tecnici, alla review finale e alla chiusura che aggiorna la conoscenza del progetto; una GUIDE conserva il modello operativo emerso quando è giustificata. Per ogni artefatto dire quale errore impedisce, non soltanto il nome. Lo sviluppatore prepara fonte, analisi, modifica ed evidenze; il responsabile tecnico valuta beneficio, ambito, rischio e decisione che resta umana. Esplicitare che i documenti governati D-UC/D-IC/P-TM/E-ISP/E-TDD appartengono al percorso con devPNT, con Functional Spec e Ledger nell'E-ISP, mentre Standalone mantiene la disciplina in ANALYSIS e nei file di progetto. La transizione chiede quale skill governa la prossima attività.

### M6 — Due skill, una memoria di progetto

Orione chiede sia di studiare il nuovo manuale sia di cambiare il software. Svolgere nella spiegazione un esempio completo: domanda sul manuale, risposta con locatore o lacuna dichiarata, beneficio della modifica, attori, superficie, rischio, decisione umana, implementazione e controlli prima della chiusura. Spiegare la proprietà della fonte e del grafo KB da un lato, la proprietà del cambiamento software dall'altro, e come un risultato verificato del primo alimenta il secondo senza duplicare l'autorità. Mostrare la modalità Standalone completa e ciò che devPNT aggiunge come governance opzionale. Solo dopo la spiegazione proporre un'applicazione facoltativa al proprio progetto: scegliere in sola lettura un documento che si è autorizzati a usare e una modifica ipotetica, porre una domanda, citare la risposta o la lacuna, tracciare beneficio, attori, superficie, rischio, decisione umana e verifica ancora dovuta. La risposta può essere orale o in note personali; non si invia il documento al corso o ai simulatori. Il criterio diagnostico segnala quale elemento manca e rimanda a M2, M4 o M5. La transizione riapre Orione dopo una settimana, un mese e anni.

### M7 — Che cosa cresce nel tempo

Raccontare Orione a tre tappe. A ogni tappa confrontare il riuso di una nota curata e quello del folder mantenuto con le due skill, senza presupporre che un agente privo di skill non sappia documentare; spiegare in parole semplici quale ricostruzione è evitata e quale fonte o decisione va invece ricontrollata. Dopo anni entra un collega nuovo che non conosce le chat passate. Concludere con il limite: il patrimonio cresce se viene consultato, corretto e mantenuto; nessuna percentuale di produttività è implicata. La verifica chiede una spiegazione causale, non la produzione di file.

## Teaching alignment

L'evidenza richiesta e la risposta insufficiente sono fissate prima della verifica della nuova revisione. I locatori seguenti descrivono il testo realmente scritto; le soluzioni vanno lette dopo il tentativo.

| Obiettivo e contesto | Evidenza e criterio di riuscita | Ponte esplicativo ed esempio | Supporto e correzione | Risposta plausibile insufficiente |
|---|---|---|---|---|
| O1: riaprire una decisione | S11: distinguere contesto, file e consultazione con fonte e motivo | S06–10: stessa decisione fra sessioni, confronto con nota curata | S12 e ritorno a S07–10 | L'agente ricorda da solo, basta salvare tutto |
| O2: risposta dal manuale | S17: percorso fonte, claim con ambito e locatore, tema e risposta | S13–16: esempio completo riapribile | S18 distingue le funzioni dei riferimenti | Il file conservato dimostra già ogni affermazione |
| O3: regole incompatibili | S23: confronto A–B/B–C condizionato alla versione mancante | S19–22: conflitto, variante temporale e rettifica | S24 corregge recenza e ambito | Vince sempre il documento arrivato dopo |
| O4: scegliere lavoro proporzionato | S27: livello motivato dagli effetti, decisione al confine e limite della Vision | S25–26, variante refuso/comportamento di S27 | S28 distingue certezza, Spike e ampliamento | Una riga è L1; la navigazione è inclusa perché conviene |
| O5: cambiamento fino alla chiusura | S38: omissioni specifiche, sequenza motivata, indipendenza delle review e criterio per GUIDE | S29–37; S33–34 completano evidenza → riuso → design e variante | S39 ordina review, implementazione, prove, review finale, chiusura | Test della costante verde; autore che si ricontrolla chiamato indipendente; elenco di sigle senza funzione |
| O6: fonte e modifica propria | S42: responsabilità e modo disponibile; S44: fonte/limite, beneficio, rischio, prova | S40 handoff completo, S41 modalità | S43 e autoconfronto S44 accettano lacune dichiarate | La rettifica decide tutto; devPNT è necessario; test inventato |
| O7: scegliere disciplina nel tempo | S47: tre confronti equi con costi/limiti; S50: raccomandazione autonoma sui casi nuovi | S45–46, S49: stesso compito, condizioni equivalenti | S48 e S51; ripresa facoltativa differita S52 | Skill sempre indispensabile; rendimento garantito negli anni |

Il supporto diminuisce: esempi svolti, domande guidate, poi raccomandazione autonoma S50. Non è richiesta la consegna di artefatti o l'esecuzione di modifiche. La verifica dell'apprendimento umano resta fuori dalle evidenze disponibili.

## Sequenza e locatori

I locatori delle sette lezioni sono stati verificati dal controllo strutturale del corso; il controllo non prova la correttezza dei contenuti. `Check` è una domanda di comprensione con criterio e percorso di correzione, non un'esercitazione obbligatoria.

| Module ID | Profile | Objective ID | Concepts | Explanation | Sources | Check | Next |
|---|---|---|---|---|---|---|---|
| M1 | P1 | O1 | CO1; CO2 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s02 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s11 | M2 |
| M2 | P1 | O2 | CO3; CO4 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s13 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s17 | M3 |
| M3 | P1 | O3 | CO5 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s19 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s23 | M4 |
| M4 | P1 | O4 | CO6 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s25 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-7 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s27 | M5 |
| M5 | P1 | O5 | CO7; CO8 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s29 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s38 | M6 |
| M6 | P1 | O6 | CO9 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s40 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s42 | M7 |
| M7 | P1 | O7 | CO10 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s45 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s50 | end |
