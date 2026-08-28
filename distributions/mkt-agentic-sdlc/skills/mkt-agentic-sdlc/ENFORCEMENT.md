# Mechanical enforcement (optional, recommended for teams)

Prompt-level rules depend on the model's discipline and degrade with long contexts, compaction and competing instructions. Three levels of increasing guarantee:

## 1. Interactive validation (default, no setup)

The agent runs a single gate at closure (Phase 5):

```
python "<skill_dir>/scripts/mkt_check.py" check
```

(`check` = validate + ledger + budget + funnel + trace in one command.) Exit code ≠ 0 ⇒ the feature is not declared closed. This is the minimum level the skill expects.

## 2. Check in CI (recommended for teams)

Copy **both** validator files into the repository — `scripts/mkt_check.py` (the entry point) **and** `scripts/sdlc_core.py` (the shared core it imports) — keeping them side by side, e.g. `tools/mkt_check.py` + `tools/sdlc_core.py`. Then add to the pipeline:

```
python tools/mkt_check.py validate --strict
```

The validator ships as two files: the core carries the behaviour and is identical in every distribution of the family, the entry point names the domain. Copying only `mkt_check.py` fails immediately with a message saying so — loudly, never as a silently green pipeline. (Copying `sdlc_core.py` alone also works: `python tools/sdlc_core.py validate --strict` behaves identically, defaulting to the code domain.)

Effect: an unregenerated index, invalid frontmatter, a missing security section or incoherent states **block the pipeline** instead of relying on the agent's memory. `--strict` also fails on warnings and on a missing `ai_docs/`, so a wrong working directory cannot produce a green pipeline. This works because documents travel in the same PR as the code (Phase 5 rule).

Note: the copy in the repo is the authoritative one for CI; update it when you update the skill — both files, together.

**Projects whose docs root is not `ai_docs/`.** Pass `--docs-dir <name>` (e.g. `--docs-dir mkt_docs`) on any subcommand, or set `AGENTIC_SDLC_DOCS_DIR`. Without either, the validator walks up from the working directory and takes the nearest root it recognizes. If it finds two side by side — the shape of a half-finished migration — it refuses and names both rather than validating half a project and printing a verdict. `ai_docs/` remains the default and the recommended root: the parameter exists so a legacy tree can be read and migrated, not so a second one can be kept.

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
            "command": "python \"C:\\Users\\<user>\\.claude\\skills\\mkt-agentic-sdlc\\scripts\\mkt_check.py\" gate --hook --protected \"src/auth;src/crypto\""
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
- **Hybrid/devPNT projects**: add `--hybrid` to the gate command. Governed designs live in the devPNT DB, so the gate also unlocks when an approved E-TDD shadow (`ai_docs/solutions/SHADOW_*tdd*.md`, exported before implementation — see the SKILL.md shadow discipline) is present. Without the flag the gate would block legitimate governed work. The flag is deliberately explicit: never auto-detected.

## 4. SessionStart hook (orientation, recommended default)

Emits the `ai_docs/` orientation — reading guide (`README.md`), manifest (`INDEX.md`), guide router (`reference/INDEX.md`) and last `handoff.md` — plus the Rule-Zero triage reminder to stdout at session start, so the agent begins already oriented instead of reading them only if it remembers to. It is **fail-open**: a missing, unreadable or oversized doc is skipped, the output is size-capped, and it always exits 0 — a broken or empty `ai_docs/` never blocks the session. It is **zero-execution** (it reads and prints, never runs anything).

**Wire it on every project that has `ai_docs/` and a Python interpreter.** It was opt-in until v1.16.0 and the field result was the defect this level exists to prevent: the guide router stayed unread unless the user asked for it by hand, so guides were written and never consulted. Prompt-level placement (Rule Zero declares the router verdict; Phase 1 reads the router) carries the process on its own — this hook is the backstop that survives long contexts, compaction and a session that never enters Phase 1 explicitly. Skip it only where Python is unavailable, and know what you are trading.

**`init` wires it for you (F-036).** Running `init` on a project that has a docs root
and a Python interpreter now installs this hook itself — it was a manual step until
2026-08-25, and the field result was exactly the defect this level exists to prevent: an
agent worked a governed project without ever meeting the router. The snippet below is
the fallback for the cases init declines, and the list is exhaustive: **any client
other than Claude Code** (Codex and Gemini keep the manual snippet — no fixture in the
repository pins their hook schema, and writing one in an unverified shape is how a
wired-but-dead hook is born), no Python, the skill not installed yet, a settings file
that is not valid JSON or carries a `hooks`/`SessionStart` shape the writer does not
recognise (it never rewrites one it cannot read), a validator path holding a character
that cannot be placed in a command safely, or a settings file it cannot write. `init`
prints which case applied, per client — a silent skip is what let "documented default
that nobody installs" survive in the first place.

**Older and agent-bootstrapped projects are silently unwired -- `check` now tells you (F-041).**
`init` wires the hook at init time only: a project initialized before F-036, or whose
docs root was bootstrapped by the agent (which runs `index`, never `init`), never
received it retroactively -- and until F-041 nothing said so. `check` now prints, right after its summary line, a
one-line `[note]` when no orientation hook is detectable (`.claude/settings.json`,
`.claude/settings.local.json`, `.codex/hooks.json`), and a DISTINCT note when a hook is
wired but the validator it names does not resolve (the wired-and-DEAD state below --
silence there would bless the worst of the three states). The notes are informational
only: never the exit code, never a `validate` warning -- CI (`validate --strict`) does
not see them, because the wired hook legitimately lives in the git-ignored
`settings.local.json`. Known residuals, accepted as honest: a client with no hook
mechanism (Gemini today) keeps the note -- read it as the manual-reads reminder; a
`.codex/hooks.json` wired in a shape other than the documented one keeps it too.

**Which settings file, and why it is not always the shared one.** The command names a
validator, and where that validator lives decides where the hook may be written:

| Case | Command | File |
|---|---|---|
| The repo vendors the validator (§2) | repo-relative | `.claude/settings.json` — portable, commit it |
| The validator is only in your skills directory (the normal case) | absolute | `.claude/settings.local.json` — machine-specific, git-ignored; each teammate runs `init` once |

Committing an absolute `C:\Users\<you>\...` path into the shared file hands every teammate a hook naming
a directory they do not have. `init` picks the file for you, and adds
`.claude/settings.local.json` to `.gitignore` when it uses the local one.

**A hook that is wired and DEAD is the worst of the three states**: it emits nothing at
every session AND it looks installed. `init` checks that an existing hook's validator
still resolves and reports it as BROKEN with the corrected command, rather than
reporting "already wired". It never rewrites the entry — it may be hand-tuned.

Wire it via each client's SessionStart mechanism — the same command everywhere (add `--hybrid` on devPNT/Hybrid projects):

Claude Code — in the project's `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python \"C:\\Users\\<user>\\.claude\\skills\\mkt-agentic-sdlc\\scripts\\mkt_check.py\" orient"
          }
        ]
      }
    ]
  }
}
```

Codex — in `.codex/hooks.json`, the same `SessionStart` → `{"type":"command","command":"… orient"}` shape (this replaces the legacy static-echo protocol some fixtures still carry).

Gemini CLI — wire the same command into its startup-hook mechanism if present; otherwise the step simply degrades to the manual Phase-1 reads (no capability lost).

**Usage notes:**
- The hook assumes the working directory is the project root (standard Claude Code hook behavior); it also accepts `--root <path>`.
- **Hybrid/devPNT projects**: add `--hybrid` — the hook then appends a one-line pointer to run `devpnt_mcp_get_bootstrap` for the Master Plan / Knowledge Layer and does not replicate them; the filesystem orientation (router + handoff + README) still emits.
- Like the CI gate (§2), if you copied the validator into the repo, the hook references that copy — keep both files current when you update the skill.

## 5. Skill eval battery (release gate)

**Skill development only.** `test_*.py` and `evals/` are deliberately absent from the npm `files` allowlist — they never reach an installed consumer, so this section applies to whoever builds the skill, not to a project that uses it. (Consumers get `mkt_check.py` + `sdlc_core.py`; §1–§4 are theirs.)

The skill self-tests its own doctrine invariants. Two layers over one scenario corpus:

**Static battery — the deterministic release gate.** Run before any publish:

```
python -m unittest discover -s skills/mkt-agentic-sdlc/scripts -p "test_*.py"
```

It aggregates the test files (`test_plan.py` + `test_session_start.py` + `test_skill_invariants.py` + `test_domain_rules.py` + `test_golden_regression.py` + `test_mkt_check.py`) and asserts the skill's invariants: the M4 triggers/hook/worktree doctrine is present and wired, support-file pointers resolve, and the generated indexes are idempotent. A non-zero exit **blocks the release** — a failing eval is always a real regression, never flakiness: the battery is stdlib-only and makes no model or network call. One test does spawn a subprocess — `test_golden_regression.py` runs the shipped validator over a frozen corpus, which is the only way to compare what a user actually sees; it is local, offline and deterministic. If `test_indexes_idempotent` fails, run `mkt_check.py index` and re-run. If `test_golden_regression` fails, the validator's behaviour on an unchanged project changed: treat that as a regression until someone declares it intended.

**Behavioral corpus — opt-in, non-CI.** `evals/scenarios/*.md` (declarative, model-neutral) + `evals/run_behavioral.py` seed a fixture and print a prompt + pass criteria for a human/agent to run and self-assess. Because live adherence is nondeterministic, this layer **never gates** — it is the reproducible way to check that, e.g., the consult trigger actually fires on a seeded repo (the "demonstrably" artifact).

**Optional CI** (same shape as §2, not mandatory): add a `run:` step invoking the `unittest discover` command above.

**T10 note:** if you copied the validator (both files) and the `test_*.py` battery into the repo for CI, that copy is authoritative — keep it current when you update the skill.
