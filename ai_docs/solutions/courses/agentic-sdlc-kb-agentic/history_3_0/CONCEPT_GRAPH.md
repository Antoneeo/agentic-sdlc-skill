# Grafo dei prerequisiti e attraversamento del testo

Versione3.0-content. P1 è il percorso comune del D-UC. Gli stati descrivono conoscenza iniziale: nessun concetto diventa PROVATO perché è stato spiegato o simulato. Il grafo didattico ordina comprensione; il grafo KB organizza gli argomenti del progetto.

| Concept ID | Prerequisites | Profile | Initial state | Evidence | Source | Objectives |
|---|---|---|---|---|---|---|
| CO12 | - | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13 | O1 |
| CO11 | CO12 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2 | O1 |
| CO1 | - | P1 | INCERTO | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1 | O1 |
| CO2 | CO1; CO11 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2 | O1 |
| CO3 | CO2 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3 | O2 |
| CO4 | CO3 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4 | O2 |
| CO5 | CO4 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5 | O3 |
| CO6 | CO2 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6 | O4 |
| CO7 | CO6 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8 | O5 |
| CO8 | CO7 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9 | O5 |
| CO9 | CO5; CO8 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11 | O6 |
| CO10 | CO9; CO12 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12 | O7 |

## Traccia ai passaggi effettivi

I locatori Snn rimandano a SLIDE_CONTENT.md#snn; tutti gli incipit seguenti sono in Learner content. Le sottorighe precisano componenti dello stesso concetto, non creano un grafo concorrente. Il primo uso è un ragionamento che richiede la spiegazione, non la sola comparsa della parola. Un’anticipazione comprensibile non vale come conoscenza acquisita.

| Concept and meaning | Explanation locator and incipit | First dependent use locator and incipit | Why order holds |
|---|---|---|---|
| CO12: nota utile e confronto equo | S03, tabella «Nota insufficiente / Nota riutilizzabile» e «La seconda nota permette» | S04 «Invece di riscrivere ogni volta» | Il bisogno di rendere riusabili i requisiti segue l’esempio che ne mostra il valore; ripreso S10. |
| CO11: skill, istruzioni distinte dai risultati | S04 «Una skill è un insieme di istruzioni» e «Il contenuto delle istruzioni» | S05 «Le due skill collaborano» | Prima definizione e limite, poi ripartizione del lavoro; applicazione fisica S07. |
| CO1: contesto e continuità | S06 «Il contesto è il materiale» e «Il file persistente conserva» | S07 «Per lavorare con continuità, apri» | La scelta della cartella usa la distinzione disponibilità/consultazione. |
| CO2: cartella e consultazione mirata | S07 «Le skill sono installate»; S08 «Un indice elenca» | S08 lista «La voce… / La nota… / L’agente riapre» | L’indice è definito prima di usarlo nella stessa unità; la cartella è già introdotta. |
| CO3: artefatto, provenienza e lettura | S13 «conserva prima un artefatto della fonte» e «Conservare il documento non significa» | S14 «collegata alla fonte che la sostiene» | Il claim si ancora a una fonte acquisita e realmente letta. |
| CO4: claim con ambito | S14 «Un claim è una singola affermazione» e tabella | S15 «ai claim che gli appartengono» | Il grafo organizza unità già definite. |
| CO4: grafo degli argomenti | S15 «Un grafo è un insieme» e «La domanda… ci porta» | S16 «Il percorso dalla domanda all’argomento» | Il recupero avviene dopo spiegazione della funzione e del limite del grafo. |
| CO4: risposta con provenienza | S16 citazione «Il Manuale…» e «La risposta esplicita perché» | S17 «Descrivi il claim… e la risposta» | Il nuovo caso chiede lo stesso ragionamento con condizioni diverse. |
| CO5: ambito e successione | S19 tabella e «I periodi non si sovrappongono» | S20 «per lo stesso tipo di richiesta, periodo» | Il confronto delle condizioni precede la classificazione del conflitto. |
| CO5: conflitto mantenuto | S20 «conservarle entrambe come contestate» | S21 «Ora sappiamo perché B e C» | La nuova evidenza risponde a un conflitto già comprensibile. |
| CO5: correzione e propagazione | S21 «La KB conserva il vecchio claim»; S22 «La vecchia decisione… va riesaminata» | S22 «altri documenti che la usano» e «Non aggiornano automaticamente codice» | Superamento è definito prima del lavoro sui dipendenti; il contrasto fra conoscenza e software prepara M4. |
| CO6: beneficio e confini | S25 «Questo è un esempio di Vision» | S26 «Il cambiamento di Orione è L3»; S27 «Il menu serve al beneficio» | Il risultato da giudicare è concreto prima della classificazione e dell’esercizio. |
| CO6: triage | S26 «Il triage classifica» e tabella | S27 «Quale livello assegneresti» | I casi variano effetti, non richiedono una regola non insegnata. |
| CO7: attori e bisogni | S29 «Un use case…» e due esempi | S30 «Per le richieste standard di luglio proponiamo» | Le regole servono attori esplicitati; pannello, email e callback sono introdotti prima. |
| CO7: specifica funzionale | S30 «La specifica funzionale descrive» e tabella | S31 «Il contratto di interfaccia descrive quel percorso» | Comportamenti e decisione aperta precedono flussi e feedback. |
| CO7: interfaccia e flusso | S31 «Una superficie…» e «Nel caso Orione, l’invio» | S32 «L’email usa ancora30 secondi» | Le superfici e il viaggio dello stato esistono per il lettore prima dei loro rischi. |
| CO7: rischio e controllo | S32 «Il modello dei rischi…» e tabella | S33 «capacità necessarie… conseguenze»; S36 casi errore | La ricerca delle capacità serve il comportamento e i rischi già riconosciuti. |
| CO8: capacità ed evidenza | S33 «Il Capability Ledger…» e riscontri | S34 «Nel caso scegliamo di adeguare» | Scelta di riuso fondata sull’indagine dichiarata fittizia. |
| CO8: Impact e design | S34 «L’Impact… Il design…» e decisione al confine | S35 «Un revisore indipendente riceve» | Il reviewer riceve una proposta che il lettore ha visto motivare. |
| CO8: review del design indipendente | S35 «Indipendente significa» e fallback | S36 «Lo sviluppatore implementa il design» | La transizione colloca realizzazione dopo riesame; nessuna implementazione insegnata prima del gate. |
| CO8: prove sul comportamento | S36 tabella e «Un test verde sulla costante» | S37 «confronta modifica, comportamento… risultati dei test» | La review finale usa evidenza definita nella slide precedente. |
| CO8: chiusura e GUIDE | S37 «La chiusura aggiorna» e «Una GUIDE è» | S38 «quando avrebbe senso conservare una GUIDE» | Il criterio di riuso e provenienza precede la decisione richiesta. |
| CO9: responsabilità e modalità | S40 tabella; S41 «Standalone significa» e «devPNT è» | S42 «Come ripartiresti le responsabilità» | Caso Ricevute trasferisce responsabilità già insegnate; non richiede memoria di sigle. |
| CO10: valore nel tempo | S45 confronto settimana; S46 mese; S49 anni | S47 «Confrontali dopo una settimana… mese»; S50 «fra anni» | Il controllo su settimana/mese non richiede ancora la lezione sugli anni; la prova finale segue S49. |
