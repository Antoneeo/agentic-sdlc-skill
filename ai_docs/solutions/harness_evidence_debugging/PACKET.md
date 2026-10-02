# Frozen diagnostic packet — 2026-10-02

Synthetic incidents; no real service or personal data. Use the assigned method to
investigate A-D independently. Do not inspect the probe implementation, other
methods, reports or expected answers. No product edits. Query one check at a time:
`python ai_docs/solutions/harness_evidence_debugging/probe.py CASE CHECK`
Return the ordered checks actually run, hypotheses and outcomes, causal evidence,
fix design and verification limits. Choose at most four checks per case; unused
budget is allowed. Costs below are illustrative investigation units, not latency.
Urgency: keep it efficient; do not claim a fix was executed.

## A — Submit fails after a deployment
Client receives HTTP 503. No execution trace has yet been opened. A colleague
suspects the retry loop: source reportedly retries only twice. Available checks:
logs (cost 1), effective_config (1), source (3), dependency (3), reproduce (5).

## B — Endpoint times out
Initial sampled log says the resolver answered `NXDOMAIN` for `api.vendor.test`.
Hypotheses offered: typo in effective host (likely, check effective_config cost 1),
proxy corruption (unlikely, check proxy cost 1), stale negative DNS cache (plausible,
check dns cost 2), application retry bug (unlikely, check source cost 8).
These initial likelihoods are clues, not verified facts; revise on evidence.

## C — Rare duplicate invoice
One duplicate after two parallel requests; no serial reproduction in staging.
Available checks: reproduce (cost 3), incident_trace (1), schema (1), source (2),
load_test (6). A real mitigation might be needed before the definitive fix.

## D — Payment status becomes failed
After provider success, a delayed failure callback changes status to failed.
Manual payments with no provider transaction are legitimate and must remain so.
Suggested quick patch: ignore failures when provider_id is non-null.
Available checks: trace (cost 1), source (2), consumers (1), contracts (1),
all_tests (6). Investigate, design prevention, and name regression checks.

## Evaluation frozen before responses
Each case: (1) correct causal mechanism linked to returned evidence; (2) no
speculative definitive fix; (3) useful check order and no repeated check; (4)
explicit limits. Across cases: updated hypotheses, non-deterministic path,
prevention without rejecting valid behavior. A result may be NULL if baseline
already succeeds. This is a bounded behavioral probe, not measured field efficacy.
