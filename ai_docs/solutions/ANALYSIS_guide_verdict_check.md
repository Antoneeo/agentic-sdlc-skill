---
id: F-076
feature: Guide verdict check before edits
description: A Claude Code PreToolUse hook that refuses an Edit/Write when the session never declared a guide-router verdict, or never read a guide its verdict names — the check the field agent said was missing ("nothing stops me").
status: IN_PROGRESS
level: L3
domain: code
topics: [guide-router, hooks, enforcement, triage]
start_date: 2026-10-23
branch: claude/f076-guide-verdict-check-eaaba8
---
# Guide verdict check before edits

## Objective

Rule Zero makes the agent declare the level with the guide-router verdict before acting,
and read the guide the verdict names. In a field project an agent edited code without
consulting the router and said nothing had stopped it (REQUEST R1; source of the
quotation pending the owner's confirmation, R5). F-075 made the router reach the
session; this unit checks, at the moment of the edit, that the duty was done.

Measured by the probe (`harness_guide_verdict_check/probe.py`, red today): on the field
case — an Edit with no verdict in the session and a guide unread — no shipped hook
flags it. The only PreToolUse surface, `gate --hook`, checks something else (an
IN_PROGRESS ANALYSIS on protected paths, opt-in) and stays silent (P5).

Facts the design rests on, each probed on this machine:
- **The transcript carries what is needed.** Claude Code passes `transcript_path` to
  every hook. Each assistant content block is one JSONL line,
  `{"type":"assistant","message":{"content":[{"type":"text"|"tool_use",…}]}}`; a
  `tool_use` block carries `name` and `input` (`file_path`, `command`, …).
- **Lag, one sample.** A text block written in the same message as a Bash call reached
  the transcript 2 s before the `tool_use` line, both before the tool ran (marker
  `F076-LAGPROBE-7731`, lines 168–169 of this session's transcript). Asynchronous-write
  lag is a residual, not observed.
- **Size.** Assistant lines are small; the bulk of a transcript is attachments and
  request blobs (1.4 MB here; 189 MB the largest on this machine). A byte prefilter
  then a JSON parse of assistant lines only scanned the 189 MB file in 0.35 s; the
  validator's start-up is 0.19 s.
- **A validator that cannot run `verdict` exits 2, and exit 2 blocks.** `python
  missing.py` exits 2 (file gone: uninstall, manual deletion), and so does an older
  validator whose argparse rejects `verdict` (downgrade). Wrapped as `…; exit 0`, the
  command exits 0 in both shells Claude Code uses on Windows (Git Bash, PowerShell 5.1)
  and on POSIX; the hook's JSON on stdout passes through.
- **Uninstall cleanup is best-effort.** `preuninstall.js` removes only the orientation
  hook; `remind`'s UserPromptSubmit entry stays pointing at a deleted file and exits 2
  — which blocks the prompt. npm 7+ may not run uninstall lifecycle scripts at all
  (npm's own change; not probed here), so the wrapper above, not the uninstaller, is
  what keeps a dead verdict entry from blocking edits.

## Feature Vision

`vision/project_vision.md` is APPROVED. Served: the anti-myopia North Star and Goal
"Make the project's intent readable and *operable* by an agent that arrives with no
context" — a guide that governs the work and is not read is the myopia the skill exists
to prevent; the Solo developer's "never re-explaining the project across sessions" (the
guide is the explanation, written once).

Admission (`vision/rulings.md`, precedent first): no row answers "refuses an edit until a
duty already in the doctrine is shown done". Nearest: r19/r32 (a per-turn reminder — it
reminds, never checks) and r14 (maintenance — the purpose here is new). The prose rules
once: new row **r34** (r33 is taken on the F-080 branch). The "No ceremony ratchet"
Non-Goal reads "at any level … a check … a cost that varies but is never zero … is
out"; its second door ("above L1 … the owner accepts it explicitly") is worded above L1.
r34 answers the "at any level" sentence directly, on r19's precedent (a cost reaching
trivial turns, disclosed and owner-accepted): here L1 pays nothing beyond the
declaration Rule Zero already requires — written with the literal `Level: L1` — and a
refusal only when that declaration is missing. Cost disclosed below, accepted (R4).
Distinct from r10: no triage authority is added (level and verdict stay the agent's;
the hook checks only that a verdict was written and its guides read, never which guide
should have matched). Distinct from r3: it names no work and orders nothing.

The uninstall fix for `remind` is r14: purpose, actor and surface unchanged; a defect of
its removal path, fixed in the function this unit generalizes.

Owner decisions: block, not warn (R3); accepted and wired by default machine-wide on
Claude Code, like `remind`, removing the entry being a standing opt-out (R4).

Elicitation: goal, actor and acceptance derive from R1 and the approved plan (R2); two
real doubts were asked and answered (R3, R4). Choices weighed here, not asked:
- **Session-wide, not per-turn.** I take "a verdict anywhere earlier in the session"
  over "a verdict since the last user prompt": pro — a multi-turn task ("continue")
  does not re-declare, and per-turn would refuse legitimate continuation work at a
  retry each; contra — a second, unrelated task later in the same session passes on the
  first task's verdict (residual).
- **"Read" = the guide's file name appears in a non-edit tool's input.** I take this
  over "a Read call on that path": pro — agents read with Read, Bash `cat`, Grep, or hand
  the path to a subagent, all carrying the name; contra — a glob read (`cat
  reference/*.md`) does not count and is refused once, the reason saying how to unblock.
- **Lenient match, and "no match" names nothing.** Any assistant text line with
  `router:` is a verdict; when the text after `router:` begins with `no match` or
  `absent`, it names no guide (so "router: no match (GUIDE_x.md does not apply)" does
  not force reading a guide just ruled out — SKILL.md: the verdict is "never an excuse to
  read every guide"). Pro — a false refusal costs a retry per edit; contra — a stray
  "router:" in prose passes. Format drift resolves toward silence, never toward refusal.

Non-goals: judging whether the verdict is right (semantic, the agent's); Bash-made
writes; other clients (no hook surface pinned; their agents keep the prose duty —
doctrine stays client-agnostic); the sibling installers (kb, mkt, course do not wire
`remind` either; their validators gain the command, their ENFORCEMENT documents manual
wiring); per-project configuration.

Success signals: the probe green (P1, P3 refused; P2, P4, P5 not; P6 a real transcript
not refused; P7 the wired command exits 0 with no validator); a field agent that skips
the verdict is stopped at its first edit with the one line that unblocks it.

## Use Cases / User Needs

- **UC1 — Agent, edit without a verdict.** The agent in a project with guides attempts
  an edit before declaring the level with the router verdict; the edit is refused with
  the form of the declaration and where the router is. Benefit: anti-myopia — the guide
  that governs the work is consulted before acting.
- **UC2 — Agent, verdict names an unread guide.** The agent declared `router:
  GUIDE_x.md → read` but never opened it; the edit is refused naming the guide.
- **UC3 — Agent, compliant or trivial.** Verdict declared and guides read, `Level: L1`
  declared, or no guides in the project: the edit proceeds, nothing shown. Benefit:
  "scale process cost to risk".
- **UC4 — Solo developer, install, opt-out, uninstall, downgrade.** Installing wires the
  check machine-wide; removing the entry is a standing opt-out; uninstalling (where the
  package manager runs the uninstaller) removes it and the per-turn entry; a missing or
  older validator never blocks an edit. Benefit: same.

Grounding: guide router (`reference/INDEX.md`), verdict (`router: …`, SKILL.md Rule
Zero), `GUIDE_*.md`, `remind`, `gate`, `transcript_path`, PreToolUse,
`permissionDecision` — EXISTS (the harness's own terms). The `verdict` command — NEW.

## Functional Spec

**FS1 — when it checks.** On an Edit, Write, MultiEdit or NotebookEdit by the main agent
(not a subagent), of a file inside the project, in a project with at least one guide in
its router. Otherwise the edit proceeds and nothing is shown.

**FS2 — what satisfies it**, judged on the session so far:
- a **verdict** is any line of the agent's own text containing `router:`; it names the
  `GUIDE_*.md` files after `router:` on that line, unless that text begins with `no
  match` or `absent`, in which case it names none;
- a **trivial declaration** is a line of the agent's text with `Level: <letter>1`
  (`L1`, `E1`, …);
- a guide is **read** when its file name appeared in the input of any tool call other
  than the four edit tools.
The edit proceeds when (a verdict or a trivial declaration exists) AND every guide named
by any verdict, and present in the project, was read.

**FS3 — refusal.** Otherwise the edit is refused and the agent is shown one line:
- no verdict: `[sdlc verdict] No guide-router verdict in this session; this project has
  guides (<docs>/reference/INDEX.md). Declare it with the level, e.g. "Level: L2 ·
  router: no match" or "router: GUIDE_x.md -> read" (L1: "Level: L1"), then retry.`
- unread: `[sdlc verdict] The router verdict names <GUIDE_a.md, GUIDE_b.md>, not read in
  this session. Read it, then retry.`
Each at most 250 characters for a docs root named `ai_docs` and two guide names. The
check never approves an edit: compliance leaves the user's normal permission flow in
place.

**FS4 — never a blind refusal.** When the check cannot tell — no or unreadable session
record, one over 256 MiB, one in which no agent entry can be read, malformed hook input,
an ambiguous or missing docs root, a validator missing or too old to know the command,
any internal error — the edit proceeds and nothing is shown.

**FS5 — wiring.** Installing the code package on Claude Code wires the check once
machine-wide; an entry already present is left as it is; an entry the user removed is
never re-added; uninstalling, where the package manager runs the uninstaller, removes the
check and the per-turn reminder entries naming the removed skill, saying which.

Acceptance: AC1 probe P1–P5, P7 as listed, P6 on a recorded transcript not refused; AC2
every FS1 skip silent; AC3 every FS4 case silent; AC4 refusal shape exact, ≤ 250
characters, no transcript text echoed, never `allow`; AC5 installer: wired once with the
exit-0 wrapper, already, opted-out, uninstall removes verdict and remind and reports
them; AC6 batteries ×4, `test_clients.js`, golden unchanged, `check` CLEAN.

## Interface Contract

Actors: the agent (software actor) perceives the refusal as the result of its edit
call; the developer perceives the install line and the uninstall line.

Flow: the agent calls Edit → Claude Code runs the PreToolUse command
`<python> "<validator>" verdict --hook; exit 0` (matcher
`Edit|Write|MultiEdit|NotebookEdit`, timeout 10 s) with the event JSON on stdin → the
code-lens entry point hands `verdict` to the spine (`knowledge.main` →
`sdlc_core.main`) → the spine checks FS1, lists the guide names, scans the transcript,
and prints the refusal as `{"hookSpecificOutput": {"hookEventName": "PreToolUse",
"permissionDecision": "deny", "permissionDecisionReason": <line>}}` or nothing → Claude
Code refuses the edit and shows the reason, or runs the normal permission flow.

Mechanism bounds: the transcript is read line by line; only lines under 1 MiB containing
`"type":"assistant"` are parsed; the guide list is a directory listing of `reference/`,
no guide is opened. The edited path is `tool_input.file_path`, or `notebook_path` for
NotebookEdit. A subagent call carries `agent_id` in the event JSON. Installer:
user settings `settings.json`, marker `verdict-hook-wired` under the family's
agent-global root (as `remind-hook-wired`).

Idioms reused: the `[sdlc gate]` prefix (here `[sdlc verdict]`), the installer's
wired/already/opted-out codes, marker, console line, and the uninstall console line.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| read a PreToolUse payload from stdin, fail-open | EXISTS | `sdlc_core.cmd_gate` (inline) | utf-8-sig decode, `json.loads`, returns 0 on error |
| resolve the edited file against the project root | EXISTS | `cmd_gate` (inline), `find_project_root` | `relative_to(root)`, ValueError → 0 |
| list the project's guide names | EXISTS | `ai_path(root, "reference")` + glob | `list_guides` not reused: it reads every guide's text (T3) |
| read the session transcript for a verdict and reads | MISSING | — | grep `transcript` in `sdlc_core.py`, `knowledge.py`: no hit |
| fail open on an ambiguous docs root | INADEQUATE | `sdlc_core.main` | fail-open only for `orient`/`remind`; others print `[ERROR]`, exit 1 |
| wire a constant-command hook machine-wide with opt-out | EXISTS for one event | `lib.js` `wireRemindHookInto` | event, matcher, marker are literals |
| remove our hooks at uninstall | INADEQUATE | `lib.js` `removeGlobalOrientHooks` | SessionStart only |

New and changed components:
- `read_hook_payload()` — stdin → dict or None; factored out of `cmd_gate`, which uses it.
- `transcript_facts(path) -> dict | None` — `{"assistant", "declared", "trivial",
  "named", "read"}`; None when unreadable or oversized.
- `verdict_reason(payload, root) -> str | None` — FS1 + FS2; the reason or None.
- `cmd_verdict(args)` — prints the refusal or nothing; always 0; `main` adds `verdict`
  to the ambiguous-docs-root fail-open branch, returning 0 silently.
- `lib.js`: `findCommandHook(settings, spec)`, `wireCommandHookInto(spec, target,
  python, validator)` generalize the remind pair (remind's exported names kept as
  wrappers); `VERDICT_HOOK` spec with the `; exit 0` wrapper; `wireGlobalVerdictHook`;
  `removeGlobalCommandHooks(roots) -> [{target, event}]` for remind and verdict, sharing
  the entry-pruning loop with `removeGlobalOrientHooks` (whose signature and return stay).

Guides: GUIDE_skill_family_changes.md — `sdlc_core.py`, `shared_files.py` and the new
battery are copied identically into three distributions, counted once.
GUIDE_shared_project_memory.md read; it maps discovery and validator composition, which
this unit does not change. Guide check: no CURRENT guide covers `cmd_gate` or the
installer's hook wiring; neither is high-complexity — no guide due.

## Impact

| Path | Change |
|---|---|
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` (+3) | `read_hook_payload`, `transcript_facts`, `verdict_reason`, `cmd_verdict`, constants (`VERDICT_EDIT_TOOLS`, `VERDICT_MAX_BYTES`, `VERDICT_LINE_MAX`, regexes); `cmd_gate` uses `read_hook_payload`; `verdict` subparser; `verdict` in the ambiguous-root fail-open branch; docstring command list |
| `skills/agentic-sdlc-skill/scripts/test_verdict.py` (+3, new, shared) | FS1–FS4, AC2–AC4 |
| `skills/agentic-sdlc-skill/scripts/shared_files.py` (+3) | `test_verdict.py` in `SHARED_FILES` |
| `shared_manifest.json` (×4) | regenerated |
| `scripts/lib.js` | generic hook wiring and removal; verdict spec |
| `scripts/postinstall.js` | wire the verdict hook; console line |
| `scripts/preuninstall.js` | remove remind/verdict entries; one console line per event removed |
| `scripts/test_clients.js` | AC5 |
| `skills/agentic-sdlc-skill/SKILL.md` | one sentence under Rule Zero's verdict paragraph |
| `skills/agentic-sdlc-skill/ENFORCEMENT.md` | §3 gains "Verdict check" (what, cost, opt-out, manual JSON) |
| `distributions/*/skills/*/ENFORCEMENT.md` (×3) | short paragraph: the command, manual wiring |
| `ai_docs/vision/rulings.md` | row r34 |
| `ai_docs/strategic/architecture.md` | Component Map: new row "Hook wiring"; Validator core row names `verdict` |
| `CHANGELOG.md` ×4 | `[Unreleased]` entries |
| `ai_docs/solutions/harness_guide_verdict_check/probe.py` | the probe, P1–P7 |

Blast radius (text search over `skills/`, `distributions/`, `scripts/`; the devPNT index
is stale, so grep is the instrument, each hit opened):
- `cmd_gate` — `sdlc_core.main` only; ENFORCEMENT §3 examples; behavior unchanged,
  guarded by `test_verdict.py`'s gate case.
- `sdlc_core.main` — every entry point via `knowledge.main` (`INTERCEPTED` does not
  include `verdict`, so it is forwarded); additive subcommand; golden corpora run named
  commands only.
- `wireRemindHookInto`, `findRemindHook`, `remindMarkerHas/Add`, `remindHookCommand` —
  `postinstall.js:48`, `test_clients.js:663–743`; kept as wrappers, same names, codes.
- `removeGlobalOrientHooks` — `preuninstall.js:24`, `test_clients.js:882–983`; signature
  and return unchanged.
Missed consumer cost: an installer test failing (caught by `test_clients.js`).

## Security and Threat Model

Surfaces: event JSON on stdin, the transcript file (path from the client), the docs-root
listing, the user settings file (installer).

- **T1 zero-execution**: reads and prints; no subprocess, eval, git.
- **T2 refusal by accident**: every path inside a try returning 0 silently; ambiguous
  docs root → 0; the wired `; exit 0` makes a missing or too-old validator, and Python's
  own errors, exit 0 — a refusal can only come from the JSON a working check prints.
- **T3 bounded reads**: size cap, line cap, assistant-only parse; guides by directory
  listing, never opened.
- **T4 injection**: the refusal is fixed text plus guide file names present in the
  project's `reference/`, matching `GUIDE_[A-Za-z0-9_-]+\.md`; no transcript text is
  echoed.
- **T5 permission bypass**: `allow` is never emitted (it would skip the user's prompt);
  a refusal only removes options.
- **T6 transcript path from the input**: read only, never followed further; not a file →
  silent.
- **T7 the wrapper hides a broken check**: a check that never runs is silent, so a broken
  install degrades to today's prose-only duty, never to a blocked machine. `check`'s
  wiring note does not cover this hook (residual).
- Residuals, declared: edits through a subagent are not checked (delegation passes on
  the orchestrator's duty, not its proof); after a resume or `/clear` that drops earlier
  entries, a declared verdict may be gone — one refusal, then re-declare; Bash-made
  writes are not checked; session-wide matching; whether a refusal applies in the
  client's bypass-permissions mode is the client's (not verified).
- Personal data: nothing from the transcript leaves the process except the outcome and
  guide names.

## Ceremony disclosure

- Per edit, compliant or exempt: ~0.2–0.5 s latency, zero tokens.
- Per edit, non-compliant: one refusal (≤ 250 characters) and one retry.
- L1: nothing beyond writing the declaration Rule Zero already requires, in the literal
  form `Level: L1`; a refusal only when it is missing.
- Projects without guides, other clients, subagents: zero.
- Read cost: SKILL.md +1 sentence; ENFORCEMENT ×4 a section or paragraph.
Accepted by the owner (R4, asked at "~250 characters").

## Action Plan

- [x] Probe red (P1, P3).
- [ ] RED: `test_verdict.py`, `test_clients.js` cases.
- [ ] `sdlc_core` functions, subparser, fail-open branch; `cmd_gate` reuse.
- [ ] `lib.js` generic wiring and removal, verdict spec; `postinstall.js`, `preuninstall.js`.
- [ ] SKILL.md, ENFORCEMENT ×4, rulings r34, architecture, CHANGELOG ×4.
- [ ] Copy shared files; `shared_files.py --update` ×4.
- [ ] GREEN: four batteries, `node scripts/test_clients.js`, probe P1–P7.
- [ ] E2E_TEST, closure review, MERGE_REVIEW, index, handoff removed.

## Test Strategy

`test_verdict.py` (shared, all four batteries), synthetic transcripts in a temp project:
refused — no verdict; verdict naming an unread guide (named in the reason); every edit
tool; an Edit naming the guide is not a read. Silent — verdict + Read; verdict + Bash
`cat`; read before verdict; `no match`; `no match` mentioning a guide; `Level: L1` /
`E1`; a guide not in the project; no guides; no docs root; ambiguous docs root; file
outside the project; NotebookEdit via `notebook_path` (refused when non-compliant);
`agent_id`; non-edit tool; garbage stdin; missing / absent / oversized transcript; an
over-cap line skipped; unrecognised format. Shape exact, ≤ 250 characters, no
transcript text echoed. `gate --hook` unchanged. `test_clients.js`: wired once with the
wrapper; already; opted-out; uninstall removes verdict and remind, reports each.
Probe: P1–P5 synthetic; P6 on a recorded transcript (`--transcript`, optional — a real
session transcript holds personal paths and is not shipped); P7 the wired command form
with a missing validator exits 0 under each shell found, the bare form 2 (red control).

## Diary

**2026-10-23 — analysis drafted.** Probe red (P1, P3). Owner: block (R3), accepted and
wired by default (R4). r33 is taken on the F-080 branch; this unit uses r34.

**2026-10-23 — design review.** Round 1 FAIL (1 BLOCK, 11 WARN), round 2 PASS with two
WARNs folded (P7 red control, npm claim hedged); REVIEW_LOG. Implementation started.
