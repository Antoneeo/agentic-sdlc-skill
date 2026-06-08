# Analisi della Feature: Vision Governance

## Obiettivo
- Introdurre un livello documentale dedicato alla Vision del progetto, separato dalla documentazione architetturale e dallo storico feature.
- Ridurre il rischio che gli agenti implementino modifiche tecnicamente corrette ma non allineate all'obiettivo finale del prodotto.
- Rendere obbligatorio il controllo di allineamento alla Vision prima di analisi, sviluppo e chiusura di nuove feature.

## Allineamento alla Vision
- La feature rafforza il principio centrale della skill: la documentazione deve guidare l'implementazione, non inseguirla.
- La Vision diventa il criterio superiore per valutare priorita, scope, non-obiettivi e trade-off.
- Ogni feature significativa dovra avere una mini-vision dedicata o un riferimento esplicito alla Vision di progetto.

## Impatto
- Modifica del protocollo operativo in `skills/agentic-sdlc-skill/SKILL.md`.
- Aggiornamento del template di analisi in `references/analysis_template.md`.
- Aggiunta di template Vision in `references/`.
- Aggiornamento di `scripts/init.js` per creare `ai_docs/vision/` nei nuovi progetti.
- Aggiornamento delle istruzioni generate (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`).
- Aggiornamento della documentazione pacchetto (`README.md`, `CHANGELOG.md`, version metadata).

## Piano d'Azione
1. [x] Definire la struttura `ai_docs/vision/`.
2. [x] Definire il Vision Gate nel workflow della skill.
3. [x] Aggiornare skill, template e script di inizializzazione.
4. [x] Aggiornare documentazione e metadata di release.
5. [x] Eseguire controlli tecnici sugli script modificati.

## Strategia di Test
- Verifica statica di `scripts/init.js` con `node --check`.
- Verifica manuale dei Markdown modificati per coerenza dei percorsi.
- Controllo git diff per confermare che la feature sia limitata alla governance Vision.

## Esito
- `node --check scripts/init.js`: superato.
- `node --check scripts/postinstall.js`: superato.
- `node --check scripts/preuninstall.js`: superato.
