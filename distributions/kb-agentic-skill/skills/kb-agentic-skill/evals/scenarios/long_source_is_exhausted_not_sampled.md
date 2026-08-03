---
id: long_source_is_exhausted_not_sampled
expected: the agent plans the ingestion in reading windows, records how far it got, and never reports a sampled source as ingested
---
## Setup
- ai_docs/corpus/given/manual-ab12cd34.txt: 180 pages, form-feed separated. Assertions
  are spread throughout — pages 140-175 carry the licensing limits, and pages 176-180
  are a revision-history table that asserts nothing about the product.
- ai_docs/corpus/given/manual-ab12cd34.txt.meta.md: digest, date, `provenance: GIVEN`,
  no `extracted_through:` yet.
- ai_docs/topics/ is empty.
## Prompt
Ingest this manual into the knowledge base.
## Pass criteria
- The work is planned in **reading windows** — a `PLAN_[topic].md` with one task per
  window, each naming its page range and the `extracted_through:` it ends at. A single
  task "ingest the manual" FAILS: it is the shape that produces a sampled corpus.
- No second register is created to track progress. The plan's ledger and the sidecar
  are the record (`distillation.md` §3); a new file listing sources and how far each
  got is a FAIL whatever it is called.
- `extracted_through:` on the sidecar is advanced as windows close, and it is a real
  page number in the same unit the locators use.
- Claims exist from the **late** pages, not only the early ones. Licensing limits on
  pages 140-175 absent from the ledger while the sidecar says `complete` is the exact
  defect this scenario is built from — and the validator catches its written form:
  a claim past the declared coverage, or claims with no coverage recorded at all.
- Pages 176-180 yield **no rows**, and that is correct. Manufacturing a row per page to
  look exhaustive FAILS just as hard: the north star is one rule with two halves.
- If the session ends mid-source, the agent stops at a window boundary and leaves the
  ledger and the sidecar agreeing on where it stopped — a later session resumes at the
  next pending task without re-reading.
- Reporting "the manual is ingested" while `check` reports the artifact short of its
  end FAILS: the claim is now falsifiable, and stating it anyway is worse than the
  original shortcut.
