<!-- SHADOW generated from devPNT (e_tdd_antigravity_client v1.0) - do not edit by hand -->
# E-TDD: Antigravity 2.0 Client Support

**Type:** Technical Design Document
**Milestone:** (NEW) Client Roster — Antigravity 2.0 support (single unit)
**Frames:** milestone_vision_antigravity_client (DRAFT)
**Derived from:** e_isp_antigravity_client v1.0 (D-A recommended solution)
**Governed by:** p_tm_antigravity_client T1–T8
**Status:** DRAFT
**TDD discipline:** tests-first for the detection/target logic (RED before GREEN); prose/doc edits (README/CHANGELOG) are exempt (recorded, per tdd.md).

## Design per file

### `scripts/lib.js`
1. **Generalize `skillTarget`** (T2):
   `function skillTarget(client){ return path.join(client.home, ...(client.skillsSubdir? client.skillsSubdir.split('/') : ['skills']), 'agentic-sdlc'); }`
   — default preserves the existing three targets exactly (`skillsSubdir` undefined → `['skills']`). Splitting on `'/'` keeps cross-platform join correctness for `config/skills`.
2. **Per-entry detection marker** (T1/T3): extend `clientDetected` so an entry may override the fs-existence test:
   `const homePathToCheck = client.homeMarker || client.home;`
   `return commandExists(client.cmd) || Boolean(process.env[client.envVar]) || fs.existsSync(homePathToCheck);`
   — existing entries omit `homeMarker` → unchanged behavior (T7).
3. **New CLIENTS entry** (append after `codex`):
   `{ key:'antigravity', label:'Google Antigravity', cmd:<PENDING Q1 — Antigravity CLI binary name>, home: process.env.ANTIGRAVITY_HOME || path.join(os.homedir(), '.gemini'), envVar:'ANTIGRAVITY_HOME', skillsSubdir:'config/skills', homeMarker: path.join(process.env.ANTIGRAVITY_HOME || path.join(os.homedir(),'.gemini'), 'config', 'skills'), reload:<PENDING Q3 — Antigravity skill-reload instruction> }`
   — `homeMarker` = `~/.gemini/config/skills`: detection fires only when the Antigravity skills dir (or CLI binary, or ANTIGRAVITY_HOME) is present, NEVER on bare `~/.gemini` (T1). skill-target → `~/.gemini/config/skills/agentic-sdlc` (T2).

### `scripts/init.js`
- Add one key to `protocolFiles`: `antigravity: 'AGENTS.md'`. No other change; `protocolContent` reused (T5). Idempotent `writeIfNotExists` means codex+Antigravity co-present write AGENTS.md once.

### `scripts/postinstall.js`, `scripts/preuninstall.js`
- NO CODE CHANGE. Registry consumers; the new entry + generalized `skillTarget` flow through. (Verified: both call only `skillTarget`/`clientDetected`.)

### `scripts/test_clients.js` (ADD, dev-only, not shipped — not in package.json `files`)
Node stdlib (`node:test` + `assert`, or a plain assert script runnable via `node scripts/test_clients.js`; E-TDD picks `node:test` for parity with the release battery's runnability). Cases:
- `skillTarget` for claude/gemini/codex unchanged (byte-equal to pre-change) — T7 regression guard.
- `skillTarget(antigravity)` === `~/.gemini/config/skills/agentic-sdlc` (with HOME stubbed) — T2.
- `clientDetected` with only bare `~/.gemini` present (no `config/skills`, no CLI, no env) → gemini TRUE, antigravity FALSE — T1 the critical case.
- `clientDetected(antigravity)` TRUE when `~/.gemini/config/skills` exists OR `ANTIGRAVITY_HOME` set OR the CLI is on PATH — T3.
- install→uninstall round-trip (temp HOME): postinstall creates the antigravity target, preuninstall removes exactly it, gemini target untouched — T2/T7.

## P-TM coverage table
| Threat | Design mechanism | Test |
|---|---|---|
| T1 double-install | `homeMarker` = `config/skills`, not bare home | bare-`~/.gemini` case: antigravity FALSE |
| T2 wrong uninstall | `skillsSubdir:'config/skills'` → distinct target | target-equality + round-trip test |
| T3 detection FP/FN | detect on marker OR cmd OR env | detection matrix test |
| T5 pointer drift | reuse single `protocolContent`; only filename maps | (code review — no new body) |
| T6 allowlist | no shipped file added; test is dev-only | npm pack --dry-run in release battery |
| T7 regression | default `skillsSubdir`/no `homeMarker` for existing 3 | byte-equal target test + round-trip |
| T8 reload msg | Antigravity-specific `reload` string | (code review) |

## Verification (declared)
Automated Node test battery (`scripts/test_clients.js`) is added — this closes the P-TM verification-stance requirement (the repo previously had no Node tests). Run: `node scripts/test_clients.js` (or `node --test scripts/`). It is dev-only (NOT in `package.json` `files`, per the test_plan.py/test_session_start.py precedent). The E-ISP's "no shipped file added" holds. Manual smoke (install into a temp HOME, list the two `.gemini` subpaths) is the fallback if `node:test` is unavailable, with the reason recorded.

## Closure surfaces (not implementation — listed for the release unit)
README client roster + install-path list (add `Google Antigravity: ~/.gemini/config/skills/agentic-sdlc/`); CHANGELOG entry; GUIDE_release triple-bump (package.json + gemini-extension.json + CHANGELOG). `check --hybrid` CLEAN + skill eval battery green before DONE.

## PENDING owner inputs (resolved in round 2 — recorded here for traceability)
- **Q1** Antigravity CLI binary name for `cmd`: **`agy`** (Antigravity CLI, announced successor to Gemini CLI; Windows `%LOCALAPPDATA%\agy\bin`). Do NOT key detection on bare `antigravity` (some Linux installers ship `/usr/bin/antigravity`); rely on `agy` + homeMarker + env.
- **Q2** Env-var override: **`ANTIGRAVITY_HOME`** (mirrors the existing per-client `envVar` pattern).
- **Q3** Reload string: **`Restart Antigravity, or run "agy skills reload", to load it. Invoke by asking for Agentic SDLC.`**
