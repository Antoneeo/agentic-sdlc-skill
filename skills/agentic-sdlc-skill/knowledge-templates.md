# Knowledge templates — shared ledger, sources and rulings

## ai_docs/topics/[slug].md (topic node)

One file per topic, flat directory, hierarchy in frontmatter (`taxonomy.md`).

```markdown
---
topic: pricing
description: How the offer is priced — list prices and negotiated exceptions.
parents: [offerta-commerciale]
owns: [pricing/list-price]
synonyms: [listino, price list]
gaps:
  - volume tiers above 500 units
status: CURRENT
---

## Claims

| id | claim | valid | qty | about | source | prov | state |
|---|---|---|---|---|---|---|---|
| | List price of module A is 12000 EUR | until 2026-03-01 | 12000 EUR cost | - | corpus/given/contract-9a1f2b7c.pdf#p=17@412-509 | GIVEN | OK |
```

- `id` empty when writing by hand: `sdlc_check.py claim-id --fill <file>` computes it.
- `valid` half-open: `from` inclusive, `until` exclusive; `if <cond>` for conditionals.
  Expiry against today is COMPUTED by the reports (`stale`'s `## claims`,
  the orient count line) -- never written into `state`: state transitions
  belong to reconciliation.
- `qty`: `<value> <unit> <kind>` — effort in person-days (h/d/w/mo/fte-mo; 8h=1d, 1w=5d,
  1mo=21d), duration in calendar days (h/d/w/mo), cost within one currency, count unit-matched.
- `about`: `<predicate> -> <slug>` for relationship claims; stored once, under the subject.
- `state`: `OK` | `CONTESTED <id>[,..]` | `SUPERSEDED <id>[,..]` — per claim, never per
  node; a split bundle (`reconciliation.md` §Splitting) names all its successors.
- A tombstone (merged/renamed topic): `status: SUPERSEDED` + `redirect_to: <slug>`, body empty.

## ai_docs/corpus/given/[name].meta.md (source sidecar)

```markdown
---
sha256: <raw-byte digest of the artifact this sidecar names — NOT the LF-normalized text digest>
date: 2026-08-01
provenance: GIVEN
supersedes: contract-1a2b3c4d.pdf
extractor: pdftotext 24.02, form-feed page breaks, whitespace collapsed
extracted_through: p=212
---
Handed over by <who>, <context in one line>.
```

`supersedes:` is what makes "which claims rest on a superseded version" answerable —
without it the two content-addressed files are unrelated. `extractor:` pins the stored
canonical extraction (`<name>-<hash8>.txt`) that offset locators address.

`extracted_through:` is how far the source has been read — `p=<n>` (paged extraction),
`L<n>` (line file), or `complete`. It is **required once any claim cites this artifact**
and it is advanced at the end of every reading window (`distillation.md` §3): unstated,
"I am finished" is not falsifiable, which is exactly how a sampled 200-page manual passes
for an ingested one. Three things are checked: claims with no field (error); a claim
whose locator addresses **past** the declared coverage, or coverage past the end of the
stored bytes (error — the sidecar and the rows contradict each other); coverage short of
the end (warning, because partial work is legal mid-ingestion). Its limit is the mirror
image of `original_sha256`'s: **nothing proves a page was read**, so a field advanced
without extracting is caught at the ingestion review, never by the validator. An artifact
nobody has extracted from yet owes nothing and stays silent.

**Extraction-as-artifact** (`distillation.md` §1 — the variant for a large binary
corpus): when the extraction IS the artifact and the original was never copied in, two
more fields record where it came from.

```markdown
---
sha256: <digest of THIS extraction — enforced, these are the bytes locators address>
date: 2026-08-02
provenance: GIVEN
extractor: pdftotext 24.02, form-feed page breaks, whitespace collapsed
original_path: /vault/manuals/xyz.pdf
original_sha256: <digest at ingest — RECORDED, never checked: we do not hold the file>
---
```

The two fields are **not** in the same position, and writing them as if they were is
how a dangling pointer survives a green run:

- `original_sha256` detects nothing on its own — we do not hold the bytes. It lets a
  human re-verify by hand and it dates the ingest. Keep that limit visible wherever the
  field is written.
- `original_path` **is** checked for resolution, and warns when it does not resolve
  (never errors — an imported bundle carries no originals). **Write it absolute, or
  relative to the project root**; the validator tries the docs root's parent first and
  the docs root second, and names both in the warning. The convention was implicit
  until F-035 and is stated here because a pointer nobody can resolve is worth less
  than no pointer at all.

Write these two values with **no trailing `# comment`**: the frontmatter reader does
not strip inline comments, so the comment lands inside the value.

`provenance:` has a consumer too: a claim row filed `prov: GIVEN` whose artifact's
sidecar declares anything else warns. Declare the chain the artifact actually has —
an OCR, a transcription from an image, a translation are not first-hand evidence, and
saying so in the sidecar's prose is not a check.

Two limits of that warning, stated so it is not mistaken for more than it is. It reads
the row's **first** source, so a weak artifact cited second is not compared. And it can
only read the **field**: a sidecar that says `provenance: GIVEN` while its prose says
"transcribed from a photograph" is silent, because prose is not machine-readable — the
warning catches the author who declared the chain honestly and then filed the row too
strongly, never the author who declared it wrongly. Nothing requires a `given/` sidecar
to carry `provenance:` at all; adding that requirement is a new gate, not this one.

## ai_docs/corpus/notes/RULING_[topic]_[date].md (practitioner ruling)

```markdown
---
origin: ruling
basis: Client confirmed Q3 delivery by phone, 2026-07-30.
date: 2026-08-01
status: CURRENT
---
Ruling on the contested delivery date of module B: Q3 stands.
Supersedes claims <id>, <id> (see topics/<slug>.md).
```

`basis:` is mandatory and states THE FACT the practitioner knows that the corpus lacks —
a preference is not a fact; the validator refuses a ruling without it. The ruling enters
the topic's claim table as a row with `prov: RULING` sourcing this note.

## Typed software topic (opt-in schema 2)

Use the topic fields above, plus `claim_schema: 2`. A typed table has exactly nine
columns. Kind never replaces provenance or claim state.

```markdown
| id | claim | valid | qty | about | source | prov | state | kind |
|---|---|---|---|---|---|---|---|---|
| | A successful edit preserves the logical card identity | if save succeeds | - | - | corpus/notes/card-identity.md#L8-10 | DERIVED | OK | OBSERVATION |
```

Kinds: OBSERVATION (observed), REQUIREMENT (required), HYPOTHESIS (documented
uncertainty), DESIGN (planned). Legacy tables retain eight columns and existing IDs;
evidence reports their nature as UNCLASSIFIED until deliberately classified.

## Software binding (capture-source generated)

```yaml
sha256: <64 hex chars: exact stored extract>
software_schema: 1
software_project_id: <canonical UUID from the docs-root README>
software_path: src/card.py
software_sha256: <64 hex chars: complete file at capture time>
software_lines: 20-48
software_role: code
```

All six software fields are required together. Roles: code, test, config, result.
The generated name contains both the full extract digest and a digest of its binding
and normalized premises; equal text from distinct paths/versions never collides.
Source locators address the STORED extract starting at line 1. `software_lines` locates
it in the original file, not in the extract. Add `extracted_through` only after reading.
No absolute `original_path` is required. These metadata do not attest completeness,
execution, truth, signature or an authenticated project identity.

A derived note uses `derived_from: [corpus/given/<extract>.txt, ...]` for ALL joint
premises. An observation that needs code, configuration and a test result must cite
that note, not list those premises as independent corroborations in its source cell.
