# Domain Routing — which lens owns this unit of work

The family ships as sibling skills built from one shared core: each lens carries its
own **fidelity discipline** (what the work must be faithful to) and its own validation
rules, over **one** `ai_docs/` tree. This file answers one question: *which lens's
method governs THIS unit of work?* It does not decide where the resulting file is
stored (step 5), and it never runs before the triage level is known — L1 never
reaches it.

## 0. Installed-lens detection — run first, fail open

Look in the skills directory this skill was loaded from for sibling lenses of the
family, identified by the `name:` in their `SKILL.md`:

| Lens | Skill name | Faithful to |
|---|---|---|
| code | `agentic-sdlc` | this repository's code |
| knowledge | `kb-agentic` | documents the user supplied |
| marketing | `mkt-agentic-sdlc` | market evidence |

- **No sibling installed, or the directory cannot be read** → the router does NOT run.
  Work under the loaded lens; read no further. This is the normal single-lens case and
  it costs nothing.
- **At least one sibling installed** → run the router below, after the level test, on
  every L2, L3 and Spike.

Fail-open is deliberate: a detection that cannot answer must never block the work. A
single-lens project that silently gains a router verdict it cannot act on is worse
than no verdict at all.

## 1. The router

Run the steps in order. Stop at the first one that decides.

1. **Fidelity / purpose.** What must the work be faithful to?
   - *This repository's code* → provisional **code**; continue to step 2.
   - *Documents the user supplied* → **knowledge**. Decided.
   - *Market evidence* → **marketing**. Decided.
   - *A deliverable whose purpose is market-facing persuasion* (copy, positioning,
     campaign material) → **marketing regardless of source**. Decided. Without this
     branch the marketing lens is reachable only when the *source* is market evidence,
     never when the *purpose* is marketing — and the launch post written from the
     release notes routes to code.

2. **Deliverable class** — only on the provisional `code` branch. The predicate is on
   the deliverable, not on its audience:
   - *Part of this repository's own document set, shipping and maintained with the
     code* (`ai_docs/`, README, CHANGELOG, comprehension guides, migration notes) →
     **code**; continue to step 3.
   - *A standalone knowledge deliverable whose fidelity extends beyond this repo's
     code* (user documentation for an external audience, a distilled corpus) →
     **knowledge**. Decided; step 3 is not reached.

3. **Build-consumed override** — only on the provisional `code` branch, never
   overriding a *marketing* or *supplied-documents* verdict. *Is the deliverable a
   file the project's build or test toolchain consumes?* Executable or imported
   source: yes. Committed Markdown: no. A yes confirms **code**.

4. **Split rule.** A request whose work must be faithful to two sources is **two units
   of work**, split before routing: the distillation (knowledge) and the design that
   cites it (code) each route alone. The router returns one lens per unit; it never
   returns two lenses for one unit.

5. **Owning tree.** A straddling artifact keeps its lens for *method* and takes this
   repository's tree and validator for *storage*. Lens and location are separate
   answers — a marketing-lens document written in a code repository still lives in
   that repository's `ai_docs/` and passes that project's validator.

6. **Cross-check.** If the verdict contradicts an installed skill's `description`, the
   descriptions are wrong: fix them. Never silently override the test with a
   description.

## 2. Worked verdicts

| Request | 1 | 2 | 3 | Lens |
|---|---|---|---|---|
| "write the API reference docs" (hand-written, ships with the repo) | code | repo's own doc set → code | not build-consumed → no flip | **code** |
| "write user documentation for our customers' admins" | code | standalone knowledge deliverable → knowledge | n/a (left the code branch at 2) | **knowledge** |
| "write the API reference docs" (generated — the work edits docstrings in source) | code | repo's own doc set → code | **build-consumed: yes → confirms code** | **code** |
| "write a comprehension guide for the auth module" | code | repo's own doc set → code | not build-consumed → no flip | **code** |
| "turn these vendor specs into a technical design" | split (step 4): spec = supplied docs; design = this repo | — | — | **knowledge** for the distillation; **code** for the design, citing it |
| "write the pricing page copy from our market research" | **purpose: market-facing → marketing** | never reached | never reached | **marketing**; stored in this repo's tree (step 5) |
| "write the launch blog post from the release notes" | purpose: market-facing → marketing | never reached | never reached | **marketing** |

## 3. Acting on the verdict

The verdict binds the **method and the validation rules**, not the storage:

- **Verdict = the loaded lens** → continue; nothing changes.
- **Verdict = a sibling lens** → say so, and work that unit under the sibling's method
  and its rule set (its templates, its mandatory risk section — code
  `## Security and Threat Model`, knowledge `## Sources and Verification`, marketing
  `## Threat Map / Plan Risks`). The artifact is written with an explicit
  `domain:` field so the answer survives the session, and it stays in this project's
  `ai_docs/` tree (step 5).
- **The unit was split** (step 4) → route and declare each half separately.

Documents under `vision/` — the project vision, principles, the roadmap — sit **above**
the domain split: they belong to no lens and are validated by the core's structural
rules only. The router is not consulted for them.
