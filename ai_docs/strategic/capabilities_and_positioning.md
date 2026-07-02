---
description: Honest catalog of agentic-sdlc's current advantages (explained), parity points, and positioning vs superpowers (through v6.0.x). Feeds the four-layer product vision.
status: CURRENT
---
# Capabilities & Positioning

Companion to `ai_docs/vision/project_vision.md`. Layer **A** (what agentic-sdlc already does, explained), the honest **parity** line, and the **B/C** map against superpowers (recon 2026-07-02, superpowers v6.0.3). Rule of the doc: parity is called parity; an advantage must be evidenced.

## A — Current advantages of agentic-sdlc (explained)

1. **Risk-proportional triage (Rule Zero).** Process scales to risk (L1/L2/L3/Spike): a typo is not a design doc, an auth change is not a one-liner. superpowers applies the same heavy 7-stage pipeline uniformly and its own guide admits it "might be overkill" for small work. Proportionality is a structural advantage, not a setting.
2. **Documentation-First with a real lifecycle.** Canonical docs carry frontmatter `status` (CURRENT/SUPERSEDED/DRAFT/DEPRECATED); a two-index model separates the curated must-read `README.md` from the generated `INDEX.md` manifest; `features_history.md` is derived from ANALYSIS frontmatter. Knowledge is durable and self-describing across sessions. superpowers persists a design doc and a progress ledger, but has no status lifecycle, no manifest, no supersede discipline — stale guidance is not marked dead.
3. **Mechanical enforcement (`sdlc_check.py`).** `check/validate/index/stale/mark/gate` — the closure gate, CI `--strict`, and a PreToolUse hook on security-critical paths. Compliance does not depend on the model remembering the rules under a long context. superpowers' enforcement is prompt-level (inline self-review checklists) — good, but it degrades exactly when context is long.
4. **Vision Gate with graded authority.** Vision docs declare DRAFT (informs) or APPROVED (binds); an APPROVED vision stops silent scope drift and forces the conflict into the open. superpowers brainstorms a design doc per feature but has no persistent, authority-graded vision that guards intent across many sessions.
5. **Security-first triage.** Security-sensitive areas (external input, authN/authZ, crypto, network, personal data, filesystem) are never L1; a threat-model section is mandatory in every L3 analysis. superpowers has no explicit security gate.
6. **Standalone-complete + optional devPNT (open-core).** The skill is whole on the filesystem; devPNT adds governed storage, versioned proposals, independent reviewers and KL as a paid amplifier — with a guaranteed downgrade path (shadows become plain docs). superpowers is single-tier.
7. **Mechanical drift tracking.** `stale`/`mark` record doc-vs-code freshness against a git ref, so "this analysis is older than the code it describes" is detectable, not a matter of trust.

## Parity (honest — not advantages)
- **Multi-client reach.** Both run on Claude Code, Gemini/Antigravity, Codex, Cursor and more (superpowers via SessionStart injection; agentic-sdlc via protocol pointers + installed skill). Parity, not an edge.
- **Fresh-context subagents & one-shot review.** superpowers 6.0.x already does per-task fresh subagents, one reviewer / two verdicts, model-per-dispatch, read-only skeptical reviewers. Our Feature A must match this, not reinvent it — and in Hybrid it reuses devPNT's independent reviewers.

## B — superpowers strengths to absorb (backlog + Feature A)
Subagent-driven execution; explicit TDD (RED/GREEN/REFACTOR); systematic debugging; disciplined receive/give code review; git worktrees + branch finishing; collaborative (Socratic) elicitation. All tracked in the evolution roadmap backlog and Phase 4.

## C — superpowers frontier (v6.0.x): match or leapfrog
- **Per-task Interfaces block** (consumes/produces per task) → matched by our executable plan (roadmap 4.1).
- **Durable progress ledger** (`.superpowers/sdd/`) → matched by our per-task ledger (4.2).
- **One reviewer / two verdicts, model-per-dispatch, read-only reviewers** → matched by our tiered independent-review design (Phase 4, seam §4.5/§4.6).
- **Global Constraints block** — project rules copied *verbatim into every plan*, not reusable across projects → **leapfrogged by Feature B**: operative guides are maintained once, versioned, source-faithful (provenance + per-section markers), injected by pointer. This is the sharpest competitive line: they duplicate rules per-plan; we keep a single authoritative, drift-tracked source.
- **Instruction Priority Hierarchy** (user CLAUDE.md/AGENTS.md ranks above skill/system) → adopt an explicit precedence consistent with D1/D7 (user > skill process > devPNT doctrine). Candidate backlog item.

## D — what nobody has
Operative guides from user indications + agent-level KB (Feature B). See `milestone_vision_operative_guides` (accepted) and roadmap §3–§4.

## Positioning one-liner
superpowers is an excellent *execution* methodology converging toward plan-embedded project rules. agentic-sdlc is a *governance-first* methodology with durable, mechanically-enforced documentation and a proportional process — absorbing superpowers' execution discipline while adding the reusable, source-faithful operative-guide layer and an optional open-core amplifier.
