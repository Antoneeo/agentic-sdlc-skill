---
id: verdict_declared_on_no_match
expected: the agent declares an explicit "no match" router verdict, proving the lookup ran
---
## Setup
- ai_docs/reference/GUIDE_release.md: Guide Release -- how to publish a version; consult before any version bump or tag.
- ai_docs/reference/INDEX.md: Guide router. GUIDE_release.md -- when publishing a version, bumping or tagging.
- ai_docs/README.md: Reading guide. 1. reference/INDEX.md -- the guide router. 2. audit/handoff.md -- where work stopped.
- src/list.py: def page(items, n, size): return items[n * size : n * size + size + 1]
## Prompt
Fix the off-by-one in the pagination offset in src/list.py and add a test.
## Pass criteria
- The agent declares the triage level WITH a router verdict -- e.g. `Level: L2 - router: no match`.
- The verdict is `no match`: GUIDE_release.md does not cover pagination, so consulting it would be a wrong match, and reading it anyway would violate the targeted-match rule (T7).
- The declaration is present even though nothing matched -- this is the whole point: it distinguishes "looked, nothing fitted" from "never looked" (F-016).
- The agent does NOT open GUIDE_release.md.
- No guide is created: this work was not governed by user-provided indications (T6), and a one-line fix is not a high-complexity comprehension signal.
