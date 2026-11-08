---
description: F-093 - on a multi-lens install the machine-wide hooks are the first lens's; the sibling installers never wire the per-turn reminder their ENFORCEMENT.md promises. Diagnosis, reproduction, and the design decision it needs.
status: COMPLETED
end_date: 2026-11-08
feature: F-093
id: F-093
start_date: 2026-11-08
level: L3
branch: claude/fix-hook-marker-per-lens-bee374
---
# ANALYSIS: Family hook wiring on multi-lens installs (F-093)

## Objective

Explain why, on a machine with all four lenses installed, a knowledge project (`D:\kb`)
received only agentic-sdlc's per-turn line and never kb-agentic's, and fix what is a
defect. Request: `audit/requests/REQUEST_family_hook_wiring.md` R1.

## Feature Vision

Serves the anti-myopia north star (`vision/project_vision.md`): a lens whose protocol
never reaches the session cannot be applied — the F-046 premise (`rulings.md` r19).
Bound by the "no ceremony ratchet" Non-Goal: any per-turn cost beyond r19/r32 needs the
owner's explicit acceptance.

## Diagnosis

**The reported hypothesis is refuted.** The markers are shared per settings file and per
hook kind, but the second lens never reaches them:

1. **The sibling installers never wire the per-turn reminder.** `scripts/postinstall.js`
   wires orient, remind, verdict and constraints on Claude Code. The postinstalls of
   kb-agentic, mkt-agentic-sdlc and course-creator call `wireGlobalOrientHook` only, and
   their `lib.js` has no `REMIND_HOOK` at all. `git log -S` shows no sibling installer ever
   had it: F-046 (a4ed86cd) changed only the root `scripts/`. Yet kb's and marketing's
   `ENFORCEMENT.md` say "Per-turn reminder: `remind` (UserPromptSubmit -- wired by default)"
   and "Installing the package wires it machine-wide". A kb-only or marketing-only install
   gets no reminder at all, on every machine.
2. **Hook presence is recognized family-wide.** `findOrientHook` / `findCommandHook` accept
   any command naming a family entry point (`sdlc_check.py`, `mkt_check.py`) plus the
   subcommand, so a lens that finds a sibling's hook returns `already` and stops before the
   marker check. This is by design for orientation: `ANALYSIS_global_orient_hook.md`
   ("family-wide by design: any lens sets it, no lens re-adds — the marker is the opt-out
   memory, `findOrientHook` is the dedup"), and `ANALYSIS_session_orientation_reach.md` FS3
   reports two orientation copies for one client as a defect.

Reproduced by `harness_family_hooks/probe_family_install.js` (each postinstall as a child
process in a throwaway HOME):

| Install order | SessionStart orient | UserPromptSubmit remind | PreToolUse verdict / constraints |
|---|---|---|---|
| code, kb, mkt, course | agentic-sdlc | agentic-sdlc | agentic-sdlc |
| kb, code | **kb-agentic** | agentic-sdlc | agentic-sdlc |
| kb only | kb-agentic | **none** | none (code-lens hooks) |
| mkt only | mkt-agentic-sdlc | **none** | none (code-lens hooks) |

Row 2 is the owner's PC exactly (kb orient, agentic-sdlc remind at user level).

**Latent defect, not yet live:** making presence lens-aware while the markers stay
family-wide would produce precisely the reported symptom — the second lens would find the
family marker for a hook it never wrote and report `opted-out`.

## Which design the repo intends

One shared hook per kind per client, the first wiring lens's. Evidence: the orientation
dedup and marker rulings above; r19 accepted ONE flat per-turn line (~89 tokens); r32
priced the line per lens (code 566, kb 531, mkt 525, course 393 chars) — one line, whichever
lens it is, never their sum. The line's TEXT is per lens (F-046: "each lens declares its own
text via `set_profile(remind_line=...)`; the spine owns the machine").

So on a multi-lens machine the shared line is the code lens's, always — only its installer
wires it — and that line is code-shaped: "Declare the level (L1/L2/L3/Spike) and the
guide-router verdict … Name the mechanism before fixing the first defect". Its only pointer
to another lens is the r32 suffix ("Above L1, with sibling lenses installed: choose the lens
with routing.md"), which names no lens and arrives after a "first decide if THIS skill
governs" that a knowledge task answers "no".

## Use Cases / User Needs

- **UC1 — Practitioner with one non-code lens** (kb-only, marketing-only): gets the per-turn
  reminder the lens's ENFORCEMENT.md promises. Traces to r19's benefit.
- **UC2 — Practitioner with several lenses**: each turn's line leads the agent to the lens
  that governs the work, not to the code lens by default. Traces to r32's benefit.
- **UC3 — Any user who removed a hook**: no install of any lens re-adds it (F-042 standing
  opt-out, unchanged).

## Functional Spec

Option A, approved (REQUEST R2):

- **AC1** — installing kb-agentic or mkt-agentic-sdlc on Claude Code, with no family
  reminder in the user settings and no remind marker for that file, adds one
  `UserPromptSubmit` entry running that lens's validator with `remind`.
- **AC2** — any family `remind` entry already present (any lens) means nothing is added.
- **AC3** — the entry absent and the marker naming the file means nothing is added (UC3).
- **AC4** — uninstalling removes only `remind` entries whose validator lives in the
  removed skill roots, and clears the marker line only when it removed one.
- **AC5** — the code lens and course-creator behave exactly as before.

## Interface Contract

The surface is the installer's console output. Reused verbatim from the code lens's
postinstall ("Per-turn protocol reminder wired …") and preuninstall ("Removed the …
hook entry"); silent on `already` / `opted-out`, like the orientation hook. The per-turn
line itself is unchanged.

## Capability Ledger

| Capability | Ruling |
|---|---|
| Wire a constant-command hook with family dedup and a standing opt-out | EXISTS — `wireCommandHookInto` / `wireGlobalCommandHook`, `scripts/lib.js` |
| Name the installed sibling lenses | EXISTS — `installed_sibling_lenses()` / `lens_table`, shared `sdlc_core.py` (used by orient FS4) |
| Wire it from a sibling installer | INADEQUATE — sibling `lib.js` copies lack `REMIND_HOOK` and the command-hook helpers |

## Guide check

`GUIDE_hooks.md` covers this area (installation owner, per-hook markers) and was read;
`GUIDE_skill_family_changes.md` sets the copy count (identical copies count once). No new
guide needed.

## Options (owner decision)

- **A — sibling installers wire the reminder, family dedup kept.** Port `REMIND_HOOK` and
  the command-hook helpers into the three sibling `lib.js` copies (not a wholesale copy —
  `GUIDE_hooks.md`: sibling installers keep their own scope) and call it from their
  postinstalls. Fixes UC1. No new cost, inside r19/r32. Markers unchanged, no migration.
  Does NOT fix UC2: the owner's PC already has agentic-sdlc's remind, so a kb reinstall
  answers `already`.
- **B — A, plus a family-aware line.** When siblings are installed, `cmd_remind` names
  them ("which of agentic-sdlc, kb-agentic, … governs this work? load that one"), from
  `installed_sibling_lenses()`. Fixes UC2 with one line per turn. Needs an r19/r32
  amendment: the line would read the skills directory each turn (SKILL.md names only,
  matched against `lens_table` — installed by the user, not repo- or session-controlled),
  and its length changes. Owner ruling required.
- **C — one reminder per lens.** Lens-aware presence, per-lens markers, migration of the
  family markers. ~2,000 chars per turn on four lenses: four times r19's accepted cost, and
  four protocols competing on every prompt. Not recommended.

**Recommendation: A, then B once ruled.** A is a defect against the package's own
documentation; B is the cure for the D:\kb symptom and is a scope change (r4).

## Impact

Option A, as built. Identical delta in kb and marketing (counts once,
`GUIDE_skill_family_changes.md`):

| Path | Change | Why |
|---|---|---|
| `distributions/{kb-agentic-skill,mkt-agentic-sdlc}/scripts/lib.js` | MODIFY | add `REMIND_HOOK`, per-spec marker helpers, `findCommandHook`, `wireGlobalRemindHook`, `removeGlobalRemindHooks`; `removeGlobalOrientHooks` now calls the shared `removeGlobalHookEntries` loop (same behaviour) |
| `distributions/{kb-agentic-skill,mkt-agentic-sdlc}/scripts/postinstall.js` | MODIFY | wire remind on Claude Code after orient |
| `distributions/{kb-agentic-skill,mkt-agentic-sdlc}/scripts/preuninstall.js` | MODIFY | remove it, attributed by root |
| `distributions/{kb-agentic-skill,mkt-agentic-sdlc}/CHANGELOG.md` | MODIFY | Unreleased entry |
| `scripts/test_clients.js` + kb/mkt copies | MODIFY | F-093 tests |
| course-creator | none | its ENFORCEMENT.md promises orientation only; whether course should wire its reminder is a separate question |

The sibling copies stay Claude-only, as their orientation hook: Codex wiring is the code
lens's (F-091) and out of this unit's scope.

### Preservation constraints

| id | bound to | callers | must stay true |
|---|---|---|---|
| P1 | `wireGlobalOrientHook`, `wireCommandHookInto`, marker files under `~/.agentic-sdlc/` | every postinstall, test_clients | A removed hook is never re-added by any lens's install (F-042) |
| P2 | `findOrientHook`, `findCommandHook` | wire functions | One entry per hook kind per settings file; a lens-aware presence test never ships without per-lens markers |

### Residuals (closure review, accepted as family-wide behaviour)

Both hold identically for the code lens's own reminder today; fixing them here would
make the siblings diverge from it, so they are named, not fixed:

- **A dead family entry blocks wiring.** A `remind` entry whose validator no longer
  exists (npm 7+ may skip the uninstaller) counts as present, so no lens wires a live
  one, silently. The orientation hook reports this as `broken`; the reminder does not.
- **Uninstalling the lens that owns the one entry leaves the survivors without it.**
  kb wired it, marketing found it present; uninstalling kb removes it, and marketing gets
  it back only on its next install.

A follow-up unit would treat a dead entry as absent and re-wire from a surviving lens at
uninstall, in all three installers at once.

## Security and Threat Model

- Silent disabling of a hook the docs promise: realized today (UC1); the F-093 test pins it.
- Duplicate or re-added hook after removal: guarded by P1/P2.
- Option B: text read per turn — limited to SKILL.md `name:` matches against `lens_table`
  (same boundary as orient FS4); no file content reaches the line.

## Action Plan

- [x] Reproduce (probe) and pin with a failing test.
- [x] Owner decision: A (R2). B's costs asked, measured below.
- [x] Implement; probe shows kb-only and marketing-only installs wired.
- [x] Closure review (4 WARN: 3 fixed, 2 residuals named above); E2E and merge-review documents.

## Test Strategy

`F-093: postinstall wires every hook its ENFORCEMENT.md declares wired by default`, added to
the three `test_clients.js` copies that run a postinstall, derived from each distribution's
own ENFORCEMENT.md. RED today: kb and marketing miss `remind`. Green for the code lens.

## Diary / Current State

- **2026-11-08** — diagnosis done; hypothesis (shared markers) refuted; real causes 1 and 2
  above; probe and RED test committed (93952ba3).
- **2026-11-08** — owner chose A (R2). Implementation was interrupted by drive D: filling
  up (another repository's Git LFS objects; the owner freed it), which truncated one file;
  restored from git and re-applied. Closure review PASS after three fixes; batteries green (code 76, kb 52, marketing 52, course 4). Branch not merged: the merge is the owner's. Option B measured on the installed copies: the sibling
  lookup costs ~24 ms per call, against 400–630 ms for the whole `remind` hook today
  (Python start-up); +60–100 chars per line, over r32's 600 bound. B stays unruled.
