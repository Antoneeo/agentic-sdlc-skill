---
name: agentic-sdlc
description: Protocollo SDLC Documentation-First con triage proporzionale, Vision come guida, modalita Standalone completa e simbiosi opzionale con devPNT. Usare per feature, bug significativi, refactor, audit e manutenzione documentata.
author: Antonio Pinto (https://github.com/Antoneeo)
copyright: (c) 2026 Antonio Pinto
---

# Agentic SDLC

Questa skill guida lo sviluppo software con un processo Documentation-First proporzionale al rischio. Deve funzionare pienamente anche senza devPNT. Quando devPNT e' disponibile e configurato per il progetto corrente, la skill lavora in simbiosi con la sua governance: M-VISION, Master Plan, Action Plan e artefatti versionati diventano il quadro autorevole per milestone e implementazione.

File di supporto nella directory della skill:
- `templates.md`: template per Vision, ANALYSIS, Spike, audit plan e handoff.
- `scripts/sdlc_check.py`: validatore meccanico per `ai_docs/` (`check`, `validate`, `index`, `stale`, `mark`, `gate`).
- `ENFORCEMENT.md`: setup opzionale per CI e hook.

Leggi questi file solo quando servono. `SKILL.md` e' il contratto operativo; i support file sono risorse progressive.

## Valori Tecnici

- **Comprendi prima di agire:** non modificare codice senza capire root cause, vincoli e forma attuale.
- **Mantieni coerenza architetturale:** rispetta layer, responsabilita, naming, pattern e convenzioni esistenti.
- **Applica DRY e semplicita:** non duplicare logica o conoscenza; astrai solo se riduce complessita reale.
- **Preserva qualita:** ogni modifica deve mantenere o migliorare stabilita, testabilita e manutenibilita.
- **Verifica tecnicamente:** chiudi lavoro implementativo con test, lint, smoke check o motivo esplicito.
- **Mantieni memoria utile:** documenta decisioni e stato operativo rilevanti, non testo riempitivo.
- **Proteggi la Vision:** ogni decisione deve restare allineata a benefici attesi, utenti, non-obiettivi e segnali di successo.

Se una patch sembra facile ma non capisci perche il codice attuale e' fatto cosi, indaga prima.

## Regola Zero: Triage

Classifica sempre la richiesta prima di scegliere il processo. Dichiara il livello scelto all'utente quando inizi il lavoro operativo.

| Livello | Criteri | Processo richiesto |
|---|---|---|
| **L1 - Triviale** | Circa 10 righe in 1-2 file; nessun cambio API, dipendenza o comportamento nuovo; refusi o fix che ripristinano comportamento gia atteso | Implementa. Esegui test pertinenti se esistono. Nessun nuovo documento. |
| **L2 - Piccolo** | Root cause chiara; massimo 3 file; nessuna nuova dipendenza o API pubblica; rischio basso | Mini-analisi nel messaggio: obiettivo, impatto, sicurezza, test. Test obbligatori. Nessun nuovo documento salvo aggiornare analisi/handoff esistenti se utile. |
| **L3 - Significativo** | Oltre 3 file, API/contratti, nuova dipendenza, comportamento visibile, area security-sensitive, cambio architetturale o design non ovvio | Workflow completo: Vision Gate, analisi, piano, implementazione, test, chiusura. |
| **Spike** | Esplorazione time-boxed per ridurre incertezza | Codice non mergiabile in main. Esito in `ai_docs/solutions/SPIKE_[tema].md`. Per produzione riclassifica come L2 o L3. |

Regole trasversali:
- Parsing input esterni, authN/authZ, crittografia, rete, dati personali e filesystem sono security-sensitive: mai L1.
- Se durante L1/L2 emerge impatto maggiore, fermati, riclassifica e dichiaralo.
- Nel dubbio scegli il livello piu alto.
- L'audit completo non parte per L1/L2 salvo richiesta esplicita.

## Modalita Operative

### Standalone completa

Usa questa modalita quando devPNT non e' disponibile, non e' configurato per il progetto corrente o l'utente chiede esplicitamente un workflow solo filesystem.

Fonte di verita:
- Vision: `ai_docs/vision/project_vision.md`, `roadmap.md`, `principles.md`.
- Feature/analisi: `ai_docs/solutions/ANALYSIS_[feature].md`.
- Audit/handoff: `ai_docs/audit/`.
- Storico feature: `ai_docs/strategic/features_history.md` manuale o generato dal validatore, in base alla struttura adottata dal progetto.

La modalita Standalone non e' ridotta: deve poter gestire audit, feature, bug significativi, test, handoff e chiusura senza devPNT.

### Hybrid in simbiosi con devPNT

Usa questa modalita quando i tool `devpnt_*` sono disponibili e puntano al progetto corrente.

Gerarchia autorevole:
1. **M-VISION devPNT**: faro strategico della milestone. Prima di design o codice, leggila e verifica benefici, success signals, scope-in e non-goals.
2. **Master Plan devPNT**: roadmap strategica e milestone.
3. **Action Plan devPNT**: lavoro tattico corrente per il goal attivo.
4. **Artefatti governati devPNT**: `D-UC`, `P-TM`, `E-ISP`, `E-TDD`, `E-TP`, ADR.
5. **`ai_docs/` locale**: contesto leggibile, fallback Standalone, handoff locale o shadow/mirror quando utile.

Regole Hybrid:
- devPNT e' la fonte governata per piani e artefatti; non creare una seconda verita in `ai_docs/`.
- La skill resta autonoma: se devPNT non c'e', passa a Standalone senza perdere capacita.
- Se richiesta utente, Vision locale e M-VISION divergono, fermati e rendi esplicito il conflitto.
- Non creare o modificare milestone senza rispettare la M-VISION.
- Non accettare automaticamente proposte devPNT: presenta la preview e attendi conferma esplicita.
- Se il protocollo devPNT locale impone bootstrap, piani o gate piu severi, seguili.

## Workflow L3

### 1. Audit e Allineamento

- Leggi `ai_docs/audit/handoff.md` se esiste; se ha Data/Branch non coerenti, trattalo come storico.
- Leggi `ai_docs/README.md` (must-read curati) e `ai_docs/INDEX.md` (manifest generato di tutti i doc canonici) per sapere cosa esiste prima di esplorare il codice. `solutions/` e `audit/` non sono indicizzate per file: cercale con glob/grep.
- Se `ai_docs/` manca o e' incompleta, crea struttura e documenti minimi analizzando il progetto a lotti.
- In Standalone usa `ai_docs/audit/audit_plan.md` per mappatura e stato.
- In Hybrid preferisci la mappatura devPNT/KL quando disponibile; non duplicare la governance dei piani.
- Per template dettagliati usa `templates.md`.

### 2. Vision Gate

Standalone:
- Leggi `project_vision.md`, `roadmap.md`, `principles.md`.
- Se un documento dichiara `Stato: DRAFT`, trattalo come ipotesi: segnala conflitti, ma non bloccare una richiesta esplicita dell'utente.
- Se dichiara `Stato: APPROVED`, e la richiesta confligge, fermati e chiedi scelta: aggiornare Vision o modificare/rifiutare la richiesta.
- Non promuovere mai una Vision a `APPROVED` senza conferma dell'utente.

Hybrid:
- Leggi la M-VISION della milestone o chiedi/crea il passaggio richiesto dal protocollo devPNT.
- Verifica che la richiesta serva un beneficio o success signal della M-VISION.
- Se la richiesta aggiunge scope non autorizzato, trattala come divergenza di Vision.

### 3. Analisi della Richiesta

Standalone L3:
- Prima di creare un nuovo `ANALYSIS_[feature].md`, cerca con glob/grep in `ai_docs/solutions/` un'analisi gia' esistente sullo stesso tema: se c'e', aggiornala invece di duplicarla.
- Crea o aggiorna `ai_docs/solutions/ANALYSIS_[feature].md`.
- Sezioni minime: Obiettivo, Vision della Feature o Allineamento alla Vision, Impatto, Sicurezza e Threat Model, Piano d'Azione, Strategia di Test, Diario/Stato Corrente.
- Per feature che attraversano piu milestone o piu analisi, crea anche `ai_docs/vision/features/VISION_[feature].md`.

Hybrid L3:
- Ripristina Master Plan, Action Plan e documenti collegati.
- Usa devPNT per piani e artefatti governati.
- Usa `ai_docs/solutions/SHADOW_[doc_key]_vX.Y.md` solo come shadow leggibile quando serve; in divergenza vince devPNT.

### 4. Sviluppo e Test

- Implementa solo dopo il gate documentale richiesto dal livello.
- Modifica in modo chirurgico, coerente con il piano.
- Scrivi o aggiorna test automatici pertinenti; usa AAA per unit test quando applicabile.
- Se l'ambiente non permette test automatici, dichiara verifica alternativa e motivo.
- Circuit breaker: dopo 3 esecuzioni consecutive senza progresso sui test, fermati e chiedi istruzioni.
- Aggiorna il Diario dell'ANALYSIS o l'Action Plan quando completi milestone, incontri blocchi o cambi decisione.

### 5. Chiusura

- Esegui test/lint/smoke check pertinenti.
- Verifica allineamento con Vision locale o M-VISION devPNT.
- Aggiorna solo i documenti effettivamente impattati.
- **Indici allineati (Poka-Yoke)**: se hai creato, spostato o rimosso documenti canonici (`vision/`, `reference/`, `architecture/`, `functional/`, `strategic/`):
  - rigenera il manifest con `sdlc_check.py index` (scrive `ai_docs/INDEX.md`) — non scriverlo a mano;
  - se il documento e' must-read, aggiungi/aggiorna la sua riga nel `README.md` curato;
  - se il documento ne sostituisce un altro, marca il vecchio `status: SUPERSEDED` e dichiara `supersedes:` nel nuovo;
  - se hai creato una nuova sottodirectory canonica, dalle uno scopo nel `README.md`.
  Doc canonico non indicizzato o senza `status` = chiusura sporca (`sdlc_check.py check` fallisce/avvisa). Non dichiarare DONE finche' non e' pulito. Dettagli: sezione "Documenti ai_docs".
- In Hybrid proponi ADR/KL quando ci sono decisioni architetturali.
- In Standalone, se il progetto adotta `sdlc_check.py`, esegui `python <skill_dir>/scripts/sdlc_check.py check --root <project_root>` o la copia locale equivalente.
- I documenti aggiornati devono viaggiare nello stesso commit/PR del codice che descrivono.

## Documenti ai_docs: due indici + lifecycle

I documenti in `ai_docs/` hanno due ruoli serviti da due indici distinti — non confonderli:

- **`ai_docs/README.md` (curato, a mano):** la priorita' di lettura. Poche righe, solo must-read canonici, cambia di rado. Giudizio umano su "cosa leggere prima".
- **`ai_docs/INDEX.md` (generato, `sdlc_check.py index`):** il manifest completo di ogni doc canonico (`vision/`, `reference/`, `architecture/`, `functional/`, `strategic/`) con descrizione e stato. Mai a mano: si rigenera, cosi' non drifta.
- **`strategic/features_history.md` (generato):** lo storico delle ANALYSIS, dai loro frontmatter.
- `audit/` e `solutions/` sono discovery-by-grep: non entrano nel manifest.

**Header dei documenti canonici (lifecycle).** Ogni doc in quelle directory dovrebbe aprirsi con un frontmatter minimo, cosi' il manifest si genera da solo e un agente sa subito se fidarsi:

```markdown
---
description: Una riga — cos'e' e quando leggerlo.
status: CURRENT              # CURRENT | SUPERSEDED | DRAFT | DEPRECATED
supersedes: vecchio_doc.md   # solo se rimpiazza un altro doc
---
```

In fallback (nessun frontmatter) il manifest deduce il titolo dal primo `# H1` e la descrizione dalla prima riga di prosa o blockquote; ma senza `status` un doc non porta segnale di freschezza. `status` mancante, valore non valido, o doc superseduto ancora `CURRENT` = avviso in `validate`. Un doc `SUPERSEDED` resta sul filesystem come storico, ma il suo stato lo dichiara morto: niente piu' grep che riportano a guide obsolete.

Senza Python/hook (ambienti minimali) gli indici e gli header restano una disciplina di prosa: aggiorna `README.md` e marca lo `status` a mano; il validatore e' solo il backstop dove e' adottato.

## Enforcement Meccanico

Il prompt non e' enforcement. Quando il progetto richiede garanzie ripetibili:
- leggi `ENFORCEMENT.md`;
- usa `scripts/sdlc_check.py validate` in CI;
- usa `scripts/sdlc_check.py gate` solo per directory security-critical, non per tutto il repository.

Il validatore e' un supporto, non un prerequisito universale: la skill deve restare usabile anche in ambienti senza Python o senza hook, dichiarando cosa non puo' verificare automaticamente.
