---
name: agentic-sdlc-v2
description: Protocollo SDLC "Documentation-First" con triage proporzionale al rischio, Vision ad autorità graduata (DRAFT/APPROVED), stato documentale validato meccanicamente e integrazione opzionale devPNT. Utilizzare per sviluppare feature, correggere bug, eseguire audit di progetti esistenti e mantenere la documentazione tecnica allineata al codice prima, durante e dopo l'implementazione.
author: Antonio Pinto (https://github.com/Antoneeo) — revisione v2 con triage, autorità graduata e validazione meccanica
copyright: © 2026 Antonio Pinto
---

# Agentic SDLC v2 (Hybrid Edition)

Workflow Documentation-First **proporzionale al rischio**: la quantità di processo dipende dal Triage (Regola Zero), non è fissa. Con il server MCP **devPNT** disponibile opera in modalità Hybrid; altrimenti in Standalone su `ai_docs/`. Basata sulla skill `agentic-sdlc` di Antonio Pinto.

File di supporto nella directory della skill — leggili solo quando servono:
- `templates.md` — template di tutti i documenti (vision, analysis, spike, audit, handoff)
- `scripts/sdlc_check.py` — validatore meccanico: `check` (= validate + stale) | `validate` | `index` | `stale` | `mark` | `gate`
- `ENFORCEMENT.md` — setup opzionale di CI e hook per garanzie non affidate al prompt

## Valori Tecnici

Privilegia qualità e comprensione rispetto alla velocità apparente.

- **Comprendi prima di agire:** non modificare codice senza aver capito il motivo; nei bug cerca la root cause, non workaround.
- **Mantieni coerenza architetturale:** rispetta layer, responsabilità, naming, pattern e convenzioni esistenti.
- **Applica DRY e semplicità:** non duplicare logica o conoscenza; crea astrazioni solo se riducono complessità reale.
- **Preserva la qualità:** ogni modifica deve mantenere o migliorare stabilità, testabilità e manutenibilità.
- **Verifica tecnicamente:** chiudi ogni task implementativo con test/lint/smoke test, o spiega perché non eseguiti.
- **Mantieni memoria utile:** documenta decisioni e stato operativo rilevanti, non rumore. La conformità al template non è l'obiettivo: una sezione senza contenuto informativo reale va riempita con il motivo per cui non si applica, non con testo riempitivo.
- **Proteggi la Vision:** ogni decisione deve restare allineata a obiettivo finale, benefici attesi, utenti target e non-obiettivi dichiarati (vedi autorità graduata, Fase 2).

Se una patch sembra facile ma non capisci perché il codice attuale è fatto così, indaga prima di modificarlo.

## Regola Zero: Triage (sempre, prima di tutto)

Classifica la richiesta e **dichiara il livello scelto all'utente nella prima risposta**:

| Livello | Criteri | Processo richiesto |
|---|---|---|
| **L1 — Triviale** | ≤ ~10 righe in 1–2 file; nessun cambio di API o dipendenze; e il comportamento o non cambia in modo osservabile, oppure viene solo **ripristinato quello già atteso** (refusi, fix che riallineano il codice a test o documentazione esistenti) | Implementa. Esegui i test esistenti pertinenti. Nessun documento. |
| **L2 — Piccolo** | Root cause chiara; ≤ 3 file; nessuna nuova dipendenza né cambio di API pubblica | Mini-analisi nel messaggio (obiettivo, impatto, sicurezza, test). Test obbligatori. Nessun nuovo documento; se cambia comportamento visibile, aggiorna l'ANALYSIS esistente o annotalo nell'handoff. |
| **L3 — Significativo** | Almeno uno: > 3 file; API o contratti; nuova dipendenza; comportamento visibile all'utente; area security-sensitive; struttura architetturale | Workflow completo (Fasi 1–6). |
| **Spike** | Esplorazione time-boxed per ridurre incertezza | Niente Vision Gate. Codice in branch/directory dedicata, non mergiabile in main. Esito in `ai_docs/solutions/SPIKE_[tema].md` (≤ 1 pagina). Per portarlo in produzione: riclassifica come L2/L3. |

Regole trasversali:
- **Aree security-sensitive** (parsing di input esterni, autenticazione/autorizzazione, crittografia, rete, dati personali, accesso al filesystem): mai L1; la valutazione di sicurezza è obbligatoria.
- **Escalation:** se durante un L1/L2 emerge un impatto maggiore del previsto, fermati, riclassifica e dichiara il cambio all'utente.
- Nel dubbio tra due livelli, scegli il più alto.
- L'audit completo (Fase 1) **non** si avvia per task L1/L2: si esegue solo su richiesta esplicita o prima del primo task L3 in un progetto privo di `ai_docs/`.

## Workflow (Fasi 1–6 per intero solo a L3)

### 0. Discovery (ambiente)
Verifica la disponibilità dei tool `devpnt_*`.
- **HYBRID (devPNT presente):** i piani (Master/Action) e gli artefatti governati (`D-UC`, `P-TM`, `E-ISP`, `E-TDD`) vivono **solo** nel database devPNT — fonte di verità unica. Le copie Markdown sono **shadow generate alla chiusura** dalla versione accettata nel DB, salvate come `ai_docs/solutions/SHADOW_[doc_key]_vX.Y.md` con intestazione `<!-- SHADOW generata da devPNT (doc_key vX.Y) — non modificare a mano -->`; in caso di divergenza vince il DB e la shadow si rigenera. Per la mappatura del progetto usa `devpnt_kl_init_scope`, **non** `audit_plan.md`. Se è attivo anche il protocollo devPNT a livello di CLAUDE.md, le sue regole prevalgono per gli artefatti governati; questa skill governa il triage e il livello filesystem.
- **STANDALONE (devPNT assente):** tutto in `ai_docs/`; mappatura via `ai_docs/audit/audit_plan.md`. Per progetti complessi suggerisci devPNT, senza bloccare il lavoro.
- In entrambe le modalità la Vision umana-leggibile vive **solo** in `ai_docs/vision/`.

### 1. Audit e Allineamento
- Leggi `ai_docs/audit/handoff.md` se esiste. Verifica l'intestazione (Data, Branch): se non corrisponde al contesto corrente, trattalo come storico da verificare, non come stato.
- **Ripresa dopo interruzione**: se ci sono segni di lavoro pregresso (ANALYSIS o `audit_plan.md` esistenti) ma l'handoff è assente o incoerente con lo stato dei file, esegui subito `python scripts/sdlc_check.py check` — indice disallineato, frontmatter invalidi e stati incompleti emergono meccanicamente prima di riprendere il lavoro. Su un progetto senza lavoro pregresso il check non serve.
- Se `ai_docs/` manca o è incompleta (e siamo a L3 o l'audit è richiesto): analisi a lotti — mappatura in `audit_plan.md` (template in `templates.md`), stati `PENDING`/`ANALYZED`/`SKIPPED` con motivo, conferma all'utente tra i lotti sui progetti grandi.
- **Non aggiornare gli stati di analisi a mano durante lo sviluppo.** La freschezza si calcola: `python scripts/sdlc_check.py stale` elenca le aree cambiate dopo l'ultima analisi registrata; `... mark <percorso>` registra una ri-analisi (hash git o timestamp). In Hybrid la mappatura è delegata a devPNT/KL e `stale` non si applica.
- Tutti i documenti prodotti dall'audit nascono con `Stato: DRAFT`.

### 2. Vision Gate (autorità graduata)
- Leggi una volta per sessione `project_vision.md`, `roadmap.md`, `principles.md` (annota nell'handoff che è stato fatto). Documenti concisi: ≤ ~80 righe ciascuno.
- Ogni documento di vision dichiara nelle prime righe `Stato: DRAFT` oppure `Stato: APPROVED (da <chi>, <data>)`.
- **DRAFT** = ipotesi ricostruita dall'agente, **non è autorità di gating**: se una richiesta vi confligge, segnala il possibile conflitto ma la richiesta dell'utente prevale; proponi di aggiornare la draft.
- **APPROVED** = autorità: se la richiesta confligge, non implementare in silenzio; esplicita il conflitto e proponi la scelta (aggiornare la Vision oppure modificare/rifiutare la richiesta).
- Alla prima occasione utile chiedi all'utente di validare le DRAFT: solo con la sua conferma esplicita aggiorna lo stato ad APPROVED, registrando chi e quando. **Non promuovere mai una vision ad APPROVED di tua iniziativa.**
- La vision della feature L3 vive nella sezione `## Vision della Feature` della sua ANALYSIS (beneficio, non-obiettivi/fuori scope, segnali di successo): un solo documento per feature. Crea un file separato `ai_docs/vision/features/VISION_[feature].md` solo se la feature attraversa più ANALYSIS o più milestone.

### 3. Analisi della Richiesta (L3)
- Crea `ai_docs/solutions/ANALYSIS_[feature].md` dal template. Il **frontmatter** del file (id, stato, livello, date) è la fonte di verità dello stato della feature.
- Sezioni obbligatorie: `## Obiettivo`, `## Vision della Feature` (beneficio, allineamento alla vision di progetto e suo stato DRAFT/APPROVED, non-obiettivi/fuori scope, segnali di successo), `## Impatto`, `## Sicurezza e Threat Model` (sempre, anche in Standalone: superfici toccate, minacce principali, mitigazioni; "nessun impatto" va motivato, non omesso), `## Piano d'Azione` con checkbox, `## Strategia di Test`, `## Diario / Stato Corrente`.
- **Hybrid:** crea inoltre il nodo nel Master Plan, l'Action Plan e gli artefatti (`D-UC`, `P-TM`, `E-ISP`, `E-TDD`) nel DB devPNT; le shadow Markdown si generano in chiusura, non ora.
- `ai_docs/strategic/features_history.md` è un **indice generato**: non editarlo a mano. Si rigenera **solo in chiusura** (Fase 5) con `python scripts/sdlc_check.py index`: essendo derivato dai frontmatter, le rigenerazioni intermedie sono superflue e un indice disallineato viene comunque rilevato da `check`. (Elimina anche i conflitti di merge: dopo un merge si rigenera.)

### 4. Sviluppo e Test
1. Frontmatter dell'ANALYSIS → `stato: IN_PROGRESS` (niente rigenerazione dell'indice: si fa una volta sola in chiusura).
2. Implementa in modo chirurgico seguendo il Piano d'Azione, spuntando le checkbox; annota le deviazioni dal piano nel Diario.
3. **Obbligatorio:** test automatici per il codice toccato (pattern AAA per gli unit test). Se l'ambiente non consente l'esecuzione (es. firmware/hardware-in-the-loop), definisci nella Strategia di Test una verifica alternativa esplicita e il motivo.
4. **Circuit breaker:** dopo **3 esecuzioni consecutive senza progresso** (l'insieme dei test falliti non si riduce e la causa non cambia) fermati e chiedi istruzioni all'utente. Il contatore si azzera quando i fallimenti diminuiscono o la causa cambia.
5. A ogni milestone (fase completata, blocco incontrato, decisione presa) aggiorna il Diario dell'ANALYSIS: l'handoff è event-driven, non solo a fine sessione.

### 5. Chiusura
- Esegui la suite di test pertinente (o la verifica alternativa dichiarata).
- Aggiorna **solo** i documenti effettivamente impattati (`architecture.md`, `existing_features.md`, vision se sono cambiati obiettivi/non-obiettivi) — sai cosa hai toccato dal Piano d'Azione e dal Diario; verifica la coerenza del risultato con la vision APPROVED e i non-obiettivi dichiarati. **Standalone:** registra le aree riviste con un solo `python scripts/sdlc_check.py mark <percorso1> <percorso2> ...`.
- **Hybrid:** proponi un ADR se ci sono state decisioni architetturali; aggiorna il Knowledge Layer; rigenera le shadow dalla versione accettata nel DB.
- Frontmatter dell'ANALYSIS → `stato: COMPLETED` + `data_fine`, poi `python scripts/sdlc_check.py index` e infine **un solo** `python scripts/sdlc_check.py check` come gate finale: se non è pulito, risolvi e ripeti `check`. Niente validate/stale intermedi durante il lavoro: il gate meccanico è unico, alla fine.
- I documenti aggiornati viaggiano **nello stesso commit/PR** del codice che descrivono.

### 6. Handoff (event-driven)
- Lo stato operativo dettagliato di ogni feature vive nella sua sezione `## Diario / Stato Corrente` (aggiornata in Fase 4, punto 5): l'handoff non dipende da un unico file condiviso.
- `ai_docs/audit/handoff.md` è solo un puntatore (≤ 20 righe): intestazione `Data / Branch / Agente`, elenco delle ANALYSIS attive, prossimo passo. Aggiornalo a ogni milestone e a fine sessione, non solo su richiesta.

## Enforcement meccanico
Le regole a livello di prompt degradano con contesti lunghi e compaction. Per garanzie reali leggi `ENFORCEMENT.md`: check `sdlc_check.py validate` in CI (l'indice disallineato o gli stati invalidi bloccano la pipeline) e hook PreToolUse `gate` sulle sole directory security-critical.
