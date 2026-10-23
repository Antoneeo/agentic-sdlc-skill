---
feature: F-077
analysis: ANALYSIS_kb_intake_hygiene.md
---
# E2E test: kb intake hygiene

## What changed, in user terms

A team document with passwords or tokens no longer enters the knowledge base as is:
the agent replaces the values before storing it and says what it replaced. If a
credential reaches a stored source anyway (or was stored before this release),
`check` stops with the file, the line and the kind, never the value. A source that
holds a secret can be withdrawn. `adopt` shows, without writing, what moving a
project's document guides into the corpus would involve. The same text stored twice
is reported.

## Environment and preconditions

- The packages built from the merged branch, installed with `npm i -g` (all four),
  Claude Code with Python on PATH.
- A scratch project (not this repository) with `ai_docs/` initialized by the installer.
- A fake configuration file with invented values, e.g. `app.properties` holding
  `db.url=jdbc:postgresql://db.example.test/app`, `db.user=app`,
  `db.password=<invent one>`. Never use a real credential.

## New-behavior scenarios

### S1 — AC1: a credential in the corpus stops `check`
Steps: 1. Copy `app.properties` unchanged into `ai_docs/corpus/given/` with a sidecar
`app.properties.meta.md` (`sha256:` of the file, `date:`). 2. Run
`sdlc_check.py check` with the kb entry point, then with the code entry point.
Expected: both fail; each prints one `[ERROR] corpus/given/app.properties: line 3 look
like a credential (password)` line with the fix; the invented value appears nowhere.
Result:

### S2 — AC2/AC3: redacted or reviewed passes
Steps: 1. Replace the value with `[REDACTED: password]`, update `sha256:`, add
`redacted_at_intake: [password]`; run `check`. 2. Restore the value and instead add
`credential_scan: reviewed — test fixture`; run `check`.
Expected: both runs show no credential error.
Result:

### S3 — FS1/FS9: the agent redacts at intake
Steps: In a kb-agentic session: "Put app.properties in the knowledge base and record
what it says about the database."
Expected: the stored artifact carries `[REDACTED: password]`; the sidecar declares
`redacted_at_intake:` and has no `original_sha256:`; the agent runs `corpus` (or
`check`) before any commit; the reply never repeats the value.
Result:

### S4 — AC5: a document guide's snapshot is scanned in every lens
Steps: 1. In a project with no `corpus/`, create a `source_kind: document` guide whose
`distilled_from:` is a snapshot in `ai_docs/reference/.sources/` holding the fake
password. 2. Run `check` with the code, kb and marketing entry points
(marketing: `--docs-dir ai_docs`). 3. Change the guide to `source_kind: code`.
Expected: steps 2: one credential error per run; step 3: none.
Result:

### S5 — AC6: withdrawal
Steps: Starting from S1: store the redacted successor (content-addressed name,
`supersedes:` the tombstone name); delete the old bytes; rename the old sidecar to
`app-withdrawn-<YYYYMMDD>.properties.meta.md`, remove its `sha256:`, add
`withdrawn: credential`; run `index` and `check`.
Expected: `check` clean; `corpus/INDEX.md` shows the tombstone row as `withdrawn`.
Put `sha256:` back on the tombstone: `check` errors. Leave a stray file in `given/`
with no sidecar: `corpus` warns "no sidecar".
Result:

### S6 — AC8: `adopt` writes nothing
Steps: In a project with document guides on `.sources/` snapshots, note
`git status`, run `sdlc_check.py adopt`, run `git status` again.
Expected: the listing names each document guide, its snapshot, credential lines if
any, the number of code guides, and "Nothing was written"; `git status` unchanged.
Result:

### S7 — AC7/AC9: one home, original_ref
Steps: 1. Put the same text in `ai_docs/reference/.sources/x.md` and
`ai_docs/corpus/given/x.md` (with sidecar); run `corpus`. 2. Add
`original_ref: wiki://space/page` to a sidecar; run `corpus`. 3. Put
`original_path: https://wiki.example.test/x` instead.
Expected: 1. one "hold the same text" warning naming both; 2. nothing about the
original; 3. a "does not resolve" warning that names `original_ref:`.
Result:

## Regression scenarios

### R1 — a clean corpus stays clean
Steps: Run `check` on an existing kb project with no credentials in `given/`.
Expected: same result as before the upgrade (no new error; a `given/` file without a
sidecar is the only possible new warning).
Result:

### R2 — guides without a corpus
Steps: In a code-lens project with document guides whose snapshots hold no
credentials, run `check`, `stale`, `index`.
Expected: unchanged output.
Result:

### R3 — export and import
Steps: `export --out ../bundle` from a kb project, `import ../bundle --dry-run` into
another, then `import`, then `check`.
Expected: as before; a tombstone (if any) is not in the bundle.
Result:

### R4 — the docs site
Steps: `docs_site.py --root <project> --open` on a kb project.
Expected: sources and chronology as before; a withdrawn artifact is not listed as a
source.
Result:
