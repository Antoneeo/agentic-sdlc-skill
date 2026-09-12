---
id: recall_verdict_names_every_branch
expected: the answering claim lives under a topic that is NOT the obvious branch for the question, so a correct descent opens more than one candidate — and the declared verdict names every slug it opened, not only the one that answered
---
## Setup
- ai_docs/README.md: Reading guide. Topics live in ai_docs/topics/.
- ai_docs/topics/INDEX.md: |
  ```
  | slug | description | parents | synonyms |
  |---|---|---|---|
  | gdpr_compliance | lawful basis, data-subject rights and the DPO approval chain | | privacy, gdpr |
  | identity | tenant model, roles and the permission matrix | | auth, ruoli |
  | observability | logging, metrics, tracing and the alerting rules | | monitoring, log |
  ```
- ai_docs/topics/observability.md: |
  ```
  ---
  topic: observability
  description: logging, metrics, tracing and the alerting rules
  parents: []
  status: CURRENT
  gaps:
    - no claim yet on the tracing sampling rate
  ---

  ## Claims

  | id | claim | valid | qty | about | source | prov | state |
  |---|---|---|---|---|---|---|---|
  | c-obs-01 | Access logs are written to the append-only audit sink, never to stdout | - | - | - | corpus/notes/obs-elicited.md#L4-4 | ELICITED | OK |
  ```
- ai_docs/topics/gdpr_compliance.md: |
  ```
  ---
  topic: gdpr_compliance
  description: lawful basis, data-subject rights and the DPO approval chain
  parents: []
  status: CURRENT
  ---

  ## Claims

  | id | claim | valid | qty | about | source | prov | state |
  |---|---|---|---|---|---|---|---|
  | c-gdpr-01 | Access logs are retained 90 days, then irreversibly deleted | from 2026-04-01 | 90 days | - | corpus/notes/dpo-ruling.md#L6-6 | RULING | OK |
  ```
- ai_docs/topics/identity.md: |
  ```
  ---
  topic: identity
  description: tenant model, roles and the permission matrix
  parents: []
  status: CURRENT
  ---

  ## Claims

  | id | claim | valid | qty | about | source | prov | state |
  |---|---|---|---|---|---|---|---|
  | c-id-01 | A tenant admin may invite other admins without support involvement | - | - | - | corpus/notes/identity-elicited.md#L2-2 | ELICITED | OK |
  ```
- ai_docs/corpus/notes/dpo-ruling.md: |
  ```
  ---
  origin: ruling
  basis: DPO confirmed the 90-day figure in the 2026-03-28 privacy review
  ---
  Access logs are retained 90 days, then irreversibly deleted.
  ```
## Prompt
For how long do we retain access logs? A customer asks it in a security questionnaire, so I need OUR figure, not a generic best practice.
## Pass criteria
- The agent scans `topics/INDEX.md` and descends BEFORE answering; it does not answer from model memory.
- More than one branch is opened: `observability` is the obvious candidate for a question about logs (synonym `log`, and it carries log claims), while the answering claim sits under `gdpr_compliance`. Stopping at the first plausible branch is the failure this scenario exists to catch.
- The answer cites `c-gdpr-01` (90 days) and names its `RULING` provenance — a formal decision, not an observed practice.
- **The declared verdict names EVERY slug the descent opened**, in the multi-slug form: e.g. `kb: gdpr_compliance, observability → 1 claim cited`. A verdict naming only the answering slug under-reports the descent; a single-slug form invented ad hoc for two branches is the contract gap this form closes.
- `kb: no coverage` is NOT declared: the corpus holds the answer, and a descent that reached it cannot report absence.
- `c-obs-01` may be cited as collateral (log integrity) only with its weaker `ELICITED` provenance named; it is never offered as the retention figure.
