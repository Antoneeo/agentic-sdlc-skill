# Subagent Execution Discipline

Opt-in orchestration for L3 work with an approved design: the orchestrator
drives a `PLAN_[feature].md` through subagents instead of implementing every
task in the same session. Default stays same-session; this is an escalation,
never a requirement.

## Trigger

Only for L3 (an approved E-TDD in Hybrid, or an ANALYSIS Action Plan in
Standalone). Never for L1/L2 — the plan/ledger machinery is overhead a small
change does not need. The plan is always `derived-from` the accepted design:
it is never independently authored, exactly like an E-TDD is never authored
without an E-ISP.

## The loop

1. `sdlc_check.py plan validate PLAN_[feature].md` — zero-execution schema +
   confinement + ledger cross-check. Non-zero exit = **no dispatch**. This is
   the hard gate: "no valid plan, no dispatch."
2. For each task, in plan order:
   - Read the task's status from the sidecar ledger
     (`PLAN_[feature].ledger.json`). `status: done` (exact sentinel) → skip,
     never re-dispatch. Anything else (pending, failed, missing, or a
     corrupt-but-parseable entry) → treat as pending and dispatch.
   - `sdlc_check.py plan brief PLAN_[feature].md --task <id>` — prints the
     task block, the `produces` of prior-order tasks (interfaces), and
     `guides` pointers (paths, never pasted content) to stdout.
   - Spawn the subagent with that brief as its entire context window.
   - Run `task.verify` out of band (the orchestrator executes it — the
     validator only ever prints it, never runs it) plus the one-shot review
     below.
   - Write `{status, verify_result, timestamp}` back to the ledger. The
     validator never writes the ledger — single-writer, orchestrator-owned.

**Guide consumption under dispatch.** Selecting each task's `guides` field IS the
consult trigger (`guides.md` §0) applied at plan-authoring time: the orchestrator
runs the router lookup (project router `ai_docs/reference/INDEX.md` + the agent-KB
router) when populating `guides`. A dispatched context-free subagent does **NOT**
run its own router consult — it reads the guide pointers handed to it in the
brief. (Proactive guide-creation stays at closure — the same broad final pass
below — so it needs no separate dispatch hook.)

## Model tiers (client-relative, no provider names)

- Default dispatch: **economy** implementer tier.
- After **two** consecutive `verify_result: fail` on the same task: escalate
  to the **deep** tier for the retry (ADR 2026-07-02). Do not escalate on the
  first failure — a single fail is often a brief or environment issue, not a
  capability gap.

## Review slots — one-shot, not iterative

Exactly three review touches per task, never a loop:

1. Inline self-review by the implementer subagent before it reports done
   (the standard critical-review pass, not a separate call).
2. One reviewer pass per task (Hybrid: reuse the devPNT code-review gate;
   Standalone: the `review.md` discipline).
3. One broad final pass over the whole plan at closure, after all tasks are
   DONE — catches cross-task drift a per-task review cannot see.

If a review FAILs, fix and re-run `verify` — that is a normal loop iteration
via the ledger's fail path, not an extra review slot.

## Ledger protocol summary

Read → skip-if-done → dispatch-if-pending → write. The ledger is the only
memory the loop needs across sessions or context compaction: a resumed
orchestrator re-reads it and picks up exactly where it left off, never
re-running a DONE task.

## Degradation

No subagent-spawning tool available → the orchestrator runs each task in the
same session, against the same plan and ledger, with the same one-shot review
slots. No capability is lost, only the parallelism/isolation subagents would
have added.

## Hybrid note

The plan's `derived-from` points at the accepted E-TDD document key. Per-task
review reuses the devPNT independent reviewers (§4.6 code review gate) rather
than restating review doctrine — see `review.md` for the single definition
both modes share.
