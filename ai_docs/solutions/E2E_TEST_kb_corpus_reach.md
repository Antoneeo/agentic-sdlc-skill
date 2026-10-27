---
feature: F-084
analysis: ANALYSIS_kb_corpus_reach.md
---
# E2E test: the corpus knows what it never examined, and what we declared

## What changed, in user terms

- A new command, `inventory <path>`, lists every project file under a path with its
  state against the knowledge base: already in it, in it in an older version, left out
  by an approved exclusion, or never examined. Code, dependency and dot folders are
  shown once as skipped.
- At session start, in a project with a corpus, the agent sees how many project files
  at most were never examined.
- `stale` names an ingested source whose original changed since it was ingested.
- A document you send out (to a client, a supplier) is stored as sent, with recipient
  and date; what it says is recorded as "declared", never as a fact about the product.
  When it contradicts a decision in the ledger, the contradiction is held and shown.
  Declarations are never exported to another project.

## Environment and preconditions

- The kb lens installed from the merged commit, Python 3 on the path.
- A project with a corpus: `ai_docs/corpus/given/` holding at least one artifact with
  a sidecar, and `ai_docs/topics/`. A real one is best; any test project works.
- Below, `kb` stands for `python <kb skill>/scripts/sdlc_check.py`.

## New-behavior scenarios

### S1 — the inventory of a folder (AC1, AC2)
Steps:
1. Put a PDF the corpus has never seen in `pdf/` of the project.
2. `kb inventory pdf --root <project>`; then `kb inventory . --root <project>`.
3. `kb inventory ../elsewhere --root <project>` and `kb inventory ai_docs --root <project>`.

Expected:
- step 2 lists the PDF as `NOT_EXAMINED`, files already ingested as `INGESTED` with
  their sidecar, `node_modules/`/`.git/`-like folders once as `SKIPPED`, in path
  order, then `Nothing was written.`; no totals line;
- step 3 prints `[ERROR]` and exits 2.

Result:

### S2 — exclusions (AC3)
Steps:
1. Create `ai_docs/audit/INVENTORY_exclusions.md` with a row `| *.log | build logs | <today> |`.
2. `kb inventory . --root <project>`; then add a row with an empty reason and run
   `kb validate --root <project>`.

Expected:
- `.log` files are `EXCLUDED` with the pattern;
- the malformed row is one `[ERROR] audit/INVENTORY_exclusions.md:<line>: …`.

Result:

### S3 — orient's count (AC4)
Steps:
1. Start a new agent session in the project (or `kb orient --root <project>`).

Expected:
- a line `Corpus reach: <= N project files not examined -- exact: sdlc_check.py inventory <path>`,
  with N matching the NOT_EXAMINED lines of `inventory .` or slightly above it.

Result:

### S4 — a changed original (AC5)
Steps:
1. Pick an artifact whose sidecar has `original_path:` and `original_sha256:`; edit
   the original file in the project.
2. `kb stale --root <project>`; then `kb check --root <project>`.

Expected:
- `stale`'s `## claims` names the artifact, the original and the number of citing
  claims; `check` does not mention it.

Result:

### S5 — a sent document and its divergence (AC6, AC7)
Steps:
1. Ask the agent: "we sent <document> to <client> on <date>: record it", where the
   document contradicts one ledger row.
2. `kb graph --root <project>`; then ask "what did we tell <client> about <subject>?".

Expected:
- the artifact's sidecar says `provenance: DECLARED`, `recipient:`, the send date;
- its rows are `DECLARED`; the contradicting one is `DIVERGES <ledger id>`; the
  ledger row is unchanged; `graph` is clean;
- the answer says "declared to <client> on <date>" and names the divergence.

Result:

### S6 — declarations stay home (AC8)
Steps:
1. `kb export --out ../bundle --root <project>`.
2. Import the bundle into an empty project, then `kb check` there.

Expected:
- export prints `declarations stay in this project: not exported`;
- the bundle holds no `DECLARED` row and no sent document; the import and `check`
  are clean.

Result:

### S7 — the docs site
Steps:
1. `python <kb skill>/scripts/docs_site.py --root <project> --open`.

Expected:
- a declared fact shows the origin "declared by this project" and, when it diverges,
  the tag "diverges" with the fact it diverges from; the chronology says "document
  sent" for it.

Result:

## Regression scenarios

### R1 — an existing project without declarations or registry
Steps: `kb check`, `kb stale`, `kb export` and `kb orient` on a project that predates
this version.
Expected: the same findings as before, plus at most the orient line; no new error.
Result:

### R2 — the other lenses
Steps: `check` in a code, marketing and course project with no corpus.
Expected: unchanged output; `inventory` exists in each and works.
Result:
