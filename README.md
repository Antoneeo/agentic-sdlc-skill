# Agentic SDLC Skill for Claude Code, Gemini CLI, Google Antigravity & Codex

## Shared project memory

All three lenses include project memory by default; install the lens you need,
not a second skill just for recall. `index` registers guides, decisions and plans
in the docs root's `memory/INDEX.md`, linking originals without copying them.
`recall "onboarding"` finds related metadata across domains; optional
`topics: [onboarding]` links documents by subject. Read the originals for authority,
status and evidence: discovery is not approval or proof of implementation.

Registration happens at `index`/documentation closure, not through a background
watcher. Existing projects acquire the catalog on their next `index`; `recall`
also sees live metadata. The KB lens remains the specialist for ingestion and
taxonomy. Marketing retains its numerical validators. See the skill's `memory.md`.
Vendoring requires all three files: the entry point, `sdlc_core.py`, `knowledge.py`.


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
- **Question discipline**: a real doubt is asked when it emerges, before its answer is written into any document — grouped, with the pros and cons of each option. A choice whose pros clearly win is taken without asking, and the weighing is written next to it; a fact is settled by evidence or asked, never weighed. A question is legal only when the agent searched first, names the search with its result, and names the decision it unblocks — never a stream of "shall I proceed?".
- **Installed support files**: Claude, Codex, Gemini, and Google Antigravity receive the full skill folder, including `templates.md`, `architect.md`, `guides.md`, `vision.md`, `tdd.md`, `debugging.md`, `elicitation.md`, `review.md`, `dispatch.md`, `routing.md`, `hybrid.md`, `ENFORCEMENT.md`, `memory.md`, and the validator's three files, `scripts/sdlc_check.py` + `scripts/sdlc_core.py` + `scripts/knowledge.py` — plus the `LICENSE` and `NOTICE` it ships under.
- **Mechanical checks**: optional validator for document structure, generated feature history, stale audit areas, and protected-path gates — `check`, `validate`, `index`, `stale`, `mark`, `benefit`, `gate`, `plan`, `orient`, `migrate`. `benefit` reports what the review gates have already caught, beside what the doctrine costs to read — it always exits 0 and carries no verdict, because a measurement that can fail a build becomes a target.

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
├── hybrid.md
├── memory.md
├── ENFORCEMENT.md
├── LICENSE
├── NOTICE
└── scripts/
    ├── sdlc_check.py
    ├── sdlc_core.py
    └── knowledge.py
```

`SKILL.md` is the entrypoint. Supporting files are loaded or executed only when the agent needs them.

The validator is **three files**: `sdlc_check.py` selects the lens, `sdlc_core.py` owns structural checks, and `knowledge.py` adds shared memory and KB integrity. Copy all three; core alone is not equivalent.

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

The three lenses share the process spine and knowledge-integrity engine. Install only the one you need; when two live in the same project, `routing.md` decides which lens owns a given piece of work. Marketing additionally runs its numerical checks: code/KB do not certify marketing arithmetic.

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

## License

Apache-2.0 — the full terms are in the `LICENSE` file, the attribution in `NOTICE`. Copyright 2026 Antonio Pinto.

If you redistribute this skill, or a version you modified, keep `LICENSE` and `NOTICE` with it.

Using the skill in your own project carries no obligation: the documents it creates or templates there are yours, and so is a copy of the validator and its tests placed in that project to check its own documents.

Versions up to 1.33.0 were released under the MIT license and remain available under it.

If you use the skill in commercial work, a mention on your product page or website is appreciated. It is a request, not a condition of the license. A ready-made badge:

```markdown
[![Made with agentic-sdlc](https://img.shields.io/badge/made%20with-agentic--sdlc-blue)](https://www.npmjs.com/package/@antoneeo/agentic-sdlc-skill)
```

## Which model to run it on

The skill names **capability tiers**, never providers — a model name in doctrine
rots at the next release. The binding is yours to make, and the rule is one line:

> **A session's floor is the highest floor among the roles it performs itself.**

Authoring a governed artifact — the vision, the analysis, the use cases, the
threat model — is a **deep-tier** role: its output is judgement, and nothing
downstream scores it. So a session that will DESIGN wants your strongest model.
A session that only executes an already-approved plan, or does small maintenance,
can sit a tier lower. The cheapest tier is the wrong choice for the main session
whatever the task, because the failure there is not a wrong answer — it is
**silently not applying the process**: a triage never run, a router verdict
declared without the lookup, a gate nobody noticed. That failure is invisible to
every check in here.

**The reviewer's tier is not automatically yours.** On some clients a subagent
inherits the session's model; on others it takes one from its own definition, so
a strong session can be reviewed by a weak one — and a weak session can buy a
strong review. Set it deliberately; the
`model` column in the review log is where the choice becomes visible.

**Avoid one combination**: authoring below the floor AND reviewing below the floor
on the same unit. One disclosed weakness is a disclosed weakness; two is an
artifact nobody competent ever read. Where your client offers nothing better, the
review still runs and both facts are recorded — a disclosed worst case beats
skipping the review.
