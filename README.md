# Agentic SDLC Skill for Claude Code, Gemini CLI & Codex

Protocollo SDLC "Documentation-First" progettato per gestire in modo rigoroso il ciclo di vita dello sviluppo software. Supporta nativamente **Claude Code** (skill auto-installata in `~/.claude/skills/`), **Gemini CLI** (extension) e **Codex AI** (hooks).

## Caratteristiche principali
- **Documentation-First**: Obbliga alla creazione/aggiornamento della documentazione (`docs/`) prima di scrivere codice.
- **Audit Automatico**: Analizza l'architettura e le feature esistenti.
- **Workflow Tracciabile**: Gestisce lo stato delle feature in `features_history.md`.
- **Qualità Garantita**: Integrazione nativa di analisi, sviluppo e test.

## Installazione

### Via npm (consigliato — installa per tutti i CLI rilevati)

```bash
npm install -g @antoneeo/agentic-sdlc-skill
```

Il `postinstall` rileva automaticamente i CLI installati e configura ciascuno:

- **Claude Code** → copia la skill in `~/.claude/skills/agentic-sdlc/`. Riavvia Claude Code; invocala via tool `Skill` come `agentic-sdlc`, o lasciala triggerare automaticamente da prompt SDLC/audit.
- **Gemini CLI** → suggerisce `gemini extensions install` (vedi sotto).
- **Codex AI** → configurabile via `npx agentic-sdlc-init` nel progetto.

`npm uninstall -g @antoneeo/agentic-sdlc-skill` rimuove anche la skill da `~/.claude/skills/agentic-sdlc/`.

### Via Gemini CLI (alternativa locale)

> **Consiglio:** Prima di installare, copia questa cartella dalla chiavetta USB sul disco fisso del tuo computer (es. in `C:\tools\agentic-sdlc-skill`). In questo modo la skill rimarrà sempre disponibile anche dopo aver rimosso la chiavetta.

Per installare questa estensione, apri il terminale nella cartella che contiene questo README e digita:

```bash
gemini extensions install .
```

*Nota: Se ti trovi in una cartella diversa, sostituisci `.` con il percorso completo della cartella della skill.*

## Disponibilità Globale
Una volta completata l'installazione, la skill è **disponibile globalmente**. Puoi chiudere questa cartella e spostarti in **qualsiasi altro progetto** sul tuo PC: Gemini CLI riconoscerà automaticamente i comandi e il workflow della skill `agentic-sdlc`.

## Come iniziare

Una volta installata, avvia Gemini CLI e verifica che la skill sia presente:

1. **Elenca le skill disponibili:**
   ```bash
   /skills list all
   ```
2. **Attiva la skill:**
   La skill si attiva automaticamente quando rileva richieste relative a sviluppo, audit o gestione feature. Puoi anche richiamarla esplicitamente:
   > "Usa la skill agentic-sdlc per analizzare questo progetto"

## Struttura del Progetto
- `skills/`: Contiene la logica della skill (`SKILL.md`).
- `references/`: Template Markdown per architettura, analisi e storico feature.
- `gemini-extension.json`: Manifesto dell'estensione.

---
Realizzato da **Antonio Pinto** ([GitHub](https://github.com/Antoneeo))
© 2026 Antonio Pinto. Tutti i diritti riservati.
