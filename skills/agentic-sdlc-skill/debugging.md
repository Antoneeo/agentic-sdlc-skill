# Systematic Debugging

Applies to bugs classified L2 or L3. Entered either from phase 4
(Development and Testing) when a defect surfaces during implementation, or
from the circuit breaker in `SKILL.md` §4 after repeated no-progress runs.

## Method

Work the steps in order; do not skip ahead to a fix before step 3 names the
mechanism.

1. **Reproduce deterministically.** Find the smallest input or scenario that
   triggers the bug every time. A bug you cannot reliably reproduce cannot be
   verified as fixed.
2. **Isolate.** Narrow the failing case to its minimal form — strip
   unrelated setup, unrelated data, unrelated code paths. Bisect (recent
   commits, code paths, input ranges) when the boundary is unclear.
3. **Root cause — name the mechanism.** State in one sentence why the
   observed behavior happens, tracing the actual execution path. Trace it by
   enumerating the real callers/consumers of each suspect symbol with the best
   symbol-graph tool your toolchain offers — an IDE/LSP call hierarchy or a
   find-usages / call-graph capability — not text search; `grep`
   under-enumerates and hides the very consumer that breaks. **MUST NOT
   patch a symptom without naming the mechanism; why: symptom patches recur
   and stack** — the same underlying defect resurfaces elsewhere, and each
   unexplained patch makes the next investigation harder, not easier.
4. **Fix at the cause**, not at the symptom identified in step 1.
5. **Write a regression test that FAILS on the old code** (verify this
   before applying the fix, or by temporarily reverting it) and passes after.
   A regression test that was never confirmed to fail proves nothing.
6. **Run the relevant suite for collateral.** A root-cause fix can change
   behavior other callers depend on; enumerate those callers with the
   symbol-graph (step 3), not from memory, and check them before closing.

**Capture the model you had to rebuild.** If naming the mechanism (step 3) forced
you to reconstruct the mental model of a complex component that no guide documents —
tracing it across files because it was written down nowhere — that is the
comprehension trigger (`guides.md` §1): it is your duty to write the `source_kind:
code` guide, so the next debugger starts with the map you just paid to build.

**Chronic fragility is a signal, not a task to grind.** If a component breaks
*repeatedly across sessions* and its complexity is no longer under control, stop
treating each break as an isolated bug — that pattern has two duties, not one:
1. **Understand** — write the `source_kind: code` comprehension guide (above) so the
   understanding stops evaporating between sessions.
2. **Escalate the complexity itself** — STOP stacking patches on a component nobody
   fully understands. Flag the fragility as tech debt and propose a dedicated
   **refactor as its own L3** (Vision-gated), instead of a fourth fix. Continuing to
   patch a component you keep breaking is the anti-pattern, not the fix.

## Circuit breaker integration

After 3 consecutive runs without progress: STOP. Do not attempt a 4th
variation of the same guess. Audit your assumptions from step 1 — is the
reproduction actually deterministic, is the isolated case actually minimal,
is the "root cause" from step 3 actually confirmed or just plausible? Then
restart from step 1 with the corrected assumption.

If still stuck after the restart, ask the user for instructions, and hand
over the evidence gathered so far: the minimal reproduction, what was ruled
out, and the current best hypothesis.

## Anti-patterns

- **Shotgun debugging**: changing several things at once hoping one fixes it
  — when it "works," you do not know which change mattered or why.
- **Stacking speculative fixes**: adding a second guess on top of an
  unverified first one instead of confirming or discarding it first.
- **"Fixed but can't say why"**: closing the bug without a step-3 mechanism
  statement. If you cannot name the mechanism, the fix is not confirmed —
  it may just be masking the trigger.
