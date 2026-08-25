# Marketing Agentic SDLC Skill

Evidence-First marketing planning protocol for AI coding agents (Claude Code, Gemini CLI, Google Antigravity, Codex). The sibling of [`@antoneeo/agentic-sdlc-skill`](https://www.npmjs.com/package/@antoneeo/agentic-sdlc-skill), transplanted from software engineering to marketing strategy.

## What it does

Turns an AI agent into a disciplined marketing strategist that produces a professional, professionally-recognized marketing plan (SOSTAC structure) with three engineered guarantees:

1. **Evidence ledger** — every market number is classified FACT / BENCHMARK / ASSUMPTION and carries an `[EV-nn]` reference to its source. No invented numbers.
2. **Mechanical validator** (`mkt_check.py` + `sdlc_core.py` — the entry point plus the family's shared spine; copy both, or neither) — budget sums (±1%), funnel math recomputed cell by cell (±5%) and the objective→tactic→KPI chain are checked mechanically, not rhetorically: `check`, `validate`, `ledger`, `budget`, `funnel`, `trace`, `index`, plus the spine's `stale`/`mark`/`gate`/`plan`/`orient`/`migrate`.
3. **Adversarial CMO review** — an independent, fresh-context reviewer attacks the strategy before the user sees it (generic-positioning swap test, untraced claims, orphan tactics).

The agent asks the user only for facts the user uniquely owns (product, price, budget, capacity); everything else — market sizing, competitor analysis, channel benchmarks — is derived from real web research.

## Install

```bash
npm i -g @antoneeo/mkt-agentic-sdlc-skill
```

That's it — the skill is copied into every detected AI client automatically
(the package's `postinstall` runs the installer). Restart the agent to load it.

**If your npm blocks install scripts** (`--ignore-scripts`, some CI/pnpm setups),
run the installer manually:

```bash
npx mkt-sdlc-install-skill
```

> The `mkt-sdlc-install-skill` command is only on your PATH after a **global**
> (`-g`) install. After a local `npm i`, invoke it via `npx` as above.

Initialize a project:

```bash
cd my-business-project
npx mkt-sdlc-init        # creates mkt_docs/ + protocol pointers
```

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

## Engagement levels (Rule Zero)

| Level | Scope | Process |
|---|---|---|
| E1 Quick | single question / asset feedback | direct answer, sourced numbers |
| E2 Campaign | one campaign or channel plan | mini-brief + targeted research + campaign doc |
| E3 Full Plan | complete marketing plan | full SOSTAC workflow, 9 phases, all gates |
| Research Spike | time-boxed market question | `mkt_docs/spikes/RESEARCH_[topic].md` |

## Several people, one project

The workstream registry (`audit/handoff.md`) is **generated** from one file per open workstream, so two people opening or closing two workstreams on two branches edit two different files and their merge is clean. Row-per-workstream alone was not enough — a file-global `Date:` header defeats row-level ownership — so the header is derived from the sources and no writer touches it. The generated view can still conflict; that conflict is resolved by re-running `index`, never by hand, and `validate` refuses CLEAN until the file matches its sources. The append-only review log gets `merge=union` (a built-in driver, no per-clone configuration). It all works with no VCS at all: it is files and a generator.

## Modes

- **Standalone** — everything on the filesystem under `mkt_docs/`.
- **Hybrid with devPNT** — plans and strategy artifacts governed as versioned devPNT documents (MKT-VISION, ICP/Personas, Threat Map, Strategy, Tactical Plan, Measurement Plan), with proposal/approval workflow and independent review gates.

## The family: three lenses, one spine

| Package | Faithful to | Unit of work |
|---|---|---|
| [`@antoneeo/agentic-sdlc-skill`](https://www.npmjs.com/package/@antoneeo/agentic-sdlc-skill) | this repository's code | feature |
| [`@antoneeo/kb-agentic-skill`](https://www.npmjs.com/package/@antoneeo/kb-agentic-skill) | the documents you supply | topic |
| `@antoneeo/mkt-agentic-sdlc-skill` (this one) | market evidence | engagement |

Triage, the Vision Gate, the review gates, the guide router, question discipline and the validator spine are byte-identical across the three; only the fidelity discipline and the vocabulary change. When two live in the same project, `routing.md` decides which lens owns a given piece of work — with the market-facing override: anything whose purpose is to persuade the market is this lens's, whatever its source.

## License

MIT — Antonio Pinto
