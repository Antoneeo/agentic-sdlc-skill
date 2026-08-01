# Research Playbook + Evidence Ledger Discipline

Research turns the user's facts into a defendable picture of the outside
world. Its output is never prose alone: every number lands in the ledger,
every claim carries its reference.

## The Evidence Ledger

Single file: `mkt_docs/research/evidence_ledger.md`. One table, one row per
piece of evidence:

| ID | Claim | Class | Value / Range | Source | Date | Confidence |
|---|---|---|---|---|---|---|

- **ID**: `EV-01`, `EV-02`, ... sequential, never reused. Artifacts cite
  numbers as `[EV-nn]`.
- **Class** (exactly one):
  - `FACT` — user input or primary data (their analytics, their CRM export).
    Source = "user, Wave 1" or the data file.
  - `BENCHMARK` — external number. Source URL **and** publication date
    mandatory. The Source cell must carry the actual external URL, NOT a
    pointer to one of your own research documents that aggregates it ("see
    VOC.md" is not a source — the validator rejects a BENCHMARK whose Source
    has no `http`). A benchmark older than 24 months is flagged in review.
  - `ASSUMPTION` — a number we need but could not source. Range mandatory
    (not a point estimate), Confidence mandatory (HIGH/MED/LOW), and the
    rationale in the Claim cell. Assumptions that drive budget decisions are
    listed in the plan's page-one Assumptions section.
- **Laundering is the cardinal sin:** an ASSUMPTION never migrates to
  BENCHMARK without a real source; a stale benchmark is not refreshed by
  editing its date. `mkt_check.py ledger` enforces the mechanical part
  (references resolve, benchmarks have URLs, assumptions have confidence);
  honesty enforces the rest.

**Two-source rule:** any number that will drive a budget allocation or an
objective target needs two independent sources (two ledger rows or one row
citing both). One vendor's blog post does not size a market.

**Source hierarchy** (prefer higher): primary data > official statistics /
regulator data > industry analyst reports > trade press > vendor benchmarks >
individual blog posts (last resort, flag as weak in Confidence).

## The engine

**Preferred:** when the `deep-research` skill (or an equivalent multi-agent
research harness) is available, use it as the engine — one refined question
per sweep, findings adversarially verified, sources cited. Feed its cited
findings into the ledger; do not bypass the ledger because the engine already
cites.

**Fallback:** manual web search per the sweep playbooks below. Slower;
the ledger discipline is identical.

## Mandatory sweeps (E3)

### 1. Market sizing
- Bottom-up first: reachable potential customers (from official statistics,
  association registries, platform audience tools) × realistic price
  `[EV: price FACT]`. Top-down (report % slicing) only as cross-check.
- Output: TAM/SAM/SOM with every input as a ledger row.

### 2. Competitor scan
- Start from the user's seeds (Wave 1) + search-discovered players.
- Per competitor: positioning claim (their own words, from their site),
  visible pricing, observed channels (where do they show up: ads
  transparency libraries, social presence, SEO footprint), review sentiment.
- Output: `mkt_docs/research/COMPETITORS.md` + ledger rows for anything
  numeric. Observed facts, not speculation about their strategy.

### 3. Voice of customer (VoC)
- Mine reviews (their category on G2/Capterra/Trustpilot/Amazon/app stores as
  applicable), forums, Reddit, comment sections — where the target segment
  already speaks.
- Harvest verbatim quotes with URLs: pains, desired outcomes, objections,
  vocabulary (the actual words become messaging raw material).
- Output: `mkt_docs/research/VOC.md`. Persona traits in `ICP_PERSONAS.md`
  must trace here.

### 4. Channel benchmarks
- For candidate channels: typical CPC/CPM, CTR, conversion rates, CAC ranges
  for the industry — each a BENCHMARK row with URL + date.
- These feed the funnel model; without them the funnel is fiction.

### Optional sweeps
- Trends/seasonality (search-volume tools, industry calendars) when timing
  matters; regulatory scan when PESTEL is in play.

## Research spikes

A standalone market question outside a full engagement:
`mkt_docs/spikes/RESEARCH_[topic].md` — question, time-box, method, answer,
ledger rows created, consequences. Max 1 page + ledger entries.

## Anti-patterns

- **Numbers from memory:** model knowledge is not a source. If it matters,
  search it; if unsearchable, it is an ASSUMPTION with a range.
- **Single-source budget decisions** (violates the two-source rule).
- **Prose-only research:** findings that never become ledger rows are lost
  and unverifiable.
- **Competitor mind-reading:** report what is observable; label inference as
  inference.
- **Benchmark hoarding:** 50 ledger rows nobody cites. Research serves the
  plan; unreferenced rows get pruned at closure (validator warns).
