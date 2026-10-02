Non ho ricevuto materiale didattico. Uso soltanto i fatti del caso, senza aver eseguito prove né consultato altre fonti.

## Cedro

Cedro conserva già una decisione stabile, con fonte e motivo, che il team sa ritrovare. Questo basta per il bisogno descritto: non introdurrei una struttura più complessa solo perché il team usa agenti.

Manterrei quella decisione nel luogo condiviso già utilizzato, con un riferimento stabile. Se mancano, aggiungerei data e ambito di validità, così da capire quando riesaminarla. Non posso concludere che Cedro abbia bisogno di un nuovo sistema documentale; posso soltanto riconoscere che, per questa decisione, conserva già le informazioni essenziali.

## Delta: decidere prima che cosa correggere

L’obiettivo operativo è evitare scadenze premature. Distinguerei tre questioni:

1. **Conflitto fra prescrizioni.** Il manuale indica 20 secondi; la circolare successiva ne indica 28 nelle stesse condizioni. La data più recente, da sola, non dimostra che la circolare sostituisca il manuale. Occorre identificare chi può chiarire la precedenza e ottenere una decisione esplicita.
2. **Incoerenza nell’implementazione.** L’indagine data per svolta mostra che pannello e notifica non dipendono dalla stessa regola: il primo usa un calcolo condiviso, la seconda una regola locale. È una base concreta per delimitare l’analisi, ma non dimostra ancora come si comportino entrambi in esecuzione.
3. **Proposta di cambiare tutta la navigazione.** Non emerge un legame necessario con il difetto delle scadenze. La registrerei separatamente, chiedendo quale problema risolverebbe e con quali criteri di successo. Non la includerei automaticamente nella correzione.

Per evitare scadenze premature si può proporre un’applicazione provvisoria dei 28 secondi, ma va qualificata come scelta operativa temporanea, approvata dal responsabile competente, non come interpretazione ormai certa delle fonti. Prima andrebbero chiariti gli effetti di un eventuale ritardo e la possibilità di revocare la scelta. Se manca l’autorità per decidere, il conflitto resta aperto: non lo risolverei silenziosamente nel codice.

## Decisioni e prove necessarie

Registrerei innanzitutto:

- le due prescrizioni, con riferimenti esatti, date, ambito e testo rilevante;
- il conflitto ancora irrisolto e la persona incaricata di chiarirlo;
- l’eventuale decisione provvisoria, chi la autorizza, il motivo e quando riesaminarla;
- il comportamento atteso di pannello e notifica, compreso l’istante da cui parte il conteggio e ciò che deve accadere al limite;
- il perimetro della correzione e la proposta sulla navigazione lasciata come lavoro distinto.

Poi esaminerei la modifica dell’agente. Un test verde consente soltanto di dire che quel test passa nelle condizioni in cui è stato eseguito. Non dimostra che la costante cambiata governi entrambi i percorsi, che il test rappresenti il requisito corretto o che il comportamento precedente fosse riprodotto.

Le verifiche dovrebbero rispondere a domande concrete:

- Quali utilizzatori dipendono dal calcolo condiviso? Cambiarlo produce effetti anche fuori da pannello e notifica?
- La costante modificata raggiunge la regola locale della notifica?
- Il difetto si riproduce con la versione precedente e il controllo fallisce per la ragione attesa?
- Entrambi i percorsi rispettano il valore deciso prima, al momento e dopo il limite?
- A parità di condizioni, pannello e notifica danno risultati coerenti?
- Le condizioni diverse, che non richiedono la modifica, conservano il comportamento previsto?

Valuterei se far usare alla notifica la stessa regola del pannello. Sarebbe utile se esprimono davvero la stessa politica; non basta che oggi abbiano lo stesso numero. In alternativa, renderei esplicita la ragione della separazione e verificherei entrambi i percorsi.

La prova finale dovrebbe includere anche l’integrazione tra i componenti interessati, con una traccia dei risultati collegata alla versione verificata. Distinguerei sempre prove proposte, prove eseguite ed esiti effettivamente osservati.

## Chiusura e conservazione

Chiuderei la correzione quando il comportamento atteso è stato deciso, i percorsi coinvolti sono stati corretti e verificati, gli effetti sugli altri utilizzatori sono stati valutati e il rilascio ha un responsabile e una modalità di recupero in caso di problema. Dopo il rilascio servirebbe un controllo del comportamento nell’ambiente di destinazione, proporzionato al rischio.

Se si è proceduto con una decisione temporanea, la correzione operativa può essere completata secondo i criteri concordati, ma il chiarimento delle prescrizioni deve restare aperto e assegnato. La chiusura non deve far sparire questa dipendenza.

Poiché devPNT non è configurato, conserverei il lavoro negli strumenti condivisi già disponibili:

- **Repository:** codice, test e decisione tecnica versionata.
- **Documentazione condivisa:** fonti, decisione applicabile, motivazione e stato del conflitto.
- **Registro di lavoro del team:** problema, responsabili, criteri di accettazione, risultati delle verifiche e collegamenti al rilascio.

Userei collegamenti reciproci e un riferimento principale per ogni informazione, evitando copie divergenti. Non è necessario introdurre devPNT per rendere il lavoro verificabile.

## Che cosa resta riutilizzabile

**Fra una settimana**, un’altra persona o un agente potrebbe riprendere il problema dai criteri di accettazione, dalla decisione sul valore, dai percorsi individuati e dalle prove collegate alla versione corretta. Non dovrebbe ricostruire tutto dalla conversazione.

**Fra un mese, con una nuova rettifica**, servirebbero soprattutto la provenienza della regola, il suo ambito e i collegamenti a codice e test. La nuova decisione dovrebbe indicare quale precedente sostituisce e da quando, preservando la storia. Le prove andrebbero aggiornate e rieseguite: un risultato passato non certifica la nuova versione.

**Fra anni, con un nuovo collega**, resterebbero utili il motivo delle scelte, le alternative scartate, l’evoluzione delle prescrizioni e la distinzione tra ciò che era provvisorio e ciò che è vigente. I test esprimerebbero esempi verificabili del comportamento atteso, mentre la documentazione spiegherebbe perché quel comportamento era stato scelto.

Buone note possono già offrire molto di questo: Cedro ne è un esempio sufficiente per il caso descritto. Il vantaggio di una struttura maggiore, per Delta, dipende da collegamenti mantenuti, stato aggiornato e prove rintracciabili. Avere più documenti o nomi specializzati non garantisce una memoria migliore.

Non mi sono rimasti oscuri termini indispensabili per rispondere. Restano invece non specificati l’autorità della circolare, il significato operativo esatto della scadenza, la copertura del test verde e il ruolo previsto di devPNT; non ho assunto risposte a questi punti.

**Unico file letto:** `C:/Users/apint/Documents/Codex/2026-09-27/che-fine-hanno-fatto-le-skills/work/course-text-review/ai_docs/solutions/courses/agentic-sdlc-kb-agentic/simulation_2_1/TASK.txt`.
