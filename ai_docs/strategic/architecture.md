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
| Project seeder | Turn an empty repository into a governed one | Creates the `ai_docs/` layout, the per-client protocol pointer and the generated `INDEX.md`; extracts every document body from the template source rather than carrying its own copies. Create-only, without exception: on a project a sibling lens already seeded, the second ladder goes into an additive note the clients do not auto-load, never into the existing pointer | `scripts/init.js` (bin `agentic-sdlc-init`) |
| Skill deployer | Put the runtime skill folder where each detected client will load it, and take it back out | Copies to every client the roster detects; the npm `files` allowlist bounds what can be copied — an unlisted support file cannot reach a consumer | `scripts/postinstall.js`, `scripts/preuninstall.js` |
| Template source | Single home for every document body the methodology writes | One fenced block per document; the seeder extracts them. Two copies drift, so there is one. Carries the multi-lens fields — optional `domain:`/`checks:` on an artifact, `default_domain:` seeded once at project level — so a single-domain project never writes any of them and behaves exactly as before | `skills/agentic-sdlc-skill/templates.md` |
| Doctrine | State the process an agent follows: triage, phases, write triggers, gates | `SKILL.md` is the contract and the only always-loaded file; each discipline is one support file, invoked by pointer, read only when its trigger fires. `routing.md` adds the multi-lens case: which sibling lens owns a unit of work — detected by the agent from its own skills directory (no code, no validator), read only when a sibling is installed, fails open to the loaded lens | `skills/agentic-sdlc-skill/SKILL.md`, `skills/agentic-sdlc-skill/architect.md`, `skills/agentic-sdlc-skill/guides.md`, `skills/agentic-sdlc-skill/vision.md`, `skills/agentic-sdlc-skill/tdd.md`, `skills/agentic-sdlc-skill/debugging.md`, `skills/agentic-sdlc-skill/elicitation.md`, `skills/agentic-sdlc-skill/review.md`, `skills/agentic-sdlc-skill/dispatch.md`, `skills/agentic-sdlc-skill/routing.md` |
| Validator core | Answer mechanically whether `ai_docs/` is well-formed, current and complete — identically in every distribution of the family | Stdlib-only, no network, no LLM; `check`/`validate`/`index`/`stale`/`mark`/`gate`/`plan`/`orient`. Generated indexes are rebuilt, never hand-edited, so they cannot drift. Holds the domain data for ALL lenses (mandatory sections, risk slot, id prefix) and the portable-check registry, so a mixed tree gets one answer whichever lens asks; the project default is read once from the docs root's `README.md`. The docs root itself is resolved once per invocation (`--docs-dir` > env > nearest recognized root > `ai_docs`), so paths, messages, generated headers and the write gate all name the same directory; two roots side by side refuse rather than half-validate. The agent-global KB store is the one path that never follows it | `skills/agentic-sdlc-skill/scripts/sdlc_core.py` |
| Validator entry point | Name the domain this distribution implements and the portable checks it carries | Thin on purpose: no rule lives here, so a domain cannot fork the core by accident. Runnable name and exit codes unchanged for every existing consumer; the core alone is runnable too, and a half-copied validator fails at import rather than passing green | `skills/agentic-sdlc-skill/scripts/sdlc_check.py` |
| Invariant battery | Fail the build when the skill's own doctrine stops being wired | Static, zero-LLM, zero-network, zero-subprocess — a failing test is always a real regression, never flakiness. Dev-only: deliberately outside the package allowlist | `skills/agentic-sdlc-skill/scripts/test_*.py`, `skills/agentic-sdlc-skill/evals/run_behavioral.py` |

## Patterns
- Documentation-first workflow.
- Risk-proportional triage before workflow selection.
- Vision-guided request gating with DRAFT/APPROVED local Vision and devPNT M-VISION authority in Hybrid mode.
- Standalone filesystem governance plus optional devPNT symbiosis.
- Domain-qualified naming (multi-lens projects): a document whose meaning differs by domain — "threat model", "vision", `principles.md`, `handoff.md` — is never referred to by its bare name. Qualify it with its domain or name its path. A convention enforced by review, not by the validator: the generated `features_history.md` tags ANALYSIS files only, and everything else (guides, canonical docs) is reachable across lenses solely by how it is named.
- Client roster as data: one `CLIENTS` entry per supported AI client (Claude Code, Gemini CLI, Codex, Google Antigravity); detection, install, uninstall and protocol-pointer writing all iterate that one registry, so they can never disagree. Clients sharing a home directory (Antigravity on `~/.gemini`) disambiguate with the optional `skillsSubdir` and `homeMarker` fields rather than a special case in the callers.
