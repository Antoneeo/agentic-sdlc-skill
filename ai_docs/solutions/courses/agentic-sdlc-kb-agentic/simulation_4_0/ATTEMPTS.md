# Tentativi preservati — 4.0-content

Data: 2026-10-04. Sessioni native fresche `/root/course40_reader` e `/root/course40_control`, modello ereditato dall'autore; nessun override. Il reviewer didattico distinto è `/root/course40_material_review`, gpt-6-astra, fresh context, read-only.

Isolamento per istruzioni, non sandbox tecnico: entrambi potevano tecnicamente accedere agli strumenti comuni. I compiti T1/T2 e i criteri sono stati congelati prima dei tentativi. Il controllo ha ricevuto solo i compiti, senza corso o criteri, e non ha usato strumenti. Il reader ha ricevuto S01–S06 una alla volta, chiedendo dopo ciascuna cosa stesse leggendo, cosa aggiungesse e quali prerequisiti o passaggi mancassero; nessun suggerimento sul contenuto atteso. Le esposizioni coincidono con `packet.json` per queste sei unità, invariate dalla successiva correzione F1–F4.

Per la prova finale il reader ha il packet completo senza le sette soluzioni. Un'unica lettura del file assegnato serve alla consegna del materiale; nessuna ricerca esterna è consentita. È un'eccezione amministrativa al divieto di strumenti del prompt congelato, da dichiarare nel confronto. L'accesso a informazioni esterne resta vietato a entrambi. Il prefisso è sequenziale; il resto del corso non è diagnosticato unità per unità.

## Reader — S01

Il corso riguarda la continuità del lavoro con gli agenti: una nuova sessione può vedere il codice senza conoscere i vincoli e le decisioni precedenti.

Questa unità introduce il problema delle informazioni disperse e presenta kb-agentic, agentic-sdlc e distill come strumenti per rendere la conoscenza riutilizzabile. Il beneficio atteso è recuperare ciò che conta e capire se vale ancora.

Non serve conoscere già le skill per seguire il problema. Restano da chiarire il ruolo di ciascuna e cosa renda una nota affidabile e attuale. La transizione annuncia un esempio concreto in cui conoscere il motivo di una scelta cambia la valutazione di una correzione.

## Reader — S02

Il corso continua a mostrare come conservare le ragioni delle modifiche, oltre al codice.

Questa unità aggiunge un esempio: Orione impedisce due invii dovuti a clic ravvicinati disabilitando il pulsante durante l’attesa. La nota conserva il problema osservato, il motivo della scelta e la verifica prevista. Conserva anche il limite: questa protezione copre il doppio clic, senza garantire che ogni duplicazione sia impedita.

L’esempio è comprensibile senza prerequisiti tecnici particolari. Non è ancora specificato dove si conserva la nota o come una nuova sessione la ritrova. La transizione annuncia un incidente diverso, ancora da conoscere.

## Reader — S03

Il problema ora riguarda un ordine duplicato perché la conferma si perde: la persona ritenta la stessa operazione, pur essendo l’ordine già stato creato.

Questa unità aggiunge una protezione basata sull’identità dell’ordine. Orione riusa la stessa chiave nei ritentativi; secondo il contratto fittizio, il fornitore riconosce quella chiave e restituisce l’esito precedente. La conoscenza da conservare comprende quindi anche un vincolo tra sistemi, oltre al motivo del blocco del pulsante.

“Ordine logico” è comprensibile come l’unico ordine voluto dalla persona. Non è ancora spiegato come Orione conservi la chiave e distingua un ritentativo da un nuovo ordine. La responsabilità annunciata nella transizione resta da conoscere.

## Reader — S04

Sto leggendo come la conoscenza del progetto si costruisce attraverso problemi successivi e ragioni conservate.

Questa unità aggiunge la separazione tra creazione dell’ordine e invio dell’email: ritentare una notifica fallita non deve creare altri ordini. Collega questa protezione alle due precedenti e chiarisce che conta poter recuperare le ragioni quando una richiesta riguarda quel comportamento, senza memorizzare le date.

Il passaggio è comprensibile. Resta da spiegare come siano organizzati i file e come si ritrovino le decisioni pertinenti. Il baco annunciato non è ancora descritto.

## Reader — S05

Sto leggendo un caso in cui correggere un sintomo può compromettere una garanzia precedente.

Questa unità mostra che la proposta combina due cambiamenti: togliere il blocco permette di ritentare, ma generare una nuova chiave può duplicare l’ordine. Distingue le conseguenze dei due interventi e chiarisce il ruolo della storia: orienta la verifica, senza decidere automaticamente il fix.

Il passaggio è comprensibile grazie al contratto sulla chiave introdotto prima. Non conosciamo ancora la causa del pulsante rimasto bloccato, quindi manca l’evidenza per scegliere la correzione. Resta aperto anche come rendere questa conoscenza reperibile tra sessioni e agenti.

## Reader — S06

Sto leggendo la distinzione tra il contesto di una conversazione e la conoscenza persistente del progetto.

Questa unità chiarisce che i file restano disponibili, ma devono essere recuperati e letti quando pertinenti. Definisce inoltre le skill e assegna un ruolo alle tre citate. L’agente può lavorare su conoscenza conservata e aggiornata senza riaddestrarsi; le istruzioni guidano il lavoro senza garantirne la correttezza.

Il passaggio è comprensibile. Non è ancora mostrato il meccanismo di recupero delle tracce. Interpreto l’esercizio finale come una richiesta all’agente di consultare le decisioni precedenti e far emergere le garanzie da rispettare, lasciandogli la verifica del guasto e la progettazione della correzione.

## Controllo — T1

«Approvo l’obiettivo di sbloccare il pulsante, ma contesto il ritentativo dell’intera operazione con un nuovo identificatore. Potrebbe creare una seconda prenotazione quando la prima è già confermata e solo la mail è fallita: è proprio il rischio che la decisione esistente intende evitare.
Prima di intervenire, leggi la decisione e il contratto nei file accessibili. Mostrami dove nasce il blocco, quali effetti sono già avvenuti quando compare e come la proposta rispetta la separazione tra conferma e messaggio. Se ritieni necessario cambiare quella decisione, esplicita il motivo e le alternative: non considerarla superata implicitamente.
Un test sul pulsante non basta per chiudere. Chiedo prove che coprano anche mail fallita dopo la conferma, ritentativi e clic ripetuti, verificando sia lo sblocco sia l’assenza di prenotazioni duplicate.
Una disciplina di conoscenza e cambiamento aiuta a recuperare il motivo delle scelte precedenti e a collegare problema, intervento e verifiche. Deve proteggere il comportamento complessivo, senza diventare documentazione fine a sé stessa.»

## Controllo — T2

«Non approvo lo stesso percorso completo per entrambi senza una ragione specifica. In Cobalto parti dalla fonte della regola e dalla nota aggiornata; approfondisci se emergono ambiguità, dipendenze o contraddizioni. In Mira serve una ricostruzione più ampia delle eccezioni e delle decisioni, distinguendo quelle attuali da quelle superate. Anche lì, motiva le letture: leggere tutto non garantisce di capire quali indicazioni governano il caso.
Adotterei quindi un metodo comune, ma con profondità proporzionata alla complessità e all’incertezza.
Contesto anche il salvataggio rinviato a dopo la compattazione. Aver trovato la causa non significa aver scelto l’intervento. Prima di compattare, registra nel luogo previsto la causa con le sue prove, la scelta ancora aperta, le alternative rilevanti e ciò che serve per decidere. Poi verifica che il contesto necessario sia recuperabile.
Non devi decidere frettolosamente per poter salvare: devi conservare fedelmente anche l’incertezza. Altrimenti la ripresa rischia di trasformare un’ipotesi in una decisione o di ripetere l’indagine.»

## Reader — trasferimento

**T1 — Risposta all’agente**

«Approvo l’obiettivo di permettere il recupero della prenotazione. Contesto il ritentativo dell’intera operazione con un identificatore nuovo ogni volta e non approvo la chiusura basata solo sul test del pulsante.

Apri la decisione e il contratto disponibili: indica i passaggi letti, la loro validità corrente e le condizioni che riguardano questa operazione. Non assumere che il contratto di Selene sia quello dell’esempio Orione. Verifica che cosa distingue un recupero della stessa prenotazione da una prenotazione nuova e quale garanzia offre l’identificatore.

Mostra quali osservazioni sostengono la causa del blocco e quali alternative hai escluso. La decisione precedente impone di verificare che una mail fallita o ritentata non crei un’altra prenotazione. Chiedo inoltre evidenze sul recupero dopo una conferma persa, sugli invii ravvicinati e sulla creazione intenzionale di una nuova prenotazione. Il test del pulsante dimostra un risultato parziale.

Prepara tu la proposta motivata, indicando impatto, garanzie preservate, scelte aperte e verifiche; sottoponi il design alla review prevista prima di implementare. Per chiudere servono prove pertinenti e tracce aggiornate che una nuova sessione possa ritrovare.

kb-agentic può aiutare a consultare fonti e decisioni mantenendone ambito e validità; agentic-sdlc collega quei vincoli al cambiamento e alle verifiche. distill aiuta a conservarli in testi utilizzabili. Nessuna delle tre garantisce da sola che il fix sia corretto.»

Passaggi usati: S03–S06, S09–S10, S14, S23–S28, S31.

**T2 — Risposta all’agente**

«Contesto il percorso completo e la lettura totale applicati automaticamente a entrambi.

In Cobalto una fonte e una nota breve, aggiornata e consultata possono bastare. Proponi un percorso proporzionato al compito e al rischio, motivando il livello che dichiari. Non serve aggiungere documenti soltanto per applicare il metodo.

In Mira considero utile una disciplina ripetibile perché eccezioni e decisioni cambiate rendono più difficile capire quali regole valgano oggi. Voglio poter recuperare fonti, condizioni, decisioni superate, ragioni e conclusioni dipendenti. Seleziona ciò che serve al compito e riapri le fonti decisive; rendi esplicite le lacune di recupero. Non caricare indiscriminatamente tutto l’archivio.

Scrittura, manutenzione, letture e review costano. Valutiamo se aiutano concretamente a ritrovare ragioni e preservare vincoli. Note governate con istruzioni equivalenti possono produrre esiti equivalenti: non assumo un vantaggio universale delle skill.

Non approvo la compattazione con il salvataggio rimandato. La causa trovata è un risultato acquisito; la scelta fra soluzioni è ancora aperta. Prima di compattare, salva nel progetto il risultato con le prove, le alternative e il punto decisionale ancora irrisolto. Prepara tu l’handoff necessario e mostrami dove una nuova sessione potrà recuperare lo stato e le fonti. Dopo aver verificato la possibilità di ripresa, possiamo compattare, riconoscendo che non è garantita senza perdite.»

Passaggi usati: S11, S14–S16, S19, S32–S39.
