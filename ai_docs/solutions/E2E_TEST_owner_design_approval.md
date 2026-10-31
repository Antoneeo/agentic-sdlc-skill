---
feature: F-087
analysis: ANALYSIS_owner_design_approval.md
---
# E2E test: il proprietario approva il design L3 prima del lavoro

## What changed, in user terms
Dopo il PASS finale della review del design, un'unità L3 si ferma. L'agente ti presenta un riassunto del design (cosa fa, per chi e attraverso quali superfici, cosa tocca, minacce, esito della review, percorso del design) e ti chiede se procedere. Solo un tuo sì, registrato nel request record con un'etichetta che comincia con `design approved`, porta l'ANALYSIS a `IN_PROGRESS`. Un'istruzione data prima di vedere il design non approva. In una sessione senza nessuno presente l'unità resta `BLOCKED on the user`. `validate` mostra un `[note]` per un L3 in lavorazione, iniziato dal 2026-10-31, senza approvazione registrata. Il messaggio di rifiuto del gate lo ricorda.

## Environment and preconditions
- Una delle quattro skill installata dal branch `claude/f087-owner-design-approval`, oppure dalla prima versione pubblicata che lo contiene (CHANGELOG `[Unreleased]`).
- Un progetto Standalone qualsiasi in cui aprire una piccola unità L3 nuova (`start_date` dal 2026-10-31).
- Il controllo si lancia dalla radice del progetto con `python <skill_dir>/scripts/sdlc_check.py validate --root .`.

## New-behavior scenarios
### S1 — FS 1–3: lo stop e la domanda
Steps: 1. Chiedi all'agente una piccola funzionalità L3. 2. Lascia che scriva l'ANALYSIS e faccia fare la review del design. 3. Quando la review passa, scrivi «vai avanti con l'unità».
Expected: l'agente non scrive codice e l'ANALYSIS resta `PLANNED`. Ti mostra il riassunto del design con il percorso dell'ANALYSIS e ti fa una sola domanda: se procedere.
Result:

### S2 — FS 3: il sì viene registrato
Steps: 1. Rispondi «sì» alla domanda di S1. 2. Apri il request record dell'unità.
Expected: c'è una voce nuova con la tua risposta verbatim e un'etichetta che comincia con `design approved`. Solo dopo l'ANALYSIS diventa `IN_PROGRESS` e l'agente comincia a scrivere codice.
Result:

### S3 — FS 5: il no rimanda il design in revisione
Steps: 1. Ripeti S1 su un'altra unità. 2. Rispondi con una correzione (per esempio «metti il pulsante altrove»).
Expected: la risposta è registrata con un'etichetta che non è `design approved`. L'agente rivede il design, dice se la review va rifatta su quella parte, e ti chiede di nuovo. Nessun codice.
Result:

### S4 — FS 9: l'avviso di `validate`
Steps: 1. In un progetto di prova, porta a mano a `IN_PROGRESS` un'ANALYSIS L3 con `start_date` 2026-11-02 e un request record senza voce `design approved`. 2. Lancia `validate`, poi `validate --strict`. 3. Aggiungi la voce `### R2 — 2026-11-02 — design approved` e rilancia.
Expected: al passo 2 una riga `[note]` nomina l'ANALYSIS e «design approval»; `--strict` esce con lo stesso codice di prima della modifica. Al passo 3 la riga sparisce.
Result: PASS, 2026-10-30, sui fixture di `harness_owner_design_approval/probe.py` (12 test OK) e di `scripts/test_design_approval.py` (18 test OK), in tutte e quattro le skill.

## Regression scenarios
### R1 — Unità esistenti
Steps: 1. Lancia `validate` su un progetto con unità L3 iniziate prima del 2026-10-31, per esempio questo repository.
Expected: nessun nuovo errore, warning o `[note]` sull'approvazione del design.
Result: PASS, 2026-10-30: `validate` su questo repository, 0 errori; nessuna riga «design approval».

### R2 — Hybrid e marketing
Steps: 1. Lancia `validate --hybrid` sul progetto di S4. 2. In un progetto marketing, chiedi una strategia fino al USER GATE della fase 6.
Expected: al passo 1 nessun `[note]` sull'approvazione. Al passo 2 il cliente riceve una sola domanda di approvazione della strategia, non due.
Result:

### R3 — Il gate
Steps: 1. Con il gate configurato (`ENFORCEMENT.md`), prova a modificare un percorso protetto senza un'ANALYSIS `IN_PROGRESS`.
Expected: la modifica è rifiutata come prima, con lo stesso codice d'uscita; il messaggio aggiunge che a L3 il passaggio a `IN_PROGRESS` segue l'approvazione del design.
Result: PASS, 2026-10-30, con il test `Gate.test_refusal_names_the_design_approval` in tutte e quattro le skill: codice d'uscita 2, il messaggio nomina «design approval». Il gate non è stato provato da un hook reale.
