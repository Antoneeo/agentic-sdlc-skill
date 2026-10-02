# Fixtures (verbatim learner-visible units, C-001 3.0-content)

## F1
Role: check
Title: Prova: che cosa manca alla risposta?

### Learner content

In una nuova sessione, l’agente trova `timeout = 30` nel codice e risponde: «Il team aveva scelto il valore indicato dal fornitore». Non mostra altri riferimenti.

Nella cartella del progetto esistono l’indice, la nota e il manuale incontrati fin qui. Non sappiamo se l’agente li abbia aperti.

Prima di accettare la spiegazione, indica:

- quale percorso di lettura gli chiederesti di seguire;
- quali informazioni deve contenere la risposta;
- che cosa può dire della scelta passata e che cosa non può ancora dire di luglio.

Tenta una risposta prima di passare alla soluzione. Non occorre creare file.

## F2
Role: explanation
Title: Un claim dice una cosa che possiamo controllare

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

## F3
Role: check
Title: Prova: dal documento alla risposta

### Learner content

Nuovo esempio inventato. Ricevi il Manuale Avvisi 1.2, conservato nel progetto. A pagina 12, §2, leggi:

> «Per le richieste urgenti dal 1 agosto, inviare un avviso dopo 10 secondi senza conferma».

La domanda di una collega è: «Il 5 agosto, per una richiesta urgente senza conferma, quando è previsto l’avviso?».

Descrivi il claim da conservare, l’argomento in cui lo cercheresti e la risposta da dare con il suo riferimento. Poi indica perché lo stesso brano non basta a rispondere sulle richieste standard.

Non devi creare un grafo o un file. Devi rendere visibile come il dato arriva alla risposta senza perdere le condizioni.

## F4
Role: check
Title: Prova: differenza o contraddizione?

### Learner content

Tre documenti inventati descrivono il tempo di risposta:

- A: «20 secondi per richieste standard fino al 31 agosto compreso».
- B: «25 secondi per richieste standard dal 1 settembre».
- C: «20 secondi dal 1 settembre», senza indicare il tipo di richiesta.

Quali conclusioni puoi sostenere sulle coppie A–B e B–C? Quale dato cercheresti prima di scegliere una regola per una richiesta standard di settembre?

Supponi poi che un nuovo documento chiarisca che C riguarda le urgenti. Che cosa cambierebbe e che cosa conserveresti della lettura precedente?

Rispondi prima della soluzione: il documento arrivato per ultimo non ha un privilegio automatico.

## F5
Role: check
Title: Prova: due correzioni, due effetti

### Learner content

Due ticket si chiamano «Correggere la scadenza».

**A.** L’indagine conferma che la schermata mostra «scadutaa». Si corregge soltanto la parola: nessuna logica, interfaccia pubblica o area sensibile cambia.

**B.** La schermata dichiara scaduta una richiesta standard di luglio dopo 30 secondi. La Rettifica D chiarisce la finestra di 45, ma non precisa il trattamento di una conferma arrivata esattamente al limite.

Un collega propone di aggiungere a B un nuovo menu di navigazione.

Quale livello assegneresti a ciascun ticket e perché? Quale decisione manca in B? Il menu serve al beneficio approvato? Se la fonte fosse ancora contestata, che cosa faresti prima di progettare la nuova regola?

## F6
Role: check
Title: Prova: «Il test è verde, possiamo chiudere»

### Learner content

In un nuovo tentativo su Orione, un agente dichiara: «Ho cambiato 30 in 45 e il test della costante passa». Non fornisce evidenze sulla notifica, sulle richieste urgenti, sul caso al confine o su una review del design.

Il beneficio resta evitare scadenze premature delle standard di luglio. Non assumere che l’indagine delle slide precedenti sia stata eseguita da questo agente.

Come risponderesti? Indica:

- quali fatti e decisioni mancano;
- quale ricerca sul sistema serve prima di scegliere la soluzione;
- quali passi e prove giustificherebbero la chiusura;
- chi dovrebbe svolgere le review e quando avrebbe senso conservare una GUIDE.

Motiva i passaggi con il caso. Un elenco di nomi di documenti non dimostra che la modifica sia stata compresa.

## F7
Role: check
Title: Prova: la risposta dell'agente regge?

### Learner content

Nuovo esempio inventato. Il Manuale Avvisi 1.2, p. 12, §2, dice: «Per le richieste urgenti dal 1 agosto, inviare un avviso dopo 10 secondi senza conferma».

Una collega chiede all'agente: «Quando parte l'avviso per una richiesta senza conferma?». L'agente risponde: «Dopo 10 secondi (Manuale Avvisi 1.2)».

Prima di inoltrare la risposta alla collega, indica che cosa controlleresti nel passaggio citato, che cosa chiederesti all'agente di precisare e perché la risposta, così com'è, non basta per una richiesta standard.
