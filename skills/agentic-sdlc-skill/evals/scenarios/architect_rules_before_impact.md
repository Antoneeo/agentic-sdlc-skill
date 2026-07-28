---
id: architect_rules_before_impact
expected: on an L3 feature the agent states required capabilities and rules EXISTS/INADEQUATE/MISSING against the platform BEFORE listing files to change
---
## Setup
- src/notify.py: class Notifier:\n    """Owns async notification. send(channel, payload) -> delivery id."""\n    def send(self, channel, payload): ...
- src/orders.py: def place_order(item): ...  # order intake, no persistence yet
- ai_docs/vision/project_vision.md: # Project Vision\nStatus: APPROVED (by owner)\n## North Star\nOrder handling a shop can trust.
- ai_docs/strategic/architecture.md: ---\ndescription: Stack and component map.\nstatus: CURRENT\n---\n# Project Architecture\n## Component Map\nCoverage: the areas audit/audit_plan.md marks ANALYZED - currently src/.\n| Component | Capability it owns | Contract | Where |\n|---|---|---|---|\n| Notifier | notify a third party asynchronously | send(channel, payload) -> delivery id | `src/notify.py#Notifier` |
- ai_docs/audit/audit_plan.md: # Audit Plan\n| Path | Status | Reference | Notes |\n|---|---|---|---|\n| src/ | ANALYZED | 2026-07-28T00:00:00Z | |
## Prompt
Add order confirmation: when an order is placed, persist it and notify the customer. This is an L3 feature; produce the ANALYSIS first.
## Pass criteria
- BEFORE any file list, the ANALYSIS carries a `## Capability Ledger` stating capabilities as verbs over domain nouns (e.g. "persist an order", "notify the customer") -- no file names in the capability column.
- "notify the customer" is ruled **EXISTS** citing `src/notify.py#Notifier` (read from the Component Map, verified in code) -- the agent does NOT design a second notifier (the inlining anti-pattern).
- "persist an order" is ruled **MISSING** with the searches named (terms/tool/areas) -- src/ is ANALYZED and owns no persistence.
- The MISSING capability is designed as a component with a contract stated WITHOUT naming the confirmation feature (e.g. "store and retrieve orders by id"), which the feature then consumes.
- The `## Impact` file list is derived from the ledger, not drafted before it.
