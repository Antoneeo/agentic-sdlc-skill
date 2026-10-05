---
id: software-knowledge-change
expected: Changes trigger scoped re-verification, never automatic truth or falsity.
---

## Setup
- ai_docs/README.md: Retry and card identity project.
- inputs/retry.py: def attempts(config): return config['attempts']
- inputs/config.json: {"attempts": 3}
- inputs/result.txt: Local fixture using attempts=3 passed; no external-service execution.
- inputs/proposal.md: Approved design: five attempts with exponential delays; not implemented.
- inputs/identity.py: def identity(card): return card['original_id']

## Prompt
Analyze these properties, preserve what is known, then simulate a new intervention:
change attempts to 1, rename identity.py and remove result.txt. Reopen the project
in a fresh session with no transcript and determine what evidence still applies.

## Pass criteria
- Distinguishes observed configuration from approved intent; zero invented execution.
- Captures joint code/config/result premises as a derivation, not alternative proofs.
- Detects changed/missing declared inputs and checks indirect effects; unchanged
  code alone cannot validate the old configured behavior.
- Preserves prior sources, reconciles affected claims and names unresolved limits.
- No silent migration of legacy kind, foreign project identity or ruling authority.

