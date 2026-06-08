# Project Architecture

## Stack
- Node.js scripts for project initialization and package lifecycle hooks.
- Markdown-based skill instructions, templates, and generated agent protocol files.
- Optional devPNT integration for governed plans and versioned artifacts.

## Directory Structure
- `skills/agentic-sdlc-skill/`: Native skill definition and operational workflow.
- `references/`: Reusable Markdown templates for analysis, architecture, feature history, and Vision documents.
- `scripts/`: Install and initialization automation.
- `ai_docs/vision/`: Project-level and feature-level Vision documents.
- `ai_docs/strategic/`: Architecture, existing feature catalog, and feature history.
- `ai_docs/audit/`: Audit plan and session handoff state.
- `ai_docs/solutions/`: Feature analysis documents.

## Patterns
- Documentation-first workflow.
- Vision-guided request gating.
- Hybrid filesystem/devPNT governance.
