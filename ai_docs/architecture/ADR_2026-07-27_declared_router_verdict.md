---
description: Why the guide consult is enforced as a declared output in Rule Zero rather than by another restatement or a hard write-gate.
status: CURRENT
---
# ADR: Enforce the guide consult as a declared output, not as another instruction

**Status:** Accepted
**Date:** 2026-07-27
**Task ref:** F-016 (`ai_docs/solutions/ANALYSIS_guide_activation.md`)

## Context

The consult trigger shipped in M4 Unit 2 and was stated in three places
(`SKILL.md` Phase 4 bullet, `SKILL.md` `## Operative Guides`, `guides.md` §0).
It still did not fire: the owner reported that unless the user asked for it by
hand, the agent neither consulted nor wrote guides.

The diagnosis was placement, not wording. All three statements sit off the
always-executed path: Phase 4 belongs to the L3 workflow only, `## Operative
Guides` is at the tail of a 306-line file, and `guides.md` is a support file the
contract itself says to open "only when needed". Rule Zero — the one step every
request runs — never mentioned guides, and Phase 1, the only always-run read
step, read `README.md` + `INDEX.md` but not the guide router.

This is a general problem for a prompt-level process: an instruction that is not
on the executed path is not an instruction, however many times it is written.

## Decision

Enforce the consult by making its **result a declared output** of a step that
always runs: the Rule Zero triage declaration carries the router verdict
(`Level: L2 · router: no match` / `router: GUIDE_x.md → read`), for L2, L3 and
Spike; L1 stays exempt.

The declaration is the mechanism, not the reminder: an undeclared lookup is
indistinguishable from a skipped one, so requiring the verdict — including the
`no match` case — converts an invisible omission into a visible one, for the
user, for a later reviewer, and for the agent itself in the next session.

Supported by two non-competing layers: the guide router joins Phase 1's
mandatory reads, and the `orient` SessionStart hook is promoted from optional to
recommended default (it already emitted the router; it was simply off).

## Alternatives considered

- **A fourth restatement of the instruction** — rejected: three existing
  statements had already failed. Repetition does not change reachability, and it
  raises the token cost of the contract for no behavioral gain.
- **A hard mechanical gate (PreToolUse block on writes until a guide is
  consulted)** — rejected: the gate cannot tell a legitimate `no match` from a
  skipped lookup, so it would block correct work; `ENFORCEMENT.md` already
  reserves `gate` for security-critical directories precisely because a coarse
  block breaks the proportional triage (an explicit `project_vision.md`
  Non-Goal: no heavyweight governance for trivial edits).
- **Hook-only enforcement** — rejected as the primary mechanism: it needs Python
  and per-client wiring, which would make Standalone-without-Python a degraded
  mode. The skill must stay fully usable with no toolchain, so the hook is the
  backstop and the prompt placement is the process.
- **Moving the mechanics into Rule Zero** — rejected: `guides.md` stays the
  single home of guide mechanics (DRY). Rule Zero carries the trigger and the
  declared output only, and points on.

## Consequences

- **Pro:** the omission becomes observable without reading the guides; the
  behavior is provable by a behavioral scenario on both the match and the
  no-match path, and assertable as a static invariant.
- **Pro:** the pattern generalizes — any discipline in this skill that keeps
  being skipped can be enforced by requiring its result as a declared output of
  a step that always runs, rather than by another restatement.
- **Con / risk:** the verdict can become theater (always `no match`). Mitigated
  in `guides.md` §0 ("never fake the verdict") and by the `verdict_declared_on_no_match`
  behavioral scenario, but it is not mechanically detectable — a false verdict
  is a doctrine violation, not a validator error.
- **Con:** one extra line per L2/L3/Spike declaration. Accepted: bounded, and
  L1 — the highest-frequency level — pays nothing.
