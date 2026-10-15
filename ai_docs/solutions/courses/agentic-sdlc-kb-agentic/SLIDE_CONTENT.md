# Perché lavorare con kb-agentic e agentic-sdlc
Course version: 4.0-content
Delivery mode: self-study
Efficacy: efficacy not verified
Feedback flow: IC1

## Course Value
| Profile | Baseline | Target capability | Teaching contribution | Observable check | Alternative and limits |
|---|---|---|---|---|---|
| P1 | Persona del team software che usa agenti; padronanza delle skill non accertata | Motivare quando e perché adottare le due skill con supporto di distill; giudicare benefici, costi e continuità del lavoro | Storia Orione: una protezione scoperta prima cambia il giudizio su un fix; si spiega il patrimonio durevole prima delle procedure | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s40 | Note curate equivalenti possono bastare. Nessuna efficacia umana o superiorità causale dimostrata. |

Testo primario: Learner content e Transition sono visibili all’allievo. Complete explanation offre lo stesso testo al relatore, senza ragionamento essenziale nascosto. Fonti in sources.md; tutti i casi sono fittizi. Feedback diretto non disponibile, vedi D-IC IC1. Il PPTX3.0 precedente non rappresenta questa revisione.

## S01
Module: M1
Objective: O1
Role: orientation
Title: Perché un agente ricomincia da capo?
Value contribution: orientare il beneficio prima del meccanismo.

### Learner content

Usi l’AI per sviluppare: una chat per un baco, un’altra per una feature, un documento con istruzioni e qualche nota presa durante il lavoro. Una nuova sessione riceve il codice attuale, ma non necessariamente le ragioni che lo hanno prodotto.

Questo non rende inevitabile un errore. Anche senza skill puoi mantenere ottime note. Il problema emerge quando fonti, decisioni e risultati restano dispersi: bisogna ritrovarli e capire quali valgono ancora. Una risposta plausibile può omettere un vincolo che il team aveva già scoperto.

Questo corso spiega perché kb-agentic e agentic-sdlc, con il supporto di distill, cercano di trasformare attività separate in conoscenza riutilizzabile. Vedremo prima il bisogno e il beneficio, poi il metodo. Non promettiamo risultati migliori in ogni progetto.

### Complete explanation

Usi l’AI per sviluppare: una chat per un baco, un’altra per una feature, un documento con istruzioni e qualche nota presa durante il lavoro. Una nuova sessione riceve il codice attuale, ma non necessariamente le ragioni che lo hanno prodotto.

Questo non rende inevitabile un errore. Anche senza skill puoi mantenere ottime note. Il problema emerge quando fonti, decisioni e risultati restano dispersi: bisogna ritrovarli e capire quali valgono ancora. Una risposta plausibile può omettere un vincolo che il team aveva già scoperto.

Questo corso spiega perché kb-agentic e agentic-sdlc, con il supporto di distill, cercano di trasformare attività separate in conoscenza riutilizzabile. Vedremo prima il bisogno e il beneficio, poi il metodo. Non promettiamo risultati migliori in ogni progetto.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Vediamo un progetto in cui la ragione di una scelta cambia il giudizio su una correzione.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1

## S02
Module: M1
Objective: O1
Role: explanation
Title: Orione cresce: il doppio clic
Value contribution: introdurre una protezione e il suo limite.

### Learner content

Orione è un software inventato che invia ordini a un fornitore. All’inizio il team vede un problema: una persona preme due volte «Invia» e vengono creati due ordini. Disabilita il pulsante durante l’attesa.

La nota di decisione conserva evento osservato, motivo del blocco e prova: due clic ravvicinati devono produrre un solo invio. Il codice contiene il blocco; la nota spiega perché esiste.

La soluzione copre il doppio clic, ma non tutti i modi in cui un ordine può essere duplicato. La storia del progetto non è un elenco di successi: conserva anche l’ambito di ogni protezione. Tutti i dati, documenti ed eventi di Orione sono fittizi; non sono risultati di una prova su software reale.

### Complete explanation

Orione è un software inventato che invia ordini a un fornitore. All’inizio il team vede un problema: una persona preme due volte «Invia» e vengono creati due ordini. Disabilita il pulsante durante l’attesa.

La nota di decisione conserva evento osservato, motivo del blocco e prova: due clic ravvicinati devono produrre un solo invio. Il codice contiene il blocco; la nota spiega perché esiste.

La soluzione copre il doppio clic, ma non tutti i modi in cui un ordine può essere duplicato. La storia del progetto non è un elenco di successi: conserva anche l’ambito di ogni protezione. Tutti i dati, documenti ed eventi di Orione sono fittizi; non sono risultati di una prova su software reale.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Un incidente diverso mostra perché ricordare il blocco non basta.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S03
Module: M1
Objective: O1
Role: explanation
Title: La conferma persa cambia il problema
Value contribution: spiegare la relazione chiave/ritentativo prima del suo uso.

### Learner content

Il fornitore crea l’ordine, ma la risposta non arriva a Orione. La persona vede ancora «in attesa» e ritenta. Un ritentativo è un nuovo invio per completare la stessa operazione, non un nuovo ordine voluto dalla persona.

Il team introduce una chiave: un identificatore dell’ordine logico. Nel nostro contratto fittizio, il fornitore restituisce l’esito precedente se riceve la stessa chiave; una chiave nuova significa un nuovo ordine. Orione conserva quindi la chiave anche nei ritentativi.

La nota collega incidente, contratto e verifica. Ora il vincolo importante è: lo stesso ordine mantiene la stessa identità. Il blocco del pulsante rimane, ma la protezione non si esaurisce nel gesto dell’utente.

### Complete explanation

Il fornitore crea l’ordine, ma la risposta non arriva a Orione. La persona vede ancora «in attesa» e ritenta. Un ritentativo è un nuovo invio per completare la stessa operazione, non un nuovo ordine voluto dalla persona.

Il team introduce una chiave: un identificatore dell’ordine logico. Nel nostro contratto fittizio, il fornitore restituisce l’esito precedente se riceve la stessa chiave; una chiave nuova significa un nuovo ordine. Orione conserva quindi la chiave anche nei ritentativi.

La nota collega incidente, contratto e verifica. Ora il vincolo importante è: lo stesso ordine mantiene la stessa identità. Il blocco del pulsante rimane, ma la protezione non si esaurisce nel gesto dell’utente.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Una terza modifica aggiunge una responsabilità che il prossimo fix dovrà rispettare.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S04
Module: M1
Objective: O1
Role: explanation
Title: Una notifica non è un nuovo ordine
Value contribution: rendere decisivi vincoli accumulati.

### Learner content

Orione aggiunge un’email di conferma. Durante un guasto l’email non parte, ma l’ordine è già stato creato. Il team separa le due attività: ritentare la notifica non deve inviare nuovamente l’ordine al fornitore.

Nei file conserva il motivo della separazione e una prova: un errore email non aumenta il numero di ordini. La cronologia ora contiene tre protezioni collegate: blocco del doppio clic, identità stabile dello stesso ordine, notifica separata.

Non devi memorizzare le date. Devi poter ritrovare le ragioni quando una nuova richiesta tocca quel comportamento. La comprensione professionale include le condizioni in cui una soluzione è stata introdotta, non solo il suo nome.

### Complete explanation

Orione aggiunge un’email di conferma. Durante un guasto l’email non parte, ma l’ordine è già stato creato. Il team separa le due attività: ritentare la notifica non deve inviare nuovamente l’ordine al fornitore.

Nei file conserva il motivo della separazione e una prova: un errore email non aumenta il numero di ordini. La cronologia ora contiene tre protezioni collegate: blocco del doppio clic, identità stabile dello stesso ordine, notifica separata.

Non devi memorizzare le date. Devi poter ritrovare le ragioni quando una nuova richiesta tocca quel comportamento. La comprensione professionale include le condizioni in cui una soluzione è stata introdotta, non solo il suo nome.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Arriva un baco che invita a rimuovere proprio quei controlli.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12

## S05
Module: M1
Objective: O1
Role: explanation
Title: La correzione ovvia può regredire
Value contribution: mostrare causalità della regressione senza attribuirla a qualsiasi sblocco.

### Learner content

Nuovo baco: dopo una conferma persa, il pulsante resta bloccato e la persona non può ritentare. L’agente propone: «Tolgo il blocco e genero una nuova chiave a ogni invio; il pulsante torna a funzionare».

Il sintomo visibile può sparire. Ma una nuova chiave può far creare un secondo ordine: il fornitore non la riconosce come ritentativo dello stesso ordine. Togliere soltanto il blocco, conservando la chiave, non avrebbe da solo questa conseguenza.

La storia suggerisce quindi una domanda precisa: quali controlli impediscono il doppio invio e quali impediscono inutilmente un recupero? Non stabilisce da sola la soluzione: occorre verificare il guasto attuale. Un fix localmente convincente non basta quando tocca garanzie nate in precedenza.

### Complete explanation

Nuovo baco: dopo una conferma persa, il pulsante resta bloccato e la persona non può ritentare. L’agente propone: «Tolgo il blocco e genero una nuova chiave a ogni invio; il pulsante torna a funzionare».

Il sintomo visibile può sparire. Ma una nuova chiave può far creare un secondo ordine: il fornitore non la riconosce come ritentativo dello stesso ordine. Togliere soltanto il blocco, conservando la chiave, non avrebbe da solo questa conseguenza.

La storia suggerisce quindi una domanda precisa: quali controlli impediscono il doppio invio e quali impediscono inutilmente un recupero? Non stabilisce da sola la soluzione: occorre verificare il guasto attuale. Un fix localmente convincente non basta quando tocca garanzie nate in precedenza.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

La conoscenza utile deve restare reperibile anche quando cambiano chat e agenti.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S06
Module: M1
Objective: O1
Role: explanation
Title: Patrimonio durevole, contesto del compito
Value contribution: definire skill e contesto collegandoli al beneficio.

### Learner content

Il contesto è il materiale disponibile al modello nella conversazione corrente. I file persistenti del progetto restano invece riapribili fra conversazioni. Conservare un file non significa che l’agente lo abbia letto: serve recuperarlo quando è pertinente.

Una skill è un insieme di istruzioni che l’agente carica per svolgere un tipo di lavoro. kb-agentic disciplina la conoscenza e le sue fonti; agentic-sdlc disciplina il cambiamento software; distill aiuta a scrivere testi che conservano le informazioni necessarie senza sommergerle.

L’“agente ingegnere” è un agente che può costruire su tracce consultate e aggiornate. Non si riaddestra durante queste attività. Il patrimonio può crescere mentre il contesto della singola attività rimane selezionato. Le istruzioni orientano il comportamento, ma non ne garantiscono l’esecuzione corretta.

### Complete explanation

Il contesto è il materiale disponibile al modello nella conversazione corrente. I file persistenti del progetto restano invece riapribili fra conversazioni. Conservare un file non significa che l’agente lo abbia letto: serve recuperarlo quando è pertinente.

Una skill è un insieme di istruzioni che l’agente carica per svolgere un tipo di lavoro. kb-agentic disciplina la conoscenza e le sue fonti; agentic-sdlc disciplina il cambiamento software; distill aiuta a scrivere testi che conservano le informazioni necessarie senza sommergerle.

L’“agente ingegnere” è un agente che può costruire su tracce consultate e aggiornate. Non si riaddestra durante queste attività. Il patrimonio può crescere mentre il contesto della singola attività rimane selezionato. Le istruzioni orientano il comportamento, ma non ne garantiscono l’esecuzione corretta.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Prova a formulare una richiesta che faccia emergere il vincolo, senza scrivere tu il design.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-14

## S07
Module: M1
Objective: O1
Role: check
Title: Che cosa chiedi davanti al fix?
Value contribution: verificare richiesta umana e ragione del beneficio.
Solution: S08

### Learner content

L’agente ti mostra la proposta di S05: nuova chiave a ogni invio e pulsante sbloccato. Dice: «Il test del pulsante passa, posso chiudere».

Come rispondi? Formula una richiesta che chiarisca quale comportamento precedente deve restare valido e quale evidenza manca. Spiega anche perché conservare e consultare la storia può aiutare una nuova sessione, e quando una buona nota curata potrebbe bastare.

Non devi produrre un’analisi al posto dell’agente: il tuo atto è decidere se accettare la chiusura e chiedere le verifiche necessarie. Prova prima di leggere la soluzione.

### Complete explanation

L’agente ti mostra la proposta di S05: nuova chiave a ogni invio e pulsante sbloccato. Dice: «Il test del pulsante passa, posso chiudere».

Come rispondi? Formula una richiesta che chiarisca quale comportamento precedente deve restare valido e quale evidenza manca. Spiega anche perché conservare e consultare la storia può aiutare una nuova sessione, e quando una buona nota curata potrebbe bastare.

Non devi produrre un’analisi al posto dell’agente: il tuo atto è decidere se accettare la chiusura e chiedere le verifiche necessarie. Prova prima di leggere la soluzione.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Confronta il tuo giudizio con una risposta motivata.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S08
Module: M1
Objective: O1
Role: solution
Title: Il beneficio non è il numero di documenti
Value contribution: correggere fiducia nei documenti e nel sintomo risolto.

### Learner content

Puoi rispondere: «Non chiudere sul solo pulsante. Recupera la decisione sulla chiave e il contratto del fornitore, verifica il guasto osservato e dimostra che un ritentativo dello stesso ordine non ne crea un altro. Controlla separatamente l’email».

La storia evita di ricostruire da zero una ragione già scoperta e rende verificabile il vincolo. Anche una nota curata, pertinente e mantenuta può ottenere questo risultato. Le skill cercano di rendere ripetibile il modo di conservarla, consultarla e aggiornarla.

«Abbiamo più documenti» non è una ragione sufficiente: se non vengono trovati o sono vecchi, possono peggiorare la decisione. Se hai approvato sul test del pulsante, torna a S03–S05 e confronta gesto visibile e ordine creato.

### Complete explanation

Puoi rispondere: «Non chiudere sul solo pulsante. Recupera la decisione sulla chiave e il contratto del fornitore, verifica il guasto osservato e dimostra che un ritentativo dello stesso ordine non ne crea un altro. Controlla separatamente l’email».

La storia evita di ricostruire da zero una ragione già scoperta e rende verificabile il vincolo. Anche una nota curata, pertinente e mantenuta può ottenere questo risultato. Le skill cercano di rendere ripetibile il modo di conservarla, consultarla e aggiornarla.

«Abbiamo più documenti» non è una ragione sufficiente: se non vengono trovati o sono vecchi, possono peggiorare la decisione. Se hai approvato sul test del pulsante, torna a S03–S05 e confronta gesto visibile e ordine creato.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Vediamo come kb-agentic rende controllabile una risposta sulle regole del fornitore.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S09
Module: M2
Objective: O2
Role: explanation
Title: Acquisire una fonte non è capirla
Value contribution: distinguere disponibilità, lettura e supporto della risposta.

### Learner content

Nel caso Orione l’agente riceve il contratto del fornitore. kb-agentic gli prescrive di conservarne una fonte riapribile con provenienza e di leggerla prima di estrarre affermazioni.

La provenienza indica da dove arriva un’informazione e a quale versione o passaggio risalire. Un documento copiato nel progetto ma mai letto è disponibile, non verificato. Se l’agente ha letto solo alcune parti, questo limite deve restare visibile.

La persona può chiedere: «Quale passaggio hai usato e che cosa non hai ancora letto?». Non deve fidarsi di una risposta solo perché il file compare in una cartella. Per un documento riservato, si usano accessi autorizzati; il nostro esempio non richiede di caricare dati reali.

### Complete explanation

Nel caso Orione l’agente riceve il contratto del fornitore. kb-agentic gli prescrive di conservarne una fonte riapribile con provenienza e di leggerla prima di estrarre affermazioni.

La provenienza indica da dove arriva un’informazione e a quale versione o passaggio risalire. Un documento copiato nel progetto ma mai letto è disponibile, non verificato. Se l’agente ha letto solo alcune parti, questo limite deve restare visibile.

La persona può chiedere: «Quale passaggio hai usato e che cosa non hai ancora letto?». Non deve fidarsi di una risposta solo perché il file compare in una cartella. Per un documento riservato, si usano accessi autorizzati; il nostro esempio non richiede di caricare dati reali.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Serve conservare anche le condizioni della frase che è stata ricavata.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3

## S10
Module: M2
Objective: O2
Role: explanation
Title: Un’affermazione ha un ambito
Value contribution: spiegare claim e ambito.

### Learner content

Un claim è un’affermazione registrata con fonte e stato. Nel contratto fittizio leggiamo: «Per il servizio Ordini, un ritentativo con la stessa chiave restituisce il precedente esito. Una nuova chiave crea un nuovo ordine».

Il claim non è semplicemente «i ritentativi sono sicuri». Ha un ambito: servizio Ordini e stessa chiave. Una risposta che elimina queste condizioni può essere fedele alle parole più brevi ma sbagliata per il lavoro da fare.

Davanti a una risposta dell’agente chiedi: «Questa regola copre proprio la nostra operazione? Dove sono le condizioni?». L’agente estrae e organizza i claim; tu controlli la risposta e decidi se usarla. Una sintesi non sostituisce la fonte quando il suo significato è decisivo.

### Complete explanation

Un claim è un’affermazione registrata con fonte e stato. Nel contratto fittizio leggiamo: «Per il servizio Ordini, un ritentativo con la stessa chiave restituisce il precedente esito. Una nuova chiave crea un nuovo ordine».

Il claim non è semplicemente «i ritentativi sono sicuri». Ha un ambito: servizio Ordini e stessa chiave. Una risposta che elimina queste condizioni può essere fedele alle parole più brevi ma sbagliata per il lavoro da fare.

Davanti a una risposta dell’agente chiedi: «Questa regola copre proprio la nostra operazione? Dove sono le condizioni?». L’agente estrae e organizza i claim; tu controlli la risposta e decidi se usarla. Una sintesi non sostituisce la fonte quando il suo significato è decisivo.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Come si trova il claim senza rileggere tutto il patrimonio?

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S11
Module: M2
Objective: O2
Role: explanation
Title: Recuperare ciò che serve, non tutto
Value contribution: motivare selezione e limite del recupero.

### Learner content

La KB organizza le affermazioni per argomenti e relazioni. Un grafo è una struttura di elementi collegati: qui aiuta a passare dalla domanda «possiamo ritentare?» all’argomento Ordini, poi alle regole pertinenti e alle fonti.

Questo grafo degli argomenti appartiene alla conoscenza del progetto. Il grafo dei prerequisiti di un corso ha invece concetti collegati secondo ciò che occorre capire prima: ordina le spiegazioni. Cercare una regola sugli ordini nella KB e scegliere cosa insegnare prima sono due lavori diversi.

Un indice è un elenco di riferimenti, non il documento che descrive ogni regola. L’agente usa riferimenti e ricerca per selezionare che cosa aprire. Se trova una sintesi derivata da un’altra nota, deve poter risalire al suo fondamento quando serve per decidere.

L’obiettivo è recuperare tutte e solo le informazioni necessarie al compito. È una disciplina di selezione, non una garanzia che ogni ricerca sia completa. Se il materiale non si trova, chiedi quali percorsi sono stati cercati: «non trovato» non significa «non esiste».

### Complete explanation

La KB organizza le affermazioni per argomenti e relazioni. Un grafo è una struttura di elementi collegati: qui aiuta a passare dalla domanda «possiamo ritentare?» all’argomento Ordini, poi alle regole pertinenti e alle fonti.

Questo grafo degli argomenti appartiene alla conoscenza del progetto. Il grafo dei prerequisiti di un corso ha invece concetti collegati secondo ciò che occorre capire prima: ordina le spiegazioni. Cercare una regola sugli ordini nella KB e scegliere cosa insegnare prima sono due lavori diversi.

Un indice è un elenco di riferimenti, non il documento che descrive ogni regola. L’agente usa riferimenti e ricerca per selezionare che cosa aprire. Se trova una sintesi derivata da un’altra nota, deve poter risalire al suo fondamento quando serve per decidere.

L’obiettivo è recuperare tutte e solo le informazioni necessarie al compito. È una disciplina di selezione, non una garanzia che ogni ricerca sia completa. Se il materiale non si trova, chiedi quali percorsi sono stati cercati: «non trovato» non significa «non esiste».

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Una fonte citata può comunque sostenere una risposta troppo ampia.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S12
Module: M2
Objective: O2
Role: check
Title: Accetti questa risposta?
Value contribution: trasferire giudizio sull’ambito a operazione diversa.
Solution: S13

### Learner content

Caso fittizio nuovo: una collega vuole inviare un secondo ordine, diverso dal primo. Chiedi all’agente se può riusare la vecchia chiave. Risponde: «Sì, il contratto dice che usare la stessa chiave evita duplicati»; non mostra il passaggio né distingue nuovo ordine e ritentativo.

Che cosa contesti? Formula la richiesta da rivolgere all’agente prima di inoltrare la risposta alla collega. Non compilare tu il claim o la risposta corretta al suo posto. Il tuo compito è verificare se il risultato proposto è utilizzabile.

### Complete explanation

Caso fittizio nuovo: una collega vuole inviare un secondo ordine, diverso dal primo. Chiedi all’agente se può riusare la vecchia chiave. Risponde: «Sì, il contratto dice che usare la stessa chiave evita duplicati»; non mostra il passaggio né distingue nuovo ordine e ritentativo.

Che cosa contesti? Formula la richiesta da rivolgere all’agente prima di inoltrare la risposta alla collega. Non compilare tu il claim o la risposta corretta al suo posto. Il tuo compito è verificare se il risultato proposto è utilizzabile.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

La differenza decisiva è l’identità dell’operazione, non la parola sicuro.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S13
Module: M2
Objective: O2
Role: solution
Title: La citazione deve sostenere la decisione
Value contribution: soluzione e correzione mirata.

### Learner content

Chiedi: «Mostra il passaggio e distingui un nuovo ordine da un ritentativo dello stesso ordine. La regola sulla stessa chiave vale per l’operazione della collega?».

Nel nostro contratto fittizio la stessa chiave restituisce il precedente esito. Non crea il secondo ordine voluto: l’agente deve correggere la risposta mantenendo quella distinzione. La fonte era pertinente al tema ma la conclusione non rispettava l’ambito.

Se hai accettato perché compariva la parola “contratto”, torna a S10. La provenienza permette di controllare, non rende automaticamente giusta l’inferenza. Questo è il giudizio della persona; l’estrazione e la registrazione restano lavoro dell’agente.

### Complete explanation

Chiedi: «Mostra il passaggio e distingui un nuovo ordine da un ritentativo dello stesso ordine. La regola sulla stessa chiave vale per l’operazione della collega?».

Nel nostro contratto fittizio la stessa chiave restituisce il precedente esito. Non crea il secondo ordine voluto: l’agente deve correggere la risposta mantenendo quella distinzione. La fonte era pertinente al tema ma la conclusione non rispettava l’ambito.

Se hai accettato perché compariva la parola “contratto”, torna a S10. La provenienza permette di controllare, non rende automaticamente giusta l’inferenza. Questo è il giudizio della persona; l’estrazione e la registrazione restano lavoro dell’agente.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Anche una risposta valida oggi può diventare inadeguata quando cambia la fonte.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S14
Module: M3
Objective: O3
Role: explanation
Title: Una ragione storica non è una regola eterna
Value contribution: insegnare validità temporale e revisione.

### Learner content

Il contratto iniziale permetteva il recupero dell’esito per un giorno. Una nuova versione, dal mese successivo, lo permette per sette giorni. I periodi non si sovrappongono: la vecchia nota può ancora spiegare una scelta di allora, ma non basta a decidere per un ordine di oggi.

Il caso e i numeri sono inventati. Il punto è distinguere validità storica da validità corrente. Una fonte conservata non resta attuale solo perché è facile da recuperare.

kb-agentic prescrive di mantenere visibili stato e sostituzioni delle informazioni. Quando una regola cambia, vanno riesaminati i documenti e le decisioni che dipendevano da essa. L’elenco dei dipendenti aiuta a farlo; non aggiorna automaticamente il software.

### Complete explanation

Il contratto iniziale permetteva il recupero dell’esito per un giorno. Una nuova versione, dal mese successivo, lo permette per sette giorni. I periodi non si sovrappongono: la vecchia nota può ancora spiegare una scelta di allora, ma non basta a decidere per un ordine di oggi.

Il caso e i numeri sono inventati. Il punto è distinguere validità storica da validità corrente. Una fonte conservata non resta attuale solo perché è facile da recuperare.

kb-agentic prescrive di mantenere visibili stato e sostituzioni delle informazioni. Quando una regola cambia, vanno riesaminati i documenti e le decisioni che dipendevano da essa. L’elenco dei dipendenti aiuta a farlo; non aggiorna automaticamente il software.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Due documenti dello stesso periodo richiedono un controllo diverso.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S15
Module: M3
Objective: O3
Role: explanation
Title: Quando le fonti sembrano contraddirsi
Value contribution: separare evidenza e preferenza.

### Learner content

Due documenti fittizi, entrambi validi oggi, riportano finestre diverse: sette giorni e un giorno. L’agente afferma che valgono per lo stesso servizio e tipo di operazione, ma non riesce a verificare questa attribuzione.

Scegliere il documento più recente non risolve quella mancanza. La procedura KB mantiene visibili le affermazioni contestate e chiede il chiarimento che può decidere l’ambito. “Contestato” significa che il risultato non va usato come fatto risolto.

Una preferenza del team, «vorremmo sette giorni», può essere una scelta di prodotto, ma non prova cosa garantisca il fornitore. La persona può indicare una fonte, chi conosce il fatto o decidere di rinviare l’affermazione non verificata.

### Complete explanation

Due documenti fittizi, entrambi validi oggi, riportano finestre diverse: sette giorni e un giorno. L’agente afferma che valgono per lo stesso servizio e tipo di operazione, ma non riesce a verificare questa attribuzione.

Scegliere il documento più recente non risolve quella mancanza. La procedura KB mantiene visibili le affermazioni contestate e chiede il chiarimento che può decidere l’ambito. “Contestato” significa che il risultato non va usato come fatto risolto.

Una preferenza del team, «vorremmo sette giorni», può essere una scelta di prodotto, ma non prova cosa garantisca il fornitore. La persona può indicare una fonte, chi conosce il fatto o decidere di rinviare l’affermazione non verificata.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Un fatto nuovo può risolvere il contrasto senza cancellarne la storia.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S16
Module: M3
Objective: O3
Role: explanation
Title: Il chiarimento deve raggiungere chi lo usava
Value contribution: mostrare aggiornamento oltre il claim isolato.

### Learner content

Arriva un chiarimento riapribile: il documento con un giorno riguarda Notifiche, quello con sette giorni riguarda Ordini. L’agente può correggere la precedente attribuzione, conservandone il superamento e la fonte del chiarimento.

La nota che aveva assunto un giorno per gli ordini deve essere riesaminata. Anche il piano che ne derivava va controllato. Una conoscenza corretta nel registro e una conclusione vecchia nel piano sono ancora una possibile regressione.

L’agente non deve rileggere la propria interpretazione come se fosse una nuova prova. Le catene di provenienza servono a riaprire il fondamento e a riconoscere ciò che è derivato. Nessun indice garantisce da solo che tutti i dipendenti siano stati individuati.

### Complete explanation

Arriva un chiarimento riapribile: il documento con un giorno riguarda Notifiche, quello con sette giorni riguarda Ordini. L’agente può correggere la precedente attribuzione, conservandone il superamento e la fonte del chiarimento.

La nota che aveva assunto un giorno per gli ordini deve essere riesaminata. Anche il piano che ne derivava va controllato. Una conoscenza corretta nel registro e una conclusione vecchia nel piano sono ancora una possibile regressione.

L’agente non deve rileggere la propria interpretazione come se fosse una nuova prova. Le catene di provenienza servono a riaprire il fondamento e a riconoscere ciò che è derivato. Nessun indice garantisce da solo che tutti i dipendenti siano stati individuati.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Prova a giudicare una risposta che anticipa il chiarimento con una preferenza.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S17
Module: M3
Objective: O3
Role: check
Title: La recenza basta?
Value contribution: giudicare escalation su fatto non noto.
Solution: S18

### Learner content

In un altro progetto inventato, l’agente trova due regole dello stesso mese per la conservazione di ricevute. Non ha accertato se una riguardi copie di prova e l’altra ricevute definitive. Dice: «Scelgo quella più nuova; dimmi soltanto quale durata preferisci».

Quale parte della risposta contesti e quale chiarimento chiedi? Se non conosci il fatto, come rispondi senza inventarlo? Il problema non richiede di classificare tu un conflitto: l’agente ha già mostrato l’incertezza e la proposta da giudicare.

### Complete explanation

In un altro progetto inventato, l’agente trova due regole dello stesso mese per la conservazione di ricevute. Non ha accertato se una riguardi copie di prova e l’altra ricevute definitive. Dice: «Scelgo quella più nuova; dimmi soltanto quale durata preferisci».

Quale parte della risposta contesti e quale chiarimento chiedi? Se non conosci il fatto, come rispondi senza inventarlo? Il problema non richiede di classificare tu un conflitto: l’agente ha già mostrato l’incertezza e la proposta da giudicare.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

La soluzione conserva la distinzione tra preferenza e prova.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S18
Module: M3
Objective: O3
Role: solution
Title: Non scegliere un fatto per preferenza
Value contribution: soluzione con percorso di correzione.

### Learner content

Contesti la scelta per recenza e chiedi di verificare a quali ricevute si riferiscono le fonti. Se non sai rispondere, indichi chi può fornire il documento o chiedi di mantenere aperta la conclusione.

Puoi decidere che il lavoro proceda su parti non dipendenti dal dato incerto. Non puoi rendere vera una garanzia del fornitore soltanto approvandola. Dopo il chiarimento chiedi la risposta corretta con fonte e i riferimenti alle conclusioni da riesaminare.

Se hai risposto solo con la durata che preferisci, torna a S15. Una scelta di perimetro è tua; l’evidenza su cosa esiste deve provenire da un fatto controllabile.

### Complete explanation

Contesti la scelta per recenza e chiedi di verificare a quali ricevute si riferiscono le fonti. Se non sai rispondere, indichi chi può fornire il documento o chiedi di mantenere aperta la conclusione.

Puoi decidere che il lavoro proceda su parti non dipendenti dal dato incerto. Non puoi rendere vera una garanzia del fornitore soltanto approvandola. Dopo il chiarimento chiedi la risposta corretta con fonte e i riferimenti alle conclusioni da riesaminare.

Se hai risposto solo con la durata che preferisci, torna a S15. Una scelta di perimetro è tua; l’evidenza su cosa esiste deve provenire da un fatto controllabile.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Quando l’informazione diventa modifica software, serve un’altra disciplina.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S19
Module: M4
Objective: O4
Role: explanation
Title: Più metodo non deve significare più burocrazia
Value contribution: rispondere al timore di rigidità con criterio concreto.

### Learner content

Un’obiezione ragionevole è: «Se devo documentare tutto, rallento e magari peggioro il risultato». agentic-sdlc distingue lavori proporzionati al rischio: L1 per correzioni banali senza cambiamento di comportamento, L2 per modifiche piccole a causa chiara e basso rischio, L3 per cambiamenti significativi, contratti o rischi maggiori. Spike è un’esplorazione non ancora pronta per produzione.

L’agente dichiara il livello; la persona può contestarlo. Una riga che cambia l’identità di un ordine non è innocua perché è corta. Un refuso isolato non deve pagare il costo di un design significativo.

Tempo, letture e verifiche hanno un costo reale. La proporzione va giudicata sul compito, non sulla volontà di “fare il metodo”.

### Complete explanation

Un’obiezione ragionevole è: «Se devo documentare tutto, rallento e magari peggioro il risultato». agentic-sdlc distingue lavori proporzionati al rischio: L1 per correzioni banali senza cambiamento di comportamento, L2 per modifiche piccole a causa chiara e basso rischio, L3 per cambiamenti significativi, contratti o rischi maggiori. Spike è un’esplorazione non ancora pronta per produzione.

L’agente dichiara il livello; la persona può contestarlo. Una riga che cambia l’identità di un ordine non è innocua perché è corta. Un refuso isolato non deve pagare il costo di un design significativo.

Tempo, letture e verifiche hanno un costo reale. La proporzione va giudicata sul compito, non sulla volontà di “fare il metodo”.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Anche una modifica ben verificata può inseguire il beneficio sbagliato.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6

## S20
Module: M4
Objective: O4
Role: explanation
Title: La Vision conserva il perché del cambiamento
Value contribution: distinguere riuscita tecnica e beneficio.

### Learner content

La Vision dichiara beneficio, destinatari, limiti e segnali di successo. Per Orione il beneficio fittizio è permettere il recupero di un invio incerto senza creare un secondo ordine e senza confondere l’email con l’ordine.

La sviluppatrice vuole verificare i percorsi toccati; il responsabile tecnico vuole sapere quale risultato verrà ottenuto e quali scelte restano aperte. Entrambi hanno bisogno di una proposta coerente con il beneficio.

Un nuovo menu commerciale non risolve quel baco. Se l’agente lo aggiunge, chiedi di separarlo o discutere il cambiamento di perimetro. La Vision approvata non va riscritta silenziosamente per giustificare ciò che l’agente ha già deciso di costruire.

### Complete explanation

La Vision dichiara beneficio, destinatari, limiti e segnali di successo. Per Orione il beneficio fittizio è permettere il recupero di un invio incerto senza creare un secondo ordine e senza confondere l’email con l’ordine.

La sviluppatrice vuole verificare i percorsi toccati; il responsabile tecnico vuole sapere quale risultato verrà ottenuto e quali scelte restano aperte. Entrambi hanno bisogno di una proposta coerente con il beneficio.

Un nuovo menu commerciale non risolve quel baco. Se l’agente lo aggiunge, chiedi di separarlo o discutere il cambiamento di perimetro. La Vision approvata non va riscritta silenziosamente per giustificare ciò che l’agente ha già deciso di costruire.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Valuta una proposta che usa la dimensione del diff come unico criterio.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-7

## S21
Module: M4
Objective: O4
Role: check
Title: Una riga può cambiare un contratto
Value contribution: verificare giudizio umano su triage e scope.
Solution: S22

### Learner content

L’agente propone la nuova chiave a ogni invio e dichiara L2: «È una sola riga». Aggiunge un menu di analisi commerciale per “rendere completo il miglioramento”.

Come rispondi sul livello e sul perimetro? Usa gli effetti della modifica e il beneficio concordato. Non ti chiediamo di classificare una richiesta prima dell’agente: stai giudicando la sua dichiarazione e scegliendo quali obiettivi autorizzare.

### Complete explanation

L’agente propone la nuova chiave a ogni invio e dichiara L2: «È una sola riga». Aggiunge un menu di analisi commerciale per “rendere completo il miglioramento”.

Come rispondi sul livello e sul perimetro? Usa gli effetti della modifica e il beneficio concordato. Non ti chiediamo di classificare una richiesta prima dell’agente: stai giudicando la sua dichiarazione e scegliendo quali obiettivi autorizzare.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Confronta dimensione della modifica e conseguenza per l’utente.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6

## S22
Module: M4
Objective: O4
Role: solution
Title: Giudicare effetti e confini
Value contribution: soluzione proporzionata.

### Learner content

Contesti L2 perché la proposta altera il contratto fra ritentativo e identità dell’ordine, con rischio di duplicazione. Chiedi all’agente di rivedere livello e analisi in base agli effetti, non alle righe.

Rifiuti il menu dentro questo fix: se interessa, sarà una scelta separata di perimetro. Per un refuso senza nuovi effetti, invece, non chiederesti tutti gli artefatti di un L3.

Se hai scelto solo in base alla lunghezza del diff, torna a S19. Se hai approvato il menu perché è utile in generale, torna a S20: utilità e appartenenza al beneficio attuale sono domande diverse.

### Complete explanation

Contesti L2 perché la proposta altera il contratto fra ritentativo e identità dell’ordine, con rischio di duplicazione. Chiedi all’agente di rivedere livello e analisi in base agli effetti, non alle righe.

Rifiuti il menu dentro questo fix: se interessa, sarà una scelta separata di perimetro. Per un refuso senza nuovi effetti, invece, non chiederesti tutti gli artefatti di un L3.

Se hai scelto solo in base alla lunghezza del diff, torna a S19. Se hai approvato il menu perché è utile in generale, torna a S20: utilità e appartenenza al beneficio attuale sono domande diverse.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Prima della soluzione definitiva, occorre osservare il guasto effettivo.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6

## S23
Module: M5
Objective: O5
Role: explanation
Title: Osservare il baco prima di spiegarlo
Value contribution: insegnare evidenza prima della causa immaginata.

### Learner content

Nel caso Orione abbiamo log fittizi: invio con chiave K, ordine creato dal fornitore, conferma non ricevuta, pulsante ancora bloccato. K è solo il nome della chiave nel racconto.

Questi eventi danno una domanda concreta al codice: perché lo stato incerto impedisce un ritentativo con K? Non provano che qualsiasi controllo sia sbagliato. L’agente deve partire dalle evidenze disponibili, controllarne ambito e mantenere le ipotesi con verifiche e risultati.

Puoi chiedere: «Quale osservazione sostiene questa causa? Quali alternative sono state escluse?». Cercare pattern sospetti nel sorgente può suggerire ipotesi; non collega da solo quel pattern all’incidente.

### Complete explanation

Nel caso Orione abbiamo log fittizi: invio con chiave K, ordine creato dal fornitore, conferma non ricevuta, pulsante ancora bloccato. K è solo il nome della chiave nel racconto.

Questi eventi danno una domanda concreta al codice: perché lo stato incerto impedisce un ritentativo con K? Non provano che qualsiasi controllo sia sbagliato. L’agente deve partire dalle evidenze disponibili, controllarne ambito e mantenere le ipotesi con verifiche e risultati.

Puoi chiedere: «Quale osservazione sostiene questa causa? Quali alternative sono state escluse?». Cercare pattern sospetti nel sorgente può suggerire ipotesi; non collega da solo quel pattern all’incidente.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

La correzione deve descrivere il comportamento desiderato oltre il pulsante.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-16

## S24
Module: M5
Objective: O5
Role: explanation
Title: Dai bisogni al comportamento osservabile
Value contribution: spiegare artefatti a partire dal loro scopo.

### Learner content

Un use case descrive cosa deve ottenere una persona: la cliente vuole sapere se l’ordine è stato accettato; l’operatrice vuole recuperare l’invio senza duplicarlo. La specifica funzionale descrive che cosa il software deve fare per quei bisogni, prima di scegliere come implementarlo.

Nel caso: stesso ordine mantiene K; conferma assente produce uno stato incerto visibile, non “fallito” certo; ritentativo con K può recuperare l’esito; email fallita rimane un problema distinto. Un nuovo ordine voluto riceve invece una nuova identità.

La persona approva il risultato e prende le scelte che l’agente le sottopone, per esempio quale informazione mostrare durante l’attesa. L’agente prepara specifica e analisi, non la persona al suo posto.

### Complete explanation

Un use case descrive cosa deve ottenere una persona: la cliente vuole sapere se l’ordine è stato accettato; l’operatrice vuole recuperare l’invio senza duplicarlo. La specifica funzionale descrive che cosa il software deve fare per quei bisogni, prima di scegliere come implementarlo.

Nel caso: stesso ordine mantiene K; conferma assente produce uno stato incerto visibile, non “fallito” certo; ritentativo con K può recuperare l’esito; email fallita rimane un problema distinto. Un nuovo ordine voluto riceve invece una nuova identità.

La persona approva il risultato e prende le scelte che l’agente le sottopone, per esempio quale informazione mostrare durante l’attesa. L’agente prepara specifica e analisi, non la persona al suo posto.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Lo stesso comportamento attraversa più superfici.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8

## S25
Module: M5
Objective: O5
Role: explanation
Title: Seguire il percorso, non un solo schermo
Value contribution: mostrare blast radius attraverso flussi accessibili.

### Learner content

Una superficie è ciò su cui una persona o un software agisce o riceve un risultato. Orione ha pulsante, pannello di stato, richiesta al fornitore e notifica email. Il contratto d’interfaccia descrive il percorso e il feedback fra queste responsabilità.

Se il pannello mostra “completato” ma l’email dice “fallito”, l’esperienza è incoerente. Se l’email ritenta l’ordine, la separazione storica è stata violata. Il modello dei rischi collega queste possibilità a controlli e verifiche.

Chi sviluppa chiede dove lo stato viene consumato; chi guida il lavoro chiede quali esiti sono accettabili e quali restano incerti. Un elenco di file non sostituisce questo quadro.

### Complete explanation

Una superficie è ciò su cui una persona o un software agisce o riceve un risultato. Orione ha pulsante, pannello di stato, richiesta al fornitore e notifica email. Il contratto d’interfaccia descrive il percorso e il feedback fra queste responsabilità.

Se il pannello mostra “completato” ma l’email dice “fallito”, l’esperienza è incoerente. Se l’email ritenta l’ordine, la separazione storica è stata violata. Il modello dei rischi collega queste possibilità a controlli e verifiche.

Chi sviluppa chiede dove lo stato viene consumato; chi guida il lavoro chiede quali esiti sono accettabili e quali restano incerti. Un elenco di file non sostituisce questo quadro.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Una buona soluzione riusa le responsabilità già presenti.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8

## S26
Module: M5
Objective: O5
Role: explanation
Title: Riusare ciò che già mantiene il vincolo
Value contribution: motivare riuso e design pulito.

### Learner content

Il Capability Ledger è il registro delle capacità necessarie e delle evidenze su ciò che esiste già. Nell’indagine fittizia l’agente trova la funzione che conserva K e il percorso distinto delle notifiche.

Propone di correggere la transizione dallo stato incerto al recupero consentito, riusando l’identità dell’ordine. Non propone una seconda implementazione del controllo di duplicazione in ogni schermo. Se una capacità non viene trovata, deve mostrare che cosa ha cercato prima di dichiararla mancante.

L’Impact indica quali parti cambiano e perché; il design specifica integrazioni, condizioni e verifiche. Il tuo giudizio è chiedere se il disegno preserva le garanzie e si fonda su evidenze, non compilare il registro al posto dell’agente.

### Complete explanation

Il Capability Ledger è il registro delle capacità necessarie e delle evidenze su ciò che esiste già. Nell’indagine fittizia l’agente trova la funzione che conserva K e il percorso distinto delle notifiche.

Propone di correggere la transizione dallo stato incerto al recupero consentito, riusando l’identità dell’ordine. Non propone una seconda implementazione del controllo di duplicazione in ogni schermo. Se una capacità non viene trovata, deve mostrare che cosa ha cercato prima di dichiararla mancante.

L’Impact indica quali parti cambiano e perché; il design specifica integrazioni, condizioni e verifiche. Il tuo giudizio è chiedere se il disegno preserva le garanzie e si fonda su evidenze, non compilare il registro al posto dell’agente.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Il design deve essere controllato prima di diventare codice.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8

## S27
Module: M5
Objective: O5
Role: explanation
Title: Prevenire l’errore dove nasce
Value contribution: collegare prevenzione e review al beneficio.

### Learner content

Poka-Yoke significa prevenire un uso errato o renderlo subito visibile. Nel caso, la responsabilità che identifica l’ordine deve mantenere K sui ritentativi; la notifica non deve poter creare un nuovo invio.

Una correzione pulita distingue nuovo ordine, recupero e notifica nelle responsabilità appropriate. Una serie di eccezioni “se succede questo baco” può lasciare altre strade incoerenti. Il criterio richiesto dal metodo è: «Dopo la correzione il software deve essere fatto come se fosse stato progettato senza quel difetto».

Un revisore indipendente controlla il design contro beneficio, rischi e sistema reale prima dell’implementazione. “Indipendente” richiede un contesto distinto dall’autore: un secondo passaggio dello stesso autore è una verifica diversa, da dichiarare come tale.

### Complete explanation

Poka-Yoke significa prevenire un uso errato o renderlo subito visibile. Nel caso, la responsabilità che identifica l’ordine deve mantenere K sui ritentativi; la notifica non deve poter creare un nuovo invio.

Una correzione pulita distingue nuovo ordine, recupero e notifica nelle responsabilità appropriate. Una serie di eccezioni “se succede questo baco” può lasciare altre strade incoerenti. Il criterio richiesto dal metodo è: «Dopo la correzione il software deve essere fatto come se fosse stato progettato senza quel difetto».

Un revisore indipendente controlla il design contro beneficio, rischi e sistema reale prima dell’implementazione. “Indipendente” richiede un contesto distinto dall’autore: un secondo passaggio dello stesso autore è una verifica diversa, da dichiarare come tale.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

La review non sostituisce le prove sul comportamento.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-16
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9

## S28
Module: M5
Objective: O5
Role: explanation
Title: Che cosa dimostrano le prove?
Value contribution: distinguere prova locale e chiusura completa.

### Learner content

L’agente deve verificare almeno gli esiti rilevanti del caso: due clic, conferma persa e recupero con K, nuovo ordine voluto con identità distinta, email fallita senza nuovo invio. Una prova del pulsante non dimostra tutti questi comportamenti.

Dopo l’implementazione, la review confronta il risultato con il design e le evidenze. La chiusura aggiorna ragioni, prove, stato e riferimenti. Una GUIDE può conservare un modello operativo riusabile: per esempio come identità e notifiche sono separate, con provenienza controllabile.

Le guide operative si trovano in ai_docs/reference/: il suo INDEX.md indirizza alla guida pertinente. Una nuova sessione consulta quel riferimento prima di agire e riapre la guida quando riguarda il compito. Un elenco presente ma non consultato non protegge il cambiamento.

Non ogni fix richiede una guida nuova. Test verdi e review sono evidenze con un ambito; non provano che ogni percorso sia corretto né che le skill migliorino sempre il lavoro.

### Complete explanation

L’agente deve verificare almeno gli esiti rilevanti del caso: due clic, conferma persa e recupero con K, nuovo ordine voluto con identità distinta, email fallita senza nuovo invio. Una prova del pulsante non dimostra tutti questi comportamenti.

Dopo l’implementazione, la review confronta il risultato con il design e le evidenze. La chiusura aggiorna ragioni, prove, stato e riferimenti. Una GUIDE può conservare un modello operativo riusabile: per esempio come identità e notifiche sono separate, con provenienza controllabile.

Le guide operative si trovano in ai_docs/reference/: il suo INDEX.md indirizza alla guida pertinente. Una nuova sessione consulta quel riferimento prima di agire e riapre la guida quando riguarda il compito. Un elenco presente ma non consultato non protegge il cambiamento.

Non ogni fix richiede una guida nuova. Test verdi e review sono evidenze con un ambito; non provano che ogni percorso sia corretto né che le skill migliorino sempre il lavoro.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Valuta una chiusura che omette il vincolo più importante.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S29
Module: M5
Objective: O5
Role: check
Title: Puoi approvare la chiusura?
Value contribution: valutare con ragione causale e ambito della prova.
Solution: S30

### Learner content

L’agente dichiara: «Ho sbloccato il pulsante. Il test UI è verde. Ho conservato una nota “problema risolto”. Non ho verificato conferma persa né percorso email».

Quale parte accetti e quali evidenze chiedi prima della chiusura? Spiega quale ragione della storia di Orione rende insufficienti il test e la nota. Non scrivere tu codice o piano dei test: formula la richiesta e la decisione sul lavoro presentato.

Una sessione futura deve ritrovare la guida sulla separazione delle notifiche. Dove chiedi all’agente di cercarla, prima di riscriverla?

### Complete explanation

L’agente dichiara: «Ho sbloccato il pulsante. Il test UI è verde. Ho conservato una nota “problema risolto”. Non ho verificato conferma persa né percorso email».

Quale parte accetti e quali evidenze chiedi prima della chiusura? Spiega quale ragione della storia di Orione rende insufficienti il test e la nota. Non scrivere tu codice o piano dei test: formula la richiesta e la decisione sul lavoro presentato.

Una sessione futura deve ritrovare la guida sulla separazione delle notifiche. Dove chiedi all’agente di cercarla, prima di riscriverla?

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

La soluzione distingue risultato parziale e chiusura.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S30
Module: M5
Objective: O5
Role: solution
Title: Un test verde ha un perimetro
Value contribution: soluzione specifica anziché checklist generica.

### Learner content

Puoi accettare il risultato sul pulsante come prova locale, ma non la chiusura. Chiedi verifica del recupero con K, dell’ordine realmente creato e della separazione email, con confronto al design e ai vincoli precedenti.

La nota “problema risolto” non permette una ripresa affidabile: mancano causa supportata, cambiamento, prove, limiti e riferimenti. Chiedi che l’agente conservi ciò che è utile al progetto, senza incollare tutta la conversazione.

Se hai chiesto soltanto “più test”, torna a S03–S04 e S28. Il criterio utile è quale comportamento rischia di regredire e quale osservazione può verificarlo.

Per la guida chiedi di consultare ai_docs/reference/INDEX.md e aprire il riferimento pertinente in ai_docs/reference/. Non trattare una guida non letta come un controllo eseguito.

### Complete explanation

Puoi accettare il risultato sul pulsante come prova locale, ma non la chiusura. Chiedi verifica del recupero con K, dell’ordine realmente creato e della separazione email, con confronto al design e ai vincoli precedenti.

La nota “problema risolto” non permette una ripresa affidabile: mancano causa supportata, cambiamento, prove, limiti e riferimenti. Chiedi che l’agente conservi ciò che è utile al progetto, senza incollare tutta la conversazione.

Se hai chiesto soltanto “più test”, torna a S03–S04 e S28. Il criterio utile è quale comportamento rischia di regredire e quale osservazione può verificarlo.

Per la guida chiedi di consultare ai_docs/reference/INDEX.md e aprire il riferimento pertinente in ai_docs/reference/. Non trattare una guida non letta come un controllo eseguito.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Conservare il risultato permette di alleggerire il contesto della prossima attività.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S31
Module: M6
Objective: O6
Role: explanation
Title: Tre contributi, un patrimonio del progetto
Value contribution: spiegare supporto distill senza terzo corso autonomo.

### Learner content

kb-agentic governa la fedeltà della conoscenza alle fonti: che cosa sappiamo, da dove e con quali limiti. agentic-sdlc governa il cambiamento software: perché lo facciamo, che cosa deve ottenere e come lo verifichiamo. distill governa la scrittura: quali informazioni il lettore deve ricevere per agire correttamente.

distill non significa “taglia il più possibile”. Se la nota elimina la condizione “stessa chiave”, è più corta ma ha perso un fatto decisivo. Se la condizione resta nascosta in molte pagine irrilevanti, il lettore può comunque non usarla.

Conoscenza, esperienza registrata e spiegazioni si sostengono, ma non si equivalgono. distill non decide se il contratto sia vero e non sostituisce le verifiche del software.

### Complete explanation

kb-agentic governa la fedeltà della conoscenza alle fonti: che cosa sappiamo, da dove e con quali limiti. agentic-sdlc governa il cambiamento software: perché lo facciamo, che cosa deve ottenere e come lo verifichiamo. distill governa la scrittura: quali informazioni il lettore deve ricevere per agire correttamente.

distill non significa “taglia il più possibile”. Se la nota elimina la condizione “stessa chiave”, è più corta ma ha perso un fatto decisivo. Se la condizione resta nascosta in molte pagine irrilevanti, il lettore può comunque non usarla.

Conoscenza, esperienza registrata e spiegazioni si sostengono, ma non si equivalgono. distill non decide se il contratto sia vero e non sostituisce le verifiche del software.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Questo patrimonio deve restare disponibile nella cartella corretta.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-14
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S32
Module: M6
Objective: O6
Role: explanation
Title: Il folder conta più della chat
Value contribution: insegnare condizioni operative e confini.

### Learner content

Lavora nel folder persistente del progetto. Le skill sono installate nell’ambiente dell’agente; fonti, decisioni, analisi e handoff prodotti appartengono al progetto, spesso sotto ai_docs/. Un handoff è un passaggio di consegne sullo stato del lavoro e sul punto da cui riprendere.

Le due skill funzionano in Standalone con i file. devPNT è un prodotto separato che può aggiungere governance quando configurato: non è necessario per seguire il corso o rendere utilizzabile il patrimonio. Qui non lo usiamo.

In Standalone l’analisi autorevole del cambiamento è il file ANALYSIS in ai_docs/solutions/. Con devPNT configurato, piani e artefatti governati passano invece per proposte versionate: la persona le approva, poi ne vengono conservate copie di consultazione nei file. Le guide operative restano leggibili in ai_docs/reference/. Una copia non sostituisce l’artefatto governato approvato. Sono due modalità di autorità, non due modi di garantire che l’agente abbia capito.

Su più progetti, una conoscenza trasferibile può essere riusata solo rispettando provenienza, ambito e autorizzazioni. Non assumere che una regola di Orione sia valida ovunque o che aprire una chat nuova renda accessibili cartelle diverse.

### Complete explanation

Lavora nel folder persistente del progetto. Le skill sono installate nell’ambiente dell’agente; fonti, decisioni, analisi e handoff prodotti appartengono al progetto, spesso sotto ai_docs/. Un handoff è un passaggio di consegne sullo stato del lavoro e sul punto da cui riprendere.

Le due skill funzionano in Standalone con i file. devPNT è un prodotto separato che può aggiungere governance quando configurato: non è necessario per seguire il corso o rendere utilizzabile il patrimonio. Qui non lo usiamo.

In Standalone l’analisi autorevole del cambiamento è il file ANALYSIS in ai_docs/solutions/. Con devPNT configurato, piani e artefatti governati passano invece per proposte versionate: la persona le approva, poi ne vengono conservate copie di consultazione nei file. Le guide operative restano leggibili in ai_docs/reference/. Una copia non sostituisce l’artefatto governato approvato. Sono due modalità di autorità, non due modi di garantire che l’agente abbia capito.

Su più progetti, una conoscenza trasferibile può essere riusata solo rispettando provenienza, ambito e autorizzazioni. Non assumere che una regola di Orione sia valida ovunque o che aprire una chat nuova renda accessibili cartelle diverse.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Ripartire richiede recupero, non un archivio riversato nel prompt.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S33
Module: M6
Objective: O6
Role: explanation
Title: Conoscenza crescente, contesto selezionato
Value contribution: evitare legge universale del contesto piccolo.

### Learner content

Per lavorare sul recupero di un ordine servono contratto, decisione su K, stato del guasto e parti coinvolte. Non servono necessariamente tutta la storia commerciale e ogni conversazione del team.

Il metodo cerca di mantenere piccolo e pertinente il contesto del compito, lasciando fuori le informazioni non necessarie e recuperando quelle che servono. “Vuoto” può descrivere il punto di ripartenza, non il contesto sufficiente per svolgere il lavoro.

Non c’è qui una prova che meno contesto migliori sempre il risultato. Eliminare una condizione decisiva lo peggiora. La domanda utile è: «Quali informazioni ti servono per questo compito e dove le recuperi?». Se il recupero fallisce, la lacuna va resa esplicita.

### Complete explanation

Per lavorare sul recupero di un ordine servono contratto, decisione su K, stato del guasto e parti coinvolte. Non servono necessariamente tutta la storia commerciale e ogni conversazione del team.

Il metodo cerca di mantenere piccolo e pertinente il contesto del compito, lasciando fuori le informazioni non necessarie e recuperando quelle che servono. “Vuoto” può descrivere il punto di ripartenza, non il contesto sufficiente per svolgere il lavoro.

Non c’è qui una prova che meno contesto migliori sempre il risultato. Eliminare una condizione decisiva lo peggiora. La domanda utile è: «Quali informazioni ti servono per questo compito e dove le recuperi?». Se il recupero fallisce, la lacuna va resa esplicita.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Dopo un risultato concreto puoi chiedere di preparare la compattazione.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-15

## S34
Module: M6
Objective: O6
Role: explanation
Title: Prima di compattare, prepara la ripresa
Value contribution: insegnare gesto e preparazione coerenti con richiestaautore.

### Learner content

La raccomandazione dell’autore è compattare il contesto non appena si è ottenuto un risultato concreto, chiedendo prima all’agente: «vorrei compattare il contesto».

Non è un comando magico delle skill. È una richiesta che permette all’agente di salvare, se necessario, un handoff e controllare che il risultato utile sia persistente. Compattare significa ridurre la storia mantenuta nel contesto; aprire una sessione nuova è un’altra forma di ripartenza.

Prima di procedere verifica dove sono risultato, prove, decisioni e punti ancora aperti, e come la prossima sessione potrà riprenderli. Un handoff riassume lo stato operativo e punta alle fonti: non sostituisce tutte le decisioni durevoli. La compattazione non è garantita senza perdite.

### Complete explanation

La raccomandazione dell’autore è compattare il contesto non appena si è ottenuto un risultato concreto, chiedendo prima all’agente: «vorrei compattare il contesto».

Non è un comando magico delle skill. È una richiesta che permette all’agente di salvare, se necessario, un handoff e controllare che il risultato utile sia persistente. Compattare significa ridurre la storia mantenuta nel contesto; aprire una sessione nuova è un’altra forma di ripartenza.

Prima di procedere verifica dove sono risultato, prove, decisioni e punti ancora aperti, e come la prossima sessione potrà riprenderli. Un handoff riassume lo stato operativo e punta alle fonti: non sostituisce tutte le decisioni durevoli. La compattazione non è garantita senza perdite.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

La frase è utile solo se precede il salvataggio necessario.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-15

## S35
Module: M6
Objective: O6
Role: check
Title: Accetti di compattare subito?
Value contribution: valutare ordine salvataggio/compattazione.
Solution: S36

### Learner content

L’agente ha trovato la causa di un baco, ma la scelta fra due soluzioni è ancora soltanto nella chat. Dice: «Abbiamo un risultato concreto, compatta pure; salverò il riepilogo dopo».

Come rispondi? Chiedi ciò che serve prima della compattazione, distinguendo il risultato acquisito dalla decisione ancora aperta. Non scrivere tu l’handoff: il tuo atto è richiederlo e verificare la possibilità di ripresa.

L’agente aggiunge che, se una copia locale contraddice una proposta approvata in devPNT configurato, basta scegliere la copia. Contesti questa regola? Che cosa cambia se il lavoro è invece Standalone?

### Complete explanation

L’agente ha trovato la causa di un baco, ma la scelta fra due soluzioni è ancora soltanto nella chat. Dice: «Abbiamo un risultato concreto, compatta pure; salverò il riepilogo dopo».

Come rispondi? Chiedi ciò che serve prima della compattazione, distinguendo il risultato acquisito dalla decisione ancora aperta. Non scrivere tu l’handoff: il tuo atto è richiederlo e verificare la possibilità di ripresa.

L’agente aggiunge che, se una copia locale contraddice una proposta approvata in devPNT configurato, basta scegliere la copia. Contesti questa regola? Che cosa cambia se il lavoro è invece Standalone?

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Un risultato concreto non elimina lo stato incompleto da conservare.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-15
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S36
Module: M6
Objective: O6
Role: solution
Title: Salvare prima, riprendere dai riferimenti
Value contribution: soluzione e limite della raccomandazione.

### Learner content

Rispondi: «Vorrei compattare il contesto. Prima salva la causa e le sue evidenze, indica la scelta ancora aperta e prepara il punto di ripresa. Mostrami i riferimenti ai file salvati; poi procediamo».

Il risultato concreto è l’indagine, non la decisione definitiva sul fix. La prossima sessione deve poter distinguerli. Conservare lo stato dopo la perdita della conversazione può essere troppo tardi.

Se hai detto soltanto “riassumi”, torna a S32–S34: il riepilogo deve essere persistente e collegato alle evidenze. L’atto della persona è verificare il passaggio di consegne, non ritenere che la parola handoff garantisca continuità.

Con devPNT configurato chiedi di verificare l’artefatto governato approvato e riallineare la copia: non scegli la copia come autorità alternativa. In Standalone l’analisi autorevole è il file ANALYSIS del progetto. In entrambe le modalità il risultato da riprendere deve essere recuperabile prima di compattare.

### Complete explanation

Rispondi: «Vorrei compattare il contesto. Prima salva la causa e le sue evidenze, indica la scelta ancora aperta e prepara il punto di ripresa. Mostrami i riferimenti ai file salvati; poi procediamo».

Il risultato concreto è l’indagine, non la decisione definitiva sul fix. La prossima sessione deve poter distinguerli. Conservare lo stato dopo la perdita della conversazione può essere troppo tardi.

Se hai detto soltanto “riassumi”, torna a S32–S34: il riepilogo deve essere persistente e collegato alle evidenze. L’atto della persona è verificare il passaggio di consegne, non ritenere che la parola handoff garantisca continuità.

Con devPNT configurato chiedi di verificare l’artefatto governato approvato e riallineare la copia: non scegli la copia come autorità alternativa. In Standalone l’analisi autorevole è il file ANALYSIS del progetto. In entrambe le modalità il risultato da riprendere deve essere recuperabile prima di compattare.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Quanto di questo patrimonio conviene mantenere dipende anche dal progetto.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-15
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S37
Module: M7
Objective: O7
Role: explanation
Title: Una settimana, un mese, anni
Value contribution: riportare accumulo e rischio neltempo.

### Learner content

Dopo una settimana, la decisione su K può evitare di dover richiedere ancora il contratto. Dopo un mese, la nuova regola richiede aggiornare fonte e conclusioni dipendenti. Dopo anni, una nuova persona può ritrovare ragioni, alternative scartate e prove dei cambiamenti.

Questi sono scenari condizionati alla registrazione, consultazione e manutenzione, non tempi di risparmio misurati. Anche buone note curate possono fornire questa continuità.

L’esperienza del progetto è utile quando guida domande e verifiche nuove. Un vecchio incidente non prova la causa del prossimo. Lo stesso patrimonio può aiutare a evitare una regressione oppure propagare una conclusione sbagliata se nessuno ne controlla più la validità.

### Complete explanation

Dopo una settimana, la decisione su K può evitare di dover richiedere ancora il contratto. Dopo un mese, la nuova regola richiede aggiornare fonte e conclusioni dipendenti. Dopo anni, una nuova persona può ritrovare ragioni, alternative scartate e prove dei cambiamenti.

Questi sono scenari condizionati alla registrazione, consultazione e manutenzione, non tempi di risparmio misurati. Anche buone note curate possono fornire questa continuità.

L’esperienza del progetto è utile quando guida domande e verifiche nuove. Un vecchio incidente non prova la causa del prossimo. Lo stesso patrimonio può aiutare a evitare una regressione oppure propagare una conclusione sbagliata se nessuno ne controlla più la validità.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Adottare il metodo richiede giudicare anche il suo costo.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12

## S38
Module: M7
Objective: O7
Role: explanation
Title: Le diffidenze hanno conseguenze reali
Value contribution: affrontare costi senza difesa promozionale.

### Learner content

«Più documenti rallentano». Vero: scrivere, leggere e mantenere costa; il processo deve essere proporzionato. «Le note possono essere sbagliate». Vero: provenienza e revisione rendono gli errori controllabili, non impossibili.

«L’agente seguirà regole invece di risolvere il problema». Una risposta è giudicare gli esiti concreti: ragioni recuperate, vincoli preservati e prove pertinenti. Se produce artefatti vuoti, il metodo è stato applicato male. «Conservare tutto riempie il contesto». L’archivio deve supportare selezione, non lettura indiscriminata.

Non chiediamo fiducia cieca. Chiediamo di valutare quale problema il processo affronta, quale controllo aggiunge e quale costo richiede. Una buona nota può bastare; un progetto in evoluzione può rendere utile una disciplina ripetibile.

### Complete explanation

«Più documenti rallentano». Vero: scrivere, leggere e mantenere costa; il processo deve essere proporzionato. «Le note possono essere sbagliate». Vero: provenienza e revisione rendono gli errori controllabili, non impossibili.

«L’agente seguirà regole invece di risolvere il problema». Una risposta è giudicare gli esiti concreti: ragioni recuperate, vincoli preservati e prove pertinenti. Se produce artefatti vuoti, il metodo è stato applicato male. «Conservare tutto riempie il contesto». L’archivio deve supportare selezione, non lettura indiscriminata.

Non chiediamo fiducia cieca. Chiediamo di valutare quale problema il processo affronta, quale controllo aggiunge e quale costo richiede. Una buona nota può bastare; un progetto in evoluzione può rendere utile una disciplina ripetibile.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Confrontiamo due condizioni senza inventare vantaggi misurati.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S39
Module: M7
Objective: O7
Role: explanation
Title: Confrontare a parità di informazioni
Value contribution: insegnare alternativa sufficiente senza benchmarkfittizio.

### Learner content

Alba e Bora sono progetti inventati. Alba ha un’unica regola stabile, una nota breve mantenuta e una modifica occasionale. Bora cambia fornitore, ha più modalità di recupero e più persone che intervengono nel tempo.

In entrambi i confronti, note curate e skill ricevono le stesse fonti, le stesse ragioni e lo stesso compito. Le skill rendono esplicite consultazione, validità, impatto e chiusura; se le note sono governate da istruzioni equivalenti, gli esiti possono equivalere.

La differenza da valutare non è “agente intelligente contro agente smemorato”. È il costo di rendere continuo e verificabile il lavoro in quelle condizioni. Non sappiamo ancora misurare quale alternativa vinca per un team reale.

### Complete explanation

Alba e Bora sono progetti inventati. Alba ha un’unica regola stabile, una nota breve mantenuta e una modifica occasionale. Bora cambia fornitore, ha più modalità di recupero e più persone che intervengono nel tempo.

In entrambi i confronti, note curate e skill ricevono le stesse fonti, le stesse ragioni e lo stesso compito. Le skill rendono esplicite consultazione, validità, impatto e chiusura; se le note sono governate da istruzioni equivalenti, gli esiti possono equivalere.

La differenza da valutare non è “agente intelligente contro agente smemorato”. È il costo di rendere continuo e verificabile il lavoro in quelle condizioni. Non sappiamo ancora misurare quale alternativa vinca per un team reale.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Prova a formulare una scelta per un caso diverso da Orione.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S40
Module: M7
Objective: O7
Role: check
Title: Scegliere, senza promessa automatica
Value contribution: trasferimento cumulativo O1/O7.
Covers: M1/O1
Solution: S41

### Learner content

Casi nuovi inventati: Cobalto ha una sola trasformazione stabile documentata in una nota mantenuta; Selene gestisce ricevute con regole cambiate, eccezioni storiche e più integrazioni. L’agente propone a entrambi: «Caricherò tutto l’archivio a ogni attività e userò sempre il percorso completo».

Formula la tua risposta. Quale problema ti porta a considerare le skill? Che cosa può bastare in Cobalto? Quale patrimonio vuoi ritrovare in Selene? Quali costi e limiti rendi espliciti? Come correggi la proposta dell’agente?

La risposta deve collegare scelta e condizioni del lavoro. Ripetere “fonti, Vision, review” senza ragioni non dimostra la decisione richiesta.

### Complete explanation

Casi nuovi inventati: Cobalto ha una sola trasformazione stabile documentata in una nota mantenuta; Selene gestisce ricevute con regole cambiate, eccezioni storiche e più integrazioni. L’agente propone a entrambi: «Caricherò tutto l’archivio a ogni attività e userò sempre il percorso completo».

Formula la tua risposta. Quale problema ti porta a considerare le skill? Che cosa può bastare in Cobalto? Quale patrimonio vuoi ritrovare in Selene? Quali costi e limiti rendi espliciti? Come correggi la proposta dell’agente?

La risposta deve collegare scelta e condizioni del lavoro. Ripetere “fonti, Vision, review” senza ragioni non dimostra la decisione richiesta.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

La soluzione confronta le condizioni, non assegna un vincitore universale.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S41
Module: M7
Objective: O7
Role: solution
Title: Una scelta motivata e rivedibile
Value contribution: soluzione trasferimento e rispostainsufficiente.
Covers: M1/O1

### Learner content

In Cobalto una nota curata può bastare finché conserva la regola, la fonte e resta consultata. In Selene la storia rende più importante una disciplina di recupero, validità e cambiamento: chiedi quali vincoli precedenti sono coinvolti e quali fonti vanno riaperte.

Contesti sia lettura indiscriminata sia percorso completo uniforme. Chiedi selezione pertinente e livello proporzionato al rischio. Rendi espliciti manutenzione, possibilità di errori e assenza di un risparmio garantito.

Se hai scelto le skill solo perché Selene è grande, torna a S37–S39: contano evoluzione e dipendenze, non una dimensione nominale. Il beneficio cercato è costruire sul lavoro precedente senza cancellarne le ragioni, restando capaci di correggerle.

### Complete explanation

In Cobalto una nota curata può bastare finché conserva la regola, la fonte e resta consultata. In Selene la storia rende più importante una disciplina di recupero, validità e cambiamento: chiedi quali vincoli precedenti sono coinvolti e quali fonti vanno riaperte.

Contesti sia lettura indiscriminata sia percorso completo uniforme. Chiedi selezione pertinente e livello proporzionato al rischio. Rendi espliciti manutenzione, possibilità di errori e assenza di un risparmio garantito.

Se hai scelto le skill solo perché Selene è grande, torna a S37–S39: contano evoluzione e dipendenze, non una dimensione nominale. Il beneficio cercato è costruire sul lavoro precedente senza cancellarne le ragioni, restando capaci di correggerle.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Puoi applicare lo stesso giudizio al tuo progetto senza modificarlo.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S42
Module: M7
Objective: O7
Role: closing
Title: Il prossimo gesto nel tuo progetto
Value contribution: preservare applicazionefacoltativaUC5e chiusura.
Covers: M6/O6

### Learner content

Applicazione facoltativa: scegli un documento non riservato del tuo progetto, accessibile all’agente. Chiedi in sola lettura: «Spiega quale regola sostiene, cita il passaggio e i limiti; proponi solo a parole una modifica che la tocchi, indicando beneficio, decisioni da prendere e prove mancanti. Non modificare file né eseguire operazioni».

Controlla se la risposta risale alla fonte, distingue storia e validità, preserva i vincoli e lascia a te le scelte aperte. Non devi redigere tu claim o design. Se non vuoi usare il progetto, usa questo caso inventato: una nota dice che ristampare una ricevuta deve conservare la data dell’acquisto, mentre l’agente propone di usare sempre la data di stampa. Chiedi il motivo storico e se cambia il significato della ricevuta prima di approvare.

Puoi tornare a questo confronto in una sessione successiva: che cosa è realmente ritrovabile? Il corso finisce qui; efficacia su persone non verificata. Il successo operativo delle skill va giudicato sul lavoro, non sulla loro sola presenza.

### Complete explanation

Applicazione facoltativa: scegli un documento non riservato del tuo progetto, accessibile all’agente. Chiedi in sola lettura: «Spiega quale regola sostiene, cita il passaggio e i limiti; proponi solo a parole una modifica che la tocchi, indicando beneficio, decisioni da prendere e prove mancanti. Non modificare file né eseguire operazioni».

Controlla se la risposta risale alla fonte, distingue storia e validità, preserva i vincoli e lascia a te le scelte aperte. Non devi redigere tu claim o design. Se non vuoi usare il progetto, usa questo caso inventato: una nota dice che ristampare una ricevuta deve conservare la data dell’acquisto, mentre l’agente propone di usare sempre la data di stampa. Chiedi il motivo storico e se cambia il significato della ricevuta prima di approvare.

Puoi tornare a questo confronto in una sessione successiva: che cosa è realmente ritrovabile? Il corso finisce qui; efficacia su persone non verificata. Il successo operativo delle skill va giudicato sul lavoro, non sulla loro sola presenza.

### Visual content

Unità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.

### Transition

Fine del percorso. Porta una richiesta e un criterio di giudizio nel lavoro successivo.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
