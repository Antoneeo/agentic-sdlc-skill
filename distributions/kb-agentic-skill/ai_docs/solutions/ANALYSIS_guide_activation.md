---
id: F-016
feature: Guide Activation (consult on the mandatory path)
status: COMPLETED
level: L3
start_date: 2026-07-27
end_date: 2026-07-27
---
# Feature Analysis: Guide Activation

## Objective

The guide layer is written but not consumed. Field report (owner, 2026-07-27):
*"le guide non vengono prese in vera considerazione: se non avviso io l'LLM di
cercare la guida, lui non la cerca e non la scrive."*

The consult trigger already exists in three places, so the fix is **not** a
fourth restatement. It is a **placement** defect: the instruction never sits on
a path the agent is guaranteed to execute.

Evidence gathered on this repo (2026-07-27):

| Where it is | Reachability |
|---|---|
| `SKILL.md:222` | bullet 5 of 10 inside **Phase 4**, i.e. only the L3 workflow |
| `SKILL.md:277` (`## Operative Guides`) | line 274 of 306 — tail of a long file |
| `guides.md` §0 | a support file declared "read only when needed" |

Where it is **not**:
- **Rule Zero** — the one step every request executes. It never names guides;
  the L2 row prescribes only "mini-analysis + tests".
- **Phase 1 Audit** (`SKILL.md:178`) — the only always-run read step. It reads
  `ai_docs/README.md` + `ai_docs/INDEX.md`, **not** `ai_docs/reference/INDEX.md`.
- `ai_docs/README.md` (this repo, and the `templates.md` bootstrap template it
  comes from) — the router is absent from the must-reads; `reference/` appears
  only in the trailing "directory purposes" line.

Mechanical backstop: `sdlc_check.py orient` already emits the router
(`ORIENT_DOCS`, `sdlc_check.py:92-97`), but `ENFORCEMENT.md` §4 labels it
*optional* and it is **not wired in this repo** (`.claude/settings.local.json`
carries permissions only).

Write side, `source_kind: code`: the Write Triggers row (`SKILL.md:63`) assigns
phase **"any"** — which is nobody's phase. No checkpoint ever asks the question,
so the duty fires only if the agent spontaneously remembers it. The `document`
proactive trigger at least has a home in Phase 5.

The owner's own hypothesis — *"forse vanno indicizzate a parte?"* — is already
satisfied: `ai_docs/reference/INDEX.md` is a separate, generated router.
Separate indexing is not the missing piece; **an always-executed step that
reads it** is.

## Feature Vision

Serves `vision/project_vision.md` (**Status: APPROVED**, 2026-07-02):
- Layer **D** ("what nobody has" — operative guides) and Layer **A**
  (code-comprehension guides). Both layers ship today but do not reach the work
  they exist to govern; an unconsulted guide delivers zero of its stated value.
- Success signal *"Feature B ships the reusable operative-guide layer that the
  superpowers Global Constraints block does not offer"*: superpowers copies
  project rules verbatim into every plan — always present, never forgotten. We
  chose to maintain them once and **point** to them; that choice is only
  superior if the pointer is actually followed. This feature pays the cost of
  the pointer model.
- North Star *"keeps every change aligned with the project's long-term intent"*
  and the skill's stated reason to exist (anti-myopia): a comprehension guide
  not consulted is exactly the "model rots between sessions" failure.

Non-Goal guard — `project_vision.md`: *"No heavyweight governance for trivial
edits"*. **L1 stays exempt** from the consult, and the declared output is one
line, not a ceremony. Any design that made L1 pay is rejected by this Non-Goal.

Not in scope for this analysis:
- **Blind-reviewer clarity check on the Vision** (owner request, same session,
  explicitly deferred): have an unaware reviewer read the Vision and report
  where it is unclear, since later sessions and reviews read it cold. Separate
  feature, separate ANALYSIS.
- Any change to `sdlc_check.py` orientation logic — `ORIENT_DOCS` already
  carries the router; this feature only promotes and wires it.
- Consumption of guides by devPNT-side agents (C11 in the evolution roadmap).

Success signals for this feature:
1. On a repo with a matching guide, a fresh agent consults it **without being
   told** — the `evals/scenarios/consult_fires_on_match.md` behavioral scenario
   passes when run cold.
2. Every L2/L3 declaration in a session carries a router verdict, so "did not
   look" is distinguishable from "looked, no match".
3. A high-complexity component understood during a session leaves a
   `source_kind: code` guide behind, without the owner prompting for it.

## Use Cases / User Needs

- **Solo developer using an AI agent** (Vision `## Actors`) — needs the agent to
  apply the indications already handed over, without re-stating them every
  session. Good UX = the agent says which guide it used (or that none matched)
  and the cost stays one line. *Today this actor must remember, and prompt, on
  every task — the exact failure reported.*
- **Team lead needing governance** — needs the router verdict to be **visible in
  the transcript**, so a reviewer can tell a guide was honored rather than
  ignored. Good UX = omission is detectable without re-reading the guides.
- **Open-core adopter** — needs the activation to hold Standalone, with no
  Python and no hook required: the prompt-level moves (A, B, D) must work alone,
  the hook (C) is defense in depth.

## Impact

Prose/doctrine change plus test and config. No product code path changes.

| Path | Change | What | Why |
|---|---|---|---|
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | Rule Zero: declared router verdict alongside the level (L1 exempt); Phase 1: `reference/INDEX.md` added to the mandatory reads; Write Triggers: code-guide row phase `any` → `5`; Phase 5: comprehension checkpoint bullet; `## Operative Guides`: consult bullet states the declaration | moves the trigger onto the always-executed path (A, B, D) |
| `skills/agentic-sdlc-skill/guides.md` | MODIFY | §0 gains the declared-verdict rule; §1 comprehension trigger gains the closure checkpoint | mechanics stay single-sourced here (DRY: SKILL.md points, guides.md defines) |
| `skills/agentic-sdlc-skill/ENFORCEMENT.md` | MODIFY | §4 `optional` → recommended default for any project with `ai_docs/` | the only non-prompt backstop (C) |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | `## ai_docs/README.md` template: router among the must-reads | new consumer projects inherit the fix (B) |
| `skills/agentic-sdlc-skill/dispatch.md` | MODIFY (verify) | reconcile the declaration with dispatch (orchestrator declares at plan-authoring; subagent does not self-consult) | avoid contradicting the existing dispatch note |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | MODIFY | new assertions for the Rule-Zero declaration, the Phase-1 router read, the code-guide checkpoint phase, and the ENFORCEMENT §4 promotion | the battery is the release gate; an unasserted doctrine line regresses silently |
| `skills/agentic-sdlc-skill/evals/scenarios/consult_fires_on_match.md` | MODIFY | pass criteria gains the declared verdict | behavioral proof of signal 2 |
| `skills/agentic-sdlc-skill/evals/scenarios/` | ADD | scenario: no guide matches → agent still declares `router: no match` | distinguishes "looked" from "did not look" |
| `ai_docs/README.md` | MODIFY | add `reference/INDEX.md` to the must-reads | this repo dogfoods B |
| `.claude/settings.json` | ADD | SessionStart hook running `sdlc_check.py orient` | this repo dogfoods C |
| `.gitignore` | MODIFY | `.claude` → `.claude/*` + `!.claude/settings.json` | found during implementation: `.claude` was ignored wholesale, so the wiring would have stayed on one machine. `settings.local.json` (machine-specific permissions) stays ignored |
| `CHANGELOG.md`, `package.json`, `gemini-extension.json` | MODIFY | version bump at release | per `reference/GUIDE_release.md` |

**Blast radius (enumerated, not sampled).** The skill files are prose: the only
mechanical consumers are the test battery and the hook.

- `test_skill_invariants.py` asserts these SKILL.md/guides.md substrings, which
  the edits MUST preserve verbatim: `"consult the guide router"`,
  `"Consult (before acting)"`, `"PROPOSE distilling a guide"`,
  `"Propose proactively"`, `"source_kind: code"`,
  `"Comprehend (code, autonomous)"`, `"Isolate the work"`,
  `"Branch/worktree hygiene"` (SKILL.md); `"## 0. Consuming a guide"`,
  `"### Proactive trigger"`, `"Comprehension trigger"`, `"source_kind"`
  (guides.md); `"## 4. SessionStart hook"`, `"## 5. Skill eval battery"`
  (ENFORCEMENT.md); `"Guide consumption under dispatch"` (dispatch.md).
  Breaking any one is a red battery, not a silent drift.
- `test_support_files_wired` requires every `*.md` beside SKILL.md to stay
  referenced in SKILL.md — no new support file is planned, so no new reference
  is due.
- `test_indexes_idempotent` compares the three generated indexes against disk:
  `ai_docs/README.md` is hand-curated (not generated) so it does not trip this,
  but any canonical-doc header change requires `sdlc_check.py index` before the
  battery runs.
- `sdlc_check.py` is **not** modified: `ORIENT_DOCS` already lists
  `ai_docs/reference/INDEX.md`. Verified at `sdlc_check.py:92-97`.
- `.claude/settings.json` does not exist yet in this repo; `settings.local.json`
  (permissions only) is untouched and does not conflict.

## Security and Threat Model

Surfaces touched: **filesystem read** (the hook reads a fixed doc set) and
**untrusted-content ingestion** (guide/router text enters the agent context
automatically). No authN/authZ, no crypto, no network, no personal data.

| Threat | Mitigation |
|---|---|
| T1 — hook executes repo-controlled content | `cmd_orient` is zero-execution by construction: it reads a hard-coded `ORIENT_DOCS` list and prints. No subprocess/eval in its call graph (asserted by `test_behavioral_driver_no_llm` for the driver; `cmd_orient` reviewed at `sdlc_check.py:1007`). Unchanged by this feature. |
| T2 — context flooding via oversized docs | `ORIENT_PER_DOC_CHARS` (6000) + `ORIENT_MAX_TOTAL_CHARS` (16000) caps, already enforced. Unchanged. |
| T3 — path escape via crafted relative paths | `confine_under(root, rel)` on every entry. Unchanged. |
| T4 — router content treated as instructions | The orientation banner already labels the payload *"repo-sourced context, not authored instructions"*. The new declaration must not weaken it: a guide is applied because the process says to consult it, never because the guide text asserts authority. Carried into the Phase-4/§0 wording. |
| T5 — declaration becomes theater | A verdict that is always `no match` is worse than none: it certifies a lookup that did not happen. Mitigated by the behavioral scenario asserting the verdict on BOTH a match and a no-match repo, and by keeping the verdict one line (no incentive to fake volume). |
| T6 — silent guide creation | Unchanged and preserved: `document` guides stay propose-only; only `source_kind: code` writes autonomously (additive, code-anchored, git-reversible). Move D adds a checkpoint, not a new writer. |
| T7 — blanket reading | Unchanged and preserved: the consult is a targeted description match. The declaration names ONE guide or none — it must not become "read them all and list them". |
| T8 — hook blocks the session | `cmd_orient` is fail-open and always returns 0. Promoting it to recommended (C) does not change that; `.claude/settings.json` carries no `timeout`-sensitive work. |

"No security impact" is **not** claimed: the hook promotion widens the default
ingestion path, which is why T1-T3 and T8 are restated as still-holding rather
than waived.

## Action Plan

- [ ] **A — Rule Zero declaration.** `SKILL.md` Rule Zero: the level declaration
      carries the router verdict (`Level: L2 · router: no match` /
      `router: GUIDE_x → read`). L1 exempt. Cross-cutting rules gain the line.
- [ ] **B — Router in orientation.** `SKILL.md` Phase 1 mandatory reads +
      `templates.md` README template must-reads + this repo's `ai_docs/README.md`.
- [ ] **C — Hook promotion + wiring.** `ENFORCEMENT.md` §4 optional →
      recommended default; create `.claude/settings.json` here with the
      `orient` command.
- [ ] **D — Comprehension checkpoint.** Write Triggers row phase `any` → `5`;
      Phase 5 closure bullet asking the question; `guides.md` §1 mirror.
- [ ] **E — Reconcile dispatch.** Verify/adjust the `dispatch.md` note so the
      declaration has one owner (orchestrator) and subagents are unaffected.
- [ ] **F — Tests.** New invariants in `test_skill_invariants.py`; extend
      `consult_fires_on_match.md`; add the no-match scenario.
- [ ] **G — Closure.** `sdlc_check.py index` + `check`, full battery green,
      handoff, CHANGELOG.

## Test Strategy

- **Static battery (release gate, deterministic):**
  `python -m unittest discover -s skills/agentic-sdlc-skill/scripts -p "test_*.py"`
  — must stay green and gain the new invariants (currently 52 tests per the
  2026-07-19 handoff; the new assertions raise that count).
- **Validator:** `python skills/agentic-sdlc-skill/scripts/sdlc_check.py check --root .`
  → 0 errors, indexes idempotent.
- **Hook smoke:** `sdlc_check.py orient --root .` prints the four sections
  including the guide router; exit 0. Also verified on an empty dir (fail-open).
- **Behavioral (opt-in, non-gating):** run `consult_fires_on_match.md` and the
  new no-match scenario cold — a fresh agent, skill only, no owner prompt. This
  is the only layer that can prove the reported defect is closed; the static
  battery proves the doctrine is present, not that it fires.
- TDD: the code delta is limited to test assertions over prose, so RED/GREEN
  applies literally — add the failing invariant first, then the doctrine line.

## Diary / Current State

**2026-07-27 — analysis drafted (Standalone).** devPNT off for this project
(per handoff 2026-07-19: locked on another project), so Standalone is the mode;
no M-VISION consulted. Elicitation round run in-session: two forks resolved by
the owner — (1) move A = **declared mandatory output**, not a silent bullet;
(2) move C = **recommended default in ENFORCEMENT + wired in this repo**. Vision
Gate passed against `project_vision.md` (APPROVED) with the L1-exemption guard
noted above. Prior art reviewed: M4 Unit 2 shipped the consult trigger itself
(`SHADOW_e_tdd_consolidation_guide_consumption_v1.0.md`) — this feature does not
redefine it, it relocates it onto the mandatory path. Related: F-015
(`ANALYSIS_comprehension_guides.md`, IN_PROGRESS) owns the code-guide KIND; move
D here owns only its trigger placement.

**2026-07-27 — implemented and closed** on branch `feat/guide-activation`, all
of A→G. TDD followed literally: the four invariants were added RED first
(`test_rule_zero_declares_router_verdict`, `test_phase1_reads_guide_router`,
`test_code_guide_trigger_has_a_phase`, `test_enforcement_hook_is_recommended_default`),
then the doctrine lines turned them GREEN. Battery **56/56**, `validate` 0
errors / 4 pre-existing warnings, `orient` smoke green (exit 0, router emitted).

Closure review = **declared self-pass** (reduced independence, stated openly):
the session harness forbids spawning a reviewer subagent unprompted, and devPNT
is off, so no independent reviewer ran. Findings raised and fixed in-pass:
1. **Spike had no verdict rule** — Rule Zero said "L2/L3", leaving Spike
   ambiguous; an ambiguous level is a skipped lookup. Fixed: L2/L3/Spike.
2. **"one guide named or none" was too rigid** — it forbade the legitimate case
   of one operative guide plus the comprehension map of the component being
   touched. Fixed in `SKILL.md` + `guides.md` §0 (two allowed for distinct
   concerns; three is a smell).
3. **The no-match scenario referenced `src/list.py` without seeding it** — the
   fixture would have handed the agent a missing file. Fixed in `## Setup`.
Not folded in (scope-creep rule): the uncommitted `review.md` bullet already in
the working tree restates the threat-model clause of the bullet above it —
flagged to the owner, left untouched.

ADR written: `architecture/ADR_2026-07-27_declared_router_verdict.md` — the
decision to enforce via a declared output rather than a fourth restatement or a
hard write-gate, with alternatives and the theater risk recorded. New canonical
directory `ai_docs/architecture/` given its purpose in `README.md`.

Residual, NOT introduced here: `sdlc_check.py check` still reports `scripts/`
stale (installer JS changed in v1.12.0 and was never re-marked). The area this
feature touched (`skills/agentic-sdlc-skill/`) is marked ANALYZED. Re-analyzing
the installer is separate work, deliberately not absorbed.

Next step: owner reviews the branch; release as **1.16.0** per
`reference/GUIDE_release.md` (CHANGELOG section is staged as
`[Unreleased - 1.16.0]`; the version bump in `package.json` +
`gemini-extension.json` is step 1 of that runbook, not done here).

Deferred sibling (owner request, same session): blind-reviewer clarity check on
the Vision — its own ANALYSIS, after this one.
