# KB Agentic Skill for Claude Code, Gemini CLI, Google Antigravity & Codex

`kb-agentic` is a Documentation-First & Knowledge-Base protocol for AI agents. It supports Claude Code, Codex, Gemini CLI, Google Antigravity 2.0, Cursor/Windsurf-style project instructions, and optional devPNT governance.

## Key Features

- **Risk-proportional knowledge triage**: L1/L2/L3/Spike triage avoids heavyweight process for quick facts, with a symmetric **Write Triggers** table mapping each knowledge event to the document it produces (one event, one destination).
- **Vision-guided knowledge governance**: Standalone projects use `ai_docs/vision/`; Hybrid projects use devPNT `M-VISION` as the milestone north star.
- **Taxonomy pass — categories and SOPs before new documents**: at L3, before creating a new document, the topic is checked against existing categories, entities, and SOPs to prevent duplication across `ai_docs/`.
- **Signal distillation & fact verification**: Contract-first writing and noise elimination to produce high-signal, verifiable documentation.
- **Knowledge reconciliation**: Systematic process for resolving conflicting notes, updating stale specs, and marking superseded documents (`status: SUPERSEDED`).
- **Operative guides + agent-global KB**: Distill user-provided indications into source-faithful operative `GUIDE_*.md` (`source_kind: document`).
- **Installed support files**: Claude, Codex, Gemini, and Google Antigravity receive the full skill folder, including `templates.md`, `taxonomy.md`, `guides.md`, `vision.md`, `distillation.md`, `reconciliation.md`, `elicitation.md`, `review.md`, `dispatch.md`, `ENFORCEMENT.md`, and `scripts/sdlc_check.py`.
- **Mechanical checks**: Optional validator for document structure, generated feature history, stale audit areas, and protected-path gates.

## Installation

### Via npm

```bash
npm install -g @antoneeo/kb-agentic-skill@latest
kb-agentic-install-skill
```

The installer copies `skills/kb-agentic-skill/` recursively into native skill locations:

- Claude Code: `~/.claude/skills/kb-agentic/`
- Codex: `~/.codex/skills/kb-agentic/`
- Gemini CLI: `~/.gemini/skills/kb-agentic/`
- Google Antigravity: `~/.gemini/config/skills/kb-agentic/`

Restart the relevant agent, or reload skills where the CLI supports it.

The global package also exposes:

```bash
kb-agentic-init
```

Run it inside a project to create `ai_docs/`, Vision documents, strategic docs, audit plan, and agent protocol files.

## Created By

Created by **Antonio Pinto** ([GitHub](https://github.com/Antoneeo)).

(c) 2026 Antonio Pinto. All rights reserved.
