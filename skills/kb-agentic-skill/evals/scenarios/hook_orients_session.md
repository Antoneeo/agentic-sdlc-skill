---
id: hook_orients_session
expected: the SessionStart hook emits a bounded orientation; with no ai_docs it stays silent (fail-open)
---
## Setup
- ai_docs/README.md: Reading guide -- start with INDEX.md then the handoff.
- ai_docs/INDEX.md: Canonical manifest -- (list of docs).
- ai_docs/reference/INDEX.md: Guide router -- GUIDE_widget_style.md : when styling a widget.
- ai_docs/audit/handoff.md: Handoff -- last session shipped Unit 3; next is the eval harness.
## Prompt
(Run `python <skill>/scripts/sdlc_check.py orient --root <fixture>` -- this is what a wired SessionStart hook runs.)
## Pass criteria
- The orient output includes the README, INDEX, guide router, and handoff sections plus the Rule-Zero triage line.
- Output is bounded (size-capped), labeled repo-sourced.
- Running orient against an empty dir (no ai_docs/) prints nothing and exits 0 (fail-open) -- it never blocks the session.
