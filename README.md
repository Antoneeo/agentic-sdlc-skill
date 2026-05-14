# Agentic SDLC Skill for Claude Code, Gemini CLI & Codex

A "Documentation-First" SDLC protocol designed to manage the software development lifecycle rigorously. It natively supports **Claude Code** (skill auto-installed in `~/.claude/skills/`), **Gemini CLI** (extension), and **Codex AI** (skill auto-installed in `~/.codex/skills/`).

## Key Features
- **Documentation-First**: Requires documentation (`docs/`) to be created or updated before writing code.
- **Automatic Audit**: Analyzes the existing architecture and features.
- **Traceable Workflow**: Tracks feature status in `features_history.md`.
- **Built-In Quality**: Native integration of analysis, development, and testing.

## Installation

### Via npm (recommended - installs for all detected CLIs)

```bash
npm install -g @antoneeo/agentic-sdlc-skill
```

The `postinstall` script automatically detects installed CLIs and configures each one:

- **Claude Code**: copies the skill to `~/.claude/skills/agentic-sdlc/`. Restart Claude Code; invoke it through the `Skill` tool as `agentic-sdlc`, or let it trigger automatically from SDLC/audit prompts.
- **Gemini CLI**: suggests `gemini extensions install` (see below).
- **Codex AI**: copies the skill to `$CODEX_HOME/skills/agentic-sdlc/` or `~/.codex/skills/agentic-sdlc/`. Restart Codex to load it.

`npm uninstall -g @antoneeo/agentic-sdlc-skill` also removes the skills from `~/.claude/skills/agentic-sdlc/` and `~/.codex/skills/agentic-sdlc/`.

#### Troubleshooting — skill not visible in Claude Code after install

If after `npm install -g` you do **not** see the line `--- Agentic SDLC Skill Discovery ---` in the npm output, and `~/.claude/skills/agentic-sdlc/` does not exist, the `postinstall` hook was skipped by npm. The most common cause is `ignore-scripts=true` in your npm config (set by some Node installers, corporate IT policies, or security tools).

The package ships an explicit `agentic-sdlc-install-skill` command that does the same work but does **not** depend on the `postinstall` hook. After `npm install -g`, the bin shim is created regardless of `ignore-scripts`, so you can simply run:

```bash
npm install -g @antoneeo/agentic-sdlc-skill@latest
agentic-sdlc-install-skill
```

You should see the `--- Agentic SDLC Skill Discovery ---` banner and `📦 Installed Claude Code skill at: ...`. Then restart Claude Code (or Codex) and the skill will be available.

> **Note on `npx`**: because the package exposes two bin commands, the shorthand `npx @antoneeo/agentic-sdlc-skill agentic-sdlc-install-skill` does not work — npx cannot disambiguate. If you prefer npx, use the explicit `-p` form: `npx -p @antoneeo/agentic-sdlc-skill agentic-sdlc-install-skill`.

Alternatively, fix the npm config and reinstall (the `postinstall` hook will then run automatically):

```bash
npm config set ignore-scripts false
npm uninstall -g @antoneeo/agentic-sdlc-skill
npm install -g @antoneeo/agentic-sdlc-skill@latest
```

### Via Gemini CLI (local alternative)

> **Tip:** Before installing, copy this folder from the USB drive to your computer's hard drive (for example, `C:\tools\agentic-sdlc-skill`). This keeps the skill available even after the USB drive is removed.

To install this extension, open a terminal in the folder that contains this README and run:

```bash
gemini extensions install .
```

*Note: If you are in a different folder, replace `.` with the full path to the skill folder.*

## Global Availability
Once installation is complete, the skill is **globally available**. You can close this folder and move to **any other project** on your PC: Gemini CLI will automatically recognize the commands and workflow of the `agentic-sdlc` skill.

## Getting Started

After installation, start Gemini CLI and verify that the skill is available:

1. **List available skills:**
   ```bash
   /skills list all
   ```
2. **Activate the skill:**
   The skill activates automatically when it detects requests related to development, audits, or feature management. You can also invoke it explicitly:
   > "Use the agentic-sdlc skill to analyze this project"

## Project Structure
- `skills/`: Contains the skill logic (`SKILL.md`).
- `references/`: Markdown templates for architecture, analysis, and feature history.
- `gemini-extension.json`: Extension manifest.

---
Created by **Antonio Pinto** ([GitHub](https://github.com/Antoneeo))
(c) 2026 Antonio Pinto. All rights reserved.
