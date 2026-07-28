---
id: unmapped_never_grounds_missing
expected: in an area the audit plan has not analyzed, the agent searches the code instead of ruling MISSING from the Component Map's silence
---
## Setup
- legacy/billing/rates.py: class RateLimiter:\n    """Owns request throttling. acquire(key) -> bool. The component the trap hides."""\n    def acquire(self, key): ...
- src/api.py: def handle(req): ...  # entry point, no throttling wired
- ai_docs/vision/project_vision.md: # Project Vision\nStatus: APPROVED (by owner)\n## North Star\nAn API that survives abusive clients.
- ai_docs/strategic/architecture.md: ---\ndescription: Stack and component map.\nstatus: CURRENT\n---\n# Project Architecture\n## Component Map\nCoverage: whatever audit/audit_plan.md marks ANALYZED - read it, do not trust a list restated here. Outside them this map is unread, not empty.\n| Component | Capability it owns | Contract | Where |\n|---|---|---|---|\n| API entry | accept a request | handle(req) | `src/api.py#handle` |
- ai_docs/audit/audit_plan.md: # Audit Plan\n| Path | Status | Reference | Notes |\n|---|---|---|---|\n| src/ | ANALYZED | 2026-07-28T00:00:00Z | |\n| legacy/ | PENDING | - | inherited code, never analyzed |
## Prompt
Add rate limiting to the API so abusive clients get throttled. This is an L3 feature; produce the ANALYSIS first.
## Pass criteria
- The agent does NOT rule "throttle requests" MISSING from the Component Map's silence: legacy/ is PENDING, so the map is unread there (the Empty-map MISSING anti-pattern).
- It SEARCHES the unmapped area (find-usages/grep for throttle/rate/limit terms) and finds `legacy/billing/rates.py#RateLimiter`.
- Verdict comes out **EXISTS** (or INADEQUATE with the gap named if it judges the contract insufficient) citing that path#symbol -- never a bare MISSING.
- The discovered component is ADDED to the Component Map as a new row, and the agent marks/notes legacy/billing/ as covered (audit plan progression).
- If the agent rules MISSING anyway and designs a new rate limiter, the scenario FAILS -- that is the duplicate-the-codebase failure this pass exists to prevent.
