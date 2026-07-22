# Behavioral eval scenarios

Declarative, model-neutral scenarios for the **opt-in, non-gating** behavioral
eval layer. The deterministic release gate is the static battery
(`scripts/test_skill_invariants.py`, run via `unittest discover`); these
scenarios exercise real agent *adherence* (nondeterministic, so it never gates).

## Format

```
---
id: <slug>
expected: <one-line expected behavior>
---
## Setup
- <relpath>: <single-line file content>   # each entry seeds one file in the fixture
## Prompt
<the task prompt to give the agent>
## Pass criteria
- <observable checks the human/agent confirms>
```

## Running

```
python ../run_behavioral.py scenarios/<file>.md
```

The driver seeds a throwaway temp fixture from `## Setup`, prints the prompt +
pass criteria; run the prompt against your agent with the fixture as cwd and
self-assess. No model call, never gates a release.
