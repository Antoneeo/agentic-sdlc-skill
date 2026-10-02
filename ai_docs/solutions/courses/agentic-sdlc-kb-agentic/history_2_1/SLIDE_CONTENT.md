# Corso kb-agentic e agentic-sdlc — sorgente completo delle slide
Course version: 2.1-content
Delivery mode: self-study
Efficacy: efficacy not verified
Feedback flow: IC1

Documento principale per leggere e realizzare il corso. Tutto il testo in **Learner content** va reso visibile: non è una scaletta da completare a voce. I titoli sono quelli esatti; le sezioni **Visual content** definiscono il contenuto della rappresentazione. Impaginazione e stile restano liberi. Se una slide risulta troppo densa, prima si divide questo sorgente preservando il ragionamento e aggiornando gli ID; non si nasconde una parte essenziale nelle note.

Destinatario P1: persona di un team software che usa agenti, senza conoscenza presunta delle due skill. Le domande non richiedono codice o file: prova a rispondere prima di leggere la soluzione successiva. Non è fissata una durata verificata. Il feedback diretto del corso non ha un canale dedicato; eventuali osservazioni al responsabile devono identificare versione e slide. Nessuna osservazione è raccolta automaticamente.

Il caso Orione e tutti i suoi manuali, circolari e rettifiche sono inventati. La documentazione delle skill sostiene i meccanismi descritti, non prova un miglioramento misurato del team. La simulazione del vecchio materiale non valuta questa revisione.

## Course Value
| Profile | Baseline | Target capability | Teaching contribution | Observable check | Alternative and limits |
|---|---|---|---|---|---|
| P1 | Usa agenti ma non è dimostrato che sappia distinguere una nota recuperabile da una decisione verificata; nessuna conoscenza delle skill presunta | Scegliere fra note curate e protocollo, riconoscere conflitti di fonte e collegare una regola a superfici e prove | Stesso caso seguito da provenienza a rettifica e design, confronto equo con note e istruzioni equivalenti | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s50 | Una nota ben fatta basta per un caso semplice; il corso aggiunge criteri per casi che evolvono, non superiorità garantita né efficacia umana dimostrata |

## S01
Module: M1
Objective: O1
Role: orientation
Title: kb-agentic e agentic-sdlc
Value contribution: Distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Learner content
Come conservare le ragioni delle scelte e guidare una modifica software

Un caso completo, dal manuale del fornitore ai test del risultato.

Il risultato atteso è saper distinguere una traccia utile da una nota insufficiente e collegare una regola verificata a un cambiamento osservabile. Non serve imparare le sigle a memoria. Il caso sarà inventato: le regole reali devono sempre venire dalle fonti del proprio progetto.

### Complete explanation
Il risultato atteso è saper distinguere una traccia utile da una nota insufficiente e collegare una regola verificata a un cambiamento osservabile. Non serve imparare le sigle a memoria. Il caso sarà inventato: le regole reali devono sempre venire dalle fonti del proprio progetto.

### Visual content
Composizione testuale: titolo, introduzione, esempio o domanda e conclusione nell’ordine riportato in Learner content. Usare un riquadro per la citazione o domanda, se presente. Non occorrono immagini esterne: il contenuto da comprendere è interamente scritto.

### Transition
Il percorso continua con «A che cosa servono queste due skill»: distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S02
Module: M1
Objective: O1
Role: explanation
Title: A che cosa servono queste due skill
Value contribution: Distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Learner content
Una skill è un insieme di istruzioni che guida il lavoro dell’agente. Qui impariamo a riconoscere il risultato che ciascuna deve lasciare.

**kb-agentic** — Organizza la conoscenza del progetto. Esempio: conserva il manuale e collega la regola sui tempi al passaggio che la sostiene.

**agentic-sdlc** — Guida il lavoro sul software. Esempio: usa quella regola per progettare una modifica, verificarla e registrarne il motivo.

**Da ricordare:** KB significa base di conoscenza. SDLC indica il ciclo di vita dello sviluppo software.

Le due responsabilità si incontrano ma non coincidono. Sapere che un manuale prescrive una finestra temporale non prova che il pannello la rispetti; correggere il pannello non rende autentica una fonte. Separare le domande permette di chiedere l’evidenza giusta a ogni passaggio.

### Complete explanation
Le due responsabilità si incontrano ma non coincidono. Sapere che un manuale prescrive una finestra temporale non prova che il pannello la rispetti; correggere il pannello non rende autentica una fonte. Separare le domande permette di chiedere l’evidenza giusta a ogni passaggio.

### Visual content
Due riquadri affiancati: il primo è il blocco «kb-agentic», il secondo «agentic-sdlc». Riportare integralmente i rispettivi testi. Introduzione sopra, conclusione e precisazioni sotto. Nessuna freccia di causalità aggiuntiva.

### Transition
Il percorso continua con «Il caso Orione: una consegna in attesa»: distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S03
Module: M1
Objective: O1
Role: explanation
Title: Il caso Orione: una consegna in attesa
Value contribution: Distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Learner content
Orione è un progetto inventato. Un’operatrice usa il suo pannello per seguire una consegna gestita con un servizio esterno.

1. **Invio** — Orione avvia la richiesta e mostra la consegna “in attesa”.
2. **Callback** — Il servizio esterno invia una risposta a Orione: questa risposta è il callback.
3. **Scadenza** — Se la risposta non arriva entro il tempo previsto, Orione mostra “scaduta”.

**Da ricordare:** La domanda del corso: come capire il tempo corretto e aggiornare tutti gli stati che ne dipendono?

Il callback è una risposta inviata dal servizio dopo la richiesta iniziale. Il tempo fra richiesta e risposta conta perché il pannello deve dire se attendere ancora. Il corso non insegna il protocollo di rete di Orione: usa questi tre stati per rendere visibile una decisione software.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Il callback è una risposta inviata dal servizio dopo la richiesta iniziale. Il tempo fra richiesta e risposta conta perché il pannello deve dire se attendere ancora. Il corso non insegna il protocollo di rete di Orione: usa questi tre stati per rendere visibile una decisione software.

### Visual content
Sequenza numerata in ordine di lettura con tutti i titoli e testi riportati in Learner content. La numerazione esprime ordine del ragionamento, non una misura di tempo. Introduzione e conclusione restano visibili.

### Transition
Il percorso continua con «Il problema che incontreremo»: distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S04
Module: M1
Objective: O1
Role: explanation
Title: Il problema che incontreremo
Value contribution: Distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Learner content
Più avanti una rettifica chiarirà che la finestra valida è 45 secondi. Il software continua però a dichiarare la scadenza dopo 30.

| Momento | Software ancora a 30 secondi | Regola chiarita a 45 secondi |
|---|---|---|
| All’invio | La consegna è in attesa. | La consegna è in attesa. |
| Dopo 35 secondi | Il pannello indica già “scaduta”. | Il callback può ancora essere valido. |
| Conseguenza | L’operatrice vede una scadenza prematura. | Occorre correggere il comportamento visibile. |

**Da ricordare:** Il caso richiede prima una fonte affidabile, poi una modifica coerente del software.

A 35 secondi le due regole producono stati diversi: per questo il cambiamento interessa una persona e non soltanto un numero nel codice. La rettifica non è ancora stata esaminata: questa è un’anticipazione del problema, non l’autorizzazione a modificare il timeout.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
A 35 secondi le due regole producono stati diversi: per questo il cambiamento interessa una persona e non soltanto un numero nel codice. La rettifica non è ancora stata esaminata: questa è un’anticipazione del problema, non l’autorizzazione a modificare il timeout.

### Visual content
Tabella con intestazione e tutte le celle esattamente come in Learner content. Lettura per righe, da sinistra a destra; non sostituire le spiegazioni con icone.

### Transition
Il percorso continua con «Il percorso del corso»: distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S05
Module: M1
Objective: O1
Role: orientation
Title: Il percorso del corso
Value contribution: Distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Learner content
Seguiremo sempre Orione. Ogni modulo risolve un pezzo della stessa storia e termina con una domanda e una risposta commentata.

**M1** — Ritrovare il motivo dei 30 secondi
**M2** — Collegare la risposta al manuale
**M3** — Risolvere il contrasto fra 30 e 45
**M4** — Definire beneficio e livello di lavoro
**M5** — Progettare, verificare e chiudere
**M6** — Passare il fatto dalla KB allo sviluppo
**M7** — Riusare il lavoro senza fidarsi alla cieca

**Da ricordare:** Non serve conoscere già le skill. I termini tecnici vengono spiegati quando entrano nel caso.

Prima impariamo a trovare e valutare il fatto, poi a usarlo nel lavoro software. Invertire l’ordine significherebbe progettare un comportamento sulla base di una regola non ancora confermata. Le domande servono a individuare quale passaggio rileggere, non a dare un voto.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Prima impariamo a trovare e valutare il fatto, poi a usarlo nel lavoro software. Invertire l’ordine significherebbe progettare un comportamento sulla base di una regola non ancora confermata. Le domande servono a individuare quale passaggio rileggere, non a dare un voto.

### Visual content
Composizione testuale: titolo, introduzione, esempio o domanda e conclusione nell’ordine riportato in Learner content. Usare un riquadro per la citazione o domanda, se presente. Non occorrono immagini esterne: il contenuto da comprendere è interamente scritto.

### Transition
Il percorso continua con «Lunedì la scelta è chiara. Venerdì va ritrovata»: distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S06
Module: M1
Objective: O1
Role: explanation
Title: Lunedì la scelta è chiara. Venerdì va ritrovata
Value contribution: Distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Learner content
Lunedì l’agente legge il manuale e aiuta a scegliere 30 secondi. Venerdì una nuova sessione riceve la domanda: “Perché proprio 30?”.

**Se resta soltanto nella chat** — Il codice conserva il numero. La nuova sessione può dover recuperare il manuale e ricostruire il ragionamento della scelta.

**Se resta nel progetto** — Una nota conserva motivo e fonte. La nuova sessione può riaprire la nota e controllare il passaggio del manuale a cui rimanda.

**Da ricordare:** Il contesto è ciò che l’agente può usare ora. I file persistenti permettono di recuperare il lavoro precedente.

Una nota ben scritta può già evitare la ricostruzione: questo beneficio non appartiene esclusivamente alle skill. La distinzione è fra ciò che è disponibile nella conversazione corrente e ciò che viene reso recuperabile nel progetto. Anche un file persistente può essere sbagliato o superato.

### Complete explanation
Una nota ben scritta può già evitare la ricostruzione: questo beneficio non appartiene esclusivamente alle skill. La distinzione è fra ciò che è disponibile nella conversazione corrente e ciò che viene reso recuperabile nel progetto. Anche un file persistente può essere sbagliato o superato.

### Visual content
Due riquadri affiancati: il primo è il blocco «Se resta soltanto nella chat», il secondo «Se resta nel progetto». Riportare integralmente i rispettivi testi. Introduzione sopra, conclusione e precisazioni sotto. Nessuna freccia di causalità aggiuntiva.

### Transition
Il percorso continua con «Le istruzioni e i risultati stanno in posti diversi»: distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S07
Module: M1
Objective: O1
Role: explanation
Title: Le istruzioni e i risultati stanno in posti diversi
Value contribution: Distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Learner content
Installare una skill dà un metodo all’agente. La continuità del progetto dipende anche dai file che quel metodo fa conservare.

**Nell’ambiente dell’agente** — Le skill installate Descrivono come raccogliere fonti, analizzare una modifica e verificarne il risultato.

**Nella cartella di Orione** — La memoria del progetto ai_docs/ può contenere fonti, Vision, analisi, decisioni, guide e indici consultabili.

**Da ricordare:** La sessione successiva deve poter accedere alla stessa cartella. Una cartella nuova non contiene automaticamente la storia.

La skill contiene istruzioni riutilizzabili, mentre la cartella conserva i risultati specifici di Orione. Reinstallare le istruzioni non ricrea fonti o decisioni perdute. Per recuperare una ragione occorrono sia accesso ai file sia un percorso per trovare il punto pertinente.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
La skill contiene istruzioni riutilizzabili, mentre la cartella conserva i risultati specifici di Orione. Reinstallare le istruzioni non ricrea fonti o decisioni perdute. Per recuperare una ragione occorrono sia accesso ai file sia un percorso per trovare il punto pertinente.

### Visual content
Due riquadri affiancati: il primo è il blocco «Nell’ambiente dell’agente», il secondo «Nella cartella di Orione». Riportare integralmente i rispettivi testi. Introduzione sopra, conclusione e precisazioni sotto. Nessuna freccia di causalità aggiuntiva.

### Transition
Il percorso continua con «“Prendi delle note” può già bastare»: distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S08
Module: M1
Objective: O1
Role: explanation
Title: “Prendi delle note” può già bastare
Value contribution: Distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Learner content
Confrontiamo due scelte legittime nello stesso caso inventato: venerdì vogliamo ritrovare il motivo dei 30 secondi.

**Note richieste bene** — Salva la decisione e il motivo, con manuale, release e passaggio citato. Se il caso è singolo e la fonte resta stabile, questa nota può bastare a riaprire il ragionamento.

**Protocollo riutilizzabile** — Specifica anche dove cercare, quando verificare e come aggiornare ciò che dipende dalla fonte. Queste istruzioni diventano utili quando il controllo va ripetuto fra fonti, modifiche o persone diverse.

**Da ricordare:** La skill non aggiunge una facoltà magica di ricordare. Rende esplicito e riutilizzabile un modo di lavorare.

Il confronto corretto non oppone una buona skill a un agente incapace. Un agente può scrivere ottime note; una persona può dare da sola istruzioni equivalenti. La scelta riguarda il costo di ricostruire e mantenere quelle istruzioni, rispetto alla complessità del lavoro.

### Complete explanation
Il confronto corretto non oppone una buona skill a un agente incapace. Un agente può scrivere ottime note; una persona può dare da sola istruzioni equivalenti. La scelta riguarda il costo di ricostruire e mantenere quelle istruzioni, rispetto alla complessità del lavoro.

### Visual content
Due riquadri affiancati: il primo è il blocco «Note richieste bene», il secondo «Protocollo riutilizzabile». Riportare integralmente i rispettivi testi. Introduzione sopra, conclusione e precisazioni sotto. Nessuna freccia di causalità aggiuntiva.

### Transition
Il percorso continua con «La differenza si cerca in obblighi osservabili»: distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S09
Module: M1
Objective: O1
Role: explanation
Title: La differenza si cerca in obblighi osservabili
Value contribution: Distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Learner content
Una richiesta generica lascia aperte alcune decisioni. Una richiesta dettagliata può colmarle anche senza installare una skill.

| Domanda | “Prendi note” non precisa | Il protocollo specifica |
|---|---|---|
| Da dove viene la regola? | Dati minimi di provenienza. | Fonte, ambito e locatore del claim. |
| Una fonte la smentisce? | Quando e come riesaminare. | Conflitto visibile e nuova evidenza per risolverlo. |
| La regola cambia il software? | Quali superfici e prove considerare. | Design, rischi e verifiche prima della chiusura. |

**Da ricordare:** Osserva gli artefatti e le verifiche prodotti. La presenza della skill non dimostra che l’agente abbia rispettato le istruzioni.

Qui “obbligo” significa requisito del protocollo, non blocco tecnico inevitabile. Alcuni controlli automatici possono segnalare mancanze strutturali; il merito delle fonti e del ragionamento richiede review. Se il risultato omette un passaggio, il difetto va corretto anche se la skill è stata caricata.

### Complete explanation
Qui “obbligo” significa requisito del protocollo, non blocco tecnico inevitabile. Alcuni controlli automatici possono segnalare mancanze strutturali; il merito delle fonti e del ragionamento richiede review. Se il risultato omette un passaggio, il difetto va corretto anche se la skill è stata caricata.

### Visual content
Tabella con intestazione e tutte le celle esattamente come in Learner content. Lettura per righe, da sinistra a destra; non sostituire le spiegazioni con icone.

### Transition
Il percorso continua con «Come si ritrova una decisione»: distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S10
Module: M1
Objective: O1
Role: explanation
Title: Come si ritrova una decisione
Value contribution: Distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Learner content
Alla domanda “Perché 30 secondi?”, l’agente cerca solo i documenti pertinenti. Non occorre caricare tutto il progetto nella conversazione.

1. **1. L’indice indica la nota** — La voce sul timeout rimanda alla decisione che riguarda il callback.
2. **2. La nota spiega la scelta** — “Abbiamo usato 30 secondi perché il Manuale 2.1 indica questa finestra.”
3. **3. Il riferimento riapre la fonte** — L’agente controlla §4.3, pagina 48, e verifica che la release sia quella richiesta.

**Da ricordare:** Anche un agente senza queste skill può scrivere note. Le skill rendono ripetibile il modo di conservarle e verificarle.

L’indice riduce la ricerca, ma la nota non sostituisce la fonte quando la risposta dipende da essa. Si apre progressivamente ciò che serve alla domanda. Questa strategia evita di confondere la disponibilità dell’archivio con la presenza dell’intero archivio nella finestra di contesto.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
L’indice riduce la ricerca, ma la nota non sostituisce la fonte quando la risposta dipende da essa. Si apre progressivamente ciò che serve alla domanda. Questa strategia evita di confondere la disponibilità dell’archivio con la presenza dell’intero archivio nella finestra di contesto.

### Visual content
Sequenza numerata in ordine di lettura con tutti i titoli e testi riportati in Learner content. La numerazione esprime ordine del ragionamento, non una misura di tempo. Introduzione e conclusione restano visibili.

### Transition
Il percorso continua con «Prova M1: il numero non spiega il motivo»: distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S11
Module: M1
Objective: O1
Role: check
Title: Prova M1: il numero non spiega il motivo
Value contribution: Distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.
Solution: S12

### Learner content
Una nuova chat trova timeout = 30 nel codice. Un collega dice: “L’agente ricorderà perché”.

**Che cosa deve recuperare prima di spiegare quella scelta?**

- Indica dove cercare il motivo e come verificarlo.
- La soluzione è nella slide successiva.

Rispondi prima di leggere la soluzione. Il numero mostra il comportamento configurato, ma non specifica quale documento e quale decisione lo giustificano. La verifica chiede di descrivere il recupero, senza creare file o supporre che l’agente ricordi una sessione precedente.

### Complete explanation
Rispondi prima di leggere la soluzione. Il numero mostra il comportamento configurato, ma non specifica quale documento e quale decisione lo giustificano. La verifica chiede di descrivere il recupero, senza creare file o supporre che l’agente ricordi una sessione precedente.

### Visual content
Composizione testuale: titolo, introduzione, esempio o domanda e conclusione nell’ordine riportato in Learner content. Usare un riquadro per la citazione o domanda, se presente. Non occorrono immagini esterne: il contenuto da comprendere è interamente scritto.

### Transition
Il percorso continua con «Soluzione M1: recuperare motivo e fonte»: distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S12
Module: M1
Objective: O1
Role: solution
Title: Soluzione M1: recuperare motivo e fonte
Value contribution: Distinguere recupero di una ragione, istruzioni riutilizzabili e semplice accumulo di note.

### Learner content
Il valore nel codice prova quale tempo usa il software. Da solo non prova perché il team lo abbia scelto.

1. **Cercare la decisione** — L’indice del progetto porta alla nota sul timeout.
2. **Controllare la ragione** — La nota collega la scelta al Manuale Orione 2.1, §4.3, p. 48.
3. **Dichiarare un’eventuale lacuna** — Se nota o fonte mancano, l’agente deve dirlo e chiedere ciò che serve.

**Da ricordare:** Se hai risposto “ricorda la vecchia chat”, rivedi la distinzione fra contesto corrente e file persistenti.

La risposta è completa quando collega numero, motivo, fonte e percorso di ricerca. Se dici soltanto “salvare tutto”, manca il modo di selezionare ciò che serve; se dici “lo ricorderà”, manca il supporto persistente. Rileggi le slide su istruzioni, risultati e consultazione.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
La risposta è completa quando collega numero, motivo, fonte e percorso di ricerca. Se dici soltanto “salvare tutto”, manca il modo di selezionare ciò che serve; se dici “lo ricorderà”, manca il supporto persistente. Rileggi le slide su istruzioni, risultati e consultazione. La risposta e il percorso di correzione sono interamente nel testo visibile; nessuna spiegazione orale è necessaria per usarli.

### Visual content
Sequenza numerata in ordine di lettura con tutti i titoli e testi riportati in Learner content. La numerazione esprime ordine del ragionamento, non una misura di tempo. Introduzione e conclusione restano visibili.

### Transition
Il percorso continua con «Un manuale lungo entra nella KB per parti»: rendere una risposta verificabile risalendo a fonte, passaggio e ambito.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S13
Module: M2
Objective: O2
Role: explanation
Title: Un manuale lungo entra nella KB per parti
Value contribution: Rendere una risposta verificabile risalendo a fonte, passaggio e ambito.

### Learner content
Arriva un manuale di 200 pagine. Per poter verificare una risposta futura, kb-agentic conserva la fonte prima di organizzare ciò che ne ricava.

**Fonte conservata** — Documento identificabile e riapribile Si registra la provenienza. Per un PDF può servire un’estrazione testuale stabile con riferimento all’originale.

**Lettura dichiarata** — Le pagine lette restano distinguibili Se l’agente ha esaminato soltanto le prime 30 pagine, registra quel limite e continua per finestre successive.

**Da ricordare:** Conservare tutto il file non significa averlo letto tutto. Questa distinzione evita risposte troppo sicure.

Conservare la fonte permette di riaprire il passaggio originale. Lavorarla per sezioni evita che il riassunto cancelli condizioni presenti altrove. “Per parti” non significa estrarre una frase isolata senza contesto: l’ambito di validità deve accompagnare ciò che viene ricavato.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Conservare la fonte permette di riaprire il passaggio originale. Lavorarla per sezioni evita che il riassunto cancelli condizioni presenti altrove. “Per parti” non significa estrarre una frase isolata senza contesto: l’ambito di validità deve accompagnare ciò che viene ricavato.

### Visual content
Due riquadri affiancati: il primo è il blocco «Fonte conservata», il secondo «Lettura dichiarata». Riportare integralmente i rispettivi testi. Introduzione sopra, conclusione e precisazioni sotto. Nessuna freccia di causalità aggiuntiva.

### Transition
Il percorso continua con «Un claim è un’affermazione controllabile»: rendere una risposta verificabile risalendo a fonte, passaggio e ambito.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S14
Module: M2
Objective: O2
Role: explanation
Title: Un claim è un’affermazione controllabile
Value contribution: Rendere una risposta verificabile risalendo a fonte, passaggio e ambito.

### Learner content
Dal manuale si estrae una frase precisa. Il claim conserva anche l’ambito in cui vale e il punto della fonte che permette di verificarla.

| Campo | Esempio di claim |
|---|---|
| Affermazione | Il callback resta valido per 30 secondi dall’invio. |
| Ambito | Release 2.1 di Orione. Nessuna estensione ad altre versioni. |
| Fonte e locatore | Manuale Callback Orione 2.1, §4.3, pagina 48. |

**Da ricordare:** Il locatore indica dove riaprire il passaggio. Nella KB reale va misurato sulla fonte conservata, mai inventato.

Un claim separa una singola affermazione dalle altre per poterla controllare e aggiornare. Il locatore permette di tornare al punto preciso della fonte, mentre release e condizioni impediscono di usarla fuori ambito. Un’affermazione plausibile senza provenienza resta insufficiente per questa risposta.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Un claim separa una singola affermazione dalle altre per poterla controllare e aggiornare. Il locatore permette di tornare al punto preciso della fonte, mentre release e condizioni impediscono di usarla fuori ambito. Un’affermazione plausibile senza provenienza resta insufficiente per questa risposta.

### Visual content
Tabella con intestazione e tutte le celle esattamente come in Learner content. Lettura per righe, da sinistra a destra; non sostituire le spiegazioni con icone.

### Transition
Il percorso continua con «Il grafo aiuta a trovare il claim giusto»: rendere una risposta verificabile risalendo a fonte, passaggio e ambito.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S15
Module: M2
Objective: O2
Role: explanation
Title: Il grafo aiuta a trovare il claim giusto
Value contribution: Rendere una risposta verificabile risalendo a fonte, passaggio e ambito.

### Learner content
Un grafo è un insieme di temi collegati. Il grafo della KB organizza le informazioni del progetto per rendere la ricerca mirata.

**Grafo della KB di Orione** — Domanda: “Quando scade il callback?” Il tema “callback” porta ai claim sui tempi e alle relative fonti. Il tema “autenticazione” riguarda altre domande.

**Grafo dei prerequisiti del corso** — Domanda: “Che cosa devo capire prima?” Per capire una risposta rintracciabile, prima impari che cosa sono una fonte conservata e un claim.

**Da ricordare:** Il primo grafo serve a recuperare conoscenza. Il secondo serve a ordinare l’apprendimento.

Il grafo degli argomenti risponde a “dove trovo ciò che sappiamo sul timeout?”. Non coincide con il grafo didattico che ordina i prerequisiti del corso. Il collegamento ai claim consente di arrivare alle fonti senza trattare una categoria del grafo come prova del fatto.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Il grafo degli argomenti risponde a “dove trovo ciò che sappiamo sul timeout?”. Non coincide con il grafo didattico che ordina i prerequisiti del corso. Il collegamento ai claim consente di arrivare alle fonti senza trattare una categoria del grafo come prova del fatto.

### Visual content
Due riquadri affiancati: il primo è il blocco «Grafo della KB di Orione», il secondo «Grafo dei prerequisiti del corso». Riportare integralmente i rispettivi testi. Introduzione sopra, conclusione e precisazioni sotto. Nessuna freccia di causalità aggiuntiva.

### Transition
Il percorso continua con «Una risposta che puoi controllare»: rendere una risposta verificabile risalendo a fonte, passaggio e ambito.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S16
Module: M2
Objective: O2
Role: explanation
Title: Una risposta che puoi controllare
Value contribution: Rendere una risposta verificabile risalendo a fonte, passaggio e ambito.

### Learner content
A questo punto della storia l’agente conosce il manuale, ma non ha ancora verificato eventuali rettifiche.

**Risposta dell’agente**

> “Per la release 2.1, il Manuale Callback Orione indica 30 secondi dall’invio (§4.3, p. 48). Non ho verificato altre versioni o rettifiche.”

La frase dichiara quale versione descrive, dove controllare il numero e che cosa resta incerto.

**Da ricordare:** Il riferimento consente di verificare ciò che la fonte dice. Non garantisce che la fonte sia corretta.

La risposta contiene una conclusione e la strada per controllarla. La citazione non rende vero un errore: bisogna verificare che il passaggio citato sostenga proprio la regola e l’ambito dichiarati. L’esempio mostra la forma della risposta, non un documento reale da applicare.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
La risposta contiene una conclusione e la strada per controllarla. La citazione non rende vero un errore: bisogna verificare che il passaggio citato sostenga proprio la regola e l’ambito dichiarati. L’esempio mostra la forma della risposta, non un documento reale da applicare.

### Visual content
Composizione testuale: titolo, introduzione, esempio o domanda e conclusione nell’ordine riportato in Learner content. Usare un riquadro per la citazione o domanda, se presente. Non occorrono immagini esterne: il contenuto da comprendere è interamente scritto.

### Transition
Il percorso continua con «Prova M2: una risposta senza provenienza»: rendere una risposta verificabile risalendo a fonte, passaggio e ambito.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S17
Module: M2
Objective: O2
Role: check
Title: Prova M2: una risposta senza provenienza
Value contribution: Rendere una risposta verificabile risalendo a fonte, passaggio e ambito.
Solution: S18

### Learner content
L’agente risponde soltanto “30 secondi”. Non sa dire quale versione o passaggio abbia letto.

**Quali passaggi mancano per rendere la risposta verificabile?**

- Parti dal file ricevuto e arriva alla risposta.
- Spiega anche il ruolo del grafo della KB.

Prima della soluzione, indica quale parte della risposta non si può controllare. Aggiungere soltanto un nome generico del manuale non risolve il problema: una revisione diversa potrebbe contenere un’altra regola. Non è necessario produrre un registro, basta spiegare il percorso.

### Complete explanation
Prima della soluzione, indica quale parte della risposta non si può controllare. Aggiungere soltanto un nome generico del manuale non risolve il problema: una revisione diversa potrebbe contenere un’altra regola. Non è necessario produrre un registro, basta spiegare il percorso.

### Visual content
Composizione testuale: titolo, introduzione, esempio o domanda e conclusione nell’ordine riportato in Learner content. Usare un riquadro per la citazione o domanda, se presente. Non occorrono immagini esterne: il contenuto da comprendere è interamente scritto.

### Transition
Il percorso continua con «Soluzione M2: il percorso deve restare riapribile»: rendere una risposta verificabile risalendo a fonte, passaggio e ambito.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S18
Module: M2
Objective: O2
Role: solution
Title: Soluzione M2: il percorso deve restare riapribile
Value contribution: Rendere una risposta verificabile risalendo a fonte, passaggio e ambito.

### Learner content
Ogni passaggio lascia un riferimento al precedente. Così un’altra sessione può controllare il risultato senza fidarsi del solo riassunto.

| Passaggio | Che cosa deve esserci |
|---|---|
| 1. Fonte | Il manuale conservato con versione e provenienza. |
| 2. Claim | La regola sui 30 secondi, l’ambito e il locatore §4.3, p. 48. |
| 3. Tema nella KB | Il tema “callback” collega la domanda al claim pertinente. |
| 4. Risposta | Il numero con citazione e limite sulle rettifiche non verificate. |

**Da ricordare:** Se hai confuso il file con il claim, torna all’esempio dei campi del claim.

Fonte conservata, locatore e ambito risolvono tre dubbi diversi: dove riapro il documento, quale passaggio sostiene la frase e a quali condizioni vale. Se manca uno dei tre, torna all’esempio del claim e ricostruisci la risposta citando quei dati.

### Complete explanation
Fonte conservata, locatore e ambito risolvono tre dubbi diversi: dove riapro il documento, quale passaggio sostiene la frase e a quali condizioni vale. Se manca uno dei tre, torna all’esempio del claim e ricostruisci la risposta citando quei dati. La risposta e il percorso di correzione sono interamente nel testo visibile; nessuna spiegazione orale è necessaria per usarli.

### Visual content
Tabella con intestazione e tutte le celle esattamente come in Learner content. Lettura per righe, da sinistra a destra; non sostituire le spiegazioni con icone.

### Transition
Il percorso continua con «Due fonti incompatibili sulla stessa release»: decidere se due regole confliggono e quale informazione permette di aggiornarle.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S19
Module: M3
Objective: O3
Role: explanation
Title: Due fonti incompatibili sulla stessa release
Value contribution: Decidere se due regole confliggono e quale informazione permette di aggiornarle.

### Learner content
Arriva una seconda fonte. Entrambe parlano della release 2.1, della stessa finestra e dello stesso istante iniziale.

**Manuale 2.1, §4.3, p. 48** — 30 secondi dall’invio È la fonte che ha sostenuto la decisione precedente.

**Scheda 2.1, §2.1** — 45 secondi dall’invio La scheda arriva più tardi, ma questo non dimostra che sia corretta.

**Da ricordare:** La KB conserva entrambi i riferimenti e dichiara il conflitto. Serve un fatto nuovo prima di dare un timeout affidabile.

Due numeri diversi non dimostrano da soli una contraddizione: devono descrivere la stessa cosa nelle stesse condizioni. Quando invece l’ambito coincide, scegliere quello più recente senza una ragione può nascondere il conflitto. Entrambe le evidenze restano visibili finché viene chiarito.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Due numeri diversi non dimostrano da soli una contraddizione: devono descrivere la stessa cosa nelle stesse condizioni. Quando invece l’ambito coincide, scegliere quello più recente senza una ragione può nascondere il conflitto. Entrambe le evidenze restano visibili finché viene chiarito.

### Visual content
Due riquadri affiancati: il primo è il blocco «Manuale 2.1, §4.3, p. 48», il secondo «Scheda 2.1, §2.1». Riportare integralmente i rispettivi testi. Introduzione sopra, conclusione e precisazioni sotto. Nessuna freccia di causalità aggiuntiva.

### Transition
Il percorso continua con «Periodi diversi possono rendere compatibili due regole»: decidere se due regole confliggono e quale informazione permette di aggiornarle.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S20
Module: M3
Objective: O3
Role: explanation
Title: Periodi diversi possono rendere compatibili due regole
Value contribution: Decidere se due regole confliggono e quale informazione permette di aggiornarle.

### Learner content
Proviamo una variante: il manuale vale fino a giugno e la scheda da luglio. I numeri diversi, in questo caso, non bastano a creare un conflitto.

| Regola | Ambito | Che cosa conclude la KB |
|---|---|---|
| 30 secondi | Fino a giugno | Può valere insieme alla regola successiva. |
| 45 secondi | Da luglio | Si applica al periodo successivo. |
| Domanda senza data | Periodo non specificato | Serve la data, oppure una risposta che dichiari il limite. |

**Da ricordare:** Prima di confrontare due affermazioni, si controllano soggetto, versione, condizioni e periodo di validità.

Una regola può essere vera fino a giugno e un’altra da luglio senza che una smentisca l’altra. Il periodo è parte dell’affermazione, non una nota decorativa. Prima di contestare due claim, confronta oggetto, release, periodo e condizioni a cui si riferiscono.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Una regola può essere vera fino a giugno e un’altra da luglio senza che una smentisca l’altra. Il periodo è parte dell’affermazione, non una nota decorativa. Prima di contestare due claim, confronta oggetto, release, periodo e condizioni a cui si riferiscono.

### Visual content
Tabella con intestazione e tutte le celle esattamente come in Learner content. Lettura per righe, da sinistra a destra; non sostituire le spiegazioni con icone.

### Transition
Il percorso continua con «La rettifica spiega perché ora vale 45»: decidere se due regole confliggono e quale informazione permette di aggiornarle.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S21
Module: M3
Objective: O3
Role: explanation
Title: La rettifica spiega perché ora vale 45
Value contribution: Decidere se due regole confliggono e quale informazione permette di aggiornarle.

### Learner content
Nel caso originale il contrasto riguarda la stessa release. Una terza fonte chiarisce espressamente l’errore del manuale.

**Rettifica Orione 2.1, §1, p. 2**

> “La finestra di 30 secondi indicata nel Manuale §4.3 è errata. Per la release 2.1 è 45 secondi dall’invio.”

Il nuovo claim rimanda alla rettifica. Il claim dei 30 secondi resta nella storia con il riferimento che lo ha superato.

**Da ricordare:** Ora si può motivare la correzione. La preferenza dell’agente o l’ordine di arrivo dei file non sarebbero bastati.

La nuova informazione utile è che la rettifica dichiara quale passaggio precedente corregge e per quale release. Non basta il numero 45 o la data del file. Si conserva la storia della sostituzione per capire perché una vecchia decisione era ragionevole e perché ora va riesaminata.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
La nuova informazione utile è che la rettifica dichiara quale passaggio precedente corregge e per quale release. Non basta il numero 45 o la data del file. Si conserva la storia della sostituzione per capire perché una vecchia decisione era ragionevole e perché ora va riesaminata.

### Visual content
Composizione testuale: titolo, introduzione, esempio o domanda e conclusione nell’ordine riportato in Learner content. Usare un riquadro per la citazione o domanda, se presente. Non occorrono immagini esterne: il contenuto da comprendere è interamente scritto.

### Transition
Il percorso continua con «La correzione deve raggiungere le vecchie decisioni»: decidere se due regole confliggono e quale informazione permette di aggiornarle.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S22
Module: M3
Objective: O3
Role: explanation
Title: La correzione deve raggiungere le vecchie decisioni
Value contribution: Decidere se due regole confliggono e quale informazione permette di aggiornarle.

### Learner content
Aggiornare il claim non aggiorna automaticamente il software. Occorre riesaminare ciò che dipendeva dalla vecchia regola.

1. **Ritrovare i riferimenti ai 30 secondi** — La vecchia decisione sul timeout rimanda al claim superato.
2. **Riesaminare documenti e guide** — Le istruzioni che usano quella regola potrebbero essere ormai obsolete.
3. **Aprire la domanda sul software** — Il team deve valutare come adeguare Orione e quali effetti verificare.

**Da ricordare:** La KB chiarisce il fatto. Il percorso SDLC governa il cambiamento che il team decide di fare.

Aggiornare la fonte non cambia automaticamente il software o le note che l’hanno usata. Il legame fra claim e decisioni consente di trovare ciò che potrebbe essere diventato obsoleto. La revisione segue quei legami e distingue “da riesaminare” da “già corretto e verificato”.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Aggiornare la fonte non cambia automaticamente il software o le note che l’hanno usata. Il legame fra claim e decisioni consente di trovare ciò che potrebbe essere diventato obsoleto. La revisione segue quei legami e distingue “da riesaminare” da “già corretto e verificato”.

### Visual content
Sequenza numerata in ordine di lettura con tutti i titoli e testi riportati in Learner content. La numerazione esprime ordine del ragionamento, non una misura di tempo. Introduzione e conclusione restano visibili.

### Transition
Il percorso continua con «Prova M3: quali regole si contraddicono?»: decidere se due regole confliggono e quale informazione permette di aggiornarle.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S23
Module: M3
Objective: O3
Role: check
Title: Prova M3: quali regole si contraddicono?
Value contribution: Decidere se due regole confliggono e quale informazione permette di aggiornarle.
Solution: S24

### Learner content
A dice “30 secondi fino a giugno”. B dice “45 secondi da luglio”. C dice “30 secondi per luglio”, senza specificare la versione.

**Quale coppia può coesistere? Quale richiede un controllo?**

- Indica quale informazione manca prima di scegliere.
- Non usare la data di arrivo del documento come criterio.

Confronta le coppie A–B e B–C ed esplicita l’ambito prima di scegliere un esito. Una risposta come “vince l’ultimo documento” non dimostra comprensione, perché non spiega se le regole competono davvero né quale nuova evidenza autorizzi la sostituzione.

### Complete explanation
Confronta le coppie A–B e B–C ed esplicita l’ambito prima di scegliere un esito. Una risposta come “vince l’ultimo documento” non dimostra comprensione, perché non spiega se le regole competono davvero né quale nuova evidenza autorizzi la sostituzione.

### Visual content
Composizione testuale: titolo, introduzione, esempio o domanda e conclusione nell’ordine riportato in Learner content. Usare un riquadro per la citazione o domanda, se presente. Non occorrono immagini esterne: il contenuto da comprendere è interamente scritto.

### Transition
Il percorso continua con «Soluzione M3: l’ambito decide il confronto»: decidere se due regole confliggono e quale informazione permette di aggiornarle.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S24
Module: M3
Objective: O3
Role: solution
Title: Soluzione M3: l’ambito decide il confronto
Value contribution: Decidere se due regole confliggono e quale informazione permette di aggiornarle.

### Learner content
Due numeri diversi diventano un conflitto solo quando si riferiscono allo stesso fatto nelle stesse condizioni.

**A e B possono coesistere** — I periodi non si sovrappongono. 30 vale fino a giugno e 45 da luglio. Una risposta deve indicare il periodo a cui si riferisce.

**B e C richiedono un controllo** — Entrambi parlano di luglio. Occorre verificare release e condizioni di C. Se coincidono con B, i 30 e i 45 secondi sono incompatibili.

**Da ricordare:** Se hai scelto subito il documento più recente, torna alla differenza fra data di arrivo e ambito di validità.

L’esito dipende dall’ambito e dalla nuova informazione, non dall’ordine in cui hai letto i file. Se hai confuso successione temporale e contraddizione, rileggi il confronto giugno/luglio. Se hai scelto una regola senza prova, rileggi il ruolo della rettifica.

### Complete explanation
L’esito dipende dall’ambito e dalla nuova informazione, non dall’ordine in cui hai letto i file. Se hai confuso successione temporale e contraddizione, rileggi il confronto giugno/luglio. Se hai scelto una regola senza prova, rileggi il ruolo della rettifica. La risposta e il percorso di correzione sono interamente nel testo visibile; nessuna spiegazione orale è necessaria per usarli.

### Visual content
Due riquadri affiancati: il primo è il blocco «A e B possono coesistere», il secondo «B e C richiedono un controllo». Riportare integralmente i rispettivi testi. Introduzione sopra, conclusione e precisazioni sotto. Nessuna freccia di causalità aggiuntiva.

### Transition
Il percorso continua con «La Vision conserva il beneficio della modifica»: collegare il lavoro richiesto a beneficio, confini e rischio.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S25
Module: M4
Objective: O4
Role: explanation
Title: La Vision conserva il beneficio della modifica
Value contribution: Collegare il lavoro richiesto a beneficio, confini e rischio.

### Learner content
La Vision registra destinatari, beneficio e confini. Serve a decidere che cosa includere nel lavoro e a giudicare il risultato.

**Esempio di obiettivo per Orione**

> “L’operatrice deve vedere uno stato attendibile della consegna, senza considerarla scaduta mentre il callback è ancora valido.”

Il timer a 45 secondi è un mezzo. Se una notifica continua ad annunciare la scadenza a 30, il beneficio non è ancora arrivato.

**Da ricordare:** Un’aggiunta fuori dai confini concordati va discussa con la persona responsabile.

Il beneficio nomina ciò che deve migliorare per l’operatrice: uno stato attendibile mentre aspetta la consegna. Il confine evita di trasformare una correzione del timeout nella riprogettazione dell’intero servizio. La persona approva quel risultato; il numero nel manuale non sostituisce la scelta.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Il beneficio nomina ciò che deve migliorare per l’operatrice: uno stato attendibile mentre aspetta la consegna. Il confine evita di trasformare una correzione del timeout nella riprogettazione dell’intero servizio. La persona approva quel risultato; il numero nel manuale non sostituisce la scelta.

### Visual content
Composizione testuale: titolo, introduzione, esempio o domanda e conclusione nell’ordine riportato in Learner content. Usare un riquadro per la citazione o domanda, se presente. Non occorrono immagini esterne: il contenuto da comprendere è interamente scritto.

### Transition
Il percorso continua con «Il triage sceglie quanto lavoro serve»: collegare il lavoro richiesto a beneficio, confini e rischio.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-7

## S26
Module: M4
Objective: O4
Role: explanation
Title: Il triage sceglie quanto lavoro serve
Value contribution: Collegare il lavoro richiesto a beneficio, confini e rischio.

### Learner content
Il triage classifica una modifica in base al rischio e al comportamento coinvolto. Il numero di righe da editare non basta.

| Livello | Quando si usa | Lavoro proporzionato |
|---|---|---|
| L1 | Refuso o correzione banale senza cambio di comportamento. | Correzione e controllo pertinente. |
| L2 | Intervento locale, causa chiara e rischio basso. | Mini-analisi, modifica e test. |
| L3 | Comportamento visibile, contratti o design significativo. | Vision, analisi, piano, review e chiusura. |
| Spike | Manca conoscenza per scegliere. | Studio limitato, poi nuova classificazione. |

**Da ricordare:** Orione è L3: cambiano il momento della scadenza e gli stati che l’utente percepisce.

Il livello proporziona il lavoro al rischio e al cambiamento. La dimensione del diff non basta: una riga può alterare una regola visibile a più attori. Se il fatto da usare è incerto, lo Spike studia il dubbio prima di fingere che il design sia già fondato.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Il livello proporziona il lavoro al rischio e al cambiamento. La dimensione del diff non basta: una riga può alterare una regola visibile a più attori. Se il fatto da usare è incerto, lo Spike studia il dubbio prima di fingere che il design sia già fondato.

### Visual content
Tabella con intestazione e tutte le celle esattamente come in Learner content. Lettura per righe, da sinistra a destra; non sostituire le spiegazioni con icone.

### Transition
Il percorso continua con «Prova M4: la stessa parola “correzione” può ingannare»: collegare il lavoro richiesto a beneficio, confini e rischio.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-7

## S27
Module: M4
Objective: O4
Role: check
Title: Prova M4: la stessa parola “correzione” può ingannare
Value contribution: Collegare il lavoro richiesto a beneficio, confini e rischio.
Solution: S28

### Learner content
Due ticket si chiamano «Correggere lo stato di consegna». Nel primo è scritto “consegna scadutaa”: l'indagine conferma che cambia soltanto quella stringa, senza logica, contratti o rischi ulteriori. Nel secondo lo stato passa a “scaduta” a 30 secondi: una rettifica valida indica 45. La modifica interessa pannello e notifica; non è ancora stabilito chi prevale fra callback e scadenza allo stesso istante.

Il beneficio concordato è mostrare all'operatrice uno stato attendibile. Un collega propone di approfittarne per ridisegnare tutta la navigazione.

**Prima di leggere la soluzione, decidi:** quale livello assegni ai due ticket e perché? Quale informazione manca al secondo? La navigazione rientra nel lavoro concordato? Se la rettifica fosse ancora contestata, quale passo cambierebbe?

Scrivi una breve motivazione per ogni scelta. Il caso è inventato; non occorre produrre documenti.

### Complete explanation
Due ticket si chiamano «Correggere lo stato di consegna». Nel primo è scritto “consegna scadutaa”: l'indagine conferma che cambia soltanto quella stringa, senza logica, contratti o rischi ulteriori. Nel secondo lo stato passa a “scaduta” a 30 secondi: una rettifica valida indica 45. La modifica interessa pannello e notifica; non è ancora stabilito chi prevale fra callback e scadenza allo stesso istante.

Il beneficio concordato è mostrare all'operatrice uno stato attendibile. Un collega propone di approfittarne per ridisegnare tutta la navigazione.

**Prima di leggere la soluzione, decidi:** quale livello assegni ai due ticket e perché? Quale informazione manca al secondo? La navigazione rientra nel lavoro concordato? Se la rettifica fosse ancora contestata, quale passo cambierebbe?

Scrivi una breve motivazione per ogni scelta. Il caso è inventato; non occorre produrre documenti.

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «Soluzione M4: si classifica l’effetto»: collegare il lavoro richiesto a beneficio, confini e rischio.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-7

## S28
Module: M4
Objective: O4
Role: solution
Title: Soluzione M4: si classifica l’effetto
Value contribution: Collegare il lavoro richiesto a beneficio, confini e rischio.

### Learner content
**Primo ticket: L1.** Abbiamo verificato che è un refuso isolato: correggere la stringa e controllarla basta. La conclusione dipende dall'indagine, non dal titolo del ticket.

**Secondo ticket: L3.** Cambiano un comportamento visibile e due superfici. Anche se bastasse editare una riga, bisogna progettare e verificare il risultato. La precedenza esatta al confine dei 45 secondi è ancora da chiarire: dichiararla aperta evita di inventare una regola.

**La Vision decide il confine.** Correggere pannello e notifica serve al beneficio concordato; ridisegnare la navigazione richiede una ragione e una decisione ulteriore con la persona responsabile. Non diventa necessario perché è comodo farlo nello stesso ticket.

**Se la rettifica è contestata**, non scegliamo 45 come fatto certo: uno Spike circoscritto può chiarire la regola; poi si riclassifica il lavoro di produzione. L2 richiede causa chiara e rischio basso entro i suoi limiti: non è una via intermedia da assegnare quando mancano informazioni.

Una risposta sufficiente collega livello agli effetti, nomina la decisione al confine e distingue il beneficio dall'ampliamento proposto. Se hai usato il numero di righe, rileggi S26; se hai incluso la navigazione senza motivarla, torna alla Vision in S25.

### Complete explanation
**Primo ticket: L1.** Abbiamo verificato che è un refuso isolato: correggere la stringa e controllarla basta. La conclusione dipende dall'indagine, non dal titolo del ticket.

**Secondo ticket: L3.** Cambiano un comportamento visibile e due superfici. Anche se bastasse editare una riga, bisogna progettare e verificare il risultato. La precedenza esatta al confine dei 45 secondi è ancora da chiarire: dichiararla aperta evita di inventare una regola.

**La Vision decide il confine.** Correggere pannello e notifica serve al beneficio concordato; ridisegnare la navigazione richiede una ragione e una decisione ulteriore con la persona responsabile. Non diventa necessario perché è comodo farlo nello stesso ticket.

**Se la rettifica è contestata**, non scegliamo 45 come fatto certo: uno Spike circoscritto può chiarire la regola; poi si riclassifica il lavoro di produzione. L2 richiede causa chiara e rischio basso entro i suoi limiti: non è una via intermedia da assegnare quando mancano informazioni.

Una risposta sufficiente collega livello agli effetti, nomina la decisione al confine e distingue il beneficio dall'ampliamento proposto. Se hai usato il numero di righe, rileggi S26; se hai incluso la navigazione senza motivarla, torna alla Vision in S25.

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «Use case: il bisogno prima della soluzione»: seguire un cambiamento fino alle superfici e alle prove del risultato.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-7

## S29
Module: M5
Objective: O5
Role: explanation
Title: Use case: il bisogno prima della soluzione
Value contribution: Seguire un cambiamento fino alle superfici e alle prove del risultato.

### Learner content
Uno use case (UC) descrive chi vuole ottenere quale risultato. Aiuta a vedere gli attori che una modifica potrebbe trascurare.

**Use case di Orione**

> “Quando consulta una consegna, l’operatrice può distinguere se è ancora in attesa oppure se è scaduta.”

Cambiare una costante non descrive questo bisogno. Il bisogno obbliga a verificare anche ciò che il pannello comunica.

**Da ricordare:** Il servizio esterno è un altro attore da considerare: anche il suo scambio di esiti fa parte del comportamento.

Lo use case parte dall’attore e dal risultato che gli serve. Questo impedisce di chiudere la discussione sulla sola modifica tecnica. Il servizio esterno conta perché invia la risposta e riceve un esito: anche il suo scambio può essere incoerente con il pannello.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Lo use case parte dall’attore e dal risultato che gli serve. Questo impedisce di chiudere la discussione sulla sola modifica tecnica. Il servizio esterno conta perché invia la risposta e riceve un esito: anche il suo scambio può essere incoerente con il pannello.

### Visual content
Composizione testuale: titolo, introduzione, esempio o domanda e conclusione nell’ordine riportato in Learner content. Usare un riquadro per la citazione o domanda, se presente. Non occorrono immagini esterne: il contenuto da comprendere è interamente scritto.

### Transition
Il percorso continua con «Functional Spec: regole che si possono verificare»: seguire un cambiamento fino alle superfici e alle prove del risultato.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S30
Module: M5
Objective: O5
Role: explanation
Title: Functional Spec: regole che si possono verificare
Value contribution: Seguire un cambiamento fino alle superfici e alle prove del risultato.

### Learner content
La specifica funzionale descrive che cosa deve accadere nei diversi casi. Componenti e file da modificare verranno scelti dopo.

| Caso di Orione | Comportamento da specificare |
|---|---|
| Prima di 45 secondi, nessun callback | La consegna non deve già apparire scaduta. |
| Scadenza raggiunta senza callback | La consegna passa a scaduta secondo la regola confermata. |
| Callback esattamente al confine | Va definita la precedenza fra risposta e scadenza. |
| Callback valido | Il sistema presenta l’esito previsto su tutte le superfici. |

**Da ricordare:** La fonte fissa la finestra. La persona responsabile deve confermare i casi di confine: non vanno indovinati.

La specifica rende discutibili e verificabili le regole prima di scegliere i file. Il confine esatto fra risposta e scadenza è un caso distinto: il manuale può non determinarne la precedenza. Scrivere un test con un’attesa arbitraria trasformerebbe una decisione mancante in un falso requisito.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
La specifica rende discutibili e verificabili le regole prima di scegliere i file. Il confine esatto fra risposta e scadenza è un caso distinto: il manuale può non determinarne la precedenza. Scrivere un test con un’attesa arbitraria trasformerebbe una decisione mancante in un falso requisito.

### Visual content
Tabella con intestazione e tutte le celle esattamente come in Learner content. Lettura per righe, da sinistra a destra; non sostituire le spiegazioni con icone.

### Transition
Il percorso continua con «Interface Contract: dove si vede la regola»: seguire un cambiamento fino alle superfici e alle prove del risultato.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S31
Module: M5
Objective: O5
Role: explanation
Title: Interface Contract: dove si vede la regola
Value contribution: Seguire un cambiamento fino alle superfici e alle prove del risultato.

### Learner content
Il contratto di interfaccia (IC) descrive azioni, risposte e stati percepiti da persone o servizi. Una “superficie” è uno di questi punti di interazione.

| Superficie | Che cosa seguire | Errore che si vuole evitare |
|---|---|---|
| Pannello | Invio, attesa, esito e scadenza. | Mostrare scaduto a 30 secondi. |
| Notifica, se presente | Quando parte e quale stato comunica. | Annunciare una scadenza prematura. |
| Servizio esterno | Messaggi di callback e risposta, inclusi gli errori. | Dare un esito incoerente con il pannello. |

**Da ricordare:** Lo stesso cambiamento va seguito dal trigger, cioè l’evento iniziale, fino al feedback che qualcuno riceve.

Seguire le superfici significa cercare dove il cambiamento viene percepito. Una notifica presente nel prodotto è parte del risultato quanto il pannello; una notifica inesistente non va inventata come requisito. Per ciascuna superficie si descrivono anche attesa, errore e feedback.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Seguire le superfici significa cercare dove il cambiamento viene percepito. Una notifica presente nel prodotto è parte del risultato quanto il pannello; una notifica inesistente non va inventata come requisito. Per ciascuna superficie si descrivono anche attesa, errore e feedback.

### Visual content
Tabella con intestazione e tutte le celle esattamente come in Learner content. Lettura per righe, da sinistra a destra; non sostituire le spiegazioni con icone.

### Transition
Il percorso continua con «Threat Model: rischi legati a una verifica»: seguire un cambiamento fino alle superfici e alle prove del risultato.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S32
Module: M5
Objective: O5
Role: explanation
Title: Threat Model: rischi legati a una verifica
Value contribution: Seguire un cambiamento fino alle superfici e alle prove del risultato.

### Learner content
Il modello delle minacce (TM) considera che cosa può andare storto. Il rischio deve riferirsi a un punto preciso e a un controllo possibile.

| Rischio del caso | Dove si manifesta | Verifica da progettare |
|---|---|---|
| Uno stato vecchio appare attuale. | Pannello. | Una prova segue gli aggiornamenti e controlla lo stato mostrato. |
| Una consegna già fallita resta in attesa. | Pannello o notifica. | Una prova controlla il feedback di errore e l’uscita dall’attesa. |
| Pannello e notifica danno esiti diversi. | Due superfici insieme. | La stessa sequenza viene verificata su entrambe. |

**Da ricordare:** Il controllo rende concreto il rischio. “Potrebbero esserci problemi” non dice che cosa verificare.

Un rischio utile identifica un esito sbagliato, il luogo in cui appare e una verifica capace di rilevarlo. Il test proposto deve osservare lo stato mostrato o comunicato, non soltanto confermare che una funzione è stata chiamata. I rischi restano ipotesi da verificare sul sistema reale.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Un rischio utile identifica un esito sbagliato, il luogo in cui appare e una verifica capace di rilevarlo. Il test proposto deve osservare lo stato mostrato o comunicato, non soltanto confermare che una funzione è stata chiamata. I rischi restano ipotesi da verificare sul sistema reale.

### Visual content
Tabella con intestazione e tutte le celle esattamente come in Learner content. Lettura per righe, da sinistra a destra; non sostituire le spiegazioni con icone.

### Transition
Il percorso continua con «Capability Ledger: che cosa sa già fare il sistema»: seguire un cambiamento fino alle superfici e alle prove del risultato.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S33
Module: M5
Objective: O5
Role: explanation
Title: Capability Ledger: che cosa sa già fare il sistema
Value contribution: Seguire un cambiamento fino alle superfici e alle prove del risultato.

### Learner content
Prima di scegliere quali parti modificare, cerchiamo ciò che esiste. Il **Capability Ledger** registra capacità, evidenza e conseguenza per il design.

**Indagine didattica inventata su Orione, ora completata:**

| Capacità cercata | Riscontro nel caso | Conseguenza |
|---|---|---|
| Calcolo condiviso della scadenza | La lettura del componente `ExpiryPolicy` e delle sue chiamate mostra un calcolo unico usato dal pannello. | Riutilizzarlo è una possibilità fondata. |
| Notifica coerente | La notifica confronta ancora il tempo con una regola locale di 30 secondi. | Cambiare soltanto il calcolo condiviso non corregge questa superficie. |
| Prove ai confini | I test disponibili controllano la costante, non il risultato su entrambe le superfici. | La prova del beneficio manca ancora. |

In un progetto reale questi riscontri richiedono file, simboli e controlli effettivamente consultati. Qui i nomi sono inventati: illustrano come un'evidenza cambia una scelta, non certificano un repository.

Il ledger evita due errori diversi: duplicare una capacità già disponibile e dimenticare un consumatore che non la usa.

### Complete explanation
Prima di scegliere quali parti modificare, cerchiamo ciò che esiste. Il **Capability Ledger** registra capacità, evidenza e conseguenza per il design.

**Indagine didattica inventata su Orione, ora completata:**

| Capacità cercata | Riscontro nel caso | Conseguenza |
|---|---|---|
| Calcolo condiviso della scadenza | La lettura del componente `ExpiryPolicy` e delle sue chiamate mostra un calcolo unico usato dal pannello. | Riutilizzarlo è una possibilità fondata. |
| Notifica coerente | La notifica confronta ancora il tempo con una regola locale di 30 secondi. | Cambiare soltanto il calcolo condiviso non corregge questa superficie. |
| Prove ai confini | I test disponibili controllano la costante, non il risultato su entrambe le superfici. | La prova del beneficio manca ancora. |

In un progetto reale questi riscontri richiedono file, simboli e controlli effettivamente consultati. Qui i nomi sono inventati: illustrano come un'evidenza cambia una scelta, non certificano un repository.

Il ledger evita due errori diversi: duplicare una capacità già disponibile e dimenticare un consumatore che non la usa.

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «Impact e design: collegare le parti al risultato»: seguire un cambiamento fino alle superfici e alle prove del risultato.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S34
Module: M5
Objective: O5
Role: explanation
Title: Impact e design: collegare le parti al risultato
Value contribution: Seguire un cambiamento fino alle superfici e alle prove del risultato.

### Learner content
**Dall'evidenza alla scelta.** In questo esempio scegliamo di adeguare il calcolo condiviso e portare la notifica a usare la stessa regola. Il pannello già la consulta. Non aggiungiamo un secondo motore di scadenza: duplicare la regola lascerebbe due punti da mantenere senza un bisogno dimostrato.

L'**Impact** nomina ciò che viene toccato e perché: calcolo per la nuova finestra, notifica per eliminare la regola locale, test per pannello e notifica. Il **design** descrive come il risultato deve comportarsi: attesa mentre il callback è valido, esito coerente nelle due superfici e trattamento esplicito di errore e dati vecchi. La precedenza allo stesso istante resta da concordare prima di implementarla.

La scelta serve al beneficio della Vision: a 35 secondi l'operatrice non deve ricevere una scadenza prematura. Modificare solo il calcolo lascerebbe la notifica errata; modificare solo il testo del pannello nasconderebbe il problema.

**Cambia una condizione:** se l'indagine non trovasse una capacità condivisa nell'area esaminata, il riuso non sarebbe una conclusione giustificata. Si registrerebbero ricerca e limite, poi si valuterebbe se introdurre una capacità comune è necessario. “Non trovato qui” non significa “non esiste ovunque”.

*Indagine e componenti sono inventati per mostrare il ragionamento.*

### Complete explanation
**Dall'evidenza alla scelta.** In questo esempio scegliamo di adeguare il calcolo condiviso e portare la notifica a usare la stessa regola. Il pannello già la consulta. Non aggiungiamo un secondo motore di scadenza: duplicare la regola lascerebbe due punti da mantenere senza un bisogno dimostrato.

L'**Impact** nomina ciò che viene toccato e perché: calcolo per la nuova finestra, notifica per eliminare la regola locale, test per pannello e notifica. Il **design** descrive come il risultato deve comportarsi: attesa mentre il callback è valido, esito coerente nelle due superfici e trattamento esplicito di errore e dati vecchi. La precedenza allo stesso istante resta da concordare prima di implementarla.

La scelta serve al beneficio della Vision: a 35 secondi l'operatrice non deve ricevere una scadenza prematura. Modificare solo il calcolo lascerebbe la notifica errata; modificare solo il testo del pannello nasconderebbe il problema.

**Cambia una condizione:** se l'indagine non trovasse una capacità condivisa nell'area esaminata, il riuso non sarebbe una conclusione giustificata. Si registrerebbero ricerca e limite, poi si valuterebbe se introdurre una capacità comune è necessario. “Non trovato qui” non significa “non esiste ovunque”.

*Indagine e componenti sono inventati per mostrare il ragionamento.*

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «I test devono seguire il comportamento osservabile»: seguire un cambiamento fino alle superfici e alle prove del risultato.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S35
Module: M5
Objective: O5
Role: explanation
Title: I test devono seguire il comportamento osservabile
Value contribution: Seguire un cambiamento fino alle superfici e alle prove del risultato.

### Learner content
Dopo il design si implementa. Un test sulla sola costante non dimostra che l’operatrice veda lo stato corretto.

| Prova nel caso Orione | Che cosa osservare | Perché serve |
|---|---|---|
| 30 secondi, nessun callback | Pannello e notifica non anticipano la scadenza. | Trova la vecchia regola rimasta in giro. |
| Prima di 45, callback valido | Esito previsto e feedback coerenti. | Controlla il percorso della risposta. |
| Esattamente a 45 | La precedenza scelta nella specifica. | Controlla il confine senza inventarlo. |
| Dopo la scadenza o in errore | Stati e risposte previsti dal contratto. | Controlla i percorsi alternativi. |

**Da ricordare:** Le attese dei test derivano dalla regola verificata e dalla specifica confermata.

I test coprono casi scelti dalla specifica e dai rischi. A 30 secondi si cerca l’anticipo errato; prima di 45 si segue una risposta valida; al confine si verifica la precedenza concordata. Un test verde sulla costante non osserva nessuna di queste interazioni.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
I test coprono casi scelti dalla specifica e dai rischi. A 30 secondi si cerca l’anticipo errato; prima di 45 si segue una risposta valida; al confine si verifica la precedenza concordata. Un test verde sulla costante non osserva nessuna di queste interazioni.

### Visual content
Tabella con intestazione e tutte le celle esattamente come in Learner content. Lettura per righe, da sinistra a destra; non sostituire le spiegazioni con icone.

### Transition
Il percorso continua con «La review finale confronta risultato e design»: seguire un cambiamento fino alle superfici e alle prove del risultato.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S36
Module: M5
Objective: O5
Role: explanation
Title: La review finale confronta risultato e design
Value contribution: Seguire un cambiamento fino alle superfici e alle prove del risultato.

### Learner content
Una review è un riesame del lavoro. Quella del design cerca omissioni nella soluzione. Quella finale cerca scostamenti e regressioni nel risultato.

**Prima di implementare** — Il design copre il cambiamento? Esempio: abbiamo considerato la notifica oltre al pannello? La regola al confine è stata decisa?

**Prima di chiudere** — Le evidenze dimostrano il risultato? Esempio: i test mostrano gli stati previsti su tutte le superfici? Il comportamento precedente resta corretto altrove?

**Da ricordare:** La chiusura aggiorna anche analisi e stato del lavoro, così la sessione successiva sa che cosa è stato deciso.

Le due review rispondono a domande diverse. Un buon design può essere implementato male, e un’implementazione fedele può riprodurre un design incompleto. Le evidenze finali vanno confrontate con beneficio, flussi e rischi; il giudizio del revisore non è una garanzia assoluta.

**Chi fa la review conta.** L'autore che rilegge design e codice può ripetere la stessa omissione. Per questo il protocollo richiede un revisore con contesto separato: per esempio un agente fresco che riceve gli artefatti e i criteri, non il ragionamento con cui l'autore ha scelto la soluzione. L'indipendenza aiuta a cercare ciò che l'autore ha trascurato; non garantisce che ogni difetto venga trovato.

Se nessuna modalità indipendente è utilizzabile, la skill prevede un self-pass esplicito, dichiarando la ragione e il limite. Non si sceglie questo ripiego per comodità quando un revisore indipendente è disponibile, e non si presenta l'autocontrollo come review indipendente.

### Complete explanation
Le due review rispondono a domande diverse. Un buon design può essere implementato male, e un’implementazione fedele può riprodurre un design incompleto. Le evidenze finali vanno confrontate con beneficio, flussi e rischi; il giudizio del revisore non è una garanzia assoluta.

**Chi fa la review conta.** L'autore che rilegge design e codice può ripetere la stessa omissione. Per questo il protocollo richiede un revisore con contesto separato: per esempio un agente fresco che riceve gli artefatti e i criteri, non il ragionamento con cui l'autore ha scelto la soluzione. L'indipendenza aiuta a cercare ciò che l'autore ha trascurato; non garantisce che ogni difetto venga trovato.

Se nessuna modalità indipendente è utilizzabile, la skill prevede un self-pass esplicito, dichiarando la ragione e il limite. Non si sceglie questo ripiego per comodità quando un revisore indipendente è disponibile, e non si presenta l'autocontrollo come review indipendente.

### Visual content
Due riquadri affiancati: il primo è il blocco «Prima di implementare», il secondo «Prima di chiudere». Riportare integralmente i rispettivi testi. Introduzione sopra, conclusione e precisazioni sotto. Nessuna freccia di causalità aggiuntiva.

### Transition
Il percorso continua con «Una GUIDE spiega come ripetere un’indagine»: seguire un cambiamento fino alle superfici e alle prove del risultato.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S37
Module: M5
Objective: O5
Role: explanation
Title: Una GUIDE spiega come ripetere un’indagine
Value contribution: Seguire un cambiamento fino alle superfici e alle prove del risultato.

### Learner content
Una GUIDE conserva un metodo riutilizzabile nato dal lavoro. Ecco un esempio di contenuto utile per cercare tutte le superfici di uno stato.

1. **Punto di partenza** — Individuare dove nasce o cambia lo stato di consegna.
2. **Percorso da seguire** — Controllare chi lo legge e come raggiunge pannello, eventuali notifiche e servizi.
3. **Controllo e confini** — Verificare attesa, esito ed errore. Indicare fonti e versione del sistema a cui l’indagine si riferisce.

**Da ricordare:** “Ricordati delle notifiche” è solo un promemoria. La GUIDE deve consentire a un’altra persona di rifare il ragionamento.

Una guida utile permette di ripetere l’indagine: punto iniziale, percorso, verifiche, ambito e fonti. Il semplice promemoria non spiega come trovare un consumatore dimenticato dello stato. Non ogni lavoro produce una GUIDE: serve un metodo riusabile sostenuto dall’esperienza documentata.

*Orione e i suoi documenti sono esempi inventati.*

### Complete explanation
Una guida utile permette di ripetere l’indagine: punto iniziale, percorso, verifiche, ambito e fonti. Il semplice promemoria non spiega come trovare un consumatore dimenticato dello stato. Non ogni lavoro produce una GUIDE: serve un metodo riusabile sostenuto dall’esperienza documentata.

### Visual content
Sequenza numerata in ordine di lettura con tutti i titoli e testi riportati in Learner content. La numerazione esprime ordine del ragionamento, non una misura di tempo. Introduzione e conclusione restano visibili.

### Transition
Il percorso continua con «Prova M5: un test verde basta per chiudere?»: seguire un cambiamento fino alle superfici e alle prove del risultato.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S38
Module: M5
Objective: O5
Role: check
Title: Prova M5: un test verde basta per chiudere?
Value contribution: Seguire un cambiamento fino alle superfici e alle prove del risultato.
Solution: S39

### Learner content
L'agente propone: “Ho cambiato 30 in 45. Il test sulla costante passa. Possiamo chiudere”. Il beneficio concordato è evitare uno stato prematuramente scaduto per l'operatrice. Nessuna evidenza accompagna la proposta su notifica, casi al confine o review del design.

**Che cosa rispondi?** Indica quali domande sul risultato restano aperte e quale indagine sulle capacità serve. Poi ordina e motiva il lavoro ancora necessario fino alla chiusura: che cosa va chiarito prima di implementare, quali prove cerchi e quando una GUIDE sarebbe giustificata?

Non assumere che l'indagine fittizia di S33 sia stata eseguita in questo nuovo tentativo. Una risposta utile lega ogni passaggio al caso; un elenco di sigle non basta. Tenta la risposta prima di S39.

Nella sequenza indica anche chi dovrebbe eseguire le review. Se l'agente autore dice «ho riletto tutto io», che evidenza manca? Quale limite andrebbe dichiarato se non fosse utilizzabile alcuna modalità indipendente?

### Complete explanation
L'agente propone: “Ho cambiato 30 in 45. Il test sulla costante passa. Possiamo chiudere”. Il beneficio concordato è evitare uno stato prematuramente scaduto per l'operatrice. Nessuna evidenza accompagna la proposta su notifica, casi al confine o review del design.

**Che cosa rispondi?** Indica quali domande sul risultato restano aperte e quale indagine sulle capacità serve. Poi ordina e motiva il lavoro ancora necessario fino alla chiusura: che cosa va chiarito prima di implementare, quali prove cerchi e quando una GUIDE sarebbe giustificata?

Non assumere che l'indagine fittizia di S33 sia stata eseguita in questo nuovo tentativo. Una risposta utile lega ogni passaggio al caso; un elenco di sigle non basta. Tenta la risposta prima di S39.

Nella sequenza indica anche chi dovrebbe eseguire le review. Se l'agente autore dice «ho riletto tutto io», che evidenza manca? Quale limite andrebbe dichiarato se non fosse utilizzabile alcuna modalità indipendente?

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «Soluzione M5: ogni passaggio evita un’omissione»: seguire un cambiamento fino alle superfici e alle prove del risultato.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S39
Module: M5
Objective: O5
Role: solution
Title: Soluzione M5: ogni passaggio evita un’omissione
Value contribution: Seguire un cambiamento fino alle superfici e alle prove del risultato.

### Learner content
Il test sulla costante dimostra un dato interno; non dimostra che l'operatrice vede uno stato attendibile. La proposta non è pronta per la chiusura.

1. **Completare l'analisi:** bisogno dell'operatrice; regola prima, al confine e dopo 45 secondi; comportamento di pannello e notifica; rischi di stato vecchio ed errore. Occorre risolvere la precedenza al confine con chi ne ha l'autorità. Cercare calcolo esistente e consumatori evita duplicazioni e omissioni.
2. **Definire Impact e design, poi review del design:** le evidenze dell'indagine guidano la scelta dei componenti. Il revisore controlla che la soluzione proposta copra beneficio, superfici e rischi prima che diventino codice. Se una modifica è già stata fatta, non si inventa una review precedente: la si rivaluta rispetto al design ora chiarito.
3. **Implementare il design accettato e raccogliere prove:** verificare, per esempio, attesa coerente a 35 secondi e gli esiti concordati al confine e dopo, su pannello e notifica. Una prova fallita richiede correzione, non una dichiarazione di completamento.
4. **Review finale:** confrontare cambiamento, design ed evidenze. Il passaggio serve a cercare omissioni rimaste anche con test verdi; non sostituisce i test.
5. **Chiusura:** registrare esito, decisioni, verifiche e limiti, aggiornando lo stato documentale dovuto. Una GUIDE è giustificata se è emerso un metodo riutilizzabile con provenienza, per esempio come verificare coerenza fra i consumatori della scadenza. Non serve un nuovo documento che ripeta soltanto “30 è diventato 45”; per una guida da indicazioni o lavoro si segue la proposta prevista dalla skill.

La sequenza è motivata: chiarire → progettare e rivedere → realizzare e provare → rivedere il risultato → chiudere. Se hai dato per concluso il lavoro dal test della costante, torna a S35; se hai scritto solo sigle, associa ogni passaggio alla specifica omissione che evita.

**Criterio sull'indipendenza:** i due momenti di review richiedono un revisore separato dall'autore, con gli artefatti necessari per giudicare. «L'autore si è ricontrollato» non soddisfa quel criterio. Se nessuna modalità indipendente è utilizzabile, occorre registrare il self-pass previsto, la ragione e il limite: non attestare una review indipendente mai svolta. Se hai equiparato i due controlli, rileggi S36.

### Complete explanation
Il test sulla costante dimostra un dato interno; non dimostra che l'operatrice vede uno stato attendibile. La proposta non è pronta per la chiusura.

1. **Completare l'analisi:** bisogno dell'operatrice; regola prima, al confine e dopo 45 secondi; comportamento di pannello e notifica; rischi di stato vecchio ed errore. Occorre risolvere la precedenza al confine con chi ne ha l'autorità. Cercare calcolo esistente e consumatori evita duplicazioni e omissioni.
2. **Definire Impact e design, poi review del design:** le evidenze dell'indagine guidano la scelta dei componenti. Il revisore controlla che la soluzione proposta copra beneficio, superfici e rischi prima che diventino codice. Se una modifica è già stata fatta, non si inventa una review precedente: la si rivaluta rispetto al design ora chiarito.
3. **Implementare il design accettato e raccogliere prove:** verificare, per esempio, attesa coerente a 35 secondi e gli esiti concordati al confine e dopo, su pannello e notifica. Una prova fallita richiede correzione, non una dichiarazione di completamento.
4. **Review finale:** confrontare cambiamento, design ed evidenze. Il passaggio serve a cercare omissioni rimaste anche con test verdi; non sostituisce i test.
5. **Chiusura:** registrare esito, decisioni, verifiche e limiti, aggiornando lo stato documentale dovuto. Una GUIDE è giustificata se è emerso un metodo riutilizzabile con provenienza, per esempio come verificare coerenza fra i consumatori della scadenza. Non serve un nuovo documento che ripeta soltanto “30 è diventato 45”; per una guida da indicazioni o lavoro si segue la proposta prevista dalla skill.

La sequenza è motivata: chiarire → progettare e rivedere → realizzare e provare → rivedere il risultato → chiudere. Se hai dato per concluso il lavoro dal test della costante, torna a S35; se hai scritto solo sigle, associa ogni passaggio alla specifica omissione che evita.

**Criterio sull'indipendenza:** i due momenti di review richiedono un revisore separato dall'autore, con gli artefatti necessari per giudicare. «L'autore si è ricontrollato» non soddisfa quel criterio. Se nessuna modalità indipendente è utilizzabile, occorre registrare il self-pass previsto, la ragione e il limite: non attestare una review indipendente mai svolta. Se hai equiparato i due controlli, rileggi S36.

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «Il passaggio fra KB e sviluppo conserva la fonte»: separare fatto, scelta umana e realizzazione verificata.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S40
Module: M6
Objective: O6
Role: explanation
Title: Il passaggio fra KB e sviluppo conserva la fonte
Value contribution: Separare fatto, scelta umana e realizzazione verificata.

### Learner content
**Esempio completo di passaggio fra conoscenza e sviluppo, inventato.** Domanda: «Per la release 2.1, quanto resta valido il callback?». La KB risponde: «45 secondi dall'invio, secondo Rettifica Orione 2.1, §1, p. 2, che corregge Manuale §4.3». Conserva entrambi i riferimenti e la storia della correzione.

La persona responsabile conferma il beneficio: «L'operatrice deve vedere uno stato attendibile durante l'attesa». Nell'analisi SDLC si cita quel claim e si precisano pannello e notifica come superfici interessate. La rettifica sostiene la durata; la persona autorizza il risultato da ottenere.

**Il limite emerge subito:** la fonte non specifica chi prevale se callback e timer scattano nello stesso istante. L'analisi registra la decisione mancante e chi deve chiarirla. Non attribuisce al manuale una regola mai scritta.

Il percorso SDLC cerca le capacità già disponibili, progetta il cambiamento, lo sottopone a review, lo implementa e verifica le superfici. Una prova prevista è che a 35 secondi non compaia una scadenza prematura; le prove al confine attendono il criterio concordato. In questo esempio non sono stati eseguiti test reali: “da verificare” resta distinto da “verificato”.

Se cambia ancora la fonte, il collegamento permette di ritrovare la decisione da riesaminare. Il collegamento non aggiorna automaticamente né il codice né i suoi consumatori.

### Complete explanation
**Esempio completo di passaggio fra conoscenza e sviluppo, inventato.** Domanda: «Per la release 2.1, quanto resta valido il callback?». La KB risponde: «45 secondi dall'invio, secondo Rettifica Orione 2.1, §1, p. 2, che corregge Manuale §4.3». Conserva entrambi i riferimenti e la storia della correzione.

La persona responsabile conferma il beneficio: «L'operatrice deve vedere uno stato attendibile durante l'attesa». Nell'analisi SDLC si cita quel claim e si precisano pannello e notifica come superfici interessate. La rettifica sostiene la durata; la persona autorizza il risultato da ottenere.

**Il limite emerge subito:** la fonte non specifica chi prevale se callback e timer scattano nello stesso istante. L'analisi registra la decisione mancante e chi deve chiarirla. Non attribuisce al manuale una regola mai scritta.

Il percorso SDLC cerca le capacità già disponibili, progetta il cambiamento, lo sottopone a review, lo implementa e verifica le superfici. Una prova prevista è che a 35 secondi non compaia una scadenza prematura; le prove al confine attendono il criterio concordato. In questo esempio non sono stati eseguiti test reali: “da verificare” resta distinto da “verificato”.

Se cambia ancora la fonte, il collegamento permette di ritrovare la decisione da riesaminare. Il collegamento non aggiorna automaticamente né il codice né i suoi consumatori.

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «Standalone e devPNT cambiano la sede dei documenti»: separare fatto, scelta umana e realizzazione verificata.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S41
Module: M6
Objective: O6
Role: explanation
Title: Standalone e devPNT cambiano la sede dei documenti
Value contribution: Separare fatto, scelta umana e realizzazione verificata.

### Learner content
Standalone è il percorso completo nella cartella del progetto. devPNT è un’integrazione facoltativa che aggiunge pianificazione e governance dei documenti.

**Standalone** — Design nell’ANALYSIS, guidato dalla Vision Le sezioni raccolgono bisogni, regole, interfacce, rischi, capacità e impatto. Fonti e guide restano consultabili nel progetto.

**Con devPNT configurato** — Documenti governati separatamente D-UC per gli use case, D-IC per le interfacce, P-TM per i rischi. E-ISP raccoglie specifica, capacità e impatto. E-TDD dettaglia il design.

**Da ricordare:** Il motivo delle verifiche resta lo stesso. Per usare le due skill non è necessario avere devPNT.

La modalità di conservazione cambia la sede di alcuni documenti, non la necessità di descrivere il comportamento. Standalone è un percorso completo. La modalità integrata richiede che devPNT sia configurato e che vengano rispettate le sue decisioni governate; non va presunto disponibile.

### Complete explanation
La modalità di conservazione cambia la sede di alcuni documenti, non la necessità di descrivere il comportamento. Standalone è un percorso completo. La modalità integrata richiede che devPNT sia configurato e che vengano rispettate le sue decisioni governate; non va presunto disponibile.

### Visual content
Due riquadri affiancati: il primo è il blocco «Standalone», il secondo «Con devPNT configurato». Riportare integralmente i rispettivi testi. Introduzione sopra, conclusione e precisazioni sotto. Nessuna freccia di causalità aggiuntiva.

### Transition
Il percorso continua con «Prova M6: la rettifica può decidere l’interfaccia?»: separare fatto, scelta umana e realizzazione verificata.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S42
Module: M6
Objective: O6
Role: check
Title: Prova M6: la rettifica può decidere l’interfaccia?
Value contribution: Separare fatto, scelta umana e realizzazione verificata.
Solution: S43

### Learner content
Un collega dice: “La rettifica afferma 45 secondi, quindi la KB può scegliere la UI e chiudere il ticket”. UI significa interfaccia utente. Nel progetto non è configurato devPNT; sono disponibili cartella del progetto, fonti e strumenti di sviluppo.

**Come prosegui?** Assegna la responsabilità di chiarire il fatto, decidere beneficio e comportamento, realizzare e verificare il cambiamento. Spiega se l'assenza di devPNT blocca il percorso e dove conserveresti il design. Indica una cosa che la rettifica non permette di concludere.

Rispondi prima di aprire S43. Non occorre disegnare un'interfaccia.

### Complete explanation
Un collega dice: “La rettifica afferma 45 secondi, quindi la KB può scegliere la UI e chiudere il ticket”. UI significa interfaccia utente. Nel progetto non è configurato devPNT; sono disponibili cartella del progetto, fonti e strumenti di sviluppo.

**Come prosegui?** Assegna la responsabilità di chiarire il fatto, decidere beneficio e comportamento, realizzare e verificare il cambiamento. Spiega se l'assenza di devPNT blocca il percorso e dove conserveresti il design. Indica una cosa che la rettifica non permette di concludere.

Rispondi prima di aprire S43. Non occorre disegnare un'interfaccia.

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «Soluzione M6: un fatto non completa la modifica»: separare fatto, scelta umana e realizzazione verificata.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S43
Module: M6
Objective: O6
Role: solution
Title: Soluzione M6: un fatto non completa la modifica
Value contribution: Separare fatto, scelta umana e realizzazione verificata.

### Learner content
**kb-agentic** sostiene il fatto: conserva rettifica, ambito, locatore e storia. Non sceglie per questo il comportamento dell'interfaccia e non certifica l'implementazione.

**La persona responsabile** conferma beneficio e confini e chiarisce le decisioni aperte, come la precedenza al confine temporale. **agentic-sdlc** governa analisi, design, implementazione, prove e review del risultato. I passaggi citano la stessa fonte, senza creare una seconda autorità sulla durata.

**Si può proseguire in Standalone.** Il design vive nelle sezioni dell'ANALYSIS e negli altri file previsti del progetto. devPNT non è un prerequisito delle due skill. Se fosse configurato per quel progetto, andrebbero invece rispettati i suoi documenti e le decisioni governate: non si può dichiarare una proposta approvata solo perché esiste un file locale.

Una risposta sufficiente distingue fatto, decisione e prova e sceglie la modalità disponibile. “Il manuale dice 45, quindi è tutto deciso” fallisce sul comportamento e sui test: rileggi S40. “Serve installare devPNT per cominciare” fallisce sulla modalità: rileggi S41.

### Complete explanation
**kb-agentic** sostiene il fatto: conserva rettifica, ambito, locatore e storia. Non sceglie per questo il comportamento dell'interfaccia e non certifica l'implementazione.

**La persona responsabile** conferma beneficio e confini e chiarisce le decisioni aperte, come la precedenza al confine temporale. **agentic-sdlc** governa analisi, design, implementazione, prove e review del risultato. I passaggi citano la stessa fonte, senza creare una seconda autorità sulla durata.

**Si può proseguire in Standalone.** Il design vive nelle sezioni dell'ANALYSIS e negli altri file previsti del progetto. devPNT non è un prerequisito delle due skill. Se fosse configurato per quel progetto, andrebbero invece rispettati i suoi documenti e le decisioni governate: non si può dichiarare una proposta approvata solo perché esiste un file locale.

Una risposta sufficiente distingue fatto, decisione e prova e sceglie la modalità disponibile. “Il manuale dice 45, quindi è tutto deciso” fallisce sul comportamento e sui test: rileggi S40. “Serve installare devPNT per cominciare” fallisce sulla modalità: rileggi S41.

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «Applicazione facoltativa a un tuo progetto»: separare fatto, scelta umana e realizzazione verificata.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S44
Module: M6
Objective: O6
Role: explanation
Title: Applicazione facoltativa a un tuo progetto
Value contribution: Separare fatto, scelta umana e realizzazione verificata.

### Learner content
Scegli un documento consultabile e una modifica ipotetica del tuo progetto. Puoi rispondere a voce o in note personali, senza modificare o inviare file. Se non hai un documento disponibile, usa il caso Orione.

1. Formula una domanda e indica documento, versione e passaggio che sostiene la risposta, oppure la lacuna.
2. Nomina beneficiario, risultato e superficie in cui deve apparire. Separa ciò che la fonte stabilisce dalla decisione ancora umana.
3. Scegli chi governa fonte e cambiamento e la modalità disponibile; indica un rischio e la prova che lo controllerebbe.

**Confronta dopo il tentativo.** Un esempio adeguato su Orione è: «Rettifica 2.1 §1 p. 2 sostiene 45 secondi; vogliamo evitare all'operatrice una scadenza prematura su pannello e notifica. La KB custodisce il fatto; SDLC progetta la modifica in Standalone. Resta da decidere la precedenza al confine. Verificherei entrambe le superfici a 35 secondi e nei casi concordati; non ho ancora eseguito le prove».

Per il tuo caso la risposta è adeguata se ogni fatto ha una provenienza o un limite dichiarato, il beneficio riguarda qualcuno, la responsabilità è chiara e la prova osserva il rischio. «Fonte non disponibile: devo recuperarla» è corretto; una citazione inventata non lo è. Fonte debole → S14–16; beneficio assente → S25; prova che controlla solo una costante → S35; modalità confusa → S41. Questo controllo diagnostico non certifica una modifica reale.

### Complete explanation
Scegli un documento consultabile e una modifica ipotetica del tuo progetto. Puoi rispondere a voce o in note personali, senza modificare o inviare file. Se non hai un documento disponibile, usa il caso Orione.

1. Formula una domanda e indica documento, versione e passaggio che sostiene la risposta, oppure la lacuna.
2. Nomina beneficiario, risultato e superficie in cui deve apparire. Separa ciò che la fonte stabilisce dalla decisione ancora umana.
3. Scegli chi governa fonte e cambiamento e la modalità disponibile; indica un rischio e la prova che lo controllerebbe.

**Confronta dopo il tentativo.** Un esempio adeguato su Orione è: «Rettifica 2.1 §1 p. 2 sostiene 45 secondi; vogliamo evitare all'operatrice una scadenza prematura su pannello e notifica. La KB custodisce il fatto; SDLC progetta la modifica in Standalone. Resta da decidere la precedenza al confine. Verificherei entrambe le superfici a 35 secondi e nei casi concordati; non ho ancora eseguito le prove».

Per il tuo caso la risposta è adeguata se ogni fatto ha una provenienza o un limite dichiarato, il beneficio riguarda qualcuno, la responsabilità è chiara e la prova osserva il rischio. «Fonte non disponibile: devo recuperarla» è corretto; una citazione inventata non lo è. Fonte debole → S14–16; beneficio assente → S25; prova che controlla solo una costante → S35; modalità confusa → S41. Questo controllo diagnostico non certifica una modifica reale.

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «Che cosa si può riusare dopo una settimana o anni»: scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S45
Module: M7
Objective: O7
Role: explanation
Title: Che cosa si può riusare dopo una settimana o anni
Value contribution: Scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Learner content
Riapriamo sempre lo stesso compito: **capire e, quando necessario, correggere perché Orione dichiara una consegna scaduta**. Confrontiamo buone note mantenute con il protocollo applicato, a parità di accesso alle fonti. Il semplice nome della skill non aggiunge una capacità.

| Quando e condizione | Nota curata | Protocollo delle skill | Costo e condizione che annulla il riuso |
|---|---|---|---|
| Una settimana: nulla è cambiato | Motivo e fonte consentono già di spiegare la scelta. | Il riferimento dalla decisione al claim porta allo stesso risultato. Nessun vantaggio aggiuntivo è dimostrato qui. | In entrambi i casi serve mantenere accessibili fonte e ambito; un collegamento rotto impedisce la verifica. |
| Un mese: arriva una rettifica | Se contiene legami a decisioni e consumatori, la nota guida già la revisione; se conserva soltanto il numero, bisogna ricostruirli. | Conflitto e dipendenze esplicite guidano la ricerca delle decisioni da riesaminare; i controlli sul software restano da fare. | Registrare e rivedere i legami costa lavoro. Dipendenze omesse possono lasciare una notifica errata. |
| Anni: arriva un nuovo collega | Una nota aggiornata con ragioni, fonti e metodo può spiegare ancora il compito. | Decisioni e GUIDE con provenienza rendono riapribile il ragionamento, se ancora pertinente. | Verificare validità e aggiornare il metodo richiede manutenzione. Una guida obsoleta non diventa affidabile perché è archiviata. |

La disciplina esplicita aiuta a non lasciare queste attività al ricordo occasionale. Istruzioni e controlli equivalenti possono realizzarla anche senza skill. Il corso non misura risparmio di tempo: il beneficio dipende dai legami effettivamente mantenuti, non dagli anni trascorsi.

### Complete explanation
Riapriamo sempre lo stesso compito: **capire e, quando necessario, correggere perché Orione dichiara una consegna scaduta**. Confrontiamo buone note mantenute con il protocollo applicato, a parità di accesso alle fonti. Il semplice nome della skill non aggiunge una capacità.

| Quando e condizione | Nota curata | Protocollo delle skill | Costo e condizione che annulla il riuso |
|---|---|---|---|
| Una settimana: nulla è cambiato | Motivo e fonte consentono già di spiegare la scelta. | Il riferimento dalla decisione al claim porta allo stesso risultato. Nessun vantaggio aggiuntivo è dimostrato qui. | In entrambi i casi serve mantenere accessibili fonte e ambito; un collegamento rotto impedisce la verifica. |
| Un mese: arriva una rettifica | Se contiene legami a decisioni e consumatori, la nota guida già la revisione; se conserva soltanto il numero, bisogna ricostruirli. | Conflitto e dipendenze esplicite guidano la ricerca delle decisioni da riesaminare; i controlli sul software restano da fare. | Registrare e rivedere i legami costa lavoro. Dipendenze omesse possono lasciare una notifica errata. |
| Anni: arriva un nuovo collega | Una nota aggiornata con ragioni, fonti e metodo può spiegare ancora il compito. | Decisioni e GUIDE con provenienza rendono riapribile il ragionamento, se ancora pertinente. | Verificare validità e aggiornare il metodo richiede manutenzione. Una guida obsoleta non diventa affidabile perché è archiviata. |

La disciplina esplicita aiuta a non lasciare queste attività al ricordo occasionale. Istruzioni e controlli equivalenti possono realizzarla anche senza skill. Il corso non misura risparmio di tempo: il beneficio dipende dai legami effettivamente mantenuti, non dagli anni trascorsi.

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «La continuità richiede anche manutenzione»: scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S46
Module: M7
Objective: O7
Role: explanation
Title: La continuità richiede anche manutenzione
Value contribution: Scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Learner content
Una cartella piena di documenti può comunque dare risposte sbagliate. Il metodo deve permettere di ritrovare i limiti e correggere le dipendenze.

1. **Il documento non c’è** — La KB dichiara che manca la fonte, anziché completare il fatto per plausibilità.
2. **La fonte è cambiata** — I claim e le decisioni collegate tornano sotto controllo.
3. **La guida è invecchiata** — Chi la riusa ne verifica ambito e riferimenti, poi aggiorna il metodo se necessario.

**Da ricordare:** Una skill non garantisce memoria personale illimitata. La continuità dipende dai file accessibili e dal loro uso.

La manutenzione comprende correggere ciò che è diventato falso o non più applicabile. Nessuna istruzione recupera file inaccessibili, e un indice aggiornato non certifica da solo il contenuto. Il valore del metodo va cercato nelle verifiche ripetibili che sostiene, non nel nome della skill.

### Complete explanation
La manutenzione comprende correggere ciò che è diventato falso o non più applicabile. Nessuna istruzione recupera file inaccessibili, e un indice aggiornato non certifica da solo il contenuto. Il valore del metodo va cercato nelle verifiche ripetibili che sostiene, non nel nome della skill.

### Visual content
Sequenza numerata in ordine di lettura con tutti i titoli e testi riportati in Learner content. La numerazione esprime ordine del ragionamento, non una misura di tempo. Introduzione e conclusione restano visibili.

### Transition
Il percorso continua con «Prova finale: spiegare il valore a un nuovo collega»: scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S47
Module: M7
Objective: O7
Role: check
Title: Prova finale: spiegare il valore a un nuovo collega
Value contribution: Scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.
Solution: S48

### Learner content
Un nuovo collega riapre il compito di spiegare lo stato di consegna. Dopo una settimana la regola è invariata; dopo un mese arriva una rettifica; dopo anni il collega trova una GUIDE con fonti non ancora ricontrollate.

**Confronta una nota curata e il protocollo applicato per ciascuna tappa.** Che cosa possono entrambi evitare di ricostruire? Quale legame o verifica aggiungeresti se mancasse? Quale costo rimane e che cosa farebbe perdere il beneficio?

Concludi se i dati consentono di promettere un guadagno di produttività o di sostenere che una skill è indispensabile. Tenta la risposta prima di S48.

### Complete explanation
Un nuovo collega riapre il compito di spiegare lo stato di consegna. Dopo una settimana la regola è invariata; dopo un mese arriva una rettifica; dopo anni il collega trova una GUIDE con fonti non ancora ricontrollate.

**Confronta una nota curata e il protocollo applicato per ciascuna tappa.** Che cosa possono entrambi evitare di ricostruire? Quale legame o verifica aggiungeresti se mancasse? Quale costo rimane e che cosa farebbe perdere il beneficio?

Concludi se i dati consentono di promettere un guadagno di produttività o di sostenere che una skill è indispensabile. Tenta la risposta prima di S48.

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «Soluzione finale: riusare e ricontrollare»: scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S48
Module: M7
Objective: O7
Role: solution
Title: Soluzione finale: riusare e ricontrollare
Value contribution: Scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Learner content
**Una settimana:** una nota con fonte e motivo può già spiegare la scelta; il percorso decisione → claim offre lo stesso riuso. Va verificato che la fonte sia apribile e pertinente. Non c'è un vantaggio esclusivo dimostrato della skill.

**Un mese:** la rettifica impone di riesaminare regola, decisioni e consumatori. Se i legami esistono anche nella nota, entrambi i metodi aiutano; se mancano, la ricostruzione resta necessaria. Il protocollo rende esplicita la richiesta di mantenerli, ma non prova che siano completi né aggiorna il codice.

**Anni:** ragioni e metodo conservati possono orientare il nuovo collega in entrambi i casi. Una GUIDE è utile se fonti e ambito sono ancora validi; il costo di verificarli e aggiornare il metodo rimane. Una vecchia regola copiata senza controllo può rendere il riuso dannoso.

Una risposta sufficiente confronta lo stesso compito, nomina per ogni tappa una ricostruzione evitabile e un controllo o costo, e ammette equivalenza quando le informazioni sono equivalenti. “La skill ricorda tutto per anni” non supera il criterio: torna a S46. “Si risparmia il 30%” non è sostenuto da questo corso. Il valore da osservare sul progetto è quali omissioni e ricostruzioni diminuiscono, insieme al costo di manutenzione.

### Complete explanation
**Una settimana:** una nota con fonte e motivo può già spiegare la scelta; il percorso decisione → claim offre lo stesso riuso. Va verificato che la fonte sia apribile e pertinente. Non c'è un vantaggio esclusivo dimostrato della skill.

**Un mese:** la rettifica impone di riesaminare regola, decisioni e consumatori. Se i legami esistono anche nella nota, entrambi i metodi aiutano; se mancano, la ricostruzione resta necessaria. Il protocollo rende esplicita la richiesta di mantenerli, ma non prova che siano completi né aggiorna il codice.

**Anni:** ragioni e metodo conservati possono orientare il nuovo collega in entrambi i casi. Una GUIDE è utile se fonti e ambito sono ancora validi; il costo di verificarli e aggiornare il metodo rimane. Una vecchia regola copiata senza controllo può rendere il riuso dannoso.

Una risposta sufficiente confronta lo stesso compito, nomina per ogni tappa una ricostruzione evitabile e un controllo o costo, e ammette equivalenza quando le informazioni sono equivalenti. “La skill ricorda tutto per anni” non supera il criterio: torna a S46. “Si risparmia il 30%” non è sostenuto da questo corso. Il valore da osservare sul progetto è quali omissioni e ricostruzioni diminuiscono, insieme al costo di manutenzione.

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «Quando usare il protocollo e quando bastano note curate»: scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S49
Module: M7
Objective: O7
Role: explanation
Title: Quando usare il protocollo e quando bastano note curate
Value contribution: Scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Learner content
Scegli in base al lavoro da ripetere e al costo delle omissioni, senza trasformare ogni appunto in un processo completo.

**Caso circoscritto** — Una fonte stabile, una decisione, un lettore. Una nota con motivo e riferimento può soddisfare il bisogno; introdurre altro processo può costare più di quanto aiuta.

**Lavoro che evolve** — Fonti discordanti, più superfici, sessioni e persone. Le regole esplicite di provenienza, revisione e chiusura rendono le omissioni più riconoscibili e il lavoro ripetibile.

**Da ricordare:** Se istruzioni equivalenti sono già applicate e verificate, il nome “skill” non aggiunge da solo un vantaggio.

Il valore del corso è permettere questa scelta motivata, non convincerti sempre a installare qualcosa. Per valutarne il beneficio reale osserva nel tuo contesto quali ricostruzioni e omissioni diminuiscono, includendo il costo di mantenere documenti e controlli. Qui non abbiamo tali misure.

### Complete explanation
Il valore del corso è permettere questa scelta motivata, non convincerti sempre a installare qualcosa. Per valutarne il beneficio reale osserva nel tuo contesto quali ricostruzioni e omissioni diminuiscono, includendo il costo di mantenere documenti e controlli. Qui non abbiamo tali misure.

### Visual content
Due riquadri affiancati: il primo è il blocco «Caso circoscritto», il secondo «Lavoro che evolve». Riportare integralmente i rispettivi testi. Introduzione sopra, conclusione e precisazioni sotto. Nessuna freccia di causalità aggiuntiva.

### Transition
Il percorso continua con «Trasferimento: due progetti, quale disciplina serve?»: scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S50
Module: M7
Objective: O7
Role: check
Title: Trasferimento: due progetti, quale disciplina serve?
Value contribution: Scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.
Solution: S51

### Learner content
Caso nuovo, inventato. Alba conserva una sola decisione su un manuale stabile, con fonte e motivo. Bora ha tre operatori, un pannello e una notifica: una nuova circolare contraddice la durata precedente per la stessa release e le stesse condizioni. Le note riportano entrambe le durate senza spiegare il contrasto. Non ci sono altre evidenze disponibili.

**Sei responsabile di proporre come proseguire nei due progetti.** Scrivi una breve raccomandazione motivata: quale disciplina manterresti o cambieresti, che cosa puoi concludere ora, che cosa cercheresti e quale risultato dovresti verificare prima di chiudere un eventuale cambiamento. Indica se la tua proposta dipende dall'uso di una skill.

Tenta la risposta senza tornare agli esempi precedenti. Ogni scelta deve essere collegata ai dati del caso; confrontala con S51 soltanto dopo.

### Complete explanation
Caso nuovo, inventato. Alba conserva una sola decisione su un manuale stabile, con fonte e motivo. Bora ha tre operatori, un pannello e una notifica: una nuova circolare contraddice la durata precedente per la stessa release e le stesse condizioni. Le note riportano entrambe le durate senza spiegare il contrasto. Non ci sono altre evidenze disponibili.

**Sei responsabile di proporre come proseguire nei due progetti.** Scrivi una breve raccomandazione motivata: quale disciplina manterresti o cambieresti, che cosa puoi concludere ora, che cosa cercheresti e quale risultato dovresti verificare prima di chiudere un eventuale cambiamento. Indica se la tua proposta dipende dall'uso di una skill.

Tenta la risposta senza tornare agli esempi precedenti. Ogni scelta deve essere collegata ai dati del caso; confrontala con S51 soltanto dopo.

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Il percorso continua con «Soluzione: il valore è saper scegliere e verificare»: scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S51
Module: M7
Objective: O7
Role: solution
Title: Soluzione: il valore è saper scegliere e verificare
Value contribution: Scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Learner content
Alba può mantenere la nota curata e controllare che la fonte sia ancora valida. Non è dimostrato un bisogno aggiuntivo di protocollo completo.

1. **Bora: chiarire il fatto** — Confrontare ambito e provenienza delle due durate; chiedere una rettifica o un fatto che risolva il contrasto. Fino ad allora il conflitto resta aperto.
2. **Bora: seguire la conseguenza** — Ritrovare la decisione sulla scadenza e progettare il comportamento coerente di pannello e notifica, inclusi attesa ed errore.
3. **Bora: dimostrare il risultato** — Verificare le superfici nei casi definiti, poi confrontare risultato e design. Non basta aggiornare la nota.

**Da ricordare:** Una skill può confezionare questa disciplina; istruzioni equivalenti possono ottenerla. Il valore sta nei passaggi espliciti e nel loro uso verificato.

Correzione: se hai scelto automaticamente l’ultima circolare, rileggi M3; se hai aggiornato soltanto la nota, M5; se hai imposto una skill ad Alba, rileggi il confronto sui casi circoscritti. La risposta richiede di scegliere e giustificare, non di ricordare le sigle.

### Complete explanation
Correzione: se hai scelto automaticamente l’ultima circolare, rileggi M3; se hai aggiornato soltanto la nota, M5; se hai imposto una skill ad Alba, rileggi il confronto sui casi circoscritti. La risposta richiede di scegliere e giustificare, non di ricordare le sigle. La risposta e il percorso di correzione sono interamente nel testo visibile; nessuna spiegazione orale è necessaria per usarli.

### Visual content
Sequenza numerata in ordine di lettura con tutti i titoli e testi riportati in Learner content. La numerazione esprime ordine del ragionamento, non una misura di tempo. Introduzione e conclusione restano visibili.

### Transition
Il percorso continua con «Riferimenti e limiti del corso»: scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S52
Module: M7
Objective: O7
Role: closing
Title: Riferimenti e limiti del corso
Value contribution: Scegliere quando il metodo aggiunge una disciplina utile e quando una nota è sufficiente.

### Learner content
Questo è il testo completo 2.1-content del corso, organizzato in 52 unità corrispondenti alle future slide. Il PowerPoint verrà prodotto dopo la definizione del testo. Le sezioni Sources rimandano al registro delle fonti e alle versioni locali delle skill usate.

**Fonti:** registro `sources.md`, con snapshot delle skill del 27 settembre 2026. Il corso 1.0-draft è una versione storica, non l'autorità aggiornata del contenuto.

**Caso didattico:** Orione, Alba, Bora, i loro documenti e componenti sono inventati. Per un progetto reale, regole e verifiche devono derivare dalle sue fonti e decisioni.

**Ripresa facoltativa:** fra qualche giorno, prova di nuovo Alba/Bora senza rileggere le spiegazioni. Poi confronta le ragioni con S51 e riapri solo i passaggi che non riesci a motivare. Non viene fissato un promemoria né registrata una prestazione; questa proposta non dimostra ritenzione duratura.

Le domande e le correzioni aiutano a individuare che cosa rileggere. L'efficacia su persone reali resta non verificata. Il corso descrive un protocollo e i suoi limiti, non un esperimento di produttività.

### Complete explanation
Questo è il testo completo 2.1-content del corso, organizzato in 52 unità corrispondenti alle future slide. Il PowerPoint verrà prodotto dopo la definizione del testo. Le sezioni Sources rimandano al registro delle fonti e alle versioni locali delle skill usate.

**Fonti:** registro `sources.md`, con snapshot delle skill del 27 settembre 2026. Il corso 1.0-draft è una versione storica, non l'autorità aggiornata del contenuto.

**Caso didattico:** Orione, Alba, Bora, i loro documenti e componenti sono inventati. Per un progetto reale, regole e verifiche devono derivare dalle sue fonti e decisioni.

**Ripresa facoltativa:** fra qualche giorno, prova di nuovo Alba/Bora senza rileggere le spiegazioni. Poi confronta le ragioni con S51 e riapri solo i passaggi che non riesci a motivare. Non viene fissato un promemoria né registrata una prestazione; questa proposta non dimostra ritenzione duratura.

Le domande e le correzioni aiutano a individuare che cosa rileggere. L'efficacia su persone reali resta non verificata. Il corso descrive un protocollo e i suoi limiti, non un esperimento di produttività.

### Visual content
Presentazione testuale nell’ordine di Learner content, con tutti i paragrafi, elenchi e celle della tabella eventualmente presente. Non sostituire ragioni o condizioni con icone. La suddivisione grafica futura deve preservare il contenuto e separare tentativo e soluzione.

### Transition
Fine del corso. Torna alla prova di trasferimento e usa le correzioni per scegliere quali passaggi rileggere.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13
