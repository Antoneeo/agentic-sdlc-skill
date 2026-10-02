"""Read-only synthetic diagnostic queries. No state or network changes."""
import json
import sys

DATA = {
    "A": {
        "logs": [1, "request r7: configuration error upstream base URL absent; outbound_calls=0; 503"],
        "effective_config": [1, "worker: UPSTREAM_BASE_URL missing; deployment manifest renamed it to UPSTREAM_URL"],
        "source": [3, "submit obtains UPSTREAM_BASE_URL at request time; absent -> 503; retry handles transient outbound failures, attempts=2"],
        "dependency": [3, "provider healthy; independently reachable from this environment"],
        "reproduce": [5, "deployment env + request r7 -> 503 before any outbound call; configured base URL -> success"],
    },
    "B": {
        "effective_config": [1, "effective host api.vendor.test matches provider's documented host"],
        "proxy": [1, "no application proxy configured; other hosts resolve normally"],
        "dns": [2, "local resolver holds stale negative answer; authoritative lookup answers address; controlled bypass of local resolver resolves same host"],
        "source": [8, "retry repeats resolution against same local resolver; no host override"],
    },
    "C": {
        "reproduce": [3, "100 serial attempts: no duplicate; concurrency of incident not reproduced"],
        "incident_trace": [1, "r1 and r2 same billing key: both SELECT absent, both provider requests accepted, then two INSERTs; provider supports idempotency key but received none"],
        "schema": [1, "billing_key non-unique; no durable reservation or database uniqueness invariant"],
        "source": [2, "check-then-act: query invoice, charge provider without idempotency key, insert invoice"],
        "load_test": [6, "synchronized concurrent attempts recreate duplicate on old protocol"],
    },
    "D": {
        "trace": [1, "payment p9 success event version=8 committed; delayed failure version=7 then committed failed"],
        "source": [2, "callback overwrites status without ordering check; manual create/update are separate operations"],
        "consumers": [1, "provider callbacks; manual reconciliation; admin refunds; shared status writer"],
        "contracts": [1, "version orders events within the same provider transaction. Manual payments may have no provider_id. Refunds after success are valid. Failure version=9 for another pending transaction is valid. Duplicate same event must be no-op"],
        "all_tests": [6, "serial success/failure tests pass; no out-of-order or replay fixtures"],
    },
}

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in DATA or sys.argv[2] not in DATA.get(sys.argv[1], {}):
        print(json.dumps({"error": "unknown case/check"}))
        return 2
    case, check = sys.argv[1:]
    cost, evidence = DATA[case][check]
    print(json.dumps({"case": case, "check": check, "cost_units": cost, "evidence": evidence}))
    return 0

if __name__ == "__main__":
    sys.exit(main())
