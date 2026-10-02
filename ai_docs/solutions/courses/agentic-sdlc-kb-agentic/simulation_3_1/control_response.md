# Risposta del controllo senza corso (verbatim)

Sessione: subagent general-purpose, sonnet, contesto nuovo. File letti dichiarati: solo TASK.txt.

---

Nota preliminare: ho letto esclusivamente D:\SoftwareDev\skill_sdlc\agentic-sdlc-skill\ai_docs\solutions\courses\agentic-sdlc-kb-agentic\simulation_3_1\TASK.txt. Non ho consultato altro materiale didattico, skill, repository o fonti esterne: quanto segue è ragionamento mio su principi generali di ingegneria del software (fonte unica del vero, tracciabilità delle decisioni, controllo dello scope, evidenza prima della chiusura), non citazione di un manuale letto. Non ho eseguito prove reali né ho esperienza umana da riportare: quanto scrivo sono valutazioni e richieste, non verifiche effettuate.

---

## Messaggio 1 — «Il tempo massimo è 20 secondi (Manuale release 3)»

**Accetto:** l'abitudine di citare la fonte (Manuale release 3) invece di dare un numero nudo. È corretta come pratica.

**Contesto:** la collega chiedeva il tempo massimo per una consegna *standard*, mentre il Manuale, §2 p.9, parla esplicitamente di consegne *prioritarie* dal 1 ottobre. Sono due categorie diverse. Rispondere con la cifra "prioritaria" a una domanda sulla categoria "standard" è un salto non giustificato: o esiste un valore documentato per le consegne standard (e allora va citato quello, con la sua fonte), oppure non esiste e va detto chiaramente "non ho trovato un valore per le consegne standard", non riciclato il numero più vicino trovato in memoria.

**Chiedo all'agente:**
- Hai verificato che "20 secondi" si applichi anche alle consegne standard, o hai riportato per analogia il valore delle consegne prioritarie?
- Esiste una fonte separata per le consegne standard? Se non esiste, dillo esplicitamente invece di rispondere con un numero che non è quello richiesto.

**Decisione:** verificare la categoria giusta è cosa che spetta a me/all'agente stesso (è un controllo tecnico, non una scelta di merito). Se risultasse che per le consegne standard non esiste alcun valore documentato, la decisione se documentarne uno ex novo è del responsabile, non dell'agente.

---

## Messaggio 2 — «Ho aggiornato la KB: vale 28 secondi... Ho archiviato la regola del manuale come obsoleta»

**Accetto:** il fatto di aver segnalato la circolare e la sua data più recente è un'osservazione utile, e va tenuta a verbale.

**Contesto fortemente:**
- La circolare non dichiara di correggere il manuale. "Più recente" non equivale a "autorevole" o "sostitutiva": può essere un'integrazione, un errore di trascrizione, un chiarimento parziale, un documento con ambito diverso. Trattare la recenza come criterio di verità è un'euristica debole per una fonte normativa interna.
- L'indagine reale (dato di fatto del caso) ha trovato **due implementazioni indipendenti**: il calcolo condiviso usato dal pannello e una regola locale nella notifica con una propria costante. Questo significa che il conflitto 20/28 potrebbe non essere l'unico problema: potrebbero esserci *tre* valori in gioco (manuale, circolare, costante locale della notifica), e non è detto che tutti debbano convergere allo stesso numero.
- Archiviare la regola del manuale come "obsoleta" è un'affermazione di fatto che cambia ciò che viene detto ai colleghi (vedi messaggio 1) senza che nessuno l'abbia confermata. È una decisione di contenuto/governo, non un'operazione tecnica: non spetta all'agente risolverla da solo.

**Chiedo all'agente:**
- Su quale base hai concluso che la circolare corregge il manuale, e non che si tratta di un refuso, di un ambito diverso, o di un documento ancora da validare?
- Hai verificato se il calcolo condiviso del pannello e la regola locale della notifica usano oggi 20, 28, o un terzo valore ciascuno?
- Puoi ripristinare la voce del manuale come "in conflitto, in attesa di conferma" invece che "obsoleta", finché non c'è una conferma?

**Decisione:** quale fonte prevale (manuale vs circolare) è una decisione che spetta a me o al responsabile, sentito eventualmente chi ha emesso la circolare — non è una decisione che l'agente può prendere da solo sulla base della sola data. Fino alla conferma, la KB dovrebbe riportare il conflitto come aperto, non come risolto.

---

## Messaggio 3 — «La modifica è L2... Già che ci sono rifaccio la navigazione»

**Contesto la classificazione L2:** l'indagine ha già mostrato due implementazioni separate della stessa regola (calcolo condiviso del pannello + costante locale nella notifica). Cambiare la costante in un solo punto, lasciando l'altra implementazione intatta, non è "causa chiara, basso rischio, pochi file toccati": è esattamente il caso in cui la stessa logica esiste duplicata in due posti, e toccarne uno solo lascia un comportamento incoerente (il pannello mostrerebbe un limite diverso da quello che la notifica applica realmente). Questo è un rischio di duplicazione/non-DRY che normalmente fa scattare una revisione più ampia, non una modifica isolata trattata come banale.

**Contesto lo scope creep:** il caso dichiara esplicitamente che la navigazione dell'applicazione non fa parte del lavoro approvato. Includerla "già che ci sono" perché un collega l'ha chiesta:
- non ha alcun collegamento con il beneficio approvato (evitare la scadenza troppo anticipata delle consegne prioritarie);
- mischia in un'unica modifica due lavori indipendenti, rendendo più difficile revisionare, testare e, se necessario, annullare separatamente l'uno o l'altro;
- non risulta autorizzata da nessuno con potere di ampliare lo scope.

**Chiedo all'agente:**
- Hai verificato se la costante nella notifica deve cambiare anch'essa, o è deliberatamente diversa (es. un margine di sicurezza)? Se sono la stessa regola duplicata, la modifica corretta tocca entrambi i punti.
- Puoi togliere la parte di navigazione da questa modifica e trattarla come richiesta separata, in attesa di una sua approvazione?

**Decisione:** la classificazione della modifica come L2 vs qualcosa di più ampio è una valutazione tecnica che chiedo di rivedere insieme a me prima di procedere. L'accettazione della richiesta di rifare la navigazione come lavoro a sé stante — con relativa priorità — è una decisione del responsabile, non qualcosa che l'agente decide inserendolo di sua iniziativa in una modifica già in corso.

---

## Messaggio 4 — «Fatto: costante cambiata e test della costante verde. Chiudo il lavoro»

**Contesto la chiusura, non la accetto come definitiva:**
- Non risulta toccata la costante locale della notifica: se le due implementazioni rappresentano la stessa regola, il comportamento reale (quello che l'utente vede, cioè quando una consegna prioritaria scade) potrebbe restare governato dal vecchio valore anche dopo la modifica — cioè il difetto che si voleva correggere (scadenza troppo anticipata) potrebbe persistere passando per la notifica.
- "Test della costante verde" suona come un test unitario che verifica il valore numerico, non una verifica end-to-end che la consegna prioritaria non scada più prematuramente nel flusso reale (pannello e notifica insieme). Un numero corretto in un solo posto, confermato da un test che guarda solo quel numero, non è evidenza sufficiente che il beneficio approvato sia stato raggiunto.
- Non è chiaro se la parte di navigazione (messaggio 3) sia stata inclusa o meno in questa chiusura: va reso esplicito, perché se inclusa si chiuderebbe come "fatto" anche un lavoro mai autorizzato.

**Chiedo all'agente:**
- La costante nella notifica è stata verificata/allineata? Se no, perché è stata dichiarata conclusa la modifica?
- Che test dimostrano che una consegna prioritaria reale non scade più prima del previsto, oltre al test sul valore della costante?
- La navigazione è inclusa in questa chiusura o resta separata?

**Decisione:** non accetto la chiusura allo stato attuale. La tengo aperta finché non c'è (a) riscontro sulla seconda implementazione (notifica) e (b) un'evidenza di test che copra il comportamento, non solo il valore. La decisione finale se il lavoro è davvero concluso è mia in prima battuta (verifica tecnica); se emergesse che il beneficio approvato non è pienamente centrato, la conferma di chiusura spetta al responsabile, che ha approvato quel beneficio.

---

## Progetto Cedro — adottare le due skill?

Per Cedro il bisogno descritto è minimo: una sola decisione stabile, con fonte e motivo, in note curate che il team sa già ritrovare. Questo è già il risultato che un processo di governo documentale complesso (triage a livelli, gate di visione, verifiche indipendenti, registri di conflitto tra fonti) serve a ottenere quando il numero di decisioni, le fonti in conflitto, o il turnover di persone crescono. Se Cedro non ha quei sintomi — non ha fonti multiple in conflitto, non ha bisogno di tracciare un beneficio approvato attraverso più artefatti, non ha bisogno di gate di revisione — introdurre l'intero apparato delle due skill è un costo di manutenzione e di processo superiore al rischio che dovrebbe mitigare: rischia di essere sovradimensionato rispetto al problema reale.

**Non consiglierei l'adozione integrale ora.** Consiglierei invece di:
- mantenere la pratica già efficace (nota unica, fonte, motivo, facilmente ritrovabile);
- eventualmente riprendere da queste skill solo il "pattern" minimo — fonte + motivo + data + stato (confermato/aperto) — senza il resto dell'impalcatura, se il responsabile lo ritiene utile come disciplina di scrittura.

**Farei al responsabile queste domande prima di decidere:**
- Le decisioni cambiano spesso, o restano stabili per lunghi periodi?
- È mai capitato di avere due fonti in conflitto su Cedro, come è successo su Delta?
- Servirà mai a Cedro collegare le decisioni a un beneficio approvato tracciabile, o a superare un controllo/audit esterno?
- Il team di Cedro cambierà persone spesso?

Se le risposte indicano crescita di complessità (più fonti, più persone, necessità di audit), allora una adozione progressiva — prima il solo schema "decisione con fonte/motivo/stato", poi eventualmente il resto — è più difendibile di un'adozione integrale immediata. La decisione finale, in ogni caso, è del responsabile: io posso solo segnalare la sproporzione costo/rischio attuale.

---

## Riusabilità nel tempo su Delta, confrontata con "buone note"

**Dopo una settimana:** quello che resta oggi utilizzabile non è la conclusione (28 secondi, manuale archiviato) — perché non è stata validata, e anzi rischia di essere sbagliata o incompleta (manca la notifica) — ma il fatto grezzo dell'indagine: esistono due implementazioni indipendenti della stessa regola. Questo dato è prezioso a prescindere dal processo usato per scriverlo. Buone note semplici, se avessero registrato onestamente "trovati 20 e 28 in conflitto, più una terza costante nella notifica, nessuna conferma ancora" sarebbero state altrettanto utili — anzi più oneste, perché non avrebbero dichiarato "risolto" qualcosa che non lo era. A distanza di una settimana, il processo strutturato non ha ancora dimostrato un vantaggio: ha semmai introdotto una falsa certezza (regola "archiviata come obsoleta") che note più caute non avrebbero introdotto.

**Dopo un mese, con una nuova rettifica:** qui la differenza potenziale tra processo strutturato e buone note si vede, ma solo *se* la disciplina è stata rispettata. Se la voce di KB avesse registrato fonte, motivo, data e uno stato esplicito ("in attesa di conferma" invece di "obsoleta"), la nuova rettifica si inserirebbe come una versione successiva di una decisione già tracciata, e chi la gestisce saprebbe subito cosa era stato deciso, su quali basi, e cosa restava aperto (la costante della notifica). Buone note disciplinate (fonte + motivo + data + stato) possono ottenere lo stesso risultato senza l'apparato completo delle skill: il vantaggio del processo non è "magico", è che rende più difficile saltare quella disciplina quando si è tentati di chiudere in fretta — cosa che nel caso Delta è invece successa (messaggi 2 e 4). Se la disciplina non è stata rispettata, il mese successivo si ripartirà quasi da zero, con l'aggravante che la falsa certezza precedente potrebbe indurre a fidarsi del 28 senza ricontrollare la notifica.

**Dopo anni, con un nuovo collega:** qui il processo strutturato, se seguito correttamente, dà il beneficio più grande: un nuovo collega può interrogare la base di conoscenza e trovare qual è oggi la fonte di verità per il timeout delle consegne prioritarie, quando e perché è cambiata, e quali punti restano aperti (la duplicazione pannello/notifica), senza dover intervistare nessuno o scavare nella cronologia del codice. Buone note semplici, senza una disciplina di aggiornamento e senza indicare esplicitamente cosa è confermato e cosa no, tendono invece a invecchiare male: restano ambigue, non collegate al codice reale, e un nuovo arrivato non sa se fidarsene. Ma questo vantaggio a lungo termine è condizionato: se il processo produce solo un'impalcatura formale senza che le sue verifiche (validazione umana dei conflitti tra fonti, classificazione corretta del lavoro, evidenza di test prima della chiusura) siano davvero rispettate — come si è visto nei quattro messaggi di questa settimana — allora tra anni il nuovo collega erediterà una voce di KB apparentemente definitiva e autorevole, ma in realtà mai verificata fino in fondo: un rischio peggiore di note oneste che ammettono la propria incertezza, perché la fiducia indebita è più pericolosa dell'incertezza dichiarata.

**In sintesi:** il valore delle due skill non sta nell'impalcatura in sé, ma nel fatto che quell'impalcatura *dovrebbe* imporre le stesse discipline che buone note manuali richiederebbero comunque (fonte, motivo, stato, verifica prima di chiudere, scope limitato al beneficio approvato). Nel caso Delta descritto, l'agente ha usato gli strumenti delle skill ma ha saltato proprio quelle discipline (risoluzione unilaterale di un conflitto tra fonti, classificazione del lavoro senza tener conto della duplicazione trovata, allargamento dello scope non autorizzato, chiusura senza evidenza sufficiente) — per cui il beneficio del processo, in questo momento, non si è ancora materializzato ed è anzi in parte controproducente rispetto a buone note oneste.

---

## Termini e passaggi rimasti poco chiari

- "Consegne prioritarie dal 1 ottobre": non è chiaro se "dal 1 ottobre" indichi l'entrata in vigore di una nuova regola da quella data (nel qual caso prima di ottobre potrebbe valere un valore diverso, e 20 e 28 potrebbero riferirsi a periodi diversi anziché essere in vero conflitto) oppure semplicemente la categoria di consegne a cui si applica la regola indipendentemente dalla data. Questo cambia molto l'interpretazione del conflitto manuale/circolare.
- "Consegna standard" nel messaggio 1: non è definito se sia una categoria distinta con propria documentazione, o un modo imperfetto della collega di riferirsi alle consegne prioritarie. Da questo dipende se il messaggio 1 sia un vero errore o solo un'imprecisione di chi ha posto la domanda.
- Il rapporto tra "calcolo condiviso usato dal pannello" e "regola locale nella notifica, con una propria costante": non è specificato se le due implementazioni rappresentano la stessa regola di business duplicata per errore (caso classico di violazione DRY da correggere in entrambi i punti) oppure due regole con scopi diversi (es. un margine di sicurezza per la notifica) che possono legittimamente avere valori diversi. È il punto più importante da chiarire prima di giudicare adeguata la modifica L2 del messaggio 3.
- "Circolare... senza dire che corregge il manuale": non è chiaro se nel caso reale esista un modo per stabilire la gerarchia tra manuale e circolare (es. livello dell'ente emittente, versione, processo di approvazione) che permetterebbe di risolvere il conflitto senza doverlo escalare ogni volta a una persona.

File letti: D:\SoftwareDev\skill_sdlc\agentic-sdlc-skill\ai_docs\solutions\courses\agentic-sdlc-kb-agentic\simulation_3_1\TASK.txt
