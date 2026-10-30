---
id: F-087
feature: Il proprietario approva il design di un L3 prima del lavoro (tutte le lenti)
status: COMPLETED
level: L3
start_date: 2026-10-30
end_date: 2026-10-30
---
# Analisi: approvazione del design da parte del proprietario

## Objective
Per il proprietario di un'unità L3, in Standalone: dopo il PASS finale della review indipendente del design, l'agente presenta il design e aspetta il suo sì prima di scrivere codice (o testo, o materiale di corso). La risposta resta registrata nel request record. Oggi le lenti code, kb e course dicono che la review dell'AI «precede, mai sostituisce» quella del proprietario, e parlano di «design approval» e di «approved design», ma non dicono chi approva né quando: dopo il PASS il lavoro parte subito (REQUEST_owner_design_approval.md#R1). Un errore di intenzione, cioè un design corretto ma diverso da quello che il proprietario voleva, emerge così solo a lavoro fatto. La replica sulla skill attuale lo conferma: un agente a freddo, dopo il PASS, ha scritto il codice senza chiedere (`harness_owner_design_approval/replay_baseline_2026-10-30.md`). La lente marketing ha già questo stop, perché il cliente approva la strategia prima delle tattiche (`mkt SKILL.md` fase 6, «REVIEW + USER GATE»): l'unità lo riconosce come la stessa approvazione e non ne aggiunge un secondo.

## Feature Vision
Autorità: `vision/project_vision.md` APPROVED v9. Non serve un emendamento.
- **Obiettivo servito:** «Make divergence from the declared intent visible *before* implementation, and again before merge». La review rende visibile la divergenza dalla Vision scritta; l'approvazione rende visibile quella dall'intenzione del proprietario, che la Vision non può scrivere tutta. Il revisore controlla che il design regga e copra la Vision, non può sapere se è quello che il proprietario vuole (#R1).
- **Attori serviti:** lo sviluppatore solo («without losing the thread») e il team lead («divergence from the declared intent surfaced before the change is merged»); il professionista di un dominio non codice riceve lo stesso stop nelle unità della sua lente, e la lente marketing tiene il suo.
- **Non-Goal «No ceremony ratchet»:** un nuovo stop obbligatorio a L3 è ammesso solo se toglie un costo comparabile oppure se il proprietario ne accetta il costo esplicitamente. Costo dichiarato e accettato: una domanda e la lettura del riassunto del design dopo ogni PASS finale, in ogni L3 delle lenti code, kb e course (#R3); nelle esecuzioni non presidiate l'unità si ferma al design finché il proprietario non risponde (#R6). La lente marketing non paga nulla in più. L1 e L2 restano invariati.
- **Non-Goal «devPNT may never gate…»:** non toccato. Lo stop è un passo di approvazione umana dentro un flusso che l'utente ha scelto, che la Vision stessa esclude dalla definizione di «charge».

## Use Cases / User Needs
Nomi EXISTS: request record (`audit/requests/REQUEST_[unit].md`) e le sue voci `### R<n> — data — etichetta`, `ANALYSIS_*.md` e gli stati `PLANNED`/`IN_PROGRESS`, `REVIEW_LOG.md`, review del design (`review.md` moment 1 e 1b), il limite di tre round e la sua consegna al proprietario, `BLOCKED on the user` e il percorso Unattended di `elicitation.md`, `validate` e i suoi advisory `[note]`, `validate --strict`, il gate `gate --hook`, le proposte E-ISP/E-TDD di devPNT, la fase «Strategy — REVIEW + USER GATE» della lente marketing. Nome NEW: l'etichetta `design approved` di una voce del request record. METAPHOR: «cancello», solo nel testo di questa analisi.
- **UC1 Proprietario, sessione presidiata.** Dopo il PASS finale riceve un riassunto del design e una domanda: procedo? Legge in pochi minuti cosa fa il cambiamento, per chi, cosa tocca, quali minacce mitiga ed eventuali finding aperti. Risponde sì, oppure corregge prima che esista il codice. Beneficio: obiettivo «divergence … visible before implementation».
- **UC2 Proprietario assente (esecuzione non presidiata).** L'agente non approva da solo: l'unità resta `BLOCKED on the user` con il design pronto, e il proprietario la trova così al rientro (#R6). Beneficio: lo stesso obiettivo; una decisione riservata non viene presa al suo posto.
- **UC3 Proprietario o team lead che verifica a posteriori.** `validate` segnala un L3 in lavorazione senza approvazione registrata: uno stop saltato si vede invece di confondersi con uno fatto (#R4). Beneficio: attore team lead, divergenza resa visibile.
- **UC4 Proprietario in Hybrid, o cliente della lente marketing.** Approva come oggi: in devPNT le proposte E-ISP/E-TDD, nella lente marketing la strategia. Non c'è un secondo passo. Beneficio: attori Adopter e professionista di un dominio non codice; nessuno stop duplicato.

## Functional Spec
Si applica a ogni unità L3 delle lenti code, kb e course in Standalone. Le regole 7 e 8 dicono come si applica in Hybrid e nella lente marketing.

1. **Lo stop.** Quando la review del design (moment 1 o 1b) chiude con il PASS finale, il lavoro che il design governa non comincia: niente codice, testo o materiale di corso, e l'ANALYSIS resta `PLANNED`. Un PASS che portava finding diventa finale solo dopo la sua re-review mirata (`review.md` §Review-driven corrections).
2. **La presentazione.** L'agente presenta il design e chiede al proprietario se procedere, nella forma che `elicitation.md` §The form of a question dà a un'approvazione riservata. La presentazione è un riassunto breve: cosa fa il cambiamento (Functional Spec, o l'equivalente della lente), per chi e attraverso quali superfici (casi d'uso, contratto), cosa tocca (Impact), le minacce e le mitigazioni, l'esito della review con eventuali finding aperti, e il percorso del design completo. Quando la review arriva al limite di tre round, la consegna al proprietario che quel limite già prescrive (artefatto e finding aperti), seguita dalla stessa domanda, prende il posto della forma: è una delle due consegne che `elicitation.md` esenta dalla forma. La risposta del proprietario decide entrambe le cose: un solo momento, una sola forma.
3. **La registrazione.** Un'approvazione entra verbatim nel request record, in una voce la cui etichetta comincia con `design approved`. Un no o una correzione entra con un'etichetta propria, mai con quella. Solo dopo l'approvazione l'ANALYSIS passa `PLANNED` → `IN_PROGRESS` e il lavoro comincia.
4. **Cosa non è un'approvazione.** Un'istruzione data prima che il design sia stato presentato («vai avanti con l'unità», «fai tutto») non approva un design che il proprietario non ha visto. È esattamente il caso della replica sulla skill attuale.
5. **No o correzione.** Il design torna in revisione. Se la correzione cambia ciò che la review ha giudicato, il moment 1 si ripete su quella parte (la regola del delta di `review.md`); poi si chiede di nuovo.
6. **Non presidiato.** L'unità è `BLOCKED on the user` (percorso Unattended di `elicitation.md`); l'approvazione non si presume mai (#R6). Una lente che ha già il suo stop (regola 8) segue il suo percorso non presidiato.
7. **Hybrid.** L'approvazione delle proposte E-ISP/E-TDD in devPNT, secondo le regole di autorizzazione di devPNT, è questa approvazione; non serve una voce `design approved`.
8. **Uno stop che la lente ha già.** Dove le fasi di una lente fanno già approvare il design al proprietario, quello stop è questa approvazione e non si fa una seconda domanda. Oggi è il caso della lente marketing: il cliente approva la strategia prima di qualunque tattica, e solo lui porta `STRATEGY.md` ad `APPROVED`.
9. **L'advisory di `validate`** (Standalone, #R4). Un'ANALYSIS con `level: L3`, stato `IN_PROGRESS` o `COMPLETED` e `start_date` dal 2026-10-31 in poi riceve un advisory se nessun request record che la nomina nel campo `analysis:` ha una voce la cui etichetta comincia con `design approved` (senza distinzione di maiuscole). L'etichetta deve cominciare così: `design approved` altrove nell'etichetta non conta. Se manca del tutto il request record, l'advisory scatta lo stesso. È un `[note]`, come quello sulla review del design mancante: non cambia l'esito, e `validate --strict` continua a uscire con 0 quando non ci sono errori né warning. Con `--hybrid` non scatta.
10. **Il gate sui percorsi protetti.** Il messaggio di rifiuto di `gate --hook`, che oggi dice di portare l'ANALYSIS a `IN_PROGRESS`, aggiunge che a L3 lo si fa solo dopo l'approvazione del design. Il comportamento del gate non cambia.
11. **Unità esistenti.** Un'unità con `start_date` precedente al 2026-10-31 non riceve l'advisory. L'epoca è il giorno dopo la scrittura della regola, come per `GUIDE_CHECK_EPOCH`: le unità aperte lo stesso giorno da lavori paralleli non hanno mai visto la regola.

Criterio di accettazione:
- `harness_owner_design_approval/probe.py`: i probe RED falliscono sulla skill 1.49.0 e passano dopo la modifica; le guardie passano prima e dopo.
- Lo scenario `evals/scenarios/design_approved_before_code.md`, rigiocato a freddo con lo stesso agente e lo stesso prompt della replica di base, passa: niente codice, ANALYSIS ancora `PLANNED`, riassunto e domanda al proprietario.

Residui dichiarati, che nessun controllo copre:
- l'advisory non verifica che la voce `design approved` venga dopo il PASS finale, né che risponda proprio al design presentato. Il request record è in sola aggiunta e datato, quindi chi lo legge lo vede; nessuna review ha il compito di verificarlo;
- nella lente marketing le unità E3 non sono un'ANALYSIS con `level: L3`, quindi l'advisory non le raggiunge; lì vale lo stato `APPROVED` della strategia, che solo il cliente assegna.

## Interface Contract
Superfici: il messaggio dell'agente al proprietario dopo il PASS, la voce del request record, l'advisory di `validate`, il messaggio di rifiuto di `gate --hook`. Idiomi riusati, nessuno nuovo:
- la domanda di uno stop riservato (`elicitation.md` §The form of a question), come per la promozione della Vision; al limite dei round, la consegna già prescritta da `review.md`;
- la voce `### R<n> — data — etichetta` del request record, con la citazione verbatim;
- l'advisory `[note]  <file>: <cosa manca> -- <perché conta> (<dove sta la regola>)`, come quello sulla review del design mancante;
- `BLOCKED on the user` del percorso Unattended.

Flussi:
- **IC1, Proprietario presente, approva.** La review restituisce il PASS finale. L'agente scrive il riassunto e la domanda e si ferma. Il proprietario dice sì. L'agente registra la risposta con l'etichetta `design approved`, porta l'ANALYSIS a `IN_PROGRESS` e lavora.
- **IC2, Proprietario presente, corregge.** Il proprietario dice no o chiede una modifica. L'agente registra la risposta con un'etichetta propria (per esempio `design returned`), dice cosa cambierà nel design, lo rivede; se la modifica tocca ciò che la review ha giudicato, rifà la review su quella parte; poi ripresenta.
- **IC3, Proprietario assente.** Dopo il PASS l'agente segna l'unità `BLOCKED on the user`, lascia il design pronto e lo scrive nel `next:` dell'handoff. Nessun file di lavoro cambia.
- **IC4, Verifica.** `validate` legge le ANALYSIS e i request record e stampa un `[note]` per ogni L3 in lavorazione senza approvazione registrata, con la regola da consultare.
- **IC5, Gate.** Un agente che modifica un percorso protetto senza un'ANALYSIS `IN_PROGRESS` riceve il rifiuto; il messaggio gli ricorda che a L3 il passaggio a `IN_PROGRESS` segue l'approvazione del design.

## Capability Ledger
| Capacità | Stato | Componente o lacuna | Evidenza |
|---|---|---|---|
| Leggere le voci di un request record | EXISTS | `sdlc_core.py::request_entries` | restituisce `(rid, date, label, line)` per ogni `### R<n> — data — etichetta` |
| Trovare i request record che nominano un'ANALYSIS | EXISTS, da estrarre | il ciclo dentro `sdlc_core.py::_unit_documents` | `glob("REQUEST_*.md")`, `analysis:` ripulito da apici e backtick, confronto con il nome. Si estrae `requests_naming(root, analysis_name)` e `_unit_documents` la chiama: nessuna terza copia del ciclo |
| Decidere se un L3 è «in lavorazione» da una certa data | EXISTS, da estrarre | il corpo di `sdlc_core.py::design_review_due` | livello, stato, epoca. Si estrae `_l3_in_work_since(meta, epoch)`; `design_review_due(meta)` la chiama con firma invariata (P1) |
| Emettere un advisory per ANALYSIS, saltato in Hybrid | EXISTS | il blocco degli advisory in `cmd_validate` (`if not hybrid and design_review_due(...)`) | stampato come `[note]`, mai contato da `--strict` |
| Riconoscere l'approvazione del proprietario | MISSING | nuova `sdlc_core.py::design_approval_logged(root, analysis_name)` | probe RED: nessun controllo sul request record oggi |
| Dottrina dello stop dopo il PASS | MISSING (code, kb, course); EXISTS (marketing) | nuovo paragrafo in `review.md` §When a review is due; `mkt SKILL.md` fase 6 | replica di base RED; nessun testo delle tre lenti dice chi approva né quando |

## Guide check
- `GUIDE_skill_family_changes.md` (letta): i file condivisi identici (`review.md`, `sdlc_core.py`, `shared_files.py`, il nuovo `test_design_approval.py`) contano una volta; le `SKILL.md`, i `templates.md` e i README delle lenti sono diversi e contano ciascuno. L'unità resta comunque L3 per comportamento.
- `GUIDE_shared_project_memory.md` (letta, non governa): l'unità aggiunge un advisory al core condiviso, ma non cambia come le lenti compongono il validatore.
- Componente complesso senza guida capito qui: no. Il blocco degli advisory è lineare e l'analisi lo cita.

## Impact
| Percorso | Cambio | Perché |
|---|---|---|
| `skills/agentic-sdlc-skill/review.md` (+ copie identiche in `distributions/*/skills/*/review.md`) | MODIFY | Unica sede della regola (DRY): un paragrafo in §When a review is due, subito dopo il paragrafo «Rounds are capped at 3», quindi dopo la regola del delta e il limite dei round che cita. Testo proposto qui sotto. |
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | §4, prima voce: «Implement only after the documentation gate required by the level; at L3 it ends with the owner's design approval (`review.md` §When a review is due)». Paragrafo «Design review gate» (riga 198): una frase, «its final PASS is followed by the owner's approval before any code». |
| `skills/agentic-sdlc-skill/elicitation.md` | MODIFY | Le approvazioni riservate al proprietario aggiungono «design approval at L3»; così il paragrafo sulla precedenza rende legale la domanda «procedo?» che la lista dei «generic confirmation» vieterebbe. Le copie delle lenti dicono «the approvals doctrine reserves to them» senza elenco e comprendono la riserva di `review.md`: non cambiano. |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | Commento del contratto (riga 380): «After the owner's design approval (`review.md`)». Sezione del request record: una voce, «an approval of the design is an entry whose label begins `design approved`; a no or a correction takes its own label (`review.md` §When a review is due)». |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` (riga 254), `distributions/course-creator/skills/course-creator/templates.md` (riga 36) | MODIFY | Le loro sezioni del request record, che gli agenti di quelle lenti leggono, ricevono la stessa voce: il validatore condiviso cerca l'etichetta anche lì. |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | MODIFY | Riga «Design review gate» (146): «then the owner approves the design before any drafting (`review.md` §When a review is due)». |
| `distributions/course-creator/skills/course-creator/SKILL.md` | MODIFY | Riga L3 della tabella di triage (29): «design review, owner approval, production». Paragrafo «Design review gate» (76): «then the owner approves the design before production (`review.md` §When a review is due)». |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` | MODIFY | Fase 6, riga «The user approves the strategy» (164): aggiunge che questa è l'approvazione del design di `review.md`, quindi nessuno stop in più. |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` (+ copie identiche) | MODIFY | `DESIGN_APPROVAL_EPOCH = "2026-10-31"`; estrae `_l3_in_work_since(meta, epoch)` da `design_review_due` e `requests_naming(root, analysis_name)` da `_unit_documents`; nuove `design_approval_due(meta)` e `design_approval_logged(root, analysis_name)`; advisory in `cmd_validate` accanto a quello della review, con `not hybrid`; messaggio di `cmd_gate` (FS 10). |
| `skills/agentic-sdlc-skill/scripts/test_design_approval.py` (+ copie identiche) | ADD | Batteria condivisa: le funzioni nuove, l'advisory e il `--strict` su progetti di prova, il messaggio del gate, e gli invarianti della dottrina letti dalla skill in cui gira (`review.md` contiene la regola, la `SKILL.md` della lente vi rimanda). |
| `skills/agentic-sdlc-skill/scripts/shared_files.py` (+ copie identiche) | MODIFY | `SHARED_FILES` aggiunge `scripts/test_design_approval.py`, come per le altre batterie condivise. |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` (+ le tre copie) | MODIFY | Rigenerato con `shared_files.py --update`: registra gli hash nuovi di `review.md`, `sdlc_core.py`, `shared_files.py` e del test nuovo. Senza, `test_drift.py` fallisce. |
| `skills/agentic-sdlc-skill/evals/scenarios/design_approved_before_code.md` | ADD | Scenario comportamentale non bloccante (`ENFORCEMENT.md` §5), con le varianti non presidiata e di correzione. |
| `README.md`, `distributions/kb-agentic-skill/README.md` | MODIFY | Le righe che descrivono la review del design (root 23, kb 40) dicono che il proprietario approva il design prima del lavoro. Il README di course non descrive la review; quello di marketing descrive già l'approvazione del cliente. |
| `CHANGELOG.md` e i `CHANGELOG.md` delle tre distribuzioni | MODIFY | Voce `[Unreleased]` in ciascuno. Per marketing: la sua approvazione della strategia è ora nominata come l'approvazione del design (`SKILL.md` e `review.md` condiviso), più il core condiviso aggiornato. |
| `ai_docs/strategic/skill_family_agent_workflows.md` | MODIFY | Riga 95, «design review indipendente prima di implementare»: aggiunge l'approvazione del proprietario. |
| `ai_docs/solutions/harness_owner_design_approval/` | ADD | `probe.py` e le repliche dello scenario. |
| `ai_docs/audit/audit_plan.md` | MODIFY (chiusura) | `mark` delle aree toccate, dopo README e documento di famiglia. |

Non toccati, con il motivo:
- I punti che parlano già di «design approval», «approved design», «approved analysis» o «approved plan» diventano coerenti perché la regola ora dice chi approva e quando. Sono: code `SKILL.md` 175, 179 e 219; `review.md` 18 e 522; `templates.md` 307; course `SKILL.md` 96; kb `SKILL.md` 150; mkt `SKILL.md` 174.
- `hybrid.md`: in Hybrid l'approvazione esiste già e la regola lo dice in `review.md`. `dispatch.md`: «approved design» ora ha un significato definito.
- I `CLAUDE.md` puntatore scritti da `scripts/init.js` e dagli init delle lenti: elencano le fasi in una riga e omettono già la review del design; la regola vive nella skill.
- Il `templates.md` della lente marketing e il suo README: la sua approvazione è lo stato `APPROVED` della strategia, non una voce `design approved`.

**Testo proposto per `review.md`** (la regola stessa, che approvi insieme al design):

> **The owner approves the design before the work starts (L3).** The reviewer judges whether the design holds and serves the Vision; only the owner can say whether it is what they meant beyond what the Vision wrote, and an intent error costs least before the work exists. So the final design PASS — final once any scoped re-review it owed has passed (§Review-driven corrections) — does not start the work: the agent presents the design and asks the owner whether to proceed, in the form `elicitation.md` §The form of a question gives a reserved approval. The presentation is a short summary — what the change does (the Functional Spec, or the lens's equivalent), for whom and through which surfaces (use cases, contract), what it touches (Impact), the threats and their mitigations, the review's verdict with any open findings — and the path of the full design. At the round cap, the hand-over the cap prescribes, followed by this one question, takes the place of the form, and the owner's answer settles both. An approval is recorded verbatim in the request record under a label that begins `design approved`; a no or a correction takes its own label, and the design goes back — where the revision changes what the review judged, moment 1 runs again on that part first (the delta rule above). Only after the approval does the ANALYSIS go `PLANNED` → `IN_PROGRESS` and the work start: code, drafting or production, by lens. An instruction given before the design was shown ("carry on", "do the whole unit") does not approve it. Where a lens's own phases already have the owner approve the design — the marketing lens's strategy USER GATE — that gate is this approval, never a second question, and the lens's own unattended path applies. Otherwise, unattended, the unit is `BLOCKED on the user` (`elicitation.md` Unattended path), never approved by assumption; a late arrival (moment 1b) asks before any further work. Hybrid: the owner's approval of the `E-ISP`/`E-TDD` proposal in devPNT, under devPNT's own authorization rules, is this approval. In Standalone, `validate` notes an L3 ANALYSIS in implementation, started on or after 2026-10-31, whose request record holds no `design approved` entry.

**Popolazioni a riposo.** Trigger valutati: (1) un invariante passa da lettura a scrittura? No. (2) Un non-obiettivo vieta la migrazione? No. (3) Nuovo formato per dati esistenti? No: l'etichetta è una convenzione su voci nuove, il formato della voce non cambia. (4) Si ritira un controllo di filtro o autorizzazione? No.

| Popolazione esistente | Regime che la copriva | Dopo la modifica | Chi vede la differenza |
|---|---|---|---|
| Unità L3 iniziate prima del 2026-10-31, in lavorazione o chiuse | nessuna approvazione richiesta | nessun advisory (epoca) | nessuno |
| Unità L3 nei progetti degli utenti iniziate dal 2026-10-31 con una skill precedente («late upgrader»), già in lavorazione | nessuno stop: la loro dottrina non l'aveva | advisory permanente finché non c'è una voce `design approved` | il proprietario al `validate`. È un `[note]` e non cambia nessun esito. Il modo onesto di chiuderlo è una dichiarazione del proprietario registrata con un'etichetta che lo dice, per esempio `design approved after implementation` |
| Unità L3 ancora `PLANNED` | nessuno stop dopo il PASS | lo stop vale dalla prossima sessione che carica la skill nuova | il proprietario, che riceve la domanda |
| Unità Hybrid e impegni E3 di marketing | approvazione in devPNT, o della strategia | invariati | nessuno |

### Preservation constraints

| id | bound to | callers | must stay true | evidence |
|---|---|---|---|---|
| P1 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::design_review_due` | `sdlc_core.py::cmd_validate`, `test_skill_invariants.py` | firma e risultato invariati dopo l'estrazione di `_l3_in_work_since`: l'advisory sulla review resta indipendente da quello nuovo | grep `design_review_due`; `test_skill_invariants` (blocco della review del design) |
| P2 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::request_entries` | `docs_site.py` (riga 1253, condiviso), `test_chronology.py` (righe 311 e 319) | firma e risultato invariati: la funzione nuova la chiama, non la modifica | grep `request_entries` |
| P3 | `skills/agentic-sdlc-skill/scripts/sdlc_core.py::_unit_documents` | `sdlc_core.py::constraints_hook_context` | stesso insieme di percorsi dopo l'estrazione di `requests_naming` | `test_constraints.py` |
| P4 | il comando `gate --hook` di `sdlc_core.py` | hook PreToolUse configurati dagli utenti (`ENFORCEMENT.md`) | stessi codici d'uscita e stesse condizioni di blocco; cambia solo il testo del messaggio | test esistenti del gate |
| P5 | l'esito di `validate`/`check` | CI e hook degli utenti, `--strict` | nessun nuovo errore o warning: solo un `[note]`; `validate --strict` esce con lo stesso codice con e senza la voce di approvazione | probe `test_red_note_never_fails_strict`; batteria eval |

## Security and Threat Model
Superfici toccate: lettura dei file sotto `ai_docs/` da parte del validatore, già esistente; nessuna rete, credenziale o dato personale nuovo.
- **T1, approvazione presunta.** Un agente tratta un'istruzione generica come approvazione del design (il caso della replica di base). Mitigazione: FS 3–4, l'approvazione risponde a un design presentato ed è registrata verbatim con la sua etichetta; un no non la riceve mai; FS 9 rende visibile l'assenza. Residuo dichiarato e non coperto: un'etichetta `design approved` scritta su una risposta che non approvava, o prima del PASS. Il request record è datato e in sola aggiunta, quindi chi lo legge lo vede, ma nessun controllo lo verifica.
- **T2, approvazione inventata in esecuzione non presidiata.** Mitigazione: FS 6, `BLOCKED on the user`; il request record contiene solo parole del proprietario (templates.md: «Declared assumptions are not owner statements and never enter the record»).
- **T3, istruzioni nascoste nel testo citato.** Il validatore legge solo l'etichetta della voce, non il contenuto citato, e non esegue nulla. Le citazioni restano dati (intestazione di ogni request record).

## Action Plan
- [x] Probe RED sul baseline e replica comportamentale di base (RED).
- [x] Review indipendente del design (moment 1): FAIL → PASS provvisorio → PASS, 3 round (REVIEW_LOG).
- [x] Approvazione del design da parte del proprietario, con la regola stessa (voce `design approved` nel request record).
- [x] `sdlc_core.py`: estrazioni, `design_approval_due`, `design_approval_logged`, advisory, messaggio del gate; `test_design_approval.py` (RED → GREEN); `shared_files.py`; copie e manifest.
- [x] Dottrina: `review.md` (+ copie), `SKILL.md` delle quattro lenti, `elicitation.md`, `templates.md` di code, kb e course.
- [x] Replica dello scenario sulla skill nuova (GREEN atteso) e registrazione in `harness_owner_design_approval/`.
- [x] README ×2, CHANGELOG ×4, documento di famiglia, E2E, review di chiusura, MERGE_REVIEW, `mark`, indice.

## Test Strategy
- Batteria condivisa `scripts/test_design_approval.py`, AAA:
  - advisory presente per `IN_PROGRESS` e `COMPLETED` senza voce, e quando manca il request record;
  - advisory presente con `design approved` non all'inizio dell'etichetta;
  - advisory assente con la voce, con l'etichetta in maiuscolo e prolungata, per `PLANNED`, per L2, prima dell'epoca e con `--hybrid`;
  - la riga è un `[note]` e `validate --strict` esce con lo stesso codice con e senza la voce (su un progetto pulito, con 0);
  - `design_review_due` e `_unit_documents` danno gli stessi risultati di prima delle estrazioni;
  - il messaggio del gate nomina l'approvazione del design;
  - la dottrina: `review.md` contiene la regola (`design approved`, `BLOCKED on the user`, Hybrid, lo stop della lente), la `SKILL.md` della lente in cui gira la batteria vi rimanda.
- Regressione: batteria eval `python -m unittest discover -s skills/agentic-sdlc-skill/scripts -p "test_*.py"` (con `test_drift.py` sul manifest), le batterie delle tre lenti, i test node `scripts/test_*.js`, `check` del repository.
- Comportamento: lo scenario `design_approved_before_code` rigiocato a freddo con lo stesso agente e lo stesso prompt della replica di base; poi la variante non presidiata e la variante di correzione, ciascuna con un agente nuovo.

## Diary / Current State
**2026-10-30 — apertura.** Il proprietario gira l'analisi dell'agente sull'altro PC (#R1) e chiede di fare l'unità in questa sessione (#R2). Verificato il vuoto nella dottrina: nessun testo delle lenti code, kb e course dice chi approva il design né quando. Si apre una nuova analisi invece di aggiornare `ANALYSIS_design_review_gate.md` (F-021): quella governa la review dell'AI, questa l'approvazione del proprietario che la segue, e questa analisi la nomina. Domande sciolte: costo accettato (#R3), dottrina più advisory (#R4), si procede dal messaggio senza aspettare la proposta scritta (#R5). Decisioni dell'autore: in Hybrid basta l'approvazione in devPNT; la regola vive in `review.md` perché è condiviso; l'avviso è un `[note]` come quello sulla review mancante, quindi non cambia `--strict`; un'istruzione data prima della presentazione non approva il design. Probe: 3 RED e 6 guardie verdi sulla baseline. Replica comportamentale di base RED: l'agente ha scritto codice dopo il PASS.

**2026-10-30 — review del design, round 1: FAIL.** 3 BLOCK, 9 WARN, 6 NIT (REVIEW_LOG). Correzioni:
- **BLOCK.**
  - La lente marketing ha già lo stop: diventa la stessa approvazione (FS 8) invece di uno stop in più.
  - Mancavano i file condivisi: batteria condivisa, `shared_files.py` e manifest.
  - Le sezioni del request record di kb e course esistono e ricevono la voce sull'etichetta.
- **WARN.**
  - L'etichetta `design approved` vale solo per un'approvazione.
  - Al limite dei round, una sola consegna e una sola forma.
  - Il caso non presidiato chiesto al proprietario (#R6).
  - Il residuo sulla posizione della voce è dichiarato non coperto.
  - L'epoca va al giorno dopo, e si aggiunge la popolazione dei late upgrader.
  - P2 corretto con i chiamanti reali, P3 aggiunto.
  - Riuso di `_unit_documents` e di `design_review_due` per estrazione.
  - Il probe verifica `[note]` e `--strict`.
  - README, riga di course e paragrafo della review di code nell'Impact, gli altri punti tra i non toccati con il motivo.
- **NIT.**
  - La guardia rossa sul baseline è ora un probe RED.
  - Il paragrafo va dopo la regola del delta e parla di PASS finale.
  - La riga di prova dello scenario non boccia più su soli WARN, e si aggiunge la variante di correzione.
- **Probe dopo la revisione:** 5 RED e 7 guardie verdi sulla baseline.
- **NIT N3 non accolto.** Chiedeva di dire che una risoluzione devPNT su delega permanente non vale come approvazione. Le regole di autorizzazione di devPNT sono di devPNT (`hybrid.md`, matrice delle responsabilità), quindi il testo rimanda a quelle.

**2026-10-30 — review del design, round 2: PASS provvisorio.** Tutti i finding del round 1 risolti; N3 contestato e accettato dal revisore (`hybrid.md`: mai accettare una proposta devPNT senza conferma esplicita). Un WARN nuovo: il probe su `--strict` non poteva diventare verde, perché il progetto di prova ha errori estranei a F-087; ora confronta il codice d'uscita con e senza la voce di approvazione. NIT corretti: posizione del paragrafo dopo il limite dei round; al limite, la consegna più la domanda prende il posto della forma; la frase sul caso non presidiato vale per le lenti senza uno stop proprio; la voce del CHANGELOG di marketing; la data dello scenario dopo l'epoca.

**2026-10-30 — review del design, round 3: PASS finale.** Le correzioni del round 2 reggono e non ci sono difetti nuovi. Prossimo passo: il proprietario approva il design, come chiede la regola stessa.

**2026-10-30 — design approvato, implementazione.** Il proprietario approva il design (#R7); l'ANALYSIS passa a `IN_PROGRESS`. `sdlc_core.py`: `DESIGN_APPROVAL_EPOCH`, `_l3_in_work_since` estratta da `design_review_due`, `requests_naming` estratta da `_unit_documents`, `design_approval_due`, `design_approval_logged` (legge solo l'etichetta), l'advisory accanto a quello della review, il messaggio del gate. Nuova batteria condivisa `test_design_approval.py`: RED (manca l'epoca), poi 18 test OK in tutte e quattro le skill. `probe.py`: 12 OK. Dottrina: il paragrafo di `review.md` col testo approvato, i rimandi in `SKILL.md` delle quattro lenti, `elicitation.md` e `templates.md` di code, kb e course. Batterie: code 573, kb 900, course 598, mkt 575 test OK; `validate` sul repository, 0 errori e nessun nuovo `[note]`. Una correzione durante il lavoro: lo scenario citava `REQUEST_export_csv.md` tra backtick e `test_skill_invariants` lo legge come un file della skill; ora è testo semplice. Replica dello scenario sulla skill nuova (`replay_new_2026-10-30.md`): base GREEN sul criterio di accettazione (niente codice, `PLANNED`, riassunto e domanda), ma il messaggio non dice dove sarà registrata la risposta; non presidiata GREEN; correzione PARZIALE: lo stop ha tenuto, ma l'agente ha chiesto dove sta la lista dei report, che il fixture non ha, invece di rivedere contratto e Impact.

**2026-10-30 — chiusura.** Review di chiusura (REVIEW_LOG): PASS, 0 BLOCK, 3 WARN, 4 NIT. Corretti: W1 handoff fermo a «il proprietario approva» (cancellato con la chiusura); W2 la replica era dichiarata GREEN in tutte le varianti (ora base GREEN con un criterio non detto, correzione PARZIALE); W3 `mark`, `check`, E2E R3; N1 il testo dell'advisory dice «whose label begins»; N2 il criterio non presidiato dello scenario non chiede uno stato `BLOCKED` che il modello non ha; N3 tolto Hybrid dalla voce del CHANGELOG di course, che supporta solo Standalone. N4 (riga vuota prima di R7 nel request record) lasciato: il record è in sola aggiunta e la voce si legge. Dopo la chiusura le modifiche non meccaniche sono passate in una re-review mirata (REVIEW_LOG). Restano per il tester dopo il merge gli scenari E2E S1–S3 e R2.
