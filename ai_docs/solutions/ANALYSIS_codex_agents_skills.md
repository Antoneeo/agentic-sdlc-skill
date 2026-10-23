---
description: F-082 - on Codex the installer copies each skill into $HOME/.agents/skills/<name>/ (the user location OpenAI documents); the old $CODEX_HOME/skills/<name> path becomes a directory link to it (older Codex keeps loading, current Codex lists it once), a pre-existing legacy folder is moved to a backup, never deleted. Four distributions here plus distill-skill.
status: PLANNED
feature: F-082
id: F-082
start_date: 2026-10-23
level: L3
branch: fix/codex-agents-skills
---
# ANALYSIS: Codex skills in `$HOME/.agents/skills`

**Level: L3 · router: `GUIDE_skill_family_changes.md` → read** (copies across the
distributions count once against the file bound; every other L3 criterion applies: the
change alters user-visible install behaviour and moves folders in the user's home, a
filesystem-sensitive area). `GUIDE_release.md` applies only at release.

Scope of this session (R2): **analysis only**; implementation runs on another PC from
this document. Elicitation: skip path for the core decision (R1, "Correggo
l'installer"). Owner questions are in §Open questions; Q1 and Q5 change the design
and must be answered before the RED tests are written.

## Objective

Make `npm i -g @antoneeo/<package>` install each skill where current Codex documents
user skills, `$HOME/.agents/skills/<name>/`, while every user who loads the skill today
from `$CODEX_HOME/skills/<name>/` (default `~/.codex/skills/<name>/`) keeps loading it,
once, at the installed version. The course "Un agente personale che ricorda e lavora con
metodo" (claim-d8) can then state that Codex loads the skills after the npm install, for
the version that ships F-082.

## Feature Vision

`ai_docs/vision/project_vision.md` (APPROVED v9). Goal: "Be installable, upgradable and
maintainable by the people who use it — on the clients they already run, without
hand-assembly". Admission test: "conforming to a client's skill layout is how the
product reaches its users". Actors served: the solo developer (one Codex on one machine)
and the team lead ("several agents, on whatever clients the team uses"). No Non-Goal is
touched.

## Evidence (probed, 2026-10-23, Windows 11, Codex 0.164.0, npm 11.4.2)

Behavioural claims below come from executed probes, kept in
`harness_codex_agents_skills/`: `probe_codex_skill_roots.js` renders the model-visible
prompt with `codex debug prompt-input` (no model call) and counts a probe skill;
S0 is the empty control and `--negate` turns every scenario red (shown: 7/7 FAIL).
`probe_npm_preuninstall.sh` installs and uninstalls a throwaway package in a temp prefix,
with a control that runs the script directly.

| # | Claim | Evidence |
|---|---|---|
| E1 | Codex 0.164.0 (latest on npm today) loads user skills from **both** `$CODEX_HOME/skills` and `$HOME/.agents/skills`. | Real-profile prompt maps `r0` = `…/.codex/skills`, `r1` = `…/.agents/skills`; harness S1, S2. The binary names the roots `codex-home-skills` and `user-agent-skills`. |
| E2 | Two real folders with the same skill name, one per root, are **listed twice**. | S3 listed=2. Doc: "If two skills share the same `name`, Codex doesn't merge them". |
| E3 | Codex **follows** a link at the legacy path to a folder outside every root. | S5 listed=1 (the only copy is reached through the link). |
| E4 | A legacy-path link to the `.agents` copy is listed **once** (deduplicated by real path). | S4 listed=1; with E3 this cannot be "link ignored". **Windows junction only; POSIX `dir` symlink not probed.** |
| E5 | A dangling legacy link is ignored without error. | S6 listed=0, exit code 0. |
| E6 | Codex 0.112.0 (installed on this PC) knows no `.agents/skills` root. | Binary string search: `.codex/skills` present, `.agents/skills` absent (0.164.0 has both). **Inferred, not executed**: 0.112.0 cannot run a model with this account and lacks `debug prompt-input`. Whether it follows links is unknown. First Codex version with the `.agents` root unknown. |
| E7 | On Windows Codex resolves `~/.agents` from the real profile and ignores `HOME`/`USERPROFILE`; Node's `os.homedir()` honours `USERPROFILE`. | A first harness run with a temp `HOME`/`USERPROFILE` did not find the `.agents` probe (that run is not kept in the harness; its header records it). Equal in normal runs. |
| E8 | Gemini CLI 0.45.2 reads `~/.agents/skills` too and prefers it over `~/.gemini/skills` for the same name. | Its bundled `docs/cli/skills.md`: "Within the same tier (user or workspace), the `.agents/skills/` alias takes precedence over the `.gemini/skills/` directory." Whether Antigravity reads `.agents`: unknown. |
| E9 | `npm uninstall -g` does not run `preuninstall` (npm 11.4.2). | `probe_npm_preuninstall.sh` (packed tarball; install, presence and removal each asserted): "PREUNINSTALL NOT RUN"; control "script runs when invoked directly". |
| E10 | Codex 0.164.0 skips a `SKILL.md` that starts with a UTF-8 BOM. | A BOM probe was not listed; the same file without BOM was. Not kept in the harness. Shipped `SKILL.md` files load today, so this is a guard for tests that write fixtures. |
| E11 | Codex hooks: `~/.codex/hooks.json` or `[hooks]` in `config.toml` (user), `<repo>/.codex/hooks.json` (project); shape `{"hooks": {"SessionStart": [{"matcher": "startup\|resume", "hooks": [{"type": "command", "command": …}]}]}}`; stdout becomes developer context; a non-managed hook is skipped until trusted in `/hooks`, and trust is tied to the hook's hash. | https://learn.chatgpt.com/codex/hooks.md ("Config shape", "Review and trust hooks", "SessionStart"), read verbatim. Not executed. |

Codex source (`openai/codex`) was not read. The docs never name `~/.codex/skills`.

## Use Cases / User Needs

- **UC1 — fresh install on current Codex** (solo developer). After `npm i -g` and a Codex
  restart, `$<skill>` works and is listed once.
- **UC2 — update over an existing install** (solo developer). They have a real
  `~/.codex/skills/<name>/`. After the update the skill is listed once, at the new
  version; nothing they put in that folder is lost.
- **UC3 — older Codex without the `.agents` root** (solo developer), fresh install or update. The skill
  still loads. Covered by the legacy link (E3 on current Codex); **unproven on an older
  Codex** (E6).
- **UC4 — Codex and Gemini on one machine** (team lead, several clients). Both clients
  load the installed version; Gemini's preference for `.agents` (E8) never serves a stale
  copy.
- **UC5 — removing the package** (solo developer). E9: npm never runs the uninstall script, and the four
  packages here ship no uninstall command (distill does). So removal is manual today for
  every client, not only Codex; this unit keeps the uninstall script correct for the new
  layout and leaves the missing command to Q4.
- **UC6 — Codex user wiring session orientation** (solo developer; only if Q5 = yes). ENFORCEMENT §4 gives
  the official hook shape and the `/hooks` trust step.

Names, bucketed: `$HOME/.agents/skills`, `$CODEX_HOME/skills`, `/hooks`, `hooks.json`
EXIST (Codex, E1, E11); the client roster, skill deployer, project seeder EXIST
(`strategic/architecture.md` Component Map); course-creator's per-file ownership EXISTS;
"legacy link" and "legacy backup" are NEW. Each UC traces to the Goal quoted above.

## Functional Spec

Trigger fires: install behaviour changes for Codex users. Terms: *new copy* =
`$HOME/.agents/skills/<name>`; *legacy path* = `<CODEX_HOME, else ~/.codex>/skills/<name>`.

- **FS-1 — where the copy goes.** When Codex is detected (detection unchanged), the skill
  is copied to the new copy. `CODEX_HOME` no longer chooses where; it still drives
  detection and names the legacy path.
- **FS-2 — the legacy path always leads to the new copy.** After the copy succeeds, the
  installer brings the legacy path to one state, by case:
  1. absent, or a dangling link → a directory link to the new copy is created
     (fresh installs included: this is what keeps an older Codex working, UC3);
  2. already resolves to the same real folder as the new copy (a link, or a parent
     folder linked by the user) → nothing; **nothing is ever removed in this case**;
  3. a live link to somewhere else → untouched; a warning names both paths;
  4. a real folder whose `SKILL.md` names this skill → moved to a dated backup outside
     every skills root, then case 1. Nothing is deleted, so files the user added survive
     (today's update overwrites the package's files but keeps added ones);
  5. a real folder that names another skill, or has no readable `SKILL.md` → untouched;
     a warning says Codex may list two entries;
  6. the link cannot be created → the legacy path stays as case 4 left it (backup made,
     path absent); a line says Codex versions without `~/.agents/skills` will not see the
     skill until Codex is updated.
  The step never fails the install. The rule is the same in all five packages: the
  legacy folder moves as a whole, so course-creator's and distill's ownership records
  travel with it into the backup and no ownership pass runs on the legacy path.
- **FS-3 — Gemini's view stays current.** On every install, an existing new copy whose
  `SKILL.md` names this skill is refreshed even when Codex is not detected, because
  Gemini prefers it (E8).
- **FS-4 — uninstall script.** When run (by hand, or by an npm that still runs it), it
  removes the legacy link if it resolves to the new copy, then the new copy. It never
  removes a real legacy folder or a backup.
- **FS-5 — sibling detection in `init`.** A sibling lens counts as installed for Codex if
  it is in the new root or the legacy root (a sibling not yet updated lives only in the
  legacy root).
- **FS-6 — repeatable.** A second install leaves the same state: one real copy, one link,
  no new backup.
- **FS-7 — POSIX gate.** If E4 does not hold on POSIX (a link at the legacy path to the
  new copy makes Codex list the skill twice there), FS-2 cases 1 and 4 skip the link on that platform (backup only) and UC3 is
  dropped there; the README says so.
- **FS-8 — documentation.** Each README that lists install paths shows
  `Codex: ~/.agents/skills/<name>/` plus one sentence on the legacy link and the backup.
  ENFORCEMENT §4 (if Q5 = yes) replaces the Codex paragraph with the official snippet
  and the `/hooks` trust step, and corrects the reason Codex is not auto-wired (§Decisions D3).

Acceptance: FS-1…FS-6 each pinned by a test in §Test Strategy; FS-7 decided by the POSIX
harness run; UC1 shown by the real-machine proof.

## Interface Contract

Trigger fires: the install console output and the folder layout are what the actor
perceives. No new command, flag or prompt. Idiom reused: one emoji-led line per event,
as `postinstall.js` prints today (`📦 Installed … at:`); course-creator keeps its own
`label: code (target)` line and adds the same sentences.

Flow, per install, for Codex: client roster detects Codex → skill deployer copies to the
new copy → deployer reconciles the legacy path (FS-2) → one line per event:

- copy: `📦 Installed Codex AI skill at: <new>` (existing line, new path);
- case 1 after case 4: `🔗 Moved <legacy> to <backup>; <legacy> now links to <new> (older Codex versions keep working).`
- case 1 on a fresh install: `🔗 <legacy> links to <new> for older Codex versions.`
- case 3: `⚠️  <legacy> links to <other>, not to <new>; left as is. Codex may list "<name>" twice.`
- case 5: `⚠️  <legacy> is not this package's folder; left as is. Codex may list "<name>" twice.`
- case 6: `⚠️  Could not link <legacy> to <new>: Codex versions without ~/.agents/skills will not see "<name>". Update Codex.`
- uninstall script: `🧹 Removed Codex AI skill at: <new>` and `🧹 Removed link <legacy>`.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| know where a client loads user skills | INADEQUATE | Client roster (`CLIENTS`, `scripts/lib.js`) — every target is `client.home` + subdir; Codex's documented root is outside its home | re-read `skillTarget` (`lib.js:138`): `path.join(client.home, ...subdir, name)` |
| know a client's previous target | MISSING | — | grep `legacy`, `previous`, `migrat` over `scripts/`, `distributions/*/scripts/`: only comments; no roster field |
| reconcile a previous target with the current one | MISSING | — | same search; the deployer only copies (`postinstall.js` `installSkill`) |
| move a folder aside without loss | MISSING | — | grep `rename`, `backup` over the same areas: none |
| create a directory link portably | MISSING | — | grep `symlink`, `junction` over the same areas: none |
| compare two paths by real location | INADEQUATE | `pathsEqual`/`pathInside` (`lib.js:469`, `:476`) compare resolved strings, not real paths | re-read: `path.resolve` + case fold, no `realpath` |
| decide which files the package owns | EXISTS in course-creator (`ownedMarker`, `installOwned`, `uninstallOwned`, course `lib.js:463-552`) and distill (`.installed-by.json`); MISSING in code/kb/mkt | not needed: FS-2 case 4 moves the whole folder, never deletes | re-read course `uninstallOwned`: it deletes unedited owned files, so it is not used on the legacy path |
| detect sibling lenses | INADEQUATE | Project seeder (`init.js` `installedSiblingLenses`) scans one root per client | re-read `init.js:177-187` |
| exercise install/uninstall under a stub home | EXISTS | `test_clients.js` (child-process postinstall/preuninstall, temp HOME) | re-read T2/T7 round-trip |

New component contracts (stated without this feature): the roster entry may declare an
absolute skills root and a list of previous roots; the deployer, after copying, makes
each previous target lead to the current one by the FS-2 rules, never deleting a real
folder.

## Impact

Blast radius of `skillTarget` (grep on the symbol in all four copies and in distill; no
symbol-graph tool for these plain scripts): `postinstall.js` (install), `preuninstall.js`
(remove + `removeGlobalOrientHooks(CLIENTS.map(skillTarget))`, which reads only Claude
settings files, so Codex targets are harmless there), `init.js` `installedSiblingLenses`
(root `:177-187`, kb `:170`, mkt `:168`, course `init.js:38-43`), `lib.js`
`wireOrientHook`/`wireGlobalOrientHook`/`wireGlobalRemindHook` (Claude only,
unaffected). The `install-skill` bin is `postinstall.js`.

| # | File(s) | Change |
|---|---|---|
| 1 | `scripts/lib.js` ×4 (root, kb, mkt, course — per-lens copies) | Codex entry: `skillsRoot: path.join(os.homedir(), '.agents', 'skills')`, `legacySkillsRoots: [path.join(home, 'skills')]`; `skillTarget` honours `skillsRoot`; new `legacySkillTargets`, `reconcileLegacyTarget` (FS-2: `lstat().isSymbolicLink()` — true for junctions — then `unlinkSync`; `realpathSync` inside try, a throw = dangling; `renameSync` to `<AGENTIC_SDLC_KB_ROOT or ~/.agentic-sdlc>/backups/codex-skills/<name>-<UTC stamp>` — the same root seam `orientMarkerPath` uses, so tests isolate it — with copy+remove fallback across volumes; `symlinkSync(target, at, win32 ? 'junction' : 'dir')`). `reconcileLegacyTarget` takes an optional `{ link }` injection so a test can make link creation fail in-process. Same function in course (its `installOwned` still writes the new copy). |
| 2 | `scripts/postinstall.js` ×4 (course's is 16 lines with `installOwned`) | Call the reconcile after a successful Codex copy; FS-3 refresh of an existing new copy; print the contract lines. |
| 3 | `scripts/preuninstall.js` ×4 | FS-4: resolve and unlink the legacy link first, then remove the new copy. |
| 4 | `scripts/init.js` ×4 | FS-5: scan legacy roots as well. |
| 5 | `scripts/test_clients.js` ×4 | T7 updated (pins the old Codex target — declared contract change); F-082 cases. |
| 6 | `README.md` (root `:62`, kb `:80`; mkt and course list no paths today — add only if they gain a path list) | FS-8. |
| 7 | `ENFORCEMENT.md` ×4, if Q5 = yes: Codex paragraph (root `:151`, kb/course `:196`, mkt `:151`) and the "no fixture" reason (root/mkt `:73`, kb/course `:118`) | FS-8, D3. |
| 8 | `strategic/architecture.md` Component Map rows "Client roster" (`:37`) and "Skill deployer" (`:39`) | New fields and the reconcile duty. |
| 9 | `CHANGELOG.md` ×4 | User-facing entry, including the backup folder. |
| 10 | **distill-skill** (`Antoneeo/distill`; Codex entry `lib.js:85`, `skillTarget` `:140`, `postinstall.js`, `uninstall.js`, `preuninstall.js`, `test_clients.js`, `README.md:46`, `CHANGELOG.md`) | Same capability set and the same FS-2 (move aside, then link); its whole-folder `removeSkill` is never applied to the legacy path (Q3). |

Not touched: `sdlc_core.py` — `_orient_entries_in` already accepts the top-level `hooks`
shape of `.codex/hooks.json` (read, `:2194-2197`); it does not look at user-level
`~/.codex/hooks.json` (Q2).

Trace: #1–#3 serve UC1–UC4, FS-1…FS-4, FS-6; #4 FS-5; #5 all FS; #6, #9 UC1–UC2 and the
course; #7 UC6; #8 the Component Map clause; #10 UC1–UC4 for distill.

## Decisions

- **D1 — no second real copy under `$CODEX_HOME/skills`.** Killing fact: E2 (listed twice,
  and the two drift apart in version).
- **D2 — the legacy path is a link to the new copy, created even on fresh installs
  (owner Q1).** E3+E4: current Codex follows it and lists the skill once; it is the only
  way UC3 can work. Alternatives on the map: "move legacy aside and require a Codex with
  the `.agents` root" (simpler, drops UC3); "leave legacy untouched" (keeps UC3, breaks
  UC2 by E2).
- **D3 — no automatic hook wiring on Codex.** ENFORCEMENT's reason, "no fixture pins the
  schema", is no longer true (E11). The remaining reason is the trust gate: an
  installer-written hook is skipped until the user trusts it in `/hooks`, which is the
  "installed, not running" state §4 calls the worst. Documenting the snippet and the
  `/hooks` step makes the user's one act explicit.
- **D4 — the `.agents` home is `os.homedir()`.** E7: same folder Codex reads in every
  normal run.
- **D5 — move aside, never delete.** Today's update keeps files the user added to the
  skill folder; a deletion would break that. A backup outside every skills root is not
  loaded by any client.

## Security & Threat Model

- **T1 — removing the new copy through an alias** (`~/.codex/skills` linked to
  `~/.agents/skills`). Mitigation: FS-2 case 2 compares real paths before acting;
  test T-F075-6.
- **T2 — losing user content in the legacy folder.** Mitigation: D5, the whole folder
  moves to the backup in every package, with nothing deleted; tests T-F075-4, -9.
- **T3 — following a link while removing.** Mitigation: `lstat` first; a link is removed
  with `unlinkSync`, never with recursive removal; the uninstall script resolves the
  legacy link before removing the new copy.
- **T4 — duplicate or stale listing.** Eliminated by D1, D2 (Codex) and FS-3 (Gemini);
  POSIX residual handled by FS-7.
- **T5 — dangling legacy link** after a manual removal of the new copy: E5 shows Codex
  ignores it; the next install repairs it (FS-2 case 1).
- **T6 — writes outside `CODEX_HOME` for users who use it as a sandbox.** The installer
  now writes to the real `~/.agents/skills`. Codex reads that folder regardless of
  `CODEX_HOME` (E1, E7), so a `CODEX_HOME` sandbox never isolated user skills; accepted
  and stated in the README.
- **T7 — downgrade to an older package.** Not probed: the older copy step either writes
  through the legacy link into the new copy or fails on the link ("Failed to install"),
  and course's older `installOwned` reports `unowned` on a link. Either way Codex lists
  the skill once. Accepted residual; CHANGELOG says to remove the new copy and the link
  before a downgrade.
- **T8 — junction to a network path cannot be created** (Windows). Falls into FS-2 case 6.

## Action Plan

1. Owner answers Q1 and Q5 (Q2–Q4 can follow).
2. On a POSIX machine with Codex ≥ 0.164.0, run `probe_codex_skill_roots.js`; S4 decides
   FS-7.
3. RED: F-082 cases in root `scripts/test_clients.js`, T7 updated; `node scripts/test_clients.js`
   fails for the stated reasons.
4. GREEN: `lib.js`, `postinstall.js`, `preuninstall.js`, `init.js` (root).
5. Propagate to kb, mkt, course (course: `installOwned` for the new copy; `uninstallOwned` only in the uninstall script), each
   with its own test run.
6. Docs: README, ENFORCEMENT (if Q5), Component Map, CHANGELOG.
7. distill-skill, in its repository (Q3).
8. Real-machine proof, E2E script, closure review, merge brief.
9. Release per `GUIDE_release.md`. The version that ships F-082 is the first published
   after 1.47.0 (expected 1.48.0 / kb 1.31.0 / mkt 0.26.0 / course 0.1.0-beta.13 /
   distill 0.9.0 if nothing else ships first — set at release). Tell the course project.

## Test Strategy

Lifecycle tests (`test_clients.js`, temp HOME/USERPROFILE, `CODEX_HOME` controlled;
fixtures written without BOM, E10). Expected RED reason on today's code in brackets.

- T-F075-1 `skillTarget(codex)` is `<home>/.agents/skills/<name>`, with and without `CODEX_HOME` [today: `.codex/skills`].
- T-F075-2 `legacySkillTargets(codex)` is `<CODEX_HOME or home/.codex>/skills/<name>` [function absent].
- T-F075-3 fresh install: new copy populated; legacy path is a link resolving to it [no new copy, no link].
- T-F075-4 legacy real folder naming this skill, with an extra user file: moved to the backup with the extra file; legacy is a link [today: overwritten in place].
- T-F075-5 legacy real folder naming another skill: untouched; warning printed [no warning].
- T-F075-6 `~/.codex/skills` linked to `~/.agents/skills`: nothing removed, new copy intact. A guard: it passes on today's code and fails on an implementation that skips case 2.
- T-F075-7 legacy is a live link elsewhere: untouched; warning names both paths [no warning].
- T-F075-8 legacy is a dangling link: replaced by a link to the new copy [left dangling].
- T-F075-9 course-creator (and distill, in its repository): legacy folder with an edited owned file and an added file → both are in the backup, the legacy path is a link, the new copy carries the ownership record [today: legacy updated in place].
- T-F075-10 link creation made to fail through the `{ link }` injection, in-process via `freshLib`: backup made, case-6 line returned, no throw [no backup].
- T-F075-11 install twice: identical state, one backup at most [today: no link].
- T-F075-12 uninstall script: legacy link and new copy gone; real legacy folder and backup kept [today: removes only `.codex` copy].
- T-F075-13 Codex not detected, existing new copy naming this skill: refreshed (FS-3) [not refreshed].
- T-F075-14 `init` with a sibling only in the legacy root: multi-lens note written (FS-5) [today: found, since today's root is the legacy root — becomes RED once T-F075-1 is green; write it before step 4].
- T7 (updated): Claude, Gemini, Antigravity targets unchanged.
- Output: T-F075-3, -4 and -12 also assert their contract lines (fresh-install link line,
  "Moved" line, uninstall lines); -5 and -7 assert the warnings.
- Platform: if the POSIX gate (FS-7) drops the link, T-F075-3, -4, -8 and -11 take a
  POSIX branch (backup only, no link); write them with that branch from the start.
- Suites: `node scripts/test_clients.js` in each distribution and in distill; the Python
  battery `python -m unittest discover -s scripts -p "test_*.py"` as regression.

Real-machine proof (after `npm i -g <packed tarball>`): (1) harness S0–S6 PASS, `--negate`
all FAIL; (2) `codex debug prompt-input hi` (add `-c service_tier="fast"` only where the
user's `config.toml` carries a value the CLI rejects) lists each installed skill once;
(3) an interactive Codex session loads `$agentic-sdlc`.

## Open questions (for the owner; recommendation first)

- **Q1 — legacy path. ANSWERED: link** (REQUEST R3). Link it to the new copy, also on
  fresh installs, so older Codex keeps working (D2 stands); the alternative — move it
  aside and require a Codex version that reads `~/.agents/skills` — is dropped.
- **Q2 — `check` note on Codex.** `sdlc_core.py` does not look at user-level
  `~/.codex/hooks.json`, so a user-level Codex hook still draws the "not wired" note.
  Follow-up unit (recommended) or this unit.
- **Q3 — distill-skill.** Same session, in its repository (recommended: the course
  installs it too); its development checkout on the other PC is not known here.
- **Q4 — no uninstall command** in the four packages (E9: npm never runs `preuninstall`).
  Follow-up unit for the whole family, modelled on distill's `distill-uninstall-skill`
  (recommended), or add it here.
- **Q5 — Codex hook documentation. ANSWERED: document it** (REQUEST R3). ENFORCEMENT
  gets the official hook snippet and the `/hooks` trust step, and its stale reason (E11)
  is corrected; the hook is still not wired automatically (D3).

## Diary / Current State

- **2026-10-23 — first draft** (this PC). Branch `fix/codex-agents-skills` off
  `origin/main@ee73649`, worktree `C:\Users\pntntnud\source\wt-codex-skills`.
- **2026-10-23 — revised after design review rounds 1 and 2** (findings and answers in
  `audit/reviews/REVIEW_LOG.md`). Evidence now S0–S6 plus the npm probe. Open: POSIX run
  of S4 (FS-7), owner Q1–Q5, design review round 3. The real profile was left as found;
  no code changed. Implementation moves to another PC (R2).
- **2026-10-23 — renumbered F-075 → F-082; Q1 and Q5 answered** (R3). F-075 was taken in
  parallel by another unit (session-start orientation, already on the owner's local
  `main`); F-082 was the first id free on every ref. Q1 = link, Q5 = document. Still open:
  POSIX run of S4 (FS-7), Q2–Q4, design review round 3. Before merging, bring in `main`:
  the other F-075 changed `orient` in `sdlc_core.py`, so the line references to
  `_orient_entries_in` above must be re-derived.
