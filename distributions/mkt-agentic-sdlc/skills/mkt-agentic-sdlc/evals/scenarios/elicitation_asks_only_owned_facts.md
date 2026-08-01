---
id: elicitation_asks_only_owned_facts
expected: the agent asks the user only for facts the user owns, and does NOT outsource market/competitor analysis to the user
---
## Setup
- mkt_docs/vision/MKT_VISION.md: Marketing Vision. Status DRAFT. Business goal to be discovered.
## Prompt
I run a small artisan soap business and I want a marketing plan to grow online sales. Where do we start?
## Pass criteria
- The agent starts Discovery (Wave 1) with business-fact questions the user uniquely owns: product, price, budget, capacity, current traction, constraints.
- It does NOT ask the user "who are your competitors and how are you positioned against them?", "what is your market size?", or "which channels convert best?" — those are the skill's research job.
- Questions are plain language, no unexplained jargon (ICP, CAC, funnel), max ~4 per round.
- On any figure the user may not have measured, it pre-authorizes "I don't know" rather than pressuring for a number.
