# Difetti: confrontare la quota e contare gli articoli da rilavorare
Course version: 1.0.0-fixture
Delivery mode: self-study
Efficacy: efficacy not verified
Feedback flow: IC1

## Course Value
| Profile | Baseline | Target capability | Teaching contribution | Observable check | Alternative and limits |
|---|---|---|---|---|---|
| P1 — Coordinatori principianti | Il brief dichiara che sanno dividere ma confrontano i difettosi senza considerare quanti articoli siano stati controllati; nessuna diagnosi individuale eseguita. | Individuare il team con il minor tasso osservato e quello con più articoli da rilavorare, motivando le due risposte e delimitando ciò che i dati consentono di dire. | Partire dalle due decisioni; mostrare perché il denominatore cambia il confronto e perché il conteggio resta necessario per quantificare gli articoli. | ai_docs/solutions/courses/ratios/SLIDE_CONTENT.md#s04 | Una scheda con la formula può bastare a chi distingue già le due domande; qui il confronto ragionato collega ciascuna domanda alla misura pertinente. Non si insegna a stimare ore di lavoro o cause dei difetti. |

## S01
Module: M1
Objective: O1
Role: explanation
Title: Prima scegli la domanda
Value contribution: Distinguere la decisione sulla quota di difetti dalla decisione sul numero di articoli da gestire.

### Learner content
Quando confronti due team, «chi ha meno difetti?» può nascondere due domande diverse.

| Domanda | Dato da usare |
|---|---|
| Quale team ha la quota più bassa di difettosi fra gli articoli controllati? | Il tasso osservato: difettosi ÷ controllati. |
| Quale team ha più articoli da rilavorare, se ogni difettoso deve essere rilavorato? | Il numero assoluto di difettosi. |

Il numero assoluto conta gli articoli. Il tasso mette quel numero in relazione con il totale controllato. Nella divisione, il totale controllato è il denominatore: risponde a «difettosi su quanti?». Per esprimere il tasso in percentuale, moltiplica il risultato per 100.

In questo corso imparerai a rispondere separatamente alle due domande. Conterai gli articoli da rilavorare; questi dati non bastano a stimare le ore necessarie.

### Complete explanation
Un conteggio risponde a quanti articoli presentano un difetto. Per valutare la quota osservata, però, occorre conoscere anche quanti articoli sono stati controllati: otto difettosi su cento non esprimono la stessa quota di otto difettosi su un totale diverso. Il denominatore dà al conteggio il suo riferimento. Per organizzare invece il numero di articoli da rilavorare, resta necessario il conteggio, a condizione che tutti i difettosi richiedano rilavorazione. La quota e il conteggio servono quindi a due decisioni distinte. Il numero di articoli non equivale alle ore di lavoro.

### Visual content
Una tabella a due colonne, «Domanda» e «Dato da usare», con le due righe riportate integralmente nel testo visibile. Ordine di lettura: introduzione, prima riga, seconda riga, definizione del denominatore, obiettivo e limite. Nessuna codifica per colore necessaria.

### Transition
Applichiamo entrambe le domande agli stessi dati: otto difettosi contro dodici.

### Sources
- ai_docs/solutions/courses/ratios/sources.md#facts

## S02
Module: M1
Objective: O1
Role: explanation
Title: Otto contro dodici: il totale cambia il confronto
Value contribution: Rendere esplicito il ragionamento che permette di superare il confronto basato sui soli conteggi.

### Learner content
Esempio didattico: tutti gli articoli difettosi indicati devono essere rilavorati.

| Team | Difettosi | Controllati | Calcolo del tasso osservato |
|---|---:|---:|---|
| A | 8 | 100 | 8 ÷ 100 = 0,08 = 8% |
| B | 12 | 300 | 12 ÷ 300 = 0,04 = 4% |

Per confrontare le quote, leggile su una base comune: A ha 8 difettosi ogni 100 controllati; il rapporto di B equivale a 4 difettosi ogni 100. Questa equivalenza non significa che ogni gruppo concreto di 100 articoli di B contenga esattamente 4 difettosi.

**B ha il tasso osservato più basso: 4% contro 8%.** Dire «A è più basso perché 8 è minore di 12» confronta solo i conteggi e perde il totale controllato.

**B ha anche più articoli da rilavorare: 12 contro 8.** Un tasso minore può accompagnarsi a un conteggio maggiore quando i totali controllati sono diversi. Per B, il 4% riguarda 300 articoli; per A, l'8% ne riguarda 100.

### Complete explanation
Il confronto otto contro dodici è corretto se la domanda riguarda il numero di articoli. Non basta se la domanda riguarda la quota di difetti, perché B ha controllato trecento articoli e A cento. La divisione rende confrontabili le quote: 8/100 produce 0,08 e 12/300 produce 0,04. Le percentuali esprimono questi rapporti su una base di cento. B ha dunque una quota osservata minore, ma mantiene dodici articoli difettosi effettivi da rilavorare. Non c'è contraddizione: cambiano la domanda e la misura impiegata. La lettura «ogni cento» esprime una proporzione, non la composizione garantita di ciascun sottogruppo di cento.

### Visual content
Tabella con le quattro colonne e i valori esatti del testo visibile. Sotto, due riquadri testuali: «Tasso osservato minore: B — 4% contro 8%» e «Più articoli da rilavorare: B — 12 contro 8». Leggere la tabella prima dei riquadri. Non disegnare dodici difettosi su cento per B: il suo denominatore è trecento.

### Transition
Le due risposte sono chiare quando disponiamo di conteggi e totali. Vediamo che cosa resta fuori da queste risposte.

### Sources
- ai_docs/solutions/courses/ratios/sources.md#facts

## S03
Module: M1
Objective: O1
Role: explanation
Title: Che cosa puoi concludere, e che cosa manca
Value contribution: Impedire che la percentuale venga usata come conteggio o come spiegazione causale.

### Learner content
Se un rapporto riporta solo «A: 8%; B: 4%», puoi dire che B ha il tasso osservato minore. Non puoi ricavare quanti articoli siano da rilavorare senza conoscere i totali controllati o i conteggi dei difettosi.

Il 4% dice «4 su 100» come rapporto. Non dice «4 articoli in tutto»: nell'esempio B ha 12 difettosi su 300.

Questi dati descrivono gli articoli osservati. Non spiegano **perché** i tassi differiscano e non dimostrano che un team causi meno difetti.

Prima di rispondere:
1. Per la quota, dividi i difettosi per i controllati e confronta i tassi.
2. Per gli articoli da rilavorare, confronta i conteggi, verificando che i difettosi richiedano rilavorazione.
3. Se manca il totale o il conteggio necessario, indica quale dato serve. Non trasformare una quota in un numero di articoli.

Le ore di rilavorazione richiedono altre informazioni sul lavoro necessario per gli articoli: qui rispondiamo soltanto a «quanti articoli?».

### Complete explanation
Una percentuale conserva la relazione fra parte e totale, ma da sola non specifica le loro dimensioni assolute. Per questo il 4% dell'esempio corrisponde a dodici articoli, non a quattro. Se il rapporto nasconde i totali, il confronto dei tassi resta possibile mentre il confronto del numero di articoli può non esserlo. Inoltre, il confronto numerico non contiene una spiegazione delle cause. La conclusione va quindi formulata come confronto osservato, senza attribuire automaticamente il risultato a capacità o comportamenti dei team. Anche un conteggio completo misura qui gli articoli, non il tempo necessario a trattarli.

### Visual content
Scelta solo testo per mantenere vicini il limite e il dato cui si riferisce. Riportare integralmente i paragrafi e la sequenza numerata. La scritta «4% ≠ 4 articoli in tutto» può essere evidenziata usando esattamente questi caratteri, accanto al secondo paragrafo.

### Transition
Ora prova su un caso nuovo. Scrivi le risposte prima di leggere la soluzione nella slide successiva.

### Sources
- ai_docs/solutions/courses/ratios/sources.md#facts

## S04
Module: M1
Objective: O1
Role: check
Title: Caso nuovo: prepara il riepilogo
Value contribution: Richiedere il trasferimento della distinzione fra quota e conteggio a valori non usati nella spiegazione.
Solution: S05

### Learner content
**Caso fittizio.** Devi preparare un riepilogo dei controlli. Tutti i difettosi riportati devono essere rilavorati.

| Team | Difettosi | Controllati |
|---|---:|---:|
| Cedro | 9 | 150 |
| Olmo | 15 | 500 |

1. Quale team ha il tasso osservato di difetti più basso? Mostra entrambi i calcoli in percentuale.
2. Quale team ha più articoli da rilavorare? Indica i due conteggi.
3. Un collega scrive: «Cedro ha meno difettosi, quindi ha anche il tasso minore». Correggi la frase spiegando quale dato trascura.
4. Se ricevessi soltanto le due percentuali, potresti stabilire quale team ha più articoli da rilavorare? Spiega quale informazione chiedere.
5. Questi dati bastano a spiegare la causa della differenza fra i tassi? Motiva in una frase.

Annota le risposte prima di proseguire. La soluzione è nella slide S05.

### Complete explanation
Il compito usa un caso fittizio distinto da quello insegnato. Per il riepilogo occorrono due risposte, una sui tassi e una sui conteggi. Le altre domande chiedono di motivare il confronto e delimitare le conclusioni. Tutti i dati necessari alle prime due risposte sono nella tabella; non occorre ipotizzare tempi di lavorazione o cause. La soluzione è separata per permettere un tentativo autonomo.

### Visual content
Riportare la dicitura «Caso fittizio», la tabella e le cinque domande senza aggiungere risultati, suggerimenti grafici o marcatori di risposta corretta. Ordine di lettura dall'alto verso il basso. La soluzione compare solo in S05.

### Transition
Quando hai scritto le risposte, confronta sia i risultati sia il ragionamento con S05.

### Sources
- ai_docs/solutions/courses/ratios/sources.md#facts — regola del tasso e distinzione fra misure; valori del caso fittizio creati per l'esercizio.

## S05
Module: M1
Objective: O1
Role: solution
Title: Soluzione: Olmo ha meno difetti in proporzione e più articoli
Value contribution: Fornire risposta, ragionamento e recupero mirato agli errori sul denominatore e sui limiti delle percentuali.

### Learner content
1. **Tasso osservato minore: Olmo.** Cedro: 9 ÷ 150 = 0,06 = 6%. Olmo: 15 ÷ 500 = 0,03 = 3%. Il 3% è minore del 6%.
2. **Più articoli da rilavorare: Olmo.** Sono 15, contro i 9 di Cedro. Qui serve il conteggio effettivo.
3. La frase corretta è: «Cedro ha meno articoli difettosi, ma il suo tasso osservato è maggiore: 6% contro 3%». Il collega trascura i totali controllati: 150 per Cedro e 500 per Olmo. Quindici difettosi su cinquecento rappresentano una quota minore di nove su centocinquanta.
4. **Le sole percentuali non bastano per confrontare il numero di articoli.** Chiedi quanti articoli sono stati controllati da ciascun team, oppure direttamente quanti sono i difettosi da rilavorare. Una percentuale descrive una quota, non il numero totale di articoli.
5. **I dati non spiegano la causa.** Descrivono i difetti osservati nei due insiemi di articoli; non dimostrano perché i tassi siano diversi.

Se hai scelto Cedro per il tasso perché 9 è minore di 15, torna a S02: scrivi per ogni team «difettosi su controllati», poi ripeti le due divisioni. Il denominatore è il totale controllato, non il conteggio dell'altro team.

Se hai trasformato il 3% in «3 articoli» o hai scelto il team con la percentuale maggiore per il numero di rilavorazioni, torna a S03 e poi separa due righe: «quota: 6% e 3%»; «articoli: 9 e 15».

Se hai attribuito la differenza alla capacità dei team, rileggi il limite in S03 e riscrivi la conclusione usando «tasso osservato», senza aggiungere una causa.

Nel tuo prossimo riepilogo indica sempre la domanda: **quota di difetti** oppure **numero di articoli da rilavorare**. Riporta la misura corrispondente e i dati che la sostengono.

### Complete explanation
Olmo ha quindici difettosi, ma rapportati a cinquecento controllati producono il 3%. Cedro ha nove difettosi, che rapportati a centocinquanta producono il 6%. Il rapporto minore e il conteggio maggiore appartengono quindi entrambi a Olmo. La correzione della frase del collega richiede il denominatore, non soltanto una risposta diversa. Con le percentuali isolate manca la dimensione assoluta necessaria per contare gli articoli. Nessuna delle operazioni spiega una causa: l'esito resta un confronto descrittivo dei dati osservati. I percorsi di recupero riportano al passaggio che distingue le due domande e invitano a riscrivere il ragionamento.

### Visual content
Testo delle cinque risposte numerate seguito dai tre paragrafi di recupero e dalla frase finale. Evidenziare «Tasso osservato minore: Olmo» e «Più articoli da rilavorare: Olmo» senza separare le etichette dai rispettivi calcoli e conteggi. Nessun contenuto necessario resta nelle note.

### Transition
Fine del modulo M1: usa il denominatore per confrontare le quote e il conteggio per quantificare gli articoli da rilavorare.

### Sources
- ai_docs/solutions/courses/ratios/sources.md#facts — regola e limiti; risultati ottenuti applicando la regola ai valori fittizi di S04.
