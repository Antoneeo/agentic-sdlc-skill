# Handoff
Date: 2026-07-19 (UTC)
Branch: main
Agent: Claude (Opus, orchestrator) — Standalone (devPNT off — locked on another project)

## State: v1.15.0 prepared, NOT yet committed/published
Two features bundled, doc-only, in the working tree:
1. **Write Triggers** — `SKILL.md` §Write Triggers, a document→trigger→phase table symmetric to Rule Zero (write-side twin of triage); de-duped so the table is the authoritative home and phases point to it. + bootstrap-set/handoff/VISION-retroactive/ADR/features_history sharpenings.
2. **Code-Comprehension Guides (F-015)** — new `source_kind: code` guide kind, written autonomously (duty, no proposal) for high-complexity components so understanding survives across sessions; reuses the whole guide machinery (source = verbatim code excerpts), `sdlc_check.py` untouched. Vision decision **B** (Layer A; Layer D untouched). Detail: `solutions/ANALYSIS_comprehension_guides.md` (Diary).

Validated by TWO independent blind comprehension tests (fresh agent, skill-only): trigger discoverable + correct; adversarial + autonomy-boundary probes pass; 6 findings all fixed. **Eval battery 52/52, `validate` 0 errors.** Version bumped in `package.json` + `gemini-extension.json`; README Key Features + CHANGELOG updated.

## Pending owner
1. **Commit + tag** v1.15.0 (both features travel together), then **`npm publish`** (2FA/EOTP). Verify: `npm view @antoneeo/agentic-sdlc-skill version` → 1.15.0. Suggest `npm pack --dry-run` first (confirm allowlist unchanged, no dev-only leak).
2. **Delete `proposed-agentic-modified/`** — the Write-Triggers proposal, fully absorbed.
3. **#8 dogfood** (optional) — write one real `source_kind: code` guide (writer-side proof: validator accepts + router lists); ANALYSIS stays IN_PROGRESS until then.

## Session notes
Repo files are CRLF; edits applied as content-delta (no whole-file churn). Packaged allowlist unchanged (tests/`ai_docs/` not shipped). devPNT untouched this session.
