# Marketing Agentic SDLC Skill

Evidence-First marketing planning protocol for AI coding agents (Claude Code, Gemini CLI, Google Antigravity, Codex). The sibling of [`@antoneeo/agentic-sdlc-skill`](https://www.npmjs.com/package/@antoneeo/agentic-sdlc-skill), transplanted from software engineering to marketing strategy.

## What it does

Turns an AI agent into a disciplined marketing strategist that produces a professional, professionally-recognized marketing plan (SOSTAC structure) with three engineered guarantees:

1. **Evidence ledger** — every market number is classified FACT / BENCHMARK / ASSUMPTION and carries an `[EV-nn]` reference to its source. No invented numbers.
2. **Mechanical validator** (`mkt_check.py`) — budget sums, funnel math and the objective→tactic→KPI chain are checked mechanically, not rhetorically.
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

## Engagement levels (Rule Zero)

| Level | Scope | Process |
|---|---|---|
| E1 Quick | single question / asset feedback | direct answer, sourced numbers |
| E2 Campaign | one campaign or channel plan | mini-brief + targeted research + campaign doc |
| E3 Full Plan | complete marketing plan | full SOSTAC workflow, 9 phases, all gates |
| Research Spike | time-boxed market question | `mkt_docs/spikes/RESEARCH_[topic].md` |

## Modes

- **Standalone** — everything on the filesystem under `mkt_docs/`.
- **Hybrid with devPNT** — plans and strategy artifacts governed as versioned devPNT documents (MKT-VISION, ICP/Personas, Threat Map, Strategy, Tactical Plan, Measurement Plan), with proposal/approval workflow and independent review gates.

## License

MIT — Antonio Pinto
