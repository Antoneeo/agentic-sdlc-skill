---
id: F-086
feature: Guida del docente e pacchetto di erogazione per i corsi con docente (course-creator)
status: COMPLETED
level: L3
start_date: 2026-10-29
end_date: 2026-10-30
---
# Analisi: guida del docente e pacchetto di erogazione

## Objective
Per l'agente che crea un corso con course-creator: un corso dichiarato `Delivery mode: instructor-led` esce con `INSTRUCTOR_GUIDE.md`, che dà al docente le istruzioni di erogazione e l'elenco verificato del materiale da consegnare. Se la guida manca, se cita un materiale che non è nel pacchetto o se il testo del corso riporta una versione diversa da `Course version`, `course_check` lo segnala come errore. Nasce dalla segnalazione d'uso sul corso `agente-personale-skills` (REQUEST_instructor_guide.md#R1): il corso superava tutti i controlli ma non aveva istruzioni operative per chi lo eroga, e la slide del feedback (S38) diceva «versione 1.0» con il corso alla 1.2. Il proprietario ha esteso la richiesta all'intero pacchetto: «confezionare il corso mettendo tutto il mteriale necessario incluse le istruzioni per l'insegnante» (REQUEST_instructor_guide.md#R3).

## Feature Vision
Autorità: `vision/features/VISION_course_creator.md` APPROVED, emendata per questa unità (REQUEST_instructor_guide.md#R4, approvata in #R7; blind check PASS, REVIEW_LOG 2026-10-29). Servono:
- l'attore **Docente**, a cui una buona esperienza consegna «insieme al corso, tutto il materiale che l'erogazione richiede e le istruzioni per usarlo»;
- il segnale «Un corso con docente si consegna con tutto il materiale che l'erogazione richiede e con le istruzioni per usarlo», per il quale ciò che le istruzioni citano fa parte del pacchetto e un materiale citato e assente resta visibile come lacuna;
- il segnale sul feedback, «Un feedback ricevuto dopo la consegna indica dove una spiegazione, un modulo o un prerequisito vanno corretti». Un feedback attribuito alla versione sbagliata indica il punto sbagliato: è la traccia del controllo sulla versione.

Confine rispettato: il materiale per l'erogazione e la guida «non comprendono date o luoghi delle sessioni, iscrizioni, presenze, elenchi di partecipanti o dati su di loro». Il modello della guida non ha campi per queste cose e `templates.md` enuncia il confine in proprio, perché la Vision di questo repository non viene spedita con la skill.

## Use Cases / User Needs
Nomi EXISTS: `Delivery mode`, `instructor-led`, `self-study`, `Course version`, `Feedback flow`, `COURSE_PLAN.md`, `SLIDE_CONTENT.md`, `COURSE_CONTENT.md`, `D-IC.md`, `P-TM.md`, unità con `Role: solution`, `course_check.py`, la sezione `## Write Triggers` di `SKILL.md`. Nome NEW: `INSTRUCTOR_GUIDE.md` e le sue sei sezioni.
- **UC1 Docente.** Tiene in aula un corso con docente. Apre la cartella del corso e trova in un solo documento cosa preparare, la scaletta, cosa non proiettare, cosa fare quando un passaggio dal vivo devia e con quale materiale di riserva, cosa ripulire dopo e come raccogliere i riscontri. Ogni file citato è nel pacchetto. Beneficio: il segnale «Un corso con docente si consegna…».
- **UC2 Autore della formazione.** Dichiara `instructor-led` e lancia `course_check` prima della consegna. Il controllo nomina ciò che manca: la guida, un materiale citato e fuori dal pacchetto, una soluzione non riservata, un rischio o un modulo inesistente, una versione superata nel testo. L'autore non lo scopre più quando qualcuno chiede dove siano le istruzioni (#R1). Beneficio: lo stesso segnale, come lacuna visibile.
- **UC3 Destinatario della formazione.** Non vede soluzioni né materiale riservato, e il corso prosegue quando una dimostrazione dal vivo devia. Beneficio: attore Destinatario, «procede per moduli comprensibili». Il Destinatario non usa nessuna superficie nuova: riceve il risultato attraverso il docente (IC2).
- **UC4 Autore e Responsabile del contenuto davanti al feedback.** Il testo del corso nomina la versione dichiarata, quindi un feedback che la cita si riconduce alla versione giusta. Beneficio: segnale sul feedback.

## Functional Spec
Si applica ai corsi con contratto di contenuto dichiarato (`slide-content-v1` o `text-content-v1`). La modalità si legge da `Delivery mode` nell'intestazione del file di contenuto. Ogni violazione elencata è un ERROR, salvo dove indicato.

1. **Obbligo.** Con `Delivery mode: instructor-led`, l'assenza di `solutions/courses/<slug>/INSTRUCTOR_GUIDE.md` è un ERROR. Con `self-study` la guida non è richiesta; se esiste, si controlla con le regole 2–8. Una modalità sconosciuta o un file di contenuto mancante restano gli ERROR già esistenti e non attivano la regola: senza una modalità valida non c'è nulla da richiedere.
2. **Intestazione.** `Course version` e `Feedback flow` compaiono una volta ciascuno e sono uguali a quelli di `COURSE_PLAN.md`. Che la guida citi il canale di `D-IC.md` senza ridefinirlo è una regola d'autore, verificata dalla review e non dal validatore.
3. **Sezioni.** Sono presenti, una volta e non vuote: `## Before the course`, `## Schedule`, `## Reserved material`, `## When something deviates`, `## After the course`, `## Materials`.
4. **Materiali, il pacchetto.** `## Materials` è una tabella `| Material | Path | Seen by | Used in |` con almeno una riga. `Path` è un percorso relativo alla radice del progetto, senza unità, `/` iniziale, `..` o `#`, che resta dentro il progetto anche dopo la risoluzione dei link ed esiste come file o come cartella (una cartella si scrive con `/` finale). Può stare ovunque nel progetto (#R10): i progetti demo e il deck generato si elencano dove sono. `Seen by` vale esattamente `instructor` o `learners`. Ogni altra forma è un ERROR. È un WARN una cartella elencata dentro `ai_docs/` che contiene un proprio `.git` o `ai_docs/`, perché la memoria del progetto indicizza `ai_docs/` e presenterebbe i documenti del progetto annidato come documenti di questo (#R9).
5. **Materiale citato.** Ogni percorso che nella guida inizia con `ai_docs/` deve esistere e cadere dentro la cartella del corso oppure sotto un percorso elencato in `## Materials`; se porta un `#locator`, il locator deve esistere. Altrimenti è un ERROR anche se il file esiste, perché ciò che le istruzioni citano fa parte del pacchetto e il pacchetto è la cartella del corso più l'elenco dei Materiali. Il modello chiede di citare il materiale solo in questa forma.
6. **Materiale riservato.** Ogni unità con `Role: solution` del file di contenuto compare come ID intero (`S03`, mai dentro `S030`) nella sezione `## Reserved material`.
7. **Deviazioni.** `## When something deviates` è una tabella `| Risk ID | In class it looks like | Instructor action | Fallback material |` con almeno una riga. Ogni `Risk ID` esiste in `P-TM.md`. `Fallback material` è `-` (nessun materiale di riserva) oppure uno o più percorsi, separati da virgole, presenti in `## Materials`. Non si chiede una riga per ogni rischio, perché non tutti si manifestano in aula.
8. **Scaletta.** `## Schedule` è una tabella `| Session | Duration | Modules |` con almeno una riga. Ogni riga ha un nome, una durata e almeno un modulo, oppure `-` per una pausa o la chiusura; ogni ID di modulo (elenco separato da virgole) esiste in `COURSE_PLAN.md`. Le durate stanno solo qui: COURSE_PLAN non le ha, quindi non si duplica nulla.
9. **Versione nel testo, in ogni modalità** (#R8). Si controllano le righe dopo l'intestazione del file di contenuto (Course Value e unità) e le righe del corpo della guida dopo la sua intestazione. Una menzione è `version` o `versione` (senza distinzione di maiuscole), seguita da un eventuale `:` e da un numero: cifre, un punto, una lettera o cifra, poi eventuali lettere, cifre, `.` o `-`, con un eventuale `v` iniziale (`1.0`, `1.x`, `4.0-content`). Un `.` finale si scarta; `,`, `;` e `)` non fanno parte del numero. Il numero si confronta per uguaglianza esatta con `Course version`: `4.0` contro `4.0-content` è una differenza, perché il feedback deve portare la versione dichiarata. La menzione si controlla solo se nella stessa riga compare la parola `corso` o `course`, oppure il nome del corso: lo slug della cartella o il titolo `# ` intero del file di contenuto, cercati come parola o frase intera, senza distinzione di maiuscole (lo slug `intro` non vale dentro «Introduzione»). Se il titolo è una sola parola che nomina anche uno strumento citato, la regola può segnalare la versione di quello strumento; l'autore riformula la riga. Un numero senza punto (`versione 2`) non si controlla.
10. **Corsi legacy** senza contratto di contenuto: nessuna nuova regola, perché non dichiarano una modalità. Resta l'avviso legacy esistente.

Criterio di accettazione:
- `harness_instructor_guide/probe.py`: i probe RED falliscono sulla skill 0.1.0-beta.14 e passano dopo la modifica; le guardie passano prima e dopo.
- Il proprietario ripete la prova sul corso reale (#R6): con la skill nuova `course_check` segnala la guida mancante e «versione 1.0» in S38; dopo aver scritto la guida e corretto S38 torna pulito.

Residui dichiarati, verificati solo dalla review del corso:
- un materiale che l'erogazione richiede ma che la guida non cita, oppure una citazione scritta in forma diversa da `ai_docs/...`;
- un rischio di deviazione che esiste in `P-TM.md` ma non è quello giusto (il modello lo dichiara accanto alla tabella);
- la somma della Scaletta diversa dalla durata del corso;
- date o luoghi scritti nelle celle della Scaletta o nel testo libero;
- una menzione di versione senza `corso`/`course` né nome del corso nella stessa riga.

## Interface Contract
Superfici: il testo della skill letto dall'agente autore, il file `INSTRUCTOR_GUIDE.md` letto dal docente e i messaggi di `course_check` letti dall'autore. Idiomi riusati, nessuno nuovo:
- l'intestazione a campi `Key: value` uguale a COURSE_PLAN, come già fa `SLIDE_CONTENT.md`;
- le tabelle a colonne fisse di `D-IC.md`, `P-TM.md` e COURSE_PLAN;
- i riferimenti relativi al progetto `ai_docs/...#locator`;
- il formato dei finding, `file item: reason`.

Flussi:
- **IC1, Autore (agente).** Dichiara `instructor-led` e legge in SKILL.md, sezione Write Triggers, la riga per la guida del docente. Scrive la guida dal modello in `templates.md`, poi lancia `course_check`. Il controllo restituisce un finding per ogni regola violata, con file, elemento e motivo; un controllo pulito non certifica la qualità delle istruzioni.
- **IC2, Docente, e attraverso di lui il Destinatario (UC3).** Apre la cartella del corso e legge `INSTRUCTOR_GUIDE.md`, nell'ordine: prima, scaletta, riservato, deviazioni, dopo, materiali. Ogni percorso porta a un file presente nel pacchetto. `Seen by` e `## Reserved material` gli dicono cosa non mostrare. Quando un passaggio dal vivo devia, la riga del rischio gli dà l'azione e il materiale di riserva. Il Destinatario riceve così un corso senza soluzioni anticipate e senza interruzioni.
- **IC3, Feedback.** La guida e il testo citano `Feedback flow` e la versione dichiarata. Il canale resta definito solo in `D-IC.md`.

## Capability Ledger
| Capacità | Stato | Componente o lacuna | Evidenza |
|---|---|---|---|
| Leggere la modalità di erogazione | EXISTS | `course_check.py::_content_contract`, campo `Delivery mode` | riga 98: legge e valida il valore, poi lo scarta |
| Confrontare la versione dell'intestazione con il piano | EXISTS | `_content_contract`, campo `Course version` | riga 96; nessuna lettura del testo delle unità (probe RED) |
| Risolvere un riferimento di progetto in modo confinato | EXISTS | `validate_course::ref` e `read` | `ref` richiede un `#locator` (riga 234); i materiali sono file o cartelle senza locator. Si riusa il confinamento (`is_relative_to(root)`, nessun `..`) in una variante senza locator |
| Leggere tabelle a colonne fisse | EXISTS | `course_check.py::_table` | usata per D-UC, D-IC, P-TM, graph e plan |
| Impacchettare il corso in un archivio | EXISTS, non riusata | `scripts/docs_site.py --zip` | archivia il sito dei documenti, non il corso; #R5 ha scelto l'elenco verificato invece di un archivio |
| Richiedere e verificare il documento di erogazione | MISSING | nuova `_delivery_package(...)` in `course_check.py` | grep `instructor`/`guide`/`Delivery mode` nella distribuzione: solo il controllo del valore (riga 98) |
| Rilevare versioni superate nel testo | MISSING | nuova `_version_mentions(...)` in `course_check.py` | grep `version` in `course_check.py`: solo i campi d'intestazione |
| Modello e regola d'autore della guida | MISSING | sezione `INSTRUCTOR_GUIDE.md` in `templates.md`, riga in SKILL.md | `templates.md` Course detail files: D-UC, D-IC, P-TM, graph, plan |

## Guide check
- Guida CURRENT su ciò che si tocca: `GUIDE_skill_family_changes.md` (letta: `course_check.py` vive solo in `distributions/course-creator`, nessuna copia da contare).
- Componente complesso senza guida capito qui: no. `course_check.py` ha 479 righe di controlli lineari, già descritti nel Component Map di `strategic/architecture.md` («Course teaching validator»).

## Impact
| Percorso | Cambio | Perché |
|---|---|---|
| `distributions/course-creator/skills/course-creator/scripts/course_check.py` | MODIFY | `_content_contract` restituisce un dizionario `{path, text, mode, title, solutions}` invece di `None` (ritorno anticipato: `None`). Nuove `_delivery_package(root, course_dir, plan, plan_rows, contract, risks, read, add)` e `_version_mentions(path, body, version, names, add)`; `validate_course` chiama `_delivery_package` dopo `_content_contract`, con gli ID di rischio letti da `P-TM.md`. Variante confinata di riferimento senza locator per file e cartelle. |
| `distributions/course-creator/skills/course-creator/scripts/test_instructor_guide.py` | ADD | Batteria AAA che porta i probe nel set di test della distribuzione, sul modello di `test_slide_content.py`, riusando la fixture di `test_course_check.CourseChecks`. |
| `distributions/course-creator/skills/course-creator/templates.md` | MODIFY | Nuova sezione `### INSTRUCTOR_GUIDE.md` in Course detail files: regole, modello, citazioni solo `ai_docs/...`, e il confine sui dati dei partecipanti enunciato qui. |
| `distributions/course-creator/skills/course-creator/SKILL.md` | MODIFY | Riga Write Triggers: «Instructor-led course, before delivery → `INSTRUCTOR_GUIDE.md` (templates.md); `course_check` refuses delivery without it». |
| `distributions/course-creator/skills/course-creator/slide_content.md` | MODIFY | Dopo la riga 62 (definizione di `Delivery mode`): in `instructor-led` la Complete explanation è il testo da dire, ma le istruzioni operative e l'elenco del materiale stanno in `INSTRUCTOR_GUIDE.md`. Riga 70 (Release review): la consegna include la guida. |
| `distributions/course-creator/skills/course-creator/learning_design.md` | MODIFY | §5, riga 43: «in guided delivery, author the necessary spoken explanation» si completa con il rimando alla guida del docente. |
| `distributions/course-creator/README.md` | MODIFY | §Primary course output: un corso con docente esce anche con `INSTRUCTOR_GUIDE.md` e l'elenco verificato del materiale; i corsi con docente esistenti falliscono `check` finché non l'hanno (riga dell'audit plan su `distributions/`). |
| `ai_docs/strategic/skill_family_agent_workflows.md` | MODIFY | Paragrafo del flusso course (riga 455, «Il validator controlla struttura, ID, cicli, ordine e riferimenti»): aggiunge il pacchetto di erogazione e la versione nel testo (stessa riga dell'audit plan). |
| `ai_docs/audit/audit_plan.md` | MODIFY (chiusura) | `sdlc_check.py mark distributions/` dopo l'aggiornamento di README e documento di famiglia. |
| `distributions/course-creator/CHANGELOG.md` | MODIFY | Voce `[Unreleased]`, con le conseguenze per i corsi esistenti. |
| `ai_docs/strategic/architecture.md` | MODIFY (chiusura) | Riga Component Map «Course teaching validator»: il contratto ora include il pacchetto di erogazione dei corsi con docente e la versione nel testo. |
| `ai_docs/solutions/harness_instructor_guide/probe.py` | ADD | Probe eseguibili che accompagnano il design. |

Non toccati: `simulation.md`, perché il pacchetto del lettore simulato si costruisce da `slide_content.md` e la guida non vi entra; `package.json`, perché i test non sono spediti e nessun file della skill si aggiunge; `sdlc_check.py`, che chiama `validate_course` e `validate_all` con firme invariate.

**Popolazioni a riposo.** Trigger valutati: (1) un invariante passa da lettura a scrittura? No. (2) Un non-obiettivo vieta la migrazione? No. (3) Nuovo formato per dati esistenti? No. (4) Si ritira un controllo di filtro o autorizzazione? No. La modifica aggiunge però requisiti a corsi già scritti:

| Popolazione esistente | Regime che la copriva | Dopo la modifica | Chi vede la differenza |
|---|---|---|---|
| Corsi `instructor-led` con contratto di contenuto, senza guida (caso #R1) | nessun requisito per il docente | ERROR finché non si scrive la guida | l'autore al prossimo `check`. #R1 chiede che il controllo segnali il caso; ERROR invece di WARN è decisione dell'autore (Diary) |
| Corsi, di ogni modalità, con una riga che nomina il corso e riporta una versione superata | nessun controllo nel testo | ERROR sulla riga | l'autore: richiesto da #R1, forma da #R8 |
| Corsi legacy senza contratto di contenuto | avviso legacy | invariati: nessuna modalità da leggere | nessuno; il residuo resta coperto dall'avviso «quality is not certified» |
| C-001 in questo repository (self-study, `4.0-content`) | 0 finding | 0 finding (guardia del probe) | nessuno |
| Guide scritte con la regola #R5, con i materiali dentro la cartella del corso | regola 4 confinata alla cartella | restano valide, perché #R10 allarga la regola; un repository demo annidato dentro `ai_docs/` ora dà un WARN | l'autore: può riportare il demo fuori da `ai_docs/` (il caso della replica, #R9) |

### Preservation constraints

| id | bound to | callers | must stay true | evidence |
|---|---|---|---|---|
| P1 | `distributions/course-creator/skills/course-creator/scripts/course_check.py::validate_course` | `scripts/sdlc_check.py` (validate/check), `course_check.py::validate_all`, `scripts/test_course_check.py`, `scripts/test_slide_content.py` (tramite fixture) | firma e tipo di ritorno (lista di `Finding`) invariati; un corso self-study valido oggi resta senza ERROR | grep `validate_course`; guardia `test_guard_self_study_needs_no_guide`; `test_slide_content.test_valid_and_legacy_migration` |
| P2 | `distributions/course-creator/skills/course-creator/scripts/course_check.py::_content_contract` | solo `validate_course` (riga 451) | i finding esistenti (versione, delivery, efficacy, valore, unità) restano gli stessi con lo stesso testo; un corso legacy produce solo l'avviso legacy | grep `_content_contract`; batterie `test_slide_content.py` e `test_course_check.py` |
| P3 | `distributions/course-creator/skills/course-creator/scripts/course_check.py::validate_all` | `scripts/sdlc_check.py`, `scripts/test_course_check.py` | i corsi di questo repository restano a 0 finding | guardia `test_guard_this_repository_courses_stay_clean` |

## Security and Threat Model
Superfici toccate: accesso al filesystem, cioè i percorsi letti dalla guida, e dati personali, per il confine della Vision.
- **T1, percorso fuori dal progetto** (`../`, assoluto, link simbolico). Un percorso citato nella guida fa leggere al validatore file esterni. Mitigazione: nessuna unità, `/` iniziale o `..`, e `resolve().is_relative_to(root)`, che respinge anche un link che esce dal progetto. Dopo #R10 i Materiali non sono più confinati alla cartella del corso ma restano confinati al progetto; le citazioni `ai_docs/` restano confinate al pacchetto. Si verifica solo l'esistenza; la ricerca di un repository annidato elenca i nomi delle cartelle sotto un materiale dentro `ai_docs/`, senza leggerne il contenuto e senza scendere in link simbolici o junction di Windows (test `test_nested_repository_walk_does_not_follow_links`). Nessun contenuto entra nell'output. Probe: `test_red_material_outside_project_is_an_error`, `test_red_cited_path_outside_course_folder_is_an_error`; i test aggiungono `../`, assoluto, unità senza barra e link simbolico.
- **T2, dati dei partecipanti nel pacchetto.** La Vision esclude date, luoghi, iscrizioni, presenze, elenchi e dati dei partecipanti. Mitigazione: il modello non ha campi per loro e `templates.md`, superficie spedita, enuncia il divieto in proprio. Residuo dichiarato: il validatore non riconosce nomi o date in testo libero né nelle celle della Scaletta; li vede la review del corso.
- **T3, soluzioni mostrate agli allievi.** Mitigazione: regola 6, ogni unità di soluzione è nominata come riservata, e `Seen by` dichiara chi vede ogni materiale. Residuo: il validatore non sa cosa venga proiettato davvero.
- **T4, istruzioni nascoste nel materiale di riserva** (trascrizioni copiate dal web o registrate dall'agente). Il validatore controlla l'esistenza dei file, non li legge né li esegue. Il trattamento del loro contenuto resta governato dal confine della Vision sui comandi incorporati.
- **Falso positivo come rischio d'uso.** La regola 9 può bloccare un corso che, nella stessa riga in cui nomina il corso, cita la versione di un altro prodotto. Costo: l'autore riformula la riga. Accettato (#R8).

## Action Plan
- [x] Spostare i probe in `scripts/test_instructor_guide.py` (RED sulla baseline).
- [x] `course_check.py`: ritorno di `_content_contract`, `_delivery_package`, `_version_mentions` e riferimento confinato senza locator (GREEN).
- [x] `templates.md`: modello `INSTRUCTOR_GUIDE.md` con il confine. `SKILL.md`: riga Write Triggers. `slide_content.md` e `learning_design.md`: rimandi.
- [x] `README.md` della distribuzione e `skill_family_agent_workflows.md`; CHANGELOG `[Unreleased]`.
- [x] Batterie, probe, `check` della distribuzione e del repository.
- [x] Emendamento #R10 dopo la replica: Materiali in tutto il progetto, avviso sul repository annidato, citazioni nel pacchetto, righe `-` nella Scaletta, messaggi e modello (risultati E2E 1–7).
- [x] Chiusura: E2E script, review di chiusura, MERGE_REVIEW, Component Map, `mark distributions/`, indice; replica del proprietario sul corso reale (#R6).

## Test Strategy
- Unità AAA in `test_instructor_guide.py`: le regole 1–10, con ogni probe RED e ogni guardia, più le varianti `../`, assoluto, cartella come materiale, locator mancante, `Seen by` non valido, `Fallback material` `-` e fuori elenco, `S030` che non vale per `S03`, `text-content-v1` con `COURSE_CONTENT.md`, versione `4.0-content`, prefisso `v`, punteggiatura finale.
- Regressione: `python -m unittest discover -s distributions/course-creator/skills/course-creator/scripts -p "test_*.py"` (la batteria della lente course); la batteria eval `python -m unittest discover -s skills/agentic-sdlc-skill/scripts -p "test_*.py"` e i test node `scripts/test_*.js`, gate di rilascio di `GUIDE_release.md`.
- `python distributions/course-creator/skills/course-creator/scripts/sdlc_check.py check --root .` sul repository.
- Prova sul caso reale: replica del proprietario sull'altro PC (#R6), registrata nel Diary.

## Diary / Current State
**2026-10-29 — apertura.** Segnalazione d'uso (#R1), estesa al pacchetto (#R3). Vision emendata e approvata (#R4, #R7) dopo il blind check, 3 round con PASS. Domande sciolte: elenco verificato dei materiali (#R5), prova con fixture più replica del proprietario (#R6). Decisione dell'autore: la guida mancante è un ERROR e non un avviso. A favore: #R1 chiede che il caso sia segnalato e #R3 dice che è importante; il difetto nasceva dal non accorgersene. Contro: i corsi con docente esistenti falliscono finché non hanno la guida, che è esattamente il materiale che manca loro. Probe: 8 RED e 4 guardie verdi sulla baseline beta.14.

**2026-10-29 — design corretto dopo la review.** Review del design FAIL al round 1 e PASS al round 2; le correzioni sono registrate in REVIEW_LOG (2026-10-29, F-086 design). La voce di apertura è stata corretta nell'attribuzione del costo (#R1 e decisione dell'autore, non #R3). Il proprietario ha fissato la forma della regola 9 (#R8). Probe: 10 RED e 5 guardie verdi sulla baseline. Prossimo passo: conferma della review sulla regola 9 (corrispondenza del nome) e implementazione test-first.

**2026-10-29 — implementazione.** `course_check.py` implementa le regole 1–10 in `_delivery_package` e `_version_mentions`; `test_instructor_guide.py` ne copre i casi e i probe passano tutti. La review di chiusura (REVIEW_LOG 2026-10-29, F-086 closure) ha trovato quattro scostamenti dal design, corretti test-first: forma `/` delle cartelle nei Materiali, citazioni cercate in tutta la guida, testo del CHANGELOG limitato ai corsi con contratto, indici rigenerati. Le regole 8 e 9 dell'analisi ora descrivono il comportamento del codice. Resta la replica del proprietario sul corso reale (#R6, E2E S1–S2) e la decisione di merge.

**2026-10-30 — replica sul corso reale e emendamento.** S1 e S2 superati (report in `harness_instructor_guide/e2e_report_2026-10-30.md`). S2 è passato solo spostando `demo/` dentro la cartella del corso: due repository demo con il proprio `ai_docs/` sono entrati nella memoria del progetto (52 file fittizi, #R9), e il deck generato fuori da `ai_docs/` non poteva essere elencato. Causa: la regola 4 confinava i Materiali alla cartella del corso (#R5), mentre la Vision chiede «tutto il materiale che l'erogazione richiede». Il proprietario ha scelto l'opzione A (#R10), preferita a escludere le cartelle annidate dalla memoria condivisa, che avrebbe cambiato le quattro distribuzioni senza risolvere il deck. Corretti test-first anche i punti 3–7: messaggi che dicono cosa fare, righe `-` per pause e chiusura, posto per gli atti del docente, lingua, limite dichiarato sul rischio giusto. Il probe sul materiale fuori dalla cartella è ora sul materiale fuori dal progetto.

**2026-10-30 — chiusura.** Merge su `main` deciso dal proprietario (#R11): fast-forward a 1a5db5d6. Il proprietario ha rifatto S2 sotto #R10 (#R12). Prima dello spostamento il controllo dava un avviso di repository annidato per TH-01 e uno per TH-02. Con `demo/` nella radice, i Materiali scritti dalla radice e l'indice rigenerato, il corso ha 0 errori e 0 avvisi, `check` è CLEAN e la memoria del progetto non elenca più i 52 file dei progetti demo. L'avviso ha quindi segnalato il caso che l'aveva motivato, ed è sparito dopo la correzione. Le righe `-` della Scaletta sono state usate per pausa e chiusura. Lo spostamento sul PC del proprietario ha avuto un incidente dovuto al blocco di TortoiseGit, che il proprietario ha risolto e verificato con `git fsck`: non riguarda la skill. Restano dichiarati i residui della Functional Spec e la verifica dal vivo dell'uscita tramite symlink. Il rilascio della prossima beta di course-creator è una decisione separata.
