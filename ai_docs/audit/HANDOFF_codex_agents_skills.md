---
workstream: F-075 Codex skills in $HOME/.agents/skills
level: L3
branch: fix/codex-agents-skills
status: PLANNED
since: 2026-10-23
next: Owner answers Q1 and Q5 in the ANALYSIS; POSIX run of the probe harness (FS-7); then RED tests in scripts/test_clients.js on the other PC.
details: ANALYSIS_codex_agents_skills.md · audit/requests/REQUEST_codex_agents_skills.md · harness_codex_agents_skills/
updated: 2026-10-23
---

## Resume state

Analysis only on this PC (R2). Design in `solutions/ANALYSIS_codex_agents_skills.md`;
evidence harness in `solutions/harness_codex_agents_skills/`. No code changed.

## Next command

On the other PC: fetch, check out `fix/codex-agents-skills`, then
`node scripts/test_clients.js` after writing the F-075 cases (they must fail first).
