# Operative Guides — pipeline

Support file for `ai_docs/reference/GUIDE_[topic].md`. Read this only when the
trigger below fires; the template lives in `templates.md`.

**The training model (what a guide IS).** A guide TRAINS the agent on a topic
the user cares about, the way training works for a person: you study the
material once, you carry a SYNTHESIS in your head, and you go back to the book
when a task needs detail. Two levels, both produced by this pipeline:
- **The guide = the synthesis** — compact and dense: core principles, decision
  rules, the map of what exists, where people go wrong. Small enough that a
  reader takes it in WHOLE before acting (that is the "preparation").
- **The snapshot = the book** (`.sources/`, verbatim) — the details live here,
  reachable on demand.
- **The fidelity markers are the bridge**: `[source: <snapshot>#anchor]` both
  proves provenance AND tells the reader where in the book the full detail is.
A guide that restates the source at length is as wrong as a fragmented one:
completeness is guaranteed by the book level, economy by the synthesis level.

## 1. When to trigger

Trigger test is origin + purpose, not content taxonomy (no "is this technical
enough" judgement call):
- **Origin**: the user hands you indications to follow — a document to adhere
  to, a pasted policy, "do it this way", a style guide, a runbook.
- **Purpose**: the material is meant to GOVERN how the agent operates, not
  just inform a one-off answer.

Both hold → this is guide material. Either is missing (e.g. the user pastes
background context with no operative intent, or asks a one-off question) →
this is not a guide; answer normally, do not create a file.

Never manufacture a guide from model knowledge. If the user asks for "a guide
on X" without handing over source material, ask for the source first — a
guide with no `distilled_from` is not this pipeline's output.

## 2. Pipeline

0. **Search before creating (DRY — one CURRENT guide per topic).** Before
   proposing anything, read `ai_docs/reference/INDEX.md` and grep
   `reference/GUIDE_*.md` for topic overlap with the new material. Never end
   up with two CURRENT guides on the same topic. Search BOTH routers: project
   `ai_docs/reference/INDEX.md` AND the agent KB router
   `~/.agentic-sdlc/ai_docs/reference/INDEX.md` (if present) — one CURRENT
   guide per topic PER SCOPE; a project guide on a KB topic requires the
   explicit `overrides:` declaration. On overlap, pick by provenance:
   - **Same source, evolved** → UPDATE the existing guide in place: new
     snapshot, new `source_hash`, same file (history lives in git).
   - **Different source replacing the old one** → NEW guide + mark the old
     one `status: SUPERSEDED` (its provenance chain must stay honest — do not
     graft a new source onto a guide distilled from another).
   - **Different source, partial overlap** → flag it to the user explicitly:
     the current frontmatter binds ONE source per guide (`distilled_from`/
     `source_hash` are singular), so a clean multi-source merge is not yet
     supported — regenerate from the prevailing source and mark what the
     merge drops, or keep the topics separate if they truly are.
   Semantic overlap is NOT mechanically detectable: this step is agent
   discipline plus the human reviewing the router — say what you found.
   **Also verify the handed SOURCE itself is current**: check its lifecycle
   (status/supersedes headers) and search the project for a newer version of
   the same document before snapshotting. A user may hand you a path that a
   migrated copy has since superseded — distilling from it produces a guide
   that is born stale. If you find a newer version, surface it and distill
   from that one. (Learned the hard way on first field use, 2026-07-02.)
1. **Decompose into PREPARATION units — and weigh the fragmentation risk.**
   A guide's goal is to PREPARE an agent for a situation: everything that
   situation needs must arrive in ONE guide. The risk is asymmetric — extra
   context injected costs tokens (cheap, recoverable); missing context makes
   the agent invent or fail (the exact failure this pipeline exists to
   prevent). Every split is a bet that no future task will cross the cut.
   Therefore:
   - **Default = one guide per source/domain.** Split ONLY when the resulting
     guides would be consulted in DISJOINT situations — no plausible task
     needs two of them at once.
   - **Run the split test per proposed fragment and DECLARE it** in the
     proposal: "which tasks consult this fragment, and would any of those
     tasks also need another fragment?" Any overlap → merge, do not split.
   - Heterogeneous sources (unrelated policies handed over together) are the
     legitimate split case; a single coherent document about one subsystem
     almost never is.
   - **Also decide SCOPE per proposed guide**: project-scope
     (`ai_docs/reference/`) or agent-scope (`~/.agentic-sdlc/ai_docs/reference/`,
     governs the agent across ALL projects; origin+purpose test unchanged,
     scope is a LOCATION decision by the user, never a content taxonomy; KB
     created lazily with `.sources/` on the first agent-scope guide).
2. **User confirms** the topic decomposition — including the fragmentation-risk
   assessment and scope decision — before any file is written.
3. **Snapshot each source verbatim** into
   `ai_docs/reference/.sources/<slug>-<hash8>.md`:
   - `slug` derives from the topic (lowercase, hyphenated).
   - `hash8` = first 8 hex chars of the snapshot file's own SHA-256 (compute
     the snapshot first, hash it, then name it — the hash is of the file you
     just wrote, not of the original source).
   - The hash is computed over LF-normalized content (CRLF → LF), exactly as
     `sdlc_check.py` does in `sha256_file` — so recorded hashes survive
     checkouts that rewrite line endings (e.g. Windows `core.autocrlf=true`).
   - Recommended for consumer projects: add
     `ai_docs/reference/.sources/** -text` to `.gitattributes` so git never
     rewrites snapshot bytes at all (keeps snapshots byte-verbatim; the
     normalized hash stays stable either way).
   - The snapshot is verbatim: no paraphrasing, no reformatting beyond what is
     needed to save it as markdown.
4. **Source-anchored SYNTHESIS (not restatement).** Select and compress what
   the source says into the operative essence — decision rules, invariants,
   the "where people go wrong" list — and POINT INTO the snapshot for the
   detail (`[source: <snapshot>#anchor]` doubles as the detail-lookup
   pointer: "full checklist → snapshot §7"). Every claim must still trace to
   a specific point in the snapshot; do not extract from memory of the
   conversation — re-read the snapshot while writing each section. Selection
   and compression are allowed and expected; ADDITION is not (that stays
   summarize-and-expand, forbidden). A guide approaching the source's own
   length is a paraphrase, not a synthesis — wrong output.
5. **Render per template** (`templates.md` → `## ai_docs/reference/GUIDE_[topic].md`):
   frontmatter with `source`, `distilled_from`, `source_hash` (the snapshot's
   SHA-256, matching what you just computed), optional `source_version`; body
   sections chosen from the repertoire, each with a fidelity marker.
   **Write for the two-level read**: the guide (synthesis) is small enough to
   be read WHOLE before acting; the snapshot (book) is where size lives and
   where readers grep/partial-read on demand, following the section markers.
   Use the repertoire's stable, self-describing headings, keep one concern per
   `##` section, and make the frontmatter `description` the "should I open
   this file at all" answer. This is why one synthesis + one book beats
   several fragments: the synthesis guarantees the whole picture, the book
   guarantees the details, the markers connect them.
6. **Run `sdlc_check.py index`** so both `ai_docs/INDEX.md` and
   `ai_docs/reference/INDEX.md` (the guide router) regenerate.

## 3. Fidelity rules (mandatory, the D5 constraint)

- Only what the source supports goes in the guide. If the source is silent on
  something a reader might expect, mark the section `[not covered by source]`
  — never fill the gap from general knowledge.
- Every `##` section body carries exactly one kind of marker: `[source:
  <snapshot>#<anchor-or-line>]` for content traceable to the snapshot, or the
  literal `[not covered by source]` for an acknowledged gap. A section with
  neither is a validator warning.
- `summarize-and-expand` is forbidden: do not take a short source note and
  "helpfully" expand it into a longer procedure using inferred steps. If the
  source says one sentence, the guide section says that one sentence
  (source-anchored), not an elaborated version of it.
- When in doubt about whether something is "supported" by the source, treat it
  as not covered rather than stretching the marker to fit.

## 4. Ingestion bound (T9)

If a source document exceeds roughly 2000 lines, do not silently truncate or
skim it. Stop and ask the user to either split it into smaller documents or
select the specific sections relevant to the guide being built. Silent
truncation produces a guide that looks complete but is missing unreviewed
material — worse than asking.

## 5. Review

Before the guide is used operatively for the first time, recommend an
independent guide-vs-source review (a fresh pass comparing the rendered guide
against the snapshot, checking every marker) — process control per the
threat model (P-TM). This is a recommendation to the user, not a hard gate:
state it explicitly when handing off a newly created guide.

## 6. Maintenance

- **Source changed**: create a new snapshot (new hash), regenerate the guide
  from it (new `source_hash`), and if the guide is replacing a prior guide
  rather than updating in place, mark the old one `status: SUPERSEDED`.
- **`stale` flags hash drift**: `sdlc_check.py stale` (also under `--hybrid`)
  compares each guide's recorded `source_hash` against the live snapshot file
  and reports `[stale]` when they diverge — that is the signal to regenerate,
  not a manual freshness check.
- **Agent-global KB guides** use the same pipeline and validator via
  `--root ~/.agentic-sdlc`; freshness via the same `stale` engine.
