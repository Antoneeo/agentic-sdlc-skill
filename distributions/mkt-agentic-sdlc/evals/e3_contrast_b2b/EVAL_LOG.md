# EVAL LOG — e3_contrast_b2b (Àncora Compliance)

Run date: 2026-07-09. Executor: Claude following skill files only.
Client: subagent playing Elena Ferraro (B2B SaaS compliance CEO).
Purpose: contrast eval (M2) — a business UNLIKE the M1 coffee case, to catch
what one synthetic run overfit. Focused run (not a full 190-fetch replay):
Discovery + 2 research sweeps + the DIFFERING decision points + the
vision-divergence injection.

## Contrast axes vs M1 (coffee)

| Axis | M1 coffee | M2 contrast |
|---|---|---|
| Model | B2C e-commerce | B2B SaaS |
| Motion | product-led / self-serve | sales-led (demo->POC->contract, 3-5 mo) |
| Buyer | consumer personas (JTBD) | firmographic ICP + buying committee (CISO/DPO/CFO) |
| Funnel | AARRR / click->purchase | lead funnel, multi-stage, closed-won lag |
| Budget | 1-1.5k/mo | 4-6k/mo |
| Special test | — | deliberate vision-divergence injection |

## Findings

| # | Phase | What happened | Class | Fix |
|---|---|---|---|---|
| 1 | Strategy gate | **Vision-divergence caught & held.** Client proposed a self-serve €49/mo tier (contradicts written non-goal [EV-13]). Skill did NOT absorb it: stopped, named it a vision change, argued on client's own terms, offered in-vision alternative. Client dropped it definitively, reaffirmed the non-goal. | SUCCESS | — (success signal 3 proven) |
| 2 | Tactics | **Funnel model is e-commerce-baked.** Columns Customers/CAC assume immediate purchase; B2B sales-led needs relabel (funnel output = qualified demos, not closed customers), a separate multi-stage Pipeline table, and an explicit closed-won-lag note. Handled ad-hoc; validator passed only via semantic relabel it cannot see. | TEMPLATE/DOCTRINE-GAP | fold: B2B/sales-led funnel guidance in frameworks.md + templates.md |
| 3 | Situation | ICP is firmographic + committee roles, not consumer JTBD. Skill accommodated it, but templates.md persona template is consumer-shaped. | TEMPLATE-GAP (minor) | fold: note the B2B ICP+committee variant in templates.md |
| 4 | Research | DPO-specific channel data NOT FOUND — labeled ASSUMPTION [EV-31], not invented. | SUCCESS | — (honesty held) |
| 5 | Discovery/gates | 2 waves, no persona trigger fired; every gate passed with sharp client refinements (milestone target, 50%-as-milestone-to-80%, genuine-reviews-only). Elicitation stayed in-rules. | SUCCESS | — |

## Verdict

The skill held on a business unlike the first. The headline result is Finding 1:
the Vision Alignment / amendment discipline works — the divergence the coffee
case never triggered was caught, refused, and resolved without a silent scope
absorption. Finding 2 is the real calibration payload: the funnel apparatus is
e-commerce-shaped and needs an explicit sales-led variant so agents don't force
closed customers into a monthly click-funnel. Validator ran CLEAN on the B2B
plan (budget/funnel/trace) once the funnel output was relabeled to demos.

## Not exercised (focused run)

- Full CMO adversarial review loop on the B2B strategy (M1 exercised it fully;
  here a self-review pass was used, declared).
- Full packaging (MARKETING_PLAN/ONE_PAGER/PDF) — M1 covered it.
- Deep-research skill engine (parallel subagents again).
