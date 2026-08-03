# Distillation — from a source to claim rows

**For whom**: the agent ingesting a source into the corpus.
**Answers**: "what is a claim, how does a source become rows, and where does every kind
of knowledge get its file".
**Does not answer**: where a claim's concept lives (above — `taxonomy.md`) or what
happens when it disagrees with an existing one (`reconciliation.md`).

## 1. Intake — everything becomes a file first

Ingest **never touches the graph**. First the source enters the corpus; the graph is fed
from the corpus, so everything is re-derivable when the rules improve.

| What arrives | Where it lands |
|---|---|
| a file from the practitioner | `corpus/given/<name>-<hash8>.<ext>` — verbatim, **content-addressed with a raw-byte sha256**; a newer version is a new file whose sidecar says `supersedes: <old>` — never an overwrite |
| a non-text original (PDF, docx, xlsx) | its **canonical extraction**: `corpus/given/<name>-<hash8>.txt`, pages separated by form-feed; extractor id, version and normalization recorded in the sidecar. Offsets address THIS file — stored bytes, not a runtime step. The original is copied beside it when it is small enough to be worth keeping; **on a large or binary-heavy corpus the extraction is the artifact and the original stays where it is** (below) |
| something the practitioner says | a transcription in `corpus/notes/`, frontmatter `origin: elicited`, dated |
| an agent synthesis | a note in `corpus/notes/` with `derived_from:` listing its sources — a note with neither `origin:` nor `derived_from:` nor `basis:` is **model knowledge disguised as a source**, and the validator refuses it |
| a practitioner ruling | a note with `basis:` (`reconciliation.md`) |

Every sidecar (`<artifact>.meta.md`) carries: the digest, the date, provenance, and
`supersedes:` when it replaces an earlier version. `corpus/INDEX.md` is generated.

**Extraction-as-artifact — the variant for a large binary corpus.** Copying gigabytes
of PDFs into the docs root buys nothing: what the digest protects is *the bytes a
locator addresses*, and those are the extraction's. So the extraction may be the
corpus artifact on its own. Then `sha256:` is the extraction's digest — immutability is
enforced exactly as before — and the original is recorded, not copied:

```yaml
sha256: <digest of this extraction>      # enforced: the bytes locators address
original_path: /vault/manuals/xyz.pdf    # recorded: where the original lives
original_sha256: <digest at ingest>      # recorded, NOT verified — we do not hold it
```

Say the limit out loud, because a field that looks like a guarantee and is not is worse
than an absent one: **`original_sha256` is never checked.** It lets a human re-verify by
hand and it dates the ingest; it detects nothing on its own. The digest that bites is
`sha256:`. Same honesty as a guide's `source_hash`, which proves the source is unchanged
and never that the guide described it correctly.

## 2. The claim — one falsifiable assertion

The unit of knowledge is the **claim**, not the document. "Doc A and doc B disagree" is
not actionable; "A says delivery Q1, B says Q3" is. A claim is a sentence that can be
true or false: "the system is robust" is not one; "the retry runs 3 times with backoff"
is.

Claims live in the owning topic's `## Claims` table (`templates.md` has the template):

| id | claim | valid | qty | about | source | prov | state |
|---|---|---|---|---|---|---|---|

- **id** — leave empty when writing by hand; `sdlc_check.py claim-id --fill <file>`
  computes it (`sha256(path#locator#qty)`, text excluded — a paraphrase must not mint a
  new identity). An empty id is a `[note]`, never an error.
- **valid** — `-`, `from X`, `until X`, `from X until Y`, `if <condition>`. Half-open:
  `until 2026-03-01` and `from 2026-03-01` do NOT overlap. A time-bounded fact is not a
  conflict with its successor — write the scope, or reconciliation will manufacture one.
- **qty** — `-` or `<value> <unit> <kind>`, kind ∈ effort/cost/duration/count. Effort in
  person-days (8h=1d, 1w=5d, 1mo=21d), duration in calendar days, cost within ONE
  currency. A figure without a unit cannot be summed, compared, or even classified as
  agreement.
- **about** — `-` or `<predicate> -> <slug>` for a claim about a relationship
  ("depends-on -> phase-1"). Stored once, under the subject; the index computes the
  reverse direction.
- **source** — `<path>#<locator>`; corroborating sources append with `;`. Locators:
  `p=<n>@<start>-<end>` (character offsets into page n of the stored extraction),
  `L<a>-<b>` (line files), `Sheet<s>!<cell>`. The span must exist — the validator opens
  the file and checks.
- **prov** — `GIVEN | ELICITED | DERIVED | RULING`. Information for whoever resolves a
  conflict; never a rank.
- **state** — `OK`, `CONTESTED <ids>`, `SUPERSEDED <id>` (`reconciliation.md` owns the
  transitions).

## 3. Extraction discipline

Read the stored extraction (not the original) and emit one row per assertion, each with
the offset span it came from. The extractor **invents nothing**: no labels, no
summaries-as-claims, no filling of gaps from model knowledge. What the source does not
assert does not become a row — it may become a `gaps:` entry on the topic.

**Cover the gates, not only the powers.** "One row per assertion" is obeyable and still
leaves the ledger optimistic: reading a capability paragraph, an extractor emits the
capability and moves on, because that is what the paragraph asserts. So for every row
saying what the subject **can do**, ask the source what must hold first — a documented
default-off state, a licence or edition gate, a firmware or version floor, something
that must be enabled elsewhere, a dependency on another construct. Each one the source
states is **its own row, with its own span**.

The failure this prevents is an answer that is true and unusable: *"yes, supported —
three verified rows"* is a plan that fails on site when the function ships disabled. On
a corpus whose purpose is to deflate over-promising, an extraction axis that records
powers and skips gates inverts the point.

**The rule is _ask_, never _produce_.** A source stating no precondition yields no
precondition row — the paragraph above still governs. An invented gate is the same
defect as an invented capability, and a gate you suspect but cannot locate is a `gaps:`
entry, not a claim. Nothing mechanical can enforce this (no validator detects an
assertion that was never extracted), which is why it carries no column and no check:
it is verified at the ingestion review (`review.md`), and it is stated here so the
extractor knows it before the reviewer does.

**Anchor across line wraps.** A PDF extraction breaks phrases mid-line, so a multi-word
anchor must match a literal space as `\s+` or it silently finds nothing — and a probe
that pretty-prints collapsed whitespace will show you the phrase intact while the
checker sees the break. `sdlc_check.py anchor` does this for you; hand-authoring a
locator without it is how two generation rounds get lost.

Extraction is read-only on the corpus and blind to the graph: rows go to placement
(`taxonomy.md`) afterwards. Ingesting a document set is **L3 by Rule Zero**; the
ingestion plan derives from the ANALYSIS Action Plan, one task per source, each task's
`verify` = "claim rows parse; every source resolves under the docs root". Serial in v1:
correctness first.

## 4. Signal discipline (what "distillation" still means)

- Contract-first for any prose you write around the rows (reader, action, payload).
- Zero speculation: unverified information is marked `[unverified]` or omitted — never
  written as a claim.
- No noise: no filler, no restated boilerplate; the claim table IS the signal.
- Lifecycle: every document carries `status:` frontmatter; superseding knowledge marks
  the old file `SUPERSEDED` (documents) or the old row (claims).
