# Assegnare una priorità motivata
Course version: 1.0
Delivery mode: self-study
Efficacy: efficacy not verified
Feedback flow: not available

## Course Value
| Profile | Baseline | Target capability | Teaching contribution | Observable check | Alternative and limits |
|---|---|---|---|---|---|
| Nuovi coordinatori | Conoscono il ticket, non questa politica; alcuni usano il tono come criterio, secondo il brief | Motivare la priorità oppure riconoscere informazioni mancanti e casi non coperti | Collegare i dati alle condizioni, separare ignoto da assente e incompletezza da mancata copertura | SLIDE_CONTENT.md#s07 | La scheda delle categorie basta per casi immediati; qui si esplicita il ragionamento sui confini e sulle informazioni mancanti |

## S01
Module: M1
Objective: O1
Role: explanation
Title: Dal racconto del cliente ai fatti operativi
Value contribution: Rendere riconoscibili gli elementi che motivano una priorità.

### Learner content
Un ticket può essere scritto con rabbia e descrivere un problema lieve. Per applicare questa politica, cerca tre informazioni:

1. **Impatto:** quale funzione è interessata? Una funzione principale è bloccata, oppure il difetto è soltanto estetico e non ostacola il lavoro?
2. **Estensione:** sono coinvolti tutti gli utenti o una parte?
3. **Soluzione temporanea:** esiste una soluzione temporanea praticabile?

Il tono e l'importanza commerciale del cliente **non cambiano da soli la categoria**. Non sostituiscono nessuna di queste informazioni.

Esempio fittizio: «È una vergogna!» accompagna un difetto di colore, confermato esclusivamente estetico e senza impatto operativo. La rabbia non trasforma il difetto in un blocco di una funzione principale. Per la decisione occorre descrivere i fatti, non l'intensità delle parole.

Leggi le otto slide nell'ordine indicato; prova gli esercizi prima di leggere le soluzioni. Tutti i casi sono fittizi. Nessun dato reale è richiesto.

### Complete explanation
Il punto di partenza è un ticket, oggetto già familiare. Separare il linguaggio dal problema permette di cercare informazioni confrontabili con la politica. Le tre domande servono a descrivere il caso, non creano nuove categorie. L'esempio mostra soltanto perché il tono non è un criterio sufficiente: non invita a dedurre dal tono né l'impatto né gli altri dati.

### Visual content
Solo testo: elenco numerato delle tre informazioni, seguito dall'esempio. L'ordine prepara il confronto con le condizioni della slide successiva.

### Transition
Ora che sai quali fatti cercare, vediamo quali combinazioni consentono di assegnare P1, P2 o P3.

### Sources
- ai_docs/solutions/courses/tickets/policy.md#priorita

## S02
Module: M2
Objective: O2
Role: explanation
Title: Le categorie dipendono da condizioni precise
Value contribution: Spiegare le combinazioni necessarie evitando una graduatoria intuitiva basata sull'urgenza percepita.

### Learner content
| Categoria | Condizioni della politica |
|---|---|
| P1 | Una funzione principale è bloccata **per tutti** e **non esiste** una soluzione temporanea praticabile. |
| P2 | Una funzione principale è bloccata **per una parte** degli utenti; **oppure** è bloccata per tutti ma **esiste** una soluzione temporanea praticabile. |
| P3 | Difetto **esclusivamente estetico**, senza impatto sull'operatività. |

In P1 le condizioni devono essere tutte vere. In P2 ci sono due percorsi: basta che il caso corrisponda a uno dei due. P3 non significa «tutto ciò che non è P1 o P2»: richiede assenza di impatto operativo e natura esclusivamente estetica.

Coppia di esempi fittizi con dati accertati: una funzione principale è bloccata per tutti gli utenti. Se non esiste una soluzione temporanea praticabile, è **P1**. Se esiste, è **P2**: il blocco rimane, ma cambia una condizione decisiva della politica.

La politica non stabilisce tempi di risposta o SLA: una categoria non autorizza a promettere un tempo.

### Complete explanation
La congiunzione «e» in P1 impedisce di decidere sulla sola base del blocco. L'«oppure» in P2 descrive due situazioni sufficienti previste dalla fonte. Nella coppia di esempi si mantiene costante il blocco per tutti per rendere visibile l'effetto della soluzione temporanea. Non viene proposta una definizione aziendale di praticabilità: gli esempi la dichiarano come dato accertato.

### Visual content
Tabella testuale con tre righe. La coppia di esempi va letta dopo la tabella, mantenendo visibili le parole «tutti» e «soluzione temporanea praticabile».

### Transition
Le condizioni funzionano quando i dati sono noti. Che cosa fare quando un ticket lascia un punto in sospeso?

### Sources
- ai_docs/solutions/courses/tickets/policy.md#priorita

## S03
Module: M3
Objective: O3
Role: explanation
Title: Informazione mancante e caso non coperto sono due situazioni diverse
Value contribution: Impedire che un vuoto informativo o una lacuna della politica diventi una categoria inventata.

### Learner content
**Se manca un dato, non completarlo per intuizione.** Quando impatto, estensione o disponibilità di una soluzione temporanea non sono noti, richiedi le informazioni mancanti e mantieni la classificazione provvisoria. La politica non indica una categoria numerica predefinita per l'attesa: non inventarla.

Esempio fittizio: è confermato il blocco di una funzione principale per tutti; non si sa se esista una soluzione temporanea praticabile. Chiedi: «Esiste una soluzione temporanea praticabile?». Intanto la classificazione resta provvisoria. **Non sapere se esiste non significa sapere che non esiste.** La risposta distingue P1 da P2.

**Se i dati sono noti ma nessuna definizione si applica, invia il caso al responsabile per decisione.** Esempio fittizio: una funzione principale è rallentata ma non bloccata, per tutti; nessuna soluzione temporanea praticabile; il rallentamento ostacola il lavoro. Non è P3, perché c'è impatto operativo. P1 e P2 richiedono un blocco: non forzare una delle tre categorie.

La politica non definisce in dettaglio «funzione principale» e «praticabile». Non inventare criteri per rendere il caso classificabile: chiarisci le informazioni mancanti; per casi non coperti, chiedi la decisione al responsabile.

### Complete explanation
Il caso incompleto può diventare classificabile quando arriva una risposta. Il caso non coperto, invece, è descritto ma non soddisfa le condizioni disponibili: occorre la decisione del responsabile. Nei due esempi il coordinatore riconosce il limite di ciò che può concludere. La provvisorietà non è una quarta priorità con regole o SLA propri.

### Visual content
Solo testo con due paragrafi distinti: «manca un dato» e «nessuna definizione si applica». Gli esempi seguono ciascuna regola.

### Transition
Uniamo adesso raccolta dei dati, confronto con la politica e motivazione in una risposta completa.

### Sources
- ai_docs/solutions/courses/tickets/policy.md#priorita

## S04
Module: M2
Objective: O2
Covers: M1/O1; M3/O3
Role: explanation
Title: Come costruire una motivazione controllabile
Value contribution: Mostrare il passaggio dai fatti alla decisione senza saltare condizioni.

### Learner content
**Caso fittizio completo:** una funzione principale è bloccata per una parte degli utenti. È accertato che non esiste una soluzione temporanea praticabile. Il cliente è importante commercialmente e scrive con rabbia.

Una motivazione possibile è: «Assegno **P2**: una funzione principale è bloccata per **una parte degli utenti**, situazione prevista da P2. L'assenza di una soluzione temporanea non basta a farne P1, che richiede anche il blocco per tutti. Tono e importanza commerciale non cambiano da soli la categoria».

Per esercitarti, usa questa traccia didattica:
**decisione → fatti decisivi → condizione della politica**.
Se manca un dato, scrivi invece **classificazione provvisoria → dato mancante → domanda precisa**. Se il caso non è coperto, indica quali condizioni non corrispondono e rinvia al responsabile.

La traccia aiuta a rendere leggibile il ragionamento; non è un nuovo obbligo aziendale.

### Complete explanation
Nel caso completo la parte di utenti coinvolta soddisfa il primo percorso di P2. Non serve trasformare l'assenza di soluzione in una regola generale di P1. La motivazione fa vedere sia perché P2 si applica, sia perché l'argomento plausibile per P1 è insufficiente. La traccia per gli altri esiti consente di dichiarare ciò che manca senza nasconderlo dietro una categoria definitiva.

### Visual content
Solo testo. La risposta modello precede la traccia, così che ogni elemento astratto abbia già un esempio.

### Transition
Ora prova a decidere senza guardare subito la soluzione.

### Sources
- ai_docs/solutions/courses/tickets/policy.md#priorita

## S05
Module: M1
Objective: O1
Covers: M2/O2
Role: check
Solution: S06
Title: Prova — quale fatto cambia la categoria?
Value contribution: Verificare la decisione motivata e il rifiuto del tono come criterio autonomo.

### Learner content
**Esercizi fittizi.** Rispondi prima di leggere S06. Per ciascun caso scrivi categoria, fatti decisivi e motivo per cui il tono non determina la risposta.

**A.** Un'etichetta ha un colore sbagliato per tutti gli utenti. È confermato che il difetto è esclusivamente estetico, senza impatto sull'operatività; non esiste una soluzione temporanea praticabile. Il cliente è furioso.

**B.** Una funzione principale è bloccata per tutti. Non esiste una soluzione temporanea praticabile. Il cliente è tranquillo.

**C.** Tutti i fatti di B restano uguali, ma ora è disponibile una soluzione temporanea praticabile. Qual è la categoria e perché cambia?

### Complete explanation
Il confronto fra A e B separa il tono dall'impatto. Il passaggio B–C richiede di applicare una condizione modificata e non soltanto ricordare una definizione. Le risposte ragionate sono nella slide seguente.

### Visual content
Solo testo, tre casi distinti A, B e C. La soluzione è separata nella slide successiva per consentire il tentativo autonomo.

### Transition
Fermati e scrivi le tre risposte; poi confrontale con S06.

### Sources
- ai_docs/solutions/courses/tickets/policy.md#priorita

## S06
Module: M1
Objective: O1
Covers: M2/O2
Role: solution
Title: Soluzioni — le condizioni contano più del tono
Value contribution: Correggere gli errori legati al tono e alla combinazione delle condizioni.

### Learner content
**A → P3.** Il difetto è esclusivamente estetico e non ha impatto operativo. Il fatto che riguardi tutti non basta a renderlo P1: manca il blocco di una funzione principale. La rabbia non modifica da sola la categoria.

**B → P1.** Sono presenti insieme funzione principale bloccata, tutti gli utenti e assenza di soluzione temporanea praticabile. Il tono tranquillo non riduce la categoria.

**C → P2.** Rimane il blocco per tutti, ma ora esiste una soluzione temporanea praticabile: è il secondo percorso di P2. La differenza da B è questo dato operativo.

Se hai scelto seguendo il tono, rileggi S01 e riscrivi ogni risposta eliminando gli aggettivi sul cliente. Se hai scelto P1 per A o per C, rileggi S02 e sottolinea tutte le condizioni necessarie di P1: individua quella che il caso non soddisfa. Se hai scritto soltanto una sigla, aggiungi la frase «perché…» con i fatti del caso.

### Complete explanation
Le soluzioni rendono esplicite anche le alternative sbagliate più plausibili: estensione a tutti scambiata per P1, rabbia scambiata per priorità e blocco per tutti considerato senza controllare la soluzione temporanea. Il recupero richiede di correggere il ragionamento scritto, non solo di sostituire la sigla.

### Visual content
Solo testo, nell'ordine A–B–C della verifica, con recupero dopo le risposte.

### Transition
Nella prossima prova dovrai anche riconoscere quando una categoria definitiva non è giustificata.

### Sources
- ai_docs/solutions/courses/tickets/policy.md#priorita

## S07
Module: M3
Objective: O3
Covers: M1/O1; M2/O2
Role: check
Solution: S08
Title: Trasferimento — decisione, domanda o rinvio?
Value contribution: Richiedere l'uso della politica in casi nuovi senza suggerire un'etichetta per ciascuno.

### Learner content
**Tre nuovi ticket fittizi.** Per ciascuno scrivi una breve nota: decisione consentita, fatti che la sostengono e, se necessaria, domanda precisa o azione successiva. Non inventare informazioni.

**D.** «Non funziona, risolvete subito! Siamo il vostro cliente più importante». Non ci sono altri dati confermati. Che cosa devi sapere prima di motivare una categoria?

**E.** Una funzione secondaria è completamente bloccata per tutti gli utenti. Il lavoro ne risente; non è un difetto estetico. È confermato che non esiste una soluzione temporanea praticabile. Tutti questi dati sono noti. Puoi assegnare una delle tre categorie previste?

**F.** Una funzione principale è bloccata per una parte degli utenti; esiste una soluzione temporanea praticabile. Il cliente è irritato. Scrivi la categoria motivata. Poi cambia un solo fatto: il blocco riguarda tutti, mentre la soluzione rimane praticabile. La categoria cambia? Spiega.

### Complete explanation
D richiede di riconoscere tutte e tre le informazioni non disponibili. E verifica il confine della politica con un tipo di funzione diverso dagli esempi precedenti. F verifica che i due percorsi di P2 possano produrre la stessa categoria e che il tono non intervenga da solo. Le risposte sono separate in S08.

### Visual content
Solo testo, casi D–E–F separati. Le richieste di motivazione e azione fanno parte del testo visibile.

### Transition
Completa le note prima di continuare: S08 contiene risposte e indicazioni per correggerle.

### Sources
- ai_docs/solutions/courses/tickets/policy.md#priorita

## S08
Module: M3
Objective: O3
Covers: M1/O1; M2/O2
Role: solution
Title: Soluzioni e promemoria operativo
Value contribution: Chiudere il percorso con risposte complete e recupero mirato.

### Learner content
**D → classificazione provvisoria; richiedere informazioni.** Non conosciamo impatto, estensione e soluzione temporanea. Domande possibili: «Quale funzione è interessata e che cosa non riuscite a fare? È una funzione principale bloccata? Il problema riguarda tutti gli utenti o una parte? Esiste una soluzione temporanea praticabile?». Né irritazione né importanza commerciale forniscono queste risposte. Non c'è una categoria numerica predefinita per l'attesa nella politica.

**E → responsabile per decisione.** I dati sono completi, ma il caso non è coperto: P1 e P2 riguardano una funzione principale bloccata; qui la funzione è secondaria. P3 richiede un difetto esclusivamente estetico senza impatto operativo, e qui il lavoro ne risente. Non assegnare P3 solo perché P1 e P2 non si applicano.

**F → P2 in entrambe le situazioni.** Nel primo caso basta il blocco della funzione principale per una parte degli utenti. Nel secondo sono coinvolti tutti, ma esiste ancora una soluzione temporanea praticabile: si applica l'altro percorso di P2. L'irritazione non cambia da sola la categoria.

**Correggi il ragionamento:** se in D hai assegnato una categoria definitiva, rileggi S03 e separa fatti noti e ignoti prima di riscrivere le domande. Se hai classificato E come P3, rileggi il limite di P3 in S02 e spiega quale condizione manca. Se in F hai cambiato categoria, confronta i due percorsi di P2 in S02 e riscrivi le due motivazioni.

Da portare nel prossimo ticket: **cerca i fatti, confronta le condizioni, motiva la decisione; chiedi ciò che manca e mantieni la classificazione provvisoria; rinvia al responsabile i casi non coperti.** Non promettere tempi sulla base di questa politica: non contiene SLA.

Corso versione 1.0; efficacia didattica non verificata. Canale di feedback non disponibile nel materiale fornito.

### Complete explanation
D non è una prova dell'assenza di impatto: è una descrizione insufficiente. E non si risolve raccogliendo di nuovo dati già espliciti, ma riconoscendo un limite della politica. F mostra che un fatto cambiato non implica necessariamente una categoria diversa: va confrontata l'intera combinazione con la fonte. Le correzioni rinviano alla spiegazione pertinente e richiedono una nuova motivazione.

### Visual content
Solo testo. Soluzioni nell'ordine D–E–F, poi recupero e promemoria finale.

### Transition
Fine del corso. Rivedi le risposte non motivate e confronta ogni tua conclusione con una condizione esplicita della politica.

### Sources
- ai_docs/solutions/courses/tickets/policy.md#priorita
