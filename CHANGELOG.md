# Changelog - Agentic SDLC Skill

Tutte le modifiche significative a questa skill saranno documentate in questo file.

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
