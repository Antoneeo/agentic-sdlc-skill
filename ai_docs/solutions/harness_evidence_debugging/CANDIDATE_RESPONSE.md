# Original candidate final response — initial version

This was a read-only diagnostic trial. I ran 13 checks, costing 19 illustrative units. No product changes or product regression tests were performed.

### A — Submit returns 503

**Actual checks:** `logs` (1) → `effective_config` (1). **Total: 2.**

Initial hypotheses were missing deployment configuration (unknown likelihood, cheap to verify), dependency failure (unknown, cost 3), and insufficient retries (colleague’s suspicion, source cost 3). Logs were the cheapest useful discriminator: an outbound attempt would keep dependency/retry explanations open; failure before outbound execution would favor configuration.

The log tied request `r7` to “upstream base URL absent,” `outbound_calls=0`, and HTTP 503. This made configuration the leading hypothesis and invalidated insufficient retries as the cause of this request. Effective configuration then confirmed that the worker lacked `UPSTREAM_BASE_URL` because the deployment manifest renamed it to `UPSTREAM_URL`.

**Supported mechanism:** the manifest and worker disagree about the configuration key, so the request fails before making an upstream call. Increasing retries would not address this incident.

**Proposed correction:** restore agreement on the canonical key in the deployment configuration. Validate required configuration during deployment/startup and keep an incorrectly configured worker unready, with an explicit diagnostic.

**Proposed regression checks:** the real deployment manifest supplies the key consumed by the worker; missing configuration rejects readiness; valid configuration permits an outbound submit; dependency failures retain their intended retry behavior.

**Limits:** no deployment history or recovery replay was checked. These observations establish the current mismatch, not the date of the last working deployment or subsequent recovery.

### B — Endpoint times out

**Actual checks:** `effective_config` (1) → `dns` (2). **Total: 3.**

Initial hypotheses: host typo high, stale negative DNS cache medium, proxy corruption low, application retry bug low. The first check tested the strongest inexpensive explanation: a mismatch with the documented host would support a typo.

Effective configuration matched the provider’s documented `api.vendor.test`, invalidating that specific typo hypothesis. I then prioritized DNS over the cheaper proxy check because the sampled `NXDOMAIN` directly concerned resolution and the DNS check could distinguish an invalid name from a local resolver problem.

DNS evidence showed that the local resolver held a stale negative answer, the authoritative lookup returned an address, and controlled bypass of the local resolver resolved the same host.

**Supported mechanism:** local negative caching prevents resolution of a valid hostname. This is confirmed at the DNS layer. Proxy corruption and application retry defects remain untested possible contributors to an end-to-end timeout, but neither is needed to explain the observed resolution failure.

**Proposed correction:** clear or replace the stale local resolver state as containment, then investigate and correct the resolver/cache behavior that retained the obsolete negative response. The packet does not establish which TTL, invalidation, or resolver defect caused retention, so a specific permanent infrastructure change would be premature.

**Proposed regression checks:** negative-to-positive DNS changes become visible within the intended cache lifetime; authoritative and local answers converge; the application recovers after resolution succeeds; legitimate negative caching still works.

**Limits:** successful name resolution was observed, not a successful endpoint request. No proxy or application-source check was run.

### C — Rare duplicate invoice

**Actual checks:** `incident_trace` (1) → `schema` (1) → `source` (2) → `reproduce` (3). **Total: 7.**

Initial hypotheses included a parallel check-then-act race (medium, given two parallel requests), a retry/replay issue (open), and an unrelated serial defect (open). The incident trace was the cheapest direct observation of the rare execution.

The trace showed two requests with the same billing key: both selected “absent,” both provider requests were accepted, and then both inserted invoices. The provider supported idempotency keys but received none. This elevated the race explanation to high likelihood.

Schema evidence confirmed a non-unique billing key and no durable reservation or database uniqueness invariant. Source evidence confirmed the executed pattern: query invoice → charge provider without idempotency key → insert invoice. Together these confirm interacting missing protections, rather than merely a suspicious source pattern.

The final reproduction check produced no duplicate in 100 **serial** attempts and explicitly did not reproduce incident concurrency. It was inconclusive for the confirmed race; it did not invalidate it.

**Supported mechanism:** two concurrent requests both pass the absence check and perform external side effects before either establishes exclusive ownership of the billing operation. Neither storage nor the provider request enforces logical uniqueness.

**Proposed correction:** atomically establish a durable unique billing-operation reservation before the provider call; use a stable provider idempotency key for that operation; let losing/replayed requests reuse or report its existing outcome. Preserve recoverable state across crashes and retries. A uniqueness constraint added only after charging would leave duplicate external side effects possible.

**Temporary containment:** serialize or temporarily hold processing for the same billing key while preserving incident evidence. Reconcile existing duplicates separately; do not assume the new invariant repairs them.

**Proposed regression checks:** barrier-controlled parallel requests for one key produce one logical invoice and one charge; distinct keys remain independent; retry after timeout or crash reuses the operation and idempotency key; reservation conflicts give explicit outcomes; recovery handles partially completed operations.

**Limits:** concurrent controlled reproduction, provider semantics, migration feasibility, and crash recovery were not verified. The serial check consumed budget without faithfully exercising the incident.

### D — Delayed failure overwrites payment success

**Actual checks:** `trace` (1) → `source` (2) → `contracts` (1) → `consumers` (1). **Total: 5.**

Initial hypotheses were stale-event acceptance (high from the symptom), an incorrect provider-identity rule (open), and a legitimate later transition misinterpreted as failure (open).

Trace evidence showed success version 8 committed, followed by delayed failure version 7 committing `failed`. Source confirmed that callbacks overwrite status without an ordering check; manual create/update operations are separate.

Contracts sharpened the invariant: versions order events **within the same provider transaction**; manual payments may lack `provider_id`; refunds after success are valid; failure version 9 for another pending transaction is valid; duplicate events must be no-ops. These facts invalidate the suggested blanket rule “ignore failures when `provider_id` is non-null.”

Consumers identified provider callbacks, manual reconciliation, admin refunds, and a shared status writer.

**Supported mechanism:** the callback path commits an older event after a newer event because it does not atomically enforce transaction-scoped ordering.

**Proposed correction:** enforce event identity, deduplication, and version ordering at the responsible callback persistence boundary. Atomically compare and update the last accepted version for the same provider transaction; stale and duplicate events produce explicit no-op outcomes. Keep manual operations and legitimate refund flows governed by their own contracts. Do not compare versions across transactions.

**Proposed regression checks:** success v8 then failure v7 preserves success; duplicate events are no-ops; simultaneous callbacks cannot defeat ordering; a valid failure for another pending transaction applies; post-success refunds work; manual creation and reconciliation without a provider transaction work; the relevant shared-writer consumer suite passes.

**Limits:** the consumers check provides a named list, not a measured symbol-graph/text-search coverage reconciliation. Exact transaction association, signatures, atomic storage facilities, and valid newer-event transitions need targeted verification before editing.

For each proposed correction, the design criterion is:

> Dopo la correzione il software deve essere fatto come se fosse stato progettato senza quel difetto

The proposals place the invariant with its responsible owner and preserve valid behavior. Implementation would still require meaningful old-fails/new-passes regression evidence and consumer verification; none is claimed here.
