Per **Cedro manterrei la nota curata**: contiene fonte e motivo, il team la sa ritrovare e la decisione è stabile. Non emerge un bisogno che giustifichi un processo più articolato. Verificherei comunque che il riferimento rimanga accessibile e pertinente quando la nota viene riutilizzata. Una skill non aggiunge automaticamente valore a istruzioni equivalenti già applicate bene (S08–S10, S49).

Per **Delta non considero concluso il lavoro**. Il test della costante dimostra solo una proprietà limitata; non dimostra che pannello e notifica evitino scadenze premature. Inoltre, dai dati disponibili non possiamo decidere se la durata corretta sia 20 o 28 secondi.

Procederei così:

1. **Chiarire il conflitto fra le fonti.** Conserverei manuale e circolare, con provenienza, release, condizioni e riferimenti precisi. Per il manuale abbiamo release 3, §2; per la circolare il locatore va ricavato dal documento, senza inventarlo. Registrerei i due claim come incompatibili nell’ambito indicato. L’arrivo successivo della circolare non ne dimostra la prevalenza: cercherei una rettifica esplicita o un chiarimento autorevole che identifichi quale regola vale e quale passaggio viene eventualmente corretto. Fino ad allora dichiarerei l’incertezza, senza sostituire il fatto con la preferenza del responsabile. Avvierei uno **Spike**, cioè uno studio circoscritto della lacuna, prima di fondare l’implementazione sul nuovo numero (S13–S16, S19–S22, S26).

2. **Confermare beneficio e confini.** La Vision può già registrare il beneficio richiesto: chi segue le consegne deve ricevere uno stato attendibile, senza scadenze premature, sia nel pannello sia nella notifica. Cambiare tutta la navigazione non è giustificato automaticamente da questo obiettivo. La proposta del responsabile va precisata e valutata come estensione esplicita del lavoro, con un proprio beneficio e impatto; non la includerei tacitamente nella correzione. Chiarita la fonte, il cambiamento di scadenza richiede un percorso **L3**, perché modifica comportamento visibile e più superfici, anche se il codice iniziale cambia di una sola riga (S25–S27).

3. **Definire comportamento e design prima di completare l’implementazione.** La specifica deve distinguere attesa, callback valido, scadenza senza callback, callback tardivo ed errore. Serve anche decidere chi prevale se callback e timer scattano esattamente allo stesso istante: le sole durate non risolvono questa domanda. Il responsabile conferma i criteri mancanti; la KB non può attribuirli al manuale. Il contratto di interfaccia descriverà cosa viene mostrato o comunicato su pannello e notifica e, dove coinvolto, l’esito restituito al servizio esterno (S29–S32, S40).

4. **Usare l’indagine già disponibile.** Il caso dà come fatto che il pannello usa un calcolo condiviso e la notifica ha una regola locale: non serve fingere che questa scoperta debba ancora avvenire. La registrerei nel Capability Ledger con i riferimenti reali dell’indagine, se disponibili. È una base per adeguare il calcolo comune e farlo usare anche dalla notifica, evitando una seconda regola da mantenere. L’Impact deve includere entrambe le superfici e le relative prove. La review del design controllerà questa copertura, i casi di confine e il trattamento degli errori prima di proseguire con il codice (S33–S36).

5. **Verificare il risultato osservabile.** Le attese dei test dipenderanno dalla regola risolta e dalla specifica confermata. Se risultasse valida la finestra di 28 secondi, una prova a 20 secondi senza callback dovrà mostrare che entrambe le superfici non annunciano già la scadenza; una prova, per esempio, a 24 secondi dovrà controllare il trattamento di un callback ancora valido. Serviranno poi prove esattamente al confine, dopo la scadenza, in errore e con aggiornamenti che potrebbero lasciare visibile uno stato vecchio. Se prevalesse invece la regola dei 20 secondi, le attese andrebbero formulate su quella base. Verificherei inoltre i consumatori interessati dal calcolo comune per cercare regressioni. Il test verde esistente resta un’evidenza parziale, non la dimostrazione del beneficio (S32, S35).

6. **Chiudere soltanto con evidenze coerenti.** La review finale confronterà implementazione e prove con design, beneficio e rischi; dovrà distinguere ciò che è verificato da ciò che resta aperto. Aggiornerei stato del lavoro, analisi, decisioni e collegamenti alle fonti. Una GUIDE sarebbe giustificata se l’indagine producesse un metodo riutilizzabile per seguire gli stati fino ai loro consumatori: dovrebbe specificare punto di partenza, percorso, verifiche, ambito e riferimenti. “Controllare anche la notifica” sarebbe soltanto un promemoria (S36–S37).

L’assenza di **devPNT non blocca Delta**. Userei il percorso Standalone nella cartella del progetto: fonti conservate, claim e loro storia, indice o grafo per recuperarli, Vision e un’ANALYSIS con specifica, interfacce, rischi, capacità, impatto e design; conserverei anche piano, review ed evidenze delle verifiche. Il grafo aiuta a trovare l’informazione, ma non prova che sia vera. I documenti rendono il ragionamento recuperabile e non aggiornano automaticamente il software (S07, S15, S22, S40–S41).

Nel tempo, il confronto con buone note sarebbe questo:

| Quando | Che cosa si può riutilizzare | Verifica e costo che rimangono |
|---|---|---|
| Fra una settimana, senza cambiamenti | Motivo della scelta e fonte, evitando di ricostruire la decisione. Una buona nota può fornire lo stesso risultato. | Occorre poter riaprire il riferimento e controllarne l’ambito. Un collegamento rotto annulla parte del beneficio. |
| Fra un mese, con una rettifica | I legami fra fonte, claim, decisioni e consumatori indicano cosa riesaminare. Anche note ben mantenute possono conservarli. | Bisogna valutare la rettifica, aggiornare le dipendenze e verificare il software. Legami omessi possono lasciare la notifica incoerente. |
| Fra anni, con un nuovo collega | Ragioni e GUIDE possono rendere ripetibile l’indagine, senza ripartire dal solo numero nel codice. | Fonti, architettura e metodo vanno ricontrollati. Una guida obsoleta può fuorviare; mantenere questa documentazione costa lavoro. |

Il protocollo rende esplicite queste attività ripetute; non dimostra da solo un guadagno di produttività né rende indispensabile una skill. Per sostenere un risparmio servirebbero misure sulle ricostruzioni e omissioni evitate, includendo il costo di manutenzione (S45–S49).

Non mi sono rimasti termini essenziali poco chiari. Restano invece **informazioni mancanti del caso**: autorità risolutiva fra manuale e circolare, criterio al confine temporale e obiettivo concreto della nuova navigazione. Non ho eseguito test né modificato file.

Ho letto soltanto:

- `simulation_2_1/learner_packet.md`
- `simulation_2_1/TASK.txt`

Entrambi nella directory assegnata `C:/Users/apint/Documents/Codex/2026-09-27/che-fine-hanno-fatto-le-skills/work/course-text-review/ai_docs/solutions/courses/agentic-sdlc-kb-agentic/`.
