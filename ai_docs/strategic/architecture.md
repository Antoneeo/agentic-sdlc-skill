---
description: Stack, package structure and architectural patterns of the skill repository.
status: CURRENT
---
# Project Architecture

## Stack
- Node.js scripts for project initialization and package lifecycle hooks.
- Markdown-based skill instructions, bundled support files, templates, and generated agent protocol files.
- Python standard-library validator for optional mechanical SDLC checks.
- Optional devPNT integration for governed M-VISION, Master Plan, Action Plan, and versioned artifacts.

## Directory Structure
- `skills/agentic-sdlc-skill/`: Native skill definition, support templates, enforcement notes, and validator script copied into agent skill directories.
- `references/`: Reusable Markdown templates for analysis, architecture, feature history, and Vision documents.
- `scripts/`: Install and initialization automation.
- `ai_docs/vision/`: Project-level and feature-level Vision documents.
- `ai_docs/strategic/`: Architecture, existing feature catalog, and feature history.
- `ai_docs/audit/`: Audit plan and session handoff state.
- `ai_docs/solutions/`: Feature analysis documents.

## Patterns
- Documentation-first workflow.
- Risk-proportional triage before workflow selection.
- Vision-guided request gating with DRAFT/APPROVED local Vision and devPNT M-VISION authority in Hybrid mode.
- Standalone filesystem governance plus optional devPNT symbiosis.
