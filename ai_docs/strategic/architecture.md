---
description: Stack, package structure and architectural patterns of the skill repository.
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

## Patterns
- Documentation-first workflow.
- Risk-proportional triage before workflow selection.
- Vision-guided request gating with DRAFT/APPROVED local Vision and devPNT M-VISION authority in Hybrid mode.
- Standalone filesystem governance plus optional devPNT symbiosis.
- Client roster as data: one `CLIENTS` entry per supported AI client (Claude Code, Gemini CLI, Codex, Google Antigravity); detection, install, uninstall and protocol-pointer writing all iterate that one registry, so they can never disagree. Clients sharing a home directory (Antigravity on `~/.gemini`) disambiguate with the optional `skillsSubdir` and `homeMarker` fields rather than a special case in the callers.
