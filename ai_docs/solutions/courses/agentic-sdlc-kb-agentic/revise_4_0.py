"""Authoring record for 4.0; no npm runtime. Explicit content, no model renderer."""
from pathlib import Path
import hashlib, zipfile, shutil, json, re
ROOT = Path(__file__).resolve().parents[4]
C = Path(__file__).resolve().parent
BASE = C.relative_to(ROOT).as_posix()
VERSION = '4.0-content'
# The prose is authored here; source and packets are reproducible from these bytes.
UNITS = [
('Perché un agente ricomincia da capo?', '''Usi l’AI per sviluppare: una chat per un baco, un’altra per una feature, un documento con istruzioni e qualche nota presa durante il lavoro. Una nuova sessione riceve il codice attuale, ma non necessariamente le ragioni che lo hanno prodotto.

Questo non rende inevitabile un errore. Anche senza skill puoi mantenere ottime note. Il problema emerge quando fonti, decisioni e risultati restano dispersi: bisogna ritrovarli e capire quali valgono ancora. Una risposta plausibile può omettere un vincolo che il team aveva già scoperto.

Questo corso spiega perché kb-agentic e agentic-sdlc, con il supporto di distill, cercano di trasformare attività separate in conoscenza riutilizzabile. Vedremo prima il bisogno e il beneficio, poi il metodo. Non promettiamo risultati migliori in ogni progetto.''', 'orientare il beneficio prima del meccanismo', 'Vediamo un progetto in cui la ragione di una scelta cambia il giudizio su una correzione.', 1),
('Orione cresce: il doppio clic', '''Orione è un software inventato che invia ordini a un fornitore. All’inizio il team vede un problema: una persona preme due volte «Invia» e vengono creati due ordini. Disabilita il pulsante durante l’attesa.

La nota di decisione conserva evento osservato, motivo del blocco e prova: due clic ravvicinati devono produrre un solo invio. Il codice contiene il blocco; la nota spiega perché esiste.

La soluzione copre il doppio clic, ma non tutti i modi in cui un ordine può essere duplicato. La storia del progetto non è un elenco di successi: conserva anche l’ambito di ogni protezione. Tutti i dati, documenti ed eventi di Orione sono fittizi; non sono risultati di una prova su software reale.''', 'introdurre una protezione e il suo limite', 'Un incidente diverso mostra perché ricordare il blocco non basta.', 13),
('La conferma persa cambia il problema', '''Il fornitore crea l’ordine, ma la risposta non arriva a Orione. La persona vede ancora «in attesa» e ritenta. Un ritentativo è un nuovo invio per completare la stessa operazione, non un nuovo ordine voluto dalla persona.

Il team introduce una chiave: un identificatore dell’ordine logico. Nel nostro contratto fittizio, il fornitore restituisce l’esito precedente se riceve la stessa chiave; una chiave nuova significa un nuovo ordine. Orione conserva quindi la chiave anche nei ritentativi.

La nota collega incidente, contratto e verifica. Ora il vincolo importante è: lo stesso ordine mantiene la stessa identità. Il blocco del pulsante rimane, ma la protezione non si esaurisce nel gesto dell’utente.''', 'spiegare la relazione chiave/ritentativo prima del suo uso', 'Una terza modifica aggiunge una responsabilità che il prossimo fix dovrà rispettare.', 13),
('Una notifica non è un nuovo ordine', '''Orione aggiunge un’email di conferma. Durante un guasto l’email non parte, ma l’ordine è già stato creato. Il team separa le due attività: ritentare la notifica non deve inviare nuovamente l’ordine al fornitore.

Nei file conserva il motivo della separazione e una prova: un errore email non aumenta il numero di ordini. La cronologia ora contiene tre protezioni collegate: blocco del doppio clic, identità stabile dello stesso ordine, notifica separata.

Non devi memorizzare le date. Devi poter ritrovare le ragioni quando una nuova richiesta tocca quel comportamento. La comprensione professionale include le condizioni in cui una soluzione è stata introdotta, non solo il suo nome.''', 'rendere decisivi vincoli accumulati', 'Arriva un baco che invita a rimuovere proprio quei controlli.', 12),
('La correzione ovvia può regredire', '''Nuovo baco: dopo una conferma persa, il pulsante resta bloccato e la persona non può ritentare. L’agente propone: «Tolgo il blocco e genero una nuova chiave a ogni invio; il pulsante torna a funzionare».

Il sintomo visibile può sparire. Ma una nuova chiave può far creare un secondo ordine: il fornitore non la riconosce come ritentativo dello stesso ordine. Togliere soltanto il blocco, conservando la chiave, non avrebbe da solo questa conseguenza.

La storia suggerisce quindi una domanda precisa: quali controlli impediscono il doppio invio e quali impediscono inutilmente un recupero? Non stabilisce da sola la soluzione: occorre verificare il guasto attuale. Un fix localmente convincente non basta quando tocca garanzie nate in precedenza.''', 'mostrare causalità della regressione senza attribuirla a qualsiasi sblocco', 'La conoscenza utile deve restare reperibile anche quando cambiano chat e agenti.', 13),
('Patrimonio durevole, contesto del compito', '''Il contesto è il materiale disponibile al modello nella conversazione corrente. I file persistenti del progetto restano invece riapribili fra conversazioni. Conservare un file non significa che l’agente lo abbia letto: serve recuperarlo quando è pertinente.

Una skill è un insieme di istruzioni che l’agente carica per svolgere un tipo di lavoro. kb-agentic disciplina la conoscenza e le sue fonti; agentic-sdlc disciplina il cambiamento software; distill aiuta a scrivere testi che conservano le informazioni necessarie senza sommergerle.

L’“agente ingegnere” è un agente che può costruire su tracce consultate e aggiornate. Non si riaddestra durante queste attività. Il patrimonio può crescere mentre il contesto della singola attività rimane selezionato. Le istruzioni orientano il comportamento, ma non ne garantiscono l’esecuzione corretta.''', 'definire skill e contesto collegandoli al beneficio', 'Prova a formulare una richiesta che faccia emergere il vincolo, senza scrivere tu il design.', 2),
('Che cosa chiedi davanti al fix?', '''L’agente ti mostra la proposta di S05: nuova chiave a ogni invio e pulsante sbloccato. Dice: «Il test del pulsante passa, posso chiudere».

Come rispondi? Formula una richiesta che chiarisca quale comportamento precedente deve restare valido e quale evidenza manca. Spiega anche perché conservare e consultare la storia può aiutare una nuova sessione, e quando una buona nota curata potrebbe bastare.

Non devi produrre un’analisi al posto dell’agente: il tuo atto è decidere se accettare la chiusura e chiedere le verifiche necessarie. Prova prima di leggere la soluzione.''', 'verificare richiesta umana e ragione del beneficio', 'Confronta il tuo giudizio con una risposta motivata.', 13),
('Il beneficio non è il numero di documenti', '''Puoi rispondere: «Non chiudere sul solo pulsante. Recupera la decisione sulla chiave e il contratto del fornitore, verifica il guasto osservato e dimostra che un ritentativo dello stesso ordine non ne crea un altro. Controlla separatamente l’email».

La storia evita di ricostruire da zero una ragione già scoperta e rende verificabile il vincolo. Anche una nota curata, pertinente e mantenuta può ottenere questo risultato. Le skill cercano di rendere ripetibile il modo di conservarla, consultarla e aggiornarla.

«Abbiamo più documenti» non è una ragione sufficiente: se non vengono trovati o sono vecchi, possono peggiorare la decisione. Se hai approvato sul test del pulsante, torna a S03–S05 e confronta gesto visibile e ordine creato.''', 'correggere fiducia nei documenti e nel sintomo risolto', 'Vediamo come kb-agentic rende controllabile una risposta sulle regole del fornitore.', 13),
('Acquisire una fonte non è capirla', '''Nel caso Orione l’agente riceve il contratto del fornitore. kb-agentic gli prescrive di conservarne una fonte riapribile con provenienza e di leggerla prima di estrarre affermazioni.

La provenienza indica da dove arriva un’informazione e a quale versione o passaggio risalire. Un documento copiato nel progetto ma mai letto è disponibile, non verificato. Se l’agente ha letto solo alcune parti, questo limite deve restare visibile.

La persona può chiedere: «Quale passaggio hai usato e che cosa non hai ancora letto?». Non deve fidarsi di una risposta solo perché il file compare in una cartella. Per un documento riservato, si usano accessi autorizzati; il nostro esempio non richiede di caricare dati reali.''', 'distinguere disponibilità, lettura e supporto della risposta', 'Serve conservare anche le condizioni della frase che è stata ricavata.', 3),
('Un’affermazione ha un ambito', '''Un claim è un’affermazione registrata con fonte e stato. Nel contratto fittizio leggiamo: «Per il servizio Ordini, un ritentativo con la stessa chiave restituisce il precedente esito. Una nuova chiave crea un nuovo ordine».

Il claim non è semplicemente «i ritentativi sono sicuri». Ha un ambito: servizio Ordini e stessa chiave. Una risposta che elimina queste condizioni può essere fedele alle parole più brevi ma sbagliata per il lavoro da fare.

Davanti a una risposta dell’agente chiedi: «Questa regola copre proprio la nostra operazione? Dove sono le condizioni?». L’agente estrae e organizza i claim; tu controlli la risposta e decidi se usarla. Una sintesi non sostituisce la fonte quando il suo significato è decisivo.''', 'spiegare claim e ambito', 'Come si trova il claim senza rileggere tutto il patrimonio?', 4),
('Recuperare ciò che serve, non tutto', '''La KB organizza le affermazioni per argomenti e relazioni. Un grafo è una struttura di elementi collegati: qui aiuta a passare dalla domanda «possiamo ritentare?» all’argomento Ordini, poi alle regole pertinenti e alle fonti.

Questo grafo degli argomenti appartiene alla conoscenza del progetto. Il grafo dei prerequisiti di un corso ha invece concetti collegati secondo ciò che occorre capire prima: ordina le spiegazioni. Cercare una regola sugli ordini nella KB e scegliere cosa insegnare prima sono due lavori diversi.

Un indice è un elenco di riferimenti, non il documento che descrive ogni regola. L’agente usa riferimenti e ricerca per selezionare che cosa aprire. Se trova una sintesi derivata da un’altra nota, deve poter risalire al suo fondamento quando serve per decidere.

L’obiettivo è recuperare tutte e solo le informazioni necessarie al compito. È una disciplina di selezione, non una garanzia che ogni ricerca sia completa. Se il materiale non si trova, chiedi quali percorsi sono stati cercati: «non trovato» non significa «non esiste».''', 'motivare selezione e limite del recupero', 'Una fonte citata può comunque sostenere una risposta troppo ampia.', 4),
('Accetti questa risposta?', '''Caso fittizio nuovo: una collega vuole inviare un secondo ordine, diverso dal primo. Chiedi all’agente se può riusare la vecchia chiave. Risponde: «Sì, il contratto dice che usare la stessa chiave evita duplicati»; non mostra il passaggio né distingue nuovo ordine e ritentativo.

Che cosa contesti? Formula la richiesta da rivolgere all’agente prima di inoltrare la risposta alla collega. Non compilare tu il claim o la risposta corretta al suo posto. Il tuo compito è verificare se il risultato proposto è utilizzabile.''', 'trasferire giudizio sull’ambito a operazione diversa', 'La differenza decisiva è l’identità dell’operazione, non la parola sicuro.', 4),
('La citazione deve sostenere la decisione', '''Chiedi: «Mostra il passaggio e distingui un nuovo ordine da un ritentativo dello stesso ordine. La regola sulla stessa chiave vale per l’operazione della collega?».

Nel nostro contratto fittizio la stessa chiave restituisce il precedente esito. Non crea il secondo ordine voluto: l’agente deve correggere la risposta mantenendo quella distinzione. La fonte era pertinente al tema ma la conclusione non rispettava l’ambito.

Se hai accettato perché compariva la parola “contratto”, torna a S10. La provenienza permette di controllare, non rende automaticamente giusta l’inferenza. Questo è il giudizio della persona; l’estrazione e la registrazione restano lavoro dell’agente.''', 'soluzione e correzione mirata', 'Anche una risposta valida oggi può diventare inadeguata quando cambia la fonte.', 4),
('Una ragione storica non è una regola eterna', '''Il contratto iniziale permetteva il recupero dell’esito per un giorno. Una nuova versione, dal mese successivo, lo permette per sette giorni. I periodi non si sovrappongono: la vecchia nota può ancora spiegare una scelta di allora, ma non basta a decidere per un ordine di oggi.

Il caso e i numeri sono inventati. Il punto è distinguere validità storica da validità corrente. Una fonte conservata non resta attuale solo perché è facile da recuperare.

kb-agentic prescrive di mantenere visibili stato e sostituzioni delle informazioni. Quando una regola cambia, vanno riesaminati i documenti e le decisioni che dipendevano da essa. L’elenco dei dipendenti aiuta a farlo; non aggiorna automaticamente il software.''', 'insegnare validità temporale e revisione', 'Due documenti dello stesso periodo richiedono un controllo diverso.', 5),
('Quando le fonti sembrano contraddirsi', '''Due documenti fittizi, entrambi validi oggi, riportano finestre diverse: sette giorni e un giorno. L’agente afferma che valgono per lo stesso servizio e tipo di operazione, ma non riesce a verificare questa attribuzione.

Scegliere il documento più recente non risolve quella mancanza. La procedura KB mantiene visibili le affermazioni contestate e chiede il chiarimento che può decidere l’ambito. “Contestato” significa che il risultato non va usato come fatto risolto.

Una preferenza del team, «vorremmo sette giorni», può essere una scelta di prodotto, ma non prova cosa garantisca il fornitore. La persona può indicare una fonte, chi conosce il fatto o decidere di rinviare l’affermazione non verificata.''', 'separare evidenza e preferenza', 'Un fatto nuovo può risolvere il contrasto senza cancellarne la storia.', 5),
('Il chiarimento deve raggiungere chi lo usava', '''Arriva un chiarimento riapribile: il documento con un giorno riguarda Notifiche, quello con sette giorni riguarda Ordini. L’agente può correggere la precedente attribuzione, conservandone il superamento e la fonte del chiarimento.

La nota che aveva assunto un giorno per gli ordini deve essere riesaminata. Anche il piano che ne derivava va controllato. Una conoscenza corretta nel registro e una conclusione vecchia nel piano sono ancora una possibile regressione.

L’agente non deve rileggere la propria interpretazione come se fosse una nuova prova. Le catene di provenienza servono a riaprire il fondamento e a riconoscere ciò che è derivato. Nessun indice garantisce da solo che tutti i dipendenti siano stati individuati.''', 'mostrare aggiornamento oltre il claim isolato', 'Prova a giudicare una risposta che anticipa il chiarimento con una preferenza.', 5),
('La recenza basta?', '''In un altro progetto inventato, l’agente trova due regole dello stesso mese per la conservazione di ricevute. Non ha accertato se una riguardi copie di prova e l’altra ricevute definitive. Dice: «Scelgo quella più nuova; dimmi soltanto quale durata preferisci».

Quale parte della risposta contesti e quale chiarimento chiedi? Se non conosci il fatto, come rispondi senza inventarlo? Il problema non richiede di classificare tu un conflitto: l’agente ha già mostrato l’incertezza e la proposta da giudicare.''', 'giudicare escalation su fatto non noto', 'La soluzione conserva la distinzione tra preferenza e prova.', 5),
('Non scegliere un fatto per preferenza', '''Contesti la scelta per recenza e chiedi di verificare a quali ricevute si riferiscono le fonti. Se non sai rispondere, indichi chi può fornire il documento o chiedi di mantenere aperta la conclusione.

Puoi decidere che il lavoro proceda su parti non dipendenti dal dato incerto. Non puoi rendere vera una garanzia del fornitore soltanto approvandola. Dopo il chiarimento chiedi la risposta corretta con fonte e i riferimenti alle conclusioni da riesaminare.

Se hai risposto solo con la durata che preferisci, torna a S15. Una scelta di perimetro è tua; l’evidenza su cosa esiste deve provenire da un fatto controllabile.''', 'soluzione con percorso di correzione', 'Quando l’informazione diventa modifica software, serve un’altra disciplina.', 5),
('Più metodo non deve significare più burocrazia', '''Un’obiezione ragionevole è: «Se devo documentare tutto, rallento e magari peggioro il risultato». agentic-sdlc distingue lavori proporzionati al rischio: L1 per correzioni banali senza cambiamento di comportamento, L2 per modifiche piccole a causa chiara e basso rischio, L3 per cambiamenti significativi, contratti o rischi maggiori. Spike è un’esplorazione non ancora pronta per produzione.

L’agente dichiara il livello; la persona può contestarlo. Una riga che cambia l’identità di un ordine non è innocua perché è corta. Un refuso isolato non deve pagare il costo di un design significativo.

Tempo, letture e verifiche hanno un costo reale. La proporzione va giudicata sul compito, non sulla volontà di “fare il metodo”.''', 'rispondere al timore di rigidità con criterio concreto', 'Anche una modifica ben verificata può inseguire il beneficio sbagliato.', 6),
('La Vision conserva il perché del cambiamento', '''La Vision dichiara beneficio, destinatari, limiti e segnali di successo. Per Orione il beneficio fittizio è permettere il recupero di un invio incerto senza creare un secondo ordine e senza confondere l’email con l’ordine.

La sviluppatrice vuole verificare i percorsi toccati; il responsabile tecnico vuole sapere quale risultato verrà ottenuto e quali scelte restano aperte. Entrambi hanno bisogno di una proposta coerente con il beneficio.

Un nuovo menu commerciale non risolve quel baco. Se l’agente lo aggiunge, chiedi di separarlo o discutere il cambiamento di perimetro. La Vision approvata non va riscritta silenziosamente per giustificare ciò che l’agente ha già deciso di costruire.''', 'distinguere riuscita tecnica e beneficio', 'Valuta una proposta che usa la dimensione del diff come unico criterio.', 7),
('Una riga può cambiare un contratto', '''L’agente propone la nuova chiave a ogni invio e dichiara L2: «È una sola riga». Aggiunge un menu di analisi commerciale per “rendere completo il miglioramento”.

Come rispondi sul livello e sul perimetro? Usa gli effetti della modifica e il beneficio concordato. Non ti chiediamo di classificare una richiesta prima dell’agente: stai giudicando la sua dichiarazione e scegliendo quali obiettivi autorizzare.''', 'verificare giudizio umano su triage e scope', 'Confronta dimensione della modifica e conseguenza per l’utente.', 6),
('Giudicare effetti e confini', '''Contesti L2 perché la proposta altera il contratto fra ritentativo e identità dell’ordine, con rischio di duplicazione. Chiedi all’agente di rivedere livello e analisi in base agli effetti, non alle righe.

Rifiuti il menu dentro questo fix: se interessa, sarà una scelta separata di perimetro. Per un refuso senza nuovi effetti, invece, non chiederesti tutti gli artefatti di un L3.

Se hai scelto solo in base alla lunghezza del diff, torna a S19. Se hai approvato il menu perché è utile in generale, torna a S20: utilità e appartenenza al beneficio attuale sono domande diverse.''', 'soluzione proporzionata', 'Prima della soluzione definitiva, occorre osservare il guasto effettivo.', 6),
('Osservare il baco prima di spiegarlo', '''Nel caso Orione abbiamo log fittizi: invio con chiave K, ordine creato dal fornitore, conferma non ricevuta, pulsante ancora bloccato. K è solo il nome della chiave nel racconto.

Questi eventi danno una domanda concreta al codice: perché lo stato incerto impedisce un ritentativo con K? Non provano che qualsiasi controllo sia sbagliato. L’agente deve partire dalle evidenze disponibili, controllarne ambito e mantenere le ipotesi con verifiche e risultati.

Puoi chiedere: «Quale osservazione sostiene questa causa? Quali alternative sono state escluse?». Cercare pattern sospetti nel sorgente può suggerire ipotesi; non collega da solo quel pattern all’incidente.''', 'insegnare evidenza prima della causa immaginata', 'La correzione deve descrivere il comportamento desiderato oltre il pulsante.', 16),
('Dai bisogni al comportamento osservabile', '''Un use case descrive cosa deve ottenere una persona: la cliente vuole sapere se l’ordine è stato accettato; l’operatrice vuole recuperare l’invio senza duplicarlo. La specifica funzionale descrive che cosa il software deve fare per quei bisogni, prima di scegliere come implementarlo.

Nel caso: stesso ordine mantiene K; conferma assente produce uno stato incerto visibile, non “fallito” certo; ritentativo con K può recuperare l’esito; email fallita rimane un problema distinto. Un nuovo ordine voluto riceve invece una nuova identità.

La persona approva il risultato e prende le scelte che l’agente le sottopone, per esempio quale informazione mostrare durante l’attesa. L’agente prepara specifica e analisi, non la persona al suo posto.''', 'spiegare artefatti a partire dal loro scopo', 'Lo stesso comportamento attraversa più superfici.', 8),
('Seguire il percorso, non un solo schermo', '''Una superficie è ciò su cui una persona o un software agisce o riceve un risultato. Orione ha pulsante, pannello di stato, richiesta al fornitore e notifica email. Il contratto d’interfaccia descrive il percorso e il feedback fra queste responsabilità.

Se il pannello mostra “completato” ma l’email dice “fallito”, l’esperienza è incoerente. Se l’email ritenta l’ordine, la separazione storica è stata violata. Il modello dei rischi collega queste possibilità a controlli e verifiche.

Chi sviluppa chiede dove lo stato viene consumato; chi guida il lavoro chiede quali esiti sono accettabili e quali restano incerti. Un elenco di file non sostituisce questo quadro.''', 'mostrare blast radius attraverso flussi accessibili', 'Una buona soluzione riusa le responsabilità già presenti.', 8),
('Riusare ciò che già mantiene il vincolo', '''Il Capability Ledger è il registro delle capacità necessarie e delle evidenze su ciò che esiste già. Nell’indagine fittizia l’agente trova la funzione che conserva K e il percorso distinto delle notifiche.

Propone di correggere la transizione dallo stato incerto al recupero consentito, riusando l’identità dell’ordine. Non propone una seconda implementazione del controllo di duplicazione in ogni schermo. Se una capacità non viene trovata, deve mostrare che cosa ha cercato prima di dichiararla mancante.

L’Impact indica quali parti cambiano e perché; il design specifica integrazioni, condizioni e verifiche. Il tuo giudizio è chiedere se il disegno preserva le garanzie e si fonda su evidenze, non compilare il registro al posto dell’agente.''', 'motivare riuso e design pulito', 'Il design deve essere controllato prima di diventare codice.', 8),
('Prevenire l’errore dove nasce', '''Poka-Yoke significa prevenire un uso errato o renderlo subito visibile. Nel caso, la responsabilità che identifica l’ordine deve mantenere K sui ritentativi; la notifica non deve poter creare un nuovo invio.

Una correzione pulita distingue nuovo ordine, recupero e notifica nelle responsabilità appropriate. Una serie di eccezioni “se succede questo baco” può lasciare altre strade incoerenti. Il criterio richiesto dal metodo è: «Dopo la correzione il software deve essere fatto come se fosse stato progettato senza quel difetto».

Un revisore indipendente controlla il design contro beneficio, rischi e sistema reale prima dell’implementazione. “Indipendente” richiede un contesto distinto dall’autore: un secondo passaggio dello stesso autore è una verifica diversa, da dichiarare come tale.''', 'collegare prevenzione e review al beneficio', 'La review non sostituisce le prove sul comportamento.', 16),
('Che cosa dimostrano le prove?', '''L’agente deve verificare almeno gli esiti rilevanti del caso: due clic, conferma persa e recupero con K, nuovo ordine voluto con identità distinta, email fallita senza nuovo invio. Una prova del pulsante non dimostra tutti questi comportamenti.

Dopo l’implementazione, la review confronta il risultato con il design e le evidenze. La chiusura aggiorna ragioni, prove, stato e riferimenti. Una GUIDE può conservare un modello operativo riusabile: per esempio come identità e notifiche sono separate, con provenienza controllabile.

Le guide operative si trovano in ai_docs/reference/: il suo INDEX.md indirizza alla guida pertinente. Una nuova sessione consulta quel riferimento prima di agire e riapre la guida quando riguarda il compito. Un elenco presente ma non consultato non protegge il cambiamento.

Non ogni fix richiede una guida nuova. Test verdi e review sono evidenze con un ambito; non provano che ogni percorso sia corretto né che le skill migliorino sempre il lavoro.''', 'distinguere prova locale e chiusura completa', 'Valuta una chiusura che omette il vincolo più importante.', 9),
('Puoi approvare la chiusura?', '''L’agente dichiara: «Ho sbloccato il pulsante. Il test UI è verde. Ho conservato una nota “problema risolto”. Non ho verificato conferma persa né percorso email».

Quale parte accetti e quali evidenze chiedi prima della chiusura? Spiega quale ragione della storia di Orione rende insufficienti il test e la nota. Non scrivere tu codice o piano dei test: formula la richiesta e la decisione sul lavoro presentato.''', 'valutare con ragione causale e ambito della prova', 'La soluzione distingue risultato parziale e chiusura.', 9),
('Un test verde ha un perimetro', '''Puoi accettare il risultato sul pulsante come prova locale, ma non la chiusura. Chiedi verifica del recupero con K, dell’ordine realmente creato e della separazione email, con confronto al design e ai vincoli precedenti.

La nota “problema risolto” non permette una ripresa affidabile: mancano causa supportata, cambiamento, prove, limiti e riferimenti. Chiedi che l’agente conservi ciò che è utile al progetto, senza incollare tutta la conversazione.

Se hai chiesto soltanto “più test”, torna a S03–S04 e S28. Il criterio utile è quale comportamento rischia di regredire e quale osservazione può verificarlo.''', 'soluzione specifica anziché checklist generica', 'Conservare il risultato permette di alleggerire il contesto della prossima attività.', 9),
('Tre contributi, un patrimonio del progetto', '''kb-agentic governa la fedeltà della conoscenza alle fonti: che cosa sappiamo, da dove e con quali limiti. agentic-sdlc governa il cambiamento software: perché lo facciamo, che cosa deve ottenere e come lo verifichiamo. distill governa la scrittura: quali informazioni il lettore deve ricevere per agire correttamente.

distill non significa “taglia il più possibile”. Se la nota elimina la condizione “stessa chiave”, è più corta ma ha perso un fatto decisivo. Se la condizione resta nascosta in molte pagine irrilevanti, il lettore può comunque non usarla.

Conoscenza, esperienza registrata e spiegazioni si sostengono, ma non si equivalgono. distill non decide se il contratto sia vero e non sostituisce le verifiche del software.''', 'spiegare supporto distill senza terzo corso autonomo', 'Questo patrimonio deve restare disponibile nella cartella corretta.', 14),
('Il folder conta più della chat', '''Lavora nel folder persistente del progetto. Le skill sono installate nell’ambiente dell’agente; fonti, decisioni, analisi e handoff prodotti appartengono al progetto, spesso sotto ai_docs/. Un handoff è un passaggio di consegne sullo stato del lavoro e sul punto da cui riprendere.

Le due skill funzionano in Standalone con i file. devPNT è un prodotto separato che può aggiungere governance quando configurato: non è necessario per seguire il corso o rendere utilizzabile il patrimonio. Qui non lo usiamo.

In Standalone l’analisi autorevole del cambiamento è il file ANALYSIS in ai_docs/solutions/. Con devPNT configurato, piani e artefatti governati passano invece per proposte versionate: la persona le approva, poi ne vengono conservate copie di consultazione nei file. Le guide operative restano leggibili in ai_docs/reference/. Una copia non sostituisce l’artefatto governato approvato. Sono due modalità di autorità, non due modi di garantire che l’agente abbia capito.

Su più progetti, una conoscenza trasferibile può essere riusata solo rispettando provenienza, ambito e autorizzazioni. Non assumere che una regola di Orione sia valida ovunque o che aprire una chat nuova renda accessibili cartelle diverse.''', 'insegnare condizioni operative e confini', 'Ripartire richiede recupero, non un archivio riversato nel prompt.', 11),
('Conoscenza crescente, contesto selezionato', '''Per lavorare sul recupero di un ordine servono contratto, decisione su K, stato del guasto e parti coinvolte. Non servono necessariamente tutta la storia commerciale e ogni conversazione del team.

Il metodo cerca di mantenere piccolo e pertinente il contesto del compito, lasciando fuori le informazioni non necessarie e recuperando quelle che servono. “Vuoto” può descrivere il punto di ripartenza, non il contesto sufficiente per svolgere il lavoro.

Non c’è qui una prova che meno contesto migliori sempre il risultato. Eliminare una condizione decisiva lo peggiora. La domanda utile è: «Quali informazioni ti servono per questo compito e dove le recuperi?». Se il recupero fallisce, la lacuna va resa esplicita.''', 'evitare legge universale del contesto piccolo', 'Dopo un risultato concreto puoi chiedere di preparare la compattazione.', 15),
('Prima di compattare, prepara la ripresa', '''La raccomandazione dell’autore è compattare il contesto non appena si è ottenuto un risultato concreto, chiedendo prima all’agente: «vorrei compattare il contesto».

Non è un comando magico delle skill. È una richiesta che permette all’agente di salvare, se necessario, un handoff e controllare che il risultato utile sia persistente. Compattare significa ridurre la storia mantenuta nel contesto; aprire una sessione nuova è un’altra forma di ripartenza.

Prima di procedere verifica dove sono risultato, prove, decisioni e punti ancora aperti, e come la prossima sessione potrà riprenderli. Un handoff riassume lo stato operativo e punta alle fonti: non sostituisce tutte le decisioni durevoli. La compattazione non è garantita senza perdite.''', 'insegnare gesto e preparazione coerenti con richiestaautore', 'La frase è utile solo se precede il salvataggio necessario.', 15),
('Accetti di compattare subito?', '''L’agente ha trovato la causa di un baco, ma la scelta fra due soluzioni è ancora soltanto nella chat. Dice: «Abbiamo un risultato concreto, compatta pure; salverò il riepilogo dopo».

Come rispondi? Chiedi ciò che serve prima della compattazione, distinguendo il risultato acquisito dalla decisione ancora aperta. Non scrivere tu l’handoff: il tuo atto è richiederlo e verificare la possibilità di ripresa.''', 'valutare ordine salvataggio/compattazione', 'Un risultato concreto non elimina lo stato incompleto da conservare.', 15),
('Salvare prima, riprendere dai riferimenti', '''Rispondi: «Vorrei compattare il contesto. Prima salva la causa e le sue evidenze, indica la scelta ancora aperta e prepara il punto di ripresa. Mostrami i riferimenti ai file salvati; poi procediamo».

Il risultato concreto è l’indagine, non la decisione definitiva sul fix. La prossima sessione deve poter distinguerli. Conservare lo stato dopo la perdita della conversazione può essere troppo tardi.

Se hai detto soltanto “riassumi”, torna a S32–S34: il riepilogo deve essere persistente e collegato alle evidenze. L’atto della persona è verificare il passaggio di consegne, non ritenere che la parola handoff garantisca continuità.''', 'soluzione e limite della raccomandazione', 'Quanto di questo patrimonio conviene mantenere dipende anche dal progetto.', 15),
('Una settimana, un mese, anni', '''Dopo una settimana, la decisione su K può evitare di dover richiedere ancora il contratto. Dopo un mese, la nuova regola richiede aggiornare fonte e conclusioni dipendenti. Dopo anni, una nuova persona può ritrovare ragioni, alternative scartate e prove dei cambiamenti.

Questi sono scenari condizionati alla registrazione, consultazione e manutenzione, non tempi di risparmio misurati. Anche buone note curate possono fornire questa continuità.

L’esperienza del progetto è utile quando guida domande e verifiche nuove. Un vecchio incidente non prova la causa del prossimo. Lo stesso patrimonio può aiutare a evitare una regressione oppure propagare una conclusione sbagliata se nessuno ne controlla più la validità.''', 'riportare accumulo e rischio neltempo', 'Adottare il metodo richiede giudicare anche il suo costo.', 12),
('Le diffidenze hanno conseguenze reali', '''«Più documenti rallentano». Vero: scrivere, leggere e mantenere costa; il processo deve essere proporzionato. «Le note possono essere sbagliate». Vero: provenienza e revisione rendono gli errori controllabili, non impossibili.

«L’agente seguirà regole invece di risolvere il problema». Una risposta è giudicare gli esiti concreti: ragioni recuperate, vincoli preservati e prove pertinenti. Se produce artefatti vuoti, il metodo è stato applicato male. «Conservare tutto riempie il contesto». L’archivio deve supportare selezione, non lettura indiscriminata.

Non chiediamo fiducia cieca. Chiediamo di valutare quale problema il processo affronta, quale controllo aggiunge e quale costo richiede. Una buona nota può bastare; un progetto in evoluzione può rendere utile una disciplina ripetibile.''', 'affrontare costi senza difesa promozionale', 'Confrontiamo due condizioni senza inventare vantaggi misurati.', 13),
('Confrontare a parità di informazioni', '''Alba e Bora sono progetti inventati. Alba ha un’unica regola stabile, una nota breve mantenuta e una modifica occasionale. Bora cambia fornitore, ha più modalità di recupero e più persone che intervengono nel tempo.

In entrambi i confronti, note curate e skill ricevono le stesse fonti, le stesse ragioni e lo stesso compito. Le skill rendono esplicite consultazione, validità, impatto e chiusura; se le note sono governate da istruzioni equivalenti, gli esiti possono equivalere.

La differenza da valutare non è “agente intelligente contro agente smemorato”. È il costo di rendere continuo e verificabile il lavoro in quelle condizioni. Non sappiamo ancora misurare quale alternativa vinca per un team reale.''', 'insegnare alternativa sufficiente senza benchmarkfittizio', 'Prova a formulare una scelta per un caso diverso da Orione.', 13),
('Scegliere, senza promessa automatica', '''Casi nuovi inventati: Cobalto ha una sola trasformazione stabile documentata in una nota mantenuta; Selene gestisce ricevute con regole cambiate, eccezioni storiche e più integrazioni. L’agente propone a entrambi: «Caricherò tutto l’archivio a ogni attività e userò sempre il percorso completo».

Formula la tua risposta. Quale problema ti porta a considerare le skill? Che cosa può bastare in Cobalto? Quale patrimonio vuoi ritrovare in Selene? Quali costi e limiti rendi espliciti? Come correggi la proposta dell’agente?

La risposta deve collegare scelta e condizioni del lavoro. Ripetere “fonti, Vision, review” senza ragioni non dimostra la decisione richiesta.''', 'trasferimento cumulativo O1/O7', 'La soluzione confronta le condizioni, non assegna un vincitore universale.', 13),
('Una scelta motivata e rivedibile', '''In Cobalto una nota curata può bastare finché conserva la regola, la fonte e resta consultata. In Selene la storia rende più importante una disciplina di recupero, validità e cambiamento: chiedi quali vincoli precedenti sono coinvolti e quali fonti vanno riaperte.

Contesti sia lettura indiscriminata sia percorso completo uniforme. Chiedi selezione pertinente e livello proporzionato al rischio. Rendi espliciti manutenzione, possibilità di errori e assenza di un risparmio garantito.

Se hai scelto le skill solo perché Selene è grande, torna a S37–S39: contano evoluzione e dipendenze, non una dimensione nominale. Il beneficio cercato è costruire sul lavoro precedente senza cancellarne le ragioni, restando capaci di correggerle.''', 'soluzione trasferimento e rispostainsufficiente', 'Puoi applicare lo stesso giudizio al tuo progetto senza modificarlo.', 13),
('Il prossimo gesto nel tuo progetto', '''Applicazione facoltativa: scegli un documento non riservato del tuo progetto, accessibile all’agente. Chiedi in sola lettura: «Spiega quale regola sostiene, cita il passaggio e i limiti; proponi solo a parole una modifica che la tocchi, indicando beneficio, decisioni da prendere e prove mancanti. Non modificare file né eseguire operazioni».

Controlla se la risposta risale alla fonte, distingue storia e validità, preserva i vincoli e lascia a te le scelte aperte. Non devi redigere tu claim o design. Se non vuoi usare il progetto, usa questo caso inventato: una nota dice che ristampare una ricevuta deve conservare la data dell’acquisto, mentre l’agente propone di usare sempre la data di stampa. Chiedi il motivo storico e se cambia il significato della ricevuta prima di approvare.

Puoi tornare a questo confronto in una sessione successiva: che cosa è realmente ritrovabile? Il corso finisce qui; efficacia su persone non verificata. Il successo operativo delle skill va giudicato sul lavoro, non sulla loro sola presenza.''', 'preservare applicazionefacoltativaUC5e chiusura', 'Fine del percorso. Porta una richiesta e un criterio di giudizio nel lavoro successivo.', 12),
]
MODULES = [(1,8),(9,13),(14,18),(19,22),(23,30),(31,36),(37,42)]
ADDITIONS = {
29:'Una sessione futura deve ritrovare la guida sulla separazione delle notifiche. Dove chiedi all’agente di cercarla, prima di riscriverla?',
30:'Per la guida chiedi di consultare ai_docs/reference/INDEX.md e aprire il riferimento pertinente in ai_docs/reference/. Non trattare una guida non letta come un controllo eseguito.',
35:'L’agente aggiunge che, se una copia locale contraddice una proposta approvata in devPNT configurato, basta scegliere la copia. Contesti questa regola? Che cosa cambia se il lavoro è invece Standalone?',
36:'Con devPNT configurato chiedi di verificare l’artefatto governato approvato e riallineare la copia: non scegli la copia come autorità alternativa. In Standalone l’analisi autorevole è il file ANALYSIS del progetto. In entrambe le modalità il risultato da riprendere deve essere recuperabile prima di compattare.'}
for unit,addition in ADDITIONS.items():
    title,body,why,transition,claim=UNITS[unit-1]
    UNITS[unit-1]=(title,body+'\n\n'+addition,why,transition,claim)
OBJECTIVES = [
'Motivare il valore delle skill e distinguere patrimonio durevole da contesto del compito.',
'Giudicare una risposta con fonte e ambito, chiedendo all’agente ciò che manca.',
'Contestare il riuso di informazioni incompatibili e chiedere evidenza che chiarisca l’ambito.',
'Giudicare livello e perimetro dichiarati dall’agente attraverso effetti, rischio e beneficio.',
'Giudicare indagine, soluzione e chiusura preservando vincoli e prove pertinenti.',
'Collaborare con le due skill e distill e preparare una ripresa verificabile prima della compattazione.',
'Motivare una scelta proporzionata fra note curate e metodo sul proprio lavoro e nel tempo.']
CHECKS = [7,12,17,21,29,35,40]
CONCEPTS = [('CO12', '-',1,13,2,5),('CO11','-',1,2,6,9),('CO1','-',1,1,6,11),('CO2','CO1',2,2,6,9),('CO3','CO2',2,3,9,10),('CO4','CO3',2,4,10,12),('CO5','CO4',3,5,14,15),('CO6','CO2',4,6,19,21),('CO7','CO6',5,8,24,26),('CO8','CO7',5,9,26,29),('CO9','CO5; CO8',6,11,31,35),('CO13','CO11',6,14,31,31),('CO14','CO1',6,15,34,35),('CO10','CO12; CO14',7,12,37,40)]
MEANINGS = ['nota utile e confronto equo','skill, istruzioni distinte dai risultati','contesto e continuità','cartella e consultazione mirata','artefatto, provenienza e lettura','claim, grafo e risposta con provenienza','validità, conflitto e propagazione','beneficio, confini e triage','bisogni, comportamento, flussi e rischi','capacità, design, review, prove e GUIDE','responsabilità e modalità','contratto di scrittura e distill','compattazione preparata e handoff','valore nel tempo']
# Incipit refer to the visible learner surface, including ordering within a unit.
TRACES = [
('CO12: nota utile',2,'La nota di decisione conserva',5,'La storia suggerisce quindi','Il motivo registrato orienta il giudizio sul nuovo fix.'),
('CO12: confronto equo',8,'Anche una nota curata',39,'In entrambi i confronti','Alternativa esplicita prima del confronto cumulativo.'),
('CO11: skill',6,'Una skill è',9,'kb-agentic gli prescrive','Definizione prima della prescrizione operativa.'),
('CO1: contesto',6,'Il contesto è',11,'L’agente usa riferimenti','Disponibilità distinta da lettura prima della selezione.'),
('CO2: cartella',6,'I file persistenti',9,'Non deve fidarsi','Il file esiste ma serve consultarlo.'),
('CO2: indice',11,'Un indice è',11,'L’agente usa riferimenti','Definizione prima dell’uso nello stesso paragrafo.'),
('CO3: provenienza e lettura',9,'La provenienza indica',10,'Un claim è','Fonte riapribile e ambito di lettura prima del claim.'),
('CO4: claim e ambito',10,'Un claim è',11,'La KB organizza','Prima affermazione con condizioni, poi organizzazione.'),
('CO4: grafo KB e grafo didattico',11,'Un grafo è',11,'Questo grafo degli argomenti','Definizione e percorso concreto prima della distinzione.'),
('CO4: risposta con provenienza',10,'Davanti a una risposta',12,'Che cosa contesti','Domanda insegnata prima del nuovo caso.'),
('CO5: validità storica',14,'I periodi non si sovrappongono',15,'Due documenti fittizi','Successione prima del conflitto simultaneo.'),
('CO5: conflitto',15,'“Contestato” significa',16,'Arriva un chiarimento','Incertezza conservata prima della soluzione.'),
('CO5: propagazione',16,'La nota che aveva assunto',18,'Dopo il chiarimento chiedi','Riesame dei derivati prima del riuso nella soluzione nuova.'),
('CO6: triage',19,'agentic-sdlc distingue',21,'Come rispondi sul livello','Effetti e rischio prima del giudizio.'),
('CO6: Vision',20,'La Vision dichiara',21,'Usa gli effetti','Beneficio e confini prima della decisione.'),
('CO7: bisogni e comportamento',24,'Un use case descrive',25,'Una superficie è','Il bisogno precede i percorsi coinvolti.'),
('CO7: flussi e rischi',25,'Il contratto d’interfaccia descrive',26,'Il Capability Ledger è','Percorsi e rischi prima della scelta delle capacità.'),
('CO8: riuso e design',26,'Il Capability Ledger è',27,'Una correzione pulita','Capacità prima della soluzione coerente.'),
('CO8: review',27,'Un revisore indipendente',28,'Dopo l’implementazione','Review del progetto prima della review del risultato.'),
('CO8: prove',28,'Dopo l’implementazione',29,'Quale parte accetti','Evidenza con ambito prima del giudizio di chiusura.'),
('CO8: GUIDE',28,'Le guide operative si trovano',29,'Una sessione futura deve ritrovare la guida','Reperibilità prima della richiesta di consultazione.'),
('CO9: responsabilità',31,'kb-agentic governa',32,'Le due skill funzionano','Ruoli prima delle modalità di autorità.'),
('CO9: modalità',32,'In Standalone l’analisi autorevole',35,'L’agente aggiunge','Autorità e persistenza prima della decisione di ripresa.'),
('CO13: distill',31,'distill governa la scrittura',31,'distill non significa','Ruolo prima del contrasto perdita/rumore nello stesso testo.'),
('CO14: handoff',32,'Un handoff è',34,'Prima di procedere verifica','Passaggio di consegne definito prima della preparazione.'),
('CO14: compattazione',34,'vorrei compattare il contesto',35,'Come rispondi','Richiesta e controllo prima dell’esercizio.'),
('CO10: valore nel tempo',37,'Dopo una settimana',40,'Formula la tua risposta','Costi e accumulo prima del trasferimento cumulativo.')]
def write(name, text):
    (C/name).parent.mkdir(parents=True, exist_ok=True)
    (C/name).write_text(text.strip()+'\n',encoding='utf-8')
def ref(name, heading): return f'{BASE}/{name}#{heading}'
def table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','|'+'---|'*len(headers)]+['| '+' | '.join(map(str,r))+' |' for r in rows])
def main():
    assert len(UNITS)==42
    old=C/'history_3_2'
    old.mkdir(exist_ok=True)
    for name in ['COURSE_PLAN.md','SLIDE_CONTENT.md','CONCEPT_GRAPH.md','D-UC.md','D-IC.md','P-TM.md','sources.md','SIMULATION_REPORT.md','FEEDBACK_REPORT.md']:
        if not (old/name).exists(): shutil.copy2(C/name,old/name)
    a=ROOT/'ai_docs/solutions/ANALYSIS_course_agentic-sdlc-kb-agentic.md'
    if not (old/a.name).exists(): shutil.copy2(a,old/a.name)
    for n in range(1,8):
        (old/'modules').mkdir(exist_ok=True)
        if not (old/f'modules/M{n}.md').exists(): shutil.copy2(C/f'modules/M{n}.md',old/f'modules/M{n}.md')
    intro=f'''# Perché lavorare con kb-agentic e agentic-sdlc
Course version: {VERSION}
Delivery mode: self-study
Efficacy: efficacy not verified
Feedback flow: IC1

## Course Value
'''+table(['Profile','Baseline','Target capability','Teaching contribution','Observable check','Alternative and limits'],[['P1','Persona del team software che usa agenti; padronanza delle skill non accertata','Motivare quando e perché adottare le due skill con supporto di distill; giudicare benefici, costi e continuità del lavoro','Storia Orione: una protezione scoperta prima cambia il giudizio su un fix; si spiega il patrimonio durevole prima delle procedure',ref('SLIDE_CONTENT.md','s40'),'Note curate equivalenti possono bastare. Nessuna efficacia umana o superiorità causale dimostrata.']])+'\n\nTesto primario: Learner content e Transition sono visibili all’allievo. Complete explanation offre lo stesso testo al relatore, senza ragionamento essenziale nascosto. Fonti in sources.md; tutti i casi sono fittizi. Feedback diretto non disponibile, vedi D-IC IC1. Il PPTX3.0 precedente non rappresenta questa revisione.\n'
    out=[intro]
    for i,(title,text,why,transition,claim) in enumerate(UNITS,1):
        m=next(j for j,(lo,hi) in enumerate(MODULES,1) if lo<=i<=hi)
        role='check' if i in CHECKS else 'solution' if i-1 in CHECKS else 'orientation' if i==1 else 'closing' if i==42 else 'explanation'
        coverage='\nCovers: M1/O1' if i in (40,41) else '\nCovers: M6/O6' if i==42 else ''
        solution=f'\nSolution: S{i+1:02}' if role=='check' else ''
        extra_claims={6:[14],27:[9],28:[10],29:[10],30:[10],31:[11],35:[11],36:[11]}.get(i,[])
        citations='\n'.join('- '+ref('sources.md',f'claim-{n}') for n in [claim]+extra_claims)
        out.append(f'## S{i:02}\nModule: M{m}\nObjective: O{m}\nRole: {role}\nTitle: {title}\nValue contribution: {why}.{coverage}{solution}\n\n### Learner content\n\n{text}\n\n### Complete explanation\n\n{text}\n\n### Visual content\n\nUnità testuale: mostrare titolo e paragrafi nell’ordine scritto. Conservare le citazioni e i contrasti espliciti nel testo; nessun diagramma necessario e nessuna immagine che aggiunga fatti al caso. La soluzione resta una unità successiva, mai accanto alla domanda durante il tentativo.\n\n### Transition\n\n{transition}\n\n### Sources\n{citations}\n')
    write('SLIDE_CONTENT.md','\n'.join(out))
    rows=[]
    for m,(lo,hi) in enumerate(MODULES,1):
        cs='; '.join(x[0] for x in CONCEPTS if x[2]==m)
        rows.append([f'M{m}','P1',f'O{m}',cs,ref('SLIDE_CONTENT.md',f's{lo:02}'),ref('sources.md',f'claim-{UNITS[lo-1][4]}'),ref('SLIDE_CONTENT.md',f's{CHECKS[m-1]:02}'),f'M{m+1}' if m<7 else 'end'])
    plan=f'# Piano del corso\nCourse version: {VERSION}\nContent contract: slide-content-v1\nEfficacy: efficacy not verified\nFeedback flow: IC1\n\n## Pubblico e formato\nP1: sviluppatore o responsabile tecnico che lavora con agenti. Self-study senza competenze specifiche presunte. Il perché precede meccanismi e prescrizioni; l’esperienza è nelle tracce del progetto, non nel riaddestramento. Distill è supporto alla scrittura, non terzo corso autonomo. Nessuna durata misurata; rendering rinviato alla revisione del testo.\n\n## Obiettivi\n'+ '\n'.join(f'- O{i}: {o}' for i,o in enumerate(OBJECTIVES,1))+'\n\n## Sequenza\n'+table(['Module ID','Profile','Objective ID','Concepts','Explanation','Sources','Check','Next'],rows)+'\n\n## Teaching alignment\n'+table(['Objectives and use context','Evidence and success criterion','Explanatory bridge','Example or contrast','Support and correction'],[[f'O{m}: {OBJECTIVES[m-1]}',f'S{CHECKS[m-1]:02}: {UNITS[CHECKS[m-1]-1][2]}; risposta insufficiente: fiducia nella sola etichetta o nel sintomo risolto',f'S{lo:02}–S{CHECKS[m-1]-1:02}: {UNITS[lo-1][2]}','Caso e alternativa sviluppati nel testo; stessi dati nel confronto',f'S{CHECKS[m-1]+1:02}: soluzione e ritorno alla spiegazione'] for m,(lo,hi) in enumerate(MODULES,1)])+'\n\nS40–S41 coprono anche O1. S42 realizza UC5/IC4 facoltativamente con sola lettura e modifica solo ipotizzata. Le verifiche chiedono atti della persona; l’agente produce claim, livello e design. Il grafo traccia spiegazione e primo uso effettivo. Le vecchie lezioni sono archiviate in history_3_2. Nessuna conoscenza iniziale diventa PROVATO dopo una simulazione.\n'
    write('COURSE_PLAN.md',plan.replace('senza competenze specifiche presunte','senza conoscenza delle skill presunta; si presume lavoro software e uso ordinario degli agenti'))
    graph='# Grafo dei prerequisiti\n\nVersione 4.0-content. Stati iniziali P1 non misurati; nessuna competenza è PROVATO. Il grafo didattico ordina spiegazioni, non sostituisce la KB. Gli ID conservano i significati3.2; CO13/CO14 aggiungono scrittura e compattazione. Le sottorighe precisano componenti, senza duplicare il grafo. Un primo uso è un ragionamento dipendente, non la comparsa della parola. Le definizioni nello stesso paragrafo precedono il loro uso.\n\n'+table(['Concept ID','Meaning','Prerequisites','Profile','Initial state','Evidence','Source','Objectives'],[[c,MEANINGS[j],d,'P1','DA_INSEGNARE','-',ref('sources.md',f'claim-{cl}'),f'O{m}'] for j,(c,d,m,cl,ex,use) in enumerate(CONCEPTS)])+'\n\n## Traccia ai passaggi effettivi\n'+table(['Concept and meaning','Explanation locator and incipit','First dependent use locator and incipit','Why order holds'],[[c,ref('SLIDE_CONTENT.md',f's{ex:02}')+' «'+ei+'»',ref('SLIDE_CONTENT.md',f's{use:02}')+' «'+ui+'»',why] for c,ex,ei,use,ui,why in TRACES])
    write('CONCEPT_GRAPH.md',graph)
    for m,(lo,hi) in enumerate(MODULES,1): write(f'modules/M{m}.md',f'# Modulo M{m}\n\nVersione 4.0-content. Obiettivo O{m}: {OBJECTIVES[m-1]}\n\nLa fonte unica è [SLIDE_CONTENT](../SLIDE_CONTENT.md#s{lo:02}), unità S{lo:02}–S{hi:02}; spiegazioni, verifica e soluzione sono visibili lì. Il modulo non conserva una seconda lezione concorrente. Feedback: IC1 nel D-IC. Fonti e limiti sono nel registro sources.md. Le versioni precedenti sono in history_3_2.\n')
    # Source record: reuse explained claims, refresh their exact supporting bytes.
    src=(old/'sources.md').read_text(encoding='utf-8')
    body=src[src.index('## claim-1'):]
    extra={14:'Distill applica un contratto prima della scrittura e un controllo di perdita/rumore: non cerca la brevità a costo delle informazioni necessarie. Fonte: copia esatta nello snapshot di distill/SKILL.md, §§1–5, proveniente dalla skill installata C:/Users/apint/.codex/skills/distill/SKILL.md. Il suo ruolo è la scrittura, non la certificazione dei fatti.',15:'Recupero mirato, risultato concreto e frase «vorrei compattare il contesto» sono indicazioni dell’autore in REPORT_indicazioni_revisione_2026-10-04.md §5. Il consiglio è preparare e verificare la persistenza prima della compattazione, non una legge sulla resa dei modelli né un comando automatico. Il supporto di continuità/handoff si trova in agentic-sdlc SKILL.md Write Triggers e Closure.',16:'Il debugging richiede evidenze locali prima della causa immaginata, ipotesi aggiornate, causalità supportata e correzione coerente con prevenzione dell’errore. Fonte: skills/agentic-sdlc-skill/debugging.md, Method passi1–5. La frase italiana in S27 è riportata verbatim dal passo4.'}
    sources=['skills/agentic-sdlc-skill/SKILL.md','skills/agentic-sdlc-skill/debugging.md','skills/agentic-sdlc-skill/hybrid.md','skills/agentic-sdlc-skill/guides.md','skills/agentic-sdlc-skill/review.md','skills/agentic-sdlc-skill/routing.md','ai_docs/strategic/skills_vs_standard_agents_team.md','ai_docs/vision/project_vision.md','ai_docs/vision/features/VISION_course_agentic-sdlc-kb-agentic.md']
    kb='distributions/kb-agentic-skill/skills/kb-agentic-skill/'
    sources += [kb+n for n in ['SKILL.md','distillation.md','taxonomy.md','reconciliation.md']]
    sources += [BASE+'/REPORT_indicazioni_revisione_2026-10-04.md']
    hashes=[]
    with zipfile.ZipFile(C/'source_snapshot_2026-10-04.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sources:
            b=(ROOT/p).read_bytes(); z.writestr(p,b); hashes.append((p,hashlib.sha256(b).hexdigest()))
        b=Path('C:/Users/apint/.codex/skills/distill/SKILL.md').read_bytes();z.writestr('distill/SKILL.md',b);hashes.append(('distill/SKILL.md',hashlib.sha256(b).hexdigest()))
    body += '\n\n'+ '\n\n'.join(f'## claim-{k}\n\n{v}' for k,v in extra.items())
    write('sources.md','# Fonti del corso\n\nRegistro unico 4.0-content. Gli originali locali sono riaperti; lo snapshot source_snapshot_2026-10-04.zip conserva i byte insegnati. Distill è separato e la copia nello snapshot conserva la fonte installata. Le frasi sulle skill sono prescrizioni, non garanzie di conformità. Tutti i contratti, log ed eventi Orione/Alba/Bora/Cobalto/Selene e gli esempi di ricevute sono inventati; non sono misure né indicazioni legali. L’inferenza sul valore cumulativo è condizionata alla consultazione e manutenzione.\n\n'+table(['Fonte','SHA-256'],hashes)+'\n\n'+body)
    write('simulation_4_0/source_hash.json',json.dumps({'version':VERSION,'sha256':hashlib.sha256((C/'SLIDE_CONTENT.md').read_bytes()).hexdigest()},indent=2))
    packet=[]
    for i,u in enumerate(UNITS,1):
        if i in [n+1 for n in CHECKS]: continue
        packet.append({'id':f'S{i:02}','text':f'{u[0]}\n\n{u[1]}\n\n{u[3]}'})
    write('simulation_4_0/packet.json',json.dumps(packet,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
