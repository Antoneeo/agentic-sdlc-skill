<!-- devpnt:generated
  date: 2026-07-09T05:29:53
  generator: functional_docs_generator v1.0
  sources: skills/mkt-agentic-sdlc/scripts/mkt_check.py
  model: GoogleGemini/gemini-flash-lite-latest
  summary_hash: bb609e8934adce55
-->

## Entities

| Entity | Python Classes | Key Attributes | Notes |
| :--- | :--- | :--- | :--- |
| Validation Report | Report | status, errors, findings | Represents the persistent state of a marketing document check. |
| Project Root | N/A (Path) | path, root_arg | Used to resolve the base directory for marketing SDLC operations. |
| Ledger | Ledger | budget_id, transaction_data | Tracks financial movements within the marketing funnel. |
| Marketing Funnel | Funnel | stages, conversion_rates | Tracks progression and metrics of marketing assets. |

## Relations

Validation Report --> Project Root
Ledger --> Marketing Funnel
Marketing Funnel --> Validation Report