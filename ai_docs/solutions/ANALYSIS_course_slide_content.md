---
id: F-060
feature: Contenuto completo e metodo didattico verificabile dei corsi
status: COMPLETED
level: L3
start_date: 2026-09-27
end_date: 2026-10-02
---
# Course Creator: contenuto, progressione e ruoli indipendenti

## Objective
Per l'agente che mantiene course-creator: quando un corso insegna a lavorare con uno strumento, un agente o un processo delegato, obiettivi, casi svolti, verifiche e simulazione devono esercitare gli atti della persona (formulare o precisare una richiesta, giudicare un'uscita, prendere una decisione riservata a lei, usare lo strumento), non le operazioni che lo strumento svolge per lei. L'incremento nasce dal feedback del proprietario su C-001 3.0: S17, S23 e S27 chiedono alla persona di scrivere un claim, classificare un conflitto fra documenti e assegnare il livello di triage. Il design dell'incremento precedente (ruoli autore, lettore e revisore) è archiviato nel Diary.

## Feature Vision
Autorità: `VISION_course_creator.md` APPROVED. Il Destinatario vi è definito come chi vuole capire un tema e, con una buona esperienza, arriva «a usare la conoscenza promessa». Per un corso su uno strumento, usare significa lavorare con lo strumento: un corso che addestra a imitarlo non porta a quell'uso. La correzione serve quindi il beneficio centrale, una spiegazione efficace per destinatari definiti, senza nuove autorità né campi. Un campo sul pubblico duplicherebbe requisiti esistenti; la distinzione entra nella situazione d'uso che §1 già chiede. La Vision di C-001, emendata il 2026-09-28, è il primo caso; la regola vale per ogni corso su strumenti, agenti o processi delegati e lascia invariati gli altri corsi. Nessun non-obiettivo toccato: nessuna efficacia viene dichiarata, nessun artefatto per corso aggiunto. Divulgazione richiesta dal test di ammissione della Vision di progetto: l'incremento aggiunge una riga obbligatoria alla rubrica di accettazione semantica L3 e un dovere di registrazione per obiettivo, entrambi solo per corsi su strumenti, agenti o processi delegati; non rimuove nulla; il costo è una riga per capacità promessa nella review e una distinzione atti/operazioni per obiettivo nella colonna esistente.

## Use Cases / User Needs
Nomi EXISTS: `learning_design.md`, `templates.md`, `simulation.md`, `slide_content.md`, la tabella `Teaching alignment` di COURSE_PLAN. Nessun nome NEW: l'incremento aggiunge una regola, non un artefatto.
- UC1 Autore della formazione: progettare obiettivi e verifiche su ciò che il destinatario fa davvero con lo strumento. Beneficio: corso rivolto alle persone giuste.
- UC2 Destinatario: esercitarsi negli atti che compirà (chiedere, giudicare, decidere) invece di riprodurre a mano ciò che lo strumento produce. Beneficio: arrivare a usare la conoscenza promessa.
- UC3 Revisore didattico (ruolo del metodo in `simulation.md`, non attore della Vision; realizza il segnale di successo «Un revisore che non ha seguito la preparazione può indicare per ogni modulo…» e restituisce i finding all'Autore): respingere una verifica il cui risultato richiesto è un'uscita dello strumento, qualunque verbo la introduca. Beneficio: la review scopre dove il corso manca la promessa.

## Functional Spec
1. Nella situazione d'uso (§1), per un corso su strumento, agente o processo delegato, l'autore registra per obiettivo gli atti della persona e le operazioni dello strumento. Il posto è la colonna esistente `Objectives and use context`; nessun nuovo campo. La ripartizione si legge dalla Vision approvata del corso (destinatari e perimetro): la registrazione la realizza e il revisore la confronta con la Vision, non con se stessa. L'elicitazione specifica dei corsi chiede chi compie ciascun atto nella situazione reale.
2. Se una verifica non mostra alcuna uscita dello strumento e chiede alla persona di assegnare un livello, una categoria o un verdetto che lo strumento produce, quel risultato resta un'uscita dello strumento anche se il ruolo della persona possiede la decisione che ne dipende. Una classificazione, valutazione o registrazione prodotta dallo strumento (livello, categoria, verdetto su un conflitto, affermazione estratta) resta una sua uscita anche quando una decisione ne dipende. La decisione della persona è accettarla, contestarla o sostituirla dopo che lo strumento l'ha prodotta. Sono riservate alla persona le decisioni che lo strumento le consegna: approvazioni, scelte aperte, perimetro.
3. Il meccanismo dello strumento si spiega quanto serve a chiedere, riconoscere e verificare. La persona può leggere da sola una fonte o un artefatto per verificare l'uscita: la verifica è un suo atto, la produzione dell'artefatto no. Prevedere che cosa restituirà lo strumento è un atto della persona quando serve a riconoscerne o verificarne l'uscita e la verifica confronta poi la previsione con l'uscita reale, salvo che la Vision approvata del corso riservi quell'uscita allo strumento. Le ammissioni del metodo sono valori predefiniti che la Vision del corso può restringere.
4. Quando la procedura la esegue lo strumento, il caso svolto (§4) mostra l'uscita accanto alle osservazioni, e il ragionamento della persona è il giudizio su quell'uscita.
5. L'accettazione semantica (§7) ha una riga `Learner's act`, applicabile solo ai corsi su strumento, agente o processo delegato che svolge operazioni per la persona (altrimenti non applicabile): la verifica parte da una richiesta, da un'uscita da giudicare o da una decisione riservata, e il risultato richiesto non è, neppure in forma ridotta, un'uscita dello strumento, qualunque verbo la introduca. Una violazione fa fallire la prontezza.
6. Nella simulazione il lettore simulato è un agente e può rispondere bene eseguendo lui stesso le operazioni dello strumento. Testo per `simulation.md`, sezione «Protocol, fixed before testing»: «When the course teaches work with a tool, agent or delegated process that performs operations for the learner (`learning_design.md` §1), the simulated learner is itself an agent and can answer well by performing the tool's operations. Place it in the person's role as the approved course Vision describes, and give the final task a tool output to judge or a request to formulate wherever the real situation has one.» Sezione «Freeze evidence and distinguish what the test evaluates»: «For a course on a tool, agent or delegated process that performs operations for the learner (see Protocol above), the frozen criteria score the person's acts (the request, the judgement of the tool's output, the reserved decision) and give no credit for producing, in any form, an output the tool produces for the person.»
7. Corsi che non insegnano a lavorare con uno strumento: nessun cambiamento.

Criterio di accettazione: con il testo §1/§4/§7 nuovo e la Vision del corso un revisore indipendente respinge S17, S23 e S27 di C-001 3.0 e ammette S11, S14, S38 e la riscrittura di S17; con il testo attuale non le respinge. Tre unità di controllo non vengono respinte per l'atto: una query SQL scritta da chi usa lo strumento, una previsione di `git status` confrontata con l'uscita reale, una spiegazione in un corso concettuale. I controlli provano FS7 e la clausola di portata; la clausola sulla previsione (FS3) non è stata esercitata da nessun revisore in un corso dove la riga si applica. Prova in `harness_course_role/`.

## Interface Contract
Superfici esistenti, nessun idioma nuovo. IC1 Autore: legge la regola in §1 quando scrive gli obiettivi e la usa nella colonna di allineamento. IC2 Revisore: applica la riga `Learner's act` di §7 alla packet reale e cita il passaggio che la viola. IC3 Simulazione: il principale prepara prompt e criteri secondo `simulation.md`; il lettore riceve il ruolo della persona. Feedback: i finding tornano all'autore come oggi.

## Capability Ledger
| Capacità | Stato | Evidenza e decisione |
|---|---|---|
| Registrare la situazione d'uso | INADEQUATE | `learning_design.md` §1 e colonna `Objectives and use context` di `templates.md` chiedono la situazione, non chi compie ciascun atto. Estendere il testo esistente. |
| Caso svolto e pratica | INADEQUATE | §4 porta la persona a eseguire la procedura; per una procedura dello strumento non dice che l'oggetto è il giudizio. Aggiungere una frase. |
| Accettazione semantica | INADEQUATE | §7 non ha un criterio sull'atto; il run `old` della prova ammette S17, S23, S27. Aggiungere riga e condizione di fallimento. |
| Simulazione con controllo | INADEQUATE | `simulation.md` non considera che il lettore simulato sia un agente premiato per eseguire lo strumento (criteri K3–K5 di C-001 2.1). Aggiungere un paragrafo. |
| Validatore strutturale | EXISTS | `course_check.py` non legge la tabella di allineamento; giudizio semantico, nessuna modifica. |

## Impact
- `distributions/course-creator/skills/course-creator/learning_design.md`: paragrafo «Who performs each act» in §1, frase in §4, riga `Learner's act` e condizione di fallimento in §7. Serve UC1–UC3, FS1–FS5.
- `templates.md`: segnaposto della colonna `Objectives and use context` con l'atto della persona e, dove esiste, l'uscita dello strumento su cui agisce o la richiesta che formula. Serve UC1, FS1.
- `simulation.md`: una frase in «Protocol, fixed before testing» e una in «Freeze evidence and distinguish what the test evaluates» (testo in FS6). Serve UC3, FS6.
- `elicitation.md`, «Course-specific elicitation»: una clausola che chiede chi compie ciascun atto nella situazione reale. Serve UC1, FS1.
- `SKILL.md`, «Content acceptance gate»: un rinvio alla riga `Learner's act` di `learning_design.md` §7 per i corsi su strumenti. Serve UC3.
- `distributions/course-creator/CHANGELOG.md`: voce `Unreleased` (il pacchetto spedisce i sei file della skill toccati). Nessun bump di versione né pubblicazione in questo incremento.
- `slide_content.md`: una frase nel paragrafo sui corsi di metodo/strumento che rinvia a §1. Serve UC1.
- `learning_design.md` §1/§4/§7: testo identico a `harness_course_role/packet_new5/RUBRIC.md`.
- ANALYSIS, HANDOFF, REVIEW_LOG e indici: stato e prove.

Blast radius: `sdlc_check.py` elenca questi file solo come file di supporto; nessun test in `scripts/` cerca le frasi modificate; nessuno è in `SHARED_FILES`. Le copie in `evals/results/` sono istantanee storiche e restano invariate.

Popolazioni esistenti: C-001 3.0 è stato prodotto con la regola vecchia e fallisce quella nuova; la sua correzione appartiene al workstream C-001, dove il debito è registrato nel Diary e nella HANDOFF. Riletti con il nuovo testo di FS6, i criteri congelati `simulation_2_1/CRITERIA.md` avrebbero dovuto essere riscritti in K2 (verdetto sul conflitto prodotto dalla persona senza un'uscita dell'agente), K3 nella parte sul livello L3 e K4 (scelta di riuso dal registro delle capacità); K1, K5–K8 valutano atti della persona. La diagnosi del 2026-09-28 indicava K3–K5: K5 giudica la chiusura dichiarata dall'agente e resta ammesso, K2 si aggiunge. I corsi di fixture in `evals/results/` e `harness_course_creator/` non vengono rivalidati: restano evidenza storica della regola precedente.

## Security and Threat Model
Nessun eseguibile, servizio o dipendenza. Rischi: (a) respingere verifiche legittime in cui la persona deve davvero lavorare da sola: la regola vale solo per corsi su strumenti, e usare lo strumento e verificare restano atti della persona; (b) scappatoia verbale che chiama decisione un'uscita dello strumento: chiusa da FS2 e dalla clausola sul verbo, provata nel run `new2`; (c) variabilità del revisore: un campione per run, dichiarato; (d) fuga dei criteri nel prompt del lettore simulato: FS6 non cambia il divieto esistente di mostrargli chiave e risposta attesa.

## Action Plan
1. Review indipendente del design (review.md, momento 1).
2. Applicare i sei file della skill e il CHANGELOG, con testo di §1/§4/§7 identico a quello provato.
3. Verificare l'identità del testo con la packet `new5`, eseguire la suite della distribuzione, review indipendente del diff.
4. Rigenerare gli indici e aggiornare HANDOFF. La correzione di S17, S23, S27 e dei criteri K2–K4 resta a C-001, registrata nel suo Diary e nella sua HANDOFF.

## Test Strategy
Prova rosso/verde in `ai_docs/solutions/harness_course_role/`: stesse sette unità, stesso profilo e prompt (`PROMPT.md`), cambia solo la rubrica. `old` rosso, `new` parziale (S27 ammessa), `new2` verde, `new3` e `new4` (correzioni dei due giri di review del design) di regressione, `new5` con la frase sui livelli assegnati senza uscita dello strumento, e due run con gli estratti della Vision di C-001 al posto del profilo (`new5_vision_a/b`, più `old_vision` come confronto); controlli `ctrl_operate` e `ctrl_concept` per FS3 e FS7. Attese congelate in `EXPECTED.md` prima di ogni run; esiti in `RESULTS.md`, uscite dei revisori in `outputs/`. FS6 non ha una prova eseguita: la verifica è la rilettura dei criteri K1–K8 di C-001 riportata in Impact; resta da provare su una simulazione nuova di C-001. Dopo l'implementazione: confronto testuale fra §1/§4/§7 del file e la packet `new5`; suite `python -m unittest discover -s scripts -p "test_*.py"` della distribuzione. Esito (`RESULTS.md`): claim e verdetti sul conflitto respinti in 6 su 6 run con la sola regola; il livello assegnato senza dichiarazione dell'agente solo in 3 su 6, e in 2 su 2 quando il revisore riceve la Vision del corso che la regola indica come autorità. Con la sola Vision emendata e la regola attuale le tre unità sono respinte, ma lo è anche S11, un giudizio legittimo sull'uscita dell'agente. Residuo dichiarato: in un corso su strumenti la cui Vision non nomina queste uscite, il verdetto su livelli e categorie può variare fra revisori. La prova non misura efficacia su persone.

## Diary / Current State
### Stato corrente
2026-09-28: incremento implementato. Sei file della skill (`learning_design.md` §1/§4/§7 identici a `harness_course_role/packet_new5/RUBRIC.md`, `templates.md`, `simulation.md`, `slide_content.md`, `elicitation.md`, `SKILL.md`) e voce `Unreleased` nel CHANGELOG; versione 0.1.0 invariata, nessuna pubblicazione. Suite della distribuzione: 245 test OK, 19 skip; `npm test` 4 pass, 1 skip. Review indipendente del diff PASS (0 BLOCK, 4 WARN, 2 CANNOT_VERIFY); corretti l'antecedente in `simulation.md`, il segnaposto di `templates.md`, i conteggi e le prove; il diff ricostruito è in `harness_course_role/F060_method.diff` perché la distribuzione non è mai stata committata. Residuo: senza una clausola della Vision del corso, il verdetto su livelli e categorie assegnati dalla persona varia fra revisori (3 su 6). Da fare in C-001: riscrivere S17, S23, S27 e i criteri K2–K4.

2026-09-28: diagnosi dello scostamento di ruolo segnalato dal proprietario su C-001 3.0. Nessuna correzione ancora progettata o applicata.

Evidenza. Le prove S11, S38 e S42 mettono la persona davanti a un'uscita dell'agente da valutare, correggere o riassegnare. Le prove S17, S23 e S27 chiedono invece alla persona di eseguire il lavoro dell'agente: formulare il claim e l'argomento, classificare il conflitto, assegnare il livello di triage. Le spiegazioni S13, S14 e S33 usano la prima persona plurale per operazioni della skill («ricaviamo», «completiamo un'indagine»). I criteri congelati K3–K5 della simulazione 2.1 premiano la riproduzione corretta degli esiti del protocollo, non la guida o la verifica di un agente.

Meccanismo. Il metodo chiede la situazione d'uso del destinatario (`learning_design.md` §1) e la colonna «Objectives and use context» (`templates.md`), ma non chiede chi compie ciascun atto in quella situazione. In un corso su uno strumento eseguito da un agente, «usare il metodo» viene quindi letto come «eseguire la procedura», e §4 (caso svolto, supporto, pratica) porta la persona a svolgere la procedura dell'agente. COURSE_PLAN compila il contesto d'uso con compiti del sistema («rispondere su una fonte nuova»). Nessun controllo della rubrica §7 o di `simulation.md` chiede a chi appartiene l'atto richiesto. La simulazione non può rivelarlo: il lettore simulato è un agente e risponde bene quando il compito coincide con l'esecuzione del protocollo.

Contributo della Vision del corso. Le promesse 2, 3 e 5 usano «seguire» ed «eseguire» senza dire se la persona osserva, chiede, verifica o svolge. I destinatari sono definiti; il verbo delle capacità ammette entrambe le letture. Una modifica richiede l'approvazione del proprietario.

Implicazione per la correzione. Un nuovo campo sul pubblico duplicherebbe requisiti esistenti. Serve una distinzione, per ogni obiettivo e prova, fra l'atto della persona e l'atto dell'agente nella situazione reale, con un controllo di review e un caso negativo: materiale accurato sul tema che addestra la persona a eseguire il lavoro dell'agente. La prova rossa-verde va eseguita su C-001 3.0 prima di dichiarare la correzione efficace.

2026-09-28: il proprietario ha approvato l'emendamento della Vision di C-001 (atti della persona, non operazioni dell'agente) dopo blind check PASS al terzo round; versione precedente in `audit/vision_history/`. Prossimo passo: design della correzione del metodo con prova rossa su S17, S23 e S27 della 3.0.

2026-09-28: prova rosso/verde della regola sull'atto della persona completata (`harness_course_role/RESULTS.md`). Design dell'incremento scritto sopra; review del design da eseguire prima di modificare la skill.

### Design dell'incremento ruoli — archiviato
#### Objective
Per l'agente che mantiene course-creator: rendere eseguibile la separazione approvata fra autore/coordinatore, lettore per profilo e revisore didattico. Il grafo e il testo canonico restano sotto un autore responsabile. Il lettore riceve soltanto il materiale già rivelato; il revisore valuta risposte, dipendenze e contenuto, l'autore applica le correzioni. L'incremento organizza ruoli già previsti, senza cambiare il metodo di progressione o il contratto testuale.

#### Feature Vision
VISION_course_creator.md APPROVED richiede spiegazioni che non obblighino il destinatario a indovinare termini o passaggi. Stesso pubblico, capacità e superficie: manutenzione di tale requisito. Nessuna nuova triage o autorità didattica. La Vision di progetto richiede autonomia: distill viene usata quando disponibile; in sua assenza resta la disciplina completa esistente, con limite dichiarato. La progettazione specifica il filo di scoperta negli spazi di spiegazione e transizione esistenti; la simulazione di lettura riceve le unità in sequenza al posto di un pacchetto intero. Nessun nuovo documento, campo obbligatorio o gate L1. La lettura progressiva sostituisce la lettura globale della simulazione esistente; il breve riscontro per unità rende localizzabile il primo difetto. Il report esistente conserva questi riscontri, senza una seconda review o artefatto obbligatorio per corso. Il proprietario ha approvato sia il riuso di distill sia questa organizzazione: un autore, un lettore per profilo e un revisore indipendente. Si riusano simulazione, review e relativi report; nessun nuovo gate L1 né documento per corso. Il controllo senza corso già richiesto resta una sessione aggiuntiva per il confronto finale, distinta dai tre ruoli principali.

#### Use Cases / User Needs
- UC1 Autore: scrivere contenuti completi per il pubblico reale con una disciplina testuale già disponibile.
- UC2 Corsista: seguire un problema o una domanda, acquisendo ogni informazione nel momento in cui serve, senza ricostruire riferimenti da slide future.
- UC3 Revisore: giudicare in un contesto indipendente i difetti segnalati dal lettore e la loro correzione, citando passaggi ed evidenza; il lettore non si auto-valuta.
- UC4 Ambiente senza distill: continuare la produzione dichiarando quale revisione non è stata eseguita.

#### Functional Spec
1. Prima di scrivere o riscrivere testo didattico sostanziale, cercare distill nel catalogo del client e leggere il suo SKILL.md; usare il suo contratto e gate, senza riprodurne le regole in course-creator.
2. Il lettore del testo didattico è il corsista del profilo approvato, non il progettista. Le note di produzione ospitano il contratto secondo distill; i metadati non entrano nelle slide.
3. La review usa distill sul materiale realmente consegnato al corsista. Restano obbligatori metodo, esempi, ragionamenti, limiti e soluzioni richiesti da course-creator; nessuna equivalenza tra testo corto e testo utile.
4. Se distill manca o non è leggibile, dichiararlo e continuare con la review di chiarezza e fedeltà già prevista. Non dichiarare applicato distill, non installarlo automaticamente, non copiarne una versione locale.
5. Learning_design §3 guida un filo narrativo conoscitivo: situazione familiare e domanda, informazione necessaria a rispondervi, conseguenza che motiva il passo successivo. Non richiede personaggi o finzione, né una formula fissa per slide. Anche corsi concettuali possono sviluppare una domanda.
6. Il grafo dei concetti è l'autorità delle dipendenze; il racconto ne realizza un ordine ammissibile. Per ogni concetto il progettista individua nella sequenza effettiva il passaggio che lo spiega e il primo passaggio che ne richiede la comprensione; verifica prima anche le spiegazioni dei suoi prerequisiti. Nomi, riferimenti e termini devono essere identificabili alla prima funzione significativa. L'apertura orienta con problema e beneficio comprensibili; un'anticipazione è ammessa se si capisce senza la spiegazione futura. La transizione nasce dalla questione aperta, non dal titolo seguente. Un prerequisito scoperto scrivendo torna nel grafo; nessun secondo grafo né nuove chiavi obbligatorie nello schema slide.
7. La simulazione di lettura rivela una sola unità per turno e conserva l'interpretazione prima della successiva. Il lettore vede solo profilo, prefisso già letto e unità corrente; niente piano, note interne, soluzioni anticipate o accesso al sorgente completo. Dove la limitazione è soltanto un'istruzione, dichiararlo. Un agente che ha visto il futuro non può validare quel prefisso.
8. Una lacuna già presente resta un finding anche se il seguito la risolve. Correggere la prima dipendenza e riprovare il prefisso in un contesto fresco. La prova di trasferimento con controllo resta separata: il controllo non riceve il dialogo della lettura. Rendering che cambia ordine o suddivisione richiede controllo dell'ordine finale.
9. Per produzione/revisione sostanziale L3, l'agente principale è autore/coordinatore e unico integratore di grafo, piano e testo. Usa sessioni indipendenti per un lettore per profilo e per un revisore didattico quando il client le rende disponibili; preserva review.md per indisponibilità, autorizzazioni e capacità. L1 resta correzione locale, L2 segue la portata del cambiamento e i controlli già dovuti.
10. Lettore: profilo e unità via via rivelate, nessuna discussione dell'autore, fonte di soluzioni o grafo. Revisore: Vision approvata, obiettivi, profili, grafo, testo, fonti, criteri, chiave e trascritti; restituisce finding localizzati e verdetto sul materiale testato. Il reviewer non ha scritto il materiale. Nessuna persona/sessione che conosce il seguito può tornare lettore dello stesso prefisso.
11. Dopo i finding, l'autore corregge la versione canonica e le dipendenze coinvolte. Lettore fresco per il prefisso interessato; reviewer ricontrolla la correzione nell'esistente limite di round di review.md. Nel SIMULATION_REPORT si distinguono autore, lettori per profilo, controlli, reviewer, versione e limiti; REVIEW_LOG conserva il verdetto del reviewer.
12. Autori paralleli non sono il default. Se scelti per lavoro ampio, ricevono fonti, unità assegnate e conoscenze attese all'ingresso/uscita; l'autore principale integra la sequenza ed è unico scrittore canonico. Resta il confine di dispatch.md: gli artefatti governati e le decisioni di perimetro restano al principale; il suo PLAN opt-in si applica all'eventuale produzione delegata, non crea un piano aggiuntivo per semplici lettori/reviewer.
13. Distill è un collaboratore esterno individuato per nome, senza path personali, versione fissa o dipendenza di packaging. Nessuna modifica a parser, schema o skill distill.

#### Interface Contract
##### IC1 — Autore
Il principale mantiene Vision, analisi, grafo, piano e testo canonico; integra eventuali bozze limitate e applica le correzioni. Il profilo e la capacità didattica alimentano il contratto di scrittura di distill. Course-creator mantiene obiettivi e completezza del sorgente; distill mantiene l'unica definizione della propria disciplina.
##### IC2 — Revisore
Il reviewer indipendente riceve gli artefatti e i trascritti e valuta insegnamento e verifica, incluso il filo di scoperta, con la rubrica pedagogica. Simulation consegna le unità in ordine e registra interpretazioni immutabili prima di proseguire. Distill valuta il testo visibile, e anche la narrazione parlata per corsi guidati. Un PASS riguarda soltanto materiale e versione esaminati.
##### IC3 — Assenza
La mancata disponibilità produce una dichiarazione e la review esistente, non blocca il corso e non certifica una verifica mai eseguita.

#### Capability Ledger
| Capacità | Stato | Evidenza e decisione |
|---|---|---|
| Progettazione e completezza | EXISTS | learning_design.md e slide_content.md: allineamento, ragionamento, fonte, soluzione; conservare |
| Disciplina testuale | EXISTS | distill SKILL.md v0.8.0 installata dal proprietario: contratto prima del testo, gate e audit; richiamare senza copia |
| Collegamento autore/revisore | EXISTS | SKILL.md §4 richiama distill per scrittura e review, con fallback dichiarato |
| Progressione narrativa | EXISTS | learning_design §3 e rubrica collegano dipendenze ai passaggi effettivi; conservare |
| Ordine meccanico | EXISTS | course_check.py first_taught usa posizione del modulo e ordine degli ID nella colonna Concepts; non analizza la spiegazione o il primo uso nel testo. Conservare e dichiarare questo limite |
| Prova con conoscenza limitata al prefisso | EXISTS | simulation consegna unità progressive e preserva le risposte; conservare |
| Separazione dei ruoli | EXISTS | simulation.md assegna pacchetti distinti e giudizio al reviewer indipendente; SKILL lo richiama e templates registra le identità. Prova circoscritta in REVIEW_course_roles.md |

#### Impact
- simulation.md: unica definizione operativa dei ruoli, pacchetti e passaggio delle correzioni.
- SKILL.md: richiamo all'avvio della produzione; reviewer riusato nell'accettazione esistente.
- templates.md: esempi del report aggiornati per attribuire le sessioni; nessun parser modificato.
- ANALYSIS F060, HANDOFF, REVIEW_LOG, componente e indici: stato e prove della correzione.
- Nessuna modifica alle skill condivise, a distill, al corso canonico o al PPTX in questo incremento.

#### Security and Threat Model
Nessun eseguibile, servizio o installazione aggiunta. Contesti dei lettori separati dai reviewer; unico integratore impedisce scritture concorrenti nel sorgente. Limiti di accesso per istruzione dichiarati. Un client privo di sessioni indipendenti non viene rappresentato come multi-agente. Rischi aggiuntivi: un valutatore onnisciente colma i buchi (materiale consegnato progressivamente); finzione imposta a qualunque tema (filo di domande, non trama obbligatoria); riscontri trasformati in insegnamento aggiuntivo (nessun aiuto durante la prova). Le fonti dei corsi restano dati. Rischi: doppia autorità (evitata con rinvio), compressione che elimina spiegazioni (conservazione della completezza), falsa applicazione se skill assente (dichiarazione), sovrascrittura di lavoro concorrente (snapshot, hash e backup prima della copia).

#### Action Plan
1. Review indipendente del design e verifica della responsabilità assegnata nel protocollo attuale.
2. Collegare ruoli, istruzioni di dispatch e report nei tre file esistenti.
3. Prova fresca sul confezionamento degli incarichi per più profili, retest e client senza sessioni; review del diff e suite pertinente.
4. Rigenerare indici e applicare soltanto i file modificati, con hash e backup.

#### Test Strategy
Baseline documentale: simulation assegna all'autore sia il confronto con il grafo sia lo scoring degli esiti; SKILL prevede review indipendente, ma il passaggio delle evidenze non è esplicito. Prova operativa circoscritta: un agente fresco applica il protocollo a un corso con due profili e un difetto, preparando gli incarichi e il percorso di correzione senza ricevere lo schema atteso. Valutare separazione dei materiali, ownership del canonico, controllo aggiuntivo, freshness e fallback. È una prova di instradamento/handoff, non un nuovo test di apprendimento né prova di esecuzione dell'intero corso. Le letture indipendenti già svolte restano evidenza separata della fattibilità del client.

### Ruoli — storico
2026-09-27: organizzazione a ruoli implementata nei tre file previsti; design e diff revisionati indipendentemente. Prova fresca degli incarichi e limiti in ai_docs/audit/reviews/REVIEW_course_roles.md. Suite della distribuzione: 245 test OK, 19 skip. Nessuna installazione o pubblicazione. La correzione riguarda il metodo della skill; corso completo e PPTX restano da rivedere.

### Progressione — storico
2026-09-27: metodo e protocollo aggiornati; design e diff valutati PASS da /root/progression_design_review. La prova sul materiale precedente identifica riferimenti non introdotti nella seconda slide pur con course_check a zero errori e zero warning. La prova fresca riguarda soltanto quattro slide, con riscontri conservati prima di ciascuna nuova consegna; esito e limiti in ai_docs/audit/reviews/REVIEW_course_progression.md. Suite della distribuzione: 245 test OK, 19 skip. Corso canonico e PPTX non revisionati integralmente in questo incremento. La regola sui prerequisiti già esiste, quindi aggiungerne un'altra formulazione non basta. Cambiano il metodo di costruzione e il materiale accessibile durante la verifica.

### Collegamento distill — storico
2026-09-27: collegamento distill implementato; review indipendenti di design e diff PASS, nessun finding bloccante. La prova fresca ha letto distill e scritto una slide con contratto e audit separati. Il fallback è verificato sulle istruzioni e tramite risposta ipotetica, non eseguito in un ambiente privo della skill. Suite della distribuzione: 245 test OK, 19 skip. Il validatore generico skill-creator non eseguito: PyYAML manca nel runtime; nessuna dipendenza installata. Evidenze in ai_docs/audit/reviews/REVIEW_course_distill.md. Il corso canonico e il PPTX non sono stati riscritti. Evidenza negativa: il testo introduttivo v2.1 usa «traccia utile», «nota insufficiente», «regola verificata» e «cambiamento osservabile» senza chiarire nella frase gli oggetti e le operazioni. I precedenti PASS non attestano adeguatezza di ogni frase. Il gate globale resta separato dalla correzione locale.

### Incremento pedagogico precedente — storico

### Stato corrente
Incremento pedagogico implementato e validato nei limiti registrati. Design indipendente PASS; review doctrine PASS con due formulazioni corrette (rubrica informata dalle fonti, non validata sperimentalmente; descrizioni mantenute insieme ai locatori). Il caso negativo completo nella struttura è stato respinto per mancato insegnamento/verifica del giudizio promesso. Entrambi i produttori baseline e revisione hanno prodotto materiale sufficiente: beneficio incrementale INCONCLUDENTE. La trasposizione testuale HTML conserva 8/8 unità e transizioni; non è un test di impaginazione PPTX.

Evidenze e limiti in `distributions/course-creator/skills/course-creator/evals/results/pedagogy/RESULTS.md`, protocollo e review. Valutatore solo parzialmente cieco: ha visto l'intenzione del controllo prima della copia neutra dei criteri; non conosceva la corrispondenza dei pacchetti. Nessuna prova di eliminazione generale della causa o di efficacia umana. Suite 245 OK/19 skip, scenari 4 OK e byte del pacchetto verificati. Review finale delle evidenze PASS: nessun finding bloccante dell’incremento. Applicazione protetta dal confronto degli hash iniziali, backup e verifica dei byte copiati; il resoconto operativo della chat conserva la ricevuta. Gate globale preesistente non CLEAN; nessuna installazione/pubblicazione.

### Storia precedente (immutata)

2026-09-27: PLANNED. Il feedback del proprietario identifica l'assenza di guida e obbligo sul risultato didattico, e richiede un documento dettagliato per ogni slide. La generazione PPTX precedente era passata tramite Presentations: questo limita l'attribuzione causale, ma il contratto di course-creator effettivamente non proteggeva l'handoff. Baseline riprodotto su fixture. In attesa della review di design prima dell'implementazione.

2026-09-27: review design indipendente FAIL → PASS, round 2, reviewer /root/review_slide_contract. Risolti inclusione npm, migrazione legacy uniforme, criterio generale di valore e baseline rieseguibile. Implementazione e review finale in corso. Il test degli invarianti ha individuato anche il profilo dei supporti in sdlc_check.py: aggiornato come integrazione locale della lente.

#### Stato al termine del primo incremento — storico

Contratto e validator corretti; 52 slide integralmente scritte per C-001 2.0-content. Review indipendente di codice e contenuto PASS dopo le correzioni registrate in `ai_docs/audit/reviews/REVIEW_course_slide_content.md`. Forward test su conteggi/tassi PASS semantico; nessuna efficacia umana dichiarata. Suite 245 test OK (19 skip), scenari 4 OK, client 4 pass/1 skip, corso 0 errori/0 warning, pacchetto npm verificato realmente.

La review ha richiesto copertura esplicita `Covers` per verifiche cumulative e spiegazioni condivise fra profili, coerentemente con la Vision preesistente. Non serve una prova distinta per modulo. Il test invarianti ha anche richiesto la dichiarazione del nuovo supporto nel profilo locale sdlc_check.py.

Status IN_PROGRESS indica chiusura documentale globale pendente: `check` restituisce validate rc=0, stale rc=1 per aree non interamente riesaminate in questa unità. C-001 conserva separatamente il limite della nuova simulazione con/senza corso non eseguita. La correzione non viene pubblicata o installata automaticamente.

2026-10-02 release closure: method independently rereviewed PASS; 245 tests OK
(19 skips), package/scratch checks pass and repository check CLEAN. Skill increment
complete for beta; C-001 content and human efficacy remain separately open.
