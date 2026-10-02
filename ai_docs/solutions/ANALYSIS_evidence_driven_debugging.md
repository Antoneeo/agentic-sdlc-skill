---
id: F-061
feature: Evidence-driven debugging and clean Poka-Yoke correction
status: COMPLETED
level: L3
domain: code
start_date: 2026-10-02
end_date: 2026-10-02
---
# F-061 — Debugging fondato sulle evidenze

## Objective

Correggere il percorso diagnostico di agentic-sdlc: partire dal guasto osservato,
mantenere ipotesi ordinate per probabilità motivata e costo di verifica,
confermare il meccanismo e correggere il disegno con Poka-Yoke senza regressioni.
L'utente segnala modelli che cercano difetti possibili nel sorgente anziché
diagnosticare l'incidente dai log locali. Il segnale è una testimonianza, non una
misurazione comparativa. Le prove di questa unità sono sintetiche e circoscritte.

## Feature Vision

La Vision APPROVED in `ai_docs/vision/project_vision.md` richiede comprensione
prima del cambiamento, prevenzione della myopia e costo proporzionato al rischio.
L'attore è lo sviluppatore che lavora con un agente. Non cambiano Vision, triage,
autorità di approvazione, servizi, dipendenze o condizioni commerciali.
Il registro contiene ipotesi causali dentro un solo bug; non ordina documenti,
assegna lavoro o aggiunge un work-management system. La precedente tranche
F-034 (`ANALYSIS_execution_integrity.md`) rinviava il rafforzamento del debugging
al successivo intervento motivato: questo è il nuovo segnale concreto.
Placement: r14 (bounded maintenance) governa il rafforzamento del proprietario
esistente. Distinzione da r2/r3: ordinare verifiche dentro un incidente non aggrega
lo stato di documenti, non assegna lavoro e non ordina workstream.
Costo aggiunto: registro leggero per ogni bug L2/L3, motivazione delle verifiche e
verifica del disegno; nessun nuovo artefatto obbligatorio o gate automatico per gli
adottanti. Il testo aggiuntivo resta nel supporto caricato per bug, con un solo
richiamo anticipato nel contratto. L'utente ha approvato questo percorso nella
conversazione del 2026-10-02; nessuna pubblicazione è autorizzata.

## Use Cases / User Needs

- UC1: diagnosticare un incidente dai dati disponibili senza correggere un difetto
  estraneo trovato nel sorgente.
- UC2: scegliere verifiche probabili ed economiche, conservando risultati e
  ipotesi invalidate senza ripeterle o confondere assenza di prova con smentita.
- UC3: indagare guasti intermittenti e concause senza inventare una catena unica
  di cinque risposte o dichiarare risolto ciò che non è verificabile.
- UC4: correggere responsabilità e invarianti al punto giusto, mantenendo validi
  gli altri comportamenti e limitando il cambiamento al necessario.

## Current Defects

Fonte: `skills/agentic-sdlc-skill/debugging.md`, Method e Circuit breaker;
`skills/agentic-sdlc-skill/SKILL.md`, Development and Testing.

| Difetto del testo attuale | Effetto possibile | Correzione proposta |
|---|---|---|
| Nessuna raccolta iniziale esplicita di log e configurazione effettiva | Ricerca statica estranea al guasto | Evidenze locali disponibili prima delle ipotesi |
| Meccanismo nominato senza criterio causale esplicito | Plausibilità scambiata per conferma | Predizione discriminante, prova e limiti |
| Nessun registro o ordinamento delle ipotesi | Ripetizioni, ancoraggio, verifiche costose premature | Registro aggiornato e priorità probabilità/costo |
| Riproduzione deterministica sempre obbligatoria | Blocco su incidenti intermittenti | Riproduzione quando possibile; evidenza alternativa dichiarata |
| Grafo statico trattato come tracciamento dell'esecuzione | Chiamante possibile scambiato per chiamante eseguito | Distinguere struttura da traccia runtime; testo come copertura |
| Fix alla causa senza criterio di disegno | Eccezione dedicata al sintomo | Invariante Poka-Yoke e frase obbligatoria del proprietario |
| Richiamo principale nella fase di implementazione | Design scritto su causa ancora presunta | Consultazione all'avvio dell'analisi di un bug |

## Functional Spec

FS1: raccogliere fatti, ambiente, log/trace disponibili e configurazione effettiva;
preservare evidenze prima di interventi che le cancellano. Non leggere tutti i log
come rituale e non ritardare un contenimento urgente; distinguerlo dal fix definitivo.
FS2: registro per bug con ipotesi, evidenze favorevoli/contrarie, probabilità motivata,
costo, verifica/esito e stato. Alta/media/bassa o sconosciuta, non numeri inventati.
Preferire ipotesi più probabili e meno costose; in un trade-off scegliere una prova
che discrimina bene. Stato dell'ipotesi: aperta/confermata/invalidata. Inconclusivo
è l'esito di una verifica: lascia aperta l'ipotesi, conservando le prove precedenti.
Riordino dopo ogni esito.
FS3: usare i perché per risalire alla causa, senza obbligo di cinque livelli.
Ammettere concause; ogni salto non provato è un'ipotesi. Separare causa del guasto
e mancata prevenzione. Non introdurre un secondo metodo di triage.
FS4: prima di correggere, collegare la causa al guasto con prove. L'assenza di log
non smentisce una causa; un grafo dei simboli non dimostra l'esecuzione.
FS5: correggere nel componente responsabile, impedendo lo stato invalido oppure
rilevandolo subito. Enumerare consumatori con gli strumenti disponibili e probe
testuale, dichiarando limiti. Verificare anche input validi, concorrenza e casi
limitrofi pertinenti; nessun refactor generale implicito.
FS6: verifica obbligatoria testuale: «Dopo la correzione il software deve essere
fatto come se fosse stato progettato senza quel difetto».
Motivare responsabilità, invariante, assenza di eccezioni ad hoc e comportamenti
validi preservati. Workaround temporanei dichiarati non chiudono il fix definitivo.
FS7: rinviare a `tdd.md` per RED/GREEN/REFACTOR; preservare regression test old-fail /
new-pass, suite pertinente, comprehension guide e circuito dopo tre tentativi senza
progresso. Per incidenti non riproducibili dichiarare quale prova sostiene quali
affermazioni, senza dispensare automaticamente dai test del meccanismo.

## Interface Contract

L'agente mostra un registro conciso nella mini-analisi L2 o nell'ANALYSIS/Action Plan
già richiesto per L3. Nessun file per ipotesi, nessun nuovo template pubblico.
Il resoconto finale distingue fatti, ipotesi residue, causa confermata, eventuale
contenimento temporaneo e verifiche del fix. Il testo resta utilizzabile offline.

## Capability Ledger

| Capacità | Stato | Proprietario verificato e decisione |
|---|---|---|
| Indagine e circuit breaker | INADEQUATE | `skills/agentic-sdlc-skill/debugging.md`: meccanismo e no speculative fixes esistono; mancano evidenze iniziali, registro e criterio di disegno. Riscrivere quel proprietario |
| RED/GREEN/REFACTOR e test comportamentali | EXISTS | `skills/agentic-sdlc-skill/tdd.md`: old-fail e comportamento osservabile; rinviare, non duplicare |
| Verifica fresh e review indipendente | EXISTS | `skills/agentic-sdlc-skill/SKILL.md` Closure e `review.md`: mantenere |
| Attivazione per bug | INADEQUATE | `skills/agentic-sdlc-skill/SKILL.md`: richiamo solo Phase 4; aggiungere trigger prima dell'analisi |

## Impact

| File | Cambiamento e motivazione |
|---|---|
| `skills/agentic-sdlc-skill/debugging.md` | Riscrittura Method, circuit breaker coerente; preservare comprehension e chronic fragility. Budget massimo 150 righe |
| `skills/agentic-sdlc-skill/SKILL.md` | Un richiamo sotto Rule Zero e rinvio Phase 4; nessuna copia del metodo |
| `CHANGELOG.md` | Voce Unreleased F-061, conservando F-058 |
| `README.md`, `ai_docs/strategic/skill_family_agent_workflows.md` | Sintesi derivate riallineate al metodo, prima del mark dell'area software |
| `ai_docs/audit/audit_plan.md` | Mark solo delle aree skills verificate; nessun aggiornamento blanket di distributions/ai_docs |
| `ai_docs/solutions/ANALYSIS_evidence_driven_debugging.md` | Design e risultati di questa unità |
| `ai_docs/solutions/harness_evidence_debugging/` | Baseline, packet e probe sintetici, candidato, risposte originali e risultati |
| `ai_docs/audit/HANDOFF_evidence_debugging.md` | Resume finché il workstream è aperto |
| `ai_docs/audit/reviews/REVIEW_evidence_debugging.md` | Review indipendenti del design e del diff |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | Append di righe; preservare tutte le righe esistenti |
| `ai_docs/strategic/architecture.md` | Correggere il contratto del componente Doctrine, senza creare un secondo owner |
| `ai_docs/strategic/existing_features.md` | Annotare il metodo corrente se implementato |
| `ai_docs/INDEX.md`, `ai_docs/memory/INDEX.md`, `ai_docs/reference/INDEX.md`, `ai_docs/strategic/features_history.md`, `ai_docs/audit/handoff.md` | Solo rigenerazione con index |

Blast radius: ricerca `rg` in skills/distributions/scripts/ai_docs ha trovato il
richiamo nel solo overlay software, package allowlist e riferimenti storici
F-034/SHADOW. Nessuna firma runtime modificata: simbol graph non applicabile alla
prosa. `debugging.md` non appartiene al shared_manifest; KB/mkt/course e loro
validatori non cambiano. Non aggiornare shadow storici o skill installate.
Popolazioni a riposo: nessun cambio di garanzie read/write, formato persistito,
migrazione/backfill o controllo redact/mask/filter/sanitize/authorize.

## Security and Threat Model

- Log possono contenere segreti/dati personali: leggere il minimo, riportare
  evidenza redatta, non copiare log sensibili nel registro o nelle guide.
- Diagnostica può modificare stato o carico: preferire read-only; esperimenti
  mutanti solo in ambiente controllato e secondo autorizzazioni esistenti.
- Poka-Yoke troppo restrittivo può rompere input validi: test validi/invalidi e
  contratti dei consumatori obbligatori. Non introdurre crash come default universale.
- Ipotesi e cinque perché possono creare falsa certezza: esito inconclusivo,
  concause e limiti di osservabilità restano espliciti.
- Overhead e scope creep: registro proporzionato, nessun documento aggiuntivo,
  nessuna esplorazione globale o refactor speculativo. Il vecchio metodo è preservato
  prima della modifica per confrontare il comportamento sul medesimo packet.

## Action Plan

1. Congelare baseline, quattro casi sintetici e rubrica prima del candidato.
2. Eseguire baseline con lettore indipendente; review del design prima dell'edit.
3. Scrivere candidato e provarlo con un altro lettore fresco; preservare risposte
   e valutare benefici, regressioni e limiti, senza dichiarare risparmio reale.
4. Integrare solo i file previsti dopo PASS del design, verificare test pertinenti,
   ottenere review del diff; riesaminare correzioni con cap tre round.
5. Aggiornare stato e indici, eseguire check, separare problemi preesistenti;
   nessun commit, installazione, version bump, push o publish.

## Test Strategy

Rubrica congelata: causa collegata a prove; ordine dei check osservato; registro
aggiornato; nessun abbandono sull'intermittenza; cause composte e controllo valido;
Poka-Yoke pulito e scope limitato; nessuna pretesa non verificata. Le unità di costo
del simulatore sono illustrative, non secondi/token reali. Due lettori condividono
il medesimo modello e hanno contesti freschi: isolamento sì, diverso modello no.
La prova non è cieca al testo assegnato e non dimostra efficacia generale.
Suite esistente: `test_skill_invariants.py`; nessun test lessicale che pretenda
di dimostrare l'adesione dell'agente. Harness: probe failure path e output valido.
`sdlc_check.py check --root .` verifica repository; un esito non CLEAN impedisce
di dichiarare chiusura globale, anche se estraneo a questa unità.

## Diary / Current State

2026-10-02: analisi preparata, design e packet da revisionare. Il proprietario ha
approvato il disegno discusso e l'esecuzione con agentic-sdlc, direttamente su main.
devPNT bootstrap punta a Eclosion, non a questo repo: modalità Standalone.
Le numerose modifiche pregresse sono preservate; budget dell'ANALYSIS 210 righe.
Design review indipendente PASS (0 BLOCK, 3 WARN), contesto fresco stesso modello.
Chiariti stati, placement e limiti di copertura. Baseline: 13 check, 22 unità di
costo illustrative, cause corrette A-D; criterio evidence-first fallisce in A
(reproduce prima dei log). Nessuna prova di inferiorità diagnostica generale.
Test iniziale invarianti: 63/64 passati, solo index idempotence fallisce dopo il
nuovo ANALYSIS; rigenerazione dovuta. Check globale iniziale già NOT CLEAN, record
in harness_evidence_debugging/check_before.txt; nessuna riparazione fuori scope.
Confronto iniziale: candidato 12 check/17 unità, stesso esito causale A-D. I totali
riassuntivi degli agenti erano errati (21 e 19/13): conservati negli originali e
ricontati meccanicamente con tally.py. In C entrambi hanno speso su prove seriali
non fedeli; aggiunto criterio esplicito di rilevanza/stop e predisposto retest fresco.
Budget di lettura iniziale: debugging 71→114 righe, +3387 byte CRLF; SKILL +249
byte sullo snapshot pre-F061, conservando la modifica F-058 già presente.
Metodo finale 118 righe, +3643 byte UTF-8 con newline LF rispetto alla baseline.
Retest fresco C/E: C due check/due unità, registro esplicito e nessuna prova seriale
fuori causa; E mantiene ipotesi ignote e contenimento separato dal fix. Prova
circoscritta, nessuna nuova lettura completa A-D del finale o efficacia sul campo.
Closure round1 FAIL per aritmetica; round2 PASS sulle correzioni e metodo finale.
Dettagli e limiti: harness_evidence_debugging/RESULTS.md e
ai_docs/audit/reviews/REVIEW_evidence_debugging.md.
Nessuna decisione architetturale runtime: nessun ADR necessario, owner invariato.
Consolidamento 2026-10-02: sintesi README/workflow aggiornate, solo le aree skills
riesaminate e marcate; patch isolata verificata senza applicarla. Sette avvisi sono
mismatch del validator su Vision Alignment, undici richiedono contesto storico.
Stato globale e perimetro del commit: harness_evidence_debugging/CONSOLIDATION.md.

2026-10-02 release closure: independent integration PASS and repository check CLEAN.
Implementation complete; F-062 owns the authorized commit and publication.
