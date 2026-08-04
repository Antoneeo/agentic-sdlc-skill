# ai_docs — reading guide

Must-reads for this repository, in order. The full manifest of canonical docs is
`INDEX.md` (generated — regenerate with `sdlc_check.py index`, never edit by hand).

1. `reference/INDEX.md` — the guide router: which guide already governs the work you are about to do (generated).
2. `vision/project_vision.md` — why the skill exists + the four-layer product thesis (check its Status first).
3. `strategic/capabilities_and_positioning.md` — what agentic-sdlc already does better, parity, and positioning vs superpowers.
4. `vision/roadmap_evoluzione_agenti.md` — the active evolution roadmap (subagents, operative guides, devPNT seam).
5. `strategic/architecture.md` — how the package is built.
6. `audit/handoff.md` — the workstream registry: what is open, on which branch, where each stopped. **Generated** — the truth is one `audit/HANDOFF_[feature].md` per open workstream (its frontmatter IS the row, its body the resume details); edit those and run `sdlc_check.py index`.

Directory purposes: `vision/` (project direction and feature visions),
`strategic/` (architecture and feature catalog), `architecture/` (ADRs — why a
structural decision was taken, and what was rejected), `functional/`
(devPNT-generated functional snapshots), `reference/` (operative guides),
`solutions/` (per-feature analyses, discovery-by-grep), `audit/` (audit plan and
handoff).
