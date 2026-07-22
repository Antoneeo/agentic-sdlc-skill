# Framework Selection Guide

A framework is a lens, not a form. Pick per relevance; an empty section is
declared ("Five Forces skipped: single-competitor niche, structure analysis
adds nothing"), never padded. A deliverable stuffed with every framework is a
student essay, not a plan.

## The spine: SOSTAC

The plan's section structure is always SOSTAC (PR Smith) — the skeleton
professionals recognize:

| SOSTAC | Phase(s) | Output |
|---|---|---|
| **S**ituation | 2-4 (Discovery, Research, Situation Analysis) | where we are: market, competitors, customers, own assets |
| **O**bjectives | 5 | where we want to be: SMART + KPI tree |
| **S**trategy | 6 | how we get there at altitude: STP, positioning, messaging |
| **T**actics | 7 | with which instruments: channels, budget, funnel |
| **A**ction | 8 | who does what when: 90-day plan |
| **C**ontrol | 9 | how we know it works: measurement, kill/scale |

## Situation-phase lenses (pick, don't stack)

| Lens | Use when | Skip when |
|---|---|---|
| **SWOT** | always — the synthesis container for research findings | never skipped, but every cell must cite `[EV-nn]` entries; adjectives without evidence are deleted |
| **PESTEL** | regulated markets, macro-exposed sectors (energy, health, finance), international expansion | stable domestic niche — declare the skip |
| **Porter Five Forces** | entering a new market or industry-structure questions (margins, supplier power) | plan for an existing position in a known market |
| **TAM/SAM/SOM** | always for E3 | — (method rules below) |

**Market sizing rules:** bottom-up preferred (number of reachable potential
customers × realistic price point, from ledger entries); top-down (industry
report % slicing) only as a cross-check. A TAM that exists only top-down is a
`WARN` in review. SOM must be defendable from channel capacity, not ambition.

## Customer lenses

- **ICP (Ideal Customer Profile):** firmographic/demographic criteria table —
  who we sell to and, as important, who we do NOT sell to.
- **Personas + JTBD:** at most 2-3 personas, each built from voice-of-customer
  evidence (mined reviews, forums, support threads — see `research.md`). Each
  persona carries: job-to-be-done, buying trigger, top objections, watering
  holes (where they actually are). A persona trait with no VoC evidence is an
  ASSUMPTION and is labeled as one; an invented persona is a review finding.

## Strategy lenses

- **STP:** Segmentation (from research) → Targeting (a CHOICE, with rationale
  and explicit rejections: "segment B rejected because...") → Positioning.
- **Positioning (April Dunford components):** competitive alternatives (what
  the customer does today, including "nothing"), unique attributes, value
  (evidence-backed), best-fit segment, market category. Then the statement:

  > For [segment] who [need], [name] is the [category] that [unique value],
  > unlike [main alternative] which [limitation].

  **Swap test (mandatory):** replace [name] with the top competitor. If the
  statement still holds, the positioning does not exclude and FAILS.
- **Messaging house:** roof = value proposition (one sentence), pillars = 2-4
  messages, foundation = proof points per pillar. A pillar without proof
  points is a slogan; the review flags it.

## Objectives

- **SMART**, each objective `O1`, `O2`, ... with owner-visible target and date.
- **KPI tree:** north-star metric → driver metrics → channel KPIs. Every
  objective maps into the tree; every channel KPI rolls up. The tree lives in
  `MEASUREMENT_PLAN.md`; `mkt_check.py trace` verifies the chain.
- 3-5 objectives maximum. Ten objectives = no objectives.

## Tactics lenses

- **Funnel model:** AARRR (acquisition, activation, retention, referral,
  revenue) for product-led; classic lead funnel (traffic → lead → MQL → SQL →
  customer) for sales-led. Pick per the sales motion captured in Discovery.
  Funnel rows must recompute (`mkt_check.py funnel`).
- **Sales-led / B2B funnel (important — the funnel table is shaped for
  immediate-purchase e-commerce).** In a long-cycle B2B motion the monthly
  funnel output is a **qualified lead / demo**, NOT a closed customer — today's
  lead closes in 3-5 months. So: (a) put ONLY the paid click channels in the
  `Funnel Model` table, and read its `Customers` column as *qualified
  demos/leads* and `CAC` as *cost per qualified demo* — state the relabel
  explicitly; (b) the primary sales-led motions (referral, content, outbound)
  are NOT click funnels — represent their yield in a separate **Pipeline
  build-up table** (per-source qualified leads/month vs the objective target);
  (c) model the multi-stage sales funnel (MQL→SQL→demo→POC→won) and the
  closed-won LAG in that pipeline section, not in the click-funnel table.
  Forcing closed customers into a monthly click-funnel produces absurd CAC.
- **Channel selection matrix:** score candidate channels on ICP presence
  (from VoC watering holes), intent level, benchmark cost `[EV-nn]`, and
  execution capacity (from Wave 3). Choose few: 2-3 core channels beat 8
  half-run ones. A channel chosen against the matrix needs written rationale.
- **Budget heuristics:** 70/20/10 (core / adjacent / experimental) as the
  default split; deviations argued. Industry %-of-revenue norms are
  BENCHMARKS — they enter only with a sourced ledger entry, never from memory.
- **4P/7P:** use as a completeness checklist on the tactical plan (price,
  place and product decisions the plan silently makes), not as a section.

## Control

- Review cadence: weekly channel KPIs, monthly objective review, quarterly
  strategy review.
- **Kill/scale criteria per channel, set BEFORE launch:** "kill if CAC > X
  after spend Y; scale if CAC < Z at volume W" — thresholds justified by
  ledger benchmarks. A plan without kill criteria is a brochure (review BLOCK).
