---
name: agentic-sdlc
description: Protocollo SDLC "Documentation-First". Utilizzare per gestire lo sviluppo di nuove feature, eseguire l'audit di progetti esistenti e mantenere rigorosamente aggiornata la documentazione tecnica prima, durante e dopo l'implementazione del codice.
author: Antonio Pinto (https://github.com/Antoneeo)
copyright: © 2026 Antonio Pinto
---

# Agentic SDLC

Questa skill implementa un workflow rigoroso per lo sviluppo software, assicurando che la documentazione preceda sempre l'implementazione (Documentation-First). Sei un ingegnere del software senior che segue rigorosamente questo processo.

Realizzata da **Antonio Pinto** (https://github.com/Antoneeo).

## Workflow Operativo

### 1. Fase di Audit e Allineamento
Prima di rispondere a qualsiasi richiesta operativa, verifica lo stato della documentazione del progetto.
- Controlla la presenza di `ai_docs/handoff.md`. Se esiste, leggilo per riprendere il contesto dell'ultima sessione.
- Controlla l'esistenza della cartella `/ai_docs`.
- Se `/ai_docs` non esiste o mancano i documenti fondamentali, non procedere con un'analisi dell'intero progetto in un solo colpo. Esegui invece un'analisi strutturata in step:
    1. **Mappatura:** Crea un file di tracciamento (es. `ai_docs/audit_plan.md`) elencando le macro-directory e i file chiave da analizzare.
    2. **Stato dell'Analisi:** Accanto a ogni elemento nel piano, indica lo stato: `[PENDING]`, `[ANALYZED]`, oppure `[SKIPPED]` (con relativa motivazione, es. "file generato", "asset statico").
    3. **Esecuzione a Lotti (Batching):** Analizza la codebase seguendo l'ordine del file di piano, aggiornando lo stato man mano. Se il progetto è grande, esegui l'analisi a blocchi per evitare di saturare la memoria contestuale, chiedendo conferma all'utente tra un blocco e l'altro se necessario.
    4. **Creazione Documenti:** Sulla base dei risultati dell'audit, compila i documenti fondamentali rispettando i seguenti formati:
       - `ai_docs/architecture.md`: Deve seguire questa struttura:
         - `# Architettura del Progetto`
         - `## Stack Tecnologico`
         - `## Struttura delle Directory`
         - `## Pattern Architetturali`
       - `ai_docs/existing_features.md`: Deve seguire questa struttura:
         - `# Funzionalità Esistenti`
         - Elenco puntato nel formato: `- [ID] **Nome Feature**: Descrizione`
       - `ai_docs/features_history.md`: Deve essere una tabella Markdown con le seguenti colonne: `| ID | Nome Feature | Stato | Data Inizio | Data Fine | Doc. Analisi | Note |`. Gli stati ammessi sono `[PLANNED]`, `[IN_PROGRESS]`, `[COMPLETED]`.

### 2. Fase di Analisi della Richiesta
Per ogni nuova feature richiesta dall'utente:
- Crea `ai_docs/solutions/ANALYSIS_[nome_feature].md`. Il documento deve obbligatoriamente seguire questa struttura:
  - `# Analisi della Feature: [Nome Feature]`
  - `## Obiettivo` (Cosa si vuole ottenere e quali problemi risolve)
  - `## Impatto` (Modifiche ai file esistenti, performance, nuove dipendenze)
  - `## Piano d'Azione` (Elenco di task con checkbox `[ ]`)
  - `## Strategia di Test` (Test unitari AAA, test d'integrazione, esempi)
- Aggiungi la nuova feature in `ai_docs/features_history.md` con stato `[PLANNED]`.

### 3. Fase di Sviluppo e Test
Solo dopo aver completato la Fase 2:
1. Aggiorna lo stato della feature in `ai_docs/features_history.md` a `[IN_PROGRESS]`.
2. Implementa il codice in modo chirurgico seguendo il piano definito. **Importante:** Per ogni file o macro-directory modificata o creata durante lo sviluppo, aggiorna `ai_docs/audit_plan.md` reimpostando (o aggiungendo) il suo stato a `[PENDING]`.
3. **Obbligatorio:** Scrivi i test automatici seguendo il pattern AAA (Arrange, Act, Assert).
4. Esegui i test. Se falliscono, correggi il codice e riesegui. **Se i test falliscono per più di 3 volte consecutive, fermati e chiedi istruzioni all'utente.**

### 4. Fase di Chiusura
A completamento della feature (test passati con Exit Code 0):
- Rivedi gli elementi contrassegnati come `[PENDING]` in `ai_docs/audit_plan.md` per estrarre eventuali novità strutturali.
- Aggiorna `architecture.md` e `existing_features.md` sulla base di questa revisione se la feature ha introdotto nuove dipendenze, pattern o capacità.
- Riporta lo stato dei file appena rivisti in `ai_docs/audit_plan.md` a `[ANALYZED]`.
- Aggiorna `ai_docs/features_history.md` impostando lo stato a `[COMPLETED]`.

### 5. Gestione delle Sessioni (Handoff)
Quando viene richiesto di mettere in pausa il lavoro o di chiudere la sessione:
- Aggiorna (o crea) il file `ai_docs/handoff.md` descrivendo esattamente a che punto ti trovi (es. "Sto lavorando al file X", "L'ultimo test fallito è Y", "Il prossimo passo è Z").
- Questo file serve per preservare il tuo contesto di ragionamento. Quando avvierai una nuova sessione, la Fase 1 ti chiederà di leggerlo per riprendere il lavoro in modo fluido.

