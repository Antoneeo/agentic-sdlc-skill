---
description: Separate Codex hook transport from Claude while reusing the existing validation rules.
status: CURRENT
---
# ADR: Codex hook profile and bounded transcript normalization

**Status:** Implemented on branch; native trusted dispatch pending acceptance
**Date:** 2026-11-04
**Task ref:** F-091

## Context

The main package copied a Codex skill but wired hooks only for Claude. Its validator
recognized Claude edit payloads and transcripts; adding JSON alone would leave Codex
checks silent. Codex also owns a separate human trust decision and local hook policy.

## Decision

Keep the existing Claude writers and commands. Add a Codex user-level profile in
the same installer library, using four absolute installed-validator invocations,
per-hook markers and conservative inspection of JSON/TOML sources. A fixed Python
wrapper transports base64-encoded argv and preserves JSON deny while normalizing
child exit codes. No trust or managed-policy setting is written.

Normalize complete native patches and recognized Codex transcript records into the
existing verdict/recall rules. Literal read hints use historical cwd/workdir; unknown
shell/JavaScript carriers are not executed or guessed. Copy the shared Python spine
into all four distributions; leave sibling Node installers unchanged.

## Alternatives considered

- JSON wiring only: fails because the validator did not recognize Codex events.
- Reuse Claude settings and shell suffix: wrong target and shell-dependent exit handling.
- Execute arbitrary transcript code to recover paths: introduces code execution at a read boundary.
- Automatically trust definitions: removes the client's human consent boundary.
- Broad shell-write enforcement: outside F-091's native patch scope.

## Consequences

Ordinary packaged install/upgrade supplies definitions without manual JSON assembly.
Trust remains a client step; configured does not mean executing. Each patch matches
two handlers, each spawning a wrapper and validator: four Python processes in total,
two validator invocations. The design's initial shorthand counted only validators.
Missing interpreters cannot be repaired by the wrapper. Unknown carriers fail open.
Windows loading and installed-command tests are recorded in the harness; native
trusted dispatch, POSIX and other client versions require separate acceptance evidence.
