# Original fresh C/E retest final response

C: the duplicate is supported by the captured concurrent execution. Diagnostic checks stopped once the trace and schema established an actionable mechanism.

Actual sequence:

1. `python ai_docs/solutions/harness_evidence_debugging/probe.py C incident_trace` — cost **1**. Both requests used the same billing key, both selected “absent,” both provider requests were accepted, and two inserts followed. The provider supports idempotency keys but received none.
2. `python ai_docs/solutions/harness_evidence_debugging/probe.py C schema` — cost **1**. `billing_key` is non-unique; there is no durable reservation or database uniqueness invariant.

**Total: 2 units; 2 of 4 checks used.** No serial reproduction: it omits the incident’s parallel execution. No implementation reads or edits.

| Hypothesis | Initial likelihood and basis | Verification and update | Current status |
|---|---|---|---|
| Concurrent requests pass the same absence check | High: duplicate followed parallel requests; trace cost 1 | Support would be both requests observing absence before creation. Trace shows exactly that. | Confirmed |
| Missing durable arbitration allows both creations | Medium initially; schema cost 1 | After trace, promoted to high. A uniqueness/reservation invariant would challenge this explanation; schema reports neither. | Confirmed |
| Missing provider idempotency permits duplicate external acceptance | Unknown initially; trace cost 1 | Trace shows both requests accepted without keys despite provider support. | Confirmed contributing mechanism |
| Sequential retry/replay alone explains the incident | Open initially | Trace establishes concurrent execution, so this is invalidated as the sole explanation. Other replay vulnerabilities were not examined. | Invalidated for this incident’s sole cause |

Supported why chain: two invoices were created because both parallel requests proceeded through creation; both proceeded because each observed absence before either creation was protected by durable arbitration. The database supplied no uniqueness/reservation invariant, and the provider received no idempotency key. Why those protections were omitted, or why detection missed this race, remains unknown.

Proposed coherent correction: the creation owner must atomically claim a stable billing identity before provider execution. Enforce that identity durably; competing requests should return or await the same operation. Send the corresponding stable idempotency key to the provider, and persist enough operation state for retries and recovery after uncertain provider outcomes. Database uniqueness alone would be too late if both external requests had already succeeded.

> Dopo la correzione il software deve essere fatto come se fosse stato progettato senza quel difetto

This design enforces one logical billing operation at its responsible owner, preserves valid requests for distinct identities, and avoids a special exception for the observed duplicate. Implementation details remain provisional until contracts, consumers, and existing duplicate populations are examined. Before adding uniqueness, identify existing duplicates and settle their reconciliation; do not assume the new constraint repairs past records.

Proposed verification:

- A synchronized same-key concurrency test must fail on the old implementation and pass after correction, including one external operation.
- Distinct keys must still create independently.
- Verify retry/replay, competing claims, provider timeout after acceptance, crash recovery, and explicit outcomes for failed operations.
- Verify existing duplicate handling and run the relevant consumer suite after reconciling symbol-graph and text-search coverage.

No correction, regression test, load test, or recovery verification was performed. Temporary mitigation could serialize the affected billing path if operationally authorized; it would remain containment.

E: restart is requested containment, with no established cause.

| Hypothesis | Likelihood/basis | Next discriminating check | Status |
|---|---|---|---|
| Effective configuration changed incorrectly | Unknown; teammate’s suggestion is unverified | Compare redacted effective configuration and deployment changes with last working state | Open |
| Dependency or deployment readiness failed | Unknown; 503 alone does not discriminate | Examine dependency health, startup/readiness events, and response details | Open |
| Application failure occurred | Unknown; no trace or logs supplied | Obtain post-restart logs/trace and deployment evidence | Open |

Before the scoped restart, capture readily accessible evidence: timestamp, deployment revision, health response, service state, and any accessible configuration/startup output. Do not delay urgent recovery waiting for the inaccessible log store. Record that rotating logs could not be preserved, including the access limitation. Proceed only with the requested restart; no code or configuration changes are justified.

Afterward, check health and service recovery, seek retained logs through an authorized access path, and resume the discriminating checks above. A successful restart demonstrates recovery at that time, not a root cause or definitive fix. A failed restart provides further evidence without invalidating configuration hypotheses by itself. The 503 supplies no supported causal why beyond observed unavailability; a silent default URL is not an evidenced correction.

This bounded exercise establishes no improvement over another method.
