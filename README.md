# Agentic SDLC Skill for Claude Code, Gemini CLI & Codex

`agentic-sdlc` is a Documentation-First SDLC protocol for AI coding agents. It supports Claude Code, Codex, Gemini CLI, Cursor/Windsurf-style project instructions, and optional devPNT governance.

## Key Features

- **Risk-proportional workflow**: L1/L2/L3/Spike triage avoids heavyweight process for trivial work.
- **Vision-guided governance**: Standalone projects use `ai_docs/vision/`; Hybrid projects use devPNT `M-VISION` as the milestone north star.
- **Standalone complete**: works fully with local `ai_docs/` without requiring devPNT.
- **devPNT symbiosis**: when devPNT is available, Master Plan, Action Plan, M-VISION, and governed artifacts become the authoritative planning layer.
- **Installed support files**: Claude, Codex, and Gemini receive the full skill folder, including `templates.md`, `ENFORCEMENT.md`, and `scripts/sdlc_check.py`.
- **Mechanical checks**: optional validator for document structure, generated feature history, stale audit areas, and protected-path gates.

## Installation

### Via npm

```bash
npm install -g @antoneeo/agentic-sdlc-skill@latest
agentic-sdlc-install-skill
```

The installer copies `skills/agentic-sdlc-skill/` recursively into native skill locations:

- Claude Code: `~/.claude/skills/agentic-sdlc/`
- Codex: `~/.codex/skills/agentic-sdlc/`
- Gemini CLI: `~/.gemini/skills/agentic-sdlc/`

Restart the relevant agent, or reload skills where the CLI supports it.

The global package also exposes:

```bash
agentic-sdlc-init
```

Run it inside a project to create `ai_docs/`, Vision documents, strategic docs, audit plan, and agent protocol files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`).

## Runtime Shape

The actual runtime skill is the folder:

```text
skills/agentic-sdlc-skill/
├── SKILL.md
├── templates.md
├── ENFORCEMENT.md
└── scripts/
    └── sdlc_check.py
```

`SKILL.md` is the entrypoint. Supporting files are loaded or executed only when the agent needs them.

## Standalone vs Hybrid

Standalone:

- `ai_docs/` is the source of truth.
- Vision, analysis, audit, handoff, test strategy, and feature history are maintained locally.

Hybrid/devPNT:

- devPNT governs `M-VISION`, Master Plan, Action Plan, and versioned artifacts.
- `ai_docs/` remains useful as readable context, fallback, handoff, or shadow copy.
- Divergence between user request, local Vision, and devPNT `M-VISION` must be surfaced before implementation.

## Gemini Extension Alternative

You can still install this folder as a Gemini extension:

```bash
gemini extensions install .
```

For native Gemini Agent Skills, the npm installer now copies the skill folder into `~/.gemini/skills/agentic-sdlc/`.

## Created By

Created by **Antonio Pinto** ([GitHub](https://github.com/Antoneeo)).

(c) 2026 Antonio Pinto. All rights reserved.
