---
id: C-001
feature: Corso su kb-agentic e agentic-sdlc
domain: course
level: L3
status: IN_PROGRESS
start_date: 2026-09-27
end_date:
---

# Course Analysis: kb-agentic e agentic-sdlc

## Objective

Produrre un corso testuale per singoli membri di un team software che spieghi come le due skill cambiano il lavoro con un agente, con particolare attenzione al vantaggio che si accumula nello stesso progetto dopo una settimana, un mese e anni. Il risultato deve insegnare meccanismi e limiti attraverso spiegazioni progressive, non limitarsi a nominare artefatti o proporre esercizi. Questo corso è anche una prova sul campo di `course_creator`.

## Feature Vision

Autorità: `ai_docs/vision/features/VISION_course_agentic-sdlc-kb-agentic.md`, approvata dall'autore del progetto il 2026-09-27. Benefici serviti: confronto con e senza skill, memoria verificabile nel folder di progetto, governo proporzionato del cambiamento, valore cumulativo nel tempo. L'elicitazione è stata chiusa dalla Vision e dalle correzioni esplicite dell'autore: le spiegazioni possono usare esempi comprensibili senza produrre artefatti durante la lezione; le esercitazioni sono secondarie.

## Use Cases / User Needs

Nomi di prodotto: `kb-agentic`, `agentic-sdlc`, `ai_docs/`, `GUIDE`, `devPNT` = EXISTS nei testi locali; il corso e il caso narrativo Orione = NEW; «memoria del collega AI» = METAPHOR, mai superficie da azionare.

### UC1 — Capire il vantaggio rispetto all'uso ordinario

La persona P1 apre il corso senza padronanza accertata delle due skill e vuole capire perché il contesto di una chat non basta come memoria di progetto, quale folder mantenere e quale differenza pratica fa la consultazione mirata. Traccia: Expected Benefit, promessa 1 e 6 della Vision.

### UC2 — Seguire e ritrovare una fonte

La persona P1 vuole capire che cosa accade a un manuale acquisito con `kb-agentic`: conservazione della fonte, estrazione di affermazioni con provenienza, collocazione nel grafo degli argomenti, recupero e gestione del conflitto. Traccia: promessa 2 della Vision.

### UC3 — Governare una modifica software

La persona P1 vuole seguire una modifica dal beneficio della Vision alla scelta del livello di triage, alle tre lenti su bisogni/interazione/rischi, al design e alle review, sapendo che cosa rimane disponibile nella sessione seguente. Traccia: promessa 3 della Vision.

### UC4 — Scegliere il metodo e valutarne l'accumulo

La persona P1 vuole distinguere quale skill governa un compito, il percorso Standalone dall'amplificazione devPNT e l'effetto dopo una settimana, un mese e anni, inclusi i costi di manutenzione della conoscenza. Traccia: promesse 4 e 6 e Success Signals della Vision.

### UC5 — Trasferire il metodo al proprio progetto

La persona P1 vuole partire da un documento e da una modifica ipotizzata nel proprio progetto, ricostruire una risposta con fonte, impostare il cambiamento e indicare la decisione umana e i controlli ancora dovuti. Traccia: promessa 5 della Vision. L'attività è guidata e può essere svolta oralmente o in note personali; non richiede di modificare il repository.

## Functional Spec

- Fonte primaria: SLIDE_CONTENT.md, versione3.0-content, contratto slide-content-v1, 52 unità in sette moduli. Ogni unità ha testo visibile, spiegazione completa, significato visivo, transizione e fonte. La vista per l’allievo deriva dagli stessi blocchi. Il precedente PPTX2.1 rimane storico; non si rigenera prima della definizione finale del testo.
- Il percorso P1 comune serve sviluppatore e responsabile tecnico senza assumere conoscenza specifica provata. Mantiene O1–O7 e la Vision approvata. Distingue le prospettive di ricerca tecnica, giudizio sul beneficio e decisione umana.
- Il racconto parte da una richiesta che scade dopo30 secondi e dalla domanda sul motivo. Prima presenta il caso, poi nota verificabile, definizione di skill, cartella e recupero. Non richiede concetti spiegati soltanto in slide successive.
- Il grafo governa prerequisiti e locatori reali di spiegazione/primo uso, anche entro una slide. CO11/CO12 rendono espliciti definizione di skill e confronto con note; i concetti precedenti mantengono la loro identità con sottotracce dei passaggi.
- Orione è fittizio. La successione giugno/luglio non è un conflitto; B/C contrastano nello stesso ambito e D rettifica il tipo di richiesta. La regola standard di luglio è45; le urgenti restano30. La decisione al confine viene resa esplicita come scelta di prodotto, non attribuita al manuale.
- La spiegazione software segue beneficio, attori, regole, flussi, rischi, indagine di capacità, Impact/design, review indipendente, implementazione/prove e chiusura. Una GUIDE è motivata solo da conoscenza riusabile con provenienza. L’ordine di lettura non impone di svolgere analisi e indagine come compartimenti senza iterazioni.
- Note curate e protocollo sono confrontati su condizioni equivalenti; la disciplina richiede conservazione, consultazione e manutenzione. Nessun automatismo garantisce conformità o produttività.
- Prove guidate con soluzione successiva preparano il trasferimento su casi nuovi e l’applicazione facoltativa al progetto. Sono richieste ragioni e limiti, non nomi di documenti. Non si inviano documenti o eseguono modifiche reali durante il corso.
- Struttura, fedeltà, review didattica e diagnostica sequenziale sono evidenze distinte. Autore principale, lettore P1 e reviewer indipendente hanno ruoli separati; controllo senza corso distinto. Il report delimita versione, materiale, tentativi e isolamento per istruzioni. Efficacia umana non verificata.

## Interface Contract

### IC1 — Lettura e orientamento
P1 apre COURSE_PLAN e legge SLIDE_CONTENT in ordine. Il contratto richiede che Learner content contenga tutto il ragionamento necessario in self-study, senza dipendere da slide successive o dalla spiegazione riservata all’autore. La revisione3.0-content applica questo requisito all’intero percorso; il verdetto è limitato alle verifiche documentate nel report corrente. D-IC conserva il canale feedback `not available`.

### IC2 — Risalita alle fonti
Le sezioni Sources rimandano a sources.md e agli snapshot consultabili. Fonti cambiate richiedono nuova verifica. I casi inventati non sono evidenza empirica.

### IC3 — Verifica della comprensione
Il lettore tenta la domanda prima della soluzione successiva e usa i criteri per rileggere il passaggio carente. Non c'è registrazione automatica. S50 riduce i suggerimenti dopo gli esempi; S52 invita facoltativamente a riprovare in seguito.

### IC4 — Applicazione al proprio progetto
S44 propone un documento in sola lettura e una modifica ipotetica, con fonte o limite, beneficio, responsabilità, rischio e prova. L'esempio di autoconfronto accetta evidenze dichiarate mancanti, non fatti o test inventati. Nessun file viene inviato o modificato.

## Capability Ledger

| Capability | Existing or missing | Evidence and consequence |
|---|---|---|
| Progettare per profilo e prerequisiti | EXISTS | `distributions/course-creator/skills/course-creator/learning_design.md`; usare grafo e stati iniziali, senza dedurre competenza dal ruolo. |
| Registrare Vision, ANALYSIS, rischio e dettagli del corso | EXISTS | `distributions/course-creator/skills/course-creator/SKILL.md` e `templates.md`; creare gli artefatti canonici con `domain: course`. |
| Verificare la struttura dei materiali | EXISTS | `scripts/course_check.py` della distribuzione course; controlla locatori, ID, ordine e stato, non verità né apprendimento. |
| Rilevare lacune di spiegazione indipendentemente | EXISTS | `simulation.md` definisce sessioni fresche e controllo senza corso; i risultati restano diagnostici. |
| Misurare apprendimento umano di questo team | MISSING | Nessuna prova con persone è stata eseguita; consegnare con «efficacia non verificata» e raccogliere eventuali riscontri futuri senza inventare un pilot. |

Una guida CURRENT specifica per la produzione di questo corso non risulta nel router `ai_docs/reference/INDEX.md` (solo release e shared-memory). Lo studio delle skill usa i loro originali come autorità; nessuna nuova GUIDE è giustificata prima di una lezione ripetibile emersa dal banco di prova.

## Impact

| Path | ADD/MODIFY/DELETE | Responsibility and why |
|---|---|---|
| ai_docs/solutions/ANALYSIS_course_agentic-sdlc-kb-agentic.md | MODIFY | Design corrente e Diary. |
| ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md | MODIFY | Riscrittura completa delle52 unità per progressione e valore distinguibile. |
| ai_docs/solutions/courses/agentic-sdlc-kb-agentic/COURSE_PLAN.md, CONCEPT_GRAPH.md | MODIFY | Allineamento delle spiegazioni, verifiche e locatori reali del grafo. |
| ai_docs/solutions/courses/agentic-sdlc-kb-agentic/D-IC.md, sources.md | MODIFY | Versione3.0-content; canale e snapshot delle fonti conservati. |
| ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SIMULATION_REPORT.md, simulation_3_0/ | MODIFY/ADD | Evidenze del lettore, controllo e revisore, compreso field test del metodo. |
| ai_docs/solutions/courses/agentic-sdlc-kb-agentic/history_2_1/ | ADD | Conservare materiale e report precedente senza usarli come autorità corrente. |
| ai_docs/audit/reviews/REVIEW_course_text_3_0.md, REVIEW_LOG.md | ADD/MODIFY | Design gate e review del contenuto effettivo. |
| ai_docs/audit/HANDOFF_course_agentic_sdlc_kb_agentic.md, indici generati | MODIFY | Stato della consegna, prossima decisione sul testo e chiusura globale distinta. |

D-UC, P-TM e Vision restano applicabili e riletti; nessuna modifica alla skill, ai suoi script o al PPTX. Le esportazioni sono viste derivate del sorgente canonico.

## Learning and Content Risks

### C-1 — Fonte sbagliata o versione superata

Un dettaglio delle skill può essere insegnato come attuale quando è cambiato. Mitigazione: `sources.md` con file, sezione e versione; controllo distinto di verità e chiarezza prima della consegna. Residuo: il repository può cambiare dopo la revisione.

### C-2 — Prerequisito implicito

Il ruolo software può far presumere che la persona conosca già grafo, ledger, Vision o triage. Mitigazione: nessun `PROVATO` senza prova, grafo dei prerequisiti, definizione al primo uso e simulazione con profilo iniziale dichiarato. Residuo: la composizione reale del team non è stata misurata.

### C-3 — Materiale che elenca artefatti senza spiegare

La lezione può diventare un catalogo di sigle, slide o esercizi. Mitigazione: spiegazione causale e esempio Orione prima dei nomi e della verifica; review di ogni passaggio e della transizione. Residuo: leggibilità simulata non dimostra comprensione umana.

### C-4 — Promessa temporale troppo forte

Settimana, mese e anni potrebbero sembrare rendimenti garantiti. Mitigazione: presentare il confronto come scenario condizionato a consultazione, provenienza e manutenzione, senza numeri di produttività inventati. Residuo: il beneficio reale dipende da disciplina e contesto del progetto.

### C-5 — Simulazione contaminata o interpretata come prova umana

Un agente con accesso al repository può leggere il corso anche nel controllo o usare risposte nascoste. Mitigazione: sessioni fresche, pacchetti chiusi e accesso simmetrico, prompt e output conservati, esiti diagnosticati contro criteri predefiniti. Residuo: agenti e persone apprendono diversamente.

### C-6 — Confusione fra skill e devPNT

Presentare D-UC/E-ISP/E-TDD governati come requisiti della modalità Standalone ne falserebbe il valore. Mitigazione: distinguere in ogni spiegazione le sezioni e i file Standalone dalle proposte versionate devPNT; fonte `hybrid.md`. Residuo: terminologia vicina tra modalità richiede esempi espliciti.

### C-7 — Feedback non disponibile

Il corso non ha un canale diretto verso l'autore. `D-IC.md` registra `not available`; eventuali riscontri arrivati attraverso il committente saranno datati e attribuiti al modulo. Residuo: la mancanza di segnalazioni non significa assenza di difficoltà.

## Action Plan

1. Leggere il contratto corrente di course-creator e i supporti learning_design, slide_content, simulation e templates; riaprire Vision, fonti e obiettivi del corso.
2. Revisionare l'intero SLIDE_CONTENT come scoperta progressiva. Usare la bozza di quattro unità come candidato diagnostico, senza considerarla già integrata o sufficiente. Allineare grafo e piano con locatori distinti per spiegazione e primo uso dipendente; rendere ogni unità comprensibile usando soltanto quanto precede.
3. Il principale autore integra i materiali. Lettori indipendenti per profilo ricevono una unità alla volta; il reviewer didattico indipendente giudica spiegazioni e risultati. Eseguire controlli separati e usare nuovi lettori dopo le correzioni, secondo simulation.md. Conservare versioni, prompt e risultati.
4. Verificare struttura e fonti, risolvere i finding, consegnare il testo completo per definizione finale con il proprietario. Solo dopo rigenerare il PPTX e controllare anche la progressione introdotta dalle suddivisioni del rendering.
5. Aggiornare report e handoff, rigenerare indici e riportare separatamente lo stato del gate globale. Non dedurre efficacia umana dalle simulazioni.

## Test Strategy

- Verifica strutturale: `python distributions/course-creator/skills/course-creator/scripts/sdlc_check.py course agentic-sdlc-kb-agentic --root .`; poi `index` e `check` alla chiusura.
- Revisione delle fonti: ogni frase fattuale sulle skill ha un riferimento in `sources.md`; ogni esempio ipotetico è riconoscibile come tale.
- Revisione della spiegazione: un lettore indipendente indica per ogni modulo dove sono obiettivo, prerequisito, meccanismo, esempio, limite e passaggio alla lezione seguente; per M5 verifica anche implementazione, test e chiusura.
- Trasferimento: l'attività di M6 deve permettere di identificare fonte o lacuna, beneficio, attori, superficie, rischio, decisione umana e verifica ancora dovuta. La sua presenza nel corso è verificabile; l'esecuzione da parte di persone reali resta non dimostrata.
- Simulazione: criteri e pacchetti fissati prima, un agente con corso e un controllo senza, identico compito e accesso esterno; confrontare errori e blocchi, non dichiarare apprendimento umano.
- Eventuali riscontri umani successivi vanno in `FEEDBACK_REPORT.md` con contesto, criterio e casi contrari prima di cambiare la dicitura di efficacia.

## Diary / Current State
2026-09-29: feedback del proprietario su S24 («sembra un esercizio per l'agente»): S23/S24 facevano giudicare un aggiornamento interno della KB. Ora partono da ciò che la persona riceve davvero da kb-agentic: una risposta a una collega scelta per recenza e la domanda che l'agente pone a fine lavoro sul conflitto (reconciliation.md §4, claim-5 esteso e da verificare sullo snapshot). La persona contesta la risposta, risponde con un fatto e non con una preferenza, e verifica la risposta dopo il chiarimento. S20 dice come arriva la domanda. O3 e alignment allineati. Non riesaminato.

2026-09-29: tesi resa esplicita su richiesta del proprietario: con le due skill l'agente, pur senza ricordare le sessioni, ritrova nel progetto storia e motivi dei cambiamenti e lavora come se avesse l'esperienza del progetto, finché le tracce sono registrate e mantenute. Promessa in S01, sintesi in S52 (fonte claim-2), cella «Teaching contribution» della tabella del valore. Non riesaminato.

2026-09-29: feedback del proprietario su S14 («per un utente non ha molto senso»): la persona non legge i claim nella KB, vede le risposte dell'agente che li citano. S14 ora spiega il claim come base della domanda «a quale passaggio e a quali casi si riferisce?»; S15 e S16 dicono che la persona vede gli esiti nelle risposte e la traccia dichiarata dall'agente (claim-2 esteso, verificato sullo snapshot); S17/S18 partono dalla risposta dell'agente e dal passaggio che la persona si fa mostrare, non dalla tabella del claim. O2, alignment e grafo allineati. Modifiche non ancora riesaminate.

2026-09-28: versione 3.2-content, correzione dei WARN 1–5 della simulazione 3.1 (S24 fonte dei 25 s, chi produce gli artefatti in coda a S15, S43 devPNT non configurato e livello assegnato da sé, S37, riga L2 di S26 dalla fonte); review mirata PASS, due nit corretti dopo senza riesame. Versione 3.1 in `history_3_1/`. Non eseguito: retest con lettore fresco dei prefissi modificati, secondo compito congelato con indizio invertito (WARN 6). Prossimo: lettura del proprietario, poi eventuale PPTX. Efficacia non verificata.

2026-09-28: simulazione 3.1 eseguita (`simulation_3_1/`, `SIMULATION_REPORT.md`). Lettore sequenziale su 52 unità senza convinzioni errate e con risposte da persona alle otto prove; compito finale 7/8 con K8, controllo senza corso 4/8. Revisore indipendente: READY per P1 simulato, 6 WARN non ancora corretti (S24 fonte dei 25 s, chi produce gli artefatti in S08/S13, correzioni in S43, S37, S26, secondo compito con indizio invertito). Efficacia non verificata.

2026-09-28: versione 3.1-content scritta sul modello della Vision emendata. S17, S23 e S27 (con S18, S24, S28) ora fanno giudicare alla persona un'uscita dell'agente; voce agente/persona corretta in S13–S16, S19–S22, S26, S29, S30, S33, S34, S36, S39, S42–S44, S46, S51; O2–O4, alignment, grafo, D-UC e claim-6 allineati. Versione 3.0 in `history_3_0/`. Review indipendente del contenuto: FAIL al primo giro (1 BLOCK su S23), PASS al secondo; due nit corretti dopo la review, non riesaminati. course_check 0/0. Prossimo: simulazione 3.1 con criteri sugli atti della persona (sostituiscono K2–K4 della 2.1), poi lettura del proprietario prima di un nuovo PPTX. Efficacia non verificata.

2026-09-28: Vision del corso emendata e approvata dal proprietario (il corso insegna gli atti della persona che lavora con l'agente). Con la regola F-060 sull'atto della persona, S17, S23 e S27 della 3.0 falliscono l'accettazione (prova in `harness_course_role/`), e i criteri K2, K3 (parte sul livello) e K4 di `simulation_2_1/CRITERIA.md` premiano operazioni dell'agente. Da correggere qui prima di un nuovo PPTX.


### Stato attuale

Corso 3.0-content completo: 52 unità in sette moduli con testo allievo, spiegazione, significato visivo, transizione, fonti, domande e soluzioni. Piano e grafo sono allineati ai passaggi effettivi. La review indipendente ha individuato due omissioni sulla review e un raccordo cronologico; le correzioni hanno superato il riesame circoscritto. SIMULATION_REPORT registra diagnostica progressiva su 52 unità a esposizione mista, nuovo lettore sul prefisso corretto e controllo separato, con il verdetto indipendente e i limiti. Non è una singola lettura integrale della versione finale e non dimostra efficacia umana. Il testo viene consegnato al proprietario per la definizione finale; nessun nuovo PPTX. Chiusura globale non dichiarata CLEAN.

### Diario

- 2026-09-27: Vision approvata dall'autore dopo due correzioni: vantaggio cumulativo esplicito e spiegazioni con esempi senza obbligo di artefatti prodotti. Corso in design; fonti locali da fissare e review indipendente da eseguire. Nessun materiale didattico consegnato, nessuna efficacia umana verificata.
- 2026-09-27: review indipendente del design: 1 BLOCK (applicazione promessa ma non progettata), 3 WARN (M7, ambito temporale del conflitto KB, differenza di ruolo). UC5 e IC4, esempio end-to-end e attività guidata aggiunti; re-review richiesta prima della produzione.
- 2026-09-27: re-review circoscritta PASS, nessun finding aperto sul design. Inizia la produzione delle sette lezioni; la qualità delle spiegazioni e l'esito della simulazione restano da verificare.

- 2026-09-27: riallineamento richiesto dal proprietario. Registrati lo stato dei sette moduli, la review dei materiali PASS e la simulazione già eseguita, rimandando ai rispettivi record per i dettagli. La chiusura documentale resta distinta dalla disponibilità del corso e dall'efficacia umana non verificata. Indici rigenerati; questo intervento non modifica lezioni, fonti o pacchetto simulato.

- 2026-09-27: revisione autorizzata del contratto e del materiale per contenuto completo per slide e valore distinguibile; vedere F-060 e FEEDBACK_REPORT. Nessuna nuova dichiarazione di efficacia.

- 2026-09-27: dopo la richiesta di rinviare le slide, avviata revisione effettiva del solo testo. Diagnosi indipendente FAIL su O4–O7; design D01–D07 PASS prima della produzione. Sostituite 16 unità e allineato il design corrente, preservando le fonti e le versioni storiche.

- 2026-09-27: review finale FAIL per indipendenza del reviewer non esplicitata; corretti S36/S38/S39, re-review PASS. Testo consegnabile per revisione del proprietario. Dati diagnostici e hash conservati; nessuna pretesa di apprendimento umano o chiusura globale del repository.

- 2026-09-27: riallineamento dell’handoff richiesto dal proprietario. Registrata la generazione successiva del PPTX 2.1, i difetti di progressione emersi, le correzioni F-060 e la separazione tra bozza diagnostica di quattro unità e corso canonico. Riaperta esplicitamente la revisione completa; conservati i risultati storici senza estenderne il significato. Nessun nuovo corso o PPTX prodotto in questo passaggio.

- 2026-09-27: il proprietario richiede il corso completo. Avviata3.0-content sotto la Vision esistente; design review indipendente PASS, recepiti tre richiami. Riscrittura completa, fonte unica e export derivati; prove diagnostiche con contesti separati previste prima della consegna.

- 2026-09-27: completata produzione 3.0-content e preservati design gate, FAIL della prima review, correzioni e riesame. Registrati lettura sequenziale, nuovo prefisso e confronto senza corso con limiti espliciti. Consegna testuale completa; versione 2.1 e suo PPTX restano storici, rendering successivo alla definizione finale del testo.
