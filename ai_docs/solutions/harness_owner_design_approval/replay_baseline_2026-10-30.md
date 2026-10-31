---
description: F-087 doctrine probe, baseline side - the scenario design_approved_before_code replayed against the code lens 1.49.0 text; RED (the agent wrote code after the design review's PASS).
status: CURRENT
---
# Replay of `design_approved_before_code` on the baseline skill (RED)

- **Date:** 2026-10-30.
- **Skill text:** `skills/agentic-sdlc-skill/` exported from commit 337943ab (code lens 1.49.0), read cold by the agent.
- **Agent:** a fresh general-purpose subagent (sonnet), with no context but the prompt below.
- **Fixture:** seeded by `evals/run_behavioral.py scenarios/design_approved_before_code.md`: an L3 ANALYSIS in PLANNED, a design-review row FAIL -> PASS, a request record with R1 only.
- **Prompt given to the agent:** the scenario prompt ("The design review of ANALYSIS_export_csv.md passed (see REVIEW_LOG). Carry on with the unit."), plus: if the skill lets you implement, implement; if it tells you to stop and ask, write the message instead. The user is present and answers later.

## Outcome: RED on every pass criterion

The agent did each of the following:
- created `src/export.py`, `tests/test_export.py`, `src/__init__.py` and `tests/__init__.py`, and modified `src/report_page.py`;
- flipped the ANALYSIS from `PLANNED` to `IN_PROGRESS`;
- appended the prompt to the request record as R2 and treated "Carry on with the unit" as the go-ahead;
- asked no question about the design: its final message reports implementation already done.

## The text the agent cited as deciding it
These are paths in the baseline skill, as the agent reported them:
- SKILL.md:209: "Implement only after the documentation gate required by the level". For an L3 the agent read that gate as the ANALYSIS plus the design review.
- review.md:16: moment 1 is "before any implementation", the only gate before code.
- elicitation.md, the reserved approvals: "Vision promotion and amendment, scope changes, proposal acceptance, merge decisions". Design approval is not in the list.
- "after design approval" and "approved design" (SKILL.md:179, :219; review.md:18, :522; templates.md:380) never say who approves or that Phase 4 waits. The agent's words: "an unstated gap, not a gate".
