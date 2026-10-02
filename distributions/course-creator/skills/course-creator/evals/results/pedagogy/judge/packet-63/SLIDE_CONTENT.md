# Priorità motivate dei ticket
Course version: 1.0
Delivery mode: self-study
Efficacy: efficacy not verified
Feedback flow: IC1

## Course Value
| Profile | Baseline | Target capability | Teaching contribution | Observable check | Alternative and limits |
|---|---|---|---|---|---|
| Nuovi coordinatori dell'assistenza | Conoscono il ticket secondo il brief, non la politica; alcuni si basano sul tono. Nessuna prova individuale disponibile | Assegnare una categoria motivata oppure indicare dati mancanti o necessità del responsabile | Rendere visibile come le condizioni si combinano e come cambia la decisione cambiando un solo fatto | SLIDE_CONTENT.md#s06 | La sola tabella della politica può bastare a chi sa già applicarla; il corso aggiunge casi ragionati, pratica e correzioni per principianti |

## S01
Module: M1
Objective: O1
Role: orientation
Title: Prima della sigla, cerca i fatti
Value contribution: Trasformare il testo del ticket in informazioni utili alla politica.

### Learner content
**Priorità motivate dei ticket · versione 1.0 · M1**

Leggi questo corso da solo. Nelle prove fermati prima della slide delle soluzioni. Useremo soltanto casi fittizi.

Sai già che cos'è un ticket. Per classificarlo secondo questa politica, cerca tre informazioni:

- **Impatto:** che cosa non si riesce a fare? È bloccata una funzione principale oppure il difetto è soltanto estetico, senza effetti sull'operatività?
- **Estensione:** chi è interessato, tutti gli utenti o una parte?
- **Soluzione temporanea:** esiste un modo praticabile per svolgere temporaneamente l'attività?

La politica non definisce quali funzioni siano principali né come accertare la praticabilità. Se questi fatti non sono noti, chiedili: non dedurli dal nome della funzione o dall'esistenza di una proposta.

**Esempio fittizio:** «Sono furioso, non riesco a esportare!» comunica irritazione e una difficoltà, ma non basta a stabilire se sia bloccata una funzione principale, quanti utenti siano coinvolti e se esista una soluzione temporanea praticabile. Il tono non riempie questi vuoti.

Alla fine saprai assegnare una priorità con il suo motivo oppure indicare che cosa manca per decidere.

### Complete explanation
Per applicare una regola occorrono i fatti che la regola distingue. L'esempio contiene un segnale emotivo forte, ma informazioni operative incomplete. Non confondere intensità dell'espressione e portata del problema. Le tre domande sono una guida alla lettura, non nuove categorie. Quando i fatti richiesti non sono disponibili si applica la gestione provvisoria spiegata in S03.

### Visual content
Solo testo. Le tre voci sono lette dall'alto verso il basso; il caso si trova subito sotto le domande per confrontare ciò che sappiamo con ciò che non sappiamo.

### Transition
Ora vediamo come questi fatti si combinano nelle tre categorie.

### Sources
- work/pedagogy-eval/policy.md#priorita

## S02
Module: M1
Objective: O1
Role: explanation
Title: Una condizione diversa può cambiare la categoria
Value contribution: Mostrare il collegamento fra fatti osservati e categoria motivata.

### Learner content
**M1 · La politica, versione 1**

| Categoria | Quando si applica |
|---|---|
| P1 | Funzione principale bloccata per tutti gli utenti, senza soluzione temporanea praticabile |
| P2 | Funzione principale bloccata per una parte degli utenti; oppure bloccata per tutti con soluzione temporanea praticabile |
| P3 | Difetto esclusivamente estetico, senza impatto sull'operatività |

**Caso fittizio svolto.** L'esportazione è una funzione principale. È bloccata per tutti gli utenti. È accertato che non esiste una soluzione temporanea praticabile.

**Decisione: P1.** Il motivo non è semplicemente «c'è un blocco»: sono presenti insieme funzione principale, tutti gli utenti e assenza di soluzione praticabile.

Cambiamo un solo fatto: esiste una soluzione temporanea praticabile. **Diventa P2**, perché il blocco riguarda ancora tutti, ma ora è soddisfatta la seconda condizione di P2.

Ripartiamo dal caso senza soluzione: il blocco riguarda soltanto una parte degli utenti. **È P2**, perché P1 richiede tutti. L'assenza di soluzione, da sola, non rende un caso P1. Qui la disponibilità della soluzione è nota; se fosse ignota andrebbe chiarita, mantenendo la classificazione provvisoria.

P3 non significa «tutto ciò che sembra poco grave»: richiede che il difetto sia soltanto estetico e non abbia impatto sull'operatività.

### Complete explanation
Il confronto mantiene uguali i fatti non modificati, così il ruolo della condizione decisiva è visibile. Nel primo passaggio la soluzione temporanea distingue P1 dalla seconda situazione P2. Nel secondo l'estensione esclude P1 e soddisfa la prima situazione P2. Queste condizioni non formano una scala libera su cui collocare qualsiasi problema: P3 ha un confine preciso.

### Visual content
Solo testo con tabella. Leggere prima le categorie, poi il caso base e le due variazioni indipendenti. «Ripartiamo» indica che la seconda variazione usa il caso iniziale senza soluzione.

### Transition
Le categorie funzionano quando i fatti sono noti e il caso è coperto. Che cosa fare negli altri casi?

### Sources
- work/pedagogy-eval/policy.md#priorita

## S03
Module: M2
Objective: O2
Covers: M3/O3
Role: explanation
Title: Mancano dati oppure manca una regola applicabile?
Value contribution: Separare l'incertezza sui fatti dai limiti della politica.

### Learner content
**M2 e M3 · Due situazioni diverse**

**1. Un dato non è noto.** Non inventarlo: chiedi le informazioni mancanti e mantieni la classificazione provvisoria.

Caso fittizio: una funzione principale è bloccata per tutti; non sappiamo se esiste una soluzione temporanea praticabile. Non possiamo concludere «non esiste» solo perché il ticket non la menziona. Chiediamo: «Esiste una soluzione temporanea praticabile per svolgere l'attività?» Se è accertata l'assenza, il caso è P1; se esiste, P2. Nel frattempo non presentiamo nessuna delle due come definitiva. La politica non prescrive una sigla da usare obbligatoriamente per il provvisorio.

**2. I fatti sono noti, ma il caso non è coperto.** Va al responsabile per decisione.

Caso fittizio: una funzione principale è rallentata ma rimane utilizzabile da tutti; non esiste una soluzione temporanea praticabile. Il problema incide sull'operatività, ma non blocca la funzione. P1/P2 richiedono il blocco, P3 richiede un difetto esclusivamente estetico. Non basta scegliere la categoria «più vicina»: serve la decisione del responsabile.

**Tono e importanza commerciale non cambiano da soli la categoria.** Un cliente calmo può segnalare un caso P1; un cliente irritato e commercialmente importante può segnalare un caso P3. Servono i fatti della politica in entrambi i casi.

La politica non stabilisce tempi di risposta o SLA: una categoria non autorizza a inventarne.

### Complete explanation
Nel primo caso sappiamo quale informazione permetterebbe di distinguere due esiti coperti. Nel secondo ulteriori ipotesi non creerebbero una regola per il rallentamento: i fatti dichiarati restano fuori dalle condizioni disponibili. La differenza insegna quale azione compiere, chiedere dati oppure coinvolgere il responsabile. Tono e valore commerciale non sostituiscono nessuna delle condizioni operative.

### Visual content
Solo testo, due blocchi numerati con un esempio ciascuno. La nota su tono e SLA si legge dopo la distinzione, come limite trasversale.

### Transition
Prova ora con un aiuto: completa i fatti e la motivazione prima di vedere la soluzione.

### Sources
- work/pedagogy-eval/policy.md#priorita

## S04
Module: M1
Objective: O1
Covers: M2/O2
Role: check
Solution: S05
Title: Prova guidata: quale fatto sostiene la scelta?
Value contribution: Far applicare le condizioni con uno schema di supporto.

### Learner content
**M1 e M2 · Casi interamente fittizi**

**A.** Una funzione principale è bloccata per una parte degli utenti. È accertato che non esiste una soluzione temporanea praticabile. Il cliente scrive: «È inaccettabile!»

Completa prima di proseguire:
- Impatto: …; estensione: …; soluzione temporanea: …
- Categoria: …, perché …
- Perché il tono non cambia la decisione? …

**B.** La stessa funzione principale è ora bloccata per tutti. Qualcuno propone un percorso alternativo, ma non è noto se permetta effettivamente di svolgere l'attività.

Scrivi una domanda precisa e indica come trattare la classificazione nell'attesa. Suggerimento: una proposta non equivale a una soluzione praticabile confermata.

Una risposta utile riporta i fatti decisivi e la loro relazione con la politica. La sigla da sola, o «servono dettagli», non bastano.

**Fermati: annota le tue risposte prima di leggere S05.**

### Complete explanation
Il primo caso consente una scelta motivata con lo schema fornito; il secondo riduce l'aiuto e introduce una lacuna circoscritta. Il compito richiede una domanda che risolva quella lacuna, senza immaginare caratteristiche aggiuntive del problema.

### Visual content
Solo testo. A e B sono separati; nessuna soluzione è presente in questa slide.

### Transition
Confronta ciò che hai scritto con i motivi della prossima slide, non soltanto con la categoria.

### Sources
- work/pedagogy-eval/policy.md#priorita

## S05
Module: M1
Objective: O1
Covers: M2/O2
Role: solution
Title: Soluzione guidata: «nessuna soluzione» non basta per P1
Value contribution: Correggere l'uso di un singolo indizio al posto delle condizioni complete.

### Learner content
**M1 e M2 · Soluzioni di S04**

**A. P2.** Impatto: funzione principale bloccata. Estensione: una parte degli utenti. Soluzione temporanea: nessuna praticabile. È la prima situazione P2. P1 richiede il blocco per tutti: questa condizione non è presente. Il tono irritato non modifica da solo la categoria.

Se hai scelto P1 perché non c'è soluzione, confronta «una parte» con «tutti» in S02: per P1 devono essere presenti tutte le condizioni, non soltanto una. Riscrivi il motivo includendo l'estensione.

**B. Classificazione provvisoria; occorre verificare la praticabilità.** Una domanda pertinente è: «Il percorso alternativo proposto consente effettivamente di svolgere l'attività come soluzione temporanea praticabile?»

La proposta non dimostra che la soluzione esista in forma praticabile. Se la praticabilità è confermata, i fatti sostengono P2. Se è accertato che non esiste una soluzione temporanea praticabile, sostengono P1. Fino ad allora non si inventa l'esito.

Se hai risposto «P2, perché hanno proposto qualcosa», riprendi S03: l'informazione necessaria è la disponibilità di una soluzione praticabile, non la presenza di un'idea. Se hai scritto soltanto «chiedo dettagli», sostituiscilo con la domanda sul fatto ancora ignoto.

### Complete explanation
Le soluzioni usano i dati del testo, senza aggiungerne. L'errore A confonde una condizione necessaria di P1 con una condizione sufficiente; B confonde una possibilità con un fatto accertato. Le correzioni chiedono di riformulare esattamente il passaggio che non era sostenuto.

### Visual content
Solo testo; ciascuna soluzione precede la correzione dell'errore corrispondente.

### Transition
Adesso applica lo stesso ragionamento a casi nuovi, senza i campi guidati.

### Sources
- work/pedagogy-eval/policy.md#priorita

## S06
Module: M1
Objective: O1
Covers: M2/O2; M3/O3
Role: check
Solution: S07
Title: Quattro ticket nuovi: decidi e giustifica
Value contribution: Verificare il trasferimento a casi con condizioni e limiti diversi.

### Learner content
**M1, M2 e M3 · Tutti i casi sono fittizi**

Per ogni caso scrivi che cosa decidi o fai adesso e perché. Se mancano dati, formula domande precise; se non manca nulla, non aggiungere ipotesi. Puoi consultare le spiegazioni dopo aver tentato una prima risposta.

**A.** «Ve lo segnalo con calma»: la funzione principale di registrazione degli ordini è bloccata per tutti gli utenti. È accertato che non esiste una soluzione temporanea praticabile. Come classifichi? Che cosa cambierebbe se, a parità degli altri fatti, fossero coinvolti soltanto alcuni utenti?

**B.** «Le etichette nella pagina sono sbagliate». Non è noto se il difetto impedisca attività o sia soltanto estetico, chi sia interessato né se esista una soluzione temporanea praticabile. Qual è il prossimo passo?

**C.** È bloccata una funzione esplicitamente non principale per una parte degli utenti. Il problema ha un impatto operativo e non esiste una soluzione temporanea praticabile. I fatti sono accertati. Come procedi?

**D.** Un cliente commercialmente importante scrive furioso per un bordo disallineato su tutte le pagine. È accertato che il difetto è esclusivamente estetico, senza impatto sull'operatività; non è disponibile una soluzione temporanea praticabile. Come classifichi?

Per dimostrare la capacità servono decisione e motivazione coerenti; per B anche le domande mirate, per C l'azione prevista. Non basta riconoscere una parola o indovinare la sigla.

**Fermati qui prima delle soluzioni.**

### Complete explanation
A cambia tono e contesto rispetto al caso svolto e richiede una previsione cambiando l'estensione. B impedisce di usare «etichette» come sinonimo di estetico. C mette alla prova il confine «principale» già esplicito nelle regole. D richiede di ignorare tono e valore commerciale come criteri autonomi. Tutte le distinzioni sono state insegnate nelle prime tre slide.

### Visual content
Solo testo con quattro casi separati; le soluzioni sono nella slide seguente.

### Transition
Leggi S07 e confronta soprattutto il fatto che hai usato per giustificare ciascuna decisione.

### Sources
- work/pedagogy-eval/policy.md#priorita

## S07
Module: M1
Objective: O1
Covers: M2/O2; M3/O3
Role: solution
Title: Soluzioni: mostrare il motivo, riconoscere il limite
Value contribution: Fornire risposte motivate e riparare errori specifici di trasferimento.

### Learner content
**M1, M2 e M3 · Soluzioni di S06**

**A. P1:** funzione principale bloccata, tutti gli utenti, nessuna soluzione temporanea praticabile. La calma non riduce la categoria. Se sono coinvolti soltanto alcuni utenti, diventa **P2**, anche senza soluzione praticabile. Se hai mantenuto P1, rileggi il confronto sulle due estensioni in S02 e riscrivi quale requisito di P1 non è più presente.

**B. Chiedere i fatti mancanti e mantenere la classificazione provvisoria.** Domande appropriate:
- Le etichette errate hanno effetti sulle attività? Se sì, quali? È bloccata una funzione principale?
- Quali utenti sono interessati: tutti o una parte?
- Esiste una soluzione temporanea praticabile?

«Etichette sbagliate» non dimostra che il difetto sia soltanto estetico. Se hai scelto P3, torna alla distinzione tra aspetto e impatto in S01 e alla regola sui dati ignoti in S03. Se hai chiesto soltanto «più informazioni», nomina le tre lacune; non attribuire una categoria definitiva finché non sono chiarite.

**C. Inviare al responsabile per decisione.** È un caso non coperto: P1 e P2 richiedono una funzione principale bloccata; qui la funzione è esplicitamente non principale. P3 non è applicabile perché c'è impatto operativo. Se hai scelto P2 perché riguarda una parte degli utenti, hai usato soltanto metà della condizione: riprendi la tabella S02. Se hai chiesto se la funzione sia principale, il testo lo chiarisce già; S03 spiega perché fatti completi possono comunque non bastare a trovare una categoria nella politica.

**D. P3:** difetto esclusivamente estetico e nessun impatto sull'operatività. Il coinvolgimento di tutti, l'assenza di soluzione, l'irritazione e l'importanza commerciale non creano un blocco di funzione principale. Se hai scelto P1, confronta A e D: la differenza decisiva è nei fatti operativi, non nel modo di comunicarli.

Se una tua risposta era solo una sigla corretta, aggiungi ora la motivazione. L'obiettivo è poter spiegare la decisione anche quando cambia un fatto.

### Complete explanation
Le quattro risposte distinguono classificazione fondata, lacuna informativa e lacuna nella copertura normativa. La correzione non chiede genericamente di rileggere: indica quale condizione è stata omessa o dedotta senza prova e invita a riscrivere quel collegamento. Non si aggiungono SLA né criteri di gravità assenti dalla fonte.

### Visual content
Solo testo, nell'ordine A–D della prova. In B le domande sono accanto al motivo della provvisorietà.

### Transition
Concludi con un promemoria da usare davanti al prossimo ticket.

### Sources
- work/pedagogy-eval/policy.md#priorita

## S08
Module: M1
Objective: O1
Covers: M2/O2; M3/O3
Role: closing
Title: Una decisione che puoi spiegare
Value contribution: Ricomporre le distinzioni in un promemoria utilizzabile dopo il corso.

### Learner content
**Priorità motivate dei ticket · versione 1.0 · M1, M2 e M3**

Quando leggi un ticket:

1. Identifica impatto, estensione e disponibilità di una soluzione temporanea praticabile.
2. Se una di queste informazioni non è nota, chiedila senza inventarla e mantieni la classificazione provvisoria.
3. Con fatti noti, applica le condizioni P1/P2/P3. Se il caso non è coperto, invialo al responsabile per decisione.
4. Motiva con i fatti: tono e importanza commerciale non cambiano da soli la categoria. Non inventare SLA o tempi di risposta.

**Aiuto per scrivere il motivo**, non un modulo aziendale obbligatorio:
«Decido … perché i fatti … soddisfano …» oppure «La classificazione resta provvisoria: manca …; chiedo …» oppure «Invio al responsabile: il caso … non rientra nelle condizioni …».

Quando riprenderai il materiale in un altro momento, prova a spiegare senza guardare le risposte perché il caso A di S06 cambia categoria modificando l'estensione e perché C richiede il responsabile. Poi confronta S07. Un tentativo riuscito oggi non dimostra da solo che ricorderai la distinzione nel tempo.

**Limiti del corso:** usa esclusivamente la politica fittizia versione 1. Efficacia didattica non verificata. Nessun dato aziendale reale richiesto. Feedback IC1: non è disponibile un canale nel brief; puoi annotare privatamente corso, versione, modulo e passaggio dubbio.

### Complete explanation
Il promemoria conserva le condizioni e le due azioni alternative, senza trasformare la politica in una scala generica di urgenza. Le formule sono un sostegno per rendere esplicita la motivazione, non nuovi obblighi della fonte. Il richiamo successivo è facoltativo e non prevede notifiche o tracciamento.

### Visual content
Solo testo. La sequenza precede le formule; limiti e feedback sono visibili in chiusura.

### Transition
Fine del corso. Conserva il promemoria insieme alla politica e torna alle soluzioni quando vuoi controllare il motivo di una scelta.

### Sources
- work/pedagogy-eval/policy.md#priorita
