# Agentic SDLC Skill for Claude Code, Gemini CLI, Google Antigravity & Codex

`agentic-sdlc` is a Documentation-First SDLC protocol for AI coding agents. It supports Claude Code, Codex, Gemini CLI, Google Antigravity 2.0, Cursor/Windsurf-style project instructions, and optional devPNT governance.

## Key Features

- **Risk-proportional workflow**: L1/L2/L3/Spike triage avoids heavyweight process for trivial work, with a symmetric **Write Triggers** table mapping each event to the document it produces (one event, one destination).
- **Vision-guided governance**: Standalone projects use `ai_docs/vision/`; Hybrid projects use devPNT `M-VISION` as the milestone north star. The Vision names its **Actors** — the cast a feature serves, one light line each — so UX is designed for concrete roles, not an implicit "user".
- **Architect pass — capabilities before files**: at L3, before listing what changes, the feature is stated as the *capabilities* it needs and each is ruled against the platform (EXISTS / INADEQUATE / MISSING); what is missing is designed as a component with its own contract, of which the feature is one consumer — never inlined into the feature's code path. A `## Component Map` in `strategic/architecture.md` is the durable inventory the pass reads, so the platform is not re-derived from source every session. On a codebase the methodology arrives in late, the map's silence is treated as **unread, not empty**: it can never ground a MISSING verdict.
- **Execution disciplines**: explicit TDD (RED/GREEN/REFACTOR), systematic debugging, an L3 spec-elicitation round, and a single code-review definition wired into the workflow phases.
- **Operative + comprehension guides + agent-global KB**: distil user-provided indications into source-faithful operative `GUIDE_*.md` (`source_kind: document`), and let the agent autonomously author **code-comprehension guides** (`source_kind: code`) for complex components — a source-faithful mental-model map that survives across sessions, so the next session doesn't re-derive and break the component from partial understanding. Consulted before work; shared cross-project via `~/.agentic-sdlc`.
- **Opt-in subagent execution**: an approved design projects into a validated executable plan an orchestrator can drive through subagents.
- **Self-activating**: a SessionStart hook emits repo-sourced orientation; a deterministic self-eval battery guards the skill's own doctrine as the release gate.
- **Standalone complete**: works fully with local `ai_docs/` without requiring devPNT.
- **devPNT symbiosis**: when devPNT is available, Master Plan, Action Plan, M-VISION, and governed artifacts become the authoritative planning layer, with independent fresh-context reviews of technical artifacts and diffs.
- **Installed support files**: Claude, Codex, Gemini, and Google Antigravity receive the full skill folder, including `templates.md`, `architect.md`, `guides.md`, `vision.md`, `tdd.md`, `debugging.md`, `elicitation.md`, `review.md`, `dispatch.md`, `ENFORCEMENT.md`, and `scripts/sdlc_check.py`.
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
- Google Antigravity: `~/.gemini/config/skills/agentic-sdlc/` (detected distinctly from Gemini CLI; override the home with `ANTIGRAVITY_HOME`)

Restart the relevant agent, or reload skills where the CLI supports it.

The global package also exposes:

```bash
agentic-sdlc-init
```

Run it inside a project to create `ai_docs/`, Vision documents, strategic docs, audit plan, and agent protocol files (`AGENTS.md` — also the Antigravity CLI surface, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`).

## Runtime Shape

The actual runtime skill is the folder:

```text
skills/agentic-sdlc-skill/
├── SKILL.md
├── templates.md
├── architect.md
├── guides.md
├── vision.md
├── tdd.md
├── debugging.md
├── elicitation.md
├── review.md
├── dispatch.md
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
