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
mkt-sdlc-install-skill   # copies the skill into every detected AI client
```

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
