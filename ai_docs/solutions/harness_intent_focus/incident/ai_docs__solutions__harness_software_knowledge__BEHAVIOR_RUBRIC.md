# Frozen comparison rubric — 2026-10-04, before F063 candidate triggers

Three variants share immutable inputs: F057 baseline at 2d5a5c6; that baseline plus
instruction-only capture/reconciliation; implemented candidate. Each gets a fresh
first context and a different fresh second context, no history or answer supplied.
The four cases are bundled within each session; this economizes context but does
not provide isolated per-case time/token estimates. Results are exploratory, not
a statistically powered claim about all agents.

After session one, set config attempts to 1, rename identity.py to card_identity.py
and remove identity-test.txt; retain all first-session ai_docs. Session two sees only
the current project, skill and its task. Eclosion source reports remain frozen.

Correctness: no invented sources; no design promoted to observed; retain every
named property and report unverified limits. Eclosion core PASS does not prove full
card integration. Retry configuration change invalidates a conclusion based on the
old config; the proposed five attempts/delays are not implemented. Rename/delete
require re-verification, not automatic falsification of the property.

Measure each session: source/doc files opened (agent's explicit path log, self-report),
elapsed wall time, written files (filesystem delta), corrections required, reused
relations. Token counts unavailable unless instrumented: never estimate them.
Compare second-session reconstruction and cumulative work even if cost increases.
Failure or inconclusive benefit is reported, not redefined as success.
