# KB Agentic Skill for Claude Code, Gemini CLI, Google Antigravity & Codex

`kb-agentic` turns an AI agent into the keeper of a second brain built **on the documents you supply** — not on what the model remembers. It supports Claude Code, Codex, Gemini CLI, Google Antigravity 2.0, Cursor/Windsurf-style project instructions, and optional devPNT governance.

The sibling of [`@antoneeo/agentic-sdlc-skill`](https://www.npmjs.com/package/@antoneeo/agentic-sdlc-skill), transplanted from source code to knowledge: same process, one different fidelity discipline.

## What it does

Two axes are kept apart on purpose — **abstraction** (a topic made of topics: the graph edges) and **certainty** (how strongly the corpus supports a statement: the claim rows).

1. **Intake — the source becomes untouchable.** Every document enters verbatim under `corpus/given/`, content-addressed by a raw-byte digest. A new version is appended with `supersedes:`, never overwritten. Non-text files get a **stored canonical extraction** (`.txt`, registered extractor) — those are the bytes locators point at, so an id stays valid across re-ingestion. On a large binary corpus the extraction **is** the artifact: the digest moves onto it (immutability still enforced, on the bytes that actually matter) and the original stays where it lives, recorded as `original_path:` + `original_sha256:`. 233 MB of manuals do not enter your repository to protect bytes no locator addresses — and the two recorded fields are honest about their limit: they let a human re-verify, they check nothing on their own. Spoken input is a note with `origin: elicited`; a synthesis carries `derived_from:`; your decision carries `basis:`. A note with none of the three is model knowledge dressed as a source, and the validator rejects it.

2. **Extraction — the unit is the claim.** Rows of `id | claim | valid | qty | about | source | prov | state`. The **id hashes the location and the quantity, never the text**, so an LLM rephrasing mints no new identity. The locator (`p=17@412-509`) is verified: the validator opens the extraction and checks the span exists — and `anchor <path> <phrase>` produces it for you, matching spaces as `\s+` because a PDF extraction breaks phrases mid-line. **Gates are extracted alongside powers**: for every row saying what something can do, the source is asked what must hold first — default-off, licence tier, version floor, dependency — because "yes, supported" without the gate is a plan that fails on site. The rule is *ask*, never *produce*: a source that states no gate yields no row. Validity scopes are half-open ("until March" and "from March" do not conflict). Quantities are typed — mixed kinds or currencies **refuse to sum**. What the source does not assert becomes a `gaps:` line, never a claim.

   **The source is exhausted, not sampled.** "Invents nothing" is a floor, and an extractor that stops when nothing it wrote is false stops on page twenty of a two-hundred-page manual with every row correct — which is exactly what a 200-page manual produces in the field. So a long source is read in **bounded windows** (30 pages by default, one plan task each, the ledger holding your place across sessions), and every window closes by advancing `extracted_through:` on the artifact's sidecar. That field is what makes "I am finished" falsifiable: claims with no coverage recorded are an error, a claim addressing a page past the declared coverage is a contradiction, and coverage short of the end is reported until it reaches it. Its limit is stated where it is written — **nothing proves a page was read**; what changes is that the shortcut must now be written down to pass. And exhaustive means read, never *a row per page*: a page that asserts nothing yields nothing.

3. **Placement — five verdicts, after querying the graph.** Descent through the generated index following every parent (polyhierarchy). EXISTS → reconcile; INADEQUATE → child; **MISSING only after the graph was actually asked**; GENERALIZES → escalate (a new root stops at you); UNPLACED → quarantine. Similar-but-maybe-different becomes a sibling **with the distinguishing line written** — if you cannot write it, it is the same concept. Cycles are refused at write time; merged nodes leave a tombstone with `redirect_to:`, never a deletion.

4. **Reconciliation — the machine detects and holds, it never decides.** Five outcomes: new / confirmation (the source is appended to the row — the base strengthens, it does not lengthen) / refinement (the old row goes `SUPERSEDED`, its text intact) / coexistence (disjoint scopes) / conflict → the whole set goes `CONTESTED`, **symmetrically**: flipping one cell by hand fails the check. Only new information resolves it — a later source, or **your ruling with a `basis:`**, the fact you know and the corpus does not. No basis, no ruling: a preference is not a fact. A ruling is challengeable — a later document reopens the case with your basis beside it.

5. **Escalation in one batch at the end of the run**, in legal form (the claims, the reopenable sources, the dates, why the machine cannot decide). Ingestion never stops to interrogate you.

Deliberately absent: any per-node coverage or completion state. `gaps:` says what a node lacks; nothing collects it into a dashboard. A **source** does record how far it has been read, but on its own sidecar and nowhere else — the corpus index prints that fact for every artifact, including the finished ones, because a list of only what is behind is the dashboard this method refuses.

## Key features

- **Risk-proportional triage, measured in knowledge and never in files**: one claim row → propagating a fact already settled → a new knowledge unit (a source ingested, a node created or superseded, the hierarchy moved). Carrying one settled fact into eight documents is small; one claim that re-parents a node is not. A **Write Triggers** table maps each knowledge event to exactly one destination.
- **Portable knowledge**: `export` bundles a subgraph together with the bytes its claims cite — a closure, not a selection, because a claim whose source cannot be reopened is model knowledge arriving by another route. `import` merges it into another project **additively**: it never overwrites a node and never deletes, and claims already present are recognised by id rather than by comparing text, since the same artifact cited at the same span mints the same id in every project. Knowledge crosses the project boundary; **authority does not** — an imported ruling arrives as `prov: IMPORTED`, keeps its original `basis:`, and cannot settle a local disagreement until you re-ratify it.
- **Several people, one project**: the workstream registry (`audit/handoff.md`) is **generated** from one file per open workstream, so two people opening or closing two workstreams on two branches edit two different files and their merge is clean. Row-per-workstream alone was not enough — a file-global `Date:` header defeats row-level ownership — so the header is derived from the sources and no writer touches it. The generated view can still conflict; that conflict is resolved by re-running `index`, never by hand, and `validate` refuses CLEAN until the file matches its sources. The append-only review log gets `merge=union` (a built-in driver, no per-clone configuration). It all works with no VCS at all: it is files and a generator.
- **Vision-guided governance**: Standalone projects use `ai_docs/vision/`; Hybrid projects use devPNT `M-VISION` as the milestone north star. `DRAFT` informs, `APPROVED` binds, promotion is the user's alone.
- **Independent review, twice**: the design before it is implemented, the result before it is declared done — fresh-context subagent > one-shot run > a declared self-pass, 3 rounds max, one log line each, and a PASS is invalid on "found nothing".
- **Question discipline**: a question is legal only when the agent searched first, names the search with its result, and names the decision it unblocks; otherwise it proceeds on a declared assumption, batched.
- **Operative guides + agent-global KB**: distil user-provided indications into source-faithful `GUIDE_*.md` (`source_kind: document`) — verbatim snapshot plus hash, so drift is detected mechanically.
- **Mechanical checks**: `check`, `validate`, `index`, `graph`, `corpus`, `claim-id`, `anchor`, `export`, `import`, plus the spine's `stale`/`mark`/`gate`/`plan`/`orient`/`migrate`. The graph and corpus checks verify spans against the stored extraction, recompute every id, refuse cycles and unreachable nodes, and enforce `CONTESTED` symmetry.
- **Installed support files**: Claude, Codex, Gemini and Google Antigravity receive the full skill folder — `SKILL.md`, `templates.md`, `taxonomy.md`, `distillation.md`, `reconciliation.md`, `guides.md`, `vision.md`, `elicitation.md`, `review.md`, `dispatch.md`, `routing.md`, `ENFORCEMENT.md`, and the validator's two files, `scripts/sdlc_check.py` + `scripts/sdlc_core.py` (the core is the family's shared spine — copy both, or neither).

## Installation

```bash
npm install -g @antoneeo/kb-agentic-skill@latest
```

That is enough — the package's `postinstall` runs the installer. If your npm blocks
install scripts (`--ignore-scripts`, some CI/pnpm setups), run it by hand:

```bash
kb-agentic-install-skill
```

> The command is on your PATH only after a **global** (`-g`) install; after a local
> `npm i`, invoke it as `npx kb-agentic-install-skill`.

The installer copies `skills/kb-agentic-skill/` recursively into native skill locations:

- Claude Code: `~/.claude/skills/kb-agentic/`
- Codex: `~/.codex/skills/kb-agentic/`
- Gemini CLI: `~/.gemini/skills/kb-agentic/`
- Google Antigravity: `~/.gemini/config/skills/kb-agentic/` (override the home with `ANTIGRAVITY_HOME`)

Restart the relevant agent, or reload skills where the CLI supports it.

Initialize a project:

```bash
kb-agentic-init
```

Run it inside a project to create `ai_docs/`, Vision documents, strategic docs, audit plan, and agent protocol files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`).

## The family: three lenses, one spine

| Package | Faithful to | Unit of work |
|---|---|---|
| [`@antoneeo/agentic-sdlc-skill`](https://www.npmjs.com/package/@antoneeo/agentic-sdlc-skill) | this repository's code | feature |
| `@antoneeo/kb-agentic-skill` (this one) | the documents you supply | topic |
| [`@antoneeo/mkt-agentic-sdlc-skill`](https://www.npmjs.com/package/@antoneeo/mkt-agentic-sdlc-skill) | market evidence | engagement |

Triage, the Vision Gate, the review gates, the guide router, question discipline and the validator spine are byte-identical across the three. When two live in the same project, `routing.md` decides which lens owns a given piece of work, and any of the three validators gives the same verdict on the same tree.

## Standalone vs Hybrid

- **Standalone** — `ai_docs/` is the source of truth: vision, topics, corpus, audit, handoff.
- **Hybrid with devPNT** — devPNT governs `M-VISION`, Master Plan, Action Plan and versioned artifacts; `ai_docs/` stays as readable context, fallback and shadow. Divergence between your request, the local Vision and the M-VISION is surfaced before any work.

## Created By

Created by **Antonio Pinto** ([GitHub](https://github.com/Antoneeo)).

MIT (c) 2026 Antonio Pinto.
