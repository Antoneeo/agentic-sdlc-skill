# Distillation — from a source to claim rows

**For whom**: the agent ingesting a source into the corpus.
**Answers**: "what is a claim, how does a source become rows, and where does every kind
of knowledge get its file".
**Does not answer**: where a claim's concept lives (above — `taxonomy.md`) or what
happens when it disagrees with an existing one (`reconciliation.md`).

> **North star.** *Not one assertion the source makes may be lost, and not one it does
> not make may appear.* These are one rule, not two: a ledger that invents nothing but
> keeps a tenth of the manual is as useless as one that keeps everything and made half
> of it up.
>
> The unit is the **assertion**, not the byte: layout, ordering, repetition and page
> furniture are not assertions. A page that asserts nothing yields nothing — exhaustive
> means **read**, never *a row per page*. And "I am finished" is an assertion like any
> other: `extracted_through:` is what makes it falsifiable.

Everything below is that one rule made operable. Where a rule below does not reach the
case in front of you, decide by the north star — both halves of it, in the same breath.

## 1. Intake — everything becomes a file first

Ingest **never touches the graph**. First the source enters the corpus; the graph is fed
from the corpus, so everything is re-derivable when the rules improve.

| What arrives | Where it lands |
|---|---|
| a file from the practitioner | `corpus/given/<name>-<hash8>.<ext>` — verbatim, **content-addressed with a raw-byte sha256**; a newer version is a new file whose sidecar says `supersedes: <old>` — never an overwrite |
| a non-text original (PDF, docx, xlsx) | its **canonical extraction**: `corpus/given/<name>-<hash8>.txt`, pages separated by form-feed; extractor id, version and normalization recorded in the sidecar. Offsets address THIS file — stored bytes, not a runtime step. The original is copied beside it when it is small enough to be worth keeping; **on a large or binary-heavy corpus the extraction is the artifact and the original stays where it is** (below) |
| something the practitioner says | a transcription in `corpus/notes/`, frontmatter `origin: elicited`, dated |
| a document the project sends out | the version sent, in `corpus/given/` like any source (redacted at intake), sidecar `provenance: DECLARED`, `recipient:` (an organization or role, never a private person's name) and `date:` = the day sent; when the file also lives in the project, `original_path:` names it. Its claims are `DECLARED`: what we said, to whom, when — not facts about the product. A resend `supersedes:` the earlier send; drafts and the files a document is generated from never enter |
| an agent synthesis | a note in `corpus/notes/` with `derived_from:` listing its sources — a note with neither `origin:` nor `derived_from:` nor `basis:` is **model knowledge disguised as a source**, and the validator refuses it |
| a practitioner ruling | a note with `basis:` (`reconciliation.md`) |

Every sidecar (`<artifact>.meta.md`) carries: the digest, the date, provenance,
`supersedes:` when it replaces an earlier version, and `extracted_through:` once anything
has been extracted from it (§3). `corpus/INDEX.md` is generated.

**Redact before storing — the one exception to verbatim.** `given/` is committed and
never edited, so what enters it must be safe to keep. Replace every credential value
and the personal or confidential third-party data the KB does not need (a role may
replace a name) with `[REDACTED: <kind>]`, the request record's marker. What the source
asserts about the value survives; the value does not — the north star's declared
exception, written in the sidecar's `redacted_at_intake: [<kind>, …]`. The digest is
the redacted bytes'. When something was redacted, keep **no `original_sha256:`** (beside
the redacted text it tests password guesses offline) and **never copy a non-text
original beside its extraction**. Notes follow the same rule and are fixed by editing.

`check` and `corpus` refuse a `given/` file — or a document guide's snapshot — holding a
credential-shaped line (a `key=value`/`key: value` whose key ends in a credential word,
with a real value; a private-key header; a password in a URL; a bearer token), naming
lines and kinds, **never the value**. Like `original_sha256`, say its limits: it flags
manual field descriptors (`Password: required`) and misses passphrases with spaces,
table rows, list items (`- password=…`), Markdown emphasis, `-Dpassword=…`, prose and
vendor formats. Only a human clears a false positive, with
`credential_scan: reviewed — <reason>` in the sidecar (for a stored `.txt` extraction,
its artifact's sidecar; for a snapshot, the guide); `redacted_at_intake:` never does. The
ingestion step runs `corpus` beside `graph`, so nothing is saved unscanned.

**Withdrawing an artifact that holds a secret** — the one removal `given/` allows. Store
the redacted successor; delete the old bytes; rename the old sidecar
`<stem>-withdrawn-<YYYYMMDD>.<ext>.meta.md` (`-2` for a second that day), drop its
`sha256:` and any `original_sha256:`, and add `withdrawn: <reason>`; the successor says `supersedes:` that name.
Re-place the claims and re-point the `derived_from:` that named the old artifact.
`check` refuses a tombstone with a digest and warns on any `given/` file without a
sidecar (a `.txt` extraction beside its declared artifact excepted); `export` never ships a tombstone. The bytes stay in git history: tell the user;
purging it is theirs.

**Extraction-as-artifact — the variant for a large binary corpus.** Copying gigabytes
of PDFs into the docs root buys nothing: what the digest protects is *the bytes a
locator addresses*, and those are the extraction's. So the extraction may be the
corpus artifact on its own. Then `sha256:` is the extraction's digest — immutability is
enforced exactly as before — and the original is recorded, not copied:

```yaml
sha256: <digest of this extraction>
original_path: /vault/manuals/xyz.pdf
original_sha256: <digest at ingest>
```

`sha256:` is the enforced one — the bytes the locators address. `original_path:` says
where the original lives and is checked to still resolve. `original_sha256:` is recorded
and never verified. **Write no trailing `# comment` on these lines**: the frontmatter
reader is a line regex and does not strip them, so the comment becomes part of the
value — which on `original_path:` now means a pointer that cannot resolve.

Say the limit out loud, because a field that looks like a guarantee and is not is worse
than an absent one — and say it **per field**, because the two are not in the same
position:

- **`original_sha256` is checked only where the original is local.** `stale` and
  `inventory` hash the file `original_path:` resolves to, when it is a local regular
  file, and report an original that changed since ingest (`stale`'s `## claims`, until
  a successor sidecar `supersedes:` this one). `check` never does: it runs on every
  change, and re-reading gigabytes there is not proportional. Elsewhere — a remote, a
  cloud-only file, no path — it detects nothing; it lets a human re-verify by hand and
  it dates the ingest.
  Same honesty as a guide's `source_hash`, which proves the source is unchanged and
  never that the guide described it correctly.
- **`original_path` IS checked — for resolution only.** "We do not hold it" was never a
  reason to leave the *pointer* unverified: it costs one `exists()`, and on a corpus
  whose whole premise is that every provenance is a real file, a pointer that has gone
  dangling in silence is the failure this design most wants to catch. A path that does
  not resolve is a **warning**, never an error: a bundle carries artifacts and sidecars
  and never the originals (`portability.md` §1), so after an import it dangles
  legitimately. Absolute paths are tested as written; a relative one is tried against
  the docs root's parent (the project root in the standard layout) and against the docs
  root itself, and warns only if neither resolves. "Absolute" here means what either
  platform calls rooted, `/vault/...` included: testing it with `Path.is_absolute()`
  alone was a real defect, because on Windows a rooted path with no drive letter is not
  absolute and got silently joined onto the docs root's drive.

The digest that bites is `sha256:`, on the bytes the locators actually address.

**Where the original is, when no path should be written.** `original_path:` is
optional. A non-local identifier (a wiki page, a document-system id) goes in
`original_ref:`, recorded and never resolved; a personal location (a home directory) is
not recorded. A URI in `original_path:` warns and names `original_ref:`.

**A document guide with a corpus — one home per source text.** Here a
`source_kind: document` guide's source is a `given/` artifact, not a `.sources/`
snapshot (this overrides `guides.md` §2 step 3): `distilled_from:` and the markers name
it, `source_hash` is the line-ending-normalized digest `stale` computes (not the
sidecar's raw `sha256:`, which differs on CRLF), and sections cite the claim ids
extracted from their span, so a superseded claim reaches the guide. `.sources/` stays
for code guides; `check` warns when a snapshot and a `given/` artifact hold the same
text. Moving existing guides: `portability.md` §6.

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
  **Its limit, stated as plainly as `original_sha256`'s:** excluding the text is what
  makes the same assertion mint the same id in another project, which is what makes
  `portability.md`'s de-duplication mechanical instead of a judgement call. The price is
  that **one span cannot carry two different assertions at the same qty** — the id
  cannot tell them apart, and the validator refuses the pair. That refusal is a
  symptom of a non-atomic row (§3): the fix is to **narrow each locator to the
  sub-span that carries its own assertion** — narrow spans make atomic rows
  id-distinct by construction. Merge ONLY when the two rows state the same single
  assertion twice; merging distinct assertions manufactures a bundled row (§3),
  trading the mechanical error for a semantic one no check can see. Narrowing is
  not nudging: a narrowed locator still addresses exactly the words that support
  its assertion, and the validator still opens the span. What stays forbidden is
  editing the qty, or moving a locator onto bytes that do NOT carry the assertion,
  until the hash differs — that distorts the evidence to satisfy a hash function,
  which is the one repair this ledger exists to prevent. A locator edit mints a
  NEW id; citers of the old one are reached by the cascade (`reconciliation.md`
  §Splitting a bundled row).
- **valid** — `-`, `from X`, `until X`, `from X until Y`, `if <condition>`. Half-open:
  `until 2026-03-01` and `from 2026-03-01` do NOT overlap. A time-bounded fact is not a
  conflict with its successor — write the scope, or reconciliation will manufacture one.
- **qty** — `-` or `<value> <unit> <kind>`, kind ∈ effort/cost/duration/count. Effort in
  person-days (8h=1d, 1w=5d, 1mo=21d), duration in calendar days, cost within ONE
  currency. A figure without a unit cannot be summed, compared, or even classified as
  agreement.
- **about** — `-` or `<predicate> -> <slug>` for a claim about a relationship
  ("depends-on -> phase-1"). Stored once, under the subject; the index computes the
  reverse direction. Several relations share one cell, separated by `; `. One predicate is reserved: `not-yet-honored-by -> ANALYSIS_<name>` says the code does not yet honor this specification claim and names the analysis that records the deferred fix, which must cite the claim id (`check` verifies both). In Hybrid the target is `SHADOW_<doc_key>`: the newest `solutions/SHADOW_<doc_key>_vX.Y.md` must exist and cite it. It states the code's relation to the claim, not what the source asserts: the code-lens unit that defers or makes the fix writes or removes it, never a knowledge unit. It has no reverse direction, and nothing lists or selects claims by it. Export drops it: it describes this project's code.
- **source** — `<path>#<locator>`; corroborating sources append with `;`. Locators:
  `p=<n>@<start>-<end>` (character offsets into page n of the stored extraction),
  `L<a>-<b>` (line files), `Sheet<s>!<cell>`. The span must exist — the validator opens
  the file and checks.
- **prov** — `GIVEN | ELICITED | DERIVED | RULING | IMPORTED | DECLARED`. `DECLARED`
  rests only on a document this project sent (its sidecar says so and names the
  `recipient:`), and no other provenance may cite one, in any source position — a
  declaration is never corroboration (`reconciliation.md` §1). `IMPORTED` is a ruling that came from another project (`portability.md`): it keeps its text and original `basis:`, it rests on a renamed copy of its note that says `imported_from:`, `import` reopens the set it had settled, and nothing is settled by it until you ratify it with a ruling of your own. Information for whoever resolves a
  conflict; never a rank.
- **state** — `OK`, `CONTESTED <id>[,..]`, `SUPERSEDED <id>[,..]`, and on a DECLARED row
  only `DIVERGES <id>[,..]` (`reconciliation.md` owns the transitions; a split bundle
  names ALL its successors).

## 3. Extraction discipline

Read the stored extraction (not the original) and emit one row per assertion, each with
the offset span it came from. The extractor **invents nothing**: no labels, no
summaries-as-claims, no filling of gaps from model knowledge. What the source does not
assert does not become a row — it may become a `gaps:` entry on the topic.

**One row asserts one thing — the span is not the unit.** The extraction unit is a
source span; the unit of use is one assertion, and they are not the same size: a row
can be atomic as provenance and plural as meaning. The common source of plurality is
the **reviewer-comment shape** — one comment under one feature heading asserting
several facts about several subjects (a capability at the door, another actor's
console, a verification flow). Extracted as one span it becomes one legal row, and
every downstream citation of it is faithful to the text while asserting what the
source did not: the off-topic part is read as applying to the citing context
(borrowed capability), another actor's surface counts as this actor's (wrong actor),
an ambiguous subject silently switches referent — and the writer who avoids all
three by quoting only the on-topic part has lost an assertion instead. Both halves
of the north star, violated by one bundled row. So **emit one row per assertion even
when the source packs several into one sentence**, and **cite the narrowest span
that supports the assertion, not the paragraph that contains it** — narrow spans are
also what make atomic rows id-distinct (§2). Sub-line precision needs no
re-extraction on a stored `.txt`: a form-feed-free file is one page, so
`p=1@<a>-<b>` addresses character offsets below the line; re-extraction is needed
only for a source with no character-addressable stored form. A bundled row already
in the ledger is repaired by splitting (`reconciliation.md` §Splitting a bundled
row), never edited in place. The validator can only hint here — a `[note]` on
suspicious claim text, heuristic and fallible, never an error: atomicity is
meaning, and meaning is verified at the ingestion review.

**Exhaust the source; never sample it.** *Invents nothing* is a floor, and a floor is not
a target: an extractor that stops the moment nothing it wrote is false stops on page
twenty of a two-hundred-page manual, with every row it emitted correct. A source is
finished when every page has been **read**, not when enough rows exist. The claim count
settles nothing in either direction — a short source legitimately yields few rows and a
dense one yields many — so it can never distinguish *finished* from *sampled*.

**Read in a bounded window, and let the plan hold your place.** A long source does not fit
in one context, and an agent that runs out of room has two moves: summarize, or stop
silently. It summarizes. So read a fixed span, emit that span's rows, and only then move
on. **30 pages is the default and the plan states the window actually used** — page
density and context budgets differ per source and per model, so the number is declared
per ingestion rather than assumed. The window is also the unit of resumption: one plan
task per window (below), so a session that ends mid-source resumes at the next task
instead of re-reading or guessing where it stopped.

**Close each window by advancing `extracted_through:`** on the artifact's sidecar
(`templates.md`) — `p=<n>`, `L<n>`, or `complete` when the last page is read. It is what
makes "I am finished" falsifiable, and it makes the rows and the field check each other:
a claim whose locator addresses past the declared coverage is a contradiction, and the
validator reports it. Say the limit out loud, as with `original_sha256` above:
**nothing here proves a page was read.** A field advanced without extracting is not
mechanically detectable, precisely because a page that asserts nothing legitimately
yields no rows — that direction is verified at the ingestion review (`review.md`), like
the gates below. What the field buys is that the shortcut must now be **written down** to
pass, and a written claim can be reopened by anyone who cares to.

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
ingestion plan derives from the ANALYSIS Action Plan, **one task per reading window** —
a source that fits one window is one task, a 200-page manual at 30 pages is seven — each
task's `verify` = "claim rows parse; every source resolves under the docs root; the
sidecar's `extracted_through:` reaches this window's last page". Serial in v1:
correctness first.

The plan's ledger already records `status: done` per task (`templates.md`), which is the
register that survives a session boundary — so ingestion **builds no second one**. What
has been covered is recorded (the sidecar, the ledger); what remains is derived from
them, never stored.

## 4. Signal discipline (what "distillation" still means)

- Contract-first for any prose you write around the rows (reader, action, payload).
- Language: `given/` artifacts and snapshots keep the source's language, never
  translated. Claim text and guide synthesis are written in the language of the
  document that holds them (the topic, the guide); the span still points at the
  original bytes, and the row's `prov` is the source's — a claim is the extractor's
  rendering, never a quote. A stored translation is a `corpus/notes/` note with
  `derived_from:` the artifact, never a `given/` artifact.
- Zero speculation: unverified information is marked `[unverified]` or omitted — never
  written as a claim.
- No noise: no filler, no restated boilerplate; the claim table IS the signal.
- Lifecycle: every document carries `status:` frontmatter; superseding knowledge marks
  the old file `SUPERSEDED` (documents) or the old row (claims).
