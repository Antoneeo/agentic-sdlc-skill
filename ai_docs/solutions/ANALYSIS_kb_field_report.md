---
id: F-029
feature: kb field-report defects — triage units, precondition axis, corpus letter, anchor resolver, overlay help
status: COMPLETED
level: L3
start_date: 2026-08-02
end_date: 2026-08-02
---
# Feature Analysis: kb field-report defects

## Objective

First full application of `kb-agentic` on a real corpus by a practitioner other than
its author: 233 MB of third-party manuals grounded against marketing specs, closing at
51 corpus artifacts, 22 topic nodes, 82 offset-verified claims, 7 notes, with
`check` / `graph` / `corpus` clean. Five findings plus one triage friction.

**All six reproduced against the shipped source before being accepted.** Two are
structural, and the report's own subject line ("one structural gap") undercounts:

1. **The claim model records capabilities and skips gates**, so the ledger is
   systematically optimistic — on a corpus whose stated purpose is to deflate
   over-promising. Field evidence: 82 rows, ~3 of them preconditions. The first real
   query returned three verified rows saying "yes, supported" while omitting that the
   function ships **off by default** and needs a second construct to work at all. A
   cold agent would have answered "yes, verified" and shipped a plan that fails on site.
2. **kb's triage boundaries were never restated in this domain's units.** `SKILL.md:46`
   and `:47` carry the *identical* bound — "at most 1-2 files" — so no file count maps
   to L2 and anything touching three files falls to L3 by "when in doubt, go higher".
   The reporter's 5-file propagation of one already-settled fact tripped **none** of the
   real escalation triggers two lines below.
3. **The skill's reader is an agent, and none of these six is an adherence failure.**
   In every one the agent did exactly what it was told and still got a wrong outcome —
   which makes them **agent-UX defects**, not carelessness. They fall in three classes,
   and the third is the dangerous one because the agent *verifies* and is confirmed in
   a false belief:

   | Class | Findings | What the agent experiences |
   |---|---|---|
   | **Undecidable** — the rule cannot be applied as written | 6 (triage bounds) | must invent a resolution; the reporter deviated and declared it, the best available behaviour |
   | **Obeyable but wrong** — applying the rule faithfully produces a bad result, with no signal | 1 (extraction axis), 2 (copy 233 MB) | no way to know it went wrong |
   | **Contradicted by the machinery** — the docs or the tools say one thing, the checker another | 3 (gate with no ramp), 4 (the probe pretty-prints whitespace the checker does not collapse), 5 (`--help` denies the overlay) | forms a false model and gets it confirmed |

   The structural cause is measurable: **kb has no cold-run coverage of its own
   method.** Its six eval scenarios are the shared spine's; two are byte-identical to
   the code lens's and test an **architect pass kb does not ship**. Nothing exercises
   claim extraction, taxonomy descent, reconciliation, the corpus letter or a locator.
   The field report *is* kb's first cold run — performed by a practitioner, by
   accident, unpaid.

## Feature Vision

**Owner ruling, 2026-08-02.** Asked *"sostituiamo i conteggi di file in kb con unità di
conoscenza (quanti nodi tocca, tocca la gerarchia sì/no)?"* — answered **"Si"**.

`basis:` the Vision's North Star requires it and reserves it: *"Each sibling restates
these three boundaries in its own domain's units before it ships; the units change, the
three levels and the ceremony attached to them do not"*, and *"The owner rules on those
boundaries; a sibling does not write its own escape."* kb shipped carrying the **code**
lens's units. The ruling repairs an unfulfilled requirement; it does not widen a limit.

**Precedent** (`vision/rulings.md`, before any prose):

| Item | Row | Consequence |
|---|---|---|
| A triage units, C corpus letter, E overlay help | **r14** — *fixes a defect with purpose, actors and surface unchanged* → **exempt** | correctness only; no capability the product lacks |
| B precondition axis — the **rule** | **r14** | extraction becomes complete, not different. The artifact's shape is unchanged |
| B precondition axis — the **`kind` column** | **Non-Goal 3 budget** | a new mandatory field on every row. Admissible only if the same change removes comparable cost, or the cost is stated and accepted. **Design position: the column ships only if it feeds the `[note]` advisory** — otherwise it is an unverifiable field, the same defect class as an EXISTS naming no symbol, paid on 82 rows |
| D anchor resolver | **r15** — *packaging, installation, the product's own tests* → **ADMIT**, and it is a tool, never a step | no ratchet: nothing becomes mandatory |

**Goal / Actor advanced.** Actor 4, *Practitioner in a non-code domain*, whose
`Good UX =` clause is item A verbatim — *"the same three levels and the same gates,
restated in their own domain's units, and never being asked for an artifact that only
makes sense for code"*. Item B advances Goal 3 (*divergence visible before
implementation*): a ledger that answers "yes" while withholding the gate is divergence
the method was built to surface.

**Non-Goal 3 budget.** Item A **removes** ceremony (a 5-file propagation stops paying
L3). Item E removes a false negative. Item D adds no step. Only B's optional column
adds, and it is gated on earning it. Net negative.

**Non-Goal 1** not entered: nothing here collects per-work state or orders work.

**Non-goals of this feature.** No change to the escalation triggers (`SKILL.md:54`) —
they are already correct and already in knowledge units. No relaxation of what a
locator must satisfy. No new provenance class.

## Use Cases / User Needs

- **Practitioner in a non-code domain** (Actor 4) — propagating one settled fact into
  five notes, with no hierarchy change and no new node, is L2 and costs an L2.
- **A cold agent answering from the ledger** — receives the gates alongside the
  capability, so "yes, verified" is not a plan that fails on site.
- **Practitioner with a large binary corpus** (Actor 4) — ingests 233 MB without
  copying it into the docs root, and the digest still protects the bytes a locator
  addresses.
- **Practitioner migrating a corpus that already carries prose citations** — `[M §2.7]`
  becomes `p=27@649-656` by tool, not by hand. This was the reporter's largest cost.
- **Anyone running `--help`** — sees that the knowledge overlay is installed.

## Capability Ledger

Architect pass run before the Impact. `distributions/` is ANALYZED in `audit_plan.md`,
so the map is groundable; the function inventory below is the full 22 `kb_*` symbols.

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| Classify a knowledge change by size **in this domain's units** | **INADEQUATE** | kb `SKILL.md:46-47` | re-read both rows: L1 and L2 carry the identical bound "at most 1-2 files". Gap: no count maps to L2. The correct criteria already exist at `:54` ("ANY of these makes it L3, **whatever the file count**": hierarchy, multi-node frontmatter, supersession) and contradict the counts above them |
| Extract every assertion a source makes about a capability, **including what gates it** | **INADEQUATE** | `distillation.md:25-30` (§2) + `:61-64` (§3) | re-read: the claim is defined by falsifiability alone, and §3 says "one row per assertion". Correct and insufficient — nothing directs the extractor to ask what must hold first. Field evidence: 82 rows, ~3 preconditions |
| Report a coverage shortfall as a finding rather than as silence | **EXISTS** | `kb_check_claims` returns `(errors, warnings, notes)` (`sdlc_check.py:274-277`) | re-read: the advisory channel exists and already carries the empty-id `[note]`. This is what a `kind` column must feed to earn its cost — and what makes the cheap variant testable |
| Hold a corpus artifact whose bytes are verifiable **without copying the original** | **EXISTS — undocumented** | `kb_corpus_check:623`, `kb_check_locator:410` | re-read both: the sidecar resolves by stripping `.meta.md`, so a `.txt` extraction is already a legal artifact; and `ext = target if target.suffix == ".txt" else ...` uses it directly. It works **today**. The gap is doctrinal: `distillation.md:17` says the extraction comes "additionally", so a faithful reader copies the original as well |
| Record where a non-copied original lives and what it hashed to | **MISSING** | — | searched `original_path`, `original_sha256`, `original` over `scripts/` and the sidecar contract at `distillation.md:22` (digest, date, provenance, `supersedes:`). No owner. Not provisional: `corpus/` is fully covered |
| Turn a prose citation into a **verified offset span** | **MISSING** | — | full inventory of the 22 `kb_*` functions: `kb_check_locator` (`:401-431`) CONSUMES spans; `kb_fill_ids` (`:241`) mints ids from a locator already supplied. Nothing mints a span. Searched anchor/offset/resolve/locate over `scripts/` |
| Show the knowledge overlay's commands in usage | **INADEQUATE** | `sdlc_check.py:806` | reproduced: `--help` is not in `INTERCEPTED`, so forward-by-default hands it to the spine and usage lists nine commands with no overlay. `graph --help`, `corpus --help`, `claim-id --help` all print correctly — the overlay is present and invisible |
| Exercise **this domain's own method** on a cold agent before shipping | **INADEQUATE** | `kb/evals/scenarios/` — six scenarios, all the shared spine's | diffed all six against the code lens: `architect_rules_before_impact.md` and `unmapped_never_grounds_missing.md` are **byte-identical**, and both test an architect pass kb does not ship (`ls architect.md` → absent; they reference `architect.md`/Component Map/Capability Ledger 3 and 4 times). Zero exercise extraction, placement, reconciliation, the corpus letter or a locator. Compare **mkt**, whose six are all its own (`no_number_without_ledger`, `swap_test_enforced`, …) — so the family already knows how to do this |
| Give the agent a method for every artifact the templates demand of it | **INADEQUATE** | kb `templates.md:244` demands `## Capability Ledger`; no `architect.md` in kb; kb `SKILL.md` never mentions the pass | grep over kb `SKILL.md`: the two `architect` hits are the `architecture/` directory and `strategic/architecture.md`, unrelated. A four-way inconsistency around one construct — template asks, doctrine is silent, method absent, evals test it. The agent is asked for an artifact whose method it cannot read |

## Impact

| Path | Change | Why |
|---|---|---|
| kb `SKILL.md` | MODIFY | A: L1/L2 rows restated in knowledge units (nodes touched, hierarchy yes/no); the file counts go. `:54` untouched |
| kb `distillation.md` | MODIFY | B: §3 gains the precondition rule **and** its anti-fabrication guard. C: §1 blesses extraction-as-artifact; §1's sidecar contract gains the two `original_*` fields with their stated limit |
| kb `templates.md` | MODIFY | B (conditional): the `kind` column, only if the advisory ships. C: sidecar template |
| kb `scripts/sdlc_check.py` | MODIFY | B (conditional): the coverage `[note]`. C: accept/record `original_*`. D: the resolver subcommand. E: `--help` |
| kb `scripts/test_claim_ledger.py`, `test_kb_graph.py` | MODIFY | per item, one test per branch |
| kb `scripts/test_skill_invariants.py` | MODIFY | A: invariant that the triage rows carry no file count and the escalation triggers survive |
| kb `scripts/fixtures/` | ADD | C: a golden corpus whose artifact is an extraction with no original. D: a wrapped-line fixture |
| kb `evals/scenarios/` | ADD + DELETE | G: cold-run scenarios for kb's own method; the two byte-identical copies go, or the pass they test arrives — one direction, decided in design |
| kb `templates.md:244` (`## Capability Ledger`) | MODIFY | G: whichever direction G takes, this section stops being an orphan |
| `ai_docs/strategic/skill_family_agent_workflows.md` | MODIFY | derived doc: it describes the kb lens's triage and claim model |
| `distributions/kb-agentic-skill/README.md` | MODIFY | derived doc: the five-stage method description |
| `CHANGELOG.md` | MODIFY | `[Unreleased]` |

**Blast radius (enumerated).**
- The triage wording appears in exactly two places family-wide: kb `SKILL.md:46-47` and
  code `SKILL.md:45-46`. **No test asserts either count** (grep over `*.py` in
  `distributions/` and `skills/`), so item A is a doctrine edit plus a new invariant,
  not a code change.
- The change is **kb-only**: `sdlc_core.py` is the byte-identical spine and is not
  touched. The drift guard must still find the three copies identical afterwards.
- Item E touches dispatch, which the file's own docstring defends as
  "not intercepted -> forward, never a hand-copied command tuple". That property is
  load-bearing and must survive — see T5.
- `mkt_check.py` carries the same forward-by-default shape and, per that docstring,
  already ships the `migrate` defect. **Out of scope here, and named so it is not lost.**

## Security and Threat Model

Surfaces: filesystem, plus parsing of third-party binary documents (PDF/docx) in the
resolver — external input, therefore never L1.

| Threat | Answer |
|---|---|
| **T1** — `original_sha256` looks like a guarantee and is not: we do not hold the file, so nothing verifies it | state the limit where the field is defined, in the same form the guides state theirs: the **enforced** digest is the extraction's, and that is the one a locator addresses. A field whose limit is unstated is worse than an absent field |
| **T2** — the L2 ruling becomes a general escape hatch ("a sibling does not write its own escape") | the ruling is the owner's, recorded verbatim with its date and basis; the escalation triggers at `:54` stay untouched and keep overriding *whatever the count*. The levels and their ceremony do not move — only the units |
| **T3** — the precondition rule becomes ceremony: every capability row owes a precondition row even where the source states none | **the guard, and the reason B is not just "add a rule"**: the rule is *ask*, never *produce*. A source that asserts no gate yields no row — §3's "what the source does not assert does not become a row" still governs, and an invented precondition is exactly the fabrication the extractor exists to prevent. A missing gate is a `gaps:` entry, not a claim |
| **T4** — the resolver anchors to the wrong span; the check accepts it because a span is verified to EXIST, not to CONTAIN the claim | the resolver prints the resolved context for human verification and **refuses to emit** what it cannot anchor (non-zero exit, nothing written). The limit is stated honestly, same shape as the guides' `source_hash`: the check proves the span exists, never that it says what the claim says |
| **T5** — intercepting `--help` breaks forward-by-default, and a future spine command is silently dropped | intercept `-h`/`--help` **only at argv[0]**, still render the spine's own usage, and append the overlay's commands. Dispatch stays "not intercepted -> forward". Regression test: add a synthetic spine command and assert it still reaches the spine |
| **T6** — the resolver parses attacker-supplied PDFs | it reads the **stored extraction**, not the binary — text in, offsets out, no PDF parser in the trust path. Extraction stays the practitioner's step, as today |

## Action Plan

- [x] **A — triage in knowledge units** (owner-ruled): kb `SKILL.md:46-47` restated;
      escalation triggers untouched; invariant + mutation test.
- [x] **B — precondition axis**: the §3 rule plus the anti-fabrication guard (T3).
      **The `kind` column does NOT ship** — decided with basis: nothing mechanical can
      detect an assertion that was never extracted, so the column could feed no
      advisory and would be a mandatory unverifiable field on every row, paid on 82.
      The rule carries it, the ingestion review verifies it, and the residual is
      recorded rather than hidden behind a field that looks like enforcement.
- [x] **C — corpus letter**: §1 blesses extraction-as-artifact; sidecar gains
      `original_path` / `original_sha256` with their stated limit.
- [x] **D — anchor resolver**: prose citation → verified span, matching literal spaces
      as `\s+` so the mid-phrase line wrap is handled by construction. This **absorbs
      field finding 4** — no doctrine line is owed for a trap the tool removes.
- [x] **E — `--help` shows the overlay**, without breaking forward-by-default.
- [x] **G — agent-UX coverage**, the item that keeps the other five from recurring:
      cold-run scenarios for kb's OWN method (one per class the field report exposed —
      extraction coverage, corpus letter, locator authoring), and the Capability Ledger
      inconsistency resolved in ONE direction: either kb gains the pass in its own
      units (taxonomy placement is already that pass under another name) or the
      template stops demanding it and the two copied scenarios go. **Not both, and not
      neither.**
- [ ] **F — closure**: design review, closure review on the diff, battery ×3, drift
      guard identical, derived docs refreshed, CHANGELOG, `index`, `mark`.

## Test Strategy

- **A** — invariant: kb's triage rows carry no file count; the `:54` triggers survive.
  Mutation: restore "at most 1-2 files" → the invariant fails.
- **B** — a fixture topic with capability rows and no precondition fires the `[note]`;
  and the **anti-fabrication** test: a source stating no gate must produce no
  precondition row. The second test is the one that keeps the rule honest.
- **C** — golden corpus whose artifact is an extraction with no original present:
  `corpus` and `check` clean. Mutation: remove the extraction → the existing
  "no stored extraction" error fires, proving the check still bites.
- **D** — resolves a phrase wrapped mid-line; **refuses** an absent phrase with a
  non-zero exit and no output written. Both branches, separately (F-027's lesson: one
  test tripping two branches lets either be deleted with the suite green).
- **E** — `--help` lists `graph`, `corpus`, `claim-id`; plus the forward-by-default
  regression from T5.
- **G** — the scenarios are the test: each runs a cold agent on kb's own method and
  fails if it reproduces the field outcome (a ledger of capabilities with no gates; a
  233 MB copy into the docs root; a hand-authored locator). A static invariant also
  asserts no kb scenario is byte-identical to a sibling lens's — a copied scenario is
  how a battery reports coverage it does not have.
- **Family** — full battery ×3, drift guard byte-identical, `npm pack` unchanged.

## Diary / Current State

**2026-08-02 — opened.** Standalone, devPNT off. `Level: L3 · router: no match`.

Source: a field report from the first full application of kb by someone who did not
write it. Every finding was **reproduced against the shipped source before being
accepted** — the report was treated as evidence to check, not as a verdict.

Two diagnoses in the report needed correcting, and both change the work:

- Finding 2 is described as *impossible to satisfy*. It is not: the code already
  accepts an extraction as the corpus artifact (`kb_corpus_check:623` resolves the
  sidecar by name; `kb_check_locator:410` uses a `.txt` target directly). The defect is
  that `distillation.md:17` presents the extraction as an addition, so a faithful
  reader copies the original too. That moves the fix from redesigning the corpus letter
  to amending §1 and recording two fields — and it means the reporter's 4.4 MB
  docs root was already conformant.
- Finding 1's proposed `kind` column is only half right. The rule in §3 is free and
  attacks the real cause (coverage at extraction time). The column is a mandatory field
  on every row that **nothing can verify** — unless it feeds the advisory channel that
  already exists (`kb_check_claims` returns a `notes` list). Gated on that here.

Findings 3 and 4 are one fix, not two: a resolver that matches literal spaces as `\s+`
removes the wrap trap by construction, so documenting the trap separately would
describe a hazard that no longer exists.

The friction the report ranks last is the largest defect found: kb's L1 and L2 carry
the **same** file bound, so the domain has no L2 for anything touching three files.
Root cause is that kb never performed the restatement the Vision requires of every
sibling before it ships. Owner ruled "Si" on 2026-08-02; recorded above with its basis.

**Owner note, 2026-08-02 — "the skill is made to be used by an agent; the UX must be
optimal so the agent uses it well and misunderstands nothing."** Evaluated, and it
reclassifies the whole report: none of the six is an adherence failure. In every case
the agent obeyed and was wrong anyway, which is a property of the instruction, not of
the reader. The three classes are in `## Objective`; the one to fear is
*contradicted by the machinery*, because there the agent checks its belief and is
confirmed in it — `--help` denying the overlay, a probe collapsing whitespace the
checker preserves, a gate no tool can ramp to.

Measuring it produced a finding the report does not contain: kb's eval battery is six
scenarios, **none** covering kb's own method, two byte-identical to the code lens's and
testing an architect pass kb does not ship — while kb's ANALYSIS template still demands
that pass's `## Capability Ledger` and kb's SKILL.md never mentions it. mkt, by
contrast, wrote all six of its own. So this is not a family-wide gap in method; it is
kb shipping the spine's tests as if they were its own. Item G, and the reason the other
five must not be closed without it: they were found by a practitioner doing unpaid
QA, and nothing here would have caught the next five.

Not in scope, recorded so it is not lost: `mkt_check.py` ships the same
forward-by-default shape and, per the kb entry point's own docstring, already drops
`migrate`. That is its own unit.

**2026-08-02, later — implemented, A through G.** Batteries: code 140, kb 190, mkt 158,
all OK; drift guard identical after regenerating the three manifests.

**Two corrections to this document's own earlier text**, both found while implementing
and both changing the work:

- The Capability Ledger row said kb's doctrine was *silent* about the pass. It is not:
  the template's comment already points at `taxonomy.md` in kb's own units. What was
  actually wrong is narrower and more insidious — the **example rows** were the code
  lens's verbatim (Python paths, `grep over src/`), and an example is what an agent
  imitates far more readily than a comment. Fixed there, plus the two copied scenarios.
- The `kind` column is **not** shipping. The ANALYSIS gated it on feeding an advisory;
  on implementation the gate closed, because no advisory is constructible: nothing
  mechanical detects an assertion never extracted, and an advisory that fires on every
  topic without preconditions would be noise on legitimately gate-free concepts — which
  is the same agent-UX defect this unit exists to remove.

Two decisions worth their reasons. `merge`-style suppression was rejected for the
generated help (E) in favour of *extending* the spine's usage: replacing it would have
traded one blindness for another. And the anchor resolver re-verifies every locator with
`kb_check_locator` before emitting it, so the tool cannot produce a span its own
validator rejects — the round-trip is a test, not a comment.

Honest residuals, declared: `original_sha256` is recorded and never checked (stated
wherever the field appears); `anchor` proves a span **exists**, never that it says what
the claim says — same limit as a guide's `source_hash`; and the precondition rule has no
mechanical enforcement by design.

Closure review: **declared self-pass** (the session harness forbids unprompted reviewer
subagents; devPNT off) — independence reduced, and said so. It mapped the diff against
this Impact table row by row and found three real gaps, all closed: the sidecar template
never gained the two `original_*` fields, and both derived documents
(`strategic/skill_family_agent_workflows.md`, the kb `README.md`) still described the
old triage grain, the old intake letter and a command list without `anchor`. Deviation
from the Impact, declared: no `scripts/fixtures/` were added — the new tests build their
trees with `tempfile`, which is what the surrounding battery already does.

**2026-08-03 — three follow-up findings from the same practitioner, reading 1.1.0.**
All three verified in the source and all three of the class this unit exists to
remove — the doctrine and the machinery disagreeing:

- `SKILL.md:24` never named `anchor`, though it shipped working and listed in
  `--help`. The practitioner found the command from the prose, by accident. Now
  guarded by a kb invariant that **derives** the expected list from `INTERCEPTED`;
  a second hand-maintained list would repeat the defect rather than close it.
- `SKILL.md:86` (Write Triggers, `corpus/given/*`) still read "verbatim copy …
  non-text originals **also** get their stored canonical extraction" — the exact
  wording §1 carried *before* this unit changed it. Two rules, opposite outcomes on
  a binary corpus. Fixed by stating both forms and naming §1 as the rule's owner.
  Lesson recorded: changing a rule in its owning file is half the change; the
  Write Triggers table restates enough of it to diverge.
- `anchor` resolved paths only from inside the docs root while its siblings take
  `--root`. Made to resolve instead of documented: a path that does not resolve from
  the current directory is retried under the docs root, so it can be written exactly
  as a claim's `source` cell carries it.

Shipped as **kb 1.1.1**; 1.1.0 was already published and is tagged `kb-v1.1.0` at
the tree the registry carries (shasum verified identical to the local pack).

Open: nothing blocking. F-028 (mergeable documentation) is PAUSED at its own design gate
by owner priority. Not in scope and recorded above: `mkt_check.py`'s dropped `migrate`.
