---
id: F-077
feature: kb intake hygiene — secrets redacted at intake, adoption on an existing ai_docs, one home per source text
description: Why a credential handed over in a team's documents could become an immutable, hash-checked corpus artifact or guide snapshot, why a project that ingested its documents as guide snapshots had no path into kb-agentic, and the redaction rule, credential check, withdrawal, adoption dry run and one-home rule that close both.
status: COMPLETED
level: L3
domain: code
topics: [corpus, intake, redaction, credentials, guides, adoption]
start_date: 2026-10-23
end_date: 2026-10-23
branch: claude/f077-kb-intake-hygiene-cf9cd8
---
# kb intake hygiene — redaction, adoption, one home per source text

## Objective

A field project installed agentic-sdlc and kb-agentic together and reported three gaps
(REQUEST R1), handled here in priority order:

1. **Secrets in immutable sources.** `corpus/given/` artifacts are verbatim,
   sha256-checked and never edited; guide snapshots in `reference/.sources/` are
   verbatim and hash-pinned. A team's documents, `.properties` files included, carry
   passwords and tokens; nothing tells the agent to remove them before intake, nothing
   flags them after, and a `given/` artifact cannot be removed at all.
2. **No path from agentic-sdlc's guide pipeline into kb-agentic.** The project ingested
   its documents as `source_kind: document` guides with snapshots in `.sources/`. No
   procedure says how to move them into `corpus/given/`.
3. **Two homes for one text.** With both skills, the same document can live in
   `.sources/` and in `corpus/given/`, and nothing reports it.

Measured before design (`harness_kb_intake_hygiene/probe.py`, kb entry point):
- B1/B2 GREEN: a document guide whose `distilled_from:` names a `corpus/given/` artifact
  passes `check` and `stale`, and `stale` reports it `[stale]` when the bytes change —
  provided `source_hash` is the line-ending-normalized digest `stale` computes; the
  sidecar's raw `sha256:` copied there makes a CRLF artifact `[stale]` at once. No new
  mechanism is needed for a guide to rest on the corpus.
- P1 RED: a `given/` artifact with `db.password=…` passes `check`. P3 RED: the same text
  in `.sources/` and `given/` is not reported. P4 RED: no adoption inventory exists.
- P2, P5 GREEN as regression guards.

## Feature Vision

`vision/project_vision.md` is APPROVED. Served:
- Goal "Keep understanding durable across sessions … nothing load-bearing lives only in
  a transcript": adoption keeps a project's earlier ingestion instead of re-doing it;
  one home per text keeps the guide and the ledger reading the same bytes.
- The Solo developer's and the Practitioner's work (Actors): both commit what the
  methodology tells their agent to store. The user's guarantee says that output stays
  in their repository forever; today the methodology tells the agent to store a team's
  secrets there verbatim and makes the corpus copy unremovable. That is a defect of
  shipped behaviour against a constraint, and the redaction duty restates for the
  corpus the rule request records already carry (`templates.md`, r26).

Admission (`vision/rulings.md`, precedent first) — one row per question, **r35**
(r33 and r34 are taken by F-080 and F-076):
- **r35a — tells the agent to redact secrets, and personal or confidential data the KB
  does not need, before a source is stored; refuses (error) credential-shaped lines in
  `given/` artifacts and document-guide snapshots; lets a secret-bearing artifact be
  withdrawn.** Not exempt maintenance: the product now refuses what it accepted and
  deletes what it never deleted (r7). r4: the corpus check is shared (r24), so the new
  error reaches every lens's `check` on a tree with a corpus or document guides —
  scope growth ruled here, not inherited. Advances Goal 2 (what stays durable is safe
  to keep) and the Solo developer's "ceremony proportional to risk" only with the cost
  disclosed below. Non-Goal "no ceremony ratchet": an at-rest corpus or snapshot with a
  credential line fails `check` at its next run whatever the change's level; on a
  project whose CI runs `check`, that includes an L1 change. The cost is stated in
  §Ceremony disclosure. Whether that L1 exposure is admissible is the owner's ruling,
  not this document's: the Non-Goal's L1 clause is unconditional, and this proposal's
  reading — a one-time remediation of data at rest, after which trivial changes pay
  nothing — is put to the owner as CONTESTED with the cost question.
- **r35b — lists, without writing, the document guides that rest on snapshots and what
  moving each into the corpus involves.** Near **r2** (collects derived per-document
  state into one surface): distinction line — `adopt` is the dry-run plan of one
  change the user has decided to make (an L3 adoption), run inside that change, like
  `migrate`'s and `import --dry-run`'s plans; Non-Goal 1 carves out "sequencing the
  steps inside one approved change". It shows per guide where its source file is and
  what the move would touch — facts about files, no score, count per status, order
  or recommendation (r3); ordered by path. If the owner reads it as r2's question, the
  row is CONTESTED and theirs to rule.
- **r35c — reports the same text stored in two places.** A validator finding on two
  named files, like the digest check; no state view.
- Coupling: the patterns are generic shapes (`key=value` lines, PEM headers, URL
  userinfo, bearer headers), written from those formats' own syntax; nothing is copied
  from a secret-scanning tool, and no vendor key format is matched.

Non-goals: no detection of personal or confidential data (no shape a line can be
tested for; the duty is redaction at intake, verified at the ingestion review); no scan
of code-guide snapshots (R6) or of `corpus/notes/` (editable — fixed by editing, under
the same redaction duty); no `--apply` for `adopt`; no purge of git history (destructive,
the user's decision, stated to them); no change to `import`; the docs site's copy of
corpus text is F-079's surface. `VISION_kb_second_brain.md` is not served by this unit.

Elicitation: the three findings (R1) are the goal; the approved F-075..F-080 plan (R2;
its content is quoted in `REQUEST_session_orientation_reach.md` R5) set the scope;
the probes in the brief are the acceptance signals. Real doubts asked: R3 (error, with
a reviewed escape), R4 (language), R5 (withdraw), R6 (document snapshots scanned), R7
(personal and confidential data redacted by need). Choices weighed here:
- **Marker** `[REDACTED: <kind>]`, the request record's: one marker family-wide.
- **Reviewed escape is its own field** (`credential_scan: reviewed — <reason>`) over
  letting `redacted_at_intake:` silence the check: a declaration that redaction happened
  is not evidence that nothing was missed.
- **`original_ref:` as its own field**, never resolved, over teaching `original_path:`
  to skip URIs: "path means checked" stays true, and a home-directory path that names a
  person has a replacement.
- **`adopt` report-only**: each guide needs a choice of source and a redaction pass that
  a copy would skip; contra — the agent copies a few files by hand, once.
- **One-home and corpus intake live in kb doctrine; snapshot redaction lives in shared
  `guides.md`.** Only kb ships `distillation.md` and `portability.md`, so a rule to
  source guides from `given/` belongs there, with kb's override of `guides.md`'s
  snapshot steps for document guides. But R6 makes every lens's `check` fail on a
  credential in a document snapshot, and every lens writes snapshots under `guides.md`
  step 3 ("verbatim"): without one redaction sentence there, shipped doctrine would
  tell the agent to copy the secret the shipped check then refuses. Pro: one coherent
  rule per surface; contra: ~0.4 KB in a file every lens reads when creating a guide.

Success signals: the probe green; a field session adopting kb-agentic moves its
document guides into `corpus/given/` with no credential committed and no text in two
homes.

## Use Cases / User Needs

- **UC1 — Practitioner's agent ingesting a team document** (Practitioner). A
  configuration file or manual with credentials enters `given/` with the values replaced
  and the replaced kinds declared; the committed corpus holds no secret, no unneeded
  personal data, and says what it removed. Benefit: Goal 2.
- **UC2 — Closure gate and ingestion step** (Practitioner, Solo developer). A credential
  that reached `given/` or a document snapshot stops `check` (closure) and `corpus`
  (ingestion step, before any save commit), naming file, lines and kinds, never the
  value. Benefit: Goal 2.
- **UC3 — Removing a secret already stored** (Practitioner). A secret-bearing artifact is
  withdrawn: a redacted successor replaces it, its bytes are deleted, its sidecar stays
  as the record that it existed and why it went. Benefit: Goal 2.
- **UC4 — Adopting kb-agentic on an existing `ai_docs/`** (Practitioner, Solo developer).
  The agent lists the document guides and their snapshots, sees which carry credential
  lines, and follows one procedure to move each into the corpus. Benefit: Goal 2.
- **UC5 — Guide upkeep with a corpus** (Practitioner). A document guide rests on a
  `given/` artifact, cites claim ids where they exist, and has no `.sources/` twin; a
  twin is reported. Benefit: Goal 2.
- **UC6 — Claims from a source in another language** (Practitioner). Sources stay
  verbatim; claim text and guide synthesis follow the document they are written in
  (R4). Benefit: the Practitioner's Good UX (their own domain's units — the team reads
  the ledger in its language) with provenance intact (Goal 2).

Grounding: `corpus/given/`, sidecar, `sha256:`, `original_path:`, `original_sha256:`,
`provenance:`, `supersedes:`, `distilled_from:`, `source_hash`, `reference/.sources/`,
`check`, `corpus`, `graph`, `stale`, `export`, ingestion step, `[REDACTED: <kind>]`,
claim id — EXISTS. `redacted_at_intake:`, `credential_scan:`, `withdrawn:`,
`original_ref:`, `adopt` — NEW.

## Functional Spec

**FS1 — redaction at intake (R7).** Before a source is stored in `given/` (or as a
document-guide snapshot), credential values are replaced by `[REDACTED: <kind>]`, and
personal or confidential third-party data the knowledge base does not need is replaced
the same way (a role — "the DBA" — may replace a name). What the source asserts about
the value survives ("the database password is set in `db.password`"); the value does
not. The stored bytes are the redacted ones; the sidecar lists the kinds in
`redacted_at_intake:` and carries **no digest of the unredacted bytes** (no
`original_sha256:`); a non-text original that was redacted through its extraction is
**not** copied beside it. Nothing to redact: nothing declared.

**FS2 — credential check.** On `check` (every lens; once per run) and on `corpus`, never
on `validate`, every file in
`given/` other than sidecars, and every snapshot named by the `distilled_from:` of a
`source_kind: document` guide (a guide with no `source_kind` counts as document), is
scanned. A file holding at least one credential-shaped line is an **error** (R3):
`[ERROR] <file>: line(s) <n,…> look like a credential (<kinds>) — …`, at most ten line
numbers, kinds from `password`, `secret`, `token`, `api-key`, `access-key`,
`private-key`, `client-secret`, `credentials`, `connection-string`, `bearer-token`;
**the value is never printed**. The message names both fixes: redact into a successor
and withdraw this one (FS3), or declare a reviewed false positive.

A line is credential-shaped when one of these holds:
- **assignment**: after optional indentation and `export `, a key (letters, digits,
  `_ . -`), optionally enclosed in one pair of `"` or `'`, then optional spaces, `=` or
  `:`, optional spaces, and a value. The key is split into segments on `_ . -` and
  lower-to-upper case changes, lowercased. It matches when its last two segments are
  `api key`, `access key`, `private key`, `client secret` or `secret key` (kind from the
  pair: `api-key`, `access-key`, `private-key`, `client-secret`, `secret`) — checked
  first — or else its **last** segment is `password`/`passwd`/`passphrase` (`password`),
  `secret`, `token`, `credential`/`credentials` (`credentials`), `apikey` (`api-key`),
  `accesskey` (`access-key`). The value (enclosing quotes and a trailing `,` removed, a
  ` #…` / ` //…` comment cut) is real unless it is empty, contains whitespace, is
  `true`/`false`/`null`/`none`/`yes`/`no`, is a YAML block indicator (`|` or `>`,
  optionally followed by `-`/`+`), is a `[REDACTED…` marker, a placeholder (`<…>`,
  `${…}`, `{{…}}`, `%(…)s`, `ENC(…)`), or only `*`/`x`;
- **private key**: `-----BEGIN … PRIVATE KEY-----`;
- **URL password**: `scheme://user:password@` (the user may be empty) with a real password, or a query
  parameter `password=`/`pwd=`/`passwd=` with a real value (kind `connection-string`);
- **bearer**: `Bearer ` followed by at least 16 token characters.

Flagged, by those rules: `db.password=s3cr3t`, `DB_PASSWORD: s3cr3t`,
`"password": "s3cr3t",`, `dbPassword = s3cr3t`, `export API_TOKEN=abc`,
`client_secret=xyz` (`client-secret`), `csrf_token: abc` (a token: accepted FP class),
`-----BEGIN RSA PRIVATE KEY-----`, `postgresql://app:s3cr3t@host/db`,
`jdbc:…?user=a&password=s3cr3t`, `Authorization: Bearer <16+ chars>`.
Not flagged: `password.min.length=8`, `max_tokens: 4096`, `tokenizer: x`,
`Password: the one you chose`, `Enter your password:` prose, `password: |`,
`db.password=${DB_PW}`, a URL without a password. Declared false positives (cleared by
the reviewed escape): single-word field descriptors in manuals (`Password: required`,
`Token: optional`, `password: -`), `csrf_token`-style keys. Declared false negatives:
values containing whitespace (passphrases), Markdown table rows
(`| password | s3cr3t |`), list items (`- POSTGRES_PASSWORD=x`, `- password: x`),
Markdown emphasis (`**Password:** x`), `-Dpassword=x`, credentials in XML elements or
prose, keys whose credential word is not last (`secret_key_base`), vendor key formats
in free text (no vendor format is matched). For a stored `.txt` extraction with no
sidecar of its own, the escape is read from its artifact's sidecar.

Escapes: for a `given/` artifact, a sidecar field `credential_scan: reviewed — <reason>`
(the word `reviewed` and a non-empty reason); for a snapshot, the same field in the
guide's frontmatter. `redacted_at_intake:` alone does not silence. A file with a NUL
byte in its first 8 KB is not read unless it starts with a UTF-16 byte-order mark
(then decoded); a line is inspected on its first 4,096 characters.

**FS3 — withdrawal (R5).** Withdrawing a secret-bearing `given/` artifact `<stem>-<hash8>.<ext>`:
its bytes are deleted; its sidecar is renamed `<stem>-withdrawn-<YYYYMMDD>.<ext>.meta.md`
and keeps `date:`, `provenance:` and `supersedes:` but **no `sha256:` and no other digest
of the withdrawn bytes** (the name's `hash8` goes with the rename), and gains
`withdrawn: <reason>`. A tombstone therefore holds nothing that tests a password guess.
The redacted successor's sidecar says `supersedes: <stem>-withdrawn-<YYYYMMDD>.<ext>`.
Claims citing the old artifact are re-placed on the successor; notes whose
`derived_from:` named it are re-pointed. `check`: a withdrawn sidecar without bytes is
accepted (today "sidecar exists but the original is gone"); with a `sha256:` or `original_sha256:` it is an
error; a second withdrawal of the same stem on the same day takes `-withdrawn-<YYYYMMDD>-2`.
Any `given/` file with no sidecar is a warning ("no sidecar: an artifact nobody
declared, or bytes a withdrawal left behind"), so leftover bytes are visible whatever
was redacted; a `supersedes:` naming a tombstone is accepted (today "not
in given/"); claims or `derived_from:` still naming the old artifact fail or warn as
today until re-placed. `export` never ships a tombstone; the corpus index marks its row
`withdrawn`; the docs site lists no tombstone as a source (the corpus index it shows
carries the row). The bytes, the old name and its `hash8` stay in git history: the
agent says so and leaves the purge to the user.

**FS4 — where the original is.** `original_path:` stays optional. A non-local
identifier of the original (a wiki page, a document-system id) goes in `original_ref:`,
never resolved, never warned about. An `original_path:` value starting with a URI
scheme of two or more letters followed by `://` still warns as unresolvable, and the
warning names `original_ref:` (a drive letter `C:` is not a scheme). A personal path
(a home directory) is not recorded.

**FS5 — language (R4).** `given/` artifacts and snapshots keep the source's language,
never translated. Claim text and guide synthesis are written in the language of the
document that holds them (the topic, the guide); the span points at the original
bytes. The row's `prov` is the source's (a claim is always the extractor's rendering,
not a quote). A stored translation is a `corpus/notes/` note with `derived_from:` the
artifact, never a `given/` artifact.

**FS6 — one home per source text (kb doctrine).** In a project with `corpus/given/`, a
`source_kind: document` guide's source is a `given/` artifact: `distilled_from:` names
it, `source_hash` is the line-ending-normalized digest (`stale`'s), markers name it,
and sections cite the claim ids extracted from their span where they exist. No
`.sources/` snapshot is made for it; `.sources/` stays for code guides and for projects
without a corpus. `check` and `corpus` warn once per pair when a `.sources/` file and a
`given/` artifact hold the same text after line-ending normalization, naming both.

**FS7 — `adopt` (dry run).** `sdlc_check.py adopt [--root] [--docs-dir]` writes nothing
and prints, per document guide ordered by path: the guide; its `distilled_from:`; where
that is (`.sources/` snapshot, already in `corpus/given/`, elsewhere, missing, or
outside the project root — not read); the `given/` artifact with the same text, if any;
credential-shaped lines (numbers and kinds). Then the number of code guides, which stay
on `.sources/`, and "Nothing was written. Procedure: portability.md §6 (kb-agentic)."
Exit 0 on any inventory; 1 with no docs root.

**FS8 — adoption procedure** (`portability.md` §6, L3). Inventory (`adopt`); per guide,
choose the source — the original when reachable and the version the guide was distilled
from, else the snapshot, whose sidecar says it is a verbatim excerpt of what, curated
when; redact (FS1); store with sidecar; re-point the guide (FS6); delete the snapshot;
`check`, `stale`. Past decisions: analyses, ADRs and diaries citing the guide keep
citing it (the name does not change); citations of a snapshot path resolve in git
history and are never rewritten. A secret already committed stays in history: the agent
says so; purging is the user's. Extracting claims afterwards is a normal ingestion.

**FS9 — ingestion step.** kb's ingestion step runs `corpus` beside `graph` and fixes
credential errors before its save commit.

Acceptance criteria:
- AC1 (P1) `db.password=<value>` in `given/` fails `check` and `corpus`; the output names
  line and kind and does not contain the value.
- AC2 (P2) redacted and declared: passes.
- AC3 `credential_scan: reviewed — <reason>` clears it; `skip` or a reason-less value does not.
- AC4 the flagged and not-flagged lines of FS2, as a table.
- AC5 a document-guide snapshot with a credential fails `check`; a code-guide snapshot
  does not; the guide-frontmatter escape clears it.
- AC6 tombstone without bytes or `sha256:` passes; with bytes or `sha256:` errors; a
  successor's `supersedes:` naming it raises no warning; export and the docs site skip
  it; the index row says withdrawn.
- AC4b `check` prints each credential error once (kb, code, mkt — mkt also on a tree
  with no corpus, snapshots only); `validate` prints none.
- AC7 (P3) same text in `.sources/` and `given/`, LF or CRLF: one warning naming both.
- AC8 (P4) `adopt` lists guide, snapshot, credential line; tree byte-identical; code
  guides counted; outside pointer not read; no docs root exits 1.
- AC9 (P5) `original_ref:` silent; a URI in `original_path:` names `original_ref:`; a
  Windows drive path does not.
- AC10 (B1/B2) guide on a `given/` artifact with LF-normalized `source_hash`: clean,
  `[stale]` on change, including a CRLF artifact.
- Doctrine (FS1, FS5, FS6, FS8, FS9): one kb eval scenario — an ingestion of a
  `.properties` file — asserting redaction, `redacted_at_intake:`, no `original_sha256:`,
  and `corpus` run before the save commit.

## Interface Contract

Surfaces: `check`/`corpus` output (agent and practitioner at the closure gate and the
ingestion step), the `adopt` command and its output, sidecar and guide frontmatter fields
the agent writes, and kb doctrine (`distillation.md`, `portability.md`, `templates.md`,
`SKILL.md`).

- **Ingesting (UC1, UC6).** Agent (following `distillation.md` §1) → redacts → stores
  artifact + sidecar → runs `corpus` (FS9) → validator scans and returns clean or
  `[ERROR]`. Idiom reused: request-record marker and redaction list; the existing
  `[ERROR] corpus/given/<name>: …` form.
- **Closure (UC2).** Agent runs `check` → knowledge layer scans `given/` and document
  snapshots → `[ERROR] … look like a credential (<kinds>) — redact into a successor and
  withdraw this one (distillation.md §1), or declare credential_scan: reviewed —
  <reason>` (snapshot form: "redact into a new snapshot — its name changes — and
  update the guide's distilled_from, source_hash and markers, or declare … in the
  guide") → summary line, exit 1.
- **Withdrawing (UC3).** Agent writes the successor (`supersedes:`), sets `withdrawn:`
  on the old sidecar, deletes the old bytes, re-places citing claims → `check` clean;
  agent tells the user the bytes remain in git history.
- **Adopting (UC4).** Agent runs `adopt` → knowledge layer reads guides (spine
  enumeration, confined pointers), snapshots, `given/` → inventory, exit 0; "outside the
  project root — not read" for an escaping pointer; `[ERROR] no docs root` exit 1.
  Idiom reused: `migrate` / `import --dry-run` "nothing was written".
- **Upkeep (UC5).** `[warn] reference/.sources/<a> and corpus/given/<b> hold the same
  text — one home per source text: re-point the guide (portability.md §6, kb-agentic)`.
- **Recording the original (FS4).** Agent writes `original_ref:`; nothing printed.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| hash raw / line-ending-normalized | EXISTS | `knowledge.kb_sha256_bytes`, `sdlc_core.sha256_file` | re-read both |
| enumerate guides with frontmatter | EXISTS | `sdlc_core.list_guides` | used by `cmd_stale`, `cmd_validate` |
| confine a guide pointer | EXISTS | `sdlc_core.confine_under` | `cmd_validate` guide check (c) |
| read sidecars, resolve `original_path` | EXISTS | `load_frontmatter`, `kb_unquote`, `_kb_original_candidates` | `kb_corpus_check` |
| ship only cited, existing artifacts | EXISTS | `kb_export_closure` (`is_file` per candidate) | re-read |
| find credential-shaped lines without echoing values | MISSING | — | grep `secret\|credential\|password\|redact` over `sdlc_core.py`, `knowledge.py`, kb `*.md`: request-record prose only |
| report document guides resting on snapshots, read-only | MISSING | — | `migrate` moves the docs root; `import` reads bundles |

New components:
- `kb_credential_findings(path) -> [(line_no, kind)]` — FS2's shapes over one file;
  `[]` for binary or unreadable; never returns a value; streams lines.
- `kb_credential_errors(root, docs) -> [str]` — the FS2 errors over `given/` and document
  snapshots, escapes applied; one carrier per command (Impact).
- `kb_cmd_adopt(root, docs) -> int` — FS7; reads only.
- Helpers: `kb_credential_line_kind(line)` (one line → kind or None),
  `kb_is_tombstone(meta)`, `_kb_same_text_warnings(docs)`, `_kb_mask_userinfo(text)`.

Guides: `GUIDE_skill_family_changes.md` (read) — `knowledge.py` counts once.
`GUIDE_shared_project_memory.md` (read) — the corpus section rides `check` after the
spine banner; the new snapshot scan rides `extra_validate`, so it runs on trees with no
corpus too; no guide is due (short linear functions).

## Impact

`knowledge.py`, `docs_site.py` and `guides.md` are shared verbatim by
`skills/agentic-sdlc-skill/` and the three `distributions/*/skills/*/`: changed once,
copied, `shared_files.py --update` ×4.

| Path | Change | Trace |
|---|---|---|
| `scripts/knowledge.py` (×4) | MODIFY | FS2 `kb_credential_findings`, `kb_credential_errors`; one carrier per command: `kb_cmd_check`'s extra_validate (code, kb, course `check`), `kb_validate_surface(full=True)` outside its `topics/`/`corpus/` guard (mkt `check`, corpus-less trees included), `main` `corpus` branch — never `kb_corpus_check` itself, so `check` prints each error once and `validate` none; FS3 tombstones in `kb_corpus_check` (no-bytes accepted, bytes/`sha256:` refused, `supersedes:` to a tombstone accepted), `kb_build_corpus_index` (`withdrawn` row), `kb_export_closure` (skips tombstone sidecars); FS4 URI hint; FS6 one-home warning in `kb_corpus_check`; FS7 `kb_cmd_adopt`, `INTERCEPTED`, parser, help |
| `scripts/docs_site.py` (×4) | MODIFY | FS3: sources built from `given/*.meta.md` skip tombstones |
| `guides.md` (×4) | MODIFY | §2 step 3: a document snapshot is verbatim except credentials and unneeded personal/confidential data, replaced by `[REDACTED: <kind>]`, the kinds listed in the guide's frontmatter `redacted_at_intake:` |
| `scripts/shared_manifest.json` (×4) | REGENERATE | copies |
| kb `distillation.md` | MODIFY | §1 FS1, FS2 limits, FS3, FS4, FS6 (override of `guides.md` snapshot steps for document guides with a corpus); §4 FS5 |
| kb `portability.md` | MODIFY | §6 FS8; §5 adoption L3; §2 withdrawn artifacts are not exported |
| kb `templates.md` | MODIFY | sidecar fields `redacted_at_intake:`, `credential_scan:`, `withdrawn:`, `original_ref:`; `original_sha256:` absent when redacted; guide template note (document guide on a `given/` artifact with a corpus) |
| kb `SKILL.md` | MODIFY | :18 `portability.md` description (adoption); :27 command list `adopt`; :75 ingestion step runs `corpus` (FS9); :103 Write Trigger row (redaction, no copy beside a redacted extraction, "never edited" except withdrawal) |
| code `templates.md` | — | unchanged: `.sources/` stays the book where there is no corpus |
| `mkt_check.py` | MODIFY | epilog shared-commands list gains `adopt` |
| kb `evals/` | ADD/MODIFY | FS1/FS9 ingestion scenario |
| kb `scripts/test_kb_intake.py` | ADD | AC1–AC10 |
| kb `README.md`, `CHANGELOG.md` ×4 | MODIFY | command list; notes (the check reaches every lens) |
| `ai_docs/strategic/architecture.md` | MODIFY | Component Map: Corpus store row ("verbatim, redacted at intake; withdrawal"), new components |
| `ai_docs/strategic/skill_family_agent_workflows.md` | CHECK | updated where it describes intake or guide snapshots |
| `ai_docs/vision/rulings.md` | MODIFY | r35a–c |
| `ai_docs/solutions/harness_kb_intake_hygiene/probe.py` | ADD | probes (P3 wording aligned with FS6's message) |

Blast radius (grep over `*.py`, all five copies):
- `kb_corpus_check` — `kb_cmd_corpus` (← `kb_cmd_check` section, `kb_validate_surface`
  full, `main corpus`), `harness_kb_graph_only/probe.py` via `kb_cmd_corpus`, and
  `test_claim_ledger.py` directly (≈11 sites). Signature and return shape unchanged;
  new findings only. Fixtures grepped: no credential-shaped body in any kb test fixture.
- `kb_cmd_check` / `kb_validate_surface` — every lens's `check`/`validate` (code and kb
  entry, course for validate/check, mkt's validate/check through `kb_validate_surface`).
  New errors only on trees with credential lines.
- `kb_build_corpus_index` — `kb_refresh_indexes`, `_kb_extra_validate` (freshness); a
  withdrawn row changes only indexes that have withdrawn sidecars.
- `INTERCEPTED` / `main` — `adopt` reaches code, kb, course and mkt entry points.

Populations at rest (triggers: none of the four fires mechanically; the check reaches
data written before it, so the table is written):

| Existing population | Regime | After | Who sees it |
|---|---|---|---|
| `given/` artifacts with credential lines | none | `check` error until withdrawn behind a redacted successor, or reviewed | the practitioner, next `check` (CI included) |
| document-guide snapshots with credential lines | none | same; fix = redacted snapshot + `source_hash`, or reviewed | same, every lens |
| sidecars with `original_sha256:` of a redacted original | n/a (no rule) | none exist: redaction is new | — |
| `.sources/` + `given/` holding the same text | none | warning | same |
| sidecars with a URI in `original_path:` | "does not resolve" warning | same warning, names `original_ref:` | same |
| secrets in git history | none | unchanged; stated to the user | the user |

## Security and Threat Model

Surfaces: reading untrusted files (`given/`, snapshots, frontmatter); findings printed
into logs and CI; paths from guide frontmatter; what intake stores.

- **T1 disclosure through the validator's output** → `kb_credential_findings` returns
  numbers and kinds only (AC1, AC8 assert the value is absent).
- **T2 offline guessing from a digest** — `original_sha256:` of an unredacted original
  beside its redacted extraction lets anyone with the repo test password guesses →
  FS1: no digest of unredacted bytes when redaction happened; FS3: a tombstone keeps
  no `sha256:` and loses the `hash8` name.
- **T3 secret kept beside its redacted extraction** — a binary original copied beside →
  FS1: not copied when redaction happened.
- **T4 secret committed before any scan** — the ingestion step's save commit → FS9.
- **T5 secret that cannot be removed** → FS3 withdrawal; history residual (T9).
- **T6 resource exhaustion** → streamed lines, 4,096 characters per line, linear
  patterns; the one-home check hashes `.sources/` files and LF-normalizes `given/`
  files whose size is within a factor of two of some snapshot's (a size prefilter;
  CRLF at most doubles a text), reading each once.
- **T7 path escape in `adopt`** → `confine_under`; escaping pointer not read (AC8).
- **T8 false positives / abuse of the escape** → explicit `reviewed — <reason>`, visible
  in the diff; reason-less values refused (AC3).
- **T9 residuals**: shape matching misses FS2's declared false negatives — the
  redaction duty is the rule, the check the backstop; secrets already in git history;
  personal data is never detected.
- **T10 zero writes in `adopt`** → no file opened for writing (AC8).
- **T11 symlinks in `given/` and `.sources/`** are followed by the scan, the
  same-text check and `adopt`, as the digest check already does: they print only line
  numbers, kinds and names. Declared residual; the pointers in guide frontmatter stay
  confined (T7).
- **T12 a password in a URL echoed by an existing warning** (`original_path:`) →
  masked (`***`).

## Ceremony disclosure

- Every `check` (every lens) on a tree with `given/` or document guides: one scan of
  those files, I/O comparable to the digest check already run. No new command.
- A project whose stored sources hold credential lines: `check` fails until each is
  withdrawn/redacted or reviewed — once per file, including in CI on an L1 change.
- A false positive: one frontmatter line.
- Intake (kb L3 ingestion, step): one redaction pass; one sidecar field when something
  was replaced; `corpus` run in the step (FS9).
- Adoption: one-off, L3, opt-in.
- Read cost, measured (UTF-8 LF bytes; estimate accepted in R8 in brackets): kb
  `distillation.md` +3,717 [2.8 KB], `portability.md` +1,947 [2.2 KB] (read on
  adoption/export), kb `templates.md` +1,177 [0.8 KB], kb `SKILL.md` +453 [0.4 KB],
  shared `guides.md` +486 [0.4 KB] (every lens, read when creating a guide). Total
  +7,780 against an estimated 6,600, accepted by the owner (R10).
- L1/L2 add no step, field or check of their own; the only L1 exposure is the at-rest
  failure above.

## Action Plan

- [x] Owner: cost acceptance and r35 ADMIT (mandated, after the design review).
- [x] RED: `test_kb_intake.py` AC1–AC10 (probe red: done).
- [x] `kb_credential_findings`, `kb_credential_errors`, wiring; withdrawn; URI hint; one-home.
- [x] `kb_cmd_adopt`, `INTERCEPTED`, parser, help; mkt epilog.
- [x] Doctrine: `distillation.md`, `portability.md`, kb `templates.md`, kb `SKILL.md`; eval.
- [x] Copy `knowledge.py` ×4; `shared_files.py --update` ×4.
- [x] Component Map, workflows doc, README, CHANGELOG ×4, rulings r35.
- [x] GREEN: four batteries, probe; E2E_TEST, closure review, MERGE_REVIEW; `check` CLEAN.

## Test Strategy

`test_kb_intake.py` (kb-only, like `test_claim_ledger.py`) covers AC1–AC10 through the
kb entry point and `knowledge.kb_credential_findings` directly; AC5 also through the
code entry point (the check reaches every lens). The kb eval scenario covers the
doctrine criteria. The probe replays P1–P5, B1–B2. Four batteries
(`python -m unittest discover -s <scripts> -p "test_*.py"`).

## Diary

**2026-10-23 — analysis drafted.** Probe: B1/B2 GREEN, P1/P3/P4 RED. R3: error with a
reviewed escape. R4: language rule.

**2026-10-23 — design review.** PASS in round 3 (REVIEW_LOG); owner R5–R7 settled
withdrawal, snapshot scanning and personal data. Next: owner cost acceptance and r35.

**2026-10-23 — implemented.** R8/R9: cost accepted, r35a–c ADMIT. RED (test_kb_intake.py,
45 red), then GREEN: batteries code 420, kb 633, mkt 422, course 415 OK; probe green on
all twelve lines, including P6 (snapshot flagged once by the code, kb and marketing
`check` on a tree with no corpus). Read cost measured at +7,500 bytes against 6,600
estimated (Ceremony disclosure). Next: closure review.

**2026-10-23 — closed.** Closure review FAIL → PASS in two rounds (REVIEW_LOG); the
post-PASS URL-masking fold is covered by a test. Owner R10 accepted the measured read
cost (+7,780). Batteries code 420, kb 642, mkt 422, course 415 OK; probe 12/12 GREEN.
Release follows the family's release guide; the CHANGELOG sections stay `[Unreleased]`.

**2026-10-23 — merged with main.** Main already held F-075, F-076, F-078 and F-080; F-076
had taken r34, so this unit's rows became r35a–c (the request record and the review log
keep the earlier names). CHANGELOG sections and the Component Map were unioned; the
shared files and their manifests regenerated identical in all four locations.
