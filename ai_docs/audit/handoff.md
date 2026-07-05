# Handoff
Date: 2026-07-05 (UTC)
Branch: main
Agent: Claude (Opus, orchestrator) — same-session doc-only implementation; independent §4.5 design reviews + §4.6 code review via fresh-context subagents

## State: M2.A7 (review-input hardening) IMPLEMENTED + reviewed; 1.13.0 staged NOT released; devPNT plan-DONE proposals + Phase-2 devPNT mirror PENDING
**M2 amendment — review reads AND proves Vision + Use-Cases + Threat Model** (node M2.A7 under the already-DONE M2 milestone — a governed amendment, not a new milestone). `review.md`: for an analysis/design review, §Requesting now takes **Vision + use-cases/user-needs + threat model** as explicit inputs, and §Reviewing requires the reviewer OUTPUT to carry a **conformance/traceability statement** (each constraint → satisfied+where | finding; PASS invalid on "found nothing"; scoped — plain code reviews stay findings-only). `SKILL.md §3`: author-trace rule. `templates.md` ANALYSIS: `## Use Cases / User Needs` section (the Standalone UC home; Minimum-sections floor left unchanged). Governed full Hybrid: E-ISP `e_isp_review_input_hardening` v2.0 (deep, 3 rounds — round-1 BLOCK caught the missing Standalone UC home; v2.0 added the output-evidence half at the owner's steer) + E-TDD v1.0 (light) + §4.6 code review PASS (self-caught + reverted a Minimum-sections regression). `check --hybrid` CLEAN, eval battery 51/51, shadow `SHADOW_e_tdd_review_input_hardening_v1.0.md` exported. **Pending for the owner:** (a) accept the M2.A7→DONE + M2→DONE plan proposals in the GUI; (b) the **1.13.0 release** — bump staged as `[Unreleased - 1.13.0]` in CHANGELOG; per `GUIDE_release`: triple-bump → verification battery → `git_push_tag.bat` → merge → `npm publish` (owner 2FA); (c) **Phase 2 — the devPNT-project mirror**: the same discipline in `devPNT/agent/core/mcp_system_prompt.md` §4.5 + the `devpnt-tech-reviewer` output format, done through devPNT's own governance + `setup_mcp.bat` redeploy (NEVER hand-edit the deployed `~/.claude` copies — see the earlier reverted mistake). No git commit/push this session.

---
### Prior session history: Antigravity 2.0 client (released as v1.12.0)
**Client Roster — Google Antigravity 2.0 support** (a NEW milestone beyond M4): the install engine now serves Antigravity. Implementation + tests + docs + closure done and `check --hybrid` CLEAN. Two things remain for the owner: (a) approve the devPNT proposals in the GUI (M-VISION promotion → Master Plan milestone → Action Plan node), (b) the release (version bump is staged in the working tree at 1.12.0; publish is the owner's 2FA step). No git commit/push was made this session.

## What was built (Antigravity client)
Implemented against the accepted **E-TDD `e_tdd_antigravity_client` v1.0** (shadow exported to `ai_docs/solutions/SHADOW_e_tdd_antigravity_client_v1.0.md` before coding, per Hybrid shadow discipline). Owner Q1–Q3 resolved: CLI binary `agy`, env override `ANTIGRAVITY_HOME`, Antigravity-specific reload string.
- **`scripts/lib.js`**: new `antigravity` CLIENTS entry (label 'Google Antigravity', cmd 'agy', home `ANTIGRAVITY_HOME || ~/.gemini`, envVar 'ANTIGRAVITY_HOME', skillsSubdir 'config/skills', homeMarker `~/.gemini/config/skills`, reload string). Generalized `skillTarget` (optional `skillsSubdir`, default 'skills') and `clientDetected` (optional `homeMarker`) — backward-compatible; the three existing clients omit both fields and are byte-identical (verified by T7 tests + `git diff --ignore-all-space`).
- **`scripts/init.js`**: `antigravity: 'AGENTS.md'` added to `protocolFiles`; single `protocolContent` reused (no per-client drift).
- **`scripts/postinstall.js` / `preuninstall.js`**: NO code change (pure registry consumers — verified; the new entry + generalized skillTarget flow through).
- **`scripts/test_clients.js`** (NEW, dev-only, NOT shipped): Node `node:test` battery, 8 cases, covering P-TM T1 (bare `~/.gemini` → gemini TRUE / antigravity FALSE, asserted unconditionally + mutation-proven), T2 (skill-target `~/.gemini/config/skills/agentic-sdlc` + install/uninstall round-trip), T3 (detection matrix marker|env|cmd), T7 (existing 3 unchanged).
- **Docs + release surfaces**: README (roster + install-path list + protocol-file note), CHANGELOG (`[1.12.0]`), triple-bump (package.json + gemini-extension.json to 1.12.0). `package.json` `files` changed from wholesale `"scripts"` to the explicit 4 lifecycle scripts so the dev-only `test_clients.js` is never packaged (npm pack --dry-run confirms exclusion). `ai_docs/solutions/antigravity_skills_guide.md` given a SUPERSEDED banner (plugin/mcp_config model → skills model; not deleted).

## The shared-home collision (the load-bearing decision)
Antigravity's global skills root `~/.gemini/config/skills/` lives UNDER `~/.gemini`, the home the legacy `gemini` client claims. Naive addition would double-detect/double-install (P-TM T1). Resolved by a distinct entry + two backward-compatible registry generalizations (`skillsSubdir`, `homeMarker`), NOT by merging or a fake separate home. ADR `adr_2026-07-03_antigravity_gemini_home_collision` (Proposed → awaiting GUI approval).

## Verification (all green)
- Node battery `node scripts/test_clients.js`: **8/8 pass** (T1 mutation-tested non-vacuous).
- Skill eval battery `python -m unittest discover -s skills/agentic-sdlc-skill/scripts -p "test_*.py"`: **51/51 OK** (no regression).
- init.js scratch smoke: rc0, fresh-project `check` CLEAN.
- `python skills/agentic-sdlc-skill/scripts/sdlc_check.py check --hybrid`: **CLEAN** (validate rc=0, stale rc=0). 4 pre-existing baseline warnings (roadmap/principles DRAFT; two functional docs missing `status:`) — carried debt, files untouched by this change.
- Independent fresh-context review (review.md): round 1 FAIL (1 real MAJOR — vacuous T1 guards), FIXED + mutation-verified → PASS. Full row + resolution in `ai_docs/audit/reviews/REVIEW_LOG.md`.

## PENDING owner action (devPNT GUI — MCP resolution is disabled)
Approve these proposals in the devPNT GUI, in order:
1. **M-VISION promotion**: `milestone_vision_antigravity_client` DRAFT → APPROVED (owner confirmed the Vision Gate).
2. **Master Plan milestone**: create the "Client Roster — Antigravity 2.0" milestone referencing the approved M-VISION (via `devpnt_create_milestone`).
3. **ADR** `adr_2026-07-03_antigravity_gemini_home_collision`: Proposed → Accepted.
(Proposal IDs are reported in the agent's closing message.) Implementation was NOT blocked on these per the owner's round-2 directive.

## Next step — the release
Version **1.12.0** (minor — new client). Per `ai_docs/reference/GUIDE_release.md`: bumps are already staged in the working tree; run the verification battery (npm pack --dry-run — confirm `test_clients.js` and `evals/`/`test_*.py` NOT listed; init smoke; check --hybrid CLEAN; eval battery green) → `git_push_tag.bat` → verify tag==HEAD → merge main → `npm publish` (USER, 2FA). Flip the CHANGELOG heading only if you prefer the `[Unreleased - X.Y.Z]` staging convention; it is currently written as the dated `[1.12.0]` entry.

## Carried debt / ops
- **Not this unit**: `ai_docs/functional/{architecture_overview,external_interfaces}.md` still lack lifecycle `status:` frontmatter (devPNT-regenerated) → 2 non-fatal `validate` warnings (check stays CLEAN). roadmap/principles still DRAFT.
- Working tree holds this unit's code + docs UNcommitted (no commit this session — owner's call). The devPNT server locks `.devpnt/*.db`: committing on the current branch (main) is fine; branch-crossing needs a worktree or a server restart (GUIDE_release trap). NOTE: the whole tree shows as modified in `git status` due to CRLF/LF churn from the devPNT server — the only REAL content changes are the files listed above (confirm with `git diff --ignore-all-space`).
- Host note: the editor's file-write tool truncated large .js writes on this Windows host mid-session; the affected files (lib.js, init.js, test_clients.js) were rebuilt via the Linux mount and re-verified (syntax + battery). No partial/corrupt file remains.
