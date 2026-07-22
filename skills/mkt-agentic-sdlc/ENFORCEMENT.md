# Mechanical Enforcement (optional)

The prompt is not enforcement. Where the project needs repeatable guarantees,
wire the validator into the workflow. Everything here is optional: the skill
must stay usable without Python or hooks, declaring what it cannot verify.

## 1. Pre-delivery gate (the one that matters)

Before presenting any E2/E3 deliverable as finished:

```bash
python <skill_dir>/scripts/mkt_check.py check --root <project_root>
```

`check` runs `validate + ledger + budget + funnel + trace`. Errors block the
delivery; warnings ship only with explicit user acknowledgment. This is the
marketing twin of "tests must pass before DONE".

## 2. CI

For a marketing repo kept under version control:

```yaml
# e.g. GitHub Actions step
- run: python skills/mkt-agentic-sdlc/scripts/mkt_check.py validate --strict --root .
- run: python skills/mkt-agentic-sdlc/scripts/mkt_check.py ledger --root .
```

Use `--strict` only in CI: locally, warnings are guidance; in CI they are
drift.

## 3. Git hook (pre-commit)

```bash
#!/bin/sh
python skills/mkt-agentic-sdlc/scripts/mkt_check.py check --root . || {
  echo "mkt_check failed — fix the plan before committing."; exit 1; }
```

## 4. What the validator cannot check (honesty list)

- Whether a BENCHMARK's URL actually supports the claimed number (it checks
  presence, not truth) — that is the review's R2/R3 territory.
- Whether the positioning passes the swap test (R1) — adversarial review only.
- Whether kill/scale thresholds are sensible — review, with ledger evidence.
- Whether the deliverable language matches the target market — Discovery
  record + review.

Declare these residuals when reporting a CLEAN check: mechanical CLEAN plus
review PASS is the full gate, neither alone.

## 5. Skill self-test (skill development only)

Two deterministic batteries — the release gate. Run both:

```bash
python -m unittest discover -s skills/mkt-agentic-sdlc/scripts -p "test_*.py"
```

- `test_mkt_check.py` — the validator itself; gate for changes to
  `mkt_check.py` or to the parseable template formats in `templates.md` (the
  two must move together: a template format change without a validator change
  is drift).
- `test_skill_invariants.py` — the doctrine invariants: asserts the
  load-bearing rules are still present in `SKILL.md` and the support files
  (the three guarantees, the review red-flags R1/R11b/R15, the elicitation
  rules, the research URL rule, the parseable template tokens, every support
  file wired). Fails when a rule is deleted or weakened — a real regression,
  never flakiness.

## 6. Behavioral eval layer (opt-in, non-gating)

```bash
python skills/mkt-agentic-sdlc/evals/run_behavioral.py skills/mkt-agentic-sdlc/evals/scenarios/<scenario>.md
```

Declarative scenarios exercise real agent *adherence* (elicitation asks only
owned facts, no number without a ledger entry, swap-test enforced, low-cost
trap flagged, E2-without-strategy escalates, no guaranteed-success promise).
The driver seeds a throwaway fixture, prints the prompt + pass criteria, makes
NO model call, and never gates — LLM nondeterminism is why the deterministic
gate stays §5. See `evals/scenarios/README.md`.
