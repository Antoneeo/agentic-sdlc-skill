---
description: F-052 - the mandatory-read diet applied to the marketing lens, and measured NOT to apply to the knowledge lens. Extracts mkt's Hybrid seam; makes F-051's conservation check derived rather than hardcoded so it works in any lens; fixes a pre-existing dangling citation in mkt.
status: COMPLETED
end_date: 2026-09-11
feature: F-052
id: F-052
start_date: 2026-09-11
level: L3
branch: main
---
# ANALYSIS: The Read Diet, Applied Per Lens (F-052)

**Level: L3 · router: `GUIDE_release.md` → read** (a new support file must reach that package's allowlist — step 2).
Elicitation: skip path — the spec is the owner's directive of 2026-09-11 ("fai la stessa estrazione per kb e mkt"), narrowed to mkt by the measurement below and confirmed by the owner. Probes: `harness_mkt_read_diet/probe.py`.

## The measurement that changed the instruction

The instruction was "do the same for kb and mkt". Measured against the real cost
of the pointer F-051 actually shipped (979 B of pointer + 303 B of support-list
line = **1,282 B**):

| Lens | Extractable Hybrid block | Net effect on its `SKILL.md` |
|---|---|---|
| **kb** | **299 B** (a mode subsection; kb has no Coexistence section at all) | **−983 B saved = the file GROWS by 3.4%** |
| **mkt** | **2,866 B** (mode block + its own ownership matrix, contiguous) | **−1,905 B measured = −8.2%** |

So kb is **measured and deliberately not done**: extracting 299 B at a cost of
1,282 B would fatten the mandatory contract in the name of a diet, add a twelfth
support file and an allowlist entry to maintain, and violate F-051's own rule,
which authorizes a move only where a session pays for something it cannot use —
not where the move costs more than the thing moved. That is an outcome, not an
omission, and it is recorded here so a later reader does not "finish the job".

mkt clears the same bar the code lens did (−8.2% measured, against −9.4%), so it
proceeds. **Counted on both sides, as the Vision's ceremony clause requires and as
F-051 established** — the projection in the row above was pre-implementation; these
are the shipped figures, printed by the unit's own probe:

| mkt session | Before | After | Delta |
|---|---|---|---|
| **Standalone** | 23,120 B | 21,215 B | **−1,905 B (−8.2%)** |
| **Hybrid** | 23,120 B | 21,215 + 3,438 = 24,653 B | **+1,533 B (+6.6%)** |

The Hybrid surcharge is proportionally larger here than the code lens's +3.9%,
because mkt's pointer costs nearly as much while its contract is half the size.
Said plainly: the diet helps the Standalone majority and costs the Hybrid minority
more in this lens than in the last one.

## What the inbound-citation sweep found, before anything moved

F-051's blocking finding was that its weighing never asked **who cites the moved
sections**. Run first this time, the sweep produced two defects — both caught
before the move rather than after:

1. **The shared battery would have failed in mkt.** `test_hybrid_seam_moved_not_deleted`
   hardcodes the code lens's anchors (`### Shadow discipline (Hybrid)`,
   `### Feature state mapping`, `### Triage equivalence`). mkt's seam contains
   none of them — it has `### Ownership matrix (the Hybrid seam)`,
   `Authoritative hierarchy:` and `Hybrid rules:`. A hardcoded conservation list
   is a per-lens assumption living in a shared file.
2. **mkt's `ENFORCEMENT.md:60` cites a section that has never existed in mkt** —
   "see the SKILL.md shadow discipline". This is pre-existing (the F-051 closure
   review noted the same sentence was already stale in kb and mkt), and it ships.

## Objective

Apply the diet where it pays, decline it where it does not, and remove the
per-lens assumption from the shared conservation check so the next lens costs
nothing to verify.

## Vision Alignment

Goal 4 again ("lowering that price without losing the process is real work"),
with the same ceremony counting F-051 established: the saving is Standalone's and
the Hybrid session pays a small surcharge. The admission test does not apply —
cost changes, capability does not (ledger r14, as ruled for F-051).

## Use Cases / User Needs

- **UC1 — the Standalone marketing session** stops reading 2.8 KB of devPNT ownership rules it cannot act on.
- **UC2 — the Hybrid marketing session** reaches them through a pointer whose trigger is mechanical.
- **UC3 — whoever diets the next lens** gets a check that carries no lens's headings AND still proves the content survived: anchors derived, reference stamped per lens.

## Functional Spec

1. mkt's `SKILL.md` loses the contiguous Hybrid block and gains a pointer carrying trigger and consequence, in mkt's own vocabulary.
2. `mkt-agentic-sdlc/hybrid.md` carries the block **verbatim and contiguous**.
3. **The shared conservation check keeps BOTH directions, with the reference as per-lens data.** Deriving anchors from `hybrid.md` alone can only ever detect duplicates — delete a section and the derived list stops mentioning it, so the gate goes green on the one failure it exists to catch (mutation-proved by both reviewers). So each lens's `hybrid.md` records `<!-- moved-block-sha256: … -->` of the block it received, and the shared check asserts the block still hashes to it: conservation returns to the SHIPPED battery, and no lens's headings live in the shared file. The duplicate direction stays derived.
4. mkt's `ENFORCEMENT.md` citation is repointed to where the content actually lives.
5. kb is untouched, and the reason is recorded.

## Capability Ledger

All capabilities EXIST — F-051 built the pattern (pointer idiom, allowlist entry,
profile declaration, README duty, conservation probe). This unit applies it and
generalizes one check. Nothing is constructed.

## Impact

| Path | Change | What |
|---|---|---|
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` | MODIFY | remove the block, add the pointer, declare `hybrid.md` in the support list |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/hybrid.md` | ADD | the moved block, verbatim |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py` | MODIFY | the lens profile's `support_files` — the battery enforces it in both directions |
| `distributions/mkt-agentic-sdlc/package.json` | MODIFY | `files` allowlist |
| `distributions/mkt-agentic-sdlc/README.md` | MODIFY | support-files bullet and Runtime Shape tree |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/ENFORCEMENT.md` | MODIFY | the dangling citation |
| `scripts/test_skill_invariants.py` **(shared battery, port ×3)** | MODIFY | conservation check derived, not hardcoded |
| `harness_mkt_read_diet/probe.py` | ADD | P1-P7 |
| `harness_mandatory_read_diet/probe.py` (F-051's) | MODIFY | the encoding fix and the digest anchor land here too — a prior unit's harness, changed by this one and therefore owed a row |
| `skills/agentic-sdlc-skill/hybrid.md` | MODIFY | **repair**: F-051 left it mojibake-corrupted (a `git show` decoded through the console codepage). Rebuilt from the pre-move source; the digest now recorded in it comes from that source, not from the artifact |
| `distributions/kb-agentic-skill/.../ENFORCEMENT.md` | MODIFY | the identical dangling citation, retired family-wide rather than left shipping in one lens |
| closure artifacts | ADD/MODIFY | ADR decision, HANDOFF, REVIEW_LOG rows, manifests, generated indexes |

Blast radius: the shared battery changes, so it ports to all three lenses and its
new form must stay green in the code lens, green in mkt, and skip cleanly in kb.
**The first cut of this change weakened the gate** — it replaced a two-directional
check with a one-directional one and claimed the opposite; the byte-contiguity
compensator it cited lives only in a repo-local harness that ships nowhere. The
shipped form is the digest stamp above, and it is mutation-verified: deleting a
section from `hybrid.md` now turns the battery red, where the derived-only version
stayed green.

## Security and Threat Model

No code path, no input parsing. The one surface is the same as F-051's: a pointer
to a file the tarball omits is worse than the inline text, so the allowlist and
the profile are in the Impact and pinned by a probe.

## Action Plan

1. Harness RED.
2. Move verbatim; pointer; profile, allowlist, README; the ENFORCEMENT citation.
3. Generalize the shared check; port ×3; manifests.
4. Harness GREEN; three batteries; `npm pack` for mkt; `benefit` before/after.
5. Design review, closure review.
6. Closure: ADR decision recorded, REVIEW_LOG rows, registration, `mark`.

## Test Strategy

Same load-bearing pair as F-051, one of them now generalized: byte-level
contiguity of the moved region, and a **derived** heading-conservation check that
makes no assumption about which lens is being diced. Plus the packaging reality
check (mkt's `npm pack` must carry the file) and the kb non-decision, asserted so
it cannot be silently "finished": kb's `SKILL.md` must still contain its Hybrid
mode block.

## Diary

- **2026-09-11 — opened.** The instruction was "both lenses"; the measurement said one. kb's extractable block is 299 B against a 1,282 B pointer cost, so the diet would grow the file it is supposed to shrink — reported to the owner before acting, and confirmed. The inbound-citation sweep, run first this time because it was F-051's blocking finding, caught two defects before the move: a shared battery whose conservation anchors are the code lens's, and a citation in mkt pointing at a section that has never existed there.
