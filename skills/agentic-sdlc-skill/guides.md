# Operative Guides — pipeline

Support file for `ai_docs/reference/GUIDE_[topic].md`. Read this only when the
trigger below fires; the template lives in `templates.md`.

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
2. **User confirms** the topic decomposition — including the declared
   fragmentation-risk assessment — before any file is written.
3. **Snapshot each source verbatim** into
   `ai_docs/reference/.sources/<slug>-<hash8>.md`:
   - `slug` derives from the topic (lowercase, hyphenated).
   - `hash8` = first 8 hex chars of the snapshot file's own SHA-256 (compute
     the snapshot first, hash it, then name it — the hash is of the file you
     just wrote, not of the original source).
   - The snapshot is verbatim: no paraphrasing, no reformatting beyond what is
     needed to save it as markdown.
4. **Source-anchored extraction.** Every claim in the guide must trace back to
   a specific point in the snapshot (`#anchor-or-line`). Do not extract from
   memory of the conversation — re-read the snapshot while writing each
   section.
5. **Render per template** (`templates.md` → `## ai_docs/reference/GUIDE_[topic].md`):
   frontmatter with `source`, `distilled_from`, `source_hash` (the snapshot's
   SHA-256, matching what you just computed), optional `source_version`; body
   sections chosen from the repertoire, each with a fidelity marker.
   **Write for selective reading**: guides are delivered by PATH and readers
   grep/partial-read them — size is fine, opacity is not. Use the repertoire's
   stable, self-describing headings (a reader must find "What NOT to do"
   without reading the file top to bottom), keep one concern per `##` section,
   and make the frontmatter `description` the "should I open this file at all"
   answer. This is why a large well-structured single guide beats several
   fragments: navigation replaces fragmentation.
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
