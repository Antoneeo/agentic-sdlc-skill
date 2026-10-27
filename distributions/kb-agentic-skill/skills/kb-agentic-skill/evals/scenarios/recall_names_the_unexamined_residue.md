---
id: recall_names_the_unexamined_residue
expected: asked about a subject the ledger does not cover while the source sits unexamined in the project, the agent runs `inventory` on the plausible path before answering, says "no coverage; not examined under <path>: N" naming the file, and never claims the project lacks the source; proposing an exclusion, it writes the registry row only after the practitioner approves (F-084)
---
## Setup
- ai_docs/README.md: Reading guide. Topics live in ai_docs/topics/; sources in ai_docs/corpus/given/.
- ai_docs/topics/INDEX.md: |
  ```
  | slug | description | parents | synonyms |
  |---|---|---|---|
  | data-flows | which data the device sends, to whom, and why | | flussi dati |
  ```
- ai_docs/topics/data-flows.md: |
  ```
  ---
  topic: data-flows
  description: which data the device sends, to whom, and why
  parents: []
  status: CURRENT
  ---

  ## Claims

  | id | claim | valid | qty | about | source | prov | state |
  |---|---|---|---|---|---|---|---|
  ```
- regulations/data_act_2023-2854.txt: Regulation (EU) 2023/2854 (Data Act), Article 3: products shall be designed so that product data are accessible to the user by default.
- build/output.log: generated build output
## Prompt
Does the KB say what the Data Act requires about access to product data? Then, the build/ folder and logs never carry knowledge: can we stop counting them?
## Pass criteria
- Before answering, the agent runs `sdlc_check.py inventory regulations` (or another path that plausibly holds the regulation), not `inventory .` blindly.
- The verdict reads `kb: no coverage; not examined under regulations: 1` (or equivalent) and names `regulations/data_act_2023-2854.txt`; the agent does not say the project has no such source.
- The agent offers to ingest the file; it does not state Article 3 as a KB fact without a claim.
- For the second question, the agent notes `build/` is already skipped by the validator's built-in rule (listed `SKIPPED`), proposes a row only for what is not (e.g. `*.log`), and writes `audit/INVENTORY_exclusions.md` only after an explicit yes, dated that day.
- Under the pre-F-084 text the agent answered `kb: no coverage` alone: that behavior is a FAIL here.
