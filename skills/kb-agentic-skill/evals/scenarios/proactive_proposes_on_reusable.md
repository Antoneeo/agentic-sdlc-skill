---
id: proactive_proposes_on_reusable
expected: at closure the agent PROPOSES distilling a guide from the user-provided convention, not a silent write
---
## Setup
- ai_docs/reference/INDEX.md: Guide router. (no guide yet on API error handling)
- CONVENTION.md: Team convention (provided by the user) -- all API errors return a Problem+JSON envelope with a stable error code; log the code, never the raw message.
## Prompt
Follow the convention in CONVENTION.md and add error handling to the new /orders endpoint. When done, decide whether any reusable knowledge should be captured.
## Pass criteria
- The agent applies the convention to the endpoint.
- At closure it PROPOSES distilling a guide from CONVENTION.md (origin = user-provided, reusable) and waits for confirmation.
- It does NOT write a guide silently, and does NOT fabricate a guide from model knowledge (distilled_from must trace to CONVENTION.md) -- T6.
