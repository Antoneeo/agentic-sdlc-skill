---
id: alignment_closes_once
expected: on "allinea" after several ingestion steps, the agent runs one Phase 5 — sweep, stale, one full re-read per dependent document, HANDOFF update, index, check, commit on the unit branch with an integration proposal — and keeps the unit open
---
## Setup
- ai_docs/README.md: Reading guide. Topics live in ai_docs/topics/.
- ai_docs/audit/HANDOFF_k02.md: |
  ```
  ---
  workstream: K-02 access-control front
  level: L3
  branch: feat/k02
  status: IN_PROGRESS
  since: 2026-10-15
  next: keep ingesting the K-02 correspondence
  details: solutions/ANALYSIS_k02.md
  scope: K-02 — every source and statement on the gate controller and its badge readers
  updated: 2026-10-15
  ---
  # HANDOFF: K-02

  - alignment pending since 2026-10-16: mail from the vendor (2 rows, 1 supersession)
  - alignment pending since 2026-10-16: phone statement by Ivaldi (1 row)
  ```
- ai_docs/solutions/ANALYSIS_k02.md: |
  ```
  ---
  description: K-02 access-control front
  status: IN_PROGRESS
  level: L3
  ---
  ## Objective
  ```
- ai_docs/audit/requests/REQUEST_k02.md: |
  ```
  ### R4 — 2026-10-16 — vendor mail ingested (step)
  > Vendor mail: the controller ships with firmware 3.2, not 3.1.
  ### R5 — 2026-10-16 — phone statement by Ivaldi (step)
  > The badge readers are the X2 model.
  ```
- ai_docs/topics/gate_controller.md: |
  ```
  ---
  topic: gate_controller
  description: the gate controller and its badge readers
  parents: []
  status: CURRENT
  ---

  ## Claims

  | id | claim | valid | qty | about | source | prov | state |
  |---|---|---|---|---|---|---|---|
  | aaaaaaaaaaaa | Controller firmware is 3.1 | - | - | - | corpus/notes/old.md#L1-1 | ELICITED | SUPERSEDED bbbbbbbbbbbb |
  | bbbbbbbbbbbb | Controller firmware is 3.2 | - | - | - | corpus/notes/mail.md#L1-1 | ELICITED | OK |
  ```
- ai_docs/solutions/REPORT_k02.md: The K-02 status report: firmware per claim aaaaaaaaaaaa; readers are X1.
## Prompt
allinea
## Pass criteria
- The agent runs Phase 5 once: the Capture Moment sweep, `stale`, then one full re-read and rewrite of `REPORT_k02.md` covering BOTH pending steps (not one rewrite per step).
- It enumerates what to revise from the request-record entries since the last closure and the uncommitted changes, not from memory.
- It updates the HANDOFF frontmatter and body to current state (the pending lines resolved), runs `index`, then `check`; its reply states the gate result, the documents revised and the commit (or that nothing was committed).
- With `check` clean it commits on `feat/k02` and proposes integration, leaving the choice to the practitioner; the HANDOFF is NOT deleted (alignment closure, the unit stays open) and no closure review runs.
- The fixture's ids and sources are illustrative: `check` may go red on them, which exercises the red path; there is no `feat/k02` git branch either — the agent says so rather than committing on the shared line.
- If `check` is red, it does not commit, names the failing checks, and keeps the unit open.
