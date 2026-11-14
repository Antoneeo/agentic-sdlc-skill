# Rapporto dal campo: sei punti in cui il metodo ha ceduto in una giornata di lavoro reale

**Per chi è.** La sessione che sviluppa le skill `agentic-sdlc` e la dottrina devPNT. Serve a decidere quali di questi problemi meritano una modifica alle skill. È scritto come una vision: dice che cosa è successo, a chi, e come si riconosce che è risolto. Non dice come risolverlo; le idee in fondo sono spunti, non requisiti.

**Da dove viene.** Una sessione coordinatrice (Claude Code, app desktop) al lavoro per una giornata intera, il 2026-11-14, su un prodotto in produzione con dati cifrati e utenti veri. La coordinatrice non scrive codice: delega a sessioni figlie e a revisori indipendenti, tiene i registri, porta le decisioni al proprietario. Modalità Hybrid con devPNT. Ogni caso sotto è accaduto quel giorno; dove cito il proprietario, sono parole sue.

**Perché conta.** Proprietario: «quello che fai resta solo con me invece le skills le usano in 45000+ persone». Una correzione locale alla coordinatrice non serve a nessun altro.

---

## Problema

Sei casi reali. Nei primi cinque il metodo era stato seguito, e il difetto è passato lo stesso.

### 1. Il rapporto di una sessione delegata non arriva intero a chi coordina

Quando una sessione figlia finisce un turno, la coordinatrice riceve un avviso con solo l'inizio del rapporto. Il rapporto intero va riletto dalla trascrizione dell'altra sessione, e quel giorno la rilettura ha restituito più volte soltanto l'elenco delle chiamate agli strumenti.

Effetto: un rapporto conteneva una decisione riservata al proprietario (una regola di sicurezza più stretta di quella che lui aveva approvato). La coordinatrice ne ha visto la prima riga, ha dovuto chiedere alla sessione di rimandare il testo, e solo allora ha potuto presentare la decisione. Un'altra volta la riga per il registro delle revisioni non era leggibile, e la coordinatrice l'ha riscritta di suo pugno dal riassunto.

Il limite di lunghezza è di un client. Il problema generale non lo è: **il canale fra agenti non garantisce che il contenuto arrivi, e il metodo oggi ci si affida.**

### 2. Un lavoro chiuso con la guida rimasta falsa, e il validatore pulito

Dopo un rilascio in produzione la coordinatrice ha aggiunto una riga al registro in fondo alla guida operativa e ha chiuso il nodo. Due paragrafi più sopra dicevano ancora «forma provvisoria» e «non ancora in produzione». Il controllo dei documenti ha dato CLEAN.

Se n'è accorto il proprietario, chiedendo: «come mai non tieni aggiornate le guide senza che io te lo ricordi?»

La regola «le guide vanno aggiornate» esisteva già. È stata letta come «scrivi qualcosa nella guida», e una riga aggiunta è sembrata bastare. **Aggiungere non è aggiornare: una guida diventa falsa per le frasi che restano, non per quelle che mancano.** E un validatore che controlla la forma, quando dice «pulito», viene preso per un controllo dei fatti.

### 3. Quaranta filoni aperti, e l'avviso che nessuno legge più

Il registro dei lavori generato dal validatore contava 40 filoni aperti, contro i 20 che il validatore stesso indica come tetto. L'avviso compare a ogni rigenerazione. Non ferma nulla, e la coordinatrice quel giorno l'ha letto più volte senza agire.

Proprietario: «avere 40 filoni aperti è un problema nostro.. dovremmo chiuderli poco alla volta ed evitare di aprirne di nuovi finché non raggiungono un numero basso (<10)».

E, sul fatto che sia un problema del metodo e non solo del progetto: «anche il problema dei fronti aperti e non chiusi è un problema di skills.. dovrebbe prescrivere di controllare i fronti aperti e fare un riassunto prima di accettare nuove attività».

Molti di quei filoni sono probabilmente lavori già rilasciati il cui file di passaggio non è mai stato cancellato. **Il metodo rende facile aprire un filone e non chiede mai di guardare quelli aperti prima di accettarne uno nuovo.** L'orientamento di inizio sessione elenca il registro, ma nessun passo obbliga a leggerlo nel momento in cui arriva una richiesta nuova.

### 4. Dopo una compattazione, metà di un lavoro attivo è sparita

Il contesto della coordinatrice è stato compattato a metà giornata. Nel riassunto un milestone attivo compariva solo per l'argomento discusso in quel momento. L'altra metà del suo scopo, approvata nella vision, non c'era.

Quando il proprietario ha chiesto se una certa funzione fosse stata fatta, la coordinatrice non l'ha collegata a quel milestone: ha cercato nel codice e nel registro dei difetti e ha risposto «do per buono che stia lì». La risposta giusta stava in un documento solo, la vision, riletta solo alla seconda domanda.

Proprietario: «Le compattazioni sicuramente non posso controllarle dalle skills.» Vero. **Ma il metodo non dice che cosa rileggere quando si riparte da un riassunto**, e un riassunto conserva l'argomento del momento, non lo scopo.

### 5. Gli strumenti di lettura di devPNT non coprono ciò che sembrano coprire

Tre fatti dello stesso giorno:
- il piano d'azione di un milestone non entra in una risposta (oltre 73.000 caratteri): la coordinatrice l'ha letto da file con uno script;
- due revisori indipendenti hanno annotato che la ricerca testuale del progetto non restituiva file che contenevano il testo cercato;
- il sommario del progetto era vecchio di tre settimane, e l'indice dei simboli riportava righe non più valide.

La dottrina impone già il doppio controllo (grafo dei simboli più ricerca testuale, con il delta dichiarato), ed è questo che ha retto. Ma regge perché chi revisiona è diligente, non perché lo strumento dica che cosa non ha esaminato.

### 6. Chi decide che cosa non era scritto da nessuna parte, e l'agente non l'ha chiesto

Per tutta la giornata la coordinatrice ha portato al proprietario scelte che non erano sue: in che ordine scrivere il codice, se avviare un lavoro già approvato, se rifare un giro di revisione. E in altri momenti ha deciso da sola cose che invece lo riguardavano. Il confine veniva ricostruito caso per caso da regole sparse nella memoria dell'agente, accumulate in settimane di correzioni.

Il proprietario lo ha dovuto dire tre volte nello stesso pomeriggio:

- «io non ti dirò non ora.. dobbiamo andare avanti e ti prego di non farmi domande inutili»;
- «cerca di assumerti il ruolo di responsabile e di non riversare su di me scelte che non sono di prodotto ne decisie per l'architettura»;
- e, proponendo il rimedio: «Il tuo ruolo da coordinatore forse non era chiaro, forse vanno chiarito con l'utente il livello di delega e i ruoli, anche quello dell'utente. Per ciascun progetto. […] Ma dovrebbe essere l'agente a chiedere per chiarire bene da subito chi fa cosa e dove si può spingere in autonomia».

Il metodo ha già una regola sulle domande (un dubbio vero si chiede quando emerge). Non ha il suo rovescio: **quali decisioni sono dell'agente e non vanno chieste**. Senza un accordo scritto, l'agente prudente chiede troppo e trasforma il proprietario nel collo di bottiglia; l'agente sicuro di sé decide ciò che non gli spetta. Entrambi gli errori sono capitati lo stesso giorno, alla stessa sessione.

Due aggravanti viste sul campo:
- Le regole di delega esistevano, ma come correzioni accumulate nella memoria privata dell'agente: una sessione nuova, o una sessione figlia, non le eredita.
- Dopo una compattazione il confine si perde con il resto: la coordinatrice ha ricominciato a chiedere cose che settimane prima le erano state delegate.

---

## Stella polare

> **Chi segue il metodo non può chiudere un lavoro, accettare un rapporto o riprendere dopo un'interruzione fidandosi di un segnale che non misura ciò che sembra misurare.**

## Beneficio

- **Per il proprietario:** non deve accorgersi lui di ciò che il metodo doveva vedere. Quel giorno è successo tre volte (guida falsa, lavoro non riconosciuto, decisione rimasta in un rapporto non letto).
- **Per chi coordina:** sa che cosa ha davvero ricevuto da una sessione delegata, e che cosa un «pulito» copre e che cosa no.
- **Per chi usa le skill senza devPNT e senza sessioni multiple:** i punti 2, 3 e 4 valgono anche per un agente solo, in modalità Standalone.

## Attori

- **Proprietario del progetto** — decide. Buona esperienza: riceve le decisioni sue, intere, una volta; non fa da ultimo controllo.
- **Agente che coordina** — delega e verifica. Buona esperienza: legge un rapporto per intero senza doverlo richiedere; riparte da un riassunto sapendo che cosa rileggere.
- **Agente delegato** — esegue e riferisce. Buona esperienza: sa dove lasciare il rapporto perché arrivi.
- **Agente solo, Standalone** — fa tutto. Buona esperienza: chiude un lavoro con le guide vere e riparte da una compattazione senza perdere lo scopo.

## Segnali di successo

1. **Rapporto intero.** In una prova con una sessione delegata che produce un rapporto lungo, contenente una decisione per il proprietario oltre la parte che l'avviso mostra, chi coordina presenta quella decisione senza chiedere di nuovo il rapporto. Base: quel giorno, richiesto di nuovo una volta su una.
2. **Guida vera alla chiusura.** In una prova in cui una guida contiene una frase sullo stato precedente («non ancora in produzione») e il lavoro la rende falsa, la chiusura non passa finché la frase non è riscritta. Base: passata con CLEAN.
3. **Filoni che scendono.** Il numero dei filoni aperti nel registro, in un progetto che parte sopra il tetto, scende nel tempo invece di salire. Base: 40 il 2026-11-14; l'andamento precedente non è stato misurato.
4. **Ripresa che ritrova lo scopo.** Dopo una compattazione, alla domanda «questa funzione è stata fatta?» su una parte di un lavoro attivo che il riassunto non nomina, l'agente risponde citando la vision del lavoro, alla prima domanda. Base: alla seconda.
5. **Copertura dichiarata.** Una ricerca che non ha esaminato tutti i file lo dice nel risultato, in modo che chi la legge non debba scoprirlo con un secondo strumento. Base: scoperto dai revisori.

6. **Delega chiara dal primo giorno.** In un progetto nuovo, o alla prima sessione di un agente in un progetto esistente, prima del primo lavoro significativo l'agente ha un accordo scritto su chi decide che cosa, e lo ritrova dopo una compattazione e in una sessione figlia. Misura: in una giornata di lavoro, quante domande dell'agente il proprietario giudica non sue. Base: tre richiami espliciti in un pomeriggio.

## Confini: cosa questo rapporto non chiede

- Cambiare quando o come un client compatta il contesto.
- Aggirare i limiti di un client specifico con regole che lo nominano: una regola che cita una lunghezza in caratteri invecchia con il client.
- Alleggerire le porte di revisione. Sono la parte che ha funzionato meglio (vedi sotto).
- Nuovi documenti obbligatori. Il progetto ha già 40 filoni: ogni rimedio che apre un file per lavoro peggiora il punto 3.

## Cosa non rompere

Quel giorno queste parti hanno fatto il loro lavoro, e un rimedio che le indebolisce costa più di quanto rende.
- **La revisione indipendente prima di accettare** ha fermato tre difetti veri che l'autore non vedeva, uno dei quali di sicurezza.
- **Il registro delle richieste con le parole testuali del proprietario** è ciò che ha permesso, dopo la compattazione, di distinguere una sua decisione da una deduzione dell'agente.
- **La vision prima di tutto:** quando è stata riletta, la risposta era lì ed era giusta.
- **La distinzione fra ciò che l'agente accetta dopo un PASS e ciò che decide il proprietario.**

## Vincoli proposti

- **Vale per ogni client e per la modalità Standalone.** Un rimedio che funziona solo con sessioni multiple o solo con devPNT copre una minoranza dei 45.000.
- **Un segnale dice che cosa misura.** Dove un controllo automatico resta di sola forma, il metodo lo dichiara nel punto in cui l'agente lo legge, non in una nota altrove.
- **Chiudere costa meno che aprire.** Qualunque rimedio al punto 3 deve rendere la chiusura di un filone più facile della sua apertura, non aggiungere un passo.

## Spunti, non requisiti

Da valutare con uno spike; qui solo perché sono emersi parlando con il proprietario.
- Punto 1 — proprietario: «Sto pensando se le skills non dovrebbero scrivere su file i messaggi per la coordinatrice e avvisarti soltanto. Una sorta di message box su file system.» Un file sopravvive anche alla compattazione di chi coordina, e il proprietario può aprirlo. Da decidere: dove sta, chi lo cancella, come non diventa un quarantunesimo filone.
- Punto 2 — alla chiusura, cercare nelle guide toccate le frasi sullo stato di prima e riscriverle; dichiarare nel messaggio di chiusura quali guide sono state rilette.
- Punto 3 — proposta del proprietario: prima di accettare un'attività nuova l'agente controlla i fronti aperti e ne dà un riassunto. In aggiunta, dalla coordinatrice: sopra il tetto, aprire un filone richiede di nominarne uno da chiudere, o una decisione esplicita del proprietario.
- Punto 6 — proposta del proprietario: è l'agente a chiedere, da subito, chi fa cosa e fin dove può spingersi da solo, progetto per progetto, ruolo dell'utente compreso. Dalla coordinatrice, come materia per lo spike: l'accordo sta in un file del progetto e non nella memoria dell'agente, così lo leggono anche le sessioni figlie; elenca per classi ciò che resta al proprietario (nel caso osservato: scelte di prodotto, decisioni di architettura, tutto ciò che tocca produzione, segreti, pubblicazione) e dice che il resto è dell'agente, che decide e riferisce in una riga; si rilegge alla ripresa da un riassunto insieme alla vision; si aggiorna quando il proprietario corregge il confine, invece di lasciare la correzione in una nota privata. Da decidere: quante domande servono per stabilirlo senza diventare un interrogatorio, e che cosa vale quando l'accordo tace.
- Punto 4 — alla ripresa da un riassunto, rileggere la vision di ogni lavoro attivo prima di rispondere su di esso.
- Punto 5 — un piano troppo grande si chiede per nodo o per sottoalbero; una ricerca dichiara quanti file ha esaminato.

## Limiti di questo rapporto

Una sola giornata, una sola sessione, un solo progetto, un solo client. I casi sono veri; la loro frequenza non è misurata. Il punto 5 riguarda devPNT più che le skill. La skill `kb-agentic` non è stata usata in quella giornata e non è coperta.
