# Original baseline final response

Read-only investigation completed. No fixes or regression tests were executed. Total diagnostic cost: **21 units**, across **13 checks**.

**A — Submit fails after deployment**

Ordered checks: `reproduce` (5) → `logs` (1) → `effective_config` (1). **Total: 7.**

The deterministic reproduction returned 503 before any outbound call; supplying the configured base URL succeeded. Logs identified an absent upstream base URL with `outbound_calls=0`. Effective configuration showed that the worker expects `UPSTREAM_BASE_URL`, while the deployment manifest renamed it to `UPSTREAM_URL`.

**Mechanism:** the deployment supplies the wrong configuration key, so request initialization fails before the outbound retry loop can execute. The colleague’s retry-count hypothesis does not explain this incident.

Proposed fix: restore the deployment key expected by the worker, then validate required configuration at startup so an invalid deployment fails visibly before serving requests.

Regression checks: reproduce the missing-key failure against the current deployment; verify corrected configuration permits submission; verify startup validation catches a missing required URL. Run the relevant deployment and submission checks afterward.

Limits: configuration recovery succeeded in the probe, but no deployment edit was performed. Source, dependency checks, and caller enumeration were not run; the evidence does not assess unrelated retry behavior.

**B — Endpoint times out**

Ordered checks: `effective_config` (1) → `dns` (2). **Total: 3.**

The effective host matched the provider’s documented host, weakening the initially likely typo hypothesis. DNS evidence showed a stale negative answer in the local resolver, an address from authoritative lookup, and successful resolution of the same host when bypassing the local resolver.

**Mechanism:** the local resolver’s stale negative cache returns `NXDOMAIN` for a host that authoritative DNS resolves. The controlled bypass isolates the resolver path as the cause of the observed name-resolution failure.

Proposed fix: invalidate the affected stale cache entry and investigate why negative answers outlive their validity. Change resolver configuration or implementation only after identifying that cause.

Regression checks: exercise a previously negative name that becomes resolvable; verify recovery after the permitted negative-cache lifetime and after invalidation. Confirm the application endpoint succeeds through its normal resolver path.

Limits: no dedicated timeout reproduction check was available. Successful DNS resolution does not prove complete endpoint recovery. Proxy and application retry behavior were not examined; they are unnecessary to explain the returned DNS evidence but remain untested.

**C — Rare duplicate invoice**

Ordered checks: `reproduce` (3) → `incident_trace` (1) → `schema` (1) → `source` (2). **Total: 7.**

One hundred serial attempts produced no duplicate and did not reproduce the incident’s concurrency. The incident trace instead showed two requests with the same billing key both observing absence, both making accepted provider requests without idempotency keys, and then inserting two invoices. The schema has neither uniqueness on `billing_key` nor a durable reservation. Source confirmed the sequence: query invoice → charge provider → insert invoice.

**Mechanism:** concurrent requests pass the same non-atomic absence check and each performs an unprotected provider side effect before inserting, while the database permits both invoices.

Proposed mitigation: temporarily serialize or pause invoice creation for the affected scope using coordination that covers all workers; an in-process lock alone would not establish that protection.

Proposed definitive fix: atomically acquire a durable, uniquely keyed reservation before contacting the provider; send a stable provider idempotency key for the same logical billing operation; make retries and crash recovery reuse that reservation and key. A uniqueness constraint added only after charging would still permit duplicate provider side effects. Existing duplicate records need explicit reconciliation before introducing uniqueness.

Regression checks: use a barrier to make two requests reach the absence check together and confirm the old implementation duplicates. Verify the proposed design produces one logical invoice and one provider operation. Cover multiple workers, retries, crashes after provider acceptance but before local completion, and distinct billing keys.

Limits: the concurrent defect was not reproduced in this investigation. Incident, schema, and source evidence support the mechanism, but the baseline’s deterministic-reproduction requirement remains unmet. Neither load testing nor mitigation effectiveness was verified; the fix remains a design proposal.

**D — Payment status becomes failed**

Ordered checks: `trace` (1) → `source` (2) → `consumers` (1) → `contracts` (1). **Total: 5.**

The trace showed success version 8 committed before delayed failure version 7 overwrote it. Source showed callbacks writing status without ordering checks. Returned consumers were provider callbacks, manual reconciliation, admin refunds, and a shared status writer. Contracts establish that versions order events within the same provider transaction; manual payments may lack `provider_id`; refunds after success are valid; a version-9 failure for another pending transaction is valid; duplicate events must be no-ops.

**Mechanism:** callback writes do not enforce transaction-scoped event ordering, allowing an older failure to overwrite a newer success.

Proposed fix: identify the provider transaction and event, reject duplicates, and atomically enforce ordering within that transaction before applying permitted transitions. Keep manual operations supported without requiring a provider identifier, and preserve valid refund behavior. Reject the suggested blanket “ignore failures when `provider_id` is non-null” patch: it would suppress legitimate failures and does not express ordering.

Regression checks: success v8 followed by failure v7 must retain success; reverse arrival must converge correctly; duplicate events must be no-ops; legitimate failure v9 for another pending transaction must apply; manual payments without provider IDs and refunds after success must remain valid. Include concurrent callbacks to verify the ordering check and write are atomic.

Limits: no fix, deterministic replay, or suite run occurred. The consumers check supplied a list without coverage metadata, so exhaustive enumeration cannot be certified. Version persistence, transaction association, and the complete allowed-transition model still require inspection before implementation.
