# Lavorare con kb-agentic e agentic-sdlc
Course version: 3.0-content
Delivery mode: self-study
Efficacy: efficacy not verified
Feedback flow: IC1

## Course Value
| Profile | Baseline | Target capability | Teaching contribution | Observable check | Alternative and limits |
|---|---|---|---|---|---|
| P1 | Persona del team software che usa agenti; conoscenza specifica delle skill non accertata | Motivare una risposta documentale e una modifica, distinguendo fonte, scelta e prova; scegliere disciplina proporzionata | Caso Orione: motivo storico, ambito, conflitto, decisione umana, capacità esistenti, comportamento verificabile e riuso nel tempo | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s50 | Note curate possono bastare; istruzioni equivalenti possono dare esiti equivalenti. Nessuna efficacia umana o superiorità causale verificata. |

### Come usare questa fonte

Il testo esatto di ciascuna slide è in Learner content; anche la Transition è visibile all’allievo. Complete explanation spiega l’intento e amplia il commento per un relatore, ma non contiene requisiti necessari nascosti alla lettura autonoma. Visual content specifica oggetti e relazioni da rendere senza inventare materiale. Questa è la fonte primaria: ogni modifica semantica del futuro PowerPoint deve tornare qui. Non comprimere una slide densa né dividerla senza aggiornare unità, rinvii e verifica della sequenza.

Il pubblico P1 comprende sviluppatori e responsabili tecnici nel percorso comune. Tutti i documenti, numeri e componenti di Orione sono fittizi. Le fonti delle affermazioni sulle skill sono nel registro sources.md e nel suo snapshot verificabile. Feedback diretto: non disponibile (IC1). Efficacia su persone non verificata.


## S01
Module: M1
Objective: O1
Role: orientation
Title: Perché aspettiamo proprio 30 secondi?
Value contribution: Il problema iniziale è riconoscibile senza conoscere le skill: una scelta è visibile, ma la sua giustificazione non è disponibile nella sessione corrente.

### Learner content

Orione è un’applicazione inventata che segue richieste inviate a un servizio esterno. Dopo l’invio mostra «in attesa». Se arriva una conferma, mostra «completata»; se non arriva entro 30 secondi, mostra «scaduta».

Una nuova collega apre il codice e trova il numero 30. Chiede: «Perché abbiamo scelto questo tempo?». Nessuno nella nuova chat ha la risposta. La scelta era stata discussa con un agente in una conversazione precedente.

Il numero è rimasto nel software. **La ragione va ritrovata.**

Seguiremo questa domanda per imparare a conservare ragioni verificabili e a usarle quando il software deve cambiare. Tutti i documenti e gli eventi di Orione sono esempi didattici inventati.

### Complete explanation

Il problema iniziale è riconoscibile senza conoscere le skill: una scelta è visibile, ma la sua giustificazione non è disponibile nella sessione corrente. Le tre etichette sono gli stati che la persona vede. Non occorre conoscere protocolli di rete o strumenti di documentazione per seguire la domanda. Il corso parte dal motivo storico, distinto dalla validità attuale che sarà esaminata dopo.

### Visual content

Tre stati in ordine: «Invio: in attesa», «Conferma ricevuta: completata», «Nessuna conferma entro 30 s: scaduta». Separare i due esiti alternativi con una biforcazione, non una sequenza completata→scaduta. Sotto, la domanda esatta del testo.

### Transition

Per trovare la ragione del numero dobbiamo recuperare ciò che il team aveva letto quando lo scelse.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S02
Module: M1
Objective: O1
Role: explanation
Title: Ritroviamo la ragione della scelta
Value contribution: La citazione fittizia fornisce tutti i dati usati nella spiegazione: tipo di richiesta, data limite, durata e istante iniziale.

### Learner content

Nel progetto troviamo una vecchia nota: «Abbiamo usato 30 secondi seguendo il Manuale Orione 2.1, §4.3, pagina 48».

Riapriamo il passaggio citato. Nel nostro esempio dice:

> «Per le richieste standard, fino al 30 giugno compreso, la conferma può arrivare entro 30 secondi dall’invio».

Ora possiamo spiegare **perché allora il team scelse 30**: la nota collega il numero a una regola del manuale e al suo periodo di validità.

Non abbiamo ancora dimostrato che 30 sia il tempo corretto per una richiesta di luglio. Per quella domanda servirà controllare la regola applicabile a luglio. Spiegare una scelta passata e confermarla per oggi sono due lavori diversi.

### Complete explanation

La citazione fittizia fornisce tutti i dati usati nella spiegazione: tipo di richiesta, data limite, durata e istante iniziale. Il locatore non viene presentato come fonte reale. La separazione tra ragione storica e validità attuale evita che il lettore interpreti il recupero della nota come autorizzazione a riusare il valore in ogni circostanza.

### Visual content

Mostrare nota e brano del manuale affiancati, con collegamento etichettato «passaggio citato». Evidenziare «fino al 30 giugno» insieme a «30 secondi», con pari rilievo.

### Transition

La nota ci ha aiutato perché conservava più del solo numero. Vediamo quale informazione ha fatto la differenza.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S03
Module: M1
Objective: O1
Role: explanation
Title: Una nota utile conserva anche il motivo
Value contribution: La comparazione mantiene identici compito e fonti.

### Learner content

Confrontiamo due note sulla stessa scelta.

| Nota insufficiente | Nota riutilizzabile |
|---|---|
| «Timeout: 30» | «Per le richieste standard fino al 30 giugno usiamo 30 secondi dall’invio. Motivo: Manuale Orione 2.1, §4.3, p.48. Per altri periodi la regola va verificata». |

**Timeout** significa qui il tempo oltre il quale Orione considera scaduta l’attesa della conferma.

La seconda nota permette a un’altra persona di controllare la scelta: conserva il valore, le condizioni, la ragione e il punto del documento da riaprire. La prima costringe a ricostruirli.

Una richiesta ben formulata all’agente può già produrre la seconda nota. Per questo caso singolo, chiedergli di prendere buone note può bastare.

### Complete explanation

La comparazione mantiene identici compito e fonti. La differenza è il contenuto della registrazione, non l’etichetta dello strumento che la produce. Il valore didattico è imparare a riconoscere ciò che rende la nota controllabile; non persuadere il lettore che ogni appunto richiede una skill. La definizione di timeout precede il suo uso successivo.

### Visual content

Tabella a due colonne con le frasi complete. Collegare «Motivo» al passaggio già mostrato in S02. Nessuna icona di vittoria associata a una skill.

### Transition

Se sappiamo già chiedere una buona nota, a che cosa può servire una skill?

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S04
Module: M1
Objective: O1
Role: explanation
Title: Una skill rende il metodo riutilizzabile
Value contribution: La skill viene introdotta solo dopo che il lettore ha visto il problema che le istruzioni dovrebbero affrontare.

### Learner content

Una **skill** è un insieme di istruzioni che l’agente può leggere e applicare per svolgere un tipo di lavoro. Può includere anche strumenti di controllo.

Invece di riscrivere ogni volta «conserva la fonte, precisa quando vale, segnala i dubbi», puoi richiamare un metodo che esplicita già quei requisiti.

Il contenuto delle istruzioni rimane distinto dal risultato: una skill può chiedere una nota verificabile, ma dobbiamo controllare che l’agente l’abbia davvero prodotta.

Nel caso Orione, le istruzioni sono riutilizzabili in altri progetti; la nota sui 30 secondi appartiene a Orione. **Installare di nuovo la skill non ricrea una nota perduta.**

### Complete explanation

La skill viene introdotta solo dopo che il lettore ha visto il problema che le istruzioni dovrebbero affrontare. Non è descritta come una memoria personale, un servizio o una garanzia. L’esempio distingue metodo generale e informazione specifica, preparando la separazione fisica tra installazione e cartella di progetto.

### Visual content

Due riquadri: «Istruzioni riutilizzabili: come lavorare» e «Nota di Orione: che cosa abbiamo deciso». Freccia dal primo al secondo etichettata «guida la produzione», mai «garantisce».

### Transition

Per seguire una fonte e per cambiare il software servono responsabilità diverse. Le due skill del corso le rendono esplicite.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S05
Module: M1
Objective: O1
Role: explanation
Title: Due domande, due responsabilità
Value contribution: I nomi entrano dopo la definizione di skill e sono associati a due domande già comprensibili.

### Learner content

**kb-agentic** organizza la conoscenza del progetto. KB significa base di conoscenza. In Orione deve aiutarci a rispondere: «Quale documento sostiene questa durata e a quali condizioni?».

**agentic-sdlc** guida il lavoro sul software. SDLC indica il ciclo di sviluppo del software. In Orione deve aiutarci a rispondere: «Se la durata cambia, che cosa dobbiamo modificare e come controlliamo il risultato?».

Il manuale può sostenere una regola senza dimostrare che il software la rispetti. Un software che supera un test non rende autentico un manuale.

Le due skill collaborano quando una conoscenza verificata diventa il punto di partenza di una modifica. Nel frattempo, la ragione dei 30 secondi deve restare accessibile alla prossima sessione.

### Complete explanation

I nomi entrano dopo la definizione di skill e sono associati a due domande già comprensibili. Non si chiedono ancora artefatti o sigle del processo. La distinzione fra fonte e prova software prepara il successivo passaggio di responsabilità e impedisce che una risposta documentale venga scambiata per verifica dell’implementazione.

### Visual content

Due colonne con nome, domanda ed evidenza cercata: «documento e condizioni» / «comportamento e verifica». Il collegamento fra le colonne si chiama «regola da considerare», non «modifica automatica».

### Transition

Dove conserviamo il risultato perché una nuova sessione possa ritrovarlo?

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S06
Module: M1
Objective: O1
Role: explanation
Title: Una nuova chat non è il nostro archivio
Value contribution: La distinzione riguarda disponibilità operativa, non una pretesa universale sui prodotti AI.

### Learner content

Il **contesto** è il materiale che l’agente può usare nella sessione corrente: messaggi, file letti e risultati degli strumenti disponibili in quel momento.

Una conversazione precedente può essere recuperabile nel client che usi, ma non va trattata come una memoria di progetto sempre presente e completa.

Se la nota sui 30 secondi resta solo in quella conversazione, la prossima sessione deve prima ritrovarla. Se la nota e il manuale stanno nella cartella del progetto, l’agente può riaprirli quando ne ha bisogno, purché abbia accesso ai file.

Il file persistente conserva l’informazione; **la lettura la rende disponibile al lavoro corrente**. Salvare senza consultare lascia il problema a metà.

### Complete explanation

La distinzione riguarda disponibilità operativa, non una pretesa universale sui prodotti AI. Alcuni client recuperano storia o memoria, ma il protocollo del progetto richiede riferimenti controllabili e accessibili. Conservazione e consultazione sono entrambe condizioni necessarie del beneficio mostrato.

### Visual content

Disegnare una cartella «Progetto Orione: nota + manuale» esterna al riquadro «Sessione corrente». Una freccia etichettata «apre i file pertinenti» porta dal contenitore alla sessione.

### Transition

Preparare la cartella significa rendere possibile questa riapertura, senza confonderla con l’installazione delle skill.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2

## S07
Module: M1
Objective: O1
Role: explanation
Title: Le skill stanno nell’ambiente, le decisioni nel progetto
Value contribution: Questa è l’impostazione operativa minima richiesta dalla Vision: usare la cartella di progetto come sede persistente.

### Learner content

Per lavorare con continuità, apri con il tuo agente la cartella persistente del progetto a cui appartiene il compito. Nella sessione successiva dovrà essere accessibile la stessa documentazione.

Le skill sono installate nell’ambiente dell’agente. I risultati del lavoro appartengono invece al progetto. Questa famiglia usa normalmente la cartella **`ai_docs/`** per la documentazione: `ai` richiama l’agente, `docs` i documenti.

In Orione vi conserviamo il percorso per ritrovare nota e fonte. L’agente deve poterli leggere; il solo nome `ai_docs/` non crea quei contenuti e non conferisce permessi di accesso.

Aprire una cartella vuota o reinstallare le istruzioni non trasferisce automaticamente la storia di Orione.

### Complete explanation

Questa è l’impostazione operativa minima richiesta dalla Vision: usare la cartella di progetto come sede persistente. Non si prescrivono menu o comandi di installazione specifici del client. La responsabilità della persona è scegliere il progetto corretto e rendere disponibili le fonti autorizzate; l’agente deve verificare cosa è realmente accessibile.

### Visual content

Due contenitori distinti: «Ambiente agente: skill» e «Cartella Orione: ai_docs/». Sotto il secondo: «nota, fonte, riferimenti». Nessuna freccia che simuli copia automatica all’installazione.

### Transition

Quando i file aumentano, dobbiamo trovare quello giusto senza leggere ogni volta tutto l’archivio.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2

## S08
Module: M1
Objective: O1
Role: explanation
Title: Un indice ci porta al documento pertinente
Value contribution: La sequenza separa tre funzioni: trovare, spiegare, verificare.

### Learner content

Un **indice** elenca documenti o argomenti e indica dove trovarli. Serve a scegliere che cosa aprire.

Per la domanda «Perché 30 secondi?» il percorso può essere:

1. La voce «Tempo di attesa delle conferme» rimanda alla nota della decisione.
2. La nota spiega il motivo e rimanda al Manuale 2.1, §4.3, p.48.
3. L’agente riapre quel passaggio e controlla che riguardi il tipo di richiesta e il periodo della domanda.

Il nome nell’indice non dimostra la regola. È il collegamento che porta alla fonte a renderla controllabile.

Così un archivio può contenere molti documenti mentre il contesto della sessione contiene soltanto quelli pertinenti al compito.

### Complete explanation

La sequenza separa tre funzioni: trovare, spiegare, verificare. Non tutto ciò che serve è in un unico file e non tutto l’archivio deve entrare nella chat. La consultazione mirata dipende da indici e riferimenti mantenuti: un collegamento errato o un documento illeggibile richiede di dichiarare il limite.

### Visual content

Tre riquadri numerati «Indice», «Nota con motivo», «Passaggio della fonte». Frecce etichettate rispettivamente «trova» e «verifica». Mostrare il periodo del manuale accanto al numero.

### Transition

La presenza di questi file ci permette anche di controllare se l’agente ha seguito il metodo.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2

## S09
Module: M1
Objective: O1
Role: explanation
Title: Il metodo si vede in ciò che resta
Value contribution: Qui il requisito del metodo diventa controllabile senza introdurre prematuramente tutta la review SDLC.

### Learner content

L’agente dice: «Ho seguito la skill». Per verificare il lavoro sui 30 secondi, chiediamo qualcosa di osservabile.

| Domanda di controllo | Evidenza da cercare |
|---|---|
| Da dove viene il numero? | Documento, versione e passaggio che lo sostiene. |
| Quando possiamo usarlo? | Tipo di richiesta e periodo dichiarati. |
| Come lo ritroviamo? | Nota e riferimento accessibili dal progetto. |
| Che cosa resta da sapere? | Limite esplicito, come la regola per luglio non ancora verificata. |

Un controllo automatico può rilevare un riferimento mancante. Stabilire se il passaggio citato sostiene davvero la frase richiede anche una lettura critica.

**La dichiarazione dell’agente non sostituisce l’evidenza.**

### Complete explanation

Qui il requisito del metodo diventa controllabile senza introdurre prematuramente tutta la review SDLC. Il lettore può già valutare l’output documentale. La distinzione fra struttura e significato evita l’equivalenza sbagliata tra un validatore verde e una risposta vera.

### Visual content

Tabella esatta. Sotto, due etichette separate: «Controllo della struttura» e «Verifica del significato», con esempi presi dalla prosa.

### Transition

A questo punto possiamo confrontare una skill e una richiesta di note senza attribuire a una delle due capacità inesistenti.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S10
Module: M1
Objective: O1
Role: explanation
Title: Quando basta chiedere una buona nota
Value contribution: L’alternativa viene trattata nelle sue condizioni migliori plausibili, non come un agente incompetente.

### Learner content

Per una scelta isolata, una fonte stabile e un solo lettore, la nota di S03 può già risolvere il problema. Una skill non aggiunge automaticamente informazione a una nota completa.

Quando il lavoro si ripete, però, ogni richiesta deve ricordare gli stessi requisiti: fonte, condizioni, dubbi, percorso di recupero. Un metodo riutilizzabile può ridurre la necessità di ricostruire quelle istruzioni a ogni sessione.

Questo vantaggio dipende dall’esecuzione: se l’agente ignora il metodo, il nome della skill non ci aiuta. E se una persona fornisce e verifica istruzioni equivalenti, può ottenere risultati equivalenti senza installarla.

La scelta riguarda **quanta disciplina serve e come mantenerla**, non una capacità speciale di memoria.

### Complete explanation

L’alternativa viene trattata nelle sue condizioni migliori plausibili, non come un agente incompetente. Il corso insegna un criterio di adozione proporzionato, che diventerà più concreto quando aumenteranno fonti, dipendenze e persone. Non ci sono dati per promettere un risparmio misurato.

### Visual content

Due percorsi verso la stessa nota: «Richiesta dettagliata» e «Skill applicata e controllata». Annotazione comune «stessi requisiti → risultati potenzialmente equivalenti».

### Transition

Proviamo ora a distinguere il numero trovato nel codice dalla ragione che lo giustifica.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S11
Module: M1
Objective: O1
Role: check
Title: Prova: che cosa manca alla risposta?
Value contribution: Il compito chiede di usare il percorso insegnato, non di ripetere una definizione di skill.
Solution: S12

### Learner content

In una nuova sessione, l’agente trova `timeout = 30` nel codice e risponde: «Il team aveva scelto il valore indicato dal fornitore». Non mostra altri riferimenti.

Nella cartella del progetto esistono l’indice, la nota e il manuale incontrati fin qui. Non sappiamo se l’agente li abbia aperti.

Prima di accettare la spiegazione, indica:

- quale percorso di lettura gli chiederesti di seguire;
- quali informazioni deve contenere la risposta;
- che cosa può dire della scelta passata e che cosa non può ancora dire di luglio.

Tenta una risposta prima di passare alla soluzione. Non occorre creare file.

### Complete explanation

Il compito chiede di usare il percorso insegnato, non di ripetere una definizione di skill. La presenza fisica dei documenti non viene scambiata per una lettura già eseguita. Il criterio distingue una ragione controllabile dalla semplice attribuzione al fornitore.

### Visual content

Solo testo, perché il lettore deve ricostruire il collegamento senza un diagramma già risolto.

### Transition

Confrontiamo la tua risposta con le evidenze effettivamente disponibili.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S12
Module: M1
Objective: O1
Role: solution
Title: Soluzione: prima ritrovare, poi concludere
Value contribution: La soluzione rende visibili sia un risultato sufficiente sia i due errori plausibili: memoria automatica e consultazione senza ambito.

### Learner content

Chiederei all’agente di aprire la voce pertinente dell’indice, leggere la nota della decisione e riaprire il passaggio del manuale.

Una risposta verificabile è: «La nota collega la scelta a Manuale Orione 2.1, §4.3, p.48: 30 secondi per richieste standard fino al 30 giugno. Questo spiega il motivo registrato allora. Non ho ancora verificato la regola di luglio».

Il codice, da solo, mostra il valore configurato: non prova il motivo storico e neppure l’intero comportamento del sistema.

Se hai risposto «l’agente se lo ricorda», rileggi S06–07. Se hai scritto soltanto «aprire il manuale», aggiungi il collegamento alla decisione e l’ambito di validità, come in S02–03.

### Complete explanation

La soluzione rende visibili sia un risultato sufficiente sia i due errori plausibili: memoria automatica e consultazione senza ambito. Riconosce anche che una costante non dimostra tutti i percorsi del software, senza richiedere ancora la progettazione dei test.

### Visual content

Riprendere il percorso in tre riquadri di S08 e aggiungere alla risposta finale una riga «Luglio: non verificato».

### Transition

Abbiamo riaperto una fonte già nota. Ora vediamo come prepararla perché altre domande possano ritrovarla.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S13
Module: M2
Objective: O2
Role: explanation
Title: Prima di riassumere, rendiamo la fonte riapribile
Value contribution: Si insegna la distinzione tra acquisizione, lettura ed estrazione.

### Learner content

Torniamo all’arrivo del Manuale 2.1, già usato nella nostra ricerca: come è stato preparato per renderlo riapribile? Il documento completo ha 200 pagine. **kb-agentic** conserva prima un artefatto della fonte e ne registra la provenienza: da dove arriva, quale versione è e quando è stata acquisita.

Per un PDF può servire un’estrazione testuale stabile, collegata all’originale. Una nuova versione viene identificata separatamente: non deve far sparire quella che sosteneva una decisione precedente.

Conservare il documento non significa averlo letto tutto. Se l’agente ha esaminato soltanto le pagine 1–30, deve dichiarare quel limite e proseguire la lettura per parti. Non può ancora sostenere di aver verificato la regola a pagina 48.

La fonte conservata permette di controllare, in seguito, anche il riassunto.

### Complete explanation

Si insegna la distinzione tra acquisizione, lettura ed estrazione. La skill ammette artefatti testuali estratti con provenienza, senza imporre sempre una copia di grandi binari. Il progresso dichiarato evita che un documento presente nell’archivio venga considerato integralmente elaborato. I numeri di pagine sono parte del caso fittizio.

### Visual content

Una barra «documento acquisito: 200 pagine» e una separata «lettura svolta: 1–30». Pagina 48 resta fuori dalla porzione letta.

### Transition

Dopo aver letto il passaggio pertinente, dobbiamo conservare la regola senza perderne le condizioni.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3

## S14
Module: M2
Objective: O2
Role: explanation
Title: Un claim dice una cosa che possiamo controllare
Value contribution: Il claim mostrato resta didattico: i locatori reali devono essere misurati sull’artefatto conservato e non inventati.

### Learner content

Un **claim** è una singola affermazione verificabile, collegata alla fonte che la sostiene. Non è il nome del documento né un riassunto indistinto di tutto il manuale.

Dal passaggio letto in S02 ricaviamo:

| Campo | Contenuto dell’esempio |
|---|---|
| Affermazione | La conferma può arrivare entro 30 secondi dall’invio. |
| Ambito | Richieste standard di Orione, fino al 30 giugno compreso. |
| Fonte | Manuale Orione 2.1. |
| Locatore | §4.3, pagina 48: il punto preciso da riaprire. |

Separare la regola dalle altre permette di ritrovarla e rivederla quando cambia. Togliere «standard» o il periodo produrrebbe invece un’affermazione più ampia di quella sostenuta dalla fonte.

### Complete explanation

Il claim mostrato resta didattico: i locatori reali devono essere misurati sull’artefatto conservato e non inventati. Si rende evidente che la fedeltà riguarda anche condizioni e ambito. Una frase atomica può portare più dati di contesto senza diventare un insieme di affermazioni indipendenti.

### Visual content

Tabella completa. Collegare il campo Locatore al brano di S02, mantenendo visibili durata e condizioni insieme.

### Transition

Una volta estratti molti claim, dove cerchiamo quello sui tempi delle conferme?

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S15
Module: M2
Objective: O2
Role: explanation
Title: Il grafo degli argomenti organizza le domande
Value contribution: La navigazione per argomenti viene spiegata dopo l’unità di conoscenza che deve collocare.

### Learner content

Un **grafo** è un insieme di elementi collegati. Nella KB gli elementi rappresentano argomenti: per esempio «Integrazioni esterne», «Conferme» e «Tempi di attesa».

La domanda «Quanto aspettiamo la conferma?» ci porta all’argomento pertinente e ai claim che gli appartengono. Da lì riapriamo le fonti. Un argomento può essere raggiunto da più percorsi senza duplicare la stessa regola in note divergenti.

Il grafo non prova che 30 secondi sia corretto: **organizza l’accesso all’evidenza**.

Esiste anche un grafo dei prerequisiti di questo corso. Quello stabilisce che capire un claim precede l’uso di una risposta con provenienza. Il grafo della KB ordina gli argomenti; il grafo didattico ordina le spiegazioni.

### Complete explanation

La navigazione per argomenti viene spiegata dopo l’unità di conoscenza che deve collocare. Il lettore vede il motivo per cui conservare soltanto file nominati per data non equivale a organizzare la conoscenza per domanda. La distinzione dal grafo didattico risponde esplicitamente alla Vision senza trasformare il corso in una lezione di teoria dei grafi.

### Visual content

Diagramma «Integrazioni esterne → Conferme → Tempi di attesa → claim → fonte». Separare sotto una piccola catena «capire fonte → capire claim → verificare risposta», etichettata «ordine didattico».

### Transition

Possiamo ora rispondere a una domanda mostrando sia la conclusione sia la strada per controllarla.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S16
Module: M2
Objective: O2
Role: explanation
Title: Una risposta utile porta con sé il suo limite
Value contribution: La conclusione è motivata con un confronto visibile tra data della richiesta e periodo della fonte.

### Learner content

La domanda è: «Per una richiesta standard inviata il 20 giugno, quanto tempo aveva il servizio per confermare?».

Il percorso dalla domanda all’argomento ci porta al claim di S14. Riapriamo il passaggio e rispondiamo:

> «Il Manuale Orione 2.1, §4.3, p.48, indica 30 secondi dall’invio per le richieste standard fino al 30 giugno. Il 20 giugno rientra in quel periodo. Non ho verificato documenti che ne rettifichino la regola».

La risposta esplicita perché il caso rientra nell’ambito. Una citazione senza questo controllo potrebbe sostenere un numero giusto per il caso sbagliato.

Se la domanda riguardasse luglio, questo passaggio non basterebbe a dare la stessa risposta.

### Complete explanation

La conclusione è motivata con un confronto visibile tra data della richiesta e periodo della fonte. Il limite sulle rettifiche non è un disclaimer generico: identifica esattamente ciò che questa consultazione non ha verificato. La fonte viene riaperta e non soltanto ricordata dal testo del claim.

### Visual content

Mostrare «Domanda: 20 giugno» accanto a «Ambito: fino al 30 giugno». Segno di inclusione nel periodo; sotto la risposta completa, inclusa l’ultima frase.

### Transition

Proviamo lo stesso percorso su una regola diversa, con tutti i dati necessari davanti.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S17
Module: M2
Objective: O2
Role: check
Title: Prova: dal documento alla risposta
Value contribution: Il caso trasferisce la procedura su una fonte diversa e distingue due tipi di richiesta.
Solution: S18

### Learner content

Nuovo esempio inventato. Ricevi il Manuale Avvisi 1.2, conservato nel progetto. A pagina 12, §2, leggi:

> «Per le richieste urgenti dal 1 agosto, inviare un avviso dopo 10 secondi senza conferma».

La domanda di una collega è: «Il 5 agosto, per una richiesta urgente senza conferma, quando è previsto l’avviso?».

Descrivi il claim da conservare, l’argomento in cui lo cercheresti e la risposta da dare con il suo riferimento. Poi indica perché lo stesso brano non basta a rispondere sulle richieste standard.

Non devi creare un grafo o un file. Devi rendere visibile come il dato arriva alla risposta senza perdere le condizioni.

### Complete explanation

Il caso trasferisce la procedura su una fonte diversa e distingue due tipi di richiesta. La consegna non richiede capacità ancora non insegnate. Tutti i dati fattuali da usare sono nel brano; l’allievo può dichiarare le rettifiche non verificate, ma non deve inventare una ricerca.

### Visual content

Solo brano e domanda. Non precompilare i campi del claim: questo è il passaggio da svolgere.

### Transition

La soluzione mostra che documento, claim e argomento svolgono funzioni diverse.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S18
Module: M2
Objective: O2
Role: solution
Title: Soluzione: la condizione viaggia con il numero
Value contribution: La risposta soddisfa la richiesta senza espandere ciò che la fonte afferma.

### Learner content

Il claim è: «Per le richieste urgenti dal 1 agosto, l’avviso è previsto dopo 10 secondi senza conferma». La fonte è Manuale Avvisi 1.2, §2, p.12.

Lo collocherei nell’argomento sugli avvisi delle richieste urgenti, cercando prima se quel tema esiste già. Il grafo aiuta a ritrovarlo; il manuale resta l’evidenza.

Risposta: «Per il caso del 5 agosto sono previsti 10 secondi senza conferma, secondo Manuale Avvisi 1.2, §2, p.12. Il brano riguarda le richieste urgenti e non stabilisce il comportamento delle standard».

Se hai scritto solo «10 secondi», aggiungi ambito e provenienza: S14. Se hai trattato la categoria del grafo come prova, rileggi S15–16.

### Complete explanation

La risposta soddisfa la richiesta senza espandere ciò che la fonte afferma. Il richiamo alla ricerca del tema esistente è coerente con il principio di evitare duplicazioni, già reso concreto in S15. La correzione individua il passaggio da riparare e non si limita a dichiarare sbagliata una risposta.

### Visual content

Quattro blocchi in ordine: fonte, claim, argomento, risposta. Il blocco finale ripete le condizioni perché appartengono alla conclusione, non solo all’archivio.

### Transition

Torniamo a Orione: che cosa succede quando arriva un documento con un numero diverso?

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4

## S19
Module: M3
Objective: O3
Role: explanation
Title: 30 e 45 possono essere entrambi corretti
Value contribution: La successione temporale viene insegnata prima del conflitto vero.

### Learner content

Arriva il Bollettino B, §1, con una nuova regola fittizia: «Per le richieste standard dal 1 luglio, la conferma può arrivare entro 45 secondi dall’invio».

Confrontiamolo con il manuale già letto.

| Fonte | Tipo di richiesta | Periodo | Tempo |
|---|---|---|---|
| Manuale 2.1 §4.3 p.48 | Standard | Fino al 30 giugno compreso | 30 secondi |
| Bollettino B §1 | Standard | Dal 1 luglio | 45 secondi |

I periodi non si sovrappongono. Le due affermazioni possono coesistere: una spiega giugno, l’altra luglio.

Prima di dichiarare un conflitto, confrontiamo **soggetto, condizioni e periodo**. Il semplice fatto che due documenti contengano numeri diversi non basta.

### Complete explanation

La successione temporale viene insegnata prima del conflitto vero. Il lettore può quindi distinguere la nuova domanda dalla ragione storica recuperata in S02. Non si riscrive il passato dicendo che i 30 secondi fossero sempre sbagliati. Nel caso fittizio i periodi sono espliciti e non sovrapposti.

### Visual content

Linea del tempo divisa fra 30 giugno e 1 luglio; sopra 30 s, sotto 45 s nei rispettivi intervalli. Affiancare tabella per conservare tipo e fonte.

### Transition

Ora arriva una nota che parla proprio dello stesso periodo: qui il confronto cambia.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S20
Module: M3
Objective: O3
Role: explanation
Title: Il conflitto resta visibile finché manca una ragione per risolverlo
Value contribution: L’ambito viene mantenuto identico per rendere la contraddizione effettiva e non solo apparente.

### Learner content

La Nota C, §2, dichiara: «Per le richieste standard dal 1 luglio, la conferma può arrivare entro 30 secondi dall’invio».

B dice 45 e C dice 30 per lo stesso tipo di richiesta, periodo e istante iniziale. Questa volta le affermazioni sono incompatibili.

kb-agentic deve conservarle entrambe come **contestate**, con le rispettive fonti. «Contestata» significa che non possiamo usarla come regola risolta ignorando l’altra.

La risposta onesta è: «B e C non concordano; manca un chiarimento». La data di arrivo del file, la preferenza dell’agente o una maggioranza di copie non stabiliscono quale sia corretto.

Serve informazione nuova: per esempio una rettifica che chiarisca a quali richieste si riferisce C.

### Complete explanation

L’ambito viene mantenuto identico per rendere la contraddizione effettiva e non solo apparente. Le due righe restano entrambe contestate, evitando una selezione silenziosa. La nuova informazione richiesta è concreta; il corso non suggerisce una domanda vaga quando un confronto delle fonti potrebbe già risolvere il caso.

### Visual content

Due riquadri B45 e C30 collegati da «stesso ambito, valori incompatibili». Entrambi riportano «contestato». Nessun colore che faccia scegliere un vincitore.

### Transition

Vediamo quale informazione sarebbe sufficiente a cambiare questa conclusione.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S21
Module: M3
Objective: O3
Role: explanation
Title: Una rettifica cambia l’evidenza, non soltanto la data
Value contribution: La rettifica fittizia nomina esattamente il testo corretto, il nuovo ambito e la regola corrente.

### Learner content

Arriva la Rettifica D, §1, che dichiara esplicitamente:

> «La Nota C §2 contiene un errore nel tipo di richiesta: “standard” va sostituito con “urgente”. Dal 1 luglio restano 45 secondi per le standard e 30 per le urgenti».

Ora sappiamo perché B e C sembravano contraddirsi. La nuova informazione modifica l’ambito di C; non elegge un documento perché arrivato dopo.

La KB conserva il vecchio claim di C come **superato**, collegandolo alla correzione. «Superato» significa che la storia resta leggibile, ma la risposta corrente deve seguire il successore pertinente.

Anche una persona può portare un fatto mancante, registrandone la base. «Preferisco 45» da solo non è un fatto che risolve il conflitto.

### Complete explanation

La rettifica fittizia nomina esattamente il testo corretto, il nuovo ambito e la regola corrente. È questa relazione a sostenere il riesame. L’esempio distingue una correzione documentale da una scelta prudenziale di prodotto, che può essere discussa ma non trasforma una preferenza in verità della fonte.

### Visual content

Prima: B standard 45 e C standard 30 contestati. Dopo: standard 45 e urgenti 30 con riferimento a D; C originale resta in un riquadro «storico, superato».

### Transition

Chiarire il fatto nella KB non modifica ancora ciò che il software mostra.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S22
Module: M3
Objective: O3
Role: explanation
Title: La conoscenza cambia prima del codice
Value contribution: La relazione fonte→decisione→comportamento viene resa concreta con 35 secondi, scelti perché interni alla nuova finestra ma oltre il vecchio limite.

### Learner content

Per le richieste standard di luglio, la fonte chiarita indica 45 secondi. Orione, però, usa ancora 30 per dichiarare la scadenza.

Se dopo 35 secondi non è arrivata conferma, il software mostra già «scaduta», mentre la finestra del servizio può essere ancora aperta.

La vecchia decisione sui 30 va riesaminata per l’uso a luglio. Il suo collegamento alla fonte ci aiuta a trovarla; altri documenti che la usano possono richiedere la stessa revisione.

I controlli della KB possono segnalare riferimenti a conoscenza superata. **Non aggiornano automaticamente codice e schermate.** Tocca al lavoro sul software stabilire cosa cambiare e dimostrare che il risultato sia coerente.

### Complete explanation

La relazione fonte→decisione→comportamento viene resa concreta con 35 secondi, scelti perché interni alla nuova finestra ma oltre il vecchio limite. Il manuale storico resta valido per giugno; è il suo uso corrente senza ambito che diventa scorretto. Il lettore deve distinguere segnalazione di dipendenze e correzione eseguita.

### Visual content

Linea 0–45 con marker 30 e 35. A 35 due etichette: «Software: scaduta» e «Finestra standard di luglio: ancora aperta». Non mostrare esito completato senza conferma.

### Transition

Prima di passare al software, controlliamo di saper riconoscere un conflitto su dati nuovi.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S23
Module: M3
Objective: O3
Role: check
Title: Prova: differenza o contraddizione?
Value contribution: Il compito cambia numeri e mese e introduce un ambito incompleto.
Solution: S24

### Learner content

Tre documenti inventati descrivono il tempo di risposta:

- A: «20 secondi per richieste standard fino al 31 agosto compreso».
- B: «25 secondi per richieste standard dal 1 settembre».
- C: «20 secondi dal 1 settembre», senza indicare il tipo di richiesta.

Quali conclusioni puoi sostenere sulle coppie A–B e B–C? Quale dato cercheresti prima di scegliere una regola per una richiesta standard di settembre?

Supponi poi che un nuovo documento chiarisca che C riguarda le urgenti. Che cosa cambierebbe e che cosa conserveresti della lettura precedente?

Rispondi prima della soluzione: il documento arrivato per ultimo non ha un privilegio automatico.

### Complete explanation

Il compito cambia numeri e mese e introduce un ambito incompleto. Consente di distinguere una contraddizione dimostrata da un possibile conflitto ancora da circoscrivere. La domanda finale chiede la revisione della conclusione alla luce di un fatto nuovo, non una scelta per maggioranza.

### Visual content

Testo dei tre documenti su tre righe; nessuna classificazione o evidenziazione di vincitori.

### Transition

La qualità della risposta dipende da ciò che sai e da ciò che riconosci di non sapere.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S24
Module: M3
Objective: O3
Role: solution
Title: Soluzione: prima confrontare gli ambiti
Value contribution: La soluzione non dichiara che B sia falso né risolve in anticipo l’ambiguità di C.

### Learner content

**A e B possono coesistere:** i periodi non si sovrappongono. A non confuta la regola di settembre.

**B e C richiedono un controllo:** il periodo coincide, ma manca il tipo di richiesta di C. Se C riguardasse le standard nelle stesse condizioni, i valori sarebbero in conflitto e andrebbero mantenuti contestati.

Se il nuovo documento dimostra che C riguarda le urgenti, possiamo distinguere 25 secondi per le standard e 20 per le urgenti. Conserviamo la fonte del chiarimento e il collegamento alla lettura che ha corretto.

Se hai scelto subito il file più recente, torna a S20–21. Se hai dichiarato A e B incompatibili, confronta i periodi come in S19.

### Complete explanation

La soluzione non dichiara che B sia falso né risolve in anticipo l’ambiguità di C. Esplicita la condizione che trasformerebbe il dubbio in conflitto. La correzione conserva provenienza e storia, insegnando che aggiornare la conoscenza non significa cancellare l’evidenza precedente.

### Visual content

Tabella coppia/esito/motivo: A–B «coesistenza, periodi separati»; B–C «ambito incompleto»; B–C chiarito «tipi diversi».

### Transition

A Orione abbiamo chiarito la regola di luglio. Ora possiamo chiedere quale risultato vogliamo ottenere cambiando il software.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5

## S25
Module: M4
Objective: O4
Role: explanation
Title: Il risultato da ottenere viene prima della costante
Value contribution: Il pannello viene definito quando diventa rilevante.

### Learner content

L’operatrice di Orione guarda un **pannello**, cioè la schermata che mostra lo stato delle richieste. Il problema è concreto: a 35 secondi una richiesta standard di luglio appare scaduta troppo presto.

Il responsabile concorda questo risultato:

> «L’operatrice deve vedere uno stato attendibile durante l’attesa della conferma. Correggiamo le scadenze premature delle richieste standard di luglio; non ridisegniamo la navigazione dell’applicazione».

Questo è un esempio di **Vision**: dichiara chi deve ottenere quale beneficio e quali confini rispettare. La Vision approvata guida il lavoro.

Cambiare 30 in 45 è una possibile parte della soluzione. Il successo è che l’operatrice riceva l’informazione corretta, senza danneggiare gli altri casi.

### Complete explanation

Il pannello viene definito quando diventa rilevante. La Vision non è una frase motivazionale: consente di giudicare sia la soluzione sia un ampliamento del lavoro. Il fatto documentale sulla durata non sostituisce la decisione della persona sul risultato da perseguire. Il beneficio è osservabile nel comportamento, non nel diff.

### Visual content

Due riquadri: «Mezzo possibile: modificare un calcolo» e «Beneficio: stato attendibile per l’operatrice». Sotto, il confine sui menu esattamente come nella citazione.

### Transition

Quanto lavoro serve per ottenere quel risultato in modo affidabile? Dipende dagli effetti della modifica.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-7

## S26
Module: M4
Objective: O4
Role: explanation
Title: Il triage proporziona il lavoro al rischio
Value contribution: La tabella insegna il criterio e rinvia ai limiti specifici della skill invece di inventare soglie universali.

### Learner content

Il **triage** classifica l’intervento prima di scegliere il percorso di lavoro. In agentic-sdlc i livelli sono:

| Livello | Caso tipico | Percorso |
|---|---|---|
| L1 | Refuso isolato, senza cambiamenti di comportamento o contratti | Correggere e controllare. |
| L2 | Causa chiara, intervento locale a rischio basso, entro i limiti della skill | Breve analisi, modifica e test. |
| L3 | Comportamento visibile, contratti, rischi sensibili o design significativo | Vision, analisi, piano, review, realizzazione, verifiche e chiusura. |
| Spike | Manca conoscenza per decidere | Indagine circoscritta; poi riclassificare la produzione. |

Il cambiamento di Orione è L3: modifica quando una richiesta viene mostrata come scaduta. Una sola riga può alterare un comportamento importante; la dimensione del codice non misura da sola il rischio.

### Complete explanation

La tabella insegna il criterio e rinvia ai limiti specifici della skill invece di inventare soglie universali. L2 non è un modo per chiamare piccolo un cambiamento incerto; Spike non autorizza la produzione prima di risolvere il dubbio che la governa. Il corso si concentra sull’esempio L3 già giustificato.

### Visual content

Tabella leggibile con quattro righe. Evidenziare la motivazione di Orione, non solo il simbolo L3.

### Transition

Due ticket con lo stesso titolo possono quindi richiedere percorsi diversi.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6

## S27
Module: M4
Objective: O4
Role: check
Title: Prova: due correzioni, due effetti
Value contribution: La prova varia l’effetto mantenendo simile il nome del lavoro.
Solution: S28

### Learner content

Due ticket si chiamano «Correggere la scadenza».

**A.** L’indagine conferma che la schermata mostra «scadutaa». Si corregge soltanto la parola: nessuna logica, interfaccia pubblica o area sensibile cambia.

**B.** La schermata dichiara scaduta una richiesta standard di luglio dopo 30 secondi. La Rettifica D chiarisce la finestra di 45, ma non precisa il trattamento di una conferma arrivata esattamente al limite.

Un collega propone di aggiungere a B un nuovo menu di navigazione.

Quale livello assegneresti a ciascun ticket e perché? Quale decisione manca in B? Il menu serve al beneficio approvato? Se la fonte fosse ancora contestata, che cosa faresti prima di progettare la nuova regola?

### Complete explanation

La prova varia l’effetto mantenendo simile il nome del lavoro. Il caso al confine è dichiarato incompleto, così l’allievo deve riconoscere la decisione mancante invece di riempirla con una consuetudine tecnica. Il menu verifica la capacità di usare il non-obiettivo della Vision.

### Visual content

Due schede A/B, seguite da tre domande. Non riportare anticipatamente livelli o risposte.

### Transition

La soluzione lega ogni scelta a un fatto del caso, non al titolo del ticket.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-7

## S28
Module: M4
Objective: O4
Role: solution
Title: Soluzione: classificare l’effetto, dichiarare il dubbio
Value contribution: La soluzione non vieta ogni lavoro finché esiste un dubbio: si può investigare e progettare ciò che non dipende dall’esito.

### Learner content

**A è L1:** l’indagine ha circoscritto il lavoro a un refuso. Correzione e controllo pertinente sono proporzionati.

**B è L3:** cambia un comportamento visibile. Prima di implementare il caso esatto dei 45 secondi, dobbiamo chiarirne la regola con la fonte competente o con chi ha autorità sul comportamento del prodotto, distinguendo le due basi.

Il menu è fuori dal beneficio e dal confine approvati: richiederebbe una proposta distinta. La comodità di modificarlo insieme non lo rende necessario.

Se la durata fosse ancora contestata, un’indagine circoscritta dovrebbe chiarire il fatto. Non chiameremmo 45 «regola verificata» solo per avanzare.

Se hai contato le righe, torna a S26. Se hai lasciato decidere tutto al manuale, separa fatto e obiettivo come in S25.

### Complete explanation

La soluzione non vieta ogni lavoro finché esiste un dubbio: si può investigare e progettare ciò che non dipende dall’esito. Impedisce però di trasformare un’ipotesi in requisito accertato. Il livello L3 resta motivato dall’effetto anche se la patch è piccola.

### Visual content

Tabella A/L1/motivo e B/L3/motivo. Riquadro separato «Decisione aperta: limite esatto».

### Transition

Definito il risultato, esaminiamo chi usa la modifica, quali comportamenti servono e dove possono fallire.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-7

## S29
Module: M5
Objective: O5
Role: explanation
Title: Il bisogno fa emergere chi potremmo dimenticare
Value contribution: La notifica viene introdotta qui come una nuova informazione esplicita del caso, non presupposta nell’apertura.

### Learner content

Guardiamo meglio Orione. L’operatrice consulta il pannello; l’assistenza riceve un’email quando una richiesta scade. Il servizio esterno invia la conferma a Orione: questa risposta asincrona viene chiamata **callback**.

Un **use case**, o caso d’uso, descrive un attore e il risultato che gli serve:

- L’operatrice vuole distinguere una richiesta ancora in attesa da una scaduta.
- L’assistenza vuole evitare di intervenire su una richiesta che può ancora completarsi.

Cambiare la costante non descrive nessuno dei due bisogni. Se sistemiamo il pannello ma l’email parte ancora a 30 secondi, uno degli attori riceve un messaggio sbagliato.

Lo sviluppatore cerca i percorsi interessati; il responsabile verifica che il risultato copra le persone coinvolte.

### Complete explanation

La notifica viene introdotta qui come una nuova informazione esplicita del caso, non presupposta nell’apertura. La definizione di callback precede il suo uso nei test. Il bisogno allarga la ricerca in modo motivato dal beneficio, senza autorizzare nuove funzionalità arbitrarie. Attori, comportamento, interfacce e rischi saranno presentati in ordine per chiarezza; nel lavoro reale l’indagine può intrecciarli.

### Visual content

Due persone nominate con la loro superficie: «Operatrice/pannello», «Assistenza/email». Terzo attore «Servizio esterno/callback». Tutti si riferiscono alla stessa richiesta.

### Transition

Per soddisfare questi bisogni dobbiamo descrivere che cosa deve accadere nei casi concreti.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8

## S30
Module: M5
Objective: O5
Role: explanation
Title: La specifica rende il comportamento discutibile prima del codice
Value contribution: La tabella separa una proposta di comportamento del prodotto dalla durata indicata dalla fonte.

### Learner content

La **specifica funzionale** descrive il comportamento voluto, senza scegliere ancora componenti e file.

Per le richieste standard di luglio proponiamo:

| Situazione | Comportamento atteso |
|---|---|
| A 35 secondi, nessuna conferma | La richiesta resta in attesa; nessuna email di scadenza. |
| Conferma valida prima del limite | La richiesta diventa completata; niente email di scadenza. |
| Dopo 45 secondi, nessuna conferma | La richiesta è scaduta e l’assistenza riceve l’avviso. |
| Conferma esattamente al limite | Decisione ancora da chiarire. |

La rettifica distingue inoltre le richieste urgenti, che restano a 30 secondi. Cambiare tutte le richieste a 45 sarebbe un’estensione errata.

Scrivere questi casi permette alla persona di approvare un comportamento, anziché soltanto un elenco di file.

### Complete explanation

La tabella separa una proposta di comportamento del prodotto dalla durata indicata dalla fonte. Il caso al confine resta aperto fino a una decisione esplicita. La permanenza delle urgenti a 30 crea una regressione concreta da evitare. L’indagine su bisogni, regole, superfici e rischi può iterare: la sequenza delle slide è un ordine di spiegazione, non un obbligo di pensare in compartimenti.

### Visual content

Tabella con riga del confine contrassegnata «aperta». Nota visibile sotto: «Urgenti:30 s; non estendere la nuova durata».

### Transition

Ora seguiamo come lo stesso comportamento arriva alle persone e al servizio esterno.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8

## S31
Module: M5
Objective: O5
Role: explanation
Title: Il contratto di interazione segue il viaggio della richiesta
Value contribution: Il contratto comprende il flusso a livello di responsabilità, non solo una lista di schermate.

### Learner content

Una **superficie di interazione** è un punto in cui una persona o un servizio agisce o riceve una risposta: pannello, email, ingresso del callback.

Il **contratto di interfaccia** descrive quel percorso: evento iniziale, responsabilità attraversate, stati e feedback ricevuti.

Nel caso Orione, l’invio crea una richiesta; il servizio che ne gestisce lo stato la mantiene in attesa. Il pannello legge lo stato. Il gestore delle notifiche lo usa per decidere se inviare un’email. Il callback può cambiare lo stato in completata.

Se il pannello non riesce a caricare un aggiornamento, deve mostrare che il dato non è disponibile, senza presentare un vecchio stato come appena verificato. Il comportamento proposto va concordato; un errore di lettura non prova una scadenza.

### Complete explanation

Il contratto comprende il flusso a livello di responsabilità, non solo una lista di schermate. Le responsabilità nominate sono un modello didattico del caso, non componenti dichiarati esistenti in un repository reale. La proposta di errore rende osservabile un limite che altrimenti il renderer o il programmatore dovrebbe inventare.

### Visual content

Flusso «Invio → gestione stato → pannello» e ramo verso «gestore notifiche → email». Il callback entra nella gestione stato. Annotare l’errore di lettura sul pannello separatamente dallo stato scaduta.

### Transition

Seguire i percorsi rivela dove un risultato apparentemente corretto potrebbe ancora danneggiare qualcuno.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8

## S32
Module: M5
Objective: O5
Role: explanation
Title: Un rischio utile indica che cosa osservare
Value contribution: I rischi provengono dalle superfici già introdotte e dai confini della regola.

### Learner content

Il **modello dei rischi**, o Threat Model, esamina che cosa può andare storto e quale controllo potrebbe rilevarlo.

| Rischio concreto | Conseguenza | Verifica da progettare |
|---|---|---|
| L’email usa ancora 30 secondi | L’assistenza interviene troppo presto | Osservare pannello ed email sulla stessa richiesta a 35 secondi. |
| Il pannello mostra un dato vecchio come attuale | L’operatrice si fida di uno stato non verificato | Simulare aggiornamento fallito e controllare il feedback concordato. |
| La nuova durata è applicata anche alle urgenti | Si attende oltre la loro regola | Provare una richiesta urgente con il limite di 30. |

«Potrebbero esserci problemi» non orienta il lavoro. Un rischio localizzato collega un effetto indesiderato a una prova. Le prove elencate sono da eseguire: qui non stiamo testando software reale.

### Complete explanation

I rischi provengono dalle superfici già introdotte e dai confini della regola. Non si aggiungono minacce estranee solo per riempire una tabella. La proposta di verifica osserva l’effetto rilevante, non soltanto una funzione chiamata o una costante modificata. Gli eventuali aspetti di sicurezza del sistema reale richiederebbero l’indagine concreta non svolta dal corso.

### Visual content

Tabella esatta con collegamenti dalla superficie al controllo. Nessun badge «test superato».

### Transition

Prima di decidere dove intervenire, dobbiamo cercare se il sistema possiede già il calcolo e i percorsi che ci servono.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9

## S33
Module: M5
Objective: O5
Role: explanation
Title: Prima di costruire, cerchiamo ciò che esiste
Value contribution: La slide mostra evidenza e conseguenza insieme: il registro non serve a elencare file già scelti, ma a giustificare la scelta.

### Learner content

Il **Capability Ledger** è il registro delle capacità necessarie, delle evidenze trovate e delle conseguenze per la soluzione.

Completiamo un’indagine inventata su Orione:

| Capacità cercata | Riscontro del caso | Conseguenza |
|---|---|---|
| Calcolare la scadenza | Il componente `ExpiryPolicy` è usato dal pannello. | Esiste un punto da valutare per il riuso. |
| Inviare avvisi coerenti | Il gestore email confronta il tempo con 30 in una regola separata. | Cambiare solo `ExpiryPolicy` lascia un errore. |
| Distinguere i tipi di richiesta | Il tipo è disponibile nei dati letti da entrambi i percorsi. | Il design può preservare la regola delle urgenti. |

Nel lavoro reale servono file, simboli e chiamate effettivamente esaminati. «Non l’ho trovato nell’area letta» non significa «non esiste nel progetto».

### Complete explanation

La slide mostra evidenza e conseguenza insieme: il registro non serve a elencare file già scelti, ma a giustificare la scelta. I nomi sono inventati e non fungono da prova su un repository. Esistenza di un calcolo non implica adeguatezza: la sua capacità di usare tipo e periodo andrà valutata nel design.

### Visual content

Tre colonne come nel testo. Evidenziare la divergenza tra pannello ed email con il valore 30 solo nella riga pertinente.

### Transition

Ora possiamo scegliere una soluzione sulla base dell’indagine, evitando un secondo calcolo aggiunto senza motivo.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9

## S34
Module: M5
Objective: O5
Role: explanation
Title: L’impatto collega la scelta alle parti da cambiare
Value contribution: La decisione sul confine chiude il dubbio prima di implementare e rende possibili prove con attese definite.

### Learner content

L’**Impact**, o mappa dell’impatto, indica quali parti cambiano e perché. Il **design** spiega come collaboreranno per ottenere il risultato.

Nel caso scegliamo di adeguare `ExpiryPolicy` a tipo e periodo della richiesta e di far usare la stessa regola al gestore email. Il pannello già la consulta. Occorre verificare entrambe le superfici e preservare le urgenti a 30 secondi.

Risolviamo anche la decisione aperta: **nel nostro esempio il responsabile conferma** che una conferma registrata entro 45 secondi, incluso il limite, completa la richiesta; la scadenza standard di luglio scatta oltre 45 senza conferma. Questa è una decisione di prodotto esplicita, non una frase attribuita al manuale.

Se non avessimo trovato un calcolo riusabile, dovremmo motivare una capacità nuova dopo la ricerca, anziché dichiarare un riuso inesistente.

### Complete explanation

La decisione sul confine chiude il dubbio prima di implementare e rende possibili prove con attese definite. In un sistema reale andrebbero precisati anche clock, ordinamento degli eventi e requisiti del fornitore: il caso didattico usa il tempo di registrazione e non pretende di risolvere un protocollo distribuito. L’Impact comprende aggiornamento del calcolo, suo consumatore email e verifiche dei comportamenti.

### Visual content

Mappa «ExpiryPolicy: tipo+periodo» verso pannello ed email. Sotto due righe: «conferma registrata≤45: completata»; «oltre 45 senza conferma: scaduta». Etichetta «decisione di prodotto nel caso inventato».

### Transition

Prima di tradurre questa scelta in codice, un’altra lettura deve cercare le omissioni del design.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9

## S35
Module: M5
Objective: O5
Role: explanation
Title: La review del design cerca ciò che l’autore ha trascurato
Value contribution: La review è introdotta nel punto causale corretto: prima di rendere costosa l’omissione nel codice.

### Learner content

Una **review** è un riesame. Per una modifica L3, quella del design precede l’implementazione.

Un revisore indipendente riceve Vision, bisogni, regole, rischi e soluzione proposta. Controlla, per esempio, notifica, urgenti e confine temporale di Orione.

**Indipendente** significa distinto dall’autore: per esempio un agente in una sessione nuova. Rileggersi da soli non soddisfa questa condizione.

Se l’unica modalità indipendente praticabile richiede un’autorizzazione, con la persona raggiungibile si chiede quell’autorizzazione prima di procedere: il silenzio non permette di ripiegare sull’autore.

Quando nessuna modalità indipendente è utilizzabile, il protocollo prevede un’autorevisione dichiarata, con ragione e limite. Questo ripiego non si sceglie per comodità e non si presenta come review indipendente.

### Complete explanation

La review è introdotta nel punto causale corretto: prima di rendere costosa l’omissione nel codice. Il reviewer valuta, mentre il responsabile conserva le decisioni di ambito e approvazione previste. L’indipendenza non è una garanzia di trovare ogni errore e il PASS non certifica un risultato ancora non realizzato.

### Visual content

Linea temporale con marcatore presente: «Design → review del design → implementazione». Accanto, due persone/contesti distinti «autore» e «revisore».

### Transition

Dopo il riesame del design, realizziamo il cambiamento e cerchiamo prove che osservino proprio i casi concordati.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9

## S36
Module: M5
Objective: O5
Role: explanation
Title: I test devono osservare ciò che ricevono le persone
Value contribution: La prova tecnica è scelta per discriminare la vecchia implementazione difettosa dalla nuova.

### Learner content

Lo sviluppatore implementa il design e raccoglie risultati di prove pertinenti. Nel nostro esempio progetterebbe almeno questi casi:

| Caso | Risultato da osservare |
|---|---|
| Standard di luglio, 35 secondi senza conferma | Pannello in attesa; nessuna email di scadenza. |
| Conferma registrata esattamente a 45 | Completata; nessuna email, secondo la decisione di S34. |
| Oltre 45, nessuna conferma | Scaduta; email coerente con lo stesso stato. |
| Urgente di luglio oltre 30, senza conferma | La precedente durata resta applicata. |

Servono anche i casi di errore e di stato non aggiornato individuati in S31–32, e controlli sulle regressioni pertinenti.

Un test verde sulla costante 45 non osserva questi percorsi. Qui abbiamo **progettato le prove**; nessun test su Orione reale è stato eseguito.

### Complete explanation

La prova tecnica è scelta per discriminare la vecchia implementazione difettosa dalla nuova. A 35 secondi la vecchia soglia sarebbe osservabile; al confine si verifica una regola confermata e non inventata nel test. I risultati devono essere raccolti dopo la modifica e riportati nel loro ambito, senza scambiare una lista di casi per esecuzione.

### Visual content

Tabella di test con intestazione «Da eseguire». Mantenere visibili insieme stato del pannello ed esito email. Nessun segno di spunta verde.

### Transition

Anche con prove superate, prima di chiudere dobbiamo confrontare il risultato completo con ciò che era stato deciso.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9

## S37
Module: M5
Objective: O5
Role: explanation
Title: La chiusura lascia un risultato e un punto da cui ripartire
Value contribution: Si distingue risultato consegnato dalla conoscenza che permette a un altro agente di riprendere.

### Learner content

La **review finale**, svolta anch’essa da un revisore distinto dall’autore, confronta modifica, comportamento concordato e risultati dei test. Cerca omissioni e regressioni rimaste. Il responsabile valuta se le evidenze sostengono il beneficio; un’autodichiarazione dell’agente non basta.

La chiusura aggiorna stato del lavoro, decisioni, verifiche e limiti ancora aperti nel progetto.

Se l’indagine ha prodotto conoscenza riusabile, una **GUIDE** può conservarla con fonti: per esempio dove nasce lo stato di una richiesta, come cercarne i consumatori e quali casi rivelano divergenze. Una GUIDE è una guida operativa consultabile nei lavori successivi, collegata alle evidenze da cui deriva.

«Ricordati delle email» è un promemoria; non spiega come trovare un consumatore dimenticato. Non ogni modifica richiede una nuova GUIDE: servono uno scopo riusabile, provenienza e il percorso previsto dalla skill.

### Complete explanation

Si distingue risultato consegnato dalla conoscenza che permette a un altro agente di riprendere. Una guida non sostituisce codice, test o fonte; conserva un modello operativo controllabile e deve essere mantenuta. La famiglia distingue guide da indicazioni e guide dal codice con diversi trigger: il corso non autorizza a crearne una per ogni ticket né sostituisce quelle regole.

### Visual content

Tre blocchi: «Review finale: risultato contro design», «Chiusura: stato e limiti», «GUIDE quando giustificata: come ripetere l’indagine + fonti».

### Transition

Mettiamo insieme questi passaggi davanti a una proposta di chiusura troppo rapida.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S38
Module: M5
Objective: O5
Role: check
Title: Prova: «Il test è verde, possiamo chiudere»
Value contribution: Il check riduce il supporto e chiede una sequenza motivata.
Solution: S39

### Learner content

In un nuovo tentativo su Orione, un agente dichiara: «Ho cambiato 30 in 45 e il test della costante passa». Non fornisce evidenze sulla notifica, sulle richieste urgenti, sul caso al confine o su una review del design.

Il beneficio resta evitare scadenze premature delle standard di luglio. Non assumere che l’indagine delle slide precedenti sia stata eseguita da questo agente.

Come risponderesti? Indica:

- quali fatti e decisioni mancano;
- quale ricerca sul sistema serve prima di scegliere la soluzione;
- quali passi e prove giustificherebbero la chiusura;
- chi dovrebbe svolgere le review e quando avrebbe senso conservare una GUIDE.

Motiva i passaggi con il caso. Un elenco di nomi di documenti non dimostra che la modifica sia stata compresa.

### Complete explanation

Il check riduce il supporto e chiede una sequenza motivata. Esplicitare che i riscontri precedenti non sono trasferibili impedisce all’allievo di trattare una capacità illustrata in un caso come prova su un tentativo nuovo. Le omissioni verificano design, evidenza tecnica e indipendenza separatamente.

### Visual content

Solo dichiarazione iniziale e consegna. Non mostrare una checklist già ordinata che suggerisca la soluzione.

### Transition

La risposta deve separare il lavoro effettivamente dimostrato da quello ancora necessario.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S39
Module: M5
Objective: O5
Role: solution
Title: Soluzione: ricostruire le evidenze mancanti
Value contribution: La sequenza non retrodata azioni mancanti e permette di recuperare una modifica già iniziata.

### Learner content

Non chiuderei dal solo test della costante.

1. Chiarirei regola applicabile, comportamento al confine e casi da preservare. Il beneficio riguarda le standard di luglio; le urgenti non devono cambiare implicitamente.
2. Cercherei il calcolo esistente e chi lo usa: pannello ed email potrebbero divergere. Da quelle evidenze derivano Impact e design.
3. Farei svolgere la review del design a un revisore distinto dall’autore. Se il codice è già stato scritto, lo rivaluterei rispetto al design chiarito ora, senza inventare una review precedente.
4. Verificherei le superfici a 35 secondi, al confine concordato, dopo la scadenza e in errore; includerei le urgenti. Poi un revisore distinto dall’autore confronterebbe risultato ed evidenze con il design nella review finale.
5. Aggiornerei stato e limiti. Una GUIDE avrebbe senso se l’indagine producesse un percorso riusabile, sostenuto da fonti.

«L’autore si è ricontrollato» non prova indipendenza: S35. «45 è nel codice» non prova il beneficio: S36.

### Complete explanation

La sequenza non retrodata azioni mancanti e permette di recuperare una modifica già iniziata. Una soluzione sufficiente collega ogni fase a una specifica omissione, include il caso non da cambiare e distingue review iniziale e finale. Le prove sono richieste, non dichiarate eseguite. La nota sulla guida evita documentazione aggiuntiva senza funzione.

### Visual content

Cinque passi numerati, con massimo una frase guida per passo in un eventuale indice laterale. Il testo completo resta visibile; non spostare le motivazioni nelle note.

### Transition

Ora possiamo vedere il percorso completo: una risposta della KB diventa un input controllabile del lavoro sul software.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10

## S40
Module: M6
Objective: O6
Role: explanation
Title: Il passaggio fra le due skill conserva la responsabilità
Value contribution: Il passaggio viene mostrato solo quando tutte le parti sono state insegnate.

### Learner content

La domanda iniziale di Orione ha attraversato tre responsabilità:

| Responsabilità | Risultato da passare al lavoro seguente |
|---|---|
| kb-agentic: fedeltà alle fonti | Per le standard da luglio la finestra è 45 secondi; Bollettino B §1 e Rettifica D §1 chiariscono il contrasto con C. |
| Persona responsabile: risultato e decisioni | Evitare scadenze premature; preservare le urgenti; concordare il confine esatto. |
| agentic-sdlc: cambiamento software | Design, modifica, prove e review che collegano quella regola a pannello ed email. |

L’analisi del cambiamento cita la conoscenza della KB. Non crea una seconda autorità sulla durata e non scambia la rettifica per una prova dei test.

Se una fonte cambia ancora, il collegamento aiuta a trovare il lavoro da riesaminare.

### Complete explanation

Il passaggio viene mostrato solo quando tutte le parti sono state insegnate. Una decisione umana riguarda beneficio, ambito e scelte aperte, mentre la fonte sostiene il fatto documentale. La responsabilità della fonte non viene trasferita implicitamente all’analisi software e il completamento software non chiude automaticamente ogni questione di conoscenza.

### Visual content

Tabella come nel testo. Collegamenti fra righe etichettati «cita l’evidenza» e «realizza il risultato», mai «approva automaticamente».

### Transition

Dove vive questa analisi quando il progetto dispone soltanto della sua cartella?

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S41
Module: M6
Objective: O6
Role: explanation
Title: Standalone è già un percorso completo
Value contribution: La distinzione di modalità arriva dopo le funzioni dei documenti.

### Learner content

**Standalone** significa svolgere il processo nei file del progetto, senza un servizio di governance aggiuntivo. L’**ANALYSIS** è il documento dell’analisi: raccoglie bisogni, regole, interazioni, rischi, capacità, impatto e piano. Fonti, decisioni e guide restano consultabili nella cartella.

**devPNT** è un’integrazione opzionale. Quando configurato per il progetto, aggiunge documenti governati e proposte versionate con approvazione umana. Per orientarsi: D-UC tratta i bisogni, D-IC le interfacce, P-TM i rischi; E-ISP raccoglie analisi della soluzione e impatto, E-TDD dettaglia il design.

Non occorre ricordare le sigle per capire la differenza: in modalità integrata bisogna rispettare l’autorità dei documenti governati. Un file locale non rende approvata una proposta, e l’agente non può auto-accettarla.

### Complete explanation

La distinzione di modalità arriva dopo le funzioni dei documenti. Standalone è completo, non un ripiego privo di analisi o review. In Hybrid Functional Spec e Capability Ledger appartengono all’E-ISP, sopra l’Impact; non si inventa una seconda versione autorevole locale. Le guide operative mantengono la loro sede nei file secondo la matrice di ownership della fonte.

### Visual content

Due colonne: Standalone «ANALYSIS nei file»; con devPNT «artefatti governati e proposte». Riga comune «stesso bisogno di fonte, design, prove e review».

### Transition

Una fonte corretta basta allora per delegare alla KB anche la scelta del prodotto e la chiusura del ticket?

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S42
Module: M6
Objective: O6
Role: check
Title: Prova: il manuale può chiudere il ticket?
Value contribution: Il caso cambia dominio dal tempo di attesa a una ricevuta, ma conserva le tre responsabilità insegnate.
Solution: S43

### Learner content

Nuovo esempio inventato: il Manuale Ricevute 3.0, §5, p.22, richiede che una ricevuta mostri la data della richiesta. Il software oggi mostra solo la data di stampa. La persona responsabile vuole eliminare questa ambiguità per l’operatore; la disposizione esatta delle due date non è ancora concordata.

Un collega propone: «La KB ha trovato la frase, quindi può scegliere il layout, cambiare il software e dichiarare chiuso». devPNT non è configurato; cartella e strumenti di sviluppo sono disponibili.

Come ripartiresti le responsabilità? Quale risultato della KB useresti, quale decisione manca, dove conserveresti il design e che cosa dovrebbe essere verificato prima di chiudere?

Tenta la risposta prima di leggere la soluzione.

### Complete explanation

Il caso cambia dominio dal tempo di attesa a una ricevuta, ma conserva le tre responsabilità insegnate. Il requisito documentale non determina da solo disposizione e leggibilità. La prova distingue l’assenza di devPNT dall’assenza di un percorso di lavoro.

### Visual content

Mostrare la frase del manuale e il comportamento attuale in due riquadri; non disegnare già il layout futuro.

### Transition

Una risposta sufficiente tiene insieme fonte, scelta di prodotto e verifica senza confonderle.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S43
Module: M6
Objective: O6
Role: solution
Title: Soluzione: fatto, scelta e prova restano distinti
Value contribution: La soluzione applica il metodo a un caso nuovo senza costringere a ricordare sigle.

### Learner content

kb-agentic conserva la frase con versione, ambito e locatore: Manuale Ricevute 3.0, §5, p.22. Questo sostiene la presenza richiesta della data della richiesta.

La persona responsabile chiarisce il comportamento utile all’operatore: come distinguere quella data dalla data di stampa. L’agente può proporre una soluzione motivata; il manuale citato non ha già scelto il layout.

agentic-sdlc guida analisi, design, implementazione, test e review. In Standalone il design vive nell’ANALYSIS del progetto. Le prove devono osservare la ricevuta prodotta e la distinzione fra le date, inclusi i casi pertinenti individuati nell’analisi.

Nessuna di queste verifiche è stata eseguita nel caso. Se hai richiesto devPNT per cominciare, torna a S41; se hai chiuso dal solo manuale, rileggi S40.

### Complete explanation

La soluzione applica il metodo a un caso nuovo senza costringere a ricordare sigle. Il beneficio per la persona determina ciò che il test deve osservare: non basta che una variabile contenga la data. Non si impone un particolare layout in assenza di decisione.

### Visual content

Tre righe «Fonte», «Decisione», «Prova», ciascuna con il contenuto concreto della ricevuta.

### Transition

Puoi provare lo stesso ragionamento su un documento del tuo lavoro, senza modificare il progetto.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S44
Module: M6
Objective: O6
Role: explanation
Title: Applicazione facoltativa: scegli un tuo documento
Value contribution: La pratica trasferisce il metodo senza imporre produzione di artefatti durante la lezione.

### Learner content

Scegli un documento che sei autorizzato a consultare e una modifica ipotetica del tuo progetto. Puoi rispondere a voce o in note personali; non devi inviare documenti o cambiare file. In alternativa usa il caso della ricevuta.

Prepara una breve proposta:

1. Quale domanda poni alla fonte? Cita la risposta con versione e passaggio, oppure dichiara ciò che manca.
2. Chi deve ottenere quale beneficio? Distingui la regola documentata dalle decisioni ancora aperte.
3. Quale superficie cambierebbe, quale rischio vedi e quale prova lo osserverebbe?
4. Chi governa conoscenza e modifica? Quale modalità è disponibile?

Confronta il risultato con S43: fonte, decisione e prova devono essere distinguibili. «Non ho ancora verificato» è una risposta corretta a un limite reale; una citazione inventata non lo è.

### Complete explanation

La pratica trasferisce il metodo senza imporre produzione di artefatti durante la lezione. La soluzione del caso Ricevute, già mostrata, funge da esempio e criterio. Nel proprio progetto non esiste una risposta universale: se manca fonte si torna a S13–16, se manca beneficio aS25, se la prova non osserva il rischio aS32–36. Non si presume l’autorizzazione a condividere dati del lavoro.

### Visual content

Lista numerata, con rinvii visibili ai quattro gruppi di idee. Nessun campo che inviti a caricare un documento.

### Transition

Che cosa rimane di questo lavoro quando riapriamo il progetto dopo una settimana, un mese o anni?

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-7
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11

## S45
Module: M7
Objective: O7
Role: explanation
Title: Dopo una settimana: evitare una ricostruzione
Value contribution: Il confronto mantiene costanti compito e informazione.

### Learner content

Una settimana dopo la correzione, una nuova sessione deve spiegare perché una richiesta standard di luglio resta in attesa a 35 secondi. Supponiamo che nulla sia cambiato nelle fonti e nel software.

**Con note curate:** la decisione, la fonte e i risultati delle prove permettono già di ricostruire la ragione senza ripetere tutta l’indagine.

**Con il protocollo applicato:** l’analisi rimanda al claim e alle fonti; i risultati registrati mostrano che cosa era stato verificato. Gli indici aiutano a raggiungerli.

Se entrambi conservano le stesse informazioni, possono dare lo stesso aiuto. La skill rende esplicito e riusabile il requisito di lasciarle; non dimostra da sola che siano presenti. Un riferimento non più apribile riduce il beneficio in entrambi i casi.

### Complete explanation

Il confronto mantiene costanti compito e informazione. Evita di contrapporre una nota povera a un protocollo eseguito perfettamente. Il valore osservabile è una specifica ricostruzione che può essere evitata, non un numero di minuti inventato o una memoria illimitata.

### Visual content

Due colonne con stessa domanda iniziale e stessi elementi: motivo, fonte, verifiche. Riga finale comune «accesso e pertinenza da controllare».

### Transition

Dopo un mese non basta ritrovare: potrebbe essere necessario correggere ciò che abbiamo conservato.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S46
Module: M7
Objective: O7
Role: explanation
Title: Dopo un mese: la memoria deve cambiare con il progetto
Value contribution: La nuova regola non riceve un numero inventato perché non serve alla spiegazione: la domanda è come si governa il cambiamento della conoscenza.

### Learner content

Un mese dopo arriva una nuova regola del fornitore. Non ne conosciamo ancora gli effetti: prima leggiamo la fonte e ne confrontiamo l’ambito.

Una nota curata con legami a decisioni e verifiche aiuta a trovare ciò che va riesaminato. Se conserva soltanto «ora 45», occorre ricostruire quelle dipendenze.

Il protocollo di kb-agentic richiede di preservare provenienza, conflitti e sostituzioni; quello di agentic-sdlc collega il cambiamento al comportamento e alle prove. Questi requisiti rendono più visibili le omissioni **se vengono applicati e controllati**.

Mantenere legami, rileggere e riprovare costa lavoro. Nessun archivio corregge automaticamente il software. Il vantaggio possibile è sapere dove intervenire e perché, anziché ricominciare senza tracce.

### Complete explanation

La nuova regola non riceve un numero inventato perché non serve alla spiegazione: la domanda è come si governa il cambiamento della conoscenza. La nota completa resta un’alternativa legittima. La distinzione dal caso della settimana è la necessità di aggiornare, non solo ritrovare.

### Visual content

Mostrare «nuova fonte → confronto → elementi da riesaminare». Due ingressi equivalenti: nota con riferimenti e protocollo con riferimenti. Evidenziare «lavoro di revisione necessario».

### Transition

Proviamo a spiegare il valore senza attribuirlo al solo nome della skill.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S47
Module: M7
Objective: O7
Role: check
Title: Prova: che cosa abbiamo davvero risparmiato?
Value contribution: Il confronto rende esplicita l’equivalenza delle condizioni prima di variarne una.
Solution: S48

### Learner content

Due team devono spiegare e, quando serve, correggere la scadenza di Orione.

Il primo mantiene note con fonti, motivi, decisioni, collegamenti ai consumatori e risultati delle prove. Il secondo usa le due skill e conserva gli stessi elementi. Entrambi li consultano e aggiornano.

Confrontali dopo una settimana senza cambiamenti e dopo un mese con una nuova fonte. Che cosa possono evitare di ricostruire? Quale lavoro devono comunque fare? Quale differenza rimarrebbe se il primo team dimenticasse di mantenere i collegamenti?

Concludi se questi dati dimostrano che la skill è indispensabile o che fa risparmiare una certa percentuale di tempo. Motiva la risposta prima di S48.

### Complete explanation

Il confronto rende esplicita l’equivalenza delle condizioni prima di variarne una. Il criterio rifiuta sia la superiorità automatica sia l’idea che la disciplina non serva: quando mancano collegamenti, una specifica omissione diventa osservabile. Non sono forniti dati quantitativi di costo o rendimento.

### Visual content

Due colonne con gli stessi elementi, senza punteggi. Una terza riga descrive la variazione «collegamenti non mantenuti».

### Transition

La risposta deve attribuire il beneficio alle informazioni e alle verifiche effettive.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S48
Module: M7
Objective: O7
Role: solution
Title: Soluzione: il vantaggio dipende dal lavoro conservato
Value contribution: Il corso attribuisce i risultati ai meccanismi descritti e ammette equivalenza dove i requisiti sono equivalenti.

### Learner content

Dopo una settimana entrambi possono riaprire motivo, fonte e prove della scelta. Evitano la ricostruzione di quel ragionamento, purché il materiale sia ancora accessibile e pertinente.

Dopo un mese entrambi devono esaminare la nuova fonte, valutarne l’ambito e riesaminare decisioni e comportamento. I collegamenti già presenti orientano la ricerca; non eseguono la correzione.

Se il primo team perde i legami, dovrà ricostruirli. La differenza osservata è la manutenzione mancante. Il protocollo può richiederla in modo riusabile, ma dobbiamo controllare che anche il secondo team l’abbia eseguita.

Questi dati non dimostrano indispensabilità o percentuali di risparmio. Se hai attribuito il vantaggio all’installazione, torna a S04 e S09; se hai dimenticato i costi di revisione, a S46.

### Complete explanation

Il corso attribuisce i risultati ai meccanismi descritti e ammette equivalenza dove i requisiti sono equivalenti. Il valore dell’insegnamento è saper riconoscere quel meccanismo e scegliere quale disciplina mantenere. L’assenza di una misura causale viene dichiarata con riferimento alla domanda concreta.

### Visual content

Quattro righe: ricostruzione evitabile, controllo necessario, differenza di manutenzione, conclusione sostenibile. Nessun grafico numerico di produttività.

### Transition

Dopo anni, la domanda più difficile arriva da chi non era presente quando il lavoro fu fatto.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S49
Module: M7
Objective: O7
Role: explanation
Title: Dopo anni: consegnare un ragionamento a chi arriva
Value contribution: Il caso completa l’orizzonte degli anni senza promessa di durata automatica.

### Learner content

Una nuova collega non conosce le vecchie chat di Orione. Trova la decisione sulla scadenza e una GUIDE che spiega come seguire il calcolo fino a pannello ed email.

La guida le dà un punto di partenza, ma deve controllare che i componenti e le fonti citati esistano ancora e svolgano quelle funzioni. Se il sistema è cambiato, la guida va corretta prima di usarla come mappa affidabile.

Note curate e documentazione prodotta con le skill possono entrambe conservare ragioni, alternative scartate e prove. Un archivio non letto o non mantenuto può invece propagare errori vecchi.

Il patrimonio utile cresce attraverso **conservazione, consultazione e revisione**. Il tempo trascorso, da solo, non lo rende più affidabile.

### Complete explanation

Il caso completa l’orizzonte degli anni senza promessa di durata automatica. Il controllo sul modello operativo è distinto dal semplice accesso al file. Il nuovo collega può evitare una parte della ricostruzione ma non il giudizio sulla pertinenza corrente; questo è il costo realistico del passaggio di conoscenza.

### Visual content

Percorso «collega nuova → decisione → GUIDE → riferimenti reali da controllare». Mostrare un ramo «divergenza trovata → aggiornare guida», senza nascondere il costo.

### Transition

Mettiamo alla prova il criterio di scelta su due progetti che non sono Orione.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S50
Module: M7
Objective: O7
Role: check
Title: Trasferimento: quale disciplina proporresti?
Value contribution: La prova cumulativa riduce i suggerimenti e richiede trasferimento: confronto equo, conflitto non risolto e impatto multisuperficie.
Solution: S51
Covers: M2/O2; M3/O3; M4/O4; M5/O5; M6/O6

### Learner content

Due progetti inventati.

**Alba** conserva una sola decisione su una fonte stabile, con motivo, passaggio citato e verifica del comportamento. Una persona mantiene quei riferimenti.

**Bora** ha tre operatori, un pannello e un’email. Due documenti indicano durate incompatibili per la stessa versione, periodo e tipo di richiesta. Non c’è una rettifica. Le note riportano i due valori senza spiegare il contrasto. Un agente propone di scegliere l’ultimo file ricevuto e cambiare soltanto il pannello.

Proponi come proseguire in entrambi i progetti. Che cosa sai già, che cosa manca, quali decisioni e prove servono, e quale traccia lasceresti a chi arriva fra anni? Motiva se useresti note curate o un protocollo riutilizzabile. Prova senza rileggere gli esempi.

### Complete explanation

La prova cumulativa riduce i suggerimenti e richiede trasferimento: confronto equo, conflitto non risolto e impatto multisuperficie. Non chiede soltanto di assegnare una skill. La soluzione successiva esplicita un percorso possibile, lasciando ammissibili proposte equivalenti motivate dai dati.

### Visual content

Due schede Alba/Bora. Nessuna freccia dal nome del progetto a una skill per non suggerire la raccomandazione.

### Transition

Confrontiamo le ragioni della scelta, non la quantità di termini tecnici usati.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S51
Module: M7
Objective: O7
Role: solution
Title: Soluzione: proporzionare, chiarire, verificare
Value contribution: Una risposta sufficiente respinge l’aggiornamento del solo pannello senza presumere l’architettura.
Covers: M2/O2; M3/O3; M4/O4; M5/O5; M6/O6

### Learner content

**Alba:** la nota curata può già bastare. Mantieni accessibili fonte, motivo e prova; riapri la scelta se cambiano le condizioni.

**Bora:** conserva il conflitto e cerca nuova informazione che lo risolva. La recenza del file non basta. Una decisione prudenziale del responsabile può essere proposta separatamente, dichiarando l’incertezza; non diventa la verità della fonte.

Quando il comportamento è definito, cerca calcoli e consumatori, progetta pannello ed email, includi confini ed errori, fai rivedere il design, realizza e prova. Sia la review del design sia quella finale richiedono un revisore distinto dall’autore. La review finale confronta evidenze e beneficio. Conserva decisioni e riferimenti per il successore; una guida serve se sostiene un’indagine riusabile.

Le skill possono organizzare questa disciplina; istruzioni equivalenti possono farlo senza skill. Se la tua risposta sceglie soltanto uno strumento, mancano le ragioni: conflitto S20–21, impatto S29–36, manutenzione S49.

### Complete explanation

Una risposta sufficiente respinge l’aggiornamento del solo pannello senza presumere l’architettura. Il limite del caso impedisce di decidere una durata corretta. La mitigazione operativa è distinta dalla risoluzione documentale e resta una proposta da valutare. Il confronto non richiede l’adozione dello strumento più complesso.

### Visual content

Due colonne con raccomandazioni motivate. Sotto Bora, separare «chiarire la fonte» da «progettare e provare il comportamento».

### Transition

L’ultima domanda è quale parte di questo metodo vuoi rendere ripetibile nel tuo lavoro.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13

## S52
Module: M7
Objective: O7
Role: closing
Title: Ripartire dalle ragioni, non dalla memoria di qualcuno
Value contribution: La chiusura collega l’azione futura all’esperienza percorsa, senza riassumere un elenco di sigle.

### Learner content

Siamo partiti da un numero nel codice. Per usarlo bene abbiamo dovuto ritrovare il motivo, controllare la fonte, riconoscere un conflitto, chiarire il risultato voluto e cercare prove sul comportamento.

Nel prossimo lavoro con un agente puoi porre tre domande:

1. «Su quale fonte e a quali condizioni si basa questa affermazione?»
2. «Quale risultato deve ottenere qualcuno, e quale scelta è ancora aperta?»
3. «Che cosa è stato verificato e quale traccia permetterà di ripartire?»

kb-agentic e agentic-sdlc rendono riutilizzabili parti di questa disciplina. Il valore sta nell’applicarla e controllarne gli esiti.

Se vuoi verificarne il ricordo, riprova fra qualche giorno il caso di S50 senza consultare la soluzione. Il corso non programma promemoria e non misura automaticamente apprendimento o risultati sul tuo progetto.

### Complete explanation

La chiusura collega l’azione futura all’esperienza percorsa, senza riassumere un elenco di sigle. Il richiamo differito è facoltativo e non equivale a una prova di ritenzione svolta. Lo stato di efficacia umana resta non verificato: il corso e le sue simulazioni non costituiscono un pilot con persone.

### Visual content

Tre domande complete, in ordine verticale. Non aggiungere un elenco di artefatti o nuove definizioni.

### Transition

Fine del percorso. Per tornare a una difficoltà usa i rinvii nelle soluzioni; non è disponibile un canale automatico di feedback del corso.

### Sources
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12
- ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13
