# Behavioral eval scenarios

Declarative, model-neutral scenarios for the **opt-in, non-gating** behavioral
eval layer. The deterministic release gate is the static battery
(`scripts/test_skill_invariants.py`, run via `unittest discover`); these
scenarios exercise real agent *adherence* (which is nondeterministic, so it
never gates). See `ENFORCEMENT.md` §5.

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

The driver seeds a throwaway temp fixture from `## Setup`, then prints the
prompt + pass criteria. Run the prompt against your agent with the fixture as
the working directory and self-assess against the criteria. The driver makes no
model call and never gates a release.
