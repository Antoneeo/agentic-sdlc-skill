# Project Vision

## North Star
- Agentic SDLC must help AI coding agents deliver software changes that remain aligned with the project's long-term intent, not only with the latest local request.

## Target Users
- Developers using AI agents for feature development, audits, refactors, and maintenance.
- Teams that need lightweight but explicit governance across Claude Code, Gemini CLI, Codex, Cursor, and similar tools.

## Goals
- Enforce documentation-first development without making the process dependent on one specific agent runtime.
- Keep project Vision, architecture, implementation plans, tests, and handoff state synchronized.
- Make strategic drift visible before implementation starts.

## Non-Goals
- The skill is not a full ALM or issue-tracking system.
- The skill should not force heavyweight governance for trivial edits.
- The skill should not hide conflicts between a user request and the declared project Vision.

## Success Signals
- New projects initialized with the skill include explicit Vision documents.
- Feature analysis includes a clear Vision alignment section.
- Agents stop and surface conflicts when a request violates declared goals or non-goals.
