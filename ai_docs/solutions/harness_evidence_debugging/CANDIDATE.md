# Systematic Debugging

Applies to bugs classified L2 or L3, from the start of their analysis, including
defects discovered during implementation. Investigate the observed failure before
proposing a definitive fix. A suspicious source-code pattern is a hypothesis, not
proof that it caused this incident.

## Method

1. **Establish the facts.** State expected versus observed behavior, affected
   environment, timing and last known working state. Read available local incident
   evidence first: relevant logs, stack traces, request/response, effective
   configuration and service state. Preserve evidence before restarts or changes
   erase it; urgent containment may come first, but label it temporary and record
   what evidence could not be preserved. Logs may be partial or misleading: check
   their scope and time window. Do not exhaust every log or wait for nonexistent
   logs when a direct observation is available. Read only what is needed, redact
   secrets/personal data in reports, and keep sensitive raw logs out of project docs.

2. **Maintain the hypotheses.** Keep a small register in the existing L2
   mini-analysis or L3 ANALYSIS/Action Plan, not a new mandatory document:

   | Cause hypothesis | Evidence for/against | Likelihood and basis | Verification cost | Check and result | Current hypothesis status |
   |---|---|---|---|---|---|

   Use high/medium/low or unknown likelihood and rough costs, with reasons; do not
   invent numerical probabilities. Prefer hypotheses that are both more likely
   and cheaper to verify. When those criteria conflict, choose a check with useful
   discrimination between the remaining explanations and justify that choice.
   State what observation would support or invalidate the hypothesis before the
   check. Record each result, update evidence/status and reorder after every check.
   An inconclusive check leaves the hypothesis open; distinguish a check's outcome
   from the hypothesis's accumulated status (open, confirmed, invalidated).
   Do not repeat an invalidated hypothesis unless new evidence reopens it.

3. **Test and trace the mechanism.** Reproduce and isolate the smallest faithful
   failing case when feasible; bisect inputs, paths or changes when informative.
   If the incident is intermittent or inaccessible, use captured traces and
   targeted diagnostic observations instead of declaring investigation impossible.
   Add minimal instrumentation when evidence is insufficient. Prefer read-only
   checks; run state-changing experiments in a controlled environment under the
   existing authorization boundaries. Read source to answer a concrete question
   arising from evidence, then check its predictions against actual execution.
   A static call graph identifies possible consumers, not the executed path.

   Use the **five whys** to deepen supported causal links, not to force five
   answers or a single linear cause. Each unsupported answer becomes a hypothesis
   in the register. Allow interacting causes; distinguish why the failure happened
   from why prevention or detection missed it. Stop when the actionable causal
   mechanism is supported, or state the evidence gap instead of inventing a cause.
   Before a definitive fix, name the mechanism and evidence connecting it to this
   failure; explain which alternatives were invalidated and which remain open.
   Missing logs or a passing unrelated test do not invalidate a hypothesis.

4. **Correct the design with Poka-Yoke.** Fix the responsible code, configuration
   or infrastructure; do not force a code edit for an environmental cause.
   Enforce the invariant where the responsibility belongs: prevent the invalid
   condition, or detect and reject it immediately with an explicit outcome when
   prevention is infeasible. Preserve legitimate behavior; a blanket rejection or
   crash is not universally appropriate. Prefer the smallest coherent correction
   over a case-specific exception, duplicated guard, silent fallback or speculative
   broad refactor. Temporary containment is not a definitive fix.

   Before editing, enumerate affected consumers using the available symbol graph
   and a text coverage probe; reconcile differences and state coverage limits.
   With no graph available, use text/targeted reads and disclose incomplete coverage
   rather than guessing completeness. Apply existing triage/design gates if scope
   expands. Mandatory design verification, preserving this wording verbatim:

   > Dopo la correzione il software deve essere fatto come se fosse stato progettato senza quel difetto

   Explain how the fix satisfies it: the correct owner enforces the invariant,
   the same failure is prevented or detected at origin, no ad hoc exception is
   needed, and valid consumer behavior is preserved. Disclose residual compromises;
   the sentence does not authorize redesign beyond the confirmed defect's scope.

5. **Verify the correction and collateral.** Follow `tdd.md` for implementation:
   confirm a regression test fails for this mechanism on the old implementation
   and passes after the fix. Verify the Poka-Yoke against invalid and valid cases,
   relevant neighboring cases, and concurrency/retry/order where the mechanism
   involves them. Run the relevant consumer suite after the final change.
   If the original incident cannot be replayed, distinguish controlled mechanism
   tests from incident recovery evidence and report remaining uncertainty; do not
   waive available regression tests or claim an unperformed verification.

**Capture the model you had to rebuild.** If tracing the cause reconstructed a
complex component with no CURRENT comprehension guide, write its `source_kind:
code` guide under `guides.md` §1. Keep evidence and invariants, not sensitive logs.

**Chronic fragility is a signal, not a task to grind.** If the component repeatedly
breaks across sessions and complexity is no longer controlled, preserve its model
in that guide and surface the debt. Propose a dedicated Vision-gated L3 refactor
instead of stacking patches; do not silently expand the current fix into it.

## Circuit breaker integration

After three consecutive attempts without new diagnostic information or progress,
STOP varying the same guess. Audit the evidence, register and checks: did a result
actually invalidate the hypothesis, did the test reproduce the relevant conditions,
and was the mechanism confirmed rather than merely plausible? Restart from the
earliest unsupported step. If still stuck after that restart, ask the user for
instructions with observed facts, checks/results, invalidated and open hypotheses,
the evidence gap and any temporary containment. More guesses are not progress.

## Anti-patterns

- Source-first speculation: patching a plausible defect without tying it to the incident.
- Shotgun debugging: changing several things at once without a discriminating check.
- Guess stacking: retaining an unverified fix while adding another.
- Register theater: invented likelihoods, repeated cheap but uninformative checks,
  or check failure presented as hypothesis falsification without adequate coverage.
- Five invented whys: unsupported causal links, or forcing one root on interacting causes.
- Symptom exceptions: suppressing one event or input instead of correcting its invariant.
- "Fixed but can't say why": closure without causal evidence and the mandatory design check.
