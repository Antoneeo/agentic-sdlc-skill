# Piano del corso: lavorare con kb-agentic e agentic-sdlc

Course version: 3.0-content
Content contract: slide-content-v1
Efficacy: efficacy not verified
Feedback flow: IC1

## Pubblico e formato

P1 è il percorso comune per una persona del team software che usa agenti, sviluppatore o responsabile tecnico. Nessuna conoscenza delle skill è dichiarata PROVATO senza evidenza individuale. La modalità è self-study: Learner content e Transition contengono tutto il ragionamento necessario. Il sorgente dettagliato SLIDE_CONTENT.md è primario; la vista di lettura è derivata dagli stessi blocchi. Ogni esempio Orione è fittizio. La durata dipende dalle pause e dai tentativi; non è stata misurata con persone. Nessun nuovo PPTX viene prodotto prima della definizione finale del testo.

Il corso insegna a distinguere fonte, decisione e prova, e a riconoscere quando una nota curata basta. Il valore non è la memorizzazione delle sigle o l’adozione obbligatoria delle skill. Lo sviluppatore cerca e verifica percorsi; il responsabile giudica beneficio, ambito e decisioni aperte (S25, S29, S34–37, S40–44).

## Obiettivi

- O1: Ritrovare il motivo di una scelta distinguendo contesto, file persistenti e consultazione mirata.
- O2: Ricostruire una risposta dalla fonte al claim con ambito e locatore, organizzato nel grafo degli argomenti.
- O3: Distinguere successione, ambito incompleto e conflitto; usare nuova informazione per correggere senza cancellare la storia.
- O4: Motivare il livello di lavoro attraverso effetti e rischio, beneficio della Vision e decisioni aperte.
- O5: Seguire un cambiamento da bisogni e comportamento a capacità esistenti, design, review, prove e chiusura con conoscenza riusabile.
- O6: Separare fedeltà alle fonti, decisione umana e cambiamento; applicare il metodo in Standalone e riconoscere l’autorità opzionale devPNT.
- O7: Confrontare note curate e protocollo sul medesimo compito a settimana, mese e anni, includendo manutenzione e casi di equivalenza.

## Sequenza

| Module ID | Profile | Objective ID | Concepts | Explanation | Sources | Check | Next |
|---|---|---|---|---|---|---|---|
| M1 | P1 | O1 | CO12; CO11; CO1; CO2 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s01 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s11 | M2 |
| M2 | P1 | O2 | CO3; CO4 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s13 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s17 | M3 |
| M3 | P1 | O3 | CO5 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s19 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s23 | M4 |
| M4 | P1 | O4 | CO6 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s25 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-7 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s27 | M5 |
| M5 | P1 | O5 | CO7; CO8 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s29 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s38 | M6 |
| M6 | P1 | O6 | CO9 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s40 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s42 | M7 |
| M7 | P1 | O7 | CO10 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s45 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-13 | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md#s50 | end |

## Teaching alignment

I criteri seguenti precedono i quesiti della revisione. I rinvii indicano passaggi effettivi della fonte. Le soluzioni seguono il tentativo; S50–51 sono cumulativi. Le riflessioni intermedie nella simulazione costituiscono supporto e non provano apprendimento spontaneo.

| Objectives and use context | Evidence and success criterion | Explanatory bridge | Example or contrast | Support and correction |
|---|---|---|---|---|
| O1: una nuova sessione deve motivare un numero | S11: recupera nota/fonte, ambito e limite. Insufficiente: ricorda la chat o basta salvare tutto | S02–04 spiegano il valore della nota e le istruzioni; S06–09 distinguono conservare, leggere e verificare | Due note S03; note curate equivalenti S10 | S12 motiva il recupero e rimanda a S02–03/S06–07 |
| O2: rispondere su una fonte nuova | S17: claim con condizioni e fonte, tema pertinente e risposta citata. Insufficiente: numero o titolo del file senza ambito | S13 fonte acquisita vs letta; S14 frase atomica e condizioni; S15 ricerca; S16 inclusione del caso | Manuale Orione e Manuale Avvisi: numeri e tipi diversi | S18 distingue funzione di fonte, claim, tema e risposta; rinvia S14–16 |
| O3: due regole diverse | S23: distingue periodi separati e ambito mancante, corregge solo con nuova informazione. Insufficiente: vince l’ultimo | S19 confronta periodi; S20 rende simmetrico il conflitto; S21 mostra cosa cambia una rettifica; S22 separa conoscenza e codice | B/C conflitto, D corregge il tipo di C; variante agosto/settembre | S24 spiega le condizioni che cambiano il verdetto e rinvia a S19–21 |
| O4: scegliere lavoro e confini | S27: livelli motivati dagli effetti, confine temporale aperto e menu fuori scope. Insufficiente: una riga=L1 | S25 beneficio osservabile e non-obiettivo; S26 rischio e incertezza | Refuso isolato vs stato prematuro; fonte contestata | S28 separa L1/L3, indagine e decisione; rimanda a S25–26 |
| O5: giudicare una proposta di chiusura | S38: cerca capacità, distingue regole da implementazione, colloca review indipendenti e prove multisuperficie, motiva GUIDE. Insufficiente: costante verde o elenco di sigle | S29–32 collegano attori, regole, flussi e rischi; S33–34 evidenza→riuso→design; S35–37 review→prove→chiusura | Pannello corretto/email vecchia; urgenti da preservare; capacità non trovata come limite di ricerca | S39 motiva sequenza e recupero; S35 per indipendenza, S36 per osservabilità |
| O6: passare dalla fonte al proprio cambiamento | S42: responsabilità distinte, design Standalone, limite del manuale e prova sulla ricevuta. S44 applicazione facoltativa. Insufficiente: KB decide layout o devPNT necessario | S40 tre responsabilità; S41 una modalità completa e governance opzionale | Caso nuovo Ricevute: data richiesta vs data stampa | S43 risposta ragionata; S44 criterio fonte/decisione/prova con rinvii precedenti |
| O7: scegliere una disciplina nel tempo | S47: parità di informazioni e costo. S50: raccomandazione autonoma su Alba/Bora. Insufficiente: skill indispensabile, recenza decide, rendimenti garantiti | S45 recupero settimana; S46 revisione mese; S49 passaggio anni e controllo della guida | Stesso compito, stessi dati, poi collegamenti non mantenuti; Alba stabile/Bora complesso | S48 esplicita costo ed equivalenza; S51 trasferimento; S52 ripresa differita facoltativa |

## Attraversamento effettivo e carico

CONCEPT_GRAPH.md contiene la traccia da ogni concetto alla spiegazione e al primo uso dipendente, con incipit distinti anche nella stessa unità. È il riferimento per l’ordine: i concetti dichiarati nella tabella dei moduli non certificano la comprensibilità dei passaggi.

Le 52 unità sono già segmentate nel sorgente; il massimo del testo Learner content nella stesura verificata è152 parole. Le tabelle contengono dati da tenere vicini alla spiegazione. Un futuro renderer deve conservare tutto il testo visibile e le transizioni; qualsiasi ulteriore divisione richiede aggiornamento dei locatori e nuovo controllo di sequenza.

## Fonti e verifica

Le 12 fonti nello snapshot del27 settembre sono state riaperte e i loro hash controllati. sources.md governa le affermazioni sulle skill; i numeri di Orione sono dati narrativi dichiarati. La review del design e quella del materiale sono separate. SIMULATION_REPORT.md identifica versione, lettore P1, controllo senza corso, isolamento e risultati; il confronto non dimostra efficacia umana né causalità della skill. Il field test di course-creator è descritto nello stesso report.
