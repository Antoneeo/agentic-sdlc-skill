# Simulazione diagnostica del corso

Status: diagnostic pass; confronto inconcludente per K5 e per efficacia umana
Course version/hash: 1.0-draft; SHA-256 `ca31084af87c493029b8747b3092cd049b8b33919a06e91fe55e5fbadfa0d149` su nomi relativi e byte di `COURSE_PLAN.md`, `sources.md`, `modules/M1.md`–`modules/M7.md` in ordine, separati da NUL.
Profile and objective: P1 (persona del team software che usa agenti); O1–O7.
Conclusion: una simulazione può trovare difetti nella spiegazione, non provare l'efficacia su persone reali.

## Protocollo fissato prima dei test

Due agenti indipendenti in contesti nuovi ricevono lo **stesso compito**. A uno sono consentiti soltanto `COURSE_PLAN.md`, `sources.md` e i sette moduli come pacchetto didattico; al controllo non è fornito il corso. Nessuno dei due riceve Vision, ANALYSIS, grafo di design, risposte attese o output dell'altro. Nessuno consulta Internet o altri file del repository. Entrambi possono rispondere usando la propria conoscenza pregressa, ma devono distinguere i fatti verificati dalle inferenze. L'accesso agli strumenti è identico; la differenza ammessa è il pacchetto corso. L'autore valuterà le risposte senza chiedere agli agenti di dare un voto a se stessi.

**Compito identico, da copiare letteralmente nei due prompt:**

> Sei una persona del team software che usa agenti AI. Spiega a un nuovo collega, usando Orione come esempio ipotetico, che cosa cambia fra usare un agente in chat senza un metodo di progetto e usare `kb-agentic` con `agentic-sdlc`. Segui un manuale dal suo ingresso fino a una risposta citabile, descrivi come gestire due regole in conflitto, poi accompagna la modifica del timeout dal beneficio atteso alla chiusura. Distingui Standalone e devPNT. Confronta lo stesso progetto dopo una settimana, un mese e anni, indicando a ogni tappa quale ricostruzione si evita e quale verifica resta necessaria. Spiega anche come useresti in sola lettura un documento del tuo progetto per iniziare un caso analogo, senza inviarlo qui. Indica i passaggi che ti restano poco chiari e i materiali che hai usato. Non inventare fatti sulle skill quando non hai una fonte.

**Criteri fissati prima delle risposte:**

| ID | Evidenza di comprensione richiesta | Blocco diagnostico |
|---|---|---|
| K1 | Distingue contesto della chat da folder persistente, consultazione selettiva e suoi limiti. | Promette memoria automatica o contesto illimitato. |
| K2 | Fonte conservata → claim con locatore → grafo → risposta; riconosce conflitto nello stesso ambito e coesistenza in ambiti diversi. | Dà un numero senza fonte o scioglie un conflitto per recenza. |
| K3 | Collega la modifica a beneficio, triage L3, UC/IC/TM, Impact/design, implementazione, test/review e chiusura; spiega la funzione dei passaggi. | Si ferma alla sostituzione della costante o elenca sigle senza nesso causale. |
| K4 | Distingue proprietà di KB e SDLC; Standalone completo, devPNT opzionale. | Fa dipendere le skill da devPNT o fa decidere la UI alla KB. |
| K5 | Settimana/mese/anni sullo stesso caso: indica riuso possibile e verifica ancora dovuta, senza promessa numerica. | Dice che l'accumulo garantisce verità o velocità. |
| K6 | Applicazione propria in sola lettura con fonte/locatore o lacuna, beneficio, attore, superficie, rischio, decisione umana e verifica mancante; nessun file prodotto necessario. | Assume un fatto non verificato o omette la scelta umana. |

La presenza di tutti i termini non equivale a comprensione: l'autore cercherà le relazioni causali nell'esempio. Un controllo che soddisfa già i criteri rende inconcludente un successo del corso. Ogni blocco nel partecipante con corso richiede una correzione della spiegazione e un nuovo paio di sessioni indipendenti. Conserveremo qui prompt e risposte verbatim, identificativi, hash e valutazione.

## Sessioni e risultati

Le sessioni sono state avviate in parallelo con `collaboration.spawn_agent` e `fork_turns: none`, senza passare i turni di progetto. I nomi seguenti sono gli identificativi restituiti dallo strumento. Non è stato applicato un sandbox filesystem separato: l'isolamento dell'accesso al repository era una regola nei prompt, rispettata secondo i materiali dichiarati nelle risposte ma non garantita tecnicamente. I due agenti avevano le stesse capacità disponibili; solo il materiale consentito differiva.

### Prompt verbatim

Il prompt completo di ciascuna sessione è il rispettivo **prefisso** seguente, due newline, poi il **compito comune** riportato subito dopo. Questa scomposizione evita di riscrivere il medesimo compito e consente di ricostruire esattamente entrambi i messaggi.

**Sessione con corso, ID `/root/course_learner_p1`:**

```text
Sei un simulatore indipendente di una persona del team software che usa agenti AI (profilo P1). Sei in un contesto nuovo: non leggere la conversazione, Vision, ANALYSIS, grafo, report, risposte attese o output di altri agenti. Il solo pacchetto corso permesso è D:\SoftwareDev\skill_sdlc\agentic-sdlc-skill\ai_docs\solutions\courses\agentic-sdlc-kb-agentic\COURSE_PLAN.md, sources.md e modules\M1.md fino a M7.md. Leggilo interamente. Non aprire altri file del repository e non cercare online. Non valutare la tua risposta con voti o criteri nascosti. Rispondi come il partecipante, con il testo della tua spiegazione e, in coda, 'Materiali usati' e 'Passaggi poco chiari'. Non scrivere file.
```

**Controllo senza corso, ID `/root/course_control_p1`:**

```text
Sei un simulatore indipendente di una persona del team software che usa agenti AI (profilo P1). Sei in un contesto nuovo: non leggere la conversazione, Vision, ANALYSIS, grafo, report, risposte attese o output di altri agenti. Questa è la sessione di controllo: non ricevi il pacchetto corso. Non aprire alcun file del repository e non cercare online. Non valutare la tua risposta con voti o criteri nascosti. Rispondi come il partecipante, con il testo della tua spiegazione e, in coda, 'Materiali usati' e 'Passaggi poco chiari'. Non scrivere file.
```

**Suffisso identico dei due prompt:**

```text
COMPITO IDENTICO PER LE DUE SESSIONI:
Sei una persona del team software che usa agenti AI. Spiega a un nuovo collega, usando Orione come esempio ipotetico, che cosa cambia fra usare un agente in chat senza un metodo di progetto e usare `kb-agentic` con `agentic-sdlc`. Segui un manuale dal suo ingresso fino a una risposta citabile, descrivi come gestire due regole in conflitto, poi accompagna la modifica del timeout dal beneficio atteso alla chiusura. Distingui Standalone e devPNT. Confronta lo stesso progetto dopo una settimana, un mese e anni, indicando a ogni tappa quale ricostruzione si evita e quale verifica resta necessaria. Spiega anche come useresti in sola lettura un documento del tuo progetto per iniziare un caso analogo, senza inviarlo qui. Indica i passaggi che ti restano poco chiari e i materiali che hai usato. Non inventare fatti sulle skill quando non hai una fonte.
```

### Risposte preservate

| Sessione | File con risposta verbatim dopo il completamento | SHA-256 |
|---|---|---|
| Con corso | `simulation_course_p1_response.md` | `2bd2daaebb08755f4492911b2b54f842eefb52d22acb79b25f0767b2e9c91ff2` |
| Controllo | `simulation_control_p1_response.md` | `86bf58dccd77bd63018ffab67eeb99c9535c81a63be5a0a2437db4a4ac250918` |

I file sono stati creati **dopo** le risposte finali dai rispettivi agenti, su richiesta di copiarle senza modificarle; non facevano parte del materiale consentito durante la prova. La sessione con corso dichiara di aver letto solo piano, fonti e M1–M7; il controllo dichiara di non aver consultato file o fonti online. La corrispondenza è auto dichiarata dagli agenti, non verificata da log di accesso.

### Valutazione dell'autore contro i criteri predefiniti

| Criterio | Con corso | Controllo senza corso | Lettura diagnostica |
|---|---|---|---|
| K1 | Soddisfatto: folder, indici, contesto selettivo e limite della memoria personale. | Parziale: riconosce perdita della chat e riuso di note, senza spiegare la consultazione mirata del folder. | Il corso rende più specifico il meccanismo. |
| K2 | Soddisfatto: fonte, claim, grafo, locatore preciso e conflitto nello stesso ambito distinto da periodi diversi. | Parziale: propone citazioni e controlla gli ambiti, ma non conosce la catena di acquisizione/claim/grafo della skill. | Il modello operativo specifico emerge solo nella risposta con corso. |
| K3 | Soddisfatto: beneficio, L3, UC, Functional Spec, IC, TM, Ledger, Impact, design, test, review e chiusura con nesso causale su Orione. | Parziale: beneficio, casi limite, implementazione e test sono ben descritti, ma triage, tre lenti, Ledger, Impact e review del design non sono verificati. | Il corso aggiunge i passaggi specifici della skill senza sostituire la competenza software generale. |
| K4 | Soddisfatto: proprietà KB/SDLC, Standalone completo ed E-ISP/E-TDD con devPNT opzionale. | Parziale e prudente: ipotizza la distinzione ma dice di dover leggere le istruzioni reali. | Nessuna invenzione nel controllo; il corso offre il riferimento concreto. |
| K5 | Soddisfatto: settimana, mese e anni, con ricostruzione evitata, verifica residua e limite di manutenzione. | Sostanzialmente soddisfatto: la tabella temporale è utile e prudente anche senza corso. | **Inconcludente** per questo criterio: il successo con corso non prova un vantaggio causale rispetto a un controllo già capace. |
| K6 | Soddisfatto: documento autorizzato in sola lettura, fonte o lacuna, beneficio, attore, superficie, rischio, decisione umana e verifiche. | Parziale: propone documento/versione/fonte, ma non trasferisce esplicitamente il caso a beneficio, attore, superficie, rischio e decisione umana. | La guida di M6 rende visibile la seconda metà del compito. |

La sessione con corso ha segnalato due dubbi utili. Primo, il comportamento esatto quando callback e scadenza coincidono al quarantacinquesimo secondo: il corso richiede che la persona lo specifichi e lo verifichi, e **non lo risolve inventando una precedenza**; non è un blocco della spiegazione. Secondo, vorrebbe vedere in un caso reale la propagazione della rettifica alle GUIDE e alle decisioni che citano il claim: è un possibile ampliamento pratico, oltre la comprensione richiesta da O3. Il controllo ha riconosciuto i limiti delle proprie conoscenze sulle procedure effettive delle skill. Nessuna delle due risposte è stata usata per dichiarare apprendimento umano. Non si è resa necessaria una riscrittura bloccante né un nuovo paio di sessioni.

## Conclusione e limiti

Il corso consente a **questo agente lettore** di ricostruire tutti i passaggi fissati nei criteri, mentre il controllo risponde bene ai temi generali ma non a vari dettagli delle skill. Per K5 il confronto non distingue i due. Un solo paio di agenti, senza isolamento tecnico del filesystem e con conoscenza pregressa non misurata, serve a cercare difetti del testo; non misura l'apprendimento del team, non quantifica produttività e non autorizza a togliere `efficacy not verified` dal piano. Un riscontro umano futuro potrà motivare correzioni del corso o, se mostra un difetto ripetibile del metodo, una modifica separata di `course-creator`.
