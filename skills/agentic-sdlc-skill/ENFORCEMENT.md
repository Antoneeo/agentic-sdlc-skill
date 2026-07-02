# Mechanical enforcement (optional, recommended for teams)

Prompt-level rules depend on the model's discipline and degrade with long contexts, compaction and competing instructions. Three levels of increasing guarantee:

## 1. Interactive validation (default, no setup)

The agent runs a single gate at closure (Phase 5):

```
python "<skill_dir>/scripts/sdlc_check.py" check
```

(`check` = validate + stale in one command.) Exit code ≠ 0 ⇒ the feature is not declared closed. This is the minimum level the skill expects.

## 2. Check in CI (recommended for teams)

Copy `scripts/sdlc_check.py` into the repository (e.g. `tools/sdlc_check.py`) and add to the pipeline:

```
python tools/sdlc_check.py validate --strict
```

Effect: an unregenerated index, invalid frontmatter, a missing security section or incoherent states **block the pipeline** instead of relying on the agent's memory. `--strict` also fails on warnings and on a missing `ai_docs/`, so a wrong working directory cannot produce a green pipeline. This works because documents travel in the same PR as the code (Phase 5 rule).

Note: the copy in the repo is the authoritative one for CI; update it when you update the skill.

## 3. PreToolUse hook (gate on writes)

Blocks Edit/Write on protected paths when no `ANALYSIS_*.md` is `IN_PROGRESS`. In the project's `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python \"C:\\Users\\<user>\\.claude\\skills\\agentic-sdlc\\scripts\\sdlc_check.py\" gate --hook --protected \"src/auth;src/crypto\""
          }
        ]
      }
    ]
  }
}
```

Semantics: exit code 2 + message on stderr ⇒ the write is blocked and the message is shown to the agent, which must create the ANALYSIS (Phase 3) before retrying.

**Usage warnings:**
- The gate is deliberately coarse: applied to all of `src/` it would also block the legitimate L1/L2 tasks foreseen by the Triage. Use it **only on security-critical directories** (`--protected "src/auth;src/crypto"`), where "never without analysis" is the desired policy.
- The paths in `--protected` are prefixes relative to the project root, separated by `;`.
- `ai_docs/`, `tests/` and `test/` are always excluded from blocking.
- The hook assumes the working directory is the project root (standard behavior of Claude Code hooks).
