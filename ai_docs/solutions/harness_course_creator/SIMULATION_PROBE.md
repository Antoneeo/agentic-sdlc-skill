---
description: Prova esplorativa del confronto fra destinatari simulati indipendenti, controllo senza corso e spiegazione corretta.
status: CURRENT
---
# Probe del protocollo di simulazione course_creator

**Data:** 2026-09-27. **Scopo:** esplorare se il confronto proposto in F-058 rende visibili due difetti didattici senza attribuire efficacia umana al risultato. Sono state aperte sei sessioni fresche, una per pacchetto. Ogni sessione è stata istruita a usare soltanto il materiale ricevuto e a non aprire file o cercare altrove. L'autore non ha partecipato come destinatario. I nomi delle sessioni qui sotto identificano input separati, ma il report li riassume e **non conserva i prompt verbatim** né una prova tecnica degli accessi effettivi. Perciò questa è una prova esplorativa, non un collaudo conforme al protocollo di F-058 e non autorizza un PASS diagnostico. La prova su un corso generato dalla skill dovrà conservare prompt e pacchetti integrali e verificare gli accessi.

## Caso A: prerequisito omesso

**Profilo e compito comuni:** principiante senza conoscenze del protocollo fittizio Alda; decidere se una ricevuta con prima tessera Luma, seconda Neri e sigillo 10 sia valida, spiegando il ragionamento.

| Sessione | Materiale ricevuto oltre al profilo e al compito | Esito |
|---|---|---|
| `sim_control` | Nessun corso, legenda o esempio | Non può determinare la validità: non conosce valori e regola del sigillo. |
| `sim_missing_prereq` | Modulo 1: Luma=2, Neri=4, Sora=6. Modulo 2: ruotare la prima tessera, sommarne il valore a quello della seconda, confrontare col sigillo; coincidenza = valida. La regola di «ruota» non compare. | Calcola la forma `ruota(Luma)+4`, ma localizza il blocco prima della somma: non sa quale tessera produca «ruota». Non dichiara valida la ricevuta. |
| `sim_complete_course` | Stessi moduli, con la regola aggiunta: ruota Luma→Sora, Neri→Luma, Sora→Neri. | Conclude valida: Sora=6, Neri=4, totale 10 uguale al sigillo. |

**Limite del caso:** il prompt del destinatario difettoso diceva esplicitamente di non inventare la regola di «ruota». Questo rafforza l'isolamento del materiale ma facilita il riconoscimento del buco. La prova di prodotto dovrà usare anche un prompt neutro, senza suggerire quale concetto manchi.

## Caso B: spiegazione generica per un principiante

**Profilo e compito comuni:** persona che sa addizioni, moltiplicazioni e divisioni elementari, ma non conosce programmazione né il protocollo fittizio Lira; decidere se per `t=3` il varco si apre e spiegare perché.

| Sessione | Materiale ricevuto oltre al profilo e al compito | Esito |
|---|---|---|
| `sim_generic_control` | Nessun corso, legenda o esempio | Non può collegare `t` all'apertura del varco. |
| `sim_generic_explanation` | «Il normalizzatore applica n(t)=2t+1. Il gate residuo accetta se n(t) mod 4 = 3. In tal caso il varco si apre.» | Calcola `n(3)=7`, ma segnala che «mod 4» non è spiegato al profilo; non attribuisce al modulo la capacità di decidere il risultato. Nominati anche «normalizzatore» e «gate residuo» come termini oscuri. |
| `sim_explained_course` | Calcolo in parole: raddoppia `t`, aggiungi 1; per `t=3` ottieni 7. Dividi per 4 e guarda il resto; 7 diviso 4 dà resto 3. `mod 4` indica quel controllo; il varco si apre se il resto è 3. | Conclude che il varco si apre. Segnala comunque che `n(t)` e `mod 4` possono restare notazioni poco familiari, anche se l'esempio consente questo compito. |

## Ruling e uso del risultato

Nei due casi il controllo non risolve il compito, la versione difettosa fa emergere il punto preciso in cui la spiegazione si interrompe, e la versione corretta permette la risposta. I risultati suggeriscono una **fattibilità diagnostica esplorativa** su due esempi artificiali; la prova non soddisfa ancora il contratto di tracciabilità e isolamento. La segnalazione residua del corso Lira corretto mostra che una risposta giusta non equivale a una spiegazione interamente chiara.

Questa prova non misura apprendimento umano, generalizzazione, durata della conoscenza o qualità di un corso reale. I simulatori sono modelli che possono conoscere già matematica e notazioni; i prompt dichiarano il profilo e limitano il materiale, ma non cancellano l'addestramento. Prima di dichiarare diagnostico il PASS di un corso prodotto dalla skill, conservare i pacchetti effettivi, verificare accessi simmetrici e ripetere prove con compiti per cui il controllo non riesce già. Se il controllo riesce, registrare il confronto come inconcludente.

## Probe aggiuntivo: ordinamento dei moduli

Sono state aperte quattro sessioni fresche e separate: un autore con la skill, un autore senza la skill, un destinatario con la spiegazione prodotta e un controllo senza spiegazione. Le sessioni non hanno scritto file. L'autore con la skill ha consultato il contratto didattico e la documentazione ufficiale Python su `graphlib`; entrambi gli autori hanno prodotto una spiegazione utilizzabile di dipendenze, cicli e ordine. Il compito di trasferimento chiedeva se fosse valido l'ordine `generateConfig, bootAPI, warmCache, runSmoke` con dipendenze `generateConfig → bootAPI`, `warmCache → bootAPI`, `bootAPI → runSmoke`, e cosa succedesse aggiungendo `runSmoke → generateConfig`.

Il destinatario con corso e il controllo senza corso hanno risposto entrambi correttamente: l'ordine proposto anticipa `bootAPI` rispetto a `warmCache`; un ordine valido pone entrambe le preparazioni prima di `bootAPI`; il nuovo arco introduce un ciclo. Il controllo ha indicato soltanto un'incertezza sul significato della freccia. Pertanto il confronto è **inconcludente** sull'incremento di comprensione prodotto dal corso. Il successo del destinatario non è un PASS diagnostico e non sostiene un'affermazione di efficacia umana. I prompt e i pacchetti integrali non sono conservati in questo report: anche questa prova resta esplorativa e non soddisfa il protocollo verbatim di `simulation.md`. Per una prova conforme serve congelare materiale e criteri prima del test, conservare gli input esatti e usare un compito che il controllo non risolva già, senza pilotare la risposta.
