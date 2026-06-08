---
name: agentic-sdlc
description: Protocollo SDLC "Documentation-First" con integrazione opzionale devPNT. Utilizzare per gestire lo sviluppo di nuove feature, eseguire l'audit di progetti esistenti e mantenere rigorosamente aggiornata la documentazione tecnica prima, durante e dopo l'implementazione del codice.
author: Antonio Pinto (https://github.com/Antoneeo)
copyright: © 2026 Antonio Pinto
---

# Agentic SDLC (Hybrid Edition)

Questa skill implementa un workflow rigoroso per lo sviluppo software, assicurando che la documentazione preceda sempre l'implementazione (Documentation-First). Se rileva la presenza del server MCP **devPNT**, potenzia il workflow utilizzando il database per la governance e i piani gerarchici.

Realizzata da **Antonio Pinto** (https://github.com/Antoneeo).

## Valori Tecnici

Privilegia qualità e comprensione rispetto alla velocità apparente.

- **Comprendi prima di agire:** non modificare codice senza aver capito il motivo; nei bug cerca la root cause, non workaround.
- **Mantieni coerenza architetturale:** rispetta layer, responsabilità, naming, pattern e convenzioni esistenti.
- **Applica DRY e semplicità:** non duplicare logica o conoscenza; crea astrazioni solo se riducono complessità reale.
- **Preserva la qualità:** ogni modifica deve mantenere o migliorare stabilità, testabilità e manutenibilità.
- **Verifica tecnicamente:** chiudi ogni task implementativo con test/lint/smoke test, o spiega perché non eseguiti.
- **Mantieni memoria utile:** documenta decisioni e stato operativo rilevanti, non rumore.
- **Proteggi la Vision:** ogni decisione deve restare allineata a obiettivo finale, benefici attesi, utenti target e non-obiettivi dichiarati.

Se una patch sembra facile ma non capisci perché il codice attuale è fatto così, indaga prima di modificarlo.

## Workflow Operativo

### 0. Fase di Discovery (Ambiente)
Prima di rispondere a qualsiasi richiesta operativa, verifica la disponibilità dei tool `devpnt_*`.
- **MODALITÀ HYBRID (devPNT presente):** Delega la gestione dei piani (Master/Action) e del versionamento degli artefatti (`D-UC`, `P-TM`, `E-ISP`, `E-TDD`) a devPNT. Usa la cartella `ai_docs/` per salvare le versioni Markdown ("shadow-copy") dei documenti per garantire visibilità e compatibilità. Mantieni sempre la Vision leggibile in `ai_docs/vision/`.
- **MODALITÀ STANDALONE (devPNT assente):** Gestisci tutto via filesystem in `ai_docs/`. In caso di progetti complessi, suggerisci l'adozione di devPNT per una governance avanzata.

### 1. Fase di Audit e Allineamento
Verifica lo stato della documentazione del progetto.
- Controlla la presenza di `ai_docs/audit/handoff.md`. Se esiste, leggilo per riprendere il contesto dell'ultima sessione.
- Controlla l'esistenza della cartella `ai_docs/`.
- Se `ai_docs/` non esiste o mancano i documenti fondamentali, non procedere con un'analisi dell'intero progetto in un solo colpo. Esegui invece un'analisi strutturata in step:
    1. **Mappatura:** Crea un file di tracciamento (es. `ai_docs/audit/audit_plan.md`) elencando le macro-directory e i file chiave da analizzare. Se in modalità **Hybrid**, puoi usare `devpnt_kl_init_scope` per generare la mappatura iniziale.
    2. **Stato dell'Analisi:** Accanto a ogni elemento nel piano, indica lo stato: `[PENDING]`, `[ANALYZED]`, oppure `[SKIPPED]` (con relativa motivazione, es. "file generato", "asset statico").
    3. **Esecuzione a Lotti (Batching):** Analizza la codebase seguendo l'ordine del file di piano, aggiornando lo stato man mano. Se il progetto è grande, esegui l'analisi a blocchi per evitare di saturare la memoria contestuale, chiedendo conferma all'utente tra un blocco e l'altro se necessario.
    4. **Creazione Documenti:** Sulla base dei risultati dell'audit, compila i documenti fondamentali rispettando i seguenti formati:
       - `ai_docs/vision/project_vision.md`: Deve descrivere North Star, utenti target, problema centrale, obiettivi, non-obiettivi e segnali di successo.
       - `ai_docs/vision/roadmap.md`: Deve descrivere milestone, benefici attesi, priorità e indicatori di avanzamento.
       - `ai_docs/vision/principles.md`: Deve elencare i principi decisionali stabili che guidano trade-off e scope.
       - `ai_docs/vision/features/`: Deve contenere una mini-vision per ogni feature significativa.
       - `ai_docs/strategic/architecture.md`: Deve seguire questa struttura:
         - `# Architettura del Progetto`
         - `## Stack Tecnologico`
         - `## Struttura delle Directory`
         - `## Pattern Architetturali`
       - `ai_docs/strategic/existing_features.md`: Deve seguire questa struttura:
         - `# Funzionalità Esistenti`
         - Elenco puntato nel formato: `- [ID] **Nome Feature**: Descrizione`
       - `ai_docs/strategic/features_history.md`: Deve essere una tabella Markdown con le seguenti colonne: `| ID | Nome Feature | Stato | Data Inizio | Data Fine | Doc. Analisi | Note |`. Gli stati ammessi sono `[PLANNED]`, `[IN_PROGRESS]`, `[COMPLETED]`.

### 2. Vision Gate
Prima di analizzare tecnicamente una nuova feature, modifica comportamentale o refactor significativo, ripristina il contesto di Vision:
- Leggi `ai_docs/vision/project_vision.md`, `ai_docs/vision/roadmap.md` e `ai_docs/vision/principles.md`.
- Se uno di questi documenti manca, è vuoto o non chiarisce l'obiettivo finale, crealo o aggiornalo prima di procedere.
- Per ogni feature significativa, crea o aggiorna `ai_docs/vision/features/VISION_[nome_feature].md` con:
  - `## Problema`
  - `## Beneficio Atteso`
  - `## Utenti o Stakeholder`
  - `## Segnali di Successo`
  - `## Non-Obiettivi / Fuori Scope`
  - `## Vincoli e Principi Collegati`
- Se la richiesta dell'utente confligge con Vision, non implementare in silenzio: esplicita il conflitto e proponi una scelta (aggiornare la Vision oppure modificare/rifiutare la richiesta).

### 3. Fase di Analisi della Richiesta
Per ogni nuova feature richiesta dall'utente:
- **Hybrid:** Crea un nodo nel Master Plan e definisci l'Action Plan tramite devPNT. Salva i documenti di design (`D-UC`, `P-TM`, `E-ISP`, `E-TDD`) nel Database e crea contemporaneamente il file Markdown in `ai_docs/solutions/ANALYSIS_[nome_feature].md`.
- **Standalone:** Crea `ai_docs/solutions/ANALYSIS_[nome_feature].md`. Il documento deve obbligatoriamente seguire questa struttura:
  - `# Analisi della Feature: [Nome Feature]`
  - `## Obiettivo` (Cosa si vuole ottenere e quali problemi risolve)
  - `## Allineamento alla Vision` (Quale Vision documenta il beneficio, quali non-obiettivi rispettare)
  - `## Impatto` (Modifiche ai file esistenti, performance, nuove dipendenze)
  - `## Piano d'Azione` (Elenco di task con checkbox `[ ]`)
  - `## Strategia di Test` (Test unitari AAA, test d'integrazione, esempi)
- In entrambe le modalità, aggiungi la nuova feature in `ai_docs/strategic/features_history.md` con stato `[PLANNED]`.

### 4. Fase di Sviluppo e Test
Solo dopo aver completato le Fasi 2 e 3:
1. Aggiorna lo stato della feature in `features_history.md` a `[IN_PROGRESS]`.
2. Implementa il codice in modo chirurgico seguendo il piano definito. **Importante:** Per ogni file o macro-directory modificata o creata durante lo sviluppo, aggiorna `ai_docs/audit/audit_plan.md` reimpostando (o aggiungendo) il suo stato a `[PENDING]`.
3. **Obbligatorio:** Scrivi i test automatici seguendo il pattern **AAA (Arrange, Act, Assert)**.
4. Esegui i test. Se falliscono, correggi il codice e riesegui. **Se i test falliscono per più di 3 volte consecutive, fermati e chiedi istruzioni all'utente.**

### 5. Fase di Chiusura
A completamento della feature (test passati con Exit Code 0):
- Verifica che il risultato consegnato rispetti `project_vision.md`, l'eventuale `VISION_[nome_feature].md` e i non-obiettivi dichiarati.
- **Hybrid:** Se la feature ha implicazioni di design, proponi un **ADR** tramite devPNT e aggiorna il Knowledge Layer (KL).
- **Standalone:** Rivedi gli elementi contrassegnati come `[PENDING]` in `ai_docs/audit/audit_plan.md` per estrarre eventuali novità strutturali. Aggiorna `architecture.md` e `existing_features.md` in `ai_docs/strategic/` se necessario.
- Aggiorna i documenti in `ai_docs/vision/` se l'implementazione ha modificato obiettivi, non-obiettivi, milestone, benefici attesi o segnali di successo.
- Riporta lo stato dei file appena rivisti in `ai_docs/audit/audit_plan.md` a `[ANALYZED]`.
- Aggiorna `features_history.md` impostando lo stato a `[COMPLETED]`.

### 6. Gestione delle Sessioni (Handoff)
Quando viene richiesto di mettere in pausa il lavoro o di chiudere la sessione:
- Aggiorna (o crea) il file `ai_docs/audit/handoff.md` descrivendo esattamente a che punto ti trovi (es. "Sto lavorando al file X", "L'ultimo test fallito è Y", "Il prossimo passo è Z"). Questo file serve per preservare il tuo contesto di ragionamento.
