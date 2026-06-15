---
id: F-001
feature: Vision Governance
stato: COMPLETED
livello: L3
data_inizio: 2026-06-07
data_fine: 2026-06-07
---
# Analisi della Feature: Vision Governance

## Obiettivo
- Introdurre un livello documentale dedicato alla Vision del progetto, separato dalla documentazione architetturale e dallo storico feature.
- Ridurre il rischio che gli agenti implementino modifiche tecnicamente corrette ma non allineate all'obiettivo finale del prodotto.
- Rendere obbligatorio il controllo di allineamento alla Vision prima di analisi, sviluppo e chiusura di nuove feature.

## Vision della Feature
- La feature rafforza il principio centrale della skill: la documentazione deve guidare l'implementazione, non inseguirla.
- La Vision diventa il criterio superiore per valutare priorita, scope, non-obiettivi e trade-off.
- Ogni feature significativa deve citare un beneficio atteso e rispettare i non-obiettivi dichiarati.

## Impatto
- Modifica del protocollo operativo in `skills/agentic-sdlc-skill/SKILL.md`.
- Aggiornamento del template di analisi in `references/analysis_template.md`.
- Aggiunta di template Vision in `references/`.
- Aggiornamento di `scripts/init.js` per creare `ai_docs/vision/` nei nuovi progetti.
- Aggiornamento delle istruzioni generate (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`).
- Aggiornamento della documentazione pacchetto (`README.md`, `CHANGELOG.md`, version metadata).

## Sicurezza e Threat Model
- Nessuna superficie runtime sensibile e' stata introdotta.
- La modifica ha cambiato solo governance documentale, template e script di inizializzazione.
- Rischio principale: Vision auto-generata scambiata per autorita. Mitigazione successiva: stato DRAFT/APPROVED introdotto in Agentic SDLC vNext.

## Piano d'Azione
- [x] Definire la struttura `ai_docs/vision/`.
- [x] Definire il Vision Gate nel workflow della skill.
- [x] Aggiornare skill, template e script di inizializzazione.
- [x] Aggiornare documentazione e metadata di release.
- [x] Eseguire controlli tecnici sugli script modificati.

## Strategia di Test
- `node --check scripts/init.js`
- `node --check scripts/postinstall.js`
- `node --check scripts/preuninstall.js`
- Verifica manuale dei Markdown modificati per coerenza dei percorsi.

## Diario / Stato Corrente
- 2026-06-07: Feature completata. La governance Vision e' stata introdotta nei documenti e nei protocolli generati.
