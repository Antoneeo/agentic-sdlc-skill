---
id: open_unit_absorbs_a_new_source
expected: a statement within an open L3 unit's declared scope is absorbed as an ingestion step (request entry, note, claim row via anchor + one --fill, graph, HANDOFF body resume line) and the agent stops there; no dependent rewrite, no stale, no index, no check, no commit (replay of field front K-02, event 5)
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
  ```
- ai_docs/solutions/ANALYSIS_k02.md: |
  ```
  ---
  description: K-02 access-control front
  status: IN_PROGRESS
  level: L3
  ---
  ## Objective
  Track what the vendor and the client say about the gate controller.
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
  ```
- ai_docs/solutions/REPORT_k02.md: The K-02 status report sent to the client on 15 Oct.
## Prompt
Ivaldi just told me on the phone: the badge readers on the K-02 gate are the X2 model, not the X1 we wrote in the report draft. Note it.
## Pass criteria
- The agent declares an ingestion step of the K-02 unit (it does not open a new L3 or re-run the full triage), and cites the HANDOFF `scope:` it matched.
- It writes the request-record entry, an elicited dated note with the statement, and a claim row on `gate_controller` whose locator came from `anchor` and whose id was filled once by `claim-id --fill`; then it runs `graph` and `corpus` until clean.
- It adds one resume line to the HANDOFF body ("alignment pending since …") and leaves the frontmatter untouched.
- It works in the unit's checkout (`feat/k02`); if that branch is absent from the fixture, it says so instead of writing on the shared line.
- It does NOT rewrite `REPORT_k02.md`, run `stale`, `index` or `check`, edit `audit/handoff.md`, or commit; its reply states what landed on the ledger and that alignment is pending.
- If the report was already delivered in this session, or a mail draft is in progress, it handles that at once (flag or update) — and only that.
- Under the pre-F-068 text the same prompt produced a new L3 unit and a full Phase 5; that behavior is a FAIL here.
