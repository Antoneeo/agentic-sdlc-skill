---
description: Why orientation-hook detection is re-implemented in the Python spine as a read-only subset of the installer's JS contract, and why the wiring note belongs to whoever owns `check`.
status: CURRENT
---
# ADR: Hook detection as a two-runtime subset contract

**Date:** 2026-08-28 · **Task ref:** F-041 (ANALYSIS_kb_midsession_drift.md)

## Context

F-036 wires the SessionStart orientation hook at `init` time, in the npm
installer's JS (`lib.js`: `findOrientHook`, `orientHookValidator`, with
injection guards on the paths it writes). The F-041 field report showed the
gap: projects initialized before F-036, or bootstrapped by the agent (which
never runs `init`), are silently unwired — and the component that runs
in-project at every closure is the Python validator, which knew nothing about
hooks. The vendored-validator rule (ENFORCEMENT §2: a stdlib-only two-file
pair, `sdlc_check.py` + `sdlc_core.py`) constrains any solution.

## Decision

1. **Re-implement the detection read-only in the Python spine** (`sdlc_core.py`:
   `orient_hook_state` + `print_orient_hook_note`), mirroring the JS predicate.
   The pinned relation is a SUBSET, not equality: entry-point names equal on
   both sides; the Python file list is a superset (`.codex/hooks.json` is
   documented but never written by init). JS stays authoritative for WRITING
   hooks; Python only DETECTS. Divergences are declared, not accidental:
   `utf-8-sig` reads (Node's `JSON.parse` chokes on BOM), and any-resolves
   aggregation across entries (init's interactive flow is first-match; a
   closure note that nagged beside a live hook would be a standing false
   alarm — the client runs ALL SessionStart hooks).
2. **The note is check-layer behaviour, owned by whoever owns `check`.** The
   spine's `cmd_check` calls `print_orient_hook_note`; an overlay that
   REPLACES the check pipeline (the marketing lens does) must re-attach the
   same call after its own verdict. Informational only, by contract: never the
   exit code, never a `validate` warning — CI (`validate --strict`) must stay
   green because the wired hook legitimately lives in git-ignored
   `settings.local.json`.

## Alternatives considered

- **Shell out to node/lib.js from the validator** — rejected: the in-project
  validator must not depend on node, and the vendored copy ships without the
  installer.
- **A shared JSON contract file read by both runtimes** — rejected: breaks the
  two-file vendoring rule (§2 "copy both, or neither"); a third file silently
  missing would resurrect the split-brain the rule exists to prevent.
- **Stay silent on the wired-but-dead state** — rejected: ENFORCEMENT §4 calls
  it "the worst of the three states" (emits nothing AND looks installed);
  blessing it at every closure would invert the note's purpose.

## Consequences

- **Pro:** the wiring gap self-reports at every closure, in-project, with zero
  new dependencies; the dead state surfaces instead of hiding; the mkt overlay
  fold documents the re-attachment contract for future overlays.
- **Con / risk:** one predicate, two runtimes — dual maintenance. Bounded by
  tests pinning each side's own constants and by the declared subset relation.
  Residuals accepted and documented (ENFORCEMENT §4): clients with no hook
  mechanism keep the note; a `.codex/hooks.json` in an undocumented shape is
  not recognized; a content-derived UNC token is existence-probed only
  (metadata touch, nothing read or executed).
