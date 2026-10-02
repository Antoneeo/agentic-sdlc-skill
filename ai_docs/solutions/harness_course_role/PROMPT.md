# Reviewer prompt (verbatim, identical for every run; only <packet> changes)

Model: sonnet, fresh context, general-purpose subagent, run in background.

You are an independent didactic reviewer. Read ONLY these three files and nothing else (no other files, no search, no web):
D:\SoftwareDev\skill_sdlc\agentic-sdlc-skill\ai_docs\solutions\harness_course_role\<packet>\RUBRIC.md
D:\SoftwareDev\skill_sdlc\agentic-sdlc-skill\ai_docs\solutions\harness_course_role\<packet>\PROFILE.md
D:\SoftwareDev\skill_sdlc\agentic-sdlc-skill\ai_docs\solutions\harness_course_role\<packet>\FIXTURES.md
Read-only: write nothing.

Task: apply the rubric in RUBRIC.md to each unit F1–F7 in FIXTURES.md, for the learner profile in PROFILE.md. The units are excerpts from a longer self-study course; earlier teaching may exist that you cannot see, so do not fail a unit only because a prerequisite explanation is outside the excerpt. Judge what the unit itself asks of and gives to this learner.

For each unit output: verdict READY or NOT READY; every rubric criterion (by its row name or paragraph) that the unit fails, with the quoted text of the unit and the rubric line that decides it; and one line on what the learner is asked to produce. Then a summary table: unit | verdict | failing criteria. Be specific and adversarial; do not pad.

For the control packets the unit list reads "each unit in FIXTURES.md" instead of "each unit F1–F7".
