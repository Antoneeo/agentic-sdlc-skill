---
feature: F-086
analysis: ANALYSIS_instructor_guide.md
---
# E2E test: guida del docente per i corsi con docente

## What changed, in user terms
Un corso con docente (`Delivery mode: instructor-led`) deve uscire con `INSTRUCTOR_GUIDE.md`. La guida dice al docente cosa preparare, la scaletta, cosa non mostrare, cosa fare quando un passaggio dal vivo devia, cosa ripulire dopo, e quale materiale consegnare. Il controllo del corso rifiuta un corso con docente senza guida, un materiale citato che non è nella cartella del corso e una riga che nomina il corso con una versione diversa da quella dichiarata.

## Environment and preconditions
- course-creator installato dal branch `claude/f086-instructor-guide`, oppure dalla prima versione pubblicata che lo contiene (CHANGELOG `[Unreleased]`).
- Il corso `agente-personale-skills` nel progetto `C:\workspace\corso AI`, sull'altro PC del proprietario, nello stato segnalato in REQUEST_instructor_guide.md#R1: Course version 1.2, `instructor-led`, senza guida, con S38 che dice «versione 1.0».
- Il controllo si lancia dalla radice del progetto con `python <skill_dir>/scripts/sdlc_check.py check --root .`. `<skill_dir>` è la cartella della skill course-creator installata.

## New-behavior scenarios
### S1 — FS 1 e 9: il corso reale viene segnalato
Steps: 1. Lancia il controllo sul progetto `corso AI` così com'è.
Expected: un errore dice che il corso con docente richiede `INSTRUCTOR_GUIDE.md`. Un altro errore indica S38 con «course version 1.0; Course version is 1.2». Se S38 non viene segnalata, annota la riga esatta di S38: la regola guarda solo le righe che contengono la parola corso o course, lo slug `agente-personale-skills` oppure il titolo intero del corso.
Result:

### S2 — FS 2–8: la guida scritta dal modello passa
Steps: 1. Chiedi all'agente di scrivere `INSTRUCTOR_GUIDE.md` dal modello in `templates.md`. Elenca in `## Materials` i progetti demo e `TRASCRIZIONI_DI_RISERVA.md`, e in `## When something deviates` metti la riga del rischio di `P-TM.md` che corrisponde al problema di Codex in S12; se non esiste, aggiungilo prima sia a `P-TM.md` sia alla sezione `## Learning and Content Risks` dell'ANALYSIS del corso, perché il controllo richiede che ogni rischio sia definito in entrambi. 2. Correggi S38 alla versione 1.2. 3. Lancia di nuovo il controllo.
Expected: il controllo è pulito per il corso. Se la cartella `demo/` sta fuori dalla cartella del corso, il controllo la segnala come fuori dal pacchetto: spostala dentro.
Result:

### S3 — FS 4–5: un materiale mancante è visibile
Steps: 1. Rinomina temporaneamente un file elencato in `## Materials`. 2. Lancia il controllo. 3. Ripristina il nome.
Expected: un errore nomina il file come assente dal pacchetto consegnato; dopo il ripristino il controllo torna pulito.
Result:

### S4 — FS 6: una soluzione non riservata è segnalata
Steps: 1. Togli dalla sezione `## Reserved material` l'ID di un'unità di soluzione. 2. Lancia il controllo. 3. Ripristina.
Expected: un errore nomina quell'unità di soluzione.
Result:

### S5 — Il docente usa la guida
Steps: 1. Una persona che non ha preparato il corso legge solo `INSTRUCTOR_GUIDE.md` e apre i file che cita.
Expected: sa cosa preparare, cosa non proiettare, cosa fare se S12 si blocca e cosa ripulire dopo, senza chiedere all'autore. Ogni percorso apre un file esistente.
Result:

## Regression scenarios
### R1 — Corso in autoapprendimento
Steps: 1. Lancia il controllo su un corso `self-study` esistente senza guida, per esempio C-001 in questo repository: `python distributions/course-creator/skills/course-creator/scripts/sdlc_check.py validate --root .`.
Expected: `course: 0 error(s), 0 warning(s)`, come prima.
Result:

### R2 — Versione di uno strumento
Steps: 1. In un'unità scrivi «Serve Python versione 3.12». 2. Lancia il controllo.
Expected: nessun errore, perché la riga non nomina il corso.
Result:

### R3 — Corso senza contratto di contenuto
Steps: 1. Lancia il controllo su un corso legacy, che non dichiara `Content contract`.
Expected: solo l'avviso legacy già esistente, nessuna richiesta di guida.
Result:

## Already covered by automated tests
`distributions/course-creator/skills/course-creator/scripts/test_instructor_guide.py`: regole 1–10 (la 10 con un corso legacy che ha guida e versione superata), percorsi fuori dalla cartella, assoluti e con `..`, locator, `Seen by`, fallback, ID interi, contratto `text-content-v1`, versione `4.0-content`. Probe: `ai_docs/solutions/harness_instructor_guide/probe.py`. Batteria completa della lente course: `python -m unittest discover -s distributions/course-creator/skills/course-creator/scripts -p "test_*.py"`.
