---
feature: F-074
analysis: ANALYSIS_vision_interview.md
---
# E2E test: Vision born from an owner interview

## What changed, in user terms
When the agent is about to write a Vision — for the project, a feature, a course, a
marketing plan or a devPNT milestone — it first asks you six questions and asks you to
approve a one- or two-sentence north star in your own words. It writes no Vision before
you approve that sentence. A new project now starts with a Vision stub, not with a Vision
the agent made up.

## Environment and preconditions
- The four packages at the versions in this change: `@antoneeo/agentic-sdlc-skill` 1.43.0,
  `@antoneeo/kb-agentic-skill` 1.26.0, `@antoneeo/mkt-agentic-sdlc` 0.21.0,
  `@antoneeo/course-creator` 0.1.0-beta.7, installed from the tagged release.
- An empty folder for each new-project scenario; for S2, a folder seeded from
  `skills/agentic-sdlc-skill/evals/scenarios/vision_needs_owner_interview.md`
  (`python evals/run_behavioral.py scenarios/vision_needs_owner_interview.md` prints the
  seed and the prompt).
- An agent client with the skill installed (Claude Code, Codex, Gemini or Antigravity).

## New-behavior scenarios

### S1 — FS5: a new project starts with a stub
Steps: 1. In an empty folder run `agentic-sdlc-init`. 2. Open `ai_docs/vision/project_vision.md`.
3. Repeat in empty folders with the kb, mkt and course installers (mkt: `mkt_docs/vision/MKT_VISION.md`).
Expected: each file holds only a title, `Status: DRAFT` and a comment saying it awaits the
owner interview — no North Star, Goals or Non-Goals text.
Result:

### S2 — FS1–FS3: one sentence and a spike do not produce a Vision
Steps: 1. Open the seeded folder from the preconditions in the agent client. 2. Send the
scenario's prompt ("Assistants should be able to draw. The spike works, so write the vision
for milestone M12."). 3. Read the agent's reply.
Expected: no Vision file is written. The agent asks, in one numbered set, about the problem
(a concrete case), the benefit, the actors including who takes the initiative, a success
signal with its starting value, the boundaries, and the known constraints — and it asks
whether the product Vision's "never sees the technical format" applies here, instead of
writing it in. It asks you to approve a north star in your own words before drafting.
Result:

### S3 — FS3–FS4: after your approval, the Vision traces to your answers
Steps: 1. Continue S2: answer the questions, then approve the north star the agent proposes
(or write your own). 2. Let the agent write the Vision.
Expected: your answers and the approval appear verbatim in `ai_docs/audit/requests/`; the
Vision's North Star is your approved sentence; every Non-Goal and constraint names where it
comes from (your answer, a quoted higher Vision, or an inference you confirmed).
Result:

### S4 — FS6: a Non-Goal is scope, not a ban
Steps: 1. During S3, answer the boundaries question with "the assistant must never show raw
diagram code".
Expected: the agent does not record it as a Non-Goal; it treats it as a constraint (with you
as its source) or an Invariant, and asks if needed.
Result:

### S5 — FS7: unattended, the unit stops instead of writing a Vision
Steps: 1. Run the S2 prompt in a scheduled or non-interactive agent run (no one can answer).
2. Open the run's output and `ai_docs/solutions/`.
Expected: no Vision file or Vision text exists; the analysis the run opened is marked
`BLOCKED on the user`, and the questions it could not ask are listed for the owner.
Result:

## Regression scenarios

### R1 — An L3 that cites an approved Vision gains no interview
Steps: 1. In a project with an APPROVED `project_vision.md`, ask for an L3 feature whose
benefit the Vision already names.
Expected: the agent runs the usual elicitation round (or its skip path, citing the Vision);
it does not open the six-question interview.
Result:

### R2 — L1 and L2 work is unchanged
Steps: 1. Ask for a typo fix, then a small bug fix with a clear cause.
Expected: no interview, no Vision questions.
Result:

### R3 — An existing Vision is never overwritten
Steps: 1. In a project that already has `ai_docs/vision/project_vision.md`, run the installer again.
Expected: the file is unchanged.
Result:

### R4 — Validation stays clean on a new project
Steps: 1. After S1, run `python <skill_dir>/scripts/sdlc_check.py check --root .`.
Expected: no errors; the three Vision files are reported as DRAFT advisories only.
Result:

## Already covered by automated tests
- Doctrine wiring and the seeded stub, in every lens: `test_skill_invariants.py`
  `test_vision_born_from_owner_interview` (four batteries).
- Skip path, gates, question order, bootstrap wording, Hybrid bullet and the scenario's
  pass criteria: `skills/agentic-sdlc-skill/scripts/test_vision_interview.py`.
- Installer behaviour in general: `scripts/test_clients.js` (code), course `scripts/test_clients.js`.
