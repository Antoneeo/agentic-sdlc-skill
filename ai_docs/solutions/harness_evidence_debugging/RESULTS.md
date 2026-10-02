# F-061 — behavioral comparison and limits

## Design and execution

Four synthetic incidents and their acceptance rubric were frozen in PACKET.md
before drafting CANDIDATE.md. FROZEN.json records SHA256 of packet, probe, baseline
and pre-F061 SKILL snapshot. `tally.py` verifies those hashes and recounts costs.
Two fresh read-only subagents received only their assigned method and the same
packet; they queried the synthetic read-only evidence surface one check at a time.
Both used the inherited model: independent context, not different-model evidence.
No real service, code correction or software regression test was performed.
The parent copied each agent's final response into BASELINE_RESPONSE.md and
CANDIDATE_RESPONSE.md. These are final reports, not full tool-usage transcripts;
sequences are the agents' reported performed checks. Provenance has this limit.

## Initial comparison

| Case | Baseline sequence / units | Initial candidate sequence / units | Assessment |
|---|---|---|---|
| A | reproduce, logs, effective_config / 7 | logs, effective_config / 2 | Same cause; evidence-first obtains the diagnosis without the costly replay |
| B | effective_config, dns / 3 | effective_config, dns / 3 | NULL on selection/cost; both follow evidence and avoid the cheap irrelevant proxy check |
| C | reproduce, incident_trace, schema, source / 7 | incident_trace, schema, source, reproduce / 7 | Earlier causal evidence; no cost improvement. Both spend on a serial reproduction that does not exercise concurrency |
| D | trace, source, consumers, contracts / 5 | trace, source, contracts, consumers / 5 | Same cause and valid-path protection; no demonstrated substantive improvement |

Recounted totals: baseline **13 checks / 22 units**; initial candidate **12 checks /
17 units**. The baseline introduction erroneously says 21; candidate introduction
erroneously says 13/19. Originals are preserved; the authoritative counts above
come from summing each reported sequence with the frozen probe's cost values.
Units are illustrative costs chosen for this packet, not seconds, money or tokens.
The difference is entirely Case A's omitted reproduction; it does not establish a
general efficiency gain. Both readers correctly identified all four mechanisms.

## Adherence and potential deterioration

- Baseline fails the proposed evidence-first ordering in A; this is a narrow RED,
  not proof that baseline cannot find a root cause. It already rejects unrelated
  retries, blanket callback suppression and uniqueness only after external charge.
- Initial candidate passes A's ordering and explicitly separates DNS-layer cause
  from endpoint recovery, intermittent evidence from deterministic replay, and
  temporary containment from a permanent correction.
- Hypothesis updates are present in prose but the initial candidate does not show
  the full accumulated register. Full FS2 behavioral adherence is **not proven**.
- The initial candidate still performs a low-value serial check in C. General
  optimal ordering is **not proven**. The final support adds four lines to reject
  known-unfaithful reproductions and stop diagnostics that cannot alter the
  decision, explicitly preserving mandatory fix/regression verification.
- Partial logs, evidence preservation before urgent containment and supported why
  chains are textual-review coverage in the initial comparison, not measured
  behavior. SUPPLEMENTAL_PACKET.md defines a fresh C/E retest of final wording;
  it has no baseline for E and cannot support a comparative efficacy claim.
- No trial independently verifies causal fixes, real regressions, source/caller
  coverage or production recovery; subjects only proposed them. A named consumer
  list without graph/text coverage never certifies completeness.
- Added reading and register duties may increase costs on simple incidents. Keep
  the register in existing L2/L3 output, no dedicated files; L1 remains exempt.
  No forced five whys, no fabricated likelihood percentages, no mandatory global
  log sweep, no universal fail-fast crash or refactor licence.

## Technical verification

Fresh final-wording retest: C queries incident_trace then schema, two units/two
checks, no known-unfaithful serial reproduction. It supplies an explicit updated
hypothesis table, supported causal links and provisional design pending consumer/
contract inspection. E retains unknown hypotheses, preserves accessible evidence
without waiting for unavailable logs, labels restart containment and does not
invent five whys or a definitive fix. Original: RETEST_RESPONSE.md.
This scoped retest supports those behaviors only; no final-wording full A-D trial
was run, and no combined total substitutes retest C into the earlier comparison.

Existing invariant battery after initial integration: 64 tests passed. Its first
run after adding the analysis failed only generated-index idempotence; regeneration
resolved that failure. Final command outputs and return codes are retained in
invariants_final.txt, check_after.txt and verification.json after final edits.
Index regeneration needed sandbox escalation for ai_docs/memory/INDEX.md only;
the same authorized local index command succeeded with escalation.
Repository baseline `check_before.txt`: NOT CLEAN, with existing schema warnings
and stale distributions/ai_docs. Generated alignment errors caused by the new
analysis/handoff are addressed by index, not hidden through false area re-marking.
The initial warning for F-061's Vision Alignment heading is local to this change;
it was corrected to the validator's Feature Vision heading. Other warnings are
preexisting. Final reading delta: 71→118 lines, +3643 UTF-8 LF bytes in debugging;
SKILL +249 bytes relative to its pre-F061 snapshot. Cost is added, not erased.
Final global result will be recorded separately; it is not inferred from invariants.
`check_after.txt`: validation zero errors, 18 preexisting warnings; stale exit 1,
so global check remains NOT CLEAN. New method edits also make the skills area
stale; broader preexisting distributions/ai_docs changes remain. None was falsely
re-marked as wholly analyzed. F-061 stays IN_PROGRESS under the closure gate.

## Review state

Design PASS: 3 WARN, 0 BLOCK; status semantics and Vision placement clarified,
coverage limitations disclosed. Closure round 1 FAIL: arithmetic B1; authoritative
counts corrected while preserving originals. W1 (partial register, C waste) is
explicitly retained above. Scoped round 2 PASS confirms arithmetic, honest
limitations and four-line relevance/stop rule without waiving regression tests.
Round 3 PASS covers the supplemental C/E evidence and final claims with their
limits. Global closure is explicitly not certified by the reviewer.
