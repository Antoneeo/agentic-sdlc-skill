# Changelog - KB Agentic Skill

Every significant change to this skill is recorded here.

## [Unreleased]

F-039 — the recall reflex (second-brain unit 1): the graph is read when answering,
not only written when distilling.

### Added
- **`SKILL.md` §Topic Recall — the answer-side consult.** Whenever a reply would
  assert facts about the project's domain, the topic index is scanned and the descent
  (`taxonomy.md` §6, new) runs in answer mode — plausibility of coverage is judged ON
  the scanned index, never before it. Four declared verdicts (claims cited / node
  matched no claims, surfacing `gaps:` / no coverage / index absent + regenerate),
  emitted only when the recall ran; never faked. Once per topic per session.
- **The anti-echo re-touch rule.** A DERIVED claim that grounds a decision has its
  chain walked to non-DERIVED ground (GIVEN artifact, ELICITED or RULING note) and
  that ground cited; an unresolvable ground marks the claim unverified for
  decision-grounding — surfaced, never silently cited. IMPORTED grounding a decision
  is named as un-re-ratified foreign authority.
- **By construction: kb `orient` appends the topic router.** The overlay special-cases
  `orient` (raw argv forwarded to the spine, never re-parsed) and appends the top of
  `topics/INDEX.md` — or `index absent (N node files)` with the regenerate command —
  so every session opens with the graph in sight. Fails open; spine untouched.
- **`test_kb_recall.py`** — new kb-only battery module (doctrine anchors + orient
  interception), deliberately outside the shared x3 manifest.
- **`run_behavioral.py` fenced-block seeding** — a scenario setup entry ending in `|`
  takes its file body from the following fenced block (common-dedented), so claims
  tables and frontmatter'd nodes can be seeded; one-line entries unchanged.
- Eval scenario `recall_descends_before_answering.md`.

## [1.6.0] - 2026-08-26

F-038 — the gated rung: truthful log vocabulary and a mandated ask, no grant memory.

### Fixed
- **A review rung that exists behind a permission policy is no longer logged as
  "unavailable".** The ladder knew two states (the client supports the rung, or not)
  and hard-coded rung 3's reason as "no subagent facility on this client" — so a gated
  facility produced false log rows, and the ladder's own prohibition ("rung 3 is
  illegitimate wherever rung 1 or 2 exists") was unsatisfiable on a gated client: the
  agent could not obey it without asking, and no rule said to ask.

### Added
- **The gated-rung stop.** At a due review gate (design; closure), when the best rung is
  permission-gated (a standing policy — an interactive per-call prompt is NOT this) and
  no ungated rung works (a working one-shot CLI pre-empts the stop; a gated rung 2 joins
  the question instead), the gate stops and asks ONE question in the five-bullet blocking
  form: the gated rung(s) vs the fallback, each higher rung's status, the quoted policy,
  the cost (~130-175k subagent tokens per deep review, measured 2026-08) AND what
  independence last bought, and what stays blocked. **No grant memory**: the answer holds
  while the conversation does; an agent that cannot recall a grant asks again. Unattended
  runs never emit the question — rung 2 is still owed a try, then rung 3 with its reason.
  (Successor to a design CANCELLED at the review cap after grant memory failed three
  ways; rulings r18/r19.)
- **The reason words.** A below-rung-1 row says why the rung(s) above did not run:
  `absent` (the client has no such facility — a claim about the client, never a policy),
  `gated, declined`, `gated, unattended`, `gated, pre-empted` (nothing asked — an
  ungated lower rung ran the review). A rung-1 row owes nothing. For rung 3 this
  re-words an existing duty; for rung 2 it is a new one-word duty, disclosed and
  accepted with the rest.

## [1.5.1] - 2026-08-25

### Fixed
- **The three README front pages did not mention the hook wiring that 1.27.0 added.**
  `init` now changes what every project gets, and the README *is* the npm page, so two
  of the three said nothing about it and the third barely did. Each now describes the
  wiring, the settings.json / settings.local.json split and why it exists, and the
  broken-hook report. `GUIDE_release.md` step 2 already made this a release duty; it was
  skipped in 1.27.0 and this is the catch-up.
- **`publish_all.bat`'s verify block reported the previous version after a successful
  publish — twice.** `--prefer-online` (added in kb 1.4.8) forces revalidation but cannot
  outrun CDN propagation of the `latest` tag in the seconds after publishing, so the
  1.27.0 run printed mkt `0.4.7` when `0.5.0` had in fact landed. The flag alone was the
  wrong fix and the note claiming otherwise is corrected: the block now **polls** each
  package until the registry agrees with the local version, and prints both when it does
  not, so "did it publish?" is answerable from the run instead of a manual `npm view`.

## [1.5.0] - 2026-08-25

F-036 — the orientation hook installs itself.

### Fixed
- **`ENFORCEMENT.md` 4 said "wire it on every project" and nothing ever did.** The
  SessionStart orientation hook was real, tested and fail-open, but installing it was a
  manual step, so it was skipped — and a session that never enters Phase 1 explicitly
  then never meets the guide router at all. Field result: an agent worked a governed
  project without invoking the process. `init` now wires the hook itself.
- **The invariant that looked like it guarded this guarded only prose** — it asserted
  the documentation section exists (`assertIn("## 4. SessionStart hook", t)`) and that
  `orient` runs. It gains a companion asserting the shipped installer actually CALLS the
  writer. Mutation-tested: the first draft asserted the bare symbol and passed on a file
  that imports the writer without invoking it, which is exactly the disabled-installer
  case it exists to catch.

### Fixed (also)
- **ENFORCEMENT 4/2's own worked hook examples named a skill directory that two of
  the three lenses do not install.** kb and mkt both printed
  `.claude/skills/agentic-sdlc/scripts/...`; kb installs under `kb-agentic` and mkt
  under `mkt-agentic-sdlc`, so anyone who copied the snippet got a hook that runs,
  prints `can't open file`, and emits nothing — the wired-and-dead defect this release
  detects, sitting in the instructions that produce it. Four paths corrected, and a new
  invariant derives the expected directory and validator from what the distribution
  actually ships and fails if an example names anything else. Mutation-tested.

### Added
- **A portability rule the doctrine did not have.** The hook command names a validator,
  and where that validator lives decides which settings file may carry it: a repo that
  vendors the validator gets a repo-relative command in the shared, committed
  `.claude/settings.json`; a normal project gets an absolute path, which goes to the
  git-ignored `.claude/settings.local.json` instead — committing it would hand every
  teammate a hook naming a directory they do not have. `init` picks the file and adds
  the local one to `.gitignore`. ENFORCEMENT 4's own worked example showed an absolute
  path and did not mention the distinction; it now does.
- **A wired-but-dead hook is detected and reported instead of counted as done.** Found
  in the field: a repository whose hook named a sibling lens's path, so it ran every
  session, printed `can't open file`, and emitted nothing. A bare "is a hook present?"
  check answers "already wired" to that and makes the silence permanent, so the existing
  command's validator path is checked on disk. Never rewritten — it may be hand-tuned —
  but never passed off as working either.

### Notes
- `init` declines rather than guessing: no Python, skill not installed, a settings file
  that is not valid JSON (never rewritten — a merge would discard what is in it), or a
  skill path containing a double quote. Each case prints the snippet to paste.
- Only Claude Code's hook shape is wired. Codex and Gemini keep the manual snippet: this
  repository has no fixture pinning their schema, and writing a hook file in a shape
  nobody has verified is how the wired-but-dead defect above was born.
- A blocking `PreToolUse` gate would be real enforcement rather than a nudge, and it is
  refused by the Vision's no-ceremony-ratchet Non-Goal. Recorded in the analysis so the
  next person to have the idea finds the ruling instead of re-deriving it.

## [1.4.8] - 2026-08-25

F-035 — second field report from the F-029 practitioner. Three defects in the corpus
letter's own enforcement: the promise is that every provenance is a real file, and two
of the three mechanisms that should hold it did not run.

### Fixed
- **`prov:` below `GIVEN` was structurally impossible for any claim citing
  `corpus/given/`.** `_note_frontmatter` read frontmatter from the cited file itself. A
  corpus artifact is bytes and carries none — but it *is* a file, so the helper returned
  `{}` rather than `None`, which the caller cannot tell apart from "resolved, field
  absent", and the required-field error fired unconditionally. `DERIVED`, `RULING` and
  `IMPORTED` were unreachable on any `given/` artifact, so every such claim was forced
  to `GIVEN` whatever its real extraction chain. The helper now reads the artifact's
  `.meta.md` **sidecar** when one exists and the cited file otherwise — sidecar-first,
  not "non-`.md`", so a verbatim `.md` source stored in `given/` resolves the same way
  as a `.txt` extraction while a `corpus/notes/*.md` note still resolves to its own
  frontmatter. It also returns the path it actually read, and the three findings now
  name that file instead of saying "note" about a sidecar.
- **`original_path:` was never verified.** Zero reads of it in either script: a folder
  of originals could be moved and sixteen sidecars go dangling behind a green run. It is
  now checked for resolution — a **warning**, never an error, because a bundle carries
  artifacts and sidecars and never the originals, so after an import it dangles
  legitimately. Absolute paths are tested as written; a relative one is tried against
  the docs root's parent and against the docs root, and warns only if neither resolves.
  `original_sha256` stays unverified for the reason already stated — we do not hold the
  bytes — and `distillation.md` now states the two limits separately, because they were
  never in the same position.
- **The duplicate-id error named the wrong defect.** "uniqueness is global across
  topics/" describes a copied row; the reporter's two rows were hand-written and
  different, and had collided in `kb_claim_id`, which hashes `path#locator#qty` and
  excludes the text on purpose. The check now branches on the **claim text** — same text
  is a copied row, different text is the collision — and the collision message explains
  why the id cannot separate them and prescribes the two legitimate repairs (widen a
  locator, or merge the rows), explicitly ruling out editing the qty to break the tie.
  The id function itself is unchanged and its two constants are now pinned by tests:
  `portability.md`'s cross-project de-duplication rests on them
  (`ADR_2026-08-25_claim_id_collision.md`).

### Added
- **A `GIVEN` row whose artifact declares a weaker chain now warns.** `provenance:` was
  written into every sidecar and read by nothing; this is its first consumer. A
  conformant corpus (`provenance: GIVEN`, or no field) is silent. **Scope, stated so it
  is not mistaken for more:** it reads the row's first source and it reads the *field* —
  a sidecar declaring `provenance: GIVEN` while its prose says "transcribed from a
  photograph" stays silent, because prose is not machine-readable. The pair's larger
  half is the fix above, which is what makes the honest declaration possible at all.

### Fixed (second review round)
- **`original_path` classification was wrong on Windows, and the documented example was
  the trigger.** `Path.is_absolute()` is False for a rooted-but-driveless path — exactly
  the `/vault/manuals/xyz.pdf` form these templates print — so it was joined under the
  docs root and silently rewritten onto the docs root's *drive*. That produced a warning
  quoting a path nobody wrote (twice, since both candidates collapsed to it), could hide
  a genuinely dangling pointer behind whatever happened to sit there, and warned falsely
  whenever the corpus and the original lived on different drives. Rootedness is now
  decided by `ntpath`/`posixpath`, the candidate list is de-duplicated, and the
  backslash normalisation is an *additional* candidate rather than a rewrite (a
  backslash is a legal character in a POSIX filename).
- **The pointer probe could crash the run.** `Path.exists()` re-raises `PermissionError`
  and `ENAMETOOLONG`; `original_path` points outside the docs root by design, so the
  validator must survive whatever is out there. It is now `is_file()` (a directory is not
  a document) inside an `OSError` guard.
- **`_note_frontmatter` could read one file outside the docs root.** A source cell of
  the form `#L1-2` — no path before the locator — made `confine_under` return the docs
  root itself, and the sidecar name was then built from `base.parent`, i.e.
  `<docs-root>.meta.md`. Both that case and a sidecar orphaned by a deleted artifact now
  return "unresolved", which the source loop already reports.
- **The collision message asserted something it had not checked.** It claimed the two
  rows "cite the same span with the same qty" — true only for a *computed* id. Two rows
  sharing a hand-typed or stale id while citing different spans now get their own
  message, naming the real repair (`claim-id --fill`).
- Frontmatter resolution is memoized per cited path: it now runs for every row, `GIVEN`
  included, and a ledger citing one artifact from eighty rows was re-reading its sidecar
  eighty times.
- The worked sidecar example carried trailing `# comment`s. The frontmatter reader is a
  line regex and does not strip them, so the comment landed inside the value — harmless
  while nothing read `original_path`, and a guaranteed false warning once something did.

### Known limits, stated
- `ELICITED` is accepted with **no required field at all** — it is named in the
  provenance branch but has no check below it. Found while fixing the above, deliberately
  not repaired here: adding one is a new gate, not a repair.
- `corpus` and `graph` still have no `--errors-only`; on a corpus with many in-progress
  artifacts the coverage warnings bury a lone error. Ranked last by the reporter.

## [1.4.7] - 2026-08-06

### Fixed
- **Shared-spine sync: the scoped re-review contradicted `dispatch.md` (ACTIVE in this lens).**
  `dispatch.md` said "exactly three review touches per task, never a loop" while `review.md`
  required every review-driven correction to be re-reviewed. Reconciled: the scoped re-review is
  a round inside slot 2 or 3, never a fourth slot. Also in the shared `review.md`: an unproven or
  stale completion claim is now a reviewer finding; a PASS carrying findings is provisional until
  its corrections pass a round; the single log row keeps the round-1 verdict (`FAIL → PASS`).
  Found by the code lens's late design review of F-034.

## [1.4.6] - 2026-08-06

### Changed
- **Shared-spine sync: review-driven corrections + reviewer honesty (ACTIVE in this lens).**
  The shared `review.md` gains the scoped re-review discipline — a fix made in response to a
  finding is unreviewed work and gets a correction-scoped re-review with per-finding verdicts
  before PASS — plus the `CANNOT VERIFY` reporting duty and the no-pre-judging rule. Unlike
  prior spine syncs these are NOT inert here: reviews of knowledge artifacts inherit the
  correction discipline directly.

## [1.4.5] - 2026-08-06

### Changed
- **Shared-spine sync: Functional Spec clause (inert in this lens).** The shared
  `review.md` gains the code lens's Functional Spec findings (absence on behavior change,
  Solution-leakage inside the spec, uncovered cases, acceptance criteria without tests).
  The kb lens defines no `## Functional Spec` template section, so the clause stays inert
  here — spine parity only.

## [1.4.4] - 2026-08-05

### Changed
- **Shared-spine sync: use-case grounding clause (inert in this lens).** The shared `review.md`
  gains the code lens's use-case-grounding finding — a product name in no EXISTS/NEW/METAPHOR
  bucket, or a use-case tracing to no Vision benefit. The kb lens defines no `## Use Cases`
  template section, so the clause stays inert here — spine parity only.

## [1.4.3] - 2026-08-05

### Changed
- **Shared-spine sync: Interface Contract rename (inert in this lens).** The shared `review.md`
  Interaction Contract clause is renamed to **Interface Contract** and gains the code lens's
  evolved checks (responsibility-level flow, solution-leakage, universal feedback); the
  `interaction_contract` capability key is unchanged. The kb lens defines no such template
  section, so the clause stays inert here — spine parity only.

## [1.4.2] - 2026-08-05

### Fixed
- **Registry recognition hard-coded to one entry point.** The workstream-registry
  header is written with `entry_script()` but was recognized as "already ours" only
  by the literal `sdlc_check.py`; recognition now matches the generated marker for
  any family entry point — relevant on mixed-lens projects.
- **Spine battery isolation.** `test_merge_safety` now pins its docs root in
  `setUpModule` instead of inheriting whichever overlay was imported first by
  unittest discovery.

### Changed
- **Shared-spine sync with code 1.22.0 (Interaction Contract, F-032).** The shared
  `review.md` gains the Interaction Contract conformance clause and the shared core
  registers the `interaction_contract` capability — both **inert in this lens**: the
  clause is keyed on the lens whose template defines the section (the code lens),
  kb claims no such capability, and no kb workflow gains any new step or artifact.

## [1.4.1] - 2026-08-03

### Added
- **`version:` in every `SKILL.md` frontmatter.** An installed skill carries no
  `package.json` and no `gemini-extension.json` — only doctrine and scripts — so nothing
  in it said which build it was. Answering "is that fix in your copy?" took `npm view`
  plus a shasum comparison; from a user's side it was unanswerable. Now the first thing
  in the operating contract says it.
- **A battery invariant asserting every bump point agrees** (`SKILL.md` ↔ `package.json`
  ↔ `gemini-extension.json`). A hand-maintained version string rots, and this repository
  has the scar: the third bump point was skipped for two whole releases with nothing to
  catch it. The fourth arrives with its guard attached, and `GUIDE_release.md` step 1
  now says FOUR.

## [1.4.0] - 2026-08-03

F-028 — several people on one project. `templates.md` had claimed the workstream
registry was "Parallel-safe by construction" since F-019, and nothing had ever exercised
it. Two workstreams opened from one base conflict **twice in one file**: on the row
insert, and on the file-global `Date:` header. Row-level ownership cannot save a file
that has a file-level field.

### Changed
- **`audit/handoff.md` is now GENERATED** from one `HANDOFF_[unit].md` per open
  workstream, whose frontmatter IS the row. Two writers on two workstreams touch two
  different files, and the `Date:` header is derived — from the newest `updated:` VALUE
  in the sources, never a filesystem timestamp (git does not preserve mtimes, and an
  mtime-derived header would make the file regenerate differently in every fresh clone).
- **`HANDOFF_[unit].md` is now written for every OPEN workstream**, with or without
  volatile state — no file, no row. It still carries the resume logistics, and deleting
  it at closure *is* what removes the row. The DRY boundary against the ANALYSIS Diary
  is restated in the template, because what used to keep narrative out of that file was
  its rarity, and the rarity is gone.
- Project-wide notes move to their own source, `audit/project_notes.md`, so generating
  the registry cannot destroy notes that belong to no workstream.

### Added
- **`validate` errors when the registry disagrees with its sources** — which is what
  turns a merge resolved carelessly from permanent into loud. Resolution is mechanical:
  re-run `index`. The generated view can still conflict; the authored truth does not.
- **`index` refuses to write while anything in the file is unaccounted for**, and names
  it. Converting one row at a time is the state that loses the others, so conversion is
  per project. A project with no sources is untouched and sees no new finding.
- **`init` writes a `.gitattributes` stanza** giving the append-only review log
  `merge=union` — a **built-in** driver, unlike `merge=ours`, which silently does
  nothing until every clone runs `git config` and leaves the file wrong even then.
  Create-only; a user's own `.gitattributes` is never clobbered.
- `scripts/test_merge_safety.py` (shared, ×3): the experiment that found the defect,
  kept as a regression test — two workstreams from one base, merged, with the assertion
  that only the generated view may conflict and that regenerating loses no state. Plus
  the mixed-state, fresh-mtime, ordering, cap and duplicate-id guards, each
  mutation-verified.
- A warning when two files claim the same workstream: the collision this design does
  **not** fix (two people opening the same work under two names) must not pass as two
  ordinary rows.

The mechanism is files and a generator: **it works with no VCS at all.** The
`.gitattributes` stanza is defence in depth — without it the outcome is today's, one
conflict resolved by hand, never a lost row.

### Upgrading
Nothing happens until you convert: with no `HANDOFF_*.md` sources, `index` and
`validate` behave exactly as before. When you convert, convert the whole registry at
once — `index` will tell you what is still unaccounted for.

## [1.3.0] - 2026-08-03

Field defect: an agent handed a 200-page manual emits a few dozen claims and reports
done. **Nothing it did broke a rule** — the extraction discipline carried a floor ("the
extractor invents nothing") and no target, so an agent stops the moment nothing it wrote
is false, and every row it emitted is correct.

### Added
- **A north star above the rules** in `distillation.md`: *not one assertion the source
  makes may be lost, and not one it does not make may appear.* One sentence on purpose —
  the halves counterweight each other, and two rules a paragraph apart get optimized
  whichever was read last. The unit is the assertion, not the byte: exhaustive means
  **read**, never *a row per page*.
- **`extracted_through:`** on the artifact's sidecar (`p=<n>`, `L<n>`, `complete`),
  required once any claim cites it — the thing that makes "I am finished" falsifiable.
  Claims with no coverage recorded error; a claim addressing past the declared coverage,
  or coverage past the end of the stored bytes, is a contradiction and errors; coverage
  short of the end warns, since partial work is legal mid-ingestion.
- **Bounded reading windows** (30 pages by default; the plan states the window used),
  one plan task each. The existing `PLAN_` ledger is the register an ingestion resumes
  from across sessions — no second register was built.
- **A coverage cell in `corpus/INDEX.md` for every artifact**, finished ones included: a
  list of only what is behind would be the work-management dashboard this method refuses.

The limit is written where the field is: **nothing proves a page was read.** A field
advanced without extracting is invisible to any checker, because a page that asserts
nothing legitimately yields no rows — that direction belongs to the ingestion review.
What changed is that the shortcut must be written down to pass.

**Upgrading an existing corpus:** `check` errors on every artifact that has claims and
no `extracted_through:`. State how far each source was actually read (`complete` if it
was finished); the message names the artifact and the first row citing it. Run
`sdlc_check.py index` once as well — `corpus/INDEX.md` gains the coverage cell.

## [1.2.0] - 2026-08-03

### Added
- **`export --out <dir>` / `import <dir>`** — knowledge built in one project can be
  carried into another. The export is a **closure**, not a selection: the bundle carries
  the bytes its claims cite (a claim whose source cannot be reopened is model knowledge
  arriving by another route) and pulls in the other half of any `CONTESTED` set, saying
  which topics it added. The import is **additive and all-or-nothing**: it never
  overwrites a node, never deletes, and computes the whole plan before writing a byte.
  Duplicate claims are recognised by id, not by comparing text.
- **`prov: IMPORTED`.** Knowledge crosses the project boundary; authority does not. An
  imported ruling keeps its text, span and original `basis:` verbatim, must declare
  `imported_from:`, and **cannot supersede a local row** until you re-ratify it with your
  own note and your own basis.
- **`portability.md`** — the doctrine those two commands cite, including what to tell the
  user in their own words.

## [1.1.1] - 2026-08-03

### Fixed
Three doctrine-vs-machinery inconsistencies found by a practitioner reading 1.1.0 —
the worst defect class, because the agent verifies and is confirmed in a false belief.
- `SKILL.md` never named `anchor`, so the command existed and the agent could not find it.
- The `corpus/given/*` Write Trigger still carried its pre-1.1.0 wording, contradicting
  the extraction-as-artifact rule it points at.
- `anchor` resolved paths only from inside the docs root, unlike every sibling command.

## [1.1.0] - 2026-08-03

### Fixed / Added
Six findings from the first full application of this skill by a practitioner other than
its author (51 artifacts, 82 claims). None was an adherence failure: the agent obeyed
every rule and the outcome was still wrong.
- **Triage restated in knowledge units.** The levels were undecidable in this domain
  because they carried the code lens's file counts. The unit here is knowledge, never
  file count — with one limit: propagation that changes what a claim asserts is not
  propagation.
- **Gates are extracted alongside powers.** For every row saying what the subject *can
  do*, the source is asked what must hold first — default-off, licence tier, version
  floor, dependency — because "yes, supported" without the gate is a plan that fails on
  site. The rule stays *ask*, never *produce*.
- **`anchor <path> <phrase>`** turns a quoted phrase into a verified locator, matching
  whitespace as `\s+` because a PDF extraction breaks phrases mid-line — the gap that
  cost a field user two generation rounds.
- **Extraction-as-artifact** for large binary corpora: the extraction is the artifact,
  the digest moves onto the bytes locators actually address, and the original stays where
  it lives as `original_path:` + `original_sha256:` (recorded, never checked — the limit
  is stated wherever the fields are).
- **`--help` lists the overlay commands**, so the ones this lens adds are discoverable
  from the CLI rather than only from the documentation.

## [1.0.1] - 2026-08-02

### Fixed
- **The multi-lens routing note announced this skill as the code lens.** `init.js` wrote
  the row for the CURRENT lens as a hardcoded literal copied from the code distribution,
  so a project initialised with `kb-agentic-init` listed `agentic-sdlc` twice and never
  named `kb-agentic`. Both the self row and the sibling table are now derived from the
  shared `routing.md` lens table; the guarding test asserts this lens is named and is
  mutation-tested against the original defect. Found by a cold-agent field test.
- `review.md` (shared spine): a review verdict travels as the reviewer's final output,
  stated on both the requester's and the reviewer's side.

## [1.0.0] - 2026-08-01

First release of the knowledge lens as its own package: the same spine as
`@antoneeo/agentic-sdlc-skill`, with fidelity to **the documents you supply**.

### Added
- **Content-addressed corpus.** Every source enters verbatim under `corpus/given/`,
  digest-verified; a new version is appended with `supersedes:`, never overwritten.
  Non-text files carry a stored canonical extraction, and locators address those bytes.
- **Claim ledger.** `id | claim | valid | qty | about | source | prov | state`, where the
  id hashes location and quantity — never the text, so an LLM rephrasing mints no new
  identity. Locator spans are verified against the extraction; validity scopes are
  half-open; mixed quantity kinds refuse to sum.
- **Topic graph** with five placement verdicts, polyhierarchy, tombstones with
  `redirect_to:`, cycles refused at write time, unreachable nodes an error.
- **Detect-and-hold reconciliation.** A conflict marks the whole set `CONTESTED`,
  symmetrically — flipping one cell by hand fails the check. Only new information
  resolves it: a later source, or the owner's ruling with a `basis:`.
- `graph`, `corpus` and `claim-id` in the validator, alongside the shared spine.

---

Everything below predates this package: it is the shared spine's history, kept
because the knowledge lens inherits it. Version numbers in that section are the
code lens's.

## [1.19.0] - 2026-07-28 (Design Review Gate)
### Added
- **The design is reviewed before the code exists (F-021).** In Standalone the ANALYSIS was reviewed only as an *input* to the closure review — that is, after implementation. The Vision's Goal 3 names two moments ("make divergence visible **before** implementation, and again before merge"); only the second was implemented. Hybrid had the first (devPNT §4.5 on `E-ISP`/`E-TDD`); Standalone had nothing. Now `review.md` carries **`## When a review is due`** with both moments — **1. design** (end of Phase 3, before any implementation, L3) and **2. closure** (Phase 5, the diff against that design, L2/L3) — plus **1b. late arrival**, for work that became L3 after code existed (an L1/L2 reclassified mid-flight): run moment 1 now, before any further implementation, logged `design (late)`. The reason the moment is its own gate: *the closure review can prove the code matches the design, never that the design was right* — and the author cannot catch what their own design omitted, which is why the gate buys **independence, not effort**. A three-rung ladder makes that concrete on any client: a fresh subagent, a one-shot CLI run (`gemini -p`, `codex exec`) with a self-contained prompt, or — **only where neither exists** — a declared self-pass whose log row must carry *why* the higher rungs were unavailable. Rung 3 stays deliberately: it is what keeps the methodology completable with no network, no account and no subagent facility. Rounds capped at 3, then the findings go to the user; one row per completed review, **PASS or FAIL**, in `ai_docs/audit/reviews/REVIEW_LOG.md` — one schema for both modes, since devPNT's gates write to the same file. New advisory in `sdlc_check.py` (`design_review_due` + `review_logged`) notices an L3 in implementation with no design row: epoch-grandfathered, PLANNED-exempt (the review is due at the *end* of Phase 3, so a design still being drafted is not late), suppressed under `--hybrid` where devPNT owns the slot, and advisory-only as always.
- **Evidence this was needed, from this repository's own log.** `REVIEW_LOG.md` now records the seven independent reviews run during F-020 — **every one at closure**, 72 findings raised, **72 real**, none rejected as noise, and none caught by the author's self-review beforehand. The two rows that opened the sequence were design defects found after the design had already been implemented.

- **Then the closure review ran on the diff and found the cost statement wrong again.** The design review had already forced "3 items → 6"; the closure review measured item 6 and found **255 words** of always-loaded `SKILL.md`, not the restated "~90" — the count had included the Phase-3 paragraph and silently omitted the Write-Triggers row and three ownership-matrix rows, which an agent loads just as unconditionally. Under the Vision's *"Omission resolves against the proposal"* that voids the acceptance, so it was restated from `git diff | wc -w` and re-accepted (Antonio Pinto, 2026-07-28). Twice on one feature the disclosure was written from what felt like the change rather than from what was measured; the acceptance history is kept in the ANALYSIS because the pattern is more instructive than the number. **The hybrid fix also had zero test coverage** — the reviewer proved it by mutation, reverting each of the three `hybrid` forwarding lines and then deleting the advisory outright, all four shipping green; `test_design_review_advisory_end_to_end` now exercises `cmd_validate`/`cmd_check` end to end and all four mutations are caught (re-run to confirm, not assumed). `review_logged` read the `tier` column positionally, so a log with one extra leading column produced a permanent, unclearable false "you skipped the review" — the column is now found by its header — and it matched the ANALYSIS filename as a bare substring, so `ANALYSIS_vision_clarity` would have satisfied `ANALYSIS_vision`'s gate (word-boundary now). `SKILL.md`'s Write-Triggers row still restated three things `review.md` owns and **had already drifted on one of them** in the very commit that fixed the DRY violation; reduced to a pointer. And the eight log rows this release appended carried no `## Notes` — the mechanism it shipped to answer "what did it find" — now written. **Left as a true positive:** `validate` on this repository flags `ANALYSIS_architect_pass.md` as an L3 with no design-review row, because F-020's seven reviews were all at closure — precisely the gap this feature closes. The flagship repo ships with one honest advisory rather than a back-dated row. Battery 75/75.

### Changed
- **The gate ran on its own design and returned FAIL — 3 BLOCK, before shipping.** (1) The independence ladder had an escape hatch: rung 3 was selectable at the agent's discretion with no duty to justify descending to it, so the cheapest path through the gate delivered zero independence while satisfying every word of the doctrine. (2) The declared ceremony cost was **three items of six** — the `conformance_statement`, the reviewer input packet and the per-finding disposition duty were all mandatory and undisclosed; under the Vision's "Omission resolves against the proposal" the recorded acceptance was void, so the cost was restated in full and re-accepted. (3) `cmd_check` never passed `hybrid` to `cmd_validate`, and devPNT's log rows are keyed on `e_isp_`/`e_tdd_` doc_keys, so the new advisory fired **permanently and unfixably on Hybrid projects** — the exact "worst outcome" the feature's own threat model names. Warnings fixed in the same pass: the log row is written on FAIL too (the highest-value review there is); the moment is read from the `tier` column, since matching "design" anywhere in a row let a *closure* row saying "conformance to the design" satisfy the check — **and the invariant asserting otherwise was vacuous**, its fixture merely omitted the word; `SKILL.md` restated `review.md` wholesale against `review.md`'s own DRY rule, and the two copies had already drifted in the same release that created the second one, so Phase 3 is now trigger-plus-pointer; the REVIEW_LOG template gained the `## Notes` section that "what did it find" requires; and mode is declared **per unit of change**, not per project. Battery 74/74.

## [1.18.0] - 2026-07-28 (Architect Pass)
### Added
- **`architect.md` — the architect pass: capabilities before files (F-020).** Phase 3 went from the spec elicitation straight to the **Impact** (the list of files that change). Nothing in between asked *what the system must be able to do* and *whether a component already does it* — so the agent designed the feature and built whatever it lacked **inside the feature's own code path**: no component owned the new capability, the next feature that needed it rebuilt it differently, and the platform accreted feature-shaped code nobody could reuse. Myopia one level above the file: the change is complete, the tests pass, and the architecture is worse. The pass runs at L3 between elicitation and the Impact, in three moves: **(1)** state the feature as required **capabilities** — verbs over domain nouns, naming no file, no class, no library (that is the decoupling); **(2)** rule each one against the platform — **EXISTS** (name the component and where it lives), **INADEQUATE** (same, plus the gap), **MISSING** (say what you searched: a MISSING declared without a real search is how duplication enters, the architecture-level DRY check); **(3)** design what is missing as a component whose **contract is stated in its own vocabulary, with the feature as one consumer, never the owner** — the test is mechanical, write the contract without naming the feature, and if you cannot, it is feature-shaped and the second consumer will force it open. Guarded on both sides: it is not a licence to build a framework (the rule constrains the contract's vocabulary and ownership, not its scope), and it is a question rather than a form (when every capability plainly exists, one line answers it). **Split rule** (§4): a capability becomes its own ANALYSIS/branch/closure when it will have more than one consumer, is independently mergeable and testable, or carries its own risk surface (security, public contract, data model, new dependency) — otherwise it is the first phase of this feature's plan, still with its own contract and its own tests, never inlined. The split rule decides the paperwork; it never decides whether the component exists. Five anti-patterns are named so a review can catch them: **inlining**, **feature-shaped platform**, **silent degradation** (a MISSING capability nobody builds, absorbed by quietly reshaping the feature — that is a scope change owed to the user, not a design detail), **speculative platform**, and the **paper ledger** (every row EXISTS, nothing named — unfalsifiable, exactly like a review that reports "I checked"). L1/L2 do not run the pass: a capability discovered MISSING during L2 work is itself an escalation trigger to L3.

- **`## Component Map` — the inventory the pass reads (F-020b).** The pass shipped with nothing to consult: §2 said *rule each capability against the platform*, and no artifact described the platform's components. `strategic/architecture.md` carried stack, directories and patterns — `## Directory Structure` names folders, not capability owners — and `source_kind: code` guides cover one component at a time, on a complexity trigger, never the inventory. So the platform had to be re-derived from source every session: the myopia the skill exists to prevent, reproduced inside the cure for it. Two more gaps came with it: **no trigger fired when a component was born** (the `architecture.md` row was keyed on *"when the stack … changed"*, and a new component is not a stack change — that is how an inventory rots silently), and the three architecture artifacts (ledger, architecture doc, ADR) never cited each other. All three close with one movement: a **`## Component Map`** section inside the canonical `architecture.md` — one row per component that OWNS a capability, carrying *capability owned* (a verb over a domain noun), *contract* (what it guarantees consumers, stated without naming any single one) and *where* (`path#symbol`). Not a new document: `architecture.md` already exists, is canonical, manifested and lifecycled, and adding a file beside it would be the **speculative platform** anti-pattern this same feature names. Wired as a loop: `architect.md` §2 reads the map **before** searching source (the map is the index, never the evidence — verify against code), the map gets its **own Write-Triggers row keyed on the component's birth**, and `review.md` makes a capability built-but-absent-from-the-map a finding, because the next feature reads that map, rules the same capability MISSING and builds it a second time. This repo's own map ships with it (7 rows: client roster, project seeder, skill deployer, template source, doctrine, validator, invariant battery). New invariant `test_component_map_wired` (asserts the trigger is *not* the bootstrap/stack row it would hide behind); battery 60/60. Left open deliberately: the ADR trigger stays prose — *no decision, no ADR* blocks useless ADRs, but nothing detects a decision taken and not recorded, and a stdlib validator cannot read a diff and judge.

- **Brownfield safety: an unread map is not an empty one (F-020c).** Telling the pass to read the Component Map first created a trap on every project the methodology arrives in late: `init.js` seeds `architecture.md` with an **empty** map, so the pass would read an authoritative-looking empty index, rule every capability MISSING, and design duplicates of components already in the codebase — the exact DRY failure the pass exists to prevent, now with a document vouching for it. Closed with an asymmetric rule instead of a caveat: **the map lowers the COST of a verdict, never the STANDARD of one** — it is a cache of evidence somebody already paid for, so a hit means the search is written down, a miss means you pay full price, and reading a row never excuses checking that it is still true. **Its silence is unread, not empty**: the map covers only the areas `audit/audit_plan.md` marks ANALYZED, and outside them it **can never ground a MISSING verdict** — you search, and the MISSING you reach carries its terms, its tool and the areas covered (an unfalsifiable MISSING is the same defect as an EXISTS with no symbol named). The deferral is scoped where it cannot do damage: **understanding is never deferred, only WRITING the map is** — the incremental licence covers the rest of the repository and never what the change touches or depends on, which is understood now, at full standard, mapped or not. Named **`Empty-map MISSING`** in the anti-patterns so a review can catch it, and `review.md` makes an unnamed-search MISSING on unmapped ground the finding that matters most on a freshly-onboarded project. **Phase 1 gains the order and the bound**: write `audit/audit_plan.md` FIRST (the scope ledger everything else is built on), then let the map start at whatever the first task made you understand — **no full-codebase sweep is required before the first feature**, because an unbounded up-front sweep is skipped silently, which is worse than an incremental map. Discovering an existing component now writes its row too, and marks the area (`sdlc_check.py mark`), so the inventory grows by the feature that needed the knowledge. This repo's own map declares its coverage. New invariant `test_unmapped_never_grounds_missing`; battery 61/61.

- **Mechanical backstops for the pass (F-020d): a skipped pass and a rotting map are now noticed, not trusted.** The pass shipped as prose plus invariants on the prose — the battery proved the doctrine was *wired*, nothing noticed whether an agent *executed* it, and a Component Map row whose symbol got renamed stayed green forever (guides have `source_hash`; the map had no equivalent). Both closed in `sdlc_check.py`, warnings only, never a gate: **(1) skipped pass** — `validate` warns when an ACTIVE (PLANNED/IN_PROGRESS) L3 ANALYSIS started on/after 2026-07-28 lacks `## Capability Ledger`; closed history and analyses born before the pass never nag (`ARCHITECT_PASS_EPOCH` grandfathering — the pre-1.17 handoff's lazy-convert doctrine applied again). **(2) rotting map** — `validate` resolves every path-shaped ref in the map's `Where` column (glob-aware, `confine_under` fail-closed on escapes) and greps the `#symbol` in the matched files: a dead path or a renamed-away symbol is flagged with the row to fix. Proof of usefulness on day one: the check caught a rotten ref in this repo's own freshly-written map. **(3) adherence** — two behavioral scenarios join the non-gating eval layer (the F-016 route): `architect_rules_before_impact` (capabilities ruled before files, EXISTS cites the map, MISSING names its searches) and `unmapped_never_grounds_missing` (the brownfield trap seeded for real: an existing `RateLimiter` in a PENDING `legacy/` area — the run that rules MISSING from the map's silence FAILS). `architect.md` gains §Mechanical backstops naming all three. New invariants `test_ledger_due_gating`, `test_component_map_rot_detected`, `test_architect_scenarios_present`; battery 64/64.

- **Independent pre-publication review, and what it changed (F-020e).** Two read-only reviewers with fresh context (conformance+correctness; adversarial Vision+doctrine) both returned FAIL on the release candidate. Five blockers, all real, all fixed before publishing: **(1)** the skipped-pass backstop could never fire — `ledger_due` required PLANNED/IN_PROGRESS, but closure flips the ANALYSIS to COMPLETED *before* `check` runs, so it was silent at the only moment the process mandates the validator (status filter dropped; `start_date` is the sole guard, which is all grandfathering needed — and the invariant that had locked the defect in is inverted). **(2)** A component the pass merely DISCOVERED had no write trigger: `architect.md` mandated the row, but `SKILL.md` — the authoritative write index — and `review.md` fired on a component's *birth* only, so an agent could obey every shipped rule, mark the area ANALYZED, leave the map silent, and let the next feature lawfully rule MISSING and build a duplicate. The trigger and the review finding now cover discovery, and `architect.md` forbids marking an area whose owners are not yet rows. **(3)** "Warnings — never a gate" was false: `--strict` escalates warnings to exit 1 and `ENFORCEMENT.md` recommends it in CI, so the ledger check was a *blocking* gate on consumer pipelines — a cost the ceremony-budget acceptance never named. Fixed by honoring the accepted budget instead of expanding it: a third severity, **advisories**, printed as `[note]`, never counted as warnings, inert even under `--strict`. **(4)** A literal bracket in a path (`app/[id]/page.tsx` — every Next.js/SvelteKit project) was interpreted as a glob and reported as rot; literal existence is tried first. **(5)** The rot check was inert in silence — `Where` assumed to be the last column, refs without `/` skipped (9 of this repo's own 18 refs unchecked), Windows separators skipped, and `#Notif` passing against `Notifier` on a substring match; all fixed, plus a notice when a map has rows but no checkable ref, because an inert check reported as clean is the same defect as an unread map reported as empty. Doctrine hardening from the same round: §4's split rule had an unreachable default branch (bullet 2 named a property §3 mandates of *every* component, so each one earned its own L3) — resharpened to "delivers value merged alone" with an IN/OUT pair; the contract test gained the re-description clause that paraphrase defeated; the MISSING search gained a floor (domain noun + two synonyms + verb, across every listed area) and a stopping rule; the "one line" licence now says the answer still lives under the heading and still names the component; `SKILL.md` phase 3 states both modes' homes and the Hybrid coverage asymmetry; the duplicated `Coverage:` list became a pointer to `audit_plan.md`. Battery 65/65.

- **Second review round: a traversal crash and a check that could not fire (F-020f).** A verification reviewer confirmed all five round-1 blockers fixed by execution; a *cold* adversarial reviewer with no knowledge of round 1 found two more. **(1)** `cmd_stale` and `cmd_mark` never confined the paths they read out of `audit_plan.md` — and `init.js` seeded the row `| / | PENDING |`. Mark that area and `root / "/"` becomes the drive: the closure gate walked the whole filesystem and died on `ValueError: ... is not in the subpath of ...`. A `../escape` row walked outside the project just as happily. The one place that walks the filesystem was the one place not using `confine_under`, which every other path input already goes through — and 1.18.0 is what promoted `audit_plan.md` to load-bearing, so a pre-existing bug became a release blocker. Both commands now confine fail-closed (`mark` refuses, `stale` warns and skips), the seeder writes `.`, and `relative_to` is guarded. **(2)** `SKILL.md` claimed the review clause was the sole Hybrid check that the pass ran, while that clause was conditional on *"when the artifact carries one"* — so on a skipped pass, which produces no ledger, it could never fire. The clause is now unconditional at L3: **an impact/solution analysis or design carrying no Capability Ledger is itself a finding.** Also from the cold round: the extension heuristic turned prose into rot warnings (`app.core`, `OrderStore.save`, `1.18.0` all reported "the map is rotting") — now a closed suffix list; a freshly seeded project emitted an advisory about the placeholder row the seeder had just written (the day-zero false positive that trains readers to ignore the channel) — placeholder rows are skipped and the template no longer ships a half-real ref; the map heading match was case-sensitive and anchored, so `## component map` silently disabled both the check and the notice meant to catch its absence; a headerless or ragged table mis-indexed columns and reported silence as cleanliness — a `Where` header is now required and ragged rows are counted and reported; and two zero-cost bypasses of the ledger backstop are closed (deleting the optional `level:` line now warns; the heading is matched anchored on comment-stripped text, so a `<!-- TODO: ## Capability Ledger -->` no longer counts). New: an advisory for **a mark nobody paid for** — an area marked ANALYZED that owns no Component Map row, the missing half of the loop, since marking is one cheap command and it is what converts the map's silence into a groundable MISSING. Doctrine: the split rule's second bullet became a real discriminator (ships on its own cadence, before the feature) instead of a restatement of the first; the MISSING search floor was unexecutable as written (it prescribed a symbol-graph tool for a query that tool cannot take, and quantified over an undefined unit) — now text-search-first, symbol-graph-to-confirm, with triage as the stopping rule and a *provisional* MISSING when the area is still PENDING; the ledger template gained the Evidence column its own rules require. Battery 69/69.

- **Third review round — and the first time anyone USED it (F-020g).** Static review had run three times; nobody had run the methodology end to end. A reviewer did, cold, on a 25-file brownfield fixture with two components hidden behind unhelpful names — and found a different class of defect than any reading had. **The convergent BLOCK** (found independently by the usage trial and a code-delta reviewer): the "a mark nobody paid for" check harvested backticked refs from the **whole** `architecture.md`, and the canonical template puts `## Directory Structure` — full of backticked paths — directly above the Component Map, so the only automated guard that a mark asserted something real was **inert on every project that filled in the shipped template**; the harvest is now scoped to the map's `Where` column. **From the usage trial:** the guide router is a mandatory Rule Zero read whose verdict may not be faked, yet `index` refused to write it with zero guides and `init.js` never created it — the required declaration was **unsatisfiable on every project's first day** (now an empty stub is always written, and `guides.md` names a third legal verdict, `router: absent`); `SKILL.md`'s L3 minimum sections omitted `## Use Cases / User Needs` while `review.md` makes an uncovered use-case a finding, so an ANALYSIS could pass `check` CLEAN and then fail its own closure review. **CI honesty, again:** the `level`-missing guard added last round shipped as a *warning*, and `--strict` escalates warnings to exit 1 — the exact defect the advisories bucket exists to prevent, reintroduced one round later, this time reddening CI on every pre-1.18 analysis that never carried the optional field. It is now an advisory, epoch-gated like the check it guards. The same applies to bootstrap DRAFT visions: the skill *mandates* `Status: DRAFT`, so `validate --strict` was red on every freshly bootstrapped project until a human ran the blind check — a pipeline teams delete rather than block on. DRAFT is a state, not a defect: advisory. Also fixed: multi-line HTML comments leaked into the generated manifest (the `project_vision.md` row read `... -->`, and the manifest is what every future agent reads to orient); `Next.js`, `Node.js` and `OrderStore.save` were reported as rotting paths (a slash-less token now needs a known suffix **and** a stem that is not a CamelCase prose word); `mark` printed `[ok] … added as ANALYZED` for paths it then discarded (all paths are validated before anything is printed or written); the `gate` message told the author to create the analysis they had just written instead of naming the real remedy (`status: IN_PROGRESS`); `SKILL.md` Phase 4 now states that flip, which nothing else performed; and `elicitation.md` gained the unattended path the trial had to improvise — declared assumptions plus `BLOCKED on the user`, never a silent guess, because a bootstrap Vision is DRAFT by mandate and the skip path is therefore unreachable on a project's first L3. Battery 73/73.
- **What the trial confirmed works, recorded so it is not refactored away.** The `architect.md` search floor's "**at least two** plausible synonyms" clause is load-bearing: in the fixture the domain noun alone returned **zero hits** for both hidden components, and the synonym clause found both — without it the run builds two duplicates. "Its silence is unread, not empty" made a confident MISSING *doctrinally unavailable* on a virgin repo. And the ledger's Evidence column turned a lookup into comprehension: re-reading the component it found surfaced a 4×-per-worker limit defect that no file-level impact analysis would have asked about, which the Silent-degradation rule then routed to the user as a scope decision instead of a quietly shipped bug. **The honest negative, not fixed here:** ceremony is proportional at the feature level and not at the *arrival* level — the first L3 in any repository pays a full product-Vision authoring round regardless of the task's size, because the incremental licence covers the audit map and pointedly not the Vision. That is a Vision-scope decision for the owner, not a bug to patch in a release.

- **Fourth round — narrow verification, and every defect it found was in a fix (F-020h).** Scope declared up front: verify the previous round's dispositions and hunt regressions in the code it introduced. Eight of nine fixes landed clean; the ninth was a **BLOCK of my own making**: the router-stub change replaced "guides exist but the router is missing → ERROR" with an unconditional advisory, so a project that has guides and loses its router (gitignored, dropped by a merge) reports CLEAN — the agent's mandatory Rule Zero lookup finds nothing, legally declares `router: absent`, and the guide that governs the work is never consulted. An **absent** router was graded below a merely **stale** one. The error is restored when guides exist; the advisory now covers only the zero-guide case. Three further defects, all the same shape — a fix whose blast radius went unmeasured: the advisory instructed users to write `owns no component` in the audit plan's Notes column and **nothing read that column** (a documented escape hatch that was fiction — now implemented, so an area that genuinely owns nothing can be declared instead of nagged forever); the unterminated-comment strip nuked to end-of-file, so an ANALYSIS that merely *mentions* `<!--` inline, or shows an unclosed example inside a fenced block, was told it had no Capability Ledger when it plainly did (heading detection now strips fences first and only opens an unterminated comment at line start); and the CamelCase exclusion added to stop `Next.js` being reported as rot silenced **22 of 39 probed filenames** — `App.tsx`, `Program.cs`, `Main.java`, `Cargo.toml`, exactly what React/C#/Java projects write in a `Where` cell — now narrowed to the one real class, a CamelCase stem with a `.js` tail. **An invariant was also theater**: the test claiming to cover the comment-bypass asserted `cmd_validate(...) == 0`, but advisories never move the exit code, so it passed against the pre-fix module; it now asserts on the extracted `has_ledger_heading()` including both false-positive cases. Finally, the manifest description fallback emitted markdown table rows (`| Milestone | Expected Benefit |`) as document descriptions — the manifest is the first thing an agent reads to orient, so table rows and bare bullets are skipped now. Battery 73/73; a freshly bootstrapped project exits 0 under `validate --strict`.

### Changed
- **`SKILL.md` phase 3 invokes the pass before the blast radius**, the L3 minimum sections gain `Capability Ledger`, and the Write-Triggers ANALYSIS row states that a split-out capability gets its own ANALYSIS with the two documents naming each other. **`templates.md`** carries the `## Capability Ledger` section immediately before `## Impact`, which it feeds. **`review.md`** gains a ledger clause on the conformance statement — the three findings that live nowhere else (MISSING implemented inside the feature's code path; a contract naming the feature; a MISSING capability absorbed as a silent scope reduction), plus an unnamed EXISTS row as a finding in itself. Authored and never checked is how a pass becomes theater. New invariant `test_architect_pass_wired` (asserts the ordering too: capabilities are ruled before files are listed); battery 59/59.
- **Ceremony budget declared, per the Vision's `no ceremony ratchet` Non-Goal**: this adds cost at L3 and removes nothing, so it takes that rule's second branch — cost stated, owner accepts explicitly, and stated in full because "Omission resolves against the proposal". The six costs, all landing on L3 only: **(1)** the architect pass itself, before the Impact; **(2)** one ANALYSIS section (`## Capability Ledger`); **(3)** one support file (`architect.md`), read only when the trigger fires; **(4)** a `## Component Map` row written at closure whenever a component is born, changes contract, or is discovered; **(5)** the `sdlc_check.py mark` obligation on an area the pass searched; **(6)** one more clause on the `review.md` conformance statement for impact/design reviews. Two validator checks report on (2), (4) and (5) as **advisories** that cannot fail a build. Accepted by Antonio Pinto, 2026-07-28, scoped to L3; L1 and L2 are verifiably untouched (`ledger_due` returns False for any non-L3 level). No validator rule lands on consumer projects — a warning on every existing ANALYSIS is the nagging the Vision forbids. Governed by `ai_docs/solutions/ANALYSIS_architect_pass.md`.

## [1.17.0] - 2026-07-27 (Parallel Handoff)
### Changed
- **`audit/handoff.md` becomes a workstream registry (F-019)** — the single narrative handoff was session-scoped: with milestones in parallel, the last session to close overwrote everyone else's resume point (observed live: two 2026-07-27 sessions clobbered each other's handoff). Now: **one row per open workstream** (feature, level, branch, status, since, next step, pointers) — closing one milestone removes one row and never touches another's; whoever opens the project sees at a glance what is in PROGRESS, on which branch, since when. Volatile resume logistics (branch/worktree, uncommitted state, environment notes, next command) move to **`audit/HANDOFF_[feature].md`** — ephemeral by design, **deleted at that feature's closure**: the ANALYSIS Diary keeps the durable narrative (DRY — anything in the HANDOFF file worth keeping was in the wrong file). The registry is an inventory for lookup, not a work board: no assignment, no due dates, no execution ordering (the Vision's work-management Non-Goal is the binding constraint, checked in the ANALYSIS). `ORIENT_DOCS` path unchanged — the registry flows through the SessionStart hook with no validator change. Touches `SKILL.md` (Write Triggers row split, Phase 1, Phase 5), `templates.md` (registry + per-feature templates with the Diary/logistics boundary), new invariant `test_parallel_handoff_wired`. Governed by `ai_docs/solutions/ANALYSIS_parallel_handoff.md`.
- **Upgrading from ≤1.16 costs nothing and requires nothing.** A legacy narrative handoff keeps working: the validator checks only its `Date:` header and age, the orientation hook reads the same path verbatim, and installing the skill never touches a consumer's `ai_docs/`. It reads as a one-row registry; **convert it lazily, the next time the write trigger fires** — `## Active features` bullets become rows, `## Next step` becomes that row's next step, `## Session notes` becomes `## Project-wide notes`. No migration sweep, no script, and deliberately **no validator warning** for the old form: nagging every existing project about a file that works is exactly the ceremony the Vision forbids. The invariant now asserts the migration clause is present — shipping a format change that strands existing projects is a caught regression.

## [1.16.0] - 2026-07-27 (Guide Activation + Verifiable Vision)
### Changed
- **Rule Zero declares the router verdict** — the triage level is declared together with the guide-router lookup result, as one line (`Level: L2 · router: no match` / `Level: L3 · router: GUIDE_x.md → read`). L1 stays exempt. Rationale: the consult trigger already existed in three places (Phase 4 bullet, `## Operative Guides`, `guides.md` §0) and still did not fire — none of them sits on a path every request executes. Making the lookup a **declared output** is what closes it: an undeclared lookup is indistinguishable from a skipped one, so `no match` is the expected, correct output on a repo with no matching guide. Field report that triggered this: guides were written and then never consulted unless the user asked by hand.
- **Phase 1 reads the guide router** — `ai_docs/reference/INDEX.md` joins `README.md` + `INDEX.md` as a mandatory orientation read: it is the only step that tells you a guide already governs the work you are about to do. The `templates.md` README template and this repo's own `ai_docs/README.md` list it first, so new projects inherit the fix.
- **SessionStart `orient` hook promoted from optional to recommended default** (`ENFORCEMENT.md` §4) and wired in this repo (`.claude/settings.json`). It already emitted the router (`ORIENT_DOCS`); it was simply off by default. Prompt placement carries the process, the hook is the backstop that survives long contexts and compaction. `sdlc_check.py` unchanged.
- **`source_kind: code` write trigger gets a real phase** — the Write-Triggers row moves from phase `any` (nobody's phase) to `4 / 5`, and Phase 5 gains a **Comprehension checkpoint** that asks the question out loud before closure: did this session force me to build a model of a high-complexity component no CURRENT guide covers? The duty still fires the moment the signal is recognized; the checkpoint is a backstop, not a deferral.
- **`guides.md` §0** gains the declare-the-verdict rule and its anti-theater twin (never fake a verdict; a verdict listing several guides means the match was not targeted, T7). **`dispatch.md`** pins verdict ownership: the orchestrator declares once at plan-authoring; a dispatched subagent does not.

### Added
- **`vision.md` — the drafting discipline that makes a Vision verifiable by a cold reviewer (F-018).** A Vision is a gate: a reader with no other context must rule ACCEPT or REJECT on a proposed change, quoting one line. Most cannot, and the gap is invisible from the inside. This file is the *why it works*, derived empirically from six blind adversarial rounds (reviewers with no repository access, ~25 attack proposals) by comparing the rules that survived every attack against the rules that fell. It carries: the **nine properties of a rule that holds** (key it to an observable property of the artifact, never to intent — *a rule whose predicate is a promise is satisfied by making the opposite promise*; both branches of the decision question answered; counterfactual phrasing; near-miss verbs enumerated; terms defined by effect with a closure rule; forms rather than instances; a checkable subject predicate; an IN/OUT pair on one axis; the anticipated re-descriptions named inside the rule's own sentence); the **five structural clauses** around them (supremacy, exceptions attached affirmatively, anti-abuse on every exemption, stated defaults per path, precedence); the **reject/admit asymmetry** — *only prohibitions reject, only positives admit*, so a Goal cannot stop anything and a criterion phrased as an already-true state cannot be advanced; the **minimum operable sections**; the **five failure classes no wording fixes** (each mapped to a mechanism, not better prose); and the **blind-check procedure** — text pasted not linked, fresh context, a battery with an accept side because *a gate that can only reject is half a gate*, and the demand for the mechanism behind each ruling. Wired from the Vision Gate (Standalone and Hybrid/M-VISION), the Write-Triggers Vision row and the `templates.md` Vision template, which is restructured to the operable sections with each marked `[gate]` or orientation. Shipped in the package allowlist. New invariant `test_vision_discipline_wired`; battery 57/57. Anchored by the owner's definition (`## What a Vision IS`): *a Vision states the benefit to be obtained while leaving the most degrees of freedom possible — it binds nothing that does not obstruct that benefit.* Operationalized as: benefit-not-mechanism (the test a North Star must pass), the **deletion test** as the generative rule for every constraint (remove the rule — benefit still reachable? delete it) and its stop rule, constraints that accumulate as work reveals obstacles (an almost-empty first draft is correct: DRAFT informs, APPROVED binds), and the invariant that a constraint never obstructs the Vision — a conflict is an amendment, owner-owned. The deletion test decides WHICH rules exist; the nine properties decide HOW to write one that holds. `elicitation.md` aligned: a mechanism is not an acceptable answer to the benefit question.

### Repository (this project's own `ai_docs/`, not shipped in the package)
- **Vision rewritten after a blind-reviewer clarity check (F-017)** — three reviewers with fresh context and **no repository access** read `ai_docs/vision/project_vision.md` cold: verdict FAIL, 10 convergent findings. Decisive one: the proposal *"cap how many operative guides a free user may create per month"* was **admissible on the literal text** — no Non-Goal covered metering, and every anti-paywall constraint was bound to the proper noun `devPNT` rather than to paywalling as a class, so the same proposal under another name passed untouched. The Vision was also undecidable in general: its only affirmative admission test was that a change "inherits `ai_docs/` frontmatter, manifest and lifecycle" — a test of form, not substance. Rewritten as `Status: DRAFT` (pending owner promotion): the product is stated in its own terms with no competitor in the North Star, a `## Core Problem` names myopia, Non-Goals are rules over classes (metering/paywall/account-gating; required network or off-repo storage; code or release coupling), a new `## The admission test` requires a change to advance a Success Signal and not merely be well-formed, and the six Success Signals are each checkable against a named artifact or command. The A/B/C/D layer map moved to its real home `strategic/capabilities_and_positioning.md`, declared a dated snapshot. Evidence: `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`; finding-by-finding disposition: `solutions/ANALYSIS_vision_clarity.md`. **No skill file changed** — this is the project's own governance, and the improvement is asserted until the blind lenses are re-run against the promoted text.

### Process note
Doc-only + tests: no `sdlc_check.py` or packaging change. Standalone L3 (devPNT off this session). Governed by `ai_docs/solutions/ANALYSIS_guide_activation.md` (F-016). Four new static invariants (Rule-Zero verdict, Phase-1 router read, code-guide phase, hook promotion) — battery 56/56 green; `validate` 0 errors. New behavioral scenario `verdict_declared_on_no_match.md` proves the "looked, nothing fitted" case; `consult_fires_on_match.md` now also asserts the verdict and that the consult fires unprompted.

## [1.15.0] - 2026-07-19 (Write Triggers + Code-Comprehension Guides)
### Added
- **Code-comprehension guides (`source_kind: code`)** — a new guide kind the agent writes **autonomously** (a duty, no proposal) when it recognizes a high-complexity component / feature / abstraction layer with no CURRENT guide: a source-faithful map of how the thing works, so the next session starts with the model instead of re-deriving it and breaking the component from partial understanding. Reuses the ENTIRE guide machinery (snapshot + `source_hash` + `stale` + router + fidelity markers) — the source is verbatim CODE EXCERPTS in `.sources/` instead of a handed document; `sdlc_check.py` is unchanged. The skill-wide "propose, never a silent write" rule is relaxed for THIS kind only (additive, code-anchored, reversible); the anti-hallucination floor holds — every claim traces to a code excerpt. Triggered by concrete signals (high comprehension cost, high fan-in, non-obvious flow, prior / repeated-across-sessions breakage from partial understanding, non-local rationale) and by **chronic fragility** (a component breaking repeatedly across sessions → write the guide AND escalate a refactor as its own L3; stop patching). Touches `guides.md` §1–§6, `SKILL.md` (4th "Comprehend" moment + Write-Triggers `code` row + consult wording), `templates.md` (`source_kind` + comprehension repertoire), `debugging.md` (capture-the-model + chronic-fragility). Positioned under Vision **Layer A** (Documentation-First lifecycle applied to code understanding), distinct from Layer D's user-indication operative guides.
- **`SKILL.md` §Write Triggers** — a mechanical document→trigger→phase table, symmetric to Rule Zero: triage decides IF documentation is due, this table decides WHICH document each event produces. One event, one destination; create-or-update, never duplicate. It is the authoritative write index; the workflow phases point to it.

### Changed
- **Bootstrap set made explicit (Phase 1)** — the named doc set (`README.md`, the three Vision docs as DRAFT, `strategic/architecture.md`, `strategic/existing_features.md`, Standalone `audit/audit_plan.md`, then regenerate `INDEX.md`) replaces the vague "minimal documents".
- **`handoff.md` write trigger + session-end rule** — mandatory at every L3 closure, and when a session ends with an ANALYSIS still IN_PROGRESS; the Phase-4 Diary trigger now names "session ends with work unfinished". Mirrored in `templates.md`.
- **`VISION_[feature].md` retroactive trigger** — fires when creating the SECOND `ANALYSIS_*` on the same theme (no foresight required).
- **ADR trigger unified** across Standalone (`architecture/`) and Hybrid (devPNT DB); no decision, no ADR.
- **`features_history.md` regime** pinned to `sdlc_check.py index` (prose discipline only without Python).
- **"Understand before acting"** now names cross-session source-memory rot — re-read a component you think you remember; trust the code (and its comprehension guide), not memory.
- **SKILL.md thesis line** — the skill's one-line "why": prevent *myopia* (acting from partial understanding).
- **Blast-radius enumeration is an authoring duty (Phase 3)** — mechanically enumerate every consumer of a signature-changed / multi-caller symbol up front with the symbol-graph, not as a review finding; `debugging.md` root-cause traces callers the same way (not text search).

### Process note
Doc-only: no `sdlc_check.py` or packaging change; validator behavior untouched (the packaged file allowlist is unchanged). Standalone L3 (devPNT off this session — locked on another project). Governed by `ai_docs/solutions/ANALYSIS_comprehension_guides.md` (F-015), Vision decision **B** (comprehension homed under Layer A, Layer D's differentiator untouched). Validated by TWO independent blind comprehension tests (fresh agent, skill-only, no hints): the new trigger is discoverable + correct, and the adversarial (refuses a general-knowledge guide) and autonomy-boundary (the autonomy relaxation does not leak to refactors or operative guides) probes pass; 6 findings surfaced across the two rounds and all fixed. Eval battery 52/52 green; `validate` 0 errors.

## [1.14.0] - 2026-07-08 (M6: Vision Actors — a characterized cast in the Vision)
### Changed
- **Vision defines Actors.** The Vision templates replace the flat `## Target Users` / `## Users or Stakeholders` with a first-class `## Actors` element: one light line per actor — **Role** — primary goal; good UX = what a good experience means to them. An Actor is defined ONCE in the Vision (project or feature) and REFERENCED by each use-case / `D-UC` (actor = who they are, use-case = what they do) — anti-DRY, and enough to design the intended UX for concrete roles instead of an implicit "user". A feature may declare its own feature-local cast for internal-tooling work.
- **`elicitation.md`**: the L3 elicitation round gains an explicit **Actors** question (role, primary goal, UX expectation); "for whom" is folded into it.
- **`SKILL.md`**: the "Protect the Vision" value now names the actors + the UX they expect; the §3 Request-Analysis trace includes the actor each part serves.
- **`review.md`**: the conformance set gains one rule — a use-case with no defined Actor, or an unmet Actor UX expectation, is a finding.
- **README** Key Features refreshed to cover the delivered M1–M6 capabilities (execution disciplines, operative guides + agent-KB, opt-in subagent execution, self-activation, and Actors).

### Process note
Governed Hybrid (devPNT re-pointed at this project): M-VISION `milestone_vision_vision_actors` v1.0 → milestone M6 → ADR `adr_2026-07-08_vision_actors` (Light record; the reviewed `ANALYSIS_vision_actors.md` is the design detail). The devPNT M-VISION doctrine mirror (`mcp_system_prompt.md` §4.2 — the M-VISION gains an Actors element, added to the Vision-Alignment re-read + the amendment hard-stop) is a devPNT-source edit pending `setup_mcp.bat` redeploy. Independent fresh-context reviews PASS (ANALYSIS diff: 2 WARN fixed, incl. the change satisfying its own new rule; ADR light: 0 BLOCK). Doc-only: `check --hybrid` CLEAN, eval battery 51/51. No new shipped support files (allowlist unchanged).

## [1.13.0] - 2026-07-05 (M2 amendment: review reads AND proves Vision + Use-Cases + Threat Model)
### Changed
- **Review discipline hardened (M2.A7).** `review.md` now, for an impact/solution-analysis / design review: (a) §Requesting takes the **Vision + use-cases/user-needs + threat model** as explicit inputs the reviewer checks the artifact *against* (Hybrid: M-VISION/D-UC/P-TM; Standalone: the ANALYSIS Vision-Alignment / Use-Cases / Threat-Model sections); (b) §Reviewing requires the reviewer OUTPUT to carry a **conformance/traceability statement** — each Vision benefit / use-case / threat mapped to where the artifact satisfies it, or a finding — and a PASS is **not valid on "found nothing"**. Scoped to analysis/design reviews (plain code reviews stay findings-only → honors the "no enforcement theater" Non-Goal); it is the reviewer-side twin of the existing §Receiving anti-silent-drop rule.
- **`SKILL.md` §3 Request Analysis**: an authoring rule — build + trace the Impact/solution ON the Vision, use-cases and threat model (so the closure review can verify conformance); a pointer to `review.md`, no restatement.
- **`templates.md`**: the ANALYSIS template gains a `## Use Cases / User Needs` section — the Standalone home for what Hybrid keeps in `D-UC`, giving the coverage-check a real target. Validator-inert (ANALYSIS_SECTIONS permits extra sections); the `Minimum sections` floor is deliberately left unchanged.

### Process note
Governed M2 amendment (Hybrid). E-ISP `e_isp_review_input_hardening` v2.0 (deep review, 3 rounds — round-1 BLOCK caught that the "use-case coverage" check had no Standalone home; v2.0 added the output-evidence half) + E-TDD v1.0 (light review, conformance statement 8/8) + §4.6 code review (PASS, zero BLOCK — self-caught + reverted a Minimum-sections regression before review). Doc-only: `check --hybrid` CLEAN, eval battery 51/51, shadow exported. The Hybrid mirror in the devPNT doctrine §4.5 + `devpnt-tech-reviewer` output format is a separate devPNT-project follow-up.

## [1.12.0] - 2026-07-03 (Client Roster: Google Antigravity 2.0 as a first-class client)
### Added
- **Google Antigravity 2.0 support** in the install engine. The runtime skill now lands where all three Antigravity products (desktop, the `agy` CLI, the agentic IDE) discover global agent skills: `~/.gemini/config/skills/agentic-sdlc/`. `agentic-sdlc-init` writes the Antigravity project pointer to `AGENTS.md` (the Antigravity CLI surface), reusing the single `protocolContent` — no per-client drift.
- **Shared-home collision resolved** (`~/.gemini`). Antigravity's global skills root lives UNDER `~/.gemini`, the home the legacy `gemini` client claims. A new distinct `antigravity` CLIENTS entry de-collides via two backward-compatible registry generalizations: an optional `skillsSubdir` (`config/skills`) on `skillTarget`, and an optional `homeMarker` (`~/.gemini/config/skills`) on `clientDetected` so Antigravity is detected only by its own skills dir, the `agy` CLI, or `ANTIGRAVITY_HOME` — never on bare `~/.gemini`. The existing three clients omit both fields and are byte-identical (no regression). See ADR `adr_2026-07-03_antigravity_gemini_home_collision`.
- **Node test battery** `scripts/test_clients.js` (dev-only, NOT shipped — excluded from the `package.json` `files` allowlist, which is now an explicit per-file list of the four lifecycle scripts). 8 cases covering the P-TM threats: T1 shared-home double-install (bare `~/.gemini` → gemini TRUE / antigravity FALSE), T2 distinct skill-target + install/uninstall round-trip, T3 detection matrix (marker OR env OR CLI), T7 the three existing clients unchanged.

### Changed
- `package.json` `files` allowlist: the wholesale `"scripts"` directory entry is replaced by the explicit four shipped lifecycle scripts (`lib.js`, `init.js`, `postinstall.js`, `preuninstall.js`), so the dev-only `test_clients.js` is never packaged (the same dev-only precedent as the Python `test_*.py` batteries).

### Process note
- Full Hybrid governance (devPNT): M-VISION → D-UC → P-TM → E-ISP → E-TDD → ADR, all governed. Implemented against the accepted **E-TDD** `e_tdd_antigravity_client` v1.0 (shadow exported to `ai_docs/solutions/` before coding). TDD: detection/target logic tests-first (RED→GREEN); prose/doc edits exempt (recorded). `postinstall.js`/`preuninstall.js` unchanged (pure registry consumers). Node battery 8/8 + skill eval battery 51/51 green; `check --hybrid` CLEAN. Owner inputs resolved in round 2: CLI binary `agy`, env override `ANTIGRAVITY_HOME`, Antigravity-specific reload string. The repo doc `ai_docs/solutions/antigravity_skills_guide.md` (plugin/mcp_config model) is superseded by the accepted skills-model decision (E-ISP/ADR).

## [1.11.0] - 2026-07-03 (M4: Consolidation & Proactive Activation — self-activating, self-consulting, self-testing skill)
### Added
- **SessionStart orientation hook** (`sdlc_check.py orient`): emits a bounded, repo-sourced orientation (README + INDEX + guide router + handoff + Rule-Zero triage) at session start. Zero-execution, **fail-OPEN** (a missing/empty `ai_docs/` never blocks the session), size-capped. Manual per-client wiring in `ENFORCEMENT.md` §4; `--hybrid` points at the devPNT bootstrap instead of duplicating plan/KL. `test_session_start.py` (9 cases).
- **Guide-layer consumption** (closes the write-only gap — Layer D "point to them"): a **consult trigger** (before operative L2/L3 work, targeted router match, L1 exempt, never blanket) and a **proactive-creation trigger** (propose a guide after user-indication-governed reusable work; never silent, never from model knowledge). Mechanics in `guides.md` §0/§1; hooked from `SKILL.md` Operative Guides + Phase 4/5; reconciled with subagent dispatch in `dispatch.md`.
- **Worktree/branch hygiene** in the closure discipline (`SKILL.md` Phase 4 isolate-on-branch / Phase 5 merge-decision + cleanup).
- **Skill eval harness** (dev-only, not shipped): `test_skill_invariants.py` is the deterministic static release gate (`python -m unittest discover -s scripts -p "test_*.py"` — asserts the skill's own doctrine invariants: triggers/hook/worktree present and wired, indexes idempotent, support pointers resolve; zero LLM/network/subprocess). Opt-in behavioral corpus `evals/scenarios/` + `run_behavioral.py` (non-CI, never gates). `ENFORCEMENT.md` §5.

### Process note
- Full governance per unit: M-VISION v2.1 (revised — added the guide-consumption unit) → D-UC + P-TM → per-unit E-ISP (deep review) + E-TDD (light review) → implement → §4.6 code review. The independent-review gate caught real defects at design time (incomplete eval invariant set, the M3↔M4 dispatch interaction, a REPO path off-by-one, a P-TM overclaim of unbuilt guards). Battery 51/51 green. ADR `adr_2026-07-03_skill_eval_harness`; KL architecture v1.4 + principles v1.2.

## [1.10.0] - 2026-07-03 (M3: Subagent Execution / Feature A — opt-in executable plan)
### Added
- **`dispatch.md`**: subagent-execution doctrine (opt-in for L3). The dispatch loop — validate the plan → per-task brief → economy-tier implementer → one-shot review → ledger — with client-relative model tiers (no provider names), one-shot review slots (no iterative loops), degradation to same-session where subagents do not exist, and guides injected by pointer (never pasted).
- **`sdlc_check.py plan` subcommand**: `plan validate` (schema check of the executable plan, fail-closed path/guide confinement, sidecar-ledger cross-check — "no valid plan, no dispatch") and `plan brief --task <id>` (emits, to stdout, the task + prior-task interfaces + guide pointers). The validator is **zero-execution**: a task's `verify` command is emitted as text, never run.
- **Executable-plan template** (`ai_docs/solutions/PLAN_[feature].md`) in `templates.md`: Markdown frontmatter (`status`, `derived-from`) + a fenced `json` task array + the sidecar `PLAN_[feature].ledger.json` shape (`task_id -> {status, verify_result, timestamp}`, git-tracked, survives compaction).
- **`SKILL.md` §4** opt-in subagent-execution hook + the Hybrid `derived-from` seam (the plan is derived from the accepted E-TDD, never independently authored).
- `test_plan.py`: stdlib-`unittest` battery for the `plan` subcommand (32 cases: schema, confinement, ledger, fail-fast JSON, zero-execution poka-yoke).

### Changed
- **`confine_under(base, rel)` extracted** in `sdlc_check.py`: the fail-closed path-confinement pattern (absolute/`..`/resolve-escape → reject), previously inlined twice (the `overrides:` and `distilled_from` checks), is now a single helper reused by both plus the new plan-path / guide-pointer confinement. Behavior-preserving (catches `(ValueError, OSError)`).

### Process note
- 4th live **model-per-dispatch** run (economy implementer from the E-TDD shadow, battery 32/32, deep code review PASS zero BLOCK). Governance: M-VISION → D-UC → P-TM → E-ISP → E-TDD, all through the independent review gate — which killed 3 real BLOCKs at design time (T1 subprocess-invariant misstatement, a missing impacted file, a `confine_under` OSError-crash regression). ADR `adr_2026-07-03_executable_plan_json_in_md`.

## [1.9.0] - 2026-07-03 (M2 execution disciplines + Feature B unit 2 agent KB)
### Added
- `tdd.md`: TDD discipline (RED/GREEN/REFACTOR, increment rule, AAA test shape, documented exemptions) — the L2/L3 default for implementation work.
- `debugging.md`: systematic debugging method (reproduce, isolate, root cause, fix, regression test, collateral check) with circuit-breaker integration.
- `elicitation.md`: spec elicitation round (goal/benefit, scope boundaries, non-goals, constraints, acceptance signals) run before drafting the analysis in phase 3.
- `review.md`: single definition of requesting, receiving, and performing code review, reused by the Hybrid review gates.
- `SKILL.md` wiring: pointers to the four new files added at phase 3 (elicitation), phase 4 (TDD, debugging, circuit breaker), and phase 5 (review).
- Agent-global KB (fixed root, project-wins precedence, `overrides:` with fail-closed confinement, collision warnings).

## [1.8.1] - 2026-07-02
### Fixed
- **Guide freshness hash is now line-ending independent**: `sha256_file` in `sdlc_check.py` normalizes CRLF → LF before hashing. Previously the raw-byte hash made a fresh Windows checkout with `core.autocrlf=true` rewrite `.sources/` snapshots and flag every guide `[stale]` (false positive). Backward compatible: recorded hashes were computed on LF content, and normalization maps CRLF copies back to the same digest. (Edge case: a hash recorded pre-1.8.1 on a snapshot that genuinely contained CRLF bytes will flag `[stale]` once — regenerate the hash.)
- `guides.md` step 3 now states the hash is computed over LF-normalized content and recommends the `ai_docs/reference/.sources/** -text` `.gitattributes` rule to consumer projects (defense in depth: keeps snapshots byte-verbatim).

### Test battery addition
- Scenario 10 (extends the unit-1 battery): snapshot checked out with CRLF endings + guide recording the LF-normalized hash → `stale` must NOT flag it; a genuine content edit must still flag `[stale]`.

## [1.8.0] - 2026-07-02 (Feature B unit 1: operative guides, project scope)
### Added
- **Operative guides** (`ai_docs/reference/GUIDE_[topic].md`): a durable, source-faithful layer distilled from USER-PROVIDED indications — the capability neither agentic-sdlc nor superpowers had. New support file `guides.md` (pipeline: topic decomposition → user confirmation → verbatim snapshot in `reference/.sources/` with SHA-256 → source-anchored extraction → per-section fidelity markers `[source: …]` / `[not covered by source]`); guide template with provenance frontmatter (`source`, `source_version`, `distilled_from`, `source_hash`) in `templates.md`; short "Operative Guides" section in `SKILL.md`.
- **Generated guide router** `ai_docs/reference/INDEX.md` (emitted by `sdlc_check.py index`, alignment-checked by `validate`): path, status, when-to-consult line and provenance summary per guide — the pointer target for the devPNT Hybrid bridge.
- **Mechanical fidelity controls** in `sdlc_check.py`: provenance-key and per-section marker checks (warn; fails CI under `--strict`); `distilled_from` path confinement — absolute paths, `..` and symlink escapes rejected, fail-closed (ERROR); guide freshness in `stale` — recorded `source_hash` vs current snapshot, flagged in EVERY mode including `--hybrid` (guides are filesystem-first even in Hybrid).

### Changed
- `stale --hybrid` no longer returns unconditionally 0: it still skips audit-plan staleness (delegated to devPNT/KL) but now checks guide-source drift.
- `list_canonical_docs` skips dot-subdirectories of canonical dirs (e.g. `reference/.sources/`): snapshot files are no longer swept into the manifest. Projects that kept `.md` files under dot-subdirs of canonical dirs will see them leave `INDEX.md` (more correct).

### Process note
- First live run of **model-per-dispatch**: implementation dispatched to an economy-tier subagent working from the accepted E-TDD shadow as a self-contained brief; independent deep code review passed first round with zero blocking findings. Governance: M-VISION → D-UC → P-TM → E-ISP → E-TDD, all through independent review gates (devPNT Hybrid).

## [1.7.0] - 2026-07-02 (Phases 0-1 of the evolution roadmap)
### Changed (breaking-soft)
- **English is now the canonical language of the skill**: `SKILL.md`, `templates.md`, `ENFORCEMENT.md`, validator messages, generated indexes and the project protocol are in English. New ANALYSIS documents use English frontmatter keys (`status`, `level`, `start_date`, `end_date`) and English section headings. **Existing projects keep working**: the validator silently accepts the deprecated Italian keys (`stato`, `livello`, `data_inizio`, `data_fine`) and Italian headings.
- The generated project protocol (`CLAUDE.md`/`GEMINI.md`/`AGENTS.md`/`.cursorrules`) is now a **thin pointer** to the skill (triage summary + where things live + closure gate) instead of a condensed copy of its rules, which had drifted from `SKILL.md`.
- `init.js` now seeds `ai_docs/` from `templates.md` (single template source) instead of inline boilerplates; it creates `ai_docs/reference/` and the curated `ai_docs/README.md`, no longer seeds the generated `features_history.md`, and generates `INDEX.md` via the validator when Python is available, so the very first `sdlc_check.py check` on a fresh project is CLEAN.
- Client detection unified between `init.js` and `postinstall.js` (`scripts/lib.js`): CLI on PATH **or** config home present (covers Claude Desktop with integrated Claude Code).

### Added
- `sdlc_check.py validate --strict` / `check --strict`: warnings and a missing `ai_docs/` become failures (for CI).
- **Coexistence with devPNT (Phase 1, the Hybrid seam)**: new SKILL.md section with the ownership matrix (who is master per artifact in Standalone vs Hybrid), the triage equivalence table (one significance threshold, two vocabularies), the ANALYSIS↔plan-node state mapping and the shadow discipline (`SHADOW_[doc_key]_vX.Y.md`, exported BEFORE implementation; never saved under an `ANALYSIS_*` name).
- `sdlc_check.py --hybrid` (explicit, never auto-detected) on `check`/`stale` (audit-plan staleness delegated to devPNT/KL) and on `gate` (an approved E-TDD shadow in `solutions/` authorizes writes on protected paths).
- devPNT MCP doctrine (`mcp_system_prompt.md`, devPNT repo) slimmed accordingly: process (triage, phases, lifecycle, closure) deferred to the skill; `ai_docs/` layout aligned (adds `vision/` and `reference/`); shadow naming and shadow-before-implementation rule; checklist items for methodology, shadow export and hybrid closure gate.
- Evolution roadmap for v1.7.0 in `ai_docs/vision/roadmap_evoluzione_agenti.md` (subagent execution, operative guides + agent-level knowledge base, devPNT seam, open-core positioning).

### Fixed
- Shadow detection is structural (filename `SHADOW_*` or `<!-- SHADOW` marker on the first line): an ANALYSIS merely *mentioning* shadows is no longer silently skipped from index and validation.
- `mark`/`index` fail fast when `ai_docs/` is missing instead of silently creating a second documentation root in the wrong directory.

### Removed
- Divergent `agentic-sdlc-v2/` copy (integrated in 1.5.0, the leftover risked edits on the wrong files).
- `references/*_template.md` (duplicated `templates.md` and had already diverged).

## [1.6.0] - 2026-06-15
### Added
- **Manifest generato dei documenti canonici** (`ai_docs/INDEX.md`): `sdlc_check.py index` ora produce, oltre a `features_history.md`, un indice completo di tutti i doc in `vision/`, `reference/`, `architecture/`, `functional/`, `strategic/`, con descrizione e stato letti dall'header. Si rigenera, quindi non drifta.
- **Lifecycle dei documenti canonici**: convenzione header `status: CURRENT|SUPERSEDED|DRAFT|DEPRECATED` + `supersedes:`. `validate` avvisa se `status` manca/è invalido o se un doc superseduto è ancora `CURRENT`. Stop ai grep che riportano a guide obsolete.
- **Modello a due indici** documentato nella sezione "Documenti ai_docs" di `SKILL.md`: `README.md` curato (must-read, a mano) vs `INDEX.md` generato (completo, meccanico) — ruoli separati, prima confusi in un unico README che driftava.

### Changed
- §1 Audit: leggere `README.md` + `INDEX.md` all'avvio per sapere cosa esiste prima di esplorare il codice.
- §3 Analisi: cercare con glob/grep un'ANALYSIS esistente prima di crearne una nuova (anti-duplicazione).
- §5 Chiusura: gate "Indici allineati" — rigenerare `INDEX.md`, aggiornare il `README.md` curato per i must-read, marcare lo `status`; doc canonico non indicizzato o senza `status` = chiusura sporca.
- `templates.md`: aggiunto il template dell'header dei documenti canonici.

### Fixed
- `sdlc_check.py` legge ora i file con `utf-8-sig`: un BOM iniziale (file autorati su Windows) non impedisce più il riconoscimento del frontmatter `---`.
- L'estrattore dell'header riconosce sia il frontmatter `status:` sia la riga in corpo `**Status:**`/`Stato:`, e gli stati di tutte le convenzioni in uso (canonici `CURRENT/SUPERSEDED/DRAFT/DEPRECATED`, vision `DRAFT/APPROVED`, ADR `Accepted/Proposed/Rejected`) — niente più falsi avvisi "status non riconosciuto" su `APPROVED`/`Accepted`.
- La descrizione del manifest salta righe di metadati (`Date`, `Created`, `Task ref`, ...) e i commenti HTML, così non finiscono come descrizione del documento.
- `index` non genera più un `INDEX.md` vuoto su progetti senza documenti canonici (solo `solutions/`+`audit/`).

### Migrazione (da 1.5.x)
- Al primo `sdlc_check.py check`/`validate` dopo l'upgrade, un progetto con documenti canonici darà **un errore** `ai_docs/INDEX.md mancante`: è atteso — esegui **una volta** `sdlc_check.py index` per generarlo. Da lì in poi resta allineato.
- I documenti canonici preesistenti senza `status:` produrranno **avvisi** (non errori): aggiungi l'header `description:`/`status:` per silenziarli. I nuovi progetti nascono già compatibili (template aggiornati).

## [1.5.0] - 2026-06-13
### Added
- Introdotta la Regola Zero di triage (`L1`, `L2`, `L3`, `Spike`) per rendere il processo proporzionale al rischio.
- Aggiunta simbiosi esplicita con devPNT: in Hybrid la `M-VISION` guida la milestone, il Master Plan resta roadmap strategica e l'Action Plan governa l'esecuzione tattica.
- Aggiunti support file dentro la skill runtime: `templates.md`, `ENFORCEMENT.md`, `scripts/sdlc_check.py`.
- `agentic-sdlc-install-skill` ora installa la skill nativa anche in `~/.gemini/skills/agentic-sdlc/`.
- Aggiunto validatore meccanico opzionale per frontmatter ANALYSIS, Vision state, indice feature e audit stale.

### Changed
- Il nome pubblico resta `agentic-sdlc`; la proposta v2 e' stata integrata come evoluzione, non come skill parallela.
- Aggiornati `agentic-sdlc-init`, template, protocolli generati, README e metadata.
- La modalita Standalone resta completa; devPNT e' un livello di governance superiore, non un prerequisito.

## [1.4.0] - 2026-06-07
### Added
- Introdotta la governance della **Vision** con nuova struttura `ai_docs/vision/` (`project_vision.md`, `roadmap.md`, `principles.md`, `features/`).
- Aggiunto il **Vision Gate** nel workflow operativo: ogni feature significativa deve essere verificata rispetto a obiettivi, non-obiettivi, benefici attesi e segnali di successo prima dell'analisi tecnica.
- Aggiunti template Vision in `references/` e sezione `Allineamento alla Vision` nel template di analisi.
- `agentic-sdlc-init` ora crea i documenti Vision boilerplate nei nuovi progetti.

## [1.3.1] - 2026-05-14
### Fixed
- Correzione documentazione (README + CHANGELOG) della sintassi per invocare il bin `agentic-sdlc-install-skill`. La forma `npx @antoneeo/agentic-sdlc-skill agentic-sdlc-install-skill` documentata in 1.3.0 **non funziona** perché npx non riesce a disambiguare il bin quando il pacchetto ne espone più di uno (errore: `could not determine executable to run`). Sintassi corretta: lanciare `agentic-sdlc-install-skill` direttamente dopo `npm install -g`, oppure usare `npx -p @antoneeo/agentic-sdlc-skill agentic-sdlc-install-skill` con `-p` esplicito.
- Nessuna modifica al codice della skill: il bin di 1.3.0 funziona correttamente, era solo la doc a indicare la sintassi sbagliata.

## [1.3.0] - 2026-05-14
### Added
- Nuovo comando esplicito `agentic-sdlc-install-skill` (registrato come `bin`): installa la skill in `~/.claude/skills/agentic-sdlc/` e `~/.codex/skills/agentic-sdlc/` **senza dipendere dal `postinstall` hook**. Risolve i casi in cui `npm` salta gli script (configurazioni `ignore-scripts=true`, policy IT aziendali, alcuni installer Node) e l'auto-install fallisce silenziosamente.
- Sezione "Troubleshooting" nel README con istruzioni per il caso in cui la skill non venga rilevata da Claude Code dopo `npm install -g`.

### Usage
```bash
npm install -g @antoneeo/agentic-sdlc-skill@latest
agentic-sdlc-install-skill
```

## [1.2.4] - 2026-05-14
### Fixed
- `postinstall` ora rileva Claude Code anche quando il CLI `claude` non è nel PATH (es. Claude Desktop con Claude Code integrato): la presenza di `~/.claude/` o della variabile `CLAUDE_CONFIG_DIR` è sufficiente per attivare l'installazione della skill in `~/.claude/skills/agentic-sdlc/`. Stesso pattern già usato per Codex.
- `preuninstall` rispetta `CLAUDE_CONFIG_DIR` per rimuovere la skill dalla directory di configurazione corretta.

## [1.2.2] - 2026-05-10
### Changed
- README convertito in inglese per la pubblicazione npm.
- Versione allineata a `1.2.2` in `package.json` e `gemini-extension.json`.

## [1.2.1] - 2026-05-10
### Fixed
- `postinstall` ora registra la skill anche per Codex copiandola in `$CODEX_HOME/skills/agentic-sdlc/` oppure `~/.codex/skills/agentic-sdlc/`.
- `preuninstall` rimuove anche la copia Codex della skill.
- `agentic-sdlc-init` ora crea `AGENTS.md` per Codex invece di `.codex/hooks.json`, che Codex non carica come istruzioni di progetto.

## [1.2.0] - 2026-05-10
### Added
- **Auto-installazione skill nativa Claude Code**: il `postinstall` ora copia `skills/agentic-sdlc-skill/` in `~/.claude/skills/agentic-sdlc/` quando rileva il CLI `claude`. La skill diventa disponibile come `agentic-sdlc` nel tool `Skill` di Claude Code dopo riavvio.
- Nuovo script `preuninstall.js` che rimuove la skill da `~/.claude/skills/agentic-sdlc/` durante `npm uninstall`.
- Fallback `copyRecursive` per Node < 16.7 (quando `fs.cpSync` non disponibile).

### Changed
- `package.json`: bump versione a 1.2.0, aggiunti keyword `claude-code` e `claude-skill`, descrizione aggiornata per riflettere supporto Claude Code nativo.

### Fixed
- Risolto bug per cui il pacchetto npm non registrava la skill in Claude Code (la cartella `~/.claude/skills/` non veniva mai popolata).

## [1.1.0] - 2026-05-10
### Fixed
- Fixed path inconsistencies in the generated `CLAUDE.md`, `GEMINI.md`, and `.cursorrules` protocols. Added full paths (`ai_docs/strategic/`) to all document references to ensure AI agents (like Claude) can correctly find and update them.
- Cleaned up encoding issues in initialization scripts.

## [1.0.9] - 2026-05-10
### Added
- New **Smart Discovery** system during project initialization.
- Official support for **Codex AI** via automatic `.codex/hooks.json` injection.
- Support for **Cursor** and **Windsurf** via `.cursorrules`.
- Binary command `agentic-sdlc-init` for use via `npx`.
- `postinstall` script for global AI CLI detection (Claude, Gemini, Codex).
- Full English localization for all user-facing messages and scripts.

### Changed
- Updated `init.js` to support the new `ai_docs/` directory structure defined in v1.0.8.

## [1.0.8] - 2026-05-10
### Aggiunto
- Skill evoluta in "Hybrid Edition": integrazione opzionale con **devPNT** (server MCP) per governance avanzata tramite database e piani gerarchici.
- Fase di Discovery per il rilevamento automatico dell'ambiente (Standalone vs Hybrid).
- Supporto per ADR (Architecture Decision Records) e Knowledge Layer (KL) nella fase di chiusura.

### Modificato
- Riorganizzazione dei percorsi di documentazione (`ai_docs/strategic/`, `ai_docs/audit/`, `ai_docs/solutions/`).
- Aggiornata la documentazione funzionale (`architecture_overview.md`, `external_interfaces.md`) con definizioni più precise.

## [1.0.7] - 2026-05-10
### Modificato
- Aggiornata l'attribuzione dell'autore (Antonio Pinto) e il copyright in tutti i file (`package.json`, `README.md`, `SKILL.md`).
- Aggiunto link al profilo GitHub ufficiale.

## [1.0.6] - 2026-05-10
### Aggiunto
- Sincronizzazione completa dei file del progetto nel repository.
- Supporto per il tracciamento delle feature e audit plan.

## [1.0.5] - 2026-04-17
### Aggiunto
- File `CHANGELOG.md` per il tracciamento delle versioni.

## [1.0.4] - 2026-04-17
### Modificato
- `README.md`: Aggiunte istruzioni specifiche per l'installazione da chiavetta USB e chiarimenti sulla disponibilità globale della skill.

## [1.0.3] - 2026-04-17
### Aggiunto
- Primo `README.md` con istruzioni di installazione e attivazione.

## [1.0.2] - 2026-04-17
### Corretto
- Riorganizzata la struttura delle cartelle secondo gli standard di Gemini CLI (`skills/agentic-sdlc-skill/SKILL.md`).
- Aggiunto frontmatter YAML a `SKILL.md` per la scoperta automatica.

## [1.0.1] - 2026-04-17
### Corretto
- Aggiunto `gemini-extension.json` (manifest dell'estensione) mancante nella versione iniziale.

## [1.0.0] - 2026-04-17
### Iniziale
- Prima pubblicazione della skill (Protocollo SDLC Documentation-First).
