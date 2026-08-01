---
id: F-019
feature: Parallel Handoff (workstream registry + per-feature resume files)
status: COMPLETED
level: L3
start_date: 2026-07-27
end_date: 2026-07-27
---
# Feature Analysis: Parallel Handoff

## Objective

`audit/handoff.md` is a single narrative slot with session scope: "where the last
session stopped". With N milestones in parallel there are N "last sessions", and the
last one to close overwrites the resume point of the others — whoever resumes
milestone A finds milestone B's state. Observed live on 2026-07-27: this session and
the parallel `scripts/` re-analysis session wrote the same file; the last writer won.
On separate branches each carries its own copy, but they collide at merge, and the
`orient` hook reads only one.

Owner's framing: *"se si lavora in parallelo su diverse milestones c'è un solo
handoff, e questo impedisce di far reiniziare le attività sulla milestone
liberamente"* — plus the requirement that whoever opens the project **sees** that
someone else has a milestone in PROGRESS.

## Feature Vision

Serves the Vision's durable-understanding goal ("Vision, design, plans, tests, guides
and handoff stay synchronized ... so nothing load-bearing lives only in a transcript")
and the team-lead Actor ("several agents ... aligned to one intent"). Admission test:
advances Goal 2 (the handoff of a paused milestone survives other milestones closing)
and the team-lead Actor commitment. Violates no Non-Goal — see the work-management
guard below, which is the design's binding constraint.

**Non-Goal guard (work-management).** A registry of workstreams flirts with the
"aggregation built to be worked through" prohibition. The line the Vision itself
draws: the registry is an **inventory of what is open and where it stopped, ordered
for lookup** — the same nature as the generated manifest. It records no assignee-as-
plan ("who must do it"), no deadline, no ordering-to-execute, and it is not a queue:
one row per open workstream, keyed by feature. It crosses the line the moment rows
carry due dates, owners-as-assignment, or priority ordering — that is the deletion
test applied: remove the registry → parallel resume breaks (keeps it); add those
fields → nothing in the benefit needs them (they stay out).

## Use Cases / User Needs

- **Solo developer using an AI agent** — pauses milestone A, works milestone B,
  resumes A weeks later: A's resume point must be intact, not overwritten by B's
  closure.
- **Team lead needing governance** — opening the project shows at a glance which
  milestones are open, on which branch, since when — before touching anything
  (the owner's "chi lavora sa che qualcun altro sta lavorando").
- **A fresh session/agent** — the SessionStart hook emits the registry (same path as
  today), so orientation shows the open workstreams without any hook change.

## Impact

Design in one line: **`handoff.md` becomes a registry (one row per open workstream);
volatile resume logistics move to `audit/HANDOFF_[feature].md`, ephemeral, deleted at
that feature's closure; durable narrative stays in the ANALYSIS Diary (DRY).**

| Path | Change | What |
|---|---|---|
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | Write Triggers: handoff row split into registry row + `HANDOFF_[feature]` row; Phase 1 reads registry then the resumed feature's HANDOFF file; Phase 5 closure updates the registry (row removed at closure, HANDOFF file deleted) |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | handoff template → registry template + new `HANDOFF_[feature].md` template with the Diary/logistics boundary stated |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | MODIFY | new invariant: registry + per-feature handoff wired in SKILL.md and templates.md |
| `ai_docs/audit/handoff.md` | MODIFY | dogfood: converted to registry form |
| `ai_docs/README.md` | MODIFY | must-read line 6 wording ("workstream registry") |
| `CHANGELOG.md` | MODIFY | `[Unreleased - 1.17.0]` |

**Blast radius (enumerated).**
- `sdlc_check.py` `ORIENT_DOCS` points at `ai_docs/audit/handoff.md` — path unchanged,
  the registry flows through the hook as-is. **No code change.** The section label
  ("Last session handoff") is cosmetic and left alone.
- Battery: no existing invariant asserts handoff wording (verified by grep over
  `test_*.py`); the new invariant is additive.
- `GUIDE_release.md` post-release step says "record version + date + next step in
  `ai_docs/audit/handoff.md`" — satisfied by a registry row; guide untouched.
- Hybrid: Action Plan node status remains the governed state; the registry is the
  filesystem glance layer, per-feature files stay filesystem-first like today's
  handoff. `dispatch.md`, `guides.md`, `elicitation.md`: no handoff references
  (grep-verified beyond the Write Triggers pointer).
- `HANDOFF_*.md` lives in `audit/`, which is discovery-by-grep — not manifested, no
  INDEX change, no validator change.

## Security and Threat Model

Surfaces: filesystem only; the registry is emitted by the SessionStart hook into
agent context (existing surface, same path, same size caps `ORIENT_PER_DOC_CHARS`).

| Threat | Mitigation |
|---|---|
| T1 — registry grows unbounded, flooding orientation | One row per OPEN workstream; rows removed at closure; ≤ 20 lines keeps binding. Hook truncation caps already bound the worst case. |
| T2 — HANDOFF_[feature] files accumulate as orphans after closure | Deletion is part of the closure checklist (same step that flips the ANALYSIS to COMPLETED); an orphan is grep-visible in `audit/` and its dangling registry row is visible at every session start. Not mechanically enforced in this unit — declared. |
| T3 — the two homes drift (Diary vs HANDOFF file) | Boundary stated in both templates: Diary = durable narrative (what/why), HANDOFF = volatile resume logistics (branch, uncommitted, environment, next command). The HANDOFF file is deletable *by design* — anything worth keeping belongs in the Diary. |
| T4 — registry becomes a work-management board | The Non-Goal guard above: no assignment, no due dates, no execution ordering; inventory-for-lookup nature stated in the template. |

## Action Plan

- [x] A — Write Triggers: split the handoff row (registry + per-feature).
- [x] B — Phase 1 / Phase 5 wording (read registry + resumed file; closure removes
      row and deletes file).
- [x] C — templates.md: registry template + `HANDOFF_[feature].md` template.
- [x] D — invariant test (RED confirmed, then GREEN — 58/58).
- [x] E — dogfood: this repo's `handoff.md` to registry form (3 rows: F-019
      PROGRESS, F-015 PAUSED, release 1.16.0 awaiting owner).
- [x] F — closure: index + mark, battery 58/58, `check` CLEAN, CHANGELOG
      `[Unreleased - 1.17.0]`. Registry header uses `Date:` (validator contract —
      `Updated:` warned; template aligned, `sdlc_check.py` untouched as designed).

## Test Strategy

- Static battery with the new invariant; no existing assertion touched.
- `sdlc_check.py check --root .` CLEAN; `orient` smoke: registry emitted at the same
  path, exit 0.
- Behavioral proof deferred: a scenario seeding two IN_PROGRESS workstreams and
  checking the agent resumes the right one is a candidate for `evals/scenarios/`,
  not built in this unit.

## Diary / Current State

**2026-07-27 — complete on `feat/parallel-handoff`.** Standalone, devPNT off.
Level L3 · router: no match. Elicitation: one round, owner chose registry +
per-feature files; my DRY correction accepted (boundary Diary/logistics + ephemeral
files) — the binding design rule. RED→GREEN on the new invariant; battery 58/58;
`check` CLEAN; `orient` smoke emits the registry at the unchanged path. Closure
review = declared self-pass (session harness forbids unprompted reviewer subagents;
devPNT off): checked the diff against this Impact map 1:1 — 6 files touched, all
named; no `sdlc_check.py` change (T-boundary held when the `Date:` warning appeared:
template aligned to the validator, not vice versa); work-management Non-Goal guard
re-read against the final registry template (no assignee/due/order fields). Registry
row for F-019 removed and no HANDOFF_parallel_handoff.md ever created — closure per
its own new rule, dogfooded.

Unreleased: rides as `[Unreleased - 1.17.0]`; release is a separate owner-gated unit
per `GUIDE_release.md`.

**2026-07-27, later — migration clause added (L2 amendment; the closure above was
premature).** Owner asked what happens to projects curated under 1.15. Answer,
verified rather than assumed: **nothing breaks.** `sdlc_check.py:619-631` checks only
the `Date:` header and the file's age — the legacy narrative template carries `Date:`,
so it validates unchanged; `ORIENT_DOCS` reads the same path verbatim; the eval battery
tests skill doctrine, not consumer repositories; and `postinstall.js` copies the skill
without ever touching a consumer's `ai_docs/`. A legacy handoff is simply a one-row
registry written in prose — it works, it is just not parallel-safe.

The real gap was that an agent meeting one had **no rule**. Added: **convert lazily, on
first write, never as a migration sweep** — a Write-Triggers row for the legacy form, a
Phase-1 reading rule, and the field-by-field conversion in `templates.md` (`## Active
features` bullets → rows, `## Next step` → that row's next step, `## Session notes` →
`## Project-wide notes`). Deliberately **no validator warning** for non-registry form:
it would fire on every existing project at once and nag about a file that is working —
the ceremony Non-Goal, and the deletion test (remove the warning → parallel-safe resume
still reachable, because the conversion happens on the next write anyway). Invariant
extended to assert the migration clause exists in both files: shipping a format change
without one strands existing projects, and that is now mechanically caught.
