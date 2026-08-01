---
id: F-022
feature: Multi-Domain Core (one spine, three domain skills)
status: IN_PROGRESS
level: L3
start_date: 2026-07-31
end_date:
---
# Feature Analysis: Multi-Domain Core

## Objective

Three skills — `agentic-sdlc` (code), `kb-agentic` (knowledge), `mkt-agentic-sdlc`
(marketing) — were created by copying one another and have already diverged in
opposite directions: kb byte-copied a spine that no longer fits it (its release gate
is red), mkt rewrote the validator instead. Evidence per claim is in the Capability
Ledger.

Collapse the duplication into **one neutral core plus three domain overlays**, so that:

1. a spine change is authored in one place and divergence is caught mechanically;
2. the three skills can be installed together and the agent routes to the right one by
   a stated, repeatable test;
3. they share **one** `ai_docs/` tree in which a fact has one home and is **cited,
   never copied**;
4. projects already using `agentic-sdlc` see **no behavioural change**, and mkt
   projects migrate only when they choose to.

Applied to the product itself, this is the problem the methodology exists to prevent.

## Feature Vision

**Expected benefit.** One authored source of process discipline, three distributions.
Maintenance stops scaling with the number of domains; a fourth domain becomes an
overlay, not a fork.

**Alignment, and the Vision amendment this feature carries.** P5/P7 publish three
packages from one repository, which contradicts what `project_vision.md` stated the
product ships as; its admission test requires such a change to amend the Vision in the
same change. **That amendment is drafted**: v7 rewrites `## North Star` (family of
skills from one shared core; the sibling-admissibility gate first drafted there was
removed after a confirming blind round and its veto restated as the *one triage
authority per kind of work* Non-Goal) **and** touches `## Actors` (family-wide
completeness; a sibling requiring devPNT is inadmissible). Status line marks the
amendment `PENDING the blind check`: the approved v6 body binds, the amended text does
not, until a blind round confirms the reshaped rules and the owner promotes. P1's
Vision work is therefore **running that blind round on the full v7 text (both amended
sections) and promoting or reverting** — not drafting the amendment, which exists.
The Vision's operative-guide paragraph ("written once and *cited* by later work") is
where C4 is grounded; this feature extends that existing principle across domains.

**Ceremony budget — declared, per the "No ceremony ratchet" Non-Goal.** That Non-Goal
counts read cost ("the instructions and documents it loads are part of the price"),
and `SKILL.md` is the only always-loaded file. The additions, each with its real cost:

| Addition | Lands on | Real cost, stated |
|---|---|---|
| Domain routing | L2/L3/Spike; **L1 exempt** — it runs *after* the level test | **One pointer line plus one trigger sentence** in `SKILL.md` (the same wiring `architect.md` and `guides.md` actually have: listing line + inline trigger + support file — the earlier "one pointer line" count matched neither precedent and is corrected here). The four-step procedure lives in `routing.md`, loaded only when a sibling lens is present. Residual accepted by the owner, 2026-07-31. |
| `domain:` frontmatter field | governed artifacts, **optional everywhere** | Absent resolves to the **project's declared default** (below), so no single-domain project of any domain ever writes it. |
| `default_domain:` project declaration | one line in `ai_docs/README.md` frontmatter, **seeded by init** | Written by whichever init the user runs (`agentic-sdlc-init` → `code`, kb's → `knowledge`, mkt's → `marketing`) — choosing the init *is* the choice, no interactive question. **Absent → `code`**, so every existing project keeps today's behaviour with zero migration. A second init finds the line and never touches it (create-only). |
| `checks:` frontmatter field | governed artifacts, **optional** | Opt-in import of another domain's portable checks (C2). A document that omits it behaves exactly as before. |

One doctrine line is added to `review.md` (C4). It adds no field and no check: it makes
an existing reviewer output catch a case it currently passes.

**Actors.** Defined in `project_vision.md` `## Actors`, not re-described here.
**Solo developer using an AI agent** and **Team lead needing governance** are the two
this feature serves. UC4 serves an internal-tooling cast declared feature-local,
permitted by `templates.md`: **Skill maintainer** — author the doctrine and publish
the packages; good UX = a spine change is authored in one place and a divergence is
reported by a test rather than discovered by a user. *Adopter evaluating the paid
layer* is untouched.

**Non-goals / out of scope.**
- **Not** merging the three into one skill. Three trigger identities are the point.
- **Not** changing the docs root for existing `agentic-sdlc` projects.
- **Not** building a package generator: it automates the cheap step (copy) and leaves
  the expensive one (reconciling three diverged validators) manual, and cannot run
  before a reconciled core exists. (A single-file build-time copy of the core inside
  the P5 monorepo is *not* this — it is evaluated in P5's own impact map.)
- **Not** deleting any repository.
- **Not** changing what any domain's doctrine *says*. This feature moves machinery.
- **Not** making the three distributions textually identical: overlays and
  domain-lensed shared files are supposed to differ (C6's membership rule).

**Success signals.**
- A spine change is authored once; **until P5 it is applied as three verbatim copies,
  and forgetting one is impossible silently** — the drift test fails. (P5's impact map
  evaluates collapsing the three copies to one file with a build-time copy step; the
  earlier signal "a spine edit lands in one file" overstated what this design produces
  and is corrected here.)
- An existing `agentic-sdlc` project's validator findings and exit code are unchanged —
  including when invoked via the `ENFORCEMENT.md` copied-file CI recipe.
- One `ai_docs/` holding code + knowledge + marketing artifacts validates clean under
  `--strict`, with the same result from any installed distribution.
- `kb-agentic`'s release gate is green.

## Use Cases / User Needs

| # | Actor | Use case |
|---|---|---|
| UC1 | Solo developer | Their agent picks the right lens and can state the test it applied, so a mis-route is visible rather than silent. |
| UC2 | Team lead | A marketing plan is built on facts the knowledge lens already distilled — located and cited, never re-collected or re-stated. ("one process, one source of truth") |
| UC3 | Team lead | A design takes distilled specs as its requirements input, citing the owning document instead of copying it. |
| UC4 | Skill maintainer *(feature-local cast, defined above)* | Author a spine change once; applying it to every distribution is mechanical, and a missed copy fails a test. |
| UC5 | Solo developer | Upgrade and observe no behavioural change — no new findings, no migration, no added step. ("ceremony proportional to risk") |
| UC6 | Team lead | Relocate a marketing project's docs root without losing the single source of truth: the old root keeps working until the move is complete, and the move is reversible. |
| UC7 | Team lead | Read the shared apparatus once and see every domain's entries, without another domain's internals arriving as noise. |
| UC8 | Team lead | A document owned by one domain but carrying another domain's material (a distilled spec with a budget table) can **import that domain's checks** instead of leaving them unrun. |

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| classify a request by **level** (risk) | EXISTS | Rule Zero triage in each `SKILL.md` | re-read all three: each carries an L1/L2/L3/Spike (mkt: E1/E2/E3) ladder with the same escalation shape |
| classify a request by **domain** | MISSING | — | searched `domain`, `lens`, `route`, `which skill` across the three skill dirs (ripgrep, all `*.md`); every Rule Zero classifies level only |
| detect that more than one lens is installed | MISSING | — | searched `installed`, `sibling`, `skills/`, `existsSync` across the three `scripts/` and all `*.md`. `lib.js` resolves *this* skill's install target; nothing enumerates siblings. → C0, **doctrine-owned**: the agent can list its own skills directory; no code is needed, only the stated rule and its fail-open default. |
| declare which domain an artifact belongs to | MISSING | — | `load_frontmatter` (`sdlc_check.py:195-209`) stores any `[A-Za-z_][\w-]*:` key, so a field is storable, but none is written or read. Nearest existing field is `source_kind:`, values **`document \| code`** (`guides.md:20,219`; `templates.md:25-26`) — a different taxonomy; the `kind` stem is what collides. |
| resolve a missing declaration **the same way from every entry point** | MISSING | — | nothing project-level exists; a per-distribution default was designed and **rejected in round 3** (F-3): with two lenses over one tree the same undeclared document resolved to different domains per validator — non-deterministic `validate`, ping-ponging generated files, and the security check swapping sections. → C1's project declaration. |
| validate an artifact against **its own domain's** rules | INADEQUATE | `scripts/sdlc_check.py` — code rules applied unconditionally | `SECURITY_SECTION` is a hard **error** with no level or domain gate (`:827-828`); the six `ANALYSIS_SECTIONS` are warnings (`:829-831`) and `--strict` escalates warnings to exit 1 (`:985`) — the CI mode `ENFORCEMENT.md:20-23` recommends |
| apply a domain's **specific competence** to a document another domain owns | MISSING | — | mkt's `ledger`/`budget`/`funnel`/`trace` exist only as `mkt_check.py` subcommands over `mkt_docs/`; nothing can run them on a knowledge-owned document carrying a budget table, so those numbers are checked by nobody. → C2's portable checks (UC8). |
| run domain validation for marketing | INADEQUATE | `scripts/mkt_check.py` — a second implementation | 567 lines, 2058-line diff vs `sdlc_check.py`; duplicates the generic plumbing and adds real domain rules — which are **already modular subcommands**, i.e. the portable-check shape C2 needs |
| index and route documents for retrieval | INADEQUATE | `build_manifest` / `build_index` / `build_guide_index`; router at `ai_docs/reference/INDEX.md` | machinery works, records no domain. `build_manifest` covers `MANIFEST_DIRS` (`:46`) — not `solutions/`; `build_index` (`:304-324`) covers `solutions/ANALYSIS_*` only. Both generated files are error-compared against their committed copy (`:857-861`, `:866-870`), which is why any column here is a compatibility event. |
| hold a single source for a claim and consume it by reference | INADEQUATE | shadow discipline; the Vision's operative-guide principle | the principle exists; nothing extends it across domains, no reviewer rule catches a restated fact, and **nothing detects a stale citation between reviews** — no reverse index, no hash on a cross-domain cite. Guides already solve this for themselves (`source_hash` + `stale`). |
| hold operative guides in a store shared across lenses | INADEQUATE | `DEFAULT_KB_ROOT = ~/.agentic-sdlc/` (`sdlc_check.py:61`) | kb's validator is byte-identical, so two lenses point at the same store; `check_kb_collisions` (`:472-496`) warns on filename collision and `--strict` escalates |
| keep the spine identical across distributions | MISSING | — | searched `sync`, `drift`, `generate`, `build` across the three `scripts/` and `ls .github/` (absent in all three): no mechanism. Drift has occurred twice, in opposite directions. |
| relocate a project's docs root safely | MISSING | — | searched `migrat`, `move`, `rename`, `mkt_docs` across all three `scripts/`: `init.js` seeds a root and never moves one. `ai_docs` occurs 49× in `sdlc_check.py`, 22/19/17 in the three test modules (107 total); `mkt_docs` 21× in `mkt_check.py`. |
| review an artifact independently | INADEQUATE | `review.md` — identical in code and kb **today** (diff = 0), but P3 must edit kb's copy | spine **plus profile**, like `test_skill_invariants.py`; needs the same split or C6's manifest falsifies on it |
| carry per-domain method | EXISTS | `architect.md`+`tdd.md`+`debugging.md` · `taxonomy.md`+`distillation.md`+`reconciliation.md` · `frameworks.md`+`research.md` | the overlay; supposed to differ |

### Components

**C0 — Installed-lens detection (doctrine-owned, ships with `routing.md` in P1).**
The agent checks its own skills directory for sibling lens skills; unknown or
single-lens → the router is not read. Stated as a rule in `routing.md` §0 — no
validator code, no separate file, no Component Map row of its own (it is doctrine, and
lands as an edit to the map's existing Doctrine row). Resolves the round-3 finding that
C0 owned no file and shipped one phase after the pointer that depends on it.

**C1 — Domain declaration, resolved at project level.** Two optional fields and one
seeded line:
- `domain: code | knowledge | marketing` on an artifact — declares its owner.
- **`default_domain:`** in `ai_docs/README.md` frontmatter — seeded by whichever init
  created the project; **absent → `code`** (every legacy project unchanged); a second
  init never overwrites it. An undeclared artifact resolves here, so `validate` gives
  **the same answer from every installed distribution** — the round-3 counter-case
  (same tree, two lenses, two different verdicts on the same file) cannot arise.
- Cases of absence, handled: legacy (→ project default → `code`); new docs in a
  single-domain project (the designed case — the field stays unwritten forever); a
  forgotten field in a mixed project (resolves to the default, and if that is the wrong
  domain the validator **fails visibly** on missing mandatory sections — never
  silently).

**C2 — Domain rule set: an exclusive part plus portable checks.**
- **Exclusive part — exactly one owner per document**: template, mandatory sections,
  the risk slot. This is where union would demand everything and intersection nothing,
  so it never composes. Each domain names its own mandatory risk section (code:
  `## Security and Threat Model`; knowledge: `## Sources and Verification`; marketing:
  `## Threat Map / Plan Risks`) — the slot is domain-translated, never dropped.
- **Portable checks — composable, opt-in per document** via `checks:`
  (e.g. `domain: knowledge` + `checks: [marketing.ledger, marketing.funnel]`). An
  imported check can only **add findings, never relax a requirement** — monotonic, so
  composition is safe by construction. mkt's subcommands are already this shape.
- **Sections-data for all three domains is authored in P2** as data in the core
  (resolving the round-3 sequencing break where TS3/TS4 needed rule sets that only
  P3/P4 would create); check *implementations* land with their domain: code+knowledge
  in P2, marketing's in P4 when `mkt_check.py` converges. A `checks:` entry naming a
  check this distribution does not carry yields a **visible warning**, never a silent
  pass.
- **`vision/` sits above the domain split**: spine-level documents (project vision,
  principles, roadmap) are validated by the core's structural rules only (frontmatter,
  status, indexes) and belong to no domain. Made explicit here because the UC-document
  discussion surfaced it as implicit.

**C3 — Domain router.** Lives in `routing.md`; reached from `SKILL.md` by one listing
line plus one inline trigger sentence; runs **after** the level test — L1 never reaches
it — and only when C0 reports a sibling. Steps:

1. **Fidelity / purpose.** What must the work be faithful to? *This repository's code*
   → provisional **code**. *Documents the user supplied* → **knowledge**. *Market
   evidence* → **marketing**. **A deliverable whose purpose is market-facing
   persuasion (copy, positioning, campaign material) → marketing regardless of
   source** — without this branch the marketing lens was reachable only when the
   *source* was market evidence, never when the *purpose* was marketing.
2. **Deliverable class** — only on the provisional `code` branch. Predicate on the
   deliverable, not on "audience": *is it part of this repository's own document set,
   shipping and maintained with the code* (`ai_docs/`, README, CHANGELOG, comprehension
   guides, migration notes)? → **code**. *Is it a standalone knowledge deliverable
   whose fidelity extends beyond this repo's code* (user documentation for an external
   audience, a distilled corpus)? → **knowledge**. This bounds the step the way step 3
   was bounded — the round-3 attacks (README, CHANGELOG, migration guide routed to a
   sibling lens) fall on the code side of this predicate.
3. **Build-consumed override** — only on the provisional `code` branch, never
   overriding a *marketing* or *supplied-documents* verdict: *is the deliverable a file
   the project's build or test toolchain consumes?* Executable or imported source, yes;
   committed Markdown, no.
4. **Split rule.** A request whose work must be faithful to two sources is **two units
   of work**, split before routing: the distillation (knowledge) and the design that
   cites it (code) each route alone. The router returns one lens per unit; it never
   returns two lenses for one unit.
5. **Owning tree.** A straddling artifact keeps its lens for *method* and takes this
   repository's tree and validator for *storage*. Lens and location are separate
   answers.
6. **Cross-check.** If the verdict contradicts an installed skill's `description`, the
   descriptions are wrong: fix them, never silently override the test.

Worked verdicts — every code-branch row now evaluates every step, and one row shows
step 3 flipping the answer:

| Request | 1 | 2 | 3 | Lens |
|---|---|---|---|---|
| "write the API reference docs" (hand-written, ships with the repo) | code | repo's own doc set → code | not build-consumed → no flip | **code** |
| "write user documentation for our customers' admins" | code | standalone knowledge deliverable → knowledge | n/a (left code branch at 2) | **knowledge** |
| "write the API reference docs" (generated — the work edits docstrings in source) | code | repo's own doc set → code | **build-consumed: yes → confirms code** | **code** |
| "write a comprehension guide for the auth module" | code | repo's own doc set → code | not build-consumed → no flip | **code** |
| "turn these vendor specs into a technical design" | split (step 4): spec = supplied docs; design = this repo | — | — | **knowledge** for the distillation; **code** for the design, citing it (UC3) |
| "write the pricing page copy from our market research" | **purpose: market-facing → marketing** (step 1) | never reached | never reached | **marketing**; file stored in this repo's tree (step 5) |
| "write the launch blog post from the release notes" | purpose: market-facing → marketing | never reached | never reached | **marketing** |

**C4 — Shared-slot ownership (cite, never copy).** Each governance slot has one owning
document per project; a second domain **references** it and adds only its delta.
Realized by (a) the domain-tagged `features_history.md`, which makes an *ANALYSIS*
owner locatable from another lens, (b) **one added clause in `review.md` §Reviewing**
(P1): a fact restated in an artifact when another document owns it is a finding, and
the conformance statement names the owner instead of repeating the fact, and (c) C5
naming for everything the tagged index does not reach (guides, canonical docs — a
declared residual, see Residuals). **Declared residual — stale citations**: between
reviews, nothing detects that a cited owner changed; no reverse index, no hash on a
cross-domain cite. Candidate extension evaluated in P2: **optional pinning** — cite
with version (`SPEC_x v1.2`) so `stale` can flag drift the way it already does for
guides via `source_hash`. Optional, so no ceremony ratchet; the mandatory `cites:`
field stays rejected.

**C5 — Domain-qualified naming.** A document whose meaning differs by domain is never
referred to by a bare name ("threat model", `principles.md`, `handoff.md`, "vision").
A convention enforced by review — recorded under `## Patterns` in
`strategic/architecture.md` (the heading that exists there; round 3 caught the earlier
text targeting a heading from the template instead).

**C6 — Drift guard.** The spine is authored once as **`scripts/sdlc_core.py`** and
applied as **three verbatim copies**, one per distribution, with `sdlc_check.py` and
`mkt_check.py` as thin domain entry points. Membership is an explicit per-file
manifest (file → the distributions that must match it), never "all"; a file leaving
the set is a reviewable change. The guard fails CI on any divergence. **Honest cost,
accepted by the owner**: until P5, an edit is applied three times and the test catches
a missed copy; P5's impact map evaluates the build-time single-file copy step that
collapses this (distinct from the rejected package generator, which generated whole
packages).

**C7 — Root migration.** Relocate a project's docs root, reversibly. Dry-run by
default; refuses a dirty git tree; moves and rewrites references but never deletes;
both roots stay readable throughout. Presupposes the root parameter (P2b).

## Impact

Phases 1, 2 and 3 are file-level concrete and are what this analysis authorises.
**P2b, P4, P5, P6 and P7 each require their own impact map before implementation.**

### Phase 1 — Contract (documentation; one behavioural change, in `init.js`)

| Path | Change | Why |
|---|---|---|
| `ai_docs/vision/project_vision.md` | GATE | the v7 amendment is already drafted (North Star **and** Actors); P1 runs the blind check on the full amended text and the owner promotes or reverts. No drafting work remains here. |
| `skills/agentic-sdlc-skill/routing.md` | ADD | C0 (§0: sibling detection, fail-open) + C3 (the six steps and the worked-verdict table above) |
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | listing line + one inline trigger sentence for `routing.md`, placed after the level test in Rule Zero; C5 naming rule |
| `skills/agentic-sdlc-skill/review.md` | MODIFY | C4(b): the restated-fact clause in §Reviewing |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | optional `domain:` and `checks:` in the ANALYSIS frontmatter + canonical header; per-domain `id:` prefix; `default_domain:` in the README template frontmatter |
| `scripts/init.js` | MODIFY | seeds `default_domain: code` in `ai_docs/README.md` frontmatter (create-only, second init never overwrites); on detecting a sibling, writes a separate additive pointer file and prints the second ladder — `writeIfNotExists` untouched (T1). |
| `scripts/test_clients.js` | MODIFY | assert create-only preserved, sibling path additive, `default_domain` seeded once (TS11) |
| `package.json` | MODIFY | `routing.md` added to `files[]` — an unlisted support file cannot reach a consumer; without this row P1's headline deliverable ships to nobody (round-3 F-1) |
| `ai_docs/strategic/architecture.md` | MODIFY | Doctrine row's `Where` list gains `routing.md` (C0, C3); Template-source and Validator rows note `domain:`/`checks:`/`default_domain:` (C1); C5 under the existing `## Patterns`. No new pathless rows — a convention is not a component (round-3 F-11). |
| `ai_docs/INDEX.md` | REGENERATE | P1 adds an ADR under `architecture/` (in `MANIFEST_DIRS`, `:46`); stale manifest is an error (`:866-870`) |
| `ai_docs/strategic/features_history.md` | REGENERATE | P1 changes this ANALYSIS's status; stale index is an error (`:861`) that would redden `test_plan.py`'s own-repo regression (`:228-233`, asserts `rc == 0` at `:233`, runs `strict=False` so only errors bite) |
| `ai_docs/architecture/ADR_2026-07-31_multi_domain_core.md` | ADD | neutral core + overlays; drift guard over generator; `ai_docs/` surviving root; project-level `default_domain`; exclusive-vs-portable rule-set split |

### Phase 2 — Domain rule sets (no root change)

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | ADD | the neutral core (C6): dispatch, **sections-data for all three domains**, the portable-check registry, `default_domain` resolution (absent → `code`), per-domain `seen_ids` (`:803`, `:813-816`), the **syntactic** column predicate — the domain column in `build_index` is emitted only when at least one analysis *writes* a `domain:` field, so the generated file is a function of the tree alone, identical from every entry point, and byte-identical on every existing tree |
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` | MODIFY | becomes the code-domain entry point over the core; code + knowledge portable checks implemented here (marketing's implementations follow in P4; an unavailable check warns visibly) |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | MODIFY | split into shared invariants + per-profile assertions, against the **measured** kb failure set: `Ran 34 tests — FAILED (failures=9, errors=4)` — 4 errors from missing `architect.md`; 8 anchor-string failures (`Comprehension checkpoint`, `Comprehend (code, autonomous)`, `Design review gate`, `HANDOFF_[feature].md`, the guide-router line, `consult the guide router`, `PROPOSE distilling a guide`, `Isolate the work`); 1 for the second missing overlay file `tdd.md` |
| `skills/agentic-sdlc-skill/scripts/test_domain_rules.py` | ADD | TS2, TS3, TS4, TS10; TS9's static half lands in the invariant battery |
| `skills/agentic-sdlc-skill/scripts/test_golden_regression.py` + `scripts/fixtures/golden_ai_docs/` | ADD | TS1's host and its frozen corpus, named per the hard gate; baseline captured from the pre-change validator **before the first P2 edit** |
| `skills/agentic-sdlc-skill/scripts/test_plan.py` | MODIFY | own-repo regression (`:228-233`) is in the blast radius |
| `skills/agentic-sdlc-skill/evals/scenarios/domain_router_verdicts.md` | ADD | TS9's behavioural half (non-gating, like every scenario in that harness) |
| `skills/agentic-sdlc-skill/ENFORCEMENT.md` | MODIFY | §2's copied-file CI recipe currently copies `sdlc_check.py` alone; after the core split that copy fails on import. Recipe rewritten to copy both files; TS12 exercises the copied invocation. (Round-3 F-2 — the guarantee UC5 states, broken on the documented path.) |
| `package.json` | MODIFY | `scripts/sdlc_core.py` in `files[]`; a packed-file-list assertion joins the P2 gate rather than waiting for P7 (round-3 F-1) |
| `ai_docs/strategic/architecture.md` | MODIFY | Validator row: core + entry-point structure (C2, C6) |

**Blast radius.** Consumers of `list_analyses`: `cmd_validate` (per-analysis loop),
`cmd_check` (forwards), `cmd_gate` (`:1185`, status-only — ruled: no domain filter),
`build_index` (`:306`). Test-side: `test_skill_invariants.py`, `test_plan.py`
(`:228-233`). `test_session_start.py` moves to **P2b's** radius (it reads
`sc.ORIENT_DOCS` directly at `:159` plus eight hard-coded `ai_docs/` seeds), since P2
changes no root handling. External consumers: the CLI entry points in `ENFORCEMENT.md`
(now in the table) and `init.js`; names and exit codes unchanged.

### Phase 2b — Docs root becomes a parameter

Prerequisite of P4 (mkt reads `mkt_docs/`) and of C7 (a migration tool must read both
roots, or it cannot verify either side). **Why the parameter exists is worth stating,
because it reads like the opposite of this feature:** `ai_docs/` remains the ONE
surviving root and the recommended default. The parameter exists so the tools can
*reach* a legacy root long enough to validate and move it — not to bless a second
permanent home. That is why `init.js` gains no rename knob (below): handing users a
way to create new roots would manufacture the fragmentation the feature exists to end.

**Resolution order — explicit beats guessed** (the `--hybrid` precedent):
1. `--docs-dir NAME` on every subcommand that takes `--root`.
2. `AGENTIC_SDLC_DOCS_DIR` — CI/test seam only, same status as `AGENTIC_SDLC_KB_ROOT`.
3. Discovery: walking up from the start path, the first directory matching a known
   candidate (`ai_docs`, `mkt_docs`).
4. Default `ai_docs`.

Discovery is evaluated **per directory level**, walking up: the first level carrying
any candidate decides. A `mkt_docs/` in the working directory therefore wins over an
`ai_docs/` further up — the nearer root is the one the user is standing in.

**Two candidates at the SAME level → refuse, naming both.** A mid-migration project has
exactly this shape, and silently picking one would validate half a project and print
CLEAN. Refusing is the only answer that cannot be mistaken for a verdict. Ambiguity
across different levels is not ambiguity: the nearer one wins, by the rule above.

The env var is read **per invocation**, not at import. `DEFAULT_KB_ROOT` reads its env
at import time and that is a known wart: it makes the value untestable without
reloading the module, and repeating it here would make TS14 impossible to write
honestly.

**Three constants stop being constants** — named because "derive it" hides a signature
change:
- `SKIP_DIRS` (`:48`), consumed at `:366` in the tree walk: becomes a function of the
  resolved name (`skip_dirs(docs_dir)`), since the docs root must stay excluded from
  the source walk whatever it is called.
- `ORIENT_DOCS` (`:227`), consumed at `:1548` **and read directly by
  `test_session_start.py:163`**: becomes `orient_docs(docs_dir)`. That test asserts the
  confinement contract by comparing against this constant, so it moves with it.
- `REVIEW_LOG_REL` (`:89`), used in messages and in the review-log lookup.
- `find_project_root` (`:242`) returns the root AND the docs dir it matched. Its three
  call sites are `cmd_gate` (`:1333`), `cmd_orient` (`:1544`) and `main` (`:1633`) —
  all internal, none in the batteries, so the return-type change is contained. It is
  still a public name re-exported by `sdlc_check.py`: the change is listed here rather
  than discovered by a consumer.

**What must NOT follow the parameter.** The agent-global KB store
(`DEFAULT_KB_ROOT / "ai_docs" / "reference"`, `sdlc_core.py:607` and `:1422`) is
client-agnostic and shared across lenses: a project renaming its docs root must not
move it. Asserted by a test, not by care.

**Blast radius — all 50 core occurrences classified** (`grep -c ai_docs sdlc_core.py`
= 50; each line inspected):

| Class | Count | Lines | Change |
|---|---|---|---|
| Path construction | 18 | 170, 246, 254, 255, 338, 355, 551, 593, 599, 652, 658, 664, 925, 1101, 1152, 1421 (+2 KB-root below) | derive from the resolved name |
| User-visible strings & prefix tests | 12 | 53, 64, 89, 228–231, 570, 1029, 1031, 1104, 1113, 1117, 1338 | derive: a message naming `ai_docs/` on a `mkt_docs/` project is a wrong instruction, and `cmd_gate`'s exempt prefix (`:1338`) would stop exempting the docs tree |
| Tree-walk exclusion | 1 | 49 (`SKIP_DIRS`) | derive, or `stale` walks the docs root as source and reports every doc as a modified area |
| **Agent-global KB root** | 2 | 607, 1422 | **unchanged on purpose** |
| Docstrings / `--help` | 17 | 17, 18, 20, 251, 252, 550, 592, 1081, 1538, 1588, 1592, 1605, 1606, 1616 | say "the docs root (default `ai_docs/`)" |

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | MODIFY | the 50 sites above; `find_project_root` returns the root AND the docs dir it matched, so no caller re-derives it |
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` | MODIFY | one docstring line |
| `skills/agentic-sdlc-skill/scripts/test_session_start.py` | MODIFY | 19 sites: it reads `sc.ORIENT_DOCS` directly (`:159`) and seeds eight hard-coded `ai_docs/` paths — the module most coupled to the constant |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | MODIFY | 22 sites (own-repo assertions stay on `ai_docs`; the parameterized ones move) |
| `skills/agentic-sdlc-skill/scripts/test_plan.py` | MODIFY | 16 sites |
| `skills/agentic-sdlc-skill/scripts/test_domain_rules.py` | MODIFY | 21 sites |
| `skills/agentic-sdlc-skill/scripts/test_golden_regression.py` | UNCHANGED | 7 sites, all inside the frozen corpus: TS1's whole job is the default path |
| `scripts/init.js` | UNCHANGED | 25 sites. Deliberate: see the opening paragraph |
| `skills/agentic-sdlc-skill/ENFORCEMENT.md` | MODIFY | one line documenting `--docs-dir` on the CI recipe |
| `ai_docs/strategic/architecture.md` | MODIFY | Validator-core row: the root is resolved, not assumed |

**Tests owed (TS14–TS17), beyond TS1 staying byte-identical:**
- TS14 resolution order: flag beats env beats discovery beats default; a `mkt_docs`-only
  tree is found without a flag.
- TS15 ambiguity: both roots present → non-zero exit, both named, no verdict printed.
- TS16 isolation: the agent-global KB reference dir is unaffected by `--docs-dir`.
- TS17 derived surfaces: on a renamed root the generated headers, the `orient` doc set,
  `REVIEW_LOG_REL`, `SKIP_DIRS` and `cmd_gate`'s exempt prefix all name the resolved
  root — asserted per surface, because each was a separate hard-coded string.

**New threat.** T7 — *a wrong root silently validates an empty tree and prints CLEAN.*
Mitigation: `require_ai_docs` keeps failing fast (it exists for this), the two-candidate
case refuses, and `--strict` still fails on a missing root. TS15 is the proof.

### Phase 3 — kb overlay rebuilt on the core

| Path | Change | Why |
|---|---|---|
| `skills/kb-agentic-skill/scripts/sdlc_core.py` | ADD | the core, verbatim |
| `skills/kb-agentic-skill/scripts/sdlc_check.py` + `test_plan.py`, `test_session_start.py`, `test_skill_invariants.py` (3 test modules; `evals/run_behavioral.py` is a driver) | REPLACE | knowledge entry point + batteries on the core |
| `skills/kb-agentic-skill/review.md` | MODIFY | split: shared discipline stays spine; `architect.md`/Capability-Ledger clauses become the code profile, knowledge profile replaces them |
| `skills/kb-agentic-skill/templates.md` | MODIFY | knowledge doctrine wired to the P2 sections-data: `Knowledge Taxonomy Ledger`, `## Sources and Verification` |
| `skills/kb-agentic-skill/taxonomy.md`, `distillation.md`, `reconciliation.md` | MODIFY | wired to the core's vocabulary |
| `skills/kb-agentic-skill/scripts/init.js` | MODIFY | same first-wins defect, its own copy (`:22,121,126`); seeds `default_domain: knowledge` |
| `skills/kb-agentic-skill/package.json` | MODIFY | `sdlc_core.py` in `files[]` |
| `skills/kb-agentic-skill/evals/scenarios/architect_rules_before_impact.md`, `unmapped_never_grounds_missing.md` | REPLACE | they assert on `src/notify.py#Notifier`; replaced by knowledge scenarios |

kb carries zero field projects and its work is preserved (commit `77ce756`; verified
bundle `skill_sdlc/kb-agentic-skill_2026-07-31.bundle`), so it proves the core first.

### Phases 4-7 — targets *(own impact map required before each)*

| Phase | Target | Note |
|---|---|---|
| 4 | `mkt_check.py` → thin entry point over `sdlc_core.py`; marketing portable-check implementations (`ledger`/`budget`/`funnel`/`trace`) enter the registry; `mkt_agentic_sdlc/scripts/init.js` (`:24,119,124`, same first-wins defect; seeds `default_domain: marketing`); mkt `package.json` `files[]` | `mkt_check.py` survives as the CI entry point. Depends on P2b. |
| 5 | monorepo consolidation; C6 drift guard lands with its per-file manifest; **evaluates the build-time single-file copy step** (UC4's "one file" made literal); Component Map row for C6 | `agentic-sdlc-skill` survives (95 commits, 27 tags, v1.19.0, published npm, field projects). mkt joins via `git subtree`; kb joins as content (history preserved by the bundle). No repository deleted. |
| 6 | root migration (C7); Component Map row for C7 | opt-in; `mkt_docs/` supported throughout |
| 7 | publish | three packages, names unchanged, no unpublish. `GUIDE_release.md` governs. |

**Interim drift window (P3→P5).** The guard cannot exist before P5 while P3/P4 create
core copies. Mitigation: at the end of P3 and P4, a **per-file hash comparison** of the
core across working copies (shape of `sha256_file`, `:169-176`), recorded in the Diary.
A file-list comparison would have caught neither historical drift event.

### Residuals, declared

- **Multi-lens protocol pointer** (round-3 F-10): the always-loaded `CLAUDE.md`/
  `GEMINI.md`/`AGENTS.md` still carries the first init's ladder; the sibling path adds
  a separate file the clients do not auto-load, plus printed instructions — a manual
  merge step. UC1 pays until the user merges. Accepted over the alternative (an `init`
  that mutates user-authored root files — the T1 exclusion).
- **UC2/UC3's real mechanism** is C5 naming + the C4(b) review clause; the domain-tagged
  index reaches ANALYSIS files only (round-3 F-15). TS10 asserts exactly that much.
- **The guide router** (`ai_docs/reference/INDEX.md`) — the surface read on the
  mandatory path every L2/L3 task — gains no domain column (compatibility);
  domain-qualified naming (C5) is its whole mitigation. Stated so the owner accepts the
  residual knowing which surface it lands on (round-3 F-18).
- `build_manifest` keeps its directory set; canonical-doc retrieval stays
  domain-tagged via C5 naming only.
- **Stale cross-domain citations**: nothing fires between reviews (C4 residual);
  optional pinning is the P2 candidate.
- The agent-global KB root stays a single shared store; a same-filename collision
  across lenses remains a `--strict` failure until a later feature owns it.

### Not impacted (asserted, then tested)

Existing `agentic-sdlc` projects: docs root unchanged, subcommand names and exit codes
unchanged, no `default_domain` line → `code`, no `domain:` fields → no column emitted,
routing not reached at L1 and not loaded without a sibling, `ENFORCEMENT.md` copied-file
recipe still works. TS1 + TS12 are the proof.

## Security and Threat Model

Surfaces: **filesystem** (migration tool; `init.js`), **supply chain** (three packages
from one source), **integrity of a security control** (the mandatory risk check
becomes domain-resolved).

| # | Threat | Mitigation |
|---|---|---|
| T1 | A tool destroys or misplaces user data. | C7: dry-run default, dirty-tree refusal, never deletes, never invoked from install/init/postinstall. `init.js` stays create-only — the sibling pointer is additive, `default_domain` seeding is create-only. TS8, TS11. |
| T2 | Domain-resolving the mandatory risk check silently disables it. | Resolution is **project-level and deterministic** (C1): same answer from every entry point — the round-3 counter-case (two lenses, two verdicts on one file) is structurally closed. Absent everything → `code`, asserted by TS2. Each rule set names its own risk section (C2); TS4 asserts the **positive** case (a knowledge/marketing analysis missing *its* risk section errors). TS1 catches any change on existing artifacts. Imported checks are monotonic — they can add findings, never relax the owner's requirements. |
| T3 | Cross-domain retrieval returns the wrong document. | C5 naming; the syntactic, tree-determined domain column in `features_history.md`. Unreached surfaces are the declared residuals above, severity stated honestly (the guide router is the mandatory-path one). |
| T4 | Publishing ships the wrong content. | `files[]` stays an explicit per-file allowlist, **updated in the same phase that adds each file** (P1 `routing.md`, P2/P3/P4 `sdlc_core.py`); packed-file assertion joins the P2 gate; full TS7 at P7. |
| T5 | Consolidation loses history. | mkt: `git subtree`, archive only after merge. kb: preserved by a verified bundle plus commit `77ce756`; the single-machine retention residual was assessed and **accepted by the owner (2026-07-31)** — recorded because an accepted risk is a decision, not an oversight. The deleted GitHub remote was empty; that fact says nothing about the local work, and the two must not be conflated. |
| T7 | A wrong docs root silently validates an empty tree and prints CLEAN (P2b). | Resolution is explicit-first (`--docs-dir` > env > discovery > `ai_docs`); `require_ai_docs` keeps failing fast, which is the reason it exists; two candidate roots in one tree refuse with both named rather than picking one; `--strict` still fails on a missing root. TS15 is the proof. The agent-global KB store never follows the parameter (TS16). |
| T6 | Drift guard bypassed. | Guard fails CI over a named core file present in every distribution; per-file manifest; P3→P5 window declared with per-file hash checkpoints. |

No new external input parsed; no authN/authZ, cryptography, network or personal-data
surface.

## Action Plan

- [x] **P0 — Safety.** kb work committed (`77ce756`) and bundled; single-machine
      retention risk assessed and **accepted by the owner, 2026-07-31**. Remaining
      before any repository action: confirm mkt's clone retains 3 commits + 2 tags.
- [x] **P1 — Contract.** Vision v7 blind-checked and APPROVED; `routing.md` (C0+C3)
      written and listed in `files[]`, reached from `SKILL.md` by a listing line and a
      Rule-Zero cross-cutting bullet (which also carries C5); `review.md` restated-fact
      clause; templates (`domain:`, `checks:`, `default_domain:`, `F-`/`K-`/`M-` id
      prefixes); `init.js` sibling path additive + create-only, `test_clients.js` TS11
      (3 cases, 11/11 green); Component Map rows (Doctrine, Template source, Project
      seeder) + C5 under `## Patterns`; ADR; both indexes regenerated. Batteries 75/75.
- [x] **P2 — Core + rule sets.** TS1 corpus + baseline captured from the pre-change
      validator and committed BEFORE the first edit (`25a2367`), then green through
      every step after it. `sdlc_core.py` carries the spine (sections-data ×3, check
      registry, project-level default resolution, per-domain ids, syntactic column
      predicate, `section_body`); `sdlc_check.py` is the thin code entry point and
      implements `code.threat_model` + `knowledge.sources`; `test_domain_rules.py`
      (TS2/TS3/TS4/TS10/TS13, 16 cases); TS9's static half in the invariant battery and
      its behavioural half in `evals/scenarios/domain_router_verdicts.md`;
      `ENFORCEMENT.md` recipe rewritten + TS12; `files[]` + TS7's file-list half in the
      node battery. **102 python + 12 node, green.** Battery profile split deferred to
      P3 (see the Diary).
- [x] **P2b — Root parameter.** Impact map written and self-reviewed first (all 50
      core sites classified), then implemented: `--docs-dir` / `AGENTIC_SDLC_DOCS_DIR`
      / per-level discovery / `ai_docs` default; `ai_path()` threads the resolved name;
      `SKIP_DIRS`, `ORIENT_DOCS`, `REVIEW_LOG_REL` and the two generated headers became
      functions of it; ambiguity refuses; the agent-global KB does not follow.
      `test_docs_root.py` (TS14–TS17, 14 cases). 116 python + 12 node, TS1 unchanged.
- [x] **P3 — kb on the core.** Overlay rebuilt on the shared spine; the battery became
      shared + PROFILE-driven (the split deferred from P2, landed where it had a
      consumer); kb's gate green — 136 tests, 10 declared skips, from 9 failures + 4
      errors.
- [x] **P4 — mkt on the core.** `sdlc_core.py` verbatim + `mkt_check.py` as the
      marketing OVERLAY (not thin: the document model is genuinely this domain's).
      Golden transcript byte-identical; mkt gains the spine commands, `--docs-dir`,
      the spine doctrine and portable marketing checks. 148 tests green.
- [x] **P5 — Drift guard.** `shared_files.py` + `shared_manifest.json` +
      `test_drift.py`: 15 shared files, LF-normalized hashes, identical manifest in all
      three. Verified it bites. The monorepo consolidation is NOT done — see Residuals.
- [x] **P6 — Migration.** `migrate` shipped: dry-run default, refuses a dirty tree,
      refuses to overwrite, never deletes, never edits user-authored pointers. TS18.
- [x] **P7 — Publish (prepared).** Versions bumped (1.20.0 / 1.0.0 / 0.3.0),
      changelogs written, `npm pack --dry-run` correct for all three (22/22/21 files,
      no dev-only assets). `npm publish` itself needs the owner's 2FA.

Gate between phases: TS1 and the **static** batteries green (the behavioural harness
is non-gating by design); from P5 on, TS5 as well.

## Test Strategy

| # | Test | Asserts |
|---|---|---|
| TS1 | **Golden non-regression.** Host `scripts/test_golden_regression.py`, corpus `scripts/fixtures/golden_ai_docs/` (committed; baseline from the pre-change validator, captured before P2's first edit). `validate`/`check` findings and exit code unchanged, paths normalized; includes the no-`domain:`-anywhere case proving no column is emitted. | UC5, T2 |
| TS2 | **Default resolution.** No `default_domain` line and no `domain:` field → code rules: mandatory risk check errors, ledger advisory fires. A `default_domain: knowledge` line flips the default; a `domain:` field overrides both. C0 fail-open: single lens → router never read. | T2, C1 |
| TS3 | **Mixed tree, entry-point invariance.** Code + knowledge + marketing artifacts in one `ai_docs/`: 0 errors / 0 warnings under `--strict`, **and byte-identical generated files from the code and knowledge entry points** (marketing joins at P4). Includes two domains each carrying their own `F-001` (mkt's templates seed no `id:`, so the collision is two-domain). | coexistence, C1, UC7 |
| TS4 | **Per-domain mandatory sections, both directions.** Knowledge-only tree demands no code sections; a knowledge analysis missing `## Sources and Verification` errors. Same pair for marketing (at P4). | T2 |
| TS5 | **Drift guard.** Every manifest file byte-identical across the distributions it names — including `sdlc_core.py` in all three; a mutation fails; an absence the manifest does not name does not. | UC4, T6 |
| TS6 | **Profile batteries.** All three static batteries green from their own directories. | release gate |
| TS7 | **Packaging.** `npm pack --dry-run` per package: expected list, no dev-only files, no cross-domain leakage. Runs at P7 **and** its file-list half runs at every phase that edits a `files[]`. | T4 |
| TS8 | **Migration tool.** Dry-run writes nothing; dirty tree refused; old root readable; fully reverted by `git checkout`. | UC6, T1 |
| TS9 | **Routing.** Static half in the invariant battery: the C3 procedure and the worked-verdict table are internally consistent — every code-branch row evaluates every step, at least one row's outcome depends on step 3, the reverse pair (comprehension guide vs customer docs) routes differently. Behavioural half in `evals/scenarios/domain_router_verdicts.md`, non-gating. | UC1 |
| TS10 | **Cross-domain locatability.** From the tagged `features_history.md`, a lens identifies the ANALYSIS owning a fact in another domain; the `review.md` restated-fact clause is asserted present (the only mechanism against copies). | UC2, UC3, C4 |
| TS11 | **`init.js` create-only.** Existing root files never modified; sibling path writes an additive file; `default_domain` seeded once and never overwritten by a second init. | T1, UC5, C1 |
| TS12 | **Copied-file CI recipe.** The `ENFORCEMENT.md` §2 copy procedure, executed as documented, runs and returns the same exit code as the in-place invocation. | UC5 |
| TS13 | **Portable checks.** A knowledge-owned doc with `checks: [marketing.ledger]`: the check runs (P4) or warns visibly as unavailable (before P4); imported checks add findings only — a doc failing an imported check while satisfying its owner's sections shows both facts. | UC8, C2 |

| TS14 | **Root resolution order** (P2b). `--docs-dir` beats `AGENTIC_SDLC_DOCS_DIR` beats discovery beats the `ai_docs` default; a `mkt_docs`-only tree is found with no flag. | P2b, C7 |
| TS15 | **Ambiguous root** (P2b). Both candidate roots in one tree: non-zero exit, both named, no verdict printed — a mid-migration project must not be half-validated and called CLEAN. | T7 |
| TS16 | **KB isolation** (P2b). The agent-global KB reference dir is unaffected by `--docs-dir`: a project rename never moves a store shared across lenses. | T7 |
| TS17 | **Derived surfaces** (P2b). On a renamed root, the generated headers, the `orient` doc set, `REVIEW_LOG_REL`, `SKIP_DIRS` and `cmd_gate`'s exempt prefix each name the resolved root — asserted per surface, because each is a separate hard-coded string today. | P2b |

TS1 gates P2 and is the most important test here: it is the only evidence that users
who did nothing are not paying for this refactor.

## Diary / Current State

- **2026-07-31 — opened.** From a publish-readiness review of `kb-agentic` (spine still
  code-domain, release gate red). Root cause: the copy-fork structure of all three
  skills.
- **2026-07-31 — six design reviews across three rounds, all FAIL, 76 findings, 76
  real; round cap reached.** Narrative in `ai_docs/audit/reviews/REVIEW_LOG.md`. The
  round-3 BLOCKs and their dispositions, all folded here: packaging (`files[]`) never
  updated → in every phase that adds a file; `ENFORCEMENT.md` copied-file recipe broken
  by the core split → recipe rewritten + TS12; per-distribution `domain:` default
  non-deterministic on shared trees → **project-level `default_domain`** (owner
  decision); TS3/TS4 scheduled before their rule sets existed → sections-data for all
  three domains authored in P2; TS1 fixture unnamed → host + corpus named; "spine edit
  lands in one file" false → success signal restated honestly, single-file step
  evaluated at P5 (owner decision); Vision paragraph quoted text already amended →
  P1 row is now the gate, not the drafting; C0 unowned and mis-phased → doctrine-owned,
  ships in `routing.md` at P1; router table step-3 cells inconsistent, step 2 unbounded,
  no split rule → C3 rebuilt (purpose branch, deliverable-class predicate, split rule,
  full table re-derived).
- **2026-07-31 — Vision v7 path.** Blind round 1 PASS-conditional (fixes applied);
  confirming round **FAIL** — same four classes re-broke through the fixes; amendment
  reshaped to change facts and add no gate (sibling gate removed from North Star; veto
  restated as the *one triage authority* Non-Goal, by function). Pre-existing Vision
  defects split to **F-023** (`ANALYSIS_vision_shape_rules.md`). v7 remains PENDING its
  confirming blind round — P1's first item.
- **2026-07-31 — owner Q&A refinements.** Multi-domain documents: one owner, N
  consumers by citation; UC docs have three legitimate homes (feature section /
  Vision `## Actors`, which sits above domains / distilled corpus owned by knowledge).
  `vision/` explicitly spine-level in C2. **Portable checks** (`checks:`, UC8) adopted:
  exclusive sections vs composable monotonic checks — closes the "budget table in a
  knowledge doc that nobody's validator checks" gap. Stale-citation risk declared as
  C4 residual with optional pinning as P2 candidate.
- **2026-07-31 — Vision v7 APPROVED.** Four blind rounds. The decisive one found that
  the amendment had made the North Star declare a family the admission test could not
  admit — every Goal, Actor and Signal stood at software-methodology altitude, so a
  knowledge sibling ruled REJECT under the document's own gate. Fixed with Goal 7,
  Actor 4 and the owning-domain rule; a narrow round confirmed **a knowledge sibling now
  rules ADMIT on its merits while a work-management sibling is still refused three times
  over**, and found two BLOCKs inside those new clauses (capturable ownership,
  self-referential Goal 7), both fixed before promotion. **P1's Vision item is therefore
  closed**: the amendment is approved and binding, and the residual Vision defects are
  F-023's, not this feature's.
- **2026-07-31 — P1 shipped.** All rows of the P1 impact table are done, with two
  deliberate deviations, both recorded rather than silently absorbed:
  (a) the **Validator row** of the Component Map was left untouched — in P1 the
  validator does not read `domain:`/`checks:`/`default_domain:` at all, so noting them
  there would describe behaviour that does not exist yet; it moves with the core in P2,
  where that row is already in the impact table.
  (b) `init.js` seeds `default_domain: code` **through the template block**, not
  through new code: `templateFor` already extracts the README body from
  `templates.md`, so the frontmatter arrives with it and `writeIfNotExists` stays
  exactly as it was (T1). The only new behaviour in `init.js` is the sibling path.
  The sibling note is `AGENTIC_MULTI_LENS.md` — additive, not auto-loaded by any
  client, and it carries the code ladder for hand-merging only when a protocol pointer
  written by another lens already existed. TS11's three cases assert precisely that:
  the seed, the create-only survival of an edited default, silence when no sibling is
  installed, and the untouched sentinel pointer when one is.
- **2026-07-31 — P2 shipped.** The order was the point: the golden corpus and its
  baseline were captured from the **pre-change** validator and committed on their own
  (`25a2367`) before `sdlc_check.py` was touched, so every later step had something
  real to be measured against. The split itself is a `git mv` — `sdlc_check.py` became
  `sdlc_core.py` and a new thin entry point took the old name — which keeps the history
  on the code and makes the diff readable. TS1 stayed byte-identical through it.
  Four deviations from the P2 impact table, all deliberate:
  (a) **The battery profile split moves to P3.** Only two assertions actually broke,
  and both were pointing at the wrong module rather than at the wrong behaviour: an
  invariant reading the validator's source (now `sdlc_core.py`) and a spy patched on
  the entry point's re-export instead of on the core that resolves it — the second
  would have passed on broken code, which is why it was fixed rather than relaxed. The
  shared-vs-profile structure has no consumer until kb's overlay runs the battery, so
  it lands with kb.
  (b) **TS12 lives in `test_golden_regression.py`**, not in the invariant battery: it
  must spawn the validator as documented, and the invariant battery's guarantee is that
  it never does. `ENFORCEMENT.md` §5 claimed the whole battery was subprocess-free — a
  claim this feature would have made false, so it was corrected rather than left to rot.
  (c) **The Component Map's Validator row became two rows** (core + entry point): one
  row cannot state a contract that is now split, and the split is exactly what a reader
  needs to know before copying the file into CI.
  (d) **`.gitattributes` gained a fixtures rule.** The corpus and the baseline are
  compared byte for byte; a checkout that rewrote their line endings would fail TS1 for
  a reason that has nothing to do with the validator.
  Two portable checks ship: `code.threat_model` and `knowledge.sources`. Both add
  findings only — TS13 asserts an imported check cannot change the owning domain's
  error/warning contract, and that a check this distribution does not carry warns
  visibly instead of passing.
- **2026-08-01 — P2b shipped.** The map was written and self-reviewed before any edit,
  and it paid: the review caught that "derive it from the parameter" was hiding a
  signature change on three constants and on `find_project_root`, and that discovery
  ambiguity was under-specified. Implemented as designed. Two things the map got wrong,
  recorded because a map that is never checked against the outcome is decoration:
  (a) **it over-predicted the test blast radius.** `test_plan.py`, `test_domain_rules.py`
  and most of `test_skill_invariants.py` needed no edit at all — their `ai_docs` strings
  are fixture paths on the default root, and the default is unchanged. Only the two
  assertions that read the constants directly moved (`ORIENT_DOCS` → `orient_docs()`,
  `REVIEW_LOG_REL` → `review_log_rel()`).
  (b) **`find_project_root` kept its return type.** Threading the resolved name through
  a module-level value set once per invocation (the shape `_ENTRY_POINT` already uses)
  left every signature in the batteries intact; changing the return type would have
  bought nothing and broken a re-exported public name.
  One real bug during the work, caught by TS1 rather than by review: a blind
  search-and-replace rewrote `kb_root / "ai_docs" / "reference"` — the agent-global
  store — because the pattern matched inside it. It is now a literal with a comment
  saying why, and TS16 asserts it.
- **2026-08-01 — P3 through P7.** The family is built. What each phase actually cost,
  and what it found:
  **P3 (kb).** kb was not a skill needing a rebase, it was a skeleton: a byte-copied
  1489-line validator, a SKILL.md that had lost every doctrine added since it was
  forked, and a node battery asserting its sibling's identity. Fixing it forced the
  right shape on the battery — shared tests plus a per-distribution PROFILE. The
  Poka-Yoke is that spine capabilities cannot be dropped by editing your own profile
  (a shared test refuses it); only genuine overlays can be declared absent, in one
  visible line. kb's 10 skips each trace to such a line.
  **P4 (mkt).** Before touching mkt, its own golden corpus and transcript were captured
  from the pre-change validator — the same instrument agentic had and mkt did not. It
  stayed byte-identical throughout. mkt's entry point is deliberately NOT thin: a
  marketing plan is not a set of ANALYSIS documents, so the document model stays its
  own and only the spine converges.
  **P5 (drift guard).** It caught a real divergence on its first run and one on demand:
  a one-line edit to a copy of the core fails it. The manifest's content is identical
  in all three distributions, which is what turns a forgotten copy into a diff.
  **P6 (migrate).** Writing its tests found a design defect: the ambiguous-root guard
  refused `migrate` — the one command that exists to end the ambiguity. Exempted, with
  the reason recorded.
  **P7.** Versions, changelogs and pack lists are ready; publishing needs the owner.
  Three literals were the recurring disease all the way through — the installed skill
  directory, the entry-point filename, the docs-root name, the expected default domain.
  Each is now derived from the manifest or the profile, because a literal in a shared
  file is precisely how three copies start asserting one distribution's identity.
- **Open — declared, not hidden:**
  1. **The monorepo is not built.** The three repositories are still separate; the
     drift guard is what makes that survivable, and it is a guard, not a merge. The
     `git subtree` consolidation and anything on GitHub is the owner's to run.
  2. **`npm publish` ×3 needs the owner's 2FA.** 1.19.0 was already awaiting
     publication before this work; npm is at 1.17.0.
  3. **kb ships thin.** Its overlay files (`taxonomy.md` 30 lines, `distillation.md`
     20, `reconciliation.md` 16) are stubs. Its process spine is now real and tested;
     its knowledge METHOD is not yet written. Publishing it is a judgement call the
     owner should make knowingly.
  4. kb does not claim `comprehension_guides`; mkt does not claim `architect_pass` or
     `taxonomy_pass`. Declared in each profile.
- **Next step:** the owner's call on 1, 2 and 3.
