# Simulazione diagnostica del testo 2.1-content
Status: completed
Course version/hash: 2.1-content / fc53e0427a06b794f02fa3fb908371b3448f58b58383495f742619e11336f4a3
Efficacy: efficacy not verified

## Protocollo
Profilo P1, medesimo TASK.txt di trasferimento Cedro/Delta, sessioni fresche senza storia e modello/effort ereditati senza override. Corso: /root/text21_learner; controllo: /root/text21_control. Il primo legge learner_packet.md e TASK.txt, il secondo soltanto TASK.txt. Nessun repository o web autorizzato. I limiti erano istruiti, non enforced da un sandbox dedicato. Entrambi dichiarano solo le letture ammesse; il parent non ha esportato qui l'intero trace interno degli strumenti e non certifica isolamento tecnico. Dopo la risposta è stato autorizzato solo il salvataggio verbatim.

Pacchetto ricavato dal testo Learner content e dalle transizioni, escludendo le unità solution e l'autoconfronto di S44. Esempi svolti didattici conservati; chiavi dei check escluse. Compito, criteri e hash congelati prima delle risposte in simulation_2_1. Prompt esatti e nomi di sessione in PROMPTS.json, risposte in learner_response.md e control_response.md. Il revisore del punteggio è l'autore del corso, non cieco; non è un test statistico.

## Risultati contro i criteri congelati
| Criterio | Con corso | Controllo | Evidenza |
|---|---|---|---|
| K1 note sufficienti Cedro | 1 | 1 | Entrambi conservano la nota senza processo aggiuntivo imposto. |
| K2 conflitto e ambito | 1 | 1 | Entrambi rifiutano la sola recenza; il controllo distingue anche una proposta provvisoria da verità della fonte. |
| K3 rischio significativo e confine | 1 | 0 | Corso nomina ragione del L3 e navigazione separata; controllo separa lo scope ma non esplicita una classificazione significativa o equivalente motivata dal rischio. |
| K4 riuso e consumatori | 1 | 1 | Entrambi trattano la regola locale e motivano il possibile riuso. |
| K5 sequenza e review | 1 | 0 | Corso distingue review design prima del codice e review finale; controllo dà prove concrete ma non rende espliciti quei due passaggi. |
| K6 responsabilità/modalità | 1 | 1 | Entrambi separano fatto, decisione e prove e proseguono senza devPNT nel progetto. |
| K7 riuso temporale condizionato | 1 | 1 | Entrambi confrontano note, collegamenti e manutenzione senza percentuali inventate. |
| K8 GUIDE condizionale/limiti | 1 | 0 | Corso motiva GUIDE riutilizzabile; controllo non la discute, pur dichiarando correttamente limiti e prove non eseguite. |

Totali secondo la rubrica fissata: corso 8/8; controllo 5/8. Il controllo è comunque sostanzialmente adeguato su molte decisioni. K3 e K8 richiedono elementi del protocollo non domandati con quei nomi nel brief: la differenza può riflettere salienza e conoscenza del protocollo, non maggiore capacità generale. Non si conclude superiorità generale o apprendimento causato dal corso. Un tentativo per condizione, agenti già competenti e valutazione non cieca limitano fortemente il risultato.

## Esito utilizzabile
Nessun blocco di comprensione emerso nel tentativo con il testo; il lettore cita passaggi pertinenti e conserva le incertezze. Questo sostiene una diagnosi circoscritta di leggibilità/applicabilità del materiale. La review semantica resta necessaria. Non sono state eseguite prove con persone, né misure di ritenzione o produttività. La simulazione 1.0-draft resta storica; il report 2.0 indicava correttamente not run. Nessun PPTX generato.

## Correzione successiva alla coppia diagnostica
La review finale ha rilevato che S36/S38/S39 non esplicitavano indipendenza del revisore e fallback dichiarato. Il testo è stato corretto dopo la simulazione: gli hash del pacchetto e il corso/hash in questo report identificano la versione effettivamente testata, non il testo finale successivo. Non si trasferisce il punteggio al nuovo criterio di indipendenza; verifica finale affidata alla re-review semantica. Il difetto non è emerso nella coppia, mostrando il limite del test.
