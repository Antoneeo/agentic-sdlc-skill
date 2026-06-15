# Template dei documenti — Agentic SDLC

Regole generali:
- Documenti concisi: ≤ ~80 righe ciascuno (handoff ≤ 20). Se un documento cresce oltre, va diviso, non gonfiato.
- La conformità al template non è l'obiettivo: se una sezione non ha contenuto reale, scrivi esplicitamente perché non si applica. Mai testo riempitivo.
- Date sempre assolute, in UTC dove indicato.

## Header dei documenti canonici (vision/ reference/ architecture/ functional/ strategic/)

Ogni documento canonico durevole apre con questo frontmatter: alimenta il manifest generato `ai_docs/INDEX.md` e dà a un agente il segnale di freschezza prima che si fidi del contenuto.

```markdown
---
description: Una riga — cos'è il documento e quando leggerlo.
status: CURRENT              # CURRENT | SUPERSEDED | DRAFT | DEPRECATED
supersedes: vecchio_doc.md   # solo se rimpiazza un altro doc canonico
---
# Titolo del Documento
```

Quando un doc ne sostituisce un altro: il nuovo dichiara `supersedes:`, il vecchio passa a `status: SUPERSEDED` (resta come storico, non si cancella). `sdlc_check.py validate` avvisa se `status` manca o se un doc superseduto è ancora `CURRENT`.

## ai_docs/vision/project_vision.md

```markdown
# Vision del Progetto
Stato: DRAFT
<!-- Stato: DRAFT (ricostruita dall'agente, NON è autorità di gating)
     oppure APPROVED (da <chi>, <data>) — solo dopo conferma esplicita dell'utente -->

## North Star
## Utenti Target
## Problema Centrale
## Obiettivi
## Non-Obiettivi
## Segnali di Successo
```

## ai_docs/vision/roadmap.md

```markdown
# Roadmap
Stato: DRAFT

## Milestone
<!-- per ciascuna: beneficio atteso, priorità, indicatore di avanzamento -->
```

## ai_docs/vision/principles.md

```markdown
# Principi Decisionali
Stato: DRAFT

<!-- elenco puntato dei principi stabili che guidano trade-off e scope, dal più critico -->
```

## ai_docs/vision/features/VISION_[nome_feature].md

Solo per feature che attraversano più ANALYSIS o più milestone: negli altri casi la vision di feature vive nella sezione `## Vision della Feature` dell'ANALYSIS.

```markdown
# Vision Feature: [Nome]

## Problema
## Beneficio Atteso
## Utenti o Stakeholder
## Segnali di Successo
## Non-Obiettivi / Fuori Scope
## Vincoli e Principi Collegati
```

## ai_docs/solutions/ANALYSIS_[nome_feature].md

Il frontmatter è la fonte di verità dello stato della feature (l'indice `features_history.md` si genera da qui).

```markdown
---
id: F-001
feature: Nome Feature
stato: PLANNED
livello: L3
data_inizio: 2026-06-11
data_fine:
---
# Analisi della Feature: [Nome]

## Obiettivo
<!-- cosa si vuole ottenere e quali problemi risolve -->

## Vision della Feature
<!-- beneficio atteso e problema risolto; allineamento alla vision di progetto
     (citare il documento e il suo stato DRAFT/APPROVED); non-obiettivi/fuori scope
     di questa feature; segnali di successo; stakeholder solo se non ovvi.
     È l'unico posto della vision di feature: il file separato VISION_[feature].md
     si crea solo se la feature attraversa più ANALYSIS o più milestone. -->

## Impatto
<!-- file esistenti toccati, API/contratti, performance, nuove dipendenze -->

## Sicurezza e Threat Model
<!-- SEMPRE obbligatoria, anche in standalone.
     Superfici toccate: input esterni, authN/authZ, crittografia, rete, dati personali, filesystem.
     Minacce principali e mitigazioni. "Nessun impatto di sicurezza" va motivato, non dichiarato. -->

## Piano d'Azione
- [ ] ...

## Strategia di Test
<!-- unit AAA, integrazione, esempi. Se l'ambiente non è eseguibile (firmware/HIL):
     verifica alternativa esplicita e motivo. -->

## Diario / Stato Corrente
<!-- aggiornato a ogni milestone: dove sono, ultimo problema, prossimo passo.
     È la fonte dell'handoff per questa feature. -->
```

Stati ammessi nel frontmatter: `PLANNED` | `IN_PROGRESS` | `COMPLETED` | `CANCELLED`. `COMPLETED` richiede `data_fine`.

## ai_docs/solutions/SPIKE_[tema].md

```markdown
# Spike: [tema]

## Domanda da rispondere
## Time-box
## Cosa è stato provato
## Risposta / Esito
## Conseguenze
<!-- max 1 pagina. Il codice dello spike NON è mergiabile: per produzione riclassificare L2/L3. -->
```

## ai_docs/audit/audit_plan.md (solo modalità Standalone)

Il campo `Riferimento` (hash git o timestamp ISO UTC) è gestito da `sdlc_check.py mark` — non compilarlo a mano. La freschezza si verifica con `sdlc_check.py stale`.

```markdown
# Piano di Audit

Stati: PENDING (da analizzare) | ANALYZED (analizzato, con riferimento) | SKIPPED (con motivo).

| Percorso | Stato | Riferimento | Note |
|---|---|---|---|
| src/core/ | PENDING | - | |
| vendor/ | SKIPPED | - | codice vendored |
```

## ai_docs/audit/handoff.md

Solo un puntatore, ≤ 20 righe. Il dettaglio vive nel Diario di ciascuna ANALYSIS.

```markdown
# Handoff
Data: 2026-06-11 (UTC)
Branch: feature/sso-login
Agente: Claude

## Feature attive
- F-001 — vedi solutions/ANALYSIS_login_sso.md (sezione Diario)

## Prossimo passo
<!-- una riga -->

## Note di sessione
<!-- vision lette in questa sessione? draft da far validare? -->
```

## ai_docs/strategic/architecture.md e existing_features.md

Doc canonici: aprono con l'header (`description:`/`status:`) cosi' entrano puliti nel manifest `INDEX.md`.

```markdown
---
description: Stack, struttura directory e pattern architetturali del progetto.
status: CURRENT
---
# Architettura del Progetto
## Stack Tecnologico
## Struttura delle Directory
## Pattern Architetturali
```

```markdown
---
description: Catalogo sintetico delle funzionalità esistenti del progetto.
status: CURRENT
---
# Funzionalità Esistenti
- [ID] **Nome Feature**: Descrizione
```

`ai_docs/strategic/features_history.md` e `ai_docs/INDEX.md` NON hanno template: sono generati da `sdlc_check.py index`.
