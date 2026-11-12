---
description: F-094 - agents read a matching guide only in part and apply it only in part. Mechanism (the verdict hook credited any mention of the guide as a read; the doctrine never said "every line"), the whole-read rule in the four lenses, and the line-span check.
status: IN_PROGRESS
feature: F-094
id: F-094
start_date: 2026-11-12
level: L3
branch: claude/f094-whole-guide-read
---
# ANALYSIS: A matched guide is read whole and applied whole (F-094)

## Objective

Agents read the guide that governs their work only in part and then apply only that part
(owner, `audit/requests/REQUEST_whole_guide_read.md` R1). Find why, and make the rule
explicit and checked: a matched guide is read in full, first line to last, and applied in
full; a rule that does not fit is proposed as an amendment of the guide, and even then the
guide is considered whole.

## Feature Vision

Serves the skill's stated purpose (`SKILL.md` "Why this skill exists": acting from partial
understanding) and the Operative Guides contract ("the guide is the synthesis a trained
agent carries — read whole before acting"). No new capability, no Non-Goal touched: the
change tightens an existing duty and the check that already enforces it.

## Diagnosis — the mechanism

Field evidence (`harness_whole_guide_read/field_scan.txt`): over the 283 Claude Code
transcripts on the owner's PC, tool calls naming a `GUIDE_*.md` included **157 Reads with
`offset`/`limit` against 118 whole Reads**, 38 Greps on a guide and `head -30` of a guide.
One verbatim case: `Read GUIDE_release.md offset 1 limit 130` — the guide is 225 lines;
lines 131–225 (release verification and publish steps) were never seen.

Four causes, in order of weight:

1. **The check certified partial reads.** `sdlc_core.transcript_facts` recorded a guide as
   read when its name appeared anywhere in the JSON input of any non-edit tool call. A
   `Read` with `limit: 130`, `head -30`, a Grep on the file, even an Agent prompt naming
   it, all satisfied `verdict --hook`. ENFORCEMENT.md said so explicitly ("Read, Bash
   `cat`, Grep, a subagent brief all count"). The agent saw no refusal, so the partial read
   looked compliant.
2. **The doctrine said "read the match", not "read every line".** `guides.md` §0 said
   "read that guide's synthesis whole", but the next bullet — "Targeted match, never
   blanket", about *which* guide — sits beside it, and §2 step 5 told readers to
   "grep/partial-read on demand". The four SKILL.md said "read it first"/"read the match
   first — a targeted description match". Nothing said what *whole* excludes (offset,
   limit, excerpt), nothing covered the client's read cap, and nothing at all said
   *apply* it whole or what to do with a rule that does not fit.
3. **The reminders carried the weakest form.** The SessionStart header said "read the
   matching guide before acting"; the per-turn lines of kb and course said nothing about
   reading a guide, agentic and mkt only "declare the guide-router verdict".
4. **The client's read cap.** Claude Code's Read stops at 2000 lines without a `limit`.
   Today's guides are short (largest here 225 lines), so this is latent, but the check
   must not certify the first 2000 lines of a longer guide either.

Probed (Execute-Before-Specify): `harness_whole_guide_read/probe.py` replays five field
shapes (Read 1–130 of 225, `head -30`, Grep, Read of a 2500-line guide without limit,
Read offset 30) and four whole-read controls against the hook. **Old code: all five field
shapes pass (RED).** New code: all five refused, all four controls pass (GREEN). The Read
`offset` semantics were probed on the live tool: `offset: 3, limit: 2` returns lines 3–4,
so offset is the 1-based first line.

## Use Cases / User Needs

- UC1 — The agent matches a guide: it reads every line before acting (EXISTS: router,
  verdict, `guides.md` §0).
- UC2 — A guide longer than the client's read cap: the agent reads it in consecutive
  chunks to the end (NEW rule on an EXISTS tool).
- UC3 — The agent finds a rule in the guide wrong or inapplicable: it names it, proposes
  the amendment, declares any deviation; the rest of the guide still binds (NEW rule).
- UC4 — The owner relies on the guide being applied in full, not in the part an agent
  happened to read (Vision: partial understanding is the failure this skill prevents).

## Functional Spec

- FS1 — A named guide counts as read only when the session's reads of it cover line 1 to
  its last line.
- FS2 — A read is a line span: Claude `Read` = `offset` (1-based, default 1) for `limit`
  lines (default 2000); a literal Bash/PowerShell `cat` or `Get-Content` = whole
  (`-TotalCount N` = lines 1..N); Codex `exec_command` reads likewise; `get_file_content`
  = whole. Every other tool call (Grep, `head`, `sed`, Agent, SendMessage...) reads nothing.
- FS3 — Spans from several calls add up (chunks); a gap is a partial read.
- FS4 — A guide whose size exceeds 8 MB cannot be counted: any read counts (fail-open,
  same posture as the rest of the hook).
- FS5 — The refusal names the guide, says "not read whole", and how to unblock, within the
  250-character bound the owner accepted for the hook (F-076 R4).
- FS6 — Doctrine, all four lenses: read whole (no offset/limit/excerpt; chunks past the
  cap); apply whole; a rule that does not fit → proposed amendment (`guides.md` §6), the
  guide as written governs until accepted, deviations declared, the rest still binds;
  "targeted" selects which guide, never which lines.

## Interface Contract

The actor-facing surfaces are the hook refusal line, the SessionStart router header and
the per-turn reminder. Each keeps its idiom: one line, same position, same caps (refusal
≤250 chars; reminder ≤600 single-lens / ≤700 with all four lenses named, rulings
r19/r32 and F-093 R3). The refusal changes from "not read in this session. Read it" to
"not read whole in this session. Read every line (no offset or limit; past the read cap,
in chunks to the end)". The router header gains "whole, every line". No new surface.

## Capability Ledger

| Capability | Verdict | Where |
|---|---|---|
| Know which guides the verdict names | EXISTS | `transcript_facts` (named) |
| Know which lines of a guide the session read | INADEQUATE → extended | was names only; now `_read_spans` + `_read_whole` in `sdlc_core.py` |
| Parse a literal shell read and its line count | INADEQUATE → extended | `shell_read` (new, returns -TotalCount); `shell_read_paths` keeps its contract over it |
| Count a guide's lines within a bound | MISSING → built | `_guide_lines` |

## Guide check

- CURRENT guides covering this work: `GUIDE_hooks.md` (hook surfaces, P1–P6 of F-091) and
  `GUIDE_skill_family_changes.md` (copies count once). Both read whole; both applied:
  P4 holds (Claude/Codex user text still cannot declare), P6 holds (shared copies identical,
  drift guard green), copies triaged once.
- No new high-complexity component without a guide: the change lives inside the verdict
  hook that `GUIDE_hooks.md` already maps. That guide is a code guide whose runtime section
  does not describe the read-credit rule, so nothing in it became wrong.

## Impact

| Path (all four lenses unless noted) | Change | Why / trace |
|---|---|---|
| `scripts/sdlc_core.py` (shared) | MODIFY: `transcript_facts` read → spans; new `_read_spans`, `_guide_lines`, `_read_whole`, `shell_read`; `transcript_events` carries -TotalCount; `verdict_reason` checks coverage; router header text | FS1–FS5, UC1–UC2 |
| `scripts/test_verdict.py` (shared) | MODIFY: 6 tests (field case, offset gap, excerpt/search tools, chunks past the cap, whole carriers, Codex -TotalCount) | FS1–FS4 |
| `guides.md` (shared) | MODIFY §0 (whole read, whole application, targeted ≠ partial, dispatch), §2.5, §6 (amendment path) | FS6, UC3 |
| `SKILL.md` (per lens) | MODIFY consult bullets (agentic Rule Zero + Operative Guides; kb Phase + Guides; mkt; course) | FS6 |
| `ENFORCEMENT.md` (per lens) | MODIFY verdict description | FS2 |
| entry point `remind_line` (per lens) | MODIFY: "read a matched guide whole, apply it whole"; agentic text compressed to stay under the caps | UC1 |
| `scripts/shared_manifest.json` (×4) | regenerated | drift guard |
| `ai_docs/solutions/harness_whole_guide_read/` (repo only) | ADD probe + field scan | Execute-Before-Specify |

### Preservation constraints

| id | bound to | callers | must stay true | evidence |
|---|---|---|---|---|
| P1 | `sdlc_core.py::transcript_facts` | `verdict_reason`; `test_constraints.test_transcript_facts_is_unchanged`; `test_verdict` | Same keys (`assistant, sidechain, declared, trivial, named, read`); declaration rules unchanged; user/tool text never declares (F-091 P4) | test_constraints, test_verdict green |
| P2 | `sdlc_core.py::shell_read_paths` | `transcript_events` (now via `shell_read`); `test_verdict.CodexParsing` | Same signature and return (paths or None); same refusals of dynamic shell | CodexParsing tests unchanged, green |
| P3 | `sdlc_core.py::verdict_reason` | `cmd_verdict`; `verdict_reason` (apply_patch recursion); test_verdict | Fail-open on anything it cannot tell; never prints allow; reason ≤250 chars, echoes no transcript text | test_verdict size/echo tests green |
| P4 | remind lines | `cmd_remind`; test_remind ×3 | ≤600 single, ≤700 named (all four lenses: 692 measured for agentic) | test_remind green in every lens |

Consumers enumerated by grep (no symbol-graph tool in this Standalone repo): `transcript_facts` 1 production caller + 2 test files; `shell_read_paths` 1 production caller (replaced by `shell_read`) + its own wrapper + CodexParsing tests. Changed in four identical copies.

### Behaviour that now refuses what passed before (accepted by design)

A session whose only "read" was a Grep, `head`, `sed`, a partial Read or an Agent brief
naming the guide is now refused at its first edit until it reads the guide whole. That is
the rule the owner asked for (R1). A read the hook cannot see (a client with another tool
name, a shell form outside the literal `cat`/`Get-Content` grammar such as `type` or a
pipe) is now refused where it used to pass if the name appeared; the unblock is a plain
Read, said by the refusal. No data at rest: the check reads transcripts, it writes nothing.

The SessionStart transcript changes on purpose (router header gains "whole, every line"):
the golden baselines of agentic and kb were re-captured, and that line is the whole diff.

### Residuals (closure review, accepted)

- Spans are matched by guide NAME, not path: a Read of a same-named file elsewhere counts.
  Same posture as the pre-F-094 check; resolving paths across clients is out of scope.
- A Read that returned an error is still credited: the transcript's tool_use block is read,
  not its tool_result.
- Claude Code may refuse a very large file by token count rather than return 2000 lines;
  not modelled. Latent: guides are small by design (largest here 225 lines).

## Security and Threat Model

- The hook reads two things more than before: each named guide's bytes (bounded by
  `GUIDE_COUNT_MAX`, only files under the project's own `reference/`, matched by name from
  `glob`), and Bash/PowerShell command strings, parsed by the existing literal grammar —
  nothing is executed or expanded.
- The reason line still echoes no transcript text: only guide file names present in
  `reference/`.
- Self-certification remains possible (an agent can `cat` a guide it ignores): the hook
  proves the read, never the application. Application is doctrine (§0) and review.
- Fail-open preserved for unreadable/oversized transcripts and guides.

## Action Plan

1. Probe RED on old code (done). 2. Line-span check + tests (done). 3. Doctrine in four
lenses, reminders, router header (done). 4. Copies + manifests (done). 5. Full batteries +
`sdlc_check.py check` CLEAN. 6. Independent review, REVIEW_LOG. 7. E2E script, merge brief,
commit on branch; no publish.

## Test Strategy

- `test_verdict.py`: 6 new tests, shown RED against the pre-change `sdlc_core.py`
  (5 failures) and GREEN after.
- `harness_whole_guide_read/probe.py`: field-shape replay, RED before / GREEN after.
- Full `unittest discover` in the four lenses, `node scripts/test_clients.js`,
  `shared_files.py` (copies identical), `sdlc_check.py check`.
- Doctrine replay: the field case (Read 1–130 of a 225-line runbook) under the old
  `guides.md` §0 text is compliant ("read that guide's synthesis whole" next to "targeted
  match", nothing excluding a limit); under the new text it violates three named
  exclusions (limit before the end, "the section that looks relevant", apply whole).

## Diary / Current State

- 2026-11-12 — Field scan, mechanism, probe RED; check implemented, probe GREEN; doctrine
  in four lenses; reminders under caps (agentic compressed 613 → 574 chars).
- 2026-11-12 — Independent review (fresh subagent, design + diff in one pass, after code):
  FAIL with 1 BLOCK (stale golden baselines) and 5 WARN; all fixed or recorded as residuals
  (REVIEW_LOG). Also aligned: `dispatch.md`, course SKILL.md Phase 1, the eval scenario,
  `strategic/skill_family_agent_workflows.md`. Audit areas marked; `check` CLEAN. Deviations
  declared: no separate design-review round before code, and no owner "design approved"
  entry (the rule was prescribed in R1). Committed on the branch; merge and release are the
  owner's.
