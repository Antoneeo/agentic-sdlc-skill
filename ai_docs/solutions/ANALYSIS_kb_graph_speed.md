---
description: F-069 - make the kb graph check fast enough for the ingestion step without narrowing it. The probe found the cost in two mechanisms of the shared knowledge.py, not in ledger size; remove them with byte-identical output. No --only flag; the field re-measures and a node-scoped check becomes a unit only if graph stays slow.
status: COMPLETED
end_date: 2026-10-16
feature: F-069
id: F-069
start_date: 2026-10-16
level: L3
branch: feat/kb-graph-only
---
# ANALYSIS: kb graph fast enough for the ingestion step (F-069)

**Level: L3 · router: `GUIDE_shared_project_memory.md` → read.** The change lands in
`knowledge.py`, a file of `scripts/shared_manifest.json` identical in all four
distributions; the guide governs validator composition across them. Elicitation: the
spec is the field measurement and the owner's scope ruling after the probe, in
`audit/requests/REQUEST_kb_graph_only.md` (R1–R3). Mode: Standalone (devPNT off,
`audit/project_notes.md`).

## Objective

F-068 made the kb ingestion step end with `graph` until clean. On the K-02 ledger
(2183 claim rows, 139 sidecars — field report, R3) the field agent measured `graph` at
46 s and `check` at 60 s (F-068 R4), so a step meant to take seconds waits most of a
minute every time it re-runs `graph`. The agent asked for `graph --only <nodo>`; the
field report conditions it: "Se `graph` resta lento sulla KB intera, un'opzione
`--only <nodo>` lo renderebbe adatto al passo" (R1).

The probe shows the time goes to two mechanisms whose cost is a product of two counts,
not to the work the check must do. Removing both keeps the full check — every row,
every cross-node relation — and makes it fast. The owner chose this scope (R2): speed
first, no flag, the field re-measures.

## Feature Vision

Vision: `vision/project_vision.md`, `Status: APPROVED` (v8). Benefit traced: the Core
Problem, **Myopia** — "an agent acts from partial understanding" (`## Core Problem`). A
node-scoped check is a deliberately partial view of a ledger whose relations
(`CONTESTED` sets, superseded citations) cross nodes; a full check fast enough to run at
every step keeps the step complete. Actor served: **Solo developer using an AI agent**,
and the **Practitioner in a non-code domain** who runs kb-agentic — "Good UX = ceremony
proportional to risk" (`## Actors`): adding three rows should not cost a minute of
waiting. Non-Goals: none touched — no flag, no state, no selection of work (the
work-management Non-Goal), no new artifact, no second triage authority. Success signal:
the field's `graph` on K-02 returns in seconds with the findings it returns today
(Action Plan step 7).

## Probe (execute before specify)

`ai_docs/solutions/harness_kb_graph_only/probe.py` builds synthetic docs roots shaped
like K-02 — topics with `## Claims` tables, paged `.txt` extractions with sidecars,
superseded rows, validity windows (some expired), one span in 50 past its page end
(43 errors), living documents citing ids, including an id inside a longer hex run and
one next to uppercase hex. It runs the working-tree `knowledge.py` and, with
`--baseline <ref>`, the one at that ref, each in a fresh interpreter, and **asserts
byte-identical transcripts** of `graph`, `corpus`, the `kb_time_cycle` result and its
warn lines, exiting 1 on any mismatch; `--profile` adds a cProfile of `graph`.

Measurements (local disk):

| Shape | rows / artifacts / pages / superseded / living | `graph` on `main` | `kb_time_cycle` | `kb_check_claims` |
|---|---|---|---|---|
| known | 2183 / 139 / 40 / 80 / 300 | 2.8–5.6 s | 0.8 s | 1.8 s |
| mature | 2183 / 139 / 200 / 400 / 1000 | 14–20 s | 10.4 s | 2.5 s |

A first prototype (monkeypatching both mechanisms out, since replaced by the
`--baseline` comparison) ran the mature shape in 1.4 s with identical output.

Findings, by profile:

1. **`kb_time_cycle` — one regex scan per (living document, superseded id).** The
   `cited` loop calls `_kb_hex_bounded(text, old)` for every superseded id against every
   living document, and again for each successor; the `expired` loop does the same per
   expired window. Cost = superseded × living × document size: 426 234 searches at the
   mature shape. It grows with the history of the KB.
2. **`kb_check_claims` — one read and one resolution per row.** For each source of each
   row, `sdlc_core.confine_under` resolves the path (`Path.resolve`, 4 737 calls) and
   `kb_check_locator` reads the whole cited extraction and splits it into pages: each of
   the 139 artifacts is read ~16 times. On the OneDrive-synced folder where the field
   ledger lives (F-068 R4), resolution and opens plausibly cost more than here.

Which cost dominates depends on the KB's history: at the known shape cost 2 does, at the
mature shape cost 1. A node-scoped check would reduce cost 2 but not cost 1 — whether a
living document cites a superseded id is answered by reading every living document,
whichever node is in scope. This unit removes both. Limit: the synthetic shape does not
reproduce 46 s; the field's superseded and living counts are unknown here. The field
number is re-measured after the release.

`kb_corpus_check` with the cycle precomputed costs 0.09 s at the mature shape: not a
target. The rest of `check` (the spine's validate and stale, ~14 s in the field by
difference) is out of scope.

## Use Cases / User Needs

- **UC1 — the step re-runs `graph`.** The solo developer's agent, or the practitioner's,
  adds claim rows at an ingestion step and runs `graph` until clean, sometimes several
  times. Need: each run returns in seconds on a mature ledger, with today's findings.
- **UC2 — closure runs `check`.** `check` computes the time cycle once and runs graph
  and corpus on it. Need: the closure gate gets the same speed-up, reporting the same.
- **UC3 — session orientation.** The session-start count line runs `kb_time_cycle` at
  every session start on a kb project. Need: no long pause before the first prompt on a
  mature KB, and no new cost on a young one.

## Functional Spec

1. For any docs root, `graph`, `corpus`, `stale`, `check`, `validate` (kb surface) and
   the orient count line print **byte-identical** output and return the same exit code
   as on `main`. Findings remain per row, each with its own file and line.
2. No text is scanned once per superseded id or per validity window: each living
   document is read for citations once, and what remains per id or window is a set
   lookup. On a KB with neither, the citation pass adds nothing.
3. One check run reads and resolves each distinct cited file a bounded number of times —
   once for its locators, plus once for its frontmatter when it has no sidecar — however
   many rows cite it.
4. Nothing is remembered between runs: a file changed between two runs in one process is
   seen as changed.

## Interface Contract

No actor-facing surface changes: commands, flags, messages, exit codes and file formats
are identical (Functional Spec 1).

## Capability Ledger

| Capability needed | Verdict | Where |
|---|---|---|
| Tell which ids a text cites (bounded 12-hex) | EXISTS, replaced | `_kb_hex_bounded` (per id) becomes `KB_HEX_TOKEN_RE` + `_kb_hex_tokens` (per text); no other id-token extractor exists in `knowledge.py`, `sdlc_core.py` or `sdlc_check.py` |
| Memoize per-run file facts inside `kb_check_claims` | EXISTS, extended | `fm_cache` / `_declaring_frontmatter` (`kb_check_claims`); the same per-call pattern now also covers resolution and locator extents |
| Path confinement | EXISTS, unchanged | `sdlc_core.confine_under` |

## Impact

| Path | Change | Responsibility | Why it changes |
|---|---|---|---|
| `skills/agentic-sdlc-skill/scripts/knowledge.py` | MODIFY | shared validator | S1, S2 below |
| `distributions/{kb-agentic-skill,course-creator,mkt-agentic-sdlc}/skills/*/scripts/knowledge.py` | MODIFY (copy) | same file, per distribution | the spine is one file; copied byte-identical |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` + the three distribution copies | MODIFY (generated) | spine integrity | `shared_files.py --update` records the new hash |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_kb_graph_speed.py` | ADD | pins | Test Strategy |
| `ai_docs/solutions/harness_kb_graph_only/probe.py` | ADD | evidence | the equivalence/timing probe above |
| `ai_docs/solutions/ANALYSIS_kb_graph_speed.md`, `ai_docs/audit/requests/REQUEST_kb_graph_only.md`, `ai_docs/audit/HANDOFF_kb_graph_speed.md` | ADD (HANDOFF deleted at closure) | unit records | this unit |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | MODIFY | review record | design and closure rows |
| `ai_docs/INDEX.md`, `ai_docs/strategic/features_history.md`, `ai_docs/audit/handoff.md`, `ai_docs/memory/INDEX.md` | MODIFY (generated) | indexes | `index` at closure |
| `ai_docs/audit/audit_plan.md` | MODIFY (by `mark`) | scope ledger | areas re-marked after the commit |
| `CHANGELOG.md` + the three distribution CHANGELOGs | MODIFY at release, not in this unit | release notes | every package ships the changed spine; written by the release unit, per `GUIDE_release.md` |

**S1 — citations by token set** (`kb_time_cycle`). Define once:

```python
KB_HEX_TOKEN_RE = re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{12}(?![0-9a-fA-F])")

def _kb_hex_tokens(text):
    """The ids a text cites: every 12-lowercase-hex run bounded by non-hex."""
    return frozenset(KB_HEX_TOKEN_RE.findall(text))
```

`kb_time_cycle` keeps `living` as `(rel, text)` and, only when `superseded` or
`windows` is non-empty, computes each living document's token set once; a document's `cited` entries come
from intersecting its token set with the superseded ids, and every `expired` question
becomes set membership. `_kb_hex_bounded` is removed: two
definitions of "a bounded citation" are how they would drift apart.

Equivalence: for a pre-validated 12-lowercase-hex `x`, `_kb_hex_bounded(text, x)` is
true iff some position holds `x` with non-hex (or the text edge) on both sides. Two
bounded runs cannot overlap — a match at position i requires i−1 to be non-hex, so no
earlier match covers it — so `findall`'s non-overlapping scan returns every one. All ids
that reach the scan come from `KB_HEX12_RE` (lowercase): superseded keys, successors,
window ids. A fuzz of 680 000 comparisons found 0 mismatches (`REVIEW_LOG.md`, design row).

**S2 — per-run memo** (`kb_check_claims`, `kb_check_locator`). `kb_check_claims` keeps,
next to `fm_cache`, a dict from each distinct source path string to its `confine_under`
result and `is_file()` answer. `kb_check_locator(target, loc, where, errors, cache=None)`
takes an optional dict the caller owns, keyed by the path actually read (the stored
`.txt` for the page form, `target` for the line form), with values holding only what the
checks compare against: the list of page lengths for the page form, the line count for
the line form, and `False` when the extraction does not exist. The text itself is not
kept, so memory stays O(pages), not O(corpus). `kb_check_claims` passes one dict per
call; `kb_resolve_anchor` and `test_claim_ledger.py` pass none and behave as today.
The memo lives in the call and is dropped with it (Functional Spec 4).

**Blast radius** — grep over the whole worktree, all files, tracked and untracked,
excluding the four identical `knowledge.py` copies; each call site read:

- `_kb_hex_bounded` — `kb_time_cycle` ×3 (cited, successors, expired). No test or
  harness references it; the probe imports only public functions.
- `kb_check_locator` — `kb_check_claims` (passes the cache), `kb_resolve_anchor` (none),
  `test_claim_ledger.py` (four positional arguments). The parameter is optional, so a
  missed caller still works.
- `kb_time_cycle` — signature and return unchanged; callers `kb_validate_surface`,
  `kb_cmd_graph`, `kb_cmd_corpus`, `kb_cmd_check`, `kb_cmd_stale`, `kb_cmd_orient`,
  `test_kb_time_cycle.py` (12 call sites), `harness_sdlc_kb_integration/probe.py`, and
  this unit's probe (through the CLI functions).
- `sdlc_core.confine_under`, `sdlc_core.read_text` — not modified; called fewer times.

**Populations at rest.** None of the four triggers fires: no invariant moves between
read-time and write-time, nothing is written (the validator is read-only here), no
format changes, no redact/mask/filter/sanitize/authorize function is touched.

## Security and Threat Model

- **Path confinement.** S2 calls `confine_under` once per distinct source string per
  run instead of once per row. `confine_under` is deterministic for a given string and
  tree, and the memo is dropped at the end of the call, so no decision outlives the run.
- **Mid-run change.** A file changing between two rows of one run is now read once, not
  twice: the check sees one consistent snapshot, the stronger behaviour.
- **ReDoS.** `KB_HEX_TOKEN_RE` is a fixed pattern with no nested quantifiers: linear.
- **Memory.** The memo stores page lengths and line counts, never the extracted text,
  and the token sets are at most one frozenset of 12-char ids per living document:
  bounded by the number of pages and ids, not by corpus size. Today's peak is one
  extraction in memory at a time; S2 keeps that, and S1 adds nothing beyond the texts
  `living` already holds on `main`.

## Action Plan

1. Probe with `--baseline` assertion (done in the design pass; green against `main`
   trivially before implementation).
2. RED: `test_kb_graph_speed.py`, failing on `main` (T1, T2).
3. Implement S1 and S2 in `skills/agentic-sdlc-skill/scripts/knowledge.py`.
4. Copy to the three distributions; `shared_files.py --update`; manifests identical.
5. Batteries: code lens, kb, course, mkt; probe `--baseline main` must print
   `identical: True` on both shapes and exit 0; record before/after times in the Diary.
6. Closure review; `index`; gate `check` clean; commit; `mark`; delete the HANDOFF.
7. After release: ask the field to time `graph` and `check` on K-02. If `graph` is still
   too slow for the step, `--only` opens as its own unit with this probe as baseline.

## Test Strategy

`test_kb_graph_speed.py` pins the mechanism, not a wall-clock budget (timing in CI is
noise):

- **T1 — one token pass per living document.** Tree: 20 superseded ids, 2 expired
  windows, 30 living documents. Wrap `knowledge.re.search` and swap
  `knowledge.KB_HEX_TOKEN_RE` for a counting wrapper (pattern attributes are read-only)
  during `kb_time_cycle`. Pass: no `re.search` call per (document, id); token extraction
  calls ≤ living documents. RED on `main`: ≥ 600 searches and no `KB_HEX_TOKEN_RE`.
- **T1b — no scan on a young KB.** No superseded ids, no windows: zero token extractions.
- **T2 — one read per cited file.** 50 rows citing one paged extraction **that has a
  sidecar** (so `_note_frontmatter` reads the sidecar, not the extraction): count
  `sdlc_core.read_text` calls on the extraction's path during `kb_check_claims`. Pass: 1.
  RED on `main`: 50.
- **T3 — per-row findings survive the memo.** Three rows citing one missing extraction,
  three rows whose spans pass a page end, and three rows whose line spans pass the end
  of one note: three findings each, each at its own line.
- **T4 — no cross-run memo.** Run `kb_check_claims`, grow the cited file so a failing
  span becomes valid, run again in the same process: the second run is clean.
- **T5 — output identity.** The probe's `--baseline main` assertion (Action Plan step 5)
  is the acceptance test for Functional Spec 1 at scale; the existing
  `test_kb_time_cycle.py` boundary tests (longer hex run, either case, generated files,
  tombstones, given/ exempt; 37 tests) and the claim-ledger battery pin it per case and
  must stay green unchanged.

## Out of scope

- `graph --only <nodo>`: deferred by the owner (R2) until the field re-measures.
- The spine's share of `check` (validate + stale, ~14 s in the field by difference):
  not profiled here; a separate unit if the field numbers show it matters.

## Diary

- 2026-10-16 — Opened from F-068 R5 ("`graph --only` is the next unit") and R1 here.
  Probe before design: the time is in `kb_time_cycle`'s per-pair scans and in
  per-row reads/resolutions, not in ledger size; a prototype gave 16 s → 1.4 s with
  identical output. The owner narrowed the unit to speed without a flag (R2). The
  folder `harness_kb_graph_only` and branch `feat/kb-graph-only` keep the name the unit
  was opened under.
- 2026-10-16 — Design review: FAIL -> PASS -> PASS (final at round 3); findings and fixes in
  `audit/reviews/REVIEW_LOG.md`. The probe now asserts identity against a baseline ref.
- 2026-10-16 — Approved (R5). RED on `main`: T1, T1b (no `KB_HEX_TOKEN_RE`) and T2
  (50 reads for 50 rows) failed; T3, T4 green by design. S1 and S2 implemented in
  `knowledge.py`, copied to the three distributions, manifests regenerated (22 shared
  files identical). Probe `--baseline main`: identical on both shapes, exit 0;
  `graph` known 2.9 s -> 1.9 s, mature 14.1 s -> 4.1 s cold (0.8 s warm under the
  profiler; the remainder is first reads of ~80 MB of extractions). Batteries: code
  249 OK, kb 439 OK (5 new), course 255 OK, mkt 261 OK.
- 2026-10-16 — Closure review: PASS -> PASS (`REVIEW_LOG.md`, closure row); the cited
  loop now intersects each token set with the superseded ids, and T3 gained a line-form
  case. Final: probe identical on both shapes (mature 14.2 s -> 4.2 s); tests 6 OK;
  batteries code 249, kb 440, course 255, mkt 261 OK.
