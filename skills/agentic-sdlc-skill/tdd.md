# TDD Discipline

Applies to L2/L3 implementation work. L1, doc-only changes, and Spikes are
exempt (a Spike records its outcome note only, per `SPIKE_[topic].md`).

## The loop

RED, GREEN, REFACTOR, in that order, every time.

- **RED**: write ONE failing test first, run it, and watch it fail. **MUST:
  no implementation code before the failing test exists; why: a test written
  after the code passes vacuously and proves nothing** — it cannot
  distinguish a correct implementation from a broken one, because it was
  shaped to match whatever the code already does.
- **GREEN**: write the minimum code needed to make that test pass. Resist
  adding behavior the test does not require yet — that belongs to the next
  loop.
- **REFACTOR**: clean up implementation and test code while the suite stays
  green. Re-run the tests after every refactor step, not just at the end.

## Increment rule

One behavior per loop. If you notice the failing test actually covers two
behaviors, split it before writing implementation code — a test that asserts
two unrelated things fails ambiguously and slows down the next RED step.

## Test shape

Unit tests follow AAA — arrange, act, assert:

- **Arrange**: set up inputs, fixtures, and collaborators.
- **Act**: invoke the one behavior under test.
- **Assert**: check the outcome, and only that outcome.

Keep the three parts visually separable (blank line or comment) so a reader
can tell what is setup, what is the trigger, and what is being checked
without tracing the whole test body. This is the single home of the AAA
guidance — do not restate it elsewhere in the skill.

## When TDD does not apply

Legitimate exemptions: no test harness exists for the target environment,
the change is pure documentation, or the work is a time-boxed Spike.

**MUST record the explicit reason in the ANALYSIS Diary or Action Plan node;
why: an unrecorded exemption is indistinguishable from forgetting** — a
reviewer (or a future you) cannot tell "skipped on purpose, here is why" from
"skipped by accident" unless the reason is written down at the time.

## Anti-patterns

- **Tests-after as the unexplained default**: writing implementation first
  and tests afterward without an entry under "When TDD does not apply" above.
- **Testing implementation details**: asserting on private state or call
  internals instead of observable behavior — the test breaks on refactors
  that change nothing externally.
- **One giant test covering everything**: a single test that exercises
  multiple behaviors is slow to diagnose when it fails and violates the
  Increment rule above.
