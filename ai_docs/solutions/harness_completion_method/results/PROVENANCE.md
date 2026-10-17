# Provenance of participant outputs

Date: 2026-10-10, Europe/Rome. All trials used native `collaboration.spawn_agent`
with `fork_turns="none"`, no model or effort override. Exact runtime model ID,
effort, per-run duration and tokens are unavailable; no cost estimate is claimed.
The same inherited model/configuration and same three files were requested.
Fresh context does not eliminate shared client instructions or model correlation.

`sample_1_excluded.md` is preserved but excluded: approval review denied one input.
User subsequently explicitly authorized subagent reads of all three named inputs.
Samples 4–6 received an added permission statement, not a diagnostic hint.

Samples 2 and 3 confirmed read completeness after returning their assessment.
No extra reads or revised findings were requested. Verbatim follow-ups:

## Sample 2

Yes. All three assigned files were read completely; initially truncated sections were recovered through subsequent chunked reads. No truncation remained unresolved.

No approval rejected a read. The initial default-launcher attempt failed because BitLocker volume E: was locked; subsequent escalated read-only calls succeeded.

## Sample 3

Yes. All three assigned files were read in full; initial output truncation was resolved through subsequent chunked reads. No unresolved truncation remained.

No approval rejected a read. Initial default-launcher attempts failed because drive E: was BitLocker-locked; escalated read-only calls succeeded.

## Manual scoring against the frozen protocol

These are experiment observations, not production-readiness review approvals.
Every participant returned NOT_READY about the intentionally faulty application.
Detection PASS below means the participant detected that fault.

| Sample | Full inputs | Concrete mismatch | Executable witness | No blanket acceptance | Static/runtime distinction | Detection |
|---|---|---|---|---|---|---|
| 1 | No | Yes | Yes | Yes | Yes | EXCLUDED |
| 2 | Yes | Yes | Yes: empty catalogue | Yes | Yes | PASS |
| 3 | Yes | Yes | Yes: two records | Yes | Yes | PASS |
| 4 | Yes | Yes | Yes: empty catalogue | Yes | Yes | PASS |
| 5 | Yes | Yes | Yes: input and expected output | Yes | Yes | PASS |
| 6 | Yes | Yes | Yes: empty catalogue | Yes | Yes | PASS |

Five valid detections out of five trials is a ceiling result for this supplied
packet, not a reliability estimate and not proof that the skill caused detection.
There was no no-skill comparison, modified-skill arm, held-out evaluation, or full
authoring workflow. All producers were visible together in a short packet.
