---
description: Vision del corso per sviluppatori su kb-agentic e agentic-sdlc, usato come primo banco di prova di course_creator.
status: APPROVED
domain: course
---

<!-- Amended 2026-09-28 (F-060): the course teaches the person's acts with the agent, not the agent's operations. Approved by Antonio Pinto in the working chat ("Si") after a blind gate check PASS in round 3 (REVIEW_LOG 2026-09-28). Previous approved text archived in ai_docs/audit/vision_history/. -->

# Course Vision: lavorare con kb-agentic e agentic-sdlc
Status: APPROVED

## Expected Benefit

Una persona del team di sviluppo sa usare `kb-agentic` e `agentic-sdlc` per lavorare con un agente che ritrova conoscenza verificabile tra sessioni e governa i cambiamenti software in rapporto al rischio. Sa preparare un folder di progetto persistente e distinguere il compito delle due skill. Soprattutto, sa **confrontare lo stesso lavoro svolto con e senza le skill**: quali fonti, decisioni e ragionamenti si perdono o vanno ricostruiti, quali restano riutilizzabili, e come il vantaggio cambia quando il progetto continua per settimane, mesi e anni.

Questo corso è anche il primo caso reale per `course_creator`: la sua progettazione, produzione e revisione devono rendere osservabile se la skill sa partire dal destinatario, ordinare concetti dipendenti, produrre spiegazioni comprensibili e correggerle usando test diagnostici. Un difetto del corso porta a correggere il corso; un difetto ripetibile del metodo può motivare una GUIDE o una modifica separata di `course_creator`.

## Learners and Starting Point

- **Sviluppatore del team che usa già agenti AI** — conosce il proprio lavoro software e l'uso ordinario di Claude o Codex, ma la familiarità con le due skill, `ai_docs/`, la gestione delle fonti e gli artefatti del processo è da accertare. Vuole capire come impostare e svolgere un'attività reale senza ricominciare da zero a ogni sessione.
- **Responsabile tecnico che collabora con agenti e sviluppatori** — deve riconoscere beneficio atteso, decisioni riservate alle persone, rischi e prove che giustificano una modifica. La conoscenza iniziale delle due skill è da accertare; il ruolo non prova la padronanza dei loro meccanismi.

Il corso usa un profilo didattico esplicito per ogni percorso o variante. La classificazione dei prerequisiti come `PROVATO`, `INCERTO` o `DA_INSEGNARE` dipende da evidenze raccolte per quei destinatari, non dal titolo professionale. In assenza di evidenza, il concetto resta incerto e viene spiegato prima dell'uso oppure dichiarato come limite.

Entrambi i profili lavorano **con** un agente che esegue le skill. È l'agente ad acquisire le fonti, estrarre le affermazioni, classificare conflitti fra documenti e livello del lavoro, compilare analisi, piani e prove. La persona formula la richiesta, legge ciò che l'agente dichiara e produce, lo confronta con fonti e Vision, prende le decisioni riservate alle persone e sceglie se accettare, correggere o fermare il lavoro. Il corso insegna questi atti della persona. Spiega i meccanismi delle skill quanto serve a capire, chiedere e verificare ciò che l'agente fa; non chiede alla persona di eseguirli al posto dell'agente.

## Promised Understanding and Ability

Al termine, il destinatario può:

1. spiegare con un esempio concreto perché il contesto di una chat non basta come memoria di progetto e perché il folder persistente aperto come progetto da Claude o Codex è la condizione operativa delle due skill, e preparare quel folder per il proprio lavoro;
2. riconoscere, in ciò che l'agente riporta usando `kb-agentic`, il percorso di una fonte: acquisizione, affermazioni estratte con provenienza, collocazione nel grafo degli argomenti, recupero mirato, obsolescenza o conflitto; chiedere all'agente il riferimento che manca, senza fornirlo lei stessa, e controllare che una risposta non vada oltre l'ambito della sua fonte; distinguere questo grafo dal grafo dei prerequisiti didattici del corso;
3. accompagnare un cambiamento software che l'agente svolge con `agentic-sdlc`: capire e, se serve, contestare il livello di triage che l'agente dichiara; approvare o correggere Vision e beneficio atteso; rispondere alle domande che l'agente pone su bisogni degli attori, superfici d'interazione e rischi, senza redigere lei stessa l'analisi; prendere le decisioni aperte; riconoscere quando mancano impatto, design, review indipendente o prove prima di implementazione e chiusura; sapere dove ritrovare la conoscenza conservata nelle GUIDE;
4. decidere quale skill deve governare un'attività concreta e riconoscere se l'agente ha fatto la stessa scelta, mostrare quando le due collaborano e distinguere il percorso Standalone dall'eventuale governance aggiunta da devPNT;
5. chiedere all'agente, sui documenti del proprio progetto, un piccolo scenario di consultazione della conoscenza e uno di pianificazione di una modifica, e verificarne il risultato: quali fonti ha usato, quali decisioni spettano a una persona e che cosa l'agente non ha verificato;
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
- Davanti a una risposta dell'agente su un caso di progetto, il destinatario sa ricostruire dove la fonte è entrata nella KB, come la risposta risale alla sua provenienza e dove una decisione o una GUIDE resta consultabile nella sessione seguente. Sa indicare che cosa l'agente non ha verificato e quale riferimento chiedergli.
- Davanti a una modifica software proposta dall'agente, il destinatario sa giudicare il livello di triage dichiarato, collegare le scelte al beneficio della Vision, indicare le decisioni che restano a una persona e distinguere ciò che il percorso Standalone produce nei file da ciò che devPNT governa come proposta.
- Ogni verifica del corso chiede un atto che la persona compie nel lavoro reale con l'agente: formulare o precisare una richiesta, valutare o contestare un'uscita dell'agente, prendere una decisione che spetta a lei. La verifica parte da una richiesta da formulare, da un'uscita dell'agente da giudicare o da una decisione riservata alla persona. Una verifica il cui risultato richiesto è, anche in forma ridotta, ciò che la skill assegna all'agente — per esempio un claim estratto, un livello di triage, o i criteri che lo determinano per un caso concreto, stabiliti prima o senza la dichiarazione dell'agente, voci del registro delle capacità (Capability Ledger), una classificazione di conflitto fra documenti, i campi mancanti di un claim o un'analisi che l'agente compila — è un difetto del corso, qualunque verbo la introduca («verificare», «decidere», «capire») e anche se il contenuto è accurato.
- Sul caso evolutivo del corso, il destinatario sa spiegare con esempi la differenza tra i due modi di lavorare dopo una settimana, un mese e anni: che cosa l'agente potrebbe ritrovare nel progetto, come lo userebbe e quale ricostruzione eviterebbe. Sa anche indicare quando una fonte o una decisione conservata richiede revisione prima del riuso.
- Una review separata controlla fedeltà delle affermazioni alle versioni citate delle skill e chiarezza delle spiegazioni per il profilo scelto. Le fonti sono riapribili e ogni affermazione fattuale insegnata ha un riferimento controllabile.
- Agenti indipendenti che simulano i profili previsti ricevono il corso in sessioni nuove; un controllo senza corso riceve compiti e accesso alle fonti comparabili. Il confronto conserva prompt, materiali, risposte ed errori e serve a trovare lacune, senza essere presentato come prova di apprendimento umano.
- Il corso può essere consegnato con la dicitura **«efficacia non verificata»**. Una dichiarazione più forte richiede riscontri osservabili da persone reali comparabili ai destinatari dichiarati, con compiti e criteri espliciti, casi contrari e limiti documentati; possono arrivare durante l'uso, senza un pilot obbligatorio.
- Il banco di prova produce almeno un resoconto verificabile su cosa `course_creator` ha aiutato a fare, dove ha richiesto correzioni e se il problema riguarda il materiale di questo corso oppure una regola riutilizzabile della skill. Una conclusione positiva senza tentativi capaci di trovare difetti non vale come prova del metodo.

## Scope and Non-Goals

- Sono nel corso le versioni delle due skill presenti in questo repository e i loro artefatti di lavoro, con esempi realistici ma separati dai progetti e dai dati riservati del team. Il confronto con l'uso ordinario degli agenti, compreso il valore che si accumula nel tempo, è parte necessaria della spiegazione: ogni vantaggio mostrato deve avere un meccanismo comprensibile e un esempio concreto. Se si sceglie un'esercitazione, i suoi risultati possono essere osservati negli artefatti prodotti; la spiegazione non richiede di produrli.
- La conoscenza di addestramento dell'agente può aiutare a formulare spiegazioni, ma non certifica fatti sulle skill. Il materiale deve ricondurre le affermazioni alle versioni riapribili dei file e segnalare ciò che cambia o resta incerto.
- Il corso insegna il rapporto con devPNT senza farlo passare per requisito delle skill. Non installa servizi né modifica progetti reali degli allievi come condizione per seguire le spiegazioni.
- Il corso non addestra la persona a sostituire l'agente nelle operazioni che le skill gli assegnano. Una persona può comunque leggere una fonte o un artefatto da sola quando serve a verificare ciò che l'agente ha prodotto: la verifica è un suo atto, la produzione dell'artefatto no.
- Le simulazioni di agenti e la review del materiale sono verifiche diagnostiche. Non misurano da sole l'efficacia su persone reali e non autorizzano automaticamente una modifica di `course_creator`.
- Formato, durata, numero di moduli e modalità di fruizione sono decisioni di design da prendere dopo questa Vision, in base ai destinatari e ai vincoli di erogazione. Nessun esercizio è obbligatorio per ogni modulo.
