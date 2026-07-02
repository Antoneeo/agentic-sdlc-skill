---
description: Roadmap della milestone di evoluzione — subagent operativi, guide operative/KB agente, eliminazione conflitti di convivenza con devPNT e posizionamento open-core. Sostituisce la bozza in docs/.
status: DRAFT
supersedes: roadmap_evoluzione_agenti_v1.md
target_version: "1.7.0"
---

# Roadmap evoluzione — Agenti operativi, Formazione dell'agente, Convivenza devPNT

Stato: DRAFT — da promuovere ad APPROVED solo con conferma umana (Vision Gate della skill).

## 1. Obiettivo della milestone

Far evolvere `agentic-sdlc` su tre fronti:

1. **Feature A — Esecuzione a subagent operativi**: delega dell'implementazione a agenti freschi per task, con review tra un task e l'altro. Opzionale per L3, mai default.
2. **Feature B — Guide operative da indicazioni dell'utente** + **KB operativa a livello agente**: rendere operative le indicazioni fornite dall'utente (testo o documenti), a scope progetto (`ai_docs/reference/`) e a scope agente (KB globale cross-progetto).
3. **Eliminazione dei conflitti di convivenza con devPNT** e formalizzazione del confine skill/devPNT come confine di prodotto (modello open-core).

Principio guida invariato: assorbire il valore senza snaturare l'identità Documentation-First. Ogni novità si innesta in `ai_docs/` ed eredita frontmatter canonico, manifest e lifecycle.

## 2. Decisioni architetturali prese

**D1 — La skill è la spina dorsale; devPNT è l'amplificatore.** La skill possiede il processo (triage, fasi, Vision Gate, lifecycle, KB). devPNT fornisce servizi (DB versionato, proposte con approvazione GUI, reviewer indipendenti, semantic analysis, KL). La doctrine devPNT non duplica il processo: vi rimanda.

**D2 — Pattern a provider.** Ogni fase della skill definisce uno slot; Standalone lo riempie il filesystem, Hybrid lo riempie devPNT. devPNT è additivo per costruzione: lo slot ha sempre il default filesystem (Poka-Yoke — la skill non può dipendere da devPNT).

**D3 — Modello commerciale open-core.** Skill gratuita e completa (canale di acquisizione); devPNT a licenza vende la macchina, mai la metodologia. Upgrade a zero attrito (stessi slot, backend più ricco); downgrade garantito (shadow → documenti veri, nessun dato in ostaggio). La linea individuale/team è la fence di prezzo: tutto ciò che richiede stato condiviso, approvazione tracciata o identità multiple sta nel tier a pagamento.

**D4 — Griglia origine × scope della conoscenza.** Origine codice + scope progetto = territorio devPNT (KL, functional docs, summaries, PKB). Origine utente = territorio skill: scope progetto → guide in `ai_docs/reference/`; scope agente → KB globale. Il ponte tra i due mondi è sempre un puntatore, mai una copia (DRY).

**D5 — Fedeltà alla fonte come vincolo strutturale (Feature B).** La guida rende operativo solo ciò che l'utente ha fornito. Marcatori obbligatori per sezione (`[fonte: …]` / `[non coperto dalla fonte]`) e frontmatter di provenienza (`source`, `source_version`, `distilled_from`) verificati dal validatore, non affidati alla prosa.

**D6 — Guide-documento, non skill installabili.** Confermata: le guide restano versionate, manifestate e validate in `ai_docs/reference/`. Unica classe di artefatto che resta filesystem-first anche in Hybrid (devono essere leggibili da subagent context-free via path, senza tool MCP).

**D7 — devPNT dipende obbligatoriamente da agentic-sdlc.** Lo stato "devPNT attivo senza metodologia" diventa illegale per costruzione: gli stati possibili sono solo skill-only (free) o skill+devPNT (paid). Conseguenze:
- **Install-time**: l'installer devPNT installa/vendorizza la skill nei target rilevati (`~/.claude|.gemini|.codex/skills/`). Mai sovrascrivere una skill già installata più recente: installa se assente, aggiorna solo se sotto la minima compatibile. Contratto di versione: la skill dichiara `methodology_version`; devPNT dichiara il range compatibile.
- **Invocation-time**: il bootstrap devPNT verifica sul filesystem presenza e versione della skill e dichiara nel payload `methodology: agentic-sdlc vX.Y RILEVATA | MANCANTE | INCOMPATIBILE`, con istruzione di caricare la skill e seguirne il triage. Enforcement selettivo: tool di query sempre disponibili; tool di governance/scrittura con warning bloccante se la metodologia manca.
- La doctrine devPNT può quindi **assumere** la skill presente e ridursi a puro rimando (rafforza 1.2).

## 3. Conflitti di convivenza rilevati (da eliminare)

| ID | Conflitto | Gravità |
|---|---|---|
| C1 | Struttura `ai_docs/` divergente tra skill (vision/, reference/, architecture/, functional/, strategic/) e doctrine devPNT (strategic/, functional/, audit/, solutions/) | Attivo |
| C2 | Tre verità per la Vision in Hybrid: `vision/project_vision.md`, M-VISION, KL vision — nessun gate rileva drift tra loro | Attivo |
| C3 | Shadow: doctrine devPNT le chiama `ANALYSIS_*.md`, la skill le definisce `SHADOW_[doc_key]_vX.Y.md` e tratta `ANALYSIS_*` come autoritativo con frontmatter obbligatorio → `validate` esplode sugli shadow devPNT | Attivo, rompe il check |
| C4 | `gate` PreToolUse sblocca solo con ANALYSIS locale IN_PROGRESS: in Hybrid (artefatti nel DB) blocca scritture legittime | Attivo, rompe Hybrid |
| C5 | Doppio stato feature senza sync: frontmatter ANALYSIS vs status nodo Action Plan | Attivo |
| C6 | Triage skill (L2 ≤ 3 file senza documenti) contraddice trigger policy devPNT (E-ISP/E-TDD da >1 file) | Attivo |
| C7 | ADR: DB devPNT vs filesystem (manifest skill) — due archivi, ricerche cieche a vicenda | Attivo |
| C8 | Doppio motore di freshness: `stale`/`mark` vs KL coverage; `stale` è mode-blind | Attivo |
| C9 | Feature A duplicherebbe i gate di review devPNT (§4.5/§4.6) | Di progetto |
| C10 | Piano eseguibile quasi isomorfo al Module Change Plan dell'E-TDD → doppia verità sul design in Hybrid | Di progetto |
| C11 | Guide invisibili agli agenti devPNT: il bootstrap (KL + functional) non menziona `reference/` | Di progetto |
| C12 | PKB devPNT (infrastruttura presente, vuota) in rotta di collisione con guide/KB se popolato con conoscenza operativa | Latente |

## 4. Piano per fasi

### Fase 0 — Bonifica repo skill (debito, prerequisito)

| # | Modifica | Dove |
|---|---|---|
| 0.1 | Eliminare/archiviare la copia divergente della skill | `agentic-sdlc-v2/` |
| 0.2 | Template: fonte unica `templates.md`; eliminare (o generare) `references/*_template.md`; `init.js` legge i template, niente stringhe inline | `references/`, `scripts/init.js`, `package.json` |
| 0.3 | Protocollo generato ridotto a protocollo-puntatore (triage in sintesi + rimando a skill/ai_docs), per non driftare da SKILL.md | `scripts/init.js` |
| 0.4 | init.js: non creare `features_history.md` (generato); frontmatter nei doc creati; creare `ai_docs/reference/` e `ai_docs/README.md`; detection home-dir come postinstall; dedup delle funzioni `install*()` | `scripts/init.js`, `scripts/postinstall.js` |
| 0.5 | Dogfooding: roadmap in `ai_docs/vision/`; `docs/functional/` → `ai_docs/functional/`; generare `INDEX.md` + `README.md` del repo | repo |
| 0.6 | Validatore: filtro shadow per filename; `mark` fail-fast senza `ai_docs/`; `validate --strict` per CI; heading/chiavi frontmatter bilingue EN/IT o chiavi canoniche dichiarate | `skills/agentic-sdlc-skill/scripts/sdlc_check.py` |

### Fase 1 — Seam skill↔devPNT (elimina C1–C8)

| # | Modifica | Dove |
|---|---|---|
| 1.1 | **Matrice di convivenza**: per artefatto → master Standalone / master Hybrid / regola mirror. Unico posto autoritativo | `SKILL.md` |
| 1.2 | Doctrine devPNT: rimuovere il processo duplicato (trigger policy rimanda al triage skill; layout `ai_docs/` allineato con `vision/` e `reference/`; shadow = `SHADOW_*`). Grazie a D7 la doctrine assume la skill presente: resta solo governance artefatti + rimando | repo devPNT (prompt `devpnt-instructions`) |
| 1.3 | Tabella di equivalenza triage: L1↔trivial exempt, L2↔localized edit, L3↔governato S2A2 | `SKILL.md` + doctrine devPNT |
| 1.4 | `gate` hybrid-aware: secondo segnale di autorizzazione (shadow E-TDD presente, o `--hybrid`→warn) | `sdlc_check.py` |
| 1.5 | `stale`/`check` mode-aware: in Hybrid saltare l'audit_plan morto | `sdlc_check.py` |
| 1.6 | Mapping stati dichiarato (ANALYSIS ↔ nodo plan) e verificato in chiusura | `SKILL.md` + `sdlc_check.py` |
| 1.7 | ADR: Hybrid→DB con shadow filesystem generata; Standalone→`architecture/` | matrice 1.1 + doctrine |
| 1.8 | Gerarchia vision: M-VISION master per milestone; `project_vision.md` = scope prodotto; KL vision = mirror rigenerato | matrice 1.1 |

### Fase 2 — Feature B: guide operative + KB agente

| # | Modifica | Dove |
|---|---|---|
| 2.1 | Risolvere la collisione di naming: `ai_docs/reference/` solo guide; i support file della skill fuori da nomi "reference" | dir skill |
| 2.2 | Pipeline transform: scomposizione in topic → conferma utente → estrazione fonte-ancorata → sezioni scelte tra quelle che la fonte sostiene; marcatori `[fonte:…]`/`[non coperto dalla fonte]`; frontmatter provenienza | `SKILL.md` + `templates.md` |
| 2.3 | Validatore: provenienza obbligatoria in `reference/`; warn su sezioni senza marcatore; `stale` esteso a `source_version` vs versione realmente importata | `sdlc_check.py` |
| 2.4 | KB agente: radice globale (es. `~/.agentic-sdlc/`), stessa struttura, stesso motore via `--root`; precedenza progetto>agente con `overrides:` e warning su collisioni non dichiarate | `sdlc_check.py` + `SKILL.md` |
| 2.5 | Ponte Hybrid: sezione bootstrap devPNT che punta all'indice guide (vedi feature devPNT F3) | repo devPNT |

### Fase 3 — Backlog Tier-1 (basso attrito, parallelizzabile)

TDD esplicito (red/green/refactor), systematic debugging, elicitation collaborativa della spec (L3), disciplina di code review → support file della skill + richiami nelle fasi 4/5 di `SKILL.md`. Nessun contatto con devPNT.

### Fase 4 — Feature A: subagent + piano eseguibile (pacchetto)

| # | Modifica | Dove |
|---|---|---|
| 4.1 | Piano eseguibile in `solutions/` con schema (path esatti, consumes/produces, comando di verifica); subcommand `sdlc_check.py plan`: **no piano valido, no dispatch** + emissione meccanica del task-brief per ogni task (solo il task, le interfacce dai task precedenti e i puntatori alle guide — mai storia incollata); in Hybrid `derived-from: e_tdd vX.Y`, mai autorato indipendente | `sdlc_check.py` + `templates.md` |
| 4.2 | Loop di dispatch: subagent fresco per task; `check` tra un task e l'altro; review slot per-task **one-shot, mai loop iterativi** (self-review inline dell'implementer + un reviewer + review ampia finale — lezione superpowers 5.0.x, §5-bis); Standalone: reviewer proprio; Hybrid: reviewer devPNT. **Progress ledger per-task durevole** (recovery da compaction, no ri-dispatch di task completati). **Model-per-dispatch**: ogni dispatch dichiara il tier; l'implementer parte sul tier economico (il design granulare rende l'implementazione traduzione, non invenzione), escalation al tier superiore dopo doppio FAIL di review sullo stesso task — decisione 2026-07-02, applicata già alla milestone Feature B | nuovo support file skill |
| 4.3 | Degradazione meccanica: presenza del tool Task/Agent rilevata, non giudicata dal modello; fallback dichiarato su esecuzione same-session | support file |
| 4.4 | Saldatura A×B: le guide rilevanti sono risolte e iniettate per valore nel prompt di ogni task | support file |

### Fase 5 — Consolidamento

SessionStart hook (carica `README.md`/`INDEX.md` di progetto + indice KB agente, annuncia il triage), eval harness della skill, igiene worktree/chiusura branch.

## 5. Feature richieste a devPNT

| ID | Feature | Serve a | Tier |
|---|---|---|---|
| F1 | `devpnt_export_shadows`: rigenera tutte le shadow filesystem dalle versioni accettate nel DB | Chiusura Hybrid automatica + garanzia di downgrade (argomento commerciale) | Base |
| F2 | Import onboarding `ai_docs/` → devPNT (ANALYSIS→seed E-ISP, vision→M-VISION draft, audit_plan→scope KL) | Conversione free→paid | Commerciale |
| F3 | Sezione bootstrap "OPERATIVE GUIDES" che inietta l'elenco (con status) da `ai_docs/reference/INDEX.md` | Chiude C11 con puntatori, zero copia | Base |
| F4 | Governance guide per team: guide come doc_type governato, condivisione multi-progetto (vocazione del PKB) | Fence di prezzo individuale/team | Paid |
| F5 | `devpnt_state_diff`: mismatch tra stato nodi plan e frontmatter shadow/ANALYSIS | Rende meccanico C5 | Base |
| F6 | Review-prompt packaging via MCP: tool che RESTITUISCE un prompt di review autosufficiente (artefatto + checklist + estratti sorgente rilevanti), **senza eseguire LLM** — l'esecuzione avviene sempre sull'orchestratore del client (subagent nativo o run one-shot `gemini -p`/`codex exec`). Vincolo: gli agenti interni devPNT sono legacy (costosi, orchestratore meno efficace di Claude Code/Codex); l'AI interna resta solo per task piccoli (summary, descrizioni) | Slot review di Feature A da qualunque client, a costo client | Paid |
| F7 | `devpnt_capabilities`: dichiara modalità/entitlement attivi (licenza, GUI, reviewer) e — bidirezionale, per D7 — presenza/versione della skill rilevata | Mode detection meccanico per la skill (Poka-Yoke) | Base |
| F8 | Methodology-check nel bootstrap + installer che installa/vendorizza la skill (regola no-downgrade, range `methodology_version` compatibile); warning bloccante sui tool di governance se metodologia mancante | Implementa D7 | Base |

## 5-bis. Verifica indipendente vs superpowers (2026-07-02)

Ricognizione dello stato attuale di superpowers (v5.0.1–5.0.7, mar–mag 2026) a conferma della direzione:
- **Differenziatore intatto**: superpowers continua a non avere guide operative da indicazioni utente; la sua risposta agli standard aziendali è "scrivi una skill" (writing-skills) — alternativa già valutata e scartata in D6. Feature B resta l'aggiunta originale.
- **Backlog confermato**: TDD, systematic debugging, elicitation socratica, code review, worktree tutti ancora core in superpowers; esclusioni (verification-before-completion, writing-skills) ancora giuste.
- **Lezioni 5.0.x recepite in Fase 4**: (a) review per-task one-shot, mai loop iterativi (retromarcia documentata di superpowers sul costo, ~60% del tempo); (b) progress ledger durevole per il recovery da compaction; (c) task-brief meccanici ("42k caratteri di storia incollata" è l'anti-pattern che ha motivato il loro `scripts/task-brief`) — conferma sperimentale della tesi §2.
- **F6 validata**: il loro `scripts/review-package` (impacchettamento meccanico del contesto di review, zero LLM) è il precedente diretto del nostro review-prompt packaging.
- **Client-agnosticismo**: superpowers supporta ora Claude Code, Antigravity, Codex, Cursor, Copilot CLI e altri via SessionStart injection — conferma la generalizzazione dei review gate e alza la priorità del Backlog #7 (SessionStart hook).

## 6. Sequenza e dipendenze

1. **Fase 0 → Fase 1** in quest'ordine: la matrice 1.1 è prerequisito concettuale di tutto il resto.
2. **Fase 2 prima della Fase 4**: A beneficia direttamente di B (le guide sono l'infrastruttura che rende affidabili i subagent context-free).
3. **Fase 3** parallelizzabile ovunque.
4. Feature devPNT F3/F5/F7 servono già in Fase 1–2; F1/F2/F4/F6 seguono il tier commerciale.

## 7. Decisioni aperte (ereditate + nuove)

- A — opt-in esplicito per gli L3 (proposta confermata) o default oltre una soglia di dimensione?
- A — granularità minima del piano eseguibile perché un subagent context-free abbia successo.
- B — mix di garanzie di fedeltà: revisione umana obbligatoria vs auto-check con citazioni, graduato sul rischio di invenzione.
- B — rappresentazione delle lacune: sezione dedicata "non coperto dalla fonte" vs marcatore inline (proposta: entrambi, marcatore obbligatorio, sezione riassuntiva generata).
- KB agente — percorso radice definitivo e comportamento su macchine senza KB.
- Naming definitivo dei support file skill dopo la rimozione dell'ambiguità "reference".
- D7 — semver del contratto `methodology_version`: cosa costituisce breaking change della metodologia (rinomina artefatti/stati sì; prosa no) e come devPNT dichiara il range compatibile.
- **Vincolo architetturale (deciso)**: gli agenti interni devPNT sono LEGACY — mai usarli per review o task sostanziosi (costo + orchestratore meno efficace dei client). L'AI interna devPNT serve solo task piccoli (summary, descrizioni, doc generation). Ogni lavoro LLM sostanzioso gira sull'orchestratore del client.
