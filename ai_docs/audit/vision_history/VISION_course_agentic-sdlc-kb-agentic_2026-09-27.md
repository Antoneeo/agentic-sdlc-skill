---
description: Vision del corso per sviluppatori su kb-agentic e agentic-sdlc, usato come primo banco di prova di course_creator.
status: SUPERSEDED
domain: course
---

<!-- Historical version: approved before 2026-09-28; superseded by ai_docs/vision/features/VISION_course_agentic-sdlc-kb-agentic.md after the owner approved the person-acts amendment on 2026-09-28 (F-060). -->

# Course Vision: lavorare con kb-agentic e agentic-sdlc
Status: SUPERSEDED

## Expected Benefit

Una persona del team di sviluppo sa usare `kb-agentic` e `agentic-sdlc` per lavorare con un agente che ritrova conoscenza verificabile tra sessioni e governa i cambiamenti software in rapporto al rischio. Sa preparare un folder di progetto persistente e distinguere il compito delle due skill. Soprattutto, sa **confrontare lo stesso lavoro svolto con e senza le skill**: quali fonti, decisioni e ragionamenti si perdono o vanno ricostruiti, quali restano riutilizzabili, e come il vantaggio cambia quando il progetto continua per settimane, mesi e anni.

Questo corso è anche il primo caso reale per `course_creator`: la sua progettazione, produzione e revisione devono rendere osservabile se la skill sa partire dal destinatario, ordinare concetti dipendenti, produrre spiegazioni comprensibili e correggerle usando test diagnostici. Un difetto del corso porta a correggere il corso; un difetto ripetibile del metodo può motivare una GUIDE o una modifica separata di `course_creator`.

## Learners and Starting Point

- **Sviluppatore del team che usa già agenti AI** — conosce il proprio lavoro software e l'uso ordinario di Claude o Codex, ma la familiarità con le due skill, `ai_docs/`, la gestione delle fonti e gli artefatti del processo è da accertare. Vuole capire come impostare e svolgere un'attività reale senza ricominciare da zero a ogni sessione.
- **Responsabile tecnico che collabora con agenti e sviluppatori** — deve riconoscere beneficio atteso, decisioni riservate alle persone, rischi e prove che giustificano una modifica. La conoscenza iniziale delle due skill è da accertare; il ruolo non prova la padronanza dei loro meccanismi.

Il corso usa un profilo didattico esplicito per ogni percorso o variante. La classificazione dei prerequisiti come `PROVATO`, `INCERTO` o `DA_INSEGNARE` dipende da evidenze raccolte per quei destinatari, non dal titolo professionale. In assenza di evidenza, il concetto resta incerto e viene spiegato prima dell'uso oppure dichiarato come limite.

## Promised Understanding and Ability

Al termine, il destinatario può:

1. spiegare con un esempio concreto perché il contesto di una chat non basta come memoria di progetto e perché il folder persistente aperto come progetto da Claude o Codex è la condizione operativa delle due skill;
2. seguire il percorso di una fonte in `kb-agentic`: acquisizione, estrazione di affermazioni con provenienza, collocazione nel grafo degli argomenti, recupero mirato, gestione di obsolescenza o conflitto; distinguere questo grafo dal grafo dei prerequisiti didattici del corso;
3. seguire un cambiamento software con `agentic-sdlc`: triage proporzionato al rischio, Vision e beneficio atteso, bisogni degli attori, superfici d'interazione, rischi, impatto, design, review indipendente, implementazione, verifica e conoscenza conservata nelle GUIDE;
4. scegliere quale skill governa un'attività concreta, mostrare quando le due collaborano e distinguere il percorso Standalone dall'eventuale governance aggiunta da devPNT;
5. eseguire, con i documenti del proprio progetto, un piccolo scenario di consultazione della conoscenza e uno di pianificazione di una modifica, indicando fonti, decisioni umane e limiti di ciò che l'agente ha verificato.
6. mostrare, sullo stesso progetto seguito nel tempo, il valore cumulativo delle due skill rispetto all'uso di un agente senza questa memoria e questo processo: che cosa è già ritrovabile dopo una settimana, che cosa viene riusato e aggiornato dopo un mese e quale patrimonio può essere consegnato a una persona o a un agente nuovo dopo anni.

Il corso costruisce queste capacità con spiegazioni progressive legate al lavoro dei destinatari. Esempi, controesempi e verifiche servono a scoprire dove la spiegazione lascia un passaggio implicito; una sequenza di slide o esercizi priva di spiegazioni non soddisfa la promessa.

## Valore nel tempo da rendere comprensibile

Il corso segue un progetto esemplificativo che cresce nel tempo e confronta, a ogni tappa, lo stesso compito con l'uso ordinario dell'agente e con le due skill. La spiegazione usa esempi comprensibili per mostrare che cosa accade e perché, senza richiedere la produzione di file o altri artefatti durante la lezione e senza presentare i tempi come una promessa automatica di produttività:

| Orizzonte | Senza una memoria e un processo di progetto | Con un folder mantenuto usando le skill |
|---|---|---|
| Dopo una settimana | Fonti lette e ragioni delle prime scelte possono restare disperse nelle chat; una nuova sessione richiede di ricostruirle. | Prime fonti, affermazioni con provenienza, Vision e decisioni di lavoro sono ritrovabili; l'agente apre solo ciò che serve al compito corrente. |
| Dopo un mese | Problemi già analizzati e alternative scartate possono essere studiati di nuovo; documenti e codice possono divergere senza che il motivo sia evidente. | Nuove attività consultano e correggono ciò che è già stato appreso; le GUIDE conservano modelli operativi costosi da ricostruire, mentre fonti mutate e decisioni superate sono riconoscibili. |
| Dopo anni | Un nuovo collega o agente dipende da chi ricorda la storia del progetto o da una ricerca fra chat e file non governati. | Il patrimonio del progetto può essere passato a chi arriva: fonti, grafo degli argomenti, Vision, decisioni, GUIDE e storia dei cambiamenti permettono di ritrovare il ragionamento pertinente senza caricare l'intero archivio nel contesto. |

Questo accumulo richiede consultazione e manutenzione: una fonte obsoleta non diventa affidabile perché è conservata, e una GUIDE non usata o non aggiornata non produce da sola il beneficio descritto.

## Success Signals

- Un revisore indipendente può seguire per ogni modulo il legame tra profilo del destinatario, conoscenze iniziali verificate o incerte, concetti necessari, spiegazione, obiettivo e modulo successivo. Un prerequisito usato prima di essere spiegato è un difetto del corso.
- Il destinatario sa ricostruire, a partire da un caso di progetto, dove una fonte entra nella KB, come una risposta risale alla sua provenienza, e dove una decisione o una GUIDE resta consultabile nella sessione seguente. Sa indicare che cosa non è stato verificato.
- Davanti a una modifica software proposta, il destinatario sa motivare il livello di triage, collegare le scelte al beneficio della Vision e distinguere ciò che il percorso Standalone produce nei file da ciò che devPNT governa come proposta.
- Sul caso evolutivo del corso, il destinatario sa spiegare con esempi la differenza tra i due modi di lavorare dopo una settimana, un mese e anni: che cosa l'agente potrebbe ritrovare nel progetto, come lo userebbe e quale ricostruzione eviterebbe. Sa anche indicare quando una fonte o una decisione conservata richiede revisione prima del riuso.
- Una review separata controlla fedeltà delle affermazioni alle versioni citate delle skill e chiarezza delle spiegazioni per il profilo scelto. Le fonti sono riapribili e ogni affermazione fattuale insegnata ha un riferimento controllabile.
- Agenti indipendenti che simulano i profili previsti ricevono il corso in sessioni nuove; un controllo senza corso riceve compiti e accesso alle fonti comparabili. Il confronto conserva prompt, materiali, risposte ed errori e serve a trovare lacune, senza essere presentato come prova di apprendimento umano.
- Il corso può essere consegnato con la dicitura **«efficacia non verificata»**. Una dichiarazione più forte richiede riscontri osservabili da persone reali comparabili ai destinatari dichiarati, con compiti e criteri espliciti, casi contrari e limiti documentati; possono arrivare durante l'uso, senza un pilot obbligatorio.
- Il banco di prova produce almeno un resoconto verificabile su cosa `course_creator` ha aiutato a fare, dove ha richiesto correzioni e se il problema riguarda il materiale di questo corso oppure una regola riutilizzabile della skill. Una conclusione positiva senza tentativi capaci di trovare difetti non vale come prova del metodo.

## Scope and Non-Goals

- Sono nel corso le versioni delle due skill presenti in questo repository e i loro artefatti di lavoro, con esempi realistici ma separati dai progetti e dai dati riservati del team. Il confronto con l'uso ordinario degli agenti, compreso il valore che si accumula nel tempo, è parte necessaria della spiegazione: ogni vantaggio mostrato deve avere un meccanismo comprensibile e un esempio concreto. Se si sceglie un'esercitazione, i suoi risultati possono essere osservati negli artefatti prodotti; la spiegazione non richiede di produrli.
- La conoscenza di addestramento dell'agente può aiutare a formulare spiegazioni, ma non certifica fatti sulle skill. Il materiale deve ricondurre le affermazioni alle versioni riapribili dei file e segnalare ciò che cambia o resta incerto.
- Il corso insegna il rapporto con devPNT senza farlo passare per requisito delle skill. Non installa servizi né modifica progetti reali degli allievi come condizione per seguire le spiegazioni.
- Le simulazioni di agenti e la review del materiale sono verifiche diagnostiche. Non misurano da sole l'efficacia su persone reali e non autorizzano automaticamente una modifica di `course_creator`.
- Formato, durata, numero di moduli e modalità di fruizione sono decisioni di design da prendere dopo questa Vision, in base ai destinatari e ai vincoli di erogazione. Nessun esercizio è obbligatorio per ogni modulo.
