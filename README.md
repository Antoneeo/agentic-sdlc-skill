# Agentic SDLC Skill for Claude Code, Gemini CLI, Google Antigravity & Codex

`agentic-sdlc` is a Documentation-First SDLC protocol for AI coding agents. It supports Claude Code, Codex, Gemini CLI, Google Antigravity 2.0, Cursor/Windsurf-style project instructions, and optional devPNT governance.

## Key Features

- **Risk-proportional workflow**: L1/L2/L3/Spike triage avoids heavyweight process for trivial work, with a symmetric **Write Triggers** table mapping each event to the document it produces (one event, one destination).
- **Vision-guided governance**: Standalone projects use `ai_docs/vision/`; Hybrid projects use devPNT `M-VISION` as the milestone north star. The Vision names its **Actors** — the cast a feature serves, one light line each — so UX is designed for concrete roles, not an implicit "user".
- **Architect pass — capabilities before files**: at L3, before listing what changes, the feature is stated as the *capabilities* it needs and each is ruled against the platform (EXISTS / INADEQUATE / MISSING); what is missing is designed as a component with its own contract, of which the feature is one consumer — never inlined into the feature's code path. A `## Component Map` in `strategic/architecture.md` is the durable inventory the pass reads, so the platform is not re-derived from source every session. On a codebase the methodology arrives in late, the map's silence is treated as **unread, not empty**: it can never ground a MISSING verdict.
- **Execution disciplines**: explicit TDD (RED/GREEN/REFACTOR), systematic debugging, an L3 spec-elicitation round, and a single code-review definition wired into the workflow phases.
- **Operative + comprehension guides + agent-global KB**: distil user-provided indications into source-faithful operative `GUIDE_*.md` (`source_kind: document`), and let the agent autonomously author **code-comprehension guides** (`source_kind: code`) for complex components — a source-faithful mental-model map that survives across sessions, so the next session doesn't re-derive and break the component from partial understanding. Consulted before work; shared cross-project via `~/.agentic-sdlc`.
- **Several people, one project**: the workstream registry (`audit/handoff.md`) is **generated** from one file per open workstream, so two people opening or closing two workstreams on two branches edit two different files and their merge is clean. Row-per-workstream alone was not enough — a file-global `Date:` header defeats row-level ownership — so the header is derived from the sources and no writer touches it. The generated view can still conflict; that conflict is resolved by re-running `index`, never by hand, and `validate` refuses CLEAN until the file matches its sources. The append-only review log gets `merge=union` (a built-in driver, no per-clone configuration). It all works with no VCS at all: it is files and a generator.
- **Opt-in subagent execution**: an approved design projects into a validated executable plan an orchestrator can drive through subagents.
- **Self-activating**: a SessionStart hook emits repo-sourced orientation; a deterministic self-eval battery guards the skill's own doctrine as the release gate.
- **Standalone complete**: works fully with local `ai_docs/` without requiring devPNT.
- **devPNT symbiosis**: when devPNT is available, Master Plan, Action Plan, M-VISION, and governed artifacts become the authoritative planning layer, with independent fresh-context reviews of technical artifacts and diffs.
- **Independent review, twice**: the design is reviewed before it is implemented and the diff before the work is declared done — by somebody other than its author. Three rungs of independence (fresh-context subagent > one-shot run > a declared self-pass, legal only when no higher rung is usable: absent, or permission-gated and declined — a gated rung is asked about, never silently skipped, and the log says which), capped at 3 rounds, one log line per review, and a PASS is invalid on "found nothing" — it must state where each constraint is satisfied.
- **Question discipline**: a question to the user is legal only when the agent searched first and names the search with its result, and names the decision the answer unblocks. Otherwise it proceeds on a declared assumption — same evidence duty, batched, never a stream of "shall I proceed?".
- **Installed support files**: Claude, Codex, Gemini, and Google Antigravity receive the full skill folder, including `templates.md`, `architect.md`, `guides.md`, `vision.md`, `tdd.md`, `debugging.md`, `elicitation.md`, `review.md`, `dispatch.md`, `routing.md`, `ENFORCEMENT.md`, and the validator's two files, `scripts/sdlc_check.py` + `scripts/sdlc_core.py`.
- **Mechanical checks**: optional validator for document structure, generated feature history, stale audit areas, and protected-path gates — `check`, `validate`, `index`, `stale`, `mark`, `gate`, `plan`, `orient`, `migrate`.

## Installation

### Via npm

```bash
npm install -g @antoneeo/agentic-sdlc-skill@latest
```

That is enough — the package's `postinstall` runs the installer. If your npm blocks
install scripts (`--ignore-scripts`, some CI/pnpm setups), run it by hand:

```bash
agentic-sdlc-install-skill
```

> The command is on your PATH only after a **global** (`-g`) install; after a local
> `npm i`, invoke it as `npx agentic-sdlc-install-skill`.

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

It also **wires the SessionStart orientation hook** into `.claude/`, so an agent opening
the project is handed the reading guide, the generated manifest, the guide router and the
last handoff before it does anything — instead of only when it remembers to look. That
wiring used to be a manual step documented in `ENFORCEMENT.md`; being manual, it was
skipped, and a project could run fully governed with an agent that never met the process.

The hook command names a validator, so where that validator lives decides which file gets
it: a repo that vendors it gets a repo-relative command in the shared `.claude/settings.json`
(portable — commit it); otherwise the path is machine-specific and goes to the git-ignored
`.claude/settings.local.json`, and each teammate runs `init` once. Re-running `init` never
duplicates the hook, and a hook whose validator no longer resolves is reported as **broken**
with the correction rather than counted as installed.

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
├── routing.md
├── ENFORCEMENT.md
└── scripts/
    ├── sdlc_check.py
    └── sdlc_core.py
```

`SKILL.md` is the entrypoint. Supporting files are loaded or executed only when the agent needs them.

The validator is **two files**: `sdlc_core.py` is the family's shared spine, `sdlc_check.py` is this lens's entry point. Copy both, or neither — the entry point is useless alone.

Installing or updating the npm package wires the session-orientation hook
machine-wide (user-level Claude Code settings; removal is a standing opt-out
that no update overrides -- ENFORCEMENT.md par.4).

## The family: three lenses, one spine

Same process, three fidelity disciplines — what the agent's assertions must be faithful to:

| Package | Faithful to | Unit of work | Own doctrine |
|---|---|---|---|
| [`@antoneeo/agentic-sdlc-skill`](https://www.npmjs.com/package/@antoneeo/agentic-sdlc-skill) | this repository's code | feature | `architect.md`, `tdd.md`, `debugging.md` |
| [`@antoneeo/kb-agentic-skill`](https://www.npmjs.com/package/@antoneeo/kb-agentic-skill) | the documents you supply | topic | `taxonomy.md`, `distillation.md`, `reconciliation.md` |
| [`@antoneeo/mkt-agentic-sdlc-skill`](https://www.npmjs.com/package/@antoneeo/mkt-agentic-sdlc-skill) | market evidence | engagement | `frameworks.md`, `research.md` |

Triage, the Vision Gate, the review gates, the guide router, question discipline and the validator spine are byte-identical across the three. Install only the one you need; when two live in the same project, `routing.md` decides which lens owns a given piece of work and any of the three validators gives the same verdict on the same tree.

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

MIT (c) 2026 Antonio Pinto.
