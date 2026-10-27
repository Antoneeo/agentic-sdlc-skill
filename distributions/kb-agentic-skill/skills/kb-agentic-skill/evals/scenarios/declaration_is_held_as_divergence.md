---
id: declaration_is_held_as_divergence
expected: given a document the project has just sent to a client, the agent ingests the sent version with provenance DECLARED, recipient and the send date, files its claims DECLARED, holds the one that contradicts the ledger as DIVERGES (leaving the ledger row untouched) and escalates it at the end of the run; asked what was told to the client, it answers "declared to <client> on <date>" and names the divergence (F-084)
---
## Setup
- ai_docs/README.md: Reading guide. Topics live in ai_docs/topics/; sources in ai_docs/corpus/given/.
- ai_docs/topics/INDEX.md: |
  ```
  | slug | description | parents | synonyms |
  |---|---|---|---|
  | personal-data | which personal data the service processes and on what basis | | dati personali |
  ```
- ai_docs/topics/personal-data.md: |
  ```
  ---
  topic: personal-data
  description: which personal data the service processes and on what basis
  parents: []
  status: CURRENT
  ---

  ## Claims

  | id | claim | valid | qty | about | source | prov | state |
  |---|---|---|---|---|---|---|---|
  | 4c9f980baca2 | The IP address is processed as personal data, retained 30 days | - | - | - | corpus/notes/ruling-ip.md#L6-6 | RULING | OK |
  ```
- ai_docs/corpus/notes/ruling-ip.md: |
  ```
  ---
  basis: the DPO confirmed on 2026-10-10 that IP addresses identify the household
  date: 2026-10-10
  ---

  The IP address is processed as personal data, retained 30 days.
  ```
- deliverables/dpia_v5.1.txt: |
  ```
  DPIA v5.1 - sent to the client on 2026-10-16.
  Section 4, data inventory. IP address: not personal data; not retained.
  Section 5, purposes. Telemetry is used only for fault diagnosis.
  ```
## Prompt
We sent deliverables/dpia_v5.1.txt to the client yesterday evening, 2026-10-16. Record it. Then: what did we tell the client about the IP address?
## Pass criteria
- The sent version is stored in `corpus/given/` with a sidecar carrying `provenance: DECLARED`, `recipient:` naming the client (an organization, not a person), `date: 2026-10-16` and `original_path: deliverables/dpia_v5.1.txt`.
- Its claim rows are `DECLARED`; none is filed GIVEN, and no DECLARED source is appended to the existing RULING row.
- The IP-address row is `DIVERGES 4c9f980baca2`; the RULING row stays `OK` and untouched.
- The divergence is escalated once, at the end of the run, naming the recipient and the send date; the agent does not decide which side is right.
- The answer says "declared to <client> on 2026-10-16" and that it diverges from the DPO-based ruling; it never states "the IP address is not personal data" as a fact.
- `graph` (or `check`) reports no error.
- Under the pre-F-084 text the sent document had no home and the KB could not answer: that behavior is a FAIL here.
