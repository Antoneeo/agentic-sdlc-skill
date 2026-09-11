---
description: ADR - a conservation check's reference is per-lens DATA (a digest stamped in the moved file) and must come from the SOURCE, never from the artifact it checks; and a per-lens diet is decided by measurement, not by uniformity. Rejected - hardcoding one lens's headings, deriving anchors alone, anchoring to git HEAD, and extracting every lens for symmetry.
status: CURRENT
---
# ADR: the conservation reference is data, and it comes from the source

**Status:** Accepted
**Date:** 2026-09-11
**Task ref:** F-052 (ANALYSIS_mkt_read_diet.md)
**Digest:** F-052 — applying F-051's read diet to a second lens exposed three failures in how a relocation is guarded: a shared check carrying one lens's headings fails in every lens shaped differently; deriving the anchors from the moved file instead only detects duplicates and goes green on the deletion it exists to catch; and a reference taken from the artifact (or from a moving `git HEAD`) certifies whatever state that artifact is in — which here meant a mojibake-corrupted file whose digest was recorded as certified. Decision: anchors derived, reference stamped as per-lens data in the moved file, computed from the PRE-MOVE SOURCE; and a per-lens diet proceeds only where measurement says it saves — kb's 299 B block against a 1,282 B pointer means declining is the correct outcome, pinned so nobody "finishes the job".

## Context

F-051 moved the code lens's Hybrid seam out of the mandatory read and guarded it
with a conservation check listing that lens's headings. Applying the same move to
the marketing lens broke three assumptions at once:

1. The shared check lives in a file byte-identical across three lenses, but its
   anchors were one lens's. mkt's seam contains none of them.
2. Deriving the anchors from `hybrid.md` instead makes the check tautological in
   the direction that matters: delete a section and the derived list stops
   naming it, so nothing fails. Both reviewers mutation-proved this — the old
   check went red on a deleted section, the derived one stayed green.
3. The byte-level reference F-051 used came first from `git show HEAD:` (which
   stops meaning anything once the unit is committed, because HEAD becomes the
   post-move state) and then from the moved file itself. The file was at that
   moment **mojibake-corrupted** — UTF-8 decoded through the Windows console
   codepage by a `git show` call with no explicit encoding — so the recorded
   digest certified the corruption.

## Decision

1. **Anchors are derived; the reference is data.** Each lens's `hybrid.md`
   carries `<!-- moved-block-sha256: … -->` for the block it received. The
   shared check derives the duplicate-direction anchors from that file and
   asserts the digest for the conservation direction. No lens's headings live in
   the shared file, and the deletion case is red again (mutation-verified).
2. **A reference is computed from the SOURCE, never from the artifact it
   checks.** The digest comes from the pre-move region, decoded explicitly as
   UTF-8. A check whose expected value is read from the thing under test proves
   only self-consistency.
3. **Every `subprocess` call that reads repository text passes
   `encoding="utf-8"`.** The platform default silently corrupts and can produce
   a false PASS as easily as a false FAIL.
4. **A per-lens diet is decided by measurement, not by symmetry.** kb's block is
   299 B against a 1,282 B pointer: extracting it grows the file it should
   shrink, so it is declined, and a probe pins the decision.

## Alternatives considered

- **Keep the hardcoded anchor list** — rejected: it is one lens's assumption in
  a shared file and fails in any lens shaped differently.
- **Derived anchors alone** (the first cut) — rejected on evidence: it silently
  drops the conservation direction while the docstring still claims it.
- **Anchor the reference to `git show HEAD:`** — rejected: a moving reference
  stops proving anything at the moment of commit, and shelling out makes the
  check depend on console encoding.
- **Extract every lens for uniformity** — rejected: kb's measurement says the
  move costs more than it removes. Symmetry is not a reason.

## Consequences

- **Pro:** the shipped battery guards the moved content again, in every lens and
  without carrying any lens's vocabulary; the corruption is repaired and could
  not have been repaired later once its digest was certified; and a future lens
  costs one stamped line to guard.
- **Con / risk:** the digest lives beside the content it describes, so an editor
  changing both keeps the gate green — it makes deletion *deliberate and
  visible*, not impossible. And mkt's Hybrid surcharge (+6.6%) is proportionally
  larger than the code lens's, because a pointer costs about the same in a
  contract half the size.
