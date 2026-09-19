---
description: Stack, package structure, component map and architectural patterns of the skill repository.
status: CURRENT
---
# Project Architecture

## Stack
- Node.js scripts for project initialization, multi-client skill install/uninstall, and package lifecycle hooks.
- Markdown-based skill instructions, bundled support files, templates, and generated agent protocol files.
- Python standard-library validator for optional mechanical SDLC checks.
- Optional devPNT integration for governed M-VISION, Master Plan, Action Plan, and versioned artifacts.

## Directory Structure
- `skills/agentic-sdlc-skill/`: Native skill definition, support templates, enforcement notes, and validator script copied into agent skill directories.
- `scripts/`: Install and initialization automation. `lib.js` is the single source for the client roster (`CLIENTS`), detection, skill-target paths and template loading; `init.js` (bin `agentic-sdlc-init`) seeds the `ai_docs/` layout, the per-client protocol pointer and the generated `INDEX.md`; `postinstall.js` (bin `agentic-sdlc-install-skill`, also the npm postinstall hook) and `preuninstall.js` copy and remove the skill for every detected client. `test_clients.js` is a dev-only `node:test` battery for the roster and the install/uninstall round-trip — deliberately absent from the package.json `files` allowlist, like the Python test batteries.
- Document templates are single-sourced in `skills/agentic-sdlc-skill/templates.md`: `init.js` extracts its fenced blocks instead of carrying inline copies. The former root `references/*_template.md` files were removed because the two copies drifted.
- `ai_docs/vision/`: Project-level and feature-level Vision documents.
- `ai_docs/reference/`: Operative guides (`GUIDE_*.md`) plus their generated router.
- `ai_docs/strategic/`: Architecture, existing feature catalog, and feature history.
- `ai_docs/audit/`: Audit plan and session handoff state.
- `ai_docs/solutions/`: Feature analysis documents.
- `ai_docs/memory/`: Generated cross-domain catalog; original documents remain authoritative.

## Component Map

The inventory the architect pass reads before searching the code (`architect.md` §2).
One row per component that owns a capability; a row is added or corrected in the same
closure that builds — or merely discovers — a component. Directories are not
components: those are in `## Directory Structure` above.

Coverage: whatever `audit/audit_plan.md` marks ANALYZED — read it, do not trust a list
restated here. Outside those areas this map is **unread, not empty**: it can never
ground a MISSING verdict, and the code is searched instead (`architect.md` §2).

| Component | Capability it owns | Contract | Where |
|---|---|---|---|
| Client roster | Know which AI clients exist, where each keeps skills, and which are installed on this machine | One `CLIENTS` entry per client is the only source of truth; detection, install, uninstall and protocol-pointer writing all iterate it, so they cannot disagree. Clients sharing a home dir disambiguate with `skillsSubdir`/`homeMarker`, never with a caller-side special case | `scripts/lib.js#CLIENTS` |
| Project seeder | Turn an empty repository into a governed one | Creates the docs layout, protocol pointer and generated indexes using the template source. Create-only: preserves existing pointers; an additive multi-lens note points to owner routing and shared memory, never merges triage scales | `scripts/init.js` (bin `agentic-sdlc-init`) and distribution copies |
| Skill deployer | Put the runtime skill folder where each detected client will load it, and take it back out | Copies to every client the roster detects; the npm `files` allowlist bounds what can be copied — an unlisted support file cannot reach a consumer | `scripts/postinstall.js`, `scripts/preuninstall.js` |
| Template source | Single home for every document body the methodology writes | One fenced block per document; the seeder extracts them. Two copies drift, so there is one. Carries the multi-lens fields — optional `domain:`/`checks:` on an artifact, `default_domain:` seeded once at project level — so a single-domain project never writes any of them and behaves exactly as before | `skills/agentic-sdlc-skill/templates.md` |
| Doctrine | State the process an agent follows: triage, phases, write triggers, gates | `SKILL.md` is the entry contract; support disciplines load by trigger. `routing.md` assigns one owner and its scale when sibling skills are present, falling back to the loaded lens. `memory.md` governs common knowledge consultation independently of sibling installation; it does not add a competing workflow | `skills/agentic-sdlc-skill/SKILL.md` and its referenced support files, including `skills/agentic-sdlc-skill/routing.md` and `skills/agentic-sdlc-skill/memory.md`; distribution equivalents |
| Validator core | Answer mechanically whether `ai_docs/` is well-formed, current and complete — identically in every distribution of the family | Stdlib-only, no network, no LLM; `check`/`validate`/`index`/`stale`/`mark`/`gate`/`plan`/`orient`. Generated indexes are rebuilt, never hand-edited, so they cannot drift. Holds the domain data for ALL lenses (mandatory sections, risk slot, id prefix) and the portable-check registry, so a mixed tree gets one answer whichever lens asks; the project default is read once from the docs root's `README.md`. The docs root itself is resolved once per invocation (`--docs-dir` > env > nearest recognized root > `ai_docs`), so paths, messages, generated headers and the write gate all name the same directory; two roots side by side refuse rather than half-validate. The agent-global KB store is the one path that never follows it | `skills/agentic-sdlc-skill/scripts/sdlc_core.py` |
| Validator entry points | Select the domain profile and compose its checks with shared knowledge integrity | Code and KB delegate to `knowledge.py`; marketing preserves ledger/budget/funnel/trace and adds common checks. Deploy entry point + `sdlc_core.py` + `knowledge.py` together: core alone is not the integrated validator. Code/KB do not certify marketing arithmetic | Code/KB `skills/agentic-sdlc-skill/scripts/sdlc_check.py`; marketing `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py` in each skill folder |
| Invariant battery | Detect regressions in doctrine wiring and CLI behavior | Local stdlib tests include subprocesses and temporary fixtures; dev-only, outside the package allowlist. Behavioral evals are a separate surface | `skills/agentic-sdlc-skill/scripts/test_*.py`, `skills/agentic-sdlc-skill/evals/run_behavioral.py` |
| Shared project memory | Discover guides, plans and decisions across domains without a second skill installation | `index` generates `memory/INDEX.md`; `recall` searches live path/domain/topics/description metadata without writes. Original authority and optional topic tags are preserved; no status aggregation, new claims, watcher or semantic search. `memory.md` governs targeted consultation and capture without a second workflow | Byte-identical `skills/agentic-sdlc-skill/scripts/knowledge.py` and `skills/agentic-sdlc-skill/memory.md` in all three skill folders; `memory_records`, `memory_index`, `memory_validate`, `memory_recall` |
| Claim ledger (knowledge) | Hold assertions with provenance and keep every disagreement visible until new information resolves it | Detect-and-hold, never decide: conflicts become symmetric CONTESTED sets; resolution only by a newer source or a `basis:`-backed ruling; ids keyed on `source#locator#qty` (text excluded), locators verified against stored bytes; empty id is advisory (L1 free). Shared engine ships in every distribution; KB owns the specialist authoring workflow | Shared `skills/agentic-sdlc-skill/scripts/knowledge.py` (ledger section); KB battery `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_claim_ledger.py` |
| Topic graph (knowledge) | Place every claim under one owning topic, navigable by abstraction | Flat `topics/` with polyhierarchy in frontmatter; edges derived from claim rows; tombstones instead of deletion; cycles refused at write, unreachable-from-root an error; generated router index (slug/description/parents/synonyms), rebuild-and-diff verified. No coverage state exists anywhere — findings only, per the work-management Non-Goal | Shared `skills/agentic-sdlc-skill/scripts/knowledge.py` (graph section), KB battery `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_kb_graph.py`; KB doctrine `distributions/kb-agentic-skill/skills/kb-agentic-skill/taxonomy.md` |
| Corpus store (knowledge) | Keep originals verbatim and make their supersession visible | Content-addressed `given/` with raw-byte digests (the LF-normalizing digest is for text only), sidecars carrying date/provenance/`supersedes:`, stored canonical extraction for non-text originals — what offset locators address; claims resting on superseded originals are reported | Shared `skills/agentic-sdlc-skill/scripts/knowledge.py` (corpus section); KB doctrine `distributions/kb-agentic-skill/skills/kb-agentic-skill/distillation.md` §1 |

## Distribution layout

One repository, three published packages. The code distribution sits at the repository
root, because that is where `ai_docs/` — the project's own governance — lives, and
governance lives once. The other two are self-contained package directories under
`distributions/`, each with its own `package.json`, `scripts/` and skill folder, so
`npm publish` works from inside them without a build step.

| Package | Where | Published as |
|---|---|---|
| code | repository root | `@antoneeo/agentic-sdlc-skill` |
| knowledge | `distributions/kb-agentic-skill/` | `@antoneeo/kb-agentic-skill` |
| marketing | `distributions/mkt-agentic-sdlc/` | `@antoneeo/mkt-agentic-sdlc-skill` |

The two grafted distributions were brought in with `git subtree`, so their history came
with them. Everything they carried that duplicated this repository's governance — a
stale copy of `ai_docs/`, protocol pointers, example projects — was removed on arrival:
keeping it would have been the exact duplication this consolidation exists to end.

## Patterns
- Documentation-first workflow.
- Risk-proportional triage before workflow selection.
- Vision-guided request gating with DRAFT/APPROVED local Vision and devPNT M-VISION authority in Hybrid mode.
- Standalone filesystem governance plus optional devPNT symbiosis.
- Domain-qualified naming (multi-lens projects): qualify ambiguous documents by domain or path. `features_history.md` tags ANALYSIS files; the shared memory catalog also exposes metadata for guides and canonical documents across domains. Discovery never substitutes for reading the original.
- Client roster as data: one `CLIENTS` entry per supported AI client (Claude Code, Gemini CLI, Codex, Google Antigravity); detection, install, uninstall and protocol-pointer writing all iterate that one registry, so they can never disagree. Clients sharing a home directory (Antigravity on `~/.gemini`) disambiguate with the optional `skillsSubdir` and `homeMarker` fields rather than a special case in the callers.
