# Seeded Defects — verification list (node A8)

Injected into a COPY of the completed fixture after the clean run. Each must
be caught by the named guard. A miss = calibration finding.

| # | Defect | Injection | Must be caught by | Expected |
|---|---|---|---|---|
| D1 | Budget sum broken | change one Budget Allocation row so sum ≠ Total budget | `mkt_check.py budget` | ERROR |
| D2 | Funnel math broken | alter Customers cell so Leads×Close% no longer holds | `mkt_check.py funnel` | ERROR |
| D3 | Orphan tactic | point one Channel Plan row at nonexistent O9 | `mkt_check.py trace` | ERROR |
| D4 | Ghost evidence ref | add `[EV-99]` to STRATEGY.md | `mkt_check.py ledger` | ERROR |
| D5 | Unsourced benchmark | strip URL from one BENCHMARK ledger row | `mkt_check.py ledger` | ERROR |
| D6 | KPI row removed | delete one objective's row from MEASUREMENT_PLAN KPI table | `mkt_check.py trace` | ERROR |
| D7 | Generic positioning | replace positioning statement with "qualità e passione artigianale per chi ama il caffè" | CMO review R1 (swap test) | BLOCK |
| D8 | Laundered assumption | rewrite an ASSUMPTION-based sentence in MARKETING_PLAN as certainty, no [EV] | CMO review R2/R3 | BLOCK |

Procedure: inject D1-D6 → run `mkt_check.py check` → all six ERROR present →
revert. Inject D7-D8 → run CMO review on the doctored plan → both BLOCK →
revert. Log outcomes in EVAL_LOG.md.
