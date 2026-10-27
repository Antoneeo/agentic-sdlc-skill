---
description: ADR - the constraint recall is a PreToolUse hook that adds context and never decides; the project is resolved from the edited file; validate's note on a missing preservation table is gated on a code-lens capability, not on the domain alone. Rejected - recall after the edit, no hook, a deny-style recall, domain-only gating.
status: CURRENT
---
# ADR: a hook that informs without deciding, and a note gated on the lens

**Status:** Accepted
**Date:** 2026-10-27
**Task ref:** F-085 (ANALYSIS_working_model.md)
**Digest:** F-085 — review FAILs came from constraints the unit had stated and the agent had not observed at the moment of the edit. Decision: a PreToolUse hook (`constraints --hook`) adds the constraints bound to the file to the agent's context and never emits a `permissionDecision`; it resolves the project from the edited file, because the hook runs in the session's current directory (live probe); `validate`'s note on a missing `### Preservation constraints` table fires only where the profile claims `preservation_constraints` (code lens). Rejected: recall after the edit (PostToolUse), no hook, a deny-style recall, gating on the domain alone. Residual: a prose line opening with an L1 level silences the recall; the verdict hook still resolves its project from the working directory.

## Context

The only PreToolUse hook the family had (the guide-verdict check, F-076) denies. F-085
needed the opposite idiom: put the constraints of the open L3 unit in front of the
agent just before it edits a file they bind, without touching the user's permission
flow. Whether Claude Code accepts a PreToolUse object holding only `additionalContext`
was not documented in a way the design could rest on, so it was probed live
(`solutions/harness_working_model/LIVE_PROBE_2026-10-27.md`): the context arrived and
the edit was applied. The same probe showed that the hook process runs in the
session's current working directory, which a `cd` moves.

At the copy into the distributions, the kb lens's golden test — which pins its 1.0
transcript line by line — showed that a note gated on the `code` domain changes what
a kb install prints for a code-domain unit. The owner had scoped the unit to the code
lens (REQUEST_working_model.md R12 (a)).

## Decision

1. The recall is PreToolUse and context-only: `hookSpecificOutput` holds
   `hookEventName` and `additionalContext`, never a `permissionDecision`; every
   failure is silence and exit 0; the wired command ends in `; exit 0`.
2. The hook resolves the project by walking up from the edited file, never from its
   working directory.
3. `validate`'s FS7 note is gated on an optional profile capability,
   `preservation_constraints`, which only the code entry point claims; the domain
   condition stays. The command, the recall and the docs site's `defect` kind are
   shared and unchanged by the gate.

## Alternatives considered

- **Recall after the edit (PostToolUse)** — kept as the fallback the owner chose (R13
  (4a)) in case the probe failed; rejected once it passed, because a constraint seen
  after the edit can only repair, not prevent.
- **No hook, the `--file` command only** — kept for clients without hooks (FS11);
  rejected as the only form: it relies on the agent remembering at the moment the
  recall exists to cover.
- **A deny-style recall** (refuse the edit until the constraints are read) — rejected:
  a cost on every bound edit the owner did not accept, and it would decide where the
  unit only needs to inform.
- **Gate the note on the domain alone** — rejected at the copy: a kb install would
  see a change the Objective promised it would not.

## Consequences

- **Pro:** the constraints reach the agent at the edit with no permission side effect;
  another lens's output is untouched; a new optional capability makes the scope a
  declared fact of each profile.
- **Con / risk:** a second PreToolUse hook per edit, in every project once installed
  (about 0.25 s on every path, `solutions/harness_working_model/probe_hook_timing.py`);
  the uninstaller now names hooks by spec, since the event no longer
  identifies them.
- **Residual:** a prose line opening with an L1 level silences the recall (errs toward
  silence); the guide-verdict hook still resolves its project from the working
  directory — a follow-up.
