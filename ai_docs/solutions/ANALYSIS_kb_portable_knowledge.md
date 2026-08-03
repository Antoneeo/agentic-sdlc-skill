---
id: F-030
feature: Portable knowledge — export a KB subgraph from one project, import it additively into another
status: COMPLETED
level: L3
start_date: 2026-08-03
end_date: 2026-08-03
---
# Feature Analysis: Portable knowledge

## Objective

Knowledge built in one project cannot leave it. A practitioner who grounded 82 claims
against a vendor's manuals in project A starts project B with nothing, and pays the
whole ingestion cost again from the same sources. Owner's ask (2026-08-03): *"un export
ed import della kb di un progetto per poterla trasferire in un altro progetto, **in
aggiunta**"* — additive, never replacing what the target already holds.

The Core Problem this methodology exists against is that *"the understanding it paid to
build evaporates"*. Today it evaporates at the **project boundary**, and nothing in the
product reaches across it.

## Feature Vision

**Precedent** (`vision/rulings.md`, before any prose). No row matches: this answers a
question none of r1–r15 has ruled — *can knowledge already grounded here be carried,
with its evidence, into another repository of the same owner?* So the prose rules once
and the verdict becomes a new row.

- **r2 / r3 / r9 not entered.** Nothing here collects per-work state, orders work, or
  outputs a selection-by-state. The export manifest lists what a bundle *contains*, keyed
  by artifact — an inventory for lookup, the permitted form. It crosses the line the
  moment it reports what is "missing", "stale" or "worth importing next"; that is the
  guard, stated so the check is possible.
- **The user's guarantee, on the free side and firmly.** This is one user moving their
  own data between their own repositories on their own machine. The guarantee's dividing
  line — *"could a single user get this from their own data on their own machine?"* —
  answers yes, so it may **never** be metered, tiered or account-gated, and it belongs
  in the skill, not in devPNT. What devPNT may charge for is the genuinely multi-person
  form (team-wide sharing of a bundle, cross-repository analysis over repositories the
  user does not hold); the single-user path stays here, free, and must remain reachable
  with devPNT absent.
- **Goal advanced.** Goal 2, *"keep understanding durable … so nothing load-bearing
  lives only in a transcript"*, read at the boundary it currently stops at. Deletion
  test: remove this and knowledge grounded in A must be re-derived in B from the same
  sources at full cost — the Core Problem, one scope up. Actor 4, *Practitioner in a
  non-code domain*, is the one who pays that cost.
- **Non-Goal 3 (ceremony).** Two commands, invoked when wanted. Nothing becomes
  mandatory at any level; L1 never meets them. No ratchet.
- **Non-Goal 4 (no coupling).** The bundle format is ours — plain files, no format
  defined by any other tool, nothing read from or taught about one. Counterfactual
  holds: no other project's release changes what this produces.

**Non-goals of this feature.** No sync, no remote, no network — a bundle is a directory
or an archive the user moves however they like. No merge of two claim *texts*: claims
are never rewritten by import. No deletion in the target, ever (the doctrine is
tombstones over deletion, and an additive import has no business removing anything).

**One decision is the owner's and is stated below rather than assumed** — what an
imported `RULING` becomes. See `## The ruling question`.

## Use Cases / User Needs

- **Practitioner in a non-code domain** (Actor 4) — has grounded a vendor's manuals in
  one engagement and starts a second for a different client on the same product: the
  vendor knowledge transfers with its evidence, the client-specific knowledge does not.
- **Practitioner in a non-code domain** — splits one overgrown KB into two projects and
  needs a subgraph to move without losing the spans its claims cite.
- **Solo developer using an AI agent** (Actor 1) — keeps a personal KB of standing
  vendor facts and seeds each new project from it.
- **A cold agent in the target project** — can reopen every imported claim's source,
  because the bytes travelled with it; an import that broke that would be model
  knowledge arriving by another route.

## Capability Ledger

Architect pass. `distributions/` is ANALYZED in `audit_plan.md`; the search below covers
the full `kb_*` inventory in the entry point.

| Capability | Verdict | Owning component / gap | Evidence |
|---|---|---|---|
| Decide where an incoming concept belongs in an existing graph | **EXISTS** | `taxonomy.md` — the placement pass, five verdicts (EXISTS / INADEQUATE / MISSING / GENERALIZES / UNPLACED) plus `owns:` as the anti-double-placement device | re-read: this is *exactly* the per-topic decision an additive import needs. Import is not a new merge algorithm; it is the existing placement pass run over an incoming set |
| Recognize that two claims are the same fact | **EXISTS** | `kb_claim_id` (`sdlc_check.py:158-162`) | re-read: `sha256(path#locator#qty)[:12]`, **text excluded on purpose**. The same content-addressed artifact cited at the same span yields the **same id in any project**, so dedup is mechanical rather than heuristic — the single fact that makes this feature cheap |
| Refuse a claim whose source cannot be reopened | **EXISTS** | `kb_check_claims` → `confine_under` + `kb_check_locator` (`:304-313`, `:401-431`) | re-read: a source that does not resolve is an error. This is what forces the export to be a **closure** — ship claims without their bytes and every row fails, which is the correct outcome, not a bug to work around |
| Detect a half-imported conflict set | **EXISTS** | CONTESTED symmetry check (`:387-394`) | re-read: a row pointing at a row that does not point back is an error. So "export the whole contested set or none of it" is a *requirement the validator already enforces*, not a nicety |
| Confine writes to the docs root | **EXISTS** | `sdlc_core.confine_under` | re-read: already used for claim sources. An import writes files from an outside bundle — the classic path-traversal surface — and the guard exists |
| Bundle a subgraph plus its corpus closure into one transferable artifact | **MISSING** | — | searched `export`, `import`, `bundle`, `pack`, `transfer` over the kb scripts and support files; no owner. `migrate` (`sdlc_core.py:1821`) **relocates one docs root**, it does not read or merge a second |
| Merge an incoming subgraph additively into a populated graph | **MISSING** | — | same search. Nothing in the product reads two trees at once |
| Carry an owner's ruling across a project boundary | **MISSING — and contested** | `PROVENANCES = (GIVEN, ELICITED, DERIVED, RULING)` (`:83`) | re-read the enum: it has no value for *"decided, with a basis, by the owner of a different project"*. Every existing value would misdescribe it. This is the owner decision below, not a design detail |

## The ruling question (owner decision, non-blocking)

`RULING` means *the fact you know and the corpus does not*, carrying a `basis:` given by
**this** project's owner; `reconciliation.md` makes it the only thing that resolves a
CONTESTED set. Importing one unchanged makes another project's decision binding here,
with authority nobody in this project ever granted — the machine deciding, which the
whole reconciliation doctrine refuses.

Three ways out, with what each costs:

| Option | What happens on import | Cost |
|---|---|---|
| **A — new provenance `IMPORTED`** (recommended) | the row keeps its text, span and original `basis:` verbatim, and says plainly that its authority is foreign. It cannot resolve a CONTESTED set here until the owner re-ratifies it, which is one ruling with a local `basis:` | one value added to an enum; every check that reads provenance must learn it |
| **B — demote to `DERIVED`** | no schema change | `DERIVED` means *agent synthesis*, so the row would lie about where it came from — and the honest limit is exactly what this product keeps writing down |
| **C — keep `RULING`** | nothing to build | another owner's decision silently binds here. This is authority laundering and it is the one outcome I would refuse to ship without you saying so |

Recommendation: **A**. I will proceed on A unless you say otherwise; it is reversible
(an unused enum value costs nothing) and it is the only option that keeps the knowledge
without moving the authority.

## Impact

Design in one line: **export writes a closure** — the chosen topics plus every corpus
artifact, sidecar and note their claims cite — and **import runs the existing placement
pass over it**, adding only, deduplicating by claim id, and refusing anything that would
leave the target's own checks failing.

| Path | Change | Why |
|---|---|---|
| kb `scripts/sdlc_check.py` | MODIFY | `export` and `import` subcommands; closure computation; per-topic placement report; digest verification on ingest; `confine_under` on every written path |
| kb `portability.md` | ADD | the method: what a bundle is, what closure means, how placement decides per topic, what import refuses and why. The support file the two commands cite |
| kb `SKILL.md` | MODIFY | support-file pointer; overlay command list (the F-029 invariant fails otherwise, by design); Write Triggers row for the bundle |
| kb `templates.md` | MODIFY | bundle manifest template; `IMPORTED` provenance if option A |
| kb `reconciliation.md` | MODIFY | if option A: an `IMPORTED` row cannot resolve a CONTESTED set until re-ratified |
| kb `distillation.md` | MODIFY | if option A: the provenance list |
| kb `scripts/test_claim_ledger.py` | MODIFY | closure, dedup, refusal branches — one test each |
| kb `evals/scenarios/` | ADD | cold-run: import into a populated graph must run placement, not overwrite |
| kb `README.md`, `strategic/skill_family_agent_workflows.md` | MODIFY | derived documents |
| `CHANGELOG.md` | MODIFY | `[Unreleased]` |

**Blast radius (enumerated).** `PROVENANCES` (`:83`) is read by the provenance check in
`kb_check_claims` and by `reconciliation.md`'s resolution rule — those two are the whole
consumer set for option A, verified by grep over the entry point and the support files.
The spine (`sdlc_core.py`) is **not** touched: this is kb's own method, so the drift
guard must still find the three copies identical. `migrate` is untouched and unrelated —
naming it here so the next reader does not mistake one for the other.

## Security and Threat Model

A bundle is **external input** arriving from outside the docs root, so this is never L1
and the surface is real.

| Threat | Answer |
|---|---|
| **T1 — authority laundering**: an imported `RULING` decides conflicts in the target | the ruling question above; option A makes foreign authority visible and inert until re-ratified |
| **T2 — path traversal**: a bundle whose manifest names `../../etc/x` writes outside the docs root | every written path goes through `confine_under`; a path that escapes aborts the whole import, never just that file. Refuse the bundle, do not sanitize it |
| **T3 — half a conflict set arrives**, breaking CONTESTED symmetry the target enforces | export computes the closure over conflict sets too, and import **refuses** a bundle whose sets are incomplete. Better to refuse than to import a tree whose `check` fails |
| **T4 — name collision with different bytes**: two projects hold `manual-ab12cd34.txt` with different content | content-addressed names carry a digest of the bytes, so equal name should mean equal bytes. Verify on import; a mismatch is a refusal with both digests printed, never a silent overwrite |
| **T5 — slug collision merges two different concepts** (`pricing` here, `pricing` there) | the placement pass decides per topic — EXISTS / INADEQUATE / sibling with the distinguishing line written. Bodies are never auto-merged, and `owns:` keeps one fact from landing twice |
| **T6 — an import invents new roots** | `GENERALIZES` already escalates to the owner and stops there; import inherits that, it does not get an exemption |
| **T7 — dangling `supersedes:` / `parents:`** after import | part of the closure; anything unresolved after import is reported and the bundle is refused |
| **T8 — the bundle carries executable content** | files only, no execution, no archive auto-extraction beyond plain reads; the validator stays zero-execution as everywhere else |

## Action Plan

- [x] **A — owner decision** on the ruling question (proceeding on option A by default).
- [x] **B — `portability.md`**: bundle shape, closure rule, placement-on-import, the
      refusal list. Doctrine before code, as everywhere else.
- [x] **C — `export`**: closure computation + manifest; refuses to write a bundle whose
      own claims would not validate.
- [x] **D — `import`**: placement per topic, dedup by claim id, digest verification,
      `confine_under` on every write, all-or-nothing refusal.
- [x] **E — `IMPORTED` provenance** (if A): enum, provenance check, reconciliation rule.
- [x] **F — tests and a cold-run scenario**; derived docs; closure.

## Test Strategy

- **Round trip**: export a subgraph, import into an empty target, `check` CLEAN and the
  claim ids identical to the source project's — the id-stability property is the
  feature's foundation, so it is tested, not assumed.
- **Additive**: import into a target that already holds an overlapping topic → the
  existing node survives, the new claims land under the placement verdict, nothing is
  overwritten, nothing deleted.
- **Dedup**: import the same bundle twice → the second is a no-op, proven by identical
  ids rather than by text comparison.
- **One refusal test per branch** (F-027's lesson — a test tripping two branches lets
  either be deleted with the suite green): path escaping the docs root; digest mismatch
  on a same-named artifact; incomplete CONTESTED set; dangling `supersedes:`.
- **Cold-run scenario**: an agent given a bundle and a populated graph must run the
  placement pass and report verdicts; overwriting a node is a FAIL.
- **Family**: batteries ×3, drift guard identical, `npm pack` unchanged in shape.

## Diary / Current State

**2026-08-03 — opened, not implemented.** Standalone, devPNT off.
`Level: L3 · router: no match`.

The architect pass changed the shape of this feature before any code was written. Three
things the product already owns do most of the work: the placement pass is exactly the
per-topic decision an additive import needs, so import is not a new merge algorithm; the
source-resolution check forces the export to be a **closure**, which is a constraint
rather than an obstacle; and the CONTESTED symmetry check turns "ship the whole conflict
set or none" into something already enforced.

The load-bearing discovery is `kb_claim_id`: `sha256(path#locator#qty)` with the text
deliberately excluded, so the same artifact cited at the same span mints the **same id
in any project**. Deduplication across projects is therefore mechanical, not a judgement
call — which is why this feature is small rather than large.

What is genuinely new is small and hostile: bundling a closure, merging additively, and
one question that is not mine to answer — whether another owner's `RULING` keeps its
authority here. Recorded above with a recommendation rather than assumed away.

**2026-08-03 — implemented, A through F.** Owner ruled **option A** (`IMPORTED`).
Batteries 141/204/159 OK, drift identical, `check` CLEAN, shipped as **kb 1.2.0**.

Proven end to end on two throwaway projects rather than asserted: export from A →
import into an empty B → B's graph clean and **the claim ids identical to A's**, which
is the property the whole design rests on. Second import: zero writes, and the existing
node reported as skipped rather than overwritten.

Two things the implementation changed from the plan, both worth recording:

- **No `knowledge_portability` capability is declared.** The capability vocabulary lives
  in the shared spine, and no shared test guards portability, so adding a label there
  would have meant editing `sdlc_core.py` in three distributions to buy nothing. The
  support file IS declared, which is what the invariant actually needs.
- **The path-escape guard is belt and braces, and the analysis overstated it.** `rglob`
  under the bundle cannot produce a `..` entry, so T2's guard cannot currently fire
  through this path; `confine_under` is kept because a future bundle form (an archive,
  manifest-driven paths) would open exactly that hole. The test says so instead of
  implying a defence that is not being exercised.

**The closure review earned its place again.** It caught that `portability.md` was NOT
in `package.json` — the published skill would have shipped a `SKILL.md` citing doctrine
its own user could not open, which is the same doctrine-vs-machinery class F-029 spent a
whole release closing. Fixed, and then generalised: a new shared invariant asserts every
declared support file is packaged, so the next one cannot slip. `npm pack` went from 22
files to 23.

Open: nothing. F-028 remains PAUSED at its design gate.

