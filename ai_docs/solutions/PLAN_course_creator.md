# course_creator — piano di implementazione F-058

> Per l'agente esecutore: leggere `ANALYSIS_course_creator.md` e la Vision APPROVED prima di ogni incremento. Eseguire gli incrementi in ordine, con un test rosso prima del codice e una review indipendente del diff prima di chiudere F-058. Questo piano è subordinato alla valutazione del proprietario sul design F-058.

**Obiettivo:** rendere installabile la quarta skill della famiglia, capace di far progettare spiegazioni progressive per destinatari definiti, con fonti verificabili, collaudo diagnostico indipendente e feedback reale.

**Architettura:** riusare il core/memoria condivisi, aggiungere un overlay didattico con artefatti e validator specialistico, e far convivere marketing e course su un unico `ai_docs/` senza due writer dello stesso indice. Il corso prodotto resta leggibile anche senza la skill. Nessuna dipendenza di rete per il funzionamento base; Python e Node standard library.

**Autorità:** `ai_docs/vision/features/VISION_course_creator.md` e `ai_docs/solutions/ANALYSIS_course_creator.md`. F-059 è COMPLETED; `domain: course` è già nel core.

## Vincoli comuni

- Nome di prodotto `course_creator`; nome installabile `course-creator`; pacchetto in `distributions/course-creator/`.
- Il confine L1 è stato approvato dal proprietario nella Functional Spec §8; il nuovo corso è L3.
- Per ogni nuovo corso la Vision canonica è `vision/features/VISION_course_<slug>.md`, l'unità governata è `solutions/ANALYSIS_course_<slug>.md` con `domain: course` e `## Learning and Content Risks`; i materiali vivono in `solutions/courses/<slug>/`. `P-TM.md` dettaglia i rischi per ID senza duplicare l'autorità dell'ANALYSIS.
- La prima versione della skill supporta Standalone. Espone la regola di non accettare automaticamente proposte devPNT e non presenta gli artefatti didattici come documenti governati Hybrid.
- I fatti insegnati hanno fonti riapribili. Il modello può orientare ricerca e formulazione, non certificare fatti.
- Il validator non promuove l'efficacia. La simulazione non prova apprendimento umano. Un corso può essere consegnato con «efficacia non verificata».
- Il drift guard deve attestare copie identiche di ogni file in `SHARED_FILES` nelle quattro skill.

## Focus della review di chiusura

1. Su `ai_docs/` invocare `index` alternando code, KB, marketing e course: gli indici condivisi rimangono identici e hanno un solo writer per percorso.
   Un progetto marketing che conserva un `ai_docs/INDEX.md` nel formato precedente riceve una diagnosi e un comando di migrazione esplicito; `validate/check` non lo riscrivono.
2. Su un progetto solo course, `mkt_check.py check --strict` non deve richiedere ledger o stati marketing; su un progetto misto un engagement incompleto deve invece produrre finding.
3. Un symlink o `../` in un riferimento didattico non può far leggere file fuori dalla radice del progetto.
4. Una risposta corretta del simulatore con controllo senza corso già riuscito non può trasformarsi in PASS diagnostico; nessuna simulazione trasforma il corso in «efficacia verificata».
5. Installazione, inizializzazione ripetuta e disinstallazione non devono sovrascrivere o cancellare file non attribuibili a `course-creator`.

## Task 1 — Router e quarta copia condivisa

**File:** `R/K/M/routing.md` e `R/K/M/SKILL.md`; `R/K/M/scripts/shared_files.py`; nuove copie sotto `distributions/course-creator/skills/course-creator/` dei 22 file in `SHARED_FILES`; i quattro `scripts/shared_manifest.json`; test drift e router nei pacchetti.

- [x] Aggiungere una prova di routing: corso da fonti fornite → course deciso al passo 1; ingestione del corpus → knowledge; copy persuasiva → marketing; codice della skill → code; richiesta corpus+corso → split. Testare separatamente code+course, KB+course e marketing+course come sole coppie installate; il testo delle tre `SKILL.md` deve attivare il router. Verificare che il router precedente non contenesse il ramo course.
- [x] Aggiungere riga, predicato, precedenze, split e casi a `routing.md`; aggiornare il rilevamento sibling nelle tre `SKILL.md`; creare la copia course. Eseguire la batteria verde. I worked examples course escono al passo 1, preservando l'invariante del ramo code.
- [x] Estendere `DISTRIBUTION_SKILL_DIRS` a quattro, copiare i file condivisi senza modificarli per la nuova lente, aggiornare i manifest. Provare `shared_files.py` e `test_drift.py` in tutte e quattro le copie.

## Task 2 — Compatibilità marketing sull'albero ai_docs

**File:** `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py` e `test_mkt_check.py`.

- [x] Aggiungere test di regressione: `ai_docs` course-only con Vision APPROVED e nessun ledger passa `index`, `validate` e `check --strict`; `ai_docs/INDEX.md` resta identico alternando entry point; una feature Vision marketing con tag o dominio effettivo ereditato dal `default_domain`, oppure un ledger, attiva i controlli marketing; Vision comune e feature Vision marketing APPROVED sono validate con gli stati del core, non con `VALID_STATUS` marketing; un indice legacy marketing già presente fallisce con istruzione di migrazione; `mkt_docs/` conserva output e codice d'uscita esistenti.
- [x] Adattare `cmd_index` al core come unico writer degli indici comuni su `ai_docs/`; lasciare `build_index` marketing solo su `mkt_docs/`.
- [x] Limitare su `ai_docs/` `run_validate` ai file marketing dichiarati e `run_check` agli engagement segnalati dal design. Comporre il codice di ritorno del core senza silenziare quello marketing. Eseguire GREEN e la batteria marketing esistente.

## Task 3 — Artefatti e validatore didattico

**File:** `distributions/course-creator/skills/course-creator/templates.md`, `scripts/course_check.py`, `scripts/test_course_check.py`, `scripts/sdlc_check.py`; fixture di corso in `ai_docs/solutions/harness_course_creator/`.

- [x] Fissare nei template campi e tabelle leggibili per Vision/ANALYSIS canoniche del corso, D-UC, D-IC, P-TM, grafo, piano, report di simulazione e feedback. Riferimenti a spiegazioni/fonti portano path e locator risolvibili; ID di concetto e modulo sono stabili.
- [x] Aggiungere test di regressione distinti per Vision di corso assente/DRAFT che blocca il design, ANALYSIS di corso assente/senza rischio `C-`, artefatto didattico mancante, arco a concetto inesistente, ciclo, prerequisito insegnato dopo l'uso, `PROVATO` senza evidenza, spiegazione/riferimento assente, path traversal e symlink esterno; un corso audio con percorso valido deve passare i controlli strutturali.
- [x] Implementare `validate_course(root, course_dir)` e `validate_all(root)` con finding file/ID/severità/motivo, letture confinate alla radice, senza pretendere di decidere qualità didattica o verità dei fatti. Eseguire la batteria verde.
- [x] Integrare `sdlc_check.py main(argv=None)` con core, memoria e validator course per `validate`/`check`; aggiungere comando focalizzato `course <slug>`. Provare le batterie condivise contro la nuova copia.

## Task 4 — Metodo della skill e prove comportamentali

**File:** `C/SKILL.md`, `C/learning_design.md`, `C/source_check.md`, `C/simulation.md`, `C/feedback.md`, `C/elicitation.md`, `C/ENFORCEMENT.md`, `C/evals/run_behavioral.py` e quattro scenari nominati nell'Impact.

- [x] Eseguire un baseline di agenti freschi senza la skill su richiesta da principiante, prerequisito omesso, spiegazione generica e feedback metodologico; conservare input/esito senza inventare un fallimento quando il baseline riesce.
- [x] Scrivere il contratto essenziale in `SKILL.md`: triage, guide router, Vision formativa, profilo, grafo, obiettivi e spiegazioni per modulo, fonti riapribili, review, simulazione, stato di efficacia, feedback. Caricare i supporti soltanto nella fase pertinente.
- [x] Ripetere gli scenari con la skill, annotando cosa cambia e i casi che restano inconcludenti. Eseguire il collaudo con due sessioni indipendenti e controllo senza corso su un corso generato dalla skill; nessun PASS del simulatore viene usato come prova di apprendimento umano.
- [x] Conservare prompt verbatim, pacchetti effettivamente visibili e accessi del collaudo. Il probe esplorativo già svolto non soddisfa questo requisito.

## Task 5 — Pacchetto e inizializzazione Standalone

**File:** i file di package, script e test elencati nell'Impact F-058; template della skill.

- [x] Aggiungere test in home temporanee per scoperta dei quattro client, installazione nel target `course-creator`, init create-only con `default_domain: course`, seconda init senza sovrascrittura, uninstall confinato, tarball completo.
- [x] Aggiungere `package.json`, licenze/NOTICE, `README.md`, `CHANGELOG.md`, estensione Gemini e script Node con path e messaggi course-specifici. Eseguire GREEN con `node scripts/test_clients.js` e `npm pack --dry-run`.


**Nota di esecuzione:** i test negativi e le fixture sono conservati e passano sulla versione finale; la cronologia test-rosso-prima-del-codice non è stata archiviata come prova separata.

## Task 6 — Integrazione e chiusura

**File:** i tre `templates.md` esistenti, i tre README/CHANGELOG esistenti, `publish_all.bat`, le GUIDE release e memoria, documenti strategici, ANALYSIS/diario, audit/review log e indici generati.

- [x] Eseguire le batterie delle quattro distribuzioni, golden regressions, prove course, router, packaging e check dell'albero; confrontare gli hash dei file condivisi.
- [x] Richiedere review indipendente del diff contro l'Impact, correggere i finding e ripetere la review dove necessario.
- [x] Aggiornare architettura, inventario delle skill, README e ADR per la scelta del writer unico; rigenerare gli indici, fare `mark` dopo la documentazione e ottenere `sdlc_check.py check` CLEAN.
- [x] Chiudere `ANALYSIS_course_creator.md`, rimuovere `HANDOFF_course_creator.md` e rigenerare il registro. Pubblicazione npm e installazione negli ambienti personali restano un'azione distinta dal pacchetto verificato localmente.
