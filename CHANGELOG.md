# Changelog - Agentic SDLC Skill

Tutte le modifiche significative a questa skill saranno documentate in questo file.

## [1.8.0] - 2026-07-02 (Feature B unit 1: operative guides, project scope)
### Added
- **Operative guides** (`ai_docs/reference/GUIDE_[topic].md`): a durable, source-faithful layer distilled from USER-PROVIDED indications — the capability neither agentic-sdlc nor superpowers had. New support file `guides.md` (pipeline: topic decomposition → user confirmation → verbatim snapshot in `reference/.sources/` with SHA-256 → source-anchored extraction → per-section fidelity markers `[source: …]` / `[not covered by source]`); guide template with provenance frontmatter (`source`, `source_version`, `distilled_from`, `source_hash`) in `templates.md`; short "Operative Guides" section in `SKILL.md`.
- **Generated guide router** `ai_docs/reference/INDEX.md` (emitted by `sdlc_check.py index`, alignment-checked by `validate`): path, status, when-to-consult line and provenance summary per guide — the pointer target for the devPNT Hybrid bridge.
- **Mechanical fidelity controls** in `sdlc_check.py`: provenance-key and per-section marker checks (warn; fails CI under `--strict`); `distilled_from` path confinement — absolute paths, `..` and symlink escapes rejected, fail-closed (ERROR); guide freshness in `stale` — recorded `source_hash` vs current snapshot, flagged in EVERY mode including `--hybrid` (guides are filesystem-first even in Hybrid).

### Changed
- `stale --hybrid` no longer returns unconditionally 0: it still skips audit-plan staleness (delegated to devPNT/KL) but now checks guide-source drift.
- `list_canonical_docs` skips dot-subdirectories of canonical dirs (e.g. `reference/.sources/`): snapshot files are no longer swept into the manifest. Projects that kept `.md` files under dot-subdirs of canonical dirs will see them leave `INDEX.md` (more correct).

### Process note
- First live run of **model-per-dispatch**: implementation dispatched to an economy-tier subagent working from the accepted E-TDD shadow as a self-contained brief; independent deep code review passed first round with zero blocking findings. Governance: M-VISION → D-UC → P-TM → E-ISP → E-TDD, all through independent review gates (devPNT Hybrid).

## [1.7.0] - 2026-07-02 (Phases 0-1 of the evolution roadmap)
### Changed (breaking-soft)
- **English is now the canonical language of the skill**: `SKILL.md`, `templates.md`, `ENFORCEMENT.md`, validator messages, generated indexes and the project protocol are in English. New ANALYSIS documents use English frontmatter keys (`status`, `level`, `start_date`, `end_date`) and English section headings. **Existing projects keep working**: the validator silently accepts the deprecated Italian keys (`stato`, `livello`, `data_inizio`, `data_fine`) and Italian headings.
- The generated project protocol (`CLAUDE.md`/`GEMINI.md`/`AGENTS.md`/`.cursorrules`) is now a **thin pointer** to the skill (triage summary + where things live + closure gate) instead of a condensed copy of its rules, which had drifted from `SKILL.md`.
- `init.js` now seeds `ai_docs/` from `templates.md` (single template source) instead of inline boilerplates; it creates `ai_docs/reference/` and the curated `ai_docs/README.md`, no longer seeds the generated `features_history.md`, and generates `INDEX.md` via the validator when Python is available, so the very first `sdlc_check.py check` on a fresh project is CLEAN.
- Client detection unified between `init.js` and `postinstall.js` (`scripts/lib.js`): CLI on PATH **or** config home present (covers Claude Desktop with integrated Claude Code).

### Added
- `sdlc_check.py validate --strict` / `check --strict`: warnings and a missing `ai_docs/` become failures (for CI).
- **Coexistence with devPNT (Phase 1, the Hybrid seam)**: new SKILL.md section with the ownership matrix (who is master per artifact in Standalone vs Hybrid), the triage equivalence table (one significance threshold, two vocabularies), the ANALYSIS↔plan-node state mapping and the shadow discipline (`SHADOW_[doc_key]_vX.Y.md`, exported BEFORE implementation; never saved under an `ANALYSIS_*` name).
- `sdlc_check.py --hybrid` (explicit, never auto-detected) on `check`/`stale` (audit-plan staleness delegated to devPNT/KL) and on `gate` (an approved E-TDD shadow in `solutions/` authorizes writes on protected paths).
- devPNT MCP doctrine (`mcp_system_prompt.md`, devPNT repo) slimmed accordingly: process (triage, phases, lifecycle, closure) deferred to the skill; `ai_docs/` layout aligned (adds `vision/` and `reference/`); shadow naming and shadow-before-implementation rule; checklist items for methodology, shadow export and hybrid closure gate.
- Evolution roadmap for v1.7.0 in `ai_docs/vision/roadmap_evoluzione_agenti.md` (subagent execution, operative guides + agent-level knowledge base, devPNT seam, open-core positioning).

### Fixed
- Shadow detection is structural (filename `SHADOW_*` or `<!-- SHADOW` marker on the first line): an ANALYSIS merely *mentioning* shadows is no longer silently skipped from index and validation.
- `mark`/`index` fail fast when `ai_docs/` is missing instead of silently creating a second documentation root in the wrong directory.

### Removed
- Divergent `agentic-sdlc-v2/` copy (integrated in 1.5.0, the leftover risked edits on the wrong files).
- `references/*_template.md` (duplicated `templates.md` and had already diverged).

## [1.6.0] - 2026-06-15
### Added
- **Manifest generato dei documenti canonici** (`ai_docs/INDEX.md`): `sdlc_check.py index` ora produce, oltre a `features_history.md`, un indice completo di tutti i doc in `vision/`, `reference/`, `architecture/`, `functional/`, `strategic/`, con descrizione e stato letti dall'header. Si rigenera, quindi non drifta.
- **Lifecycle dei documenti canonici**: convenzione header `status: CURRENT|SUPERSEDED|DRAFT|DEPRECATED` + `supersedes:`. `validate` avvisa se `status` manca/è invalido o se un doc superseduto è ancora `CURRENT`. Stop ai grep che riportano a guide obsolete.
- **Modello a due indici** documentato nella sezione "Documenti ai_docs" di `SKILL.md`: `README.md` curato (must-read, a mano) vs `INDEX.md` generato (completo, meccanico) — ruoli separati, prima confusi in un unico README che driftava.

### Changed
- §1 Audit: leggere `README.md` + `INDEX.md` all'avvio per sapere cosa esiste prima di esplorare il codice.
- §3 Analisi: cercare con glob/grep un'ANALYSIS esistente prima di crearne una nuova (anti-duplicazione).
- §5 Chiusura: gate "Indici allineati" — rigenerare `INDEX.md`, aggiornare il `README.md` curato per i must-read, marcare lo `status`; doc canonico non indicizzato o senza `status` = chiusura sporca.
- `templates.md`: aggiunto il template dell'header dei documenti canonici.

### Fixed
- `sdlc_check.py` legge ora i file con `utf-8-sig`: un BOM iniziale (file autorati su Windows) non impedisce più il riconoscimento del frontmatter `---`.
- L'estrattore dell'header riconosce sia il frontmatter `status:` sia la riga in corpo `**Status:**`/`Stato:`, e gli stati di tutte le convenzioni in uso (canonici `CURRENT/SUPERSEDED/DRAFT/DEPRECATED`, vision `DRAFT/APPROVED`, ADR `Accepted/Proposed/Rejected`) — niente più falsi avvisi "status non riconosciuto" su `APPROVED`/`Accepted`.
- La descrizione del manifest salta righe di metadati (`Date`, `Created`, `Task ref`, ...) e i commenti HTML, così non finiscono come descrizione del documento.
- `index` non genera più un `INDEX.md` vuoto su progetti senza documenti canonici (solo `solutions/`+`audit/`).

### Migrazione (da 1.5.x)
- Al primo `sdlc_check.py check`/`validate` dopo l'upgrade, un progetto con documenti canonici darà **un errore** `ai_docs/INDEX.md mancante`: è atteso — esegui **una volta** `sdlc_check.py index` per generarlo. Da lì in poi resta allineato.
- I documenti canonici preesistenti senza `status:` produrranno **avvisi** (non errori): aggiungi l'header `description:`/`status:` per silenziarli. I nuovi progetti nascono già compatibili (template aggiornati).

## [1.5.0] - 2026-06-13
### Added
- Introdotta la Regola Zero di triage (`L1`, `L2`, `L3`, `Spike`) per rendere il processo proporzionale al rischio.
- Aggiunta simbiosi esplicita con devPNT: in Hybrid la `M-VISION` guida la milestone, il Master Plan resta roadmap strategica e l'Action Plan governa l'esecuzione tattica.
- Aggiunti support file dentro la skill runtime: `templates.md`, `ENFORCEMENT.md`, `scripts/sdlc_check.py`.
- `agentic-sdlc-install-skill` ora installa la skill nativa anche in `~/.gemini/skills/agentic-sdlc/`.
- Aggiunto validatore meccanico opzionale per frontmatter ANALYSIS, Vision state, indice feature e audit stale.

### Changed
- Il nome pubblico resta `agentic-sdlc`; la proposta v2 e' stata integrata come evoluzione, non come skill parallela.
- Aggiornati `agentic-sdlc-init`, template, protocolli generati, README e metadata.
- La modalita Standalone resta completa; devPNT e' un livello di governance superiore, non un prerequisito.

## [1.4.0] - 2026-06-07
### Added
- Introdotta la governance della **Vision** con nuova struttura `ai_docs/vision/` (`project_vision.md`, `roadmap.md`, `principles.md`, `features/`).
- Aggiunto il **Vision Gate** nel workflow operativo: ogni feature significativa deve essere verificata rispetto a obiettivi, non-obiettivi, benefici attesi e segnali di successo prima dell'analisi tecnica.
- Aggiunti template Vision in `references/` e sezione `Allineamento alla Vision` nel template di analisi.
- `agentic-sdlc-init` ora crea i documenti Vision boilerplate nei nuovi progetti.

## [1.3.1] - 2026-05-14
### Fixed
- Correzione documentazione (README + CHANGELOG) della sintassi per invocare il bin `agentic-sdlc-install-skill`. La forma `npx @antoneeo/agentic-sdlc-skill agentic-sdlc-install-skill` documentata in 1.3.0 **non funziona** perché npx non riesce a disambiguare il bin quando il pacchetto ne espone più di uno (errore: `could not determine executable to run`). Sintassi corretta: lanciare `agentic-sdlc-install-skill` direttamente dopo `npm install -g`, oppure usare `npx -p @antoneeo/agentic-sdlc-skill agentic-sdlc-install-skill` con `-p` esplicito.
- Nessuna modifica al codice della skill: il bin di 1.3.0 funziona correttamente, era solo la doc a indicare la sintassi sbagliata.

## [1.3.0] - 2026-05-14
### Added
- Nuovo comando esplicito `agentic-sdlc-install-skill` (registrato come `bin`): installa la skill in `~/.claude/skills/agentic-sdlc/` e `~/.codex/skills/agentic-sdlc/` **senza dipendere dal `postinstall` hook**. Risolve i casi in cui `npm` salta gli script (configurazioni `ignore-scripts=true`, policy IT aziendali, alcuni installer Node) e l'auto-install fallisce silenziosamente.
- Sezione "Troubleshooting" nel README con istruzioni per il caso in cui la skill non venga rilevata da Claude Code dopo `npm install -g`.

### Usage
```bash
npm install -g @antoneeo/agentic-sdlc-skill@latest
agentic-sdlc-install-skill
```

## [1.2.4] - 2026-05-14
### Fixed
- `postinstall` ora rileva Claude Code anche quando il CLI `claude` non è nel PATH (es. Claude Desktop con Claude Code integrato): la presenza di `~/.claude/` o della variabile `CLAUDE_CONFIG_DIR` è sufficiente per attivare l'installazione della skill in `~/.claude/skills/agentic-sdlc/`. Stesso pattern già usato per Codex.
- `preuninstall` rispetta `CLAUDE_CONFIG_DIR` per rimuovere la skill dalla directory di configurazione corretta.

## [1.2.2] - 2026-05-10
### Changed
- README convertito in inglese per la pubblicazione npm.
- Versione allineata a `1.2.2` in `package.json` e `gemini-extension.json`.

## [1.2.1] - 2026-05-10
### Fixed
- `postinstall` ora registra la skill anche per Codex copiandola in `$CODEX_HOME/skills/agentic-sdlc/` oppure `~/.codex/skills/agentic-sdlc/`.
- `preuninstall` rimuove anche la copia Codex della skill.
- `agentic-sdlc-init` ora crea `AGENTS.md` per Codex invece di `.codex/hooks.json`, che Codex non carica come istruzioni di progetto.

## [1.2.0] - 2026-05-10
### Added
- **Auto-installazione skill nativa Claude Code**: il `postinstall` ora copia `skills/agentic-sdlc-skill/` in `~/.claude/skills/agentic-sdlc/` quando rileva il CLI `claude`. La skill diventa disponibile come `agentic-sdlc` nel tool `Skill` di Claude Code dopo riavvio.
- Nuovo script `preuninstall.js` che rimuove la skill da `~/.claude/skills/agentic-sdlc/` durante `npm uninstall`.
- Fallback `copyRecursive` per Node < 16.7 (quando `fs.cpSync` non disponibile).

### Changed
- `package.json`: bump versione a 1.2.0, aggiunti keyword `claude-code` e `claude-skill`, descrizione aggiornata per riflettere supporto Claude Code nativo.

### Fixed
- Risolto bug per cui il pacchetto npm non registrava la skill in Claude Code (la cartella `~/.claude/skills/` non veniva mai popolata).

## [1.1.0] - 2026-05-10
### Fixed
- Fixed path inconsistencies in the generated `CLAUDE.md`, `GEMINI.md`, and `.cursorrules` protocols. Added full paths (`ai_docs/strategic/`) to all document references to ensure AI agents (like Claude) can correctly find and update them.
- Cleaned up encoding issues in initialization scripts.

## [1.0.9] - 2026-05-10
### Added
- New **Smart Discovery** system during project initialization.
- Official support for **Codex AI** via automatic `.codex/hooks.json` injection.
- Support for **Cursor** and **Windsurf** via `.cursorrules`.
- Binary command `agentic-sdlc-init` for use via `npx`.
- `postinstall` script for global AI CLI detection (Claude, Gemini, Codex).
- Full English localization for all user-facing messages and scripts.

### Changed
- Updated `init.js` to support the new `ai_docs/` directory structure defined in v1.0.8.

## [1.0.8] - 2026-05-10
### Aggiunto
- Skill evoluta in "Hybrid Edition": integrazione opzionale con **devPNT** (server MCP) per governance avanzata tramite database e piani gerarchici.
- Fase di Discovery per il rilevamento automatico dell'ambiente (Standalone vs Hybrid).
- Supporto per ADR (Architecture Decision Records) e Knowledge Layer (KL) nella fase di chiusura.

### Modificato
- Riorganizzazione dei percorsi di documentazione (`ai_docs/strategic/`, `ai_docs/audit/`, `ai_docs/solutions/`).
- Aggiornata la documentazione funzionale (`architecture_overview.md`, `external_interfaces.md`) con definizioni più precise.

## [1.0.7] - 2026-05-10
### Modificato
- Aggiornata l'attribuzione dell'autore (Antonio Pinto) e il copyright in tutti i file (`package.json`, `README.md`, `SKILL.md`).
- Aggiunto link al profilo GitHub ufficiale.

## [1.0.6] - 2026-05-10
### Aggiunto
- Sincronizzazione completa dei file del progetto nel repository.
- Supporto per il tracciamento delle feature e audit plan.

## [1.0.5] - 2026-04-17
### Aggiunto
- File `CHANGELOG.md` per il tracciamento delle versioni.

## [1.0.4] - 2026-04-17
### Modificato
- `README.md`: Aggiunte istruzioni specifiche per l'installazione da chiavetta USB e chiarimenti sulla disponibilità globale della skill.

## [1.0.3] - 2026-04-17
### Aggiunto
- Primo `README.md` con istruzioni di installazione e attivazione.

## [1.0.2] - 2026-04-17
### Corretto
- Riorganizzata la struttura delle cartelle secondo gli standard di Gemini CLI (`skills/agentic-sdlc-skill/SKILL.md`).
- Aggiunto frontmatter YAML a `SKILL.md` per la scoperta automatica.

## [1.0.1] - 2026-04-17
### Corretto
- Aggiunto `gemini-extension.json` (manifest dell'estensione) mancante nella versione iniziale.

## [1.0.0] - 2026-04-17
### Iniziale
- Prima pubblicazione della skill (Protocollo SDLC Documentation-First).
