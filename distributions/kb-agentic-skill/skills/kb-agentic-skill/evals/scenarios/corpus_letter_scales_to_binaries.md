---
id: corpus_letter_scales_to_binaries
expected: the agent ingests a large binary corpus by storing the canonical extraction as the artifact, and does not copy gigabytes into the docs root
---
## Setup
- A folder outside the repository, `/vault/manuals/`, holding 230 MB of PDFs.
- ai_docs/corpus/given/ is empty.
- The practitioner asks for the manuals to be ingested and grounded.
## Prompt
Ingest the manuals in /vault/manuals. They're about 230 MB of PDFs and they live on a
synced drive I'd rather not duplicate.
## Pass criteria
- The agent stores the **canonical extraction** as the corpus artifact
  (`corpus/given/<name>-<hash8>.txt`), records `sha256:` of that extraction, and records
  the original as `original_path:` + `original_sha256:` — it does NOT copy the PDFs into
  the docs root (`distillation.md` §1, extraction-as-artifact).
- It states the limit rather than implying a guarantee: `original_sha256` is recorded
  and never checked; the digest that bites is the extraction's, because those are the
  bytes a locator addresses.
- `sdlc_check.py corpus` is clean with no original present.
- It does NOT reason that the corpus letter forbids this and ask the practitioner to
  copy the files anyway.
